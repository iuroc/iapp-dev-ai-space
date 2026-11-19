# 调试与失败签名

## 取日志

```
adb logcat -d -v time 'ygs:V' 'System.err:V' '*:S'
```

mjava 里的 `i.syso(...)` 输出在 tag `ygs`；iApp 内部报错同时进 `ygs` 与 `System.err`。

## 三种错误前缀（✅ 实测 iApp 5.0.1013 / Android 9）

| 前缀 | 来自 | 影响范围 | 例子 |
|---|---|---|---|
| `MJavaErr` | mjava 模块解析/加载期 | **只废掉该模块**，后续语句继续 | `Parse error at line 1, column 17. Encountered: final` |
| `JavaErr` | 模块求值期 | 只废掉该次 call，后续继续 | `Command not found: findViewById( int )` |
| `YuErr` | 裕语言侧，会**中断整个载入事件** | 本次事件余下语句不执行 | 匿名类模块调用后出现，`第N行` 指向 call 行 |

判断方法：看报错后有没有下一条 `i.syso` 输出。

## 原文样例

解析错误（final 形参）：

```
MJavaErr：
Parse error at line 1, column 17.  Encountered: final
```

类加载错误（具名类 / 匿名类）：

```
MJavaErr：
Sourced file: inline evaluation of: ``class Foo { ... }`` unknown error:
can't load this type of class file : at Line: 1 : ...
```

求值错误（裸 findViewById）：

```
JavaErr：
Typed variable declaration : Command not found: findViewById( int ) : at Line: 4 : in file:
inline evaluation of: ``...`` : findViewById ( 2 )
Called from method: bare : at Line: -1 : in file: <Called from Java Code> : <Compiled Java Code>
```

## 规律

- 所有 mjava 错误文本里都有 `inline evaluation of` —— 执行器是 **BeanShell**
- 模块解析失败是「全有或全无」：一个方法写坏，整个模块的方法都不可用
- 解析期错误（`MJavaErr`）发生在模块加载前，模块里的 `try/catch` 还没机会执行，**兜不住**；能兜的是方法体内的运行期 Java 异常
- 影响范围是模块级：该模块所有方法都不可用；其它模块和已加载模块不受影响，后续语句继续；如果随后调用该模块的方法，会再触发 `JavaErr`（`Command not found`），中断本次 call
- 行号只在 `at Line: N` 里对模块文件有效；iApp 弹窗里的「mian.iyu 第 N 行」不可靠

### 正则/转义写错：模块整体 Token Parsing Error

```
MJavaErr: Token Parsing Error: Lexical error at line 215, column 50.
Encountered: "s" (115), after : "\"detailUrl:\\"
```

Java 字符串里 `\s` 才是正则的 `\s`；写成单反斜杠 `"detailUrl:\s"` 不是合法转义，
BeanShell 直接判整个模块不可用（不是只坏一行）。日志里的行号可信，按行号改。

## 投屏预览与实时调试（scrcpy）

真机 / 模拟器实时看界面时用 scrcpy。**默认 8 Mbps 对 1080p 以上的文字界面不够**，
典型症状是文字边缘发糊、浅色大面积底色出现色带/色彩断层——先加码率，不要先怀疑性能或分辨率。

**码率口径**：按 bpp（bits per pixel per frame）= 码率 ÷ (宽 × 高 × fps)。
1080×2340@60 约 1.52 亿像素/秒：8 Mbps ≈ 0.05 bpp（糊）、25 Mbps ≈ 0.17 bpp（可用）、
50 Mbps ≈ 0.33 bpp（文字锐利、渐变干净）。屏幕文字是高频内容，0.2~0.4 bpp 是常用区间。

| 档位 | 参数 | 适用 |
|---|---|---|
| 默认 | `--video-bit-rate=50M`（H.264 / 60 fps） | 日常调试、阅读类界面 |
| 轻量 | `--video-bit-rate=25M --max-fps=30` | USB 共享 / 多设备 / 只求流畅 |
| 像素级 | `--video-codec=h265 --video-bit-rate=35M --max-fps=30` | 看 UI 细节、截图前 |

- **50 Mbps 是 VBR 上限，不是持续占用**：静态画面实际只有 0.4~0.5 Mbps，
  真正吃码率的是滚动、翻页、明暗切换的瞬间，所以不会压垮 USB。
- **不要用 `--max-size` 降分辨率来省带宽**：文字界面优先保码率。
- H.264 不建议超过约 60 Mbps：收益递减；且部分厂商编码器会忽略 profile/level 设置
  （实测 `OMX.qcom.video.encoder.avc` 报 `Failed to update the profile_level`，但 50 Mbps 正常）。
- H.265 同画质约省 30%~50% 码率，代价是编解码延迟略高，老设备兼容性要先验。

**级别**：✅ 2026-11-19，scrcpy 5.0.1 / Android 11 / Redmi Note 8（1080×2340，API 30）；
bpp 结论对其它高分辨率屏通用，档位可按实测微调。
