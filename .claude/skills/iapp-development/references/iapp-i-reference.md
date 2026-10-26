# i 对象参考（Aid_javaCode）

版本前提：iApp 5.0.1013、API 28 实测。

## 身份

- `i` 的真实类：`com.iapp.app.Aid_javaCode`
- 公开方法 390 个，公开字段 12 个：
  `a b c d e f g h i j alertdialog ss_dim`
- 反射筛选 `ss/sss/dim/d` 得到 6 个方法重载（见下）

## 关键成员

| 成员 | 签名 | 行为 | 级别 |
|---|---|---|---|
| `i.d` | 字段，`bsh.Interpreter` 子类 | 当前**这次 call** 的 BeanShell 解释器 | ✅ |
| `i.d.set(k,v)` / `get(k)` | — | 同一次 call 内可读写；`get(未定义)` 返回 null | ✅ |
| `i.d.eval("1+1")` | — | 返回 2 | ✅ |
| `i.d.f(name)` | 方法表中存在 `f` | 仅开发模式按文件名导入；打包后无 `f(String)` | ⚠ |
| `i.fn(name)` | — | 加载模块进当前解释器；交付用 | ✅ |
| `i.call(lang,"mod.method",Object[])` | — | 新建解释器调用；void 方法不要接返回值 | ✅ |
| `i.d(Aid_javaCode,String)` | → int | 同名方法，与字段 `d` 并存 | ✅ |
| `i.ss` | `ss(String)`→Object / `ss(String,Object)`→void | 底层 HashMap 默认 **null**，读写直接 NPE | ✅ |
| `i.sss` | `sss(String)`→Object / `sss(String,Object)`→void | 跨 call 共享；每次**运行**重置 | ✅ |
| `i.dim` | `dim(String,Object)`→void | 按 key 前缀分派 | ✅ |
| `i.a` | 实例字段（Map） | `i.dim` 无前缀时的落点；**每次 call 新实例** | ✅ |

## 生命周期（同一 pid 内实测）

| 对象 | 跨 call | 跨「运行」 | 跨进程 |
|---|---|---|---|
| `i.d` 解释器 | ❌ 每次 call 新建（`dget-cross=null`） | ❌ | ❌ |
| `i.a` 实例 Map | ❌ 每次 call 重置 | ❌ | ❌ |
| `i.sss` | ✅（`sss=1` → `sssRead=1`） | ❌ 同 pid 两次运行都从 null 起算 | ❌ |

读数：

```
B4c-dget0=null
B4c-dget1=v1
B4c-deval=2
B4c-dget-cross=null
B4c-dim-d=null
B4c-dim-a={b4x=v2}
B4c-pre-sss=v3
B4c-pre-ss-err=NullPointerException … HashMap.put … null object reference
B4c-pre-a={a=v5}
```

结论：`i.d` 与 `i.a` 是**每次 call 新建的实例字段**；`i.sss` 是**每次运行重置的类级存储**。

## i.dim 前缀分派（✅）

| 调用 | 落点 | 验证 |
|---|---|---|
| `i.dim("sss.b4y","v3")` | `i.sss("b4y")` = v3 | ✅ |
| `i.dim("ss.b4z","v4")` | `i.ss("b4z")` → NPE（ss_dim 为 null） | ✅ |
| `i.dim("b4x","v2")` | 没有写进 `i.d`（`i.d.get` = null），落在 `i.a` Map | ✅ |
| `i.dim("a","v5")` | 落到 `i.a` Map，`{a=v5}` | ✅ |

注意：`i.a` 每次 call 重置，所以 `dim` 无前缀写入的值**活不过一次 call**。

## 与旧预期的差异

- 旧预期：`i.sss` 是静态 HashMap，同进程跨运行保留。
- 实测：跨 call 保留，但**同 pid 的两次运行不保留**（两次 `B4-sss=1`）。重置点在「每次运行」，疑似每次运行重建类加载器。
