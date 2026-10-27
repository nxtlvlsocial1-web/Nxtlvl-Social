"""Write audio_meta.json: the original music as host BGM plus every SFX cue placed on the beat grid.

Each cue names the moment it should HIT (absolute seconds). The script subtracts the file's measured peak
time so the transient lands one frame after its picture, then tools/assemble_audio.py writes the <audio>
tags into index.html.  Run: python3 tools/sound_cues.py && python3 tools/assemble_audio.py
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LATE = 1 / 30          # light before sound: every hit lands one frame after its picture

# measured peak (s into the file) and length of each bundled sound
SFX = {
    'impact-bass-1': (0.08, 2.12), 'impact-bass-2': (2.04, 2.59), 'whoosh-cinematic': (2.55, 5.54),
    'whoosh-short': (0.17, 0.57), 'pop': (0.13, 0.72), 'sparkle': (0.09, 1.80), 'chime': (0.43, 2.50),
    'notification': (0.24, 2.46), 'click-soft': (0.06, 0.37), 'riser': (0.0, 2.0),
}
WHOOSH = ['whoosh-short', 'whoosh-cinematic']   # rotated so no two cuts share a take

CUES = [  # (hit time s, sound, volume)
    # 1 · hook: the slot rolls on beats 2, 4, 6
    (1.0, 'whoosh-short', 0.14), (2.0, 'whoosh-short', 0.14), (3.0, 'whoosh-short', 0.14),
    (2.5, 'sparkle', 0.16),                                       # the meteor
    # 2 · design (4-10): the drop, chips, typing, approve
    (4.0, 'impact-bass-1', 0.42),
    (5.0, 'pop', 0.22), (5.25, 'pop', 0.2), (5.5, 'pop', 0.2), (5.75, 'pop', 0.18),   # swatches + font chip
    *[(6.0 + 0.08 * i, 'click-soft', 0.12) for i in range(13)],                       # the headline types
    (7.5, 'pop', 0.22),                                           # "Today only"
    (8.5, 'click-soft', 0.34),                                    # Approve pressed
    (8.62, 'sparkle', 0.26),                                      # Designer-finished badge
    (9.75, 'whoosh-short', 0.2),                                  # whip out
    # 3 · reels (10-16): captions on the stabs, reactions
    (10.05, 'whoosh-cinematic', 0.18),
    (11.0, 'pop', 0.18), (11.5, 'pop', 0.18), (12.0, 'pop', 0.18), (12.5, 'pop', 0.18),
    (13.6, 'pop', 0.16),                                          # the cover tucks in
    (14.0, 'notification', 0.2), (14.4, 'notification', 0.16), (14.8, 'pop', 0.16),
    (15.75, 'whoosh-short', 0.2),
    # 4 · website (16-22): window in, headline builds, click, badges
    (16.05, 'whoosh-cinematic', 0.2),
    *[(17.0 + 0.1 * i, 'click-soft', 0.1) for i in range(8)],                          # headline words
    (19.0, 'click-soft', 0.34),                                   # Book a free call pressed
    (19.3, 'pop', 0.2), (19.65, 'pop', 0.2), (20.0, 'pop', 0.2),  # badges
    # 5 · automation (22-27): the impact, rail steps, toasts, counter
    (22.0, 'impact-bass-2', 0.5),
    (23.0, 'pop', 0.18), (23.5, 'pop', 0.18), (24.0, 'pop', 0.18), (24.5, 'pop', 0.18),   # rail steps
    (23.3, 'notification', 0.2), (24.0, 'notification', 0.2), (24.7, 'notification', 0.2),
    *[(25.0 + 0.12 * i, 'click-soft', 0.1) for i in range(6)],                         # the counter
    (26.55, 'whoosh-cinematic', 0.26),                            # the streak begins
    # 6 · end card (27-32): strike, lockup, press
    (27.5, 'impact-bass-1', 0.46), (27.52, 'sparkle', 0.3),
    (28.65, 'whoosh-short', 0.14),                                # the wordmark wipes in
    (30.0, 'click-soft', 0.34),                                   # Book a free call pressed
]

sfx = []
for hit, name, vol in CUES:
    peak, length = SFX[name]
    start = max(0.0, hit + LATE - peak)
    sfx.append({"start_s": round(start, 3), "file": f"assets/sfx/{name}.mp3", "duration_s": length, "volume": vol,
                "source": "host", "license": "Pixabay Content License"})

meta = {"bgm": {"path": "assets/music/nxtlvl-brand.wav", "volume": 1.0, "duration_s": 32.0, "source": "host"},
        "voices": [], "sfx": sfx}
json.dump(meta, open(os.path.join(ROOT, 'audio_meta.json'), 'w'), indent=1)
print(f'{len(sfx)} sfx cues + host bgm -> audio_meta.json')
