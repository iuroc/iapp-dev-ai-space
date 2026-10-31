# iapp-completion Specification

## Purpose
在编辑 mjava 与 iyu 时给出与工程索引、Java 类型推断一致的上下文补全，覆盖方法、模块、页面、i 对象成员、Java 成员、事件类型与标签，减少查表和拼写错误。

## Requirements

### Requirement: mjava 方法与模块补全

扩展 SHALL 在 mjava 代码位置提供方法候选，按“当前模块 → `i.fn` 加载集 → 工程内其它模块”排序，并显示签名与所属模块；在 `i.fn`、`i.uigo`、`i.call` 的字符串内 SHALL 分别提供模块名、页面名与 `模块.方法` 候选。

#### Scenario: 当前模块优先

- **WHEN** 用户在 `home` 模块输入方法名前缀 `first`
- **THEN** `home.first` 排在已加载模块与其它模块的同名方法之前

#### Scenario: 模块字符串

- **WHEN** 用户在 `i.fn("` 后输入
- **THEN** 候选列出工程内的 mjava 模块名

#### Scenario: 页面字符串

- **WHEN** 用户在 `i.uigo("` 后输入
- **THEN** 候选列出工程内的页面名，并带 `.iyu` 扩展名

### Requirement: i 对象成员补全

扩展 SHALL 在 `i.` 之后提供内置 `Aid_javaCode` stub 的方法与字段候选，并显示签名。

#### Scenario: i 成员

- **WHEN** 用户输入 `i.`
- **THEN** 候选包含 `fn`、`sss`、`syso`、`uigo`、`us`、`call` 等成员

### Requirement: Java 成员补全

当成员访问的接收者类型可推断时，扩展 SHALL 沿继承链列出该类型的方法与字段，子类成员优先、`java.lang.Object` 成员最后；接收者类型不可推断时 MUST NOT 返回成员候选。

#### Scenario: TextView 成员

- **WHEN** 用户在 `TextView tv` 后输入 `tv.set`
- **THEN** 候选包含两个 `setText` 重载，以及从父类继承的 `setId`

#### Scenario: 未知接收者

- **WHEN** 接收者来自反射或无法推断的表达式
- **THEN** 不返回成员候选

### Requirement: iyu 补全

扩展 SHALL 在 `eventItme type="` 内提供事件类型候选，在 `call(..., "` 内提供 `模块.方法` 候选。

#### Scenario: 事件类型

- **WHEN** 用户在 `<eventItme type="` 后输入
- **THEN** 候选包含 `loading`、`loadingComplete`、`resume`、`clicki`、`downkey` 等事件类型

#### Scenario: 入口目标

- **WHEN** 用户在 `call(null, "mjava", "` 后输入
- **THEN** 候选列出工程内的 `模块.方法`

### Requirement: 补全与上下文一致

补全 MUST NOT 在字符串或注释中给出代码补全，MUST NOT 在已有括号时重复插入括号；候选范围 SHALL 以当前工程为界。

#### Scenario: 注释内不补全

- **WHEN** 光标位于 `//` 注释内
- **THEN** 不返回方法或成员候选

#### Scenario: 已有括号

- **WHEN** 光标前后已经有 `(`
- **THEN** 接受方法候选只插入方法名，不重复插入括号
