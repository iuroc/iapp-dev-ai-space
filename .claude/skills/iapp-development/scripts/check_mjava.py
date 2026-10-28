"""扫描 .mjava 里会让整个模块失效、或调用未定义模块方法的写法（投递前跑）。

用法：
  python check_mjava.py <工程 src 目录或 .mjava 文件...>

第一类（解析期致命，整个模块不加载）：
  final 修饰符 / lambda -> / 可变参数 ... / 大于 int 的十六进制字面量
  new bsh.* / 类型声明或 new 里用全限定类名 / 字符串里的非法转义

第二类（运行期 Command not found）：
  调用带 `<模块>_` 前缀、但工程里没有定义的方法

退出码 1 表示有命中。注释行会跳过；确定是误报时用 `# noqa` 标在该行。
"""
import os
import re
import sys

CHECKS = [
    ("final 修饰符", re.compile(r"\bfinal\b")),
    ("lambda ->", re.compile(r"->")),
    ("可变参数 ...", re.compile(r"\.\.\.\s*\)|\w+\s*\.\.\.")),
    ("大十六进制字面量", re.compile(r"0x[89A-Fa-f][0-9A-Fa-f]{3,}")),
    ("new bsh.*", re.compile(r"new\s+bsh\.")),
    ("类型声明里的全限定名", re.compile(r"^\s*(android|androidx|com|org|java|javax)\.[\w.]+\s+\w+\s*(=|;)")),
    ("new 里的全限定名", re.compile(r"=\s*new\s+(android|androidx|com|org)\.\w")),
    ("字符串非法转义（\\s/\\d/\\w 等要写成 \\\\s）", re.compile(r"(?<!\\)\\[sdwSDWbBAZ]")),
]

DEF_RE = re.compile(r"^\s*(?:public|private|protected)\s+[\w\[\]<>,\s]+?\s+(\w+)\s*\(", re.M)
CALL_RE = re.compile(r"\b([a-z][a-z0-9]*_[a-z0-9_]+)\s*\(")


def scan(path):
    hits = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for no, line in enumerate(f, 1):
            raw = line.rstrip("\n")
            s = raw.strip()
            if s.startswith("//") or s.startswith("*") or s.startswith("/*"):
                continue
            if "# noqa" in raw:
                continue
            for name, rx in CHECKS:
                if rx.search(raw):
                    hits.append((no, name, raw.strip()))
    return hits


def iter_files(args):
    for a in args:
        if os.path.isdir(a):
            for root, _dirs, files in os.walk(a):
                for fn in files:
                    if fn.endswith(".mjava"):
                        yield os.path.join(root, fn)
        elif a.endswith(".mjava"):
            yield a


def check_prefix_calls(files):
    """调用带前缀的方法，但整个工程从未定义过 -> 运行期 Command not found。"""
    defined = set()
    bodies = []
    for path in files:
        text = open(path, "r", encoding="utf-8", errors="replace").read()
        bodies.append((path, text))
        for m in DEF_RE.finditer(text):
            defined.add(m.group(1))
    problems = []
    for path, text in bodies:
        for no, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if s.startswith("//") or DEF_RE.match(line):
                continue
            for m in CALL_RE.finditer(line):
                name = m.group(1)
                if name not in defined:
                    problems.append((path, no, name, line.strip()))
    return problems


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    files = list(iter_files(args))
    total = 0
    for path in files:
        for no, name, text in scan(path):
            total += 1
            print("%s:%d  [%s]  %s" % (path, no, name, text))
    for path, no, name, text in check_prefix_calls(files):
        total += 1
        print("%s:%d  [调用未定义的模块方法 %s]  %s" % (path, no, name, text))
    if total:
        print("\n共 %d 处。前一类会让模块失效，后一类会在运行期 Command not found，投递前都要改。" % total)
        sys.exit(1)
    print("check_mjava: OK（未发现致命写法）")


if __name__ == "__main__":
    main()
