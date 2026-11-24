"""Voice for the AI.NXTLVL Off Grid reel: Kokoro-82M (Apache 2.0, local), voice from plan/vo_kok.json (am_michael),
no cloning. Copied from creedom-grade-9x16/build/vo_kok.py.

For every line of plan/script.json ("text" is what is said, "display" what the captions show, "speed" the line's pace),
three takes are made around that speed. Each take is transcribed with faster-whisper small.en and compared with the
display words (Whisper writes numbers as digits, like the display); the take with the fewest slips wins, ties go to the
wider pitch range (livelier). Takes are trimmed to their speech, joined with short gaps (GAP, longer after a line in
plan/vo_kok.json "gap"), polished (high-pass, light compression, -16 LUFS) into assets/audio/vo.wav, and the word times
go to plan/words.json with the display spelling.
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_kok.py
"""
import json
import os
import re
import subprocess

import librosa
import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "audio", "vo_takes_v5")
CFG = json.load(open(os.path.join(ROOT, "plan", "vo_kok.json")))       # {"gap": .26, "after": {"f02": .5}}
SAY = {"Creedom": "[Creedom](/kɹˈidəm/)", "Cree": "[Cree](/kɹˈi/)", "reel": "[reel](/ɹˈiːl/)"}
SR, LEAD = 48000, .05


def norm(w):
    return re.sub(r"[^a-z0-9.]", "", w.lower()).strip(".")


def wer(ref, hyp):
    r, h = [x for x in map(norm, ref) if x], [x for x in map(norm, hyp) if x]
    d = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        prev, d[0] = d.copy(), i
        for j in range(1, len(h) + 1):
            d[j] = min(prev[j] + 1, d[j - 1] + 1, prev[j - 1] + (r[i - 1] != h[j - 1]))
    return int(d[len(h)])


def spread(y):
    f0, _, _ = librosa.pyin(librosa.resample(y, orig_sr=SR, target_sr=16000), fmin=80, fmax=600, sr=16000)
    f0 = f0[~np.isnan(f0)]
    return float(np.percentile(f0, 95) - np.percentile(f0, 5)) if len(f0) > 10 else 0.0


def main():
    from kokoro import KPipeline
    from faster_whisper import WhisperModel
    os.makedirs(OUT, exist_ok=True)
    script = json.load(open(os.path.join(ROOT, "plan", "script.json")))
    kp = KPipeline(lang_code="a")
    wm = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
    out, words, log, t = [np.zeros(int(LEAD * SR), np.float32)], [], [], LEAD
    for ln in script:
        text = ln["text"]
        for a, b in SAY.items():
            text = re.sub(rf"\b{a}\b", b, text)
        disp = ln["display"].replace('"', "").split()
        best = None
        for k, sp in enumerate((ln["speed"] - .05, ln["speed"], ln["speed"] + .05)):
            path = os.path.join(OUT, f"{ln['id']}_t{k}.wav")
            a = np.concatenate([np.asarray(x[2]) for x in kp(text, voice=CFG.get("voice", "af_heart"), speed=sp)])
            sf.write(path, a, 24000)
            segs, _ = wm.transcribe(path, word_timestamps=True, language="en", beam_size=5, vad_filter=False)
            ws = []
            for s in segs:
                for w in s.words:
                    tok = w.word.strip()
                    if tok.startswith(".") and ws:
                        ws[-1] = (ws[-1][0] + tok, ws[-1][1], w.end)
                    else:
                        ws.append((tok, w.start, w.end))
            y, _ = librosa.load(path, sr=SR, mono=True)
            sc = (wer(disp, [w[0] for w in ws]), -min(spread(y), 300))
            log.append({"line": ln["id"], "take": k, "speed": round(sp, 2), "heard": " ".join(w[0] for w in ws), "slips": sc[0]})
            if best is None or sc < best[0]:
                best = (sc, k, y, ws)
        sc, k, y, ws = best
        a0, b0 = max(0, int((ws[0][1] - .03) * SR)), min(len(y), int((ws[-1][2] + .1) * SR))
        seg = y[a0:b0].astype(np.float32)
        f = int(.01 * SR)
        seg[:f] *= np.linspace(0, 1, f)
        seg[-f:] *= np.linspace(1, 0, f)
        use = disp if len(disp) == len(ws) else [w[0] for w in ws]
        for (tok, s0, s1), txt in zip(ws, use):
            words.append({"line": ln["id"], "w": txt, "t0": round(t + s0 - a0 / SR, 3), "t1": round(t + s1 - a0 / SR, 3)})
        out.append(seg)
        t += len(seg) / SR
        g = CFG["after"].get(ln["id"], CFG["gap"])
        out.append(np.zeros(int(g * SR), np.float32))
        t += g
        print(f"{ln['id']} take {k} slips {sc[0]} {len(seg) / SR:.2f}s  {' '.join(w[0] for w in ws)}", flush=True)
    vo = np.concatenate(out + [np.zeros(int(.3 * SR), np.float32)])
    raw = os.path.join(ROOT, "assets", "audio", "vo_raw.wav")
    sf.write(raw, vo, SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-2:LRA=9",
                    "-ar", str(SR), "-ac", "1", os.path.join(ROOT, "assets", "audio", "vo.wav")], check=True)
    json.dump(words, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
    json.dump({"duration": round(len(vo) / SR, 3), "takes": log}, open(os.path.join(ROOT, "plan", "vo_pick.json"), "w"), indent=1)
    print(f"vo.wav {len(vo) / SR:.2f}s, {len(words)} words")


if __name__ == "__main__":
    main()
