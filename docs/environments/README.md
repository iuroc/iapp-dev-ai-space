# 环境档案索引

一台机器一套环境。根 `CLAUDE.md` 只写「怎么选」，这里写「这台/这类机器长什么样」。
通用知识（iApp 本身的能力、投递通道的选择方法）在 `.claude/skills/iapp-development/`，不在这里重复。

## 先探测，再读档案

```bash
python docs/scripts/detect_env.py            # 人读摘要
python docs/scripts/detect_env.py --json     # 机器可读
```

拿到「产品 / Android / adb / 共享目录 / 通道」后再翻对应档案。探测不到也不要猜，标 ❓ 并写清怎么验。

## 机器编号

| 编号 | 机器 | 状态 |
|---|---|---|
| M1 | 当前这台：Windows 10 Pro Education 19045，雷电 14 + 雷电 9 并存 | **主开发机** |
| M2 | 另一台：Windows 11，只能开 Hyper-V，只有腾讯应用宝电脑版，无可用 adb | 备用/协作机，本机未复验 |

机器全称只在这里写一次，档案里只写 `M1` / `M2`。

## 状态图例

| 记号 | 含义 |
|---|---|
| ✅ | 在本机（或注明的那台机器上）实测通过，带日期 |
| ⚠ | 有条件成立 / 他机读数 / 口述，本机未复验 |
| ❓ | 未测，必须在条目里写「怎么验」 |
| ❌ | 实测不可用 |
| — | 不适用 |

级别怎么标、怎么升降，见 `.claude/skills/docs-architecture/references/evidence-and-levels.md`（本文件只写图例与事实）。

## 能力矩阵

| 维度 | 雷电 14（M1，主） | 雷电 9（M1，备） | 应用宝电脑版（M2） |
|---|---|---|---|
| 宿主 OS | Win10 Pro Education 10.0.19045 ✅ 2026-10-28 | 同左 ✅ | Windows 11（具体版本 ⚠ 他机） |
| 宿主虚拟化 | Hyper-V 未启用（`HypervisorPresent=False`）✅ 2026-10-28 | 同左 ✅ | 必须开 Hyper-V ⚠ 他机口述 |
| 产品版本 | 雷电 14.0.32.1 ✅ | 雷电 9.5.42.0 ✅ | 应用宝电脑版（版本 ❓） |
| Android / API | 14 / 34 ✅ | 9 / 28 ✅ | ❓（>11 猜测，无读数） |
| adb | ✅ `emulator-5556`（或 `127.0.0.1:5557`） | ✅ 宿主端口 5555（未连接时 `adb devices` 为空） | ❌ 自带 `adb.exe` 但 `adb devices` 为空 ⚠ 他机 |
| root | `su -c id` → uid=0 ✅ | `adb root` → uid=0 ✅ | ❓ |
| 共享目录 | `android-sync/` ↔ `/sdcard/Pictures` ✅ | 同左 ✅ | ❓ |
| iApp 工程根 | `Android/data/com.iapp.app/files/iApp/ProjectApp` → 软链 `Pictures/ProjectApp` ✅ | `/sdcard/iApp/ProjectApp`（可直接改）✅ | ❓ |
| 工程根可否改 | 只能在 app 内改到 `Android/data` 内，出界需 root 软链 | 可在 iApp 设置里直接改到 `Pictures/ProjectApp` | ❓ |
| 存储权限 | `MANAGE_EXTERNAL_STORAGE=allow` ✅ | `READ/WRITE_EXTERNAL_STORAGE`（运行时）✅ | ❓ |
| FTP（宿主→设备） | ❌ 直连不通；✅ 经 `adb forward`（含逐数据端口）2026-10-28 | ❓ | ✅ 匿名可登录 ⚠ 他机 2026-10-27 |
| FTP（设备内→自身） | ❓ 待设备内终端探测 | ❓ | ❓ |
| 推荐通道 | 共享目录（adb 兜底） | 共享目录 / adb | FTP |
| 版本定位 | **主开发**（API 34 优先） | 仅按需做低版本兼容 | 该机器的主环境 |

## 通道总览

| 通道 | 什么时候用 | 详见 |
|---|---|---|
| 共享目录镜像 | 宿主目录与设备目录双向映射 | 各档案「投递」节 + SKILL `references/emulator-setup.md` |
| `adb push/pull` | `adb devices` 有 `device` 行 | 各档案「投递」节 |
| iApp 内置 FTP（直连） | 设备装 iApp、控制台已开、**宿主能直达端口** | SKILL `references/ftp-delivery.md` |
| iApp 内置 FTP（`adb forward`） | 同上，但宿主到设备网络不通、有 adb | 同上 §7 |
| 手工导入 | 以上都不通 | SKILL `references/delivery-guide.md` |

**本工作区推荐顺序**（按开发用途，详见 SKILL `references/environment-adaptation.md`）：

1. 共享目录（日常改码）
2. `adb push/pull` + `logcat`（单文件 / 取证 / 共享目录核不上）
3. FTP —— 先看能否直达：雷电 14 上 ❌，需 `adb forward`；应用宝 M2 上 ⚠（他机）可直连
4. 手工导入

判断「能否直达」用 `Test-NetConnection <设备IP> -Port <端口>`，不要只看 `ping`。

## 档案骨架

每份档案固定这些节：元信息（环境 ID / 机器 / 核验时间）/ 识别方法 / Android / 投递链路 / 工程根 / 权限与 root / 已知坑 / 未测项 / 取证。

## 维护规则

1. 一条事实只放一个主文件，别处交叉引用；原始 logcat/截图进 `docs/evidence.md`。
2. 每条事实带「级别 + 来源 + 日期」；口述必须标「未复测」。
3. 档案写「环境类」的长期事实；本机当前连接、端口、UID 这类快照放 `docs/runtime-env.md`。
4. 与 SKILL 冲突时：**原始读数 > 环境档案 > SKILL 通用结论**。SKILL 只改条件/级别，不抄读数。
5. 探测脚本升级后，先追加 `evidence.md`，再更新档案。

## 索引

- `ldplayer14.md` — 雷电 14 / API 34（M1 主开发环境）
- `ldplayer9.md` — 雷电 9 / API 28（M1，仅按需）
- `tencent-appstore-pc.md` — 腾讯应用宝电脑版 / Windows 11（M2，无 adb）
- `oppo-watch-x2.md` — OPPO Watch X2 圆表盘（侧载目标 W1，不是开发主机）
