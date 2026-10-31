# Spec Delta

## Purpose

让开发者在 `.mjava` 模块内以及跨模块调用时直接定位方法定义，并能把 Java/Android 类型与方法引用接回官方源码。

## ADDED Requirements

### Requirement: `.mjava` 作为独立语言被识别

扩展 SHALL 把 `.mjava` 注册为独立语言，而不是 Java；打开文件时 SHALL 使用 mjava 的语法高亮与语言模式，且 MUST NOT 触发 Java 工程的编译或诊断。

#### Scenario: 打开 mjava 文件

- **WHEN** 用户打开 `src/home.mjava`
- **THEN** 编辑器语言模式显示为 mjava，关键字/字符串/注释按 mjava 高亮
- **AND** 不出现 Java 语言的“无法解析的编译单元”类诊断

### Requirement: 模块与方法索引

扩展 SHALL 把工程 `src/` 下每个 `.mjava` 识别为一个模块，模块名取文件名（不含扩展名）；SHALL 记录每个方法的名称、参数、返回类型、可见性与源码范围。

#### Scenario: 工程加载后可见

- **WHEN** 打开一个包含 `src/home.mjava` 的 iApp 工程
- **THEN** 模块 `home` 及其方法出现在索引中

#### Scenario: 编辑后更新

- **WHEN** 用户修改或新增一个方法并保存
- **THEN** 索引在不需要重载窗口的情况下反映新方法

### Requirement: 裸方法调用的定义跳转

对 mjava 中以裸名调用的方法，扩展 SHALL 按以下顺序解析并跳转：当前模块；当前事件或调用链中通过 `i.fn` 加载的模块；全工程唯一同名方法；否则返回全部候选供用户选择。扩展 MUST NOT 在多个候选时任意选一个。

#### Scenario: 同模块调用

- **WHEN** 用户对 `lib_wire()` 触发“转到定义”
- **THEN** 跳到同文件中的 `lib_wire` 声明

#### Scenario: 已加载模块的调用

- **WHEN** 某函数先调用 `i.fn("ui")`，之后调用 `ui_col()`
- **THEN** 跳到 `ui.mjava` 中的 `ui_col` 声明

#### Scenario: 重名入口方法

- **WHEN** `home.first` 与 `search.first` 同时存在，当前事件加载的是 `home`
- **THEN** 跳到 `home.mjava` 的 `first`，而不是 `search.mjava`

#### Scenario: 无法消歧

- **WHEN** 调用的方法名在多个模块中存在，且当前调用链没有信息能确定加载顺序
- **THEN** 返回候选列表，不跳转到任意一个，也不报错

### Requirement: 模块与页面路径引用跳转

扩展 SHALL 支持从 `i.fn("name")` 跳到 `name.mjava`，从 `i.uigo("page.iyu")` 跳到对应 `.iyu` 页面；页面引用可以带或不带 `.iyu` 扩展名。

#### Scenario: 跳模块文件

- **WHEN** 用户对 `i.fn("theme")` 触发“转到定义”
- **THEN** 打开 `theme.mjava`

#### Scenario: 跳页面文件

- **WHEN** 用户对 `i.uigo("search.iyu")` 触发“转到定义”
- **THEN** 打开 `search.iyu`

### Requirement: Java 类名与成员跳转

扩展 SHALL 把 mjava 中的类引用（通过 import 解析的短名或全限定名）映射到 JDK/Android 源码声明；对成员调用 SHALL 根据接收者类型解析，并在无法推断接收者类型时退回类内候选或返回空结果，MUST NOT 猜测一个可能错误的位置。

#### Scenario: 类名跳转

- **WHEN** 用户对 `TextView` 触发“转到定义”
- **THEN** 打开 Android 源码中的 `android/widget/TextView.java` 类声明

#### Scenario: 成员跳转

- **WHEN** 代码为 `TextView tv = ...; tv.setText("x");`，用户对 `setText` 触发“转到定义”
- **THEN** 打开 `TextView.java` 中匹配的 `setText` 声明

#### Scenario: 接收者类型未知

- **WHEN** 成员调用的接收者来自反射或无法推断的表达式
- **THEN** 扩展返回空结果或候选，不跳到无关方法

### Requirement: Hover 显示签名与来源

扩展 SHALL 在方法声明或调用处显示 Hover，内容包含签名、所属模块或类；当 Java 源码带 javadoc 时 SHALL 一并显示。

#### Scenario: mjava 方法 Hover

- **WHEN** 用户悬停在 `lib_page()` 上
- **THEN** Hover 显示返回类型 `View` 与所属模块 `home`

#### Scenario: Java 方法 Hover

- **WHEN** 用户悬停在 `TextView.setText` 上且 Android 源码可用
- **THEN** Hover 显示方法签名与 javadoc 摘要

### Requirement: 方法注释文档

扩展 SHALL 读取方法声明正上方的 `/** ... */` 或连续 `//` 注释，并在 Hover 与补全说明中显示；`/** */` 中的 `@param` 等标签行 SHALL 保留。注释与声明之间存在空行时 MUST NOT 挂到该方法。

#### Scenario: 块注释

- **WHEN** 方法上方是带 `@param` 的 `/** ... */`
- **THEN** Hover 显示描述与标签行

#### Scenario: 行注释

- **WHEN** 方法上方是连续的 `//` 行
- **THEN** Hover 与补全说明显示合并后的注释文本

#### Scenario: 空行分隔

- **WHEN** 注释与方法之间隔着一个空行（如分节标题）
- **THEN** 该注释不挂到方法上

### Requirement: mjava 大纲

扩展 SHALL 为 mjava 文件提供文档大纲，列出方法及其签名，以及文件顶层的变量声明。

#### Scenario: 大纲内容

- **WHEN** 用户打开 mjava 文件的大纲
- **THEN** 能看到该文件全部方法，点击可跳转到声明

### Requirement: 方法引用查找

扩展 SHALL 在方法声明或调用处提供“查找引用”，列出工程内指向同一方法的 mjava 裸调用、`i.call` 目标与 iyu 入口；引用范围 MUST 以当前工程为界，不混入其它工程。

#### Scenario: 声明处查找引用

- **WHEN** 用户对 `home.first` 的声明触发“查找所有引用”
- **THEN** 结果包含 `misc.mjava` 的 `i.call("mjava", "home.first")` 与 `mian.iyu` 的入口字符串

#### Scenario: Java 成员引用

- **WHEN** 用户对可推断的 `TextView.setText` 调用触发“查找所有引用”
- **THEN** 结果列出工程内接收者类型可推断、且声明落在同一 `TextView.setText` 的调用点

#### Scenario: 无法推断

- **WHEN** 接收者来自反射或动态表达式
- **THEN** 不返回该调用作为引用，不伪造结果
