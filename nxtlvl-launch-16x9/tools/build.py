"""Nxtlvl Social launch film v2 (16:9, 32 s): writes index.html and mixes the voice and the ducked music bed.

Voice lines (work/v2/*.wav, local Kokoro TTS) are placed on the film clock in LINES; every spoken line also appears
on screen as type, so there is no separate caption track. Transitions live in compositions/fx.html, the film-slate
frame in compositions/hud.html.
Run:  python3 tools/build.py && npx hyperframes check
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DUR = 32.0

LINES = [  # id, start on the film clock
    ('l1', 0.20), ('l2', 1.45),             # Stop posting. / Start getting seen.
    ('l3', 4.20),                           # This is Next Level Social.
    ('l4', 6.45),                           # Your entire creative team, in one studio.
    ('l5', 9.70),                           # Social media design. From five dollars a month.
    ('l6', 13.00),                          # Reel editing. From fifteen dollars.
    ('l7', 15.40),                          # Automation that replies while you sleep. From forty nine dollars.
    ('l8', 19.55),                          # And websites that turn views into clients.
    ('l10', 22.25),                         # Your brand. Next level.
    ('l9', 24.40),                          # No contracts. Cancel any month.
    ('l11', 27.00),                         # Book a free call at nxtlvlsocial.ai
]

SCENES = [  # id, start, duration, z
    ('s1-hook', 0, 4.0, 2),
    ('s2-logo', 4.0, 2.3, 2),
    ('s3-team', 6.3, 3.2, 2),
    ('s4-design', 9.5, 3.45, 2),
    ('s5-reels', 12.8, 2.65, 3),
    ('s6-automation', 15.25, 4.2, 4),
    ('s7-websites', 19.4, 2.6, 2),
    ('s8-impact', 22.0, 2.35, 2),
    ('s9-end', 24.2, DUR - 24.2, 3),
    ('fx', 0, DUR, 20),
    ('hud', 0, DUR, 30),
]

SFX = [  # file, start, volume
    ('impact-bass-1.mp3', 0.0, .32), ('pop.mp3', 0.62, .2), ('whoosh-short.mp3', 1.42, .24), ('impact-bass-2.mp3', 1.45, .26),
    ('pop.mp3', 1.85, .18), ('whoosh-cinematic.mp3', 2.58, .22),
    ('whoosh-cinematic.mp3', 3.7, .3), ('impact-bass-2.mp3', 4.0, .42), ('sparkle.mp3', 4.4, .26),
    ('whoosh-short.mp3', 6.0, .3), ('click-soft.mp3', 6.57, .26), ('click-soft.mp3', 7.07, .26), ('pop.mp3', 7.75, .2),
    ('whoosh-short.mp3', 9.2, .26), ('whoosh-short.mp3', 9.5, .2), ('pop.mp3', 9.9, .18), ('pop.mp3', 10.4, .18),
    ('impact-bass-1.mp3', 11.05, .3), ('sparkle.mp3', 11.15, .2),
    ('whoosh-cinematic.mp3', 12.72, .3), ('click-soft.mp3', 13.5, .3), ('click-soft.mp3', 14.0, .3), ('click-soft.mp3', 14.5, .3),
    ('impact-bass-1.mp3', 13.95, .26),
    ('whoosh-short.mp3', 15.22, .28), ('notification.mp3', 15.9, .2), ('pop.mp3', 16.9, .22), ('impact-bass-1.mp3', 18.15, .3),
    ('whoosh-cinematic.mp3', 19.12, .28), ('click-soft.mp3', 21.29, .34), ('chime.mp3', 21.45, .2),
    ('impact-bass-2.mp3', 22.0, .44), ('whoosh-short.mp3', 22.95, .2), ('sparkle.mp3', 23.5, .24),
    ('whoosh-cinematic.mp3', 23.95, .26), ('sparkle.mp3', 24.35, .2), ('pop.mp3', 25.1, .18), ('pop.mp3', 25.22, .18),
    ('pop.mp3', 25.34, .18), ('pop.mp3', 25.46, .18), ('pop.mp3', 26.8, .2), ('click-soft.mp3', 27.48, .36),
]


def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))


def mix_audio():
    work = os.path.join(ROOT, 'work', 'v2')
    ins, fc, mix = [], '', ''
    for i, (lid, t) in enumerate(LINES):
        ins += ['-i', os.path.join(work, f'{lid}.wav')]
        ms = int(t * 1000)
        fc += f'[{i}:a]adelay={ms}|{ms},apad=whole_dur={DUR}[a{i}];'
        mix += f'[a{i}]'
    chain = ('highpass=f=70,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=3500:t=q:w=1:g=2,'
             'acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2')
    pre = os.path.join(work, 'vo-pre.wav')
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', *ins, '-filter_complex',
                    f'{fc}{mix}amix=inputs={len(LINES)}:normalize=0,{chain},atrim=0:{DUR},aformat=channel_layouts=mono[v]',
                    '-map', '[v]', '-ar', '48000', pre], check=True)
    vo = os.path.join(ROOT, 'assets', 'voice', 'vo.wav')
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', pre, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7',
                    '-ar', '48000', vo], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', os.path.join(ROOT, 'assets', 'music', 'nxtlvl-brand.wav'),
                    '-i', vo, '-filter_complex',
                    f'[0:a]atrim=0:{DUR},afade=t=out:st={DUR - 1.6}:d=1.6[m];[1:a]aformat=channel_layouts=stereo[sc];'
                    '[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[d]',
                    '-map', '[d]', '-ar', '48000', os.path.join(ROOT, 'assets', 'music', 'bed-ducked.wav')], check=True)


def index():
    hosts = []
    for i, (sid, start, d, z) in enumerate(SCENES):
        kind = 'graphics'
        hosts.append(f'<div id="el-{sid}" class="scene clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{d:.2f}" data-track-index="{i + 1}" data-track-kind="{kind}" style="z-index:{z}"></div>')
    audio = [f'<audio id="el-vo" src="assets/voice/vo.wav" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="40"></audio>',
             f'<audio id="el-bgm" src="assets/music/bed-ducked.wav" data-start="0" data-duration="{DUR}" data-volume="0.4" data-track-index="41"></audio>']
    for i, (f, t, v) in enumerate(SFX):
        d = min(dur(os.path.join(ROOT, 'assets', 'sfx', f)), DUR - t)
        audio.append(f'<audio id="el-sfx-{i}" src="assets/sfx/{f}" data-start="{t}" data-duration="{d:.2f}" data-volume="{v}" data-track-index="{50 + i}"></audio>')
    nl = '\n      '
    return f'''<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #05030C; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #05030C; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      {nl.join(hosts)}
      {nl.join(audio)}
    </div>
    <script>
      var tl = gsap.timeline({{ paused: true }});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''


def main():
    mix_audio()
    with open(os.path.join(ROOT, 'index.html'), 'w') as f:
        f.write(index())
    print('wrote index.html, assets/voice/vo.wav, assets/music/bed-ducked.wav')


if __name__ == '__main__':
    main()
