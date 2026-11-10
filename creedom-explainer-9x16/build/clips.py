"""The app clips from the owner's screen recording (assets/video/screen.mp4, iPhone, 1320x2868, recorded dimmed to
about half brightness). Each clip is brightened back (x2.02), trimmed, sped to fit its line of the voiceover and
scaled to 660x1434 for the phone frame.  python3 build/clips.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "video", "screen.mp4")
CLIPS = [  # name, source start, source end, output seconds
    ("c1_pick", 12.6, 15.6, 2.0),     # the prompt, then "Pick one Reel" and the reel picked
    ("c2_steps", 15.6, 30.0, 2.0),    # Cree on it: the checklist ticking through
    ("c3_score", 95.5, 103.5, 6.6),   # the score lands (3 -> 4 / 5), second by second
    ("c4_fixes", 103.5, 113.4, 4.1),  # the fixes, then the hooks that would have gone viral
]
for name, a, b, d in CLIPS:
    sp = (b - a) / d
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-t", f"{b - a}", "-i", SRC, "-an",
                    "-vf", f"setpts=PTS/{sp:.4f},fps=30,format=rgb24,lutrgb=r='clip(val*2.02,0,255)':g='clip(val*2.02,0,255)':b='clip(val*2.02,0,255)',"
                           f"scale=660:1434:flags=lanczos",
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "15",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",   # SDR now: drop the phone's HDR tags
                    os.path.join(ROOT, "assets", "video", f"{name}.mp4")], check=True)
    print(name, f"{sp:.2f}x")
