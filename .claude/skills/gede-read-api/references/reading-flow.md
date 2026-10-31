# 阅读链路：从列表到正文

> 主文件：本文件负责时序、分页数学与正文渲染。端点字段以 `references/api-reference.md` 为准。

## 1. 全链路时序

```
列表 (books/magazines/magazineItems)
  │  拿 surl（可能不带协议）
  ▼
补协议 → https://<surl>
  │
  ▼
GET /o/a.h?a=GEDE:<urlencode(https://surl)>        ← HTML，约 11 KB
  │  正则取 sid / from / detailUrl
  ▼
（按 surl 缓存三件套，同一本书只取一次）
  │
  ▼
GET /other/epub_epubRead_readNew.jspx
      ?psize=0&page=1&w=1000&h=2000&ucatalog=true&ctype=3&fsize=18
      &sid=…&from=…&detailUrl=…
  │  msg.catalogs[] 全量目录 + msg.pageAll 总页数（contents 为空）
  ▼
按需分段：page = 起点，psize = 段长
  │  msg.contents[] 直接按页号放在数组里
  ▼
渲染 / 缓存 / 记进度
```

**关键点**：目录和总页数用 `psize=0` 一次拿全（`contents` 为空），之后每段只拉正文。这样一本书
= 1 次 token + 1 次目录 + ⌈pageAll/30⌉ 次正文。

✅ 2026-10-30 复测：图书（`pageAll=84`、目录 9 条）与期刊期次（`pageAll=54`、目录 30 条）两条链路各跑通一次。

## 2. 分页数学

### 2.1 `page` 是内容起点，不是段号

```
取第 N 页（单页）：      page=N,        psize=1
取第 N 页所在段（段长 S）：start = floor((N-1)/S)*S + 1,  page=start, psize=S
取全书：                 page=1,        psize=10000
```

验证读数（同一本书，2026-10-28）：

```
psize=10&page=1  → contents[0..9]
psize=10&page=2  → contents[0] == 上一段的 contents[1]      ← page 是起点，会重叠
psize=30&page=31 → 从第 31 条内容开始
```

所以 `page=2` **不是**第二段。分段时必须自己算 `start`。

### 2.2 页码由 `w/h/fsize` 决定

服务端按你声明的虚拟阅读器尺寸重排整本书，`pageAll` 和 `catalogs[].page` 一起缩放。

同一本书（2026-10-29 读数）：

| `w` × `h` | `fsize` | `pageAll` |
|---|---|---|
| 1000 × 2000 | 18 | 84 |
| 400 × 400 | 18 | 487 |
| 400 × 400 | 24 | 754 |
| 330 × 340 | 18 | 640 |
| 165 × 170 | 18 | 2195 |

**选型建议**：除非要做「按屏幕精确分页」，一律沿用手机参数 `w=1000&h=2000&fsize=18`。
理由：请求量少一个数量级；文字页本身无固定宽度，客户端会按视口重排；图片靠 CSS 压回。
换尺寸只对「必须按物理页翻页」（如小屏手表）有意义，代价是请求数暴涨。

**硬约束**：同一本书在整个 App 生命周期内只能用一组 `w/h/fsize`，否则书签、进度、目录全部错位。

### 2.3 分段取正文与跳页

段长 `S` 固定（常用 30），段起点按 1 基对齐：

```
start(p) = floor((p - 1) / S) * S + 1
          page = start(p),  psize = S
          contents 下标记为  p - start(p)
```

| 目标页 | 请求 |
|---|---|
| 1–30 | `page=1&psize=30` |
| 31–60 | `page=31&psize=30` |
| 181–210 | `page=181&psize=30`（阅读到 185 页时跳转也只取这一段） |

- **缓存键 = `surl` + `w/h/fsize` + `start`**；同一段只拉一次
- 跳页（历史进度、目录）只取目标所在的那一段，**不要从第 1 页重新拉**
- 最后一段可能不满 `S` 条（实测 84 页的书：`page=61&psize=30` 只返回 24 条）
- `page > pageAll` 返回 `result:1` + 空数组，不是错误；请求前先夹到 `[1, pageAll]`
  （见 `references/api-reference.md §6`）

✅ 2026-10-30 实测（84 页的书，`page=1/31/61` 三段分别返回 30/30/24 条，共 115/176/82 KB）。

### 2.4 `fsize` 的语义

⚠ 未定：从读数看它更像「虚拟字号档」而不是像素值（`fsize` 从 18 升到 24，页数从 487 涨到 754）。
换尺寸前先按 `references/api-reference.md §9` 的验法扫一遍，不要凭猜测换算。

## 3. 目录语义

`catalogs[]` 是**完整**目录，与 `psize` 无关，且**分两层**（顶层项 + `children[]`）。
层级与子项页码的两种形态见 `references/api-reference.md §6`「目录层级」——
子项页码可能与父页相同（只是页内小标题），也可能不同（可独立跳转）。

```
第 i 个目录项 → 页号 p = catalogs[i].page      （1 基）
              → contents 下标 = p - 1
```

**不要用 `contentIndex`**。它是章节在书内的序号，不是页号。真实读数：

```
catalogs:  page=1   contentIndex=0   封面
           page=2   contentIndex=1   前折页
           …
           page=82  contentIndex=6   后记     ← 页号与 contentIndex 早已分叉
           page=84  contentIndex=8   封底
```

青简旧版用 `contentIndex` 做跳页，点击「第 100 页」实际落在第 20 页。修法：`idx = page - 1`，
再夹在 `[0, contents.length - 1]`。

✅ 2026-10-28（QJ-P3）+ 2026-10-30 复测（节选 9 条目录）。

## 4. 正文 HTML 形态与渲染

`contents[]` 的每个元素是一页 HTML 片段，不是完整文档。

**文字页**：

```html
<div class="text"><div><p>正文…</p></div></div>
```

- 无内联宽度，天然按视口重排
- 排版靠客户端注入的 CSS 控制

**图片页**：

```html
<div class="text"><div style="text-align:center;…">
  <img width="973" height="1392" src="https://gdepub.sslibrary.com/…/Cover.jpg"/>
</div></div>
```

- `src` 是**绝对 URL**，无需拼 base
- `width/height` 是死值，直接渲染会撑破屏幕

渲染配方（WebView / 浏览器 / 任意 HTML 容器通用）：

```css
html,body{margin:0;padding:0;}
body{font-size:18px;line-height:1.8;padding:0 20px;overflow-x:hidden;}
img{max-width:100%!important;height:auto!important;}
```

- 必须覆盖 `img` 的 `width/height`，否则宽图横向溢出
- 关闭横向滚动条与横向手势
- 视口 meta 用 `width=device-width, initial-scale=1`
- 内嵌容器用「加载完成回调 + 延迟 300ms 再滚动到顶部」；`loadDataWithBaseURL` 是异步的
- 保存 base URL 为 `https://gede.5read.com/`，以防未来出现相对路径资源

✅ 2026-10-29（WATCH-3/4，API 30 + API 34）+ 2026-10-30 复测（图片绝对 URL）。

## 5. 缓存与断点续读

建议缓存三层，都是「可重新拉取」的：

| 层 | 键 | 内容 | 失效 |
|---|---|---|---|
| token | `surl` | `sid` / `from` / `detailUrl` | 正文返回 `result:0` 时清掉重取 |
| 目录 | `surl` + `w/h/fsize` | `pageAll` + `catalogs[]` | 同上 |
| 正文段 | `surl` + `w/h/fsize` + `start` | `contents[]` | 同上 |

进度只存「页号」不够，必须同时存 `w/h/fsize` 与 `pageAll`；否则换设备/换排版参数后页号失真。
青简的做法是存 `{surl, page, pageAll, params, updatedAt}`，恢复时若 `params` 不一致就按比例换算。

✅ 2026-10-28/29：阅读历史落盘与断点续读在 API 34 与 API 30 上均跑通（WATCH-3/4）。
