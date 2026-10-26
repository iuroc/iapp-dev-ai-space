"""把已经下载到本地的 HTML 转成纯文本并取片段（离线，不联网）。

用法：
  python -I fetch_text.py page.html                      # 全文
  python -I fetch_text.py page.html --find "Safer dynamic code loading" --chars 2000
  python -I fetch_text.py page.html --out page.txt

为什么单独做这一步：
  国内网络下 WebFetch 抓不了 Google 系域名，只能 curl 落盘；
  落盘后统一用本地脚本解析，结论可回溯，也不受网络波动影响。
"""
import argparse
import html
import re


def to_text(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        s = f.read()
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(p|div|li|tr|h[1-6])>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--find", default=None, help="从第一次出现的位置开始截取")
    ap.add_argument("--chars", type=int, default=3000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t = to_text(args.html)
    if args.find:
        i = t.find(args.find)
        if i < 0:
            raise SystemExit("not found: " + args.find)
        t = t[i:i + args.chars]
    elif args.chars and not args.out:
        t = t[:args.chars]

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(t)
        print("text ->", args.out, len(t), "chars")
    else:
        print(t)


if __name__ == "__main__":
    main()
