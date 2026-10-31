# Tasks

## 1. 基线

- [x] 1.1 把当前未提交的 5 个文件（`pitfalls.md`、`status-bar-guide.md`、`ui-kit.md`、`assets/ui-kit/ui.mjava`、`docs/evidence.md`）提交为一个基线 commit —— 验证：`git status --short` 除本变更的 `openspec/` 目录外无其他改动，且 `git log -1 --oneline` 形如 `docs: <中文单行>`

## 2. 修冲突（必须在删原文之前完成）

- [x] 2.1 `references/pitfalls.md` #2：删掉「有共享目录/同步盘就改共享目录；不可用时再 `adb push`」，改为一行为「通道优先级见 `environment-adaptation.md` §推荐优先级」—— 验证：`grep -n '有共享目录' references/pitfalls.md` 无命中，且该段仍保留 bind mount 的失败签名
- [x] 2.2 `references/pitfalls.md` #7 与 `references/md-components-guide.md`：把「ppt 里声明…（这是默认做法）」「默认仍先试 ppt」改为「历史路径 / 仅例外场景」—— 验证：`grep -rn '这是默认做法\|默认仍先试 ppt' references/` 无命中
- [x] 2.3 `references/ui-kit.md` §已知限制：把「图片资源没有一条同时覆盖开发模式与打包产物的路径」改成一行指针指 `recipes.md` §工程 res/ 图片 —— 验证：`grep -n '没有一条同时覆盖' references/ui-kit.md` 无命中，且 `grep -n 'recipes.md' references/ui-kit.md` 命中该行
- [x] 2.4 `references/delivery-guide.md` §产物可移植性：把「自包含 ⚠（推断）」与「手表侧载 ⚠（口述未取 logcat）」升为 ✅ 并附日期与依据（WATCH-2 的 adb 安装/启动/logcat 全链路）—— 验证：两行均含 `✅` 与 `2026-10-29`，且不再出现 `未取 logcat`
- [x] 2.5 `references/watch-app-guide.md` §11：把「滚轮 = `ACTION_SCROLL`，可驱动 `ScrollView`」改为「scrcpy 注入的滚轮在 `sdk` / `uhid` 两种模式均无效，滚动用按住拖动」—— 验证：`grep -n '滚轮' references/watch-app-guide.md` 不再出现「可驱动 `ScrollView`」，且含「拖动」
- [x] 2.6 共享目录残留：`SKILL.md` 已验证表两行与导航第 337 行、`references/emulator-setup.md` §2/§3/§4、`docs/environments/ldplayer9.md` §3/§4 —— 统一标注「通道 2026-10-30 起停用，以下为机制/历史说明」—— 验证：`grep -rn 'Pictures/ProjectApp' .claude/skills/iapp-development docs/environments` 的每一处命中都同段含「停用」或「历史」
- [x] 2.7 `references/environment-adaptation.md` §共同铁律：给「不读回设备侧做 md5/size 比对」加范围——仅指 `adb push`；FTP 通道仍用服务端 `SIZE`/`MD5` 校验 —— 验证：该条同时出现 `adb push` 与 `FTP`
- [x] 2.8 `references/style-guide.md` §波纹 与 `references/pitfalls.md` #40：两条无法定案的冲突（Ripple 第三参传 `null` 是否安全；`| 8192` 是否有条件）改为并列两种说法并标 `❓` 与「怎么验」—— 验证：两处均含 `❓`，且各有一句以「怎么验：」开头的操作
- [x] 2.9 收口其余口径：`references/emulator-setup.md` §3.5 的 `chown`/`chmod` 标「仅雷电 9 / sdcardfs」；`targetSdk 37（安装包） vs 36（打包产物）」在涉及处统一表述 —— 验证：`grep -n 'chown' references/emulator-setup.md` 同行含「雷电 9」；`grep -rn 'targetSdk' references/` 无「以 37 为准」类单一取值表述
- [x] 2.10 提交本阶段 —— 验证：`git log -1 --oneline` 为 `fix: <中文单行>`，`git show --stat HEAD` 只含第 2 组涉及的文件

## 3. 上浮遗漏结论（18 条）

- [x] 3.1 `references/events-guide.md`：新增「`addTab` 首枚自动回调一次、切换时 unselected+selected 成对」；补「`keyboard` 排在 `editormonitor` 之前、每次按键重发」；把 8 个未收录变量（`st_vW2`/`st_tT`/`st_taB`/`st_pS`/`st_pT`/`st_dX`/`st_dY`/`st_isB`）加进 §事件内置变量并标 `⚠（DEX 证实，未运行期验）` —— 验证：`grep -n 'addTab' references/events-guide.md` 命中新句；`grep -c 'st_dX'` ≥ 1
- [x] 3.2 `references/navigation-guide.md` §addv 与 `references/pitfalls.md` #7：补 drawer 子控件未改 gravity 时的 `IllegalArgumentException: No drawer view found with gravity LEFT`；补「`build.xml` 登记但不 ppt 声明 → 不崩也不渲染」—— 验证：`grep -rn 'No drawer view found' references/` 与 `grep -n '不渲染' references/pitfalls.md` 均命中
- [x] 3.3 `references/mjava-guide.md` §原生底部抽屉：补「底色禁用 `setBackgroundColor`（抹掉 MaterialShapeDrawable 圆角），走 `setFillColor`」「展开用 `getBehavior().setState(STATE_EXPANDED)`」—— 验证：`grep -n 'setFillColor\|setState' references/mjava-guide.md` 两处均命中
- [x] 3.4 `references/watch-app-guide.md`：§5 补「圆屏禁用系统 Dialog，确认类交互改页内面板」；§11 补「scrcpy 注入坐标须按 client/视频 换算并叠加 `ClientToScreen` 原点」—— 验证：`grep -n 'Dialog' references/watch-app-guide.md` 命中该句；`grep -n 'ClientToScreen'` 命中
- [x] 3.5 `references/emulator-setup.md` §4 与 `references/external-library-guide.md`：补「`adb push` 不能在 `Android/data/<pkg>/` 下自建目录（`secure_mkdirs failed`），须先 `mkdir -p`」；补「`classes.jar` 可完全不含 R 类（XUI 1025 类全非 R），此时 aapt2 生成的 R 直接顶上」—— 验证：`grep -rn 'secure_mkdirs' references/` 与 `grep -n '1025' references/external-library-guide.md` 均命中
- [x] 3.6 `references/ui-kit.md`：补「两类失败分型：调不存在的 `i` 方法抛 `UndeclaredThrowableException`，可被 `catch(Throwable)` 接住；调未加载模块方法报 `Command not found`，整个方法中断、接不住」；补「`i.sss` 直存 View 跨 call 取回为 null，需包一层 `HashMap` 或改用 `setTag(int, View)`」并标 `⚠（单次现象，待复验）` —— 验证：`grep -n 'UndeclaredThrowableException' references/ui-kit.md` 命中；该条含 `⚠` 与「待复验」
- [x] 3.7 `references/recipes.md` 与 `references/methodology.md`：新增「单弹窗多级选择器（level 栈 + 返回 + 仅叶子回调）」小节；§Canvas 卡面 补「先按 200×250 量级画完再放大」；§铁律 补「视觉类需求先出静帧/多方案预览再上机」—— 验证：三个小节标题都能 `grep -n` 到，且方法论那条标注来源批次
- [x] 3.8 `.claude/skills/docs-architecture/references/maintenance.md` §回填流程：补「计划与规格只写判据，不写死基线 commit 与体检计数」—— 验证：`grep -n '基线 commit\|快照数字' maintenance.md` 命中
- [x] 3.9 提交本阶段 —— 验证：`git log -1 --oneline` 为 `docs: <中文单行>`，且 `git show --stat HEAD` 覆盖 3.1–3.8 列出的文件

## 4. 冻结原文 + 重建索引

- [x] 4.1 创建 `docs/archive/`，把当前 `docs/evidence.md` 原样复制为 `docs/archive/evidence-2026-10.md` —— 验证：`diff <(git show HEAD:docs/evidence.md) docs/archive/evidence-2026-10.md` 无输出（此时尚未加说明头）
- [x] 4.2 给归档文件加说明头：只读声明、「批次 ID 是引用键不要改名」、以现行 SKILL 为准，并集中列出已被后续批次推翻的 8 类结论及其正确去向 —— 验证：`diff` 结果只剩新增的头部行（用 `git diff --no-index --stat` 核对只增不删）；头部 8 类各有一行去向
- [x] 4.3 重写 `docs/evidence.md` 为索引：按日期平铺 127 行（日期 / 批次 / 一句结论 / 主文件 / 状态），`###` 子批次升为独立行；文末设「未决读数」节，⚠/❓ 项保留读数摘要与「怎么验」—— 验证：`wc -l docs/evidence.md` < 260；`grep -c '^| 20' docs/evidence.md` ≈ 127；8 个被外部引用的批次 ID（`SYNC-2`/`SYNC-3`/`UIPROBE-1`/`UIPROBE-2`/`DELIVERY-1`/`WATCH-2`/`E0`/`E1`）逐个 `grep -n` 有命中
- [x] 4.4 迁移引用：把指向「完整步骤 / 原始读数」的 12 处改为 `docs/archive/evidence-2026-10.md <批次ID>`；只写批次号的引用不动 —— 验证：`grep -rn 'evidence.md' docs/ CLAUDE.md README.md | grep -i '原始读数\|完整步骤'` 不再指向 `docs/evidence.md`；抽查 20 处批次号引用能定位
- [x] 4.5 登记新文件与规则：`docs/README.md` 增 `archive/` 行；`docs-architecture/references/architecture.md` §5 目录布局补 `archive/` 并在 §3 表补「冻结快照」一行；`scripts/review_config.json` 的 `history_files` 加归档路径 —— 验证：`python .claude/skills/docs-architecture/scripts/review_docs.py` 不对 `docs/archive/` 报问题，且不报「索引未登记」
- [x] 4.6 提交本阶段 —— 验证：`git log -1 --oneline` 为 `docs: <中文单行>`；`git show --stat HEAD` 含新增归档、重写的 `docs/evidence.md` 与登记的 3 个文件

## 5. 验收

- [x] 5.1 跑文档体检：`python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on blocker` 与 `python .claude/skills/iapp-development/scripts/check_portable.py` —— 验证：两条命令退出码为 0，阻断数为 0
- [x] 5.2 抽查结论可达性：随机取 10 个已从 evidence 删除的批次，按索引行的「主文件」能定位到等价结论 —— 验证：10/10 命中，抽查结果写进本任务的完成说明
- [x] 5.3 汇报：列出「验了哪几条 / 一致·推翻·未知 / 回填了哪些文件 / 下一轮做什么」—— 验证：汇报覆盖四段，并明确下一轮是 SKILL 19 簇指针化

## Workflow follow-up

- 审查通过后归档本变更（`/opsx:archive`），归档前确认第二轮（SKILL 指针化）已另立变更，不并入本次。
