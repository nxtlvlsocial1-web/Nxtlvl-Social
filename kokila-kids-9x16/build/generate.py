"""Dr S Kokila, "children see a friend" talking head, 9:16: writes index.html.

Owner's brief (2026-11-18):
- Style, transitions, background and effects from the Kanav Kesar "Surrender" ad (surrender-ad-9x16/build/generate.py):
  pink dotted background, split (top a glass screen on the pink stage, bottom her face, black-box white caption on the
  seam), full frames with a script word over a big Anton word (red on key words), zoom-blur cuts, the magenta tint /
  light leak / white flash into a split, grain.
- Hook title in the middle, red, on screen 4-5 s at the start.
- Then minimal animation: no motion-graphic cards, only the captions and the cuts.
- Real reference footage as the script asks, but the focus is her: mostly her full screen, the footage only on a few
  lines, and always with her face under it in the split.
- No transition-pack effect (owner, 2026-11-18: the "TRANSITION AND CLICK SAAS" pixel ring is not to be used in any
  video until the owner says so). The hook simply settles in, as in the Kanav ad.
- v3 reference footage is silhouettes only (owner: "keep it gender, race, skin neutral").
- No music, sound effects only (build/sfx_sheet.py).
Footage: assets/video/face_full.mp4 (the tight cut, build/tight.py) and face_split.mp4 (its 1080x960 crop).
Captions run on plan/words_final.json (the words as heard in the tight cut).
python3 build/generate.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF = json.load(open(os.path.join(ROOT, "plan", "words_final.json")))
W, LINES = WF["words"], WF["lines"]
FW, FH, FPS = 1080, 1920, 30
VDUR = round(WF["dur"], 3)
DUR = round(VDUR + 1.4, 3)        # the close holds 1.4 s on her last frame so the last line can be read
A, HIDE, POST, CUES, TOPV = [], [], [], [], []
NID = [0]
HOOK = ["NO CHILD IS BORN", "WITH PREJUDICE"]
HOOK_END = 5.0                       # owner: at least 4-5 s
TR_PEAK = .63                        # both transition clips are at their widest 19 frames in


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def T(i):
    return W[i]["s"]


def LS(i):
    """the cut point for a section starting at word i: the start of its line, or just before the word mid-line"""
    if i and W[i - 1]["line"] == W[i]["line"]:
        return W[i]["s"] - .04
    return LINES[W[i]["line"]][0]


def word(i):
    return re.sub(r"[,.?!]", "", W[i]["text"]).strip()


# (kind, first word, end word, reference clip, clip in-point s). A section starts at its first word's line.
SECTIONS = [("open", 0, 21, "ref_kids", 0.3),        # Have you seen two children playing together? ... the other is white.
            ("full", 21, 30),                         # But do you know what they see? A friend.
            ("split", 30, 40, "ref_plane", 0.8),      # They don't ask which God the other child prays to.
            ("full", 40, 49),                         # They don't ask which country their parents are from.
            ("split", 49, 54, "ref_jump", 6.0),    # They just laugh, enjoy, share.
            ("full", 54, 74),                         # But somewhere along the way ... and sometimes who to fear.
            ("full", 74, 83),                         # And that's how our brain learns fear and prejudice.
            ("full", 83, 94),                         # But here's a beautiful part: our brain can learn empathy too.
            ("split", 94, 101, "ref_family", 8.0),     # Children can be taught compassion before discrimination.
            ("full", 101, 114),                       # They can be taught a little more kindness and a little more compassion.
            ("split", 114, 122, "ref_family", 0.3),    # And that's how, when we begin healing ourselves,
            ("full", 122, None)]                      # we begin healing humanity.
RED = {"friend", "fear", "prejudice", "empathy", "compassion", "discrimination", "kindness", "humanity"}


def sec_times():
    out = []
    for k, s in enumerate(SECTIONS):
        kind, a, b = s[:3]
        ta = 0.0 if a == 0 else LS(a)
        tb = DUR if b is None else LS(b)
        out.append((kind, ta, tb, a, len(W) if b is None else b) + tuple(s[3:]))
    return out


SECS = sec_times()


def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {max(0, t0):.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')


# ------------------------------------------------------------------------------------------------ captions
FUNC = {"the", "a", "is", "to", "and", "of", "you", "we", "our", "their", "are", "can", "be", "who", "they", "do", "what",
        "which", "how", "when", "that's", "but", "and", "have", "one", "just", "more", "little", "here's", "them", "don't"}


def chunks(a, b, maxw=3, maxc=16):
    """Phrases of up to maxw words; a chunk never ends on a short function word unless a sentence ends there."""
    out, cur = [], []
    for i in range(a, b):
        cur.append(i)
        txt = " ".join(word(j) for j in cur)
        end = W[i]["text"][-1] in ",.?"
        if (len(cur) >= maxw or len(txt) >= maxc or end) and (end or word(i).lower() not in FUNC or len(cur) >= maxw + 2):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    merged = []
    for c in out:
        if merged and all(word(j).lower() in FUNC for j in c):
            merged[-1] = merged[-1] + c
        else:
            merged.append(c)
    return merged


def seam_caps(a, b, tend):
    """Split sections: one to three words in a black box with white type, on the seam; under the hook, lower."""
    ch = chunks(a, b)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        i = nid("sc")
        low = ' style="top:1125px"' if t0 < HOOK_END else ""   # under the hook, over the wall above her head
        POST.append(f'<div class="seam" id="{i}"{low}><span>{" ".join(word(j) for j in c)}</span></div>')
        show(f"#{i}", t0, t1)
        js(f'tl.fromTo("#{i} span", {{scale: 1.12}}, {{scale: 1, duration: .16, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
        if t0 < HOOK_END < t1 and low:          # the caption moves up to the seam once the hook has gone
            j = nid("sc")
            POST.append(f'<div class="seam" id="{j}"><span>{" ".join(word(x) for x in c)}</span></div>')
            js(f'tl.set("#{i}", {{opacity: 0}}, {HOOK_END:.3f});')
            show(f"#{j}", HOOK_END, t1)


def full_caps(a, b, tend):
    """Full sections: a small script word over a big condensed word (red on key words), lower third."""
    ch = chunks(a, b, maxw=4, maxc=26 if tend >= DUR else 22)
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else tend
        key = [j for j in c if word(j).lower() in RED]
        tail = [j for j in c if word(j).lower() not in FUNC]
        big = key[-1:] if key else (c[c.index(tail[-1]):] if tail else c[-1:])
        small = [j for j in c if j < big[0]]
        after = [j for j in c if j > big[-1]]
        if after:                                # words after the key word ride on the big line
            big = big + after
        red = bool(key)
        i = nid("fc")
        sm = " ".join(word(j) for j in small).lower()
        bg = " ".join(word(j) for j in big).upper()
        POST.append(f'<div class="fcap" id="{i}">' + (f'<div class="scr">{sm}</div>' if sm else "") +
                    f'<div class="bigw{" red" if red else ""}" style="font-size:{min(150, int(1780 / max(1, len(bg))))}px">{bg}</div></div>')
        show(f"#{i}", t0, t1)
        if sm:
            js(f'tl.fromTo("#{i} .scr", {{opacity: 0, x: -20, filter: "blur(6px)"}}, {{opacity: 1, x: 0, filter: "blur(0px)", duration: .18, ease: "power3.out", immediateRender: false}}, {t0:.3f});')
        tb = T(big[0]) - .02
        if t1 - tb < .45:                        # the big word never flashes: it comes with the line
            tb = t0
        js(f'tl.set("#{i} .bigw", {{opacity: 0}}, {t0 - .001:.3f});')
        js(f'tl.fromTo("#{i} .bigw", {{opacity: 0, scale: 1.3, filter: "blur(10px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: .22, ease: "expo.out", immediateRender: false}}, {max(t0, tb):.3f});')
        if red:
            CUES.append((max(t0, tb), "hit"))


# ------------------------------------------------------------------------------------------------ layout + transitions
def refscreen(k, ta, tb, clip, at, opening):
    """The reference clip in a floating liquid-glass screen on the pink stage (top half)."""
    sid = nid("rs")
    top, h = (110, 580) if opening else (130, 650)
    TOPV.append(f'<div class="card" id="{sid}" style="top:{top}px;height:{h}px"><div class="scr">'
                f'<video id="{sid}v" class="clip" src="assets/video/{clip}.mp4" data-start="{ta:.3f}" data-duration="{tb - ta:.3f}" '
                f'data-media-start="{at:.3f}" data-track-index="{3 + k % 3}" muted playsinline></video></div></div>')
    show(f"#{sid}", ta, tb)
    js(f'tl.fromTo("#{sid}", {{y: 50, rotationX: 10, filter: "blur(12px)"}}, {{y: 0, rotationX: 2, filter: "blur(0px)", duration: .5, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
    n = int((tb - ta - .5) / 1.4)
    if n > 0:
        js(f'tl.to("#{sid}", {{y: -12, rotationX: 0, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: {n - 1}}}, {ta + .5:.3f});')


def layout():
    for k, sec in enumerate(SECS):
        kind, ta, tb, a, b = sec[:5]
        prev = SECS[k - 1][0] if k else None
        nxt = SECS[k + 1][0] if k + 1 < len(SECS) else None
        if kind in ("open", "split"):
            refscreen(k, ta, tb, sec[5], sec[6], kind == "open")
            js(f'tl.set("#split", {{opacity: 1, scale: 1, filter: "blur(0px)"}}, {ta:.3f});')
            js(f'tl.fromTo("#stage", {{scale: 1.0}}, {{scale: 1.05, duration: {tb - ta:.2f}, ease: "none", immediateRender: false}}, {ta:.3f});')
            js(f'tl.set("#split", {{opacity: 0}}, {tb:.3f});')
            if kind == "open":                      # opened by the owner's pixel ring (reveal())
                js(f'tl.fromTo("#botin", {{scale: 1.12, filter: "blur(6px)"}}, {{scale: 1, filter: "blur(0px)", duration: .5, ease: "expo.out", immediateRender: false}}, 0);')
                js(f'tl.fromTo("#topin", {{scale: 1.1, filter: "blur(8px)"}}, {{scale: 1, filter: "blur(0px)", duration: .5, ease: "expo.out", immediateRender: false}}, 0);')
                hook()
            else:                                   # Kanav's cut into a split: the face lands close and blurred
                js(f'tl.fromTo("#botin", {{scale: 1.55, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: .38, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                js(f'tl.fromTo("#topin", {{scale: 1.14, filter: "blur(14px)"}}, {{scale: 1, filter: "blur(0px)", duration: .42, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
                CUES.extend([(ta - .06, "whoosh_big"), (ta, "boom")])
            seam_caps(a, b, tb)
            if nxt == "full":                       # zoom-blur out of the split
                js(f'tl.to("#split", {{scale: 1.22, filter: "blur(16px)", duration: .2, ease: "power2.in"}}, {tb - .2:.3f});')
            continue
        # full
        js(f'tl.set("#full", {{opacity: 1}}, {ta:.3f});')
        if tb < DUR:
            js(f'tl.set("#full", {{opacity: 0}}, {tb:.3f});')
        s0 = 1.12 if prev == "full" else 1.18
        js(f'tl.fromTo("#fullin", {{scale: {s0}, filter: "blur(12px)"}}, {{scale: 1, filter: "blur(0px)", duration: .3, ease: "expo.out", immediateRender: false}}, {ta:.3f});')
        if prev != "open":
            CUES.append((ta - .12, "whoosh"))
        full_caps(a, b, tb)
        if nxt == "split":                          # Kanav's colour flash into the next split
            js(f'tl.set("#tint", {{opacity: .55}}, {tb - .3:.3f});')
            js(f'tl.set("#tint", {{opacity: 0}}, {tb - .23:.3f});')
            js(f'tl.fromTo("#leak", {{opacity: 0, x: -500}}, {{opacity: 1, x: 0, duration: .22, ease: "power2.in", immediateRender: false}}, {tb - .2:.3f});')
            js(f'tl.to("#leak", {{opacity: 0, x: 400, duration: .28, ease: "power2.out"}}, {tb + .02:.3f});')
            js(f'tl.fromTo("#flash", {{opacity: 0}}, {{opacity: .85, duration: .06, immediateRender: false}}, {tb - .05:.3f});')
            js(f'tl.to("#flash", {{opacity: 0, duration: .25, ease: "power2.out"}}, {tb + .02:.3f});')
            CUES.append((tb - .3, "shimmer"))
    HIDE.extend(["#split", "#full", "#tint", "#leak", "#flash", "#hold"])
    js(f'tl.set("#hold", {{opacity: 1}}, {VDUR - .04:.3f});')


def hook():
    """Red title in the middle of the frame (over the seam), from the first frames to HOOK_END."""
    POST.append('<div id="hook"><div class="hb">' + "".join(f'<div class="hl">{l}</div>' for l in HOOK) + '</div></div>')
    HIDE.append("#hook")
    js('tl.set("#hook", {opacity: 1}, 0);')       # Kanav's hook entrance: settles in from slightly big
    js('tl.fromTo("#hook .hb", {scale: 1.15, filter: "blur(8px)"}, {scale: 1, filter: "blur(0px)", duration: .5, ease: "expo.out", immediateRender: false}, 0);')
    js('tl.fromTo("#hook .hl", {y: 14, opacity: 0}, {y: 0, opacity: 1, duration: .45, ease: "expo.out", stagger: .08, immediateRender: false}, .05);')
    js(f'tl.to("#hook", {{y: -50, opacity: 0, filter: "blur(8px)", duration: .26, ease: "power2.in"}}, {HOOK_END - .26:.3f});')
    CUES.extend([(0.05, "boom"), (HOOK_END - .26, "swish")])


CSS = f"""
@font-face {{ font-family: "Inter"; font-weight: 500; src: url("assets/fonts/inter-latin-500-normal.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 700; src: url("assets/fonts/Inter-700.woff2"); }}
@font-face {{ font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2"); }}
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton.ttf"); }}
@font-face {{ font-family: "Kaushan"; src: url("assets/fonts/KaushanScript.ttf"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #f7b7c3; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; font-family: "Inter"; color: #3b0a1f; }}
#bg {{ position: absolute; inset: 0; background: radial-gradient(120% 75% at 50% 8%, #fff4f6 0%, #ffd6de 42%, #f7a2b4 100%); }}
#bg::after {{ content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(190,40,80,.17) 1.7px, transparent 2.1px);
  background-size: 26px 26px; -webkit-mask-image: linear-gradient(#000 20%, rgba(0,0,0,.35)); mask-image: linear-gradient(#000 20%, rgba(0,0,0,.35)); }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(90px); opacity: .3; }}
#split {{ position: absolute; inset: 0; opacity: 0; transform-origin: 50% 50%; }}
#top {{ position: absolute; left: 0; top: 0; width: {FW}px; height: 960px; overflow: hidden; }}
#topin {{ position: absolute; inset: 0; perspective: 1400px; transform-origin: 50% 50%; }}
#stage {{ position: absolute; left: 0; top: 0; width: 1080px; height: 960px; transform-origin: 50% 45%; perspective: 1400px; }}
.card {{ position: absolute; left: 70px; width: 940px; border-radius: 46px; padding: 16px; opacity: 0;
  background: linear-gradient(140deg, rgba(255,255,255,.62), rgba(255,255,255,.18) 50%, rgba(255,255,255,.38));
  border: 1.5px solid rgba(255,255,255,.85); backdrop-filter: blur(24px) saturate(1.7); -webkit-backdrop-filter: blur(24px) saturate(1.7);
  box-shadow: inset 0 2px 0 rgba(255,255,255,.95), inset 0 -18px 40px rgba(255,80,130,.18), 0 40px 80px rgba(140,20,60,.30), 0 8px 22px rgba(140,20,60,.16); }}
.card::after {{ content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  background: linear-gradient(118deg, rgba(255,255,255,.55) 0%, rgba(255,255,255,0) 26%, rgba(255,255,255,0) 74%, rgba(255,255,255,.22) 100%); }}
.card .scr {{ position: relative; width: 100%; height: 100%; border-radius: 32px; overflow: hidden; box-shadow: 0 0 0 1px rgba(255,255,255,.5); }}
.card video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#bot {{ position: absolute; left: 0; top: 960px; width: {FW}px; height: 960px; overflow: hidden; background: #2a0d14; }}
#botin {{ position: absolute; inset: 0; transform-origin: 50% 35%; }}
#botin video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#seamline {{ position: absolute; left: 0; top: 957px; width: {FW}px; height: 6px; background: linear-gradient(90deg, #ff2d55, #ff7aa0, #ff2d55); z-index: 6; }}
#full {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; background: #2a0d14; }}
#fullin {{ position: absolute; inset: 0; transform-origin: 50% 35%; }}
#fullin video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#hold {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; }}
#hook {{ position: absolute; left: 0; top: 806px; width: {FW}px; text-align: center; z-index: 12; opacity: 0; }}
#hook .hb {{ display: inline-block; padding: 26px 46px 30px; border-radius: 30px; background: rgba(255,255,255,.96);
  box-shadow: 0 24px 60px rgba(120,10,40,.35), inset 0 -10px 30px rgba(255,80,130,.12); }}
#hook .hl {{ font: 400 112px/1.02 "Anton"; color: #e0182d; letter-spacing: .01em; text-transform: uppercase; }}
.seam {{ position: absolute; left: 0; width: {FW}px; top: 905px; text-align: center; opacity: 0; z-index: 9; }}
.seam span {{ display: inline-block; background: #000; color: #fff; font: 800 50px/1 "Inter"; padding: 12px 24px 14px; border-radius: 8px; letter-spacing: -.01em; }}
.fcap {{ position: absolute; left: 110px; right: 80px; top: 1250px; opacity: 0; z-index: 9; }}
.fcap .scr {{ font: 400 74px/1.1 "Kaushan"; color: #fff; text-shadow: 0 4px 14px rgba(0,0,0,.55); margin-left: 6px; }}
.fcap .bigw {{ font: 400 150px/1 "Anton"; color: #fff; letter-spacing: .01em; text-shadow: 0 8px 26px rgba(0,0,0,.45); transform-origin: 0 60%; }}
.fcap .bigw.red {{ display: inline-block; color: #e0182d; background: #fff; padding: 8px 26px 4px; border-radius: 18px; text-shadow: none;
  box-shadow: 0 14px 34px rgba(0,0,0,.35); }}   /* her kurta is red: the key word sits on white, like the hook */
#scene {{ position: absolute; inset: 0; }}
html, body, #root {{ background: #1a0610; }}
#tint {{ position: absolute; inset: 0; z-index: 20; opacity: 0; background: #d23cff; mix-blend-mode: screen; }}
#leak {{ position: absolute; left: -400px; top: -200px; width: 1900px; height: 2400px; z-index: 21; opacity: 0; mix-blend-mode: screen;
  background: radial-gradient(ellipse 40% 50% at 50% 50%, rgba(255,240,200,1), rgba(255,170,60,.85) 35%, rgba(255,120,40,0) 70%); }}
#flash {{ position: absolute; inset: 0; z-index: 22; opacity: 0; background: #fff8f0; }}
#grain {{ position: absolute; inset: 0; z-index: 23; pointer-events: none; opacity: .05; background: url(assets/img/grain.png); mix-blend-mode: overlay; }}
"""


def main():
    layout()
    blobs = "".join(f'<i class="blob" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>'
                    for x, y, s, c in [(-120, 80, 520, "#ff6f95"), (620, 360, 560, "#ffffff"), (300, 620, 460, "#ff3d6e"), (760, -80, 420, "#ffb2c4")])
    for k, (x, y) in enumerate([(160, 260), (-140, -120), (120, -200), (-180, 180)]):
        js(f'tl.to(".blob:nth-child({k + 1})", {{x: {x}, y: {y}, duration: {DUR:.1f}, ease: "sine.inOut"}}, 0);')
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Kokila kids 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="scene"><div id="bg"></div>
      <div id="split">
        <div id="top"><div id="topin"><div id="blobs">{blobs}</div><div id="stage">{"".join(TOPV)}</div></div></div>
        <div id="bot"><div id="botin"><video id="vsplit" class="clip" src="assets/video/face_split.mp4" data-start="0" data-duration="{VDUR}" data-track-index="2" muted playsinline></video></div></div>
        <div id="seamline"></div>
      </div>
      <div id="full"><div id="fullin"><video id="vfull" class="clip" src="assets/video/face_full.mp4" data-start="0" data-duration="{VDUR}" data-track-index="1" muted playsinline></video><img id="hold" src="assets/img/last_full.png" alt=""></div></div>
      {"".join(POST)}</div>
      <div id="tint"></div><div id="leak"></div><div id="flash"></div><div id="grain"></div>
      <audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{VDUR}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      gsap.set({json.dumps(list(dict.fromkeys(HIDE)))}, {{opacity: 0}});
{chr(10).join(A)}
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    ev = sorted(({"t": round(t, 3), "type": k} for t, k in CUES if 0 <= t < DUR), key=lambda e: e["t"])
    json.dump(ev, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, {len(SECS)} sections, {len(ev)} sound moments")
    for s in SECS:
        print(f"  {s[0]:5s} {s[1]:6.2f} - {s[2]:6.2f}  {s[5] if len(s) > 5 else ''}")


if __name__ == "__main__":
    main()
