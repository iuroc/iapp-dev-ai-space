---
name: iapp-development
description: 开发、调试、打包 iApp（Android 可视化 IDE，显示名"测兆编程"）工程时使用。只要出现 .iyu 界面文件、.mjava 模块、裕语言语法、call 跨语言调用、iApp 工程结构、adb 投递调试、iApp 打包交付，或换机器/换模拟器/无 adb 环境、FTP 投递、共享目录同步等环境适配需求，就先读本技能。里面有实测过的语法铁律、失败签名、三条投递通道的选择方法与探针方法，能避免重复踩坑；不确定的行为按本技能的探针流程先测再写。
---

# iApp 开发知识库

iApp（显示名"测兆编程"）是 Android 上的可视化 IDE：工程是「界面文件 + 模块代码 + 资源」的目录，直接在设备上编译运行。

> **适用边界**：iApp 适合手机 App。手表只到「能跑」这一级，属**实验性**——
> 中高端表上页面跳转与代码解释卡顿 1~3 s，正式手表应用建议走官方方案。
> 详见 `references/watch-app-guide.md` §0。

## 写什么 / 不写什么（本库的边界）

本库优先记录 **iApp 特有** 的行为，不重复通用 Android / Java 知识；通用知识只在它是“iApp 里可直接复制的完整配方”时收录（如 Canvas 卡面、外部库装载）。

- **不写**：与原生 Android / Java 完全一致的零散用法。例如 `Paint.setAntiAlias(true)`、`FileWriter` 读写文本、`AlertDialog.Builder` 的基本链式调用——凭通用知识就能写对，写进来只增加维护负担和过期风险。
- **必写**：在 iApp 里**不能照原生 / Java 的写法直接用**，需要转换、绕开或额外处理的。判据是"照通用知识写会失败或静默不生效"，包括：
  - 语言层限制：BeanShell 不支持 `final`、具名 class、`0xFF` 大十六进制字面量、可变参数；模块级变量跨 `call` 丢失
  - 能力缺失：不能继承类（自定义 View / Adapter 要走 dex）；裸 `findViewById` 不存在
  - 属性 / 事件名与原生不一致：ppt 用 `layout_weight` 而不是 `weight`；`alpha`、`weight` 在 ppt 里静默无效；事件名写错静默忽略
  - 宿主环境副作用：开发模式跑在 `com.iapp.app` 进程里，`getFilesDir()` 多工程共用、权限是宿主的、改系统 UI / 方向会影响宿主
  - 需要双证据才敢下结论的：行为与文档不一致、版本相关（API 28 vs 34）
- **本库会被单独拷走分享**：里面**不许出现读者拿不到的东西**——作者自己的工程包名、一次性探针的工程名、工作区内部路径、别的 skill / agent、已删除的目录。读者拿到这些只会当成「必填项」或「该去下的东西」，然后照着做失败。
  - 能出现的只有两类：**读者能自己找到的**（宿主包 `com.iapp.app`、`com.android.*`、`com.google.android.*`、公开开源库 `com.xuexiang.*`、JDK）与**明确标成示例的占位**（`com.example.*`、`<项目ID>`、`<宿主工程目录>`）
  - 举证需要指向具体工程时，写成「一次性探针 · 状态栏类型矩阵」这种**描述性名称**，不写包名
  - 由 `scripts/check_portable.py` 兜底检查
- **写法**：先写"原生写法是什么 → 在 iApp 里会怎样 → 应该怎么写"三段式；结论带 ✅/⚠/❓ 与版本前提。
- **更新前自检**：新增内容如果删掉后，一个懂 Android / Java 的人照样能写对，就不该进来；除非它是 iApp 环境里必须原样复制的完整配方。

## 路径写法（写实还是占位）

本库要分享给别的 workspace，但不等于把路径全变成占位符。判据是**这个值对“大多数用这个环境的人”是否成立**：

- **写实**：常见环境/工具的默认路径，例如 `C:\Program Files`、`C:\LDPlayer\LDPlayer9`、`/sdcard/Pictures`、`/data/media/0`、`com.iapp.app`。这些是通用知识，写实才方便别人照着做。
- **占位或环境变量**：只对作者机器或本项目成立的，例如 `<作者盘符>\...` 这种作者机器路径；随实例/项目变化的，例如 `<serial>`、`<VM-UUID>`、`<项目ID>`；版本化工具目录用 `BUILD_TOOLS` / `JDK_BIN` / `DEXDUMP` 覆盖，文档同时给常见默认位置。
- **不要为了“可移植”把常见路径泛化成 `<目录>` 或 `%ENV%`**；只有确实没有共识默认值时才这么做。

## 五分钟模型

```
工程根/                       # 设备上的实际位置随环境不同（iApp 内设置或按环境文档）
├── src/
│   ├── mian.iyu              # 入口界面（必须叫 mian.iyu）
│   ├── *.iyu                 # 其它界面
│   └── *.mjava               # Java 模块（无 class 外壳，直接写方法）
├── files/                    # 运行期文件
├── res/  sdk/  icon.png
├── AndroidManifest.xml
└── .project                  # 工程元数据
```

界面文件是伪 XML：`<View id= did= type=>` + `<ppt>` 属性块 + `<event>` 事件块；
全局事件集中在文件末尾 `<UIEventset>`，事件项写成 `<eventItme type="loading">代码</eventItme>`。

代码分两种语言，可互相调用：
- `.iyu` 里只留 `call(...)` / `addv(...)` 做编排（日志、Toast、运行期改动都在 mjava 里；静态样式写 ppt）
- `.mjava` 里是 Java 语法，但**由 BeanShell 解释执行**，不是编译成 class（报错原文见 `references/mjava-guide.md`）

`call` 三要素：`call(接收返回值的变量, "mjava", "模块.方法", 参数…)`；无返回/无参用 `call(null, "mjava", "app.run")`。
传给模块的参数个数要与方法签名一致，返回值只对 mjava 有效。

## 实现取向：能复用库就别自己写

iApp 是冷门环境，本库的规则管的是**大方向**——`.iyu`/`.mjava` 怎么写、`call` 与 `i.fn` 怎么调、
工程怎么投递。**具体实现**则优先用 Android / AndroidX / Material / 开源库里已有的东西，
不要自己造：自己写的每一行都要在这个环境里重新踩一遍坑，而库里的行为已经被人跑过千万遍。

- **先查支持矩阵**：`references/material-components.md` 列出 iApp 5.0.1013 内置的 material 1.13.0
  可用组件（抽屉、底部面板、弹窗、进度、输入框、FAB…），用之前先看那一格是 ✅ 还是 ⚪
- **要「行为」就找带行为的容器**：底部面板要拖动/遮罩/收起动画 → `BottomSheetDialog`；
  侧边导航要边缘拖拽与遮罩 → `DrawerLayout`；长列表要回收 → `RecyclerView`。
  不要自己接 `OnTouchListener` 攒手势、自己拼动画——那是在手搓库的下半截
- **适配 ≠ 自造**：库组件在 iApp 里可能要改 Context、改主题、改构造方式（见
  `references/material-components.md` §样式注意），但那是「按库的正确用法装配」，
  不是「绕开库自己画一个像它的」
- **判据**：一个需求如果能用「库组件 + 参数」表达，就不要用「自绘 View + 触摸事件」表达
- **代价有实例**：把 `DrawerLayout` 当全屏浮层用，关掉后它吞掉整页点击（pitfalls #41）；
  手写底部面板，结果遮罩瞬间消失、只能从抓手拖动；`ObjectAnimator.ofFloat` 变参绑不上（pitfalls #43）

## 界面构建：mjava 建树为默认，`.iyu` 只留根

**默认做法**：每个页面的 `.iyu` 只有一个全屏根容器加 `<UIEventset>` 全局事件表，
其余一切视图——容器、文本、图像、列表——都在 mjava 里建，样式用 setter 写。

| 问 | 命中 → |
|---|---|
| 是页面根容器（`id=1` 的全屏 `FrameLayout`）吗？ | 写在 `.iyu`，只带 `width` / `height` / `backgroundcolor` 三个键 |
| 是 `loading` / `loadingComplete` / `pause` / `resume` 事件吗？ | 写在 `<UIEventset>` |
| 其余一切视图、样式、监听器 | mjava 建（`src/ui.mjava`，函数清单见 `references/ui-kit.md`） |

为什么翻成这个方向（2026-10-30 实测批次 UIPROBE-1/2，雷电 14 / API 34 / 1080×1920）：

- `.iyu`/ppt 的未知键**静默忽略**，已踩 `alpha`、`weight`、`layout_gravity`、`padding` 按 px 四个坑；
  mjava 的未知面是一张 6 条的短清单（`mjava-guide.md`），遇到一次就记住
- mjava 建的视图与 ppt 声明在测量上**完全一致**：同属性下 `forcedMeasure` 都是 `463x70`，
  字号 `48.0` / 字重 / `maxLines` / `maxWidth` 全等——不存在"动态创建更脆"这回事
- 建 40 个视图 14 ms、整页在 `loading` 内建完 195 ms，一帧内做得完
- 若工程由 AI 持续维护、没有人依赖设计器预览，这条翻转的代价更低；迭代反馈本来就来自设备截图

**样式一律写在 mjava setter 里**：tint、描边、圆角、渐变、alpha、选中态、Ripple、间距。
ppt 只剩根上那三个键。分层规范见 `references/style-guide.md`。

**实现前提**（完整清单见 `references/ui-kit.md` §已知限制）：`loading` 阶段宽高为 0、
`getRootWindowInsets()` 为 null，尺寸取 `DisplayMetrics`、安全区在 `loadingComplete`/`resume` 应用；
不要装匿名的 `setOnApplyWindowInsetsListener`（整份模块 Parse error）；不能继承 View，
"组件"只能是工厂函数 + 命名句柄。

### 例外：确实要在 `.iyu` 里声明控件时

历史工程还在用 ppt 骨架的可以不动；某些独立探针页只想要一个静态界面看属性时也可以照旧。
这条路径下的规则不变：

`.iyu` 的 `type=` 只有两条来源，**写之前先看值里有没有点号**：

| `type` 写法 | 例子 | `build.xml` |
|---|---|---|
| 内置短名（无点号） | `TextView`、`LinearLayout`、`TextInputLayout` | 不用登记 |
| 完整类名（含 `.`） | `com.google.android.material.textfield.TextInputEditText` | **必须登记**，否则设计器显示“未知” |

- 判据是 **`type` 的语法**，不是“这个类算不算自定义 / 是不是 Material”
- 登记格式、随工程走、自查命令与“未知”控件的处理见 `references/project-structure.md` §build.xml 与自定义控件
- 短名清单在 `references/builtin-controls.md`，**不要按“安卓类名去包名”猜**（`Switch` 就不是短名）
- **`SearchBar` 不能走这条路**：写进 ppt 后设计器保存/序列化时崩（`VisualDesigner.T0` NPE，与登记无关）——
  `T0` 把每个 View 的 `tag` 当 `Object[]` 读，`id >= 1` 时跳过 null 检查，而 `SearchBar` 自建的内部子 View
  带资源 id 没有 tag → NPE。只能 mjava 建。`TabLayout` / `ChipGroup` / `MaterialDivider` 已实测排除
  （2026-10-27，`pitfalls.md` #7）
- **版本前提**：ppt 完整类名 = 真实实例是 API 34 实测；API 28 的旧结论是“影子实例”⚠

**Material 组件选型**：mjava 里直接 `new` 对应类即可，没有短名映射问题；
只有回到 ppt 声明时才需要写 `com.google.android.material.*` 完整类名（部分短名指向 iApp 封装或 androidx：
`TabLayout` → `com.iapp.app.TabLayout`、`CardView` / `SwitchCompat` / `Toolbar` → androidx）。
完整清单与支持矩阵见 `references/material-components.md`。

## iyu 白名单（只允许 `call` / `addv`）

`.iyu` 事件体**只允许 `call` / `addv`**。其它裕语言函数、Java 表达式（`activity.finish()`、`i.lan(...)`、
`end()`、`ViewGroup.removeView(...)` 等）一律下沉到 mjava，用原生写法。返回、转场、删视图都写成
mjava 方法，再由事件体 `call` 进去。

逐个函数的替代写法见 `references/iyu-whitelist.md` §替换表。

## 多模块（加载另一个 mjava）

`i.fn("b")` 加载、之后直接调 `b_hello()`。三条硬约束：**`importAll()` 写在 public 入口的方法体内第一行**
（写文件顶层或加载前调用都会让整个方法中断，`catch` 接不住）；**交付用 `i.fn`、源码直接打包**
（`i.d.f` 仅开发模式）；**跨模块加载不要用 `i.call`**（每次新建解释器，找不到当前工程模块）。
facade 模式、命名前缀与失败签名见 `references/modularization-guide.md`。

## 核心规则（iApp 硬约束 + 推荐做法）

【硬】= iApp 行为如此，不遵守会坏；【荐】= 本库推荐，按你的环境取舍。

1. 【硬】**入口必须是 `src/mian.iyu`**（不是 main.iyu）。
2. 【荐】**iApp 以内存为准**：外部改文件前先 `am force-stop`，或在 iApp 里关掉工程；否则保存/运行会用旧内存覆盖磁盘。
3. 【荐】**投递优先级：adb 整目录 → FTP → 手工导入**；共享目录通道已停用（2026-10-30）。
   任何通道都遵守：**改前关工程、整目录覆盖、只认返回码**——源在宿主，不读设备副本比对，
   验收靠运行现象与 `logcat`。通道选择、共同铁律与失败签名见 `references/environment-adaptation.md`。
4. 【荐】**双证据**：屏幕现象（screencap）+ 原文日志；取日志命令、错误前缀与判读见 `references/debugging.md`。
5. 【硬】日志 tag=`ygs`；mjava 里 `i.syso(...)` 的内容出现在这里（旧写法 `.iyu` 里的 `syso` 已按白名单禁用）。
   **注意**：iApp 的「数据调试工具」面板打开时，`i.syso` 只进面板、`adb logcat` 抓不到（2026-10-30 实测）；
   取证前先确认面板是关的，否则拿到 0 行会误判成"代码没跑"。
6. 【硬】控制台行号不可信（常报第 0 行），定位靠日志与现象。
7. 【荐】结论标注：✅实测 / ⚠推测 / ❓未知。null/false/0 必须有对照锚点。
8. 【荐】**界面默认 mjava 建树**：`.iyu` 只留根容器与 `<UIEventset>`，子控件、样式、监听器都在 mjava 里写，
   组件库见 `references/ui-kit.md`。只有在例外路径（历史工程、静态探针页）里用 `type=` 声明控件时，
   才涉及 `build.xml` 的 `<newControl>` 登记——这条已降级为例外说明，见「界面构建」一节的末尾。
9. 【荐】**换机器/换设备先勘测，别照抄上一台的路径**：确认五件事——设备能起且 iApp 已装、`adb devices` 有没有 `device` 行（不是「adb 可执行」）、iApp 设置里显示的工程根、有没有共享目录、FTP 能不能登。
   缺哪项就在结论里标 ❓ 并写清怎么验，不要用「应该/通常」代替。见 `references/environment-adaptation.md`。
10. 【荐】**版本优先高**：新功能与验证默认在可用的最高 Android 上做（写成这条时是 API 34）；
    API 28 及以下只做有限兼容，且要开发者明确要求才投入，不追求低版本结论与高版本追平。
11. 【硬】**不要用 `java { }` 内联块**：开发模式能跑，但**打包属 VIP**，非 VIP「强制打包」会删掉该功能；
    且有「一个块编译失败全工程块失效」「块不可复用」两个硬伤。仅作实验性存档，
    见 `references/inline-java-block.md`；工程一律走 `call` → `.mjava`。

## 已验证（能力速览）

一行一个能力，**只写边界与级别**；每条的依据、读数和写法在对应 reference 里。
新增验证先写进 reference，再决定要不要在这里加一行——不要把实现细节抄回来。

| 能力 | 边界 | 级别 |
|---|---|---|
| 入口与工程结构 | `src/mian.iyu` 是唯一入口；最小集 `.project` + manifest + `mian.iyu` + `icon.png` | ✅ |
| 语言层 | BeanShell 解释：无 `final` / 具名 class / `0xFF` / 可变参数；模块变量跨 `call` 丢；匿名类会中断载入事件，匿名接口可用 | ✅ |
| `i` 对象 | 390 方法 / 12 字段；`i.d` 每次 call 新建；`i.ss` 默认 null；`i.sss` 每次运行重置 | ✅ |
| 模块加载 | `i.fn` + `importAll()` 写在方法体内；`i.d.f` 仅开发模式；`i.call` 不用于跨模块 | ✅ |
| 事件 | 参数统一 `st_*`；Tab/Spinner 初始化会自动回调一次；`downkey` 会吞返回键 | ✅/❓ |
| 多页导航 | 每页一个 Activity 实例；`uigo` flag 只有 1073741824 有用；传参靠 `i.sss` | ✅ |
| `addv` 内嵌 | 只有 DrawerLayout 可用；内嵌 id 按文件首次内嵌顺序分 10000 号段 | ✅ |
| 界面构建 | mjava 建树为默认；ppt 未知键静默忽略；不能继承 View | ✅ |
| WebView 全前端桥接 | URL scheme + `shouldoverrideurlloading` 调 mjava；`i.has` 回传；`iapp.fn` 只认 yul 模块；file:// + universal access 可绕过 CORS | ✅ |
| ppt 声明控件 | 完整类名必须 `build.xml` 登记；`SearchBar` 会使设计器崩 | ✅/⚠ |
| Material | 1.13 内置 490 类、34/35 可 `(Context)` 构造；TIL 需 `loading` 修复 | ✅ |
| 外部库 | JAR→D8→dex；带资源 AAR 用独立包 ID + 两个 AssetManager；Android 14+ dex 只读 | ✅ |
| 动画与触摸 | `ObjectAnimator` 用数组变参；`getHistorySize(int)` 等重载会杀进程 | ✅ |
| 绘图与图标 | Canvas 现画；`invalidate()` 可刷新；工程图标由 `icon.png` 决定 | ✅ |
| 工程资源 | `res/` 图片用 `i.us(@名称)`；`getIdentifier` 恒 0 | ✅ |
| 状态栏 | 72px 来自宿主内容容器背景；铺满要挂 DecorView（1 个 `loading` 事件、5 行）；图标明暗走 insets 控制器；隐藏用 `hide()` | ✅ |
| 打包 | `versionCode = 100000 + versionint`；打包后 `ygs` 无输出、`VisualDesigner` 被裁 | ✅ |
| 投递 | adb 整目录优先；FTP 需逐数据端口 forward；共享目录通道已停用 | ✅ |
| 环境 | 两套雷电抢宿主 5555；实例改名可按序号永久分开 | ✅ |
| 已废弃 | `java { }` 内联块打包属 VIP → 不要用 | ⚠ |
| 崩溃源 | 同名方法后者覆盖；回调里的 `Command not found` 会崩进程 | ✅ |

## 导航

- `references/methodology.md` — 探针方法与铁律
- `references/recipes.md` — 常用配方、持久化、自检、Canvas 卡面与 API 28 注意事项
- `references/animation-guide.md` — mjava 动画（ObjectAnimator / postDelayed / 3D 倾斜 / 输入锁）
- `scripts/` — 随包脚本（图标、建工程、APK/dex 扫描、编译类进 dex、AAR 转 dex：`build_aar_dex.py` 通用版 / `build_sora_dex.py` 专用版）
- `scripts/check_portable.py` — 分享前自检：禁止外部路径、作者机器路径、**具体工程包名**（只允许宿主包 / 公开库 / 示例占位）、工作区专属 skill/agent 引用、指向不存在随包文件的引用
- `references/iapp-history.md` — 版本读数与已知会随版本变化项
- `references/iyu-whitelist.md` — iyu 只允许 call/addv
- `references/inline-java-block.md` — ⚠ 实验性存档：`java { }` 内联块（打包需 VIP，**当前不要用**，方案大概率废弃）
- `references/navigation-guide.md` — 多 `.iyu` 跳转 / 栈 / 返回（每页一个 Activity 实例、downkey 吞返回键、状态边界）
- `references/webview-bridge.md` — WebView 全前端 + mjava 桥接：URL scheme、`i.has` 回传、本地页面两形态、状态栏主题同步
- `references/iyu-guide.md` — 界面文件结构
- `references/mjava-guide.md` — 模块写法与互调
- `references/modularization-guide.md` — 多模块拆分、`i.fn`、facade 规范
- `references/events-guide.md` — 事件类型与写法
- `references/iapp-i-reference.md` — `i` 对象成员与生命周期
- `references/external-library-guide.md` — JAR/AAR/DEX 装载、编译类进 dex、Android 14+ 只读要求
- `references/network-and-mirrors.md` — 国内网络抓文档/依赖：curl 落盘、可用镜像、离线转文本
- `references/iapp-internals.md` — 内部类、APK 结构、分析脚本
- `references/delivery-guide.md` — `.iApp` 备份、APK 打包、边界
- `references/project-structure.md` — 工程结构与新建工程
- `references/emulator-setup.md` — 模拟器环境参考：多开 adb 端口冲突、雷电 9 实测工程根 `/data/media/0/iApp/ProjectApp`（仅供参考，以 iApp 设置为准）、API 34 共享目录与软链机制（**通道 2026-10-30 起停用，仅历史参考**）
- `references/environment-adaptation.md` — 环境适应：能力维度、未知宿主勘测五问、投递通道选择、版本政策、无 adb 时取证、「当…可试…」参考写法
- `references/watch-app-guide.md` — 手表应用（圆屏）：内接方框布局、轻量控件选型、手势与按压反馈、WebView 正文、页面与导航约定
- `references/status-bar-guide.md` — 状态栏决策表：默认 / 同色 / 铺满 / 隐藏 / 染色 / 图标明暗，各自最少代码与效果
- `references/ftp-delivery.md` — iApp 内置 FTP 通道：适用条件、实测特性、坑、失败签名、宿主不可达的三种办法、安全边界
- `references/icon-guide.md` — 应用图标（来源、规格、离线生成）
- `references/builtin-controls.md` — 内置短名控件清单
- `references/style-guide.md` — ppt 与 mjava 的样式分层
- `references/ui-kit.md` — mjava 建树基础库 `ui.mjava` 的函数清单、三段式骨架与已知限制（权威副本在 `assets/ui-kit/`）
- `references/md-components-guide.md` — Material 组件（ppt 声明 + TIL 修复配方 + 动态创建兜底）
- `references/material-components.md` — Material 组件选型规范与支持矩阵（优先全类名）
- `references/debugging.md` — 错误前缀与失败签名
- `references/pitfalls.md` — 踩过的坑
