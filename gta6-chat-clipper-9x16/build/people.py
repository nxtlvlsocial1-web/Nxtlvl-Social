"""Paper cut-out people for the GTA 6 chat-clipper Vox cut (owner, v3: "don't keep that single robot mascot, build
people types as per the frame requirements").

person(pid, look, ...) returns one hand-cut paper bust as SVG (viewBox 600 x 900, cut straight at the bottom so it can
sit on the frame edge or behind a prop). Every shape is cut with slightly wobbly edges and carries an offset shadow.

Animatable parts (select them as "#pid .class"):
  .armL / .armR   whole arm incl. the prop in its hand; rotate with svgOrigin ARM_L / ARM_R
  .head           head, face, hair, accessories; rotate with svgOrigin HEAD
  .e_n .e_w .e_h .e_t .e_c     eyes: normal, wide, happy, tired, closed      (EYES)
  .m_s .m_g .m_o .m_f .m_w     mouth: smile, grin, open shout, flat, small o (MOUTHS)
  .b_n .b_up .b_dn             brows: normal, raised, worried                (BROWS)
"""
import math
import random

R = random.Random(11)
INK = "#14213D"
SHADOW = "rgba(20,33,61,.32)"
ARM_L, ARM_R, HEAD = "155 520", "445 520", "300 430"
EYES = ("e_n", "e_w", "e_h", "e_t", "e_c")
MOUTHS = ("m_s", "m_g", "m_o", "m_f", "m_w")
BROWS = ("b_n", "b_up", "b_dn")


def jit(v, a):
    return v + R.uniform(-a, a)


def poly(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def cut_rect(x, y, w, h, r=0, a=1.6, step=34):
    pts = []
    r = min(r, w / 2, h / 2)

    def edge(x0, y0, x1, y1):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            t = i / n
            pts.append((jit(x0 + (x1 - x0) * t, a), jit(y0 + (y1 - y0) * t, a)))

    def arc(cx, cy, a0):
        for k in range(5):
            ang = math.radians(a0 + k * 18)
            pts.append((jit(cx + r * math.cos(ang), a * .6), jit(cy + r * math.sin(ang), a * .6)))

    edge(x + r, y, x + w - r, y)
    if r:
        arc(x + w - r, y + r, -90)
    edge(x + w, y + r, x + w, y + h - r)
    if r:
        arc(x + w - r, y + h - r, 0)
    edge(x + w - r, y + h, x + r, y + h)
    if r:
        arc(x + r, y + h - r, 90)
    edge(x, y + h - r, x, y + r)
    if r:
        arc(x + r, y + r, 180)
    return poly(pts)


def cut_ellipse(cx, cy, rx, ry, a=1.3, n=44):
    return poly([(jit(cx + rx * math.cos(2 * math.pi * k / n), a), jit(cy + ry * math.sin(2 * math.pi * k / n), a)) for k in range(n)])


class Paper:
    """shapes rendered twice: an offset shadow layer, then the coloured paper"""

    def __init__(self, dx=6, dy=8):
        self.items, self.dx, self.dy = [], dx, dy

    def add(self, kind, fill, *args, extra="", **kw):
        pts = cut_rect(*args, **kw) if kind == "rect" else cut_ellipse(*args, **kw) if kind == "ell" else args[0]
        self.items.append((pts, fill, extra))
        return self

    def raw(self, svg):
        self.items.append((None, None, svg))
        return self

    def svg(self, shadow=True):
        sh = "".join(f'<polygon points="{p}"/>' for p, f, e in self.items if p) if shadow else ""
        body = "".join((f'<polygon points="{p}" fill="{f}" {e}/>' if p else e) for p, f, e in self.items)
        return (f'<g transform="translate({self.dx},{self.dy})" fill="{SHADOW}">{sh}</g>' if shadow else "") + body


def shade(hex_, k=.82):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * k), int(g * k), int(b * k))


# ------------------------------------------------------------------ props held in a hand (hand at 0,0; arm points +y)
def prop_svg(name, rot=0):
    p = Paper(4, 6)
    if name == "mag":
        p.add("rect", INK, -10, 10, 20, 110, r=8)
        p.raw(f'<circle cx="0" cy="182" r="64" fill="rgba(255,255,255,.42)" stroke="{INK}" stroke-width="13"/>'
              f'<path d="M-30 160 Q-20 140 4 136" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>')
    elif name == "pointer":
        p.add("rect", "#9a6631", -7, -10, 14, 300, r=6)
        p.add("ell", "#B8312A", 0, 296, 14, 14)
    elif name == "scissors":
        p.raw(f'<circle cx="-22" cy="-6" r="26" fill="none" stroke="#B8312A" stroke-width="12"/><circle cx="26" cy="-6" r="26" fill="none" stroke="#B8312A" stroke-width="12"/>')
        p.add("poly", "#c9d2e3", poly([(-8, 14), (6, 14), (-30, 250), (-40, 246)]))
        p.add("poly", "#e6ebf5", poly([(8, 14), (-6, 14), (40, 250), (30, 254)]))
        p.add("ell", INK, 0, 22, 9, 9)
    elif name == "phone":
        p.add("rect", INK, -52, -96, 104, 192, r=18)
        p.add("rect", "#ffffff", -42, -82, 84, 160, r=10)
        p.add("rect", "#7a2ffb", -34, -70, 68, 18, r=6)
        p.add("rect", "#F2C230", -34, -44, 50, 14, r=6)
        p.add("rect", "#cfd6e6", -34, -22, 60, 14, r=6)
    elif name == "drink":
        p.add("poly", "#3ef0ff", poly([(-38, -70), (38, -70), (28, 50), (-28, 50)]), extra='opacity=".9"')
        p.add("rect", "#ff4fa3", -36, -40, 72, 20, r=4)
        p.raw(f'<path d="M10 -70 L34 -126" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
              f'<path d="M-6 -78 Q-40 -128 -70 -80 Z" fill="#F2C230" stroke="{INK}" stroke-width="4"/>')
    elif name == "controller":
        p.add("rect", "#2b2f3a", -70, -34, 140, 68, r=34)
        p.add("ell", "#3ef0ff", 34, -4, 9, 9)
        p.add("ell", "#ff4fa3", 50, 12, 9, 9)
        p.add("rect", "#cfd6e6", -50, -6, 34, 10, r=4)
        p.add("rect", "#cfd6e6", -38, -18, 10, 34, r=4)
    else:
        return ""
    return f'<g transform="rotate({rot})">{p.svg()}</g>'


# ------------------------------------------------------------------ the bust
def _arm(side, look, prop=None, prop_rot=0):
    sleeve, skin = look["top"], look["skin"]
    long_sleeve = look.get("sleeves", "short") == "long"
    x0 = 410 if side == "R" else 120
    hx = 445 if side == "R" else 155
    p = Paper()
    p.add("rect", sleeve, x0, 488, 70, 186, r=34)
    p.add("rect", sleeve if long_sleeve else skin, x0 + 6, 640, 58, 150, r=28)
    if long_sleeve:
        p.add("rect", shade(sleeve), x0 + 4, 770, 62, 20, r=8)
    hand = Paper()
    hand.add("ell", skin, hx, 794, 33, 32)
    pr = f'<g transform="translate({hx} 794)">{prop_svg(prop, prop_rot)}</g>' if prop else ""
    if prop in ("phone", "controller", "drink"):      # held from behind: the hand sits under the object
        return f'<g class="arm{side}">{p.svg()}{hand.svg()}{pr}</g>'
    return f'<g class="arm{side}">{p.svg()}{pr}{hand.svg()}</g>'


def _hair_back(look):
    s, c = look["hair_style"], look["hair"]
    p = Paper()
    if s == "long":
        p.add("rect", c, 172, 200, 256, 360, r=112)
    elif s == "bun":
        p.add("ell", c, 300, 160, 50, 44)
    elif s == "pony":
        p.add("ell", c, 420, 300, 42, 96)
    elif s == "curly":
        for k in range(16):
            a = math.pi * (0.85 + 1.3 * k / 15)
            p.add("ell", c, 300 + 128 * math.cos(a), 270 + 120 * math.sin(a), R.uniform(44, 56), R.uniform(44, 56))
        p.add("ell", c, 300, 250, 130, 110)
    if look.get("top_style") == "hoodie":
        p.add("ell", shade(look["top"], .88), 300, 470, 150, 62)
    return p.svg()


def _hair_front(look):
    s, c = look["hair_style"], look["hair"]
    p = Paper(3, 4)
    if s in ("short", "bun", "pony", "long"):
        p.add("ell", c, 300, 224, 108, 54)
        p.add("ell", c, 236 if s != "short" else 360, 252, 52, 30)
        if s == "long":
            p.add("rect", c, 186, 230, 34, 150, r=17)
            p.add("rect", c, 380, 230, 34, 150, r=17)
    elif s == "buzz":
        p.add("ell", c, 300, 214, 100, 42)
    elif s == "curly":
        for k in range(9):
            p.add("ell", c, 212 + k * 22, 214 + 10 * math.sin(k), 30, 28)
    elif s == "cap":
        p.add("ell", look.get("cap", "#B8312A"), 300, 212, 110, 58)
        p.add("rect", shade(look.get("cap", "#B8312A")), 172, 246, 256, 28, r=14)
        p.add("ell", "#fff", 300, 196, 16, 12)
    elif s == "beanie":
        p.add("rect", look.get("cap", "#F2C230"), 190, 150, 220, 110, r=55)
        p.add("rect", shade(look.get("cap", "#F2C230")), 184, 232, 232, 40, r=16)
        p.add("ell", look.get("cap", "#F2C230"), 300, 148, 26, 24)
    return p.svg()


def _torso(look):
    top, skin, sty = look["top"], look["skin"], look.get("top_style", "tee")
    p = Paper()
    p.add("rect", top, 120, 470, 360, 330, r=110)
    p.add("rect", top, 120, 640, 360, 262, r=0, a=1.0)
    if sty == "tee":
        p.add("ell", skin, 300, 478, 52, 30)
    elif sty == "hoodie":
        p.add("ell", skin, 300, 474, 46, 24)
        p.raw(f'<path d="M282 500 L276 590 M318 500 L324 590" stroke="{shade(top, .6)}" stroke-width="7" stroke-linecap="round"/>')
        p.add("rect", shade(top, .88), 200, 720, 200, 110, r=30)
    elif sty == "blazer":
        p.add("poly", look.get("shirt", "#FBF7EE"), poly([(250, 468), (350, 468), (330, 900), (270, 900)]))
        p.add("poly", shade(top, .8), poly([(250, 468), (300, 560), (262, 640), (214, 520)]))
        p.add("poly", shade(top, .8), poly([(350, 468), (300, 560), (338, 640), (386, 520)]))
    elif sty == "apron":
        p.add("ell", skin, 300, 478, 52, 30)
        p.add("rect", look.get("apron", "#F1E6D0"), 210, 560, 180, 342, r=20)
        p.raw(f'<path d="M222 566 L250 486 M378 566 L350 486" stroke="{look.get("apron", "#F1E6D0")}" stroke-width="12"/>')
        p.add("rect", shade(look.get("apron", "#F1E6D0")), 250, 650, 100, 60, r=10)
    if look.get("tag"):
        p.raw(f'<text x="300" y="{690 if sty != "blazer" else 760}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="54" fill="{look.get("tag_ink", "#FBF7EE")}">{look["tag"]}</text>')
    return p.svg()


def _face(look):
    skin = look["skin"]
    o = {k: 0 for k in EYES + MOUTHS + BROWS}
    for k in (look.get("eyes", "e_n"), look.get("mouth", "m_s"), look.get("brows", "b_n")):
        o[k] = 1
    nose = shade(skin, .78)
    f = [f'<path d="M300 326 Q312 346 296 352" stroke="{nose}" stroke-width="6" fill="none" stroke-linecap="round"/>',
         f'<ellipse cx="236" cy="356" rx="20" ry="11" fill="#F28AA8" opacity=".45"/><ellipse cx="364" cy="356" rx="20" ry="11" fill="#F28AA8" opacity=".45"/>',
         # eyes
         f'<g class="e_n" opacity="{o["e_n"]}"><ellipse cx="262" cy="318" rx="10" ry="14" fill="{INK}"/><ellipse cx="338" cy="318" rx="10" ry="14" fill="{INK}"/>'
         f'<circle cx="265" cy="313" r="3.5" fill="#fff"/><circle cx="341" cy="313" r="3.5" fill="#fff"/></g>',
         f'<g class="e_w" opacity="{o["e_w"]}"><ellipse cx="260" cy="316" rx="19" ry="22" fill="#fff" stroke="{INK}" stroke-width="5"/><ellipse cx="340" cy="316" rx="19" ry="22" fill="#fff" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="262" cy="320" r="8" fill="{INK}"/><circle cx="338" cy="320" r="8" fill="{INK}"/></g>',
         f'<g class="e_h" opacity="{o["e_h"]}"><path d="M246 324 Q262 300 278 324 M322 324 Q338 300 354 324" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/></g>',
         f'<g class="e_t" opacity="{o["e_t"]}"><path d="M248 318 Q262 330 276 318 Z M324 318 Q338 330 352 318 Z" fill="{INK}"/>'
         f'<path d="M244 316 H280 M320 316 H356" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
         f'<path d="M248 340 Q262 348 276 340 M324 340 Q338 348 352 340" stroke="{shade(skin, .7)}" stroke-width="5" fill="none" stroke-linecap="round"/></g>',
         f'<g class="e_c" opacity="{o["e_c"]}"><path d="M246 316 Q262 330 278 316 M322 316 Q338 330 354 316" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/></g>',
         # brows
         f'<path class="b_n" opacity="{o["b_n"]}" d="M244 288 L278 283 M322 283 L356 288" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
         f'<path class="b_up" opacity="{o["b_up"]}" d="M242 276 Q260 262 280 270 M320 270 Q340 262 358 276" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>',
         f'<path class="b_dn" opacity="{o["b_dn"]}" d="M244 280 L278 292 M322 292 L356 280" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>']
    if look.get("beard"):
        b = Paper(2, 3)
        b.add("poly", look["hair"], poly([(206, 330), (222, 392), (262, 430), (300, 440), (338, 430), (378, 392), (394, 330), (370, 372), (330, 392), (270, 392), (230, 372)]))
        b.add("ell", look["hair"], 300, 360, 40, 12)
        f.append(b.svg())
    mouth_ink = INK if not look.get("beard") else "#3a1010"
    f += [f'<path class="m_s" opacity="{o["m_s"]}" d="M274 372 Q300 394 326 372" stroke="{mouth_ink}" stroke-width="7" fill="none" stroke-linecap="round"/>',
          f'<g class="m_g" opacity="{o["m_g"]}"><path d="M262 366 Q300 420 338 366 Z" fill="{mouth_ink}"/><path d="M270 370 H330 L324 380 H276 Z" fill="#fff"/></g>',
          f'<g class="m_o" opacity="{o["m_o"]}"><ellipse cx="300" cy="382" rx="26" ry="30" fill="{mouth_ink}"/><ellipse cx="300" cy="398" rx="15" ry="9" fill="#e0607a"/></g>',
          f'<path class="m_f" opacity="{o["m_f"]}" d="M280 380 H320" stroke="{mouth_ink}" stroke-width="7" stroke-linecap="round"/>',
          f'<ellipse class="m_w" opacity="{o["m_w"]}" cx="300" cy="380" rx="11" ry="13" fill="{mouth_ink}"/>']
    return "".join(f)


def _acc(look):
    out = []
    acc = look.get("acc", ())
    c = look.get("acc_color", "#7a2ffb")
    if "headset" in acc:
        out.append(f'<path d="M186 310 Q184 156 300 152 Q416 156 414 310" stroke="{INK}" stroke-width="16" fill="none"/>'
                   f'<rect x="168" y="282" width="44" height="76" rx="20" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                   f'<rect x="388" y="282" width="44" height="76" rx="20" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                   f'<path d="M196 350 Q210 404 262 396" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="266" cy="396" r="10" fill="{INK}"/>')
    if "neckphones" in acc:
        out.append(f'<path d="M222 470 Q300 536 378 470" stroke="{INK}" stroke-width="12" fill="none"/>'
                   f'<ellipse cx="220" cy="462" rx="30" ry="24" fill="{c}" stroke="{INK}" stroke-width="5"/><ellipse cx="380" cy="462" rx="30" ry="24" fill="{c}" stroke="{INK}" stroke-width="5"/>')
    if "glasses" in acc:
        out.append(f'<g fill="none" stroke="{INK}" stroke-width="6"><circle cx="261" cy="318" r="27"/><circle cx="339" cy="318" r="27"/><path d="M288 316 Q300 308 312 316"/></g>')
    return "".join(out)


def _shades():
    return (f'<g class="shades" opacity="0"><rect x="230" y="296" width="60" height="40" rx="16" fill="{INK}"/><rect x="310" y="296" width="60" height="40" rx="16" fill="{INK}"/>'
            f'<path d="M290 310 H310" stroke="{INK}" stroke-width="7"/><path d="M240 306 L256 304 M320 306 L336 304" stroke="#ff4fa3" stroke-width="6" stroke-linecap="round"/></g>')


def person(pid, look, propL=None, propR=None, rotL=0, rotR=0, width=440, style=""):
    """one paper bust; wrapper div id = pid (used for show/hide and moves)"""
    head = Paper()
    head.add("ell", look["skin"], 195, 320, 17, 25)
    head.add("ell", look["skin"], 405, 320, 17, 25)
    head.add("ell", look["skin"], 300, 300, 106, 120)
    neck = Paper()
    neck.add("rect", shade(look["skin"], .9), 266, 386, 68, 100, r=26)
    svg = (f'<svg class="psv" viewBox="0 0 600 900">{_hair_back(look)}{neck.svg()}{_torso(look)}'
           f'{_arm("L", look, propL, rotL)}{_arm("R", look, propR, rotR)}'
           f'<g class="head">{head.svg()}{_face(look)}{_hair_front(look)}{_acc(look)}{_shades()}</g></svg>')
    return f'<div class="per" id="{pid}" style="width:{width}px;{style}">{svg}</div>'


# ------------------------------------------------------------------ the cast: one look per role, as the shots need
CAST = {
    # S1, S7: the clipper who used to scrub six-hour VODs (tired hoodie, headphones round the neck)
    "clipper": dict(skin="#B5764E", hair="#1d1a22", hair_style="short", top="#2f3e66", top_style="hoodie", sleeves="long",
                    acc=("neckphones",), acc_color="#ff4fa3", eyes="e_t", mouth="m_f", brows="b_dn"),
    # S1: the chat viewer who already found the moment
    "viewer_a": dict(skin="#F1C7A1", hair="#6b3e22", hair_style="bun", top="#F2C230", acc=("headset",), acc_color="#3ef0ff", eyes="e_h", mouth="m_g", brows="b_up"),
    # S2: three viewers losing it
    "viewer_b": dict(skin="#8A5434", hair="#1d1a22", hair_style="curly", top="#ff4fa3", eyes="e_w", mouth="m_o", brows="b_up"),
    "viewer_c": dict(skin="#E2B08A", hair="#1d1a22", hair_style="cap", cap="#B8312A", top="#3a86ff", eyes="e_w", mouth="m_o", brows="b_up"),
    "viewer_d": dict(skin="#C68A62", hair="#2a1f3d", hair_style="long", top="#2a9d8f", acc=("glasses",), eyes="e_w", mouth="m_o", brows="b_up"),
    # S3: the one who reads the graph (blazer, pointer)
    "analyst": dict(skin="#5E3A24", hair="#1d1a22", hair_style="pony", top="#B8312A", top_style="blazer", sleeves="long", shirt="#FBF7EE",
                    eyes="e_n", mouth="m_s", brows="b_n"),
    # S4: the creator who asked Claude for the tool (beanie, beard)
    "builder": dict(skin="#D9A07A", hair="#6b3e22", hair_style="beanie", cap="#F2C230", top="#14213D", top_style="hoodie", sleeves="long",
                    beard=True, eyes="e_n", mouth="m_s", brows="b_n"),
    # S5: the editor with the scissors
    "editor": dict(skin="#F6D3B8", hair="#c9853f", hair_style="short", top="#7a2ffb", top_style="apron", apron="#F1E6D0", eyes="e_n", mouth="m_g", brows="b_n"),
    # S6: the viewer who reacts late, and the clipper rewinding
    "late": dict(skin="#B5764E", hair="#2a1f3d", hair_style="buzz", top="#e76f51", sleeves="long", eyes="e_c", mouth="m_f", brows="b_n"),
    "rewinder": dict(skin="#8A5434", hair="#1d1a22", hair_style="long", top="#3ef0ff", acc=("headset",), acc_color="#ff4fa3", eyes="e_n", mouth="m_s", brows="b_n"),
    # S7: the couch of chat watching the streams
    "couch1": dict(skin="#F1C7A1", hair="#1d1a22", hair_style="short", top="#ff4fa3", eyes="e_n", mouth="m_s"),
    "couch2": dict(skin="#5E3A24", hair="#1d1a22", hair_style="curly", top="#F2C230", eyes="e_w", mouth="m_o", brows="b_up"),
    "couch3": dict(skin="#D9A07A", hair="#c9853f", hair_style="bun", top="#2a9d8f", eyes="e_h", mouth="m_g"),
    # S8: the host of the CTA (waves, phone in the other hand)
    "host": dict(skin="#C68A62", hair="#3b2418", hair_style="long", top="#F2C230", top_style="tee", eyes="e_h", mouth="m_g", brows="b_up"),
}
