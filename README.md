# iApp 开发工作区

在 Windows 宿主上开发、调试、打包 iApp（Android 可视化 IDE，显示名「测兆编程」）工程的私有工作区：
源码是 `.iyu` 界面 + `.mjava` 模块，产物是可安装 APK，通过当前环境可用的通道投递到模拟器或真机。

**这里不写规则。** 环境协商、投递链路、设备选择、git 约定、开发取向全部在 [`CLAUDE.md`](CLAUDE.md)，
本文件只做入口索引。

## 从哪开始

| 你要做什么 | 先看 |
|---|---|
| 第一次进这个工作区 | [`CLAUDE.md`](CLAUDE.md) → 跑一次 `python docs/scripts/detect_env.py` |
| 换了一台机器 / 换了个模拟器 | `CLAUDE.md` §环境协商、§本机变量 |
| 写 `.iyu` / `.mjava`，查语法铁律与失败签名 | [`.claude/skills/iapp-development/`](.claude/skills/iapp-development/SKILL.md) |
| 改完代码不知道怎么送到设备 | `CLAUDE.md` §投递链路 |
| 需要某台设备的读数（屏幕、ABI、键位…） | [`docs/environments/`](docs/environments/README.md) |
| 想知道上次实测出了什么 | [`docs/evidence.md`](docs/evidence.md) |
| 要加结论、改文档、提交前体检 | [`.claude/skills/docs-architecture/`](.claude/skills/docs-architecture/SKILL.md) |
| 要设计新页面、定配色与组件规格 | [`docs/ui-skills.md`](docs/ui-skills.md) |

## 目录

| 路径 | 内容 |
|---|---|
| `CLAUDE.md` | 本机事实与工作规则（唯一的主文件） |
| `.claude/skills/iapp-development/` | iApp 通用知识：语法、控件、投递、打包、手表开发 |
| `.claude/skills/docs-architecture/` | 三层文档规范与只读体检脚本 |
| `.claude/skills/material-3/`、`mobile-app-ui-design/` | UI 辅助技能（外部引入，见 `skills-lock.json`） |
| `docs/` | 本机读数：环境档案、证据账本、脚本，索引见 [`docs/README.md`](docs/README.md) |
| `android-sync/` | iApp 工程在宿主的镜像（**不入库**，见下） |
| `tools/` | 本机薄包装，如 `ftp-sync.py`（实现仍在 SKILL 里） |
| `openspec/` | 规格驱动脚手架，目前是空骨架（`changes/` 与 `specs/`） |

## 三层知识怎么落

同一句话只写一处，其余只留指针：

```
换台机器仍成立  →  SKILL      .claude/skills/iapp-development/
只对本机成立    →  CLAUDE.md  根目录
读数与快照      →  docs/      environments/ + evidence.md
```

判据、级别（✅/⚠/❓）、去重与回填流程见 `docs-architecture` 技能；提交前跑
`review_docs.py --fail-on blocker` 与 `check_portable.py`。

## 这个仓库里没有什么

`.gitignore` 刻意排除了几类东西，克隆下来是**没有**的：

- **`android-sync/`** —— 设备工程的宿主镜像，按设备各自维护。
  需要时用 `docs/scripts/refresh-mirror.sh` 拉回，或走 `CLAUDE.md` 里的 FTP 通道。
  里面的每个正式工程自带独立 git 仓库，版本历史在工程自己的仓库里，不在这个仓库。
- **产物与样本** —— `*.apk`、`*.dex`、`*.jar`、`docs/artifacts/` 等，需要时重新打包或 pull。
- **`tools/ftp-sync.local`** —— 含设备 IP 与端口的本机配置。

所以「工作区仓库」只记录**规则、知识、读数**，不记录工程内容本身。

## 脚本

| 脚本 | 用途 |
|---|---|
| `docs/scripts/detect_env.py` | 只读环境探测，决定这轮走哪条通道 |
| `docs/scripts/refresh-mirror.sh` | 把设备上的工程快照拉回宿主镜像 |
| `tools/ftp-sync.py` | 注入本机默认参数后转调 SKILL 里的通用 `ftp_sync.py` |

逐个说明见 [`docs/scripts/README.md`](docs/scripts/README.md)。
