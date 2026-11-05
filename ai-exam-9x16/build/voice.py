"""The AI Exam reel's dialogue (YOU, the student, and HOOT, the AI owl), voiced phrase by phrase, and its caption timing.

python3 build/voice.py      (from the project root; needs kokoro-onnx, numpy, soundfile, ffmpeg)

Placeholder voices: Kokoro-82M (Apache-2.0, local); the final voices come from ElevenLabs (voice/el/<take>.wav,
one take per line, which replace the Kokoro phrases when present). Every phrase in
voice/script.json carries an emotion. The emotion sets the speaking rate (Kokoro's speed), a small pitch move (about a
semitone, by playback rate, with Kokoro slowed to match so there are no artifacts) and the level, and the phrase is followed by its own pause: hushed and tense phrases are
slower, lower and quieter, excited ones faster, higher and louder, punches land after a beat. The phrases are laid end
to end, so every phrase boundary is exact; inside a phrase the words share the time by syllable count. A line may carry a
display text for the captions (same word count; `~` merges a spoken word into the previous caption word).
Writes voice/phr/*.wav, assets/audio/voice.wav (-16 LUFS), voice/lines.json and build/words.json.
"""
import json
import os
import re
import subprocess
from fractions import Fraction

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from scipy.signal import resample_poly

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice")
CACHE = os.path.expanduser("~/.cache/hyperframes/tts")
SR = 48000
LEAD = .12
LINE_GAP = .28
VOICES = {"you": "af_bella", "owl": "am_fenrir"}
# emotion -> (speed, semitones, gain dB)
EMO = {"panic": (1.08, .4, 1.0), "dry": (.92, -.3, 0), "whine": (1.02, .5, .5), "calm": (.98, 0, 0), "surprised": (1.04, .5, 1.0),
       "warm": (.97, 0, 0), "proud": (1.0, .2, .5), "amazed": (1.06, .6, 1.5), "sad": (.88, -.4, -2.0), "excite": (1.1, .6, 2.0),
       "scheme": (1.0, .1, -1.0), "smile": (1.03, .3, .5), "punch": (.98, .2, 1.5)}


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith(("le", "ee")) and len(w) > 3 else 0)
    return max(1, n)


def fade(x, thr=-52):
    """Trim the model's silence gently (a soft first sound like 'sh' or 's' starts far below the vowel), keep 70 ms of
    air before the first sound and 120 ms after the last, and soften the edges."""
    hop = SR // 200
    n = len(x) // hop
    env = 20 * np.log10(np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    idx = np.flatnonzero(env > max(thr, env.max() - 48))
    a_, b_ = max(0, idx[0] - 14), min(n, idx[-1] + 24)
    y = x[a_ * hop: b_ * hop].copy()
    f = int(.02 * SR); y[:f] *= np.linspace(0, 1, f) ** 2
    f = int(.05 * SR); y[-f:] *= np.linspace(1, 0, f)
    return y


def split_phrases(a, n):
    """[(start, end)] in seconds for n phrases of a take: the n-1 longest pauses inside the speech split it, in order."""
    hop = SR // 100
    m = len(a) // hop
    env = 20 * np.log10(np.sqrt(np.mean(a[: m * hop].reshape(m, hop) ** 2, axis=1)) + 1e-9)
    on = env > max(-45, env.max() - 35)
    idx = np.flatnonzero(on); a0, a1 = idx[0], idx[-1] + 1
    gaps, k = [], a0
    while k < a1:
        if not on[k]:
            j = k
            while j < a1 and not on[j]:
                j += 1
            gaps.append((j - k, k, j)); k = j
        else:
            k += 1
    cuts = sorted(sorted(gaps, reverse=True)[: n - 1], key=lambda g: g[1])
    bounds, s0 = [], a0
    for _, g0, g1 in cuts:
        bounds.append((s0 / 100, g0 / 100)); s0 = g1
    bounds.append((s0 / 100, a1 / 100))
    while len(bounds) < n:
        bounds.append(bounds[-1])
    return bounds


def main():
    script = json.load(open(os.path.join(V, "script.json")))["lines"]
    os.makedirs(os.path.join(V, "phr"), exist_ok=True)
    k = Kokoro(os.path.join(CACHE, "models", "kokoro-v1.0.onnx"), os.path.join(CACHE, "voices", "voices-v1.0.bin"))
    out, lines, words, t = [], [], [], LEAD
    for i, (take, spk, disp, phrases) in enumerate(script):
        shown = disp.split() if disp else None
        wi, t0 = 0, t
        elp = os.path.join(V, "el", f"{take}.wav")
        if os.path.exists(elp):                     # an ElevenLabs take for the whole line
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", elp, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
            a = fade(np.frombuffer(raw, np.float32).astype(np.float64))
            d = len(a) / SR
            spans = split_phrases(a, len(phrases))
            for (text, emo, pause), (p0, p1) in zip(phrases, spans):
                ws = [w for w in text.split() if re.search(r"[A-Za-z0-9]", w)]
                wt = np.array([syl(w) + .35 for w in ws])
                c = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
                for j, w in enumerate(ws):
                    sw = shown[wi] if shown else w
                    wi += 1
                    s_, e_ = t + p0 + (p1 - p0) * c[j], t + p0 + (p1 - p0) * c[j + 1]
                    if sw == "~" and words:
                        words[-1]["e"] = round(e_, 3); continue
                    words.append({"line": i + 1, "speaker": spk, "w": sw, "s": round(s_ - .02, 3), "e": round(e_, 3)})
            out.append((t, a)); t += d
            txt = disp.replace(" ~", "") if disp else " ".join(p[0] for p in phrases)
            lines.append({"line": i + 1, "take": take, "speaker": spk, "text": txt, "start": round(t0, 3), "end": round(t, 3)})
            print(f"  {t0:6.2f}-{t:6.2f}  [el] {txt}")
            t += LINE_GAP
            continue
        for n, (text, emo, pause) in enumerate(phrases):
            sp, st, gdb = EMO[emo]
            r = 2 ** (st / 12)                       # pitch by playback rate; Kokoro speaks slower to keep the pace
            a, sr = k.create(text, voice=VOICES[spk], speed=sp / r, lang="en-us", trim=False)
            q = Fraction(SR / (r * sr)).limit_denominator(200)
            a = resample_poly(a.astype(np.float64), q.numerator, q.denominator)
            a = fade(a) * 10 ** (gdb / 20)
            sf.write(os.path.join(V, "phr", f"{take}_{n}.wav"), a.astype(np.float32), SR)
            d = len(a) / SR
            ws = [w for w in text.split() if re.search(r"[A-Za-z0-9]", w)]     # "..." is a pause, not a word
            wt = np.array([syl(w) + .35 for w in ws])
            c = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
            for j, w in enumerate(ws):
                sw = shown[wi] if shown else w
                wi += 1
                s_, e_ = t + d * c[j], t + d * c[j + 1]
                if sw == "~" and words:
                    words[-1]["e"] = round(e_, 3); continue
                words.append({"line": i + 1, "speaker": spk, "w": sw, "s": round(s_ - .02, 3), "e": round(e_, 3)})
            out.append((t, a))
            t += d + (pause if n < len(phrases) - 1 else 0)
        txt = disp.replace(" ~", "") if disp else " ".join(p[0] for p in phrases)
        lines.append({"line": i + 1, "take": take, "speaker": spk, "text": txt, "start": round(t0, 3), "end": round(t, 3)})
        print(f"  {t0:6.2f}-{t:6.2f}  {txt}")
        t += LINE_GAP
    total = t - LINE_GAP + .15
    mix = np.zeros(int(total * SR) + SR)
    for st_, a in out:
        i0 = int(st_ * SR); mix[i0:i0 + len(a)] += a
    mix = mix[: int(total * SR)]
    raw = os.path.join(V, "voice_raw.wav")
    sf.write(raw, (mix / max(1e-9, np.max(np.abs(mix))) * .8).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1",
                    os.path.join(ROOT, "assets", "audio", "voice.wav")], check=True)
    os.remove(raw)
    json.dump({"duration": round(total, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    json.dump(words, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    print(f"voice.wav {total:.2f} s, {len(words)} words")


if __name__ == "__main__":
    main()
