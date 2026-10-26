# 工作区规则（本机）

## 三层，内容不混

| 层 | 位置 | 放什么 | 判据 |
|---|---|---|---|
| SKILL | `.claude/skills/iapp-development/` | 通用 iApp 知识：SKILL.md + references/ + cases/ | 换台机器仍成立 |
| 本文件 | 工作区根 | 本机路径、设备、投递链路、协作约定、导航 | 只对本机成立，不复制 SKILL |
| docs | `docs/` | 本机事实与证据；索引见 `docs/README.md` | 原始读数、环境快照 |

不确定归哪层时：先写 `docs/evidence.md`，提炼后再进 SKILL。

## 本机变量（只在这里定义一次）

```
IAPP_PKG       = com.iapp.app
ADB            = E:\Program Files\platform-tools\adb.exe
BUILD_TOOLS    = E:\Program Files\build-tools_r35_windows\android-15
JDK            = E:\Program Files\openjdk-25_windows-x64_bin\jdk-25\bin
PYTHON         = E:\Program Files\python3.13.17
DEVICE         = emulator-5554（LDPlayer9，Android 9 / API 28，adb root 可用）
DEV_PROJECT    = /storage/emulated/0/iApp/ProjectApp/<项目ID>
SHARED_HOST    = E:\workspaces\2026-10-24-iapp-dev-ai-space\android-sync
SHARED_GUEST   = /mnt/shared/Pictures
```

细节见 `docs/runtime-env.md`，装机/连机步骤见 `docs/dev-env-setup.md`。

## 投递链路

**主链路（已实测）**：iApp 的工程根已被设置为 `Pictures/ProjectApp`，而 `/sdcard/Pictures` 就是 LDPlayer 的共享目录：

```
宿主机 android-sync/ProjectApp/<项目ID>/  ==  /sdcard/Pictures/ProjectApp/<项目ID>/
```

- 直接改宿主机文件即等于改设备工程（vboxsf 实时，md5 已对齐）
- iApp 仍以内存为准：改文件前先 `am force-stop`，改完请用户重新打开工程
- 不需要 bind mount、不需要 push

**兜底（共享目录不可用时）**：

```
adb shell am force-stop $IAPP_PKG
adb push <host 文件> /storage/emulated/0/iApp/ProjectApp/<项目ID>/src/<名>
adb shell chown u0_a50:sdcard_rw .../src/*; chmod 660 .../src/*
```

- **不要用 bind mount**：sdcardfs + 应用独立 mount namespace，挂载对 iApp 不可见（证据见 `docs/evidence.md` B0）
- 用户负责在 iApp 里运行并回报；Claude 不代点界面
- **改完源码不要 `am force-stop` iApp**：用户会按规范自己关闭/重开工程（旧行为已废弃）
- 日志：`adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'`

## 目录约定

- `android-sync/` 只放 iApp 工程镜像，层级与设备一致：`android-sync/ProjectApp/<包名>/`
  - 项目 `src/` 只允许 `.iyu` 和 `.mjava`，入口必须叫 `mian.iyu`
  - 临时探针放 `android-sync/iapp-demo/<批次>/`，用完即删
  - `android-sync/cache`、`android-sync/data` 是 LDPlayer 共享目录自带，忽略
  - **镜像是手动快照，不与设备自动同步**：共享目录只映射 `android-sync/` ↔ `/mnt/shared/Pictures`，工程目录在设备 `.../iApp/ProjectApp/<项目ID>`，两者无关；设备上的新增文件（如 jar）不会出现在宿主机，需 `adb pull` 刷新（`docs/scripts/refresh-mirror.sh`）
- `docs/`：`README.md` 索引、`runtime-env.md`、`dev-env-setup.md`、`evidence.md`、`reference/`（官方手册）、`artifacts/`（APK 等）、`plans/`、`specs/`
- 文档和代码用 `<包名>` / `<项目ID>` 占位，不写死；本机实际值只在本文件的变量区定义

## 开发取向

- **本工作区默认产出物就是 iApp 工程**：不必再问需求面向什么环境/平台，一律按 iApp（`.iyu` + `.mjava` + 本机投递链路）来设计；只有用户明确说要别的介质时才例外。
- 官方两份 txt 手册（`docs/reference/iyu-helpV3.0.txt`、`ijava-helpV3.0.txt`）不完整、偶有错别字和过时内容，**只作参考**，最终会被淘汰；不要把它们当权威。
- 真实开发面向**通用 Android 原生知识**（Activity/View/权限/WebView/存储等），iApp 只提供容器与调用桥。
- iyu 层尽量只写 `call` 编排和事件绑定，具体实现放进 `.mjava`；这样逻辑可迁移、可测试。

## 知识沉淀（强制）

每轮探针结束必须回填，不许攒：

1. 原始读数先写 `docs/evidence.md`（日期、批次、探针、logcat 原文、屏幕现象）
2. 提炼后的通用结论回填 SKILL（带版本前提，✅/⚠/❓）
3. 本机事实回填 `docs/runtime-env.md` 或 `docs/dev-env-setup.md`

## 每轮探针流程

1. 探针源码写进 `android-sync/iapp-demo/<批次>/`
2. force-stop → push → 清 logcat
3. 用户运行并回报现象
4. 拉 logcat，把日期、批次号、原始读数写进 `docs/evidence.md`
5. 提炼通用结论回填 SKILL（含版本前提），再清掉临时探针
6. 汇报按：验了哪几条 / 一致·推翻·未知 / 回填了哪些文件 / 下一轮要用户做什么

## 导航

- 通用知识：`.claude/skills/iapp-development/SKILL.md`
- 本机事实：`docs/README.md`
