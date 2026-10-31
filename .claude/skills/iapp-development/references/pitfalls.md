# 坑

## 1. 内存覆盖磁盘

iApp 编辑器以内存中的工程为准。点运行 / 保存 / 退出保存都会把旧内存写回磁盘。

**做法**：外部改源码前先 `am force-stop com.iapp.app`（或人在 iApp 里关掉工程），push 完再重新打开。

## 2. bind mount 对应用不可见（Android 9，sdcardfs）

- 挂到 `/data/media/0/...`：被 sdcardfs 挡住，`/storage/emulated/0/...` 视图是空的
- 挂到 `/storage/emulated/0/...`：shell 能看，**iApp 进程看不到**
  - 应用 namespace 由 zygote 派生，后加的挂载不传播
  - 验证方法：`grep <目标目录> /proc/<iApp pid>/mountinfo`；或 `cat /proc/<pid>/root/...`

**做法**：不要用 bind mount。通道优先级见 `environment-adaptation.md` §推荐优先级
（adb 整目录优先；共享目录自 2026-10-30 起不再作为通道）。

## 3. Git Bash 改写路径

`adb shell ls /storage/...` 会被 MSYS 改写成 `C:/Program Files/Git/storage/...`（Git for Windows 的默认安装盘；装在别处按实际）。

**做法**：`export MSYS_NO_PATHCONV=1`。

## 4. su 参数被拆散

`adb shell su -c "ls -la /data"` 到了设备上引号丢失，`su` 把 `-la` 当自己的参数。

**做法**：整段用单引号包住 `adb shell 'su -c "ls -la /data"'`；或直接 `adb root`。

## 5. 入口名

入口固定 `src/mian.iyu`（min 不是 main）。任务书里偶尔写成 `main.iyu`，以实测为准。

## 6. 状态放错地方

- `i.ss` 的底层 HashMap 默认是 null，一读一写就 NPE——不要当存储用。
- `i.d`（BeanShell 解释器）**每次 call 都是新的**，不能拿来跨 call 存变量。
- `i.sss` 只在**同一次运行**内跨 call 有效；重新运行就清零（同进程也一样）。
- 要跨运行持久化，用文件（工程 `files/` 或外部存储），不要依赖内存对象。
- 各成员的生命周期与签名见 `iapp-i-reference.md` §生命周期；能装什么见 `recipes.md` §`i.sss` 与 `setTag` 能装什么。

## 7. 自定义类控件（Material / androidx）

- **依赖子控件 Context/背景的组件（典型是 `TextInputLayout`）在 ppt 里外观会退化**：子控件由 iApp 用 activity Context 构造，拿不到 `til.getContext()` 那层 Material 主题覆盖 → 输入框看起来是普通 EditText（API 34 实测，2026-10-27）。Button / Card / Chip 等不依赖子控件 Context 的组件不受影响
- ppt 建的实例本身**是真的**：`findViewById` 返回的就是屏幕上那个（hash 与视图树一致）、`attached=true`、`addView` 生效。API 28 的“影子实例”旧结论按版本差异对待 ⚠
- **TIL 盒子默认不画**：Material 1.13 把盒子贴成 EditText 的 background，ppt 子控件自带原生背景 → 被跳过（`boxBackgroundApplied=false`）。修复必须挂在 `loading`（`loadingComplete` 会让首帧先画出无盒子的页面）；完整配方与「修完与 mjava 一致」的对照见 `md-components-guide.md` §ppt 声明的 TIL：盒子默认不画
- `TextInputLayout` 内部那层 `FrameLayout` 是它自己的 `inputFrame`（内含 `StartCompoundLayout`/`EndCompoundLayout`），**不是 iApp 套的**；旧记录归因错误
- 组合控件：**ppt 里声明父容器与子控件属历史路径**（实例真实可写），只用于历史工程与静态探针页；新页面一律 mjava 建树，见 `style-guide.md`。走历史路径时 TIL 按下面的 `loading` 配方修复，其它组件只补运行期内容
- **写完整类名（`type=` 含点号）的那一刻就登记**：`build.xml` 的 `<newControl>`，子项标签是 `itme`。设计器显示“未知”说明已经漏了；新建工程的登记不继承
- **反过来不成立**：`build.xml` 登记了某个控件、页面 ppt 却没声明它 → 设计器不崩，页面**不渲染**该控件。
  登记只解决「设计器认不认识这个类」，不会凭空创建视图 ✅（2026-10-27）
- **设计器崩溃（根因：`SearchBar` + 序列化器空 tag）**：`SearchBar` 写进 ppt 后，点运行/保存/切代码页等**触发设计器自动保存**时抛 `NullPointerException: Attempt to read from null array`（`VisualDesigner.T0:54`，2026-10-27），iApp 进程被杀
  - 根因（R8 反编译）：`T0` 把 `view.getTag()` 当 `Object[]` 读（约定 `[type,ppt,event]`）；`id >= 1` 的控件**跳过 tag 空检查**，直接 `aget-object` → NPE。`SearchBar` 构造里 inflate `mtrl_search_bar`，内部子 View 带资源 id 但没有 tag → 递归到它时崩
  - 触发条件是**保存/序列化动作**（`S0`→`R0`→`T0`），不是“打开设计器”；`S0` 有 2 秒防抖（`D8` 在 Activity 构造时赋值），刚重开时第一次保存会被跳过，看起来像“第一次正常、之后崩”
  - 与 `build.xml` 登记无关：`type` 含点号时 `if0.q` 直接反射实例化；只登记不声明连续 3 次正常，不登记只声明仍崩
  - 做法：**不要 ppt 声明 `SearchBar`**，改 mjava 动态创建（运行期不经过序列化器）；动态创建的控件也不用登记
  - 原清单里的 `TabLayout`（短名/全类名/登记与否）、`ChipGroup`（含 `Chip` 子项）、`MaterialDivider` 已实测单独 ppt 声明**不崩**，全部排除
  - 未登记的完整类名一般只让组件树显示“未知”（`TabLayout` 探针工程能开、无报错）；`SearchBar` 显示“未知”也照样会崩
  - 泛化：任何“构造时自建带资源 id 子 View”的第三方控件都可能触发同一缺陷，不止 `SearchBar`

## 8. BeanShell 解析不到某些继承方法

`Error in method invocation: Method isSingleLine() not found in class 'com.google.android.material.textfield.TextInputEditText'`

- 该方法在 TextView 上是公开的，但 BeanShell 解析失败，**整个方法会中断**
- 处理：换等价属性（如读 inputType / lineCount），或用反射调用；不要把关键流程建立在这种调用上

### 8.1 重载解析失败会杀进程（API 28 实测）

`MotionEvent.getHistorySize(int)` / `getHistoricalX(int,int)` 这类带 pointerIndex 的重载在 BeanShell 里找不到；
无参 / 单参版本反而能用。在 `OnTouchListener` 回调里调用它时：

```
E/AndroidRuntime: FATAL EXCEPTION: main
java.lang.reflect.UndeclaredThrowableException
  at $Proxy3.onTouch(...)
Caused by: Error in method invocation: Method getHistorySize( int ) not found ...
W/System.err: call killProcess callstack! pid=3039
```

- **`catch (Throwable)` 接不住**，异常穿透匿名接口代理，iApp 直接 killProcess
- 同一回调里排在它前面的 `getActionMasked/getActionIndex/getPointerId/findPointerIndex/getX(int)` 都正常
- 做法：只用无参 `getHistorySize()`（对应 pointer 0）；要按指针取历史点就另想办法
- API 28 实测（2026-10-26）
- 同类签名：在匿名 `Runnable` / 接口回调里对 **null 数组取下标**（如 `((Object[]) view.getTag())[0]`），
  BeanShell 抛 `Typed variable declaration : Not an array`，穿成 `UndeclaredThrowableException` 并杀进程，
  `catch(Throwable)` 接不住（2026-10-27，API 34）

## 9. 把短类名当成“去包名”

`type="Switch"` 设计器显示“未知”——`Switch` 不在内置短名表里，运行时可能正常，但设计器不认识。

- 短名清单以 `builtin-controls.md` 为准，不要维护第二份
- 其它类写完整类名（如 `android.widget.Switch`）并在 `build.xml` 的 `<newControl>` 登记
- 判据：设计器显示“未知”就是短名不存在或未登记

## 10. 竖向布局“堆在顶部”，不铺满

根 `height=-1` 但子行都写 `height=-2` 时，内容只占顶部，底部留白。

要均分剩余高度：

```xml
<!-- 行 -->
<ppt>height=0
layout_weight=1</ppt>

<!-- 行内按钮 -->
<ppt>width=0
height=-1
layout_weight=1</ppt>
```

## 11. DrawerLayout 必须精确尺寸

`width=-2 height=-2` 会让整个页面闪退：

```
java.lang.IllegalArgumentException: DrawerLayout must be measured with MeasureSpec.EXACTLY.
```

给固定 dp（如 `300dp`）或精确的 match 尺寸，并单独隔离测试。

## 12. mjava 里按 `android.widget.*` 猜导入，类根本不存在

`SwipeRefreshLayout` 的正确类是 `androidx.swiperefreshlayout.widget.SwipeRefreshLayout`，写成 `android.widget.SwipeRefreshLayout` 直接：

```
Typed variable declaration : Class: SwipeRefreshLayout not found in namespace : at Line: 19
```

- 短名表里的“实际类”就是导入路径，照抄；GifView→`pl.droidsonroids.gif.GifImageView`、TabLayout/RoundImageView→`com.iapp.app.*` 同理
- 这类报错是**运行期**的：同一函数里它之后的代码全部不执行，但它之前的代码已经生效（`setProgress` 已经触发过回调）
- 所以初始化函数要**按块 try/catch**，一块写坏不能拖累其它控件

## 13. 绑了 `shouldoverrideurlloading`，WebView 链接就不跳了

`run/mian$i0.shouldOverrideUrlLoading` 的逻辑：

- **没绑**这个事件 → iApp 默认处理：`http/https/rtsp/ftp` 在 WebView 内 `loadUrl`，其它 scheme 走 `ACTION_VIEW`
- **绑了** → 执行完 yul 代码**直接 return true**，默认跳转被跳过，`ondownloadstart` 也等不到

所以“链接没反应”不是 HTML 的问题，是自己绑了事件却没写跳转。要跳就在事件里自己 `loadUrl`：

```xml
<eventItme type="shouldoverrideurlloading">call(null, "mjava", "br.override", st_url)</eventItme>
```

另外一个坑：参数变量必须写 `st_url`。写 `url` 会变成未定义变量，调用退化为零参：

```
JavaErr：Method override() not found in bsh scripted object: global
```

## 14. `i.call` 的三个坑

正确用法与适用边界见 `mjava-guide.md` §跨模块调用 `i.call`；本节只列失败形态。

```java
i.call("mjava", "pick.show", new Object[]{…});
```

- **第一个参数是语言**，不是变量名：传 `null` → `NullPointerException: … String.equals`；传 `""` → 静默不执行、不报错
- **第二个参数必须带模块名**（`"pick.show"`），只写方法名会拼出 `.mjava`
- **目标是 void 方法时不要赋值**：`Object r = i.call(...)` → `Typed variable declaration : Void initializer.`，而且**整个方法立刻中止**，后面的语句全不执行

## 15. `String.valueOf(null)` 在 BeanShell 里会炸

```
NullPointerException: Attempt to get length of null array
    at java.lang.StringFactory.newStringFromChars
    at java.lang.String.valueOf(String.java:2912)
    at bsh.Reflect.invokeStaticMethod
```

BeanShell 解析 `String.valueOf(x)` 时，如果 `x` 是 `null`，会选到 `valueOf(char[])` 重载，对空数组取长度直接 NPE。

最常见的触发点：`String.valueOf(i.sss("key"))`，而该 key 还没赋值。

```java
// 错误
String v = String.valueOf(i.sss("pick.sel"));
// 正确
Object o = i.sss("pick.sel");
String v = (o == null) ? "" : String.valueOf(o);
```

建议每个模块都放一个 `str(Object)` 小工具，凡是可能为 null 的值都走它。

## 16. 日志过滤

只抓 `ygs` 与 `System.err`：

```
adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'
```

`System.err` 里的 `Toast callstack!` 是 iApp 自己打印提示用的，不是错误。

退出运行预览时还会出现一组：

```
java.lang.IllegalArgumentException: View=... not attached to window manager
  at com.iapp.app.VisualDesigner$i1.handleMessage
```

这是 iApp 拆预览悬浮窗的噪音，与本工程代码无关，不要当 crash 查。

## 17. `downkey` 不传 `st_kC` 就不知道按了哪个键

`downkey/upkey` 事件体有三个内置变量：`st_kC`（键码）、`st_eA`（动作）、`st_eR`（重复计数）。
只写 `call(null,"mjava","x.y")` 也会触发，但 mjava 拿不到键码。

```xml
<eventItme type="downkey">call(null, "mjava", "game.keyCode", st_kC)</eventItme>
```

同时挂 `setOnKeyListener` 会双触发，需要按 `(键码, 120ms)` 去抖。
绑了 `downkey` 之后返回键会被吞、要自己 `activity.finish()`，见 `navigation-guide.md` §返回。

## 18. 动画收尾不要用 `AnimatorListenerAdapter`

它是**抽象类**，BeanShell 只能匿名实现接口，写 `new AnimatorListenerAdapter(){...}` 会让模块失效。
用 `view.postDelayed(new Runnable(){ public void run(){ nextStep(); } }, 120)` 收尾。
详见 `animation-guide.md`。

## 19. 动态视图跨 `call` 会“丢”

模块变量在每次 `call` 都重置，`ArrayList<View>` 这类字段存不住。
动态加的视图用 `setTag("tile:"+idx)`，之后遍历 `getChildCount()/getChildAt(k)` 按 tag 找。

## 20. `getFilesDir()` 是多工程共用的

开发模式下它指向 iApp 宿主 `com.iapp.app` 的私有目录，不是当前工程目录；
打包后是打包应用自己的私有目录。
开发模式存档文件名要带工程前缀（如 `game2048.save`），否则不同工程会互相覆盖；
反例：把存档写成 `save.txt`，两个工程一起跑就串了。

## 21. 1×1 占位图 = 纯蓝方块

早期 `create_project.py` 写的 70 字节 `icon.png` 注释是“透明”，实际像素是
RGBA `00 00 FF 7F`（半透明蓝）。启动器把它拉满整个图标，所有工程都是蓝方块。

- 判据：`icon.png` 只有几十字节、尺寸 1×1
- 做法：用 `scripts/make_icon.py` 生成 512×512 真图标
- iApp 打包时把 `icon.png` 原样塞进 `res/mipmap-*/img_iapp.png`，没有多密度切图
- 桌面图标有缓存，换图后要重新打包安装才看得到

详见 `icon-guide.md`。

## 22. 跨模块调用前没 `i.fn`

新一次 `call` 是新的 BeanShell 解释器，上一次加载的模块**不在了**。
在 `importAll()` 之前调用 `u_st()` 这类子模块方法：

```
Command not found: u_st( java.lang.String ) : at Line: 60 ...
Called from method: layout
```

**整个方法中断，`catch(Throwable)` 接不住**，后面的渲染/逻辑都不执行。

做法：

- facade 的每个 public 入口**第一行** `importAll()`
- `importAll()` 里 `i.fn("模块名")`（不带 `.mjava`）
- 用模块级 `G_IMPORTED` 标记“本次 call 已加载”
- 不要先做 `if (u_st(...))` 再加载
- 详见 `modularization-guide.md`

## 23. `i.d.f` 只在开发模式可用，交付用 `i.fn`

开发模式 `i.d.f("x.mjava")` 能按文件名导入；打包 APK 后：

```
Method f( java.lang.String ) not found in class'xn0'
```

- `i.d` 变成混淆类 `xn0`，`f` 是 **Context 字段**，不是导入方法
- `i.call` 不是不能用：正确顺序是 `i.call("mjava","x.method",Object[])`；
  它每次新建解释器，跨模块加载优先 `i.fn`
- **正确做法**：`i.fn("x")`，源码直接打包，不合并

```java
i.fn("b");
b_hello();
```

- 详见 `modularization-guide.md`

## 24. 外部 AAR 的 R 全是 0，构造里就要资源 → 必须自己链资源

AAR 里的 `R.txt` 全是 `0x0`（真实 ID 在宿主 App 链接时才分配）。如果库在**构造期**
就用 `R.layout.*`（sora-editor 的 `CodeEditor` 构造 → `EditorTextActionWindow` →
`inflate(R.layout.text_compose_panel)`），不链资源直接 `new` 必崩：

```
Resources$NotFoundException: Resource ID #0x0
```

做法（完整脚本见 `scripts/build_sora_dex.py`）：

1. `aapt2 compile --dir res -o compiled.zip`
2. `aapt2 link -I <framework-res.apk> --package-id 0x80 --java gen …`
   - **包 ID 必须 ≥ 0x7f**（aapt2 拒绝 0x7e），宿主是 0x7f，所以用 0x80
   - 没有 `android.jar` 时，可以用设备上 pull 的
     `/system/framework/framework-res.apk` 当 `-I`（实测可用）
3. `javac --release 11` 编译生成的 `R.java`，打进 dex（**先剥掉 AAR 自带的 `R*.class`**）
4. 运行时 `activity.getAssets().addAssetPath(资源apk路径)`（反射，hidden API，实测可用）

完整链路、资源不自足的库与打包差异见 `external-library-guide.md` §带资源的 AAR。

## 25. `DexClassLoader` 父加载器：宿主自带同名库时给 `null`

```java
// ❌ 宿主 APK 里若自带同名类，父优先委派会先命中它
new DexClassLoader(dex, cacheDir, null, activity.getClassLoader());
// ✅ 只用 boot classpath + 自己的 dex
new DexClassLoader(dex, cacheDir, null, null);
```

反过来，编译类依赖 `androidx.*` 或宿主已有类型时，父加载器要给宿主 loader（见 `external-library-guide.md` 的「编译类进 dex」）。

实测：宿主 `com.iapp.app` 的 APK **自带一份混淆过的 sora-editor**
（`base.vdex` 里能看到 `io.github.rosemoe.sora.widget.CodeEditor.p3`）。
父加载器给宿主时，`loadClass("io.github.rosemoe.sora.widget.CodeEditor")` 拿到的是宿主那份：

| 现象 | 说明 |
|---|---|
| 方法表完整（共 953、声明 325），但按名字一个都查不到 | 自有方法名被混淆成 `A`/`A0`/`p3` 之类 |
| 继承自框架的方法名正常（`getTextDirection` 等） | 只有该类**声明**的方法被改名 |
| `Class.getMethod("getText")` → `NoSuchMethodException` | 同上 |
| 按签名能找到并调用，但行为怪（字号乱、语言没设上） | 命中的是混淆版同签名方法 |
| 编译进 dex 的桥接类直接 SIGSEGV | 方法 id 解析到语义不同的混淆方法 |

打包版没有宿主干扰，所以同一份 dex 一切正常——**排查时先比较「开发 vs 打包」**。
自检写法：`ce.getDeclaredMethod("setTextSizePx", new Class[]{Float.TYPE})` 能找到 = 用的是自己的。
父加载器选择规则见 `external-library-guide.md` §运行时加载。

## 26. 重载族不能只靠「参数类型 + 返回类型」定位

方法名不可信时（见 #23 之外的场景），按签名匹配看似可行，但对同签名族会错位：

- `(float) -> void`：`setTextSize` / `setTextSizePx` / `setTextScaleX` / `setDividerWidth` …
- `(boolean) -> void`：`setEditable` / `setWordwrap` / `setLineNumberEnabled` / 一堆 `set*Enabled`

命中哪个取决于方法表顺序，结果就是「文本进去了但字号失控、语言没设上」。
**正解：把 glue 编译成 dex 里的桥接类**，编译期解析方法引用；mjava 只跟桥接类打交道，
而且只用两种入口——构造函数（按参数类型取）和框架方法（`View.setTag` / `View.getTag`）。
桥接类写法见 `external-library-guide.md` §编译类进 dex。

## 27. Android 14+：动态加载的 dex 必须是只读文件

targetSdk ≥ 34 的应用在 Android 14（API 34）及以上，`DexClassLoader` 加载的
dex/jar/apk **必须是只读文件**，否则系统直接抛异常（行为变更「Safer dynamic code loading」）。
iApp 打包的 targetSdk 是 36，所以在 Android 14/15 实机上必踩；Android 9 上没这条限制，
**本地测不出来**。

典型触发：把 dex 复制到 `getCacheDir()`（默认可写）后直接加载。

```java
// ❌ 写完就加载：文件仍可写
FileOutputStream fo = new FileOutputStream(d);
fo.write(bytes); fo.close();
new DexClassLoader(d.getAbsolutePath(), …);

// ✅ 官方顺序：打开输出流 → setReadOnly() → 写 → 关闭 → 再设一次
if (d.exists()) { d.setWritable(true); d.delete(); }
FileOutputStream fo = new FileOutputStream(d);
d.setReadOnly();
fo.write(bytes); fo.close();
d.setReadOnly();
new DexClassLoader(d.getAbsolutePath(), …);
```

要点：

- 限制的是「文件可写」，**不是目录**；换 `getCodeCacheDir()` 不一定能绕过
- 已存在的只读文件必须先 `setWritable(true)` + `delete()` 再重建，否则写不进去
- 官方推荐「先设只读再写」，而不是写完再改权限（消除竞态）
- 同一个 dex 既要被开发模式又要被打包模式加载时，两条路都要经过这套流程

版本要求与完整顺序见 `external-library-guide.md` §Android 14+ 的 DCL 只读要求。

## 28. 多开模拟器：`emulator-5554` 会指向错误的设备

两套**独立安装**的雷电（如 `LDPlayer9` + `LDPlayer14`）各自只有 `index=0`，VM NAT 规则都是
`adb,tcp,,5555,,5555`，同时运行就抢宿主机 5555——**后启动的那台赢**。

实测（LDPlayer 9.5.42.0 / 14.0.32.1，2026-10-26）：

- LD14 启动前 `adb shell` 读到 Android 9；LD14 启动后，连 LDPlayer9 自带的 `ldconsole adb` 都读到 Android 14
- `adb devices` 里 `emulator-5554` 和 `127.0.0.1:5555` 可能是同一台 Android 14，名字却不提示

端口分配规则与「改名 `leidian1` 永久分开」的做法见 `emulator-setup.md` §5。
- 危险点：`adb push` / `pm install` 静默落到错版本上，以为是 API 28 其实是 API 34

**做法**：

- 每次投递前先核对：`adb -s <serial> shell getprop ro.build.version.sdk`
- 需要同时用两台：运行时 `VBoxManage controlvm <vm-uuid> natpf1 delete adb` 再用
  `natpf1 "adb,tcp,,5557,,5555"` 改宿主端口（重启失效，需重加）
- 两台同时开时不要依赖 `emulator-5554` 这个名字，统一用 `127.0.0.1:<端口>` 显式指定
- 只开一台时，先启动你要用的那台，再启动另一台就会把 5555 抢走

## 29. `layout_gravity` 在 ppt 里不生效，圆屏要对齐必须走 mjava

**适用范围**：只在「用 ppt 声明控件」这条路径下成立；默认的 mjava 建树范式不涉及——
摆位一律走 `LayoutParams`（`ui-kit` 的 `ui_fplace` 已封装），见 `references/style-guide.md`。

**版本**：不限于旧系统。2026-10-29 打包版 / API 30 手表首见，
2026-10-30 在 **API 34 开发模式（1080×1920）** 复现，属于 ppt 语义本身的问题。
**级别**：✅（两个版本各复现一次）

实测现象：`FrameLayout` 下三个子控件分别写了 `layout_gravity=center`、
`top|center_horizontal`、`bottom|center_horizontal`，运行后**全部堆在 (0,0)**，
`layout_gravity` 被忽略（`width/height` 生效），且**没有任何报错**。

做法：在 mjava 里用 `LayoutParams` 摆：

```java
FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(ui_dp(165), ui_dp(165));
lp.gravity = Gravity.CENTER;
view.setLayoutParams(lp);
```

**圆屏安全区**：直径 D 的圆里最大的内接正方形边长 = `D / √2`。
466px 屏 → 330px（165dp @density 2）；内容按这个方框居中，四角才不会被裁。
`layout_gravity` 的旧写法不要指望，写完都要在真机截图上确认一次。

## 30. 事件里带 `0` 调 mjava，方法签名必须接这个参数

`.iyu` 的事件体常写成 `call(null, "mjava", "mod.method", 0)`。这个 `0` 是**实参**：
目标方法若不接收参数，会报方法找不到并**静默中断**（打包版 `ygs` 是死的，看不到任何提示）。

实测（2026-10-29，手表工程）：

```xml
<!-- 事件体 -->
<eventItme type="clicki">call(null, "mjava", "watch_reader.menu", 0)</eventItme>
```

```java
public void menu() { ... }         // ❌ 不执行，无日志、无异常
public void menu(Object arg) { ... }  // ✅ 正常
```

对照：同一工程里 `loading` 事件的 `call(null, "mjava", "watch_reader.boot")`
**不带参数**，配 `public void boot()` 正常 —— 判据是「事件体有没有实参」，不是事件类型。

**做法**：
- 事件体里带了 `0`（或任何实参），被调方法就写 `public void xxx(Object arg)`；
  `clicki` / `downkey` 这类习惯性带参的入口一律按带参写
- 阅读器示例工程手机版的 `prev/next/settings/back` 全是 `Object arg`，就是这个原因
- 排查时不要只看 `logcat`：这条失败**不打印任何东西**。要么给方法加 `android.util.Log`，
  要么干脆在 mjava 里 `setOnClickListener` 挂监听（本书架/菜单页最终采用的方案）

## 31. 后台线程的匿名 Runnable 里调模块方法，必须先 `i.fn`

实测（2026-10-29，打包版 / API 30，手表阅读器示例）：

```
E/AndroidRuntime: FATAL EXCEPTION: Thread-10
E/AndroidRuntime: java.lang.reflect.UndeclaredThrowableException
  at $Proxy3.run(Unknown Source)
Caused by: Typed variable declaration : Command not found:
  core_readPage( java.lang.String, int, int, int ) : at Line: 315
  Called from method: run
```

现象：方法入口 `i.fn("qj_core")` 已经写过，主线程调用正常；但
`new Thread(new Runnable(){ public void run(){ core_readPage(...) } })`
一执行就报 `Command not found`，并被包成 `UndeclaredThrowableException` **直接杀进程**
（不是只中断本次调用）。

**做法**：**在 Runnable 内部第一行再 `i.fn("模块名")`**，不要指望外层 import 穿透到线程闭包。
`activity.runOnUiThread(new Runnable(){...})` 里的 UI 回调同理：回调里要调其它模块方法，
就得先 `i.fn`。排查要点：这条只在子线程崩，主线程完全正常，异常线程名是 `Thread-N` 而不是 `main`。

## 32. 系统栏预留量在「根的直接父容器 padding」上，改 Window 无效

实测（2026-10-30，雷电 14 / API 34 / 1080×1920）：目标是「状态栏保留可见，但内容铺到屏幕顶边」。

- 三代原生写法全部失败：`setDecorFitsSystemWindows(false)` 不改起点；遍历祖先清
  `padding` / `fitsSystemWindows` / `clipToPadding` 会被宿主下一轮布局加回；延迟清也一样
- 预留量在**根的直接父容器**上：实测祖先链最内层是 `LinearLayout[pad 0,72,0,0 fsw=false]`，
  一路到 `DecorView`；根 `y=72 h=1848`

**做法**：不跟它对抗，绕过它——读根被顶下去的距离 → 父容器关 `clipToPadding` →
根 `translationY` 上移同距离、高度补成屏幕高。上移后安全区的差值公式会自动把正文留在状态栏下方，
不需要额外常量。封装在 `ui.mjava` 的 `ui_edgeToEdge()` / `ui_bleed()`。
配方与形态选择见 `status-bar-guide.md`，函数说明见 `ui-kit.md` §窗口姿态。

**级别**：✅（三色对照：窗口背景绿、内容顶橙，状态栏显示橙，证明内容真的透到后面）。

## 33. 同模块同名方法后定义覆盖先定义，令牌 getter 撞上工厂会自我递归

现象：`loading` 里秒崩，`StackOverflowError`，`logcat` 里一条 `ygs` 都没有（崩在模块求值阶段）。
堆栈里 `bsh.BSHVariableDeclarator` → `BSHAllocationExpression` → `BshMethod.invokeImpl` 反复出现。

原因：同一个 `.mjava` 里定义了两个同名方法，后一个覆盖前一个。典型撞法是
「颜色令牌 `th_rule()` 返回 `#E4E4E0`」和「分隔线工厂 `th_rule()` 返回 View」同名，
而工厂体内又写 `ui_color(th_rule())` 取色 —— 调回自己，每层都正好是
「声明变量 + `new` + 以自身调用作参数」，和堆栈形态完全对得上。

对策：

- 取值令牌与造视图工厂分开命名：令牌加后缀（`th_ruleHex()`），工厂用动词/名词（`th_rule()`）
- 提交前扫一遍重名（同模块内；跨模块加载后也在同一命名空间）
- 匿名内部类的 `onClick` / `run` 不参与这个覆盖（类作用域），别被静态扫描吓到

**级别**：✅（2026-10-30，API 34）

## 34. 从回调里抛出的 `Command not found` 会直接崩进程

现象：点某个控件，进程直接没了。`AndroidRuntime` 是
`java.lang.reflect.UndeclaredThrowableException`，`Caused by: Command not found: ui_stroke( int, java.lang.String, int, android.view.View )`。

原因：调了一个实参类型对不上、因而不存在的方法（例：把返回 View 的工厂当成颜色字符串传进去）。
BeanShell 抛 `Command not found`，代理类把它包成 `UndeclaredThrowableException` 抛到主线程，
没人接就崩。

对策：

- 不要把它理解成「方法不执行、界面没反应」——**从回调抛出的这条会崩进程**
- 报错原文带着**实参类型列表**，对着方法签名逐个核对，通常一眼能看出哪个实参类型不对
- 令牌与工厂别用同名家族（见 #33）

**级别**：✅（2026-10-30，API 34）

## 35. `RippleDrawable` 不给遮罩，涟漪会扩散成整圆

现象：列表行点下去，水波纹是一个完整的圆，超出行的边界。

原因：`new RippleDrawable(color, content, null)` 第三个参数传 `null` 时没有形状约束，
涟漪以触点为圆心、半径不受控件边界裁剪。修法与圆角遮罩示例见 `style-guide.md` §波纹。

对策：给第三个参数传一个与控件形状一致的 mask（`GradientDrawable` 纯色即可，只有 alpha 参与遮罩）：
直角行用直角、圆角按钮用同半径、圆形按钮用 `OVAL`。

**级别**：✅（2026-10-30，API 34）

## 36. 点击回调也是新解释器，跨模块调用前要自己 `i.fn`

现象：页面首次渲染正常，一旦点按钮/切 Tab 就崩，`UndeclaredThrowableException`，
`Caused by: Command not found: ct_build(...)` / `book_page(...)`。
`first()` 里明明写过 `i.fn("widgets")`。

原因：`loading` 里加载的模块**不会穿透到事件回调**。每个 `onClick` / `Runnable` /
`runOnUiThread` 闭包都是新的解释器上下文，只有它自己 `i.fn` 过的模块才可见。
这与 #31（线程）是同一机制的不同入口，容易被当成「首次渲染对了就说明加载没问题」。

对策：把依赖收敛成每个模块一个 `wire()`（`i.fn` 一串），**在每个可能被事件触发的公开入口第一行调用**，
而不是只在 `first()` 里调一次。facade 写法与 `importAll` 位置见 `modularization-guide.md`。

**级别**：✅（2026-10-31，API 34，某书刊阅读 App）

## 37. `ScrollView` / `HorizontalScrollView` 没有 `LayoutParams` 内部类

现象：模块**解析阶段**就失效，页面整块空白或退化成左上角堆叠。
`System.err` 里是：`No static field or inner class: LayoutParams of class android.widget.HorizontalScrollView`。

原因：`ScrollView` 与 `HorizontalScrollView` 都直接继承 `FrameLayout`，没有定义自己的
`LayoutParams`。写 `new ScrollView.LayoutParams(...)` 在 javac 能过、在 BeanShell 解析失败。

对策：凡是「容器继承自 FrameLayout、但没重定义 LayoutParams」的控件，一律用
`new FrameLayout.LayoutParams(w, h)`。已知安全的：`LinearLayout` / `FrameLayout` /
`RelativeLayout` / `DrawerLayout`（androidx）各有自己的。

**级别**：✅（2026-10-31，API 34）

## 38. WebView 的缩放与视口开关在 `WebSettings` 上

现象：进阅读页立刻崩，`Caused by: Method setSupportZoom( boolean ) not found in class'android.webkit.WebView'`。

原因：`setSupportZoom` / `setBuiltInZoomControls` / `setDisplayZoomControls` /
`setUseWideViewPort` / `setLoadWithOverviewMode` 是 `WebSettings` 的方法。
`setHorizontalScrollBarEnabled` / `setVerticalScrollBarEnabled` / `setLongClickable` /
`setOverScrollMode` / `setBackgroundColor` 才是 `WebView` 自己的。

对策：

```java
WebSettings ws = wv.getSettings();
ws.setSupportZoom(false);
ws.setBuiltInZoomControls(false);
ws.setDisplayZoomControls(false);
ws.setUseWideViewPort(false);
ws.setLoadWithOverviewMode(false);
```

注意 `android.webkit.WebSettings` 要写在文件顶部 `import`，不能出现在 `new` 或类型声明的全限定名里。

**级别**：✅（2026-10-31，API 34）

## 39. `setLineSpacing` 的倍率是叠乘在字体行高之上的

现象：给 `TextView` 设了 `setLineSpacing(0, 1.4f)`，多行文字之间空得离谱，
比段落之间的外边距还大；按 `字号 × 倍率` 手算的行高又偏小，第二行被裁掉。

原因：`setLineSpacing(额外像素, 倍率)` 的倍率乘的是**字体自身行高**（中文约 1.16 em），
不是字号。13sp × 1.16 × 1.4 ≈ 21sp，而汉字只占 13sp，多出来的 8sp 全是行间空白。

对策：

- 测量一律用 `TextView.getLineHeight()` 实测，**不要手算**
- 窄容器里的短文本（书名、标签）**不叠加倍率**，层级靠**块间外边距**做：
  块内用字体默认行距（紧），块与块之间加 8dp（松）
- 成段正文才需要 1.4 以上的倍率

**级别**：✅（2026-10-31，API 34）

## 40. 状态栏区域的颜色来自「宿主内容容器」的背景；要内容铺进去得把根挂到 DecorView

现象（2026-10-31，STATBAR-1~3，雷电 14 / API 34 / 1080×1920）：

- 经典写法 `decor.setSystemUiVisibility(8192)` + `w.addFlags(67108864)`
  （`LIGHT_STATUS_BAR` + `FLAG_TRANSLUCENT_STATUS`）之后，`rootY` 恒为 72，内容没进状态栏；
  `getStatusBarColor()` 前后都是 `0`——**iApp 的状态栏本来就是透明的**，translucent flag 不是前提
- 把 DecorView 背景轮换成 6 种色，状态栏那块灰条不变；把根的全部祖先（a0~a7）背景一起轮换，
  灰条跟着变，`a0:LinearLayout padT=72 h=1920 bg=<轮换色>` —— 灰条画在宿主内容容器 a0 上，
  不是窗口背景，也不是系统栏自己
- 给 a0 设背景色 = 状态栏与页面同色（视觉沉浸）；把根挂到 DecorView = 内容铺满整屏，状态栏浮在内容上

挂根的做法（核心 5 行）：

```java
View root = activity.findViewById(1);
ViewGroup old = (ViewGroup) root.getParent();
old.removeView(root);
FrameLayout decor = (FrameLayout) activity.getWindow().getDecorView();
decor.addView(root, new FrameLayout.LayoutParams(-1, -1));
// 图标明暗不要在这里设：View 位在 API 34 上改不出可见变化，见 status-bar-guide.md §2.5
```

图标明暗走 `WindowInsetsController.setSystemBarsAppearance(...)`，**不要用 `setSystemUiVisibility(8192)`**：
API 34 上设/清 8192 前后屏幕无差异，真正生效的是 insets 控制器（`status-bar-guide.md` §2.5）。
本段早期写法是无条件 `| 8192`，在深色页面上会得到看不见的深色图标。

❓ **其它 iApp / Android 版本是否同样如此未验**。怎么验：进页面后先打
`getSystemUiVisibility()`，再用 `setSystemBarsAppearance` 设一次深色图标、清一次，截图比对图标颜色。

实测：`rootY 72→0`、`rootH 1848→1920`，色带出现在状态栏图标后面；事件与 `findViewById` 照常。

边界：

- 根铺满后**同时盖住底部导航栏**，正文要自己按 insets 留安全区（`insetTop` 仍报 72，可读）
- ✅ 打包 APK、pause/resume 后保持、`addv` 内嵌页均已验（2026-10-31）
- 改的是宿主 Activity 的视图层级：可先只对「以画面为主体」的展示页启用，正文页继续用
  `ui_bleed`（translationY）兜底

**级别**：✅ 开发模式（API 34）/ ❓ 打包与多页边界

## 41. `DrawerLayout` 必须当根容器包住内容，不能当浮在全屏上的浮层

现象：抽屉第一次能打开，关掉之后**整个页面点不动**——底栏、正文、任何按钮都没反应，
看起来像被一层透明的东西盖住了，并且再也打不开抽屉。

原因：`DrawerLayout.onTouchEvent()` 恒返回 `true`。把它 `addv` 到一个全屏 overlay 层、
浮在别的视图上面时，只要它进了树，无论抽屉开没开，它都会把落到自己身上的
`ACTION_DOWN` 吞掉，下层视图再也收不到事件。这与控件「可见性」无关：抽屉关着也不放行。

对策：让 DrawerLayout **只有一个实例、包住本页内容**

```java
DrawerLayout dl = new DrawerLayout(activity);
dl.addView(content, new DrawerLayout.LayoutParams(-1, -1));   // 第 1 个 child = 页面内容
dl.addView(panel, panelLp);                                    // 第 2 个 child = 抽屉
host.addView(dl, new FrameLayout.LayoutParams(-1, -1));        // dl 整体作为页面根
```

这样它拦截的正好是内容区自己的点击，不会越过边界。不要用「抽屉关闭后 `setVisibility(GONE)`」
打补丁：既打断关闭动画，重新 `VISIBLE` 后 `openDrawer` 还要等一次布局。

配套：见 #11（必须精确尺寸）与 #42（跨页面复用实例）。

补充（2026-10-31）：`isDrawerOpen()` 在**滑出/收起动画途中仍返回 `false`**（它只认「已完全打开」）。
用「按返回先收抽屉」这类判断会漏掉正在弹出的半途，表现为返回键直接把页面关掉。
兜底：抽屉完全收起时 `drawerView.getLeft() == -width`，`getLeft() > -width` 即「正在或已经弹出」。

**级别**：✅（2026-10-31，API 34，某书刊阅读 App 阅读页目录抽屉）

## 42. `ui_reg` 的句柄在同一次运行的多个页面间共享，复用旧 View 会崩

现象：进阅读页 → 退出 → 再进同一本（或换一本），崩在
`java.lang.IllegalStateException: The specified child already has a parent. You must call
removeView() on the child's parent first.`，栈顶就是 `host.addView(dl, …)`。

原因：`i.sss` 只在**重新运行**时重置，切换 `.iyu` 页面不清表。上一页用 `ui_reg` 存下的
View 还挂在旧的 `safe` 上（`ui_init` 只清当前根的子控件，不会去摘别的页面里的树），
所以 `ui_get("xxx") != null` 拿到的是**上一个页面的实例**，且 `getParent() != null`。

连带坑：只对「容器」复用时更隐蔽——不报错，但 `removeAllViews()` / `addView` 全作用在
上一页的视图上，表现为「新页面数据不显示、旧页面莫名变化」。

对策：

- **页面自己的句柄一律在 `first()` / `build()` 里重新 `ui_reg`**，不要用「已存在就复用」的惰性写法
- 确实要复用的，先 `View p = old.getParent(); if (p != null) p.removeView(old);`
- 判断「是不是本页的」只看 `getParent()` / 是否在当前根树下，不要靠 `ui_get != null`

**连带坑：`ui_init()` 注册的 `bg` / `safe` / `overlay` 也是全局键**（2026-10-31 补充）。
每个页面 `ui_init()` 都会覆盖它们，于是从任何别的 `.iyu` 返回后，**不走 `ui_init` 的重建**
（换主题、切 Tab 触发的壳重绘）会画进上一页已销毁的视图树里：不报错、日志照常、
界面纹丝不动——表现成「点了没反应」，而且「没进过别的页面前一切正常」。

判别：`ui_layer("safe").getContext() != activity` 就说明句柄被串页了
（View 的 context 就是创建它的那个 Activity）。做法：页面 `resume` 时先判一次，
串了就 `ui_init(ui_root())` 重新注册三层，再重建内容。

**级别**：✅（2026-10-31，API 34，某书刊阅读 App 阅读页重进；连带坑为同日从阅读页返回后换主题失效）

## 43. BeanShell 绑不上 Java 的**变参**方法，`try/catch` 也接不住

现象：点按钮直接崩，`java.lang.reflect.UndeclaredThrowableException`，
`Caused by: Typed variable declaration : Error in method invocation:
Static method ofFloat( android.widget.LinearLayout, java.lang.String, float, float ) not found
in class 'android.animation.ObjectAnimator'`。

原因：`ObjectAnimator.ofFloat(Object, String, float...)` 是**变参**。BeanShell 按实参逐个匹配方法，
不会自动打包成 `float[]`，于是找不到签名。同类风险：`setIndicatorColor(int...)`（#样式注意里那条）、
`ofPropertyValuesHolder(...)`、各种 builder 的可变参数重载。

关键点：这个异常是 `bsh.EvalError`，**`try/catch(Throwable)` 接不住**，
所以「包一层 try 就没事」的直觉在这里失效——它照旧穿出去把整个事件打断。

对策：避开变参 API，改用**定参**的等价物

| 想做的事 | 别写 | 改写 |
|---|---|---|
| 位移/透明度动画 | `ObjectAnimator.ofFloat(v, "translationY", a, b)` | `v.animate().translationY(b).setDuration(180).start()` |
| 无限循环扫动 | `ObjectAnimator` + `setRepeatCount(INFINITE)` | `new TranslateAnimation(0f, x, 0f, 0f)` + `setRepeatCount(Animation.INFINITE)` + `v.startAnimation(a)` |
| 进度条配色 | `setIndicatorColor(int)` | `setIndicatorColor(new int[] {color})` |

判据：签名里出现 `T...` 的一律先查定参重载；实在没有，就换组件或换 API。

**级别**：✅（2026-10-31，API 34，某书刊阅读 App Aa 面板与加载扫动线，两次撞同一处）

## 44. framework 类的静态常量未必解析得到，拿不准就传字面量

现象：切到图书/期刊 Tab 时整页构建中断，日志是

```
No static field or inner class: JUSTIFICATION_MODE_INTER_WORD of class android.widget.TextView
```

而 `TextView.setJustificationMode(int)` 本身在 API 26+ 是存在的——**方法有、常量取不到**。

原因：BeanShell 解析 `类名.常量名` 走的是自己的名字解析，不是编译期常量折叠。
`Gravity.CENTER` / `View.VISIBLE` / `MotionEvent.ACTION_DOWN` / `WindowInsets.Type.systemBars()`
这些常用的能过，但**不是所有 framework 常量都能过**（material 库自己的常量如
`TabLayout.MODE_SCROLLABLE` 目前没出过问题）。

对策：

- 常量拿不到就直接传**数值**，并在注释里写清含义：
  `t.setJustificationMode(1); // 1 = JUSTIFICATION_MODE_INTER_WORD`
- 新写一个不常用的 framework API 时，先想想它的常量能不能解析；不确定就查数值传字面量
- 这类错误**报在调用方方法名上**（本例报在 `first`），位置会误导，看 `Target exception` 那行更准

❓ 哪些 framework 常量会失败尚未普查；目前确认可用：`Gravity.*`、`View.VISIBLE/GONE`、
`MotionEvent.ACTION_*`、`WindowInsets.Type.*`；确认失败：`TextView.JUSTIFICATION_MODE_*`。

**级别**：✅（2026-10-31，API 34，某书刊阅读 App 详情页两端对齐）

## 45. 要让涟漪/描边画出控件边界，得把一整条容器链的两个裁剪开关都关掉

现象：给列表项/格子加按下的高亮，结果只有**某一侧**能扩出去；换个位置（第 1 列 / 中间 / 最后 1 列）
现象还不一样：首列只往右扩、末列只往左扩、中间列左右都行。

原因：Android 有两道独立的裁剪，默认都开：

| 开关 | 默认 | 裁剪依据 |
|---|---|---|
| `clipChildren` | true | 子控件超出**容器边界** |
| `clipToPadding` | true | 子控件超出**内容区（去掉 padding）** |

只要从控件到屏幕之间**任何一层**还开着，那个方向的溢出就被切掉。首列/末列只扩一边，
正是因为另一边撞上了带 padding 的外层容器；中间列两侧都在内容区里，所以看起来正常。

对策：从控件往上逐层关掉两个开关，**包括看起来无关的那几层**：

```java
grid.setClipChildren(false);   grid.setClipToPadding(false);    // 网格（左右 16dp padding）
row.setClipChildren(false);    row.setClipToPadding(false);     // 行（底部 24dp padding）
hs.setClipChildren(false);     hs.setClipToPadding(false);      // HorizontalScrollView
body.setClipChildren(false);   body.setClipToPadding(false);    // 页内容区（左右 16dp padding）
```

排查口诀：**给容器加过 padding，就一定也要关 `clipToPadding`**；`clipChildren` 只解决越界，
解决不了「被 padding 框住」。

配套坑：负边距外扩的覆盖层若挂在 `wrap_content` 的父容器里，`match_parent` 会按**整屏可用空间**
测量，高亮会糊到上下排去。需要先 `measure()` 拿到真实高度、把父容器高度定死，再挂覆盖层。

**级别**：✅（2026-10-31，API 34，某书刊阅读 App 书架格子）

## 46. `i.us` 加载的图片画在所有普通 View 之上，覆盖层/前景都盖不住它

现象：给书架格子加了一个铺满的透明覆盖层（或多个方案里的 `setForeground`），想让按下高亮盖住封面，
结果**封面区域永远不上色**，高亮只出现在封面之外的空白处——看上去像「只有文字那块亮」。

原因：iApp 图片加载器（`i.us`）把图绘制在普通 View 之上，`background` / `foreground` /
兄弟覆盖层都压不住。定位方法：看高亮的上边缘是不是**正好卡在封面底边**——是，就是被图片盖住了。

对策：

- 按下反馈不要指望覆盖层盖住图片；对 `ImageView` 本身做处理：`setColorFilter(Color.argb(80,0,0,0))`
  压暗、或者 `setAlpha()`（注意 alpha 会透出下层浅色占位，看着**发白**，所以优先用 colorFilter）
- 外围的高亮（扩到格子外的涟漪）仍然可以用覆盖层，两者叠加效果才完整

**级别**：✅（2026-10-31，API 34，某书刊阅读 App 书架格子；❓ 未确认是所有 `i.us`
调用都如此，还是与图片尺寸/加载方式有关）

## 47. 开发态 `getPackageName()` 是宿主 IDE 包，读 `versionName` 拿到的是 IDE 版本

现象：想在页面里运行时显示自己的版本号（免得每次改版本都要回来改文案），
`activity.getPackageManager().getPackageInfo(activity.getPackageName(), 0).versionName`
在开发模式下返回 iApp 自己的版本（如 `5.0.1013`），打包后才返回工程的 `versionName`。

原因：开发模式下工程跑在宿主进程里，`getPackageName()` = `com.iapp.app`。

对策（ui-kit 已封装为 `ui_versionText()`）：

```java
String pkg = activity.getPackageName();
if ("com.iapp.app".equals(pkg)) {
    return "开发版";                  // 开发态：宿主版本会误导，干脆不显示数字
}
PackageInfo pi = activity.getPackageManager().getPackageInfo(pkg, 0);
return pi.versionName;                // 打包态：= AndroidManifest 的 <versionName>
```

验收：开发态显示「开发版」，打包产物显示 `AndroidManifest.xml` 里的 `<versionName>`。
这是「开发态与打包态取到的值来源不同」的又一例，和 #40（窗口边界）同一类问题。

**级别**：✅（2026-10-31，API 34；开发态与打包态各实测一次）

## 48. `window.iapp.fn/fn2` 只认 yul 模块（`.myu`），不能拿来调 mjava

现象：WebView 里用 `hsas` 注入的 `iapp.fn2('call(...)', 'r')`，JS 侧抛
`Error invoking fn2: Java exception was raised during method invocation`，logcat 原文：

```
java.lang.NumberFormatException: For input string: "call(r, "mjava", "app.myu"
    at fj.a ← fj.y ← fj.I ← rm.z2 ← rm.H0 ← com.iapp.app.iapp.fn2
```

原因：`iapp.fn2(code, varName)` 先 `rm.H0(code)` 执行，再按变量名读返回值。`H0` 取第一个
`(` 前的函数名 + 参数个数查内置表，查不到时把代码里**第一个 `.` 之前的前缀拼 `myu`** 去加载
模块文件。`"app.dispatch"` 里的点被当成模块分隔符，于是去找 `app.myu`，再把剩余内容当数字解析。

结论：这个桥是给「JS 调 yul 模块」用的，`iapp.fn('a.b("x")')` 里的 `a` 必须是 `.myu` 模块；
**JS 调 mjava 要走 URL scheme + `shouldoverrideurlloading`**，配方见 `webview-bridge.md` §4。

**级别**：✅（2026-10-31，API 34，开发模式失败签名；打包产物同一 dex，未单独复测）

## 49. `String.valueOf(null)` 在 BeanShell 里命中 `char[]` 重载，抛「length of null array」

现象：两次踩到同一个签名：

```
java.lang.NullPointerException: Attempt to get length of null array
```

- `String.valueOf(i.sss("webfile"))`：这个 key 从没设过，值是 null
- `String.valueOf(c.getHeaderField("Access-Control-Allow-Origin"))`：响应没有这个头

原因：BeanShell 做重载解析时，实参为 null 会选更具体的 `String.valueOf(char[])`，
而不是 `valueOf(Object)`，于是对 null 取 `.length`。静态类型写成 `Object` / `String`
也挡不住。

对策：先判 null，或先接成局部变量再处理：

```java
Object v = i.sss("webfile");
String s = v == null ? "" : String.valueOf(v);
```

字符串拼接 `"" + null` 是安全的（得到 `"null"`），不会抛。进程不崩，只让当前调用返回错误。

**级别**：✅（2026-10-31，API 34，开发模式；两条路径各复现一次）



## 50. 生命周期入口里调用页面构建函数，必须把依赖模块 `i.fn` 齐

现象：给 `again()` 补了一段「重新建壳」，之后从别的页面返回就崩在
`Command not found: th_bg()`（或 `ic_make()` / `wg_ripple()`），页面停在旧内容上。

原因：每个事件回调、每次跨语言调用都是**新解释器**（见 #36），页面模块之外的函数
（theme / icon / widgets / store / net …）必须在本解释器里 `i.fn` 过才有定义。
`again()` 原来只 `i.fn("ui")` 就够用，加上建壳逻辑后这条链就不够了。

对策：生命周期入口（`first` / `again` / 事件回调）里只要会调到别的模块的函数，
就在入口开头把那条链上的模块全 `i.fn` 一遍，不要依赖「上次调用已经装过」——
同一个页面不同入口的解释器是分家的。

```java
public void again() {
    i.fn("ui");
    i.fn("theme");
    i.fn("icon");
    i.fn("widgets");
    ...
}
```

**级别**：✅（2026-10-31，API 34，某书刊阅读 App 首页 resume 重建）
