# Spec Delta

## Purpose

让开发者在 `.iyu` 页面文件中看到事件结构，并从未必显眼的 `call` 字符串直接跳到对应 mjava 方法。

## ADDED Requirements

### Requirement: `.iyu` 作为独立语言被识别

扩展 SHALL 把 `.iyu` 注册为独立语言并提供高亮；`.iyu` 内容是近似 XML 的 iApp 页面格式，MUST NOT 按严格 XML 校验。

#### Scenario: 打开 iyu 文件

- **WHEN** 用户打开 `mian.iyu`
- **THEN** 编辑器使用 iyu 语言模式，`<View>`、`<ppt>`、`<UIEventset>` 与 `call` 语句可辨识
- **AND** 多个根 `<View>` 不产生 XML 结构错误

### Requirement: 页面与事件索引

扩展 SHALL 记录每个页面的视图、id、did、类型、全局事件表（`<UIEventset>`）中的事件类型，以及事件体中的 `call` 语句及其参数。

#### Scenario: 事件可枚举

- **WHEN** 打开包含 `loading`、`loadingComplete`、`resume` 三个事件的页面
- **THEN** 大纲或项目模型中能看到三个事件及各自的目标

### Requirement: 从 call 字符串跳转到 mjava 方法

对事件体中的 `call(<接收>, "mjava", "<模块>.<方法>", ...)`，扩展 SHALL 解析模块与方法名，并在对应 mjava 模块中定位方法声明；参数个数 SHALL 一并记录，供后续校验使用。

#### Scenario: 入口跳转

- **WHEN** 用户对 `call(null, "mjava", "home.first")` 中的 `"home.first"` 触发“转到定义”
- **THEN** 打开 `home.mjava` 并定位到 `first` 方法

#### Scenario: 带参数入口

- **WHEN** 事件调用 `call(null, "mjava", "reader.key", st_kC)`
- **THEN** 跳转到 `reader.mjava` 的 `key` 方法，并记录实参个数为 1

#### Scenario: 目标不存在

- **WHEN** 字符串指向工程中不存在的模块或方法
- **THEN** “转到定义”返回空结果，由诊断报告问题，不打开无关文件

### Requirement: call 目标的 Hover

扩展 SHALL 在 `"模块.方法"` 字符串上显示 Hover，包含目标模块、方法签名与实参个数。

#### Scenario: Hover 目标

- **WHEN** 用户悬停在 `"home.first"` 上
- **THEN** 显示目标为 `home.first`，并给出声明签名（当可解析时）

### Requirement: iyu 大纲

扩展 SHALL 为 `.iyu` 文件提供文档大纲，按 `UIEventset` 的事件类型分组列出 `call` 目标；当页面包含视图时，SHALL 同时列出视图 id 与类型。

#### Scenario: 大纲展示事件

- **WHEN** 用户查看 `mian.iyu` 大纲
- **THEN** 看到 `loading -> home.first`、`loadingComplete -> home.second`、`resume -> home.again`

### Requirement: 标签与属性提示

扩展 SHALL 为 `View`、`ppt`、`event`、`UIEventset`、`eventItme` 提供标签名与属性名的 Hover 说明；SHALL 在输入 `<`、`</` 时补全标签名，并在 `View` 标签内补全 `id`/`did`/`type`、在 `eventItme` 标签内补全 `type`。字符串与注释内 MUST NOT 触发标签补全。

#### Scenario: 标签 Hover

- **WHEN** 用户悬停 `<eventItme>` 的标签名
- **THEN** 显示这是单个事件入口、`type` 属性与事件体只允许 `call`/`addv`

#### Scenario: 标签补全

- **WHEN** 用户在行首输入 `<`
- **THEN** 候选列出 `View`、`ppt`、`event`、`UIEventset`、`eventItme`

#### Scenario: 属性补全

- **WHEN** 用户在 `<View ` 后输入
- **THEN** 候选列出 `id`、`did`、`type`，并跳过已经写过的属性

### Requirement: 入口目标的引用查找

扩展 SHALL 允许在 iyu 的 `"模块.方法"` 字符串上查找引用，列出所有指向同一方法的 mjava 调用与其它 iyu 入口。

#### Scenario: 从入口字符串查找引用

- **WHEN** 用户对 `"home.first"` 触发“查找所有引用”
- **THEN** 结果包含 `misc.mjava` 的显式调用与 `mian.iyu` 的其它入口
