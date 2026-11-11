"""Sound kinds for the GTA 6 x Claude reel: plan/sfx_events.json (build/generate.py) -> real recordings.
House rule: Openverse first (sfx/search/*.json). Its sound-effect results are Freesound files, whose server refuses
downloads from cloud sessions (403; we never pose as a browser), so the effects are OpenGameArt packs:
  * car sounds fetched for this reel by build/oga_sfx.py into sfx/oga/ (credits in plan/sfx_credits_oga.json;
    the tyre squeal and the boost are qubodup, CC BY 3.0: credit them in the post)
  * the CC0 library built for Spin Bout U (../spin-bout-u-drake/assets/sfx/oga) for whooshes, hits, typing and UI.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAR = os.path.join(ROOT, "sfx", "oga")
L = os.path.join(os.path.dirname(ROOT), "spin-bout-u-drake", "assets", "sfx", "oga")


def f(rel, base=L):
    p = os.path.join(base, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing sound: {rel}")
    return p


def c(rel):
    return f(rel, CAR)


# kind: ([sources], max_dur, extra) ; one-shots. "engine" and "squeal" are beds, built in sfx_mix.py.
KINDS = {
    "whoosh_big": ([f("wind-hit-time-morph/qubodup-megaswosh1.wav"), f("wind-hit-time-morph/60009__qubodup__swosh_22.flac")], .7, {}),
    "whoosh": ([f("swishes-sound-pack/swishes__swish-4.wav"), f("swishes-sound-pack/swishes__swish-8.wav"),
                f("fantasy-sound-effects-tinysized-sfx/sfx-cc0__tube-plastic-whoosh-02.wav")], .45, {}),
    "swish": ([f("swishes-sound-pack/swishes__swish-6.wav"), f("swishes-sound-pack/swishes__swish-4.wav")], .4, {}),
    "stamp": ([f("150-combat-sound-effects/01_combat_melee__impact_punch_heavy_001_48kHz_16bit_0.54s_fb104b0a_s02.wav")], .45, {}),
    "hit": ([f("150-combat-sound-effects/03_explosions_destruction__BlastImpact_03_s01.wav")], 1.0, {"fade_out": .4}),
    "bass": ([f("sci-fi-sounds/Audio__lowFrequency_explosion_000.ogg")], 1.6, {"fade_out": .6}),
    "tick": ([f("interface-sounds/Audio__click_002.ogg")], .2, {}),
    "type": ([f("interface-sounds/Audio__click_001.ogg"), f("interface-sounds/Audio__click_003.ogg")], .15, {}),
    "click": ([f("ui-sounds/button2.ogg")], .3, {}),
    "success": ([f("interface-sounds/Audio__confirmation_001.ogg")], .6, {}),
    "rise": ([f("wind-hit-time-morph/qubodup-megaswosh2.wav")], 1.2, {"reverse": True, "anchor": "end"}),
    "boost": ([c("racing-speed-boost-sound/boost-ogg__boost-start.ogg")], .6, {}),
    "siren": ([c("sirens-and-alarm-noise/siren_0.mp3")], 2.4, {"start": 6.0, "fade_in": .3, "fade_out": .8}),
}
ENGINE = c("racing-car-engine-sound-loops/loop_4_0.wav")
SQUEAL = c("car-tire-squeal-skid-loop/tires_squal_loop.wav")
