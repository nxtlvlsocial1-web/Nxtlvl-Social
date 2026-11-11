"""Sound for the GTA 6 x Claude reel, with the openverse-sfx skill's recipe (~/.claude/skills/openverse-sfx):
  * the brief: a whoosh on the cuts, engine / drift sound under the gameplay, a bass hit on the ramp jump, the voice loudest.
  * one-shots (build/sfx_sheet.py) trimmed to their moment and PEAK-normalised with the skill's sfx_normalize.py; the
    per-kind peak sets the hierarchy.
  * the engine bed (a racing engine loop, CC0) runs only under the gameplay shots and the tyre squeal (CC BY 3.0,
    qubodup) only under the drift shots, both with short fades at the cuts.
  * the music ("Miami" by Lyvo, Openverse / Jamendo, CC BY 3.0, cut by build/music.py) at -19 LUFS, ducked under the voice.
  * two-pass loudnorm to -16 LUFS, -4.5 dBTP; muxed onto the picture.
python3 build/sfx_mix.py PICTURE.mp4 OUT.mp4
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx_sheet import ENGINE, KINDS, SQUEAL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.expanduser("~/.claude/skills/openverse-sfx/scripts")
WORK = os.path.join(ROOT, "sfx", "work")
SR = 48000
DUR = round(json.load(open(os.path.join(ROOT, "plan", "words.json")))[-1]["t1"] + 2.4, 2)
PEAK = {"whoosh_big": -7, "whoosh": -10, "swish": -12, "stamp": -9, "hit": -6, "bass": -3, "tick": -18, "type": -19, "click": -10,
        "success": -10, "rise": -9, "boost": -8, "siren": -16}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd[:6])} ...\n{r.stderr[-1500:]}")
    return r


def prep(kind, src, k):
    files, md, extra = KINDS[kind]
    raw = os.path.join(WORK, f"{kind}_{k}_raw.wav")
    af = []
    if extra.get("reverse"):
        af.append("areverse")
    af.append(f"atrim={extra.get('start', 0)}:{extra.get('start', 0) + md},asetpts=PTS-STARTPTS")
    if extra.get("fade_in"):
        af.append(f"afade=t=in:st=0:d={extra['fade_in']}")
    fo = extra.get("fade_out", min(.08, md / 3))
    af.append(f"afade=t=out:st={max(0, md - fo):.3f}:d={fo:.3f}")
    af.append(f"aresample={SR}")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", ",".join(af), "-ac", "2", "-c:a", "pcm_f32le", raw])
    out = os.path.join(WORK, f"{kind}_{k}.wav")
    run(["python3", os.path.join(SKILL, "sfx_normalize.py"), raw, out, "--mode", "peak", "--target", str(PEAK[kind])])
    return out, md, extra.get("anchor") == "end"


def load(path):
    tmp = os.path.join(WORK, "_dec.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-c:a", "pcm_f32le", tmp])
    y, _ = sf.read(tmp, dtype="float32")
    return y


def bed(src, spans, peak_db, name, fade=.04):
    """Loop src across the reel, audible only inside spans [(t0, t1)], with short fades; peak at peak_db."""
    y = load(src)
    y = y / (np.abs(y).max() + 1e-9) * 10 ** (peak_db / 20)
    n = int(DUR * SR)
    reps = int(np.ceil(n / len(y))) + 1
    loop = np.tile(y, (reps, 1))[:n]
    env = np.zeros(n, dtype=np.float32)
    nf = int(fade * SR)
    for t0, t1 in spans:
        a, b = int(t0 * SR), min(n, int(t1 * SR))
        if b - a <= 2 * nf:
            continue
        env[a:b] = 1
        env[a:a + nf] = np.linspace(0, 1, nf)
        env[b - nf:b] = np.linspace(1, 0, nf)
    out = os.path.join(WORK, f"bed_{name}.wav")
    sf.write(out, loop * env[:, None], SR, subtype="FLOAT")
    return out


def main():
    pic, out = sys.argv[1], sys.argv[2]
    os.makedirs(WORK, exist_ok=True)
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    prepared, rot, cues, last = {}, {}, [], {}
    for e in ev:
        kind, t = e["type"], e["t"]
        if kind not in KINDS or t - last.get(kind, -9) < (.06 if kind == "type" else .2):
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
    eng = bed(ENGINE, [(e["t"], e["t"] + e["len"]) for e in ev if e["type"] == "engine"], -20, "engine")
    sq = bed(SQUEAL, [(e["t"], e["t"] + e["len"]) for e in ev if e["type"] == "squeal"], -19, "squeal", fade=.12)

    music = os.path.join(WORK, "music_bed.wav")
    run(["python3", os.path.join(SKILL, "sfx_normalize.py"), os.path.join(ROOT, "assets", "audio", "music.wav"), music, "--mode", "lufs",
         "--target", "-19", "--max-peak", "-3"])
    inputs = ["-i", music, "-i", os.path.join(ROOT, "assets", "audio", "vo.wav"), "-i", eng, "-i", sq]
    for _, path, _, _ in cues:
        inputs += ["-i", path]
    fc = [f"[1:a]aresample={SR},aformat=channel_layouts=stereo,apad=whole_dur={DUR + .1},asplit=2[sc][vo]",
          f"[0:a]aresample={SR}[bd]", "[bd][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=350:makeup=1[bg]",
          "[2:a]anull[en]", "[3:a]anull[sq]"]
    labels = ["[bg]", "[vo]", "[en]", "[sq]"]
    for k, (start, _, _, _) in enumerate(cues):
        ms = int(round(start * 1000))
        fc.append(f"[{k + 4}:a]adelay={ms}|{ms}[s{k}]")
        labels.append(f"[s{k}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR}[mix]")
    mix = os.path.join(WORK, "mix.wav")
    script = os.path.join(WORK, "mix_graph.txt")
    open(script, "w").write(";\n".join(fc))
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex_script", script, "-map", "[mix]", "-ar", str(SR), "-c:a", "pcm_f32le", mix])
    r = run(["ffmpeg", "-i", mix, "-af", "loudnorm=I=-16:TP=-5.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    final_audio = os.path.join(WORK, "final_audio.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", mix, "-af",
         f"loudnorm=I=-16:TP=-5.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", str(SR), "-c:a", "pcm_f32le", final_audio])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", pic, "-i", final_audio, "-map", "0:v", "-c:v", "copy", "-map", "1:a", "-af", "apad",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    json.dump([{"t": round(s, 3), "cue": round(t, 3), "kind": k} for s, _, k, t in cues], open(os.path.join(ROOT, "plan", "sfx_cues_final.json"), "w"), indent=0)
    print("wrote", out)


if __name__ == "__main__":
    main()
