#!/usr/bin/env python3
"""分享前自检：skill 包内不得出现作者机器/工作区专属路径。

允许常见默认路径（`C:\\Program Files`、`C:\\LDPlayer\\LDPlayer9`、`/sdcard`、
`/data/media/0` 等）；只拦截作者机器的绝对路径和工作区目录。

检查对象：SKILL.md、references/**/*.md、scripts/**/*.py、scripts/README.md。
发现命中时打印 file:line，并以非零码退出。

用法：
  python scripts/check_portable.py
"""
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF = os.path.abspath(__file__)

# 允许的通用说法：本机端口 = 运行 adb 的那台电脑，不是作者机器。
FORBIDDEN = [
    (re.compile(r"docs[/\\]"), "外部 docs 路径"),
    (re.compile(r"cases[/\\]"), "已删除的 cases 路径"),
    (re.compile(r"CLAUDE\.md"), "工作区专属 CLAUDE.md"),
    (re.compile(r"android-sync"), "作者工作区的目录名"),
    (re.compile(r"\.claude/(?:skills|agents|hooks)"), "工作区专属的 skill / agent 引用"),
    (re.compile(r"本机(?!端口)"), "作者机器视角的“本机”"),
    (re.compile(r"本工作区"), "工作区视角"),
    (re.compile(r"[Ee]:[\\/]+Program Files[\\/]+(?:leidian|build-tools_r35|openjdk-25|platform-tools|python3)"), "作者机器的绝对路径"),
    (re.compile(r"[Ee]:[\\/]+workspaces"), "作者工作区路径"),
]

# 包名：只允许「读者查得到」的 —— 宿主包、系统/公开库、以及公认的示例占位。
# 判据是「拿到这个包名，读者能不能自己去搜到它」：
#   com.iapp.app / com.android.* / com.google.android.* / com.sun.*   公开可查
#   com.example.*                                                     RFC 2606 保留的示例域，公认占位
# 作者自己的工程包名、一次性探针的包名、私有库包名，读者查不到，一律算违规。
ALLOW_PKG = (
    "com.iapp.app",        # iApp 宿主（公开产品）
    "com.android.",        # 系统 framework
    "com.google.android.", # androidx / material（公开库）
    "com.example.",        # 示例占位（RFC 2606）
    "com.sun.",            # JDK 公开 API
    "com.xuexiang.",       # XUI：GitHub 公开开源库，读者能查能装
)
PKG_RE = re.compile(r"\bcom\.[a-z0-9_]+(?:\.[a-z0-9_]+)+")

# 文档里引用的随包文件必须真的存在。
REF_RE = re.compile(r"(?:references|scripts)/[A-Za-z0-9_.\-/]+\.(?:md|py)")

SKIP_DIRS = {".git", "__pycache__"}


def iter_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith((".md", ".py")):
                continue
            path = os.path.join(dirpath, name)
            if os.path.abspath(path) == SELF:
                continue
            yield path


def main() -> int:
    hits = []
    for path in iter_files():
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        with open(path, encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, 1):
                for pattern, label in FORBIDDEN:
                    if pattern.search(line):
                        hits.append((rel, lineno, label, line.strip()))
                for m in REF_RE.finditer(line):
                    target = m.group(0)
                    if not os.path.exists(os.path.join(ROOT, target)):
                        hits.append((rel, lineno, "引用了不存在的随包文件", target))
                for m in PKG_RE.finditer(line):
                    pkg = m.group(0)
                    # 白名单里带尾点表示前缀匹配；不带尾点的（com.iapp.app）允许本身命中
                    ok = any(pkg.startswith(a) or pkg == a.rstrip(".") for a in ALLOW_PKG)
                    if not ok:
                        hits.append((rel, lineno, "具体工程包名（读者没有这个工程）", pkg))

    if not hits:
        print("portable check: OK")
        return 0

    print("portable check: %d issue(s)" % len(hits))
    for rel, lineno, label, detail in hits:
        print("%s:%d: %s -> %s" % (rel, lineno, label, detail))
    return 1


if __name__ == "__main__":
    sys.exit(main())
