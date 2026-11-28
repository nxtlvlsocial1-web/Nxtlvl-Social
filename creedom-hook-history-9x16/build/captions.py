"""Word-by-word captions as a PNG state sequence (ffmpeg concat with durations), kept above Instagram's bottom UI
(band bottom at y 1500 of 1920). History lines highlight yellow, today/Creedom lines pink."""
import json, pathlib, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = pathlib.Path(__file__).resolve().parent.parent
OUT = P / "out" / "caps"; OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*.png"): f.unlink()
script = json.loads((P / "script.json").read_text()); words = json.loads((P / "audio/words.json").read_text())
tm = json.loads((P / "audio/timing.json").read_text())
FONT = ImageFont.truetype(str(P / "fonts/cond.ttf"), 104)
YEL, PINK, INK = (246, 206, 46), (243, 67, 162), (26, 16, 32)
W, H, CY = 1080, 1920, 1420
states = []        # (t0, t1, chunk_words, active_index, colour)
lines = [l for t in script["takes"] for l in t["lines"]]
for ln in lines:
    disp = ln["text"].replace("Creedom,", "Creedom").split()
    wt = words[str(ln["id"])]
    assert len(disp) == len(wt), (ln["id"], disp, [x["w"] for x in wt])
    col = YEL if ln["id"] <= 8 else PINK
    chunks, cur = [], []
    for i, w in enumerate(disp):
        cur.append(i)
        if len(cur) == 3 or sum(len(disp[j]) for j in cur) > 13 or re.search(r"[.,?]$", w):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for ch in chunks:
        for a, i in enumerate(ch):
            t0 = wt[i]["s"]
            t1 = wt[i + 1]["s"] if i + 1 < len(wt) else wt[i]["e"] + 0.3
            states.append((t0, t1, [disp[j].upper().strip(".,") for j in ch], a, col))
# render
def draw(chunk, act, col):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    gap = 26
    ws = [d.textlength(w, font=FONT) for w in chunk]
    total = sum(ws) + gap * (len(chunk) - 1)
    x = (W - total) / 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([x - 34, CY - 72, x + total + 34, CY + 62], 26, fill=(10, 8, 6, 175))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(2))); d = ImageDraw.Draw(im)
    for k, (w, wd) in enumerate(zip(chunk, ws)):
        if k == act:
            d.rounded_rectangle([x - 12, CY - 60, x + wd + 12, CY + 50], 14, fill=col + (255,))
            d.text((x, CY - 58), w, font=FONT, fill=(INK if col == YEL else (255, 255, 255)) + (255,))
        else:
            d.text((x, CY - 58), w, font=FONT, fill=(246, 243, 236, 255))
        x += wd + gap
    return im
blank = OUT / "blank.png"; Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)
lst, cursor = [], 0.0
for n, (t0, t1, ch, a, col) in enumerate(states):
    if t0 > cursor + 0.01:
        lst.append((blank, t0 - cursor))
    f = OUT / f"s{n:03d}.png"; draw(ch, a, col).save(f, optimize=False, compress_level=1)
    lst.append((f, t1 - max(t0, cursor))); cursor = t1
lst.append((blank, tm["total_duration"] - cursor + 0.5))
txt = "".join(f"file '{f}'\nduration {d:.3f}\n" for f, d in lst if d > 0) + f"file '{blank}'\n"
(OUT / "list.txt").write_text(txt)
print(len(states), "caption states")
