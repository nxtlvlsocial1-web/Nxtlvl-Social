"""The voiceover: cut Liam's take into its eight lines, time every word, lay the lines out tight.

python3 build/voice.py              (from the project root; needs numpy and ffmpeg)
python3 build/voice.py --estimate   (no take yet: provisional timings from the text, for building the visuals)

voice/raw/vo1.mp3 is one ElevenLabs read (voice "Liam - Energetic, Social Media Creator", Eleven v4) of LINES, with a
pause between lines. The line breaks are the silences named in BOUNDS (from ffmpeg silencedetect at -40 dB: Liam's
pauses between lines are no longer than the ones inside them, so they're picked by hand); inside a line, the voiced stretches are matched to
its phrases (split at full stops, commas, "?" and "...") and words share their phrase's time by syllable weight. Each
line is cut from its first sound to its last, pauses inside it held to KEEP, and the lines are laid end to end with GAP
between them. When voice/raw/words_vo1.json is there (ElevenLabs Scribe word timestamps for the take, delivery tags
removed), those times are used instead of the estimate. Writes assets/audio/voice.wav (48 kHz mono, -16 LUFS), build/words.json and voice/lines.json.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
HOP = 480
KEEP = .22
LEAD = .12
GAP = [.0, .28, .3, .35, .3, .3, .45, .4]       # before each line: tight, with a beat into the twist and the CTA
TEMPO = 1.0
BOUNDS = [4.17, 9.76, 13.30, 18.94, 23.34, 27.37, 33.27]      # middles of the silences between the eight lines
LINES = [
    "At three A.M., a developer deleted his entire production database.",
    "One point two million rows. Gone. And the backups? Dead since March.",
    "But his AI had a copy. Here's the setup that saved him.",
    "One: a snapshot hook. Before any DROP or DELETE runs, Claude backs up the database first.",
    "Two: a production block. Destructive commands on prod? Refused.",
    "Three: a backup alarm. Every session checks your backups are fresh.",
    "And the part nobody does... a read-only login for production. You can't drop what you can't touch.",
    "Comment BACKUP, and I'll send you the whole setup.",
]


def run(*a):
    return subprocess.run(a, capture_output=True, check=True)


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") and len(w) > 3 else 0)
    return max(1, n) + .4


def phrases(text):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if re.search(r"[.,?!:]$|\.\.\.$", w):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def spread(ws, a, b):
    k = [syl(w) for w in ws]
    out, t = [], a
    for w, x in zip(ws, k):
        d = (b - a) * x / sum(k)
        out.append((w, t, t + d)); t += d
    return out


def runs(x, a, b, bridge=10):
    seg = x[int(a * SR):int(b * SR)]
    n = len(seg) // HOP
    db = 20 * np.log10(np.sqrt(np.mean(seg[:n * HOP].reshape(n, HOP) ** 2, axis=1)) + 1e-9)
    on = db > max(-42, db.max() - 34)
    out, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if out and i - out[-1][1] < bridge:
                out[-1][1] = j
            else:
                out.append([i, j])
            i = j
        else:
            i += 1
    return [(a + s * HOP / SR, a + e * HOP / SR) for s, e in out if e - s > 3]


def estimate():
    words, lines, t = [], [], .25
    for li, text in enumerate(LINES):
        t += GAP[li]
        ps = phrases(text)
        a = t
        for p in ps:
            d = sum(syl(w) for w in p) * .2
            for w, s, e in spread(p, t, t + d):
                words.append({"line": li + 1, "w": w, "s": round(s, 3), "e": round(e, 3)})
            t += d + .18
        lines.append({"line": li + 1, "text": text, "start": round(a, 3), "end": round(t - .18, 3)})
    return words, lines, t + .1


def main():
    if "--estimate" in sys.argv:
        words, lines, dur = estimate()
    else:
        raw = run("ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "voice", "raw", "vo1.mp3"), "-f", "f32le", "-ac", "1",
                  "-ar", str(SR), "-").stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        dur0 = len(x) / SR
        edges = [0] + BOUNDS + [dur0]
        sw = os.path.join(ROOT, "voice", "raw", "words_vo1.json")
        scribe = json.load(open(sw)) if os.path.exists(sw) else None
        si = 0
        parts, words, lines, t0 = [], [], [], .25
        parts.append(np.zeros(int(.25 * SR)))
        for li, text in enumerate(LINES):
            vs = runs(x, edges[li], edges[li + 1])
            a, b = max(0, vs[0][0] - LEAD), min(dur0, vs[-1][1] + LEAD)
            ps = phrases(text)
            if len(vs) >= len(ps) > 1:
                gi = sorted(sorted(range(1, len(vs)), key=lambda k: -(vs[k][0] - vs[k - 1][1]))[:len(ps) - 1])
                spans, prev = [], 0
                for c in gi + [len(vs)]:
                    spans.append((vs[prev][0], vs[c - 1][1])); prev = c
            else:
                k = [sum(syl(w) for w in p) for p in ps]
                spans, acc = [], vs[0][0]
                for kk in k:
                    d = (vs[-1][1] - vs[0][0]) * kk / sum(k); spans.append((acc, acc + d)); acc += d
            ws = [wt for p, (s0, s1) in zip(ps, spans) for wt in spread(p, s0, s1)]
            if scribe:
                n = len(text.split())
                got = scribe[si:si + n]; si += n
                if [re.sub(r"[^a-z']", "", g["text"].lower()) for g in got] != [re.sub(r"[^a-z']", "", w.lower()) for w in text.split()]:
                    raise SystemExit(f"Scribe words don't match line {li + 1}: " + " ".join(g["text"] for g in got))
                ws = [(w, max(g["start"], vs[0][0]) if k == 0 else g["start"], g["end"]) for k, (w, g) in enumerate(zip(text.split(), got))]
                # the cut stays on the sound itself (a, b above); Scribe squeezes the first word after a tag, so
                # a line's first word starts no later than its first sound
                ws[0] = (ws[0][0], min(ws[0][1], vs[0][0] + .02), ws[0][2])
            # cut a..b, holding the pauses between voiced stretches to KEEP
            cut, mapping, pos = [], [], a
            for (v0, v1) in runs(x, a, b, bridge=4):
                if v0 - pos > KEEP:
                    mapping.append((pos + KEEP / 2, v0 - KEEP / 2))
                pos = v1
            seg = x[int(a * SR):int(b * SR)].copy()
            keep = np.ones(len(seg), bool)
            for c0, c1 in mapping:
                keep[int((c0 - a) * SR):int((c1 - a) * SR)] = False
            mapt = lambda t: t - a - sum(min(t, c1) - c0 for c0, c1 in mapping if t > c0)  # noqa: E731
            y = seg[keep]
            f = int(.01 * SR)
            y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
            t0 += GAP[li]
            parts.append(np.zeros(int(GAP[li] * SR))); parts.append(y)
            for w, s, e in ws:
                words.append({"line": li + 1, "w": w, "s": round(t0 + mapt(s), 3), "e": round(t0 + mapt(e), 3)})
            lw = [w for w in words if w["line"] == li + 1]
            lines.append({"line": li + 1, "text": text, "start": lw[0]["s"], "end": lw[-1]["e"]})
            t0 += len(y) / SR
        y = np.concatenate(parts + [np.zeros(int(.3 * SR))])
        tmp = os.path.join(ROOT, "voice", "tight.f32")
        y.astype(np.float32).tofile(tmp)
        os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
        run("ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp, "-af",
            f"atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1",
            os.path.join(ROOT, "assets", "audio", "voice.wav"))
        os.remove(tmp)
        dur = len(y) / SR / TEMPO
        if TEMPO != 1.0:
            for w in words:
                w["s"], w["e"] = round(w["s"] / TEMPO, 3), round(w["e"] / TEMPO, 3)
            for ln in lines:
                ln["start"], ln["end"] = round(ln["start"] / TEMPO, 3), round(ln["end"] / TEMPO, 3)
    json.dump(words, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    json.dump({"duration": round(dur, 3), "lines": lines}, open(os.path.join(ROOT, "voice", "lines.json"), "w"), indent=1)
    print(f"voice {dur:.2f} s{' (ESTIMATE)' if '--estimate' in sys.argv else ''}")
    for ln in lines:
        print(f"  {ln['start']:6.2f}-{ln['end']:6.2f}  {ln['text']}")


if __name__ == "__main__":
    main()
