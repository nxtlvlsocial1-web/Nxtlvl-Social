"""SST "The Journey Continues": cut, crop and grade every shot of plan/edl.json from the Pexels sources (footage/pexels)
into assets/video/<id>.mp4 at the band size (1080x1160), with a handle at the end for the dissolves. One look per beat:
night (deep navy, low saturation), dark (colder, darker: the challenge), turn (navy easing toward balanced), warm and dawn
(balanced, a little warmth: moving forward). Keyframe every 10 frames for clean seeks.
python3 build/prep_shots.py
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "plan", "edl.json")))
BW, BH = E["band"]
GRADE = {
    "night": "eq=contrast=1.08:saturation=0.62:brightness=-0.02:gamma=0.97,colorbalance=rs=-0.05:gs=-0.01:bs=0.09:rm=-0.03:bm=0.05:rh=0.01:bh=0.0",
    "dark": "eq=contrast=1.12:saturation=0.5:brightness=-0.05:gamma=0.93,colorbalance=rs=-0.07:gs=-0.02:bs=0.12:rm=-0.04:bm=0.07:bh=0.02",
    "turn": "eq=contrast=1.06:saturation=0.68:brightness=-0.01,colorbalance=rs=-0.03:bs=0.06:rm=-0.01:bm=0.03:rh=0.02",
    "warm": "eq=contrast=1.05:saturation=0.82:brightness=0.0,colorbalance=rs=-0.01:bs=0.04:rh=0.03:bh=-0.02",
    "dawn": "eq=contrast=1.05:saturation=0.85:brightness=0.0,colorbalance=rs=-0.02:bs=0.05:rh=0.02",
}


def probe(p):
    w, h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", p],
                          capture_output=True, text=True).stdout.strip().split(",")[:2]
    return int(w), int(h)


def main():
    os.makedirs(os.path.join(ROOT, "assets", "video"), exist_ok=True)
    only = set(sys.argv[1:])
    for s in E["shots"]:
        if only and s["id"] not in only:
            continue
        src = os.path.join(ROOT, "footage", "pexels", s["src"] + ".mp4")
        out = os.path.join(ROOT, "assets", "video", s["id"] + ".mp4")
        w, h = probe(src)
        # scale so the band is covered, then crop around the focus (x for wide sources, y for tall ones)
        if w / h > BW / BH:
            sw, sh = round(w * BH / h / 2) * 2, BH
            crop = f"crop={BW}:{BH}:{int(max(0, min(sw - BW, s['focus'] * sw - BW / 2)))}:0"
        else:
            sw, sh = BW, round(h * BW / w / 2) * 2
            crop = f"crop={BW}:{BH}:0:{int(max(0, min(sh - BH, s['focus'] * sh - BH / 2)))}"
        vf = f"scale={sw}:{sh}:flags=lanczos,{crop},{GRADE[s['grade']]}" + (("," + s["extra"]) if s.get("extra") else "") + ",fps=30,format=yuv420p"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["in"]), "-i", src, "-t", str(round(s["d"] + E["handle"], 2)), "-an",
                        "-vf", vf, "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-g", "10", "-movflags", "+faststart", out], check=True)
        print(s["id"], s["src"], f"{w}x{h}", "->", out, flush=True)


if __name__ == "__main__":
    main()
