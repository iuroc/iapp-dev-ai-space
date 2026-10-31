# Tasks

## 1. 探针：验证范式前提

整个范式建立在「mjava 建树尚未在本仓库跑过」之上，先问完再写库。

- [x] 1.1 建探针工程 `android-sync/ProjectApp/com.demo.uiparadigm/`（不 init git；iApp 工程根是 `/sdcard/Pictures/ProjectApp`，放 `iapp-demo/` 下不会出现在工程列表），`.iyu` 只留根容器 + `<UIEventset>`；直接落在共享目录、不经 `push.py` —— 验证：工程列表可见、运行不崩
- [x] 1.2 P2：纯根 `.iyu` 下 `loading` / `loadingComplete` / `pause` / `resume` 是否照常触发 —— 验证：logcat 出现四条对应日志
- [x] 1.3 P1：`loading` 里往根 `addView` 是否显示、是否被宿主后续流程清掉 —— 验证：截图有内容，切后台再回前台内容仍在
- [x] 1.4 P5：根视图的 `getHeight()`、`getLocationOnScreen()`、`getRootWindowInsets()` 三组数值 —— 验证：四项读数写进日志，能判断宿主的窗口姿态
- [x] 1.5 P3：`i.sss` 能否存 `HashMap<String,View>` 并跨 `call` 取回同一实例 —— 验证：两次 `call` 打同一对象 hash，日志里 hash 相同
- [x] 1.6 P4：一次性建 40 个视图的耗时 —— 验证：日志给出毫秒数，用于判断分段粒度
- [x] 1.7 P8：mjava 新建的 `TextView` 与 ppt 声明的同属性 `TextView` 在测量上是否一致（`wrap_content` / `textstyle=bold` / `maxlines`） —— 验证：日志打出两组 `getMeasuredWidth/Height`，数值一致或记录差异
- [ ] 1.8 P6：三键导航 ↔ 手势导航切换后 `systemBars.bottom` 的实际变化 —— **本机无法回答**：雷电 14 的 SystemUI 不提供 `navigationBars` InsetsSource（启停 threebutton / gestural overlay 前后 `dumpsys window displays` 都只有 statusBars / ime / mandatorySystemGestures / tappableElement），`systemBars.bottom` 恒 0；已改用「改造 Android 16 真机补测」承接，见 1.9 与 4.5
- [ ] 1.9 P7：键盘弹出时 ime inset 与内容位移 —— **本机无法回答**：模拟器无软键盘 UI，输入框聚焦后 IME 不显示（`ime list` 有 pinyin、已是默认、`show_ime_with_hard_keyboard=1` 均已确认），`ime.bottom` 恒 0；改真机补测
- [x] 1.10 把 1.2–1.9 的原始读数写进 `docs/evidence.md`（批次号、日期、命令、读数） —— 验证：`docs/evidence.md` 能查到本批次
- [x] 1.11 清掉探针工程（`android-sync/ProjectApp/com.demo.uiparadigm/`） —— 验证：目录不存在（第 2 组做完后再清；`sdk/` 由 iApp 生成，要单独清空后才能 rmdir）

## 2. 组件库最小集

只做 G1 重写要用的函数；每加一个函数都以上一组的实测为准，不凭空设计。

- [x] 2.1 新建 `.claude/skills/iapp-development/assets/ui-kit/ui.mjava`，含 dp/sp 换算、颜色解析、`init(root)` 与三段式根骨架 —— 验证：`kit.iyu` 里 `i.fn("ui")` 成功、跨模块 `ui_log` 成功、`bg/safe/overlay` 三层齐
- [x] 2.2 建容器 / 文本 / 图像 + 摆位函数（`place` 全部走 `LayoutParams`，把 `layout_gravity` 坑关进库） —— 验证：`ui_fplace(..., Gravity.BOTTOM|CENTER_HORIZONTAL)` 贴底居中卡片上屏正确（正是 ppt `layout_gravity` 做不到的那一种）；其余 gravity 值由 3.x 的 G1 重写覆盖
- [x] 2.3 外观函数：圆角、描边、渐变、玻璃 —— 验证：圆角 + 描边已上屏（截图对照）；渐变与玻璃是纯 `GradientDrawable` 组合，与 G1 现有观感的一致性在 3.x 里对照
- [x] 2.4 insets 接入：`safe` / `overlay` 的 padding 由「insets 减根偏移」的差值与 ime 计算（监听器路线已因为 Parse error 否掉，改 `ui_insets()` 主动查询） —— 验证：`rootTop=72 rootH=1848 gapBottom=0 bars=72/0 => pad 0/0`，与 P5 读数自洽；三键/手势切换后的随动本机测不了（P6 同理），归真机
- [x] 2.5 命名句柄与注册表函数（`ui_reg` / `ui_get` / `ui_layer` / `ui_tag` / `ui_find`） —— 验证：`ui_find(card)=found`、`stageB tag lookup=found`、三层图层按名取回全部 ok
- [x] 2.6 段调度函数（名字 + 延迟，自动打进出日志） —— 验证：`stage> BOOM` → `stage! BOOM`（`UndeclaredThrowableException`）→ `stage> AFTER` → `stageAfter 存活`，隔离成立
- [x] 2.7 写 `references/ui-kit.md` 初版（函数清单、约定、已知限制），并在 SKILL 导航里登记 —— 验证：文档里能查到 2.1–2.6 全部函数

## 3. G1 重写为范式样板

- [x] 3.1 `project/com.showcase.liquidglass/src/mian.iyu` 砍到根容器 + `<UIEventset>`，删掉全部子控件与 `<event>` 块 —— 验证：`grep -c '<View' src/mian.iyu` 结果为 1
- [x] 3.2 把 `ui.mjava` 复制进工程，`glass.mjava` 入口改为「骨架段 / 内容段 / 效果段」三段，各自独立入口 —— 验证：日志里三段进出各两行
- [x] 3.3 删掉硬编码系统栏间距（`sh - dp(28) - ch` 一类）与对 `setStatusBarColor` 的视觉依赖，改走 overlay 层 + 根自绘背景 —— 验证：`grep -n 'dp(28)' src/glass.mjava` 无结果（胶囊间距同时从 28dp 收到 24dp，与左右边距对齐）
- [x] 3.4 推送上机，由用户运行并回报四个观察点（胶囊贴底位置、扫光、状态栏图标可读、无空屏） —— 验证：四项均确认（打包版截图确认三项，扫光由用户目视确认「有白光从左到右」）
- [x] 3.5 抽重复三次以上的逻辑回 `assets/ui-kit/ui.mjava`，并同步 `references/ui-kit.md` —— 验证：`diff` 两处 `ui.mjava` 完全一致；新增 `ui_dpf` / `ui_addTop` / `ui_addWeight` 已进文档
- [x] 3.6 工程内提交（碎提交，`<type>: <message>` + `Co-Authored-By` 行） —— 验证：`git -C project/com.showcase.liquidglass log --oneline -5` 能看到本轮提交（`9614cc8`）

## 4. 知识层按实测改写

- [x] 4.1 `SKILL.md`：控件判据表翻转为「mjava 建树为默认，`.iyu` 只留根」，核心规则 #8（`build.xml` 登记）降级为例外说明 —— 验证：表里第一条是「是页面根容器吗 → 写在 `.iyu`」，其余走 mjava
- [x] 4.2 `references/style-guide.md` 重写为「骨架与样式分层」，删除「画布能看见」立论，四个 ppt 语义坑（`layout_gravity` / `weight` / `alpha` / `padding` 按 px）标注为档 A 历史 —— 验证：全文无「ppt 优先/画布可见」的立论，坑表集中在「档 A 历史」一节
- [x] 4.3 `references/pitfalls.md` #29 标注版本与适用范围；`references/md-components-guide.md` 的 TextInputLayout 修复配方标注为档 A 才需要 —— 验证：两处都有适用范围说明（#29 另补 API 34 复现与新范式不涉及）
- [x] 4.4 `CLAUDE.md` §开发取向 的「控件优先在 ppt 声明」翻转，新增「UI 构建范式」一节点向 `style-guide.md` —— 验证：`grep -n 'mjava' CLAUDE.md` 能定位到 §UI 构建范式
- [x] 4.5 `docs/environments/ldplayer14.md` §7 增加 Android 15+ 的 edge-to-edge 与系统栏配色待验项（❓ + 怎么验）；`docs/environments/tencent-appstore-pc.md` 登记 Android 16 真机为本机补测出口 —— 验证：两份档案各有对应行（ldplayer14 另记 P6/P7 本机问不出来）
- [x] 4.6 `README.md` 与 `docs/README.md` 索引同步新增/改名的文件 —— 验证：README 的 skill 行已注明 `assets/ui-kit/`；docs/README 无新增顶层文件，无需改动
- [x] 4.7 跑 `review_docs.py --fail-on blocker` 与 `check_portable.py`（脚本实际在 `.claude/skills/*/scripts/`，不在 `docs/scripts/`） —— 验证：阻断 0 / 应修 0 / 建议 3（已知分口径数值）、portable OK

## 5. 集成验证

- [x] 5.1 单条命令完成投递：`python tools/push.py com.showcase.liquidglass --serial <serial>` 退出码 0 —— 验证：退出码 0
- [x] 5.2 复核 `docs/evidence.md` 的探针结论与 `SKILL.md` / `style-guide.md` 的表述一致（读数 → 结论 → 通用规则三级对得上） —— 验证：逐条对照，**修掉一处冲突**：核心规则 #5 原称 `i.syso` 进 logcat 的 `ygs`，实测面板打开时抓不到，已改成条件表述并同步 evidence R2 与 ui-kit.md
- [x] 5.3 `openspec validate mjava-first-ui --strict` 通过 —— 验证：`Change 'mjava-first-ui' is valid`

## 6. 窗口姿态：内容铺到屏幕顶边（施工中追加）

用户在看 G1 成片后追加的需求：状态栏照常显示，但页面内容铺到屏幕最顶边。

- [x] 6.1 先做「隐藏系统栏」的沉浸式（`hide(systemBars)` + 边缘临时唤出） —— 验证：可用，但用户否掉（要的是系统栏保留）
- [x] 6.2 改 `setDecorFitsSystemWindows(false)` + 透明状态栏 —— 验证：**无效**，内容仍从状态栏下开始
- [x] 6.3 遍历祖先清 `padding` / `fitsSystemWindows` / `clipToPadding`（含延迟到布局后再清） —— 验证：**无效**，清掉后被宿主下一轮布局加回
- [x] 6.4 打祖先链日志定位预留量的真实位置 —— 验证：在「根的直接父容器」的 top padding 上（`LinearLayout[pad 0,72,0,0]`），8 层祖先全量打印
- [x] 6.5 改为绕过：根上移「已预留距离」+ 高度补成整屏 + 父容器关 `clipToPadding` —— 验证：三色对照（窗口绿 / 内容顶橙）显示状态栏变橙，内容真的透过去
- [x] 6.6 去掉 iApp 专有接口 `uycl`，纯 Window 方案落地；库新增 `ui_bleed` / `ui_statusBarIcons` —— 验证：正式配色下状态栏与渐变顶部无缝
- [x] 6.7 spec / design / pitfalls #32 / 已验证表 / evidence WINDOW-1 同步 —— 验证：`openspec validate --strict` valid、文档体检阻断 0

## Workflow follow-up

- 归档本 change：`/opsx:archive`（把两份 delta spec 合入 `openspec/specs/`）
- 开 change 2 `puzzle2048-demo`：用定稿的组件库从零建 2048，**不许改库**，暴露的缺口另开 change
- Android 16 真机到手后补测 edge-to-edge / 系统栏配色，结论回填 `ldplayer14.md` 与 SKILL
