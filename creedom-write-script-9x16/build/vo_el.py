"""v4 voice: the owner's ElevenLabs take (Eleven v3 voice "Blondie - Conversational", plan/elevenlabs_vo.md), used as is.
Word times come from faster-whisper small.en (local) on the take; the take matched the script word for word, so the
words are split into lines by the script's word counts and keep the script's spelling. The voice is polished like the
others (high-pass, light compression, -16 LUFS) into assets/audio/vo.wav; plan/words.json gets the word times.
/root/tts/.venv/bin/python build/vo_el.py      (HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1)
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
RAW = os.path.join(ROOT, "assets", "audio", "el", "el_raw.mp3")
LEAD = .06

src = open(os.path.join(ROOT, "build", "vo2.py")).read()
LINES = re.findall(r'\("(m0\d)", "((?:[^"\\]|\\.)*)", "[^"]*", [\d.]+\)', src)
LINES = [(i, t.replace('\\"', '"')) for i, t in LINES]


def main():
    from faster_whisper import WhisperModel
    wm = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
    segs, _ = wm.transcribe(RAW, word_timestamps=True, language="en", beam_size=5, vad_filter=False)
    ws = [w for s in segs for w in s.words]
    words, k = [], 0
    for lid, text in LINES:
        sw = text.split()
        chunk = ws[k:k + len(sw)]
        k += len(sw)
        for w, txt in zip(chunk, sw):
            words.append({"line": lid, "w": txt, "t0": round(w.start + LEAD, 3), "t1": round(w.end + LEAD, 3)})
    if k != len(ws):
        print(f"warning: {len(ws)} words heard, {k} in the script")
    json.dump(words, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
    json.dump([{"id": i, "text": t} for i, t in LINES], open(os.path.join(ROOT, "plan", "script.json"), "w"), indent=1)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", RAW, "-af",
                    f"adelay={int(LEAD * 1000)}:all=1,apad=pad_dur=0.4,highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80:makeup=1.5,"
                    "loudnorm=I=-16:TP=-2:LRA=9", "-ar", "48000", "-ac", "1", os.path.join(ROOT, "assets", "audio", "vo.wav")], check=True)
    print(f"{len(words)} words, last ends {words[-1]['t1']} s")


if __name__ == "__main__":
    main()
