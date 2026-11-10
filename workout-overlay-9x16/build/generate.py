"""Workout overlay reel, 9:16 (1080x1920): the owner's footage (a solo full-body bodyweight circuit, recorded 4K HDR, here
a 1080p SDR working copy) with a minimal overlay in the style of the reference reel the owner sent: the six moves in two
columns, the current one in yellow, a ring timer for each 20 s work block and a yellow countdown for each 10 s rest,
plus (owner's request) the targeted muscles under the timer as each move comes up. No pulsing: things fade or slide in
once and stay still.

Timing (owner: "list workout and timings same as reel video", "synced with the activity done and the music"):
the reel runs 20 s work / 10 s rest per move; in the footage he starts each move every 30 s on the music's beat at
5.13 s (+30 s each move, measured: motion analysis plus the music's beat grid, cache/beats.json), so work k runs
5.13 + 30k .. +20 s, rest the 10 s after it.

python3 build/generate.py  ->  index.html
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FW, FH, FPS = 1080, 1920, 30
DUR = 178.4
W0, CYCLE, WORK, REST = 5.132, 30.0, 20.0, 10.0
YEL = "#F6DE3F"
MOVES = [("Jump Squats", "Quads + Glutes + Power"),
         ("Spiderman Pushups", "Chest + Triceps + Core"),
         ("Glute Bridges", "Glutes + Hamstrings"),
         ("Shoulder Taps", "Core + Shoulder + Stability"),
         ("Burpees", "Full Body + Cardio"),
         ("Prone Swimmers", "Upper Back + Rear Delts + Posterior Chain")]
A, HIDE = [], []


def js(s):
    A.append("      " + s)


def scenes():
    # the title, on screen from the first frame (like the reel's opening card), lifts away before the panel arrives
    js('tl.to("#title", {opacity: 0, y: -40, duration: .35, ease: "power2.in"}, 2.55);')
    # the panel settles in once, with the timer full at 20 and move 1 up next
    js('tl.fromTo("#panel", {opacity: 0, y: -24}, {opacity: 1, y: 0, duration: .45, ease: "power3.out", immediateRender: false}, 2.95);')
    HIDE.append("#panel")
    js(f'tl.set("#mv0", {{color: "{YEL}"}}, 2.95);')
    for k, (name, muscles) in enumerate(MOVES):
        w = W0 + k * CYCLE
        r = w + WORK
        # work: white ring drains over 20 s, the count steps down every second, this move in yellow, its muscles pop up
        js(f'tl.set("#work", {{opacity: 1}}, {w:.3f}); tl.set("#rest", {{opacity: 0}}, {w:.3f});')
        js(f'tl.fromTo("#wring", {{strokeDashoffset: 0}}, {{strokeDashoffset: 1000, duration: {WORK}, ease: "none", immediateRender: false}}, {w:.3f});')
        for s in range(int(WORK)):
            js(f'tl.set("#wnum", {{textContent: "{int(WORK) - s}"}}, {w + s:.3f});')
        for j in range(len(MOVES)):
            js(f'tl.set("#mv{j}", {{color: "{YEL if j == k else "#ffffff"}", opacity: {1 if j == k else .82}}}, {w:.3f});')
        js(f'tl.set("#mus", {{textContent: "{muscles}"}}, {w - .01:.3f});')
        js(f'tl.fromTo("#mus", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: .35, ease: "power2.out", immediateRender: false}}, {w:.3f});')
        js(f'tl.to("#mus", {{opacity: 0, duration: .25, ease: "power1.in"}}, {r - .05:.3f});')
        if k == len(MOVES) - 1:
            # the last move: when it ends the timer shows 0, then the panel leaves
            js(f'tl.set("#wnum", {{textContent: "0"}}, {r:.3f});')
            js(f'tl.to("#panel", {{opacity: 0, y: -24, duration: .5, ease: "power2.in"}}, {r + .6:.3f});')
            continue
        # rest: the yellow disc with a two-digit count and a draining yellow ring; the next move turns yellow, ready
        js(f'tl.set("#work", {{opacity: 0}}, {r:.3f}); tl.set("#rest", {{opacity: 1}}, {r:.3f});')
        js(f'tl.fromTo("#rdisc", {{scale: .86}}, {{scale: 1, duration: .25, ease: "power2.out", immediateRender: false}}, {r:.3f});')
        js(f'tl.fromTo("#rring", {{strokeDashoffset: 0}}, {{strokeDashoffset: 1000, duration: {REST}, ease: "none", immediateRender: false}}, {r:.3f});')
        for s in range(int(REST)):
            # a zero-width space keeps "09" a string (GSAP would read it as the number 9)
            js(f'tl.set("#rnum", {{textContent: "\\u200b{int(REST) - s:02d}"}}, {r + s:.3f});')
        for j in range(len(MOVES)):
            js(f'tl.set("#mv{j}", {{color: "{YEL if j == k + 1 else "#ffffff"}", opacity: {1 if j == k + 1 else .82}}}, {r:.3f});')


CSS = f"""
@font-face {{ font-family: "Ubuntu"; font-weight: 500; src: url("assets/fonts/ubuntu-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Ubuntu"; font-weight: 700; src: url("assets/fonts/ubuntu-latin-700-normal.woff2"); }}
@font-face {{ font-family: "Montserrat"; font-weight: 900; font-style: italic; src: url("assets/fonts/montserrat-latin-900-italic.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #000; font-family: "Ubuntu"; color: #fff; }}
#foot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
/* the opening card, like the reel's */
#title {{ position: absolute; left: 0; right: 0; top: 300px; text-align: center; z-index: 5; font-family: "Montserrat"; font-weight: 900; font-style: italic;
  color: {YEL}; -webkit-text-stroke: 9px #111; paint-order: stroke fill; letter-spacing: -.01em; }}
#title .t1 {{ font-size: 132px; line-height: 1; }}
#title .t2 {{ font-size: 56px; line-height: 1.15; margin-top: 10px; -webkit-text-stroke-width: 7px; }}
/* the panel */
#panel {{ position: absolute; left: 60px; right: 60px; top: 250px; height: 280px; z-index: 5; border-radius: 40px;
  background: rgba(16,16,18,.55); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); opacity: 0; }}
.col {{ position: absolute; top: 34px; display: flex; flex-direction: column; gap: 22px; font-weight: 500; font-size: 33px; line-height: 1.12;
  white-space: nowrap; text-shadow: 0 2px 8px rgba(0,0,0,.35); }}
.col.l {{ left: 40px; }}
.col.r {{ left: 585px; }}
.mv {{ color: #fff; opacity: .82; }}
#timer {{ position: absolute; left: 400px; top: 22px; width: 160px; height: 160px; }}
#timer svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
.trk {{ fill: none; stroke: rgba(255,255,255,.22); stroke-width: 10; }}
#wring {{ fill: none; stroke: #fff; stroke-width: 10; stroke-linecap: round; }}
#rring {{ fill: none; stroke: {YEL}; stroke-width: 8; stroke-linecap: round; }}
#rdisc {{ fill: {YEL}; transform-box: fill-box; transform-origin: center; }}
.num {{ position: absolute; inset: 0; display: grid; place-items: center; font-weight: 700; font-variant-numeric: tabular-nums; }}
#wnum {{ font-size: 70px; color: #fff; }}
#rnum {{ font-size: 56px; color: #141414; }}
#work, #rest {{ position: absolute; inset: 0; }}
#rest {{ opacity: 0; }}
#mus {{ position: absolute; left: 0; right: 0; top: 214px; text-align: center; font-weight: 500; font-size: 30px; letter-spacing: .01em; color: #fff;
  opacity: 0; white-space: nowrap; }}
"""


def main():
    scenes()
    left = "".join(f'<div class="mv" id="mv{k}">{k + 1}. {n}</div>' for k, (n, _) in enumerate(MOVES[:3]))
    right = "".join(f'<div class="mv" id="mv{k + 3}">{k + 4}. {n}</div>' for k, (n, _) in enumerate(MOVES[3:]))
    # rings run on a 1000-unit path: GSAP rounds px values, so a 0..1 path would jump instead of drain
    ring = 'cx="100" cy="100" pathLength="1000" stroke-dasharray="1000" transform="rotate(-90 100 100)"'
    timer = (f'<div id="timer"><div id="work"><svg viewBox="0 0 200 200"><circle class="trk" cx="100" cy="100" r="88"/>'
             f'<circle id="wring" r="88" {ring} stroke-dashoffset="0"/></svg><div class="num" id="wnum">20</div></div>'
             f'<div id="rest"><svg viewBox="0 0 200 200"><circle id="rdisc" cx="100" cy="100" r="74"/><circle id="rring" r="92" {ring} stroke-dashoffset="0"/></svg>'
             f'<div class="num" id="rnum">&#8203;10</div></div></div>')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Workout overlay 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <video id="foot" src="assets/video/footage_1080.mp4" data-start="0" data-duration="{DUR}" data-track-index="0" muted playsinline></video>
      <div id="title"><div class="t1">5 SETS</div><div class="t2">Full Body Intermediate workout</div></div>
      <div id="panel"><div class="col l">{left}</div>{timer}<div class="col r">{right}</div><div id="mus"></div></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(HIDE)}, {{opacity: 0}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    json.dump([{"move": n, "muscles": m, "work": [round(W0 + k * CYCLE, 3), round(W0 + k * CYCLE + WORK, 3)]} for k, (n, m) in enumerate(MOVES)],
              open(os.path.join(ROOT, "plan", "schedule.json"), "w"), indent=1)
    print(f"wrote index.html, {len(A)} timeline lines, {DUR} s")


if __name__ == "__main__":
    main()
