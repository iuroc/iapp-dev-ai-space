# 06 模块装载：call 与 f（B5 第一部分）

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 对比

| 方式 | 写法 | 解释器 | 耗时（本机 50 次均值） |
|---|---|---|---|
| `i.call` | `i.call("mjava","模块.方法")` | 每次新建 | 5.17 ms |
| `i.d.f` | `i.d.f("模块.mjava")` | 导入**当前**解释器 | 0.87 ms（含读文件+eval） |
| 导入后调用 | `i.d.eval("方法()")` | 复用当前解释器 | 0.23 ms |

裕语言侧对应的就是 `call(变量, "mjava", "模块.方法", 参数…)`。

## 语义

- `f(name)` 的参数必须是**带扩展名的文件名**（`b5m.mjava`）。只给 `b5m` 时，iApp 会把名字当整数解析并抛 `NumberFormatException`（字节码里 `fj.a` 在文件不存在时调 `Integer.parseInt`）。
- 导入后 `activity`、`i` 与主流程是同一对象（`eval("activity != null")`=true，`i` 仍是 `Aid_javaCode`）。
- 同名方法：后导入覆盖先导入（`b5m` 后导 `b5m2`，`b5hi()` 返回 `hit2`）。
- 把 `i.d` 存进 `i.sss`，下一次 call 取回的对象类仍是 `j6h`，`eval("b5hi()")` 可正常返回 —— 解释器可跨 call 复用。
- `f` 内部只捕获 `bsh.EvalError`：解析/求值错误打印 `MJavaErr：` 并返回 false；`NumberFormatException` 这类异常会冒泡。

## 与预期差异

| 预期 | 实测 |
|---|---|
| `i.call` 约 11ms/次 | 5.17ms/次（本机） |
| `i.d.f` 约 0.1ms/次 | 0.87ms/次（含读文件与 eval；纯 eval 0.23ms） |
| 异常吞成 JavaErr + null | 解析/求值错误走 `MJavaErr` + 返回 false；其它异常冒泡 —— 需再验 `i.call` 侧 |
| `i.d` 可跨 call 存活 | ✅ 经 `i.sss` 中转成立 |
| 重复 f 重跑模块顶层 | ❓ 未测 |

## 未决

- `i.call` 遇到模块运行时异常是否返回 null（B2 的 `R-xx=null` 是间接证据）
- 重复 `f` 是否重跑模块顶层
- 外部库 JAR / AAR / DEX 三条路

> 2026-10-26 补充：`i.d.f` 仅开发模式可用；交付用 `i.fn("模块名")`，
> 源码直接打包，不合并。见 `cases/15-modularization.md`。
