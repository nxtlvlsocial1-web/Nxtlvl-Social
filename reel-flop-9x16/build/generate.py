"""Reel-flop explainer, 9:16 (1080x1920, 30 fps): "Your reel didn't flop because of the algorithm."

Owner's brief: an explainer from their script card, no @ handle anywhere (the CTA is only in the script), a minimal
white-and-black gradient ground, one red accent (picked: "3-second autopsy" concept, one red accent, no brand).

The idea: a reel lives or dies in its first 3 seconds, so the video acts it out. Problems play on the light (white) side,
each fix and each big line on the dark (black) side: an iris wipe flips the ground on every beat. Red is kept for the
moments a reel dies (the strike-through, the 0 on the countdown, "killing", the swipe-away, the scroll-past, "too late").
Every word appears only when it is spoken (plan/words.json, from build/vo_pick.py). Mock reels in a phone show each
mistake failing, then fixed; no usernames, handles or logos.

python3 build/generate.py  ->  index.html, plan/sfx_events.json
(needs fontTools + brotli for the text fit: /root/tts/.venv/bin/python build/generate.py)
"""
import json
import os

from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
WORDS = json.load(open(os.path.join(ROOT, "plan", "words.json")))
DUR = round(WORDS[-1]["t1"] + 1.7, 2)          # the CTA holds ~1.7 s after the last word
INK, PAPER, RED = "#0b0b0b", "#f6f6f6", "#ff2a2a"
GREY_L, GREY_D = "#6f6f6f", "#9c9c9c"           # secondary text on light / dark
A, SFX = [], []
MAXW = 920

# ---------------------------------------------------------------- text measuring (Inter, the weights used)
_F = {}


def text_w(s, size, weight, ls):
    if weight not in _F:
        f = TTFont(os.path.join(ROOT, "assets", "fonts", f"inter-latin-{weight}-normal.woff2"))
        _F[weight] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    cmap, hm, upm = _F[weight]
    return sum(hm[cmap.get(ord(c), cmap[ord("n")])][0] for c in s) / upm * size + ls * size * (len(s) - 1)


STYLE = {"big": (132, 800, -.035), "mid": (92, 800, -.03), "sm": (60, 600, -.01)}


def js(s):
    A.append("      " + s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def W(line, i, key="t0"):
    ws = [w for w in WORDS if w["line"] == line]
    return ws[i][key]


def words_of(line):
    return [w for w in WORDS if w["line"] == line]


# ---------------------------------------------------------------- words that appear as they are spoken
def title(tid, line, rows, top, scheme="light", start=0, t_out=None, extra_cls=""):
    """rows: [(style, "display text")]; display words pair one by one with the line's spoken words from `start`.
    *word* marks the red accent. Each word rises in, sharp, on its own spoken time; the block drifts up slowly while
    on screen and leaves (if t_out) blurred and lifted."""
    ws = words_of(line)
    k = start
    html = [f'<div class="tt {scheme} {extra_cls}" id="{tid}" style="top:{top}px">']
    first = ws[start]["t0"]
    for r, (style, text) in enumerate(rows):
        size, weight, ls = STYLE[style]
        plain = text.replace("*", "").replace("~", "")
        size = min(size, int(MAXW / text_w(plain, 1, weight, ls)))
        html.append(f'<div class="ln {style}" style="font-size:{size}px">')
        for j, word in enumerate(text.split(" ")):
            red, stk = word.startswith("*"), word.startswith("~")
            word = word.replace("*", "").replace("~", "")
            wid = f"{tid}_{r}_{j}"
            inner = f'{word}<i class="stk" id="{wid}s"></i>' if stk else word
            html.append(f'<span class="w{" red" if red else ""}" id="{wid}">{inner}</span>')
            t = ws[k]["t0"]
            js(f'tl.fromTo("#{wid}", {{opacity: 0, yPercent: 45, filter: "blur(10px)"}}, {{opacity: 1, yPercent: 0, filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {t - .04:.3f});')
            k += 1
        html.append('</div>')
    html.append('</div>')
    js(f'tl.set("#{tid}", {{opacity: 1}}, {first - .05:.3f});')
    end = t_out if t_out else DUR
    js(f'tl.fromTo("#{tid}", {{y: 0}}, {{y: -16, duration: {end - first + .3:.3f}, ease: "none", immediateRender: false}}, {first - .05:.3f});')
    if t_out:
        js(f'tl.to("#{tid}", {{opacity: 0, yPercent: -12, filter: "blur(10px)", duration: .3, ease: "power2.in"}}, {t_out:.3f});')
    return "".join(html)


def kicker(kid, text, top, t, t_out, scheme="light"):
    js(f'tl.fromTo("#{kid}", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: .35, ease: "power3.out", immediateRender: false}}, {t:.3f});')
    js(f'tl.to("#{kid}", {{opacity: 0, filter: "blur(6px)", duration: .25, ease: "power2.in"}}, {t_out:.3f});')
    return f'<div class="kick {scheme}" id="{kid}" style="top:{top}px">{text}</div>'


def show(sel, t, d=.4, y=24, ease="expo.out", extra=""):
    js(f'tl.fromTo("{sel}", {{opacity: 0, y: {y}{", " + extra.split("|")[0] if extra else ""}}}, {{opacity: 1, y: 0{", " + extra.split("|")[1] if extra else ""}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def hide(sel, t, d=.3):
    js(f'tl.to("{sel}", {{opacity: 0, filter: "blur(8px)", duration: {d}, ease: "power2.in"}}, {t:.3f});')


def font_metrics(weight=800):
    f = TTFont(os.path.join(ROOT, "assets", "fonts", f"inter-latin-{weight}-normal.woff2"))
    hh, upm = f["hhea"], f["head"].unitsPerEm
    return hh.ascent / upm, -hh.descent / upm, f


def shard_points(n=150):
    """Start points inside the letters of "algorithm." (where the caption draws it) and end points inside a giant "3"
    (where #bign draws it), both from the real font outlines rasterised with PIL. Returns (starts, targets, (x, top))."""
    import random

    from PIL import Image, ImageDraw, ImageFont
    asc, desc, f = font_metrics(800)
    ttf = os.path.join(ROOT, "cache", "inter-800.ttf")
    if not os.path.exists(ttf):
        os.makedirs(os.path.dirname(ttf), exist_ok=True)
        f.flavor = None
        f.save(ttf)
    upm = f["head"].unitsPerEm

    def base(top, size, lh):
        return top + ((lh - (asc + desc)) / 2 + asc) * size

    def sample(text, size, x, baseline, k, seed):
        im = Image.new("L", (FW, FH), 0)
        ImageDraw.Draw(im).text((x, baseline), text, font=ImageFont.truetype(ttf, size), fill=255, anchor="ls")
        px = [(i % FW, i // FW) for i, v in enumerate(im.getdata()) if v > 128]
        r = random.Random(seed)
        return r.sample(px, k)

    # caption row 4 of #t1 (top 600: big, big, sm, big)
    big, sm = STYLE["big"][0], STYLE["sm"][0]
    row4 = 600 + 2 * big * 1.07 + sm * 1.3
    starts = sample("algorithm.", big, 80, base(row4, big, 1.07), n, 3)
    # the giant numeral: font-size 1100, line-height 1, centred; its digit top at y 690
    size = 1100
    adv = f["hmtx"][f.getBestCmap()[ord("3")]][0] / upm * size
    glyf_top = f["glyf"][f.getBestCmap()[ord("3")]].yMax / upm * size if "glyf" in f else .73 * size
    top = round(690 - (base(0, size, 1.0) - glyf_top))
    targets = sample("3", size, 540 - adv / 2, base(top, size, 1.0), n, 5)
    key = lambda p: p[0] + .35 * p[1]    # noqa: E731
    return sorted(starts, key=key), sorted(targets, key=key), (540 - adv / 2, top)


def fake_reel_html():
    """Frame 0: an ordinary-looking reel, full screen (no username: an avatar dot and blank bars), and the next reel
    under it for the fake swipe."""
    icon = {
        "heart": '<path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"/>',
        "comment": '<path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.2A8 8 0 1 1 20 12z"/>',
        "share": '<path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/>',
        "save": '<path d="M6 3.5h12v17l-6-4.2-6 4.2z"/>',
    }
    acts = "".join(f'<div class="fa"><svg viewBox="0 0 24 24">{icon[k]}</svg><span>{n}</span></div>'
                   for k, n in [("heart", "1,204"), ("comment", "86"), ("share", "41"), ("save", "")])
    reel = (f'<div class="fk" id="fk1"><div class="fksh" id="fkSh"><i class="fkh"></i><i class="fkb"></i></div>'
            f'<!--CAPTION--><div id="fkAct">{acts}</div>'
            f'<div id="fkMeta"><i class="fkav"></i><i class="fkbar b1"></i><i class="fkbar b2"></i><i class="fkbar b3"></i></div>'
            f'<div class="fkpb"><i id="fkPb"></i></div></div>')
    nxt = ('<div class="fk" id="fk2"><div class="fksh s2"><i class="fkh"></i><i class="fkb"></i></div>'
           '<div id="fkMeta2"><i class="fkav"></i><i class="fkbar b1"></i><i class="fkbar b2"></i></div></div>')
    return (f'<div id="fake"><div id="fkS">{reel}{nxt}</div><div id="fkThumb"></div>'
            f'<div id="almost"><i class="dot"></i>you almost scrolled.</div></div>')


# ---------------------------------------------------------------- the ground: iris flips light <-> dark
def flip(t, x, y, to_dark):
    a, b = ("0px", "2400px") if to_dark else ("2400px", "0px")
    js(f'tl.fromTo("#bgD", {{clipPath: "circle({a} at {x}px {y}px)"}}, {{clipPath: "circle({b} at {x}px {y}px)", duration: .62, ease: "expo.inOut", immediateRender: false}}, {t:.3f});')
    # the persistent 3-second pill follows the ground
    if to_dark:
        js(f'tl.to("#tp", {{color: "#f2f2f2", backgroundColor: "rgba(255,255,255,.07)", borderColor: "rgba(255,255,255,.16)", duration: .4}}, {t + .15:.3f});')
    else:
        js(f'tl.to("#tp", {{color: "{INK}", backgroundColor: "rgba(255,255,255,.6)", borderColor: "rgba(0,0,0,.1)", duration: .4}}, {t + .15:.3f});')
    sfx("whoosh_big" if to_dark else "whoosh", t + .05)


# ================================================================= scenes
def scenes():
    H = []
    L = lambda l, i, k="t0": W(l, i, k)    # noqa: E731

    # ---- S1 hook (owner: "try something miraculous in the first 6-7 seconds", picked the fourth-wall fake swipe +
    # the shatter + the full-screen countdown). Frame 0 is an ordinary-looking reel, full screen, already playing (no
    # username anywhere); its on-screen text is the voice, word by word. On "didn't" an invisible thumb swipes it away on
    # the viewer's own screen, the next reel shows, then it snaps back with "you almost scrolled."
    H.append(fake_reel_html())
    t_sw = L("l01", 2) + .1
    js(f'tl.fromTo("#fkThumb", {{opacity: 0, scale: .7}}, {{opacity: .9, scale: 1, duration: .16, ease: "power2.out", immediateRender: false}}, {t_sw - .18:.3f});')
    js(f'tl.to("#fkS, #fkThumb", {{y: -1050, duration: .42, ease: "power2.inOut"}}, {t_sw:.3f});')
    js(f'tl.to("#fkThumb", {{opacity: 0, duration: .12}}, {t_sw + .46:.3f});')
    js(f'tl.to("#fkS", {{y: 0, duration: .75, ease: "elastic.out(1, .6)"}}, {t_sw + .5:.3f});')
    sfx("whoosh", t_sw + .02)
    sfx("swish", t_sw + .5)
    t_alm = t_sw + .62
    js(f'tl.fromTo("#almost", {{opacity: 0, scale: .6, y: 20}}, {{opacity: 1, scale: 1, y: 0, duration: .4, ease: "back.out(2)", immediateRender: false}}, {t_alm:.3f});')
    sfx("error", t_alm)
    js(f'tl.fromTo("#fkSh", {{scale: 1}}, {{scale: 1.07, duration: 3, ease: "none", immediateRender: false}}, 0);')
    js(f'tl.fromTo("#fkPb", {{scaleX: 0}}, {{scaleX: .32, duration: 3, ease: "none", immediateRender: false}}, 0);')
    H_title = title("t1", "l01", [("big", "Your reel"), ("big", "didn't flop"), ("sm", "because of the"), ("big", "~algorithm.")], 600, scheme="dark fk")
    H[-1] = H[-1].replace("<!--CAPTION-->", H_title)
    a_end = L("l01", 7, "t1")
    js(f'tl.fromTo("#t1_3_0s", {{scaleX: 0}}, {{scaleX: 1, duration: .24, ease: "power3.inOut", immediateRender: false}}, {a_end - .1:.3f});')
    js(f'tl.to("#t1_3_0", {{color: "#a9a9a9", duration: .2}}, {a_end - .05:.3f});')
    sfx("scratch", a_end - .08)

    # "algorithm." shatters: the struck word breaks into shards that burst out, then rush together into a giant red 3
    t_x = a_end + .16
    js(f'tl.to("#almost", {{opacity: 0, duration: .2}}, {t_x - .1:.3f});')
    js(f'tl.set("#t1_3_0", {{opacity: 0}}, {t_x:.3f});')
    js(f'tl.to("#fake", {{opacity: 0, scale: .94, duration: .45, ease: "power2.inOut"}}, {t_x:.3f});')
    starts, targets, (bx, btop) = shard_points()
    import random
    rnd = random.Random(7)
    cx = sum(p[0] for p in starts) / len(starts)
    cy = sum(p[1] for p in starts) / len(starts)
    sh = []
    t_g = t_x + .42                 # gather
    t_3 = t_g + .5                  # the solid 3
    for k, ((sx, sy), (tx, ty)) in enumerate(zip(starts, targets)):
        size = rnd.randint(16, 30)
        pts = [(rnd.randint(0, 40), rnd.randint(0, 30)), (rnd.randint(60, 100), rnd.randint(0, 45)), (rnd.randint(20, 80), rnd.randint(70, 100))]
        poly = ", ".join(f"{a}% {b}%" for a, b in pts)
        col = RED if rnd.random() < .35 else "#b5b5b5"
        sh.append(f'<i class="shd" id="sh{k}" style="left:{sx - size / 2:.0f}px;top:{sy - size / 2:.0f}px;width:{size}px;height:{size}px;'
                  f'clip-path:polygon({poly});background:{col}"></i>')
        ang = __import__("math").atan2(sy - cy, sx - cx) + rnd.uniform(-.6, .6)
        dist = rnd.uniform(140, 460)
        ex, ey = __import__("math").cos(ang) * dist, __import__("math").sin(ang) * dist + rnd.uniform(-80, 40)
        rot = rnd.uniform(-260, 260)
        js(f'tl.fromTo("#sh{k}", {{opacity: 1, x: 0, y: 0, rotation: 0}}, {{opacity: 1, x: {ex:.0f}, y: {ey:.0f}, rotation: {rot:.0f}, duration: .42, ease: "expo.out", immediateRender: false}}, {t_x:.3f});')
        d = rnd.uniform(0, .1)
        js(f'tl.to("#sh{k}", {{x: {tx - sx:.0f}, y: {ty - sy:.0f}, rotation: {rnd.uniform(-30, 30):.0f}, backgroundColor: "{RED}", duration: {.46 - d:.2f}, ease: "expo.inOut"}}, {t_g + d:.3f});')
    js(f'tl.to(".shd", {{opacity: 0, duration: .18}}, {t_3:.3f});')
    H.append(f'<div id="shards">{"".join(sh)}</div>')
    sfx("glitch", t_x)
    sfx("whoosh_big", t_x + .02)
    sfx("rise", t_g)
    sfx("hit", t_3 - .04)

    # ---- S2 peak: "It flopped in the first three seconds." The 3 fills the screen; 3, 2, 1 cut the ground
    # white / black / white with hard cuts, 0 lands red on black as the beat drops
    t_flip1 = L("l02", 6, "t1") + .06
    H.append(title("t2", "l02", [("big", "It flopped"), ("mid", "in the first 3 seconds.")], 380, t_out=t_flip1 - .02))
    H.append(f'<div id="bign" style="top:{btop}px">&#8203;3</div>')
    js(f'tl.fromTo("#bign", {{opacity: 0}}, {{opacity: 1, duration: .16, immediateRender: false}}, {t_3 - .06:.3f});')
    js(f'tl.fromTo("#bign", {{scale: 1.06}}, {{scale: 1, duration: .5, ease: "expo.out", immediateRender: false}}, {t_3 - .06:.3f});')
    c2, c0 = L("l02", 5) - .02, t_flip1
    c1 = (c2 + c0) / 2
    for t, n, dark, col in [(c2, 2, True, "#ffffff"), (c1, 1, False, INK), (c0, 0, True, RED)]:
        js(f'tl.set("#bgD", {{clipPath: "circle({2400 if dark else 0}px at 540px 1100px)"}}, {t:.3f});')
        js(f'tl.set("#bign", {{textContent: "\\u200b{n}", color: "{col}"}}, {t:.3f});')
        if n:
            js(f'tl.set("#t2", {{color: "{"#ffffff" if dark else INK}"}}, {t:.3f});')
        js(f'tl.fromTo("#bign", {{scale: 1.12}}, {{scale: 1, duration: .3, ease: "expo.out", immediateRender: false}}, {t:.3f});')
        sfx("count" if n else "glitch", t)
    # the dead "0" shrinks away; the persistent 3-second pill takes over at the top
    t_s3 = L("l03", 0)
    js(f'tl.to("#bign", {{opacity: 0, scale: .1, y: -760, duration: .5, ease: "power3.in"}}, {t_s3 - .25:.3f});')
    H.append('<div id="tp"><i class="dot"></i>FIRST 3 SECONDS</div>')
    js(f'tl.fromTo("#tp", {{opacity: 0, y: -14}}, {{opacity: 1, y: 0, duration: .4, ease: "expo.out", immediateRender: false}}, {t_s3 + .2:.3f});')

    # ---- S3 (dark): "Here are three mistakes killing your views." + three numbered glass slots
    t_s4 = L("l04", 0) - .14
    H.append(title("t3", "l03", [("sm", "Here are"), ("big", "3 mistakes"), ("mid", "*killing* your views.")], 470, scheme="dark", t_out=t_s4))
    slots = "".join(f'<div class="slot" id="sl{k}"><span>{k + 1}</span></div>' for k in range(3))
    H.append(f'<div id="slots">{slots}</div>')
    for k in range(3):
        tt = L("l03", 2) + k * .13
        js(f'tl.fromTo("#sl{k}", {{opacity: 0, y: 60, rotationX: -35, transformPerspective: 900}}, {{opacity: 1, y: 0, rotationX: 0, transformPerspective: 900, duration: .55, ease: "expo.out", immediateRender: false}}, {tt:.3f});')
        sfx("pop", tt)
    # on "views" the slots tilt down a touch: views falling
    js(f'tl.to("#slots", {{y: 26, duration: .4, ease: "power2.out"}}, {L("l03", 6):.3f});')
    sfx("drop", L("l03", 6))
    js(f'tl.to("#sl1, #sl2", {{opacity: 0, filter: "blur(8px)", duration: .3, ease: "power2.in"}}, {t_s4:.3f});')
    js(f'tl.to("#sl0", {{scale: 2.4, opacity: 0, duration: .5, ease: "power3.in"}}, {t_s4:.3f});')

    # ---- the phone (S4, S5): mock reels, no usernames
    H.append(phone_html())
    flip(t_s4 + .02, 230, 1210, False)
    show("#phone", t_s4 + .25, d=.6, y=120)
    sfx("swish", t_s4 + .25)
    js(f'tl.fromTo("#phone", {{rotation: -2}}, {{rotation: 0, duration: .9, ease: "expo.out", immediateRender: false}}, {t_s4 + .25:.3f});')

    # ---- S4a mistake 1: "One: your hook is a greeting." The reel opens on "Hey guys, so today..."
    t_m1b = L("l05", 0) - .1
    H.append(kicker("k1", "MISTAKE 1", 346, L("l04", 0) - .04, t_m1b))
    H.append(title("t4", "l04", [("mid", "Your hook is"), ("big", "a greeting.")], 410, start=1, t_out=t_m1b))
    t_cap = L("l04", 4) - .1
    cap = "Hey guys, so today..."
    js(f'tl.set("#cap1", {{opacity: 1}}, {t_cap:.3f});')
    for i in range(1, len(cap) + 1):
        js(f'tl.set("#cap1t", {{textContent: {json.dumps(cap[:i])}}}, {t_cap + i * .035:.3f});')
        if i % 4 == 1:
            sfx("type", t_cap + i * .035)
    js(f'tl.fromTo("#pb1", {{scaleX: 0}}, {{scaleX: .035, duration: 2.6, ease: "none", immediateRender: false}}, {L("l04", 1):.3f});')

    # "Nobody stays for 'Hey guys.'": a thumb flicks it away before 0:03
    H.append(title("t4b", "l05", [("mid", "Nobody stays for"), ("big", "“Hey guys.”")], 410, t_out=L("l06", 0) - .12))
    t_sw = L("l05", 3)
    js(f'tl.fromTo("#thumb", {{opacity: 0, x: 40, y: 140}}, {{opacity: .92, x: 0, y: 0, duration: .3, ease: "power3.out", immediateRender: false}}, {t_sw - .35:.3f});')
    js(f'tl.to("#thumb", {{y: -330, opacity: 0, duration: .32, ease: "power3.in"}}, {t_sw + .02:.3f});')
    js(f'tl.to("#reel1", {{yPercent: -100, duration: .38, ease: "power3.in"}}, {t_sw + .06:.3f});')
    js(f'tl.fromTo("#reel1b", {{yPercent: 100, opacity: 1}}, {{yPercent: 0, opacity: 1, duration: .38, ease: "power3.in", immediateRender: false}}, {t_sw + .06:.3f});')
    sfx("whoosh", t_sw)
    js(f'tl.fromTo("#gone1", {{opacity: 0, scale: .85}}, {{opacity: 1, scale: 1, duration: .32, ease: "back.out(1.7)", immediateRender: false}}, {t_sw + .42:.3f});')
    sfx("error", t_sw + .42)

    # ---- S4b fix 1 (dark): "Start with the result." The next reel opens on the result itself
    t_f1 = L("l06", 0) - .1
    flip(t_f1, 540, 1100, True)
    js(f'tl.to("#phone", {{boxShadow: "0 0 0 3px rgba(255,255,255,.22), 0 40px 90px rgba(0,0,0,.55)", duration: .4}}, {t_f1 + .1:.3f});')
    H.append(title("t5", "l06", [("mid", "Start with"), ("big", "the result.")], 410, scheme="dark", t_out=L("l07", 0) - .12))
    js(f'tl.fromTo("#reel2", {{yPercent: 100, opacity: 1}}, {{yPercent: 0, opacity: 1, duration: .45, ease: "expo.out", immediateRender: false}}, {t_f1 + .1:.3f});')
    t_res = L("l06", 3) - .05
    js(f'tl.to("#gone1", {{opacity: 0, duration: .2}}, {t_res - .2:.3f});')
    js(f'tl.fromTo("#res1", {{opacity: 0, scale: .6, filter: "blur(10px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .45, ease: "back.out(1.6)", immediateRender: false}}, {t_res:.3f});')
    js(f'tl.fromTo("#res2", {{opacity: 0, y: 16}}, {{opacity: 1, y: 0, duration: .35, ease: "power3.out", immediateRender: false}}, {t_res + .14:.3f});')
    sfx("hit", t_res)
    # its progress bar runs straight past the 3-second mark
    js(f'tl.fromTo("#pb2", {{scaleX: 0}}, {{scaleX: .22, duration: 1.5, ease: "none", immediateRender: false}}, {t_f1 + .1:.3f});')
    t_pass = t_f1 + .1 + 1.5 * (.1 / .22)
    js(f'tl.to("#mk2", {{backgroundColor: "#ffffff", scaleY: 1.6, duration: .2}}, {t_pass:.3f});')
    js(f'tl.fromTo("#kept", {{opacity: 0, y: 10}}, {{opacity: 1, y: 0, duration: .3, ease: "power3.out", immediateRender: false}}, {t_pass:.3f});')
    sfx("ding", t_pass)

    # ---- S5a mistake 2 (light): "Two: your first frame is still." A feed; the first frame is a still photo
    t_m2 = L("l07", 0) - .12
    flip(t_m2, 540, 1100, False)
    js(f'tl.to("#phone", {{boxShadow: "0 0 0 0px rgba(255,255,255,0), 0 40px 90px rgba(0,0,0,.28)", duration: .4}}, {t_m2 + .1:.3f});')
    t_m2b = L("l08", 0) - .1
    H.append(kicker("k2", "MISTAKE 2", 346, t_m2 + .08, t_m2b))
    H.append(title("t6", "l07", [("mid", "Your first frame"), ("big", "is still.")], 410, start=1, t_out=t_m2b))
    js(f'tl.to("#kept, #res1, #res2", {{opacity: 0, duration: .2}}, {t_m2:.3f});')
    js(f'tl.fromTo("#feed", {{yPercent: 100, opacity: 1}}, {{yPercent: 0, opacity: 1, duration: .5, ease: "expo.out", immediateRender: false}}, {t_m2 + .1:.3f});')
    sfx("swish", t_m2 + .1)
    js(f'tl.fromTo("#paused", {{opacity: 0, scale: .7}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(1.7)", immediateRender: false}}, {L("l07", 5):.3f});')
    sfx("click", L("l07", 5))
    # "If nothing moves, thumbs keep scrolling." The music drops out on "nothing moves", then the feed whips past it
    H.append(title("t6b", "l08", [("mid", "If nothing moves,"), ("mid", "thumbs keep scrolling.")], 410, t_out=L("l09", 0) - .14))
    js(f'tl.fromTo("#nomove", {{opacity: 0, x: -20}}, {{opacity: 1, x: 0, duration: .3, ease: "power3.out", immediateRender: false}}, {L("l08", 2):.3f});')
    sfx("alert", L("l08", 2))
    t_sc = L("l08", 3)
    js(f'tl.fromTo("#thumb", {{opacity: 0, x: 40, y: 140}}, {{opacity: .92, x: 0, y: 0, duration: .25, ease: "power3.out", immediateRender: false}}, {t_sc - .28:.3f});')
    js(f'tl.to("#thumb", {{y: -330, opacity: 0, duration: .3, ease: "power3.in"}}, {t_sc:.3f});')
    js(f'tl.to("#nomove", {{opacity: 0, duration: .15}}, {t_sc:.3f});')
    js(f'tl.to("#strip", {{yPercent: -66.667, duration: .85, ease: "expo.inOut"}}, {t_sc:.3f});')
    js(f'tl.fromTo("#strip", {{filter: "blur(0px)"}}, {{filter: "blur(9px)", duration: .3, ease: "power2.in", immediateRender: false}}, {t_sc + .1:.3f});')
    js(f'tl.to("#strip", {{filter: "blur(0px)", duration: .3, ease: "power2.out"}}, {t_sc + .5:.3f});')
    sfx("whoosh", t_sc + .05)
    sfx("swish", t_sc + .35)
    js(f'tl.fromTo("#gone2", {{opacity: 0, scale: .85}}, {{opacity: 1, scale: 1, duration: .3, ease: "back.out(1.7)", immediateRender: false}}, {t_sc + .62:.3f});')
    sfx("error", t_sc + .62)
    t_m3 = L("l09", 0) - .14
    js(f'tl.to("#phone", {{opacity: 0, y: 140, rotation: 3, duration: .4, ease: "power3.in"}}, {t_m3 + .55:.3f});')

    # ---- S6a mistake 3 (light): "Three: you explain before you show." Two cards in the wrong order
    t_m3b = L("l10", 0) - .1
    H.append(kicker("k3", "MISTAKE 3", 346, t_m3 + .1, t_m3b))
    H.append(title("t7", "l09", [("mid", "You explain"), ("big", "before you show.")], 410, start=1, t_out=t_m3b))
    H.append('<div class="card" id="cEx"><span class="cn" id="cExn">1</span><div><b>EXPLAIN</b><i>how you did it</i></div></div>'
             '<div class="card" id="cSh"><span class="cn" id="cShn">2</span><div><b>SHOW</b><i>the result</i></div></div>'
             '<div id="late"><i class="dot"></i>viewer gone before this</div>')
    show("#cEx", L("l09", 2) - .05, d=.45, y=50)
    sfx("pop", L("l09", 2) - .05)
    show("#cSh", L("l09", 5) - .05, d=.45, y=50)
    sfx("pop", L("l09", 5) - .05)
    js(f'tl.fromTo("#late", {{opacity: 0, x: -24}}, {{opacity: 1, x: 0, duration: .25, ease: "power3.out", immediateRender: false}}, {L("l09", 5) + .1:.3f});')
    sfx("error", L("l09", 5) + .1)

    # ---- S6b fix 3 (dark): "Show the result first, then explain how you got it." The cards swap
    t_f3 = L("l10", 0) - .1
    flip(t_f3, 540, 1100, True)
    H.append(title("t8", "l10", [("mid", "Show the result first,"), ("sm", "then explain how you got it.")], 410, scheme="dark", t_out=L("l11", 0) - .14))
    js(f'tl.to("#late", {{opacity: 0, duration: .2}}, {t_f3:.3f});')
    t_swap = t_f3 + .3
    js(f'tl.to("#cSh", {{y: -240, x: 0, duration: .6, ease: "expo.inOut"}}, {t_swap:.3f});')
    js(f'tl.to("#cSh", {{keyframes: {{x: [0, 70, 0]}}, duration: .6, ease: "sine.inOut"}}, {t_swap:.3f});')
    js(f'tl.to("#cEx", {{y: 240, duration: .6, ease: "expo.inOut"}}, {t_swap:.3f});')
    js(f'tl.to("#cEx", {{keyframes: {{x: [0, -70, 0]}}, duration: .6, ease: "sine.inOut"}}, {t_swap:.3f});')
    sfx("swish", t_swap)
    js(f'tl.set("#cShn", {{textContent: "1"}}, {t_swap + .3:.3f}); tl.set("#cExn", {{textContent: "2"}}, {t_swap + .3:.3f});')
    js(f'tl.to("#cSh", {{backgroundColor: "#ffffff", color: "{INK}", borderColor: "#ffffff", duration: .35}}, {t_swap + .55:.3f});')
    js(f'tl.to("#cShn", {{backgroundColor: "{INK}", color: "#ffffff", duration: .35}}, {t_swap + .55:.3f});')
    js(f'tl.to("#cEx", {{backgroundColor: "rgba(255,255,255,.06)", color: "#f2f2f2", borderColor: "rgba(255,255,255,.16)", duration: .35}}, {t_f3 + .1:.3f});')
    js(f'tl.to("#cExn", {{backgroundColor: "rgba(255,255,255,.14)", color: "#ffffff", duration: .35}}, {t_f3 + .1:.3f});')
    js(f'tl.to("#cSh", {{backgroundColor: "rgba(255,255,255,.06)", color: "#f2f2f2", borderColor: "rgba(255,255,255,.16)", duration: .3}}, {t_f3 + .1:.3f});')
    js(f'tl.fromTo("#chk", {{opacity: 0, scale: .4}}, {{opacity: 1, scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false}}, {t_swap + .65:.3f});')
    sfx("success", t_swap + .65)
    H.append('<div id="chk"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" /></svg></div>')

    # ---- S7 (light): "Fix these three and watch your next reel." Checklist + views climbing
    t_s7 = L("l11", 0) - .14
    flip(t_s7, 540, 960, False)
    js(f'tl.to("#cEx, #cSh, #chk", {{opacity: 0, filter: "blur(8px)", duration: .3, ease: "power2.in"}}, {t_s7:.3f});')
    H.append(title("t9", "l11", [("big", "Fix these three"), ("sm", "and watch your next reel.")], 380, t_out=L("l12", 0) - .14))
    fixes = ["Start with the result", "Move in frame one", "Show, then explain"]
    rows = "".join(f'<div class="row" id="rw{k}"><span class="rn">{k + 1}</span><b>{t}</b><span class="rc" id="rc{k}">'
                   f'<svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" /></svg></span></div>' for k, t in enumerate(fixes))
    H.append(f'<div id="rows">{rows}</div>')
    for k in range(3):
        tt = L("l11", k) - .04
        show(f"#rw{k}", tt, d=.45, y=40)
        sfx("click", tt)
        js(f'tl.to("#rc{k}", {{backgroundColor: "{INK}", borderColor: "{INK}", duration: .2}}, {tt + .35:.3f});')
        js(f'tl.fromTo("#rc{k} path", {{strokeDashoffset: 30}}, {{strokeDashoffset: 0, duration: .25, ease: "power2.out", immediateRender: false}}, {tt + .35:.3f});')
        sfx("pop", tt + .35)
    H.append('<div id="ctr"><div id="ctrn">312</div><div id="ctrl"><span class="up">&#8593;</span> views on your next reel</div></div>')
    t_c = L("l11", 4) - .05
    show("#ctr", t_c, d=.4, y=30)
    vals = [312, 900, 2400, 5200, 9800, 15400, 22100, 29300, 36100, 41800, 45600, 47600, 48200]
    for i, v in enumerate(vals):
        js(f'tl.set("#ctrn", {{textContent: "{v:,}"}}, {t_c + .1 + i * .075:.3f});')
    sfx("rise", t_c)
    sfx("ding", t_c + .1 + (len(vals) - 1) * .075)

    # ---- S8 CTA (dark): "Save this so you don't forget, and comment HOOK for my list of twenty hooks that work."
    t_s8 = L("l12", 0) - .14
    flip(t_s8, 540, 330, True)
    js(f'tl.to("#rows, #ctr", {{opacity: 0, filter: "blur(8px)", duration: .3, ease: "power2.in"}}, {t_s8:.3f});')
    js(f'tl.to("#tp", {{opacity: 0, y: -14, duration: .3, ease: "power2.in"}}, {t_s8:.3f});')
    H.append('<div id="bkm"><svg viewBox="0 0 24 24"><path id="bkp" d="M6 3.5h12v17l-6-4.2-6 4.2z"/></svg></div>')
    js(f'tl.fromTo("#bkm", {{opacity: 0, scale: .5, y: 20}}, {{opacity: 1, scale: 1, y: 0, duration: .45, ease: "back.out(1.8)", immediateRender: false}}, {L("l12", 0) - .05:.3f});')
    js(f'tl.to("#bkp", {{fill: "#ffffff", duration: .2}}, {L("l12", 1):.3f});')
    sfx("pop", L("l12", 0) - .05)
    H.append(title("t10", "l12", [("big", "Save this"), ("sm", "so you don't forget,")], 420, scheme="dark"))
    H.append(title("t11", "l12", [("sm", "and comment")], 790, scheme="dark", start=6))
    # the comment box types HOOK, then the keyword card lands and holds to the end
    t_in = L("l12", 7) - .1
    H.append('<div id="cbox"><span id="cbt"><span id="cbph">Add a comment...</span><span id="cbk"></span><i id="caret"></i></span>'
             '<span id="send"><svg viewBox="0 0 24 24"><path d="M4 12h14M13 6l6 6-6 6"/></svg></span></div>')
    show("#cbox", t_in, d=.45, y=30)
    sfx("click", t_in)
    t_k = L("l12", 8) - .06
    js(f'tl.set("#cbph", {{display: "none"}}, {t_k:.3f});')
    for i, s in enumerate(["H", "HO", "HOO", "HOOK"]):
        js(f'tl.set("#cbk", {{textContent: "{s}"}}, {t_k + i * .09:.3f});')
        sfx("type", t_k + i * .09)
    js(f'tl.to("#send", {{backgroundColor: "#ffffff", color: "{INK}", duration: .2}}, {t_k + .4:.3f});')
    H.append('<div id="hook">HOOK</div>')
    t_h = t_k + .5
    js(f'tl.fromTo("#hook", {{opacity: 0, scale: .55, y: 40, filter: "blur(12px)"}}, {{opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: .55, ease: "back.out(1.5)", immediateRender: false}}, {t_h:.3f});')
    js(f'tl.fromTo("#hook", {{scale: 1}}, {{scale: 1.035, duration: {DUR - t_h - .55:.3f}, ease: "none", immediateRender: false}}, {t_h + .55:.3f});')
    sfx("hit", t_h)
    sfx("sparkle", t_h + .1)
    H.append(title("t12", "l12", [("sm", "for my list of 20 hooks that work.")], 1390, scheme="dark", start=9))
    return "".join(H)


def phone_html():
    """A phone with four screens: reel 1 (the greeting), the reel after the swipe, reel 2 (the result), the feed."""
    bar = lambda i, mk: (f'<div class="pbar"><i class="pfill" id="pb{i}"></i>'      # noqa: E731
                         f'<i class="mk" id="mk{i}"></i></div>' if mk else f'<div class="pbar"><i class="pfill" id="pb{i}"></i></div>')
    person = '<div class="person"><i class="hd"></i><i class="bd"></i></div>'
    reel1 = (f'<div class="reel" id="reel1"><div class="shot s1">{person}</div>'
             f'<div class="cap" id="cap1"><span id="cap1t"></span></div>{bar(1, True)}</div>')
    reel1b = '<div class="reel" id="reel1b"><div class="shot s2"><i class="ln1"></i><i class="ln2"></i><i class="ln3"></i></div></div>'
    reel2 = (f'<div class="reel" id="reel2"><div class="shot s3">{person}</div>'
             f'<div class="res"><div id="res1">1M views</div><div id="res2">in 3 days. Here\'s how.</div></div>'
             f'<div id="kept">still watching past 0:03</div>{bar(2, True)}</div>')
    still = (f'<div class="fi"><div class="shot s4"><div class="photo"><i class="sun"></i><i class="hill1"></i><i class="hill2"></i></div></div>'
             f'<div id="paused"><i></i><i></i></div><div id="nomove"><i class="dot"></i>nothing moves</div>{bar(3, True)}</div>')
    other = lambda c: f'<div class="fi"><div class="shot {c}"><i class="ln1"></i><i class="ln2"></i><i class="ln3"></i></div></div>'  # noqa: E731
    feed = f'<div class="reel" id="feed"><div id="strip">{still}{other("s5")}{other("s6")}</div></div>'
    gone1 = '<div class="gone" id="gone1"><i class="dot"></i>swiped at 0:01</div>'
    gone2 = '<div class="gone" id="gone2"><i class="dot"></i>scrolled past at 0:00</div>'
    return (f'<div id="phone"><div id="scr">{reel1}{reel1b}{reel2}{feed}{gone1}{gone2}</div>'
            f'<i class="notch"></i><div id="thumb"></div></div>')


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #e9e9e9; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter"; color: {INK}; }}
/* the ground: a white gradient, and a black gradient revealed by the iris */
#bgL, #bgD {{ position: absolute; inset: 0; overflow: hidden; }}
#bgL {{ z-index: 0; background: radial-gradient(130% 85% at 50% 32%, #ffffff 0%, #f3f3f3 42%, #d9d9d9 78%, #c4c4c4 100%); }}
#bgD {{ z-index: 1; background: radial-gradient(130% 85% at 50% 32%, #303030 0%, #151515 45%, #060606 80%, #000 100%);
  clip-path: circle(0px at 540px 1140px); }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(60px); }}
#bgL .blob {{ background: radial-gradient(circle, rgba(0,0,0,.09), rgba(0,0,0,0) 70%); }}
#bgD .blob {{ background: radial-gradient(circle, rgba(255,255,255,.11), rgba(255,255,255,0) 70%); }}
.b1 {{ width: 900px; height: 900px; left: -260px; top: 120px; }}
.b2 {{ width: 760px; height: 760px; left: 520px; top: 1080px; }}
#grain {{ position: absolute; inset: 0; z-index: 2; pointer-events: none; opacity: .06; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
#cam {{ position: absolute; inset: 0; z-index: 3; }}
/* titles: every word on its own spoken time */
.tt {{ position: absolute; left: 80px; right: 80px; text-align: left; opacity: 0; }}
.ln {{ white-space: nowrap; line-height: 1.07; }}
.ln.big, .ln.mid {{ font-weight: 800; letter-spacing: -.035em; }}
.ln.mid {{ letter-spacing: -.03em; }}
.ln.sm {{ font-weight: 600; letter-spacing: -.01em; line-height: 1.3; }}
.tt.light {{ color: {INK}; }} .tt.light .sm {{ color: {GREY_L}; }}
.tt.dark {{ color: #f4f4f4; }} .tt.dark .sm {{ color: {GREY_D}; }}
.w {{ display: inline-block; opacity: 0; margin-right: .24em; padding-bottom: .06em; position: relative; }}
.w .stk {{ position: absolute; left: -.04em; right: -.04em; top: 50%; height: .09em; border-radius: .05em; background: {RED}; transform-origin: left center; transform: scaleX(0); }}
.w.red {{ color: {RED}; }}
.kick {{ position: absolute; left: 80px; width: fit-content; padding: 8px 20px; border-radius: 999px; font-weight: 700; font-size: 28px;
  letter-spacing: .24em; opacity: 0; white-space: nowrap; }}
.kick.light {{ color: {INK}; border: 2px solid rgba(0,0,0,.85); }}
/* frame 0: a dead reel's stats */
.chip {{ position: absolute; top: 420px; left: 80px; width: fit-content; display: flex; align-items: center; gap: 16px; padding: 14px 28px;
  border-radius: 999px; font-size: 34px; font-weight: 700; white-space: nowrap; }}
.chip.light {{ background: rgba(255,255,255,.7); border: 1.5px solid rgba(0,0,0,.08); box-shadow: 0 14px 40px rgba(0,0,0,.08); }}
.play {{ width: 0; height: 0; border-left: 20px solid {INK}; border-top: 12px solid transparent; border-bottom: 12px solid transparent; }}
.redtxt {{ color: {RED}; }}
#strike {{ position: absolute; left: 248px; right: 248px; top: 1020px; height: 12px; border-radius: 6px; background: {RED}; transform-origin: left center;
  opacity: 0; }}
/* the fake reel (frame 0) */
#fake {{ position: absolute; inset: 0; z-index: 4; overflow: hidden; }}
#fkS {{ position: absolute; left: 0; top: 0; width: 100%; height: 200%; }}
.fk {{ position: absolute; left: 0; width: 100%; height: 50%; overflow: hidden; }}
#fk1 {{ top: 0; background: radial-gradient(90% 55% at 50% 40%, #4c4c4c 0%, #262626 55%, #0e0e0e 100%); }}
#fk2 {{ top: 50%; background: radial-gradient(90% 55% at 40% 45%, #6a6a6a 0%, #3a3a3a 55%, #1a1a1a 100%); }}
.fksh {{ position: absolute; inset: 0; transform-origin: 50% 70%; }}
.fkh {{ position: absolute; left: 400px; top: 760px; width: 280px; height: 340px; border-radius: 50%; background: linear-gradient(160deg, #5c5c5c, #353535); }}
.fkb {{ position: absolute; left: 170px; top: 1090px; width: 740px; height: 900px; border-radius: 370px 370px 0 0; background: linear-gradient(170deg, #474747, #222 70%); }}
.fksh.s2 .fkh {{ left: 300px; background: linear-gradient(160deg, #8a8a8a, #555); }}
.fksh.s2 .fkb {{ left: 60px; background: linear-gradient(170deg, #707070, #3a3a3a 70%); }}
.tt.fk {{ text-shadow: 0 4px 30px rgba(0,0,0,.45); }}
#fkAct {{ position: absolute; right: 34px; top: 1150px; display: flex; flex-direction: column; align-items: center; gap: 40px; }}
.fa {{ display: flex; flex-direction: column; align-items: center; gap: 8px; color: #fff; font-weight: 600; font-size: 28px; }}
.fa svg {{ width: 70px; height: 70px; fill: none; stroke: #fff; stroke-width: 1.8; stroke-linejoin: round; stroke-linecap: round; }}
#fkMeta, #fkMeta2 {{ position: absolute; left: 40px; top: 1640px; width: 700px; height: 200px; }}
.fkav {{ position: absolute; left: 0; top: 0; width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #9a9a9a, #5a5a5a); border: 3px solid #fff; }}
.fkbar {{ position: absolute; height: 22px; border-radius: 11px; background: rgba(255,255,255,.55); }}
.fkbar.b1 {{ left: 92px; top: 24px; width: 220px; }}
.fkbar.b2 {{ left: 0; top: 104px; width: 560px; background: rgba(255,255,255,.35); }}
.fkbar.b3 {{ left: 0; top: 144px; width: 380px; background: rgba(255,255,255,.35); }}
.fkpb {{ position: absolute; left: 0; right: 0; bottom: 0; height: 6px; background: rgba(255,255,255,.25); }}
#fkPb {{ position: absolute; inset: 0; background: #fff; transform-origin: left center; transform: scaleX(0); }}
#fkThumb {{ position: absolute; left: 560px; top: 1450px; width: 120px; height: 120px; border-radius: 50%; background: rgba(255,255,255,.88);
  box-shadow: 0 0 0 14px rgba(255,255,255,.2), 0 12px 40px rgba(0,0,0,.4); opacity: 0; }}
#almost {{ position: absolute; top: 420px; left: 80px; width: fit-content; display: flex; align-items: center; gap: 14px; padding: 16px 30px;
  border-radius: 999px; background: {RED}; color: #fff; font-weight: 800; font-size: 44px; letter-spacing: -.01em; white-space: nowrap; opacity: 0;
  box-shadow: 0 18px 50px rgba(255,42,42,.35); }}
#almost .dot {{ background: #fff; }}
/* shards and the giant numeral */
#shards {{ position: absolute; inset: 0; z-index: 6; pointer-events: none; }}
.shd {{ position: absolute; opacity: 0; }}
#bign {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 800; font-size: 1100px; line-height: 1; letter-spacing: 0; color: {RED};
  font-variant-numeric: tabular-nums; opacity: 0; z-index: 1; }}
/* the countdown ring */
#ring {{ position: absolute; left: 330px; top: 930px; width: 420px; height: 420px; opacity: 0; }}
#ring svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
.rtrk {{ fill: none; stroke: rgba(0,0,0,.12); stroke-width: 9; }}
#rfill {{ fill: none; stroke: {INK}; stroke-width: 9; stroke-linecap: round; }}
#rnum {{ position: absolute; inset: 0; display: grid; place-items: center; font-weight: 800; font-size: 230px; letter-spacing: -.05em;
  font-variant-numeric: tabular-nums; color: {INK}; }}
/* the 3-second pill */
#tp {{ position: absolute; top: 268px; left: 0; right: 0; margin-left: auto; margin-right: auto; width: fit-content; display: flex; align-items: center; gap: 12px; padding: 10px 22px;
  border-radius: 999px; font-size: 28px; font-weight: 700; letter-spacing: .2em; white-space: nowrap; color: #f2f2f2;
  background: rgba(255,255,255,.07); border: 1.5px solid rgba(255,255,255,.16); opacity: 0; }}
.dot {{ display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: {RED}; flex: none; }}
/* three slots */
#slots {{ position: absolute; left: 90px; right: 90px; top: 1060px; display: flex; justify-content: space-between; }}
.slot {{ width: 270px; height: 320px; border-radius: 36px; background: rgba(255,255,255,.06); border: 1.5px solid rgba(255,255,255,.16);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.12), 0 30px 60px rgba(0,0,0,.4); display: grid; place-items: center; opacity: 0; }}
.slot span {{ font-weight: 800; font-size: 150px; color: transparent; -webkit-text-stroke: 3px rgba(255,255,255,.7); letter-spacing: -.04em; }}
/* the phone */
#phone {{ position: absolute; left: 315px; top: 700px; width: 450px; height: 800px; border-radius: 64px; background: {INK}; padding: 11px;
  box-shadow: 0 0 0 0 rgba(255,255,255,0), 0 40px 90px rgba(0,0,0,.28); opacity: 0; }}
#scr {{ position: relative; width: 100%; height: 100%; border-radius: 54px; overflow: hidden; background: #1a1a1a; }}
.notch {{ position: absolute; left: 50%; top: 24px; width: 120px; height: 34px; margin-left: -60px; border-radius: 20px; background: #000; z-index: 6; }}
.reel {{ position: absolute; inset: 0; }}
#reel1b, #reel2, #feed {{ opacity: 0; }}
.shot {{ position: absolute; inset: 0; }}
.s1 {{ background: linear-gradient(180deg, #3a3a3a, #232323 60%, #1b1b1b); }}
.s2 {{ background: linear-gradient(180deg, #4b4b4b, #2d2d2d); }}
.s3 {{ background: linear-gradient(180deg, #2e2e2e, #141414 70%); }}
#reel2 .person {{ transform: translateY(150px); }}
.s4 {{ background: #262626; }}
.s5 {{ background: linear-gradient(180deg, #555, #333); }}
.s6 {{ background: linear-gradient(180deg, #3d3d3d, #222); }}
.person .hd {{ position: absolute; left: 165px; top: 250px; width: 100px; height: 120px; border-radius: 50%; background: #5a5a5a; }}
.person .bd {{ position: absolute; left: 100px; top: 380px; width: 230px; height: 420px; border-radius: 115px 115px 0 0; background: #4a4a4a; }}
.ln1, .ln2, .ln3 {{ position: absolute; left: 40px; height: 22px; border-radius: 11px; background: rgba(255,255,255,.16); }}
.ln1 {{ top: 520px; width: 300px; }} .ln2 {{ top: 560px; width: 220px; }} .ln3 {{ top: 600px; width: 260px; }}
.cap {{ position: absolute; left: 30px; right: 30px; top: 470px; text-align: center; opacity: 0; }}
.cap span {{ display: inline-block; min-height: 52px; padding: 8px 16px; border-radius: 12px; background: rgba(0,0,0,.72); color: #fff; font-weight: 700; font-size: 30px; }}
.pbar {{ position: absolute; left: 26px; right: 26px; bottom: 34px; height: 8px; border-radius: 4px; background: rgba(255,255,255,.22); }}
.pfill {{ position: absolute; left: 0; top: 0; bottom: 0; width: 100%; border-radius: 4px; background: #fff; transform-origin: left center; transform: scaleX(0); }}
#pb1, #pb3 {{ background: {RED}; }}
.mk {{ position: absolute; left: 10%; top: -7px; width: 4px; height: 22px; border-radius: 2px; background: {RED}; }}
.res {{ position: absolute; left: 20px; right: 20px; top: 170px; text-align: center; color: #fff; }}
#res1 {{ font-weight: 800; font-size: 84px; letter-spacing: -.04em; opacity: 0; }}
#res2 {{ font-weight: 600; font-size: 30px; color: #cfcfcf; margin-top: 6px; opacity: 0; }}
#kept {{ position: absolute; left: 0; right: 0; bottom: 64px; text-align: center; font-size: 26px; font-weight: 700; color: #fff; opacity: 0; letter-spacing: .02em; }}
#strip {{ position: absolute; left: 0; right: 0; top: 0; height: 300%; }}
.fi {{ position: relative; height: 33.3334%; overflow: hidden; }}
.photo {{ position: absolute; inset: 0; background: linear-gradient(180deg, #8d8d8d, #6a6a6a 55%, #4a4a4a); }}
.sun {{ position: absolute; left: 270px; top: 150px; width: 90px; height: 90px; border-radius: 50%; background: #d8d8d8; }}
.hill1 {{ position: absolute; left: -80px; top: 470px; width: 520px; height: 520px; border-radius: 50%; background: #3e3e3e; }}
.hill2 {{ position: absolute; left: 160px; top: 540px; width: 460px; height: 460px; border-radius: 50%; background: #2c2c2c; }}
#paused {{ position: absolute; left: 50%; top: 50%; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; background: rgba(0,0,0,.55);
  display: flex; align-items: center; justify-content: center; gap: 16px; opacity: 0; }}
#paused i {{ width: 14px; height: 46px; border-radius: 4px; background: #fff; }}
#nomove {{ position: absolute; left: 24px; top: 84px; display: flex; align-items: center; gap: 10px; padding: 8px 16px; border-radius: 999px;
  background: rgba(0,0,0,.7); color: #fff; font-weight: 700; font-size: 26px; opacity: 0; }}
.gone {{ position: absolute; top: 46%; left: 0; right: 0; margin-left: auto; margin-right: auto; width: fit-content; display: flex; align-items: center; gap: 12px; padding: 14px 24px;
  border-radius: 999px; background: #fff; color: {INK}; font-weight: 700; font-size: 30px; white-space: nowrap; opacity: 0;
  box-shadow: 0 16px 40px rgba(0,0,0,.4); z-index: 5; }}
#thumb {{ position: absolute; left: 190px; top: 600px; width: 86px; height: 86px; border-radius: 50%; background: rgba(255,255,255,.85);
  box-shadow: 0 0 0 10px rgba(255,255,255,.18), 0 10px 30px rgba(0,0,0,.35); opacity: 0; z-index: 7; }}
/* explain / show cards */
.card {{ position: absolute; left: 140px; width: 800px; height: 200px; border-radius: 40px; display: flex; align-items: center; gap: 36px; padding: 0 44px;
  background: rgba(255,255,255,.72); border: 1.5px solid rgba(0,0,0,.08); box-shadow: 0 24px 60px rgba(0,0,0,.1); color: {INK}; opacity: 0; }}
#cEx {{ top: 820px; }} #cSh {{ top: 1060px; }}
.cn {{ width: 96px; height: 96px; border-radius: 50%; display: grid; place-items: center; font-weight: 800; font-size: 52px; background: {INK}; color: #fff; flex: none; }}
.card b {{ display: block; font-weight: 800; font-size: 64px; letter-spacing: -.02em; line-height: 1; }}
.card i {{ display: block; font-style: normal; font-weight: 600; font-size: 32px; opacity: .6; margin-top: 8px; }}
#late {{ position: absolute; top: 1290px; left: 0; right: 0; margin-left: auto; margin-right: auto; width: fit-content; display: flex; align-items: center; gap: 12px; padding: 12px 24px;
  border-radius: 999px; border: 2px solid {RED}; color: {RED}; font-weight: 700; font-size: 30px; white-space: nowrap; opacity: 0; }}
#chk {{ position: absolute; left: 816px; top: 846px; width: 96px; height: 96px; border-radius: 50%; background: {INK}; display: grid; place-items: center; opacity: 0; }}
#chk svg {{ width: 56px; height: 56px; fill: none; stroke: #fff; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
/* checklist + counter */
#rows {{ position: absolute; left: 110px; right: 110px; top: 690px; display: flex; flex-direction: column; gap: 26px; }}
.row {{ height: 128px; border-radius: 32px; display: flex; align-items: center; gap: 30px; padding: 0 30px; background: rgba(255,255,255,.72);
  border: 1.5px solid rgba(0,0,0,.08); box-shadow: 0 18px 40px rgba(0,0,0,.08); opacity: 0; }}
.rn {{ width: 64px; height: 64px; border-radius: 50%; border: 3px solid {INK}; display: grid; place-items: center; font-weight: 800; font-size: 34px; flex: none; }}
.row b {{ flex: 1; font-weight: 700; font-size: 46px; letter-spacing: -.02em; white-space: nowrap; }}
.rc {{ width: 64px; height: 64px; border-radius: 50%; border: 3px solid rgba(0,0,0,.25); display: grid; place-items: center; flex: none; }}
.rc svg {{ width: 40px; height: 40px; fill: none; stroke: #fff; stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 30; stroke-dashoffset: 30; }}
#ctr {{ position: absolute; left: 60px; right: 60px; top: 1200px; text-align: center; opacity: 0; }}
#ctrn {{ font-weight: 800; font-size: 170px; letter-spacing: -.05em; line-height: 1; font-variant-numeric: tabular-nums; }}
#ctrl {{ font-weight: 600; font-size: 40px; color: {GREY_L}; margin-top: 6px; }}
.up {{ color: {INK}; font-weight: 800; }}
/* CTA */
#bkm {{ position: absolute; left: 495px; top: 290px; width: 90px; height: 110px; opacity: 0; }}
#bkm svg {{ width: 100%; height: 100%; overflow: visible; }}
#bkp {{ fill: none; stroke: #fff; stroke-width: 1.8; stroke-linejoin: round; }}
#cbox {{ position: absolute; left: 110px; right: 110px; top: 880px; height: 132px; border-radius: 999px; display: flex; align-items: center;
  justify-content: space-between; padding: 0 18px 0 46px; background: rgba(255,255,255,.07); border: 1.5px solid rgba(255,255,255,.2);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.12); opacity: 0; }}
#cbt {{ display: flex; align-items: center; font-size: 46px; font-weight: 700; color: #fff; letter-spacing: .04em; }}
#cbph {{ color: rgba(255,255,255,.45); font-weight: 600; letter-spacing: 0; }}
#caret {{ width: 4px; height: 52px; margin-left: 6px; background: #fff; border-radius: 2px; }}
#send {{ width: 96px; height: 96px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.12); color: #fff; }}
#send svg {{ width: 48px; height: 48px; fill: none; stroke: currentColor; stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round; }}
#hook {{ position: absolute; left: 50%; top: 1080px; margin-left: -330px; width: 660px; height: 250px; border-radius: 60px; background: #fff; color: {INK};
  display: grid; place-items: center; font-weight: 800; font-size: 190px; letter-spacing: -.04em; opacity: 0;
  box-shadow: 0 0 0 10px rgba(255,255,255,.08), 0 40px 120px rgba(255,255,255,.14); }}
"""


def main():
    body = scenes()
    # the ground breathes: two soft blobs drift the whole time on both sides of the iris
    for side in ("L", "D"):
        js(f'tl.to("#bg{side} .b1", {{x: 160, y: -90, duration: {DUR / 2:.2f}, ease: "sine.inOut", repeat: 1, yoyo: true}}, 0);')
        js(f'tl.to("#bg{side} .b2", {{x: -180, y: 70, duration: {DUR / 3:.2f}, ease: "sine.inOut", repeat: 2, yoyo: true}}, 0);')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Reel flop explainer 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="bgL"><i class="blob b1"></i><i class="blob b2"></i></div>
      <div id="bgD"><i class="blob b1"></i><i class="blob b2"></i></div>
      <div id="grain"></div>
      <div id="cam">{body}</div>
      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(sorted(SFX, key=lambda e: e["t"]), open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html, {len(A)} timeline lines, {len(SFX)} sfx cues, {DUR} s")


if __name__ == "__main__":
    main()
