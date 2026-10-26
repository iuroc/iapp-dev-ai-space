# 外部库（JAR / AAR / DEX）

版本前提：iApp 5.0.1013、API 28。结论来自实机探针 + 已确认的基础结论。

## 基础结论

iApp **没有 Gradle、也没有内置 D8**，外部库必须在打包前自己转格式：

| 输入 | 处理 | 产物 |
|---|---|---|
| JAR | D8 转 dex | `xxx.dex` |
| AAR | 拆出 `classes.jar` 走 D8；`res/` 走 aapt2 | dex + resource apk |
| DEX | 直接用 | `xxx.dex` |

产物放 **`apk/assets/`**（`apk/lib/` 属 VIP/付费打包入口，不要用）。
运行时：`DexClassLoader` 加载代码，`AssetManager.addAssetPath` 挂资源，然后 import / 实例化。

## 目录

```
工程根/
└── apk/
    └── assets/
        ├── lib.dex          # D8 产物，直接放
        └── libres.apk       # aapt2 产物（可选，带资源时）
```

## 运行时加载

开发环境（工程在外部目录）可以直接按路径加载；打包后 assets 在 APK 内，需先释放到 `cacheDir`。两条路都写在下面。

```java
// 1) 开发环境：工程根 + apk/assets/lib.dex
java.lang.Class vd = activity.getClassLoader().loadClass("com.iapp.app.VisualDesigner");
String root = (String) vd.getField("a9").get(null);
String dex = root + "/apk/assets/lib.dex";

// 2) 打包环境：从 APK assets 释放到 cache
java.io.InputStream is = activity.getAssets().open("lib.dex");
java.io.File out = new java.io.File(activity.getCacheDir(), "lib.dex");
// 复制流到 out ...

dalvik.system.DexClassLoader dcl = new dalvik.system.DexClassLoader(
        dexOrOut, activity.getCacheDir().getAbsolutePath(), null, activity.getClassLoader());
java.lang.Class c = dcl.loadClass("com.example.Hello");
Object o = c.newInstance();
c.getMethod("inst", new java.lang.Class[]{}).invoke(o, new Object[]{});
c.getMethod("hi", new java.lang.Class[]{}).invoke(null, new Object[]{});
```

带资源时（✅ 实测，API 28）：

```java
// addAssetPath 是 hidden API，用反射；直接挂在宿主的 AssetManager 上即可，
// 不需要另建 Resources（资源包用独立包 ID，见下文「带资源的 AAR」）
Method add = android.content.res.AssetManager.class
        .getDeclaredMethod("addAssetPath", new Class[]{String.class});
add.setAccessible(true);
add.invoke(activity.getAssets(), new Object[]{resApkPath});
```

## 两条路径均已实测（✅）

| 环境 | dex 来源 | 结果 |
|---|---|---|
| 开发 | `<工程根>/apk/assets/b5lib.dex` | `cls=b5lib.Hello` / `jar-inst` / `jar-hit` |
| 打包 | `assets/b5lib.dex` → 释放到 cache → 加载 | 同上 |
| 打包（备选） | `getExternalFilesDir(null)/b5lib.jar` | 同上 |

打包产物里可见：

```
assets/lib.so
assets/b5lib.dex            (772 B)
assets/b5lib.dex.x86_64.flock
assets/oat/x86_64/b5lib.odex
assets/oat/x86_64/b5lib.vdex
assets/extra_conf1g.xml
```

说明 `apk/assets/` 下的文件会原样进入 APK 的 `assets/`，且 iApp 会顺带生成 odex/vdex。

## 打包环境（✅ 实测）

打包包会裁掉 `VisualDesigner`、也不包含工程 `files/`，所以打包后不能用工程根。已验证可用：

```java
java.io.File dir = activity.getExternalFilesDir(null);      // /sdcard/Android/data/<包名>/files
String dex = dir.getAbsolutePath() + "/b5lib.jar";         // dex 化后的 jar 或 dex 均可
dalvik.system.DexClassLoader dcl = new dalvik.system.DexClassLoader(
        dex, activity.getCacheDir().getAbsolutePath(), null, activity.getClassLoader());
```

屏幕读数：`exists=true`、`cls=b5lib.Hello`、`inst=jar-inst`、`hi=jar-hit`。

首发时把库释放到该目录（assets 复制或下载），再加载。

## 实测记录

- `i.loadjar` 只会去 `<工程根>/apk/lib/` 找，且要求 dex；该目录触发付费，弃用
- 纯 `.class` 的 jar 在 Android 上无法加载（DexPathList 为空）
- `Class.forName("com.iapp.app.VisualDesigner")` 在模块里不可用；要用 `activity.getClassLoader().loadClass(...)`
- 打包后 `VisualDesigner` 被裁掉、`files/` 不进 APK —— 打包环境必须走 assets 释放路径

## 带资源的 AAR（✅ 已实测：sora-editor 0.21.1）

AAR 比 JAR 多两件事：`res/` 和「R 是 0」。两个都得处理，否则库在构造期就会崩。

### 为什么 R 是 0 会崩

AAR 的 `R.txt` 全是 `0x0`，真实 ID 由宿主 App 链接时才分配。库如果在**构造期**就用
`R.layout.*`，直接 `new` 会 `Resources$NotFoundException: Resource ID #0x0`。
sora-editor 就是这种：`new CodeEditor(ctx)` → `EditorTextActionPanel` → `inflate(layout)`。

### 处理链路

```
AAR ──classes.jar（剥掉自带 R*.class）──► d8 ──┐
    └─ res/ ──aapt2 compile──► compiled.zip     │
              ──aapt2 link -I <framework> ──► 资源apk + gen/R.java
                                              └─ javac R.java ──► r.jar ──► d8（同一个 dex）
```

| 步骤 | 坑 |
|---|---|
| `aapt2 link` | 需要 `-I` 框架资源。没有 android.jar 时可用设备上的 `/system/framework/framework-res.apk` |
| `--package-id` | **必须 ≥ 0x7f**；宿主占 0x7f，所以用 `0x80`，避免 ID 冲突 |
| `javac R.java` | JDK 25 默认产 class 69，d8 不认 → `--release 11` |
| `d8` | 不接受目录输入，`rclasses/` 先打成 jar；多输入文件可一次进同一个 dex |

产物两份，都放 `apk/assets/`：`xxx.dex`（代码）+ `xxx-res.apk`（资源）。

### 运行时

```java
// 1) 挂资源（hidden API，反射可用）
AssetManager am = activity.getAssets();
Method add = AssetManager.class.getDeclaredMethod("addAssetPath", new Class[]{String.class});
add.setAccessible(true);
add.invoke(am, new Object[]{resApkPath});

// 2) 加载代码：父加载器必须给 null（见 pitfalls #23）
DexClassLoader dcl = new DexClassLoader(dexPath, cacheDir, null, null);
```

- 资源 ID 在 `0x80xxxxxx`，与宿主 `0x7fxxxxxx` 不冲突；`addAssetPath` 之后宿主
  `Resources` 就能解析这些 ID（不需要另建 `Resources` 对象）
- 库若强转 `ContextThemeWrapper`（sora 的 `CodeEditor` 会），要把
  `new ContextThemeWrapper(activity, android.R.style.Theme_DeviceDefault_Light)` 传给它
- 开发模式路径：`VisualDesigner` 字段 `a9` + `/apk/assets/`；打包后从 assets 复制到
  `cacheDir` 再加载（两条路都要，靠 try 兜底）

### 桥接类：库 API 多时不要从 mjava 反射调

mjava 是 BeanShell，按名字调库方法在「名字可信」时才成立；遇到重载族（`(float)->void`
有十来个）连按签名都不保险。做法是把 glue **编译进 dex**：

```java
// iappbridge.SoraHost（javac 编译，和库一起 d8）
public SoraHost(Context ctx, ViewGroup parent, String text) { … }  // 建 + 挂 + 设文本
public SoraHost(String text) { … }                                  // 换文本
public SoraHost(View sink, String op) { sink.setTag(compute(op)); } // 读数据走 tag
```

mjava 只用两种入口，都不受改名影响：

- **构造函数**：`cls.getConstructor(new Class[]{Context.class, ViewGroup.class, String.class})`
- **框架方法**：`sink.getTag()` / `sink.setTag(...)`（`View` 是框架类）

### 实例

`sora-editor 0.21.1` + `language-java` + `kotlin-stdlib 1.8.10` →
`sora.dex` 约 2.8 MB（1383 个类）+ `sora-res.apk` 约 18 KB。完整脚本见工作区
`docs/scripts/build_sora_dex.py`，案例见 `cases/19-code-editor.md`。

## 编译类进 dex（BeanShell 写不了「继承类」时的通用解）

BeanShell 只能实现接口，**不能继承类**（匿名类会中断事件）。遇到必须继承抽象类的场景
——`PagerAdapter`、`BaseAdapter`、`ItemDecoration` 之类——就自己写 Java 编成 dex：

```
Xxx.java ──javac（-classpath android.jar;依赖.jar）──► classes ──jar──► d8 --lib … ──► xxx.dex
```

```java
// iappbridge/VpAdapter.java
public class VpAdapter extends PagerAdapter {
    public VpAdapter(Context c) { … }          // 只要构造函数能被取到
    @Override public int getCount() { … }
}
```

```java
// mjava：用构造函数 + 反射拿实例（构造函数按参数类型匹配，不受改名影响）
DexClassLoader dcl = new DexClassLoader(dex, cacheDir, null, activity.getClassLoader());
Class a = dcl.loadClass("iappbridge.VpAdapter");
Object ad = a.getConstructor(new Class[]{Context.class}).newInstance(new Object[]{activity});
vp.setAdapter((PagerAdapter) ad);
```

要点：

- **父加载器给宿主**：这类子类依赖的 `androidx.*` 在宿主里，不能像 sora 那样给 `null`
- 自己的包名要有前缀（如 `iappbridge.`），避免和宿主同名类相撞（见 pitfalls #23）
- 方法名不会被混淆——混淆只发生在「拿到宿主自带类」的情况下
- 编译用 `--release 11`，d8 不接受目录输入；脚本见工作区 `docs/scripts/build_class_dex.py`
- 实测：ViewPager 探针用它跑通了三个翻页事件（见 `events-guide.md`）

## Android 14+ 的 DCL 只读要求（targetSdk ≥ 34）

官方行为变更原文（developer.android.com/about/versions/14/behavior-changes-14
「Safer dynamic code loading」）：

> If your app targets Android 14 (API level 34) or higher and uses Dynamic Code Loading
> (DCL), **all dynamically-loaded files must be marked as read-only**. Otherwise, the
> system throws an exception.

- 适用范围看 **targetSdk**：iApp 打包出来的 targetSdk 是 36，所以在 Android 14/15 设备上
  必然命中；Android 9 及更低没有这条限制
- 用户实测：Android 15 实机上 `sora.dex` 放在 `getCacheDir()`（默认可写）→ 加载被系统拒绝
- 注意限制的是**文件可写**，不是目录。换 `getCodeCacheDir()` 不一定能绕过

### 正确写法（官方推荐顺序）

**先 `setReadOnly()`，再写内容** —— 目的是消除「写完到设只读之间」的竞态窗口：

```java
File d = new File(activity.getCacheDir(), "lib.dex");
if (d.exists()) {          // 已存在的文件官方建议删除重建
    d.setWritable(true);
    d.delete();
}
FileOutputStream fo = new FileOutputStream(d);
d.setReadOnly();           // 打开输出流之后、写入之前（fd 已打开，写入仍可继续）
byte[] buf = new byte[8192];
… fo.write(…) …
fo.close();
d.setReadOnly();           // 收尾再设一次，确保最终权限
```

- 反过来做（写完再 `setReadOnly`）不满足官方建议的顺序
- 已有只读文件时要先 `setWritable(true)` + `delete()`，否则 `FileOutputStream` 打不开
- 每次覆盖都要经过这套流程；**不要把只读文件直接复写成可写的**

### 和本工作区实现的关系

`com.demo.editor` 的 `ed_sora.sora_write()` 就是上面这套；`sora_copy()`（打包模式
assets → cache）和 `sora_local()`（开发模式工程目录 → cache）都走它。
Android 14 以下同样适用，没有副作用。

## 未决

- `addAssetPath` 在 **API 28 以下 / 高版本**（灰名单收紧后）的行为未测 ❓
- 资源包与宿主资源**同名资源**的覆盖优先级未测 ❓
