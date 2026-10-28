# 安卓手表应用（iApp）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **状态：待排期。** 可行性已确认，功能目标未定；Task 0–2 与功能无关，可以先做。

**Goal:** 用 iApp 做一款适配圆表盘（主目标 OPPO Watch X2，466×466）的应用，交付形态是 APK，
经 USB 侧载到手表安装运行。

**Architecture:** 与现有 iApp 工程一致——`.iyu` 只声明布局与绑事件（`call` / `addv`），
具体逻辑放 `.mjava`。开发与调试全部在雷电 14（API 34）上完成，
手表只承担「装上去看一眼」的真机验收；表上不装 iApp，也不存在共享目录 / FTP 通道。

**Tech Stack:** iApp 5.0.1013（裕 3 + mjava/BeanShell）、开发环境 Android 14 / API 34、
打包产物 minSdk 21 / targetSdk 36、原生库仅 `arm64-v8a`。

**Env profile:** `docs/environments/oppo-watch-x2.md`（W1）
**Evidence:** `docs/evidence.md` §2026-10-28 WATCH-1

## 已确认 / 未确认（开工前必须分清）

| 结论 | 级别 | 来源 |
|---|---|---|
| iApp 打包 APK 可安装到 OPPO Watch X2 并启动 | ⚠ 口述 | 2026-10-28 |
| 打包 APK 自包含，表上不需要装 iApp 本体 | ⚠ 推断（APK 结构） | 2026-10-28 |
| 手表用户空间至少支持 `arm64-v8a` | ⚠ 由上行反推 | 2026-10-28 |
| 屏幕 466×466 圆、310 ppi、1.5″ | ⚠ 资料 | 2026-10-28 |
| 默认密度 320（画布约 233dp） | ⚠ 社区资料 | 2026-10-28 |
| API 级 / 实际密度 / 圆屏裁切量 / 表上 logcat | ❓ | 见 Task 0 |

## Global Constraints

- **画布**：按 233dp 见方设计（466px ÷ 2.0）；Task 0 测出真实值后修正这个基准
- **圆屏安全区**：四角不可见，正文与可点元素都收在有效直径内（先按 ~210dp 设计）
- `.iyu` 事件体只允许 `call` / `addv`；逻辑下沉 mjava
- 控件优先在 ppt 声明；`type=` 含点号要在 `build.xml` `<newControl>` 登记
- 打包版 `i.syso`（`ygs`）无输出，调试一律 `android.util.Log`
- 文件读写走应用私有目录（`getFilesDir()`），**不依赖** `MANAGE_EXTERNAL_STORAGE`
- 不假设有软键盘：避免文字输入，交互用按钮 / 列表 / 滑动
- 不做表盘（watch face）、磁贴（Tile）、complication、ambient 模式——iApp 无此能力
- 包名、应用名未定，Task 1 开工前定稿；不得出现个人姓名 / 缩写 / 个人域名

## Review Focus

- 页面在 233dp 圆屏上是否有内容被四角裁掉、文字被截断
- 表上首启是否弹权限窗（`POST_NOTIFICATIONS`）导致白屏或卡住
- 息屏 → 亮屏后回到前台是否重建页面、状态是否丢
- 打包版与开发模式的视觉差异（画布不执行 mjava，重复样式会不一致）
- APK 体积与冷启动时间（表上 2GB RAM，BeanShell 解释执行）

---

### Task 0: 手表基准读数与圆屏探针（无功能依赖，优先做）

**Files:**
- Create: `android-sync/iapp-demo/watch-probe-20261028/mian.iyu`
- Create: `android-sync/iapp-demo/watch-probe-20261028/probe.mjava`
- 完成后：`docs/evidence.md` 追加 WATCH-2，修正 `docs/environments/oppo-watch-x2.md` 的 ❓ 项

**Interfaces:**
- Produces: 一组真机读数（API / 密度 / 裁切量），后续所有页面的尺寸常量以此为准
- Produces: `probe.metrics()` 可复用到正式工程做运行时自检

- [ ] **Step 1: 连表取静态读数**（表开开发者选项 + USB 调试，充电底座接电脑）

```bash
adb devices -l
adb -s <serial> shell getprop ro.build.version.sdk
adb -s <serial> shell getprop ro.product.cpu.abilist
adb -s <serial> shell wm size; adb -s <serial> shell wm density
adb -s <serial> shell getprop ro.sf.lcd_density
```

- [ ] **Step 2: 写探针页**：界面印 `widthPixels × heightPixels`、`density`、`densityDpi`、
  屏幕尺寸 dp；再画一个 466px 正方形边线 + 中心十字 + 每 30° 一根刻度线（`Canvas` → `ImageView`）
- [ ] **Step 3: 打包并安装**：iApp 内打包 → `adb install -r bin/<包名>.apk`
      （无 adb 时：表上「腕上网盘」一类应用侧载，用户截图回报）
- [ ] **Step 4: 取证**：`adb exec-out screencap -p > docs/artifacts/watch-probe.png`；
      同时 `adb logcat -d -s AndroidRuntime:E` 确认无崩溃（打包版 `ygs` 不可用）
- [ ] **Step 5: 回填**：读数进 `docs/evidence.md`，结论进 `docs/environments/oppo-watch-x2.md`，
      把本文件 Global Constraints 的「233dp」换成实测值
- [ ] **Step 6: 清临时探针**：删 `android-sync/iapp-demo/watch-probe-20261028/`（保留截图）

**Acceptance:** 截图上能读出四角被裁掉的像素范围，且有 `wm size` / `wm density` 原始文字读数。

---

### Task 1: 手表工程骨架与尺寸常量

**Files:**
- Create: `android-sync/ProjectApp/<包名>/`（`.claude/skills/iapp-development/scripts/create_project.py` 生成最小集）
- Create: `src/mian.iyu`（单页壳：圆形底色 + 安全区容器）
- Create: `src/ui.mjava`（尺寸/配色常量、自检）

**Interfaces:**
- Produces: `int ui.dp(int v)`、`int ui.safeW()`（安全区宽度 dp）、`void ui.boot()`
- Produces: 运行时打印 `UI metrics` 的自检（打包版可用 `Log`）

- [ ] **Step 1: 建工程**（`.project` / `AndroidManifest.xml` / `icon.png`，按 `.claude/skills/iapp-development/scripts/create_project.py`）
- [ ] **Step 2: 根容器**：`FrameLayout` + 圆形背景；内容放进居中的安全区容器
- [ ] **Step 3: 常量模块**：字号四级、间距 4 的倍数、主色/底色，全部集中在 `ui.mjava`
- [ ] **Step 4: 模拟器预览对齐**：雷电 14 上 `wm size 466x466` + `wm density 320` 临时切到手表尺寸，
      确认与表上截图一致后切回
- [ ] **Step 5: 装机验证**：打包 → 安装 → 截图对照

**Acceptance:** 表上与模拟器上同一页面观感一致；没有任何元素越过安全区。

---

### Task 2: 页面骨架与导航（依赖功能形态）

**Files:**
- Create: `src/*.iyu`（按页面数）
- Create: `src/nav.mjava`（`i.uigo` 跳转与返回处理）

- [ ] **Step 1: 定页面数量与跳转图**（单页 / 两页 / 列表+详情）
- [ ] **Step 2: 每页一个 `.iyu`**，`uigo` 跳转；返回键按 `.claude/skills/iapp-development/references/navigation-guide.md` 处理（绑 `downkey` 会吞返回键）
- [ ] **Step 3: 状态放 `i.sss`**（模块变量跨 `call` 必丢）
- [ ] **Step 4: 表上跑一遍完整路径**

**Acceptance:** 页间往返不丢状态、返回行为符合预期、转场不闪白。

---

### Task 3: 功能实现（**阻塞：等应用目标确定**）

待用户给出「做什么用、数据从哪来（本地 / 网络 / 传感器）、几个页面」后，拆成独立 Task。
候选能力与风险需在此确认：

| 能力 | 可行性 | 备注 |
|---|---|---|
| 本地存储 | ⚠ 待验 | 用 `getFilesDir()`，不碰外部存储 |
| 网络请求 | ⚠ 待验 | 表上有 Wi-Fi；无 GMS，不依赖 Google 服务 |
| Canvas 自绘 / 动画 | ✅ 预期可行 | 与屏幕形状无关，已有配方 |
| 传感器 / 健康数据 | ❓ | 健康数据多为 OPPO 私有接口，iApp 大概率取不到 |
| 通知 / 后台常驻 | ❓ | 手表对后台更激进，需单独验 |

---

### Task 4: 打包与交付

- [ ] **Step 1: 工程信息定稿**：包名、应用名、`icon.png`（`.claude/skills/iapp-development/scripts/make_icon.py` 生成圆角安全版）
- [ ] **Step 2: 打包**：iApp 内手动打包（versionCode = 100000 + versionint）
- [ ] **Step 3: 安装**：`adb install -r bin/<包名>.apk`；升级覆盖同包名
- [ ] **Step 4: 交付记录**：APK 与截图归档到 `docs/artifacts/`，版本与安装方式写进 evidence
- [ ] **Step 5: 体检**：`review_docs.py --fail-on blocker` + `check_portable.py`

**Acceptance:** 手表上从应用列表启动、跑完主流程、无崩溃日志。

## 风险与待决

| 项 | 影响 | 处置 |
|---|---|---|
| 真实画布 / 裁切量与资料不符 | 全部页面尺寸要改 | Task 0 先测，再写页面 |
| 圆屏矩形布局裁角 | 内容不可读 | 安全区容器 + 表上截图逐页验收 |
| 表上无可用 logcat | 排查只能靠截图 | Task 0 验；不行就让页面自带日志面板 |
| 输入法不可用 | 不能做输入型功能 | 设计上回避 |
| 健康/传感器数据取不到 | 部分功能不可行 | Task 3 前确认数据源 |
| 应用功能未定 | Task 3 无法排期 | 需求确定后追加 |

## 排期建议

1. **Task 0 + Task 1**（约一轮）：拿到基准、立起骨架，之后所有页面都有统一尺寸依据
2. **Task 2**：页面结构随功能一起定
3. **Task 3–4**：等功能明确后展开

功能确定前不要动 Task 2/3——页面结构会被推翻。
