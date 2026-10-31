"""Anton glyph outlines for the 3D text (assets/js/glyphs.js), so Three.js can extrude words without loading a font.

python3 build/glyphs.py      (from the project root; needs fontTools)
"""
import json
import os

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ'*0123456789&"


class Rec(BasePen):
    def __init__(self, gs):
        super().__init__(gs)
        self.c = []

    def _moveTo(self, p):
        self.c.append(["m", round(p[0]), round(p[1])])

    def _lineTo(self, p):
        self.c.append(["l", round(p[0]), round(p[1])])

    def _qCurveToOne(self, p1, p2):
        self.c.append(["q", round(p1[0]), round(p1[1]), round(p2[0]), round(p2[1])])

    def _curveToOne(self, p1, p2, p3):
        self.c.append(["b", round(p1[0]), round(p1[1]), round(p2[0]), round(p2[1]), round(p3[0]), round(p3[1])])

    def _closePath(self):
        self.c.append(["z"])


f = TTFont(os.path.join(ROOT, "assets", "fonts", "Anton.ttf"))
gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
out = {"upm": f["head"].unitsPerEm, "g": {}}
for ch in CHARS:
    name = cmap[ord(ch)]
    pen = Rec(gs)
    gs[name].draw(pen)
    out["g"][ch] = {"a": hmtx[name][0], "c": pen.c}
out["g"][" "] = {"a": hmtx[cmap[32]][0], "c": []}
open(os.path.join(ROOT, "assets", "js", "glyphs.js"), "w").write("window.ANTON = " + json.dumps(out, separators=(",", ":")) + ";\n")
print("wrote assets/js/glyphs.js", os.path.getsize(os.path.join(ROOT, "assets", "js", "glyphs.js")) // 1024, "KB")
