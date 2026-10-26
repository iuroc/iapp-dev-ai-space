# 版本与历史读数

所有结论都带版本前提；换版本后数字与行为都要重测。

## iApp 5.0.1013（参考版本）

| 项 | 读数 |
|---|---|
| versionName / versionCode | 5.0.1013 / 127 |
| minSdk | 21 |
| targetSdk | 37（安装包声明；运行在 API 28 上按 28 走） |
| 工程 `.project` 的 toolversion | `iApp V5.0.1013`（IDE 版本） |
| 开发模式 | `AndroidManifest.xml` 的 `<yuv>3</yuv>`（裕 3） |
| 打包 versionCode | 100000 + versionint |
| 打包 APK targetSdk | 实测 36（与安装包声明 37 不同，以产物为准） |

## 各批次实测定稿（2026-10）

- B0 入口 `src/mian.iyu`；iApp 工程在设备 `iApp/ProjectApp/<项目ID>`（本机后来改到共享目录）
- B1 `activity` 与 `i` 默认可用；`i.gvs(id)` 与 `findViewById(id)` 同一实例；模块级变量不跨 call
- B2 BeanShell 限制：`final` / 具名 class / `0xFF000000` / 可变参数 / `bsh.*` 全部让模块失效；匿名**类**中断事件，匿名**接口**在 API 28 可用
- B3 `textsize` 是 sp、`padding` 是 px；`st_` 桥可用但 `20sp` 不行；行尾注释会中断事件
- B4 `i` = `Aid_javaCode`；`i.d` 每次 call 新建；`i.sss` 跨 call、跨运行重置；`i.ss` 默认 NPE
- B5 `i.d.f("x.mjava")` 导入当前解释器；外部库走 D8 + `apk/assets` + `DexClassLoader`
- B6 静态：`ss_dim` 是静态 HashMap；`qm.n` 是 HashMap；打包后 `VisualDesigner` 被裁
- B7 `.iApp` 顶层无包名目录；打包后无日志；`files/` 不进 APK，`apk/assets/` 进

## 已知会随版本变化的

- `i` 的方法数（本版 390 个公开方法 / 12 字段）
- 接口的 default 方法（决定匿名实现能否用）
- 打包产物的 targetSdk / versionCode 规则
