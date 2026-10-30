"""The music-video layer of the collage edit: the Ashke video cut to the song's beat, photocopied in black and white.

python3 build/footage.py      (from the project root; needs ffmpeg, plan/beats_raw.json)

The song section is 2:14 to 3:14; there the music video runs 0.40 s behind the audio, so "sync" shots show
MV time = edit time + 134.40 and keep the lip-sync. Cutaways come from the rest of the video (the estate, the tea
party, the Aston Martins, polo). The picture is cropped out of its 2:1 letterbox, upscaled and turned into a high-
contrast photocopy (grey, auto-levelled per shot so dark rooms keep detail, hard curve, crisp sharpening, a fixed fine
grain) stepped to 15 fps like stop-motion (every frame held twice). Cuts land on every half beat, quarter beats in the
bursts and whole beats in the breathers. Writes assets/video/bw_main.mp4 (1920x1080, 30 fps), plan/shots.json (the cut list the
collage layout follows) and assets/img/stills/*.jpg (photocopied stills for the secondary collage cards).
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "video", "music-video-src.mp4")
SECTION_START, DUR, MV_OFFSET = 134.0, 60.0, 0.40
B = json.load(open(os.path.join(ROOT, "plan", "beats_raw.json")))
BEAT0, PERIOD = B["beats"][0], 60 / B["bpm"]
LOOK = ("crop=568:320:36:20,scale=1920:1080:flags=lanczos,setsar=1,format=gray,normalize=smoothing=20:independence=0,"
        "eq=contrast=1.75:brightness=0.04:gamma=1.12,unsharp=5:5:1.9:5:5:0,unsharp=3:3:0.6,noise=alls=4:allf=u")

# cutaways (MV start, end): Karan at the tea party, by the Aston Martins, polo, the manor; no subtitled dialogue
CUT = {"car_a": (71.5, 75.0), "car_b": (75.2, 77.2), "car_c": (78.8, 80.1), "car_d": (82.7, 85.3), "tea_e": (68.9, 71.3),
       "tea_c": (65.3, 66.6), "tea_a": (59.8, 61.5), "tea_f": (77.4, 78.6), "polo_close": (61.7, 62.7), "polo_wide": (56.1, 59.6),
       "manor": (7.6, 10.4), "group": (107.2, 109.5), "tea_g": (80.3, 81.3), "polo_b": (62.9, 64.2)}
ORDER = ["sync", "car_a", "sync", "sync", "tea_e", "sync", "polo_close", "sync", "car_d", "sync", "sync", "tea_c", "sync", "car_c",
         "sync", "car_b", "sync", "sync", "tea_a", "sync", "polo_wide", "sync", "car_c", "sync", "sync", "group", "sync", "tea_f",
         "sync", "car_a", "sync", "sync", "polo_b", "sync", "tea_g", "sync", "car_d", "sync"]


def cut_times():
    ts, k = [], 1
    while True:
        t = BEAT0 + k * PERIOD
        if t > 59.4:
            break
        ts.append(round(t, 3))
        if t < 1.9 or 36.0 <= t < 37.8 or 57.0 <= t:
            k += 1                     # breathers: the intro, "daaka", the finale
        elif 14.3 <= t < 16.3 or 44.8 <= t < 46.3 or 48.5 <= t < 50.0:
            k += .25                   # bursts: 5-frame cuts
        else:
            k += .5
    return ts


def plan():
    edges = [0.0] + cut_times() + [DUR]
    shots, used = [], {}
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        src = ORDER[i % len(ORDER)]
        if src == "sync":
            ms = a + SECTION_START + MV_OFFSET
        else:
            s0, s1 = CUT[src]
            off = used.get(src, 0.0)
            if s0 + off + (b - a) > s1:
                off = 0.0
            ms = s0 + off
            used[src] = off + (b - a)
        shots.append({"a": round(a, 3), "b": round(b, 3), "src": src, "media": round(ms, 3)})
    return shots


def build(shots):
    lst = os.path.join(ROOT, "cache", "bw_parts")
    os.makedirs(lst, exist_ok=True)
    parts = []
    for i, s in enumerate(shots):
        out = os.path.join(lst, f"p{i:03d}.mp4")
        n = round(s["b"] * 30) - round(s["a"] * 30)      # frame counts from absolute times: no drift, cuts stay on the beat
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['media']:.3f}", "-i", SRC, "-vf", f"{LOOK},fps=15,fps=30", "-frames:v", str(n),
                        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "15", "-pix_fmt", "yuv420p", out], check=True)
        parts.append(out)
    with open(os.path.join(lst, "list.txt"), "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(lst, "list.txt"), "-c", "copy",
                    os.path.join(ROOT, "assets", "video", "bw_main.mp4")], check=True)
    # photocopied stills for the secondary cards
    sd = os.path.join(ROOT, "assets", "img", "stills")
    os.makedirs(sd, exist_ok=True)
    picks = [72.5, 76.0, 83.5, 70.0, 60.5, 58.0, 9.0, 108.0, 140.5, 144.0, 152.0, 161.5, 163.0, 167.5, 172.0, 176.5, 178.0, 186.0, 190.0, 196.5]
    for k, t in enumerate(picks):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", SRC, "-frames:v", "1", "-vf", LOOK.replace(",noise=alls=4:allf=u", ""),
                        "-q:v", "3", os.path.join(sd, f"s{k:02d}.jpg")], check=True)


if __name__ == "__main__":
    shots = plan()
    json.dump(shots, open(os.path.join(ROOT, "plan", "shots.json"), "w"), indent=0)
    print(len(shots), "shots")
    build(shots)
    print("wrote assets/video/bw_main.mp4, plan/shots.json, assets/img/stills/")
