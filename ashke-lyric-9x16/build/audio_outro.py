"""v10b: the soundtrack with room for the logo outro. The 60 s section (build/audio.py) already fades out over
59.2-60 s; under the logo (60 s on) a soft echo of the song's last moment (58.9-59.7 s, low-passed, four repeats)
decays to silence, so the sound trails off with the picture instead of stopping dead. Writes
assets/audio/section_outro.wav (TOTAL s).

python3 build/audio_outro.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets", "audio")
TOTAL = 61.72

fc = ("[0:a]apad=whole_dur={T}[song];"
      "[0:a]atrim=58.9:59.7,asetpts=PTS-STARTPTS,lowpass=f=2200,aecho=0.8:0.9:420|840|1260|1680:0.6|0.45|0.32|0.2,"
      "apad=whole_dur=3.2,afade=t=out:st=1.0:d=2.2,volume=0.7[tail0];"
      "[tail0]adelay=59300|59300,apad=whole_dur={T}[tail];"
      "[song][tail]amix=inputs=2:normalize=0,atrim=0:{T},afade=t=out:st={F}:d=0.3[o]").format(T=TOTAL, F=TOTAL - .3)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(A, "section.wav"), "-filter_complex", fc, "-map", "[o]",
                "-ar", "48000", os.path.join(A, "section_outro.wav")], check=True)
print("wrote assets/audio/section_outro.wav")
