# iapp-lint Specification

## Purpose
把会导致 mjava 模块整体失效、或让 iyu/跨模块调用在运行期静默失败的写法，在编辑时以诊断形式暴露出来。

## Requirements

### Requirement: mjava 致命写法诊断

扩展 SHALL 对 mjava 中已知会让整个模块无法加载的写法报告错误，包括：`final` 修饰符、lambda `->`、可变参数 `...`、大于 `0x7FFFFFFF` 的十六进制字面量、`new bsh.*`、类型声明或 `new` 中的全限定类名、以及字符串里的非法转义。

#### Scenario: final 形参

- **WHEN** 方法形参写成 `final Object x`
- **THEN** 该行报告错误，说明模块会整体失效

#### Scenario: lambda

- **WHEN** 代码出现 `() -> {}`
- **THEN** 报告错误并指出对应的解析失败风险

### Requirement: 未定义的目标诊断

扩展 SHALL 对以下情况报告诊断：`i.fn` 指向不存在的模块；mjava 调用带模块前缀但工程内无定义的方法；iyu 的 `call` 指向不存在的模块或方法；`uigo` 指向不存在的页面。

#### Scenario: iyu 入口写错

- **WHEN** `mian.iyu` 调用 `"home.frist"`，而 `home.mjava` 中只有 `first`
- **THEN** 在该字符串上报错，指出目标不存在

#### Scenario: 模块缺失

- **WHEN** 代码调用 `i.fn("theme")`，但工程内没有 `theme.mjava`
- **THEN** 在 `"theme"` 上报错

### Requirement: 先加载后调用诊断

当一次 iyu 事件或 mjava 入口调用跨模块方法、却在同一调用链中找不到对应的 `i.fn` 时，扩展 SHALL 报告警告；当无法静态确定加载顺序时 MUST NOT 报告为错误。

#### Scenario: 缺少 i.fn

- **WHEN** 事件直接调用 `ui_col()`，但入口方法及其调用链都没有 `i.fn("ui")`
- **THEN** 报告警告，提示可能运行期 `Command not found`

#### Scenario: 动态加载无法确认

- **WHEN** 加载发生在反射或无法静态展开的调用中
- **THEN** 不报告该诊断

### Requirement: iyu 书写规则诊断

扩展 SHALL 对 iyu 报告：事件体中出现 `call`/`addv` 之外的语句；事件体行尾注释；`ppt` 中 `key = value` 两边带空格；以及可识别的重复 id。

#### Scenario: 行尾注释

- **WHEN** 事件体写成 `call(...) // 注释`
- **THEN** 报告错误，说明会中断整个载入事件

#### Scenario: ppt 空格

- **WHEN** `ppt` 中出现 `textsize = 20sp`
- **THEN** 报告警告，说明该行会整行失效

### Requirement: 标签与属性诊断

扩展 SHALL 对 iyu 报告未知标签（error）、标签上的未知属性（warning），以及 `<eventItme>` 缺少 `type`（error）。

#### Scenario: 标签拼写错误

- **WHEN** 文件出现 `<eventItem type="loading">`
- **THEN** 报告未知标签，并列出允许的 5 个标签

#### Scenario: View 属性写错

- **WHEN** `<View idd="1" ...>` 使用了不存在的属性
- **THEN** 在该属性名上报 warning

#### Scenario: 缺少事件名

- **WHEN** `<eventItme>` 没有 `type`
- **THEN** 报告 error

### Requirement: 参数个数诊断

扩展 SHALL 在目标方法可静态确定时比较调用实参个数与声明参数个数；不一致时报告警告，因为运行期可能因动态类型或可变参数而不同。

#### Scenario: iyu 参数不匹配

- **WHEN** `call(null, "mjava", "reader.key", st_kC)` 目标方法声明 2 个参数
- **THEN** 报告参数个数不匹配的警告

### Requirement: 重名方法覆盖提示

当同一事件或调用链加载的两个模块定义了同名方法时，扩展 SHALL 报告提示，说明后加载者会覆盖先加载者。

#### Scenario: 入口方法重名

- **WHEN** 某事件链同时加载 `home` 与 `search`，两者都有 `first`
- **THEN** 提示 `first` 会被后加载的模块覆盖

### Requirement: 诊断抑制与开关

扩展 SHALL 允许按规则或按行抑制诊断（例如行内 `# noqa` 等价标记），并 SHALL 允许整体关闭 lint；被抑制的诊断 MUST NOT 出现在 Problems 中。

#### Scenario: 行内抑制

- **WHEN** 用户在命中行写入抑制标记
- **THEN** 该行的对应诊断不再报告

#### Scenario: 关闭 lint

- **WHEN** 用户关闭 lint 设置
- **THEN** 不再产生新的 iApp 诊断
