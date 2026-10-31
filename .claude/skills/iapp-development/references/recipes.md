# 常用配方

## 最小可运行页

```xml
<View id="1" did="0" type="LinearLayout">
<ppt>width=-1
height=-1</ppt>
<event></event>
</View>
<UIEventset><eventItme type="loading">
call(null, "mjava", "app.run")
</eventItme></UIEventset>
```

```java
// app.mjava
public void run() {
    i.syso("ok");
}
```

`.iyu` 里不写 `syso`，日志一律由 mjava 输出。

## 调模块并拿返回值

```java
call(v, "mjava", "mod.method", 1, 2)   // 参数个数要与方法一致
```

## 加载其他 mjava（模块化）

```java
i.fn("b");           // 模块名不带扩展名
b_hello();           // 加载后直接调
int n = b_add(2, 3);
```

- **先 fn，再调用**：未加载调用会 `Command not found`，整个方法中断，`catch` 接不住
- 同名方法后加载覆盖；子模块方法加前缀
- 推荐 facade：入口模块每个 public 方法第一行 `importAll()`，子模块私有
- `i.d.f` 只在开发模式可用；打包交付用 `i.fn`，源码直接打包，不合并
- 完整规范见 `modularization-guide.md`

## 外部库

见 `external-library-guide.md`：JAR→D8→dex，放 `apk/assets/`，开发用工程根加载，打包用 assets→cache 或 `getExternalFilesDir`。

## 新建工程

最小集：`.project` + `AndroidManifest.xml` + `src/mian.iyu` + `icon.png`（`files/`、`res/` 可空）。
`build.xml`、`sdk/iapp.sdk`、`<包名>/` 由 iApp 首次打开时生成。详见 `project-structure.md`。

## 带状态的交互页（计算器模式）

```xml
<UIEventset><eventItme type="loading">
call(null, "mjava", "app.styles")
call(null, "mjava", "app.init")
</eventItme></UIEventset>
```

- 每个按键：控件级 `clicki` → `call(null,"mjava","app.press","7")`
- 状态全部放 `i.sss`（模块变量跨 call 会丢）：`cur/acc/op/fresh`
- 每次按键：读 `i.sss` → 计算 → 写回 → 刷新显示 → `i.syso` 记账
- 按键网格均分：

```xml
<!-- 行：填满剩余高度 -->
<ppt>width=-1
height=0
layout_weight=1
orientation=horizontal</ppt>

<!-- 按钮：等宽等高 -->
<ppt>width=0
height=-1
layout_weight=1
layout_marginleft=4dp
layout_marginright=4dp
layout_margintop=4dp
layout_marginbottom=4dp</ppt>
```

- 边距用四个方向分别写；`layout_margin` 这种合并写法不保证生效

## 持久化（杀进程不丢）

优先用应用私有目录，不需要任何权限：

```java
File f = new File(activity.getFilesDir(), "game2048.save");
FileWriter w = new FileWriter(f, false);
w.write(data);
w.close();
```

- 读：`BufferedReader(new FileReader(f))` 逐行读，文件不存在返回空
- 写时机：**每次状态变化立即写**，不要只依赖 `pause/destroy`（进程可能被直接杀）
- **开发模式**：`getFilesDir()` 是 iApp 宿主 `com.iapp.app` 的私有目录，多个工程共用；文件名前加工程前缀，避免撞车
- **打包模式**：`getFilesDir()` 是打包应用自己的私有目录；开发期写下的存档不会自动带过去，需要迁移就自己导出/导入
- 实测：每次状态变化落盘，杀掉 iApp 再开工程，状态恢复（iApp 5.0.1013 / API 28，2026-10-26）

### `i.sss` 与 `setTag` 能装什么

- `i.sss` 能直接存 `int[]` 与 `ArrayList`，跨 `call` 取回仍是同一类型 ✅（API 28）
- `view.setTag(HashMap)` 跨 `call` 可取回，HashMap 里可以装 `Bitmap` / `Canvas` / `Paint` ✅（API 28）
- `view.setTag(int[])` / `setTag(float[])` 也能跨 `call` 存视图状态，取回时强转 ✅（API 28）
- **存 View 要包一层**：`i.sss` 直接存 View、跨 `call` 取回可能是 null；包成
  `HashMap<String,View>` 后可取回同一实例（⚠ 单次现象，见 `ui-kit.md` §已知限制）。
  只存单个视图时更稳的是 `view.setTag(int, Object)`
- 语义与生命周期见 `iapp-i-reference.md`；这里只记「装得下什么」

### 验证 `i.sss` 是否跨进程（追加式账本）

1. 每次运行向 `getFilesDir()/sss_probe.log` **追加**一行：
   `时间戳 | pid | runId | sss_old | sss_fresh | sss_null | sss_new`。
   启动时先读账本最后一行，再读 `i.sss` 的旧值，最后写本次新值。
2. 每次启动前后确认进程真的死了：
   - `adb shell pidof com.iapp.app` 应为空；
   - `adb shell ps -A | grep com.iapp.app` 无输出；
   - 重开后 `pid` 必须变化；pid 没变 → 只是退到后台，实验无效。
3. 账本是持久化对照：上一行一定在；被测的是 `i.sss` 的 `sss_old`。
4. 锚点：
   - `k_fresh` 从未写过；
   - `k_null` 写过 null；
   - 账本上一行（确定恢复）作正对照。
5. 判读：
   - `sss_old=null`、账本有上一行 → `i.sss` 只在内存，跨进程不保留；
   - `sss_old=上次写入值` → 被恢复，需再用 `kill -9` 或写入后立刻杀，排除保存时机；
   - 账本没有上一行 → 探针没跑到或文件写失败，实验无效。

## 应用内自检

没有单元测试框架时，把纯逻辑用例挂在 `loading`，结果写 logcat：

```java
public void selftest() {
    String[] o = new String[4];
    int[] r = calc(new int[]{2,2,4,4, /*...*/}, 0, o);
    i.syso("G2048 TEST left-merge " + ("4,8,0,0".equals(row(r)) ? "PASS" : "FAIL") + " " + row(r));
}
```

- 用例只碰数组和纯函数，不碰视图，避免被界面问题拖累
- 统一格式 `TAG TEST <name> PASS|FAIL <detail>`，拉一次 logcat 就能判断
- 每次重新运行都会重跑，适合当回归
- 实测 8 项（合并、二次合并、跨零、无效移动、方向、判负、判胜、序列化往返）全 PASS

## 行内水波纹（圆角裁剪）

配方与遮罩原理见 `style-guide.md` §波纹。行内列表只多两个差异：遮罩用不透明圆角矩形；
第二参数（content drawable）可以传 `null`，行底色交给父容器。

## 布局尺寸：约束 > 测量 > 写死

mjava 没有布局预览，写死像素看起来「当场对了」，但字体 metrics、系统字号缩放、
不同 density 一变就会裁字或留空。按这个优先级选：

| 优先级 | 手段 | 适用 |
|---|---|---|
| ① 约束 | `minLines` / `maxLines` / `layout_weight` / `match_parent` / `wrap_content` | 绝大多数情况 |
| ② 测量 | `getLineHeight()` / `getMeasuredHeight()` 等运行时真值 | 需要在代码里算高度时 |
| ③ 写死 | 固定 dp 高度 | ① ② 都表达不了时 |

**需要跨控件对齐时，给它们同一条约束，而不是同一个像素。** 例：三列书架要让作者行对齐，
正确做法是每格都「标题 2 行 + 作者 1 行」，高度自然相等；错误做法是算出像素值写死，
一旦字号档位变化就裁字（实测踩过，见 `pitfalls.md` #39）。

另一条：`ScrollView` / `HorizontalScrollView` 没有自己的 `LayoutParams`，用
`FrameLayout.LayoutParams`（见 `pitfalls.md` #37）。

**级别**：✅（2026-10-31，API 34）

## 纯代码画图标（不用 emoji / 文字符号）

```java
Bitmap bm = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888);
Canvas c = new Canvas(bm);
Paint p = new Paint();
p.setColor(Color.parseColor("#2D7FF9"));
p.setAntiAlias(true);
p.setStyle(Paint.Style.STROKE);     // 线条类图标
p.setStrokeWidth(size * 0.12f);
p.setStrokeCap(Paint.Cap.ROUND);
Path path = new Path();
path.moveTo(size * 0.26f, size * 0.40f);
path.lineTo(size * 0.50f, size * 0.64f);
path.lineTo(size * 0.74f, size * 0.40f);
c.drawPath(path, p);
imageView.setImageBitmap(bm);
```

- 折线类（箭头、对勾）用 `STROKE` + `ROUND` 线帽
- 面状类（定位针、方块）用 `FILL` + `drawCircle` / `drawRoundRect`
- 坐标一律按 `size` 比例写，换尺寸不用改路径
- 图标缓存成字段可避免重复创建

## 工程 res/ 图片：`@名称` 引用与两种形态

工程 `res/` 下的图片用 `@名称.后缀` 引用。**同一条解析链在 mjava 里也能用**：
`i.us(view, "src", "@qj.png")` / `i.us(view, "background", "@qj.png")` 在**开发模式与打包产物里都成立**。

两种形态的图片来源不同，这是关键：

| | 开发模式 | 打包产物 |
|---|---|---|
| `getPackageName()` | `com.iapp.app` | 自己的包名 |
| `res/` 实际位置 | 设备上 `<ProjectApp>/<项目ID>/res/` | APK 内 `assets/res/` |
| `getAssets().list("")` | 宿主自己的条目，**没有 `res`** | 含 **`res`** |

因此原生写法必须分形态：

| 写法 | 开发模式 | 打包产物 |
|---|---|---|
| `i.us(v, "src", "@qj.png")` | ✅ 96x96 | ✅ 96x96 |
| `activity.getAssets().open("res/qj.png")` | ❌ FileNotFound | ✅ 96x96 |
| `BitmapFactory.decodeFile(<ProjectApp>/<id>/res/qj.png)` | ✅ 96x96 | ❌ 文件不存在 |
| `getResources().getIdentifier("qj","drawable",pkg)` | ❌ id=0 | ❌ id=0 |
| `i.us(v, "src", "file:///android_asset/res/qj.png")` | ❌ 1x1 空图 | ❌ drawable 为空 |

结论：**图片一律用 `i.us(v, prop, "@名称.png")`**，一行覆盖两种形态；
不要自己拼 assets 或 sdcard 路径。`res/` 不参与资源编译（`getIdentifier` 恒为 0），
它只是「随包带走的图片目录」，不是 `R.drawable`。

**失败签名**（不抛异常，静默给空图）：`1x1` 或 `-1x-1` 的 `BitmapDrawable`。
判成功要看 `getIntrinsicWidth() > 1`，只看 `getDrawable() != null` 会把失败当成功。

实测依据：2026-10-30 探针（开发模式 + 打包产物各跑一次，结果上屏）。
❓ 未验：`@` 是否支持子目录（`@sub/x.png`）；WebView 里 `file:///android_asset/res/x.png`
（手册提到，本轮只验了 `us` 通道）。怎么验：图片放 `res/sub/`，两种写法各跑两种形态。

## Canvas 卡面：噪声 / 径向渐变 / 圆角裁剪

- 喷砂噪声：160×160 ARGB 位图，`setPixels` 后 `BitmapShader(REPEAT)`；alpha 0~21 已肉眼可见，再大就发灰
- 径向渐变 3 段会有肉眼可见的同心环；9 段 + 256² 再放大才平滑
- 正方形 View 才是正圆；拉伸成矩形就是椭圆
- 圆角裁剪：父容器 `setClipToOutline(true)` + 圆角 `GradientDrawable` 背景，溢出的子 View 自动裁掉
- 已上屏的 Bitmap 改完内容后 `imageView.invalidate()` 即可刷新（`Bitmap + Canvas + ImageView`
  路线成立）✅（API 28）；具体耗时应按设备重测
- **先在 200×250 量级画完，再整体放大**：低分辨率下先把柔和感调对（噪声、渐变段数），
  再用 `Bitmap.createScaledBitmap` 放大到目标尺寸；直接在 120×150 画会糊成一片，一次调不出来
- 整卡绘制耗时随设备和尺寸变化，按目标机实测，不要套用固定毫秒数

## 单弹窗多级选择器（级联 + 返回上一级）

「省 / 市 / 区」这类多级选择，用一个面板 + 一个层级栈，**不要为每一级开新弹窗**：

- 维护 `ArrayList<Level>` 当栈，每级记 `items` 与 `selectedIndex`
- 点非叶子项 → 入栈并重绘列表；点叶子项 → **只回调一次**，把结果交回调用方
- 「返回上一级」= 弹栈重绘；**栈空时才关面板**，不要一按返回就关
- 结果用「父 / 子 / 孙」路径串返回，调用方按分隔符自己拆
- 选中行的水波纹见 `style-guide.md` §波纹（第三参要给与行同形状的遮罩）

✅（API 28 目视验收；对应探针工程已删）

## Dialog 回调里拿不到 final

BeanShell 禁用 `final`。删除确认这类回调，把目标路径先存 `i.sss("del")`，回调里再读；不要试图在匿名类里捕获局部变量。

## 样式分层

见 `style-guide.md`：ppt 管静态，mjava 管计算与全局。

## 动画

见 `animation-guide.md`：`ObjectAnimator` + `postDelayed` 收尾。

## 存储权限（按 API 分）

| 设备 | 广域共享存储的判断 | 申请 |
|---|---|---|
| API ≤ 28（Android 9） | `checkSelfPermission(WRITE_EXTERNAL_STORAGE) == PERMISSION_GRANTED` | `requestPermissions(new String[]{READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE}, code)` |
| API 30+（Android 11+） | `Environment.isExternalStorageManager()` | `Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION` + `package:` URI |
| API 33+（Android 13+） | 同上（广域）；媒体用 `READ_MEDIA_IMAGES/VIDEO/AUDIO` | 同上 / 媒体权限 |

- Android 10（API 29）是过渡期：`requestLegacyExternalStorage` 只对 targetSdk 29 有效，新工程别依赖。
- Android 13+：`READ/WRITE_EXTERNAL_STORAGE` 不再给广域访问，`WRITE` 基本无效；不要拿 `checkSelfPermission(WRITE_EXTERNAL_STORAGE)` 判断 Android 14 的文件权限。
- 只访问 app 私有目录（`getFilesDir()` / `getExternalFilesDir()` / `Android/data/<包名>`）不需要上述权限。
- 只让用户选一个目录：用 SAF（`ACTION_OPEN_DOCUMENT_TREE`），也不需要 `MANAGE_EXTERNAL_STORAGE`。
- **开发模式权限属于 `com.iapp.app` 宿主**：Android 9 上通常已授权，`checkSelfPermission` 恒 true，走不到申请流程；Android 14 上宿主需要 `MANAGE_EXTERNAL_STORAGE` appop，否则共享目录读写被拒。
- 打包版权限属于打包应用；manifest 声明后首次启动申请。

## Android 9（API 28）注意

- 外部存储权限见上一节；API 28 走 `READ/WRITE_EXTERNAL_STORAGE` 运行时权限。
- **开发模式里权限是 iApp 宿主的**：工程跑在 `com.iapp.app` 进程内，`checkSelfPermission` 直接返回宿主的授权结果，开发时常常看不到权限弹窗——这是正常现象，不代表打包版也不需要授权。打包安装后首次启动仍要在系统弹窗里允许
- `listFiles()` 无权限时返回 `null`（或空数组），**不抛异常**；`/data` 这类目录就是 0 项，界面要能处理空列表
- 调试授权：
  ```
  adb shell pm grant <包名> android.permission.WRITE_EXTERNAL_STORAGE
  ```
- WebView 较老：先读 UA / 内核版本再定前端写法
- `targetSdk` 可以高于设备 API，但运行时行为按设备 API 走（该次测量：targetSdk 36 / API 28）
