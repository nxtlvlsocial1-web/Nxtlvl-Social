"""AI.NXTLVL fork of creedom-postmortem-9x16/build/kit_min.py (night background with violet glows, Montserrat 800 +
Instrument Serif Italic accents, white captions). Original note: clean premium minimal kit (v4) for the Creedom remakes, shared by creedom-postmortem-9x16 and creedom-grade-9x16
(identical copies). Owner's picks: background "Glacier" (cool white, ice-blue and lilac glows, fine grain), type
Unbounded (display, OFL) + Satoshi (text, Fontshare ITF Free Font License: video and social allowed, the files must not
be redistributed, so assets/fonts/fontshare/ is gitignored), JetBrains Mono for small labels.

Motion language: things rise into place (y + blur, expo.out), lines of text slide up out of a mask, cards float in soft
3D, the camera pushes in slowly every scene, numbers count. No stickers, flashes, shake or confetti. Colour carries
meaning only: red for the bad number, green for the fix, Creedom pink only once the product is named.
One paused GSAP timeline; every tween is a pure function of time.
"""
import json
import os
import re

INK, MUTE, RED, GREEN, PINK = "#ffffff", "rgba(255,255,255,.66)", "#ff5a5f", "#3ddc97", "#b687f9"   # AI.NXTLVL: white on night, lavender accent
STAR, VIOLET, NIGHT = "#7a2ffb", "#7f1bf8", "#07050f"


class Reel:
    def __init__(self, root, title):
        self.ROOT, self.title = root, title
        self.W = json.load(open(os.path.join(root, "plan", "words.json")))
        self.SCRIPT = json.load(open(os.path.join(root, "plan", "script.json")))
        self.LW = {}
        for w in self.W:
            self.LW.setdefault(w["line"], []).append(w)
        self.JS, self.SFX, self.HTML, self.TOP = [], [], [], []
        self.IDS = [ln["id"] for ln in self.SCRIPT]
        self.L = {i: (self.LW[i][0]["t0"], self.LW[i][-1]["t1"]) for i in self.IDS}
        self.S = [self.L[i][0] for i in self.IDS] + [self.L[self.IDS[-1]][1] + .8]
        self.DUR = round(self.S[-1], 2)
        self.n = 0
        self.HIDDEN = []
        self.RISE_END = {}        # an exit never starts before the element's entrance has finished (it would be overridden)          # v6: hidden from frame 0 in CSS (a set at time 0 does not render on the very first frame)

    # ---- primitives
    def js(self, s):
        self.JS.append(s)

    def sfx(self, kind, t):
        self.SFX.append({"type": kind, "t": round(max(0, t), 3)})

    @staticmethod
    def _join(obj, extra):
        body = obj.strip()[1:-1].strip()
        return "{" + (body + ", " if body else "") + extra + "}"

    def ft(self, sel, t, d, frm, to_, ease="expo.out"):
        if re.search(r"opacity:\s*1\b", frm) and "opacity" not in to_:
            to_ = self._join(to_, "opacity: 1")
        self.js(f'tl.fromTo("{sel}", {frm}, {self._join(to_, f"duration: {d}, ease: \"{ease}\", immediateRender: false")}, {t:.3f});')

    def to(self, sel, t, d, props, ease="power2.inOut"):
        self.js(f'tl.to("{sel}", {self._join(props, f"duration: {d}, ease: \"{ease}\"")}, {t:.3f});')

    def st(self, sel, t, props):
        if t <= .0001 and props.replace(" ", "") == "{opacity:0}":
            self.HIDDEN.append(sel)
        self.js(f'tl.set("{sel}", {props}, {t:.3f});')

    def wt(self, line, word, n=0, end=False):
        hits = [w for w in self.LW[line] if re.sub(r"[^a-z0-9.]", "", w["w"].lower()).startswith(word.lower())]
        if not hits:
            raise SystemExit(f"{line}: no word starting {word!r}: {[w['w'] for w in self.LW[line]]}")
        h = hits[min(n, len(hits) - 1)]
        return h["t1"] if end else h["t0"]

    def counter(self, el_id, t, d, a, b, fmt="Math.round(o.v)", ease="power3.out"):
        self.js(f'(() => {{ const o = {{v: {a}}}; tl.to(o, {{v: {b}, duration: {d}, ease: "{ease}", onUpdate: () => {{ '
                f'document.getElementById("{el_id}").textContent = {fmt}; }}}}, {t:.3f}); }})();')

    def typer(self, el_id, t, text, d):
        n = len(text)
        self.js(f'(() => {{ const o = {{n: 0}}; tl.to(o, {{n: {n}, duration: {d}, ease: "steps({n})", onUpdate: () => {{ '
                f'document.getElementById("{el_id}").textContent = "{text}".slice(0, Math.round(o.n)); }}}}, {t:.3f}); }})();')

    # ---- motion language
    def rise(self, sel, t, d=.8, y=60, blur=12, delay=0):
        if t + delay > .02:                       # hidden until it rises (frame-1 elements are set visible by the scene)
            self.st(sel, 0, "{opacity: 0}")
        self.ft(sel, t + delay, d, f'{{opacity: 1, y: {y}, filter: "blur({blur}px)"}}', '{y: 0, filter: "blur(0px)"}', "expo.out")
        self.RISE_END[sel] = t + delay + d

    def leave(self, sel, t, d=.4, y=-40):
        t = max(t, self.RISE_END.get(sel, 0) + .02)
        self.to(sel, t, d, f'{{opacity: 0, y: {y}, filter: "blur(10px)"}}', "power2.in")

    def mask_lines(self, sel, t, stagger=.09, d=.85):
        """lines (.ln > span) slide up out of their mask; the block is hidden until then"""
        self.st(sel, 0, "{opacity: 0}")
        self.st(sel, t - .001, "{opacity: 1}")
        self.js(f'tl.fromTo("{sel} .ln > span", {{yPercent: 112}}, {{yPercent: 0, duration: {d}, ease: "expo.out", stagger: {stagger}, immediateRender: true}}, {t:.3f});')

    def lines_html(self, el_id, lines, cls="hd"):
        inner = "".join(f'<span class="ln"><span>{ln}</span></span>' for ln in lines)
        return f'<div class="{cls}" id="{el_id}">{inner}</div>'

    def push(self, t0, t1, z=.045):
        """slow camera push for one scene (pure function of time)"""
        self.ft("#cam", t0, max(.1, t1 - t0), "{scale: 1}", f"{{scale: {1 + z:.3f}}}", "none")

    def focus(self, t, scale=1.0, x=0, y=0, d=.7, ease="expo.inOut"):
        """the lens moves in on a detail (a cut-like move inside a scene); focus(t) with defaults goes back to wide"""
        self.to("#lens", t, d, f"{{scale: {scale}, x: {x}, y: {y}}}", ease)

    def float3d(self, sel, t0, t1, rx=(10, 4), ry=(-14, -6), rz=(1.5, -.5)):
        self.ft(sel, t0, max(.1, t1 - t0), f"{{rotationX: {rx[0]}, rotationY: {ry[0]}, rotation: {rz[0]}}}",
                f"{{rotationX: {rx[1]}, rotationY: {ry[1]}, rotation: {rz[1]}}}", "sine.inOut")

    # ---- v7 (owner's reference video): a mascot companion, light-beam wipes, smear cuts, word highlights, dense UI sound
    def cree_init(self, x, y, pose, size=230):
        """Cree lives in the top layer for the whole reel (visible from frame 0): #creew hops (x, y), #creeb bobs, the img
        squashes and changes pose"""
        self.cree_size = size
        self.TOP.append(f'<div id="creew" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px"><div id="creeb">'
                        f'<img id="creei" src="assets/img/poses/{pose}.png" alt=""></div></div>')
        D = self.DUR
        self.js(f'tl.fromTo("#creeb", {{y: 0}}, {{y: -12, duration: .55, repeat: {int(D / .55)}, yoyo: true, ease: "sine.inOut", immediateRender: true}}, 0);')
        self.cree_xy = (0, 0)

    def cree_hop(self, t, dx, dy, pose=None, d=.55, peak=150):
        """hop to a new spot (offset from the start spot), turn into a new pose in the air, squash on landing"""
        x0, y0 = self.cree_xy
        self.to("#creew", t, d, f"{{x: {dx}}}", "power1.inOut")
        top = min(y0, dy) - peak
        self.js(f'tl.to("#creew", {{keyframes: [{{y: {top}, duration: {d / 2:.3f}, ease: "power2.out"}}, {{y: {dy}, duration: {d / 2:.3f}, ease: "power2.in"}}]}}, {t:.3f});')
        if pose:
            self.st("#creei", t + d * .45, f'{{attr: {{src: "assets/img/poses/{pose}.png"}}}}')
        self.ft("#creei", t + d - .02, .45, "{scaleX: 1.18, scaleY: .78}", "{scaleX: 1, scaleY: 1}", "elastic.out(1, .45)")
        self.sfx("boing", t)
        self.sfx("pop", t + d - .02)
        self.cree_xy = (dx, dy)

    def cree_react(self, t, pose, sound="g_pop"):
        """a quick squash-and-stretch with a new pose, in place"""
        self.ft("#creei", t, .5, "{scaleX: .82, scaleY: 1.2}", "{scaleX: 1, scaleY: 1}", "elastic.out(1, .4)")
        self.st("#creei", t + .04, f'{{attr: {{src: "assets/img/poses/{pose}.png"}}}}')
        if sound:
            self.sfx(sound, t)

    def beam(self, t, col="rgba(232,48,125,.55)"):
        """a diagonal light beam sweeps across on a scene change (the reference's neon wipe, in the brand pink)"""
        self.n += 1
        i = f"bm{self.n}"
        self.TOP.append(f'<i class="beam" id="{i}" style="background:linear-gradient(90deg, rgba(255,255,255,0), {col} 45%, #fff 50%, {col} 55%, rgba(255,255,255,0))"></i>')
        self.ft(f"#{i}", t, .5, "{opacity: 1, x: -1700}", "{x: 1700}", "power2.inOut")
        self.st(f"#{i}", 0, "{opacity: 0}")
        self.to(f"#{i}", t + .5, .01, "{opacity: 0}", "none")
        self.ft("#wash", t + .18, .4, "{opacity: .5}", "{opacity: 0}", "power2.out")
        self.sfx("whoosh_big", t)

    def smear_out(self, sel, t, d=.3, dx=-320):
        self.to(sel, max(t, self.RISE_END.get(sel, 0) + .02), d, f'{{opacity: 0, x: {dx}, filter: "blur(22px)"}}', "power2.in")

    def smear_in(self, sel, t, d=.55, dx=340):
        self.ft(sel, t, d, f'{{opacity: 1, x: {dx}, filter: "blur(22px)"}}', '{x: 0, filter: "blur(0px)"}', "expo.out")
        self.st(sel, 0, "{opacity: 0}")
        self.RISE_END[sel] = t + d

    def highlight_words(self, el_id, words, times, hot=(), sound="tick"):
        """hook words light up as they are spoken (frame 0 keeps the full line for the cover, then it dims and fills)"""
        for k, (w, t) in enumerate(zip(words, times)):
            sel = f"#{el_id}_{k}"
            self.st(sel, .04, "{opacity: .22}")
            self.ft(sel, t - .03, .35, "{opacity: 1, y: 10, scale: .9}", "{y: 0, scale: 1}", "back.out(2.5)")
            if sound and k % 2 == 0:
                self.sfx(sound, t - .02)

    def topbar(self, keyword, t_kw, logo="assets/img/creedom_logo.png"):
        """v6 (owner: viewers who leave early should still get the tool): the Creedom logo is on screen from frame 1 for
        the whole reel, and the comment keyword joins it early, so anyone who leaves still saw what to comment"""
        self.TOP.append(f'<div id="tbar"><img src="{logo}" alt=""><span>AI TOOLS</span><b id="kw">Comment <i>{keyword}</i></b></div>')
        self.ft("#kw", t_kw, .6, '{opacity: 1, x: 30, filter: "blur(6px)"}', '{x: 0, filter: "blur(0px)"}', "expo.out")
        self.st("#kw", 0, "{opacity: 0}")

    def kicker(self, text, t, t_out=None, dot=RED):
        self.n += 1
        i = f"kk{self.n}"
        self.HTML.append(f'<div class="kick" id="{i}"><i style="background:{dot}"></i>{text}</div>')
        self.rise(f"#{i}", t, .7, 20, 6)
        if t_out:
            self.leave(f"#{i}", t_out, .3, -14)
        return f"#{i}"

    def draw(self, sel, t, d=.9, ease="power2.inOut"):
        """an SVG stroke (pathLength=1, dasharray=1) draws itself"""
        self.ft(sel, t, d, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", ease)

    # ---- captions: quiet karaoke, the spoken words turn ink, the rest stay muted
    def captions(self, top=1470, max_words=5):
        caps = []
        for ln in self.SCRIPT:
            disp, ws = ln["display"].replace('"', "").split(), self.LW[ln["id"]]
            timed = [(d, w["t0"], w["t1"]) for d, w in zip(disp, ws)]
            chunk = []
            for i, x in enumerate(timed):
                chunk.append(x)
                if len(chunk) >= max_words or (x[0][-1] in ".,?!" and len(chunk) >= 2) or i == len(timed) - 1:
                    caps.append(chunk)
                    chunk = []
        for ci, chunk in enumerate(caps):
            spans = " ".join(f'<span class="cw" id="c{ci}_{k}">{w}</span>' for k, (w, _, _) in enumerate(chunk))
            self.TOP.append(f'<div class="cap" id="cap{ci}" style="top:{top}px">{spans}</div>')
            t0, t1 = chunk[0][1], chunk[-1][2]
            nxt = caps[ci + 1][0][1] if ci + 1 < len(caps) else self.DUR
            self.ft(f"#cap{ci}", t0 - .08, .35, "{opacity: 1, y: 14}", "{y: 0}", "expo.out")
            self.st(f"#cap{ci}", min(nxt - .06, t1 + .6), "{opacity: 0}")
            for k, (_, a, _) in enumerate(chunk):                 # each word appears as it is spoken
                self.ft(f"#c{ci}_{k}", a - .04, .28, "{opacity: 1, y: 12}", "{y: 0}", "power3.out")
                self.st(f"#c{ci}_{k}", 0, "{opacity: 0}")

    CSS = f"""
@font-face {{ font-family: Unb; font-weight: 900; src: url("assets/fonts/unbounded-latin-900-normal.woff2"); }}
@font-face {{ font-family: Mont; font-weight: 100 900; src: url("assets/fonts/montserrat.ttf"); }}
@font-face {{ font-family: Ser; font-style: italic; src: url("assets/fonts/instrument-serif-latin-400-italic.woff2"); }}
@font-face {{ font-family: Unb; font-weight: 800; src: url("assets/fonts/unbounded-latin-800-normal.woff2"); }}
@font-face {{ font-family: Sat; font-weight: 500; src: url("assets/fonts/fontshare/Satoshi-Medium.woff2"); }}
@font-face {{ font-family: Sat; font-weight: 700; src: url("assets/fonts/fontshare/Satoshi-Bold.woff2"); }}
@font-face {{ font-family: Sat; font-weight: 900; src: url("assets/fonts/fontshare/Satoshi-Black.woff2"); }}
@font-face {{ font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {NIGHT}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Sat; color: {INK}; background: {NIGHT}; }}
#bg {{ position: absolute; inset: -240px; }}
.gl {{ position: absolute; border-radius: 50%; filter: blur(120px); }}
#g1 {{ left: -200px; top: -100px; width: 900px; height: 900px; background: rgba(127,27,248,.55); }}
#g2 {{ left: 500px; top: 1300px; width: 1000px; height: 1000px; background: rgba(96,8,242,.5); }}
#g3 {{ left: 380px; top: 800px; width: 560px; height: 560px; background: rgba(182,135,249,.16); }}
#grain {{ position: absolute; inset: 0; background: url(assets/img/noise.png); opacity: .08; mix-blend-mode: overlay; pointer-events: none; z-index: 90; }}
#cam, #lens {{ position: absolute; inset: 0; transform-origin: 540px 860px; z-index: 10; }}
.kick {{ position: absolute; left: 90px; top: 250px; font-family: Mono; font-size: 26px; letter-spacing: .26em; color: {MUTE}; opacity: 0; z-index: 30; }}
.kick i {{ display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 18px; vertical-align: 3px; }}
.ln {{ display: block; overflow: hidden; padding-bottom: .06em; }}
.ln > span {{ display: inline-block; }}
.hd {{ position: absolute; left: 88px; right: 80px; font-family: Mont; font-weight: 800; font-size: 88px; line-height: 1.02; letter-spacing: -.04em; z-index: 20; }}
.hd em {{ font-family: Ser; font-style: italic; font-weight: 400; color: {PINK}; letter-spacing: -.01em; }}
.num {{ position: absolute; left: 80px; font-family: Unb; font-weight: 900; letter-spacing: -.06em; line-height: 1; z-index: 20; }}
.cap {{ position: absolute; left: 90px; right: 90px; font-family: Sat; font-weight: 700; font-size: 62px; line-height: 1.18; letter-spacing: -.02em; opacity: 0; z-index: 60; }}
.cw {{ display: inline-block; color: {INK}; }}
.stage {{ position: absolute; left: 0; right: 0; perspective: 1900px; z-index: 15; }}
.soft {{ box-shadow: 0 50px 100px rgba(0,0,0,.6), 0 0 80px rgba(127,27,248,.25); }}
#tbar {{ position: absolute; left: 90px; right: 90px; top: 214px; height: 64px; display: flex; align-items: center; gap: 18px; z-index: 72; }}
#tbar img {{ height: 46px; }}
#tbar span {{ font-family: Mono; font-size: 22px; letter-spacing: .2em; color: rgba(255,255,255,.7); }}
#tbar b {{ margin-left: auto; font-family: Sat; font-weight: 700; font-size: 34px; color: {INK}; background: rgba(16,2,44,.9); padding: 12px 24px; border-radius: 999px;
  box-shadow: 0 12px 30px rgba(0,0,0,.4); border: 2px solid {STAR}; }}
#tbar b i {{ font-style: normal; font-weight: 900; color: {PINK}; }}
#creew {{ position: absolute; z-index: 58; pointer-events: none; }}
#creeb, #creei {{ position: absolute; inset: 0; }}
#creei {{ width: 100%; height: 100%; object-fit: contain; transform-origin: 50% 95%; filter: drop-shadow(0 18px 24px rgba(40,50,90,.22)); }}
.beam {{ position: absolute; left: 340px; top: -400px; width: 420px; height: 2800px; transform: rotate(22deg); z-index: 74; pointer-events: none; mix-blend-mode: screen; }}
#wash {{ position: absolute; inset: 0; background: {STAR}; opacity: 0; z-index: 73; pointer-events: none; }}
.hw {{ display: inline-block; }}
#prog {{ position: absolute; left: 90px; right: 90px; top: 190px; height: 3px; background: rgba(255,255,255,.1); z-index: 70; border-radius: 2px; }}
#prog i {{ position: absolute; inset: 0; background: {INK}; transform-origin: left center; transform: scaleX(0); border-radius: 2px; }}
"""

    def write(self, extra_css):
        D = self.DUR
        self.js(f'tl.fromTo("#g1", {{x: 0, y: 0}}, {{x: -260, y: 300, duration: {D:.2f}, ease: "sine.inOut", immediateRender: true}}, 0);')
        self.js(f'tl.fromTo("#g2", {{x: 0, y: 0}}, {{x: 300, y: -340, duration: {D:.2f}, ease: "sine.inOut", immediateRender: true}}, 0);')
        self.js(f'tl.fromTo("#g3", {{x: 0, y: 0, scale: 1}}, {{x: -180, y: 160, scale: 1.25, duration: {D:.2f}, ease: "sine.inOut", immediateRender: true}}, 0);')
        self.js(f'tl.fromTo("#prog i", {{scaleX: 0}}, {{scaleX: 1, duration: {D:.2f}, ease: "none", immediateRender: true}}, 0);')
        html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{self.title}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{self.CSS}{extra_css}{"".join(f"{sel} {{ opacity: 0; }}" for sel in dict.fromkeys(self.HIDDEN))}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div id="bg"><i class="gl" id="g1"></i><i class="gl" id="g2"></i><i class="gl" id="g3"></i></div>
      <div id="cam"><div id="lens">
      {chr(10).join(self.HTML)}
      </div></div>
      {chr(10).join(self.TOP)}
      <div id="wash"></div>
      <div id="prog"><i></i></div>
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in self.JS).strip()}
      tl.set({{}}, {{}}, {D:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
        open(os.path.join(self.ROOT, "index.html"), "w").write(html)
        self.SFX.sort(key=lambda e: e["t"])
        json.dump(self.SFX, open(os.path.join(self.ROOT, "plan", "sfx_events.json"), "w"), indent=0)
        json.dump({"dur": D, "scenes": {}}, open(os.path.join(self.ROOT, "plan", "edit.json"), "w"), indent=1)
        print(f"wrote index.html: {D:.2f} s, {len(self.JS)} timeline lines, {len(self.SFX)} sfx; line starts {[round(x, 2) for x in self.S]}")
