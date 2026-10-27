# iApp 开发工作区（本机）

## 这个工作区是做什么的

在 Windows 宿主机上开发、调试、打包 iApp（Android 可视化 IDE，显示名“测兆编程”）工程：
源码是 `.iyu` 界面 + `.mjava` 模块（只做裕 3 + mjava，不涉及 ijava/ilua/mlua），
产物是 iApp 工程和可安装 APK；工程经共享目录投递到雷电模拟器（Android 9/14），
用户在设备上运行并回报。通用知识放 skill（可独立分享），本机事实放 docs。

## 三层，内容不混

| 层 | 位置 | 放什么 | 判据 |
|---|---|---|---|
| SKILL | `.claude/skills/iapp-development/` | 通用 iApp 知识：SKILL.md + references/ + scripts/ | 换台机器仍成立 |
| 本文件 | 工作区根 | 工作区目标、本机路径、设备、投递链路、协作约定、流程、导航 | 只对本机成立，不复制 SKILL |
| docs | `docs/` | 本机事实与证据；索引见 `docs/README.md` | 原始读数、环境快照 |

本文件不教 iApp 语法/API；通用知识一律进 SKILL。不确定归哪层时：先写 `docs/evidence.md`，提炼后再进 SKILL。

## 本机变量（只在这里定义一次）

```
IAPP_PKG       = com.iapp.app
ADB            = E:\Program Files\platform-tools\adb.exe
BUILD_TOOLS    = E:\Program Files\build-tools_r35_windows\android-15
JDK            = E:\Program Files\openjdk-25_windows-x64_bin\jdk-25\bin
PYTHON         = E:\Program Files\python3.13.17
DEVICE         = 不写死，按下方「设备选择」现查；2026-10-27 快照为 emulator-5556（Android 14 / API 34），以 adb devices 为准
DEV_PROJECT    = /sdcard/Pictures/ProjectApp/<项目ID>    # 当前工程根（iApp 设置已改到 Pictures）
DEV_PROJECT_DEFAULT = /sdcard/iApp/ProjectApp/<项目ID>   # 未改设置时的默认位置；仅供参考，以 iApp 设置为准
SHARED_HOST    = E:\workspaces\2026-10-24-iapp-dev-ai-space\android-sync
SHARED_GUEST   = /mnt/shared/Pictures
```

### 设备选择（每次投递前）

`adb devices` 可能同时看到 2 台（多开雷电各占一个端口，serial 会变）：

1. **只有 1 台** → 直接用它
2. **有 2 台** → 默认选 **API 版本高** 的那台
3. **用户指定了 Android 版本** → 按用户要求的版本选

选定后先核版本再投递：

```
adb -s <serial> shell getprop ro.build.version.sdk
```

不要写死 `emulator-5554` / `-5555`：实例序号与端口随多开顺序变化。

细节见 `docs/runtime-env.md`，装机/连机步骤见 `docs/dev-env-setup.md`。

## 投递链路

**主链路（已实测）**：iApp 的工程根已被设置为 `Pictures/ProjectApp`，而 `/sdcard/Pictures` 就是 LDPlayer 的共享目录：

```
宿主机 android-sync/ProjectApp/<项目ID>/  ==  /sdcard/Pictures/ProjectApp/<项目ID>/
```

操作顺序：

1. 改文件前 `am force-stop com.iapp.app`（iApp 以内存为准）。
2. 直接改宿主机文件即等于改设备工程；**但改「已存在」文件后必须核 `/sdcard/Pictures/...` 的 md5**——
   vboxsf 直挂（`/mnt/shared/Pictures`）会立刻更新，FUSE 视图（`/sdcard/Pictures`，iApp 实际读的那侧）
   可能仍是旧内容，新建文件则两侧立刻可见（2026-10-27 实测）。不一致就 `adb push` 兜底。
   工程必须在 iApp 里是关闭的，打开期间设备端可能读到旧缓存。
3. 改完**不要再次 force-stop**；交给用户重新打开工程。用户负责在 iApp 里运行并回报，Claude 不代点界面。
4. 不需要 bind mount；`adb push` 只在共享目录不可用或核不上 md5 时兜底。

**兜底（共享目录不可用时）**：

```
adb shell am force-stop $IAPP_PKG
adb push <host 文件> $DEV_PROJECT/src/<名>
adb shell chown u0_a50:sdcard_rw $DEV_PROJECT/src/*; chmod 660 $DEV_PROJECT/src/*
```

- `u0_a50` 是当前 uid，以 `pm list packages -U com.iapp.app` 为准。
- 如果用户重置过工程根，把 `$DEV_PROJECT` 换成 `$DEV_PROJECT_DEFAULT`，或直接用 iApp 设置里显示的路径。
- **不要用 bind mount**：sdcardfs + 应用独立 mount namespace，挂载对 iApp 不可见（证据见 `docs/evidence.md` B0）。
- 日志：`adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'`

## 目录约定

- `android-sync/` 只放 iApp 工程镜像，层级与设备一致：`android-sync/ProjectApp/<包名>/`
  - 项目 `src/` 只允许 `.iyu` 和 `.mjava`，入口必须叫 `mian.iyu`
  - 临时探针放 `android-sync/iapp-demo/<批次>/`，用完即删
  - `android-sync/cache`、`android-sync/data` 是 LDPlayer 共享目录自带，忽略
  - **镜像是手动快照，不与设备自动同步**：共享目录只映射 `android-sync/` ↔ `/mnt/shared/Pictures`，设备工程在 iApp 设置显示的路径（当前 `$DEV_PROJECT`），两者无关；设备上的新增文件（如 jar）不会出现在宿主机，需 `adb pull` 刷新（`docs/scripts/refresh-mirror.sh`）
- `docs/`：`README.md` 索引、`runtime-env.md`、`dev-env-setup.md`、`evidence.md`、`reference/`（官方手册）、`artifacts/`（APK 等）、`plans/`、`specs/`
- 文档和代码用 `<包名>` / `<项目ID>` 占位，不写死；本机实际值只在本文件的变量区定义

## 开发取向

- **默认按 iApp 工程交付**（`.iyu` + `.mjava` + 本机投递链路）；只有用户明确说要别的介质时才例外。
- 官方两份 txt 手册（`docs/reference/iyu-helpV3.0.txt`、`ijava-helpV3.0.txt`）不完整、偶有错别字和过时内容，**只作参考**，最终会被淘汰；不要把它们当权威。
- 真实开发面向**通用 Android 原生知识**（Activity/View/权限/WebView/存储等），iApp 只提供容器与调用桥。
- iyu 层尽量只写 `call` 编排和事件绑定，具体实现放进 `.mjava`；这样逻辑可迁移、可测试。
- **控件优先在 `.iyu` 里声明自定义控件**（`type=` 完整类名 + `build.xml` 登记），短名兜底；mjava 只做运行期内容填充与必要修复（如 TextInputLayout 盒子），**不要整页动态创建**。
- **版本策略**：验证与开发**优先高版本 Android**（当前 API 34 / LD14）；Android 9（API 28）及以下**只做有限兼容测试**，不追求结论追平。SKILL 里未标注版本的结论默认按 API 34 成立。

## 知识沉淀（强制）

每轮探针结束必须回填，不许攒：

1. 原始读数先写 `docs/evidence.md`（日期、批次、探针、logcat 原文、屏幕现象）
2. 提炼后的通用结论回填 SKILL（带版本前提，✅/⚠/❓）
3. 本机事实回填 `docs/runtime-env.md` 或 `docs/dev-env-setup.md`

- 先证据后结论：没有原始读数不下结论。
- 一条结论只放一个主文件，别处交叉引用，避免同一数字多处维护。
- 对话中推理得出、三层都没有且可复用的知识，也按层回填：通用结论进 SKILL，本机事实进 docs/CLAUDE.md；先确认三层确实没有，避免重复。
- skill 改完跑 `python .claude/skills/iapp-development/scripts/check_portable.py`。

## 每轮探针流程

1. 探针源码写进 `android-sync/iapp-demo/<批次>/`；`.iyu` 的 `type=` 含点号（完整类名）时，工程首次打开后在 `build.xml` 补 `<newControl>` 登记（新工程不继承旧登记）
2. force-stop → 写共享目录（不可用时 `adb push`）→ 清 logcat
3. 用户运行并回报现象
4. 拉 logcat，把日期、批次号、原始读数写进 `docs/evidence.md`
5. 提炼通用结论回填 SKILL（含版本前提），再清掉临时探针
6. 汇报按：验了哪几条 / 一致·推翻·未知 / 回填了哪些文件 / 下一轮要用户做什么

## 导航

- 通用知识：`.claude/skills/iapp-development/SKILL.md`
- 本机事实：`docs/README.md`
