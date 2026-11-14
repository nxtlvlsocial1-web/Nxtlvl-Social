"""Pexels clips -> graded vertical 1080x1920 proxies in assets/video/<id>.mp4 (one look for the whole reel: slightly
cool, lower saturation, a touch more contrast, soft vignette, the premium sports-documentary grade the brief asks for).
Horizontal sources are cropped to 9:16 around FOCUS (0..1 of the width). Keyframe every 10 frames for clean seeks.
python3 build/prep_footage.py [ids]
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "footage", "pexels")
OUT = os.path.join(ROOT, "assets", "video")
FOCUS = {"8533122": .45, "8456204": .5, "8456207": .5, "8533918": .55, "6388432": .5, "16408434": .5, "9943211": .5,
         "6084027": .42, "6078634": .42, "5837709": .55, "4745804": .43, "5192026": .3, "9431556": .52, "4468823": .5,
         "11755921": .5, "5730331": .55}
GRADE = ("eq=contrast=1.07:saturation=0.84:brightness=-0.015,"
         "colorbalance=rs=-0.03:bs=0.05:rm=-0.01:bm=0.02:rh=0.01:bh=-0.01,vignette=angle=PI/5")


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", p],
                       capture_output=True, text=True).stdout.strip().split(",")
    return int(r[0]), int(r[1])


def main():
    os.makedirs(OUT, exist_ok=True)
    ids = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(SRC) if f.endswith(".mp4"))
    for vid in ids:
        src, dst = os.path.join(SRC, vid + ".mp4"), os.path.join(OUT, vid + ".mp4")
        w, h = probe(src)
        if w / h > 9 / 16 + .01:          # wider than 9:16: crop around the focus
            cw = round(h * 9 / 16 / 2) * 2
            x = min(max(0, round(FOCUS.get(vid, .5) * w - cw / 2)), w - cw)
            geo = f"crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos"
        else:
            geo = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-an", "-vf", f"{geo},{GRADE},fps=30,format=yuv420p",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-g", "10", "-movflags", "+faststart", dst], check=True)
        print(vid, w, "x", h, "->", round(os.path.getsize(dst) / 1e6, 1), "MB", flush=True)


if __name__ == "__main__":
    main()
