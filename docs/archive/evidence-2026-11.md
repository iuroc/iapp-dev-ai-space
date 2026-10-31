# 探针证据账本（2026-11）

> 本文件是 2026-11 当月原始读数的续写区，跨月冻结；提炼后的现行结论在
> `.claude/skills/iapp-development/` 与 `docs/environments/`，批次去向见 `docs/evidence.md`。
>
> - **批次 ID 是引用键**（`IYUFMT-1` …），不要改名、不要合并。
> - 本文件只放原始读数与当次判定，结论稳定后回填 SKILL 并把索引行改为 `已提炼`。

---

## 2026-11-01 IYUFMT-1 iyu 格式化容忍度

**环境**：iApp V3.0 2018 版数据调试工具；设备经 FTP `172.22.35.129:9527`
（adb 不可用，只有上屏与 Toast，无 logcat）。

**探针**：临时工程 `com.probe.iyufmt`，7 页 `P0`–`P6`。每页结构相同：
`View id=1 FrameLayout` + `id=2/id=3` 两个 TextView（ppt `text=INDENT_PPT` / `text=FLAT_PPT`），
`loading` 事件 `call(null,"mjava","probe.check","Pn")`；mjava 读取 id 2/3 文本并 Toast + 页底白条。

**各页差异**

| 页 | 差异 |
|---|---|
| P0 | 原始写法（对照）：所有行从列 0 开始 |
| P1 | 标签行缩进 2/4 空格 + 标签之间空行；ppt 与事件体保持列 0 |
| P2 | 在 P1 基础上，ppt 每行与 `call(...)` 行缩进 4/6 空格 |
| P3 | 在 P2 基础上，空 `<event></event>` 改为 `<event/>` |
| P4 | 在 P2 基础上，`<View>` 的属性拆成多行（`id/did/type` 各占一行） |
| P5 | 在 P2 基础上，加 `<?xml version="1.0"?>` 并用 `<root>` 包住全部内容 |
| P6 | 在 P2 基础上，`</ppt>` 与 `</eventItme>` 另起一行 |

**原始读数**（用户于设备上逐页点击回报）

```
[03:03:17:491]  P0 | root=Y | id2=Y text2=INDENT_PPT | id3=Y text3=FLAT_PPT
[03:03:40:989]  P1 | root=Y | id2=Y text2=INDENT_PPT | id3=Y text3=FLAT_PPT
[03:03:47:554]  P2 | root=Y | id2=Y text2=INDENT_PPT | id3=Y text3=FLAT_PPT
[03:03:50:658]  P3 | root=Y | id2=Y text2=INDENT_PPT | id3=Y text3=FLAT_PPT
[03:03:53:070]  P4 | root=N | id2=N text2=MISSING | id3=N text3=MISSING
[03:04:00:738]  P5 | root=Y | id2=Y text2=INDENT_PPT | id3=Y text3=FLAT_PPT
[03:04:03:554]  P6 | root=Y | id2=Y text2=INDENT_PPT | id3=Y text3=FLAT_PPT
```

用户补充：P4 页面为空、组件属性没有读出；并提醒 **ppt 不能有任何前置空格**。

**当次判定**

| # | 读数 | 结论 | 级别 |
|---|---|---|---|
| 1 | P1 全 Y | 标签行缩进、标签间空行可接受 | ✅ 用户实测 |
| 2 | P2 全 Y | ppt 行与事件体 `call` 行缩进在该版本可接受；但与「ppt 不能有前置空格」的提醒冲突，格式化器不依赖该行为 | ⚠ 单次实测 |
| 3 | P3 全 Y | 空 `<event/>` 自闭合可载入 | ✅ 用户实测 |
| 4 | P4 全 N | **`<View>` 属性换行会让整页控件全部丢失** | ✅ 用户实测 |
| 5 | P5 全 Y | `<?xml?>` + `<root>` 包裹可载入；格式化器仍不采用 | ⚠ 单次实测 |
| 6 | P6 全 Y | `</ppt>`、`</eventItme>` 另起一行可接受 | ✅ 用户实测 |

**本地对照**（扩展解析器，同页 7 种变体）：views/events/properties/calls 模型完全一致；
即本地解析容忍度高于 iApp 运行时，不能拿解析结果代替实机验证。

**回填**

- `.claude/skills/iapp-development/references/iyu-guide.md` §格式化容忍度
