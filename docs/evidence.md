# 探针批次索引

每轮探针在这里留**一行**：日期 / 批次 ID / 一句结论 / 现行主文件 / 状态。
原始读数不进本文件——2026-10-24 ~ 2026-10-31 的全文冻结在
`docs/archive/evidence-2026-10.md`（只读），需要 logcat 原文或复现命令时去那里按批次 ID 找。

规则：

- **批次 ID 是引用键**（`SYNC-2` / `UIPROBE-1` / `WATCH-2` …），外部文档按它寻址，不要改名、不要合并。
- 新批次先加一行、状态写 `未提炼`；结论稳定后写进 SKILL，再把这一行改成 `已提炼` 并填主文件。
- 已定级（✅）的批次只留一句结论；⚠/❓ 的读数摘要与验证方法写在文末「未决读数」，不要丢。
- 结论只写一份在 SKILL / 环境档案里，本表只做「去向索引」。

## 索引

| 日期 | 批次 | 一句结论 | 主文件 | 状态 |
|---|---|---|---|---|
| 10-24 | B0 | 雷电 9 工程根 `/data/media/0/iApp/ProjectApp`；bind mount 对 app 不可见 | `environments/ldplayer9.md` §4、`pitfalls.md` #2 | 已提炼 |
| 10-24 | B1 | `activity` 与 `i` 是两个默认对象；裸 `findViewById` 不存在 | `mjava-guide.md` §两个默认对象 | 已提炼 |
| 10-24 | B2 | `final` / 具名 class / `0xFF` / 可变参数会让整个模块失效 | `mjava-guide.md` §铁律表 | 已提炼 |
| 10-24 | B3 | ppt 单位与 `st_` 桥；未知键静默忽略 | `iyu-guide.md` §ppt 属性层 | 已提炼 |
| 10-24 | B4 | `i.ss` 底层 HashMap 默认 null；`i.sss` 跨 call 但每次运行重置 | `iapp-i-reference.md` §生命周期 | 已提炼 |
| 10-24 | B5（模块装载） | `i.d.f` 仅开发模式；交付用 `i.fn`，源码直接打包 | `modularization-guide.md` §不要用 `i.d.f` | 已提炼 |
| 10-24 | B5（外部 JAR） | JAR→D8→dex，产物放 `apk/assets/` | `external-library-guide.md` §基础结论 | 已提炼 |
| 10-24 | B6（静态分析） | `i` = `Aid_javaCode`，390 方法 / 12 字段 | `iapp-internals.md` §关键类 | 已提炼 |
| 10-24 | B6 补测 | `ss_dim` 是 static；`qm` 字段容器 | `iapp-internals.md` §字段 | 已提炼 |
| 10-24 | B7（打包） | `versionCode = 100000 + versionint`；打包后 `ygs` 无输出 | `delivery-guide.md` §打包环境的限制 | 已提炼 |
| 10-24 | B7（`.iApp` 备份） | 顶层直接是工程内容；同包名导入失败 | `delivery-guide.md` §默认交付 | 已提炼 |
| 10-24 | D1 样式分层 | `weight`/`alpha`/`padding`(px) 静默失真；`loading` 阶段宽高为 0 | `style-guide.md` §档 A 历史 | 已提炼 |
| 10-24 | D1b 波纹/MD | 必须 `setClickable(true)` 才有波纹；Button 自定义背景会丢原生波纹 | `style-guide.md` §波纹 | 已提炼 |
| 10-24 | D2 Material 组件 | 「影子实例」只在 API 28 成立；API 34 是真实实例 | `pitfalls.md` #7 | 已提炼·版本差异 ⚠ |
| 10-26 | MDF 表单 | TIL 外观由子控件 Context 决定 | `md-components-guide.md` §ppt 声明的 TIL | 已提炼 |
| 10-26 | 事件探针第一轮 | 负结论作废（事件名写错）；正确名单见权威表 | `events-guide.md` §运行期已确认触发 | 已作废 |
| 10-26 | 事件类型权威表 | 事件名单来自 `VisualDesigner`；参数统一 `st_*` | `events-guide.md` §权威名单 | 已提炼 |
| 10-26 | 短名问题 | `Switch` 不是内置短名 | `builtin-controls.md` §注意 | 已提炼 |
| 10-26 | 黑金计算器 | 状态放 `i.sss`；均分用 `height=0 + layout_weight=1` | `recipes.md` §带状态的交互页 | 已提炼 |
| 10-26 | 内置短名页闪退 | `DrawerLayout` 必须精确尺寸，否则闪退 | `pitfalls.md` #11 | 已提炼 |
| 10-26 | events6 | 生命周期 `loading → start → loadingComplete`；`downkey/upkey` 成对 | `events-guide.md` §运行期已确认触发 | 已提炼 |
| 10-26 | events7 | 滚动事件属列表型控件；WebView 不支持滚动事件 | `events-guide.md` §滚动/列表事件 | 已提炼 |
| 10-26 | events8（两轮） | SeekBar 用 `onprogresschanged2`；SwipeRefresh 导入 androidx | `events-guide.md` §拖动条、`pitfalls.md` #12 | 已提炼 |
| 10-26 | events9 | `addTab` 首枚自动回调；切换成对；Spinner `setAdapter` 自动回调 | `events-guide.md` §运行期已确认触发 | 已提炼 |
| 10-26 | events10 | 抽屉事件可用；事件名写错静默忽略 | `events-guide.md` §抽屉 | 已提炼 |
| 10-26 | events4（两轮） | `call` 模块名写错即静默失败；override WebView 链接要自己 `loadUrl` | `pitfalls.md` #13 | 已提炼 |
| 10-26 | B8 文件管理器 | 匿名接口回调可用；权限是宿主的 | `mjava-guide.md` §铁律表 | 已提炼 |
| 10-26 | 2048 实战 | 键盘/触摸/动画/持久化/自检全链路 | `recipes.md`、`animation-guide.md`、`events-guide.md` | 已提炼 |
| 10-26 | 浏览器首轮 | 事件变量靠反查 DEX 得到；`url` 未定义 → `st_url` | `events-guide.md` §事件内置变量 | 已提炼 |
| 10-26 | B8 浏览器 | `canGoBack`、进度回调 3 次、结束 URL 为 `about:blank` | `events-guide.md` §WebView | 已提炼 |
| 10-26 | 应用图标 | `icon.png` 原样进 `mipmap-*/img_iapp.png`；1×1 蓝会被拉成蓝方块 | `icon-guide.md` | 已提炼 |
| 10-26 | 模块化探针 | `i.fn` 加载；`importAll()` 写在方法体内；同名后加载覆盖 | `modularization-guide.md` | 已提炼 |
| 10-26 | `i.call` 语义 | 首参是语言；void 方法不能接返回值 | `mjava-guide.md` §跨模块调用 `i.call` | 已提炼 |
| 10-26 | 下拉选择器 v1 | `String.valueOf(null)` 选中 `char[]` 重载 → NPE | `pitfalls.md` #15 | 已提炼 |
| 10-26 | 下拉选择器 v2 | 单弹窗多级级联 + 返回上一级 + 仅叶子回调 | `recipes.md` §单弹窗多级选择器 | 已提炼 |
| 10-26 | sora-editor AAR | AAR 拆 classes.jar/res；包 ID 用 0x80；父加载器见宿主 | `external-library-guide.md` §带资源的 AAR | 已提炼 |
| 10-26 | ViewPager 事件 | `onpageselected/onpagescrolled/onpagescrollstatechanged` 可用 | `events-guide.md` §ViewPager | 已提炼 |
| 10-26 | onoffsetchanged | `st_vO` 是真实偏移（px，负值） | `events-guide.md` §AppBarLayout 偏移 | 已提炼 |
| 10-26 | 黑金卡 3D | 普通 View 可做 3D 倾斜；视觉需求先出静帧再上机 | `animation-guide.md` §3D 倾斜、`methodology.md` #9 | 已提炼 |
| 10-26 | Android 15 DCL | targetSdk≥34：动态加载的 dex 必须只读 | `external-library-guide.md` §Android 14+ 只读 | 已提炼 |
| 10-26 | 国内网络 | WebFetch 不可用；`curl -k` + 镜像可用 | `network-and-mirrors.md` | 已提炼 |
| 10-26 | E0 双模拟器 | 两套雷电抢宿主 5555；`emulator-5554` 会静默漂移 | `emulator-setup.md` §5、`pitfalls.md` #28 | 已提炼 |
| 10-26 | Android 14 root | Koush Superuser 写 `su.sqlite` 可永久授权 | `environments/ldplayer14.md` §root | 已提炼 |
| 10-26 | Android 14 软链 Pictures | 软链可行；vboxsf 本身不支持 `ln -s` | `emulator-setup.md` §0 | 历史·通道停用 |
| 10-26 | E1 实例改名 | `leidian1` → 宿主 5557，两套安装可永久分开 | `emulator-setup.md` §5 | 已提炼 |
| 10-26 | 课堂黑板 BB-P1 | API 28 布局时机与四种刷新耗时；`getHistorySize(int)` 杀进程 | `pitfalls.md` #8.1、`recipes.md` | 已提炼 |
| 10-26 | E2 其他模拟器 | MuMu 12 / BlueStacks 5 的共享目录路径 | `emulator-setup.md` §6 | 已提炼 ⚠ 未实机 |
| 10-27 | TIL 探针 | ppt 建 TIL 是真的，但子控件用 activity ctx → 无 M3 外观 | `md-components-guide.md` §档 A | 已提炼 |
| 10-27 | custom.iyu | 全类名声明 M3 控件；盒子不画，修复挂 `loading` | `md-components-guide.md`、`material-components.md` | 已提炼 |
| 10-27 | NAV-1 | 每页一个 Activity 实例；前进 `pause → loading… → stop` | `navigation-guide.md` §页面栈 | 已提炼 |
| 10-27 | NAV-2 | `finish()` 当返回；A→A 会再压一个同名实例 | `navigation-guide.md` §返回 | 已提炼 |
| 10-27 | NAV-3 | `uigo` flag 按 Activity 组件匹配；只有 1073741824 真有用 | `navigation-guide.md` §flag | 已提炼 |
| 10-27 | NAV-5 | 传参用 `i.sss`；无 ActivityResult 通道 | `navigation-guide.md` §传参 | 已提炼 |
| 10-27 | NAV-6 | 打包版多页导航语义与开发模式一致 | `navigation-guide.md` §打包模式 | 已提炼 |
| 10-27 | NAV-7 | `lan` 转场、`end`、`addv` 只能写在 yul | `navigation-guide.md` §转场 | 已提炼 |
| 10-27 | Material 静态扫描 | material 1.13 共 490 类；35 个候选控件 | `material-components.md` §支持矩阵 | 已提炼 |
| 10-27 | Material 运行时扫描 | 34/35 可 `(Context)` 构造；`Carousel` 被裁 | `material-components.md` §支持矩阵 | 已提炼 |
| 10-27 | 组件画廊 | 20 个组件全部构造并上屏成功 | `material-components.md` §上屏 | 已提炼 |
| 10-27 | NAV-8 | 内嵌页事件照常触发；ViewPager 子控件进树但不渲染 | `navigation-guide.md` §addv | 已提炼 |
| 10-27 | NAV-9 | 内嵌 id 按「文件首次内嵌顺序」分号段，不是固定 +10000 | `navigation-guide.md` §addv | 已提炼·首句已修正 |
| 10-27 | NAV-10 | 多页 addv 号段；VerticalViewPager 不渲染 | `navigation-guide.md` §addv | 已提炼 |
| 10-27 | NAV-11 | drawer 未改 gravity → `No drawer view found with gravity LEFT` | `navigation-guide.md` §addv | 已提炼 |
| 10-27 | NAV-12 | `DrawerLayout` 三步：改 gravity + 延迟 400ms `openDrawer` | `navigation-guide.md` §addv | 已提炼 |
| 10-27 | NAV-13 | ScrollView 根 + 内层 LinearLayout 的长页结构 | `iyu-guide.md` §长页面 | 已提炼 |
| 10-27 | NAV-14 | 打包版二级内嵌页事件正常 | `navigation-guide.md` §打包模式 | 已提炼 |
| 10-27 | NAV-15 | 二级内嵌 + 抽屉页事件闭环 | `navigation-guide.md` §addv | 已提炼 |
| 10-27 | NAV-16 | 打包版 DrawerLayout / ScrollView 正常 | `navigation-guide.md` §打包模式 | 已提炼 |
| 10-27 | 设计器崩溃（showcase） | 四类嫌疑 → 实测只剩 `SearchBar` | `pitfalls.md` #7 | 已推翻 |
| 10-27 | XUI 1.1.9（P1/P2） | 资源不自足 AAR 全链路；双 AssetManager；主题用屏幕型变体 | `external-library-guide.md` §带资源的 AAR（二） | 已提炼 |
| 10-27 | XUI-P3 | 库 setter 可能假设 AttributeSet 已初始化；先 `javap -c` 看字节码 | `external-library-guide.md` §库的 setter | 已提炼 |
| 10-27 | XUI-P4 | 打包版要把 dex 与资源包都释放到 cache；dex 走只读 | `external-library-guide.md` §打包模式 | 已提炼 |
| 10-27 | API-A1 | 歌德五端点普查；期刊按刊期换代 | `.claude/skills/gede-read-api/` | 已提炼·搜索条被 QJ-P2 推翻 |
| 10-27 | M3-D1 | 组件样张首轮；`setStrokeColor` 等重载要按签名调 | `material-components.md` §样式注意 | 已提炼 |
| 10-27 | 设计器崩溃 P1/P2/P3 | `TabLayout` 排除；`SearchBar` 确认；触发是保存动作 + 2s 防抖 | `pitfalls.md` #7 | 已提炼 |
| 10-27 | 设计器崩溃根因 | R8 反编译：`T0` 把 tag 当 `Object[]`，`id≥1` 跳过判空 → NPE | `pitfalls.md` #7 | 已提炼 |
| 10-27 | 崩溃根因验证 Demo | sbverify 运行期自检 + sbcrash 时序 A/B | `pitfalls.md` #7 | 已提炼 |
| 10-27 | QJ-P1 | `i.hs`/`runOnUiThread`/`i.us` 网络图；`org.json` 必须 import | `mjava-guide.md` §网络 | 已提炼 |
| 10-28 | QJ-P2 | 站内搜索 `keyword` 是假参数，返回全量 | `.claude/skills/gede-read-api/` | 已提炼·推翻 API-A1 |
| 10-28 | QJ-P3 | `catalogs[].page` 是 1 基页号；`contentIndex` 不是页索引 | `.claude/skills/gede-read-api/` | 已提炼 |
| 10-28 | QJ-P4 | 两处 BeanShell 崩溃点（搜索页首次打开 / 目录跳页回归） | `pitfalls.md` #15 | 已提炼 |
| 10-28 | QJ-P5 | ppt 的 TIL 塞进 56dp 横条会被撑高、文字下沉 | `md-components-guide.md` §别把 TIL 塞进固定高度 | 已提炼 |
| 10-28 | ENV-1 | 环境探测首跑：shared/adb/FTP 三通道判定 | `environments/ldplayer14.md` §1 | 已提炼 |
| 10-28 | ENV-2 | 他机 FTP 读数（M2 带回，本机未复验） | `environments/tencent-appstore-pc.md` | 已提炼 ⚠ |
| 10-28 | ENV-3 | NAT 后只 forward 控制端口不够，每个数据端口都要转发 | `ftp-delivery.md` §7 | 已提炼 |
| 10-28 | ENV-4 | FTP 写操作全通；`MKD` 非递归、`STOR` 不建父目录 | `ftp-delivery.md` §4/§5 | 已提炼 |
| 10-28 | ENV-5 | `ftp_sync.py` 端到端（含 CWD 校验、错误元组坑） | `ftp-delivery.md` §6 | 已提炼 |
| 10-28 | QJ-P6 | 阅读接口分段与虚拟尺寸 | `.claude/skills/gede-read-api/` | 已提炼 |
| 10-28 | DOC-1 | 文档体检脚本落地；六类误报校准 | `.claude/skills/docs-architecture/` | 已提炼 |
| 10-28 | CAP-1 | BeanShell 匿名接口能捕获形参与局部变量 | `mjava-guide.md` §铁律表 | 已提炼 |
| 10-28 | WATCH-1 | 手表侧载口述（含 arm64 推断） | `environments/oppo-watch-x2.md` | 已推翻·见 WATCH-2 |
| 10-28 | QJ-P7 | `BottomSheetDialog` 的可变参数调用与上色 | `mjava-guide.md` §原生底部抽屉 | 已提炼 |
| 10-28 | QJ-P8 | 抽屉上色闪退、嵌套滚动、入口 import | `mjava-guide.md` §原生底部抽屉、`pitfalls.md` #34 | 已提炼 |
| 10-28 | WATCH-2 | 应用宝容器→手表全链路；ABI 与键码实测 | `watch-app-guide.md` §1、`environments/oppo-watch-x2.md` §已知坑 | 已提炼 |
| 10-29 | WATCH-3 | 手表 WebView、服务端分页与圆屏布局 | `watch-app-guide.md` §2/§6 | 已提炼 |
| 10-29 | WATCH-4 | 手表版 8 页迭代读数 | `watch-app-guide.md` §4/§5 | 已提炼 |
| 10-29 | DOC-2 | 文档体检与修复；计划不写死基线 commit 与计数 | `docs-architecture/references/maintenance.md` §4 | 已提炼 |
| 10-29 | DOC-3 | 工程私有文档区；项目不放 `.claude/` | `docs-architecture/references/architecture.md` §1 | 已提炼 |
| 10-30 | DOC-4 | 项目私有文档归属（用户决策） | `docs-architecture/references/architecture.md` §5 | 已提炼 |
| 10-29 | DOC-5 | 体检工具与语义审 | `docs-architecture/references/review-checklist.md` | 已提炼 |
| 10-29 | WATCH-5 | 模拟器圆表盘罩层（不改显示尺寸） | `watch-app-guide.md` §10 | 已提炼 |
| 10-29 | WATCH-6 | 手表版 2048；圆屏禁用系统 Dialog | `watch-app-guide.md` §5 | 已提炼 |
| 10-29 | WATCH-7 | scrcpy 控表：实时预览与交互通道 | `watch-app-guide.md` §11 | 已提炼 |
| 10-29 | WATCH-8 | uhid 键位 F1/F2；131/132 来自 `qpnp-pon` | `environments/oppo-watch-x2.md` §取证 | 已提炼 |
| 10-29 | WATCH-9 | scrcpy 窗口≠视频尺寸，注入前要换算坐标 | `watch-app-guide.md` §11 | 已提炼 |
| 10-29 | WATCH-10 | scrcpy 滚轮两种模式都无效；改用按住拖动 | `watch-app-guide.md` §11 | 已提炼 |
| 10-30 | WATCH-11 | iApp 手表支持定为实验性 | `watch-app-guide.md` §0 | 已提炼 |
| 10-30 | SYNC-2 | 共享目录改写设备已读文件后，FUSE 长期返回旧内容 | 根 `CLAUDE.md` §投递链路 | 历史·通道停用 |
| 10-30 | SYNC-3 | 共享目录里「源」与「设备副本」是同一批字节 | 根 `CLAUDE.md` §目录约定 | 历史·通道停用 |
| 10-30 | UIPROBE-1 | mjava 建树前提 P1–P8（同属性测量一致 463×70、40 视图 14ms） | `SKILL.md` §界面构建、`ui-kit.md` §已知限制 | 已提炼 |
| 10-30 | UIPROBE-2 | ui-kit 自检 K1–K7；两类失败要分型 | `ui-kit.md` §已知限制 | 已提炼 |
| 10-30 | JAVA-BLOCK-1 | `java { }` 技术可行，但打包属 VIP → 不用 | `inline-java-block.md` | 已提炼·勿用 |
| 10-30 | DELIVERY-1 | 停用共享目录，改 iApp 默认工程根；push 不能自建目录 | 根 `CLAUDE.md` §投递链路、`emulator-setup.md` §4 | 已提炼 |
| 10-30 | G1-REWRITE-1 | liquidglass 按 mjava 建树上机（基线代码已删） | —（状态见 SHOWCASE-C01-STATUS） | 已过时 |
| 10-30 | WINDOW-1 | 内容铺到顶边三败一成：要动根的直接父容器 | `pitfalls.md` #32、`status-bar-guide.md` | 已提炼 |
| 10-30 | GEDE-P1 | 歌德五端点契约复测 + `gede-read-api` skill 落地 | `.claude/skills/gede-read-api/` | 已提炼 |
| 10-30 | RES-1 | 工程 `res/` 图片用 `i.us(@名称)`，开发与打包两形态都成立 | `recipes.md` §工程 res/ 图片 | 已提炼 |
| 10-30 | GEDE-P2 | `psize=0`、越界页、token 301 的行为 | `.claude/skills/gede-read-api/` | 已提炼 |
| 10-30 | GEDE-P3 | 目录层级实测，推翻「children 恒空」 | `.claude/skills/gede-read-api/` | 已提炼 |
| 10-31 | SHOWCASE-DOC-1 | 提示词文档改为「动静一体」的案例集 | `docs/ui-showcase-prompts.md` | 已提炼 |
| 10-31 | SHOWCASE-C01-STATUS | C01 旧实现已删，状态回退「未建」 | `docs/ui-showcase-prompts.md` | 状态更正 |
| 10-31 | JY-IMPLEMENT-1 | 回调/线程是新解释器、ScrollView 无 LayoutParams、WebSettings、行距叠乘 | `pitfalls.md` #36–#39 | 已提炼 |
| 10-31 | STATBAR-1~3 | 状态栏背景来自宿主 a0；根挂 DecorView 才真铺满 | `status-bar-guide.md` §0/§1 | 已提炼 |
| 10-31 | STATBAR-MIN | 铺满只需 1 个 `loading` 事件 | `status-bar-guide.md` §2.1 | 已提炼 |
| 10-31 | STATBAR-TYPES | 隐藏状态栏约 400ms 后宿主自动铺满；同色只改 a0 背景 | `status-bar-guide.md` §1/§2.4 | 已提炼 |
| 10-31 | JY-UIREUSE-1 | `DrawerLayout` 必须包住内容；`ui_reg` 跨页存活；变参绑不上且 catch 不住 | `pitfalls.md` #41–#43 | 已提炼 |
| 10-31 | STATBAR-ICONS | 图标明暗只能用 `WindowInsetsController.setSystemBarsAppearance` | `status-bar-guide.md` §2.5 | 已提炼 |
| 10-31 | STATBAR-EDGE | pause/resume 与打包均保持；`hide()` 滑动唤出后不自动隐藏 | `status-bar-guide.md` §2.4/§4 | 已提炼 |
| 10-31 | STATBAR-ADDV | 挂根后 `addv` 内嵌页正常；透明唤出行为下滑后自动隐回 | `status-bar-guide.md` §2.4/§4 | 已提炼 |
| 10-31 | NAVBAR-RRO | 雷电 14 镜像 `config_showNavigationBar=false`，RRO 可临时改但重启即失效，导航栏启不了一直生效 | `environments/ldplayer14.md` §2 | 已提炼·放弃 |
| 10-31 | WEBVIEW-ARCH-1 | WebView 全前端 + URL scheme 桥接成立；`iapp.fn` 只能调 yul 模块；状态栏底色/图标随主题同步 | `webview-bridge.md`、`pitfalls.md` #48 | 已提炼 |
| 10-31 | WEBVIEW-NET-1 | file:// + universal access 可绕过 CORS；https base 受限；原生代理子线程 + 主线程 `i.has` 兜底 | `webview-bridge.md` §6、`pitfalls.md` #49 | 已提炼 |
| 10-31 | WEBVIEW-PKG-1 | 打包态复核：android_asset 同样绕 CORS；原生代理/主题/uigo 入口均成立；IME 未验 | `webview-bridge.md` §6/§9 | 已提炼 |
| 10-31 | JY-VER-1 | 开发态包名是宿主 `com.iapp.app`，读 `versionName` 拿到 IDE 版本；打包态才是工程版本 | `pitfalls.md` #47、`ui-kit.md` §包信息 | 已提炼 |
| 10-31 | JY-HANDLE-1 | `ui_init` 三层是全局键；跨页返回后不重建会画进旧树；生命周期入口需 `i.fn` 齐依赖模块 | `pitfalls.md` #42 连带坑、#50 | 已提炼 |
| 10-31 | JY-TOC-1 | 同一 EPUB 文件的兄弟项共用 `href`/`id`，节点键要带 `contentIndex`；子页码可能只是父页 | `gede-read-api/references/api-reference.md` §6 | 已提炼 |
| 10-31 | JY-ERR-1 | 书不存在 = 200 + 400 错误页且无令牌字段；与网络失败必须分开提示 | `gede-read-api/references/api-reference.md` §5 | 已提炼 |
| 11-01 | IYUFMT-1 | 标签缩进/空行/自闭合/闭合标签另起行可用；`<View>` 属性换行会整页失效；ppt 按列 0 保守处理 | `iyu-guide.md` §格式化容忍度 | 已提炼 |

## 未决读数

只列还没定级、且会影响写法的事项；验证方法写在这里，验完把结论搬进主文件并把对应批次改成 `已提炼`。

- **Ripple 第三参能否传 `null`**（`style-guide.md` §波纹 ❓）：早期记录说圆角背景可传 null，
  `pitfalls.md` #35 实测会不受边界裁剪、扩散成整圆。
  怎么验：同一圆角背景控件分别用 null 与圆角矩形遮罩各画一次，在圆角外侧截图比对。
- **图标明暗的其它版本**（`pitfalls.md` #40 ❓）：API 34 上 `setSystemUiVisibility(8192)` 无效已定案；
  其它 iApp / Android 版本是否同样如此未验。怎么验：进页面后 `setSystemBarsAppearance` 设深/浅各一次，截图比对。
- **`i.sss` 直接存 View**（`ui-kit.md` §已知限制 ⚠）：WATCH-5 单次现象是取回 null，包 `HashMap` 后可取回。
  怎么验：同一模块里直存 View 与存 HashMap 各取一次，比较是否为 null；稳定方案仍是 `setTag(int, View)`。
- **API 28 的「影子实例」**（`pitfalls.md` #7 ⚠）：D2 的 API 28 读数是该结论唯一来源，API 34 已推翻。
  怎么验：API 28 设备上跑最小 ppt 自定义类探针，核 `attached` / `addView` / hash。
- **浏览器事件的 `st_eX` / `st_eY`**（`events-guide.md` §事件内置变量 ❓）：
  DEX 里有，运行期未见过。怎么验：在 `touchmonitor` 里打印这两个变量的值。
- **隐藏状态栏后的边缘滑出**（`status-bar-guide.md` §2.4 ❓）：
  怎么验：隐藏后从屏幕顶部下滑一次，看系统栏是否被唤出。
- **手表 `BottomSheetDialog` 的拖动与遮罩**（JY-UIREUSE-1 R5 ⚠）：只验到「能弹出」。
  怎么验：表上打开后拖一次、点遮罩一次，看是否按 `BottomSheetBehavior` 正常收起。
- **打包 APK 下的窗口边界**（`pitfalls.md` #40 ❓）：根挂 DecorView 后，打包版是否保持、
  `pause/resume` 是否还原、`addv` 内嵌页是否受影响。怎么验：打包后跑同一探针，各场景读 `rootY/rootH`。

---

## 2026-10-31 STATBAR-PKG 打包版安全区失效，推翻「打包与开发一致」

**来源**：用户在 `com.jianyue.reader` 打包安装后回报（非探针读数，无 logcat）。

**现象**：开发模式下页面正常；**打包 APK 里顶部标题被状态栏压住**（搜索按钮有一部分进了状态栏），
即 `ui_insets()` 算出的 `top` 为 0。

**推断原因**：挂根（内容铺满）后顶部安全区完全依赖 `getRootWindowInsets()`；
打包版里它可能返回 null 或全 0，于是 `top = max0(barsTop - rootTop) = 0`。

**为什么之前没发现**：STATBAR-1~3 / STATBAR-MIN 只读了 `rootY` / `rootH` / `insetTop`，
验的是「铺满有没有生效」，**没有验**「insets 驱动的安全区在打包版是否成立」。
`status-bar-guide.md` §4 里那条「打包后效果一致 ✅」属于结论外推，已修正为分段结论。

**对策（已写进 `ui.mjava`）**：`getRootWindowInsets()` 为 null、或 `barsTop<=0 且 rootTop<=0` 时，
用 `getIdentifier("status_bar_height","dimen","android")` 兜底；**底部不兜底**
（手势导航下 `navigation_bar_height` 仍有值，兜了会多出一条空白）。

**结论**

| # | 结论 | 级别 |
|---|---|---|
| P1 | 打包版可能读不到窗口 insets，铺满页的顶部安全区会失去保护 | ⚠ 用户实测语义，无读数 |
| P2 | 兜底用 `status_bar_height` 可行；底部不能用 `navigation_bar_height` | ✅ 2026-10-31 打包复验：顶部留出状态栏高度、底部正常 |
| P3 | 「打包与开发效果一致」只对 `rootY/rootH` 成立，对安全区不成立 | ✅ 2026-10-31 推翻旧结论 |

**回填**

- `.claude/skills/iapp-development/references/status-bar-guide.md`：新增 §2.6，修正 §4
- `project/com.jianyue.reader/src/ui.mjava`：`ui_insets()` 增加 dimens 兜底

---

## 2026-10-31 JY-RIPPLE-1 书架格子按下高亮：两轮都只对了一半

**背景**：要求「按下时高亮沿格子四周扩出去一圈」。前后试了背景涟漪、前景 drawable、
兄弟覆盖层、手动 pressed 底色四种写法，逐轮定位出两个独立问题。

**问题 1：高亮只出现在封面之外**

- 试过 `setBackground`、`setForeground`、兄弟覆盖层，封面区域始终不上色
- 定位依据：高亮的上边缘**正好卡在封面底边**
- 结论：`i.us` 加载的图片绘制在普通 View 之上，覆盖层/前景都压不住（见 pitfalls #46）

**问题 2：外扩只成功了一侧**

- 现象按列不同：首列只往右扩、中间列左右都行、末列只往左扩；上下亦同
- 定位：容器链上只要有一层 `clipToPadding=true`（默认），溢进 padding 的部分就被切
- 修复：从格子到屏幕逐层关 `clipChildren` + `clipToPadding`（网格 / 行 / HorizontalScrollView /
  页内容区），共 4 层才关全（见 pitfalls #45）

**问题 3（附带）**：负边距覆盖层挂在 `wrap_content` 父容器里时，`match_parent` 会按整屏测量，
高亮糊到上下排。修法：先 `measure()` 取真实高度、把父容器高度定死。

**结论**

| # | 结论 | 级别 |
|---|---|---|
| R1 | `i.us` 的图片盖过 overlay/foreground，按下反馈要作用在 ImageView 自身 | ✅ 用户实测 |
| R2 | 溢出绘制要逐层关 `clipChildren` + `clipToPadding`，含带 padding 的外层 | ✅ 用户实测 |
| R3 | `wrap_content` 父容器里的 `match_parent` 子控件按整屏测量 | ✅ 用户实测 |
| R4 | 涟漪遮罩圆角 = `RippleDrawable` mask 的 `setCornerRadius`，本项目取 8dp | ✅ |

**回填**

- `.claude/skills/iapp-development/references/pitfalls.md`：#45（裁剪链）、#46（图片层级）
- `.claude/skills/iapp-development/references/material-components.md`：`MaterialCardView` 配方
