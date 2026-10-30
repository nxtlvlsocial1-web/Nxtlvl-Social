"""Assemble the AI City reel's voiceover from the ElevenLabs takes (Eleven v4, narrator: Jon - Catalyst, American).

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
    ("01_hook_a", "narrator", "What if, for twenty-four hours, one AI ran an entire city? No mayor. No traffic cops. Just the AI... and a clock.", 0, .3, 1.15, .3),
    ("02_dawn_a", "narrator", "Six A.M. Every traffic light in the city syncs at once. Buses only stop where people are actually waiting. Rush hour... just disappears.", 0, .26, 1.15, .22),
    ("03_noon_a", "narrator", "Noon. Drones drop deliveries in minutes. The power grid shifts energy before anyone turns on the AC. Hospitals get ready before the ambulance even calls.", 0, .22, 1.15, .3),
    ("04_turn_a", "narrator", "Four P.M. One sensor misreads a flooded street. The AI reroutes ten thousand cars... onto one bridge.", 0, .35, 1.1, .15),
    ("05_chaos_a", "narrator", "Traffic locks up. Deliveries stall. The grid panics and cuts power to protect itself. One tiny mistake... and the whole city freezes.", 0, .28, 1.16, .4),
    ("06_midnight_a", "narrator", "Midnight. The AI fixes it in seconds, faster than any human could. But nobody can explain why it happened.", 0, .35, 1.1, .28),
    ("07_takeaway_a", "narrator", "And this isn't science fiction. Google's AI already helps time traffic lights in cities like Seattle and Rio. So the real question isn't whether AI can run a city... it's who's in charge when it gets it wrong.", 0, .3, 1.15, .3),
    ("08_cta_a", "narrator", "Follow me, and comment CITY... and I'll send you the cities already testing this.", 0, .25, 1.05, 0),
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
