"""The audio bed: the tight voiceover over the original music, the music ducked under the voice (sidechain).
Sound effects go on top later (build/sfx_sheet.py + the real-sfx mixer). Writes assets/audio/bed.wav.
python3 build/bed.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets", "audio")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(A, "music.wav"), "-i", os.path.join(A, "vo.wav"), "-filter_complex",
                "[1]aformat=channel_layouts=stereo,apad=whole_dur=37.5,asplit=2[v1][v2];"
                "[0]volume=-9dB,atrim=0:37.5[m];[m][v1]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=350:makeup=1[md];"
                "[v2][md]amix=inputs=2:normalize=0:weights=1 1,atrim=0:37.5[o]",
                "-map", "[o]", "-ar", "48000", "-c:a", "pcm_s16le", os.path.join(A, "bed.wav")], check=True)
print("bed.wav")
