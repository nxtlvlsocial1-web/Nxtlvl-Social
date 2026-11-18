"""Creators 100X x Creedom "GROW" reel, style A "Classified" (9:16): writes index.html, plan/sfx_events.json and
plan/edit.json from plan/words.json (the owner's ElevenLabs take, word times from faster-whisper).

Script: the client's (Creedom paid collab, "The secret AI growing accounts"), voiced by the owner in ElevenLabs
(Blondie - Conversational). Visual beats follow the client's beat sheet, told as a top-secret case file:
  0 hook (dark desk, one spotlight): a pink case file slides in, TOP SECRET slams on "secret", the file opens on a
    blurred app with a views graph climbing; Cree pops up with his magnifier;
  1 "not ChatGPT": a generic chatbot window gets a red X and drops away; Cree shakes his head;
  2 reveal: a redaction bar wipes the frame, the codename bar peels off the Creedom wordmark on "Creedom", the lights
    come up (light pink world); "an Instagram coach that reads your account";
  3 the profile under the scan line: winners glow WORKING, one tile is flagged KILLING VIEWS (Cree shocked);
  4 before you post: thumb on Share, the phone freezes, "Weak hook" card flips to "Ready to post";
  5 what to post next (dark again, through an iris): three classified memos fan out, each tagged "your audience saved this";
  6 the crazy part: lights go down to one spotlight, then a before / after graph with an IT WORKED stamp;
  7 social proof (light): a 150,000+ counter, creator dots, "Meta Tech Partner" and "free first account read" pills;
  8 CTA (dark): Comment GROW, the DM "Here's the secret", the case file closes and TOP SECRET slams on "secret".
Transitions: redaction-bar wipe, classified-sheet slide, whip pan, spotlight iris.
python3 build/generate.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import T, js, sfx, ft, to, st, LINES, L0, L1, JS, SFX, HTML, ROOT, head, head_out, punch, scene, whip, snap  # noqa: E402
from fx import cree_html, cree_to, pose, cree_walk, cree_hop, cree_wiggle, blink, sweat, say, sparkle, P  # noqa: E402

random.seed(14)
INK = "#0B0B0B"
DUR = round(L1["g8"] + 2.0, 2)
K = ["g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8"]
S = {k: (0.0 if k == "g0" else snap(L0[k] - .1)) for k in K}
END = {k: (S[K[i + 1]] if i + 1 < len(K) else DUR) for i, k in enumerate(K)}
# Whisper runs "saved." into "And the crazy part?"; the take's real gap is 28.66-29.01 s (silencedetect),
# so cut at its start; plan/words.json carries the corrected times for "And" (g6) and "Comment GROW" (g8) from the level curve
S["g6"] = snap(28.7)
END = {k: (S[K[i + 1]] if i + 1 < len(K) else DUR) for i, k in enumerate(K)}
for a, b in zip(K, K[1:]):
    assert b == "g6" or (S[b] < L0[b] and S[b] > L1[a] - .05), (a, b, S[b])


# ---- headlines: every one is recorded with its line; any still on screen leaves at the end of its scene ----------------
HEADS, CLOSED = [], set()


def H(hid, rows, top, line, **kw):
    HEADS.append((hid, line))
    return head(hid, rows, top, line, **kw)


def HO(hid, t):
    CLOSED.add(hid)
    head_out(hid, t)


# ---- shared moves -------------------------------------------------------------------------------------------------------
def light(t, on, d=.3):
    to("#light", t, d, f"{{opacity: {1 if on else 0}}}", "power2.inOut")


def spot(t, x, y, s=1.0, d=.8, ease="power2.inOut"):
    """move the spotlight so its centre sits at (x, y)"""
    js(f'tl.to("#spot", {{x: {x - 540:.0f}, y: {y - 920:.0f}, scale: {s}, duration: {d}, ease: "{ease}"}}, {t:.3f});')


def shake(t, amp=16, n=6, per=.035):
    ks = ", ".join(f'{{x: {random.choice((-1, 1)) * amp * (1 - k / n):.1f}, y: {random.choice((-1, 1)) * amp * .7 * (1 - k / n):.1f}, duration: {per}}}' for k in range(n))
    js(f'tl.fromTo("#shake", {{x: 0, y: 0}}, {{keyframes: [{ks}, {{x: 0, y: 0, duration: {per}}}], immediateRender: false}}, {t:.3f});')


SPL = [0]


def stamp(sel, t, rot=-10, big=True, gn=False):
    """rubber stamp: drops from big and slams down, ink specks fly, the frame shakes"""
    ft(sel, t - .16, .16, f"{{opacity: 0, scale: 2.6, rotation: {rot - 8}}}", f"{{opacity: 1, scale: 1, rotation: {rot}}}", "power4.in")
    ft(sel, t, .22, "{scale: .94}", "{scale: 1}", "back.out(3)")
    shake(t, 20 if big else 10)
    sfx("stamp", t - .02)
    sfx("sub", t - .02)
    st("#flash", t, "{opacity: .5}")
    to("#flash", t + .01, .3, "{opacity: 0}", "power2.out")


def redact(t):
    """a black redaction bar (pink edge) sweeps across the frame and covers the cut"""
    ft("#redact", t - .3, .3, "{x: -2100}", "{x: 0}", "power3.in")
    to("#redact", t + .02, .34, "{x: 2100}", "power3.out")
    js(f'tl.fromTo("#redact", {{scaleY: .3}}, {{scaleY: 5.2, duration: .3, ease: "power3.in", immediateRender: false}}, {t - .3:.3f});')
    js(f'tl.to("#redact", {{scaleY: .3, duration: .34, ease: "power3.out"}}, {t + .02:.3f});')
    sfx("riser_short", t - .9)
    sfx("whoosh_big", t - .32)
    sfx("glitch", t - .02)


def sheet(t):
    """a classified sheet slides up over the frame and away"""
    ft("#sheet", t - .3, .3, "{y: 2400, rotation: 6}", "{y: 0, rotation: 0}", "power3.in")
    to("#sheet", t + .03, .36, "{y: -2500, rotation: -5}", "power3.in")
    sfx("riser_short", t - .9)
    sfx("flip", t - .28)
    sfx("whoosh", t - .05)
    sfx("paper", t + .05)


def iris(t):
    """the spotlight closes to a point and opens again on the next scene"""
    st("#iris", t - .32, "{opacity: 1}")
    ft("#iris", t - .32, .32, "{width: 2600, height: 2600, x: -1300, y: -1300}", "{width: 0, height: 0, x: 0, y: 0}", "power3.in")
    ft("#iris", t + .02, .38, "{width: 0, height: 0, x: 0, y: 0}", "{width: 2600, height: 2600, x: -1300, y: -1300}", "power3.out")
    st("#iris", t + .42, "{opacity: 0}")
    sfx("whoosh_big", t - .34)
    sfx("switch", t - .01)


def draw(sel, t, d, ease="power2.inOut"):
    ft(sel, t, d, "{strokeDashoffset: 1}", "{strokeDashoffset: 0}", ease)


def cree_pop(t, x, feet, s, name, flip=None):
    """Cree pops up into the frame from below"""
    cree_to(t - .02, *P(x, feet, s), d=.01)
    pose(t, name, flip=flip, squash=False)
    st("#cree", t, "{opacity: 1}")
    ft("#creeb", t, .5, "{y: 520}", "{y: 0}", "back.out(1.5)")
    sfx("pop", t + .1)


def cree_hide(t):
    st("#cree", t, "{opacity: 0}")


ARROW_UP = '<svg viewBox="0 0 24 24"><path d="M12 20V5M5 11l7-7 7 7" fill="none" stroke="#15a05a" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
WARN = ('<svg viewBox="0 0 48 48"><path d="M24 4 L46 42 H2 Z" fill="#F5B544" stroke="#8a4b00" stroke-width="3" stroke-linejoin="round"/>'
        '<path d="M24 17 V29" stroke="#3b2200" stroke-width="5" stroke-linecap="round"/><circle cx="24" cy="36" r="3" fill="#3b2200"/></svg>')
TICK = ('<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="#2fbf71"/><path d="M13 25 L21 33 L36 16" fill="none" stroke="#fff" stroke-width="5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
BOOK = '<svg viewBox="0 0 20 24"><path d="M2 2 H18 V22 L10 16 L2 22 Z" fill="#fff"/></svg>'
KEY = ('<svg viewBox="0 0 48 48"><circle cx="15" cy="24" r="9" fill="none" stroke="#F343A2" stroke-width="5"/><path d="M24 24 H44 M36 24 V31 M42 24 V30" '
       'fill="none" stroke="#F343A2" stroke-width="5" stroke-linecap="round"/></svg>')
META = ('<svg viewBox="0 0 48 48"><path d="M6 30 C6 18 12 12 17 12 C23 12 27 22 31 28 C34 33 37 36 40 36 C43 36 44 33 44 29 C44 20 39 12 33 12 C27 12 22 22 18 28 '
        'C15 33 12 36 9 36 C7 36 6 34 6 30 Z" fill="none" stroke="#fff" stroke-width="4"/></svg>')
GIFT = ('<svg viewBox="0 0 48 48"><rect x="6" y="18" width="36" height="24" rx="4" fill="#F343A2"/><rect x="4" y="12" width="40" height="9" rx="3" fill="#F54BA8"/>'
        '<rect x="21" y="12" width="6" height="30" fill="#fff"/></svg>')


def folder(fid, tab, label, lines=4, stamp_id=None, inside=""):
    st_html = f'<div class="stamp" id="{stamp_id}" style="left:120px;top:60px">Top Secret</div>' if stamp_id else ""
    fl = "".join(f'<i style="width:{w}%"></i>' for w in (92, 70, 84, 58)[:lines])
    return (f'<div class="fold" id="{fid}" data-layout-allow-overlap data-layout-allow-overflow><div class="ftab">{tab}</div><div class="fback"></div><div class="fpage">{inside}</div>'
            f'<div class="ffront" id="{fid}_fr"><div class="flabel">{label}</div><div class="flines">{fl}</div>{st_html}</div></div>')


# =======================================================================================================================
# 0 HOOK (dark): the case file, TOP SECRET, the leak
s0, e0 = S["g0"], END["g0"]
leak = ('<div class="leak"><div class="blurcard"><i class="av"></i><div class="tx"><i></i><i style="width:70%"></i></div></div>'
        f'<div class="up" id="up0">{ARROW_UP}</div>'
        '<div class="graph"><svg viewBox="0 0 660 360" preserveAspectRatio="none"><defs><linearGradient id="gfill" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#F343A2" stop-opacity=".35"/><stop offset="1" stop-color="#F343A2" stop-opacity="0"/></linearGradient></defs>'
        '<path class="ar" id="ar0" d="M0 340 L70 320 L140 330 L210 290 L280 300 L350 240 L420 210 L490 150 L560 90 L660 20 L660 360 L0 360 Z"/>'
        '<path class="ln" id="ln0" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" '
        'd="M0 340 L70 320 L140 330 L210 290 L280 300 L350 240 L420 210 L490 150 L560 90 L660 20"/></svg></div></div>')
HTML.append(f'<div class="scn" id="s0" style="opacity:1">{folder("f0", "CASE FILE 0814", "SUBJECT: GROWTH", 4, "stp0", leak)}</div>')
js('tl.set("#f0", {left: 140, top: 720}, 0);')
scene("s0", s0, e0)
h0a = H("h0a", [[("This", ""), ("is", ""), ("the", "")], [("secret", "it"), ("AI", "")]], 250, "g0", size=128, dark=True)
t_q = T("g0", "quietly")
HO("h0a", t_q - .12)
H("h0b", [[("quietly", "sm"), ("growing", "it")], [("Instagram", ""), ("accounts.", "")]], 270, "g0", size=112, dark=True, after=t_q - .05)
ft("#f0", 0, .6, "{y: 330, rotation: -11, opacity: 1}", "{y: 0, rotation: -2, opacity: 1}", "expo.out")
sfx("whoosh_big", 0)
sfx("paper", .12)
t_sec = T("g0", "secret")
stamp("#stp0", t_sec + .1, -12)
punch(t_sec + .12, 1.06)
for i in range(7):
    HTML.append(f'<i class="splat" id="sp{i}" style="left:{random.randint(260, 820)}px;top:{random.randint(760, 1080)}px;width:{random.randint(8, 22)}px;'
                f'height:{random.randint(8, 22)}px"></i>')
    ft(f"#sp{i}", t_sec + .1, .3, "{opacity: 0, scale: 0}", "{opacity: .85, scale: 1}", "back.out(3)")
    to(f"#sp{i}", t_q - .2, .3, "{opacity: 0}")
js(f'tl.to("#f0", {{rotation: 1, duration: 1.4, ease: "sine.inOut"}}, {t_sec + .3:.3f});')
# the cover swings open on "quietly"
js(f'tl.to("#f0_fr", {{rotationY: -168, transformPerspective: 2200, duration: .62, ease: "power3.inOut"}}, {t_q:.3f});')
sfx("open", t_q)
sfx("flip", t_q + .05)
sfx("whoosh", t_q + .1)
draw("#ln0", t_q + .35, 1.7, "power1.inOut")
ft("#ar0", t_q + .35, 1.7, "{opacity: 0}", "{opacity: 1}", "power1.in")
for k in range(6):
    sfx("tick", t_q + .45 + .28 * k)
ft("#up0", T("g0", "accounts") - .2, .45, "{opacity: 0, y: 40, scale: .5}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.4)")
sfx("ding2", T("g0", "accounts"))
js(f'tl.fromTo("#f0", {{scale: 1}}, {{scale: 1.05, duration: {e0 - t_q:.2f}, ease: "none", immediateRender: false}}, {t_q:.3f});')
spot(0, 120, 520, 1.1, .01)
spot(.05, 540, 1040, 1.0, .8, "power3.out")
spot(T("g0", "growing") + .1, 700, 1200, 1.15, 1.2)
# Cree pops up beside the file with his magnifier
C0 = (905, 1505, .36)
cree_pop(T("g0", "growing"), *C0, "mag")
blink(T("g0", "accounts") + .3)
whip(e0)

# =======================================================================================================================
# 1 NOT CHATGPT (dark): a generic chatbot window gets crossed out
s1, e1 = S["g1"], END["g1"]
HTML.append('<div class="scn" id="s1"><div class="chat" id="chat"><div class="ch"><i></i>ChatGPT</div><div class="b1">How do I grow my Instagram?</div>'
            '<div class="b2"><i></i><i style="width:88%"></i><i style="width:72%"></i><i style="width:80%"></i><i style="width:46%"></i></div></div>'
            '<svg class="xmark" viewBox="0 0 900 720"><path id="x0" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M120 110 L780 610"/>'
            '<path id="x1" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M780 110 L120 610"/></svg></div>')
scene("s1", s1, e1)
H("h1", [[("And", ""), ("no,", "")], [("it's", ""), ("not", "rd"), ("ChatGPT.", "")]], 250, "g1", size=118, dark=True)
t_and = T("g1", "And")
ft("#chat", t_and - .1, .55, "{opacity: 1, x: -1000, rotation: -8}", "{opacity: 1, x: 0, rotation: -2}", "back.out(1.4)")
sfx("whoosh", t_and - .1)
t_not = T("g1", "not")
draw("#x0", t_not - .02, .16, "power2.out")
draw("#x1", t_not + .14, .16, "power2.out")
sfx("scratch", t_not)
sfx("scratch", t_not + .15)
sfx("error", t_not + .05)
shake(t_not + .05, 12)
js(f'tl.to("#chat", {{filter: "grayscale(1) brightness(.55)", duration: .3}}, {t_not:.3f});')
t_drop = L1["g1"] + .05
to("#chat", t_drop, .45, "{y: 1500, rotation: 24}", "power2.in")
js(f'tl.to(".xmark", {{y: 1500, rotation: 24, duration: .45, ease: "power2.in"}}, {t_drop:.3f});')
sfx("swish", t_drop + .05)
spot(s1, 540, 940, .95, .6)
C1 = (905, 1505, .36)
cree_to(s1 - .05, *P(*C1), d=.01)
pose(t_and, "think", flip=False)
pose(t_not - .05, "sad")
cree_wiggle(t_not, 4, 10, .18)
say(t_not + .1, "!?", .9, left=True)
pose(t_drop, "stand")
blink(t_drop + .25)

# =======================================================================================================================
# 2 REVEAL: the codename peels off Creedom, the lights come up
s2, e2 = S["g2"], END["g2"]
redact(s2)
HTML.append('<div class="scn" id="s2"><div class="doss" id="doss"><div class="dk1">CODENAME</div><div class="dl" id="dl">DECLASSIFIED</div>'
            '<div class="dlogo"><img src="assets/img/creedom_logo.png" alt="Creedom"><i class="bar" id="cbar2"></i></div>'
            '<div class="tag" id="tag2">Stop guessing. <em>Just create.</em></div></div></div>')
scene("s2", s2, e2)
H("h2a", [[("It's", ""), ("called...", "")]], 300, "g2", size=110, dark=True)
ft("#doss", s2 - .02, .5, "{opacity: 1, y: 160, rotation: 4, scale: .92}", "{opacity: 1, y: 0, rotation: -1.5, scale: 1}", "back.out(1.5)")
t_cr = T("g2", "Creedom")
for k, dt in enumerate((-.42, -.3, -.2)):
    st("#cbar2", t_cr + dt, f"{{opacity: {(.35, 1, .5)[k]}}}")
st("#cbar2", t_cr - .1, "{opacity: 1}")
sfx("glitch", t_cr - .4)
sfx("glitch", t_cr - .2)
ft("#cbar2", t_cr, .38, "{scaleX: 1}", "{scaleX: 0}", "power3.inOut")
st("#wflash", t_cr + .02, "{opacity: .9}")
to("#wflash", t_cr + .04, .55, "{opacity: 0}", "power2.out")
light(t_cr + .02, True, .05)
HO("h2a", t_cr + .02)
sfx("sub", t_cr)
sfx("ding", t_cr + .05)
punch(t_cr + .05, 1.06)
ft("#dl", t_cr + .25, .35, "{opacity: 0, scale: 2, rotation: 0}", "{opacity: 1, scale: 1, rotation: 6}", "power4.in")
sfx("stamp2", t_cr + .58)
ft("#tag2", T("g2", "AI") + .1, .5, "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", "power3.out")
t_bas = T("g2", "Basically")
js(f'tl.to("#doss", {{y: -40, scale: .9, duration: .5, ease: "power3.inOut"}}, {t_bas - .1:.3f});')
H("h2b", [[("An", ""), ("Instagram", ""), ("coach", "it")], [("that", ""), ("reads", "pk"), ("your", ""), ("account.", "")]], 250, "g2", size=92, after=t_bas)
C2 = (540, 1500, .4)
cree_to(s2 - .05, *P(*C2), d=.01)
cree_hide(s2 - .05)
cree_pop(t_cr + .3, *C2, "present", flip=False)
sparkle(t_cr + .4, 1.0)
t_rd = T("g2", "reads")
pose(t_rd - .05, "mag", flip=False)
cree_wiggle(t_rd + .1, 2, 5)
blink(t_bas + .4)

# =======================================================================================================================
# 3 THE PROFILE UNDER THE SCAN LINE (light)
s3, e3 = S["g3"], END["g3"]
sheet(s3)
TB = ["linear-gradient(160deg,#ffd0e6,#F343A2)", "linear-gradient(160deg,#fde3c8,#F5876C)", "linear-gradient(160deg,#e9d6ff,#b14dff)",
      "linear-gradient(160deg,#ffe0ef,#ee688b)", "linear-gradient(160deg,#ffeacc,#f2b134)", "linear-gradient(160deg,#d8d0d4,#6b5a63)",
      "linear-gradient(160deg,#ffd6e8,#d81f86)", "linear-gradient(160deg,#f9d9c8,#e68b70)", "linear-gradient(160deg,#ffe3f1,#ff8cc6)"]
GOOD, BAD = (0, 4, 7), 5
tiles = ""
for i, bg in enumerate(TB):
    tg = '<span class="tg bad" id="tg5">KILLING VIEWS</span>' if i == BAD else (f'<span class="tg" id="tg{i}">WORKING</span>' if i in GOOD else "")
    rg = f'<i class="ring bad" id="rg{i}"></i>' if i == BAD else (f'<i class="ring" id="rg{i}"></i>' if i in GOOD else "")
    tiles += (f'<div class="tile" id="tl{i}" style="height:200px"><i class="tbg" style="background:{bg}"></i>'
              f'<i class="tbg" style="background:radial-gradient(40% 30% at {random.randint(30, 70)}% {random.randint(30, 60)}%,rgba(255,255,255,.55),rgba(255,255,255,0))"></i>'
              f'<i class="pl"></i>{rg}{tg}</div>')
HTML.append(f'<div class="scn" id="s3"><div class="prof" id="prof" style="left:130px"><div class="ph"><i class="av"></i><div><b>@yourhandle</b>'
            f'<span>SUBJECT · UNDER REVIEW</span></div></div><div class="tiles" id="tiles">{tiles}<i class="scan" id="scan"></i></div></div></div>')
scene("s3", s3, e3)
H("h3a", [[("What's", ""), ("working", "gn")], [("in", ""), ("your", ""), ("own", ""), ("reels,", "")]], 250, "g3", size=100)
t_and3 = T("g3", "and")
HO("h3a", t_and3 + .25)
H("h3b", [[("And", "sm"), ("what's", "sm"), ("quietly", "sm")], [("killing", "rd"), ("your", ""), ("views.", "")]], 250, "g3", size=110, after=t_and3)
ft("#prof", s3 + .05, .5, "{opacity: 1, y: 140, scale: .94}", "{opacity: 1, y: 0, scale: 1}", "back.out(1.4)")
js(f'tl.fromTo("#tl0, #tl1, #tl2, #tl3, #tl4, #tl5, #tl6, #tl7, #tl8", {{opacity: 0, scale: .6}}, {{opacity: 1, scale: 1, duration: .35, ease: "back.out(2)", '
   f'stagger: .04, immediateRender: false}}, {s3 + .12:.3f});')
sfx("flip", s3 + .15)
t_fi = T("g3", "finds")
st("#scan", t_fi - .05, "{opacity: 1}")
ft("#scan", t_fi - .05, 1.1, "{y: -10}", "{y: 624}", "power1.inOut")
ft("#scan", t_fi + 1.05, .9, "{y: 624}", "{y: -10}", "power1.inOut")
st("#scan", t_fi + 1.95, "{opacity: 0}")
sfx("riser_short", t_fi - .1)
t_wk = T("g3", "working")
for k, i in enumerate(GOOD):
    ft(f"#rg{i}", t_wk + .12 * k, .3, "{opacity: 0, scale: 1.2}", "{opacity: 1, scale: 1}", "back.out(2)")
    ft(f"#tg{i}", t_wk + .12 * k + .05, .35, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1}", "back.out(2.6)")
    js(f'tl.fromTo("#tl{i}", {{scale: 1}}, {{scale: 1.06, duration: .2, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_wk + .12 * k:.3f});')
    sfx("ding2", t_wk + .12 * k)
t_kl = T("g3", "killing")
st("#scan", t_kl - .3, "{opacity: 1}")
ft("#scan", t_kl - .3, .4, "{y: 0}", "{y: 300}", "power2.out")
st("#scan", t_kl + .2, "{opacity: 0}")
js(f'tl.to("#tl0, #tl1, #tl2, #tl3, #tl4, #tl6, #tl7, #tl8", {{opacity: .45, filter: "grayscale(.7)", duration: .3}}, {t_kl:.3f});')
ft("#rg5", t_kl, .25, "{opacity: 0, scale: 1.3}", "{opacity: 1, scale: 1}", "power3.out")
ft("#tg5", t_kl + .05, .3, "{opacity: 0, scale: 2.2}", "{opacity: 1, scale: 1}", "power4.in")
js(f'tl.fromTo("#tl5", {{x: 0}}, {{keyframes: [{{x: -10, duration: .05}}, {{x: 10, duration: .05}}, {{x: -8, duration: .05}}, {{x: 8, duration: .05}}, {{x: 0, duration: .05}}], '
   f'immediateRender: false}}, {t_kl + .05:.3f});')
js(f'tl.to("#tl5", {{scale: 1.14, zIndex: 6, duration: .3, ease: "back.out(2)"}}, {t_kl:.3f});')
sfx("error", t_kl)
sfx("stamp2", t_kl + .2)
punch(t_kl + .05, 1.05)
C3 = (920, 1520, .34)
cree_walk(s3 + .1, s3 + .9, P(1240, C3[1], C3[2]), P(*C3), end="mag")
pose(t_and3 + .3, "think")
pose(t_kl - .05, "shock")
sweat(t_kl + .1, 1.0)
say(t_kl + .05, "!", .8, left=True)
blink(t_fi + .6)

# =======================================================================================================================
# 4 BEFORE YOU POST: thumb on Share, the phone freezes, the warning flips to ready (light)
s4, e4 = S["g4"], END["g4"]
whip(s4)
HTML.append('<div class="scn" id="s4"><div class="phone" id="ph"><div class="scr"><i class="sky"></i><i class="subj"></i>'
            '<div class="cap"><i></i><i style="width:70%"></i></div><div class="frz" id="frz"></div>'
            '<div class="share" id="share">Share</div></div></div><i class="thumb" id="thumb"></i>'
            f'<div class="flipc" id="fc" data-layout-allow-overlap><div class="fi" id="fci"><div class="fa">{WARN}<div><small>0:01</small>Weak hook</div></div>'
            f'<div class="fb">{TICK}<div><small>FIXED</small>Ready to post</div></div></div></div></div>')
scene("s4", s4, e4)
H("h4a", [[("Before", ""), ("you", ""), ("post,", "pk")], [("it", ""), ("checks", "it"), ("your", ""), ("reel,", "")]], 250, "g4", size=104)
t_so = T("g4", "so")
HO("h4a", t_so - .1)
H("h4b", [[("so", ""), ("you", ""), ("fix", "pk"), ("the", ""), ("hook", "")], [("before", ""), ("it", ""), ("flops.", "rd")]], 250, "g4", size=104, after=t_so - .05)
ft("#ph", s4 + .05, .55, "{opacity: 1, y: 300, rotation: 6}", "{opacity: 1, y: 0, rotation: 0}", "back.out(1.4)")
t_po = T("g4", "post")
ft("#thumb", t_po - .3, .5, "{opacity: 1, x: 940, y: 1760}", "{opacity: 1, x: 465, y: 1330}", "power3.out")
to("#thumb", t_po + .22, .1, "{scale: .86}")
sfx("click", t_po + .22)
t_ck = T("g4", "checks")
st("#frz", t_ck, "{opacity: 1}")
ft("#frz", t_ck, .2, "{opacity: 0}", "{opacity: 1}")
js(f'tl.to("#share", {{backgroundColor: "#5b4a55", duration: .2}}, {t_ck:.3f});')
sfx("glitch", t_ck)
sfx("switch", t_ck + .05)
shake(t_ck, 8, 4)
t_rl = T("g4", "reel")
ft("#fc", t_rl - .1, .45, "{opacity: 1, scale: .5, y: 80}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.2)")
sfx("error", t_rl - .05)
sfx("pop", t_rl)
t_fx = T("g4", "fix")
js(f'tl.to("#fci", {{rotationY: 180, duration: .55, ease: "back.out(1.4)"}}, {t_fx:.3f});')
sfx("whoosh", t_fx)
sfx("ding", t_fx + .25)
to("#frz", t_fx + .15, .3, "{opacity: 0}")
js(f'tl.to("#share", {{backgroundColor: "#F343A2", duration: .25}}, {t_fx + .2:.3f});')
st("#share", t_fx + .3, '{textContent: "Post it"}')
to("#thumb", t_fx + .1, .35, "{scale: 1, opacity: 0, y: 1500}")
t_fl = T("g4", "flops")
js(f'tl.to("#fc", {{y: -20, duration: .25, yoyo: true, repeat: 1, ease: "power2.out"}}, {t_fl:.3f});')
C4 = (930, 1520, .34)
cree_to(s4 - .05, *P(*C4), d=.01)
pose(s4 + .1, "point", flip=True)
cree_hop(s4 + .15, 50)
pose(t_ck, "shock")
sweat(t_rl, .8)
pose(t_fx + .2, "cheer")
cree_hop(t_fx + .3, 80, 2)
pose(t_fl, "proud")
blink(t_po + .1)

# =======================================================================================================================
# 5 WHAT TO POST NEXT: classified memos fan out (dark, through the iris)
s5, e5 = S["g5"], END["g5"]
iris(s5)
light(s5, False, .02)
IDEAS = [("IDEA 01", "Your 5am routine, in 30 seconds"), ("IDEA 02", "3 tools you use every day"), ("IDEA 03", "Before and after: your desk setup")]
memos = "".join(f'<div class="memo" id="m{i}" style="top:560px"><i class="pclip"></i><div class="mk">NEXT POST · {k}</div><div class="mt">{t}</div>'
                f'<div class="mls"><i></i><i></i><i></i></div><div class="saved" id="sv{i}">{BOOK}your audience saved this</div></div>' for i, (k, t) in enumerate(IDEAS))
HTML.append(f'<div class="scn" id="s5"><div data-layout-allow-overlap>{memos}</div></div>')
scene("s5", s5, e5)
H("h5a", [[("Exactly", ""), ("what", "")], [("to", ""), ("post", ""), ("next.", "it")]], 250, "g5", size=120, dark=True)
t_bs = T("g5", "based")
HO("h5a", t_bs - .12)
H("h5b", [[("Based", ""), ("on", ""), ("what", ""), ("your", "")], [("audience", ""), ("actually", "sm"), ("saved.", "pk")]], 250, "g5", size=92, dark=True, after=t_bs - .05)
FAN = [(-232, 40, -9), (0, 0, 0), (232, 40, 9)]
for i in range(3):
    ft(f"#m{i}", s5 + .1 + .14 * i, .5, "{opacity: 1, y: 1300, rotation: 20, scale: .8}", "{opacity: 1, y: 0, rotation: 0, scale: .8}", "power3.out")
    sfx("paper", s5 + .12 + .14 * i)
t_nx = T("g5", "next")
for i, (dx, dy, r) in enumerate(FAN):
    js(f'tl.to("#m{i}", {{x: {dx}, y: {dy}, rotation: {r}, scale: .72, duration: .55, ease: "back.out(1.6)"}}, {t_nx - .05 + .04 * i:.3f});')
js(f'tl.set("#m1", {{zIndex: 22}}, {t_nx:.3f});')
sfx("whoosh_big", t_nx - .1)
sfx("flip", t_nx)
t_sv = T("g5", "saved")
t_au = T("g5", "audience")
for i in range(3):
    ft(f"#sv{i}", t_au - .1 + .14 * i, .4, "{opacity: 0, scale: .4, y: 20}", "{opacity: 1, scale: 1, y: 0}", "back.out(2.6)")
    sfx("ding2", t_au - .1 + .14 * i)
spot(s5, 540, 1000, 1.1, .4)
spot(t_nx, 540, 1000, 1.35, 1.0)
C5 = (540, 1500, .36)
cree_to(s5 - .05, *P(*C5), d=.01)
pose(s5 + .1, "phone", flip=False)
sfx("typing", s5 + .3)
pose(t_nx - .05, "point", flip=False)
pose(t_bs + .2, "think")
pose(t_sv - .2, "cheer")
cree_hop(t_sv - .1, 80)
blink(s5 + 1.2)

# =======================================================================================================================
# 6 THE CRAZY PART: lights go down, then the before / after graph and IT WORKED (dark)
s6, e6 = S["g6"], END["g6"]
t_cz = T("g6", "crazy")
st("#blackout", s6, "{opacity: .9}")
to("#blackout", s6 + .08, .7, "{opacity: 0}", "power2.out")
sfx("switch", s6)
sfx("sub", s6)
HTML.append('<div class="scn" id="s6"><div class="gcard" id="gc" style="height:640px"><div class="gk">RESULTS · AFTER YOU POST</div>'
            '<svg viewBox="0 0 780 460"><line class="ax" x1="0" y1="440" x2="780" y2="440"/>'
            '<path class="gbefore" id="gb" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M0 380 L60 392 L120 372 L180 390 L240 378 L300 386 L380 380"/>'
            '<line class="mark" id="gm" x1="390" y1="20" x2="390" y2="440"/>'
            '<path class="gafter" id="ga" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" d="M380 380 L450 350 L520 300 L590 230 L660 150 L720 90 L780 30"/></svg>'
            '<div class="mlab" id="mlab">ADVICE APPLIED</div><span class="bl2" style="left:120px;bottom:36px">BEFORE</span>'
            '<span class="bl2" style="right:120px;bottom:36px;color:#c2186f">AFTER</span>'
            '<div class="stamp gn" id="stp6" style="left:230px;top:220px;font-size:104px">It Worked</div></div></div>')
scene("s6", s6, e6)
H("h6a", [[("And", ""), ("the", "")], [("crazy", "it"), ("part?", "")]], 640, "g6", size=170, dark=True)
js(f'tl.fromTo("#h6a", {{scale: 1}}, {{scale: 1.08, duration: 1.6, ease: "none", immediateRender: false}}, {s6:.3f});')
js(f'tl.fromTo("#h6a", {{rotation: 0}}, {{keyframes: [{{rotation: -2, duration: .05}}, {{rotation: 2, duration: .05}}, {{rotation: 0, duration: .05}}], immediateRender: false}}, {t_cz:.3f});')
sfx("riser", T("g6", "part") - .2)
spot(s6, 540, 880, .55, .3, "power3.out")
t_af = T("g6", "After")
HO("h6a", t_af - .15)
H("h6b", [[("It", ""), ("shows", ""), ("you", ""), ("if", ""), ("the", "")], [("advice", ""), ("actually", "sm"), ("worked.", "gn")]], 250, "g6", size=92, dark=True,
     after=t_af + .5)
spot(t_af - .1, 540, 1000, 1.3, .6)
ft("#gc", t_af - .1, .55, "{opacity: 1, y: 300, rotationX: 40, transformPerspective: 1600}", "{opacity: 1, y: 0, rotationX: 0, transformPerspective: 1600}", "back.out(1.3)")
sfx("whoosh", t_af - .1)
draw("#gb", t_af + .35, .9, "power1.inOut")
t_sh = T("g6", "shows")
ft("#gm", t_sh - .1, .3, "{opacity: 0, scaleY: 0}", "{opacity: 1, scaleY: 1}", "power3.out")
ft("#mlab", t_sh, .3, "{opacity: 0, y: -20}", "{opacity: 1, y: 0}", "back.out(2)")
sfx("click", t_sh)
draw("#ga", T("g6", "you", 1) + .05, 1.1, "power2.in")
sfx("riser_short", T("g6", "you", 1))
t_wo = T("g6", "worked")
stamp("#stp6", t_wo + .08, -8)
sfx("ding", t_wo + .12)
punch(t_wo + .1, 1.06)
C6 = (930, 1520, .32)
cree_to(s6 - .05, *P(*C6), d=.01)
pose(s6 + .05, "shock")
pose(t_cz + .3, "think")
say(t_cz + .2, "?", .9, left=True)
pose(t_af + .2, "mag", flip=False)
pose(t_wo + .05, "cheer")
cree_hop(t_wo + .1, 90, 2)
sparkle(t_wo + .15, 1.1)
blink(t_af + 1.2)

# =======================================================================================================================
# 7 SOCIAL PROOF (light): the counter, the creators, the pills
s7, e7 = S["g7"], END["g7"]
sheet(s7)
light(s7, True, .02)
DOTC = ["linear-gradient(135deg,#F515E8,#F5876C)", "linear-gradient(135deg,#ff8cc6,#F343A2)", "linear-gradient(135deg,#ffc21a,#F5876C)",
        "linear-gradient(135deg,#b98bff,#F343A2)", "linear-gradient(135deg,#ffd0e6,#ee688b)"]
dots = ""
pts = []
for _ in range(20000):                           # dots live around the counter, its line and the pills, never on them
    if len(pts) >= 34:
        break
    ax, ay = random.randint(70, 1010), random.randint(470, 1480)
    if (130 < ax < 950 and 520 < ay < 1010) or (90 < ax < 990 and 1060 < ay < 1360):
        continue
    if all((ax - a) ** 2 + (ay - b) ** 2 > 74 ** 2 for a, b in pts):
        pts.append((ax, ay))
pts = [(ax - 23, ay - 23) for ax, ay in pts]       # top-left corners in frame px (the .dots layer is the full frame)
for i, (x, y) in enumerate(pts):
    dots += f'<i class="dot" id="dt{i}" style="left:{x}px;top:{y}px;background:{random.choice(DOTC)}"></i>'
HTML.append(f'<div class="scn" id="s7"><div class="dots" style="left:0;top:0;width:1080px;height:1920px">{dots}</div><div class="count" id="cnt">0</div>'
            f'<div class="pill blk" id="pl0" style="top:1090px">{META}Official Meta Tech Partner</div>'
            f'<div class="pill wht" id="pl1" style="top:1230px">{GIFT}Your first account read is <span class="fr" id="fr">free</span></div></div>')
scene("s7", s7, e7)
H("h7", [[("creators", "pk"), ("already", "")], [("using", ""), ("it.", "")]], 800, "g7", size=96)
t_hu = T("g7", "hundred")
t_th = T("g7", "thousand")
ft("#cnt", t_hu - .1, .3, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "back.out(2)")
n = int((t_th + .4 - t_hu) * 30)
for k in range(n + 1):
    v = int(round(150000 * (1 - (1 - k / n) ** 3) / 10) * 10)
    st("#cnt", t_hu + k / 30, f'{{textContent: "{v:,}"}}')
    if k % 3 == 0:
        sfx("tick", t_hu + k / 30)
st("#cnt", t_th + .45, '{textContent: "150,000+"}')
js(f'tl.fromTo("#cnt", {{scale: 1}}, {{scale: 1.1, duration: .16, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_th + .45:.3f});')
sfx("coin", t_th + .45)
punch(t_th + .47, 1.04)
order = sorted(range(len(pts)), key=lambda i: random.random())
for j, i in enumerate(order):
    ft(f"#dt{i}", t_hu + .02 * j, .3, "{opacity: 0, scale: 0}", "{opacity: .9, scale: 1}", "back.out(3)")
for j in range(0, len(order), 6):
    sfx("pop", t_hu + .02 * j)
js(f'tl.to(".dot", {{y: "-=26", duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: 2, stagger: {{each: .03, from: "random"}}}}, {t_th + .5:.3f});')
t_al = T("g7", "already")
ft("#pl0", t_al + .1, .45, "{opacity: 0, y: 60, scale: .7}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
sfx("pop", t_al + .1)
t_fs = T("g7", "first")
ft("#pl1", t_fs - .15, .45, "{opacity: 0, y: 60, scale: .7}", "{opacity: 1, y: 0, scale: 1}", "back.out(2)")
sfx("pop", t_fs - .15)
t_fr = T("g7", "free")
js(f'tl.fromTo("#fr", {{scale: 1}}, {{scale: 1.35, duration: .18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false}}, {t_fr:.3f});')
js(f'tl.fromTo("#pl1", {{boxShadow: "0 16px 34px rgba(177,71,107,.25)"}}, {{boxShadow: "0 0 0 10px rgba(243,67,162,.35)", duration: .25, yoyo: true, repeat: 1, '
   f'immediateRender: false}}, {t_fr:.3f});')
sfx("ding2", t_fr)
C7 = (935, 1520, .3)
cree_hide(s7 - .05)
t_us = T("g7", "using")
cree_walk(t_us - .4, t_us + .3, P(1260, C7[1], C7[2]), P(*C7), end="proud")
pose(t_fr - .05, "cheer")
cree_hop(t_fr, 70)
st("#cree", t_us - .4, "{opacity: 1}")

# =======================================================================================================================
# 8 CTA (dark): Comment GROW, the DM, the case file closes on "secret"
s8 = S["g8"]
redact(s8)
light(s8, False, .02)
cty = "".join(f"<i>{c}</i>" for c in "GROW")
HTML.append('<div class="scn" id="s8">'
            f'{folder("f8", "CASE FILE 0814", "SUBJECT: YOUR ACCOUNT", 3, "stp8")}'
            '<div class="grow" id="grow" style="top:400px">GROW</div>'
            f'<div class="cbar" id="cbr" style="top:780px"><i class="cav"></i><span class="cph" id="cph">Add a comment…</span><span class="cty" id="cty">{cty}</span>'
            '<b class="csend" id="csend"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></b></div>'
            f'<div class="dm" id="dm" style="top:950px"><img src="assets/img/c100x_mark.png" alt=""><div><b>creators.100x</b><span>{KEY}Here\'s the secret</span></div>'
            '<em>now</em></div></div>')
js('tl.set("#f8", {left: 140, top: 1150, scale: .55, transformOrigin: "50% 0%"}, 0);')
scene("s8", s8, DUR + 1)
H("h8", [[("Comment", "")]], 250, "g8", size=110, dark=True)
t_cm = T("g8", "Comment")
t_gw = T("g8", "GROW")
ft("#grow", t_gw, .22, "{opacity: 0, scale: 2.4}", "{opacity: 1, scale: 1}", "power4.in")
shake(t_gw + .2, 14)
sfx("stamp", t_gw + .18)
sfx("sub", t_gw + .18)
js(f'tl.to("#grow", {{scale: 1.04, duration: .9, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {t_gw + .4:.3f});')
ft("#f8", s8 + .05, .55, "{opacity: 1, y: 900, rotation: 10}", "{opacity: 1, y: 0, rotation: -2}", "back.out(1.3)")
sfx("paper", s8 + .1)
ft("#cbr", t_gw + .3, .45, "{opacity: 0, y: 80}", "{opacity: 1, y: 0}", "back.out(1.7)")
t_ty = t_gw + .65
st("#cph", t_ty, "{opacity: 0}")
js(f'tl.fromTo("#cty i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: .08, immediateRender: false}}, {t_ty:.3f});')
for k in range(4):
    sfx("click", t_ty + .08 * k)
to("#csend", t_ty + .4, .1, "{scale: .8}")
to("#csend", t_ty + .5, .25, "{scale: 1.12, backgroundColor: '#F343A2'}", "back.out(3)")
sfx("click", t_ty + .42)
t_sd = T("g8", "send")
ft("#dm", t_sd - .1, .55, "{opacity: 0, y: -160}", "{opacity: 1, y: 0}", "back.out(1.6)")
sfx("ding", t_sd)
t_sc = T("g8", "secret")
stamp("#stp8", t_sc + .12, -12)
spot(s8, 540, 900, 1.25, .5)
C8 = (930, 1520, .3)
cree_to(s8 - .05, *P(*C8), d=.01)
pose(s8 + .1, "phone", flip=False)
pose(t_sd - .1, "point", flip=True)
cree_wiggle(t_sd, 2, 5)
pose(t_sc + .15, "cheer")
cree_hop(t_sc + .2, 80, 2)
pose(t_sc + 1.0, "wave", flip=False)
blink(t_sc + 1.4)

for hid, line in HEADS:
    if hid not in CLOSED and line != "g8":
        HO(hid, END[line] - .24)

# ---- Cree's idle breathing over the whole reel --------------------------------------------------------------------------
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -9, duration: .8, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .8)}, immediateRender: false}}, 0);')
HTML.append(cree_html())

# ---- worlds -------------------------------------------------------------------------------------------------------------
LB = [(-260, -200, 760, "rgba(238,104,139,.5)"), (520, 240, 820, "rgba(255,190,214,.7)"), (-280, 1000, 900, "rgba(217,194,255,.5)"),
      (480, 1300, 820, "rgba(255,216,194,.6)")]
blobs = "".join(f'<i class="bl" id="lb{i}" style="left:{x}px;top:{y}px;width:{z}px;height:{z}px;background:{c}"></i>' for i, (x, y, z, c) in enumerate(LB))
for i in range(len(LB)):
    js(f'tl.fromTo("#lb{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-240, 240)}, y: {random.randint(-240, 240)}, scale: {random.uniform(.85, 1.3):.2f}, '
       f'duration: {DUR / 3:.2f}, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false}}, 0);')
dust = ""
for i in range(28):
    x, y, z = random.randint(40, 1040), random.randint(300, 1700), random.choice((4, 5, 6, 8))
    dust += f'<i class="dust" id="du{i}" style="left:{x}px;top:{y}px;width:{z}px;height:{z}px"></i>'
    js(f'tl.fromTo("#du{i}", {{x: 0, y: 0, opacity: {random.uniform(.2, .8):.2f}}}, {{x: {random.randint(-80, 80)}, y: {-random.randint(160, 420)}, '
       f'opacity: {random.uniform(.1, .7):.2f}, duration: {random.uniform(6, 11):.2f}, ease: "sine.inOut", yoyo: true, repeat: 5, immediateRender: false}}, 0);')

CSS = open(os.path.join(ROOT, "build", "style.css")).read().replace("$INK", INK)
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: GROW, the secret AI (Classified) 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="world" id="dark"><i id="felt"></i><i id="spot2"></i><i id="spot"></i>{dust}</div>
      <div class="world" id="light">{blobs}<i id="lgrid"></i></div>
      <div id="cam"><div id="shake"><div id="punch"><div id="drift">
        {chr(10).join(HTML)}
      </div></div></div></div>
      <i class="stk" id="stk0"></i><i class="stk" id="stk1"></i><i class="stk" id="stk2"></i>
      <div id="redact"></div>
      <div id="sheet"><b>CLASSIFIED</b></div>
      <div id="iris"></div>
      <div id="blackout"></div>
      <div id="flash"></div>
      <div id="wflash"></div>
      <div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set("#redact", {{x: -2100, rotation: -12, opacity: 1}}, 0);
      tl.set("#sheet", {{y: 2400, opacity: 1}}, 0);
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
json.dump({"dur": DUR, "scenes": {k: [S[k], END[k]] for k in K}}, open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx; cuts {[round(S[k], 2) for k in K]}")
