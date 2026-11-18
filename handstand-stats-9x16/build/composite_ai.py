"""Combine the Higgsfield FLUX 3 Video Edit result (people removed, but 704x1248 / 24 fps and slightly reframed) with the
original 1080x1920 / 30 fps footage: the original stays everywhere except where background people stood; there, the AI
frame nearest in time is upscaled, sharpened, aligned to the original (SIFT + RANSAC homography on the background) and
colour-matched on a ring around the hole. The athlete always comes from the original, so he stays sharp and untouched.

hsvenv/bin/python build/composite_ai.py ORIG.mp4 AI.mp4 OUTDIR --last 84
"""
import argparse
import os

import cv2
import numpy as np
from ultralytics import YOLO

ap = argparse.ArgumentParser()
ap.add_argument("orig")
ap.add_argument("ai")
ap.add_argument("out")
ap.add_argument("--last", type=int, default=84)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
yolo = YOLO(os.path.join(os.environ.get("HS_MODELS", "models"), "yolov8x-seg.pt"))
sift = cv2.SIFT_create(5000)
bf = cv2.BFMatcher(cv2.NORM_L2)


def read_all(p):
    c, fs = cv2.VideoCapture(p), []
    fps = c.get(cv2.CAP_PROP_FPS)
    while True:
        ok, f = c.read()
        if not ok:
            return fs, fps
        fs.append(f)


O, ofps = read_all(a.orig)
A, afps = read_all(a.ai)
H, W = O[0].shape[:2]
print(len(O), ofps, len(A), afps, flush=True)
prev = None
for i in range(0, a.last + 1):
    fr = O[i]
    r = yolo(fr, classes=[0], conf=.25, imgsz=960, retina_masks=True, verbose=False)[0]
    ms, bs = [], []
    if r.masks is not None:
        for m, b in zip(r.masks.data.cpu().numpy(), r.boxes.xyxy.cpu().numpy()):
            ms.append((cv2.resize(m, (W, H)) > .5).astype(np.uint8) * 255)
            bs.append(b)
    if len(bs) < 2:
        cv2.imwrite(os.path.join(a.out, f"f{i:05d}.png"), fr)
        continue
    si = int(np.argmax([(b[2] - b[0]) * (b[3] - b[1]) for b in bs]))
    hole = np.zeros((H, W), np.uint8)
    allm = np.zeros((H, W), np.uint8)
    for j, m in enumerate(ms):
        allm |= m
        if j != si:
            cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cs:
                cv2.fillPoly(hole, [cv2.convexHull(np.vstack(cs))], 255)
    hole = cv2.dilate(hole, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    # the AI frame nearest in time, upscaled and lightly sharpened
    k = min(len(A) - 1, int(round(i / ofps * afps)))   # AI clip retimed to 30 fps first (minterpolate), so k == i
    ai = cv2.resize(A[k], (W, H), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(ai, (0, 0), 1.2)
    ai = cv2.addWeighted(ai, 1.5, bl, -.5, 0)
    # align AI -> original on the background (people and the hole excluded in the original)
    excl = cv2.dilate(allm | hole, np.ones((25, 25), np.uint8))
    ko, do = sift.detectAndCompute(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), cv2.bitwise_not(excl))
    ka, da = sift.detectAndCompute(cv2.cvtColor(ai, cv2.COLOR_BGR2GRAY), None)
    mt = [m for m, n in bf.knnMatch(da, do, k=2) if m.distance < .72 * n.distance]
    Hm = None
    if len(mt) >= 30:
        Hm, inl = cv2.findHomography(np.float32([ka[m.queryIdx].pt for m in mt]), np.float32([ko[m.trainIdx].pt for m in mt]), cv2.RANSAC, 2.0)
    if Hm is None:
        print(f"frame {i}: no alignment, kept original", flush=True)
        cv2.imwrite(os.path.join(a.out, f"f{i:05d}.png"), fr)
        continue
    aw = cv2.warpPerspective(ai, Hm, (W, H), flags=cv2.INTER_LINEAR)
    av = cv2.warpPerspective(np.full((H, W), 255, np.uint8), Hm, (W, H), flags=cv2.INTER_NEAREST)
    # smooth colour match on a ring of clean background around the holes
    ring = (cv2.dilate(hole, np.ones((81, 81), np.uint8)) > 0) & (hole == 0) & (allm == 0) & (av > 0)
    rv = ring.astype(np.float32)
    num = cv2.GaussianBlur((fr.astype(np.float32) - aw.astype(np.float32)) * rv[..., None], (0, 0), 45)
    den = cv2.GaussianBlur(rv, (0, 0), 45)[..., None]
    fill = np.clip(aw.astype(np.float32) + np.clip(np.where(den > 1e-3, num / np.maximum(den, 1e-3), 0), -40, 40), 0, 255)
    use = ((hole > 0) & (av > 0)).astype(np.float32)
    al = np.clip(cv2.GaussianBlur(use, (0, 0), 5) * 2 - 1, 0, 1)[..., None]
    out = fill * al + fr.astype(np.float32) * (1 - al)
    subj = cv2.GaussianBlur(cv2.dilate(ms[si], np.ones((7, 7), np.uint8)).astype(np.float32) / 255, (0, 0), 1.5)[..., None]
    # where the athlete's mask overlaps a removed person, the mask can swallow that person (they stand right behind him):
    # there, pixels that clearly differ from the AI frame (which has the athlete but not the person) take the AI pixels
    ov = ((hole > 0) & (ms[si] > 0) & (av > 0)).astype(np.float32)
    if ov.sum() > 1500:
        # heavy overlap (the person stands right behind him): take the whole patch, athlete included, from the AI frame
        R = cv2.dilate(((hole > 0) | (ms[si] > 0)).astype(np.uint8) * 255, np.ones((25, 25), np.uint8))
        ring2 = (cv2.dilate(R, np.ones((81, 81), np.uint8)) > 0) & (R == 0) & (allm == 0) & (av > 0)
        rv2 = ring2.astype(np.float32)
        num2 = cv2.GaussianBlur((fr.astype(np.float32) - aw.astype(np.float32)) * rv2[..., None], (0, 0), 45)
        den2 = cv2.GaussianBlur(rv2, (0, 0), 45)[..., None]
        fill2 = np.clip(aw.astype(np.float32) + np.clip(np.where(den2 > 1e-3, num2 / np.maximum(den2, 1e-3), 0), -40, 40), 0, 255)
        w2 = np.clip(cv2.GaussianBlur(((R > 0) & (av > 0)).astype(np.float32), (0, 0), 6) * 2 - 1, 0, 1)[..., None]
        out = (fill2 * w2 + fr.astype(np.float32) * (1 - w2)).astype(np.uint8)
        cv2.imwrite(os.path.join(a.out, f"f{i:05d}.png"), out)
        print("out", i, len(mt), "patch", flush=True)
        continue
    if ov.any():
        d = np.abs(fr.astype(np.float32) - fill).mean(2)
        d = cv2.GaussianBlur(d, (0, 0), 3)
        w = np.clip((d - 22) / 30, 0, 1) * cv2.GaussianBlur(ov, (0, 0), 2)
        w = cv2.GaussianBlur(w, (0, 0), 3)[..., None]
        subj = subj * (1 - w)
        out = fill * w + out * (1 - w)
    out = (fr * subj + out * (1 - subj)).astype(np.uint8)
    cv2.imwrite(os.path.join(a.out, f"f{i:05d}.png"), out)
    print("out", i, len(mt), flush=True)
print("done")
