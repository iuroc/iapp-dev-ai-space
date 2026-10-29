# 随包脚本

| 脚本 | 用途 |
|---|---|
| `review_docs.py` | 三层文档架构体检（只读）：死链、索引漏登记、级别标注、skill 本机事实、参数与文档一致性、数值分组 |
| `review_config.json` | 体检配置：排除项、白名单、索引映射、数值键表、已知分口径指标（`known_split`）、已判定非冲突指标（`known_nonconflict`） |

## 用法

```bash
# 人读摘要
python .claude/skills/docs-architecture/scripts/review_docs.py

# 机器可读（含 git 基线，便于跨轮 diff）
python .claude/skills/docs-architecture/scripts/review_docs.py --json

# 只跑某几项（可用组名 LINK / INDEX / SKILL / LEVEL / DUP / NUM / ARG）
python .claude/skills/docs-architecture/scripts/review_docs.py --check LEVEL,ARG

# 按更严的阈值退出（默认 blocker）
python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on major
```

## 参数

| 参数 | 说明 |
|---|---|
| `--root` | 仓库根；默认按脚本位置推断（`scripts/` 上三级） |
| `--config` | 配置文件，默认 `review_config.json` |
| `--json` | 输出 JSON（schema 固定，含 `rev` / `summary` / `findings`） |
| `--fail-on` | `blocker`（默认）/ `major` / `none` |
| `--check` | 只跑指定检查项，逗号分隔 |
| `--no-portable` | 跳过 `check_portable.py` |
| `--max-per-check` | 每项最多报告 N 条，0 为不限 |

## 说明

- 纯标准库、**只读**：不写文件、不改配置。
- 便携性检查**调用** `iapp-development/scripts/check_portable.py`，不复制它的规则；
  它不存在时自动跳过。
- 历史归档（`docs/evidence.md`、`docs/superpowers/plans/`、`docs/superpowers/specs/`）里的问题自动降一级，
  避免每次都被旧引用淹没。
- `NUM-01` 只报告「同一指标出现多个值」，**不判定谁对谁错**，需人工确认口径。
  人工判定确属非冲突（不同时间快照）后，把指标键写进 `known_nonconflict`，该组降为提示。
