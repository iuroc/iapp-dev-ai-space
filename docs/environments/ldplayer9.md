# 雷电 9（Android 9 / API 28）

> **定位：仅按需兼容环境。** 默认不在这台上开发；只有开发者**明确要求**验证 Android 9 行为时启用。
> 低版本只做有限兼容测试，不追求结论追平 API 34。

| 项 | 值 |
|---|---|
| 环境 ID | `ldplayer9` |
| 机器 | M1（Windows 10 Pro Education 19045） |
| 最后核验 | 2026-10-26（快照）；2026-10-27 起未再连 adb，现状 ⚠ |
| 状态 | 备用 / 按需 |

## 1. 识别

| 判据 | 值 |
|---|---|
| 安装目录 | `E:\Program Files\leidian\LDPlayer9` ✅ 2026-10-26 |
| 引擎版本 | `dnplayer` 9.5.42.0；VM 引擎进程 `Ld9BoxHeadless.exe`（`C:\Program Files\ldplayer9box`）✅ |
| 注册表卸载项 | DisplayName「雷电模拟器9」，DisplayVersion 9.5.42.0 ✅ 2026-10-28 |
| 实例目录 | `vms\leidian0` ✅ |
| 宿主端口 | `adb,tcp,,5555,,5555` ✅ |
| 伪装型号 | 25060RK16C ✅ |

## 2. Android 与屏幕

- Android 9 / API 28；`/storage/emulated/0` 是 **sdcardfs**（不是 FUSE）✅
- 屏幕 1080×1920 / 480dpi（判读 sp/px 的锚点，换设备必须重取）✅
- `getprop ro.build.version.sdk` → `28`

## 3. 投递

### 共享目录镜像

```
宿主 android-sync/                       ↔  设备 /mnt/shared/Pictures
宿主 android-sync/ProjectApp/<项目ID>/   ≡  设备 /sdcard/Pictures/ProjectApp/<项目ID>/
```

前提是 iApp 设置里的工程根已指到 `/sdcard/Pictures/ProjectApp`（这台改过）✅ 2026-10-26。
`sdcardfs` 没有 FUSE 那层旧缓存问题，但仍建议改完核一次 md5。

### adb push

```bash
export MSYS_NO_PATHCONV=1
adb root
adb -s <serial> shell am force-stop com.iapp.app
adb -s <serial> push <宿主文件> /sdcard/Pictures/ProjectApp/<项目ID>/src/<名>
adb -s <serial> shell "chown <uid>:sdcard_rw /sdcard/Pictures/ProjectApp/<项目ID>/src/*; chmod 660 /sdcard/.../src/*"
```

`<uid>` 用 `pm list packages -U com.iapp.app` 现查；`su -c` 的参数在 Android 9 上容易被拆散，整段用单引号包。

## 4. 工程根

- iApp 默认（未改设置）：`/data/media/0/iApp/ProjectApp/<项目ID>`，日常视图 `/sdcard/iApp/ProjectApp/<项目ID>` ✅
- 这台已改成 `/sdcard/Pictures/ProjectApp`；旧路径仍有一份副本，不再使用
- 与 Android 14 不同：**可以直接在 iApp 设置里改到共享存储**，不需要 root 软链

## 5. 权限与 root

- `adb root` → `uid=0(root)` ✅ 2026-10-26（`adb unroot` 可回）
- 存储用运行时权限 `READ/WRITE_EXTERNAL_STORAGE`；Android 9 无分区存储
- `su -c` 传参易被拆散，整段单引号

## 6. 已知坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 两套雷电抢 5555 | 各自唯一实例都叫 `leidian0` | 一次只开一台，或把另一套改名 `leidian1` |
| iApp 看到旧工程 | 工程还开着 / 读到旧路径 | 关工程重开；确认 iApp 设置里的工程根 |
| 写 Pictures 被拒 | 存储权限没给 | 在 iApp 里授权存储 |
| 旧/新工程根并存 | 改过设置 | 只认 iApp 设置里显示的那个 |

## 7. 未测项

| 项 | 级别 | 怎么验 |
|---|---|---|
| 当前能否正常启动并连 adb | ⚠ | 启动后 `adb devices -l` + `getprop ro.build.version.sdk` |
| 本机 FTP（宿主 / 设备内） | ❓ | 同 `ldplayer14.md` 的两条路径 |
| 应用宝同款问题的低版本表现 | ❓ | 需要时再测，不主动投入 |

## 8. 取证

- `docs/evidence.md` 2026-10-26 E0 / E1
- `docs/evidence.md` 2026-10-27（共享目录核 md5 的实测）
- `.claude/skills/iapp-development/references/emulator-setup.md` §3（通用步骤）
