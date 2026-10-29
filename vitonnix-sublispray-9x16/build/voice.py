"""Tighten the ElevenLabs voiceover (Eleven v4, voice "Kangana - Candid, Warm, Engaging") and map its word timings.

python3 build/voice.py      (from the project root; needs numpy and ffmpeg)

Input: voice/raw/take1.mp3 and voice/raw/words_take1.json (ElevenLabs Scribe, per-word start/end in seconds).
Every pause is shortened to KEEP seconds (a few beats keep more), the result is sped up by TEMPO with the pitch
kept (ffmpeg atempo) and normalised to -16 LUFS. Every word time goes through the same cut map and tempo, so the
captions stay on the words.

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
TEMPO = 1.06
KEEP = .14
LONG = {"vitamins?": .30, "swallow.": .26, "done.": .30, "aftertaste.": .26, "biotin.": .22, "you.": .26, "uk.": .26, "g.": .30}
LEAD = .08
LINES = [
    "Still swallowing your vitamins?",
    "Meet Vitonnix SubliSpray.",
    "Vitamins you spray, not swallow.",
    "Two quick sprays under your tongue, and you're done.",
    "No pills. No water. No chalky aftertaste.",
    "Vitamin D. B12. Biotin.",
    "One little bottle each, wherever your day takes you.",
    "Created by three doctors. Developed in the UK.",
    "Available now on Tata 1 M G.",
    "Comment SPRAY, and we'll DM you the link.",
]


def run(*a, **k):
    return subprocess.run(a, capture_output=True, check=True, **k)


def norm(s):
    return re.sub(r"[^a-z0-9']", "", s.lower())


def main():
    raw = run("ffmpeg", "-v", "error", "-i", os.path.join(V, "raw", "take1.mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-").stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)
    words = [w for w in json.load(open(os.path.join(V, "raw", "words_take1.json"))) if w.get("type", "word") == "word" and norm(w["text"])]
    end = min(len(x) / SR, words[-1]["end"] + .2)
    x = x[:int(end * SR)]
    # silences from the signal: 10 ms frames under -38 dBFS for 120 ms or more
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
            if j - i >= 12:
                sil.append((i * hop / SR, j * hop / SR))
            i = j
        else:
            i += 1
    # how much silence to keep after the word that precedes each gap
    cuts = []  # (start, end) of removed audio, in source time
    for a, b in sil:
        prev = [w for w in words if w["end"] <= a + .05]
        keep = KEEP
        if prev:
            keep = LONG.get(norm_punct(prev[-1]["text"]), KEEP)
        if a < .01:                       # leading silence: keep LEAD
            keep = LEAD
        if b - a > keep:
            cuts.append((a + keep / 2 if a > .01 else b - keep, b - keep / 2 if a > .01 else b))
    cuts = [(c0, c1) for c0, c1 in cuts if c1 > c0]
    # build the cut audio and the time map
    pieces, t = [], 0.0
    segs = []  # (src_start, src_end, dst_start)
    for c0, c1 in cuts:
        segs.append((t, c0, None))
        t = c1
    segs.append((t, len(x) / SR, None))
    out, dst = [], 0.0
    mapped = []
    for s0, s1, _ in segs:
        out.append(x[int(s0 * SR):int(s1 * SR)])
        mapped.append((s0, s1, dst))
        dst += s1 - s0
    y = np.concatenate(out)

    def mapt(ts):
        for s0, s1, d in mapped:
            if ts <= s1 + 1e-6:
                return d + max(0.0, ts - s0)
        return dst

    y = y / (np.max(np.abs(y)) + 1e-9) * .9
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    tmp = os.path.join(ROOT, "assets", "audio", "_cut.wav")
    run("ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-", tmp, input=y.astype(np.float32).tobytes())
    outp = os.path.join(ROOT, "assets", "audio", "voice.wav")
    run("ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=9", "-ar", str(SR), "-ac", "1", outp)
    os.remove(tmp)
    dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", outp).stdout.decode().strip())

    # words -> lines, by matching the script in order
    script = [(li, norm(w)) for li, line in enumerate(LINES, 1) for w in line.split()]
    outw, k = [], 0
    for w in words:
        nw = norm(w["text"])
        if k < len(script) and (script[k][1] == nw or script[k][1].startswith(nw) or nw.startswith(script[k][1])):
            line = script[k][0]
            k += 1
        elif k < len(script) and k + 1 < len(script) and script[k + 1][1] == nw:   # aligner split or merged a token
            k += 1
            line = script[k][0]
            k += 1
        else:
            line = outw[-1]["line"] if outw else 1
        outw.append({"w": w["text"], "s": round(mapt(w["start"]) / TEMPO, 3), "e": round(mapt(w["end"]) / TEMPO, 3), "line": line})
    if k < len(script):
        print("WARNING: script words not all matched; unmatched from", script[k])
    json.dump(outw, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=1)
    lines = []
    for li, text in enumerate(LINES, 1):
        ws = [w for w in outw if w["line"] == li]
        lines.append({"line": li, "text": text, "start": ws[0]["s"], "end": ws[-1]["e"]})
    json.dump({"duration": round(dur, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    print(f"voice.wav {dur:.2f}s; cut {sum(c1 - c0 for c0, c1 in cuts):.2f}s of pauses; {len(outw)} words")
    for ln in lines:
        print(f"  {ln['start']:6.2f}-{ln['end']:6.2f}  {ln['text']}")


def norm_punct(s):
    return re.sub(r"[^a-z0-9'?.!]", "", s.lower())


if __name__ == "__main__":
    main()
