"""Segments of the owner's two Drake clips (assets/video/src/clip_a.mp4 backstage walk, clip_b.mp4 phone in the arena
seats) cut for v13: 30 fps, no audio, a little contrast and a touch of warmth so they sit in the edit's grade.
Writes assets/video/clips/<name>.mp4 (not in git).

python3 build/clips_drake.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEG = {   # name: (source, start s, end s)
    "b_phone1": ("clip_b", 0.2, 2.3),     # one call, you in runway shows: phone close-up
    "b_seated": ("clip_b", 7.3, 9.5),     # one call, I'm sittin' front row: in the seats
    "b_phone2": ("clip_b", 2.1, 4.2),     # one call and my n**** ten toes
    "a_close": ("clip_a", 9.4, 13.4),     # wipe him like he snotty: close-up
    "a_walk": ("clip_a", 0.4, 3.6),       # the ending: walking in, smiling
}


def main():
    os.makedirs(os.path.join(ROOT, "assets", "video", "clips"), exist_ok=True)
    for name, (src, a, b) in SEG.items():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", os.path.join(ROOT, "assets", "video", "src", src + ".mp4"),
                        "-vf", "fps=30,scale=720:-2,eq=contrast=1.08:saturation=.92:gamma=.97,colorbalance=rs=.03:bs=-.02",
                        "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        os.path.join(ROOT, "assets", "video", "clips", name + ".mp4")], check=True)
        print("wrote", name)


if __name__ == "__main__":
    main()
