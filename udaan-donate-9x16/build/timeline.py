"""Places the VO segments (assets/audio/vo/sNN.wav) on one track with set gaps.
s07 is split at the pause before "उड़ान" (vo_src/s07.wav -> s07a/s07b) for a beat before the reveal.
Writes assets/audio/voice.wav and plan/timings.json ({id: [start, end]}).  python3 build/timeline.py"""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = 0.30
# gap AFTER each segment (s)
GAPS = {"s01": .25, "s02": .65, "s03": .75, "s04": .55, "s05": .65, "s06": 1.0, "s07a": .55, "s07b": .9,
        "s08": .4, "s09": .4, "s10": .55, "s11": .55, "s12": .5, "s13": .35, "s14": 0}
TOTAL = 66.5
ids = sorted(GAPS)
def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
t, tim, inputs, filt = START, {}, [], []
for k, i in enumerate(ids):
    p = os.path.join(ROOT, "assets/audio/vo", i + ".wav")
    d = dur(p)
    tim[i] = [round(t, 3), round(t + d, 3)]
    inputs += ["-i", p]
    filt.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=mono,adelay={int(t*1000)}[a{k}]")
    t += d + GAPS[i]
filt.append("".join(f"[a{k}]" for k in range(len(ids))) + f"amix=inputs={len(ids)}:normalize=0,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]",
                os.path.join(ROOT, "assets/audio/voice.wav")], check=True)
json.dump(tim, open(os.path.join(ROOT, "plan/timings.json"), "w"), indent=1)
print(json.dumps(tim))
