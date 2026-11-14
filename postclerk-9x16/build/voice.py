"""Pick the best take per line, lay the lines out at reel pace, and time every word for the captions.

~/.venvs/tts/bin/python build/voice.py      (from the project root, after build/voices.py)

Each take is transcribed with faster-whisper; the take whose words match the script best wins (ties go to the livelier
one), unless voice/picks.json pins a take. Each pick is trimmed to its first and last sound, sped up by TEMPO (pitch kept,
ffmpeg atempo) and laid end to end with GAP[i] before line i. Whisper word times on the assembled voice are mapped onto the
script's display words (difflib), so the captions show "Metricool" and "Postclerk", not what the ear spelling says.
Writes assets/audio/voice.wav (48 kHz mono, -16 LUFS), build/words.json and build/cues.json (line starts and ends).
"""
import difflib
import json
import os
import re
import subprocess

import librosa
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
TEMPO = 1.07
LEAD = .25
GAP = [0, .22, .18, .3, .3, .25, .4, .2, .2, .3, .35, .35]
DISPLAY = [
    "Stop paying for Metricool.",
    "This one is free, and it's open source.",
    "It's called Postclerk.",
    "Instagram, TikTok, LinkedIn, YouTube and three more. All scheduled from one calendar.",
    "One composer, with a different caption for every platform.",
    "And a preview of your Instagram feed before anything goes live.",
    "But here's what Metricool doesn't give you.",
    "It connects to your AI.",
    "Claude Code, Cursor or Codex draft your posts and schedule them for you.",
    "I typed one sentence: plan my posts for next week. Done.",
    "Want your own copy? It deploys free on Cloudflare in about two minutes.",
    "Comment POST and I'll send you the link.",
]
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("metri cool", "metricool").replace("post clerk", "postclerk").replace("-", " ")).split()  # noqa: E731


def trim(y, sr):
    iv = librosa.effects.split(y, top_db=38, frame_length=1024, hop_length=256)
    return y[max(0, iv[0][0] - int(.03 * sr)): min(len(y), iv[-1][1] + int(.06 * sr))]


def main():
    takes = json.load(open(os.path.join(ROOT, "voice", "takes", "takes.json")))
    pins = json.load(open(os.path.join(ROOT, "voice", "picks.json"))) if os.path.exists(os.path.join(ROOT, "voice", "picks.json")) else {}
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    picks, out = {}, []
    for i, disp in enumerate(DISPLAY):
        key = f"{i + 1:02d}"; ref = norm(disp); best = None
        for k in range(3):
            f = os.path.join(ROOT, "voice", "takes", f"{key}_{k}.wav")
            if not os.path.exists(f): continue
            a, _ = librosa.load(f, sr=16000)
            txt = " ".join(s.text for s in m.transcribe(a, language="en", beam_size=5)[0])
            sc = difflib.SequenceMatcher(None, ref, norm(txt)).ratio()
            ex = takes.get(f"{key}_{k}", {}).get("exaggeration", 0)
            if best is None or (sc, ex) > (best[0], best[2]): best = (sc, k, ex, txt)
        k = pins.get(key, best[1]); picks[key] = {"take": k, "match": round(best[0], 2), "heard": best[3].strip()}
        print(key, k, round(best[0], 2), best[3].strip())
        y, sr = librosa.load(os.path.join(ROOT, "voice", "takes", f"{key}_{k}.wav"), sr=SR)
        out.append(trim(y, sr))
    json.dump(picks, open(os.path.join(ROOT, "voice", "picked.json"), "w"), indent=1)
    tmp = os.path.join(ROOT, "voice", "_raw.wav"); parts, t, lines = [np.zeros(int(LEAD * SR))], LEAD, []
    for i, y in enumerate(out):
        sf.write(tmp, y, SR)
        sped = subprocess.run(["ffmpeg", "-v", "error", "-i", tmp, "-af", f"atempo={TEMPO}", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        y2 = np.frombuffer(sped, np.float32).astype(np.float64)
        if i: parts.append(np.zeros(int(GAP[i] * SR))); t += GAP[i]
        lines.append([round(t, 3), round(t + len(y2) / SR, 3)]); parts.append(y2); t += len(y2) / SR
    os.remove(tmp)
    v = np.concatenate(parts + [np.zeros(int(.5 * SR))])
    raw = os.path.join(ROOT, "voice", "_v.wav"); sf.write(raw, v.astype(np.float32), SR)
    dst = os.path.join(ROOT, "assets", "audio", "voice.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", str(SR), "-ac", "1", dst], check=True)
    os.remove(raw)
    # word times
    a, _ = librosa.load(dst, sr=16000)
    segs, _ = m.transcribe(a, language="en", word_timestamps=True, beam_size=5)
    heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    words = []
    for li, disp in enumerate(DISPLAY):
        for w in disp.split(): words.append({"w": w, "line": li + 1})
    hn = [norm(h[0])[0] if norm(h[0]) else "" for h in heard]
    dn = [norm(w["w"])[0] if norm(w["w"]) else "" for w in words]
    sm = difflib.SequenceMatcher(None, dn, hn, autojunk=False)
    for blk in sm.get_matching_blocks():
        for j in range(blk.size):
            words[blk.a + j]["s"], words[blk.a + j]["e"] = round(heard[blk.b + j][1], 3), round(heard[blk.b + j][2], 3)
    # unmatched words: spread inside their line between known neighbours
    for li, (a0, a1) in enumerate(lines):
        idx = [i for i, w in enumerate(words) if w["line"] == li + 1]
        for n, i in enumerate(idx):
            if "s" in words[i] and a0 - .3 <= words[i]["s"] <= a1 + .3: continue
            prev = next((words[j]["e"] for j in reversed(idx[:n]) if "e" in words[j] and a0 - .3 <= words[j]["s"] <= a1 + .3), a0)
            nxt = next((words[j]["s"] for j in idx[n + 1:] if "s" in words[j] and a0 - .3 <= words[j]["s"] <= a1 + .3), a1)
            rest = [j for j in idx[n:] if not ("s" in words[j] and a0 - .3 <= words[j]["s"] <= a1 + .3)]
            k = rest.index(i) if i in rest else 0; cnt = max(1, len([j for j in rest if j <= idx[-1]]))
            step = max(.05, (nxt - prev) / cnt)
            words[i]["s"] = round(prev + step * k, 3); words[i]["e"] = round(prev + step * (k + 1), 3)
    json.dump(words, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    json.dump({"lines": lines, "end": round(t + .1, 3)}, open(os.path.join(ROOT, "build", "cues.json"), "w"), indent=1)
    print("voice", round(t, 2), "s; matched", sum(1 for blk in sm.get_matching_blocks() for _ in range(blk.size)), "/", len(words), "words")


if __name__ == "__main__":
    main()
