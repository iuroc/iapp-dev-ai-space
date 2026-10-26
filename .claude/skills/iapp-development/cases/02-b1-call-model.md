# 02 工程与调用模型（B1）

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 页面

根 LinearLayout(id=1) 内按文件顺序：TextView(2)、LinearLayout(7)、TextView(9)；TextView(10) 写在最后但 `did=7`。
独立模块：app / app2 / app3 / app4 / app5 / bare，坏一个不连坐。

## 读数（logcat 原文）

```
14:52:18.670 V/ygs: B1-start
14:52:18.702 V/ygs: A1 activity=true find=true sameAsTv=true
14:52:18.731 V/ygs: A2 i=true idEq=true gvsNull=false
14:52:18.792 V/ygs: A3 n=3 idx0=2 idx1=7 idx2=9 parentIs7=true
14:52:18.817 V/ygs: A4-1 A4 cnt=1
14:52:18.825 V/ygs: A4-2 A4 cnt=1
14:52:18.857 V/ygs: A5 A5 7
14:52:18.867 V/ygs: JavaErr：… Command not found: findViewById( int ) …
14:52:18.867 V/ygs: B1-end
```

## 结论

| 断言 | 结果 |
|---|---|
| `activity` 与 `i` 都是模块内默认对象 | ✅ |
| `activity.findViewById(2) == i.gvs(2)` | ✅ 同一实例 |
| 裸 `findViewById` | ✅ 报 Command not found |
| 模块级变量跨 call | ✅ 丢失（两次 cnt=1） |
| call 传参/返回值 | ✅ 3+4 → 7 |
| did 树 | ✅ n=3，索引 2/7/9，10 的父是 7 |
| 单模块报错是否连坐 | ✅ 不连坐，载入事件继续执行 |

## 未决

- 兄弟顺序「按文件顺序而不是 id」：本页 id 恰好升序，**没有区分度**，需在 B3 用乱序 id 复测 ❓
- A1–A3 首轮只在屏幕输出、没进日志，后补 `syso` 才拿到；以后探针默认双通道（日志+屏幕）
