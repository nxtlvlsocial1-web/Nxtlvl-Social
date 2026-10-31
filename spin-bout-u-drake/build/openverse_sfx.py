"""Build a small real-recording SFX library from Openverse for the edit (owner: "use openverse to browse them").

Only licences that allow commercial use and editing: CC0 and CC BY (credit required; the credits land in
plan/sfx_credits.json for the post description). No NC, no ND, no sampling+.
Files go to assets/sfx/openverse/<category>/<slug>_<id>.mp3 (not in git), named so the real-sfx skill's index can
read the role from the folder and the name.

python3 build/openverse_sfx.py            (re-run safe: existing files are kept)
"""
import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "assets", "sfx", "openverse")
UA = {"User-Agent": "nxtlvl-social-sfx/1.0"}

# folder: [(query, max duration s, how many)]
WANT = {
    "whoosh": [("whoosh", 2.5, 8), ("swoosh transition", 2.5, 6), ("fast swish", 1.5, 6), ("whoosh reverse", 3.0, 3)],
    "hit": [("cinematic impact hit", 3.0, 6), ("punch impact", 1.5, 4), ("boom low impact", 3.0, 4)],
    "riser": [("riser", 4.0, 4), ("reverse cymbal", 4.0, 3)],
    "glitch": [("glitch", 2.0, 6), ("digital glitch stutter", 2.0, 4)],
    "camera": [("camera shutter", 1.5, 6), ("camera flash", 2.0, 3)],
    "phone": [("phone dialing tone", 6.0, 4), ("phone ringing", 6.0, 4), ("phone call connect beep", 3.0, 3)],
    "retro": [("8 bit shoot", 1.2, 4), ("8bit laser", 1.2, 4), ("8 bit hurt", 1.2, 3), ("8 bit explosion", 2.0, 3),
              ("8bit coin", 1.2, 4), ("8 bit jump", 1.0, 3), ("chiptune powerup", 2.0, 3), ("8bit step", 0.6, 3)],
    "smoke": [("steam hiss", 4.0, 4), ("smoke puff", 3.0, 3)],
    "lighter": [("zippo lighter", 3.0, 4), ("lighter flick", 2.0, 3)],
    "fire": [("fire whoosh", 3.0, 4), ("fire ignite", 3.0, 3), ("flame burst", 3.0, 3), ("fire crackle", 8.0, 2)],
    "chime": [("sparkle", 2.5, 4), ("glass chime", 2.5, 3), ("twinkle", 2.5, 3), ("jewel", 2.0, 3)],
    "coin": [("coins drop", 2.5, 3), ("coin drop", 1.5, 3)],
    "thud": [("thud", 1.5, 4), ("body fall", 1.5, 3)],
    "footstep": [("footstep concrete", 1.2, 5), ("single footstep", 1.2, 4)],
    "pop": [("pop", 0.8, 5), ("bubble pop", 0.8, 3)],
    "paper": [("paper rip", 1.5, 3), ("tape rip", 1.5, 3)],
    "static": [("tv static burst", 2.0, 3), ("film projector", 3.0, 2)],
}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40] or "sound"


def main():
    os.makedirs(LIB, exist_ok=True)
    cpath = os.path.join(ROOT, "plan", "sfx_credits.json")
    credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
    seen = {v["openverse_id"] for v in credits.values()}
    for folder, queries in WANT.items():
        os.makedirs(os.path.join(LIB, folder), exist_ok=True)
        for q, maxd, n in queries:
            url = ("https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode(
                {"q": q, "license": "cc0,by", "page_size": 20, "source": "freesound"}))
            try:
                res = json.loads(get(url))["results"]
            except Exception as e:                       # noqa: BLE001
                print("query failed", q, e)
                time.sleep(4)
                continue
            res.sort(key=lambda r: (r["license"] != "cc0", abs((r.get("duration") or 9e9) / 1000 - maxd * .4)))
            got = 0
            for r in res:
                d = (r.get("duration") or 0) / 1000
                if got >= n or not r.get("url") or r["id"] in seen or not (.08 < d <= maxd):
                    continue
                name = f"{slug(r['title'])}_{r['id'][:8]}.mp3"
                rel = os.path.join(folder, name)
                dst = os.path.join(LIB, rel)
                try:
                    if not os.path.exists(dst):
                        open(dst, "wb").write(get(r["url"]))
                except Exception as e:                   # noqa: BLE001
                    print("  download failed", r["title"], e)
                    continue
                credits[rel] = {"openverse_id": r["id"], "title": r["title"], "creator": r.get("creator"),
                                "license": r["license"], "license_version": r.get("license_version"),
                                "landing": r.get("foreign_landing_url"), "query": q, "duration_s": d}
                seen.add(r["id"])
                got += 1
            print(f"{folder:9s} {q!r}: {got}")
            time.sleep(1.2)
    json.dump(credits, open(cpath, "w"), indent=1, ensure_ascii=False)
    print(len(credits), "sounds;", sum(1 for v in credits.values() if v["license"] == "by"), "need credit (CC BY)")


if __name__ == "__main__":
    main()
