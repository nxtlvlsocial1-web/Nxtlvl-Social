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

sys.path.insert(0, os.path.join(ROOT, "build"))
import worlds  # noqa: E402

MARGIN = 30
_PTS = worlds._arch_points(400)


def opening(y):
    """Inner x-range of the palace arch opening at frame height y, or None above the apex."""
    if y >= 560:
        return 92, 988
    left = [p for p in _PTS if p[0] <= 540]
    best = min(left, key=lambda p: abs(p[1] - y))
    if y < best[1] - 4:
        return None
    return best[0], 1080 - best[0]


def region_fail(kind, theme, bx):
    if kind == "garden":
        if bx["l"] < 80 or bx["r"] > 1000 or bx["t"] < 240 or bx["b"] > 1300:
            return f"outside the garden text area: {bx['l']:.0f}-{bx['r']:.0f} x {bx['t']:.0f}-{bx['b']:.0f}"
        return None
    for y in (bx["t"], bx["b"]):
        o = opening(y)
        if o is None:
            return f"above the arch at y={y:.0f}"
        if bx["l"] < o[0] + MARGIN or bx["r"] > o[1] - MARGIN:
            return f"x {bx['l']:.0f}-{bx['r']:.0f} outside {o[0] + MARGIN:.0f}-{o[1] - MARGIN:.0f} at y={y:.0f}"
    if worlds.THEMES[theme]["hang"] and bx["t"] < 470 and bx["r"] > 250 and bx["l"] < 830:
        return f"under the hanging flowers (top {bx['t']:.0f})"
    if bx["b"] > 1380:
        return f"bottom {bx['b']:.0f} reaches the shrubs"
    return None


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
            pg.evaluate(f"window.__timelines.main.seek({b - 0.6}) && 0")
            results += [r for r in pg.evaluate(JS) if r["scene"] == f"sc-{sid}"]
        br.close()
    for r in results:
        bx = r["box"]
        sid = r["scene"][3:]
        kind, sub = generate.KIND[sid]
        msg = None
        if r["kind"] == "ring":
            ring = r["ring"]
            half = max(ring["cx"] - bx["l"], bx["r"] - ring["cx"])
            if half > ring["r"] - 6:
                msg = f"text half-width {half:.0f} > ring radius {ring['r'] - 6:.0f}"
        else:
            msg = region_fail(kind, sub, bx)
        if msg:
            bad += 1
            print(f"FAIL {r['scene']:10s} {r['text']!r:44s} {msg}")
    print(f"{len(results)} elements checked, {bad} outside their shape")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
