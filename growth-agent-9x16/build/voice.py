"""Tighten the ElevenLabs voiceover and map its word timings (Eleven v4, voice "Matt - Natural, Authentic, Engaging").

python3 build/voice.py      (from the project root; needs numpy and ffmpeg with rubberband)

voice/raw/take2.mp3 is the picked take of the full script in one read; voice/raw/words_take2.json is its ElevenLabs Scribe
alignment (per-word start/end in s). Every pause is shortened to KEEP (the "And five?" beat and the "results..." hold
keep a little more), the read is sped up by TEMPO with the pitch kept, and loudness-matched to -16 LUFS. Every word time
goes through the same cut map and tempo, so the captions stay on the words.

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
# the script, one entry per caption line (the words must match the take's words in order)
LINES = [
    "I turned Claude into an Instagram growth agent...",
    "and it took my page from three thirty-nine to twenty-four hundred followers.",
    "It doesn't just post. It grows your page.",
    "Five moves. The last one's the smartest.",
    "One: it spots what's blowing up in your niche.",
    "Two: it plans the visuals.",
    "Three: it writes the script and the caption.",
    "Four: it replies to your comments.",
    "And five?",
    "It studies every reel's results... and rewrites your next one.",
    "Bonus: a free viral reels course. Sixteen thousand downloads.",
    "Comment AGENT, and I'll send you my setup... plus the course.",
]


def run(*a, **k):
    return subprocess.run(a, capture_output=True, check=True, **k)


def main():
    raw = run("ffmpeg", "-v", "error", "-i", os.path.join(V, "raw", "take2.mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-").stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)
    words = [w for w in json.load(open(os.path.join(V, "raw", "words_take2.json"))) if not w["text"].startswith("[") and not w["text"].endswith("]")]
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
    # cut each silence down to its keep length; the cut sits in the middle of the silence
    cuts = []                                   # (start, end) of removed audio, in source seconds
    for a, b in sil:
        if a < .05:                              # leading silence: drop to LEAD
            cuts.append((0, max(0, b - LEAD))); continue
        prev = max((w for w in words if w["start"] < a), key=lambda w: w["start"], default=None)
        keep = LONG.get(prev["text"], KEEP) if prev else KEEP
        if b - a > keep:
            m = (a + b) / 2
            cuts.append((m - (b - a - keep) / 2, m + (b - a - keep) / 2))
    if words[-1]["end"] < len(x) / SR - .3:
        cuts.append((words[-1]["end"] + .25, len(x) / SR))

    def mapt(t):
        removed = sum(min(t, b) - a for a, b in cuts if t > a)
        return (t - removed) / TEMPO

    keep_mask = np.ones(len(x), bool)
    for a, b in cuts:
        keep_mask[int(a * SR):int(b * SR)] = False
    # 8 ms fades either side of every splice, so the joins don't click
    y = x.copy()
    f = int(.008 * SR)
    for a, b in cuts:
        ia, ib = int(a * SR), int(b * SR)
        if ia - f > 0:
            y[ia - f:ia] *= np.linspace(1, 0, f)
        if ib + f < len(y):
            y[ib:ib + f] *= np.linspace(0, 1, f)
    y = y[keep_mask]
    tight = os.path.join(V, "tight.f32")
    y.astype(np.float32).tofile(tight)
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    out = os.path.join(ROOT, "assets", "audio", "voice.wav")
    run("ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tight,
        "-af", f"rubberband=tempo={TEMPO}:pitchq=quality:formant=preserved,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1", out)
    os.remove(tight)
    dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out, text=True).stdout)
    # words -> lines
    norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
    seq = [w for ln in LINES for w in ln.split()]
    if [norm(w["text"]) for w in words] != [norm(w) for w in seq]:
        raise SystemExit("take words don't match the script:\n" + " ".join(w["text"] for w in words))
    outw, k, lines = [], 0, []
    for li, ln in enumerate(LINES):
        ws = ln.split()
        for w in ws:
            src = words[k]; k += 1
            outw.append({"line": li + 1, "w": w, "s": round(mapt(src["start"]), 3), "e": round(mapt(src["end"]), 3)})
        mine = [w for w in outw if w["line"] == li + 1]
        lines.append({"line": li + 1, "text": ln, "start": mine[0]["s"], "end": mine[-1]["e"]})
    json.dump(outw, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    json.dump({"duration": round(dur, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    print(f"voice.wav {dur:.2f} s ({len(x) / SR:.2f} s raw, {len(cuts)} cuts, tempo {TEMPO})")
    for l in lines:
        print(f"  {l['start']:6.2f}-{l['end']:6.2f}  {l['text']}")


if __name__ == "__main__":
    main()
