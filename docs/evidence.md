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
