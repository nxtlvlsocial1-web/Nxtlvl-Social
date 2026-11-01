"""Liquid gradient background for Ashke v10 (owner: "remove the white grids, go for a gradient background"), built the
way the owner's CreateGradients pack builds its looks (a 4-colour gradient warped by animated turbulent displacement), in the Ashke palette (blood red, crimson, an ember highlight, near-black). Pre-rendered so the browser render
stays cheap: writes assets/video/fluid_bg.mp4 (540x540, 30 fps, the full edit length; the page scales it up, it is
soft by design).

python3 build/fluidbg.py     (needs numpy and ffmpeg)
"""
import json
import os
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, FPS, DUR = 540, 30, 60.0
BEATS = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))["beats"]

# (colour, path centre x, y, radius of the path, speed, phase, weight)
PTS = [((120, 12, 20), .25, .30, .18, .11, 0.0, 1.0),      # blood red
       ((216, 35, 42), .72, .35, .20, .13, 1.9, .85),      # crimson (the edit's red)
       ((255, 112, 60), .58, .72, .16, .17, 3.4, .38),     # ember highlight
       ((52, 8, 16), .22, .78, .19, .09, 4.6, 1.0)]        # deep maroon
BASE = np.array((12, 5, 6), float)                         # near-black warm floor


def frame(t, yy, xx):
    # turbulent displacement: two octaves of drifting sine noise warp the coordinates (domain warping)
    wx = xx + .07 * np.sin(yy * 7.0 + t * .55 + np.sin(xx * 5.0 - t * .4)) + .035 * np.sin(yy * 17 + xx * 9 - t * 1.1)
    wy = yy + .07 * np.sin(xx * 6.0 - t * .45 + np.sin(yy * 4.0 + t * .35)) + .035 * np.sin(xx * 15 - yy * 11 + t * .9)
    lb = max([b for b in BEATS if b <= t] or [-9])
    pulse = 1.0                                            # v16: no beat throb (owner: no pulsing effects)
    acc = np.zeros(xx.shape + (3,))
    wsum = np.full(xx.shape, .9)                           # the base colour's share
    acc += .9 * BASE
    for (col, cx, cy, r, sp, ph, wt) in PTS:
        px = cx + r * np.sin(t * sp * 2 * np.pi * .35 + ph)
        py = cy + r * np.cos(t * sp * 2 * np.pi * .28 + ph * 1.3)
        d2 = (wx - px) ** 2 + (wy - py) ** 2
        w = wt * pulse ** (1 if col[0] > 200 else .5) / (d2 * 22 + .02) ** 1.15
        acc += w[..., None] * np.array(col, float)
        wsum += w
    img = acc / wsum[..., None]
    v = np.hypot(xx - .5, yy - .5)                         # soft vignette
    img *= (1 - .55 * np.clip(v - .25, 0, 1) ** 1.2)[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    out = os.path.join(ROOT, "assets", "video", "fluid_bg.mp4")
    yy, xx = np.mgrid[0:N, 0:N] / N
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{N}x{N}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(int(DUR * FPS) + FPS):
        p.stdin.write(frame(f / FPS, yy, xx).tobytes())
    p.stdin.close()
    p.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
