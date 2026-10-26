# 内部结构（静态分析）

版本前提：iApp 5.0.1013（versionCode 127）。

## 关键类

| 类 | 作用 | 证据 |
|---|---|---|
| `com.iapp.app.Aid_javaCode` | 运行时 `i` 对象本体；390 个公开方法、12 个公开字段 | 反射 + dexdump |
| `com.iapp.app.Aid_jsCode` / `Aid_luaCode` | 其它语言的同构实现 | 静态：同样有静态 `ss_dim` |
| `bsh.Interpreter` 子类 `j6h` | `i.d`：每次 call 新建的 BeanShell 解释器；`f(String)` 导入 `.mjava` | 字节码 |
| `com.iapp.app.VisualDesigner` | 字段 `a9` = 当前工程根（开发环境）；打包后被裁掉 | 字节码 + 打包实测 |
| `qm` | 静态字段容器（307 字段、0 方法），`n` 是 HashMap | dexdump |
| `fj` | 文件/资源工具：`a` 读源码、`s` 建 DexClassLoader | 字节码 |

## 宿主自带的第三方库（重要）

宿主的 APK **自身就打包了一份混淆过的 sora-editor**（IDE 自己的代码编辑器用的）：

```
grep -c rosemoe /data/app/com.iapp.app-*/oat/x86_64/base.vdex   → 15
崩溃栈里可见：io.github.rosemoe.sora.widget.CodeEditor.p3
```

后果：工程里再引入官方 sora 时，`DexClassLoader` 若以宿主 loader 为父，
**父优先委派会拿到宿主那份混淆版**，方法名全是 `A`/`A0`/`p3`，
按名字反射全 miss、按签名匹配错位、编译桥接类直接 SIGSEGV。

对策：`new DexClassLoader(dex, cacheDir, null, null)`（父加载器给 `null`）。

意义不止于 sora：**任何可能被宿主内置的库**（编辑器、图片加载、图表、网络库）
都要考虑这条。开发模式出现「方法名短得像混淆过」时，先查宿主 vdex。

## 字段

`Aid_javaCode` 公开字段：`a`(HashMap)、`b`(Activity)、`c`(Context)、`d`(j6h)、`i`(HashMap)、`ss_dim`(静态 HashMap，默认 null)、`alertdialog` 等，共 12 个。

`ss_dim` 在 `Aid_javaCode` / `Aid_jsCode` / `Aid_luaCode` 中都是 **static**。

## 打包产物结构（APK）

```
assets/lib.so             # 运行库
assets/b5lib.dex          # 工程 apk/assets 下的自定义文件（若有）
assets/oat/x86_64/*.odex  # 打包时生成
assets/extra_conf1g.xml
classes.dex
lib/arm64-v8a/libygsiyu.so
lib/arm64-v8a/libluajava.so
```

工程源码（`.iyu`/`.mjava`）不以明文出现在 APK 中。

## 分析脚本

`docs/scripts/`（本机路径，按需参考）：
- `dex_classes.py` 列类与成员数
- `dex_api_dump.py` 导公开 API
- `dex_body.py` 导方法字节码
- `dex_map_fields.py` 按字段名反查类

依赖 build-tools 的 `dexdump`，经 `DEXDUMP` 环境变量指定。
