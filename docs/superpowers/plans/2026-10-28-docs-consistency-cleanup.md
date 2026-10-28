# 三层文档一致性收尾 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `review_docs.py` 剩余的 64 项「应修」清零，让三层文档的级别标注、引用与索引完全自洽。

**Architecture:** 按检查项分任务。每个任务先跑一次体检拿到精确清单（不写死行号，行号会漂移），改完再跑同一检查项确认归零；跨层重复单独一个任务，因为它需要人工判断主文件归属，脚本只报警不判错。

**Tech Stack:** Python 3.10+；`.claude/skills/docs-architecture/scripts/review_docs.py`（只读体检）；Markdown。

**Spec:** `.claude/skills/docs-architecture/references/review-checklist.md`（判据与真实反例）+ `docs/evidence.md` 的「2026-10-28 DOC-1」一节（本轮基线读数）。

**基线：** `fb190e0`，阻断 0 / 应修 64 / 建议 22。

## Global Constraints

- **不改写历史读数**：`docs/evidence.md` 只允许在末尾追加；正文里的旧结论要更正时，写「（已被 XX 更正）」而不是抹掉原文。
- **他机读数上限 ⚠**：任何「他机 / M2 / 交接文档 / 未复验 / 口述」的条目不能标 ✅。
- **禁行号引用**：一律写「文件 §小节标题」，不写 `文件.md:123`。
- **每条事实三件套**：级别 + 来源 + 日期；标 ❓ 必须同条写「怎么验」。
- **阻断必须保持 0**：每次提交前跑 `python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on blocker`。
- **便携检查必须绿**：每次提交前跑 `python .claude/skills/iapp-development/scripts/check_portable.py`。
- **不要动并行会话的文件**：`.claude/skills/iapp-development/references/` 下的 `mjava-guide.md`、`events-guide.md`、`md-components-guide.md`、`modularization-guide.md`、`debugging.md` 归青简项目会话；`docs/evidence.md` 的追加也先问一句再动。
- **占位符写法**：`<设备IP>`、`<端口>`、`<项目ID>`、`<宿主目录>`；不写真实 IP/端口/serial。

## Review Focus

1. **给 ✅ 补日期时填错日期**——日期必须是该事实的实测日，不是今天；没有证据就降级为 ⚠，不要编。
2. **给 ❓ 补的「怎么验」本身没验过**——写成「建议验法」，级别保持 ❓，不要因为写了方法就升级。
3. **加 skill 前缀时指错目录**——前缀必须是实际存在的 `.claude/skills/<skill>/references/<文件>.md`，改完用一条 `ls` 核对。
4. **清 `cases/` 死链时删掉唯一线索**——保留原文件名（如「原 cases 目录下的 14-2048」），只去掉会判死链的路径形式。
5. **去重时判错主文件**——按 `architecture.md` 的「结论 → 主文件」查表，拿不准就保留现状并记进报告的「语义审结论」，不要猜。

## File Structure

| 文件 | 本计划中的职责 |
|---|---|
| `docs/environments/ldplayer14.md` | 补日期（7）、补 ❓ 验法、跨 skill 前缀（1） |
| `docs/environments/ldplayer9.md` | 补日期（7）、补 ❓ 验法（2） |
| `docs/environments/README.md` | 补日期（6）、补 ❓ 验法（5）、跨 skill 前缀（4） |
| `docs/environments/tencent-appstore-pc.md` | 补 ❓ 验法（7）、跨 skill 前缀（2） |
| `docs/ui-skills.md` | 补日期（3）、补 ❓ 验法（1） |
| `docs/dev-env-setup.md` | 跨 skill 前缀（1） |
| `CLAUDE.md` | 跨 skill 前缀（2），保持精简 |
| `docs/superpowers/specs/2026-10-26-blackboard-design.md` | 归档死链（5 + 1） |
| `docs/superpowers/specs/2026-10-26-2048-design.md` | 归档死链（3） |
| `docs/evidence.md` | 归档死链（3，仅改措辞，不改读数） |
| `.claude/skills/docs-architecture/references/review-checklist.md` | 跨 skill 前缀（2） |

---

### Task 1: 补齐 ✅ 的日期（LEVEL-03，23 处）

**Files:**
- Modify: `docs/environments/ldplayer14.md`（7）、`docs/environments/ldplayer9.md`（7）、
  `docs/environments/README.md`（6）、`docs/ui-skills.md`（3）

**Interfaces:**
- Consumes: 无
- Produces: 四个文件里所有 ✅ 行都带 `YYYY-MM-DD`，供后续任务的行定位保持稳定

- [ ] **Step 1: 拿到精确清单**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LEVEL-03
```
Expected: 列出 23 条 `文件:行 — ✅ 缺少日期`，顺序固定。

- [ ] **Step 2: 逐条补日期**

规则（三选一，按顺序）：
1. 该行结论能在 `docs/evidence.md` 找到对应批次 → 填那个日期；
2. 同文件「元信息」里有「最后核验 YYYY-MM-DD」→ 填该日期；
3. 两者都没有 → 把该行降为 `⚠`，并在该文件的「未测项」表里加一行写清怎么验。

不要填当天日期：日期是证据的时间，不是修改的时间。

- [ ] **Step 3: 验证归零**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LEVEL-03
```
Expected: `LEVEL-03×0`（其余检查项的数字不变）。

- [ ] **Step 4: 全量回归**

Run: `python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on blocker`
Expected: 阻断 0，退出码 0。

- [ ] **Step 5: Commit**

```bash
git add docs/environments docs/ui-skills.md
git commit -m "docs: 给环境档案与 UI 技能文档的 ✅ 结论补日期"
```

---

### Task 2: 给 ❓ 补「怎么验」（LEVEL-05，15 处）

**Files:**
- Modify: `docs/environments/tencent-appstore-pc.md`（7）、`docs/environments/README.md`（5）、
  `docs/environments/ldplayer9.md`（2）、`docs/ui-skills.md`（1）

**Interfaces:**
- Consumes: Task 1 补好的日期（同一批文件，避免二次冲突）
- Produces: 每个 ❓ 后面都跟一句可执行的验证方法，供下一轮真正去测

- [ ] **Step 1: 拿到精确清单**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LEVEL-05
```
Expected: 15 条 `❓ 没有写「怎么验」`。

- [ ] **Step 2: 逐条补验证方法**

三种合格写法，任选其一并保持 `❓` 级别不变：
1. 一条命令：`怎么验：adb shell getprop ro.build.version.sdk`（期望 34）；
2. 一个探针：`怎么验：在 android-sync/iapp-demo/<批次>/ 建页，loading 里打印结果并上屏`；
3. 一次观察判据：`怎么验：打开设置页看版本号是否显示 14`。

禁止写「待测」「后续验证」「需要时再测」。
`docs/environments/README.md` 里那 5 条如果已在某个环境档案的「未测项」表里写过，改成指向该表的指针。

- [ ] **Step 3: 验证归零**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LEVEL-05
```
Expected: `LEVEL-05×0`。

- [ ] **Step 4: 全量回归 + 提交**

Run: `python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on blocker` → 阻断 0。

```bash
git add docs/environments docs/ui-skills.md
git commit -m "docs: 为未测项补上可执行的验证方法"
```

---

### Task 3: 跨 skill 引用补前缀（LINK-03，12 处）

**Files:**
- Modify: `docs/environments/README.md`（4）、`docs/environments/tencent-appstore-pc.md`（2）、
  `docs/environments/ldplayer14.md`（1）、`docs/dev-env-setup.md`（1）、`CLAUDE.md`（2）、
  `.claude/skills/docs-architecture/references/review-checklist.md`（2）

**Interfaces:**
- Consumes: 无
- Produces: 所有指向 skill 内文件的引用都用完整前缀，`LINK-01` 不会再被误报

- [ ] **Step 1: 拿到精确清单**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LINK-03
```
Expected: 12 条，每条给出 `证据：references/<名>.md` 与建议前缀。

- [ ] **Step 2: 逐条改为带前缀的完整路径**

把 `references/<名>.md` 改成 `.claude/skills/iapp-development/references/<名>.md`
（本 skill 自己的引用改成 `.claude/skills/docs-architecture/references/<名>.md`）。
`CLAUDE.md` 里两处注意保持短句，不要因为加前缀把一行撑成两行——必要时改成「见 iapp-development 的 `references/<名>.md`」。

- [ ] **Step 3: 核对目标存在（防止指错目录）**

Run:
```bash
ls .claude/skills/iapp-development/references/ .claude/skills/docs-architecture/references/
```
Expected: 上一步写进去的每个文件名都能在列出的结果里找到。

- [ ] **Step 4: 验证归零 + 提交**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LINK-03
```
Expected: `LINK-03×0`。

```bash
git add docs CLAUDE.md .claude/skills/docs-architecture
git commit -m "docs: 跨 skill 引用补全路径前缀"
```

---

### Task 4: 历史归档死链（LINK-04 11 + LINK-01 1）

**Files:**
- Modify: `docs/superpowers/specs/2026-10-26-blackboard-design.md`（5 处 `cases/` + 1 处指向 canvas-guide.md 的引用）、
  `docs/superpowers/specs/2026-10-26-2048-design.md`（3 处 `cases/`）、`docs/evidence.md`（3 处 `cases/`）

**Interfaces:**
- Consumes: 无
- Produces: 归档文档不再有指向已删目录的路径

- [ ] **Step 1: 拿到精确清单**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LINK-04,LINK-01
```
Expected: 12 条，集中在两份 spec 与 evidence。

- [ ] **Step 2: 改成不带路径的追溯说法**

不重建 `cases/` 目录。每条按下面两种之一改：
- evidence 里有对应批次：`（原 cases/<名>，目录已删除；读数见 docs/evidence.md 2026-10-26 <批次>）`
- 找不到对应批次：`（原 cases/<名>，目录已删除，出处不可追溯）`

那条 canvas-guide.md 引用改成实际存在的 `.claude/skills/iapp-development/references/recipes.md`（该文件承载 Canvas 配方）。
`docs/evidence.md` 只改这三处措辞，**不动任何读数**。

- [ ] **Step 3: 验证归零 + 提交**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check LINK-04,LINK-01
```
Expected: 两项都是 ×0。

```bash
git add docs
git commit -m "docs: 归档文档中已删除 cases 目录的引用改为可追溯说法"
```

---

### Task 5: 数值口径分组（NUM-01，2 组）

**Files:**
- Modify: 视 Step 1 结果而定，通常在 `docs/runtime-env.md`、`docs/environments/*.md`、
  `docs/dev-env-setup.md` 三者之间

**Interfaces:**
- Consumes: 无
- Produces: 每个指标只剩「一个值」或「两个值 + 各自口径」

- [ ] **Step 1: 看是哪两组**

Run:
```bash
python .claude/skills/docs-architecture/scripts/review_docs.py --check NUM-01
```
Expected: 两行 `同一指标出现多个取值：<key>`，带 `needs_human` 标记。已知候选是 `UID`（`u0_a50` / `u0_a72`）与 `serial`（`5554` / `5556`）。

- [ ] **Step 2: 按「同一对象 / 同一时间 / 同一层」判断**

- 同一对象的旧值 → 删掉旧值，或标「已过期（YYYY-MM-DD 前）」；
- 不同对象（不同机器、不同实例）→ 各自加口径限定，例如
  `UID：主机 A = u0_a72；主机 B = u0_a50（口径不同，非冲突）`。

不要用「以最新的为准」一句话糊过去——那正是上一轮 `targetSdk` 被判成矛盾的成因。

- [ ] **Step 3: 验证 + 提交**

Run: `python .claude/skills/docs-architecture/scripts/review_docs.py --check NUM-01`
Expected: ×0，或只剩 `known_split` 里的提示级条目。

```bash
git add docs
git commit -m "docs: 同一指标的多处取值按口径合并或标注"
```

---

### Task 6: 跨层重复治理（DUP-01，人工判断）

**Files:**
- Modify: 视 Step 1 盘点结果而定；预期涉及 `docs/environments/*.md`、`CLAUDE.md`、
  `.claude/skills/iapp-development/references/environment-adaptation.md`、
  `.claude/skills/iapp-development/references/emulator-setup.md`、
  `.claude/skills/iapp-development/references/pitfalls.md`

**Interfaces:**
- Consumes: 无
- Produces: 七条高频结论各只剩一个主文件，其余位置是一行指针

- [ ] **Step 1: 逐条盘点落点**

对下面七条，分别在三层里 grep 关键词，记录所有落点：

| 结论 | 建议关键词 |
|---|---|
| 共享目录 FUSE 旧缓存 | `FUSE`、`旧缓存`、`/sdcard` |
| MSYS 路径改写 | `MSYS_NO_PATHCONV` |
| 不用 bind mount | `bind mount`、`mount --bind` |
| `Android/data` 软链 | `Android/data`、`软链` |
| 投递通道优先级 | `优先级`、`共享目录`、`adb push` |
| 版本政策 | `API 34`、`版本优先` |
| 改前关工程 / force-stop | `force-stop`、`关工程` |

- [ ] **Step 2: 按查表定主文件，其余改指针**

判据在 `.claude/skills/docs-architecture/references/architecture.md` 的「结论 → 主文件」表。
改法：主文件保留完整结论（级别 + 日期 + 条件），其他位置压成一行
「见 `<主文件>` §<小节>」。历史 spec / evidence 不作为主文件，只保留原文不改。

**拿不准就保留现状**，把该条写进本轮报告的「语义审结论」，不要猜——判错会把正确的档案改坏。

- [ ] **Step 3: 验证没有新增重复**

Run: `python .claude/skills/docs-architecture/scripts/review_docs.py --check DUP`
Expected: `DUP-02×0`（元规则不双写）；`DUP-01` 属报告级，不参与通过判定。

- [ ] **Step 4: 提交**

```bash
git add docs CLAUDE.md .claude/skills/iapp-development/references
git commit -m "docs: 高频结论各归一个主文件，其余改为指针"
```

---

### Task 7: 收尾与记录

**Files:**
- Modify: `docs/evidence.md`（末尾追加一节，不改历史）

**Interfaces:**
- Consumes: Task 1–6 的全部改动
- Produces: 一份「剩余 0 应修」的基线记录，供下一轮对照

- [ ] **Step 1: 全量体检**

Run: `python .claude/skills/docs-architecture/scripts/review_docs.py`
Expected: 阻断 0、应修 0；建议项可以非 0（措辞类不强制清）。

- [ ] **Step 2: 便携检查**

Run: `python .claude/skills/iapp-development/scripts/check_portable.py`
Expected: `portable check: OK`。

- [ ] **Step 3: 追加记录**

在 `docs/evidence.md` 末尾追加一节，写明：基线 sha、清理前后数字（阻断/应修/建议）、
Task 6 里「保留现状」的条目清单及原因。**只追加**。

- [ ] **Step 4: 提交**

```bash
git add docs/evidence.md
git commit -m "docs: 记录本轮文档一致性清理的基线与结果"
```

---

## 执行方式建议

任务之间**有顺序依赖**（Task 1 与 Task 2 改同一批文件；Task 3 依赖前两步稳定下来的行定位），
但每个任务都可独立验收。建议用 **subagent-driven**：每个任务一个全新 subagent 实现、一个全新 reviewer 验收，
因为这里的错误大多是「判断错主文件」「编了一个日期」这类需要外部视角才能发现的问题。

如果只追求快，也可以 native 执行——体检脚本本身就是每步的客观验收。
