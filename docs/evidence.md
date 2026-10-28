# 探针证据账本（原始读数）

规则：每轮先在这里追加「日期 / 批次 / 探针 / 原始读数」，再把提炼后的通用结论写进 SKILL。

---

## 2026-10-24 B0 环境基线

**探针**：LinearLayout + TextView(id=2) + `app.mjava`；载入事件 `syso("loading-fired")` + `call(a,"mjava","app.bind")`

```
14:37:46.632 V/ygs: loading-fired
14:37:46.648 V/ygs: ok
```

屏幕：TextView 显示 `Hello from mjava`。

其他读数：

- `adb devices` → emulator-5554；`adb root` → uid=0
- 工程根 `/storage/emulated/0/iApp/ProjectApp/<项目ID>`；入口 `src/mian.iyu`
- bind mount 到 `/data/media/0/*`：sdcardfs 视图为空；到 `/storage/emulated/0/*`：shell 可见，`/proc/<pid>/mountinfo` 无记录
- push 修改文件后 iApp 画布显示 `HOST-SYNC-OK`

---

## 2026-10-24 B1 调用模型

**探针**：app/app2/app3/app4/app5/bare 六个独立模块；iyu 逐项 `syso`

```
14:52:18.670 V/ygs: B1-start
14:52:18.702 V/ygs: A1 activity=true find=true sameAsTv=true
14:52:18.731 V/ygs: A2 i=true idEq=true gvsNull=false
14:52:18.792 V/ygs: A3 n=3 idx0=2 idx1=7 idx2=9 parentIs7=true
14:52:18.817 V/ygs: A4-1 A4 cnt=1
14:52:18.825 V/ygs: A4-2 A4 cnt=1
14:52:18.857 V/ygs: A5 A5 7
14:52:18.867 V/ygs: JavaErr： … Command not found: findViewById( int ) …
14:52:18.867 V/ygs: B1-end
```

---

## 2026-10-24 B2 mjava 铁律

**第一轮**（m_ok…m_shadow 顺序）：

```
14:53:58.804 R-ok=ok
14:53:58.814 R-arr=len=2
14:53:58.825 MJavaErr： Parse error at line 1, column 17.  Encountered: final
14:53:58.843 R-cls=null  ← can't load this type of class file
14:53:58.853 MJavaErr： Error or number too big for integer type: 0xFF000000
14:53:58.860 MJavaErr： Parse error at line 1, column 23.  Encountered: .
14:53:58.871 JavaErr： No static field or inner class: Interpreter of class bsh
14:53:58.881 YuErr： mian.iyu文件,第23行 … call(r8, "mjava", "m_anon.t")
```

**第二轮**（匿名类挪到最后）：

```
14:56:53.684 B2b-start
14:56:53.701 R-cmp=cmp=true
14:56:53.712 R-oll=oll=true
14:56:53.725 R-shadow=s=1 iObj=true
14:56:53.734 YuErr： … call(a4, "mjava", "m_anon.t")   ← 事件中断
```

---

## 2026-10-24 B3 IYU 属性层

**ppt 与 st_ 读数**：

```
15:00:20.226 B3-start
15:00:20.271 B3-order=9,3,5
15:00:20.282 B3-density=3.0 scaled=3.0
15:00:20.287 B3-pad12=12
15:00:20.290 B3-size24=72.0
15:00:20.290 B3-st20=60.0
15:00:20.290 B3-st20sp=42.0
15:00:20.290 B3-def=42.0
15:00:20.294 B3-colorDec=16711680
15:00:20.294 B3-colorHex=-11975345
15:00:20.297 B3-alpha=128.0
15:00:20.297 B3-spaceEq=42.0
15:00:20.297 B3-unknown=true
15:00:20.327 B3-usSt=42.0
15:00:20.327 B3-def2=42.0
```

**锚点复跑**：

```
15:05:45.521 B3-colorDef=-11975345
15:05:45.522 B3-colorHex2=-11975345
15:05:45.525 B3-alphaDef=1.0
15:05:45.526 B3-alpha128=128.0
15:05:45.529 B3b-sA=1
15:05:45.530 B3b-sB-null=true
```

**语法细节**：

```
（注释页）
C-std-ok
x                       ← syso("x","y") 只输出第一个
C-arg-ok
YuErr： mian.iyu文件,第4行 … syso("C-cmt") // trailing comment

（\n 页）
15:11:25.080 C2-start
15:11:25.080 A
15:11:25.080 B
15:11:25.080 C2-nl-ok
15:11:25.080 C2-end
```

---

## 2026-10-24 B4 状态与 i 对象

探针：`b4.api`（反射 i 的类/方法/字段）、`b4.sss`、`b4.sssRead`、`b4.ss`、`b4.dinfo`

**第一轮（单次运行，15:41:37）**

```
15:41:37.617 B4-start
15:41:37.652 B4-iclass=com.iapp.app.Aid_javaCode
15:41:37.663 B4-api d/2
15:41:37.667 B4-api dim/2
15:41:37.706 B4-api ss/1
15:41:37.706 B4-api ss/2
15:41:37.709 B4-api sss/1
15:41:37.710 B4-api sss/2
15:41:37.731 B4-api-count=6 total=390
15:41:37.732 B4-fields=12
15:41:37.733 B4-field a … j（a,b,c,d,e,f,g,h,i,j）
15:41:37.735 B4-field alertdialog / ss_dim
15:41:37.753 B4-sss=1
15:41:37.778 B4-sssRead=1
15:41:37.794 B4-ssread-err=java.lang.NullPointerException … HashMap.get … on a null object reference
15:41:37.795 B4-sswrite-err=java.lang.NullPointerException … HashMap.put … on a null object reference
15:41:37.807 B4-dclass=j6h
15:41:37.811 JavaErr： Method put( java.lang.String, java.lang.String ) not found in class 'j6h' : … i.d.put("b4k","b4v")
15:41:37.811 B4-end
```

解读（待复验）：
- `i` = `com.iapp.app.Aid_javaCode`，390 个公开方法，12 个公开字段
- `i.ss` 内部 HashMap 为 null → NPE（与预期一致）
- `i.d` 是混淆类 `j6h`，无 `put(String,String)`；类型待下一轮反射确认
- 同一进程内两次 call 共享 `i.sss`（sssRead=1）

**第二轮（B4b 反射，15:44:01，pid 5348）**

```
B4b-sig d(com.iapp.app.Aid_javaCode,java.lang.String,) -> int
B4b-sig dim(java.lang.String,java.lang.Object,) -> void
B4b-sig ss(java.lang.String,) -> java.lang.Object
B4b-sig ss(java.lang.String,java.lang.Object,) -> void
B4b-sig sss(java.lang.String,) -> java.lang.Object
B4b-sig sss(java.lang.String,java.lang.Object,) -> void
B4b-dclass=j6h super=bsh.Interpreter
B4b-dmethods=a b c class$ d debug e equals error eval eval eval eval f g get getClass getClassManager getErr getIn getInterface getNameSpace getOut getParent getShowResults getSourceFileInfo getStrictJava getu hashCode invokeMain loadRCFiles main notify notifyAll pathToFile print println redirectOutputToFile run set set set set set set setClassLoader setConsole setErr setExitOnEOF setNameSpace setOut setShowResults setStrictJava source source staticInit toString unset wait wait wait
B4b-dgetmiss=null
B4-sss=1
B4b-sssRead=1
```

解读：
- `i.d` 是 `bsh.Interpreter` 的子类 `j6h` —— BeanShell 解释器确认
- `i.d.get(未定义)` 返回 null，不报错
- `i.dim(String,Object)->void` 只有 setter；`i.d(Aid_javaCode,String)->int` 是同名方法，与字段 `d` 并存
- 本轮 logcat 只记录到 1 次运行（pid 5348），5 轮账本未取全

**账本（同页连跑两次，pid 不变）**

```
15:44:01.751 (5348) B4b-start
15:44:01.853 (5348) B4-sss=1
15:44:01.878 (5348) B4b-sssRead=1
15:45:36.548 (5348) B4b-start
15:45:36.593 (5348) B4-sss=1        ← 第二次运行仍从 null 起算
15:45:36.601 (5348) B4b-sssRead=1
```

结论（待与进程重启对照）：**`i.sss` 在同一进程内、跨两次「运行」不保留**，重置发生在每次运行（疑似每次运行重建类加载器/Aid_javaCode 静态区），而不是进程重启。

**第三轮（B4c，pid 5541，force-stop 后连跑两次）**

```
15:47:36.703 B4c-start
15:47:36.726 B4c-dget0=null
15:47:36.726 B4c-dget1=v1
15:47:36.727 B4c-deval=2
15:47:36.745 B4c-dget-cross=null
15:47:36.761 B4c-dim-d=null
15:47:36.761 B4c-dim-a={b4x=v2}
15:47:36.775 B4c-pre-sss=v3
15:47:36.776 B4c-pre-ss-err=NullPointerException … HashMap.put … null object reference
15:47:36.776 B4c-pre-a={a=v5}
15:47:36.792 B4c-sssRead=null
15:47:41.674 B4c-start（第二次运行，读数完全相同）
```

解读：
- `i.d` 每次 call 新建（`dget-cross=null`）
- `i.a` 每 call 重置（`dim-a={b4x=v2}`，随后 `pre-a={a=v5}`）
- `i.dim` 前缀分派：`sss.` → i.sss；`ss.` → i.ss（NPE）；无前缀 → i.a Map
- `i.sss` 跨 call 有效、跨运行重置

**B4 结论**：`i` = `com.iapp.app.Aid_javaCode`，390 方法 / 12 字段；`i.d` 是 `bsh.Interpreter` 子类且每 call 新建；`i.ss` 默认 null；`i.sss` 是每次运行重置的类级存储。

**待办**：B5（i.call vs i.d.f）、B6 静态印证「每次运行重建类加载器」

---

## 2026-10-24 B5 模块装载（第一批 + 第二批）

**B5a 反射与失败签名（pid 5368 之前一轮）**

```
B5a-i.call(java.lang.String,java.lang.String,) -> java.lang.Object
B5a-i.call(java.lang.String,java.lang.String,[Ljava.lang.Object;,) -> java.lang.Object
B5a-d.f(java.lang.String,) -> boolean
B5a-d.source(java.lang.String,) -> java.lang.Object
B5a-d.eval(java.lang.String,) -> java.lang.Object
B5a-f-err=java.lang.NumberFormatException: For input string: "b5m"
B5a-eval-err=Sourced file … Command not found: b5hi()
B5a-store=ok
B5a-load=err:… Command not found: b5hi()   ← 取回了旧解释器，但当时未导入成功
B5a-call-hi=hit
```

**B5b 导入与计时（15:54:28，pid 5865）**

```
B5b-f-ret=true
B5b-eval-hi=hit
B5b-eval-activity=true
B5b-eval-i=com.iapp.app.Aid_javaCode
B5b-call-avg-ms=5.16504606
B5b-f-avg-ms=0.8693417800000001
B5b-eval-avg-ms=0.22888894
B5b-override=hit2
B5b-store2=ok eval=hit
B5b-load2=cls=j6h eval=hit
```

**静态印证**（`j6h.f` 字节码）：

1. `fj.a(Context,String)` 取源码：先按名字取资源；否则拼 `<工程根>/src/<name>`；文件不存在时 `Integer.parseInt(name)`（这就是 `"b5m"` 抛 NumberFormatException 的原因）
2. 先 `eval` 一段预置代码（定义 `syso/tw/fn/ss/sss/imports` 包装），再 `eval` 模块源码到**当前解释器**
3. 只捕获 `bsh.EvalError`：打印 `MJavaErr：` 并 `return false`；其它异常原样抛出

**结论**：

- `i.d.f("模块.mjava")` 能把模块导入当前解释器，之后可直接 `eval("方法()")`
- 导入后的解释器与主流程共享 `activity`、`i`
- 同名方法后导入覆盖先导入（`hit2`）
- 耗时（本机，50 次均值）：`i.call` 5.17ms；`i.d.f` 0.87ms；`i.d.eval("方法()")` 0.23ms
- 把已导入的 `i.d` 存进 `i.sss`，下一次 call 取回后仍可调用（`load2=… eval=hit`）

---

## 2026-10-24 B6 静态分析（进行中，脚本已可用）

**工具**：`docs/scripts/dex_common.py / dex_classes.py / dex_api_dump.py / dex_body.py / dex_map_fields.py`，调用 build-tools 的 `dexdump`。

**Aid_javaCode 公开成员（静态）**：

```
public  a       Ljava/util/HashMap;     ← i.a（i.dim 无前缀落点）
public  b       Landroid/app/Activity;
public  c       Landroid/content/Context;
public  d       Lj6h;                  ← i.d 解释器
public  i       Ljava/util/HashMap;     ← 与字段名 i 同名
public  ss_dim  Ljava/util/HashMap;     ← i.ss 的底层，默认 null
public  sss     (String)Object / (String,Object)void
public  call    (String,String)Object / (String,String,Object[])Object
public  d       (Aid_javaCode,String)I
```

**qm 类**：`Lqm;` 307 字段、0 方法；`public n Ljava/util/HashMap;`（与「i.sss 落 qm.n」的预期相符，待进一步印证）

**工程元数据**：

- `.project` → `<toolversion>iApp V5.0.1013</toolversion>`（IDE 版本，非运行版本）
- `AndroidManifest.xml` → `<yuv>3</yuv>`

**B5c 装载 API（16:00:01，pid 5993）**

```
B5c-sig loadjar(java.lang.String,) -> java.lang.ClassLoader
B5c-sig loadjar(java.lang.String,boolean,) -> java.lang.ClassLoader
B5c-sig loadjar(java.lang.String,boolean,java.lang.ClassLoader,) -> java.lang.ClassLoader
B5c-sig loadso(java.lang.String,) -> void
```

无 loaddex / loadjar 之外的 dex 入口。

---

## 2026-10-24 B5 外部 JAR（B5d/B5e/B5g）

**B5d（16:17）** jar 在工程根，未 dex：

```
B5d-cl=m4h[DexPathList[[], nativeLibraryDirectories=[/system/lib64, /system/vendor/lib64]]]
B5d-cls=null
```

**B5e（16:23）** dexed jar 放 files/，用 `../../files/b5lib.jar`：

```
B5e-cl=m4h[DexPathList[[], ...]]
B5e-cls=null
```

**静态**：`Aid_javaCode.loadjar → fj.s(Context,String,ClassLoader)`；路径固定为 `VisualDesigner.a9 + "/apk/lib/" + name`，构造 `DexClassLoader`。

**B5f（16:25）** `Class.forName("com.iapp.app.VisualDesigner")`：

```
B5f-rooterr=java.lang.ClassNotFoundException: com.iapp.app.VisualDesigner
```

**B5g（16:26）** 改走 `activity.getClassLoader()` + 自建 DexClassLoader：

```
B5g-sfi=<unknown source>
B5g-rootA=/sdcard/Pictures/ProjectApp/<项目ID>
B5g-rootB=/sdcard/Pictures/ProjectApp/<项目ID>
B5g-exists=true path=/sdcard/Pictures/ProjectApp/<项目ID>/files/b5lib.jar
B5g-class=b5lib.Hello
B5g-inst=jar-inst
B5g-hi=jar-hit
```

**结论**：开发环境外部 JAR 可用；`apk/lib/` 属付费打包入口，弃用。打包安装后的行为未验（B7）。

---

## 2026-10-24 B7 打包安装（第一轮）

**打包产物**：`docs/artifacts/packaged.apk`，4,898,062 字节

| 项 | 读数 |
|---|---|
| package | `com.i7f3d3b94b508ff9f` |
| versionCode | **100001**（= 100000 + versionint 1）✅ |
| versionName | 1.0 |
| minSdkVersion | 21 |
| targetSdkVersion | 36 |
| compileSdkVersion | 36 |
| platformBuildVersionName | 21 |
| assets | `lib.so`、`extra_conf1g.xml`、`dexopt/*` —— **没有** `mian.iyu` 或 `files/b5lib.jar` |
| manifest meta-data | `i_app_logOutput=shi`、`i_app_errLogOutput=shi`（值已确认） |

**运行观测**：

- 打包应用可启动，页面显示 `LIVE-EDIT-OK`（界面打包成功）
- 进程 pid 7471，`/data/data/<包名>/files/iApp/` 只有 `DownloadFileDir`
- **logcat 中没有任何 `ygs` 输出**（meta-data 已带 `shi` 也无效）；打包环境 syso 不可读

**结论**：打包环境不能用日志取证，必须把结果写到界面控件上。已改 `b5h.show()` 把 root/exists/加载结果写进 TextView，待重新打包验证。

**第二轮（b5h，屏幕取证）**：

```
rooterr=java.lang.ClassNotFoundException: Didn't find class "com.iapp.app.VisualDesigner"
  on path: DexPathList[[zip file "/data/app/com.i7f3d3b94b508ff9f-.../base.apk"], ...]
```

→ 打包包裁掉了 `VisualDesigner`，不能靠工程根找库。

**第三轮（b5i，屏幕取证，用户目视 + 截图复核）**：

```
ext=/storage/emulated/0/Android/data/com.i7f3d3b94b508ff9f/files
exists=true
cls=b5lib.Hello
inst=jar-inst
hi=jar-hit
```

→ **打包环境可用路径：`activity.getExternalFilesDir(null)` + `DexClassLoader`**（先把 dex/jar 放到该目录）。

**第四轮（b5j，`apk/assets` 路径，用户目视确认）**：

- 开发环境：`dev=<工程根>/apk/assets/b5lib.dex exists=true`，`cls=b5lib.Hello`、`inst=jar-inst`、`hi=jar-hit` ✅
- 打包环境：assets 释放到 cache 后同样输出 ✅

**打包产物复核（packaged2.apk，4,906,539 B）**：

```
assets/lib.so
assets/b5lib.dex            772 B
assets/b5lib.dex.x86_64.flock
assets/oat/x86_64/b5lib.odex
assets/oat/x86_64/b5lib.vdex
assets/extra_conf1g.xml
```

→ `apk/assets/` 会原样进 APK 的 assets，并生成 odex/vdex。

**B5 收口**：外部库三条路（开发 assets、打包 assets→cache、打包 externalFilesDir）全部可用；`apk/lib` 属付费，不用。

---

## 2026-10-24 B6 补测

```
$ dex_map_fields.py classes4.dex ss_dim
ss_dim  Ljava/util/HashMap;  Lcom/iapp/app/Aid_javaCode;   static
ss_dim  Ljava/util/HashMap;  Lcom/iapp/app/Aid_jsCode;     static
ss_dim  Ljava/util/HashMap;  Lcom/iapp/app/Aid_luaCode;    static

$ dex_classes.py classes4.dex Lqm;
classes4.dex  Lqm;  307 fields  0 methods
```

脚本 `dex_classes / dex_api_dump / dex_body / dex_map_fields` 均可运行。

---

## 2026-10-24 B7 `.iApp` 备份

文件：`/storage/emulated/0/iApp/iAppDir/com.i7f3d3b94b508ff9f.iApp`（3,833,075 B）

**顶层直接是工程内容，没有包名目录**：

```
.project
AndroidManifest.xml
build.xml
icon.png
apk/assets/b5lib.dex (+ .flock, oat/x86_64/*.odex|vdex)
bin/com.i7f3d3b94b508ff9f.apk      ← 已构建的 APK
bin/com.i7f3d3b94b508ff9f.apk.idsig
files/b5lib.jar (+ .flock, oat)
res/
sdk/iapp.sdk
src/*.mjava, src/mian.iyu
```

**导入方式（用户实测）**：直接打开该文件，选择用 iApp 打开；若同包名工程已存在 → 提示导入失败，需先删除旧工程。

---

## 2026-10-24 D1 样式分层 Demo

```
17:14:43.992 D1-start
17:14:44.012 D1-rootChildren=6
17:14:44.016 D1-weight21=0.0 layout_weight331=1.0
17:14:44.025 D1-headerH=0 density=3.0
17:14:44.030 D1-cardPad=48
17:14:44.033 D1-t31Size=54.0 bold=true
17:14:44.037 D1-t32max=2 ellipsize=END
17:14:44.040 D1-vis5=8 vis6=4
17:14:44.043 D1-alpha42=1.0
17:14:44.079 D1-apply-ok radius=36 btnRadius=60
17:14:44.132 D1-report …
```

屏幕（`docs/artifacts/d1.png`）：顶栏标题消失（`weight` 无效 + `width=0`）、圆角正常、`alpha=0.5` 未生效、四层嵌套正常。

结论：`layout_weight` 有效 / `weight` 无效；`alpha` 需 mjava；`padding` 是 px、`textsize` 是 sp；载入事件时 `getHeight()`=0。

---

## 2026-10-24 D1b 波纹 / MD / 属性

```
17:29:55.049 D1b-styles-ok dp8=24 dp24=72
17:29:55.112 D1b-report click7=false click8=true click9=true | bg7=RippleDrawable
             | bg10=RippleDrawable | bg11=GradientDrawable | alpha4=0.5
             | minheight13=120 elevation13=12.0
17:29:55.204 D1b-heights h3=129 h11=129 h13=129
```

屏幕（`docs/artifacts/d1b.png`）：焦点输入框蓝边；圆角按钮正常；`ScrollView` 生效。

结论：ppt 的 `clickable` / `minheight` / `elevation` 均生效且 dp→px；`alpha` 只能 mjava；Ripple 必须 clickable；Button 写 `backgroundcolor` 会丢掉原生波纹。

---

## 2026-10-24 D2 Material 组件

**ppt 直接写自定义类（影子实例）**

```
D2-pre children=0 act=191800877
D2-imm children=0 pad=0 id2031=false
D2c act=191800877 out=STYLES-RAN | … 203 children=0 … card pad=0
D2-post children=0 pad=0 id2031=false
```

同一 Activity、内置 TextView 改动可见；自定义类的 `addView` / `setPadding` 立即读也为 0。

**设计器登记**（`build.xml`）：`<newControl><itme title="…" class="…" info="…"/></newControl>`，iApp 解析代码确认标签拼写为 `itme`。

**动态创建**

```
D2d | 201 children=1 -> MaterialButton attached=false | 202 -> MaterialCardView inner=1
    | 203 -> TextInputLayout inner=1 | 204 -> TextInputLayout inner=1
    | 205 Chip | 206 SwitchMaterial | 207 FloatingActionButton
D2f-theme=none
D2e-mode=2
D2e-post mode=2 h=183
```

屏幕：203 为圆角描边框输入框；204 为 filled 下划线。

---

## 2026-10-26 MDF 表单组件探针（mdform.iyu）

```
MDF til-ok / btn-ok / select-ok / chip-ok / progress-ok / matrix-ok
JavaErr： Method isSingleLine() not found in class
  'com.google.android.material.textfield.TextInputEditText'
```

- 组件创建全部成功（5 类）
- `report()` 因 `isSingleLine()` 在 BeanShell 解析失败而中断，读数未输出；已移除该方法
- 屏幕矩阵：A/B（activity 上下文）呈原生 EditText 外观，C/D（til.getContext）为 outline；A 与 B 无差别 → **决定外观的是 Context，不是 setSingleLine**

**第二轮读数（09:46:00）**

```
110 mode=2 ctxCls=ContextThemeWrapper
111 mode=1
112 mode=0
113 mode=2
114 mode=2
124-0 mode=2 ctxIsAct=true  ctxCls=com.iapp.app.run.mian
124-1 mode=2 ctxIsAct=true  ctxCls=com.iapp.app.run.mian
124-2 mode=2 ctxIsAct=false ctxCls=androidx.appcompat.view.ContextThemeWrapper
124-3 mode=2 ctxIsAct=false ctxCls=androidx.appcompat.view.ContextThemeWrapper
120 n=4  121 n=3  122 n=3  123 n=3
```

结论：`TextInputLayout` 构造时把 Context 包成 `ContextThemeWrapper`；子控件用 activity 会绕过主题覆盖，因此画成原生下划线。组件创建（按钮 4、选择 3、Chip 3、进度 3）全部成功。

---

## 2026-10-26 事件探针第一轮（events.iyu）

```
10:12:35.813 g-loading
10:12:57.267 c10-touchmonitor / c10-clicki
10:13:04.884 c10-press
10:13:10.434 c11-clicki / 10:13:12.827 c11-press
10:13:21.738 c12-focuschange
10:13:22.762 c12-keyboard → 22.778 beforetextchanged → 22.798 ontextchanged → 22.814 aftertextchanged
10:13:23.240 c12-editormonitor + 三连
10:13:34.815 之后每次按键持续 c12-keyboard
10:13:41.442 / 42.328 c13-clicki（勾选）
```

- 控件级 `<event><eventItme>` 语法成立
- 未触发：`pressmenu`、`checkbox`、`checkedchange`、以及除 `loading` 外的全局事件（`onresume/onpause/onstart/onstop/ondestroy/keydown/keyup/loadingend/loadcomplete`）
- `keyboard` 每次按键都触发，高频
- 文本变化顺序：`keyboard → editormonitor → beforetextchanged → ontextchanged → aftertextchanged`

## 2026-10-26 短名问题

`type="Switch"` 在设计器显示“未知”。改为 `android.widget.Switch` 并在 `build.xml` 登记 `<itme title="Switch" class="android.widget.Switch" info="原生开关"/>`。

---

## 2026-10-26 黑金计算器（com.demo.calc）

```
CALC styles-ok
CALC init
CALC key=1 acc= op= cur=1
CALC key=+ acc=1 op=+ cur=
CALC key=2 acc=1 op=+ cur=2
CALC key== acc=3 op= cur=
CALC key=× acc=5 op=× cur=
CALC key=4 acc=5 op=× cur=4
CALC key== acc=20 op= cur=
CALC key=÷ acc=5 op=÷ cur=
CALC key=0 acc=5 op=÷ cur=0
CALC key== acc=ERR op= cur=
CALC key=± acc= op= cur=-7
CALC key=% acc= op= cur=0.5
CALC key=⌫ acc= op= cur=12
CALC key== acc=3.75 op= cur=
```

- 七个用例全部符合即时执行预期
- 状态在 `i.sss`（`calc.cur/acc/op/fresh`）跨 call 保持
- 视觉问题：行 `height=-2` 导致不铺满；改为行 `height=0 + layout_weight=1`、按钮 `height=-1`（视觉待确认）
- `layout_margin=4dp` 不可靠，改为四方向分别写

---

## 2026-10-26 内置短名页闪退（builtins.iyu）

用户提供 `e.iyu` 全量短名清单；复制为探针页后闪退：

```
FATAL EXCEPTION: main
java.lang.IllegalArgumentException: DrawerLayout must be measured with MeasureSpec.EXACTLY.
  at androidx.drawerlayout.widget.DrawerLayout.onMeasure(...)
```

原因：40 号 `DrawerLayout` 写的是 `width=-2 height=-2`。改为 `300dp × 300dp` 后待复测。

清单本身未受影响；`Switch` 的短名确认为 `SwitchCompat`。

---

## 2026-10-26 事件类型权威表（dex）

来源：`com.iapp.app.VisualDesigner.<init>` 里的 const-string 表（设计器支持的事件名）。

控件事件组（原文）：

```
oncheckedchanged / onoffsetchanged
clicki / touchmonitor / press / keyboard / pressmenu
editormonitor / ontextchanged,beforetextchanged,aftertextchanged
focuschange
onscrollstatechanged,onscrolled,onscroll
clickitem
onprogresschanged,shouldoverrideurlloading,onpagestarted,onpagefinished,onreceivederror,ondownloadstart
onpageselected,onpagescrolled,onpagescrollstatechanged
ondrawerclosed,ondraweropened,onoptionsitemselected
onitemselected,onnothingselected
onpicturecallback
onstarttrackingtouch,onstoptrackingtouch,onprogresschanged2
ontabselected,ontabunselected,ontabreselected
onrefresh
```

界面事件：

```
loading / loadingComplete / menu / downkey / upkey / destroy / stop / restart / start / resume / pause
onactivityresult / onrequestpermissionsresult / sensor
```

要点：

- 没有 `androidResume` 等名字；events2 里那批不会触发
- “载入完毕”是 `loadingComplete`
- 滚动事件正确名字是 `onscrolled`（不是 `onscrollchanged`）

运行期已确认：`loading`、`clicki`、`touchmonitor`、`press`、`keyboard`、`editormonitor`、`ontextchanged/before/after`、`focuschange`、`oncheckedchanged`、WebView 的 `onpagestarted/onprogresschanged/onpagefinished/onreceivederror`。
`pressmenu` 仍未触发（条件未知）；生命周期与滚动待 events6 复测。

---

## 2026-10-26 events6：生命周期确认 + 滚动未触发

```
12:27:50.376 g-loading
12:27:50.394 g-start
12:27:50.475 g-loadingComplete
12:28:12.342 c10-press
12:28:18.298 g-pause
12:28:18.321 g-stop
12:28:22.206 g-restart
12:28:22.223 g-start
12:28:22.238 g-resume
12:28:30-40 多组 g-downkey / g-upkey（成对）
```

- 生命周期名字确认：`loading → start → loadingComplete`；Home：`pause → stop`；回来：`restart → start → resume`
- `downkey/upkey` 成对触发（返回键等物理/导航按键）
- `press` 正常，`pressmenu` 仍未触发
- **ScrollView 上的 `onscrolled/onscroll/onscrollstatechanged` 全都没有触发**（用户上下滑动无日志）→ 滚动事件大概只绑在列表型控件上，待 events7 用 ListView/WebView 验证

---

## 2026-10-26 events7：ListView / Spinner / WebView

```
12:31:36.213 E7-setup-ok
12:31:36.357 s31-onitemselected
12:31:44-12:32:01 l30-onscroll（大量）+ l30-onscrollstatechanged（多次）
12:31:49 / 51 / 59 / 12:32:00 / 01 l30-clickitem
```

- ListView：`onscroll` ✅、`onscrollstatechanged` ✅、`clickitem` ✅；`onscrolled` ❌
- Spinner：`onitemselected` ✅；`onnothingselected` 未出现（非空列表）
- WebView：`w32-*` 一个都没有 → WebView 不支持滚动事件
- 结论：滚动事件属于列表型控件；`onscrolled` 可能只属于 RecyclerView

---

## 2026-10-26 events8 第一轮：SeekBar 命中、SwipeRefreshLayout 导入错误

```
13:03:09.162 W/System.err: IllegalArgumentException: View=android.widget.RelativeLayout{...} not attached to window manager
13:03:12.150 V/ygs: EV sb40-onprogresschanged2
13:03:12.168 W/System.err: Typed variable declaration : Class: SwipeRefreshLayout not found in namespace
                  : at Line: 19 : in file: inline evaluation of: ``import android.view.ViewGroup; ...
13:03:12.168 V/ygs: JavaErr：... SwipeRefreshLayout
```

读数：

- `e8.setup()` 在 `import android.widget.SwipeRefreshLayout` 处整块抛错（第 19 行），**一行错导致后面的代码全部不执行** → setup 必须按块 try/catch
- 错误行之前的 `sb.setProgress(30)` 已经执行，它**触发了 `onprogresschanged2`**（时间 12.150 早于报错 12.168）→ `onprogresschanged2` 对程序化 setProgress 也回调
- `onprogresschanged` 没有出现 → SeekBar 上那个名字不是有效事件（设计器把它归在浏览器组）
- base.apk 里有 `Landroidx/swiperefreshlayout/widget/SwipeRefreshLayout;`（143 个方法），正确导入是 `androidx.swiperefreshlayout.widget.SwipeRefreshLayout`
- 13:03:09.162 那批 `not attached to window manager` 是设计器切换页面时的既有噪声，与探针无关

修正：e8.mjava 改为三段独立 try/catch，导入改为 androidx；onrefresh 走 `e8.onrefresh()` 里 `setRefreshing(false)` 收尾。

---

## 2026-10-26 events8 第二轮：SeekBar / SwipeRefresh / 空 Spinner

```
13:07:15.742 EV sb40-onprogresschanged2      ← e8.setup 里 setProgress(30)
13:07:15.751 E8-seekbar-ok
13:07:15.759 E8-spinner-ok
13:07:15.773 E8-swipe-ok
13:07:15.773 E8-setup-done
13:07:21.408 EV sb40-onstarttrackingtouch
13:07:21.600~22.208 EV sb40-onprogresschanged2 ×18（连续拖动）
13:07:22.361 EV sb40-onstoptrackingtouch
13:08:12.139 EV sw42-onrefresh
```

- SeekBar：`onstarttrackingtouch` ✅（手指按下）、`onprogresschanged2` ✅（每次进度变化，程序化 setProgress 也触发）、`onstoptrackingtouch` ✅（抬起）；`onprogresschanged` **全程没出现** → 该名字在 SeekBar 上无效
- SwipeRefreshLayout：`onrefresh` ✅，下拉后转圈出现；但绑定的是 `ev.mark`，没人调 `setRefreshing(false)`，**转圈不会自己停**（用户反馈：42 有下拉，没有自动清除）
- 空 Spinner：点开没有任何日志，`onitemselected`/`onnothingselected` 都没触发
  → 空列表下两个回调都不走；`onnothingselected` 是否只在“有选中项被清空”时触发，待 events9 用「先选后清空」验证

---

## 2026-10-26 events9：Spinner 反选 / Tab / 长按菜单

```
13:24:25.363 E9-spinner-ok
13:24:25.386 EV tab52-ontabselected        ← setup 里 addTab 三次，只第一枚触发
13:24:25.395 E9-tabs-ok
13:24:25.487 EV sp50-onitemselected        ← setAdapter 后自动选中第 0 项并回调
13:24:40.203 EV sp50-onitemselected        ← 用户手选
13:24:42.670 E9-clear-start
13:24:42.684 E9-spinner-cleared            ← setAdapter(空) 之后没有任何 onnothingselected
13:24:48.551 EV tab52-ontabreselected      ← 重复点当前 tab
13:24:49.167/759 EV tab52-ontabunselected / tab52-ontabselected（切换 tab，成对）
13:25:00.502 EV tab52-ontabreselected
13:25:11.799 / 13:25:13.958 / 13:25:20.967 EV btn53-clicki
13:25:13.224 / 13:25:15.186 / 13:25:20.264 / 13:25:22.040 EV btn53-press
（btn53-pressmenu 一次都没有；ui-menu 也没有。用户：event9 没有菜单）
```

- TabLayout：`ontabselected` ✅、`ontabunselected` ✅、`ontabreselected` ✅（重按当前页）；切换时 unselected+selected 成对出现；`addTab` 时首枚自动 selected 也会回调
- Spinner：`onitemselected` ✅，且 **setAdapter 后自动回调一次**（默认第 0 项）
- Spinner：先选后清空，`onnothingselected` 仍然 ❌ 不触发（空列表点开也不触发）→ 两种条件都不走，视为不可用
- `pressmenu` ❌：Button 单击/长按都正常，长按菜单事件四次按压均未触发；界面事件 `menu` 也没触发（LDPlayer 无菜单键）
- 用户复核 events8：[42] 下拉转圈现在能自动清除（`setRefreshing(false)` 生效）

## 2026-10-26 events4 第一次：模块名写错

```
13:25:49.326 JavaErr：Method loadHtml() not found in bsh scripted object: global
```

events4.iyu 的 `<UIEventset>` 写的是 `call(null,"mjava","ev.loadHtml")`，但 loadHtml 在 `e4.mjava` 里 → 改成 `e4.loadHtml`。

---

## 2026-10-26 events4 第二轮：WebView 链接被拦

```
13:28:07.193 E4-loaded
13:28:07.230 EV e4-progress
13:28:07.295 EV e4-pagestarted
13:28:07.310 / .325 / .341 EV e4-progress ×2
13:28:07.341 EV e4-pagefinished
13:28:14.459 EV e4-shouldoverride      ← 点链接 ①
13:28:14.476/491/505 EV e4-progress ×3（之后没有 pagestarted/pagefinished）
13:28:21.855 EV e4-shouldoverride      ← 点链接 ②
13:28:21.869/902/916 EV e4-progress ×3
```

- 首屏 `loadData`：`pagestarted → onprogresschanged ×5 → pagefinished` ✅
- 点链接：`shouldoverrideurlloading` ✅ 触发一次；但**没有 pagestarted/pagefinished** → iApp 的处理器把这次导航吞掉了，页面没跳转
- `ondownloadstart` ❌、`onreceivederror` ❌：override 挡在前面，下载/错误都没机会发生
- 结论：**iApp 内 WebView 里的链接点了不跳**；要跳转/下载必须在 `shouldoverrideurlloading` 的 mjava 里自己处理（`loadUrl` / 系统浏览器 / 下载器）

## 2026-10-26 events10：抽屉 / destroy

```
13:29:29.006 E10-setup-ok
13:29:30.041 E10-open-called  → 13:29:30.430 EV dl60-ondraweropened
13:29:31.319 E10-close-called → 13:29:31.715 EV dl60-ondrawerclosed
13:29:32.184 E10-open-called  → 13:29:32.581 EV dl60-ondraweropened
13:29:32.983 EV dl60-ondrawerclosed   ← 用户点抽屉外关闭
13:29:35.396 EV ui-destroy             ← 退出页面
```

- DrawerLayout（ppt 精确 320dp×300dp）`ondraweropened` ✅、`ondrawerclosed` ✅，程序化 `openDrawer/closeDrawers` 与点外部关闭都会回调
- 界面事件 `destroy` ✅，退出页面时触发
- switcheroo：ppt 里 DrawerLayout 可以用 mjava `addView` 动态塞内容区 + 抽屉（抽屉用 `DrawerLayout.LayoutParams(240, MATCH_PARENT).gravity=LEFT`）

补充读数：events4 里还绑了 `onreceivedtitle` / `onloadresource` / `onconsolemessage` 三个**不在权威名单**的事件名，全程既没有回调也**没有 YuErr**。
→ 事件名写错/不存在时 iApp **静默忽略**，不报错。只能靠对照 `VisualDesigner` 的名单自查。

---

## 2026-10-26 B8 第一例：文件管理器（com.demo.filemgr）

```
13:42:43.522 FM-start path=/storage/emulated/0
13:42:43.553 FM-perm-granted=true          ← 开发模式直接 true，无弹窗、无 onrequestpermissionsresult
13:42:43.582 FM-list /storage/emulated/0 count=16
13:43:12.881 FM-click pos=1 → FM-list .../Android count=2
13:43:26.489 FM-click pos=4 → FM-list /data count=0
13:43:25.265 FM-up root
13:43:24.174 FM-list / count=45
13:43:18.800 FM-click pos=0 → FM-file .../open/1792832533843_853125.apk size=4889870
13:43:54.524 FM-long pos=2
13:44:08.468 FM-del /sdcard/Pictures/bindtest/marker.txt ok=true → FM-list ... count=0
```

- 匿名接口的回调里调脚本方法（`onItemClick → fmTap(pos) → fmReload()`）**正常**
- 长按 + AlertDialog 删除成功，删除后列表自动刷新
- `/data` 无权限：`listFiles()` 返回 0 项，不抛异常
- 开发模式 `checkSelfPermission(WRITE_EXTERNAL_STORAGE)` = true，**权限继承自 iApp 宿主进程**
- 用户实测：打包安装版同样可用

---

## 2026-10-26 2048 实战（com.demo.game2048）

目标：用 SKILL + docs 从零做经典 2048，反向验证文档缺口。
工程：`android-sync/ProjectApp/com.demo.game2048/`，`src/mian.iyu` + `src/game.mjava`（单模块）。
环境：iApp 5.0.1013 / Android 9 (API 28) / 1080×1920 density 3.0。

### 启动与布局

```
13:55:12.089 G2048 newGame board=0,0,0,0,0,0,0,0,0,2,0,0,0,4,0,0
13:55:12.091 G2048 init score=0 best=0 board=...
13:55:12.419 G2048 layout side=984 cell=208
```

- `loadingComplete` 里 `findViewById(31).getLayoutParams()` 改 `width/height` 生效：棋盘 984px 正方形，格子 208px
- 动态 `addView` 的 16 个格子 + 瓦片正常渲染，`bringToFront()` 后弹层压住瓦片
- 用户屏幕确认：棋盘正方形、格子/数字/顶部分数框显示正常

### 自检（8 项全 PASS）

```
G2048 TEST left-merge PASS 4,8,0,0,... add=12
G2048 TEST no-double PASS 4,4,0,0,...
G2048 TEST gap-merge PASS 4,0,0,0,...
G2048 TEST noop PASS changed=0
G2048 TEST right-move PASS 0,0,0,4,...
G2048 TEST gameover PASS canMove=false
G2048 TEST win-2048 PASS 2048,0,0,0,...
G2048 TEST roundtrip PASS 2,4,2,4,...
```

- 纯逻辑用例在 `loading` 里跑、结果写 `i.syso`，是可行的**应用内自检**方式
- 每次重新运行都会重跑一遍，8 项全 PASS

### 键盘（downkey）

```
13:55:16.650 G2048 key code=22 dir=1
13:55:17.439 G2048 key code=21 dir=0
13:55:17.847 G2048 key code=20 dir=3
```

iyu 写法：`<eventItme type="downkey">call(null,"mjava","game.keyCode", st_kC)</eventItme>`

- 方向键 19/20/21/22 → 上/下/左/右 ✅（mjava 侧统一收到 `keyCode`）
- **隔离复核（14:07）**：把 `setOnKeyListener` 注释掉、只留 `downkey` 事件，方向键仍全部生效
  → `downkey` + `st_kC` **单条即可工作** ✅（不再需要 View 级监听器兜底）
- 反编译 `main2` 的 UIEventset 参数表：`downkey/upkey` 声明为 `st_kC,st_eA,st_eR`（键码/动作/重复计数）
- 非方向键（Ctrl=113、A=29、C=31）进来只打 `key other=`，不误触

### 滑动（mjava OnTouchListener）

```
13:56:35.063 G2048 touch dx=-727.875 dy=-3.555542 dir=0
13:56:35.671 G2048 touch dx=544.5 dy=12.444336 dir=1
13:56:40.439 G2048 touch short dx=0.0 dy=0.0
13:56:44.975 G2048 touch dx=18.0 dy=344.88892 dir=3
13:56:45.558 G2048 touch dx=73.6875 dy=266.66663 dir=3
```

- `boardFrame.setOnTouchListener(new View.OnTouchListener(){...})` ✅；回调里调模块方法 `touchStart/touchEnd/doMove` 正常
- 主导轴判向 + 24dp 阈值有效：短触（0,0）被忽略
- 用户确认：四向滑动都能移动、能合并

### 动画与输入锁

```
13:55:17.848 G2048 move dir=D add=4 score=4 spawn=5 ...
13:55:17.850 G2048 anim slide tiles=4
13:55:17.974 G2048 step2 merged=1 spawn=5
13:55:18.067 G2048 key code=22 dir=1
13:55:18.067 G2048 move queued dir=R
13:55:18.118 G2048 apply pending=1
```

- `ObjectAnimator.ofFloat(view,"translationX", new float[]{0f,dx})` + `setDuration` ✅
- 滑动 110ms → `postDelayed(匿名 Runnable, 120)` 回调 `afterSlide/step2` ✅
- 合并放大回弹（scaleX/scaleY 两段）、新块 scale+alpha 进场 ✅
- 动画期间第二输入进入 `g.pending`，结束后自动执行；用户确认视觉连贯
- `AnimatorListenerAdapter` 未使用（抽象类，BeanShell 不可匿名继承）；结束点用 `postDelayed` 代替

### 持久化（杀进程恢复）

```
13:56:34.121 G2048 init score=0  best=12 board=0,2,0,0,0,2,...   ← 新游戏后仅 best 保留
13:56:50.289 G2048 init score=8  best=12 board=0,0,4,0,0,0,0,0,0,0,0,4,0,2,0,4
```

- `activity.getFilesDir()/game2048.save` + `FileWriter` / `BufferedReader` ✅
- 每次有效移动立即落盘；杀掉 iApp 进程再开工程，棋盘/分数/最高分原样恢复
- 新游戏清空棋盘与 score，但 best 保留（上面 13:56:34 组）

### 噪音

```
W/System.err: java.lang.IllegalArgumentException: View=... not attached to window manager
  at com.iapp.app.VisualDesigner$i1.handleMessage
```

- 退出运行预览时 iApp 自己拆悬浮窗的日志，与游戏代码无关，不要当错误查

### 复核：隔离键盘 / 胜利弹层 / 死局识别

```
14:07:14.753 G2048 init score=1024 best=2048 board=1024,1024,0,0,...
14:07:17.155 G2048 key code=22 dir=1
14:07:17.172 G2048 move dir=R add=2048 score=3072 spawn=8 board=0,0,0,2048,...
14:07:17.488 G2048 win
14:07:28.215 G2048 keepPlaying
14:07:27.224 G2048 key other=57
14:07:27.172 G2048 key repeat ignored=57

14:08:48.834 G2048 init score=468 best=3096 board=2,4,2,4,4,2,4,2,...
14:08:49.038 G2048 restore gameover
```

- 存档写入近胜局面（`1024,1024`），**只按方向键**（`key code=22`）即合并出 2048 → `G2048 win`，胜利弹层正常；点“继续挑战”后 `keepPlaying`，后续继续用方向键移动 ✅
- 满盘死局且存档故意写 `over=0`，启动时 `restoreOverlay()` 自己算出无路可走 → `restore gameover`，弹层直接出现 ✅
- 长按/连按会产生重复 `downkey`，120ms 去抖日志 `key repeat ignored=57` 生效 ✅
- `setOnKeyListener` 全程处于注释状态，以上移动全部由 iApp 事件驱动 → 键盘结论已隔离 ✅

### 静态分析补充（dexdump classes4.dex）

- `VisualDesigner` 的 `downkey/upkey` 参数描述：
  `st_kC = 按下的物理按键对应的数值`、`st_eA = 执行的动作`、`st_eR = 检索事件的重复计数`
- `main2$i.onTouch` 里 `touchmonitor` 的派发串包含：view、view id、action、x、y、rawX、rawY
  （裕 3 运行期的参数变量名未确认；本项目改用 mjava `setOnTouchListener`）
- `touchmonitor` 事件名出现在 `Aid_javaCode` / `Aid_jsCode` / `Aid_luaCode` / `main2$i`，是引擎级能力

### 本轮文档缺口（已回填）

1. `downkey` 能拿键码、变量名 `st_kC`，且单条入口就够 —— events-guide 原来只写"触发"，没写参数
2. `touchmonitor` 的参数清单 —— 原文只有一句话，补了静态证据与替代方案
3. BeanShell 里做动画的可行写法 —— 原来没有 animation 文档
4. `getFilesDir()` 持久化 + 杀进程验证 —— recipes 原来没有
5. 动态瓦片跨 call 定位 —— 靠 `setTag("tile:"+idx)`，模块变量跨 call 必丢
6. 应用内自检模式 —— 原来只有"探针页 + 用户操作"，没有"纯逻辑用例自动跑"

---

## 2026-10-26 浏览器首轮：`url` 未定义 + 反查 DEX 找到事件变量

```
13:50:32.776 BR-UA Mozilla/5.0 (Linux; Android 9; 25060RK16C Build/PQ3A.190705.09211140; wv)
               AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36
13:50:33.216 BR-finished title=about:blank url=about:blank
13:50:45.206 JavaErr：Method override() not found in bsh scripted object: global
```

`retval` 里写 `call(...,"br.override", url)` 时 `url` 是未定义变量 → 参数被丢掉 → 调用变成零参 `override()`。

**纠正前面 events4 的结论**（`shouldoverrideurlloading` 不是“永远拦截”）。反查 `Lcom/iapp/app/run/mian$i0;.shouldOverrideUrlLoading`：

```
0x0000 getTag → gl.j(tag, "<eventItme type=\"shouldoverrideurlloading\">", "</eventItme>")
0x001f new qm(activity)
0x0023 qm.Z("st_vId", view.getId())
0x002e qm.Z("st_vW", view)
0x0033 qm.Z("st_url", url)
0x0036 qm.s(eventCode)
0x0039 return true                       ← 有事件：执行后直接 true，默认跳转被跳过
0x003a … E0(url.toLowerCase())           ← 无事件：http/https/rtsp/ftp
0x0044 WebView.loadUrl(url)
0x0048 … Intent(ACTION_VIEW) + startActivity
```

`gl.E0` 只认 `http:` `https:` `rtsp:` `ftp:` 四个前缀。

事件变量全表（`run/mian$*` 各监听器里 `qm.Z("st_…")`）：

| 监听器 | 变量 |
|---|---|
| `$i` onClick / `$l` onLongClick / `$n` onCreateContextMenu | `st_vId` `st_vW` |
| `$r` onItemClick | + `st_pN`（position）`st_iD`（row id） |
| `$s` onItemSelected / onNothingSelected | + `st_vW2` |
| `$q` onScroll | `st_fM` `st_vT` `st_bT`；onScrollStateChanged → `st_sE` |
| `$w` onScrolled（RecyclerView） | `st_dX` `st_dY` `st_isB` + 上面四项 |
| `$t` onProgressChanged | `st_nS`（进度）`st_fR`（fromUser） |
| `$u` onTab* | `st_pN` `st_tT` `st_taB` |
| `$z` onPage* | `st_pN` `st_pS` `st_pT` `st_sE` |
| `$b0` onCheckedChanged | `st_iC` |
| `$p` onFocusChange | `st_hF` |
| `$c0` onOffsetChanged | `st_vO` |
| `$j` onTouch | `st_eA` `st_eX` `st_eY` `st_rX` `st_rY` |
| `$m` onKey | `st_eA` `st_eR` `st_kC` |
| `$o` onEditorAction | `st_aI` `st_eA` `st_eK` `st_eR` |
| `$h` 传感器 | `st_x` `st_y` `st_z` |
| `$i0` WebView | `st_url` `st_bP`；onReceivedError 只有 `st_vId` `st_vW` |
| `$a0` SwipeRefresh onRefresh | `st_vId` `st_vW` |

浏览器 `mian.iyu` 已改为 `call(null, "mjava", "br.override", st_url)`。

---

## 2026-10-26 B8 第二例：浏览器（com.demo.browser）

```
14:05:51.079 BR-UA ... Chrome/91.0.4472.114 Mobile Safari/537.36
14:05:53.916 BR-override url=https://www.baidu.com/
14:05:54.658 BR-finished title=百度一下 url=https://www.baidu.com/
14:06:05.379 BR-override url=https://example.com/next
14:06:05.942 BR-finished title=Example Domain url=https://example.com/next
14:06:33.870 BR-go https://i.2980.com
14:06:33.939 BR-override url=https://login.2980.com/authorize?…
14:06:34.465 BR-finished title=火星公共登录平台 url=https://login.2980.com/authorize?…
14:06:36.610 BR-back
14:06:36.711 BR-finished title=about:blank url=about:blank
```

- `st_url` ✅ 完整目标地址；绝对链接 / 相对链接（按 base 解析）/ 站点登录跳转全部接住
- `canGoBack/goBack` ✅
- `onprogresschanged` 到 100 一次加载回调 3 次
- `loadDataWithBaseURL` 的本地页 `getUrl()` 返回 `about:blank`，不是 base
- 用户反馈界面无异常

---

## 2026-10-26 应用图标（所有 ProjectApp 工程）

### 蓝方块的原因

`create_project.py` 早期写的 70 字节 `icon.png` 注释是“1×1 透明 PNG”，解码实际是：

```
size 1 x 1  bit 8  colorType 6  raw=01 00 00 FF 7F
→ RGBA (0,0,255,127)：半透明蓝色
```

启动器把一个像素拉满整个图标 → 所有脚本新建工程都是蓝方块。

### 图标如何进 APK

```
aapt dump badging com.demo.game2048.apk
application-icon-160/240/320/480/640:'res/mipmap-*/img_iapp.png'
application: label='2048' icon='res/mipmap-mdpi-v4/img_iapp.png'

md5(工程 icon.png) == md5(APK res/mipmap-xxxhdpi-v4/img_iapp.png)
```

- iApp 把工程 `icon.png` **原样**写进各 density 的 `img_iapp.png`，不做切图
- 在 iApp 里手动新建的工程默认图标是 192×192、`#50C4E5` 底 + 白色标志
- 因此图标完全由工程根 `icon.png` 决定

### 离线生成器

新增 `docs/scripts/make_icon.py`（纯标准库，不联网、无 Pillow）：

- 标题有数字 → 大字徽章（`经典 2048` → `2048`）
- 有英文 → 首字母/短词（`File Manager` → `FM`）
- 纯中文 → 品类符号（计算器/文件夹/地球/笔记/聊天…）
- 已接入 `create_project.py`：不传 `--icon` 时自动生成

批量给现有 8 个工程补图：

```
com.demo.game2048   text='2048'      category=game
com.demo.calc       symbol=计算器    category=calc
com.demo.filemgr    symbol=文件夹    category=file
com.demo.browser    symbol=地球      category=browser
com.demo.selector   symbol=滑块      category=tool
com.demo.newproject / scaffold / com.i7f3d3b94b508ff9f → 九宫格
```

- 打包安装链路与桌面图标均已目视确认正常（2048 米色大字；计算器黑金，用户 2026-10-26）
- 产物样例与解包对照图存 `docs/artifacts/icon-probe/`

### 回填

`SKILL.md`、`references/icon-guide.md`（新建）、`project-structure.md`、`pitfalls.md` 第 19 条、
`docs/scripts/make_icon.py`、`docs/scripts/create_project.py`。

---

## 2026-10-26 模块化探针（com.demo.game2048/probe.iyu）

问题：单个 `game.mjava` 太长，SKILL 只有 `i.d.f` 的性能数据，没有“模块 A 能否直接调 B”和拆分规范。

探针：`pa.mjava` 逐项调用，`pb/pc/putil` 作为被导入模块；`probe.iyu` 的 `loading` 依次 `call`。

### 原始读数

```
14:27:17.071 MP caseImport start
14:27:17.075 MP import-ret=true
14:27:17.075 MP b-hello
14:27:17.075 MP direct-after-import=ok

14:27:17.083 MP eval-import-ret=true
14:27:17.083 MP b-hello
14:27:17.083 MP eval-call=null
14:27:17.083 MP eval-add=5

14:27:17.090 W/System.err: Command not found: b_hello() : at Line: 36 ...
14:27:17.090 V/ygs: JavaErr：
14:27:17.090 V/ygs: Command not found: b_hello() ...
   ← caseDirect 在导入前调用，方法直接中断；没有进 catch，也没有后续日志

14:27:17.105 MP util-dp8=24 tag=UTIL
14:27:17.115 MP collision-same=3
14:27:17.121 MP missing-err=java.lang.NumberFormatException: For input string: "nope.mjava"
14:27:17.128 MP state-after-inc=2
14:27:17.134 MP state-fresh-call=0
14:27:17.141 MP path-src-err=java.lang.NumberFormatException: For input string: "src/putil.mjava"
14:27:17.145 MP b-hello          ← iyu 直接 call 第二个模块
```

### 判定

| 结论 | 级别 |
|---|---|
| `i.d.f("pb.mjava")` 返回 `true`，把模块导进**当前解释器** | ✅ |
| 导入后可以**不加前缀直接调** `b_hello()` / `b_add(2,3)` | ✅ |
| `i.d.eval("b_add(2,3)")` 返回 `5` | ✅ |
| `.iyu` 可以直接 `call` 任意模块（`pb.b_hello`） | ✅ |
| 工具模块同样可导入复用（`putil` → `u_dp(8)=24`） | ✅ |
| 同名方法**后导入覆盖先导入**（pb=2, pc=3 → 3） | ✅ |
| 模块级变量在同一次 `call` 内保留（累加到 2），下一次 call 归 0 | ✅ |
| 未导入就调用 → `Command not found`，**整个方法中断，`catch(Throwable)` 也接不住** | ✅ |
| 缺文件 → `NumberFormatException: For input string: "nope.mjava"`（不返回 false） | ✅ |
| 路径是相对 `src/` 的**裸文件名**；`src/putil.mjava` 会失败 | ✅ |

### 影响

- 模块化可行：一个 facade 统一 `i.d.f` 导入，子模块方法加前缀，直接互调。
- 导入必须发生在调用之前；不能把“可能未导入”的调用包在 try/catch 里兜底。
- 拆分层次要避免环：`util ← core/store/ui/anim ← game`，动画只放原语，回调留在 facade。
- 详见 `references/modularization-guide.md` 与 `cases/15-modularization.md`。

### 2048 七模块拆分首轮失败（14:33）

拆分后第一次运行：

```
G2048 import g2048_util.mjava=true
G2048 import g2048_core.mjava=true
G2048 import g2048_store.mjava=true
G2048 import g2048_ui.mjava=true
G2048 import g2048_anim.mjava=true
G2048 init score=468 best=3096 board=...
G2048 TEST ... 8 项全 PASS
JavaErr：
Command not found: u_st( java.lang.String ) : at Line: 60
Called from method: layout
```

- `init()` 第一行 `importAll()`，读档、自检全过 → 说明 `i.d.f` 导入本身成功，
  子模块里的 `java.io` / `android.widget.TextView` import 也正常
- `layout()` 在 `importAll()` **之前**写了 `if (u_st("built").equals("1"))`；
  新 call 的解释器里没有 `u_st` → `Command not found` → 整个方法中断
- 正是探针 `caseDirect` 的失败签名：**导入前调用，catch 不住**
- 修复：`layout()` 改为 `try { importAll(); if (u_st("built")...) ... }`
- 同时按初始方案 B8 拆出第 7 个模块 `g2048_input.mjava`（触摸/按键）

### 修复后复跑（14:43）

```
G2048 import g2048_util.mjava=true
G2048 import g2048_core.mjava=true
G2048 import g2048_store.mjava=true
G2048 import g2048_ui.mjava=true
G2048 import g2048_anim.mjava=true
G2048 import g2048_input.mjava=true
G2048 restore gameover
G2048 layout side=984 cell=208
G2048 newGame board=0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0
G2048 touch dx=66.9375 dy=245.33337 dir=3
G2048 move dir=D add=0 score=0 spawn=3 ...
G2048 anim slide tiles=2
G2048 step2 merged=0 spawn=3
G2048 touch dx=-438.1875 ... dir=0
G2048 move dir=L add=4 score=4 ...
G2048 step2 merged=1 spawn=3
G2048 move queued dir=R → apply pending=1
G2048 key other=113 / 29 / 31
```

- 6 个模块全部 `import=true`；`layout` 正常渲染，无 `Command not found`
- 滑动、合并、动画、输入排队、死局恢复、方向键入口全部正常
- 用户确认：七模块版现象正常
- 结论：`i.d.f` 在真实工程里成立；facade + 6 子模块的拆分可通过

### 打包版失败：`i.d.f` 不存在（14:48）

用户打包安装后启动，进程 `com.demo.game2048` 起来了，但 BeanShell 报：

```
Typed variable declaration : Error in method invocation:
Method f( java.lang.String ) not found in class'xn0'
: at Line: 34 : in file: eval stream : i . d . f ( mods [ k ] )
```

反编译打包 APK `classes.dex`：

```
Class descriptor : 'Lxn0;'   Superclass : 'Lbsh/Interpreter;'
  field  f : Landroid/content/Context;
  method a(String)              -> Object   按名调用无参方法
  method b(String, Object[])    -> Object   按名调用有参方法
  method c(String, Object[])    -> boolean
  method d(String)              -> void     eval 默认 import 头 + 源码
  method e(String)              -> boolean
```

- 开发模式 `i.d.f(String)` 是“按文件名读 .mjava 并 eval”；打包版没有这个方法
- 打包版的 `f` 是 **Context 字段**，不是方法；所以 `i.d.f(...)` 直接 JavaErr
- APK 里没有 `.mjava` 明文（`grep g2048_core.mjava` / `ui_addTile` 均 0 命中），
  工程源码在运行时内部存储里，不能按文件名二次导入
- 结论：**`i.d.f` 是开发模式能力，打包后不可用**
- 正确加载：`i.fn("模块名")`（不带扩展名）把模块加载进当前解释器，之后直接调
- 15:10 探针：

```
FN loaded
CALL b-hello
FN hello-ok
FN add=5
```

- `i.call` 的正确顺序是 `i.call("mjava","模块.方法",Object[])`；
  之前写成 `i.call("模块.方法","mjava")` 返回 null 是**参数顺序错**，不是不能用
- 交付：源码保持 7 模块，直接打包；facade 的 `importAll()` 用 `i.fn`；不合并
- 打包安装后运行正常（用户确认，2026-10-26）

---

## 2026-10-26 i.call 语义探针（com.demo.callprobe）

```
14:28:27.798 P1 call2=hi-from-t2                          ← i.call("mjava","t2.hello")
14:28:27.808 P2 call3=5                                   ← i.call("mjava","t2.add", new Object[]{2,3})
14:28:27.812 P3 call3var=a+b                              ← 参数数组先放变量再传
14:28:27.817 T2-note hello                                ← 目标方法执行了
14:28:27.817 JavaErr: Typed variable declaration : Void initializer. : at Line: 25 …
                  : r = i.call("mjava","t2.note", new Object[]{…})
（P5 / P-done 没有输出 → 报错中止了整个方法）
```

结论：

- `i.call(语言, "模块.方法", Object[] 参数)`：**第一个参数是语言**（DEX 里先 `equals("myu")` 再 `equals("mjava")`），不是“接收返回值的变量”
- 第二个参数必须带模块名，不带点会拼出 `.mjava`
- 第三个参数 `Object[]` 内联、变量传都行
- **返回值跟目标方法走**：目标返回 int/String 时可以 `Object r = i.call(...)` 接住；
  目标是 void 时赋值会报 `Void initializer`，并且**整个方法立即中止**（后续语句不执行）
- 安全写法：一律当语句调用，不接返回值
- 补充：2026-10-26 15:10 的 `i.call("pb.b_hello","mjava")` 返回 null，是参数顺序写反；
  正确顺序是 `i.call("mjava","pb.b_hello")`

产物：`com.demo.callprobe`（`t2.mjava` + `p.mjava`），验证完保留作回归。

---

## 2026-10-26 下拉选择器：String.valueOf(null) 崩在 render

```
14:34:36.025 PICK-render-err=java.lang.NullPointerException: Attempt to get length of null array
    at java.lang.StringFactory.newStringFromChars
    at java.lang.String.valueOf(String.java:2912)
    at bsh.Reflect.invokeStaticMethod
    ...
    at bsh.BSHTypedVariableDeclaration.eval
```

- 弹窗能打开、输入框在，但列表空：`render()` 在第一行就抛了
- 根因 `String sel = String.valueOf(i.sss("pick.sel"))`，首次 `pick.sel` 为 null，
  BeanShell 选中 `String.valueOf(char[])` 重载 → 对 null 取 `length` → NPE
- 修法：加 `str(Object)` 工具（null → ""），render / pickChoose / demo 里所有 `i.sss` 取值都改用 `str()`

---

## 2026-10-26 下拉选择器 v2：单弹窗级联 + 返回 + 行内波纹

```
14:42:28.723 PICK-level 0 n=3
14:42:30.256 PICK-enter 广东省 depth=1 → PICK-level 1 n=3
14:42:34.197 PICK-enter 广州市 depth=2 → PICK-level 2 n=4
14:42:37.085 PICK-pick 广东省 / 广州市 / 海珠区 → PICK-cb-sent demo.onPick
14:42:37.131 DEMO-onPick 广东省 / 广州市 / 海珠区 → DEMO-call pick.setTrigger
14:42:22.061 PICK-back depth=0            ← 返回箭头回退一级
14:42:27.149 PICK-pick 四川省 / 绵阳市 / 涪城区
```

- 单弹窗内完成三级切换，`PICK-enter` / `PICK-back` 与 level 计数一致
- 回调只触发一次（叶子节点），路径以 `父 / 子 / 孙` 形式返回
- 行内波纹：`RippleDrawable(csl, null, mask)` 的第三个参数用圆角 GradientDrawable 遮罩，涟漪被裁到行内（修掉了整圆）
- 图标全部 Canvas 绘制：定位针 / 楼群 / 四宫格 / 返回箭头 / 对勾
- 用户目视确认效果正常

---

## 2026-10-26 B8 代码编辑器：接入 sora-editor AAR（构建侧读数）

目标：编辑器用官方 `io.github.Rosemoe.sora-editor` AAR，走外部库链路；顺带回答
`external-library-guide.md` 里挂着的 ❓「AAR 带资源怎么用」。

### 选版本

```
editor-0.21.1.aar       558,405 B   minSdk 21   classes 326  res 19 个文件
editor-0.23.6.aar       665,203 B   minSdk 21   classes 432  res 21 个文件
language-java-0.21.1    26,159 B    纯代码，无 res，14 个 class
kotlin-stdlib-1.8.10   1,636,559 B
```

- 两个版本都带 `kotlin-stdlib` 运行时依赖；0.23.6 还多一个 `androidx.collection`
- 选 0.21.1：依赖最少（editor + language-java + kotlin-stdlib），语法高亮由官方
  `io.github.rosemoe.sora.langs.java.JavaLanguage` 提供（无参构造）

### 关键发现：AAR 的 R 是 0，且构造期就要资源

```
R.txt 全部 0x0
CodeEditor.<init> → initialize() → ComponentManager → new EditorTextActionWindow(this)
  EditorTextActionWindow.<init>:
    LayoutInflater.from(ctx).inflate(R$layout.text_compose_panel, null)   ← 构造里立刻 inflate
```

所以「不挂资源直接 new」必崩（`Resources$NotFoundException: Resource ID #0x0`），
必须生成真 R 并在运行时让这些 ID 能解析。

### 转换链路（脚本 docs/scripts/build_sora_dex.py）

```
1 aar → classes.jar（剥掉自带 R*.class）
2 aar → res/
3 aapt2 compile --dir res -o compiled.zip
4 aapt2 link -I <framework-res.apk> --manifest <stub> --java gen --package-id 0x80
5 javac --release 11 gen/.../R.java           → r.jar
6 d8 --min-api 21 editor.jar language.jar kotlin-stdlib.jar r.jar → sora.dex
```

踩到的坑（都写进脚本注释）：

| 现象 | 原因 / 修法 |
|---|---|
| `error: invalid package ID 0x7e. Must be in the range 0x7f-0xff.` | aapt2 只接受 ≥0x7f；宿主是 0x7f，所以用 **0x80** |
| `Unsupported source file type` | d8 不接受目录输入，`rclasses` 要先打成 `r.jar` |
| `Unsupported class file major version 69` | JDK 25 默认产 class 69，d8(R8 8.6) 不认；加 `--release 11` |
| 没有 android.jar，aapt2 无法链接 `@android:color/*` | 从设备 pull `/system/framework/framework-res.apk`（API 28，13.6 MB）当 `-I`，可用 |

产物：

```
sora.dex        2,793,852 B   class_defs 1383（含 R$* 8 个类 + CodeEditor + JavaLanguage）
sora-res.apk       18,112 B   包 ID 0x80，独立于宿主 0x7f
```

两份文件放 `工程根/apk/assets/`。

### 运行期加载顺序（待实机验证）

```java
activity.getAssets().addAssetPath(sora-res.apk)   // 反射，hidden API
new DexClassLoader(sora.dex, cacheDir, null, activity.getClassLoader())
new ContextThemeWrapper(activity, Theme_DeviceDefault_Light)   // sora 里强转 ContextThemeWrapper
反射 new CodeEditor(ctx) → FrameLayout.addView
```

### 开发模式装载工程 dex 时的读数（关键）

开发环境：Sora 组件出现但为空，反射调用全部 miss；打包环境同一份 dex 完全正常。

```
ED probe control sizeHit=1 total=42            ← ArrayList 按名字能匹配
ED probe editor getTextHit=0 total=953 head= A A0 A1 A2 A3 A4 B0 B1
ED probe joined len=14130 hasGetText=5395 hasSetTextSizePx=-1
ED probe getMethod getText err NoSuchMethodException: getText []
ED probe sameClass=true byNameMethods=953
ED call-miss getText n=0 cls=io.github.rosemoe.sora.widget.CodeEditor total=953 decl=325

JavaErr：Method setTextSizePx( float ) not found in class'io.github.rosemoe.sora.widget.CodeEditor'
（BeanShell 原生派发同样失败，且 catch(Throwable) 接不住，整个方法中断）
```

- `total=953`、`decl=325`：方法表完整
- 继承自 `View` 的方法名正常（`getName` 里能搜到 `getTextDirection` / `getTextAlignment`）
- **`CodeEditor` 自己声明的 325 个方法名字变成了 `A`、`A0`、`A1`、`A2`…**（首 8 个）
- `getText` 不是精确方法名，`setTextSizePx` 在全部 953 个名字里根本不存在（`hasSetTextSizePx=-1`）
- 设备上的 dex 与宿主机 md5 完全相同（`25096bdf…`），cache 副本也一样 → 不是文件问题，是**运行期符号重命名**
- 打包环境（独立进程）同一份 dex 方法名正常 → 重命名只在开发宿主进程里发生

结论（⚠ 待二轮确认）：开发模式下 iApp 装载工程 dex 会重命名类自有成员；
**类名、参数类型、返回类型不受影响**。因此跨模式可用的调用方式是「按签名找方法」：

```java
// 参数类型 + 返回类型 唯一定位；同名同签名的覆盖方法优先取声明类==实例类
Method m = find(obj, new String[]{"float"}, "void");   // setTextSizePx(float)
```

修法（待跑）：`ed_sora` 全部改为签名查找（`sora_find` / `sora_invoke`）。
`Cursor.getLeftLine()` 与 `getRightLine()` 等签名相同、无法区分，状态栏先只报行数/字符数。

### 根因：宿主 APK 自带混淆版 sora-editor（✅ 已定性）

```
grep -c rosemoe /data/app/com.iapp.app-*/oat/x86_64/base.vdex   → 15

signal 11 (SIGSEGV), fault addr 0x5
#02 io.github.rosemoe.sora.widget.CodeEditor.p3
    /data/app/com.iapp.app-…/oat/x86_64/base.vdex
#08 iappbridge.SoraHost.<init>  /data/…/com.iapp.app/cache/oat/x86_64/sora.vdex
```

- `DexClassLoader` 父加载器 = `activity.getClassLoader()`（宿主）→ 父优先委派 →
  `loadClass("io.github.rosemoe.sora.widget.CodeEditor")` 命中**宿主那份混淆版**
- 之前所有怪现象同源：方法表 953/325 但名字是 `A`/`A0`/`p3`；按签名匹配错位；桥接类 SIGSEGV
- 打包版没有宿主干扰（独立进程、自己的 APK 里没有 sora）→ 同一份 dex 一切正常

修法：`new DexClassLoader(dex, cacheDir, null, null)`，父加载器给 `null`。

### 最终读数（开发环境，✅ 用户确认正常）

```
ED asset dev sora.dex 2795992 / sora-res.apk 18112
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

- 开发环境：编辑器正常显示 Demo.java，Java 高亮，行号与行高正常
- 打包环境：同一份 dex，同样正常（父加载器修复前已验）
- 自检行 `sora-source=ours` 用来确认加载的是官方版而非宿主副本

### 编辑器文件读写闭环（✅ 用户确认）

```
ED init seed=have=2                 ← 首次播种 Demo.java / notes.txt
ED create Hello.java                ← 新建
ED open Demo.java len=253  → open Hello.java len=0 → open notes.txt len=82
ED openDialog n=3                   ← 打开对话框列出 3 个文件
ED save Hello.java ok=true len=115  ← 输入 115 字符后保存
ED open Hello.java len=115          ← 重新打开，内容长度一致 → 写盘往返成立
```

- 文件目录：`activity.getFilesDir()/iap_editor`（应用私有目录，不需要任何权限）
- 新建 / 打开 / 保存三项用户实测通过；写入后重新打开长度一致
- 打包版此前已验证（显示 Demo.java + 高亮），最终版需在 iApp 内重新打包才含桥接类

---

## 2026-10-26 ViewPager 翻页事件探针（✅ 全部触发）

工程：`com.demo.scaffold`（探针页，用完已还原）；适配器 `iappbridge.VpAdapter`
（编译成 `apk/assets/vpadapter.dex`，1948 B）。

事件绑定用「重载兜底」：`vp.onSel` / `vp.onScroll` / `vp.onState` 各写 0/1/2 参重载，
iApp 注入几个参数就命中哪个，日志同时暴露了实际参数个数。

```
VP setup ok count=5 cur=0
VP state 1-arg st_sE=0            ← 静止
VP scroll 2-args st_pN=0 st_vO=null
VP state 1-arg st_sE=1            ← 拖拽
VP state 1-arg st_sE=2            ← 回弹
VP sel 1-arg st_pN=1
VP prev -> 1 / VP next -> 2 / VP jump -> 3
VP sel 1-arg st_pN=3
```

| 事件 | 触发 | 参数读数 |
|---|---|---|
| `onpageselected` | 手势翻页 + `setCurrentItem(n,true)` 都触发 | 1 个：`st_pN` = 页码，准确 |
| `onpagescrolled` | 高频（一次翻页 10+ 次） | 2 个：`st_pN` 正确；第二个 `st_vO` **值为 null**（偏移量取不到） |
| `onpagescrollstatechanged` | 每次滚动成组 | 1 个：`st_sE` = 0/1/2 |

- 顺序（按时间升序）：`state 1 → state 2 → sel → state 0`
- 第二个参数不是「被丢掉」（被丢掉会退化成 1 参重载），而是**传了 null**
- 适配器必须是编译类：BeanShell 不能继承 `PagerAdapter`
- `DexClassLoader` 父加载器要给宿主（`androidx.viewpager.*` 在宿主里），
  与 sora 那次「父加载器给 null」相反，取决于依赖是否在宿主内

---

## 2026-10-26 onoffsetchanged 探针（✅ 触发，参数可用）

工程：`com.demo.scaffold`（探针页，用完已还原）
结构：`LinearLayout` → `CoordinatorLayout` → `AppBarLayout`(绑事件) + `NestedScrollView`(40 行内容)

```
AB setup ok appbarH=0 total=0 nsvChild=1
AB offset 1-arg st_vO=0
AB offset 1-arg st_vO=-12 … -360        ← 共 453 条
AB collapse -> top=0 range=360 / top=-360 range=360
AB expand   -> top=-360
AB top -> scrollY=0
```

- `onoffsetchanged` 在手势滚动和 `setExpanded(false/true, true)` 下都触发
- 参数 1 个：`st_vO` = 真实偏移量（px，负值），范围 `0 → -360`
  （标题条 120dp × density 3 = 360px，与 `getTotalScrollRange()` 一致）
- 从未出现 `0-args` 重载 → 参数不会被丢（与 pager 的 `st_vO=null` 不同）
- 结构要点：子视图要用 `AppBarLayout.LayoutParams` + `setScrollFlags(SCROLL|ENTER_ALWAYS)`；
  滚动子视图要设 `AppBarLayout.ScrollingViewBehavior`，否则内容压住标题条

剩余 ❓（缺条件，已写进 events-guide）：
- `onoptionsitemselected`：需要 ActionBar/Toolbar 上真的有菜单项
- `onpicturecallback`：模拟器无摄像头，需真机或虚拟摄像头

---

## 2026-10-26 黑金卡 3D 倾斜 + 金属反光（`com.demo.card3d`，✅ 效果验收）

一屏 Demo：黑金抽卡卡面，手指拖动产生小幅 3D 倾斜，表面有圆形白光斑。
最终形态是 **6 个探针页**共用 `card.mjava`：`mian.iyu` 与 `card_b/c/d/e/f.iyu`，
每页只写一行 `call(null, "mjava", "card.page", "<mode>")`，光斑差异全在 `lightMode(mode)` 里。

### 原始读数（logcat，tag `ygs`）

```
CARD page mode=c
CARD init-start
CARD init-done ms=276 w=900 h=1260
CARD dump=/storage/emulated/0/Android/data/com.iapp.app/files/card3d-face.png
CARD light mode=c
CARD light-done children=3
CARD bind-start
CARD bind-done
CARD down
CARD up rx=6.662804 ry=8.0
CARD up rx=-8.0 ry=-6.2191877
CARD page mode=d ... CARD light-done children=3
CARD page mode=e ... CARD light-done children=4
CARD page mode=f ... CARD light-done children=3
```

- `init-done ms` 四次读数：276 / 262 / 260 / 261 → 900×1260 卡面现画稳定在 **260~280 ms**
- 全部页面**零 `CARD *-err`**（init / light / bind / touch / spring / moveLight 都没报）
- 倾斜角精确停在 `±8.0`（上限生效）

### 屏幕现象

- 卡面居中、黑金、喷砂细颗粒；上 1/3 处一团圆形柔边白光斑
- 拖动时朝手指位移方向倾斜，最大 8°，松手回弹，按下不放大
- 光斑随倾斜滑动；双光模式（e）多一团右下的副光
- 6 个页面参数用户逐一确认「效果都没问题」

### 一致 / 推翻 / 未知

| 断言 | 判定 | 依据 |
|---|---|---|
| 普通 View 上 `setRotationX/Y` + `setCameraDistance` 可做卡片 3D 倾斜 | ✅ | 实拍 + 无异常 |
| 圆角 `GradientDrawable` 背景 + `setClipToOutline(true)` 能裁掉溢出的光斑子 View | ✅ | 光斑在圆角处被裁 |
| `View.setTag(int[])` 跨 call 存状态，`(int[]) getTag()` 可转回 | ✅ | 无 `moveLight-err`，光斑跟手 |
| `View.animate()`（ViewPropertyAnimator）链式调用 + `.cancel()` 可用 | ✅ | 回弹正常，无 `spring-err` |
| 多个 `.iyu` 可各自作入口；`call(null,"mjava","mod.method","str")` 传字符串 | ✅ | card_b~f 依次跑通 |
| BeanShell 里 `Canvas` 现画 900×1260 卡面（260 次 drawLine + 160² 噪声）≈ 260~280 ms | ✅ | 4 次读数 |
| `getExternalFilesDir(null)` + `Bitmap.compress(PNG)` 可 dump 位图回宿主机核对 | ✅ | 路径 `/sdcard/Android/data/com.iapp.app/files/card3d-face.png` |
| `BlurMaskFilter` 软边 / `PorterDuffXfermode` 彩虹蒙版在 mjava 里可用 | ❓ | 写过但方案被否，**没上机跑** |

### 踩坑

1. **绝对位置驱动倾斜**（按下点离中心多远就转多少）→ 用户「一按下就大幅倾斜」。
   改为**相对按下点的位移**驱动，按下瞬间角度为 0。
2. **按下放大 1.03** → 用户「卡片变大了」，删掉。
3. **`GradientDrawable` 三色径向渐变有明显色阶断层**（肉眼可见同心环）。
   改 `RadialGradient` 9 段 + 256² 画完放大到目标尺寸，断层消失。
4. **同一渐变在矩形 View 里是椭圆、正方形里才是圆**；要圆斑就给正方形 View。
5. **需求误读代价最大**：把「白光打在金属上」依次做成了灯泡光晕 → 直光带 → 柔光箱长条 → 彩虹镭射，
   全部被否；正解是**圆形柔边白光斑 + 上 1/3 + 面积大**。视觉类需求先出静帧预览再上机。
6. 卡面绘制走"低分辨率画完再放大"能一次拿到朦胧感；但分辨率过低（120×150）会糊成一片，
   200×250 是清晰与柔和的平衡点。

### 产物

- 工程：`android-sync/ProjectApp/com.demo.card3d/`（可作示例保留）
- 卡面 dump：`docs/artifacts/card3d-face-v5.png`（900×1260）
- 设备截图：`docs/artifacts/card3d-screen-v5.png`
- 六种打光的宿主机合成预览：`docs/artifacts/mode-a.png` ~ `mode-f.png`

---

## 2026-10-26 Android 15 实机：动态加载的 dex 必须只读（用户实测 + 官方文档核实）

现象（用户在 Android 15 实机运行代码编辑器）：`DexClassLoader` 加载
`/data/user/0/com.iapp.app/cache/sora.dex` 被系统拒绝。

官方文档核实（`developer.android.google.cn/about/versions/14/behavior-changes-14`
「Safer dynamic code loading」原文）：

> If your app targets Android 14 (API level 34) or higher and uses Dynamic Code
> Loading (DCL), all dynamically-loaded files must be marked as read-only.
> Otherwise, the system throws an exception.
>
> …use the following approach to set the dynamically-loaded file … as read-only
> **as soon as the file is opened and before any content is written**:
> `File jar = new File(...); try (FileOutputStream os = new FileOutputStream(jar)) { jar.setReadOnly(); … }`
>
> To prevent exceptions … for existing dynamically-loaded files, we recommend
> **deleting and recreating** the files before …

| 事实 | 级别 |
|---|---|
| targetSdk ≥ 34 时，DCL 加载的文件必须只读，否则抛异常 | ✅ 官方文档 |
| iApp 打包产物 targetSdk = 36 → Android 14/15 设备上必然命中 | ✅（见 B6 读数） |
| Android 15 实机上 `getCacheDir()` 里的可写 dex 被拒 | ✅ 用户实测（本会话无 Android 15 设备，未复现） |
| 「换 `getCodeCacheDir()` 就没事」 | ❌ 官方未提；限制针对文件可写，不针对目录，不作为方案 |
| 具体异常文案（如 `Writable dex file '…' is not allowed`） | ⚠ 未在本机复现 |

代码修改：`com.demo.editor/src/ed_sora.mjava` 增加 `sora_write(InputStream, File)`：

```
已存在 → setWritable(true) + delete()
打开 FileOutputStream → setReadOnly() → 写 → 关闭 → setReadOnly()
```

`sora_copy()`（打包模式 assets→cache）与 `sora_local()`（开发模式工程目录→cache）都改走它。
Android 9 上行为不变（多两次权限调用）。

---

## 2026-10-26 国内网络：抓官方文档与依赖的连通性读数

### 抓取工具

| 方式 | 目标 | 结果 |
|---|---|---|
| WebFetch | `developer.android.com` | `Unable to verify if domain … is safe to fetch` |
| WebFetch | `developer.android.google.cn` | 同上 → 抓取服务侧就被挡，与域名无关 |
| curl (https) | `developer.android.google.cn` | exit 35（SSL connect error），`000` |
| curl (http) | `developer.android.google.cn` | `301`（站点可达，要 https） |
| curl **-k** (https) | `developer.android.google.cn/…?hl=en` | **200，303,141 B** ✅ |
| curl | `aospxref.com` | `000` |
| curl | `juejin.cn` | `200` |

### 依赖镜像

| 目标 | 地址 | 结果 |
|---|---|---|
| sora-editor（Maven Central） | `maven.aliyun.com/repository/central/…` | 200 ✅ |
| androidx.viewpager（Google Maven） | `maven.aliyun.com/repository/central/…` | **404 + HTML 提示页**（不在 central） |
| 同上 | `maven.aliyun.com/repository/google/…` | 200，53,513 B ✅ |
| 同上（备用） | `mirrors.cloud.tencent.com/nexus/repository/maven-public/…` | 200，53,513 B ✅ |
| repo1.maven.org | — | `000` |
| dl.google.com | — | `000` |
| Android SDK platform-28 | `mirrors.cloud.tencent.com/AndroidSDK/platform-28_r06.zip` | 200，75,565,084 B ✅（内含 `android-9/android.jar`） |

适用范围：以上读数全部来自 **Claude Code CLI**（内置 WebFetch 不可用、Bash 里的 curl 可用）。
其他智能体工具的网络出口与内置抓取工具不同，结论不一定成立，换工具时重新探测。

结论：本环境下 WebFetch 对 Google 系域名不可用；`curl -k` 落盘 + 阿里云/腾讯镜像是稳定路径。
已沉淀到 SKILL 的 `references/network-and-mirrors.md`，离线解析脚本见 `docs/scripts/fetch_text.py`。

---

## 2026-10-26 E0 双模拟器与 adb 端口冲突

**探针**：`adb devices -l` / `adb connect` / 两套 `ldconsole.exe list2|adb` / `VBoxManage showvminfo --machinereadable` / `adb shell`

**两套独立安装同时在跑**

| 项 | LDPlayer9 | LDPlayer14 |
|---|---|---|
| 引擎版本 | `dnplayer v9.5.42.0` | `dnplayer v14.0.32.1` |
| 安装目录 | `E:\Program Files\leidian\LDPlayer9` | `C:\leidian\LDPlayer14` |
| 实例名 | `iApp测试`（GBK 乱码显示） | `安卓14验证` |
| 分辨率 | 1080×1920 / 480dpi | 720×1280 / 320dpi |
| Android | 9 / API 28 | 14 / API 34 |
| 伪装型号 | 25060RK16C（REDMI） | 25102RKBEC（REDMI） |
| 共享 Pictures | `E:\...\android-sync` | `C:\Users\hello\Documents\leidian14\Pictures` |
| root 配置 | `rootMode: true` | `rootMode: true` |

VM 标识（两套实例都叫 `leidian0`，必须用 UUID 区分）：

- LD9：`20160302-aaaa-aaaa-012e-000000000000`，box 启动 19:19:10
- LD14：`20160302-aaaa-aaaa-7046-000000000000`，box 启动 19:20:29

**端口冲突（关键）**

```
Forwarding(0)="adb,tcp,,5555,,5555"   # 两台都是
Forwarding(1)="gdb,tcp,,2222,,2222"   # 两台都是
netstat: 0.0.0.0:5555 被两个 Ld9BoxHeadless（PID 8616/3924）同时 LISTEN
```

读数时间线：

```
（LD14 启动前）adb shell → release 9 / sdk 28 / model 25060RK16C      ← LD9
adb connect 127.0.0.1:5555 → devices 出现 127.0.0.1:5555
  product:25102RKBEC model:25102RKBEC device:unicorn                  ← 落到 LD14
（此时）emulator-5554 也变成 25102RKBEC → LD9 的 LDPlayer9 自带 ldconsole adb 同样读到 14/34/25102RKBEC
```

结论：5555 归**后启动**那台（本次 LD14）；此后 `emulator-5554` 这个名字会**静默指向 Android 14**，改文件/投递会打到错的设备。

**Android 14 root 读数** ✅

```
su -c id                     → uid=0(root) gid=0(root) context=u:r:su:s0   （adbd 还是 shell 时）
adb root                     → service.adb.root=1；恢复后 shell id → uid=0
adb unroot                   → shell id → uid=2000(shell)；su -c id 仍 → uid=0
getprop ro.build.type        → user
getprop ro.secure            → 1
getprop ro.debuggable        → 1
getprop ro.build.tags        → release-keys
ls -l /system/xbin/su        → -rwsr-x--x root shell 60368   （/system/bin/su -> ../xbin/su）
```

**Android 14 其他读数**

```
com.iapp.app                 已安装：versionName 5.0.1013 / versionCode 127 / targetSdk 37 / minSdk 21
/storage/emulated/0/iApp     不存在
/sdcard/Pictures             vboxsf → C:\Users\hello\Documents\leidian14\Pictures
/sdcard/Pictures/ProjectApp  不存在（仅 cache/ data/ 芙郇肢.xml）
```

性质标注：双份 5555 转发与「后启动者占用」✅实测；`emulator-5554` 名称漂移 ✅实测；Android 14 su 可用 ✅实测。

## 2026-10-26 Android 14 永久 root 授权（`com.iapp.app`，Koush/CM Superuser）

设备：`emulator-5556`（LDPlayer14，14 / API 34，model 25102RKBEC），SELinux = Permissive。

**机制读数**

```
/system/xbin/su                 -rwsr-x--x root shell 60368   md5 c45514d3f6bc2364ce5a2ad5c55682f1
init.svc.su_daemon              running（root，pid 228）
proc/net/unix                   @SUPERUSER（daemon 监听）
Settings APK                    com.android.settings.cyanogenmod.superuser.{RequestActivity,SuReceiver,NotifyActivity}
                                + com.koushikdutta.superuser.db.SuDatabaseHelper（v6）
su 二进制字符串                 select policy, until, command from uid_policy where uid=%d
                                policy ∈ {allow, interactive, deny}
getprop ro.cm.version           空 → su 的 access_disabled() 分支整体跳过
getprop persist.sys.root_access 不存在（且因上一条不生效）
```

运行时实际 DB 路径（**不是**二进制里的 `/data/data/...` 字符串）：

```
/data/user_de/0/com.android.settings/databases/su.sqlite
```

**基线（授权前，uid 10072 发请求）**

```
E/su: sqlite3 open /data/user_de/0/com.android.settings/databases/su.sqlite failure: 14
D/su: /dev/com.android.settings/.socket2521
D/su: waiting for user
（约 25s 后）
D/su: 10072 /system/bin/sh executing 0 id using binary /system/bin/sh : sh -c id
```

即：无策略行 → interactive → 拉起 RequestActivity 等用户。

**写入**

- 建库 `PRAGMA user_version=6`，schema 与 Settings 内 `SuDatabaseHelper` v6 一致
- 行：`uid=10072, command='', desired_uid=0, policy='allow', until=0`
  - `until=0` 在 `db.c` 里含义是「永不过期」（`until == 0 || until > time(NULL)`）
  - `command=''` 匹配该 uid 的所有命令
- `chown system:system`，DB 660 / 目录 771，`restorecon`

**授权后（同一 uid 10072 复测）**

```
$ time su 10072 /system/bin/sh -c '/system/xbin/su -c id'
uid=0(root) ...
real 0m0.273s

D/su: starting daemon client 10072 0
D/su: remote uid: 10072
D/su: db allowed
D/su: 10072 /system/xbin/su executing 0 id using binary /system/bin/sh : sh -c id
```

判定：✅ 永久策略命中（`db allowed`，无 `waiting for user`）。

边界：

- ⚠ 未做整机重启复测；DB 与 `persist` 均在 `/data`，按设计重启保留。
- ⚠ 未用真实 app 进程复测，用的是同 uid 的 `su` 派生进程；daemon 只按客户端上报的 `from.uid` 判定，且 SELinux 为 Permissive，差异风险低。
- ⚠ 重装 iApp 后 uid 可能变化，需要重写该行。

产物：`docs/artifacts/root/`（su 二进制、Koush 源码快照、授权脚本）。

## 2026-10-26 Android 14：iApp 工程目录链接到 Pictures（宿主机同步）

目标：

```
/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp
  -> /storage/emulated/0/Pictures/ProjectApp
```

**存储层读数**

```
mount | grep emulated
  /dev/fuse on /storage/emulated type fuse (rw,lazytime,nosuid,nodev,noexec,noatime,user_id=0,group_id=0,allow_other)
  Pictures on /data/media/0/Pictures type vboxsf (rw,...,uid=1023,gid=1023,dmode=0777,fmode=0777)
  Pictures on /mnt/pass_through/0/emulated/0/Pictures type vboxsf (...)
ls -ld /storage/emulated/0        0770 media_rw media_rw  u:object_r:fuse:s0
ls -ld /storage/emulated/0/Pictures  0777 media_rw media_rw  u:object_r:fuse:s0
readlink /proc/1/ns/mnt           mnt:[4026531841]
readlink /proc/2865/ns/mnt        mnt:[4026532215]      ← iApp 独立 mount namespace
/proc/2865/attr/current           u:r:untrusted_app:s0:c72,c256,c512,c768
/proc/2865/status                 Uid/Gid 10072；Groups 1079 3003 9997 20072 50072
```

**符号链接可行性**

```
（root）ln -s /storage/emulated/0/Pictures/ProjectApp .../files/iApp/ProjectApp
  → rc=0；readlink 正常
（root）echo probe > .../ProjectApp/__link_probe.txt
  → /storage/emulated/0/Pictures/ProjectApp/__link_probe.txt 出现
  → 宿主 E:\...\android-sync\ProjectApp\__link_probe.txt 回读一致；删除同步
（Pictures 内）ln -s ...
  → ln: Function not implemented        ← vboxsf 不支持 symlink
```

**非 app 进程访问 Android/data 被拒（不是权限问题）**

```
su 10072 sh -c 'ls /storage/emulated/0/Android/data/com.iapp.app/files/iApp'
  → Permission denied
```

AOSP `FuseDaemon.cpp` `is_app_accessible_path()`：

```
if (!fuse->bpf && StartsWith(path, PRIMARY_VOLUME_PREFIX)) {
    // Emulated storage bind-mounts app-private data directories...
    LOG(WARNING) << "Rejected access to app-private dir on FUSE: " << path ...
    return false;
}
```

即 `Android/data/<pkg>` 在该 app 的 mount namespace 里由 bind mount 提供，FUSE 侧一律拒绝；所以普通 su 派生进程测不了，必须用真实 app 进程。

**iApp 侧**

- `MANAGE_EXTERNAL_STORAGE` 原为 `default`，已 `appops set com.iapp.app MANAGE_EXTERNAL_STORAGE allow`
- 用户实机操作：iApp 内成功加载并编辑 `Pictures` 中的文件（2026-10-26）
- 最终形态：`.../files/iApp/ProjectApp -> /storage/emulated/0/Pictures/ProjectApp`（owner `u0_a72:ext_data_rw`）

**宿主映射（修正旧记录）**

```
C:\leidian\LDPlayer14\vms\config\leidian1.config
  "statusSettings.sharedPictures": "E:\\workspaces\\2026-10-24-iapp-dev-ai-space\\android-sync"
```

此前 `docs/runtime-env.md` 记的 `C:\Users\hello\Documents\leidian14\Pictures` 已过时；LD14 实际与 LD9 共用 `android-sync`。

**边界**

- `Android/data` 随卸载/清除数据消失，链接需重建；重装 iApp 后 UID、appop、链接都可能变。
- vboxsf 不支持符号链接，所以链接只能放在设备侧（ext4/FUSE 路径），不能反向建在 `Pictures` 里。
- `nsenter`（toybox 0.8.9-android）有 bug：`-t <pid>` 恒解析成 0（`/proc/0/ns/mnt`），无法进 app namespace。

## 2026-10-26 E1 实例改名分开 adb 端口（用户实测 + 本机复测）

背景见 E0：两套独立安装各自唯一的实例都叫 `leidian0`，NAT 规则都是宿主 5555。

做法（用户 2026-10-26 实测有效，环境 = 安卓 9 一台 + 安卓 14 一台）：

1. 关 LD14：`ldconsole.exe quit --index 0`
2. `vms\leidian0` → `vms\leidian1`；`vms\config\leidian0.config` → `leidian1.config`
3. `ldconsole.exe launch --index 1`

**本机复测读数**

```
VBoxManage list vms
  "leidian0" {20160302-aaaa-aaaa-7046-000000000000}   ← LD14 空实例（0 字节）
  "leidian0" {20160302-aaaa-aaaa-012e-000000000000}   ← LD9
  "leidian1" {20160302-aaaa-aaaa-7046-000000000001}   ← LD14 实机（766M）

showvminfo ...7046-000000000001 --machinereadable
  Forwarding(0)="adb,tcp,,5557,,5555"
  Forwarding(1)="gdb,tcp,,2222,,2222"

netstat -ano
  0.0.0.0:5555  LISTENING  8664      （LD9）
  0.0.0.0:5557  LISTENING  6108      （LD14）
  ← 各只有一个监听，不再抢 5555

adb devices -l
  emulator-5554  25060RK16C  sdk 28  ← LD9 / 5555
  emulator-5556  25102RKBEC  sdk 34  ← LD14 / 5557
```

**Android 14 重启后状态仍在**

```
readlink .../files/iApp/ProjectApp   → /storage/emulated/0/Pictures/ProjectApp
appops get com.iapp.app MANAGE_EXTERNAL_STORAGE → allow
sqlite3 .../su.sqlite "select uid,policy,until from uid_policy"
  10072|allow|0        ← com.iapp.app
  10071|allow|0        ← bin.mt.plus（非本轮操作，应是用户在 UI 里授权的）
```

**注意**

- 改名后雷电 GUI 自动新建了一个空 `leidian0`（0 字节）；不要启动它，稳定后可删。
- `emulator-5556` 是 adb 的串口名，对应宿主 5557；建议统一用 `127.0.0.1:5557` 或先 `getprop` 核对。
- 回滚：`quit --index 1` → `ren leidian1 leidian0` → `ren leidian1.config leidian0.config`，数据盘不动。

## 2026-10-26 课堂黑板 BB-P1（P1 刷新 / P2 触摸 / P3 布局 / P4 状态）

工程 `com.demo.blackboard`，LD9 / API 28，探针源码归档 `android-sync/iapp-demo/blackboard-p1/`。
用户操作：横屏点 P1 → 转竖屏 → 点 P1 → 点触摸区（闪退）。

### P3 布局时机 ✅

```
BB P3 stage=loading w=0 h=0
BB P3 stage=loadingComplete w=1080 h=1848
BB P3 stage=post root=1080x1848 row10=1080x262
BB P3 layout-change 0,72,1920,1080 old=0,72,1920,1080
BB P3 layout-change 0,72,1080,1920 old=0,72,1920,1080
```

- `loading` 里宽高为 0；`loadingComplete` 已拿到真实尺寸。
- `addOnLayoutChangeListener` 可用，旋转会触发。
- **旋转后页面重建并重跑 `loading`**（21:08:34 再次出现 `stage=loading w=0 h=0`），板书状态必须从文件恢复。

### P4 状态载体 ✅

```
BB P4 stage=init store-ok arr/list/tag-put var=set-in-init
BB P4 stage=ready tag=v-init arr=7,8,9 list=size=2 first=a var=init-default
BB P4 stage=click tag=v-init arr=7,8,9 list=size=2 first=a var=init-default
```

- `View.setTag(HashMap)` 跨 call 可取回；HashMap 里装了 Bitmap / Canvas / Paint，P1 后续取出来继续画，正常。
- `i.sss` 能存 `int[]` 与 `ArrayList`，跨 call 不变。
- 模块级变量每次 call 重置（`set-in-init` → `init-default`）。

### P1 刷新耗时（API 28）

第一次点击（含预热）：

```
BB P1 row=0 firstUs=1718 loopUs=11628 avgUs=116   invalidate
BB P1 row=1 firstUs=2064 loopUs=4581  avgUs=45    setImageBitmap
BB P1 row=2 firstUs=2538 loopUs=3447  avgUs=34    null+set
BB P1 row=3 firstUs=12   loopUs=3009  avgUs=30    software+invalidate
```

第二次点击（稳定）：

```
BB P1 row=0 firstUs=1551 loopUs=2847 avgUs=28
BB P1 row=1 firstUs=1627 loopUs=2665 avgUs=26
BB P1 row=2 firstUs=1336 loopUs=2880 avgUs=28
BB P1 row=3 firstUs=14   loopUs=2608 avgUs=26
```

- 四种写法单次刷新都在 26~28µs，成本差异可以忽略。
- **四种写法能否真正上屏更新，用户尚未目视确认**（待补）。

### P2 触摸：首轮崩溃 ❌

```
E/AndroidRuntime( 3039): FATAL EXCEPTION: main
E/AndroidRuntime( 3039): Process: com.iapp.app, PID: 3039
E/AndroidRuntime( 3039): java.lang.reflect.UndeclaredThrowableException
E/AndroidRuntime( 3039): 	at $Proxy3.onTouch(Unknown Source)
E/AndroidRuntime( 3039): Caused by: Typed variable declaration :
  Error in method invocation: Method getHistorySize( int ) not found in class'android.view.MotionEvent'
  : at Line: 311 : ... e .getHistorySize ( idx )
W/System.err( 3039): java.lang.Exception: call killProcess callstack! pid=3039
```

- `MotionEvent.getHistorySize(int)` 在 BeanShell 里找不到；`catch (Throwable)` 接不住，异常穿透匿名接口代理，iApp 直接 `killProcess`。
- 崩溃行之前已成功解析并执行：`getActionMasked()`、`getActionCount()`（实际用了 `getPointerCount()`）、`getActionIndex()`、`getPointerId(int)`、`findPointerIndex(int)`、`getX(int)`、`getY(int)`——说明这些 API 本身可用。
- 修复：改用无参 `getHistorySize()`；历史点坐标本轮先不取，避免再踩 `(int,int)` 重载。

### P2 复跑（修复 `getHistorySize` 后）✅

用户操作：在触摸区单指划动数次。

```
BB P2 raw=0 masked=0 cnt=1 ai=0 id=0 idx=0 x=195 y=424 hist=0
BB P2 raw=2 masked=2 cnt=1 ai=0 id=0 idx=0 x=182 y=444 hist=2
BB P2 raw=1 masked=1 cnt=1 ai=0 id=0 idx=0 x=168 y=488 hist=0
...
BB P2 raw=2 masked=2 cnt=1 ai=0 id=0 idx=0 x=1084 y=317 hist=2
```

- 不再崩溃；`getActionMasked()` 正确返回 DOWN=0 / UP=1 / MOVE=2。
- `getPointerCount()`、`getActionIndex()`、`getPointerId(int)`、`findPointerIndex(int)`、`getX(int)`、`getY(int)` 全部可用。
- `getHistorySize()`（无参）可用；每次 MOVE 带 2~3 个历史点。LD9 左键划动的 MOVE 事件约 160ms 一批。
- 用户目视：底部状态文字随触摸变化，触摸区出现绿色点；**快速划动时点之间有空隙**——探针只在采样点画圆点，主实现改为连接线段。
- 触摸区的位图是「`setImageBitmap` 一次 → 之后改内容 + `invalidate()`」，绿点能上屏，**证明 `invalidate()` 刷新可变 Bitmap 可行**（API 28）。

### 本轮结论

- ✅ 布局时机、状态载体、四种刷新耗时；`invalidate()` 上屏刷新可行。
- ✅ 多点触控相关 API（单指路径）可用；带 pointerIndex 的历史点重载会杀进程（已回填 `pitfalls.md` 8.1、`events-guide.md`）。
- 待补：多点（双指）实机语义；P6 导出；P8 性能。

## 2026-10-26 E2 其他模拟器共享目录资料（MuMu 12 / BlueStacks 5）

用途：给 SKILL 的模拟器环境案例补非雷电的菜单/路径。本机**未安装**这两款，结论级别为 ⚠（官方文档 + 社区资料，未实机）。

**MuMu 模拟器 12**

官方帮助（2026-10-26 抓取，HTML 与提取文本在 `docs/artifacts/emulator-docs/`）：

- https://mumu.163.com/help/20230711/35047_1098046.html（共享文件夹功能教程）
- https://mumu.163.com/help/20240320/35047_1144336.html（自定义路径）

读数：

```
菜单：右上角菜单 → 更多工具 → 共享文件夹
      （打开电脑端 / 打开安卓端 / 更改共享文件夹路径）
自定义路径需 MuMu ≥ 3.8.9；改完需重启模拟器生效
宿主默认：C:\Users\<用户名>\Documents\MuMu共享文件夹
          （官方原文写作 C:\Users\Documents\MuMu共享文件夹，省略了用户名）
安卓端：/sdcard/MuMu12Shared 或 /sdcard/MuMuShared
        （原文：\sdcard\$MuMu12Shared / \mnt\shared\MuMuShared）
```

**BlueStacks 5**

- 官方媒体导入：https://support.bluestacks.com/hc/en-us/articles/4405395140621-How-to-upload-and-share-media-files-on-BlueStacks-5
- 官方“修改安装位置”文章含 `<SharedFolder>` 配置：https://support.bluestacks.com/hc/en-us/articles/7225681713037
- 本机访问 support.bluestacks.com 直连 403，WebFetch 被域名策略拦截；以下为搜索结果转述，未核对原文

读数（⚠）：

```
实例配置 .bstk（如 ...\Engine\Nougat32\Nougat32.bstk）：
  <SharedFolder name="BstSharedFolder"
     hostPath="C:\ProgramData\BlueStacks_nxt\Engine\UserData\SharedFolder"
     writable="true" autoMount="false"/>
改 hostPath 后删 .bstk-prev，重启；多实例（Nougat32/64、Pie64）各改各的
安卓端：社区常见 /mnt/windows/BstSharedFolder
        旧版/其他写法 /sdcard/windows/BstSharedFolder、/sdcard/bstfolder/、/sdcard/BlueStacksShared/
        以 adb shell ls 实测为准
```

结论：MuMu 菜单与默认路径 ✅ 官方文档；BlueStacks 路径 ⚠ 版本差异大，需实机核对。

---

## 2026-10-27 TIL ppt 父控件探针（com.demo.tilprobe）

环境：iApp 5.0.1013 / **Android 14（API 34，emulator-5556）**，不是 CLAUDE.md 里记的 API 28 那台。

探针矩阵（同一页）：A 短名 TIL + 短名 EditText；B 全类名 TIL + 短名 EditText；C 短名 TIL + 全类名 TIET；E 全类名 TIL + 全类名 TIET；D mjava 动态创建基线。

**原始读数（09:48:15~16，logcat tag ygs / TILP）**

```
TILP A-short id=10 cls=com.google.android.material.textfield.TextInputLayout hash=111293832 attached=true parent=android.widget.LinearLayout children=1
TILP A-short mode=2 hint=A-短名-TIL
TILP A-short addChild-ok children=2
TILP B-full id=20 cls=com.google.android.material.textfield.TextInputLayout attached=true children=1
TILP C-short-tieet id=30 cls=com.google.android.material.textfield.TextInputLayout attached=true children=1
TILP E-full-full id=50 cls=com.google.android.material.textfield.TextInputLayout attached=true children=1
TILP D created children=1 mode=2
```

视图树节选：

```
TextInputLayout id=10 n=2
 └ FrameLayout n=3
    ├ EditText id=11 ctx=com.iapp.app.run.mian
    ├ StartCompoundLayout n=2
    └ EndCompoundLayout n=3
```

- 短名 `TextInputLayout` 与全类名**都**解析为 `com.google.android.material.textfield.TextInputLayout`（"短名指向 support 包"的怀疑被推翻）
- ppt 建的四个 TIL 全部 `attached=true`、hash 与树一致、`addView` 后 children 1→2 → **本机不是影子实例**（与 `cases/11` 的 API 28 结论冲突，疑为版本差异 ⚠）
- FrameLayout 内含 `StartCompoundLayout`/`EndCompoundLayout` → 是 TIL 自带 `inputFrame`，**不是 iApp 套的**；`cases/11` 的归因需修正
- 子控件 ctx 全为 `com.iapp.app.run.mian`（activity）；动态 D 用 `til.getContext()`，外观差异待屏幕确认
- 页面上的「X」是探针里影子测试加的 TextView，不是控件本身

**屏幕现象（用户回报）**：D 动态 TIL 为正常 M3；各组件之间出现单行 X（探针产物）。

**09:50:26 第二轮（已去掉 X 与树 dump）**

```
TILP A-short id=10 cls=…TextInputLayout hash=215373446 attached=true children=1
TILP B-full id=20 cls=…TextInputLayout hash=121887559 attached=true children=1
TILP C-short-tieet id=30 cls=…TextInputLayout hash=77475700 attached=true children=1
TILP E-full-full id=50 cls=…TextInputLayout hash=25672861 attached=true children=1
TILP D created children=1 mode=2
```

屏幕现象（用户回报）：**A/B/C/E 看起来都是普通 EditText，只有 D 是 Material 3**。

判定：ppt 建 TIL 的实例是真的（attached、hash 与树一致、可 addView），但子控件固定用 activity Context，拿不到 `til.getContext()` 的 Material 主题覆盖 → 外观退化为原生。**M3 外观只能 mjava 动态创建**。短名/全类名、子控件短名/全类名四种组合结果一致。

**本轮顺带实测的失败签名**

```
[09:39:31] MJavaErr: Command not found: importAll() : at Line: 1
            ← importAll() 写在文件顶层；它只能写在方法体内
[09:45:57] MJavaErr: Class: View not found in namespace : at Line: 51
            ← 缺少 import；删 importAll() 不能连带删 import
```

**投递**：工程打开期间，宿主机改 `src/*.iyu|*.mjava`，设备端读到旧缓存（md5 不一致）；关闭工程后自动刷新对齐。本轮全程未 push。

---

## 2026-10-27 custom.iyu 自定义控件边界（com.demo.m3showcase，API 34）

页面：pp t 里用**全类名**声明 13 个 Material 控件（`mian.iyu` 的 mjava 版保留不动）。读数 tag `CUST`（10:11:15）。

```
CUST btn id=100 cls=…MaterialButton att=true
CUST card id=110 cls=…MaterialCardView att=true n=1
CUST til-outline id=120 cls=…TextInputLayout att=true n=1
CUST til-outline mode=2 hint=TIL-全类名-outline
CUST tiet-outline id=121 cls=…TextInputEditText att=true
CUST til-filled id=130 cls=…TextInputLayout att=true n=1
CUST til-filled mode=2 hint=TIL-全类名-filled
CUST checkbox id=140 cls=…MaterialCheckBox att=true
CUST radiogroup id=141 cls=android.widget.RadioGroup att=true n=2
CUST switch id=150 cls=…SwitchMaterial att=true
CUST chip id=160 cls=…Chip att=true
CUST chip checkable=false checked=false
CUST slider id=170 cls=…Slider att=true / value=0.0
CUST linear id=180 / circular id=181 / fab id=190 att=true
CUST toggle id=200 cls=…MaterialButtonToggleGroup att=true n=2
```

- 全类名声明全部渲染成功、`attached=true`；`MaterialCardView` / `MaterialButtonToggleGroup` 用 `did` 挂子控件成功
- `st_setChecked=true`（Chip）**无效**：`checkable=false checked=false` → `st_` 桥不认布尔字符串
- 两个 TIL 都 `mode=2`（`st_setBoxBackgroundMode` 未设的 130 也是 2 → 默认即 outline），但**盒子没画**；hint 已浮起
- 子控件 `TextInputEditText` ctx=`com.iapp.app.run.mian`（activity），焦点态显示原生粉色下划线
- 组件 ctx 分组：MaterialButton / Chip / FAB / TIL = `ContextThemeWrapper`（组件自身主题覆盖）；MaterialCardView / CheckBox / Radio / Switch / Slider / Progress / ToggleGroup = `com.iapp.app.run.mian`
- 截图：`docs/artifacts/m3-custom.png`

**待验**：运行时对 120/130 重新调用 `setBoxBackgroundMode`，看盒子是否出现（判断是否为 ppt 属性应用时机问题）。

**10:26 / 10:30 修复轮**

```
CUST clearbg 120
CUST F afterfix-120 boxBackgroundApplied = true
CUST clearbg 130
CUST F afterfix-130 boxBackgroundApplied = true
CUST cmp ppt size=54.0 pad=12/30 color=-14935264
CUST cmp ctl size=48.0 pad=48/51 color=-14935264
```

- 修复：`et.setBackground(null)` + `til.updateEditTextBoxBackgroundIfNeeded()` → 盒子出现（屏幕确认）
- 修复前 ppt 实例 `boxBackgroundApplied=false`，对照 true；字节码确认 `updateEditTextBoxBackgroundIfNeeded` 在 `editText.getBackground()!=null` 时直接 return
- 修复后仍差在子控件排版：ppt 54px / 内边距 12,30；对照 48px / 48,51（颜色相同）
- 截图：`docs/artifacts/m3-custom-fixed2.png`
- 待确认：盒子出现有约 1s 延迟（已加 `requestLayout()`+`invalidate()`，效果待复测）

**10:43 / 10:49 最终轮：修复移到 `loading` + 抄内置字号/内边距**

```
CUST early                    10:43:55.832
CUST fixOne 120 ok            10:43:55.885   ← 首帧前修好
CUST begin (loadingComplete)  10:43:56.402
CUST F before-120 boxBackgroundApplied = true
CUST bg t100 ImplApi18 1048x136 et=1048x136 att=true
```

```
CUST fixOne 130 ok size=48.0 pad=48/51
CUST fixOne 120 ok size=48.0 pad=48/51
CUST cmp ppt size=48.0 pad=48/51 color=-14935264
CUST cmp ctl size=48.0 pad=48/51 color=-14935264
CUST bg t100 ImplApi18 1048x167 et=1048x167 att=true
```

- 结论：修复必须挂在 `loading`；`loadingComplete` 会让首帧先画出无盒子状态（观感延迟）
- 字号/内边距从 `new TextInputEditText(til.getContext())` 抄，等价使用组件内置样式
- 屏幕：盒子首帧即有、文字内边距正常（用户确认"完美"）

---

## 2026-10-27 多 .iyu 跳转 / 栈 / 返回（NAV-1，com.demo.navprobe，API 34）

**工程**：`android-sync/ProjectApp/com.demo.navprobe`（A=`mian.iyu`、B=`p_b.iyu`、C=`p_c.iyu`，模块 `nav.mjava`）
**链路**：宿主 `android-sync/ProjectApp/<ID>` ↔ 设备 `/storage/emulated/0/Pictures/ProjectApp/<ID>`；4 个源文件 md5 一致，未 push
**设备**：emulator-5556，Android 14 / API 34，iApp 5.0.1013
**原始读数**：`docs/artifacts/nav1/logcat.txt`（757 行）、`docs/artifacts/nav1/dumpsys-activities.txt`
**logcat 命令**：`adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'`

探针：每页 `loading` 打 `NAV-ENTER`（activity 身份哈希 / 标题控件身份哈希 / sameAct / sameView / cls / taskId / pid / 上一页），`loadingComplete` 打 `NAV-READY`，`start/resume/pause/stop/destroy` 打 `NAV-LIFE`，跳转打 `NAV-GO`，返回键打 `NAV-KEY`。

**操作**：A 载入 → A→B → B→C → 在 C 连按系统返回 17 次 → 从外部弹出（非按键、非 uigo）→ 再弹 B → 再弹 A。

```
10-27 10:14:20.806 NAV-ENTER page=A n=1 act=156645770 sameAct=false view=243508003 sameView=false cls=com.iapp.app.run.mian task=7 pid=1140 last=null
10-27 10:14:20.825 NAV-LIFE page=A ev=start act=156645770
10-27 10:14:21.236 NAV-READY page=A act=156645770 view=243887875
10-27 10:14:22.922 NAV-GO from=A to=p_b.iyu flag=0 act=156645770
10-27 10:14:22.930 NAV-GO-RET to=p_b.iyu flag=0
10-27 10:14:22.941 NAV-LIFE page=A ev=pause act=156645770
10-27 10:14:23.034 NAV-ENTER page=B n=1 act=105583167 sameAct=false view=233482897 sameView=false cls=com.iapp.app.run.mian task=7 pid=1140 last=A
10-27 10:14:23.055 NAV-LIFE page=B ev=start act=105583167
10-27 10:14:23.376 NAV-READY page=B act=105583167 view=189877886
10-27 10:14:23.736 NAV-LIFE page=A ev=stop act=156645770
10-27 10:14:31.228 NAV-GO from=B to=p_c.iyu flag=0 act=105583167
10-27 10:14:31.243 NAV-GO-RET to=p_c.iyu flag=0
10-27 10:14:31.267 NAV-LIFE page=B ev=pause act=105583167
10-27 10:14:31.350 NAV-ENTER page=C n=1 act=18828245 sameAct=false view=15131297 sameView=false cls=com.iapp.app.run.mian task=7 pid=1140 last=B
10-27 10:14:31.368 NAV-LIFE page=C ev=start act=18828245
10-27 10:14:31.712 NAV-READY page=C act=18828245 view=28776009
10-27 10:14:32.036 NAV-LIFE page=B ev=stop act=105583167
10-27 10:14:51.723 NAV-KEY page=C kc=4 act=18828245
10-27 10:14:54.718 NAV-KEY page=C kc=4 act=18828245
...（kc=4 共 17 次，10:14:51 ~ 10:15:08，页面始终停在 C）
10-27 10:15:11.718 NAV-KEY page=C kc=113 act=18828245
10-27 10:15:11.758 NAV-KEY page=C kc=29 act=18828245
10-27 10:15:12.104 NAV-KEY page=C kc=31 act=18828245
10-27 10:15:57.345 NAV-LIFE page=C ev=pause act=18828245
10-27 10:15:57.368 NAV-LIFE page=B ev=start act=105583167
10-27 10:15:57.376 NAV-LIFE page=B ev=resume act=105583167
10-27 10:15:58.040 NAV-LIFE page=C ev=stop act=18828245
10-27 10:15:58.048 NAV-LIFE page=C ev=destroy act=18828245
10-27 10:15:59.809 NAV-LIFE page=B ev=pause act=105583167
10-27 10:15:59.819 NAV-LIFE page=A ev=start act=156645770
10-27 10:15:59.827 NAV-LIFE page=A ev=resume act=156645770
10-27 10:16:00.481 NAV-LIFE page=B ev=stop act=105583167
10-27 10:16:00.491 NAV-LIFE page=B ev=destroy act=105583167
10-27 10:16:01.440 NAV-LIFE page=A ev=pause act=156645770
10-27 10:16:02.056 NAV-LIFE page=A ev=stop act=156645770
10-27 10:16:02.063 NAV-LIFE page=A ev=destroy act=156645770
10-27 10:16:04.303 W/System.err( 1140): java.lang.IllegalArgumentException: View=android.widget.RelativeLayout{...} not attached to window manager
```

**读数**

| # | 现象 | 判定 |
|---|---|---|
| N1 | 三页 activity 身份哈希各不相同（A=156645770 / B=105583167 / C=18828245），类名均为 `com.iapp.app.run.mian`，`task=7`、`pid=1140` 不变 | ✅ `uigo` 每页新建一个 Activity 实例，同进程同任务 |
| N2 | 前进时序：旧页 `pause` → 新页 `loading`(NAV-ENTER) → `start` → `loadingComplete`(NAV-READY) → 旧页 `stop` | ✅ |
| N3 | C 已绑 `downkey`，返回键 17 次全部只进事件（`kc=4`），页面一次不弹 | ✅ 绑 `downkey` 会吞掉返回键 |
| N4 | 从外部弹掉 C 后：C `pause` → B `start`/`resume` → C `stop`/`destroy`；B 的 act 仍是 105583167，**没有 NAV-ENTER** | ✅ 弹栈回旧页 = 复用原 Activity，不重建、`loading` 不重跑 |
| N5 | 弹掉 B 回到 A 同样复用 156645770；A 最后 `pause`→`stop`→`destroy` 回到编辑器 | ✅ |
| N6 | 100 次按键里 `kc=113/29/31` 也进 `downkey`（音量下 / A / C） | ✅ 与既有结论一致：非方向键同样进事件 |
| N7 | 10:16:04 `IllegalArgumentException: … not attached to window manager` | ⚠ 发生在全部页面 destroy 之后，疑为 iApp 调试悬浮窗清理；与本课题无关，未深究 |

**未验证**：不绑 `downkey` 时返回键是否正常弹栈；`loading` 之外的 `restart` 事件（本页未绑，故 10:15:57 只看到 start/resume）；4 个 flag 的语义。

## 2026-10-27 多 .iyu 跳转 / 栈 / 返回（NAV-2，com.demo.navprobe，API 34）

NAV-1 的后续轮次。改动：C 页 `downkey` 改为 `nav.back`（判 `kc==4` 后 `activity.finish()`）；三页补绑 `restart`。
**原始读数**：`docs/artifacts/nav2/logcat.txt`

### 段一：finish() 当返回 + 默认返回键（10:19:35 ~ 10:19:54）

```
10-27 10:19:35.649 NAV-ENTER page=A n=1 act=188376684 sameAct=false view=251004189 sameView=false cls=com.iapp.app.run.mian task=9 pid=4042 last=null
10-27 10:19:37.503 NAV-LIFE page=A ev=pause act=188376684
10-27 10:19:37.608 NAV-ENTER page=B n=1 act=104209952 sameAct=false ... last=A
10-27 10:19:38.012 NAV-READY page=B act=104209952 view=19766467
10-27 10:19:38.338 NAV-LIFE page=A ev=stop act=188376684
10-27 10:19:40.024 NAV-LIFE page=B ev=pause act=104209952
10-27 10:19:40.121 NAV-ENTER page=C n=1 act=233137950 sameAct=false ... last=B
10-27 10:19:40.905 NAV-LIFE page=B ev=stop act=104209952
10-27 10:19:42.916 NAV-BACK page=C kc=4 act=233137950          ← 按返回
10-27 10:19:42.926 NAV-BACK-FINISH page=C                       ← activity.finish()
10-27 10:19:42.935 NAV-LIFE page=C ev=pause act=233137950
10-27 10:19:42.947 NAV-LIFE page=B ev=restart act=104209952      ← 旧页复用，无 NAV-ENTER
10-27 10:19:42.958 NAV-LIFE page=B ev=start act=104209952
10-27 10:19:42.967 NAV-LIFE page=B ev=resume act=104209952
10-27 10:19:43.596 NAV-LIFE page=C ev=stop act=233137950
10-27 10:19:43.605 NAV-LIFE page=C ev=destroy act=233137950
10-27 10:19:49.713 NAV-LIFE page=B ev=pause act=104209952      ← B 未绑 downkey，按返回
10-27 10:19:49.721 NAV-LIFE page=A ev=restart act=188376684
10-27 10:19:49.729 NAV-LIFE page=A ev=start act=188376684
10-27 10:19:49.737 NAV-LIFE page=A ev=resume act=188376684
10-27 10:19:50.380 NAV-LIFE page=B ev=stop act=104209952
10-27 10:19:50.387 NAV-LIFE page=B ev=destroy act=104209952
10-27 10:19:53.497 NAV-LIFE page=A ev=pause act=188376684      ← A 未绑，按返回
10-27 10:19:54.123 NAV-LIFE page=A ev=stop act=188376684
10-27 10:19:54.132 NAV-LIFE page=A ev=destroy act=188376684
```

### 段二：A→A 自跳（10:19:59 ~ 10:20:16）

```
10-27 10:19:59.294 NAV-ENTER page=A n=1 act=112367454 ...
10-27 10:20:01.296 NAV-GO from=A to=mian.iyu flag=0 act=112367454
10-27 10:20:01.310 NAV-LIFE page=A ev=pause act=112367454
10-27 10:20:01.391 NAV-ENTER page=A n=2 act=100162897 sameAct=false ... last=A   ← 新实例
10-27 10:20:01.757 NAV-READY page=A act=100162897
10-27 10:20:02.084 NAV-LIFE page=A ev=stop act=112367454                          ← 旧 A 进后台
10-27 10:20:04.076 NAV-LIFE page=A ev=pause act=100162897                          ← 按返回
10-27 10:20:04.084 NAV-LIFE page=A ev=restart act=112367454                        ← 回到旧 A
10-27 10:20:04.093 NAV-LIFE page=A ev=start act=112367454
10-27 10:20:04.100 NAV-LIFE page=A ev=resume act=112367454
10-27 10:20:04.715 NAV-LIFE page=A ev=stop act=100162897
10-27 10:20:04.724 NAV-LIFE page=A ev=destroy act=100162897
10-27 10:20:16.336 NAV-LIFE page=A ev=pause act=112367454
10-27 10:20:16.962 NAV-LIFE page=A ev=stop act=112367454
10-27 10:20:16.968 NAV-LIFE page=A ev=destroy act=112367454
```

**读数**

| # | 现象 | 判定 |
|---|---|---|
| N8 | C 绑 `downkey` 后判 `kc==4` 调 `activity.finish()`：C pause → B **restart/start/resume** → C stop/destroy，B 的 act 仍是 104209952 且无 NAV-ENTER | ✅ `finish()` 就是"返回"，且旧页复用 |
| N9 | B、A 未绑 `downkey`，按返回直接弹栈（B→A→destroy 回编辑器） | ✅ 不绑 downkey 时返回键走默认 Activity 栈 |
| N10 | 回到停过的页面事件顺序是 `restart → start → resume`（NAV-1 因未绑 restart 只看到 start） | ✅ |
| N11 | A→A 自跳：新 A 是**另一个 Activity 实例**（100162897），旧 A（112367454）pause→stop 留在栈里；返回回到旧 A 且 `restart/start/resume`，无 NAV-ENTER | ✅ 同名页也照样压栈，不做去重 |
| N12 | 用户屏幕观察：返回旧 A 后，旧 A 的数据完全没动过，"仿佛页面一直在后台" | ✅ 与 N11 一致 |

**未验证**：4 个 flag（536870912 / 67108864 / 268435456 / 1073741824）的语义。

## 2026-10-27 flag 536870912（NAV-3 分段一，com.demo.navprobe，API 34）

**原始读数**：`docs/artifacts/nav3/logcat-sofar.txt`

操作：A 页连点「A→B（flag 536870912）」共 10 次，每次间隔几百毫秒。屏幕始终停在 A，无任何跳转。

```
10-27 10:24:25.042 NAV-GO from=A to=p_b.iyu flag=536870912 act=182819623
10-27 10:24:25.059 NAV-GO-RET to=p_b.iyu flag=536870912
10-27 10:24:25.067 NAV-LIFE page=A ev=pause act=182819623
10-27 10:24:25.075 NAV-LIFE page=A ev=resume act=182819623
...（同一模式重复 10 次，act 恒为 182819623，无 NAV-ENTER）
10-27 10:24:57.057 NAV-LIFE page=A ev=pause act=182819623
10-27 10:24:57.723 NAV-LIFE page=A ev=stop act=182819623
10-27 10:24:57.737 NAV-LIFE page=A ev=destroy act=182819623
```

| # | 现象 | 判定 |
|---|---|---|
| N13 | `uigo("p_b.iyu", 536870912)` 每次：`NAV-GO` → `NAV-GO-RET` → 当前页 `pause` → 当前页 `resume`（同一 act），**不新建页面、不换页、不重跑 loading** | ✅ 536870912 在当前页上是 no-op |
| N14 | 手册称该值用于"内存中存在且正在显示时复用该界面"，但此处目标页 B 根本不在栈里，照样不跳 | ✅ 推翻手册页级语义 |

**解释（⚠ 推测）**：536870912 = `FLAG_ACTIVITY_SINGLE_TOP`(0x20000000)。所有 `.iyu` 共用同一个 Activity 组件 `com.iapp.app.run.mian`，栈顶永远"同类"，于是 Intent 被投递给栈顶实例（`onNewIntent`），而 iApp 的 `onNewIntent` 不换页 → 观感是"点了没反应"。行为特征（pause/resume 一次、不重建）与 SINGLE_TOP 命中完全吻合。

### NAV-3 分段二：其余 flag（10:27:46 ~ 10:30:14）

**原始读数**：`docs/artifacts/nav3/logcat-run2.txt`

```
10-27 10:27:46.955 NAV-ENTER page=A n=1 act=42157520 ... task=9 pid=4042
10-27 10:27:53.887 NAV-ENTER page=B n=1 act=25552376 ...
10-27 10:28:01.954 NAV-GO from=B to=p_b.iyu flag=536870912 act=25552376
10-27 10:28:01.976 NAV-LIFE page=B ev=pause act=25552376
10-27 10:28:01.982 NAV-LIFE page=B ev=resume act=25552376      ← 同页也是 no-op
10-27 10:29:04.041 NAV-GO from=B to=p_b.iyu flag=268435456 act=42157520
10-27 10:29:04.197 NAV-ENTER page=B n=2 act=177500752 ... task=9   ← task 不变
10-27 10:30:01.871 NAV-GO from=B to=p_b.iyu flag=0 act=42157520
10-27 10:30:02.003 NAV-ENTER page=B n=3 act=10549461 ... task=9
10-27 10:30:14.629 JavaErr：
10-27 10:30:14.629 Method go( java.lang.String, java.lang.Long ) not found in bsh scripted object: global
```

| # | 现象 | 判定 |
|---|---|---|
| N15 | `B→B(536870912)` 同页：B pause → B resume（act 不变），不新建 | ✅ 536870912 同页也是 no-op，手册"复用该界面"在观感上等于"什么都不做" |
| N16 | `268435456`：正常新建 B 实例（act=177500752），**task 仍是 9**，与普通跳转无可见差异 | ✅ NEW_TASK 在本场景不产生新任务（同 affinity 已有任务） |
| N17 | `1073741824` 点击后界面无反应，logcat 报 `Method go( java.lang.String, java.lang.Long ) not found` | ✅ 2³⁰ 的 yul 字面量以 **Long** 传入 mjava，签名 `(String,int)` 匹配失败、静默中断 |
| N18 | 返回 A 后点 `268435456` 按钮，`NAV-GO from=B`（实际在 A） | ✅ 返回不重跑 `loading`，探针的 `nav.page` 停在旧值 —— 反过来再次佐证"返回复用" |

**对照数据**：同一轮里 `0` / `268435456`(2²⁸) / `536870912`(2²⁹) 都是 `Integer`，只有 `1073741824`(2³⁰) 是 `Long`。

### NAV-3 分段三：Long 修复后复测（10:32:57 ~ 10:34:25）

**原始读数**：`docs/artifacts/nav3/logcat-run3.txt`

```
10-27 10:33:06.105 NAV-GO from=B to=p_c.iyu flag=1073741824 raw=java.lang.Long act=190984069
10-27 10:33:06.214 NAV-ENTER page=C n=1 act=58374498 ... last=B          ← 修复后能跳了
10-27 10:33:23.242 NAV-BACK page=C kc=4 act=58374498
10-27 10:33:23.276 NAV-LIFE page=B ev=restart act=190984069              ← 返回落 B
10-27 10:33:48.936 NAV-LIFE page=A ev=restart act=107700030              ← 再返回到 A
-------- 第二次：CLEAR_TOP --------
10-27 10:34:00.667 NAV-ENTER page=B n=2 act=233715948 ...
10-27 10:34:03.470 NAV-ENTER page=C n=2 act=104811828 ...
10-27 10:34:12.023 NAV-GO from=C to=mian.iyu flag=67108864 raw=java.lang.Integer act=104811828
10-27 10:34:12.106 NAV-ENTER page=A n=2 act=71043199 ... last=C           ← 新 A 实例
10-27 10:34:12.802 NAV-LIFE page=C ev=stop act=104811828
10-27 10:34:12.809 NAV-LIFE page=C ev=destroy act=104811828                 ← 只有 C 被销毁
10-27 10:34:23.561 NAV-LIFE page=B ev=restart act=233715948                 ← 返回落 B（B 没被清）
10-27 10:34:24.303 NAV-LIFE page=A ev=restart act=107700030                 ← 再返回到栈底 A
```

| # | 现象 | 判定 |
|---|---|---|
| N19 | `1073741824` 经修复后正常跳到 C；C 绑 downkey 按返回 → B → A | ✅ 能跳；"不排在内存中"的区分性效果**尚未测到**（按返回弹栈本身不区分） |
| N20 | 栈 `[A1, B, C]` 在 C 点 `C→A(67108864)`：**新 A2 压上来、只有 C 被销毁、B 原样保留**；返回依次 A2→B→A1 | ✅ CLEAR_TOP 没有清中间页 |

**统一解释（⚠ 推测，与 N13/N16 吻合）**：所有 `.iyu` 共用同一个 Activity 组件 `com.iapp.app.run.mian`，Android 的 Activity flag 是按**组件**匹配的，不是按页面文件匹配：

- `CLEAR_TOP` 命中的"已存在的目标实例"就是栈顶自己（C）→ 关掉 C、再起一个新的 run.mian（A），中间页不受影响
- `SINGLE_TOP` 同理永远命中栈顶 → 变成 no-op
- `NEW_TASK` 按 affinity 找任务，iApp 任务本来就在 → 同一 task

**结论：uigo 的 flag 不能用来做"页面级"栈控制。**

### NAV-3 分段四：NO_HISTORY 区分性测试（10:36:35 ~ 10:37:15）

**原始读数**：`docs/artifacts/nav3/logcat-run4.txt`

```
10-27 10:36:35.030 NAV-ENTER page=B n=1 act=218604471 ...
10-27 10:36:39.366 NAV-GO from=B to=p_c.iyu flag=1073741824 raw=java.lang.Long
10-27 10:36:39.444 NAV-ENTER page=C n=1 act=37357758 ... last=B
10-27 10:36:40.134 NAV-LIFE page=B ev=stop act=218604471            ← 普通页：只 stop
10-27 10:36:47.829 NAV-ENTER page=A n=2 act=799168 ... last=C
10-27 10:36:48.569 NAV-LIFE page=C ev=stop act=37357758
10-27 10:36:48.576 NAV-LIFE page=C ev=destroy act=37357758          ← NO_HISTORY 页：离开即 destroy
10-27 10:36:51.187 NAV-LIFE page=B ev=restart act=218604471         ← 返回直接落到 B
10-27 10:37:08.479 NAV-LIFE page=A ev=restart act=185890349         ← 再返回落到栈底 A
```

| # | 现象 | 判定 |
|---|---|---|
| N21 | 用 `1073741824` 进的 C，在 `C→A` 之后**立即** `stop → destroy`；返回时跳过 C 落到 B | ✅ NO_HISTORY 生效 |
| N22 | 同一次运行里普通页 B 只 `stop` 不 `destroy`（对照锚点） | ✅ 差别来自 flag，不是页面本身 |

## 2026-10-27 页面间传参 / 返回结果（NAV-5 分段一，com.demo.navprobe，API 34）

**操作**：A→B（i.sss 传参）→ B 显示参数；B→A（带回结果）→ A 显示结果；A→B（Intent extra 传参）→ 报错。
**读数**：用户屏幕 + 调试工具日志（`NAVPROBE`/`NAV-`）

```
10:50:58.523 NAV-PARAM-SET value=hello-from-A
10:50:58.672 NAV-ENTER page=B n=2 act=105686534 ...           ← B 载入，第 2 行显示 hello-from-A
10:51:12.807 NAV-RESULT-SET page=B value=res-from-B
10:51:12.925 NAV-LIFE page=A ev=restart act=99399440
10:51:13.005 NAV-LIFE page=A ev=resume act=99399440           ← A 回来，第 4 行读到 res-from-B
10:51:41.082 NAV-EXTRA-ERR java.lang.ClassNotFoundException: com.iapp.app.run.mian
    at java.lang.Class.forName(Class.java:485)
    at bsh.Reflect.invokeStaticMethod(Unknown Source:17)
    ...
```

| # | 现象 | 判定 |
|---|---|---|
| N23 | `i.sss` 设参数 → 目标页 `loading` 里读到 `hello-from-A` | ✅ `i.sss` 是跨页传参的可用通道 |
| N24 | B 里写 `i.sss("nav.result", ...)` 再 `finish()` → A 的 `resume` 读到 `res-from-B` | ✅ "返回结果"用 `i.sss` + 在 `resume` 里读，成立 |
| N25 | `Class.forName("com.iapp.app.run.mian")` 抛 `ClassNotFoundException`，而同一对象的 `getClass().getName()` 就是它 | ✅ mjava 的 BeanShell 解释器**看不见宿主类**（只能解析 boot class 如 `android.*`）；按名字取宿主 Class 不可行 |

**推断（⚠）**：不能按名字加载宿主类 → BeanShell 解释器用的是隔离（无父）类加载器。要拿 Class 只能从已有对象 `getClass()`，或者用 `i`/`activity` 直接反射调用。

**待办**：改用 `activity.getClass()` 重测自建 Intent 传参；自定义转场未回报。

### NAV-5 分段二：自建 Intent / 转场（10:53:45 ~ 10:54:39）

```
10-27 10:53:45.989 NAV-EXTRA-GO to=p_b.iyu k1=extra-from-A pkg=com.demo.navprobe open=mian.iyu
10-27 10:54:21.214 NAV-ANIM-GO to=p_b.iyu
10-27 10:54:21.234 NAV-ANIM-APPLIED
10-27 10:54:27.424 NAV-ENTER page=B n=3 act=254792838 ...        ← 转场页正常载入
```

| # | 现象 | 判定 |
|---|---|---|
| N26 | 用 `activity.getClass()` 自建 Intent（带 `ProjectPackageName` / `OpenFilexmlui` / 自定义 `k1`）→ `startActivity` 成功，B 页第 3 行读到 `extra-from-A` | ✅ 可以自己塞 extra 传参 |
| N27 | `uigo` 之后调用 `activity.overridePendingTransition(slide_in_left, slide_out_right)` → 用户观感"有区别" | ✅ mjava 可接管转场 |
| N28 | 重开工程后 A 第 4 行（`i.sss 结果`）为 `null` | ✅ 符合 `i.sss` 每次运行重置；非 bug |

**静态对照**：`uigo` 字节码只做 `new Intent` → `putExtras(fj.D(file))` → `startActivity`；`fj.D` 只放 `ProjectPackageName` + `OpenFilexmlui` 两个键；宿主里 `overridePendingTransition` 仅有一处字符串字面量，无原生调用。

## 2026-10-27 打包模式复验（NAV-6，com.demo.navprobe.apk，API 34）

**包**：`android-sync/ProjectApp/com.demo.navprobe/bin/com.demo.navprobe.apk`（4910350 B）
`versionCode=100001`（=100000+versionint）、`versionName=NAV-1`、`targetSdk=36`、启动 Activity `com.iapp.app.run.mian` ✅ 与既有打包结论一致
**安装**：`adb install -r` 成功，包名 `com.demo.navprobe`（与开发模式宿主 com.iapp.app 并存）
**原始读数**：`docs/artifacts/nav5/logcat-packaged.txt`

操作：桌面图标启动 → A→B（普通）→ 返回 → A→B（i.sss 传参）→ B→A（带回结果）→ A→B（Intent extra 传参）→ 返回 → A→B（自定义转场）

```
11:04:03.537 I/NAVPROBE: NAV-ENTER page=A n=1 act=228792239 ... cls=com.iapp.app.run.mian task=16 pid=7211
11:04:42.248 I/NAVPROBE: NAV-PARAM-SET value=hello-from-A
11:04:56.667 I/NAVPROBE: NAV-RESULT-SET page=B value=res-from-B
11:05:05.030 I/NAVPROBE: NAV-EXTRA-GO to=p_b.iyu k1=extra-from-A pkg=null open=null
11:05:06.347 I/NAVPROBE: NAV-ENTER page=B n=3 act=89880000 ... task=16
11:05:28.811 I/NAVPROBE: NAV-ANIM-GO to=p_b.iyu
11:05:29.009 I/NAVPROBE: NAV-ANIM-APPLIED
11:05:30.137 I/NAVPROBE: NAV-ENTER page=B n=4 act=264052886 ... task=16
```

| # | 现象 | 判定 |
|---|---|---|
| N29 | 打包后 A→B 正常，`NAV-ENTER` 显示每页新的 act、cls=`com.iapp.app.run.mian`、task=16 | ✅ 打包模式仍是"每页一个 Activity 实例" |
| N30 | `i.sss` 传参 `hello-from-A`、返回结果 `res-from-B` 均到达（用户屏幕确认） | ✅ 打包后 `i.sss` 与生命周期语义一致 |
| N31 | 自建 Intent 传 `k1` 成功，但当前 Intent 的 `ProjectPackageName` / `OpenFilexmlui` 都是 **null** | ✅ 打包模式不依赖这两个内部键；自建 Intent 仍可用 |
| N32 | `overridePendingTransition` 在打包版同样有可见效果 | ✅ |
| N33 | `ygs` 通道 **0 行**，`I/NAVPROBE`（`android.util.Log`）**61 行** | ✅ 打包只关 `i.syso`，标准 Log 正常 |

## 2026-10-27 lan / addv（NAV-7 分段一，com.demo.navprobe，API 34）

**背景**：用户提醒手册里还有跳转动画与"界面替换"入口，复查手册发现漏了 `lan` / `end` / `addv`。

**手册原文（`docs/reference/iyu-helpV3.0.txt`）**
- 【lan 跳转界面动画】2441：`uigo("abc.iyu")` + `lan(6)`，模式 0~11（6=右往左推出）
- 【end 结束界面】1306：`end()` 结束当前界面并返回原界面，没有原界面则退出应用
- 【addv 加载界面】2106：`addv(id, "a.iyu")` 把界面载入指定控件；支持 `a.iyu|b.iyu` 侧滑/滑动窗体
- uigo 段落（1222）**只有 4 个 flag**，没有"清栈/替换当前页"的模式

**本轮读数**

| # | 现象 | 判定 |
|---|---|---|
| N34 | `i.uigo(file)` 后 `i.lan(6)`：转场为**向左平移**；对照 `activity.overridePendingTransition(slide_in_left, slide_out_right)` 为**向右平移** | ✅ `lan` 可用，且与 override 是两套入口 |
| N35 | `i.addv(Integer.valueOf(20), "p_b.iyu")` → 返回 `null`，容器 `children=0`，无异常 | ❌ id 形式不生效 |
| N36 | `addv` 字节码：第一参不是 `View` 时走 `u(obj, String.valueOf(obj))` 解析，解析不到直接 `return null`；普通容器分支按后缀做 `endsWith` 过滤后才载入 | ✅ 解释了 N35 |

**待复测**：`i.addv(activity.findViewById(20), "p_b.iyu")`（直传 View）是否能把 `.iyu` 载入容器。

### NAV-7 分段二：addv 传 View（11:36:05）

```
NAV-EMBED-GO file=p_b.iyu
NAV-EMBED-RET file=p_b.iyu view=android.widget.LinearLayout ret=null children=0
```

| # | 现象 | 判定 |
|---|---|---|
| N37 | 直传容器 View 给 `i.addv` 仍返回 `null`、无子控件、无异常 | ❌ mjava 侧 `i.addv` 对 `.iyu` 无效 |

下一步：在同一页对比「iyu 里直接 `addv(20,"p_b.iyu")`」与「mjava `i.addv`」。

### NAV-7 分段三：addv 只能写在 iyu（11:39:06 ~ 11:39:31）

```
11:39:07.502 NAV-ENTER page=C ...
11:39:1x     （点「内嵌 B（iyu 直接 addv）」→ 容器里出现 B，无任何 NAV-ENTER）
11:39:16.775 NAV-UNEMBED before=1 after=0
11:39:17.398 NAV-EMBED-RET file=p_b.iyu view=android.widget.LinearLayout ret=null children=0 icls=com.iapp.app.Aid_javaCode
```

| # | 现象 | 判定 |
|---|---|---|
| N38 | `.iyu` 里直接 `addv(20, "p_b.iyu")` → B 的界面出现在容器里；mjava `i.addv(view, file)` → `ret=null`、`children=0`，而 `i.getClass().getName()` 就是 `com.iapp.app.Aid_javaCode` | ✅ `addv` 是 **yul 层专属**，`Aid_javaCode.addv` 走不通 |
| N39 | 内嵌过程中没有 `NAV-ENTER` / 生命周期事件；容器子控件数 1（目标页被包了一层 LinearLayout） | ✅ 内嵌只是塞控件树，不是新页面 |
| N40 | mjava 侧对容器 `removeAllViews()`：`before=1 after=0` | ✅ 内嵌内容可由 mjava 清理 |

**结论**：`addv` 是"一个 Activity 里换页"的官方通道，但调用点必须在 `.iyu`（白名单本来就只允许 iyu 写 `addv`）。uigo 是"每页一个 Activity"的另一套。

---

## 2026-10-27 Material 1.13 包支持扫描（静态）

- 工程 `sdk/iapp.sdk` 内置 `com.google.android.material:material:1.13.0`
- APK 内 `com/google/android/material/` 类共 490 个
- `docs/scripts/material_scan.py docs/artifacts/base.apk`：主要 widget 全部具备
  `(Landroid/content/Context;)V` 构造（MaterialButton / MaterialCardView / Chip / ChipGroup /
  Slider / RangeSlider / 两个 Progress / LoadingIndicator / FAB / ExtendedFAB / MaterialSwitch /
  SwitchMaterial / CheckBox / RadioButton / 各 TextField / TabLayout / 各 AppBar / 各 Navigation /
  SearchBar / SearchView / Carousel / MaskableFrameLayout / ShapeableImageView / MaterialDivider /
  MaterialSplitButton / MaterialButtonToggleGroup）
- 运行时扫描页：`com.demo.m3showcase/src/material.iyu` + `matsupport.mjava`（日志 tag `MAT`）
- 规范落点：`references/material-components.md`、`SKILL.md` 控件类型一节、`builtin-controls.md`

### NAV-8：内嵌页事件 / 原生查找 / 多页 addv（12:05:28 ~ 12:07:20）

```
12:05:36.429 NAV-ENTER page=D n=1 act=9901789 ...
12:05:49.440 NAV-EMBEDDED-CLICK n=1 act=9901789
...（共 16 次 NAV-EMBEDDED-CLICK）
12:06:25.887 NAV-FIND act9001=false(null) c20find=false(null) c20n=1 c21n=0
12:07:16.523 NAV-CLEAR c20=1->0 c21=2->0
12:07:20.062 NAV-FIND act9001=false(null) c20find=false(null) c20n=0 c21n=0
```

| # | 现象 | 判定 |
|---|---|---|
| N41 | 内嵌页 E 的按钮被点 16 次，`clicki` 全部进到 mjava（`NAV-EMBEDDED-CLICK n=1..16`，act 与宿主相同） | ✅ **内嵌页的事件绑定正常工作** |
| N42 | `activity.findViewById(9001)` 与 `c20.findViewById(9001)` 都拿不到（`false`），但容器 `c20` 有 1 个子控件 | ✅ 内嵌时控件 id **被重新分配**，原生按原 id 查不到（这解释了手册为何用 `ug(a.2,…)` 点号寻址） |
| N43 | 按钮里执行 `addv(21, "p_e.iyu|p_b.iyu")`：界面无变化，但随后 `NAV-CLEAR c21=2->0` 显示 ViewPager 里确有 2 个子控件 | ⚠ 多页 addv 塞进了子控件但 ViewPager 不显示（缺 adapter / 时机不对） |
| N44 | 内嵌页面的 `setText(9003)` 无效 → "没点击"文案没变 | ✅ 与 N42 同因；事件本身是通的 |

**下一步**：dump 内嵌控件树的真实 id；把多页 addv 挪到 `loading` 事件里（手册的用法）。

### NAV-9：内嵌控件 id 偏移 +10000（12:09:34 ~ 12:11:25）

**原始读数**：`docs/artifacts/nav5/logcat-nav9.txt`

```
12:09:34.406 NAV-ENTER page=D n=1 act=109640244 ...
12:10:08.360 NAV-TREE-START c20n=1
12:10:08.377 NAV-TREE android.widget.LinearLayout id=20              ← 容器
12:10:08.384 NAV-TREE   android.widget.LinearLayout id=19000         ← E 的根（原 9000）
12:10:08.399 NAV-TREE     android.widget.TextView id=19001 text=E-内嵌页（id 9000 段）
12:10:08.423 NAV-TREE     android.widget.Button id=19002 text=E 按钮（点我）
12:10:08.424 NAV-TREE     android.widget.TextView id=19003 text=未点击
12:11:25.124 NAV-FIND raw9001=false act19001=true(E-内嵌页（id 9000 段）) c20find19001=true(...) c20n=1
```

| # | 现象 | 判定 |
|---|---|---|
| N45 | 内嵌页控件树：原 id 9000/9001/9002/9003 → 实际 **19000/19001/19002/19003**（+10000），且外层包了一层 id=20 的容器（页面根挂在容器下） | ✅ **内嵌时控件 id 统一 +10000** |
| N46 | `activity.findViewById(19001)` 与 `c20.findViewById(19001)` 都能拿到，`getText()` 是原页文案 | ✅ 内嵌页可用**原生 findViewById** 访问 |
| N47 | 用 `setText(19003, …)` 改内嵌页文案成功（用户确认"变了"）；内嵌页按钮 `clicki` 每次都能进 mjava | ✅ 内嵌页"事件 + 原生读写"两条都通 |
| N43（续） | 多页 `addv(21, "p_e.iyu|p_b.iyu")` 到 ViewPager：容器里有 2 个子控件但界面空白、不能滑 | ❓ ViewPager 不渲染；单页 addv 到普通容器完全可用 |

**未验**：多层内嵌时偏移是否叠加（10000×层数）。

## 2026-10-27 Material 包运行时扫描（material.iyu / matsupport）

```
MAT total=35 ok=34
MAT ok-ctx com.google.android.material.button.MaterialButton view
MAT ok-ctx com.google.android.material.textfield.TextInputLayout group
...
MAT no-ctx  com.google.android.material.carousel.Carousel java.lang.NoSuchMethodException
MAT no-ctor com.google.android.material.carousel.Carousel java.lang.NoSuchMethodException
```

- 35 个候选里 34 个可用 `(Context)` 构造实例化（view/group 已标注）
- `Carousel` 失败是**类被裁剪**：dex 里 `Carousel` 只有 5 个 getter（getCarouselAlignment /
  getContainerHeight / getContainerWidth / getItemCount / isHorizontal），没有 `<init>`
- 第一次扫描 35 个全部 `lookup-fail`：`Class.forName(name)` 在 BeanShell 里看不到应用类；
  改用 `activity.getClassLoader().loadClass(name)` 后正常
- 交付插曲：共享目录把 `matsupport.mjava` 同步成截断文件（4190/4222 字节），
  iApp 报 `Parse error ... <EOF>`；`adb push` 后 md5 对齐

### NAV-10：多页 addv / 二级内嵌（12:15:47 ~ 12:16:53）

**原始读数**：`docs/artifacts/nav5/logcat-nav10.txt`

```
12:15:47 NAV-TREE fr.castorflex.android.verticalviewpager.VerticalViewPager id=31
12:15:47 NAV-TREE   android.widget.LinearLayout id=19000        ← E（9000 + 10000）
12:15:47 NAV-TREE     ... 19001 / 19002 / 19003
12:15:47 NAV-TREE   android.widget.LinearLayout id=20001        ← B（1 + 20000）
12:15:47 NAV-TREE     ... 20002 / 20003 / 20004 / 20005 / 20006 / 20010 / 20011 / 20012
12:15:47 NAV-TREE androidx.drawerlayout.widget.DrawerLayout id=32   （子控件与 31 相同：19000 + 20001）
12:16:53 NAV-TREE android.widget.LinearLayout id=20
12:16:53 NAV-TREE   android.widget.LinearLayout id=38000        ← F（8000 + 30000）
12:16:53 NAV-TREE     android.widget.TextView id=38001 text=F-中间页（id 8000 段）
12:16:53 NAV-TREE     android.widget.LinearLayout id=38002
```

| # | 现象 | 判定 |
|---|---|---|
| N48 | 同一 `addv` 调用里的多页，按顺序分配号段：第 1 页 +10000、第 2 页 +20000（E→19000，B→20001） | ✅ 号段按"页序"分配 |
| N49 | 另一个页面（H）里首次内嵌 `p_f.iyu`，得到 **+30000**（8000→38000），而同进程里再次内嵌的 E 仍是 +10000 | ✅ 号段是 **按界面文件、进程级**分配，不是按容器、不是按层级 |
| N50 | `VerticalViewPager` 容器：子控件（E、B）都在树里，但界面无内容 | ❌ 与 ViewPager 同 |
| N51 | `DrawerLayout` 容器：有内容（第 1 页 E 显示），第 2 页 B 是抽屉、收起状态，滑不出来 | ⚠ 子控件齐全，只是抽屉需要程序打开 |
| N52 | H 页用硬编码 `addv(18002, "p_e.iyu")` 无效（F 的容器实际是 38002） | ✅ 印证 N49，不能按 +10000 硬编码 |

**修正 N45**：内嵌 id 不是固定 +10000，而是**每个界面文件在进程内独占一个 10000 号段，按首次内嵌顺序递增**。

## 2026-10-27 组件画廊上屏（gallery.iyu / gallery.mjava）

```
GAL total=20 ok=20
GAL add/ok <20 个 Material 全类名>（逐条 ok，无 fail）
```

- 20 个待验证项全部构造并 attach 成功，页面无崩溃、无重叠
- 默认可见 10 个：MaterialSwitch、RangeSlider（单 thumb）、LoadingIndicator、
  ExtendedFloatingActionButton（胶囊底）、BottomAppBar、BottomNavigationView（空底栏）、
  TabLayout（基线）、SearchBar（胶囊+图标）、MaterialDivider（细线）、BottomSheetDragHandleView
- 默认空白 10 个（需内容/属性）：MaterialSplitButton、ChipGroup、MaterialAutoCompleteTextView、
  MaterialToolbar、CollapsingToolbarLayout、NavigationRailView、NavigationView、SearchView、
  MaskableFrameLayout、ShapeableImageView
- 截图：`docs/artifacts/m3-gallery.png`（上半）、`m3-gallery-mid.png`、`m3-gallery-bottom.png`
- 实现方式：反射 `activity.getClassLoader().loadClass` + `(Context)` 构造，逐项 try/catch，
  失败项红字上屏（本轮无失败）

### NAV-11：原生找容器 + 抽屉（13:03:23 ~ 13:04:25）

**原始读数**：`docs/artifacts/nav5/logcat-nav11.txt`

```
13:03:23.195 NAV-FBOX id=18002 cls=android.widget.LinearLayout      ← 原生找到 F 的容器
13:03:32.819 NAV-TREE android.widget.LinearLayout id=20
13:03:32.835 NAV-TREE   android.widget.LinearLayout id=18000         ← F 占第 1 段（+10000）
13:03:32.851 NAV-TREE     android.widget.LinearLayout id=18002
13:03:32.851 NAV-TREE       android.widget.LinearLayout id=29000     ← 嵌套的 E 占第 2 段（+20000）
13:03:32.852 NAV-TREE         ... 29001 / 29002 / 29003
13:04:10.455 NAV-DRAWER-ERR java.lang.IllegalArgumentException: No drawer view found with gravity LEFT
```

| # | 现象 | 判定 |
|---|---|---|
| N53 | mjava 沿树找到 F 的容器 `18002`，把**控件对象**交给 yul 的 `addv` → E 成功内嵌到 F 内部（树里出现 29000 段） | ✅ **addv 第一参可以直接传 View**，用来做"原生定位 + 内嵌" |
| N54 | 本次运行 F 先嵌 → +10000；E 后嵌 → +20000（同一进程内顺序分配） | ✅ 印证 N49：号段按"文件首次内嵌顺序"递增，不能硬编码 |
| N55 | `DrawerLayout.openDrawer(Gravity.START)` 抛 `No drawer view found with gravity LEFT` | ✅ 内嵌子控件没有 drawer gravity，DrawerLayout 不认 |

**推论**：内嵌控件的 id 无法预先知道 → 正确做法是**用原生遍历找控件/容器**，再交给 `addv`（N53）。

**MaterialSplitButton 空白的机制（13:05 补充）**

```
Class descriptor : 'Lcom/google/android/material/button/MaterialSplitButton;'
Superclass       : 'Lcom/google/android/material/button/MaterialButtonGroup;'
REQUIRED_BUTTON_COUNT : 2
```

- 它是按钮组容器，必须挂恰好 2 个 `MaterialButton` 子按钮；画廊里只 `new` 了容器 → 空组空白
- 属预期行为，不是加载失败；矩阵里归 ⚪（需内容）

### NAV-12：DrawerLayout 抽屉打通（13:14:19 ~ 13:14:29）

```
13:14:19.617 NAV-DRAWERFIX child=1 lpcls=androidx.drawerlayout.widget.DrawerLayout$LayoutParams gravity=8388611
13:14:19.632 NAV-DRAWER scheduled id=32
13:14:20.049 NAV-DRAWER open-later id=32 vis=0 w=540
13:14:20.066 NAV-DRAWER open-later-done isOpen=false
13:14:27.264 NAV-DSTATE container=32 me w=540 h=540 n=2 isOpen=true
13:14:27.318 NAV-DSTATE  child0 LinearLayout w=540 h=540 left=0 x=0.0 vis=0
13:14:27.319 NAV-DSTATE  child1 LinearLayout w=348 h=540 left=0 x=0.0 vis=0
```

| # | 现象 | 判定 |
|---|---|---|
| N56 | 改第二个子控件 `DrawerLayout.LayoutParams.gravity=0x800003` 后，延后 400ms `openDrawer(START)`：子控件从 `vis=4 / x=-348` 变为 `vis=0 / x=0`，`isDrawerOpen=true`，屏幕出现 B 页 | ✅ **DrawerLayout 是可用的多页容器**（内容页 + 抽屉页） |
| N57 | 立刻调 `openDrawer` 时 `isOpen=false`、`x=-348`、`vis=4`；延后调用才生效 | ✅ 必须等布局完成（`postDelayed` 400ms） |
| N58 | 用户反馈：32 高度太小、上方 31 空白占位，页面需要滚动 | ✅ 长页面改 `ScrollView` 根 + 内层 LinearLayout（`id=1` ScrollView / `id=2` 容器，其余 `did=2`） |

### NAV-13：ScrollView 结构复验（13:16 ~ 13:20）

| # | 现象 | 判定 |
|---|---|---|
| N59 | G 页改成 `ScrollView(id=1)` + 内层 `LinearLayout(id=2, height=-2)` 后：能上下滚动、32 号 DrawerLayout（320dp）完整可见；`addv → 32` 后抽屉页 B 直接可见；改 gravity + 延迟 openDrawer 仍正常 | ✅ 长页面统一用 ScrollView 根；DrawerLayout 在滚动容器里也正常 |
| N60 | D 页同样改滚动结构后可以滚到 21 号 ViewPager | ✅ |

**未验**：打包模式下 `addv` / `DrawerLayout` / `ScrollView` 的行为（本课题全部 addv 结论均来自开发模式）。

### NAV-14：打包版内嵌页事件复验（13:32:05 ~ 13:32:26）

```
13:32:16.805 I/NAVPROBE: NAV-ENTER page=H n=1 act=5518808 ...
13:32:20.389 I/NAVPROBE: NAV-FBOX id=18002 cls=android.widget.LinearLayout
13:32:22.264 I/NAVPROBE: NAV-EMBEDDED-CLICK n=1 act=5518808
...（共 8 次，act 全部是 H 页）
```

| # | 现象 | 判定 |
|---|---|---|
| N61 | **打包版**里二级内嵌页（E 在 F 里）的按钮被点 8 次，`clicki` 全部触发并进到 mjava | ✅ 二级内嵌的事件绑定在打包模式下正常 |
| N62 | 用户观感"点了没反应"：实际是探针处理函数写死 `setText(19003, …)`，而本次 E 位于第 2 号段（29000），写错了控件 | ✅ **探针缺陷**，不是平台行为；已改为按文字前缀找控件 |
| N63 | 用户反馈：打包与开发环境表现一致（除日志通道） | ✅ 与 NAV-6 结论一致 |

**覆盖缺口（本轮补测）**：内嵌到 DrawerLayout 第 2 页（抽屉里的 B）的控件事件尚未验。

### NAV-15：抽屉页事件 / 二级内嵌写回（13:4x）

| # | 现象 | 判定 |
|---|---|---|
| N64 | 二级内嵌的 E 按钮点击后文案正确变化（处理函数改按文字前缀查找后） | ✅ 二级内嵌的事件 + 原生写回都成立 |
| N65 | DrawerLayout 抽屉里（第 2 页 B）的「B → C」按钮点击后正常跳转到 C 页 | ✅ **抽屉页的控件事件正常**，内嵌到抽屉的页面是可交互的 |

**内嵌事件覆盖闭环**：一级 ✅ / 二级 ✅ / 抽屉页 ✅。

### NAV-16：打包版 DrawerLayout / ScrollView（13:39 ~ 13:50）

```
13:50:26.106 I/NAVPROBE: NAV-DRAWER-ERR ... No drawer view found with gravity LEFT   ← 未改 gravity 前，符合预期
13:50:28.160 I/NAVPROBE: NAV-DRAWERFIX child=1 ... gravity=8388611
13:50:28.615 I/NAVPROBE: NAV-DRAWER open-later id=32 vis=0 w=960
```

| # | 现象 | 判定 |
|---|---|---|
| N66 | 打包版 G 页（ScrollView 根 + DrawerLayout 320dp）：能滚动、`addv` 双页、改 gravity + 延迟 `openDrawer` 后抽屉正常滑出 | ✅ 打包模式与开发模式一致 |

**本课题打包模式覆盖**：uigo 多页 / 传参 / 返回结果 / 自建 Intent / 转场 / addv 二级内嵌事件 / DrawerLayout / ScrollView —— 全部一致。

## 2026-10-27 设计器崩溃（showcase.iyu，API 34）

```
FATAL EXCEPTION: main
java.lang.NullPointerException: Attempt to read from null array
  at com.iapp.app.VisualDesigner.T0(...:54)
  at com.iapp.app.VisualDesigner.T0(...:128) ×5
  at com.iapp.app.VisualDesigner.R0/S0/onClick
```

- 日志里没有任何 `SHOW fix` → 页面未运行，崩在设计器构建控件树/预览阶段
- 嫌疑：本轮新进 ppt 的 `ChipGroup` / `TabLayout` / `SearchBar` / `MaterialDivider`（及它们的 build.xml 登记）
- 处理：四类改为 mjava 动态创建、并从 `build.xml` 移除登记 → 页面可打开运行
- 未逐个隔离具体是哪一类触发

## 2026-10-27 XUI 1.1.9 试用（批次 XUI-P1 / P2，API 34）

目的：用「带资源的第三方 AAR」验证 SKILL 的外部库链路够不够用。

### 构件

| 项 | 值 |
|---|---|
| 库 | XUI 1.1.9（jitpack `com.github.xuexiangjys:XUI:1.1.9`），1025 个类 / 275 个资源文件 |
| 代码依赖 | calligraphy3 3.1.1、viewpump 2.0.3（XUI 类直接 implements `HasTypeface`，缺了类加载就失败） |
| 资源依赖 | appcompat 1.3.1（XUI 的 values 引用 `colorAccent`、`Theme.AppCompat.*`、`Widget.AppCompat.Spinner`） |
| 产物 | `xui.dex` 1 636 900 B + `xui-res.apk` 749 721 B（包 ID `0x80`） |
| 工程 | `android-sync/ProjectApp/com.demo.xui`（`apk/assets/` 放上面两件） |

### 打包链路上的读数

| # | 现象 | 判定 |
|---|---|---|
| X1 | `aapt2 link` 只喂 XUI 自己的 `res/`：`resource attr/colorAccent not found`、`style/Theme.AppCompat.*`、`Widget.AppCompat.Spinner` 全部 not found | ✅ 库的资源**不自足** |
| X2 | 加 `-I <宿主 base.apk>`（149 MB，带 0x7f 的 appcompat/material）无效，同样的 not found；最小复现（1 个 style 继承 `Theme.AppCompat.Light.Dialog`）同样失败 | ✅ `-I` 不能当资源依赖来源 |
| X3 | 把 appcompat 1.3.1 的 `res/` 和 XUI 的 `res/` 一起编进**同一个包**（`--package-id 0x80`）后通过 | ✅ 依赖资源必须同包链接 |
| X4 | 再加 material 1.13.0，报 `resource 'styleable/SearchView' has a conflicting value`；改 `-R` overlay 后又因 appcompat 的 attr 在 overlay 里不可见而连环失败 | ✅ 依赖版本必须对齐（appcompat 1.3.1 ↔ material 1.4.x 那一代） |
| X5 | material 走不通后只剩一个缺口：`style/Theme.Design.Light.BottomSheetDialog`（XUI 的 `XUITheme.BottomSheetDialog` 父样式） | ✅ 补桩样式即可 |
| X6 | appcompat 1.3.1 的 `res/color/*` 用了 `app:alpha`，但它自己的 `R.txt` 里没有 `attr/alpha` | ✅ 需补 `<attr name="alpha" format="float"/>` |
| X7 | XUI 的 `classes.jar` 里**没有** R 类（1025 个类全非 R），生成的 R 直接顶上 | ✅ 不存在重复类问题 |

补桩文件（链接期专用，随产物一起编进 0x80）：

```xml
<resources>
    <style name="Theme.Design.Light.BottomSheetDialog" parent="Theme.AppCompat.Light.Dialog"/>
    <attr name="alpha" format="float"/>
</resources>
```

### 运行期读数（P1：11 PASS / 6 FAIL）

```
XUI ROOT /storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp/com.demo.xui
XUI RES-MOUNT ret=7 path=.../apk/assets/xui-res.apk
XUI DCL-DIRECT-ERR java.lang.SecurityException: Writable dex file '.../apk/assets/xui.dex' is not allowed.
XUI DEX-COPY len=1636900
XUI DCL-CACHE ok
XUI XUI-INIT ok
XUI THEME-ID=0x800d01cb
XUI PASS ButtonView / CountDownButton / SmoothCheckBox / SwitchIconView / CircleProgressView /
         HorizontalProgressView / RadiusImageView / FlowTagLayout / AutoMoveTextView /
         MultipleStatusView / TabSegment
XUI FAIL TitleBar :: java.lang.UnsupportedOperationException: Failed to resolve attribute at index 3:
         TypedValue{t=0x2/d=0x800304c4 a=7}
XUI FAIL ShadowButton :: ... index 37: TypedValue{t=0x2/d=0x800304f0 a=7}
XUI FAIL ClearEditText :: ... index 68: TypedValue{t=0x2/d=0x8003051d a=7}
XUI FAIL MaterialSearchView :: InflateException ... line #36 ... TypedValue{t=0x2/d=0x800303a0 a=-1}
XUI FAIL RippleView :: Resources$NotFoundException: Resource ID #0x800500cd
XUI FAIL ShadowTextView :: Resources$NotFoundException: Resource ID #0x800600c3
XUI SELFTEST ok=11 fail=6
```

ID 反查（用生成的 `R.java`）：`0x800500cd=color/xui_config_color_white`、`0x800600c3=dimen/default_sd_shadow_radius`、
`0x800303a0=attr/search_view_actionbar_height`、`0x800304c4=attr/xui_actionbar_height`、`0x800304f0=attr/xui_btn_view_height`、
`0x8003051d=attr/xui_config_size_edittext_left_padding`。

| # | 结论 | 判定 |
|---|---|---|
| X8 | 直接加载工程目录里的 dex 被 Android 14 拒绝（`Writable dex file … is not allowed`），cache + 先 `setReadOnly` 再写的兜底成功 | ✅ 与 SKILL 既有结论一致 |
| X9 | `addAssetPath` 返回 7（非 0），`getIdentifier("XUITheme","style","com.xuexiang.xui")` 得到 `0x800d01cb` | ✅ 资源包挂载成功 |
| X10 | 6 个 FAIL 分两组原因，**互不相关** | ✅ |
| X11 | 组 A（4 个 attr 失败）：XUI 的尺寸类 attr 只定义在 `XUITheme.Phone` / `XUITheme.Tablet.*`，光用 `XUITheme` 时 `obtainStyledAttributes` 解析 `?attr/xui_actionbar_height` 失败 | ✅ |
| X12 | 组 B（2 个 NotFound）：`ResUtils.getResources()` = `XUI.getContext().getResources()`，即 **Application** 的 Resources；只把路径挂到 Activity 的 AssetManager 时 Application 看不见 | ✅（字节码 `XUI.getContext().getResources()`） |

### 运行期读数（P2：17 PASS / 0 FAIL）

改成 `ContextThemeWrapper(activity, XUITheme.Phone)` + 两个 AssetManager 都 `addAssetPath` 之后：

```
XUI RES-MOUNT[act] ret=7
XUI RES-MOUNT[app] ret=7
XUI PROBE-ID color=0x800500cd dimen=0x800600c3
XUI PROBE-ACT color=0xffffffff  dimen=24
XUI PROBE-APP color=0xffffffff  dimen=24
XUI XUI-INIT ok
XUI THEME-NAME XUITheme.Phone id=0x800d01cf
XUI SELFTEST ok=17 fail=0
XUI TOTAL ms=634
```

屏幕现象：TitleBar 用 XUI 自己的蓝色（`colorPrimary`）+ 返回箭头图标渲染；ShadowTextView / ButtonView /
CountDownButton / AutoMoveTextView / ClearEditText / 进度条全部上屏；检查框与开关图标类控件因为没设图标不可见（行为正常）。
→ 资源包里的 drawable / color / dimen / style / attr 在 iApp 里都能正常解析。

### 部署链路的两个现场事实

- `VisualDesigner.a9` 给出的工程根是 `/storage/emulated/0/Android/data/com.iapp.app/files/iApp/ProjectApp/<项目ID>`；
  该目录是指向 `/storage/emulated/0/Pictures/ProjectApp` 的**符号链接**，与共享目录是同一份文件（`md5` 一致）
- 宿主机改**已存在**的 `src/xui.mjava` 后：`/mnt/shared/Pictures/...`（vboxsf 直挂）已是新内容，
  `/sdcard/Pictures/...`（FUSE 视图）仍是旧内容（8312 vs 10836 字节），iApp 跑的是旧代码；
  `adb push` 该文件后两侧 md5 一致。新建文件（`__marker.txt`）则两侧立刻可见

### 复现命令（`scripts/build_aar_dex.py`）

```bash
export BUILD_TOOLS=<build-tools 目录>; export JDK_BIN=<jdk bin 目录>
python build_aar_dex.py \
  --aar XUI-1.1.9.aar --aar calligraphy3-3.1.1.aar --aar viewpump-2.0.3.aar \
  --res-aar appcompat-1.3.1.aar \
  --stub-res stub/res \
  --framework-res framework-res.apk \
  --manifest-package com.xuexiang.xui --name xui --out out/
```

- 产物与手工链路一致：`xui.dex` 1 636 952 B / `xui-res.apk` 749 817 B（手工版 1 636 900 / 749 721，
  差在一个 viewpump 的 res 文件和 zip 时间戳）；**脚本产物未再上机复跑**，工程里跑的是手工链路那一版
- 下载源：XUI 走 jitpack（`https://jitpack.io/com/github/xuexiangjys/XUI/1.1.9/XUI-1.1.9.aar`），
  calligraphy3 / viewpump / appcompat 走阿里云（central / google）

---

## 2026-10-27 API-A1 com.oyp.pytx 后端接口可用性普查（宿主机 curl/urllib，非设备探针）

**对象**：`gede.5read.com`（超星歌德借阅机），`gedeid=84751638`；旧配置 `http://ouyangpeng.top/urls.json`

**原始读数**（HTTP 状态 / 返回体首段）：

```
GET /apis/touchBook/books.jspx?cataid=123&pageSize=-1&gedeid=84751638
  → 200 {"result":0,"errorMsg":"没有获取到数据"}            # 图书「精品推荐」已空
GET /apis/touchBook/books.jspx?cataid=124&pageSize=-1&gedeid=84751638
  → 200 {"result":1,"msg":{"allCount":466,"list":[...]}}    # 其余 11 个分类全部有数据
GET /apis/magazine/magazines.jspx?cataid=6&pageSize=-1&gedeid=84751638
  → 200 {"result":1,"msg":{"allCount":54,...}}              # 期刊 7 个分类全部有数据（3/4/5/6/8/9/10）
GET /apis/magazine/magazineItems.jspx?magazineid=MZ11000014
  → 200 {"result":0,"errorMsg":"magazineid不能为空或参数不正确"}
GET /apis/magazine/magazineItems.jspx?magazineid=25
  → 200 {"result":1,"msg":{"magazine":{...},"itemList":[95 期]}}   # 只认数字 id
GET /apis/touchBook/books.jspx?keyword=%E8%AF%BB%E8%80%85&page=2&pageSize=5&gedeid=84751638
  → 200 {"result":1,"msg":{"pageCount":575,"allCount":2871,...}}   # 站内搜索可用
GET /apis/magazine/magazines.jspx?keyword=...（name/q/searchName/searchKey 同样试过）
  → 200 {"result":0,"errorMsg":"未获取到数据"}                     # 期刊无 keyword 搜索
GET /other/epub_epubRead_read.jspx?...sid=MZ12038766&from=5&detailUrl=...
  → HTTP 500（旧期刊阅读路径失效）
GET https://gede.5read.com/o/a.h?a=GEDE:gede.5read.com%2Fg%2F89949779.h
  → 301 → 200，页面内 InitData：{sid:'MZ12038766', from:'5', detailUrl:'<160 字符密文>', url:'BORROWMACHINE:...'}
GET /other/epub_epubRead_readNew.jspx?psize=10000&sid=MZ12038766&ucatalog=true&ctype=3&fsize=20&from=5&detailUrl=<密文>
  → 200 {"result":1,"msg":{"contents":[218],"catalogs":[30],"pageAll":218}}
  # 同一流程换图书 surl：contents=333, catalogs=9, pageAll=333；不带 cookie 也可用
GET http://ouyangpeng.top/urls.json
  → 302 Location: https://ai.ouyangpeng.top/jump.js（站点已改作跳转，搜索配置源失效）
```

**结论**：列表接口基本全活；期刊「挂了」是**阅读接口换代**（`epub_epubRead_read.jspx` → `readNew` + 密文 token）；
搜索原依赖的外部配置域名已失效，站内 `books.jspx?keyword=` 可替代；图书「精品推荐」分类 123 已无数据。

**复现**：上述均为宿主机直连，不依赖设备；密文 `detailUrl` 需先取 `/o/a.h` 页面。

---

## 2026-10-27 M3-D1 com.demo.m3demo 组件样张首轮（API 34 / iApp 5.0.1013）

**探针**：全新工程 `com.demo.m3demo`，8 组 Material 组件全部 ppt 声明，`loading` → `call(null,"mjava","m3.init")`；
mjava 只做配色、TIL 修复、tab/滑块/进度值与 FAB 图标。

**原始报错**（用户控制台原文，第一次运行）：

```
JavaErr：
Error in method invocation: Method setStrokeColor( int ) not found in class
'com.google.android.material.button.MaterialButton' : at Line: 76 :
... outlined.setStrokeColor(Color.parseColor("#717973"))
Called from method: paintButtons : at Line: 36 ...
Called from method: init : at Line: -1 ...
```

**屏幕现象（第一次）**：按钮组停在默认主题色；卡片、Chip、两个输入框、选择、滑块/进度、Tabs、反馈区
**全部没有执行初始化**；04 组两个 `TextInputLayout` 都没有盒子。

**修复**：`setStrokeColor(ColorStateList.valueOf(color))`（该类在该版本没有 int 重载）；
`init()` 里每段 `try/catch(Throwable)` 并 `i.syso("M3 fail xxx: "+t)`。

**第二次运行**：两个输入框盒子恢复，后续区块依次初始化（用户实机确认）。logcat 未见 `M3 fail` 输出。

**归因（✅）**：输入框盒子一直在代码里，是按 `md-components-guide.md` 的 `loading` 配方修的；
第一次运行根本**没跑到 `paintFields()`**——`paintButtons()` 里的方法不存在抛错，中断了整个 `loading` 事件。
所以「输入框没盒子」只是更早一处 Material API 重载写错的下游表现。

**复现**：MaterialButton 1.13.0 的 `setStrokeColor` 只有 `ColorStateList` 重载；int 会抛上述错误。

**第二轮补充读数**（2026-10-27 20:00:57，同一工程）：

```
10-27 19:51:22.503 Method setIndicatorColor( int ) not found ... LinearProgressIndicator   # 单值 int 中断
10-27 20:00:57.356 V/ygs: M3 init done                                                   # 改传 int[] 后整段跑完
```

- `setIndicatorColor(new int[]{color})` 被 BeanShell 接受 ✅，此后 `paintValue` / `paintFab` 均执行
- 每段 `try/catch` 没有输出（`M3 fail …` 一条都没有）→ 证实方法不存在的中断 `catch(Throwable)` 接不住

## 2026-10-27 设计器崩溃隔离 P1（批次 tabdesigner-p1，API 34）

目的：`pitfalls.md` #7 的 `VisualDesigner.T0` NPE 只隔离 `TabLayout`——短名 / Material 全类名 / `build.xml` 登记，三者谁触发。

### 探针（每工程只改一个变量；最小页 = LinearLayout 根 + 标签 TextView）

| 工程 | 页面 `type=` | `build.xml` 登记 | 用户观察 |
|---|---|---|---|
| `com.demo.tabprobe1` | `TabLayout`（短名） | 无 | 设计器正常 |
| `com.demo.tabprobe2` | `com.google.android.material.tabs.TabLayout` | 有 | 设计器正常 |
| `com.demo.tabprobe3` | `com.google.android.material.tabs.TabLayout` | 无 | 组件树显示“未知”，能开，无报错 |
| `com.demo.tabprobe4` | 页面无 TabLayout（仅 TextView） | 有（TabLayout） | 正常；登记项不出现在页面，无报错 |

源码归档：`android-sync/iapp-demo/tabdesigner-p1/`

### 原始读数（logcat，2026-10-27 20:21–20:24，`emulator-5556`）

```text
# 崩溃标记计数（FATAL EXCEPTION / VisualDesigner.T0 / Attempt to read from null array / killProcess）
0
```

只出现已知噪音（`pitfalls.md` #16）：

```text
W/System.err: java.lang.IllegalArgumentException: View=android.widget.ImageView{...} not attached to window manager
  at tj.B(...)
  at com.iapp.app.VisualDesigner.onCreate(...:133)
```

`VisualDesigner` 每次都能 `Displayed com.iapp.app/.VisualDesigner ... +178~195ms`；iApp 进程（pid 9106）全程存活，未被杀。

### 结论

- ✅ **`TabLayout`（短名与 Material 全类名）在 ppt 声明不会让设计器崩溃**；登记/不登记都不崩
- ✅ 未登记的完整类名 → 设计器组件树显示“未知”，但工程能打开、无报错（未验证展开“未知”节点）
- ✅ 仅登记、页面不声明 → 不崩；页面也不渲染该控件（符合预期）
- ❌ 推翻上一轮“四类都可能崩”的粗判：`TabLayout` 排除，真凶在 `ChipGroup` / `SearchBar` / `MaterialDivider`
- 下一步：批次 `tabdesigner-p2` 逐类隔离剩余三类

## 2026-10-27 设计器崩溃隔离 P2（批次 tabdesigner-p2，API 34）

目的：`tabdesigner-p1` 排除 `TabLayout` 后，逐个隔离 `ChipGroup` / `SearchBar` / `MaterialDivider`。

### 探针（每工程只放一类；全类名 + `build.xml` 登记）

| 工程 | 页面内容 | 登记 | 用户观察 |
|---|---|---|---|
| `com.demo.tabprobe5` | `ChipGroup` + 2×`Chip` | ChipGroup / Chip | 正常 |
| `com.demo.tabprobe6` | `SearchBar` | SearchBar | **闪退**；重复多次偶尔能进（能进时页面正常），多数闪退 |
| `com.demo.tabprobe7` | `MaterialDivider` | MaterialDivider | 正常（文字下方一条线，符合预期） |

源码归档：`android-sync/iapp-demo/tabdesigner-p2/`

### 原始读数（logcat，2026-10-27 20:26:54–20:27:56，`emulator-5556`）

三次 FATAL，栈完全相同，全部发生在 P6（SearchBar）打开设计器时，iApp 进程被杀：

```text
E/AndroidRuntime( 9644): FATAL EXCEPTION: main
E/AndroidRuntime( 9644): java.lang.NullPointerException: Attempt to read from null array
E/AndroidRuntime( 9644): 	at com.iapp.app.VisualDesigner.T0(...:54)
E/AndroidRuntime( 9644): 	at com.iapp.app.VisualDesigner.T0(...:128)
E/AndroidRuntime( 9644): 	at com.iapp.app.VisualDesigner.T0(...:128)
W/System.err( 9644): java.lang.Exception: call killProcess callstack! pid=9644
I/ActivityManager(  339): Process com.iapp.app (pid 9644) has died: fg  TOP
```

- 三次时间/pid：20:27:26（9644）、20:27:41（9939）、20:27:55（10068）
- P5 / P7 时段无 `FATAL EXCEPTION`、无 `VisualDesigner.T0`、无进程被杀

### 结论

- ✅ **`SearchBar` 是设计器崩溃的确认触发源**：页面只放 `com.google.android.material.search.SearchBar`（全类名 + 登记）即可复现
- ⚠ 崩溃是**概率性**的：多数打开闪退，少数能进；能进时页面正常
- ✅ `ChipGroup`（含 `Chip` 子项）、`MaterialDivider` 单独 ppt 声明**不崩**，从嫌疑清单排除
- ✅ 运行期 mjava 动态创建 `SearchBar` 可用（`material-components.md` 上屏矩阵 ✅）；问题只在设计器
- ❓ 仅登记 `SearchBar`、页面不声明是否也崩，未测
- 文档收敛：崩溃清单从三类缩为 `SearchBar` 一类

## 2026-10-27 设计器崩溃隔离 P3（批次 tabdesigner-p3，API 34）

目的：拆开 `SearchBar` 的“声明”和“登记”，并确认崩溃的时序规律。

### 探针

| 工程 | 页面 | `build.xml` | 用户观察 |
|---|---|---|---|
| P6'（复用） | 无 SearchBar（仅描述文字） | 登记 SearchBar | 连续 3 次打开都正常；下方空白，无报错 |
| P8（新建） | `SearchBar` 全类名 | 不登记 | 组件树显示“未知”；闪退 → 重开正常 → 再开闪退，交替 |

源码归档：`android-sync/iapp-demo/tabdesigner-p3/`

### 原始读数（logcat，2026-10-27 20:39:35–20:41:45，`emulator-5556`）

```text
20:39:35  Start proc 10963
20:39:40  Displayed com.iapp.app/.VisualDesigner   <- P6 第 1 次（正常）
20:40:10  Displayed com.iapp.app/.VisualDesigner   <- P6 第 2 次（正常）
20:40:20  Displayed com.iapp.app/.VisualDesigner   <- P6 第 3 次（正常）
20:40:24  FATAL (10963) VisualDesigner.T0 NPE      <- P8 在该进程第 4 次构建 -> 崩
20:40:25  Process com.iapp.app (pid 10963) has died
20:40:39  Displayed com.iapp.app/.VisualDesigner   <- 新进程 11337 首次构建 P8 -> 正常
20:40:45  FATAL (11337) VisualDesigner.T0 NPE      <- 同进程第二次 -> 崩
20:40:50  Displayed com.iapp.app/.VisualDesigner   <- 新进程 11465 首次 -> 正常
20:40:54  FATAL (11465) VisualDesigner.T0 NPE      <- 同进程第二次 -> 崩
20:41:45  Displayed com.iapp.app/.VisualDesigner   <- 新进程 11658 首次 -> 正常
```

三次崩溃栈完全相同：

```text
java.lang.NullPointerException: Attempt to read from null array
  at com.iapp.app.VisualDesigner.T0(...:54)
  at com.iapp.app.VisualDesigner.T0(...:128)
```

### 结论

- ✅ 触发条件是 **`SearchBar` 写进 ppt**，与 `build.xml` 登记无关：
  只登记不声明（P6'）连续 3 次正常；不登记只声明（P8）仍崩
- ⚠ 现象上表现为“新进程第一次正常、之后崩”，但**根因不是构建次数**——是设计器保存/序列化的 2 秒防抖，
  见文末「设计器崩溃根因（R8 反编译）」
- ✅ 未登记的 `SearchBar` 在设计器里显示“未知”，但仍会在第二次构建时崩
- ✅ 结论：`SearchBar` 只能 mjava 动态创建，不要写进 ppt；登记无影响，动态创建也不需要登记
- ⚠ 该时序规律与原 `m3showcase` 崩溃一致（打开它时进程里已构建过设计器树），但当时未记录进程内构建次数

### XUI-P3：开发模式补内容（20:07，API 34）

给每个控件配真实内容后，暴露两个**调用姿势**问题（都不是渲染问题，控件根本没进容器）：

```
XUI FAIL ButtonView :: java.lang.NullPointerException: Attempt to invoke virtual method
        'void android.graphics.drawable.GradientDrawable.setColor(int)' on a null object reference
XUI FAIL RippleView :: android.content.res.Resources$NotFoundException: Resource ID #0xff299ee3
XUI SELFTEST ok=15 fail=2
```

| # | 现象 | 根因（字节码确认） | 判定 |
|---|---|---|---|
| X13 | `ButtonView` 用 `new ButtonView(ctx)` 后调 `setSolidColor(int)` NPE | `setSolidColor` 直接对私有字段 `gradientDrawable` 调 `setColor`；该字段只在带 `AttributeSet` 的初始化路径里赋值，`(Context)` 构造后是 `null` | ✅ |
| X14 | `RippleView.setRippleColor(0xff299ee3)` 抛 `Resource ID #0xff299ee3` | 形参是**颜色资源 id**（内部 `getResources().getColor(id)`），传 ARGB 值会被当成 id 去查 | ✅ |

修法：ButtonView 自己铺 `GradientDrawable`（`setColor` + `setCornerRadius` + `setBackgroundDrawable`）；
RippleView 传 `getIdentifier("xui_config_color_main_theme","color","com.xuexiang.xui")` 拿到的 id。

### XUI-P4：打包版（20:42，API 34）

第一次打包运行失败：`projectRoot()` 依赖 `VisualDesigner.a9`，打包包里该类被裁掉 → `setup()` 直接放弃。
补上打包路径后（`getAssets()` → `cacheDir`，dex 走只读流程）：

```
I/XUI (12112): ROOT-ERR java.lang.ClassNotFoundException: Didn't find class "com.iapp.app.VisualDesigner" ...
I/XUI (12112): MODE=packaged
I/XUI (12112): ASSET-COPY xui-res.apk len=749721
I/XUI (12112): ASSET-COPY xui.dex len=1636900
I/XUI (12112): PATHS dex=/data/user/0/com.demo.xui/cache/xui.dex res=/data/user/0/com.demo.xui/cache/xui-res.apk
I/XUI (12112): RES-MOUNT[act] ret=6
I/XUI (12112): RES-MOUNT[app] ret=6
I/XUI (12112): PROBE-ACT color=0xffffffff dimen=24
I/XUI (12112): PROBE-APP color=0xffffffff dimen=24
I/XUI (12112): DCL-DIRECT ok
I/XUI (12112): XUI-INIT ok
I/XUI (12112): THEME-NAME XUITheme.Phone id=0x800d01cf
I/XUI (12112): SELFTEST ok=17 fail=0
I/XUI (12112): TOTAL ms=1042
```

| # | 结论 | 判定 |
|---|---|---|
| X15 | 打包模式：dex 和**资源包**都要从 APK assets 释放到 `cacheDir`；资源包可写不影响，dex 必须只读（走「开流 → setReadOnly → 写完再设一次」） | ✅ |
| X16 | 只读释放后 `DexClassLoader` 直接加载成功（`DCL-DIRECT ok`，无 SecurityException）；addAssetPath 的 cookie 从 7 变 6 属正常（路径顺序不同） | ✅ |
| X17 | 打包版 `ygs` 无输出，`android.util.Log.i("XUI", …)` 有输出；两套日志同时写最省事 | ✅ |
| X18 | 资源包在 cacheDir 里同样能被 `addAssetPath` 挂载，Activity/Application 两份都生效（`PROBE-ACT`/`PROBE-APP` 都能取到 color/dimen） | ✅ |

---

## 2026-10-27 QJ-P1 青简运行时能力探针（com.qingjian.reader，API 34）

**探针**：`mian.iyu` 的 `loading` → `call(null,"mjava","qj_probe.boot")`；`boot` 内 `i.fn("qj_ui")` 上色后，
在 `new Thread(new Runnable(){...})` 里 `i.hs` 拉真实列表 → `org.json` 解析 → `runOnUiThread` 回主线程 →
动态建 ImageView 并用 `i.us(iv,"src",cover)` 加载网络封面。

**第一轮（20:43:17）闪退**：

```
20:43:17.105 V/ygs: PROBE hs len=2624
20:43:17.120 E/AndroidRuntime: FATAL EXCEPTION: Thread-33
    Process: com.iapp.app, PID: 11901
    java.lang.reflect.UndeclaredThrowableException
      at $Proxy5.run(Unknown Source)
      at java.lang.Thread.run(Thread.java:1012)
    Caused by: Typed variable declaration : No static field or inner class: json of class org
      at Line: 22 ... : org .json .JSONObject
      at bsh.BSHAmbiguousName.toObject ...
```

- 屏幕：直接闪退，无页面
- 归因：`org.json.JSONObject` 全限定名被 BeanShell 解析成「类 `org` 的字段 `json`」；
  该错误在线程内 `catch(Throwable)` 接不住，穿过 bsh Proxy 到 `Thread.run`，**杀进程**

**第二轮（20:44:44）通过**（顶部 `import org.json.JSONObject;` 后）：

```
20:44:44.755 V/ygs: PROBE hs len=2624
20:44:44.757 V/ygs: PROBE json result=1 n=2
20:44:44.770 V/ygs: PROBE ui
20:44:44.782 V/ygs: PROBE img https://unicover.duxiu.com/coverNew/CoverNew.dll?iid=…
```

屏幕：首页骨架 + 一张 80×110 封面缩略图；无 JavaErr。

**结论（✅ API 34）**：`i.hs(String)` 同步 GET 可用；匿名 `Runnable` 与 `runOnUiThread` 可用；
`i.us(View,"src",url)` 能加载网络图；`org.json.*` 必须 import，不能用全限定名。

---

## 2026-10-27 设计器崩溃根因（R8 反编译，API 34）

对象：`docs/artifacts/base.apk`（iApp 5.0.1013，`classes4.dex`）中的 `com.iapp.app.VisualDesigner`。
工具：`dexdump -d` + `scripts/dex_body.py`（`DEXDUMP` 指向 build-tools 35 的 `dexdump.exe`）。
本节修正 P3 的“同进程第二次构建起必崩”表述：那只是现象，真正条件是**设计器执行保存/序列化**。

### 调用链（与崩溃栈逐帧对应）

```text
VisualDesigner.onClick(:554)
  -> S0(:89)          自动保存
    -> R0(:24)        遍历预览容器子控件
      -> T0(:128)     递归子控件
        -> T0(:54)    aget-object 读 tag 数组 -> NPE
```

### 各方法（字节码还原）

- `S0()V`：当前文件后缀为 `.iyu/.ilua/.ijava/.ijs` 时，若 `now - D8 < 2000` 直接返回（2 秒防抖）；
  否则拼 `<工程根>/src/<当前文件>`，用 `R0(R$id.Vo)` 取预览树文本，追加 `<UIEventset>…</UIEventset>` 后写盘。
  `D8 = System.currentTimeMillis()` 在 `VisualDesigner.<init>` 里赋值。
- `R0(I)String`：`findViewById(id)` → `ViewGroup` → 遍历 `getChildAt(i)`，逐个 `T0(child, 0, sb)`。
- `T0(View,I,StringBuilder)V`：把 View 序列化回 `<View id did type><ppt><event>`；
  从 `view.getTag()` 取 `Object[]`，约定 `[0]=type, [1]=ppt, [2]=event`。
- `q2(String,ArrayList,Map)V`：解析 `<View …>` 时给每个由 `.iyu` 创建的控件
  `setTag(new Object[]{type,ppt,event,null})`。
- `if0.q(id,type)`：短名 switch 找不到时，若 `type` 含 `.` 就走 `t0()` 反射实例化，**与 `build.xml` 登记无关**。

### 崩溃点（`T0` 字节码）

```text
0x000a: if-ge v0, 1, 0x29      # id >= 1 -> 直接去序列化
0x000c: if-nez v1, 0x85        # 只有 id < 1 才做 tag == null 检查
...
0x0035: aget-object v4, v1, 0  # 对 null 数组取下标 -> NPE（positions: 0x0035 line=54）
```

即：**`id >= 1` 的控件跳过 tag 空检查**，`tag == null` 时直接 NPE。

### 为什么是 `SearchBar`

`SearchBar` 构造里 `inflate(R.layout.mtrl_search_bar, this)`，给自己加了带资源 id 的内部子 View：

```text
sget R$id.open_search_bar_text_view / open_search_bar_placeholder_text_view /
     open_search_bar_text_view_container
```

这些子 View 的 id 非 0，但不是 `.iyu` 声明的，iApp 不会给它们打 `Object[]` tag。
序列化时 `T0` 递归进 `SearchBar`，再递归到它的内部 TextView → tag 为 null → 第 54 行 NPE。

`TabLayout` / `ChipGroup` / `MaterialDivider` 的内部子 View 没有非 0 id（或没有自建子 View），所以不崩。

### 结论

- ✅ 崩溃发生在**设计器保存/序列化**（运行前保存、切代码页、布局调整等都会调 `S0`），不是“打开设计器就崩”
- ✅ `S0` 有 2 秒防抖（`D8` 在 Activity 构造时赋值）：进程刚起、2 秒内的第一次保存会被跳过，
  看起来像“重开第一次正常”
- ✅ 与 `build.xml` 登记无关；`type` 含点号时 `if0.q` 直接反射实例化
- ✅ 运行期 mjava 动态创建不受影响：`R0` 只序列化设计器预览树
- ⚠ 泛化：任何“构造时自建带资源 id 子 View”的第三方控件都可能触发同一缺陷，不止 `SearchBar`

> 收尾（2026-10-27）：`com.demo.xui` 工程与 `build/xui` 中间产物已按「探针用完即删」清理。
> 复建时按上面的复现命令重新下载依赖、生成 `xui.dex` / `xui-res.apk`，放进新工程的 `apk/assets/`；
> 运行期代码照 `SKILL references/external-library-guide.md` 的「接入骨架」抄。

---

## 2026-10-27 设计器崩溃根因验证 Demo（com.demo.sbverify / com.demo.sbcrash，API 34）

目的：用两个可运行 Demo 独立验证上节根因与时序，不依赖设计器的偶发现象。

### Demo 1：机制自检（`com.demo.sbverify`，安全页）

页面 ppt 不含 SearchBar；`loading` → mjava 在运行期 `new SearchBar(activity)`，给 SearchBar 自己
`setId(9999)` + 模拟 q2 的 `Object[]{type,ppt,event,null}` tag，再遍历它的子 View。

原始读数（2026-10-27 20:58:57–20:58:58）：

```text
SBCHECK searchbar id=9999 tagType=[Ljava.lang.Object;
SBCHECK childCount=2
SBCHECK child=0 cls=androidx.appcompat.widget.AppCompatImageButton id=-1 tag=null risky=false
SBCHECK child=1 cls=android.widget.FrameLayout id=2131296828 tag=null risky=true
SBCHECK risky=1
SBCHECK sim child=0 id=-1 skip:id<1
FATAL EXCEPTION: main
java.lang.reflect.UndeclaredThrowableException
  at $Proxy3.run(...)
Caused by: Typed variable declaration : Not an array : at Line: 73 ... [ 0 ]
```

`2131296828 = 0x7F09023C = com.iapp.app:id/open_search_bar_text_view_container`
（`aapt dump resources` 反查），正是 SearchBar 构造时 inflate `mtrl_search_bar` 加进来的内部 FrameLayout。

结论：

- ✅ 运行期实测：SearchBar 的直接子 View 带非 0 资源 id、`tag=null`（`risky=1`）
- ✅ 对 `id >= 1` 的子 View 执行 `((Object[]) tag)[0]` 直接杀进程；BeanShell 抛
  `Typed variable declaration : Not an array`，穿过匿名 Runnable 代理成
  `UndeclaredThrowableException`，`catch(Throwable)` 接不住（与 `pitfalls.md` #8.1 同类）
- 设计器里同一操作是 JVM 级 `aget-object` → `NullPointerException: Attempt to read from null array`；
  Demo 里是 BeanShell 求值 `[0]` 抛的不同异常类，但**后果相同（进程死）**，指向同一缺陷

### Demo 2：设计器时序（`com.demo.sbcrash`）

页面 ppt 直接声明未登记的 SearchBar；`loading` 打 `SBCRASH page running` 作为“页面真的运行了”的标记。

原始读数（20:59:36–20:59:55）：

```text
20:59:36.733 Displayed com.iapp.app/.VisualDesigner   <- 打开工程
20:59:38.380 V/ygs: SBCRASH page running              <- 首次运行（打开后约 1.6s，S0 防抖跳过保存）
20:59:38.462 Displayed com.iapp.app/.run.mian
20:59:55.116 FATAL ... VisualDesigner.T0:54           <- 再次运行/保存（>2s） -> 崩
```

结论：

- ✅ 打开设计器本身不崩（能看到搜索框）
- ✅ 打开后 2 秒内的首次保存被 `S0` 防抖跳过 → 页面正常运行（`SBCRASH page running`）
- ✅ 超过 2 秒后再触发保存 → `T0:54` NPE 闪退
- ✅ 与用户观察一致：第一次运行正常，第二次运行闪退

### 总体

根因（`T0` 对 `id >= 1` 跳过 tag 判空 + SearchBar 内部子 View 无 tag）已由**运行期自检**与
**设计器 A/B** 两条独立证据链验证通过。

源码归档：`android-sync/iapp-demo/sbverify-demo/`（`com.demo.sbverify` / `com.demo.sbcrash`）。

---

## 2026-10-28 QJ-P2 搜索接口复查：`keyword` 是假参数（推翻 API-A1 的一条结论）

**触发**：青简搜索页无论输入什么，结果完全一致。

**原始读数**（宿主机直连，同一 `gedeid`）：

```
keyword=读者      → {"result":1,"msg":{"allCount":2871,...}}  首两条：<同一批>
keyword=孔子      → {"result":1,"msg":{"allCount":2871,...}}  首两条：<同一批>
keyword=123331231231232 → allCount=2871
keyword=zzzzzz    → allCount=2871
```

参数扫：`keyword / name / title / q / key / word / searchKey / searchText / kw / value / bookName`
全部返回 `allCount=2871`，首条标题一致 → **参数被忽略，返回的是全量列表**。

路径扫：`/apis/touchBook/search.jspx`、`searchBook.jspx`、`/apis/search/*` 等均返回
`{"result":0,"errorMsg":"接口路径不存在"}`（`books/search.jspx` 为 404）→ 官方接口没有搜索。

**结论（✅ API 34 环境无关，纯服务端行为）**：`books.jspx` 的 `keyword` 无效，API-A1 里
“站内搜索可用”是误判——当时只看 `result:1` 和条数，没有比对不同关键词的结果。
旧版 app 的搜索依赖 `ouyangpeng.top/urls.json` 指向的私有代理，官方没有等价接口。

**替代方案**：客户端全量索引——11 个图书分类 + 7 个期刊分类各拉一次 `pageSize=-1`，
按 key 去重落盘，之后本地按标题/作者/简介过滤（约 4000 图书 + 500 期刊，首次约 18 个请求）。

---

## 2026-10-28 QJ-P3 目录跳页：`contentIndex` 不是页索引

**现象**：阅读器目录显示「第 100 页」，点击跳到后底部页码显示「第 20 页」（举例）。

**原始读数**（图书 `HYB…`，surl `gede.5read.com/g/c8ef34b77bcb49b790c4df77cd8d4031.h`）：

```
contents=333  pageAll=333  catalogs=9
  page=1   contentIndex=0
  page=2   contentIndex=1
  page=3   contentIndex=2
  page=330 contentIndex=6      ← 页号与 contentIndex 不再一致
  page=332 contentIndex=7
  page=333 contentIndex=8
```

**结论（✅）**：`catalogs[].page` 是 1 基页号，直接对应 `contents[page-1]`；
`contentIndex` 是章节内部的索引，不能拿来当页号。青简原来的 `toc()` 用了 `contentIndex`，所以跳错。

**修法**：`ci = page - 1`，并夹在 `[0, total-1]`。

---

## 2026-10-28 QJ-P4 两个 BeanShell 崩溃点（搜索页首次打开 / 目录跳页回归）

**崩溃读数**（搜索页首次打开，pid 3283）：

```
W/System.err: java.lang.NullPointerException: Attempt to get length of null array
    at java.lang.StringFactory.newStringFromChars
    at java.lang.String.valueOf(String.java:4106)
    at bsh.Reflect.invokeStaticMethod
    ... bsh.BSHTypedVariableDeclaration ...
```

**归因（✅）**：`String st = String.valueOf(i.sss("qj.idx.state"))`，首次打开时该 key 为 null，
BeanShell 把 `valueOf(null)` 解析到 `valueOf(char[])` 重载，直接 NPE。
同类写法 `String.valueOf(m.get("total"))` 在旧历史记录上也会踩。

**修法**：统一走 `x == null ? "" : String.valueOf(x)` 的兜底函数；数字解析再包一层默认值。

**另一条（✅ 2026-10-27）**：`downkey` 事件只传 `st_kC` 一个实参时，iApp 报
`NumberFormatException: For input string: "qj_pages.mjava"`；写成 `"D", st_kC` 两个实参即正常，
与 navprobe / game2048 的既有形状一致。

---

## 2026-10-28 QJ-P5 搜索框：ppt TIL 放进 56dp 横条被撑高、文字下沉

**现象**（截图）：搜索页顶部 `TextInputLayout` 盒子高约 90dp，占满并溢出 56dp 顶栏；
hint「书名 / 作者 / 出版社」贴在盒子顶部内侧，输入文字沉到盒子下半部且可内部滚动。

**探针**：`search.iyu` 中 TIL `width=0 height=-2 layout_weight=1`，子控件 `TextInputEditText`；
`ui_fixField(4)` 按 `md-components-guide.md` 配方修盒子。

**结论（⚠→改方案）**：同一修复配方在纵向列表里正常（`com.demo.m3demo`），
但放进固定 56dp 的横向栏（weight 撑宽 + wrap 高）后，TIL 的 box 高度按子控件内边距计算，约 90dp，
在栏内被裁；文字看起来“滚到下面”。

**改法**：搜索框改为普通 `EditText` + 圆角 `GradientDrawable`（22dp）+ 左右 16dp padding，
不再用 TIL。输入框高度 44dp、`singleLine=true`、`imeOptions=actionsearch`。

---

## 2026-10-28 ENV-1 环境探测首跑（M1：Windows 10 + 雷电 14/9）

**工具**：`docs/scripts/detect_env.py`（本轮新建，只读）

**原始输出**：

```
== 环境探测 2026-10-28T11:22:01 ==
宿主  Microsoft Windows 10 专业教育版 10.0.19045
虚拟化 Hyper-V=off
产品  雷电模拟器 9 v9.5.42.0 — 运行中
产品  雷电模拟器 14 v14.0.32.1 — 运行中
adb   E:\Program Files\platform-tools\adb.EXE (Android Debug Bridge version 1.0.41)
       emulator-5556 [device] API=34 android=14 model=25102RKBEC iApp=5.0.1013 uid=10072 root=yes 工程根->/storage/emulated/0/Pictures/ProjectApp
共享  E:\workspaces\2026-10-24-iapp-dev-ai-space\android-sync -> /sdcard/Pictures/ProjectApp [ok]
FTP   未配置 [skipped]
通道  shared=ok adb=ok ftp=unknown
建议  shared（备选 adb）；档案 ldplayer14
```

**补充读数**（`adb shell`，2026-10-28）：

```
pm list packages -U com.iapp.app  -> package:com.iapp.app uid:10072
dumpsys package com.iapp.app     -> versionCode=127 minSdk=21 targetSdk=37 / versionName=5.0.1013
readlink .../Android/data/com.iapp.app/files/iApp/ProjectApp
                                 -> /storage/emulated/0/Pictures/ProjectApp
ls -ld /sdcard/Pictures/ProjectApp-> drwxrwxrwx 1 media_rw media_rw 4096 2026-10-27 21:20
appops get ... MANAGE_EXTERNAL_STORAGE -> allow
su -c id                         -> uid=0(root) gid=0(root) context=u:r:su:s0
```

**进程路径**（区分两套雷电）：

```
dnplayer        -> C:\leidian\LDPlayer14\dnplayer.exe
Ld9BoxHeadless  -> C:\Program Files\ldplayer9box\Ld9BoxHeadless.exe
```

**结论**：

- M1 = 雷电 14（API 34）在连 + 雷电 9（API 28）已装且 VM 引擎在跑但未连 adb ✅
- 宿主 Hyper-V 未启用（`HypervisorPresent=False`）✅
- `targetSdk` 实测 37，与 `delivery-guide.md` 里的 36 不符 ⚠（以 37 为准）
- `dnplayer.exe` 在雷电 9/14 下同名，**只能靠可执行文件路径区分** ✅

---

## 2026-10-28 ENV-2 FTP 通道读数（M2 他机，经交接文档带回，本机未复验）

> 来源：另一台 Windows 11 + 腾讯应用宝电脑版的机器，2026-10-27 在该机实测。
> 本机（M1）现在无法复验（宿主到雷电内的 FTP 因网关隔离不通，用户 2026-10-28 口述）。

**服务器**：`ftp://172.22.39.216:9527`（该机一次读数，端口每次可能变）

**原始读数（他机）**：

```
登录            anonymous + 任意邮箱 -> 成功
FEAT            MLSD MLST SIZE MD5 MODE Z AUTH TLS
STOR/DELE/MKD/RMD                 -> 全部成功
MLSD /ProjectApp/<项目ID>          -> 列表中没有 .project；SIZE 145B，与本地 MD5 一致
STOR 到不存在的父目录              -> 失败（不会自动建父目录）
传完立即 MD5                       -> 一致
根目录                             -> ProjectApp/ DownloadFileDir/ Userimg/ screenshot/ *.txt
```

**结论（级别 ⚠ 他机）**：匿名可读写、`SIZE`/`MD5` 可用、点文件不列、`STOR` 不建父目录。
宿主可达性因环境而异，不作为通用事实。

**本机补充（2026-10-28）**：`ftp_sync.py` 的参数守卫生效——Git Bash 把
`--remote /ProjectApp/x` 改写成 `C:/Program Files/Git/ProjectApp/x` 后，脚本按预期拒绝并提示
`MSYS_NO_PATHCONV=1`（实测，见本轮命令输出）。

---

## 2026-10-28 ENV-3 FTP 通道本机实测（M1 雷电 14，经 adb forward）

**前提**：用户在 iApp 打开服务器控制台，地址 `ftp://172.16.1.87:9527`；
设备侧 `netstat` 显示 `[::]:9527 LISTEN 5388/com.iapp.app`。

**宿主直连（❌）**：

```
detect_env.py --ftp 172.16.1.87:9527
-> FTP 172.16.1.87:9527 [unreachable]（WinError 10061）
```

宿主不在 172.16.1.x 网段（设备在雷电 NAT 后），直连不可达。

**只转发控制端口（部分可用）**：

```
adb -s emulator-5556 forward tcp:9527 tcp:9527
-> detect_env --ftp 127.0.0.1:9527 -> [ok]（登录成功）
-> 但 NLST 时报 ConnectionRefusedError：
   PASV 返回 172.16.1.87:<数据端口>，宿主到不了
```

**主动模式（❌）**：`set_pasv(False)` → `425 Can't open data connection`（超时）。

**逐数据端口转发（✅）**：重写 `makepasv()`——拿到 PASV 端口后 `adb forward tcp:<port>`，
再连 `127.0.0.1:<port>`。实测每次数据连接会新开端口（如 32969、36219），所以必须逐个转发。

**原始读数（本机，2026-10-28）**：

```
FEAT   211-Extensions supported
         SIZE | MDTM | REST STREAM | LANG en;zh-tw;ja;is | MLST Size;Modify;Type;Perm
         AUTH SSL | AUTH TLS | MODE Z | UTF8 | TVFS | MD5 | MMD5 | MFMT
PWD    /
NLST   DownloadFileDir ProjectApp Temp Userimg iAppDir screenshot tempFile
       igame-helpV1.0.txt igame-<乱码>.txt ijava-helpV3.0.txt ijs-helpV3.0.txt
       ilua-helpV3.0.txt iyu-helpV3.0.txt iyu-helpV5.0.txt iyu-helpV6.0.txt
MLSD   /ProjectApp/com.qingjian.reader
       -> AndroidManifest.xml build.xml files icon.png res sdk src   （无 .project）
SIZE   /ProjectApp/com.qingjian.reader/.project      -> 213 145
MD5    /ProjectApp/com.qingjian.reader/src/mian.iyu  -> 341CAFE426CFE30C3BF767EAA2C73474
本地   src/mian.iyu 4384B md5 341cafe426cfe30c3bf767eaa2c73474（一致）
```

`ftp_sync.py --adb-forward emulator-5556 --port 9527 --remote /ProjectApp/com.qingjian.reader --dry-run`：

```
15 个文件；13 个两侧大小一致，2 个本地更大：
  ~ src/qj_pages.mjava  本地 32423 / 远端 32401
  ~ src/qj_reader.mjava 本地 9653 / 远端 9642
```

**写入未验完**：准备在 `/ProjectApp/_ftp_probe_20261028` 做 MKD/STOR/SIZE/MD5/DELE/RMD 时，
iApp 进程退出（`pidof com.iapp.app` 为空，9527 只剩 TIME_WAIT），连接得到 EOFError；
探针未创建任何目录或文件。写入能力仍按他机读数记 ⚠。

**结论**：
- 宿主直连设备 FTP ❌（NAT）✅本机
- 控制端口 forward 可登录 ✅本机
- 数据连接必须逐端口 forward；主动模式不可用 ✅本机
- 点文件不列、`SIZE` 可探、`MD5` 与本地一致 ✅本机
- 根目录含中文文件名乱码一条（`igame-<乱码>.txt`），编码问题待查 ⚠
  - **更正（见 ENV-4）**：那是本机控制台编码导致的显示问题；服务端文件名本身是正常 UTF-8

---

## 2026-10-28 ENV-4 FTP 写入与协议细节（M1，iApp pid 6161，经 adb forward）

**环境**：`ftp://172.16.1.87:9527`，设备侧 `[::]:9527 LISTEN 6161/com.iapp.app`；
宿主经 `adb forward`（控制 + 逐数据端口）连接。探针目录 `/ProjectApp/_ftp_probe_20261028b`，跑完即删。

| 操作 | 结果 | 原始响应 |
|---|---|---|
| `MKD root` / `MKD a` / `MKD a/b` | ✅ | 257 逐级创建成功 |
| `MKD p/q`（父 `p` 不存在） | ❌ | `550 Can't create directory .../p/q` → **MKD 非递归** |
| `STOR probe.bin`（8192B 随机） | ✅ | 226 Transfer complete |
| `SIZE probe.bin` | ✅ | `213 8192` |
| `MD5 probe.bin` | ✅ | `567EB07E…DB55`，与本地一致 |
| `MLSD root` | ✅ | `['a', 'probe.bin']` |
| `STOR .probe_dot` / `SIZE` | ✅ | `213 3`；**MLSD 不列点文件** |
| `STOR "测试 文件.txt"` / `SIZE` | ✅ | `213 5`；MLSD 精确返回 `测试 文件.txt` |
| `RNFR/RNTO` | ✅ | 250 file renamed |
| `APPE` +10B | ✅ | `213 8202`（8192+10） |
| `REST 100` + `RETR` | ✅ | 收到 8102B（8202-100） |
| `STOR missing/x.bin`（父不存在） | ❌ | **`551 /...: Error on output file`**（不是 550/553） |
| `DELE` ×3 / `RMD` ×3 | ✅ | 250 |
| 清理后 `MLSD` | ✅ | 空列表 |

**编码核对（推翻 ENV-3 的乱码结论）**：

```
MLSD 返回名 repr: '\u6d4b\u8bd5 \u6587\u4ef6.txt'   -> 精确等于「测试 文件.txt」✅
根目录 igame 手册: 'igame-\u4e2d\u6587\u7f16\u7a0bV1.0.txt' -> 「igame-中文编程V1.0.txt」✅
```

ENV-3 里看到的 `igame-<乱码>.txt` 是**本机控制台编码**（GBK）造成的显示问题，不是服务端编码问题。
含中文与空格的路径可正常 `STOR`/`SIZE`/`DELE`，往返一致。

**结论**：FTP 通道的读、写、改名、追加、断点、删除、建/删目录全部可用；
两个硬约束是 **`MKD` 非递归** 与 **`STOR` 不建父目录（551）**，投递脚本必须先逐级建目录。

---

## 2026-10-28 ENV-5 ftp_sync.py 端到端（M1，经 adb forward）

**探针**：临时本地目录 4 个文件（含 `.project`、`src/sub/`、`sdk/`、5000B 随机二进制），
远端 `/ProjectApp/_ftp_probe_sync`（隔离目录，跑完删除）。

```
push : 文件总数 4  上传 4/4  MD5 校验 4  -> 退出码 0
pull : 文件总数 4  下载 4/4  MD5 校验 4  -> 退出码 0
两侧 md5sum 全部一致
pull 不存在的远端 /ProjectApp/_no_such_dir_xyz -> 退出码 5（550 No such directory）
```

**过程中发现并修掉的两个脚本问题**：

1. **拉取不存在的远端会“成功返回 0 文件”**：`walk_remote` 把 `MLSD`/`NLST` 的失败吞掉了。
   已改为拉取前先 `CWD <remote>`，失败即退出 5。
2. **`except (all_errors, RuntimeError)` 抛 TypeError**：`ftplib.all_errors` 本身就是元组，
   不能嵌套在 `except` 的元组里。已改为 `ALL_ERRORS = all_errors + (RuntimeError,)`。

**清理时的额外验证**：`MLSD` 不列 `.project`，按列表删文件后 `RMD` 报
`450 Can't remove directory`——必须按 `DOTFILES` 点名删点文件，再自底向上删目录。
清理后 `/ProjectApp` 下恢复为 19 个工程，无残留。

---

## 2026-10-28 QJ-P6 阅读接口分段与虚拟尺寸

**探针**（同一本图书，token 复用）：

```
psize=10000              -> contents=333  catalogs=9  pageAll=333
psize=30                 -> contents=30   catalogs=9  pageAll=333   # 目录不受 psize 限制
psize=1                  -> contents=1    catalogs=9  pageAll=333   # 取目录的最省请求
psize=10&page=1 vs page=2 -> p2[0] == p1[1]                          # page 是 1 基内容起点
psize=30&page=31         -> 从第 31 条内容开始
w=1000&h=2000            -> pageAll=91，目录页号同步缩放（330→89 / 333→91）
w=2000&h=2000            -> pageAll=85
```

**结论（✅）**：
1. `page` 是内容起点（1 基），配合 `psize` 可做分段拉取；`page=31&psize=30` 取 31–60 页。
2. `psize=1` 也返回完整 `catalogs`，目录可以单独便宜地取。
3. `w/h` 决定服务端分页，必须固定一组值（青简用 1000×2000）；否则 `pageAll`、目录页号、分段边界全对不上。
4. 正文 HTML 无内联宽度；图片带 `width/height` 属性，需要 `max-width:100%!important;height:auto!important` 覆盖，
   并关闭 WebView 的 wide viewport / overview mode，宽屏才会铺满。
## 2026-10-28 DOC-1 三层文档架构体检与 review skill 落地

**新建** `.claude/skills/docs-architecture/`：`SKILL.md` + 4 份 references（architecture / evidence-and-levels / maintenance / review-checklist）
+ `scripts/review_docs.py` + `review_config.json` + `scripts/README.md`。
根 `CLAUDE.md` 的三层判据、目录约定、知识沉淀细则迁入该 skill，`CLAUDE.md` 只留 8 条要点 + 指针。

**体检输出（`e55723b` 基线，59 个 Markdown）**：

```
阻断 0 / 应修 64 / 建议 21
LEVEL-03×23  LEVEL-05×15  LINK-03×20  LINK-02×12  LINK-04×11  NUM-01×3  LINK-01×1
```

**首跑到收敛的校准记录**（198 阻断 → 0）：

| 误报来源 | 处理 |
|---|---|
| 代码块里的示例路径被当死链 | 跳过 fenced code |
| 整份 `SKILL.md` 的表格被当索引进 | 索引只扫「导航」小节，且只认首列是反引号路径的行 |
| 多行命令被逐行判缺参 | 按反斜杠续行拼接后再判 |
| 三列能力矩阵被当「同格多级别」 | 级别判断改为按单元格，且只看 ✅+⚠ |
| 版本号 `9.5.42.0` 被当 IPv4 | 行内含 LDPlayer/版本 时跳过 IP 检查 |
| `C:\Program Files` 被截成 `C:\Program` | 盘符正则吃到反引号或行尾 |

**本轮修掉的阻断项**：SKILL 里的真实 IP（`ftp-delivery.md`、`ftp_sync.py`）、作者盘符（`emulator-setup.md`、`icon-guide.md`、`scripts/README.md`、`make_icon.py`）、
他机读数写成 ✅（`tencent-appstore-pc.md`、`environments/README.md`）、`CLAUDE.md` FTP 示例缺 `--remote`/`--port`、`--tls` help 与实现不符、
`targetSdk 37/36` 被当成矛盾（改为「安装包 37 / 打包产物 36」）、`scripts/README` 漏 `dex_common.py`、`docs/scripts/README.md` 缺失。

**未修（留作下一轮应修）**：`✅` 缺日期 23、`❓` 缺验证法 15、跨 skill 引用缺前缀 20、历史 spec 的行号引用 12 与 `cases/` 死链 11、数值口径分组 3。

**反向验证**：临时目录里造「死链 + 他机 ✅ + 缺索引」三类问题，脚本全部报出且退出码 1。

---

## 2026-10-28 CAP-1 BeanShell 匿名接口捕获形参/局部变量（com.demo.captureprobe，API 34）

**探针**：`mian.iyu` 的 `loading` → `cap.boot()`，五项各建一个匿名回调，回调里直接读外层变量，
不带 `final`。

**原始读数**（用户控制台）：

```
CAP t1 tag=T1         # Thread(Runnable) 读局部 String
CAP t2 n=42           # runOnUiThread(Runnable) 读局部 int
CAP t3 who=T3-arg     # OnClickListener 读方法形参
CAP t4 size=2         # OnClickListener 读局部 ArrayList
CAP t5 sb=XY          # 回调创建后 sb.append("Y")，回调读到 XY → 按引用捕获
CAP done
```

**结论（✅ API 34）**：匿名接口回调可以捕获方法形参和局部变量，不需要 `final`；
对象按引用捕获。未覆盖：回调创建后重新赋值局部变量时的可见性（❓）。

---

## 2026-10-28 WATCH-1 iApp 打包 APK 在 OPPO Watch X2 上安装并运行（用户口述）

**探针**：无新探针。用户把 iApp 打包产物（同 `docs/artifacts/packaged.apk` 一类：4.7 MB、
minSdk 21 / targetSdk 36 / `lib/` 仅 `arm64-v8a`）侧载到 OPPO Watch X2 实机。

**原始读数**（用户口述，未取 logcat / screencap）：

```
安装：成功
启动：成功，界面能打开运行
```

**结论（⚠ 口述，未复测）**：
1. iApp 打包 APK 是自包含标准 APK，可以侧载到手表，**不需要在表上装 iApp 本体**。
2. 反推：该手表用户空间支持 `arm64-v8a`（APK 内原生库只有这一种 ABI）。
3. 待补读数：API 级、`abilist`、屏幕密度、圆屏裁切范围、桌面入口位置、表上 adb logcat 可用性
   —— 见 `docs/environments/oppo-watch-x2.md` §未测项。

## 2026-10-28 QJ-P7 原生底部抽屉（BottomSheetDialog）与可变参数调用

**探针 / 读数**：

```
# iApp 自带 dex 是否含 Material 抽屉类（pull base.apk 后按 dex 查字符串）
classes4.dex: bottomsheet/BottomSheetDialog, bottomsheet/BottomSheetBehavior, shape/MaterialShapeDrawable

# 抽屉内容里的骨架屏（ObjectAnimator 可变参数）
JavaErr: Static method ofFloat( android.widget.LinearLayout, java.lang.String, float, float )
         not found in class'android.animation.ObjectAnimator'
# 改法：ObjectAnimator.ofFloat(v, "alpha", new float[]{0.45f, 1f}) -> 正常
```

**结论（✅，API 34 / iApp 5.0.1013）**：
1. iApp 的 Material 是完整 AAR，`BottomSheetDialog` / `BottomSheetBehavior` / `MaterialShapeDrawable`
   都能在 mjava 里直接 `new`，不需要 build.xml 登记（登记只针对 `.iyu` 的 `type=`）。
2. 用 `new BottomSheetDialog(activity)` + `setContentView` 即得到原生模态抽屉：贴底、
   只圆上边两角、遮罩、下滑/外点关闭、`getBehavior().setState(STATE_EXPANDED)` 控制展开高度。
3. 想改抽屉底色而不丢圆角：`show()` 后取内容视图的 `getParent()`（= design_bottom_sheet），
   若背景是 `MaterialShapeDrawable` 就 `setFillColor(...)`，**不要** `setBackgroundColor`（会抹掉形状）。
   ⚠ 2026-10-28 修正：只有 `setFillColor(ColorStateList)` 重载，传 int 会闪退，见下面 QJ-P8。
4. 可变参数方法必须显式传数组，见 SKILL `mjava-guide` §调 Material / 框架的可变参数方法。

## 2026-10-28 QJ-P8 阅读设置面板：抽屉上色闪退、嵌套滚动、入口 import（API 34）

**探针 / 读数**（青简 `com.qingjian.reader`，mjava 源码即探针）：

```
# 1) 切纸色时闪退（setFillColor 传 int）
E/AndroidRuntime: FATAL EXCEPTION: main
E/AndroidRuntime: Process: com.iapp.app, PID: 2914
E/AndroidRuntime: java.lang.reflect.UndeclaredThrowableException
                 at $Proxy4.onClick(Unknown Source)
E/AndroidRuntime: Caused by: Error in method invocation:
                 Method setFillColor( int ) not found in class
                 'com.google.android.material.shape.MaterialShapeDrawable'
                 Called from method: set_put / set_click / onClick
W/System.err: java.lang.Exception: call killProcess callstack! pid=2914

# 2) 底栏翻页失效（跨模块方法没 import）
JavaErr: Command not found: set_css() : at Line: 132 : in file: inline evaluation of: qj_reader.mjava
         Called from method: reader_html : at Line: 260 … reader_render … reader_step … next
（只打印 JavaErr + 翻页无效，进程不崩）

# 3) 抽屉内滚动：ScrollView 往上拖会带关抽屉；换 NestedScrollView 后正常
（用户口述：往下滚可以，往回滚抽屉被拖走；替换后回滚正常、滚到顶才收起）
```

**结论（✅，API 34 / iApp 5.0.1013）**：
1. `MaterialShapeDrawable` 只有 `setFillColor(ColorStateList)`；传 int 报
   `Method setFillColor( int ) not found`，而 EvalError 在**匿名接口回调**里 `catch (Throwable)` 接不住，
   被包成 `UndeclaredThrowableException` 穿到点击分发 → iApp 杀进程。
2. 同一个 EvalError 出现在 iyu 事件直接 `call(...)` 的入口时只打印 `JavaErr`、中断本次调用，不崩。
   → UI 回调里禁止出现“方法可能不存在”的调用（同名重载、varargs、拼错）。
3. iyu 每次事件是新解释器：`prev/next` 只 `i.fn` 了 `qj_ui/qj_core/qj_store`，内部改调
   `qj_set.set_css()` 就 `Command not found`。每个入口必须自己 import；被多入口复用的方法在体内再 import 一次。
4. 抽屉内滚动要用 `androidx.core.widget.NestedScrollView`（`ScrollView` 不是 NestedScrollingChild，
   `BottomSheetBehavior` 感知不到内容位置，会抢走回滚手势）。
5. 抽屉底色要在首帧前刷：`setContentView()` 后、`show()` 前沿 `root.getParent()` 往上遍历刷
   `MaterialShapeDrawable.fillColor`；只在 `show()` 后刷会有一条白帧。
   本次同时确认：`show()` 刚返回时 `root.getParent()` 常常还不是圆角面板，
   所以上一版写成 int 的那行**从未执行**（这也是它当时没崩的原因）。

**产品改动（顺带记录，非探针）**：阅读页底栏 88dp → 56dp，只留上一页/页码/下一页；
新增 `qj_set.mjava`（原生 BottomSheetDialog 设置面板：字号/字间距/行距/字体/纸色/屏幕常亮 + 恢复默认）；
设置落盘 `filesDir/qingjian/settings.json`；默认值唯一来源 `qj_store.store_defaults()`；
点屏翻页区与「翻页方式」设置按用户要求移除（只保留底栏按钮）。

---

## 2026-10-28 WATCH-2 应用宝容器 → OPPO Watch X2 全链路（MD3 按钮 Demo）

**探针**：iApp 工程 `com.demo.watchdemo`（`mian.iyu` 单页 + `watch.mjava`）。
开发/打包在应用宝电脑版的 Android 容器内，工程经 iApp 内置 FTP 投递；APK 拉回宿主后用 adb 装表。

**设备读数**（`adb -s d96d6a4e`，2026-10-28）：

```
ro.product.model=OWW251  ro.product.brand=OPPO  ro.oplus.wear.oppo.product=true
ro.build.version.release=11   ro.build.version.sdk=30
ro.build.display.id=OWW251_11_A.265     security_patch=2024-03-05
ro.product.cpu.abilist=armeabi-v7a,armeabi   abilist64=（空）   ro.zygote=zygote32
/proc/cpuinfo: ARMv7 Processor rev 4 (v7l) x4   Hardware: Qualcomm MONACO
wm size: 466x466   wm density: 320   ro.sf.lcd_density=320
MemTotal: 1873636 kB   battery level=92 (USB powered)
id: uid=2000(shell)；su: inaccessible or not found
```

**FTP（iApp 服务器控制台）**：`ftp://172.22.44.17:9527`，匿名可登录，根含
`ProjectApp/ DownloadFileDir/ Userimg/ screenshot/ iyu-helpV*.txt`。
`ftp_sync.py` push 6/6 文件 `MD5` 全过（退出码 0）；`RETR` 可取回 `bin/<包名>.apk`。

**打包 ABI 对照**：

```
# 第 1 次：iApp 设置默认（只勾 arm64-v8a）
lib/arm64-v8a/libygsiyu.so        ELF class=2 machine=0xb7
lib/arm64-v8a/libluajava.so       ELF class=2 machine=0xb7
lib/arm64-v8a/libpl_droidsonroids_gif.so  ELF class=2 machine=0xb7
adb install → Failure [INSTALL_FAILED_NO_MATCHING_ABIS: Failed to extract native libraries, res=-113]

# 第 2 次：设置 →【打包设定so库】四项全勾
lib/{armeabi-v7a,arm64-v8a,x86,x86_64}/ 三个 .so 齐备
adb install -r → Success
```

**对照样本**：表上已装的 iApp 产物 `com.iuroc.watch`
（`primaryCpuAbi=armeabi-v7a`，`versionCode=100001`，`targetSdk=31`）是三架构包：
`armeabi-v7a` + `arm64-v8a` + `x86`，同样三个 `.so`。

**运行读数**（打包版，`android.util.Log` tag `watchdemo`）：

```
23:51:22.272 I/watchdemo(10378): init style=0
23:51:30.072 I/watchdemo(10378): pick count=1
...（共 34 次 pick，间隔 0.2~5s）
23:51:50.959 I/watchdemo(10378): style=1
23:51:53.938 I/watchdemo(10378): style=2
23:51:57.213 I/watchdemo(10378): style=3
23:52:01.701 I/watchdemo(10378): style=0
```

启动噪声（不影响运行）：

```
W/System.err: java.io.FileNotFoundException: userencryption.xml
  at android.content.res.AssetManager.nativeOpenAsset(Native Method)
  at com.iapp.app.run.iActivity.onCreate(...)
W/System.err: Caused by: java.lang.ClassNotFoundException: com.demo.watchdemo.IConfig
```

侧键（不是表冠，pid 10558）：

```
23:55:16.667 I/watchdemo(10558): key kc=132
23:55:23.732 I/watchdemo(10558): key kc=131
```

`131` = `KEYCODE_F1`、`132` = `KEYCODE_F2`；系统侧同时出现
`ComboKeyCtrl/ShortcutKeyCtrl interceptKeyBeforeQueueing keyCode: 131 / 138`。

**表冠不是按键**（`adb shell timeout 20 getevent -lt`，用户正反各转，2026-10-29）：

```
add device 1: /dev/input/event3
  name:     "oplus_crown"

[7374.133631] /dev/input/event3: EV_REL       REL_WHEEL            fffffff5   (-11)
[7374.149408] /dev/input/event3: EV_REL       REL_WHEEL            fffffffb   (-5)
[7374.165053] /dev/input/event3: EV_REL       REL_WHEEL            fffffffc   (-4)
...
```

统计：20 秒内 `EV_REL/REL_WHEEL` **307 次**，`SYN_REPORT` 307 次，
取值 `-15 … +24`（负值 1 个方向、正值另 1 个方向）；**`EV_KEY` 0 次**。
设备表里另有 `fts_ts`（触摸）、`qpnp_pon`、`gpio-keys`（侧键）。

对照：应用前台、屏幕常亮时转表冠，`downkey` **一次都不触发**（`watchdemo` 无 `key kc=` 日志）。

返回：用户按返回后 `ResumedActivity` 变为 `com.heytap.wearable.launcher/.Launcher`，
但 `pidof com.demo.watchdemo` 仍为 `10558`，任务栈里 activity 仍是 `paused`（未被 finish），
**没有 `key kc=4`**。系统日志同窗口出现
`NaviKeyCtrl: launch app from the single click ...` 与 `EditorInfoManager` 行。

息屏：`mWakefulness=Asleep`、`Display Power: state=OFF` 时
`pidof com.demo.watchdemo` 仍返回 `10378`。

截图（466×466 PNG）像素：背景 `#141218`、文字 `#D0BCFF`/`#CAC4D0`/`#938F99`，
与 ppt 声明一致；150dp 按钮实测 300px 宽 → density = 2.0。

**结论（✅，2026-10-28，API 30 / 应用宝容器打包）**：

1. 打包 APK 的 `lib/` 架构由 iApp 设置【打包设定so库】决定，**默认只勾 arm64-v8a**；
   纯 32 位用户空间设备需要勾上 `armeabi-v7a`，否则安装直接失败（`res=-113`）。
2. 应用宝容器内的 iApp 打包链路可用：FTP 推工程 → 容器内打包 → FTP 取回 APK → adb 装表。
3. 手表侧 adb `install` / `am start` / `logcat` / `screencap` / `pidof` 全部可用；无 root。
4. 打包版 `android.util.Log` 有输出（`ygs`/`i.syso` 本轮未验）。
5. 圆屏 466×466 / density 320：ppt 的 dp 值按 2.0 换算，`backgroundcolor` 与 `textcolor` 均生效。
6. **表冠不是按键**：`oplus_crown` 只发 `EV_REL/REL_WHEEL`（相对滚动，有负值），
   `downkey` 不触发；要用表冠必须接 `MotionEvent.ACTION_SCROLL` / `AXIS_SCROLL`。
   侧键才产生 `KEYCODE_F1(131)` / `F2(132)` / `F8(138)`。
7. 息屏后进程存活（短时观测，未测长时间/内存回收）。
8. 该表的「返回」走系统手势/侧键，**不向应用派发 `kc=4`**：应用被退到后台而非 finish，
   绑了 `downkey` 也拦不到；要保证退出得另找入口（见手表档案 §未测项）。
