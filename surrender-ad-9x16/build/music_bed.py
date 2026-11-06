"""Music bed (owner: "use this music from timestamp 0:46"). From 0:46 the track has 106.8 s left and the edit runs
about 139 s, so it loops on downbeats inside its full-energy part (86.3 BPM, a bar is 2.78 s; the splice pair with the
v4: back to the 0:46 start each time). Pieces join with 80 ms crossfades. Writes assets/audio/music_bed.wav.
python3 build/music_bed.py [length_s]
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "audio", "music_full.wav")
LEN = float(sys.argv[1]) if len(sys.argv) > 1 else 140.0
# v4 (owner: "loop the music from where it started"): the bed runs from 0:46 to the last full-energy downbeat before
# the track's quiet outro (2:12.12), then starts again from 0:46
A, LOOP_IN, LOOP_OUT = 45.95, 45.95, 132.12
pieces, have = [(A, LOOP_OUT)], LOOP_OUT - A
while have < LEN:
    take = min(LOOP_OUT - LOOP_IN, LEN - have + .1)
    pieces.append((LOOP_IN, LOOP_IN + take))
    have += take
fc = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[p{k}];" for k, (a, b) in enumerate(pieces))
cur = "p0"
for k in range(1, len(pieces)):
    fc += f"[{cur}][p{k}]acrossfade=d=0.08:c1=tri:c2=tri[x{k}];"
    cur = f"x{k}"
fc += f"[{cur}]atrim=0:{LEN},afade=t=out:st={LEN - 1.2}:d=1.2[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[o]", "-ar", "48000",
                os.path.join(ROOT, "assets", "audio", "music_bed.wav")], check=True)
print("pieces", pieces)
