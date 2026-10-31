# iApp 开发工作区（本机）

## 这个工作区是做什么的

在 Windows 宿主机上开发、调试、打包 iApp（Android 可视化 IDE，显示名“测兆编程”）工程：
源码是 `.iyu` 界面 + `.mjava` 模块（只做裕语言 + mjava，不涉及 ijava/ilua/mlua），
产物是 iApp 工程和可安装 APK；工程经**当前环境可用的通道**投递到模拟器/设备（雷电 14 主用），
用户在设备上运行并回报。通用知识放 skill（可独立分享），本机事实放 docs。

## 文档分层（要点）

完整规范在 `.claude/skills/docs-architecture/`（含只读体检脚本），这里只留每轮都要用的几条：

1. 换台机器仍成立 → SKILL；只对本机 → 本文件；读数/快照 → `docs/`。
2. 一条结论只放一个主文件，别处只写一行指针（主文件查表见 `.claude/skills/docs-architecture/references/architecture.md`）。
3. 每条结论带级别 + 来源 + 日期；他机读数最高 ⚠；标 ❓ 必须写「怎么验」。
4. 先证据后结论：原始读数先进当月账本 `docs/archive/evidence-<YYYY-MM>.md`，
   `docs/evidence.md` 只留「批次 → 一句结论 → 主文件」的索引，提炼后再往上搬。
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
DEV_PROJECT    = 以 iApp 设置里显示的为准；2026-10-30 起是 iApp 默认路径
                 /sdcard/Android/data/com.iapp.app/files/iApp/ProjectApp/<项目ID>
SHARED_*       = 2026-10-30 起不再使用共享目录：宿主 android-sync/ 已移除，
                 设备侧 /sdcard/Pictures/ProjectApp 已删；不要再往这两个位置放工程
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

**本机主链路是 adb**（2026-10-30 起；共享目录同日起停用）。两条通道，按环境能力选：

| 通道 | 前置 | 写入 | 校验 | force-stop / logcat |
|---|---|---|---|---|
| adb（主） | `adb devices` 有设备 | `tools/push.py` / `adb push` | push 退出码 | 能 |
| FTP（备） | 控制台已开 + 宿主可达（直连或经 adb forward） | `ftp_sync.py` | 脚本退出码 + MD5 | 不能 |

只有 adb 不可用、或设备侧只暴露了 FTP 时才走 FTP。

**主链路**：源在 `project/<项目ID>/`（各自 git 仓库），设备侧只是副本，
用 `tools/push.py` **整目录覆盖推送**到 iApp 的工程根：

```bash
export MSYS_NO_PATHCONV=1
python tools/push.py <项目ID> [--serial <serial>]
```

- 默认先清远端 `src/ res/ files/` 的内容，再全量推；**不用增量**：`--sync` 从不删远端文件，
  本地删掉/改名的 `.mjava` 会残留并被 iApp 加载，而这种残留在「不读设备副本」的流程里发现不了
- 不读回设备内容、不做 md5/size 比对；只认命令退出码，验收靠实跑 + `logcat` + 用户反馈
- 推之前工程要在 iApp 里关着；推完**不要**代为运行，交给用户打开并回报
- 远端这几个目录删不掉（`Text file busy`），所以脚本删的是**目录内容**
- 目标目录不存在时脚本会先 `adb shell mkdir -p`：让 `adb push` 自己去建，
  在 `/sdcard/Android/data/<pkg>/` 下会报 `remote secure_mkdirs failed: Operation not permitted`（2026-10-30 实测）
- 清理后会再把本地 `src/ res/ files/` 下的每个子目录在远端 `mkdir -p` 出来；
  `adb push` 不建多级目录，`res/web/index.html` 这类嵌套资源否则会整批失败（2026-10-31 实测）
- 工程根不在默认位置时用 `--root <dir>` 覆盖，不要改脚本里的默认值

**共享目录已停用（2026-10-30）**：`android-sync/` 已从宿主移除，设备侧 `/sdcard/Pictures/ProjectApp`
也一并删除。历史教训留在 `docs/evidence.md` SYNC-2 / SYNC-3：那条链路里源与副本是同一批字节，
且 FUSE 层会让设备长期读到旧内容。**不要把工程再放回共享目录**。

**FTP**（没有 adb 时的备选）：

```
export MSYS_NO_PATHCONV=1
# 先在 tools/ftp-sync.local 写好 host=/port=/remote=/local-root=（不入库），或命令行给全（--remote 必填）
python tools/ftp-sync.py --adb-forward <serial> --port <端口> \
  --remote /ProjectApp/<项目ID> --local-root project/<项目ID>
```

- 设备 IP 与端口每次从 iApp「服务器控制台」现抄，不写死；杀掉 iApp 后要手动重开控制台
- 本机宿主直连不通，必须走 `--adb-forward`（脚本自动转发每个 PASV 数据端口）
- 要同步删除就带 `--delete-extras --managed-dirs src,res,files`
- 完整示例见 `docs/environments/ldplayer14.md` §3（只保留一份，避免漂移）

日志（有 adb 时）：`adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'`

## 目录约定

- **`project/<包名>/` 是工程源目录**：各自独立 git 仓库，工作区 `.gitignore` 忽略 `/project/`
  - 改代码、提交、写文档都只在这里做；工程可能随时独立成库，引用一律写工程根相对路径
  - 项目 `src/` 只允许 `.iyu` 和 `.mjava`，入口必须叫 `mian.iyu`
  - **工程自带的文档只有两块**：`<工程根>/openspec/`（它自己的 OpenSpec 根）与 `<工程根>/docs/`
    （私有资料区 + `superpowers/plans|specs/`）；**项目不搭 AI 工作区**（不放 `.claude/`、不放 skill 副本）。
    判据、归属与布局见 `.claude/skills/docs-architecture/references/architecture.md` §1/§5
- `android-sync/` **已移除**（2026-10-30）：原来是 LDPlayer 共享目录的宿主侧。不要再建，
  也不要把「宿主目录 ↔ 设备目录」当成同一批字节来用，历史教训见 `docs/evidence.md` SYNC-2 / SYNC-3
- `tools/`：本机薄包装（`push.py` 整目录推送、`ftp-sync.py` FTP 通道），不含实现
- `docs/` 与 `.claude/skills/` 的完整布局、免登记目录见
  `.claude/skills/docs-architecture/references/architecture.md`；docs 索引本身在 `docs/README.md`
- 文档和代码用 `<包名>` / `<项目ID>` 占位，不写死；本机实际值只在本文件的变量区定义

## git 约定

- **提交时机**：改完一个小环节、验收通过就提交，粒度要碎，方便回退到节点与溯源。不攒批量。
- **提交信息**：`<type>: <message>`，单行中文，type 取 `feat` / `fix` / `refactor` / `test` / `docs` / `chore`。
- **新建工程**：`project/<包名>/` 一律带 `--git`（init + `.gitignore` + 首次提交）；
  一次性探针工程不 init，也不要放进 `project/`（见 §每轮探针流程）。`.gitignore` 模板见
  `.claude/skills/iapp-development/references/project-structure.md` §工程自带 git 仓库。
- **单分支**：不做分支模型，靠 commit 回退。
- **不推送远程**：远程很可能是镜像地址（如 `ghproxy`），push 会失败；只管本地仓库，
  不要 `push`、不要加 remote。
- 产物 `bin/<包名>.apk` 不入库；要留档就在 `docs/` 记读数，不提交 APK 本身。

## 开发取向

- **默认按 iApp 工程交付**（`.iyu` + `.mjava` + 本机投递链路）；只有用户明确说要别的介质时才例外。
- **手表应用不默认走 iApp**：iApp 的手表支持是**实验性**的，中高端表上页面跳转与代码解释
  卡顿 1~3 s；正式手表应用建议走官方方案，用户明确要用 iApp 做表时再走 iApp 路线。
  边界与原因见 `.claude/skills/iapp-development/references/watch-app-guide.md` §0。
- **采用标准 superpowers SDD 模式**：计划放 `plans/`、规格放 `specs/`；
  **单个工程的任务放该工程 `<工程根>/docs/superpowers/`，跨工程任务才放工作区 `docs/superpowers/`**；
  分层与索引规则见 `.claude/skills/docs-architecture/references/architecture.md` §5。
- 官方两份 txt 手册（`docs/reference/iyu-helpV3.0.txt`、`ijava-helpV3.0.txt`）不完整、偶有错别字和过时内容，
  **只作参考**，不要当权威。
- 真实开发面向**通用 Android 原生知识**（Activity/View/权限/WebView/存储等），iApp 只提供容器与调用桥。
- iyu 层尽量只写 `call` 编排和事件绑定，具体实现放进 `.mjava`。
- **界面默认 mjava 建树**：`.iyu` 只留一个根容器 + `<UIEventset>`，子控件、样式、监听器都在 mjava 里写，
  组件库 vendor 一份 `src/ui.mjava` 进工程。详见下面「UI 构建范式」。

## 改动文件的方式（强制）

改源码、配置、文档一律用编辑器级工具：`Write` 整写，或 `Edit` 精确替换（先用 `Read` 读出目标区间再改）。

- **不用 `python -c` / `python - <<EOF` / `sed -i` 做批量字符串替换。** 改动不透明，用户看不到 diff，
  也失去「改了哪行、改成什么」的自证；`project/` 下的 `.mjava`、`.iyu` 是交付物，更不能这样改。
- 例外只留给工具处理不了的场景（二进制文件、真正的大规模改名）；用了就要 `git diff` 逐段核对，
  并在汇报里说明为什么走例外。
- 只读校验脚本（`check_mjava.py`、`review_docs.py`、`check_portable.py`）不受这条限制。

## 展示 Demo 批次（`com.showcase.*`）

2026-10-30 起，展示向 UI Demo 单独成批，包名统一为 **`com.showcase.<slug>`**（三段，
slug 取风格英文、全小写、不要连字符），与旧的 `com.demo.*` 探针工程区分开：

- 工程目录就是包名：`project/com.showcase.<slug>/`（源目录，自带 git；推送目标由 `tools/push.py` 决定）
- 打包产物 `bin/com.showcase.<slug>.apk`；包名互不相同，装同一台设备不会互相覆盖，可并排对比
- 每个方向一个 slug，slug 与已建状态写在案例标题里，见 `docs/ui-showcase-prompts.md` §4
- 新方向沿用同一格式；**不要**把展示 Demo 塞进 `com.demo.*`，也不要给同一方向起第二个名字

## UI 构建范式（mjava 建树）

2026-10-30 起，本工作区出产的工程默认按这套写（实测见 `docs/evidence.md` §UIPROBE-1 / UIPROBE-2）：

- `.iyu` 只放一个全屏根 `FrameLayout`（`id=1`）与 `<UIEventset>` 四个事件；不声明子控件、
  不写每控件的 `<event>` 块
- 视图、样式、监听器全部在 mjava 里建；尺寸取 `DisplayMetrics`（`loading` 阶段视图宽高是 0）
- 构建拆成「骨架段 / 内容段 / 效果段」，每段独立入口 + `postDelayed` 串接：一段出错只毁一段
- 组件 = 返回 View 的工厂函数 + `ui_tag` 命名句柄（不能继承 View，这是本环境的天花板）
- 系统栏 / 键盘 / 手势：安全区一律读 insets 与根偏移的**差值**，禁止 dp 常量；背景由根自己画

通用知识在 `.claude/skills/iapp-development/`：
`.claude/skills/iapp-development/references/ui-kit.md`（函数清单与限制）、
`.claude/skills/iapp-development/references/style-guide.md`（骨架与样式分层）、
`.claude/skills/iapp-development/assets/ui-kit/ui.mjava`（权威副本，新工程复制进 `src/`）。

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
探针/实测 → docs/archive/evidence-<YYYY-MM>.md（日期 + 批次 + 原始读数；当月可续写，跨月冻结）
         → docs/evidence.md（同一批次加一行索引：一句结论 + 主文件 + 状态）
         → docs/environments/<环境>.md（长期事实：级别 + 来源 + 日期）
         → SKILL（通用结论：版本前提 + 级别）
         → 清临时探针 → 跑体检
```

- 级别升降、❓ 怎么写、去重三步：见 `.claude/skills/docs-architecture/references/evidence-and-levels.md`
  与 `maintenance.md`。
- **开发途中撞见已有文档本身有错，当轮提出并修**，不要在心里绕过：结论过时、路径失效、
  放错层、与新实测冲突，都算。修完同样跑体检；改的是「已有事实」而不是新增读数时，
  在 `docs/evidence.md` 留一条决策/更正条目，写清旧说法与新说法。
- 换环境得到的可复用经验，按「当用户处于 X、在做 Y 时，或许可以这样 Z」写进
  `.claude/skills/iapp-development/references/environment-adaptation.md` 的「环境提示」表，注明「实际可用性需实测」。

## 每轮探针流程

1. 探针工程建在宿主临时目录（不入库、不 init git、不放 `project/`），`adb push` 推到设备工程根下；
   `type=` 含点号时，工程首次打开后在 `build.xml` 补登记。用完**两侧都删**
2. 按通道投递（源在 `project/<包ID>/`）：
   - 有 adb：`python tools/push.py <包ID>` 整目录覆盖推送，再清 logcat
   - 没有 adb：请用户先关工程 → `tools/ftp-sync.py` 推（退出码 0 即完成；没有 logcat）
   - 不核设备侧内容；推完交给用户
3. 用户运行并回报现象
4. 取证：有 adb 就拉 logcat + screencap；没有就让用户截图，探针结果必须上屏
5. 把日期、批次号、原始读数写进当月的 `docs/archive/evidence-<YYYY-MM>.md`，并在
   `docs/evidence.md` 加一行批次索引
6. 提炼结论回填 SKILL / 环境档案，清掉临时探针
7. 汇报按：验了哪几条 / 一致·推翻·未知 / 回填了哪些文件 / 下一轮要用户做什么

## 导航

- 通用知识：`.claude/skills/iapp-development/SKILL.md`
- 歌德借阅机内容 API（跨平台，与 iApp 无关）：`.claude/skills/gede-read-api/SKILL.md`
- 文档规范与体检：`.claude/skills/docs-architecture/SKILL.md`
- 工程质量审阅（复用缺失 / 样式一致性 / 重复代码 / 技术债）：`.claude/skills/app-quality-review/SKILL.md`
- 环境档案：`docs/environments/README.md`
- 本机事实：`docs/README.md`
- 工作区索引（不写规则，只做入口）：`README.md`
