#!/usr/bin/env python3
"""三层文档架构体检（只读）。

检查 CLAUDE.md / docs/ / .claude/skills/ 之间的架构一致性：死链、索引漏登记、
级别标注、skill 里的本机事实、脚本参数与文档是否一致、同一指标的数值是否打架。

只读：不写任何文件、不改配置。默认输出人读摘要，--json 输出结构化结果。

用法：
    python .claude/skills/docs-architecture/scripts/review_docs.py
    python .claude/skills/docs-architecture/scripts/review_docs.py --json
    python .claude/skills/docs-architecture/scripts/review_docs.py --check LEVEL-04,ARG-02
    python .claude/skills/docs-architecture/scripts/review_docs.py --fail-on major
    python .claude/skills/docs-architecture/scripts/review_docs.py --root <repo> --no-portable

退出码：
    0 没有达到 --fail-on 阈值的问题（默认 blocker）
    1 有达到阈值的问题
    2 脚本自身错误（配置读不了、路径不对）
"""

from __future__ import annotations

import argparse
import ast
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).with_name("review_config.json")
RULES_VERSION = "2026-10-28"

SEVERITY_ORDER = {"blocker": 3, "major": 2, "minor": 1}


# ------------------------------------------------------------------ 基础

def load_config(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"读不了配置 {path}: {exc}")


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_excluded(path: Path, root: Path, excludes: list[str]) -> bool:
    parts = rel(path, root).split("/")
    for ex in excludes:
        ex_parts = ex.strip("/").split("/")
        if len(ex_parts) > 1:
            if parts[: len(ex_parts)] == ex_parts:
                return True
        elif ex_parts[0] in parts:  # 任意层级出现（如 __pycache__）
            return True
    return False


def collect_markdown(root: Path, cfg: dict) -> list[Path]:
    files = []
    for pattern in cfg.get("include", []):
        for path in root.glob(pattern):
            if path.is_file() and path.suffix == ".md":
                if not is_excluded(path, root, cfg.get("exclude_dirs", [])):
                    files.append(path)
    return sorted(set(files))


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def iter_lines(path: Path):
    """逐行产出 (行号, 原文, 是否在代码块内)。代码块里的路径多半是示例，不判死链。"""
    in_fence = False
    for idx, line in enumerate(read_lines(path), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            yield idx, line, True
            continue
        yield idx, line, in_fence


def joined_lines(path: Path):
    """把以反斜杠续行的命令拼成一行，返回 (起始行号, 拼接后的文本)。"""
    buf, start = "", 0
    for idx, line, _ in iter_lines(path):
        if not buf:
            start = idx
        if line.rstrip().endswith("\\"):
            buf += line.rstrip()[:-1] + " "
            continue
        buf += line
        yield start, buf
        buf = ""
    if buf:
        yield start, buf


def finding(check, severity, path, line, message, evidence="", hint="", confidence="high"):
    return {
        "id": check,
        "severity": severity,
        "file": path,
        "line": line,
        "message": message,
        "evidence": evidence,
        "hint": hint,
        "confidence": confidence,
    }


def in_history(path: str, cfg: dict) -> bool:
    return any(path == h or path.startswith(h.rstrip("/") + "/") for h in cfg.get("history_files", []))


def downgrade(severity: str, path: str, cfg: dict) -> str:
    """历史归档里的问题降一级：它们不该阻塞当前工作。"""
    if not in_history(path, cfg):
        return severity
    return {"blocker": "major", "major": "minor"}.get(severity, severity)


# ------------------------------------------------------------------ LINK

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PATH_TOKEN = re.compile(
    r"(?<![\w/.-])((?:\.claude/skills/[\w.-]+/)?(?:references|scripts|docs|tools)/"
    r"[A-Za-z0-9_./-]+\.(?:md|py|json|sh|ps1|txt))"
)
PLACEHOLDER = re.compile(r"[<>*?{}]")


def skill_root_of(path: Path) -> Path | None:
    for parent in path.parents:
        if (parent / "SKILL.md").is_file():
            return parent
    return None


def resolve_token(token: str, src: Path, root: Path) -> Path:
    if token.startswith((".claude/", "docs/", "tools/")):
        return root / token
    if token.startswith(("references/", "scripts/")):
        base = skill_root_of(src)
        if base:
            return base / token
        return src.parent / token
    return root / token


def check_links(files, root, cfg):
    out = []
    allowed_missing = set(cfg.get("allow_missing", []))
    for path in files:
        rp = rel(path, root)
        for idx, line, in_fence in iter_lines(path):
            if in_fence:
                continue
            for match in MD_LINK.finditer(line):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if PLACEHOLDER.search(target):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    out.append(finding("LINK-01", downgrade("blocker", rp, cfg), rp, idx,
                                       "markdown 链接目标不存在",
                                       evidence=target, hint="修正路径或删掉链接"))
            for match in PATH_TOKEN.finditer(line):
                token = match.group(1)
                if PLACEHOLDER.search(token) or token in allowed_missing:
                    continue
                if any(token.startswith(pfx) for pfx in cfg.get("allow_missing_prefix", [])):
                    continue
                if resolve_token(token, path, root).exists():
                    continue
                other = list((root / ".claude" / "skills").glob(f"*/{token}"))
                if token.startswith(("references/", "scripts/")) and other:
                    skill_name = other[0].parents[1].name
                    out.append(finding("LINK-03", downgrade("major", rp, cfg), rp, idx,
                                       "跨 skill 引用缺少 skill 路径前缀", evidence=token,
                                       hint=f"改为 .claude/skills/{skill_name}/{token}"))
                    continue
                out.append(finding("LINK-01", downgrade("blocker", rp, cfg), rp, idx,
                                   "引用的文件不存在", evidence=token,
                                   hint="修正路径；若为跨 skill 引用请带 skill 前缀"))

            for match in re.finditer(r"[A-Za-z0-9_./-]+\.md:\d+", line):
                out.append(finding("LINK-02", downgrade("major", rp, cfg), rp, idx,
                                   "使用了行号引用（行号会漂移）", evidence=match.group(0),
                                   hint="改为「文件 + §小节标题」"))

            for stone in cfg.get("tombstones", []):
                if re.search(stone, line):
                    out.append(finding("LINK-04", downgrade("blocker", rp, cfg), rp, idx,
                                       "引用了已删除或已废弃的路径", evidence=stone,
                                       hint="改为指向 evidence 的日期/批次，或删掉这句"))

    return out


# ------------------------------------------------------------------ INDEX

def section_range(path: Path, section: str | None):
    """返回某标题小节的 (起始行, 结束行)；没有 section 时覆盖全文。"""
    if not section:
        return 1, None
    lines = read_lines(path)
    start, level = 0, None
    for i, line in enumerate(lines, 1):
        match = re.match(r"^(#+)\s+(.*)", line)
        if match and section in match.group(2):
            start, level = i, len(match.group(1))
            continue
        if start and match and len(match.group(1)) <= level:
            return start, i - 1
    return (start, None) if start else (0, 0)


def index_tokens(path: Path, start: int = 1, end: int | None = None):
    """只认「表格首列恰好是一个反引号路径」或「列表项以反引号路径开头」的索引行。"""
    for idx, line in enumerate(read_lines(path), 1):
        if idx < start or (end is not None and idx > end):
            continue
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and re.fullmatch(r"`[^`]+`", cells[0]):
                yield idx, cells[0][1:-1]
            continue
        match = re.match(r"^[-*]\s+`([^`]+)`", s)
        if match:
            yield idx, match.group(1)


def check_index(root, cfg):
    out = []
    for entry in cfg.get("index_map", []):
        index_rel = entry["index"]
        index_path = root / index_rel
        if not index_path.is_file():
            out.append(finding("INDEX-00", "blocker", index_rel, 0,
                               "索引文件不存在", evidence=index_rel,
                               hint="新建该索引，或从 review_config.json 的 index_map 移除"))
            continue
        text = "\n".join(read_lines(index_path))

        for scope in entry.get("scope", []):
            for actual in sorted(root.glob(scope)):
                if actual.resolve() == index_path.resolve():
                    continue
                if is_excluded(actual, root, cfg.get("exclude_dirs", [])):
                    continue
                name = actual.name
                if actual.is_dir():
                    if name not in text:
                        out.append(finding("INDEX-01", "blocker", index_rel, 0,
                                           "目录未登记到索引", evidence=name,
                                           hint=f"在索引里加一行 {name}/"))
                else:
                    if name not in text:
                        out.append(finding("INDEX-01", "blocker", index_rel, 0,
                                           "文件未登记到索引", evidence=name,
                                           hint=f"在索引里加一行 {name}"))

        start, end = section_range(index_path, entry.get("section"))
        if end == 0:
            out.append(finding("INDEX-02", "blocker", index_rel, 0,
                               "索引小节不存在", evidence=entry.get("section", ""),
                               hint="检查 index_map 里的 section 名"))
            continue
        for idx, token in index_tokens(index_path, start, end):
            if PLACEHOLDER.search(token) or " " in token:
                continue
            if token.startswith(("--", "com.")) or not re.search(r"[/.]", token):
                continue
            target = (index_path.parent / token).resolve()
            target_rel = rel(target, root).rstrip("/") + "/"
            if any(target_rel.startswith(pfx) or token.startswith(pfx)
                   for pfx in cfg.get("allow_missing_prefix", [])):
                continue
            if not target.exists():
                out.append(finding("INDEX-02", "blocker", index_rel, idx,
                                   "索引条目指向不存在的文件", evidence=token,
                                   hint="修正条目或删掉该行"))
    return out


# ------------------------------------------------------------------ SKILL

def check_portable(root, cfg):
    portable_rel = cfg.get("portable_script")
    if not portable_rel:
        return []
    script = root / portable_rel
    if not script.is_file():
        return []
    proc = subprocess.run([sys.executable, str(script)], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    out = []
    for line in (proc.stdout or "").splitlines():
        match = re.match(r"(.+?):(\d+): (.+)", line.strip())
        if not match:
            continue
        file, lineno, detail = match.groups()
        out.append(finding("SKILL-01", "blocker", file, int(lineno),
                           "便携性检查未通过（check_portable.py）",
                           evidence=detail, hint="按 check_portable 的提示修正"))
    return out


IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SERIAL = re.compile(r"\bemulator-\d+\b")
DRIVE = re.compile(r"\b[A-Za-z]:[\\/][^`\n]*")
DEVICE_COUNT = re.compile(r"安卓\s*\d+[^。\n]*各一台|安卓\s*\d+\s*一台[^。\n]*安卓\s*\d+\s*一台")


def ip_allowed(ip: str, cfg: dict) -> bool:
    return any(ip.startswith(pfx) for pfx in cfg.get("allowed_ip_prefixes", []))


def path_allowed(p: str, cfg: dict) -> bool:
    return any(p.lower().startswith(a.lower()) for a in cfg.get("allowed_paths", []))


def check_skill_facts(root, cfg):
    out = []
    for skill_dir in cfg.get("skill_dirs", []):
        base = root / skill_dir
        if not base.is_dir():
            continue
        ignore_names = set(cfg.get("skill_fact_ignore_files", []))
        for path in sorted(list(base.rglob("*.md")) + list(base.rglob("*.py"))):
            if path.name in ignore_names:
                continue
            if is_excluded(path, root, cfg.get("exclude_dirs", [])):
                continue
            rp = rel(path, root)
            for idx, line in enumerate(read_lines(path), 1):
                if any(tag in line for tag in cfg.get("ip_context_allow", [])):
                    line_for_ip = ""
                else:
                    line_for_ip = line
                for ip in IPV4.findall(line_for_ip):
                    if not ip_allowed(ip, cfg):
                        out.append(finding("SKILL-02", "blocker", rp, idx,
                                           "skill 里出现真实 IP", evidence=ip,
                                           hint="换成<设备IP>或文档保留网段 192.0.2.x"))
                for drive in DRIVE.findall(line):
                    if not path_allowed(drive, cfg):
                        out.append(finding("SKILL-02", "blocker", rp, idx,
                                           "skill 里出现作者机器盘符路径", evidence=drive,
                                           hint="换成 <宿主目录> 之类的占位"))
                if DEVICE_COUNT.search(line):
                    out.append(finding("SKILL-03", "major", rp, idx,
                                       "skill 里混入单机设备数量描述", evidence=line.strip()[:60],
                                       hint="改为「两台不同 API 级别的实例」，读数与日期放 docs"))
    return out


# ------------------------------------------------------------------ LEVEL

DATE = re.compile(r"20\d\d-\d\d-\d\d")


def table_cells(line: str) -> list[str]:
    """表格行按单元格拆开；非表格行整体当一个格。级别判断按格，不按行。"""
    s = line.strip()
    if s.startswith("|"):
        return [c.strip() for c in s.strip("|").split("|")]
    return [s]
OTHER_MACHINE = ("他机", "M2", "未复验", "口述", "另一台", "交接文档")
VERIFY_HINT = ("怎么验", "验证", "探针", "命令", "观察", "跑一次", "执行")


def check_levels(files, root, cfg):
    out = []
    level_dirs = tuple(cfg.get("level_dirs", []))
    for path in files:
        rp = rel(path, root)
        if not rp.startswith(level_dirs):
            continue
        lines = read_lines(path)
        for idx, line in enumerate(lines, 1):
            if "只升不降" in line or "→" in line:
                continue  # 规则条文本身会同时出现所有记号
            for cell in table_cells(line):
                if "✅" in cell and "⚠" in cell:
                    out.append(finding("LEVEL-02", "blocker", rp, idx,
                                       "同一格同时出现 ✅ 与 ⚠", evidence=cell[:60],
                                       hint="拆成两条，或按证据只留一个级别"))
                if "✅" in cell and any(tag in cell for tag in OTHER_MACHINE):
                    out.append(finding("LEVEL-04", "blocker", rp, idx,
                                       "他机/未复验读数被标成 ✅", evidence=cell[:60],
                                       hint="降为 ⚠ 并注明来源"))
            has_ok = "✅" in line
            if has_ok and not DATE.search(line):
                out.append(finding("LEVEL-03", "major", rp, idx,
                                   "✅ 缺少日期", evidence=line.strip()[:60],
                                   hint="补日期，或指向 evidence 批次", confidence="medium"))
            if "❓" in line:
                window = "\n".join(lines[max(0, idx - 1): idx + 2])
                if not any(hint in window for hint in VERIFY_HINT):
                    out.append(finding("LEVEL-05", "major", rp, idx,
                                       "❓ 没有写「怎么验」", evidence=line.strip()[:60],
                                       hint="补一条命令 / 探针路径 / 观察判据", confidence="medium"))
    return out


# ------------------------------------------------------------------ DUP / NUM

def check_rule_dups(files, root, cfg):
    hits = {}
    for path in files:
        rp = rel(path, root)
        for idx, line in enumerate(read_lines(path), 1):
            for phrase in cfg.get("rule_phrases", []):
                if phrase in line:
                    hits.setdefault(phrase, []).append((rp, idx))
    out = []
    for phrase, locs in hits.items():
        fileset = {f for f, _ in locs}
        if len(fileset) > 1:
            out.append(finding("DUP-02", "major", locs[0][0], locs[0][1],
                               "元规则条文出现在多个文件", evidence=f"{phrase} -> {sorted(fileset)}",
                               hint="保留主文件（本 skill），其余改为一行指针"))
    return out


def check_numeric(files, root, cfg):
    groups = {}
    for path in files:
        rp = rel(path, root)
        for idx, line in enumerate(read_lines(path), 1):
            for key, pattern in cfg.get("numeric_patterns", {}).items():
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    value = match.group(1)
                    groups.setdefault(key, set()).add(value)
    out = []
    for key, values in groups.items():
        if len(values) <= 1:
            continue
        if key in cfg.get("known_nonconflict", []):
            sev, note = "minor", "已人工判定为非冲突（不同时间快照），无需再查"
        elif key in cfg.get("known_split", []):
            sev, note = "minor", "已知分口径指标，只提示；确认是否同一对象/同一时间"
        else:
            sev, note = "major", "可能冲突，需人工确认；确认是否同一对象/同一时间"
        out.append(finding("NUM-01", sev, "（多处）", 0,
                           f"同一指标出现多个取值：{key}", evidence=", ".join(sorted(values)),
                           hint=note, confidence="needs_human"))
    return out


# ------------------------------------------------------------------ ARG

def script_options(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return {}, []
    opts, required = set(), set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument"):
            continue
        names = [a.value for a in node.args
                 if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("--")]
        is_required = any(k.arg == "required" and isinstance(k.value, ast.Constant)
                          and k.value.value is True for k in node.keywords)
        for name in names:
            opts.add(name)
            if is_required:
                required.add(name)
    return opts, sorted(required)


ARG_TOKEN = re.compile(r"(?<![\w-])(--[A-Za-z][\w-]*)")


def check_args(files, root, cfg):
    out = []
    all_known = set()
    scripts = []
    for script_rel in cfg.get("arg_scripts", []):
        script = root / script_rel
        if not script.is_file():
            continue
        opts, required = script_options(script)
        if not opts:
            continue
        all_known |= opts
        scripts.append((script_rel, script, opts, required))

    for script_rel, script, opts, required in scripts:
        name = script.name
        rules = cfg.get("arg_rules", {}).get(name, {})
        required = sorted(set(required) | set(rules.get("required", [])))
        required_unless = rules.get("required_unless", {})
        documented = set()

        # 一个文档只要提到过这个脚本，它里面出现的参数就算「已记录」
        related = [p for p in files if name in "\n".join(read_lines(p))]
        for path in related:
            for line in read_lines(path):
                documented |= set(ARG_TOKEN.findall(line))

        for path in related:
            rp = rel(path, root)
            for idx, line in joined_lines(path):
                if name not in line:
                    continue
                used = set(ARG_TOKEN.findall(line))
                if not used:
                    continue
                is_command = "python" in line or line.strip().startswith(name)
                for opt in used:
                    if opt in opts or opt in cfg.get("ignore_options", []):
                        continue
                    if not is_command and opt in all_known:
                        continue  # 同一句话提到多个脚本时，别把别人的参数算到它头上
                    out.append(finding("ARG-03", "blocker", rp, idx,
                                       "文档里出现了脚本不支持的参数", evidence=opt,
                                       hint=f"{name} 没有该参数"))
                if is_command:
                    for opt in required:
                        if opt not in used:
                            out.append(finding("ARG-02", "blocker", rp, idx,
                                               "示例命令缺少必填参数", evidence=f"{name} 缺 {opt}",
                                               hint=f"补上 {opt}，或改写成「见 xxx」避免第二份命令副本"))
                    for opt, escape in required_unless.items():
                        if opt not in used and not (set(escape) & used):
                            out.append(finding("ARG-02", "blocker", rp, idx,
                                               "示例命令缺少条件必填参数",
                                               evidence=f"{name} 缺 {opt}（或 {escape}）",
                                               hint=f"补上 {opt} 或 {'/'.join(escape)}"))

        missing = sorted(opts - documented - set(cfg.get("ignore_options", [])))
        if missing:
            out.append(finding("ARG-01", "major", script_rel, 0,
                               "脚本参数从未出现在文档里", evidence=", ".join(missing),
                               hint="在对应的 scripts/README.md 与用法示例里补上",
                               confidence="medium"))
    return out


# ------------------------------------------------------------------ 主流程

CHECKS = {
    "LINK": ("LINK-01", "LINK-02", "LINK-03", "LINK-04"),
    "INDEX": ("INDEX-00", "INDEX-01", "INDEX-02"),
    "SKILL": ("SKILL-01", "SKILL-02", "SKILL-03"),
    "LEVEL": ("LEVEL-02", "LEVEL-03", "LEVEL-04", "LEVEL-05"),
    "DUP": ("DUP-02",),
    "NUM": ("NUM-01",),
    "ARG": ("ARG-01", "ARG-02", "ARG-03"),
}


def run(root: Path, cfg: dict, checks: set[str] | None, no_portable: bool):
    files = collect_markdown(root, cfg)
    findings = []
    findings += check_links(files, root, cfg)
    findings += check_index(root, cfg)
    if not no_portable:
        findings += check_portable(root, cfg)
    findings += check_skill_facts(root, cfg)
    findings += check_levels(files, root, cfg)
    findings += check_rule_dups(files, root, cfg)
    findings += check_numeric(files, root, cfg)
    findings += check_args(files, root, cfg)
    if checks:
        findings = [f for f in findings if f["id"] in checks]
    return files, findings


def git_rev(root: Path) -> str | None:
    try:
        proc = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(root),
                              capture_output=True, text=True, timeout=10)
        return proc.stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


def summarize(findings):
    summary = {"blocker": 0, "major": 0, "minor": 0}
    by_check = {}
    for item in findings:
        summary[item["severity"]] += 1
        by_check[item["id"]] = by_check.get(item["id"], 0) + 1
    return summary, dict(sorted(by_check.items()))


def human_report(findings, summary, by_check, files, rev):
    today = datetime.date.today().isoformat()
    lines = [f"== 文档架构体检 {today}（规则 v{RULES_VERSION}） / 基线 {rev or 'n/a'} ==",
             f"扫描 {len(files)} 个 Markdown 文件；阻断 {summary['blocker']} / "
             f"应修 {summary['major']} / 建议 {summary['minor']}"]
    if by_check:
        lines.append("按检查项：" + "，".join(f"{k}×{v}" for k, v in by_check.items()))
    for level, title in (("blocker", "阻断"), ("major", "应修"), ("minor", "建议")):
        items = [f for f in findings if f["severity"] == level]
        if not items:
            continue
        lines.append("")
        lines.append(f"## {title}（{len(items)}）")
        for item in items:
            where = item["file"] + (f":{item['line']}" if item["line"] else "")
            lines.append(f"- [{item['id']}] {where} — {item['message']}")
            if item["evidence"]:
                lines.append(f"    证据：{item['evidence']}")
            if item["hint"]:
                lines.append(f"    建议：{item['hint']}")
    if not findings:
        lines.append("")
        lines.append("没有发现问题。")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="三层文档架构体检（只读）")
    parser.add_argument("--root", default=None, help="仓库根，默认按脚本位置推断")
    parser.add_argument("--config", default=None, help="配置文件，默认 scripts/review_config.json")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--fail-on", choices=["blocker", "major", "none"], default="blocker",
                        help="达到该级别即返回非零（默认 blocker）")
    parser.add_argument("--check", default=None, help="只跑指定检查项，逗号分隔，可用组名 LINK/INDEX/...")
    parser.add_argument("--no-portable", action="store_true", help="跳过 check_portable.py")
    parser.add_argument("--max-per-check", type=int, default=0, help="每项最多报告 N 条（0 不限）")
    args = parser.parse_args(argv)

    script = Path(__file__).resolve()
    root = Path(args.root).resolve() if args.root else script.parents[4]
    cfg_path = Path(args.config) if args.config else DEFAULT_CONFIG
    if not cfg_path.is_file():
        print(f"配置文件不存在：{cfg_path}", file=sys.stderr)
        return 2
    cfg = load_config(cfg_path)

    checks = None
    if args.check:
        checks = set()
        for token in args.check.split(","):
            token = token.strip().upper()
            checks.update(CHECKS.get(token, (token,)))

    try:
        files, findings = run(root, cfg, checks, args.no_portable)
    except Exception as exc:  # noqa: BLE001
        print(f"体检内部错误：{exc}", file=sys.stderr)
        return 2

    if args.max_per_check > 0:
        kept, counts = [], {}
        for item in findings:
            n = counts.get(item["id"], 0)
            if n < args.max_per_check:
                kept.append(item)
                counts[item["id"]] = n + 1
        findings = kept

    summary, by_check = summarize(findings)
    rev = git_rev(root)

    if args.json:
        json.dump({
            "schema": 1,
            "tool": "review_docs",
            "rules": RULES_VERSION,
            "root": str(root),
            "rev": rev,
            "scan": {"files": len(files), "portable": not args.no_portable},
            "summary": summary,
            "by_check": by_check,
            "findings": findings,
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(human_report(findings, summary, by_check, files, rev))

    if args.fail_on == "none":
        return 0
    threshold = SEVERITY_ORDER[args.fail_on]
    worst = max((SEVERITY_ORDER[f["severity"]] for f in findings), default=0)
    return 1 if worst >= threshold else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
