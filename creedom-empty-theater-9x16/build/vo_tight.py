"""v3: also used with VO_SRC (another take), VO_TEMPO=1 (no speed-up), VO_GAP and VO_NO_WORDS=1 (word times from build/vo_words.py).
v2 (owner: "it also feels slow, i want it to be around 28 seconds"): the owner's 42.6 s ElevenLabs take, tightened.
Every pause is cut to a breath (silencedetect -42 dB / 0.12 s, then 0.05 s kept; a little more after the hook and around
"And the crazy part?"), then the whole take is sped up with Rubber Band (pitch and formants kept) to land at ~27.5 s.
Word times in plan/words_take.json (the take) are mapped onto the new timeline -> plan/words.json.
python3 build/vo_tight.py"""
import json, os, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, os.environ.get("VO_SRC", os.path.join("assets", "audio", "vo_el.mp3")))
TEMPO = float(os.environ.get("VO_TEMPO", "1.38"))
GAP, PAD = float(os.environ.get("VO_GAP", ".05")), .03
KEEP = json.loads(os.environ.get("VO_KEEP", "{}")) if os.environ.get("VO_KEEP") else {4.85: .14, 28.67: .1, 29.97: .2}
KEEP = {float(k): v for k, v in KEEP.items()}          # take time of a pause start -> gap kept (s, before the speed-up)
SR = 48000
r = subprocess.run(["ffmpeg", "-i", SRC, "-af", "silencedetect=n=-42dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC], capture_output=True, text=True).stdout)
# speech islands between the pauses (the take starts with ~0.16 s of air)
cuts = sorted(zip(st, en))
isl, a = [], 0.14
for s, e in cuts:
    if min(s + PAD, dur) - a > .05:            # skip an empty island (a take that opens on silence)
        isl.append((a, min(s + PAD, dur)))
    a = max(e - PAD, 0)
if a < dur - .05:
    isl.append((a, dur))
gaps = []
for s, e in cuts[:len(isl) - 1]:
    g = next((v for k, v in KEEP.items() if abs(k - s) < .1), GAP)
    gaps.append(g)
# concatenated timeline
new, t = [], 0.0
for i, (a, b) in enumerate(isl):
    new.append((a, b, t))
    t += b - a + (gaps[i] if i < len(gaps) else 0)
total = t


def m(x):
    for a, b, n0 in new:
        if x <= b + 1e-6:
            return (n0 + max(0.0, x - a)) / TEMPO
    a, b, n0 = new[-1]
    return (n0 + (b - a)) / TEMPO


filt = ";".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={b - a - .012:.4f}:d=0.012,apad=pad_dur={gaps[i] if i < len(gaps) else 0:.3f}[s{i}]"
                for i, (a, b) in enumerate(isl))
filt += ";" + "".join(f"[s{i}]" for i in range(len(isl))) + f"concat=n={len(isl)}:v=0:a=1,{"rubberband=tempo=%s:pitchq=quality:formant=preserved," % TEMPO if TEMPO != 1 else ""}loudnorm=I=-16:TP=-2:LRA=11[o]"
out = os.path.join(ROOT, "assets", "audio", "vo.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-filter_complex", filt, "-map", "[o]", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", out], check=True)
if os.environ.get("VO_NO_WORDS"):
    print(f"{len(isl)} islands -> {total / TEMPO:.2f} s (word times: run build/vo_words.py)")
    raise SystemExit(0)
W = json.load(open(os.path.join(ROOT, "plan", "words_take.json")))
for w in W:
    w["t0"], w["t1"] = round(m(w["t0"]), 3), round(m(w["t1"]), 3)
json.dump(W, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
print(f"{len(isl)} islands, concat {total:.2f} s -> {d:.2f} s at {TEMPO}x; last word ends {W[-1]['t1']:.2f} s")
