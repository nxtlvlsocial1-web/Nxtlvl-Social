"""Voiceover: Kokoro (open source, Apache-2.0), voice am_michael at 1.1x, one take per script line, each placed on its
scene cue. Writes assets/audio/vo_raw.wav (audio.py levels it into vo.wav) and build/vo_timing.json (speech runs per line, from silence detection), which
generate.py turns into word-timed captions.

python3 -I build/vo.py <dir with kokoro-v1.0.onnx and voices-v1.0.bin>      (run from the project root)
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 30.0
SR = 24000
# (scene cue, slot end, what Kokoro reads, what the captions show)
LINES = [
    (0.0, 3.0, "This AI app went viral...", "This AI app went VIRAL..."),
    (3.0, 6.0, "then OpenAI killed it.", "...then OpenAI KILLED it."),
    (6.0, 11.0, "Every video you made cost them real G P U money. Every. Single. Time.",
     "Every video you made cost them real GPU money. Every. Single. Time."),
    (11.0, 16.0, "More users didn't mean more profit. It meant more loss.",
     "More users didn't mean more profit. It meant more LOSS."),
    (16.0, 21.0, "Because hype doesn't pay the bills.", "Because HYPE doesn't pay the BILLS."),
    (21.0, 26.0, "The real lesson? In A I, cheap beats cool.", "The real lesson? In AI, CHEAP beats COOL."),
    (26.0, 30.0, "Follow for the A I stories nobody explains.", "FOLLOW for the AI stories nobody explains."),
]
LEAD = 0.1


def runs(a, thr=0.012, gap=0.12):
    """Speech runs (start, end) in seconds: frames over a threshold, joined across gaps shorter than `gap`."""
    hop = int(0.01 * SR)
    env = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
    on = env > thr
    out, s = [], None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        if not v and s is not None:
            out.append([s, i]); s = None
    if s is not None:
        out.append([s, len(on)])
    merged = []
    for r in out:
        if merged and (r[0] - merged[-1][1]) * 0.01 < gap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [(r[0] * 0.01, r[1] * 0.01) for r in merged if (r[1] - r[0]) * 0.01 > 0.06]


def main():
    k = Kokoro(os.path.join(sys.argv[1], "kokoro-v1.0.onnx"), os.path.join(sys.argv[1], "voices-v1.0.bin"))
    track = np.zeros(int(DUR * SR), dtype=np.float32)
    timing = []
    for start, end, say, show in LINES:
        a, _ = k.create(say, voice="am_michael", speed=1.1, lang="en-us")
        idx = np.where(np.abs(a) > 0.01)[0]
        a = a[max(idx[0] - 240, 0): idx[-1] + 2400]
        assert len(a) / SR <= end - start - LEAD, (say, len(a) / SR)
        s = int((start + LEAD) * SR)
        track[s:s + len(a)] += a
        timing.append({"start": start, "end": end, "text": show,
                       "runs": [(round(start + LEAD + x, 3), round(start + LEAD + y, 3)) for x, y in runs(a)]})
        print(f"{start:5.1f}  {len(a) / SR:4.2f}s  {len(timing[-1]['runs'])} runs  {show}")
    track *= 0.89 / np.max(np.abs(track))
    sf.write(os.path.join(ROOT, "assets", "audio", "vo_raw.wav"), track, SR)
    with open(os.path.join(ROOT, "build", "vo_timing.json"), "w") as f:
        json.dump(timing, f, indent=1)


if __name__ == "__main__":
    main()
