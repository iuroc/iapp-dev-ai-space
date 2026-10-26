# 16 文件管理器（实战：权限 / ListView / 匿名接口 / 长按菜单）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 目标

B8 实战验收第一例：用通用 Android 写法（不是 iApp 特供 API）做文件管理器，压测权限、文件 API、ListView 交互、对话框删除。开发模式与打包安装均跑通。

## 工程

```
<包名>/
├── .project / AndroidManifest.xml / icon.png / files/ / res/
├── src/mian.iyu      # 顶栏（路径 + 上级 + 刷新）+ ListView + 状态栏
└── src/fm.mjava      # 全部逻辑
```

`AndroidManifest.xml` 的 `<Permissions>` 里声明 `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE`。

iyu 只写控件树 + 两个 `call`（`fm.setup`、`fm.up`、`fm.reload`）和界面事件
`loading → fm.setup`、`onrequestpermissionsresult → fm.onPerm`。

## 关键写法

| 需求 | 做法 | 说明 |
|---|---|---|
| 列表点击 | mjava 里 `setOnItemClickListener` 匿名**接口** | 不依赖 iyu `clickitem` 的传参语义 |
| 列表长按 | `setOnItemLongClickListener` + `AlertDialog` | 替代不可用的 `pressmenu` |
| 删除确认 | 长按弹框，正按钮里再删 | `final` 被 BeanShell 禁用 → 目标路径存 `i.sss("fm.del")` |
| 状态 | `i.sss("fm.path")` / `i.sss("fm.names")` | 跨 call 存活 |
| 排序 | 目录在前，其余按名字 | `Collections.sort` + 匿名 `Comparator`（接口，可用） |
| 权限 | `activity.checkSelfPermission` + `requestPermissions` | 详见下节 |

## 实测读数

```
FM-start path=/storage/emulated/0
FM-perm-granted=true
FM-list /storage/emulated/0 count=16
FM-click pos=1
FM-list /storage/emulated/0/Android count=2
FM-list /data count=0
FM-up root
FM-list / count=45
FM-click pos=0
FM-file .../open/1792832533843_853125.apk size=4889870
FM-long pos=0
FM-del /sdcard/Pictures/bindtest/marker.txt ok=true
FM-list /sdcard/Pictures/bindtest count=0
```

## 结论

- 匿名**接口**里调用脚本方法（`onItemClick → fmTap(pos) → fmReload()`）**完全可用**，事件+逻辑不用挤在一个方法里
- `listFiles()` 无权限时返回 null/0 项，**不抛异常**（`/data` 就是这样），所以 UI 不会崩但要自己判断空
- `checkSelfPermission` 在开发模式直接 true：工程跑在 iApp 宿主进程里，权限是宿主的。开发模式看不到权限弹窗是正常现象
- 打包安装后同样可用（用户实测），首次启动需在系统弹窗里允许存储权限；打包版没有 ygs 日志，权限流程只能靠界面现象判断
- 长按 + `AlertDialog` 覆盖了 `pressmenu` 的缺口
