"""Apoorva AI true-or-false quiz: the A-roll edit (talking head) from the two phone takes.

Take 1 = IMG_0764 (wider frame, has "False, TSMC does." and the live flip "True. Sorry, false, false.")
Take 2 = IMG_0765 (closer frame, clean answers). Plan agreed with the owner: hook + Q1 + Q2 from take 1 (Q2 keeps her
flip), Q3-Q6 from take 2, the repeated boss question cut, Q6 left as an audience poll ("Audience poll, comment.").
Every question gets a 1.2 s lock-in on her stare before the reveal: her real silent pause, topped up with a held frame
when the pause is shorter. Take 1 is punched in to match take 2's framing. The voice is cleaned (high-pass, denoise,
gentle compression, -16 LUFS).

Writes assets/video/aroll.mp4 (1080x1920, 30 fps, voice) and plan/events.json (every beat in reel time).
python3 build/edit.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = {1: os.path.join(ROOT, "assets", "video", "take1.mp4"), 2: os.path.join(ROOT, "assets", "video", "take2.mp4")}
LOCK = 1.2
# per-take framing: take 1 is shot wider, so it is scaled up and cropped (centre x, face kept in the upper half)
FRAME = {1: (1.34, 0.30), 2: (1.0, 0.5)}

# (label, take, start, end, hold) : hold = seconds of frozen last frame added after the piece (silent)
# kinds: hook / q (question) / lock (her silent stare) / a (answer) / cta
PIECES = [
    ("hook",  1, 3.00, 4.98, 0.0),
    ("q1",    1, 5.30, 6.80, 0.0),
    ("lock1", 1, 6.80, 8.00, 0.0),
    ("a1",    1, 8.62, 10.15, 0.0),
    ("q2",    1, 10.55, 13.12, 0.0),
    ("lock2", 1, 13.12, 14.12, 0.20),
    ("a2a",   1, 14.12, 15.98, 0.0),     # "Same answer every time."
    ("a2b",   1, 16.84, 17.38, 0.0),     # "True."
    ("a2c",   1, 17.78, 19.26, 0.0),     # "Sorry, false, false."
    ("q3",    2, 22.10, 24.46, 0.0),
    ("lock3", 2, 24.46, 25.34, 0.32),
    ("a3",    2, 25.34, 26.60, 0.0),
    ("q4",    2, 27.32, 28.86, 0.0),
    ("lock4", 2, 28.86, 30.06, 0.0),
    ("a4",    2, 30.18, 31.70, 0.0),
    ("q5",    2, 32.06, 35.08, 0.0),
    ("lock5", 2, 35.08, 35.46, 0.82),
    ("a5",    2, 35.46, 36.50, 0.0),
    ("q6",    2, 36.66, 39.64, 0.0),
    ("lock6", 2, 39.64, 40.40, 0.44),
    ("cta",   2, 47.74, 50.05, 1.30),
]


def words(take):
    f = {1: "IMG_0764", 2: "IMG_0765"}[take]
    return [(w[0].strip(), w[1], w[2]) for s in json.load(open(os.path.join(ROOT, "plan", f + "_words.json"))) for w in s["w"]]


def main():
    W = {1: words(1), 2: words(2)}
    fc, vl, al, t, ev = [], [], [], 0.0, []
    for i, (lab, tk, a, b, hold) in enumerate(PIECES):
        z, fy = FRAME[tk]
        w, h = int(1080 * z) // 2 * 2, int(1920 * z) // 2 * 2
        y0 = int((h - 1920) * fy)
        x0 = (w - 1080) // 2
        v = f"[{tk - 1}:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={w}:{h},crop=1080:1920:{x0}:{y0},fps=30"
        if hold:
            v += f",tpad=stop_mode=clone:stop_duration={hold}"
        fc.append(v + f",setsar=1[v{i}]")
        aa = f"[{tk - 1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.03:.3f}:d=0.03"
        if hold:
            aa += f",apad=pad_dur={hold}"
        fc.append(aa + f",aresample=48000[a{i}]")
        vl.append(f"[v{i}]")
        al.append(f"[a{i}]")
        dur = b - a + hold
        ws = [{"w": x, "t0": round(t + s0 - a, 3), "t1": round(t + s1 - a, 3)} for x, s0, s1 in W[tk] if s0 >= a - .05 and s1 <= b + .05]
        ev.append({"label": lab, "take": tk, "t0": round(t, 3), "t1": round(t + dur, 3), "src": [a, b], "hold": hold, "words": ws})
        t += dur
    fc.append("".join(f"{vl[i]}{al[i]}" for i in range(len(PIECES))) + f"concat=n={len(PIECES)}:v=1:a=1[vv][ar]")
    fc.append("[ar]highpass=f=90,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90:makeup=1.6,loudnorm=I=-16:TP=-2:LRA=9[aa]")
    script = os.path.join(ROOT, "cache", "edit_graph.txt")
    os.makedirs(os.path.dirname(script), exist_ok=True)
    open(script, "w").write(";\n".join(fc))
    out = os.path.join(ROOT, "assets", "video", "aroll.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", V[1], "-i", V[2], "-filter_complex_script", script, "-map", "[vv]", "-map", "[aa]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000",
                    out.replace(".mp4", ".mov")], check=True)
    # HyperFrames plays the picture; the voice goes to the mix as wav
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out.replace(".mp4", ".mov"), "-an", "-c:v", "copy", out], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out.replace(".mp4", ".mov"), "-vn", "-c:a", "pcm_s16le",
                    os.path.join(ROOT, "assets", "audio", "voice.wav")], check=True)
    os.remove(out.replace(".mp4", ".mov"))
    json.dump({"dur": round(t, 3), "pieces": ev}, open(os.path.join(ROOT, "plan", "events.json"), "w"), indent=1)
    print(f"aroll {t:.2f} s, {len(PIECES)} pieces")


if __name__ == "__main__":
    main()
