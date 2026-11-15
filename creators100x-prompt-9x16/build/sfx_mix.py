"""Sound for the Creators 100X prompt reel.
  * Voice: assets/audio/vo.wav (Kokoro af_heart), the loudest layer.
  * Music: "Inspiring Ambient Motivation" by Soundrider/Dope (Jamendo 1670558 via Openverse, CC BY 3.0, credit in the
    post), 117.45 bpm, from a beat (8.196 s, where the full groove is in), sidechain-ducked under the voice. v2 (owner: "reduce the background music"): bed at -24 LUFS (was -19); v3 (owner: "reduce it more"): -28 LUFS, a deeper duck.
  * SFX: CC0 one-shots (plan/sfx_library.json): keystrokes (Kenney interface clicks, OpenGameArt CC0, because
    Freesound previews refused this machine), pops, whooshes, a ding, a glitch, stamps.
  * Master: two-pass loudnorm to -14 LUFS, -2 dBTP; muxed onto the picture with the video stream copied.
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
SONG = os.path.join(ROOT, "sfx", "music", "inspiring_ambient_motivation_soundrider.mp3")
SONG_AT = 8.196
KINDS = {"key": (["k_click_001", "k_click_002", "k_click_003", "k_click_005"], -24, .12), "send": (["whoosh_b"], -18, .4),
         "ding": (["notify"], -16, .5), "pop": (["pop"], -15, .3), "error": (["k_glitch_004"], -24, .25),
         "whoosh": (["whoosh_a"], -14, .6), "glitch": (["k_glitch_002"], -15, .6), "stamp": (["stamp"], -11, .5)}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd[:6])} ...\n{r.stderr[-1500:]}")
    return r


def prep(kind, name):
    _, peak, md = KINDS[kind]
    raw, out = os.path.join(WORK, f"{kind}_{name}_raw.wav"), os.path.join(WORK, f"{kind}_{name}.wav")
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
    prepared, rot = {}, {}
    for e in ev:
        files = KINDS[e["type"]][0]
        name = files[rot.get(e["type"], 0) % len(files)]
        rot[e["type"]] = rot.get(e["type"], 0) + 1
        if (e["type"], name) not in prepared:
            prepared[(e["type"], name)] = prep(e["type"], name)
        e["file"] = prepared[(e["type"], name)]
    bed = os.path.join(WORK, "music_bed.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(SONG_AT), "-t", f"{DUR + .2:.2f}", "-i", SONG, "-vn", "-af",
         f"loudnorm=I=-28:TP=-12:LRA=11,afade=t=in:d=0.05,afade=t=out:st={DUR - 1.0:.2f}:d=1.0", "-ar", "48000", "-ac", "2", bed])
    inputs = ["-i", os.path.join(ROOT, "assets", "audio", "vo.wav"), "-i", bed]
    fc = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[vo][sc]",
          "[1:a][sc]sidechaincompress=threshold=0.015:ratio=8:attack=12:release=420:makeup=1[bg]"]
    labels = ["[vo]", "[bg]"]
    for i, e in enumerate(ev):
        inputs += ["-i", e["file"]]
        ms = int(round(e["t"] * 1000))
        g = 10 ** (e.get("gain", 0) / 20 / 2)          # the event's gain, softened (the peaks are already set per kind)
        fc.append(f"[{2 + i}:a]volume={g:.3f},adelay={ms}|{ms}[s{i}]")
        labels.append(f"[s{i}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR}[mix]")
    script = os.path.join(WORK, "graph.txt")
    open(script, "w").write(";\n".join(fc))
    mix = os.path.join(WORK, "mix.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex_script", script, "-map", "[mix]", "-ar", "48000", "-c:a", "pcm_f32le", mix])
    m = json.loads(re.findall(r"\{[^{}]*\}", run(["ffmpeg", "-i", mix, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"]).stderr)[-1])
    fin = os.path.join(WORK, "final_audio.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", mix, "-af",
         f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", "48000", "-c:a", "pcm_f32le", fin])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", pic, "-i", fin, "-map", "0:v", "-c:v", "copy", "-map", "1:a", "-c:a", "aac", "-b:a", "256k",
         "-shortest", "-movflags", "+faststart", out])
    json.dump({"song": "Inspiring Ambient Motivation - Soundrider/Dope (CC BY 3.0)", "song_at": SONG_AT, "cues": [{k: v for k, v in e.items() if k != "file"} for e in ev]},
              open(os.path.join(ROOT, "plan", "sfx_cues_final.json"), "w"), indent=0)
    print(f"wrote {out} ({len(ev)} sfx cues, music from {SONG_AT} s)")


if __name__ == "__main__":
    main()
