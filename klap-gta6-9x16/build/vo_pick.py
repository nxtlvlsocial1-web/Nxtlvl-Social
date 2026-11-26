"""AI.NXTLVL first-customers reel (copied from prism-dl-9x16): pick the voiceover takes and join them (after build/vo.py); copied from the reel-flop project.

For every line, both takes are transcribed locally with faster-whisper (small.en, MIT; word timestamps) and scored:
  1. words wrong against the script (any slip loses);
  2. then the more expressive take: wider pitch range (5-95 % F0 spread, pyin), the "emotion in every word" ask.
The chosen takes are trimmed to their speech (+ a short tail), joined with a pause set by the arc beat after each line,
normalised, and written to assets/audio/vo.wav. Word times (absolute, from Whisper on the chosen takes, with the
script's spelling) go to plan/words.json for the word-on-speech type; plan/vo_pick.json logs the scores.

/root/tts/.venv/bin/python build/vo_pick.py      (HF_HOME=/root/tts/hf)
"""
import json
import os
import re
import subprocess

import librosa
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAKES = os.path.join(ROOT, os.environ.get("VO_TAKES", os.path.join("assets", "audio", "vo_takes")))
TAG = os.environ.get("VO_TAG", "")   # v2: one pick per reference voice (vo_<tag>.wav, words_<tag>.json)
SR = 48000
TEMPO = float(os.environ.get("VO_TEMPO", "1.0"))
GAP_SCALE = 1.0
LEAD = .04          # silence before the first word of the reel (v3: the cold open hits at once)
# pause after each line (s): peaks get room to land, the list moves fast
GAP = {"g1": .24, "g2": .3, "g3": .28, "g4": .4, "g5": .22, "g6": .3, "g7": .36, "g8": .0}


NUM = {"eleven": "11", "ten": "10", "two": "2", "hundred": "100", "thousand": "000", "one": "1", "six": "6", "nineteenth": "19th", "fortysix": "46", "one": "1", "two": "2", "three": "3", "twenty": "20", "1": "one", "3": "three"}


def norm(w):
    w = re.sub(r"[^a-z0-9]", "", w.lower())
    return NUM.get(w, w)


def spoken(text):
    """Whisper writes numbers and names its own way ("GTA6", "8 -hour", "10"): compare in spoken words"""
    t = re.sub(r"(?i)gta\s*6|gta\s*six", "gta six", text)
    t = re.sub(r"(?i)\bmr\.?\s*beast", "mrbeast", t)
    t = re.sub(r"(?i)\bi\s*show\s*speed", "ishowspeed", t)
    t = re.sub(r"(?i)\$1\b", "a dollar", t)
    t = re.sub(r"(?i)\b1,?000\b", "thousand", t)
    t = re.sub(r"(?i)\bclap\b|\bklapp?\b", "klap", t)
    t = re.sub(r"(?i)\b3[- ]hour\b", "three hour", t)
    t = t.replace("-", " ")
    return t.split()


def wer(ref, hyp):
    r, h = [norm(w) for w in spoken(ref)], [norm(w) for w in spoken(hyp)]
    r, h = [w for w in r if w], [w for w in h if w]
    d = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        prev, d[0] = d.copy(), i
        for j in range(1, len(h) + 1):
            d[j] = min(prev[j] + 1, d[j - 1] + 1, prev[j - 1] + (r[i - 1] != h[j - 1]))
    return int(d[len(h)])


def dynamics(y, sr):
    """v2: loudness movement inside the take (std / mean of 50 ms RMS over the louder frames): flat reads as generic"""
    f = int(.05 * sr)
    r = np.array([np.sqrt(np.mean(y[i:i + f] ** 2)) for i in range(0, len(y) - f, f)])
    r = r[r > r.max() * .08]
    return float(r.std() / (r.mean() + 1e-9)) if len(r) > 4 else 0.0


def spread(y, sr):
    f0, _, _ = librosa.pyin(librosa.resample(y, orig_sr=sr, target_sr=16000), fmin=80, fmax=600, sr=16000)
    f0 = f0[~np.isnan(f0)]
    return float(np.percentile(f0, 95) - np.percentile(f0, 5)) if len(f0) > 10 else 0.0


def main():
    script = json.load(open(os.path.join(ROOT, "plan", "script.json")))
    wm = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
    out, words, log, t = [np.zeros(int(LEAD * SR), dtype=np.float32)], [], [], LEAD
    for ln in script:
        best = None
        for k in (0, 1, 2, 3):
            path = os.path.join(TAKES, f"{ln['id']}_t{k}.wav")
            if not os.path.exists(path):
                continue
            segs, _ = wm.transcribe(path, word_timestamps=True, language="en", beam_size=5, vad_filter=False)
            ws = [w for s in segs for w in s.words]
            hyp = " ".join(w.word.strip() for w in ws)
            y, sr = librosa.load(path, sr=SR, mono=True)
            sp, dy = spread(y, sr), dynamics(y, sr)
            # a pitch range far beyond speech (> 300 Hz) is a glitch (a squeak), counted as a slip; a take much longer than
            # its siblings usually holds a stall or a repeat, counted as one too
            expr = min(sp, 300) / 300 + dy
            score = (wer(ln["text"], hyp) + (1 if sp > 300 else 0), -round(expr, 3))
            log.append({"line": ln["id"], "take": k, "heard": hyp, "errors": score[0], "pitch_spread_hz": round(sp), "dynamics": round(dy, 3), "dur": round(len(y) / sr, 2)})
            if best is None or score < best[0]:
                best = (score, k, y, ws)
        score, k, y, ws = best
        # trim to the speech: from just before the first word to a short tail after the last
        a = max(0, int((ws[0].start - .04) * SR))
        b = min(len(y), int((ws[-1].end + .12) * SR))
        seg = y[a:b]
        fade = int(.012 * SR)
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        # word times in the reel; the script's own words (same count when the take is clean, else Whisper's)
        sw = ln["text"].split()
        use = sw if len(sw) == len(ws) else [w.word.strip() for w in ws]
        for w, txt in zip(ws, use):
            words.append({"line": ln["id"], "w": txt, "t0": round(t + w.start - a / SR, 3), "t1": round(t + w.end - a / SR, 3)})
        out.append(seg.astype(np.float32))
        t += len(seg) / SR
        g = GAP[ln["id"]] * GAP_SCALE
        out.append(np.zeros(int(g * SR), dtype=np.float32))
        t += g
        print(f"{ln['id']} take {k} errors {score[0]} expr {-score[1]:.2f}  {len(seg) / SR:.2f}s", flush=True)
    vo = np.concatenate(out + [np.zeros(int(.3 * SR), dtype=np.float32)])
    sfx = f"_{TAG}" if TAG else ""
    raw = os.path.join(ROOT, "assets", "audio", f"vo_raw{sfx}.wav")
    sf.write(raw, vo, SR)
    # v2 mastering: high-pass, de-ess, a broadcast compressor, a little less mud at 250 Hz, presence at 3.2 kHz and air at
    # 9 kHz, a limiter, then -16 LUFS for the voice on its own
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    f"atempo={TEMPO},highpass=f=85,deesser=i=0.4,acompressor=threshold=-18dB:ratio=3:attack=8:release=110:makeup=3,"
                    "equalizer=f=250:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1:g=2,equalizer=f=9000:t=h:w=2000:g=1,alimiter=limit=0.95,"
                    "loudnorm=I=-16:TP=-2:LRA=9",
                    "-ar", str(SR), "-ac", "1", os.path.join(ROOT, "assets", "audio", f"vo{sfx}.wav")], check=True)
    for w in words:                       # atempo scales time linearly
        w["t0"], w["t1"] = round(w["t0"] / TEMPO, 3), round(w["t1"] / TEMPO, 3)
    json.dump(words, open(os.path.join(ROOT, "plan", f"words{sfx}.json"), "w"), indent=0)
    json.dump({"duration": round(len(vo) / SR, 3), "takes": log}, open(os.path.join(ROOT, "plan", f"vo_pick{sfx}.json"), "w"), indent=1)
    print(f"vo{sfx}.wav {len(vo) / SR:.2f}s, {len(words)} words")


if __name__ == "__main__":
    main()
