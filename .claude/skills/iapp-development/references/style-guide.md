# 骨架与样式分层：`.iyu` 只放根，其余全在 mjava

核心判据：**`.iyu` 只承担「根容器 + 全局事件表」；视图、样式、间距一律在 mjava 里写。**

这条判据来自 2026-10-30 的范式翻转，理由与实测见 `SKILL.md` §界面构建 与
实测批次 UIPROBE-1（mjava 建的视图与 ppt 声明在测量上完全一致，API 34 / 1080×1920）。

## 两层各管什么

| 层 | 写什么 | 不写什么 |
|---|---|---|
| `.iyu` | 一个全屏根 `FrameLayout`（`id=1`，`width=-1 height=-1 backgroundcolor=…`）；`<UIEventset>` 的四个事件 | 子控件、静态样式键、每控件的 `<event>` 块 |
| mjava | 其余一切：建视图、设样式、摆位、装监听器、画 drawable | — |

`.iyu` 里那三个 ppt 键只决定「根铺多大、第一帧什么底色」；连根自己的样式想改也可以放到 mjava 里。

## 尺寸与单位

- mjava 的 setter 一律收 **px**。用 `ui_dp(int)` / `ui_dpf(float)`（`ui.mjava`）换算，
  不要自己乘 density，也别把 dp 数直接喂给 setter
- 屏幕尺寸取 `DisplayMetrics`（`ui_screenW()` / `ui_screenH()`），**不要**在 `loading` 里读视图宽高——
  那一刻还是 0（实测）
- 字号用 `ui_textSize(v, sp)`，内部走 `COMPLEX_UNIT_SP`

## 外观

| 需要 | 做法 |
|---|---|
| 圆角填充 | `ui_round(radiusDp, fillHex)` |
| 圆角 + 描边 | `ui_stroke(radiusDp, fillHex, strokeDp, strokeHex)` |
| 渐变 | `ui_gradient(v, radiusDp, fromHex, toHex, vertical)` |
| 玻璃表层 | `ui_glass(v, radiusDp, fillAlpha%, strokeAlpha%)`（模糊/折射自己画，库不做） |
| 透明度 | `view.setAlpha(0.5f)` |

复杂外观（卡面、噪点、渐变光斑）用 `Bitmap + Canvas + Paint` 现画再 `setImageBitmap`，
不要引入图标库或 emoji。

## 波纹（Ripple）

`RippleDrawable` 只能由 mjava 构造；**宿主控件 `setClickable(true)` 才会响应**。

```java
ColorStateList ripple = ColorStateList.valueOf(Color.parseColor("#66FFFFFF"));
GradientDrawable bg = new GradientDrawable();
bg.setColor(Color.parseColor("#2196F3"));
bg.setCornerRadius(ui_dp(24));
view.setBackground(new RippleDrawable(ripple, bg, null));
```

第三个参数是**遮罩**：行内水波纹要给一个不透明圆角矩形遮罩，否则涟漪会按无边界圆扩散成整圆。

❓ **「整块背景已是圆角时传 `null` 是否安全」尚未定案**：本库早期记录称可传 `null`、由内容 drawable
约束涟漪；`pitfalls.md` #35 的实测则是 `null` 时涟漪不受控件边界裁剪、会扩散成整圆（圆角处溢出）。
怎么验：同一个圆角背景控件分别用 `null` 与圆角矩形遮罩各画一次，在圆角外侧截图比对有没有涟漪溢出。
**定案前一律传与背景同形状的遮罩**，上例代码里的 `null` 只作占位。

| 组合 | 现象 |
|---|---|
| RippleDrawable + 未 `setClickable(true)` | 无波纹 |
| RippleDrawable + `setClickable(true)`（TextView / LinearLayout / Button） | 正常波纹 |
| Button + 自定义 background | 覆盖原生背景，原生波纹丢失 |

## Material 复合控件

mjava 里直接 `new`，**子控件的 Context 默认就是对的**，
所以 `md-components-guide.md` 里那条「从 `loading` 抄 `TextInputEditText` 字号 + `setBackground(null)`」
的修复配方只在「ppt 声明」这条历史路径下才需要，mjava 建树时不用做。

- 主题：`new` Material 控件要宿主主题带对应 attr，拿不准就用 `til.getContext()` 这类控件自己的 Context
- `SearchBar` 只能 mjava 建（ppt 路径会让设计器序列化崩溃，见 `pitfalls.md` #7）
- 选型与支持矩阵见 `material-components.md`

## MD 风格输入框

`EditText` + `GradientDrawable`（圆角 + 描边），焦点态换描边色：

```java
input.setOnFocusChangeListener(new View.OnFocusChangeListener() {
    public void onFocusChange(View v, boolean focused) {
        // 重建 GradientDrawable，描边色 #3F51B5 / #CCCCCC
    }
});
```

实测：聚焦后边框变蓝；`setPadding` 用 dp 换算。

## 档 A 历史：ppt 的四个语义坑

只有**例外路径**（历史工程的 ppt 骨架、静态探针页）才会遇到：`layout_gravity` / `alpha` 静默失效，
`weight` 要写成 `layout_weight`，`padding` 按 **px** 解释。共同点是**没有报错，只是没效果**——
这正是当初把默认写法翻到 mjava 的原因。mjava 里对应的做法见 `ui-kit.md`（摆位、`ui_dp`）。

逐键实测读数见 `iyu-guide.md` §普通属性。`layout_gravity` 在 2026-10-29 打包版 / API 30
与 2026-10-30 API 34 开发模式各复现过一次，不是特定版本问题。

## 其他历史写法

- **`st_` 桥**：ppt 里直接调 Java setter（`st_setTextColor=16711680`），只认整数、无单位后缀。
  新代码不要用这种第三种写法
- **组件 `.iyu` 复用**：结构重复 5 次以上时曾经抽成组件 `.iyu`；现在改为抽成
  `ui.mjava` 里的工厂函数 + `ui_tag` / `ui_find` 命名句柄（见 `ui-kit.md`）
