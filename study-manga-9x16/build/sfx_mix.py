"""Sound for the Creators 100X STUDY reel (copied from gta6-playbook-9x16/build/sfx_mix.py).

  * Voice: assets/audio/vo.wav (build/vo_pick.py, -16 LUFS), the loudest layer.
  * Music: "Be Happy - FREE MUSIC" by ANtarcticbreeze (Jamendo via Openverse, CC BY 3.0: credit in the post), from
    0:20 (where it is at full energy), -18 LUFS, sidechain-ducked under the voice. Freesound refused the CC0 pick's
    preview download this time, so this Jamendo track was used instead (plan/music.json, sfx/credits.txt).
  * Sound effects: Openverse CC0 one-shots fetched for the GTA 6 playbook reel (assets/sfx; plan/sfx_library.json).
  * Master: two-pass loudnorm to -14 LUFS, -1.5 dBTP; muxed onto the picture with the video stream copied.
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
SONG, SONG_AT = os.path.join(ROOT, "sfx", "music", "music_be_happy.mp3"), 20.0
# kind -> (files, peak dBFS, max length s)
KINDS = {
    "whoosh": (["whoosh_a", "whoosh_b"], -10, .6), "whoosh_big": (["whoosh_deep"], -9, 1.1), "swish": (["whoosh_b"], -13, .5),
    "impact": (["impact"], -7, 1.6), "pop": (["pop"], -12, .35), "click": (["click"], -11, .2), "tick": (["click"], -17, .15),
    "screech": (["screech"], -13, 1.2), "shutter": (["shutter"], -11, .35), "cash": (["cash"], -12, 1.0), "notify": (["notify"], -12, .4),
    "stamp": (["stamp"], -7, .6), "buzzer": (["buzzer"], -15, .5), "lock": (["lock"], -10, .9), "riser": (["riser"], -13, 1.0),
    "riser_short": (["riser"], -18, 1.0), "ding": (["notify"], -11, .4),
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
             f"afade=t=in:d=0.12,afade=t=out:st={DUR - 1.0:.2f}:d=1.0,loudnorm=I=-18:TP=-3:LRA=11", "-ar", "48000", "-ac", "2", bed])
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
