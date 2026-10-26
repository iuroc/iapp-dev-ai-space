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
- `getFilesDir()` 是 iApp 宿主 `com.iapp.app` 的私有目录，**多个工程共用**；文件名前加工程前缀，避免撞车
- 实测：`com.demo.game2048` 每次移动落盘，杀掉 iApp 再开工程，棋盘/分数/最高分恢复（证据见 `docs/evidence.md` 2026-10-26）

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

```java
GradientDrawable mask = new GradientDrawable();
mask.setShape(GradientDrawable.RECTANGLE);
mask.setColor(Color.WHITE);
mask.setCornerRadius(dp(10));

row.setBackground(new RippleDrawable(
        ColorStateList.valueOf(Color.parseColor("#1A2D7FF9")), null, mask));
```

- 第三个参数是**遮罩**。不给遮罩（传 null）时涟漪会按无边界圆扩散，看起来是一个整圆
- 遮罩用不透明圆角矩形即可，涟漪自动被裁到形状内
- 第二参数（内容 drawable）可以为 null，行本身的底色由父容器决定

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

## 样式分层

见 `style-guide.md`：ppt 管静态，mjava 管计算与全局。

## 动画

见 `animation-guide.md`：`ObjectAnimator` + `postDelayed` 收尾。

## Android 9（API 28）注意

- 外部存储用 `WRITE_EXTERNAL_STORAGE` 运行时权限 + `checkSelfPermission`；**不要**用 `MANAGE_EXTERNAL_STORAGE` / `Environment.isExternalStorageManager()`（API 30+）
- **开发模式里权限是 iApp 宿主的**：工程跑在 `com.iapp.app` 进程内，`checkSelfPermission` 直接返回宿主的授权结果，开发时常常看不到权限弹窗——这是正常现象，不代表打包版也不需要授权。打包安装后首次启动仍要在系统弹窗里允许
- `listFiles()` 无权限时返回 `null`（或空数组），**不抛异常**；`/data` 这类目录就是 0 项，界面要能处理空列表
- 调试授权：
  ```
  adb shell pm grant <包名> android.permission.WRITE_EXTERNAL_STORAGE
  ```
- WebView 较老：先读 UA / 内核版本再定前端写法
- `targetSdk` 可以高于设备 API，但运行时行为按设备 API 走（本机实测 targetSdk 36 / API 28）
