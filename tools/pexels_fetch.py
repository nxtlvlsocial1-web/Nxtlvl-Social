"""Download Pexels videos by id, without the API (Pexels has paused new API keys).

Pexels' site and API answer cloud machines with 403 / need a key, but its file server (videos.pexels.com) serves the
same public files the site's "Free download" button gives. Each file is named <id>-<quality>_<w>_<h>_<fps>fps.mp4, so
the likely names are tried with HEAD requests (nothing is faked: a plain curl) and the first HD file found is saved.
Find ids with a web search restricted to pexels.com (the id ends each video page URL: .../video/<slug>-<id>/).
Licence: the Pexels licence (free for commercial use, no credit required; do not sell the clips as they are).

python3 tools/pexels_fetch.py OUT_DIR ID [ID ...]      -> OUT_DIR/<id>.mp4 and OUT_DIR/pexels.json
"""
import json
import os
import subprocess
import sys

SIZES = ["hd_1920_1080", "hd_1080_1920", "hd_2048_1080", "hd_1080_2048", "hd_1280_720", "hd_720_1280", "hd_1366_720", "hd_720_1366",
         "uhd_2560_1440", "uhd_1440_2560", "uhd_3840_2160", "uhd_2160_3840", "uhd_4096_2160", "uhd_2160_4096", "sd_960_540", "sd_540_960"]
FPS = ["25", "30", "24", "50", "60"]


def head(url):
    r = subprocess.run(["curl", "-sS", "-I", "-o", "/dev/null", "-m", "10", "-w", "%{http_code}", url], capture_output=True, text=True)
    return r.stdout.strip() == "200"


def find(vid):
    for size in SIZES:
        for fps in FPS:
            url = f"https://videos.pexels.com/video-files/{vid}/{vid}-{size}_{fps}fps.mp4"
            if head(url):
                return url
    return None


def main():
    out, ids = sys.argv[1], sys.argv[2:]
    os.makedirs(out, exist_ok=True)
    log_p = os.path.join(out, "pexels.json")
    log = json.load(open(log_p)) if os.path.exists(log_p) else {}
    for vid in ids:
        dst = os.path.join(out, f"{vid}.mp4")
        if os.path.exists(dst):
            print(vid, "already here")
            continue
        url = find(vid)
        if not url:
            print(vid, "no file found")
            continue
        subprocess.run(["curl", "-sS", "-L", "-o", dst, url], check=True)
        info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height:format=duration",
                               "-of", "json", dst], capture_output=True, text=True).stdout
        j = json.loads(info)
        st = j["streams"][0]
        log[vid] = {"file": url, "page": f"https://www.pexels.com/video/{vid}/", "w": st["width"], "h": st["height"],
                    "dur": round(float(j["format"]["duration"]), 2), "licence": "Pexels licence"}
        print(vid, st["width"], "x", st["height"], log[vid]["dur"], "s")
        json.dump(log, open(log_p, "w"), indent=1)


if __name__ == "__main__":
    main()
