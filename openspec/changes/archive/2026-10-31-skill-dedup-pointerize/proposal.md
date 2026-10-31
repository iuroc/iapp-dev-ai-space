# Proposal

## Why

第一轮（`evidence-ledger-converge`）把 `docs/evidence.md` 从 5628 行收敛为 126 行索引，
但 SKILL 内部「同一结论写在多处」的问题没有动。审计出来 19 组概念重复，其中 6 组是「应修」级别：
模块加载 5 处、投递通道 5 处、状态栏 4 处、TIL 修复配方 4 处、外部库装载 3 处、`downkey` 4 处。

后果不是文件变胖，而是**改一处必漏一处**：第一轮修「共享目录优先级」「ppt 是否默认」「res 图片路径」
三个冲突时，每一处都有 2–5 个副本需要同步。`SKILL.md` 的「已验证」表 120 行里约 115 行是
references 正文的复述，已经事实上成为第二事实源。

## What Changes

- **一条结论一个主文件**：19 组重复各指定一个权威文件，其余位置压成一行指针
  （保留该文件自己的「失败签名 / 索引行」，删掉重复的「做法」正文）。
- **`SKILL.md` 已验证表瘦身**：先把它独有的 3 条结论搬进 `recipes.md`，再把整表压成
  ≤20 行的**能力清单**（一行一个能力 + 级别，不写实现细节）。
- **`SKILL.md` 正文减重**：§多模块 17 行 → 3 行；§iyu 白名单替换表 → 一行指针；
  核心规则 #3 的 9 行 → 2 行；§界面构建三个实现前提 → 1 行 + 指针。
- **明确不做**：不合并文件（`material-*` 两份、环境三份保持原样）；不动第一轮已对齐的冲突结论；
  不改任何 `project/` 内容。

## Capabilities

### New Capabilities

无。纯文档组织重构，不改变系统行为。

### Modified Capabilities

无。`ui-paradigm` / `window-insets` 的要求文本不动；本变更设 `skip_specs: true`。

## Impact

- **`SKILL.md`**：表与正文大幅缩短（预计 349 → 250 行上下）
- **references**：`modularization-guide`、`mjava-guide`、`environment-adaptation`、`ftp-delivery`、
  `emulator-setup`、`delivery-guide`、`status-bar-guide`、`pitfalls`、`ui-kit`、`md-components-guide`、
  `material-components`、`navigation-guide`、`events-guide`、`iyu-guide`、`style-guide`、`recipes`、
  `debugging`、`methodology`、`iapp-i-reference`、`icon-guide`、`project-structure`、`iapp-history`
- **不改动**：`docs/evidence.md`（索引）、`docs/archive/`、工程源码、投递脚本
- **不需要设备**：纯文档变更
