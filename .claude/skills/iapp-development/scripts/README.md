# 随包脚本

这些是**可选**的辅助脚本，不是使用本技能的前提。主知识在 `references/`；脚本只负责重复性劳动。

| 脚本 | 用途 |
|---|---|
| `make_icon.py` | 离线生成 512×512 工程图标（纯标准库） |
| `create_project.py` | 新建最小 iApp 工程（默认调用 `make_icon.py`） |
| `material_scan.py` | 扫 iApp APK 里哪些 Material 类有 `(Context)` 构造 |
| `class_methods.py` | 列某个类自己声明的方法（核对 API 是否被裁剪） |
| `dex_common.py` | dexdump 输出解析工具（被其它 `dex_*` 脚本 import，也可单独运行） |
| `dex_classes.py` / `dex_api_dump.py` / `dex_body.py` / `dex_map_fields.py` | dexdump 分析小工具 |
| `build_class_dex.py` | 把 Java 源码编译成 iApp 可加载的 dex（继承类的场景） |
| `build_sora_dex.py` | 把 sora-editor AAR 转成 dex + 资源 apk |
| `build_aar_dex.py` | 通用版：多 AAR + 依赖资源 + 补桩 → dex + 资源 apk（XUI 1.1.9 实测） |
| `ftp_sync.py` | 通过 iApp 内置 FTP 全量推/拉工程（SIZE+MD5 双校验，纯标准库） |
| `check_mjava.py` | 投递前扫 `.mjava`：找出「解析失败 → 整个模块不加载」的写法 |
| `check_portable.py` | 分享前自检：禁止外部路径与作者机器路径 |

## 环境

- Python 3.10+
- `dexdump`：默认从 `PATH` 找；Android SDK 的 build-tools 目录里自带，也可设 `DEXDUMP=<dexdump 完整路径>`
- Android build-tools：`aapt2` / `d8` 默认从 `PATH` 找；也可设 `BUILD_TOOLS=<build-tools 目录>`
- JDK：`javac` 默认从 `PATH` 找；也可设 `JDK_BIN=<jdk bin 目录>`

```bash
# 例：Windows（Android Studio 默认 SDK + Oracle JDK 常见路径；版本号按实际替换）
set BUILD_TOOLS=%LOCALAPPDATA%\Android\Sdk\build-tools\35.0.0
set JDK_BIN=C:\Program Files\Java\jdk-21\bin
set DEXDUMP=%BUILD_TOOLS%\dexdump.exe

# 例：类 Unix
export BUILD_TOOLS=$HOME/Android/Sdk/build-tools/35.0.0
export JDK_BIN=/usr/lib/jvm/java-21-openjdk/bin
export DEXDUMP=$BUILD_TOOLS/dexdump
```

## 用法示例

```bash
# 图标
python scripts/make_icon.py --project-dir <宿主工程目录>/<项目ID>
python scripts/make_icon.py --all <宿主工程目录>

# 新建工程
python scripts/create_project.py --root <宿主工程目录> --package com.example.demo --title 演示

# 扫 APK
python scripts/material_scan.py <你的 iApp APK>
python scripts/class_methods.py <你的 iApp APK> com/google/android/material/slider/

# 编译类进 dex
python scripts/build_class_dex.py --src <java 源码目录> --out <输出.dex> --lib <android.jar>

# 经 iApp 内置 FTP 投递（先 `export MSYS_NO_PATHCONV=1`，否则 /ProjectApp 会被改写）
python scripts/ftp_sync.py --host <设备IP> --port <端口> --remote /ProjectApp/<项目ID> \
  --local-root <宿主工程目录> --dry-run

# 宿主到设备网络不通、但有 adb：自动转发控制端口与每个 PASV 数据端口
python scripts/ftp_sync.py --adb-forward <serial> --port <端口> \
  --remote /ProjectApp/<项目ID> --local-root <宿主工程目录> --dry-run
```

## `ftp_sync.py` 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--host` | 无 | 设备 IP；给 `--adb-forward` 时可省略（连 `127.0.0.1`） |
| `--port` | `21` | FTP 端口，按 iApp 界面填 |
| `--remote` | 必填 | 远端工程根，必须以 `/` 开头 |
| `--local-root` | 当前目录 | 宿主工程目录 |
| `--adb-forward` | 无 | 传 adb 序列号：自动转发控制端口与每个 PASV 数据端口 |
| `--adb` | PATH 里的 adb | adb 可执行文件 |
| `--user` / `--password-env` | `anonymous` / `FTP_PASSWORD` | 密码只从环境变量或交互读取，不走命令行 |
| `--exclude` | `.git,.claude,__pycache__,.idea,.vscode` | 按目录/文件名排除，逗号分隔 |
| `--managed-dirs` | `src,sdk` | 只有这些顶层目录内的多余文件会被 `--delete-extras` 删 |
| `--delete-extras` | 关 | **默认完全不删远端文件**；开启后也只作用于 `--managed-dirs` |
| `--pull` | 关 | 反方向：设备 → 宿主 |
| `--dry-run` | 关 | 只读预演，不写远端 |
| `--no-verify` | 关 | 跳过 SIZE/MD5 校验（不推荐） |
| `--tls` | 关 | 显式 FTPS；服务器不支持时直接失败，**不回退明文** |
| `--timeout` | `20` | 连接/单操作超时秒数 |

## 分享前自检

```bash
python scripts/check_portable.py
```

零命中才适合把整个目录拷给别的 workspace。
