"""v11: the soundtrack with the logo outro. Owner: no sound effects on the logo, blend the music fade into it. So the
song keeps playing past the section's end (2:14 to 3:15.72 of the full song, ../ashke-lyric-16x9/assets/audio/
song-full.wav, not in git) at the section's own level (build/audio.py's loudnorm measured as a static -7.62 dB on this
section, correlation 0.9997), and fades out once across the logo, 59.2-61.6 s, as the picture eases into the dark and
the logo comes in. Writes assets/audio/section_outro.wav (TOTAL s).

python3 build/audio_outro.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets", "audio")
SRC = os.path.join(os.path.dirname(ROOT), "ashke-lyric-16x9", "assets", "audio", "song-full.wav")
START, TOTAL, GAIN_DB = 134.0, 61.72, -7.62
FADE_AT, FADE = 59.2, 2.4

subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(START), "-t", str(TOTAL), "-i", SRC, "-af",
                f"volume={GAIN_DB}dB,afade=t=in:d=0.04,afade=t=out:st={FADE_AT}:d={FADE}:curve=qsin,apad=whole_dur={TOTAL},atrim=0:{TOTAL}",
                "-ar", "48000", os.path.join(A, "section_outro.wav")], check=True)
print("wrote assets/audio/section_outro.wav")
