"""Writes index.html (scene hosts, voice, ducked music, SFX) and compositions/captions.html for the
Nxtlvl Social launch film (16:9). Voice lines are placed on the film clock in tools/voice.sh terms (LINES below).
Run:  python3 tools/build.py && npx hyperframes check
"""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DUR = 32.0

# id, text, start on the film clock, captioned?
LINES = [
    ('l1', "Everyone's posting.", 0.25, False),         # the hook says it on screen
    ('l2', 'Almost no one gets seen.', 1.60, False),
    ('l3', 'Meet Nxtlvl Social.', 4.15, False),           # the logo says it
    ('l4', 'The creative studio that takes your brand to the next level.', 6.00, True),
    ('l5', 'Designs that stop the scroll.', 9.60, True),
    ('l6', 'Reels, cut on the beat.', 11.60, True),
    ('l7', 'Automation that replies while you sleep.', 13.60, True),
    ('l8', 'Websites that turn views into clients.', 15.85, True),
    ('l9', 'Zero to 7,000 followers. In 22 posts.', 18.25, True),
    ('l10', 'Not luck. A system.', 22.15, False),
    ('l11', 'Nxtlvl Social. Your brand, next level.', 24.40, False),   # the end card says it
    ('l12', 'Find us at nxtlvlsocial.ai', 28.30, False),
]
KEYWORDS = {'creative', 'studio', 'next', 'level.', 'stop', 'scroll.', 'beat.', 'sleep.', 'clients.', '7,000', '22', 'social.', 'level.'}

SCENES = [  # id, start, duration, z
    ('bg', 0, DUR, 0),
    ('s1-hook', 0, 4.0, 3),
    ('s2-meet', 4.0, 5.6, 3),
    ('s3-services', 9.6, 8.6, 3),
    ('s4-proof', 18.2, 3.8, 3),
    ('s5-system', 22.0, 2.3, 4),
    ('s6-end', 24.3, DUR - 24.3, 4),
]

SFX = [  # file, start, volume
    ('whoosh-short.mp3', 0.05, .18), ('notification.mp3', 0.6, .12), ('pop.mp3', 1.65, .18),
    ('whoosh-cinematic.mp3', 3.75, .26), ('impact-bass-2.mp3', 4.0, .4), ('sparkle.mp3', 4.55, .26),
    ('whoosh-short.mp3', 9.55, .2), ('pop.mp3', 9.85, .2), ('pop.mp3', 10.05, .2), ('pop.mp3', 10.25, .2),
    ('whoosh-short.mp3', 11.55, .2), ('click-soft.mp3', 12.0, .28), ('click-soft.mp3', 12.5, .28), ('click-soft.mp3', 13.0, .28),
    ('whoosh-short.mp3', 13.55, .2), ('notification.mp3', 13.85, .2), ('pop.mp3', 14.75, .22),
    ('whoosh-short.mp3', 15.8, .2), ('click-soft.mp3', 16.75, .32), ('chime.mp3', 17.0, .22),
    ('whoosh-short.mp3', 18.15, .2), ('sparkle.mp3', 21.2, .24),
    ('impact-bass-1.mp3', 22.0, .4), ('whoosh-short.mp3', 22.55, .22),
    ('whoosh-cinematic.mp3', 24.15, .24), ('sparkle.mp3', 24.8, .24), ('chime.mp3', 27.5, .24), ('pop.mp3', 28.35, .22),
]


def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))


def words_timed(text, start, length):
    """Spread a line's words over its spoken length by letter weight, with a little air after punctuation."""
    words = text.split()
    weights = [len(re.sub(r'[^A-Za-z]', '', w)) + 3.5 * len(re.sub(r'[^0-9]', '', w)) + 1.6 + (1.4 if w[-1] in ',.' else 0) for w in words]
    total = sum(weights)
    t, out = start, []
    for w, k in zip(words, weights):
        out.append((w, round(t, 3)))
        t += length * k / total
    return out


def captions():
    groups = []
    for lid, text, start, cap in LINES:
        if not cap:
            continue
        length = dur(os.path.join(ROOT, 'work', f'{lid}.wav'))
        ws = words_timed(text, start, length)
        # split into short groups (at most 4 words, break after commas and full stops)
        cur = []
        for w, t in ws:
            cur.append((w, t))
            if len(cur) == 4 or w[-1] in ',.':
                groups.append(cur)
                cur = []
        if cur:
            groups.append(cur)
    # each group shows from its first word until the next group (or 0.35 s after its last word ends)
    html, tl = [], []
    for gi, g in enumerate(groups):
        g0 = g[0][1] - 0.06
        nxt = groups[gi + 1][0][1] - 0.06 if gi + 1 < len(groups) else g[-1][1] + 0.9
        end = min(nxt, g[-1][1] + 1.0)
        spans = ' '.join(f'<span class="cw{" kw" if w.lower() in KEYWORDS else ""}" id="w{gi}-{wi}">{w}</span>'
                         for wi, (w, _) in enumerate(g))
        html.append(f'<div id="g{gi}" class="cg clip" data-start="{g0:.3f}" data-duration="{end - g0:.3f}" data-track-index="0">{spans}</div>')
        tl.append(f'tl.fromTo("#g{gi}", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.16, ease: "power3.out" }}, {g0:.3f});')
        for wi, (w, t) in enumerate(g):
            col = '#D8BBFF' if w.lower() in KEYWORDS else '#FFFFFF'
            tl.append(f'tl.fromTo("#w{gi}-{wi}", {{ color: "rgba(245,242,255,.38)", scale: .94 }}, '
                      f'{{ color: "{col}", scale: 1, duration: 0.12, ease: "power2.out" }}, {t:.3f});')
        tl.append(f'tl.to("#g{gi}", {{ opacity: 0, y: -14, duration: 0.1, ease: "power2.in" }}, {end - 0.11:.3f});')
    return f'''<template>
  <style>
    @font-face {{ font-family: "Serif Italic"; src: url("assets/fonts/instrument-serif-italic-400.woff2") format("woff2"); }}
    #root {{ position: absolute; inset: 0; }}
    .cg {{ position: absolute; left: 160px; right: 160px; top: 900px; height: 100px; text-align: center; opacity: 0;
      font-family: "Serif Italic", serif; font-size: 64px; line-height: 100px; letter-spacing: -.005em; white-space: nowrap;
      text-shadow: 0 4px 24px rgba(5,3,12,.85); }}
    .cw {{ display: inline-block; margin: 0 .05em; color: rgba(245,242,255,.38); }}
  </style>
  <script src="assets/vendor/gsap.min.js"></script>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-duration="{DUR}">
    {chr(10).join("    " + h for h in html)}
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + l for l in tl)}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
'''


def index():
    hosts = []
    for i, (sid, start, d, z) in enumerate(SCENES):
        hosts.append(f'<div id="el-{sid}" class="scene clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{d}" data-track-index="{i + 1}" data-track-kind="graphics" style="z-index:{z}"></div>')
    hosts.append(f'<div id="el-captions" class="scene clip" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{DUR}" data-track-index="9" data-track-kind="captions" style="z-index:8"></div>')
    audio = [f'<audio id="el-vo" src="assets/voice/vo.wav" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="10"></audio>',
             f'<audio id="el-bgm" src="assets/music/bed-ducked.wav" data-start="0" data-duration="{DUR}" data-volume="0.34" data-track-index="11"></audio>']
    for i, (f, t, v) in enumerate(SFX):
        d = min(dur(os.path.join(ROOT, 'assets', 'sfx', f)), DUR - t)
        audio.append(f'<audio id="el-sfx-{i}" src="assets/sfx/{f}" data-start="{t}" data-duration="{d:.2f}" data-volume="{v}" data-track-index="{20 + i}"></audio>')
    nl = '\n      '
    return f'''<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #05030C; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #05030C; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      {nl.join(hosts)}
      {nl.join(audio)}
    </div>
    <script>
      var tl = gsap.timeline({{ paused: true }});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''


def main():
    with open(os.path.join(ROOT, 'index.html'), 'w') as f:
        f.write(index())
    with open(os.path.join(ROOT, 'compositions', 'captions.html'), 'w') as f:
        f.write(captions())
    print('wrote index.html and compositions/captions.html')


if __name__ == '__main__':
    main()
