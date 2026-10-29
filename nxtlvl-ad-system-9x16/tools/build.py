"""Writes index.html (footage, camera moves, scene hosts, music and SFX) and compositions/captions.html.

Film time = source time - TRIM. Word timings come from transcript.json (ElevenLabs Scribe, corrected).
Run from the project folder:  python3 tools/build.py && npx hyperframes check
"""
import html
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TRIM, SRC_END = 1.2, 24.96            # source seconds kept: [1.2, 24.96] (the whole take after the silent start)
DUR = round(SRC_END - TRIM, 2)        # 23.76 s
FPS = 30
WORDS = [dict(w, start=round(w['start'] - TRIM, 3), end=round(w['end'] - TRIM, 3))
         for w in json.load(open(os.path.join(ROOT, 'transcript.json')))]


def q(t):
    """Quantise to the frame grid."""
    return round(round(t * FPS) / FPS, 4)


# ---------------------------------------------------------------- captions
# (first word index, word count, group start, group end, keyword indices within the group)
GROUPS = [
    (0, 3, 0.20, 1.16, {2}),       # We took @ai.nxtlvl
    (3, 3, 1.16, 1.64, {1}),       # from zero to
    (6, 2, 1.64, 2.76, {0}),       # 7,100 followers
    (8, 4, 2.76, 3.96, {2, 3}),    # with just 22 posts.
    (16, 2, 5.38, 5.75, set()),    # and here's
    (18, 3, 5.75, 6.56, {1}),      # what's inside it.
    (58, 3, 18.60, 19.10, set()),  # Want this for
    (61, 3, 19.10, 19.84, {2}),    # your own brand?
    (64, 4, 19.94, 20.56, set()),  # Reach out to us
    (68, 4, 20.56, 21.52, {2, 3}), # and tap Send Message.
]


def captions():
    groups_html, js = [], []
    for g, (i0, n, gs, ge, kw) in enumerate(GROUPS):
        words = WORDS[i0:i0 + n]
        spans = ''.join(
            f'<span id="cw-{g}-{k}" class="cw{" kw" if k in kw else ""}">{html.escape(w["text"])}</span>'
            for k, w in enumerate(words))
        groups_html.append(f'<div id="cg-{g}" class="cg">{spans}</div>')
        gs, ge = q(gs), q(ge)
        js.append(f'tl.set("#cg-{g}", {{ visibility: "visible" }}, {gs});')
        js.append(f'tl.fromTo("#cg-{g}", {{ opacity: 0, filter: "blur(8px)" }}, '
                  f'{{ opacity: 1, filter: "blur(0px)", duration: 0.13, ease: "power2.out" }}, {gs});')
        for k, w in enumerate(words):
            ws, we = q(max(w['start'], gs)), q(min(w['end'] + 0.04, ge - 0.02))
            js.append(f'tl.to("#cw-{g}-{k}", {{ backgroundColor: "rgba(125,24,252,0.96)", scale: 1.07, '
                      f'duration: 0.06, ease: "power2.out" }}, {ws});')
            js.append(f'tl.to("#cw-{g}-{k}", {{ backgroundColor: "rgba(125,24,252,0)", scale: 1, '
                      f'duration: 0.08, ease: "power2.in" }}, {max(ws + 0.07, we)});')
        js.append(f'tl.to("#cg-{g}", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {q(ge - 0.1)});')
        js.append(f'tl.set("#cg-{g}", {{ opacity: 0, visibility: "hidden" }}, {ge});')
    return f"""<template>
  <link rel="stylesheet" href="assets/css/ad.css" />
  <style>
    @font-face {{ font-family: "Archivo"; src: url("assets/fonts/archivo-variable.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
    @font-face {{ font-family: "Instrument Sans"; src: url("assets/fonts/instrument-sans-700.woff2") format("woff2"); font-weight: 700; }}
    @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/instrument-serif-400.woff2") format("woff2"); font-weight: 400; }}
    #root {{ position: absolute; inset: 0; overflow: visible; pointer-events: none; }}
    /* one caption line, centred on the chest band (y 1200-1310), under the chin and above Meta's buttons */
    .cg {{ position: absolute; left: 60px; right: 60px; top: 1196px; text-align: center; visibility: hidden;
          font-family: "Archivo", sans-serif; font-weight: 800; font-stretch: 104%; font-size: 70px; line-height: 1.18;
          letter-spacing: -.01em; color: #FFFFFF; white-space: nowrap; }}
    .cw {{ display: inline-block; margin: 0 .07em; padding: 0 .14em; border-radius: 16px; background: rgba(125,24,252,0);
          -webkit-text-stroke: 9px rgba(5,3,12,.82); paint-order: stroke fill; text-shadow: 0 6px 22px rgba(5,3,12,.55); }}
    .cw.kw {{ color: #E2CCFF; }}
  </style>
  <script src="assets/vendor/gsap.min.js"></script>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{DUR}">
    {chr(10).join('    ' + h for h in groups_html).strip()}
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
    (2.42, 'pop', 0.30), (2.46, 'sparkle', 0.16),          # followers land on 7,100
    (3.52, 'pop', 0.26),                                   # 22 posts
    (4.34, 'whoosh-short', 0.20),                          # punch-in on "Not"
    (4.94, 'impact-bass-1', 0.30),                         # "A system."
    (6.62, 'whoosh-cinematic', 0.22),                      # the camera pulls back into the window
    (7.00, 'pop', 0.24), (9.42, 'whoosh-short', 0.16), (9.46, 'pop', 0.22),
    (11.46, 'whoosh-short', 0.16), (11.50, 'pop', 0.22),   # the three service cards
    (14.24, 'whoosh-short', 0.18), (15.42, 'pop', 0.22),   # price card, ₹25,000
    (16.42, 'click-soft', 0.30),                           # strike-through
    (17.64, 'pop', 0.28), (17.66, 'sparkle', 0.24),        # ₹999
    (18.52, 'whoosh-cinematic', 0.20),                     # camera opens back to full frame
    (20.00, 'notification', 0.20),                         # Tap Send Message chip
    (21.56, 'impact-bass-2', 0.30), (21.58, 'sparkle', 0.22),  # end card
]


def audio():
    tags = [f'<audio id="el-bgm" src="assets/music/nxtlvl-brand.wav" data-start="0" data-duration="{DUR}" '
            f'data-media-start="4" data-volume="0.14" data-fade-out="1.2" data-track-index="10"></audio>']
    for i, (hit, name, vol) in enumerate(CUES):
        peak, length = SFX_PEAK[name]
        start = max(0.0, round(hit + 1 / FPS - peak, 3))
        length = round(min(length, DUR - start), 3)
        tags.append(f'<audio id="el-sfx-{i}" src="assets/sfx/{name}.mp3" data-start="{start}" '
                    f'data-duration="{length}" data-volume="{vol}" data-track-index="{20 + i}"></audio>')
    return '\n      '.join(tags)


# ---------------------------------------------------------------- root
SCENES = [  # id, start, end, z
    ('stage', 6.44, 19.06, 1),
    ('01-hook', 0, 4.40, 5),
    ('02-system', 4.30, 5.42, 5),
    ('03-inside', 6.48, 14.26, 6),
    ('04-price', 14.14, 18.62, 6),
    ('05-cta', 19.80, DUR, 9),
]


def index():
    hosts = '\n      '.join(
        f'<div id="el-{sid}" class="scene clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
        f'data-start="{s}" data-duration="{round(e - s, 2)}" data-track-index="{2 + n}" data-track-kind="graphics" '
        f'style="z-index:{z}"></div>' for n, (sid, s, e, z) in enumerate(SCENES))
    return f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #05030C; }}
      @font-face {{ font-family: "Archivo"; src: url("assets/fonts/archivo-variable.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
      @font-face {{ font-family: "Instrument Sans"; src: url("assets/fonts/instrument-sans-600.woff2") format("woff2"); font-weight: 600; }}
      @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/instrument-serif-400.woff2") format("woff2"); font-weight: 400; }}
      body {{ font-family: "Archivo", "Instrument Sans", sans-serif; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #05030C; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      /* the camera: GSAP scales and moves this wrapper (origin top-left) and crops it with clip-path */
      #cam {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 2; transform-origin: 0 0; overflow: hidden; }}
      #a-roll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="cam" data-layout-allow-overflow>
        <video id="a-roll" class="clip" src="assets/video/footage.mp4" playsinline data-has-audio="true"
          data-start="0" data-duration="{DUR}" data-media-start="{TRIM}" data-track-index="0"></video>
      </div>

      {hosts}
      <div id="el-captions" class="scene clip" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="captions" style="z-index:8"></div>

      {audio()}
    </div>
    <script>
      (function () {{
        var tl = gsap.timeline({{ paused: true }});
        // punch-ins scale about the chin (540, 1150) so the face rises and the caption band stays clear
        function punch(s) {{ return {{ scale: s, x: 540 * (1 - s), y: 1150 * (1 - s) }}; }}
        var FULL = "inset(0px 0px 0px 0px round 0px)";
        // the face window: source rect x 90-990, y 360-1200, shown at 0.72 at (216, 262) -> 648 x 605
        var WIN = "inset(360px 90px 720px 90px round 56px)";
        tl.set("#cam", {{ scale: 1, x: 0, y: 0, clipPath: FULL }}, 0);
        tl.set("#cam", punch(1.16), 4.3333);                       // "Not luck" - hard cut in
        tl.set("#cam", punch(1.26), 4.9333);                       // "A system." - tighter
        tl.set("#cam", punch(1), 5.4);                             // "and here's what's inside it" - back out
        tl.to("#cam", {{ scale: 0.72, x: 151.2, y: 2.8, clipPath: WIN, duration: 0.6, ease: "power3.inOut" }}, 6.5);
        tl.to("#cam", {{ scale: 1, x: 0, y: 0, clipPath: FULL, duration: 0.6, ease: "power3.inOut" }}, 18.45);
        tl.set("#cam", punch(1.1), 19.9667);                       // "Reach out to us" - punch in
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
