"""Writes the two logo scenes, compositions/s5-reveal.html and s6-live.html, from the real N Disc geometry
(tools/disc.json, exported from brands/nxtlvl-edits/source: the N outline, its centre line and the star).
Run:  python3 tools/scenes.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
D = json.load(open(os.path.join(HERE, 'disc.json')))
SPARK = 'M0-1C.06-.34.34-.06 1 0 .34.06.06.34 0 1-.06.34-.34.06-1 0-.34-.06-.06-.34 0-1Z'
CX, CY, DIAM = 540, 700, 420          # where scene 4's card closes into the disc


def pearl(p):
    stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in D['pearl'])
    return f'<linearGradient id="{p}pl" gradientUnits="userSpaceOnUse" x1="0" y1="600" x2="600" y2="0">{stops}</linearGradient>'


def real_disc(p, extra=''):
    """The disc with the N and star cut out (600-unit viewBox)."""
    sx, sy, sr = D['star']
    return (f'<defs>{pearl(p)}<mask id="{p}cut" maskUnits="userSpaceOnUse" x="0" y="0" width="600" height="600">'
            f'<rect width="600" height="600" fill="#fff"/>'
            f'<path d="{D["outline"]}" transform="translate({D["ox"]:.1f} {D["oy"]:.1f}) scale({D["k"]})" fill="#000"/>'
            f'<path d="{SPARK}" transform="translate({sx:.1f} {sy:.1f}) scale({sr:.1f})" fill="#000"/></mask>{extra}</defs>'
            f'<circle cx="300" cy="300" r="300" fill="url(#{p}pl)" mask="url(#{p}cut)"/>')


HEAD = '''<template>
  <style>
    @font-face {{ font-family: "Archivo"; src: url("assets/fonts/archivo-variable.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
    @font-face {{ font-family: "Instrument Sans"; src: url("assets/fonts/instrument-sans-600.woff2") format("woff2"); font-weight: 600; }}
    @font-face {{ font-family: "Serif Italic"; src: url("assets/fonts/instrument-serif-italic-400.woff2") format("woff2"); }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .disc {{ position: absolute; left: {L}px; top: {T}px; width: {S}px; height: {S}px; overflow: visible; }}
{css}
  </style>
  <script src="assets/vendor/gsap.min.js"></script>
'''


def s5():
    L, T = CX - DIAM / 2, CY - DIAM / 2
    sx, sy, sr = D['star']
    k = DIAM / 600
    css = f'''    #r-rays {{ position: absolute; left: {CX - 700}px; top: {CY - 700}px; width: 1400px; height: 1400px; border-radius: 50%; opacity: 0;
      background: repeating-conic-gradient(from 0deg, rgba(216,187,255,.16) 0deg 4deg, rgba(216,187,255,0) 4deg 18deg);
      -webkit-mask: radial-gradient(closest-side, #000 20%, transparent 100%); mask: radial-gradient(closest-side, #000 20%, transparent 100%); }}
    #r-halo {{ position: absolute; left: {CX - 420}px; top: {CY - 420}px; width: 840px; height: 840px; border-radius: 50%; opacity: 0;
      background: radial-gradient(closest-side, rgba(169,92,255,.55), rgba(125,24,252,.18) 55%, rgba(125,24,252,0)); }}
    .r-orbit {{ position: absolute; left: {CX - 360}px; top: {CY - 360}px; width: 720px; height: 720px; overflow: visible; opacity: 0; }}
    #r-glint {{ position: absolute; left: {L + sx * k - 90:.1f}px; top: {T + sy * k - 90:.1f}px; width: 180px; height: 180px; overflow: visible; opacity: 0; }}
    #r-sheenwrap {{ position: absolute; left: {L}px; top: {T}px; width: {DIAM}px; height: {DIAM}px; border-radius: 50%; overflow: hidden; }}
    #r-sheen {{ position: absolute; left: -300px; top: -100px; width: 140px; height: 640px; opacity: 0;
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.85), rgba(255,255,255,0)); }}
    #r-sheenrot {{ position: absolute; inset: 0; transform: rotate(28deg); }}'''
    orbit = lambda i, rx, ry, rot: (f'<svg id="r-orbit{i}" class="r-orbit" viewBox="-360 -360 720 720" data-layout-allow-overflow>'
                                    f'<g transform="rotate({rot})"><ellipse rx="{rx}" ry="{ry}" fill="none" stroke="rgba(216,187,255,.45)" stroke-width="2.5"/>'
                                    f'<circle cx="{rx}" cy="0" r="7" fill="#F5F2FF"/></g></svg>')
    body = f'''  <div id="root" data-composition-id="s5-reveal" data-width="1080" data-height="1920" data-duration="4.6">
    <div id="r-wrap" class="clip" data-start="0" data-duration="4.6" data-track-index="0" style="position:absolute;inset:0" data-layout-allow-overflow>
      <div id="r-rays"></div>
      <div id="r-halo"></div>
      {orbit(0, 330, 120, -18)}
      {orbit(1, 300, 150, 32)}
      <svg id="r-plain" class="disc" viewBox="0 0 600 600"><defs>{pearl('r5p')}</defs><circle cx="300" cy="300" r="300" fill="url(#r5ppl)"/>
        <path id="r-carve" d="{D['centre']}" transform="translate({D['ox']:.1f} {D['oy']:.1f}) scale({D['k']})" pathLength="1"
          fill="none" stroke="#120828" stroke-width="17" stroke-linecap="butt" stroke-linejoin="round" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg>
      <svg id="r-real" class="disc" viewBox="0 0 600 600" style="opacity:0">{real_disc('r5r')}</svg>
      <div id="r-sheenwrap"><div id="r-sheenrot"><div id="r-sheen"></div></div></div>
      <svg id="r-glint" viewBox="-1 -1 2 2" data-layout-allow-overflow><path d="{SPARK}" fill="#FFFFFF"/></svg>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      // the plain pearl disc from scene 4 settles, light gathers behind it
      tl.fromTo("#r-halo", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 1.2, ease: "power2.out" }}, 0);
      tl.fromTo("#r-rays", {{ opacity: 0, rotation: 0 }}, {{ opacity: 1, rotation: 40, duration: 4.6, ease: "none" }}, 0.2);
      tl.fromTo(["#r-orbit0", "#r-orbit1"], {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "power3.out", stagger: 0.12 }}, 0.3);
      tl.fromTo("#r-orbit0", {{ rotation: 0 }}, {{ rotation: 200, duration: 4.3, ease: "none" }}, 0.3);
      tl.fromTo("#r-orbit1", {{ rotation: 0 }}, {{ rotation: -160, duration: 4.3, ease: "none" }}, 0.3);
      // "Next Level Edits": the N is carved into the disc in one stroke
      tl.fromTo("#r-carve", {{ strokeDashoffset: 1.1 }}, {{ strokeDashoffset: 0, duration: 1.15, ease: "power2.inOut" }}, 0.55);
      tl.fromTo("#r-real", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12, ease: "none" }}, 1.72);
      tl.to("#r-plain", {{ opacity: 0, duration: 0.05 }}, 1.84);
      // the star is cut, it glints, a sheen runs across the pearl
      tl.fromTo("#r-glint", {{ opacity: 0, scale: 0.2, rotation: -30 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.25, ease: "back.out(2.5)" }}, 1.72);
      tl.to("#r-glint", {{ opacity: 0, scale: 0.4, rotation: 45, duration: 0.45, ease: "power2.in" }}, 2.0);
      tl.fromTo("#r-sheen", {{ x: 0, opacity: 1 }}, {{ x: 760, opacity: 1, duration: 0.7, ease: "power2.inOut" }}, 2.05);
      tl.fromTo(["#r-real", "#r-sheenwrap"], {{ scale: 1 }}, {{ scale: 1.05, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }}, 1.72);
      // it breathes on the lift into the impact
      tl.to(["#r-real", "#r-sheenwrap"], {{ scale: 0.94, duration: 2.0, ease: "sine.inOut" }}, 2.4);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["s5-reveal"] = tl;
    }})();
  </script>
</template>
'''
    return HEAD.format(L=L, T=T, S=DIAM, css=css) + body


def s6():
    L, T = CX - DIAM / 2, CY - DIAM / 2
    css = '''    #v-ring0, #v-ring1, #v-ring2 { position: absolute; left: 540px; top: 700px; width: 440px; height: 440px; margin: -220px 0 0 -220px;
      border-radius: 50%; border: 5px solid rgba(216,187,255,.8); opacity: 0; }
    #v-flash { position: absolute; inset: 0; background: #F5F2FF; opacity: 0; }
    #v-live { position: absolute; left: 0; right: 0; top: 800px; text-align: center; font-family: "Archivo", sans-serif; font-weight: 900;
      font-stretch: 112%; font-size: 136px; line-height: 1; letter-spacing: -.035em; color: #F5F2FF; white-space: nowrap; }
    #v-live i { display: inline-block; width: 44px; height: 44px; border-radius: 50%; background: #FF4D6D; margin-right: 26px; vertical-align: 18px;
      box-shadow: 0 0 24px rgba(255,77,109,.9); }
    #v-handle { position: absolute; left: 0; right: 0; top: 980px; text-align: center; font-family: "Serif Italic", serif; font-size: 84px; line-height: 1.1;
      color: #D8BBFF; }
    #v-btn { position: absolute; left: 540px; top: 1124px; height: 104px; width: 380px; margin-left: -190px; border-radius: 52px; background: #F5F2FF;
      display: flex; align-items: center; justify-content: center; gap: 16px; font-family: "Archivo", sans-serif; font-weight: 800; font-stretch: 112%;
      font-size: 44px; color: #05030C; box-shadow: 0 16px 50px rgba(125,24,252,.55); }
    #v-tap { position: absolute; left: 640px; top: 1170px; width: 90px; height: 90px; border-radius: 50%; background: rgba(245,242,255,.35);
      border: 4px solid #FFFFFF; opacity: 0; }'''
    body = f'''  <div id="root" data-composition-id="s6-live" data-width="1080" data-height="1920" data-duration="4.5">
    <div id="v-wrap" style="position:absolute;inset:0" data-layout-allow-overflow>
      <div id="v-stage" class="clip" data-start="0" data-duration="4.5" data-track-index="0" style="position:absolute;inset:0"></div>
      <div id="v-ring0"></div><div id="v-ring1"></div><div id="v-ring2"></div>
      <svg id="v-disc" class="disc" viewBox="0 0 600 600">{real_disc('r6')}</svg>
      <div id="v-live"><i id="v-dot"></i>NOW LIVE</div>
      <div id="v-handle">@nxtlvlledits</div>
      <div id="v-btn">Follow <span style="font-size:36px">✦</span></div>
      <div id="v-tap"></div>
      <div id="v-flash" class="clip" data-start="0" data-duration="0.4" data-track-index="1"></div>
    </div>
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      // the impact: a flash, the disc punches, shockwaves roll out
      tl.fromTo("#v-flash", {{ opacity: 0.7 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, 0);
      tl.fromTo("#v-disc", {{ scale: 0.94 }}, {{ scale: 1.14, duration: 0.1, ease: "power2.out" }}, 0);
      tl.to("#v-disc", {{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, 0.1);
      for (var r = 0; r < 3; r++) {{
        tl.fromTo("#v-ring" + r, {{ opacity: 0.9, scale: 1 }}, {{ opacity: 0, scale: 3 + r, duration: 0.9, ease: "power2.out" }}, r * 0.12);
      }}
      // the disc rises to make room for the news
      tl.to("#v-disc", {{ y: -250, scale: 0.72, duration: 0.55, ease: "expo.inOut" }}, 0.55);
      tl.fromTo("#v-live", {{ opacity: 0, y: 80, scale: 0.9 }}, {{ opacity: 1, y: -60, scale: 1, duration: 0.45, ease: "expo.out" }}, 0.8);
      tl.fromTo("#v-dot", {{ scale: 1 }}, {{ scale: 1.35, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, 1.2);
      tl.fromTo("#v-handle", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: -60, duration: 0.4, ease: "expo.out" }}, 1.15);
      tl.fromTo("#v-btn", {{ opacity: 0, y: 40, scale: 0.85 }}, {{ opacity: 1, y: -60, scale: 1, duration: 0.4, ease: "back.out(2)" }}, 1.45);
      // a tap on Follow
      tl.fromTo("#v-tap", {{ opacity: 0, scale: 1.6, y: -60 }}, {{ opacity: 1, scale: 1, y: -60, duration: 0.2, ease: "power2.out" }}, 2.2);
      tl.to("#v-btn", {{ scale: 0.93, duration: 0.08, ease: "power2.out" }}, 2.35);
      tl.to("#v-btn", {{ scale: 1, background: "#A95CFF", color: "#FFFFFF", duration: 0.25, ease: "back.out(2)" }}, 2.43);
      tl.to("#v-tap", {{ opacity: 0, scale: 1.8, duration: 0.35, ease: "power2.out" }}, 2.43);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["s6-live"] = tl;
    }})();
  </script>
</template>
'''
    return HEAD.format(L=L, T=T, S=DIAM, css=css) + body


for name, text in (('s5-reveal', s5()), ('s6-live', s6())):
    with open(os.path.join(ROOT, 'compositions', f'{name}.html'), 'w') as f:
        f.write(text)
print('wrote s5-reveal and s6-live')
