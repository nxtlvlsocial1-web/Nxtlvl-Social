"""3D pixel icons for the Ashke lyric video, in the reference's style: chunky pixel art, a dark outline, a limited
palette (orange, cream, black, gold) rendered as extruded voxels by assets/js/world3d.js.

Each icon is a pixel map (fill only). pixel_icon() adds the black outline around every filled cell and returns
{"w", "h", "cells": [[x, y, hex], ...]}. Some icons are drawn from geometry (wheel, chain, watch).
"""
import math

PAL = {"o": "#ff5a1f", "O": "#c43d12", "w": "#f6efe2", "k": "#161110", "y": "#f2b632", "Y": "#c98a17", "d": "#2b2321",
       "g": "#8d8781", "b": "#9fd6ff", "B": "#3f5f92", "r": "#e2332d", "s": "#e9b98d", "e": "#2fe08a", "n": "#6d4a2e"}

MAPS = {
    "sunglasses": ["yyyyyyy..yyyyyyy",
                   "ydwdddyyyydwdddy",
                   "ydddddy..ydddddy",
                   "ydddddy..ydddddy",
                   ".ydddy....ydddy."],
    "car": ["....wwwwww......",
            "...wbbwbbbw.....",
            "..owbbwbbbwoooo.",
            ".ooooooooooooooy",
            "oooooooooooooooo",
            ".OOggOOOOOOggOO.",
            "...gg......gg..."],
    "teacup": ["..w...w...w.",
               "...w...w....",
               "............",
               "wwwwwwwwww..",
               "wnnnnnnnnwww",
               "wwwwwwwwww.w",
               ".wwyyyyww.ww",
               ".wwwwwwww...",
               "..wwwwww....",
               "yyyyyyyyyy..",
               ".wwwwwwww..."],
    "heart": [".oo...oo.",
              "owOo.oOoo",
              "owooooooo",
              "ooooooooo",
              ".ooooooo.",
              "..ooooo..",
              "...ooo...",
              "....o...."],
    "diamond": ["..bbbbbbb..",
                ".bwbbwbbwb.",
                "bwwbbwbbwwb",
                "bbbbbbbbbbb",
                ".bwbbwbbwb.",
                "..bwbwbwb..",
                "...bbwbb...",
                "....bwb....",
                ".....b....."],
    "crown": ["y....y....y",
              "yy..yyy..yy",
              "yyy.yyy.yyy",
              "yyyyyyyyyyy",
              "yryyyoyyyry",
              "yyyyyyyyyyy",
              "YYYYYYYYYYY"],
    "ring": ["....bb.....",
             "...bwwb....",
             "....bb.....",
             "..yyyyyy...",
             ".yy....yy..",
             "yy......yy.",
             "y........y.",
             "y........y.",
             "yy......yy.",
             ".yy....yy..",
             "..yyyyyy..."],
    "eye": ["....wwwww....",
            "..wwwwwwwww..",
            ".wwwwoooowww.",
            "wwwwoddoowwww",
            ".wwwwoooowww.",
            "..wwwwwwwww..",
            "....wwwww...."],
    "falcon": ["oo..........oo",
               ".ooo......ooo.",
               "..oooo..oooo..",
               "...oooowoooo..",
               "....oowwoo....",
               ".....oyyo.....",
               "......oo......",
               ".....o..o....."],
    "snake": ["..oooo....",
              ".oooooo...",
              ".oeooeo...",
              "..oooo....",
              "..rr.oo...",
              "......oo..",
              ".....oo...",
              "...ooo....",
              "..oo......",
              "..oo...oo.",
              "...ooooo.."],
    "shoe": [".......www....",
             "......wwwww...",
             ".....wwoowwww.",
             "...wwwwwwwwwww",
             ".wwwwwwwwwwwww",
             "oooooooooooooo"],
    "shirt": ["..ww....ww..",
              ".wwwwooowwww",
              "wwwwwoowwwww",
              "ww.wwwwwww.w",
              "...wwwwwww..",
              "...wwwwwww..",
              "...wwwwwww..",
              "...wwwwwww.."],
    "trousers": ["BBBBBBBBBB",
                 "BBBBBBBBBB",
                 "BBBBBBBBBB",
                 "BBBB..BBBB",
                 "BBBB..BBBB",
                 "BBBB..BBBB",
                 "BBBBB.BBBBB"[:10],
                 "BBBB..BBBB",
                 "BBBBB..BBBBB"[:10]],
    "stones": ["...ggg.......",
               "..ggwgg......",
               ".ggggggg.ggg.",
               ".gggggggggwgg",
               "ggggg.ggggggg"],
    "king": ["....y....",
             "...yyy...",
             "....y....",
             "..yyyyy..",
             "...yyy...",
             "...yyy...",
             "...yyy...",
             "..yyyyy..",
             ".yyyyyyy.",
             "YYYYYYYYY"],
    "shield": ["ooooooooo",
               "owwwowwwo",
               "owwwowwwo",
               "ooooooooo",
               ".owwowwo.",
               "..owowo..",
               "...ooo...",
               "....o...."],
}


def _circle(r, ring, fill_inner=None):
    rows = []
    n = 2 * r + 1
    for y in range(n):
        row = ""
        for x in range(n):
            d = math.hypot(x - r, y - r)
            row += ring if r - 1.3 <= d <= r + .3 else (fill_inner if fill_inner and d < r - 1.3 else ".")
        rows.append(row)
    return rows


def _wheel():
    m = [list(r) for r in _circle(6, "g")]
    for i in range(13):
        m[6][i] = m[6][i] if m[6][i] != "." else "w"
        m[i][6] = m[i][6] if m[i][6] != "." else "w"
    m[6][6] = "o"
    return ["".join(r) for r in m]


def _chain():
    m = [list(r) for r in _circle(6, "y")]
    for x in range(5, 8):
        for y in range(12, 15):
            if y >= len(m):
                m.append(["."] * 13)
            m[y][x] = "o"
    return ["".join(r) for r in m]


def _watch():
    m = [list(r) for r in _circle(5, "y", "w")]
    for y in range(2, 6):
        m[y][5] = "k"
    for x in range(5, 8):
        m[5][x] = "k"
    top = [list("...ddddd...") for _ in range(3)]
    return ["".join(r) for r in top + m + top]


MAPS["wheel"] = _wheel()
MAPS["chain"] = _chain()
MAPS["watch"] = _watch()


def pixel_icon(name):
    rows = MAPS[name]
    filled = {}
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != ".":
                filled[(x, y)] = PAL[c]
    outline = {(x + dx, y + dy) for (x, y) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - set(filled)
    cells = dict(filled)
    for p in outline:
        cells[p] = PAL["k"]
    xs = [x for x, _ in cells]
    ys = [y for _, y in cells]
    x0, y0 = min(xs), min(ys)
    return {"w": max(xs) - x0 + 1, "h": max(ys) - y0 + 1, "cells": [[x - x0, y - y0, c] for (x, y), c in cells.items()]}


ICONS = {n: pixel_icon(n) for n in MAPS}

if __name__ == "__main__":
    for n, ic in ICONS.items():
        print(n, ic["w"], ic["h"], len(ic["cells"]))
