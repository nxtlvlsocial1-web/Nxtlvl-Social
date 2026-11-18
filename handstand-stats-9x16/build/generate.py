"""Handstand "post it like runners" reel (9:16): writes index.html and plan/sfx_events.json + plan/edit.json.

After the owner's reference (a handstand reel with a running-app stat card) and their notes: background people removed
(build/clean.py), the clip plays through the kick-up and freezes on the first full handstand, then the stat card builds
in with the owner's numbers: Hold Time 1m 07s, Handstand Height 6ft 7in, Attempts 67.
python3 build/generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FZ = 85 / 30            # freeze on frame 84 (2.8 s), the first straight handstand
DUR = round(FZ + 5.4, 2)
OR = "#FC5200"
JS, SFX = [], []


def js(s):
    JS.append(s)


def sfx(kind, t):
    SFX.append({"type": kind, "t": round(t, 3)})


def ft(sel, t, d, frm, to_, ease="power3.out"):
    js(f'tl.fromTo("{sel}", {frm}, {{...{to_}, duration: {d}, ease: "{ease}", immediateRender: false}}, {t:.3f});')


def to(sel, t, d, props, ease="power2.out"):
    js(f'tl.to("{sel}", {{...{props}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def st(sel, t, props):
    js(f'tl.set("{sel}", {props}, {t:.3f});')


ICON = {
    "hold": '<svg viewBox="0 0 48 48"><circle cx="24" cy="27" r="16" fill="none" stroke="currentColor" stroke-width="4"/>'
            '<path d="M24 27 L24 17" stroke="currentColor" stroke-width="4" stroke-linecap="round" class="hand"/>'
            '<path d="M18 5 H30 M24 5 V11 M37 12 L40 9" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>',
    "height": '<svg viewBox="0 0 48 48"><path d="M10 5 H38 M10 43 H38 M24 9 V39 M17 15 L24 8 L31 15 M17 33 L24 40 L31 33" fill="none" '
              'stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "att": '<svg viewBox="0 0 48 48"><path d="M40 24 A16 16 0 1 1 33 10.8" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round"/>'
           '<path d="M26 6 L35 10 L31 19" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
ROWS = [("hold", "Hold Time", '<b id="v0a">0</b><i>m</i> <b id="v0b">00</b><i>s</i>'),
        ("height", "Handstand Height", '<b id="v1a">0</b><i>ft</i> <b id="v1b">0</b><i>in</i>'),
        ("att", "Attempts", '<b id="v2a">0</b>')]
rows = "".join(f'<div class="row" id="row{i}"><div class="ic" id="ic{i}">{ICON[k]}</div><div class="tx"><div class="lb">{lab}</div>'
               f'<div class="val">{val}</div></div></div>' for i, (k, lab, val) in enumerate(ROWS))
HTML = f"""
<div id="cam">
  <video id="kick" src="assets/video/kick.mp4" data-start="0" data-duration="{FZ:.3f}" data-track-index="1" muted playsinline></video>
  <img id="frz" src="assets/img/freeze.png">
</div>
<div id="shade"></div>
<div id="flash"></div>
<div id="hook">Can I post my handstands<br>like runners?</div>
<div id="card"><div id="brand">STRAVA</div>{rows}</div>
<div id="bar"></div>
"""

# ---- timeline -------------------------------------------------------------------------------------------------------------
ft("#hook", 0, .3, "{opacity: 0, y: 10}", "{opacity: 1, y: 0}")
sfx("riser", FZ - 1.0)
sfx("whoosh", FZ - .22)
# the freeze: the still takes over from the video, a camera-flash pop, then a slow push-in
st("#frz", FZ, "{opacity: 1}")
st("#flash", FZ, "{opacity: .55}")
to("#flash", FZ + .02, .4, "{opacity: 0}", "power2.out")
ft("#frz", FZ, DUR - FZ, "{scale: 1}", "{scale: 1.06}", "sine.out")
sfx("shutter", FZ)
sfx("impact", FZ + .02)
to("#hook", FZ + .15, .3, "{opacity: 0, y: -10}", "power2.in")
ft("#shade", FZ + .1, .5, "{opacity: 0}", "{opacity: 1}")
# the stat card builds in
ft("#brand", FZ + .3, .4, "{opacity: 0, x: -40}", "{opacity: 1, x: 0}", "power3.out")
sfx("whoosh", FZ + .28)
ft("#bar", FZ + .35, .7, "{scaleY: 0}", "{scaleY: 1}", "power3.inOut")
COUNT = [  # (start, element ids and final values)
    (FZ + .6, [("#v0a", 1), ("#v0b", 7)], "hold"),
    (FZ + .95, [("#v1a", 6), ("#v1b", 7)], "height"),
    (FZ + 1.3, [("#v2a", 67)], "att"),
]
for i, (t, vals, k) in enumerate(COUNT):
    ft(f"#row{i}", t, .4, "{opacity: 0, x: -36}", "{opacity: 1, x: 0}", "power3.out")
    ft(f"#ic{i}", t + .05, .45, "{scale: 0, rotation: -40}", "{scale: 1, rotation: 0}", "back.out(2.6)")
    sfx("pop", t + .05)
    # numbers count up (seconds, inches and attempts), deterministic from the timeline position
    if k == "hold":
        js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 67, duration: .9, ease: "power2.out", onUpdate: () => {{ const s = Math.round(o.v); '
           f'document.querySelector("#v0a").textContent = Math.floor(s / 60); document.querySelector("#v0b").textContent = String(s % 60).padStart(2, "0"); }}}}, {t + .1:.3f}); }})();')
    elif k == "height":
        js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 79, duration: .9, ease: "power2.out", onUpdate: () => {{ const s = Math.round(o.v); '
           f'document.querySelector("#v1a").textContent = Math.floor(s / 12); document.querySelector("#v1b").textContent = s % 12; }}}}, {t + .1:.3f}); }})();')
    else:
        js(f'(() => {{ const o = {{v: 0}}; tl.to(o, {{v: 67, duration: .9, ease: "power2.out", onUpdate: () => {{ '
           f'document.querySelector("#v2a").textContent = Math.round(o.v); }}}}, {t + .1:.3f}); }})();')
    for j in range(5):
        sfx("click", t + .12 + j * .14)
    sfx("notify" if i == 2 else "click", t + 1.0)
# stopwatch hand ticks round while the card is up
js(f'tl.fromTo("#ic0 .hand", {{rotation: 0}}, {{rotation: 720, svgOrigin: "24 27", duration: {DUR - FZ - .7:.2f}, ease: "none", immediateRender: false}}, {FZ + .65:.3f});')

CSS = f"""
@font-face {{ font-family: Inter; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url("assets/fonts/inter-latin-700-normal.woff2"); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Inter; color: #fff; background: #000; }}
#cam {{ position: absolute; inset: 0; }}
#kick, #frz {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
#frz {{ opacity: 0; transform-origin: 60% 40%; }}
#shade {{ position: absolute; inset: 0; opacity: 0; background: linear-gradient(90deg, rgba(0,0,0,.6) 0%, rgba(0,0,0,.38) 26%, rgba(0,0,0,0) 40%); }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
#hook {{ position: absolute; left: 0; right: 0; top: 470px; text-align: center; font-weight: 600; font-size: 44px; line-height: 1.22; letter-spacing: -.01em;
  opacity: 0; text-shadow: 0 2px 4px rgba(0,0,0,.55), 0 0 18px rgba(0,0,0,.45); }}
#card {{ position: absolute; left: 40px; top: 640px; width: 270px; }}
#brand {{ font-weight: 800; font-style: italic; font-size: 54px; letter-spacing: -.02em; opacity: 0; text-shadow: 0 2px 10px rgba(0,0,0,.35); }}
.row {{ display: flex; align-items: center; gap: 14px; margin-top: 34px; opacity: 0; }}
.ic {{ width: 62px; height: 62px; color: {OR}; flex: none; filter: drop-shadow(0 2px 6px rgba(0,0,0,.35)); }}
.ic svg {{ width: 100%; height: 100%; overflow: visible; }}
.lb {{ font-weight: 600; font-size: 21px; text-shadow: 0 1px 6px rgba(0,0,0,.5); }}
.val {{ margin-top: 2px; font-weight: 800; font-size: 64px; line-height: 1; letter-spacing: -.02em; white-space: nowrap; text-shadow: 0 2px 12px rgba(0,0,0,.4); }}
.val b {{ font-weight: 800; }}
.val i {{ font-style: normal; font-weight: 700; font-size: 34px; margin-left: 2px; }}
#bar {{ position: absolute; left: 322px; top: 650px; width: 10px; height: 590px; border-radius: 6px; background: {OR}; transform-origin: 50% 0;
  transform: scaleY(0); box-shadow: 0 0 14px rgba(252,82,0,.45); }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Handstand stats 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      {HTML}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
os.makedirs(os.path.join(ROOT, "plan"), exist_ok=True)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx")
