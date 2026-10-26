# 01 环境基线（B0）

日期：2026-10-24　环境：Android 9 (API 28) (API 28)　iApp 5.0.1013

## 问题

在 Android 9 上重建投递链路，跑通最小页，并复验上一环境（Android 14）的结论。

## 读数

| 项 | 读数 | 级别 |
|---|---|---|
| adb root | `adb root` 后 `id` = uid=0 | ✅ |
| 工程根 | `/storage/emulated/0/iApp/ProjectApp/<id>` | ✅ |
| 任务书预期的 `Android/data/<包名>/files/iApp/ProjectApp` | 不存在 | ✅ |
| 共享目录 | 宿主机 `android-sync` ↔ `/mnt/shared/Pictures`，双向实时 | ✅ |
| bind mount 到 `/data/media/0` | sdcardfs 视图为空 | ✅ |
| bind mount 到 `/storage/emulated/0` | shell 可见；应用 namespace 无该挂载 | ✅ |
| push 后 iApp 渲染新内容 | 画布显示 `HOST-SYNC-OK` | ✅ |

## 最小页

`src/mian.iyu`：LinearLayout + TextView(id=2)，载入事件 `syso("loading-fired")` + `call(a,"mjava","app.bind")`
`src/app.mjava`：`bind()` 里 `syso("ok")` 并 `activity.findViewById(2).setText("Hello from mjava")`

## 证据

- 屏幕：TextView 显示 `Hello from mjava`
- logcat（同一 pid）：

```
14:37:46.632 V/ygs: loading-fired
14:37:46.648 V/ygs: ok
```

## 结论

- 与任务书预期的差异：入口在 `src/mian.iyu`；工程不在 `Android/data/...`；bind mount 不可用，改 push。
- 事件格式取自 APK dex 内置模板：`<UIEventset><eventItme type="loading">`。
- 顺带读到：可视化设计器里长按[运行]会打包安装运行（Toast 提示原文），未实测 ❓。
