# 运行时环境（本机快照）

快照时间：2026-10-26

## 设备

本机装了两套**独立**的雷电（不是同一安装的两个实例）。2026-10-26 已把 LDPlayer14 的实例从 `leidian0` 改名为 `leidian1`，宿主端口永久改为 5557；LDPlayer9 保持 `leidian0` / 5555。仍推荐一次开一台，两台同开时按下面的端口对应关系使用。

| 项 | LDPlayer9（iApp 主用） | LDPlayer14（验证用） |
|---|---|---|
| 安装目录 | `E:\Program Files\leidian\LDPlayer9` | `C:\leidian\LDPlayer14` |
| 引擎 | dnplayer 9.5.42.0 | dnplayer 14.0.32.1 |
| 实例名 | iApp测试 | 安卓14验证 |
| VM UUID | `…-012e-000000000000` | `…-7046-000000000001`（`leidian1` 实机）；旧的 `…-7046-000000000000` 是改名后 GUI 自动建的**空实例**（0 字节，勿启动） |
| 实例目录 | `vms\leidian0` | `vms\leidian1`（另有空 `vms\leidian0`，勿启动） |
| Android | 9 / API 28，`/storage/emulated/0` 为 **sdcardfs** | 14 / API 34 |
| 伪装型号 | 25060RK16C | 25102RKBEC |
| 屏幕 | 1080×1920 / 480dpi | 720×1280 / 320dpi |
| root | `adb root` → uid=0 | `su -c id` 直接 uid=0；`adb root`/`unroot` 均可用 |
| sharedPictures | `E:\...\android-sync` | `E:\workspaces\2026-10-24-iapp-dev-ai-space\android-sync`（2026-10-26 核实，见 evidence） |
| iApp | 已装 5.0.1013 | 已装 5.0.1013（工程根经软链指向 `Pictures/ProjectApp`） |

端口：LD9 `adb,tcp,,5555,,5555`；LD14 `adb,tcp,,5557,,5555`（两者都有 `gdb,tcp,,2222,,2222`）

> **当前状态（2026-10-26 用户实测 + 本机复测）**：LD9 = `emulator-5554` / 5555 / sdk 28；LD14 = `emulator-5556`（串口名）或 `127.0.0.1:5557` / sdk 34。
> 投递前仍先 `adb -s <serial> shell getprop ro.build.version.sdk` 核对，不要盲信 `emulator-5554`。
> 推荐一次开一台；需要同时开就分别按安卓版本配置。若 LD14 又被 GUI 拉回 5555：检查 `vms` 下是不是又出现实机 `leidian0`，按 `docs/evidence.md` 2026-10-26 E1 重新改名为 `leidian1`。
> **选择规则（2026-10-27 起，原文在 `CLAUDE.md`「设备选择」）**：只有 1 台就用它；2 台默认取 API 高的；用户指定版本则按用户要求。
> 2026-10-27 当前：只连 LD14 = `emulator-5556` / sdk 34（LD9 未启动）。
> 详见 `docs/evidence.md` 2026-10-26 E0（冲突成因）/ E1（改名验证）。

## Android 14 的 root 机制（LDPlayer14）

- `su` 是 Koush / CyanogenMod Superuser 体系：`/system/xbin/su`（setuid root）+ 常驻 `su_daemon`（socket `@SUPERUSER`）
- 授权库：`/data/user_de/0/com.android.settings/databases/su.sqlite`，表 `uid_policy`（`SuDatabaseHelper` v6 schema）
- 永久允许一行：`uid=<app uid>, command='', desired_uid=0, policy='allow', until=0`
- `ro.cm.version` 为空 → `persist.sys.root_access` 门禁不生效
- iApp 在 LD14 上 UID = 10072（u0_a72）；2026-10-26 已写入永久 allow
- 重装 iApp 后 UID 可能变化，需重写该行；脚本见 `docs/artifacts/root/grant_iapp_root.sh`
- 取证与 logcat 原文见 `docs/evidence.md` 2026-10-26「Android 14 永久 root 授权」

## Android 14 的 iApp 工程目录（LDPlayer14）

- iApp 默认工程根：`/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp`
- 已建符号链接 → `/storage/emulated/0/Pictures/ProjectApp`（宿主 `android-sync/ProjectApp`）
- 写入链路已实测：设备链接 → `Pictures` → vboxsf → 宿主 `android-sync/ProjectApp`，删除同步
- 前提：iApp 已授予 `MANAGE_EXTERNAL_STORAGE`（`appops set com.iapp.app MANAGE_EXTERNAL_STORAGE allow`，2026-10-26）
- `Android/data` 随卸载/清除数据消失；重装后链接和 appop 都要重建
- 宿主只能在 `android-sync/ProjectApp` 侧看结果，不能直接访问设备 `Android/data`
- 取证见 `docs/evidence.md` 2026-10-26「iApp 工程目录链接到 Pictures」

## iApp

| 项 | 值 |
|---|---|
| 包名 | `com.iapp.app`（显示名 测兆编程） |
| versionName | 5.0.1013（versionCode 127，minSdk 21，targetSdk 37） |
| 安装时间 | 2026-10-24 13:10 |
| 进程内 UID | u0_a50（app 文件属主用 `u0_a50:sdcard_rw`） |

## 工程实际路径

- **当前工程根（用户在 iApp 内改过）：`/storage/emulated/0/Pictures/ProjectApp/<项目ID>`**
  - `/sdcard/Pictures` 即 LDPlayer 共享目录 ↔ 宿主机 `android-sync/`
  - 因此宿主机 `android-sync/ProjectApp/<项目ID>/` 就是设备工程本体
- 旧路径 `/storage/emulated/0/iApp/ProjectApp/<项目ID>` 仍存在（旧副本，不再使用）
- 已有的可运行工程：
  - `com.demo.game2048`（显示名 2048）— 滑动/方向键/动画/持久化，2026-10-26
  - `com.demo.calc`（显示名 黑金计算器）— 4×5 按键网格与跨 call 状态
  - `com.i7f3d3b94b508ff9f`（显示名 测试项目）— 早期探针宿主
- 入口：`src/mian.iyu`
- 其他：`.project`、`files/`、`res/`、`sdk/`、`build.xml`、`icon.png`、`AndroidManifest.xml`
- 任务书里的 `Android/data/<包名>/files/iApp/ProjectApp` 在本机**不存在**
- 官方手册：`/storage/emulated/0/iApp/*.txt`，另有副本在 `/data/data/<包名>/files/iApp/`

## 调试存档（2048）

- 路径：`/data/data/com.iapp.app/files/game2048.save`，属主 `u0_a50:u0_a50`，权限 `600`
- `adb root` 后可覆盖；覆盖前先让用户关掉工程，避免运行中的状态再写回
- 写完后 `chown u0_a50:u0_a50` + `chmod 600`，否则 iApp 读不到
- 格式：`v1` + `board=`（16 个逗号分隔整数）+ `score=` + `best=` + `won=` + `over=`

## 共享目录

- 宿主机 `android-sync/` ↔ 模拟器 `/mnt/shared/Pictures`（vboxsf，rw，ttl=0，双向实时）
- **工程打开期间有读缓存**：iApp 正开着的工程，宿主机改 `src/*.iyu|*.mjava`、`build.xml`，设备端可能仍读到旧内容（md5 不一致）；关掉工程后自动刷新对齐（2026-10-27 实测）
- **可能同步出截断文件**：2026-10-27 实测 `matsupport.mjava` 设备端只有 4190/4222 字节，截断在行中间，iApp 报 `Parse error ... Encountered: <EOF>`。改完先核 `wc -c` + md5，不一致就 `adb push` 兜底
- 投递顺序：先改同步目录 → 让用户关/重开工程 → 核 md5；只有核不上才 `adb push` 兜底
- **2026-10-27 出现单文件不同步**：同一轮改了 3 个 `.iyu`，设备上只有 `mian.iyu` 更新，`p_b.iyu` / `p_c.iyu` 仍是旧 md5（等待 2s 仍未同步）→ 核 md5 这一步不能省
- **Git Bash 下 `adb push` 远程路径会被 MSYS 改写**成 `D:/Program Files/Git/storage/...`，报 `secure_mkdirs failed`；先 `export MSYS_NO_PATHCONV=1` 再 push
- **工程根是符号链接**：`VisualDesigner.a9`（开发模式取工程根）返回
  `/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp/<项目ID>`，
  而 `.../files/iApp/ProjectApp` 是指向 `/storage/emulated/0/Pictures/ProjectApp` 的**符号链接**（`u0_a72 ext_data_rw`），
  与共享目录是同一份文件；两条路径的 `md5` 一致，写哪边都生效（2026-10-27）
  - 所以 mjava 里拼 `<root>/apk/assets/xxx.dex` 拿到的就是共享目录里的产物
- **改「已存在」文件可能只有 vboxsf 直挂那侧更新**：宿主改 `xui.mjava` 后
  `/mnt/shared/Pictures/...` 是新内容（10836 B），`/sdcard/Pictures/...`（FUSE 视图）仍是旧内容（8312 B），
  iApp 读 `/sdcard` 侧就跑旧代码；**新建**文件（marker）则两侧立刻可见。
  结论：改已存在文件后，核的是 `/sdcard/...` 的 md5，不一致直接 `adb push` 覆盖（2026-10-27 实测）
- `android-sync/cache`、`android-sync/data` 是 LDPlayer 侧文件，与本项目无关

## 工具

| 工具 | 路径 |
|---|---|
| adb | `E:\Program Files\platform-tools\adb.exe`（1.0.41 / 37.0.1） |
| LDPlayer 自带 adb | `E:\Program Files\leidian\LDPlayer9\adb.exe`（可用，非默认） |
| build-tools | `E:\Program Files\build-tools_r35_windows\android-15`（aapt/aapt2/d8/zipalign/apksigner/dexdump） |
| 图标生成 | `docs/scripts/make_icon.py`（纯 Python 标准库，离线） |

## 屏幕

- 1080×1920，density = scaledDensity = 3.0（判读 sp/px 的锚点，换设备必须重取）
