# UI 辅助技能怎么配合 iApp 用

本工作区装了两个 UI 技能：`mobile-app-ui-design`、`material-3`。它们面向「原生 Android /
React / Flutter」的世界，而 iApp 只有 **Android View + ppt 声明 + BeanShell(mjava)**。
结论先放这里：**设计层可以直接用，实现层几乎都要换写法**。

## 什么时候用哪个

| 场景 | 用哪个 | 说明 |
|---|---|---|
| 设计新页面、改造观感、定信息架构、写空状态/引导流 | `mobile-app-ui-design` | 设计流程与反模式是媒介无关的 |
| 落实 Material 3 的配色、字号阶梯、圆角、组件规格、可访问性 | `material-3` | 取它的 token 与组件语义，不取代码 |
| 写 `.iyu` / `.mjava`、控件登记、投递调试、打包 | `iapp-development` | 这两个 UI 技能**不能**替代它 |

两者同时能用时：`material-3` 负责「设计系统长什么样」，`mobile-app-ui-design` 负责「这个页面为什么这样排」。

## 能用 / 不能用

### mobile-app-ui-design

| 部分 | 对 iApp |
|---|---|
| 设计流程（语境 → 结构 → 视觉 → 情绪 → 细节）、拇指区、F 型阅读、空状态、反模式、行业惯例 | ✅ 直接用 |
| Implementation Notes（Tailwind、Lucide、Recharts、`backdrop-blur`、375px 基线） | ❌ 不适用，是 Web/React 的实现 |
| 参考文件 `.claude/skills/mobile-app-ui-design/references/industry-conventions.md` | ✅ 可直接读，按行业取约定 |

替代：375px 基线换成常见安卓宽度（360dp 宽、400dp 高以上）；图标用 Canvas 现画（见
`.claude/skills/iapp-development/references/icon-guide.md`），不引图标库。

### material-3

| 部分 | 对 iApp |
|---|---|
| 颜色角色（`primary` / `surface` / `outline` …）、type scale、shape token、elevation 语义 | ✅ 当作设计规格用 |
| 组件清单、状态、可访问性、MD3 审计清单 | ✅ 用来验收 |
| Jetpack Compose / Flutter / `@material/web` 的代码与 API | ❌ 不能照抄 |
| M3 Expressive（Compose 专属的形变、spring 物理） | ❌ iApp 没有 Compose |
| Dynamic color（`DynamicColors`） | ❓ 未在 iApp 验过；按静态色板设计更稳 |
| Spring-based motion | ⚠ 用 `ObjectAnimator` / `View.animate()` 近似（见 `animation-guide.md`） |

## M3 概念 → iApp 写法

| M3 概念 | 在 iApp 里怎么写 | 备注 |
|---|---|---|
| 颜色角色 | ppt `backgroundcolor` / `textcolor`；或 mjava 常量模块集中管理 | **颜色写 ppt 画布才看得到**；全放 mjava 会导致预览与真机不一致 |
| Type scale | ppt `textsize` / `textstyle` / `maxlines` / `ellipsize` | 字号单位按 sp 用；`padding` 例外，ppt 按 **px** |
| Shape（圆角） | `MaterialCardView` 的 `cornerRadius`；或 mjava `GradientDrawable` + `setClipToOutline` | 渐变/描边/Ripple 只能在 mjava |
| Elevation | ppt `elevation`；或 `MaterialCardView` 自带 | 用 tonal surface 替代阴影时，直接给容器色 |
| 组件 | ppt `type=` 写**完整类名** `com.google.android.material.*` + `build.xml` 登记 | 短名可能指向 iApp 封装或 androidx，见 `material-components.md` |
| Bottom navigation | `com.google.android.material.bottomnavigation.BottomNavigationView` + 多页 `uigo` | 页面切换语义见 `navigation-guide.md` |
| Icons | Canvas + Path 现画成 Bitmap | 不用 emoji/文字符号 |
| 动效 | `ObjectAnimator` / `View.animate()` / `postDelayed` | 没有 Compose 的 spring |

## 已知限制（会直接拉低还原度）

1. **没有 Compose**：iApp 只有 Android View + Material 1.13 的类。M3 的 Expressive 特性基本落不了地。
2. **`SearchBar` 不能 ppt 声明**：设计器保存/序列化时会崩，只能 mjava 动态创建且不登记。
3. **`TextInputLayout` 要修**：ppt 声明的 TIL 默认不画盒子，需按 `md-components-guide.md` 的 `loading` 配方修复。
4. **`padding` 按 px**：M3 的 8dp 间距系统要自己换算。
5. **画布不执行 mjava**：颜色/字号若全放 mjava，设计器预览与真机不一致；静态样式尽量写 ppt。
6. **动态取色未验**：不要默认「跟随壁纸」可用；按 seed 色静态生成一套色板更稳。

## 推荐工作流

1. 用 `mobile-app-ui-design` 过一遍信息架构与页面结构，产出文字结论（不要产出 React/Tailwind 代码）。
2. 用 `material-3` 取一套规格：色板（hex）、字号阶梯、间距、圆角、组件清单与状态。
3. 用 `iapp-development` 落成 `.iyu`：静态样式写 ppt、完整类名登记 `build.xml`、运行期内容进 mjava。
4. 真机截图与设计规格逐项对照；差异（尤其圆角、阴影、字号）写进 `docs/evidence.md`，再决定是否值得用 mjava 修。

## 不要做

- 不要把 Compose / Flutter / `@material/web` 的代码贴进 mjava（BeanShell 跑不了 Compose）。
- 不要让 UI 技能决定工程结构、投递通道或打包方式——那是 `iapp-development` 与本工作区 `CLAUDE.md` 的职责。
- 不要为一个页面引入 Web 依赖或图标库；iApp 的图标/矢量一律现画或图片资源。
