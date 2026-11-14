"""Music, Cree's gibberish voice, sound design and the mastered mix for the Creedom "I Wish..." reel.

Score (CC BY 3.0, Jamendo, found through Openverse; all instrumental, checked with faster-whisper), cut as a cue sheet for
tension and relief: "Emotional - Piano Instrumental" by E. Erkut under the breakdown; "Suspense and Tension" (stem 5) by
3minutetunes building through the wishes and teasers; a hush (near silence) while the lights die; "Helios Tilt" by CM ONNI
for the entrance, its drop placed on the superhero landing; "Inspiring Progress" by Soundrider/Dope for the fixes and hug.
Cree never says real words: his voice is built here from real bird chirps (CC0 / CC BY recordings found through Openverse,
cut into single chirps by build/cree_syllables.py; see assets/sfx/cree/CREDITS.md), strung into little "words" with a
contour, timed to build/chirps.json, while the speech clouds on screen say what he means. SFX: HyperFrames' bundled library
(Pixabay Content License) and an ElevenLabs room tone from the owner's earlier reels. Music ducks under the voice.
python3 build/audio.py      (from the project root, after build/voice.py and build/generate.py)
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import butter, resample, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "media-use", "audio", "assets", "sfx")
SR = 48000
CU = json.load(open(os.path.join(ROOT, "build", "cues.json")))
CH = json.load(open(os.path.join(ROOT, "build", "chirps.json")))["chirps"]
DUR = CU["end"]
N = int(DUR * SR)
Ls = lambda k: CU["lines"][k][0]  # noqa: E731
Le = lambda k: CU["lines"][k][1]  # noqa: E731
Bs = lambda k: CU["beats"][k][0]  # noqa: E731
Be = lambda k: CU["beats"][k][1]  # noqa: E731


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def put(bus, x, t, g=1.0, a=0.0, b=None, fin=.02, fout=.05):
    x = x[int(a * SR):int(b * SR) if b else None].copy()
    if len(x) == 0:
        return
    fi, fo = min(len(x), int(fin * SR)), min(len(x), int(fout * SR))
    if fi: x[:fi] *= np.linspace(0, 1, fi)[:, None]
    if fo: x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    i = int(round(t * SR))
    if i < 0:
        x, i = x[-i:], 0
    x = x[: max(0, N - i)]
    bus[i:i + len(x)] += x * g


def lp(x, f, kind="low"):
    return np.stack([sosfilt(butter(2, f, kind, fs=SR, output="sos"), x[:, c]) for c in (0, 1)], 1)


SYL = json.load(open(os.path.join(ROOT, "assets", "sfx", "cree", "syllables.json")))
_SYLC = {}


def syl(name):
    if name not in _SYLC:
        _SYLC[name], _ = sf.read(os.path.join(ROOT, "assets", "sfx", "cree", "syl", name))
    return _SYLC[name]


def shift(x, semis):
    """Pitch by resampling (pitch and length move together, as in a real bird's call)."""
    r = 2 ** (semis / 12)
    n = max(8, int(len(x) / r))
    pad = np.concatenate([np.zeros(256), x, np.zeros(256)])
    y = resample(pad, int(len(pad) / r))
    return y[int(256 / r): int(256 / r) + n]


def chirp_phrase(dur, seed, mood="talk"):
    """Cree's voice from real chirps: little 'words' of 2-4 chirps, short pauses between them, a contour across the phrase.
    mood: talk (falls at the end), happy (brighter, rises at the end), proud (one long confident trill), tiny (one or two)."""
    rng = np.random.default_rng(seed)
    peeps = [r for r in SYL if r["src"] == "src_003"]
    sweet = [r for r in SYL if r["src"] in ("src_001", "src_006", "src_002")]
    trill = [r for r in SYL if r["src"] == "src_005"]
    y = np.zeros(int((dur + .4) * SR)); t = 0.0
    base = {"talk": -2.0, "happy": -0.5, "proud": -2.5, "tiny": -1.0}[mood]
    words = []
    while t < dur - .08:
        nw = int(rng.integers(2, 5)) if mood != "tiny" else int(rng.integers(1, 3))
        words.append(nw); t += nw * .1 + .12
    total = sum(words); k = 0; t = 0.0
    for wi, nw in enumerate(words):
        for j in range(nw):
            u = k / max(1, total - 1)
            if mood in ("happy",): contour = 1.6 * u + .8 * np.sin(u * 3.1)
            elif mood == "proud": contour = 1.2 * np.sin(u * 3.1)
            else: contour = 1.4 * np.sin(u * 2.6) - 1.8 * max(0, u - .75) / .25
            pool = peeps if rng.random() < .62 else (sweet if rng.random() < .7 else trill)
            if mood == "proud" and wi == len(words) - 1 and j == nw - 1: pool = trill
            r = pool[int(rng.integers(0, len(pool)))]
            x = syl(r["file"]) * (1.0 if j == 0 else .78) * 10 ** (rng.uniform(-2.5, 1.0) / 20)
            # keep every chirp near 3.2 kHz before the contour, so the sources sit together as one voice
            norm = 12 * np.log2(3200 / max(1500, r["dom"]))
            x = shift(x, float(np.clip(norm, -7, 4)) + base + contour + rng.uniform(-.8, .8))
            i = int(t * SR)
            if i + len(x) > len(y): break
            y[i:i + len(x)] += x
            t += len(x) / SR + rng.uniform(.018, .05)
            k += 1
        t += rng.uniform(.08, .15)
        if t > dur: break
    y = y[: int(dur * SR) + int(.2 * SR)]
    y = sosfilt(butter(4, [1500, 8500], "band", fs=SR, output="sos"), y)
    # a touch of the room around him
    ir = np.random.default_rng(3).standard_normal(int(.18 * SR)) * np.exp(-np.arange(int(.18 * SR)) / (.04 * SR))
    wet = np.convolve(y, ir)[: len(y)]
    y = y + .06 * wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(y))
    return np.stack([y, y], 1)


def buzz(dur):
    tt = np.arange(int(dur * SR)) / SR
    on = ((tt % .5) < .32).astype(float)
    y = np.sin(2 * np.pi * 150 * tt) * (.6 + .4 * np.sign(np.sin(2 * np.pi * 37 * tt))) * on
    y = sosfilt(butter(2, [90, 900], "band", fs=SR, output="sos"), y) * .5
    return np.stack([y, y], 1)


def music():
    m = np.zeros((N, 2))
    L = lambda f: load(os.path.join(ROOT, "assets", "music", f))  # noqa: E731
    hero = Bs("hero"); land = hero + 2.75 + .28; burst = hero + .7
    w1 = Ls("04")
    put(m, L("s_emotional.mp3"), 0, 1.0, 3.0, 3.0 + w1 + .3, fin=.3, fout=.9)                       # the breakdown
    sus = L("t_susp5.mp3"); seg = hero - (w1 - .6)
    put(m, sus * 1.1, w1 - .6, 1.0, 56.0 - seg, 56.0, fin=1.0, fout=.12)                            # building to the hush
    put(m, L("h_helios.mp3") * .9, burst, 1.0, 12.0 - (land - burst), 12.0 - (land - burst) + (Bs("fix1") - burst) + .6, fin=.05, fout=.7)   # the drop lands on the landing
    up = L("u_progress.mp3"); seg2 = DUR - Bs("fix1") + .3
    put(m, up * .8, Bs("fix1") - .1, 1.0, 8.0, 8.0 + seg2, fin=.6, fout=1.5)                        # the fixes, the hug, the end
    return m


MOODS = ["proud", "talk", "happy", "talk", "happy", "happy"]
EXTRA = [                                                     # (time, mood, gain, seed): little reactions outside the clouds
    (Bs("teaser2") + .55, "tiny", .35, 101),                 # a distant chirp as he streaks past
    (Bs("hero") + 1.62, "tiny", .7, 103),                    # a heroic chirp through the window
    (Bs("hero") + 3.85, "proud", .8, 105),                   # the proud chirp as he rises from the landing
    (Bs("fix1") + 1.9, "tiny", .6, 107),                     # found it: second three
    (Bs("fix2") + 1.65, "tiny", .65, 109),                   # the gold card
    (Bs("fix3") + 1.35, "happy", .7, 111),                   # the cheer
]   # say no more / second three / make more / DM goes out / waiting for you / end card


def cree():
    c = np.zeros((N, 2))
    for k, (a, b) in enumerate(CH):
        put(c, chirp_phrase(b - a, 11 + k * 7, MOODS[k] if k < len(MOODS) else "talk"), a, 1.0, fin=.002, fout=.03)
    for t, mood, g, seed in EXTRA:                     # little reactions outside the speech clouds (also move his beak)
        put(c, chirp_phrase(.3 if mood == "tiny" else .55, seed, mood), t, g, fin=.002, fout=.03)
    return c


def sfx():
    s = np.zeros((N, 2))
    S = lambda n: load(os.path.join(ROOT, "assets", "sfx", n + ".mp3"))  # noqa: E731
    lib = lambda n: load(os.path.join(LIB, n + ".mp3"))  # noqa: E731
    reps = int(np.ceil(DUR * SR / len(S("room_tone")))) + 1
    put(s, lp(np.concatenate([S("room_tone")] * reps)[:N], 1400), 0, .3, fin=.05, fout=.8)
    put(s, lib("pop"), .45, .3)                                                        # 42 views
    put(s, lib("whoosh-short"), Le("01") + .1, .25)                                    # he slides off the chair
    put(s, lib("impact-bass-2"), Bs("thud") + .2, .35)                                 # face-down on the desk
    put(s, lib("click-soft"), Bs("thud") + 1.65, .3)                                    # the pen hits the floor
    for k in ("04", "05", "06"):
        put(s, lib("chime"), Ls(k) - .05, .12)                                         # the wish chips
    put(s, lib("whoosh-cinematic"), Bs("teaser1") + .4, .14)                          # teaser 1: a far-off streak
    put(s, lib("sparkle"), Bs("teaser1") + .9, .12)
    put(s, lib("whoosh"), Bs("teaser2") + .25, .35)                                   # teaser 2: he whooshes past the window
    put(s, lib("whoosh-short"), Bs("teaser2") + .65, .2)                              # papers lift
    put(s, buzz(Le("06") - Ls("06") + .2), Ls("06") - .1, .12)                         # the phone buzzing on the bed
    put(s, lib("riser"), Bs("hero") - 1.6, .25)                                       # tension into the hush
    for k in range(3):
        put(s, lib("click-soft"), Bs("hero") + .1 + k * .13, .25)                         # the lights flicker out
    put(s, lib("whoosh-cinematic"), Bs("hero") + .7, .3)                                  # the rise: wind, the silhouette in the window
    put(s, lib("sparkle"), Bs("hero") + 1.12, .3)                                         # his eyes glint
    put(s, lib("impact-bass-2"), Bs("hero") + 1.55, .5); put(s, lib("glitch-1"), Bs("hero") + 1.56, .1)   # the window blows open
    put(s, lib("sparkle"), Bs("hero") + 1.6, .22)                                         # glass glints
    put(s, lib("whoosh"), Bs("hero") + 1.7, .5)                                           # he rockets in
    put(s, lib("whoosh-short"), Bs("hero") + 2.05, .35)                                   # the barrel roll
    put(s, lib("whoosh-short"), Bs("hero") + 2.35, .3)                                    # the turn
    put(s, lib("whoosh"), Bs("hero") + 2.72, .45)                                         # the drop
    put(s, lib("impact-bass-1"), Bs("hero") + 2.75 + .28, .65)                            # the superhero landing (on the music's drop)
    for k in range(5):
        put(s, lib("click-soft"), Bs("hero") + 3.12 + k * .07, .12)                       # the lights come back, one by one
    put(s, lib("sparkle"), Bs("hero") + 3.3, .25)
    put(s, lib("ping"), Bs("hero") + 3.97, .18)                                           # the eye glint
    put(s, lib("pop"), Bs("fix1") + 1.75, .3); put(s, lib("ping"), Bs("fix1") + 1.85, .3)                  # tap, the tag
    put(s, lib("whoosh-short"), Bs("fix2") + .1, .25); put(s, lib("chime"), Bs("fix2") + 1.5, .3)          # the cards, gold
    put(s, lib("click"), Bs("fix3") + .8, .45); put(s, lib("ping"), Bs("fix3") + .9, .25)                  # the lever, the switch
    for i in range(6):
        put(s, lib("whoosh-short"), Bs("fix3") + 1.0 + i * .28, .12)                                       # paper planes
    put(s, lib("notification"), Bs("fix3") + 1.4, .2)
    put(s, lib("sparkle"), Ls("10") + .1, .2)                                                              # the hug
    put(s, lib("pop"), Bs("endin") + .15, .3); put(s, lib("typing"), Bs("endin") + .85, .25, 0, .9); put(s, lib("click"), Bs("endin") + 1.95, .35)
    return s


def ffmpeg(*a):
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", *a], capture_output=True, text=True, check=True)


def main():
    voice, vsr = sf.read(os.path.join(ROOT, "assets", "audio", "voice.wav"))
    assert vsr == SR
    v = np.zeros(N); v[: min(N, len(voice))] = voice[:N]
    rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)  # noqa: E731
    tt = np.arange(N) / SR
    talk = np.zeros(N)
    for a, b in list(CU["lines"].values()) + CH:
        talk = np.maximum(talk, np.clip((tt - (a - .2)) / .2, 0, 1) * np.clip(((b + .3) - tt) / .3, 0, 1))
    m, c, s = music(), cree(), sfx()
    def env(x):
        hop = SR // 30; n = len(x) // hop
        r = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
        ref = np.percentile(r[r > 1e-4], 95) if np.any(r > 1e-4) else 1
        return [round(float(min(1, v / ref)), 2) for v in r]
    json.dump({"voice": env(v), "cree": env(c[:, 0])}, open(os.path.join(ROOT, "build", "env.json"), "w"))
    m = m * (.13 / rms(m)) * (1 - .6 * talk)[:, None]
    s = s * (.07 / rms(s))
    c = c * (.16 / rms(c[np.abs(c[:, 0]) > 1e-4]))
    mix = m + s + c + (v * (.17 / rms(v[v != 0])))[:, None]
    fade = np.ones(N); fade[-int(.5 * SR):] = np.linspace(1, 0, int(.5 * SR))
    mix *= fade[:, None]
    mix *= min(1, .98 / np.max(np.abs(mix)))
    raw = os.path.join(ROOT, "assets", "audio", "mix_raw.wav")
    sf.write(raw, mix.astype(np.float32), SR, subtype="FLOAT")
    o = ffmpeg("-i", raw, "-af", "loudnorm=I=-13.7:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-").stderr
    meas = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-13.7:TP=-2.0:LRA=11:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
          f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out = os.path.join(ROOT, "assets", "audio", "mix.wav")
    ffmpeg("-i", raw, "-af", af + ",alimiter=limit=0.78:level=false:attack=1:release=60", "-ar", str(SR), "-c:a", "pcm_s24le", out)
    os.remove(raw)
    chk = ffmpeg("-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    summ = chk[chk.rindex("Summary:"):]
    print("wrote", out, " ".join(ln.strip() for ln in summ.splitlines() if ln.strip().startswith(("I:", "Peak:"))))


if __name__ == "__main__":
    main()
