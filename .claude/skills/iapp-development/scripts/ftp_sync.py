#!/usr/bin/env python3
"""通过 iApp 内置 FTP 单向同步工程目录（全量 + SIZE/MD5 校验）。

对应 iApp「服务器控制台」给出的 ftp://<设备IP>:<端口>；远端的根是 iApp 应用级文件区，
工程通常在 /ProjectApp/<项目ID>。

用法：
    # 预演（只读）
    python ftp_sync.py --host <设备IP> --port <端口> \
        --remote /ProjectApp/<项目ID> --local-root <本地工程目录> --dry-run

    # 推（宿主 -> 设备）
    python ftp_sync.py --host <IP> --port <PORT> --remote /ProjectApp/<ID> --local-root <本地工程>

    # 拉（设备 -> 宿主；首次建镜像或回滚）
    python ftp_sync.py --host <IP> --port <PORT> --remote /ProjectApp/<ID> --local-root <本地工程> --pull

退出码：
    0 全部成功（或 dry-run 无差异）
    1 参数错误
    2 连接/登录失败
    3 传输失败（有文件没传成功）
    4 校验失败（SIZE 或 MD5 不一致）
    5 远端路径/权限失败

注意：iApp 以内存为准，推送前请先在 App 内关掉工程（或 am force-stop）。
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import os
import posixpath
import re
import shutil
import subprocess
import sys
from ftplib import FTP, FTP_TLS, all_errors
from pathlib import Path

DEFAULT_EXCLUDES = [".git", ".claude", "__pycache__", ".idea", ".vscode"]
DEFAULT_MANAGED = ["src", "sdk"]
DOTFILES = [".project"]  # 目录列表（MLSD/NLST）通常看不到点文件，这里点名探
BLOCK = 64 * 1024
ALL_ERRORS = all_errors + (RuntimeError,)  # all_errors 是元组，嵌套进 except 会 TypeError

# 为 NAT 隔离的设备建立的 adb 转发：(serial, 端口)。退出时统一清掉。
FORWARDS: list[tuple[str, int]] = []


def _ensure_forward(adb, serial, port):
    key = (serial, int(port))
    if key in FORWARDS:
        return
    proc = subprocess.run(
        [adb, "-s", serial, "forward", f"tcp:{port}", f"tcp:{port}"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"adb forward tcp:{port} 失败：{(proc.stderr or proc.stdout).strip()}")
    FORWARDS.append(key)


def _cleanup_forwards(adb):
    if not adb:
        return
    for serial, port in list(FORWARDS):
        subprocess.run([adb, "-s", serial, "forward", "--remove", f"tcp:{port}"],
                       capture_output=True)
        FORWARDS.remove((serial, port))


class _AdbForwardMixin:
    """PASV 返回的是设备自己的地址，宿主到不了；把每个数据端口也转发一次再连 127.0.0.1。"""
    adb = None
    serial = None

    def makepasv(self):
        _host, port = super().makepasv()
        _ensure_forward(self.adb, self.serial, port)
        return "127.0.0.1", int(port)


class AdbForwardFTP(_AdbForwardMixin, FTP):
    pass


class AdbForwardFTP_TLS(_AdbForwardMixin, FTP_TLS):
    pass


# ------------------------------------------------------------------ 本地

def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(BLOCK), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_local(root: Path, excludes: set[str]):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in excludes)
        for name in sorted(filenames):
            if name in excludes or name.endswith(".part"):
                continue
            abs_path = Path(dirpath) / name
            rel = abs_path.relative_to(root).as_posix()
            files.append((rel, abs_path, abs_path.stat().st_size))
    return files


def looks_rewritten(path: str) -> bool:
    p = path.replace("\\", "/")
    if re.match(r"^[A-Za-z]:", p):
        return True
    return "Program Files/Git" in p or "Program Files (x86)/Git" in p


# ------------------------------------------------------------------ 远端

def connect(args):
    host = args.host
    adb = None
    if args.adb_forward:
        adb = args.adb or shutil.which("adb") or os.environ.get("ADB")
        if not adb:
            raise RuntimeError("指定了 --adb-forward，但找不到 adb（用 --adb 指定路径）")
        _ensure_forward(adb, args.adb_forward, args.port)
        host = host or "127.0.0.1"

    if args.adb_forward:
        cls = AdbForwardFTP_TLS if args.tls else AdbForwardFTP
        ftp = cls()
        ftp.adb = adb
        ftp.serial = args.adb_forward
    else:
        cls = FTP_TLS if args.tls else FTP
        ftp = cls()
    ftp.encoding = "utf-8"
    ftp.connect(host, args.port, timeout=args.timeout)
    if args.tls:
        ftp.auth()  # 显式 TLS
    user = args.user or os.environ.get("FTP_USER") or "anonymous"
    password = os.environ.get(args.password_env, "") if args.password_env else ""
    if not password:
        if user == "anonymous":
            password = "anonymous@example.com"
        else:
            password = getpass.getpass(f"FTP password for {user}: ")
    ftp.login(user, password)
    if args.tls:
        ftp.prot_p()
    ftp.voidcmd("TYPE I")  # 全程二进制
    ftp.set_pasv(True)
    return ftp


def remote_size(ftp, path):
    """存在返回字节数（0 是合法值），不存在返回 None；不支持 SIZE 也返回 None。"""
    try:
        resp = ftp.sendcmd("SIZE " + path)
    except all_errors:
        return None
    if not resp.startswith("213"):
        return None
    try:
        return int(resp.split()[1])
    except (IndexError, ValueError):
        return None


def remote_md5(ftp, path):
    try:
        resp = ftp.sendcmd("MD5 " + path)
    except all_errors:
        return None
    for token in resp.split():
        if len(token) == 32 and all(c in "0123456789abcdefABCDEF" for c in token):
            return token.lower()
    return None


def ensure_remote_root(ftp, remote_root):
    """从 / 开始逐级建出远端根；MKD 不递归，父目录必须先存在。"""
    cur = ""
    for part in [p for p in remote_root.strip("/").split("/") if p]:
        cur = f"{cur}/{part}"
        try:
            ftp.cwd(cur)
        except all_errors:
            try:
                ftp.mkd(cur)
            except all_errors as exc:
                raise RuntimeError(f"远端根不可用 {cur}: {exc}") from exc


def ensure_remote_dir(ftp, remote_root, rel_dir):
    """逐级建目录；已存在则跳过。"""
    if not rel_dir:
        return
    cur = remote_root.rstrip("/")
    for part in [p for p in rel_dir.split("/") if p]:
        cur = f"{cur}/{part}"
        try:
            ftp.cwd(cur)
        except all_errors:
            try:
                ftp.mkd(cur)
            except all_errors as exc:
                raise RuntimeError(f"无法创建远端目录 {cur}: {exc}") from exc


def walk_remote(ftp, root):
    """返回 (files, dirs)，路径相对 root。MLSD 失败时回落到 NLST + SIZE 判定。"""
    files, dirs = [], []
    stack = [""]
    while stack:
        rel = stack.pop()
        path = posixpath.join(root, rel) if rel else root
        try:
            entries = [(name, facts.get("type", "")) for name, facts in ftp.mlsd(path)]
        except all_errors:
            entries = None

        if entries is None:
            try:
                names = ftp.nlst(path)
            except all_errors:
                continue
            for item in names:
                name = posixpath.basename(item.rstrip("/"))
                if not name or name in (".", ".."):
                    continue
                full = posixpath.join(path, name)
                child = posixpath.join(rel, name) if rel else name
                if remote_size(ftp, full) is not None:
                    files.append(child)
                else:
                    dirs.append(child)
                    stack.append(child)
            continue

        for name, typ in entries:
            if name in (".", ".."):
                continue
            child = posixpath.join(rel, name) if rel else name
            if typ in ("cdir", "pdir"):
                continue
            if typ == "dir":
                dirs.append(child)
                stack.append(child)
            elif typ == "file":
                files.append(child)
    return files, dirs


# ------------------------------------------------------------------ 同步

def push(ftp, args, local_files):
    remote_root = args.remote.rstrip("/")
    if not args.dry_run:
        ensure_remote_root(ftp, remote_root)
    made_dirs = set()
    uploaded = 0
    failed = []
    verify_md5 = 0
    md5_supported = True

    for rel, abs_path, size in local_files:
        remote_path = f"{remote_root}/{rel}"
        parent = posixpath.dirname(rel)

        if args.dry_run:
            cur = remote_size(ftp, remote_path)
            if cur is None:
                mark = "+"
            elif cur != size:
                mark = "~"
            else:
                mark = "="
            print(f"  {mark} {rel} ({size}B)" + ("" if cur is None else f" 远端 {cur}B"))
            continue

        if parent and parent not in made_dirs:
            try:
                ensure_remote_dir(ftp, remote_root, parent)
                made_dirs.add(parent)
            except RuntimeError as exc:
                failed.append((rel, str(exc)))
                continue

        try:
            with open(abs_path, "rb") as fh:
                ftp.storbinary(f"STOR {remote_path}", fh, blocksize=BLOCK)
            uploaded += 1
        except all_errors as exc:
            failed.append((rel, f"STOR: {exc}"))
            continue

        if args.no_verify:
            continue
        got = remote_size(ftp, remote_path)
        if got is None:
            print(f"  ! {rel} 服务端不支持 SIZE，跳过大小校验")
            continue
        if got != size:
            failed.append((rel, f"SIZE 不一致：本地 {size} / 远端 {got}"))
            continue
        if md5_supported:
            remote_hash = remote_md5(ftp, remote_path)
            if remote_hash is None:
                md5_supported = False
                md5_verify_note = "服务端不支持 MD5，本次只校验 SIZE"
                print(f"  ! {md5_verify_note}")
            elif remote_hash != md5_file(abs_path):
                failed.append((rel, "MD5 不一致"))
            else:
                verify_md5 += 1

    if args.delete_extras and not args.dry_run:
        remote_files, _ = walk_remote(ftp, remote_root)
        local_set = {rel for rel, _, _ in local_files}
        managed = [d.strip("/") for d in args.managed_dirs if d.strip()]
        for rel in remote_files:
            if rel in local_set:
                continue
            if any(rel == m or rel.startswith(m + "/") for m in managed):
                try:
                    ftp.delete(f"{remote_root}/{rel}")
                    print(f"  - 删除远端多余文件 {rel}")
                except all_errors as exc:
                    failed.append((rel, f"DELE: {exc}"))

    return {
        "mode": "dry-run" if args.dry_run else "push",
        "files": len(local_files),
        "uploaded": uploaded,
        "md5_verified": verify_md5,
        "md5_supported": md5_supported,
        "failed": failed,
    }


def pull(ftp, args):
    remote_root = args.remote.rstrip("/")
    try:
        ftp.cwd(remote_root)
    except all_errors as exc:
        raise RuntimeError(f"远端路径不存在或不可访问 {remote_root}: {exc}") from exc

    local_root = Path(args.local_root)
    local_root.mkdir(parents=True, exist_ok=True)

    remote_files, dirs = walk_remote(ftp, remote_root)
    for name in DOTFILES:
        if remote_size(ftp, f"{remote_root}/{name}") is not None and name not in remote_files:
            remote_files.append(name)

    downloaded = 0
    failed = []
    verified = 0

    for rel in sorted(remote_files):
        remote_path = f"{remote_root}/{rel}"
        target = local_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)

        if args.dry_run:
            print(f"  + {rel}")
            continue

        tmp = target.with_name(target.name + ".part")
        try:
            expected = remote_size(ftp, remote_path)
            with open(tmp, "wb") as fh:
                ftp.retrbinary(f"RETR {remote_path}", fh.write, blocksize=BLOCK)
            actual = tmp.stat().st_size
            if expected is not None and expected != actual:
                raise RuntimeError(f"SIZE 不一致：远端 {expected} / 本地 {actual}")
            if not args.no_verify:
                remote_hash = remote_md5(ftp, remote_path)
                if remote_hash and remote_hash != md5_file(tmp):
                    raise RuntimeError("MD5 不一致")
                if remote_hash:
                    verified += 1
            os.replace(tmp, target)
            downloaded += 1
        except (all_errors, OSError, RuntimeError) as exc:
            failed.append((rel, str(exc)))
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass

    return {
        "mode": "dry-run" if args.dry_run else "pull",
        "files": len(remote_files),
        "downloaded": downloaded,
        "md5_verified": verified,
        "failed": failed,
    }


# ------------------------------------------------------------------ CLI

def build_parser():
    p = argparse.ArgumentParser(
        description="通过 iApp 内置 FTP 全量同步工程目录（SIZE/MD5 校验，纯标准库）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--host", default=None,
                   help="设备 IP 或主机名；用 --adb-forward 时可省略（自动连 127.0.0.1）")
    p.add_argument("--port", type=int, default=21, help="FTP 端口（iApp 常给非 21，按界面填）")
    p.add_argument("--adb-forward", metavar="SERIAL", default=None,
                   help="设备在 NAT 后、宿主直连不到时：用该 adb 序列号把控制端口和每个数据端口逐个转发")
    p.add_argument("--adb", metavar="PATH", default=None, help="adb 可执行文件（默认 PATH / ADB 环境变量）")
    p.add_argument("--user", default=None, help="默认 anonymous")
    p.add_argument("--password-env", default="FTP_PASSWORD", help="从该环境变量取密码（默认 FTP_PASSWORD）")
    p.add_argument("--remote", required=True, help="远端工程根，必须以 / 开头，如 /ProjectApp/<项目ID>")
    p.add_argument("--local-root", default=".", help="宿主工程目录（默认当前目录）")
    p.add_argument("--exclude", default=",".join(DEFAULT_EXCLUDES), help="按目录/文件名排除，逗号分隔")
    p.add_argument("--managed-dirs", default=",".join(DEFAULT_MANAGED),
                   help="只在这些顶层目录内允许 --delete-extras")
    p.add_argument("--pull", action="store_true", help="反方向：设备 -> 宿主")
    p.add_argument("--dry-run", action="store_true", help="只读预演，不写远端")
    p.add_argument("--delete-extras", action="store_true",
                   help="删除远端 managed-dirs 内、本地没有的文件（默认不删）")
    p.add_argument("--no-verify", action="store_true", help="跳过 SIZE/MD5 校验（不推荐）")
    p.add_argument("--tls", action="store_true", help="显式 FTPS；服务器不支持时直接失败，不回退明文")
    p.add_argument("--timeout", type=float, default=20.0, help="连接/单操作超时秒数")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.host and not args.adb_forward:
        print("请给 --host，或用 --adb-forward <serial> 让脚本自己转发。", file=sys.stderr)
        return 1

    if not args.remote.startswith("/"):
        print("--remote 必须以 / 开头（绝对路径，如 /ProjectApp/<项目ID>）。", file=sys.stderr)
        if looks_rewritten(args.remote):
            print("检测到路径被 Git Bash/MSYS 改写成了 Windows 路径；"
                  "请 export MSYS_NO_PATHCONV=1，或用 Python 直接调用。", file=sys.stderr)
        return 1
    if ".." in args.remote.replace("\\", "/").split("/"):
        print("--remote 不允许包含 ..", file=sys.stderr)
        return 1

    local_root = Path(args.local_root).expanduser()
    if not args.pull and not local_root.is_dir():
        print(f"本地目录不存在：{local_root}", file=sys.stderr)
        return 1

    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}
    args.managed_dirs = [d.strip() for d in args.managed_dirs.split(",") if d.strip()]

    try:
        ftp = connect(args)
    except ALL_ERRORS as exc:
        print(f"连接/登录失败：{exc}", file=sys.stderr)
        if args.adb_forward:
            _cleanup_forwards(args.adb or shutil.which("adb") or os.environ.get("ADB"))
        return 2

    try:
        if args.pull:
            result = pull(ftp, args)
        else:
            local_files = collect_local(local_root, excludes)
            if not local_files:
                print(f"本地没有可传文件：{local_root}", file=sys.stderr)
                return 1
            result = push(ftp, args, local_files)
    except ALL_ERRORS as exc:
        print(f"远端路径/权限失败：{exc}", file=sys.stderr)
        return 5
    finally:
        try:
            ftp.quit()
        except Exception:  # noqa: BLE001
            try:
                ftp.close()
            except Exception:  # noqa: BLE001
                pass
        if args.adb_forward:
            _cleanup_forwards(args.adb or shutil.which("adb") or os.environ.get("ADB"))

    failed = result["failed"]
    print()
    print(f"模式：{result['mode']}  远端：{args.remote}  本地：{local_root}")
    print(f"文件总数：{result['files']}")
    if result["mode"] == "pull":
        print(f"下载：{result['downloaded']}/{result['files']}  MD5 校验：{result['md5_verified']}")
    else:
        print(f"上传：{result['uploaded']}/{result['files']}  MD5 校验：{result['md5_verified']}")
        if not result["md5_supported"] and not args.no_verify and result["mode"] != "dry-run":
            print("⚠ 服务端不支持 MD5，本次只校验了 SIZE")
    if failed:
        print(f"失败：{len(failed)}")
        for rel, why in failed:
            print(f"  - {rel}: {why}")
    if result["mode"] == "dry-run":
        print("dry-run：没有写入任何文件")
        return 0
    if not failed:
        print("完成：全部文件已校验通过（退出码 0）")
        return 0
    if any("SIZE" in why or "MD5" in why for _, why in failed):
        print("未完成：存在校验失败，重跑到退出码 0 才算投递成功", file=sys.stderr)
        return 4
    print("未完成：存在传输失败，重跑到退出码 0 才算投递成功", file=sys.stderr)
    return 3


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
