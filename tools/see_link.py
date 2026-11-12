"""See a reel or video from its link: download it, then turn it into things Claude can read.

  python3 tools/see_link.py URL [--out DIR] [--frames 16] [--ears]
  python3 tools/see_link.py --file VIDEO.mp4 [--out DIR] ...     (a file already downloaded or uploaded)

Writes to DIR (default: a folder named after the post id in the scratchpad or /tmp):
  video.mp4        the file (Instagram works; YouTube refuses video downloads from cloud machines, see below)
  info.txt         title / creator / length / caption / likes and views when public
  sheet.jpg        a contact sheet of --frames evenly spaced frames, each labelled with its time
  frames/          the frames themselves (frame_<seconds>.jpg)
  transcript.txt   the speech with timestamps (faster-whisper small.en, local, free)
  ears.txt         with --ears: earshot's listening transcript of the sound (music, hits, levels)

Instagram lets a cloud machine fetch only a few posts anonymously, then asks for a login ("rate-limit for accessing
posts anonymously"); wait a while, or upload the file and use --file. YouTube: from cloud machines it answers "Sign in to confirm you're not a bot" / 403 for the video file. We never pass
the owner's cookies or pose as a browser to get round that. The script then falls back to what YouTube still serves:
the info and the caption track (transcript.txt from the subtitles). For the picture, download the video on a phone and
upload the file instead.

Needs: ffmpeg; yt-dlp in /root/tools/ytdlp (installed on first use: python3 -m venv + pip install "yt-dlp[default]");
optional /root/tts/.venv (faster-whisper) for transcripts and /root/tools/earshot for --ears.
Reference only: a downloaded reel is for studying, never for reuse in a client video.
"""
import argparse
import json
import os
import re
import subprocess
import sys

YTDLP_VENV = "/root/tools/ytdlp"
YTDLP = os.path.join(YTDLP_VENV, "bin", "yt-dlp")
TTS_PY = "/root/tts/.venv/bin/python"
EARSHOT = "/root/tools/earshot/.venv/bin/earshot"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def ensure_ytdlp():
    if os.path.exists(YTDLP):
        return
    print("installing yt-dlp ...", flush=True)
    run([sys.executable, "-m", "venv", YTDLP_VENV])
    r = run([os.path.join(YTDLP_VENV, "bin", "python"), "-m", "pip", "install", "-q", "yt-dlp[default]"])
    if r.returncode:
        sys.exit("could not install yt-dlp:\n" + r.stderr[-800:])


def post_id(url):
    m = re.search(r"/(?:reel|reels|p|shorts|tv)/([A-Za-z0-9_-]+)", url) or re.search(r"[?&]v=([A-Za-z0-9_-]+)", url) \
        or re.search(r"youtu\.be/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else "link"


def download(url, out):
    base = [YTDLP, "--js-runtimes", "node", "--no-playlist", "--write-info-json", "-o", os.path.join(out, "video.%(ext)s")]
    r = run(base + ["-f", "bv*[height<=1920]+ba/b", "--merge-output-format", "mp4", url])
    ok = os.path.exists(os.path.join(out, "video.mp4"))
    if not ok:
        print("video download refused:", (re.findall(r"ERROR: (.*)", r.stderr) or [r.stderr[-300:]])[-1], flush=True)
        # what YouTube still serves to cloud machines: the info and the caption track
        run(base + ["--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", "en,en-orig,en-US", "--sub-format", "vtt", url])
    return ok


def write_info(out):
    j = next((os.path.join(out, f) for f in os.listdir(out) if f.endswith(".info.json")), None)
    if not j:
        return {}
    d = json.load(open(j))
    keep = {k: d.get(k) for k in ("title", "uploader", "channel", "duration", "view_count", "like_count", "comment_count",
                                  "upload_date", "width", "height", "webpage_url")}
    desc = (d.get("description") or "").strip()
    with open(os.path.join(out, "info.txt"), "w") as f:
        for k, v in keep.items():
            if v not in (None, ""):
                f.write(f"{k}: {v}\n")
        if desc:
            f.write("\ncaption:\n" + desc + "\n")
    return d


def sheet(video, out, n):
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]).stdout.strip() or 0)
    fd = os.path.join(out, "frames")
    os.makedirs(fd, exist_ok=True)
    times = [round(dur * (i + .5) / n, 2) for i in range(n)]
    paths = []
    for t in times:
        p = os.path.join(fd, f"frame_{t:06.2f}.jpg")
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", "scale=360:-2", "-q:v", "3", p])
        if os.path.exists(p):
            paths.append((t, p))
    if not paths:
        return dur
    cols = 4 if len(paths) > 9 else 3
    # one ffmpeg tile, each frame stamped with its time
    inputs, labels = [], []
    for k, (t, p) in enumerate(paths):
        inputs += ["-i", p]
        labels.append(f"[{k}:v]scale=360:640:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2,"
                      f"drawtext=text='{t:.1f}s':x=10:y=10:fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6[f{k}]")
    rows = (len(paths) + cols - 1) // cols
    while len(labels) < rows * cols:                     # pad the grid
        k = len(labels)
        labels.append(f"color=c=black:s=360x640:d=1[f{k}]")
    grid = "".join(f"[f{k}]" for k in range(rows * cols))
    layout = "|".join(f"{(k % cols) * 360}_{(k // cols) * 640}" for k in range(rows * cols))
    fc = ";".join(labels) + f";{grid}xstack=inputs={rows * cols}:layout={layout}[o]"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc, "-map", "[o]", "-frames:v", "1", "-q:v", "3",
         os.path.join(out, "sheet.jpg")])
    return dur


def transcribe(video, out):
    if not os.path.exists(TTS_PY):
        return False
    code = ("import sys\nfrom faster_whisper import WhisperModel\n"
            "m=WhisperModel('Systran/faster-whisper-small.en',device='cpu',compute_type='int8')\n"
            "segs,_=m.transcribe(sys.argv[1],language='en',vad_filter=True)\n"
            "open(sys.argv[2],'w').write(''.join(f'[{s.start:6.2f} - {s.end:6.2f}] {s.text.strip()}\\n' for s in segs))\n")
    env = dict(os.environ, HF_HOME="/root/tts/hf", HF_HUB_OFFLINE="1")
    r = run([TTS_PY, "-c", code, video, os.path.join(out, "transcript.txt")], env=env)
    return r.returncode == 0


def subs_to_transcript(out):
    vtt = next((os.path.join(out, f) for f in sorted(os.listdir(out)) if f.endswith(".vtt")), None)
    if not vtt:
        return False
    lines, last = [], None
    for block in open(vtt).read().split("\n\n"):
        m = re.search(r"(\d+:\d+:\d+\.\d+) -->", block)
        txt = " ".join(l for l in block.splitlines() if l and "-->" not in l and not l.startswith(("WEBVTT", "Kind:", "Language:")))
        txt = re.sub(r"<[^>]+>", "", txt).strip()
        if m and txt and txt != last:
            lines.append(f"[{m.group(1)}] {txt}")
            last = txt
    open(os.path.join(out, "transcript.txt"), "w").write("\n".join(lines) + "\n")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?")
    ap.add_argument("--file", help="analyse this local video instead of downloading")
    ap.add_argument("--out")
    ap.add_argument("--frames", type=int, default=16)
    ap.add_argument("--ears", action="store_true")
    a = ap.parse_args()
    if not a.url and not a.file:
        ap.error("give a URL or --file")
    out = a.out or os.path.join(os.environ.get("TMPDIR", "/tmp"), "see_link",
                                post_id(a.url) if a.url else os.path.splitext(os.path.basename(a.file))[0])
    os.makedirs(out, exist_ok=True)
    if a.file:
        import shutil
        if os.path.abspath(a.file) != os.path.abspath(os.path.join(out, "video.mp4")):
            shutil.copy(a.file, os.path.join(out, "video.mp4"))
        for f in os.listdir(os.path.dirname(os.path.abspath(a.file))):      # an info.json next to it, if any
            if f.endswith(".info.json"):
                shutil.copy(os.path.join(os.path.dirname(os.path.abspath(a.file)), f), out)
        got = True
    else:
        ensure_ytdlp()
        got = download(a.url, out)
    info = write_info(out)
    print(f"{info.get('title') or ''} | {info.get('uploader') or info.get('channel') or ''} | {info.get('duration')} s")
    if got:
        video = os.path.join(out, "video.mp4")
        sheet(video, out, a.frames)
        print("frames:", "ok" if os.path.exists(os.path.join(out, "sheet.jpg")) else "failed")
        print("transcript:", "ok" if transcribe(video, out) else "skipped (no faster-whisper)")
        if a.ears and os.path.exists(EARSHOT):
            r = run([EARSHOT, "timeline", video], timeout=900)
            open(os.path.join(out, "ears.txt"), "w").write(r.stdout or r.stderr)
            print("ears: ok")
    else:
        print("transcript from captions:", "ok" if subs_to_transcript(out) else "none available")
    print("out:", out)


if __name__ == "__main__":
    main()
