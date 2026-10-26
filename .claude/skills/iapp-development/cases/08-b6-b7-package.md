# 08 静态分析与打包边界（B6/B7）

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## B6 静态读数

| 项 | 读数 | 与预期 |
|---|---|---|
| `i` 类 | `com.iapp.app.Aid_javaCode` | 一致 |
| 公开方法（反射） | **390** | 预期 381（版本差异） |
| 公开字段 | **12** | 一致 |
| `ss_dim` | static HashMap，默认 null | 一致（解释 `i.ss` NPE） |
| `qm` | 307 字段、0 方法；`n` 是 HashMap | 部分印证「i.sss 落 qm.n」 |
| `.project` 的 toolversion | `iApp V5.0.1013` | 一致：IDE 版本 |
| `<yuv>` | 3 | — |

## B7 打包读数

| 项 | 读数 |
|---|---|
| versionCode | **100001** = 100000 + versionint(1) ✅ |
| versionName | 1.0 |
| minSdk / targetSdk | 21 / 36 |
| platformBuildVersionName | 21 |
| 打包后 `ygs` 日志 | **完全没有**（manifest 已带 `i_app_logOutput=shi`） |
| 打包后 `VisualDesigner` | ClassNotFoundException（被裁） |
| 工程 `files/` | 不进 APK |
| 工程 `apk/assets/` | 原样进 APK 的 `assets/`，并生成 odex/vdex |

## 结论

- 打包环境不能靠日志取证，必须把结果写到界面控件
- 打包环境不能靠工程根找外部库；用 assets 释放或 `getExternalFilesDir`
- 交付默认 `.iApp`；APK 需用户点名并在 iApp 内手动打包

## 未决

- `.iApp` 备份包结构（顶层是否直接是工程目录）、导出/导入行为 ❓
- `<sdk>` 是否只改 platformBuildVersionName（本机 minSdk 也是 21，无法区分）❓
