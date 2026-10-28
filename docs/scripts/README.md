# 本机脚本索引

`docs/scripts/` 放**本机**脚本：只用在这台机器上的探测、投递与分析工具。
通用的 iApp 脚本在 `.claude/skills/iapp-development/scripts/`，两边**同名副本会各自漂移**，
下表标了「同 / 异 / 独有」，改的时候注意改哪一份。

| 脚本 | 用途 | 与 skill 同名副本 |
|---|---|---|
| `detect_env.py` | 只读环境探测：宿主 / 模拟器 / adb 设备 / 共享目录 / 可选 FTP；支持 `--json`、`--ftp`、`--mirror-root`、`--adb` | 独有（仅本机） |
| `deploy.sh` | 把宿主 `src` 推到设备工程（本机投递脚本） | 独有 |
| `refresh-mirror.sh` | 把设备上的工程快照拉回宿主镜像（设备 → 主机单向覆盖） | 独有 |
| `ensure-dual-adb.ps1` | 让两套雷电停在不同的宿主 adb 端口（实例改名 / 端口转发） | 独有 |
| `fetch_text.py` | 把已下载到本地的 HTML 转成纯文本并取片段（离线） | 独有 |
| `make_icon.py` | 离线生成 iApp 工程图标（纯标准库，不联网） | 异（本机版含本地路径示例） |
| `build_class_dex.py` | 把 Java 源码编译成 iApp 可加载的 dex | 异 |
| `build_sora_dex.py` | 把 sora-editor 的 AAR 转成 dex + 资源 apk | 异 |
| `dex_common.py` | dexdump 输出解析工具（被其它脚本 import） | 异 |
| `class_methods.py` | 列出 APK/DEX 里某类自己声明的方法 | 异 |
| `material_scan.py` | 扫描 Material 类是否有可用构造器 | 同 |
| `dex_classes.py` | 列出类与成员数量 | 同 |
| `dex_api_dump.py` | 导出类的公开 API | 同 |
| `dex_body.py` | 打印方法的字节码与可读字符串 | 同 |
| `dex_map_fields.py` | 按字段名反查类，辅助辨认混淆类 | 同 |
| `create_project.py` | 新建一个最小 iApp 工程 | 同 |

## 说明

- 「同」= 与 `.claude/skills/iapp-development/scripts/` 下同名文件内容一致；「异」= 内容已分叉，
  改动时需要决定改哪一份或同步两边。
- `detect_env.py` 的退出码：`0` 有可用通道 / `1` 无可用通道 / `2` 参数错误 / `3` 内部异常。
- 二进制产物与外部材料不在此列，见 `docs/artifacts/`。
