"""Music: "Finding Hope" by Blindmoore (Jamendo via Openverse, CC BY 3.0; vocal check: vocals -54.6 dB under the mix,
earshot: "inspirational corporate background music"). Its first 14 s are a soft pad intro, the band comes in on the
beat at 14.58 s.

The edit, on the reel's clock (plan/words_final.json):
  * the band lands on "people" in "...that tracker is the PEOPLE around you" (the reveal);
  * before it the soft intro plays: the reel is longer than the intro there, so the intro runs from its start and is
    restarted once under a 1 s crossfade (a pad, so the seam is not heard);
  * under the silent "Drained. Anxious. Exhausted." beat the music drops to a low-passed hush and comes back on "Or";
  * it holds to the end and fades over the last 0.6 s (earshot: end on a hit, not a fade).
Writes assets/audio/music.wav and plan/music_edit.json.
python3 build/music.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sfx", "music", "finding_hope.mp3")
OUT = os.path.join(ROOT, "assets", "audio", "music.wav")
W = json.load(open(os.path.join(ROOT, "plan", "words_final.json")))
E = json.load(open(os.path.join(ROOT, "plan", "edit.json")))          # written by build/generate.py
BAND = 14.58


def word(line, text):
    return next(w for w in W if w["line"] == line and w["w"].lower().strip(".,?!") == text)


def main():
    dur = E["dur"]
    reveal = word("L3", "people")["s"]
    off = BAND - reveal                     # track time = reel time + off (after the restart)
    xf = 1.0
    seam = -off                             # reel time where the track would be at 0
    d0, d1 = E["beat"]                      # the silent text beat
    w = f"clip((t-{d0:.3f})/0.25,0,1)*clip(({d1:.3f}-t)/0.2,0,1)"
    # v1b (earshot: "music is heard in only 27% of the film"): the input is split before it is used twice (it was
    # read once, so the second half came out empty), the soft pad intro is lifted 14 dB (it sits ~20 dB under the band)
    lift = "volume='if(lt(t,14.3),5.0,1)':eval=frame"
    fc = (f"[0:a]asplit=2[s1][s2];"
          f"[s1]atrim=0:{seam + xf:.3f},asetpts=PTS-STARTPTS,volume=5.0[a];"                 # the intro from its start
          f"[s2]atrim=0:{dur - seam + .1:.3f},asetpts=PTS-STARTPTS,{lift},adelay={int(seam * 1000)}|{int(seam * 1000)}[b];"
          f"[a]afade=t=out:st={seam:.3f}:d={xf}[a2];[b]afade=t=in:st={seam:.3f}:d={xf}[b2];"
          f"[a2][b2]amix=inputs=2:normalize=0:duration=longest,aresample=48000[out]")
    # two passes: in one graph the second amix stopped at the first branch's length (12.6 s) without an error
    tmp = os.path.join(ROOT, "cache", "music_join.wav")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-filter_complex", fc, "-map", "[out]", "-ac", "2", "-c:a", "pcm_f32le", tmp], check=True)
    fc2 = (f"[0:a]asplit=2[m1][m2];[m1]volume='1-{w}':eval=frame[dry];[m2]lowpass=f=500,lowpass=f=500,volume='0.25*{w}':eval=frame[wet];"
           f"[dry][wet]amix=inputs=2:normalize=0:duration=longest,afade=t=out:st={dur - .6:.3f}:d=0.6,atrim=0:{dur:.3f}[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-filter_complex", fc2, "-map", "[out]", "-ac", "2", "-ar", "48000",
                    "-c:a", "pcm_f32le", OUT], check=True)
    json.dump({"track": "sfx/music/finding_hope.mp3", "band_on": round(reveal, 3), "restart_at": round(seam, 3), "dip": [d0, d1], "dur": dur},
              open(os.path.join(ROOT, "plan", "music_edit.json"), "w"), indent=1)
    print(f"music.wav {dur} s: band on 'people' at {reveal:.2f} s, intro restarted at {seam:.2f} s, dip {d0:.2f}-{d1:.2f}")


if __name__ == "__main__":
    main()
