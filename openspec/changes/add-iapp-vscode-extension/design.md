# Design

## Context

- `.mjava` 是 BeanShell 解释的 Java 子集：没有 `class` 外壳、顶部可写 `import`、方法直接定义在文件里；模块名就是文件名。
- `.iyu` 是近似 XML 的页面格式：多个根 `<View>`、事件标签实际拼写为 `eventItme`、事件体是裕语言。
- 模块加载是运行期行为：`i.fn("mod")` 把模块导入当前解释器；iyu 每个事件都是新解释器，必须在事件入口重新加载。
- 方法命名有两套：模块前缀（`ui_`、`wg_`、`book_`）与入口方法（`first`、`second`、`again`、`key`、`back`）；入口方法在不同模块重名。
- 工作区现有 50 个 `.mjava`、21 个 `.iyu`；import 以 Android/AndroidX/Material 为主。
- 本机有 JDK 25 的 `lib/src.zip`（51 MB），没有 Android SDK sources，也没装 `redhat.java`；Node 24 可用。

动机见 `proposal.md` §Why；行为契约见 `specs/`。

## Goals / Non-Goals

**Goals:**

- 在编辑器内完成 iApp 符号（模块、方法、页面）与 Java 符号（JDK/Android 类、成员）的统一导航。
- 在无 Java 语言服务器、无编译器的前提下，用索引与轻量类型推断覆盖绝大多数静态写法。
- 对动态加载、反射、无法推断的写法明确降级，不制造错误跳转。
- lint 规则与现有 `check_mjava.py` 保持可对照的判定口径。

**Non-Goals:**

- 不做编译器/执行器，不替代设备实跑。
- 不做 javac/JDT 级别的完整类型系统；泛型与重载只做近似。
- 不做重命名、格式化、自动修复。
- v1 不发布 Marketplace，不承诺跨编辑器复用。

## Decisions

### D1. 普通 VS Code 扩展 + 直接 Provider，而不是 LSP 服务器

第一版用 VS Code 原生 Provider（Definition/Hover/DocumentSymbol/Diagnostic/TreeView），核心逻辑放纯 TS 的 `core/`，与 VS Code API 隔离。

- 备选：LSP 服务器。可复用、边界干净，但需要额外进程/传输/打包，第一版收益不抵成本。
- 备选：桥接 `redhat.java`。公开入口只有 `java.execute.workspaceCommand`、`java.project.resolveWorkspaceSymbol` 一类命令，没有“按 FQN 返回定义”的稳定契约，且本机未安装；不作为主路径。
- 以后要 LSP，只需在 `core/` 外包一层，不改解析与索引。

### D2. mjava 用 `@lezer/java` 包裹解析

做法：

1. 提取文件顶部的 `import` 语句。
2. 把原文件中的 import 行替换成空行，保持行号。
3. 生成 `import ...; class __IAppWrap { <去 import 原文> }`。
4. 用 `@lezer/java` 解析，得到一个 Java 语法树。
5. 记录“合成行 → 原文件行”的映射，所有范围回映射。

- 选它而不是 `tree-sitter-java`：纯 JS、解包约 222 KB、无 native/WASM 加载；mjava 是合法 Java 子集，包裹后语法够用。
- 备选：tree-sitter WASM。解析更宽容，但多一层 WASM 加载与打包。
- 备选：手写扫描器。快，但取参数类型、返回类型、匿名类作用域会越来越难维护。
- BeanShell 私有写法（`imports("...")`）是普通调用，不影响语法树；真正会解析失败的写法（`final`、`->`、`...`）本来就是要报错的。

### D3. iyu 用容错行解析器，不用 XML 解析器

按行识别 `<View ...>`、`<ppt>...</ppt>`、`<event>...</event>`、`</View>`、`<UIEventset>`、`<eventItme type="...">`；事件体用括号/字符串感知的扫描器提取 `call(...)`/`addv(...)` 语句与范围。

- 备选：XML 解析。多根节点、`eventItme` 拼写、事件体里的裕语言都会让严格解析失败；包一层 synthetic root 也只能解决多根，解决不了正文。
- 行解析器还能精确报告 `key = value` 空格、事件体行尾注释这类“格式对但语义失效”的问题。

### D4. 索引以 iApp 工程为界

- 工程识别：目录含 `AndroidManifest.xml` 且根元素为 `<iapp>`，或含 `src/mian.iyu`。
- 模块名 = 文件名去 `.mjava`；页面名 = 文件名去 `.iyu`。
- 工作区多工程时，每个工程维护独立索引；同名模块/页面不跨工程解析。
- 文件监听采用保存触发 + 增量重解析；新增/删除文件时重建工程清单。

### D5. 裸方法调用按“本模块 → 加载集 → 全局唯一 → 候选”解析

- 当前模块：同名 + 参数个数匹配。
- 加载集：从当前函数或 iyu 事件入口出发，收集可达函数中的 `i.fn` 调用；这是过近似，不区分 `i.fn` 与调用点的先后。
- 全局唯一：整个工程只有一个同名方法时直接跳。
- 否则返回全部候选，由 Peek 选择；不猜。
- 对 `i.call("mjava", "mod.method", ...)` 与 iyu 字符串这类显式限定名，直接按模块解析，不走上面的顺序。

### D6. 轻量类型推断

只为“接收者 → 类型”服务，规则保持可解释：

- 局部变量：`Type name = expr;` / `Type name;`。
- 形参、for-each 变量、catch 参数、匿名类/回调参数。
- 表达式：`new X(...)`、`(X) expr`、`this`/`super`、字符串拼接、数组访问、三元表达式。
- 方法调用：用 mjava 索引或 Java 索引的返回类型。
- 字段访问：用 Java 索引的字段类型。
- `activity` 固定为 `android.app.Activity`；`i` 固定为 stub 类型 `Aid_javaCode`。
- 推断不出来就标记 unknown；成员跳转返回空或类内候选，不猜。
- 泛型先按原始类型处理；`ArrayList<String>.get` 这类会退化为 `Object`，列为已知限制。

### D7. Java 源码索引：类名映射 + 按需解析

- 类级：读取 zip/jar 的 entry 列表，把路径规范化为 FQCN，建立 `FQCN -> 文件`。
  - JDK `src.zip` 的 entry 形如 `java.base/java/lang/String.java`，去掉模块段。
  - Android sources 与 AndroidX/Material sources 按包路径映射；解析文件内的 `package` 声明做校验。
- 成员级：第一次需要某个类时解析该文件，提取 package、import、类/嵌套类声明、`extends`/`implements`、方法、字段、范围与 javadoc；结果缓存。
- 继承：解析 `extends`/`implements` 名字时按 import、同包、`java.lang.*`、全限定名依次尝试；沿父类/接口向上找成员。
- 重载：按名字 + 实参个数筛选；多个候选全部返回，能按实参类型收窄时再收窄。
- 备选：javac/JDT 语义后端。准确，但需要合成 Java 工程、Java 辅助进程、Android 类路径，与“第一版轻量索引”的约束冲突；保留为后续升级路径。
- 备选：只索引 `android.jar`。没有源码行与 javadoc，跳转体验明显下降；作为没有 sources 时的降级。

### D8. iApp 私有 API 用手写 stub

- `i` → `Aid_javaCode`，方法表来自工作区 `iapp-i-reference.md` 与现有代码实际用到的调用。
- `activity` → `android.app.Activity`（Android 源码索引覆盖）。
- stub 以只读虚拟文档或内置 `.d.ts` 形式提供，用于 Hover/跳转/补全；不参与用户工程索引。
- 以后需要更准的签名，再从设备 `base.apk` 抽 dex；第一版不做。

### D9. 源码安装与缓存

- 优先本地：`iapp.jdkHome`、`JAVA_HOME`、常见 JDK 路径；Android 侧读 `ANDROID_HOME`/`ANDROID_SDK_ROOT` 或用户指定目录。
- 缺少 Android sources 时提供显式安装命令：提示约 48 MB（`sources-34` 45.5 MB + AndroidX/Material sources 约 2.2 MB），确认后下载到 `context.globalStorageUri`，不写入工程目录。
- 允许取消；取消后 JDK 功能仍可用，Android 跳转返回空，lint 不把未解析的 Android 引用报成错误。
- 索引缓存放内存 + global storage；源码文件未变化不重复解析。

### D10. 诊断引擎与规则集

- 规则集移植 `check_mjava.py` 的八条致命写法，并补充未定义目标、先加载后调用、iyu 书写规则、参数个数、重名覆盖。
- 严重级别：解析期致命 → error；运行期可能静默失败 → warning；覆盖/冗余 → info。
- 动态写法、反射、无法展开的加载 → 不报错，最多提示。
- 抑制：支持行内标记（与 `# noqa` 等价）与设置项开关；被抑制的诊断不进 Problems。
- 注释与字符串内容在规则匹配前排除，避免 `// final`、字符串里的 `->` 误报。

### D11. 打包与发布

- TypeScript + esbuild 打包成单文件扩展；`@lezer/java` 纯 JS 直接 bundle。
- `package.json` 贡献：语言、语法、命令、视图、配置。
- 产物为 VSIX，本地安装；不发布 Marketplace。

### D12. 测试策略

- 单元测试：用工作区工程做夹具，覆盖方法计数、重名入口、`i.fn` 加载集、iyu 事件解析、参数个数。
- 导航金样：对固定位置断言“跳转到哪个文件/行”。
- 集成测试：Extension Development Host 打开夹具工程，调用 Definition/Hover/Diagnostics。
- 性能冒烟：50 个 mjava 的索引时间、首次/二次成员跳转延迟。
- 与 `check_mjava.py` 做对照测试，保证同一输入下命中集合一致。

### D13. 引用查找复用解析器与类型推断

- 方法身份用「模块名 + 声明行列」锚定，避免重名入口混淆。
- iApp 引用来源：裸调用按 D5 的解析顺序、`i.call` 显式限定名、iyu `call` 入口；Java 成员则要求接收者类型可推断，并匹配声明类 + 方法名 + 参数个数。
- 重名或无法消歧时返回候选并集；接收者未知时不返回该调用，不伪造引用。
- 引用扫描以当前工程模型为界，工程隔离与导航一致。

### D14. 补全共用索引与类型推断

- 补全核心返回纯候选（标签、签名、文档、插入文本、排序组），Provider 只做上下文识别与 `CompletionItem` 映射，保持可单测。
- mjava 成员接收者先用词法扫描提取表达式，再交给 `MjavaTypeInference`；Java 成员表由 `listMembers` 沿继承链收集并去重。
- 字符串补全按行前缀识别 `i.fn`/`i.uigo`/`i.call` 与 iyu `eventItme`/`call`，避免未闭合字符串时解析器拿不到调用节点。
- 未知接收者、注释内、无法消歧时不返回候选；不做实参类型过滤、自动 import 与全量类名模糊搜索。

### D15. 方法注释按声明邻接提取

- 统一 `docCommentBefore`：从声明起始行向上看，允许最多两个空行，再取 `/** ... */` 或连续 `//` 块；纯分隔线注释（`----------` 占比高）视为分节标题，不挂到声明。
- `/** */` 去掉每行 `*` 前缀、保留段落与 `@param`/`@return` 标签；`//` 去掉行首标记后按行合并。
- mjava 与 Java 源码共用同一提取器，Hover 与补全说明直接使用提取结果。
- 注释渲染走 `appendText` 逐行输出并插入硬换行：保留原始折行，避免 `---`、`*`、单换行被 Markdown 重新排版；签名与元信息仍用 Markdown。

### D16. 变量定位用词法作用域近似

- 标识符扫描跳过字符串、注释、注解与关键字；`obj.name` 记为成员访问，`name(` 记为调用，只有裸标识符参与变量解析。
- 解析顺序：当前方法中光标前最近声明的局部变量 → 形参 → 模块字段；循环变量与 catch 参数并入局部变量表。
- 引用范围：局部变量/形参限定在方法范围，字段扫描整个模块；每次出现都重新按位置解析，用于处理同名变量。
- 不建立完整词法作用域树：匿名类内部同名变量按外层方法近似，跨模块字段引用不扫描。

### D17. 模块文件注释取首段连续注释

- 文件说明只取开头第一个连续注释块：跳过开头空行，收集连续 `//` 行；或收集一个 `/** */`/`/* */` 块，后接无空行分隔的 `//` 行。
- 空行截断；只有 `//` 的空注释行仍属于同一块。避免把“标题 + 空行 + 另一段说明”误合并。
- 解析结果挂在 `MjavaFile.documentation`，由模块 Hover、模块补全与工程树 tooltip 复用。

## Risks / Trade-offs

- **mjava 包裹后解析不稳** → 先做 spike；若 Lezer 在 import 行或 BeanShell 写法上恢复失败，退回“保留 import 在合成文件顶部 + 逐行映射”的方案，或对手写扫描器做局部兜底。
- **类型推断覆盖不到动态写法** → 明确 unknown，跳转返回空/候选；lint 不把 unknown 当错误。
- **Android 源码版本与 iApp 运行时不一致** → 第一版用官方 API 34 + 常见 AndroidX/Material 版本；版本敏感的诊断标 ⚠，允许用户覆盖源码路径；后续可从 APK 抽实际版本。
- **入口方法重名导致误跳** → 解析顺序优先加载集；仍无法确定时返回候选，不猜。
- **加载集是过近似** → 可能漏报“先加载后调用”，但不会误报；精确流分析留到后续。
- **首次成员跳转有解析延迟** → 按需解析 + 缓存；只解析目标类及其继承链。
- **iApp 私有 API stub 不全** → 先覆盖实际用到的 `i.fn`/`i.sss`/`i.syso`/`i.uigo`/`i.us`，其余按文档补；未知方法返回空，不报错。
- **源码分发许可** → 不随扩展分发 Android/JDK 源码，只读取本地文件或在用户确认后下载。

## Migration Plan

- 新工程，不改既有 iApp 工程、投递链路与运行时。
- 以 VSIX 安装；卸载即回滚，索引与缓存在 global storage，可单独清理。
- `check_mjava.py` 继续保留为无编辑器时的兜底；扩展 lint 与脚本做对照测试，先并行再决定是否收敛。

## Open Questions

- 扩展仓库放在独立仓库还是本工作区 `extensions/iapp-vscode/`，不影响 specs 与架构，可在实现前定。
- iApp 实际打包的 AndroidX/Material 版本未知；第一版用官方版本并在诊断上标注版本敏感，后续从设备 APK 读取。
- 是否在 v1 就提供 `i.*` 与模块方法的补全，属于 P1，可按实现进度取舍。
- 是否对外暴露 `ProjectModel` 的 JSON 命令，属于可延后的集成需求。
