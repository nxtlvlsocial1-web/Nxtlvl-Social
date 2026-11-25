"""v2 voice: the client's ElevenLabs read (Vikram, assets/audio/vo_vikram/vikram_raw.mp3, 69.4 s) with 0.6 s of
silence added in the pause before "उड़ान" (cut at 34.70 s) so the walls can hold before they shatter.
Times after 34.70 s move by +0.6 s. Writes assets/audio/voice_v2.wav.   python3 build/voice_v2.py"""
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets/audio/vo_vikram/vikram_raw.mp3")
OUT = os.path.join(ROOT, "assets/audio/voice_v2.wav")
CUT, GAP, TOTAL = 34.70, 0.60, 74.0
fc = (f"[0:a]aresample=48000,aformat=channel_layouts=mono,asplit=2[a][b];"
      f"[a]atrim=0:{CUT},asetpts=PTS-STARTPTS[p1];[b]atrim={CUT},asetpts=PTS-STARTPTS,adelay={int(GAP*1000)}[p2];"
      f"[p1][p2]concat=n=2:v=0:a=1,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[o]", OUT], check=True)
print(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", OUT]).decode().strip())
