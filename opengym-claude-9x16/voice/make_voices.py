"""Expressive open-source voiceovers for the openGym x Claude reel.

Made for a small GPU (the laptop's RTX 3050 has 4 GB of VRAM); everything also runs on the CPU, only slower.

Engines (all open source, commercial use allowed):
  kokoro            hexgrad Kokoro-82M (Apache-2.0): small and fast, with natural American male voices
                    (am_adam, am_echo, am_eric, am_fenrir, am_liam, am_michael, am_onyx, am_puck). Designs the two voices.
  chatterbox        Resemble AI Chatterbox (MIT): clones a designed voice and acts each line, with an `exaggeration`
                    knob for emotion intensity. Default for the lines.
  chatterbox-turbo  Chatterbox Turbo (MIT), if the installed chatterbox-tts ships it: smaller and faster, and it reads
                    sound tags such as [laugh] and [sigh]. Check the tag list in its model card before relying on it.
  dia               Nari Labs Dia-1.6B (Apache-2.0): dialogue with real non-verbals, but it needs far more than 4 GB of
                    VRAM. Only for a bigger GPU.

Steps (from the repo root, inside the voice venv):
  python opengym-claude-9x16/voice/make_voices.py design
      -> voice/design/{nxt,human}_<voice>.wav, one sample per Kokoro voice. Listen and pick one per character.
  python opengym-claude-9x16/voice/make_voices.py lines --nxt am_puck --human am_liam [--takes 3] [--device cpu]
      -> voice/lines/<nn>_<speaker>_t<k>.wav: every line, `takes` versions each, acted in the picked voices.
  python opengym-claude-9x16/voice/make_voices.py assemble [--pick 03=2 07=1]
      -> assets/audio/voice_nxt.wav, voice_human.wav, voice.wav (both, timed) and voice/lines.json (start/end per line).
         By default take 1 of each line; --pick chooses another take for a line; --tempo 1.06 speeds every line up
         (pitch kept) when the voice runs over the 33.5 s budget.

NXT gets a light robot colour (a subtle chorus and a short metallic echo) in assemble; --no-robot turns it off.
Every line is loudness-matched (-16 LUFS) and resampled to 48 kHz, so the mix stays even.
"""
import argparse
import json
import os
import random
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
SR = 48000

# (speaker, line with non-verbals in parentheses, chatterbox exaggeration, chatterbox cfg_weight, gap after in seconds)
# Higher exaggeration = more emotion; lower cfg_weight = faster, looser pacing (keep it low when exaggeration is high).
LINES = [
    ("human", "(sighs) Ugh... my gym app wants me to upgrade. Again.", .65, .35, .10),
    ("nxt", "Delete it. This one's free... forever. And Claude helped build it.", .75, .35, .08),
    ("human", "(gasps) Wait. Claude built a gym app?", .85, .30, .08),
    ("nxt", "openGym. Open source. No subscription, no ads, no account.", .70, .40, .10),
    ("nxt", "Plug in Claude as your coach...", .60, .40, .06),
    ("human", "Four days. Dumbbells. Build muscle.", .55, .40, .06),
    ("nxt", "...and it plans your whole week. You just approve it.", .70, .35, .10),
    ("nxt", "Fifty-six hundred exercises with demos. Weights pre-filled. It even adds weight when you're ready.", .80, .30, .10),
    ("human", "And that muscle map?", .60, .35, .06),
    ("nxt", "Worked. Recovering. Untrained... Legs, bro.", .85, .30, .04),
    ("human", "(laughs) Fair.", .90, .30, .14),
    ("nxt", "Comment GYM. I'll DM you the official links... and my Claude prompt.", .70, .35, .00),
]

# Reference lines used to design each voice (about 8 s of speech in character; Chatterbox clones from these).
DESIGN = {
    "nxt": "Relax, I've got this. Your whole week, planned in seconds. Trust me, leg day is coming for you.",
    "human": "Bro, I'm so tired of these apps. Every week it's upgrade this, premium that. I just want to lift, man.",
}
KOKORO_VOICES = ["am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael", "am_onyx", "am_puck"]
ROBOT_FX = "highpass=f=90,chorus=0.7:0.9:22|34:0.22|0.18:0.30|0.24:1.6|2.1,aecho=0.85:0.5:8:0.12"


def seed_all(s):
    import numpy as np
    import torch
    random.seed(s)
    np.random.seed(s)
    torch.manual_seed(s)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(s)


def device(a):
    import torch
    return a.device or ("cuda" if torch.cuda.is_available() else "cpu")


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


DIA_ARGS = dict(use_torch_compile=False, verbose=False, cfg_scale=3.0, temperature=1.8, top_p=0.90, cfg_filter_top_k=50)


def dia_model():
    from dia.model import Dia
    return Dia.from_pretrained("nari-labs/Dia-1.6B-0626", compute_dtype="float16")


def design(a):
    import numpy as np
    import soundfile as sf
    out = os.path.join(HERE, "design")
    os.makedirs(out, exist_ok=True)
    if a.engine == "kokoro":
        from kokoro import KPipeline
        pipe = KPipeline(lang_code="a", device=device(a))          # "a" = American English
        for v in a.voices:
            for who, text in DESIGN.items():
                audio = np.concatenate([np.asarray(chunk) for _, _, chunk in pipe(text, voice=v, speed=1.0)])
                p = os.path.join(out, f"{who}_{v}.wav")
                sf.write(p, audio, 24000)
                print("wrote", p)
    else:
        m = dia_model()
        for s in a.seeds:
            for who, text in DESIGN.items():
                seed_all(s)
                p = os.path.join(out, f"{who}_seed{s}.wav")
                m.save_audio(p, m.generate(f"[S1] {text}", **DIA_ARGS))
                print("wrote", p)


def ref_for(a, who):
    """The clip (and its transcript, for Dia) that every line of this character is cloned from."""
    ext = getattr(a, f"{who}_ref")
    if ext:
        return ext, getattr(a, f"{who}_ref_text")
    pick = getattr(a, who)
    if not pick:
        raise SystemExit(f"pick a voice: --{who} <name from voice/design, e.g. am_puck or seed23> or --{who}-ref clip.wav")
    p = os.path.join(HERE, "design", f"{who}_{pick}.wav")
    if not os.path.exists(p):
        raise SystemExit(f"missing {p}: run design first")
    return p, DESIGN[who]


def speakable(t, turbo=False):
    """Chatterbox reads non-verbals aloud, so turn them into sounds (Turbo: into its sound tags)."""
    if turbo:
        t = t.replace("(laughs)", "[laugh]").replace("(sighs)", "[sigh]").replace("(gasps)", "[gasp]")
    else:
        t = t.replace("(laughs)", "Haha,").replace("(sighs)", "Hhh...").replace("(gasps)", "Oh!")
    return re.sub(r"\([^)]*\)", "", t).strip()


def lines(a):
    out_dir = os.path.join(HERE, "lines")
    os.makedirs(out_dir, exist_ok=True)
    refs = {w: ref_for(a, w) for w in ("nxt", "human")}
    dev = device(a)
    if a.engine == "dia":
        m = dia_model()
    elif a.engine == "chatterbox-turbo":
        try:
            from chatterbox.tts_turbo import ChatterboxTurboTTS
        except ImportError:
            raise SystemExit("this chatterbox-tts has no Turbo model; upgrade it (pip install -U chatterbox-tts) "
                             "or use --engine chatterbox")
        m = ChatterboxTurboTTS.from_pretrained(device=dev)
    else:
        from chatterbox.tts import ChatterboxTTS
        m = ChatterboxTTS.from_pretrained(device=dev)
    if a.engine != "dia":
        import torchaudio
    for i, (who, text, ex, cfg, _) in enumerate(LINES, 1):
        if a.only and i not in a.only:
            continue
        ref_wav, ref_text = refs[who]
        for k in range(1, a.takes + 1):
            seed_all(1000 * i + k)
            p = os.path.join(out_dir, f"{i:02d}_{who}_t{k}.wav")
            if a.engine == "dia":
                # clone: the prompt transcript, then the new line, both as the same speaker [S1]
                m.save_audio(p, m.generate(f"[S1] {ref_text} [S1] {text}", audio_prompt=ref_wav, **DIA_ARGS))
            elif a.engine == "chatterbox-turbo":
                torchaudio.save(p, m.generate(speakable(text, True), audio_prompt_path=ref_wav), m.sr)
            else:
                wav = m.generate(speakable(text), audio_prompt_path=ref_wav, exaggeration=ex, cfg_weight=cfg)
                torchaudio.save(p, wav, m.sr)
            print("wrote", p)


def duration(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def assemble(a):
    import numpy as np
    import soundfile as sf
    picks = dict(x.split("=") for x in a.pick)
    tmp = os.path.join(HERE, "norm")
    os.makedirs(tmp, exist_ok=True)
    tracks = {"nxt": [], "human": []}
    timeline, t = [], .15
    for i, (who, text, _, _, gap) in enumerate(LINES, 1):
        k = picks.get(f"{i:02d}", "1")
        src = os.path.join(HERE, "lines", f"{i:02d}_{who}_t{k}.wav")
        dst = os.path.join(tmp, f"{i:02d}.wav")
        fx = "" if who != "nxt" or a.no_robot else ROBOT_FX + ","
        fx = (f"atempo={a.tempo}," if a.tempo != 1 else "") + fx
        if a.max_pause:   # shorten long pauses inside the line, keeping max_pause of each
            fx = (f"silenceremove=stop_periods=-1:stop_duration={a.max_pause}:stop_threshold=-40dB:"
                  f"stop_silence={a.max_pause}:detection=rms,") + fx
        # trim leading/trailing silence, (speed up), colour NXT, match loudness, 48 kHz mono
        ffmpeg("-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,"
               "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse,"
               f"{fx}loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1", dst)
        d = duration(dst)
        tracks[who].append((t, dst))
        timeline.append({"line": i, "speaker": who, "text": text, "take": int(k), "start": round(t, 3), "end": round(t + d, 3)})
        t += d + gap
    total = t + .2
    n = int(total * SR)
    mix = np.zeros(n)
    os.makedirs(os.path.join(PROJ, "assets", "audio"), exist_ok=True)
    for who, items in tracks.items():
        buf = np.zeros(n)
        for st, p in items:
            x, _ = sf.read(p)
            i0 = int(st * SR)
            buf[i0:i0 + len(x)] += x[: n - i0]
        sf.write(os.path.join(PROJ, "assets", "audio", f"voice_{who}.wav"), buf, SR)
        mix += buf
    sf.write(os.path.join(PROJ, "assets", "audio", "voice.wav"), mix, SR)
    json.dump({"duration": round(total, 3), "lines": timeline}, open(os.path.join(HERE, "lines.json"), "w"), indent=1)
    print(f"voice.wav {total:.2f} s, {len(timeline)} lines -> voice/lines.json")
    if timeline[-1]["end"] > 33.5:
        print("over budget: the reel must stay under 35 s with the 1.5 s end card; pick faster takes or trim gaps")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("design")
    d.add_argument("--engine", choices=["kokoro", "dia"], default="kokoro")
    d.add_argument("--voices", nargs="+", default=KOKORO_VOICES)
    d.add_argument("--seeds", type=int, nargs="+", default=[3, 7, 11, 19, 23, 31, 42, 58])
    d.add_argument("--device")
    ln = sub.add_parser("lines")
    ln.add_argument("--engine", choices=["chatterbox", "chatterbox-turbo", "dia"], default="chatterbox")
    ln.add_argument("--takes", type=int, default=3)
    ln.add_argument("--only", type=int, nargs="*", help="regenerate just these line numbers")
    ln.add_argument("--device", help="cuda or cpu (default: cuda if available)")
    for who in ("nxt", "human"):
        ln.add_argument(f"--{who}", help="voice picked from voice/design, e.g. am_puck")
        ln.add_argument(f"--{who}-ref", help="or any reference clip to clone (only with the speaker's consent)")
        ln.add_argument(f"--{who}-ref-text", help="its transcript (Dia only)")
    asm = sub.add_parser("assemble")
    asm.add_argument("--pick", nargs="*", default=[])
    asm.add_argument("--no-robot", action="store_true")
    asm.add_argument("--tempo", type=float, default=1.0, help="speed every line up (pitch kept), e.g. 1.06 to fit the time budget")
    asm.add_argument("--max-pause", type=float, help="cap pauses inside a line at this many seconds, e.g. 0.4")
    a = ap.parse_args()
    {"design": design, "lines": lines, "assemble": assemble}[a.cmd](a)


if __name__ == "__main__":
    main()
