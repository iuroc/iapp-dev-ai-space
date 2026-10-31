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
| 引擎版本 | `dnplayer` 14.0.32.1 ✅ 2026-10-28 |
| 注册表卸载项 | DisplayName「雷电模拟器14」，DisplayVersion 14.0.32.1 ✅ 2026-10-28 |
| 运行进程 | `dnplayer.exe`（路径指向上面目录）✅ 2026-10-28 |
| 实例目录 | `vms\leidian1`；同目录下的空 `vms\leidian0` 是改名后 GUI 自动建的**空实例**，勿启动 ✅ 2026-10-28 |
| 伪装型号 | 25102RKBEC ✅ 2026-10-28 |

同机还装了雷电 9（见 `ldplayer9.md`）。两套独立安装，不要靠 `emulator-5554` 这种名字认设备。

## 2. Android 与屏幕

- Android 14 / API 34 ✅ 2026-10-28
- 屏幕 **1080×1920 / 480dpi** ✅ 2026-10-29（`wm size` / `wm density` 物理值；
  2026-10-28 读到 720×1280 / 320dpi，实例分辨率被改过，以开工时现查为准）
- `adb -s <serial> shell getprop ro.build.version.sdk` → `34` ✅ 2026-10-28
- 手表预览探针：`ProjectApp/com.demo.watchmask`（233dp 圆罩层，状态栏隐藏、点击穿透）✅ 2026-10-29
- **没有底部导航栏**：镜像把 framework `config_showNavigationBar` 编译成 `false`，
  即使 `navigation_mode=0`、启用 `navbar.threebutton` overlay 也不出 `NavigationBar0`；
  RRO 改值重启即失效。测 insets / 底部安全区时**不要假设有导航栏**，
  `navigation_bar_height` 仍有值（48dip）但不可靠 ✅ 2026-10-31（`evidence-2026-10.md` §NAVBAR-RRO）

## 3. 投递

### 主：adb 整目录推送

源在 `project/<项目ID>/`（各自 git 仓库），设备侧只是副本：

```bash
export MSYS_NO_PATHCONV=1
python tools/push.py <项目ID> --serial emulator-5556
```

- 默认先清远端 `src/ res/ files/` 的**内容**，再全量推；不读回、不比对，只认退出码
- 远端那几个目录删不掉：`rm -rf <目录>` 报 `Text file busy`，删内容可以 ✅ 2026-10-30
- 推之前工程要在 iApp 里关着；推完交给用户重新打开，Claude 不代运行

### 备：FTP over `adb forward`（没有 adb 时）

见下节；命令形如
`python tools/ftp-sync.py --adb-forward emulator-5556 --port <端口> --remote /ProjectApp/<项目ID> --local-root project/<项目ID>`。

### 共享目录：2026-10-30 起已停用

宿主 `android-sync/` 已移除，设备侧 `/sdcard/Pictures/ProjectApp` 已删，
现在工程只走 `push.py` 推到 iApp 默认工程根（见 §4）。下面这段是停用前的事实，留作历史：

### 共享目录：只是设备镜像的宿主侧投影，别当通道

```
宿主 android-sync/                       ↔  设备 /mnt/shared/Pictures（vboxfs）
宿主 android-sync/ProjectApp/<项目ID>/   ≡  设备 /sdcard/Pictures/ProjectApp/<项目ID>/   （同一批字节）
```

- **源和镜像在这里是同一批字节** ✅ 2026-10-30：在「设备侧」执行 `rm -rf .../src/*` 删掉的就是宿主源文件
  （当天真删过一次，靠 git 恢复）。所以工程源目录必须放在共享目录外，本机约定 `project/`
- **宿主改写设备已读过的文件后，`/sdcard` 侧会长期读到旧内容** ✅ 2026-10-30：改了 10 分钟设备上还是旧模块，
  重开工程无效；同一文件走 vboxsf 直挂 `/mnt/shared/Pictures` 却是新的 → 旧的是 Android FUSE 层缓存
- 新建文件两侧立刻可见 ✅ 2026-10-27（别因此以为整条链路都是实时的）
- 兜底（仅当不得不在共享目录里改）：`adb push` 该文件，或设备侧
  `su -c 'echo 3 > /proc/sys/vm/drop_caches'`（立刻生效）

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
  --remote /ProjectApp/<项目ID> --local-root project/<项目ID> --dry-run
```

脚本会自动转发控制端口与每个 PASV 数据端口，退出时清理。详见 SKILL `.claude/skills/iapp-development/references/ftp-delivery.md`。

**FTP 与共享目录曾是同一份文件（2026-10-30 前，已失效）**：当时工程根软链 → `Pictures` → 共享目录，
FTP 侧的读写最终落到宿主镜像。共享目录停用、工程根改回普通目录后这条不成立。
仍成立的是：**FTP 的远端根是应用级文件区 `/ProjectApp/<项目ID>`**。

## 4. 工程根

**当前（2026-10-30 起）**：

```
/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp
```

- iApp 已改回这个默认路径，共享目录停用后它就是一个普通目录 ✅ 2026-10-30
  （`ls` 可写、`adb push` 正常；`push.py` 的默认 `--root` 就是它）
- 目录不存在时先 `adb shell mkdir -p`：让 `adb push` 自己建会报
  `remote secure_mkdirs failed: Operation not permitted` ✅ 2026-10-30

**停用前（2026-10-26 ~ 2026-10-30）**：

```
/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp
  → /storage/emulated/0/Pictures/ProjectApp          （软链，2026-10-26 建）
```

- iApp 开发模式取工程根返回 `Android/data/...` 侧，实际落在共享目录，两条路径 md5 一致 ✅ 2026-10-27
- Android 11+ 的 `Android/data/<包名>` 只有该 app 自己的 mount namespace 能访问；
  普通 `adb shell` 会被 FUSE 拒绝，建链接必须 `su` ✅ 2026-10-26
- 链接建在设备侧 ext4/FUSE 路径；**共享目录（vboxsf）不支持 `ln -s`**（`Function not implemented`）✅ 2026-10-26

## 5. 权限与 root

- `su -c id` → `uid=0(root)` ✅ 2026-10-28
- su 体系是 Koush / CyanogenMod Superuser：`/system/xbin/su` + 常驻 `su_daemon`（socket `@SUPERUSER`）
- 授权库 `/data/user_de/0/com.android.settings/databases/su.sqlite`，表 `uid_policy`；
  永久允许行 `uid=<app uid>, command='', desired_uid=0, policy='allow', until=0`
- iApp UID：`10072`（`u0_a72`）✅ 2026-10-28；重装后可能变，要重写该行
- `MANAGE_EXTERNAL_STORAGE: allow` ✅ 2026-10-28
- `SYSTEM_ALERT_WINDOW: allow`（iApp 自带悬浮窗能力，开发模式可直接加覆盖层）✅ 2026-10-29
- 脚本：`docs/artifacts/root/grant_iapp_root.sh`

## 6. 已知坑

| 现象 | 原因 | 处理 |
|---|---|---|
| `emulator-5554` 指到别的实例 / offline | 两套雷电都抢宿主 5555 | 把第二套改名 `leidian1`（端口 5557）；投递前 `getprop` 核对 |
| GUI 自动出现一个空的 `leidian0` | 改名后的残留 | 不要启动；稳定后可删 |
| 宿主改了 iApp 看不到 | FUSE 旧缓存 / 工程还开着 | 关工程重开；必要时换 `adb push` |
| 软链消失、写入被拒 | 卸载/清除数据删了 `Android/data`，appop 也被重置 | 重建软链 + 重新 `appops set` |
| `adb push` 报 `secure_mkdirs failed` | Git Bash 把 `/storage/...` 改写成 Windows 路径 | `export MSYS_NO_PATHCONV=1` |
| `bind mount` 后 app 看不到 | 应用独立 mount namespace | 不用 bind mount，用共享目录 + 软链 |
| 为手表预览改 `wm size` / `wm density` | **整实例全局生效**，iApp 与所有 app 一起变方屏，无法正常调试 | 不改尺寸；用 `com.demo.watchmask` 的 233dp 罩层（SKILL `watch-app-guide.md` §10）。已改就 `wm size reset` + `wm density reset` |

## 7. 未测项

| 项 | 级别 | 怎么验 |
|---|---|---|
| 宿主 → 本机 FTP 可达 | ⚠（口述不可达） | `adb forward tcp:<端口> tcp:<端口>` 后连 `127.0.0.1:<端口>` |
| 设备内 → 自身 FTP | ❓ | MT 管理器终端连 `127.0.0.1:<端口>` |
| 雷电 9 当前状态 | ⚠（2026-10-27 后未连） | 启动后跑 `detect_env.py` |
| 三键 / 手势导航下的底部 insets | ❓ 本机问不出来 | 本机 SystemUI 不提供 `navigationBars` InsetsSource（`cmd overlay` 启停 threebutton / gestural 均无变化，`systemBars.bottom` 恒 0），**不要在这台上再试**；改真机补测，见下两条 |
| 软键盘弹出时的 ime inset | ❓ 本机问不出来 | 本机无软键盘 UI：输入框聚焦后 IME 不显示（`ime list` 有 pinyin 且是默认、`show_ime_with_hard_keyboard=1` 均已确认），`ime.bottom` 恒 0。装第三方输入法也无用；改真机补测 |
| Android 15+ 强制 edge-to-edge 后的窗口姿态 | ❓ | 怎么验：本机是 API 34 测不了；真机上跑 ui-kit 自检页，看 `ui_insets` 日志里 `rootTop` 是否变成 0、`pad` 是否从 0 变成状态栏高度 |
| Android 15+ 系统栏配色接口是否失效 | ❓ | 怎么验：`setStatusBarColor` 在 `targetSdk 36` 的新系统上预期被忽略。真机上把窗口背景设成与页面不同的颜色，看状态栏那一条跟的是哪一个 |

## 8. 取证

- `docs/evidence.md` 2026-10-26 E0 / E1（端口冲突与改名）
- `docs/evidence.md` 2026-10-26「Android 14 永久 root 授权」「iApp 工程目录链接到 Pictures」
- `docs/evidence.md` 2026-10-27（共享目录 FUSE 旧内容、截断文件）
- `docs/evidence.md` 2026-10-28（`detect_env.py` 首跑）
- `docs/evidence.md` 2026-10-29 WATCH-5（模拟器圆表盘罩层）
- `docs/evidence.md` 2026-10-30 DELIVERY-1（停用共享目录，改投 iApp 默认工程根）

## 附：口径说明

- iApp `targetSdk`：**两个对象，不是冲突**——安装包声明 **37**（`dumpsys package`），打包产物 **36**（`aapt2 dump badging`）。
  见 `.claude/skills/iapp-development/references/iapp-history.md`。
- iApp UID：当前 **10072**（`u0_a72`，2026-10-28 `pm list packages -U`）；重装会变，快照以 `runtime-env.md` 为准。
  旧记录 `u0_a50` 已过期。
