# 10 波纹与 MD 风格

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 页面

`ScrollView(1) → LinearLayout(100)`，每项上方一行小字说明 id。
包含：权重行、mjava alpha、原生/带色按钮、四种波纹、MD 输入框、MD 按钮、minheight/elevation 测试。

## 读数

```
D1b-styles-ok dp8=24 dp24=72
D1b-report click7=false click8=true click9=true | bg7=RippleDrawable | bg10=RippleDrawable
           | bg11=GradientDrawable | alpha4=0.5 | minheight13=120 elevation13=12.0
D1b-heights h3=129 h11=129 h13=129
```

## 结论

| 项 | 结果 |
|---|---|
| `clickable=true`（ppt） | ✅ 生效；Ripple 必须依赖它 |
| `minheight=40dp` | ✅ 120px（dp→px） |
| `elevation=4dp` | ✅ 12.0（dp→px） |
| `alpha` 的 mjava 补差 | ✅ 0.5 |
| RippleDrawable 四种宿主 | ✅ TextView / LinearLayout / Button 均可，前提 clickable |
| Button + ppt `backgroundcolor` | 覆盖原生背景 → 原生波纹丢失 |
| MD 输入框焦点描边 | ✅ 灰→蓝 |
| `post()` 后取高度 | ✅ 非 0（载入事件里是 0） |

## 回填

`references/iyu-guide.md`、`references/style-guide.md`（波纹与 MD 小节）。
