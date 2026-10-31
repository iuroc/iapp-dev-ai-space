# Tasks

## 1. 工程骨架与风险验证

- [x] 1.1 在 `extensions/iapp-vscode/` 建 TypeScript 扩展骨架（`package.json`、`tsconfig.json`、esbuild 配置、`.gitignore`、`README.md`），验证 `npm install` 与 `npm run compile` 成功，且 `code --extensionDevelopmentPath=extensions/iapp-vscode` 能打开 Extension Development Host
- [x] 1.2 加入 `@lezer/java` 与 zip 读取依赖，验证打包产物只包含纯 JS 依赖、无 native 模块，并记录 bundle 体积
- [x] 1.3 Spike：对含 import、普通方法、匿名 `Runnable`、强转的 mjava 夹具做“提取 import + 包一层 class”解析，验证方法/参数/返回类型的范围能准确映射回原文件行号
- [x] 1.4 Spike：检查 JDK `src.zip` 与 Android sources 的 entry 结构，建立并验证 `java.util.ArrayList`、`android.widget.TextView` 两个类名映射；没有 Android sources 时先用夹具目录验证同一套索引器
- [x] 1.5 在 `extensions/iapp-vscode/` 初始化独立 git 仓库，并把 `/extensions/` 加入工作区 `.gitignore`，验证 `git status` 不把嵌套仓库当成普通目录

## 2. 语言注册与高亮

- [x] 2.1 在 `package.json` 注册 `mjava`、`iyu` 两个语言与 `.mjava`/`.iyu` 扩展名，验证打开文件时状态栏语言模式正确
- [x] 2.2 为 mjava 提供 TextMate 语法（Java 语法基础上放宽顶层方法/import），验证关键字、字符串、注释、数值字面量在 EDH 中着色正确
- [x] 2.3 为 iyu 提供 TextMate 语法，验证 `<View>`、`<ppt>`、`<UIEventset>`、`call` 与注释可辨识，且多根 `<View>` 不出现结构错误
- [x] 2.4 为两种语言补语言配置（括号、注释、自动闭合），验证编辑时注释切换与括号匹配正常
- [x] 2.5 为两种语言各加一个语法夹具测试并写明 README 的语言支持范围，验证测试通过

## 3. 工程识别与索引

- [x] 3.1 实现工程识别（`AndroidManifest.xml` 根为 `<iapp>` 或 `src/mian.iyu`），验证 `project/com.jianyue.reader` 被识别、普通临时目录不被识别
- [x] 3.2 实现 mjava 解析器，提取模块名、import、方法（名称/参数/返回类型/可见性/范围）与顶层变量；对工作区全部 `.mjava` 跑夹具测试，验证无解析失败且方法总数符合预期
- [x] 3.3 实现 iyu 容错解析器，提取视图、id、did、type、事件类型、`call` 语句与范围；对工作区全部 `.iyu` 跑夹具测试，验证页面/事件数符合预期
- [x] 3.4 建立 `ProjectModel`：模块、页面、方法、import、`i.fn` 加载边、iyu 入口边；验证 `com.jianyue.reader` 得到 23 个模块、8 个页面、约 488 个方法
- [x] 3.5 实现文件监听与增量重解析，验证新增/修改/删除 `.mjava` 或 `.iyu` 后模型在不需要重载窗口的情况下更新
- [x] 3.6 用两个都含 `ui.mjava` 的夹具工程验证工程隔离，确认 A 工程的跳转不会落到 B 工程
- [x] 3.7 在扩展 README 记录项目模型字段与刷新规则，验证文档中的字段名与实现一致

## 4. iApp 导航

- [x] 4.1 实现方法索引与裸调用解析顺序（本模块 → 加载集 → 全局唯一 → 候选），单元测试覆盖同模块、已加载模块、重名入口、无法消歧四种情况
- [x] 4.2 实现 iyu `call` 字符串解析与目标解析，测试覆盖 `home.first`、带参数的 `reader.key`、目标不存在
- [x] 4.3 实现 `i.fn("mod")` 与 `i.uigo("page.iyu")` 路径跳转，测试覆盖带/不带 `.iyu` 扩展名
- [x] 4.4 接入 DefinitionProvider，在 EDH 中对 `lib_wire()`、`i.fn("ui")`、`"home.first"`、`uigo("search.iyu")` 各验证一次跳转
- [x] 4.5 实现 mjava/iyu Hover，显示签名、所属模块、实参个数；单元测试断言文本，EDH 抽检两处
- [x] 4.6 实现 mjava/iyu DocumentSymbol，验证大纲能列出方法、顶层变量、事件与 `call` 目标
- [x] 4.7 写导航使用说明（含重名方法与候选列表的预期行为），验证文档里的示例在当前工作区可复现
- [x] 4.8 加一组“固定位置 → 预期文件/行”的导航金样测试，验证改动解析器后不会悄悄跑偏

## 5. Java 索引与类型推断

- [x] 5.1 实现 zip/jar entry 到 FQCN 的类级索引，单元测试验证 JDK、Android、AndroidX 三类路径都能映射
- [x] 5.2 实现源码懒解析：package、import、类/嵌套类、`extends`/`implements`、方法、字段、范围、javadoc；用 `String` 与 `TextView` 夹具验证
- [x] 5.3 实现继承解析，测试 `TextView` 实例上的 `getId` 能落到 `View.getId`，接口方法也能定位
- [x] 5.4 实现成员重载筛选，测试同参数个数的多个 `setText` 返回候选而非随机选一个
- [x] 5.5 实现轻量类型推断（局部变量、形参、`new`、强转、方法返回类型、字段、字符串拼接、数组），单元测试覆盖可推断与 unknown 两类
- [x] 5.6 接入 Java 类/成员 Definition 跳转，在 EDH 中验证 `TextView`、`TextView.setText`、`ArrayList.add`、`activity.getResources()` 四处
- [x] 5.7 接入 Java Hover，验证 Android 源码的 javadoc 摘要能显示；源码缺失时返回空而不是报错
- [x] 5.8 加入 `i`（`Aid_javaCode`）与 `activity` 的 stub，验证 `i.fn`、`i.sss`、`activity.finish()` 的 Hover/跳转可用
- [x] 5.9 在 README 记录源码配置项与类型推断限制（泛型退化、动态写法返回空），验证文档与设置项名称一致

## 6. 诊断

- [x] 6.1 实现 mjava 八条致命写法诊断，与 `check_mjava.py` 对同一批工作区文件做对照测试，验证命中集合一致
- [x] 6.2 实现未定义目标诊断（`i.fn` 模块、带前缀方法、iyu 入口、`uigo` 页面），每类至少一个测试
- [x] 6.3 实现“先加载后调用”警告，测试覆盖“调用链缺 `i.fn`”与“动态加载无法静态展开”两种情况，后者必须不报
- [x] 6.4 实现 iyu 书写规则诊断（白名单、事件体行尾注释、`ppt` 空格、重复 id），每类至少一个测试
- [x] 6.5 实现参数个数与重名覆盖诊断，测试覆盖 iyu 入口实参不匹配、两个模块同名方法被先后加载
- [x] 6.6 实现抑制标记与 lint 总开关，测试验证被抑制项不出现在诊断集合中
- [x] 6.7 接入 DiagnosticCollection 与保存防抖，在 EDH 中打开 `com.jianyue.reader` 验证 Problems 面板有预期结果、无整屏误报
- [x] 6.8 在 README 列出规则 ID、严重级别与抑制写法，验证文档表格与实现一致

## 7. 项目 TreeView

- [x] 7.1 实现 TreeDataProvider，展示工程 → 模块/页面 → 方法/入口，验证 `com.jianyue.reader` 的节点数量与模型一致
- [x] 7.2 实现节点点击跳转，验证点击 `home.first` 打开 `home.mjava` 并定位到方法
- [x] 7.3 实现文件变化后的刷新，验证新增模块后 TreeView 自动出现
- [x] 7.4 为树模型加单元测试并写项目视图说明，验证文档中的节点路径可点击复现

## 8. 源码安装与配置

- [x] 8.1 实现 `jdkHome`、`androidSources`、`extraSourceJars` 设置与常见路径自动探测，测试覆盖“找到/找不到”两种结果
- [x] 8.2 实现 Android 源码安装命令：显示约 48 MB 体积、要求确认、支持取消、缓存到 global storage；用 mock 下载验证流程，再手测一次真实下载
- [x] 8.3 实现索引不可用时的降级：Android 源码缺失时 `TextView` 跳转返回空、lint 不报未解析 Java 引用；单元测试覆盖
- [x] 8.4 在 README 写安装、离线使用与缓存清理步骤，验证按文档操作能回到 JDK-only 状态

## 9. 打包与集成验收

- [x] 9.1 用 `vsce package` 打出 VSIX，在干净 VS Code 配置中安装并验证扩展激活、语言注册与命令可见
- [x] 9.2 在 `com.jianyue.reader` 与一个 watch 工程上跑完整验收：定义跳转、Hover、大纲、诊断、TreeView 各抽检至少两处
- [x] 9.3 性能冒烟：记录 50 个 mjava 的首次索引耗时、首次成员跳转耗时与二次跳转耗时，确认首次索引不超过 3 秒、二次成员跳转不超过 50 ms（本机基线）
- [x] 9.4 补扩展 README、CHANGELOG 与工作区根 README 索引，运行 `python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on blocker`（默认包含 portable 检查）或单独运行 `python .claude/skills/iapp-development/scripts/check_portable.py` 验证通过
- [x] 9.5 做一轮代码质量检查（复用、死代码、样式一致性），确认没有阻断项后再交付

## 10. 方法引用查找

- [x] 10.1 实现 iApp 方法引用核心（mjava 裸调用、`i.call`、iyu 入口），单元测试断言文件/行
- [x] 10.2 实现 Java 成员引用（接收者类型 → 声明类/方法/参数个数匹配），用夹具工程测试
- [x] 10.3 接入 ReferenceProvider，覆盖方法声明、裸调用、iyu 入口与 `setText`
- [x] 10.4 更新 README 与 CHANGELOG 的引用查找说明

## 11. 补全

- [x] 11.1 实现 mjava 方法/模块/页面/限定方法候选与排序，单元测试覆盖当前模块、加载集、全局与字符串前缀
- [x] 11.2 实现 `listMembers` 继承成员表与接收者表达式提取，测试覆盖 `tv.`、链式调用、`new`、强转与未知接收者
- [x] 11.3 实现 `i.` 内置成员与 iyu 事件类型/`call` 目标补全，测试候选内容
- [x] 11.4 接入 CompletionItemProvider：触发字符、字符串范围替换、snippet 与已有括号降级
- [x] 11.5 补 README/CHANGELOG，跑全量测试并在 EDH 抽检 `i.`、`tv.` 与 iyu 补全

## 12. 方法注释

- [x] 12.1 实现统一的声明邻接注释提取：`/** ... */`、连续 `//`、空行分节不挂载；mjava 与 Java 源码共用
- [x] 12.2 接入 Hover 与补全说明，测试覆盖块注释、行注释、标签行、空行分隔与真实工程注释
- [x] 12.3 更新 README/CHANGELOG，打包并在 EDH 抽检 `ui_versionText` 的 Hover

## 13. 变量定位与引用

- [x] 13.1 实现标识符扫描与变量解析：局部变量、形参、模块字段、循环变量、catch 变量
- [x] 13.2 实现变量引用查找与方法内/模块范围划分，排除成员名、方法名、字符串与注释
- [x] 13.3 接入 Definition/Hover/Reference Provider，并补变量补全
- [x] 13.4 用 `home.mjava` 的 `body.addView(ui_text(hints[idx], 15, th_ink2()))` 金样验证，更新 README/CHANGELOG

## 14. 模块文件注释

- [x] 14.1 实现文件开头首段连续注释提取：`//`、`/** */`、`/* */`，空行截断，允许开头空行
- [x] 14.2 接入 `MjavaFile.documentation`、模块 Hover、模块补全说明与工程树 tooltip
- [x] 14.3 测试覆盖连续行、空注释行、空行截断、块注释与真实工程 `mine.mjava`，更新 README/CHANGELOG
