# Proposal

## Why

`docs/evidence.md` 已到 5537 行 / 127 个批次，其中约 83% 的结论已提炼进 SKILL，但原文只进不出，
文件本身成为工作区最胖、最少被通读的文档。与此同时，同一主题在 SKILL 里存在 19 组概念重复，
其中 3 组是「两份说法版本不同」而非简单复述——照旧文档做会直接出错：

- `pitfalls.md` #2 仍写「有共享目录就改共享目录」，与现行「adb 第一、共享目录停用」对立；
- `pitfalls.md` #7 仍写「ppt 声明是默认做法」，与 2026-10-30 起的 mjava 建树范式正相反；
- `ui-kit.md` §已知限制 仍写「图片资源没有一条通吃路径 ⚠ 推断」，而 `recipes.md` 已 ✅ 实测
  `i.us(v,"src","@名称")` 在开发模式与打包产物都成立。

现状还卡住清理本身：`CLAUDE.md`、`runtime-env.md`、`dev-env-setup.md`、`ldplayer14.md`、
`ldplayer9.md`、`oppo-watch-x2.md`、`tencent-appstore-pc.md`、两份 plans 共 20+ 处按「批次号」
引用 evidence.md，所以既不敢删，也无法原地精简。结构上还有 11 个 `###` 子批次挂错了父节
（`NAV-8`～`NAV-16`、`XUI-P3/P4` 被塞进 Material 扫描与组件画廊下），按标题层级无法可靠索引。

## What Changes

- **冻结归档**：现存 5537 行原样移入 `docs/archive/evidence-2026-10.md`，加一段说明头
  （只读、批次 ID 引用键、哪些批次的结论已被后续推翻），保证原文可读、不靠 git 考古。
- **账本重建**：`docs/evidence.md` 重写为按日期平铺的批次索引，每批一行
  （日期 / 批次 ID / 一句结论 / 主文件 / 状态），约 150 行；**批次 ID 原样保留**，
  使外部按批次号的引用继续解析。未决读数（⚠/❓）单独成节，保留读数摘要与验证方法。
- **先修冲突再谈删减**：修 15 处互相矛盾的表述，含上述 3 处阻断项；无法定案的两条
  （Ripple 第三参传 `null`、`pitfalls.md` #40 无条件 `| 8192`）标 ❓ 并写清怎么验。
- **上浮遗漏**：把审计发现的 18 条「已实测但未被 SKILL 吸收」的结论写进对应 reference
  （events / navigation / pitfalls / mjava / watch / emulator / ui-kit / external-library /
  delivery / recipes / methodology / docs-architecture）。
- **引用迁移**：12 处指向「完整步骤 / 原始读数」的引用改指归档文件；只写批次号的引用不动。
  同步更新 `docs/README.md`、`docs-architecture` 的「只追加」定义、`review_config.json` 的
  历史文件与索引表。
- **明确不做（留给下一轮）**：SKILL 19 簇重复的指针化、`SKILL.md` 已验证表压到 ≤20 行、
  同主题文件合并。本轮只保证「删掉 evidence 原文不会丢结论」，不重构 SKILL 结构。

## Capabilities

### New Capabilities

无。本次是文档与知识组织方式的重构，不改变任何系统行为。

### Modified Capabilities

无。`ui-paradigm` 与 `window-insets` 描述的是界面与窗口行为，本轮不触碰其要求文本。
因此本变更在 `.openspec.yaml` 设 `skip_specs: true`。

## Impact

- **重写**：`docs/evidence.md`
- **新增**：`docs/archive/evidence-2026-10.md`（冻结快照，只读）
- **修改的 SKILL 正文**：`references/pitfalls.md`、`ui-kit.md`、`recipes.md`、`style-guide.md`、
  `watch-app-guide.md`、`emulator-setup.md`、`delivery-guide.md`、`environment-adaptation.md`、
  `navigation-guide.md`、`events-guide.md`、`mjava-guide.md`、`external-library-guide.md`、
  `methodology.md`、`md-components-guide.md`、`SKILL.md`（仅共享目录相关三处）
- **修改的规范与配置**：`docs-architecture/references/architecture.md`、`maintenance.md`、
  `scripts/review_config.json`、`docs/README.md`
- **修改的本机文档**：`docs/environments/ldplayer9.md`、`ldplayer14.md`（共享目录停用说明）、
  `docs/dev-env-setup.md`、`docs/runtime-env.md`（仅引用指向）
- **不改动**：`project/` 下任何工程源码、`.iyu` / `.mjava`、投递脚本、设备侧内容
- **不需要设备**：本轮全部为文档变更，不需要投递、运行或 logcat
