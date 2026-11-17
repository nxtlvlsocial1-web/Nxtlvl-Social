"""Creators 100X x Creedom "@write-script" reel (9:16, Option A "The blank screen"): writes index.html,
plan/sfx_events.json and plan/edit.json from plan/words.json.

Same look as the CHECK reel (light and dark fluid worlds, frosted glass, word-by-word focus type, Cree the mascot,
liquid-glass morphs, whips, punch-ins), with every visual from the approved plan (plan/script_options.md, Option A):
  A  real footage: a creator sets up her phone and ring light (Pexels 9384669), then a phone with an empty notes page
     and a blinking cursor;
  B  a grey generic AI script types out and a red "SOUNDS LIKE EVERYONE" stamp slams onto it;
  C  the card crumples and flies off; our six past reels sit greyed out ("never seen"), Cree peeks in with his magnifier;
  D  Creedom's home screen rebuilt in code from the owner's screenshot; "@write-script" types into the pink input,
     snaps into a pill and sends;
  E  the past reels fan out and get read; openers, pauses and words fly out of them into a "your voice" card;
  F  the script card writes itself; its first line glows with a "from your reel 0:02" tag;
  G  the card splits into HOOK / STORY / CTA blocks over real footage (Pexels 7234061), then shrinks into a
     teleprompter on the phone;
  H  CTA: "Comment SCRIPT", the comment types in, Creedom's DM arrives, Cree points at it.
The script on screen is an example and says so.
python3 build/generate.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import *          # noqa: F401,F403  (helpers and the shared JS / SFX / HTML lists)

random.seed(17)
DUR = round(L1["w07"] + .8, 2)
RED = "#E5383B"


def chars(cid, text, cls=""):
    """text as one span per character, for typing that is a pure tween (exact on every frame)"""
    return f'<span class="ty {cls}" id="{cid}">' + "".join(f'<i>{"&nbsp;" if c == " " else c}</i>' for c in text) + "</span>"


def type_on(cid, t, d, n, tick=True):
    js(f'tl.fromTo("#{cid} i", {{opacity: 0}}, {{opacity: 1, duration: .01, stagger: {d / n:.3f}, immediateRender: false}}, {t:.3f});')
    if tick:
        for k in range(0, n, 2):
            sfx("tick", t + d / n * k)


def words_on(sel, t, d):
    js(f'tl.fromTo("{sel}", {{opacity: 0, y: 14, filter: "blur(6px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: .22, '
       f'stagger: {d:.3f}, ease: "power2.out", immediateRender: false}}, {t:.3f});')


def wsp(text):
    return " ".join(f"<span>{w}</span>" for w in text.split())


def blink_cursor(sel, t0, t1, per=.5):
    n = max(1, int((t1 - t0) / per))
    js(f'tl.fromTo("{sel}", {{opacity: 1}}, {{opacity: 0, duration: {per / 2:.2f}, ease: "steps(1)", yoyo: true, repeat: {2 * n - 1}, immediateRender: false}}, {t0:.3f});')
    st(sel, t1, "{opacity: 0}")


# ---- scene cuts on the half-beat grid of the song --------------------------------------------------------------------------
SA = 0.0
SA2 = snap(T("w00", "and") - .1)
SB, SC, SD, SE, SF, SG, SX = (snap(L0[k] - .12) for k in ("w01", "w02", "w03", "w04", "w05", "w06", "w07"))
T_IN = T("w06", "In")

# ---- icons ------------------------------------------------------------------------------------------------------------------
def ico(path, cls="ic", vb="0 0 24 24"):
    return f'<svg class="{cls}" viewBox="{vb}"><path d="{path}"/></svg>'


I_BOLT = ico("M13 2 4 14h7l-1 8 9-12h-7l1-8z")
I_FILM = ('<svg class="ic" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 3v18M17 3v18M3 8h4M3 12h4M3 16h4'
          'M17 8h4M17 12h4M17 16h4"/></svg>')
I_PEN = ico("M4 20h4L19 9l-4-4L4 16v4zM14 6l4 4M13 20h7")
I_SEND = ico("M21 3 10 14M21 3l-7 18-4-7-7-4 18-7z")
I_IG = '<svg class="ig" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="16.9" cy="7.1" r=".6"/></svg>'
I_EYE = ('<svg class="eye" viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'
         '<path d="M3 3l18 18"/></svg>')

# ============================================================================================================================
# A1 hook: real footage, she sets up the phone and the ring light
HTML.append('<div class="scn" id="sa1"><video class="foot" id="v1" src="assets/video/9384669.mp4" data-start="0" '
            f'data-duration="{SA2 + .1:.3f}" data-media-start="1.2" data-track-index="1" muted playsinline></video>'
            '<div class="topfade"></div><div class="ringglow" id="ringglow"></div>')
head("ha1", [[("Camera's", ""), ("set", ""), ("up.", "")], [("Lights", ""), ("on.", "it")]], 200, "w00", 104, dark=True)
HTML.append("</div>")
scene("sa1", SA, SA2)
sfx("impact", 0)
streak(.1)
t_l = T("w00", "lights")
punch(t_l, 1.06)
ft("#ringglow", t_l - .05, .5, "{opacity: 0, scale: .6}", "{opacity: 1, scale: 1}", "power2.out")
sfx("click", t_l - .05)

# A2: the phone, an empty notes page and a blinking cursor
HTML.append('<div class="scn" id="sa2">')
head("ha2", [[("And", ""), ("I've", ""), ("got", "")], [("nothing", "it pk"), ("to", ""), ("say.", "")]], 200, "w00", 96, after=SA2 - .2)
HTML.append('<div class="phone" id="phone"><div class="scr notes"><div class="nbar"><span>&#8249; Notes</span><b>Done</b></div>'
            '<div class="ntitle">Reel script</div><div class="ndate">Today, 11:42 PM</div><div class="nbody"><i class="cur" id="cur"></i></div>'
            '<div class="nwc" id="nwc">0 words</div></div><div class="isl"></div></div></div>')
scene("sa2", SA2, SB)
zoom_through(SA2)
ft("#phone", SA2 + .02, .55, "{opacity: 0, y: 160, rotationX: 18, scale: .66}", "{opacity: 1, y: 0, rotationX: 0, scale: .72}", "back.out(1.4)")
blink_cursor("#cur", SA2 + .3, SB)
t_no = T("w00", "nothing")
punch(t_no, 1.05)
ft("#nwc", t_no, .4, "{opacity: 0, y: 20}", "{opacity: 1, y: 0}", "back.out(2)")
head_out("ha2", SB - .3)

# ============================================================================================================================
# B (dark): the generic AI script, then the stamp
GEN = ["In today's fast-paced digital world,", "consistency is the key to success.", "Here are 5 tips to unlock your", "full potential. Let's dive in!"]
gen_lines = "".join(f'<p class="gl">{wsp(x)}</p>' for x in GEN)
HTML.append('<div class="scn" id="sb">')
head("hb1", [[("I", ""), ("asked", ""), ("AI", "")], [("for", ""), ("a", ""), ("script.", "it")]], 190, "w01", 92, dark=True)
head("hb2", [[("It", ""), ("sounded", ""), ("like", ""), ("a", "")], [("LinkedIn", "it pk"), ("post.", "it pk")]], 190, "w01", 92, dark=True,
     after=T("w01", "sounded") - .1)
HTML.append("</div>")
HTML.append('<div class="gen" id="gen"><div class="ghead"><i class="gav">AI</i><span>GENERIC AI CHAT</span></div>'
            '<div class="gq">Write me a reel script</div>' + gen_lines +
            '<div class="stamp" id="stamp">SOUNDS LIKE<br>EVERYONE</div></div>')
scene("sb", SB, SC)
whip(SB)
mode(SB, True)
t_as = T("w01", "asked")
ft("#gen", SB + .02, .55, "{opacity: 0, y: 200, rotationX: 30, scale: .9}", "{opacity: 1, y: 0, rotationX: 0, scale: 1}", "back.out(1.3)")
ft("#gen .gq", t_as, .35, "{opacity: 0, x: 60}", "{opacity: 1, x: 0}", "back.out(1.6)")
sfx("pop", t_as)
t_sc0 = T("w01", "script")
words_on("#gen .gl span", t_sc0, .06)
for k in range(10):
    sfx("tick", t_sc0 + .12 * k)
head_out("hb1", T("w01", "sounded") - .25)
t_li = T("w01", "LinkedIn")
ft("#stamp", t_li - .02, .22, "{opacity: 0, scale: 2.6, rotation: -24}", "{opacity: 1, scale: 1, rotation: -12}", "power4.in")
sfx("stamp", t_li + .18)
punch(t_li + .2, 1.07)
to("#gen", t_li + .2, .5, "{filter: 'grayscale(1)'}")
ft("#gen", t_li + .2, .25, "{x: 0}", "{x: 0, keyframes: [{x: -14, duration: .05}, {x: 12, duration: .05}, {x: -6, duration: .05}, {x: 0, duration: .05}]}", "none")
head_out("hb2", SC - .3)

# ============================================================================================================================
# C (light): the card crumples and flies off; our past reels, never seen; Cree peeks in with his magnifier
REELS = [f"assets/img/reel{i}.jpg" for i in range(6)]
grid = "".join(f'<div class="gr" id="gr{i}"><img src="{s}">{I_EYE}</div>' for i, s in enumerate(REELS))
HTML.append(f'<div class="scn" id="sc"><div class="grid">{grid}</div><div class="seen glass" id="seen">{SH}<b>0</b> of my reels seen</div>')
head("hc", [[("It's", ""), ("never", "it"), ("seen", "")], [("a", ""), ("single", ""), ("one", "it pk")], [("of", ""), ("my", ""), ("reels.", "")]],
     170, "w02", 82)
HTML.append("</div>")
scene("sc", SC, SD)
# crumple: squeeze, spin, round off into a ball, then a throw to the left
js(f'tl.to("#gen", {{keyframes: [{{scaleX: .8, scaleY: .7, rotation: 8, borderRadius: "60px", duration: .12}}, '
   f'{{scale: .42, rotation: -40, borderRadius: "45%", skewX: 12, filter: "grayscale(1) brightness(.85)", duration: .14}}, '
   f'{{scale: .22, rotation: 120, borderRadius: "50%", skewX: -8, duration: .1}}], ease: "power2.in"}}, {SC - .3:.3f});')
to("#gen", SC - .02, .35, "{x: -900, y: -380, rotation: 420, opacity: 0}", "power2.in")
st("#stamp", SC - .1, "{opacity: 0}")
sfx("impact", SC - .3)
sfx("whoosh", SC - .05)
mode(SC, False)
streak(SC)
t_se = T("w02", "seen")
for i in range(6):
    t = t_se - .3 + .07 * i
    ft(f"#gr{i}", t, .5, "{opacity: 0, y: 80, scale: .7, rotationX: 40}", "{opacity: 1, y: 0, scale: 1, rotationX: 0}", "back.out(1.5)")
    sfx("shutter" if i % 2 == 0 else "tick", t)
ft(".gr .eye", T("w02", "single"), .4, "{opacity: 0, scale: .4}", "{opacity: 1, scale: 1, stagger: .05}", "back.out(2.5)")
ft("#seen", T("w02", "one"), .45, "{opacity: 0, y: 30, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "back.out(1.6)")
shine("#seen", T("w02", "one") + .3, .6)
sfx("buzzer", T("w02", "one"))
head_out("hc", SD - .28)

# ============================================================================================================================
# D (light): Creedom's home screen, rebuilt from the owner's screenshot (native 1320 x 1734, shown at 760 px wide)
APP_S = 760 / 1320
CARDS = [(I_BOLT, "Ideas tuned to your account"), (I_FILM, "Check a reel before you post"), (I_PEN, "Get a script in your voice"),
         (I_SEND, "Send a DM to your comments")]
cards = "".join(f'<div class="uc" id="uc{i}" style="left:{(62, 668)[i % 2]}px;top:{(895, 1213)[i // 2]}px">{ic}<div>{tx}</div></div>'
                for i, (ic, tx) in enumerate(CARDS))
CHIPS = [("Audit my Instagram profile", 305, 660), ("Use one of my Reels and give me insights", 459, 970), ("Analyse one of my latest reels", 613, 735)]
chips = "".join(f'<div class="uchip" id="uh{i}" style="top:{y}px;width:{w}px;margin-left:{-w // 2}px">{tx}</div>' for i, (tx, y, w) in enumerate(CHIPS))
HTML.append('<div class="scn" id="sd">')
head("hd", [[("I", ""), ("typed", ""), ("one", "it"), ("thing.", "it")]], 175, "w03", 86)
HTML.append(f'<div class="app" id="app"><div class="appi" style="transform:scale({APP_S:.5f})">'
            '<div class="ucirc" style="left:50px"><i></i><i></i><i></i></div>'
            f'<div class="uacct">{I_IG}<span>creators.100x</span><svg class="chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></div>'
            '<div class="ucirc ued" style="left:1140px"><svg viewBox="0 0 24 24"><path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg></div>'
            f'<div class="utitle">How can Cree help?</div>{chips}<div class="ustart">START SOMETHING</div>{cards}'
            '<div class="uin" id="uin"><div class="uplus">+</div><div class="utext"><i class="cur2" id="cur2"></i>'
            + chars("ws", "@write-script") + '<span class="wpill" id="wpill">@write-script</span></div>'
            '<div class="usend" id="usend"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div></div>'
            '<i class="ash" id="ash"></i></div></div></div>')
scene("sd", SD, SE)
liquid(SD)
ft("#app", SD + .02, .6, "{opacity: 0, y: 220, rotationX: 24, scale: .9}", "{opacity: 1, y: 0, rotationX: 0, scale: 1}", "back.out(1.3)")
ft(".uchip", SD + .25, .4, "{opacity: 0, y: 40, scale: .9}", "{opacity: 1, y: 0, scale: 1, stagger: .07}", "back.out(1.8)")
ft(".uc", SD + .45, .4, "{opacity: 0, y: 50, scale: .9}", "{opacity: 1, y: 0, scale: 1, stagger: .06}", "back.out(1.6)")
sfx("swish", SD + .25)
t_ty = T("w03", "typed")
to("#uin", t_ty - .05, .3, "{boxShadow: '0 0 0 10px rgba(238,104,139,.18), 0 20px 50px rgba(238,104,139,.35)'}")
blink_cursor("#cur2", t_ty, T("w03", "At") - .02, .4)
sfx("click", t_ty)
t_cr = T("w03", "Creedom")
to("#uc2", t_cr - .05, .35, "{borderColor: '#EE688B', boxShadow: '0 0 0 6px rgba(238,104,139,.25), 0 24px 60px rgba(243,67,162,.3)', scale: 1.04}", "back.out(2)")
ft("#ash", t_cr, .9, "{xPercent: -160}", "{xPercent: 460}", "power2.inOut")
punch(t_cr, 1.04)
t_at = T("w03", "At")
type_on("ws", t_at, .5, 13)
t_snap = t_at + .62
st("#ws", t_snap, "{opacity: 0}")
ft("#wpill", t_snap, .4, "{opacity: 0, scale: 1.35}", "{opacity: 1, scale: 1}", "back.out(2.6)")
sfx("pop", t_snap)
to("#usend", t_snap + .1, .3, "{background: 'linear-gradient(135deg, #EE688B, #F343A2)', scale: 1.12}", "back.out(2)")
to("#usend", t_snap + .4, .12, "{scale: .88}")
to("#usend", t_snap + .52, .25, "{scale: 1}", "back.out(3)")
sfx("click", t_snap + .4)
sfx("whoosh", t_snap + .45)
tilt("#app", SD + .7, SE - .2, 3, 1.1)
head_out("hd", SE - .28)

# ============================================================================================================================
# E (dark): the past reels fan out and get read; openers, pauses and words fly into the "your voice" card
FAN = [(-27, -330), (-16, -200), (-6, -68), (6, 68), (16, 200), (27, 330)]           # (rotation, x offset) around x 540
fan = "".join(f'<div class="fan" id="fn{i}"><img src="{REELS[i]}"></div>' for i in range(6))
VOICE = [("vo0", "OPENER", "“Nobody talks about this…”", 34, 86, 2), ("vo1", "PAUSE", "— beat —", 34, 180, 0),
         ("vo2", "WORDS", "“Save this.”", 34, 274, 4), ("vo3", "WORDS", "“Here’s the thing”", 34, 368, 5)]
vchips = "".join(f'<div class="vc glass dkg" id="{v}" style="left:{x}px;top:{y}px">{SH}<u>{tag}</u><span>{tx}</span></div>' for v, tag, tx, x, y, _ in VOICE)
HTML.append(f'<div class="scn" id="se"><div class="fanw">{fan}</div><div class="scanb" id="scanb"></div>'
            f'<div class="vcard glass dkg" id="vcard">{SH}<div class="vh"><img src="assets/img/creedom_logo.png"><span>YOUR VOICE</span></div>{vchips}</div>')
head("he1", [[("It", ""), ("read", ""), ("my", "")], [("reels", ""), ("first.", "it pk")]], 175, "w04", 92, dark=True)
head("he2", [[("My", ""), ("openers,", "it pk"), ("my", ""), ("pauses,", "it pk")], [("the", ""), ("words", "it pk"), ("I", ""), ("use.", "")]],
     175, "w04", 78, dark=True, after=T("w04", "My") - .1)
HTML.append("</div>")
scene("se", SE, SF)
whip(SE, -1)
mode(SE, True)
st("#app", SE, "{opacity: 0}")
t_rd = T("w04", "read")
for i, (r, x) in enumerate(FAN):
    t = t_rd - .15 + .06 * i
    ft(f"#fn{i}", t, .55, "{opacity: 0, x: 0, y: 160, rotation: 0, scale: .6}", f"{{opacity: 1, x: {x}, y: {abs(x) * .18:.0f}, rotation: {r}, scale: 1}}", "back.out(1.5)")
    sfx("shutter" if i % 2 == 0 else "tick", t)
t_fi = T("w04", "first")
ft("#scanb", t_fi - .1, .75, "{opacity: 1, x: -560}", "{opacity: 1, x: 560}", "sine.inOut")
to("#scanb", t_fi + .65, .15, "{opacity: 0}")
js(f'tl.fromTo(".fan", {{boxShadow: "0 20px 40px rgba(0,0,0,.4)"}}, {{boxShadow: "0 0 40px 6px rgba(243,67,162,.7)", duration: .2, stagger: .1, yoyo: true, repeat: 1, immediateRender: false}}, {t_fi:.3f});')
sfx("riser_short", t_fi - .3)
head_out("he1", T("w04", "My") - .3)
ft("#vcard", T("w04", "My") - .2, .5, "{opacity: 0, y: 120, scale: .92, filter: 'blur(12px)'}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#vcard", T("w04", "My") + .2)
VC_TOP, VC_LEFT = 890, 90
for (v, tag, tx, x, y, src), key in zip(VOICE, ("openers", "pauses", "words", "use")):
    t = T("w04", key) - .08
    r, fx_ = FAN[src]
    sx, sy = 540 + fx_ - (VC_LEFT + x) - 120, 640 - (VC_TOP + y)                     # from its source reel in the fan
    ft(f"#{v}", t, .5, f"{{opacity: 0, x: {sx:.0f}, y: {sy:.0f}, scale: .5, rotation: {r}}}", "{opacity: 1, x: 0, y: 0, scale: 1, rotation: 0}", "back.out(1.3)")
    ft(f"#fn{src}", t - .05, .3, "{filter: 'brightness(1)'}", "{filter: 'brightness(1.5)', yoyo: true, repeat: 1}", "power2.out")
    shine(f"#{v}", t + .4, .5)
    sfx("whoosh" if key == "openers" else "swish", t - .05)
    sfx("pop", t + .35)
tilt("#vcard", T("w04", "use"), SF, 4, 1.0)
head_out("he2", SF - .28)

# ============================================================================================================================
# F (light): the script writes itself; its first line glows with its source tag
SCRIPT = [("hk", "HOOK", ["Nobody talks about this…"]), ("st", "STORY", ["My best hook was buried at 0:34.", "Viewers decide in three seconds."]),
          ("ct", "CTA", ["Save this for your next edit."])]
STAG = '<div class="stag" id="stag"><i></i>from your reel 0:02</div>'
groups = "".join(f'<div class="sg" id="sg_{g}">{"<i class=mark id=mark></i>" if g == "hk" else ""}<u class="sgl">{lab}</u><div class="sls">'
                 + "".join(f'<p class="sl">{wsp(x)}</p>' for x in ls) + (STAG if g == "hk" else "") + "</div></div>" for g, lab, ls in SCRIPT)
HTML.append('<div class="scn" id="sf">')
head("hf1", [[("Then", ""), ("it", ""), ("wrote", "")], [("the", ""), ("script.", "it pk")]], 175, "w05", 92)
head("hf2", [[("It", ""), ("opened", ""), ("the", ""), ("way", "")], [("I", ""), ("always", "it pk"), ("open.", "")]], 175, "w05", 86,
     after=T("w05", "opened") - .3)
HTML.append("</div>")
HTML.append(f'<div class="scard glass" id="scard">{SH}<div class="sch"><img src="assets/img/creedom_logo.png"><span class="spill">@write-script</span>'
            f'<em>EXAMPLE SCRIPT</em></div><div class="sgs">{groups}</div></div>')
scene("sf", SF, SG)
zoom_through(SF)
mode(SF, False)
ft("#scard", SF + .02, .55, "{opacity: 0, y: 200, scale: .9, rotationX: 24, filter: 'blur(12px)'}", "{opacity: 1, y: 0, scale: 1, rotationX: 0, filter: 'blur(0px)'}", "back.out(1.3)")
shine("#scard", SF + .5)
t_wr = T("w05", "wrote")
words_on("#scard .sl span", t_wr, .07)
for k in range(14):
    sfx("tick", t_wr + .1 * k)
head_out("hf1", T("w05", "opened") - .35)
t_op = T("w05", "opened")
ft("#mark", t_op, .45, "{scaleX: 0}", "{scaleX: 1}", "power3.out")
ft("#sg_hk .sl", t_op + .1, .3, "{color: '#0B0B0B'}", "{color: '#C2185B'}")
ft("#stag", t_op + .2, .45, "{opacity: 0, y: -20, scale: .6}", "{opacity: 1, y: 0, scale: 1}", "back.out(2.4)")
sfx("ding", t_op + .2)
punch(T("w05", "always"), 1.05)
tilt("#scard", SF + .8, SG - .1, 3, 1.1)
head_out("hf2", SG - .28)

# ============================================================================================================================
# G: real footage behind; the card splits into HOOK / STORY / CTA, then shrinks into the teleprompter on the phone
TP = ["Nobody talks about this…", "My best hook was buried at 0:34.", "Viewers decide in three seconds.", "Save this for your next edit.",
      "Comment SCRIPT for the link."]
tp_lines = "".join(f'<p class="tp{" on" if i == 0 else ""}">{x}</p>' for i, x in enumerate(TP))
HTML.append('<div class="scn" id="sg"><video class="foot" id="v2" src="assets/video/7234061.mp4" '
            f'data-start="{SG - .05:.3f}" data-duration="{SX - SG + .15:.3f}" data-media-start="1.0" data-track-index="2" muted playsinline></video>'
            '<div class="topfade"></div><div class="footdim" id="footdim"></div>'
            f'<div class="tphone" id="tphone"><div class="tscr"><div class="tpbar"><i></i>TELEPROMPTER</div><div class="tpw" id="tpw">{tp_lines}</div></div></div>')
head("hg", [[("In", ""), ("my", "it pk"), ("words.", "")]], 190, "w06", 110, dark=True)
HTML.append("</div>")
scene("sg", SG, SX)
liquid(SG)
st("#footdim", SG, "{opacity: 1}")
to("#scard", SG - .1, .4, "{y: 120}", "power2.inOut")
for g, key, dy in (("hk", "Hook", 0), ("st", "story", 40), ("ct", "call", 80)):
    t = T("w06", key) - .05
    if dy:
        to(f"#sg_{g}", t, .35, "{marginTop: 22}", "back.out(2)")
    ft(f"#sg_{g} .sgl", t, .35, "{opacity: 0, scale: .4, x: -30}", "{opacity: 1, scale: 1, x: 0}", "back.out(2.6)")
    to(f"#sg_{g}", t, .3, "{background: 'rgba(255,255,255,.92)', boxShadow: '0 20px 50px rgba(120,20,60,.25)'}")
    sfx("pop", t)
    punch(t + .02, 1.03)
to("#scard", T_IN - .25, .4, "{x: 230, y: 380, scale: .3, opacity: 0, filter: 'blur(8px)'}", "power3.in")
sfx("whoosh", T_IN - .25)
to("#footdim", T_IN - .1, .5, "{opacity: 0}")
ft("#tphone", T_IN - .12, .5, "{opacity: 0, scale: .7, y: 60}", "{opacity: 1, scale: 1, y: 0}", "back.out(1.6)")
ft("#tpw", T_IN, SX - T_IN + .1, "{y: 0}", "{y: -150}", "none")
punch(T("w06", "my"), 1.05)

# ============================================================================================================================
# H (dark): CTA
HTML.append(f'<div class="scn" id="scta"><div class="dm glass dkg" id="dm">{SH}<img src="assets/img/creedom_logo.png"><div><b>Creedom</b><span>sent you the link</span></div><em>now</em></div>'
            '<div class="cm" id="cmh">Comment</div><div class="kw" id="kw">SCRIPT</div>'
            f'<div class="cbox glass dkg" id="cbox">{SH}<i></i><span class="ph" id="cph">Add a comment…</span>' + chars("ctx", "SCRIPT", "ctx") +
            '<b id="csend">&#10148;</b></div><div class="sub" id="sub">and I\'ll DM you the <i>link.</i></div></div>')
scene("scta", SX, DUR + 1)
whip(SX)
mode(SX, True)
for b in ("#tphone", "#scard"):
    st(b, SX, "{opacity: 0}")
t_c = T("w07", "Comment")
ft("#cmh", t_c - .05, .5, "{opacity: 0, filter: 'blur(14px)', y: 30}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
t_k = T("w07", "Script")
ft("#kw", t_k - .1, .8, "{opacity: 0, scale: 1.6, scaleX: 1.9, filter: 'blur(24px)'}", "{opacity: 1, scale: 1, scaleX: 1, filter: 'blur(0px)'}", "back.out(1.4)")
sfx("impact", t_k)
sfx("thump", t_k)
punch(t_k, 1.08)
ft("#cbox", t_k + .3, .5, "{opacity: 0, y: 60, filter: 'blur(10px)'}", "{opacity: 1, y: 0, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#cbox", t_k + .55)
t_ty2 = t_k + .55
st("#cph", t_ty2, "{opacity: 0}")
type_on("ctx", t_ty2, .45, 6, tick=False)
for k in range(6):
    sfx("tick", t_ty2 + .075 * k)
to("#csend", t_ty2 + .5, .12, "{scale: 1.3}")
to("#csend", t_ty2 + .62, .15, "{scale: 1}")
sfx("click", t_ty2 + .5)
ft("#sub", T("w07", "DM") - .1, .5, "{opacity: 0, filter: 'blur(12px)', y: 20}", "{opacity: 1, filter: 'blur(0px)', y: 0}", "power3.out")
t_dm = T("w07", "link")
ft("#dm", t_dm - .1, .7, "{opacity: 0, y: -160, scale: .9, filter: 'blur(12px)'}", "{opacity: 1, y: 0, scale: 1, filter: 'blur(0px)'}", "back.out(1.4)")
shine("#dm", t_dm + .35)
sfx("notify", t_dm)
tilt("#cbox", t_ty2 + .8, DUR, 4, 1.0)

# ============================================================================================================================
# Cree the mascot
HTML.append(cree_html())
A2_POS = P(890, 1350, .46)
B_POS = P(540, 1560, .5)
C_IN, C_POS = P(1260, 1430, .5), P(990, 1430, .5)
D_POS = P(905, 1600, .42)
E_POS = P(930, 1600, .38)
F_POS = P(900, 1590, .44)
H_POS = P(540, 1540, .52)
js(f'tl.set("#cree", {{x: {1260 - PCX}, y: {A2_POS[1] - PCY:.0f}, scale: {A2_POS[2]}, opacity: 0}}, 0);')
st("#cree", SA2, "{opacity: 1}")
js(f'tl.fromTo("#creep", {{y: 0}}, {{y: -9, duration: .8, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / .8)}, immediateRender: false}}, 0);')
js(f'tl.fromTo("#creeb", {{scaleY: 1}}, {{scaleY: 1.015, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: {int(DUR / 1.1)}, immediateRender: false}}, 0);')
# A2: walks in, droops at "nothing", a "?" by his head
cree_walk(SA2, SA2 + .45, (1260, A2_POS[1], A2_POS[2]), A2_POS, end="stand", end_flip=True)
pose(t_no - .05, "sad")
say(t_no + .05, "?", .8, left=True)
sweat(t_no + .2, .8)
# B: centre under the card; thinks at "asked", shock at the stamp
cree_walk(SB - .2, SB + .35, A2_POS, B_POS, end="stand")
pose(t_as - .05, "think")
cree_tilt(t_as, -8)
pose(T("w01", "sounded") - .05, "stand")
cree_tilt(T("w01", "sounded"), 0)
pose(t_li + .15, "shock")
cree_hop(t_li + .2, 60)
say(t_li + .25, "!", .7)
sweat(t_li + .3, .8)
pose(t_li + .8, "sad")
# C: peeks in from the right with his magnifier
st("#cree", SC - .05, "{opacity: 0}")
cree_to(SC - .05, *C_IN, d=.01)
st("#cree", SC + .2, "{opacity: 1}")
pose(SC + .2, "mag", flip=True)
cree_to(SC + .2, *C_POS, d=.55, ease="back.out(1.6)")
sfx("swish", SC + .2)
js(f'tl.fromTo("#creef", {{rotation: 0}}, {{rotation: 8, duration: .45, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, {SC + .8:.3f});')
pose(T("w02", "reels") - .05, "think", flip=True)
say(T("w02", "reels"), "?", .6, left=True)
# D: under the app; types on his phone, cheers when the pill snaps
cree_walk(SD - .3, SD + .3, C_POS, D_POS, end="stand", end_flip=True)
pose(t_ty - .05, "phone", flip=True)
pose(t_snap - .05, "cheer")
cree_hop(t_snap, 90)
sparkle(t_snap + .05, .9)
# E: reads with his magnifier, thinks at "pauses", proud at "use"
cree_to(SE - .2, *E_POS, d=.4)
pose(t_rd - .05, "mag", flip=True)
js(f'tl.fromTo("#creef", {{y: 0}}, {{y: -24, duration: .4, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, {t_rd + .1:.3f});')
pose(T("w04", "pauses") - .05, "think")
pose(T("w04", "use") - .05, "proud")
cree_wiggle(T("w04", "use"), 2, 5)
# F: points at the glowing first line, cheers at "always"
cree_to(SF - .2, *F_POS, d=.4)
pose(SF + .1, "stand")
pose(t_op - .05, "point", flip=True)
cree_tilt(t_op, 10)
cree_tilt(T("w05", "always") - .1, 0, .15)
pose(T("w05", "always") - .05, "cheer")
cree_hop(T("w05", "always"), 90)
sparkle(T("w05", "always") + .05, .9, -140)
# G: off stage (the footage carries it); H: back centre stage
st("#cree", SG, "{opacity: 0}")
cree_to(SX - .05, *H_POS, d=.01)
st("#cree", SX + .15, "{opacity: 1}")
pose(SX + .15, "wave")
cree_hop(SX + .15, 70)
pose(t_k - .05, "cheer")
cree_hop(t_k, 90)
pose(t_ty2 - .1, "phone")
pose(t_dm - .05, "point", flip=True)
cree_wiggle(t_dm + .1, 3, 6)
pose(DUR - .6, "proud")
for t in (2.9, 5.2, 9.1, 11.6, 15.9, 19.0, 24.9):
    blink(t)

# ---- fluid blobs and drifting glass panes ------------------------------------------------------------------------------------
LB = [(-200, -150, 760, "rgba(238,104,139,.55)"), (520, 260, 820, "rgba(255,190,214,.75)"), (-260, 980, 900, "rgba(217,194,255,.6)"),
      (480, 1280, 820, "rgba(255,216,194,.6)")]
DB = [(-220, -120, 800, "rgba(177,71,107,.55)"), (480, 900, 900, "rgba(243,67,162,.38)"), (-200, 1300, 760, "rgba(120,40,200,.35)")]
blobs_l = "".join(f'<i class="bl" id="lb{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(LB))
blobs_d = "".join(f'<i class="bl" id="db{i}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>' for i, (x, y, s, c) in enumerate(DB))
for pre, n in (("lb", len(LB)), ("db", len(DB))):
    for i in range(n):
        js(f'tl.fromTo("#{pre}{i}", {{x: 0, y: 0, scale: 1}}, {{x: {random.randint(-260, 260)}, y: {random.randint(-260, 260)}, scale: {random.uniform(.8, 1.35):.2f}, '
           f'duration: {DUR / 3:.2f}, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false}}, 0);')
PANES = [(-300, 330, 560, 340, -18), (830, 1500, 600, 360, 16), (690, -170, 520, 300, 24), (-330, 1560, 600, 320, -10)]
panes = "".join(f'<i class="pane" id="pn{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>' for i, (x, y, w, h, r) in enumerate(PANES))
for i, (x, y, w, h, r) in enumerate(PANES):
    js(f'tl.fromTo("#pn{i}", {{rotation: {r}, x: 0, y: 0}}, {{rotation: {r + random.choice((-1, 1)) * random.randint(8, 14)}, x: {random.randint(-80, 80)}, '
       f'y: {random.randint(-160, 160)}, duration: {DUR / 4:.2f}, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, 0);')

CSS = open(os.path.join(ROOT, "build", "style.css")).read().replace("$PINK", PINK).replace("$MAG", MAG).replace("$ROSE", ROSE).replace("$INK", INK).replace("$RED", RED)

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Creedom: @write-script 9x16</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-fps="30" data-width="1080" data-height="1920">
      <div class="world" id="light">{blobs_l}</div>
      <div class="world" id="dark">{blobs_d}</div>
      <div id="panes">{panes}</div>
      <div id="cam"><div id="punch"><div id="drift">
        {chr(10).join(HTML)}
      </div></div></div>
      <div id="flash"></div><div id="stk0" class="stk"></div><div id="stk1" class="stk"></div><div id="stk2" class="stk"></div>
      <div id="liq"></div><div id="sweep"></div><div id="grain"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true}});
      tl.set("#sweep", {{xPercent: -170}}, 0);
      tl.set("#liq", {{scale: .04}}, 0);
      tl.set(".stk", {{rotation: -24, xPercent: -260}}, 0);
      tl.set(".sh, #ash", {{skewX: -18, xPercent: -160}}, 0);
      {chr(10).join("      " + j for j in JS).strip()}
      tl.set({{}}, {{}}, {DUR:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w").write(html)
SFX.sort(key=lambda e: e["t"])
json.dump(SFX, open(os.path.join(ROOT, "plan", "sfx_events.json"), "w"), indent=0)
json.dump({"dur": DUR, "scenes": {"hook": [SA, SB], "generic": [SB, SC], "never": [SC, SD], "type": [SD, SE], "read": [SE, SF],
                                  "write": [SF, SG], "blocks": [SG, SX], "cta": [SX, DUR]}},
          open(os.path.join(ROOT, "plan", "edit.json"), "w"), indent=1)
print(f"wrote index.html: {DUR:.2f} s, {len(JS)} timeline lines, {len(SFX)} sfx; cuts {[round(x, 2) for x in (SA2, SB, SC, SD, SE, SF, SG, SX)]}")
