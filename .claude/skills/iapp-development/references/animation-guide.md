# mjava 动画

版本前提：iApp 5.0.1013、Android 9（API 28）、裕 3。

结论先行：**用 `ObjectAnimator` 驱动，用 `View.postDelayed` + 匿名 `Runnable` 收尾。**
不要用 `AnimatorListenerAdapter`（抽象类），也不要指望模块变量跨回调保留。

## 能用 / 不能用

| 写法 | 结果 |
|---|---|
| `ObjectAnimator.ofFloat(view, "translationX", new float[]{0f, dx})` | ✅ |
| `ObjectAnimator.ofFloat(view, "scaleX", new float[]{1f, 1.18f})` | ✅ |
| `setDuration(int)` / `setStartDelay(int)` / `start()` | ✅ |
| `view.setScaleX/setScaleY/setAlpha` | ✅ |
| `view.postDelayed(new Runnable(){ public void run(){ step2(); } }, 120)` | ✅ |
| 匿名 `Runnable` / `OnTouchListener` / `OnKeyListener` 回调里调同模块方法 | ✅ |
| `AnimatorListenerAdapter`（匿名继承抽象类） | ❌ BeanShell 只能匿名实现接口 |
| 依赖模块级变量跨 `call` | ❌ 每次 `call` 新解释器 |

## 平移

```java
ObjectAnimator ax = ObjectAnimator.ofFloat(v, "translationX", new float[]{0.0f, dx});
ax.setDuration(110);
ax.start();
```

## 回弹/归位：优先 `View.animate()`

✅ 实测（API 28，卡面 3D 探针）：ViewPropertyAnimator 在 mjava 里可链式调用，
而且**能取消**——这是 ObjectAnimator 做不到的地方（拿不到 animator 引用就没法取消）。

```java
v.animate().rotationX(0.0f).rotationY(0.0f).setDuration(420).start();   // 回弹
v.animate().cancel();                                                    // 按下时打断
```

- 适合"松手归位""按下打断"这类**会被新输入打断**的收尾动画
- 需要精确控制多段/插值器时仍用 ObjectAnimator
- 两者不要混用同一个属性：ObjectAnimator 不会被 `animate().cancel()` 停掉

- 一定要传 `new float[]{...}`，不要依赖可变参数展开
- 动画只改 `translation`，不改布局参数；结束后重绘/重建视图即可归位

## 收尾（没有监听器时的做法）

```java
boardFrame.postDelayed(new Runnable() {
    public void run() {
        afterSlide();
    }
}, 120);
```

`afterSlide()` 里再 `postDelayed` 到下一段（例如 `step3` 解锁输入）。
每一段都套 `try/catch`，异常时直接跳下一段，避免动画失败把输入锁死。

## 合并回弹 / 生成进场

```java
// 合并：先放大再回弹，两段靠 setStartDelay 串起来
ObjectAnimator sx1 = ObjectAnimator.ofFloat(v, "scaleX", new float[]{1.0f, 1.18f});
sx1.setDuration(60); sx1.start();
ObjectAnimator sx2 = ObjectAnimator.ofFloat(v, "scaleX", new float[]{1.18f, 1.0f});
sx2.setStartDelay(60); sx2.setDuration(60); sx2.start();
// scaleY 同理

// 生成
v.setScaleX(0.0f); v.setScaleY(0.0f); v.setAlpha(0.0f);
ObjectAnimator a = ObjectAnimator.ofFloat(v, "scaleX", new float[]{0.0f, 1.0f});
a.setDuration(110); a.start();
```

## 状态与视图身份

- 动画各阶段之间用 `i.sss` 传参（如 `merged` / `spawn` / `busy`），不要用模块变量
- 动态创建的视图跨 `call` 找不回来：给每个视图 `setTag("tile:" + idx)`，之后遍历 `getChildCount()/getChildAt(k)` 按 tag 查
- 视图层级有弹层时，重建后 `overlay.bringToFront()`

## 输入锁与排队

经典手感：动画期间不丢输入，也不让状态打架。

```java
if (busy) { i.sss("g.pending", dir); return; }
busy = true;
// ... 动画 ...
// 最后一段回调
busy = false;
String p = st("pending"); st("pending", "");
if (p.length() > 0) doMove(Integer.parseInt(p));
```

## 实测读数

2026-10-26 `com.demo.game2048`：

```
G2048 move dir=D add=4 score=4 spawn=5 ...
G2048 anim slide tiles=4
G2048 step2 merged=1 spawn=5
G2048 key code=22 dir=1
G2048 move queued dir=R
G2048 apply pending=1
```

用户确认：滑动、合并、生成动画都正常，连按不打架。
