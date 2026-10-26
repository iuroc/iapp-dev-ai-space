# 07 外部 JAR（B5 第二部分）

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 过程

1. `i.loadjar("b5lib.jar")`（jar 在工程根）→ `DexPathList[[]]`，`cls=null`
2. 静态看 `j6h.f` / `Aid_javaCode.loadjar` / `fj.s`：路径固定为 `<工程根>/apk/lib/<名>`，用 `DexClassLoader`
3. jar 放进 `apk/lib/` 并 dex 后 → 加载成功；但 `apk/` 属付费打包入口，不可用
4. 改放 `files/`，用 `../../files/x.jar` → `DexPathList[[]]`（路径校验吃掉 `..`）
5. `Class.forName("com.iapp.app.VisualDesigner")` → `ClassNotFoundException`
6. 改用 `activity.getClassLoader().loadClass(...)` 取字段 `a9` 得工程根，自己 `new DexClassLoader` → **成功**

## 读数

```
B5g-sfi=<unknown source>
B5g-rootA=/sdcard/Pictures/ProjectApp/<项目ID>
B5g-rootB=/sdcard/Pictures/ProjectApp/<项目ID>
B5g-exists=true path=/sdcard/Pictures/ProjectApp/<项目ID>/files/b5lib.jar
B5g-class=b5lib.Hello
B5g-inst=jar-inst
B5g-hi=jar-hit
```

## 结论

JAR 放 `files/`，运行时用 `DexClassLoader` 加载；工程根从 `VisualDesigner.a9` 取，取类的 classloader 必须是 `activity`/`i` 的，不能用 `Class.forName`。

## 未决

AAR、纯 dex、so 未实测。
