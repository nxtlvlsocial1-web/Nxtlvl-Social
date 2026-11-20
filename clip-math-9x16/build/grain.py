"""Film-grain tile for the Clip Math reel.

python3 build/grain.py      (from the project root; needs numpy)
Writes assets/img/grain.png: a 256x256 seeded noise tile (grey, alpha) that index.html tiles and jitters.
"""
import os
import struct
import zlib

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "grain.png")


def png(path, rgba):
    h, w, _ = rgba.shape
    raw = b"".join(b"\x00" + rgba[y].tobytes() for y in range(h))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def main():
    rng = np.random.default_rng(20261120)
    n = rng.normal(0.5, 0.22, (256, 256)).clip(0, 1)
    g = (n * 255).astype(np.uint8)
    a = (np.abs(n - 0.5) * 2 * 255).clip(0, 255).astype(np.uint8)
    rgba = np.dstack([g, g, g, a])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    png(OUT, rgba)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
