# 歌德借阅机 API 参考

> 主文件：本文件是端点契约的唯一权威。其他文件只写指针。
> 级别与来源写在每节末尾。✅ = 2026-10-30 复测（批次 GEDE-P1）与 2026-10-27/28 实测一致。

## 1. 通用约定

| 项 | 值 |
|---|---|
| 基址 | `https://gede.5read.com` |
| 方法 | 全部 `GET`，无 POST |
| 认证 | **无**。没有登录、token、签名、Cookie 依赖 |
| 借阅机 ID | `gedeid=84751638`（配置项，换馆必换） |
| 响应类型 | `Content-Type: text/html;charset=UTF-8`，**正文是 JSON 或 HTML**，不是 `application/json` |
| 字符集 | UTF-8（`Content-Type` 声明与实际字节一致） |
| CORS | **无** `Access-Control-Allow-Origin`；浏览器跨域 `fetch` 会被拦，需自建代理或同源部署 |

**两个默认值的来源**：青简工程把 `gede.5read.com|84751638` 与固定密钥做 XOR，以整数数组存进
`net_decoded()` 运行时还原（只避免源码明文，不防抓包）。新客户端**不需要**这套混淆，直接用上表默认值；
内部复核时按同一数组解回即可。skill 属内部私有，这两个值不随对外交付物外传。

响应信封（JSON 端点通用）：

```json
{ "result": 1, "msg": { ... } }
{ "result": 0, "errorMsg": "没有获取到数据" }
```

- `result == 1`：读 `msg`
- `result == 0`：**业务空/参数错**，读 `errorMsg`。这是正常 HTTP 200，不要当网络错误重试
- 观察到的 `errorMsg`：`没有获取到数据`、`magazineid参数不符合要求，请确认`、`接口路径错误，请重试`

⚠ 2026-10-30：CORS 无头为单次读数（GET + 自定义 Origin），换 CDN 或换馆需重测。

## 2. 图书列表 `/apis/touchBook/books.jspx`

| 参数 | 必填 | 说明 |
|---|---|---|
| `cataid` | 是 | 分类 ID，见 §7 |
| `page` | 否 | 1 基页码，默认 1 |
| `pageSize` | 否 | 每页条数；`-1` = 全量 |
| `gedeid` | 是 | 借阅机 ID |
| `keyword` | **无效** | 服务端忽略；任意值返回同一结果 ✅ |

响应：

```json
{"result":1,"msg":{"page":1,"pageSize":2,"pageCount":233,"allCount":466,"list":[…]}}
```

`list[]` 字段（26 个，常用如下）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `bookNum` | string | 书目号，如 `HYB11735982`；客户端天然主键 |
| `title` | string | 书名 |
| `author` | string | 作者（含「著」字） |
| `summary` | string | 简介。**详情页唯一的简介来源**，没有独立详情接口 |
| `cover` | string | 封面 URL（`unicover.duxiu.com`，长 query） |
| `bcover` | string | 备用封面 URL |
| `ftpcover` / `ftpbcover` | string | `resource.superlib.com` 的小图/大图 |
| `surl` | string | **阅读入口**，形如 `gede.5read.com/g/<hash>.h`，不带协议 |
| `bookNum` / `isbn` / `publish` / `price` / `pageNum` | string/number | 元信息 |
| `newbook` / `hotbook` | int | 0/1 标记 |
| `type` | string | 如 `HY` |
| `urlid` / `urlIdKey` | int/string | 服务端内部 ID |

✅ 2026-10-27 首次普查，2026-10-30 复测字段一致。

## 3. 期刊列表 `/apis/magazine/magazines.jspx`

参数同 §2（`cataid` / `page` / `pageSize` / `gedeid`；`keyword` 同样无效）。

```json
{"result":1,"msg":{"page":1,"pageSize":1,"pageCount":27,"allCount":54,"list":[…]}}
```

`list[]` 字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | **数字 ID**，是查期次的唯一入参 |
| `magazineNum` | string | 刊号，如 `MZ11000014`；**不能**用于 `magazineid` |
| `name` | string | 刊名 |
| `ISSN` | string | 国际刊号 |
| `CN` | string | 国内刊号 |
| `summary` | string | 简介 |
| `coverPath` | string | 封面完整 URL（`gdfile.superlib.com`） |
| `surl` | string | 期刊级阅读入口（不带协议） |

✅ 2026-10-30 复测。

## 4. 期刊期次 `/apis/magazine/magazineItems.jspx`

| 参数 | 必填 | 说明 |
|---|---|---|
| `magazineid` | 是 | **纯数字** `id`；传 `MZ…` 号会报 `magazineid参数不符合要求` |

响应：

```json
{"result":1,"msg":{"magazine":{…},"itemList":[…]}}
```

- `msg.magazine`：与 §3 的 `list[]` 同构
- `msg.itemList[]`：每个元素是一「期」

| 字段 | 类型 | 说明 |
|---|---|---|
| `magazineItemNum` | string | 期次号，如 `MZ12038766`；期次级主键 |
| `issue` | string | 展示用期号，如 `2023年第23期` |
| `name` | string | 刊名 |
| `coverPath` | string | 该期封面完整 URL |
| `surl` | string | **该期的阅读入口，带 `https://` 前缀**（与图书不同） |
| `magazineid` | int | 回指期刊 |
| `sort` | string | 排序键，如 `20232300`（倒序即最新在前） |
| `codeImg` | string | 二维码图片 URL |
| `id` | int | 期次数字 ID |

✅ 2026-10-27 首次普查，2026-10-30 复测。

## 5. 阅读 token `/o/a.h?a=GEDE:<surl>`

**这是唯一返回 HTML 的端点**，不能按 JSON 解析。

> ⚠ **该端点会 301 跳转**到 `https://gdread.sslibrary.com/o/a.h?...`（实测 2026-10-30）。
> Android `HttpURLConnection` 的 GET 默认跟随重定向，**不要关掉**
> `setInstanceFollowRedirects(false)`；不跟随的客户端只会拿到 216 B 的 301 页面，
> 正则一个字段也取不到。其余四个端点仍在 `gede.5read.com` 上直接 200。

| 参数 | 值 |
|---|---|
| `a` | 固定前缀 `GEDE:` + URL-encode 后的**完整** surl（含 `https://`） |

页面约 11 KB，正文里含一段 `InitData` 配置。用正则取三个字段：

```
detailUrl:\s*'([^']+)'
sid:\s*'([^']*)'
from:\s*'([^']*)'
```

| 字段 | 图书示例 | 期刊期次示例 | 用途 |
|---|---|---|---|
| `sid` | `HYB11735982` | `MZ12038766` | 正文接口身份 |
| `from` | `4` | `5` | 正文接口来源标识 |
| `detailUrl` | 144 字符密文 | 160 字符密文 | 正文接口凭证，**必须原样回传** |

- 三个字段缺一即失败；拿到后**按 surl 缓存**，同一本书只换一次
- 不需要 Cookie，换 IP/换 UA 均可
- `detailUrl` 是密文，客户端不要试图解码或构造，原样 URL-encode 回传即可

✅ 2026-10-30 复测（图书 + 期刊期次各一次）。

### 书不存在：HTTP 200 + 400 错误页，**没有**三个字段

伪造一个不存在的 surl，该端点不会报 HTTP 错误，而是跟随重定向落到
`https://gdread.sslibrary.com/error/error400.jsp`：

| 读数（2026-10-31 实测） | 值 |
|---|---|
| HTTP 状态码 | `200` |
| 页面 `<title>` | `400` |
| 正文 | 「未查询到相关图书的 idKey 参数错误…」 |
| `sid` / `from` / `detailUrl` | **三个都取不到** |

客户端价值：这是区分「网络失败」与「书/期次不存在」的可靠判据——

- **网络失败**：请求本身失败（非 2xx、超时、DNS/连接异常）
- **资源不存在**：请求成功（200），但没有令牌字段

两者对用户的处理完全不同（前者可重试，后者应提示书已下线），不要合并成一句「加载失败」。

## 6. 分页正文 `/other/epub_epubRead_readNew.jspx`

| 参数 | 必填 | 说明 |
|---|---|---|
| `sid` | 是 | 来自 §5 |
| `from` | 是 | 来自 §5 |
| `detailUrl` | 是 | 来自 §5，URL-encode |
| `page` | 是 | 1 基**内容起点** |
| `psize` | 是 | 本段页数；`0` = 只取目录（`contents` 为空），`1` = 目录 + 1 页，`10000` = 全书 |
| `w` / `h` | 是 | 虚拟阅读器宽高（px），决定服务端分页 |
| `fsize` | 是 | 虚拟字号，决定每页字数 |
| `ucatalog` | 是 | `true` 才返回目录 |
| `ctype` | 是 | 固定 `3` |

响应：

```json
{"result":1,"msg":{"pageAll":84,"contents":["<div class=\"text\">…"],"catalogs":[…]}}
```

| 字段 | 说明 |
|---|---|
| `pageAll` | 全书总页数（按 `w/h/fsize` 算出） |
| `contents[]` | 本段每页一个 HTML 字符串 |
| `catalogs[]` | 完整目录，**不受 `psize` 限制**（`psize=0` 也全量返回） |

`catalogs[]` 元素：

| 字段 | 说明 |
|---|---|
| `page` | **1 基页号**，直接对应 `contents[page-1]` |
| `contentIndex` | 章节内部索引，**不是页号**，不要拿来做跳页 |
| `title` | 章节名 |
| `href` / `id` | 原 EPUB 文件名与 ID |
| `pid` / `snum` | 层级与序号。`pid == 0` 即顶层，否则指向父项的 `id`/`href` |
| `children` | **子项数组，可以非空**（见下方「目录层级」），最多两层 |

### 目录层级

`catalogs[]` 是**树**：顶层项 + `children[]`，子项可以继续带 `children[]`。
深度上限**未验证**，不要把「两层」当契约——客户端按递归处理。

| 事实 | 读数 |
|---|---|
| 实测深度 | 14 个样本全部 ≤ 2 层（⚠ 小样本，不能推出上限） |
| 顶层 + 子项总量 | 期刊可达 87 + 302；图书可达 3 + 143 |
| 子项页码 | **两种形态都存在**，见下 |

子项页码有两种，**必须按数据判断，不能假设**：

- **子页码 == 父页**：子项只是同一页里的小标题，不是独立跳转目标
  - 期刊几乎全是这种（实测 58/58、52/52、53/53、302/302 全部相等）
  - 图书也有（实测 51/51、143/143、20/20 相等）
- **子页码 != 父页**：子项是真正可跳转的独立位置
  - 图书里出现过（实测 42/42、28/28 全部不等）

✅ 2026-10-30 实测（期刊 3 分类 × 2 本、图书 2 分类 × 4 本）。

**同一 EPUB 文件内的兄弟项会共用 `href` / `id`**：一个 xhtml 里可以有多个锚点，
实测某一章 15 个子项的 `href` / `id` **全都是 `txt007`**，只有 `contentIndex`（11…25）与
`snum` 不同。客户端若拿 `id` 当节点键（展开状态、当前项高亮、滚动定位），
15 个兄弟会撞成同一个键：展开一个等于全部展开、命中一个等于整排高亮。
**键里必须再带上 `contentIndex`，没有该字段时退回 `snum`。**（2026-10-31 实测）

⚠ **同一文件内锚点的 `page` 不可信**：实测某章父项 `page=58`，15 个子项里 14 个也标 `58`、
最后一个标 `59`；而按同样 `w/h/fsize` 取正文，第 58 页只有 51 个字（就是章标题），
全部正文都在第 59 页。也就是说「子页码 == 父页码」**并不必然**表示「就在父页」，
只表示服务端没给出更细的位置。客户端照原样显示与跳转即可，但不要据此推断内容分布，
更不要用这个相等关系去「纠正」跳转目标。（2026-10-31 实测）

**跳转规则**：子项的 `page` 是它自己的页号；若与父页相同，跳到父页即可。

⚠ **`page` 越界不报错**：`page > pageAll` 时返回 `result:1` + `contents:[]`
（2026-10-30 实测：84 页的书，`page=85` 与 `page=999` 都是空数组，没有 `errorMsg`）。
分段起点算错或历史进度超出新 `pageAll` 时会**静默拿到空内容**，客户端必须自己把 `page`
夹到 `[1, pageAll]`，并校验 `contents.length > 0` 再渲染。

## 7. 分类 ID

服务端**只认 ID，不返回分类名**。下表是青简工程约定的标签与顺序；换 App 可以自己起名，
但 ID 是服务端事实。

**图书**（`books.jspx?cataid=`）：

| ID | 标签 | 本馆条数 | 备注 |
|---|---|---|---|
| 123 | 精品推荐 | 0 | **已无数据**，返回 `result:0` |
| 124 | 诗歌散文 | 466 | 青简首页用它做「新书」 |
| 125 | 小说传记 | 843 | |
| 126 | 科学技术 | 228 | |
| 127 | 国学经典 | 183 | |
| 128 | 历史文化 | 546 | |
| 129 | 社会科学 | 128 | |
| 130 | 心理成长 | 187 | |
| 131 | 艺术审美 | 149 | |
| 132 | 哲学宗教 | 149 | |
| 140 | 教育研究 | 772 | |
| 141 | 家长尊享 | 395 | |

**期刊**（`magazines.jspx?cataid=`）：

| ID | 标签 | 本馆条数 |
|---|---|---|
| 6 | 精品推荐 | 54 |
| 3 | 时政军事 | 49 |
| 4 | 文学艺术 | 44 |
| 5 | 时尚生活 | 29 |
| 8 | 财经管理 | 54 |
| 9 | 文化综合 | 185 |
| 10 | 其它 | 80 |

- ID 集合 ✅ 2026-10-27 普查；条数 ✅ 2026-10-30 复测（`gedeid=84751638`）
- 条数是**分类内条数之和**：图书 4046（跨分类有重复，去重后约 4000），期刊 495
- 标签映射来自青简工程代码，属客户端约定，**服务端不提供名称**；换 App 可自定义
- ⚠ 馆藏与分类随馆变化：换 `gedeid` 后必须重新普查一遍，不要把这里的数量当常量

## 8. 图片与静态资源域名

| 用途 | 域名 | 出现在 |
|---|---|---|
| 图书封面 | `unicover.duxiu.com` | `list[].cover` / `bcover` |
| 图书备用封面 | `resource.superlib.com` | `list[].ftpcover` / `ftpbcover` |
| 期刊封面 | `gdfile.superlib.com` | `list[].coverPath` / `itemList[].coverPath` |
| 正文内嵌图片 | `gdepub.sslibrary.com` | `contents[]` 的 HTML 内，**绝对 URL** |
| 期次二维码 | `qcode.16q.cn` | `itemList[].codeImg` |

✅ 2026-10-30 复测：正文图片为绝对 URL，无需拼 base。

## 9. 未验证项

| 项 | 状态 | 怎么验 |
|---|---|---|
| 是否限流 / 单 IP 配额 | ❓ | 连续发 200 个列表请求，看是否出现 429 或 `result:0` 突增 |
| `ctype` 其它取值 | ❓ | 固定同一本书，扫 `ctype=1..5`，比对 `contents` 差异 |
| `fsize` 的语义单位（px / 字号档） | ⚠ | 同一 `w/h` 下扫 `fsize=12..30`，记录 `pageAll` 变化曲线 |
| 换馆后分类 ID 是否一致 | ⚠ | 换一个 `gedeid`，重跑 §7 的 11 + 7 个分类 |
| 浏览器端直连 | ⚠ | 已知无 CORS 头；换馆/CDN 后需重测，默认按「不可直连」设计 |
