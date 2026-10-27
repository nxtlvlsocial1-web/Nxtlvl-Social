"""Write the <audio> clips from audio_meta.json into index.html between the AUDIO markers.
Run after tools/sound_cues.py: python3 tools/assemble_audio.py
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
meta = json.load(open(os.path.join(ROOT, 'audio_meta.json')))
ROOT_DUR = 32.0

lines = ['      <!-- AUDIO:START (written by tools/assemble_audio.py from audio_meta.json) -->']
b = meta['bgm']
lines.append(f'      <audio id="el-bgm" src="{b["path"]}" data-start="0" data-duration="{b["duration_s"]}" data-track-index="11" data-volume="{b["volume"]}"></audio>')
for i, s in enumerate(meta['sfx']):
    dur = min(s['duration_s'], ROOT_DUR - s['start_s'])
    if dur <= 0.05:
        continue
    lines.append(f'      <audio id="el-sfx-{i}" src="{s["file"]}" data-start="{s["start_s"]}" data-duration="{round(dur, 3)}" data-track-index="{20 + i}" data-volume="{s["volume"]}"></audio>')
lines.append('      <!-- AUDIO:END -->')

p = os.path.join(ROOT, 'index.html')
html = open(p).read()
html = re.sub(r'      <!-- AUDIO:START.*?<!-- AUDIO:END -->', '\n'.join(lines), html, flags=re.S)
open(p, 'w').write(html)
print(f'{len(lines) - 2} audio clips written into index.html')
