"""Klap reel v2: the voiceover on ElevenLabs v3 (owner: "better voiceover with the flow, emotions"). The API key is a
network secret on this session's environment (the proxy injects it into requests to api.elevenlabs.io; the header
below is a placeholder). Voice: "Liam" (ElevenLabs' premade "Energetic, Social Media Creator"). The script is the brand's
own, with v3 audio tags for the delivery. Two takes (stability Natural .5 and Creative 0) with character timestamps (mp3_44100_128: PCM needs the Pro tier);
build/vo_pick_eleven.py transcribes both, picks one and writes assets/audio/vo.wav + plan/words.json.
python3 build/vo_eleven.py
"""
import base64
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "audio", "el")
VOICE = "TX3LPaxmHKxFdv7VOQHJ"   # Liam
SCRIPT = ("[excited] GTA 6 is out... and GTA clips are taking over every feed. And clippers? Are getting PAID for views. "
          "MrBeast and IShowSpeed campaigns pay around a dollar for every thousand views. "
          "[serious] But the hard part... is finding the moment. A three-hour stream. One crazy chase. "
          "[confident] This tool finds it for you. It's called Klap. "
          "You paste the stream link. It picks the best moments, and scores each one for how viral it could go. "
          "It cuts them vertical, keeps the gameplay AND the streamer in frame, and adds captions that pop. "
          "[playful] So while other clippers are still scrubbing hour two... your clip is already up. "
          "[warm] Comment Klap, and I'll send you the link. Or hit the link in my bio.")
TAKES = [("natural", .5), ("creative", .0)]


def words_from_alignment(al):
    """character timestamps -> words (the tags are not spoken; drop anything inside [...])"""
    chars, t0, t1 = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, depth = [], None, 0
    for c, a, b in zip(chars, t0, t1):
        if c == "[":
            depth += 1; continue
        if c == "]":
            depth = max(0, depth - 1); continue
        if depth:
            continue
        if c.isspace():
            if cur:
                words.append(cur); cur = None
            continue
        if cur is None:
            cur = {"w": c, "t0": round(a, 3), "t1": round(b, 3)}
        else:
            cur["w"] += c; cur["t1"] = round(b, 3)
    if cur:
        words.append(cur)
    return words


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, stab in TAKES:
        body = {"text": SCRIPT, "model_id": "eleven_v3",
                "voice_settings": {"stability": stab, "similarity_boost": .85, "use_speaker_boost": True, "speed": 1.0}}
        bp, rp = os.path.join(OUT, f"{name}_req.json"), os.path.join(OUT, f"{name}_res.json")
        json.dump(body, open(bp, "w"))
        r = subprocess.run(["curl", "-s", "--max-time", "180", "-o", rp, "-w", "%{http_code}",
                            "-H", "xi-api-key: placeholder", "-H", "Content-Type: application/json", "--data-binary", f"@{bp}",
                            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128"],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        if code != "200":
            print(name, "HTTP", code, open(rp, errors="ignore").read()[:400]); continue
        res = json.load(open(rp))
        mp3 = os.path.join(OUT, f"{name}.mp3")
        open(mp3, "wb").write(base64.b64decode(res["audio_base64"]))
        wav = os.path.join(OUT, f"{name}.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ar", "48000", "-ac", "1", wav], check=True)
        al = res.get("normalized_alignment") or res.get("alignment")
        words = words_from_alignment(al) if al else []
        json.dump(words, open(os.path.join(OUT, f"{name}_words.json"), "w"), indent=0)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout)
        print(name, f"{dur:.2f}s", len(words), "words", "alignment:", "yes" if al else "no")
    print("done")


if __name__ == "__main__":
    main()
