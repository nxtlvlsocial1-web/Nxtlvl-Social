"""samarpit.ai lead auto-reply reel (copied from framework-flywheel-9x16): pick the voiceover takes and join them (after build/vo.py); copied from the reel-flop project.

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
SR = 48000
TEMPO = float(os.environ.get("VO_TEMPO", "1.0"))
GAP_SCALE = 1.0
LEAD = .05         # the cold open hits at once
# pause after each line (s): peaks get room to land, the list moves fast
GAP = {"g1": .35, "g2": .3, "g3": .25, "g4": .35, "g5": .35, "g6": .35, "g7": .3}


NUM = {"one": "1", "two": "2", "three": "3", "anthropics": "anthropic", "claude": "claude"}


def norm(w):
    w = re.sub(r"[^a-z0-9]", "", w.lower())
    return NUM.get(w, w)


def spoken(text):
    """Whisper writes numbers and names its own way ("GTA6", "8 -hour", "10"): compare in spoken words"""
    t = text
    for a, b in (("19.7%", "nineteen point seven percent"), ("41.2%", "forty one point two percent"), ("41.2", "forty one point two"),
                 ("11.9%", "eleven point nine percent"), ("11.9", "eleven point nine"), ("19.7", "nineteen point seven"), ("/", "slash ")):
        t = t.replace(a, b)
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
            segs, _ = wm.transcribe(librosa.load(path, sr=16000, mono=True)[0], word_timestamps=True, language="en", beam_size=5, vad_filter=False)
            ws = [w for s in segs for w in s.words]
            hyp = " ".join(w.word.strip() for w in ws)
            y, sr = librosa.load(path, sr=SR, mono=True)
            sp = spread(y, sr)
            f = int(.05 * sr)
            r = np.array([np.sqrt(np.mean(y[i:i + f] ** 2)) for i in range(0, len(y) - f, f)])
            r = r[r > r.max() * .08]
            dy = float(r.std() / (r.mean() + 1e-9)) if len(r) > 4 else 0.0
            # a pitch range far beyond speech (> 300 Hz) is a glitch (a squeak), counted as a slip; then the liveliest take
            # wins: pitch movement plus loudness movement (v5: the owner heard a flat, read-out delivery)
            score = (wer(ln["text"], hyp) + (1 if sp > 300 else 0), -(min(sp, 300) / 300 + dy))
            log.append({"line": ln["id"], "take": k, "heard": hyp, "errors": score[0], "pitch_spread_hz": round(sp), "dynamics": round(dy, 3)})
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
        nxt = next((x for x in script[script.index(ln) + 1:]), None)
        g = (max(.35, nxt["at"] - t) if nxt and nxt.get("at") is not None else GAP.get(ln["id"], .4)) if nxt else 0.0
        out.append(np.zeros(int(g * SR), dtype=np.float32))
        t += g
        print(f"{ln['id']} take {k} errors {score[0]} expr {-score[1]:.2f}  {len(seg) / SR:.2f}s", flush=True)
    vo = np.concatenate(out + [np.zeros(int(.3 * SR), dtype=np.float32)])
    raw = os.path.join(ROOT, "assets", "audio", "vo_raw.wav")
    sf.write(raw, vo, SR)
    # gentle polish: high-pass, a little compression, then -16 LUFS for the voice on its own
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    f"atempo={TEMPO},highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-2:LRA=9",
                    "-ar", str(SR), "-ac", "1", os.path.join(ROOT, "assets", "audio", "vo.wav")], check=True)
    for w in words:                       # atempo scales time linearly
        w["t0"], w["t1"] = round(w["t0"] / TEMPO, 3), round(w["t1"] / TEMPO, 3)
    json.dump(words, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
    json.dump({"duration": round(len(vo) / SR, 3), "takes": log}, open(os.path.join(ROOT, "plan", "vo_pick.json"), "w"), indent=1)
    print(f"vo.wav {len(vo) / SR:.2f}s, {len(words)} words")


if __name__ == "__main__":
    main()
