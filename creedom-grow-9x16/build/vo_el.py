"""v3 voice (owner: "the sped up voice looks bad" -> a shorter script read at natural speed, generated with ElevenLabs).
The owner's ElevenLabs account is on the free plan, which can't use Voice Library voices (Blondie) through the API, so
this uses the built-in voice Jessica on Eleven v3 with mood tags. Script: the ~75-word cut sent to the owner (client
approval needed: it is a paid collab). Writes assets/audio/el_takes/take_<n>.mp3.
python3 build/vo_el.py [n_takes]"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.environ.get("EL_VOICE", "cgSgspJ2msm6clMCkdW9")      # Jessica (ElevenLabs built-in)
SCRIPT = """[whispering, conspiratorial] This is the secret AI... [softly] quietly growing Instagram accounts.

[playful, teasing] And no... it's not ChatGPT.

[warm, a little proud] It's Cree-dum AI. [casual] An Instagram coach that reads your account.

[intrigued] It finds what's working... [hushed] and what's killing your views.

[urgent] It checks your reel before you post. [confident] Tells you what to post next.

[excited whisper] And the crazy part? [amazed] It shows you if the advice actually worked.

[impressed] Over a hundred and fifty thousand creators use it. [warmly] Your first account read is free.

[upbeat, energetic] Comment GROW... [playful whisper] and I'll send you the secret."""
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
out = os.path.join(ROOT, "assets", "audio", "el_takes")
os.makedirs(out, exist_ok=True)
for k in range(1, n + 1):
    body = json.dumps({"text": SCRIPT, "model_id": "eleven_v3", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}})
    p = os.path.join(out, f"take_{k}.mp3")
    r = subprocess.run(["curl", "-sS", "-m", "180", "-o", p, "-w", "%{http_code}", "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json",
                        "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", "-d", body], capture_output=True, text=True)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    print(f"take {k}: HTTP {r.stdout} {d or open(p, errors='ignore').read(200)} s {r.stderr.strip()}")
