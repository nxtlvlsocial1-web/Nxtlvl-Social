"""Creators 100X x Creedom "Messages to My Past Self" (9:16): writes index.html, plan/sfx_events.json and plan/edit.json
from plan/msgs.json and plan/words.json (build/vo_pick.py).

Script approved by the owner on 2026-11-19, two voices (ElevenLabs built-ins: present-her Jessica, past-her Sarah).
A phone chat at 2 a.m. between a creator and herself six months ago: pink bubbles (present, "Today") on the right, grey
bubbles (past, "Mar 14, 2:14 AM") on the left, typing dots before every reply, the header showing "typing…". Low point: a
47-views screenshot, "I think I'm done.", a "Delete account?" pop-up and one beat of silence. The turn ("Stop
guessing"): the pop-up drops away, the room and the screen warm from cool blue to Creedom pink, a Creedom account read
is sent (labelled EXAMPLE), Cree arrives as a sticker (his real 3D poses), "Ready to post" is sent, past-her decides not
to delete, a heart reaction, the header turns "online". CTA: the last bubble, "Seen", and the Comment GROW bar.
Claims stay within what Creedom does (reads the account, shows what's working / what's killing views, checks before posting).
python3 build/generate.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, JS, SFX, ROOT, punch  # noqa: E402

random.seed(21)
MSGS = {m["id"]: m for m in json.load(open(os.path.join(ROOT, "plan", "msgs.json")))}
ORDER = [m["id"] for m in json.load(open(os.path.join(ROOT, "plan", "msgs.json")))]
DUR = round(MSGS["m10"]["t1"] + 1.4, 2)
TIME = {"P": "Today 9:41 PM", "Q": "Mar 14, 2:14 AM"}
POSES = json.load(open(os.path.join(ROOT, "plan", "poses.json")))

# ---- layout: estimate every bubble's size, stack the chat, scroll so the newest item sits on the anchor line ----------
CH = 24.2                     # average px per character at 46 px Inter 500
MAXW = 680


def wrap(text):
    lines, cur = [], ""
    for w in text.split():
        nxt = (cur + " " + w).strip()
        if len(nxt) * CH > MAXW - 72 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = nxt
    lines.append(cur)
    return lines


def bubble_h(text):
    ls = wrap(text)
    return 56 + len(ls) * 59 + 38, min(MAXW, max(len(l) for l in ls) * CH + 72)


ANCHOR = 1140                 # view-local y the newest item's bottom scrolls to (screen y = 360 + local)
ITEMS = []                    # (id, kind, side, y, h, t_show)
CHAT, OVER = [], []
y = 400                       # the chat starts low, like a fresh conversation near the keyboard
prev_side = None


def place(h, side):
    global y, prev_side
    if prev_side and side != prev_side:
        y += 14
    top = y
    y += h + 20
    prev_side = side
    return top


HEART = ('<svg viewBox="0 0 24 24"><path d="M12 21 C5 15.5 2 12.4 2 8.6 C2 5.5 4.4 3.2 7.3 3.2 C9.2 3.2 10.9 4.2 12 5.8 C13.1 4.2 14.8 3.2 16.7 3.2 '
         'C19.6 3.2 22 5.5 22 8.6 C22 12.4 19 15.5 12 21 Z" fill="#ff5c9a"/></svg>')
DOWN = '<svg viewBox="0 0 24 24"><path d="M12 4v15M5 13l7 7 7-7" fill="none" stroke="#ff4d6d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
OKI = '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="#2fbf71"/><path d="M13 25 L21 33 L36 16" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BADI = '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="#e11d48"/><path d="M16 16 L32 32 M32 16 L16 32" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'

scroll_keys = []              # (t, offset)


def show_item(sel, t, side, top, h, pop=True):
    bottom = top + h
    if bottom > ANCHOR:
        scroll_keys.append((t, -(bottom - ANCHOR)))
    if pop:
        frm = "{opacity: 1, scale: .86, y: 16}" if t < .05 else "{opacity: 0, scale: .6, y: 30}"   # frame 0 already shows the hook
        ft(sel, t, .38, frm, "{opacity: 1, scale: 1, y: 0}", "back.out(1.8)")


def msg(mid, t_show):
    m = MSGS[mid]
    h, w = bubble_h(m["text"])
    top = place(h, m["who"])
    CHAT.append(f'<div class="msg {m["who"]}" id="b_{mid}" style="top:{top}px;width:{w:.0f}px">{m["text"]}<small>{TIME[m["who"]]}</small></div>')
    show_item(f"#b_{mid}", t_show, m["who"], top, h)
    sfx("send" if m["who"] == "P" else "recv", t_show)
    return top, h


def typing(mid_next, t0, t1):
    """typing dots where past-her's next bubble will land, and "typing…" in the header"""
    h, _ = bubble_h(MSGS[mid_next]["text"])
    top = y + (14 if prev_side != "Q" else 0)
    tid = f"ty_{mid_next}"
    CHAT.append(f'<div class="typing" id="{tid}" style="top:{top}px"><i></i><i></i><i></i></div>')
    if top + 92 > ANCHOR:
        scroll_keys.append((t0, -(top + 92 - ANCHOR)))
    ft(f"#{tid}", t0, .25, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2)")
    js(f'tl.fromTo("#{tid} i", {{y: 0}}, {{y: -12, duration: .16, yoyo: true, repeat: {max(1, int((t1 - t0) / .32)) * 2 - 1}, stagger: .08, ease: "sine.inOut", immediateRender: false}}, {t0:.3f});')
    st(f"#{tid}", t1, "{opacity: 0}")
    st("#hsub", t0, '{textContent: "typing…"}')
    st("#hsub", t1, '{textContent: "last seen Mar 14, 2:14 AM"}')
    n = int((t1 - t0) / .12)
    for k in range(0, n, 2):
        sfx("tick", t0 + .12 * k)


def attach(aid, side, html, h, t_show):
    top = place(h, side)
    CHAT.append(f'<div class="att {side}" id="{aid}" style="top:{top}px">{html}</div>')
    show_item(f"#{aid}", t_show, side, top, h)
    return top


# ---- the conversation -----------------------------------------------------------------------------------------------
M = MSGS
CHAT.append('<div class="day" style="top:340px">TODAY</div>')
t = M["m0"]["t0"] - .12
msg("m0", max(0.0, t))
sfx("buzz", 0)
typing("m1", M["m0"]["t1"] + .02, M["m1"]["t0"] - .08)
msg("m1", M["m1"]["t0"] - .08)
msg("m2", M["m2"]["t0"] - .1)
st("#hfuture", T("m2", "Six") - .05, "{opacity: 1}")
st("#hlast", T("m2", "Six") - .05, "{opacity: 0}")
st("#hfuture", M["m2"]["t1"] + .3, "{opacity: 0}")
st("#hlast", M["m2"]["t1"] + .3, "{opacity: 1}")
typing("m3", M["m2"]["t1"] + .02, M["m3"]["t0"] - .08)
msg("m3", M["m3"]["t0"] - .08)
SHOT = (f'<div class="shot"><i class="th"></i><div><small>YOUR REEL · 7 DAYS</small><b>47{DOWN}</b><span>views</span></div></div>')
attach("a_shot", "Q", SHOT, 300, M["m3"]["t0"] + .45)
sfx("pop", M["m3"]["t0"] + .45)
typing("m4", M["m3"]["t1"] + .02, M["m4"]["t0"] - .06)
msg("m4", M["m4"]["t0"] - .06)
# the delete pop-up and one beat of silence
t_mod = M["m4"]["t1"] + .08
ft("#dim", t_mod, .3, "{opacity: 0}", "{opacity: 1}", "power2.out")
ft("#modal", t_mod, .4, "{opacity: 0, scale: .8}", "{opacity: 1, scale: 1}", "back.out(1.6)")
sfx("error", t_mod)
js(f'tl.to("#cam", {{scale: 1.06, duration: {M["m5"]["t0"] - t_mod:.2f}, ease: "power1.inOut"}}, {t_mod:.3f});')
# the turn: "Don't delete it. Stop guessing."
t5 = M["m5"]["t0"]
msg("m5", t5 - .1)
t_sg = T("m5", "Stop")
to("#modal", t_sg - .05, .35, "{opacity: 0, scale: .6, y: 300, rotation: -8}", "power2.in")
to("#dim", t_sg, .35, "{opacity: 0}")
js(f'tl.to("#cam", {{scale: 1, duration: .6, ease: "power2.out"}}, {t_sg:.3f});')
sfx("whoosh_big", t_sg - .05)
punch(t_sg + .05, 1.03)
WARM0, WARM1 = t_sg, M["m9"]["t1"]
for sel, op in (("#warm", 1), ("#screenW", 1), ("#lamp3", 1), ("#glowP", 1)):
    js(f'tl.to("{sel}", {{opacity: {op}, duration: {WARM1 - WARM0:.2f}, ease: "power1.inOut"}}, {WARM0:.3f});')
js(f'tl.to("#phone", {{boxShadow: "0 0 0 14px #1c1a22, 0 0 0 16px #2e2b36, 0 60px 120px rgba(0,0,0,.6), 0 0 200px rgba(243,67,162,.35)", duration: {WARM1 - WARM0:.2f}}}, {WARM0:.3f});')
msg("m6", M["m6"]["t0"] - .1)
CREAD = ('<div class="cread"><div class="top"><img src="assets/img/creedom_logo.png" alt="Creedom"><span>ACCOUNT READ · EXAMPLE</span></div>'
         f'<div class="row ok">{OKI}<div><small>WORKING</small>Talking reels</div></div>'
         f'<div class="row bad">{BADI}<div><small>KILLING VIEWS</small>Slow first 3 seconds</div></div></div>')
t_cr = T("m6", "showed")
attach("a_cread", "P", CREAD, 360, t_cr - .1)
sfx("ding", t_cr - .05)
typing("m7", M["m6"]["t1"] + .02, M["m7"]["t0"] - .08)
msg("m7", M["m7"]["t0"] - .08)
# Cree arrives as a sticker (his own 3D poses), first the magnifier, then cheering
stk_top = attach("a_stk", "Q", '<div class="sticker" id="stk" style="position:relative;opacity:1">'
                 '<img id="stk_mag" src="assets/img/poses/mag.png" alt=""><img id="stk_cheer" src="assets/img/poses/cheer.png" alt="" style="opacity:0"></div>', 300,
                 M["m7"]["t0"] + .35)
st("#stk_mag", M["m7"]["t1"] + .15, "{opacity: 0}")
st("#stk_cheer", M["m7"]["t1"] + .15, "{opacity: 1}")
js(f'tl.fromTo("#stk", {{y: 0, scaleY: 1}}, {{keyframes: [{{scaleY: .88, y: 8, duration: .07}}, {{scaleY: 1.06, y: -40, duration: .14}}, {{scaleY: 1, y: 0, duration: .13}}], immediateRender: false}}, {M["m7"]["t1"] + .15:.3f});')
sfx("pop", M["m7"]["t0"] + .35)
sfx("pop", M["m7"]["t1"] + .15)
msg("m8", M["m8"]["t0"] - .1)
attach("a_ready", "P", f'<div class="ready">{OKI}Ready to post</div>', 130, T("m8", "checks"))
sfx("ding2", T("m8", "checks"))
typing("m9", M["m8"]["t1"] + .02, M["m9"]["t0"] - .08)
top9, h9 = msg("m9", M["m9"]["t0"] - .08)
CHAT.append(f'<div class="react" id="rx" style="left:{44 + bubble_h(M["m9"]["text"])[1] - 50:.0f}px;top:{top9 + h9 - 40}px">{HEART}</div>')
t_rx = M["m9"]["t1"] - .25
ft("#rx", t_rx, .35, "{opacity: 0, scale: 0}", "{opacity: 1, scale: 1}", "back.out(3)")
sfx("pop", t_rx)
st("#hsub", M["m9"]["t1"], '{textContent: "online"}')
js(f'tl.set("#hsub", {{color: "#ff8cc6"}}, {M["m9"]["t1"]:.3f});')
ft("#avW", M["m9"]["t1"], .5, "{opacity: 0}", "{opacity: 1}", "power2.out")
# CTA: last bubble, Seen, the Comment GROW bar
ANCHOR = 1140 - 230
top10, h10 = msg("m10", M["m10"]["t0"] - .1)
CHAT.append(f'<div class="seen" id="seen" style="top:{top10 + h10 + 4}px">Seen</div>')
ft("#seen", M["m10"]["t1"] + .1, .3, "{opacity: 0}", "{opacity: 1}")
t_cm = T("m10", "Comment")
ft("#cbr", t_cm + .2, .45, "{opacity: 0, y: 120}", "{opacity: 1, y: 0}", "back.out(1.7)")
t_ty = t_cm + .55
st("#cph", t_ty, "{opacity: 0}")
js(f'tl.fromTo("#cty i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .07, immediateRender: false}}, {t_ty:.3f});')
for k in range(4):
    sfx("click", t_ty + .07 * k)
to("#csend", t_ty + .35, .08, "{scale: .8}")
to("#csend", t_ty + .43, .22, "{scale: 1.12, backgroundColor: '#F343A2'}", "back.out(3)")
sfx("ding", T("m10", "secret"))

# scroll keys -> one smooth scroll per new item
last = 0
for tk, off in sorted(scroll_keys):
    if off < last:
        js(f'tl.to("#chat", {{y: {off}, duration: .4, ease: "power3.out"}}, {tk:.3f});')
        last = off

# handheld drift, slow push, room dots
js(f'tl.fromTo("#cam", {{rotation: -.35, x: -4}}, {{rotation: .35, x: 4, duration: 2.6, yoyo: true, repeat: {int(DUR / 2.6)}, ease: "sine.inOut", immediateRender: false}}, 0);')
js(f'tl.fromTo("#punch", {{scale: 1}}, {{scale: 1.04, duration: {DUR:.2f}, ease: "none", immediateRender: false}}, 0);')
dots = ""
for i in range(14):
    x, yy, s = random.randint(-40, 1080), random.randint(0, 1920), random.randint(30, 90)
    dots += f'<i class="dot" id="dt{i}" style="left:{x}px;top:{yy}px;width:{s}px;height:{s}px;opacity:{random.uniform(.2, .5):.2f}"></i>'
    js(f'tl.fromTo("#dt{i}", {{y: 0}}, {{y: {random.randint(-80, -30)}, duration: {random.uniform(4, 7):.2f}, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false}}, 0);')

CSS = open(os.path.join(ROOT, "build", "style.css")).read()
cty = "".join(f"<i>{c}</i>" for c in "GROW")
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: Messages to My Past Self 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="room" id="cool"></div><div class="room" id="warm"></div>
      <i class="lamp" id="lamp1"></i><i class="lamp" id="lamp2"></i><i class="lamp" id="lamp3"></i>{dots}
      <div id="punch"><div id="cam">
        <div id="phone" data-layout-allow-overlap><div id="screen"></div><div id="screenW"></div><div id="glowP"></div><i class="island"></i>
          <div class="hdr"><i class="back"></i><div class="av"><i></i><b></b><div id="avW"></div></div>
            <div class="hname"><b>me</b><span><em id="hfuture" style="opacity:0;position:absolute">from the future</em><span id="hlast" style="display:inline">
            <span id="hsub">last seen Mar 14, 2:14 AM</span></span></span></div></div>
          <div id="view"><div id="chat">{"".join(CHAT)}</div></div>
          <div class="inp">Message…<b class="send"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></b></div>
          <div id="dim"></div>
          <div id="modal"><h4>Delete account?</h4><p>All your reels, followers and drafts will be gone for good.</p><div class="btns"><span>Cancel</span><span>Delete</span></div></div>
        </div>
      </div></div>
      <div class="cbar" id="cbr"><i class="cav"></i><span class="cph" id="cph">Add a comment…</span><span class="cty" id="cty">{cty}</span>
        <b class="csend" id="csend"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></b></div>
      <div id="vig"></div><div id="grain"></div><div id="flash"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      tl.progress(1, true).progress(0, true);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "msgs": MSGS}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx, chat height {y}")
