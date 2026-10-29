"""Writes index.html (split screen: the cut take on top, panels below, camera zooms, music, SFX) and
compositions/captions.html from transcript-cut.json (made by tools/cut.py).

Layout on 1080x1920: the brand panel fills the top half (graphics in y 300-740, captions just above the seam at
y 860-956); the take fills the bottom half (960-1920), cropped so the face sits high in it, above Meta's caption and
Send message button.
Run from the project folder:  python3 tools/cut.py && python3 tools/build.py && npx hyperframes check
"""
import html
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CUT = json.load(open(os.path.join(ROOT, 'transcript-cut.json')))
WORDS, SEGS = CUT['words'], CUT['segments']
DUR = round(CUT['duration'], 2)       # 21.83 s
END = 19.66                            # the end card takes the whole frame from here
FPS = 30


def q(t):
    return round(round(t * FPS) / FPS, 4)


# ---------------------------------------------------------------- captions
# (first word index, word count, keyword indices within the group); times come from the words
GROUPS = [
    (0, 3, {2}), (3, 3, {1}), (6, 2, {0}), (8, 4, {2, 3}),          # hook
    (16, 2, set()), (18, 3, {1}),                                    # and here's what's inside it  ("Not luck, a system" is the panel)
    (21, 3, set()), (24, 4, {3}), (28, 3, set()),                    # designs
    (31, 3, {1, 2}), (34, 4, {2, 3}),                                # calendar
    (38, 4, {0}), (42, 5, {2}),                                      # reels
    (47, 3, set()), (50, 3, {0}), (53, 4, set()), (57, 1, {0}),      # price
    (58, 3, set()), (61, 3, {2}), (64, 4, set()), (68, 4, {2, 3}),   # CTA
]


def captions():
    spans_html, js = [], []
    bounds = []
    for g, (i0, n, kw) in enumerate(GROUPS):
        ws = WORDS[i0:i0 + n]
        bounds.append((ws[0]['start'] - 0.06, ws[-1]['end'] + 0.06))
    for g, (i0, n, kw) in enumerate(GROUPS):
        ws = WORDS[i0:i0 + n]
        gs = q(max(0.08, bounds[g][0]))
        nxt = bounds[g + 1][0] if g + 1 < len(bounds) else END
        ge = q(min(max(bounds[g][1], gs + 0.45), nxt, END))           # never overlaps the next group
        spans = ''.join(f'<span id="cw-{g}-{k}" class="cw{" kw" if k in kw else ""}">{html.escape(w["text"])}</span>'
                        for k, w in enumerate(ws))
        spans_html.append(f'<div id="cg-{g}" class="cg">{spans}</div>')
        js.append(f'tl.set("#cg-{g}", {{ visibility: "visible" }}, {gs});')
        js.append(f'tl.fromTo("#cg-{g}", {{ opacity: 0, y: 14, filter: "blur(6px)" }}, '
                  f'{{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.14, ease: "power2.out" }}, {gs});')
        for k, w in enumerate(ws):
            t = q(max(w['start'], gs))
            lit = '#D3AEFF' if k in kw else '#FFFFFF'
            js.append(f'tl.to("#cw-{g}-{k}", {{ color: "{lit}", scale: 1.08, duration: 0.07, ease: "power2.out" }}, {t});')
            js.append(f'tl.to("#cw-{g}-{k}", {{ scale: 1, duration: 0.16, ease: "power3.out" }}, {q(t + 0.1)});')
        js.append(f'tl.to("#cg-{g}", {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, {q(ge - 0.08)});')
        js.append(f'tl.set("#cg-{g}", {{ opacity: 0, visibility: "hidden" }}, {ge});')
    return f"""<template>
  <link rel="stylesheet" href="assets/css/ad.css" />
  <style>
    @font-face {{ font-family: "Archivo"; src: url("assets/fonts/archivo-variable.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
    @font-face {{ font-family: "Instrument Sans"; src: url("assets/fonts/instrument-sans-700.woff2") format("woff2"); font-weight: 700; }}
    @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/instrument-serif-400.woff2") format("woff2"); font-weight: 400; }}
    #root {{ position: absolute; inset: 0; overflow: visible; pointer-events: none; }}
    /* captions in the "Not luck." serif, just under the seam; words light up as they are said */
    .cg {{ position: absolute; left: 40px; right: 40px; top: 860px; height: 96px; text-align: center; visibility: hidden;
          font-family: "Instrument Serif", serif; font-style: italic; font-size: 76px; line-height: 96px; white-space: nowrap; }}
    .cw {{ display: inline-block; margin: 0 .1em; color: rgba(245,242,255,.42); transform-origin: 50% 70%;
          text-shadow: 0 4px 24px rgba(5,3,12,.8); }}
  </style>
  <script src="assets/vendor/gsap.min.js"></script>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{END}">
    {chr(10).join('    ' + h for h in spans_html).strip()}
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      {chr(10).join('      ' + s for s in js).strip()}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""


# ---------------------------------------------------------------- sound
SFX_PEAK = {  # measured peak (s into the file), file length (s)
    'pop': (0.13, 0.72), 'whoosh-short': (0.17, 0.57), 'whoosh-cinematic': (2.55, 5.54), 'sparkle': (0.09, 1.80),
    'impact-bass-1': (0.08, 2.12), 'impact-bass-2': (2.04, 2.59), 'notification': (0.24, 2.46), 'click-soft': (0.06, 0.37),
}
CUES = [  # (film time the sound should hit, sound, volume)
    (2.30, 'pop', 0.30), (2.32, 'sparkle', 0.16),              # 7,100 lands
    (3.00, 'pop', 0.24),                                       # 22 posts
    (3.84, 'whoosh-short', 0.18),                              # cut + punch-in on "Not luck"
    (4.31, 'click-soft', 0.30),                                # strike
    (4.51, 'impact-bass-1', 0.30),                             # "A system."
    (5.55, 'whoosh-short', 0.16),                              # the three rows appear
    (6.18, 'pop', 0.22), (7.16, 'pop', 0.16), (8.16, 'click-soft', 0.28),
    (8.31, 'pop', 0.22), (10.09, 'click-soft', 0.28),
    (10.25, 'pop', 0.22), (12.69, 'click-soft', 0.28),          # rows light up, then tick
    (12.83, 'whoosh-short', 0.18), (13.92, 'pop', 0.22),       # price tiles, ₹25,000
    (15.13, 'click-soft', 0.30),                               # strike
    (15.99, 'pop', 0.28), (16.01, 'sparkle', 0.24),            # ₹999
    (16.85, 'whoosh-short', 0.16),                             # "your brand"
    (18.08, 'notification', 0.18),                             # the Send message button
    (18.88, 'click-soft', 0.34),                               # "tap"
    (19.68, 'impact-bass-2', 0.30), (19.70, 'sparkle', 0.22),  # end card
]


def audio():
    tags = [f'<audio id="el-bgm" src="assets/music/nxtlvl-brand.wav" data-start="0" data-duration="{DUR}" '
            f'data-media-start="4" data-volume="0.13" data-fade-out="1.2" data-track-index="10"></audio>']
    for i, (hit, name, vol) in enumerate(CUES):
        peak, length = SFX_PEAK[name]
        start = max(0.0, round(hit + 1 / FPS - peak, 3))
        length = round(min(length, DUR - start), 3)
        tags.append(f'<audio id="el-sfx-{i}" src="assets/sfx/{name}.mp3" data-start="{start}" '
                    f'data-duration="{length}" data-volume="{vol}" data-track-index="{20 + i}"></audio>')
    return '\n      '.join(tags)


# ---------------------------------------------------------------- root
SCENES = [  # id, start, end, z
    ('panel', 0, END, 3),
    ('p1-hook', 0, 3.84, 5),
    ('p2-system', 3.84, 5.6, 5),
    ('p3-inside', 5.45, 12.8, 5),
    ('p4-price', 12.77, 16.82, 5),
    ('p5-cta', 16.8, DUR, 9),
]
# one framing per cut: the jump cuts alternate the zoom so each lands as a new shot
ZOOMS = [1.0, 1.15, 1.0, 1.1, 1.0, 1.1, 1.22, 1.0, 1.12]


def index():
    hosts = '\n      '.join(
        f'<div id="el-{sid}" class="scene clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
        f'data-start="{s}" data-duration="{round(e - s, 2)}" data-track-index="{2 + n}" data-track-kind="graphics" '
        f'style="z-index:{z}"></div>' for n, (sid, s, e, z) in enumerate(SCENES))
    zoom_js = []
    for seg, s in zip(SEGS, ZOOMS):
        zoom_js.append(f'tl.set("#cam", frame({s}), {q(seg["film"])});')
    zoom_js.append('tl.set("#cam", frame(1.26), 4.5);                 // "A system." - tighter, inside the same cut')
    return f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Archivo"; src: url("assets/fonts/archivo-variable.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
      @font-face {{ font-family: "Instrument Sans"; src: url("assets/fonts/instrument-sans-600.woff2") format("woff2"); font-weight: 600; }}
      @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/instrument-serif-400.woff2") format("woff2"); font-weight: 400; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #05030C; }}
      body {{ font-family: "Archivo", "Instrument Sans", sans-serif; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #05030C; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      /* the bottom half: a fixed window onto the take; the camera inside it zooms per cut */
      #pane {{ position: absolute; left: 0; top: 960px; width: 1080px; height: 960px; overflow: hidden; z-index: 2; background: #05030C; }}
      #cam {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }}
      #a-roll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="pane" data-layout-allow-overflow>
        <div id="cam" data-layout-allow-overflow>
          <video id="a-roll" class="clip" src="assets/video/aroll.mp4" playsinline data-has-audio="true"
            data-start="0" data-duration="{DUR}" data-track-index="0"></video>
        </div>
      </div>

      {hosts}
      <div id="el-captions" class="scene clip" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{END}" data-track-index="1" data-track-kind="captions" style="z-index:7"></div>

      {audio()}
    </div>
    <script>
      (function () {{
        var tl = gsap.timeline({{ paused: true }});
        // keep the face centre (source 540, 850) at (540, 275) in the bottom window (canvas y 1235): eyes ~y 1300,
        // mouth ~1450, so the face stays above Meta's caption and button
        function frame(s) {{ return {{ scale: s, x: 540 * (1 - s), y: 275 - 850 * s }}; }}
        {chr(10).join('        ' + z for z in zoom_js).strip()}
        window.__timelines = window.__timelines || {{}};
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
"""


if __name__ == '__main__':
    open(os.path.join(ROOT, 'index.html'), 'w').write(index())
    open(os.path.join(ROOT, 'compositions', 'captions.html'), 'w').write(captions())
    print(f'index.html and compositions/captions.html written ({DUR} s, {len(CUES)} sfx, {len(GROUPS)} caption groups)')
