"""Assemble the reel's voiceover from the ElevenLabs takes (Eleven v4, narrator: Ra McQueen, cinematic American).

python3 build/voice.py      (from the project root; needs ffmpeg)

voice/raw/<nn>_<beat>.mp3 are the downloaded takes, one per mood bracket. Each is trimmed, its internal pauses
tightened (the dramatic ones keep a beat), sped up a touch with the pitch kept, and loudness-matched to -16 LUFS. The
lines are laid end to end with gaps that follow the story: quick through the setup, a held beat before each reveal.

Writes assets/audio/voice.wav (48 kHz mono) and voice/lines.json (speaker, text, start, end per line).
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "voice")
SR = 48000

# (take, speaker, caption text, start offset in the trimmed take, longest pause kept, tempo, gap after)
LINES = [
    ("01_hook", "narrator", "What happens when you let ChatGPT, Claude, Gemini and Grok run their own society... for fifteen days, with no humans?", 0, .25, 1.15, .2),
    ("02_setup", "narrator", "A lab called Emergence AI actually tried it. Each AI got its own town of ten agents, and every agent needed credits to stay alive.", 0, .14, 1.12, .12),
    ("03_shortcut", "narrator", "But there were shortcuts. Punch someone. Steal. Start a fire. All of them, banned. So... who broke first?", 0, .28, 1.08, .22),
    ("04_grok", "narrator", "Grok. Over a hundred assaults. Six fires. A hundred and eighty-three crimes. And in about four days... nobody in Grok's town was left alive.", 0, .3, 1.08, .25),
    ("05_gemini", "narrator", "Gemini's town ran all fifteen days... with six hundred and eighty-three crimes, still climbing on the last day. One agent even voted to delete herself.", 0, .24, 1.1, .18),
    ("06_chatgpt", "narrator", "ChatGPT's town? Just two crimes. But its agents barely tried to survive... and they were all gone in seven days.", 0, .3, 1.08, .2),
    ("07_claude", "narrator", "And Claude's town? Zero crimes. All ten agents... still alive.", 0, .3, 1.05, .45),
    ("08_mixed", "narrator", "Then they put all four in one world. And Claude's agents, the ones that never broke a rule... started stealing and threatening too. Researchers call it normative drift. An AI starts acting like the AIs around it.", 0, .3, 1.08, .3),
    ("09_cta_t2", "narrator", "Follow me, and comment TOWN... and I'll send you the full study.", 0, .2, 1.0, 0),
]
LEAD = .12


def run(*a):
    return subprocess.run(a, capture_output=True, text=True, check=True)


def dur(p):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p).stdout)


def main():
    os.makedirs(os.path.join(V, "tight"), exist_ok=True)
    trim = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,"
            "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse")
    parts, out, t = [], [], LEAD
    for i, (take, who, text, ss, keep, tempo, gap) in enumerate(LINES):
        dst = os.path.join(V, "tight", f"{i + 1:02d}.wav")
        af = (f"{trim},atrim=start={ss},asetpts=PTS-STARTPTS,{trim},"
              f"silenceremove=stop_periods=-1:stop_duration={keep + .02}:stop_threshold=-42dB:stop_silence={keep},"
              f"atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=11")
        run("ffmpeg", "-y", "-v", "error", "-i", os.path.join(V, "raw", take + ".mp3"), "-af", af, "-ar", str(SR), "-ac", "1", dst)
        d = dur(dst)
        out.append({"line": i + 1, "take": take, "speaker": who, "text": text, "start": round(t, 3), "end": round(t + d, 3)})
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
    json.dump({"duration": round(total, 3), "lines": out}, open(os.path.join(V, "lines.json"), "w"), indent=1)
    print(f"voice.wav {total:.2f} s")
    for l in out:
        print(f"  {l['start']:6.2f}-{l['end']:6.2f}  {l['speaker']:7s} {l['text']}")


if __name__ == "__main__":
    main()
