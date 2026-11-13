"""v3 (client: "the reference videos must be in full screen more"): full-screen 1080x1920 versions of the reference
clips. Landscape Pexels clips are cropped from their 4K file where Pexels has one (footage/broll_uhd, fetched from
videos.pexels.com like tools/pexels_fetch.py), else from the HD file; the crop is centred on the people (FOCUS, the
horizontal position 0..1). Vertical clips are only scaled/cropped to 1080x1920. The two podcast clips get full-screen
cuts the same way as assets/video/pod_full.mp4 (crop of the screen recording around Deepinder, graded later in CSS).
Writes footage/broll_v/<id>.mp4 and assets/video/pod_cF.mp4, pod_dF.mp4.
python3 build/broll_vertical.py
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "footage", "broll_v")
FOCUS = {"8632780": .48, "6639660": .66, "4763892": .5, "8165946": .55, "9782812": .5, "8557555": .22, "7640672": .5,
         "5658237": .33, "8888536": .5, "8058107": .3, "8416831": .5, "9579386": .45, "8773862": .55, "7223986": .5, "5899973": .45,
         # v4: Indian people throughout (client)
         "7164569": .4, "8811044": .62, "4584772": .5, "4334053": .27, "8187787": .45, "5034858": .4, "6956640": .5}
ENC = ["-an", "-r", "30", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p"]


def main():
    os.makedirs(OUT, exist_ok=True)
    for vid, fx in FOCUS.items():
        uhd = os.path.join(ROOT, "footage", "broll_uhd", f"{vid}.mp4")
        src = uhd if os.path.exists(uhd) else os.path.join(ROOT, "footage", "broll", f"{vid}.mp4")
        dst = os.path.join(OUT, f"{vid}.mp4")
        if os.path.exists(dst) and os.path.getsize(dst) > 100000:
            continue
        vf = (f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920:(iw-1080)*{fx}:(ih-1920)/2,"
              f"unsharp=5:5:0.35:5:5:0.0")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", vf, *ENC, dst], check=True)
        print(vid, "from", "4K" if src == uhd else "HD")
    pv = "unsharp=5:5:0.4:5:5:0.0,format=yuv420p"
    for name, ss, d, x in (("pod_cF", 29.0, 4.5, 1190), ("pod_dF", 33.8, 3.7, 1320)):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ss), "-t", str(d), "-i", os.path.join(ROOT, "footage", "podcast_rec.mp4"),
                        "-vf", f"crop=741:1318:{x}:1,scale=1080:1920:flags=lanczos,{pv}", *ENC[:-2],
                        os.path.join(ROOT, "assets", "video", f"{name}.mp4")], check=True)
        print(name)


if __name__ == "__main__":
    main()
