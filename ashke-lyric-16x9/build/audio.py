"""The soundtrack: 2:14 to 3:14 of the song (assets/audio/song-full.wav), mastered to -14 LUFS.

python3 build/audio.py      (from the project root; needs ffmpeg). Writes assets/audio/section.wav.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, DUR = 134.0, 60.0

subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(START), "-t", str(DUR), "-i", os.path.join(ROOT, "assets", "audio", "song-full.wav"),
                "-af", "afade=t=in:d=0.04,afade=t=out:st=59.2:d=0.8,loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
                os.path.join(ROOT, "assets", "audio", "section.wav")], check=True)
print("wrote assets/audio/section.wav")
