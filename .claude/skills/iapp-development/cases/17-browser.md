# 17 浏览器（实战：WebView 事件 / st_url / 返回栈）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 目标

B8 第二例：WebView 做浏览器，验证 `shouldoverrideurlloading` 的正确用法、事件参数 `st_url`、进度与返回栈。

## 工程

```
<包名>/
├── src/mian.iyu      # 地址栏 EditText + 前往 + 后退 + 状态行 + WebView
└── src/br.mjava      # 配置、加载、前进后退、进度、错误
```

WebView 绑定：

```xml
<eventItme type="onprogresschanged">call(null, "mjava", "br.progress")</eventItme>
<eventItme type="shouldoverrideurlloading">call(null, "mjava", "br.override", st_url)</eventItme>
<eventItme type="onpagefinished">call(null, "mjava", "br.finished")</eventItme>
<eventItme type="onreceivederror">call(null, "mjava", "br.error")</eventItme>
```

## 关键点

- `shouldoverrideurlloading` **一旦绑定，iApp 的默认跳转会 return true 被跳过**，必须在事件里自己 `loadUrl`
- 目标地址用 `st_url`；写 `url` 会退化成零参调用并报 `Method override() not found`
- 只在自己的 `loadUrl` 里处理 http(s)，其它 scheme（tel/mailto/自定义）留给系统或自己分派，避免死循环

## 实测读数

```
14:05:51.079 BR-UA Mozilla/5.0 (Linux; Android 9; 25060RK16C Build/PQ3A.190705.09211140; wv)
                AppleWebKit/537.36 ... Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36
14:05:53.916 BR-override url=https://www.baidu.com/
14:05:54.658 BR-finished title=百度一下 url=https://www.baidu.com/
14:06:05.379 BR-override url=https://example.com/next      ← 相对链接按 base 解析
14:06:05.942 BR-finished title=Example Domain url=https://example.com/next
14:06:33.870 BR-go https://i.2980.com
14:06:33.939 BR-override url=https://login.2980.com/authorize?…
14:06:34.465 BR-finished title=火星公共登录平台 url=https://login.2980.com/authorize?…
14:06:36.610 BR-back
14:06:36.711 BR-finished title=about:blank url=about:blank
```

## 结论

- `st_url` 拿到了完整目标地址，绝对链接、相对链接、JS/302 跳转都能接住
- 站点自身的登录跳转同样走 `shouldoverrideurlloading`，处理逻辑统一
- `canGoBack()/goBack()` 正常工作
- `onprogresschanged` 到 100 会回调**多次**（一次加载常见 3 次），别在 100 时做重活
- `loadDataWithBaseURL` 打开的本地页，`webView.getUrl()` 返回 `about:blank`（不是 base 地址）——本地页不要靠 `getUrl()` 判断当前页
- 本机 WebView 内核：Chrome 91.0.4472.114，前端可按 2021 年前后的能力写，别用太新的 CSS/JS
