#!/usr/bin/env python3
"""整目录覆盖推送 iApp 工程到设备（adb push 的薄包装）。

原则：**源在宿主，设备侧只是副本，每次整目录覆盖**。
不用增量同步：`--sync` 只按 size/mtime 决定传不传，从不删除远端文件，
本地删掉/改名的 `.mjava`、`.iyu` 会残留在设备上继续被加载，而这种残留
在「不读设备副本核对」的流程里发现不了。工程除 .git 外不到 100 KB，
全量重推是毫秒级，不值得为省这点时间引入这种不可见的状态。

默认先删远端 src/ res/ files/ 再全量推；sdk/ 不碰（iApp 自己生成的运行态）。
清理后会把本地这三个目录下的所有子目录在远端 `mkdir -p` 出来：`adb push` 在
`/sdcard/Android/data/<pkg>/` 下不会自建多级目录，嵌套资源（如 `res/web/index.html`）
会报 `remote secure_mkdirs failed`。
成功与否只认 adb 退出码；不读回设备侧内容、不做 md5/size 比对，
验收靠开发者实跑 + logcat + iApp 控制台日志。

用法：
  python tools/push.py <项目ID> [--serial S] [--no-clean] [--sync] [--dry-run] [--adb PATH] [--root DIR]

默认路径：
  源   project/<项目ID>
  目标 <iApp 工程根>/<项目ID>，默认 iApp 的应用私有外部目录（Android 11+ 的默认工程根）：
       /sdcard/Android/data/com.iapp.app/files/iApp/ProjectApp
  2026-10-30 起不再使用共享目录 /sdcard/Pictures/ProjectApp；若某台设备的 iApp
  把工程根设成了别处，用 --root 覆盖，不要改这里的默认值

推送范围：src/ res/ files/ + .project AndroidManifest.xml build.xml icon.png
跳过：.git/（越推越大）、bin/（产物）、sdk/（iApp 首次打开时生成）

--no-clean 保留远端旧文件（只在确定没有删除/改名时用）
--sync     走 adb push --sync 增量（快，但按上面的理由不建议）
"""
import argparse
import os
import subprocess
import sys

DIRS = ["src", "res", "files"]
DEFAULT_ROOT = "/sdcard/Android/data/com.iapp.app/files/iApp/ProjectApp"
FILES = [".project", "AndroidManifest.xml", "build.xml", "icon.png"]
DEFAULT_ADB = r"E:\Program Files\platform-tools\adb.exe"


def find_adb(explicit):
    for cand in (explicit, os.environ.get("ADB"), "adb", DEFAULT_ADB):
        if not cand:
            continue
        try:
            out = subprocess.run([cand, "version"], capture_output=True, text=True, timeout=20)
        except Exception:
            continue
        if out.returncode == 0:
            return cand
    return None


def run(cmd, dry, quiet=False):
    if dry:
        print("  $ " + " ".join(cmd))
        return 0
    p = subprocess.run(cmd, capture_output=True, text=True)
    if not quiet and p.stdout.strip():
        print("    " + p.stdout.strip().replace("\n", "\n    "))
    if p.returncode != 0 and p.stderr.strip():
        print("    ! " + p.stderr.strip().replace("\n", "\n    "))
    return p.returncode


def main():
    ap = argparse.ArgumentParser(description="整目录推送 iApp 工程（adb push --sync）")
    ap.add_argument("project", help="项目ID，即 ProjectApp 下的目录名")
    ap.add_argument("--serial", help="adb 序列号；只有一台设备时可省")
    ap.add_argument("--adb", help="adb 可执行文件；默认 PATH / ADB 环境变量 / 常见安装位置")
    ap.add_argument("--no-clean", action="store_true", help="保留远端旧文件（默认会先删 src/ res/ files/）")
    ap.add_argument("--sync", action="store_true", help="改用 adb push --sync 增量（不建议）")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="设备上的工程根目录；默认 iApp 的默认路径")
    args = ap.parse_args()

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(here, "project", args.project)
    if not os.path.isdir(src):
        print("源目录不存在: " + src)
        return 2
    dst = args.root.rstrip("/") + "/" + args.project

    adb = find_adb(args.adb)
    if not adb:
        print("找不到 adb（--adb / ADB 环境变量 / PATH / " + DEFAULT_ADB + "）")
        return 1
    base = [adb] + (["-s", args.serial] if args.serial else [])

    devs = subprocess.run(base + ["devices"], capture_output=True, text=True)
    lines = [l for l in devs.stdout.splitlines()[1:] if l.strip().endswith("device")]
    if not lines:
        print("没有已连接的设备，先起模拟器/连真机")
        return 1
    if not args.serial and len(lines) > 1:
        print("多台设备，请用 --serial 指定：" + ", ".join(l.split()[0] for l in lines))
        return 1
    print("源  : " + src)
    print("目标: " + dst + "  (" + (args.serial or lines[0].split()[0]) + ")")

    # 目标目录可能还不存在（首次推送 / 换了工程根）。必须先用 shell 建好：
    # 让 adb push 自己去建，在 /sdcard/Android/data/<pkg>/ 下会报
    # `remote secure_mkdirs failed: Operation not permitted` ✅ 2026-10-30
    mkdirs = "mkdir -p " + " ".join([dst] + [dst + "/" + d for d in DIRS])
    if run(base + ["shell", mkdirs], args.dry_run) != 0:
        print("创建目标目录失败: " + dst)
        return 3

    if not args.no_clean:
        # 删内容不删目录：设备上这几个目录会是 busy（iApp / FUSE 持有），
        # `rm -rf <dir>` 会以 Text file busy 失败，`rm -rf <dir>/*` 可以 ✅ 2026-10-30
        print("清远端 src/ res/ files/ 内容")
        for d in DIRS:
            p = dst + "/" + d
            if run(base + ["shell", "rm -rf " + p + "/* " + p + "/.[!.]*"], args.dry_run) != 0:
                print("清理失败: " + d)
                return 3

    # adb push 在应用私有外部目录下不会自建多级目录，先把本地子目录在远端建出来
    # （必须在清理之后，rm -rf res/* 会把上次建的子目录一起删掉）✅ 2026-10-31
    subdirs = []
    for d in DIRS:
        ld = os.path.join(src, d)
        if not os.path.isdir(ld):
            continue
        for root, dirs, _files in os.walk(ld):
            for name in dirs:
                rel = os.path.relpath(os.path.join(root, name), src).replace(os.sep, "/")
                subdirs.append(dst + "/" + rel)
    if subdirs and run(base + ["shell", "mkdir -p " + " ".join(subdirs)], args.dry_run) != 0:
        print("创建子目录失败")
        return 3

    flags = ["push", "--sync"] if args.sync else ["push"]
    ok = True
    for d in DIRS:
        ld = os.path.join(src, d)
        if not os.path.isdir(ld):
            continue
        print("推 " + d + "/")
        if run(base + flags + [ld + os.sep + ".", dst + "/" + d + "/"], args.dry_run) != 0:
            ok = False

    present = [f for f in FILES if os.path.isfile(os.path.join(src, f))]
    if present:
        print("推 " + " ".join(present))
        cmd = base + flags + [os.path.join(src, f) for f in present] + [dst + "/"]
        if run(cmd, args.dry_run) != 0:
            ok = False

    print("完成" if ok else "有失败项")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
