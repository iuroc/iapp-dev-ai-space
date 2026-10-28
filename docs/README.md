# docs 索引

本机事实与证据。通用 iApp 知识在 `.claude/skills/iapp-development/`，本机规则在根目录 `CLAUDE.md`，
文档规范与体检在 `.claude/skills/docs-architecture/`。

| 文件/目录 | 内容 |
|---|---|
| `environments/` | 环境档案：雷电 14（主）/ 雷电 9（按需）/ 应用宝电脑版（无 adb）；含能力矩阵与选档判据 |
| `runtime-env.md` | 当前机器快照：在连设备、安装与端口、iApp 版本、工程根、工具路径 |
| `scripts/detect_env.py` | 只读环境探测（宿主 / 模拟器 / adb / 共享目录 / 可选 FTP）。参数：`--json` 机器可读、`--ftp HOST:PORT` 探宿主到设备 FTP 的可达性、`--mirror-root PATH` 指定共享目录、`--adb PATH` 指定 adb；退出码 0 有可用通道 / 1 无可用通道 / 2 参数错误 / 3 内部异常 |
| `dev-env-setup.md` | 本机装机/连机/投递步骤与踩过的环境坑 |
| `ui-skills.md` | 两个 UI 辅助技能（`mobile-app-ui-design` / `material-3`）怎么配合 iApp：能用哪些、怎么映射、哪些实现不能照抄 |
| `evidence.md` | 每轮探针的日期、批次、原始读数（先写这里，再提炼进 SKILL） |
| `reference/` | 官方手册副本（iyu、ijava） |
| `artifacts/` | 从设备拉下的 APK 与 dex 分析产物 |
| `superpowers/plans/` | 实施计划（superpowers SDD 标准位置，`YYYY-MM-DD-<feature>.md`） |
| `superpowers/specs/` | 设计规格（`YYYY-MM-DD-<topic>-design.md`） |
| `scripts/` | 本机脚本目录，逐个说明见 `scripts/README.md`（含与 skill 同名副本的「同 / 异」标注） |
