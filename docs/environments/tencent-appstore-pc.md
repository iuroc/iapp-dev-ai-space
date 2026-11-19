# 腾讯应用宝电脑版（Windows 11）

> 本档案描述 M2。2026-10-28 的复验就在本机（M2）完成，「识别 / adb / FTP」三节以实测为准；
> 其余条目沿用 2026-10-27 的旧读数，保留 ⚠ 与来源标注。

| 项 | 值 |
|---|---|
| 环境 ID | `tencent-appstore-pc` |
| 机器 | M2（Windows 11） |
| 最后核验 | 2026-11-19（M2 上实测，见 `docs/evidence.md` R8-1）；此前 2026-10-28 / 29（WATCH-2 / WATCH-3）；M1 从未复验 |
| 状态 | 该机器的主环境；本机（M1）不适用 |

## 1. 识别

| 判据 | 值 | 级别 |
|---|---|---|
| 宿主 OS | Windows 11 专业版，build 10.0.26300，64 位 | ✅ 本机 2026-11-19 |
| 宿主虚拟化 | Hyper-V 运行中（为跑 Docker Desktop 无法关闭） | ⚠ 他机 |
| 产品 | 腾讯应用宝电脑版 /「腾讯应用宝移动应用引擎」 | ⚠ 他机 |
| 安装目录 | `E:\Program Files\Tencent\Androws\Application\5.10.7500.6534` | ⚠ 他机 |
| 运行进程 | `Androws.exe`、`AndrowsAssistant.exe`、`AndrowsDlSvr.exe` | ⚠ 他机 |
| adb | 产品自带 `adb.EXE` 在 PATH 里；`adb devices` 能看到外接 USB（红米 Note 8 `cdc69048`）与容器本身（`adb connect 127.0.0.1:5555` → `127.0.0.1:5555`，`AOSP_on_Intel_Platform`）。**仅腾讯官方下载版支持**：设置里连续点击「性能」Tab 开开发者模式；微软商店版不能开 | ✅ 本机 2026-11-19 |
| 雷电 9 / 14 | 未安装（Hyper-V 占用，VirtualBox 系装不上） | ⚠ 他机 |
| MuMu / 夜神 | 未安装 | ⚠ 他机 |
| 容器内 iApp | `com.iapp.app` 已装（`Androws\apps\com.iapp.app`） | ✅ 本机 2026-10-28 |

判据：模拟器/容器只看「装没装」——安装目录、注册表卸载项、运行进程任一命中即算在用；
`adb` 只看「有没有 `device` 状态的目标」，不是「adb 可执行」。

## 2. Android 与屏幕

| 项 | 值 | 级别 |
|---|---|---|
| Android / API | 13 / 33（`AOSP_on_Intel_Platform`，ABI `x86_64`） | ✅ adb 2026-11-19 |
| 屏幕 / density | **iApp 跑在 display 2**：2160×3840 / 640（约 540×960dp）；display 0 是容器内置屏 320×480 / 410，iApp 页面不在那块屏上 | ✅ `wm size -d 2` / `dumpsys display` 2026-11-19 |
| 系统栏 / 挖孔 | display 2 是**全面屏虚拟显示**：无状态栏、无导航栏、无挖孔 | ✅ 用户确认 2026-11-19 |
| 是否 root | ❓ | 怎么验：`adb shell su -c id`（`su` 可能挂起，加超时）；目前无结论 |

## 3. 投递

**进容器（官方下载版）：adb 整目录 push（主）。** `adb connect 127.0.0.1:5555` 后
`python tools/push.py <项目ID> --serial 127.0.0.1:5555` ✅ 2026-11-19。
iApp 内置 FTP 仍是备选（微软商店版没有 adb 时只能走它）。出容器到外接设备：宿主 `adb install`。

| 项 | 值 |
|---|---|
| 地址 | `ftp://172.22.44.17:9527`（2026-10-28 本机实测）；2026-10-27 为 `172.22.39.216:9527` —— **地址和端口每次可能变，以 iApp 服务器控制台为准** |
| 登录 | 匿名 `anonymous` + 任意邮箱 ✅ 本机 2026-10-28 |
| FTP 根 | App 级文件区：`ProjectApp/`、`DownloadFileDir/`、`Userimg/`、`screenshot/`、手册副本 |
| 工程位置 | `/ProjectApp/<项目ID>` ✅ 本机 2026-10-28（FTP 推 `src/` → 容器内打包 → FTP 取回 `bin/<包名>.apk`） |
| 读 | `MLSD` / `NLST` / `SIZE` / `MD5` / `RETR` ✅ 本机 2026-10-28/29（WATCH-2 / WATCH-3） |
| 写（上传 / 建目录） | `STOR` / `MKD` ✅ 本机 2026-10-28/29（`ftp_sync.py` 推 6 个、9 个文件，MD5 全一致） |
| 写（删除 / 改名 / 追加） | `DELE` / `RMD` / `RNFR` / `APPE` ⚠ 他机 2026-10-27 |
| 点文件 | `MLSD`/`NLST` **不列** `.project`；`SIZE`/`MD5` 正常 ⚠ 他机 2026-10-27（M2 未单独复验） |
| 父目录 | `STOR` **不会**自动建父目录；`MKD` 非递归 ⚠ 他机 2026-10-27 |
| 逐级建目录 | `ftp_sync.py` 逐级 `MKD` 后 push 成功 ✅ 本机 2026-10-28 |

共享目录：❓ 未确认本产品是否有宿主 ↔ 设备共享目录；怎么验：产品设置的「共享文件夹」类选项里找宿主目录映射。

投递命令见 SKILL `.claude/skills/iapp-development/references/ftp-delivery.md` 与
`.claude/skills/iapp-development/scripts/ftp_sync.py`。

## 4. 工程根

iApp 设置里显示的工程根：❓ 未抄回；怎么验：打开容器内 iApp 读取设置页显示的路径。
FTP 视角下工程在 `/ProjectApp/<项目ID>`；两者是同一份文件 ✅ 本机 2026-10-28（FTP 推 `src/` → 容器内打包 → FTP 取回 `bin/<包名>.apk`，见 WATCH-2）。

## 5. 权限与 root

adb 可用后已有 `shell`（`uid=2000` 语义未单独抄）。root 状态 ❓，怎么验：
`adb shell su -c id`（`su` 可能挂起，命令加超时）。存储权限：怎么验：
`adb shell appops get com.iapp.app MANAGE_EXTERNAL_STORAGE`。

## 6. 已知坑

| 现象 | 原因 | 处理 |
|---|---|---|
| `adb devices` 里没有容器 | 容器 adb 需要先开开发者模式；**微软商店版无法开启** | 官方下载版：设置里连续点击「性能」Tab → 开开发者模式 → `adb connect 127.0.0.1:5555`；微软商店版只能走 FTP |
| `wm size` 只有 320×480 | 容器有 display 0（内置屏 320×480）和 display 2（HDMI 2160×3840，iApp 实际所在） | 查应用屏用 `wm size -d 2` / `wm density -d 2`，不要用默认的 display 0 |
| 雷电/MuMu 装不上 | 宿主必须开 Hyper-V | 换 VirtualBox 系容器不可行；用本产品 |
| `.project` 在列表里看不到 | 服务端不列点开头文件 | 用 `SIZE` 探，不要按清单判断存在性 |
| `STOR` 报 550 | 父目录不存在 | 先逐级 `MKD` |
| 端口连不上 | 端口每次可能变 / 网络模式 | 每次从 iApp 服务器控制台抄地址 |

「应用宝与 Intel 合作、依赖 WHPX」是官方宣传口径，M2 上**无外网**未独立核实——
只记「Hyper-V 开启 + 应用宝在用 = 共存可用」这一条实测，不写实现细节。

## 7. 未测项

| 项 | 级别 | 怎么验 |
|---|---|---|
| 容器 adb 通道 | ✅ 2026-11-19 | 官方版开开发者模式后 `adb connect 127.0.0.1:5555` 成功；微软商店版不可用 |
| 容器内 iApp 是否能打 32 位包 | ✅ 2026-10-28 | 设置 →【打包设定so库】全勾后可产出四架构 APK |
| Android / API、屏幕、density | ❓ | 怎么验：模拟器内「设置 → 关于手机」，或容器内 `wm size` / `wm density` |
| iApp 设置显示的工程根 | ❓ | 怎么验：打开容器内 iApp，抄设置页显示的路径 |
| 宿主 ↔ 设备共享目录 | ❓ | 怎么验：产品设置里找「共享文件夹」类选项 |
| 设备内 FTP 自连 | ❓ | 怎么验：设备内终端连 `127.0.0.1:<端口>` |
| `ftp_sync.py` 端到端真推 | ❓ | 怎么验：关工程 → 全量推 → 退出码 0 |
| **Android 16 真机补测出口** | ❓ 待建 | 怎么验：本机（雷电 14 / API 34）测不了的三项在这里补——① 三键 / 手势导航下的 `systemBars.bottom`；② 软键盘弹出时的 `ime.bottom` 与内容位移；③ Android 15+ 强制 edge-to-edge 后的 `rootTop` 与系统栏配色。做法：连真机后跑 ui-kit 自检页，把 `ui_insets` 日志与截图抄进 `docs/evidence.md`，再回填 `ldplayer14.md` §7 与 SKILL |

## 8. 取证

- `docs/evidence.md` 2026-10-28「M2 环境探测与 FTP 读数（他机）」
- 交接文档：独立文档，未入库；关键读数已抄进上面各表

## 9. 本机工具

| 工具 | 路径 / 版本 | 级别 |
|---|---|---|
| scrcpy | `E:\Dev Tools\scrcpy\scrcpy-win64-v5.0.1\scrcpy.exe`（5.0.1） | ✅ 2026-11-19 |
| 投屏入口 | `python tools/mirror.py --serial <serial> --preset default` | ✅ 2026-11-19 |

- 默认预设 H.264 50 Mbps / 60 fps；`light` = 25M/30fps，`pixel` = H.265 35M/30fps。
- 依据与码率口径见 SKILL `.claude/skills/iapp-development/references/debugging.md` §投屏预览；
  本文件只记路径与版本。
