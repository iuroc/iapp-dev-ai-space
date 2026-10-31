# iyu 内联 Java 块（`java { }`）— ⚠ 实验性存档

> **⚠ 当前不要用。** 本文件只是把 2026-10-30 的探明结果存档，供将来需要时参考。
> `java { }` 块**打包属于 VIP 功能**，非 VIP 的「强制打包」会删掉该功能、可能导致应用不可用；
> 其余用法也尚未验证。**现有工程一律走 `call` → `.mjava`，不要在任何交付工程里写 `java { }`。**
> 这套方案后续可能补全，但**大概率会被废弃**（不接受 VIP 依赖）。
>
> 一句话：`.iyu` 事件里可以写 `java { … }`，它**不是解释执行**，而是被抽成
> `androidx.Yu3Java` 类的静态方法，用 App **内嵌的 javac + R8** 现场编译成 dex 再加载。
> 语言层是真 Java；但按块调用、无类体、编译单元全工程共享，且**打包要 VIP**。
>
> 版本前提：iApp V5.0.1013 / 裕 V3（`<yuv>3</yuv>`）/ Android 14（API 34）。
> 更早或更晚的版本按 ❓ 处理，先复跑 §8 的探针。

## §0 判断：技术上可行，但**当前不采用**

| 维度 | `java { }` 块 | `call` → `.mjava` |
|---|---|---|
| 执行方式 | **javac 编译** → dex → 反射调用 | BeanShell 解释 |
| Java 语言面 | 完整现代 Java（lambda / var / try-with-resources 实测可用） | BeanShell 子集（`final`、具名类、可变参数等都不行） |
| 继承 / 匿名类 / 适配器 | ✅ 可写 | ❌ 必须编译进 dex |
| iApp API（`i` 对象 390 个方法） | ❌ 拿不到（`yuc` 不是 `i`） | ✅ 直接可用 |
| 跨事件状态 | 只能走 `sss`（块内没有类体，写不了字段） | 同上，走 `i.sss` |
| 复用 / 模块化 | 块是匿名的，名字是 `ff<hash>`，**不能按名复用** | 模块 + 方法，可复用 |
| 编译失败影响面 | **全工程的块一起失效** | 只坏那一个模块的方法体 |
| 性能（1M 次 `acc += k % 7`） | 3004 µs | 2 144 230 µs（约 **714 倍**） |
| 打包交付 | **VIP 功能**；非 VIP「强制打包」会删掉该功能 | 免费 |

**否决理由**（按权重）：

1. **交付被 VIP 卡死**：非 VIP 不能正常打包，这不是技术能绕的。
2. **连坐**：一个块编译失败，全工程的块一起失效，且失败静默。
3. **不可复用**：块没有稳定名字、没有类体，做不了模块化。
4. 其余细节都没验（打包后行为、`.java` 互操作、编译耗时随规模变化）。

**结论**：不进现有开发流程，不做迁移。本文件的价值只剩"将来若解禁 VIP，能少走弯路"。

## §1 它到底怎么跑（机制，静态 + 运行时双证据）

1. 预编译时扫描工程 `src/` 下的 `.iyu` 文件（`.myu` 不在其列，见 §4），
   把每个 `java { … }` 抽出来，替换成裕语言调用 `java("ff<hash>")`。
2. 所有块拼进同一个类 `androidx.Yu3Java`，每个块一个静态方法：

   ```java
   public static void ff783611576(final Activity activity, final Context context,
       final Object yuc, final HashMap<String,Object> sss,
       final HashMap<String,Object> ss, final HashMap<String,Object> s){
       // 块里的代码原样放这里
   }
   ```

3. 类里另有两个桥方法，都用反射进 `com.iapp.app.iapp`：
   - `yu(Object yuc, String code)` → `callYu`，回执行裕语言
   - `syso(Object yuc, Object log)` → `callYu_syso`，进 `ygs`
4. App 里内嵌 javac（`com.sun.tools.javac.*`）+ R8 + smali，编译成 dex 后用
   `DexClassLoader` 加载。**不是** BeanShell，也不是远程编译。

生成源码可以现场读（路径里的 `app__<id>` 随安装变）：

```
/data/data/com.iapp.app/app_<id>/iapp_yuv3_run/android/src/androidx/Yu3Java.java
```

排查编译问题直接 `su -c 'cat'` 这个文件 —— 它就是你写的块拼出来的完整类。

## §2 怎么写

### 预置变量（签名固定，名字别改）

| 名字 | 类型 | 说明 |
|---|---|---|
| `activity` | `Activity` | 真实 Activity 实例（实测 `com.iapp.app.run.mian`） |
| `context` | `Context` | 同上 |
| `yuc` | `Object` | 裕语言运行时句柄（实测类名 `rm`），只用来传给 `yu` / `syso` |
| `sss` / `ss` / `s` | `HashMap<String,Object>` | 全局 / 界面 / 局部变量，**和裕语言是同一张表** |

`s.put("x", …)` 之后，事件里直接 `x` 就能读到；反向同理。

### 预置 import

只有这四个：

```java
import android.app.Activity;
import android.content.Context;
import java.lang.*;
import java.util.*;
```

其余类**写全名**，或在工程 `build.xml` 里加：

```xml
<importClass><itme name="/src/mian.iyu">android.widget.TextView
android.os.Handler</itme></importClass>
```

- 一行一个类，**行首不能有空格**（会原样变成 `import  android.widget…;`）
- 实测生效 ✅：加完后块里可直接 `new TextView(activity)`
- 只对 `name="/src/mian.iyu"` 这一个 itme 生效（其他文件名未验 ❓；验证方法：换 `.iyu` 文件名再跑）

### 转义

`.iyu` 按类 XML 读，`<` 要写成 `&lt;`（运行时会把 `&lt;`/`&gt;` 还原）：

```java
for (int k = 0; k &lt; 1000000; k++) { … }
java.util.List&lt;String&gt; xs = new java.util.ArrayList&lt;String&gt;();
```

`>` 直接写没问题（lambda `() -> "x"` 实测可用）。`&`（`&&`）未单测 ❓。

### 事件里的位置

实测可用的位置：`loading`、`clicki`、`f(){}` 内、`w(){}` 内、同一事件多个块。
块按书写顺序执行，和裕语言**同线程、同步**。

## §3 已实测能力（API 34 / 5.0.1013 / 2026-10-30）

| 能力 | 级别 |
|---|---|
| `s`/`ss`/`sss` 双向读写，java 写回后裕语言立即可读 | ✅ |
| 块跑在调用它的线程上（loading/click 都是 `main`） | ✅ |
| `activity.findViewById(id)` + `setText` 直接改界面 | ✅ |
| `new Thread(…).start()` + `activity.runOnUiThread(…)` | ✅ |
| 子线程 / UI 回调里再调 `yu(yuc, …)` | ✅ |
| 匿名类实现接口（`OnClickListener`） | ✅ |
| 局部类（方法内 `class Local {}`） | ✅ |
| `new android.widget.TextView(activity)` 动态建控件 | ✅ |
| **匿名 `BaseAdapter` 子类**（mjava 必须走 dex 的那种） | ✅ |
| 泛型、增强 for、`Collections.sort` + 匿名 `Comparator` | ✅ |
| 现代 Java：菱形 `<>`、方法引用 `String::toUpperCase`、lambda、`var`、try-with-resources | ✅ |
| `try/catch` 捕获运行时异常（`ArithmeticException`） | ✅ |
| 未捕获异常 | ✅ 不崩、不中断事件；栈进 `System.err`，帧名是 `androidx.Yu3Java.ff<hash>(Yu3Java.java:N)` |
| `importClass` | ✅ |
| 100 万次循环：块 3.0 ms / mjava 2 144 ms | ✅（同机同轮） |

## §4 边界与坑

1. **一个坏块，全工程连坐** ✅
   全部块在同一个 `Yu3Java` 类里；任何一块编译不过，整个类编译失败 →
   该工程**所有** `java{}` 块一起失效（探针 J3：好块 + 坏块同工程，好块也没输出）。
   推论：块要么一次写对，要么整个工程停摆；不要在生产工程的同一个工程里"试着写"。

2. **编译失败是静默的** ✅
   只通过 `msgService` 写进 iApp「数据调试工具」控制台（`Java代码预编译失败：…`），
   **不进 logcat**。裕语言代码照常执行，块被直接跳过。
   排查手段：读 §1 那个生成源码 + 在块里先放一行 `syso(yuc, "R-x")` 当哨兵。

3. **`.myu` 模块里的块不生效** ✅
   在 `.myu` 的 `fn` 里写 `java { … }`，调用时报
   `YuErr … >错误: java`，块源码原样出现在错误里（说明没被替换成 `java("ffN")`）。
   报错后**事件不中断**，后面的语句照常跑。机制原因 ⚠ 推测是块替换只走 `.iyu` 路径。

4. **`yuc` 不是 `i`** ✅
   `yuc.getClass().getMethods()` 284 个方法，没有 `uigo/syso/sss/call/gvs`
   这些名字 → 拿不到 iApp 封装 API。要 iApp 能力就回裕语言 / mjava。
   需要原生能力时才用块。

5. **块没有名字、不能复用** ✅
   方法名是 `ff<hash>`，随工程内容变；跨块 / 跨页按名调用不可靠，不要依赖。

6. **块内写不了字段 / 静态方法** ✅
   块只是一段方法体。要共享状态走 `sss`；要共享代码只能复制，或改用 mjava/dex。

7. **打包是 VIP 功能** ⚠（弹窗实测，未真正打包）
   点打包会弹：「当前项目使用了会员VIP功能 [原生Java代码编译] 和 [裕V3与Java代码交叉编译]」，
   非 VIP 只有「强制打包」，而强制打包**会删掉该功能，可能导致项目无法正常运行**。
   待验 ❓：VIP 打包后的 APK 里块是否照常编译加载。验证方法：有 VIP 的账号打包 →
   安装 → 跑块 → 看屏幕是否有块的输出（打包后 `ygs` 静默，只能看屏幕 / `System.err`）。

8. **性能读数随设备变** ⚠
   714 倍是同机同轮对照，换设备两边都会变；比值比绝对值稳。

## §5 如果将来解禁 VIP，可能的用法（**现在不要照做**）

> 下面只是把"真要用起来该怎么摆"记下来，前提是 **VIP 打包问题已解决**。
> 当前没有这个前提，所以本节不构成建议。

**分层不变**：`.iyu` 只做 `call` 编排，业务在 `.mjava`。

**若采用，优先这四类**：

1. **mjava 写不了的**：继承、匿名/局部类、`BaseAdapter`、自定义 `View`、需要接口回调的库。
2. **性能热点**：循环、字符串/图像处理、每帧都要跑的逻辑（先量再换）。
3. **需要真 Java 语义的**：泛型擦除之外的类型安全、try-with-resources、lambda 回调。
4. **一次性原生调用**：直接 `activity.xxx()`，不值得为它开一个 mjava 方法。

**边界**：

- 块与 mjava 的桥是裕语言：块内 `yu(yuc, "call(null,\"mjava\",\"mod.m\")")` 回到 mjava；
  反向没有可靠通道（不要尝试从 mjava 调块）。
- 状态统一放 `sss`，两边都能读写。
- 写块前先确认工程能打包（VIP），否则开发期能跑、交付期废掉 ——
  这一条目前**无法满足**，所以实际结论仍是"不要用"。

**若采用，工程组织建议**：

- 块只放在**已经稳定的工程**里；试验期单独建探针工程，避免连坐。
- 一个工程里块越少越好；同类逻辑集中到一个块，而不是散在很多事件里。
- 块内第一行放哨兵 `syso(yuc, "R-<名字>")`，编译失败时能一眼看出是块没跑而不是逻辑错。

## §6 与其他"Java 通道"的区别

iApp 里有四条能碰 Java 的路，别混：

| 通道 | 形态 | 典型用途 |
|---|---|---|
| `call` → `.mjava` | BeanShell 解释的方法体 | iApp 业务默认写法，能用 `i` |
| `java { }` | 编译进 `androidx.Yu3Java` 的方法体 | 原生能力、性能热点、mjava 写不了的 |
| `java(...)` / `javax` / `javanew` 等裕语言函数 | 反射调用单个方法/构造器 | 临时调一个 API，不值得开块 |
| `.java` → `d8` → `apk/assets/*.dex` | 真正的外部类/库 | 继承/库封装/可复用组件 |

`java { }` 与 `java(...)` 是**两回事**，只是同名前缀：前者是源码块，后者是反射调用。
（手册里"java 调用java代码方法"一节讲的是后者。）

## §7 未决

| 问题 | 级别 | 怎么验 |
|---|---|---|
| VIP 打包后块是否照常工作 | ❓ | §4-7 |
| 裸 `<` 不写 `&lt;` 是否也能过 | ❓ | 在探针块里写 `1 < 2` 看编译是否失败 |
| `&&` 是否要转义 | ❓ | 在探针块里写 `if (1>0 && 2>1)` |
| `importClass` 是否只认 `mian.iyu` | ❓ | 把 itme 的 name 改成别的 `.iyu` 再跑 |
| 块能否引用工程内的 `.java` / 外部 dex 类 | ❓ | 按手册 `/. ./.` 的例子建一个外部类，看编译期能否解析 |
| 编译耗时随块数/代码量怎么变 | ❓ | 放 50 个块 + 2000 行，量首次运行延迟 |

## §8 复现（探针工程）

三个工程，源码在 `project/` 下，都是可推的设备工程：

| 探针 | 覆盖 |
|---|---|
| 探针 1 | 作用域 / yu 互调 / UI 线程 / 嵌套位置 / 跨事件状态 / 性能 / 异常 / 能力（P2–P7） |
| 探针 2 | 现代语法 + `importClass` |
| 探针 3 | 好块 + 坏块同工程，验证连坐与静默 |

判读只要看 `ygs` 里的 `R-*` 行；屏幕同时会给一份（`app.show` 走 mjava）。
