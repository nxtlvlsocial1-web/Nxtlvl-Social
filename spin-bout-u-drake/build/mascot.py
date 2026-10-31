"""The live pixel mascot of Drake for v14 (owner: "make a live pixel mascot of him and animate him"), drawn by hand in
code (not a pixelated photo): a chibi Drake (cornrows, full beard, black hoodie, gold chain, white sneakers) with
animation frames, a pixel girl, a pixel diamond, sparkle and heart. Writes sprite sheets to assets/img/pixel/
(our own drawings, committed):
  drake_sheet.png  44 x 40 frames: idle0 idle1 walk0 walk1 walk2 walk3 aim shoot drop
  girl_sheet.png   28 x 40 frames: idle0 idle1 happy0 happy1   (facing left)
  guy_sheet.png    24 x 40 frames: idle0 idle1 hit
  diamond.png, sparkle.png, heart.png

python3 build/mascot.py
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "pixel")
K, S, S2, H, H2 = (20, 18, 19), (122, 74, 46), (94, 56, 34), (27, 20, 20), (64, 50, 48)
B, D, D2, G, P = (24, 18, 17), (32, 32, 38), (56, 56, 66), (232, 184, 74), (40, 40, 48)
W, R, A, A2 = (242, 241, 236), (176, 25, 79), (78, 78, 88), (120, 120, 132)
DRAKE_FRAMES = ["idle0", "idle1", "walk0", "walk1", "walk2", "walk3", "aim", "shoot", "drop"]


class Canvas:
    def __init__(self, w, h):
        self.im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.w, self.h = w, h

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.im.putpixel((x, y), c + (255,))

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def outline(self):
        src = self.im.copy()
        for y in range(self.h):
            for x in range(self.w):
                if src.getpixel((x, y))[3]:
                    continue
                if any(0 <= x + dx < self.w and 0 <= y + dy < self.h and src.getpixel((x + dx, y + dy))[3]
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    self.im.putpixel((x, y), K + (255,))
        return self.im


def drake(pose):
    c = Canvas(44, 40)
    walk = {"walk0": (2, -2, "r"), "walk1": (0, 0, ""), "walk2": (-2, 2, "l"), "walk3": (0, 0, "")}
    lo, ro, lift = walk.get(pose, (0, 0, ""))
    bob = 1 if pose in ("idle1", "walk1", "walk3") else 0
    # legs and sneakers (no bob, they stay on the floor)
    for (x0, off, side) in ((11, lo, "l"), (17, ro, "r")):
        up = 1 if lift == side else 0
        c.rect(x0 + off, 30 - up, x0 + off + 3, 35 - up, P)
        c.rect(x0 + off - 1, 36 - up, x0 + off + 4, 37 - up, W)
        c.px(x0 + off + 1, 36 - up, R)
        c.px(x0 + off + 2, 36 - up, R)
    y = bob
    # back arm
    c.rect(8, 19 + y, 9, 26 + y, D)
    c.rect(8, 27 + y, 9, 28 + y, S)
    # hoodie, pocket, chain
    c.rect(11, 17 + y, 20, 18 + y, D)
    c.rect(10, 18 + y, 21, 29 + y, D)
    c.rect(12, 24 + y, 19, 28 + y, D2)
    c.rect(13, 25 + y, 18, 25 + y, D)
    for gx, gy in ((13, 19), (18, 19), (14, 20), (15, 21), (16, 21), (17, 20)):
        c.px(gx, gy + y, G)
    c.px(15, 22 + y, G)
    c.px(16, 22 + y, W)
    # head: cornrows, face, ear, eyes, nose, beard
    c.rect(10, 3 + y, 21, 6 + y, H)
    for bx in (11, 13, 15, 17, 19, 21):
        c.rect(bx, 3 + y, bx, 5 + y, H2)
    c.rect(10, 7 + y, 21, 16 + y, S)
    c.rect(10, 7 + y, 13, 8 + y, H)                         # hairline at the side
    c.rect(10, 9 + y, 11, 12 + y, S2)                       # ear
    c.px(11, 10 + y, S)
    for ex in (15, 19):
        c.rect(ex, 9 + y, ex + 1, 9 + y, H)                 # brows
        c.px(ex, 10 + y, W)
        c.px(ex + 1, 10 + y, K)
    c.rect(21, 11 + y, 21, 12 + y, S2)
    c.px(22, 12 + y, S)                                     # nose
    c.rect(12, 13 + y, 21, 13 + y, B)
    c.rect(11, 14 + y, 21, 16 + y, B)
    c.rect(17, 13 + y, 20, 13 + y, B)
    c.rect(18, 14 + y, 20, 14 + y, S2)                      # lip
    c.rect(13, 17 + y, 18, 17 + y, B)                       # beard under the jaw
    # front arm by pose
    if pose in ("aim", "shoot"):
        r = -1 if pose == "shoot" else 0
        for k in range(8):                                  # diagonal sleeve up to the right
            ax, ay = 20 + k + r, 20 - k * 6 // 8 + y + r
            c.rect(ax, ay, ax + 1, ay + 2, D)
        hx, hy = 28 + r, 13 + y + r
        c.rect(hx, hy, hx + 2, hy + 2, S)
        c.rect(hx + 2, hy - 1, hx + 8, hy, A)               # barrel
        c.rect(hx + 3, hy - 1, hx + 7, hy - 1, A2)
        c.rect(hx + 2, hy + 1, hx + 3, hy + 3, A)           # grip
    elif pose == "drop":
        c.rect(20, 20 + y, 28, 22 + y, D)
        c.rect(29, 21 + y, 31, 23 + y, S)
        c.px(29, 24 + y, S)
        c.px(31, 24 + y, S)
    else:
        c.rect(20, 19 + y, 22, 26 + y, D)
        c.rect(20, 27 + y, 22, 28 + y, S)
    return c.outline()


def girl(pose):
    c = Canvas(28, 40)
    bob = 1 if pose in ("idle1", "happy1") else 0
    LS, LS2, HR, HR2, TOP, TOP2 = (176, 112, 78), (146, 88, 58), (44, 26, 22), (78, 46, 38), (176, 25, 79), (220, 60, 120)
    for x0 in (11, 15):
        c.rect(x0, 31, x0 + 2, 35, LS)
        c.rect(x0 - 1, 36, x0 + 3, 37, W)
    y = bob
    c.rect(9, 6 + y, 20, 26 + y, HR)                        # long hair behind
    c.rect(10, 18 + y, 19, 26 + y, TOP)                     # top
    c.rect(9, 25 + y, 20, 30 + y, TOP2)                     # skirt
    c.rect(12, 19 + y, 17, 19 + y, TOP2)
    c.rect(10, 4 + y, 19, 6 + y, HR)
    c.rect(11, 7 + y, 19, 16 + y, LS)                       # face
    c.rect(10, 7 + y, 12, 15 + y, HR)                       # side hair
    c.rect(11, 4 + y, 19, 7 + y, HR)
    for hx in (12, 15, 18):
        c.px(hx, 5 + y, HR2)
    for ex in (14, 17):
        c.px(ex, 10 + y, K)
        c.px(ex, 9 + y, HR)
    c.rect(18, 12 + y, 18, 12 + y, LS2)
    c.rect(15, 14 + y, 17, 14 + y, (196, 40, 90))           # lips
    c.px(13, 12 + y, (232, 130, 150))                       # blush
    c.px(19, 12 + y, (232, 130, 150))
    c.rect(14, 17 + y, 16, 17 + y, LS2)                     # neck
    if pose.startswith("happy"):
        c.rect(7, 12 + y, 8, 19 + y, LS)                    # arms up
        c.rect(21, 12 + y, 22, 19 + y, LS)
        c.rect(7, 10 + y, 8, 11 + y, LS)
        c.rect(21, 10 + y, 22, 11 + y, LS)
        c.px(16, 15 + y, W)                                 # smile
    else:
        c.rect(8, 19 + y, 9, 27 + y, LS)
        c.rect(20, 19 + y, 21, 27 + y, LS)
    return c.outline().transpose(Image.FLIP_LEFT_RIGHT)


def guy(pose):
    from pixel import GUY, grid  # the hand-drawn guy from v13, given idle / hit frames
    base = grid(GUY)
    im = Image.new("RGBA", base.size, (0, 0, 0, 0))
    if pose == "idle1":
        top = base.crop((0, 0, base.width, 27))
        im.paste(base.crop((0, 27, base.width, base.height)), (0, 27))
        im.alpha_composite(top, (0, 1))
    elif pose == "hit":
        im = base.copy()
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a:
                    px[x, y] = (255, 255, 255, 255) if (r + g + b) > 60 else (r, g, b, a)
    else:
        im = base
    return im


def sheet(frames):
    w, h = frames[0].size
    out = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    for k, f in enumerate(frames):
        out.alpha_composite(f, (k * w, 0))
    return out


def grid_rows(rows, pal):
    w, h = max(len(r) for r in rows), len(rows)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in pal:
                im.putpixel((x, y), pal[ch] + (255,))
    return im


DIAMOND = ["..kkkkk..", ".kwcwcck.", "kwwccwcck", "kkkkkkkkk", ".kcwccck.", "..kcwck..", "...kck...", "....k...."]
SPARKLE = ["..w..", "..w..", "wwyww", "..w..", "..w.."]
HEART = [".kk.kk.", "krrkrrk", "krrrrrk", ".krrrk.", "..krk..", "...k..."]


def main():
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(OUT, exist_ok=True)
    sheet([drake(p) for p in DRAKE_FRAMES]).save(os.path.join(OUT, "drake_sheet.png"))
    sheet([girl(p) for p in ("idle0", "idle1", "happy0", "happy1")]).save(os.path.join(OUT, "girl_sheet.png"))
    sheet([guy(p) for p in ("idle0", "idle1", "hit")]).save(os.path.join(OUT, "guy_sheet.png"))
    pal = {"k": K, "w": W, "c": (127, 216, 255), "y": (255, 214, 64), "r": (230, 40, 100)}
    grid_rows(DIAMOND, pal).save(os.path.join(OUT, "diamond.png"))
    grid_rows(SPARKLE, pal).save(os.path.join(OUT, "sparkle.png"))
    grid_rows(HEART, pal).save(os.path.join(OUT, "heart.png"))
    print("wrote", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
