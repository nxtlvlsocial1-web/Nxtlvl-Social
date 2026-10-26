"""Expressive open-source voiceovers for the openGym x Claude reel. Run on a machine with a CUDA GPU.

Engines (both open source, commercial use allowed):
  dia         Nari Labs Dia-1.6B (Apache-2.0): dialogue TTS with real non-verbals, e.g. (sighs) (gasps) (laughs).
              Default engine. Voices come from the seed; a chosen voice is kept with an audio prompt.
  chatterbox  Resemble AI Chatterbox (MIT): zero-shot cloning from a reference clip, plus an `exaggeration`
              knob for emotion intensity. Fallback, or for cloning a reference you supply.

Steps (from the repo root):
  pip install git+https://github.com/nari-labs/dia.git          # for dia
  pip install chatterbox-tts                                     # for chatterbox
  python opengym-claude-9x16/voice/make_voices.py design --seeds 3 7 11 19 23 31 42 58
      -> voice/design/{nxt,human}_seed<N>.wav: one sample per seed per character. Listen, pick one per character.
  python opengym-claude-9x16/voice/make_voices.py lines --nxt-seed 23 --human-seed 42 [--takes 3]
      -> voice/lines/<nn>_<speaker>_t<k>.wav: every line, `takes` versions each, cloned from the picked voices.
         --human-ref my_voice.wav (with --human-ref-text "...") clones a supplied clip instead (only with consent).
  python opengym-claude-9x16/voice/make_voices.py assemble [--pick 03=2 07=1]
      -> assets/audio/voice_nxt.wav, voice_human.wav, voice.wav (both, timed) and voice/lines.json (start/end per line).
         By default take 1 of each line; --pick chooses another take for a line.

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

# (speaker, Dia text with non-verbals, chatterbox exaggeration, chatterbox cfg_weight, gap after in seconds)
# Lower cfg_weight = faster, looser pacing; higher exaggeration = more emotion.
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

# Short reference lines used to design each voice (5-10 s of speech in character).
DESIGN = {
    "nxt": "Relax, I've got this. Your whole week, planned in seconds. Trust me, legs day is coming for you.",
    "human": "Bro, I'm so tired of these apps. Every week it's upgrade this, premium that. I just want to lift, man.",
}
ROBOT_FX = "highpass=f=90,chorus=0.7:0.9:22|34:0.22|0.18:0.30|0.24:1.6|2.1,aecho=0.85:0.5:8:0.12"


def seed_all(s):
    import numpy as np
    import torch
    random.seed(s)
    np.random.seed(s)
    torch.manual_seed(s)
    torch.cuda.manual_seed_all(s)


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def dia_model():
    from dia.model import Dia
    return Dia.from_pretrained("nari-labs/Dia-1.6B-0626", compute_dtype="float16")


DIA_ARGS = dict(use_torch_compile=False, verbose=False, cfg_scale=3.0, temperature=1.8, top_p=0.90, cfg_filter_top_k=50)


def design(a):
    os.makedirs(os.path.join(HERE, "design"), exist_ok=True)
    m = dia_model()
    for who, text in DESIGN.items():
        for s in a.seeds:
            seed_all(s)
            out = m.generate(f"[S1] {text}", **DIA_ARGS)
            p = os.path.join(HERE, "design", f"{who}_seed{s}.wav")
            m.save_audio(p, out)
            print("wrote", p)


def ref_for(a, who):
    """The clip and its transcript that every line of this character is cloned from."""
    ext = getattr(a, f"{who}_ref")
    if ext:
        return ext, getattr(a, f"{who}_ref_text")
    s = getattr(a, f"{who}_seed")
    if s is None:
        raise SystemExit(f"pick a voice: --{who}-seed N (from design/) or --{who}-ref clip.wav")
    return os.path.join(HERE, "design", f"{who}_seed{s}.wav"), DESIGN[who]


def chatterbox_text(t):
    """Chatterbox reads non-verbals aloud, so turn them into speakable sounds."""
    t = t.replace("(laughs)", "Haha,").replace("(sighs)", "Hhh...").replace("(gasps)", "Oh!")
    return re.sub(r"\([^)]*\)", "", t).strip()


def lines(a):
    out_dir = os.path.join(HERE, "lines")
    os.makedirs(out_dir, exist_ok=True)
    refs = {w: ref_for(a, w) for w in ("nxt", "human")}
    if a.engine == "dia":
        m = dia_model()
    else:
        import torchaudio
        from chatterbox.tts import ChatterboxTTS
        m = ChatterboxTTS.from_pretrained(device="cuda")
    for i, (who, text, ex, cfg, _) in enumerate(LINES, 1):
        ref_wav, ref_text = refs[who]
        for k in range(1, a.takes + 1):
            seed_all(1000 * i + k)
            p = os.path.join(out_dir, f"{i:02d}_{who}_t{k}.wav")
            if a.engine == "dia":
                # clone: the prompt transcript, then the new line, both as the same speaker [S1]
                out = m.generate(f"[S1] {ref_text} [S1] {text}", audio_prompt=ref_wav, **DIA_ARGS)
                m.save_audio(p, out)
            else:
                wav = m.generate(chatterbox_text(text), audio_prompt_path=ref_wav, exaggeration=ex, cfg_weight=cfg)
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
        fx = ("" if who != "nxt" or a.no_robot else ROBOT_FX + ",")
        # trim leading/trailing silence, colour NXT, match loudness, 48 kHz mono
        ffmpeg("-i", src, "-af", f"silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,"
               f"areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse,"
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
    if total > 33.5:
        print("over budget: the reel must stay under 35 s with the 1.5 s end card; pick faster takes or trim gaps")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("design")
    d.add_argument("--seeds", type=int, nargs="+", default=[3, 7, 11, 19, 23, 31, 42, 58])
    ln = sub.add_parser("lines")
    ln.add_argument("--engine", choices=["dia", "chatterbox"], default="dia")
    ln.add_argument("--takes", type=int, default=3)
    for who in ("nxt", "human"):
        ln.add_argument(f"--{who}-seed", type=int)
        ln.add_argument(f"--{who}-ref")
        ln.add_argument(f"--{who}-ref-text")
    asm = sub.add_parser("assemble")
    asm.add_argument("--pick", nargs="*", default=[])
    asm.add_argument("--no-robot", action="store_true")
    a = ap.parse_args()
    {"design": design, "lines": lines, "assemble": assemble}[a.cmd](a)


if __name__ == "__main__":
    main()
