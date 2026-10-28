# 交付与打包边界

版本前提：iApp 5.0.1013、API 28。

## 默认交付：`.iApp` 备份包

导出位置：`iApp/iAppDir/<包名>.iApp`（ZIP）。

结构（✅ 实测）：**顶层直接是工程内容，没有包名目录**

```
.project
AndroidManifest.xml
build.xml
icon.png
apk/assets/…              # 工程 apk/assets 的内容（含 dex 与生成的 odex/vdex）
bin/<包名>.apk            # 已构建的 APK
bin/<包名>.apk.idsig
files/…
res/
sdk/iapp.sdk
src/*.iyu, *.mjava
```

导入：直接打开 `.iApp` 文件并选择 iApp 打开；**同包名工程已存在时会提示导入失败**，需先删除旧工程。

## APK 打包（仅用户点名时）

| 项 | 读数 |
|---|---|
| versionCode | `100000 + versionint`（versionint=1 → 100001）✅ |
| versionName | 工程设置的原值（1.0） |
| minSdkVersion | 21 |
| targetSdkVersion | 36（打包产物；安装包声明为 37，见 `references/iapp-history.md`） |
| platformBuildVersionName | 21 |
| `<sdk>21` | 未观察到对 minSdk 的额外影响（该版本两处都是 21）❓ |

## 打包环境的限制（✅ 实测）

- `ygs` 日志完全无输出（manifest 里 `i_app_logOutput=shi` 也无效）—— **但 `android.util.Log` 正常**：打包版实测 `android.util.Log` 有输出、`ygs` 0 行（2026-10-27）
  - 调试一律用 `android.util.Log.i("TAG", ...)`，`i.syso` 在打包后是死的
- `com.iapp.app.VisualDesigner` 被裁掉 → 不能靠工程根定位资源
- 工程 `files/` 不进 APK；`apk/assets/` 会原样进 APK 的 `assets/`
- 外部库要在打包前转成 dex，并放到 `apk/assets/`
- 打包版 `getFilesDir()` 是打包应用自己的私有目录；开发期写在宿主 `com.iapp.app` 下的存档不会自动带过去

## 产物可移植性（侧载到其它设备）

- 打包 APK **自包含**（解释器 dex + 资源 + 原生库），目标设备**不需要装 iApp 本体** ⚠（推断：APK 结构）
- 侧载到 **OPPO Watch X2（圆表盘）** 可安装并启动 ⚠（用户口述 2026-10-28，未取 logcat）
- 原生库只有 `lib/arm64-v8a`，且 `libygsiyu.so` 是裕语言引擎（`.iyu` 解析依赖它）：
  **纯 32 位用户空间的设备装不上**（`INSTALL_FAILED_NO_MATCHING_ABIS`），删 `lib/` 重签也救不回来 ⚠（推断）
- 小圆屏 UI：`466px / 310dpi` 这类屏幕按 dp 画布（约 233dp）设计，四角会被裁掉

## 外部同步的边界

- 通过共享目录/同步盘改工程时，可能同步出**截断文件**：设备端字节数不足，iApp 报 `Parse error ... Encountered: <EOF>`。改完先核字节数/md5，不一致就重新复制或改用 `adb push`
- 工程在 iApp 里打开期间可能读到旧缓存；改完让用户关闭并重开工程，再核 md5
- 同一轮改多个文件时，可能只有部分文件同步过去；不要只看一个文件就认为整批已生效
- 没有共享目录、也没有 adb 时，可改用 iApp 内置 FTP 投递（`references/ftp-delivery.md`）；
  三条通道的取舍与共同铁律见 `references/environment-adaptation.md`

## 边界

- 默认交付 `.iApp`
- 只有用户明确点名 APK 时，才由用户在 iApp 内手动打包
