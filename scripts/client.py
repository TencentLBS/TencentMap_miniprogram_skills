#!/usr/bin/env python3
"""
腾讯地图小程序客户端。封装 Key 管理，自动从 tempkey.json 解析 Key。

用法：
    from scripts.client import Client

    client = Client()                # 自动解析：传参 → tempkey.json
    client = Client(key="xxx")       # 显式传 Key
    client.save_key("xxx")           # 保存正式 Key
"""

import sys, os, json
from datetime import datetime
from typing import List, Tuple, Optional

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".tencentmap", "tempkey.json")

_KEY_SOURCE_LABELS = {
    "argument": "调用时传入",
    "manual": "手动指定",
    "tempkey": "已申请的临时 Key",
}


def _mask_key(key: str) -> str:
    if not key:
        return ""
    if len(key) <= 12:
        return key[:4] + "****"
    return f"{key[:8]}****{key[-4:]}"


def _source_label(source: str) -> str:
    return _KEY_SOURCE_LABELS.get(source, source)


def _collect_tempkeys() -> List[Tuple[str, str]]:
    candidates = []
    if not os.path.exists(CONFIG_PATH):
        return candidates
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return candidates
        manual = data.get("__manual__")
        if isinstance(manual, dict) and manual.get("key") and manual.get("status") != "expired":
            candidates.append((manual["key"], "manual"))
        for phone, entry in data.items():
            if phone == "__manual__" or not isinstance(entry, dict):
                continue
            k = entry.get("key")
            expire_str = entry.get("expire_time", "")
            status = entry.get("status", "active")
            if not k or not expire_str or status == "expired":
                continue
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    if datetime.now() < datetime.strptime(expire_str, fmt):
                        candidates.append((k, "tempkey"))
                    break
                except ValueError:
                    continue
    except Exception:
        pass
    return candidates


def _collect_keys(passed_key: Optional[str]) -> List[Tuple[str, str]]:
    candidates = []
    if passed_key:
        candidates.append((passed_key, "argument"))
    candidates.extend(_collect_tempkeys())
    return candidates


class Client:
    def __init__(self, key=None):
        self._key_pool = _collect_keys(key)
        self._key_idx = 0
        if self._key_pool:
            self.key, self.source = self._key_pool[0]
        else:
            self.key = None
            self.source = "none"

    def switch_key(self) -> Optional[str]:
        """切换到候选池中下一个 Key，用于当前 Key 报错时自动轮询。
        
        :return: 新 Key 字符串，若已是最后一个候选则返回 None
        """
        if self._key_idx + 1 < len(self._key_pool):
            self._key_idx += 1
            self.key, self.source = self._key_pool[self._key_idx]
            return self.key
        return None

    def save_key(self, key):
        records = {}
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except Exception:
                records = {}
        records["__manual__"] = {"key": key, "status": "active", "source": "manual"}
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        self.key = key
        self.source = "manual"
        return CONFIG_PATH


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--save":
        c = Client()
        path = c.save_key(sys.argv[2])
        print(json.dumps({"key": sys.argv[2], "source": "manual", "saved_to": path}, ensure_ascii=False))
    else:
        c = Client()
        print(json.dumps({
            "key": c.key, "source": c.source,
            "available_keys": len(c._key_pool),
            "pool": [{ "key": _mask_key(k), "source": _source_label(src) } for k, src in c._key_pool]
        }, ensure_ascii=False))
