"""GTA 6 x Claude reel: the music. "Miami" by Lyvo (Openverse / Jamendo, CC BY 3.0, 129 BPM), instrumental (Demucs: its
vocal stem sits ~52 dB under the mix, build/music_check.py). Its quiet build (track 62-118 s) plays under the hook and the
how-it-works part, and its full kick slams back (track 120.02 s, on a beat) exactly on "This is what it made.", when the
real game first appears. A short fade at the end; the reel loops.
Writes assets/audio/music.wav. python3 build/music.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
DROP = 120.024
DUR = round(W[-1]["t1"] + 2.4, 2)


def main():
    t_reveal = next(w for w in W if w["line"] == "g05")["t0"]
    o = DROP - t_reveal
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, "sfx", "music", "m3_miami.mp3"),
                    "-af", f"atrim={o:.3f}:{o + DUR:.3f},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.05,afade=t=out:st={DUR - .5:.2f}:d=0.5",
                    "-ac", "2", "-c:a", "pcm_f32le", os.path.join(ROOT, "assets", "audio", "music.wav")], check=True)
    json.dump({"track": "sfx/music/m3_miami.mp3", "offset": round(o, 3), "drop_at": t_reveal, "dur": DUR},
              open(os.path.join(ROOT, "plan", "music_edit.json"), "w"), indent=1)
    print(f"music: track {o:.2f} s -> video 0, the kick lands at {t_reveal:.2f} s; {DUR} s")


if __name__ == "__main__":
    main()
