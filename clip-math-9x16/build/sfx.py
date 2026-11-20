"""Sound design for the Clip Math reel: whooshes, ticks and impacts, pre-mixed into one 40 s track.

python3 build/sfx.py      (from the project root; needs numpy and ffmpeg)

Sources: assets/sfx/*.mp3, copied from HyperFrames' bundled library (Pixabay Content License: free for commercial use,
no attribution required; see assets/sfx/CREDITS.md). No music, no voice. The cue times below match the animation
times in index.html: change both together. Writes assets/audio/sfx.wav (48 kHz stereo, peak -3 dBFS).
"""
import os
import subprocess
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
DUR = 40.0
N = int(DUR * SR)

# (time s, file, gain)
CUES = [
    # 1 hook: counter ticks, then the slam
    *[(t, "key-press", 0.35) for t in (0.30, 0.62, 0.92, 1.18, 1.40, 1.58, 1.74, 1.86)],
    (1.95, "impact-bass-1", 0.95),
    # 2 not $1,000: slam in, strike
    (2.98, "whoosh-short", 0.55), (3.52, "whoosh", 0.55), (3.57, "click", 0.6),
    # 3 wipe, receipt slides in, lines print, total pops
    (4.82, "whoosh", 0.7), (5.30, "whoosh-short", 0.45),
    *[(5.75 + i * 0.2, "key-press", 0.5) for i in range(4)], (6.55, "pop", 0.6),
    # 4 wipe up, $1 slam, chart, 50K ticks
    (6.82, "whoosh", 0.7), (7.12, "impact-bass-1", 0.45), (7.66, "click-soft", 0.6),
    *[(t, "click", 0.4) for t in (8.7, 9.4, 10.1, 10.8)],
    # 5 headline swap, ceiling slams, the hit, +$0 ticks
    (11.0, "whoosh-short", 0.45), (11.15, "impact-bass-1", 0.6), (12.2, "impact-bass-1", 0.9),
    *[(t, "click-soft", 0.55) for t in (12.75, 13.45, 14.15)],
    # 6 headline swap, blade, $225 lands
    (15.0, "whoosh-short", 0.45), (15.32, "whoosh", 0.65), (16.1, "pop", 0.6), (16.1, "impact-bass-1", 0.35),
    # 7 wipe, track draws, 250K marker, $0 slam
    (17.82, "whoosh", 0.7), (18.4, "click-soft", 0.5), (19.4, "key-press", 0.6), (19.42, "pop", 0.5),
    (20.0, "impact-bass-1", 0.8),
    # 8 hard cut to the pink frame, three words fly in, exit
    (21.0, "impact-bass-1", 0.55), *[(21.05 + i * 0.35, "whoosh-short", 0.45) for i in range(3)], (22.8, "whoosh", 0.55),
    # 9 five cards pop and count
    *[(23.6 + i * 0.75, "pop", 0.55) for i in range(5)], *[(24.22 + i * 0.75, "key-press", 0.45) for i in range(5)],
    # 10 stack, total, fee chip, $900, split, 4x stamp
    (28.1, "whoosh", 0.55), (28.62, "pop", 0.5), (29.1, "click", 0.6), (29.9, "impact-bass-1", 0.7),
    (30.3, "whoosh-short", 0.5), (31.0, "impact-bass-1", 1.0),
    # 11 the viral card shrinks, the five come back
    (32.0, "whoosh-short", 0.45), (32.25, "whoosh", 0.5), *[(32.7 + i * 0.05, "pop", 0.22) for i in range(5)],
    # 12 hazard wipe, warning card, icon pulses
    (33.82, "whoosh", 0.7), (34.1, "impact-bass-1", 0.6), (35.0, "error", 0.3), (36.0, "click-soft", 0.5),
    # 13 comment box, typing, send, loop-out
    (37.05, "whoosh-short", 0.5), *[(t, "key-press", 0.7) for t in (37.3, 37.42, 37.54, 37.66)],
    (38.35, "click", 0.75), (38.5, "whoosh-short", 0.5), (39.68, "whoosh-short", 0.5),
]


def load(name):
    path = os.path.join(ROOT, "assets", "sfx", name + ".mp3")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64).reshape(-1, 2)


def main():
    cache, bus = {}, np.zeros((N, 2))
    for t, name, g in CUES:
        x = cache.setdefault(name, load(name))
        i = int(round(t * SR))
        x = x[: max(0, N - i)]
        bus[i:i + len(x)] += x * g
    tail = int(0.03 * SR)                        # tiny fade at both ends so the loop point never clicks
    bus[:tail] *= np.linspace(0, 1, tail)[:, None]
    bus[-tail:] *= np.linspace(1, 0, tail)[:, None]
    bus *= 0.708 / max(1e-9, np.abs(bus).max())  # peak -3 dBFS
    pcm = (bus * 32767).astype("<i2")
    out = os.path.join(ROOT, "assets", "audio", "sfx.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print("wrote", out, f"({len(CUES)} cues)")


if __name__ == "__main__":
    main()
