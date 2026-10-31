# Design：mjava 优先构建范式

## Context

`com.showcase.liquidglass`（G1）是唯一的现有样本：`src/mian.iyu` 150 行、`src/glass.mjava` 802 行，
mjava 里 **23 处 `findViewById`、0 次动态创建视图**——所有视图都来自 ppt 声明。
也就是说「mjava 建树」这条路在本仓库里一次都没走过，下面的决策全部建立在**未验证**之上，
因此第一批任务是探针而不是编码。

约束（详细动机见 proposal.md）：

- `.iyu` 的未知键**静默忽略**；mjava 的未知是一张 6 条的短清单
- 解释层不能具名 class → 不可能有 View 子类
- 模块级变量不跨 `call` 存活；`i.sss` 跨 `call` 但每次运行重置
- 部分错误会让**整个方法中断且 `catch` 接不住**
- iApp 打包产物 `targetSdk 36`；本机只有 API 34 模拟器，Android 15/16 无真机可测
- 宿主窗口姿态未知：`wm size` 1080×1920 而根视图高 1848，差 72px，指向「宿主已扣系统栏」，
  但未证实

## Goals / Non-Goals

**Goals**

- 让页面构建只依赖「Java + Android SDK 通用知识」，把私有格式的接触面压到一个根节点与四五个事件名
- 把系统栏/键盘/手势这些跨机型差异收在一处，页面代码不必再想
- 让一段代码在「宿主已避开系统栏」和「内容铺到屏幕边缘」两种姿态下都正确，从而不必现在就适配新系统
- 组件可跨工程复制复用，且工程保持可独立打包

**Non-Goals**

- 不改 iApp 的窗口姿态，不与宿主争窗口控制权
- 不为 Android 15/16 写任何分支或兜底（无证据）
- 不做档 C（`.iyu` 空文件 + 接管 `setContentView`）
- 不引入外部依赖、不改投递链路

## Decisions

### D1 档 B：`<View id=1 FrameLayout>` + `<UIEventset>`，其余 mjava

**选择**：`.iyu` 保留一个全屏根与四个生命周期事件，其余全部 mjava 建。

**为什么不是档 A**（保留 ppt 骨架）：问题的根源就是 ppt 的静默失效面，保留骨架等于保留问题。

**为什么不是档 C**（空 `.iyu` + `setContentView`）：事件由 `.iyu` 驱动，空文件的 `loading`
是否触发未验证；且与宿主的视图管理争使用权，风险不对等。C 留作后续可选探针。

### D2 在 `loading` 建树，尺寸取自 `DisplayMetrics`

**选择**：`loading` 里一次建完，宽高用 `getResources().getDisplayMetrics()`。

**为什么不用 `loadingComplete`**：G1 之所以等到 `loadingComplete`，是因为它要 `root.getWidth()`，
而 `loading` 里宽高为 0——为此付出了 `g.retried` 重试补丁和一次空帧。根是 `match_parent`，
屏幕尺寸本来就不需要测量。改用 `DisplayMetrics` 后，补丁和空帧一起消失。

**代价**：丢掉「骨架先出现」这个诊断信号，由 D5 补偿。

### D3 三段式根骨架：bg / safe / overlay

**选择**：组件库在 `loading` 里建出三层，页面只用后两层。

```
root (FrameLayout, 不装 insets 监听, 零 padding)
 +-- bg      全屏零 padding   背景图/渐变, 故意延伸到系统栏下
 +-- safe    padding = 上下系统栏差值      正文
 +-- overlay padding = max(系统栏差值, ime 差值)  贴底元素, 再叠加自己的间距
```

差值算法见 D8；两层都在 `loadingComplete` 与 `resume` 刷新。

**为什么不用「根上直接加 padding」**：背景必须能延伸进系统栏，正文必须避开；
两种需求并存时只能分层。

**为什么 overlay 单独一层**：贴底元素（胶囊、悬浮按钮）的高度随键盘和导航模式变，
和正文的滚动/布局无关，混在正文里每加一个就要重算一次。

### D4 视图回溯：闭包 → 注册表 → 标签，禁用 `setId`

**选择**：

| 场景 | 手段 |
|---|---|
| 点击、定时、动画收尾 | 匿名接口/Runnable 闭包直接捕获（已实测可用） |
| `resume`/`pause` 等再次进入的入口 | `i.sss` 里一个「名字 → View」注册表 |
| 复合组件对外暴露子视图 | `setTag("ui:name")` + 递归查找 |

**为什么不 `setId`**：iApp 的 id 是 ppt 命名空间的工程内小整数，`activity.findViewById`
是否等价于标准树查找未验证；一旦不是，自定义 id 会静默查不到。字符串名字无冲突面，且对 AI 可读。

**关键洞察**：全 mjava 后回溯需求大幅减少——监听器是建树时装上的，回调天然带着引用。

### D5 分段构建，靠结构而非 `catch` 兜错

**选择**：`loading` 只建骨架；其余按视觉区块拆成独立入口方法，用 `postDelayed` 串成后续帧执行，
每段进出各打一行日志。

**为什么不能靠 `try/catch`**：已实测「未加载先调用」这类错误会让整个方法中断且 `catch` 接不住；
一个 300 行的 `build()` 就是单点故障。拆段后错误的影响半径就是那一段。

**代价**：构建从一帧变成 3~4 帧（约 50ms），观感上等价于入场动画。

### D6 组件 = 工厂函数 + 命名句柄

**选择**：`ui.mjava` 提供建容器、建文本、摆位、圆角、玻璃、动效等函数；复合组件返回容器，
内部子视图用标签命名，调用方按名取。

**为什么只能这样**：解释层不能具名 class，没有 View 子类，也没有 XML inflate 式的类型复用。
这是本环境下「组件化」的天花板。

**收益**：`layout_gravity`、`padding` 按 px、`weight` 这些 ppt 语义坑一次性关进库内部，
页面层再也碰不到。

### D7 组件库权威副本在 SKILL 的 `assets/ui-kit/`，工程内 vendor 一份

**选择**：权威副本 `.claude/skills/iapp-development/assets/ui-kit/ui.mjava` 随通用知识分发，
新建工程时复制进 `project/<包名>/src/ui.mjava`，改进靠手动回灌。
放 `assets/` 而不是 `references/`：它是可直接复制进工程的源码，不是给人读的说明文档；
说明文档另写 `references/ui-kit.md`。

**为什么不用共享单副本**：工程要能脱离工作区独立打包分享；跨工程单副本会把「哪些工程能编译」
变成隐形的全局状态。

### D8 窗口：跟随宿主姿态，安全区取「insets 减根偏移」的差值

**选择**：不调 `setDecorFitsSystemWindows`、不隐藏系统栏、不改 cutout 模式；
在 `loadingComplete` 与每次 `resume` 读 `getRootWindowInsets()` 和根的屏幕位置，
把**差值**算成 safe/overlay 的 padding：

```
topPad    = max(0, insets.top    - rootTop)
bottomPad = max(0, insets.bottom - (displayH - rootTop - rootH))
```

**为什么不能直接用 insets 的值**：P5 实测宿主已经把根摆在状态栏下面
（`loc.y=72`、`h=1848`、`display=1920`），而 `getRootWindowInsets().systemBars.top` 仍是 72。
直接按值留白等于扣两遍，正文会平白下移 24 dp。差值在两种姿态下都成立：

| 宿主姿态 | rootTop / rootH | insets.top | topPad | 结果 |
|---|---|---|---|---|
| 已避开状态栏（本机） | 72 / 1848 | 72 | 0 | 铺满，不重复留白 |
| 内容铺到屏幕边缘 | 0 / 1920 | 72 | 72 | 自动避开状态栏 |

**读数时机**：`loading` 阶段 `getRootWindowInsets()` 返回 null（P5 实测），
所以结构在 `loading` 建、insets 在 `loadingComplete` 与 `resume` 应用。
本机姿态下 padding 恒为 0，首帧不会因此跳动。

**为什么这样能免掉新系统适配**：宿主扣没扣系统栏、系统是否强制全屏，
都只体现在这几个整数的差上，代码路径不变，不需要判断"现在是哪种姿态"。

**装监听器这条路已否**：`setOnApplyWindowInsetsListener(匿名实现)` 会让整份 `.mjava`
Parse error（P1 探针实测），只能主动查询。

**备选（已否）**：主动接管 edge-to-edge（`setDecorFitsSystemWindows(false)` + 自己管窗口）。
一旦接管就要对 Android 15/16 的强制行为负责，而现在测不了。

**唯一开口：展示类页面可显式接管窗口姿态**（2026-10-30 追加，用户指定）。两档，`ui.mjava` 各一个函数：

| 档 | 调用 | 效果 |
|---|---|---|
| edge-to-edge（本工程采用） | `ui_edgeToEdge(true)` → 根上移「宿主已预留的距离」+ 高度补成整屏 + 状态栏透明 | 背景铺到屏幕四边，**系统栏仍可见**，正文按 insets 差值避开状态栏 |
| 沉浸式 | `ui_immersive(true)` → `hide(systemBars)` + 滑动临时唤出 | 画面完全占满 |

选定 edge-to-edge 的过程（三次返工，全记录在 `pitfalls.md` #32 与 UIPROBE 批次）：

1. 先做 `hide(systemBars)`，用户看到「状态栏整个消失」，明确否掉——要的是**系统栏保留、内容延伸到顶边**
2. 改用 `setDecorFitsSystemWindows(false)` + 透明状态栏 → 无效；清祖先 padding 也会被宿主动态加回
3. 打日志走完 8 层祖先才看清：预留量在「根的直接父容器」的 top padding 上，每轮布局重算
4. 最终不跟它对抗：上移根 + 加高到整屏 + 关父容器 `clipToPadding`，正文留白交给差值公式

颜色不写死：库只把状态栏设成透明，图标明暗由页面用 `ui_statusBarIcons(dark)` 声明。

两条硬约束：① 只在以画面为主体的页面用；② `pause` 时必须还原——
开发模式下窗口属于 iApp 宿主，不还原会连带改掉 IDE 自己。验收以打包产物为准。

### D9 状态栏视觉由背景保证，图标深浅走 insets 控制器

**选择**：根容器自己画背景并延伸至四边；状态栏图标明暗用 `WindowInsetsController` 的外观标志。
仍调用系统栏配色接口（在 API 34 上生效），但不把它当作视觉的保证。

**为什么**：`targetSdk 36` 下新系统会忽略系统栏配色，届时唯一还在的保证就是我们自己画的背景；
图标外观接口在新系统上仍然有效。

### D10 键盘与手势

**选择**：输入类页面监听 ime inset，安全区下边距取 `max(systemBars.bottom, ime.bottom)`；
贴边控件按 `systemGestures` 安全区定位；业务手势与系统手势冲突时显式声明手势排除区域。

**为什么**：edge-to-edge 下键盘不再自动压缩布局；左右边缘是返回手势热区，2048 这类四向滑动页面会正面冲突。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 整页空白（单一 `build()` 崩掉） | D5 分段；每段独立入口 + 进出日志 |
| mjava 建树耗时不可知，可能看到闪烁 | 探针量 40 视图的构建耗时；超标则放宽分段粒度、把段并入 `loading` |
| mjava 建的视图与 ppt 声明的视图测量结果不同（字重、`maxlines`、`wrap_content`） | 探针 P4 对照同一组属性；有差异则在库里统一补偿 |
| `i.sss` 不能存 View 引用 | 降级为标签查找（D4 第三档），并在证据里记一笔 |
| 宿主对 mjava 建的视图有特殊处理（层级、刷新） | 探针 P1/P2 先确认，再写库 |
| 组件库跨工程漂移 | 权威副本单一来源 + 新工程复制时带版本行；回灌是显式动作 |
| 项目不能被人工维护 | 已接受；以「页面代码读起来像装配句子」降低阅读成本 |
| Android 15/16 行为未验 | 只记待验项；D8/D9 的写法使漂移只体现为数值变化 |

## Migration Plan

1. 探针工程跑 P1–P7（见 tasks.md），把结论写进 `docs/evidence.md`
2. 用探针结论定 `ui.mjava` 最小集，只做 G1 重写要用的函数
3. G1 按 D1–D10 重写：`.iyu` 砍到根 + 事件表，`glass.mjava` 拆成「骨架段 / 内容段 / 效果段」，
   新增 `ui.mjava`
4. 重写过程中重复三次以上的东西抽回 `ui.mjava`
5. 文档三层按实测改写（清单见 proposal.md Impact）
6. 回滚：G1 在 `project/` 自己的仓库里，按 commit 回退；本轮之前的 `7054e2a` 是可运行版本

## Open Questions

- 横屏是否在 G1 重写范围内？当前 G1 只做竖屏；横屏的 insets（左右 cutout）等 2048 之后再做
- 2048（change 2）要用到的手势判定是否需要库内封装，等 change 2 的探索再定
