# 20 ViewPager 翻页事件（探针：编译适配器 + 参数形状）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 之前为什么卡住

`onpageselected/onpagescrolled/onpagescrollstatechanged` 一直标 ❓，原因是
**`PagerAdapter` 是抽象类，BeanShell 只能实现接口、不能继承类**，没有适配器就点不亮事件。

现在有了「编译类进 dex」这条路（`external-library-guide.md`），探针得以跑通。

## 探针结构

```
iappbridge/VpAdapter.java      5 页纯色 TextView，继承 androidx.viewpager.widget.PagerAdapter
        ↓ javac(android.jar + viewpager.jar) → d8 --lib … 
apk/assets/vpadapter.dex       1.9 KB
探针页 mian.iyu                ViewPager 20 + 三个按钮（上一页/下一页/跳第 4 页）
vp.mjava                       setup/next/prev/jump + 事件回调
```

事件绑定用**重载兜底**，一次跑完就能确定参数个数：

```java
public void onSel() { … }          public void onSel(Object p) { … }
public void onScroll() { … }       public void onScroll(Object p) { … }
public void onScroll(Object p, Object o) { … }
public void onState() { … }        public void onState(Object s) { … }
```

iApp 注入几个参数就命中对应重载；被丢掉的参数会让调用退化到更少的重载，
所以「命中哪一档」本身就是读数。

## 读数

```
VP setup ok count=5 cur=0
VP state 1-arg st_sE=0
VP scroll 2-args st_pN=0 st_vO=null
VP state 1-arg st_sE=1
VP state 1-arg st_sE=2
VP sel 1-arg st_pN=1
VP jump -> 3 → VP sel 1-arg st_pN=3
```

| 事件 | 触发 | 参数 |
|---|---|---|
| `onpageselected` | 手势 + `setCurrentItem(n,true)` | 1 个：`st_pN` 页码，准确 |
| `onpagescrolled` | 高频，一次翻页 10+ 次 | 2 个：`st_pN` 正确；第二个 `st_vO` = **null** |
| `onpagescrollstatechanged` | 每次滚动成组 | 1 个：`st_sE` = 0 静止 / 1 拖拽 / 2 回弹 |

顺序：`state 1 → state 2 → sel → state 0`。

`st_vO` 是 null 而不是「参数被丢掉」——被丢掉会退化成 1 参重载，实测走的是 2 参。

## 复用结论

1. 需要继承类的场景（Adapter / Decoration / Callback 基类）一律走「编成 dex」
2. 该场景 `DexClassLoader` 父加载器**给宿主**（依赖如 `androidx.*` 在宿主里）；
   给 `null` 只适用于「依赖全在自己 dex 里」的库（如 sora）
3. 事件参数探测用重载兜底，省一轮往返

## 未决

- 偏移量（`positionOffset`）有没有别的变量名可拿，未穷举
- `VerticalViewPager` 是否同样支持这三个事件，未测
