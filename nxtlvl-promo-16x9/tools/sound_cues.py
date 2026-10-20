"""Write audio_meta.json: the original music as host BGM plus every SFX cue placed on the beat grid.

Each cue names the moment it should HIT (absolute seconds). The script subtracts the file's measured peak
time so the transient lands exactly on that moment, then converts to the assembler's frame + offset form.
Run: python3 tools/sound_cues.py
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# measured peak (s into the file) and length of each bundled sound
SFX = {
    'impact-bass-1': (0.08, 2.12), 'impact-bass-2': (2.04, 2.59), 'whoosh-cinematic': (2.55, 5.54),
    'whoosh-short': (0.17, 0.57), 'pop': (0.13, 0.72), 'sparkle': (0.09, 1.80), 'chime': (0.43, 2.50),
    'notification': (0.24, 2.46), 'click-soft': (0.06, 0.37),
}
FRAMES = [(1, 0.0), (2, 4.0), (3, 10.0), (4, 18.0), (5, 24.0), (6, 27.0)]   # (frame number, start s)

CUES = [  # (hit time s, sound, volume)
    (0.5, 'notification', 0.26),                                               # "0 posts?"
    (4.0, 'impact-bass-1', 0.42),                                              # the drop
    *[(4.0 + 0.5 * i, 'pop', 0.2) for i in range(9)],                          # nine posts land on the beats
    (5.0, 'whoosh-short', 0.16),                                               # "creative team."
    *[(8.0 + 0.25 * i, 'click-soft', 0.18) for i in range(4)],                 # the four pills
    (9.0, 'sparkle', 0.22),                                                    # "by nxtlvl"
    *[(t, 'whoosh-short', 0.15) for t in (11.0, 12.0, 13.0, 14.0, 15.0, 15.5, 16.0)],   # word swaps
    *[(t, 'notification', 0.2) for t in (12.0, 14.0, 16.0)],                   # "Posted" toasts
    *[(t, 'pop', 0.15) for t in (14.0, 14.5, 15.0, 16.0, 16.5, 17.0)],          # posts 10-15
    (18.35, 'whoosh-cinematic', 0.34),                                         # the pull-back
    *[(18.5 + 0.5 * i, 'pop', 0.12) for i in range(7)],                        # the wave across the wall
    (20.0, 'whoosh-short', 0.15), (21.0, 'whoosh-short', 0.15),                # the headline
    (24.0, 'impact-bass-2', 0.5),                                              # the price hit
    (24.1, 'sparkle', 0.24),
    *[(25.0 + 0.25 * i, 'click-soft', 0.16) for i in range(3)],                # terms pills
    (27.0, 'chime', 0.4),                                                      # the spark ignites
    (27.5, 'click-soft', 0.3),                                                 # the button press
]


def frame_of(t):
    for n, start in reversed(FRAMES):
        if t >= start - 1e-9:
            return n, start
    return FRAMES[0]


sfx = []
for hit, name, vol in CUES:
    peak, length = SFX[name]
    start = max(0.0, hit - peak)
    n, fstart = frame_of(start)
    sfx.append({"frame": n, "file": f"assets/sfx/{name}.mp3", "offset_s": round(start - fstart, 3),
                "duration_s": length, "volume": vol, "source": "host", "license": "Pixabay Content License"})

meta = {"bgm": {"path": "assets/music/nxtlvl-theme.wav", "volume": 1.0, "source": "host"},
        "voices": [], "sfx": sfx}
json.dump(meta, open(os.path.join(ROOT, 'audio_meta.json'), 'w'), indent=1)
print(f'{len(sfx)} sfx cues + host bgm -> audio_meta.json')
