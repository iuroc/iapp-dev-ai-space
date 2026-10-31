# ui-kit：mjava 建树基础库

iApp 的界面默认由 mjava 在 `loading` 里建，不用 ppt 声明子控件。
本库把这些重复劳动收成函数，并把几个 ppt 语义坑（`layout_gravity` 不生效、`padding` 按 px、
`weight` 无效）关在库内部，页面代码只写"装配句子"。

**权威副本**：`assets/ui-kit/ui.mjava`（随本技能分发，是可直接复制进工程的源码，不是说明文档）。
工程内 vendor 一份到 `project/<包名>/src/ui.mjava`，改进先在一个工程里验证、再手动回灌权威副本；
不回灌的话新工程继续用旧版。

**版本**：v0.1（2026-10-30）。每个副本文件头都有版本行，回灌前先核对。

> 实测依据：2026-10-30 的探针批次 UIPROBE-1 / UIPROBE-2
> （原始读数留在工作区证据档，不随 skill 分发）。其中 UIPROBE-2 是本库自身的自检批次，
> 标 ✅ 的条目都是真机跑出来的。

## 快速上手

`.iyu` 只留一个根容器和全局事件表：

```
<View id="1" did="0" type="FrameLayout">
<ppt>width=-1
height=-1
backgroundcolor=#0B1016</ppt>
<event></event>
</View>
<UIEventset><eventItme type="loading">
call(null, "mjava", "page.first")
</eventItme><eventItme type="loadingComplete">
call(null, "mjava", "page.second")
</eventItme><eventItme type="resume">
call(null, "mjava", "page.again")
</eventItme></UIEventset>
```

页面模块：

```java
public void first() {
	i.fn("ui");
	ui_init(activity.findViewById(1));      // 建 bg / safe / overlay
	View safe = ui_layer("safe");
	LinearLayout col = ui_col();
	col.setPadding(ui_dp(20), ui_dp(28), ui_dp(20), ui_dp(20));
	ui_add((ViewGroup) safe, col, -1, -1);
	ui_add(col, ui_text("标题", 20, "#FFFFFF"), -1, -2);
}

public void second() {
	i.fn("ui");
	ui_insets();                             // 安全区只能在这之后读
}

public void again() {
	i.fn("ui");
	ui_insets();                             // 重新进入时刷新
}
```

**每个入口都要先 `i.fn("ui")`**：每次 `call` 都是新解释器，加载不继承。

## 三段式根骨架

```
root  FrameLayout · 零 padding · 我们不装 insets 监听
 +-- bg       全屏 · 背景图/渐变 · 故意延伸到系统栏下
 +-- safe     padding = 系统栏差值 · 正文
 +-- overlay  padding = max(系统栏差值, ime 差值) · 贴底元素
```

背景要能进系统栏、正文要避开、贴底元素要跟着键盘走，三种需求并存只能分层。
`ui_init` 会先 `removeAllViews()` 再建——**这个根归我们**，不要往里手塞视图。

安全区一律走 `ui_insets()`，它算的是差值而不是 insets 本身：

```
topPad    = max(0, insets.top    - rootTop)
bottomPad = max(0, insets.bottom - (displayH - rootTop - rootH))
```

宿主已经避开状态栏时 `rootTop` 等于状态栏高度，差值自然为 0；宿主让内容铺到屏幕边缘时
`rootTop` 为 0，差值就是 insets，自动留白。同一份代码两种姿态都对，**不要**把 insets 直接当 padding。

**打包版例外（v0.2 起已内置兜底）**：打包 APK 里 `getRootWindowInsets()` 可能返回 null 或全 0，
差值为 0 会让标题顶到状态栏下面。现在 `ui_insets()` 在「拿不到 insets」或「insets.top=0 且
`rootTop<=0`」时回落到 `ui_statusBarHeight()`（读 `android:dimen/status_bar_height`）。
只兜底顶部：底部的 `navigation_bar_height` 在手势导航下仍有值，兜了会多出一条空白。
详见 `status-bar-guide.md` §2.6。

## 函数清单

### 基础

| 函数 | 说明 |
|---|---|
| `ui_dp(int)` / `ui_dpf(float)` / `ui_density()` | dp → px（整数 / 浮点） |
| `ui_screenW()` / `ui_screenH()` | 取 `DisplayMetrics`；`loading` 里也只能用这个，视图宽高还是 0 |
| `ui_color(String)` | `#RRGGBB` / `#AARRGGBB`；解析失败退回白色 |
| `ui_textSize(TextView, int)` | 按 sp 设置字号 |
| `ui_log(String)` | `i.syso("UI " + s)` |

### 骨架与句柄

| 函数 | 说明 |
|---|---|
| `ui_init(View)` | 建 bg/safe/overlay 三层并注册；会清空根 |
| `ui_root()` | `activity.findViewById(1)` |
| `ui_layer(String)` | 按名取回 `bg` / `safe` / `overlay` |
| `ui_reg(String, Object)` / `ui_get(String)` | 运行期注册表（落在 `i.sss`，跨 call 存活、每次运行重置；**切页不清表**，句柄必须按页面重注册，见 pitfalls #42） |
| `ui_tag(View, String)` / `ui_find(View, String)` | 视图标签与递归查找，用于复合组件对外暴露子视图 |

### 控件

| 函数 | 说明 |
|---|---|
| `ui_frame()` / `ui_col()` / `ui_row()` | 容器 |
| `ui_text(String, int sp, String color)` | 文本 |
| `ui_image()` | 图像 |

### 摆位（绕开 ppt 的 `layout_gravity` 坑）

| 函数 | 说明 |
|---|---|
| `ui_add(parent, child, w, h)` | 按父容器类型自动选 `LayoutParams`；FrameLayout 下默认贴左上 |
| `ui_addTop(LinearLayout, child, w, h, topDp)` | 垂直列表里加一个带顶距的子视图（最常用的一条） |
| `ui_addWeight(parent, child, w, h, weight)` | 线性布局按权重分配；父容器不是线性布局时退回 `ui_add` |
| `ui_fplace(parent, child, w, h, gravity)` | FrameLayout 专用，`Gravity.BOTTOM \| Gravity.CENTER_HORIZONTAL` 这类才生效 |
| `ui_margins(v, l, t, r, b)` | 单位 dp，加在已有的 `LayoutParams` 上；已用 `ui_addTop` 时一般不需要 |
| `ui_weight(v, float)` | 改已有子视图的权重（`ui_addWeight` 在添加时就设好了） |

尺寸用 `-1`（match_parent）/ `-2`（wrap_content），与原生一致。

### 外观

| 函数 | 说明 |
|---|---|
| `ui_round(radiusDp, fillHex)` | 圆角填充 |
| `ui_stroke(radiusDp, fillHex, strokeDp, strokeHex)` | 圆角 + 描边 |
| `ui_gradient(v, radiusDp, fromHex, toHex, vertical)` | 渐变背景 |
| `ui_glass(v, radiusDp, fillAlpha%, strokeAlpha%)` | 玻璃表层（白填充 + 白描边） |

`ui_glass` 只做表层。真正的模糊/折射（例如裁背景位图缩小再放大）由调用方自己画，库不做。

### 安全区与分段

| 函数 | 说明 |
|---|---|
| `ui_insets()` | 在 `loadingComplete` 与每次 `resume` 调；算差值并设 safe/overlay 的 padding；打包版 insets 缺失时用 `ui_statusBarHeight()` 兜底 |
| `ui_statusBarHeight()` / `ui_dimen(String)` | 读 `android:dimen/*` 的像素值；打包版安全区兜底用 |
| `ui_edgeToEdge(boolean)` | 展示类页面开/关 edge-to-edge（背景铺到屏幕四边，系统栏仍可见）；**必须在 `pause` 关掉** |
| `ui_bleed(boolean)` | 让根覆盖整屏：上移宿主已预留的距离并加高到屏幕高（`ui_edgeToEdge` 内部已调，一般不用单独用） |
| `ui_statusBarIcons(boolean)` | 状态栏图标明暗：背景深传 `false`（浅色图标），背景浅传 `true` |
| `ui_immersive(boolean)` | 更进一步：隐藏系统栏 + 边缘滑动临时唤出；同样必须 `pause` 关掉 |
| `ui_later(name, delayMs, Runnable)` | 分段调度：进出一行日志、段内异常只毁该段 |
| `ui_max(a,b)` / `ui_max0(v)` | 小工具 |

### 包信息

| 函数 | 说明 |
|---|---|
| `ui_versionText()` | 运行时读包自身的 `versionName`（打包态 = 工程的 `<versionName>`）；开发态包名是宿主 `com.iapp.app`，读到的是 IDE 版本，此时返回「开发版」。见 `pitfalls.md` #47 |

**窗口姿态**：只给以画面为主体的展示页（看图、播放器、游戏）用，别给正文页用。

`ui_edgeToEdge(true)` 的效果是「**系统栏仍然可见，背景铺到屏幕四边**」，正文仍按 insets 差值
避开状态栏。它不含任何颜色常量——状态栏设成透明，图标明暗由页面用 `ui_statusBarIcons` 自己声明。

它为什么不能靠直接改 Window 实现（2026-10-30 实测，三代写法全部失败）：

| 写法 | 结果 |
|---|---|
| `setDecorFitsSystemWindows(false)` + 状态栏透明 | 无效，内容仍从状态栏下开始 |
| 再清祖先容器的 `padding` / `fitsSystemWindows` | 清掉后被宿主下一轮布局重新加回 |
| 延迟到布局完成后清 + 不主动 `requestApplyInsets` | 仍然被重新加回 |

打日志把根往上走了 8 层才看清：**预留量在「我们根的直接父容器」的 top padding 上**
（实测 `LinearLayout[pad 0,72,0,0]`），而且每轮布局都会重算。

所以库里的做法是**不去对抗**：读到根被顶下去多少，就把根 `translationY` 上移同样距离、
高度补成屏幕高，父容器的 `clipToPadding` 关掉（否则上移出去那截会被裁）。
根顶回到 0 之后，`ui_insets` 的差值公式自动算出 `topPad = 状态栏高`，正文仍在状态栏下方。

**补充（2026-10-31，STATBAR-1~3，API 34）**：

- iApp 开发模式下 `getStatusBarColor()` 默认就是 `0`（透明）；状态栏区域显示的是**宿主内容容器 a0 的背景**，
  不是窗口背景。想让状态栏与页面同色，直接给根的直接父容器（a0）设背景色；`FLAG_TRANSLUCENT_STATUS`
  不是透明的前提，也不会让内容绕过 a0 的 top padding
- 想让内容**真的铺进状态栏**：把根从 a0 取出、挂到 `DecorView`（`FrameLayout.LayoutParams(-1,-1)`），
  实测 `rootY 72→0`、`rootH 1848→1920`，事件与 `findViewById` 不受影响。
  ✅ 打包 APK、`pause` 后保持、`addv` 内嵌页均已验（2026-10-31）；根会同时盖住底部导航栏，正文要自己按 insets 留安全区。
  详见 `pitfalls.md` #40
- 按需求选方案的完整决策表与最少代码：`status-bar-guide.md`

两条硬约束：① `pause` 里必须 `ui_edgeToEdge(false)` 还原（开发模式下窗口是 iApp 宿主自己的，
不还原会连带改掉 IDE）；② 验收以打包产物为准。

**分段怎么写**：

```java
ui_later("content", 0,   new Runnable() { public void run() { buildContent(); } });
ui_later("effect",  60,  new Runnable() { public void run() { buildEffect(); } });
```

每段是独立的 `Runnable`，由 `postDelayed` 单独进入。这保证一段出错时后面的段照常执行——
BeanShell 的部分错误会让整个方法中断且 `catch` 接不住，**分段靠的是结构而不是异常处理**。

## 已知限制（都实测过，别绕回去）

| 限制 | 依据 |
|---|---|
| 不能装 `setOnApplyWindowInsetsListener(匿名实现)`，会让整份 `.mjava` Parse error | UIPROBE-1 R1；只能像 `ui_insets()` 这样主动查询 |
| `loading` 阶段 `getRootWindowInsets()` 返回 null，视图宽高为 0 | UIPROBE-1 P5 |
| 不能继承 View，没有 View 子类；复合组件只能是"工厂函数 + 命名句柄" | BeanShell 不支持具名 class |
| iApp「数据调试工具」面板打开时，`i.syso` 只进面板、`adb logcat` 抓不到（面板未开时能抓到 `ygs`） | UIPROBE-1 R2；取证要么让用户贴控制台，要么先关面板 |
| `i.sss` 仅在**重新运行**时重置，切换 `.iyu` 页面**不清表** | 每个页面都要重新 `ui_reg` 自己的句柄，跨页复用旧 View 会崩 `child already has a parent`（pitfalls #42） |
| `i.sss` 直接存 View，跨 `call` 取回可能是 null；包一层 `HashMap<String,View>` 后可取回同一实例（`identityHashCode` 一致） | ⚠ 单次现象，待复验；稳定可用的是 `setTag(int, View)`。怎么验：同一模块里直存 View 与存 HashMap 各取一次，比较是否为 null |
| 两类失败要分开处理：调**不存在的 `i` 方法**抛 `UndeclaredThrowableException`，**可以**被 `catch(Throwable)` 接住；调**未加载或签名不符的模块方法**报 `Command not found`，整个方法中断、**接不住** | UIPROBE-2 K7；`pitfalls.md` #34。写 `catch(Throwable)` 时不要以为能兜住全部 |
| 本库不做横屏（左右 cutout）适配 | 未实测 |
| 图片不要走 `getIdentifier`：工程 `res/` 不参与资源编译，`getIdentifier(...,"drawable",...)` 恒为 0，失败静默给空图 | `res/` 图片用 `i.us(v,"src"/"background","@名称")`，开发模式与打包产物都成立 ✅ 2026-10-30；配方见 `recipes.md` §工程 res/ 图片。本行原「图片没有一条通吃路径 ⚠ 推断」已被该实测推翻 |

## 相关

- 为什么默认 mjava 建树、`.iyu` 只留根：`references/style-guide.md`
- ppt 的静默失效项清单：`references/pitfalls.md`
- 组件库怎么回灌与分发：`references/project-structure.md`
