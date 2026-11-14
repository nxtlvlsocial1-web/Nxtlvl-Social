"""The showcase footage, made safe to publish: the owner's screen recording with the live MCP bearer token blurred.

The recording (assets/video/source_raw.mp4, 2212x1080, 60 fps, silent, kept out of git because it holds the token) zooms
and scrolls all through the AI assistants page, so the token row moves and changes size. Each frame is searched for the
"Authorization: Bearer" label (multi-scale template match, cut from the frame at 8.6 s) and everything from that label to
the end of the row is blurred hard and darkened, with the box smoothed over time. Frames with no match keep the last box
for a few frames. Writes assets/video/showcase.mp4 (30 fps, H.264) and build/token_track.json (for checking).
python3 build/safe_clip.py
"""
import json
import os
import subprocess

import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "video", "source_raw.mp4")
OUT = os.path.join(ROOT, "assets", "video", "showcase.mp4")
T0 = 7.6                                   # the AI assistants page starts loading here


def main():
    cap = cv2.VideoCapture(SRC); fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ref = cv2.imread(os.path.join(ROOT, "build", "token_ref.png"))                  # the frame at 8.6 s (ffmpeg, exact)
    tpl = cv2.cvtColor(ref[788:818, 915:1225], cv2.COLOR_BGR2GRAY)               # "Authorization: Bearer"
    cv2.imwrite(os.path.join(ROOT, "build", "token_tpl.png"), tpl)
    th, tw = tpl.shape
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frames, track = [], []
    for i in range(n):
        ok, f = cap.read()
        if not ok: break
        frames.append(f)
    cap.release()
    boxes = [None] * len(frames)
    D = .5                                                       # search at half resolution
    tplD = cv2.resize(tpl, (int(tw * D), int(th * D)), interpolation=cv2.INTER_AREA)
    prev = None                                                  # (x, y, w, h, scale) of the last hit, full-res
    for i, f in enumerate(frames):
        if i / fps < T0: continue
        g = cv2.cvtColor(cv2.resize(f, None, fx=D, fy=D, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        if prev is None: scales, roi = np.arange(.3, 1.31, .03), (0, 0, g.shape[1], g.shape[0])
        else:
            scales = np.arange(max(.25, prev[4] - .08), prev[4] + .081, .01)
            cx, cy = prev[0] * D, prev[1] * D
            roi = (int(max(0, cx - 160)), int(max(0, cy - 120)), int(min(g.shape[1], cx + prev[2] * D + 160)), int(min(g.shape[0], cy + prev[3] * D + 120)))
        sub = g[roi[1]:roi[3], roi[0]:roi[2]]; best = (0, None)
        for sc in scales:
            t2 = cv2.resize(tplD, (max(6, int(tplD.shape[1] * sc)), max(3, int(tplD.shape[0] * sc))), interpolation=cv2.INTER_AREA)
            if t2.shape[0] >= sub.shape[0] or t2.shape[1] >= sub.shape[1]: continue
            r = cv2.matchTemplate(sub, t2, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
            if mv > best[0]: best = (mv, ((ml[0] + roi[0]) / D, (ml[1] + roi[1]) / D, t2.shape[1] / D, t2.shape[0] / D, sc))
        if best[0] > .78 and best[1][3] >= 14:
            boxes[i] = best[1][:4]; prev = best[1]
        else:
            prev = None
        track.append({"t": round(i / fps, 3), "score": round(float(best[0]), 3), "box": best[1][:4] if best[1] else None})
    # fill gaps: between two good frames (up to 40 frames apart) interpolate the box and widen it 25%; at the ends, copy
    # the nearest good box (up to 12 frames away)
    good = [i for i, bx in enumerate(boxes) if bx is not None]
    filled = list(boxes)
    for i in range(int(T0 * fps), len(boxes)):
        if boxes[i] is not None or not good: continue
        pv = [g for g in good if g < i]; nx = [g for g in good if g > i]
        if pv and nx and nx[0] - pv[-1] <= 40:
            u = (i - pv[-1]) / (nx[0] - pv[-1]); A, B2 = np.array(boxes[pv[-1]]), np.array(boxes[nx[0]])
            x, y, w, h = A + (B2 - A) * u; filled[i] = (x - .05 * w, y - .25 * h, w * 1.1, h * 1.5)
        else:
            j = min(good, key=lambda g: abs(g - i))
            if abs(j - i) <= 12: filled[i] = boxes[j]
    sm = []
    for i in range(len(filled)):
        win = [filled[j] for j in range(max(0, i - 2), min(len(filled), i + 3)) if filled[j] is not None]
        sm.append(tuple(np.median(win, axis=0)) if win and filled[i] is not None else None)
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{frames[0].shape[1]}x{frames[0].shape[0]}", "-r", str(fps), "-i", "-",
                             "-vf", "fps=30", "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i, f in enumerate(frames):
        b = sm[i]
        if b is not None:
            x, y, w, h = b
            x0, y0 = int(max(0, x - .08 * w)), int(max(0, y - .7 * h)); x1, y1 = int(min(f.shape[1], x + 3.78 * w)), int(min(f.shape[0], y + 1.7 * h))
            roi = f[y0:y1, x0:x1]
            if roi.size:
                k = max(15, int(h * 1.6) | 1)
                f[y0:y1, x0:x1] = (cv2.GaussianBlur(roi, (k, k), 0) * .55 + 12).astype(np.uint8)
        proc.stdin.write(f.tobytes())
    proc.stdin.close(); proc.wait()
    json.dump(track, open(os.path.join(ROOT, "build", "token_track.json"), "w"))
    hit = sum(1 for b in boxes[int(T0 * fps):] if b is not None); tot = len(boxes) - int(T0 * fps)
    print(f"wrote {OUT}; token found in {hit}/{tot} frames after {T0}s")


if __name__ == "__main__":
    main()
