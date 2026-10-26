#!/usr/bin/env bash
# 把主机 src 目录推到设备工程里。
# 用法：
#   export ADB="<adb 路径>"
#   export IAPP_PKG=com.iapp.app
#   ./deploy.sh <主机src目录> <设备工程目录>
set -euo pipefail

HOST_SRC=$(cd "${1:?主机 src 目录}" && pwd)
DEV_PROJ="${2:?设备工程目录}"
ADB=${ADB:-adb}
PKG=${IAPP_PKG:?需要 IAPP_PKG}

# 先停掉 iApp，避免旧内存回写覆盖
"$ADB" shell am force-stop "$PKG" || true

for f in "$HOST_SRC"/*.iyu "$HOST_SRC"/*.mjava; do
  [ -e "$f" ] || continue
  "$ADB" push "$f" "$DEV_PROJ/src/$(basename "$f")"
done

# push 出来的文件属主是 adb root，改成和 iApp 新建文件一致，保证可读
"$ADB" shell "chown 10150:1015 $DEV_PROJ/src/*; chmod 660 $DEV_PROJ/src/*" 2>/dev/null || \
  "$ADB" shell "chmod 666 $DEV_PROJ/src/*"

echo "deployed -> $DEV_PROJ/src"
