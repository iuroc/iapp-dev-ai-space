#!/usr/bin/env bash
# 把设备上的工程快照拉回宿主机镜像。设备 → 主机单向覆盖。
# 用法：ADB=<adb> DEV_PROJECT=<设备工程目录> ./refresh-mirror.sh <主机镜像目录>
set -euo pipefail
ADB=${ADB:-adb}
DEV_PROJECT=${DEV_PROJECT:?需要 DEV_PROJECT}
DEST=${1:?主机镜像目录}
mkdir -p "$DEST"
"$ADB" pull "$DEV_PROJECT/." "$DEST/"
echo "mirror refreshed -> $DEST"
