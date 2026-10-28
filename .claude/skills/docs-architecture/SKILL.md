---
name: docs-architecture
description: 维护或审阅本工作区的三层文档（SKILL / 根 CLAUDE.md / docs）时使用。只要出现这些情况就先读本技能：同一条结论散落多个文件、拿不准某段该写进 skill 还是 docs、CLAUDE.md 太胖需要精简、docs 索引漏登记新文件、文档之间互相引用的路径失效、结论缺 ✅/⚠/❓ 级别、标了 ❓ 却没写怎么验、他机读数被写成实测、targetSdk/UID/序列号/端口等数值前后不一致、脚本参数改了但文档没跟上、知识沉淀与回填、提交前给文档做体检。带一个只读体检脚本（支持 --json）和分级报告模板，只给修复建议、不改文档。不适用于 iApp 语法、控件、投递、打包问题——那些用 iapp-development。
user-invokable: true
argument-hint: "[audit|migrate] [路径]"
---

# 三层文档架构：规范与审阅

本工作区的知识分三层，各有职责。维护时最容易出的问题不是「写错」，而是「写重了」「写错层了」「索引没跟上」。
本技能给出判据、检查流程和一个只读体检脚本。

## 何时用 / 何时不用

**用**：新增或修改 `CLAUDE.md`、`docs/**`、`.claude/skills/**` 之后；一轮探针回填完成后；
准备提交文档前；怀疑某条结论存在多处、或数值对不上时。

**不用**：写 `.iyu` / `.mjava`、查 iApp 语法与 API、投递调试、打包 —— 走 `iapp-development`；
MD3 组件合规审计 —— 走 `material-3` 的 audit 模式。

## 三层判据（30 秒版）

| 层 | 放什么 | 判据 |
|---|---|---|
| SKILL `.claude/skills/iapp-development/` | 通用 iApp 知识：语法、能力、通道选择、配方 | **换台机器仍成立** |
| 根 `CLAUDE.md` | 本机编排策略：怎么探测、选哪台设备、走哪条通道、流程 | 只对本机成立 |
| `docs/` | 本机事实与证据：环境档案、快照、原始读数 | 是读数不是结论 |

拿不准就先写 `docs/evidence.md`，提炼后再往上搬。完整判据与「结论 → 主文件」查表见
`references/architecture.md`。

## 三问定位

1. **换台机器还成立吗？** 成立 → SKILL；只对这台机器 → `CLAUDE.md`。
2. **是行为，还是读数？** 行为 → SKILL；读数/快照 → `docs/`。
3. **是本工作区的决策规则吗？** 是 → `CLAUDE.md`；元规则（级别、引用、索引）→ 本技能。

## 审阅流程

```
0 记基线        git rev-parse --short HEAD（报告里带上，便于判断行号是否还成立）
1 机械体检      python .claude/skills/docs-architecture/scripts/review_docs.py
2 语义审        按 references/review-checklist.md 的五问逐文件过
3 分级          阻断 / 应修 / 建议（判据是「照文档做会不会出错」）
4 出报告        阻断 → 应修 → 建议 → 语义结论 → 已通过项
5 修复建议      每条给「文件 + 改法 + 理由」；默认只报告，不改文件
6 复跑          改完先 --check 跑相关项，最后全量 + check_portable
```

脚本只覆盖机械可判的部分；跨层重复、结论是否仍成立、级别是否越级这类判断必须人工做。

## 检查项速查

完整判据与真实反例见 `references/review-checklist.md`，脚本实现见 `scripts/review_docs.py`。

| 组 | 检查 |
|---|---|
| LINK | 死链、行号引用、跨 skill 缺前缀、已删目录（`cases/` 等） |
| INDEX | 索引漏登记、索引指向不存在的文件 |
| SKILL | 便携违规（调用 `check_portable.py`）、真实 IP/端口/盘符、混入单机事实 |
| LEVEL | 同格多级别、✅ 缺日期、他机写成 ✅、❓ 缺验证法 |
| DUP | 元规则双写；近似重复仅报告不拦 |
| NUM | 同一指标多处取值不同（**只报组，不判错**） |
| ARG | 脚本参数未文档化、文档命令缺必填参数、文档命令含不存在参数 |

## 严重级别

| 级别 | 判据 | 处置 |
|---|---|---|
| **阻断** | 照文档做会失败；结论是错的；泄露本机信息；新增文件没人找得到 | 当轮修完 |
| **应修** | 会持续放大：级别越级、❓ 无验法、参数未文档化、行号引用、≥3 处重复 | 修高风险项，其余挂待办 |
| **建议** | 措辞、单处重复、可加锚点 | 记录即可 |

## 报告模板

```markdown
# 文档架构体检 YYYY-MM-DD
范围：<扫描到的文件数>    基线：<git sha>（工作区 dirty?）
统计：阻断 N / 应修 N / 建议 N；未运行：<便携检查等>

## 阻断
- [LINK-04] docs/xxx.md:42
  证据：`cases/14-2048.md`
  改法：改为「出处已随 cases 删除，见 evidence 对应批次」
  理由：目录已删，读者无法追溯

## 应修 / 建议
## 语义审结论（人工判断）
## 已通过项（证明跑过）
```

## 常见误判

- **`targetSdk 37` 与 `36` 不是冲突**：前者是安装包、后者是打包产物，属两个对象（见 `references/evidence-and-levels.md`）。
- **他机读数**：凡是「他机 / M2 / 交接文档 / 未复验 / 口述」的条目，上限是 ⚠，不能升 ✅。
- **占位符路径**：含 `< > * ?` 的引用是示例，不该判死链。
- **历史文档**：`docs/evidence.md`、`docs/superpowers/plans/`、`docs/superpowers/specs/` 是归档，旧引用标「历史，仅提示」，不计阻断。
- **图例与索引行**：允许与正文重复短语，不判跨层重复。

## 导航

- `references/architecture.md` — 放哪：三层判据、目录布局、「结论 → 主文件」查表、冲突裁决、版本政策
- `references/evidence-and-levels.md` — 怎么写：级别制度、来源与日期、证据链、❓ 的可验写法、假冲突识别
- `references/maintenance.md` — 怎么维护：索引登记、引用规范、去重、回填流程、提交前清单
- `references/review-checklist.md` — 语义审手册：五问 + 逐文件清单
- `scripts/review_docs.py` — 只读体检脚本
- `scripts/review_config.json` — 排除项、白名单、数值键表、已知假冲突
