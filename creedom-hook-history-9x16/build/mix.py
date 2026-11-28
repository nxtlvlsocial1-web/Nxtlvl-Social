"""Sound: Epidemic SFX on the film's cue list + period beds, under the voice (voice untouched except level).
Writes audio/mix.m4a (-14 LUFS, TP -2.5). No music."""
import json, pathlib, subprocess
P = pathlib.Path(__file__).resolve().parent.parent
S = P / "assets" / "sfx_es"
tm = json.loads((P / "audio/timing.json").read_text()); words = json.loads((P / "audio/words.json").read_text())
seg = {s["id"]: s for s in tm["segments"]}
L = lambda i: seg[i]["start"]; E = lambda i: seg[i]["end"]
W = lambda i, w: [x["s"] for x in words[str(i)] if x["w"].startswith(w)][0]
cues = json.loads((P / "sfx_cues.json").read_text())["cues"]
ev = []          # (file, t, gain_db, start_in_file, dur or None, fade_out)
wh = ["es_swish.mp3", "es_whoosh_tech.mp3"]; k = 0
swipe_t = W(10, "moves") - 0.1
for c in cues:
    t, g = c["t"], c.get("gain", 1.0)
    typ = c["type"]
    if typ == "stamp":
        ev += [("es_rstamp.mp3", t, -1, 0, None, 0), ("es_boom.mp3", t, -17, 0, 0.6, 0.3)]
    elif typ == "whoosh":
        if abs(t - swipe_t) < 0.3:
            ev.append(("es_swipe.mp3", t - 0.05, -4, 0, None, 0))
        else:
            ev.append((wh[k % 2], t - 0.05, -13 + 6 * g, 0, 1.2, 0.3)); k += 1
    elif typ == "pop":
        ev.append(("es_glasspop.mp3", t, -10, 0, None, 0))
    elif typ in ("marker", "pencil"):
        ev.append(("es_paper.mp3", t - 0.05, -9, 1.2, 0.6, 0.25))
    elif typ == "ticks":
        ev.append(("es_clock.mp3", t, -6, 2.0, 1.0, 0.3))
    elif typ == "ding":
        ev.append(("es_success.mp3", t, -8, 0, None, 0))
    elif typ == "impact":
        ev.append(("es_boom.mp3", t, -12, 0, 0.7, 0.3))
# period beds
ev += [("es_paper.mp3", L(3) - 0.15, -8, 4.0, 1.1, 0.4),
       ("es_projector.mp3", L(4) - 0.2, -17, 0.5, E(6) - L(4) + 0.6, 0.5),
       ("es_static.mp3", L(7) - 0.35, -16, 1.0, 0.55, 0.25),
       ("es_clock.mp3", W(7, "ran") - 0.2, -12, 5.0, E(8) - W(7, "ran") + 0.5, 0.4),
       ("es_riser.mp3", L(11) - 0.9, -16, 0, 1.2, 0.3)]
dur = tm["total_duration"]
cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(P / "audio/narration.m4a")]
fl = []
for n, (f, t, gdb, ss, d, fo) in enumerate(ev, start=1):
    cmd += ["-i", str(S / f)]
    tr = f"atrim=start={ss}" + (f":duration={d}" if d else "") + ",asetpts=PTS-STARTPTS"
    if d and fo:
        tr += f",afade=t=out:st={max(0, d - fo):.3f}:d={fo}"
    fl.append(f"[{n}:a]{tr},aformat=sample_rates=48000:channel_layouts=stereo,volume={gdb}dB,adelay={int(max(0, t) * 1000)}:all=1[s{n}]")
fl.append("[0:a]aformat=sample_rates=48000:channel_layouts=stereo[v]")
fl.append("".join(f"[s{n}]" for n in range(1, len(ev) + 1)) + f"amix=inputs={len(ev)}:normalize=0,volume=-3dB[fx]")
fl.append(f"[v][fx]amix=inputs=2:normalize=0,atrim=duration={dur},loudnorm=I=-14:TP=-2.5:LRA=11,aresample=48000[out]")
cmd += ["-filter_complex", ";".join(fl), "-map", "[out]", "-c:a", "aac", "-b:a", "192k", str(P / "audio/mix.m4a")]
subprocess.run(cmd, check=True)
print(len(ev), "sound events -> audio/mix.m4a")
