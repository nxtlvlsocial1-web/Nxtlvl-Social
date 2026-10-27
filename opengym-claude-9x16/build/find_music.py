"""Find a real, licensed gym track for the reel on Openverse, in place of the synthesized score.

python opengym-claude-9x16/build/find_music.py search      (inside the voice venv; needs internet, librosa, ffmpeg)
    -> assets/audio/candidates/<id>.<ext> and build/music_candidates.json, ranked: tempo near 120 bpm (or 60/90/140),
       steady high energy, at least 40 s long.
python opengym-claude-9x16/build/find_music.py use <id>
    -> assets/audio/track.<ext> and build/track.json (title, artist, licence, link, credit line). build/audio.py then
       uses this track as the music bed, ducked under the voice.

Only licences that allow commercial use and editing are kept: CC0, Public Domain Mark and CC BY (credit the artist in
the post caption). No NC (non-commercial), no ND (no derivatives: cutting and ducking a track is an edit), no SA.
"""
import json
import os
import shutil
import sys
import urllib.parse
import urllib.request

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = os.path.join(ROOT, "assets", "audio", "candidates")
API = "https://api.openverse.org/v1/audio/"
QUERIES = ["workout", "gym", "energetic electronic", "upbeat edm", "hip hop beat", "trap beat", "sport motivation",
           "electro house", "phonk", "fitness"]
OK = {"cc0", "pdm", "by"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "nxtlvl-reel-music-search/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def analyse(path):
    import librosa
    y, sr = librosa.load(path, sr=22050, mono=True, duration=120)
    tempo = float(np.atleast_1d(librosa.beat.beat_track(y=y, sr=sr)[0])[0])
    rms = librosa.feature.rms(y=y)[0]
    loud = float(np.percentile(rms, 75))
    steady = float(np.mean(rms > .5 * np.median(rms)))      # share of frames that are not quiet breaks
    onset = float(np.mean(librosa.onset.onset_strength(y=y, sr=sr)))
    best = min(abs(tempo * k - 120) for k in (1, 2, .5, 4 / 3, 3 / 4))
    score = steady * 2 + min(onset / 2, 1.5) + loud * 4 - best / 15
    return {"tempo": round(tempo, 1), "loud": round(loud, 4), "steady": round(steady, 3), "punch": round(onset, 2),
            "score": round(score, 3)}


def search():
    os.makedirs(CAND, exist_ok=True)
    seen, rows = set(), []
    for q in QUERIES:
        qs = urllib.parse.urlencode({"q": q, "category": "music", "license": ",".join(sorted(OK)), "page_size": 20})
        try:
            res = json.loads(get(f"{API}?{qs}"))["results"]
        except Exception as e:                                   # one failed query shouldn't stop the search
            print("query failed:", q, e)
            continue
        for r in res:
            dur = (r.get("duration") or 0) / 1000
            if r["id"] in seen or r["license"] not in OK or dur < 40 or not r.get("url"):
                continue
            seen.add(r["id"])
            ext = os.path.splitext(urllib.parse.urlparse(r["url"]).path)[1] or ".mp3"
            p = os.path.join(CAND, r["id"] + ext)
            try:
                if not os.path.exists(p):
                    open(p, "wb").write(get(r["url"]))
                a = analyse(p)
            except Exception as e:
                print("skip", r["title"], e)
                continue
            rows.append({"id": r["id"], "title": r["title"], "creator": r.get("creator"), "license": r["license"],
                         "license_version": r.get("license_version"), "license_url": r.get("license_url"),
                         "landing": r.get("foreign_landing_url"), "source": r.get("source"), "duration": round(dur, 1),
                         "file": os.path.relpath(p, ROOT).replace(os.sep, "/"), **a})
            print(f"{a['score']:6.2f}  {a['tempo']:6.1f} bpm  {r['license']:4}  {r['title'][:50]}  ({r.get('creator')})")
    rows.sort(key=lambda x: -x["score"])
    json.dump(rows, open(os.path.join(ROOT, "build", "music_candidates.json"), "w"), indent=1)
    print(f"{len(rows)} candidates -> build/music_candidates.json (best first). Listen to the top few, then: use <id>")


def use(cid):
    rows = json.load(open(os.path.join(ROOT, "build", "music_candidates.json")))
    r = next(x for x in rows if x["id"] == cid)
    src = os.path.join(ROOT, r["file"])
    for f in os.listdir(os.path.join(ROOT, "assets", "audio")):
        if f.startswith("track."):
            os.remove(os.path.join(ROOT, "assets", "audio", f))
    dst = os.path.join(ROOT, "assets", "audio", "track" + os.path.splitext(src)[1])
    shutil.copy(src, dst)
    lic = {"cc0": "CC0", "pdm": "Public Domain"}.get(r["license"], f"CC {r['license'].upper()} {r.get('license_version') or ''}".strip())
    r["credit"] = f"Music: \"{r['title']}\" by {r['creator']} ({lic})" + (f" {r['landing']}" if r["license"] == "by" else "")
    r["track"] = os.path.relpath(dst, ROOT).replace(os.sep, "/")
    json.dump(r, open(os.path.join(ROOT, "build", "track.json"), "w"), indent=1)
    print("using", r["track"], "|", r["credit"])


if __name__ == "__main__":
    {"search": lambda: search(), "use": lambda: use(sys.argv[2])}[sys.argv[1]]()
