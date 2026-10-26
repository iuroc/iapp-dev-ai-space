# 19 代码编辑器（B8 验收：官方 sora-editor AAR + 带资源外部库）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 目标

B8 最后一项。要求用**官方** sora-editor（不是宿主内置的那份），验证：

1. 带资源的 AAR 怎样进 iApp（iApp 没有 Gradle，也不合并资源）
2. 开发 / 打包两种模式都能跑
3. 语法高亮、行号、文件打开保存

## 工程

```
com.demo.editor/
├── src/mian.iyu         顶栏（文件名 / 新建 / 打开 / 保存）+ FrameLayout 11 + 状态栏 30
├── src/editor.mjava     facade：init / open / newFile / save / status / ticker
├── src/ed_util.mjava    dp / i.sss / 日志 / Toast
├── src/ed_store.mjava   文件目录、列表、读写、首次播种
├── src/ed_sora.mjava    dex 加载、资源挂载、桥接类调用
└── apk/assets/
    ├── sora.dex         2.8 MB（editor + language-java + kotlin-stdlib + 生成的 R + 桥接类）
    └── sora-res.apk     18 KB（AAR 的 res/，包 ID 0x80）
```

## 选型

| 依赖 | 版本 | 说明 |
|---|---|---|
| `io.github.Rosemoe.sora-editor:editor` | 0.21.1 | minSdk 21；自带 19 个资源文件 |
| `…:language-java` | 0.21.1 | 纯代码，提供 `JavaLanguage`（高亮 + 自动补全） |
| `org.jetbrains.kotlin:kotlin-stdlib` | 1.8.10 | sora 的运行期依赖 |

0.23.6 也能用，但多一个 `androidx.collection` 依赖，没选。

## 构建（脚本 `build_sora_dex.py`）

```
AAR classes.jar（剥 R） ┐
language-java.jar       ├─ d8 ──► sora.dex
kotlin-stdlib.jar       │
gen/R.java → javac      │
桥接类 → javac          ┘
AAR res/ → aapt2 compile → aapt2 link --package-id 0x80 → sora-res.apk
```

踩到的坑：`--package-id` 只能 ≥0x7f（用 0x80）；没有 android.jar 时用设备 pull 的
`framework-res.apk` 当 `-I`；JDK 25 要加 `--release 11`；d8 不收目录输入。

## 运行期顺序

```java
activity.getAssets().addAssetPath(sora-res.apk)      // 反射，挂资源（cookie=3/5）
new DexClassLoader(sora.dex, cacheDir, null, null)   // 父加载器必须为 null
cls = dcl.loadClass("iappbridge.SoraHost")
new SoraHost(activity, box, text)                    // 构造函数，参数类型定位
```

## 三代方案与失败读数

### v1 `EditText` + `ForegroundColorSpan` 自己高亮

可行（`Spannable.setSpan` 在 BeanShell 里能用），但用户要求改用官方 sora，作废。
留下的结论：`RippleDrawable` 之外，编辑器还需要等宽字体 + 行号栏滚动同步；
自己实现不如引库。

### v2 反射调用 sora —— 开发模式全 miss

```
ED call-miss setTextSizePx n=1 cls=io.github.rosemoe.sora.widget.CodeEditor total=953 decl=325
ED probe editor getTextHit=0 total=953 head= A A0 A1 A2 A3 A4 B0 B1
ED probe getMethod getText err NoSuchMethodException: getText []
ED probe sameClass=true byNameMethods=953
```

方法表完整、`sameClass=true`、`View` 继承的方法名正常，但 `CodeEditor` 自己声明的
325 个方法名字是 `A`/`A0`/`p3` 这种。同一份 dex 打包后完全正常。

改成「参数类型 + 返回类型」签名匹配后能调通，但重载族错位：
`(float)->void` 命中的不是 `setTextSizePx`，表现为「文本进去了、字号失控、没有高亮」。

### v3 编译桥接类 —— SIGSEGV

把 glue 编译进 dex（`iappbridge.SoraHost`），mjava 只走构造函数 + `View.setTag/getTag`。
结果构造里直接崩：

```
signal 11 (SIGSEGV), fault addr 0x5
#02 io.github.rosemoe.sora.widget.CodeEditor.p3
    /data/app/com.iapp.app-…/oat/x86_64/base.vdex     ← 宿主自己的 vdex
#08 iappbridge.SoraHost.<init>  /data/…/cache/oat/x86_64/sora.vdex
```

## 根因：宿主 APK 自带一份混淆过的 sora-editor

- `base.vdex` 里有 `io.github.rosemoe.sora.widget.CodeEditor.p3`（`grep rosemoe` 命中 15 处）
- `DexClassLoader` 的父加载器是宿主 loader → **父优先委派** → `loadClass` 拿到宿主那份
- 开发模式全 miss、签名错位、SIGSEGV 都是同一个原因

修法一行：

```java
new DexClassLoader(dex, cacheDir, null, null);   // 父加载器 null，只用 boot + 自己的 dex
```

## 验收读数（最终）

```
ED asset dev sora.dex 2795992
ED localize sora.dex 2795992 / sora-res.apk 18112
ED addAssetPath=3
ED sora-source=ours (setTextSizePx found, methods=325)
ED bridge ok
ED attached
ED bridge-log ctx | new | size | font | basic | lang | color | text | add |
ED init sora=ok
ED setText done len=253
ED open Demo.java len=253
```

- 开发环境：编辑器正常、Demo.java 显示、Java 高亮、行号正常、行高正常（用户确认）
- 打包环境：同一份 dex，同样正常（在修父加载器之前就已验证：显示 Demo.java + 高亮）

文件读写闭环（用户点按钮实测）：

```
ED init seed=have=2
ED create Hello.java → open Hello.java len=0
ED openDialog n=3 → open notes.txt len=82 → open Hello.java len=0
ED save Hello.java ok=true len=115
ED open Hello.java len=115          ← 写盘往返长度一致
```

文件放在 `activity.getFilesDir()/iap_editor`，应用私有目录，不需要任何权限。

## 复用结论

1. **AAR 带资源**必须 aapt2 链 → 独立包 ID（≥0x7f）+ 生成真 R + 运行时 `addAssetPath`
2. **`DexClassLoader` 父加载器给 `null`**：宿主可能自带同名类（iApp 就有 sora）
3. 库 API 多时**别从 BeanShell 反射调**，编译桥接类；mjava 只碰构造函数和 `View.setTag`
4. 排查套路：先比「开发 vs 打包」，再看方法名是否被混淆、`sameClass`、类来自哪个 vdex

## Android 15 实机追加（2026-10-26）

用户在 Android 15 实机上运行同一工程时，`DexClassLoader` 拒绝加载 cache 里的 `sora.dex`。

- 根因：targetSdk ≥ 34 时，动态加载的 dex/jar/apk **必须只读**（Android 14 行为变更
  「Safer dynamic code loading」，官方原文见 `external-library-guide.md`）
- 本案例在 API 28 上测不出这条，Android 9 没有该限制
- 修法：写 dex 时「打开输出流 → `setReadOnly()` → 写 → 关闭 → 再设只读」；
  已有文件先 `setWritable(true)` + `delete()` 再重建
- 落地：`ed_sora.sora_write()`，`sora_copy()` / `sora_local()` 都走它

## 未决

- 文本长按选择时 sora 的 `EditorTextActionWindow` 依赖的资源是否全部生效（未逐项验）
- 大文件（>1 MB）高亮与滚动性能未测
- 0.23.6（多一个 `androidx.collection` 依赖）未试
