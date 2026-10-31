# 状态栏与窗口姿态：按需求选配置

**适用范围**：iApp 页面（`.iyu` + mjava）的状态栏 / 内容铺满 / 系统栏显隐。
**版本前提**：未标注版本的读数 = 雷电 14 / API 34 / 1080×1920 / iApp 5.0.1013，2026-10-31。
开发模式与打包 APK 均已验 ✅；API 28 未验 ❓（版本政策：不追低版本）。

## 0. 三条底座事实

1. **iApp 的状态栏本来就是透明的**：`activity.getWindow().getStatusBarColor()` 默认 `0`。
   `FLAG_TRANSLUCENT_STATUS`（`addFlags(67108864)`）不是透明的前提。✅（API 34）
2. **状态栏那一条（72px）显示的是宿主内容容器 `a0` 的背景**，不是窗口背景，也不是系统栏自己画的：
   `a0:LinearLayout padT=72 h=1920 bg=<它自己的背景>`。✅（API 34）
3. 默认 `decor.getSystemUiVisibility() == 8464`，View 位里带着 `8192` 与 `256`；
   但 **View 位不代表实际图标色**——API 34 上改它们看不出变化，图标明暗由
   `WindowInsetsController` 管（见 2.5）。✅（API 34）

## 1. 决策表

| 需求 | 做法 | 最少代码 | 内容起点 | 状态栏那条显示 | 级别 |
|---|---|---|---|---|---|
| 什么都不做 | — | 0 行 | y=72 | a0 的背景（默认灰） | ✅ |
| 状态栏与页面同色 | 给根的直接父容器（a0）设背景色 | 1 行 | y=72 | 你设的颜色 | ✅ |
| 内容铺满整屏（状态栏浮在内容上） | 根从 a0 取出，挂到 `DecorView` | 5 行 | **y=0** | 你自己的内容 | ✅ |
| 状态栏纯色 | `w.setStatusBarColor(color)` | 1 行 | y=72 | 你设的颜色 | ✅ |
| 深色 / 浅色图标 | `WindowInsetsController.setSystemBarsAppearance(...)` | 3 行 | 不变 | 不变 | ✅ |
| 隐藏状态栏 | `WindowInsetsController.hide(statusBars())` | 3 行 | **y=0（约 400ms 内自动）** | 不存在 | ✅ |
| 隐藏 + 铺满 | 上面两条叠加 | 8 行 | y=0（与只隐藏相同） | 不存在 | ✅（挂根冗余） |

> 实测（一次性探针 · 状态栏类型矩阵，第 3、4 步）：隐藏状态栏后约 400ms，宿主把 a0 的
> `padT 72→0`，`rootY=0`、`rootH=1920`、`insetTop=0`；再挂根读数完全相同。
> 所以**隐藏状态栏不需要铺满**。边缘滑动唤出与自动隐回见 §2.4 / §4（✅ 2026-10-31）。

**同色与铺满是二选一**：根挂到 DecorView 后 a0 不再可见，再给 a0 设背景没有意义。

## 2. 最少代码

### 2.1 内容铺满整屏（状态栏浮在内容上；推荐形态：只 1 个事件）

> 注意：「铺满」= 内容从 y=0 画到屏幕底，**状态栏那 72px 也被内容覆盖**，图标浮在内容上；
> 不是「只铺状态栏以下那一块」——那是默认行为（内容从 y=72 开始）。

`.iyu` 只留根和 `loading`：

```xml
<View id="1" did="0" type="FrameLayout">
<ppt>width=-1
height=-1</ppt>
<event></event>
</View>
<UIEventset><eventItme type="loading">
call(null, "mjava", "page.fullBleed")
</eventItme></UIEventset>
```

`page.mjava`（核心 5 行）：

```java
public void fullBleed() {
	View root = activity.findViewById(1);
	FrameLayout decor = (FrameLayout) activity.getWindow().getDecorView();
	ViewGroup old = (ViewGroup) root.getParent();
	old.removeView(root);
	decor.addView(root, new FrameLayout.LayoutParams(-1, -1));
}
```

实测（2026-10-31，一次性探针 · 最小铺满，**仅 `loading` 一个事件**）：

```
[after-loading] parent=DecorView rootY=0 rootH=0      ← loading 时还没布局
[t300]   rootY=0 rootH=1920 insetTop=72 vis=8464
[t12000] rootY=0 rootH=1920 insetTop=72 vis=8464      ← 12 秒稳定
```

- `loading` 里就能挂，不需要 `loadingComplete` / `resume` / `pause`
- 挂完 300ms 内 `rootY` 变 0、`rootH` 变整屏
- **`insetTop` 仍报 72**：正文顶部安全区要自己留（见 `ui-kit.md` 的 `ui_insets` 差值公式）
- 根会同时盖住**底部导航栏**，底部安全区同样自己留

### 2.2 状态栏与页面同色（不铺满）

```java
((View) activity.findViewById(1).getParent()).setBackgroundColor(color);
```

### 2.3 状态栏纯色

```java
activity.getWindow().setStatusBarColor(color);
```

### 2.4 隐藏状态栏

```java
WindowInsetsController wic = activity.getWindow().getInsetsController();
if (wic != null) {
	wic.hide(WindowInsets.Type.statusBars());
}
```

实测：约 400ms 后宿主自动把 a0 的 `padT` 清到 0，`rootY=0`、`rootH=1920`、`insetTop=0`；
内容铺满**不需要再挂根**。恢复用 `wic.show(WindowInsets.Type.statusBars())`。

**注意是「一次性隐藏」**：顶部下滑会临时唤出状态栏，但松手后**不会自动再隐藏**
（2026-10-31 用户实测）。要「滑出后自动隐藏」，先设：

```java
wic.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
wic.hide(WindowInsets.Type.statusBars());
```

实测：这样下滑唤出后 **3~5 秒自动隐回** ✅（2026-10-31，STEP 8）。

### 2.5 状态栏图标明暗（深色背景 → 白图标；浅色背景 → 黑图标）

```java
WindowInsetsController wic = activity.getWindow().getInsetsController();
int mask = WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS;
if (wic != null) {
	wic.setSystemBarsAppearance(darkIcons ? mask : 0, mask);
}
```

- `darkIcons=true` → 深色图标（适合浅色背景）；`false` → 白色图标（适合深色背景）
- **不要用旧的 `decor.setSystemUiVisibility(8192)`**：API 34 上改 View 位观察不到图标变化
  （实测清/设 8192 前后屏幕无差异），实际明暗由 `WindowInsetsController` 管 ✅
- 视觉验收：状态栏背后要有对比色（深底看白图标、浅底看黑图标），灰底上两种都容易看错

## 3. 哪些行不需要（删掉不影响效果）

| 常见写法 | 结论 |
|---|---|
| `w.addFlags(67108864)`（`FLAG_TRANSLUCENT_STATUS`） | **不需要**：状态栏默认已透明，且它绕不过 a0 的 72px padding ✅ |
| `w.setDecorFitsSystemWindows(false)` | **不需要**：内容仍从 y=72 开始（`pitfalls.md` #32）✅ |
| 单独 `decor.setSystemUiVisibility(8192)` | **无效，不要用**：API 34 上改 View 位观察不到图标变化；改用 `WindowInsetsController.setSystemBarsAppearance` ✅ |
| `loadingComplete` / `resume` / `pause` 事件 | **铺满不需要**：1 个 `loading` 实测够 ✅；只有要读 insets 做安全区时才需要 `loadingComplete` |
| 清 a0 的 `padding` / `fitsSystemWindows` | **不需要**：挂根已经绕开它，且清了也会被重新加回（`pitfalls.md` #32）✅ |
| 隐藏状态栏时再挂根 | **不需要**：隐藏后读数与挂根完全相同（`rootY=0 rootH=1920`）✅ |

### 2.6 打包版的安全区：insets 可能拿不到，必须用系统 dimens 兜底

**这是最容易在开发期看不出来的坑**：挂根后内容从 y=0 开始，顶部安全区完全靠 `ui_insets()` 留。
开发模式下 `getRootWindowInsets()` 正常返回 72，一切正常；**打包后它可能返回 null 或全 0**，
于是 `top = max0(barsTop - rootTop) = 0`，标题、页头按钮会被状态栏直接压住（顶到 y=0）。

兜底配方（iApp 里实测可用）：

```java
public int ui_statusBarHeight() {
	int id = activity.getResources().getIdentifier("status_bar_height", "dimen", "android");
	return id > 0 ? activity.getResources().getDimensionPixelSize(id) : 0;
}

// ui_insets() 里
boolean ready = false;
WindowInsets wi = root.getRootWindowInsets();     // 可能为 null
if (wi != null) { barsTop = wi.getInsets(systemBars()).top; ready = true; }
if (!ready) {
	barsTop = ui_statusBarHeight();                // 打包版兜底
} else if (barsTop <= 0 && rootTop <= 0) {         // insets 报 0 但确实在铺满
	barsTop = ui_statusBarHeight();
}
```

要点：

- **只兜底顶部**。底部不要用 `navigation_bar_height` 兜底：手势导航下该 dimen 仍有值（约 48dp），
  而真实 inset 是 0，兜了会多出一条空白
- 兜底值不影响「不铺满」的页面：那种情况 `rootTop == 72`，`top = 72 - 72 = 0`
- 判断「是否真的铺满」看 `rootTop <= 0`，不要看 root 高度

**级别**：✅ 2026-10-31 打包复验（简阅打包版加兜底后顶部留出状态栏高度、底部正常）；
「打包版读不到 insets」这一现象为 ⚠ 用户实测语义（无 logcat）

## 4. 边界与未验

- **打包 APK（仅 rootY/rootH）** ✅ 2026-10-31 探针读数与开发模式一致；`i.syso` 不输出，无 logcat
- **打包 APK（安全区）** ✅ **加 §2.6 的 dimens 兜底后正常**（2026-10-31 打包复验：顶部留出状态栏高度、
  底部也正常）。注意：不加兜底时打包版**会**顶到状态栏下面——早先「打包后效果一致」的结论只覆盖了
  铺满本身，没有覆盖 insets 驱动的安全区
- **pause / resume 后是否保持** ✅（2026-10-31 用户回报：按 Home 再回来内容仍在状态栏后面）
- **`addv` 内嵌页** ✅ 挂根后正常：`children=2`、内嵌 `FrameLayout h=1920`、父容器为 DecorView（2026-10-31）
- **隐藏状态栏的唤出** ✅ 一次性隐藏：顶部下滑会临时唤出，但**不会自动再隐藏**；
  配 `setSystemBarsBehavior(BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE)` 后，下滑唤出 **3~5 秒自动隐回**（2026-10-31 实测）
- 开发模式下挂根改的是**页面自己的 Activity 视图树**；不要拿它去动 IDE 窗口
- 根铺满后系统栏仍在，只是内容在它后面；隐藏状态栏是另一件事（决策表第 6 行）

## 5. 与 `ui.mjava` 的关系

- `ui_insets()` 仍然需要：铺满后 `insetTop=72` 照旧，安全区靠它留
- `ui_bleed()`（translationY 方案）仍是**正文页**的兜底；打包 APK 已验证（2026-10-31），
  可考虑下一步把「挂 DecorView」收进 `ui.mjava` 作为展示页的正式入口
