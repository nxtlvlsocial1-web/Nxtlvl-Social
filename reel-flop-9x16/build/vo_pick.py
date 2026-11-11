"""Pick the voiceover takes and join them (after build/vo.py).

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
TAKES = os.path.join(ROOT, "assets", "audio", "vo_takes")
SR = 48000
LEAD = .04          # silence before the first word of the reel (v3: the cold open hits at once)
# pause after each line (s): peaks get room to land, the list moves fast
GAP = {"l00": .3, "l01": .22, "l02": .5, "l03": .3, "l04": .12, "l05": .3, "l06": .4, "l07": .12, "l08": .4, "l09": .12, "l10": .3, "l11": .4,
       "l12": .0}


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower().replace("twenty", "20"))


def wer(ref, hyp):
    r, h = [norm(w) for w in ref.split()], [norm(w) for w in hyp.split()]
    r, h = [w for w in r if w], [w for w in h if w]
    d = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        prev, d[0] = d.copy(), i
        for j in range(1, len(h) + 1):
            d[j] = min(prev[j] + 1, d[j - 1] + 1, prev[j - 1] + (r[i - 1] != h[j - 1]))
    return int(d[len(h)])


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
        for k in (0, 1):
            path = os.path.join(TAKES, f"{ln['id']}_t{k}.wav")
            if not os.path.exists(path):
                continue
            segs, _ = wm.transcribe(path, word_timestamps=True, language="en", beam_size=5, vad_filter=False)
            ws = [w for s in segs for w in s.words]
            hyp = " ".join(w.word.strip() for w in ws)
            y, sr = librosa.load(path, sr=SR, mono=True)
            score = (wer(ln["text"], hyp), -spread(y, sr))
            log.append({"line": ln["id"], "take": k, "heard": hyp, "errors": score[0], "pitch_spread_hz": round(-score[1])})
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
        g = GAP[ln["id"]]
        out.append(np.zeros(int(g * SR), dtype=np.float32))
        t += g
        print(f"{ln['id']} take {k} errors {score[0]} spread {-score[1]:.0f} Hz  {len(seg) / SR:.2f}s", flush=True)
    vo = np.concatenate(out + [np.zeros(int(.3 * SR), dtype=np.float32)])
    raw = os.path.join(ROOT, "assets", "audio", "vo_raw.wav")
    sf.write(raw, vo, SR)
    # gentle polish: high-pass, a little compression, then -16 LUFS for the voice on its own
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-2:LRA=9",
                    "-ar", str(SR), "-ac", "1", os.path.join(ROOT, "assets", "audio", "vo.wav")], check=True)
    json.dump(words, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
    json.dump({"duration": round(len(vo) / SR, 3), "takes": log}, open(os.path.join(ROOT, "plan", "vo_pick.json"), "w"), indent=1)
    print(f"vo.wav {len(vo) / SR:.2f}s, {len(words)} words")


if __name__ == "__main__":
    main()
