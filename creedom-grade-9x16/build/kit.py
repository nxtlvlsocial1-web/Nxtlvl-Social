"""Kinetic kit for the Creedom remakes v2 (bright pink, fast). Shared by creedom-postmortem-9x16 and creedom-grade-9x16
(the grade project keeps an identical copy in its own build/ folder).

Layers, back to front:  #bg (moving pink gradient, blobs, dots)  >  #shk (shake)  >  #cam (punch-ins)  >  #drift (slow
per-scene push)  >  scene content  >  .burst / #flash  >  captions  >  grain.
Everything is a pure function of the one paused GSAP timeline.
"""
import json
import os
import random
import re

PINK, HOT, INK, SUN = "#ff3d8b", "#ff1f74", "#16121a", "#ffe14d"


class Reel:
    def __init__(self, root, title):
        self.ROOT, self.title = root, title
        self.W = json.load(open(os.path.join(root, "plan", "words.json")))
        self.SCRIPT = json.load(open(os.path.join(root, "plan", "script.json")))
        self.LW = {}
        for w in self.W:
            self.LW.setdefault(w["line"], []).append(w)
        self.JS, self.SFX, self.HTML, self.TOP, self.CSS = [], [], [], [], []
        self.IDS = [ln["id"] for ln in self.SCRIPT]
        self.L = {i: (self.LW[i][0]["t0"], self.LW[i][-1]["t1"]) for i in self.IDS}
        self.S = [self.L[i][0] for i in self.IDS] + [self.L[self.IDS[-1]][1] + .9]
        self.DUR = round(self.S[-1], 2)
        self.n_slam = 0

    # ---- timeline primitives
    def js(self, s):
        self.JS.append(s)

    def sfx(self, kind, t):
        self.SFX.append({"type": kind, "t": round(max(0, t), 3)})

    @staticmethod
    def _join(obj, extra):
        body = obj.strip()[1:-1].strip()
        return "{" + (body + ", " if body else "") + extra + "}"

    def ft(self, sel, t, d, frm, to_, ease="power3.out"):
        # cold-seek safe: a from-state that reveals the element must also reveal it in the to-vars
        if re.search(r"opacity:\s*1\b", frm) and "opacity" not in to_:
            to_ = self._join(to_, "opacity: 1")
        self.js(f'tl.fromTo("{sel}", {frm}, {self._join(to_, f"duration: {d}, ease: \"{ease}\", immediateRender: false")}, {t:.3f});')

    def to(self, sel, t, d, props, ease="power2.out"):
        self.js(f'tl.to("{sel}", {self._join(props, f"duration: {d}, ease: \"{ease}\"")}, {t:.3f});')

    def st(self, sel, t, props):
        self.js(f'tl.set("{sel}", {props}, {t:.3f});')

    def wt(self, line, word, n=0, end=False):
        hits = [w for w in self.LW[line] if re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(word.lower())]
        if not hits:
            raise SystemExit(f"{line}: no word starting {word!r}: {[w['w'] for w in self.LW[line]]}")
        h = hits[min(n, len(hits) - 1)]
        return h["t1"] if end else h["t0"]

    def counter(self, el_id, t, d, a, b, fmt="Math.round(o.v)", ease="power2.out"):
        self.js(f'(() => {{ const o = {{v: {a}}}; tl.to(o, {{v: {b}, duration: {d}, ease: "{ease}", onUpdate: () => {{ '
                f'document.getElementById("{el_id}").textContent = {fmt}; }}}}, {t:.3f}); }})();')

    def typer(self, el_id, t, text, d):
        n = len(text)
        self.js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: {n}, duration: {d}, ease: "steps({n})", onUpdate: () => {{ '
                f'document.getElementById("{el_id}").textContent = "{text}".slice(0, Math.round(o.n)); }}}}, {t:.3f}); }})();')

    # ---- camera grammar
    def punch(self, t, amt=.09, d=.4):
        """camera punch-in: jumps in by amt and settles (a cut-like hit)"""
        self.ft("#cam", t, d, f"{{scale: {1 + amt:.3f}}}", "{scale: 1}", "expo.out")

    def shake(self, t, s=14, rot=1.2):
        ks = [{"x": -s, "y": s * .4, "rotation": -rot}, {"x": s * .8, "y": -s * .5, "rotation": rot}, {"x": -s * .5, "y": s * .3, "rotation": -rot * .5},
              {"x": s * .3, "y": -s * .2, "rotation": rot * .3}, {"x": 0, "y": 0, "rotation": 0}]
        kf = ", ".join(f'{{x: {k["x"]:.1f}, y: {k["y"]:.1f}, rotation: {k["rotation"]:.2f}, duration: .045}}' for k in ks)
        self.ft("#shk", t, .25, "{x: 0, y: 0, rotation: 0}", f"{{keyframes: [{kf}]}}", "none")

    def drift(self, t, d, rot=1.2, z=.07):
        """slow push for the length of a scene, so nothing ever sits still"""
        self.ft("#drift", t, d, f"{{scale: 1, rotation: {-rot / 2:.2f}}}", f"{{scale: {1 + z:.3f}, rotation: {rot / 2:.2f}}}", "none")

    def flash(self, t, a=.85, d=.2):
        self.ft("#flash", t, d, f"{{opacity: {a}}}", "{opacity: 0}", "power2.out")

    def burst(self, t, x=540, y=900, scale=1.0, col="#fff"):
        """speed-line burst behind a hit"""
        self.st("#burst", t, f'{{x: {x - 540}, y: {y - 960}, stroke: "{col}"}}')
        self.ft("#burst", t, .4, f"{{opacity: 1, scale: {.5 * scale:.2f}}}", f"{{opacity: 0, scale: {1.5 * scale:.2f}}}", "power2.out")

    def whip_out(self, sel, t, dirn=-1, d=.2):
        self.to(sel, t, d, f'{{x: {1400 * dirn}, rotation: {10 * dirn}, filter: "blur(26px)", opacity: 0}}', "power3.in")

    def whip_in(self, sel, t, dirn=1, d=.32, rot=0):
        self.ft(sel, t, d, f'{{opacity: 1, x: {1400 * dirn}, rotation: {10 * dirn + rot}, filter: "blur(26px)"}}',
                f'{{x: 0, rotation: {rot}, filter: "blur(0px)"}}', "expo.out")

    def zoom_out(self, sel, t, d=.18):
        self.to(sel, t, d, '{scale: 2.2, opacity: 0, filter: "blur(18px)"}', "power3.in")

    def pop_in(self, sel, t, d=.32, frm_scale=.4, rot=0, ease="back.out(2.4)"):
        self.ft(sel, t, d, f"{{opacity: 0, scale: {frm_scale}, rotation: {rot - 12}}}", f"{{opacity: 1, scale: 1, rotation: {rot}}}", ease)

    def pop_out(self, sel, t, d=.14):
        self.to(sel, t, d, "{opacity: 0, scale: .6}", "power2.in")

    def slam(self, html, t, hold, top=760, size=200, rot=-4, col="#fff", sfx="impact", stroke=True, cls="", shake=True):
        """giant word that slams in on a hit and leaves fast"""
        k = self.n_slam = self.n_slam + 1
        self.HTML.append(f'<div class="slam {cls}" data-layout-allow-overlap id="sl{k}" style="top:{top}px;font-size:{size}px;color:{col}"><span{" class=st" if stroke else ""}>{html}</span></div>')
        self.ft(f"#sl{k}", t - .04, .22, f"{{opacity: 0, scale: 2.6, rotation: {rot - 10}}}", f"{{opacity: 1, scale: 1, rotation: {rot}}}", "power4.out")
        self.to(f"#sl{k}", t + .18, hold, f"{{scale: 1.06, rotation: {rot + 1.5}}}", "none")
        self.to(f"#sl{k}", t + .18 + hold, .12, "{opacity: 0, scale: .7}", "power2.in")
        if sfx:
            self.sfx(sfx, t - .02)
        self.punch(t + .02, .07)
        if shake:
            self.shake(t + .04, 10, .8)
        return f"#sl{k}"

    def confetti(self, t, n=36, seed=3, x=540, y=760):
        rnd = random.Random(seed)
        cols = ["#fff", SUN, "#7a5cff", HOT, "#ffb3d1", "#3ad1a0"]
        bits = []
        for i in range(n):
            bits.append(f'<i class="cf" id="cf{seed}_{i}" style="background:{rnd.choice(cols)};width:{rnd.randint(14, 26)}px;height:{rnd.randint(22, 40)}px"></i>')
            dx, up, fall, r = rnd.uniform(-520, 520), rnd.uniform(240, 620), rnd.uniform(700, 1200), rnd.uniform(-720, 720)
            d = rnd.uniform(1.1, 1.6)
            self.st(f"#cf{seed}_{i}", t, f"{{opacity: 1, x: {x}, y: {y}, rotation: 0}}")
            self.to(f"#cf{seed}_{i}", t, d * .35, f"{{y: {y - up:.0f}, x: {x + dx * .6:.0f}}}", "power2.out")
            self.to(f"#cf{seed}_{i}", t + d * .35, d * .65, f"{{y: {y - up + fall:.0f}, x: {x + dx:.0f}}}", "power1.in")
            self.to(f"#cf{seed}_{i}", t, d, f"{{rotation: {r:.0f}}}", "none")
            self.to(f"#cf{seed}_{i}", t + d - .25, .25, "{opacity: 0}", "none")
        self.TOP.append('<div class="cfw">' + "".join(bits) + "</div>")

    # ---- captions: 1-3 words per card, white with ink outline, the spoken word on a yellow block
    def captions(self, top=1430, max_words=3, skip=()):
        caps = []
        for ln in self.SCRIPT:
            if ln["id"] in skip:
                continue
            disp, ws = ln["display"].replace('"', "").split(), self.LW[ln["id"]]
            n, m = len(disp), len(ws)
            timed = []
            for i, dw in enumerate(disp):
                j = i if n == m else round(i * (m - 1) / max(1, n - 1))
                timed.append((dw, ws[j]["t0"], ws[min(m - 1, j)]["t1"]))
            chunk = []
            for i, x in enumerate(timed):
                chunk.append(x)
                if len(chunk) >= max_words or x[0][-1] in ".,?!" or i == len(timed) - 1:
                    caps.append(chunk)
                    chunk = []
        for ci, chunk in enumerate(caps):
            spans = " ".join(f'<span class="cw" id="c{ci}_{k}">{w}</span>' for k, (w, _, _) in enumerate(chunk))
            self.TOP.append(f'<div class="cap" id="cap{ci}" style="top:{top}px">{spans}</div>')
            t0, t1 = chunk[0][1], chunk[-1][2]
            nxt = caps[ci + 1][0][1] if ci + 1 < len(caps) else self.DUR
            self.ft(f"#cap{ci}", t0 - .05, .14, "{opacity: 1, scale: .78}", "{scale: 1}", "back.out(3)")
            self.st(f"#cap{ci}", min(nxt - .05, t1 + .5), "{opacity: 0}")
            for k, (_, a, _) in enumerate(chunk):
                self.st(f"#c{ci}_{k}", a - .03, "{className: 'cw on'}")
                if k:
                    self.st(f"#c{ci}_{k - 1}", a - .03, "{className: 'cw'}")
        return caps

    # ---- moving pink world (always on)
    def background(self):
        D = self.DUR
        self.js(f'tl.fromTo("#b1", {{x: -120, y: 0}}, {{x: 260, y: 420, duration: {D:.2f}, ease: "sine.inOut", immediateRender: true}}, 0);')
        self.js(f'tl.fromTo("#b2", {{x: 120, y: 0}}, {{x: -300, y: -380, duration: {D:.2f}, ease: "sine.inOut", immediateRender: true}}, 0);')
        self.js(f'tl.fromTo("#b3", {{x: 0, y: 0, scale: 1}}, {{x: 200, y: -200, scale: 1.3, duration: {D:.2f}, ease: "sine.inOut", immediateRender: true}}, 0);')
        self.js(f'tl.fromTo("#dots", {{backgroundPosition: "0px 0px"}}, {{backgroundPosition: "{int(D * 40)}px {int(D * 80)}px", duration: {D:.2f}, ease: "none", immediateRender: true}}, 0);')

    BASE_CSS = f"""
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: Serif; font-style: italic; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {PINK}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: {INK}; background: {PINK}; }}
#bg {{ position: absolute; inset: -200px; background: linear-gradient(165deg, #ff2f7f 0%, #ff4f97 45%, #ff7ab3 75%, #ff3d8b 100%); overflow: hidden; }}
.bb {{ position: absolute; border-radius: 50%; filter: blur(110px); }}
#b1 {{ left: 0; top: 100px; width: 760px; height: 760px; background: rgba(255,214,234,.75); }}
#b2 {{ right: 0; top: 1100px; width: 820px; height: 820px; background: rgba(150,80,255,.45); }}
#b3 {{ left: 300px; top: 700px; width: 600px; height: 600px; background: rgba(255,120,80,.35); }}
#dots {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,.22) 3px, transparent 3.5px); background-size: 46px 46px; }}
#shk, #cam, #drift {{ position: absolute; inset: 0; transform-origin: 540px 900px; }}
#shk {{ z-index: 10; }}
.slam {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 800; letter-spacing: -.045em; line-height: .92; opacity: 0; z-index: 45; pointer-events: none; }}
.slam .st {{ -webkit-text-stroke: 16px {INK}; paint-order: stroke fill; text-shadow: 0 14px 0 {INK}, 0 26px 50px rgba(60,0,30,.35); }}
.slam em {{ font-style: normal; color: {SUN}; }}
#burst {{ position: absolute; left: 40px; top: 460px; width: 1000px; height: 1000px; opacity: 0; z-index: 5; pointer-events: none; stroke: #fff; }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 70; pointer-events: none; }}
.cfw {{ position: absolute; inset: 0; z-index: 48; pointer-events: none; }}
.cf {{ position: absolute; left: 0; top: 0; opacity: 0; border-radius: 4px; }}
.cap {{ position: absolute; left: 50px; right: 50px; text-align: center; font-weight: 800; font-size: 82px; line-height: 1.12; letter-spacing: -.03em;
  opacity: 0; z-index: 50; color: #fff; }}
.cw {{ display: inline-block; padding: 2px 14px; border-radius: 16px; -webkit-text-stroke: 12px {INK}; paint-order: stroke fill;
  text-shadow: 0 8px 0 {INK}; }}
.cw.on {{ background: {SUN}; color: {INK}; -webkit-text-stroke: 0; text-shadow: none; transform: scale(1.08) rotate(-2deg); box-shadow: 0 8px 0 {INK}; }}
#grain {{ position: absolute; inset: 0; background: url(assets/img/grain.png); opacity: .06; mix-blend-mode: multiply; pointer-events: none; z-index: 80; }}
"""

    def write(self, extra_css):
        burst = "".join(f'<line x1="{500 + 170 * c:.0f}" y1="{500 + 170 * s:.0f}" x2="{500 + 480 * c:.0f}" y2="{500 + 480 * s:.0f}"/>'
                        for c, s in [(__import__("math").cos(a / 18 * 6.2832), __import__("math").sin(a / 18 * 6.2832)) for a in range(18)])
        self.background()
        html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{self.title}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{self.BASE_CSS}{extra_css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{self.DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg"><i class="bb" id="b1"></i><i class="bb" id="b2"></i><i class="bb" id="b3"></i><i id="dots"></i></div>
      <svg id="burst" viewBox="0 0 1000 1000" fill="none" stroke-width="14" stroke-linecap="round">{burst}</svg>
      <div id="shk"><div id="cam"><div id="drift">
      {chr(10).join(self.HTML)}
      </div></div></div>
      {chr(10).join(self.TOP)}
      <div id="flash"></div>
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in self.JS).strip()}
      tl.set({{}}, {{}}, {self.DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
        open(os.path.join(self.ROOT, "index.html"), "w").write(html)
        self.SFX.sort(key=lambda e: e["t"])
        json.dump(self.SFX, open(os.path.join(self.ROOT, "plan", "sfx_events.json"), "w"), indent=0)
        json.dump({"dur": self.DUR, "scenes": {}}, open(os.path.join(self.ROOT, "plan", "edit.json"), "w"), indent=1)
        print(f"wrote index.html: {self.DUR:.2f} s, {len(self.JS)} timeline lines, {len(self.SFX)} sfx; line starts {[round(x, 2) for x in self.S]}")
