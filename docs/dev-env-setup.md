# 本机开发环境与投递步骤

> 本机专属步骤。环境类知识与其它机器的做法见 `docs/environments/`；
> 通道选择方法与通用坑见 `.claude/skills/iapp-development/references/environment-adaptation.md`。

## 0. Shell 前提

Git Bash 里调 adb 必须关掉路径改写，否则 `/storage/...` 会被转成 Windows 路径：

```bash
export MSYS_NO_PATHCONV=1
ADB="E:/Program Files/platform-tools/adb.exe"
```

## 1. 连机与提权

```bash
"$ADB" devices                       # 现查：取有 device 行的那台（detect_env.py 也会给）
"$ADB" root                          # adbd 重启为 root
"$ADB" shell id                      # uid=0(root)
```

su 传参在 Android 9 上会被拆散，整段用单引号：

```bash
"$ADB" shell 'su -c "ls -la /data/data"'
```

## 2. 找到工程

```bash
"$ADB" shell 'ls -la /sdcard/Pictures/ProjectApp/'      # 当前工程根，见 environments/ldplayer14.md §4
```

旧路径 `/storage/emulated/0/iApp/ProjectApp/` 仍存在一份副本，但已不再使用。

工程 = `ProjectApp/<项目ID>`，入口在 `src/mian.iyu`。

### 其他工具

| 工具 | 路径 |
|---|---|
| JDK 25 | `E:\Program Files\openjdk-25_windows-x64_bin\jdk-25\bin`（java/javac/jar/javap） |
| Python 3.13 | `E:\Program Files\python3.13.17` |

需要下依赖时优先用国内镜像源加速（pip：清华/阿里；maven：阿里云）。

## 3. 投递

### 主链路：共享目录直改（已实测）

iApp 内把工程根设为 `Pictures/ProjectApp` 后：

```
宿主机 android-sync/ProjectApp/<项目ID>/  ==  设备 /sdcard/Pictures/ProjectApp/<项目ID>/
```

宿主机直接改文件即可，设备立即可见；改之前先 `am force-stop com.iapp.app`，改完让用户重新打开工程。

### 兜底：adb push

```bash
IAPP_PKG=com.iapp.app
DEV_PROJECT=/sdcard/Pictures/ProjectApp/<项目ID>          # 以 iApp 设置里显示的为准
UID_APP=$("$ADB" shell pm list packages -U com.iapp.app | sed 's/.*uid://' | tr -d '\r')

"$ADB" shell "am force-stop $IAPP_PKG"
"$ADB" push ./src/mian.iyu "$DEV_PROJECT/src/mian.iyu"
"$ADB" shell "chown $UID_APP:sdcard_rw $DEV_PROJECT/src/*; chmod 660 $DEV_PROJECT/src/*"
```

- 必须先 force-stop：iApp 以内存为准，运行/保存会用旧内存覆盖磁盘
- 脚本：`docs/scripts/deploy.sh`

### 备选：iApp 内置 FTP

没有 adb、也没有共享目录时用。iApp 内打开「服务器控制台」，拿到 `ftp://<设备IP>:<端口>` 后：

```bash
export MSYS_NO_PATHCONV=1
python .claude/skills/iapp-development/scripts/ftp_sync.py \
  --host <设备IP> --port <端口> --remote /ProjectApp/<项目ID> \
  --local-root android-sync/ProjectApp/<项目ID> --dry-run
```

宿主连不上时先试 `adb forward tcp:<端口> tcp:<端口>`（连 `127.0.0.1:<端口>`）；
仍不通就只能在设备内终端验证。详见 `docs/environments/` 对应档案与 SKILL `.claude/skills/iapp-development/references/ftp-delivery.md`。

## 4. 取证

```bash
"$ADB" logcat -d -v time 'ygs:V' 'System.err:V' '*:S'
"$ADB" shell 'screencap -p /data/local/tmp/x.png'
"$ADB" pull /data/local/tmp/x.png .
```

## 5. 已排除的方案：bind mount

- `mount --bind <共享目录> /data/media/0/...`：sdcardfs 视图看不到
- `mount --bind <共享目录> /storage/emulated/0/...`：shell 可见，**iApp 进程不可见**
  - 验证：`grep <目录> /proc/<iApp pid>/mountinfo` 为空
  - 原因：应用 namespace 由 zygote 派生，后加挂载不传播

## 6. 共享目录

- 宿主机工作区目录 ↔ 模拟器 `/sdcard/Pictures`（vboxsf 实时，`/mnt/shared/Pictures` 同源）
- 工程同步：Android 9 让 iApp 工程根指向 `/sdcard/Pictures/ProjectApp`；Android 14 在 `Android/data/<包名>/files/iApp/ProjectApp` 建软链指向 `/sdcard/Pictures/ProjectApp`
- 通用案例与排障：`.claude/skills/iapp-development/references/emulator-setup.md`
- 共享目录本身不支持软链（vboxsf 报 `Function not implemented`）
- 兜底仍可用 `adb push`（见 §3）

## 7. 双开与 adb 端口

- 两套独立安装各自的唯一实例都叫 `leidian0`，都抢宿主 5555；推荐一次开一台
- 需要同开：把第二套改名为 `leidian1`（`vms` 目录 + `vms/config` 配置两处），端口变 5557，重启仍生效
- 完整步骤、验证与回滚：`docs/evidence.md` 2026-10-26 E1
