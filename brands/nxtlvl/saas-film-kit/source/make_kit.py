"""Builds the Nxtlvl Social SaaS film kit with no generation API: logo files from the real rocket mark,
start frames for every scene (HTML + existing mascot images), and one combined PDF of images + prompts."""
import os, sys
sys.path.insert(0, '/home/user/Nxtlvl-Social/website-src')
import build  # star_svg / wordmark_svg (main() is guarded)

REPO = '/home/user/Nxtlvl-Social'
OUT = REPO + '/brands/nxtlvl/saas-film-kit'
WORK = os.path.dirname(os.path.abspath(__file__))
IMG = 'file://' + REPO + '/website/img/'
FONT = 'file://' + REPO + '/website/fonts/'
os.makedirs(OUT, exist_ok=True)

ROCKET = build.star_svg('k')
WORD_DARK = build.wordmark_svg().replace('fill="#0B0816"', 'fill="#140B2E"')

BASE_CSS = f'''
@font-face {{ font-family: B; src: url({FONT}bricolage-variable.woff2); font-weight: 200 800; }}
@font-face {{ font-family: S; src: url({FONT}satoshi-500.woff2); font-weight: 500; }}
@font-face {{ font-family: S; src: url({FONT}satoshi-700.woff2); font-weight: 700; }}
* {{ box-sizing: border-box; }} html, body {{ margin: 0; background: transparent; }}
.stage {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; font-family: S, sans-serif; color: #140B2E;
  background: radial-gradient(38% 50% at 12% 10%, rgba(125,24,252,.16), transparent 70%), radial-gradient(40% 55% at 92% 20%, rgba(180,108,255,.24), transparent 70%),
  radial-gradient(35% 45% at 70% 95%, rgba(255,79,163,.10), transparent 70%), #F4F0FE; }}
.stage.sq {{ width: 1080px; height: 1080px; }}
.stage::after {{ content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(94,36,190,.10) 1.5px, transparent 1.5px); background-size: 34px 34px;
  -webkit-mask-image: radial-gradient(60% 60% at 50% 45%, #000, transparent 80%); pointer-events: none; }}
.abs {{ position: absolute; }}
.glass {{ position: absolute; background: rgba(255,255,255,.8); border: 1.5px solid rgba(125,24,252,.13); border-radius: 30px;
  box-shadow: 0 2px 6px rgba(20,11,46,.05), 0 50px 90px -46px rgba(94,6,242,.45); }}
.bar {{ height: 16px; border-radius: 99px; background: #E9E2FA; }} .bar.v {{ background: linear-gradient(90deg,#7D18FC,#B46CFF); }} .bar.d {{ background: #D9CDF6; }}
.bub {{ position: absolute; border-radius: 26px; padding: 22px 26px; display: grid; gap: 12px; }}
.bub.in {{ background: #F1ECFB; border-top-left-radius: 8px; }} .bub.out {{ background: linear-gradient(140deg,#8B2DFF,#6A0FE0); border-top-right-radius: 8px; box-shadow: 0 18px 30px -16px rgba(94,6,242,.7); }}
.bub.out .bar {{ background: rgba(255,255,255,.55); }}
.orb {{ position: absolute; border-radius: 50%; background: conic-gradient(from 0deg,#5E06F2,#7D18FC,#B46CFF,#E6D2FF,#7D18FC,#5E06F2); filter: blur(70px); opacity: .5; }}
.spark {{ position: absolute; width: 34px; height: 34px; background: #B46CFF; clip-path: polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%); opacity: .8; }}
.spark.w {{ background: #fff; }} .spark.s {{ width: 20px; height: 20px; }}
.tick {{ width: 56px; height: 56px; border-radius: 50%; background: #0B9B68; display: grid; place-items: center; box-shadow: 0 10px 22px -10px rgba(11,155,104,.8); }}
.tick svg {{ width: 30px; height: 30px; }}
.mascot {{ position: absolute; height: auto; filter: drop-shadow(0 40px 40px rgba(94,6,242,.25)); }}
.tile {{ display: grid; place-items: center; background: radial-gradient(70% 70% at 15% 10%, rgba(126,26,246,.95), rgba(126,26,246,0)),
  radial-gradient(70% 70% at 90% 95%, rgba(94,6,242,.9), rgba(94,6,242,0)), #0A0620; box-shadow: 0 0 0 2px rgba(125,24,252,.22) inset, 0 40px 80px -30px rgba(94,6,242,.7); }}
.tile svg {{ width: 75%; height: 75%; }}
'''
TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
def bars(*ws, cls=''):
    return ''.join(f'<div class="bar {cls}" style="width:{w}px"></div>' for w in ws)
def cal(x, y, on):
    cells = ''.join(f'<div style="aspect-ratio:1;border-radius:12px;background:{"linear-gradient(140deg,#8B2DFF,#B46CFF)" if i in on else "#F1ECFB"}"></div>' for i in range(28))
    return f'<div class="glass" style="left:{x}px;top:{y}px;width:460px;height:300px;padding:28px"><div class="bar d" style="width:160px;margin-bottom:22px"></div><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:10px">{cells}</div></div>'

SCENES = {}
SCENES['01-hello'] = f'''<div class="orb" style="left:660px;top:190px;width:600px;height:600px"></div>
<div class="abs" style="left:610px;top:140px;width:700px;height:700px;border-radius:50%;border:2px dashed rgba(125,24,252,.25)"></div>
<div class="abs" style="left:720px;top:250px;width:480px;height:480px;border-radius:50%;border:1.5px solid rgba(125,24,252,.18)"></div>
<img class="mascot" src="{IMG}mascot.webp" style="left:730px;top:200px;width:460px">
<div class="glass" style="left:330px;top:300px;width:250px;padding:22px;display:grid;gap:12px;border-radius:24px">{bars(150, 200)}</div>
<div class="glass" style="left:1340px;top:240px;width:260px;padding:22px;display:grid;gap:12px;border-radius:24px">{bars(120, 210, cls='')}</div>
<div class="glass" style="left:1360px;top:660px;width:250px;padding:20px;border-radius:24px;display:flex;gap:16px;align-items:center"><div class="tick">{TICK}</div><div style="display:grid;gap:10px">{bars(130, 90)}</div></div>
<div class="spark" style="left:520px;top:200px"></div><div class="spark s" style="left:1460px;top:540px"></div><div class="spark w s" style="left:640px;top:760px"></div><div class="spark s" style="left:1250px;top:150px"></div>'''
SCENES['02-dashboard'] = f'''<div class="orb" style="left:80px;top:300px;width:520px;height:520px;opacity:.35"></div>
<img class="mascot" src="{IMG}pose-point.webp" style="left:150px;top:330px;width:470px">
<div class="glass" style="left:720px;top:160px;width:540px;height:720px;padding:34px">
  <div style="display:flex;gap:16px;align-items:center;margin-bottom:34px"><div style="width:58px;height:58px;border-radius:50%;background:linear-gradient(140deg,#8B2DFF,#B46CFF)"></div><div style="display:grid;gap:10px">{bars(170, 110)}</div></div>
  <div class="bub in" style="position:relative;width:360px">{bars(280, 220)}</div>
  <div class="bub out" style="position:relative;width:330px;margin:20px 0 0 auto">{bars(250, 180)}</div>
  <div class="bub in" style="position:relative;width:300px;margin-top:20px">{bars(200)}</div>
  <div class="bub out" style="position:relative;width:280px;margin:20px 0 0 auto">{bars(210, 140)}</div></div>
<div class="glass" style="left:1310px;top:160px;width:460px;height:300px;padding:28px"><div class="bar d" style="width:150px;margin-bottom:18px"></div>
  <svg viewBox="0 0 400 200" style="width:100%;height:190px"><defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9B4DFF" stop-opacity=".35"/><stop offset="1" stop-color="#9B4DFF" stop-opacity="0"/></linearGradient></defs>
  <path d="M0 170 C60 165 90 140 140 145 S230 110 280 100 S360 40 400 25 L400 200 L0 200Z" fill="url(#lg)"/><path d="M0 170 C60 165 90 140 140 145 S230 110 280 100 S360 40 400 25" fill="none" stroke="#7D18FC" stroke-width="7" stroke-linecap="round"/><circle cx="400" cy="25" r="12" fill="#7D18FC"/></svg></div>
{cal(1310, 500, {2, 5, 8, 10, 13, 16, 19, 22, 24, 27})}
<div class="glass" style="left:1180px;top:860px;width:340px;padding:20px;border-radius:24px;display:flex;gap:16px;align-items:center"><div class="tick">{TICK}</div><div style="display:grid;gap:10px">{bars(170, 110)}</div></div>'''
SCENES['03-whatsapp-flow'] = f'''<svg class="abs" style="left:0;top:0" width="1920" height="1080"><defs><linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="#7D18FC"/><stop offset="1" stop-color="#B46CFF"/></linearGradient></defs>
  <g fill="none" stroke="url(#w)" stroke-width="6" stroke-linecap="round" stroke-dasharray="2 16"><path d="M470 540 C640 540 700 540 830 540"/><path d="M1090 540 C1200 540 1220 300 1350 300"/><path d="M1090 540 L1350 540"/><path d="M1090 540 C1200 540 1220 780 1350 780"/></g>
  <g fill="#7D18FC"><circle cx="830" cy="540" r="10"/><circle cx="1350" cy="300" r="10"/><circle cx="1350" cy="540" r="10"/><circle cx="1350" cy="780" r="10"/></g></svg>
<div class="glass" style="left:150px;top:440px;width:320px;padding:30px;border-radius:30px;background:linear-gradient(140deg,#DFF8EA,#FFFFFF);display:grid;gap:14px"><div style="display:flex;gap:12px"><span style="width:18px;height:18px;border-radius:50%;background:#25D366"></span><span style="width:18px;height:18px;border-radius:50%;background:#25D366;opacity:.6"></span><span style="width:18px;height:18px;border-radius:50%;background:#25D366;opacity:.35"></span></div>{bars(240, 180)}</div>
<div class="orb" style="left:760px;top:340px;width:400px;height:400px;opacity:.55"></div>
<div class="abs" style="left:830px;top:410px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle at 32% 28%,#fff 0,#E8D8FF 18%,#9B4DFF 55%,#5E06F2 100%);box-shadow:0 40px 80px -30px rgba(94,6,242,.8), inset 0 -20px 40px rgba(40,0,120,.35)"></div>
<div class="spark w" style="left:943px;top:520px;width:40px;height:40px;opacity:1"></div>
<div class="glass" style="left:1360px;top:220px;width:400px;height:160px;padding:30px;display:grid;gap:14px;align-content:center"><div class="bub out" style="position:relative;padding:18px 22px">{bars(260, 170)}</div></div>
<div class="glass" style="left:1360px;top:460px;width:400px;height:160px;padding:30px;display:flex;gap:22px;align-items:center"><div style="width:90px;height:90px;border-radius:20px;background:#F1ECFB;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding:12px">{''.join('<i style="border-radius:5px;background:' + ('#9B4DFF' if i in (1,4,6) else '#E1D6F9') + '"></i>' for i in range(9))}</div><div class="tick">{TICK}</div></div>
<div class="glass" style="left:1360px;top:700px;width:400px;height:160px;padding:30px;display:flex;gap:20px;align-items:center"><div style="width:76px;height:76px;border-radius:50%;background:linear-gradient(140deg,#FF8A3D,#FF4FA3)"></div><div style="display:grid;gap:12px">{bars(200, 140)}</div></div>
<div class="spark s" style="left:640px;top:380px"></div><div class="spark s" style="left:1220px;top:900px"></div>'''
SCENES['04-lead-capture'] = f'''<svg class="abs" style="left:0;top:0" width="1920" height="1080"><path d="M700 380 C900 180 1150 220 1290 470" fill="none" stroke="#9B4DFF" stroke-width="6" stroke-linecap="round" stroke-dasharray="2 18"/></svg>
<div class="abs" style="left:360px;top:150px;width:380px;height:760px;border-radius:64px;background:#fff;border:14px solid #ECE4FB;box-shadow:0 60px 100px -50px rgba(94,6,242,.55);transform:rotate(-8deg);padding:30px;display:grid;gap:22px;align-content:start">
  <div style="width:110px;height:12px;border-radius:9px;background:#E6DEFA;justify-self:center"></div>
  <div style="height:300px;border-radius:28px;background:radial-gradient(60% 60% at 30% 30%,#E6D2FF,transparent),linear-gradient(140deg,#B46CFF,#7D18FC)"></div>{bars(260, 200)}<div style="height:64px;border-radius:99px;background:linear-gradient(90deg,#7D18FC,#B46CFF)"></div></div>
<div class="glass" style="left:820px;top:300px;width:360px;padding:34px;display:grid;gap:18px;transform:rotate(6deg)">{bars(160, cls='d')}<div style="height:56px;border-radius:16px;border:2px solid #E6DEFA"></div><div style="height:56px;border-radius:16px;border:2px solid #E6DEFA"></div><div style="height:56px;border-radius:99px;background:linear-gradient(90deg,#7D18FC,#B46CFF)"></div></div>
<div class="glass" style="left:1250px;top:470px;width:520px;height:400px;padding:34px;display:grid;gap:16px;align-content:end;background:linear-gradient(180deg,rgba(255,255,255,.6),#fff)">
  <div class="glass" style="position:relative;inset:auto;padding:22px;border-radius:20px;opacity:.55;transform:scale(.92)">{bars(260)}</div>
  <div class="glass" style="position:relative;inset:auto;padding:22px;border-radius:20px;opacity:.8;transform:scale(.96)">{bars(300, 200)}</div>
  <div class="glass" style="position:relative;inset:auto;padding:22px;border-radius:20px;display:flex;gap:16px;align-items:center"><div style="width:54px;height:54px;border-radius:50%;background:linear-gradient(140deg,#8B2DFF,#B46CFF)"></div><div style="display:grid;gap:10px">{bars(260, 170)}</div></div></div>
<div class="tick abs" style="left:1720px;top:440px;width:84px;height:84px">{TICK}</div>
<div class="abs" style="left:1520px;top:170px;width:150px;height:290px;border-radius:34px;background:#fff;border:8px solid #ECE4FB;transform:rotate(10deg);box-shadow:0 30px 60px -30px rgba(94,6,242,.5)"><div style="margin:40px auto;width:40px;height:40px;border-radius:50%;background:#7D18FC;box-shadow:0 0 0 12px rgba(125,24,252,.15)"></div></div>
<div class="spark s" style="left:1050px;top:200px"></div><div class="spark" style="left:260px;top:840px"></div>'''
SCENES['05-content-website'] = f'''<div class="abs" style="left:220px;top:140px;width:360px;height:760px;border-radius:64px;background:#fff;border:14px solid #ECE4FB;box-shadow:0 60px 100px -50px rgba(94,6,242,.55);padding:26px;display:grid;gap:18px;align-content:start">
  <div style="height:470px;border-radius:30px;background:radial-gradient(50% 40% at 50% 35%,#F3E8FF,transparent),linear-gradient(170deg,#C898FF,#7D18FC 70%,#5E06F2);display:grid;place-items:center"><div style="width:110px;height:110px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;box-shadow:0 20px 40px -14px rgba(40,0,120,.6)"><div style="width:0;height:0;border-left:38px solid #7D18FC;border-top:24px solid transparent;border-bottom:24px solid transparent;margin-left:10px"></div></div></div>
  {bars(270, 190)}<div style="display:flex;gap:10px"><div class="bar v" style="width:120px;height:14px"></div><div class="bar" style="width:80px;height:14px"></div></div></div>
<div class="abs" style="left:610px;top:200px;display:grid;gap:18px">{''.join(f'<div class="glass" style="position:relative;inset:auto;width:250px;height:150px;border-radius:22px;padding:14px;opacity:{o}"><div style="height:100%;border-radius:14px;background:linear-gradient(150deg,{a},{b})"></div></div>' for a, b, o in [('#FFD5E8','#FF4FA3',1),('#D7E6FF','#3B82F6',.9),('#E6D2FF','#7D18FC',.8)])}</div>
<div class="abs" style="left:520px;top:120px;width:70px;height:62px;background:#FF4FA3;clip-path:path('M35 62 L6 33 C-6 20 2 0 18 0 C27 0 33 6 35 12 C37 6 43 0 52 0 C68 0 76 20 64 33Z')"></div>
<div class="abs" style="left:150px;top:560px;width:56px;height:50px;background:#B46CFF;clip-path:path('M28 50 L5 26 C-5 16 2 0 14 0 C21 0 26 5 28 10 C30 5 35 0 42 0 C54 0 61 16 51 26Z')"></div>
<div class="glass" style="left:930px;top:180px;width:820px;height:560px;padding:0;overflow:hidden">
  <div style="height:58px;background:#F7F3FF;display:flex;gap:12px;align-items:center;padding:0 26px;border-bottom:1.5px solid #EEE6FD"><i style="width:16px;height:16px;border-radius:50%;background:#FF8A9E"></i><i style="width:16px;height:16px;border-radius:50%;background:#FFC86B"></i><i style="width:16px;height:16px;border-radius:50%;background:#5FD49A"></i><div style="margin-left:24px;width:300px;height:22px;border-radius:99px;background:#EDE6FB"></div></div>
  <div style="padding:34px;display:grid;grid-template-columns:1.2fr 1fr;gap:28px"><div style="display:grid;gap:18px;align-content:center">{bars(360, cls='d')}{bars(300, 240)}<div style="width:190px;height:58px;border-radius:99px;background:linear-gradient(90deg,#7D18FC,#B46CFF)"></div></div>
  <div style="height:230px;border-radius:24px;background:radial-gradient(60% 60% at 30% 30%,#F0E4FF,transparent),linear-gradient(140deg,#D9BFFF,#9B4DFF)"></div></div>
  <div style="padding:0 34px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{''.join('<div style="height:120px;border-radius:20px;background:#F6F1FF;border:1.5px solid #EEE6FD"></div>' for _ in range(3))}</div></div>
<div class="glass" style="left:1560px;top:650px;width:250px;height:250px;border-radius:50%;display:grid;place-items:center"><svg viewBox="0 0 100 100" style="width:190px"><circle cx="50" cy="50" r="40" fill="none" stroke="#E9F7F0" stroke-width="10"/><circle cx="50" cy="50" r="40" fill="none" stroke="#0B9B68" stroke-width="10" stroke-linecap="round" stroke-dasharray="251" stroke-dashoffset="8" transform="rotate(-90 50 50)"/></svg></div>
<div class="abs" style="left:1130px;top:790px;width:300px;height:220px;border-radius:40px;background:#fff;border:10px solid #ECE4FB;box-shadow:0 30px 60px -30px rgba(94,6,242,.5);padding:20px;display:grid;gap:12px">{bars(200, cls='d')}{bars(240, 160)}</div>'''
heights = [140, 210, 270, 360, 450, 560]
SCENES['06-growth'] = f'''<div class="orb" style="left:80px;top:360px;width:520px;height:520px;opacity:.35"></div>
<img class="mascot" src="{IMG}pose-celebrate.webp" style="left:130px;top:380px;width:470px">
<div class="glass" style="left:660px;top:170px;width:1100px;height:720px;padding:60px 70px">
  <div class="bar d" style="width:220px"></div>
  <div style="position:absolute;left:70px;right:70px;bottom:60px;height:580px;display:flex;align-items:flex-end;gap:44px">{''.join(f'<div style="flex:1;height:{h}px;border-radius:22px 22px 10px 10px;background:linear-gradient(180deg,{"#B46CFF" if i == 5 else "#C9A4FF"},{"#5E06F2" if i == 5 else "#9B4DFF"});opacity:{0.55 + i * 0.09}"></div>' for i, h in enumerate(heights))}</div>
  <svg style="position:absolute;left:70px;right:70px;bottom:60px" width="960" height="600" viewBox="0 0 960 600"><path d="M40 470 C200 440 260 380 380 330 S600 220 700 160 S860 60 930 40" fill="none" stroke="#140B2E" stroke-opacity=".75" stroke-width="7" stroke-linecap="round"/><circle cx="930" cy="40" r="14" fill="#140B2E"/></svg></div>
<div class="spark" style="left:1640px;top:150px;width:60px;height:60px"></div><div class="spark w" style="left:1600px;top:240px"></div><div class="spark s" style="left:1720px;top:250px"></div>
<div class="glass" style="left:1500px;top:820px;width:290px;padding:20px;border-radius:24px;display:flex;gap:16px;align-items:center"><div class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div><div style="display:grid;gap:10px">{bars(150, 100)}</div></div>'''
SCENES['07-end-card'] = f'''<div class="orb" style="left:560px;top:180px;width:800px;height:700px;opacity:.35"></div>
<div class="abs" style="left:0;right:0;top:300px;display:grid;justify-items:center;gap:56px">
  <div style="display:flex;align-items:center;gap:44px"><div class="tile" style="width:220px;height:220px;border-radius:58px">{ROCKET}</div><div style="width:900px">{WORD_DARK.replace('class="lg-word"', 'style="width:100%;height:auto;display:block"')}</div></div>
  <div style="display:flex;align-items:center;gap:26px;font:700 44px S"><span style="padding:24px 48px;border-radius:99px;background:linear-gradient(90deg,#7D18FC,#B46CFF);color:#fff;box-shadow:0 24px 40px -20px rgba(94,6,242,.8)">Book a free call</span><span style="color:#4D4570">nxtlvlsocial.ai</span></div></div>
<div class="spark s" style="left:520px;top:260px"></div><div class="spark" style="left:1440px;top:740px"></div>'''
LOGO = {
 'logo-frame-1x1': ('sq', f'<div class="orb" style="left:290px;top:290px;width:500px;height:500px;opacity:.35"></div><div class="tile abs" style="left:290px;top:290px;width:500px;height:500px;border-radius:128px">{ROCKET}</div>'),
 'logo-frame-16x9': ('', f'<div class="orb" style="left:560px;top:290px;width:500px;height:500px;opacity:.35"></div><div class="tile abs" style="left:560px;top:290px;width:500px;height:500px;border-radius:128px">{ROCKET}</div>'),
}
TRANSPARENT = {
 'nxtlvl-social-rocket-tile.png': (1024, 1024, f'<div class="tile" style="width:1024px;height:1024px;border-radius:230px;box-shadow:none">{ROCKET}</div>'),
 'nxtlvl-social-rocket-mark.png': (1024, 1024, f'<div style="width:1024px;height:1024px;display:grid;place-items:center">{ROCKET.replace("<svg ", "<svg style=\"width:86%;height:86%\" ")}</div>'),
 'nxtlvl-social-logo-lockup.png': (2400, 520, f'<div style="width:2400px;height:520px;display:flex;align-items:center;gap:90px;padding:0 40px"><div class="tile" style="width:440px;height:440px;border-radius:112px;box-shadow:none;flex:none">{ROCKET}</div><div style="flex:1">{WORD_DARK.replace("class=\"lg-word\"", "style=\"width:100%;height:auto;display:block\"")}</div></div>'),
}

def page(body, cls=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body><div class="stage {cls}">{body}</div></body></html>'

if __name__ == '__main__':
    import json
    jobs = []
    for name, body in SCENES.items():
        p = os.path.join(WORK, name + '.html'); open(p, 'w').write(page(body)); jobs.append([p, OUT + '/frames/' + name + '.png', 1920, 1080, False])
    for name, (cls, body) in LOGO.items():
        p = os.path.join(WORK, name + '.html'); open(p, 'w').write(page(body, cls)); jobs.append([p, OUT + '/logo/' + name + '.png', 1080 if cls else 1920, 1080, False])
    for name, (w, h, body) in TRANSPARENT.items():
        p = os.path.join(WORK, name + '.html')
        open(p, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS} body{{background:transparent}}</style></head><body>{body}</body></html>')
        jobs.append([p, OUT + '/logo/' + name, w, h, True])
    os.makedirs(OUT + '/frames', exist_ok=True); os.makedirs(OUT + '/logo', exist_ok=True)
    json.dump(jobs, open(os.path.join(WORK, 'jobs.json'), 'w'))
    print(len(jobs), 'pages written')
