"""More expressive takes for the creator (v4). Chatterbox (MIT) copies some of the prosody of its voice prompt, so first an
emotional prompt is made from the creator's Kokoro reference at high exaggeration, then every line is performed from that
prompt four times across an exaggeration ladder, with punctuation written for drama. build/pick2.py keeps the most
expressive take that is still word-perfect. ~/.venvs/tts/bin/python build/voices2.py"""
import json, os, torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
EMO = "voice/refs/creator_emo.wav"
if not os.path.exists(EMO):
    torch.manual_seed(5)
    w = m.generate("No, no, no... this can't be happening! I worked SO hard on this... and NOBODY watched it!", audio_prompt_path="voice/refs/creator.wav", exaggeration=1.4, cfg_weight=.3)
    ta.save(EMO, w, m.sr)
LINES = [  # take, text, exaggeration ladder, cfg
    ("01", "My latest reel... got... forty-two views.", (1.0, 1.25, 1.5, 1.75), .3),
    ("02", "I used trending audio! I posted at seven A M! I even changed my HAIR!", (1.1, 1.4, 1.7, 2.0), .35),
    ("03", "And still... nothing...", (1.0, 1.3, 1.6, 1.9), .25),
    ("04", "I wish... someone could review my reel... before I post it.", (.8, 1.0, 1.2, 1.4), .3),
    ("05", "I wish it could look at my old reels... and tell me what actually worked.", (.8, 1.0, 1.2, 1.4), .3),
    ("06", "And I wish... it could just set up my D M automation... for me.", (.9, 1.1, 1.35, 1.6), .3),
    ("07", "Whoa!!", (1.2, 1.6, 2.0, 2.4), .4),
    ("08", "That's... actually it!", (1.0, 1.3, 1.6, 1.9), .3),
    ("09", "Wait... I forgot I even made that!", (1.0, 1.3, 1.6, 1.9), .35),
    ("10", "Where have you BEEN all my life?!", (1.0, 1.3, 1.6, 1.9), .3),
    ("11", "Comment Kree dum, and I'll send you the link!", (.8, 1.0, 1.2, 1.4), .45),
]
log = {}
for take, text, ladder, cfg in LINES:
    for k, ex in enumerate(ladder):
        out = f"voice/takes2/{take}_{k}.wav"
        if os.path.exists(out):
            continue
        torch.manual_seed(11 + k * 13)
        wav = m.generate(text, audio_prompt_path=EMO, exaggeration=ex, cfg_weight=cfg)
        ta.save(out, wav, m.sr)
        log[f"{take}_{k}"] = {"text": text, "exaggeration": ex, "cfg_weight": cfg, "seconds": round(wav.shape[-1] / m.sr, 2)}
        print(take, k, ex, log[f"{take}_{k}"]["seconds"], flush=True)
        json.dump(log, open("voice/takes2/takes.json", "w"), indent=1)
