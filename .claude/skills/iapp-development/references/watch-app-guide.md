# 手表应用（圆屏）开发指南

版本前提：OPPO Watch X2 / Android 11（API 30）/ 466×466 / density 320 / 纯 32 位用户空间。
2026-10-28 ~ 10-29 用青简手表版（8 个页面）完整走通后整理。

## 1. 交付链路

```
PC 容器内 iApp 打包（设置 →【打包设定so库】ABI 全勾）
  → FTP 取回 /ProjectApp/<项目ID>/bin/<包名>.apk
  → adb install -r  → 手动验证
```

- 手表不跑 iApp，只装 APK；首次启动会弹存储权限，`pm grant` 可代授（重装后要再授）
- 装完用 `am start -n <包名>/com.iapp.app.run.mian` 拉起
- 取证前先 `svc power stayon usb`，否则几秒就息屏

## 2. 圆屏布局

- **内容收进内接正方形**：边长 = 直径 / √2。466px → 330px = **165dp**（density 2.0）
- 摆放用 mjava：

```java
FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(dp(165), dp(165));
lp.gravity = Gravity.CENTER;
view.setLayoutParams(lp);
```

- **ppt 的 `layout_gravity` 不生效**（见 `pitfalls.md` #29），别在 ppt 里写
- 方框之外的环形区域可以放小元素：顶部标题（top 6dp）、底部页码/菜单（bottom 2~4dp）、
  左右翻页按钮（左右各 3dp、30×60dp），都在圆内

## 3. 固定标题

标题要常驻就**不能放进 ScrollView**：作为 root FrameLayout 的直接子 View，
`Gravity.TOP|CENTER_HORIZONTAL`、宽 110dp、9sp、单行 ellipsize。

详情这类「标题属于正文」的页面，正文标题照常滚动，另加一个固定小标题（图书详情/期刊详情）。

## 4. 控件选型与性能

| 场景 | 用法 |
|---|---|
| 列表行 | `TextView` + `setPadding`，**一屏 3~5 行**，靠滚动 |
| 按钮（少量） | `TextView` + `GradientDrawable`（圆角 + 描边/填充），空心/实心两套 |
| 大量按钮 | **不要用 MaterialButton**：11 个 Material 组件会让分类页明显卡顿 |

- 统一按钮：12sp、圆角 10dp、上下 10dp 内边距
  - 空心：透明底 + 1dp `#4A4458` 描边 + `#E6E0E9` 字
  - 实心：`#4A4458` 底 + `#EADDFF` 字
  - 主行动按钮（开始阅读）：`#D0BCFF` 底 + `#141218` 字
- 字号参考：固定标题 9sp / 列表行 11~12sp / 详情正文 13sp、书名 14sp / 首页色块 15sp
- 两列网格：每行一个横向 `LinearLayout`，子项 `width=0 + weight=1`，奇数补透明占位

## 5. 手势与反馈

| 交互 | 做法 |
|---|---|
| 表冠 | `ACTION_SCROLL` + `AXIS_VSCROLL`（详见 `events-guide.md` §滚轮/表冠） |
| 横滑返回 | 每页 `OnTouchListener`，判定 `dx > 90 && dx > dy*1.5` → `activity.finish()` |
| 触摸目标 | 根布局必须 `setClickable(true)`，否则 `DOWN` 不消费、收不到 `MOVE/UP` |
| 按压反馈 | `if (view.hasOnClickListeners()) view.setAlpha(0.55f)`，抬起还原 1.0f |

**坐标系**：多 View 共用监听时一律用 `getRawX()/getRawY()`。
用 `getX()` 会串——按下在子控件（相对 0）、移动在 ScrollView（相对 140），
凭空算出 140px 位移，纵向滚动被误判成横滑而退出页面。

**不要用 `getTag() != null` 判断控件**：iApp 会给 ppt 里的 View 自动挂 tag（设计器用），
容器也会命中，结果是按空白处整屏变暗。

## 6. 阅读正文（WebView）

```java
ws.setSupportZoom(false);
ws.setBuiltInZoomControls(false);
ws.setDisplayZoomControls(false);
ws.setUseWideViewPort(false);
ws.setLoadWithOverviewMode(false);
wv.setHorizontalScrollBarEnabled(false);
wv.setVerticalScrollBarEnabled(false);
wv.setLongClickable(false);                       // 关掉长按选中/上下文菜单
wv.setOnLongClickListener(... return true ...);
```

CSS（必须）：

```css
html,body{margin:0;padding:0;background:#141218;color:#E6E0E9;overflow-x:hidden;}
body{font-size:14px;line-height:1.6;-webkit-user-select:none;user-select:none;
     -webkit-touch-callout:none;}
p{margin:0 0 .6em 0;text-indent:2em;}
img{max-width:100%!important;height:auto!important;display:block;margin:6px auto;}
```

**图片只用 CSS 覆盖，不要改写 HTML**：`max-width/height:auto` 足以压住内联
`width="973" height="1412"`；在 Java 字符串里写正则（`\s`、`\"`）极易转义出错，
一旦 Java 字符串解析失败，**整个 mjava 模块失效**，页面会退化成「控件全堆左上角」。

**分页参数沿用手机版** `w=1000&h=2000&fsize=18`：
- 页码与手机版同源，进度可互通
- 按表盘尺寸重新分页会让请求量涨 20 倍（84 页 vs 2195 页）
- 文字会按视口重排，图片靠 CSS 压回

其它：
- 翻页后 `scrollTo(0,0)` 要**延迟 300ms** 再执行一次（`loadDataWithBaseURL` 是异步的）
- 左右按钮 = **直接翻页**；页内滚动交给表冠/手指（别让按钮先滚到底再翻）
- 目录用 `core_readPage` 已返回的 `catalogs`，不额外请求

## 7. 页面与导航约定

- 一页一个 `.iyu`，`i.uigo("xxx.iyu")` 压栈；返回交给各页自己的横滑监听
- 跨页传值走 `i.sss`（`qj.item` / `pending` / `goto` 等）
- 阅读页**不做横滑返回**（防误退），退出走菜单页的「关闭阅读器」：
  菜单页设 `quit=1` 后 `finish()`，阅读页 `resume` 里检测标志再 `finish()`
- 目录页选章后设 `goto=<page>` + `menuclose=1` 并 `finish()`，菜单页 `resume` 关自己，
  阅读页 `resume` 读到 `goto` 再跳页

## 8. 踩过的坑（本目录实测）

1. 后台线程 `Runnable` 里调模块方法，必须先 `i.fn("模块")` —— 否则 `Command not found` 杀进程（`pitfalls.md` #31）
2. 事件体带 `0` 实参，被调方法必须接参（`pitfalls.md` #30）
3. ppt `layout_gravity` 不生效，圆屏对齐走 `LayoutParams`（`pitfalls.md` #29）
4. Java 字符串里的正则转义错误 → 模块整体解析失败 → 页面「裸奔」（本指南 §6）
5. 根布局不 `setClickable(true)` → 只有 ScrollView 覆盖区能识别滑动
6. 用 `getX()` 混坐标系 → 滚动被误判成横滑
7. 用 `getTag()` 判断可点控件 → iApp 自带 tag，容器也会变暗

## 9. 未覆盖

- 表盘（watch face）、磁贴（Tile）、complication、环境模式（iApp 做不了）
- 手表独立的历史/设置存储与手机版**不共享**（不同包名，`getFilesDir()` 各自独立）
