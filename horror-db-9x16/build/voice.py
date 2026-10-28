"""Cut the two ElevenLabs takes into lines and lay them out as the dialogue (Eleven v4).

python3 build/voice.py      (from the project root; needs numpy and ffmpeg)

voice/raw/dev1.mp3     the developer, every line in one read (voice "Louie the Legend": whispering, panicking)
voice/raw/claude1.mp3  Claude, every line in one read (voice "Ivy": low, close, unhurried)
voice/raw/words_<take>.json is each take's ElevenLabs Scribe alignment (per-word start/end in s). A line is cut from its
first word to its last (plus a breath either side); pauses inside a line are held to KEEP so the "..." beats stay but
don't drag. The lines are laid end to end with the GAP before each: short in the back-and-forth, long where the scene
needs the silence (the blackout before the snapshot, the restore, the black before the CTA). No speed-up: the dread
needs the space. Each take is loudness-matched, the mix normalised to -17 LUFS (quiet, close voices).

Writes assets/audio/voice.wav (48 kHz mono), build/words.json (w, s, e, line, who) and voice/lines.json.
"""
import json
import os
import re
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice")
SR = 48000
KEEP = .26
TEMPO = 1.08                                      # a touch faster, pitch kept (ffmpeg atempo)
LEAD = .62                                        # the hook's Enter key and "rows deleted" come before the first word
# (take, text, gap before[, first word kept]) in story order; each take's lines must appear in its read in this order.
# Gaps are before the speed-up.
LINES = [
    ("dev1", "Claude... tell me that didn't just run.", LEAD),
    ("claude1", "It ran.", .3),
    ("dev1", "How much is gone?", .32),
    ("claude1", "All of it. One point two million rows.", .3),
    ("dev1", "Okay. Okay. The backup. There's always a backup.", .28, 2),      # read from "The backup."
    ("claude1", "The backup job stopped in March. No one checked.", .32),
    ("dev1", "Nine hundred people are using it. Right now.", .32),
    ("claude1", "...I know.", .42),
    ("claude1", "Before you told me to \"clean things up\"... I took a snapshot.", 1.25),
    ("dev1", "...Why would you do that?", .3),
    ("claude1", "Because the last time you said \"clean things up\"... it was a Friday.", .32),
    ("claude1", "Restoring now.", .38),
    ("dev1", "...Thank you.", .7),
    ("claude1", "One more thing. I've revoked your production access.", .38),
    ("claude1", "Comment BACKUP... and I'll send you the setup that saved him.", .85),
]
WHO = {"dev1": "dev", "claude1": "claude"}


def run(*a, **k):
    return subprocess.run(a, capture_output=True, check=True, **k)


def norm(s):
    return re.sub(r"[^a-z0-9']", "", s.lower())


def load(take):
    raw = run("ffmpeg", "-v", "error", "-i", os.path.join(V, "raw", take + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-").stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def cut(x, a, b, words):
    """Samples a..b (s) with pauses longer than KEEP held to KEEP; returns (samples, [(w, s, e)] relative to the cut)."""
    seg = x[int(a * SR):int(b * SR)].copy()
    hop = SR // 100
    n = len(seg) // hop
    db = 20 * np.log10(np.sqrt(np.mean(seg[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    quiet = db < -40
    cuts, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            s0, s1 = i * hop / SR, j * hop / SR
            if s1 - s0 > KEEP and s0 > .1 and s1 < len(seg) / SR - .1:
                m = (s0 + s1) / 2
                cuts.append((m - (s1 - s0 - KEEP) / 2, m + (s1 - s0 - KEEP) / 2))
            i = j
        else:
            i += 1
    mask = np.ones(len(seg), bool)
    f = int(.008 * SR)
    for c0, c1 in cuts:
        i0, i1 = int(c0 * SR), int(c1 * SR)
        mask[i0:i1] = False
        if i0 - f > 0:
            seg[i0 - f:i0] *= np.linspace(1, 0, f)
        if i1 + f < len(seg):
            seg[i1:i1 + f] *= np.linspace(0, 1, f)
    fe = int(.03 * SR)
    seg[:fe] *= np.linspace(0, 1, fe); seg[-fe:] *= np.linspace(1, 0, fe)
    mapt = lambda t: t - sum(min(t, c1) - c0 for c0, c1 in cuts if t > c0)  # noqa: E731
    return seg[mask], [(w["text"], mapt(w["start"] - a), mapt(w["end"] - a)) for w in words]


def main():
    takes = {t: load(t) for t in WHO}
    words = {t: json.load(open(os.path.join(V, "raw", f"words_{t}.json"))) for t in WHO}
    idx = {t: 0 for t in WHO}

    def vrms(y):
        fr = np.sqrt(np.mean(y[: len(y) // 480 * 480].reshape(-1, 480) ** 2, axis=1))
        return np.sqrt(np.mean(fr[fr > .3 * fr.max()] ** 2))
    gain = {t: 1 / vrms(takes[t]) for t in WHO}
    parts, outw, lines, t0 = [], [], [], 0.0
    for li, (take, text, gap, *first) in enumerate(LINES):
        n = len(text.split())
        ws = words[take][idx[take]:idx[take] + n]; idx[take] += n
        if [norm(w["text"]) for w in ws] != [norm(w) for w in text.split()]:
            raise SystemExit(f"line {li + 1} ({take}) doesn't match its read:\n  {text}\n  " + " ".join(w["text"] for w in ws))
        k0 = first[0] if first else 0
        ws, text = ws[k0:], " ".join(text.split()[k0:])
        a, b = max(0, ws[0]["start"] - .12), min(len(takes[take]) / SR, ws[-1]["end"] + .25)
        y, mw = cut(takes[take], a, b, ws)
        parts.append(np.zeros(int(gap * SR))); t0 += gap
        parts.append(y * gain[take] * .1)
        for (w, s, e), src in zip(mw, text.split()):
            outw.append({"line": li + 1, "who": WHO[take], "w": src, "s": round((t0 + s) / TEMPO, 3), "e": round((t0 + e) / TEMPO, 3)})
        lines.append({"line": li + 1, "who": WHO[take], "text": text, "start": round((t0 + mw[0][1]) / TEMPO, 3), "end": round((t0 + mw[-1][2]) / TEMPO, 3)})
        t0 += len(y) / SR
    y = np.concatenate(parts + [np.zeros(int(.3 * SR))])
    tight = os.path.join(V, "dialogue.f32")
    y.astype(np.float32).tofile(tight)
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    out = os.path.join(ROOT, "assets", "audio", "voice.wav")
    run("ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tight,
        "-af", f"atempo={TEMPO},loudnorm=I=-17:TP=-1.5:LRA=14", "-ar", str(SR), "-ac", "1", out)
    os.remove(tight)
    json.dump(outw, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    json.dump({"duration": round(len(y) / SR / TEMPO, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    print(f"voice.wav {len(y) / SR / TEMPO:.2f} s")
    for l in lines:
        print(f"  {l['start']:6.2f}-{l['end']:6.2f}  {l['who']:6s} {l['text']}")


if __name__ == "__main__":
    main()
