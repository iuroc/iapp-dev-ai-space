# 手表应用（圆屏）开发指南

版本前提：OPPO Watch X2 / Android 11（API 30）/ 466×466 / density 320 / 纯 32 位用户空间。
2026-10-28 ~ 10-29 用一个 8 页的 iApp 阅读器示例工程完整走通后整理；
下文提到的「示例工程」即该阅读器的手表移植版（内部示例工程；换项目时替换成你自己的工程即可）。

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

- **关键尺寸一律 mjava 设置**：开发模式里 `.iyu` 的 `dp` 与 mjava 的 `density` 可能不一致
  （实测 `.iyu` 的 233dp 解析成 932px，而 mjava `density=3.0`），只靠 ppt 定尺寸会整体放大 4/3；
  容器/棋盘/按钮尺寸与 `setTextSize` 都放 mjava（✅ 2026-10-29，API 34）
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

## 10. 模拟器预览圆表盘（注入式罩层）

手机模拟器和手机开发共用时，**不要改 `wm size` / `wm density`**：整实例全局生效，iApp 和其它 app
会一起变成方屏（✅ 2026-10-29）。用注入式罩层代替：

- 把 `scripts/bezel.mjava` 复制到工程 `src/`
- `.iyu` 的 `loading` 事件加一行（只传表盘直径，单位 dp）：

```
call(null, "mjava", "bezel.install", 233)
```

行为：

- **环境判断**：`min(widthPixels,heightPixels)/density < 300` 或 `Configuration.isScreenRound()`
  → 认为是手表，直接返回不画；手机（360dp 宽）才画
- **罩层加在 `DecorView`**：圆外半透明黑（约 50%）+ `PorterDuff.CLEAR` 挖出圆 + 2dp 中性色圆环；
  不可点，触摸穿透；表盘内部的底色/样式完全由工程自己决定
- 不依赖 `SYSTEM_ALERT_WINDOW`，不跨 app 残留，打包后同样有效
- 罩层只「挡」不「排版」：页面内容仍要自己居中在 233dp 内
- 圆直径跟随参数，换表只改调用里的 dp；不传颜色，圆外固定半透明黑，下面内容可见且点击穿透
- 状态栏：单独 `FLAG_FULLSCREEN` 会被 iApp 覆盖，要加
  `SYSTEM_UI_FLAG_IMMERSIVE_STICKY | LAYOUT_FULLSCREEN | LAYOUT_HIDE_NAVIGATION`，
  并在 `loading` / `loadingComplete` / `resume` 各设一次（✅ API 34，2026-10-29）
- 工程侧只需「模块文件 + loading 一行」，布局与样式代码零侵入

## 11. 真机预览与按键模拟（scrcpy）

屏幕小、息屏快的手表，用 scrcpy 做实时预览和交互，比反复 `screencap` 高效。

- **默认 `--keyboard=sdk` 不转发 F1–F12**（✅ 2026-10-29）；要用键盘模拟物理键必须
  `--keyboard=uhid`。uhid 会在设备上注册一只虚拟键盘（`/dev/input/event4`，name `scrcpy`，
  断开即消失），前提是设备有 `/dev/uhid` 且 shell 在 `uhid` 组
- uhid 下按键走**内核输入栈**，与物理按键同一条路；sdk 走系统 API 注入，功能键会丢
- 物理键在 Android 上常映射成 `KEYCODE_F1`/`F2`…：先 `adb shell getevent -pl` 看设备树与 `KEY (...)`
  能力位，再 `adb shell input keyevent <数字>` 逐个试。`sendevent` 直写 `/dev/input/*`
  一般被 SELinux 拒绝，没有 root 走不通
- 鼠标点击 = 触摸；滚轮 = `ACTION_SCROLL`，可驱动 `ScrollView`，也对应表冠的滚动轴
- 具体机型的键位（哪个数字是哪颗物理键、按下去做什么）属于设备事实，记在对应环境档案，
  不写进本技能
