# OPPO Watch X2（手表，侧载目标）

## 元信息

| 项 | 值 |
|---|---|
| 环境 ID | W1（手表侧载目标，不是开发主机） |
| 宿主 | M2（应用宝电脑版，实测 adb 直连）；M1 亦可 |
| 核验时间 | 2026-10-28 |
| 当前状态 | adb 直连可用；API 30 / 纯 32 位；三架构 APK 可装可跑；iApp 打包的手表版八页示例工程已跑通 ✅ 2026-10-29 |
| 用途 | 手表应用（圆表盘 466×466）的唯一真机验收环境 |

开发与打包在**应用宝容器内的 iApp** 完成，手表只负责安装、运行与取证。

## 识别方法

- `adb devices -l` 看 `model`：`OWW251`（本机实测）。
- serial 每次现查（`d96d6a4e` 是 2026-10-28 的读数，不作为常量）。
- 连上先核 `ro.build.version.sdk`，本机为 30。

## 系统

| 项 | 读数 | 级别 · 来源 · 日期 |
|---|---|---|
| 型号 | `OWW251`（OPPO，`ro.oplus.wear.oppo.product=true`） | ✅ adb 2026-10-28 |
| Android / API | 11 / 30 | ✅ adb 2026-10-28 |
| 固件 | `OWW251_11_A.265`，构建 2026-08-27，安全补丁 2024-03-05 | ✅ adb 2026-10-28 |
| ColorOS Watch 版本 | ❓ | 怎么验：表内「设置 → 关于手表」 |
| ABI | `armeabi-v7a`、`armeabi`；`abilist64` 为空，`ro.zygote=zygote32` | ✅ adb 2026-10-28 |
| CPU | Qualcomm MONACO，ARMv7 rev4 ×4 | ✅ `/proc/cpuinfo` 2026-10-28 |
| 屏幕 | 466×466，圆屏（`ro.oplus.wear.screen.round=true`） | ✅ `wm size` 2026-10-28 |
| 密度 | 320（`wm density` 与 `ro.sf.lcd_density` 一致，比例 2.0 → 画布 233dp） | ✅ adb 2026-10-28 |
| 内存 | MemTotal 1,873,636 kB | ✅ `/proc/meminfo` 2026-10-28 |
| root | ❌ `su` 不存在（`shell` uid=2000） | ✅ adb 2026-10-28 |

**架构结论**：这块表是**纯 32 位用户空间**。APK 的 `lib/` 必须含 `armeabi-v7a`，
只带 `arm64-v8a` 的包装不上（`INSTALL_FAILED_NO_MATCHING_ABIS`，`res=-113`）。
2026-10-28 之前的「能装 arm64-only APK」口述**已被推翻**。

## 投递链路

表上**不跑 iApp**，只有「把打包好的 APK 送进去」。

```
应用宝容器内 iApp（开发 + 打包）
   └─ FTP 取回 APK → 宿主 Windows
        └─ adb install -r <apk>  → 手表
             └─ am start / logcat / screencap（取证）
```

| 通道 | 前置 | 命令 | 取证能力 |
|---|---|---|---|
| USB adb（主） | 开发者选项 + USB 调试 + 充电底座接电脑 | `adb install -r` | logcat / screencap / pidof ✅ 2026-10-28 |
| 无线 adb | 固件有无「无线调试」 ❓ | 怎么验：表内开发者选项找「无线调试」，开 `adb pair` / `adb connect` | 同上，未验 |

- 打包产物在容器内 `/ProjectApp/<项目ID>/bin/<包名>.apk`，可用 `ftp_sync.py` 或 `ftplib` `RETR` 取回。
- 启动组件统一是 `<包名>/com.iapp.app.run.mian`（`cmd package resolve-activity --brief` 可查）。
- 打包版 `i.syso`（`ygs`）是死的，调试一律 `android.util.Log`，用 `adb logcat -s <tag>:V` 取。

## 工程根

不适用（表上没有 iApp 工程）。

## 权限与 root

| 项 | 状态 |
|---|---|
| root | ❌ `su` 不存在 ✅ 2026-10-28 |
| `MANAGE_EXTERNAL_STORAGE` | ❓ 怎么验：`adb shell appops get <包名> MANAGE_EXTERNAL_STORAGE` |
| `POST_NOTIFICATIONS` | ❓ 运行时权限，首启是否弹窗未验；怎么验：装包后首启观察是否弹权限窗，或 `adb shell dumpsys package <包名>` 查 `POST_NOTIFICATIONS` 授权态 |

**建议**：文件读写走应用私有目录（`getFilesDir()` / `getExternalFilesDir()`）。

## 已知坑

1. **ABI 默认只勾 arm64**：iApp 设置 →【打包设定so库】必须勾上 `armeabi-v7a`，
   否则产物装不上这块表（详见 SKILL `.claude/skills/iapp-development/references/delivery-guide.md` §产物可移植性）。
2. **圆屏裁切**：466px 圆形，四角不可见；按约 233dp 画布、内容收在中央安全区。
3. **息屏很积极**：界面静置即息屏；`screencap` 可能拿到全白图。
   取证优先用 `logcat`，截图前先唤醒或由用户操作。✅ 2026-10-28
4. **表冠是滚动轴，不是按键**：`/dev/input/event3` 名为 `oplus_crown`，只发
   `EV_REL/REL_WHEEL`（20 秒 307 次，值 `-15…+24`，正负即方向），**没有 `EV_KEY`**；
   `downkey` 收不到，要用表冠得接 `MotionEvent.ACTION_SCROLL` + `AXIS_SCROLL`。✅ 2026-10-29
   - 系统用途 = **上下滚动页面**（用户确认 ✅ 2026-10-29）
   - iApp 里取值：`MotionEvent.ACTION_SCROLL` 下，**`AXIS_VSCROLL` 才有值**
     （`AXIS_SCROLL` 与 `AXIS_HSCROLL` 恒 0）；顺时针为负、逆时针为正。✅ 2026-10-29
   - **页面放进 `ScrollView` 后，表冠可直接原生滚动，无需写代码** ✅ 2026-10-29（用户观察）
   - 侧键 / 表冠按下走 `gpio-keys`：`131`（F1）= **回桌面**、
     `132`（F2）= **打开运动功能页**（骑行/跑步等运动模式列表，用户确认 ✅ 2026-10-29）、
     `138`（F8）用途未确认 ❓，怎么验：`adb shell getevent -l` 后逐个按侧键，对照 `kc=138` 触发的系统界面
     —— 都是系统占用，应用不要拿来做功能键
   - 其它厂商的手表**不一定**沿用同样的映射（用户提示），跨机型要重新测 ⚠
6. **左滑返回对第三方应用不生效**：滑动是纯触摸事件（`fts_ts` 的 `BTN_TOUCH` +
   `ABS_MT_POSITION`），系统**不翻译成按键**；三种方向的 `input swipe` 都无法退出应用。
   要在页面内返回，只能自己在 `OnTouchListener` 里识别横向滑动 ✅ 2026-10-29
5. **返回不派发 `kc=4`**：按返回后应用只是**退到后台**（`paused`，未 `finish`），
   `downkey` 绑定也拦不到；需要真退出得自己放入口（如长按/按钮调 `activity.finish()`）。✅ 2026-10-28
6. **没有可靠的输入法**：避免文字输入，用按钮/列表。
7. **iApp 做不了**：表盘（watch face）、磁贴（Tile）、complication、环境模式专属 API。
8. **国行无 GMS**：依赖 Google 服务的功能不可用。
9. **启动噪声**：`FileNotFoundException: userencryption.xml` 与
   `ClassNotFoundException: <包名>.IConfig` 会出现在 `System.err`，不影响运行 ✅ 2026-10-28。

## 取证（✅ 2026-10-29）

表很爱息屏，且插着 USB 时会弹出**充电全屏界面**（`SysUI.Charging`）抢走焦点。
固定三步，缺一步就会拿到全白截图或拿不到事件：

```bash
adb -s <serial> shell svc power stayon usb    # USB 供电时常亮，防自动息屏
adb -s <serial> shell input keyevent 131      # 侧键事件，让充电界面让开焦点
adb -s <serial> exec-out screencap -p > s.png # 此时截图稳定
```

- 测完记得还原：`adb shell svc power stayon false`
- 焦点确认：`dumpsys window | grep mCurrentFocus`，必须是你自己的窗口
- 应用在后台时表冠/按键事件会被系统收走，`logcat` 里不会有任何记录

## 未测项（每条都写怎么验）

| 项 | 怎么验 |
|---|---|
| 表冠在 iApp 里怎么接 | 根 View `setFocusable(true)` + `requestFocus()`，再 `setOnGenericMotionListener` 读 `ACTION_SCROLL`/`AXIS_SCROLL`；`downkey` 无解 |
| 主动退出的可靠入口 | 手势返回不派发 `kc=4`；试长按事件 / 页面内按钮调 `activity.finish()` |
| 桌面入口位置 | 装完后在表上应用列表里找并截图 |
| 圆屏实际裁切 | 探针页画 466px 正方形边线，截图量四角被切多少 |
| 长时间后台存活 | 息屏 10 分钟后 `pidof <包名>` + `dumpsys activity activities` |
| 无线 adb | 表内开发者选项找「无线调试」 |
| `MANAGE_EXTERNAL_STORAGE` | `adb shell appops get <包名> MANAGE_EXTERNAL_STORAGE` |

## 取证

- `docs/evidence.md` §2026-10-28 WATCH-2（全链路：FTP 投递、打包 ABI 对照、安装、日志、息屏存活）
- `docs/evidence.md` §2026-10-28 WATCH-1（旧口述，已被 WATCH-2 修正）
