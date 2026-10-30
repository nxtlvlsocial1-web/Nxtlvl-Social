"""The cast: three original pixel mascots, one per classic PS2 game style, drawn as SVG.

ROOK the brawler (bronze horned helmet, glowing eyes, teal cape, giant hammer), VESPER the scout (mustard raincoat,
glinting round glasses, lantern) and DASH the speedster (electric-blue spikes, visor shades, pink star jacket, roller
skates, bubblegum). They are our own designs, not likenesses of any game's characters. Each map is 12 x 16 cells;
cells next to a filled cell get a dark outline automatically, so every sprite reads as clean pixel art.
"""

INK = "#1d1a26"

ROOK = dict(pal={"h": "#efe6cf", "b": "#c8873a", "B": "#8a5523", "E": "#5ff3ff", "k": INK, "t": "#1fa59a", "g": "#9aa7b8",
                 "s": "#c98b5e", "l": "#6b3f22", "f": "#4a2e1c"},
            rows=["h..........h",
                  "hh.bbbbbb.hh",
                  ".hbbbbbbbbh.",
                  "..bbbbbbbb..",
                  "..BBBBBBBB..",
                  "..bkEkkEkb..",
                  "..bbbbbbbb..",
                  "...bBBBBb...",
                  ".ttggggggtt.",
                  "ttsggllggstt",
                  "t.sggggggs.t",
                  "..ssggggss..",
                  "...llllll...",
                  "...ff..ff...",
                  "..fff..fff..",
                  "............"],
            prop=[(12, 3, 1, 12, "#6b3f22"), (10, 1, 5, 4, "#9aa7b8"), (10, 2, 5, 2, "#c4ced9")])   # the hammer

VESPER = dict(pal={"y": "#f2c230", "Y": "#c99a1a", "s": "#f1c7a5", "g": "#2a2a2a", "w": "#ffffff", "r": "#e0335a"},
              rows=["....yyyy....",
                    "...yyyyyy...",
                    "..yyyyyyyy..",
                    "..yYssssYy..",
                    ".yYsggsggsYy",
                    ".yYgwgsgwgYy",
                    ".yYsggsggsYy",
                    "..yYsssssYy.",
                    "..yyyyyyyy..",
                    ".yyyyYyyyyy.",
                    ".yyyyYyyyyy.",
                    ".syyyYyyyys.",
                    "..yyyYyyyy..",
                    "..yyyyyyyy..",
                    "...rr..rr...",
                    "..rrr..rrr.."],
              prop=[(12, 9, 1, 2, INK), (11, 11, 3, 3, "#ffd36e"), (12, 12, 1, 1, "#fff6c8")])   # the lantern

DASH = dict(pal={"h": "#3aa0ff", "s": "#e2a878", "k": INK, "v": "#39e6ff", "j": "#ff6fae", "w": "#ffffff", "n": "#2b2f6b",
                 "r": "#f4f2fa", "o": "#ff9d3c"},
            rows=["..h.h..h....",
                  ".hhhhhhhh...",
                  "hhhhhhhhhh..",
                  ".hsssssssh..",
                  ".kvvvvvvvk..",
                  ".kvvvvvvvk..",
                  "..sssssss...",
                  "...sssss....",
                  "..jjjjjjj...",
                  ".jjjjwjjjj..",
                  ".sjjwwwjjs..",
                  "..jjjwjjj...",
                  "..nnn.nnn...",
                  "..nnn.nnn...",
                  ".rrrr.rrrr..",
                  ".o.o..o.o..."],
            prop=[(8, 5, 3, 3, "#ff9cd0"), (9, 5, 1, 1, "#ffd1ea"), (7, 6, 1, 1, "#ff9cd0")])   # the bubblegum bubble

CAST = {"rook": ROOK, "vesper": VESPER, "dash": DASH}


def _cells(m, grey=False):
    rows = m["rows"]
    filled = {}
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != ".":
                filled[(x, y)] = m["pal"][c]
    for x, y, w, h, c in m["prop"]:
        for dx in range(w):
            for dy in range(h):
                filled[(x + dx, y + dy)] = c
    if grey:
        def g(c):
            r, gg, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
            v = int(.3 * r + .59 * gg + .11 * b) // 2 + 100
            return f"#{v:02x}{v:02x}{v:02x}"
        filled = {k: g(v) for k, v in filled.items()}
    outline = set()
    for (x, y) in filled:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p not in filled:
                outline.add(p)
    return filled, outline


def sprite(name, size, cid=None, grey=False, extra="", mono=None):
    """An inline SVG of a mascot, `size` px wide; `mono` paints it as a one-colour silhouette."""
    m = CAST[name]
    filled, outline = _cells(m, grey)
    if mono:
        filled = {k: mono for k in filled}
    xs = [x for x, _ in list(filled) + list(outline)]
    ys = [y for _, y in list(filled) + list(outline)]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs) + 1, max(ys) + 1
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{mono or (INK if not grey else "#55525e")}"/>' for x, y in outline)
    rects += "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{c}"/>' for (x, y), c in filled.items())
    w, h = x1 - x0, y1 - y0
    ids = f' id="{cid}"' if cid else ""
    return (f'<svg class="mascot"{ids} viewBox="{x0} {y0} {w} {h}" width="{size}" height="{size * h / w:.0f}" shape-rendering="crispEdges">'
            f'{rects}{extra}</svg>')


def mosaic(name, size, block=3):
    """A deliberately low-res version of a mascot (cells merged into blocks): the "before" of sharper graphics."""
    m = CAST[name]
    filled, outline = _cells(m)
    allc = dict(filled)
    for p in outline:
        allc[p] = INK
    xs = [x for x, _ in allc]
    ys = [y for _, y in allc]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs) + 1, max(ys) + 1
    out = []
    for bx in range(x0, x1, block):
        for by in range(y0, y1, block):
            cs = [allc[(x, y)] for x in range(bx, bx + block) for y in range(by, by + block) if (x, y) in allc]
            if len(cs) >= block * block / 3:
                c = max(set(cs), key=cs.count)
                out.append(f'<rect x="{bx}" y="{by}" width="{block}" height="{block}" fill="{c}"/>')
    w, h = x1 - x0, y1 - y0
    return (f'<svg class="mascot" viewBox="{x0} {y0} {w} {h}" width="{size}" height="{size * h / w:.0f}" shape-rendering="crispEdges">'
            f'{"".join(out)}</svg>')


# ------------------------------------------------------------------ poses for the canvas actors (assets/js/actors.js)
# Each pose swaps some rows of the base map, adds loose cells (x, y, palette key) and may move the prop.

POSES = {
    "rook": {
        "cheer": dict(rows={5: "s.bkEkkEkb.s", 6: "s.bbbbbbbb.s", 7: "ss.bBBBBb.ss", 9: "tt.ggllgg.tt", 10: "t..gggggg..t", 11: "...gggggg..."},
                      prop=[(12, -4, 1, 10, "#6b3f22"), (10, -6, 5, 3, "#9aa7b8"), (10, -5, 5, 1, "#c4ced9")]),
        "run": dict(rows={13: "..ff....ff..", 14: ".ff......ff."}),
        "swing": dict(rows={9: "ttsggllggs.t", 10: "t.sgggggg.ss"},
                      prop=[(11, 7, 7, 1, "#6b3f22"), (17, 5, 3, 5, "#9aa7b8"), (18, 5, 1, 5, "#c4ced9")]),
    },
    "vesper": {
        "cheer": dict(rows={11: ".yyyyYyyyyy."}, extra=[(-1, 6, "s"), (-1, 7, "s"), (12, 6, "s"), (12, 7, "s")],
                      prop=[(12, 3, 1, 3, INK), (11, 0, 3, 3, "#ffd36e"), (12, 1, 1, 1, "#fff6c8")]),
        "run": dict(rows={14: "..rr...rr...", 15: ".rr.....rr.."}),
        "peek": dict(rows={11: ".yyyyYyyyyy."}, extra=[(12, 9, "s"), (13, 9, "s")],
                     prop=[(13, 6, 1, 3, INK), (12, 9, 3, 3, "#ffd36e"), (13, 10, 1, 1, "#fff6c8")]),
    },
    "dash": {
        "cheer": dict(rows={10: ".jjjwwwjjj.."}, extra=[(0, 6, "s"), (0, 7, "s"), (10, 5, "s"), (10, 6, "s")]),
        "run": dict(rows={14: ".rrr...rrr..", 15: "o.o.....o.o."}),
    },
}

CRAB = {"o": "#D97757", "O": "#b9583a", "d": "#2a1d18", "l": "#dff1ff", "p": "#2a1d18", "b": "#8fb8ff", "k": "#ff9ccf"}


def _crab_rects(pose="stand", prop=None):
    r = [(2, 6, 12, 6, "o"), (2, 12, 12, 1, "O"), (5, 8, 1, 2, "d"), (10, 8, 1, 2, "d")]
    r += [(x, 13, 1, 2, "o") for x in (3, 5, 10, 12)]
    if pose == "cheer":
        r += [(1, 6, 1, 2, "o"), (0, 4, 2, 2, "o"), (14, 6, 1, 2, "o"), (14, 4, 2, 2, "o")]
    elif pose == "wave":
        r += [(1, 6, 1, 2, "o"), (0, 4, 2, 2, "o"), (14, 8, 2, 2, "o")]
    else:
        r += [(0, 8, 2, 2, "o"), (14, 8, 2, 2, "o")]
    if prop == "mag":
        r += [(14, 0, 3, 1, "d"), (13, 1, 1, 3, "d"), (17, 1, 1, 3, "d"), (14, 4, 3, 1, "d"), (14, 1, 3, 3, "l"), (13, 5, 1, 2, "d")]
    elif prop == "pad":
        r += [(4, 9, 8, 3, "p"), (5, 10, 1, 1, "b"), (10, 10, 1, 1, "k")]
    return r


def pixel_map(name, pose="stand", prop=None):
    """Cells of a mascot pose as [x, y, colour] (outline included), origin at the top-left of its bounding box."""
    filled = {}
    if name == "crab":
        for x, y, w, h, c in _crab_rects(pose, prop):
            for dx in range(w):
                for dy in range(h):
                    filled[(x + dx, y + dy)] = CRAB[c]
    else:
        m = CAST[name]
        ps = POSES.get(name, {}).get(pose, {})
        rows = [ps.get("rows", {}).get(i, r) for i, r in enumerate(m["rows"])]
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c != ".":
                    filled[(x, y)] = m["pal"][c]
        for x, y, c in ps.get("extra", []):
            filled[(x, y)] = m["pal"][c]
        for x, y, w, h, c in ps.get("prop", m["prop"]):
            for dx in range(w):
                for dy in range(h):
                    filled[(x + dx, y + dy)] = c
    outline = {(x + dx, y + dy) for (x, y) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - set(filled)
    allc = dict(filled)
    for p_ in outline:
        allc[p_] = INK
    xs = [x for x, _ in allc]
    ys = [y for _, y in allc]
    x0, y0 = min(xs), min(ys)
    # ax: the body's centre column, so a prop sticking out on one side doesn't shift the character
    return {"w": max(xs) - x0 + 1, "h": max(ys) - y0 + 1, "ax": (8 if name == "crab" else 6) - x0, "cells": [[x - x0, y - y0, c] for (x, y), c in sorted(allc.items(), key=lambda kv: (kv[0][1], kv[0][0]))]}


if __name__ == "__main__":
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cells = "".join(f'<div style="display:inline-block;margin:20px">{sprite(n, 220)}<br>{sprite(n, 110, grey=True)}{mosaic(n, 110)}</div>'
                    for n in CAST)
    open(os.path.join(root, "build", "mascots_preview.html"), "w").write(
        f'<!doctype html><body style="background:#f1eef4;margin:0;padding:20px">{cells}</body>')
    print("wrote build/mascots_preview.html")
