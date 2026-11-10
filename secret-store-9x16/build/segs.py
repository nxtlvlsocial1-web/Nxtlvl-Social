"""Print the speech segments (pauses >= 90 ms) of each candidate take: helps pick takes and map phrases."""
import subprocess, sys, glob, os
import numpy as np
SR = 48000
for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "voice/el/cand/*.mp3")):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).astype(np.float64)
    hop = SR // 100; m = len(a) // hop
    env = 20 * np.log10(np.sqrt(np.mean(a[: m * hop].reshape(m, hop) ** 2, axis=1)) + 1e-9)
    on = env > max(-45, env.max() - 32)
    segs, k = [], 0
    while k < m:
        if on[k]:
            j = k
            while j < m and (on[j] or (j + 9 < m and on[j:j + 9].any())):
                j += 1
            segs.append((k / 100, j / 100)); k = j
        else:
            k += 1
    print(os.path.basename(f), f"{len(a)/SR:.2f}s", " | ".join(f"{s:.2f}-{e:.2f}" for s, e in segs), f"peak {env.max():.0f}dB")
