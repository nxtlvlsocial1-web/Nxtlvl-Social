"""Dr S Kokila, "Not everyone will like you" talking head, 9:16: writes index.html.

Built on her edit template (brands/dr-kokila/brand.md, "Edit template"; first used in kokila-kids-9x16):
- Opening split: reference footage full-bleed in the top 45 %, her talking head below, a thin white seam line, the hook
  box on the seam for the whole split.
- Hook: "Not everyone / will like you" (owner: "everyone" and "you" red), white rounded box, Montserrat Black Italic.
- Captions: 2-3 words, never across two spoken lines, in a small white rounded box, black Fredoka; low, clear of her lips.
- Then her full frame (a jump-cut punch-in on alternate lines) with a few full-screen reference shots. Hard cuts.
- Screen time (owner rule): 60 % her full frame, 40 % reference footage by duration (the split counts as reference).
- Footage literal to the script. No music; light sound effects (build/sfx_sheet.py). No transition-pack effects.
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
DUR = round(VDUR + 1.4, 3)           # the close holds on her last frame so the last line can be read
SEAM = 860                           # the template's seam sits at 45 % of the height
A, HIDE, POST, CUES, TOPV, OVER = [], [], [], [], [], []
NID = [0]
HOOK = ['Not <b>everyone</b>', 'will like <b>you</b>']


def js(s):
    A.append("      " + s)


def nid(p):
    NID[0] += 1
    return f"{p}{NID[0]}"


def T(i):
    return W[i]["s"]


def CUT(i):
    """the cut point before word i: the start of its line, or just before the word mid-line"""
    if i and W[i - 1]["line"] == W[i]["line"]:
        return W[i]["s"] - .04
    return LINES[W[i]["line"]][0]


def word(i):
    return re.sub(r"[,.?!]", "", W[i]["text"]).strip()


def show(sel, t0, t1):
    HIDE.append(sel)
    js(f'tl.set("{sel}", {{opacity: 1}}, {max(0, t0):.3f});')
    if t1 < DUR:
        js(f'tl.set("{sel}", {{opacity: 0}}, {t1:.3f});')


SPLIT_END = 36                       # the split runs through line 2 ("...everything you do.")
REF_SHARE = .40                      # owner rule (2026-11-18): 60 % her full frame, 40 % reference footage
# top half of the split: (first word, clip, in-point s)
TOP_CLIPS = [(0, "t_pack", .5),          # No matter how good you are
             (6, "t_volunteer", 1.0),    # or how much good you do,
             (12, "t_eyeroll", 29.5),    # there will always be people who won't like you.
             (21, "t_complain", 2.5),    # They'll complain about you,
             (25, "t_whisper", 1.0),     # talk about you
             (28, "t_check", 5.0)]       # and find something wrong in everything you do.
# full-screen reference shots after the split: (first word, end word, clip, in-point s)
FULL_REFS = [(60, 62, "f_mirror", 5.0),  # their insecurities,
             (79, 87, "f_walk", 7.0)]    # (Keep) doing good, keep growing and let them talk.


# ------------------------------------------------------------------------------------------------ captions
FUNC = {"the", "a", "is", "to", "and", "of", "you", "we", "our", "their", "are", "can", "be", "who", "they", "do", "what",
        "which", "how", "when", "that's", "but", "have", "one", "just", "more", "little", "here's", "them", "don't"}


def chunks(a, b, maxw=3, maxc=16):
    out, cur = [], []
    for i in range(a, b):
        cur.append(i)
        txt = " ".join(word(j) for j in cur)
        end = W[i]["text"][-1] in ",.?" or i + 1 == b or W[i + 1]["line"] != W[i]["line"]   # never across two lines
        if (len(cur) >= maxw or len(txt) >= maxc or end) and (end or word(i).lower() not in FUNC or len(cur) >= maxw + 1):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def captions():
    """The template's caption: a small white rounded box, black rounded type, cut on with the word."""
    ch = chunks(0, len(W))
    for k, c in enumerate(ch):
        t0 = T(c[0]) - .02
        t1 = T(ch[k + 1][0]) - .02 if k + 1 < len(ch) else DUR
        top = 1560 if c[0] < SPLIT_END else 1310   # v5 (owner): lower, clear of her lips
        i = nid("cp")
        txt = " ".join(W[j]["text"].rstrip(",") for j in c)
        POST.append(f'<div class="cap" id="{i}" style="top:{top}px"><span>{txt}</span></div>')
        show(f"#{i}", t0, t1)


# ------------------------------------------------------------------------------------------------ layout
def layout():
    ts = CUT(SPLIT_END)
    # split: top clips change on their words, the face below, the hook on the seam the whole time
    show("#split", 0, ts)
    for k, (i, clip, at) in enumerate(TOP_CLIPS):
        t0 = 0.0 if i == 0 else CUT(i)
        t1 = ts if k + 1 == len(TOP_CLIPS) else CUT(TOP_CLIPS[k + 1][0])
        vid = nid("tv")
        TOPV.append(f'<video id="{vid}" class="topv" src="assets/video/{clip}.mp4" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
                    f'data-media-start="{at:.3f}" data-track-index="{3 + k % 2}" muted playsinline></video>')
        show(f"#{vid}", t0, t1)
        if i:
            CUES.append((t0, "swish"))
    js('tl.fromTo("#hook .hb", {scale: 1.12}, {scale: 1, duration: .35, ease: "back.out(2)", immediateRender: false}, 0);')
    CUES.append((0.0, "boom"))
    # full: her face, a jump-cut punch-in on alternate lines, a few full-screen reference shots
    show("#full", ts, DUR)
    CUES.append((ts - .05, "whoosh_big"))
    starts = sorted({CUT(i) for i in range(SPLIT_END, len(W)) if i == SPLIT_END or W[i - 1]["line"] != W[i]["line"]})
    for k, t0 in enumerate(starts):
        js(f'tl.set("#fullin", {{scale: {1.0 if k % 2 == 0 else 1.12}}}, {t0:.3f});')
    for k, (a, b, clip, at) in enumerate(FULL_REFS):
        t0, t1 = CUT(a), CUT(b)
        vid = nid("fv")
        OVER.append(f'<video id="{vid}" class="fullref" src="assets/video/{clip}.mp4" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
                    f'data-media-start="{at:.3f}" data-track-index="{5 + k % 2}" muted playsinline></video>')
        show(f"#{vid}", t0, t1)
        js(f'tl.fromTo("#{vid}", {{scale: 1.0}}, {{scale: 1.06, duration: {t1 - t0:.2f}, ease: "none", immediateRender: false}}, {t0:.3f});')
        CUES.append((t0 - .05, "whoosh"))
    HIDE.append("#hold")
    js(f'tl.set("#hold", {{opacity: 1}}, {VDUR - .04:.3f});')


CSS = f"""
@font-face {{ font-family: "Montserrat"; font-weight: 900; font-style: italic; src: url("assets/fonts/montserrat-latin-900-italic.woff2"); }}
@font-face {{ font-family: "Montserrat"; font-weight: 800; font-style: italic; src: url("assets/fonts/montserrat-latin-800-italic.woff2"); }}
@font-face {{ font-family: "Fredoka"; font-weight: 600; src: url("assets/fonts/fredoka-latin-600-normal.woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {FW}px; height: {FH}px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: {FW}px; height: {FH}px; overflow: hidden; background: #000; }}
#split, #full {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; }}
#top {{ position: absolute; left: 0; top: 0; width: {FW}px; height: {SEAM}px; overflow: hidden; background: #000; }}
.topv {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; }}
#bot {{ position: absolute; left: 0; top: {SEAM}px; width: {FW}px; height: {FH - SEAM}px; overflow: hidden; }}
#bot video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
#seamline {{ position: absolute; left: 0; top: {SEAM - 2}px; width: {FW}px; height: 4px; background: #fff; z-index: 6; }}
#hook {{ position: absolute; left: 0; width: {FW}px; top: {SEAM}px; transform: translateY(-50%); text-align: center; z-index: 8; }}
#hook .hb {{ display: inline-block; background: #fff; border-radius: 22px; padding: 14px 40px 18px; text-align: left;
  box-shadow: 0 6px 18px rgba(0,0,0,.18); }}
#hook .hl {{ font: italic 900 72px/1.12 "Montserrat"; color: #111; letter-spacing: -.01em; white-space: nowrap; }}
#hook .hl b {{ color: #e3202b; font-weight: 900; }}
#fullin {{ position: absolute; inset: 0; transform-origin: 50% 32%; }}
#fullin video, #hold {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }}
#hold {{ opacity: 0; }}
.fullref {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; transform-origin: 50% 50%; }}
.cap {{ position: absolute; left: 0; width: {FW}px; text-align: center; opacity: 0; z-index: 9; }}
.cap span {{ display: inline-block; background: #fff; color: #000; font: 600 46px/1 "Fredoka"; padding: 10px 20px 12px; border-radius: 12px;
  letter-spacing: -.005em; }}
"""


def main():
    layout()
    captions()
    hook = '<div id="hook"><div class="hb">' + "".join(f'<div class="hl">{l}</div>' for l in HOOK) + '</div></div>'
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={FW}, height={FH}" />
    <title>Kokila not everyone 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-fps="{FPS}" data-width="{FW}" data-height="{FH}">
      <div id="full"><div id="fullin"><video id="vfull" class="clip" src="assets/video/face_full.mp4" data-start="0" data-duration="{VDUR}" data-track-index="1" muted playsinline></video><img id="hold" src="assets/img/last_full.png" alt=""></div>
        {"".join(OVER)}</div>
      <div id="split">
        <div id="top">{"".join(TOPV)}</div>
        <div id="bot"><video id="vsplit" class="clip" src="assets/video/face_split.mp4" data-start="0" data-duration="{VDUR}" data-track-index="2" muted playsinline></video></div>
        <div id="seamline"></div>{hook}
      </div>
      {"".join(POST)}
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
    ref = CUT(SPLIT_END) + sum(CUT(b) - CUT(a) for a, b, _, _ in FULL_REFS)
    print(f"reference footage {ref:.2f} s of {DUR:.2f} s = {ref / DUR:.0%} (target {REF_SHARE:.0%}); her full frame {1 - ref / DUR:.0%}")
    print(f"wrote index.html {len(html) // 1024} KB, {len(A)} timeline lines, split to {CUT(SPLIT_END):.2f} s, {len(ev)} sound moments")


if __name__ == "__main__":
    main()
