# Spec Delta

## Purpose

为 mjava 提供 JDK 与 Android 官方源码的类/成员查阅能力，使跳转不依赖 Java 语言服务器也能落到真实源码。

## ADDED Requirements

### Requirement: 源码集配置

扩展 SHALL 允许配置 JDK `src.zip`、Android 源码目录以及额外的源码 jar；当本机存在可自动发现的 JDK 或 Android SDK 时 SHALL 优先使用本地路径。

#### Scenario: 使用本地 JDK

- **WHEN** 用户配置了 `jdkHome`，且其 `lib/src.zip` 存在
- **THEN** JDK 类与成员可被索引

#### Scenario: 使用 Android SDK

- **WHEN** 用户指向一个包含 `sources/android-<API>` 的 Android SDK
- **THEN** `android.*` 类可被索引

### Requirement: 类级索引

扩展 SHALL 建立“全限定类名 → 源码文件”的索引；索引 SHALL 覆盖 JDK 模块、Android framework 包，以及已配置的 AndroidX/Material 源码。

#### Scenario: 解析 JDK 类

- **WHEN** 代码引用 `java.util.ArrayList`
- **THEN** 索引返回对应的 `ArrayList.java`

#### Scenario: 解析 Android 类

- **WHEN** 代码引用 `android.widget.TextView`
- **THEN** 索引返回对应的 Android framework 源码文件

### Requirement: 懒加载的成员索引

扩展 SHALL 按需解析单个源码文件，提取包名、import、类声明、继承关系、方法、字段、源码范围与 javadoc；解析结果 SHALL 被缓存，文件未变化时不重复解析。

#### Scenario: 首次成员跳转

- **WHEN** 用户第一次对 `ArrayList.add` 触发“转到定义”
- **THEN** 解析 `ArrayList.java` 并定位 `add` 的重载

#### Scenario: 继承方法

- **WHEN** 用户在 `TextView` 实例上跳转 `getId`
- **THEN** 沿继承链找到 `android.view.View.getId`

### Requirement: 成员解析与重载

给定接收者类型、成员名与实参个数，扩展 SHALL 在类及其父类/接口中查找匹配成员；存在多个同参数个数重载时 SHALL 返回全部候选或按可推断的实参类型收窄，MUST NOT 随机选一个。

#### Scenario: 多个重载

- **WHEN** `setText` 有多个重载且实参类型不足以唯一确定
- **THEN** 返回候选列表供用户选择

#### Scenario: 继承与接口

- **WHEN** 方法声明在接口或父类上
- **THEN** 仍能定位到声明处

### Requirement: 索引不可用时的降级

当源码索引未配置或不可读时，扩展 SHALL 让 Java 类/成员跳转返回空结果，并 MUST NOT 把“未解析的 Java 引用”报告为错误。

#### Scenario: 未配置 Android 源码

- **WHEN** 工程引用 `TextView` 但未配置 Android 源码
- **THEN** 跳转返回空，lint 不因该引用报错

### Requirement: 下载与缓存

当本地缺少 Android 源码时，扩展 SHALL 提供显式的安装入口，在下载前告知体积并取得用户确认；下载内容 SHALL 存入扩展的缓存目录，MUST NOT 静默下载或写入工程目录。

#### Scenario: 首次安装

- **WHEN** 用户选择安装 Android 源码
- **THEN** 扩展显示约 48 MB 的体积提示，确认后下载并缓存
- **AND** 用户可以取消，取消后不影响 JDK 已有功能
