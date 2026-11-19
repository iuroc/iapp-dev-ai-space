# 探针证据账本（原始读数）

2026-11 当月账本。规则同 `docs/archive/evidence-2026-10.md`：先在这里追加「日期 / 批次 / 探针 / 原始读数」，
再把提炼后的结论写进 `docs/environments/` 或 SKILL；`docs/evidence.md` 只留索引行。

> - **批次 ID 是引用键**，不要改名、不要合并。
> - 当月可续写；跨月后冻结为只读。

---

## 2026-11-19 R8-1 红米 Note 8 环境读数与简阅推送

**背景**：用户接入一台 Android 11 红米 Note 8，要求收集基本信息并把「简阅」最新版推到设备 iApp 工程目录。

**宿主探测**（`python docs/scripts/detect_env.py`）：

```
宿主  Microsoft Windows 11 专业版 10.0.26300
虚拟化 Hyper-V=on
产品  腾讯应用宝电脑版 — 已安装
adb   E:\Program Files\Tencent\Androws\Application\5.10.7500.6534\adb.EXE (1.0.41)
       cdc69048 [device] API=30 android=11 model=Redmi Note 8 iApp=5.0.1015 uid=10231
共享  未配置 [unconfigured]
FTP   未配置 [skipped]
通道  shared=unknown adb=ok ftp=unknown
建议  adb（备选 无）；档案 tencent-appstore-pc
```

**宿主归属**：用户确认当前宿主是 **M2**（Windows 11 + 应用宝），M1 是另一台 Win10 + 雷电环境 ✅ 2026-11-19。

**设备读数**（`adb -s cdc69048 shell ...`）：

```
ro.product.model=Redmi Note 8     ro.product.manufacturer=Xiaomi
ro.product.device=ginkgo          ro.board.platform=trinket
ro.build.version.release=11       ro.build.version.sdk=30
ro.miui.ui.version.name=V125      ro.build.version.incremental=V12.5.5.0.RCOCNXM
ro.build.version.security_patch=2022-07-01
ro.build.date=Mon Aug  1 19:18:47 CST 2022
uname: Linux localhost 4.14.190-perf-gc61d39ef577d-dirty #2 SMP PREEMPT aarch64
ro.product.cpu.abilist=arm64-v8a,armeabi-v7a,armeabi
wm size: Physical size: 1080x2340
wm density: Physical density: 440
MemTotal: 5761544 kB          MemAvailable: 3511732 kB
df: /data 49G total, 7.9G used, 41G avail (17%)
battery: level 92, status 2, health 2, temperature 261, USB powered
uptime: up 1 day, 19:50      timezone: Asia/Shanghai
su -c id -> /system/bin/sh: su: inaccessible or not found   (shell uid=2000)
```

**iApp 读数**：

```
dumpsys package com.iapp.app:
  versionCode=128  minSdk=21  targetSdk=37  versionName=5.0.1015
  firstInstallTime=2026-11-18 01:50:49
工程根: /sdcard/Android/data/com.iapp.app/files/iApp/ProjectApp
设备侧仅: com.jianyue.reader
```

**推送**（工程 `com.jianyue.reader`，推送前 `pidof com.iapp.app` 为空、前台为 MIUI 桌面）：

```
export MSYS_NO_PATHCONV=1
python tools/push.py com.jianyue.reader --serial cdc69048
→ src/ 31 files pushed
→ .project / AndroidManifest.xml / icon.png 3 files pushed
→ 退出码 0（完成）
```

**结论**：

| # | 结论 | 级别 |
|---|---|---|
| R8-1 | 红米 Note 8 = API 30 / MIUI 12.5.5 / 骁龙 665 / arm64+armv7 / 1080×2340@440 / 6G RAM / 无 root | ✅ adb 2026-11-19 |
| R8-2 | iApp 5.0.1015（128）已装，工程根为默认 `Android/data/.../ProjectApp`，adb 整目录推送可用 | ✅ adb 2026-11-19 |
| R8-3 | 该机无 `su`，不能 `adb root`，`/data/data` 不可读 | ✅ adb 2026-11-19 |

**回填**：`docs/environments/redmi-note-8.md`（新建）；`docs/environments/README.md` 索引。
