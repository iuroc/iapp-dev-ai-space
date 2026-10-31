# 校准样本

目的：对齐「什么该报、什么不该报、报多重」。样本取自一个真实 iApp 阅读类工程
（19 个 `.mjava` / 约 5.5k 行，有 token 模块、公共组件模块、列表/详情/阅读三套页面），
只作尺度参照——**数值与行号会随工程演进而失效，不要当规范**。

> 读取口径：样本按「读取时的 worktree」记录，含未提交改动。定位优先用**函数名/符号**，
> 行号只是当时的辅助；同一工程里已经修好的项也保留在文末作对照，避免重复报。

---

## 1. 工程画像（审阅前先建立）

| 事实源 | 存在时给审阅带来的便利 |
|---|---|
| `src/theme.mjava` | 只有颜色 token（`th_bg` / `th_ink1` / `th_accent` …），**没有字号、间距、圆角 token** → STYLE 类只能报「分叉」，统一值留待设计决策 |
| `src/widgets.mjava` | 页头、图标按钮、骨架、扫动线、空/错态、发丝线、涟漪都已有工厂 → 不在工厂里的同类块优先怀疑 DUP |
| `src/ui.mjava` | 建树基础：`ui_dp` / `ui_col` / `ui_row` / `ui_reg` / `ui_insets` → REUSE 判定要把「已有工厂」算进去 |
| `src/store.mjava` | 持久化唯一入口 → 散落文件读写即 STATE/DUP |

判读顺序：REUSE → DUP → STYLE → STATE。本工程先判 REUSE，才能发现「抽屉/面板/分类栏/缓存
已用库，剩下几处自绘」这类真正的复用缺失，而不是把所有自绘一刀切。

---

## 2. REUSE 样本

### 2.1 该报：手写底部四 Tab

- 位置：`src/home.mjava` `navItem()`（读取时 104-131）
- 现状：4 个 `LinearLayout` 均分，图标 + 文案 + 选中色 + `Typeface.BOLD` + 手调涟漪；
  切 Tab 时 `removeAllViews` 全量重建。
- 可换成：`BottomNavigationView`（矩阵 ✅，需 menu 项；Canvas 图标包成 `BitmapDrawable` 后 `setIcon`）。
- 判定：三问全 yes（矩阵 ✅ / 参数可达 / 需要与选中态工厂共用）→ **应修**。
  若坚持不用库，也必须抽成 `wg_tabBar(items, selected, onPick)`，不能留在页面里。
- 风险：menu 项只能程序化 `getMenu().add`；M3 观感要手动设 `itemIconTintList` / `itemTextColor`。
- 验收：4 项等高、选中项变色且加粗、点击切换 Tab、返回不崩。

### 2.2 该报：确定进度条自绘且长度算错

- 位置：`src/lib.mjava` `lib_continueCard()`（读取时 173-190）
- 现状：`FrameLayout` 轨道 + `View` 条，长度 `ui_screenW() * ratio / 1000`；卡片左右各有 16dp 内边距，
  满进度时条超出内容区，约 90% 就顶满并被裁。
- 可换成：`LinearProgressIndicator`（✅，`setProgressCompat`，颜色传 `new int[]{c}`）。
- 判定：**阻断**——用户能直接看见进度提前满格。
- 验收：10% / 50% / 100% 三档截图，条右缘距卡片内容右缘 0±1dp。

### 2.3 该报：加载槽按钮手绘

- 位置：`src/shelf.mjava` `sh_moreSet()`（读取时 189-241）
- 现状：`TextView` + `GradientDrawable` 描边 + `RippleDrawable` 遮罩 + `try/catch` 兜底，
  四态（可加载 / 载入中 / 已到底 / 失败）靠 if 改字色与描边色。
- 可换成：`MaterialButton`（✅）：`setCornerRadius`、`backgroundTintList`、
  `setStrokeWidth` + `setStrokeColor(ColorStateList)`。
- 判定：**应修**（复用缺失 + 四态各一套手写分支）。
- 风险：`setStrokeColor(int)` 不存在，传 int 会中断载入事件。

### 2.4 该报：阅读器 chip 手写选中态

- 位置：`src/reader.mjava` `rd_chip()` / `rd_chipStyle()`（读取时 652-681 / 618-633）
- 现状：每行 3-4 个 `TextView`，选中换字色 + `wg_rippleFill`，取消换 `wg_ripple`；
  高 40dp / 圆角 20dp。
- 可换成：`MaterialButtonToggleGroup` + `MaterialButton`（✅，`setSingleSelection(true)`）。
- 判定：**应修**。同工程的 `src/mine.mjava` `mine_themeToggle()` 已用这套（高 44dp / 圆角 22dp），
  两份对照正好是「统一工厂」的必要性证据。
- 风险：ToggleGroup 的选中态由库维护，子按钮描边/字色要逐个设；本环境不能继承 group 写子类。

### 2.5 该报：搜索输入框手搭

- 位置：`src/search.mjava` `build()`（读取时 81 起的 `new EditText`）
- 现状：`EditText` + 手调 hint / textColor / `setBackgroundColor(透明)` / 内边距；
  清空按钮、聚焦态、错误态都要自己补。
- 可换成：`TextInputLayout` + `TextInputEditText`（✅），或 `SearchBar`（✅ 运行期，只能 mjava 建）。
- 判定：**应修**；若只想要「无装饰输入行」，至少把配置收进 `wg_searchBar(...)` 工厂。
- 风险：TIL 必须直接包 TIE，子控件用 `til.getContext()`；`SearchBar` 进 ppt 会崩设计器。

### 2.6 不该报（合法自定义）

| 位置 | 为什么不算 |
|---|---|
| `src/icon.mjava` `ic_make()` | Canvas 线稿图标，库无等价物；统一 24dp 盒 / 1.5dp 线宽是正确的实现 |
| `src/ui.mjava` 的 `ui_insets` | `setOnApplyWindowInsetsListener(匿名实现)` 会让整份模块 Parse error |
| `src/store.mjava` 文件 KV | 多工程共用 `getFilesDir()`，`SharedPreferences` 不适用 |
| `src/toc.mjava` 目录树缩进/展开 | `NavigationView` 的 menu 表达不了嵌套树；外层已复用 `DrawerLayout` |
| `src/shelf.mjava` 手写三列网格 | 无 dex 时 `RecyclerView.Adapter` 不可用；登记为已知代价（有 dex 时可升级） |

---

## 3. STYLE 样本

### 3.1 该报：正文同一角色两个字号

- 位置：`src/bookdetail.mjava` `build()` 的简介（读取时字号 17）vs
  `src/magdetail.mjava` `build()` 的简介（字号 15）。
- 判定：**应修**（同一「正文」角色、同一层级、相邻页面）。
- 验收：两个详情页简介字号与行距观感一致（值由设计定，报告只给候选）。

### 3.2 该报：页边距两套

- 位置：16dp —— `src/lib.mjava` 的 body、`src/search.mjava` 的结果列表；
  20dp —— `src/mine.mjava` 的 body、`src/bookdetail.mjava` / `src/magdetail.mjava` 的 body。
- 判定：**应修**（无层级理由的横向页边距分叉）。
- 注意：Tab 内页与独立页可以不同，但要在 token 里命名（如 `th_pagePadTab` / `th_pagePadDetail`）。

### 3.3 该报：三态各写各的

- 位置：统一块 —— `src/book.mjava` / `src/mag.mjava` 用 `wg_message`；
  手搭 —— `src/search.mjava` 的「没有找到」块与 `sr_placeholder()`、
  `src/magdetail.mjava` 的「暂无往期」纯文本、`src/reader.mjava` 的 `rd_status()` 居中文本。
- 判定：**应修**（同一语义两套实现）。统一 `wg_state(host, kind, …)`。
- 验收：空 / 错 / 载三态在五处的字号、间距、可重试性一致。

### 3.4 全工程读数（用于定阈值，不是判决）

- 字号字面量：13sp × 23、15sp × 15、17sp × 9、20sp × 3 —— 数值本身是阶梯，问题是**没有角色名**。
- 间距：`ui_dp(8)` × 31、`ui_dp(16)` × 27、`ui_dp(20)` × 24、`ui_dp(24)` × 18、`ui_dp(12)` × 18。
- 圆角：2（封面）、4（卡）、20（面板/chip）、22（chip）、28（主按钮）—— 同角色两个值才算问题。

---

## 4. DUP 样本

### 4.1 该报：两个列表页只差数据源

- 位置：`src/book.mjava`（250 行）与 `src/mag.mjava`（246 行）。
- 对应关系：`book_flag`/`mag_flag`（逐字相同）、`*_page` / `*_switch` / `*_more` / `*_load` /
  `*_render` / `*_reload` / `*_open` 一一对应。
- 判定：**应修**。抽 `listctrl_page(cfg)`：分类 id/名、网络方法、字段映射（title/name、
  author/ISSN、cover/coverPath）、`isMag`、详情目标。
- 风险：合并后若长出 ≥3 个分支就停止合并；先合并「骨架 + 翻页 + 三态」，字段映射留参数。
- 验收：两个 Tab 的首屏 / 切分类 / 第 2 页 / 断网 / 空分类截图逐项一致。

### 4.2 该报：封面块复制 5 份

- 位置：`src/shelf.mjava` `sh_cell()`、`src/lib.mjava` `lib_picks()`、
  `src/search.mjava` `sr_row()`、`src/bookdetail.mjava` `coverOf()`、
  `src/magdetail.mjava` `coverOf()`。
- 现状：完全同一骨架（占位底色 + 首字 + `ImageView` + `i.us`），差异只有尺寸、首字字号、字段名。
- 判定：**应修**（≥3 处）。抽 `wg_cover(json, wDp, hDp, field)`。
- 验收：五处外观不变；无封面时仍显示首字占位；封面加载失败不露灰块。

### 4.3 该报：文件读循环 6 份

- 位置：`src/store.mjava`（2 处）、`src/indexer.mjava`（3 处）、`src/net.mjava`（1 处，追加换行的变体）。
- 判定：**应修**（≥3 处）。抽 `io_readText(File)`；BeanShell 无 try-with-resources，抽函数时保留 `finally` 关流。
- 验收：连续搜索/翻页 50 次不崩，日志无文件句柄错误。

### 4.4 该报：`wire()` 与入口加载重复

- 位置：`src/lib.mjava` `lib_wire`、`src/mine.mjava` `mine_wire`、`src/reader.mjava` `rd_wire`、
  `src/toc.mjava` `toc_wire`、`src/magdetail.mjava` `md_wire`、`src/search.mjava` `sr_wire`、
  `src/book.mjava` `book_wire`、`src/mag.mjava` `mag_wire`；外加各自 `first/second/again` 里再写一遍
  （全工程 `i.fn` 调用：`reader` 26 次、`home` 18 次）。
- 判定：**应修**。抽 `wire_ui()` / `wire_data()`，按依赖分组；差异（`net` / `store` / `indexer`）走参数。
- 风险：`importAll()` 必须留在各 public 入口方法体第一行；未加载先调用会 `Command not found` 且 `catch` 不住。

---

## 5. STATE 样本

### 5.1 该报：`i.sss` 键散落

- 读数：19 个不同键；高频 `reader.title` 5、`reader.surl` 5、`detail.book` 5（3 写 1 读 1 注释）、
  `reader.author` 4、`ix.running` 4、`ct.cur` 4、`sh.pick` 3、`detail.mag` 3、`jy.tk.<surl>` 3；
  分布 9 个以上模块。
- 判定：**应修**（拼错不报错，静默读到 null）。
- 方向：`keys.mjava` 只返回常量 + 工程内一页键表（用途 / 写方 / 读方 / 类型）。

### 5.2 该报：隐式契约 `sh.pick`

- 位置：写 `src/shelf.mjava` `sh_cell()`；读 `src/book.mjava` `book_open()`、`src/mag.mjava` `mag_open()`。
- 现状：写方塞 `JSONObject.toString()`，读方不知道格式；靠全局键传参。
- 方向：`onPick` 改为带参接口（匿名实现接口可用）或通过 `setTag` 取。

### 5.3 该报：职责越界与死代码

- `src/home.mjava` `tabPage()` 末尾（读取时 152-171）：四个分支都已 return，末尾占位页不可达，
  还复制了一份页头逻辑。
- `src/cattabs.mjava` `ct_reselect()`：`labels` / `onPick` 形参未使用。
- `src/search.mjava` `sr_row()`：局部 `isMag` 未使用。
- `src/mine.mjava` `home_repaint()`：页面互相调内部方法的中间层，能删则删，保留就注释清用途。
- 判定：**建议**（不改变当前行为），但会误导后续维护。

---

## 6. 已通过项（证明扫描不误报）

| 模块 | 结论 |
|---|---|
| `src/cattabs.mjava` | 分类栏 = `TabLayout`（`MODE_SCROLLABLE`）；逐项改字重属合法自定义 |
| `src/widgets.mjava` `wg_sweepTrack()` | 不确定进度 = `LinearProgressIndicator`，且 `setIndicatorColor(new int[]{…})` 写法正确 |
| `src/reader.mjava` `rd_sheetShow()` | 外观面板 = `BottomSheetDialog`；抓手只是视觉暗示，拖动归库 |
| `src/toc.mjava` `toc_wrap()` | 抽屉 = `DrawerLayout`，且按 pitfalls #41 包住内容当根 |
| `src/net.mjava` `net_cache()` | 分段缓存 = `android.util.LruCache`，按条数淘汰，未重写 `sizeOf` |
| `src/mine.mjava` `mine_themeToggle()` | 主题切换 = `MaterialButtonToggleGroup`，选中态归库 |
| `src/shelf.mjava` `sh_lineH()` | 行高用 `TextView.getLineHeight()` 实测，不是手算魔法数 |
| `src/icon.mjava` | 线稿统一 24dp 盒 / 1.5dp 线宽 / 圆头端点 |

这 8 项要写进报告的「已通过」，它同时是「本轮确实读了代码」的证据。

### 已修复对照（不要重复报）

| 位置 | 修前 → 修后 | 校准价值 |
|---|---|---|
| `src/widgets.mjava` `wg_header()` | 无条件画返回键 → `backRun == null` 时不画 | 「用户可感知的死按钮」= 阻断的典型 |
| `src/mine.mjava` 主题切换 | `TextView` 手写选中态 → `MaterialButtonToggleGroup` | 同一角色的第 2 套实现，是 REUSE 应修的范本 |
| `src/net.mjava` 分段缓存 | `LinkedHashMap` + `ArrayList` 手写 LRU → `android.util.LruCache` | 手写淘汰逻辑没有理由，库一行替换 |
| `src/widgets.mjava` `wg_sweepTrack()` | `TranslateAnimation` 手写扫动 → `LinearProgressIndicator` | 「行为已有组件」就不该自己接动画 |

> 审阅时先看 worktree：只看 commit 历史会把已修项再报一遍。

---

## 7. 尺度口诀

- 看见**同一个按钮/条目/页头**造了两套 → DUP 或 STYLE，至少应修。
- 看见**库组件已在用**、旁边还有同语义自绘 → REUSE，应修。
- 看见**用户能点出错觉**（死按钮、进度满格、点击无响应）→ 阻断。
- 看见**单处、只影响可读性** → 建议，不排期。
- 拿不准是否该复用 → 先查矩阵，再问「换库后视觉会变吗、能不能接受」，答不上就标 ❓ 写验法。
