# 13 黑金计算器（实战：从建工程到交互）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 目标

用现有 KB 从头做一个真实工程，验证「建工程 → 分层样式 → 事件 → 跨 call 状态」整条链路。

## 工程

```
com.demo.calc/
├── .project / AndroidManifest.xml / icon.png / files/ / res/
├── src/mian.iyu      # 4×5 按键网格 + 两行显示
└── src/calc.mjava    # 状态机 + 样式
```

- 入口 `mian.iyu`（可直接打包）
- 新建用 `docs/scripts/create_project.py`
- iyu 只有 `call`；`clicki` 事件逐个绑定按键

## 分工

| 层 | 内容 |
|---|---|
| ppt | 控件树、尺寸、颜色、字号、`layout_weight`、`clickable` |
| mjava | 圆角/渐变/波纹、dp→px、点击处理、显示刷新、状态机 |
| i.sss | 全部计算状态（跨 call 存活） |

状态键：`calc.cur` / `calc.acc` / `calc.op` / `calc.fresh`。

## 运算模型

即时执行（左到右）：`2+3×4 = 20`。

## 实测读数

```
CALC key=1 acc= op= cur=1
CALC key=+ acc=1 op=+ cur=
CALC key=2 acc=1 op=+ cur=2
CALC key== acc=3 op= cur=
...
CALC key=× acc=5 op=× cur=
CALC key=4 acc=5 op=× cur=4
CALC key== acc=20 op= cur=
...
CALC key=÷ acc=5 op=÷ cur=
CALC key=0 acc=5 op=÷ cur=0
CALC key== acc=ERR op= cur=
...
CALC key=± acc= op= cur=-7
CALC key=% acc= op= cur=0.5
CALC key=⌫ acc= op= cur=12
CALC key== acc=3.75 op= cur=
```

七个用例全部符合预期：`3 / 20 / ERR / -7 / 0.5 / 12 / 3.75`。

## 遇到的问题

1. **界面不铺满高度**：5 行都写 `height=-2`，内容堆在顶部。
   修复：行 `height=0` + `layout_weight=1`，按钮 `height=-1`
2. `layout_margin=4dp` 不是可靠键名，改成四个方向分别写

## 复用的 KB 结论

- 新建工程最小文件集 + `build.xml` 由 iApp 首次打开生成
- 内置短名 `Button` / `LinearLayout` / `TextView`
- ppt 管静态样式，mjava 管计算与 drawable
- 控件级 `<event><eventItme type="clicki">` 可用
- 模块级变量跨 call 必丢，状态必须放 `i.sss`
- `Color.parseColor` 代替 `0xFF……` 字面量
- `layout_weight` 生效（`weight` 无效）

## 未决

- 铺满高度后的视觉确认 ⚠
- 打包安装后的表现（未验）
