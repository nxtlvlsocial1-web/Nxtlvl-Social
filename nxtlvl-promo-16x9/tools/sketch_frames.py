"""Sketch pass: write each storyboard frame as a static, posed sub-composition (no motion yet).

Shared pieces (the phone, the posts, the ground) come from assets/css/kit.css and the helpers below,
so every frame draws them identically. Run: python3 tools/sketch_frames.py
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'compositions', 'frames')
os.makedirs(OUT, exist_ok=True)

# every post design in the kit, with its caption and corner tag
POSTS = {
    'latte': ('Monday<br/>Mocha', 'reel'), 'diwali': ('Happy Diwali', ''), 'menu': ('NEW<br/>MENU', ''),
    'salon': ('5 looks<br/>for fall', 'multi'), 'gym': ('Summer<br/>shred', 'reel'), 'offer': ('20% OFF<small>this weekend</small>', ''),
    'bake': ('Fresh<br/>at 7am', ''), 'drop': ('NEW<br/>DROP', 'multi'), 'review': ('Best coffee<br/>in town', ''),
    'thali': ('Thali<br/>Tuesday', 'reel'), 'navratri': ('Navratri<br/>nights', ''), 'hours': ('Open<br/>till 10', ''),
}


def post(kind, pid):
    cap, tag = POSTS[kind]
    t = f'<i class="nx-tag {tag}"></i>' if tag else ''
    return f'<div class="nx-post nx-p-{kind}" id="{pid}">{t}<div class="nx-cap">{cap}</div></div>'


def phone(pfx, handle, name, bio, posts, followers, following, tiles=None, empty=False, feed_y=0, toast=None, x=770, y=80, scale=1.0):
    """The phone, posed. `tiles` is a list of post kinds or None for an empty slot."""
    grid = ''
    if empty:
        body = ('<div class="nx-empty"><div class="nx-cam"></div><h4>No posts yet</h4>'
                '<p>When you share photos, they will appear here.</p></div>')
    else:
        cells = []
        for i, k in enumerate(tiles or []):
            cells.append(post(k, f'{pfx}-t{i + 1}') if k else '<div class="nx-empty-tile"></div>')
        body = f'<div class="nx-grid" id="{pfx}-grid">{"".join(cells)}</div>'
    tst = ''
    if toast:
        tst = (f'<div class="nx-toast" id="{pfx}-toast" style="top:{toast[2]}px"><i class="nx-ok"></i>{toast[0]}'
               f'<small>{toast[1]}</small></div>')
    sig = ''.join(f'<i style="height:{h}px"></i>' for h in (4, 6, 8, 10))
    return f'''<div class="nx-phone" id="{pfx}-phone" style="left:{x}px; top:{y}px; transform:scale({scale}); transform-origin:0 0">
  <div class="nx-screen">
    <div class="nx-island"></div>
    <div class="nx-status"><span>9:41</span><span class="nx-sig">{sig}<b class="nx-bat"></b></span></div>
    <div class="nx-feed" id="{pfx}-feed" style="top:{52 - feed_y}px">
      <div class="nx-prof">
        <div class="nx-handle">{handle}<i class="nx-chev"></i></div>
        <div class="nx-row"><div class="nx-ava"><b></b></div>
          <div class="nx-stats"><div><b id="{pfx}-count">{posts}</b><span>posts</span></div><div><b>{followers}</b><span>followers</span></div><div><b>{following}</b><span>following</span></div></div></div>
        <div class="nx-name">{name}</div><div class="nx-bio">{bio}</div>
        <div class="nx-btns"><span>Edit profile</span><span>Share profile</span></div>
      </div>
      <div class="nx-tabs"><i class="on"></i><i></i><i></i></div>
      {body}
    </div>
    {tst}
  </div>
</div>'''


CAFE = dict(handle='the.corner.cafe', name='The Corner Café', bio='Coffee · brunch · open 7–10', followers='412', following='180')


def frame(fid, duration, inner, css=''):
    return f'''<template>
  <link rel="stylesheet" href="assets/css/kit.css" />
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    #{fid}-bg {{ position: absolute; inset: 0; }}
{css}
  </style>
  <script src="assets/vendor/gsap.min.js"></script>
  <div id="root" data-composition-id="{fid}" data-width="1920" data-height="1080" data-duration="{duration}">
    <div id="{fid}-bg" class="clip nx-ground" data-start="0" data-duration="{duration}" data-track-index="0">
      <i class="nx-glow a"></i><i class="nx-glow b"></i><i class="nx-glow c"></i><i class="nx-ribbon"></i><i class="nx-stars"></i>
    </div>
    <div id="{fid}-stage" class="clip" data-start="0" data-duration="{duration}" data-track-index="1" style="position:absolute; inset:0">
{inner}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["{fid}"] = tl;
  </script>
</template>
'''


def write(fid, duration, inner, css=''):
    with open(os.path.join(OUT, f'{fid}.html'), 'w') as f:
        f.write(frame(fid, duration, inner, css))


FILLED9 = ['latte', 'diwali', 'menu', 'salon', 'offer', 'review', 'thali', 'navratri', 'hours']

# ---------------------------------------------------------------- 01 · Still 0 posts?
write('01-zero-posts', 4, f'''
      <div class="nx-display" id="f1-still" style="position:absolute; right:1200px; top:372px; font-size:132px; text-align:right">Still</div>
      {phone('f1', posts='0', empty=True, **CAFE)}
      <div class="nx-display" id="f1-zero" style="position:absolute; left:1200px; top:372px; font-size:132px; white-space:nowrap"><span style="color:var(--nx-lift); text-shadow:0 0 60px rgba(169,92,255,.7)">0</span> posts?</div>
      <div class="nx-serif" id="f1-busy" style="position:absolute; left:1204px; top:530px; font-size:58px; line-height:1.02; width:600px">You're busy running the place.</div>
''')

# ---------------------------------------------------------------- 02 · Meet your entire creative team
write('02-meet-the-team', 6, f'''
      <div class="nx-display" id="f2-meet" style="position:absolute; right:1200px; top:300px; font-size:112px; text-align:right; white-space:nowrap">Meet your<br/>entire</div>
      {phone('f2', posts='9', tiles=FILLED9 + [None, None, None], **CAFE)}
      <div class="nx-serif" id="f2-team" style="position:absolute; left:1200px; top:286px; font-size:150px; line-height:.9; white-space:nowrap">creative<br/>team.</div>
      <div id="f2-pills" style="position:absolute; right:1200px; top:560px; width:600px; display:flex; flex-wrap:wrap; gap:12px; justify-content:flex-end">
        <span class="nx-pill"><i class="nx-dot"></i>Design</span><span class="nx-pill"><i class="nx-dot"></i>Video</span>
        <span class="nx-pill"><i class="nx-dot"></i>Posting</span><span class="nx-pill"><i class="nx-dot"></i>Automation</span>
      </div>
      <div id="f2-by" style="position:absolute; left:1206px; top:600px; display:flex; align-items:center; gap:14px">
        <span class="nx-body" style="font-size:26px">by</span>
        <img src="assets/nxtlvl-wordmark.png" alt="nxtlvl" style="width:190px; height:auto" />
        <svg viewBox="0 0 24 24" style="width:22px; height:22px; margin:-26px 0 0 -8px"><path d="M12 0c.5 6.4 5.1 11 11.5 11.5C17.1 12 12.5 16.6 12 23c-.5-6.4-5.1-11-11.5-11.5C6.9 11 11.5 6.4 12 0z" fill="#A95CFF"/></svg>
      </div>
''')

# ---------------------------------------------------------------- 03 · What lands in your feed (key moment: "the posters.")
FEED15 = FILLED9 + ['gym', 'drop', 'bake', 'latte', 'diwali', 'salon']   # frame 2's nine, then slots 10-15
write('03-what-lands', 8, f'''
      <div class="nx-display" id="f3-make" style="position:absolute; right:1200px; top:388px; font-size:120px; text-align:right; white-space:nowrap">We make</div>
      {phone('f3', posts='15', tiles=FEED15, feed_y=170, toast=('Posted · Diwali poster', 'Tue 6 PM', 640), **CAFE)}
      <div class="nx-serif" id="f3-word" style="position:absolute; left:1200px; top:374px; font-size:132px; line-height:.92; width:660px">the posters.</div>
''')

# ---------------------------------------------------------------- 04 · For every kind of business (key moment: the full wall)
WALL = [
    ('glow.salon', 'Glow Salon', 'Hair · nails · bridal', ['salon', 'drop', 'offer', 'navratri', 'review', 'hours'], 'Salon'),
    ('ironworks.gym', 'Ironworks Gym', 'Strength · HIIT · 5am–11pm', ['gym', 'offer', 'hours', 'review', 'gym', 'drop'], 'Gym'),
    ('maya.boutique', 'Maya Boutique', 'Ethnic & fusion wear', ['drop', 'navratri', 'salon', 'diwali', 'offer', 'review'], 'Boutique'),
    ('the.corner.cafe', 'The Corner Café', 'Coffee · brunch · open 7–10', None, 'Café'),   # continues frame 3's phone
    ('rise.bakery', 'Rise Bakery', 'Sourdough from 7am', ['bake', 'menu', 'diwali', 'latte', 'hours', 'review'], 'Bakery'),
    ('smile.dental', 'Smile Dental', 'Family dentistry', ['review', 'hours', 'offer', 'menu', 'drop', 'bake'], 'Clinic'),
    ('flow.studio', 'Flow Yoga Studio', 'Classes daily · all levels', ['navratri', 'hours', 'review', 'gym', 'salon', 'drop'], 'Studio'),
]
S = 0.6
W, Hh, GAP = 380 * S, 780 * S, 22
x0 = (1920 - (7 * W + 6 * GAP)) / 2
wall = []
for i, (h, n, b, tiles, label) in enumerate(WALL):
    x = x0 + i * (W + GAP)
    if tiles is None:   # the café phone: frame 3's end state (15 posts, scrolled 170 px), at wall scale
        wall.append(phone(f'f4p{i + 1}', posts='15', tiles=FEED15, feed_y=170, x=round(x, 1), y=96, scale=S, **CAFE))
    else:
        wall.append(phone(f'f4p{i + 1}', h, n, b, str(9 + i * 3), str(300 + i * 137), str(120 + i * 11), tiles=tiles + tiles[:3], x=round(x, 1), y=96, scale=S))
    wall.append(f'<span class="nx-pill" id="f4-l{i + 1}" style="position:absolute; left:{round(x + W / 2, 1)}px; top:{96 + Hh + 18}px; transform:translateX(-50%)"><i class="nx-dot"></i>{label}</span>')
write('04-every-business', 6, '\n'.join('      ' + w for w in wall) + '''
      <div id="f4-head" style="position:absolute; left:0; right:0; top:700px; text-align:center">
        <div class="nx-display" style="font-size:76px">Built for the businesses</div>
        <div class="nx-serif" style="font-size:96px; line-height:1; margin-top:6px">agencies won't call back.</div>
      </div>
''')

# ---------------------------------------------------------------- 05 · From $5 a month
blur_wall = '\n'.join(phone(f'f5p{i + 1}', h, n, b, '0', '0', '0', tiles=(t or FILLED9[:6]) + (t or FILLED9)[:3], x=round(x0 + i * (W + GAP), 1), y=96, scale=S)
                      for i, (h, n, b, t, _l) in enumerate(WALL))
write('05-five-dollars', 3, f'''
      <div id="f5-wall" style="position:absolute; inset:0; filter:blur(16px) saturate(1.1); opacity:.32">{blur_wall}</div>
      <div id="f5-veil" style="position:absolute; inset:0; background:radial-gradient(60% 55% at 50% 48%, rgba(5,3,12,.35), rgba(5,3,12,.92))"></div>
      <div class="nx-display" id="f5-team" style="position:absolute; left:0; right:0; top:178px; text-align:center; font-size:60px; color:var(--nx-muted)">Your entire creative team,</div>
      <div id="f5-price" style="position:absolute; left:0; right:0; top:260px; display:flex; justify-content:center; align-items:baseline; gap:30px">
        <span class="nx-serif" style="font-size:120px; color:var(--nx-fg)">from</span>
        <span class="nx-display" id="f5-five" style="font-size:380px; line-height:.9; font-variation-settings:'wdth' 118,'wght' 900; background:linear-gradient(180deg,#FFFFFF 10%,#D8BBFF 45%,#A95CFF 100%); -webkit-background-clip:text; background-clip:text; color:transparent; filter:drop-shadow(0 0 60px rgba(125,24,252,.75))">$5</span>
        <span class="nx-serif" style="font-size:120px; color:var(--nx-fg)">a month.</span>
      </div>
      <div id="f5-terms" style="position:absolute; left:0; right:0; top:760px; display:flex; justify-content:center; gap:14px">
        <span class="nx-pill">No contracts</span><span class="nx-pill">Cancel any month</span><span class="nx-pill">You own every file</span>
      </div>
''')

# ---------------------------------------------------------------- 06 · Book a free call
rings = ''.join(f'<i style="position:absolute; left:50%; top:50%; width:{d}px; height:{d}px; margin:-{d // 2}px 0 0 -{d // 2}px; border-radius:50%; border:1px solid rgba(169,124,255,{a})"></i>'
                for d, a in ((420, .32), (640, .22), (880, .14), (1160, .08)))
write('06-book-a-call', 3, f'''
      <div id="f6-rings" style="position:absolute; left:960px; top:400px; width:0; height:0">{rings}</div>
      <div id="f6-lock" style="position:absolute; left:0; right:0; top:300px; display:flex; justify-content:center">
        <div style="position:relative">
          <img src="assets/nxtlvl-wordmark.png" alt="nxtlvl" style="width:620px; height:auto; display:block" />
          <svg id="f6-spark" viewBox="0 0 24 24" style="position:absolute; right:-70px; top:-40px; width:72px; height:72px; filter:drop-shadow(0 0 22px rgba(169,92,255,.95))"><path d="M12 0c.5 6.4 5.1 11 11.5 11.5C17.1 12 12.5 16.6 12 23c-.5-6.4-5.1-11-11.5-11.5C6.9 11 11.5 6.4 12 0z" fill="#A95CFF"/></svg>
        </div>
      </div>
      <div id="f6-cta" style="position:absolute; left:0; right:0; top:560px; display:flex; justify-content:center">
        <span style="display:inline-flex; align-items:center; gap:18px; padding:24px 28px 24px 44px; border-radius:100px; background:var(--nx-violet); color:#fff; font-family:'Instrument Sans',sans-serif; font-weight:600; font-size:44px; box-shadow:0 30px 80px -20px rgba(125,24,252,.9)">Book a free call
          <b style="display:grid; place-items:center; width:58px; height:58px; border-radius:50%; background:rgba(255,255,255,.18)"><svg viewBox="0 0 24 24" style="width:30px; height:30px" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M9 7h8v8"/></svg></b>
        </span>
      </div>
''')
print('wrote', sorted(os.listdir(OUT)))
