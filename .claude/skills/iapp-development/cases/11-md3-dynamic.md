# 11 Material 组件（MD3）

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 过程与读数

1. ppt 直接写完整类名：组件能渲染，但 `findViewById` 是影子实例
   - `203 children=0`、`card pad=0`，`addView`/`setPadding` 立即读也无变化
   - 同一 Activity（`act=191800877`），内置控件（99 号 TextView）改动正常
2. 设计器组件树显示“未知” → 在 `build.xml` 登记：
   `<newControl><itme title="…" class="…" info="…"/></newControl>`
3. ppt 用 `did` 嵌套 `TextInputEditText` 到 `TextInputLayout`：多一层 `FrameLayout`，浮标与 hint 重叠
4. 改为 **ppt 只放 LinearLayout 占位 + mjava 动态创建**：

```
D2d | 201 children=1 -> MaterialButton attached=false
    | 202 children=1 -> MaterialCardView inner=1
    | 203 children=1 -> TextInputLayout inner=1
    | 204 children=1 -> TextInputLayout inner=1
    | 205 Chip | 206 SwitchMaterial | 207 FloatingActionButton
D2f-theme=none
D2e-mode=2
D2e-post mode=2 h=183
```

5. 输入框最终写法：`new TextInputLayout(activity)`、`setBoxBackgroundMode(BOX_BACKGROUND_OUTLINE)`、`new TextInputEditText(til.getContext())`、`setSingleLine(true)`、`addView`

## 归因说明

- **有硬证据**：`did` 嵌套组合控件会产生 `FrameLayout` 包裹；ppt 直接创建的自定义类，mjava `addView`/`setPadding` 后立即读仍为 0
- **未完全隔离**：outline 不生效的直接原因。早期动态版本也设了 `BOX_BACKGROUND_OUTLINE`，但没回读 mode；最终生效版本改用 `til.getContext()` + `setSingleLine` 并读到 `mode=2`。两者是强相关，尚未做单变量对照

## 结论

- 自定义类控件在 ppt 里是影子实例，必须 mjava 动态创建
- `build.xml` 的 `<newControl>` 只影响设计器；登记子项标签是 `itme`
- 组合控件必须保持真实父子关系，不能靠 `did`
- 描边框由 `BOX_BACKGROUND_OUTLINE` 得到；本机解析不到 M3 主题 id，但 outline 仍生效
- 载入事件阶段 `isAttachedToWindow()` 为 false 属正常
