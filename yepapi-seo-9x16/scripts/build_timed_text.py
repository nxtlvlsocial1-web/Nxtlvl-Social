#!/usr/bin/env python3
"""Rebuild the voice-timed text from assets/voice/transcript.json.

Writes:
  - compositions/captions.html  (caption groups, one visible at a time, active word highlighted)
  - compositions/s4.html        (the typed question, between the CHARS / TIMES markers)

Run from the project root after re-transcribing a new voiceover:
  npx hyperframes transcribe assets/voice/vo.wav --model small.en
  python3 scripts/build_timed_text.py
If the new transcript splits words differently, update GROUPS / QUESTION_WORDS (word indices).
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
words = json.loads((ROOT / "assets/voice/transcript.json").read_text())

# Display overrides: index -> text (None = merged into the previous word)
OVERRIDES = {55: "YEPAPI.", 56: None, 91: "YEPAPI", 92: None}

# Caption groups as inclusive word-index ranges. The question (30-38) is typed on screen in s4,
# and the CTA (90-98) is carried by the end card, so neither is captioned twice.
GROUPS = [
    (0, 3), (4, 7), (8, 9), (10, 12), (13, 14), (15, 16), (17, 20), (21, 24), (25, 25),
    (26, 29), (39, 42), (43, 46), (47, 49), (50, 52), (53, 56), (57, 58), (59, 61),
    (62, 64), (65, 68), (69, 72), (73, 75), (76, 79), (80, 81), (82, 85), (86, 89),
]
QUESTION_WORDS = (30, 38)
S4_START = 9.7  # absolute start of scene s4


def display_words(a, b):
    out = []
    for i in range(a, b + 1):
        w = words[i]
        text = OVERRIDES.get(i, w["text"])
        if text is None:
            out[-1]["e"] = w["end"]
            continue
        out.append({"t": text.upper(), "s": w["start"], "e": w["end"]})
    return out


def caption_html():
    groups = []
    for gi, (a, b) in enumerate(GROUPS):
        ws = display_words(a, b)
        nxt = words[GROUPS[gi + 1][0]]["start"] if gi + 1 < len(GROUPS) else 99
        s = max(0.12, ws[0]["s"] - 0.04)
        e = min(ws[-1]["e"] + 0.3, nxt - 0.04)
        chars = sum(len(w["t"]) for w in ws)
        fs = int(min(64, max(48, (860 - len(ws) * 18) / (0.66 * chars))))
        spans = []
        for k, w in enumerate(ws):
            wn = ws[k + 1]["s"] if k + 1 < len(ws) else e
            spans.append(f'<span class="cap-w" data-s="{w["s"]:.2f}" data-n="{wn:.2f}">{html.escape(w["t"])}</span>')
        groups.append(
            f'      <div class="cap-g" id="cap-g{gi}" data-s="{s:.2f}" data-e="{e:.2f}" style="font-size: {fs}px">'
            + " ".join(spans) + "</div>"
        )
    return "\n".join(groups)


CAPTIONS_TEMPLATE = """<template>
  <style>
    #root { position: absolute; inset: 0; overflow: visible; background: transparent; pointer-events: none; }
    #root * { box-sizing: border-box; }
    .cap-g { position: absolute; left: 0; top: 1300px; width: 1080px; padding: 0 110px; text-align: center; line-height: 1.15; opacity: 0; visibility: hidden; overflow: visible; }
    .cap-w { display: inline-block; font-family: "Inter", sans-serif; font-weight: 900; letter-spacing: -0.01em; text-transform: uppercase; color: #ffffff; text-shadow: 0 4px 20px rgba(0, 0, 0, 0.75), 0 2px 4px rgba(0, 0, 0, 0.6); }
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
__GROUPS__
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      document.querySelectorAll(".cap-g").forEach((g) => {
        const s = parseFloat(g.dataset.s), e = parseFloat(g.dataset.e);
        tl.set(g, { visibility: "visible" }, s);
        tl.fromTo(g, { opacity: 0, y: 14, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.14, ease: "power2.out" }, s);
        g.querySelectorAll(".cap-w").forEach((w) => {
          const ws = parseFloat(w.dataset.s), wn = parseFloat(w.dataset.n);
          // the spoken word glows lemon, then settles back to white
          tl.fromTo(w, { color: "#ffffff", textShadow: "0 4px 20px rgba(0,0,0,0.75), 0 2px 4px rgba(0,0,0,0.6)" }, { color: "#fff56c", textShadow: "0 0 24px rgba(255,245,108,0.55), 0 2px 4px rgba(0,0,0,0.6)", duration: 0.05, ease: "none" }, ws);
          tl.to(w, { color: "#ffffff", textShadow: "0 4px 20px rgba(0,0,0,0.75), 0 2px 4px rgba(0,0,0,0.6)", duration: 0.08, ease: "none" }, Math.min(wn, e - 0.1));
        });
        tl.to(g, { opacity: 0, duration: 0.1, ease: "power2.in" }, e - 0.1);
        tl.set(g, { opacity: 0, visibility: "hidden" }, e);
      });
      window.__timelines["captions"] = tl;
    })();
  </script>
</template>
"""


def question_parts():
    a, b = QUESTION_WORDS
    spans, sets = [], []
    n = 0
    for i in range(a, b + 1):
        w = words[i]
        text = w["text"].replace("?", "") + ("?" if i == b else "")
        if i == a:
            text = text[0].upper() + text[1:]
        t0 = w["start"] - S4_START
        dur = max(0.08, (w["end"] - w["start"]) * 0.85)
        chars = (" " if i > a else "") + text
        for k, ch in enumerate(chars):
            cid = f"s4-c{n}"
            spans.append(f'<span class="s4-c" id="{cid}">{html.escape(ch) if ch != " " else " "}</span>')
            sets.append(f'tl.set("#{cid}", {{ display: "inline" }}, {t0 + dur * k / len(chars):.3f});')
            n += 1
    return "".join(spans), "\n      ".join(sets)


def main():
    (ROOT / "compositions/captions.html").write_text(CAPTIONS_TEMPLATE.replace("__GROUPS__", caption_html()))
    s4 = (ROOT / "compositions/s4.html").read_text()
    spans, sets = question_parts()
    chars_block = "<!--CHARS-->" + spans + "<!--/CHARS-->"
    times_block = "/*TIMES*/\n      " + sets + "\n      /*/TIMES*/"
    if "<!--/CHARS-->" in s4:
        s4 = re.sub(r"<!--CHARS-->.*?<!--/CHARS-->", lambda m: chars_block, s4, flags=re.S)
    else:
        s4 = s4.replace("<!--CHARS-->", chars_block)
    if "/*/TIMES*/" in s4:
        s4 = re.sub(r"/\*TIMES\*/.*?/\*/TIMES\*/", lambda m: times_block, s4, flags=re.S)
    else:
        s4 = s4.replace("/*TIMES*/", times_block)
    (ROOT / "compositions/s4.html").write_text(s4)
    print("captions:", len(GROUPS), "groups; question chars:", spans.count("s4-c"))


if __name__ == "__main__":
    main()
