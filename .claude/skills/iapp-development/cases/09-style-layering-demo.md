# 09 多层组件树与样式分层

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 页面

四层结构：`1(root) → 4 → 41 → 411 → 4111`，另有顶栏、卡片、卡片内横向行。
同一页里混放三类样式：纯 ppt、需计算的圆角/全局色（mjava）、权重与透明度对照。

## 读数

```
D1-rootChildren=6
D1-weight21=0.0 layout_weight331=1.0
D1-headerH=0 density=3.0
D1-cardPad=48
D1-t31Size=54.0 bold=true
D1-t32max=2 ellipsize=END
D1-vis5=8 vis6=4
D1-alpha42=1.0
D1-apply-ok radius=36 btnRadius=60
```

屏幕：
- 顶栏标题**消失**（`weight=1` 无效 + `width=0`）
- 卡片/按钮圆角正常（mjava `GradientDrawable`）
- 正文按 2 行省略（`maxlines` + `ellipsize` 生效）
- `alpha=0.5` 的字仍是不透明

## 结论

| 结论 | 级别 |
|---|---|
| `layout_weight` 生效，`weight` 不生效 | ✅ |
| `alpha` 不能写在 ppt，要用 mjava `setAlpha` | ✅ |
| `padding` 按 px、`textsize` 按 sp（density=3.0） | ✅ |
| `textstyle=bold`、`maxlines`、`ellipsize`、`visibility` 都生效 | ✅ |
| 载入事件里 `getHeight()` 为 0（尚未布局） | ✅ |
| 圆角/渐变只能 mjava | ✅ |

## 回填

`references/iyu-guide.md`（属性表与布局时机）、`references/style-guide.md`（实测分界表）。
