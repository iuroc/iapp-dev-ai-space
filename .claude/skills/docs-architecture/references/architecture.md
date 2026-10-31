# 架构：一条知识该放哪

> 本文件是「归属」的规范正文，其他文件只写指针，不复制。

## 1. 三层职责

| 层 | 位置 | 放什么 | 判据 |
|---|---|---|---|
| SKILL | `.claude/skills/iapp-development/` | iApp 本身的能力、语法、失败签名、通用配方、通道选择方法 | **换台机器仍成立** |
| 本工作区策略 | 根 `CLAUDE.md` | 怎么探测、选哪台设备、走哪条通道、探针流程、变量取值顺序 | 只对本机成立 |
| 事实与证据 | `docs/` | 环境档案、当前快照、原始读数、历史计划与规格 | 是读数或归档，不是通用结论 |

三条推论：

- `CLAUDE.md` **不教 iApp 语法**；它教「这台机器上怎么做事」。
- `docs/` **不写通用方法**；能换台机器成立的，搬去 SKILL。
- SKILL **不写本机数值**（IP、端口、序列号、盘符、真实包名、单机日期）；这些留在 `docs/`。

### 工程私有文档区（三层之外）

每个 iApp 工程在**工程根**自带两块私有文档区，只对该工程成立，不往工作区搬。iApp 只读
`src/` 里的既有文件，工程根可安全新增任意目录（不改动已有文件即可）。

| 位置 | 放什么 |
|---|---|
| `<工程根>/openspec/` | 该工程自己的 OpenSpec 根：`config.yaml`、`specs/`、`changes/`（含 `changes/archive/`）。提案、设计、规格、任务、归档全在工程内部 |
| `<工程根>/docs/` | 工程私有资料区：规格、计划、报告、探针读数、设计素材等，类型不限 |
| `<工程根>/docs/superpowers/plans\|specs/` | 单工程的 superpowers SDD 产物（两级归属见 §5） |

✅（用户决策，2026-10-30；来源：用户口述规则）

- **项目不搭 AI 编码工作区**：工程里不放 `.claude/`，也不放 agents 或 skill 副本做日常依赖。
  旧说法「脱离时把 `.claude/skills/iapp-development/` 整目录复制进工程」**作废**。
- **开发方式**：先拉取本工作区，工程放进 `project/`，在本工作区里开发；工程自身保持干净
  （源码 + 资源 + 自己的 `openspec/` 与 `docs/`）。
- **本工作区读写工程文档**：以**工程根为基准**写相对路径，不写工作区相对路径；定位 OpenSpec
  根时，工程内 `<工程根>/openspec/` 是**最近根**，优先于工作区 `openspec/`。
- **工作区三层不放任何单个 App 的私有文档**：`.claude/skills/`、根 `CLAUDE.md`、`docs/` 都不收；
  工作区 `openspec/specs/` 只收**跨工程**的范式级能力（如 ui-paradigm、window-insets），
  不收单个 App 的功能规格。

它不是第四层，判据仍走下面五问：

- 工程 `docs/` / `openspec/` 里攒出**换台机器仍成立**的结论 → 照旧上浮到 SKILL。
- 只对**本机**成立的实证 → 留在工作区 `docs/`，不往工程里塞。
- 只对**这个工程**成立 → 工程 `<工程根>/docs/` 或 `<工程根>/openspec/`。

工程随时可能脱离本工作区独立成库，但工程**不再复制** skill，脱离后工程内引用的 skill 路径
不再解析：需要随工程长期保存的结论，写进工程自己的 `openspec/` 或 `docs/`。工程内引用 skill
仍写 skill 路径前缀（`.claude/skills/iapp-development/…`），禁止写工作区绝对路径或上一层相对路径。

## 2. 归属五问

按顺序问，止于第一条命中：

1. **换台机器还成立吗？** 成立 → SKILL。
2. **是行为/条件，还是具体读数？** 行为 → SKILL；读数 → `docs/`。
3. **是本工作区的决策规则吗？**（优先级、设备选择、流程）→ 根 `CLAUDE.md`。
4. **是原始日志/命令输出/截图吗？** → 当月账本 `docs/archive/evidence-<YYYY-MM>.md`；
   同时在 `docs/evidence.md` 加一行批次索引。
5. **只对这个 App 工程成立吗？**（它的功能规格、提案、计划、报告、素材）→ 工程根：
   `<工程根>/openspec/` 或 `<工程根>/docs/`，**不进**工作区三层；判据见 §1「工程私有文档区」。

五问都答不上来：先把原始读数写进当月账本、在 `docs/evidence.md` 记一行索引，等结论稳定再往上提炼。

## 3. 一条结论一个主文件

同一条结论只允许有一个「主文件」，其余位置只能写**一行指针**。主文件按下表选：

| 结论类型 | 主文件 | 别处只能写 |
|---|---|---|
| iApp 行为 / 语法 / API / 配方 / 失败签名 | `.claude/skills/iapp-development/references/<主题>.md` | 一行指针 + 级别 |
| 通道选择方法与通用坑 | `iapp-development/references/environment-adaptation.md` | 指针 |
| 本机编排策略（协商顺序、设备选择、通道优先级、变量顺序） | 根 `CLAUDE.md` | 指针 |
| 某台机器的长期事实（安装目录、root、工程根、权限、能力矩阵） | `docs/environments/<环境ID>.md` | 指针 |
| 当前会话快照（在连设备、serial、UID、端口） | `docs/runtime-env.md`（顶部必须带日期） | 不复制，只引 |
| 原始读数（logcat、截图、命令输出、批次） | `docs/archive/evidence-<YYYY-MM>.md`（当月可续写，跨月冻结） | 引用日期/批次 |
| 批次索引（批次 ID → 一句结论 → 主文件） | `docs/evidence.md` | 引用批次 ID |
| 计划、历史规格（superpowers SDD 约定位置） | 跨工程任务 → 工作区 `docs/superpowers/plans|specs/`；单个工程 → `<工程根>/docs/superpowers/plans|specs/`（归档，不作权威） | 不复述结论 |
| 只对某个 iApp 工程成立的资料（规格、报告、探针读数、素材） | `<工程根>/docs/`（工程私有，随工程脱离） | 不复述 |
| 能力规格（openspec） | 跨工程范式级 → 工作区 `openspec/specs/`；单个工程 → `<工程根>/openspec/specs/` | 不复述 |
| 脚本行为与参数 | 脚本 `--help`（事实源）+ 同目录 `README.md` | 指针 |
| 级别制度、引用规范、索引规则、冲突裁决 | 本 skill `references/*.md` | 一行指针 |
| UI 辅助技能 ↔ iApp 的映射与限制 | `docs/ui-skills.md` | 指针 |
| 第三方内容服务 API 契约与跨平台接入（歌德借阅机） | `.claude/skills/gede-read-api/references/api-reference.md` | 一行指针 + 级别 |

例外：**索引行、图例、术语表**允许与正文重复短语（读者靠它找到正文），但不得搬整段结论。

判断是否重复时，问一句：**改一处时，另一处会不会漏改？** 会漏改，就是重复。

## 4. 冲突裁决

优先级：**原始读数 > 环境档案 > SKILL 通用结论 > plans/specs**。

- 档案与 SKILL 冲突时，以档案实测为准，改 SKILL 的**条件或级别**，不把读数抄进 SKILL。
- plans/specs 是历史，冲突时一律让位；它们的结论若仍有效，说明还没提炼，应回填。
- 无法裁决时标 ⚠ 并写进「未决读数」节，不要硬选一个。

## 5. 目录布局

```
<工作区根>/
├── CLAUDE.md                        # 本机编排策略
├── .claude/
│   ├── skills/
│   │   ├── iapp-development/        # 通用 iApp 知识（可分享）
│   │   │   ├── SKILL.md             # 导航 + 核心规则 + 已验证表
│   │   │   ├── references/*.md
│   │   │   └── scripts/*.py + README.md
│   │   ├── gede-read-api/           # 歌德借阅机内容 API（内部私有，与 iApp 无关）
│   │   └── docs-architecture/       # 本 skill：文档规范与审阅（不可分享）
│   └── agents/                      # 子智能体定义（只读执行壳，规则仍在 skills）
├── docs/
│   ├── README.md                    # docs 索引
│   ├── environments/                # 环境档案（一个环境一个文件）
│   ├── runtime-env.md               # 当前机器快照
│   ├── evidence.md                  # 批次索引（只增行；原文在 archive/）
│   ├── archive/                     # 原始读数账本，按月一个文件；跨月冻结只读
│   │   └── evidence-YYYY-MM.md
│   ├── dev-env-setup.md             # 本机装机/连机步骤
│   ├── ui-skills.md                 # UI 辅助技能映射
│   ├── scripts/                     # 本机脚本（含 README 索引）
│   ├── superpowers/                 # superpowers SDD 标准位置（归档）
│   │   ├── plans/                   # 实施计划 YYYY-MM-DD-<feature>.md
│   │   └── specs/                   # 设计规格 YYYY-MM-DD-<topic>-design.md
│   ├── reference/                   # 官方手册副本
│   └── artifacts/                   # 二进制证据（免登记到文件级）
├── openspec/                        # 跨工程 OpenSpec 根
│   ├── config.yaml
│   ├── specs/                       # 只收跨工程范式级能力（如 ui-paradigm、window-insets）
│   └── changes/                     # 含 archive/；不收单个 App 的功能规格
└── tools/                           # 本机薄包装（不含实现）
```

不是文档层的位置：`android-sync/`（设备镜像）、`tmp-recon/`（临时反编译）、`.superpowers/`（会话状态）、
`.claude/agents/`（Claude Code 专用执行壳，不可移植，不承载规则）。

每个 iApp 工程本身也是一个小仓库，脱离本工作区后要能自解释：

```
<工程根>/
├── src/                            # .iyu + .mjava（iApp 只读这里）
├── build.xml / .project / icon.png
├── openspec/                       # 工程自己的 OpenSpec 根（最近根优先于工作区 openspec/）
│   ├── config.yaml
│   ├── specs/
│   └── changes/                    # 含 archive/
├── docs/                           # 工程私有资料区（类型不限）
│   └── superpowers/
│       ├── plans/                  # YYYY-MM-DD-<feature>.md
│       └── specs/                  # YYYY-MM-DD-<topic>-design.md
└── （不建 .claude/）                # 项目不搭 AI 工作区
```

**项目不搭 AI 编码工作区**：不放 `.claude/`、不放 agents、不放 skill 副本；开发在本工作区里做
（工程放进 `project/`），工程自身只留源码、资源与自己的 `openspec/`、`docs/`。
✅（用户决策，2026-10-30；来源：用户口述规则）

**计划与规格遵循 superpowers SDD 约定**，位置按归属分两级，本工作区不再另设
`docs/plans/`、`docs/specs/`：

- **单个工程的任务** → `<工程根>/docs/superpowers/plans|specs/`，随工程走
- **跨工程任务**（文档体检、环境探测等不属于任何工程的活）→ 工作区 `docs/superpowers/plans|specs/`

**OpenSpec 产物同样两级**：跨工程的能力 → 工作区 `openspec/specs/`（只收范式级规格）；
单个工程的功能规格、提案、归档 → `<工程根>/openspec/`，最近根优先于工作区。
✅（用户决策，2026-10-30；来源：用户口述规则）
- 实施计划 → `YYYY-MM-DD-<feature-name>.md`（由 `writing-plans` 产出）
- 设计规格 → `YYYY-MM-DD-<topic>-design.md`（由 `brainstorming` 产出）
- 执行期产物（ledger、任务简报、review 包）→ `.superpowers/sdd/<plan 名>/`，gitignored，属会话状态，不归档

执行中的进度写在 ledger 里，但 ledger 不入库：**任务完成时要在计划文件里勾 checkbox**，
否则仓库里看不出这份计划做到哪一步。

## 6. 版本政策（通用部分）

- 未标注版本的结论，默认按**主开发环境**的 API 级别成立。
- 低版本差异必须单独标 ⚠ 并写版本前提，不要与高版本结论合并成一句。
- 跨版本结论冲突时**分条记录**，不要取平均或只留一条。
- 具体「主环境是哪台机器、哪个 API」属于本机策略，写在根 `CLAUDE.md`。
