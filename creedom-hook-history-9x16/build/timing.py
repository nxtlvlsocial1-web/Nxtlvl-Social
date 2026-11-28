"""Timing from the real take (voice kept exactly as recorded: loudnorm only, no trims, no tempo).
Writes audio/narration.m4a, audio/timing.json (engine format) and audio/words.json (per-line word times)."""
import json, pathlib, re, subprocess
P = pathlib.Path(__file__).resolve().parent.parent
TAIL = 2.2                      # end-card hold after the last word (silence added after the voice, voice untouched)
words = json.loads((P / "audio/words_whisper.json").read_text())
script = json.loads((P / "script.json").read_text())
lines = [l for t in script["takes"] for l in t["lines"]]
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
# last whisper token of each line
ends = ["rule", "way", "page", "film", "trailers", ("them", 2), "seconds", "watch", "seconds", "moves", "audience", "to", "post"]
segs, wl, k = [], {}, 0
for ln, end in zip(lines, ends):
    start = k
    end, n = end if isinstance(end, tuple) else (end, 1)
    while True:
        if norm(words[k]["w"]) == end:
            n -= 1
            if n == 0: break
        k += 1
    toks = words[start:k + 1]; k += 1
    wl[ln["id"]] = [{"w": norm(t["w"]), "s": t["s"], "e": t["e"]} for t in toks]
    segs.append({"id": ln["id"], "scene": 1, "caption": ln["text"], "vo": ln["spoken"],
                 "start": toks[0]["s"], "end": toks[-1]["e"], "duration": round(toks[-1]["e"] - toks[0]["s"], 3)})
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(P / "audio/vo_raw.mp3")],
                           capture_output=True, text=True).stdout)
total = round(dur + TAIL, 3)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P / "audio/vo_raw.mp3"), "-af",
                f"loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,apad=whole_dur={total}", "-ar", "48000", "-ac", "1",
                "-c:a", "aac", "-b:a", "192k", str(P / "audio/narration.m4a")], check=True)
(P / "audio/timing.json").write_text(json.dumps({"total_duration": total, "lead_in": 0, "tail_out": TAIL, "tempo": 1.0, "segments": segs}, indent=1))
(P / "audio/words.json").write_text(json.dumps(wl, indent=0))
for s in segs: print(f'{s["id"]:2d} {s["start"]:6.2f}-{s["end"]:6.2f}  {s["caption"]}')
print("total", total)
