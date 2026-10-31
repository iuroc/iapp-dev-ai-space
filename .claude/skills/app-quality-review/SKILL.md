---
name: app-quality-review
description: 对 iApp 工程做周期性工程质量审阅（只报告、不改代码）。只要用户提到工程质量审阅、代码质量巡检、复用检查、样式一致性、重复代码、重构清单、技术债盘点，或问「哪些地方该用现成库却自己写了」，就先读本技能。它给出四类检查（复用缺失 / 样式不统一 / 重复未封装 / 状态与结构）的判定口径、可执行的 grep 扫描、阻断/应修/建议分级与报告模板，并附校准样本与误报豁免清单。
user-invokable: true
---

# 工程质量审阅（iApp 工程）

iApp 工程里「自己实现的东西越多，出问题的概率越大」：`.mjava` 由 BeanShell 解释，没有编译期检查，
一处写错就是整模块失效。所以审阅不判代码风格，只回答三个可执行的问题：
**哪些该复用库却手写了、哪些同类界面长得不一样、哪些逻辑复制了多份**；
顺带查 iApp 特有的散落状态键与职责越界。

## 何时用 / 何时不用

**用**：一轮功能收尾、要出重构清单、怀疑样式分叉、新模块并入后、打包前做技术债盘点。
**不用**：写/改代码（只报告，不改一行）；查 iApp 语法与投递 → `iapp-development`；查设计规范 → `material-3`；判断某条知识放哪层 → `docs-architecture`。

## 适用边界

- 对象：`<工程根>/src/*.mjava` 与 `*.iyu`；默认工程在 `project/<包名>/`
- 前提：BeanShell 解释执行 → PMD / IDE 重构 / 编译期告警都用不上；**grep 定位 + 人工核对 + 设备实测**才是闭环
- 基线：先记 `git -C <工程根> rev-parse --short HEAD`；报告里的行号只对该基线成立
- 只读：不 `adb push`、不 force-stop、不改工程文件；确需上屏确认时单独申请一轮探针

## 复用原则（引用，不复制）

判据在 `.claude/skills/iapp-development/SKILL.md` §「实现取向：能复用库就别自己写」：
**能用「库组件 + 参数」表达的需求，就不要用「自绘 View + 触摸/状态代码」表达**。
组件可用性查 `.claude/skills/iapp-development/references/material-components.md` 的支持矩阵（✅/⚪/❌）。
**BeanShell 不能继承类、只能匿名实现接口**（见 `.claude/skills/iapp-development/references/mjava-guide.md`
§铁律表）——这条决定了「手写」有时是唯一解：`RecyclerView.Adapter`、`LruCache.sizeOf`
这类要继承类的路子得先编译成 dex；没有 dex 时手写网格属于**合法自定义**，但要在报告里登记理由。

## 四类检查与判定口径

| 类 | 一句话判定 | 升级到应修/阻断的判据 | 默认级别 |
|---|---|---|---|
| **REUSE** 复用缺失 | 库有等价物、参数能表达，却自己搭 | 矩阵 ✅/⚪ + 下面三问全过 | 应修；用户可感知错误 → 阻断 |
| **STYLE** 样式不统一 | 同一语义角色 ≥2 套值或结构 | 与 token / 统一工厂不一致，且不在豁免清单 | 应修 |
| **DUP** 重复未封装 | 同构块 ≥3 处，或 2 处 >15 行 | 归一化后能 diff 出同一骨架 | 应修；2 处短块 → 建议 |
| **STATE** 状态与结构 | 跨模块隐式契约、魔法值、越界、死代码 | 键/数值没有单一来源 | 建议；会被误读 → 应修 |

**REUSE 三问**（全 yes 才算复用缺失）：① 该行为在矩阵里是 ✅/⚪？② 参数/主题能到同一视觉？
③ 两处以上能共用同一工厂？任一为 no → 记为「合法自定义」并写理由。

**STYLE 只判同一角色**：正文/次要文字/标题、间距、圆角、图标盒、页头、按压反馈、加载/空/错误三态。
「列表封面 104dp vs 详情封面 132dp」是层级差异，不算；「正文 17sp vs 15sp」算。

**DUP 的合并判据**：合并后需要 **≥3 个 if 分支**才叫合理分支，否则就是复制；
**只差数据源**的列表页/详情页一律按 DUP 处理。

**STATE 只查 iApp 特有的隐式面**：`i.sss` 键、`ui_reg` 句柄名、跨模块裸方法调用、`i.fn` 加载集合、
魔法数值。通用 Java 命名偏好不查。

## 不算问题（先排除，避免误报）

1. **Canvas 现画图标/线稿**：库无等价物（统一的盒尺寸 / 线宽 / 圆头端点）
2. **`ui_insets` 主动查询**：环境限制，`setOnApplyWindowInsetsListener(匿名实现)` 会让整份模块 Parse error
3. **文件 KV 存储**：多工程共用 `getFilesDir()`，`SharedPreferences` 不适用
4. **要继承类的组件**：`RecyclerView.Adapter` / `LruCache.sizeOf` / 自定义 View，BeanShell 做不到
5. **目录树缩进/展开**：`NavigationView` 的 menu 表达不了嵌套层级
6. **WebView 正文排版**（字号/行距/字距）：CSS 是唯一通道
7. **行高/宽用 `getLineHeight()` 实测**：正确做法，不是魔法数
8. **已登记的视觉差异**：阅读器专属配色、主/次按钮尺寸、不同层级封面尺寸；`TabLayout` 逐项改字重同理（`setTabTextColors` 管不了 per-state 粗体）

## 扫描（只读，在 `<工程根>/src` 执行）

```bash
# 0 语言自检：退出码非 0 就停，模块本身已经坏了
python .claude/skills/iapp-development/scripts/check_mjava.py <工程根>/src

# 1 规模与加载基线
wc -l *.mjava | sort -n
grep -c 'i\.fn("' *.mjava | sort -t: -k2 -rn

# 2 REUSE：自绘块 vs 已在用的库组件（左侧同语义块即候选）
grep -n 'new GradientDrawable\|new RippleDrawable\|setOnClickListener' *.mjava
grep -n 'LinearProgressIndicator\|BottomSheetDialog\|TabLayout\|LruCache\|DrawerLayout\|MaterialButton\|TextInputLayout' *.mjava

# 3 STYLE：字号 / 间距 / 圆角 / 页头 / 三态
grep -ohE 'ui_text\([^,]+, *[0-9]+,' *.mjava | grep -oE '[0-9]+' | sort | uniq -c | sort -rn
grep -oh 'ui_dp([0-9]*)' *.mjava | sort | uniq -c | sort -rn
grep -n 'setCornerRadius(ui_dp(' *.mjava
grep -n 'wg_header\|wg_message\|wg_hairline' *.mjava

# 4 DUP：同构块与复制工厂
grep -n 'coverBox\|substring(0, 1)' *.mjava
grep -n 'void .*_wire()' *.mjava
grep -n 'new Thread(new Runnable()' *.mjava

# 5 STATE：键、句柄、加载集合、魔法值
grep -oh 'i\.sss("[^"]*"' *.mjava | sort | uniq -c | sort -rn
grep -n 'ui_reg("' *.mjava
grep -n '^public .*_flag(String key)' *.mjava
```

逐项清单、人工核对点与验收写法见 `references/checklist.md`。
**把命令原样贴进报告**，证明「扫过」；没贴命令对应的结论不算。

## 严重级别

| 级别 | 判据 | 处置 |
|---|---|---|
| **阻断** | 用户可感知的错误或必然失败（死返回键、进度条长度算错、点击无响应） | 当轮修 |
| **应修** | 会持续放大：≥3 处复制、样式分叉、跨模块隐式键、复用缺失 | 排进下一轮重构清单 |
| **建议** | 单处、命名、死参数、可读性 | 记录即可 |

## 输出要求

- **只报告，不改代码**；每条发现给五要素：`文件:行` + 现状 + 可替换的库组件/统一写法 + 风险 + 验收点
- 验收点必须能上屏或看日志（例：「四个 Tab 页不再出现返回箭头」「100% 时进度条右缘贴住卡片内容右缘」）
- 误报写进「已排除」节并给理由，别静默丢弃
- 模板：`references/output-template.md`；校准样本：`references/calibration.md`

## 导航

- `references/checklist.md` — 四类逐项清单：判据、grep、人工核对点、验收写法
- `references/output-template.md` — 报告模板 + 一条填好的示例
- `references/calibration.md` — 校准样本：真实工程的通过项与问题项，用来对齐「什么该报、什么不该报」
