"""(Copied from reel-flop-9x16.)
Cue sheet for the real-sfx skill's mix.py: plan/sfx_events.json (build/generate.py) -> real CC0 recordings.
House rule: Openverse first; its sound effects are Freesound files, which refuse downloads from cloud sessions, so the
CC0 OpenGameArt library built for Spin Bout U is used (../spin-bout-u-drake/assets/sfx/oga; CC0, no credit needed).
python3 build/sfx_sheet.py VIDEO.mp4 [--out renders/cues.json]
"""
import argparse
import itertools
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(os.path.dirname(ROOT), "spin-bout-u-drake", "assets", "sfx", "oga")
TS = "fantasy-sound-effects-tinysized-sfx/sfx-cc0__"


def f(rel):
    p = os.path.join(L, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing sound: {rel}")
    return p


KINDS = {
    "whoosh_big": ([f("wind-hit-time-morph/qubodup-megaswosh1.wav"), f("wind-hit-time-morph/60009__qubodup__swosh_22.flac")], "whoosh", -14, {"max_dur": .7}),
    "whoosh": ([f("swishes-sound-pack/swishes__swish-4.wav"), f(TS + "tube-plastic-whoosh-02.wav"), f("swishes-sound-pack/swishes__swish-8.wav")],
               "whoosh", -16, {"max_dur": .5}),
    "swish": ([f("swishes-sound-pack/swishes__swish-6.wav"), f("swishes-sound-pack/swishes__swish-4.wav")], "whoosh", -18, {"max_dur": .4}),
    "pop": ([f("100-cc0-sfx/plop_01.ogg"), f("100-cc0-sfx/plop_02.ogg"), f("ui-sounds/button1.ogg")], "pop", -17, {"max_dur": .3}),
    "hit": ([f("100-cc0-sfx/hit_01.ogg")], "hit", -16, {"max_dur": .35}),
    "alert": ([f("interface-sounds/Audio__bong_001.ogg")], "ui", -18, {"max_dur": .6}),
    "stamp": ([f("75-cc0-breaking-falling-hit-sfx/bfh1_hit_02.ogg")], "hit", -15, {"max_dur": .4}),
    "tick": ([f("interface-sounds/Audio__click_002.ogg")], "ui", -20, {"max_dur": .2}),
    "success": ([f("interface-sounds/Audio__confirmation_001.ogg")], "ui", -16, {"max_dur": .6}),
    "drop": ([f("interface-sounds/Audio__drop_002.ogg")], "ui", -15, {"max_dur": .6}),
    "sparkle": ([f("bell-dingschimes/bell_ding2.wav")], "chime", -20, {"max_dur": 1.0, "fade_out": .4}),
    "click": ([f("ui-sounds/button2.ogg")], "ui", -15, {"max_dur": .3}),
    "type": ([f("interface-sounds/Audio__click_001.ogg"), f("interface-sounds/Audio__click_003.ogg")], "ui", -19, {"max_dur": .15}),
    "rise": ([f("fantasy-magic-spell/fantasy_magic_button_1.mp3")], "chime", -19, {"max_dur": .9, "fade_out": .3}),
    "ding": ([f("ui-sounds/complete.ogg")], "ui", -15, {"max_dur": 1.0}),
    "notify": ([f("interface-sounds/Audio__confirmation_002.ogg")], "ui", -15, {"max_dur": .7}),
    # reel-flop additions: the "reel dies" moments (strike-through, freeze, swipe-away), the 3-2-1 countdown
    "error": ([f("interface-sounds/Audio__error_004.ogg")], "ui", -16, {"max_dur": .5}),
    "glitch": ([f("interface-sounds/Audio__glitch_002.ogg"), f("interface-sounds/Audio__glitch_003.ogg")], "ui", -15, {"max_dur": .45}),
    "scratch": ([f("interface-sounds/Audio__scratch_003.ogg")], "ui", -15, {"max_dur": .45}),
    "count": ([f("interface-sounds/Audio__tick_002.ogg")], "ui", -16, {"max_dur": .25}),
    # v3 cold open: the screen cracks on "lose", shatters on "you."
    "crack": ([f("100-cc0-sfx-2/sfx100v2_glass_04.ogg")], "hit", -12, {"max_dur": .3}),
    "shatter": ([f("100-cc0-sfx/glass_05.ogg")], "hit", -12, {"max_dur": 1.0, "fade_out": .3}),
    # v4 papercraft: paper handling for the scraps / strips / cards, a real paper rip for the tears
    "paper": ([f("100-cc0-sfx/paper_01.ogg"), f("100-cc0-sfx/paper_02.ogg"), f("100-cc0-sfx/paper_03.ogg"), f("100-cc0-sfx/paper_04.ogg")], "foley", -14, {"max_dur": .45}),
    "rip": ([f("202-more-sound-effects/Paper _ Stationery__Stationery_44.wav")], "foley", -8, {"max_dur": .9, "fade_out": .25}),
    "logo": ([f("wind-hit-time-morph/qubodup-megaswosh2.wav")], "whoosh", -16, {"reverse": True, "max_dur": .6, "anchor": "end"}),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=os.path.join(ROOT, "renders", "cues.json"))
    a = ap.parse_args()
    ev = json.load(open(os.path.join(ROOT, "plan", "sfx_events.json")))
    rot = {k: itertools.cycle(v[0]) for k, v in KINDS.items()}
    cues, uses, last = [], {}, {}
    for e in ev:
        k, t = e["type"], e["t"]
        if k not in KINDS or t - last.get(k, -9) < (.06 if k == "type" else .2):
            continue
        last[k] = t
        files, role, gain, extra = KINDS[k]
        fn = next(rot[k])
        n = uses.get(fn, 0)
        uses[fn] = n + 1
        c = {"t": max(0.0, t), "label": k, "file": fn, "role": role, "gain_db": gain} | extra
        if n and k != "type":
            c["pitch"] = (0, -1, 1, -2, 2)[n % 5]
        cues.append(c)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({"video": os.path.abspath(a.video), "keep_audio": "yes", "cues": cues}, open(a.out, "w"), indent=1)
    print(f"{len(cues)} cues -> {a.out}")


if __name__ == "__main__":
    main()
