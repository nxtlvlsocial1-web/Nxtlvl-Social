"""Assemble the reel's voiceover from the ElevenLabs takes (Eleven v4; Claude = AKIRA, the creator = Liam).

python3 build/voice.py      (from the project root; needs ffmpeg)

voice/raw/<nn>_<who>_t<k>.mp3 are the downloaded takes. Each picked take is trimmed, its internal pauses tightened (the
"Not one skill... eleven" beat and the whisper keep theirs), sped up a touch with the pitch kept, and loudness-matched
to -16 LUFS. The lines are then laid end to end with gaps that follow the energy curve: tight through the chaos and
the list, a long breath after "But the craziest one?" (the calm), quick again into virality.

Cut for length (takes kept in voice/raw): the spoken name in line 03 (the name is a 3D title card instead) and line 11,
the creator's "Wait... it wrote all this?" (the wake-up stays on screen with a gasp SFX).

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
    ("01_creator_t1", "creator", "Three AM... and I'm still not done.", 0, .22, 1.08, .04),
    ("02_claude_t1", "claude", "I can run your whole YouTube channel now... for free.", 0, .16, 1.12, .05),
    ("03_claude_t1", "claude", "Not one skill... eleven.", 1.98, .3, 1.06, .07),
    ("04_claude_t1", "claude", "One writes your scripts with twenty-one hook formulas.", 0, .1, 1.15, .03),
    ("05_claude_t1", "claude", "One tunes your titles and thumbnails.", 0, .1, 1.15, .03),
    ("06_claude_t1", "claude", "One finds every cut your edit needs.", 0, .1, 1.15, .03),
    ("07_claude_t1", "claude", "One replies to your comments.", 0, .1, 1.14, .05),
    ("08_claude_t1", "claude", "And one plans your whole week.", 0, .14, 1.08, .3),
    ("09_claude_t1", "claude", "But the craziest one?", 0, .3, 1.0, .55),
    ("10_claude_t2", "claude", "Virality. It finds what's blowing up in your niche... then writes your next one, in your voice.", 0, .14, 1.13, .12),
    ("12_claude_t2", "claude", "No more guessing. Setup? Just paste one link.", 0, .16, 1.1, .1),
    ("13_claude_t2", "claude", "Comment YOUTUBE, and I'll DM you the full guide.", 0, .15, 1.05, 0),
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
