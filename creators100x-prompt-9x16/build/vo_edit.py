"""v2 (owner, 2026-11-24): line 2 ("And honestly, that's the point.") confused viewers. It is cut from the voice; in its
place a silent beat carries the on-screen line "Sounds robotic?" (no new recording: ElevenLabs is no longer available).
Reads the tightened natural take (assets/audio/vo_natural.wav, from vo_tight.py) and plan/words_full.json; writes
assets/audio/vo_natural_edit.wav and plan/words.json (r1 removed, later words shifted). Then run vo_robot.py.
python3 build/vo_edit.py"""
import json, os, shutil, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
if not os.path.exists(P("plan", "words_full.json")):
    shutil.copy(P("plan", "words.json"), P("plan", "words_full.json"))
W = json.load(open(P("plan", "words_full.json")))
r0_end = max(w["t1"] for w in W if w["line"] == "r0")
r2_start = min(w["t0"] for w in W if w["line"] == "r2")
KEEP_A = round(r0_end + .17, 3)          # end of the robot line (+ its tail)
SRC_B = round(r2_start - .06, 3)         # resume just before "If you type"
NEW_R2 = 3.3                             # where "If" lands now: the robot line, the glitch, then the "Sounds robotic?" beat
gap = NEW_R2 - .06 - KEEP_A
delta = NEW_R2 - r2_start
filt = (f"[0:a]atrim=0:{KEEP_A},asetpts=PTS-STARTPTS,afade=t=out:st={KEEP_A - .02:.3f}:d=0.02,apad=pad_dur={gap:.3f}[a];"
        f"[0:a]atrim={SRC_B},asetpts=PTS-STARTPTS,afade=t=in:d=0.01[b];[a][b]concat=n=2:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", P("assets", "audio", "vo_natural.wav"), "-filter_complex", filt, "-map", "[o]",
                "-ar", "48000", "-ac", "1", "-c:a", "pcm_f32le", P("assets", "audio", "vo_natural_edit.wav")], check=True)
out = []
for w in W:
    if w["line"] == "r1":
        continue
    if w["line"] != "r0":
        w = {**w, "t0": round(w["t0"] + delta, 3), "t1": round(w["t1"] + delta, 3)}
    out.append(w)
json.dump(out, open(P("plan", "words.json"), "w"), indent=0)
print(f"cut {KEEP_A}-{SRC_B} s, beat {gap:.2f} s, later words shifted {delta:+.2f} s; last word ends {out[-1]['t1']:.2f} s")
