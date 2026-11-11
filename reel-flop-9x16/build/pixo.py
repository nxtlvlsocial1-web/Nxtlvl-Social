"""Pixo, the imaginary pixel mascot of reel 2 in the intro (v9, owner: "an imaginary pixelated mascot who is introducing
himself, make him speak gibberish"). Everything is made here, so it is ours:
  * sprite frames on a 32x32 pixel grid (idle, talk, blink, wave-up, wave-down), upscaled with nearest neighbour;
  * a 54x96 pixel-art sunset scene, upscaled x20 to 1080x1920;
  * the gibberish: 8-bit "talk" blips synthesised syllable by syllable (square waves with a pitch glide), over a short
    chiptune loop; syllable onsets go to plan/pixo_sylls.json so his mouth moves with them.
python3 build/pixo.py
"""
import json
import math
import os
import random

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img", "pixo")
AUD = os.path.join(ROOT, "assets", "audio", "intro")
SR = 48000

C = {"o": (27, 31, 74), "b": (79, 224, 181), "B": (41, 176, 146), "h": (176, 255, 228), "w": (255, 255, 255), "p": (27, 31, 74),
     "c": (255, 130, 170), "m": (122, 31, 61), "t": (255, 110, 140), "a": (27, 31, 74), "y": (255, 214, 64), "f": (255, 159, 67), "F": (214, 112, 36)}


SKINS = {"mint": ((79, 224, 181), (41, 176, 146), (176, 255, 228)), "pink": ((255, 143, 199), (222, 92, 160), (255, 205, 230)),
         "sun": ((255, 214, 79), (232, 168, 40), (255, 240, 170))}


def sprite(mouth="closed", eyes="open", arm="down", skin="mint"):
    C["b"], C["B"], C["h"] = SKINS[skin]
    g = [[None] * 32 for _ in range(32)]

    def px(x, y, k):
        if 0 <= x < 32 and 0 <= y < 32:
            g[y][x] = C[k]
    cx, cy, r = 15.5, 18.5, 11
    for y in range(32):
        for x in range(32):
            d = math.hypot(x - cx, (y - cy) * 1.05)
            if d <= r - .5:
                k = "b"
                if (x - cx) + (y - cy) > 7:
                    k = "B"
                if math.hypot(x - (cx - 4), y - (cy - 5)) < 3.2:
                    k = "h"
                px(x, y, k)
            elif d <= r + .6:
                px(x, y, "o")
    for y in range(3, 8):                       # antenna
        px(16, y, "a")
    for x, y in [(15, 1), (16, 1), (17, 1), (15, 2), (16, 2), (17, 2), (16, 0)]:
        px(x, y, "y")
    for ex in (11, 19):                          # eyes
        if eyes == "open":
            for y in range(14, 19):
                for x in range(ex, ex + 3):
                    px(x, y, "w")
            for y in range(15, 18):
                for x in range(ex + 1, ex + 3):
                    px(x, y, "p")
            px(ex, 14, "w")
        else:
            for x in range(ex, ex + 3):
                px(x, 17, "p")
    for x, y in [(8, 20), (9, 20), (22, 20), (23, 20)]:
        px(x, y, "c")
    if mouth == "closed":
        for x in range(14, 18):
            px(x, 21, "m")
        px(13, 20, "m"), px(18, 20, "m")
    else:
        for y in range(20, 24):
            for x in range(13, 19):
                px(x, y, "m")
        for x in range(14, 18):
            px(x, 23, "t")
    for x in range(10, 14):                      # feet
        px(x, 30, "f"), px(x, 31, "F")
    for x in range(18, 22):
        px(x, 30, "f"), px(x, 31, "F")
    if arm == "down":
        for y in range(19, 24):
            px(27, y, "o"), px(28, y, "b")
        px(28, 24, "o")
    else:
        pts = [(26, 15), (27, 14), (28, 13), (29, 12), (30, 11)] if arm == "up" else [(26, 17), (27, 17), (28, 16), (29, 16), (30, 15)]
        for x, y in pts:
            px(x, y, "b"), px(x, y - 1, "o"), px(x, y + 1, "o")
        hx, hy = pts[-1]
        for dx in (0, 1):
            for dy in (-1, 0, 1):
                px(hx + dx, hy + dy, "b")
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    for y in range(32):
        for x in range(32):
            if g[y][x]:
                im.putpixel((x, y), g[y][x] + (255,))
    return im.resize((32 * 22, 32 * 22), Image.NEAREST)


def scene():
    W, H = 54, 96
    im = Image.new("RGB", (W, H))
    bands = [(43, 27, 90), (64, 33, 125), (106, 47, 176), (151, 62, 196), (193, 79, 214), (232, 100, 190), (255, 122, 168), (255, 160, 130), (255, 190, 110)]
    for y in range(H):
        im.paste(bands[min(len(bands) - 1, int(y / 72 * len(bands)))], (0, y, W, y + 1))
    rnd = random.Random(3)
    for _ in range(26):                           # stars
        x, y = rnd.randrange(W), rnd.randrange(30)
        im.putpixel((x, y), (255, 240, 200) if rnd.random() < .7 else (180, 220, 255))
    for y in range(H):                            # sun with stripes
        for x in range(W):
            if math.hypot(x - 38, y - 40) < 9 and not (y > 40 and y % 3 == 0):
                im.putpixel((x, y), (255, 214, 90) if y < 38 else (255, 170, 80))
    for cxx, cyy, w in [(12, 22, 9), (40, 14, 7), (20, 52, 8)]:   # clouds
        for y in range(cyy, cyy + 3):
            for x in range(cxx - w // 2 - (y == cyy + 1), cxx + w // 2 + 1 + (y == cyy + 1)):
                if 0 <= x < W:
                    im.putpixel((x, y), (255, 222, 236))
    for x in range(W):                            # mountains
        h1 = int(60 + 7 * math.sin(x * .25) + 4 * math.sin(x * .7))
        h2 = int(66 + 5 * math.sin(x * .33 + 1.5))
        for y in range(h1, H):
            im.putpixel((x, y), (92, 46, 140))
        for y in range(h2, H):
            im.putpixel((x, y), (66, 34, 110))
    for y in range(76, H):                        # grass + dirt
        for x in range(W):
            if y < 79:
                c = (58, 209, 122) if (x + y) % 4 else (44, 170, 98)
            elif y < 81:
                c = (44, 170, 98)
            else:
                c = (150, 96, 60) if (x * 3 + y) % 7 else (120, 74, 44)
            im.putpixel((x, y), c)
    for x in range(0, W, 5):                      # grass tufts
        im.putpixel((x, 75), (58, 209, 122))
    return im.resize((W * 20, H * 20), Image.NEAREST)


def blip(f0, dur, rnd):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + .25 * np.exp(-t * 30)) * (1 + .03 * np.sin(2 * math.pi * 9 * t))
    ph = 2 * math.pi * np.cumsum(f) / SR
    sq = np.sign(np.sin(ph)) * .55 + .45 * np.sin(2 * ph)
    env = np.minimum(1, t / .006) * np.exp(-t * (6 + rnd.uniform(0, 6)))
    return sq * env


def gibberish():
    words = ["Blip-blop!", "Mi", "Pi-xo!", "Zib-ba", "wum-wum,", "ka-pow", "zee!"]
    rnd = random.Random(9)
    out, sylls, wtimes, t = [], [], [], .08
    base = [784, 880, 988, 1047, 880, 740, 1175]
    for wi, w in enumerate(words):
        wtimes.append(round(t, 3))
        for s in w.strip("!,").split("-"):
            d = rnd.uniform(.075, .11) * max(1, len(s) / 3)
            sylls.append(round(t, 3))
            out.append((t, blip(rnd.choice(base) * rnd.uniform(.93, 1.07), d, rnd)))
            t += d + .03
        t += .09 if not w.endswith(("!", ",")) else .17
    total = t + .2
    buf = np.zeros(int(total * SR))
    for t0, b in out:
        i = int(t0 * SR)
        buf[i:i + len(b)] += b[:len(buf) - i]
    # a little chiptune bed: bass + arpeggio at 150 BPM
    beat = 60 / 150
    bed = np.zeros_like(buf)
    notes = [(196, 247, 294), (220, 262, 330), (175, 220, 262), (196, 247, 294)]
    for k in range(int(total / (beat / 2)) + 1):
        root = notes[(k // 8) % 4]
        tt = k * beat / 2
        i = int(tt * SR)
        n = int(beat / 2 * SR * .9)
        x = np.arange(n) / SR
        arp = np.sign(np.sin(2 * math.pi * root[k % 3] * 2 * x)) * np.exp(-x * 9) * .16
        bass = (2 * np.abs(2 * ((root[0] / 2 * x) % 1) - 1) - 1) * np.exp(-x * 3) * .3 if k % 2 == 0 else 0
        seg = arp + bass
        bed[i:i + n] += seg[:max(0, len(bed) - i)]
    mix = buf * .55 + bed * .5
    mix /= np.max(np.abs(mix)) * 1.15
    st = np.stack([mix, mix], 1).astype(np.float32)
    import soundfile as sf
    sf.write(os.path.join(AUD, "gibberish.wav"), st, SR)
    json.dump({"sylls": sylls, "words": words, "word_t": wtimes, "dur": round(total, 3)}, open(os.path.join(ROOT, "plan", "pixo_sylls.json"), "w"), indent=0)
    return total


def dance_song(bars=2, bpm=150):
    """v10 (owner: "make those mascots dance to a funny song based on their setting"): a goofy 8-bit polka-ish tune,
    oom-pah bass, a silly melody with pitch slides, noise snares, spring "boings"; made here, original."""
    import soundfile as sf
    beat = 60 / bpm
    n_beats = bars * 4 + 1
    total = n_beats * beat + .3
    buf = np.zeros(int(total * SR))
    t_all = np.arange(len(buf)) / SR

    def add(t0, sig):
        i = int(t0 * SR)
        n = min(len(sig), len(buf) - i)
        if n > 0:
            buf[i:i + n] += sig[:n]

    def sq(f, d, vol=.3, slide=1.0, duty=.5, dec=6):
        n = int(d * SR)
        t = np.arange(n) / SR
        ff = f * (slide ** (t / d))
        ph = np.cumsum(ff) / SR % 1
        return np.where(ph < duty, 1, -1) * np.exp(-t * dec) * vol

    def tri(f, d, vol=.4):
        n = int(d * SR)
        t = np.arange(n) / SR
        return (2 * np.abs(2 * ((f * t) % 1) - 1) - 1) * np.exp(-t * 5) * vol

    def noise(d, vol=.25, dec=28):
        n = int(d * SR)
        r = np.random.default_rng(int(d * 1e4)).uniform(-1, 1, n)
        return r * np.exp(-np.arange(n) / SR * dec) * vol
    roots = [(131, 196), (147, 220), (131, 196), (98, 147)]
    mel = [523, 659, 784, 659, 698, 880, 784, 523, 587, 740, 880, 740, 784, 659, 523, 392]
    for b in range(n_beats):
        t = b * beat
        r = roots[(b // 2) % 4]
        add(t, tri(r[0] if b % 2 == 0 else r[1], beat * .8, .42))             # oom-pah
        if b % 2:
            add(t, noise(.12, .22))                                            # snare
        add(t, sq(60, .06, .5, slide=.4, dec=40))                              # kick blip
        for h in (0, 1):                                                        # melody in eighths, some sliding
            k = (b * 2 + h) % len(mel)
            sl = 1.12 if k % 5 == 2 else (.89 if k % 7 == 3 else 1.0)
            add(t + h * beat / 2, sq(mel[k], beat / 2 * .9, .2, slide=sl, duty=.25, dec=7))
        if b % 4 == 3:                                                          # boing
            add(t + beat / 2, sq(220, .35, .22, slide=3.2, duty=.5, dec=5))
    buf /= np.max(np.abs(buf)) * 1.12
    sf.write(os.path.join(AUD, "dance.wav"), np.stack([buf, buf], 1).astype(np.float32), SR)
    json.dump({"bpm": bpm, "beat": beat, "beats": [round(b * beat, 3) for b in range(n_beats)], "dur": round(total, 3)},
              open(os.path.join(ROOT, "plan", "dance.json"), "w"), indent=0)
    return total


def main():
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(AUD, exist_ok=True)
    for skin in ("mint", "pink", "sun"):
        for name, kw in [("idle", {}), ("talk", {"mouth": "open"}), ("blink", {"eyes": "closed"}), ("waveup", {"arm": "up", "mouth": "open"}), ("wavedn", {"arm": "mid", "mouth": "open"})]:
            fn = f"{name}.png" if skin == "mint" else f"{skin}_{name}.png"
            sprite(skin=skin, **kw).save(os.path.join(IMG, fn))
    print("dance song", round(dance_song(bars=1), 2), "s")
    scene().save(os.path.join(IMG, "bg.png"))
    print("gibberish", round(gibberish(), 2), "s; sprites + scene written")


if __name__ == "__main__":
    main()
