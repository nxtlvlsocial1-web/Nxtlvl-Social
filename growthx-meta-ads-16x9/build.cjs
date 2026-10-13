// Run: node build.cjs  (regenerates index.html; edit word timings in the scenes list)
// Generates growthx-meta-ads-16x9/index.html (static clips, one paused GSAP timeline).
const fs = require("fs");
const out = process.argv[2] || require("path").join(__dirname, "index.html");
const DUR = 41.2;

// w(text, t, cls) — one spoken word, revealed at global time t.
const w = (text, t, cls = "") => ({ text, t, cls });

// Scenes: start, end, lines of words, plus optional extra HTML + extra tweens.
const scenes = [
  { id: "s1", start: 6.35, end: 8.5, lines: [
      [w("agar", 6.6, "sm"), w("apne", 6.78, "sm")],
      [w("D2C", 7.0, "xl lime"), w("BRAND", 7.15, "xl lime")],
      [w("abhi", 7.6, "md"), w("start", 7.75, "md"), w("kiya", 7.92, "md"), w("hai", 8.05, "md")],
    ] },
  { id: "s2", start: 8.5, end: 12.0, lines: [
      [w("to", 8.6, "sm"), w("yeh", 8.78, "sm")],
      [w("META", 9.4, "lg hl"), w("AD", 9.58, "lg hl"), w("STRATEGY", 9.76, "lg hl")],
      [w("apko", 10.3, "md"), w("direct", 10.5, "md")],
      [w("CUSTOMER", 11.0, "lg lime"), w("lake", 11.3, "md"), w("degi", 11.48, "md")],
    ] },
  { id: "s3", start: 12.0, end: 12.9, lines: [
      [w("karna", 12.0, "md"), w("kuch", 12.15, "md")],
      [w("NAHI", 12.32, "xl red"), w("HAI", 12.5, "xl red")],
    ], shake: 12.4 },
  { id: "s4", start: 12.9, end: 16.2, top: true, lines: [
      [w("bss", 13.0, "md"), w("EK", 13.18, "lg lime"), w("campaign", 13.42, "md"), w("bnao", 13.65, "md")],
    ], extra: `
      <div class="ui-card" id="s4-card">
        <div class="ui-label">CAMPAIGN OBJECTIVE</div>
        <div class="chips">
          <div class="chip" id="s4-c1">Awareness</div>
          <div class="chip" id="s4-c2">Traffic</div>
          <div class="chip on" id="s4-c3"><span class="tick">✓</span> Sales</div>
        </div>
        <div class="ui-row"><span class="ui-k">Goal</span><span class="ui-v" id="s4-conv">Conversion</span></div>
        <div class="ui-foot" id="s4-foot"><span class="w-inline" id="s4-ob">objective</span> <span class="w-inline" id="s4-ke">ke</span></div>
      </div>`,
    tweens: (A) => {
      A.pop("#s4-card", 13.8, 0.45);
      A.pop("#s4-c1", 13.9); A.pop("#s4-c2", 13.95); A.pop("#s4-c3", 14.0);
      A.flash("#s4-c3", 14.05);
      A.pop("#s4-conv", 14.4);
      A.pop("#s4-ob", 14.9); A.pop("#s4-ke", 15.4);
    } },
  { id: "s5", start: 16.2, end: 18.4, lines: [
      [w("aur", 16.4, "md"), w("usmei", 16.58, "md")],
      [w("3", 17.0, "huge lime", "s5-num"), w("AD SETS", 17.18, "lg")],
      [w("add", 17.5, "md"), w("karo", 17.68, "md")],
    ], shake: 17.05 },
  { id: "s6", start: 18.4, end: 22.8, top: true, lines: [
      [w("3 AD SETS", 18.45, "sm dim")],
    ], extra: `
      <div class="sets">
        ${["Broad Audience|globe|01", "Interest Targeting|target|02", "Lookalike Audience|people|03"].map((s, i) => {
          const [name, icon, n] = s.split("|");
          return `<div class="set" id="s6-set${i}"><div class="set-n">${n}</div><div class="ico ico-${icon}"></div><div class="set-name">${name}</div></div>`;
        }).join("")}
      </div>`,
    tweens: (A) => {
      [18.5, 20.0, 21.0].forEach((t, i) => { A.pop(`#s6-set${i}`, t, 0.45); A.activate(`#s6-set${i}`, t, [18.5, 20.0, 21.0][i + 1]); });
    } },
  { id: "s7", start: 22.8, end: 25.45, split: true, lines: [
      [w("jo", 22.75, "md"), w("apki", 22.85, "md")],
      [w("WEBSITE", 22.95, "lg lime"), w("VISIT", 23.1, "lg lime")],
      [w("ya", 23.2, "md"), w("VIDEO", 23.3, "lg"), w("VIEWS", 23.45, "lg")],
      [w("pe", 23.55, "md"), w("based", 23.65, "md"), w("ho", 23.8, "md")],
    ], extra: `
      <div class="browser" id="s7-browser">
        <div class="bar"><i></i><i></i><i></i><div class="url">yourbrand.com</div></div>
        <div class="viewport"></div>
      </div>`,
    noDrift: true,
    tweens: (A) => { T(`tl.fromTo("#s7-browser",{opacity:0},{opacity:1,duration:.15},22.8);`); } },
  { id: "s8", start: 25.45, end: 28.1, lines: [
      [w("aur", 25.5, "md"), w("jisne", 25.75, "md"), w("apke", 26.0, "md")],
      [w("INSTAGRAM", 26.2, "xl ig")],
      [w("pe", 26.9, "md"), w("engage", 27.05, "md lime"), w("kiya", 27.5, "md"), w("hai", 27.65, "md")],
    ], extra: `
      <div class="float f1" id="s8-f1">♥ 2.4K</div>
      <div class="float f2" id="s8-f2">💬 318</div>
      <div class="float f3" id="s8-f3">↗ 1.1K</div>`,
    tweens: (A) => { A.pop("#s8-f1", 26.95); A.pop("#s8-f2", 27.15); A.pop("#s8-f3", 27.35); } },
  { id: "s9", start: 28.1, end: 29.6, lines: [
      [w("usko", 28.2, "md")],
      [w("LOOKALIKE", 28.4, "xl lime")],
      [w("mei", 28.9, "md"), w("daldo", 29.05, "md")],
    ], extra: `<div class="dots" id="s9-dots">${Array.from({ length: 24 }, (_, i) => `<b class="dot" style="--i:${i}"></b>`).join("")}</div>`,
    tweens: (A) => { A.dots("#s9-dots .dot", 28.3); } },
  { id: "s10", start: 29.6, end: 31.9, lines: [
      [w("aur", 29.85, "md")],
      [w("CREATIVE", 30.0, "xl lime")],
      [w("jo", 30.5, "md"), w("sabse", 30.65, "md")],
      [w("IMPORTANT", 31.0, "lg hl"), w("hai", 31.3, "md")],
    ], extra: `
      <div class="cards">
        <div class="ad ad1" id="s10-a1"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
        <div class="ad ad2" id="s10-a2"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
        <div class="ad ad3" id="s10-a3"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
      </div>`,
    tweens: (A) => { A.fan(["#s10-a1", "#s10-a2", "#s10-a3"], 30.0); } },
  { id: "s11", start: 31.9, end: 33.6, lines: [
      [w("SALES", 32.0, "xl lime")],
      [w("ko", 32.45, "md"), w("scale", 32.55, "md"), w("karne", 32.7, "md"), w("ke", 32.82, "md"), w("liye", 32.92, "md")],
    ], extra: `
      <svg class="chart" viewBox="0 0 1600 600" id="s11-chart"><path id="s11-line" d="M0 560 L260 500 L480 520 L720 380 L960 400 L1200 210 L1420 120 L1600 30" /></svg>`,
    tweens: (A) => { A.draw("#s11-line", 32.0, 1.4); } },
  { id: "s12", start: 33.6, end: 36.3, lines: [
      [w("Full", 34.0, "lg"), w("Detailed", 34.2, "lg")],
      [w("PDF", 34.45, "xl lime"), w("chahiye?", 34.65, "lg")],
    ], extra: `
      <div class="follow" id="s12-btn"><span class="f-a">+ FOLLOW</span><span class="f-b" id="s12-done">✓ FOLLOWING</span></div>
      <div class="cursor" id="s12-cur"></div>`,
    tweens: (A) => { A.follow(34.9); } },
  { id: "s13", start: 36.3, end: 38.3, lines: [
      [w("aur", 36.5, "md"), w("meri", 36.65, "md")],
      [w("WhatsApp", 36.8, "xl wa"), w("Community", 37.05, "xl wa")],
      [w("join", 37.5, "md"), w("karo", 37.68, "md")],
    ] },
  { id: "s14", start: 38.3, end: DUR, top: true, lines: [
      [w("jiska", 38.5, "md"), w("link", 38.65, "md"), w("apko", 38.8, "md")],
      [w("BIO", 39.0, "xl lime"), w("mei", 39.15, "lg"), w("mil", 39.3, "lg"), w("jayega", 39.48, "lg")],
    ], extra: `
      <div class="cta" id="s14-cta">
        <div class="pill" id="s14-pill">LINK IN BIO ↗</div>
        <div class="mail" id="s14-mail"><span class="mail-ico">✉</span> thegrowthxstudio@gmail.com</div>
      </div>`,
    tweens: (A) => { A.pop("#s14-pill", 39.8, 0.45); A.pop("#s14-mail", 40.05, 0.45); } },
];

const wipes = [6.35, 12.9, 18.4, 22.8, 25.45, 29.6, 33.6, 38.3];

let wordId = 0;
const words = [];
const sceneHtml = scenes.map((s, si) => {
  const lines = s.lines.map((line) => `<div class="line">${line.map((x) => {
    const id = `w${wordId++}`; words.push({ id, t: x.t, cls: x.cls });
    return `<span class="w ${x.cls}" id="${id}"><span class="wi">${x.text}</span></span>`;
  }).join("")}</div>`).join("\n");
  const layout = s.split ? "split" : s.top ? "top" : "center";
  return `
    <section id="${s.id}" class="clip scene ${layout}" data-start="${s.start}" data-duration="${(s.end - s.start).toFixed(2)}" data-track-index="${2 + (si % 2)}">
      <div class="stage" id="${s.id}-stage">
        <div class="text">${lines}</div>
        ${s.extra || ""}
      </div>
    </section>`;
}).join("\n");

// --- timeline script ---
const js = [];
const T = (s) => js.push(s);
const A = {
  pop: (sel, t, d = 0.35) => T(`tl.fromTo("${sel}",{opacity:0,y:50,scale:.85},{opacity:1,y:0,scale:1,duration:${d},ease:"back.out(2)"},${t});`),
  flash: (sel, t) => T(`tl.fromTo("${sel}",{boxShadow:"0 0 0 0 rgba(200,255,46,.9)"},{boxShadow:"0 0 0 18px rgba(200,255,46,0)",duration:.6,ease:"power2.out",immediateRender:false},${t});`),
  drift: (sel, t, d) => T(`tl.to("${sel}",{scale:1.04,duration:${d},ease:"none"},${t + 0.5});`),
  activate: (sel, t, next) => {
    T(`tl.to("${sel}",{borderColor:"#C8FF2E",backgroundColor:"rgba(200,255,46,.12)",duration:.2},${t});`);
    if (next) T(`tl.to("${sel}",{borderColor:"rgba(255,255,255,.14)",backgroundColor:"rgba(255,255,255,.04)",duration:.2},${next});`);
  },
  dots: (sel, t) => T(`tl.fromTo("${sel}",{opacity:0,scale:0},{opacity:1,scale:1,duration:.3,ease:"back.out(3)",stagger:{each:.035,from:"start"}},${t});`),
  fan: (sels, t) => {
    const rot = [-14, 0, 14], x = [-520, 0, 520];
    sels.forEach((s, i) => T(`tl.fromTo("${s}",{opacity:0,x:0,y:200,rotation:0},{opacity:.9,x:${x[i]},y:${i === 1 ? -20 : 40},rotation:${rot[i]},duration:.55,ease:"back.out(1.6)"},${t + i * 0.08});`));
  },
  draw: (sel, t, d) => T(`(function(){const p=document.querySelector("${sel}");const L=p.getTotalLength();tl.fromTo(p,{strokeDasharray:L,strokeDashoffset:L},{strokeDashoffset:0,duration:${d},ease:"power2.inOut"},${t});})();`),
  follow: (t) => {
    T(`tl.fromTo("#s12-btn",{opacity:0,y:60,scale:.8},{opacity:1,y:0,scale:1,duration:.4,ease:"back.out(2)"},${t});`);
    T(`tl.fromTo("#s12-cur",{opacity:0,x:260,y:200},{opacity:1,x:0,y:0,duration:.45,ease:"power3.out"},${t + 0.2});`);
    T(`tl.to("#s12-btn",{scale:.92,duration:.08,yoyo:true,repeat:1},${t + 0.65});`);
    T(`tl.to("#s12-btn",{backgroundColor:"#0B0D12",borderColor:"#C8FF2E",color:"#C8FF2E",duration:.1},${t + 0.7});`);
    T(`tl.fromTo("#s12-done",{yPercent:100},{yPercent:0,duration:.2,ease:"power2.out"},${t + 0.7});`);
    T(`tl.to("#s12-btn .f-a",{yPercent:-100,opacity:0,duration:.2},${t + 0.7});`);
  },
};

// Hook: slow push-in on the original clip + tag.
T(`tl.fromTo("#hook-wrap",{scale:1},{scale:1.12,duration:6.35,ease:"none"},0);`);
T(`tl.fromTo("#hook-tag",{opacity:0,y:-30},{opacity:1,y:0,duration:.4,ease:"back.out(2)"},0.15);`);
T(`tl.fromTo("#hook-tag2",{opacity:0,x:-40},{opacity:1,x:0,duration:.4,ease:"power3.out"},0.35);`);

words.forEach((x) => {
  T(`tl.fromTo("#${x.id} .wi",{opacity:0,yPercent:70,scale:.8},{opacity:1,yPercent:0,scale:1,duration:.26,ease:"back.out(2.2)"},${x.t});`);
  if (/\b(xl|huge)\b/.test(x.cls)) T(`tl.fromTo("#${x.id}",{scale:1.25},{scale:1,duration:.35,ease:"power3.out"},${x.t});`);
  if (/\bhl\b/.test(x.cls)) T(`tl.fromTo("#${x.id}",{"--hl":0},{"--hl":1,duration:.25,ease:"power2.out"},${x.t + 0.08});`);
});

scenes.forEach((s) => {
  if (!s.noDrift) T(`tl.fromTo("#${s.id}-stage",{scale:1},{scale:1.05,duration:${(s.end - s.start).toFixed(2)},ease:"none"},${s.start});`);
  if (s.shake) T(`tl.fromTo("#${s.id}-stage",{x:-14},{x:0,duration:.35,ease:"elastic.out(1.4,.3)",immediateRender:false},${s.shake});`);
  if (s.tweens) s.tweens(A);
});

// Counter 1→3 on the "3".

// Transitions: lime wipe + white flash.
wipes.forEach((t, i) => {
  T(`tl.fromTo("#wipe .wp",{xPercent:-130},{xPercent:130,duration:.42,ease:"power3.inOut"${i ? ",immediateRender:false" : ""}},${(t - 0.21).toFixed(2)});`);
});
T(`tl.fromTo("#flash",{opacity:.85},{opacity:0,duration:.25,ease:"power2.out",immediateRender:false},6.35);`);

// Background glow drift.
T(`tl.fromTo("#glow",{xPercent:-20,yPercent:-10},{xPercent:20,yPercent:10,duration:${DUR},ease:"sine.inOut"},0);`);
// Progress bar.
T(`tl.fromTo("#progress i",{scaleX:0},{scaleX:1,duration:${DUR},ease:"none"},0);`);

const html = `<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>GrowthX Meta Ads Strategy</title>
    <script src="vendor/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Display"; src: url("fonts/InterDisplay-Black.otf"); font-weight: 900; }
      @font-face { font-family: "Display"; src: url("fonts/InterDisplay-Bold.otf"); font-weight: 700; }
      @font-face { font-family: "Display"; src: url("fonts/InterDisplay-SemiBold.otf"); font-weight: 600; }
      :root { --bg:#07080C; --ink:#F5F5F0; --lime:#C8FF2E; --dim:#8A8F98; --red:#FF3D3D; --wa:#25D366; }
      * { margin:0; padding:0; box-sizing:border-box; }
      html, body { width:1920px; height:1080px; overflow:hidden; background:var(--bg); }
      #root { position:relative; width:100%; height:100%; overflow:hidden; font-family:"Display", sans-serif; color:var(--ink); }
      .bg { position:absolute; inset:0; background:var(--bg); }
      .grid { position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px); background-size:80px 80px; }
      #glow { position:absolute; left:460px; top:140px; width:1000px; height:800px; border-radius:50%; background:radial-gradient(closest-side,rgba(200,255,46,.16),rgba(200,255,46,0)); }
      .vignette { position:absolute; inset:0; background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.6) 100%); }

      #hook-wrap { position:absolute; inset:0; overflow:hidden; }
      #hook { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
      .hook-ui { position:absolute; inset:0; }
      #hook-tag { position:absolute; left:80px; top:70px; background:var(--lime); color:#07080C; font-weight:900; font-size:40px; padding:14px 28px; border-radius:14px; letter-spacing:.02em; }
      #hook-tag2 { position:absolute; left:80px; top:160px; background:rgba(7,8,12,.94); color:var(--ink); font-weight:700; font-size:34px; padding:12px 24px; border-radius:12px; border:2px solid rgba(200,255,46,.6); }

      .scene { position:absolute; inset:0; }
      .stage { position:absolute; inset:0; isolation:isolate; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:40px; }
      .scene.top .stage { justify-content:flex-start; padding-top:150px; }
      .scene.split .stage { flex-direction:row; justify-content:space-between; padding:0 110px; }
      .scene.split .text { align-items:flex-start; text-align:left; width:760px; margin-left:auto; }
      .text { display:flex; flex-direction:column; align-items:center; text-align:center; gap:6px; }
      .line { display:flex; flex-wrap:wrap; justify-content:center; align-items:baseline; gap:0 26px; }
      .scene.split .line { justify-content:flex-start; }
      .w { display:inline-block; position:relative; line-height:1.05; }
      .wi { display:inline-block; position:relative; }
      .sm { font-size:64px; font-weight:600; color:var(--dim); }
      .md { font-size:84px; font-weight:700; }
      .lg { font-size:128px; font-weight:900; letter-spacing:-.02em; }
      .xl { font-size:200px; font-weight:900; letter-spacing:-.035em; line-height:.95; }
      .huge { font-size:340px; font-weight:900; line-height:.9; }
      .lime { color:var(--lime); }
      .red { color:var(--red); }
      .dim { color:var(--dim); letter-spacing:.2em; }
      .wa { color:var(--wa); font-size:150px; }
      .ig .wi { background:linear-gradient(90deg,#FEDA75,#FA7E1E,#D62976,#962FBF,#4F5BD5); -webkit-background-clip:text; background-clip:text; color:transparent; padding:0 6px; }
      .hl { --hl:0; color:#07080C; }
      .hl::before { content:""; position:absolute; left:-12px; right:-12px; top:8%; bottom:4%; background:var(--lime); border-radius:14px; transform-origin:left center; transform:scaleX(var(--hl)); }
      .hl.lg { color:#07080C; }

      .ui-card { width:900px; padding:44px 50px; border-radius:28px; background:rgba(255,255,255,.05); border:2px solid rgba(255,255,255,.14); display:flex; flex-direction:column; gap:30px; }
      .ui-label { font-size:28px; font-weight:700; color:var(--dim); letter-spacing:.2em; }
      .chips { display:flex; gap:20px; }
      .chip { font-size:40px; font-weight:700; padding:16px 30px; border-radius:999px; border:2px solid rgba(255,255,255,.2); color:var(--dim); }
      .chip.on { background:var(--lime); color:#07080C; border-color:var(--lime); }
      .tick { font-weight:900; }
      .ui-row { display:flex; justify-content:space-between; align-items:center; font-size:48px; padding-top:22px; border-top:2px solid rgba(255,255,255,.1); }
      .ui-k { color:var(--dim); font-weight:600; }
      .ui-v { color:var(--lime); font-weight:900; font-size:64px; display:inline-block; }
      .ui-foot { font-size:56px; font-weight:700; text-align:center; }
      .w-inline { display:inline-block; }

      .sets { display:flex; gap:44px; margin-top:40px; }
      .set { width:500px; height:520px; border-radius:32px; border:3px solid rgba(255,255,255,.14); background:rgba(255,255,255,.04); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:36px; position:relative; }
      .set-n { position:absolute; top:28px; left:34px; font-size:40px; font-weight:900; color:var(--lime); }
      .set-name { font-size:58px; font-weight:900; text-align:center; line-height:1.05; padding:0 30px; }
      .ico { width:150px; height:150px; position:relative; }
      .ico-globe { border:10px solid var(--lime); border-radius:50%; }
      .ico-globe::before { content:""; position:absolute; inset:0 38px; border:8px solid var(--lime); border-radius:50%; }
      .ico-globe::after { content:""; position:absolute; left:0; right:0; top:61px; height:8px; background:var(--lime); }
      .ico-target { border:10px solid var(--lime); border-radius:50%; }
      .ico-target::before { content:""; position:absolute; inset:24px; border:10px solid var(--lime); border-radius:50%; }
      .ico-target::after { content:""; position:absolute; inset:54px; background:var(--lime); border-radius:50%; }
      .ico-people::before, .ico-people::after { content:""; position:absolute; width:62px; height:62px; border-radius:50%; background:var(--lime); top:14px; box-shadow:0 78px 0 18px var(--lime); }
      .ico-people::before { left:10px; opacity:.45; }
      .ico-people::after { right:22px; }

      .browser { position:absolute; left:110px; top:234px; width:900px; border-radius:22px; overflow:hidden; background:#fff; box-shadow:0 40px 120px rgba(0,0,0,.6), 0 0 0 3px rgba(200,255,46,.5); order:1; }
      .bar { height:56px; background:#1A1D24; display:flex; align-items:center; gap:12px; padding:0 22px; }
      .bar i { width:16px; height:16px; border-radius:50%; background:#3A3F4A; }
      .bar i:first-child { background:#FF5F57; } .bar i:nth-child(2) { background:#FEBC2E; } .bar i:nth-child(3) { background:#28C840; }
      .url { margin-left:20px; flex:1; height:34px; border-radius:10px; background:#0B0D12; color:var(--dim); font-size:20px; font-weight:600; display:flex; align-items:center; padding-left:18px; }
      .viewport { position:relative; width:900px; height:556px; background:#fff; }
      #website { position:absolute; left:110px; top:290px; width:900px; height:556px; object-fit:cover; }

      .float { position:absolute; font-size:44px; font-weight:900; padding:16px 28px; border-radius:20px; background:rgba(255,255,255,.08); border:2px solid rgba(255,255,255,.18); }
      .f1 { left:170px; top:230px; color:#FF4D79; }
      .f2 { right:180px; top:280px; }
      .f3 { right:300px; bottom:170px; color:var(--lime); }

      .dots { position:absolute; left:50%; bottom:110px; width:720px; margin-left:-360px; display:flex; flex-wrap:wrap; gap:18px; justify-content:center; }
      .dot { display:block; width:42px; height:42px; border-radius:50%; background:var(--lime); }
      .dot:nth-child(-n+6) { background:var(--ink); }

      .cards { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; z-index:-1; }
      .ad { position:absolute; width:400px; height:560px; border-radius:28px; background:#151821; border:2px solid rgba(255,255,255,.12); padding:24px; display:flex; flex-direction:column; gap:18px; }
      .ad-img { height:380px; border-radius:18px; background:linear-gradient(135deg,#2A3140,#11141B); }
      .ad1 .ad-img { background:linear-gradient(135deg,#C8FF2E,#4E7A00); }
      .ad3 .ad-img { background:linear-gradient(135deg,#FA7E1E,#962FBF); }
      .ad-l { height:22px; border-radius:11px; background:rgba(255,255,255,.18); }
      .ad-l.s { width:60%; }
      #s10 .text { position:relative; z-index:2; background:rgba(7,8,12,.78); padding:30px 60px; border-radius:30px; }

      .chart { position:absolute; left:160px; bottom:120px; width:1600px; height:600px; z-index:-1; }
      .chart path { fill:none; stroke:var(--lime); stroke-width:14; stroke-linecap:round; stroke-linejoin:round; opacity:.55; }

      .follow { position:relative; overflow:hidden; height:110px; width:520px; border-radius:24px; background:#2F6BFF; border:4px solid #2F6BFF; color:#fff; font-size:50px; font-weight:900; }
      .f-a, .f-b { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }
            .cursor { position:absolute; left:1080px; top:780px; width:0; height:0; border-left:28px solid transparent; border-right:28px solid transparent; border-bottom:70px solid #fff; transform-origin:center; rotate:-30deg; filter:drop-shadow(0 6px 10px rgba(0,0,0,.6)); }

      .cta { display:flex; flex-direction:column; align-items:center; gap:30px; margin-top:30px; }
      .pill { background:var(--lime); color:#07080C; font-size:64px; font-weight:900; padding:22px 56px; border-radius:999px; }
      .mail { font-size:46px; font-weight:700; padding:18px 40px; border-radius:20px; background:rgba(255,255,255,.06); border:2px solid rgba(255,255,255,.2); }
      .mail-ico { color:var(--lime); }

      #wipe { position:absolute; inset:0; overflow:hidden; pointer-events:none; }
      #wipe .wp { position:absolute; top:-20%; bottom:-20%; left:0; width:100%; background:var(--lime); transform:skewX(-18deg); }
      #flash { position:absolute; inset:0; background:#fff; opacity:0; }
      #progress { position:absolute; left:0; right:0; bottom:0; height:10px; background:rgba(255,255,255,.08); }
      #progress i { display:block; height:100%; background:var(--lime); transform-origin:left center; }
      #brand { position:absolute; right:60px; top:50px; font-size:30px; font-weight:900; letter-spacing:.06em; color:rgba(245,245,240,.75); }
      #brand b { color:var(--lime); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${DUR}" data-width="1920" data-height="1080">
      <div class="bg"></div>
      <div class="grid"></div>
      <div id="glow"></div>
      <div class="vignette"></div>

      <div id="hook-wrap">
        <video id="hook" src="assets/hook.mp4" muted playsinline data-start="0" data-duration="6.35" data-track-index="1"></video>
      </div>
      <div class="hook-ui clip" id="hook-ui" data-start="0" data-duration="6.35" data-track-index="4">
        <div id="hook-tag">D2C FOUNDERS</div>
        <div id="hook-tag2">Meta Ads ka simple formula</div>
      </div>

      ${sceneHtml}

      <video id="website" src="assets/website.mp4" muted playsinline data-start="22.85" data-duration="2.4" data-track-index="5"></video>

      <div id="wipe" class="clip" data-start="0" data-duration="${DUR}" data-track-index="6"><div class="wp"></div></div>
      <div id="flash" class="clip" data-start="0" data-duration="${DUR}" data-track-index="7"></div>
      <div id="brand" class="clip" data-start="6.35" data-duration="${(DUR - 6.35).toFixed(2)}" data-track-index="8">GROWTH<b>X</b> STUDIO</div>
      <div id="progress" class="clip" data-start="0" data-duration="${DUR}" data-track-index="9"><i></i></div>

      <audio id="vo" src="assets/voiceover.m4a" data-start="0" data-duration="40.29" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      ${js.join("\n      ")}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
fs.writeFileSync(out, html);
console.log("wrote", out, words.length, "words");
