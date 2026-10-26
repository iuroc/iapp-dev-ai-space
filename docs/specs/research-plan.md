# iApp 研究复现任务书（存档）

## 身份与目标

iApp 是 Android 上的可视化 IDE（显示名 测兆编程，包名 com.iapp.app），闭源、公开资料少且不可靠。目标不是做业务，而是用探针把运行时行为一条条测清楚，沉淀成自足知识库，最终能独立开发、调试、交付 iApp 工程。

## 铁律

1. 先探针后开发；不确定就写探针页
2. 双证据：屏幕现象 + adb logcat 原文；控制台行号不可信
   `adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'`
3. 结论分级 ✅实测 / ⚠推测 / ❓未知；null/false/0 必须设锚点
4. 跨运行比较用追加模式账本；读对象前先问「读它会不会动它」
5. iApp 编辑器以内存为准：外部改源码前先关闭工程，改完重开再运行
6. 入口必须叫 mian.iyu；src/ 只放 .iyu 和 .mjava；UTF-8 + LF
7. 一页只问一件事，但一轮可写多页
8. 文档只引用包内文件；不写死包名和本机路径；通用结论进 SKILL，本机事实进 docs

## 批次

### B0 环境基线
- 建立投递链路；记录 adb、iApp 版本、Android 版本
- 最小页：mian.iyu（LinearLayout + TextView）+ app.mjava，载入事件 `call(a,"mjava","app.bind")`
- 预期：显示 Hello from mjava，日志有 ok

### B1 工程与调用模型
- 工程结构、did 控件树、call 传参与返回值、activity 与 i 两个默认变量
- 预期：findViewById 与 i.gvs 同一实例；裸 findViewById 报 Command not found；模块级变量跨 call 必丢

### B2 mjava 铁律
- `{...}` 数组、形参 final、具名类、0xFF000000、可变参数、bsh.*、匿名类、接口默认方法、循环变量叫 i
- 预期：前 6 条让模块失效；匿名类报 can't load this type of class file；循环变量 i 闪退
- 接口默认方法按目标 API 判断；Android 14 的 OnLongClickListener 有 default，API 28 没有

### B3 IYU 语法与属性层
- 注释独占行；字符串 \n；短指令参数个数；变量写法；did 与兄弟顺序；ppt 两层
- 预期：textsize=24 是 sp、padding=12 是 px；st_setTextSize=20 生效、20sp 不生效；st_setTextColor 只认十进制；st_setAlpha 生效；us 不认 st_；= 两边空格整行失效；未知键静默忽略

### B4 状态与 i 对象
- i.sss / i.ss / i.dim 存哪、活多久；i.d 是什么；5 轮账本；APK 静态印证
- 预期：i.sss 是静态 HashMap 同进程跨运行保留；i.ss 读 Aid_javaCode.ss_dim，一用 NPE；i.dim 按 key 前缀分派；i.d 是当前模块的 BeanShell 解释器；i.sss 不是磁盘持久化

### B5 模块化与外部库
- 对比 `i.call(a,"mjava","b.method",...)` 与 `i.d.f("b.mjava")`
- 预期：i.call 每次新建解释器（约 11ms/次），异常吞成 JavaErr + null；i.d.f 是真 import（约 0.1ms/次），共享 activity/i/命名控件，同名方法覆盖，异常原样传播；i.d 可存进 i.sss 跨 call 存活；重复 f 会重跑模块顶层
- 外部库：JAR / AAR / DEX 三条路；aapt2 + d8 生成 dex；plugin view 的 dex 放 apk/assets

### B6 静态分析与版本
- adb pull APK，写 dex_classes / dex_api_dump / dex_body / dex_map_fields 脚本
- 预期：i 对象约 381 方法 / 226 名字 / 12 字段；确认 qm.n 与 Aid_javaCode.ss_dim
- .project 的 toolversion 是 IDE 版本，开发模式在 AndroidManifest 的 <yuv>
- 数字只对参考 APK 成立；targetSdk 37 在 Android 9 可安装，运行时按 API 28

### B7 交付与打包边界
- 验 .iApp 备份包结构（顶层没有包名目录）、生成与导入；同包名必须先删旧工程
- 预期：versionCode = 100000 + versionint；<sdk> 只改 platformBuildVersionName，打包后 minSdk 仍是 21
- 默认交付 .iApp；只有用户点名 APK 才由用户在 iApp 内手动打包

### B8 实战验收（选做）
- 文件管理器 → 浏览器 → 2048 → 代码编辑器 → 下拉选择器，各补 case
- 文件管理器：Android 9 用 WRITE_EXTERNAL_STORAGE 运行时权限；不要用 MANAGE_EXTERNAL_STORAGE / Environment.isExternalStorageManager
- 浏览器：先读 WebView UA / 内核版本再定写法

## 汇报格式

1. 本轮验了哪几条 + 原始读数（logcat 摘要）
2. 一致 / 推翻 / 仍未知及证据
3. 回填了哪些文件
4. 下一批需要用户做什么（一次说清）

## 停止条件

B0–B7 的 ✔ 项都有实机读数，做不到的标 ❓ 并写「缺什么才能验」。禁止把推测写成实测。
