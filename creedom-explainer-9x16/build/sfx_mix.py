"""Sound design with the openverse-sfx skill (owner: "use this to add sound effects", the skill at
~/.claude/skills/openverse-sfx), following its recipes:

  * sounds: Openverse first (one search per kind of sound, results in sfx/search/). Every sound-effect result is a
    Freesound file, and Freesound's file server answers this cloud session with 403 (checked with the skill's own
    honest user agent; we never pose as a browser). So, per the skill's step 4 ("use the project's existing sound
    library first") and the house rule, the effects come from the CC0 OpenGameArt library built for Spin Bout U
    (build/sfx_sheet.py maps each cue kind to a file).
  * every effect is trimmed to its moment, then PEAK-normalised by measurement with the skill's sfx_normalize.py
    (never loudnorm on a short file); the per-kind peak target sets the hierarchy (hits and whooshes up, ticks and
    typing down), all of them above the music and under the voice.
  * the music (Openverse: "Inspiring Technology" by Soundrider/Dope, CC BY 3.0, edited to the reel by build/music_ov.py)
    is normalised to -20 LUFS and sidechain-ducked under the voice; the voice is the loudest layer.
  * two-pass loudnorm to -16 LUFS with a -4.5 dBTP ceiling (the AAC encode adds ~0.5 dB), muxed onto the picture.
  * credits.txt lists every pack used (CC0: no credit required, logged anyway).

python3 build/sfx_mix.py PICTURE.mp4 OUT.mp4      (PICTURE: the rendered video; its own audio is ignored)
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx_sheet import KINDS, L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.expanduser("~/.claude/skills/openverse-sfx/scripts")
WORK = os.path.join(ROOT, "sfx", "work")
DUR = 37.5
# peak target (dBTP) per kind after normalising: the mix hierarchy
PEAK = {"whoosh_big": -6, "whoosh": -8, "swish": -10, "pop": -9, "hit": -6, "alert": -9, "stamp": -6, "tick": -16, "success": -8,
        "drop": -8, "sparkle": -12, "click": -10, "type": -17, "rise": -10, "ding": -8, "notify": -8, "logo": -7}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd[:6])} ...\n{r.stderr[-1500:]}")
    return r


def prep(kind, src, k):
    """Trim / fade / reverse a source as the cue sheet says, then peak-normalise it with the skill's script."""
    files, role, gain, extra = KINDS[kind]
    raw = os.path.join(WORK, f"{kind}_{k}_raw.wav")
    af = []
    if extra.get("reverse"):
        af.append("areverse")
    md = extra.get("max_dur", 1.0)
    af.append(f"atrim=0:{md}")
    fo = extra.get("fade_out", min(.08, md / 3))
    af.append(f"afade=t=out:st={max(0, md - fo):.3f}:d={fo:.3f}")
    af.append("aresample=48000")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", ",".join(af), "-ac", "2", "-c:a", "pcm_f32le", raw])
    out = os.path.join(WORK, f"{kind}_{k}.wav")
    run(["python3", os.path.join(SKILL, "sfx_normalize.py"), raw, out, "--mode", "peak", "--target", str(PEAK[kind])])
    return out, md, extra.get("anchor") == "end"


def main():
    pic, out = sys.argv[1], sys.argv[2]
    os.makedirs(WORK, exist_ok=True)
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    # one prepared file per (kind, source); rotate through a kind's sources like the cue sheet does
    prepared, rot, cues, last, packs = {}, {}, [], {}, set()
    for e in ev:
        kind, t = e["type"], e["t"]
        if kind not in KINDS or t - last.get(kind, -9) < (.06 if kind == "type" else .2):
            continue
        last[kind] = t
        files = KINDS[kind][0]
        n = rot.get(kind, 0)
        rot[kind] = n + 1
        src = files[n % len(files)]
        key = (kind, src)
        if key not in prepared:
            prepared[key] = prep(kind, src, len([k for k in prepared if k[0] == kind]))
        path, md, end_anchor = prepared[key]
        start = max(0, t - md) if end_anchor else t
        cues.append((start, path, kind, t))
        packs.add(os.path.relpath(src, L).split(os.sep)[0].split("/")[0])
    print(f"{len(cues)} cues from {len(prepared)} prepared sounds")

    # the music bed: -20 LUFS, then ducked under the voice
    bed = os.path.join(WORK, "music_bed.wav")
    run(["python3", os.path.join(SKILL, "sfx_normalize.py"), os.path.join(ROOT, "assets", "audio", "music_ov.wav"), bed, "--mode", "lufs", "--target", "-20",
         "--max-peak", "-3"])
    vo = os.path.join(ROOT, "assets", "audio", "vo.wav")
    # mix: voice + ducked bed + every effect at its moment (amix normalize=0, float, so nothing clips before the master)
    inputs = ["-i", bed, "-i", vo]
    for _, path, _, _ in cues:
        inputs += ["-i", path]
    # the voice is padded to full length: sidechaincompress stops when its control input ends (it cut the logo tail)
    fc = [f"[1:a]aresample=48000,apad=whole_dur={DUR + .1},asplit=2[sc][vo]", "[0:a]aresample=48000[bd]",
          "[bd][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400:makeup=1[bg]"]
    labels = ["[bg]", "[vo]"]
    for k, (start, _, _, _) in enumerate(cues):
        ms = int(round(start * 1000))
        fc.append(f"[{k + 2}:a]adelay={ms}|{ms}[s{k}]")
        labels.append(f"[s{k}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR}[mix]")
    mix = os.path.join(WORK, "mix.wav")
    script = os.path.join(WORK, "mix_graph.txt")
    open(script, "w").write(";\n".join(fc))
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex_script", script, "-map", "[mix]", "-ar", "48000", "-c:a", "pcm_f32le", mix])
    # two-pass loudnorm: -16 LUFS, -4.5 dBTP ceiling
    r = run(["ffmpeg", "-i", mix, "-af", "loudnorm=I=-16:TP=-4.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    final_audio = os.path.join(WORK, "final_audio.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", mix, "-af",
         f"loudnorm=I=-16:TP=-4.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", "48000", "-c:a", "pcm_f32le", final_audio])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", pic, "-i", final_audio, "-map", "0:v", "-c:v", "copy", "-map", "1:a", "-af", "apad",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    # credits
    oga = json.load(open(os.path.join(os.path.dirname(ROOT), "spin-bout-u-drake", "plan", "sfx_credits_oga.json")))
    lines = ["Creedom explainer reel - sound credits", "",
             "Music: \"Inspiring Technology\" by Soundrider/Dope is licensed under CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/),",
             "found on Openverse, hosted by Jamendo. Edited (cut and spliced to the reel, low-pass dip at 0:13) by Nxtlvl Social.",
             "Voice: ElevenLabs (eleven_v3).", "",
             "Openverse was searched first (sfx/search/*.json); its sound-effect results are Freesound files, whose server refuses",
             "downloads from this cloud session (HTTP 403), so the effects are CC0 recordings from OpenGameArt:", ""]
    for p in sorted(packs):
        c = oga.get(p, {})
        lines.append(f"- {p}: {c.get('author', '?')}, {c.get('licence', 'CC0')}, {c.get('page', '')}")
    lines += ["", "CC0 needs no credit; listed for the record."]
    open(os.path.join(ROOT, "credits.txt"), "w").write("\n".join(lines) + "\n")
    json.dump([{"t": round(s, 3), "cue": round(t, 3), "kind": k} for s, _, k, t in cues], open(os.path.join(ROOT, "plan", "sfx_cues_final.json"), "w"), indent=0)
    print("wrote", out, "and credits.txt")


if __name__ == "__main__":
    main()
