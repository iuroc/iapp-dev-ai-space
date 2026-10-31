# 四类检查清单（逐项）

每条给：**症状** → **扫描** → **替换/统一方向** → **风险** → **验收**。
矩阵状态引用 `.claude/skills/iapp-development/references/material-components.md`（材料 1.13.0 / API 34）；
BeanShell 边界引用 `.claude/skills/iapp-development/references/mjava-guide.md`。

---

## 0. 前置（不做完不算审阅）

| 步 | 动作 | 停下条件 |
|---|---|---|
| 0.1 | `git -C <工程根> rev-parse --short HEAD`，记录基线 | 拿不到基线就在报告顶部写「无基线，行号仅本次有效」 |
| 0.2 | `wc -l <工程根>/src/*.mjava`，模块数与总行数进报告 | — |
| 0.3 | `python .claude/skills/iapp-development/scripts/check_mjava.py <工程根>/src` | **退出码非 0 就停**：先修语言级错误，再谈质量 |
| 0.4 | 读三个「事实源」模块（若存在）：`theme.*`（token）、`widgets.*` / `ui.*`（统一工厂）、`store.*`（持久化入口） | 没有 token 模块时，STYLE 一类的「统一目标」只能写成建议 |

判读顺序固定：**REUSE → DUP → STYLE → STATE**。先定「该不该自己写」，再谈「写得统不统一」；
反过来会把大量合法自绘报成样式问题。

---

## 1. REUSE：复用缺失

### 判定三问（全 yes 才报）

1. 需求行为在支持矩阵里是 ✅ 或 ⚪（⚪ 需补内容，仍算可用）？
2. 用库的参数 / 主题 / tint 能达到同一视觉，不需要重画？
3. 工程里 ≥2 处能共用同一工厂（或至少同一种装配）？

任一为 no，写进报告的「已排除 · 合法自定义」，附一行理由。

### 逐项

| ID | 症状（扫描命中） | 替换方向 | 风险 / 边界 | 验收点 |
|---|---|---|---|---|
| R-01 | `View` + `GradientDrawable` 拼的确定/不确定进度条、`setPadding`/宽度百分比算条长 | `LinearProgressIndicator` ✅；`setProgressCompat(int,int)`；不确定态 `setIndeterminate(true)` | `setIndicatorColor` 是 `int...`：**必须传 `new int[]{c}`**，单值会 `Method not found` 并中断整段 | 0/50/100% 三档下条长与父容器内容宽一致（现自绘常拿 `ui_screenW()` 算，撑满后被裁） |
| R-02 | 手写 `boolean on` + 改字色/字重 + 换背景的「选中态」循环 | 两个以上互斥选项 → `MaterialButtonToggleGroup` + `MaterialButton` ✅；标签型 → `ChipGroup`+`Chip` ⚪ | ToggleGroup 子按钮样式要逐个设；BeanShell 不能继承，没法写子类化 group | 切换后仅一项选中；重复点当前项不重建整页 |
| R-03 | 用 `LinearLayout` 横排 + 点击切页做分类栏 | `com.google.android.material.tabs.TabLayout` ✅（mjava 里用全类名，短名是 iApp 封装） | ppt 声明 `TabLayout` 已实测排除（见 pitfalls #7），只能 mjava 建 | 选中下划线位置随文案宽度、横向可滚、无障碍朗读不丢 |
| R-04 | `new EditText` + 手调 hint/textColor + 自己改背景 | `TextInputLayout` + `TextInputEditText` ✅；或 `SearchBar` ✅（运行期） | TIL 必须直接包 TIE，子控件用 `til.getContext()`；`SearchBar` 只能 mjava 建（进 ppt 会崩设计器） | 输入、清空、键盘弹出时内容不被遮；失败/空结果在同一容器内呈现 |
| R-05 | `TextView` + `GradientDrawable` 描边 + `RippleDrawable` 拼按钮 | `MaterialButton` ✅：`setCornerRadius` / `backgroundTintList` / `setStrokeWidth` + `setStrokeColor(ColorStateList)` | `setStrokeColor` **只有 `ColorStateList` 重载**，传 int 会中断载入事件 | 描边宽度/颜色、圆角、按压涟漪与其它按钮一致；禁用态可辨 |
| R-06 | 四角 `GradientDrawable` 当卡片 | `MaterialCardView` ✅（`setContentPadding` / `cardCornerRadius`） | 默认带 elevation，纸感主题需 `setCardElevation(0)` + 底色 tint | 卡片圆角/内边距/阴影三页一致 |
| R-07 | `new View` + `setBackgroundColor` 当 1px 分割线 | `MaterialDivider` ✅ | — | 分割线粗细与 inset（是否通栏）一致 |
| R-08 | 自写遮罩 + 抓手 + 拖动跟踪 + 收起动画 | `BottomSheetDialog` ✅（拖拽/遮罩/返回键/层级都归库） | 内容要能滚用 `NestedScrollView`，`ScrollView` 会让抽屉一拖就关；底色别用 `setBackgroundColor`，会丢圆角 | 内容滚到顶才收起；深色主题无白帧；返回键先关面板 |
| R-09 | 自写侧滑层 + 遮罩 | `DrawerLayout` ✅ + 面板（`NavigationView` ⚪ 需 menu） | **必须包住内容当根**，当全屏浮层会吞点击（pitfalls #41）；嵌套树表达不了就只复用 DrawerLayout | 关抽屉后正文与底栏点击正常 |
| R-10 | 手写 `HashMap` + 计数/时间淘汰的缓存 | `android.util.LruCache` ✅ | 不能重写 `sizeOf`（继承类），只能按条数；键要含全部影响结果的参数（w/h/fsize/段起点） | 来回翻页命中缓存（日志无重复请求）；条目数封顶后旧段被淘汰 |
| R-11 | 自绘 Toast/对话框/行内提示条 | `Snackbar` / `MaterialAlertDialogBuilder`（不是 View，mjava 直接调） | 与页面内联的状态块不冲突：全局反馈用 Snackbar，内容区失败仍走三态块 | 连续触发不叠加、不遮挡底部主按钮 |
| R-12 | 手写「每 N 个一行」的网格、手写复用池 | `RecyclerView`（adapter 需编译成 dex）；或 `GridView` + `SimpleAdapter` + `ViewBinder`（接口可匿名实现） | **没有 dex 时手写网格是合法自定义**，但要登记；`SimpleAdapter` 能否承载「封面+两行文字」先做最小探针 ❓ | 长列表滚动不重建全部子 View；滚动位置在切分类后可恢复 |
| R-13 | 自绘渐变、玻璃、圆角面 | 无 M3 等价物 → 合法自绘，但要求**参数化 + 命名**（如 `ui_round` / `ui_stroke` / `ui_glass`） | 同一效果出现三套手写参数即转 STYLE | 同一视觉效果的调用点参数一致 |

### 本类最常见的误报

- 统一图标用 Canvas 现画：库无等价物，报它只会得到「没有替代品」。
- `LinearProgressIndicator` 已在用，旁边还有一条自绘条：要报的是**剩下那条**，不是整个模块。
- 组件在矩阵里是 ❌（如 `Carousel` 被裁剪）：不能建议换，只能记「无解，保持现状」。

---

## 2. STYLE：样式不统一

只比较**同一语义角色**。先列出工程的角色表（没有就自己归纳），再逐角色取值。

| 角色 | 扫描 | 判为不统一的阈值 | 统一目标 |
|---|---|---|---|
| 字号阶梯 | `grep -ohE 'ui_text\([^,]+, *[0-9]+,' *.mjava` | 同一角色 ≥2 个值；全工程 >5 个不同值 | token getter（正文/次要/标题/大标题）或统一工厂参数 |
| 间距刻度 | `grep -oh 'ui_dp([0-9]*)' *.mjava \| sort \| uniq -c` | 页边距出现两套（如 16 vs 20）且无层级理由 | 4/8/12/16/20/24 取一套；页边距单独定义 |
| 圆角 | `grep -n 'setCornerRadius(ui_dp(' *.mjava` | 同一控件类型两个半径（chip 20 vs 22） | 按控件类型定：chip / card / 按钮 / 面板 各一个值 |
| 图标盒与线宽 | `grep -n 'ic_make(' *.mjava` | 同一位置两套盒尺寸（24 vs 18 vs 28）或线宽不一致 | 统一 `ic_make(name, sizeDp, color)` 的 size 枚举 |
| 页头结构 | `grep -n 'wg_header' *.mjava` | 页头高度/左右内边距不同；**返回键在不需要的页面出现** | 一种页头工厂 + 显式 `showBack` 开关 |
| 按压反馈 | `grep -n 'RippleDrawable\|wg_ripple' *.mjava` | 同尺寸控件涟漪半径不同，或有的控件无反馈 | 统一 `wg_ripple` / `wg_rippleFill` |
| 三态（加载/空/错误） | `grep -n 'wg_message\|Gravity.CENTER' *.mjava` | 同一语义（空结果）一页用统一块、一页用手搭文本 | 一个 `wg_state(kind, …)`，三态同款 |
| 遮罩/透明度 | `grep -n 'setScrimColor\|#52\|#1F\|#14' *.mjava` | 同类遮罩两个 alpha | token 里给 `th_scrim()` |
| 主/次按钮 | `grep -n 'wg_rippleFill' *.mjava` | 高度/圆角/字色两套 | 主按钮 1 种、次按钮 1 种，参数只留文案 |
| 文案口径 | 人工：`"加载中"` / `"载入中…"` / `"正在载入…"` | 同一状态三种说法 | 统一状态词表 |

### 判定细则

- **算**：同一角色、同一层级、用户能在相邻页面同时看到，值不同。
- **不算**：层级不同（列表封面 vs 详情封面）、平台限制（阅读器 WebView 内 CSS）、
  已登记的主题分支（纸 / 夜两套色本来就不同）。
- 修复方向优先「收敛到 token / 工厂」，**不建议**在报告里直接给某个字号拍板——那是设计决策，
  报告只给出「候选值与影响面」，由用户选。

---

## 3. DUP：重复未封装

| ID | 症状 | 扫描 | 判据 | 处理方向 |
|---|---|---|---|---|
| D-01 | 两个模块只差数据源（图书/期刊、两个详情页） | 对同名前缀模块 `diff` 方法名列表：`grep -n '^public' a.mjava b.mjava` | 方法一一对应且函数体近似 → 应修 | 抽 `listctrl` / `wg_detailPage(cfg)`，参数化：分类表、网络方法、字段名、详情目标 |
| D-02 | 每个入口都重复同一组 `i.fn` | `grep -n 'i.fn("' *.mjava`；`grep -n 'void .*_wire'` | 同一集合出现 ≥3 次 → 应修 | 一个 `app_wire(kind)` 或按依赖分组的 `wire_ui()` / `wire_data()`；`importAll()` 仍留在各 public 入口第一行 |
| D-03 | 同一工厂块复制（封面、列表行、chip） | `grep -n 'coverBox\|substring(0, 1)'`、`grep -n 'wrap.addView(row'` | ≥3 处 → 应修；2 处 >15 行 → 应修 | 抽 `wg_cover(json, w, h, field)`、`wg_listRow(...)`；字段名差异用参数 |
| D-04 | 文件文本读取/写入模板 | `grep -n 'new InputStreamReader\|new FileOutputStream'` | ≥2 处相同循环 → 应修 | 一个 `io_readText(File)` / `io_writeText(File,String)`；BeanShell 无 try-with-resources，`finally` 关流 |
| D-05 | `new Thread` + `runOnUiThread` 模板 | `grep -n 'new Thread(new Runnable()'` | ≥3 处同构 → 应修 | 抽 `bg_load(callable-ish, onOk, onErr)`；回调参数用接口（可匿名实现）或 `i.sss` 传结果 |
| D-06 | 每个模块抄一份 `xxx_flag(String key)` / `getInt` | `grep -n '^public .*_flag(String key)'` | 完全相同的实现 ≥2 份 → 应修 | 统一放 `ui_` 或 `store_` 一个读取器 |
| D-07 | 三态拼装各写一遍 | `grep -n 'removeAllViews' *.mjava` 后人工看邻域 | ≥3 处 → 应修 | 一个 `wg_state(host, kind, ...)` |
| D-08 | 排序/JSON 转换手写 | `grep -n 'JSONArray nw\|插入排序\|for (int j = 0; j < '` | 2 处以上 → 建议 | `Collections.sort` + 匿名 `Comparator`（接口可用）；或统一工具方法 |

### 合并 vs 保留

- 合并后需要 **≥3 个 if 分支** 才能覆盖差异 → 保留两份，报告里写「差异将扩大，不再合并」。
- 合并会改变调用时序（例如列表页的注册/重建顺序）→ 先做最小探针，再列入下一轮。
- 只差字符串（标题、字段名）→ 一定合并。

---

## 4. STATE：状态与结构

| ID | 症状 | 扫描 | 判据 | 处理方向 |
|---|---|---|---|---|
| S-01 | `i.sss` 键散落、无登记 | `grep -oh 'i\.sss("[^"]*"' *.mjava \| sort \| uniq -c \| sort -rn` | 同一键在 ≥2 模块出现，或全工程键数 >10 且无表 → 应修 | 建 `keys.mjava`（只返回常量）+ 工程内一页键表（用途/写方/读方/类型）；拼错在 BeanShell 里不报错 |
| S-02 | `ui_reg` 句柄名手写 | `grep -n 'ui_reg("' *.mjava` | 同类句柄命名不一致（`x.grid` vs `x.list`）→ 建议 | 命名 `<模块>.<角色>`；页面重建时显式重注册 |
| S-03 | 页面 A 直接调页面 B 内部方法 / 写别人的状态键 | `grep -n 'i\.fn("home")\|i\.fn("reader")' *.mjava` + 人工 | 跨模块只该调对外入口；写别人的键 → 应修 | 抽 `openReader(...)` / `repaintHome()` 这类显式入口；数据通过参数或本模块键 |
| S-04 | 每个入口的 `i.fn` 集合不一致（漏加载） | `grep -c 'i\.fn("' *.mjava` + 逐入口核对 | 同一模块不同入口加载集合不同 → 应修（未加载先调用会 `Command not found` 且 catch 不住） | 入口统一走 wire；回调里跨模块调用前也要 `i.fn` |
| S-05 | 魔法数值 | 字号/间距/圆角/超时/条数/页大小 | 同一语义 ≥3 处字面量 → 应修 | token 或常量 getter（网络分页参数尤其要单一来源） |
| S-06 | 死代码、死参数、不可达分支 | `grep -n 'return;'` 后人工看邻域；IDE 不可用就通读短模块 | 永远到不了的分支 / 形参未使用 → 建议（会误导后续维护） | 删；先确认没有未知入参兜底 |
| S-07 | 同名方法相互覆盖 / getter 撞工厂 | `grep -n '^public' *.mjava \| cut -d' ' -f3 \| sort \| uniq -d` | 同模块重名 → 阻断（后者静默覆盖，或自我递归 `StackOverflowError`） | 令牌 getter 与视图工厂必须不同名 |

---

## 5. 定级与确认

### 定级只看两个问题

1. **用户现在能不能看见错？**（错位、死按钮、数字不对、白屏）→ 阻断候选。
2. **不修会不会越长越大？**（复制第 3 份、样式第 2 套、键第 5 处）→ 应修候选。
两者都不成立，最多建议。

### 确认一条发现的三步

1. **命中**：grep 给出 `文件:行`，贴进报告。
2. **读邻域**：往上 20 行确认它属于哪个角色/哪个页面；确认没有已登记的豁免理由。
3. **定影响**：能静态判断的写「静态可判」；需要上屏的写验收点并标 ❓「待设备实测」。

### 不能确认时

写「❓ 待验」+ 一条最小探针做法（哪个页面、点什么、看什么日志/截图），
不要把推测写成结论——与知识沉淀同一套级别制度。

---

## 6. 报告交付自检

- [ ] 基线 sha 与扫描命令都在报告里
- [ ] 每条发现五要素齐全（文件:行 / 现状 / 替换 / 风险 / 验收）
- [ ] 「已排除」节列出了至少 3 条豁免项及理由（证明不是照抄清单）
- [ ] 没有改任何工程文件（`git -C <工程根> status` 保持干净）
- [ ] 阻断项按「用户可感知错误」逐条复述，不是「建议重构」
- [ ] 汇总表能与明细对得上（数量、级别一致）
