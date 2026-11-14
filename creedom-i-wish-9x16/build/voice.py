"""Timeline for the Creedom "I Wish..." reel: the creator's picked takes (voice/el/<take>.wav, see build/pick.py) laid end
to end with Cree's beats between them (the half reveals, the hero entrance, his speech clouds), and the word timing for
the captions. Writes assets/audio/voice.wav (-16 LUFS), build/cues.json and build/words.json.
python3 build/voice.py      (from the project root; needs numpy, soundfile, ffmpeg)
"""
import json
import os
import re
import subprocess

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
TEMPO = 1.05           # Chatterbox speaks a touch slowly; 5% faster, pitch unchanged
TEXT = {               # caption text per take (what the creator says)
    "01": "My latest reel... got 42 views.",
    "02": "I used trending audio! I posted at 7 AM! I even changed my hair!",
    "03": "And still... nothing.",
    "04": "I wish someone could review my reel... before I post it.",
    "05": "I wish it could look at my old reels... and tell me what actually worked.",
    "06": "And I wish it could just set up my DM automation for me.",
    "07": "Whoa!",
    "08": "That's... actually it.",
    "09": "I forgot I even made that!",
    "10": "Where have you been all my life?",
    "11": "Comment CREEDOM, and I'll send you the link.",
}
# the reel, in order: ("L", take, gap after) for a creator line, ("B", name, seconds) for a beat without him talking
EVENTS = [
    ("B", "lead", .35), ("L", "01", 0), ("B", "slide", .55), ("L", "02", .1), ("B", "thud", .45), ("L", "03", .35),
    ("L", "04", .2), ("B", "reveal1", 2.5), ("L", "05", .15), ("B", "reveal2", 2.4), ("L", "06", .1),
    ("B", "hero", 2.2), ("L", "07", 0), ("B", "say", 1.7),
    ("B", "fix1", 2.7), ("L", "08", .15), ("B", "fix2", 2.4), ("L", "09", .1), ("B", "fix3", 3.0),
    ("L", "10", 0), ("B", "ask", 1.7), ("B", "endin", .25), ("L", "11", 0), ("B", "tail", 1.6),
]


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    return max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith(("le", "ee")) and len(w) > 3 else 0))


def trim(x, thr=-52):
    hop = SR // 200
    n = len(x) // hop
    env = 20 * np.log10(np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    idx = np.flatnonzero(env > max(thr, env.max() - 48))
    a_, b_ = max(0, idx[0] - 10), min(n, idx[-1] + 20)
    y = x[a_ * hop: b_ * hop].copy()
    f = int(.015 * SR); y[:f] *= np.linspace(0, 1, f) ** 2
    f = int(.05 * SR); y[-f:] *= np.linspace(1, 0, f)
    return y


def level(x, target=-20.0):
    hop = SR // 100
    n = len(x) // hop
    fr = x[: n * hop].reshape(n, hop)
    db = 20 * np.log10(np.sqrt(np.mean(fr ** 2, axis=1)) + 1e-9)
    act = fr[db > db.max() - 30]
    return x * 10 ** ((target - 20 * np.log10(np.sqrt(np.mean(act ** 2)) + 1e-9)) / 20)


def main():
    t, out, cues, words = 0.0, [], {"lines": {}, "beats": {}}, []
    for kind, name, v in EVENTS:
        if kind == "B":
            cues["beats"][name] = [round(t, 3), round(t + v, 3)]
            t += v
            continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "voice", "el", f"{name}.wav"), "-af", f"atempo={TEMPO}",
                              "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        a = level(trim(np.frombuffer(raw, np.float32).astype(np.float64)))
        d = len(a) / SR
        out.append((t, a))
        cues["lines"][name] = [round(t, 3), round(t + d, 3)]
        ws = TEXT[name].split()
        wt = np.array([syl(w) + .35 for w in ws]); c = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
        for j, w in enumerate(ws):
            words.append({"take": name, "w": w, "s": round(t + d * c[j] - .02, 3), "e": round(t + d * c[j + 1], 3)})
        print(f"  {t:6.2f}-{t + d:6.2f}  {TEXT[name]}")
        t += d + v
    cues["end"] = round(t, 3)
    mix = np.zeros(int(t * SR) + SR)
    for st, a in out:
        i0 = int(st * SR); mix[i0:i0 + len(a)] += a
    mix = mix[: int(t * SR)]
    tmp = os.path.join(ROOT, "assets", "audio", "voice_raw.wav")
    sf.write(tmp, (mix / np.max(np.abs(mix)) * .8).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1",
                    os.path.join(ROOT, "assets", "audio", "voice.wav")], check=True)
    os.remove(tmp)
    json.dump(cues, open(os.path.join(ROOT, "build", "cues.json"), "w"), indent=1)
    json.dump(words, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    print(f"voice.wav {t:.2f} s")


if __name__ == "__main__":
    main()
