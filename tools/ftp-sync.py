#!/usr/bin/env python3
"""本机薄包装：给通用 FTP 同步脚本注入默认参数。

通用实现（真正干活的）在 `.claude/skills/iapp-development/scripts/ftp_sync.py`；
这里只做三件事：
1. 从 `tools/ftp-sync.local`（不入库）或环境变量读本机默认值；
2. 修掉 Git Bash/MSYS 把 `/ProjectApp/...` 改写成的 Windows 路径；
3. 转调通用脚本，命令行参数优先。

本机默认值（任选其一）：
    tools/ftp-sync.local           # 每行 key=value，也接受 JSON
    IAPP_FTP_HOST / IAPP_FTP_PORT / IAPP_FTP_REMOTE / IAPP_SYNC_ROOT

示例：
    python tools/ftp-sync.py --dry-run
    python tools/ftp-sync.py --pull
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TARGET = REPO / ".claude" / "skills" / "iapp-development" / "scripts" / "ftp_sync.py"
CONF_FILE = Path(__file__).resolve().with_name("ftp-sync.local")

ENV_KEYS = {
    "host": "IAPP_FTP_HOST",
    "port": "IAPP_FTP_PORT",
    "remote": "IAPP_FTP_REMOTE",
    "local-root": "IAPP_SYNC_ROOT",
}


def read_conf():
    if not CONF_FILE.is_file():
        return {}
    text = CONF_FILE.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            print(f"{CONF_FILE} 不是合法 JSON：{exc}", file=sys.stderr)
            return {}
    conf = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        conf[key.strip()] = value.strip()
    return conf


def fix_remote(value):
    """把 MSYS 改写过的 C:/.../Git/ProjectApp/... 还原成 /ProjectApp/..."""
    if not value or value.startswith("/"):
        return value
    normalized = value.replace("\\", "/")
    match = re.search(r"(/ProjectApp(?:/.*)?)$", normalized)
    if match:
        return match.group(1)
    if re.match(r"^[A-Za-z]:", normalized):
        print(
            "远端路径看起来被 Git Bash/MSYS 改写成了 Windows 路径："
            f"{value}\n请 export MSYS_NO_PATHCONV=1 后重试。",
            file=sys.stderr,
        )
    return value


def build_argv(user_argv):
    conf = read_conf()
    argv = list(user_argv)
    missing = []
    for key, env in ENV_KEYS.items():
        flag = f"--{key}"
        if any(a == flag or a.startswith(flag + "=") for a in argv):
            continue
        value = os.environ.get(env) or conf.get(key) or conf.get(key.replace("-", "_"))
        if value:
            argv.extend([flag, fix_remote(str(value)) if key == "remote" else str(value)])
        else:
            missing.append(f"{flag}（{env} 或 {CONF_FILE.name} 里的 {key}）")

    required_missing = [m for m in missing if m.startswith(("--host", "--remote"))]
    if required_missing:
        print("缺少必要参数：" + "；".join(required_missing), file=sys.stderr)
        print("任选其一补齐：", file=sys.stderr)
        print(f"  - 在 {CONF_FILE} 里写 host= / port= / remote= / local-root=", file=sys.stderr)
        print("  - 设置环境变量 IAPP_FTP_HOST / IAPP_FTP_PORT / IAPP_FTP_REMOTE / IAPP_SYNC_ROOT", file=sys.stderr)
        print("  - 直接在命令行给 --host 等参数", file=sys.stderr)
        return None
    return argv


def load_target():
    spec = importlib.util.spec_from_file_location("iapp_ftp_sync", TARGET)
    if spec is None or spec.loader is None:
        raise SystemExit(f"找不到通用脚本：{TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    argv = build_argv(sys.argv[1:])
    if argv is None:
        return 2
    module = load_target()
    return module.main(argv)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
