# 12 MD 表单组件矩阵（mdform.iyu）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 页面

独立 `.iyu`（不占用 `mian.iyu`），ppt 放占位 LinearLayout，组件全部 mjava 动态创建：

- 110/111/112：outline / filled / none
- 113：自定义描边色、圆角、字数上限
- 114：密码显隐
- 120：MaterialButton 4 种
- 121：CheckBox / RadioButton / Switch
- 122：Chip 3 种
- 123：Slider + 圆形/线性进度
- 124：Context × setSingleLine 矩阵

## 读数

```
MDF til-ok / btn-ok / select-ok / chip-ok / progress-ok / matrix-ok
110 mode=2 | 111 mode=1 | 112 mode=0 | 113 mode=2 | 114 mode=2
124-0 ctxCls=com.iapp.app.run.mian (ctxIsAct=true)
124-1 ctxCls=com.iapp.app.run.mian
124-2 ctxCls=androidx.appcompat.view.ContextThemeWrapper
124-3 ctxCls=androidx.appcompat.view.ContextThemeWrapper
tilCtxCls 一律 ContextThemeWrapper
120 n=4  121 n=3  122 n=3  123 n=3
```

## 结论

- 三种 box 模式都可设置并回读（2/1/0）
- `TextInputEditText` 的 Context 决定它是否继承 Material 主题覆盖：用 activity → 原生下划线；用 `til.getContext()` → outline
- `setSingleLine` 不影响外观（A vs B 一致）
- 按钮、选择控件、Chip、Slider、进度条全部可动态创建

## 坑

- BeanShell 里 `TextInputEditText.isSingleLine()` 解析失败（`Method isSingleLine() not found`），会让整个方法中断；读状态时换别的属性
- 自定义组件不要进 ppt（影子实例），见 `cases/11`
