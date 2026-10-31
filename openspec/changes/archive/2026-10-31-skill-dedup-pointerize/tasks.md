# Tasks

## 1. 先搬后删：表内独有结论

- [x] 1.1 把 `SKILL.md` 已验证表独有的 3 条结论搬进 `references/recipes.md`：`setTag(HashMap)` 跨 call 可取回（可装 Bitmap/Canvas/Paint）、`i.sss` 能存 `int[]`/`ArrayList`、已上屏 Bitmap 改内容后 `invalidate()` 能刷新 —— 验证：`grep -n 'HashMap\|ArrayList\|invalidate()' references/recipes.md` 三条各至少 1 次命中
- [x] 1.2 提交 —— 验证：`git log -1 --oneline` 为 `docs: …`

## 2. `SKILL.md` 瘦身

- [x] 2.1 「已验证」表压到 ≤20 行能力清单：每行「能力 + 一句边界 + 级别」，实现细节改指 references —— 验证：表行数 `awk '/^## 已验证/,/^## 导航/' SKILL.md | grep -c '^| '` ≤ 22（含表头分隔两行）
- [x] 2.2 §多模块 17 行压到 ≤5 行（保留 `i.fn`/`importAll` 位置、`i.d.f` 仅开发模式、`i.call` 不用，其余指向 `modularization-guide.md`）—— 验证：`awk '/^## 多模块/,/^## 核心规则/' SKILL.md | wc -l` ≤ 8
- [x] 2.3 §iyu 白名单替换表改为一行指针（指向 `iyu-whitelist.md`）—— 验证：`grep -c '^| `us`' SKILL.md` = 0
- [x] 2.4 核心规则 #3 压到 ≤3 行（只留「adb 整目录 → FTP → 手工导入」「先关工程、整目录、只认返回码」两句 + 指针）—— 验证：`awk '/^3\. 【荐】/,/^4\. 【荐】/' SKILL.md | wc -l` ≤ 4
- [x] 2.5 §界面构建的三个实现前提改为 1 行 + 指针 —— 验证：`grep -c 'setOnApplyWindowInsetsListener(匿名实现)' SKILL.md` = 0
- [x] 2.6 提交 —— 验证：`git log -1 --oneline`，`git show --stat` 只含 `SKILL.md`

## 3. 应修簇指针化（6 组）

- [x] 3.1 模块加载：`mjava-guide.md` §加载模块压成「`i.fn("b")` + 指针」；`pitfalls.md` #22/#23/#36 删掉复述做法、保留失败签名 + 指针 —— 验证：`grep -c 'importAll' references/mjava-guide.md` ≤ 2，且 `grep -rn 'modularization-guide.md' references/pitfalls.md | wc -l` ≥ 3
- [x] 3.2 投递通道：`SKILL.md` #3 已在上组处理；`ftp-delivery.md` §8 对照表改指针；`emulator-setup.md` §2 原则 1 的通道优先级改指针；`delivery-guide.md` §外部同步改指针 —— 验证：`grep -rn 'environment-adaptation.md' references/ftp-delivery.md references/emulator-setup.md references/delivery-guide.md | wc -l` ≥ 3
- [x] 3.3 状态栏：`pitfalls.md` #32/#40 各压成「现象 + 结论一句 + 指针」；`ui-kit.md` §窗口姿态只留 `ui_insets` 语义 + 指针 —— 验证：`grep -c 'status-bar-guide.md' references/pitfalls.md` ≥ 2，且 `awk '/^## 32\./,/^## 33\./' references/pitfalls.md | wc -l` ≤ 40
- [x] 3.4 TIL 配方：`pitfalls.md` #7 的修复配方压成 2 行 + 指针；`material-components.md` 只留「需修复」标记 —— 验证：`grep -c 'updateEditTextBoxBackgroundIfNeeded' references/pitfalls.md` ≤ 1
- [x] 3.5 外部库：`pitfalls.md` #24–#27 删掉复述链路、保留失败签名 + 指针 —— 验证：`grep -c 'external-library-guide.md' references/pitfalls.md` ≥ 4
- [x] 3.6 `downkey`：`events-guide.md` §按键参数保留键码/去抖读数 + 一行指针；`pitfalls.md` #17 只留 `st_eA/st_eR` 与去抖 —— 验证：`grep -c 'navigation-guide.md' references/events-guide.md references/pitfalls.md` 各 ≥1
- [x] 3.7 提交 —— 验证：`git show --stat HEAD` 覆盖 3.1–3.6 的文件

## 4. 建议簇指针化（10 组）

- [x] 4.1 ppt 四键：`style-guide.md` §档 A 改「四键一览 + 指针」；`pitfalls.md` #29 留圆屏复现；`material-components.md`/`SKILL.md` 各 1 行 —— 验证：`grep -c 'iyu-guide.md' references/style-guide.md` ≥ 1
- [x] 4.2 Ripple：`pitfalls.md` #35 压成 2 行 + 指针；`recipes.md` §行内水波纹改指针 —— 验证：`grep -c 'style-guide.md' references/pitfalls.md` ≥ 1
- [x] 4.3 SearchBar：`material-components.md`、`md-components-guide.md`、`SKILL.md` 各 1 行指向 `pitfalls.md` #7 —— 验证：`grep -rn 'pitfalls.md.*#7' references/material-components.md references/md-components-guide.md SKILL.md | wc -l` ≥ 3
- [x] 4.4 `build.xml` 登记：`SKILL.md` 只留「先看有没有点号」判据表；登记格式与自查命令指向 `project-structure.md` —— 验证：`grep -c 'newControl' SKILL.md` ≤ 1，`grep -c 'newControl' references/project-structure.md` ≥ 1
- [x] 4.5 5555 端口：`pitfalls.md` #28 留读数 + 指针；`SKILL.md` 两行合 1 —— 验证：`grep -c 'emulator-setup.md' references/pitfalls.md` ≥ 1
- [x] 4.6 logcat/双证据：`SKILL.md` #4 改指针；`methodology.md` 留原则句；`pitfalls.md` #16 留噪音判读 —— 验证：`grep -c 'debugging.md' SKILL.md` ≥ 1
- [x] 4.7 `i.sss` 语义：`pitfalls.md` #6、`mjava-guide.md` §作用域、`recipes.md` §持久化 各压成 1 行 + 指针 —— 验证：`grep -c 'iapp-i-reference.md' references/pitfalls.md references/mjava-guide.md | tr -d '\n'` 两处各 ≥1
- [x] 4.8 图标：`project-structure.md` §icon.png 压成 3 行 + 指针；`pitfalls.md` #21 只留史实；`SKILL.md` 三行合 1 —— 验证：`grep -c 'icon-guide.md' references/project-structure.md` ≥ 1
- [x] 4.9 打包版本读数：`delivery-guide.md` 版本表改指针指 `iapp-history.md` —— 验证：`grep -c 'iapp-history.md' references/delivery-guide.md` ≥ 1
- [x] 4.10 `i.call`：`modularization-guide.md`、`pitfalls.md` #14、`SKILL.md` 各 1 行指向 `mjava-guide.md` —— 验证：`grep -c 'mjava-guide.md' references/modularization-guide.md` ≥ 1
- [x] 4.11 提交 —— 验证：`git show --stat HEAD` 覆盖 4.1–4.10 的文件

## 5. 验收

- [x] 5.1 跑 `review_docs.py --fail-on blocker` 与 `check_portable.py` —— 验证：两条命令退出码 0、阻断 0
- [x] 5.2 抽查 5 组重复：同一结论在全库只命中主文件 1 处正文，其余为指针 —— 验证：逐组 `grep -rn` 计数写进完成说明
- [x] 5.3 汇报：改前改后行数、每组主文件、剩余「允许重复」（索引行/图例）—— 验证：汇报含三节

## Workflow follow-up

- 第二轮验收通过后，与第一轮一并归档；两轮都是一个主题（文档收敛），可合并成一次 archive 说明。
