#!/usr/bin/env python3
"""scrcpy 投屏薄包装：固定码率预设，按设备启动预览窗口。

为什么需要预设：scrcpy 默认 8 Mbps，对 1080p 以上的文字界面不够，表现为文字发糊、
浅色底色出现色带/断层。50 Mbps 是 VBR 上限，静态画面实际只用到不到 1 Mbps，
真正吃码率的是滚动和翻页瞬间，所以不会压垮 USB。

预设（依据见 SKILL debugging.md §投屏预览）：
  default  H.264 / 50 Mbps / 60 fps   日常调试与阅读类界面
  light    H.264 / 25 Mbps / 30 fps   USB 共享、多设备
  pixel    H.265 / 35 Mbps / 30 fps   看 UI 细节、截图前

用法：
  python tools/mirror.py --serial <serial>
  python tools/mirror.py --serial <serial> --preset light
  python tools/mirror.py --serial <serial> -- --print-fps   # 额外参数透传

查找顺序：--scrcpy → SCRCPY 环境变量 → PATH 里的 scrcpy → 常见安装位置。
这是本机薄包装，不含投屏实现；换机器时改候选路径或设 SCRCPY 即可。
"""
import argparse
import os
import subprocess
import sys

PRESETS = {
    "default": ["--video-bit-rate=50M"],
    "light": ["--video-bit-rate=25M", "--max-fps=30"],
    "pixel": ["--video-codec=h265", "--video-bit-rate=35M", "--max-fps=30"],
}

CANDIDATES = [
    r"E:\Dev Tools\scrcpy\scrcpy-win64-v5.0.1\scrcpy.exe",
    r"C:\scrcpy\scrcpy.exe",
]


def find_scrcpy(explicit):
    for cand in (explicit, os.environ.get("SCRCPY"), "scrcpy", *CANDIDATES):
        if not cand:
            continue
        try:
            p = subprocess.run([cand, "--version"], capture_output=True, text=True, timeout=10)
        except Exception:
            continue
        if p.returncode == 0:
            return cand
    return None


def main():
    ap = argparse.ArgumentParser(description="按预设启动 scrcpy 投屏")
    ap.add_argument("--serial", help="adb 序列号；只有一台设备时可省")
    ap.add_argument("--preset", default="default", choices=sorted(PRESETS),
                    help="码率预设：default / light / pixel")
    ap.add_argument("--scrcpy", help="scrcpy 可执行文件；默认按环境变量/PATH/常见位置查找")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令")
    ap.add_argument("extra", nargs=argparse.REMAINDER, help="透传给 scrcpy 的额外参数（放在 -- 之后）")
    args = ap.parse_args()

    exe = find_scrcpy(args.scrcpy)
    if not exe:
        print("找不到 scrcpy（--scrcpy / SCRCPY / PATH / 常见安装位置）")
        return 1

    cmd = [exe]
    if args.serial:
        cmd += ["-s", args.serial]
    cmd += PRESETS[args.preset]
    title = "scrcpy" + (" " + args.serial if args.serial else "") + " [" + args.preset + "]"
    cmd += ["--window-title", title]
    extra = list(args.extra)
    if extra and extra[0] == "--":
        extra = extra[1:]
    cmd += extra

    print("预设: " + args.preset + "  (" + " ".join(PRESETS[args.preset]) + ")")
    print("$ " + " ".join(cmd))
    if args.dry_run:
        return 0

    try:
        return subprocess.run(cmd).returncode
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
