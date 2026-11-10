"""Background music from Openverse (owner: "add a better background music with the help of openverse which fits the
context and script"): "Inspiring Technology" by Soundrider/Dope (Jamendo, CC BY 3.0), picked by measurement from four
Openverse/Jamendo shortlisted tracks (sfx/search/music_*.json): the brightest, most driving one (172 BPM half-time
feel, ~5 onsets/s, spectral centre ~3.1 kHz), right for a fast AI-for-creators explainer.

The edit (plan/music_edit.json, worked out on the skill's beat grid, sfx/music/beats.json):
  * video 0 s = track 12.75 s, the last bars of its build, so the track's first kick drop lands on the hook's "second."
  * at 31.48 s (a beat, just after the CTA wipe) it splices, 192 beats later and in phase, into the track's ending, so
    the last kick (track 120.5 s) hits under the creedom logo and its tail rings out at the end;
  * on "energy dropped" (13.2-14.4 s) the music sinks behind a low-pass and comes back, acting out the line.
Writes assets/audio/music_ov.wav (37.6 s, 48 kHz stereo); build/sfx_mix.py uses it as the bed.
python3 build/music_ov.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = json.load(open(os.path.join(ROOT, "plan", "music_edit.json")))
SRC = os.path.join(ROOT, E["track"])
OUT = os.path.join(ROOT, "assets", "audio", "music_ov.wav")
DUR = 37.6
XF = .04


def main():
    o1, o2, sp = E["o1"], E["o2"], E["splice"]
    a0, a1 = o1, o1 + sp + XF / 2                 # segment A: track time for video [0, splice]
    b0 = sp + o2 - XF / 2                          # segment B: from the splice to the end
    b1 = DUR + o2
    d0, d1 = E["dip"]
    w = (f"clip((t-{d0 - .05})/0.12,0,1)*clip(({d1 + .1}-t)/0.25,0,1)")   # 0 -> 1 -> 0, smooth edges
    fc = (f"[0:a]atrim={a0}:{a1},asetpts=PTS-STARTPTS[a];"
          f"[1:a]atrim={b0}:{b1},asetpts=PTS-STARTPTS[b];"
          f"[a][b]acrossfade=d={XF}:c1=tri:c2=tri,aresample=48000,afade=t=in:d=0.03,afade=t=out:st={DUR - .45:.2f}:d=0.45,asplit=2[m1][m2];"
          f"[m1]volume='1-{w}':eval=frame[dry];"
          f"[m2]lowpass=f=650,lowpass=f=650,volume='0.75*{w}':eval=frame[wet];"
          f"[dry][wet]amix=inputs=2:normalize=0,atrim=0:{DUR}[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-i", SRC, "-filter_complex", fc, "-map", "[out]", "-ac", "2",
                    "-ar", "48000", "-c:a", "pcm_f32le", OUT], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
