"""Writes the Nxtlvl SaaS film (v2, After Effects-style polish): index.html + five scene files.
Run from anywhere: python3 tools/gen.py. Everything is deterministic (no random at render time)."""
import json, os, math
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = json.load(open(P + '/assets/icons.json'))
ROCKET = open(P + '/assets/rocket.svg.txt').read()
WORD = open(P + '/assets/wordmark.svg.txt').read()


def icon(k, size=34, col=None):
    b = ICONS[k]
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="{col or "#" + b["hex"]}" aria-hidden="true"><path d="{b["d"]}"/></svg>'


FONTS = '''@font-face { font-family: "Bricolage Grotesque"; src: url("assets/fonts/bricolage-variable.woff2") format("woff2"); font-weight: 200 800; }
@font-face { font-family: "Geist"; src: url("assets/fonts/geist-variable.woff2") format("woff2"); font-weight: 100 900; }
@font-face { font-family: "Geist Mono"; src: url("assets/fonts/geist-mono-variable.woff2") format("woff2"); font-weight: 100 900; }'''
BASE = FONTS + '''
#root { position: absolute; inset: 0; overflow: hidden; font-family: "Geist", sans-serif; color: #F4EFFF; }
.title { position: absolute; left: 150px; margin: 0; font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 84px; line-height: 1.02; letter-spacing: -0.03em; white-space: nowrap; }
.ln { display: block; overflow: hidden; padding: 0 0.04em 0.12em; margin-bottom: -0.12em; }
.ln > span { display: inline-block; will-change: transform; }
.acc { color: #B98AFF; }
.panel { position: absolute; background: #130C28; border: 1px solid rgba(216, 187, 255, .16); border-radius: 30px; box-shadow: 0 50px 120px -40px rgba(94, 6, 242, .65), 0 0 0 1px rgba(0, 0, 0, .3); }
.mono { font-family: "Geist Mono", monospace; }
.cursor { position: absolute; left: 0; top: 0; width: 70px; height: 70px; z-index: 50; filter: drop-shadow(0 10px 16px rgba(0, 0, 0, .55)); }
.spark { position: absolute; width: 26px; height: 26px; background: #D8BBFF; clip-path: polygon(50% 0, 62% 38%, 100% 50%, 62% 62%, 50% 100%, 38% 62%, 0 50%, 38% 38%); }
'''
CURSOR = '<svg class="cursor" id="{id}" viewBox="0 0 24 24"><path d="M4 2.5l15 8.6-6.4 1.6 3.9 6.9-2.9 1.6-3.9-6.9L4.6 18.9z" fill="#fff" stroke="#140B2E" stroke-width="1.2" stroke-linejoin="round"/></svg>'
TICK = '<svg viewBox="0 0 18 12" width="26" height="17"><path d="M1 6.5l3 3L10 2.5M7 9.5l1 1L16.5 2" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHK = '<svg viewBox="0 0 24 24" width="28" height="28"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#052b1c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def lines(rows):
    """rows: list of lists of (word, accent?) -> masked lines for a rise-up text animator"""
    out = []
    for row in rows:
        out.append('<span class="ln">' + ' '.join(f'<span class="{"acc" if a else ""}">{w}</span>' for w, a in row) + '</span>')
    return ''.join(out)


def scene(cid, css, body, js):
    return f'''<template>
  <style>
{BASE}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const rise = (sel, at, each = 0.06) => tl.fromTo(sel, {{ yPercent: 115, rotation: 4 }}, {{ yPercent: 0, rotation: 0, duration: 0.7, stagger: each, ease: "expo.out" }}, at);
    const fall = (sel, at) => tl.to(sel, {{ yPercent: -115, duration: 0.32, stagger: 0.03, ease: "power3.in" }}, at);
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''


# ================================================================ 1. hook (0-4.6 s)
TOASTS = [('instagram', 'Instagram', 'Price for 2 people?', 240), ('whatsapp', 'WhatsApp', 'Table for 4 at 8 tonight?', 400), ('meta', 'Meta lead ad', 'Interested in the brunch offer', 560), ('instagram', 'Instagram', 'Do you deliver to Baner?', 720)]
toasts = ''.join(f'''<div class="toast" id="hk-n{i}" style="top:{y}px"><span class="tic">{icon(k, 36)}</span><div class="tx"><b>{src}</b><span>{msg}</span></div>
  <span class="st mono"><em class="w8">now</em><em class="ok">{CHK.replace('width="28" height="28"', 'width="20" height="20"')} Replied</em></span></div>''' for i, (k, src, msg, y) in enumerate(TOASTS))
burst = ''.join(f'<i class="ray" style="transform:rotate({a}deg)"></i>' for a in range(0, 360, 30))
hook_css = '''
#hk-clock { position: absolute; left: 150px; top: 150px; z-index: 2; font-family: "Geist Mono", monospace; font-size: 34px; color: #BDB2DC; display: flex; align-items: center; gap: 14px; }
#hk-clock i { width: 12px; height: 12px; border-radius: 50%; background: #FF5A7A; box-shadow: 0 0 0 6px rgba(255, 90, 122, .18); }
#hk-unread { margin-left: 10px; padding: 4px 14px; border-radius: 99px; background: #FF5A7A; color: #fff; font-size: 26px; font-weight: 600; }
#hk-unread.zero { background: #4ADE9E; color: #052b1c; }
#hk-t1 { top: 220px; } #hk-t2 { top: 220px; }
.digit { display: inline-block; height: 0.98em; overflow: hidden; vertical-align: top; } .digit > span { display: flex; flex-direction: column; } .digit b { display: block; height: 0.98em; font-weight: 800; color: #C9A4FF; -webkit-text-fill-color: #C9A4FF; }
.toast { position: absolute; left: 1080px; width: 690px; height: 132px; display: flex; align-items: center; gap: 20px; padding: 0 26px; border-radius: 26px; background: rgba(26, 17, 53, .92); border: 1px solid rgba(216, 187, 255, .18);
  box-shadow: 0 30px 60px -30px rgba(0, 0, 0, .8); }
.tic { width: 70px; height: 70px; border-radius: 20px; display: grid; place-items: center; background: rgba(216, 187, 255, .07); flex: none; }
.tx { flex: 1; min-width: 0; } .tx b { display: block; font-size: 26px; color: #BDB2DC; font-weight: 500; } .tx span { display: block; font-size: 33px; font-weight: 600; white-space: nowrap; }
.st { position: relative; width: 150px; height: 40px; font-size: 24px; } .st em { position: absolute; right: 0; top: 0; font-style: normal; display: flex; align-items: center; gap: 6px; height: 40px; }
.st .w8 { color: #8E84B4; } .st .ok { color: #052b1c; background: #4ADE9E; padding: 0 14px; border-radius: 99px; font-weight: 600; opacity: 0; }
#hk-sub { position: absolute; left: 154px; top: 640px; font-size: 34px; color: #BDB2DC; }
#hk-nx { position: absolute; left: 640px; top: 560px; width: 340px; height: auto; filter: drop-shadow(0 30px 30px rgba(94, 6, 242, .5)); z-index: 5; }
#hk-burst { position: absolute; left: 810px; top: 760px; width: 0; height: 0; z-index: 4; opacity: 0; }
#hk-burst .ray { position: absolute; left: -2px; top: -170px; width: 4px; height: 70px; border-radius: 4px; background: linear-gradient(#FFFFFF, rgba(169, 92, 255, 0)); transform-origin: 2px 170px; }
#hk-ring { position: absolute; left: 810px; top: 760px; width: 300px; height: 300px; margin: -150px 0 0 -150px; border-radius: 50%; border: 3px solid #B98AFF; z-index: 4; opacity: 0; }
'''
d4 = '<span class="digit"><span>' + ''.join(f'<b>{n}</b>' for n in [9, 8, 7, 6, 5, 4]) + '</span></span>'
hook_body = f'''    <div id="hk-clock" data-motion-blur="off"><i></i><span>11:42 pm · Café Aroma</span><span id="hk-unread"><b id="hk-un">1</b> unread</span></div>
    <h1 id="hk-t1" class="title" data-motion-blur="off">{lines([[("Customers", False)], [("are", False), ("waiting.", True)]])}</h1>
    <h1 id="hk-t2" class="title" data-motion-blur="off"><span class="ln"><span>Answered</span></span><span class="ln"><span>in</span> <span>{d4}</span> <span class="acc">seconds.</span></span></h1>
    <p id="hk-sub">Your AI team replies day and night.</p>
    {toasts}
    <div id="hk-ring"></div><div id="hk-burst">{burst}</div>
    <img id="hk-nx" src="assets/img/mascot.webp" alt="Nextyy waving">'''
hook_js = '''
    // frame 0: the clock and the first message are already there (the poster frame)
    tl.fromTo("#hk-clock i", { scale: 1 }, { scale: 1.35, duration: 0.25, ease: "power1.inOut", yoyo: true, repeat: 5 }, 0);
    rise("#hk-t1 .ln > span", 0.1, 0.09);
    const T = ["#hk-n0", "#hk-n1", "#hk-n2", "#hk-n3"];
    tl.fromTo(T[0], { x: 0, opacity: 1 }, { x: 0, opacity: 1, duration: 0.01 }, 0);
    T.slice(1).forEach((t, i) => tl.fromTo(t, { x: 820, rotation: 6, opacity: 0 }, { x: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(1.4)" }, 0.35 + i * 0.28));
    // the unread count climbs with every message, then drops to zero as they are answered
    const un = { v: 1 }, unEl = document.querySelector("#hk-un");
    tl.fromTo(un, { v: 1 }, { v: 4, duration: 0.9, ease: "steps(3)", onUpdate: () => { unEl.textContent = Math.round(un.v); } }, 0.4);
    const un2 = { v: 4 };
    tl.fromTo(un2, { v: 4 }, { v: 0, duration: 0.75, ease: "steps(4)", immediateRender: false, onUpdate: () => { unEl.textContent = Math.round(un2.v); } }, 1.95);
    tl.fromTo("#hk-unread", { backgroundColor: "#FF5A7A", color: "#ffffff" }, { backgroundColor: "#4ADE9E", color: "#052b1c", duration: 0.2, ease: "none" }, 2.7);
    // the stack buzzes like a phone
    tl.fromTo(".toast", { y: 0 }, { y: -6, duration: 0.05, ease: "none", yoyo: true, repeat: 7 }, 1.25);
    // Nextyy bursts in
    tl.fromTo("#hk-ring", { scale: 0.2, opacity: 1 }, { scale: 2.2, opacity: 0, duration: 0.7, ease: "expo.out", immediateRender: false }, 1.55);
    tl.fromTo("#hk-burst", { opacity: 1 }, { opacity: 1, duration: 0.6, immediateRender: false }, 1.55);
    tl.to("#hk-burst", { opacity: 0, duration: 0.01 }, 2.16);
    tl.fromTo("#hk-burst .ray", { scaleY: 0.2, opacity: 1 }, { scaleY: 1.4, opacity: 0, duration: 0.6, ease: "expo.out", immediateRender: false }, 1.55);
    tl.fromTo("#hk-nx", { opacity: 0, y: 220, scale: 0.4, rotation: -14 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.8, ease: "back.out(1.8)" }, 1.5);
    tl.to("#hk-nx", { rotation: 7, duration: 0.2, ease: "power1.inOut", yoyo: true, repeat: 3 }, 2.35);
    // every message gets answered, one after another
    T.forEach((t, i) => { tl.to(t + " .w8", { opacity: 0, duration: 0.12, ease: "none" }, 1.95 + i * 0.18); tl.fromTo(t + " .ok", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 1.95 + i * 0.18);
      tl.fromTo(t, { borderColor: "rgba(216,187,255,0.18)" }, { borderColor: "rgba(74,222,158,0.5)", duration: 0.3, ease: "none" }, 1.95 + i * 0.18); });
    // the line changes: text animator out, new line in, the 4 rolls like a slot machine
    fall("#hk-t1 .ln > span", 2.2);
    tl.fromTo("#hk-t2", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 2.44);
    rise("#hk-t2 .ln > span", 2.45, 0.08);
    tl.fromTo("#hk-t2 .digit > span", { yPercent: 0 }, { yPercent: -83.333, duration: 0.9, ease: "power3.out" }, 2.55);
    tl.fromTo("#hk-sub", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }, 2.55);
    // hand-off: Nextyy flies (with motion blur) into the agent app's pin; the rest pushes away
    tl.to("#hk-nx", { x: -580, y: -425, scale: 0.25, rotation: -10, duration: 0.55, ease: "power3.inOut" }, 3.95);
    tl.to(".toast", { x: 900, opacity: 0, duration: 0.4, stagger: 0.04, ease: "power3.in" }, 3.95);
    fall("#hk-t2 .ln > span", 4.0);
    tl.to(["#hk-sub", "#hk-clock"], { opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }, 4.05);
'''

# ================================================================ 2. agents (4.6-10.4 s, 5.8 s)
AG = [('content', 'Content Agent', '3 hooks ready for Friday'), ('reply', 'Reply Agent', '47 messages answered'), ('ads', 'Ads Agent', 'Creative B is 38% cheaper'),
      ('edit', 'Edit Agent', 'Reel v2 ready: 0:28'), ('seo', 'SEO Agent', '#1 for "best café in Baner"'), ('report', 'Report Agent', 'November report ready')]
rows = ''.join(f'<div class="row" id="ag-r{i}"><img src="assets/img/agent-{k}.webp" alt=""><div><b>{n}</b><small>{p}</small><span class="bar"><i></i></span></div><i class="dot"></i></div>' for i, (k, n, p) in enumerate(AG))
SP = '<svg viewBox="0 0 16 16" width="26" height="26"><circle class="ring" cx="8" cy="8" r="6" fill="none" stroke="#4ADE9E" stroke-width="1.6"/><path class="ck" d="M4.5 8.2l2.3 2.3 4.7-4.9" fill="none" stroke="#4ADE9E" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
chips = ''.join(f'<span class="stp" id="ag-s{i}">{SP}{t}</span>' for i, t in enumerate(['Pulled Meta ads data', 'Compared cost per lead', 'Found the winner']))
ag_css = '''
#ag-cam { position: absolute; inset: 0; transform-origin: 50% 60%; }
#ag-t { top: 92px; }
#ag-app { left: 160px; top: 236px; width: 1600px; height: 790px; overflow: hidden; display: grid; grid-template-columns: 480px 1fr; transform-origin: 50% 0; }
.side { position: relative; background: linear-gradient(180deg, #160E2E, #0F0920); border-right: 1px solid rgba(216, 187, 255, .1); padding: 16px 18px 24px; }
.exl { display: block; padding: 0 10px 10px; font-size: 22px; color: #8E84B4; }
.row .bar { display: block; width: 210px; height: 5px; margin-top: 7px; border-radius: 5px; background: rgba(216, 187, 255, .1); overflow: hidden; } .row .bar i { display: block; height: 100%; width: 100%; border-radius: 5px; background: linear-gradient(90deg, #7D18FC, #B46CFF); transform-origin: 0 50%; }
.pin { display: flex; align-items: center; gap: 16px; padding: 4px 10px 22px; } .pin span { width: 84px; height: 84px; }
.pin b { font-size: 30px; font-weight: 650; } .pin small { display: block; font-size: 23px; color: #8E84B4; }
.row { position: relative; display: flex; align-items: center; gap: 18px; padding: 8px 14px; border-radius: 18px; margin-bottom: 4px; height: 96px; z-index: 1; }
.row img { width: 66px; height: 66px; border-radius: 16px; background: #1A1135; }
.row b { display: block; font-size: 29px; font-weight: 600; } .row small { font-size: 23px; color: #8E84B4; white-space: nowrap; }
.row .dot { position: absolute; right: 16px; top: 50%; width: 11px; height: 11px; margin-top: -5px; border-radius: 50%; background: #4ADE9E; }
#ag-hi { position: absolute; left: 18px; top: 169px; width: 444px; height: 96px; border-radius: 18px; background: #2A1B55; box-shadow: inset 0 0 0 2px rgba(169, 92, 255, .6), 0 10px 30px -10px rgba(125, 24, 252, .8); }
.main { position: relative; padding: 30px 40px; }
.mh { display: flex; align-items: center; gap: 18px; padding-bottom: 24px; border-bottom: 1px solid rgba(216, 187, 255, .1); }
.mh img { width: 72px; height: 72px; } .mh b { font-size: 34px; font-weight: 650; } .mh small { display: block; font-size: 23px; color: #8E84B4; }
.mh .state { margin-left: auto; padding: 8px 18px; border-radius: 99px; background: rgba(74, 222, 158, .12); color: #4ADE9E; font-size: 23px; }
.steps { position: absolute; left: 40px; top: 190px; display: flex; gap: 12px; flex-wrap: wrap; width: 1010px; }
.stp { display: inline-flex; align-items: center; gap: 10px; padding: 12px 20px 12px 14px; border-radius: 99px; border: 1px solid rgba(74, 222, 158, .28); background: rgba(74, 222, 158, .06); font-size: 25px; color: #D6CEF0; }
#ag-msg { position: absolute; left: 40px; top: 290px; width: 880px; padding: 26px 30px; border-radius: 28px; border-top-left-radius: 8px; background: #231745; font-size: 33px; line-height: 1.4; }
#ag-you { position: absolute; right: 40px; top: 476px; padding: 18px 34px; border-radius: 99px; background: linear-gradient(100deg, #5E06F2, #7D18FC 45%, #B46CFF); font-size: 30px; font-weight: 600; color: #fff; box-shadow: 0 18px 40px -16px rgba(125, 24, 252, .9); }
#ag-rc { position: absolute; left: 40px; top: 580px; display: flex; align-items: center; gap: 18px; padding: 22px 28px; border-radius: 22px; background: rgba(74, 222, 158, .1); border: 1.5px solid rgba(74, 222, 158, .4); color: #B8F5D6; font-size: 32px; font-weight: 650; transform-origin: 20% 50%; }
#ag-rc i { width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; background: #4ADE9E; font-style: normal; }
#ag-nx { position: absolute; left: 188px; top: 299px; width: 84px; height: 84px; z-index: 3; }
'''
ag_body = f'''    <div id="ag-cam">
    <h1 id="ag-t" class="title" data-motion-blur="off">{lines([[("Six", True), ("AI", True), ("agents", True), ("work", False), ("your", False), ("brand", False), ("every", False), ("day.", False)]])}</h1>
    <div id="ag-app" class="panel">
      <div class="side"><span class="exl mono">Example workspace · Café Aroma</span><div class="pin"><span></span><div><b>Nextyy</b><small>your team lead</small></div></div><div id="ag-hi"></div>{rows}</div>
      <div class="main"><div class="mh"><img src="assets/img/agent-ads.webp" alt=""><div><b>Ads Agent</b><small>Watches Meta and Google campaigns daily</small></div><span class="state mono">Optimising</span></div>
        <div class="steps">{chips}</div>
        <div id="ag-msg">Creative B gets leads 38% cheaper. Move ₹2,000 to it?</div>
        <div id="ag-you">Yes, move it</div>
        <div id="ag-rc"><i>{CHK}</i><span>₹<b id="ag-amt">0</b> moved · Creative A → B</span></div></div>
    </div>
    <img id="ag-nx" src="assets/img/pin-nextyy.webp" alt="">
    </div>
    {CURSOR.format(id="ag-cur")}'''
ag_js = '''
    // 3D layer entrance and a slow camera push through the scene
    tl.fromTo("#ag-app", { opacity: 0, rotationX: 22, y: 120, scale: 0.9, transformPerspective: 1600, filter: "blur(10px)" }, { opacity: 1, rotationX: 0, y: 0, scale: 1, filter: "blur(0px)", duration: 0.9, ease: "expo.out" }, 0);
    tl.fromTo("#ag-cam", { scale: 1 }, { scale: 1.035, duration: 5.8, ease: "none" }, 0);
    rise("#ag-t .ln > span", 0.15);
    tl.fromTo(".row", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.5, stagger: 0.05, ease: "expo.out" }, 0.3);
    tl.fromTo(".row .dot", { scale: 0 }, { scale: 1, duration: 0.3, stagger: 0.05, ease: "back.out(3)" }, 0.6);
    [0.35, 0.8, 0.55, 0.9, 0.45, 0.7].forEach((v, i) => tl.fromTo("#ag-r" + i + " .bar i", { scaleX: 0 }, { scaleX: v, duration: 1.4 + i * 0.15, ease: "power2.out" }, 0.7 + i * 0.05));
    tl.fromTo(".main > *", { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
    // the cursor clicks the Ads Agent, which causes the selection
    tl.fromTo("#ag-cur", { x: 1500, y: 1150 }, { x: 330, y: 470, duration: 0.8, ease: "power3.inOut" }, 0.7);
    tl.to("#ag-cur", { scale: 0.82, duration: 0.08, ease: "power2.in", yoyo: true, repeat: 1 }, 1.5);
    tl.to("#ag-hi", { y: 200, duration: 0.35, ease: "power3.out" }, 1.56);
    tl.to("#ag-r2", { scale: 1.03, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, 1.56);
    tl.fromTo(".main .mh", { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.5, ease: "expo.out" }, 1.7);
    [0, 1, 2].forEach(i => { tl.fromTo("#ag-s" + i, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 1.95 + i * 0.28);
      tl.fromTo("#ag-s" + i + " .ck", { strokeDasharray: 12, strokeDashoffset: 12 }, { strokeDashoffset: 0, duration: 0.25, ease: "power2.out" }, 2.15 + i * 0.28); });
    tl.fromTo("#ag-msg", { opacity: 0, y: 26, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "expo.out" }, 2.8);
    tl.fromTo("#ag-you", { opacity: 0, y: 20, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 3.1);
    tl.to("#ag-cur", { x: 1600, y: 760, duration: 0.6, ease: "power3.inOut" }, 3.2);
    tl.to("#ag-cur", { scale: 0.82, duration: 0.08, ease: "power2.in", yoyo: true, repeat: 1 }, 3.85);
    tl.to("#ag-you", { scale: 0.94, duration: 0.08, ease: "power2.in", yoyo: true, repeat: 1 }, 3.85);
    tl.fromTo("#ag-rc", { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.7)" }, 4.0);
    const amt = { v: 0 }, el = document.querySelector("#ag-amt");
    tl.fromTo(amt, { v: 0 }, { v: 2000, duration: 0.7, ease: "power3.out", onUpdate: () => { el.textContent = Math.round(amt.v).toLocaleString("en-IN"); } }, 4.05);
    tl.to("#ag-cur", { x: 1900, y: 1200, duration: 0.5, ease: "power3.in" }, 4.4);
    // hand-off: zoom through the receipt
    tl.to("#ag-rc", { scale: 3.2, x: 420, y: -40, duration: 0.4, ease: "power3.in" }, 5.4);
    tl.to(["#ag-app", "#ag-t", "#ag-nx"], { opacity: 0, filter: "blur(16px)", duration: 0.3, ease: "power3.in" }, 5.45);
    tl.to("#ag-rc", { opacity: 0, duration: 0.1, ease: "none" }, 5.7);
'''

# ================================================================ 3. automation (10.4-15.4 s, 5 s)
srcs = [('instagram', 'Instagram DM', 'Price? Timings?'), ('whatsapp', 'WhatsApp', 'Booking request'), ('meta', 'Meta lead ad', 'New lead · Rahul')]
outs = [('Replied in your voice', 'in 4 s, 24/7'), ('Lead qualified', 'budget, area, timeline'), ('Saved to CRM', 'owner told on WhatsApp')]
YS = [360, 540, 720]
src_html = ''.join(f'<div class="nd src" id="fl-s{i}" style="top:{y}px"><span class="ic">{icon(k, 38)}</span><div><b>{n}</b><small>{s}</small></div><span class="glow"></span></div>' for i, ((k, n, s), y) in enumerate(zip(srcs, YS)))
out_html = ''.join(f'<div class="nd out" id="fl-o{i}" style="top:{y}px"><span class="ic ok">{CHK}</span><div><b>{n}</b><small>{s}</small></div><span class="glow"></span></div>' for i, ((n, s), y) in enumerate(zip(outs, YS)))


def wire(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    return f'M{x1} {y1} C{mx} {y1} {mx} {y2} {x2} {y2}'


wires = ''.join(f'<path id="fl-w{i}" d="{wire(600, y + 64, 760, 620)}"/>' for i, y in enumerate(YS)) + ''.join(f'<path id="fl-v{i}" d="{wire(1160, 620, 1320, y + 64)}"/>' for i, y in enumerate(YS))
pulses = ''.join(f'<circle class="pulse" id="fl-p{i}" r="7"/>' for i in range(6))
fl_css = '''
#fl-cam { position: absolute; inset: 0; }
#fl-t { top: 100px; }
.nd { position: absolute; width: 440px; height: 128px; display: flex; align-items: center; gap: 20px; padding: 0 26px; background: #130C28; border: 1.5px solid rgba(216, 187, 255, .16); border-radius: 24px; box-shadow: 0 30px 60px -34px rgba(0, 0, 0, .8); }
.nd.src { left: 160px; } .nd.out { left: 1320px; }
.nd .ic { width: 66px; height: 66px; border-radius: 18px; display: grid; place-items: center; background: rgba(216, 187, 255, .06); flex: none; }
.nd .ic.ok { background: rgba(216, 187, 255, .08); } .nd .ic.ok svg { opacity: 0; }
.nd b { display: block; font-size: 30px; font-weight: 600; } .nd small { font-size: 25px; color: #8E84B4; }
.nd .glow { position: absolute; inset: -1.5px; border-radius: 24px; border: 2px solid #A95CFF; box-shadow: 0 0 0 7px rgba(125, 24, 252, .2), 0 20px 46px -16px rgba(125, 24, 252, 1); opacity: 0; }
.nd.out .glow { border-color: #4ADE9E; box-shadow: 0 0 0 7px rgba(74, 222, 158, .16), 0 20px 46px -16px rgba(74, 222, 158, .8); }
#fl-core { position: absolute; left: 760px; top: 470px; width: 400px; height: 300px; border-radius: 32px; background: linear-gradient(160deg, rgba(125, 24, 252, .55), #130C28 72%); border: 1.5px solid rgba(169, 92, 255, .6);
  display: grid; justify-items: center; align-content: center; gap: 10px; box-shadow: 0 30px 90px -30px rgba(125, 24, 252, .9); }
#fl-core img { width: 124px; height: 124px; } #fl-core b { font-size: 33px; font-weight: 650; } #fl-core small { font-size: 26px; color: #BDB2DC; }
#fl-cring { position: absolute; left: 960px; top: 620px; width: 420px; height: 420px; margin: -210px 0 0 -210px; border-radius: 50%; border: 3px solid #B98AFF; }
#fl-wires { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; }
#fl-wires path { fill: none; stroke: rgba(216, 187, 255, .32); stroke-width: 3; stroke-linecap: round; }
#fl-wires .pulse { fill: #FFFFFF; filter: drop-shadow(0 0 8px #B98AFF); opacity: 0; }
#fl-lead { position: absolute; left: 0; top: 0; display: flex; align-items: center; gap: 12px; padding: 14px 20px; border-radius: 16px; background: #7D18FC; color: #fff; font-size: 28px; font-weight: 600; box-shadow: 0 18px 40px -12px rgba(125, 24, 252, 1); white-space: nowrap; z-index: 6; }
.tag { position: absolute; padding: 8px 16px; border-radius: 12px; background: rgba(125, 24, 252, .18); border: 1px solid rgba(169, 92, 255, .45); font-size: 24px; color: #E4D3FF; white-space: nowrap; }
.wt { position: absolute; font-size: 22px; color: #8E84B4; }
#fl-count { position: absolute; left: 1320px; top: 240px; display: flex; align-items: center; gap: 14px; font-size: 26px; color: #BDB2DC; padding: 12px 24px; border-radius: 99px; background: rgba(19, 12, 40, .85); border: 1px solid rgba(216, 187, 255, .18); }
#fl-count b { color: #fff; font-size: 32px; font-weight: 600; font-variant-numeric: tabular-nums; } #fl-count i { width: 12px; height: 12px; border-radius: 50%; background: #4ADE9E; }
'''
fl_body = f'''    <div id="fl-cam">
    <h1 id="fl-t" class="title" data-motion-blur="off">{lines([[("Every", False), ("lead", True), ("answered,", False), ("qualified", False), ("and", False), ("saved.", False)]])}</h1>
    <svg id="fl-wires" viewBox="0 0 1920 1080">{wires}{pulses}</svg>
    {src_html}
    <div id="fl-cring"></div>
    <div id="fl-core"><img src="assets/img/pin-nextyy.webp" alt=""><b>Nxtlvl Agent</b><small class="mono">avg reply 0.8 s</small></div>
    {out_html}
    <div class="tag mono" id="fl-tg0" style="left:742px;top:800px">Intent: booking</div><div class="tag mono" id="fl-tg1" style="left:1016px;top:800px">Party: 4</div><div class="tag mono" id="fl-tg2" style="left:858px;top:858px">Tonight · 8 pm</div>
    <div class="wt mono" style="left:640px;top:520px">0.2 s</div><div class="wt mono" style="left:1196px;top:520px">0.6 s</div>
    <div id="fl-count" class="mono"><i></i>Handled today <b id="fl-n">1,284</b></div>
    <div id="fl-lead">{icon("whatsapp", 30, "#fff")}New lead · table for 4</div>
    </div>'''
fl_js = '''
    tl.fromTo("#fl-cam", { scale: 1.08, x: 40 }, { scale: 1, x: -20, duration: 4.7, ease: "power1.out" }, 0);
    rise("#fl-t .ln > span", 0.05, 0.05);
    tl.fromTo(".nd.src", { opacity: 0, x: -60, scale: 0.9 }, { opacity: 1, x: 0, scale: 1, duration: 0.6, stagger: 0.07, ease: "expo.out" }, 0.05);
    tl.fromTo("#fl-core", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(1.6)" }, 0.15);
    tl.fromTo(".nd.out", { opacity: 0, x: 60, scale: 0.9 }, { opacity: 1, x: 0, scale: 1, duration: 0.6, stagger: 0.07, ease: "expo.out" }, 0.25);
    tl.fromTo("#fl-count", { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 0.35);
    const paths = [...document.querySelectorAll("#fl-wires path")];
    paths.forEach((p, i) => { const L = p.getTotalLength(); tl.fromTo(p, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, 0.4 + (i % 3) * 0.06 + (i > 2 ? 0.25 : 0)); });
    // glowing pulses run along the wires (seek-safe: position is a function of tween progress)
    paths.forEach((p, i) => { const L = p.getTotalLength(), c = document.querySelector("#fl-p" + i), o = { t: 0 };
      const start = (i < 3 ? 1.0 : 2.25) + (i % 3) * 0.12;
      tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.1, ease: "none" }, start);
      tl.fromTo(o, { t: 0 }, { t: 1, duration: 0.7, ease: "power1.inOut", onUpdate: () => { const pt = p.getPointAtLength(o.t * L); c.setAttribute("cx", pt.x); c.setAttribute("cy", pt.y); } }, start);
      tl.to(c, { opacity: 0, duration: 0.12, ease: "none" }, start + 0.62); });
    tl.to("#fl-s1 .glow", { opacity: 1, duration: 0.2, ease: "none" }, 0.75);
    tl.fromTo("#fl-lead", { x: 612, y: 578, opacity: 0, scale: 0.7 }, { x: 612, y: 578, opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 0.8);
    tl.to("#fl-lead", { x: 800, y: 592, duration: 0.55, ease: "power3.inOut" }, 1.45);
    tl.to("#fl-lead", { opacity: 0, scale: 0.5, duration: 0.15, ease: "power3.in" }, 1.95);
    tl.to("#fl-s1 .glow", { opacity: 0, duration: 0.3, ease: "none" }, 2.0);
    [0, 1, 2].forEach(i => tl.fromTo("#fl-tg" + i, { opacity: 0, y: 14, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }, 2.1 + i * 0.12));
    tl.fromTo(".wt", { opacity: 0 }, { opacity: 1, duration: 0.4, stagger: 0.2, ease: "none" }, 0.9);
    tl.fromTo("#fl-cring", { scale: 0.6, opacity: 0.9 }, { scale: 1.6, opacity: 0, duration: 0.8, ease: "expo.out" }, 1.98);
    tl.to("#fl-core", { scale: 1.07, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }, 1.98);
    [0, 1, 2].forEach(i => { const t = 2.6 + i * 0.28;
      tl.to("#fl-o" + i + " .glow", { opacity: 1, duration: 0.2, ease: "none" }, t);
      tl.fromTo("#fl-o" + i + " .ic", { backgroundColor: "rgba(216,187,255,0.08)" }, { backgroundColor: "#4ADE9E", duration: 0.2, ease: "none" }, t);
      tl.fromTo("#fl-o" + i + " .ic svg", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, t);
      tl.to("#fl-o" + i, { scale: 1.05, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, t); });
    const n = { v: 1284 }, el = document.querySelector("#fl-n");
    tl.fromTo(n, { v: 1284 }, { v: 1302, duration: 1.8, ease: "power2.out", onUpdate: () => { el.textContent = Math.round(n.v).toLocaleString("en-IN"); } }, 2.4);
    // hand-off: whip pan left
    tl.to("#fl-cam", { x: -580, filter: "blur(22px)", opacity: 0, duration: 0.26, ease: "power3.in" }, 4.74);
'''

# ================================================================ 4. proof (15.4-18.6 s, 3.2 s)
chips_pr = [('instagram', '❤ 48.2K likes', 1500, 210), ('instagram', '💬 1,940 comments', 1560, 760), ('instagram', '↗ 6.1K shares', 1010, 820)]
pr_css = '''
#pr-t { top: 130px; }
#pr-big { position: absolute; left: 140px; top: 290px; height: 340px; overflow: hidden; }
#pr-n { display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 330px; line-height: 1; letter-spacing: -0.045em; font-variant-numeric: tabular-nums;
  color: #FFFFFF; }
#pr-l { position: absolute; left: 156px; top: 650px; font-size: 46px; font-weight: 650; }
#pr-f { position: absolute; left: 156px; top: 722px; font-size: 34px; color: #BDB2DC; } #pr-f b { color: #fff; font-variant-numeric: tabular-nums; }
#pr-s { position: absolute; left: 158px; top: 790px; font-size: 30px; color: #8E84B4; display: flex; align-items: center; gap: 12px; }
#pr-chart { position: absolute; left: 980px; top: 320px; width: 780px; height: 500px; }
#pr-chart .ln2 { fill: none; stroke: url(#prs); stroke-width: 8; stroke-linecap: round; }
#pr-chart .ar { fill: url(#prg); } #pr-chart .gd { stroke: rgba(216, 187, 255, .1); stroke-width: 1.5; }
#pr-head { fill: #fff; filter: drop-shadow(0 0 10px #B98AFF); }
.ax { position: absolute; font-size: 24px; color: #8E84B4; }
'''
pr_body = f'''    <h1 id="pr-t" class="title" data-motion-blur="off">{lines([[("We", False), ("grow", False), ("our", False), ("own", True), ("page", True), ("first.", False)]])}</h1>
    <div id="pr-big" data-motion-blur="off"><span id="pr-n">0</span></div>
    <div id="pr-l">views in 30 days</div>
    <div id="pr-f"><b id="pr-fn">0</b> followers and counting</div>
    <div id="pr-s" class="mono">{icon("instagram", 32)}@ai.nxtlvl · our own Instagram</div>
    <svg id="pr-chart" viewBox="0 0 780 500"><defs><linearGradient id="prg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A95CFF" stop-opacity=".4"/><stop offset="1" stop-color="#A95CFF" stop-opacity="0"/></linearGradient>
      <linearGradient id="prs" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7D18FC"/><stop offset=".6" stop-color="#B46CFF"/><stop offset="1" stop-color="#FF8BD1"/></linearGradient></defs>
      <path class="gd" d="M0 125H780M0 250H780M0 375H780"/>
      <path class="ar" id="pr-ar" d="M0 470 C120 465 180 440 260 430 S400 380 470 330 S620 170 780 40 L780 500 L0 500Z"/>
      <path class="ln2" id="pr-ln" d="M0 470 C120 465 180 440 260 430 S400 380 470 330 S620 170 780 40"/>
      <circle id="pr-head" r="13" cx="0" cy="470"/></svg>
    <div class="ax mono" style="left:980px;top:836px">Day 1</div><div class="ax mono" style="left:1660px;top:836px">Day 30</div>'''
pr_js = '''
    tl.fromTo(["#pr-chart", "#pr-l", "#pr-f", "#pr-s", ".ax"], { opacity: 0, x: 160, filter: "blur(18px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.4, stagger: 0.04, ease: "expo.out" }, 0);
    rise("#pr-t .ln > span", 0.0, 0.05);
    tl.fromTo("#pr-n", { yPercent: 105 }, { yPercent: 0, duration: 0.7, ease: "expo.out" }, 0.1);
    const ln = document.querySelector("#pr-ln"), L = ln.getTotalLength(), head = document.querySelector("#pr-head"), hp = { t: 0 };
    tl.fromTo(ln, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 1.3, ease: "power3.out" }, 0.3);
    tl.fromTo(hp, { t: 0 }, { t: 1, duration: 1.3, ease: "power3.out", onUpdate: () => { const p = ln.getPointAtLength(hp.t * L); head.setAttribute("cx", p.x); head.setAttribute("cy", p.y); } }, 0.3);
    tl.fromTo("#pr-ar", { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "none" }, 0.9);
    const c = { v: 0 }, el = document.querySelector("#pr-n");
    tl.fromTo(c, { v: 0 }, { v: 1000000, duration: 1.3, ease: "power3.out", onUpdate: () => { el.textContent = c.v >= 995000 ? "1.0M" : Math.round(c.v / 1000) + "K"; } }, 0.25);
    const f = { v: 0 }, fe = document.querySelector("#pr-fn");
    tl.fromTo(f, { v: 0 }, { v: 9924, duration: 1.3, ease: "power3.out", onUpdate: () => { fe.textContent = Math.round(f.v).toLocaleString("en-IN"); } }, 0.35);
    tl.to("#pr-n", { scale: 1.04, transformOrigin: "0% 60%", duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, 1.55);
    // hand-off: everything streaks out to the upper right after the shooting star
    tl.to("#root > *", { x: 260, y: -120, opacity: 0, filter: "blur(14px)", duration: 0.26, ease: "power3.in" }, 2.94);
'''

# ================================================================ 5. end card (18.6-22 s, 3.4 s)
ec_css = '''
#ec-lock { position: absolute; left: 50%; top: 350px; width: 780px; height: 176px; margin-left: -390px; }
#ec-tile { position: absolute; left: 0; top: 0; width: 176px; height: 176px; border-radius: 46px;
  background: radial-gradient(70% 70% at 15% 10%, rgba(126, 26, 246, .95), rgba(126, 26, 246, 0)), radial-gradient(70% 70% at 90% 95%, rgba(94, 6, 242, .9), rgba(94, 6, 242, 0)), #0A0620;
  box-shadow: 0 0 0 2px rgba(125, 24, 252, .3) inset, 0 40px 90px -30px rgba(125, 24, 252, .9); }
#ec-mark { position: absolute; left: 0; top: 0; width: 176px; height: 176px; display: grid; place-items: center; z-index: 3; }
#ec-mark svg { width: 74%; height: 74%; }
#ec-trail { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; z-index: 2; }
#ec-trail path { fill: none; stroke: url(#ect); stroke-width: 6; stroke-linecap: round; }
#ec-word { position: absolute; left: 214px; top: 39px; width: 566px; height: 104px; overflow: hidden; }
#ec-word svg { width: 566px; height: auto; display: block; }

#ec-cta { position: absolute; left: 0; right: 0; top: 610px; display: flex; justify-content: center; align-items: center; gap: 30px; }
#ec-btn { position: relative; overflow: hidden; padding: 26px 52px; border-radius: 99px; background: linear-gradient(100deg, #5E06F2, #7D18FC 45%, #B46CFF); font-size: 40px; font-weight: 650; color: #fff; box-shadow: 0 26px 56px -20px rgba(125, 24, 252, 1); }
#ec-shine { position: absolute; top: 0; bottom: 0; left: -40%; width: 30%; background: linear-gradient(100deg, transparent, rgba(255, 255, 255, .55), transparent); transform: skewX(-20deg); }
#ec-url { font-size: 36px; color: #BDB2DC; }
#ec-trust { position: absolute; left: 0; right: 0; top: 760px; text-align: center; font-size: 28px; color: #8E84B4; letter-spacing: .02em; }
#ec-nx { position: absolute; left: 1470px; top: 540px; width: 290px; height: auto; filter: drop-shadow(0 30px 30px rgba(94, 6, 242, .5)); }
'''
ec_body = f'''    <svg id="ec-trail" viewBox="0 0 1920 1080"><defs><linearGradient id="ect" gradientUnits="userSpaceOnUse" x1="160" y1="980" x2="660" y2="440"><stop offset="0" stop-color="#7D18FC" stop-opacity="0"/><stop offset=".7" stop-color="#D8BBFF" stop-opacity=".8"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient></defs>
      <path id="ec-path" d="M160 980 C300 900 420 640 658 438"/></svg>
    <div id="ec-lock"><div id="ec-tile"></div><div id="ec-mark">{ROCKET}</div><div id="ec-word">{WORD.replace('class="lg-word"', 'role="img" aria-label="nxtlvl social"')}</div></div>
    <div id="ec-cta"><span id="ec-btn">Book a free call<i id="ec-shine"></i></span><span id="ec-url" class="mono">nxtlvlsocial.ai</span></div>
    <div id="ec-trust" class="mono">Monthly plans · No lock-in · You own everything</div>
    <img id="ec-nx" src="assets/img/pose-celebrate.webp" alt="Nextyy celebrating">'''
ec_js = '''
    // the rocket flies in on its own trail and lands in the tile; the tile pops; the wordmark wipes in
    const path = document.querySelector("#ec-path"), L = path.getTotalLength(), fly = { t: 0 }, mark = document.querySelector("#ec-mark");
    tl.fromTo(path, { strokeDasharray: L, strokeDashoffset: L, opacity: 1 }, { strokeDashoffset: 0, duration: 0.55, ease: "power3.out" }, 0);
    tl.fromTo(fly, { t: 0 }, { t: 1, duration: 0.55, ease: "power3.out", onUpdate: () => { const p = path.getPointAtLength(fly.t * L); gsap.set(mark, { x: p.x - 658, y: p.y - 438, scale: 0.5 + 0.5 * fly.t }); } }, 0);
    tl.to(path, { opacity: 0, duration: 0.35, ease: "none" }, 0.5);
    tl.fromTo("#ec-tile", { scale: 0, rotation: -20 }, { scale: 1, rotation: 0, duration: 0.6, ease: "back.out(1.8)" }, 0.45);
    tl.fromTo(mark, { rotation: 0 }, { rotation: 0, duration: 0.01 }, 0.56);
    tl.to("#ec-tile", { scale: 1.08, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, 1.12);
    tl.fromTo("#ec-word", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }, 0.75);
    tl.fromTo("#ec-btn", { opacity: 0, y: 30, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.6)" }, 0.95);
    tl.fromTo("#ec-url", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }, 1.05);
    tl.fromTo("#ec-trust", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 1.25);
    tl.fromTo("#ec-shine", { xPercent: 0 }, { xPercent: 520, duration: 0.7, ease: "power2.inOut" }, 1.5);
    tl.fromTo("#ec-nx", { opacity: 0, y: 300, rotation: 12 }, { opacity: 1, y: 0, rotation: 0, duration: 0.7, ease: "back.out(1.7)" }, 0.9);
'''

files = {'hook': (hook_css, hook_body, hook_js), 'agents': (ag_css, ag_body, ag_js), 'automation': (fl_css, fl_body, fl_js), 'proof': (pr_css, pr_body, pr_js), 'endcard': (ec_css, ec_body, ec_js)}
for k, (c, b, j) in files.items():
    open(f'{P}/compositions/{k}.html', 'w').write(scene(k, c, b, j))

# ---------------------------------------------------------------- root: ground, drifting light, seam flashes, shooting stars
SLOTS = [('hook', 0, 4.6), ('agents', 4.6, 5.8), ('automation', 10.4, 5.0), ('proof', 15.4, 3.2), ('endcard', 18.6, 3.4)]
DUR = 22
hosts = '\n'.join(f'''      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{d}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080"></div>''' for k, s, d in SLOTS)
SEAMS = [4.45, 10.25, 15.25, 18.45]
flashes = '\n'.join(f'      <div id="fx-flash{i}" class="clip flash" data-start="{t:.2f}" data-duration="0.5" data-track-index="3" data-layout-ignore><i></i></div>' for i, t in enumerate(SEAMS))
STARS = [(4.3, 'a'), (15.1, 'b'), (18.3, 'c')]
stars = '\n'.join(f'      <div id="fx-star{i}" class="clip star" data-start="{t}" data-duration="0.7" data-track-index="4" data-layout-ignore><i></i></div>' for i, (t, _) in enumerate(STARS))
index = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ --ground: #0B0618; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: var(--ground); }}
      #root {{ width: 100%; height: 100%; position: relative; }}
      #ground {{ position: absolute; inset: 0; background: var(--ground); overflow: hidden; }}
      .blob {{ position: absolute; border-radius: 50%; filter: blur(110px); }}
      #blob-a {{ left: -260px; top: -320px; width: 1100px; height: 900px; background: rgba(126, 26, 246, .42); }}
      #blob-b {{ right: -300px; bottom: -380px; width: 1100px; height: 950px; background: rgba(94, 6, 242, .34); }}
      #blob-c {{ left: 760px; top: 640px; width: 700px; height: 520px; background: rgba(255, 79, 163, .12); }}
      #texture {{ position: absolute; inset: 0; opacity: .55; background-image: radial-gradient(rgba(216, 187, 255, .08) 1.4px, transparent 1.4px); background-size: 34px 34px; }}
      #vignette {{ position: absolute; inset: 0; background: radial-gradient(120% 90% at 50% 45%, transparent 60%, rgba(0, 0, 0, .45)); pointer-events: none; z-index: 20; }}
      .flash {{ position: absolute; inset: 0; z-index: 30; pointer-events: none; }}
      .flash i {{ position: absolute; inset: 0; background: radial-gradient(60% 70% at 50% 50%, rgba(216, 187, 255, .2), rgba(125, 24, 252, .12) 45%, transparent 75%); opacity: 0; }}
      .star {{ position: absolute; inset: 0; z-index: 31; pointer-events: none; overflow: hidden; }}
      .star i {{ position: absolute; left: 0; top: 0; width: 520px; height: 6px; border-radius: 6px; background: linear-gradient(90deg, rgba(169, 92, 255, 0), rgba(216, 187, 255, .8) 70%, #fff); box-shadow: 0 0 20px rgba(216, 187, 255, .8); transform-origin: 100% 50%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080" data-motion-blur="on">
      <div id="ground" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"><div id="blob-a" class="blob"></div><div id="blob-b" class="blob"></div><div id="blob-c" class="blob"></div></div>
      <div id="texture" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1" data-layout-ignore></div>
{hosts}
{flashes}
{stars}
      <div id="vignette" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5" data-layout-ignore></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // the light behind everything drifts slowly (a background stage, 22 s, loops back to its start)
      tl.fromTo("#blob-a", {{ x: 0, y: 0 }}, {{ x: 260, y: 140, duration: {DUR / 2}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);
      tl.fromTo("#blob-b", {{ x: 0, y: 0 }}, {{ x: -240, y: -120, duration: {DUR / 2}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);
      tl.fromTo("#blob-c", {{ x: 0, scale: 1 }}, {{ x: -380, scale: 1.3, duration: {DUR / 2}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);
      // a violet light flash on every scene seam
      {"".join(f'tl.fromTo("#fx-flash{i} i", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15, ease: "power2.out", yoyo: true, repeat: 1 }}, {t});' for i, t in enumerate(SEAMS))}
      // shooting stars (the logo's rocket) streak across at the big hand-offs
      {"".join(f'tl.fromTo("#fx-star{i} i", {{ x: -600, y: {900 - i * 120}, rotation: -28, opacity: 1 }}, {{ x: 2200, y: {60 + i * 60}, rotation: -28, opacity: 1, duration: 0.6, ease: "power2.in" }}, {t});' for i, (t, _) in enumerate(STARS))}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(f'{P}/index.html', 'w').write(index)
print('written v2')
