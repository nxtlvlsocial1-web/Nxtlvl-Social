"""Voiceover, captions and the timeline for find-skills-9x16.

python3 build/voice.py        (from the project root)

Needs ffmpeg, numpy, the HyperFrames CLI, and for the voice a Python with `pip install kokoro-onnx soundfile` named by
HYPERFRAMES_PYTHON (the CLI's local Kokoro TTS). Word timestamps come from `npx hyperframes transcribe` (local Whisper).

Voices each line (Kokoro am_michael, the owner's voice pick), trims it, transcribes it, lays the lines out at a natural
pace with each scene starting just before its line, and writes:
  assets/audio/voice.wav   the voice track
  build/timing.json        scene starts, line starts and every spoken word's time (assets/js/timing.js: same, for the page)
  assets/js/captions.js    caption groups in the approved script words, timed to the spoken words
  captions.srt             the same captions as SubRip
index.html and assets/js/scene3d.js key every animation to these times (scene starts and named words), so a new take
re-times the whole reel with no hand edits.

Facts in the script were checked on skills.sh on 23 Nov 2026: 1,528,982 skills listed; find-skills (vercel-labs/skills)
is #1 with 4.5M installs; it finds and installs agent skills for a task you describe.
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
VOICE, SPEED, SR = "am_michael", 1.18, 24000
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1")

# (what Kokoro reads, caption markup: groups split on |, * = accent word, {display=spoken}, minimum scene length s)
LINES = [
    ("Stop installing Claude skills one by one.", "*Stop installing | Claude skills | one by one.", 2.5),
    ("There are over one and a half million of them.", "There are over | *{1.5 million=one and a half million} | of them.", 2.8),
    ("This free skill finds the right ones for you.", "This *free skill | finds the right ones | for you.", 2.2),
    ("It's called find skills, from Vercel Labs.", "It's called | *{find-skills,=find skills} | from Vercel Labs.", 2.5),
    ("Tell it what you're working on, like a content reel.", "Tell it what | you're working on, | like a *content reel.", 2.8),
    ("It searches the whole directory, picks the best skills for that job, and installs them for you.",
     "It *searches | the whole directory, | *picks the best skills | for that job, | and *installs them | for you.", 4.8),
    ("No wonder it's the number one skill on skills dot S H, with four and a half million installs.",
     "No wonder it's | the *{#1=number one} skill | on {skills.sh,=skills dot s h} | with *{4.5 million=four and a half million} | installs.", 3.8),
    ("Comment the word skills, and I'll send you the link.", "Comment the word *SKILLS | and I'll send you | the link.", 3.0),
]
PRE, GAP, CTA_HOLD, LOOP_TAIL = 0.12, 0.16, 0.9, 0.35


def run(cmd):
    r = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")


def read_wav(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels()).mean(axis=1)


def write_wav(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def trim(x, thr=0.01, pad=0.03):
    idx = np.where(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - int(pad * SR)): min(len(x), idx[-1] + int(pad * SR))]


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n):
    if n < 20: return [ONES[n]]
    if n < 100: return [TENS[n // 10]] + ([ONES[n % 10]] if n % 10 else [])
    if n < 1000: return [ONES[n // 100], "hundred"] + (num_words(n % 100) if n % 100 else [])
    if n < 1_000_000: return num_words(n // 1000) + ["thousand"] + (num_words(n % 1000) if n % 1000 else [])
    return num_words(n // 1_000_000) + ["million"] + (num_words(n % 1_000_000) if n % 1_000_000 else [])


def words_of(text):
    return [w for w in re.split(r"[-\s.]+", re.sub(r"[^a-z0-9'\-\s.]", "", text.lower())) if w]


def spoken(token):
    """whisper token -> spoken words ("#1" -> number one, "1.5" -> one and a half, "4.5M" -> ... million)"""
    t = token.lower().strip(",:;!?\"'")
    t = t[:-1] if t.endswith(".") else t
    m = re.fullmatch(r"(#)?(\$)?(\d[\d,]*)(\.5)?(k|m|%)?", t)
    if m:
        out = ["number"] if m.group(1) else []
        out += num_words(int(m.group(3).replace(",", "")))
        if m.group(4): out += ["and", "a", "half"]
        out += {"k": ["thousand"], "m": ["million"], "%": ["percent"]}.get(m.group(5), [])
        if m.group(2): out.append("dollars")
        return out
    return words_of(t)


def parse_caption(markup):
    groups = []
    for g in markup.split("|"):
        toks = []
        for t in re.findall(r"\*?\{[^}]+\}|\S+", g.strip()):
            acc = t.startswith("*"); t = t[1:] if acc else t
            m = re.fullmatch(r"\{([^=]+)=([^}]+)\}", t)
            disp, spk = (m.group(1), m.group(2)) if m else (t, t)
            toks.append({"w": disp, "accent": acc, "spoken": words_of(spk)})
        groups.append(toks)
    return groups


def align(groups, words):
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
        for k in range(n): times[a + k] = Wt[b + k]
    t0, t1 = (words[0]["start"], words[-1]["end"]) if words else (0, 1)
    i = 0
    while i < len(S):
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
    for (gi, ti), tm in zip(owner, times):
        tok = groups[gi][ti]; tok.setdefault("s", tm[0]); tok["e"] = tm[1]
    return list(zip(S, times))


def main():
    work = tempfile.mkdtemp(prefix="vo-")
    lines = []
    for i, (tts, cap, _) in enumerate(LINES):
        raw = os.path.join(work, f"l{i}.wav")
        run(["npx", "hyperframes", "tts", tts, "--voice", VOICE, "--speed", str(SPEED), "-o", raw])
        x = trim(read_wav(raw)); clip = os.path.join(work, f"c{i}.wav"); write_wav(clip, x)
        d = os.path.join(work, f"t{i}"); os.makedirs(d)
        run(["npx", "hyperframes", "transcribe", clip, "--dir", d])
        words = json.load(open(os.path.join(d, "transcript.json")))
        dur = len(x) / SR
        for w in words: w["start"], w["end"] = min(w["start"], dur), min(w["end"], dur)
        lines.append({"audio": x, "dur": dur, "words": words, "groups": parse_caption(cap)})
        print(f"line {i + 1}  {dur:5.2f}s  " + " ".join(w["text"] for w in words))

    n = len(LINES)
    T, Ls = [0.0] * (n + 1), [0.0] * n
    Ls[0] = 0.1
    for i in range(n):
        end = Ls[i] + lines[i]["dur"]
        if i + 1 < n:
            Ls[i + 1] = max(end + GAP, T[i] + LINES[i][2] + PRE); T[i + 1] = Ls[i + 1] - PRE
        else:
            T[n] = max(T[i] + LINES[i][2], end + CTA_HOLD)
    reel = round(T[n] + LOOP_TAIL, 3)

    vo = np.zeros(int((reel + 0.1) * SR), dtype=np.float32)
    for i, ln in enumerate(lines):
        a = int(Ls[i] * SR); vo[a:a + len(ln["audio"])] += ln["audio"]
    vo = vo / (np.max(np.abs(vo)) or 1) * 0.89
    write_wav(os.path.join(ROOT, "assets", "audio", "voice.wav"), vo[: int(reel * SR)])

    caps, tl_lines = [], []
    for i, ln in enumerate(lines):
        sw = align(ln["groups"], ln["words"])
        tl_lines.append({"start": round(Ls[i], 3), "end": round(Ls[i] + ln["dur"], 3),
                         "words": [{"w": s, "s": round(a + Ls[i], 3), "e": round(b + Ls[i], 3)} for s, (a, b) in sw]})
        scene_end = T[i + 1]
        for gi, g in enumerate(ln["groups"]):
            for tok in g: tok["s"] += Ls[i]; tok["e"] += Ls[i]
        for gi, g in enumerate(ln["groups"]):
            end = ln["groups"][gi + 1][0]["s"] if gi + 1 < len(ln["groups"]) else min(scene_end - 0.02, g[-1]["e"] + 0.45)
            caps.append({"s": round(g[0]["s"], 3), "e": round(max(end, g[0]["s"] + 0.1), 3),
                         "words": [{"w": t["w"], "accent": t["accent"], "s": round(t["s"], 3), "e": round(t["e"], 3)} for t in g]})
    for a, b in zip(caps, caps[1:]): a["e"] = min(a["e"], b["s"])

    timing = {"end": reel, "scenes": [round(t, 3) for t in T], "lines": tl_lines}
    json.dump(timing, open(os.path.join(ROOT, "build", "timing.json"), "w"), indent=1)
    open(os.path.join(ROOT, "assets", "js", "timing.js"), "w").write(
        "// generated by build/voice.py: scene starts and every spoken word's time\nwindow.TIMING = " + json.dumps(timing) + ";\n")
    open(os.path.join(ROOT, "assets", "js", "captions.js"), "w").write(
        "// generated by build/voice.py from the voiceover's word timestamps; edit the lines there\nwindow.CAPS = " + json.dumps(caps) + ";\n")

    def ts(x):
        ms = int(round(x * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    open(os.path.join(ROOT, "captions.srt"), "w").write(
        "\n".join(f"{k + 1}\n{ts(c['s'])} --> {ts(c['e'])}\n{' '.join(w['w'] for w in c['words'])}\n" for k, c in enumerate(caps)))
    print("scenes:", " ".join(f"{t:.2f}" for t in T), "| reel", reel)
    for c in caps: print(f"{c['s']:6.2f} {c['e']:6.2f}  " + " ".join(f"{w['w']}@{w['s']:.2f}" for w in c["words"]))


if __name__ == "__main__":
    main()
