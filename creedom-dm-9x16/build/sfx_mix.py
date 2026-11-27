"""Sound for the Creators 100X x Creedom "The refresh spiral" reel (POV, framework: relatable -> conflict -> realisation -> action).

  * Voice: assets/audio/vo.wav, the owner's ElevenLabs take (Blondie, "Intense Woman", Eleven v4), pauses trimmed (build/vo_tight.py).
  * Music, in three parts (plan/music.json; credit both in the post):
      the relatable bit: "Swinging Around" by Daniel Bautista (Jamendo 2126278, CC BY 3.0), cut at the realisation (MUSIC_CUT);
      the realisation plays dry (voice and sound effects only);
      the action: "Positive Backgroundl" by Soundrider/Dope (Jamendo 1671032, CC BY 3.0) enters on "So now I check" on a downbeat.
  * Sound effects: CC0 OpenGameArt packs plus one-shots made for these reels.
  * Master: two-pass loudnorm to -14 LUFS, -2.5 dBTP; muxed onto the picture with the video stream copied.
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
SONG = os.path.join(ROOT, "sfx", "music", os.environ.get("SONG", "music_swinging_around_daniel_bautista.mp3"))
SONG_AT = float(os.environ.get("SONG_AT", "0.58"))
MUSIC_CUT = E.get("music_cut")
MUSIC_LUFS = float(os.environ.get("MUSIC_LUFS", "-22"))
# the action: "Positive Backgroundl" enters on "So now I check" (music_switch in plan/edit.json), a downbeat at 34.68 s
SONG2 = os.path.join(ROOT, "sfx", "music", "music_positive_background_soundrider.mp3")
SONG2_HIT = 34.68
MUSIC2_LUFS = float(os.environ.get("MUSIC2_LUFS", "-19"))
T_HIT = E.get("music_switch")
# kind -> (files, peak dBFS, max length s)
KINDS = {   # v2: Epidemic Sound effects (assets/sfx_es, via the Higgsfield library) for the main hits
    "whoosh": (["es_whoosh_tech", "es_swish"], -12, .9), "whoosh_big": (["es_whoosh_tech"], -9, 1.2), "swish": (["es_swish"], -15, .6),
    "impact": (["es_boom"], -7, 1.8), "sub": (["es_boom"], -9, 1.4), "ding": (["es_success"], -11, 1.2), "ding2": (["es_notif"], -13, .9),
    "error": (["es_buzzer"], -15, .7), "pop": (["es_bubble", "es_glasspop"], -14, .5), "tick": (["es_bubble"], -21, .2),
    "click": (["click"], -12, .1), "stamp": (["es_stamp"], -6, .3), "riser_short": (["es_riser"], -15, 1.4), "scanner": (["es_scanner"], -19, 1.8),
    "powerdown": (["es_powerdown"], -10, 1.3), "typing": (["es_typing"], -16, .6), "sparkle": (["es_sparkle"], -13, 1.4),
    "coin": (["es_notif"], -14, .8), "msg": (["es_msg"], -10, .9), "sent": (["es_sent"], -12, .6), "toggle": (["es_toggle"], -9, .5), "snap": (["es_snap"], -10, .3), "shutter": (["es_shutter"], -13, .5), "chime": (["es_success"], -12, 1.2), "scratch": (["scratch"], -11, .25),
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
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, "assets", "sfx_es" if name.startswith("es_") else "sfx", name + ".mp3"), "-af",
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
        if T_HIT:
            sad, happy = os.path.join(WORK, "music_sad.wav"), os.path.join(WORK, "music_happy.wav")
            t_in = T_HIT - .85                                  # the happy track enters in its break, under the riser
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(SONG_AT), "-t", f"{T_HIT + .1:.2f}", "-i", SONG, "-vn", "-af",
                 f"loudnorm=I={MUSIC_LUFS}:TP=-3:LRA=11,afade=t=in:d=0.12,afade=t=out:st={(MUSIC_CUT or t_in) - .4:.2f}:d={.6 if MUSIC_CUT else 1.3:.2f}", "-ar", "48000", "-ac", "2", sad])
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{SONG2_HIT - (T_HIT - t_in):.3f}", "-t", f"{DUR - t_in + .2:.2f}", "-i", SONG2, "-vn", "-af",
                 f"loudnorm=I={MUSIC2_LUFS}:TP=-3:LRA=11,afade=t=in:d=0.5,afade=t=out:st={DUR - t_in - 1.0:.2f}:d=1.0", "-ar", "48000", "-ac", "2", happy])
            ms = int(round(t_in * 1000))
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", sad, "-i", happy, "-filter_complex",
                 f"[1:a]adelay={ms}|{ms}[h];[0:a][h]amix=inputs=2:normalize=0:duration=longest,atrim=0:{DUR + .2:.2f}", "-ar", "48000", "-ac", "2", bed])
        else:
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(SONG_AT), "-t", f"{DUR + .2:.2f}", "-i", SONG, "-vn", "-af",
                 f"afade=t=in:d=0.12,afade=t=out:st={DUR - 1.0:.2f}:d=1.0,loudnorm=I={MUSIC_LUFS}:TP=-3:LRA=11", "-ar", "48000", "-ac", "2", bed])
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
    m = json.loads(re.findall(r"\{[^{}]*\}", run(["ffmpeg", "-i", mix, "-af", "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr)[-1])
    fin = os.path.join(WORK, "final_audio.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", mix, "-af",
         f"loudnorm=I=-14:TP=-2.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", "48000", "-c:a", "pcm_f32le", fin])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", pic, "-i", fin, "-map", "0:v", "-c:v", "copy", "-map", "1:a", "-c:a", "aac", "-b:a", "256k",
         "-shortest", "-movflags", "+faststart", out])
    json.dump([{"t": round(t, 3), "kind": k, "file": os.path.basename(p)} for t, p, k in cues],
              open(os.path.join(ROOT, "plan", "sfx_cues_final.json"), "w"), indent=0)
    print(f"wrote {out} ({len(cues)} sfx cues, music {'on' if music else 'off'})")


if __name__ == "__main__":
    main()
