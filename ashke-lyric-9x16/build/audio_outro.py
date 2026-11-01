"""v10c: the soundtrack with room for the logo outro. The song fades out once, smoothly, over 59.0-60.0 s (a
quarter-sine curve on top of the section's own fade, build/audio.py), in step with the picture's dip into the logo;
then silence under the logo except its own swell and bell (build/sfx_sheet.py). No echo tail (owner: it repeated
the lyric). Writes assets/audio/section_outro.wav (TOTAL s).

python3 build/audio_outro.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets", "audio")
TOTAL, FADE_AT, FADE = 61.72, 59.0, 1.0

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(A, "section.wav"), "-af",
                f"afade=t=out:st={FADE_AT}:d={FADE}:curve=qsin,apad=whole_dur={TOTAL},atrim=0:{TOTAL}", "-ar", "48000",
                os.path.join(A, "section_outro.wav")], check=True)
print("wrote assets/audio/section_outro.wav")
