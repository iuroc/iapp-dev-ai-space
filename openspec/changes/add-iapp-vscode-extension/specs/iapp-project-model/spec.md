# Spec Delta

## Purpose

识别一个目录是否属于 iApp 工程，并把模块、页面、入口事件和加载关系汇总成可浏览的项目信息。

## ADDED Requirements

### Requirement: 工程识别

扩展 SHALL 把包含 `AndroidManifest.xml`（根元素为 `<iapp>`）或 `src/mian.iyu` 的目录识别为一个 iApp 工程；索引范围 MUST 以该工程根为界。

#### Scenario: 识别工程

- **WHEN** 工作区包含 `com.jianyue.reader/AndroidManifest.xml`
- **THEN** 该目录被识别为一个工程，`src/` 下的 mjava 与 iyu 被纳入索引

#### Scenario: 非工程目录

- **WHEN** 目录下既没有 iApp manifest 也没有 `src/mian.iyu`
- **THEN** 不建立工程索引

### Requirement: 清单信息

扩展 SHALL 从 `AndroidManifest.xml` 读取并展示包名、应用名、版本、目标 sdk 与权限列表。

#### Scenario: 展示清单

- **WHEN** 用户查看工程信息
- **THEN** 能看到 `packageName`、`title`、`sdk` 与权限列表

### Requirement: 模块与页面清单

扩展 SHALL 列出工程内全部模块及其方法数，以及全部页面及其事件入口；无法解析的入口 SHALL 在项目信息中标记为异常。

#### Scenario: 模块清单

- **WHEN** 工程有 23 个 mjava 模块
- **THEN** 项目信息列出 23 个模块及各自方法数

#### Scenario: 页面清单

- **WHEN** 工程有 8 个 iyu 页面
- **THEN** 项目信息列出 8 个页面及其事件入口

### Requirement: 加载与调用关系

扩展 SHALL 汇总 `i.fn` 形成的模块加载边，以及 iyu 事件到 mjava 方法的入口边；这些关系 SHALL 可用于导航和后续诊断。

#### Scenario: 加载边

- **WHEN** `lib.mjava` 中调用 `i.fn("ui")`
- **THEN** 项目信息中出现 `lib -> ui` 的加载关系

#### Scenario: 入口边

- **WHEN** `mian.iyu` 的 `loading` 事件调用 `home.first`
- **THEN** 项目信息中出现 `mian.iyu -> home.first` 的入口关系

### Requirement: 工程隔离

同名模块或页面在不同工程中 SHALL 被视为不同符号；跨工程 MUST NOT 互相解析或产生歧义提示。

#### Scenario: 两个工程都有 ui.mjava

- **WHEN** 工作区同时打开两个工程，且都包含 `ui.mjava`
- **THEN** 在 A 工程内的跳转只解析 A 的 `ui.mjava`

### Requirement: TreeView 展示

扩展 SHALL 以树形视图展示工程、模块、页面与入口，节点可点击跳转到对应文件或方法，并在文件变化后刷新。

#### Scenario: 点击节点

- **WHEN** 用户点击 TreeView 中的 `home.first`
- **THEN** 编辑器打开 `home.mjava` 并定位到 `first`

#### Scenario: 文件变更

- **WHEN** 用户新增一个 `.mjava` 文件
- **THEN** TreeView 在不需要重载窗口的情况下出现该模块
