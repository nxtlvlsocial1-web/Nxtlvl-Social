"""Checks that every piece of text sits inside its shape: the cream arch, the monogram rings and the
date row. Seeks the timeline to the end of each scene (everything revealed) and measures real glyph
boxes in Chromium.

python3 -I build/check_layout.py      (run from the project root; needs `pip install playwright`)
"""
import math
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
import generate  # noqa: E402

AX, AY = 110, 250          # arch position in the frame
INSET, MARGIN = 22, 18     # inner gold line, and breathing room inside it


def arch_edge(y):
    """Left edge x of the inner arch line at frame height y (the arch is symmetric)."""
    ay = y - AY
    p0, p1, p2, p3 = (INSET, 338), (INSET, 206), (274, 132), (430, 26)
    if ay >= 338:
        return AX + INSET
    if ay <= 26:
        return None
    best = None
    for i in range(2001):
        t = i / 2000
        u = 1 - t
        by = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
        bx = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
        if best is None or abs(by - ay) < best[0]:
            best = (abs(by - ay), bx)
    return AX + best[1]


JS = """() => {
  const out = [];
  const scenes = document.querySelectorAll('.scene');
  for (const sc of scenes) {
    const textEls = sc.querySelectorAll('.row .t, .mini-t, .side, .num');
    for (const el of textEls) {
      if (!el.textContent.trim()) continue;
      const r = document.createRange(); r.selectNodeContents(el);
      const rects = [...r.getClientRects()].filter(b => b.width > 0);
      if (!rects.length) continue;
      const box = {l: Math.min(...rects.map(b => b.left)), r: Math.max(...rects.map(b => b.right)),
                   t: Math.min(...rects.map(b => b.top)), b: Math.max(...rects.map(b => b.bottom))};
      const kind = el.classList.contains('mini-t') ? 'ring' : 'arch';
      let ring = null;
      if (kind === 'ring') { const p = el.parentElement.getBoundingClientRect(); ring = {cx: p.left + p.width/2, cy: p.top + p.height/2, r: p.width * 0.4 - 14}; }
      out.push({scene: sc.id, text: el.textContent.trim().slice(0, 40), kind, box, ring});
    }
    for (const el of sc.querySelectorAll('.win')) {
      const b = el.getBoundingClientRect();
      out.push({scene: sc.id, text: el.className, kind: 'arch', box: {l: b.left, r: b.right, t: b.top, b: b.bottom}});
    }
  }
  return out;
}"""


def main():
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                               args=["--no-sandbox"])
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + os.path.join(ROOT, "index.html"), wait_until="domcontentloaded")
        pg.wait_for_timeout(800)
        pg.evaluate("document.fonts.ready.then(() => 1)")
        results = []
        for sid, (a, b) in generate.S.items():
            if sid == "doors":
                continue
            pg.evaluate(f"window.__timelines.main.seek({b - 0.55}) && 0")
            results += [r for r in pg.evaluate(JS) if r["scene"] == f"sc-{sid}"]
        br.close()
    for r in results:
        bx = r["box"]
        msg = None
        if r["kind"] == "ring":
            ring = r["ring"]
            half = max(ring["cx"] - bx["l"], bx["r"] - ring["cx"])
            if half > ring["r"] - 6:
                msg = f"text half-width {half:.0f} > ring radius {ring['r'] - 6:.0f}"
        else:
            for y in (bx["t"], bx["b"]):
                e = arch_edge(y)
                if e is None:
                    msg = f"above the arch apex at y={y:.0f}"
                    break
                lo, hi = e + MARGIN, 1080 - e - MARGIN
                if bx["l"] < lo or bx["r"] > hi:
                    msg = (f"x {bx['l']:.0f}-{bx['r']:.0f} outside {lo:.0f}-{hi:.0f} at y={y:.0f}")
                    break
            if bx["b"] > AY + 1260 - INSET - MARGIN:
                msg = f"bottom {bx['b']:.0f} below the arch floor"
        if msg:
            bad += 1
            print(f"FAIL {r['scene']:10s} {r['text']!r:44s} {msg}")
    print(f"{len(results)} elements checked, {bad} outside their shape")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
