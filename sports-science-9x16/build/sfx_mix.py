"""Sound for the Sports Science & Technology reel. Brief: SFX minimal, calm documentary music under a clear voice.
  * Voice: assets/audio/vo.wav (Kokoro am_michael), the loudest layer.
  * Music: "Prologue" by Hyperreal (Jamendo 1076983 via Openverse, CC BY 3.0, credit in the post), cinematic orchestral.
    Cut so its final hit lands on the end card (track 85.85 s -> reel end_card), quieter for the question and the
    body types, full from the performance scene; sidechain-ducked under the voice.
  * SFX: four Openverse CC0 one-shots, low (plan/sfx_library.json).
  * Master: two-pass loudnorm to -14 LUFS, -1.5 dBTP; muxed onto the picture with the video stream copied.
python3 build/sfx_mix.py PICTURE.mp4 OUT.mp4
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "sfx", "work")
LIB = os.path.join(ROOT, "assets", "sfx")
E = json.load(open(os.path.join(ROOT, "plan", "edit.json")))
DUR = E["dur"]
SONG = os.path.join(ROOT, "sfx", "music", "prologue_hyperreal.mp3")
HIT = 85.85                                  # the track's last big hit, then a long tail
SONG_AT = round(HIT - (E["end_card"] + .05), 3)
QUIET_TO = json.load(open(os.path.join(ROOT, "plan", "lines.json")))[3]["s"] - .1     # scene 3 starts
KINDS = {"whoosh_soft": ("whoosh_a", -16, .7), "impact_soft": ("impact", -12, 2.2), "tick": ("click", -22, .15),
         "whoosh_deep": ("whoosh_deep", -14, 1.1)}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd[:6])} ...\n{r.stderr[-1500:]}")
    return r


def prep(kind):
    name, peak, md = KINDS[kind]
    raw, out = os.path.join(WORK, f"{kind}_raw.wav"), os.path.join(WORK, f"{kind}.wav")
    fo = min(.3, md / 3)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(LIB, name + ".mp3"), "-af",
         f"silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:{md},afade=t=out:st={md - fo:.3f}:d={fo:.3f},aresample=48000",
         "-ac", "2", "-c:a", "pcm_f32le", raw])
    mx = float(re.findall(r"max_volume: (-?[\d.]+) dB", run(["ffmpeg", "-i", raw, "-af", "volumedetect", "-f", "null", "-"]).stderr)[-1])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", f"volume={peak - mx:.2f}dB", "-c:a", "pcm_f32le", out])
    return out


def main():
    pic, out = sys.argv[1], sys.argv[2]
    os.makedirs(WORK, exist_ok=True)
    ev = [e for e in json.load(open(os.path.join(ROOT, "plan", "sfx_events.json"))) if e["type"] in KINDS]
    prepared = {k: prep(k) for k in {e["type"] for e in ev}}
    bed = os.path.join(WORK, "music_bed.wav")
    # quieter (-5 dB) through the question and the body types, up over 1.5 s into the performance scene
    vol = f"volume='if(lt(t,{QUIET_TO - 1.5:.2f}),0.56,if(lt(t,{QUIET_TO:.2f}),0.56+0.44*(t-{QUIET_TO - 1.5:.2f})/1.5,1))':eval=frame"
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(SONG_AT), "-t", f"{DUR + .2:.2f}", "-i", SONG, "-vn", "-af",
         f"loudnorm=I=-18:TP=-3:LRA=11,{vol},afade=t=in:d=2.0,afade=t=out:st={DUR - 1.2:.2f}:d=1.2", "-ar", "48000", "-ac", "2", bed])
    inputs = ["-i", os.path.join(ROOT, "assets", "audio", "vo.wav"), "-i", bed]
    fc = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[vo][sc]",
          "[1:a][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=350:makeup=1[bg]"]
    labels = ["[vo]", "[bg]"]
    for i, e in enumerate(ev):
        inputs += ["-i", prepared[e["type"]]]
        ms = int(round(e["t"] * 1000))
        g = 10 ** (e.get("gain", 0) / 20 / 2)          # the event's gain, softened (the peaks are already set per kind)
        fc.append(f"[{2 + i}:a]volume={g:.3f},adelay={ms}|{ms}[s{i}]")
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
    json.dump({"song": "Prologue - Hyperreal (CC BY 3.0)", "song_at": SONG_AT, "cues": ev},
              open(os.path.join(ROOT, "plan", "sfx_cues_final.json"), "w"), indent=0)
    print(f"wrote {out} ({len(ev)} sfx cues, music from {SONG_AT} s)")


if __name__ == "__main__":
    main()
