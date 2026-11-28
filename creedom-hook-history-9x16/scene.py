"""THE FIRST THREE SECONDS: Creedom documentary reel, 9:16 (render at 1080x1920).

One camera travels DOWN one board, a vertical timeline:
  title (y 0) -> 1918 front page (y 8k) -> silent-era film strip (y 15k) -> 1941 TV (y 23k) -> TODAY phone (y 31k)
then pulls back over every era (TESTED LIVE) and lands on the phone and the Creedom analyzer card.

Times come from the real take: L(i)/E(i) line start/end, T(i, word) the word's measured start
(audio/words.json, from faster-whisper on the recorded voice, which is used exactly as recorded).
At 1080 px wide, zoom 1 shows 3840 x 6827 world px.
"""
import json
import math
import pathlib

import skia

from engine import (HILITE, WHITE, BigText, Counter, Film, Item, PenMark, Print, Stamp, SAMPLING, clamp, draw_text,
                    ease_in_out, ease_out_back, ease_out_cubic, paint, ramp, text_width)

HERE = pathlib.Path(__file__).resolve().parent
PINK = (243, 67, 162)
PINK_SOFT = (255, 198, 224)
INKD = (26, 16, 32)
DARK = (30, 26, 22)
RED = (176, 26, 22)
POPPINS = HERE.parent / "brands" / "creedom" / "fonts"

Y_NEWS, Y_FILM, Y_TV, Y_NOW = 8200, 15400, 23300, 29900


# ---------------------------------------------------------------- helpers
_TF = {}


def pop_font(weight, size):
    if weight not in _TF:
        _TF[weight] = skia.Typeface.MakeFromFile(str(POPPINS / f"Poppins-{weight}.ttf"))
    f = skia.Font(_TF[weight], size); f.setSubpixel(True); f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def ptext(c, text, x, y, size, weight="Bold", rgb=INKD, a=1.0, align="left"):
    f = pop_font(weight, size)
    w = f.measureText(text)
    x0 = x - w / 2 if align == "center" else x - w if align == "right" else x
    c.drawString(text, x0, y, f, paint(rgb, a))
    return w


def rrect(x, y, w, h, r):
    return skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)


# ---------------------------------------------------------------- custom items
class FilmStrip(Item):
    """A vertical film strip that unrolls down: feature frames (crops of the 1914 poster), THE END, then the
    trailer frame. At t_move the trailer frame jumps to the front (top) and the others shift down."""
    z = 14

    def __init__(self, x, y, t_in, t_move, fw=1250, fh=900, pitch=1050, t_out=None):
        super().__init__(t_in, t_out)
        self.x, self.y, self.t_move, self.fw, self.fh, self.pitch = x, y, t_move, fw, fh, pitch
        self.n = 5

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.x - 1200, self.y - 900, self.x + 1200, self.y + self.pitch * self.n + 900)

    def cues(self):
        return [("whoosh", self.t_in, 0.35, {}), ("pop", self.t_move, 0.7, {})]

    def slot(self, i, t):
        u = ease_in_out(ramp(t, self.t_move, 0.7))
        if i == 4:                      # trailer: from the last slot to the first
            return 4 * (1 - u)
        return i + u                    # everyone else: one slot down

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.25) * self.fade(t)
        if a <= 0:
            return
        unroll = ease_out_cubic(ramp(t, self.t_in, 1.1))
        W = self.fw + 300
        top = self.y - self.pitch / 2
        H = self.pitch * self.n
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(self.x - W, top - 200, 2 * W, (H + 400) * unroll))
        c.save(); c.translate(0, 30)
        c.drawRect(skia.Rect.MakeXYWH(self.x - W / 2, top, W, H), paint((0, 0, 0), 0.45 * a, blur=40)); c.restore()
        c.drawRect(skia.Rect.MakeXYWH(self.x - W / 2, top, W, H), paint((24, 19, 15), a))
        hole = paint((214, 204, 186), 0.9 * a)
        k = 0
        yy = top + 40
        while yy < top + H - 60:
            for sx in (self.x - W / 2 + 40, self.x + W / 2 - 40 - 70):
                c.drawRRect(rrect(sx, yy, 70, 90, 14), hole)
            yy += 150; k += 1
        img = res.image("P02")
        iw, ih = img.width(), img.height()
        crops = [(0.10, 0.30), (0.20, 0.52), (0.05, 0.74)]       # (left, top) fractions of the poster
        order = sorted(range(self.n), key=lambda i: 1 if i == 4 else 0)   # trailer drawn last (on top while moving)
        for i in order:
            cy = self.y + self.slot(i, t) * self.pitch
            r = skia.Rect.MakeXYWH(self.x - self.fw / 2, cy - self.fh / 2, self.fw, self.fh)
            if i < 3:
                fl, ft = crops[i]
                sw = iw * 0.62; sh = sw * self.fh / self.fw
                src = skia.Rect.MakeXYWH(iw * fl, ih * ft, sw, sh)
                p = skia.Paint(AntiAlias=True); p.setAlphaf(a)
                p.setColorFilter(skia.ColorFilters.Matrix([0.30, 0.55, 0.12, 0, 0.04, 0.26, 0.48, 0.10, 0, 0.016,
                                                           0.20, 0.38, 0.08, 0, 0, 0, 0, 0, 1, 0]))
                c.drawImageRect(img, src, r, SAMPLING, p)
                draw_text(c, res, f"FEATURE  ·  REEL {i + 1}", r.left() + 40, r.bottom() - 40, 64, "mono", (240, 230, 210), 0.8 * a)
            elif i == 3:
                c.drawRect(r, paint((8, 7, 6), a))
                draw_text(c, res, "THE END", self.x, cy + 70, 230, "serif", (238, 230, 214), a, 0.08, "center")
                c.drawRect(skia.Rect.MakeXYWH(self.x - 300, cy + 130, 600, 8), paint((238, 230, 214), 0.7 * a))
            else:
                c.drawRect(r, paint((232, 196, 92), a))
                c.drawRect(skia.Rect.MakeXYWH(r.left() + 36, r.top() + 36, self.fw - 72, self.fh - 72),
                           paint((40, 26, 12), a, stroke=14))
                draw_text(c, res, "COMING", self.x, cy - 40, 250, "cond", (40, 26, 12), a, 0.06, "center")
                draw_text(c, res, "ATTRACTIONS", self.x, cy + 200, 200, "cond", (176, 30, 22), a, 0.06, "center")
                draw_text(c, res, "TRAILER", r.left() + 40, r.bottom() - 40, 64, "mono", (40, 26, 12), 0.8 * a)
        c.restore()


class WatchFace(Item):
    """A watch face whose ring fills over `dur` seconds (ten seconds of airtime, compressed) and a sweeping hand."""
    z = 16

    def __init__(self, x, y, r, t_in, t_fill, dur, t_out=None):
        super().__init__(t_in, t_out)
        self.x, self.y, self.r, self.t_fill, self.dur = x, y, r, t_fill, dur

    def bounds(self, res):
        R = self.r * 1.6
        return skia.Rect.MakeLTRB(self.x - R, self.y - R, self.x + R, self.y + R)

    def draw(self, c, res, t):
        u = ease_out_back(ramp(t, self.t_in, 0.45), 1.3)
        a = ramp(t, self.t_in, 0.2) * self.fade(t)
        if a <= 0:
            return
        r = self.r * (0.85 + 0.15 * u)
        c.save(); c.translate(0, 24); c.drawCircle(self.x, self.y, r * 1.08, paint((0, 0, 0), 0.4 * a, blur=36)); c.restore()
        c.drawCircle(self.x, self.y, r * 1.08, paint((196, 160, 92), a))
        c.drawCircle(self.x, self.y, r, paint((246, 238, 222), a))
        for k in range(60):
            ang = math.radians(k * 6 - 90)
            l = r * (0.16 if k % 5 == 0 else 0.07)
            w = 16 if k % 5 == 0 else 6
            c.drawLine(self.x + math.cos(ang) * (r * 0.9 - l), self.y + math.sin(ang) * (r * 0.9 - l),
                       self.x + math.cos(ang) * r * 0.9, self.y + math.sin(ang) * r * 0.9, paint(DARK, a, stroke=w))
        f = ramp(t, self.t_fill, self.dur)
        if f > 0:
            path = skia.Path(); oval = skia.Rect.MakeXYWH(self.x - r * 0.7, self.y - r * 0.7, r * 1.4, r * 1.4)
            path.moveTo(self.x, self.y); path.arcTo(oval, -90, 360 * f * 10 / 60, False); path.close()
            c.drawPath(path, paint(RED, 0.85 * a))
        ang = math.radians(-90 + 360 * f * 10 / 60)
        c.drawLine(self.x, self.y, self.x + math.cos(ang) * r * 0.82, self.y + math.sin(ang) * r * 0.82, paint(DARK, a, stroke=18))
        c.drawCircle(self.x, self.y, 34, paint(DARK, a))
        draw_text(c, res, "ON AIR", self.x, self.y + r * 0.45, r * 0.16, "cond", RED, a, 0.12, "center")


class Phone(Item):
    """Today's screen, in colour: a reel with a hook line; at t_swipe a thumb flicks it away and the next reel slides in."""
    z = 20

    def __init__(self, x, y, w, t_in, t_swipe, t_out=None):
        super().__init__(t_in, t_out)
        self.x, self.y, self.w, self.h, self.t_swipe = x, y, w, w * 2.05, t_swipe

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.x - self.w, self.y - self.h, self.x + self.w, self.y + self.h)

    def cues(self):
        return [("pop", self.t_in, 0.6, {}), ("whoosh", self.t_swipe, 0.5, {})]

    def reel(self, c, res, x0, y0, w, h, a, kind):
        if kind == 0:
            sh = skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x0 + w, y0 + h)],
                                                [skia.Color(255, 120, 72), skia.Color(243, 67, 162)])
        else:
            sh = skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x0 + w, y0 + h)],
                                                [skia.Color(60, 90, 220), skia.Color(30, 200, 190)])
        p = skia.Paint(AntiAlias=True, Shader=sh); p.setAlphaf(a)
        c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), p)
        cx = x0 + w / 2
        if kind == 0:
            c.drawRRect(rrect(cx - w * 0.36, y0 + h * 0.30, w * 0.72, h * 0.13, 30), paint(WHITE, 0.95 * a))
            ptext(c, "wait for it...", cx, y0 + h * 0.385, w * 0.085, "ExtraBold", INKD, a, "center")
        else:
            c.drawRRect(rrect(cx - w * 0.36, y0 + h * 0.30, w * 0.72, h * 0.13, 30), paint(WHITE, 0.95 * a))
            ptext(c, "your next reel", cx, y0 + h * 0.383, w * 0.068, "ExtraBold", INKD, a, "center")
        for k in range(3):                       # like / comment / share column
            c.drawCircle(x0 + w * 0.88, y0 + h * (0.58 + 0.08 * k), w * 0.045, paint(WHITE, 0.9 * a))
        c.drawCircle(x0 + w * 0.10, y0 + h * 0.86, w * 0.05, paint(WHITE, 0.9 * a))
        c.drawRRect(rrect(x0 + w * 0.18, y0 + h * 0.845, w * 0.42, h * 0.018, 12), paint(WHITE, 0.85 * a))
        c.drawRRect(rrect(x0 + w * 0.06, y0 + h * 0.90, w * 0.62, h * 0.014, 10), paint(WHITE, 0.6 * a))

    def draw(self, c, res, t):
        u = ease_out_back(ramp(t, self.t_in, 0.5), 1.2)
        a = ramp(t, self.t_in, 0.2) * self.fade(t)
        if a <= 0:
            return
        W, H = self.w, self.h
        c.save(); c.translate(self.x, self.y + (1 - u) * 300)
        c.save(); c.translate(0, 40); c.drawRRect(rrect(-W / 2, -H / 2, W, H, W * 0.14), paint((0, 0, 0), 0.5 * a, blur=60)); c.restore()
        c.drawRRect(rrect(-W / 2, -H / 2, W, H, W * 0.14), paint((14, 14, 16), a))
        bz = W * 0.04
        scr = rrect(-W / 2 + bz, -H / 2 + bz, W - 2 * bz, H - 2 * bz, W * 0.11)
        c.save(); c.clipRRect(scr, skia.ClipOp.kIntersect, True)
        sx, sy, sw, shh = -W / 2 + bz, -H / 2 + bz, W - 2 * bz, H - 2 * bz
        s = ease_in_out(ramp(t, self.t_swipe, 0.45))
        self.reel(c, res, sx, sy - s * shh, sw, shh, a, 0)
        if s > 0:
            self.reel(c, res, sx, sy + (1 - s) * shh, sw, shh, a, 1)
        # progress bar of the first reel: 3 seconds
        c.drawRect(skia.Rect.MakeXYWH(sx, sy + shh - 18, sw * clamp((t - self.t_in) / 3.0), 18), paint(WHITE, 0.9 * a * (1 - s)))
        c.restore()
        c.drawRRect(rrect(-W * 0.14, -H / 2 + bz + 30, W * 0.28, W * 0.075, W * 0.04), paint((14, 14, 16), a))   # notch
        # thumb: a soft disc that flicks upward
        th = ramp(t, self.t_swipe - 0.25, 0.75)
        if 0 < th < 1:
            ty = H * 0.30 - th * H * 0.55
            ta = math.sin(th * math.pi) * a
            c.drawCircle(W * 0.12, ty, W * 0.13, paint((255, 222, 200), 0.85 * ta))
            c.drawCircle(W * 0.12, ty, W * 0.13, paint(WHITE, 0.9 * ta, stroke=10))
        c.restore()


class AnalyzerCard(Item):
    """Creedom's Reel Analyzer result (an illustration): hook score 4.2 / 5 labelled EXAMPLE, one flagged second with its fix."""
    z = 40

    def __init__(self, x, y, w, t_in, t_score, t_flag, t_post, t_out=None):
        super().__init__(t_in, t_out)
        self.x, self.y, self.w, self.h = x, y, w, w * 0.78
        self.t_score, self.t_flag, self.t_post = t_score, t_flag, t_post

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.x - self.w, self.y - self.h, self.x + self.w, self.y + self.h)

    def cues(self):
        return [("pop", self.t_in, 0.7, {}), ("ticks", self.t_score, 0.6, {}), ("pop", self.t_flag, 0.5, {}), ("ding", self.t_post, 0.6, {})]

    def draw(self, c, res, t):
        u = ease_out_back(ramp(t, self.t_in, 0.5), 1.25)
        a = ramp(t, self.t_in, 0.18) * self.fade(t)
        if a <= 0:
            return
        W, H = self.w, self.h
        c.save(); c.translate(self.x, self.y + (1 - u) * 260); s = 0.9 + 0.1 * u; c.scale(s, s)
        c.save(); c.translate(0, 40); c.drawRRect(rrect(-W / 2, -H / 2, W, H, 90), paint((0, 0, 0), 0.45 * a, blur=60)); c.restore()
        c.drawRRect(rrect(-W / 2, -H / 2, W, H, 90), paint((253, 241, 246), a))
        c.drawRRect(rrect(-W / 2, -H / 2, W, H, 90), paint(PINK, a, stroke=10))
        L = -W / 2 + W * 0.07
        logo = res.image("logo_creedom.png", 1400)
        lw = W * 0.38; lh = lw * logo.height() / logo.width()
        p = skia.Paint(AntiAlias=True); p.setAlphaf(a)
        c.drawImageRect(logo, skia.Rect.MakeXYWH(L, -H / 2 + H * 0.07, lw, lh), SAMPLING, p)
        ptext(c, "REEL ANALYZER", W / 2 - W * 0.07, -H / 2 + H * 0.07 + lh * 0.78, W * 0.042, "SemiBold", (120, 100, 120), a, "right")
        # score
        su = ramp(t, self.t_score, 0.9)
        v = 4.2 * ease_out_cubic(su)
        ptext(c, "HOOK SCORE", L, -H / 2 + H * 0.36, W * 0.05, "SemiBold", (120, 100, 120), a)
        sw = ptext(c, f"{v:.1f}", L, -H / 2 + H * 0.60, W * 0.20, "ExtraBold", INKD, a * clamp(su * 4))
        ptext(c, "/ 5", L + sw + W * 0.03, -H / 2 + H * 0.60, W * 0.08, "Bold", (120, 100, 120), a * clamp(su * 4))
        # EXAMPLE tag
        ex = ramp(t, self.t_score + 0.3, 0.3) * a
        tx, ty = W / 2 - W * 0.07 - W * 0.26, -H / 2 + H * 0.43
        c.drawRRect(rrect(tx, ty, W * 0.26, W * 0.08, W * 0.04), paint(INKD, ex))
        ptext(c, "EXAMPLE", tx + W * 0.13, ty + W * 0.055, W * 0.04, "Bold", PINK_SOFT, ex, "center")
        # stars
        for k in range(5):
            cx = W / 2 - W * 0.07 - W * 0.26 + W * 0.026 + k * W * 0.052
            fill = clamp(v - k)
            c.drawCircle(cx, -H / 2 + H * 0.60 - W * 0.03, W * 0.019, paint((230, 210, 222), a))
            if fill > 0:
                c.drawCircle(cx, -H / 2 + H * 0.60 - W * 0.03, W * 0.019 * (0.4 + 0.6 * fill), paint(PINK, a))
        # flag row
        fa = ramp(t, self.t_flag, 0.3) * a
        fy = -H / 2 + H * 0.68
        c.drawRRect(rrect(L, fy, W * 0.86, H * 0.13, 40), paint(WHITE, fa))
        c.drawRRect(rrect(L + W * 0.025, fy + H * 0.025, W * 0.13, H * 0.08, 24), paint(PINK, fa))
        ptext(c, "0:02", L + W * 0.025 + W * 0.065, fy + H * 0.085, W * 0.04, "Bold", WHITE, fa, "center")
        ptext(c, "Weak hook", L + W * 0.19, fy + H * 0.06, W * 0.04, "Bold", INKD, fa)
        ptext(c, "Fix: show the result first", L + W * 0.19, fy + H * 0.105, W * 0.034, "SemiBold", (110, 90, 110), fa)
        # before-you-post pill
        pa = ramp(t, self.t_post, 0.3) * a
        py = -H / 2 + H * 0.86
        pw = W * 0.86
        c.drawRRect(rrect(L, py, pw * ease_out_cubic(ramp(t, self.t_post, 0.4)), H * 0.1, 50), paint(INKD, pa))
        ptext(c, "CHECKED BEFORE YOU POST", L + pw / 2, py + H * 0.067, W * 0.043, "Bold", PINK_SOFT, pa, "center")
        c.restore()


class EndLine(Item):
    """creedom.ai sign-off in Poppins."""
    z = 45

    def __init__(self, x, y, size, t_in):
        super().__init__(t_in, None)
        self.x, self.y, self.size = x, y, size

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.x - 4000, self.y - 2000, self.x + 4000, self.y + 2000)

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.4)
        if a <= 0:
            return
        dy = (1 - ease_out_cubic(ramp(t, self.t_in, 0.6))) * 80
        ptext(c, "Test your hook before you post", self.x, self.y + dy, self.size * 0.5, "SemiBold", WHITE, a * 0.92, "center")
        ptext(c, "creedom.ai", self.x, self.y + self.size * 0.95 + dy, self.size, "ExtraBold", PINK, a, "center")


# ---------------------------------------------------------------- engagement layer (v2)
import random as _random


class Flash(Item):
    """A white documentary flash-cut: peaks at t_in and decays in 0.2 s."""
    z = 300

    def __init__(self, t_in, peak=0.55):
        super().__init__(t_in, t_in + 0.25, sfx=False)
        self.peak = peak

    def visible(self, t):
        return self.t_in - 0.02 <= t <= self.t_in + 0.3

    def draw(self, c, res, t):
        u = (t - self.t_in) / 0.22
        if not 0 <= u <= 1:
            return
        c.drawRect(skia.Rect.MakeXYWH(-200000, -200000, 400000, 400000), paint((255, 248, 232), self.peak * (1 - u) ** 2))


class YearRoll(Item):
    """A year that rolls from y0 to y1 like an odometer, dark ink on a yellow block."""
    z = 70

    def __init__(self, x, y, size, y0, y1, t_in, dur=0.7, rgb=DARK, bar=HILITE):
        super().__init__(t_in, None)
        self.x, self.y, self.size, self.y0, self.y1, self.dur, self.rgb, self.bar = x, y, size, y0, y1, dur, rgb, bar

    def bounds(self, res):
        r = self.size * 4
        return skia.Rect.MakeLTRB(self.x - r, self.y - r, self.x + r, self.y + r)

    def cues(self):
        return [("ticks", self.t_in, 0.7, {})]

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.2)
        if a <= 0:
            return
        u = ease_out_cubic(ramp(t, self.t_in, self.dur))
        v = self.y0 + (self.y1 - self.y0) * u
        tw = text_width(res, "8888", self.size, "cond", 0.04)
        bw = ease_out_cubic(ramp(t, self.t_in - 0.05, 0.3))
        c.drawRect(skia.Rect.MakeXYWH(self.x - tw / 2 - self.size * 0.15, self.y + self.size * 0.063 - self.size * 0.92,
                                      (tw + self.size * 0.3) * bw, self.size * 0.92), paint(self.bar, 0.95 * a))
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(self.x - tw, self.y - self.size * 0.86, tw * 2, self.size * 0.92))
        n, frac = int(v), v - int(v)
        off = frac * self.size * 1.05 if u < 1 else 0
        draw_text(c, res, str(n), self.x, self.y - off, self.size, "cond", self.rgb, a, 0.04, "center")
        if u < 1:
            draw_text(c, res, str(n + 1), self.x, self.y - off + self.size * 1.05, self.size, "cond", self.rgb, a, 0.04, "center")
        c.restore()


class Magnifier(Item):
    """A brass-rimmed lens that slides along a line of a print, showing it magnified."""
    z = 55

    def __init__(self, pr, a, b, r, mag, t_in, dur, t_out):
        super().__init__(t_in, t_out)
        self.pr, self.a, self.b, self.r, self.mag, self.dur = pr, a, b, r, mag, dur

    def bounds(self, res):
        x0, x1 = sorted((self.a[0], self.b[0])); y0, y1 = sorted((self.a[1], self.b[1]))
        return skia.Rect.MakeLTRB(x0 - 2 * self.r, y0 - 2 * self.r, x1 + 2 * self.r, y1 + 3 * self.r)

    def cues(self):
        return [("whoosh", self.t_in, 0.3, {})]

    def draw(self, c, res, t):
        al = ramp(t, self.t_in, 0.2) * self.fade(t)
        if al <= 0:
            return
        u = ease_in_out(ramp(t, self.t_in, self.dur))
        lx = self.a[0] + (self.b[0] - self.a[0]) * u; ly = self.a[1] + (self.b[1] - self.a[1]) * u
        r = self.r * (0.6 + 0.4 * ease_out_back(ramp(t, self.t_in, 0.35), 1.4))
        pr = self.pr; w, h = pr.size(res)
        c.save(); c.translate(20, 40); c.drawCircle(lx, ly, r * 1.1, paint((0, 0, 0), 0.45 * al, blur=40)); c.restore()
        hx, hy = lx + r * 0.8, ly + r * 0.8           # handle
        c.drawLine(hx, hy, hx + r * 0.9, hy + r * 0.9, paint((60, 40, 22), al, stroke=r * 0.22))
        c.save()
        path = skia.Path(); path.addCircle(lx, ly, r)
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        c.drawCircle(lx, ly, r, paint((236, 228, 210), al))
        c.translate(lx, ly); c.scale(self.mag, self.mag); c.translate(-lx, -ly)
        c.translate(pr.x, pr.y); c.rotate(pr.rot)
        p = skia.Paint(AntiAlias=True); p.setAlphaf(al)
        c.drawImageRect(res.image(pr.key), skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), SAMPLING, p)
        c.restore()
        c.drawCircle(lx - r * 0.3, ly - r * 0.35, r * 0.45, paint((255, 255, 255), 0.12 * al, blur=30))
        c.drawCircle(lx, ly, r, paint((182, 140, 70), al, stroke=r * 0.1))
        c.drawCircle(lx, ly, r * 1.05, paint((90, 62, 30), al, stroke=r * 0.03))


class FilmDamage(Item):
    """Old-film texture over a region: flickering exposure, vertical scratches and dust, re-drawn 12 times a second."""
    z = 250

    def __init__(self, rect, t_in, t_out, strength=1.0):
        super().__init__(t_in, t_out, sfx=False)
        self.rect, self.k = rect, strength

    def bounds(self, res):
        x, y, w, h = self.rect
        return skia.Rect.MakeXYWH(x, y, w, h)

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.3) * self.fade(t) * self.k
        if a <= 0:
            return
        x, y, w, h = self.rect
        rng = _random.Random(int(t * 12))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint((255, 236, 200), a * rng.uniform(0.0, 0.07)))
        for _ in range(rng.randint(1, 3)):
            sx = x + rng.uniform(0, w)
            c.drawLine(sx, y, sx + rng.uniform(-40, 40), y + h, paint((250, 240, 220), a * rng.uniform(0.08, 0.22), stroke=rng.uniform(3, 9)))
        for _ in range(rng.randint(5, 12)):
            c.drawCircle(x + rng.uniform(0, w), y + rng.uniform(0, h), rng.uniform(6, 22), paint((20, 14, 10), a * rng.uniform(0.25, 0.6)))


class TVScreen(Item):
    """Switches the 1939 set on: static noise, then a glowing picture with a small clock and ON AIR."""
    z = 15

    def __init__(self, pr, doc, t_static, t_on):
        super().__init__(t_static, None)
        self.pr, self.t_on = pr, t_on
        self.c = doc.on(pr, 0.5, 0.125)
        w, h = pr.size_from(doc.meta)
        self.w, self.h = w * 0.33, h * 0.085

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.c[0] - 800, self.c[1] - 500, self.c[0] + 800, self.c[1] + 500)

    def cues(self):
        return [("static", self.t_in, 0.6, {})]

    def draw(self, c, res, t):
        if t < self.t_in:
            return
        cx, cy = self.c; w, h = self.w, self.h
        c.save(); c.translate(cx, cy); c.rotate(self.pr.rot)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 40, 40)
        c.clipRRect(rr, skia.ClipOp.kIntersect, True)
        if t < self.t_on:
            rng = _random.Random(int(t * 30))
            c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), paint((40, 40, 40), 1))
            for _ in range(160):
                g = rng.randint(80, 255)
                c.drawRect(skia.Rect.MakeXYWH(-w / 2 + rng.uniform(0, w), -h / 2 + rng.uniform(0, h), rng.uniform(8, 40), rng.uniform(4, 10)), paint((g, g, g), 0.9))
        else:
            u = ramp(t, self.t_on, 0.25)
            c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), paint((214, 222, 214), u))
            r = h * 0.32
            c.drawCircle(-w * 0.18, 0, r, paint((40, 40, 40), u, stroke=10))
            ang = math.radians(-90 + 360 * ((t - self.t_on) / 10.0))
            c.drawLine(-w * 0.18, 0, -w * 0.18 + math.cos(ang) * r * 0.8, math.sin(ang) * r * 0.8, paint((40, 40, 40), u, stroke=10))
            draw_text(c, res, "ON AIR", w * 0.17, h * 0.12, h * 0.34, "cond", (176, 26, 22), u, 0.1, "center")
            c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), paint((255, 255, 255), 0.25 * (1 - u)))
        c.restore()
        c.save(); c.translate(cx, cy); c.rotate(self.pr.rot)
        glow = ramp(t, self.t_on, 0.3)
        if glow > 0:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 - 30, -h / 2 - 30, w + 60, h + 60), 60, 60),
                        paint((210, 230, 255), 0.18 * glow, blur=60))
        c.restore()


class FeedScroll(Item):
    """An endless feed: two dim columns of reel cards scrolling up behind the phone, faster after the swipe."""
    z = 17

    def __init__(self, x, y, t_in, t_fast, t_out):
        super().__init__(t_in, t_out, sfx=False)
        self.x, self.y, self.t_fast = x, y, t_fast
        self.cols = [((243, 67, 162), (255, 140, 80)), ((70, 110, 230), (40, 200, 190)), ((150, 80, 220), (243, 67, 162)), ((255, 170, 60), (240, 80, 90))]

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.x - 3000, self.y - 5000, self.x + 3000, self.y + 5000)

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.4) * self.fade(t)
        if a <= 0:
            return
        dt = t - self.t_in
        fast = max(0.0, t - self.t_fast)
        off = dt * 700 + fast * 2600
        cw, ch, gap = 640, 1140, 220
        for side, xs in ((-1, self.x - 1560), (1, self.x + 1560)):
            for k in range(-4, 6):
                yy = self.y + k * (ch + gap) - (off * (1 if side < 0 else 1.15)) % (ch + gap)
                ca, cb = self.cols[(k + (2 if side > 0 else 0)) % 4]
                sh = skia.GradientShader.MakeLinear([skia.Point(xs, yy), skia.Point(xs + cw, yy + ch)],
                                                    [skia.Color(*ca), skia.Color(*cb)])
                p = skia.Paint(AntiAlias=True, Shader=sh); p.setAlphaf(0.42 * a)
                c.drawRRect(rrect(xs - cw / 2, yy - ch / 2, cw, ch, 60), p)
                c.drawRRect(rrect(xs - cw * 0.35, yy - ch * 0.1, cw * 0.7, ch * 0.09, 20), paint(WHITE, 0.4 * a))


class HookScan(Item):
    """Line 13: a pink scan sweeps the phone screen; three segments 0:01 0:02 0:03 tick on; label above."""
    z = 30

    def __init__(self, phone, t_in, t_out, t_end):
        super().__init__(t_in, t_out)
        self.ph, self.t_end = phone, t_end

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.ph.x - 3000, self.ph.y - self.ph.h, self.ph.x + 3000, self.ph.y + self.ph.h)

    def cues(self):
        return [("scan", self.t_in, 0.7, {})]

    def draw(self, c, res, t):
        a = ramp(t, self.t_in, 0.25) * self.fade(t)
        if a <= 0:
            return
        ph = self.ph; W, H = ph.w * 0.92, ph.h * 0.94
        x0, y0 = ph.x - W / 2, ph.y - H / 2
        per = 0.9
        u = ((t - self.t_in) % per) / per
        sy = y0 + H * u
        g = skia.GradientShader.MakeLinear([skia.Point(0, sy - 260), skia.Point(0, sy)],
                                           [skia.Color(243, 67, 162, 0), skia.Color(243, 67, 162, int(150 * a))])
        p = skia.Paint(AntiAlias=True, Shader=g)
        c.save(); c.clipRRect(rrect(x0, y0, W, H, ph.w * 0.1), skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeXYWH(x0, sy - 260, W, 260), p)
        c.drawRect(skia.Rect.MakeXYWH(x0, sy - 6, W, 12), paint((255, 230, 245), a))
        c.restore()
        for k in range(4):                                  # corner brackets
            cx = x0 - 60 if k % 2 == 0 else x0 + W + 60
            cy = y0 - 60 if k < 2 else y0 + H + 60
            dx = 1 if k % 2 == 0 else -1; dy = 1 if k < 2 else -1
            pk = paint(PINK, a, stroke=22)
            c.drawLine(cx, cy, cx + dx * 260, cy, pk); c.drawLine(cx, cy, cx, cy + dy * 260, pk)
        ptext(c, "SCANNING THE FIRST 3 SECONDS", ph.x, y0 - 700, 185, "ExtraBold", WHITE, a, "center")
        segw, gap = 560, 50
        tot = 3 * segw + 2 * gap
        for k in range(3):
            fill = clamp((t - self.t_in - 0.25 - k * 0.55) / 0.5)
            sx = ph.x - tot / 2 + k * (segw + gap)
            c.drawRRect(rrect(sx, y0 - 330, segw, 80, 40), paint((255, 255, 255), 0.25 * a))
            if fill > 0:
                c.drawRRect(rrect(sx, y0 - 330, segw * fill, 80, 40), paint(PINK, a))
            ptext(c, f"0:0{k + 1}", sx + segw / 2, y0 - 400, 140, "Bold", WHITE, a * (0.5 + 0.5 * (fill >= 1)), "center")


# ---------------------------------------------------------------- the film
def build_film(doc):
    L, E = doc.L, doc.E
    words = json.loads((doc.dir / "audio" / "words.json").read_text())

    def T(i, w, nth=0):
        hits = [x["s"] for x in words[str(i)] if x["w"].startswith(w.lower())]
        return hits[nth]

    film = Film(doc.duration, fps=42, look="wall")
    film.fade_in, film.fade_out = 0.0, 0.6            # frame one is the hook: no fade from black
    film.look["grain"] = 0.02

    def shot(t, x, y, z, rot=0.0, strength=0.45):
        film.shot(t, x, y, z, rot, radius=2600 / z, strength=strength)

    # ================================================= OPEN (1-2): the title over four eras
    film.add(BigText("THE FIRST", 0, -2150, 520, -0.7, rgb=(244, 238, 226), hit=None))
    film.add(BigText("3 SECONDS", 0, -1050, 780, -0.7, rgb=DARK, bar=HILITE, bar_h=0.92, shadow=False, hit=None))
    minis = [film.add(Print("P01", -1300, 1250, 1050, rot=-4, t_in=-0.7, pin=True, sfx=False)),
             film.add(Print("P02", 0, 1150, 1000, rot=2.5, t_in=-0.6, pin=True, sfx=False)),
             film.add(Print("P04", 1300, 1250, 900, rot=4, t_in=-0.5, pin=True, sfx=False))]
    film.add(BigText("EVERY SCREEN. ONE RULE.", 0, 2700, 300, T(1, "same") - 0.1, rgb=(244, 238, 226), type_on=0.5, hit=None, t_out=E(3)))
    film.add(Stamp("THE HARD WAY", 0, 1450, size=330, rot=-9, t_in=T(2, "hard"), t_out=E(3)))

    shot(0.0, 0, -200, 1.12, -0.6)
    shot(1.4, 0, 150, 1.02, 0.3)
    shot(E(1) + 0.2, 0, 500, 0.98, 0.0)
    shot(T(2, "hard") + 0.25, 0, 900, 1.05, -0.4)

    # ================================================= NEWS (3): 1918 front page, the headline
    film.add(YearRoll(0, Y_NEWS - 2300, 520, 1890, 1918, L(3) - 0.15, dur=0.8))
    film.add(Flash(L(3) - 0.05, 0.45))
    news = film.add(Print("P01", 0, Y_NEWS, 2800, rot=-1.2, t_in=L(3) + 0.05, label="THE NEW YORK TIMES · NOV 11, 1918",
                          label_t=L(3) + 0.6))
    hx, hy = doc.on(news, 0.5, 0.118)
    film.add(PenMark("highlight", hx, hy, 2500, 0, t_in=T(3, "headline") - 0.2, dur=0.5, width=150, rot=-1.2, rgb=HILITE))
    film.add(Stamp("HEADLINE", 650, Y_NEWS + 900, size=300, rot=-10, t_in=T(3, "biggest")))
    a = doc.on(news, 0.22, 0.118); b = doc.on(news, 0.78, 0.118)
    film.add(Magnifier(news, (a[0], a[1] + 40), (b[0], b[1] + 40), 470, 1.9, T(3, "whole") - 0.1, T(3, "biggest") - T(3, "whole") + 0.2, T(3, "biggest") + 0.2))
    film.add(FilmDamage((-2600, Y_NEWS - 3000, 5200, 5600), L(3), E(3) + 0.2, 0.7))

    shot(L(3) - 0.3, 0, Y_NEWS - 1700, 0.95, 0.4)
    shot(L(3) + 0.6, 0, Y_NEWS - 900, 1.08, -0.5)
    shot(T(3, "headline") + 0.2, 0, hy + 200, 1.35, -0.8)
    shot(T(3, "biggest") + 0.2, 300, Y_NEWS + 300, 1.05, 0.2)
    shot(E(3) - 0.1, 200, Y_NEWS + 500, 0.98, 0.5)

    # ================================================= FILM (4-6): trailers trailed, then moved to the front
    sx = -750
    top = Y_FILM - 2100
    film.add(BigText("THE SILENT ERA", 0, top - 800, 360, L(4) - 0.2, rgb=(244, 238, 226)))
    strip = film.add(FilmStrip(sx, top, L(4), T(6, "front") - 0.25))
    film.add(Flash(L(4) - 0.08, 0.4))
    film.add(FilmDamage((-2700, top - 1600, 5400, 7400), L(4) - 0.1, E(6) + 0.2, 1.0))
    film.add(PenMark("ellipse", sx, top + 3 * 1050, 1700, 1150, t_in=T(4, "film") - 0.15, dur=0.45, width=24, rgb=(236, 230, 220), t_out=L(6)))
    film.add(PenMark("arrow", sx + 760, top + 3.5 * 1050, 950, 260, t_in=T(4, "after") - 0.1, dur=0.5, width=26, rot=90, rgb=(244, 238, 226), t_out=L(6)))
    film.add(BigText("AFTER", sx + 1750, top + 3 * 1050 + 140, 300, T(4, "after"), rgb=(244, 238, 226), t_out=L(6)))
    film.add(BigText("TRAILER", sx + 1750, top + 4 * 1050 + 120, 330, T(5, "trailers") - 0.15, rgb=DARK, bar=HILITE, bar_h=0.92,
                     shadow=False, t_out=L(6) + 0.2))
    film.add(BigText("1930s", sx + 1750, top - 50, 420, T(6, "1930") - 0.1, rgb=DARK, bar=HILITE, bar_h=0.92, shadow=False))
    film.add(PenMark("arrow", sx + 760, top + 2 * 1050, 4000, -380, t_in=T(6, "front") - 0.25, dur=0.6, width=26, rot=-90, rgb=HILITE, t_out=E(6)))
    film.add(Print("P03", sx + 1750, top + 1900, 1400, rot=3, t_in=T(6, "more") - 0.1, label="GRAUMAN'S EGYPTIAN, 1926",
                   label_t=T(6, "more") + 0.4))

    shot(L(4) - 0.35, 0, top - 300, 0.95, -0.3)
    shot(L(4) + 0.5, 0, top + 1300, 0.9, 0.3)
    shot(T(4, "after") + 0.3, 0, top + 3 * 1050, 1.0, -0.4)
    shot(L(5) + 0.2, 100, top + 3.6 * 1050, 1.05, 0.3)
    shot(T(6, "front"), 0, top + 1300, 0.86, -0.2)
    shot(T(6, "more") + 0.4, 300, top + 1500, 0.92, 0.3)
    shot(E(6) - 0.1, 300, top + 1700, 0.9, 0.0)

    # ================================================= TV (7-8): 1941, ten seconds
    film.add(YearRoll(0, Y_TV - 2400, 700, 1918, 1941, L(7) - 0.05, dur=T(7, "1941") - L(7) + 0.45))
    film.add(Flash(L(7) - 0.06, 0.4))
    film.add(BigText("JULY 1, 1941  ·  NEW YORK", 0, Y_TV - 1450, 150, T(7, "america") - 0.1, font="mono", rgb=(236, 228, 210), type_on=0.6, grunge=False))
    film.add(BigText("FIRST TV AD IN AMERICA", 0, Y_TV - 1750, 215, T(7, "first") - 0.05, rgb=(244, 238, 226), type_on=0.5))
    film.add(Print("P05", 1150, Y_TV + 2150, 1250, rot=4, t_in=T(7, "america"), sfx=False))
    tv = film.add(Print("P04", -620, Y_TV + 150, 1900, rot=-1.5, t_in=L(7) + 0.15, label="RCA TELEVISION, 1939", label_t=T(7, "america")))
    film.add(TVScreen(tv, doc, T(7, "tv") - 0.15, T(7, "ad") + 0.25))
    watch = film.add(WatchFace(1150, Y_TV - 550, 470, T(7, "ran") - 0.2, T(7, "10"), E(8) - T(7, "10")))
    film.add(Counter(1150, Y_TV + 750, 700, 10, T(7, "10") - 0.1, dur=0.5, caption="SECONDS", rgb=(244, 238, 226)))
    film.add(Stamp("10 SECONDS", -620, Y_TV + 900, size=290, rot=-8, t_in=T(8, "watch") - 0.05))

    shot(L(7) - 0.4, 0, Y_TV - 2700, 1.1, 0.5)
    shot(T(7, "first") + 0.2, 0, Y_TV - 1700, 1.0, -0.3)
    shot(T(7, "america") + 0.2, -200, Y_TV - 300, 0.92, 0.2)
    shot(T(7, "10") + 0.15, 350, Y_TV, 1.04, -0.5)
    shot(L(8) + 0.3, 400, Y_TV + 100, 1.0, 0.3)
    shot(T(8, "watch") + 0.2, 0, Y_TV + 400, 0.96, -0.2)

    # ================================================= TODAY (9-10): about three seconds, then the thumb
    film.add(BigText("TODAY", 0, Y_NOW - 2600, 760, T(9, "today") - 0.1, rgb=WHITE, bar=PINK, bar_h=0.92, shadow=False, t_out=L(11)))
    phone = film.add(Phone(0, Y_NOW + 200, 1650, T(9, "today") + 0.1, T(10, "moves") - 0.1))
    film.add(Flash(L(9) - 0.05, 0.5))
    film.add(FeedScroll(0, Y_NOW + 200, T(9, "today") + 0.3, T(10, "moves") - 0.1, L(11) + 0.4))
    t3 = T(9, "three")
    for k, (n, tt) in enumerate((("3", t3), ("2", t3 + 0.5), ("1", T(10, "before")))):
        film.add(BigText(n, 1450, Y_NOW - 900, 1100, tt - 0.05, t_out=tt + 0.35 if k < 2 else T(10, "moves") + 0.2,
                         rgb=WHITE, bar=PINK, bar_h=0.92, shadow=False, hit=0.5))

    shot(L(9) - 0.12, 0, Y_NOW - 2700, 1.05, -0.4)
    shot(T(9, "today") + 0.35, 0, Y_NOW - 1700, 0.98, 0.2)
    shot(t3 + 0.1, 250, Y_NOW - 400, 1.0, -0.3)
    shot(T(10, "moves") + 0.1, 100, Y_NOW + 100, 1.04, 0.3)
    shot(E(10), 0, Y_NOW, 0.98, 0.0)

    # ================================================= PULL BACK (11): they all tested live
    for k, (pr, w) in enumerate(zip(minis, ("tested", "live", "audience"))):
        film.add(Stamp("TESTED LIVE", pr.x, pr.y + 80, size=235, rot=-12 + 9 * k, t_in=T(11, w) - 0.05, shake=k == 0))
    shot(L(11) - 0.15, 0, 4200, 0.5, 0.0, strength=0.2)
    shot(L(11) + 0.35, 0, 1300, 1.0, -0.4, strength=0.35)
    shot(E(11) + 0.15, 0, 1250, 1.04, 0.3, strength=0.35)

    # ================================================= TEST FIRST (12) + CREEDOM (13) + sign-off
    film.add(Stamp("TEST FIRST", 0, Y_NOW - 2700, size=420, rot=-8, rgb=PINK, t_in=T(12, "have") - 0.05, t_out=L(13) + 0.1))
    film.add(HookScan(phone, L(13) + 0.2, L(14) + 0.1, E(13)))
    film.add(Flash(L(14) - 0.05, 0.35))
    film.add(AnalyzerCard(0, Y_NOW + 1500, 3100, T(14, "cred") - 0.15, T(14, "scored") - 0.1, T(14, "hook") - 0.05, T(14, "post") - 0.1))
    film.add(EndLine(0, Y_NOW + 3700, 330, E(14) + 0.15))

    shot(L(12) + 0.15, 0, Y_NOW - 1500, 0.95, -0.3)
    shot(T(12, "have") + 0.25, 0, Y_NOW - 700, 1.0, 0.2)
    shot(L(13) + 0.35, 0, Y_NOW - 150, 0.92, -0.3)
    shot(T(13, "tested") + 0.1, 0, Y_NOW - 50, 0.97, 0.3)
    shot(E(13) - 0.1, 0, Y_NOW + 50, 1.0, -0.2)
    shot(T(14, "cred") + 0.3, 0, Y_NOW + 1700, 0.98, -0.2)
    shot(T(14, "scored") + 0.2, 0, Y_NOW + 1850, 1.04, 0.2)
    shot(E(14), 0, Y_NOW + 2200, 0.95, 0.0)
    shot(film.duration, 0, Y_NOW + 2350, 0.93, 0.0)
    return film
