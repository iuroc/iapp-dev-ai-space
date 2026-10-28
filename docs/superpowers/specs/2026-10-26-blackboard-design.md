# 课堂黑板（画板）设计

日期：2026-10-26
环境前提：iApp 5.0.1013、裕 3 模式、LDPlayer9 / Android 9（API 28）、1080×1920 / density 3.0，**横屏使用**
用途：老师上课当黑板，整节课手写

## 1. 意图

做一块能顶替实体黑板的画板，同时把它当作一次**对 SKILL 绘制链路能力的压力测试**。

成功不是"代码写完"，而是三件事同时成立：

1. 老师在设备上能连续写一整节课：落笔出墨、跟手、不断线；能换笔、擦、撤销/重做、清空；杀掉进程重开板书还在；能导出文件带走、再导入。
2. 每个新踩到的行为都有**双证据**：logcat 原文 + 屏幕现象。
3. 探针结束后 SKILL 与 docs 已回填；新缺口有明确归属（尤其 Canvas/Bitmap/多点触控/布局时机这些目前覆盖薄的地方）。

## 2. 目标 / 非目标 / 反目标

### 目标

- 全屏深色画布，手指（或鼠标）书写，横屏布局。
- 笔：4 色（白/黄/红/蓝）× 3 档粗细（细/中/粗）。
- 像素级橡皮（能擦掉半个字），不是整笔删除。
- 撤销 / 重做；清空（二次确认，可撤销一步）。
- 自动持久化：每次落笔结束即写盘（节流），杀进程重开恢复。
- 导出备份到 `/sdcard/Download/Blackboard/`：`.board`（可再导入、保留笔迹）+ `.png`（可直接看/发群）。
- 导入：列出该目录下的 `.board`，选择后替换当前板（二次确认）。
- 内置自检：序列化往返、撤销/重做栈、缩放换算、文件往返、重放耗时，logcat 输出 PASS/FAIL。
- 产出一份"文档缺口清单"，并当场回填。

### 非目标

- 翻页/多块板/无限画布；图片插入、文字、形状、激光笔。
- 双指缩放/平移、压感、倾斜笔锋。
- 云同步、系统分享 Intent、从任意目录选文件（本轮只扫固定导出目录）。
- 打包 APK 与安装（本轮只到开发模式运行；打包留作后续）。
- 硬件级手掌防误触（只做单指跟踪，见 §7.3）。

### 反目标（即使能写也算失败）

- 在 `.iyu` 里写 `call`/`addv` 以外的裕语言函数。
- 把状态放在模块级变量里跨 `call` 使用。
- 每个 `ACTION_MOVE` 全量重绘整块画布，导致掉笔/断线。
- 每个 `ACTION_MOVE` 写盘。
- 用 bind mount 投递，或改完源码 `am force-stop` iApp 打断用户正在看的工程。
- 遇到文档没写的 API 直接猜着写，不先探针。
- 为了"顺手"把撤销做成每笔存整张位图快照，一次性吃光内存。

## 3. 约束

| 约束 | 来源 |
|---|---|
| 入口 `src/mian.iyu`；`src/` 只放 `.iyu` / `.mjava` | SKILL |
| `.iyu` 只用 `call` / `addv` | SKILL 白名单 |
| `.mjava` 由 BeanShell 解释：禁 `final`、具名 class、`0xFF`、可变参数、`bsh.*` | SKILL 铁律 |
| 匿名**接口**实现可用；匿名**类**会中断事件 | SKILL（API 28 实测） |
| 模块级变量跨 `call` 必丢；跨 call 状态放 `i.sss` 或控件 `setTag` | SKILL |
| 自定义 `View` 子类写不了 → 用 `Bitmap + Canvas + ImageView` 绕开；子类化失败再走编译 dex | SKILL（BeanShell 限制） |
| 工程镜像直接写 `android-sync/ProjectApp/<包名>/`，即设备工程 | 工作区 CLAUDE.md |
| 改源码后不 `am force-stop` iApp，由用户关/开工程 | 工作区 CLAUDE.md |
| 目标 API 28；共享目录 `/sdcard/Pictures` ↔ `android-sync/` 已实测 | docs/runtime-env.md |
| `0xFF…` 这类 > `0x7FFFFFFF` 的十六进制字面量会让模块失效 → 颜色用 `Color.parseColor` 或负数 | SKILL（mjava-guide） |
| `getFilesDir()` 是宿主 iApp 的私有目录，**多个工程共用** → 存档名必须带工程前缀 | SKILL（recipes / pitfalls） |
| `i.sss` 每次「运行」重置，不只是进程结束 | SKILL（iapp-i-reference） |
| ppt 属性名是 `layout_weight`（写 `weight` 无效）；`alpha` 无效；`padding` 按 px 解析 | SKILL（iyu-guide） |

## 4. 工程与文件

新建工程：`android-sync/ProjectApp/com.demo.blackboard/`

```
com.demo.blackboard/
├── .project / AndroidManifest.xml / icon.png
├── files/ res/ sdk/ build.xml          # 由 iApp 首次打开生成
└── src/
    ├── mian.iyu        # 页面结构 + 点击事件（只 call）
    ├── board.mjava     # facade：init/layout/工具切换/撤销/清空/导出导入入口/自检
    ├── pen.mjava       # 画布：位图、画笔、笔迹模型、触摸、重放
    ├── store.mjava     # 序列化、内部存档、导出目录、PNG
    └── ui.mjava        # 工具栏选中态、对话框、Toast
```

**为什么这样拆**：`pen` 是纯绘制与输入，`store` 是文件，`ui` 是控件状态，`board` 只做编排。
跨模块用 `i.fn("模块名")` 加载进当前解释器，子模块方法统一前缀（`pen_` / `store_` / `ui_`）。
**每个 public 入口第一行 `importAll()`**；漏掉会 `Command not found` 且中断整个方法。

## 5. 绘制模型

### 5.1 为什么不用自定义 View

`.mjava` 由 BeanShell 解释，写不了继承类；自定义 `View` 的 `onDraw`/`onTouchEvent` 没有等价入口。
本轮采用**位图 + ImageView**：

- `Bitmap bmp` = 与画布控件同尺寸的 `ARGB_8888`，先填背景色。
- `Canvas c = new Canvas(bmp)`；落笔时直接往 `bmp` 上画，然后让 ImageView 刷新。
- 触摸用 `setOnTouchListener`（匿名接口，SKILL 已实测可用）。
- 如果 P1 证明硬件加速下内容刷新不可靠或太慢，再启用备选：把 `PenSurface` 编译成独立 dex 并用 `DexClassLoader` 加载（SKILL 有装载规范）；本轮不先做。

### 5.2 笔迹数据

每条笔迹：

```
int tool      // 1=笔 2=橡皮
int color     // ARGB
int widthPx   // 线宽（像素）
int[] pts     // x0,y0,x1,y1,... 画布像素坐标
```

- 进行中的笔迹单独维护，`ACTION_UP` 时并入 `strokes`。
- 撤销栈 = `strokes` 末尾弹出；重做栈 = 被撤销的笔迹。
- 新笔迹写入时清空重做栈。
- 清空 = 把整份 `strokes` 存进 `lastCleared`（只保留一层），清空后可撤销一次。
- **不设笔迹数量上限**（一节课 1000~3000 笔量级，内存可接受）；撤销靠重放，不存位图快照。

### 5.3 绘制与重放

- 落笔：`ACTION_DOWN` 画一个圆点；`ACTION_MOVE` 用 `drawLine` 增量画（圆头圆角），**不做全量重绘**。
- 重放（撤销/清空撤销/导入/启动恢复）：清背景，按笔迹逐条构造 `Path`（`moveTo` + `lineTo`）后 `drawPath` 一次画完。
  比逐段 `drawLine` 少一个数量级的 Canvas 调用。
- 重放耗时由 P8 实测（1000 / 3000 两档）；本轮不预先优化，只有 3000 笔重放 > 1s 才记档，并把"包围盒区域快照"留作后续方案。

### 5.4 刷新方式（探针决定）

`ImageView` 已 `setImageBitmap(bmp)` 后，直接改 `bmp` 内容再刷新有几种写法，P1 逐一测：

1. `iv.invalidate()`
2. `iv.setImageBitmap(bmp)`（重建 `BitmapDrawable`）
3. `iv.setImageBitmap(null)` + `iv.setImageBitmap(bmp)`
4. `iv.setLayerType(View.LAYER_TYPE_SOFTWARE, null)` 后再 `invalidate()`

判定：屏幕上的墨迹是否真的更新 + 单次刷新耗时。**默认用测出来最快且稳定的一种**，结果回填 SKILL。

### 5.5 尺寸变化

- 画布 `Bitmap` 尺寸 = 控件布局后的 `getWidth()/getHeight()`（P3 确认取值时机）。
- 尺寸一旦变化（旋转、分屏、全屏开关改变高度）：新建位图 → 用**统一比例** `s = min(newW/oldW, newH/oldH)` 把旧位图缩放后居中贴上（留白填底色）→ 所有笔迹坐标 `x' = x*s + ox`、`y' = y*s + oy`，线宽 `*s` → 全量重写存档。
- 用统一比例而不是两轴各自拉伸：**字迹形状不变**，验收里的"比例正确"按这个口径判。
- 存档文件头记录坐标所依据的 `w h`；导入到不同尺寸画布时按同样规则等比缩放居中。
- 开发机是 1080×1920 手机，横屏为 1920×1080；**不锁方向**（开发模式锁方向会连带锁住宿主 iApp 编辑器），靠上面的自适应处理旋转。

## 6. 界面（横屏）

### 6.1 结构（`mian.iyu`）

```
root LinearLayout (vertical, #101418)
├── bar LinearLayout (horizontal, height=52dp, #161B21, padding 4dp)
│   ├── 白 黄 红 蓝        # 4 个颜色格（TextView，layout_weight=1）
│   ├── 粗细               # 循环 细/中/粗，button 文案跟着变
│   ├── 笔 橡皮            # 两个互斥工具
│   ├── 撤销 重做
│   ├── 清空
│   └── 文件               # 点开对话框：导出 / 导入 / 全屏
└── canvas ImageView (width=-1, height=0, layout_weight=1, #101418)
```

- 单行工具栏，共 11 个等宽格；横屏 1920px 下每格约 64dp，够手指点。
- 颜色格用文字「白/黄/红/蓝」，文字色即该颜色；选中的格子加深色底 + 亮边框。
- 「笔/橡皮」「粗细」用文字高亮表示选中态。
- 所有点击在 `.iyu` 里绑 `clicki` → `call(null,"mjava","board.xxx", 参数…)`，静态结构不动态创建。
- 「文件」对话框用 `AlertDialog.Builder` + 三个按钮；「清空」「导入」都有二次确认。

### 6.2 配色

| 用途 | 色值 |
|---|---|
| 画布底 | `#101418` |
| 工具栏底 | `#161B21` |
| 工具未选 | 底 `#1E252D`，字 `#C7D2DE` |
| 工具选中 | 底 `#2D3A48`，字 `#FFFFFF`，边框 `#5AA9E6` |
| 白笔 | `#F5F7FA` |
| 黄笔 | `#FFD54F` |
| 红笔 | `#FF6B6B` |
| 蓝笔 | `#6BC5FF` |

粗细：细 = 2dp、中 = 5dp、粗 = 10dp；橡皮固定 28dp。

## 7. 输入

### 7.1 主路径

`canvas.setOnTouchListener(new View.OnTouchListener(){...})`，回调里调 `pen_touch(v, e)`。

- 只跟踪**第一个按下**的指针：`ACTION_DOWN` 记录 `pointerId`。
- `ACTION_MOVE` 用该 id 的 `findPointerIndex` 取坐标；越界（找不到）立即收笔。
- 其余指针（`ACTION_POINTER_DOWN` / 多指 MOVE）一律忽略，不改当前笔迹，也不提升为主指针。
- 收笔条件：`ACTION_UP`，或 `ACTION_POINTER_UP` 且抬起的就是跟踪指针（手指抬起、手掌还按着的场景）；`ACTION_CANCEL` 同样收笔。
- 收笔时**保留已画出的部分**（提交进模型并写盘），不回滚重绘——所见即所得，也避免半截笔迹丢失。
- 收笔后要等新的 `ACTION_DOWN` 才开始下一笔。
- 坐标直接用 `MotionEvent.getX(index)/getY(index)`（相对画布控件），与位图像素 1:1。

### 7.2 探针要求

P2 必须确认 BeanShell 下可用：`getActionMasked()`、`getPointerCount()`、`getPointerId(i)`、`findPointerIndex(id)`、`getHistoricalX/Y(i, h)`。
若 `getActionMasked` 不可用，退回 `getAction() & 0xFF`。
历史点（`getHistoricalX/Y`）能显著改善快速划线的连贯性，可用就接入，不可用则只画当前点。

### 7.3 手掌

V1 只做"只认第一根手指"，不主动取消笔迹（避免写字时手掌落下导致整笔消失）。
`getSize()` / `getToolType()` 的可用性顺手记录，但不作为验收项。

## 8. 状态与跨 call

- 运行时对象（`Bitmap`、`Canvas`、`Paint`、`strokes`、`redo`、`current`）放进一个 `HashMap`，挂在画布 `ImageView.setTag(...)` 上。
  - 控件实例在本次页面生命周期内稳定；`call` 结束后回调里 `findViewById(10).getTag()` 能取回（同 2048/card3d 的 `setTag` 用法）。
  - 每次回调先取 bundle，取不到就 `pen_rebuild()`（从存档恢复）。
- 工具选择（颜色/粗细/当前工具）放 `i.sss`：`bb.color` / `bb.width` / `bb.tool`。
- 不依赖模块级变量；不假设 `i.sss` 能存任意对象（P4 顺手验证，但不作为架构前提）。

## 9. 持久化

### 9.1 文件

内部存档：`activity.getFilesDir()/blackboard.board`（应用私有，无需权限）。
失败回退：`activity.getExternalFilesDir(null)/blackboard.board`。

### 9.2 格式

纯文本，一行一条笔迹：

```
v1 <w> <h>
A <color> <width> <tool>
S <tool> <color> <width> <n> <x0> <y0> <x1> <y1> ...
```

- `<w> <h>`：笔迹坐标当时对应的画布像素尺寸，用于导入/旋转时缩放。
- `A` 行：上次使用的颜色/粗细/工具。`i.sss` 每次运行都会重置，工具设置靠这一行跨次恢复。
- 坐标取整像素，颜色十进制 ARGB（`Color.parseColor` 返回的是负数，`Integer.parseInt` 能往返），线宽像素。
- **容错解析**：逐行读，遇到第一条坏行就停，保留此前解析成功的笔迹，日志 `BB load-truncated line=<n>`；0 字节/空文件按空板处理。
- 导入时 `.board` 若一行都解析不出来 → **中止导入、保留当前板**，Toast「文件损坏」，不清空。

### 9.3 写盘方式与时机

- **普通落笔只追加**：`FileWriter(f, true)` 追加一行 `S ...`，不在 UI 线程重写整份文件。
- **结构性变更**（撤销/重做/清空/缩放/导入/导出前）才全量重写。
- 全量重写走原子替换：写 `blackboard.board.tmp` → `renameTo(blackboard.board)`；失败再回退直接覆盖。
- 每次收笔后最多 1.5s 写一次（节流）；停笔后补一次延迟写。
- **不依赖生命周期回调**（事件存在，但开发模式可靠性待 P7 复核；即使有也不用它兜底）。
- 进程被杀的极端情况最多丢最后一笔；中途截断由 §9.2 的前缀容错兜住。

## 10. 导出 / 导入

### 10.1 位置

`/sdcard/Download/Blackboard/`（API 28 公共目录，文件管理器可见，可发微信/拷 U 盘）。
无写权限时回退 `activity.getExternalFilesDir(null)/Blackboard/`，Toast 提示实际路径。

### 10.2 导出

1. 先写内部存档。
2. 复制成 `<时间戳>.board`（`blackboard-20261026-143000.board`）。
3. 当前位图 `compress(PNG, 100, fos)` 成同名 `.png`。
4. 通知媒体库（`ACTION_MEDIA_SCANNER_SCAN_FILE`，若不可用就跳过，P6 验证是否必要）。
5. Toast 两个文件名。

### 10.3 导入

1. 列目录下 `*.board`，按修改时间倒序，`AlertDialog` 单选列表显示「文件名 · 大小」。
2. 选中后二次确认「替换当前板书？」。
3. 解析 → 坐标缩放到当前画布尺寸 → 替换 `strokes`、清空 `redo` 与 `lastCleared` → 重放 → 立即写内部存档。
4. 空目录/解析失败都有 Toast，不崩。

### 10.4 权限

`AndroidManifest.xml` 加 `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE`；首次导出时 `checkSelfPermission`，未授权就 `requestPermissions`，结果回调复用 `onrequestpermissionsresult`（`cases/16`）。

**开发模式验证不了授权流程**：权限属于宿主 `com.iapp.app`，LD9 上已是 allow，`checkSelfPermission` 恒 true，不会走 `requestPermissions`。本轮只验「文件真的落盘、目录可见」，回调与打包后首次授权标 ❓；不 revoke 宿主权限（会杀 iApp 进程、打断用户工程）。

## 11. 全屏与常亮

- 常亮：`activity.getWindow().addFlags(FLAG_KEEP_SCREEN_ON)`。
  - 开发模式跑在宿主 iApp 进程里，这个 flag 会连带让 iApp 编辑器常亮——可接受，但要在 P5 记录副作用。
- 沉浸式：**默认不开启**（会藏掉宿主 iApp 的编辑界面）。「文件」对话框里放「全屏」开关，手动切换，打包后可默认开。
- 返回键/退出：本轮不做拦截；误退出时板书已落盘。

## 12. 自检与证据

`selftest()` 在 `loading` 里跑，日志格式统一：

```
BB TEST <name> PASS|FAIL <detail>
```

最少覆盖：

1. 两条笔迹序列化 → 反序列化，字段与点数一致
2. 撤销/重做栈：push 3 → undo 2 → redo 1 → 剩下 2
3. 清空 → 撤销，笔迹数恢复
4. 坐标缩放：100×100 板上的点缩放到 200×200，值翻倍
5. 文件写读往返：写 2 笔 → 读回一致
6. 重放 500 条合成笔迹：不抛异常，耗时 ≤ 300ms（PASS 判定）；另打印 1000 / 3000 条的耗时供 P8 记录

运行期日志（不带每次 MOVE）：

```
BB init w= h= strokes= ...
BB stroke-end n= pts= ms= save=
BB undo depth= redo=
BB export board=... png=... ms=
BB import name= strokes= ms=
```

双证据：用户操作 + `adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'` + `adb exec-out screencap -p`。

## 13. 探针计划（写主工程前）

### 13.1 覆盖度盘点结论（2026-10-26，全 references 通读）

| 能力 | SKILL 现状 | 本设计的处理 |
|---|---|---|
| Bitmap 创建 / Canvas 绘制 / `setImageBitmap` 一次性出图 | 有配方（`recipes.md`、`cases/19`） | 直接用 |
| 已上屏 Bitmap 的**增量刷新** | 全库无 `invalidate` / `setLayerType` / 硬件加速记载 | P1 必测 |
| 多点触控 / pointer id / 历史点 | 全库无；示例只有 `getAction()` 单指 | P2 必测 |
| 自定义 View 子类 | 只证过 `PagerAdapter`；`SKILL.md:105` 与 `:108` 对 DexClassLoader 父加载器**自相矛盾** | 本轮不子类化，绕开；矛盾记入回填 |
| 撤销 / 重做 | 全库无 | 本轮首次沉淀 |
| 布局时机 | `loading` 里 `getHeight()=0`，`loadingComplete` 可用 | P3 复核 |
| 生命周期事件 | 事件名存在（`pause/stop/destroy/resume`…），触发顺序有表 | P7 复核可靠性，但不作为保存依赖 |
| 全屏 / 常亮 / 沉浸 | 全库无 | P5 必测 |
| PNG 编码 / 公共目录导出 | 无 `Bitmap.compress` 记载；`cases/19` 只有一条 PNG 落盘日志 | P6 必测 |
| 文件选择器 | 无；`onactivityresult` 事件存在但参数未文档化 | 绕开：只扫固定目录 + `AlertDialog` |
| 内置绘图控件 / `i.*` 绘图方法 | 无（390 个方法未全量枚举，属"未证明的缺席"） | 不用；顺手记结论 |

**已确认的文档病（本轮要修）**：

1. `SKILL.md:105`（父加载器给 `null`）与 `SKILL.md:108`（父加载器给宿主）冲突；`pitfalls.md:273-280` 只给了 `null` 版本，`external-library-guide.md:203` 又加了 androidx 例外。
2. `SKILL.md:28`「样式都在 mjava 里」与 `style-guide.md:3`「画布能看见的留在 ppt」冲突。
3. `touchmonitor` 的参数在 `events-guide.md:122-133` 有记载，但 `cases/14-2048.md:78` 判为"参数不明"，两处未对齐。
4. `recipes.md:170` 说不要用 `MANAGE_EXTERNAL_STORAGE`，`emulator-setup.md:46` / `SKILL.md:150` 说 Android 14 必须用；缺 API 29–33 的说明。

### 13.2 探针表

探针源码放 `android-sync/iapp-demo/blackboard-probe/`，复制进工程作为 `probe.iyu` 运行；每轮结束删掉。

| 编号 | 问题 | 判定 | 回填目标 |
|---|---|---|---|
| P1 | 改 `Bitmap` 后哪种刷新方式真的更新屏幕、最快 | 四种写法逐一截图对比 + 耗时 | 新建 `references/canvas-guide.md` |
| P2 | 多点触控 API 在 BeanShell 下是否可用 | `getActionMasked`/`getPointerId`/`findPointerIndex`/历史点 | `events-guide.md` |
| P3 | `loading` / `loadingComplete` 时控件宽高、`addOnLayoutChangeListener` | 何时能拿到非零尺寸；旋转是否重建页面 | `recipes.md` / `events-guide.md` |
| P4 | `setTag(Object)` 存 `HashMap` / `i.sss` 存对象 | 跨 call 取回是否一致 | `mjava-guide.md` |
| P5 | `FLAG_KEEP_SCREEN_ON`、`setSystemUiVisibility` 的副作用 | 生效情况 + 对宿主影响 | `recipes.md` |
| P6 | `/sdcard/Download` 写文件、媒体扫描（授权回调开发模式不可达，标 ❓） | 文件是否落盘、目录/相册是否可见 | `recipes.md` / `delivery-guide.md` |
| P7 | 生命周期事件在开发模式下的实际触发（`pause/stop/destroy/resume`） | 事件名与顺序是否与文档一致；能否拿到参数 | `events-guide.md` |
| P8 | 性能：单次增量绘线、重放 1000/3000 笔、单行追加与全量重写、PNG 压缩 | 各耗时，是否掉帧；3000 笔重放 > 1s 记档 | `canvas-guide.md` |
| P9 | `BitmapFactory.decodeFile`（可选，PNG 当底图） | 能否解码 | `recipes.md` |
| P10 | 同一工程在 LD14 / API 34 上复跑 P1、P2 | 刷新方式与多点触控是否一致；匿名 `OnTouchListener` 是否受 default method 影响 | `canvas-guide.md` / `pitfalls.md` |

P1–P8 跑 LD9（API 28，主目标）；P10 只在 LD14 上复跑两项，用来验证"API 28 结论不外推"的铁律。

每轮探针结束立即：原文 → `docs/evidence.md`；通用结论 → SKILL；本机事实 → `docs/runtime-env.md`。

**回填过滤（SKILL 规范）**：只写 iApp 特有的部分——原生 Android / Java 照写就能对的（如 `Paint.setAntiAlias`、`FileWriter`、`AlertDialog.Builder` 基本用法）不重复记录；照通用知识写会失败、静默不生效、或需要转换绕开的，必须写清"原生写法 → iApp 里的实际行为 → 正确写法"。

## 14. 实施顺序

1. 建工程 + 最小页，确认 iApp 能打开（用户操作）。
2. P1–P4 探针（绘制/触摸/布局/状态），定下刷新方式与触摸写法。
3. `pen.mjava`：位图、画笔、增量画线、重放；先用手写坐标在 `probe.iyu` 里验证。
4. `store.mjava` + 内部持久化；杀进程恢复验收。
5. `ui.mjava` + `mian.iyu` 工具栏与对话框。
6. P5–P8（常亮/文件/生命周期/性能），接入导出导入。
7. 整板验收：写、换笔、擦、撤销/重做、清空、恢复、导出、导入、旋转。
8. 记录 `cases/21-blackboard.md`；清理探针；更新索引。

## 15. 验收清单

- [ ] 启动无 `YuErr` / `MJavaErr`，自检 6 项全 PASS
- [ ] 4 色 × 3 档粗细都能写出对应线条，跟手不断线
- [ ] 橡皮能擦掉局部笔迹；擦完可撤销
- [ ] 撤销 20 步、重做 20 步，画面完全一致
- [ ] 清空有二次确认；清空后可撤销一次
- [ ] 杀进程重开，板书完整恢复（最多丢最后一笔）
- [ ] 导出后 `/sdcard/Download/Blackboard/` 有同名 `.board` 与 `.png`，PNG 能打开
- [ ] 导入列表能看到文件，导入后笔迹与导出前一致
- [ ] 旋转屏幕后板书不丢、字迹形状不变（等比缩放居中）
- [ ] 工具栏选中态随操作更新，按钮不会误触画布
- [ ] 所有探针结论已回填，`docs/evidence.md` 有原文

## 16. 留给实现者的决定

- 刷新方式按 P1 实测选，不追求统一写法。
- 重放 3000 笔超过 1s 才考虑"包围盒区域快照"；本轮只测量、记档，不提前优化。
- 颜色格文案用汉字还是色块（汉字更直观，色盲友好度差一些）。
- 「全屏」开关放文件对话框里是否够用。
- 是否在本轮末尾打包 APK（默认不打包）。
- 导入列表最多显示多少条（建议 50 条）。
