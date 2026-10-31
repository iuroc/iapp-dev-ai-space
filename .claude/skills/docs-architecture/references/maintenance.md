# 维护：新增、引用与去重

> 本文件是「怎么维护」的规范正文，其他文件只写指针。

## 1. 索引登记

新增、改名、删除文件时，**同一次提交**更新「最近一层」的索引。五个索引文件：

| 索引 | 覆盖范围 |
|---|---|
| `.claude/skills/iapp-development/SKILL.md` 的「导航」节 | `references/*.md`、`scripts/*.py` |
| `.claude/skills/iapp-development/scripts/README.md` | 每个脚本一行 |
| `docs/README.md` | `docs/` 下的文件与目录 |
| `docs/environments/README.md` | 每个环境档案 |
| `docs/scripts/README.md` | `docs/scripts/` 下每个脚本 |

规则：

- 只登记到最近一层，不要跨层重复登记细节。`docs/README.md` 写到 `scripts/` 这一级即可，细节交给子 README。
- 索引行写「名称 + 一句话用途」，不要裸文件名。
- 免登记：`docs/artifacts/`（二进制证据，按目录说明即可）、`tmp-recon/`、`android-sync/`。
- 删除文件时，索引行也要删；不要留下指向不存在文件的条目。

## 2. 引用规范

| 做法 | 原因 |
|---|---|
| 引用写「文件 + §小节标题」，**不写行号** | 行号必随编辑漂移，历史 spec 里已经全量失效 |
| 跨 skill 引用带 skill 路径前缀，如 `.claude/skills/<skill>/references/<主题>.md` | 只写 `references/<主题>.md` 会被误解析到当前 skill |
| skill 包内引用用相对 skill 根的 `references/<主题>.md` | 与 `check_portable.py` 的校验口径一致 |
| 不引用已删除的目录（如 `cases/`） | 死链；历史结论改为指向 `evidence.md` 的日期/批次 |
| 示例路径用占位符（`<设备IP>`、`<项目ID>`、`<宿主目录>`） | 真实值只在本机层出现 |

## 3. 去重三步

发现同一条结论在多处时：

1. **定主文件**：按 `architecture.md` 的「结论 → 主文件」查表。
2. **别处降级为一行指针**：「详见 `<主文件>` §X」，删掉重复的细节与日期。
3. **索引只留短语**：索引行的用途说明可以复述关键词，但不搬结论。

允许重复的：图例、术语表、索引行、表格表头。
不允许重复的：任何带级别/日期/条件的结论句。

判断方法：**改一处时，另一处会不会漏改？** 会漏，就是重复。

## 4. 回填流程

```
探针/实测
  → docs/archive/evidence-<YYYY-MM>.md   日期 + 批次 + 探针 + 原始读数（当月续写，跨月冻结）
  → docs/evidence.md        同一批次一行索引（一句结论 + 主文件 + 状态；只增行）
  → docs/environments/<环境>.md   长期事实，带级别 + 来源 + 日期
  → SKILL                   通用结论，带版本前提 + 级别
  → 清掉临时探针
  → 跑 review_docs.py + check_portable.py
```

更正旧结论时：**追加一条更正记录**，或在原处加一行「已被 XX 推翻」；不要静默改写历史读数。

**计划与规格只写判据，不写快照数字**：不要在 plan / spec 里写死「基线 commit `<sha>`」
「本次预计阻断 20 / 应修 12」这类会随仓库演进而失效的值。写「体检阻断为 0 才提交」这种判据，
读者才知道什么算通过；写死数字的文档过两周就自相矛盾（DOC-2 的基线 commit 已 `git cat-file` 不存在）。

## 5. 脚本与文档一致

- **事实源是 `--help`**，不是文档。文档里的命令必须能被真的执行。
- 新增/改名参数：同一次提交里更新对应的 `README.md` 与使用示例。
- 删除参数：反向 grep 文档，清掉残留示例。
- 文档里的示例命令要写全必填参数；省略号截断的命令请在代码块外说明。
- 破坏性参数（删除、覆盖）必须在文档里写明默认值与边界。

## 6. 提交前清单

- [ ] 新增/改名/删除的文件已登记到最近一层索引
- [ ] 没有 `文件.md:行号` 形式的引用
- [ ] 新结论写在自己的主文件里，别处只有指针
- [ ] 每条结论带级别 + 来源 + 日期；他机不超过 ⚠；❓ 都写了怎么验
- [ ] 文档里的命令能照抄执行（必填参数齐全、参数名存在）
- [ ] `python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on blocker` 通过
- [ ] `python .claude/skills/iapp-development/scripts/check_portable.py` 通过
