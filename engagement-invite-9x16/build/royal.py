"""Maroon-and-gold royal look for v4 (after the client's card): gold filigree frame, palace spaces the
couples walk through, and the transition pieces (light flare, diamond shatter, petal burst).
All our own drawing.
"""
import math
import random

import art
import elements as el
import figures as fg

GOLD_GRAD = ('<linearGradient id="{id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8a5a12"/>'
             '<stop offset=".35" stop-color="#e9c46a"/><stop offset=".5" stop-color="#fff1b8"/>'
             '<stop offset=".65" stop-color="#d4a017"/><stop offset="1" stop-color="#7a4b0c"/></linearGradient>')


# ------------------------------------------------------------------ filigree
def _scroll(x, y, r, a0, turns, sgn=1):
    """Spiral scroll centre line as a polyline path."""
    pts = []
    for i in range(60):
        t = i / 59
        a = a0 + sgn * t * turns * math.tau
        rr = r * (1 - .78 * t)
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    return "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)


def corner(gid):
    """Top-left corner flourish in a 300 x 520 box (mirror it for the other corners)."""
    r = random.Random(9)
    lace = "".join(f'<path d="M{x} 0 L{x - 160} 160" stroke="url(#{gid})" stroke-width="1" opacity=".35"/>'
                   f'<path d="M{x - 160} 0 L{x} 160" stroke="url(#{gid})" stroke-width="1" opacity=".35"/>'
                   for x in range(0, 300, 16))
    scrolls = "".join(f'<path d="{_scroll(x, y, rr, a, t, s)}" fill="none" stroke="url(#{gid})" stroke-width="{w}" '
                      f'stroke-linecap="round"/>'
                      for x, y, rr, a, t, s, w in [(70, 70, 60, 0, 1.4, 1, 6), (170, 60, 46, 2, 1.2, -1, 5),
                                                   (60, 190, 48, 4, 1.3, 1, 5), (130, 150, 34, 1, 1.1, -1, 4),
                                                   (220, 120, 30, 3, 1.2, 1, 3.5), (60, 300, 36, 5, 1.2, -1, 4)])
    leaves = "".join(art.leaf(round(x), round(y), r.uniform(26, 42), round(r.uniform(0, 360)), col=f"url(#{gid})",
                              vein="#5b3708")
                     for x, y in [(110, 40), (230, 40), (40, 120), (200, 170), (100, 240), (30, 250), (150, 210),
                                  (260, 80), (90, 360), (40, 400)])
    flowers = "".join(el.flower5(x, y, rr, f"url(#{gid})", centre="#7a4b0c")
                      for x, y, rr in [(120, 100, 26), (60, 230, 20), (240, 150, 18), (190, 230, 16)])
    # beaded strand hanging down the side (like the card)
    beads = "".join(f'<ellipse cx="38" cy="{300 + k * 18}" rx="{6 if k % 3 else 9}" ry="7" fill="url(#{gid})"/>'
                    for k in range(12))
    return (f'<g><g clip-path="url(#lc-{gid})">{lace}</g>{scrolls}{leaves}{flowers}'
            f'<path d="M38 290 L38 520" stroke="url(#{gid})" stroke-width="2"/>{beads}'
            f'<path d="M26 520 L38 545 L50 520 Z" fill="url(#{gid})"/></g>')


def side_ornament(gid):
    """Symmetric leaf fan for the middle of the side edges, 120 x 420, centred at (60, 210)."""
    out = []
    for k in range(7):
        a = -60 + k * 20
        out.append(art.leaf(60, 210, 120 - abs(a) * .8, a + 90, col=f"url(#{gid})", vein="#5b3708"))
        out.append(art.leaf(60, 210, 120 - abs(a) * .8, a - 90, col=f"url(#{gid})", vein="#5b3708"))
    out.append(el.flower5(60, 210, 22, f"url(#{gid})", centre="#7a4b0c"))
    out.append(f'<path d="M60 0 C90 80 90 140 60 210 C30 280 30 340 60 420" stroke="url(#{gid})" stroke-width="3" '
               f'fill="none"/>')
    return f'<g>{"".join(out)}</g>'


def card_frame(sid):
    """The card dressing: gold bands top and bottom, four filigree corners, side ornaments."""
    gid = f"gold-{sid}"
    c = corner(gid)
    so = side_ornament(gid)
    return (f'<svg class="frame" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<defs>{GOLD_GRAD.format(id=gid)}<clipPath id="lc-{gid}"><path d="M0 0 H300 C200 40 120 120 0 300 Z"/>'
            f'</clipPath><linearGradient id="band-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" '
            f'stop-color="#e9c46a"/><stop offset="1" stop-color="#b8862b"/></linearGradient></defs>'
            f'<rect class="band-t" x="250" y="0" width="580" height="78" fill="url(#band-{sid})"/>'
            f'<rect class="band-b" x="250" y="1842" width="580" height="78" fill="url(#band-{sid})" transform="rotate(180 540 1881)"/>'
            f'<g class="fr-c1"><g>{c}</g></g>'
            f'<g class="fr-c2"><g transform="translate(1080 0) scale(-1 1)">{c}</g></g>'
            f'<g class="fr-c3"><g transform="translate(0 1920) scale(1 -1)">{c}</g></g>'
            f'<g class="fr-c4"><g transform="translate(1080 1920) scale(-1 -1)">{c}</g></g>'
            f'<g class="fr-s1"><g transform="translate(10 750)">{so}</g></g>'
            f'<g class="fr-s2"><g transform="translate(1070 750) scale(-1 1)">{so}</g></g></svg>')


def card_bg():
    return '<img class="leather" src="assets/img/paper.jpg" width="1080" height="1920" alt="">'


# ------------------------------------------------------------------ palace spaces
def _cusped_arch(x, w, top, bottom, fill, stroke, sw=5):
    """Cusped arch outline from x to x+w; spring at top+0.35w, apex at top."""
    sp = top + w * .45
    pts = []
    for i in range(9):
        t = i / 8
        a = math.pi * (1 - t)
        pts.append((x + w / 2 + math.cos(a) * w / 2, sp - math.sin(a) * (sp - top)))
    d = f"M{x} {bottom} L{x} {sp:.0f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ch = math.hypot(x1 - x0, y1 - y0)
        d += f" A{ch * .6:.0f} {ch * .6:.0f} 0 0 1 {x1:.0f} {y1:.0f}"
    d += f" L{x + w} {bottom} Z"
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def lantern(x, y, s=1.0, cls="lantern"):
    return (f'<g class="{cls}" data-o="{x} {y - 160 * s:.0f}"><path d="M{x} {y - 160 * s:.0f} L{x} {y - 40 * s:.0f}" '
            f'stroke="#d4a017" stroke-width="2"/>'
            f'<g transform="translate({x} {y}) scale({s})">'
            f'<circle r="70" fill="#ffcf6b" opacity=".18"/><circle r="40" fill="#ffd98a" opacity=".22"/>'
            f'<path d="M-22 -40 L22 -40 L30 0 L22 40 L-22 40 L-30 0 Z" fill="#7a1022" stroke="#e9c46a" stroke-width="3"/>'
            f'<path d="M-14 -30 L14 -30 L20 0 L14 30 L-14 30 L-20 0 Z" fill="#ffd166" opacity=".9"/>'
            f'<path d="M-26 -40 L0 -62 L26 -40 Z" fill="#e9c46a"/><path d="M-20 40 L0 58 L20 40 Z" fill="#e9c46a"/>'
            f'</g></g>')


def corridor(sid):
    """Colonnade of cusped gold arches with lanterns, a crimson carpet and marble floor.
    The `.mid` strip is 2400 wide so it can scroll left while the couple walks."""
    gid = f"gc-{sid}"
    arches = "".join(
        _cusped_arch(x, 220, 820, 1540, "#2a0610", f"url(#{gid})", 6) +
        f'<rect x="{x + 222}" y="760" width="80" height="780" fill="#6e1424"/>'
        f'<rect x="{x + 230}" y="760" width="64" height="780" fill="url(#pil-{sid})"/>'
        + lantern(x + 110, 1040, .9)
        for x in range(-40, 2400, 300))
    floor_lines = "".join(f'<path d="M{x} 1640 L{x - 140} 1920" stroke="#c9a46a" stroke-width="2" opacity=".5"/>'
                          for x in range(0, 2600, 120))
    fore = "".join(f'<rect x="{x}" y="0" width="150" height="1920" fill="url(#fp-{sid})"/>'
                   for x in range(-200, 3600, 1300))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<defs>{GOLD_GRAD.format(id=gid)}'
            f'<linearGradient id="pil-{sid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a0b17"/>'
            f'<stop offset=".5" stop-color="#9b1c31"/><stop offset="1" stop-color="#4a0912"/></linearGradient>'
            f'<linearGradient id="fp-{sid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1c0408"/>'
            f'<stop offset=".5" stop-color="#3b0a14"/><stop offset="1" stop-color="#14030a"/></linearGradient>'
            f'<linearGradient id="fl-{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9dcc6"/>'
            f'<stop offset="1" stop-color="#b79f7e"/></linearGradient></defs>'
            f'<g class="mid">{arches}'
            f'<rect x="-100" y="1540" width="2700" height="22" fill="url(#{gid})"/>'
            f'<rect x="-100" y="1562" width="2700" height="358" fill="url(#fl-{sid})"/>{floor_lines}</g>'
            f'<rect x="0" y="1600" width="1080" height="110" fill="#9b1028"/>'
            f'<rect x="0" y="1600" width="1080" height="8" fill="url(#{gid})"/>'
            f'<rect x="0" y="1702" width="1080" height="8" fill="url(#{gid})"/>'
            f'<g class="fore" filter="url(#soft-{sid})">{fore}</g>'
            f'<filter id="soft-{sid}"><feGaussianBlur stdDeviation="8"/></filter></svg>')


def courtyard(sid):
    """Sunset courtyard: maroon-to-amber sky, palace domes, a pool, gold lamp posts."""
    gid = f"gc-{sid}"
    domes = "".join(
        f'<g transform="translate({x} 1230)"><rect x="-90" y="-160" width="180" height="160" fill="#3a0812"/>'
        f'<path d="M-80 -160 C-80 -260 80 -260 80 -160 Z" fill="#3a0812"/>'
        f'<path d="M0 -250 L0 -290" stroke="#e9c46a" stroke-width="5"/>'
        + "".join(f'<path d="M{ax} 0 L{ax} -70 C{ax} -96 {ax + 30} -96 {ax + 30} -70 L{ax + 30} 0 Z" fill="#ffb347" '
                  f'opacity=".55"/>' for ax in (-70, -15, 40)) +
        '</g>' for x in range(80, 2500, 340))
    lamps = "".join(f'<g transform="translate({x} 1600)"><rect x="-5" y="-260" width="10" height="260" fill="url(#{gid})"/>'
                    f'<circle cy="-275" r="22" fill="#ffd98a"/><circle cy="-275" r="60" fill="#ffcf6b" opacity=".2"/></g>'
                    for x in range(150, 2600, 520))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<defs>{GOLD_GRAD.format(id=gid)}<linearGradient id="sun-{sid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#3f0712"/><stop offset=".45" stop-color="#7a1022"/>'
            f'<stop offset=".72" stop-color="#d9480f"/><stop offset=".85" stop-color="#f59f00"/></linearGradient>'
            f'<radialGradient id="sd-{sid}"><stop offset="0" stop-color="#fff3bf"/><stop offset=".3" stop-color="#ffd43b"/>'
            f'<stop offset="1" stop-color="#ffd43b" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#sun-{sid})"/>'
            f'<circle class="sundisc" cx="540" cy="1180" r="260" fill="url(#sd-{sid})"/>'
            f'<g class="mid">{domes}<rect x="-100" y="1230" width="2700" height="40" fill="#2a0610"/>'
            f'<rect x="-100" y="1270" width="2700" height="250" fill="#5a0b17"/>'
            f'<rect x="-100" y="1300" width="2700" height="90" fill="#ff922b" opacity=".35"/>{lamps}</g>'
            f'<rect x="0" y="1520" width="1080" height="400" fill="#e7d3b0"/>'
            f'<rect x="0" y="1600" width="1080" height="110" fill="#9b1028"/>'
            f'<rect x="0" y="1600" width="1080" height="8" fill="url(#{gid})"/>'
            f'<rect x="0" y="1702" width="1080" height="8" fill="url(#{gid})"/></svg>')


def chandelier(x, y, s=1.0):
    drops = "".join(f'<path d="M{dx} 20 L{dx} {50 + abs(dx) % 30}" stroke="#fff6d5" stroke-width="2"/>'
                    f'<circle cx="{dx}" cy="{54 + abs(dx) % 30}" r="5" fill="#fffbe6"/>' for dx in range(-80, 90, 20))
    return (f'<g class="chand" data-o="{x} 0"><path d="M{x} 0 L{x} {y - 40}" stroke="#d4a017" stroke-width="3"/>'
            f'<g transform="translate({x} {y}) scale({s})"><circle r="120" fill="#ffd98a" opacity=".16"/>'
            f'<path d="M-90 0 C-60 30 60 30 90 0" stroke="#e9c46a" stroke-width="6" fill="none"/>'
            f'<path d="M-50 -30 C-30 -10 30 -10 50 -30" stroke="#e9c46a" stroke-width="5" fill="none"/>'
            f'{drops}' + "".join(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#ffd166"/>'
                                 for cx, cy in [(-90, -6), (90, -6), (-50, -36), (50, -36), (0, -50)]) + '</g></g>')


def hall(sid):
    """Durbar hall: ivory walls with gold niches, chandeliers, a crimson carpet."""
    gid = f"gc-{sid}"
    niches = "".join(_cusped_arch(x, 200, 860, 1520, "#f1e2c8", f"url(#{gid})", 5) +
                     f'<path d="M{x + 100} 1180 m-30 0 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0" fill="#ffcf6b" opacity=".25"/>'
                     for x in range(-60, 2500, 280))
    return (f'<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920">'
            f'<defs>{GOLD_GRAD.format(id=gid)}</defs>'
            f'<g class="mid">{niches}<rect x="-100" y="1520" width="2700" height="400" fill="#d9c4a0"/>'
            + "".join(f'<path d="M{x} 1540 L{x - 160} 1920" stroke="#a88a5c" stroke-width="2" opacity=".5"/>'
                      for x in range(0, 2600, 140)) +
            f'</g>{chandelier(150, 780, .9)}{chandelier(930, 780, .9)}'
            f'<rect x="0" y="1600" width="1080" height="110" fill="#9b1028"/>'
            f'<rect x="0" y="1600" width="1080" height="8" fill="url(#{gid})"/>'
            f'<rect x="0" y="1702" width="1080" height="8" fill="url(#{gid})"/></svg>')


# ------------------------------------------------------------------ couples (maroon & gold outfits)
C1 = {"groom": ("#f3e7cf", "#c9973f", "#9b1028", "#efe3cc", "#7a4b0c"),
      "bride": ("#b0122e", "#e9c46a", "#8e0f26", "#f7c6a5", "#e9c46a")}
C2 = {"groom": ("#7a1022", "#e9c46a", "#f3e7cf", "#efe3cc", "#5b3708"),
      "bride": ("#f1c27d", "#b0122e", "#e8a24a", "#fde2e4", "#b0122e")}


def walkers(pal, cls, x, y, s):
    return f'<g class="walk {cls}"><g transform="translate({x} {y}) scale({s})">{fg.couple(pal, cls)}</g></g>'


# ------------------------------------------------------------------ transition pieces
def shards(n=26, seed=3):
    """Diamond shards radiating from the centre (they fly out when the diamond breaks)."""
    r = random.Random(seed)
    out = []
    for i in range(n):
        a = i / n * math.tau + r.uniform(-.1, .1)
        d = r.uniform(20, 120)
        cx, cy = math.cos(a) * d, math.sin(a) * d
        pts = [(cx + r.uniform(-40, 40), cy + r.uniform(-40, 40)) for _ in range(3)]
        tx, ty = math.cos(a) * r.uniform(700, 1200), math.sin(a) * r.uniform(800, 1300)
        out.append(f'<path class="shard" data-tx="{tx:.0f}" data-ty="{ty:.0f}" data-r="{r.uniform(-260, 260):.0f}" '
                   f'd="M{pts[0][0]:.0f} {pts[0][1]:.0f} L{pts[1][0]:.0f} {pts[1][1]:.0f} L{pts[2][0]:.0f} '
                   f'{pts[2][1]:.0f} Z" fill="url(#dia)" stroke="#ffffff" stroke-width="2" opacity=".95"/>')
    return out


def diamond_heart():
    return ('<path d="M0 80 C-60 40 -100 6 -100 -30 C-100 -60 -76 -80 -50 -80 C-26 -80 -8 -64 0 -46 '
            'C8 -64 26 -80 50 -80 C76 -80 100 -60 100 -30 C100 6 60 40 0 80 Z" fill="url(#dia)" stroke="#fff" '
            'stroke-width="4"/>'
            '<path d="M-100 -30 L0 80 L100 -30 M-50 -80 L-30 -30 L0 80 L30 -30 L50 -80 M-100 -30 L100 -30 '
            'M0 -46 L-30 -30 M0 -46 L30 -30" stroke="#ffffff" stroke-width="2.4" fill="none" opacity=".8"/>')


def burst_petals(n=70, seed=12):
    r = random.Random(seed)
    cols = ("#b0122e", "#e11d48", "#8e0f26", "#e9c46a", "#f43f5e")
    out = []
    for i in range(n):
        s = r.uniform(.8, 2.0)
        out.append(f'<div class="bp" data-y="{r.uniform(-200, 2000):.0f}" data-d="{r.uniform(0, .5):.2f}" '
                   f'data-rot="{r.uniform(-400, 400):.0f}"><svg viewBox="0 0 30 40" width="{30 * s:.0f}" '
                   f'height="{40 * s:.0f}"><path d="M15 0 C30 12 26 34 15 40 C4 34 0 12 15 0 Z" '
                   f'fill="{r.choice(cols)}"/></svg></div>')
    return "".join(out)


def gold_dust(n=46, seed=8):
    r = random.Random(seed)
    els, specs = [], []
    for i in range(n):
        x, y, s = r.uniform(0, 1080), r.uniform(200, 1900), r.uniform(3, 8)
        els.append(f'<div class="gd" id="gd{i}" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px">'
                   f'</div>')
        specs.append((i, r.uniform(0, 6), r.uniform(5, 9), r.uniform(-260, -120), r.uniform(-40, 40)))
    return "".join(els), specs


def doors_royal():
    """Maroon-and-gold doors (recoloured versions of the palace doors)."""
    def recolor(svg):
        return (svg.replace("#f6c99a", "#7a1022").replace(art.SAND_D, "#d4a017").replace(art.GOLD_D, "#f2c96b")
                .replace(art.GOLD, "#e9c46a"))
    frame = (art.door_frame().replace(art.SAND2, "#4a0912").replace(art.SAND_D, "#c9973f")
             .replace(art.ROSE_L, "#f2c96b").replace(art.ROSE_D, "#7a1022").replace(art.ROSE, "#b0122e"))
    return recolor(art.door_panel("l")), recolor(art.door_panel("r")), frame


def hands_royal(size):
    svg = el.hands_medallion(size)
    for a, b in [("#f3c6d2", "#7a1022"), ("#e9a3b8", "#9b1c31"), ("#e48fa9", "#5a0b17"), ("#f7d6df", "#b0122e"),
                 ("#efb3c4", "#8e0f26"), ("#fbe1e8", "#c2410c")]:
        svg = svg.replace(a, b)
    return svg


def elephant_royal(flip=False):
    svg = el.elephant(flip)
    return svg.replace(el.MAROON_E2, "#f3e7cf").replace(el.MAROON_E, "#d9c4a0")


def bouquet_royal():
    svg = el.bouquet()
    for a, b in [(el.PINK, "#b0122e"), ("#fbd3dc", "#e11d48"), (el.PEACH, "#e9c46a"), ("#fde0cf", "#fff1b8"),
                 (el.PEACH_D, "#c2410c"), (el.BLUE, "#f3e7cf"), (el.BLUE_D, "#d4a017")]:
        svg = svg.replace(a, b)
    return svg
