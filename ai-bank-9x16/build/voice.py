"""Assemble the AI Bank reel's voiceover from the narration takes and time its captions.

python3 build/voice.py      (from the project root; needs ffmpeg and numpy)

voice/raw/<nn>_<beat>_af_heart.wav are the takes: Kokoro-82M (Apache-2.0), voice af_heart, made with
`npx hyperframes tts`. ElevenLabs had no credits left for this reel. Each take is trimmed to its speech,
sped up a touch and loudness-matched to -16 LUFS; the lines are laid end to end.

Captions: Kokoro gives no word times, so each take is split at its pauses. The longest pauses inside a line are
matched, in order, to the line's punctuation (. , ?), so every phrase gets its exact start and end; inside a phrase the
words share the time by syllable count. Writes assets/audio/voice.wav, voice/lines.json and build/words.json.
"""
import json
import os
import re
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice")
SR = 48000
TEMPO = 1.0
GAPS = [.28, .3, .3, .3, .38, .45, .35, 0]
LEAD = .1


def run(*a):
    return subprocess.run(a, capture_output=True, check=True)


def load(path):
    raw = run("ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-").stdout
    return np.frombuffer(raw, np.float32)


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith(("le", "ee")) and len(w) > 3 else 0)
    return max(1, n)


def span(x, thr=-34):
    hop = SR // 100
    env = 20 * np.log10(np.sqrt(np.mean(x[: len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1)) + 1e-9)
    on = env > thr
    idx = np.flatnonzero(on)
    return on, idx[0], idx[-1] + 1


def phrase_times(x, text, take):
    """[(start, end)] per phrase of the line, in seconds of the raw take. Each phrase was also synthesized on its own
    (voice/phr); their lengths say where the breaks should fall, and the nearest real pause in the take is used."""
    on, a, b = span(x)
    sil, k = [], a
    while k < b:
        if not on[k]:
            j = k
            while j < b and not on[j]:
                j += 1
            if j - k >= 3:
                sil.append((k, j))
            k = j
        else:
            k += 1
    phrases = [p for p in re.split(r"(?<=[.,?])\s+", text.strip()) if p]
    lens = []
    for n in range(len(phrases)):
        _, pa, pb = span(load(os.path.join(V, "phr", f"{take}_{n}.wav")))
        lens.append(pb - pa)
    cum = np.cumsum(lens)[:-1] / sum(lens)
    edges, used = [a], set()
    for c in cum:
        want = a + c * (b - a)
        best = min((s for s in sil if s not in used and s[0] > edges[-1]), key=lambda s: abs((s[0] + s[1]) / 2 - want), default=None)
        if best is None or abs((best[0] + best[1]) / 2 - want) > 45:
            edges += [int(want), int(want)]
        else:
            used.add(best); edges += [best[0], best[1]]
    edges.append(b)
    return phrases, [(edges[2 * i] / 100, edges[2 * i + 1] / 100) for i in range(len(phrases))], a / 100, b / 100


def main():
    script = json.load(open(os.path.join(V, "script.json")))["lines"]
    os.makedirs(os.path.join(V, "tight"), exist_ok=True)
    parts, lines, words, t = [], [], [], LEAD
    for i, (take, text) in enumerate(script):
        src = os.path.join(V, "raw", f"{take}_af_heart.wav")
        x = load(src)
        phrases, spans, s0, s1 = phrase_times(x, text, take)
        cut_in, cut_out = max(0, s0 - .04), min(len(x) / SR, s1 + .12)
        dst = os.path.join(V, "tight", f"{i + 1:02d}.wav")
        af = (f"atrim=start={cut_in:.3f}:end={cut_out:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.06,"
              f"areverse,atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11")
        run("ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ar", str(SR), "-ac", "1", dst)
        d = (cut_out - cut_in) / TEMPO
        lines.append({"line": i + 1, "take": take, "speaker": "narrator", "text": text, "start": round(t, 3), "end": round(t + d, 3)})
        m = lambda v: t + (v - cut_in) / TEMPO  # noqa: E731
        for ph, (a, b) in zip(phrases, spans):
            ws = ph.split()
            wt = np.array([syl(w) + .35 for w in ws])
            c = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
            for k, w in enumerate(ws):
                ws_, we_ = a + (b - a) * c[k], a + (b - a) * c[k + 1]
                words.append({"line": i + 1, "speaker": "narrator", "w": w, "s": round(m(ws_) - .02, 3), "e": round(m(we_), 3)})
        parts.append((t, dst))
        t += d + GAPS[i]
    total = t + .1
    flt = "".join(f"[{k}]adelay={int(st * 1000)}|{int(st * 1000)}[a{k}];" for k, (st, _) in enumerate(parts))
    flt += "".join(f"[a{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total}"
    args = ["ffmpeg", "-y", "-v", "error"]
    for _, p in parts:
        args += ["-i", p]
    run(*args, "-filter_complex", flt, "-ar", str(SR), "-ac", "1", os.path.join(ROOT, "assets", "audio", "voice.wav"))
    json.dump({"duration": round(total, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    json.dump(words, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    print(f"voice.wav {total:.2f} s, {len(words)} words")
    for l in lines:
        print(f"  {l['start']:6.2f}-{l['end']:6.2f}  " + " ".join(f"{w['w']}@{w['s']:.2f}" for w in words if w["line"] == l["line"]))


if __name__ == "__main__":
    main()
