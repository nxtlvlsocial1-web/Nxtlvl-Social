"""Pick a take per message (faster-whisper: words right first, then the tighter take) and build assets/audio/vo.wav:
each clip's inner pauses cut to a breath (0.09 s; the dramatic ones kept a little longer), then the messages laid end to end
with the chat's gaps (past-her's replies wait for the typing dots). Writes plan/words.json (line = message id) and
plan/msgs.json (start / end of every message).   HF_HOME=/root/tts/hf /root/tts/.venv/bin/python build/vo_pick.py"""
import json, os, re, subprocess
import numpy as np
from faster_whisper import WhisperModel
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
LINES = json.load(open(os.path.join(ROOT, "plan", "lines.json")))
GAP_BEFORE = {"P": .14, "Q": .38}                    # past-her "types" before her reply lands
HOLD_AFTER = {"m4": .6}                            # the beat of silence after "I think I'm done."
INNER = {"m0": .22, "m4": .1}                       # inner pause kept per message (default .09)
m = WhisperModel("small.en", device="cpu", compute_type="int8")
norm = lambda s: [w for w in re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("forty-seven", "47").replace("okay", "ok")).split() if w]


def islands(path, keep):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "silencedetect=n=-40dB:d=0.1", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
    if len(en) < len(st):
        en.append(dur)
    isl, a = [], 0.0
    for s, e in zip(st, en):
        if s - a > .05:
            isl.append((max(0, a - .02), s + .03))
        a = e
    if dur - a > .05:
        isl.append((max(0, a - .02), dur))
    return isl, sum(b - a for a, b in isl) + keep * (len(isl) - 1)


def wav(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ar", "16000", "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


picks, pieces, t, words, msgs = {}, [], 0.0, [], []
work = os.path.join(ROOT, "assets", "audio", "work")
os.makedirs(work, exist_ok=True)
for L in LINES:
    lid, who = L["id"], L["who"]
    keep = INNER.get(lid, .09)
    best = None
    for k in (1, 2):
        p = os.path.join(ROOT, "assets", "audio", "el_lines", f"{lid}_{k}.mp3")
        segs, _ = m.transcribe(wav(p), beam_size=5)
        hyp = " ".join(s.text for s in segs)
        ref, h = norm(L["text"].replace("Creedom", "")), norm(hyp)
        miss = len([w for w in ref if w not in h])
        isl, length = islands(p, keep)
        cand = (miss, length, k, p, isl, hyp)
        if best is None or cand[:2] < best[:2]:
            best = cand
    miss, length, k, p, isl, hyp = best
    picks[lid] = {"take": k, "missing_words": miss, "length": round(length, 2), "heard": hyp.strip()}
    t += GAP_BEFORE[who] if lid != "m0" else 0.05
    # trim the clip to its speech islands joined by short breaths
    out = os.path.join(work, f"{lid}.wav")
    parts = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.006,afade=t=out:st={b - a - .01:.3f}:d=0.01,apad=pad_dur={keep if i < len(isl) - 1 else 0:.3f}[s{i}];" for i, (a, b) in enumerate(isl))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-filter_complex", parts + "".join(f"[s{i}]" for i in range(len(isl))) + f"concat=n={len(isl)}:v=0:a=1[o]",
                    "-map", "[o]", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", out], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    # word times inside the trimmed clip
    segs, _ = m.transcribe(wav(out), beam_size=5, word_timestamps=True)
    ws = [w for s in segs for w in s.words]
    for w in ws:
        words.append({"line": lid, "w": w.word.strip(), "t0": round(t + w.start, 3), "t1": round(t + w.end, 3)})
    msgs.append({"id": lid, "who": who, "text": L["text"], "t0": round(t, 3), "t1": round(t + d, 3)})
    pieces.append((t, out))
    t += d + HOLD_AFTER.get(lid, 0)
total = t
inputs, fc = [], []
for i, (t0, path) in enumerate(pieces):
    inputs += ["-i", path]
    ms = int(round(t0 * 1000))
    fc.append(f"[{i}:a]adelay={ms}|{ms}[d{i}]")
fc.append("".join(f"[d{i}]" for i in range(len(pieces))) + f"amix=inputs={len(pieces)}:normalize=0:duration=longest,apad=whole_dur={total + .05:.3f},loudnorm=I=-16:TP=-2:LRA=11[o]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[o]", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le",
                os.path.join(ROOT, "assets", "audio", "vo.wav")], check=True)
json.dump(words, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
json.dump(msgs, open(os.path.join(ROOT, "plan", "msgs.json"), "w"), indent=1)
json.dump(picks, open(os.path.join(ROOT, "plan", "vo_pick.json"), "w"), indent=1)
for lid, v in picks.items():
    print(lid, v)
print(f"voice track {total:.2f} s")
