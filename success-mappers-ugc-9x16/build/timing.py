"""Word timings for the voiceover.

The speech model could not be downloaded, so timings come from the audio itself:
spoken stretches were found with ffmpeg silencedetect (-35 dB, 0.18 s and 0.08 s),
and the known script words are spread across each stretch by spoken length.
"""
import re

# (start, end, text) for each spoken stretch, measured from voiceover.mp3
SEGMENTS = [
    (0.11, 2.12, "Tumhe pata hai tumhe kya banna hai..."),
    (2.61, 3.12, "but"),
    (3.39, 6.68, "kya tumhe pata hai tumhare liye best career options kaun-se hain?"),
    (7.25, 12.34, "Hum career ko aksar ek stream, ek degree ya ek job title tak limit kar dete hain."),
    (12.80, 13.30, "But"),
    (13.49, 16.80, "ek hi direction ke andar kitne saare possibilities hoti hain,"),
    (17.30, 18.89, "hum unke baare mein sochte bhi nahi."),
    (19.38, 23.83, "Because career choose karna sirf ye decide karna nahi hai ki tumhe kya banna hai."),
    (24.30, 28.35, "It's also about understanding which career paths deserve your attention first."),
    (28.75, 32.10, "Yahi wajah hai ki Success Mappers ka concept interesting hai."),
    (32.54, 32.67, "Ye"),
    (32.76, 33.60, "personality,"),
    (33.73, 34.41, "interests,"),
    (34.56, 35.24, "aptitude,"),
    (35.34, 35.96, "skills confidence"),
    (36.15, 36.77, "aur"),
    (36.87, 39.55, "work values jaise aspects ko consider karke"),
    (39.87, 44.01, "tumhe different career directions aur unki priorities samajhne mein help karta hai."),
    (44.44, 46.73, "Taaki tumhare paas sirf options ki list nahi,"),
    (47.11, 51.52, "balki apne career ko explore karne aur next steps samajhne ka ek roadmap ho."),
    (51.97, 53.73, "Agar tum student ho ya parent,"),
    (53.99, 56.62, "Success Mappers ka 2-minute free scan try karo."),
    (56.99, 59.00, "Because choosing a career is important."),
    (59.36, 61.44, "Understanding your options matters too."),
]


def words():
    """Return [{'w', 'start', 'end', 'seg'}] for every word."""
    out = []
    for si, (s, e, text) in enumerate(SEGMENTS):
        toks = text.split()
        weights = [len(re.sub(r"[^\w]", "", t)) + 1.6 for t in toks]
        total = sum(weights)
        t = s
        for tok, wt in zip(toks, weights):
            d = (e - s) * wt / total
            out.append({"w": tok, "start": round(t, 3), "end": round(t + d, 3), "seg": si})
            t += d
    return out


def find(ws, word, after=0.0):
    """Start time of the first word matching `word` (case-insensitive) at or after `after`."""
    key = re.sub(r"[^\w-]", "", word.lower())
    for w in ws:
        if w["start"] >= after - 1e-6 and re.sub(r"[^\w-]", "", w["w"].lower()) == key:
            return w["start"]
    raise KeyError(f"{word} after {after}")


def chunks(ws, max_words=3, max_chars=20):
    """Group words into caption chunks; break on punctuation, segment change or size."""
    groups, cur = [], []
    for i, w in enumerate(ws):
        if cur and (w["seg"] != cur[-1]["seg"] or len(cur) >= max_words
                    or len(" ".join(x["w"] for x in cur + [w])) > max_chars):
            groups.append(cur)
            cur = []
        cur.append(w)
        if re.search(r"[,.?!…]$", w["w"]) or w["w"].endswith("..."):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


if __name__ == "__main__":
    ws = words()
    for g in chunks(ws):
        print(f'{g[0]["start"]:6.2f}-{g[-1]["end"]:6.2f}  ' + " ".join(x["w"] for x in g))
