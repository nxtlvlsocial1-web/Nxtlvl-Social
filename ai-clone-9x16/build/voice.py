"""Assemble the AI Clone reel's voiceover from the narration takes and time its captions.

python3 build/voice.py      (from the project root; needs ffmpeg and numpy)

voice/raw/<nn>_<beat>.wav are the takes: Kokoro-82M (Apache-2.0), voice am_michael, made with
`npx hyperframes tts`. ElevenLabs had no credits left for this reel. A line may carry a display text for the
captions (same word count; `~` merges a spoken word into the previous caption word). Each take is trimmed to its speech,
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
GAPS = [.3, .3, .32, .3, .4, .45, .35, 0]
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


def feats(x):
    """log band energies, 10 ms hop"""
    hop, win = SR // 100, SR // 40
    n = (len(x) - win) // hop
    fr = np.stack([x[k * hop:k * hop + win] * np.hanning(win) for k in range(max(1, n))])
    sp = np.abs(np.fft.rfft(fr, axis=1)) ** 2
    edges = np.geomspace(80, 8000, 25) / (SR / 2) * sp.shape[1]
    bands = np.stack([sp[:, int(a):max(int(a) + 1, int(b))].sum(1) for a, b in zip(edges[:-1], edges[1:])], 1)
    f = np.log(bands + 1e-9)
    return (f - f.mean(0)) / (f.std(0) + 1e-6)


def dtw_path(A, B):
    """monotone alignment of frames of A to frames of B (cosine distance)"""
    a = A / np.linalg.norm(A, axis=1, keepdims=True); b = B / np.linalg.norm(B, axis=1, keepdims=True)
    D = 1 - a @ b.T
    n, m = D.shape
    acc = np.full((n + 1, m + 1), np.inf); acc[0, 0] = 0
    for i in range(1, n + 1):
        row = D[i - 1]
        prev = acc[i - 1]
        cur = acc[i]
        # vectorised over j for the two predecessors from the previous row, then the in-row one in a loop-free cumulative way
        best = np.minimum(prev[1:], prev[:-1]) + row
        for j_ in range(1, m + 1):
            v = best[j_ - 1]
            w = cur[j_ - 1] + row[j_ - 1]
            cur[j_] = v if v < w else w
    # backtrack
    i, j_ = n, m; path = []
    while i > 0 and j_ > 0:
        path.append((i - 1, j_ - 1))
        opts = [(acc[i - 1, j_ - 1], i - 1, j_ - 1), (acc[i - 1, j_], i - 1, j_), (acc[i, j_ - 1], i, j_ - 1)]
        _, i, j_ = min(opts)
    return path[::-1]


def phrase_times(x, text, take):
    """[(start, end)] per phrase in seconds of the raw take. Each phrase was also voiced on its own (voice/phr); the
    phrases, trimmed and laid end to end, are aligned to the full take with DTW, which carries their exact
    boundaries across."""
    on, a, b = span(x)
    phrases = [p for p in re.split(r"(?<=[.,?])\s+", text.strip()) if p]
    pieces, bounds, pos = [], [], 0
    for n in range(len(phrases)):
        y = load(os.path.join(V, "phr", f"{take}_{n}.wav"))
        _, pa, pb = span(y)
        seg_ = y[pa * SR // 100: pb * SR // 100]
        pieces.append(seg_); bounds.append((pos, pos + len(seg_))); pos += len(seg_)
    ref = np.concatenate(pieces)
    FA, FB = feats(x[a * SR // 100: b * SR // 100]), feats(ref)
    path = dtw_path(FB, FA)                         # ref frame -> take frame
    m = {}
    for i_, j_ in path:
        m.setdefault(i_, j_)
    def to_take(sample):
        f = min(int(sample / (SR // 100)), len(FB) - 1)
        while f not in m and f > 0:
            f -= 1
        return a / 100 + m.get(f, 0) / 100
    spans = [(to_take(s0), to_take(s1)) for s0, s1 in bounds]
    return phrases, spans, a / 100, b / 100


def main():
    script = json.load(open(os.path.join(V, "script.json")))["lines"]
    os.makedirs(os.path.join(V, "tight"), exist_ok=True)
    parts, lines, words, t = [], [], [], LEAD
    for i, (take, text, disp, _sp) in enumerate(script):
        src = os.path.join(V, "raw", f"{take}.wav")
        x = load(src)
        phrases, spans, s0, s1 = phrase_times(x, text, take)
        cut_in, cut_out = max(0, s0 - .04), min(len(x) / SR, s1 + .12)
        dst = os.path.join(V, "tight", f"{i + 1:02d}.wav")
        af = (f"atrim=start={cut_in:.3f}:end={cut_out:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.06,"
              f"areverse,atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11")
        run("ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ar", str(SR), "-ac", "1", dst)
        d = (cut_out - cut_in) / TEMPO
        lines.append({"line": i + 1, "take": take, "speaker": "narrator", "text": disp.replace(" ~", "") if disp else text, "start": round(t, 3), "end": round(t + d, 3)})
        m = lambda v: t + (v - cut_in) / TEMPO  # noqa: E731
        shown = (disp or text).split()
        wi = 0
        for ph, (a, b) in zip(phrases, spans):
            ws = ph.split()
            wt = np.array([syl(w) + .35 for w in ws])
            c = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
            for k, w in enumerate(ws):
                ws_, we_ = a + (b - a) * c[k], a + (b - a) * c[k + 1]
                sw = shown[wi]; wi += 1
                if sw == "~" and words:
                    words[-1]["e"] = round(m(we_), 3); continue
                words.append({"line": i + 1, "speaker": "narrator", "w": sw, "s": round(m(ws_) - .02, 3), "e": round(m(we_), 3)})
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
