"""Voice for the Creedom "Empty Theater" reel: ElevenLabs Eleven v3, built-in voice Jessica (the owner's free plan can't use
Voice Library voices through the API), mood tags. Script approved by the owner on 2026-11-19 (Empty Theater).
Writes assets/audio/el_takes/take_<n>.mp3.   python3 build/vo_el.py [n_takes]"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.environ.get("EL_VOICE", "cgSgspJ2msm6clMCkdW9")      # Jessica (ElevenLabs built-in)
SCRIPT = """[warm, storytelling, softly] She gave every reel everything she had.

[quiet, a little sad] And every night... the same empty room.

[hushed] The few who came... left in the first three seconds.

[gentle, honest] She didn't need more effort. [softly] She needed to know why.

[hopeful, building] Then Cree-dum read her whole account... [clear] and showed her exactly where they left.

[steady, warm] It checked her next reel before she posted.

[emotional, rising] And this time... [moved, smiling] they stayed.

[warm, playful] Comment GROW, [softly] and I'll send you the secret."""
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
