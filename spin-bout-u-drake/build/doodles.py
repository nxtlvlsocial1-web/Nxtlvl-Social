"""One doodle sticker per lyric line for the v9 collage (the Ashke edit's lyric elements), in the Spin Bout U colours:
off-white paper border, thick ink outline, magenta and off-white fills. svg(name) returns the sticker (viewBox 0 0 120).
"""
INK, MAG, WHITE, MAR = "#141213", "#b0194f", "#f2f1ec", "#5f1b30"

ICON = {   # line -> element
    -1: "star", 0: "eye", 1: "magazine", 2: "cassette", 3: "phone", 4: "heel", 5: "chair", 6: "house", 7: "foot", 8: "arrow",
    9: "plane", 10: "sign", 11: "heart", 12: "diamond", 13: "cloud", 14: "flame", 15: "heart2", 16: "ghost", 17: "tissue", 18: "star2",
}
WORD = {-1: "SPIN", 0: "JEALOUS", 1: "VOGUE", 2: "'90S", 3: "CALL", 4: "RUNWAY", 5: "FRONT ROW", 6: "SENT HOME", 7: "TEN TOES",
        8: "GO", 9: "GLOBE", 10: "ROAD", 11: "FEEL", 12: "DROPPED", 13: "SMOKE", 14: "BURN", 15: "THESE DAYS", 16: "BODY",
        17: "SNOTTY", 18: "FOR YOU"}

SHAPES = {   # (path, fill, stroke width)
    "star": [("M60 6 L74 44 L114 46 L82 70 L94 110 L60 86 L26 110 L38 70 L6 46 L46 44 Z", MAG, 6)],
    "star2": [("M60 6 L74 44 L114 46 L82 70 L94 110 L60 86 L26 110 L38 70 L6 46 L46 44 Z", WHITE, 6),
              ("M60 34 L66 52 L86 53 L70 64 L76 84 L60 72 L44 84 L50 64 L34 53 L54 52 Z", MAG, 4)],
    "eye": [("M6 60 C30 22 90 22 114 60 C90 98 30 98 6 60 Z", WHITE, 6), ("M60 36 A24 24 0 1 0 60.1 36 Z", MAG, 5),
            ("M60 50 A10 10 0 1 0 60.1 50 Z", INK, 0)],
    "magazine": [("M20 8 L100 8 L100 112 L20 112 Z", WHITE, 6), ("M30 20 L90 20 L90 40 L30 40 Z", MAG, 0),
                 ("M34 52 C50 48 70 60 86 100 L34 100 Z", INK, 0)],
    "cassette": [("M8 26 L112 26 L112 96 L8 96 Z", MAG, 6), ("M24 38 L96 38 L96 64 L24 64 Z", WHITE, 4),
                 ("M42 51 A8 8 0 1 0 42.1 51 Z M78 51 A8 8 0 1 0 78.1 51 Z", INK, 0), ("M30 96 L40 78 L80 78 L90 96", WHITE, 5)],
    "phone": [("M34 6 L86 6 Q96 6 96 16 L96 104 Q96 114 86 114 L34 114 Q24 114 24 104 L24 16 Q24 6 34 6 Z", INK, 6),
              ("M32 18 L88 18 L88 96 L32 96 Z", MAG, 0), ("M52 104 L68 104", WHITE, 5)],
    "heel": [("M10 96 C30 96 40 60 56 50 C74 40 96 56 104 78 L104 96 L90 96 L90 112 L82 112 L82 96 Z", MAG, 6)],
    "chair": [("M30 10 L90 10 L90 60 L30 60 Z", MAG, 6), ("M24 60 L96 60 L96 76 L24 76 Z", WHITE, 6),
              ("M30 76 L26 112 M90 76 L94 112", "none", 8)],
    "house": [("M12 58 L60 14 L108 58 L94 58 L94 108 L26 108 L26 58 Z", WHITE, 6), ("M48 76 L72 76 L72 108 L48 108 Z", MAG, 5),
              ("M20 20 L100 100 M100 20 L20 100", "none", 10)],
    "foot": [("M40 40 C20 50 22 96 44 108 C66 118 82 98 78 70 C76 52 62 32 40 40 Z", WHITE, 6),
             ("M56 8 A9 9 0 1 0 56.1 8 Z M76 14 A7 7 0 1 0 76.1 14 Z M90 26 A6 6 0 1 0 90.1 26 Z M98 42 A5 5 0 1 0 98.1 42 Z", MAG, 4)],
    "arrow": [("M10 70 L70 70 L70 96 L112 56 L70 16 L70 42 L10 42 Z", MAG, 6)],
    "plane": [("M8 66 L50 58 L76 14 L88 16 L72 58 L104 54 L112 62 L104 70 L72 66 L88 104 L76 106 L50 70 L8 66 Z", WHITE, 6)],
    "sign": [("M56 40 L64 40 L64 114 L56 114 Z", INK, 4), ("M16 10 L96 10 L112 26 L96 42 L16 42 Z", MAG, 6),
             ("M28 26 L80 26", WHITE, 5)],
    "heart": [("M60 108 C20 80 6 58 10 38 C14 16 44 10 60 32 C76 10 106 16 110 38 C114 58 100 80 60 108 Z", MAG, 6),
              ("M30 36 C34 28 42 26 48 30", WHITE, 5)],
    "heart2": [("M60 108 C20 80 6 58 10 38 C14 16 44 10 60 32 C76 10 106 16 110 38 C114 58 100 80 60 108 Z", WHITE, 6),
               ("M60 86 C38 70 30 56 32 46 C34 34 50 32 60 44 C70 32 86 34 88 46 C90 56 82 70 60 86 Z", MAG, 0)],
    "diamond": [("M24 18 L96 18 L114 46 L60 112 L6 46 Z", WHITE, 6), ("M6 46 L114 46 M40 18 L28 46 L60 112 L92 46 L80 18", "none", 4),
                ("M28 46 L60 112 L92 46 Z", MAG, 0)],
    "cloud": [("M24 92 C6 92 4 66 22 62 C18 40 44 30 56 44 C64 22 98 26 96 54 C116 56 116 92 94 92 Z", WHITE, 6)],
    "flame": [("M60 4 C72 30 98 42 90 78 C86 100 70 114 56 114 C36 112 22 96 26 74 C30 56 44 52 44 36 C54 46 56 56 56 64 "
               "C66 52 68 30 60 4 Z", MAG, 6), ("M50 112 C40 96 48 84 58 72 C60 86 72 92 66 112", WHITE, 5)],
    "ghost": [("M24 112 L24 48 C24 22 42 8 60 8 C78 8 96 22 96 48 L96 112 L84 100 L72 112 L60 100 L48 112 L36 100 Z", WHITE, 6),
              ("M46 46 A6 8 0 1 0 46.1 46 Z M74 46 A6 8 0 1 0 74.1 46 Z", INK, 0)],
    "tissue": [("M14 62 L106 62 L106 112 L14 112 Z", MAG, 6), ("M40 62 C40 40 52 24 46 6 C66 16 74 36 80 62", WHITE, 6)],
}


def svg(name, size=230):
    parts = SHAPES[name]
    border = "".join(f'<path d="{d}" fill="{WHITE if f != "none" else "none"}" stroke="{WHITE}" stroke-width="{max(w, 4) + 14}" '
                     f'stroke-linejoin="round" stroke-linecap="round"/>' for d, f, w in parts)
    ink = "".join(f'<path d="{d}" fill="{f}" stroke="{INK}" stroke-width="{w if w else 0}" stroke-linejoin="round" stroke-linecap="round"/>'
                  for d, f, w in parts)
    return (f'<svg viewBox="-10 -10 140 140" width="{size}" height="{size}" style="overflow:visible;'
            f'filter:drop-shadow(0 8px 10px rgba(0,0,0,.4))">{border}{ink}</svg>')
