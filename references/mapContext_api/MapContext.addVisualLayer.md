# MapContext.addVisualLayer(Object object)

> **⚠️ 前置要求（必须满足，否则真机调用失败）**：
> - `layerId` 为用户在腾讯位置服务控制台创建的可视化图层 ID（创建入口：https://lbs.qq.com/dev/console/layers/layerEdit ），**agent 不得编造或使用占位符**，编写代码前必须向用户确认 layerId；
> - map 组件需配置 `subkey` 参数，且 subkey 须与 layerId 绑定；
> - 需在[图层绑定页面](https://lbs.qq.com/dev/console/layers/layerBind)授权当前小程序 APPID。

> 基础库 2.20.1 开始支持，低版本需做兼容处理。

> **以 Promise 风格 调用**：不支持
>
> **小程序插件**：支持
>
> **微信 鸿蒙 OS 版**：支持

> 相关文档: map

## 功能描述

添加可视化图层。需要刷新时，interval 可设置的最小值为 15 s。工具侧暂未支持。

> **注意事项**：
> - 使用前需在 map 组件上配置 `subkey` 参数，且 `subkey` 须与 `layerId` 绑定。
> - 需在 [图层绑定页面](https://lbs.qq.com/dev/console/layers/layerBind) 授权当前小程序 APPID，否则真机调用会失败。

## 参数

### Object object

| 属性     | 类型     | 默认值 | 必填 | 说明                                       |
| -------- | -------- | ------ | ---- | ------------------------------------------ |
| layerId  | String   |        | 是   | 可视化图层id                               |
| interval | Number   | 0      | 否   | 刷新周期，单位秒                           |
| zIndex   | Number   | 1      | 否   | 图层绘制顺序                               |
| opacity  | Number   | 1      | 否   | 图层透明度                                 |
| success  | function |        | 否   | 接口调用成功的回调函数                     |
| fail     | function |        | 否   | 接口调用失败的回调函数                     |
| complete | function |        | 否   | 接口调用结束的回调函数（调用成功、失败都会执行） |
