# WebView 全前端 + mjava 桥接

**版本前提**：iApp 5.0.1013 / API 34（雷电 14）；开发模式与打包 APK 均实测 ✅（2026-10-31）。
**适用**：界面 100% 用 HTML/CSS/JS 写，系统能力（文件、权限、Intent、系统栏…）全部放进 mjava。
**不适用**：已有原生控件页面的局部 WebView（那类页面照旧用 mjava 建树 + `us(v,"url",…)`）。

## 0. 结论速览

| 问题 | 结论 | 级别 |
|---|---|---|
| 界面能否全部放 WebView | 能。`.iyu` 只留根容器 + 一个 WebView 控件，其余全在 HTML 里 | ✅ |
| JS 能否调 mjava | 能，但要走 **URL scheme + `shouldoverrideurlloading`**；是异步 RPC | ✅ |
| mjava 能否调 JS | 能，`i.has(webView, "语句")` | ✅ |
| `i.hsas` 注入的 `window.iapp.fn/fn2` 能否调 mjava | **不能**，它只认 yul 模块调用 `a.b(...)`（去找 `a.myu`） | ✅ 失败签名 |
| 本地页面开发 / 打包两种形态 | 开发读工程 `res/`；打包读 APK 内 `assets/res/` | ✅ |
| 跨域 fetch/XHR 能否绕过 | 能：页面以 `file://` 加载 + `setAllowUniversalAccessFromFileURLs(true)`；https base 下被 CORS 拦 | ✅ |
| 状态栏跟随 Web 主题 | 改宿主 a0 背景 + `WindowInsetsController` 图标明暗 | ✅ |

## 1. 为什么 WebView 要写在 `.iyu` 里

`shouldoverrideurlloading` 是 iApp 的**控件事件**，只能在 `.iyu` 的 `<event>` 块里绑。
mjava 里 `new WebView(activity)` 建出来的实例没有 id，也没有事件入口，绑不上这个事件。

所以这里与「mjava 建树」的默认做法不同：**根容器和 WebView 留在 `.iyu`，WebView 的配置、
前端文件加载、桥接和全部业务逻辑在 mjava**。控件本身不写任何样式之外的逻辑。

## 2. `.iyu` 骨架

```xml
<View id="1" did="0" type="FrameLayout">
<ppt>width=-1
height=-1
backgroundcolor=#0B0E14</ppt>
<event></event>
</View>
<View id="2" did="1" type="WebView">
<ppt>width=-1
height=-1
backgroundcolor=#0B0E14</ppt>
<event><eventItme type="shouldoverrideurlloading">call(null, "mjava", "app.onUrl", st_url)</eventItme></event>
</View>
<UIEventset><eventItme type="loading">
call(null, "mjava", "app.boot")
</eventItme></UIEventset>
```

- `WebView` 是内置短名（`android.webkit.WebView`），不用 `build.xml` 登记
- 事件变量必须写 `st_url`；写 `url` 会退化成零参调用，mjava 收不到地址
- 绑了 `shouldoverrideurlloading` 之后，**所有** scheme 的跳转都会被你的代码接住并 `return true`；
  默认的 `http/https → loadUrl`、其它 scheme → `ACTION_VIEW` 全部失效。这是桥接的前提，不是副作用

## 3. mjava：配置 WebView 并加载本地页面

```java
public void boot() {
	WebView wv = (WebView) activity.findViewById(2);
	WebSettings ws = wv.getSettings();
	ws.setJavaScriptEnabled(true);
	ws.setDomStorageEnabled(true);
	ws.setAllowFileAccess(true);
	ws.setAllowFileAccessFromFileURLs(true);
	ws.setAllowUniversalAccessFromFileURLs(true);
	ws.setUseWideViewPort(true);
	ws.setSupportZoom(false);          // 缩放是 WebSettings 的能力，不是 WebView 的
	i.sss("wv", wv);                   // 跨 call 存 WebView
	String html = webHtml();
	wv.loadDataWithBaseURL("https://webview.local/", html, "text/html", "utf-8", null);
}
```

- WebView 存 `i.sss`，后续 `onUrl` / `i.has` 都从这里取
- `loadDataWithBaseURL` 的 base URL 给一个 https 地址：页面 origin 稳定，`localStorage` 可用；
  之后 `getUrl()` 返回的是这个 base，不要拿它判断当前页面
- **安全边界**：`setAllowUniversalAccessFromFileURLs(true)` 会跳过 file:// 页面的 CORS 检查，
  等于把本地文件的读取能力开放给页面。它只适用于「只加载本地页面」的 WebView；**绝不能让这个
  WebView 打开远程页面**。本配方用 `shouldoverrideurlloading` 吞掉所有导航、只放行 `iapp://` 桥，
  页内也不要渲染可点击的外部链接

### 本地前端文件的两种形态

| 形态 | 位置 | 读法 |
|---|---|---|
| 开发模式 | `<工程根>/res/web.html` | 普通 `File` 读 |
| 打包产物 | APK 内 `assets/res/web.html` | `activity.getAssets().open("res/web.html")` |

`res/` 在两种形态下的位置与其它资源（图片等）的读取方式见 `recipes.md` §工程 res/ 图片。

```java
public String devRoot() {
	try {
		Class vd = activity.getClassLoader().loadClass("com.iapp.app.VisualDesigner");
		Object r = vd.getField("a9").get(null);
		if (r != null) {
			return String.valueOf(r);
		}
	} catch (Throwable t) {
	}
	return "";
}
```

- 打包后 `VisualDesigner` 被裁掉，`loadClass` 抛 `ClassNotFoundException` 是**正常分支**，用它区分两种形态
- 先试开发路径，读不到再走 `assets`；两条路径的 HTML 是同一份源码，不需要改代码
- `res/` 里的 HTML/CSS/JS 不参与 R 资源编译，只是「随包带走的文件目录」

## 4. JS → mjava：URL scheme

### 4.1 前端

```js
function rpc(req) {
	return new Promise(function (resolve, reject) {
		var id = 'q' + (++reqSeq);
		pending[id] = { resolve: resolve, reject: reject };
		var payload = b64url(JSON.stringify({ id: id, req: req }));
		window.location.href = 'iapp://r/' + payload;
		setTimeout(function () {
			if (!pending[id]) return;
			delete pending[id];
			reject(new Error('原生响应超时'));
		}, 4000);
	});
}

window.__nativeResult = function (id, b64) {
	var cb = pending[id];
	if (!cb) return;
	delete pending[id];
	cb.resolve(JSON.parse(b64urlDecode(b64)));
};
```

要点：

- payload 放 **path**（`iapp://r/<base64url>`），host 固定为短串：host 大小写会被 URL 规范化
- 用 base64url（`A-Z a-z 0-9 - _`）编码：没有 `+ / =`，不会被 URL 转义，也不受 yul 字符串特殊字符影响
- **同一时刻不要连发两个 `location.href`**：后一个可能覆盖前一个，前一个请求丢失。需要并发就给请求排队
- 前端必须有超时兜底；`shouldoverrideurlloading` 没绑对时不会有任何报错

### 4.2 mjava 入口

```java
public void onUrl(Object uObj) {
	String url = uObj == null ? "" : String.valueOf(uObj);
	String prefix = "iapp://r/";
	if (!url.startsWith(prefix)) {
		return;
	}
	String id = "";
	String out;
	try {
		byte[] raw = Base64.decode(url.substring(prefix.length()), 11); // URL_SAFE|NO_WRAP|NO_PADDING
		JSONObject p = new JSONObject(new String(raw, "UTF-8"));
		id = p.optString("id", "");
		out = dispatchText(p.optString("req", "{}"));
	} catch (Throwable t) {
		out = errJson("onUrl: " + t);
	}
	if (id.length() == 0) {
		return;
	}
	pushResult(id, out);
}
```

- `shouldoverrideurlloading` 回调在 UI 线程，`i.has` 可以直接调
- 回调里做文件 IO 会阻塞 UI；重活自己开线程，**算完回主线程再 `i.has`**（`i.has` 内部是
  `WebView.loadUrl`，只能在主线程调，见 §5）
- base64 用 `android.util.Base64`，flag 传 `11`（API 21 也有；`java.util.Base64` 要 API 26+）

### 4.3 不要用 `window.iapp.fn/fn2` 调 mjava

`i.hsas(wv, true)` 注入的 `window.iapp` 只有 `fn / fn2 / g / s`，它的执行器把代码按
`函数名(参数…)` 解析，查不到就把第一个 `.` 之前的前缀拼 `myu` 去加载 **yul 模块文件**（`a.myu`）。

```java
// 这样写会失败
i.hsas(wv, true);
// JS: iapp.fn2('call(r, "mjava", "app.dispatch", sss.req)', 'r')
```

失败签名与逐层解析见 `pitfalls.md` #48；最关键的一行是：

```
java.lang.NumberFormatException: For input string: "call(r, "mjava", "app.myu"
```

它把 `"app.dispatch"` 当模块名去拼 `app.myu` 了。所以 `window.iapp` 适合
「JS 调 yul 模块」，不适合「JS 调 mjava」；要调 mjava 用上面的 URL scheme。

## 5. mjava → JS：`i.has`

```java
i.has(webView, "window.__nativeResult && window.__nativeResult(\"q1\", \"" + b64 + "\")");
```

- `i.has(Object, String)` 内部是 `webView.loadUrl("javascript:{ 你给的语句 };")`；
  传**语句**，不要带 `<script>`，也不要带外层 `javascript:` 前缀
- 语句里用 `&&` 做存在性判断，避免页面还没定义回调时报错
- 回传 JSON 同样建议 base64url，避开引号、换行和中文转义
- 这个通道是「通知式」的：mjava 主动推，JS 用全局函数接
- **`i.has` 只能在主线程调**：内部是 `WebView.loadUrl`，子线程调用会抛
  `RuntimeException: A WebView method was called on thread 'Thread-N' ...`
  ✅（2026-10-31）。在子线程算完结果后要 `activity.runOnUiThread(new Runnable(){...})`
  回到主线程再 `i.has`
- 子线程的匿名 `Runnable` 里**不要直接调本模块方法**（BeanShell 线程闭包找不到，
  `Command not found` 会杀进程）；要么全部内联，要么在闭包第一行 `i.fn("模块名")`

## 6. 跨域与网络请求（实测矩阵）

同一份页面分别在两种加载方式下请求一个**不返回 `Access-Control-Allow-Origin` 的公共接口**
（探针用的是一次性测试页，接口可换成任意同类服务）：

| 加载方式 | fetch 直连 | XHR 直连 | fetch no-cors | img | mjava 原生代理 |
|---|---|---|---|---|---|
| `file://` + `setAllowUniversalAccessFromFileURLs(true)` | ✅ 200 可读（type=basic） | ✅ 200 可读 | ⚠ type=basic（本探针未读 body） | ✅ | ✅ |
| `https://webview.local/`（`loadDataWithBaseURL`） | ❌ `TypeError: Failed to fetch` | ❌ onerror | ⚠ type=opaque（body 不可读） | ✅ | ✅ |

结论：

- **需要跨域读数据时，让页面以 `file://` 加载并开 `setAllowUniversalAccessFromFileURLs(true)`**：
  这个开关会让 WebView 跳过 file:// 页面的 CORS 检查，普通 fetch/XHR 直接读到 JSON ✅
- 用 `loadDataWithBaseURL` 给 https base 时等同普通网页，CORS 照常执行；要读跨域 JSON
  只能靠服务端 ACAO、JSONP，或走原生代理
- `img` 不受 CORS 限制（能显示，不能读像素）
- `no-cors` 在 https base 下是 opaque、body 不可读；`file://` 模式下返回 type=basic，
  本探针**没有读 body**，是否可读未验 ❓ 怎么验：在 file 模式对 no-cors 响应调 `text()`，
  看是否抛错
- 原生代理是两种模式都能用的兜底
- **打包产物同理**：页面以 `file:///android_asset/res/net.html` 加载时，universal access 仍然生效，
  直连 fetch/XHR 照样能读；https base 照样被拦（✅ 2026-10-31 打包实测）

### 原生代理的线程写法

`shouldoverrideurlloading` 回调在 UI 线程，主线程做 HTTP 会
`NetworkOnMainThreadException`；`i.has` 又只能在主线程。所以固定是「子线程算 + 回主线程推」：

```java
public void httpAsync(String id, String url) {
	Thread th = new Thread(new Runnable() {
		public void run() {
			// 闭包里不要调本模块方法：HTTP / JSON / Base64 全部内联
			String out = "...";   // 请求并组好 JSON
			String b64 = Base64.encodeToString(out.getBytes("UTF-8"), 11);
			String payload = "window.__nativeResult && window.__nativeResult(\"" + id + "\", \"" + b64 + "\")";
			activity.runOnUiThread(new Runnable() {
				public void run() {
					i.has(wvo, payload);
				}
			});
		}
	});
	th.start();
}
```

- 匿名接口实现可以读方法形参与局部变量，**不需要 `final`** ✅（API 34）
- 前端仍是异步 RPC：结果经 `i.has` 回来，Promise 正常 resolve
- 三层超时都要有：前端（15 s）、connect（8 s）、read（12 s）
- 接口是 `http://` 时给 `WebSettings.setMixedContentMode(0)`（ALWAYS_ALLOW）；`https` 不用

## 7. 状态栏与主题（WebView 在外，状态栏在更外）

状态栏那一条 72px 画的是宿主内容容器 `a0` 的背景（见 `status-bar-guide.md` §0），
**不是 WebView、也不是页面 CSS 能改到的**。所以 Web 端切主题时，必须同时通知 mjava：

```java
public String themeJson(String mode) {
	boolean light = "light".equals(mode);
	int c = Color.parseColor(light ? "#F5F7FB" : "#0B0E14");
	View rootView = activity.findViewById(1);
	View parent = (View) rootView.getParent();
	if (parent != null) {
		parent.setBackgroundColor(c);          // 状态栏区域 = 页面底色
	}
	((WebView) i.sss("wv")).setBackgroundColor(c);
	WindowInsetsController wic = activity.getWindow().getInsetsController();
	if (wic != null) {
		int mask = WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS;
		wic.setSystemBarsAppearance(light ? mask : 0, mask); // 浅底深图标 / 深底白图标
	}
	// 返回 {"ok":true,"mode":"light|dark"} 给前端
}
```

- 只改 CSS 不改 a0：状态栏区域会和页面脱节，出现一条异色带
- 「透明状态栏 + 顶上留出状态栏间距」= a0 背景改成页面底色；不要挂 DecorView 铺满，
  铺满后 WebView 会盖到状态栏下面，还得自己算 insets
- 前端切换时发一次 `{op:"theme", mode:"light|dark"}`，选择存 `localStorage`；页面 `<head>` 里
  先按存储值设 `data-theme`，避免先闪一下深色

## 8. 资源与投递

- 前端建议先做**单文件**（CSS/JS 内联在 `res/web.html`），`loadDataWithBaseURL` 一次读完，
  没有相对路径与 file:// 权限问题
- 要多文件（`res/web/index.html` + `app.css` + `app.js`）：打包后整个 `res/` 在
  `assets/res/`，但用 adb 整目录推送时，`adb push` **不会**在
  `/sdcard/Android/data/<pkg>/` 下自建多级目录，会报
  `remote secure_mkdirs failed: Operation not permitted`；推之前先 `adb shell mkdir -p`
  每个远端子目录，或把前端文件平铺成 `res/web.html`
- 改动 mjava / HTML 后要重新加载页面；WebView 不会热更新

## 9. 未验 / 边界

- `us(wv, "url", "@web.html")` 和 `%web.html` 这类 HTML 路径写法未验 ❓；
  怎么验：把同一份 HTML 放 `res/`，分别用 `us(wv,"url","@web.html")` 与
  `file:///android_asset/res/web.html` 两种写法，在开发模式与打包产物各跑一次
- 大载荷（几百 KB JSON）走 URL scheme 未验 ❓；怎么验：造一个 >100 KB 的 JSON 走一次
  `iapp://` 调用，看是否被截断或返回失败。桥适合小请求，大内容走文件读写
- 返回键未绑定 `downkey`；页面内自己维护返回栈，或把 `downkey` 事件转给 JS（`i.has`）
- 软键盘 / IME 与底部输入面板的遮挡未验 ❓；怎么验：真机或带虚拟键盘的模拟器，在 Web 输入框
  聚焦时看输入框和按钮是否被键盘盖住（WebView 的 `adjustResize` 行为随宿主主题变化）
- WebView 内核随设备变化，老设备按 Chrome 91 设保守下限；API 28 未覆盖（版本政策只做有限兼容），
  怎么验：在 API 28 设备上重跑本页探针，不要求与 API 34 追平
