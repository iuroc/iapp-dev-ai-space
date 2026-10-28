# iApp 开发工作区（本机）

## 这个工作区是做什么的

在 Windows 宿主机上开发、调试、打包 iApp（Android 可视化 IDE，显示名“测兆编程”）工程：
源码是 `.iyu` 界面 + `.mjava` 模块（只做裕语言 + mjava，不涉及 ijava/ilua/mlua），
产物是 iApp 工程和可安装 APK；工程经**当前环境可用的通道**投递到模拟器/设备（雷电 14 主用），
用户在设备上运行并回报。通用知识放 skill（可独立分享），本机事实放 docs。

## 文档分层（要点）

完整规范在 `.claude/skills/docs-architecture/`（含只读体检脚本），这里只留每轮都要用的几条：

1. 换台机器仍成立 → SKILL；只对本机 → 本文件；读数/快照 → `docs/`。
2. 一条结论只放一个主文件，别处只写一行指针（主文件查表见 `references/architecture.md`）。
3. 每条结论带级别 + 来源 + 日期；他机读数最高 ⚠；标 ❓ 必须写「怎么验」。
4. 先证据后结论：原始读数先进 `docs/evidence.md`，提炼后再往上搬。
5. 新增/改名/删除文件，同一次提交更新最近一层 README 索引。
6. 引用写「文件 §小节」，不写行号；跨 skill 引用带 skill 路径前缀。
7. 冲突裁决：原始读数 > 环境档案 > SKILL 通用结论；同键不同对象不算冲突。
8. 提交前跑 `review_docs.py --fail-on blocker` 与 `check_portable.py`。

本文件不教 iApp 语法/API。

## 环境协商（每次开工 / 每次投递前）

1. 先跑只读探测：

   ```bash
   python docs/scripts/detect_env.py          # 人读摘要
   python docs/scripts/detect_env.py --json   # 机器可读
   ```

2. 按输出读对应档案：`docs/environments/ldplayer14.md`（主）、`ldplayer9.md`（按需）、
   `tencent-appstore-pc.md`（无 adb 的机器）。
3. 用一行写下结论再动手：

   ```
   环境=<档案> / 设备=<serial 或 FTP 地址> / 通道=shared|adb|ftp / 依据=<探测结果>
   ```

4. 探测结果与已知值冲突、或有多台设备/多个 FTP 目标时，**问用户，不要猜**；
   也不要因为「上次是雷电 14」就默认这次还是它。

## 版本政策

- **雷电 14 / API 34 是主开发环境**：新功能、验证、结论默认都在这台上做。
- **雷电 9 / API 28 只在开发者显式声明时启用**（例：「这轮测 Android 9」）；只做有限兼容，
  不追求低版本结论与高版本追平。
- SKILL 里未标注版本的结论，默认按 API 34 成立。

## 本机变量（先探测再取）

快照日期 2026-10-28。取值顺序：探测结果 → 下表已知值 → 常见默认。设备/端口不写死。

```
IAPP_PKG       = com.iapp.app
ADB            = E:\Program Files\platform-tools\adb.exe        # 探测不到时用这个
BUILD_TOOLS    = E:\Program Files\build-tools_r35_windows\android-15
JDK            = E:\Program Files\openjdk-25_windows-x64_bin\jdk-25\bin
PYTHON         = E:\Program Files\python3.13.17
DEVICE         = 现查：adb devices 里有 device 行的那台；2026-10-28 为 emulator-5556（API 34）
DEV_PROJECT    = 以 iApp 设置里显示的为准；当前 /storage/emulated/0/Pictures/ProjectApp/<项目ID>
                 （= Android/data/com.iapp.app/files/iApp/ProjectApp/<项目ID> 的软链目标）
DEV_PROJECT_DEFAULT = /sdcard/iApp/ProjectApp/<项目ID>           # 未改设置时的默认位置，仅供参考
SHARED_HOST    = E:\workspaces\2026-10-24-iapp-dev-ai-space\android-sync
SHARED_GUEST   = /mnt/shared/Pictures
FTP_*          = 本机未配置；需要时从 iApp「服务器控制台」现抄，填进 tools/ftp-sync.local（不入库）
```

## 设备选择（每次投递前）

**有 adb 设备时**：

1. 只有 1 台 → 直接用它
2. 有 2 台 → 默认选 **API 版本高** 的那台
3. 用户指定了 Android 版本 → 按用户要求的版本选

选定后先核版本，再投递：

```bash
adb -s <serial> shell getprop ro.build.version.sdk
```

不要写死 `emulator-5554` / `-5555`：实例序号与端口随多开顺序变化。

**没有 adb 设备、但设备侧开了 FTP 时**：

- 「设备」= iApp 界面给出的 `ftp://<设备IP>:<端口>`，每次现抄（端口会变）
- 先验：列远端根 + `SIZE <工程根>/src/mian.iyu`
- 没有 `logcat` / `screencap` / `force-stop`；探针结果必须上屏
- 宿主连不上（本机雷电 14 就是这种，网关隔离）→ 先试 `adb forward tcp:<端口> tcp:<端口>`；
  仍不通就只能请用户在设备内终端验证，**不要当成 FTP 不可用**

**两者都不可用**：停下，请用户启动模拟器或打开服务器控制台；不猜路径、不猜端口。

## 投递链路

三条通道并列，按当前环境能力选；本机主链路是共享目录。

| 通道 | 前置 | 写入 | 校验 | force-stop / logcat | 失败后 |
|---|---|---|---|---|---|
| 共享目录 | 宿主 `android-sync/` ↔ 设备 `Pictures` | 直接改宿主文件 | 核设备侧 md5 | 需另配 adb | 核不上就 `adb push` |
| adb | `adb devices` 有设备 | `adb push/pull` | `md5sum` / `wc -c` | 能 | 换共享目录 |
| FTP | 控制台已开 + 宿主可达（直连或经 adb forward） | `ftp_sync.py` | `SIZE` + `MD5` | 不能 | 修通道或换环境 |

**本机优先级（2026-10-28）**：

1. 共享目录 —— 日常改码
2. `adb push/pull` + `logcat` —— 单文件、取证、共享目录核不上
3. FTP over `adb forward` —— 共享目录不可用且有 adb（本机已验到只读；写入待验）
4. 手工导入 —— 都不通

先判断 FTP 能不能直达：`Test-NetConnection <设备IP> -Port <端口>`（不要只看 `ping`）。
能直达就直接用设备地址；不能才走 `--adb-forward`。哪天网络变了，第 3 条自动降级为最简单的直连。

**主链路（本机）**：iApp 工程根已指向 `Pictures/ProjectApp`，而 `/sdcard/Pictures` 就是 LDPlayer 共享目录：

```
宿主机 android-sync/ProjectApp/<项目ID>/  ==  /sdcard/Pictures/ProjectApp/<项目ID>/
```

1. 改文件前 `am force-stop com.iapp.app`（iApp 以内存为准）。
2. 直接改宿主机文件即等于改设备工程；**但改「已存在」文件后必须核 `/sdcard/Pictures/...` 的 md5**——
   vboxsf 直挂（`/mnt/shared/Pictures`）会立刻更新，FUSE 视图（iApp 实际读的那侧）可能仍是旧内容；
   新建文件则两侧立刻可见。不一致就 `adb push` 兜底。工程必须在 iApp 里关着。
3. 改完**不要再次 force-stop**；交给用户重新打开工程。用户负责运行并回报，Claude 不代点界面。

**adb 兜底**（共享目录不可用或核不上 md5）：

```
adb shell am force-stop $IAPP_PKG
adb push <host 文件> $DEV_PROJECT/src/<名>
adb shell chown <uid>:sdcard_rw $DEV_PROJECT/src/*; chmod 660 $DEV_PROJECT/src/*
```

- `<uid>` 用 `pm list packages -U com.iapp.app` 现查（当前 u0_a72）
- Git Bash 下先 `export MSYS_NO_PATHCONV=1`，否则 `/storage/...` 被改写成盘符路径
- **不要用 bind mount**：应用独立 mount namespace，挂载对 iApp 不可见

**FTP**（仅当 adb 与共享目录都不可用）：

```
export MSYS_NO_PATHCONV=1
# 先在 tools/ftp-sync.local 写好 host=/port=/remote=/local-root=（不入库），或命令行给全（--remote 必填）
python tools/ftp-sync.py --adb-forward emulator-5556 --dry-run
python tools/ftp-sync.py --adb-forward emulator-5556   # 退出码 0 才算投递完成
```

- 本机雷电 14 实测：宿主直连不通，必须走 `--adb-forward`（脚本自动转发每个 PASV 数据端口）
- 端口从 iApp「服务器控制台」现抄；`--adb-forward` 时 `--host` 可省（默认连 `127.0.0.1`）
- 带 `--remote`/`--port` 的完整示例见 `docs/environments/ldplayer14.md` §3（只保留一份，避免漂移）
- 主动模式不可用（实测 `425`）；直连只在宿主与设备同网段时可行

日志（有 adb 时）：`adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'`

## 目录约定

- `android-sync/` 只放 iApp 工程镜像，层级与设备一致：`android-sync/ProjectApp/<包名>/`
  - 项目 `src/` 只允许 `.iyu` 和 `.mjava`，入口必须叫 `mian.iyu`
  - 临时探针放 `android-sync/iapp-demo/<批次>/`，用完即删
  - `android-sync/cache`、`android-sync/data` 是 LDPlayer 共享目录自带，忽略
  - **镜像是手动快照，不与设备自动同步**；设备上的新增文件需 `adb pull` 刷新（`docs/scripts/refresh-mirror.sh`）
- `tools/`：本机薄包装（`ftp-sync.py`），不含实现
- `docs/` 与 `.claude/skills/` 的完整布局、免登记目录见
  `docs-architecture/references/architecture.md`；docs 索引本身在 `docs/README.md`
- 文档和代码用 `<包名>` / `<项目ID>` 占位，不写死；本机实际值只在本文件的变量区定义

## 开发取向

- **默认按 iApp 工程交付**（`.iyu` + `.mjava` + 本机投递链路）；只有用户明确说要别的介质时才例外。
- **采用标准 superpowers SDD 模式**：计划放 `docs/superpowers/plans/`、规格放 `docs/superpowers/specs/`；
  分层与索引规则见 `.claude/skills/docs-architecture/references/architecture.md` §5。
- 官方两份 txt 手册（`docs/reference/iyu-helpV3.0.txt`、`ijava-helpV3.0.txt`）不完整、偶有错别字和过时内容，
  **只作参考**，不要当权威。
- 真实开发面向**通用 Android 原生知识**（Activity/View/权限/WebView/存储等），iApp 只提供容器与调用桥。
- iyu 层尽量只写 `call` 编排和事件绑定，具体实现放进 `.mjava`。
- **控件优先在 `.iyu` 里声明自定义控件**（`type=` 完整类名 + `build.xml` 登记），短名兜底；
  mjava 只做运行期内容填充与必要修复，**不要整页动态创建**。

## 辅助技能（UI 设计）

工作区装了 `mobile-app-ui-design` 与 `material-3`，都是**辅助**技能，不并入 `iapp-development`。
两者面向原生/Compose/Web，**设计层可直接用，实现层要换成 iApp 写法**：

- **要设计新页面、改造观感、定信息架构/空状态/引导流** → 用 `mobile-app-ui-design`；
  只取它的设计流程与反模式，**不要**照搬 Tailwind / Lucide / React 那套实现说明。
- **要 M3 的配色角色、字号阶梯、圆角、elevation、组件规格、验收清单** → 用 `material-3`；
  取 token 与组件语义，**不要**照抄 Compose / Flutter / `@material/web` 代码，也不要假设 Expressive 可用。
- **写 `.iyu` / `.mjava`、控件登记、投递调试、打包** → 仍然只认 `iapp-development`，UI 技能不替代它。
- 概念到 iApp 的映射、已知限制（无 Compose、`SearchBar` 崩溃、TIL 修复、`padding` 按 px）与推荐工作流：
  见 `docs/ui-skills.md`。

## 知识沉淀（强制）

每轮探针结束必须回填，不许攒：

```
探针/实测 → docs/evidence.md（日期 + 批次 + 原始读数）
         → docs/environments/<环境>.md（长期事实：级别 + 来源 + 日期）
         → SKILL（通用结论：版本前提 + 级别）
         → 清临时探针 → 跑体检
```

- 级别升降、❓ 怎么写、去重三步：见 `.claude/skills/docs-architecture/references/evidence-and-levels.md`
  与 `maintenance.md`。
- 换环境得到的可复用经验，按「当用户处于 X、在做 Y 时，或许可以这样 Z」写进
  `references/environment-adaptation.md` 的「环境提示」表，注明「实际可用性需实测」。

## 每轮探针流程

1. 探针源码写进 `android-sync/iapp-demo/<批次>/`；`type=` 含点号时，工程首次打开后在 `build.xml` 补登记
2. 按通道投递：
   - 共享目录 / adb：force-stop → 写共享目录 → 清 logcat
   - 仅 FTP：请用户先关工程 → `ftp_sync.py` 推 → 核 SIZE/MD5（没有 logcat）
3. 用户运行并回报现象
4. 取证：有 adb 就拉 logcat + screencap；没有就让用户截图，探针结果必须上屏
5. 把日期、批次号、原始读数写进 `docs/evidence.md`
6. 提炼结论回填 SKILL / 环境档案，清掉临时探针
7. 汇报按：验了哪几条 / 一致·推翻·未知 / 回填了哪些文件 / 下一轮要用户做什么

## 导航

- 通用知识：`.claude/skills/iapp-development/SKILL.md`
- 文档规范与体检：`.claude/skills/docs-architecture/SKILL.md`
- 环境档案：`docs/environments/README.md`
- 本机事实：`docs/README.md`
