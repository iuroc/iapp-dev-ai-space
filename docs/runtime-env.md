# 运行时环境（当前机器快照）

快照：2026-10-28（`python docs/scripts/detect_env.py` 实跑）
环境类知识与通用步骤在 `docs/environments/`，这里只记这台机器的具体值。

## 当前连接

| 项 | 值 |
|---|---|
| 宿主 | Windows 10 Pro Education 10.0.19045；Hyper-V 未启用 |
| 在连设备 | `emulator-5556`（雷电 14）/ API 34 / Android 14 / model 25102RKBEC |
| 另一台 | 雷电 9 已安装、VM 引擎在跑，但未连 adb（`adb devices` 不出现） |
| 推荐通道 | 共享目录（主）→ adb（取证/兜底）→ FTP over `adb forward`（读写均已验 ✅ 2026-10-28） |

选择规则见根 `CLAUDE.md`「设备选择」；两台同开时的端口冲突见 `environments/ldplayer14.md` §1、§6。

## 安装与端口

| 项 | 雷电 9 | 雷电 14 |
|---|---|---|
| 安装目录 | `E:\Program Files\leidian\LDPlayer9` | `C:\leidian\LDPlayer14` |
| 引擎 | dnplayer 9.5.42.0 | dnplayer 14.0.32.1 |
| 实例 | `leidian0` | `leidian1`（另有空 `leidian0`，勿启动） |
| 宿主端口 | 5555 | 5557 |
| Android | 9 / API 28（sdcardfs） | 14 / API 34 |
| 屏幕 | 1080×1920 / 480dpi | 720×1280 / 320dpi |
| root | `adb root` | `su -c id` → uid=0 |
| 共享目录 | `android-sync/` ↔ `/mnt/shared/Pictures` | 同左 |

## iApp

| 项 | 值 |
|---|---|
| 包名 / 显示名 | `com.iapp.app` / 测兆编程 |
| versionName | 5.0.1013（versionCode 127，minSdk 21，targetSdk 37） |
| UID（雷电 14） | `10072`（`u0_a72`）✅ 2026-10-28；重装后会变 |
| 工程根 | `/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp` → 软链 `/storage/emulated/0/Pictures/ProjectApp` |
| 存储权限 | `MANAGE_EXTERNAL_STORAGE: allow` ✅ 2026-10-28 |
| 旧工程根 | `/storage/emulated/0/iApp/ProjectApp/<项目ID>`（旧副本，不再使用） |

root 授权细节（`su.sqlite` / `uid_policy` / `grant_iapp_root.sh`）见 `environments/ldplayer14.md` §5。

## 共享目录现状

- 宿主 `android-sync/` ↔ 设备 `/mnt/shared/Pictures`（vboxsf，rw，双向实时）
- 改「已存在」文件后，FUSE 视图（`/sdcard/Pictures`，iApp 实际读的那侧）可能仍是旧内容 → 遇到时核 `/sdcard` 侧 md5 诊断，或改用 `adb push`
- 可能同步出截断文件 → 核 `wc -c`，不一致就 `adb push`
- Git Bash 下 `adb push` 前先 `export MSYS_NO_PATHCONV=1`
- 工程根是软链时，`VisualDesigner.a9` 返回 `Android/data` 侧路径，与共享目录同一份文件（md5 一致）

## 已有工程

- `com.qingjian.reader`（青简阅读器，进行中）
- `com.demo.game2048`、`com.demo.calc`、`com.i7f3d3b94b508ff9f` 等探针/演示工程
- 目录：`android-sync/ProjectApp/<项目ID>/`，入口 `src/mian.iyu`

## 调试存档（2048）

- `/data/data/com.iapp.app/files/game2048.save`，属主 = iApp 自己的 uid（当前 `u0_a72`，以 `pm list packages -U` 为准），权限 `600`
- 覆盖前让用户关工程；写后 `chown` + `chmod 600`，否则 iApp 读不到
- 格式：`v1` + `board=`（16 个逗号分隔整数）+ `score=` + `best=` + `won=` + `over=`

## 工具

| 工具 | 路径 |
|---|---|
| adb | `E:\Program Files\platform-tools\adb.exe`（1.0.41） |
| LDPlayer 自带 adb | `E:\Program Files\leidian\LDPlayer9\adb.exe`（可用，非默认） |
| build-tools | `E:\Program Files\build-tools_r35_windows\android-15` |
| JDK | `E:\Program Files\openjdk-25_windows-x64_bin\jdk-25\bin` |
| Python | `E:\Program Files\python3.13.17` |

## 口径说明

- `targetSdk`：安装包声明 **37**（`dumpsys package`），打包产物 **36**（`aapt2 dump badging`）——两个对象，不是冲突。
  见 `.claude/skills/iapp-development/references/iapp-history.md`。
