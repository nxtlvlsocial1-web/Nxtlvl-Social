"""Builds assets/audio/mix.wav (66.5 s): voice.wav (build/timeline.py) + music bed + CC0 sound effects.
Music: "Cinematic Story Intro" by tyops, CC BY 4.0, https://freesound.org/people/tyops/sounds/456270 (credit in post).
Its big hit (53.023 s in the track) lands on the UDAAN reveal at 32.0 s: the bed starts at 21.023 s; to stretch the
loud part under the CTA, it plays to the downbeat at 65.666 s and jumps back four bars (95 bpm, bar 2.53 s) to 55.560 s.
The music is ducked under the voice with a sidechain compressor.  python3 build/mix_audio.py"""
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda p: os.path.join(ROOT, "assets/audio", p)
TOTAL = 66.5
OFF, OUT1, IN2 = 21.023, 65.666, 55.560
# (file, start_s, gain_dB)  -- start chosen so each sound's peak lands on its picture event
SFX = [("sfx/pop.mp3", 3.22, -12), ("sfx/pop.mp3", 4.08, -12), ("sfx/pop.mp3", 4.98, -12),
       ("sfx/thud.mp3", 19.08, -16),
       ("sfx/thud.mp3", 23.27, -7), ("sfx/thud.mp3", 24.62, -7), ("sfx/thud.mp3", 25.62, -6),
       ("sfx/pop.mp3", 27.15, -16), ("sfx/thud.mp3", 27.80, -20),
       ("sfx/riserhit.mp3", 31.35, -9), ("sfx/glimmer.mp3", 32.05, -2),
       ("sfx/whoosh.mp3", 33.50, -15), ("sfx/whoosh.mp3", 46.80, -16),
       ("sfx/glimmer.mp3", 61.80, -4), ("sfx/whoosh.mp3", 62.50, -14), ("sfx/glimmer.mp3", 63.85, -6)]
inputs = ["-i", A("voice.wav"), "-i", A("music_src.mp3"), "-i", A("music_src.mp3")]
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
                "-ar", "48000", A("mix.wav")], check=True)
print(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", A("mix.wav")]).decode().strip())
