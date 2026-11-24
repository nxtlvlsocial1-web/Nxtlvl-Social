"""v4 voice: the owner's ElevenLabs take ("Blondie - Intense Woman", plan/elevenlabs_vo.md), shared by
creedom-postmortem-9x16 and creedom-grade-9x16 (identical copies).

1. Word times from faster-whisper small.en (local, no credits) on assets/audio/el/el_raw.mp3. Whisper splits decimals
   ("2", ".9"); a token that starts with "." is merged into the one before. The take matched the script, so the tokens
   are split into lines by the word counts of each line's "display" text and keep the display spelling.
2. Long silences are shortened for pace: a pause between lines keeps GAP_LINE seconds (or GAP[line] after that line),
   a pause inside a line keeps GAP_IN. The cut sits in the middle of each pause, with 12 ms fades at every join.
3. A light speed-up (CFG "tempo", 1.06: the delivery is slow and dramatic; real pauses are already 0.3-0.5 s), then
   the voice is polished like the others (high-pass, light compression, -16 LUFS) into assets/audio/vo.wav;
   plan/words.json gets the new word times.
HF_HOME=/root/tts/hf HF_HUB_OFFLINE=1 /root/tts/.venv/bin/python build/vo_el2.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets", "audio", "el", "el_raw.mp3")
CFG = json.load(open(os.path.join(ROOT, "plan", "vo_el2.json")))      # {"gap_line": .45, "gap_in": .7, "gap": {"f03": .9}}
LEAD, TAIL, SR = .06, .5, 48000


def main():
    from faster_whisper import WhisperModel
    script = json.load(open(os.path.join(ROOT, "plan", "script.json")))
    wm = WhisperModel("Systran/faster-whisper-small.en", device="cpu", compute_type="int8")
    segs, _ = wm.transcribe(RAW, word_timestamps=True, language="en", beam_size=5, vad_filter=False)
    toks = []
    for s in segs:
        for w in s.words:
            t = w.word.strip()
            if t.startswith(".") and toks:
                toks[-1] = (toks[-1][0] + t, toks[-1][1], w.end)
            else:
                toks.append((t, w.start, w.end))
    lines = [(ln["id"], ln["display"].replace('"', "").split()) for ln in script]
    need = sum(len(d) for _, d in lines)
    if need != len(toks):
        raise SystemExit(f"{len(toks)} words heard, {need} in the script: {[t[0] for t in toks]}")
    words, k = [], 0
    for lid, disp in lines:
        for d in disp:
            words.append({"line": lid, "w": d, "a": toks[k][1], "b": toks[k][2]})
            k += 1
    # keep-segments in the raw take
    keep, cur = [], max(0.0, words[0]["a"] - .04)
    for i in range(len(words) - 1):
        w, n = words[i], words[i + 1]
        allow = CFG["gap"].get(w["line"], CFG["gap_line"]) if n["line"] != w["line"] else CFG["gap_in"]
        gap = n["a"] - w["b"]
        if gap > allow:
            keep.append((cur, w["b"] + allow / 2))
            cur = n["a"] - allow / 2
    keep.append((cur, words[-1]["b"] + TAIL))
    # new word times
    def remap(t):
        out = LEAD
        for a, b in keep:
            if t <= b:
                return round(out + max(0.0, t - a), 3)
            out += b - a
        return round(out, 3)
    T = CFG.get("tempo", 1.0)
    tm = lambda t: round((remap(t) - LEAD) / T + LEAD, 3)
    res = [{"line": w["line"], "w": w["w"], "t0": tm(w["a"]), "t1": tm(w["b"])} for w in words]
    parts = []
    for i, (a, b) in enumerate(keep):
        parts.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0, b - a - .012):.3f}:d=0.012[p{i}]")
    graph = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[c];" \
        f"[c]atempo={CFG.get('tempo', 1.0)},adelay={int(LEAD * 1000)}:all=1,highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80:makeup=1.5,loudnorm=I=-16:TP=-2:LRA=9[o]"
    out = os.path.join(ROOT, "assets", "audio", "vo.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", RAW, "-filter_complex", graph, "-map", "[o]", "-ar", str(SR), "-ac", "1", out], check=True)
    json.dump(res, open(os.path.join(ROOT, "plan", "words.json"), "w"), indent=0)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    print(f"vo.wav {dur:.2f}s (raw {float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', RAW], capture_output=True, text=True).stdout):.2f}s), "
          f"{len(res)} words, {len(keep) - 1} pauses shortened")
    for lid, _ in lines:
        ws = [w for w in res if w["line"] == lid]
        print(f"  {lid} {ws[0]['t0']:6.2f} - {ws[-1]['t1']:6.2f}  {' '.join(w['w'] for w in ws)[:70]}")


if __name__ == "__main__":
    main()
