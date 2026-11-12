"""Sound for the Dr Kokila reel, with the openverse-sfx skill's recipe (~/.claude/skills/openverse-sfx).

  * Voice: her tight cut (assets/video/tight.mp4) cleaned (80 Hz high-pass, light de-noise, gentle compression) and
    levelled; Deepinder Goyal's own line (assets/audio/deepinder_bite.wav, the Raj Shamani podcast) under the cold
    open, cleaned and levelled to match her. The voice is the loudest layer.
  * Music: "Finding Hope" by Blindmoore (Openverse / Jamendo, CC BY 3.0), cut by build/music.py, at -19 LUFS and
    sidechain-ducked under the voice.
  * Sound effects: Openverse was searched first (sfx/search/); every effect result is a Freesound file and Freesound
    refuses this cloud machine (403 on its site, API and files; we never pose as a browser). The owner chose the CC0
    OpenGameArt library (../spin-bout-u-drake/assets/sfx/oga, mapped in build/sfx_sheet.py) instead of downloading
    Freesound picks by hand. Each effect is trimmed, peak-normalised with the skill's sfx_normalize.py, and panned off
    centre (whooshes sweep across), as earshot asked of the last reel.
  * Master: two-pass loudnorm to -14 LUFS, -2 dBTP ceiling; muxed onto the picture.
python3 build/sfx_mix.py PICTURE.mp4 OUT.mp4
"""
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx_sheet import KINDS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.expanduser("~/.claude/skills/openverse-sfx/scripts")
WORK = os.path.join(ROOT, "sfx", "work")
E = json.load(open(os.path.join(ROOT, "plan", "edit.json")))
DUR = E["dur"]
PEAK = {"whoosh_big": -9, "whoosh": -11, "swish": -13, "pop": -12, "hit": -7, "stamp": -8, "tick": -18, "success": -11,
        "drop": -10, "sparkle": -14, "click": -13, "type": -19, "rise": -11, "ding": -10, "error": -13, "scratch": -12, "count": -14, "sub": -5}
VCHAIN = "highpass=f=80,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd[:6])} ...\n{r.stderr[-1500:]}")
    return r


def prep(kind, src, k):
    files, role, gain, extra = KINDS[kind]
    raw = os.path.join(WORK, f"{kind}_{k}_raw.wav")
    af = []
    if extra.get("reverse"):
        af.append("areverse")
    md = extra.get("max_dur", 1.0)
    af.append(f"atrim=0:{md}")
    fo = extra.get("fade_out", min(.08, md / 3))
    af += [f"afade=t=out:st={max(0, md - fo):.3f}:d={fo:.3f}", "aresample=48000"]
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", ",".join(af), "-ac", "2", "-c:a", "pcm_f32le", raw])
    out = os.path.join(WORK, f"{kind}_{k}.wav")
    run(["python3", os.path.join(SKILL, "sfx_normalize.py"), raw, out, "--mode", "peak", "--target", str(PEAK[kind])])
    return out, md, extra.get("anchor") == "end"


def main():
    pic, out = sys.argv[1], sys.argv[2]
    os.makedirs(WORK, exist_ok=True)
    # the voice: her cut and Deepinder's line, each cleaned and levelled to -16 LUFS, then laid together
    her = os.path.join(WORK, "voice_her.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, "assets", "video", "tight.mp4"), "-vn", "-af",
         f"{VCHAIN},loudnorm=I=-16:TP=-3:LRA=9", "-ar", "48000", "-ac", "1", her])
    bite = os.path.join(WORK, "voice_bite.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, E["bite"]["src"]), "-af",
         f"{VCHAIN},afade=t=out:st=2.45:d=0.12,loudnorm=I=-16:TP=-3:LRA=9", "-ar", "48000", "-ac", "1", bite])
    vo = os.path.join(WORK, "voice_full.wav")
    ms = int(E["bite"]["at"] * 1000)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", her, "-i", bite, "-filter_complex",
         f"[1:a]adelay={ms}[b];[0:a][b]amix=inputs=2:normalize=0:duration=longest,apad=whole_dur={DUR}[o]", "-map", "[o]",
         "-ac", "2", "-c:a", "pcm_f32le", vo])
    # effects
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    prepared, rot, cues, last = {}, {}, [], {}
    for e in ev:
        kind, t = e["type"], e["t"]
        if kind not in KINDS or t - last.get(kind, -9) < .15:
            continue
        last[kind] = t
        files = KINDS[kind][0]
        n = rot.get(kind, 0)
        rot[kind] = n + 1
        src = files[n % len(files)]
        if (kind, src) not in prepared:
            prepared[(kind, src)] = prep(kind, src, len([k for k in prepared if k[0] == kind]))
        path, md, end_anchor = prepared[(kind, src)]
        cues.append((max(0, t - md) if end_anchor else t, path, kind, t))
    print(f"{len(cues)} cues from {len(prepared)} prepared sounds")
    bed = os.path.join(WORK, "music_bed.wav")
    run(["python3", os.path.join(SKILL, "sfx_normalize.py"), os.path.join(ROOT, "assets", "audio", "music.wav"), bed, "--mode", "lufs",
         "--target", "-19", "--max-peak", "-3"])
    inputs = ["-i", bed, "-i", vo]
    for _, path, _, _ in cues:
        inputs += ["-i", path]
    fc = [f"[1:a]aresample=48000,apad=whole_dur={DUR + .1},asplit=2[sc][vo]", "[0:a]aresample=48000[bd]",
          "[bd][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=380:makeup=1[bg]"]
    labels = ["[bg]", "[vo]"]
    for k, (start, _, kind, _) in enumerate(cues):
        ms = int(round(start * 1000))
        if kind in ("whoosh", "whoosh_big", "swish"):
            d = 1 if k % 2 else -1
            fc.append(f"[{k + 2}:a]aformat=channel_layouts=stereo,channelsplit[sl{k}][sr{k}];"
                      f"[sl{k}]volume='cos((0.5+{d}*0.35*(2*min(t/0.4,1)-1))*PI/2)*1.414':eval=frame[gl{k}];"
                      f"[sr{k}]volume='sin((0.5+{d}*0.35*(2*min(t/0.4,1)-1))*PI/2)*1.414':eval=frame[gr{k}];"
                      f"[gl{k}][gr{k}]join=inputs=2:channel_layout=stereo,adelay={ms}|{ms}[s{k}]")
        else:
            p = .5 + (.2 if k % 2 else -.2)
            gl, gr = math.cos(p * math.pi / 2) * 1.414, math.sin(p * math.pi / 2) * 1.414
            fc.append(f"[{k + 2}:a]aformat=channel_layouts=stereo,pan=stereo|c0={gl:.3f}*c0|c1={gr:.3f}*c1,adelay={ms}|{ms}[s{k}]")
        labels.append(f"[s{k}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR}[mix]")
    mix = os.path.join(WORK, "mix.wav")
    script = os.path.join(WORK, "mix_graph.txt")
    open(script, "w").write(";\n".join(fc))
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex_script", script, "-map", "[mix]", "-ar", "48000", "-c:a", "pcm_f32le", mix])
    r = run(["ffmpeg", "-i", mix, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"])
    m = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    final_audio = os.path.join(WORK, "final_audio.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", mix, "-af",
         f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", "48000", "-c:a", "pcm_f32le", final_audio])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", pic, "-i", final_audio, "-map", "0:v", "-c:v", "copy", "-map", "1:a", "-af", "apad",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    json.dump([{"t": round(s, 3), "cue": round(t, 3), "kind": k} for s, _, k, t in cues], open(os.path.join(ROOT, "plan", "sfx_cues_final.json"), "w"), indent=0)
    print("wrote", out)


if __name__ == "__main__":
    main()
