"""The Secret Free Store reel: the Nxtlvl Bot narration, one ElevenLabs take per line (voice/el/cand/<cand>.mp3), laid out
with the story beats between lines, and its word timing for the captions.

python3 build/voice.py      (from the project root; needs numpy, scipy, soundfile, ffmpeg)

Each take is split into its phrases at its longest pauses, the pauses between phrases are set to the script's values
(tight, for a fast reel), then the line is pitched up two semitones by resampling (a smaller, brighter robot, and
about 12 % faster, then 5 % more by time-stretch) and given a light robot colour (a short metallic comb and a touch of ring modulation). Inside a
phrase the words share the time by syllable count. Writes assets/audio/voice.wav (-16 LUFS), voice/lines.json and
build/words.json.
"""
import json
import os
import re
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, resample_poly, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice")
SR = 48000
LEAD = .12
TAIL = 1.5          # the end card holds after the last word
UP, DOWN = 500, 561  # resample: +2 semitones, 1.12x faster


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith(("le", "ee")) and len(w) > 3 else 0)
    return max(1, n)


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def envelope(a):
    hop = SR // 100
    m = len(a) // hop
    return 20 * np.log10(np.sqrt(np.mean(a[: m * hop].reshape(m, hop) ** 2, axis=1)) + 1e-9)


def phrases_of(a, n):
    """[(start, end)] in samples for n phrases: the n-1 longest pauses inside the speech split it, in order."""
    env = envelope(a)
    on = env > max(-45, env.max() - 32)
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
    out, s0 = [], a0
    for _, g0, g1 in cuts:
        out.append((s0, g0)); s0 = g1
    out.append((s0, a1))
    hop = SR // 100
    # keep 30 ms of air before each phrase and 50 ms after
    return [(max(0, s * hop - int(.03 * SR)), min(len(a), e * hop + int(.05 * SR))) for s, e in out]


TEMPO = 1.05       # plus a light pitch-preserving speed-up


def tempo(x):
    if TEMPO == 1:
        return x
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={TEMPO}", "-f", "f32le", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(r, np.float32).astype(np.float64)


def soft(x, fi=.012, fo=.04):
    x = x.copy(); f = min(len(x), int(fi * SR)); x[:f] *= np.linspace(0, 1, f) ** 2
    f = min(len(x), int(fo * SR)); x[-f:] *= np.linspace(1, 0, f)
    return x


def level(x, target=-20.0):
    hop = SR // 100
    n = len(x) // hop
    fr = x[: n * hop].reshape(n, hop)
    db = 20 * np.log10(np.sqrt(np.mean(fr ** 2, axis=1)) + 1e-9)
    act = fr[db > db.max() - 30]
    rms = 20 * np.log10(np.sqrt(np.mean(act ** 2)) + 1e-9)
    return x * 10 ** ((target - rms) / 20)


def robot(x):
    """A small, bright robot: high-passed, a short metallic comb and a touch of ring modulation."""
    x = sosfilt(butter(2, 140, "high", fs=SR, output="sos"), x)
    d = int(.0031 * SR)
    y = x.copy(); y[d:] += .32 * x[:-d]
    t = np.arange(len(y)) / SR
    y = y + .11 * y * np.sin(2 * np.pi * 170 * t)
    return y


def main():
    script = json.load(open(os.path.join(V, "script.json")))["lines"]
    out, lines, words, t = [], [], [], LEAD
    for i, (take, cand, disp, phrases, gap_after) in enumerate(script):
        a = level(load(os.path.join(V, "el", "cand", f"{cand}.mp3")))
        spans = phrases_of(a, len(phrases))
        parts, rel = [], []                       # rel: phrase (start, end) in the resampled line, seconds
        pos = 0
        for (text, gap), (s, e) in zip(phrases, spans):
            seg = soft(tempo(resample_poly(soft(a[s:e]), UP, DOWN)))
            rel.append((pos / SR, (pos + len(seg)) / SR))
            parts.append(seg); pos += len(seg)
            if gap:
                parts.append(np.zeros(int(gap * SR))); pos += int(gap * SR)
        y = robot(np.concatenate(parts))
        d = len(y) / SR
        shown = disp.split() if disp else None
        wi = 0
        ph_out = []
        for (text, _), (p0, p1) in zip(phrases, rel):
            ws = [w for w in text.split() if re.search(r"[A-Za-z0-9]", w)]
            wt = np.array([syl(w) + .35 for w in ws])
            c = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
            # the phrase's air: 40 ms before, 70 ms after (scaled by the resample)
            q0, q1 = p0 + .027, p1 - .045
            for j, w in enumerate(ws):
                sw = shown[wi] if shown else w
                wi += 1
                s_, e_ = t + q0 + (q1 - q0) * c[j], t + q0 + (q1 - q0) * c[j + 1]
                if sw == "~" and words:
                    words[-1]["e"] = round(e_, 3); continue
                words.append({"line": i + 1, "w": sw, "s": round(s_ - .02, 3), "e": round(e_, 3)})
            ph_out.append({"text": text, "start": round(t + q0, 3), "end": round(t + q1, 3)})
        out.append((t, y))
        txt = disp.replace(" ~", "") if disp else " ".join(p[0] for p in phrases)
        lines.append({"line": i + 1, "take": take, "cand": cand, "text": txt, "start": round(t, 3), "end": round(t + d, 3), "phrases": ph_out})
        print(f"  {t:6.2f}-{t + d:6.2f}  {txt}")
        t += d + gap_after
    total = t + TAIL
    mix = np.zeros(int(total * SR) + SR)
    for st_, y in out:
        i0 = int(st_ * SR); mix[i0:i0 + len(y)] += y
    mix = mix[: int(total * SR)]
    raw = os.path.join(V, "voice_raw.wav")
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    sf.write(raw, (mix / max(1e-9, np.max(np.abs(mix))) * .8).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1",
                    os.path.join(ROOT, "assets", "audio", "voice.wav")], check=True)
    os.remove(raw)
    json.dump({"duration": round(total, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    json.dump(words, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    print(f"voice.wav {total:.2f} s, {len(words)} words")


if __name__ == "__main__":
    main()
