# 03 mjava 铁律（B2）

日期：2026-10-24　环境：Android 9 (API 28) (API 28)　iApp 5.0.1013

## 方法

11 个独立模块，一个写法一个模块；iyu 侧每项 `syso("R-xx=" + r)`。第一轮跑完发现匿名类会中断事件，第二轮把匿名类挪到最后复跑。

## 读数

| 标记 | 写法 | 读数 |
|---|---|---|
| R-arr | `String[] a = {"x","y"}` | `len=2` ✅ |
| R-fin | `final Object x` | `MJavaErr: Encountered: final` |
| R-cls | 具名 `class Foo` | `can't load this type of class file` |
| R-hex | `0xFF000000` | `Error or number too big for integer type` |
| R-var | `Object... xs` | `Parse error ... Encountered: .` |
| R-bsh | `new bsh.Interpreter()` | `No static field or inner class: Interpreter of class bsh` |
| R-cmp | 匿名 `Comparator` | `cmp=true` ✅ |
| R-oll | 匿名 `View.OnLongClickListener` | `oll=true` ✅ |
| R-shadow | 循环变量 `i` | `s=1 iObj=true`（不闪退）✅ |
| R-anon | 匿名 `new Object(){...}` | `YuErr`，事件中断，后续不执行 |

## 与预期差异

1. **`{...}` 数组合法**，不会让模块失效（预期说会）。
2. **匿名接口实现可用**（API 28）：Comparator 与 OnLongClickListener 都通过。预期中"OnLongClickListener 匿名实现会崩"是 Android 14 的现象，API 28 无该 default 方法。
3. **循环变量 `i` 不遮蔽** `i` 对象，不闪退。
4. 其余 5 条与预期一致：模块失效、全有或全无。
5. 匿名**类**（继承 Object）失败并把整个载入事件打断——比"只废模块"更严重。

## 结论

见 `references/mjava-guide.md` 铁律表；错误前缀语义见 `references/debugging.md`。
