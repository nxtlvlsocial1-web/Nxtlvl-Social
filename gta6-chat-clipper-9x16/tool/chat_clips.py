#!/usr/bin/env python3
"""chat_clips.py - find a stream's best moments from its chat.

When something crazy happens on stream, chat explodes. This tool
reads the chat (downloaded with the free TwitchDownloader), counts
messages in 10-second windows, finds the spikes, and cuts each
moment into a vertical 1080x1920 clip with FFmpeg. Chat reacts
late, so every clip starts 20 seconds before the spike.

Needs Python 3.8+ and FFmpeg. Nothing else to install.

  python chat_clips.py chat.json             list the top moments
  python chat_clips.py chat.json stream.mp4  cut them into clips/

Options:
  --top 10      how many clips
  --window 10   seconds per counting window
  --pre 20      seconds of lead-in before each spike
  --length 40   clip length in seconds
  --crop        fill the frame by cropping the centre
                (default: the full picture on a blurred background)
  --out clips   output folder

Only clip streams you own, or ones whose streamer has given you
permission to clip and post.
"""
import argparse
import csv
import json
import os
import shutil
import statistics
import subprocess
import sys

HYPE = {
    "lmao", "lmfao", "lol", "lul", "kekw", "omegalul", "icant",
    "w", "ww", "www", "clip", "clipit", "clip it", "no way", "noway",
    "wtf", "omg", "pog", "poggers", "pogchamp", "ayo", "bro", "nah",
    "insane", "crazy", "holy", "???", "!!!",
}


def load_chat(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        comments = data
    else:
        comments = data.get("comments", [])
    out = []
    for c in comments:
        t = c.get("content_offset_seconds")
        if t is None:
            continue
        msg = c.get("message") or {}
        if isinstance(msg, dict):
            body = msg.get("body") or ""
        else:
            body = str(msg)
        out.append((float(t), body))
    if not out:
        sys.exit("No chat messages found. "
                 "Is this a TwitchDownloader chat .json file?")
    return sorted(out)


def weight(body):
    """a normal message counts 1, a hype reaction (LMAO, KEKW,
    CLIP IT, ???) counts 2, shouting counts 1.5"""
    b = body.lower().strip()
    for h in HYPE:
        if b == h or b.startswith(h + " ") or \
                (" " + h + " ") in (" " + b + " "):
            return 2.0
    letters = [ch for ch in body if ch.isalpha()]
    shout = len(letters) >= 3 and all(ch.isupper() for ch in letters)
    if b.count("?") >= 3 or b.count("!") >= 3 or shout:
        return 1.5
    return 1.0


def find_spikes(chat, window, top, length, pre):
    n = int(chat[-1][0] // window) + 1
    counts, raw = [0.0] * n, [0] * n
    for t, body in chat:
        i = int(t // window)
        counts[i] += weight(body)
        raw[i] += 1
    # baseline: the median of the surrounding 5 minutes, so a busy
    # chat and a quiet chat are judged fairly
    half = max(3, int(150 // window))
    scores = []
    for i in range(n):
        lo, hi = max(0, i - half), min(n, i + half + 1)
        base = statistics.median(counts[lo:hi]) or 1.0
        scores.append(counts[i] / max(base, 1.0))
    order = sorted(range(n), key=lambda i: (scores[i], counts[i]),
                   reverse=True)
    picked = []
    for i in order:
        if counts[i] < 5 or scores[i] < 2.0:
            continue
        start = max(0.0, i * window - pre)
        if all(abs(start - p["start"]) >= length for p in picked):
            picked.append({"start": start, "messages": raw[i],
                           "score": round(scores[i], 1)})
        if len(picked) >= top:
            break
    return sorted(picked, key=lambda p: p["start"]), n


def hms(s):
    s = int(s)
    return f"{s // 3600}h{s % 3600 // 60:02d}m{s % 60:02d}s"


def cut(video, spike, length, crop, path):
    if crop:
        args = ["-vf", "crop=ih*9/16:ih,scale=1080:1920"]
    else:
        fc = ("[0:v]split=2[a][b];"
              "[a]scale=1080:1920:force_original_aspect_ratio=increase,"
              "crop=1080:1920,boxblur=24:2,eq=brightness=-0.08[bg];"
              "[b]scale=1080:-2[fg];"
              "[bg][fg]overlay=(W-w)/2:(H-h)/2[v]")
        args = ["-filter_complex", fc, "-map", "[v]", "-map", "0:a?"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-ss", f"{spike['start']:.2f}", "-t", f"{length:.2f}",
           "-i", video, *args,
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
           path]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(
        description="Find a stream's best moments from its chat.")
    ap.add_argument("chat", help="the chat .json from TwitchDownloader")
    ap.add_argument("video", nargs="?", help="the stream video (.mp4)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--window", type=float, default=10)
    ap.add_argument("--pre", type=float, default=20)
    ap.add_argument("--length", type=float, default=40)
    ap.add_argument("--crop", action="store_true")
    ap.add_argument("--out", default="clips")
    a = ap.parse_args()

    chat = load_chat(a.chat)
    spikes, n = find_spikes(chat, a.window, a.top, a.length, a.pre)
    print(f"{len(chat)} chat messages, {hms(chat[-1][0])} of stream, "
          f"{n} windows of {a.window:g} s")
    if not spikes:
        print("No clear spikes. Try --window 15 or a busier stream.")
        return
    print(f"Top {len(spikes)} moments "
          f"(each clip starts {a.pre:g} s before the spike):")
    for k, s in enumerate(spikes, 1):
        print(f"  #{k:<2} {hms(s['start'])}  {s['messages']:>4} "
              f"messages  {s['score']:>5}x normal")

    if not a.video:
        print("\nAdd the stream video to cut these into clips:\n"
              "  python chat_clips.py chat.json stream.mp4")
        return
    if not shutil.which("ffmpeg"):
        sys.exit("FFmpeg not found. Install it (see the guide).")
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "moments.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["clip", "starts_at", "messages", "x_normal"])
        for k, s in enumerate(spikes, 1):
            name = f"clip_{k:02d}_{hms(s['start'])}.mp4"
            print(f"cutting {name} ...", flush=True)
            cut(a.video, s, a.length, a.crop,
                os.path.join(a.out, name))
            w.writerow([name, hms(s["start"]), s["messages"],
                        s["score"]])
    print(f"\nDone: {len(spikes)} vertical clips in {a.out}/")


if __name__ == "__main__":
    main()
