"""Music bed (owner: "use this music from timestamp 0:46"). From 0:46 the track has 106.8 s left and the edit runs
about 139 s, so it loops on downbeats inside its full-energy part (86.3 BPM, a bar is 2.78 s; the splice pair with the
closest spectral match, 2:03.78 -> 1:19.32, 16 bars). Pieces join with 40 ms crossfades. Writes assets/audio/music_bed.wav.
python3 build/music_bed.py [length_s]
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "audio", "music_full.wav")
LEN = float(sys.argv[1]) if len(sys.argv) > 1 else 140.0
A, LOOP_IN, LOOP_OUT = 45.95, 79.32, 123.78
pieces, have = [(A, LOOP_OUT)], LOOP_OUT - A
while have < LEN:
    take = min(LOOP_OUT - LOOP_IN, LEN - have + .1)
    pieces.append((LOOP_IN, LOOP_IN + take))
    have += take
fc = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[p{k}];" for k, (a, b) in enumerate(pieces))
cur = "p0"
for k in range(1, len(pieces)):
    fc += f"[{cur}][p{k}]acrossfade=d=0.04:c1=tri:c2=tri[x{k}];"
    cur = f"x{k}"
fc += f"[{cur}]atrim=0:{LEN},afade=t=out:st={LEN - 1.2}:d=1.2[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[o]", "-ar", "48000",
                os.path.join(ROOT, "assets", "audio", "music_bed.wav")], check=True)
print("pieces", pieces)
