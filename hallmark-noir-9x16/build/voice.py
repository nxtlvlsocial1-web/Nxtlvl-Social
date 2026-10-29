"""The voiceover: tighten the pauses of the noir read and time every word.

python3 build/voice.py      (from the project root; needs numpy, soundfile and ffmpeg)

voice/raw/take1.mp3 is one ElevenLabs read (voice "Drag Jackson", Eleven v4, a slow 1940s film-noir detective) of the
nine LINES. voice/raw/words_take1.json holds its ElevenLabs Scribe word times, delivery tags removed. Every silence
(ffmpeg silencedetect, -40 dB, at least 0.18 s) is held to at most CAP, or LINE_CAP where one line ends and the next
begins, so the read keeps its noir pacing without dead air; word times are moved with the audio. Writes
assets/audio/voice.wav (48 kHz mono, -16 LUFS), build/words.json and voice/lines.json.
"""
import json
import os
import re
import subprocess

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
CAP = .34          # longest pause kept inside a line
LINE_CAP = .5      # longest pause kept between lines
LEAD = .15         # silence before the first word
LINES = [
    "It was a rainy night. She walked in alone, holding a website Claude had built her.",
    "It looked fine. That was the problem. It looked like every other one in town.",
    "Two million users nobody counted. Reviews from people who don't exist. Labels shouting in capitals.",
    "Claude wasn't the culprit. Its defaults were.",
    "So I called a specialist. Hallmark. A free design skill for Claude Code.",
    "It deals a real design, then checks it against every AI giveaway in the book.",
    "Same prompt. Same Claude.",
    "No fake numbers. No fake reviews. This time, it looked designed. Not generated.",
    "Comment HALLMARK and I'll send you the install. Case closed.",
]


def run(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True)


def silences(path):
    err = run("ffmpeg", "-i", path, "-af", "silencedetect=noise=-40dB:d=0.18", "-f", "null", "-").stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(st, en))


def main():
    raw = os.path.join(ROOT, "voice", "raw", "take1.mp3")
    words = json.load(open(os.path.join(ROOT, "voice", "raw", "words_take1.json")))
    n = sum(len(ln.split()) for ln in LINES)
    assert len(words) == n, (len(words), n)
    line_of, k = [], 0
    for li, ln in enumerate(LINES):
        for w in ln.split():
            assert re.sub(r"\W", "", words[k]["w"].lower()) == re.sub(r"\W", "", w.lower()), (words[k], w)
            line_of.append(li); k += 1
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", raw, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32)
    # line boundaries: the gap after each line's last word
    ends = {i for i in range(len(words) - 1) if line_of[i] != line_of[i + 1]}
    # build the cut list: keep everything, shrink each silence to its cap
    first = max(0, words[0]["s"] - LEAD)
    cuts = []   # (src_start, src_end) of silence stretches to shorten, with the length to keep
    for a, b in silences(raw):
        if b <= first or a >= words[-1]["e"]:
            continue
        mid = (a + b) / 2
        between = any(words[i]["e"] - .15 <= mid <= words[i + 1]["s"] + .15 for i in ends)
        cap = LINE_CAP if between else CAP
        if b - a > cap:
            cuts.append((a + cap / 2, b - cap / 2))
    # map source time to output time
    segs, t = [], first
    for a, b in cuts:
        segs.append((t, a)); t = b
    end = min(len(x) / SR, words[-1]["e"] + .6)
    segs.append((t, end))

    def tmap(s):
        out = 0.0
        for a, b in segs:
            if s <= a:
                return out
            if s <= b:
                return out + s - a
            out += b - a
        return out

    f = int(.006 * SR)
    ramp = np.linspace(0, 1, f)

    def piece(a, b):   # each kept stretch with tiny fades, so no splice clicks
        p = x[int(a * SR):int(b * SR)].copy()
        p[:f] *= ramp; p[-f:] *= ramp[::-1]
        return p

    y = np.concatenate([piece(a, b) for a, b in segs])
    tmp = os.path.join(ROOT, "assets", "audio", "voice_raw.wav")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    sf.write(tmp, y, SR, subtype="FLOAT")
    out = os.path.join(ROOT, "assets", "audio", "voice.wav")
    run("ffmpeg", "-y", "-i", tmp, "-af", "highpass=f=70,loudnorm=I=-16:TP=-2:LRA=9", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s24le", out)
    os.remove(tmp)
    W = [{"w": w["w"], "s": round(tmap(w["s"]), 3), "e": round(tmap(w["e"]), 3), "line": line_of[i] + 1} for i, w in enumerate(words)]
    json.dump(W, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    lines = []
    for li, ln in enumerate(LINES):
        ws = [w for w in W if w["line"] == li + 1]
        lines.append({"text": ln, "start": ws[0]["s"], "end": ws[-1]["e"]})
    json.dump({"source": "voice/raw/take1.mp3", "lines": lines}, open(os.path.join(ROOT, "voice", "lines.json"), "w"), indent=1)
    print(f"voice {len(y) / SR:.2f} s (source {len(x) / SR:.2f} s), {len(cuts)} pauses shortened")
    for ln in lines:
        print(f"  {ln['start']:6.2f} {ln['end']:6.2f}  {ln['text'][:60]}")


if __name__ == "__main__":
    main()
