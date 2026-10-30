"""The voiceover: tighten the pauses of the read and time every word.

python3 build/voice.py      (from the project root; needs numpy, soundfile and ffmpeg)

voice/raw/v4_stacey_b.mp3 is the chosen ElevenLabs read: voice "Stacey - Bright, Energetic, Expressive", Eleven v4,
with emotion tags (dramatic, whispered "forever", a gasp on "Wait", laughs, a shouted "Steam Deck"). It was picked from
four v4 takes (two Stacey, two Hallie) as the most expressive (pitch range 18 semitones against 6.6 for the first,
flatter v3 read in take1.mp3). voice/raw/words_v4_stacey_b.json holds its ElevenLabs Scribe word times. Every silence
is held to at most CAP, or LINE_CAP between lines, with a few dramatic pauses kept longer (KEEP); word times move with
the audio. Writes assets/audio/voice.wav (48 kHz mono, -16 LUFS), build/words.json and voice/lines.json.
"""
import json
import os
import re
import subprocess

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
CAP = .3          # longest pause kept inside a line
LINE_CAP = .46     # longest pause kept between lines
LEAD = .08         # silence before the first word
KEEP = {9: .5, 11: .32, 56: .42}   # dramatic pauses kept longer: before "forever", after "Wait,", after "Boss fight."
LINES = [
    "Your favorite PS2 game is about to time out forever.",
    "Wait, player two just joined. It's Claude.",
    "It's called Console Skill. 11 free skills that rebuild PS2 games you own as real PC games, not an emulator.",
    "Grab the powerups. Mod it just by asking. Sharper graphics, new levels, your own controller.",
    "Game crashes? Boss fight. The tester skill finds out why.",
    "Then New Game Plus. Play it on Windows, Mac, Linux, even a Steam Deck.",
    "It's still early access, so not every game boots yet.",
    "Comment console to continue, and I'll send you the link",
]


def run(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True)


def silences(path):
    err = run("ffmpeg", "-i", path, "-af", "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-").stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(st, en))


def gaps(words):
    """Pauses from the word times themselves, so quiet breaths that silencedetect misses still get shortened."""
    return [(words[i]["e"] + .04, words[i + 1]["s"] - .04) for i in range(len(words) - 1) if words[i + 1]["s"] - words[i]["e"] > .3]


def main():
    raw = os.path.join(ROOT, "voice", "raw", "v4_stacey_b.mp3")
    words = json.load(open(os.path.join(ROOT, "voice", "raw", "words_v4_stacey_b.json")))
    n = sum(len(ln.split()) for ln in LINES)
    assert len(words) == n, (len(words), n)
    line_of, k = [], 0
    for li, ln in enumerate(LINES):
        for w in ln.split():
            assert re.sub(r"\W", "", words[k]["w"].lower()) == re.sub(r"\W", "", w.lower()), (words[k], w)
            line_of.append(li); k += 1
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", raw, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32)
    ends = {i for i in range(len(words) - 1) if line_of[i] != line_of[i + 1]}
    first = max(0, words[0]["s"] - LEAD)
    # merge detected silences with word gaps, then shrink each to its cap
    spans = sorted(silences(raw) + gaps(words))
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    cuts = []
    for a, b in merged:
        if b <= first or a >= words[-1]["e"]:
            continue
        # never cut into a word
        if any(w["s"] < b and w["e"] > a for w in words):
            continue
        mid = (a + b) / 2
        between = any(words[i]["e"] - .15 <= mid <= words[i + 1]["s"] + .15 for i in ends)
        cap = LINE_CAP if between else CAP
        for i, c in KEEP.items():
            if abs(words[i]["s"] - b) < .12:
                cap = c
        if b - a > cap:
            cuts.append((a + cap / 2, b - cap / 2))
    segs, t = [], first
    for a, b in cuts:
        segs.append((t, a)); t = b
    end = min(len(x) / SR, words[-1]["e"] + .5)
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

    def piece(a, b):
        p = x[int(a * SR):int(b * SR)].copy()
        p[:f] *= ramp; p[-f:] *= ramp[::-1]
        return p

    y = np.concatenate([piece(a, b) for a, b in segs])
    tmp = os.path.join(ROOT, "assets", "audio", "voice_raw.wav")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    sf.write(tmp, y, SR, subtype="FLOAT")
    out = os.path.join(ROOT, "assets", "audio", "voice.wav")
    run("ffmpeg", "-y", "-i", tmp, "-af", "highpass=f=80,loudnorm=I=-16:TP=-2:LRA=9", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s24le", out)
    os.remove(tmp)
    W = [{"w": w["w"], "s": round(tmap(w["s"]), 3), "e": round(tmap(w["e"]), 3), "line": line_of[i] + 1} for i, w in enumerate(words)]
    json.dump(W, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    lines = []
    for li, ln in enumerate(LINES):
        ws = [w for w in W if w["line"] == li + 1]
        lines.append({"text": ln, "start": ws[0]["s"], "end": ws[-1]["e"]})
    json.dump({"source": "voice/raw/v4_stacey_b.mp3", "lines": lines}, open(os.path.join(ROOT, "voice", "lines.json"), "w"), indent=1)
    print(f"voice {len(y) / SR:.2f} s (source {len(x) / SR:.2f} s), {len(cuts)} pauses shortened")
    for ln in lines:
        print(f"  {ln['start']:6.2f} {ln['end']:6.2f}  {ln['text'][:70]}")


if __name__ == "__main__":
    main()
