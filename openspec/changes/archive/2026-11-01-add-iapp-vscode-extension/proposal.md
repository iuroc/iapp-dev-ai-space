# Proposal

## Why

mjava 与 iyu 都不是标准 Java/XML：mjava 没有 `class` 外壳、由 BeanShell 解释，iyu 不是严格 XML、事件体是裕语言。
今天在这些文件里找方法只能靠 grep，跨模块调用是否写对要到设备上跑一次才知道；查 JDK/Android API 又得离开编辑器。
现有 `check_mjava.py` 只能手动在终端跑，解决不了「写的时候就知道」。

## What Changes

- 新增一个 VS Code 扩展（TypeScript），面向本工作区的 iApp 工程：
  - 注册 `.mjava` / `.iyu` 语言并提供语法高亮。
  - 以 `AndroidManifest.xml` 为界建立工程级索引：模块、方法、页面、事件、import、`i.fn` 加载关系。
  - 提供方法定义跳转：iyu 字符串入口 → mjava 方法、mjava 裸调用 → 模块方法、`i.fn`/`uigo` → 模块/页面文件。
  - 复用 JDK `src.zip` 与 Android 官方源码索引，支持类名与可推断成员跳转到 JDK/Android 源码。
  - 提供 Hover、大纲、项目 TreeView、lint 诊断。
  - 提供补全：工程方法与模块/页面字符串、`i.*` 成员、可推断接收者的 Java 成员、iyu 事件与入口目标。
- Java 源码索引按需构建：优先使用本地 JDK/Android SDK；缺失时提供一次性的、明确体积的下载选项。
- 不修改任何既有 iApp 工程、投递链路或运行时行为。

## Capabilities

### New Capabilities

- `mjava-navigation`: 解析 mjava 模块，建立方法/模块/调用索引，提供定义跳转、Hover 与大纲；处理 `i.fn` 动态加载下的跨模块消歧。
- `iyu-navigation`: 解析 iyu 页面与事件表，从 `call(..., "mjava", "mod.method")` 跳到目标方法，提供 Hover 与大纲。
- `java-symbol-index`: 从 JDK `src.zip` 与 Android 源码构建按需索引，解析类、继承链、方法与 javadoc，供 mjava 跳转复用。
- `iapp-project-model`: 识别 iApp 工程，汇总模块、页面、入口事件、方法计数与加载关系，在 TreeView 中展示。
- `iapp-lint`: 对 mjava 与 iyu 提供诊断，覆盖会导致模块失效或运行期静默失败的写法。
- `iapp-completion`: 复用工程索引与 Java 类型推断，为 mjava/iyu 提供上下文补全。

### Modified Capabilities

（无）

## Impact

- 新增独立工程（建议独立 git 仓库，或本工作区 `extensions/iapp-vscode/`）；不进入 `project/`。
- 新增依赖：`@lezer/java`（纯 JS 解析）、zip 读取库；不引入 Java 运行时。
- 读取本机 JDK `lib/src.zip` 与可选的 Android 源码目录；首次可选下载约 48 MB（Android `sources-34` 约 45.5 MB + AndroidX/Material sources 约 2.2 MB）。
- 不影响 iApp 工程的源码结构、打包产物与设备投递。

## Non-goals

- 不做编译器或执行器，不替代设备上的实跑。
- 不引入 javac/JDT 级别的完整语义分析；成员解析允许在动态写法上退化。
- 不做重命名、格式化、自动修复。
- v1 不发布到 VS Code Marketplace。
