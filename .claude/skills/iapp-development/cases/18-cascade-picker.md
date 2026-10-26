# 18 级联选择器组件（实战：单弹窗多级 / 返回 / 绘制图标）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 目标

B8 第三例：把「下拉选择器」做成可复用组件——一个弹窗内完成多级级联、支持回退上一级，
行内水波纹裁剪到圆角范围内，所有图标用 Canvas 现画（不用 emoji、不用文字符号）。

## 分层

| 模块 | 职责 |
|---|---|
| `pick.mjava` | 通用组件：触发条、弹窗、搜索、级联栈、绘制图标、回调 |
| `demo.mjava` | 业务数据：`HashMap<父名称, 子列表>`（根键空串）+ 回调处理 |
| `mian.iyu` | 只有控件占位和一次 `call`（`loading → demo.setup`） |

对外 API：

```java
pick.buildTrigger(int hostId, String text, String tapCall)  // 画触发条
pick.setTrigger(String text)                                // 更新触发条文案
pick.show(String title, HashMap tree, String rootKey, String cb)  // 打开
// 叶子被选中时回调 cb，参数是 "父 / 子 / 孙"
```

## 级联的做法

- 栈放 `i.sss`：`pick.keys`（数据键）与 `pick.names`（显示名）两个 ArrayList
- 点行时：`tree.containsKey(name)` 有子项 → 入栈并就地重渲染；没有子项 → 回调 + dismiss
- 返回箭头：出栈一级；`keys.size()==1` 时箭头设为 `INVISIBLE`
- 面包屑由 `pick.names` 拼接，标题在左、路径在下
- 换级时清空搜索框，用 `pick.mute` 标记避免 `TextWatcher` 递归渲染

## 行内水波纹

```java
GradientDrawable mask = roundBg("#FFFFFF", dp(10), 0, "#00000000");
row.setBackground(new RippleDrawable(
        ColorStateList.valueOf(Color.parseColor("#1A2D7FF9")), null, mask));
```

- 第三个参数是**遮罩**；不给遮罩时涟漪按无边界圆扩散，看起来是一个整圆
- 遮罩必须是不透明形状（圆角矩形即可）

## 图标全部绘制

`Bitmap.createBitmap` + `Canvas` + `Paint` + `Path`：

| 图标 | 画法 |
|---|---|
| 触发条箭头 | `Path` 折线 + `STROKE` + `ROUND` 线帽 |
| 返回箭头 | 同上，方向朝左 |
| 对勾 | 两段折线 |
| 省 / 市 / 区 | 定位针（圆 + 三角）/ 三个圆角竖块 / 四宫格 |

颜色按层级区分（蓝 `#2D7FF9` / 绿 `#34B37E` / 橙 `#F2994A`）。

## 实测读数

```
PICK-level 0 n=3
PICK-enter 广东省 depth=1 → PICK-level 1 n=3
PICK-enter 广州市 depth=2 → PICK-level 2 n=4
PICK-pick 广东省 / 广州市 / 海珠区 → PICK-cb-sent demo.onPick
DEMO-onPick 广东省 / 广州市 / 海珠区 → DEMO-call pick.setTrigger
PICK-back depth=0
```

## 踩过的坑

- `i.call` 第一个参数是语言标识（`"mjava"`），不是变量名；传 `null` NPE、传 `""` 静默不执行
- 目标是 void 方法时不能接返回值，否则 `Void initializer` 并中止整个方法 → 组件方法统一 `return String`
- `String.valueOf(i.sss("key"))` 在 key 为 null 时会命中 `valueOf(char[])` 重载 → `length of null array`；每个模块备一个 `str(Object)`
