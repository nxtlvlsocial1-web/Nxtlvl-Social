"""GTA 6 x Claude reel: pick instrumental night-drive music from Openverse (house lesson from the reel-flop reel, "I don't need singing in background ... just plain music"). The v4-v6 track
had vocals that a speech check missed, so every candidate is now split with Demucs (htdemucs, MIT, run locally) and
its vocal stem measured against the full mix over a 60 s stretch: only tracks whose vocal stem stays near silent pass.
Also measures tempo, density and brightness. Writes sfx/music/check_v7.json.
/root/tts/.venv/bin/python build/music_check.py
"""
import glob
import json
import os
import subprocess
import sys

import librosa
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(ROOT, "sfx", "music")
WORK = os.path.join(ROOT, "cache", "demucs")
WANT = {"Night City - FREE MUSIC", "Car Chase", "Late For Disco (80s Mix)", "Dam Burst [Synthy Electro]", "Mosaic [Electro]", "Miami",
        "Speed Surfer"}


def main():
    os.makedirs(WORK, exist_ok=True)
    seen = {}
    for f in glob.glob(os.path.join(ROOT, "sfx", "search", "music*.json")):
        for x in json.load(open(f))["results"]:
            if x["source"] == "jamendo" and any(x["title"].startswith(w) for w in WANT) and x["title"] not in seen:
                seen[x["title"]] = x
    cand = json.load(open(os.path.join(M, "candidates.json"))) if os.path.exists(os.path.join(M, "candidates.json")) else {}
    out = []
    for t, x in seen.items():
        name = "m3_" + "".join(c if c.isalnum() else "_" for c in t.lower())[:28]
        mp3 = os.path.join(M, name + ".mp3")
        if not os.path.exists(mp3):
            subprocess.run(["python3", os.path.expanduser("~/.claude/skills/openverse-sfx/scripts/sfx_fetch.py"), "--audio-url", x["audio_url"], "--name", name,
                            "--attribution", x["attribution"], "--dir", M, "--credits", os.path.join(M, "credits_candidates.txt")], capture_output=True)
        if not os.path.exists(mp3):
            print("download failed", t, flush=True)
            continue
        cand[t] = x
        dur = librosa.get_duration(path=mp3)
        st = max(0, dur * .35)
        seg = os.path.join(WORK, name + ".wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{st:.1f}", "-t", "60", "-i", mp3, "-ac", "2", "-ar", "44100", seg], check=True)
        subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", WORK, seg], capture_output=True)
        vd = os.path.join(WORK, "htdemucs", name)
        v, sr = librosa.load(os.path.join(vd, "vocals.wav"), sr=22050)
        a, _ = librosa.load(seg, sr=22050)
        rv = librosa.feature.rms(y=v)[0]
        ra = librosa.feature.rms(y=a)[0]
        ratio_db = 20 * np.log10(np.mean(rv) / max(np.mean(ra), 1e-9))
        active = float(np.mean(rv > .25 * ra))       # share of frames where the vocal stem is a real part of the mix
        y, _ = librosa.load(mp3, sr=22050, duration=180)
        tempo = float(np.atleast_1d(librosa.beat.beat_track(y=y, sr=22050)[0])[0])
        rate = len(librosa.onset.onset_detect(y=y, sr=22050)) / (len(y) / 22050)
        cent = float(np.median(librosa.feature.spectral_centroid(y=y, sr=22050)))
        r = {"title": t, "creator": x["creator"], "file": os.path.relpath(mp3, ROOT), "license": x["license"], "url": x["landing_url"],
             "vocal_db": round(float(ratio_db), 1), "vocal_active": round(active, 3), "tempo": round(tempo, 1), "onsets": round(rate, 2),
             "centroid": round(cent), "dur": round(dur, 1)}
        out.append(r)
        print(json.dumps(r), flush=True)
    json.dump(cand, open(os.path.join(M, "candidates.json"), "w"), indent=1)
    json.dump(out, open(os.path.join(M, "check.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
