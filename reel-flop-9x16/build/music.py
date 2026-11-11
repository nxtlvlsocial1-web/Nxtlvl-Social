"""Background music from Openverse (owner: "also use background music from openverse"). v4 (owner: the music was too
slow/flat): "What Can Do" by Felixjd (Jamendo, CC BY 3.0), 129 BPM, the busiest and brightest of the faster CC BY tracks
found on Openverse (sfx/search/music2_*.json; all checked instrumental with Whisper). v1-v3 used "Hip-Hop 1" by Deff
Syndicate (83 BPM).

The edit (beat grid: sfx/music/beats_hh1.json, the skill's beat_grid.py):
  * the track's breakdown (60-74 s) plays under the hook, and its full beat slams back (track 74.07 s, on a beat) exactly
    on the countdown's 0 after "three seconds.";
  * on "If nothing moves," the music drops out (low-pass, near silence) and comes back on "thumbs keep scrolling",
    acting out the line;
  * a 1.2 s fade at the end.
Writes assets/audio/music.wav; build/sfx_mix.py ducks it under the voice.
python3 build/music.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sfx", "music", "m2_what_can_do.mp3")
OUT = os.path.join(ROOT, "assets", "audio", "music.wav")
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
DROP_BEAT = 74.072


def wt(line, i, key="t0"):
    return [w for w in W if w["line"] == line][i][key]


def main():
    dur = round(W[-1]["t1"] + 1.7, 2)
    flip = wt("l02", 6, "t1") + .06            # the countdown's 0, the iris flip (build/generate.py: the 0 lands at the end of "seconds." + .06)
    o = DROP_BEAT - flip
    d0, d1 = wt("l08", 1) - .04, wt("l08", 3) - .02   # "nothing moves," .. "thumbs"
    w = f"clip((t-{d0:.3f})/0.08,0,1)*clip(({d1:.3f}-t)/0.06,0,1)"
    fc = (f"[0:a]atrim={o:.3f}:{o + dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.04,"
          f"afade=t=out:st={dur - 1.2:.2f}:d=1.2,asplit=2[m1][m2];"
          f"[m1]volume='1-{w}':eval=frame[dry];"
          f"[m2]lowpass=f=400,lowpass=f=400,volume='0.22*{w}':eval=frame[wet];"
          f"[dry][wet]amix=inputs=2:normalize=0,atrim=0:{dur}[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-filter_complex", fc, "-map", "[out]", "-ac", "2", "-ar", "48000",
                    "-c:a", "pcm_f32le", OUT], check=True)
    json.dump({"track": "sfx/music/m2_what_can_do.mp3", "offset": round(o, 3), "flip": round(flip, 3), "dip": [round(d0, 3), round(d1, 3)], "dur": dur},
              open(os.path.join(ROOT, "plan", "music_edit.json"), "w"), indent=1)
    print(f"wrote {OUT}: track {o:.2f} s -> video 0, beat drop on the flip at {flip:.2f} s, dip {d0:.2f}-{d1:.2f}")


if __name__ == "__main__":
    main()
