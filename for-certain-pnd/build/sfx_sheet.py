"""Cue sheet for the real-sfx skill's mix.py: plan/sfx_events.json (written by build/generate.py) -> real CC0
recordings from the OpenGameArt library built for Spin Bout U (../spin-bout-u-drake/assets/sfx/oga; all CC0, no credit
needed). Openverse comes first by the house rule, but its Freesound downloads are refused from cloud sessions.
A light layer under the song:
- a reversed swell into each portal dive
- a swish on the whips, air on the dissolves
- a hit on the flashes and the drop
- thuds for the bags, a glass break on PRIDE, a stamp on CERTAIN
- a sparkle on the diamond, a spray, a pour, a neon buzz
- a soft swell into the logo
v2 adds a paper tear on the torn-hole cuts, the phone buzz, a heartbeat thump, a camera shutter and a paper slap for
the polaroid memories.

python3 build/sfx_sheet.py VIDEO.mp4 [--out renders/cues.json]
"""
import argparse
import itertools
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(os.path.dirname(ROOT), "spin-bout-u-drake", "assets", "sfx", "oga")
RPG_SWING = sorted(x for x in os.listdir(os.path.join(L, "rpg-sound-pack")) if "swing" in x.lower())


def f(rel):
    p = os.path.join(L, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing sound: {rel}")
    return p


SUB = {"lowpass": 300, "max_dur": .5, "fade_out": .2}
KINDS = {   # kind: (files, role, gain_db, extra)
    "portal": ([f("wind-hit-time-morph/qubodup-megaswosh1.wav"), f("wind-hit-time-morph/qubodup-megaswosh2.wav"),
                f("wind-hit-time-morph/60009__qubodup__swosh_22.flac")], "whoosh", -10, {"reverse": True, "max_dur": .7, "anchor": "end"}),
    "whip": ([f("swishes-sound-pack/swishes__swish-4.wav"), f("rpg-sound-pack/" + RPG_SWING[0]), f("swishes-sound-pack/swishes__swish-8.wav"),
              f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__tube-plastic-whoosh-02.wav")], "whoosh", -11, {"max_dur": .5}),
    "air": ([f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__cloth-pouch-shake-01.wav")], "whoosh", -17, {"max_dur": .6}),
    "hit": ([f("100-cc0-sfx-2/sfx100v2_hit_01.ogg"), f("100-cc0-sfx-2/sfx100v2_hit_03.ogg")], "hit", -13, {}),
    "drop": ([f("sci-fi-sounds/Audio__lowFrequency_explosion_001.ogg")], "hit", -9, SUB),
    "glitch": ([f("interface-sounds/Audio__glitch_002.ogg")], "glitch", -14, {"max_dur": .35}),
    "thud": ([f("75-cc0-breaking-falling-hit-sfx/bfh1_hit_02.ogg")], "foley", -12, {"max_dur": .4}),
    "stamp": ([f("150-combat-sound-effects/01_combat_melee__impact_punch_heavy_000_48kHz_16bit_0.65s_8fb58ba7_s02.wav")], "hit", -11, {"max_dur": .45}),
    "shatter": ([f("75-cc0-breaking-falling-hit-sfx/bfh1_glass_breaking_02.ogg")], "glass", -12, {"max_dur": .9, "fade_out": .3}),
    "sparkle": ([f("bell-dingschimes/bell_ding2.wav")], "chime", -18, {"max_dur": 1.0, "fade_out": .4}),
    "spray": ([f("steam-release-sounds/steam hisses - Marker _2.wav")], "foley", -18, {"anchor": "start", "max_dur": .8, "fade_out": .3}),
    "pour": ([f("202-more-sound-effects/Drink__Drink_02.wav")], "foley", -14, {"anchor": "start", "max_dur": 1.0, "fade_out": .3}),
    "scratch": ([f("interface-sounds/Audio__error_004.ogg")], "glitch", -16, {"max_dur": .3}),
    "neon": ([f("sci-fi-sounds/Audio__forceField_001.ogg")], "ambience", -20, {"anchor": "start", "max_dur": .5, "fade_out": .2}),
    "logo": ([f("wind-hit-time-morph/qubodup-megaswosh2.wav")], "whoosh", -14, {"reverse": True, "max_dur": .6}),
    # v2
    "tear": ([f("100-cc0-sfx/paper_04.ogg"), f("100-cc0-sfx/paper_03.ogg")], "foley", -10, {"max_dur": .6}),
    "buzz": ([f("202-more-sound-effects/Phone__Phone2.wav")], "foley", -14, {}),
    "heartbeat": ([f("75-cc0-breaking-falling-hit-sfx/bfh1_hit_02.ogg")], "hit", -12, {"lowpass": 400, "max_dur": .35}),
    "shutter": ([f("camera/photo.ogg")], "foley", -11, {"max_dur": .6}),
    "slap": ([f("100-cc0-sfx/paper_01.ogg"), f("100-cc0-sfx/paper_02.ogg")], "foley", -13, {"max_dur": .45}),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=os.path.join(ROOT, "renders", "cues.json"))
    a = ap.parse_args()
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    rot = {k: itertools.cycle(v[0]) for k, v in KINDS.items()}
    cues, uses = [], {}
    for e in ev:
        k, t = e["type"], e["t"]
        if k not in KINDS:
            continue
        files, role, gain, extra = KINDS[k]
        fn = next(rot[k])
        n = uses.get(fn, 0)
        uses[fn] = n + 1
        c = {"t": max(0.0, t), "label": k, "file": fn, "role": role, "gain_db": gain} | extra
        if n:
            c["pitch"] = (0, -1, 1, -2, 2)[n % 5]
        cues.append(c)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({"video": os.path.abspath(a.video), "keep_audio": "yes", "cues": cues}, open(a.out, "w"), indent=1)
    print(f"{len(cues)} cues -> {a.out}")


if __name__ == "__main__":
    main()
