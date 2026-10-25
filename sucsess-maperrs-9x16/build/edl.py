"""Edit decision list for the Sucsess Maperrs talking head: best takes, tightened pauses, one cut master.

python3 -I build/edl.py      (run from the project root; needs ffmpeg)

The raw take (assets/video/raw.mp4, 113.4 s) has two retakes: the "Introducing ..." line (27.2 s and again at 35.3 s)
and the "2 minute instant success scan" line (81.8 s and 85.9 s). The second take of each is kept. Speech runs come from
ffmpeg silencedetect (-36 dB, 0.22 s), stored in build/runs.json; each line below lists the runs it keeps. Inside a line,
pauses up to MERGE seconds stay natural; longer ones are cut down. Between lines the pause is tightened to a snappy beat.

Writes assets/video/talk.mp4 (1080x1920, 30 fps, keyframe every frame-second so seeks never freeze) and
build/edl.json: one entry per line with its text and its start/end on the cut timeline, plus the cut points.
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets", "video", "raw.mp4")
OUT = os.path.join(ROOT, "assets", "video", "talk.mp4")
RUNS = json.load(open(os.path.join(ROOT, "build", "runs.json")))
PRE, POST, MERGE = .08, .14, .42

# (run indices kept, English caption: a subtitle translation of the Hinglish line; the brand name is spelled exactly as
# the client spells it, Sucsess Maperrs)
LINES = [
    ([0], "You invest lakhs in your children's education."),
    ([1, 2], "But have you ever taken the time to discover their real strengths and interests?"),
    ([3], "A stream chosen by marks. A career chosen by family expectations."),
    ([4], "Does one formula really work for every student?"),
    ([5], "A career decision isn't just about what to become. It's about understanding which direction to grow in."),
    ([10, 11, 12, 13], "Introducing Sucsess Maperrs. Here you explore your personality, interests, aptitude and strengths."),
    ([14, 15, 16, 17], "You can also view Numerological and Cosmic Life Cycle insights as an optional, reflective perspective "
                       "that can help you see your journey from a new angle."),
    ([18], "These insights are not guaranteed predictions or career outcomes."),
    ([19, 20], "The goal isn't just to choose a career,"),
    ([21, 22, 23, 24, 25], "but to explore a better alignment between your strengths, possibilities and personal direction,"),
    ([26, 27], "so you can make informed career decisions and understand your chances of real satisfaction."),
    ([29], "So start with our 2-minute Instant Success Scan."),
    ([30], "And for deeper self-reflection, take the full Success Map Pro assessment, now 90% off, at only Rs. 2,300."),
    ([31, 32], "Don't leave your child's future to guesswork."),
    ([33, 34], "Sucsess Maperrs. First understand yourself, then choose your future."),
    ([35, 36], "Start your Instant Success Scan today. It's absolutely free."),
]
END = 113.36


def segments():
    """Source ranges to keep, in order, each tagged with its line."""
    segs = []
    for li, (idx, _) in enumerate(LINES):
        cur = None
        for k in idx:
            s, e = RUNS[k]
            s, e = max(0, s - PRE), min(END, e + POST)
            if cur and s - cur[1] <= MERGE - PRE - POST:
                cur[1] = e
            else:
                if cur:
                    segs.append(cur)
                cur = [s, e, li]
        segs.append(cur)
    return [(round(a, 3), round(b, 3), li) for a, b, li in segs]


def main():
    segs = segments()
    parts, labels = [], []
    for i, (a, b, _) in enumerate(segs):
        d = b - a
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}];"
                     f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,"
                     f"afade=t=out:st={d - .02:.3f}:d=0.02[a{i}];")
        labels.append(f"[v{i}][a{i}]")
    fc = "".join(parts) + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", RAW, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", "30", "-keyint_min", "30",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
    # cut timeline
    t, lines, cuts = 0.0, [], []
    for a, b, li in segs:
        if t > 0:
            cuts.append(round(t, 3))
        if not lines or lines[-1]["line"] != li:
            lines.append({"line": li, "text": LINES[li][1], "start": round(t, 3), "end": None, "src": []})
        lines[-1]["src"].append([a, b, round(t, 3)])
        t += b - a
        lines[-1]["end"] = round(t, 3)
    json.dump({"duration": round(t, 3), "cuts": cuts, "lines": lines}, open(os.path.join(ROOT, "build", "edl.json"), "w"), indent=1)
    print(f"{len(segs)} segments, {t:.2f} s (raw {END:.2f} s)")


if __name__ == "__main__":
    main()
