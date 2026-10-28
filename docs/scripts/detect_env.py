#!/usr/bin/env python3
"""只读环境探测：宿主 / 模拟器 / adb 设备 / 共享目录 / 可选 FTP。

给「换了一台机器」时用：先看这台机器具备什么能力，再决定走哪条投递通道、
读 docs/environments/ 下哪份档案。只读，不改系统、不 root、不装应用。

用法:
    python docs/scripts/detect_env.py
    python docs/scripts/detect_env.py --json
    python docs/scripts/detect_env.py --ftp 172.22.39.216:9527
    python docs/scripts/detect_env.py --mirror-root D:/iAppWorkspace/sync

退出码:
    0 探测完成，至少一条投递通道可用
    1 探测完成，但没找到可用通道（设备没开 / 没配 FTP 都算）
    2 参数错误
    3 内部异常（已尽量输出已完成的部分）
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

TIMEOUT = 8
IS_WIN = platform.system() == "Windows"

# 产品候选：目录、进程、注册表名。装没装 = 任一命中。
PRODUCTS = [
    {
        "id": "ldplayer9",
        "name": "雷电模拟器 9",
        "dirs": [
            r"C:\LDPlayer\LDPlayer9",
            r"C:\Program Files\leidian\LDPlayer9",
            r"C:\Program Files (x86)\leidian\LDPlayer9",
        ],
        "procs": ["dnplayer.exe", "Ld9BoxHeadless.exe", "LdVBoxHeadless.exe"],
        "path_tokens": ["ldplayer9", "ldplayer9box"],
        "registry": ["雷电模拟器9", "LDPlayer9"],
    },
    {
        "id": "ldplayer14",
        "name": "雷电模拟器 14",
        "dirs": [
            r"C:\leidian\LDPlayer14",
            r"C:\LDPlayer\LDPlayer14",
            r"C:\Program Files\leidian\LDPlayer14",
        ],
        "procs": ["dnplayer.exe", "Ld14BoxHeadless.exe"],
        "path_tokens": ["ldplayer14", "ldplayer14box"],
        "registry": ["雷电模拟器14", "LDPlayer14"],
    },
    {
        "id": "tencent-appstore-pc",
        "name": "腾讯应用宝电脑版",
        "dirs": [r"C:\Program Files\Tencent\Androws", r"C:\Program Files (x86)\Tencent\Androws"],
        "procs": ["Androws.exe", "AndrowsAssistant.exe", "AndrowsDlSvr.exe"],
        "path_tokens": ["androws"],
        "registry": ["应用宝", "Androws"],
    },
    {
        "id": "mumu",
        "name": "MuMu 模拟器",
        "dirs": [
            r"C:\Program Files\Netease\MuMuPlayer-12.0",
            r"C:\Program Files\Netease\MuMu Player 12",
        ],
        "procs": ["MuMuPlayer.exe", "MuMuVMMHeadless.exe", "MuMuNxDevice.exe"],
        "path_tokens": ["mumu"],
        "registry": ["MuMu"],
    },
    {
        "id": "nox",
        "name": "夜神模拟器",
        "dirs": [r"C:\Program Files\Nox\bin", r"C:\Program Files (x86)\Nox\bin"],
        "procs": ["Nox.exe", "NoxVMHandle.exe"],
        "path_tokens": ["nox"],
        "registry": ["Nox", "夜神"],
    },
]

ADB_CANDIDATES = [
    r"C:\Program Files\platform-tools\adb.exe",
    r"C:\platform-tools\adb.exe",
]

IAPP_PKG = "com.iapp.app"


# ---------------------------------------------------------------- 基础工具

def run(cmd, timeout=TIMEOUT):
    """跑外部命令，永远返回 (code, out, err)，不抛异常。"""
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=False,
        )
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except FileNotFoundError:
        return 127, "", "command not found"
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as exc:  # noqa: BLE001 - 探测脚本不该因为单项失败中断
        return 1, "", str(exc)


def probe(pid, status, value=None, detail=None, error=None):
    return {"id": pid, "status": status, "value": value, "detail": detail, "error": error}


def win_env(name):
    return os.environ.get(name, "")


# ---------------------------------------------------------------- 宿主

def probe_host():
    info = {
        "os": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
    if IS_WIN:
        try:
            caption = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; "
                 "(Get-CimInstance Win32_OperatingSystem).Caption"],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=TIMEOUT,
            ).stdout.strip()
            info["caption"] = caption or None
        except Exception:  # noqa: BLE001
            info["caption"] = None
    return info


def probe_virtualization():
    out = {"hypervisor_present": None, "detail": None}
    if not IS_WIN:
        out["detail"] = "non-windows: skipped"
        return out
    code, stdout, _ = run([
        "powershell", "-NoProfile", "-Command",
        "(Get-CimInstance Win32_ComputerSystem).HypervisorPresent",
    ])
    if code == 0 and stdout:
        out["hypervisor_present"] = stdout.strip().lower() == "true"
        out["detail"] = "Win32_ComputerSystem.HypervisorPresent"
    else:
        out["detail"] = "unavailable (不要求管理员，拿不到就记 unknown)"
    return out


# ---------------------------------------------------------------- 模拟器

def registry_entries():
    """读卸载表，返回 [{name, version, location}]。非 Windows 返回空表。"""
    if not IS_WIN:
        return []
    try:
        import winreg
    except ImportError:
        return []

    roots = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    entries = []
    for hive, path in roots:
        try:
            key = winreg.OpenKey(hive, path)
        except OSError:
            continue
        try:
            index = 0
            while True:
                try:
                    sub_name = winreg.EnumKey(key, index)
                except OSError:
                    break
                index += 1
                try:
                    sub = winreg.OpenKey(key, sub_name)
                    name = winreg.QueryValueEx(sub, "DisplayName")[0]
                    version = winreg.QueryValueEx(sub, "DisplayVersion")[0]
                    try:
                        location = winreg.QueryValueEx(sub, "InstallLocation")[0]
                    except OSError:
                        location = ""
                    entries.append({"name": name, "version": version, "location": location})
                except OSError:
                    continue
        finally:
            try:
                winreg.CloseKey(key)
            except OSError:
                pass
    return entries


def running_processes():
    """返回 {进程名小写(不带 .exe): [可执行路径]}。拿不到路径时值为空列表。"""
    result = {}
    if not IS_WIN:
        code, out, _ = run(["ps", "-eo", "comm="])
        if code == 0:
            for line in out.splitlines():
                name = line.strip()
                if name:
                    result.setdefault(name.lower(), [])
        return result

    # 一次拿全量的「进程名 + 路径」：dnplayer.exe 在雷电 9/14 下同名，必须靠路径区分
    code, out, _ = run([
        "powershell", "-NoProfile", "-Command",
        "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; "
        "Get-Process | ForEach-Object { \"$($_.ProcessName)`t$($_.Path)\" }",
    ], timeout=TIMEOUT * 2)
    if code == 0 and out:
        for line in out.splitlines():
            name, _, path = line.partition("\t")
            name, path = name.strip().lower(), path.strip()
            if not name:
                continue
            bucket = result.setdefault(name, [])
            if path and path not in bucket:
                bucket.append(path)
        return result

    # PowerShell 不可用时退回进程名（没有路径，产品区分会变粗）
    code, out, _ = run(["tasklist", "/FO", "CSV", "/NH"])
    if code == 0:
        for line in out.splitlines():
            parts = [p.strip('"') for p in line.split('","')]
            if len(parts) < 2:
                continue
            name = parts[0].strip('"').lower()
            if name.endswith(".exe"):
                name = name[:-4]
            if name:
                result.setdefault(name, [])
    return result


def probe_products(reg_entries, procs):
    products = []
    for spec in PRODUCTS:
        found_dirs = []
        for d in spec["dirs"]:
            expanded = os.path.expandvars(d)
            if os.path.isdir(expanded):
                found_dirs.append(expanded)

        found_regs = [
            e for e in reg_entries
            if any(token.lower() in (e["name"] or "").lower() for token in spec["registry"])
        ]

        tokens = [t.lower() for t in spec.get("path_tokens", [])]
        found_procs = []
        for p in spec["procs"]:
            key = p.lower()
            if key.endswith(".exe"):
                key = key[:-4]
            if key not in procs:
                continue
            paths = procs[key]
            if paths and tokens:
                matched = [
                    x for x in paths
                    if any(t in x.lower().replace("/", "\\") for t in tokens)
                ]
                if not matched:
                    continue  # 同名进程但路径不属于这个产品（dnplayer.exe 属于另一套雷电）
                paths = matched
            found_procs.append({"name": p, "paths": paths})

        installed = bool(found_dirs or found_regs or found_procs)
        version = found_regs[0]["version"] if found_regs and found_regs[0]["version"] else None

        products.append({
            "id": spec["id"],
            "name": spec["name"],
            "installed": installed,
            "running": bool(found_procs),
            "install_dirs": found_dirs,
            "registry": found_regs,
            "processes": found_procs,
            "version": version,
        })
    return products


# ---------------------------------------------------------------- adb

def resolve_adb(explicit=None):
    for cand in (explicit, os.environ.get("ADB"), shutil.which("adb"), *ADB_CANDIDATES):
        if cand and os.path.isfile(cand):
            return cand
    return None


def probe_adb(adb_path):
    info = {"path": adb_path, "version": None, "devices": [], "error": None}
    if not adb_path:
        info["error"] = "adb not found"
        return info

    code, out, err = run([adb_path, "version"])
    if code == 0 and out:
        info["version"] = out.splitlines()[0].strip()
    else:
        info["error"] = err or f"exit {code}"
        return info

    code, out, _ = run([adb_path, "devices", "-l"])
    if code != 0:
        return info

    for line in out.splitlines()[1:]:
        line = line.strip()
        if not line or line.startswith("*"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        serial, state = parts[0], parts[1]
        device = {"serial": serial, "state": state}
        if state == "device":
            device.update(probe_device_shell(adb_path, serial))
        info["devices"].append(device)
    return info


def device_getprop(adb_path, serial, prop):
    code, out, _ = run([adb_path, "-s", serial, "shell", "getprop", prop])
    return out if code == 0 and out else None


def probe_device_shell(adb_path, serial):
    """设备内只读查询。单条失败不影响其它。"""
    out = {
        "api": device_getprop(adb_path, serial, "ro.build.version.sdk"),
        "android": device_getprop(adb_path, serial, "ro.build.version.release"),
        "model": device_getprop(adb_path, serial, "ro.product.model"),
        "iapp": {"installed": None, "uid": None, "version": None},
        "project_root": {},
        "storage_permission": None,
        "root": None,
    }

    code, stdout, _ = run([adb_path, "-s", serial, "shell", "pm", "list", "packages", "-U"])
    if code == 0:
        for line in stdout.splitlines():
            if line.startswith("package:") and IAPP_PKG in line:
                out["iapp"]["installed"] = True
                if "uid:" in line:
                    out["iapp"]["uid"] = line.split("uid:")[-1].strip()
                break
        else:
            out["iapp"]["installed"] = False

    if out["iapp"]["installed"]:
        code, stdout, _ = run([adb_path, "-s", serial, "shell", "dumpsys", "package", IAPP_PKG])
        if code == 0:
            for line in stdout.splitlines():
                if "versionName=" in line:
                    out["iapp"]["version"] = line.split("versionName=")[-1].strip()
                    break

        code, stdout, _ = run([
            adb_path, "-s", serial, "shell", "readlink",
            f"/storage/emulated/0/Android/data/{IAPP_PKG}/files/iApp/ProjectApp",
        ])
        if code == 0 and stdout:
            out["project_root"]["symlink"] = stdout

        for cand in ("/sdcard/Pictures/ProjectApp", "/sdcard/iApp/ProjectApp"):
            code, stdout, _ = run([adb_path, "-s", serial, "shell", "ls", "-ld", cand])
            if code == 0 and stdout:
                out["project_root"].setdefault("existing", []).append(
                    {"path": cand, "stat": stdout}
                )

        code, stdout, _ = run([
            adb_path, "-s", serial, "shell", "appops", "get", IAPP_PKG,
            "MANAGE_EXTERNAL_STORAGE",
        ])
        if code == 0 and stdout:
            out["storage_permission"] = stdout.strip()

    code, stdout, _ = run([adb_path, "-s", serial, "shell", "su", "-c", "id"])
    if code == 0 and "uid=0" in stdout:
        out["root"] = True
    elif code == 0:
        out["root"] = False
    return out


# ---------------------------------------------------------------- 共享目录 / FTP

def probe_shared(mirror_root, adb_path, devices):
    info = {"host": str(mirror_root) if mirror_root else None, "guest": None, "status": "unknown"}
    if not mirror_root:
        info["status"] = "unconfigured"
        return info

    mirror = Path(mirror_root)
    if not mirror.is_dir():
        info["status"] = "missing"
        return info

    info["has_projectapp"] = (mirror / "ProjectApp").is_dir()

    with_device = [d for d in devices if d.get("state") == "device"]
    if not with_device:
        info["status"] = "unknown"
        info["detail"] = "有宿主目录，但没有 adb 设备可核设备侧"
        return info

    code, stdout, _ = run([
        adb_path, "-s", with_device[0]["serial"], "shell", "ls", "-d",
        "/sdcard/Pictures/ProjectApp",
    ])
    if code == 0 and stdout:
        info["guest"] = "/sdcard/Pictures/ProjectApp"
        info["status"] = "ok"
    else:
        info["status"] = "missing-guest"
    return info


def probe_ftp(spec, timeout=5):
    info = {"spec": spec, "status": "skipped"}
    if not spec:
        return info

    host, _, port = spec.partition(":")
    port = int(port) if port.isdigit() else 21
    info.update({"host": host, "port": port})

    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
    except Exception as exc:  # noqa: BLE001
        info["status"] = "unreachable"
        info["error"] = str(exc)
        info["hint"] = "宿主不可达不代表服务端不可用；先试 adb forward，或在设备内终端连 127.0.0.1:<端口>"
        return info

    try:
        import ftplib
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=timeout)
        ftp.login("anonymous", "anonymous@example.com")
        info["login"] = "ok"
        try:
            info["features"] = [ln.strip() for ln in ftp.sendcmd("FEAT").splitlines()[1:-1]]
        except Exception:  # noqa: BLE001
            info["features"] = None
        try:
            info["root_listing"] = ftp.nlst()[:20]
        except Exception:  # noqa: BLE001
            info["root_listing"] = None
        ftp.quit()
        info["status"] = "ok"
    except Exception as exc:  # noqa: BLE001
        info["status"] = "auth_failed" if "530" in str(exc) else "error"
        info["error"] = str(exc)
    return info


# ---------------------------------------------------------------- 汇总

def summarize(host, virt, products, adb, shared, ftp):
    channels = {
        "shared": "ok" if shared.get("status") == "ok" else
                  ("unknown" if shared.get("status") in ("unknown", "unconfigured") else "unavailable"),
        "adb": "ok" if any(d.get("state") == "device" for d in adb.get("devices", [])) else "unavailable",
        "ftp": "ok" if ftp.get("status") == "ok" else
               ("unknown" if ftp.get("status") == "skipped" else "unavailable"),
    }

    profile = None
    running = [p["id"] for p in products if p["running"]]
    if "ldplayer14" in running:
        profile = "ldplayer14"
    elif "ldplayer9" in running:
        profile = "ldplayer9"
    elif "tencent-appstore-pc" in running:
        profile = "tencent-appstore-pc"
    elif any(p["installed"] for p in products):
        installed = [p["id"] for p in products if p["installed"]]
        profile = installed[0]

    if channels["shared"] == "ok":
        primary, fallbacks = "shared", [c for c, s in channels.items() if s == "ok" and c != "shared"]
    elif channels["adb"] == "ok":
        primary, fallbacks = "adb", [c for c, s in channels.items() if s == "ok" and c != "adb"]
    elif channels["ftp"] == "ok":
        primary, fallbacks = "ftp", []
    else:
        primary, fallbacks = None, []

    return {
        "channels": channels,
        "profile": profile,
        "recommendation": {
            "primary": primary,
            "fallbacks": fallbacks,
            "reason": "按可用性取第一条；同一条通道的写入不要并行",
        },
    }


def human_report(result):
    host = result["host"]
    virt = result["virtualization"]
    adb = result["adb"]
    lines = []
    lines.append(f"== 环境探测 {result['generated_at']} ==")
    lines.append(
        f"宿主  {host.get('caption') or host['os']} {host.get('version', '')}".rstrip()
    )
    hyper = virt.get("hypervisor_present")
    lines.append(
        f"虚拟化 Hyper-V={'on' if hyper is True else 'off' if hyper is False else 'unknown'}"
    )

    for p in result["products"]:
        if p["installed"]:
            state = "运行中" if p["running"] else "已安装"
            ver = f" v{p['version']}" if p["version"] else ""
            lines.append(f"产品  {p['name']}{ver} — {state}")

    if adb["path"]:
        lines.append(f"adb   {adb['path']} ({adb.get('version') or '?'})")
        if adb["devices"]:
            for d in adb["devices"]:
                extra = ""
                if d.get("state") == "device":
                    extra = f" API={d.get('api')} android={d.get('android')} model={d.get('model')}"
                    iapp = d.get("iapp") or {}
                    if iapp.get("installed"):
                        extra += f" iApp={iapp.get('version') or '?'} uid={iapp.get('uid') or '?'}"
                    if d.get("root") is True:
                        extra += " root=yes"
                    root_info = d.get("project_root") or {}
                    if root_info.get("symlink"):
                        extra += f" 工程根->{root_info['symlink']}"
                lines.append(f"       {d['serial']} [{d['state']}]{extra}")
        else:
            lines.append("       无 device 状态目标")
    else:
        lines.append("adb   未找到")

    shared = result["shared"]
    lines.append(f"共享  {shared.get('host') or '未配置'} -> {shared.get('guest') or '?'} [{shared.get('status')}]")
    ftp = result["ftp"]
    lines.append(f"FTP   {ftp.get('spec') or '未配置'} [{ftp.get('status')}]")
    if ftp.get("hint"):
        lines.append(f"      {ftp['hint']}")

    ch = result["channels"]
    lines.append(f"通道  shared={ch['shared']} adb={ch['adb']} ftp={ch['ftp']}")
    rec = result["recommendation"]
    if rec["primary"]:
        lines.append(f"建议  {rec['primary']}（备选 {', '.join(rec['fallbacks']) or '无'}）；档案 {result['profile'] or '待建'}")
    else:
        lines.append("建议  没有可用通道：先启动模拟器，或用 --ftp 指定设备地址")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="只读探测本机 iApp 开发环境")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--ftp", metavar="HOST:PORT", help="设备侧 FTP 地址（只验证宿主可达性）")
    parser.add_argument("--mirror-root", metavar="PATH", help="宿主共享目录镜像根（默认 <repo>/android-sync）")
    parser.add_argument("--adb", metavar="PATH", help="adb 可执行文件路径")
    args = parser.parse_args(argv)

    if args.ftp and ":" not in args.ftp:
        print("参数错误：--ftp 需要 HOST:PORT", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[2]
    mirror = Path(args.mirror_root) if args.mirror_root else (repo_root / "android-sync")
    if not mirror.is_dir():
        mirror = None

    started = time.time()
    try:
        host = probe_host()
        virt = probe_virtualization()
        procs = running_processes()
        products = probe_products(registry_entries(), procs)
        adb = probe_adb(resolve_adb(args.adb))
        shared = probe_shared(mirror, adb["path"], adb["devices"])
        ftp = probe_ftp(args.ftp)
        summary = summarize(host, virt, products, adb, shared, ftp)
    except Exception as exc:  # noqa: BLE001
        print(f"探测内部异常: {exc}", file=sys.stderr)
        return 3

    result = {
        "schema": 1,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_seconds": round(time.time() - started, 2),
        "host": host,
        "virtualization": virt,
        "products": products,
        "adb": adb,
        "shared": shared,
        "ftp": ftp,
        **summary,
    }

    if args.json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(human_report(result))

    return 0 if summary["recommendation"]["primary"] else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
