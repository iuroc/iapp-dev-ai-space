# Design

## Context

第一轮已建立「一条结论一个主文件」的判据（`.claude/skills/docs-architecture/references/architecture.md` §3），
但 SKILL 内部没有执行。审计给出的 19 组重复里，6 组会让照做的人出错，13 组只是维护负担。

两个约束决定了做法：

- `pitfalls.md` 的定位是「现象 + 失败签名」速查，它保留症状表不算重复；
  重复的是它跟着写了一遍完整「做法」。
- `SKILL.md` 的「已验证」表按 `architecture.md` §5 是**规定的组成部分**（导航 + 核心规则 + 已验证表），
  所以不能整表删除，只能把它降回「能力清单」的粒度。

## Goals / Non-Goals

**Goals:**

- 同一主题只留一份正文；改一条结论只需改一个文件。
- `SKILL.md` 首屏只承载「导航 + 硬规则 + 能力速览」，不承载实现细节。
- 删表内结论前先确认它在 references 有等价正文。

**Non-Goals:**

- 不合并文件、不改文件边界、不重命名。
- 不重新审计结论对错（第一轮已做），只处理重复。
- 不改 `docs/` 侧。

## Decisions

### D1 主文件按「谁最完整」指派，不按「谁最先写」

| 主题 | 主文件 | 其余降级为 |
|---|---|---|
| 模块加载 / facade | `modularization-guide.md` | `mjava-guide.md` 保留 `i.fn` 单点事实；`pitfalls` #22/#23/#36 只留签名 |
| 投递通道与共同铁律 | `environment-adaptation.md` | `ftp-delivery.md` 留实测特性表；`emulator-setup.md` 留路径模型 |
| 状态栏 | `status-bar-guide.md` | `pitfalls` #32/#40、`ui-kit.md`、`SKILL.md` 只留现象与指针 |
| TIL 修复配方 | `md-components-guide.md` | `pitfalls` #7 压成 2 行；`material-components.md` 只留「需修复」标记 |
| 外部库装载 | `external-library-guide.md` | `pitfalls` #24–#27 只留失败签名 |
| `downkey` 吞返回 | `navigation-guide.md` | `events-guide.md` 留键码读数；`pitfalls` #17 留去抖 |
| ppt 四个静默失效键 | `iyu-guide.md` | `style-guide.md` 改一览表；`pitfalls` #29 留圆屏复现 |
| Ripple 遮罩 | `style-guide.md` | `pitfalls` #35、`recipes.md`、`SKILL.md` 各 1 行 |
| SearchBar 崩溃 | `pitfalls.md` #7 | `material-components.md`、`md-components-guide.md`、`SKILL.md` 各 1 行 |
| `build.xml` 登记 | `project-structure.md` | `SKILL.md` 留判据表；其余 1 行 |
| 5555 端口冲突 | `emulator-setup.md` §5 | `pitfalls` #28 留读数；`SKILL.md` 1 行 |
| logcat 命令与双证据 | `debugging.md` | `methodology.md` 留原则句；`SKILL.md` #4 指针 |
| `i.sss` / `i.d` 语义 | `iapp-i-reference.md` | `pitfalls` #6、`mjava-guide.md`、`recipes.md` 各 1 行 |
| 应用图标 | `icon-guide.md` | `project-structure.md`、`pitfalls` #21、`SKILL.md` 各 1 行 |
| 打包产物版本读数 | `iapp-history.md` | `delivery-guide.md` 指针 |
| `i.call` 三参数 | `mjava-guide.md` §跨模块调用 | `modularization-guide.md`、`pitfalls` #14、`SKILL.md` 各 1 行 |

**理由**：主文件选「写了最多上下文、且读者最先会打开」的那份；`pitfalls.md` 的签名表是它自己的索引，
保留症状、删掉复述的做法，符合 `architecture.md` §3「索引行允许重复短语」。

### D2 已验证表压成「能力清单」，不是删表

**选择**：≤20 行，每行 = 能力 + 一句边界 + 级别，实现细节一律指向 references。

**备选**：整表删除、改为主题导航。

**理由**：表是 `architecture.md` 规定的组成部分；完全删掉会失去「一眼看全验证过什么」的入口。
但 120 行逐条复述已让它成为第二事实源，必须降到「清单」粒度。

### D3 先搬后删

表内独有的 3 条（`setTag(HashMap)`、`i.sss` 存 `int[]`/`ArrayList`、`invalidate()` 刷新）
先写进 `recipes.md` §持久化 / §Canvas，确认存在后再删表行。

## Risks / Trade-offs

- [指针链太长：A→B→C] → 指针一律直接指向主文件，不链式指向另一处指针。
- [删过头，读者在 pitfalls 里找不到做法] → `pitfalls` 每条保留「现象 + 一句根因」；
  做法只在主文件，指针写在根因后面。
- [主文件与旧副本内容有细微差异，合并时丢信息] → 逐簇比对后，把旧副本里**独有的**读数补进主文件再删。
- [大改之后 diff 难审] → 按簇分 3 个 commit（SKILL 表 / 6 个应修簇 / 10 个建议簇）。

## Migration Plan

1. 搬 3 条独有结论进 `recipes.md` → commit。
2. 压 `SKILL.md` 表与正文 → commit。
3. 处理 6 个应修簇 → commit。
4. 处理 10 个建议簇 → commit。
5. 体检 + 汇报。

回滚：每簇独立 commit，可单簇 revert。

## Open Questions

无。
