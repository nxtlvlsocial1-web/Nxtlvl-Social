"""Voiceover timing for the Creedom reel (Nota 3 take, 32.13 s), shared by generate.py and audio.py.

Phrase intervals are the speech runs between pauses (ffmpeg silencedetect, -38 dB) and their words come from a local
whisper transcription. Words inside a phrase are spread by length, which is close enough for one-word captions.
"""

DUR = 33.6
VO_LEN = 32.13

PHRASES = [
    (0.00, 3.28, "One reel did 85x my usual views"),
    (3.77, 5.30, "and I had no idea why."),
    (5.84, 6.45, "The next one?"),
    (6.91, 7.68, "A few thousand."),
    (8.24, 8.88, "Numbers..."),
    (9.36, 10.21, "never reasons."),
    (10.78, 12.42, "So I gave my page to Creedom."),
    (12.82, 13.72, "Twenty seconds."),
    (14.21, 15.02, "Content score:"),
    (15.37, 16.83, "82 out of 100."),
    (17.30, 19.58, "Then its reel analyser watched my reel..."),
    (19.93, 21.06, "second by second."),
    (21.49, 22.85, "And found what I'd missed..."),
    (23.33, 25.98, "my best hook was buried at 0:34."),
    (26.50, 27.97, "Now I edit with reasons."),
    (28.30, 29.13, "Not guesses."),
    (29.62, 30.56, "Comment CREEDOM..."),
    (30.89, 31.96, "and I'll DM you the link."),
]

# words that get the pink pill when they are spoken
KEY = {"85x", "why.", "thousand.", "reasons.", "Creedom.", "Twenty", "score:", "82", "analyser", "second.",
       "missed...", "0:34.", "guesses.", "CREEDOM...", "link."}

# scene windows (seconds); each cut sits in a pause of the voice
SCENES = [
    ("hook", 0.0, 3.5), ("why", 3.5, 5.6), ("next", 5.6, 8.05), ("nums", 8.05, 10.5), ("read", 10.5, 14.0),
    ("score", 14.0, 17.1), ("analyse", 17.1, 21.3), ("twist", 21.3, 26.3), ("reasons", 26.3, 29.4),
    ("cta", 29.4, DUR),
]


def words():
    """[(start, end, word)] for the captions."""
    out = []
    for a, z, text in PHRASES:
        ws = text.split()
        weights = [len(w.strip(".,:?")) + 2 for w in ws]
        t, tot = a, sum(weights)
        for w, k in zip(ws, weights):
            d = (z - a) * k / tot
            out.append((round(t, 3), round(t + d, 3), w))
            t += d
    return out


S_TWIST = next((a, z) for k, a, z in SCENES if k == "twist")
