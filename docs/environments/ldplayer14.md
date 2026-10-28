# 雷电 14（Android 14 / API 34）

| 项 | 值 |
|---|---|
| 环境 ID | `ldplayer14` |
| 机器 | M1（Windows 10 Pro Education 19045） |
| 最后核验 | 2026-10-28（`adb` + `detect_env.py`） |
| 状态 | **主开发环境**；新功能与验证默认在这台上做 |

## 1. 识别

| 判据 | 值 |
|---|---|
| 安装目录 | `C:\leidian\LDPlayer14` ✅ 2026-10-26 |
| 引擎版本 | `dnplayer` 14.0.32.1 ✅ |
| 注册表卸载项 | DisplayName「雷电模拟器14」，DisplayVersion 14.0.32.1 ✅ 2026-10-28 |
| 运行进程 | `dnplayer.exe`（路径指向上面目录）✅ 2026-10-28 |
| 实例目录 | `vms\leidian1`；同目录下的空 `vms\leidian0` 是改名后 GUI 自动建的**空实例**，勿启动 ✅ |
| 伪装型号 | 25102RKBEC ✅ |

同机还装了雷电 9（见 `ldplayer9.md`）。两套独立安装，不要靠 `emulator-5554` 这种名字认设备。

## 2. Android 与屏幕

- Android 14 / API 34 ✅
- 屏幕 720×1280 / 320dpi ✅
- `adb -s <serial> shell getprop ro.build.version.sdk` → `34` ✅ 2026-10-28

## 3. 投递

### 主：共享目录镜像

```
宿主 android-sync/                       ↔  设备 /mnt/shared/Pictures（vboxfs）
宿主 android-sync/ProjectApp/<项目ID>/   ≡  设备 /sdcard/Pictures/ProjectApp/<项目ID>/
```

- 改文件前先 `am force-stop com.iapp.app`（iApp 以内存为准）
- **改「已存在」文件后必须核 `/sdcard` 侧的 md5**：vboxsf 直挂侧会立刻更新，FUSE 视图可能仍是旧内容；
  新建文件两侧立刻可见 ✅ 2026-10-27
- 可能同步出截断文件（设备端字节数少于宿主），核 `wc -c`，不一致就 `adb push`

### 备：adb push / pull

```bash
export MSYS_NO_PATHCONV=1
adb -s <serial> shell am force-stop com.iapp.app
adb -s <serial> push <宿主文件> /storage/emulated/0/Pictures/ProjectApp/<项目ID>/src/<名>
```

写入 `Android/data` 侧需要 root；写 `Pictures` 侧注意属主（见 SKILL `emulator-setup.md`）。

### FTP：直连不可达，经 adb forward 可用

| 路径 | 结果 | 级别 |
|---|---|---|
| 宿主直连 `172.16.1.87:9527` | 不通（宿主不在 172.16.1.x，设备在 NAT 后） | ✅ 2026-10-28 |
| 只转发控制端口 | 能登录，但数据连接被拒（PASV 返回设备 IP） | ✅ 2026-10-28 |
| 主动模式 | `425 Can't open data connection` | ✅ 2026-10-28 |
| 控制端口 + 逐数据端口 `adb forward` | 全部只读操作可用（`NLST`/`MLSD`/`SIZE`/`MD5`） | ✅ 2026-10-28 |
| 写入（`STOR`/`DELE`/`MKD`/`RMD`/`RNFR`/`APPE`/`REST`） | 全部可用；`MKD` 非递归、`STOR` 不建父目录（551） | ✅ 2026-10-28 |
| `ftp_sync.py` 端到端 | 推 4/4、拉 4/4、MD5 全一致；远端不存在时退出 5 | ✅ 2026-10-28 |

```bash
export MSYS_NO_PATHCONV=1
python .claude/skills/iapp-development/scripts/ftp_sync.py \
  --adb-forward emulator-5556 --port 9527 \
  --remote /ProjectApp/<项目ID> --local-root android-sync/ProjectApp/<项目ID> --dry-run
```

脚本会自动转发控制端口与每个 PASV 数据端口，退出时清理。详见 SKILL `references/ftp-delivery.md`。

**FTP 与共享目录是同一份文件**：工程根软链 → `Pictures` → 共享目录，所以 FTP 侧的读写最终落到宿主镜像。
两侧偶尔出现字节差是瞬时的（编辑中/缓存），不是两份副本；2026-10-28 复核两个曾有差异的文件，
md5 已完全相同。这也意味着**不要同时用 FTP 和共享目录写同一个文件**。

## 4. 工程根

```
/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp
  → /storage/emulated/0/Pictures/ProjectApp          （软链，2026-10-26 建）
```

- iApp 开发模式取工程根返回 `Android/data/...` 侧，实际落在共享目录，两条路径 md5 一致 ✅ 2026-10-27
- Android 11+ 的 `Android/data/<包名>` 只有该 app 自己的 mount namespace 能访问；
  普通 `adb shell` 会被 FUSE 拒绝，建链接必须 `su` ✅
- 链接建在设备侧 ext4/FUSE 路径；**共享目录（vboxsf）不支持 `ln -s`**（`Function not implemented`）✅

## 5. 权限与 root

- `su -c id` → `uid=0(root)` ✅ 2026-10-28
- su 体系是 Koush / CyanogenMod Superuser：`/system/xbin/su` + 常驻 `su_daemon`（socket `@SUPERUSER`）
- 授权库 `/data/user_de/0/com.android.settings/databases/su.sqlite`，表 `uid_policy`；
  永久允许行 `uid=<app uid>, command='', desired_uid=0, policy='allow', until=0`
- iApp UID：`10072`（`u0_a72`）✅ 2026-10-28；重装后可能变，要重写该行
- `MANAGE_EXTERNAL_STORAGE: allow` ✅ 2026-10-28
- 脚本：`docs/artifacts/root/grant_iapp_root.sh`

## 6. 已知坑

| 现象 | 原因 | 处理 |
|---|---|---|
| `emulator-5554` 指到别的实例 / offline | 两套雷电都抢宿主 5555 | 把第二套改名 `leidian1`（端口 5557）；投递前 `getprop` 核对 |
| GUI 自动出现一个空的 `leidian0` | 改名后的残留 | 不要启动；稳定后可删 |
| 宿主改了 iApp 看不到 | FUSE 旧缓存 / 工程还开着 | 关工程重开；核 `/sdcard` 侧 md5 |
| 软链消失、写入被拒 | 卸载/清除数据删了 `Android/data`，appop 也被重置 | 重建软链 + 重新 `appops set` |
| `adb push` 报 `secure_mkdirs failed` | Git Bash 把 `/storage/...` 改写成 Windows 路径 | `export MSYS_NO_PATHCONV=1` |
| `bind mount` 后 app 看不到 | 应用独立 mount namespace | 不用 bind mount，用共享目录 + 软链 |

## 7. 未测项

| 项 | 级别 | 怎么验 |
|---|---|---|
| 宿主 → 本机 FTP 可达 | ⚠（口述不可达） | `adb forward tcp:<端口> tcp:<端口>` 后连 `127.0.0.1:<端口>` |
| 设备内 → 自身 FTP | ❓ | MT 管理器终端连 `127.0.0.1:<端口>` |
| 雷电 9 当前状态 | ⚠（2026-10-27 后未连） | 启动后跑 `detect_env.py` |

## 8. 取证

- `docs/evidence.md` 2026-10-26 E0 / E1（端口冲突与改名）
- `docs/evidence.md` 2026-10-26「Android 14 永久 root 授权」「iApp 工程目录链接到 Pictures」
- `docs/evidence.md` 2026-10-27（共享目录 FUSE 旧内容、截断文件）
- `docs/evidence.md` 2026-10-28（`detect_env.py` 首跑）

## 附：口径说明

- iApp `targetSdk`：**两个对象，不是冲突**——安装包声明 **37**（`dumpsys package`），打包产物 **36**（`aapt2 dump badging`）。
  见 `.claude/skills/iapp-development/references/iapp-history.md`。
- iApp UID：当前 **10072**（`u0_a72`，2026-10-28 `pm list packages -U`）；重装会变，快照以 `runtime-env.md` 为准。
  旧记录 `u0_a50` 已过期。
