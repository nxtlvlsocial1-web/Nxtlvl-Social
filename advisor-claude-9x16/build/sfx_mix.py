"""Sound for the AI.NXTLVL advisor reel: the voice (assets/audio/vo.wav, -16 LUFS) on top; the AI.NXTLVL bed "Funky Nurykabe
(Spinningmerkaba Mix)" by ccMixter (Jamendo 1468789, CC BY 3.0, credit in the post) sidechained under it; sound effects
fetched fresh from Openverse for this reel (plan/sfx_library.json, plan/sfx_credits.txt: CC0, plus two CC BY credited
in the post), peak-normalised per kind. Master: two-pass loudnorm to -14 LUFS, -1.5 dBTP.
python3 build/sfx_mix.py PICTURE.mp4 OUT.mp4 [--no-music]
"""
import json
import math
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "sfx", "work")
LIB = os.path.join(ROOT, "assets", "sfx")
E = json.load(open(os.path.join(ROOT, "plan", "edit.json")))
DUR = E["dur"]
SONG, SONG_AT = os.path.join(ROOT, "sfx", "music", "funky_nurykabe.mp3"), float(os.environ.get("SONG_AT", "115.96"))
MUSIC_LUFS = float(os.environ.get("MUSIC_LUFS", "-24"))   # an upbeat bed well under the voice
# short dips under words the bed masks (soft onsets: "Here's" landed on a hit and read as "Use"; the name "Claude")
_W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
DIPS = [(w["t0"] - .3, w["t1"] + .15) for w in _W if w["w"].lower().strip(".,:") in ("here's", "claude")]
DIP_EXPR = "1" + "".join(f"-0.8*clip((t-{a:.2f})/0.12,0,1)*clip(({b:.2f}-t)/0.12,0,1)" for a, b in DIPS)
# kind -> (files, peak dBFS, max length s)
KINDS = {
    "whoosh_big": (["whoosh_deep"], -9, 1.1), "whoosh": (["whoosh_a"], -11, .6), "swish": (["whoosh_a"], -19, .45),
    "pop": (["pop"], -12, .35), "click": (["click"], -16, .15), "riser": (["riser"], -15, 1.0), "wake": (["robot_wake"], -16, 1.2),
    "impact": (["impact"], -8, 1.6), "impact_soft": (["impact"], -14, 1.2), "upgrade": (["upgrade"], -12, 1.4),
    "beep": (["beep"], -14, .6), "beep_soft": (["beep"], -20, .4), "chime": (["chime"], -13, 1.0), "chime_short": (["chime"], -15, .55), "notify": (["notify"], -14, .8),
    "typing": (["typing"], -17, 1.6), "typing_soft": (["typing"], -21, 1.4), "thump": (["impact"], -18, .45), "coin": (["chime"], -17, .6),
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd[:6])} ...\n{r.stderr[-1500:]}")
    return r


def prep(kind, name):
    _, peak, md = KINDS[kind]
    raw, out = os.path.join(WORK, f"{kind}_{name}_raw.wav"), os.path.join(WORK, f"{kind}_{name}.wav")
    fo = min(.12, md / 3)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(LIB, name + ".mp3"), "-af",
         f"silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:{md},afade=t=out:st={md - fo:.3f}:d={fo:.3f},aresample=48000",
         "-ac", "2", "-c:a", "pcm_f32le", raw])
    mx = float(re.findall(r"max_volume: (-?[\d.]+) dB", run(["ffmpeg", "-i", raw, "-af", "volumedetect", "-f", "null", "-"]).stderr)[-1])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", f"volume={peak - mx:.2f}dB", "-c:a", "pcm_f32le", out])
    return out


def main():
    pic, out = sys.argv[1], sys.argv[2]
    music = "--no-music" not in sys.argv
    os.makedirs(WORK, exist_ok=True)
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    cues, rot, last, prepared = [], {}, {}, {}
    for e in ev:
        k, t = e["type"], e["t"]
        if k not in KINDS or t - last.get(k, -9) < .12:
            continue
        last[k] = t
        files = KINDS[k][0]
        name = files[rot.get(k, 0) % len(files)]
        rot[k] = rot.get(k, 0) + 1
        if (k, name) not in prepared:
            prepared[(k, name)] = prep(k, name)
        cues.append((max(0.0, t), prepared[(k, name)], k))
    inputs = ["-i", os.path.join(ROOT, "assets", "audio", "vo.wav")]
    fc = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[vo][sc]"]
    labels = ["[vo]"]
    if music:
        bed = os.path.join(WORK, "music_bed.wav")
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(SONG_AT), "-t", f"{DUR + .2:.2f}", "-i", SONG, "-vn", "-af",
             f"afade=t=in:d=0.12,afade=t=out:st={DUR - 1.0:.2f}:d=1.0,loudnorm=I={MUSIC_LUFS}:TP=-3:LRA=11,volume='{DIP_EXPR}':eval=frame", "-ar", "48000", "-ac", "2", bed])
        inputs += ["-i", bed]
        fc.append("[1:a][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=300:makeup=1[bg]")
        labels.append("[bg]")
    else:
        fc.append("[sc]anullsink")
    base = len(inputs) // 2
    for i, (t, path, k) in enumerate(cues):
        inputs += ["-i", path]
        ms = int(round(t * 1000))
        p = .5 + (.22 if i % 2 else -.22) * (0 if k in ("impact", "riser", "stamp") else 1)
        gl, gr = math.cos(p * math.pi / 2) * 1.414, math.sin(p * math.pi / 2) * 1.414
        fc.append(f"[{base + i}:a]pan=stereo|c0={gl:.3f}*c0|c1={gr:.3f}*c1,adelay={ms}|{ms}[s{i}]")
        labels.append(f"[s{i}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR}[mix]")
    script = os.path.join(WORK, "graph.txt")
    open(script, "w").write(";\n".join(fc))
    mix = os.path.join(WORK, "mix.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex_script", script, "-map", "[mix]", "-ar", "48000", "-c:a", "pcm_f32le", mix])
    m = json.loads(re.findall(r"\{[^{}]*\}", run(["ffmpeg", "-i", mix, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr)[-1])
    fin = os.path.join(WORK, "final_audio.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", mix, "-af",
         f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", "48000", "-c:a", "pcm_f32le", fin])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", pic, "-i", fin, "-map", "0:v", "-c:v", "copy", "-map", "1:a", "-c:a", "aac", "-b:a", "256k",
         "-shortest", "-movflags", "+faststart", out])
    json.dump([{"t": round(t, 3), "kind": k, "file": os.path.basename(p)} for t, p, k in cues],
              open(os.path.join(ROOT, "plan", "sfx_cues_final.json"), "w"), indent=0)
    print(f"wrote {out} ({len(cues)} sfx cues, music {'on' if music else 'off'})")


if __name__ == "__main__":
    main()
