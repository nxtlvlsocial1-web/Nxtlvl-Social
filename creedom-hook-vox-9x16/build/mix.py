"""Epidemic SFX from plan/sfx_events.json + beds under the voice (voice untouched except level). Muxes onto the silent render."""
import json, pathlib, subprocess, sys
P = pathlib.Path(__file__).resolve().parent.parent
S = P / "assets/sfx_es"
ev = json.loads((P / "plan/sfx_events.json").read_text())
tm = json.loads((P / "assets/audio/timing.json").read_text()); words = json.loads((P / "assets/audio/words.json").read_text())
seg = {s["id"]: s for s in tm["segments"]}
L = lambda i: seg[i]["start"]; E = lambda i: seg[i]["end"]
W = lambda i, w: [x["s"] for x in words[str(i)] if x["w"].startswith(w)][0]
MAP = {  # kind: (file, gain dB, start in file, duration or None, fade out)
    "pop": ("es_glasspop.mp3", -11, 0, None, 0), "slap": ("es_slap.mp3", -6, 0, 0.5, 0.15), "tear": ("es_tear.mp3", -5, 0, None, 0),
    "scribble": ("es_scribble.mp3", -8, 0, None, 0), "type": ("es_typing.mp3", -14, 0, 0.6, 0.2), "tick": ("es_clock.mp3", -7, 2.0, 0.8, 0.25),
    "static": ("es_static.mp3", -12, 3.0, 0.6, 0.2), "riser": ("es_riser.mp3", -12, 0, 1.0, 0.2), "boom": ("es_boom.mp3", -9, 0, 1.0, 0.4),
    "impact": ("es_boom.mp3", -13, 0, 0.6, 0.3), "swipe": ("es_swipe.mp3", -4, 0, None, 0), "scan": ("es_scanner.mp3", -10, 0, 2.4, 0.4),
    "ding": ("es_success.mp3", -8, 0, None, 0), "sparkle": ("es_sparkle.mp3", -12, 0, None, 0),
    "projector": ("es_projector.mp3", -16, 0.5, L(7) - L(4) + 0.2, 0.4), "clock": ("es_clock.mp3", -12, 5.0, E(8) - W(7, "ran") + 0.4, 0.4),
}
items, k = [], 0
for e in ev:
    kind, t = e["kind"], e["t"]
    if kind == "stamp":
        items += [("es_rstamp.mp3", t, -1, 0, None, 0), ("es_boom.mp3", t, -18, 0, 0.6, 0.3)]
    elif kind == "whoosh":
        items.append((("es_swish.mp3", "es_whoosh_tech.mp3")[k % 2], t, -10, 0, 1.1, 0.3)); k += 1
    else:
        f, g, ss, d, fo = MAP[kind]; items.append((f, t, g + e.get("gain", 0), ss, d, fo))
items.append(("es_paper.mp3", L(3) - 0.1, -9, 4.0, 0.9, 0.3))
dur = tm["total_duration"]
cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(P / "assets/audio/narration.m4a")]
fl = []
for n, (f, t, g, ss, d, fo) in enumerate(items, start=1):
    cmd += ["-i", str(S / f)]
    tr = f"atrim=start={ss}" + (f":duration={d}" if d else "") + ",asetpts=PTS-STARTPTS"
    if d and fo:
        tr += f",afade=t=out:st={max(0, d - fo):.3f}:d={fo}"
    fl.append(f"[{n}:a]{tr},aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={int(max(0, t) * 1000)}:all=1[s{n}]")
fl.append("[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v]")
fl.append("".join(f"[s{n}]" for n in range(1, len(items) + 1)) + f"amix=inputs={len(items)}:normalize=0,volume=-3dB[fx]")
fl.append(f"[v][fx]amix=inputs=2:normalize=0,atrim=duration={dur},loudnorm=I=-14:TP=-2.5:LRA=11,aresample=48000[out]")
cmd += ["-filter_complex", ";".join(fl), "-map", "[out]", "-c:a", "aac", "-b:a", "192k", str(P / "assets/audio/mix.m4a")]
subprocess.run(cmd, check=True)
print(len(items), "sound events -> assets/audio/mix.m4a")
