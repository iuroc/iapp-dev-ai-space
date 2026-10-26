---
name: iapp-development
description: 开发、调试、打包 iApp（Android 可视化 IDE，显示名"测兆编程"）工程时使用。只要出现 .iyu 界面文件、.mjava 模块、裕语言语法、call 跨语言调用、iApp 工程结构、adb 投递调试、iApp 打包交付等需求，就先读本技能。里面有实测过的语法铁律、失败签名、投递链路和探针方法，能避免重复踩坑；不确定的行为按本技能的探针流程先测再写。
---

# iApp 开发知识库

iApp（显示名"测兆编程"）是 Android 上的可视化 IDE：工程是「界面文件 + 模块代码 + 资源」的目录，直接在设备上编译运行。

## 写什么 / 不写什么（本库的边界）

本库只记录 **iApp 特有** 的行为，不重复通用 Android / Java 知识。

- **不写**：与原生 Android / Java 完全一致的用法。例如 `Paint.setAntiAlias(true)`、`FileWriter` 读写文本、`AlertDialog.Builder` 的基本链式调用——凭通用知识就能写对，写进来只增加维护负担和过期风险。
- **必写**：在 iApp 里**不能照原生 / Java 的写法直接用**，需要转换、绕开或额外处理的。判据是"照通用知识写会失败或静默不生效"，包括：
  - 语言层限制：BeanShell 不支持 `final`、具名 class、`0xFF` 大十六进制字面量、可变参数；模块级变量跨 `call` 丢失
  - 能力缺失：不能继承类（自定义 View / Adapter 要走 dex）；裸 `findViewById` 不存在
  - 属性 / 事件名与原生不一致：ppt 用 `layout_weight` 而不是 `weight`；`alpha`、`weight` 在 ppt 里静默无效；事件名写错静默忽略
  - 宿主环境副作用：开发模式跑在 `com.iapp.app` 进程里，`getFilesDir()` 多工程共用、权限是宿主的、改系统 UI / 方向会影响宿主
  - 需要双证据才敢下结论的：行为与文档不一致、版本相关（API 28 vs 34）
- **写法**：先写"原生写法是什么 → 在 iApp 里会怎样 → 应该怎么写"三段式；结论带 ✅/⚠/❓ 与版本前提。
- **更新前自检**：新增内容如果删掉后，一个懂 Android / Java 的人照样能写对，就不该进来。

## 五分钟模型

```
工程根/                       # 设备上的实际位置随环境不同，见工作区本机文档
├── src/
│   ├── mian.iyu              # 入口界面（必须叫 mian.iyu）
│   ├── *.iyu                 # 其它界面
│   └── *.mjava               # Java 模块（无 class 外壳，直接写方法）
├── files/                    # 运行期文件
├── res/  sdk/  icon.png
├── AndroidManifest.xml
└── .project                  # 工程元数据
```

界面文件是伪 XML：`<View id= did= type=>` + `<ppt>` 属性块 + `<event>` 事件块；
全局事件集中在文件末尾 `<UIEventset>`，事件项写成 `<eventItme type="loading">代码</eventItme>`。

代码分两种语言，可互相调用：
- `.iyu` 里只留 `call(...)` / `addv(...)` 做编排（日志、Toast、样式都在 mjava 里）
- `.mjava` 里是 Java 语法，但**由 BeanShell 解释执行**，不是编译成 class（报错原文见 `references/mjava-guide.md`）

`call` 三要素：`call(接收返回值的变量, "mjava", "模块.方法", 参数…)`；无返回/无参用 `call(null, "mjava", "app.run")`。
传给模块的参数个数要与方法签名一致，返回值只对 mjava/mlua 有效。

## iyu 白名单（只允许 `call` / `addv`）

`.iyu` 里除了 `call` 和 `addv`，**一律不用其它裕语言函数**，改用 mjava 的 Java 写法：

| 原函数 | 替代 |
|---|---|
| `us` / `ug` | 原生 setter / getter（mjava） |
| `gvs` | `activity.findViewById(id)` |
| `s` / `ss` / `sss` / `dim` | `i.sss` / 隐藏控件 / SharedPreferences |
| `syso` | `i.syso(...)` 或 `android.util.Log` |
| `tw` / `utw` | Toast / AlertDialog |
| `uigo` | `.uigo` 方式（见对应文档） |

可以直接使用：`activity.finish()`、`i.lan`、`ViewGroup.removeView(...)`。

## 多模块（加载另一个 mjava）

```java
i.fn("b");          // 实测加载，模块名不带扩展名
b_hello();          // 加载后直接调
```

- **每个 public 入口第一行 `importAll()`**；加载前调用会 `Command not found`，
  整个方法中断，`catch` 接不住
- 同名方法后加载覆盖；子模块方法统一加前缀（`core_` / `ui_` / …）
- 推荐 facade 模式：`game.mjava` 只暴露 `init/layout/...`，子模块私有
- 状态仍放 `i.sss`；模块级变量只在本次 `call` 内有效
- `i.d.f("b.mjava")` 只在开发模式可用；打包后 `i.d` 是 `xn0`，没有 `f(String)`。
  **交付用 `i.fn`，源码直接打包，不合并**
- `i.call("b.b_hello","mjava")` 会新建解释器且找不到当前工程模块（实测返回 null），
  跨模块加载不要用它
- 完整规范：`references/modularization-guide.md`

## 硬规则

1. **入口必须是 `src/mian.iyu`**（不是 main.iyu）。
2. **iApp 以内存为准**：push 前先 `am force-stop`，或在 iApp 里关掉工程；否则保存/运行会用旧内存覆盖磁盘。
3. **交付用 adb push**，不要用 bind mount（应用 namespace 看不到后加的挂载）。
4. **双证据**：屏幕现象（screencap）+ 原文日志
   `adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'`
5. 日志 tag=`ygs`；mjava 里 `i.syso(...)` 的内容出现在这里（旧写法 `.iyu` 里的 `syso` 已按白名单禁用）。
6. 控制台行号不可信（常报第 0 行），定位靠日志与现象。
7. 结论标注：✅实测 / ⚠推测 / ❓未知。null/false/0 必须有对照锚点。

## 已验证

| 结论 | 级别 |
|---|---|
| 入口 `src/mian.iyu` 生效，载入事件触发 | ✅ |
| 载入事件格式 `<UIEventset><eventItme type="loading">…</eventItme></UIEventset>` | ✅ |
| `call(a, "mjava", "app.bind")` 能调起模块方法 | ✅ |
| `.mjava` 直接写方法（无 class），`syso()` 输出到 `ygs` | ✅ |
| 模块里 `activity` 与 `i` 是两个默认对象 | ✅ |
| `activity.findViewById(id)` 与 `i.gvs(id)` 返回同一实例 | ✅ |
| 裸 `findViewById(id)` 不存在，报 `Command not found: findViewById( int )` | ✅ |
| 模块级变量不跨 `call` 保留（两次调用都从初值开始） | ✅ |
| `call` 能传参并接收返回值 | ✅ |
| `did` 决定控件挂到哪个父容器；根子控件数/顺序与文件一致 | ✅ |
| push 改文件后重开工程，界面按新内容渲染 | ✅ |
| mjava 由 BeanShell 解释：`final`/具名 class/`0xFF`/可变参数/`bsh.*` 都会让模块失效 | ✅ |
| 匿名**类**失败并中断整个载入事件；匿名**接口实现**在 API 28 可用 | ✅ |
| `{...}` 数组字面量可用（与旧结论相反） | ✅ |
| 循环变量 `i` 不遮蔽 iApp 的 `i` 对象（API 28） | ✅ |
| `i` = `Aid_javaCode`：390 个公开方法、12 个公开字段 | ✅ |
| `i.d` 是 BeanShell 解释器，**每次 call 新建** | ✅ |
| `i.ss` 底层 HashMap 默认 null，读写直接 NPE | ✅ |
| `i.sss` 跨 call 保留，但**每次运行重置**（同 pid 也一样） | ✅ |
| `i.dim` 按前缀分派：`sss.` / `ss.` / 无前缀落 `i.a` | ✅ |
| 外部库：JAR→D8→dex、AAR 拆 classes.jar/res、DEX 直用；产物放 `apk/assets/` | ✅ |
| 开发用工程根 `/apk/assets/*.dex` 加载；打包用 assets→cache 或 `getExternalFilesDir` | ✅ |
| 带资源的 AAR：aapt2 链接用独立包 ID（≥0x7f，如 0x80）+ 生成真 R；运行时 `addAssetPath` 挂载 | ✅ |
| `DexClassLoader` 父加载器必须给 `null`：宿主 APK 自带同名类会抢走加载（iApp 自带混淆版 sora-editor） | ✅ |
| Android 14+/targetSdk≥34：动态加载的 dex 必须只读；先 `setReadOnly()` 再写，已有文件删了重建 | ✅（官方文档 + 实机） |
| 库 API 多时把 glue 编译进 dex 做桥接类，mjava 只用构造器 + `View.setTag/getTag` 交互 | ✅ |
| BeanShell 写不了「继承类」时：写 .java → javac → d8 成独立 dex，父加载器给宿主 | ✅ |
| ViewPager `onpageselected/onpagescrolled/onpagescrollstatechanged` 可用（适配器须编译类） | ✅ |
| AppBarLayout `onoffsetchanged` 可用；`st_vO` 是真实偏移量（px，负值） | ✅ |
| `i.loadjar` 只认 `apk/lib/`（VIP 付费入口），不要用 | ✅ |
| 新建工程最小集：`.project` + `AndroidManifest.xml` + `src/mian.iyu` + `icon.png`；`build.xml`/`sdk/` 由 iApp 首次打开生成 | ✅ |
| ppt 里直接写自定义类是**影子实例**，`addView`/`setPadding` 无效；必须 mjava 动态创建 | ✅ |
| 自定义类要在 `build.xml` 的 `<newControl><itme title class info/>` 登记，否则设计器显示“未知” | ✅ |
| `TextInputLayout` 必须直接包含 `TextInputEditText`；子控件用 `til.getContext()`（ContextThemeWrapper），用 `activity` 会自绘成原生外观 | ✅（A/B/C/D 矩阵） |
| 独立探针页可新建任意 `.iyu` 作为开发入口；打包只认 `mian.iyu` | ✅ |
| 交互页状态放 `i.sss`（模块变量跨 call 必丢）；布局均分用 `height=0 + layout_weight=1` | ✅ |
| `.iApp` 备份：顶层直接是工程内容，无包名目录；同包名存在时导入失败 | ✅ |
| 打包 APK：versionCode = 100000 + versionint；打包后无日志、`VisualDesigner` 被裁 | ✅ |
| 界面事件 `downkey` 方向键可用（19/20/21/22）；`st_kC` 为键码，单条入口即可（已隔离验证） | ✅ |
| `i.fn("b")` 把模块加载进当前解释器；之后可直接调 `b_method()` | ✅ |
| 未加载先调用 → `Command not found`，**整个方法中断且 `catch` 不住** | ✅ |
| `i.d.f("b.mjava")` 仅开发模式可用；打包后 `i.d` 是 `xn0`，无 `f(String)` | ✅ |
| `i.call("mjava","b.method",Object[])` 可用；每次新建解释器；void 方法不要接返回值 | ✅ |
| 同名方法后加载覆盖；子模块方法应加前缀 | ✅ |
| `.iyu` 可以直接 `call` 任意模块，不必经过 facade | ✅ |
| 多模块源码可直接打包：交付用 `i.fn`，不合并 | ✅ |
| mjava `setOnTouchListener` 匿名接口可用，回调里能调同模块方法 | ✅ |
| `ObjectAnimator.ofFloat(view, prop, new float[]{…})` 可用；`postDelayed(匿名 Runnable)` 能收尾 | ✅ |
| `activity.getFilesDir()` + 文件读写持久化，杀进程后恢复 | ✅ |
| 动态视图用 `setTag("tile:"+idx)` 跨 `call` 找回；`bringToFront()` 管弹层层级 | ✅ |
| 应用内自检：`loading` 里跑纯逻辑用例，`i.syso` 输出 PASS/FAIL | ✅ |
| 事件参数统一以 `st_*` 注入（`st_vId`/`st_vW`/`st_pN`/`st_url`/`st_eX`…）；写别的名字会退化成零参调用 | ✅（DEX + 实测） |
| 绑 `shouldoverrideurlloading` 会跳过 iApp 默认跳转（内部 return true），要跳必须自己 `loadUrl` | ✅（DEX + 实测） |
| `i.call(语言, "模块.方法", Object[])`：首参是语言不是变量名；目标 void 时不能接返回值 | ✅（探针） |
| 行内水波纹要给 `RippleDrawable` 第三个参数传圆角遮罩，否则扩散成整圆 | ✅ |
| 图标用 `Canvas` + `Path` 现画（Bitmap → ImageView），不用 emoji/文字符号 | ✅ |
| 工程图标完全由根目录 `icon.png` 决定；打包为 `res/mipmap-*/img_iapp.png`（原样，无多密度切图） | ✅ |
| 1×1 半透明蓝像素占位图会被启动器拉成纯蓝方块；用 `make_icon.py` 生成真图标 | ✅ |
| 离线图标生成 `make_icon.py`：纯标准库，不联网、不依赖 Pillow | ✅ |
| 普通 View 的 `setRotationX/Y` + `setCameraDistance` 可做 3D 倾斜（无需自定义 View） | ✅（API 28） |
| 圆角 `GradientDrawable` 背景 + `setClipToOutline(true)` 会裁掉溢出的子 View | ✅ |
| `View.animate()`（ViewPropertyAnimator）可链式调用，`cancel()` 能打断 | ✅ |
| `View.setTag(int[]/float[])` 跨 call 存视图状态，强转能取回 | ✅ |
| 多个 `.iyu` 可各自作入口；`call(null,"mjava","mod.m","str")` 传字符串参数 | ✅ |
| Canvas 现画 900×1260 卡面（含 160² 噪声、文字、金边）约 260~280 ms | ✅ |
| 径向渐变 3 段会出肉眼可见的同心环；9 段 + 256² 放大才平滑 | ✅ |
| 两套独立雷电同跑会抢宿主机 5555，`emulator-5554` 可能静默指向后启动那台（投递前用 `getprop ro.build.version.sdk` 核对） | ✅ |
| Android 11+：`/sdcard/Android/data/<pkg>` 由 app 自身 mount namespace 的 bind mount 提供；FUSE 对其它进程一律拒绝（`is_app_accessible_path`），所以不能用 `su <uid>` 派生进程模拟 app 访问 | ✅（AOSP 源码 + API 34 实机） |
| Android 11+：可在 app 自己的 `Android/data/<pkg>` 下建指向共享存储（如 `Pictures`）的符号链接，app 自身可经链接读写；写入可经 vboxsf/共享目录落到宿主机（需相应存储权限，如 `MANAGE_EXTERNAL_STORAGE` appop） | ✅（API 34 + iApp 实机） |
| 共享目录（vboxsf）本身不支持符号链接：`ln -s` 报 `Function not implemented`，链接只能建在设备 ext4/FUSE 侧 | ✅（LDPlayer14） |
| 雷电实例序号 = `vms\leidianN`，宿主端口按序号走（0→5555，1→5557）；两套安装各自的 `leidian0` 会抢 5555，把第二套改名成 `leidian1` 可永久分开，无需脚本 | ✅（2026-10-26，安卓 9 + 安卓 14 各一台） |
| `MotionEvent` 的 `getActionMasked/getActionIndex/getPointerCount/getPointerId/findPointerIndex/getX(int)` 可用 | ✅（API 28） |
| `MotionEvent.getHistorySize(int)` 等带 pointerIndex 的重载**解析失败且杀进程**，`catch` 接不住；只用无参版本 | ✅（API 28） |
| 旋转屏幕会重建页面并重跑 `loading`；`loading` 里宽高=0，`loadingComplete` 有真实尺寸；`addOnLayoutChangeListener` 可用 | ✅（API 28） |
| `View.setTag(HashMap)` 跨 call 可取回，HashMap 里可装 Bitmap/Canvas/Paint | ✅（API 28） |
| `i.sss` 能存 `int[]` / `ArrayList`，跨 call 保持 | ✅（API 28） |
| 已上屏 Bitmap 改内容后 `invalidate()` 能刷新（`Bitmap + Canvas + ImageView` 路线成立）；四种刷新均 26~28µs/次 | ✅（API 28） |

## 导航

- `references/methodology.md` — 探针方法与铁律
- `references/recipes.md` — 常用配方、持久化、自检与 API 28 注意事项
- `references/animation-guide.md` — mjava 动画（ObjectAnimator / postDelayed / 输入锁）
- `references/iapp-history.md` — 版本读数与批次定稿
- `references/iyu-whitelist.md` — iyu 只允许 call/addv
- `references/iyu-guide.md` — 界面文件结构
- `references/mjava-guide.md` — 模块写法与互调
- `references/modularization-guide.md` — 多模块拆分、`i.fn`、facade 规范
- `references/events-guide.md` — 事件类型与写法
- `references/iapp-i-reference.md` — `i` 对象成员与生命周期
- `references/external-library-guide.md` — JAR/AAR/DEX 装载、编译类进 dex、Android 14+ 只读要求
- `references/network-and-mirrors.md` — 国内网络抓文档/依赖：curl 落盘、可用镜像、离线转文本
- `references/iapp-internals.md` — 内部类、APK 结构、分析脚本
- `references/delivery-guide.md` — `.iApp` 备份、APK 打包、边界
- `references/project-structure.md` — 工程结构与新建工程
- `references/emulator-setup.md` — 模拟器环境案例：宿主工作区 ↔ Pictures 同步、安卓 9/14 工程根、多开 adb 端口冲突
- `references/icon-guide.md` — 应用图标（来源、规格、离线生成）
- `references/builtin-controls.md` — 内置短名控件清单
- `references/style-guide.md` — ppt 与 mjava 的样式分层
- `references/md-components-guide.md` — Material 组件（动态创建）
- `references/debugging.md` — 错误前缀与失败签名
- `references/pitfalls.md` — 踩过的坑
- `cases/` — 实验记录（含每轮读数与判定）
  - `cases/19-card3d-tilt-light.md` — 卡面 3D 倾斜 + 金属光斑（不用自定义 View 的伪 3D）
