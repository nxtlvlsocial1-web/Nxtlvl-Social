"""Tighten pauses in the raw ElevenLabs take, speed it up, and remap word timings.

Usage: python3 -I tools/process_vo.py   (run from the project root)
Writes assets/audio/vo.wav and tools/vo_words.json.
"""
import json, re, subprocess, sys
import numpy as np

SR = 48000
TEMPO = 1.2
SRC = "assets/raw/vo_a.mp3"
TRIM_TO = 0.14          # default length a long pause is cut down to (pre-tempo)
KEEP = {38.0: 0.34}     # pauses (by start, rounded) that keep a dramatic beat


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def silences(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "silencedetect=n=-38dB:d=0.18", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    e = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return list(zip(s, e))


audio = decode(SRC)
dur = len(audio) / SR
pauses = silences(SRC)

# Build kept segments [(src_start, src_end)] and a piecewise map src -> out.
keep, cursor = [], 0.0
for s, e in pauses:
    target = TRIM_TO
    for k, v in KEEP.items():
        if abs(s - k) < 0.6:
            target = v
    if e - s <= target:
        continue
    # keep half the target on each side of the pause
    keep.append((cursor, s + target / 2))
    cursor = e - target / 2
keep.append((cursor, dur))

pieces, out_map, t_out = [], [], 0.0
fade = int(0.008 * SR)
for a, b in keep:
    seg = audio[int(a * SR):int(b * SR)].copy()
    if len(seg) > 2 * fade:
        ramp = np.linspace(0, 1, fade, dtype=np.float32)
        seg[:fade] *= ramp
        seg[-fade:] *= ramp[::-1]
    out_map.append((a, b, t_out))
    pieces.append(seg)
    t_out += (b - a)
tight = np.concatenate(pieces)


def remap(t):
    for a, b, o in out_map:
        if t <= b:
            return (o + max(0.0, t - a)) / TEMPO
    a, b, o = out_map[-1]
    return (o + (t - a)) / TEMPO


subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-af", f"atempo={TEMPO},highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
                       "loudnorm=I=-16:TP=-1.5:LRA=7",
                "-ar", str(SR), "assets/audio/vo.wav"], input=tight.tobytes(), check=True)

words = json.load(open("tools/vo_words_raw.json"))
out = [{"text": w, "start": round(remap(s), 3), "end": round(remap(e), 3)} for w, s, e in words]
json.dump(out, open("tools/vo_words.json", "w"), indent=0)
print(f"raw {dur:.2f}s -> tightened {len(tight)/SR:.2f}s -> final {len(tight)/SR/TEMPO:.2f}s")
for w in out:
    print(f"{w['start']:6.2f} {w['end']:6.2f} {w['text']}")
