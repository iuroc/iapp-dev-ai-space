---
name: gede-read-api
description: Use when building or porting a client for the 歌德电子书借阅机 content API (gede.5read.com) — listing books and magazines, fetching server-paged EPUB text, or reimplementing the 青简 reader on another platform (Android, iOS, desktop, web, watch, embedded). Triggers: 5read, gede.5read.com, 超星歌德, 借阅机, 青简, touchBook/books.jspx, magazineItems.jspx, epub_epubRead_readNew, surl, detailUrl, gedeid.
---

# 歌德借阅机内容 API

## 这是什么

`gede.5read.com` 是超星「歌德电子书借阅机」的内容服务。它没有公开文档，客户端靠**五个 HTTP GET**
串起「发现 → 目录 → 正文」：

| 能力 | 端点 | 返回 |
|---|---|---|
| 图书列表 | `/apis/touchBook/books.jspx` | JSON，`msg.list[]` |
| 期刊列表 | `/apis/magazine/magazines.jspx` | JSON，`msg.list[]` |
| 期刊期次 | `/apis/magazine/magazineItems.jspx` | JSON，`msg.itemList[]` |
| 阅读 token | `/o/a.h?a=GEDE:<surl>` | **HTML**，正则取 3 个字段 |
| 分页正文 | `/other/epub_epubRead_readNew.jspx` | JSON，`msg.contents[]` + `msg.catalogs[]` |

**默认目标**：`https://gede.5read.com`，`gedeid=84751638`（借阅机 ID，换馆必须换）。
新工程直接写死这两个默认值即可，但**只留一处常量**，不要散落在代码里。

本 skill 是**内部私有**：接口细节、`gedeid` 与 `detailUrl` 只在内部流转，不放进对外交付物。

**核心心智模型**：列表给你一本「书」（`surl`），token 页给你一张「借阅凭证」，正文接口按你声明的
虚拟阅读器尺寸把这本书切成页。**页码不是书的属性，是你选的尺寸的函数。**

✅ 2026-10-30 复测（批次 GEDE-P1）：契约与 2026-10-27/28 实测一致。

⚠ 同日补充：`/o/a.h` 会 **301 跳转**到 `gdread.sslibrary.com`，其余四个端点仍在 `gede.5read.com`
直接 200。HTTP 客户端必须跟随重定向（详见 `references/api-reference.md §5`）。

## 五分钟跑通

```
1) 图书列表   GET https://gede.5read.com/apis/touchBook/books.jspx
                  ?cataid=124&page=1&pageSize=2&gedeid=84751638
2) 取 surl    → msg.list[0].surl = "gede.5read.com/g/<id>.h"   （可能不带协议）
3) 阅读 token GET https://gede.5read.com/o/a.h
                  ?a=GEDE:<URL-encode 补全协议后的 surl>
4) 取目录     GET https://gede.5read.com/other/epub_epubRead_readNew.jspx
                  ?psize=0&page=1&w=1000&h=2000&ucatalog=true&ctype=3&fsize=18
                  &sid=<token.sid>&from=<token.from>&detailUrl=<URL-encode detailUrl>
5) 取正文     psize=30&page=1 起，按 30 页一段往后翻
```

第 4 步用 `psize=0` 是最省的「只取目录」方式：`contents` 返回空数组，`catalogs` 与 `pageAll`
仍然全量（实测 1262 B，比 `psize=1` 少带一条正文）。目录不受 `psize` 限制。
完整字段与错误码见 `references/api-reference.md §2-§6`，时序与分页数学见
`references/reading-flow.md §2`。

## 七条不变量（写代码前必须记住）

1. **`result == 1` 才读 `msg`**。`result == 0` 是服务端「没有数据 / 参数不对」，不是网络失败；
   `errorMsg` 是中文提示，不要拿来给用户看原样。
2. **`page` 是 1 基内容起点**，不是「第几个分段」。`page=31&psize=30` 取第 31–60 页。
   列表接口的 `pageSize=-1` 表示取全量（图书 466 条一次返回）。
3. **`catalogs[].page` 是页号，`contentIndex` 不是**。目录跳页用 `contents[catalog.page - 1]`；
   用 `contentIndex` 会跳到错页（青简旧版就踩过）。
4. **`w/h/fsize` 一经选定不可变**。服务端按它们重排整本书；换值后 `pageAll`、目录页号、
   分段边界全部对不上。同一本书：`1000×2000/18 → 84 页`，`400×400/18 → 487 页`。
5. **`surl` 可能不带协议**（图书是 `gede.5read.com/g/...`，期刊期次是 `https://gede.5read.com/g/...`）。
   先补 `https://` 再拼 token URL，否则 token 页返回错误页。
6. **列表接口没有搜索**。`keyword` 被服务端静默忽略（任意关键词都返回同一批全量结果）。
   搜索要么本地建索引，要么由你的后端代理。
7. **目录是树，不是平铺列表**。`pid == 0` 是顶层，子项在 `children[]` 里，可继续递归。
   **深度不是契约**：14 个样本里都 ≤ 2 层，但没有证据表明不会出现 3 层以上——
   客户端必须按递归实现，按最多 4 层预留。
   子项的 `page` 可能与父页相同（页内小标题，跳父页）或不同（独立目标），要按数据判断。

## 何时用 / 何时不用

**用**：要读这套借阅机的内容；要把青简类阅读器换到别的语言/系统/载体；要复现青简的分页与目录行为。

**不用**：iApp 工程本身的语法、投递、打包问题 —— 走 `iapp-development` 技能。
本技能只描述 HTTP 契约与接入方法，不含任何 iApp 专有写法。

## 导航

| 文件 | 内容 |
|---|---|
| `references/api-reference.md` | 端点全表、参数、返回字段、错误码、分类 ID、图片域名 |
| `references/reading-flow.md` | token → 目录 → 正文的完整时序、分页数学、HTML 形态与渲染配方 |
| `references/integration-guide.md` | 跨平台接入清单：HTTP/JSON/线程/缓存/本地索引/进度存储/Web CORS |
| `references/pitfalls.md` | 已知坑与失败签名，按「现象 → 原因 → 改法」编排 |

## 版本与前提

- 契约实测于 2026-10-27 至 2026-10-30，客户端为 Android（API 28/30/34）与宿主机直连两路。
- 服务端可能随时改版；客户端应把「`result != 1` + `errorMsg`」当作可上报的异常，而不是崩溃。
- 结论级别：✅ 表示两端都复现过；⚠ 表示单平台或单次读数，换载体前需重测；
  ❓ 表示未验证，文件里会写明怎么验。
