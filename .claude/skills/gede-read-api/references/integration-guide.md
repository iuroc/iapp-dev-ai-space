# 跨平台接入指南

> 主文件：本文件负责「换语言、换系统、换载体时怎么做」。契约本身见
> `references/api-reference.md`，阅读链路见 `references/reading-flow.md`。

## 0. 内部约束

- 本 skill 属**内部私有**：接口细节、`gedeid`、`detailUrl` 只在内部流转，不放进对外交付物。
- 这套接口是**机构借阅服务的私有后端**，没有公开文档，也没有稳定的兼容承诺。
- 换机构 = 换 `gedeid`，馆藏与分类都可能不同，`api-reference.md §7` 的数量**不能当常量**。
- 服务端随时可能改版。客户端把「`result != 1`」当可上报异常，而不是崩溃。

## 1. 任何语言的最小接入清单

只需要四样东西，没有 SDK、没有签名：

| 需要 | 说明 |
|---|---|
| HTTP GET + 查询串编码 | 所有端点都是 GET；`detailUrl`、`surl`、`sid` 必须 URL-encode |
| JSON 解析 | 列表/正文端点；注意 `Content-Type` 是 `text/html`，**不能按 header 判断类型** |
| 正则 | 仅用于 `/o/a.h` 的 HTML，取 3 个字段 |
| HTML 渲染容器 | WebView / WKWebView / CEF / 浏览器 iframe / 自写渲染器 |

**没有 Cookie 会话、没有 OAuth、没有请求签名**；不要引入不必要的 HTTP 客户端特性。

## 2. 网络与线程

- 所有请求是**同步阻塞**的，单次 100 ms–2 s；一律放后台线程/协程，UI 线程只收结果。
- 一次阅读会话的请求量：`1 token + 1 目录 + ⌈pageAll/30⌉ 正文`。
  按手机参数，一本 300 页的书约 12 个请求。
- 列表全量索引：11 个图书分类 + 7 个期刊分类，共 18 个请求（每个 `pageSize=-1`）。
  串行发、间隔 100–200 ms，避免瞬时并发。
- 设 10–20 s 超时；失败重试 1 次即可，不要指数退避堆积。

## 3. 数据模型

客户端只需要一个最小模型，字段名建议直接沿用服务端，减少映射错误：

```text
Item     { key, type("ebook"|"magazine"|"issue"), title, author, summary, cover, surl, extra }
Catalog  { title, page, level }
Progress { surl, page, pageAll, params{w,h,fsize}, updatedAt }
```

- `key` 取值：图书用 `bookNum`，期刊用 `"m"+id`，期次用 `magazineItemNum`
- 详情页**没有独立接口**：书名、作者、简介、封面全部来自列表项。列表里没拿到的字段，
  详情页也拿不到，不要设计「进详情再拉一次」的流程
- 期刊是三层：期刊（`magazines`）→ 期次（`magazineItems`）→ 正文（`surl` 属于某个期次）

## 4. 搜索：服务端没有，必须自己做

`books.jspx` 的 `keyword` 被静默忽略（任意关键词返回同一批结果）。可选三条路：

| 方案 | 做法 | 代价 |
|---|---|---|
| 本地全量索引 | 首次进搜索页时后台拉 18 个分类（`pageSize=-1`），按 `key` 去重落盘，之后本地按标题/作者/简介过滤 | 首次 18 个请求，约 4000 图书 + 500 期刊；存储几百 KB |
| 自建后端代理 | 你的服务器拉全量、建索引、提供搜索 API | 需要运维 |
| 只用分类浏览 | 不做搜索，搜索框改「分类入口」 | 功能缩水 |

推荐本地全量索引：实现简单、离线可用、不依赖第三方。索引要带版本号与更新时间，
隔一段时间（如 7 天）后台刷新一次。

✅ 2026-10-28（QJ-P2）：参数扫 `keyword / name / title / q / key / word / searchKey / searchText / kw / value / bookName`
全部返回同一 `allCount`；路径扫 `search.jspx` / `searchBook.jspx` / `/apis/search/*` 全部 `结果路径错误`。

## 5. 阅读器实现

最小的分页阅读器需要：

1. **目录抽屉**：`catalogs[]` 列表，点击跳 `page-1`
2. **正文容器**：渲染一页 HTML，注入 `reading-flow.md §4` 的 CSS
3. **翻页**：上一页/下一页 = 在当前段内移动下标；跨段时按 `start` 规则拉新段
4. **进度**：离开时写 `Progress`，进入时若 `params` 一致就直达，否则按比例换算
5. **字号切换**：改的是**客户端 CSS 的字号**，不是 `fsize`。
   `fsize` 只在「重新向服务端分页」时才变；两者不要混用

**分页 vs 滚动**：服务端给的是「按固定虚拟尺寸切好的页」。客户端可以：

- 严格分页：一屏一页，尊重 `page`（青简手机版）
- 连续滚动：把整段 `contents[]` 拼起来当长文档，页码只用来记进度
- 小屏/手表：沿用 `1000×2000` 参数 + CSS 缩放，不要改 `w/h`（请求量会涨 20 倍）

## 6. 平台差异

| 载体 | 要点 |
|---|---|
| Android | `WebView.loadDataWithBaseURL("https://gede.5read.com/", html, "text/html", "utf-8", null)`；关横向滚动条；`loadDataWithBaseURL` 是异步的，翻页后延迟 300 ms 再 `scrollTo(0,0)` |
| iOS | `WKWebView.loadHTMLString(html, baseURL:)`；同样需要 viewport meta 与 CSS 覆盖 |
| 桌面 | WebView2 / CEF / Electron 均可；也可用原生 HTML 渲染库，但 CSS 覆盖要自己实现 |
| **Web 浏览器** | ⚠ 服务端**无 CORS 头**，跨域 `fetch` 会被拦。必须自建同源代理，或只在服务端渲染后回传 HTML |
| 手表 / 小屏 | 沿用手机分页参数，内容会按视口重排；图片靠 `max-width:100%` 压回 |
| 墨水屏 | 同上；避免动画与渐变，正文用纯色背景 |

⚠ 2026-10-30：CORS 为单次读数（自定义 `Origin` 的 GET），换馆/CDN 后需重测；
默认按「浏览器不可直连」设计。

## 7. 自测清单

接入完成前，逐条跑一遍：

- [ ] 图书列表 `cataid=124&pageSize=2` 返回 `result:1` 且 `allCount>0`
- [ ] `pageSize=-1` 能一次拿全量，且 `pageCount` 为 `null`（正常现象）
- [ ] 空分类（`cataid=123`）返回 `result:0` 且客户端不崩
- [ ] `surl` 不带协议时能正确补全
- [ ] token 页三个字段都能取到；同一 surl 第二次不重复请求
- [ ] `psize=0` 能拿到完整 `catalogs` 与 `pageAll`（`contents` 为空）
- [ ] 目录第 i 项跳 `catalogs[i].page - 1`，不是 `contentIndex`
- [ ] `w/h/fsize` 全 App 只有一处常量
- [ ] 图片页不横向溢出
- [ ] 关掉再进，进度能续上

## 8. 失败排查顺序

1. `result` 是不是 1 → 看 `errorMsg`
2. `detailUrl` / `sid` / `from` 是否原样、是否 URL-encode
3. `surl` 是否补了协议
4. `w/h/fsize` 是否与上次一致
5. 页码是否用了 `contentIndex`

更多现象对照见 `references/pitfalls.md`。
