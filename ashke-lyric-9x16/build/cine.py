"""The cinematic layer (from the owner's eimantasbitinas23 reference): full-bleed, colour-graded music-video shots that
take over the screen on the hit lines and the bursts, between the collage scenes.

python3 build/cine.py      (from the project root; needs ffmpeg)

Writes assets/video/cine.mp4 (1080x1920, 30 fps, 60 s; black outside the cinema segments) and assets/img/stills/c*.jpg
(colour stills for the photo-grid scenes). Shots are cropped to 9:16 out of the 2:1 picture around Karan (crop centres
picked by eye from contact sheets) and graded like the reference: red monochrome, film colour (teal shadows, warm
highlights, heavy moving grain), one-bit threshold noise, silver black and white. The reference's pacing: long smooth
holds at the full frame rate (not stepped like the collage), broken by flurries of 4-frame cuts that cycle grades.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "video", "music-video-src.mp4")
OFF = 134.40                       # MV time = edit time + 134.40 keeps the lip-sync
DUR = 60.0
GRADE = {
    "film": "eq=contrast=1.12:saturation=1.3:gamma=.95,colorbalance=rs=-.08:gs=.04:bs=.08:rh=.08:gh=.02:bh=-.08,"
            "unsharp=5:5:.8,noise=alls=26:allf=t+u,vignette=PI/5",
    "red": "format=gray,normalize=smoothing=20:independence=0,eq=contrast=1.45:gamma=1.2,format=rgb24,colorchannelmixer=rr=1:gg=.13:bb=.11,"
           "noise=alls=14:allf=t,vignette=PI/4",
    "thresh": "format=gray,normalize=smoothing=20:independence=0,eq=contrast=2.2:brightness=.08,noise=alls=60:allf=t+u,lutyuv=y='if(gt(val,128),235,16)'",
    "silver": "format=gray,normalize=smoothing=20:independence=0,eq=contrast=1.5:gamma=.9,unsharp=5:5:1.2,noise=alls=10:allf=t,vignette=PI/4",
}


def crop(cx):
    x = max(0, min(568 - 180, cx - 90)) + 36
    return f"crop=180:320:{x}:20,scale=1080:1920:flags=lanczos,setsar=1"


# (edit start, edit end, MV time at the start or None for sync, crop centre, grade)
HOLD = [
    (0.0, 1.2, None, 170, "red"), (1.2, 1.9, None, 280, "red"),                                   # intro
    (6.84, 7.24, None, 220, "thresh"), (7.24, 8.0, None, 225, "film"), (8.0, 9.04, None, 282, "film"),   # SHADY
    (23.38, 23.78, None, 300, "thresh"), (23.78, 24.2, OFF + 57.0, 320, "red"), (24.2, 24.76, None, 270, "red"),   # JATT KHULLA
    (35.74, 36.14, None, 425, "thresh"), (36.14, 36.5, None, 425, "film"), (36.5, 37.74, None, 320, "film"),  # DAAKA
    (48.46, 48.86, None, 290, "red"), (48.86, 49.84, None, 300, "thresh"),                          # JATT MUDHTO ZEHRI
    (57.0, 58.6, None, 325, "film"), (58.6, 59.2, None, 285, "film"), (59.2, 59.5, None, 310, "film"), (59.5, 60.0, None, 400, "film"),
]
# flurry pool: (MV time, crop centre); 4-frame cuts that cycle the grades
POOL = [(OFF + 16.04, 286), (OFF + 7.3, 234), (OFF + 24.3, 288), (OFF + 36.7, 320), (OFF + 57.4, 324), (OFF + 14.69, 284),
        (OFF + .3, 170), (OFF + 48.9, 300), (OFF + 37.1, 330), (OFF + 8.6, 284)]
FLURRY = [(14.24, 15.8), (44.92, 46.24)]
FLURRY_LAND = [(15.8, 16.26, None, 286, "thresh")]
CYCLE = ["thresh", "red", "film", "silver"]


def segments():
    segs = list(HOLD) + list(FLURRY_LAND)
    k = 0
    for a, b in FLURRY:
        t = a
        while t < b - .01:
            e = min(b, t + 4 / 30)
            src, cx = POOL[k % len(POOL)]
            segs.append((t, e, src + (t - a), cx, CYCLE[k % len(CYCLE)]))
            t, k = e, k + 1
    segs.sort()
    # black filler between segments
    out, t = [], 0.0
    for s in segs:
        if s[0] > t + .001:
            out.append((t, s[0], "black", 0, ""))
        out.append(s)
        t = s[1]
    if t < DUR:
        out.append((t, DUR, "black", 0, ""))
    return out


def build():
    d = os.path.join(ROOT, "cache", "cine_parts")
    os.makedirs(d, exist_ok=True)
    parts = []
    for i, (a, b, src, cx, grade) in enumerate(segments()):
        n = round(b * 30) - round(a * 30)
        if n <= 0:
            continue
        out = os.path.join(d, f"c{i:03d}.mp4")
        if src == "black":
            cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:r=30", "-frames:v", str(n)]
        else:
            ms = a + OFF if src is None else src
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{ms:.3f}", "-i", SRC, "-vf", f"{crop(cx)},{GRADE[grade]},fps=30,format=yuv420p",
                   "-frames:v", str(n), "-an"]
        subprocess.run(cmd + ["-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30", out], check=True)
        parts.append(out)
    with open(os.path.join(d, "list.txt"), "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(d, "list.txt"), "-c", "copy",
                    os.path.join(ROOT, "assets", "video", "cine.mp4")], check=True)
    # colour stills for the photo grid (film grade, no grain), centre crops around the subject
    sd = os.path.join(ROOT, "assets", "img", "stills")
    picks = [(OFF + 7.3, 234), (OFF + 16.04, 286), (OFF + 24.3, 288), (OFF + 36.7, 320), (OFF + 57.4, 324), (OFF + 14.69, 284),
             (OFF + .3, 170), (OFF + 48.9, 300), (OFF + 37.1, 330), (OFF + 8.6, 284), (72.5, 284), (76.0, 284), (60.5, 284), (108.0, 284)]
    for k, (t, cx) in enumerate(picks):
        x = max(0, min(568 - 300, cx - 150)) + 36
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", SRC, "-frames:v", "1", "-vf",
                        f"crop=300:240:{x}:60,scale=600:480:flags=lanczos,eq=contrast=1.12:saturation=1.25,"
                        "colorbalance=rs=-.06:gs=.03:bs=.06:rh=.06:bh=-.06,unsharp=5:5:.8", "-q:v", "3",
                        os.path.join(sd, f"c{k:02d}.jpg")], check=True)


if __name__ == "__main__":
    build()
    print("wrote assets/video/cine.mp4 and assets/img/stills/c*.jpg")
