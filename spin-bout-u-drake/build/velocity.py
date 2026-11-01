"""Velocity edit footage for the ending (owner, v18): from the second "the way" (44.28 s) to the end, the walking clip
(clip A) runs with a velocity speed curve locked to the song: every two beats it hangs in slow motion just after the
hit (0.32x) and whips up to 3x into the next one, so the motion lands on the beat. Writes assets/video/clips/vel_end.mp4
(30 fps, the length of the section; not in git).

python3 build/velocity.py
"""
import glob
import json
import os
import subprocess

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "video", "src", "clip_a.mp4")
T0, T1, FPS, S0 = 44.28, 60.0, 30, 3.0        # section start / end on the song, output fps, where the clip starts


def speed(u):
    """u in [0,1) through a two-beat cycle: slow-mo hang after the hit, ramp, fast into the next hit."""
    if u < .5:
        return .32
    if u < .8:
        return .32 + (3.0 - .32) * ((u - .5) / .3) ** 2
    return 3.0


def main():
    beats = [b for b in json.load(open(os.path.join(ROOT, "plan", "beats.json")))["beats"]]
    cyc = [b for b in beats[::2] if T0 - 1 <= b <= T1 + 1]
    fdir = os.path.join(ROOT, "cache", "vel_frames")
    if not glob.glob(os.path.join(fdir, "*.jpg")):
        os.makedirs(fdir, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-vf", "fps=30,scale=720:-2", "-q:v", "3",
                        os.path.join(fdir, "f%04d.jpg")], check=True)
    frames = sorted(glob.glob(os.path.join(fdir, "*.jpg")))
    n_out = int(round((T1 - T0) * FPS))
    s, src_idx = S0, []
    for k in range(n_out):
        t = T0 + k / FPS
        prev = max([b for b in cyc if b <= t] or [cyc[0]])
        nxt = min([b for b in cyc if b > t] or [prev + .76])
        u = (t - prev) / max(1e-3, nxt - prev)
        src_idx.append(min(len(frames) - 1, int(round(s * FPS))))
        s += speed(u) / FPS
    w, h = Image.open(frames[0]).size
    out = os.path.join(ROOT, "assets", "video", "clips", "vel_end.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS),
                          "-i", "-", "-vf", "eq=contrast=1.08:saturation=.92", "-c:v", "libx264", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in src_idx:
        p.stdin.write(np.asarray(Image.open(frames[i]).convert("RGB")).tobytes())
    p.stdin.close()
    p.wait()
    print(f"wrote {out}: {n_out} frames, source {S0:.1f}-{s:.1f} s")


if __name__ == "__main__":
    main()
