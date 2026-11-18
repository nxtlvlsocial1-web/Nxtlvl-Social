"""Remove the background people from the handstand clip: YOLOv8x-seg finds every person, the athlete is tracked
(largest person at the start, then the best overlap frame to frame), everyone else is masked (dilated, minus the
athlete) and filled with LaMa (ONNX) on a padded crop. Frames in, frames out.

hsvenv/bin/python build/clean.py IN.mp4 OUTDIR [--only t1,t2,...] [--start S --end E]
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np
import onnxruntime as ort
from ultralytics import YOLO

MOD = os.environ.get("HS_MODELS", "models")
ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("--only", default="")
ap.add_argument("--start", type=float, default=0)
ap.add_argument("--end", type=float, default=1e9)
ap.add_argument("--dil", type=int, default=31)
ap.add_argument("--ctx", type=float, default=1.6)
ap.add_argument("--model", default="yolov8x-seg.pt")
ap.add_argument("--conf", type=float, default=.2)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
yolo = YOLO(os.path.join(MOD, a.model))
so = ort.SessionOptions()
so.intra_op_num_threads = 4
lama = ort.InferenceSession(os.path.join(MOD, "lama_fp32.onnx"), so)


def inpaint(img, mask):
    """LaMa on padded square crops around each masked blob group"""
    out = img.copy()
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    H, W = mask.shape
    boxes = [stats[i][:4] for i in range(1, n) if stats[i][4] > 50]
    # merge nearby blobs into crops
    crops = []
    for x, y, w, h in boxes:
        cx, cy = x + w / 2, y + h / 2
        s = int(max(w, h) * a.ctx + 64)
        s = max(s, 384)
        s = min(s, min(H, W))
        x0 = int(min(max(cx - s / 2, 0), W - s))
        y0 = int(min(max(cy - s / 2, 0), H - s))
        crops.append((x0, y0, s))
    for x0, y0, s in crops:
        ci = out[y0:y0 + s, x0:x0 + s]
        cm = mask[y0:y0 + s, x0:x0 + s]
        if cm.max() == 0:
            continue
        im = cv2.resize(cv2.cvtColor(ci, cv2.COLOR_BGR2RGB), (512, 512), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
        mm = (cv2.resize(cm, (512, 512), interpolation=cv2.INTER_NEAREST) > 0).astype(np.float32)
        r = lama.run(None, {"image": (im * (1 - mm[..., None])).transpose(2, 0, 1)[None], "mask": mm[None, None]})[0][0].transpose(1, 2, 0)
        if r.max() <= 1.5:
            r = r * 255
        r = cv2.cvtColor(np.clip(r, 0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        r = cv2.resize(r, (s, s), interpolation=cv2.INTER_CUBIC)
        al = cv2.GaussianBlur(cm.astype(np.float32) / 255, (0, 0), 3)[..., None]
        out[y0:y0 + s, x0:x0 + s] = (r * al + ci * (1 - al)).astype(np.uint8)
    return out


def iou(a, b):
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    i = max(0, x1 - x0) * max(0, y1 - y0)
    return i / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i + 1e-6)


cap = cv2.VideoCapture(a.src)
fps = cap.get(cv2.CAP_PROP_FPS)
only = [round(float(t) * fps) for t in a.only.split(",")] if a.only else None
prev = None
k = -1
K = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (a.dil, a.dil))
K2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
while True:
    ok, fr = cap.read()
    if not ok:
        break
    k += 1
    t = k / fps
    if t < a.start - 1e-6 or t > a.end or (only is not None and k not in only):
        continue
    res = yolo(fr, classes=[0], conf=a.conf, imgsz=960, retina_masks=True, verbose=False)[0]
    H, W = fr.shape[:2]
    ms, bs = [], []
    if res.masks is not None:
        for m, b in zip(res.masks.data.cpu().numpy(), res.boxes.xyxy.cpu().numpy()):
            ms.append((cv2.resize(m, (W, H)) > .5).astype(np.uint8) * 255)
            bs.append(b)
    if bs:
        # the athlete: overlap with the last frame's athlete plus size (he is always the biggest person in shot)
        si = int(np.argmax([(iou(b, prev) if prev is not None else 0) + 2 * ((b[2] - b[0]) * (b[3] - b[1])) / (W * H) for b in bs]))
        prev = bs[si]
        bg = np.zeros((H, W), np.uint8)
        for i, m in enumerate(ms):
            if i != si:
                cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if cs:
                    hull = cv2.convexHull(np.vstack(cs))
                    cv2.fillPoly(bg, [hull], 255)
        bg = cv2.dilate(bg, K)
        subj = cv2.GaussianBlur(cv2.dilate(ms[si], K2).astype(np.float32) / 255, (0, 0), 2)[..., None]
        outf = (fr * subj + inpaint(fr, bg) * (1 - subj)).astype(np.uint8) if bg.max() else fr
    else:
        outf = fr
    if only is None or k in only:
        cv2.imwrite(os.path.join(a.out, f"f{k:05d}.png"), outf)
        if only is not None:
            dbg = fr.copy()
            if bs:
                dbg[bg > 0] = (dbg[bg > 0] * .4 + np.array([0, 0, 255]) * .6).astype(np.uint8)
            cv2.imwrite(os.path.join(a.out, f"m{k:05d}.jpg"), cv2.resize(dbg, (540, 960)))
    if k % 30 == 0:
        print(f"{t:.1f}s", flush=True)
    if only is not None and k >= max(only):
        break
print("done", k)
