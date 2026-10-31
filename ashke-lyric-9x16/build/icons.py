"""One element per lyric line, drawn from what the line says, as a doodle sticker in the collage's style: white paper
border, thick black ink outline, red and white fills (like the flame doodle in the YouMotion reference).

ICON maps each lyric line to its element; svg(name) returns the sticker's SVG markup (viewBox 0 0 120 120).
"""
INK, RED, WHITE, GREY = "#161616", "#d8232a", "#f4f2ec", "#9d9890"

# line -> element: what the line says
ICON = {
    0: "arrow",      # main sidha turiya jaavaan: I walk straight
    1: "eye",        # tu takkdi tedhi-tedhi: you look at me sideways
    2: "tape",       # tu body kar laae slim: you got slim
    3: "shades",     # kamm shady
    4: "clock",      # poora phera: the full round
    5: "car",        # main nahi laaunda gedhi: I don't go cruising
    6: "shoe",       # car'an, jutti te asla: cars, shoes and weapons
    7: "flag",       # ni eh tinne Italy made: all three made in Italy
    8: "hanger",     # leerha-latta: clothes
    9: "peak",       # top da rakhhaan main: I keep it top
    10: "teeth",     # kacchi oon chabb ja: chew it raw
    11: "cup",       # peene aan chaahaan nu odan kaadh ke: we drink our tea brewed like that
    12: "wings",     # jatt khulla ghummda: the Jatt roams free
    13: "binoculars",  # vairi nu rakhhaan main odan taadh ke: I keep the rivals watched
    14: "flower",    # ni tu phull vargi: you're like a flower
    15: "rocks",     # pathraan nu aaya munda paarh ke: came up breaking through stone
    16: "heart",     # tu kardi meriyan deedaaan: you long to see me
    17: "unlock",    # ni saada khull gaya jhaaka: our shyness opened up
    18: "mask",      # tu dil kardi ae chori: you steal hearts
    19: "money",     # main maarida daaka: I pull the robbery
    20: "ring",      # bebe kehndi tainu viaahuna: mum says she'll marry you to me
    21: "shield",    # shastar de naal thaaka: the engagement with the weapon
    22: "crow",      # dass ki kar laina kaavaan: tell me, what can the crows do
    23: "hawk",      # baajaan aala raakha: the one with the hawks protects me
    24: "cone",      # raahan vich rodhe: stones on the road
    25: "link",      # yaaran naa': with the friends
    26: "poison",    # jatt mudh ton zehri: poisonous from the start
    27: "snake",     # naag nahi riha koi saanu dass ke: no snake has bitten us
    28: "crown",     # baabe di saanu baksh ae: Baba's blessing
    29: "necklace",  # kann nattian, gaani lashke: earrings, the necklace shines
    30: "gun",       # modhe paundi doonaali: the double barrel on her shoulder
    31: "burst",     # ashke
}

# the Punjabi word written on each element's tag
WORD = {0: "ਸਿੱਧਾ", 1: "ਟੇਢੀ", 2: "ਸਲਿੱਮ", 3: "ਸ਼ੇਡੀ", 4: "ਫੇਰਾ", 5: "ਗੇੜੀ", 6: "ਜੁੱਤੀ", 7: "ਇਟਲੀ", 8: "ਲੀੜਾ", 9: "ਟੌਪ",
        10: "ਚੱਬ", 11: "ਚਾਹ", 12: "ਖੁੱਲ੍ਹਾ", 13: "ਤਾੜ", 14: "ਫੁੱਲ", 15: "ਪੱਥਰ", 16: "ਦੀਦਾ", 17: "ਝਾਕਾ", 18: "ਚੋਰੀ",
        19: "ਡਾਕਾ", 20: "ਵਿਆਹ", 21: "ਸ਼ਸਤਰ", 22: "ਕਾਂ", 23: "ਬਾਜ", 24: "ਰੋੜੇ", 25: "ਯਾਰ", 26: "ਜ਼ਹਿਰ", 27: "ਨਾਗ",
        28: "ਬਖ਼ਸ਼", 29: "ਗਾਨੀ", 30: "ਦੂਨਾਲੀ", 31: "ਅਸ਼ਕੇ"}

# (path d, fill, stroke width); "none" fill draws a line
GREEN = "#2e8b57"
SHAPES = {
    "flag": [("M14 6 L22 6 L22 116 L14 116 Z", INK, 3), ("M22 14 L50 14 L50 70 L22 70 Z", GREEN, 4),
             ("M50 14 L78 14 L78 70 L50 70 Z", WHITE, 4), ("M78 14 L106 14 L106 70 L78 70 Z", RED, 4)],
    "cup": [("M20 50 L86 50 L80 94 Q54 106 26 94 Z", WHITE, 5), ("M86 58 Q104 60 100 74 Q96 84 82 82", "none", 5),
            ("M40 40 Q34 30 42 22 M58 40 Q52 30 60 22 M76 40 Q70 30 78 22", "none", 4), ("M10 104 L96 104", "none", 5)],
    "binoculars": [("M12 50 L50 50 L50 100 Q31 112 12 100 Z", INK, 4), ("M70 50 L108 50 L108 100 Q89 112 70 100 Z", INK, 4),
                   ("M50 64 L70 64 L70 80 L50 80 Z", GREY, 4), ("M20 92 a11 11 0 1 0 22 0 a11 11 0 1 0 -22 0 Z M78 92 a11 11 0 1 0 22 0 a11 11 0 1 0 -22 0 Z", WHITE, 3),
                   ("M18 50 L24 24 L44 24 L48 50 M72 50 L76 24 L96 24 L102 50", "none", 4)],
    "flower": [("M60 30 a16 16 0 1 1 0.1 0 Z M88 50 a16 16 0 1 1 0.1 0 Z M78 82 a16 16 0 1 1 0.1 0 Z M42 82 a16 16 0 1 1 0.1 0 Z M32 50 a16 16 0 1 1 0.1 0 Z", RED, 4),
               ("M60 58 a10 10 0 1 0 0.1 0 Z", WHITE, 4), ("M60 74 Q56 98 62 116", "none", 5)],
    "unlock": [("M22 56 L98 56 L98 112 L22 112 Z", RED, 5), ("M36 56 L36 36 Q36 10 62 10 Q86 10 88 32", "none", 9),
               ("M56 76 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0 Z M58 80 L66 80 L64 96 L60 96 Z", INK, 2)],
    "crow": [("M6 70 Q30 44 58 52 L76 38 Q92 36 98 46 L114 50 L98 56 Q96 76 74 84 L62 108 L56 86 Q30 88 6 70 Z", INK, 4),
             ("M86 44 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 Z", WHITE, 0)],
    "gun": [("M4 50 L94 40 L96 50 L6 60 Z", INK, 3), ("M4 62 L94 52 L96 60 L6 70 Z", GREY, 3),
            ("M90 42 L104 40 Q118 44 116 72 L106 104 L88 100 L94 72 L84 64 Z", RED, 4), ("M76 66 Q80 80 92 78", "none", 4)],
    "arrow": [("M60 6 L104 52 L76 52 L76 114 L44 114 L44 52 L16 52 Z", RED, 5)],
    "eye": [("M6 60 Q60 8 114 60 Q60 112 6 60 Z", WHITE, 5), ("M66 60 a20 20 0 1 0 40 0 a20 20 0 1 0 -40 0 Z", INK, 3),
            ("M80 54 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z", WHITE, 0)],
    "tape": [("M12 56 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 Z", RED, 5), ("M40 56 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 Z", WHITE, 4),
             ("M52 92 L116 92 L116 112 L52 112 Z", WHITE, 4), ("M64 92 L64 102 M76 92 L76 100 M88 92 L88 102 M100 92 L100 100", "none", 3)],
    "shades": [("M6 42 L56 42 L52 72 Q32 86 12 72 Z", INK, 5), ("M64 42 L114 42 L108 72 Q88 86 68 72 Z", INK, 5),
               ("M56 46 Q60 40 64 46", "none", 5), ("M16 50 L28 50", "none", 3)],
    "clock": [("M10 62 a50 50 0 1 0 100 0 a50 50 0 1 0 -100 0 Z", WHITE, 6), ("M60 62 L60 30 M60 62 L82 74", "none", 7),
              ("M52 6 L68 6 L68 14 L52 14 Z", RED, 4)],
    "car": [("M8 80 L16 54 L40 44 L80 44 L98 58 L114 62 L114 82 Z", RED, 5), ("M42 50 L58 50 L58 60 L32 60 Z", WHITE, 3),
            ("M64 50 L80 50 L92 60 L64 60 Z", WHITE, 3), ("M22 84 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 Z", INK, 3),
            ("M80 84 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 Z", INK, 3)],
    "shoe": [("M8 90 Q8 62 40 62 Q70 64 92 50 Q108 40 112 26 Q120 62 104 82 Q90 96 60 96 L12 96 Z", RED, 5),
             ("M30 70 Q54 74 80 62", "none", 3), ("M8 96 L100 92 Q110 96 102 104 L10 106 Z", INK, 3)],
    "cards": [("M14 22 L62 14 L74 98 L26 106 Z", WHITE, 5), ("M52 26 L100 32 L90 114 L42 108 Z", WHITE, 5),
              ("M70 62 Q62 52 56 60 Q52 68 70 84 Q88 68 84 60 Q78 52 70 62 Z", RED, 3)],
    "hanger": [("M60 34 Q60 20 70 16 Q80 14 78 26 Q76 32 68 34", "none", 6), ("M60 34 L10 80 L110 80 Z", WHITE, 6)],
    "peak": [("M4 108 L44 40 L60 62 L80 32 L116 108 Z", WHITE, 5), ("M80 32 L80 6", "none", 5), ("M80 6 L104 14 L80 22 Z", RED, 4)],
    "teeth": [("M10 40 Q60 6 110 40 L110 66 Q60 104 10 66 Z", RED, 5),
              ("M24 48 L36 48 L36 62 L24 62 Z M40 50 L52 50 L52 66 L40 66 Z M56 50 L68 50 L68 66 L56 66 Z M72 50 L84 50 L84 66 L72 66 Z M88 48 L98 48 L98 62 L88 62 Z", WHITE, 3)],
    "tea": [("M20 50 L86 50 L80 94 Q54 106 26 94 Z", WHITE, 5), ("M86 58 Q104 60 100 74 Q96 84 82 82", "none", 5),
            ("M40 40 Q34 30 42 22 M58 40 Q52 30 60 22", "none", 4), ("M12 14 L108 112 M108 14 L12 112", "none", 9)],
    "wings": [("M8 74 Q36 18 112 26 Q86 36 94 48 Q66 48 76 62 Q46 62 54 74 Q30 74 8 74 Z", WHITE, 5)],
    "wind": [("M8 44 L72 44 Q94 44 94 26 Q94 12 80 12 Q68 14 70 26", "none", 7), ("M8 66 L96 66 Q114 66 112 82 Q110 96 96 94", "none", 7),
             ("M20 88 L60 88", "none", 7)],
    "jeans": [("M28 8 L92 8 L98 114 L68 114 L60 48 L52 114 L22 114 Z", INK, 5), ("M30 22 L90 22 M60 22 L60 44", "none", 2)],
    "rocks": [("M6 104 L22 64 L50 56 L66 74 L60 104 Z", GREY, 5), ("M54 104 L70 46 L102 40 L116 104 Z", GREY, 5),
              ("M84 46 L78 66 L90 78 L84 96", "none", 3)],
    "heart": [("M60 108 L14 62 Q2 40 22 24 Q42 12 60 36 Q78 12 98 24 Q118 40 106 62 Z", RED, 5)],
    "wheel": [("M8 60 a52 52 0 1 0 104 0 a52 52 0 1 0 -104 0 Z", INK, 4), ("M30 60 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0 Z", WHITE, 4),
              ("M60 30 L60 90 M30 60 L90 60 M39 39 L81 81 M81 39 L39 81", "none", 4)],
    "mask": [("M60 110 L14 64 Q2 42 22 26 Q42 14 60 38 Q78 14 98 26 Q118 42 106 64 Z", RED, 5),
             ("M10 48 L110 48 L104 68 L16 68 Z", INK, 3), ("M34 54 L50 54 L48 62 L36 62 Z M70 54 L86 54 L84 62 L72 62 Z", WHITE, 0)],
    "money": [("M44 26 L76 26 L70 40 Q108 58 100 94 Q92 114 60 114 Q28 114 20 94 Q12 58 50 40 Z", WHITE, 5),
              ("M46 38 L74 38", "none", 6), ("M46 62 L74 62 M46 72 L74 72 M52 62 Q72 62 72 74 Q72 84 54 84 L74 104", "none", 6)],
    "ring": [("M30 82 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0", "none", 9), ("M42 22 L78 22 L90 36 L60 62 L30 36 Z", WHITE, 5),
             ("M30 36 L90 36 M50 22 L60 62 L70 22", "none", 3)],
    "shield": [("M60 6 L108 22 Q108 80 60 114 Q12 80 12 22 Z", RED, 5), ("M60 20 L60 98 M30 44 L90 44", "none", 5)],
    "question": [("M8 60 a52 52 0 1 0 104 0 a52 52 0 1 0 -104 0 Z", WHITE, 5),
                 ("M42 46 Q42 26 60 26 Q80 26 80 44 Q80 56 64 62 L62 74", "none", 9), ("M57 86 L67 86 L67 96 L57 96 Z", INK, 3)],
    "hawk": [("M4 52 Q30 38 50 50 L60 28 L70 50 Q90 38 116 52 Q92 62 74 64 L68 92 L52 92 L46 64 Q28 62 4 52 Z", INK, 4),
             ("M56 40 L64 40 L60 34 Z", RED, 0)],
    "cone": [("M48 10 L72 10 L98 100 L22 100 Z", RED, 5), ("M40 40 L80 40 L86 62 L34 62 Z", WHITE, 3), ("M12 100 L108 100 L108 114 L12 114 Z", INK, 4)],
    "link": [("M10 60 a28 28 0 1 0 56 0 a28 28 0 1 0 -56 0", "none", 10), ("M54 60 a28 28 0 1 0 56 0 a28 28 0 1 0 -56 0", "none", 10)],
    "poison": [("M48 8 L72 8 L72 30 Q102 44 98 80 Q96 112 60 112 Q24 112 22 80 Q18 44 48 30 Z", WHITE, 5),
               ("M42 66 Q42 48 60 48 Q78 48 78 66 Q78 76 70 78 L70 88 L50 88 L50 78 Q42 76 42 66 Z", INK, 2),
               ("M50 62 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z M62 62 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z", WHITE, 0)],
    "snake": [("M10 100 Q26 62 48 80 Q70 98 80 68 Q90 38 70 34 Q54 30 60 16 Q66 6 86 12", "none", 12),
              ("M86 12 L100 8 M86 12 L98 20", "none", 3)],
    "crown": [("M12 92 L18 32 L42 58 L60 20 L78 58 L102 32 L108 92 Z", RED, 5), ("M12 92 L108 92 L108 108 L12 108 Z", INK, 4)],
    "necklace": [("M12 14 Q60 104 108 14", "none", 6),
                 ("M24 40 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z M40 62 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z M70 62 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z M86 40 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z", WHITE, 3),
                 ("M60 70 L72 86 L60 108 L48 86 Z", RED, 4)],
    "turn": [("M60 4 L116 60 L60 116 L4 60 Z", WHITE, 6), ("M46 88 L46 62 Q46 46 64 46 L72 46", "none", 8), ("M70 34 L86 46 L70 58 Z", INK, 3)],
    "burst": [("M60 4 L70 40 L104 18 L82 50 L116 60 L82 70 L104 102 L70 80 L60 116 L50 80 L16 102 L38 70 L4 60 L38 50 L16 18 L50 40 Z", RED, 5)],
}


def svg(name, size=230):
    parts = SHAPES[name]
    border = "".join(f'<path d="{d}" fill="{WHITE if f != "none" else "none"}" stroke="{WHITE}" stroke-width="{max(w, 4) + 14}" '
                     f'stroke-linejoin="round" stroke-linecap="round"/>' for d, f, w in parts)
    ink = "".join(f'<path d="{d}" fill="{f}" stroke="{INK}" stroke-width="{w if w else 0}" stroke-linejoin="round" stroke-linecap="round"/>'
                  for d, f, w in parts)
    return (f'<svg viewBox="-10 -10 140 140" width="{size}" height="{size}" style="overflow:visible;'
            f'filter:drop-shadow(0 8px 10px rgba(0,0,0,.3))">{border}{ink}</svg>')
