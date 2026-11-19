# 红米 Note 8（真机，侧载 / 运行目标）

## 元信息

| 项 | 值 |
|---|---|
| 环境 ID | R8（运行目标，不是开发主机） |
| 宿主 | **M2**（用户确认 2026-11-19）：Windows 11 Pro 10.0.26300、Hyper-V 开启、装了腾讯应用宝电脑版；adb 用产品自带 `adb.EXE`（1.0.41）。M1 是另一台 Win10 + 雷电环境 |
| 核验时间 | 2026-11-19 |
| 当前状态 | adb 直连可用；API 30 / arm64+armv7；iApp 5.0.1015 已装；`tools/push.py` 整目录推送成功 ✅ 2026-11-19 |
| 用途 | Android 11 真机验证（填补模拟器之外的 API 30 读数） |

## 识别方法

- `adb devices -l` 看 `model`：`Redmi_Note_8`，`device:ginkgo`（本机实测）。
- serial 每次现查：`cdc69048` 是 2026-11-19 的读数，**不作为常量**。
- 连上先核 `ro.build.version.sdk`，本机为 30。

## 系统

| 项 | 读数 | 级别 · 来源 · 日期 |
|---|---|---|
| 型号 / 厂商 | `Redmi Note 8`（`ro.product.model`）/ `Xiaomi` | ✅ adb 2026-11-19 |
| 代号 / 平台 | `ginkgo` / `trinket`（高通骁龙 665 平台） | ✅ adb 2026-11-19 |
| Android / API | 11 / 30 | ✅ adb 2026-11-19 |
| MIUI | `V125`，构建 `V12.5.5.0.RCOCNXM` | ✅ adb 2026-11-19 |
| 安全补丁 | 2022-07-01 | ✅ adb 2026-11-19 |
| 系统构建日期 | 2022-08-01 | ✅ adb 2026-11-19 |
| 内核 | `4.14.190-perf-gc61d39ef577d-dirty`，aarch64 | ✅ adb 2026-11-19 |
| ABI | `arm64-v8a`、`armeabi-v7a`、`armeabi` | ✅ adb 2026-11-19 |
| 屏幕 | 物理 1080×2340 | ✅ `wm size` 2026-11-19 |
| 密度 | `wm density` 440（比例 2.75 → 约 393dp 宽） | ✅ adb 2026-11-19 |
| 内存 | `MemTotal` 5,761,544 kB（约 5.5 GiB） | ✅ `/proc/meminfo` 2026-11-19 |
| 存储 | `/data` 49G，已用 7.9G，可用 41G | ✅ `df -h` 2026-11-19 |
| root | ❌ `su` 不存在（`shell` uid=2000） | ✅ adb 2026-11-19 |
| 时区 | `Asia/Shanghai` | ✅ adb 2026-11-19 |

## iApp

| 项 | 值 | 级别 |
|---|---|---|
| 包名 | `com.iapp.app` | ✅ 2026-11-19 |
| versionName / versionCode | 5.0.1015 / 128 | ✅ `dumpsys package` 2026-11-19 |
| minSdk / targetSdk | 21 / 37（安装包声明口径） | ✅ `dumpsys package` 2026-11-19 |
| 安装 / 更新时间 | 2026-11-18 01:50:49 | ✅ 2026-11-19 |
| UID | `10231` | ✅ `detect_env.py` 2026-11-19；重装会变 |
| 工程根 | `/sdcard/Android/data/com.iapp.app/files/iApp/ProjectApp` | ✅ adb 2026-11-19；与 iApp 默认路径一致 |
| 设备侧工程 | 当日只有 `com.jianyue.reader` | ✅ adb 2026-11-19 |

## 投递链路

| 通道 | 前置 | 结果 |
|---|---|---|
| USB adb（主） | 开发者选项 + USB 调试；宿主用产品自带 adb | ✅ `python tools/push.py <项目ID> --serial <serial>` 2026-11-19 |
| FTP | 未开控制台 | ❓ 未验；怎么验：打开 iApp「服务器控制台」抄地址，先试直连，不通再 `adb forward` |

- 2026-11-19 实测：`com.jianyue.reader` 整目录推送，`src/` 31 个文件 + `.project` / `AndroidManifest.xml` / `icon.png` 3 个文件，退出码 0。
- 设备非 root，**不能** `adb root`，也读不了 `/data/data/com.iapp.app` 下的私有文件（探针存档类操作要换方案）。

## 权限

| 项 | 状态 |
|---|---|
| root | ❌ `su` 不存在 ✅ 2026-11-19 |
| `MANAGE_EXTERNAL_STORAGE` | ❓ 怎么验：`adb shell appops get com.iapp.app MANAGE_EXTERNAL_STORAGE` |
| 私有外部目录可写 | ✅ `adb push` 到 `Android/data/com.iapp.app/...` 成功 2026-11-19 |

## 已知坑

1. **无 root**：不能 `adb root`，`/data/data` 不可读；依赖私有目录存档的调试手法在这台上不可用。
2. **Android 11 分区存储**：工程根在 `Android/data/...` 下；`push.py` 先 `mkdir -p` 再推，避免 `secure_mkdirs failed`。
3. **`DisplayMetrics.heightPixels` 不含系统栏**：MIUI 12.5 / Android 11 上报 `1080x2216`，物理屏 `1080x2340`
   （扣掉状态栏 80 + 导航栏 44/130）。根挂到 DecorView 后实际占满整屏，用 `heightPixels` 算底部安全区差值会得到负数，
   底部 padding 被放大成 `168px`（应为 `44`/`130`），表现为 Tab 栏下面多一条空白 ✅ 2026-11-19。
   处理：用 `getRealMetrics()` 取真实高度（ui-kit `ui_realH()` 已内置）。
4. **MIUI 不自动收回 transient 状态栏** ✅ 2026-11-19 用户实测：阅读页用
   `BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE` 下滑唤出后 8 秒仍不隐回（API 34 模拟器会自动隐回）。
   已加 `IMMERSIVE_STICKY` 兜底，是否生效 ❓ 怎么验：重开阅读页下滑唤出状态栏，等 5 秒看是否隐回。
5. **MIUI 电池优化**：MIUI 12.5 可能杀后台；长跑探针前确认 iApp 未被省电策略清理 ❓ 未验。
6. **投屏默认码率不够**：USB 2.0 机型，硬件编码器 `OMX.qcom.video.encoder.avc`；scrcpy 默认
   8 Mbps 下文字发糊、浅色底出色彩带。50 Mbps 实测正常（编码器接受 `bitrate=50000000`，
   静态 VBR 实际 0.4~0.5 Mbps）。用 `python tools/mirror.py --serial <serial>` ✅ 2026-11-19。

## 未测项

| 项 | 级别 | 怎么验 |
|---|---|---|
| FTP 通道 | ❓ | 打开 iApp 服务器控制台，抄地址后直连 / `adb forward` |
| `MANAGE_EXTERNAL_STORAGE` | ❓ | `appops get com.iapp.app MANAGE_EXTERNAL_STORAGE` |
| MIUI 后台清理对 iApp 的影响 | ❓ | 长时间运行探针，观察进程是否被杀 |
| 手势导航 / 系统栏 inset 读数 | ❓ | 怎么验：装 ui-kit 自检页工程，`adb logcat -s ygs:V` 抄 `ui_insets` 读数并截图 |

## 取证

- `docs/evidence.md` 2026-11-19「R8-1 红米 Note 8 环境读数与简阅推送」
- 原始读数：`docs/archive/evidence-2026-11.md` §R8-1
