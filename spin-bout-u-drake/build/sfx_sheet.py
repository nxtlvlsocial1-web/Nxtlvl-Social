"""Cue sheet for the real-sfx skill's mix.py: plan/sfx_events.json (written by build/collage.py) -> exact real
recordings from the CC0 library in assets/sfx/oga (OpenGameArt packs, see plan/sfx_credits_oga.json).

Under a full song the sound design stays a layer, not a second track: thinned (no sound on keyword flickers, two
camera clicks per clip at most, diamonds every other bounce), most kinds a few dB under their role level.

python3 build/sfx_sheet.py RENDER.mp4 [--out cache/sfx/cues.json]
"""
import argparse
import itertools
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(ROOT, "assets", "sfx", "oga")
RPG_SWING = sorted(x for x in os.listdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "sfx", "oga", "rpg-sound-pack")) if "swing" in x.lower())
R8P = ("512-sound-effects-8-bit-style/The Essential Retro Video Game Sound Effects Collection _512 sounds_ By Juhani Junkala__"
       "Movement__Portals and Transitions__")
R8 = "512-sound-effects-8-bit-style/The Essential Retro Video Game Sound Effects Collection _512 sounds_ By Juhani Junkala__"


def f(rel):
    p = os.path.join(L, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing sound: {rel}")
    return p


def r8(sub):
    d = os.path.join(L, "512-sound-effects-8-bit-style")
    hits = sorted(x for x in os.listdir(d) if sub in x)
    if not hits:
        raise SystemExit(f"no 8-bit sound matching {sub}")
    return [os.path.join(d, x) for x in hits]


# kind: (files to rotate through, role, gain_db, extra cue fields)
KINDS = {
    # cuts: five whoosh families interleaved (critique: 13 takes of one swish family gave the pack away)
    "whoosh": ([f("rpg-sound-pack/" + RPG_SWING[0]), f("wind-hit-time-morph/60009__qubodup__swosh_22.flac"),
                f("swishes-sound-pack/swishes__swish-9.wav"), f("wierd-whooshes/weird_whoosh_sounds_-_whoosh_12_0.mp3"),
                f(R8P + "sfx_movement_portal5.wav"), f(R8P + "sfx_movement_portal1.wav"),
                f("rpg-sound-pack/" + RPG_SWING[1])], "whoosh", -4, {"max_dur": 1.0}),
    "swish": ([f("swishes-sound-pack/swishes__swish-4.wav"), f("wind-hit-time-morph/qubodup-megaswosh2.wav"),
               f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__cloth-pouch-shake-01.wav"), f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__cloth-pouch-shake-02.wav"),
               f("rpg-sound-pack/" + RPG_SWING[2])], "whoosh", -6, {"max_dur": .8}),
    # v17: whoosh2_0 holds 9 sweeps and the weird whoosh 15; at max_dur 1.6 two of them played (owner: "double woosh").
    # Only single-sweep recordings on the big cuts now, and the multi-sweep files are cut to their first sweep elsewhere.
    "whoosh_big": ([f("wind-hit-time-morph/qubodup-megaswosh1.wav"), f("wind-hit-time-morph/60009__qubodup__swosh_22.flac"),
                    f("wind-hit-time-morph/qubodup-megaswosh2.wav"), f("rpg-sound-pack/" + RPG_SWING[0])],
                   "whoosh", -2, {"max_dur": .9}),
    "glitch": ([f(p_) for k in range(4) for p_ in (f"interface-sounds/Audio__glitch_00{k + 1}.ogg",
                                                     f"sci-fi-sounds/Audio__computerNoise_00{k}.ogg")], "glitch", -7, {"max_dur": .35}),
    "hit": ([f("100-cc0-sfx-2/sfx100v2_hit_01.ogg"), f("75-cc0-breaking-falling-hit-sfx/bfh1_hit_02.ogg"),
             f("100-cc0-sfx-2/sfx100v2_hit_03.ogg")], "hit", -4, {}),
    "boom": ([f("sci-fi-sounds/Audio__lowFrequency_explosion_000.ogg")], "hit", -2, {"max_dur": 1.6}),
    "camera": ([f("camera/photo.ogg"), f("202-more-sound-effects/Camera__Camera_01.wav"), f("camerashudder/camera_0.ogg"),
                f("202-more-sound-effects/Camera__Camera_03.wav")], "camera", -8, {}),
    "sticker": ([f("202-more-sound-effects/Paper _ Stationery__Stationery_01.wav"), f("card-game-sounds/cockatrice__playcard.wav"),
                 f("rpg-sound-pack/RPG Sound Pack__inventory__cloth.wav"), f("202-more-sound-effects/Paper _ Stationery__Stationery_03.wav"),
                 f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__book-page-01.wav"), f("rpg-sound-pack/RPG Sound Pack__inventory__cloth-heavy.wav"),
                 f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__cover-paper-tear-01.wav"), f("card-game-sounds/cockatrice__draw.wav")],
                "paper", -9, {"max_dur": .45, "slice": "first"}),
    "step": ([f("footsteps-0/02-footstep.ogg"), f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__boots-leather-step-01.wav"),
              f("footsteps-0/04-footstep.ogg"), f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__boots-leather-jump-01.wav")], "foley", -5, {}),
    "pin": ([f(f"interface-sounds/Audio__drop_00{k}.ogg") for k in (1, 2, 3)], "pop", -4, {}),
    "tick": ([f("interface-sounds/Audio__tick_001.ogg"), f("interface-sounds/Audio__click_002.ogg"),
              f("interface-sounds/Audio__tick_002.ogg"), f("interface-sounds/Audio__switch_003.ogg")], "click", -3, {}),
    "phone": ([f("modern-ringtone-chirptone/chirptone.wav")], "ui", -9, {"anchor": "start", "fade_out": .25}),
    "connect": ([f("interface-sounds/Audio__confirmation_001.ogg")], "ui", -6, {}),
    "lighter": ([f("zippo-click-sound/zipclick.flac")], "foley", -1, {}),
    "ignite": ([f("catching-fire/flame_0.ogg")], "foley", 0, {"anchor": "start", "max_dur": 1.4}),
    "fire": ([f("catching-fire/flame_0.ogg")], "ambience", -4, {"anchor": "start", "fade_out": .3}),
    "smoke": ([f("steam-release-sounds/steam hisses - Marker _2.wav")], "ambience", -1, {"anchor": "start", "fade_out": .5}),
    "throw": (r8("sfx_movement_jump1."), "ui", -6, {}),
    "phone_throw": (r8("sfx_movement_jump2."), "ui", -14, {}),
    "phone_smash": ([f("75-cc0-breaking-falling-hit-sfx/bfh1_glass_hit_01.ogg"), f("75-cc0-breaking-falling-hit-sfx/bfh1_glass_hit_02.ogg")],
                    "glass", -12, {"max_dur": .5}),
    "streak": ([f(p_) for k in range(4) for p_ in (f"sci-fi-sounds/Audio__computerNoise_00{3 - k}.ogg",)] + r8("sfx_sounds_interaction")[:4],
               "glitch", -12, {"max_dur": .2}),
    "ghost": ([f("wind-hit-time-morph/qubodup-slomo1.wav")], "whoosh", -6, {"max_dur": 1.2}),
    "pixel_start": (r8("sfx_sounds_powerup1."), "ui", -10, {}),
    "pixel_walk": (r8("sfx_movement_footsteps"), "foley", -9, {"anchor": "start"}),
    "pixel_hold": (r8("menu_select1"), "ui", -9, {}),
    "pixel_shot": (r8("sfx_weapon_singleshot1."), "hit", -3, {}),
    "pixel_hit": (r8("sfx_damage_hit1."), "hit", -7, {}),
    "pixel_fall": (r8("sfx_sounds_falling1."), "foley", -7, {}),
    "diamond": (r8("sfx_coin_single"), "coin", -9, {}),
    "heart": (r8("sfx_sounds_powerup2."), "ui", -12, {}),
}
SKIP = {"keyword"}
PIXEL = {"pixel_walk", "pixel_hold", "pixel_shot", "pixel_hit", "pixel_fall", "diamond", "heart", "throw", "pixel_start"}
PIXEL_TRIM = -6.0   # v16: the owner wants every pixel-illustration sound quieter
# v15: the owner found the transition whooshes too light. Every cut whoosh is pitched down and gets a low impact
# under it (a lowpassed explosion / bang / thump, rotated so the sub layer is not one sample on repeat).
SUBS = ["sci-fi-sounds/Audio__lowFrequency_explosion_000.ogg", "25-cc0-bang-firework-sfx/bang_03.ogg",
        "sci-fi-sounds/Audio__lowFrequency_explosion_001.ogg", "75-cc0-breaking-falling-hit-sfx/bfh1_falling_02.ogg",
        "100-cc0-sfx/explosion.ogg", "25-cc0-bang-firework-sfx/bang_07.ogg"]
WEIGHT = {"whoosh": (-3, -5), "swish": (-2, -8), "whoosh_big": (-4, -2)}   # (pitch semitones, sub layer gain)
LIFT = 2.0          # critique round 3: the median sound sat -13 dB under the song (target -12..+2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=os.path.join(ROOT, "cache", "sfx", "cues.json"))
    a = ap.parse_args()
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    rot = {k: itertools.cycle(v[0]) for k, v in KINDS.items()}
    if "streak" in KINDS:                                   # interleave the two streak families
        st = KINDS["streak"][0]
        rot["streak"] = itertools.cycle([x for pair in zip(st[:4], st[4:]) for x in pair])
    cues, last_cam, n_dia, uses = [], [], 0, {}
    busy = sorted(e["t"] for e in ev if e["type"] not in SKIP | {"sticker", "camera", "diamond", "heart"})
    hard = [e["t"] for e in ev if e["type"] in ("pixel_shot", "boom")]
    seen = set()
    for e in ev:
        k, t = e["type"], e["t"]
        if (k, round(t, 2)) in seen:                       # the same moment listed twice
            continue
        seen.add((k, round(t, 2)))
        if k in SKIP or k not in KINDS:
            continue
        if k == "camera":                                  # two clicks per clip
            if sum(1 for x in last_cam if t - x < 2.6) >= 1:
                continue
            last_cam.append(t)
        if k == "diamond":
            n_dia += 1
            if n_dia % 3 != 1:
                continue
        if k == "hit" and any(abs(t - h) < .25 for h in hard):   # the bang / the drop already carry this flash
            continue
        if k == "glitch" and any(e2["type"].startswith(("whoosh", "swish")) and abs(e2["t"] - t) < .12 for e2 in ev):
            continue                                       # a cut already has its whoosh: the flash rides on it
        if k == "heart":
            if any(c["label"] == "heart" and t - c["t"] < .45 for c in cues):
                continue
        if k == "sticker" and any(c["label"] == "sticker" for c in cues):
            continue                                       # v16: one paper slap in the whole edit (owner)
        if k == "hit" and any(e2["type"].startswith(("whoosh", "swish")) and abs(e2["t"] - t) < .15 for e2 in ev):
            continue                                       # a burst's white frame on a cut that already has its whoosh + sub
        if k == "sticker" and any(abs(t - x) < .35 for x in busy):  # a sticker landing under a cut or a hit is lost anyway
            continue
        files, role, gain, extra = KINDS[k]
        if k == "pixel_hit":
            t += .08                                       # 70 ms after the shot smeared into it
        fn = next(rot[k])
        n = uses.get(fn, 0)
        uses[fn] = n + 1
        c = {"t": t, "label": k, "file": fn, "role": role, "gain_db": gain + LIFT + (PIXEL_TRIM if k in PIXEL else 0)} | extra
        if n and "pitch" not in c and k not in ("phone", "fire", "smoke"):
            c["pitch"] = (0, -1, 1, -2, 2)[n % 5]              # a repeat is a new take, not the same file twice
        if fn.endswith(("whoosh2_0.wav", "weird_whoosh_sounds_-_whoosh_12_0.mp3")):
            c["slice"] = [0.0, .9] if fn.endswith("whoosh2_0.wav") else [.25, .85]
        if k in WEIGHT:
            pt, sub_gain = WEIGHT[k]
            c["pitch"] = max(-12, c.get("pitch", 0) + pt)
            sub = SUBS[sum(1 for x in cues if x.get("layers")) % len(SUBS)]
            c["layers"] = [{"dt": 0.0, "file": f(sub), "role": "hit", "gain_db": sub_gain + LIFT,
                            "lowpass": 320, "max_dur": .55, "fade_out": .2}]
        if e.get("len") and k in ("phone", "fire", "smoke", "pixel_walk"):
            c["max_dur"] = e["len"]
        cues.append(c)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({"video": os.path.abspath(a.video), "keep_audio": "yes", "cues": cues}, open(a.out, "w"), indent=1)
    by = {}
    for c in cues:
        by[c["label"]] = by.get(c["label"], 0) + 1
    print(f"{len(cues)} cues -> {a.out}", by)


if __name__ == "__main__":
    main()
