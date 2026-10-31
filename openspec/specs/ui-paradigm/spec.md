# ui-paradigm Specification

## Purpose
规定 iApp 工程的界面如何被构建：`.iyu` 允许承载什么、在哪一帧建树、失败如何局部化、
组件以什么形态存在与复用、跨事件如何重新拿到视图引用。

## Requirements

### Requirement: `.iyu` 只承载根容器与全局事件表

每个页面的 `.iyu` MUST 只包含一个全屏根容器和 `<UIEventset>` 全局事件表。
MUST NOT 声明子控件、静态样式键或每个控件的 `<event>` 块。视图形状、层级、样式与监听器一律由 mjava 构建。

#### Scenario: 新建一个页面

- **WHEN** 工程师新增页面
- **THEN** `.iyu` 里只有一个根容器节点与事件表，其余视图在 mjava 里创建

#### Scenario: 需要给某个视图加样式

- **WHEN** 某视图需要颜色、字号、圆角、描边等外观
- **THEN** 在 mjava 里设置，不回到 `.iyu` 声明

#### Scenario: 需要点击响应

- **WHEN** 某视图需要响应点击
- **THEN** 建树时在 mjava 里装监听器，不使用 `.iyu` 的 `<event>` 块

### Requirement: 建树发生在 `loading`，尺寸取自 `DisplayMetrics`

整棵树 MUST 在 `loading` 阶段一次建完，首帧即为成品。
视图尺寸与位置 MUST 基于 `DisplayMetrics` 换算，MUST NOT 依赖 `getWidth()`/`getHeight()`
（`loading` 阶段这些值尚未测量，返回 0）。

#### Scenario: 首帧可见

- **WHEN** 页面进入 `loading`
- **THEN** 树已建好，首帧即有完整内容，不存在「先空屏再填充」的过程

#### Scenario: 需要屏幕尺寸

- **WHEN** 计算全屏或居中布局
- **THEN** 取 `DisplayMetrics` 的宽高，不使用任何视图的实测尺寸

#### Scenario: 确实需要实测尺寸

- **WHEN** 某效果（如背景快照裁剪）必须知道实际像素尺寸
- **THEN** 在 `loadingComplete` 里补做该段，且该段可独立失败

### Requirement: 构建分段，失败局部化

页面构建 MUST 拆成若干独立入口的段，段之间异步串接。
任一段抛错 MUST 只影响该段，其余段照常执行并上屏。
每段进出 MUST 各留一行日志。

#### Scenario: 某一段有语法或调用错误

- **WHEN** 中间一段抛出错误
- **THEN** 页面其余部分照常显示，logcat 能看出死在哪个段

#### Scenario: 段间时序

- **WHEN** 前一段已完成
- **THEN** 后一段在下一帧执行，段与段之间不共享局部变量，需要传递的对象由前一段显式交回

### Requirement: 组件是工厂函数，跨工程按副本复用

组件 MUST 表现为「返回视图的工厂函数 + 组合」，MUST NOT 依赖继承 View 的自定义类
（解释层不支持具名 class）。
复合组件对外的子视图 MUST 通过命名句柄暴露（视图标签），由调用方按名字取。

组件库 MUST 在每个工程内自带一份完整副本，工程 MUST NOT 在运行时依赖工程外的文件；
组件库的权威副本维护在通用知识层，工程内副本用于分发，改进需手动回灌。

#### Scenario: 新工程需要组件库

- **WHEN** 新建工程
- **THEN** 组件库文件随工程创建复制进来，工程可脱离工作区独立打包

#### Scenario: 复合组件暴露内部子视图

- **WHEN** 调用方需要拿到复合组件内部的某个子视图
- **THEN** 通过命名句柄查找，不依赖子视图的下标顺序

#### Scenario: 组件库需要改进

- **WHEN** 发现某组件在多个工程都有用
- **THEN** 先在当前工程验证，再回灌权威副本，不回灌则新工程继续用旧版本

### Requirement: 视图回溯按闭包优先、注册表次之

同一构建批次内的回调 MUST 通过闭包捕获视图引用。
跨批次入口（由应用生命周期再次进入的方法）需要少量视图时 MUST 通过运行期注册表取回。
MUST NOT 为视图分配自定义 id 再靠查找取回。

#### Scenario: 点击更新自身外观

- **WHEN** 某视图的点击需要改变它自己的图标
- **THEN** 监听器直接捕获该视图引用，不做查找

#### Scenario: 生命周期入口需要更新界面

- **WHEN** `resume` 或 `pause` 需要更新播放态、进度等少量视图
- **THEN** 从运行期注册表按名字取

#### Scenario: 注册表不可用

- **WHEN** 运行期注册表无法承载引用
- **THEN** 降级为视图标签查找，并记录该降级为待验证项
