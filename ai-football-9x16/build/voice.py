"""Assemble the AI Football Club reel's voiceover from the ElevenLabs takes (Eleven v4, narrator: Asher, British).

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
    ("01_hook_a", "narrator", "Matchday one. The AI manager just benched the club's best player. Thirty thousand fans are booing.", 0, .28, 1.08, .25),
    ("02_fournil_a", "narrator", "Ninety minutes later... four-nil. The tracking data had spotted what no coach could: he'd lost half a yard of pace.", 0, .3, 1.08, .25),
    ("03_signing_a", "narrator", "Week three. It signs a seventeen-year-old nobody's heard of, for less than the star earns in a month. He scores on his debut.", 0, .28, 1.08, .25),
    ("04_halftime_b", "narrator", "Then it starts managing the game live. Two-nil down at half-time, it rewires the whole formation from the players' heart-rate data. Three goals in twenty minutes.", 0, .25, 1.08, .25),
    ("05_top_a", "narrator", "By Christmas, they're top of the league. The fans who booed? They're chanting its name.", 0, .25, 1.06, .35),
    ("06_captain_a", "narrator", "Then, in January... it sells the captain. No warning. No explanation. And in the cup final, he scores the winner. Against them.", 0, .38, 1.05, .4),
    ("07_real_a", "narrator", "Sounds far-fetched? Liverpool and Google DeepMind already built an AI that designs corner-kick tactics. And in a blind test, the club's own experts preferred its ideas nine times out of ten.", 0, .25, 1.1, .3),
    ("08_close_a", "narrator", "So... would you trust an AI with your club? Follow for more what-ifs.", 0, .3, 1.02, 0),
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
