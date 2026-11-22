"""Writes the Nxtlvl SaaS film HyperFrames project: index.html + five scene files."""
import json, os
P = '/home/user/Nxtlvl-Social/nxtlvl-saas-film-16x9'
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
.title { position: absolute; left: 160px; margin: 0; font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 76px; line-height: 1.02; letter-spacing: -0.025em; white-space: nowrap; }
.title .w { display: inline-block; }
.acc { color: #B98AFF; }
.panel { position: absolute; background: #130C28; border: 1px solid rgba(216, 187, 255, .14); border-radius: 28px; box-shadow: 0 40px 100px -40px rgba(94, 6, 242, .55); }
.mono { font-family: "Geist Mono", monospace; }
'''

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
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''

def words(text, cls='w', acc=()):
    out = []
    for i, w in enumerate(text.split(' ')):
        c = cls + (' acc' if i in acc else '')
        out.append(f'<span class="{c}">{w}</span>')
    return ' '.join(out)

TICK = '<svg viewBox="0 0 18 12" width="26" height="17"><path d="M1 6.5l3 3L10 2.5M7 9.5l1 1L16.5 2" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ---------------------------------------------------------------- 1. hook (4.2 s)
hook_css = '''
#hk-t1 { top: 190px; } #hk-t2 { top: 190px; }
.sub { position: absolute; left: 164px; top: 520px; font-size: 32px; color: #BDB2DC; max-width: 640px; line-height: 1.4; }
#hk-chat { left: 1000px; top: 150px; width: 780px; height: 780px; overflow: hidden; }
.ch-top { display: flex; align-items: center; gap: 18px; padding: 26px 30px; border-bottom: 1px solid rgba(216, 187, 255, .1); }
.ch-av { width: 64px; height: 64px; border-radius: 50%; background: #7D18FC; display: grid; place-items: center; font-weight: 700; font-size: 24px; }
.ch-top b { display: block; font-size: 30px; font-weight: 600; } .ch-top small { font-size: 22px; color: #4ADE9E; }
.ch-top .mono { margin-left: auto; font-size: 24px; color: #8E84B4; }
.bub { position: absolute; max-width: 560px; padding: 22px 28px; border-radius: 28px; font-size: 32px; line-height: 1.35; }
.bub.in { left: 34px; background: #231745; border-top-left-radius: 8px; }
.bub.out { right: 34px; background: linear-gradient(150deg, #8B2DFF, #6A0FE0); border-top-right-radius: 8px; color: #fff; }
.bub .meta { display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-top: 6px; font-size: 22px; color: rgba(255, 255, 255, .7); }
#hk-typing { position: absolute; left: 34px; top: 380px; display: flex; gap: 9px; padding: 22px 26px; border-radius: 24px; background: #231745; }
#hk-typing i { width: 13px; height: 13px; border-radius: 50%; background: #8E84B4; }
#hk-ticks svg { stroke: rgba(255, 255, 255, .55); }
#hk-ticks2 svg { stroke: #53BDEB; }
#hk-ticks, #hk-ticks2 { display: inline-flex; }
#hk-tickwrap { position: relative; display: inline-flex; width: 26px; height: 17px; } #hk-tickwrap > span { position: absolute; inset: 0; }
#hk-saved { position: absolute; left: 50%; top: 680px; transform: translateX(-50%); padding: 12px 22px; border-radius: 99px; background: rgba(74, 222, 158, .12); color: #4ADE9E; font-size: 24px; white-space: nowrap; }
#hk-nx { position: absolute; left: 760px; top: 600px; width: 300px; height: auto; filter: drop-shadow(0 30px 30px rgba(94, 6, 242, .45)); }
'''
hook_body = f'''    <h1 id="hk-t1" class="title"><span class="w acc">11:42</span> <span class="w acc">pm.</span><br><span class="w">A</span> <span class="w">customer</span><br><span class="w">is</span> <span class="w">waiting.</span></h1>
    <h1 id="hk-t2" class="title"><span class="w">Answered</span><br><span class="w">in</span> <span class="w acc">4</span> <span class="w acc">seconds.</span></h1>
    <p id="hk-sub" class="sub">Your AI team replies day and night.</p>
    <div id="hk-chat" class="panel">
      <div class="ch-top">{icon("whatsapp", 40)}<span class="ch-av">CA</span><div><b>Café Aroma</b><small>Reply Agent on</small></div><span class="mono">11:42 pm</span></div>
      <div id="hk-in" class="bub in" style="top:150px">Hi! Are you open tonight? Table for 4 at 8?<div class="meta mono">11:42 pm</div></div>
      <div id="hk-typing"><i></i><i></i><i></i></div>
      <div id="hk-out" class="bub out" style="top:380px">Booked! Table for 4 at 8 pm.<div class="meta mono">11:42 pm <span id="hk-tickwrap"><span id="hk-ticks">{TICK}</span><span id="hk-ticks2">{TICK}</span></span></div></div>
      <div id="hk-saved" class="mono">Lead saved · owner notified</div>
    </div>
    <img id="hk-nx" src="assets/img/mascot.webp" alt="Nextyy waving">'''
hook_js = '''
    const w1 = "#hk-t1 .w", w2 = "#hk-t2 .w";
    // frame 0 already shows the hook (it is the thumbnail): the title, the chat and the waiting message
    tl.fromTo("#hk-in .meta", { opacity: 0.4 }, { opacity: 1, duration: 0.4, ease: "none" }, 0.2);
    tl.fromTo("#hk-sub", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }, 0.6);
    tl.fromTo("#hk-typing", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, 0.9);
    tl.fromTo("#hk-typing i", { y: 0 }, { y: -8, duration: 0.18, ease: "power1.inOut", stagger: { each: 0.09, repeat: 3, yoyo: true } }, 1.0);
    tl.to("#hk-typing", { opacity: 0, scale: 0.8, duration: 0.15, ease: "power3.in" }, 1.7);
    tl.fromTo("#hk-out", { opacity: 0, y: 40, scale: 0.92, filter: "blur(6px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, 1.75);
    tl.fromTo("#hk-ticks2", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "none" }, 2.4);
    tl.fromTo("#hk-saved", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 2.45);
    tl.fromTo("#hk-nx", { opacity: 0, y: 260, scale: 0.6, rotation: -8 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.9, ease: "back.out(1.6)" }, 1.4);
    tl.to("#hk-nx", { rotation: 6, duration: 0.25, ease: "power1.inOut", yoyo: true, repeat: 3 }, 2.3);
    tl.to(w1, { opacity: 0, filter: "blur(8px)", duration: 0.14, stagger: 0.04, ease: "power3.in" }, 1.85);
    tl.fromTo(w2, { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16, stagger: 0.07, ease: "power4.out" }, 2.2);
    // hand-off: Nextyy carries across into the agent app's pinned avatar; the rest blurs away on the same ground
    tl.to("#hk-nx", { x: -680, y: -480, scale: 0.28, rotation: 0, duration: 0.5, ease: "power2.inOut" }, 3.65);
    tl.to(["#hk-t2", "#hk-sub", "#hk-chat"], { opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }, 3.8);
'''

# ---------------------------------------------------------------- 2. agents (5.3 s)
AG = [('content', 'Content Agent', '3 hooks ready for Friday'), ('reply', 'Reply Agent', '47 messages answered'), ('ads', 'Ads Agent', 'Creative B is 38% cheaper'),
      ('edit', 'Edit Agent', 'Reel v2 ready: 0:28'), ('seo', 'SEO Agent', '#1 for "best café in Baner"'), ('report', 'Report Agent', 'November report ready')]
rows = ''.join(f'<div class="row" id="ag-r{i}"><img src="assets/img/agent-{k}.webp" alt=""><div><b>{n}</b><small>{p}</small></div></div>' for i, (k, n, p) in enumerate(AG))
steps = ['Pulled Meta ads data', 'Compared cost per lead', 'Found the winner']
SP = '<svg viewBox="0 0 16 16" width="26" height="26"><circle cx="8" cy="8" r="6" fill="none" stroke="#4ADE9E" stroke-width="1.6" opacity=".5"/><path d="M4.5 8.2l2.3 2.3 4.7-4.9" fill="none" stroke="#4ADE9E" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
chips = ''.join(f'<span class="stp" id="ag-s{i}">{SP}{t}</span>' for i, t in enumerate(steps))
ag_css = '''
#ag-t { top: 96px; }
#ag-app { left: 160px; top: 232px; width: 1600px; height: 790px; overflow: hidden; display: grid; grid-template-columns: 480px 1fr; }
.side { background: linear-gradient(180deg, #160E2E, #0F0920); border-right: 1px solid rgba(216, 187, 255, .1); padding: 24px 18px; }
.pin { display: flex; align-items: center; gap: 16px; padding: 4px 10px 22px; }
.pin span { width: 84px; height: 84px; } .pin b { font-size: 30px; font-weight: 650; } .pin small { display: block; font-size: 22px; color: #8E84B4; }
.row { display: flex; align-items: center; gap: 18px; padding: 12px 14px; border-radius: 18px; margin-bottom: 4px; }
.row img { width: 66px; height: 66px; border-radius: 16px; background: #1A1135; }
.row b { display: block; font-size: 29px; font-weight: 600; } .row small { font-size: 24px; color: #8E84B4; white-space: nowrap; }
#ag-hi { position: absolute; left: 18px; top: 134px; width: 444px; height: 92px; border-radius: 18px; background: #231745; box-shadow: inset 0 0 0 1.5px rgba(169, 92, 255, .5); }
.main { position: relative; padding: 30px 40px; }
.mh { display: flex; align-items: center; gap: 18px; padding-bottom: 24px; border-bottom: 1px solid rgba(216, 187, 255, .1); }
.mh img { width: 72px; height: 72px; } .mh b { font-size: 34px; font-weight: 650; } .mh small { display: block; font-size: 22px; color: #8E84B4; }
.mh .state { margin-left: auto; padding: 8px 18px; border-radius: 99px; background: rgba(74, 222, 158, .12); color: #4ADE9E; font-size: 22px; }
.steps { position: absolute; left: 40px; top: 190px; display: flex; gap: 12px; flex-wrap: wrap; width: 1000px; }
.stp { display: inline-flex; align-items: center; gap: 10px; padding: 12px 20px 12px 14px; border-radius: 99px; border: 1px solid rgba(74, 222, 158, .25); background: rgba(74, 222, 158, .06); font-size: 24px; color: #BDB2DC; }
#ag-msg { position: absolute; left: 40px; top: 290px; width: 860px; padding: 26px 30px; border-radius: 28px; border-top-left-radius: 8px; background: #231745; font-size: 32px; line-height: 1.4; }
#ag-you { position: absolute; right: 40px; top: 470px; padding: 16px 30px; border-radius: 99px; background: linear-gradient(100deg, #5E06F2, #7D18FC 45%, #B46CFF); font-size: 30px; font-weight: 600; color: #fff; }
#ag-rc { position: absolute; left: 40px; top: 570px; display: flex; align-items: center; gap: 16px; padding: 20px 26px; border-radius: 20px; background: rgba(74, 222, 158, .1); border: 1.5px solid rgba(74, 222, 158, .35); color: #A7F3CF; font-size: 30px; font-weight: 600; transform-origin: 30% 50%; }
#ag-rc i { width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: #4ADE9E; color: #052b1c; font-style: normal; font-weight: 800; font-size: 24px; }
#ag-nx { position: absolute; left: 188px; top: 260px; width: 84px; height: 84px; }
'''
ag_body = f'''    <h1 id="ag-t" class="title">{words("Six AI agents work your brand every day.", acc=(0, 1, 2))}</h1>
    <div id="ag-app" class="panel">
      <div class="side"><div class="pin"><span></span><div><b>Nextyy</b><small>your team lead</small></div></div>
        <div id="ag-hi"></div>{rows}</div>
      <div class="main"><div class="mh"><img src="assets/img/agent-ads.webp" alt=""><div><b>Ads Agent</b><small>Watches Meta and Google campaigns daily</small></div><span class="state mono">Optimising</span></div>
        <div class="steps">{chips}</div>
        <div id="ag-msg">Creative B gets leads 38% cheaper. Move ₹2,000 to it?</div>
        <div id="ag-you">Yes, move it</div>
        <div id="ag-rc"><i>✓</i>₹2,000 moved · Creative A → B</div></div>
    </div>
    <img id="ag-nx" src="assets/img/pin-nextyy.webp" alt="">'''
ag_js = '''
    tl.fromTo("#ag-app", { opacity: 0, scale: 0.96, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 0);
    tl.fromTo("#ag-t .w", { opacity: 0.12 }, { opacity: 1, duration: 0.2, stagger: 0.08, ease: "none" }, 0.2);
    tl.fromTo(".row", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, stagger: 0.06, ease: "expo.out" }, 0.25);
    // the selection walks the agents, then settles on Ads
    const ys = [134, 230, 326, 422, 518, 614];
    [0, 1, 2, 3, 4, 5, 2].forEach((r, i) => tl.to("#ag-hi", { y: ys[r] - 134, duration: 0.22, ease: "power2.inOut" }, 0.8 + i * 0.24));
    tl.fromTo(".main .mh", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 2.2);
    [0, 1, 2].forEach(i => tl.fromTo("#ag-s" + i, { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, 2.45 + i * 0.3));
    tl.fromTo("#ag-msg", { opacity: 0, y: 24, filter: "blur(4px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 3.2);
    tl.fromTo("#ag-you", { opacity: 0, y: 18, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 3.55);
    tl.fromTo("#ag-rc", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 3.8);
    // hand-off: zoom through the receipt into the automation flow
    tl.to("#ag-rc", { scale: 2.6, x: 300, duration: 0.35, ease: "power3.in" }, 4.92);
    tl.to(["#ag-app", "#ag-t", "#ag-nx"], { opacity: 0, filter: "blur(14px)", duration: 0.3, ease: "power3.in" }, 4.95);
    tl.to("#ag-rc", { opacity: 0, duration: 0.12, ease: "none" }, 5.16);
'''

# ---------------------------------------------------------------- 3. automation (4.5 s)
srcs = [('instagram', 'Instagram DM', 'Price? Timings?'), ('whatsapp', 'WhatsApp', 'Booking request'), ('meta', 'Meta lead ad', 'New lead · Rahul')]
outs = [('Replied in your voice', 'in 4 s, 24/7'), ('Lead qualified', 'budget, area, timeline'), ('Saved to CRM', 'owner told on WhatsApp')]
src_html = ''.join(f'<div class="nd src" id="fl-s{i}" style="top:{y}px"><span class="ic">{icon(k, 38)}</span><div><b>{n}</b><small>{s}</small></div></div>' for i, ((k, n, s), y) in enumerate(zip(srcs, [360, 540, 720])))
CHK = '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#052b1c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
out_html = ''.join(f'<div class="nd out" id="fl-o{i}" style="top:{y}px"><span class="ic ok">{CHK}</span><div><b>{n}</b><small>{s}</small></div></div>' for i, ((n, s), y) in enumerate(zip(outs, [360, 540, 720])))
fl_css = '''
#fl-t { top: 110px; }
.nd { position: absolute; width: 440px; height: 128px; display: flex; align-items: center; gap: 20px; padding: 0 26px; background: #130C28; border: 1.5px solid rgba(216, 187, 255, .16); border-radius: 24px; }
.nd.src { left: 160px; } .nd.out { left: 1320px; }
.nd .ic { width: 66px; height: 66px; border-radius: 18px; display: grid; place-items: center; background: rgba(216, 187, 255, .06); flex: none; }
.nd .ic.ok { background: rgba(216, 187, 255, .08); }
.nd b { display: block; font-size: 30px; font-weight: 600; } .nd small { font-size: 25px; color: #8E84B4; }
.nd .glow { position: absolute; inset: -1.5px; border-radius: 24px; border: 2px solid #A95CFF; box-shadow: 0 0 0 6px rgba(125, 24, 252, .18), 0 18px 40px -16px rgba(125, 24, 252, .9); opacity: 0; }
.nd.out .glow { border-color: #4ADE9E; box-shadow: 0 0 0 6px rgba(74, 222, 158, .14), 0 18px 40px -16px rgba(74, 222, 158, .7); }
#fl-core { position: absolute; left: 760px; top: 470px; width: 400px; height: 300px; border-radius: 30px; background: linear-gradient(160deg, rgba(125, 24, 252, .5), #130C28 70%); border: 1.5px solid rgba(169, 92, 255, .55);
  display: grid; justify-items: center; align-content: center; gap: 10px; box-shadow: 0 30px 80px -30px rgba(125, 24, 252, .8); }
#fl-core img { width: 120px; height: 120px; } #fl-core b { font-size: 32px; font-weight: 650; } #fl-core small { font-size: 26px; color: #BDB2DC; }
#fl-wires { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; }
#fl-wires path { fill: none; stroke: rgba(216, 187, 255, .35); stroke-width: 3; stroke-linecap: round; }
#fl-lead { position: absolute; left: 0; top: 0; display: flex; align-items: center; gap: 12px; padding: 12px 18px; border-radius: 16px; background: #7D18FC; color: #fff; font-size: 24px; font-weight: 600; box-shadow: 0 16px 34px -12px rgba(125, 24, 252, .9); white-space: nowrap; }
#fl-count { position: absolute; left: 1320px; top: 250px; display: flex; align-items: center; gap: 14px; font-size: 24px; color: #BDB2DC; padding: 12px 22px; border-radius: 99px; background: rgba(19, 12, 40, .8); border: 1px solid rgba(216, 187, 255, .16); }
#fl-count b { color: #fff; font-size: 30px; font-weight: 600; font-variant-numeric: tabular-nums; }
#fl-count i { width: 12px; height: 12px; border-radius: 50%; background: #4ADE9E; }
'''
def wire(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    return f'M{x1} {y1} C{mx} {y1} {mx} {y2} {x2} {y2}'
wires = ''.join(f'<path id="fl-w{i}" d="{wire(600, y, 760, 620)}"/>' for i, y in enumerate([424, 604, 784])) + ''.join(f'<path id="fl-v{i}" d="{wire(1160, 620, 1320, y)}"/>' for i, y in enumerate([424, 604, 784]))
fl_body = f'''    <h1 id="fl-t" class="title">{words("Every lead answered, qualified and saved.", acc=(1,))}</h1>
    <svg id="fl-wires" viewBox="0 0 1920 1080">{wires}</svg>
    {src_html.replace('</div></div>', '</div><span class="glow"></span></div>')}
    <div id="fl-core"><img src="assets/img/pin-nextyy.webp" alt=""><b>Nxtlvl Agent</b><small class="mono">avg reply 0.8 s</small></div>
    {out_html.replace('</div></div>', '</div><span class="glow"></span></div>')}
    <div id="fl-count" class="mono"><i></i>Handled today <b id="fl-n">1,284</b></div>
    <div id="fl-lead">{icon("whatsapp", 28, "#fff")}New lead · table for 4</div>'''
fl_js = '''
    tl.fromTo("#fl-t", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power2.out" }, 0.1);
    tl.fromTo(".nd.src", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.6, stagger: 0.07, ease: "expo.out" }, 0.05);
    tl.fromTo("#fl-core", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.7, ease: "expo.out" }, 0.15);
    tl.fromTo(".nd.out", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.6, stagger: 0.07, ease: "expo.out" }, 0.25);
    tl.fromTo("#fl-count", { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 0.35);
    document.querySelectorAll("#fl-wires path").forEach((p, i) => { const L = p.getTotalLength(); tl.fromTo(p, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, 0.45 + (i % 3) * 0.06 + (i > 2 ? 0.25 : 0)); });
    // a WhatsApp lead travels into the agent
    tl.to("#fl-s1 .glow", { opacity: 1, duration: 0.2, ease: "none" }, 0.7);
    tl.fromTo("#fl-lead", { x: 612, y: 578, opacity: 0, scale: 0.8 }, { x: 612, y: 578, opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, 0.75);
    tl.to("#fl-lead", { x: 800, y: 592, duration: 0.6, ease: "power2.inOut" }, 1.4);
    tl.to("#fl-lead", { opacity: 0, scale: 0.6, duration: 0.15, ease: "power3.in" }, 1.95);
    tl.to("#fl-s1 .glow", { opacity: 0, duration: 0.3, ease: "none" }, 2.0);
    tl.to("#fl-core", { scale: 1.05, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }, 1.95);
    [0, 1, 2].forEach(i => { tl.to("#fl-o" + i + " .glow", { opacity: 1, duration: 0.2, ease: "none" }, 2.3 + i * 0.3); tl.fromTo("#fl-o" + i + " .ic", { backgroundColor: "rgba(216,187,255,0.08)" }, { backgroundColor: "#4ADE9E", duration: 0.2, ease: "none" }, 2.3 + i * 0.3); });
    const n = { v: 1284 }, el = document.querySelector("#fl-n");
    tl.fromTo(n, { v: 1284 }, { v: 1302, duration: 1.6, ease: "power2.out", onUpdate: () => { el.textContent = Math.round(n.v).toLocaleString("en-IN"); } }, 2.2);
    // hand-off: whip left
    tl.to("#root > *", { x: "-=320", opacity: 0, filter: "blur(18px)", duration: 0.22, ease: "power3.in" }, 4.26);
'''

# ---------------------------------------------------------------- 4. proof (3 s)
pr_css = '''
#pr-t { top: 150px; }
#pr-n { position: absolute; left: 150px; top: 300px; font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 330px; line-height: 1; letter-spacing: -0.04em; font-variant-numeric: tabular-nums;
  background: linear-gradient(100deg, #FFFFFF 0%, #D8BBFF 45%, #A95CFF 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
#pr-l { position: absolute; left: 164px; top: 660px; font-size: 44px; font-weight: 600; }
#pr-s { position: absolute; left: 166px; top: 730px; font-size: 30px; color: #8E84B4; display: flex; align-items: center; gap: 12px; }
#pr-chart { position: absolute; left: 980px; top: 330px; width: 780px; height: 500px; }
#pr-chart .ln { fill: none; stroke: #A95CFF; stroke-width: 7; stroke-linecap: round; }
#pr-chart .ar { fill: url(#prg); }
#pr-chart .gd { stroke: rgba(216, 187, 255, .1); stroke-width: 1.5; }
#pr-dot { fill: #4ADE9E; }
'''
pr_body = f'''    <h1 id="pr-t" class="title">{words("We grow our own page first.", acc=(3, 4))}</h1>
    <div id="pr-n">0</div>
    <div id="pr-l">views in 30 days</div>
    <div id="pr-s" class="mono">{icon("instagram", 30)}@ai.nxtlvl · our own Instagram</div>
    <svg id="pr-chart" viewBox="0 0 780 500"><defs><linearGradient id="prg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A95CFF" stop-opacity=".35"/><stop offset="1" stop-color="#A95CFF" stop-opacity="0"/></linearGradient></defs>
      <path class="gd" d="M0 125H780M0 250H780M0 375H780"/>
      <path class="ar" id="pr-ar" d="M0 470 C120 465 180 440 260 430 S400 380 470 330 S620 170 780 40 L780 500 L0 500Z"/>
      <path class="ln" id="pr-ln" d="M0 470 C120 465 180 440 260 430 S400 380 470 330 S620 170 780 40"/>
      <circle id="pr-dot" cx="780" cy="40" r="14"/></svg>'''
pr_js = '''
    tl.fromTo(["#pr-t", "#pr-n", "#pr-l", "#pr-s", "#pr-chart"], { opacity: 0, x: 120, filter: "blur(16px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.35, stagger: 0.04, ease: "expo.out" }, 0);
    const ln = document.querySelector("#pr-ln"), L = ln.getTotalLength();
    tl.fromTo(ln, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 1.2, ease: "power3.out" }, 0.3);
    tl.fromTo("#pr-ar", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "none" }, 0.9);
    tl.fromTo("#pr-dot", { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.4, ease: "back.out(2)" }, 1.4);
    const c = { v: 0 }, el = document.querySelector("#pr-n");
    tl.fromTo(c, { v: 0 }, { v: 1000000, duration: 1.2, ease: "power3.out", onUpdate: () => { el.textContent = c.v >= 995000 ? "1.0M" : Math.round(c.v / 1000) + "K"; } }, 0.3);
    tl.to("#root > *", { opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }, 2.78);
'''

# ---------------------------------------------------------------- 5. end card (3 s)
ec_css = '''
#ec-lock { position: absolute; left: 50%; top: 360px; width: 760px; height: 170px; margin-left: -380px; }
#ec-tile { position: absolute; left: 0; top: 0; width: 170px; height: 170px; border-radius: 44px; display: grid; place-items: center;
  background: radial-gradient(70% 70% at 15% 10%, rgba(126, 26, 246, .95), rgba(126, 26, 246, 0)), radial-gradient(70% 70% at 90% 95%, rgba(94, 6, 242, .9), rgba(94, 6, 242, 0)), #0A0620;
  box-shadow: 0 0 0 2px rgba(125, 24, 252, .3) inset, 0 40px 80px -30px rgba(125, 24, 252, .8); }
#ec-tile svg { width: 74%; height: 74%; }
#ec-word { position: absolute; left: 206px; top: 38px; width: 554px; height: 101px; overflow: hidden; }
#ec-word svg { width: 554px; height: auto; display: block; }
#ec-wipe { position: absolute; inset: 0; background: #0B0618; transform-origin: 100% 50%; }
#ec-cta { position: absolute; left: 0; right: 0; top: 610px; display: flex; justify-content: center; align-items: center; gap: 30px; }
#ec-btn { padding: 24px 48px; border-radius: 99px; background: linear-gradient(100deg, #5E06F2, #7D18FC 45%, #B46CFF); font-size: 38px; font-weight: 650; color: #fff; box-shadow: 0 24px 50px -20px rgba(125, 24, 252, .9); }
#ec-url { font-size: 34px; color: #BDB2DC; }
#ec-nx { position: absolute; left: 1330px; top: 560px; width: 300px; height: auto; filter: drop-shadow(0 30px 30px rgba(94, 6, 242, .45)); }
'''
ec_body = f'''    <div id="ec-lock"><div id="ec-tile">{ROCKET}</div><div id="ec-word">{WORD.replace('class="lg-word"', 'role="img" aria-label="nxtlvl social"')}<div id="ec-wipe"></div></div></div>
    <div id="ec-cta"><span id="ec-btn">Book a free call</span><span id="ec-url" class="mono">nxtlvlsocial.ai</span></div>
    <img id="ec-nx" src="assets/img/pose-celebrate.webp" alt="Nextyy celebrating">'''
ec_js = '''
    // Nextyy rises carrying the tile, the tile springs into the lockup, the wordmark wipes in, then the call to action
    tl.fromTo("#ec-nx", { opacity: 0, x: -520, y: 420, scale: 0.8 }, { opacity: 1, x: -520, y: 0, scale: 1, duration: 0.55, ease: "expo.out" }, 0);
    tl.fromTo("#ec-tile", { x: 200, y: 330, scale: 0.6, rotation: -12 }, { x: 200, y: 160, scale: 0.6, rotation: -12, duration: 0.55, ease: "expo.out" }, 0);
    tl.to("#ec-tile", { x: 0, y: 0, scale: 1, rotation: 0, duration: 0.6, ease: "back.out(1.5)" }, 0.55);
    tl.to("#ec-nx", { x: 0, y: 0, scale: 0.85, duration: 0.6, ease: "power2.inOut" }, 0.6);
    tl.fromTo("#ec-wipe", { scaleX: 1 }, { scaleX: 0, duration: 0.45, ease: "power2.inOut" }, 0.7);
    tl.fromTo("#ec-btn", { opacity: 0, y: 24, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "expo.out" }, 0.85);
    tl.fromTo("#ec-url", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }, 0.9);
'''

files = {'hook': (hook_css, hook_body, hook_js), 'agents': (ag_css, ag_body, ag_js), 'automation': (fl_css, fl_body, fl_js), 'proof': (pr_css, pr_body, pr_js), 'endcard': (ec_css, ec_body, ec_js)}
for k, (c, b, j) in files.items():
    open(f'{P}/compositions/{k}.html', 'w').write(scene(k, c, b, j))

SLOTS = [('hook', 0, 4.2), ('agents', 4.2, 5.3), ('automation', 9.5, 4.5), ('proof', 14.0, 3.0), ('endcard', 17.0, 3.0)]
hosts = '\n'.join(f'''      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>''' for k, s, d in SLOTS)
index = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ --ground: #0B0618; --ink: #F4EFFF; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: var(--ground); }}
      #root {{ width: 100%; height: 100%; position: relative; }}
      #ground {{ position: absolute; inset: 0;
        background: radial-gradient(48% 60% at 8% 0%, rgba(126, 26, 246, .26), transparent 70%), radial-gradient(45% 60% at 100% 100%, rgba(94, 6, 242, .2), transparent 70%), var(--ground); }}
      #texture {{ position: absolute; inset: 0; opacity: .5; background-image: radial-gradient(rgba(216, 187, 255, .07) 1.4px, transparent 1.4px); background-size: 34px 34px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="20" data-width="1920" data-height="1080">
      <div id="ground" class="clip" data-start="0" data-duration="20" data-track-index="0"></div>
      <div id="texture" class="clip" data-start="0" data-duration="20" data-track-index="0" data-layout-ignore></div>
{hosts}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
open(f'{P}/index.html', 'w').write(index)
print('written')
