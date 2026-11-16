#!/usr/bin/env python3
"""Join per-line Kokoro takes into one narration track with authored pauses.

Usage: python3 assemble-vo.py <takes_dir> <project_dir>
Reads  <takes_dir>/lNN.wav (one per line of audio/vo-lines.txt)
Writes <project_dir>/audio/vo.wav and <project_dir>/audio/vo-lines.json
"""
import json
import subprocess
import sys
from pathlib import Path

takes = Path(sys.argv[1])
proj = Path(sys.argv[2])
lines = [l for l in (proj / "audio" / "vo-lines.txt").read_text().splitlines() if l.strip()]

LEAD_IN = 0.3
DEFAULT_GAP = 0.16
GAP_AFTER = {    # line number -> pause after it (seconds)
    1: 0.5, 2: 0.45, 3: 0.9, 4: 0.6, 5: 0.55, 6: 1.2, 7: 1.6, 8: 0.6, 9: 0.5, 10: 0.6, 11: 0.5, 12: 0.6, 13: 0.7, 14: 0.5, 15: 0.5, 16: 0.9, 17: 0.6, 18: 0.5, 19: 0.6, 20: 0.5, 21: 0.6, 22: 0.9, 23: 0.6, 24: 0.6, 25: 1.4, 26: 0.6, 27: 0.6, 28: 0.7, 29: 0.6, 30: 0.6, 31: 0.8, 32: 1.2, 33: 0.5, 34: 1.3, 35: 1.6, 36: 0.7, 37: 0.6, 38: 0.6, 39: 0.6, 40: 0.5, 41: 0.5, 42: 0.6, 43: 0.6, 44: 0.8, 45: 0.6, 46: 0.6, 47: 0.6, 48: 0.9, 49: 0.8, 50: 0.8, 51: 0.6, 52: 0.6, 53: 1.0, 54: 0.6, 55: 0.8, 56: 0.7, 57: 0.6,
}
TAIL = 14.0      # end screen after the last line
SR = 24000

work = takes / "trimmed"
work.mkdir(exist_ok=True)


def dur(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", str(p)])
    return float(out)


# trim leading/trailing silence of each take, keep a hair of tail so words don't clip
trim = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,"
        "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.06,areverse")
pieces, meta, t = [], [], LEAD_IN


def silence(seconds, name):
    path = work / name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono",
                    "-t", f"{seconds:.3f}", str(path)], check=True)
    return path


pieces.append(silence(LEAD_IN, "lead.wav"))
for i, text in enumerate(lines, start=1):
    src = takes / f"l{i:02d}.wav"
    dst = work / f"t{i:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", trim, "-ar", str(SR), "-ac", "1",
                    str(dst)], check=True)
    d = dur(dst)
    meta.append({"line": i, "text": text, "start": round(t, 3), "end": round(t + d, 3)})
    pieces.append(dst)
    t += d
    gap = TAIL if i == len(lines) else GAP_AFTER.get(i, DEFAULT_GAP)
    pieces.append(silence(gap, f"g{i:02d}.wav"))
    t += gap

listfile = work / "list.txt"
listfile.write_text("".join(f"file '{p}'\n" for p in pieces))
out = proj / "audio" / "vo.wav"
raw = work / "joined.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
                "-ar", "48000", "-ac", "1", str(raw)], check=True)
# social-video loudness for the narration: -16 LUFS integrated, -1.5 dBTP
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", "48000", "-ac", "1", str(out)], check=True)
(proj / "audio" / "vo-lines.json").write_text(json.dumps({"duration": round(dur(out), 3), "lines": meta},
                                                         indent=1))
print(f"vo.wav {dur(out):.2f}s, {len(meta)} lines")
