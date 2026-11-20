"""Jump-cut the take and clean the voice.

Reads assets/video/footage.mp4 (the original take, dense keyframes) and transcript.json (source word times).
Writes:
  assets/video/aroll.mp4    the cut: every pause between sentences removed, frame-accurate, 12 ms audio fades at each
                            cut, voice cleaned (high-pass, light de-noise, de-mud and presence EQ, compression,
                            two-pass loudness normalisation to -16 LUFS / -1.5 dBTP)
  transcript-cut.json       the words retimed to the cut, plus the segment list (each cut's film time)
Run from the project folder:  python3 tools/cut.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'assets/video/footage.mp4')
OUT = os.path.join(ROOT, 'assets/video/aroll.mp4')
FPS = 30

# Sentence segments in source seconds: ~80 ms before the first word and after the last, so no word is clipped.
SEGMENTS = [
    (1.30, 5.12),    # We took @ai.nxtlvl from zero to 7,100 followers with just 22 posts.
    (5.46, 7.74),    # Not luck, a system, and here's what's inside it.
    (8.10, 10.24),   # Designs that are made to be saved, not scrolled past.
    (10.56, 12.50),  # A content calendar planned a month ahead.
    (12.60, 15.20),  # Reels edited and posted every single week for you.
    (15.42, 17.88),  # Most agencies charge 25,000 for this,
    (18.02, 19.60),  # but we start at 999.
    (19.74, 20.96),  # Want this for your own brand?
    (21.10, 24.94),  # Reach out to us and tap Send Message.  (+ the quiet tail under the end card)
]


def frame(t):
    return round(t * FPS) / FPS


def main():
    segs = [(frame(a), frame(b)) for a, b in SEGMENTS]
    parts, labels, starts, t = [], [], [], 0.0
    for i, (a, b) in enumerate(segs):
        d = b - a
        parts.append(f'[0:v]trim=start={a:.4f}:end={b:.4f},setpts=PTS-STARTPTS[v{i}]')
        parts.append(f'[0:a]atrim=start={a:.4f}:end={b:.4f},asetpts=PTS-STARTPTS,'
                     f'afade=t=in:d=0.012,afade=t=out:st={d - 0.012:.4f}:d=0.012[a{i}]')
        labels.append(f'[v{i}][a{i}]')
        starts.append((round(t, 4), a, b))
        t += d
    voice = ('highpass=f=80,afftdn=nr=8:nf=-50,'
             'equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=7500:t=q:w=2:g=-1.5,'
             'acompressor=threshold=-22dB:ratio=3.5:attack=6:release=120:makeup=3:knee=4')
    graph = ';'.join(parts) + f';{"".join(labels)}concat=n={len(segs)}:v=1:a=1[vc][ac];[ac]{voice}[av]'

    # pass 1: measure the processed voice for loudnorm
    m = subprocess.run(['ffmpeg', '-hide_banner', '-i', SRC, '-filter_complex',
                        graph + ';[vc]nullsink;[av]loudnorm=I=-16:TP=-1.5:LRA=5:print_format=json[an]',
                        '-map', '[an]', '-f', 'null', '-'], capture_output=True, text=True)
    found = re.search(r'\{[^{}]*"input_i"[^{}]*\}', m.stderr)
    if not found:
        raise SystemExit('loudness pass failed:\n' + m.stderr[-1500:])
    stats = json.loads(found.group(0))
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=5:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
          f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true")
    # pass 2: write the cut
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-filter_complex', graph + f';[av]{ln},aresample=48000[an]',
                    '-map', '[vc]', '-map', '[an]', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-g', '30',
                    '-keyint_min', '30', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k',
                    '-movflags', '+faststart', OUT], check=True)

    # retime the words onto the cut
    words = json.load(open(os.path.join(ROOT, 'transcript.json')))
    out = []
    for w in words:
        for n, a, b in starts:
            if a - 0.001 <= w['start'] < b:
                out.append({'text': w['text'], 'start': round(n + w['start'] - a, 3), 'end': round(n + min(w['end'], b) - a, 3)})
                break
    total = round(t, 4)
    json.dump({'duration': total, 'segments': [{'film': n, 'src_start': a, 'src_end': b} for n, a, b in starts],
               'words': out}, open(os.path.join(ROOT, 'transcript-cut.json'), 'w'), indent=1)
    print(f'cut: {len(segs)} segments, {total:.2f} s (was {24.97 - 1.2:.2f} s after the silent start); '
          f'{len(out)}/{len(words)} words kept; voice measured at {stats["input_i"]} LUFS before normalising')


if __name__ == '__main__':
    main()
