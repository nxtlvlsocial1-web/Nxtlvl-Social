"""Tighten the ElevenLabs voiceover and map its word timings (Eleven v4, voice "Matt - Natural, Authentic, Engaging").

python3 build/voice.py      (from the project root; needs numpy and ffmpeg with rubberband)

Two takes, each with its ElevenLabs Scribe alignment (voice/raw/words_<take>.json, per-word start/end in s):
  take2  the full script in one read; lines 1-10 are used (the bonus line and the old CTA are cut after "next one.")
  cta1   the CTA on its own: "Comment AGENT, and I'll send you my whole setup."
In each take every pause is shortened to KEEP (the "And five?" beat and the "results..." hold keep a little more); the
pieces are loudness-matched, joined with a GAP, sped up by TEMPO with the pitch kept and normalised to -16 LUFS. Every
word time goes through the same cut map and tempo, so the captions stay on the words.

Writes assets/audio/voice.wav (48 kHz mono), build/words.json (w, s, e, line) and voice/lines.json.
"""
import json
import os
import re
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice")
SR = 48000
TEMPO = 1.13
KEEP = .11
LONG = {"five?": .34, "results...": .18, "smartest.": .2, "followers.": .14}       # pauses after these words keep more
LEAD = .06
GAP = .34                                     # between "next one." and the CTA, before the tempo change
# the script, one entry per caption line, and the take each line comes from (the words must match the take's, in order)
LINES = [
    ("take2", "I turned Claude into an Instagram growth agent..."),
    ("take2", "and it took my page from three thirty-nine to twenty-four hundred followers."),
    ("take2", "It doesn't just post. It grows your page."),
    ("take2", "Five moves. The last one's the smartest."),
    ("take2", "One: it spots what's blowing up in your niche."),
    ("take2", "Two: it plans the visuals."),
    ("take2", "Three: it writes the script and the caption."),
    ("take2", "Four: it replies to your comments."),
    ("take2", "And five?"),
    ("take2", "It studies every reel's results... and rewrites your next one."),
    ("cta1", "Comment AGENT, and I'll send you my whole setup."),
]


def run(*a, **k):
    return subprocess.run(a, capture_output=True, check=True, **k)


def norm(s):
    return re.sub(r"[^a-z0-9']", "", s.lower())


def tighten(take, n_words):
    """The take's first n_words words with every pause shortened: (samples, [(word, start, end)] in the new time)."""
    raw = run("ffmpeg", "-v", "error", "-i", os.path.join(V, "raw", take + ".mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-").stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)
    words = json.load(open(os.path.join(V, "raw", f"words_{take}.json")))[:n_words]
    end = min(len(x) / SR, words[-1]["end"] + .18)
    x = x[:int(end * SR)]
    # silences from the signal (10 ms frames under -38 dBFS for 100 ms or more), not from the aligner's word ends
    hop = SR // 100
    n = len(x) // hop
    db = 20 * np.log10(np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    quiet = db < -38
    sil, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if j - i >= 10:
                sil.append((i * hop / SR, j * hop / SR))
            i = j
        else:
            i += 1
    cuts = []                                   # (start, end) of removed audio, in source seconds
    for a, b in sil:
        if a < .05:                              # leading silence: drop to LEAD
            cuts.append((0, max(0, b - LEAD))); continue
        prev = max((w for w in words if w["start"] < a), key=lambda w: w["start"], default=None)
        keep = LONG.get(prev["text"], KEEP) if prev else KEEP
        if b - a > keep:
            m = (a + b) / 2
            cuts.append((m - (b - a - keep) / 2, m + (b - a - keep) / 2))

    def mapt(t):
        return t - sum(min(t, b) - a for a, b in cuts if t > a)

    mask = np.ones(len(x), bool)
    f = int(.008 * SR)
    y = x.copy()
    for a, b in cuts:                            # 8 ms fades either side of every splice, so the joins don't click
        ia, ib = int(a * SR), int(b * SR)
        mask[ia:ib] = False
        if ia - f > 0:
            y[ia - f:ia] *= np.linspace(1, 0, f)
        if ib + f < len(y):
            y[ib:ib + f] *= np.linspace(0, 1, f)
    fo = int(.04 * SR)
    y[-fo:] *= np.linspace(1, 0, fo)
    return y[mask], [(w["text"], mapt(w["start"]), mapt(w["end"])) for w in words]


def main():
    takes = []
    for take in dict.fromkeys(t for t, _ in LINES):
        n = sum(len(ln.split()) for t, ln in LINES if t == take)
        y, ws = tighten(take, n)
        script = [w for t, ln in LINES if t == take for w in ln.split()]
        if [norm(w) for w, _, _ in ws] != [norm(w) for w in script]:
            raise SystemExit(f"{take}: words don't match the script:\n" + " ".join(w for w, _, _ in ws))
        takes.append((take, y, ws))
    # match the pieces' loudness (voiced frames only), then join them
    def vrms(y):
        fr = np.sqrt(np.mean(y[: len(y) // 480 * 480].reshape(-1, 480) ** 2, axis=1))
        return np.sqrt(np.mean(fr[fr > .3 * fr.max()] ** 2))
    ref = vrms(takes[0][1])
    parts, offs, t0 = [], {}, 0.0
    for k, (take, y, ws) in enumerate(takes):
        y = y * (ref / vrms(y))
        if k:
            parts.append(np.zeros(int(GAP * SR))); t0 += GAP
        offs[take] = t0
        parts.append(y); t0 += len(y) / SR
    tight = os.path.join(V, "tight.f32")
    np.concatenate(parts).astype(np.float32).tofile(tight)
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    out = os.path.join(ROOT, "assets", "audio", "voice.wav")
    run("ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tight,
        "-af", f"rubberband=tempo={TEMPO}:pitchq=quality:formant=preserved,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1", out)
    os.remove(tight)
    dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out, text=True).stdout)
    outw, lines, idx = [], [], {t: 0 for t, _, _ in takes}
    tw = {t: ws for t, _, ws in takes}
    for li, (take, ln) in enumerate(LINES):
        for w in ln.split():
            _, s, e = tw[take][idx[take]]; idx[take] += 1
            outw.append({"line": li + 1, "w": w, "s": round((s + offs[take]) / TEMPO, 3), "e": round((e + offs[take]) / TEMPO, 3)})
        mine = [w for w in outw if w["line"] == li + 1]
        lines.append({"line": li + 1, "text": ln, "start": mine[0]["s"], "end": mine[-1]["e"]})
    json.dump(outw, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    json.dump({"duration": round(dur, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    print(f"voice.wav {dur:.2f} s (tempo {TEMPO})")
    for l in lines:
        print(f"  {l['start']:6.2f}-{l['end']:6.2f}  {l['text']}")


if __name__ == "__main__":
    main()
