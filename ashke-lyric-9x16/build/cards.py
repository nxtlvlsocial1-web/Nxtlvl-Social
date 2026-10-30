"""Footage for the photo prints in the v3 edit: two card tracks, each 720x900 (4:5), 30 fps stepped to 15 fps, black
outside the scenes that use them, plus the photos that fill the giant R2 keywords.

python3 build/cards.py      (from the project root; needs ffmpeg; reads the shot plan in build/plan.py)

Shots come from the owner's two clips (assets/video/src/estate.mp4, the estate shoot at 1276x718, and tour.mp4, the
Manchester concert at 1200x720) at close to their own resolution, so the prints stay sharp (no 9:16 blow-ups). Look:
photocopy black and white (grey, auto-levels, hard curve, sharpened, fine grain), the dark R2 print a stop lower.
Each print opens on the sharpest frame of its shot (searched over its first 0.6 s), held for 8 frames, then runs into
the moving footage from that frame. Writes assets/video/card1.mp4, card2.mp4, assets/img/photo/fill_<line>.jpg
(black-and-white threshold photos) and assets/img/photo/frame_<shot>.jpg (each shot's best frame in the print look,
for the single-frame transitions).
"""
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan import CARD1, CARD2, FILL, RECIPE, ROOT, SHOTS, scenes  # noqa: E402

V = os.path.join(ROOT, "assets", "video")
SRC = {"estate": (os.path.join(V, "src", "estate.mp4"), 1276, 718), "tour": (os.path.join(V, "src", "tour.mp4"), 1200, 720)}
LOOK = ("format=gray,normalize=smoothing=20:independence=0,eq=contrast=1.6:brightness={b}:gamma=1.1,"
        "unsharp=5:5:1.4,noise=alls=6:allf=u,tpad=stop_mode=clone:stop_duration=4,fps=15,fps=30,"
        "tpad=start_mode=clone:start_duration=0.267,format=yuv420p")
_BEST = {}


def best_time(shot):
    """The sharpest frame (variance of a Laplacian) in the shot's first 0.6 s (so the print never runs into a
    neighbouring shot)."""
    if shot in _BEST:
        return _BEST[shot]
    src, st, fx = SHOTS[shot]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-t", "0.6", "-i", SRC[src][0], "-vf", "fps=10,scale=320:-2,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    h = 180 if src == "estate" else 192
    fr = np.frombuffer(raw, np.uint8)
    fr = fr[: len(fr) // (320 * h) * 320 * h].reshape(-1, h, 320).astype(np.float32)
    lap = [np.var(f[1:-1, 1:-1] * 4 - f[:-2, 1:-1] - f[2:, 1:-1] - f[1:-1, :-2] - f[1:-1, 2:]) for f in fr]
    _BEST[shot] = st + int(np.argmax(lap)) / 10
    return _BEST[shot]


def crop(src, fx):
    _, w, h = SRC[src]
    cw = round(h * .8) // 2 * 2
    x = max(0, min(w - cw, round(fx * w - cw / 2)))
    return f"crop={cw}:{h}:{x}:0,scale=720:900:flags=lanczos,setsar=1"


def track(name, plan):
    d = os.path.join(ROOT, "cache", f"{name}_parts")
    os.makedirs(d, exist_ok=True)
    parts, t = [], 0.0
    segs = [(a, b, li) for a, b, li in scenes() if li in plan]
    for i, (a, b, li) in enumerate(segs + [(60.0, 60.0, None)]):
        if a > t + .001:                                     # black filler
            out = os.path.join(d, f"g{i:03d}.mp4")
            n = round(a * 30) - round(t * 30)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=720x900:r=30", "-frames:v", str(n),
                            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], check=True)
            parts.append(out)
        if li is None:
            break
        src, _, fx = SHOTS[plan[li]]
        st = best_time(plan[li])
        out = os.path.join(d, f"s{i:03d}.mp4")
        n = round(b * 30) - round(a * 30)
        b_ = "-.12" if RECIPE[li] == "R2" else ".03"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{st:.3f}", "-i", SRC[src][0], "-vf", f"{crop(src, fx)},{LOOK.format(b=b_)}",
                        "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30", out], check=True)
        parts.append(out)
        t = b
    with open(os.path.join(d, "list.txt"), "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(d, "list.txt"), "-c", "copy",
                    os.path.join(V, f"{name}.mp4")], check=True)


def fills():
    od = os.path.join(ROOT, "assets", "img", "photo")
    os.makedirs(od, exist_ok=True)
    for li, shot in FILL.items():
        src, st, fx = SHOTS[shot]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{st + .4:.3f}", "-i", SRC[src][0], "-frames:v", "1", "-vf",
                        "format=gray,normalize=independence=0,eq=contrast=2.4,format=rgb24,"
                        "lutrgb=r='if(gt(val,70),242,20)':g='if(gt(val,70),238,18)':b='if(gt(val,70),230,18)',scale=1200:-2",
                        "-q:v", "2", os.path.join(od, f"fill_{li}.jpg")], check=True)


def frames():
    od = os.path.join(ROOT, "assets", "img", "photo")
    os.makedirs(od, exist_ok=True)
    for shot, (src, _, fx) in SHOTS.items():
        t = best_time(shot)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", SRC[src][0], "-frames:v", "1", "-vf",
                        f"{crop(src, fx)},{LOOK.format(b='.03').split(',tpad')[0]}", "-q:v", "2", os.path.join(od, f"frame_{shot}.jpg")], check=True)


if __name__ == "__main__":
    frames()
    track("card1", CARD1)
    track("card2", CARD2)
    fills()
    print("wrote assets/video/card1.mp4, card2.mp4 and assets/img/photo/fill_*.jpg")
