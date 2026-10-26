# 19 卡面 3D 倾斜 + 金属光斑（实战：不用自定义 View 的伪 3D）

日期：2026-10-26　环境：Android 9 (API 28)　iApp 5.0.1013

## 目标

一屏展示黑金卡：拖动卡片小幅 3D 倾斜，表面有圆形柔边白色光斑，整体喷砂哑光。
不做抽卡流程。验证「`.mjava` 不能定义 class」的前提下，能做出多好的 3D 视觉。

## 结论先行

**不需要自定义 View，也不需要 GL。** 三个普通 View 叠起来就够：

```
FrameLayout(卡容器, 300dp×420dp)     ← setRotationX/Y + setCameraDistance 做 3D
├── ImageView 卡面(900×1260 位图)    ← Canvas 现画：底色/喷砂/立绘/金边/文字
├── ImageView 光晕(480dp 正方形)     ← 极淡环境光
└── ImageView 光斑(300dp 正方形)     ← 圆形高光，随倾斜平移
```

容器上 `setClipToOutline(true)` + 圆角 `GradientDrawable` 背景，子 View 超出圆角的部分自动被裁——
光斑、光晕都不用自己做蒙版。

## 关键实现

### 1. 卡面现画（免资源文件）

```java
int w = dp(300);
int h = dp(420);
Bitmap bmp = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
Canvas c = new Canvas(bmp);
Paint p = new Paint();
p.setAntiAlias(true);
p.setShader(new LinearGradient(0, 0, w * 0.4f, h, Color.parseColor("#121218"), Color.parseColor("#020203"), Shader.TileMode.CLAMP));
c.drawRect(0, 0, w, h, p);
```

- 900×1260 整卡（含喷砂噪声 160²、文字、金边）耗时 **260~280 ms**，放载入事件可接受
- 文字用 `p.setTextSize(...)` + `c.drawText(...)`，右对齐用 `p.measureText()` 自己减
- 想「隔着毛玻璃」：**先在低分辨率位图上画，再放大贴上去**（120×150 很糊，200×250 较清晰）

### 2. 喷砂面 = 一张噪声平铺

```java
int n = 160;
int[] px = new int[n * n];
Random nr = new Random(4242L);
for (int k = 0; k < px.length; k++) {
    int al = nr.nextInt(22);
    int v = 205 + nr.nextInt(50);
    px[k] = (al << 24) | (v << 16) | (v << 8) | v;
}
Bitmap fine = Bitmap.createBitmap(n, n, Bitmap.Config.ARGB_8888);
fine.setPixels(px, 0, n, 0, 0, n, n);
p.setShader(new BitmapShader(fine, Shader.TileMode.REPEAT, Shader.TileMode.REPEAT));
c.drawRect(0, 0, W, H, p);
```

- 纯白噪声 + `REPEAT` = 均匀细颗粒哑光，**不要画拉丝线**（那是另一种表面）
- alpha 0~21 已经肉眼可见；再大就发灰，不是黑卡
- 想更粗糙：把同一张噪声用 `c.scale(4,4)` 再画一遍（4×4 像素的粗颗粒）

### 3. 圆形光斑：9 段衰减 + 放大

```java
Bitmap makeOrb(int wdp, int hdp, int core) {
    int s = 256;
    Bitmap sq = Bitmap.createBitmap(s, s, Bitmap.Config.ARGB_8888);
    Canvas sc = new Canvas(sq);
    Paint sp = new Paint();
    sp.setAntiAlias(true);
    int a = core;
    sp.setShader(new RadialGradient(s * 0.5f, s * 0.5f, s * 0.5f,
        new int[]{ Color.argb(a, 255, 250, 232), /* … 9 段 … */ Color.argb(0, 255, 224, 166) },
        new float[]{ 0f, 0.07f, 0.15f, 0.25f, 0.36f, 0.48f, 0.62f, 0.78f, 1f },
        Shader.TileMode.CLAMP));
    sc.drawRect(0, 0, s, s, sp);

    Bitmap out = Bitmap.createBitmap(dp(wdp), dp(hdp), Bitmap.Config.ARGB_8888);
    Canvas oc = new Canvas(out);
    Paint fp = new Paint();
    fp.setFilterBitmap(true);
    oc.scale(dp(wdp) / (float) s, dp(hdp) / (float) s);
    oc.drawBitmap(sq, 0f, 0f, fp);
    return out;
}
```

- **3 段渐变会出同心环**（色阶断层），9 段 + 双线性放大才干净
- 正方形 View 才是正圆；拉伸成矩形就是椭圆
- 光斑带 alpha，直接叠在卡面上就是"光打上去"

### 4. 交互：位移驱动倾斜

```java
public boolean touch(View v, MotionEvent e) {
    int a = e.getAction();
    if (a == MotionEvent.ACTION_DOWN) {
        v.setTag(new float[]{ e.getX(), e.getY() });      // 只记起点
        v.animate().cancel();
        return true;
    }
    if (a == MotionEvent.ACTION_MOVE) {
        float[] d = (float[]) v.getTag();
        float nx = (e.getX() - d[0]) / dp(110);
        float ny = (e.getY() - d[1]) / dp(110);
        // clamp 到 ±1 后乘最大角
        v.setRotationY(nx * 8.0f);
        v.setRotationX(-ny * 8.0f);
        applyLight(...);                                  // 光斑反向平移
    } else if (a == MotionEvent.ACTION_UP || a == MotionEvent.ACTION_CANCEL) {
        v.animate().rotationX(0f).rotationY(0f).setDuration(420).start();
    }
    return true;
}
```

- **按下的那一刻角度必须是 0**；用按下点绝对位置算角度会"一碰就歪"
- `setCameraDistance(dp(760))` 控制透视强度（越小越夸张）
- 回弹用 `View.animate()`（ViewPropertyAnimator），`cancel()` 能打断，比 ObjectAnimator 好收场
- 光斑位置存在 View 的 tag 里（`int[]{homeX, homeY}`），跨 call 不丢

## 实测读数

```
CARD init-done ms=276 w=900 h=1260
CARD dump=/storage/emulated/0/Android/data/com.iapp.app/files/card3d-face.png
CARD light-done children=3
CARD up rx=6.662804 ry=8.0
```

- init 260~280 ms（4 次）
- 全程零 `CARD *-err`
- 倾斜角精确停在 8.0（clamp 生效）

## 多方案共存：一页一个 `.iyu`

同一工程里放多个 `.iyu`，每个页面写一行带参数的 call：

```xml
<UIEventset><eventItme type="loading">call(null, "mjava", "card.page", "c")</eventItme></UIEventset>
```

```java
public void page(String mode) {
    init();          // 建卡面
    lightMode(mode); // 按模式布光
    bind();          // 绑触摸
}
```

加新方案只改 `lightMode` 里的参数表，**不要复制整页代码**。

## 未决

- `BlurMaskFilter`（软边）、`PorterDuffXfermode`（彩虹蒙版）在 mjava 里未实测 ⚠
- 只在 LDPlayer API 28 / density 3 上跑过，换机需重测耗时
- 光斑与卡面是两层独立 View，倾斜时两者的透视略有错位（8° 内看不出来，角度大可能会露）
