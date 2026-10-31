# 提案：iApp 界面的 mjava 优先构建范式

## Why

`.iyu`/`ppt` 是 iApp 私有的声明式格式，未知键**静默忽略**（已踩 `alpha`、`weight`、`layout_gravity` 三个），
而 mjava 的边界是一张可枚举的短清单（不能 `final`、不能具名 class、不能可变参数……）。
未知面的性质是「无界、逐项靠真机试」对「有界、遇到一次就记住」——继续以 ppt 为主写法，
等于把每次新样式都变成一次没有报错的实验。

同时这套工作区是纯 AI 编码的：项目由 AI 生、由 AI 维护，iApp 设计器的预览价值随之消失
（过去的迭代反馈全部来自设备截图，设计器从未进入回路）。放弃设计器后，ppt 唯一的立论也就没有了。

## What Changes

- **BREAKING** `.iyu` 收缩到「根容器 + `<UIEventset>`」，不再声明子控件、静态样式、每控件 `<event>` 块
- UI 改为在 `loading` 里由 mjava 一次建完；尺寸一律取 `DisplayMetrics`，不再依赖 `getWidth()`
  （零尺寸重试的补丁随之消失）
- 构建按「段」拆分，每段独立入口 + `postDelayed` 串接：一段抛错只毁一段，页面其余部分照常上屏
- 组件形态定为**返回 View 的工厂函数 + `setTag("ui:name")` 命名句柄**（BeanShell 不能继承类，
  不存在 View 子类这条路）；抽成 `ui.mjava`，权威副本进 SKILL，各工程 vendor 一份
- 新增窗口与安全区规则：背景由根容器自己画、所有系统栏间距由 insets 计算（禁止 dp 常量）、
  状态栏图标深浅走 `WindowInsetsController`、**不主动改窗口 flag**（跟随 iApp 姿态）
- 文档三层按实测改写：`SKILL.md` 控件判据表翻转、`style-guide.md` 重写、`pitfalls.md` #29 降级、
  `md-components-guide.md` 的 TextInputLayout 修复配方作废（mjava 建树时 Context 本来就对）
- G1 `com.showcase.liquidglass` 重写为范式样板，作为 `ui.mjava` 的第一个消费者

**不做**：Android 15/16 的 edge-to-edge 适配（无真机可测，只记待验项与验证出口）；
档 C（`.iyu` 彻底空、mjava `setContentView` 接管）；`View.setId` 路线；新造包名前缀。

## Capabilities

### New Capabilities

- `ui-paradigm`：iApp 工程的界面构建方式——`.iyu` 允许写什么、在哪一帧建树、失败如何局部化、
  组件以什么形态存在与复用、跨 call 如何找回视图
- `window-insets`：窗口姿态与安全区——系统栏/键盘/手势热区如何取值、页面如何避免与系统 UI 打架、
  哪些系统 API 依赖是有意保留或有意回避的

### Modified Capabilities

无（本仓库此前没有任何已归档的 spec）。

## Impact

- **知识层**：`.claude/skills/iapp-development/SKILL.md` 的控件判据表与核心规则 #8；
  `references/style-guide.md`（重写）、`pitfalls.md` #29、`md-components-guide.md`、
  `material-components.md`、新增 `references/ui-kit.md`
- **本机事实层**：`CLAUDE.md` 的 §开发取向、新增「UI 构建范式」指针
- **读数层**：`docs/evidence.md` 新增探针批次；`docs/environments/ldplayer14.md` §7 增加
  Android 15+ 待验项；`docs/environments/tencent-appstore-pc.md` 标记 Android 16 真机补测出口
- **工程**：`project/com.showcase.liquidglass/`（重写 `src/mian.iyu`、拆分 `src/glass.mjava`、
  新增 `src/ui.mjava`）
- **投递**：不变（`tools/push.py` 整目录推送）
