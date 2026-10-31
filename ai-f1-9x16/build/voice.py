"""Assemble the AI F1 reel's voiceover from the ElevenLabs takes (Eleven v4, narrator: Jase) and time its captions.

python3 build/voice.py      (from the project root; needs ffmpeg and numpy)

voice/raw/<nn>_<beat>.mp3 are the chosen takes. Each is cut from just before its first word to just after its last,
sped up a touch with the pitch kept (atempo), and loudness-matched to -16 LUFS. No pauses are removed inside a take,
so the per-take ElevenLabs Scribe word times in voice/scribe_takes.json map straight across:
    t_reel = line_start + (t_take - cut_in) / tempo

Writes assets/audio/voice.wav (48 kHz mono), voice/lines.json and build/words.json (every caption word with s/e).
"""
import json
import os
import re
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice")
SR = 48000

# (take, caption text, tempo, gap after)
LINES = [
    ("01_hook_a", "Lap one. The AI race engineer just called its driver into the pits. On lap one. He drops to last.", 1.07, .22),
    ("02_rain_a", "Two laps later... rain. Every other car is on slick tyres. He's the only one on wets. Six cars, passed in one lap.", 1.06, .25),
    ("03_listen_a", "Then it starts listening. It reads tyre wear from the sound of the engine, and tells him exactly which corner to attack.", 1.06, .25),
    ("04_crash_b", "Lap forty. It sees a crash before it happens, and slows him down one second early. Two cars spin out right in front of him. He drives straight through.", 1.05, .3),
    ("05_final_a", "Final lap. He's leading. His teammate is right behind him. And the AI says... let him through.", 1.03, .3),
    ("06_reason_a", "He doesn't understand. But he obeys. His teammate wins the championship... by one point.", 1.03, .4),
    ("07_real_a", "Sounds far-fetched? Real Formula One teams already run billions of race simulations every weekend, just to decide when to pit.", 1.07, .3),
    ("08_close_a", "So... would you follow its orders? Follow for more what-ifs.", 1.02, 0),
]
LEAD = .1
PRE, POST = .06, .14
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())  # noqa: E731


def run(*a):
    return subprocess.run(a, capture_output=True, check=True)


def dur(p):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p).stdout)


def onset(path):
    """First moment the take rises above -45 dBFS (10 ms windows)."""
    raw = run("ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-").stdout
    x = np.frombuffer(raw, np.float32)
    w = SR // 100
    rms = np.sqrt(np.mean(x[: len(x) // w * w].reshape(-1, w) ** 2, axis=1) + 1e-12)
    hit = np.flatnonzero(20 * np.log10(rms) > -45)
    return hit[0] * .01 if len(hit) else 0.0


def main():
    takes = json.load(open(os.path.join(V, "scribe_takes.json")))["takes"]
    os.makedirs(os.path.join(V, "tight"), exist_ok=True)
    parts, lines, words, t = [], [], [], LEAD
    for i, (take, text, tempo, gap) in enumerate(LINES):
        src = os.path.join(V, "raw", take + ".mp3")
        sw = takes[take]
        cut_in = max(0.0, min(onset(src), sw[0][1]) - PRE)
        cut_out = sw[-1][2] + POST
        dst = os.path.join(V, "tight", f"{i + 1:02d}.wav")
        af = (f"atrim=start={cut_in:.3f}:end={cut_out:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
              f"areverse,afade=t=in:d=0.06,areverse,atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=11")
        run("ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ar", str(SR), "-ac", "1", dst)
        d = (cut_out - cut_in) / tempo
        lines.append({"line": i + 1, "take": take, "speaker": "narrator", "text": text,
                      "start": round(t, 3), "end": round(t + d, 3)})
        script = text.replace("...", "… ").split()
        assert [norm(w) for w in script] == [norm(w[0]) for w in sw], (take, script, [w[0] for w in sw])
        for w, (_, s, e) in zip(script, sw):
            ws, we = t + (s - cut_in) / tempo, t + (e - cut_in) / tempo
            words.append({"line": i + 1, "speaker": "narrator", "w": w, "s": round(ws - .03, 3), "e": round(max(we, ws + .1), 3)})
        parts.append((t, dst))
        t += d + gap
    total = t + .1
    flt = "".join(f"[{k}]adelay={int(st * 1000)}|{int(st * 1000)}[a{k}];" for k, (st, _) in enumerate(parts))
    flt += "".join(f"[a{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total}"
    args = ["ffmpeg", "-y", "-v", "error"]
    for _, p in parts:
        args += ["-i", p]
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    run(*args, "-filter_complex", flt, "-ar", str(SR), "-ac", "1", os.path.join(ROOT, "assets", "audio", "voice.wav"))
    json.dump({"duration": round(total, 3), "lines": lines}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    json.dump(words, open(os.path.join(ROOT, "build", "words.json"), "w"), indent=0)
    print(f"voice.wav {total:.2f} s, {len(words)} words")
    for l in lines:
        ws = [w for w in words if w["line"] == l["line"]]
        print(f"  {l['start']:6.2f}-{l['end']:6.2f}  " + " ".join(f"{w['w']}@{w['s']:.2f}" for w in ws))


if __name__ == "__main__":
    main()
