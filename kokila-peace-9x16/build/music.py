"""Music v2 (client: "the music is a little too fast for my niche"): "Hope" by Yakov Golman (Jamendo 1559870 via
Openverse, CC BY 3.0; earshot: "solo piano music, uplifting and hopeful"; no drums, no vocals), an even, gentle
solo piano. It runs from its start under the whole reel (it is 2 min long, so no restart is needed), fades in over
0.3 s and out over the last 0.8 s. The v1 edit of "Finding Hope" by Blindmoore is kept in build/music_v1_finding_hope.py.
Writes assets/audio/music.wav and plan/music_edit.json (reads the reel length from plan/edit.json).
python3 build/music.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sfx", "music", "hope_golman.mp3")
OUT = os.path.join(ROOT, "assets", "audio", "music.wav")
E = json.load(open(os.path.join(ROOT, "plan", "edit.json")))          # written by build/generate.py


def main():
    dur = E["dur"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-af",
                    f"atrim=0:{dur:.3f},afade=t=in:d=0.3,afade=t=out:st={dur - .8:.3f}:d=0.8,aresample=48000",
                    "-ac", "2", "-c:a", "pcm_f32le", OUT], check=True)
    json.dump({"track": "sfx/music/hope_golman.mp3", "title": "Hope", "creator": "Yakov Golman", "license": "CC BY 3.0",
               "landing_url": "https://www.jamendo.com/track/1559870", "from": 0.0, "dur": dur},
              open(os.path.join(ROOT, "plan", "music_edit.json"), "w"), indent=1)
    print(f"music.wav {dur} s from 'Hope' by Yakov Golman")


if __name__ == "__main__":
    main()
