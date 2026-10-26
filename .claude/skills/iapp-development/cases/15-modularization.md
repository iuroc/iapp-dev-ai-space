# 15 模块化（i.fn 实测 + 2048 七模块拆分）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 目标

1. 验三种加载方式：`i.fn`、`i.d.f`、`i.call`，确定交付用哪条。
2. 把单文件 ~700 行的 2048 拆成 facade + 6 个子模块（共 7 个）。
3. 把“怎么加载、按什么顺序、失败长什么样”写进规范。

## 第一轮：`i.d.f`（只在开发模式）

```
MP import-ret=true
MP b-hello
MP direct-after-import=ok
MP eval-add=5
MP util-dp8=24 tag=UTIL
MP collision-same=3
MP missing-err=NumberFormatException: For input string: "nope.mjava"
MP state-after-inc=2
MP state-fresh-call=0
MP path-src-err=NumberFormatException: For input string: "src/putil.mjava"
MP b-hello                         ← iyu 直接 call pb.b_hello

Command not found: b_hello() ...
   ← 导入前调用：方法直接中断，没有进 catch
```

| 结论 | 级别 |
|---|---|
| `i.d.f("b.mjava")` 返回 true，导入当前解释器 | ✅ |
| 导入后可直接调 `b_hello()` / `b_add(2,3)` | ✅ |
| 同名方法后导入覆盖（2 → 3） | ✅ |
| 模块级变量同 call 保留（2），下一次 call 归 0 | ✅ |
| 未导入先调用 → `Command not found`，方法中断且 catch 不住 | ✅ |
| 缺文件 → `NumberFormatException` | ✅ |
| 路径必须裸文件名（cwd = `src/`） | ✅ |

打包 APK 后 `i.d.f` 直接失败：

```
Method f( java.lang.String ) not found in class'xn0'
```

- 打包版 `i.d` 是 `xn0`（继承 `bsh.Interpreter`），`f` 是 Context 字段
- 只剩 `a/b/c/d/e`；没有按文件名导入的方法

## 第二轮：`i.fn`（正确加载，✅）

```java
i.fn("pb");          // 模块名不带扩展名
b_hello();           // 加载后直接调
b_add(2, 3);         // 5
```

```
FN loaded
CALL b-hello
FN hello-ok
FN add=5
```

- `i.fn` 把模块加载进**当前**解释器，方法直接可用
- 一次 call 内加载一次即可；facade 用 `G_IMPORTED` 标记
- 交付用这条；源码直接打包，不合并

## `i.call` 的正确语义

```java
Object r = i.call("mjava", "pb.b_add", new Object[]{2, 3});  // 5
i.call("mjava", "pb.b_hello");                                // void：当语句调
```

- 参数顺序：**语言 → "模块.方法" → Object[]**
- 写成 `i.call("pb.b_hello","mjava")` 返回 null，方法不执行（顺序错）
- 每次新建解释器，约 5–11ms；模块级变量不共享
- void 方法不要接返回值：`Object r = i.call(...)` 报 `Void initializer` 并中断
- 适合偶尔的隔离调用；跨模块加载优先 `i.fn`

## 七模块拆分

```
src/
├── mian.iyu              # 只 call facade
├── game.mjava            # facade：init/layout/newGame/keepPlaying/keyCode + importAll(i.fn)
├── g2048_util.mjava      # u_*     dp / i.sss / 日志
├── g2048_core.mjava      # core_*  规则 + 自检
├── g2048_store.mjava     # store_* 存档
├── g2048_ui.mjava        # ui_*    样式 / 卡片 / 弹层
├── g2048_anim.mjava      # anim_*  平移 / 缩放
└── g2048_input.mjava     # input_* 滑动 / 方向键
```

| 文件 | 行数 |
|---|---|
| game.mjava | ~333 |
| g2048_core.mjava | ~199 |
| g2048_ui.mjava | ~233 |
| g2048_input.mjava | ~114 |
| g2048_store.mjava | ~90 |
| g2048_anim.mjava | ~50 |
| g2048_util.mjava | ~35 |

## 拆分时踩的坑

```
Command not found: u_st( java.lang.String ) : at Line: 60
Called from method: layout
```

`layout()` 在 `importAll()` **之前**做了 `if (u_st("built").equals("1"))`。
新 call 的解释器里还没有 `u_st` → 整个 `layout` 中断，棋盘不渲染。

修复：把 `importAll()` 提到 `layout()` 第一行，`built` 检查放到它后面。

这条坑进了 `pitfalls.md` 第 20 条和 `modularization-guide.md` 的“铁律：先加载，再调用”。

## 复用的 KB 结论

- 交付加载用 `i.fn("模块名")`
- `i.d.f` 仅开发模式；打包版 `i.d` 是 `xn0`，没有 `f(String)`
- `i.call("mjava","模块.方法",Object[])` 可用，但每次新建解释器
- 加载后直接调；加载前调用不可 catch
- 子模块方法加前缀，避免同名覆盖
- 模块级变量只活一次 call，状态放 i.sss
- facade + 私有子模块的分层
- 动画只放原语，流程回调留 facade

## 验收

- 7 模块 + `i.d.f` 在开发模式已跑通（`layout side=984 cell=208`，滑动/动画/存档正常）
- 15:10 `i.fn` 探针：`FN loaded` / `FN hello-ok` / `FN add=5`
- facade 已改用 `i.fn`；开发 + 打包均已运行正常（用户确认）
