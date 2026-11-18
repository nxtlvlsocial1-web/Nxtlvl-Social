"""Real-recording SFX packs from OpenGameArt for the edit (Openverse's Freesound files would not download here).

Each pack page is read for its licence; only CC0 and CC BY (3.0 / 4.0) are taken, never BY-SA, GPL or NC.
Files go to assets/sfx/oga/<pack>/ (not in git); the licence and author of each pack land in plan/sfx_credits_oga.json
so CC BY packs can be credited in the post.

python3 build/oga_sfx.py
"""
import io
import json
import os
import re
import urllib.parse
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "assets", "sfx", "oga")
PACKS = ["512-sound-effects-8-bit-style", "interface-sounds", "rpg-sound-pack", "sci-fi-sounds", "swishes-sound-pack",
         "air-whoosh", "75-cc0-breaking-falling-hit-sfx", "100-cc0-sfx", "100-cc0-sfx-2", "202-more-sound-effects",
         "camera", "camerashudder", "modern-ringtone-chirptone", "zippo-click-sound", "catching-fire",
         "25-cc0-bang-firework-sfx", "coin-sounds", "metal-footsteps-on-concrete", "footsteps-0", "80-cc0-rpg-sfx",
         "wind-hit-time-morph", "4-metal-dingsrings", "fantasy-sound-effects-tinysized-sfx", "erase-escape",
         "ui-sounds", "steam-release-sounds", "bell-dingschimes", "gold-coin-6", "beep-sound", "wierd-whooshes",
         "swish-bamboo-stick-weapon-swhoshes", "7-assorted-sound-effects-menu-level-up", "150-combat-sound-effects",
         "atmospheric-interaction-sound-pack", "card-game-sounds", "fantasy-magic-spell", "completion-sound"]
OK = {"publicdomain/zero/1.0": "CC0", "licenses/by/3.0": "CC BY 3.0", "licenses/by/4.0": "CC BY 4.0"}
AUD = (".wav", ".ogg", ".mp3", ".flac")


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url), timeout=60) as r:
        return r.read()


def main():
    cpath = os.path.join(ROOT, "plan", "sfx_credits_oga.json")
    credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
    for p in PACKS:
        dst = os.path.join(LIB, p)
        if p in credits and os.path.isdir(dst):
            continue
        try:
            html = get(f"https://opengameart.org/content/{p}").decode("utf-8", "replace")
        except Exception as e:                           # noqa: BLE001
            print("page failed", p, e)
            continue
        block = html[html.find("field-name-field-art-licenses"):][:3000]
        lic = sorted({m for m in re.findall(r"creativecommons\.org/((?:publicdomain/zero|licenses/[a-z-]+)/[0-9.]+)", block)})
        names = [OK[m] for m in lic if m in OK]
        if not names or len(names) != len(lic) and not any(m.startswith("publicdomain") for m in lic):
            print(f"skip {p}: licence {lic or 'unknown'}")
            continue
        lname = "CC0" if "CC0" in names else names[0]
        author = re.search(r'Author:.*?<a href="/users/[^"]*">([^<]+)</a>', html, re.S)
        files = sorted(set(re.findall(r'href="(https://opengameart\.org/sites/default/files/(?!styles/|css/|audio_preview/)[^"]+\.(?:zip|wav|ogg|mp3|flac))"', html)))
        os.makedirs(dst, exist_ok=True)
        n = 0
        for f in files:
            try:
                data = get(f)
            except Exception as e:                       # noqa: BLE001
                print("  file failed", f, e)
                continue
            if f.lower().endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    for m in z.namelist():
                        if m.lower().endswith(AUD) and not os.path.basename(m).startswith("._") and "__MACOSX" not in m:
                            out = os.path.join(dst, re.sub(r"[^\w.\- ]+", "_", m.replace("/", "__")))
                            open(out, "wb").write(z.read(m))
                            n += 1
            else:
                open(os.path.join(dst, urllib.parse.unquote(os.path.basename(f))), "wb").write(data)
                n += 1
        credits[p] = {"licence": lname, "author": author.group(1) if author else None,
                      "page": f"https://opengameart.org/content/{p}", "files": n}
        print(f"{p}: {n} files, {lname}, by {credits[p]['author']}")
        json.dump(credits, open(cpath, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
