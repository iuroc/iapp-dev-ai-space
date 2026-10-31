# window-insets Specification

## Purpose
规定 iApp 工程如何与系统 UI 共存：窗口姿态跟随宿主、安全区由 insets 计算、
状态栏与键盘如何呈现、手势热区如何避让，以及哪些系统行为是有意不接管的。

## Requirements

### Requirement: 窗口姿态默认跟随宿主，展示类页面可显式接管

应用 MUST NOT 默认修改窗口装饰行为：MUST NOT 调用 `setDecorFitsSystemWindows`、
MUST NOT 隐藏系统栏、MUST NOT 修改 `layoutInDisplayCutoutMode`。
安全区 MUST 依据宿主给出的实际 insets 计算，使同一份代码在「内容已被系统栏占用」
与「内容延伸至屏幕边缘」两种姿态下都正确。

例外仅限展示类页面（看图、播放器、游戏），且只允许 edge-to-edge 与沉浸式两档；
任何接管 MUST 在离开页面时还原，MUST NOT 让窗口停留在被接管的状态。

#### Scenario: 宿主已经避开系统栏

- **WHEN** 根视图已被宿主摆到状态栏之下（根的上边界等于状态栏高度）
- **THEN** 内容区不再为顶部系统栏留白，直接铺满根视图；
  即使此时窗口 insets 仍报出完整的系统栏高度，也不得按其数值再留一次

#### Scenario: 宿主未避开系统栏

- **WHEN** 根视图与屏幕边缘齐平且系统栏 insets 大于 0
- **THEN** 内容区按 insets 数值留白，内容不被状态栏或导航栏遮挡

#### Scenario: 升级到强制全屏的新系统

- **WHEN** 同一份代码运行在宿主改为让内容铺到屏幕边缘的平台上
- **THEN** 布局自动按差值留白，无需改动代码

#### Scenario: 展示类页面开启 edge-to-edge

- **WHEN** 某个以画面为主体的页面显式开启 edge-to-edge：把根上移宿主已预留的距离、
  高度补足到整屏、状态栏设为透明
- **THEN** 背景铺到屏幕四边（包括状态栏后面），系统栏仍然可见，
  正文按 insets 差值留白、不被状态栏遮挡

#### Scenario: 宿主在父容器上预留系统栏空间

- **WHEN** 宿主把系统栏预留量加在根的直接父容器的 padding 上，且每轮布局重新施加
- **THEN** 实现 MUST NOT 依赖清除该 padding 来实现 edge-to-edge（会被重新加回），
  而 MUST 通过上移并加高根来覆盖该预留区

#### Scenario: 展示类页面开启沉浸式

- **WHEN** 某页面在 edge-to-edge 基础上再 `hide(systemBars)`，并设为边缘滑动临时唤出
- **THEN** 系统栏被隐藏、边缘滑动可唤出，内容按 insets 变成 0 自动铺满四边，
  不额外补写任何尺寸常量

#### Scenario: 离开接管过窗口的页面

- **WHEN** 用户切走该页面（`pause`）
- **THEN** 窗口装饰被还原，宿主或其他页面不残留全屏状态；
  尤其在被其他应用承载的模式（如可视化 IDE 里预览）下必须还原

#### Scenario: 窗口姿态只在打包形态验收

- **WHEN** 需要确认 edge-to-edge / 沉浸式的实际表现
- **THEN** 以打包产物为准；开发模式下窗口属于宿主，结果不能代表交付形态

### Requirement: 安全区取 insets 与根偏移的差值

为系统栏让位的间距 MUST 等于「窗口 insets」与「根容器在窗口中已让出的距离」的差值，
并以 0 为下界；MUST NOT 直接把窗口 insets 当作 padding，
因为宿主可能已经在窗口层面避开过系统栏，直接取用会重复留白。
差值 MUST 在根视图完成测量之后读取（`loading` 阶段无法取得 insets），
并在每次重新进入页面时刷新。

#### Scenario: 宿主已避让且 insets 仍为满值

- **WHEN** 屏幕高 1920、根位于 `y=72`、高 1848，顶部系统栏 insets 为 72
- **THEN** 顶部安全区取 `72 - 72 = 0`，正文从根顶部开始

#### Scenario: 首帧尚不能读 insets

- **WHEN** 页面处于 `loading` 阶段，`getRootWindowInsets()` 返回空
- **THEN** 先按 0 留白完成首帧，待 `loadingComplete` 与 `resume` 读到实际差值后再刷新

### Requirement: 系统栏间距一律由 insets 计算

任何为系统栏让位的间距 MUST 来自运行期读取的 insets，MUST NOT 使用固定尺寸常量。
底部间距 MUST 能随三键导航、手势导航、导航栏隐藏三种状态自适应。

#### Scenario: 三键与手势导航切换

- **WHEN** 用户把系统导航从三键切换为手势、或反过来
- **THEN** 贴底元素的位置随之改变，不发生重叠或悬空

#### Scenario: 导航栏被隐藏

- **WHEN** 导航栏处于隐藏状态、insets 为 0
- **THEN** 贴底元素贴到屏幕底边，下方不残留空白

### Requirement: 背景由根容器绘制，不依赖系统栏配色接口

页面的背景（颜色、渐变、图片）MUST 由根容器自身绘制并延伸至屏幕四边。
MUST NOT 把系统栏配色接口当作背景的保证。

#### Scenario: 系统栏变透明

- **WHEN** 平台忽略系统栏配色设置、系统栏变为透明
- **THEN** 根容器的背景自然延续到系统栏后面，视觉不出现断层

### Requirement: 状态栏图标深浅由窗口 insets 控制器设置

状态栏图标明暗 MUST 通过窗口的 insets 控制器设置外观，MUST NOT 使用已废弃的全局
`SystemUiVisibility` 标志位。

#### Scenario: 深色背景

- **WHEN** 页面背景为深色
- **THEN** 状态栏图标显示为浅色，确保可读

#### Scenario: 浅色背景

- **WHEN** 页面背景为浅色
- **THEN** 状态栏图标显示为深色

### Requirement: 键盘以 ime inset 响应

输入类页面 MUST 监听 ime inset 的变化并据此调整内容位置，
MUST NOT 假定键盘弹出会自动压缩布局。安全区下边距 MUST 取系统栏与 ime 两者中的较大值。

#### Scenario: 键盘弹出

- **WHEN** 输入框获得焦点并弹出键盘
- **THEN** 输入框与提交按钮保持可见，不被键盘遮挡

#### Scenario: 键盘收起

- **WHEN** 键盘收起
- **THEN** 内容回到原位置，下边距回落到系统导航栏的高度

### Requirement: 交互控件避让系统手势热区

贴边与贴底的交互控件 MUST 依据系统手势安全区定位；当手势与业务手势冲突时，
MUST 显式声明手势排除区域，或改用不依赖边缘起手的手势。

#### Scenario: 底部贴边按钮

- **WHEN** 按钮贴在屏幕底部
- **THEN** 按钮位于手势条与系统栏之上，不与系统手势重叠

#### Scenario: 页面本身需要四向滑动

- **WHEN** 页面依赖从屏幕边缘起手的滑动
- **THEN** 显式声明手势排除区域，并在真机上确认边缘起手不被系统返回手势抢走

### Requirement: 新系统行为只记录不实现

尚未取得实测证据的平台行为（当前为 Android 15 及以上的强制全屏与系统栏配色变化）
MUST 记录为环境档案中的待验项，附带验证方式；MUST NOT 在未验证的情况下为其编写分支逻辑。

#### Scenario: 遇到未验证的平台差异

- **WHEN** 某行为在可获得证据前无法确认
- **THEN** 在环境档案登记为待验项并写明怎么验，实现保持不分支

#### Scenario: 反馈来自更新的系统

- **WHEN** 用户在新系统真机上反馈现象
- **THEN** 先比对已登记的待验项，再决定是修实现还是补记结论
