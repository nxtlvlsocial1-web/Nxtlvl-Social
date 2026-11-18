"""Remove the background people with REAL background pixels (no AI fill): a clean-plate composite.

1. Every 6th frame of the whole clip is aligned to the freeze frame (SIFT features on the background only, RANSAC
   homography: the phone mostly rotates, so one homography holds for the wall, the banner and the grass).
2. People (YOLOv8x-seg, all of them, the athlete too) are masked out and the per-pixel median of the aligned frames
   gives one clean plate of the place, on a canvas bigger than the frame so pans are covered.
3. For each output frame the plate is warped back into it, colour-matched on a ring around each hole, and fills the
   background people (convex hull, dilated); the athlete is pasted back on top from his own mask.

hsvenv/bin/python build/plate.py IN.mp4 OUTDIR --last 84 [--step 6]
"""
import argparse
import os

import cv2
import numpy as np
from ultralytics import YOLO

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("--last", type=int, default=84)          # output frames 0..last; the freeze frame is the reference
ap.add_argument("--step", type=int, default=6)
ap.add_argument("--pad", type=int, default=500)
ap.add_argument("--plate", default="")      # reuse a plate.png / plate_have.png pair from an earlier run
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
yolo = YOLO(os.path.join(os.environ.get("HS_MODELS", "models"), "yolov8x-seg.pt"))
sift = cv2.SIFT_create(4000)
P = a.pad
T = np.array([[1, 0, P], [0, 1, P], [0, 0, 1]], np.float64)   # frame-of-reference -> canvas


def people(fr):
    r = yolo(fr, classes=[0], conf=.25, imgsz=960, retina_masks=True, verbose=False)[0]
    H, W = fr.shape[:2]
    ms, bs = [], []
    if r.masks is not None:
        for m, b in zip(r.masks.data.cpu().numpy(), r.boxes.xyxy.cpu().numpy()):
            ms.append((cv2.resize(m, (W, H)) > .5).astype(np.uint8) * 255)
            bs.append(b)
    return ms, bs


def feats(fr, mask):
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    return sift.detectAndCompute(g, cv2.bitwise_not(cv2.dilate(mask, np.ones((25, 25), np.uint8))))


cap = cv2.VideoCapture(a.src)
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
N, (H, W) = len(frames), frames[0].shape[:2]
print("frames", N, flush=True)
ref = frames[a.last]
rms, rbs = people(ref)
rall = np.zeros((H, W), np.uint8)
for m in rms:
    rall |= m
rk, rd = feats(ref, rall)
bf = cv2.BFMatcher(cv2.NORM_L2)


def homog(fr, allm):
    k, d = feats(fr, allm)
    mt = [m for m, n in bf.knnMatch(d, rd, k=2) if m.distance < .72 * n.distance]
    if len(mt) < 30:
        return None
    src = np.float32([k[m.queryIdx].pt for m in mt])
    dst = np.float32([rk[m.trainIdx].pt for m in mt])
    Hm, inl = cv2.findHomography(src, dst, cv2.RANSAC, 2.5)
    return Hm if inl is not None and inl.sum() > 25 else None


# ---- 1-2: the clean plate ---------------------------------------------------------------------------------------------------
CH, CW = H + 2 * P, W + 2 * P
warps, valids = [], []
for i in (range(0, N, a.step) if not a.plate else []):
    fr = frames[i]
    ms, _ = people(fr)
    allm = np.zeros((H, W), np.uint8)
    for m in ms:
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if cs:
            cv2.fillPoly(allm, [cv2.convexHull(np.vstack(cs))], 255)
    Hm = homog(fr, allm)
    if Hm is None:
        continue
    M = T @ Hm
    warps.append(cv2.warpPerspective(fr, M, (CW, CH), flags=cv2.INTER_LINEAR))
    ok = cv2.warpPerspective(np.full((H, W), 255, np.uint8), M, (CW, CH), flags=cv2.INTER_NEAREST)
    ok = cv2.erode(ok, np.ones((5, 5), np.uint8))
    ok[cv2.warpPerspective(cv2.dilate(allm, np.ones((41, 41), np.uint8)), M, (CW, CH), flags=cv2.INTER_NEAREST) > 0] = 0
    valids.append(ok > 0)
    print("plate", i, flush=True)
plate = np.zeros((CH, CW, 3), np.uint8)
have = np.zeros((CH, CW), bool)
if a.plate:
    plate = cv2.imread(os.path.join(a.plate, "plate.png"))
    have = cv2.imread(os.path.join(a.plate, "plate_have.png"), 0) > 0
for y0 in (range(0, CH, 160) if not a.plate else []):
    st = np.stack([w[y0:y0 + 160] for w in warps]).astype(np.float32)
    vm = np.stack([v[y0:y0 + 160] for v in valids])
    st[~vm] = np.nan
    med = np.nanmedian(st, axis=0)
    have[y0:y0 + 160] = vm.any(0)
    plate[y0:y0 + 160] = np.nan_to_num(med).astype(np.uint8)
cv2.imwrite(os.path.join(a.out, "plate.png"), plate)
cv2.imwrite(os.path.join(a.out, "plate_have.png"), have.astype(np.uint8) * 255)
del warps, valids

# ---- 3: fill each output frame -------------------------------------------------------------------------------------------------
prev = None
K = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
for i in range(0, a.last + 1):
    fr = frames[i]
    ms, bs = people(fr)
    if not bs:
        cv2.imwrite(os.path.join(a.out, f"f{i:05d}.png"), fr)
        continue
    si = int(np.argmax([((lambda b, p: 0 if p is None else max(0, min(b[2], p[2]) - max(b[0], p[0])) * max(0, min(b[3], p[3]) - max(b[1], p[1])) /
                          ((b[2] - b[0]) * (b[3] - b[1])))(b, prev)) + 2 * (b[2] - b[0]) * (b[3] - b[1]) / (W * H) for b in bs]))
    prev = bs[si]
    hole = np.zeros((H, W), np.uint8)
    allm = ms[si].copy()
    for j, m in enumerate(ms):
        allm |= m
        if j != si:
            cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cs:
                cv2.fillPoly(hole, [cv2.convexHull(np.vstack(cs))], 255)
    hole = cv2.dilate(hole, K)
    Hm = homog(fr, allm) if i != a.last else np.eye(3)
    out = fr.copy()
    if hole.max() and Hm is not None:
        Mi = np.linalg.inv(T @ Hm)
        bgw = cv2.warpPerspective(plate, Mi, (W, H), flags=cv2.INTER_LINEAR)
        hv = cv2.warpPerspective(have.astype(np.uint8) * 255, Mi, (W, H), flags=cv2.INTER_NEAREST)
        # colour match per hole on a ring around it (exposure drifts a little across the clip)
        n, lab = cv2.connectedComponents(hole)
        bgc = bgw.astype(np.float32)
        for c in range(1, n):
            h1 = (lab == c).astype(np.uint8) * 255
            ring = (cv2.dilate(h1, np.ones((61, 61), np.uint8)) > 0) & (h1 == 0) & (allm == 0) & (hv > 0)
            if ring.sum() > 200:
                g = (fr[ring].astype(np.float32).mean(0) + 1) / (bgw[ring].astype(np.float32).mean(0) + 1)
                sel = h1 > 0
                bgc[sel] = bgc[sel] * np.clip(g, .8, 1.25)
        fill = np.clip(bgc, 0, 255).astype(np.uint8)
        use = ((hole > 0) & (hv > 0)).astype(np.float32)
        al = cv2.GaussianBlur(use, (0, 0), 10)[..., None]
        al = np.clip(al * 2, 0, 1) * (cv2.dilate(hole, np.ones((41, 41), np.uint8)) > 0)[..., None]
        out = (fill * al + fr * (1 - al)).astype(np.uint8)
        # spots the plate never saw clean (always behind the athlete): copy a nearby patch of the same ground sideways
        miss = ((hole > 0) & (hv == 0) & (ms[si] == 0)).astype(np.uint8) * 255
        if miss.max():
            n2, lab2, st2, _ = cv2.connectedComponentsWithStats(miss, 8)
            avoid = cv2.dilate(((hole > 0) & (hv == 0)).astype(np.uint8) | (ms[si] > 0).astype(np.uint8), np.ones((15, 15), np.uint8))
            for c in range(1, n2):
                x, y, w, h, _ = st2[c]
                comp = (lab2 == c).astype(np.uint8) * 255
                grow = cv2.dilate(comp, np.ones((31, 31), np.uint8))
                for dx in sorted(range(-400, 401, 20), key=abs):
                    if dx == 0 or x + dx < 0 or x + w + dx + 15 >= W:
                        continue
                    sh = np.roll(grow, dx, axis=1)
                    if (avoid[sh > 0]).any():
                        continue
                    src = np.roll(out, -dx, axis=1)
                    al2 = cv2.GaussianBlur(grow.astype(np.float32) / 255, (0, 0), 6)[..., None]
                    al2 = np.maximum(al2, (comp > 0)[..., None].astype(np.float32))
                    out = (src * al2 + out * (1 - al2)).astype(np.uint8)
                    break
                else:
                    print(f"frame {i}: no patch for a {w}x{h} spot", flush=True)
    subj = cv2.GaussianBlur(cv2.dilate(ms[si], np.ones((7, 7), np.uint8)).astype(np.float32) / 255, (0, 0), 1.5)[..., None]
    out = (fr * subj + out * (1 - subj)).astype(np.uint8)
    cv2.imwrite(os.path.join(a.out, f"f{i:05d}.png"), out)
    print("out", i, flush=True)
print("done")
