"""The pink bird: rig and performance.

One cut-out (bird.png) is split into body, two wings and the beak; the face is rebuilt on top as an SVG rig so it can
emote: sockets with movable pupils (look anywhere, shrink in shock, grow when hopeful), upper and lower lids
(blink, squint, sad, sleepy, wink, smiling eyes), happy-closed "^ ^" arcs, eyebrows that lift and tilt, cheeks that
blush, a beak that opens wide or closes (and chatters for talking), plus heart eyes, star eyes and a tear.

Nesting, outermost first: #birdpos (where it is) > #bflip (which way it faces) > #bpose (posture: tall, slouch,
lean in or back, crouch) > #bwig (hops, walk wobble, head shakes) > #bidle (always-on bob and sway) > #bbreath.
Face coordinates are in the 604x640 space of the cut-out; the rig is drawn at half size (300x318).
"""

INK = "#0B0B0B"
PINK = "#E2557D"

# socket centre, radius, default pupil centre and radius (measured on bird.png)
EYES = {"L": (207, 219, 74, 219, 222, 53), "R": (411, 173, 69, 400, 180, 51)}
# upper-lid colours sampled from the body just above each eye, so a closing lid matches the skin around it
LIDCOL = {"L": ("#f45ca3", "#ee4a99"), "R": ("#f467ae", "#f055a6")}
BROWS = {"L": ("M160 128 Q206 104 252 124", "206 118"), "R": ("M368 84 Q410 62 448 78", "408 74")}

# expression = lids up (L, R), lids down (L, R), brows (dy, rot) L and R, cheeks, beak, pupil scale, overlays
EXPR = {
    "neutral":   dict(lu=(0, 0), ld=(0, 0), bl=(0, 0), br=(0, 0), ck=.25, bk="open", ps=1.0),
    "smile":     dict(lu=(0, 0), ld=(.32, .32), bl=(-6, 0), br=(-6, 0), ck=.55, bk="open", ps=1.0),
    "joy":       dict(lu=(1, 1), ld=(0, 0), bl=(-10, 0), br=(-10, 0), ck=.7, bk="wide", ps=1.0, ha=True),
    "excited":   dict(lu=(0, 0), ld=(0, 0), bl=(-18, 0), br=(-18, 0), ck=.5, bk="wide", ps=1.0, star=True),
    "love":      dict(lu=(0, 0), ld=(0, 0), bl=(-12, 0), br=(-12, 0), ck=.85, bk="open", ps=1.0, heart=True),
    "confused":  dict(lu=(.15, .3), ld=(0, 0), bl=(-16, -10), br=(6, 12), ck=.2, bk="closed", ps=.9),
    "hopeful":   dict(lu=(0, 0), ld=(0, 0), bl=(-14, -12), br=(-14, 12), ck=.35, bk="closed", ps=1.18),
    "sad":       dict(lu=(.45, .45), ld=(0, 0), bl=(-4, -18), br=(-4, 18), ck=.1, bk="closed", ps=1.05),
    "shock":     dict(lu=(0, 0), ld=(0, 0), bl=(-26, 0), br=(-26, 0), ck=.15, bk="wide", ps=.6),
    "skeptical": dict(lu=(.5, .12), ld=(.15, 0), bl=(6, 12), br=(-14, -6), ck=.15, bk="closed", ps=.95),
    "annoyed":   dict(lu=(.38, .38), ld=(.1, .1), bl=(6, 16), br=(6, -16), ck=.1, bk="closed", ps=.95),
    "focused":   dict(lu=(.28, .28), ld=(.15, .15), bl=(4, 10), br=(4, -10), ck=.2, bk="closed", ps=1.0),
    "curious":   dict(lu=(0, .1), ld=(0, 0), bl=(-14, -6), br=(-4, 6), ck=.3, bk="closed", ps=1.08),
    "proud":     dict(lu=(.2, .2), ld=(.3, .3), bl=(-4, 8), br=(-4, -8), ck=.5, bk="closed", ps=1.0),
    "wink":      dict(lu=(0, 1), ld=(.3, 0), bl=(-8, 0), br=(2, 0), ck=.6, bk="open", ps=1.0, haR=True),
}

# postures change the lean and height, never the proportions much: the art is a 3D render and big squash reads as
# distortion, so scale stays within about 3%
POSE = {
    "neutral": dict(scaleX=1, scaleY=1, rotation=0, y=0),
    "tall": dict(scaleX=.985, scaleY=1.03, rotation=0, y=-6),
    "slouch": dict(scaleX=1.02, scaleY=.97, rotation=6, y=8),
    "leanin": dict(scaleX=1, scaleY=1, rotation=10, y=0),
    "leanback": dict(scaleX=1, scaleY=1.01, rotation=-10, y=0),
    "crouch": dict(scaleX=1.03, scaleY=.96, rotation=0, y=6),
}


def _heart(cx, cy, s, cls):
    return (f'<path class="{cls}" transform="translate({cx} {cy}) scale({s})" d="M0 30 C-36 6 -50 -14 -36 -30 C-24 -44 '
            f'-6 -38 0 -24 C6 -38 24 -44 36 -30 C50 -14 36 6 0 30 Z" fill="#ff3b6b" stroke="#fff" stroke-width="4"/>')


def _star(cx, cy, s, cls):
    return (f'<path class="{cls}" transform="translate({cx} {cy}) scale({s})" d="M0 -40 L11 -12 L40 -12 L17 6 L25 36 L0 18 '
            f'L-25 36 L-17 6 L-40 -12 L-11 -12 Z" fill="#FFC531" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>')


def face_svg():
    defs = ('<defs><radialGradient id="scl" cx="45%" cy="40%" r="65%"><stop offset="0" stop-color="#ffffff"/>'
            '<stop offset=".8" stop-color="#f7eef3"/><stop offset="1" stop-color="#ead2df"/></radialGradient>'
            '<radialGradient id="pup" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#2c2c34"/>'
            '<stop offset="1" stop-color="#030305"/></radialGradient>'
            + "".join(f'<linearGradient id="lidg{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/>'
                      f'<stop offset=".93" stop-color="{b}"/><stop offset=".965" stop-color="#b8226f"/><stop offset="1" '
                      f'stop-color="#b8226f"/></linearGradient>' for k, (a, b) in LIDCOL.items()) +
            '<linearGradient id="lidb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f25aab"/>'
            '<stop offset=".9" stop-color="#f46db5"/><stop offset=".95" stop-color="#c42f80"/><stop offset="1" '
            'stop-color="#c42f80"/></linearGradient>'
            '<radialGradient id="ckg"><stop offset="0" stop-color="#ff4f88" stop-opacity=".9"/><stop offset="1" '
            'stop-color="#ff4f88" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="bkp" cx="50%" cy="50%" r="55%"><stop offset="0" stop-color="#f3519f"/>'
            '<stop offset=".8" stop-color="#f3539f"/><stop offset="1" stop-color="#f3539f" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="bky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe066"/>'
            '<stop offset="1" stop-color="#f2a516"/></linearGradient>' +
            "".join(f'<clipPath id="c{k}"><ellipse cx="{e[0]}" cy="{e[1]}" rx="{e[2]}" ry="{e[2]}"/></clipPath>'
                    f'<clipPath id="cl{k}"><ellipse cx="{e[0]}" cy="{e[1]}" rx="{e[2] + 4}" ry="{e[2] + 4}"/></clipPath>'
                    for k, e in EYES.items()) + '</defs>')
    eyes = []
    for k, (cx, cy, r, px, py, pr) in EYES.items():
        hx, hy = px + pr * .3, py - pr * .45
        arc = f'M{cx - 42} {cy + 12} Q{cx} {cy - 30} {cx + 42} {cy + 12}'
        eyes.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="url(#scl)" stroke="#f6b3d3" stroke-width="8"/>'
            f'<g clip-path="url(#c{k})"><g id="p{k}"><g id="p{k}s">'
            f'<circle cx="{px}" cy="{py}" r="{pr}" fill="url(#pup)"/>'
            f'<circle cx="{px}" cy="{py}" r="{pr - 7}" fill="none" stroke="#24243a" stroke-width="4" opacity=".6"/>'
            f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{pr * .27:.0f}" fill="#fff"/>'
            f'<circle cx="{px - pr * .38:.0f}" cy="{py + pr * .4:.0f}" r="{pr * .11:.0f}" fill="#fff" opacity=".9"/></g></g></g>'
            f'<g clip-path="url(#cl{k})"><rect id="lu{k}" x="{cx - r - 6}" y="{cy - r - 6}" width="{2 * r + 12}" height="{2 * r + 12}" fill="url(#lidg{k})"/>'
            f'<rect id="ld{k}" x="{cx - r - 6}" y="{cy - r - 6}" width="{2 * r + 12}" height="{2 * r + 12}" fill="url(#lidb)"/>'
            f'</g><path id="ha{k}" d="{arc}" stroke="#6d1a43" stroke-width="11" fill="none" stroke-linecap="round" opacity="0"/>'
            f'<g id="hrt{k}" opacity="0">{_heart(cx, cy + 4, 1.55, "hp")}</g>'
            f'<g id="str{k}" opacity="0">{_star(cx, cy + 2, 1.5, "sp")}</g>')
    brows = "".join(f'<g id="br{k}"><path d="{d}" stroke="#b72a77" stroke-width="15" fill="none" stroke-linecap="round"/></g>'
                    for k, (d, _) in BROWS.items())
    cheeks = ('<ellipse id="ckL" cx="172" cy="318" rx="44" ry="26" fill="url(#ckg)" opacity=".25"/>'
              '<ellipse id="ckR" cx="452" cy="268" rx="40" ry="24" fill="url(#ckg)" opacity=".25"/>')
    beak = ('<image id="beak" href="assets/img/bird_beak.png" x="0" y="0" width="604" height="640"/>'
            '<g id="cbk" opacity="0"><ellipse cx="326" cy="262" rx="62" ry="68" fill="url(#bkp)"/>'
            '<path d="M284 214 C298 194 352 194 368 214 C374 238 342 266 326 272 C310 266 278 238 284 214 Z" fill="url(#bky)" '
            'stroke="#e2930f" stroke-width="4"/><path d="M302 214 C316 206 336 206 350 214" stroke="#fff6c4" stroke-width="6" '
            'fill="none" stroke-linecap="round" opacity=".8"/></g>')
    tear = ('<path id="tear" d="M188 300 C196 316 204 324 204 334 C204 344 196 350 188 350 C180 350 172 344 172 334 '
            'C172 324 180 316 188 300 Z" fill="#7cc8ff" stroke="#fff" stroke-width="3" opacity="0"/>')
    return (f'<svg id="face" viewBox="0 0 604 640" width="300" height="318">{defs}{cheeks}{"".join(eyes)}{brows}{beak}'
            f'{tear}</svg>')


def magnifier(s=150):
    return (f'<svg viewBox="0 0 150 150" width="{s}" height="{s}"><path d="M92 92 L138 138" stroke="#8a5a2b" '
            f'stroke-width="16" stroke-linecap="round"/><circle cx="62" cy="62" r="44" fill="rgba(220,240,255,.45)" '
            f'stroke="#f2b134" stroke-width="12"/><path d="M40 48 C46 36 58 30 70 32" stroke="#fff" stroke-width="6" '
            f'fill="none" stroke-linecap="round" opacity=".9"/></svg>')


def bubble(inner, w=150, h=120, cls=""):
    return (f'<div class="bub {cls}" data-layout-ignore style="width:{w}px;height:{h}px">{inner}'
            f'<svg class="tail" viewBox="0 0 60 50" width="60" height="50"><circle cx="20" cy="12" r="11" fill="#fff" '
            f'stroke="{INK}" stroke-width="4"/><circle cx="6" cy="38" r="6" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            f'</svg></div>')


def cloud():
    drops = "".join(f'<i class="drop" style="left:{x}px"></i>' for x in (40, 80, 120, 60, 100))
    return (f'<div id="cloud" data-layout-ignore><svg viewBox="0 0 180 90" width="180" height="90"><path d="M30 80 C8 80 4 52 '
            f'26 46 C24 22 54 12 70 30 C80 6 122 8 126 36 C150 30 170 50 156 70 C152 78 146 80 140 80 Z" fill="#c9ccd6"/>'
            f'</svg>{drops}</div>')


def rig(star):
    sp = "".join(f'<div class="bsp bsp{i}" style="left:{x}px;top:{y}px">{star(s, c)}</div>'
                 for i, (x, y, s, c) in enumerate([(-40, 40, 54, PINK), (270, -10, 44, "#f2b134"),
                                                   (290, 170, 36, PINK), (-20, 210, 34, "#f2b134")]))

    def lay(i, src, extra=""):
        return f'<div id="{i}" class="lay"{extra}><div id="{i}i" class="lay"><img src="assets/img/{src}" width="300" height="318" alt=""></div></div>'
    return (f'<div id="birdpos"><div id="bshadow"></div><div id="bflip"><div id="bpose"><div id="bwig"><div id="bidle">'
            f'<div id="bbreath">'
            + lay("wingL", "bird_wingl.png") + lay("wingD", "bird_wingl.png") +
            '<div id="footL" class="foot"><div id="footLi" class="foot"><img src="assets/img/bird_foot.png" alt=""></div></div>'
            '<div id="footR" class="foot"><div id="footRi" class="foot"><img src="assets/img/bird_foot.png" alt=""></div></div>'
            f'<img id="bimg" src="assets/img/bird_core.png" width="300" height="318" alt="">'
            '<div id="footK" class="foot"><div id="footKi" class="foot"><img src="assets/img/bird_foot_up.png" alt=""></div></div>' +
            f'{face_svg()}' + lay("wingR", "bird_wing.png") +
            f'<div id="sweat"><svg viewBox="0 0 30 44" width="30" height="44"><path d="M15 0 C22 14 30 22 30 30 '
            f'C30 38 23 44 15 44 C7 44 0 38 0 30 C0 22 8 14 15 0 Z" fill="#7cc8ff"/></svg></div>'
            f'<div id="mag">{magnifier(150)}</div></div></div></div></div></div>'
            f'{bubble("<b>?</b>", 130, 120, "bq")}{bubble("<b>!</b>", 120, 120, "bx")}'
            f'{cloud()}{sp}</div>')


CSS = """
#birdlayer { z-index: 20; }
#birdpos { position: absolute; left: 0; top: 0; width: 300px; height: 318px; transform-origin: 50% 100%; }
#bshadow { position: absolute; left: 40px; top: 296px; width: 220px; height: 40px; border-radius: 50%;
  background: radial-gradient(closest-side, rgba(226,53,160,.35), rgba(226,53,160,0)); }
#bflip, #bpose, #bwig, #bidle, #bbreath { position: absolute; inset: 0; transform-origin: 50% 100%; }
#bflip { transform-origin: 50% 60%; }
#bimg, #face { position: absolute; left: 0; top: 0; }
#bimg { filter: drop-shadow(0 18px 24px rgba(160,20,90,.25)); }
.lay { position: absolute; inset: 0; }
.lay img { position: absolute; left: 0; top: 0; }
#wingR, #wingRi { transform-origin: 266px 154px; }
#wingL, #wingLi { transform-origin: 47px 209px; }
#wingD, #wingDi { transform-origin: 267px 209px; }
/* the right wing is the left one mirrored about the body's centre line (the original right wing was cropped) */
#wingD img { transform: scaleX(-1); transform-origin: 157px 0; }
/* feet sit behind the body so its round bottom tucks over them; the kicked foot is in front, as in the art */
.foot { position: absolute; }
.foot img { display: block; width: 100%; height: 100%; }
#footL { left: 60px; top: 264px; width: 84px; height: 53px; transform: rotate(-8deg); }
#footR { left: 160px; top: 262px; width: 84px; height: 53px; transform: scaleX(-1) rotate(-8deg); }
#footLi, #footRi { inset: 0; transform-origin: 70% 20%; }
#footK { left: 218px; top: 214px; width: 73px; height: 63px; }
#footKi { inset: 0; transform-origin: 20% 60%; }
#sweat { position: absolute; left: 250px; top: 30px; }
#mag { position: absolute; left: 150px; top: 140px; transform-origin: 30% 30%; }
.bub { position: absolute; left: 190px; top: -130px; background: #fff; border: 4px solid #0B0B0B; border-radius: 50px;
  display: flex; align-items: center; justify-content: center; font: 700 80px "Google Sans"; color: #C93A6D; }
.bub .tail { position: absolute; left: 6px; bottom: -48px; }
.bub i { font: 700 52px "Google Sans"; font-style: normal; letter-spacing: 1px; background: linear-gradient(90deg, #E235DD, #E34CB7 45%, #E68B70);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.bc { left: -200px; top: -150px; }
.bsp { position: absolute; }
#cloud { position: absolute; left: 60px; top: -150px; width: 180px; height: 200px; }
.drop { position: absolute; top: 80px; width: 8px; height: 22px; border-radius: 4px; background: #7cc8ff; }
"""


class Bird:
    """Writes the bird's tweens in time order and keeps track of its facing, lids and pose."""

    def __init__(self, add):
        self.add = add
        self.facing = 1
        self.lu = {"L": 0, "R": 0}
        self.hist = [(0, {"L": 0, "R": 0})]

    # ---------------------------------------------------------------- body
    def at(self, t, x, y, s, d=.5, ease="power3.inOut"):
        self.add(f'tl.to("#birdpos",{{x:{x},y:{y},scale:{s},duration:{d},ease:"{ease}"}},{t:.2f});')

    def face(self, t, d):
        self.facing = d
        self.add(f'tl.to("#bflip",{{scaleX:{d},duration:.16,ease:"power2.inOut"}},{t:.2f});')

    def pose(self, t, name, d=.3, ease="back.out(2)"):
        p = POSE[name]
        self.add(f'tl.to("#bpose",{{scaleX:{p["scaleX"]},scaleY:{p["scaleY"]},rotation:{p["rotation"]},y:{p["y"]},'
                 f'duration:{d},ease:"{ease}"}},{t:.2f});')

    def hop(self, t, h=60):
        """Crouch to load, spring up stretched, fall, squash on landing; the feet tuck while airborne."""
        a = max(0, t - .1)
        self.add(f'tl.to("#bwig",{{scaleY:.95,scaleX:1.04,y:4,duration:.1,ease:"power2.out"}},{a:.2f});')
        self.add(f'tl.to("#bwig",{{y:-{h},scaleY:1.04,scaleX:.97,duration:.2,ease:"power2.out"}},{t:.2f});')
        self.add(f'tl.to("#bwig",{{y:0,scaleY:1,scaleX:1,duration:.17,ease:"power2.in"}},{t + .2:.2f});')
        self.add(f'tl.to("#bwig",{{scaleY:.95,scaleX:1.05,duration:.07,ease:"power1.out",yoyo:true,repeat:1}},{t + .37:.2f});')
        self.add(f'tl.to("#footLi, #footRi",{{y:-10,rotation:20,duration:.16,ease:"power2.out",yoyo:true,repeat:1}},{t:.2f});')

    def walk(self, t, d, step=.24):
        """A real walk: feet step alternately, body rocks and bobs."""
        n = max(2, int(d / step))
        self.legs(t, "stand", .05)
        self.add(f'tl.to("#bwig",{{rotation:6,y:-12,duration:{step / 2:.3f},ease:"sine.inOut",yoyo:true,repeat:{n - 1}}},{t:.2f});')
        self.add(f'tl.to("#bwig",{{rotation:0,y:0,duration:.1}},{t + n * step / 2 + .01:.2f});')
        for f, off in (("#footLi", 0), ("#footRi", step / 2)):
            m = max(1, int((d - off) / step))
            self.add(f'tl.to("{f}",{{y:-13,x:6,rotation:-16,duration:{step / 2:.3f},ease:"sine.inOut",yoyo:true,repeat:{m * 2 - 1},'
                     f'repeatDelay:0}},{t + off:.2f});')
    def shake(self, t, n=3, a=10):
        """Head shake 'no'."""
        self.add(f'tl.fromTo("#bwig",{{rotation:-{a}}},{{rotation:{a},duration:.11,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1},'
                 f'immediateRender:false}},{t:.2f});tl.to("#bwig",{{rotation:0,duration:.1}},{t + n * .22 + .01:.2f});')

    def nod(self, t, n=2):
        self.add(f'tl.to("#bwig",{{y:12,rotation:4,duration:.13,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')

    def bounce(self, t, n=4, h=22):
        self.add(f'tl.to("#bwig",{{y:-{h},duration:.12,ease:"power1.out",yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')

    def spin(self, t):
        self.add(f'tl.to("#bflip",{{rotation:360,duration:.55,ease:"power2.inOut"}},{t:.2f});tl.set("#bflip",{{rotation:0}},{t + .6:.2f});')

    def startle(self, t):
        self.add(f'tl.to("#bwig",{{scaleY:1.05,scaleX:.96,y:-60,duration:.13,yoyo:true,repeat:1}},{t:.2f});')

    # ---------------------------------------------------------------- limbs
    def arms(self, t, state, d=.12):
        """'down' = both wings hanging (resting), 'up' = the right wing raised (waving / pointing / scratching)."""
        up = 1 if state == "up" else 0
        self.add(f'tl.to("#wingR",{{opacity:{up},duration:{d}}},{t:.2f});tl.to("#wingD",{{opacity:{1 - up},duration:{d}}},{t:.2f});')

    def legs(self, t, state, d=.12):
        """'stand' = both feet on the ground, 'kick' = right foot lifted (the original pose)."""
        k = 1 if state == "kick" else 0
        self.add(f'tl.to("#footK",{{opacity:{k},duration:{d}}},{t:.2f});tl.to("#footR",{{opacity:{1 - k},duration:{d}}},{t:.2f});')

    def spread(self, t, a, d=.25, ease="back.out(2)"):
        """Both resting wings out sideways by a degrees (0 = back at the sides, negative = tucked in)."""
        self.add(f'tl.to("#wingL",{{rotation:{a},duration:{d},ease:"{ease}"}},{t:.2f});')
        self.add(f'tl.to("#wingD",{{rotation:{-a},duration:{d},ease:"{ease}"}},{t:.2f});')

    def flap(self, t, n=4, a=40):
        self.add(f'tl.to("#wingL",{{rotation:{a},duration:.07,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')
        self.add(f'tl.to("#wingD",{{rotation:-{a},duration:.07,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')

    def wave(self, t, n=3):
        self.arms(t, "up")
        self.add(f'tl.fromTo("#wingR",{{rotation:-12}},{{rotation:24,duration:.16,ease:"sine.inOut",yoyo:true,repeat:{n * 2 - 1},'
                 f'immediateRender:false}},{t:.2f});tl.to("#wingR",{{rotation:0,duration:.12}},{t + n * .32 + .01:.2f});')
        self.arms(t + n * .32 + .1, "down")

    def point(self, t, d=1.0):
        """Raise the front wing towards what it faces and jab it a few times."""
        n = max(1, int((d - .3) / .3))
        self.arms(t, "up", .08)
        self.add(f'tl.to("#wingR",{{rotation:42,duration:.22,ease:"back.out(2)"}},{t:.2f});')
        self.add(f'tl.to("#wingR",{{rotation:30,duration:.15,yoyo:true,repeat:{n * 2 - 1}}},{t + .25:.2f});')
        self.add(f'tl.to("#wingR",{{rotation:0,duration:.2}},{t + .25 + n * .3 + .02:.2f});')
        self.arms(t + .25 + n * .3 + .2, "down")

    def scratch(self, t, d=1.2):
        """Right wing up to the head, rubbing."""
        n = max(1, int(d / .24))
        self.arms(t, "up", .08)
        self.add(f'tl.to("#wingR",{{rotation:-38,duration:.25,ease:"back.out(2)"}},{t:.2f});')
        self.add(f'tl.to("#wingR",{{rotation:-26,duration:.12,yoyo:true,repeat:{n * 2 - 1}}},{t + .27:.2f});')
        self.add(f'tl.to("#wingR",{{rotation:0,duration:.2}},{t + .27 + n * .24 + .02:.2f});')
        self.arms(t + .27 + n * .24 + .2, "down")

    def kick(self, t, d=.8):
        self.legs(t, "kick", .06)
        self.add(f'tl.fromTo("#footKi",{{rotation:-8}},{{rotation:10,duration:.14,yoyo:true,repeat:{max(1, int(d / .28)) * 2 - 1},'
                 f'immediateRender:false}},{t:.2f});')
        self.legs(t + d, "stand", .06)

    def tap(self, t, n=4):
        """Impatient / excited foot tap."""
        self.add(f'tl.to("#footRi",{{rotation:-16,y:-6,duration:.09,yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')

    # ---------------------------------------------------------------- face
    def look(self, t, dx, dy, d=.14):
        self.add(f'tl.to("#pL, #pR",{{x:{dx * self.facing},y:{dy},duration:{d},ease:"power2.out"}},{t:.2f});')

    def expr(self, t, name, d=.18):
        e = EXPR[name]
        for i, k in enumerate("LR"):
            cx, cy, r = EYES[k][:3]
            top, bot = cy - r - 6, cy + r + 6
            self.add(f'tl.to("#lu{k}",{{scaleY:{e["lu"][i]},svgOrigin:"{cx} {top}",duration:{d}}},{t:.2f});')
            self.add(f'tl.to("#ld{k}",{{scaleY:{e["ld"][i]},svgOrigin:"{cx} {bot}",duration:{d}}},{t:.2f});')
            dy, rot = e["b" + k.lower()]
            self.add(f'tl.to("#br{k}",{{y:{dy},rotation:{rot},svgOrigin:"{BROWS[k][1]}",duration:{d},ease:"back.out(2)"}},{t:.2f});')
            px, py = EYES[k][3:5]
            self.add(f'tl.to("#p{k}s",{{scale:{e["ps"]},svgOrigin:"{px} {py}",duration:{d}}},{t:.2f});')
            self.lu[k] = e["lu"][i]
        self.hist.append((t + d, dict(self.lu)))
        self.add(f'tl.to("#ckL, #ckR",{{opacity:{e["ck"]},duration:{d}}},{t:.2f});')
        bk = e["bk"]
        self.add(f'tl.to("#cbk",{{opacity:{1 if bk == "closed" else 0},duration:.08}},{t:.2f});')
        self.add(f'tl.to("#beak",{{scale:{1.22 if bk == "wide" else 1},svgOrigin:"326 200",duration:{d},ease:"back.out(2)"}},{t:.2f});')
        ha_l = 1 if e.get("ha") else 0
        ha_r = 1 if e.get("ha") or e.get("haR") else 0
        self.add(f'tl.to("#haL",{{opacity:{ha_l},duration:{d}}},{t:.2f});tl.to("#haR",{{opacity:{ha_r},duration:{d}}},{t:.2f});')
        for ov, key in (("hrt", "heart"), ("str", "star")):
            on = 1 if e.get(key) else 0
            self.add(f'tl.to("#{ov}L, #{ov}R",{{opacity:{on},duration:{d}}},{t:.2f});')

    def blink(self, t):
        lu = [h for h in self.hist if h[0] <= t][-1][1]
        for k in "LR":
            cx, cy, r = EYES[k][:3]
            self.add(f'tl.to("#lu{k}",{{scaleY:1,svgOrigin:"{cx} {cy - r - 6}",duration:.06}},{t:.2f});'
                     f'tl.to("#lu{k}",{{scaleY:{lu[k]},svgOrigin:"{cx} {cy - r - 6}",duration:.08}},{t + .07:.2f});')

    def talk(self, t, d):
        n = max(1, int(d / .16))
        self.add(f'tl.to("#cbk",{{opacity:1,duration:.04,yoyo:true,repeat:{n * 2 - 1},repeatDelay:.04}},{t:.2f});')

    def pulse_overlay(self, t, ov, n=4):
        for k in "LR":
            cx, cy = EYES[k][:2]
            self.add(f'tl.to("#{ov}{k}",{{scale:1.25,svgOrigin:"{cx} {cy}",duration:.16,yoyo:true,repeat:{n * 2 - 1}}},{t:.2f});')

    def tear(self, t):
        self.add(f'tl.fromTo("#tear",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:.2,immediateRender:false}},{t:.2f});')
        self.add(f'tl.to("#tear",{{y:120,opacity:0,duration:.7,ease:"power1.in"}},{t + .3:.2f});')

    def show(self, sel, t, on=True, d=.3):
        if on:
            self.add(f'tl.to("{sel}",{{opacity:1,scale:1,duration:{d},ease:"back.out(3)"}},{t:.2f});')
        else:
            self.add(f'tl.to("{sel}",{{opacity:0,scale:.5,duration:.2,ease:"power2.in"}},{t:.2f});')


def perform(add, dur):
    """The bird's performance, line by line with the voiceover. Resting pose: on both feet, wings at the sides."""
    b = Bird(add)
    add('tl.set("#birdpos",{x:1160,y:1010,scale:.85},0);tl.set("#bflip",{scaleX:-1},0);')
    add('tl.set("#sweat,#mag,.bub,.bsp,#cloud",{opacity:0,scale:.5},0);tl.set("#wingR,#footK",{opacity:0},0);')
    for k in "LR":
        cx, cy, r = EYES[k][:3]
        add(f'tl.set("#lu{k}",{{scaleY:0,svgOrigin:"{cx} {cy - r - 6}"}},0);tl.set("#ld{k}",{{scaleY:0,svgOrigin:"{cx} {cy + r + 6}"}},0);')
    b.facing = -1
    # always alive under every gesture
    add(f'tl.to("#bidle",{{y:-7,duration:.42,ease:"sine.inOut",yoyo:true,repeat:{int(dur / .42) - 1}}},0);')
    add(f'tl.fromTo("#bidle",{{rotation:-2.5}},{{rotation:2.5,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(dur / 1.3) - 1}}},0);')
    add(f'tl.to("#bbreath",{{scaleY:1.012,scaleX:.994,duration:.8,ease:"sine.inOut",yoyo:true,repeat:{int(dur / .8) - 1}}},0);')
    add(f'tl.fromTo("#wingLi",{{rotation:3}},{{rotation:-4,duration:.6,ease:"sine.inOut",yoyo:true,repeat:{int(dur / .6) - 1}}},0);')
    add(f'tl.fromTo("#wingDi",{{rotation:-3}},{{rotation:4,duration:.6,ease:"sine.inOut",yoyo:true,repeat:{int(dur / .6) - 1}}},.3);')
    # weight shifts from foot to foot with the body's sway, so the feet are never frozen
    add(f'tl.fromTo("#footLi",{{rotation:0,y:0}},{{rotation:-7,y:-4,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(dur / 1.3) - 1}}},0);')
    add(f'tl.fromTo("#footRi",{{rotation:-7,y:-4}},{{rotation:0,y:0,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(dur / 1.3) - 1}}},0);')
    add(f'tl.fromTo("#wingRi",{{rotation:-4}},{{rotation:8,duration:.45,ease:"sine.inOut",yoyo:true,repeat:{int(dur / .45) - 1}}},0);')
    add('tl.set("#bshadow",{opacity:0},0);tl.to("#bshadow",{opacity:1,duration:.3},.6);')

    # "One reel did 85x my usual views" — walks in curious, stops on both feet, sees the counter, explodes on 85x
    b.expr(0, "curious", .01)
    b.at(.1, 660, 1010, .85, 1.0, "power1.out")
    b.walk(.1, 1.0)
    b.look(.2, 10, 0)
    b.face(1.12, 1)
    b.look(1.12, -16, -8)
    b.expr(1.3, "excited", .14)
    b.pose(1.25, "tall", .15)
    b.hop(1.3, 120)
    b.kick(1.3, .7)
    b.flap(1.3, 5, 50)
    b.pulse_overlay(1.45, "str", 4)
    b.show(".bsp", 1.4)
    add('tl.to(".bsp",{rotation:120,duration:1.2,ease:"none"},1.4);')
    b.show(".bsp", 2.6, False)
    b.pose(2.2, "neutral", .25)
    b.expr(2.35, "joy", .15)
    b.bounce(2.35, 3, 16)
    b.spread(2.35, 20)
    b.spread(3.1, 0)
    # "and I had no idea why." — stands still, confused, head tilt, scratches its head, looks up thinking
    b.expr(3.6, "confused", .2)
    b.look(3.6, -10, -14)
    b.pose(3.6, "leanback", .3)
    add('tl.to("#bwig",{rotation:-12,duration:.35,ease:"back.out(2)"},3.7);')
    b.scratch(3.75, 1.1)
    b.show(".bq", 3.9)
    b.look(4.5, 14, -12)
    b.blink(4.9)
    b.show(".bq", 5.4, False)
    add('tl.to("#bwig",{rotation:0,duration:.2},5.3);')
    # "The next one?" — walks over hopefully, stands tall on tiptoe, leans in to the new cover
    b.face(5.55, -1)
    b.expr(5.55, "hopeful", .2)
    b.at(5.6, 760, 1000, .82, .55, "power2.inOut")
    b.walk(5.6, .55)
    b.face(6.2, 1)
    b.pose(6.2, "leanin", .25)
    b.look(6.2, -18, -6)
    b.spread(6.2, -8)
    # "A few thousand." — deflates: sad eyes, slouch, wings hang limp, a tear and a rain cloud
    b.expr(6.95, "sad", .3)
    b.pose(6.95, "slouch", .4, "power2.out")
    b.look(6.95, -6, 14)
    b.spread(6.95, -14, .4, "power2.out")
    b.show("#sweat", 7.0)
    add('tl.to("#sweat",{y:40,duration:.9,ease:"power1.in"},7.1);')
    b.tear(7.2)
    b.show("#cloud", 6.95)
    add('tl.fromTo("#cloud .drop",{y:0,opacity:1},{y:90,opacity:0,duration:.35,stagger:.07,repeat:2,ease:"power1.in"},7.05);')
    b.show("#sweat", 7.95, False)
    b.show("#cloud", 7.95, False)
    # "Numbers..." — jolted upright by the tiles slamming in, wings fly out
    b.pose(8.05, "neutral", .15)
    b.spread(8.05, 0, .15)
    b.at(8.1, 400, 1080, .78, .45)
    b.expr(8.35, "shock", .1)
    b.startle(8.35)
    b.look(8.4, 0, -18)
    b.spread(8.35, 55, .12)
    b.spread(8.75, 0, .2)
    # "...never reasons." — unimpressed: skeptical squint, big shrug, head shake
    b.expr(9.1, "skeptical", .2)
    b.look(9.1, 12, 0)
    b.spread(9.25, 60, .18)
    b.shake(9.35, 3, 9)
    b.spread(10.0, 0, .2)
    # "So I gave my page to Creedom." — perks up and smiles, stands tall, takes the magnifier, walks along scanning
    b.at(10.45, 800, 1130, .72, .5)
    b.expr(10.6, "smile", .2)
    b.pose(10.6, "tall", .25)
    b.show("#mag", 10.8)
    b.face(11.0, -1)
    b.at(11.0, 520, 1130, .72, 1.6, "sine.inOut")
    b.walk(11.0, 1.6, .28)
    b.expr(11.1, "focused", .2)
    b.look(11.1, 14, -14)
    add('tl.to("#mag",{rotation:-14,y:-20,duration:.4,ease:"sine.inOut",yoyo:true,repeat:3},11.0);')
    b.look(11.9, 6, -18)
    # "Twenty seconds." — turns to the stopwatch, impressed, jumps with a kick
    b.face(12.7, 1)
    b.expr(12.75, "excited", .15)
    b.look(12.75, 14, -10)
    b.hop(12.85, 70)
    b.kick(12.85, .5)
    b.show("#mag", 13.6, False)
    b.pose(13.6, "neutral", .2)
    # "Content score:" — stands still on both feet, leans in, taps a foot in anticipation
    b.at(13.9, 730, 1100, .7, .45)
    b.expr(14.1, "curious", .2)
    b.pose(14.2, "leanin", .3)
    b.look(14.2, -18, -16)
    b.face(14.2, -1)
    b.tap(14.45, 4)
    # "82 out of 100." — heart eyes, blush, jump, spin, flap
    b.expr(15.35, "love", .15)
    b.pose(15.35, "tall", .15)
    b.hop(15.35, 140)
    b.spin(15.35)
    b.flap(15.35, 5, 55)
    b.pulse_overlay(15.5, "hrt", 4)
    b.show(".bsp", 15.45)
    add('tl.to(".bsp",{rotation:220,duration:1.3,ease:"none"},15.45);')
    b.show(".bsp", 16.8, False)
    b.expr(16.3, "joy", .15)
    b.wave(16.3, 2)
    b.pose(16.9, "neutral", .2)
    # "Then its reel analyser watched my reel..." — curious, points at the chat, then stands and nods along
    b.at(17.05, 760, 1060, .6, .45)
    b.face(17.3, -1)
    b.expr(17.3, "curious", .2)
    b.look(17.3, 14, -18)
    b.point(17.4, 1.0)
    b.nod(18.3, 2)
    b.expr(18.6, "focused", .2)
    b.face(18.6, 1)
    b.look(18.6, 16, 4)
    b.blink(19.3)
    # "second by second." — surfs the playhead down the timeline, wings out for balance
    b.face(19.6, 1)
    b.at(19.85, -60, 330, .42, .4)
    b.pose(20.15, "leanin", .2)
    b.spread(20.2, 50, .2)
    b.kick(20.2, 1.0)
    b.expr(20.2, "excited", .15)
    b.look(20.2, 10, 16)
    add('tl.to("#birdpos",{y:960,duration:1.05,ease:"power1.inOut"},20.25);')
    b.pose(21.25, "neutral", .2)
    b.spread(21.25, 0, .2)
    # "And found what I'd missed..." — inside the reel: it holds the giant magnifier up to the film strip and walks on
    # the spot while the frames scroll under the lens, stopping on each one
    b.face(21.3, 1)
    b.at(21.3, 40, 960, .78, .35, "power3.out")
    b.pose(21.35, "neutral", .2)
    b.arms(21.4, "up", .1)
    add('tl.to("#wingR",{rotation:18,duration:.25,ease:"back.out(2)"},21.4);')
    b.expr(21.45, "focused", .25)
    b.look(21.5, 14, -10)
    b.walk(21.62, 1.62, .27)
    b.look(22.4, 16, -14)
    # "my best hook was buried at 0:34." — the lens lands on it: jolt, "!", star eyes, a little victory hop
    b.expr(23.33, "shock", .1)
    b.startle(23.33)
    b.show(".bx", 23.4)
    b.look(23.35, 18, -18)
    b.show(".bx", 24.3, False)
    b.expr(23.75, "excited", .15)
    b.pulse_overlay(23.85, "str", 3)
    b.hop(24.1, 50)
    # the frame lifts out and flies back to 0:00: it watches it go, then cheers when it lands
    b.look(24.6, -18, -20)
    b.pose(24.6, "leanback", .3)
    add('tl.to("#wingR",{rotation:0,duration:.2},24.6);')
    b.arms(24.75, "down", .1)
    b.flap(24.7, 4, 45)
    b.pose(25.3, "tall", .2)
    b.expr(25.3, "joy", .15)
    b.hop(25.35, 70)
    b.wave(25.75, 1)
    # "Now I edit with reasons." — stands tall and proud on both feet, nods, then jumps to the reasons card
    b.at(26.3, 150, 332, .5, .45)
    b.face(26.4, 1)
    b.expr(26.5, "proud", .2)
    b.pose(26.5, "tall", .3)
    b.look(26.5, 0, 0)
    b.spread(26.5, -10, .25)
    b.nod(26.6, 1)
    add('tl.to("#birdpos",{x:700,duration:.6,ease:"power2.inOut"},27.0);')
    add('tl.to("#birdpos",{y:200,duration:.3,ease:"power2.out",yoyo:true,repeat:1},27.0);')
    b.flap(27.0, 4, 45)
    add('tl.to("#birdpos",{y:282,duration:.15,ease:"power2.out"},27.62);')
    b.expr(27.6, "smile", .15)
    # "Not guesses." — turns back to the guesses card, frowns, shakes its head and wags a wing "no"
    b.face(28.25, -1)
    b.look(28.25, 18, 10)
    b.expr(28.3, "annoyed", .15)
    b.pose(28.3, "neutral", .2)
    b.shake(28.35, 3, 11)
    b.arms(28.4, "up", .08)
    add('tl.to("#wingR",{rotation:30,duration:.15},28.4);tl.to("#wingR",{rotation:10,duration:.1,yoyo:true,repeat:5},28.55);')
    add('tl.to("#wingR",{rotation:0,duration:.12},29.15);')
    b.arms(29.25, "down")
    # "Comment CREEDOM..." — excited, points at the box, chatters, winks
    b.at(29.4, 730, 1080, .7, .45)
    b.expr(29.5, "excited", .12)
    b.face(30.05, -1)
    b.look(30.05, 16, 0)
    b.point(30.1, .9)
    b.talk(29.62, .9)
    b.expr(30.5, "wink", .15)
    # "and I'll DM you the link." — stands, watches the paper plane fly off, smiling, taps a happy foot
    b.expr(30.9, "smile", .15)
    b.look(31.05, -16, -18)
    b.pose(31.05, "leanback", .3)
    b.talk(31.0, .9)
    b.tap(31.2, 3)
    # end card: centre stage on both feet, joyful, waves goodbye, final wink
    b.face(32.0, 1)
    b.pose(32.0, "tall", .2)
    b.at(32.1, 390, 900, 1.05, .5, "back.out(1.4)")
    b.hop(32.15, 60)
    b.expr(32.2, "joy", .15)
    b.look(32.2, 0, 0)
    b.wave(32.55, 3)
    b.expr(33.0, "wink", .12)
    b.hist.sort(key=lambda h: h[0])
    for t in (2.0, 4.2, 6.6, 9.8, 11.6, 13.3, 17.0, 18.2, 19.8, 22.6, 26.0, 27.2, 29.1, 31.7):
        b.blink(t)
