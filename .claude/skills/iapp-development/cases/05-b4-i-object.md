# 05 i 对象与状态（B4）

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 方法

1. 反射 `i` 的类、方法、字段（`b4.api` / `b4b.api2`）
2. 5 轮账本（实际拿到 2 轮同 pid + 1 轮重启后）
3. `i.d` / `i.dim` 行为（`b4c`）

## 读数

见 `docs/evidence.md` 同名章节。要点：

```
B4-iclass=com.iapp.app.Aid_javaCode
B4-api-count=6 total=390
B4-fields=12
B4-field a … j, alertdialog, ss_dim
B4-ssread-err=NullPointerException … HashMap.get … null object reference
B4b-dclass=j6h super=bsh.Interpreter
B4b-dgetmiss=null
B4c-dget-cross=null
B4c-dim-a={b4x=v2}
B4c-pre-sss=v3
```

## 结论

- `i` = `Aid_javaCode`；`i.d` = `bsh.Interpreter` 子类
- 每次 call 新建解释器与实例字段；`i.sss` 是类级存储，跨 call 但跨「运行」重置
- `i.ss` 默认 NPE；`i.dim` 前缀分派 `sss.` / `ss.` / 无前缀 → `i.a`

## 与预期差异

| 预期 | 实测 |
|---|---|
| `i.sss` 同进程跨运行保留 | ❌ 同 pid 两次运行都从 null 起算 |
| `i.dim` 不带点落实例字段 | ✅ 但落点是 Map `i.a`，不是"同名字段" |
| `i.d` 是当前模块的 BeanShell 解释器 | ✅，且**每次 call 都是新的** |

## 未决

- 重置是否由类加载器重建导致（需静态印证）❓
- `i.sss` 在后台进程/服务里是否同样重置 ❓
