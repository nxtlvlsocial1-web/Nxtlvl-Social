"""v2: builds assets/audio/mix_v2.wav (74 s): voice_v2.wav (build/voice_v2.py, Vikram) + music bed + CC0 sound effects.
Music: "Cinematic Story Intro" by tyops, CC BY 4.0, https://freesound.org/people/tyops/sounds/456270 (credit in post).
Its big hit (53.023 s in the track) lands on "उड़ान" at 35.45 s: the bed starts at 17.573 s; to stretch the
loud part under the CTA, it plays to the downbeat at 70.722 s and jumps back six bars (95 bpm, bar 2.53 s) to 55.560 s.
The music is ducked under the voice with a sidechain compressor.  python3 build/mix_audio.py"""
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda p: os.path.join(ROOT, "assets/audio", p)
TOTAL = 74.0
OFF, OUT1, IN2 = 17.573, 70.722, 55.560
# (file, start_s, gain_dB)  -- start chosen so each sound's peak lands on its picture event
SFX = [("sfx/pop.mp3", 3.25, -12), ("sfx/pop.mp3", 4.34, -12), ("sfx/pop.mp3", 5.46, -12),
       ("sfx/whoosh.mp3", 10.75, -18),
       ("sfx/thud.mp3", 22.0, -17),
       ("sfx/thud.mp3", 26.10, -6), ("sfx/thud.mp3", 27.45, -6), ("sfx/thud.mp3", 28.45, -5),
       ("sfx/pop.mp3", 30.15, -16), ("sfx/thud.mp3", 30.75, -19),
       ("sfx/riserhit.mp3", 34.85, -8), ("sfx/glimmer.mp3", 35.50, -2),
       ("sfx/whoosh.mp3", 36.20, -15), ("sfx/whoosh.mp3", 41.70, -17), ("sfx/whoosh.mp3", 46.75, -17),
       ("sfx/whoosh.mp3", 51.95, -16),
       ("sfx/whoosh.mp3", 68.30, -12), ("sfx/glimmer.mp3", 68.75, -4), ("sfx/whoosh.mp3", 69.65, -15),
       ("sfx/glimmer.mp3", 70.95, -6)]
inputs = ["-i", A("voice_v2.wav"), "-i", A("music_src.mp3"), "-i", A("music_src.mp3")]
for f, _, _ in SFX:
    inputs += ["-i", A(f)]
fc = [
    "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-16:TP=-2:LRA=9,apad=whole_dur=%s,asplit=2[vo][sc]" % TOTAL,
    f"[1:a]atrim={OFF}:{OUT1},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[m1]",
    f"[2:a]atrim={IN2},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[m2]",
    "[m1][m2]acrossfade=d=0.06:c1=tri:c2=tri,afade=t=in:d=0.25,volume=-15dB[mb]",
    "[mb][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=350:makeup=1[md]",
]
sl = []
for k, (f, t, g) in enumerate(SFX):
    fc.append(f"[{k+3}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={int(t*1000)}:all=1[x{k}]")
    sl.append(f"[x{k}]")
fc.append("".join(sl) + f"amix=inputs={len(SFX)}:normalize=0[fx]")
fc.append(f"[vo][md][fx]amix=inputs=3:normalize=0,atrim=0:{TOTAL},afade=t=out:st={TOTAL-1.2}:d=1.2,"
          "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]",
                "-ar", "48000", A("mix_v2.wav")], check=True)
print(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", A("mix_v2.wav")]).decode().strip())
