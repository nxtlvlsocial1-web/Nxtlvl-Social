"""The owner's Canva Image-to-Video clips, cut to their lyric and turned into 1990s TV anime.

python3 build/clips90.py      (from the project root; needs ffmpeg)

Sources (kept out of git): assets/video/anime/<name>_src.mp4, 1440x1440, 30 fps, 5 s, exported from the owner's Canva
designs (plan/anime.json). For each clip: start partway in and retime it so its best moment (the smirk, the smile,
the spin) lands inside the scene; drop the motion to 8 drawings a second (90s anime is drawn on threes, so the
smooth in-between motion that reads as AI goes); soften it like a 480-line broadcast; bleed the colour sideways;
fade and warm the colour; a soft vignette; then back to the edit's 20 fps with live film grain on every frame.
Writes assets/video/anime/<name>.mp4 (1080x1080, 20 fps, silent).
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "assets", "video", "anime")
# name: (start in the source s, playback rate, length in the edit s); lengths cover the scene plus its 6-frame tail
CLIPS = {
    "jealous": (1.2, 1.0, 3.3),        # 2.9-6.2: the side-eye, the smirk at the end
    "road": (1.3, 2.0, 1.5),           # 28.1-29.6: she leans in
    "her_blush": (0.0, .86, 5.45),     # 29.7-35.15: the whole glance back and smile, slowed a touch
    "him_smitten": (2.3, 1.0, 2.3),    # 32.85-35.15: the shy smile
    "fire": (.6, 2.0, 1.85),           # 42.5-44.35: the walk out of the fire
    "spin": (0.0, .84, 5.55),          # 44.35-49.9: the whole spin
}
TAIL = .35


def main():
    for name, (ms, rate, dur) in CLIPS.items():
        src = os.path.join(V, f"{name}_src.mp4")
        if not os.path.exists(src):
            print(name, "no source, skipped")
            continue
        d = dur + TAIL
        vf = (f"trim=start={ms},setpts=(PTS-STARTPTS)/{rate},fps=8,"
              "scale=720:720:flags=bilinear,scale=1080:1080:flags=bicubic,"
              "chromashift=cbh=-3:crh=3,"
              "eq=saturation=0.94:contrast=1.05:brightness=0.015,"
              "curves=r='0/0.05 1/1':g='0/0.03 1/0.97':b='0/0.03 1/0.9',"
              "vignette=angle=PI/8,"
              f"fps=20,noise=alls=9:allf=t,trim=duration={d:.2f},setpts=PTS-STARTPTS")
        out = os.path.join(V, f"{name}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-preset", "slow",
                        "-crf", "16", "-pix_fmt", "yuv420p", "-r", "20", out], check=True)
        print(name, f"{d:.2f}s")


if __name__ == "__main__":
    main()
