"""Three neutral body-type figures (ectomorph, mesomorph, endomorph) as clean infographic silhouettes: same pose, same
colour, same size on screen, so no build reads as better than another (brief guardrail: no ranking). Parametric:
half-widths of shoulders / chest / waist / hips and limb thickness. Writes assets/img/body_<key>.svg (viewBox 300x780).
python3 build/bodies.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CX = 150
B = {  # head r, neck, shoulder, chest, waist, hip, arm, leg, shoulder y, hip y, feet y
    "ecto": dict(hr=29, nk=10, sh=56, ch=44, wa=33, hp=41, arm=19, leg=26, sy=128, hy=372, fy=752),
    "meso": dict(hr=30, nk=14, sh=84, ch=72, wa=49, hp=58, arm=31, leg=37, sy=132, hy=368, fy=740),
    "endo": dict(hr=31, nk=15, sh=74, ch=80, wa=88, hp=86, arm=34, leg=46, sy=134, hy=376, fy=730),
}


def fig(p):
    hr, nk, sh, ch, wa, hp, arm, leg, sy, hy, fy = (p[k] for k in ("hr", "nk", "sh", "ch", "wa", "hp", "arm", "leg", "sy", "hy", "fy"))
    hy0 = sy - 34 - hr          # head centre
    ny = hy0 + hr - 6
    wy = sy + (hy - sy) * .58
    ky = hy + (fy - hy) * .5
    lx = (hp + 5) / 2           # leg centre: the thighs meet at the crotch
    kw, aw = leg * .5, leg * .28
    L = lambda x: CX - x
    R = lambda x: CX + x

    def side(f, flip):
        # one side from the neck down the outside of the leg and back up the inside, as path commands
        pts = [f"{f(nk)},{ny}", f"C{f(nk)},{sy - 8} {f(sh - 16)},{sy - 4} {f(sh - 4)},{sy + 6}",
               f"Q{f(sh + 4)},{sy + 18} {f(ch + 2)},{sy + 64}",
               f"C{f(ch + 1)},{sy + 110} {f(wa + 3)},{wy - 46} {f(wa)},{wy}",
               f"C{f(wa - 1)},{wy + 44} {f(hp + 2)},{hy - 56} {f(hp)},{hy}",
               f"C{f(hp - 2)},{hy + 70} {f(lx + kw + 4)},{ky - 60} {f(lx + kw)},{ky}",
               f"C{f(lx + kw - 4)},{ky + 70} {f(lx + aw + 2)},{fy - 60} {f(lx + aw)},{fy - 16}",
               f"Q{f(lx + aw + 10)},{fy} {f(lx + aw + 4)},{fy} L{f(lx - aw)},{fy} L{f(lx - aw)},{fy - 16}",
               f"C{f(lx - aw - 2)},{fy - 60} {f(lx - kw + 4)},{ky + 70} {f(lx - kw)},{ky}",
               f"C{f(lx - kw - 2)},{ky - 70} {f(5)},{hy + 60} {f(0)},{hy + 36}"]
        if not flip:
            return pts
        # reverse traversal for the right side so the outline closes
        return None

    left = side(L, False)
    # right side: mirror of left traversed backwards (crotch -> up inside leg -> ... -> neck)
    mir = lambda x: 2 * CX - x
    import re
    def mirror(cmds):
        out = []
        for c in cmds:
            out.append(re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", lambda m: f"{mir(float(m.group(1))):.1f},{m.group(2)}", c))
        return out
    # build right side by re-deriving with R in reverse order
    right = [f"C{R(5)},{hy + 60} {R(lx - kw - 2)},{ky - 70} {R(lx - kw)},{ky}",
             f"C{R(lx - kw + 4)},{ky + 70} {R(lx - aw - 2)},{fy - 60} {R(lx - aw)},{fy - 16}",
             f"L{R(lx - aw)},{fy} L{R(lx + aw + 4)},{fy} Q{R(lx + aw + 10)},{fy} {R(lx + aw)},{fy - 16}",
             f"C{R(lx + aw + 2)},{fy - 60} {R(lx + kw - 4)},{ky + 70} {R(lx + kw)},{ky}",
             f"C{R(lx + kw + 4)},{ky - 60} {R(hp - 2)},{hy + 70} {R(hp)},{hy}",
             f"C{R(hp + 2)},{hy - 56} {R(wa - 1)},{wy + 44} {R(wa)},{wy}",
             f"C{R(wa + 3)},{wy - 46} {R(ch + 1)},{sy + 110} {R(ch + 2)},{sy + 64}",
             f"Q{R(sh + 4)},{sy + 18} {R(sh - 4)},{sy + 6}",
             f"C{R(sh - 16)},{sy - 4} {R(nk)},{sy - 8} {R(nk)},{ny}"]
    body = "M" + " ".join(left) + " " + " ".join(right) + " Z"
    # arms: upper arm and forearm, tapered, hands
    ax0, ay0 = sh - arm * .5, sy + 16
    out = max(ch, wa) + arm * .5 + 4
    ex, ey = out + 2, sy + (hy - sy) * .5
    wx, wy2 = out + 6, hy + 30
    arms = ""
    for f in (L, R):
        arms += (f'<path d="M{f(ax0)},{ay0} Q{f(out)},{ay0 + 30} {f(ex)},{ey}" stroke-width="{arm}"/>'
                 f'<path d="M{f(ex)},{ey} L{f(wx)},{wy2}" stroke-width="{arm * .78}"/>'
                 f'<circle cx="{f(wx)}" cy="{wy2 + arm * .35}" r="{arm * .48}" stroke="none" fill="url(#g)"/>')
    guides = (f'<g stroke="#9fb4ff" stroke-width="2" stroke-dasharray="6 7" opacity=".5">'
              f'<line x1="{L(sh + 34)}" y1="{sy + 8}" x2="{R(sh + 34)}" y2="{sy + 8}"/>'
              f'<line x1="{L(out + 30)}" y1="{wy}" x2="{R(out + 30)}" y2="{wy}"/>'
              f'<line x1="{L(hp + 34)}" y1="{hy}" x2="{R(hp + 34)}" y2="{hy}"/></g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 780" width="300" height="780">
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="40" x2="0" y2="760"><stop offset="0" stop-color="#7d97ff"/><stop offset=".5" stop-color="#3159ec"/><stop offset="1" stop-color="#1a37ad"/></linearGradient>
<linearGradient id="hl" gradientUnits="userSpaceOnUse" x1="{CX - sh}" y1="0" x2="{CX + sh}" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".2"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<g fill="none" stroke="url(#g)" stroke-linecap="round">{arms}</g>
<path d="{body}" fill="url(#g)"/>
<circle cx="{CX}" cy="{hy0}" r="{hr}" fill="url(#g)"/>
<path d="{body}" fill="url(#hl)"/>
<path d="{body}" fill="none" stroke="#b9c8ff" stroke-opacity=".35" stroke-width="1.5"/>
<rect x="{CX - nk - 1}" y="{ny - 12}" width="{2 * nk + 2}" height="16" fill="url(#g)"/>
<circle cx="{CX}" cy="{hy0}" r="{hr}" fill="url(#g)" stroke="#b9c8ff" stroke-opacity=".35" stroke-width="1.5"/>
{guides}
</svg>"""


def main():
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    for k, p in B.items():
        open(os.path.join(ROOT, "assets", "img", f"body_{k}.svg"), "w").write(fig(p))
    print("wrote", ", ".join(f"body_{k}.svg" for k in B))


if __name__ == "__main__":
    main()
