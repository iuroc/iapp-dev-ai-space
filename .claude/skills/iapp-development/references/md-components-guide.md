# Material 组件（MD3）

版本前提：iApp 5.0.1013、API 28，SDK 内含 material 1.13.0。

## 结论：用 mjava 动态创建，不要在 ppt 里直接写自定义类

ppt 里写 `type="com.google.android.material.button.MaterialButton"` 这类完整类名，运行时会渲染，但存在两个坑：

1. **影子实例**：`findViewById` 拿到的是脱离窗口的实例，`addView` / `setPadding` 全部无效（实测 `children` 恒为 0、`pad` 恒为 0，`isAttachedToWindow()` 为 false）
2. **设计器“未知”**：必须在 `build.xml` 的 `<newControl>` 里登记，否则组件树显示未知（登记格式见 `project-structure.md`）

正确做法：ppt 只放普通 `LinearLayout` 占位，组件在 mjava 里 `new` 出来再 `addView`。

## 输入框（TextInputLayout）正确写法

```java
TextInputLayout til = new TextInputLayout(activity);
til.setHint("MD3 输入框");
til.setBoxBackgroundMode(TextInputLayout.BOX_BACKGROUND_OUTLINE);
TextInputEditText et = new TextInputEditText(til.getContext());   // 关键：用 layout 的 Context
et.setSingleLine(true);
til.addView(et, new LinearLayout.LayoutParams(MATCH_PARENT, WRAP_CONTENT));
```

实测：`D2f-theme=none`（资源名解析不到 M3 主题，`materialContext()` 回退到 activity），但上面这段仍拿到 `boxBackgroundMode=2`、布局后高度 183，界面为描边框。

归因（✅ A/B/C/D 矩阵 + Context 类名日志）：

| 组 | 子控件构造 | 子控件 `ctxCls` | 外观 |
|---|---|---|---|
| A | `new TextInputEditText(activity)`，不单行 | `com.iapp.app.run.mian` | 原生下划线 |
| B | `new TextInputEditText(activity)`，单行 | 同上 | 原生下划线 |
| C | `new TextInputEditText(til.getContext())`，不单行 | `androidx.appcompat.view.ContextThemeWrapper` | outline |
| D | `new TextInputEditText(til.getContext())`，单行 | 同上 | outline |

- 所有 `TextInputLayout.getContext()` 都返回 `ContextThemeWrapper`：构造时被包了一层 Material 主题覆盖
- 子控件用 `activity` 构造会**绕过**这层覆盖，按 AppCompat 主题自绘背景
- A 与 B 外观一致 → `setSingleLine` 不是因素
- 结论：**决定外观的是子控件拿到的 Context**

各模式回读：`110 mode=2`（outline）、`111 mode=1`（filled）、`112 mode=0`（none）、`113/114 mode=2`。

要点：

- `TextInputEditText` 必须是 `TextInputLayout` 的**直接子控件**；用 ppt 的 `did` 挂会多一层 `FrameLayout`，浮标和 hint 会重叠
- 子控件一定要用 `til.getContext()` 构造（即使 layout 用的是 activity）
- `setSingleLine(true)`
- `setBoxBackgroundMode(BOX_BACKGROUND_OUTLINE)` 才能得到描边框；默认是 filled 下划线
- 若能把主题 id 解析出来，用 `ContextThemeWrapper(activity, themeId)` 构造 layout 更稳；本机资源名下解析不到（`getIdentifier("Theme_Material3_*","style",pkg)` 返回 0）

## TextInputLayout 常用参数（✅ 实测可设可读）

| 参数 | 调用 | 说明 |
|---|---|---|
| box 模式 | `setBoxBackgroundMode(...)` | `OUTLINE=2`、`FILLED=1`、`NONE=0`，`getBoxBackgroundMode()` 可回读 |
| 提示 | `setHint(...)` | 浮标文本 |
| 辅助文字 | `setHelperText(...)` | — |
| 错误 | `setErrorEnabled(true)` + `setError(...)` | — |
| 字数 | `setCounterEnabled(true)` + `setCounterMaxLength(n)` | — |
| 前后缀 | `setPrefixText("https://")` / `setSuffixText(".com")` | 配合 `BOX_BACKGROUND_NONE` 可用 |
| 描边 | `setBoxStrokeColor(color)` / `setBoxStrokeWidth(dp)` | 需 OUTLINE |
| 圆角 | `setBoxCornerRadii(l,t,r,b)` | 需 OUTLINE |
| 密码显隐 | `setEndIconMode(TextInputLayout.END_ICON_PASSWORD_TOGGLE)` | 子控件 `setInputType(TEXT_PASSWORD)` |

## 其它组件（全部动态创建成功）

| 组件 | 类 | 备注 |
|---|---|---|
| 按钮 | `com.google.android.material.button.MaterialButton` | 圆角胶囊；可用 `setCornerRadius` / `setBackgroundTintList` / `setStrokeWidth`+`setStrokeColor` 逼近 filled/tonal/outlined/text |
| 卡片 | `com.google.android.material.card.MaterialCardView` | 默认无内容内边距，需 `setContentPadding` |
| 标签 | `com.google.android.material.chip.Chip` | `setText` 后要 `setClickable(true)`；`setCheckable(true)` 做 filter/choice |
| 开关 | `com.google.android.material.switchmaterial.SwitchMaterial` | — |
| 复选框 | `com.google.android.material.checkbox.MaterialCheckBox` | — |
| 单选框 | `com.google.android.material.radiobutton.MaterialRadioButton` | — |
| 滑块 | `com.google.android.material.slider.Slider` | `setValueFrom/To/Value` |
| 圆形进度 | `com.google.android.material.progressindicator.CircularProgressIndicator` | `setIndeterminate(true)` |
| 线性进度 | `com.google.android.material.progressindicator.LinearProgressIndicator` | `setIndeterminate(true)` |
| 悬浮按钮 | `com.google.android.material.floatingactionbutton.FloatingActionButton` | 无图标时显示为空色块 |

## 主题现状（实测）

- `accent=#ff4081`（AppCompat 粉）、`primary=#6750a4`（M3 基线紫）→ 混合主题
- `com.google.android.material.R$style` / `R$attr` 类被裁，反射枚举 M3 主题不可行
- `getIdentifier("Theme_Material3_DayNight","style",pkg)` 返回 0（资源名不在应用包下）；`ContextThemeWrapper` 方案在本机不可用，回退到 activity 仍可得到 outline

## 时序

- 载入事件里子控件 `isAttachedToWindow()` 仍为 false（尚未 attach），不是失败
