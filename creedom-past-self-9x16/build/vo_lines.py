"""Voices for the Creedom "Messages to My Past Self" reel (script approved 2026-11-19, two voices): every chat message is
its own ElevenLabs Eleven v3 clip. Present-her = Jessica (warm, steady), past-her = Sarah (quiet, tired); both are
ElevenLabs built-in voices (the owner's free plan can't use library voices through the API). Two takes per line ->
assets/audio/el_lines/<id>_<take>.mp3; plan/lines.json lists the messages.   python3 build/vo_lines.py"""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES = {"P": "cgSgspJ2msm6clMCkdW9", "Q": "EXAVITQu4vr4xnSDxMaL"}      # P present (Jessica), Q past (Sarah)
LINES = [
    ("m0", "P", "If you're reading this... you're about to quit.", "[softly, knowing] If you're reading this... [gently] you're about to quit."),
    ("m1", "Q", "how do you know", "[tired, quiet] how do you know?"),
    ("m2", "P", "Because I'm you. Six months from now.", "[warm, a little smile] Because I'm you. [softly] Six months from now."),
    ("m3", "Q", "47 views. again. I don't even know what I'm doing wrong", "[exhausted, flat] Forty-seven views. Again. [voice breaking a little] I don't even know what I'm doing wrong."),
    ("m4", "Q", "I think I'm done.", "[barely a whisper] I think I'm done."),
    ("m5", "P", "Don't delete it. Stop guessing.", "[urgent but gentle] Don't delete it. [firm, warm] Stop guessing."),
    ("m6", "P", "Creedom read our whole account. It showed what's working, and what was killing our views.",
     "[reassuring] Cree-dum read our whole account. [clear] It showed what's working... and what was killing our views."),
    ("m7", "Q", "wait... it tells you WHY?", "[surprised, hopeful] Wait... it tells you why?"),
    ("m8", "P", "And it checks every reel before you post.", "[smiling] And it checks every reel before you post."),
    ("m9", "Q", "ok. I'm not deleting it.", "[small laugh, relieved] Okay. [steady] I'm not deleting it."),
    ("m10", "P", "Comment GROW. I'll send you the secret.", "[warm, playful] Comment GROW. [softly] I'll send you the secret."),
]
out = os.path.join(ROOT, "assets", "audio", "el_lines")
os.makedirs(out, exist_ok=True)
json.dump([{"id": i, "who": w, "text": t} for i, w, t, _ in LINES], open(os.path.join(ROOT, "plan", "lines.json"), "w"), indent=1)
for lid, who, _, tts in LINES:
    for k in (1, 2):
        p = os.path.join(out, f"{lid}_{k}.mp3")
        if os.path.exists(p) and os.path.getsize(p) > 2000:
            continue
        body = json.dumps({"text": tts, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}})
        r = subprocess.run(["curl", "-sS", "-m", "120", "-o", p, "-w", "%{http_code}", "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json",
                            "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[who]}?output_format=mp3_44100_128", "-d", body], capture_output=True, text=True)
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
        print(lid, who, k, r.stdout, d)
