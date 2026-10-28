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

## 2. 归属四问

按顺序问，止于第一条命中：

1. **换台机器还成立吗？** 成立 → SKILL。
2. **是行为/条件，还是具体读数？** 行为 → SKILL；读数 → `docs/`。
3. **是本工作区的决策规则吗？**（优先级、设备选择、流程）→ 根 `CLAUDE.md`。
4. **是原始日志/命令输出/截图吗？** → `docs/evidence.md`。

四问都答不上来：先写进 `docs/evidence.md`，等结论稳定再往上提炼。

## 3. 一条结论一个主文件

同一条结论只允许有一个「主文件」，其余位置只能写**一行指针**。主文件按下表选：

| 结论类型 | 主文件 | 别处只能写 |
|---|---|---|
| iApp 行为 / 语法 / API / 配方 / 失败签名 | `.claude/skills/iapp-development/references/<主题>.md` | 一行指针 + 级别 |
| 通道选择方法与通用坑 | `iapp-development/references/environment-adaptation.md` | 指针 |
| 本机编排策略（协商顺序、设备选择、通道优先级、变量顺序） | 根 `CLAUDE.md` | 指针 |
| 某台机器的长期事实（安装目录、root、工程根、权限、能力矩阵） | `docs/environments/<环境ID>.md` | 指针 |
| 当前会话快照（在连设备、serial、UID、端口） | `docs/runtime-env.md`（顶部必须带日期） | 不复制，只引 |
| 原始读数（logcat、截图、命令输出、批次） | `docs/evidence.md` | 引用日期/批次 |
| 计划、历史规格（superpowers SDD 约定位置） | `docs/superpowers/plans/`、`docs/superpowers/specs/`（归档，不作权威） | 不复述结论 |
| 脚本行为与参数 | 脚本 `--help`（事实源）+ 同目录 `README.md` | 指针 |
| 级别制度、引用规范、索引规则、冲突裁决 | 本 skill `references/*.md` | 一行指针 |
| UI 辅助技能 ↔ iApp 的映射与限制 | `docs/ui-skills.md` | 指针 |

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
├── .claude/skills/
│   ├── iapp-development/            # 通用 iApp 知识（可分享）
│   │   ├── SKILL.md                 # 导航 + 核心规则 + 已验证表
│   │   ├── references/*.md
│   │   └── scripts/*.py + README.md
│   └── docs-architecture/           # 本 skill：文档规范与审阅（不可分享）
├── docs/
│   ├── README.md                    # docs 索引
│   ├── environments/                # 环境档案（一个环境一个文件）
│   ├── runtime-env.md               # 当前机器快照
│   ├── evidence.md                  # 原始读数账本（只追加）
│   ├── dev-env-setup.md             # 本机装机/连机步骤
│   ├── ui-skills.md                 # UI 辅助技能映射
│   ├── scripts/                     # 本机脚本（含 README 索引）
│   ├── superpowers/                 # superpowers SDD 标准位置（归档）
│   │   ├── plans/                   # 实施计划 YYYY-MM-DD-<feature>.md
│   │   └── specs/                   # 设计规格 YYYY-MM-DD-<topic>-design.md
│   ├── reference/                   # 官方手册副本
│   └── artifacts/                   # 二进制证据（免登记到文件级）
└── tools/                           # 本机薄包装（不含实现）
```

不是文档层的位置：`android-sync/`（设备镜像）、`tmp-recon/`（临时反编译）、`.superpowers/`（会话状态）。

**计划与规格遵循 superpowers SDD 约定**，本工作区不再另设 `docs/plans/`、`docs/specs/`：

- 实施计划 → `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`（由 `writing-plans` 产出）
- 设计规格 → `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`（由 `brainstorming` 产出）
- 执行期产物（ledger、任务简报、review 包）→ `.superpowers/sdd/<plan 名>/`，gitignored，属会话状态，不归档

执行中的进度写在 ledger 里，但 ledger 不入库：**任务完成时要在计划文件里勾 checkbox**，
否则仓库里看不出这份计划做到哪一步。

## 6. 版本政策（通用部分）

- 未标注版本的结论，默认按**主开发环境**的 API 级别成立。
- 低版本差异必须单独标 ⚠ 并写版本前提，不要与高版本结论合并成一句。
- 跨版本结论冲突时**分条记录**，不要取平均或只留一条。
- 具体「主环境是哪台机器、哪个 API」属于本机策略，写在根 `CLAUDE.md`。
