# 04 IYU 属性层（B3）

日期：2026-10-24　环境：Android 9 (API 28)　iApp 5.0.1013

## 读数（logcat）

```
B3-order=9,3,5
B3-density=3.0 scaled=3.0
B3-pad12=12
B3-size24=72.0
B3-st20=60.0
B3-st20sp=42.0
B3-def=42.0
B3-colorDec=16711680
B3-colorHex=-11975345
B3-alpha=128.0
B3-spaceEq=42.0
B3-unknown=true
B3-usSt=42.0
B3-def2=42.0
---
B3-colorDef=-11975345
B3-colorHex2=-11975345
B3-alphaDef=1.0
B3-alpha128=128.0
B3b-sA=1
B3b-sB-null=true
```

## 一致 / 推翻 / 未知

| 断言 | 判定 | 证据 |
|---|---|---|
| 兄弟按文件顺序，不按 id | ✅ 一致 | 9,3,5 |
| `textsize=24` 是 sp | ✅ 一致 | 72.0 = 24×3 |
| `padding=12` 是 px | ✅ 一致 | 12 |
| `st_setTextSize=20` 生效 | ✅ 一致 | 60.0 |
| `st_setTextSize=20sp` 不生效 | ✅ 一致 | 42.0 = 默认 |
| `st_setTextColor` 只认十进制 | ✅ 一致 | 十进制 16711680 生效；`#ff0000` 读回默认 -11975345 |
| `st_setAlpha` 生效 | ⚠ 部分 | 读回 128.0（默认 1.0），值原样落地、无 clamp |
| `=` 两边空格整行失效 | ✅ 一致 | 42.0 = 默认 |
| 未知键静默忽略 | ✅（无报错）；是否"忽略"只能说不生效 | `unknown=true` |
| `us` 不认 `st_` | ✅ 一致 | 42.0 |
| 注释独占行 | ✅ 一致 | 独占行正常；行尾注释 `YuErr` 并中断事件 |
| `\n` 劈开源码 | ❌ 推翻 | `syso("A\nB")` 输出两行，后续正常 |
| 参数个数必须一致 | ❌ 部分推翻 | `syso("x","y")` 不报错，只输出 `x` |

## 备注

- density 与 scaledDensity 都为 3.0，是判读 sp/px 的锚点，换设备必须重取。
- `st_setAlpha=128` 的 128.0 不符合 `View.setAlpha(float)` 的 0..1 契约，疑似 iApp 直接写字段而非调 setAlpha；未做进一步验证。
