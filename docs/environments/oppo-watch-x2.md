# OPPO Watch X2（手表，侧载目标）

## 元信息

| 项 | 值 |
|---|---|
| 环境 ID | W1（手表侧载目标，不是开发主机） |
| 宿主 | M1（见 `README.md` §机器编号） |
| 核验时间 | 2026-10-28 |
| 当前状态 | 仅「iApp 打包 APK 能装能启动」一条成立（⚠ 口述）；表**未接入 adb**，其余全 ❓ |
| 用途 | 手表应用（圆表盘 466×466）的唯一真机验收环境 |

开发仍在 M1 的雷电 14 上做（`.iyu` / `.mjava` / 打包），手表只负责安装与验收。

## 识别方法

- 连上后 `adb devices -l` 看型号。国行/海外版的型号与系统不同（见下节），**先确认是哪一版**。
- 本文件不预设 serial：手表通常走 USB（充电底座），serial 每次现查。

## 系统

| 项 | 读数 | 级别 · 来源 · 日期 |
|---|---|---|
| 型号 | OWWE251（海外版资料） | ⚠ 资料 2026-10-28 |
| 系统（国行） | ColorOS Watch 7.0，底层 Android 版本 ❓ | ⚠ 资料 2026-10-28 |
| 系统（海外） | Wear OS 5.0（Android 14 底）+ ColorOS Watch 7.0 皮肤 | ⚠ 资料 2026-10-28 |
| API 级 | ❓ | 怎么验：`adb shell getprop ro.build.version.sdk` |
| ABI | 至少含 `arm64-v8a`（APK 只带 arm64 原生库仍能装能跑） | ⚠ 用户口述 2026-10-28 |
| 屏幕 | 1.5″ 圆形 466×466，310 ppi | ⚠ 资料 2026-10-28 |
| 密度 | 社区传默认 320 → 画布约 233dp | ⚠ 资料 2026-10-28 |
| 实际尺寸/密度 | ❓ | 怎么验：`adb shell wm size` / `wm density` |

**架构结论**：能装 `arm64-v8a`-only 的 APK，说明不是纯 32 位用户空间；
社区「OPPO 表只能装 32 位」的说法对本机不成立（或只适用于旧机型）。

## 投递链路

表上**不跑 iApp**，所以没有共享目录、没有 FTP。只有「把打包好的 APK 送进去」这一件事。

| 通道 | 前置 | 命令 | 取证能力 |
|---|---|---|---|
| USB（主） | 开发者选项 + USB 调试 + 磁吸充电底座接电脑 | `adb install -r <apk>` | 有 logcat / screencap ❓ 未验 |
| 无线 adb | 固件有「无线调试」开关 | `adb pair <ip>:<port>` → `adb connect` | 同上 |
| 表内侧载 | 装「腕上网盘」一类应用 + 开「安装未知应用」 | 表上下载 APK 点安装 | 无 logcat |

- 进开发者模式：设置 → 其他设置 → 关于手表 → 连点「版本号」7 次 → 开发者选项 → 打开 USB 调试。
- 打包版 `i.syso`（`ygs` 日志）是死的，调试一律 `android.util.Log`，靠 `adb logcat` 取。

## 工程根

不适用（表上没有 iApp 工程）。

## 权限与 root

| 项 | 状态 |
|---|---|
| root | ❓ 怎么验：`adb shell su -c id` |
| `MANAGE_EXTERNAL_STORAGE` | 打包 APK 会声明；表上是否可授 ❓ 怎么验：`adb shell appops get <包名> MANAGE_EXTERNAL_STORAGE` |
| `POST_NOTIFICATIONS` | 运行时权限，首启会弹窗 ❓ |
| 「安装未知应用」 | 表内侧载必须开，USB adb 安装不依赖它 ⚠ 资料 |

**建议**：手表应用的文件读写一律走应用私有目录（`getFilesDir()` / `getExternalFilesDir()`），
不要依赖 `MANAGE_EXTERNAL_STORAGE`。

## 已知坑

1. **圆屏裁切**：466px 圆形，四角不可见。ppt 内容是矩形布局，靠边的内容会被切掉。
   设计按有效直径 ~210dp、四角留白。
2. **密度可能被用户改**：社区流行改 DPI 让界面变小。按默认密度设计，别假设用户改过。
3. **没有输入法/键盘的可靠保证**：避免文字输入框，改用列表、按钮、滑动。
4. **iApp 做不了的能力**：表盘（watch face）、磁贴（Tile）、complication、环境模式专属 API；
   表冠大概率被系统映射成滚动/按键（❓ 未验）。
5. **国行无 GMS**：任何依赖 Google 服务的功能不可用。

## 未测项（每条都写怎么验）

| 项 | 怎么验 |
|---|---|
| API 级、`abilist`、`wm size`、`wm density` | 连 USB 后跑上节命令 |
| 表上 `adb logcat` / `screencap` 是否可用 | 连上后 `adb logcat -d`、`adb exec-out screencap -p > s.png` |
| 桌面入口：装完从哪儿启动 | 用户看表上应用列表并回报 |
| 圆屏实际裁切范围 | 探针页画一个 466px 正方形边线 + 中心十字，截图看四角被切多少 |
| 密度改没改过 | `wm density` 与 `ro.sf.lcd_density` 对比 |
| 后台存活 / 息屏行为 | 息屏 1 分钟后回 `adb shell dumpsys activity activities \| grep <包名>` |
| 表冠事件 | 绑 `downkey` 事件，转表冠看 `st_kC` |

## 取证

- `docs/evidence.md` §2026-10-28 WATCH-1（安装+启动成功，口述）
