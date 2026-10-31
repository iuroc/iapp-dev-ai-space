# 审阅输出模板

复制下面的骨架到**工程自己的私有资料区**（`<工程根>/docs/`）或当轮汇报里，不要写进 skill 目录。
文件名建议 `YYYY-MM-DD-quality-review.md`。

---

````markdown
# 工程质量审阅 YYYY-MM-DD

工程：<包名>
基线：<git sha>（工作区 dirty? yes/no）
规模：N 个 .mjava / M 行；.iyu K 个
范围：REUSE / STYLE / DUP / STATE（本轮未覆盖：<项>）
统计：阻断 a / 应修 b / 建议 c

## 扫描命令（证明跑过）

```bash
python .claude/skills/iapp-development/scripts/check_mjava.py <工程根>/src
wc -l <工程根>/src/*.mjava | sort -n
grep -oh 'i\.sss("[^"]*"' <工程根>/src/*.mjava | sort | uniq -c | sort -rn
# …把实际跑过的都贴上来
```

## 阻断

### [REUSE-02] src/<模块>.mjava:120 —— 进度条用屏宽算长度
- 现状：卡片内自绘 `FrameLayout` 轨道 + `View` 条，长度 `ui_screenW() * ratio / 1000`；
  卡片有 16dp 内边距，满进度时条超出内容宽，约 90% 就顶满并被裁。
- 可换成：`LinearProgressIndicator`（矩阵 ✅，`setProgressCompat`，`setIndicatorColor(new int[]{c})`）。
- 风险：颜色/轨道色要手动 tint；可变参方法必须传数组，单值会中断整段载入事件。
- 验收：`page/pageAll` = 10% / 50% / 100% 三档截图，条右缘距卡片内容右缘 0±1dp。

## 应修

### [DUP-01] src/list.mjava 全篇 / src/maglist.mjava 全篇 —— 两个列表页只差数据源
- 现状：分类表、页面骨架、切分类、翻页、错误态、骨架屏逐一对应，约 90% 同构。
- 可换成：`listctrl_page(cfg)`，cfg 含分类 id/名、网络方法、字段映射、详情目标。
- 风险：合并后可能长出 ≥3 个分支；先合并「骨架 + 翻页 + 三态」，数据映射留参数。
- 验收：两个 Tab 逐项对比截图（首屏 / 切分类 / 第 2 页 / 断网 / 空分类）一致。

## 建议

### [STATE-06] src/<模块>.mjava:88 —— tabPage 末尾分支不可达
- 现状：四个分支都已 return，末尾的占位页永远不执行，还自带一份页头逻辑。
- 处理：删除；先确认没有未知 idx 依赖它兜底。
- 验收：四个 Tab 切换正常，无异常日志。

## 已通过项（说明扫到了、没误报）

| 项 | 结论 |
|---|---|
| Canvas 线稿图标 `src/icon.mjava` | 库无等价物，合法自定义 |
| 安全区主动查询 `ui_insets` | `setOnApplyWindowInsetsListener` 会 Parse error，唯一解 |
| 分段缓存 `android.util.LruCache` | 已复用库；未重写 `sizeOf`（继承类不可用） |
| 面板 `BottomSheetDialog` / 抽屉 `DrawerLayout` / 分类栏 `TabLayout` | 已复用库 |

## 已排除（误报候选 + 理由）

| 候选 | 不报的理由 |
|---|---|
| 列表封面 104dp vs 详情封面 132dp | 层级差异，不是样式分叉 |
| `ct_style` 逐项改字重 | `TabLayout` 无 per-state 粗体 API，属合法自定义 |
| 手写三列网格 | 无 dex 时 `RecyclerView.Adapter` 不可用；已登记为已知代价 |

## 未决 / 待验

- [ ] [REUSE-12] `GridView + SimpleAdapter` 能否承载「封面+两行文字」❓
      验法：最小探针页挂 6 条假数据，看封面与第二行是否渲染、滚动是否复用。

## 下一轮入口

1. 先修阻断（本轮 N 条），再按「合并面最大」排序做应修
2. 建议项不排期，随相关页面改动顺手处理
````

---

## 填写规则

- **五要素缺一不写**：`文件:行`、现状、可替换的库组件/统一写法、风险、验收点。
- 验收点必须能被第三人执行：写明页面、操作、观察对象（截图/日志/属性）。
- 同一条发现只出现一次；跨类别时归到主因（复用缺失导致的样式分叉 → REUSE）。
- 数量以汇总表为准；明细里每条带类别 ID（`REUSE-01` / `STYLE-03` / `DUP-02` / `STATE-05`），
  与 `references/checklist.md` 的编号对应。
- 结论级别与知识沉淀一致：静态可判不加标记，需要上屏的写验收点，不确定的标 ❓ 并给验法。
