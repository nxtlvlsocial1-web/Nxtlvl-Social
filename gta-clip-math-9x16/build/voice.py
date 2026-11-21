"""Voiceover for gta-clip-math-9x16, and the timing everything else follows.

python3 build/voice.py        (from the project root)

Needs: ffmpeg, numpy, the HyperFrames CLI, and Kokoro for the voice: a Python with `pip install kokoro-onnx soundfile`,
named by HYPERFRAMES_PYTHON (the CLI's local TTS). Word timestamps come from `npx hyperframes transcribe` (local Whisper).

1. Voices each script line with Kokoro (voice am_michael, the owner's pick), trims the silence around it and
   transcribes it for word timestamps.
2. Lays the lines out at a natural pace. Each scene now starts just before its line, and gets at least ~70% of its
   original length so the animation still reads.
3. Writes a time warp (old animation time <-> new time) with knots at every scene cut and at the key hits (the $225
   slam on "two hundred twenty-five", the cap on "capped", $900 and 4x on their words...). index.html, scene3d.js and
   build/sfx.py all read it, so the animation keeps its authored times and is retimed to the voice as a whole.
4. Writes assets/audio/voice.wav, build/timing.json, assets/js/timing.js, assets/js/captions.js and captions.srt
   (captions use the approved script words, timed to the spoken words).
"""
import difflib
import json
import os
import re
import subprocess
import tempfile
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE, SPEED, SR = "am_michael", 1.16, 24000
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1")

# old scene windows (the animation's authored times) and each scene's line.
# tts: what Kokoro reads; cap: the caption markup (groups split on |, * = accent word, {display=spoken}).
OLD = [0, 3, 5, 7, 11, 15, 18, 21, 23, 28, 32, 34, 37, 39.62]
OLD_END = 40.0
LINES = [
    ("A million-view G T A 6 clip pays two hundred twenty-five dollars.", "A million-view | {GTA=gee tee ay} {6=six} clip | pays *{$225.=two hundred twenty five dollars}"),
    ("Not a thousand.", "Not a *thousand."),
    ("Here's the math nobody shows you.", "Here's the *math | nobody shows you."),
    ("Dylan Page's campaign pays one dollar per thousand views.", "Dylan Page's campaign | pays *{$1=one dollar} | per *{1,000=thousand} views."),
    ("But every clip is capped at two hundred fifty dollars.", "But every clip | is *capped | at *{$250.=two hundred fifty dollars}"),
    ("Then the platform takes ten percent.", "Then the platform | takes *{10%.=ten percent}"),
    ("So your clip stops earning at two hundred fifty thousand views.", "So your clip | *stops earning | at *{250K=two hundred fifty thousand} views."),
    ("Now watch this.", "Now watch *this."),
    ("Five clips at two hundred thousand views each.", "*{5=five} clips | at *{200K=two hundred thousand} views each."),
    ("Same million views. That pays nine hundred dollars. Four times more.", "Same million views. | That pays *{$900.=nine hundred dollars} | *{4x=four times} more."),
    ("So stop chasing one viral clip.", "So stop chasing | *one viral clip."),
    ("One catch: budgets run out fast. Check the campaign page first.", "One catch: | budgets run out *fast. | Check the campaign | page first."),
    ("Comment math and I'll send you the full rate list.", "Comment *MATH | and I'll send you | the full rate list."),
]
# key hits: (scene, old time, spoken word it lands on, occurrence of that word in the line)
HITS = [
    (0, 1.60, "two", 0), (1, 3.69, "thousand", 0), (2, 5.71, "math", 0), (3, 8.89, "one", 0), (3, 10.13, "thousand", 0),
    (4, 12.50, "capped", 0), (4, 13.23, "two", 0), (5, 16.82, "ten", 0), (6, 19.40, "two", 0), (8, 23.15, "five", 0),
    (9, 29.68, "nine", 0), (9, 31.05, "four", 0), (10, 32.42, "one", 0), (11, 35.48, "fast", 0), (11, 35.90, "check", 0),
    (12, 37.51, "math", 0),
]
PRE, GAP, MIN_FRAC = 0.12, 0.2, 0.7
MIN_ABS = {0: 2.6, 1: 1.6, 7: 1.6, 12: 2.62}
LOOP_TAIL = 0.38  # the loop frames (a copy of frame 0) after the CTA


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def read_wav(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2, (w.getframerate(), w.getsampwidth())
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels()).mean(axis=1)


def write_wav(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def trim(x, thr=0.01, pad=0.03):
    idx = np.where(np.abs(x) > thr)[0]
    a, b = max(0, idx[0] - int(pad * SR)), min(len(x), idx[-1] + int(pad * SR))
    return x[a:b], a / SR


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n):
    if n < 20: return ONES[n].split()
    if n < 100: return [TENS[n // 10]] + (ONES[n % 10].split() if n % 10 else [])
    if n < 1000: return [ONES[n // 100], "hundred"] + (num_words(n % 100) if n % 100 else [])
    if n < 1_000_000: return num_words(n // 1000) + ["thousand"] + (num_words(n % 1000) if n % 1000 else [])
    return num_words(n // 1_000_000) + ["million"] + (num_words(n % 1_000_000) if n % 1_000_000 else [])


def spoken(token):
    """whisper token -> spoken words (numbers, $, %, K spelled out)"""
    t = token.lower().strip(".,:;!?\"'")
    m = re.fullmatch(r"(\$)?([\d,]+)(k|%)?", t)
    if m:
        n = int(m.group(2).replace(",", "")) * (1000 if m.group(3) == "k" else 1)
        out = num_words(n)
        if m.group(3) == "%": out.append("percent")
        if m.group(1): out.append("dollars")
        return out
    return [w for w in re.split(r"[-\s]+", re.sub(r"[^a-z0-9'\-\s]", "", t)) if w]


def parse_caption(markup):
    groups = []
    for g in markup.split("|"):
        toks = []
        for t in re.findall(r"\*?\{[^}]+\}|\S+", g.strip()):
            acc = t.startswith("*")
            t = t[1:] if acc else t
            m = re.fullmatch(r"\{([^=]+)=([^}]+)\}", t)
            disp, spk = (m.group(1), m.group(2)) if m else (t, t)
            toks.append({"w": disp, "accent": acc, "spoken": [w for w in re.split(r"[-\s]+", re.sub(r"[^a-z0-9'\-\s]", "", spk.lower())) if w]})
        groups.append(toks)
    return groups


def align(groups, words):
    """time each caption token from whisper words (sequence-matched on spoken words, gaps interpolated)"""
    S, owner = [], []
    for gi, g in enumerate(groups):
        for ti, tok in enumerate(g):
            for w in tok["spoken"]:
                S.append(w); owner.append((gi, ti))
    Wd, Wt = [], []
    for w in words:
        sp = spoken(w["text"]) or ["_"]
        d = (w["end"] - w["start"]) / len(sp)
        for k, s in enumerate(sp):
            Wd.append(s); Wt.append((w["start"] + k * d, w["start"] + (k + 1) * d))
    times = [None] * len(S)
    for a, b, n in difflib.SequenceMatcher(None, S, Wd, autojunk=False).get_matching_blocks():
        for k in range(n):
            times[a + k] = Wt[b + k]
    t0, t1 = (words[0]["start"], words[-1]["end"]) if words else (0, 1)
    i = 0
    while i < len(S):  # interpolate unmatched runs between their matched neighbours
        if times[i] is None:
            j = i
            while j < len(S) and times[j] is None: j += 1
            lo = times[i - 1][1] if i > 0 else t0
            hi = times[j][0] if j < len(S) else t1
            step = (hi - lo) / (j - i)
            for k in range(i, j): times[k] = (lo + (k - i) * step, lo + (k - i + 1) * step)
            i = j
        else:
            i += 1
    for (gi, ti), tm, s in zip(owner, times, S):
        tok = groups[gi][ti]
        tok.setdefault("s", tm[0]); tok["e"] = tm[1]
    return S, times


def main():
    work = tempfile.mkdtemp(prefix="vo-")
    lines = []
    for i, (tts, cap) in enumerate(LINES):
        raw = os.path.join(work, f"l{i:02d}.wav")
        run(["npx", "hyperframes", "tts", tts, "--voice", VOICE, "--speed", str(SPEED), "-o", raw])
        x, _ = trim(read_wav(raw))
        clip = os.path.join(work, f"c{i:02d}.wav"); write_wav(clip, x)
        d = os.path.join(work, f"t{i:02d}"); os.makedirs(d)
        run(["npx", "hyperframes", "transcribe", clip, "--dir", d])
        words = json.load(open(os.path.join(d, "transcript.json")))
        dur = len(x) / SR
        for w in words:  # whisper can overshoot the clip slightly
            w["start"], w["end"] = min(w["start"], dur), min(w["end"], dur)
        lines.append({"audio": x, "dur": dur, "words": words, "groups": parse_caption(cap)})
        print(f"line {i + 1:2d}  {dur:5.2f}s  " + " ".join(w["text"] for w in words))

    # layout: each scene starts PRE before its line; a scene lasts at least MIN_FRAC of its old length
    n = len(LINES)
    T, Lst = [0.0] * (n + 1), [0.0] * n
    Lst[0] = 0.1
    for i in range(n):
        old_d = (OLD[i + 1] if i + 1 < len(OLD) else OLD_END) - OLD[i]
        min_d = max(MIN_ABS.get(i, 0), MIN_FRAC * old_d)
        line_end = Lst[i] + lines[i]["dur"]
        if i + 1 < n:
            Lst[i + 1] = max(line_end + GAP, T[i] + min_d + PRE)
            T[i + 1] = Lst[i + 1] - PRE
        else:
            T[n] = max(T[i] + min_d, line_end + 0.35)  # CTA end: the line finishes, then the loop frames
    new_end = T[n] + LOOP_TAIL
    print(f"voice ends {Lst[-1] + lines[-1]['dur']:.2f}s, reel {new_end:.2f}s")

    # assemble the voice track
    vo = np.zeros(int((new_end + 0.1) * SR), dtype=np.float32)
    for i, ln in enumerate(lines):
        a = int(Lst[i] * SR); vo[a:a + len(ln["audio"])] += ln["audio"]
    vo = vo / (np.max(np.abs(vo)) or 1) * 0.89
    write_wav(os.path.join(ROOT, "assets", "audio", "voice.wav"), vo[: int(new_end * SR)])

    # captions on the new timeline
    caps = []
    for i, ln in enumerate(lines):
        S, tm = align(ln["groups"], ln["words"])
        for g in ln["groups"]:
            for tok in g: tok["s"] += Lst[i]; tok["e"] += Lst[i]
        ln["spoken"] = [(s, a + Lst[i], b + Lst[i]) for s, (a, b) in zip(S, tm)]
        scene_end = T[i + 1] if i + 1 < n else T[n]
        for gi, g in enumerate(ln["groups"]):
            nxt = ln["groups"][gi + 1][0]["s"] if gi + 1 < len(ln["groups"]) else min(scene_end - 0.02, g[-1]["e"] + 0.5)
            caps.append({"s": round(g[0]["s"], 3), "e": round(max(nxt, g[-1]["e"]), 3) if gi + 1 == len(ln["groups"]) else round(nxt, 3),
                         "words": [{"w": t["w"], "accent": t["accent"], "s": round(t["s"], 3), "e": round(t["e"], 3)} for t in g]})
    for a, b in zip(caps, caps[1:]):  # never two caption groups at once
        a["e"] = min(a["e"], b["s"])

    # warp knots: every scene cut, plus each key hit on its word
    knots = [[OLD[i], T[i]] for i in range(n)] + [[OLD[n], T[n]], [OLD_END, new_end]]
    for scene, old_t, word, occ in HITS:
        hits = [a for (s, a, b) in lines[scene]["spoken"] if s == word]
        if len(hits) > occ:
            knots.append([old_t, round(hits[occ], 3)])
    knots.sort()
    clean = [knots[0]]
    for o, nw in knots[1:]:  # keep only knots that stay monotonic with a sane local speed
        po, pn = clean[-1]
        if o - po < 1e-6: continue
        r = (nw - pn) / (o - po)
        if 0.45 <= r <= 2.4: clean.append([o, nw])
        else: print(f"  dropped knot old {o} -> new {nw} (rate {r:.2f})")
    timing = {"newEnd": round(new_end, 3), "warp": [[round(o, 3), round(nw, 3)] for o, nw in clean],
              "scenes": [round(t, 3) for t in T], "lines": [{"start": round(Lst[i], 3), "dur": round(ln["dur"], 3)} for i, ln in enumerate(lines)]}
    json.dump(timing, open(os.path.join(ROOT, "build", "timing.json"), "w"), indent=1)
    with open(os.path.join(ROOT, "assets", "js", "timing.js"), "w") as f:
        f.write("// generated by build/voice.py: the voice timeline. WARP maps old animation time <-> new time.\n")
        f.write(f"window.TIMING = {json.dumps(timing)};\n")
    with open(os.path.join(ROOT, "assets", "js", "captions.js"), "w") as f:
        f.write("// generated by build/voice.py from the voiceover's word timestamps; edit the lines there\nwindow.CAPS = " + json.dumps(caps) + ";\n")

    def ts(x):
        ms = int(round(x * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(os.path.join(ROOT, "captions.srt"), "w") as f:
        f.write("\n".join(f"{k + 1}\n{ts(c['s'])} --> {ts(c['e'])}\n{' '.join(w['w'] for w in c['words'])}\n" for k, c in enumerate(caps)))
    print("scenes:", " ".join(f"{t:.2f}" for t in T), f"| end {new_end:.2f}")
    print("warp:", timing["warp"])


if __name__ == "__main__":
    main()
