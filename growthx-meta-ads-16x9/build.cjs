// Run: node build.cjs  (regenerates index.html; edit word timings in the scenes list)
// Generates growthx-meta-ads-16x9/index.html (static clips, one paused GSAP timeline).
const fs = require("fs");
const out = process.argv[2] || require("path").join(__dirname, "index.html");
const DUR = 41.6;
const sfx = [];
const S = (t, type, vol = 1) => sfx.push({ t: +t.toFixed(3), type, vol });

// w(text, t, cls) — one spoken word, revealed at global time t.
const w = (text, t, cls = "") => ({ text, t, cls });

// Scenes: start, end, lines of words, plus optional extra HTML + extra tweens.
const scenes = [
  { id: "s1", start: 6.35, end: 8.5, lines: [
      [w("agar", 6.6, "sm"), w("apne", 6.78, "sm")],
      [w("D2C", 7.0, "xl acc"), w("BRAND", 7.15, "xl acc")],
      [w("abhi", 7.6, "md"), w("start", 7.75, "md"), w("kiya", 7.92, "md"), w("hai", 8.05, "md")],
    ] },
  { id: "s2", start: 8.5, end: 12.0, lines: [
      [w("to", 8.6, "sm"), w("yeh", 8.78, "sm")],
      [w("META", 9.4, "lg hl"), w("AD", 9.58, "lg hl"), w("STRATEGY", 9.76, "lg hl")],
      [w("apko", 10.3, "md"), w("direct", 10.5, "md")],
      [w("CUSTOMER", 11.0, "lg acc"), w("lake", 11.3, "md"), w("degi", 11.48, "md")],
    ] },
  { id: "s3", start: 12.0, end: 12.9, lines: [
      [w("karna", 12.0, "md"), w("kuch", 12.15, "md")],
      [w("NAHI", 12.32, "xl red"), w("HAI", 12.5, "xl red")],
    ], shake: 12.4 },
  { id: "s4", start: 12.9, end: 16.2, top: true, lines: [
      [w("bss", 13.0, "md"), w("EK", 13.18, "lg acc"), w("campaign", 13.42, "md"), w("bnao", 13.65, "md")],
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
      [w("3", 17.0, "huge acc", "s5-num"), w("AD SETS", 17.18, "lg")],
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
      [w("WEBSITE", 22.95, "lg acc"), w("VISIT", 23.1, "lg acc")],
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
      [w("pe", 26.9, "md"), w("engage", 27.05, "md acc"), w("kiya", 27.5, "md"), w("hai", 27.65, "md")],
    ], extra: `
      <div class="float f1" id="s8-f1">♥ 2.4K</div>
      <div class="float f2" id="s8-f2">💬 318</div>
      <div class="float f3" id="s8-f3">↗ 1.1K</div>`,
    tweens: (A) => { A.pop("#s8-f1", 26.95); A.pop("#s8-f2", 27.15); A.pop("#s8-f3", 27.35); } },
  { id: "s9", start: 28.1, end: 29.6, lines: [
      [w("usko", 28.2, "md")],
      [w("LOOKALIKE", 28.4, "xl acc")],
      [w("mei", 28.9, "md"), w("daldo", 29.05, "md")],
    ], extra: `<div class="dots" id="s9-dots">${Array.from({ length: 24 }, (_, i) => `<b class="dot" style="--i:${i}"></b>`).join("")}</div>`,
    tweens: (A) => { A.dots("#s9-dots .dot", 28.3); } },
  { id: "s10", start: 29.6, end: 31.9, lines: [
      [w("aur", 29.85, "md")],
      [w("CREATIVE", 30.0, "xl acc")],
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
      [w("SALES", 32.0, "xl acc")],
      [w("ko", 32.45, "md"), w("scale", 32.55, "md"), w("karne", 32.7, "md"), w("ke", 32.82, "md"), w("liye", 32.92, "md")],
    ], extra: `
      <svg class="chart" viewBox="0 0 1600 600" id="s11-chart"><path id="s11-line" d="M0 560 L260 500 L480 520 L720 380 L960 400 L1200 210 L1420 120 L1600 30" /><path id="s11-arrow" d="M1530 20 L1610 26 L1585 100" /></svg>`,
    tweens: (A) => { A.draw("#s11-line", 32.0, 1.4); T(`tl.fromTo("#s11-arrow",{opacity:0},{opacity:1,duration:.15},33.35);`); } },
  { id: "s12", start: 33.6, end: 36.3, lines: [
      [w("Full", 34.0, "lg"), w("Detailed", 34.2, "lg")],
      [w("PDF", 34.45, "xl acc"), w("chahiye?", 34.65, "lg")],
    ], extra: `
      <div class="follow" id="s12-btn"><span class="f-a">+ FOLLOW</span><span class="f-b" id="s12-done">✓ FOLLOWING</span></div>
      <div class="cursor" id="s12-cur"></div>`,
    tweens: (A) => { A.follow(34.9); } },
  // Voiceover ends after "PDF chahiye" (assets/voiceover.m4a is cut at 36.2s); this CTA is on-screen only.
  { id: "s13", start: 36.3, end: 38.9, lines: [
      [w("Comment", 36.4, "lg"), w("karo", 36.6, "lg")],
      [w("“META”", 36.8, "huge acc")],
    ], shake: 36.85, extra: `
      <div class="cmt" id="s13-cmt">
        <div class="cmt-av"><img src="brand/logo-mark.png" alt="" /></div>
        <div class="cmt-in"><span class="cmt-ph">Add a comment…</span><span class="cmt-txt">${["M", "E", "T", "A"].map((c, i) => `<b id="s13-k${i}">${c}</b>`).join("")}</span></div>
        <div class="cmt-send" id="s13-send">Post</div>
      </div>
      <div class="dm" id="s13-dm">PDF seedha aapke <span>DM</span> mein ✉</div>`,
    tweens: (A) => {
      A.pop("#s13-cmt", 37.0, 0.4);
      T(`tl.fromTo("#s13-cmt .cmt-ph",{opacity:1},{opacity:0,duration:.05,immediateRender:false},37.25);`);
      [37.3, 37.4, 37.5, 37.6].forEach((t, i) => { S(t, "tick", .5); T(`tl.fromTo("#s13-k${i}",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.12,ease:"back.out(3)"},${t});`); });
      S(37.8, "click", .9); S(37.86, "ding", .55);
      T(`tl.to("#s13-send",{scale:.88,duration:.07,yoyo:true,repeat:1},37.8);`);
      T(`tl.to("#s13-send",{backgroundColor:"#8B2FE8",color:"#FFFFFF",duration:.1},37.86);`);
      A.pop("#s13-dm", 38.05, 0.4);
    } },
  { id: "s15", start: 38.9, end: DUR, lines: [], noDrift: true, extra: `
      <div class="outro">
        <div class="logo-wrap" id="s15-logo"><div class="logo-ring" id="s15-ring"></div><img class="logo-big" src="brand/logo.png" alt="The GrowthX Studio" /></div>
        <div class="outro-r">
          <div class="pill" id="s15-pill">COMMENT “META” 💬</div>
          <div class="mail" id="s15-mail"><span class="mail-ico">✉</span> thegrowthxstudio@gmail.com</div>
          <div class="tagline" id="s15-tag">BUILD <i>•</i> GROW <i>•</i> SCALE</div>
        </div>
      </div>`,
    tweens: (A) => {
      T(`tl.fromTo("#s15-logo",{opacity:0,scale:.5,rotation:-25},{opacity:1,scale:1,rotation:0,duration:.7,ease:"back.out(1.7)"},38.95);`);
      T(`tl.fromTo("#s15-ring",{opacity:.9,scale:1},{opacity:0,scale:1.6,duration:.9,ease:"power2.out"},39.1);`);
      T(`tl.to("#s15-logo",{scale:1.04,duration:2,ease:"sine.inOut"},39.65);`);
      A.pop("#s15-pill", 39.4, 0.45); A.pop("#s15-mail", 39.65, 0.45);
      T(`tl.fromTo("#s15-tag",{opacity:0,x:-40},{opacity:1,x:0,duration:.6,ease:"power3.out"},39.9);`);
      S(38.95, "impact", .8); S(39.0, "shimmer", .55);
    } },
];

const wipes = [6.35, 12.9, 18.4, 22.8, 25.45, 29.6, 33.6, 36.3, 38.9];

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
  pop: (sel, t, d = 0.35) => (S(t, "pop", .45), T(`tl.fromTo("${sel}",{opacity:0,y:50,scale:.85},{opacity:1,y:0,scale:1,duration:${d},ease:"back.out(2)"},${t});`)),
  flash: (sel, t) => (S(t, "ding", .5), T(`tl.fromTo("${sel}",{boxShadow:"0 0 0 0 rgba(139,47,232,.9)"},{boxShadow:"0 0 0 18px rgba(139,47,232,0)",duration:.6,ease:"power2.out",immediateRender:false},${t});`)),
  drift: (sel, t, d) => T(`tl.to("${sel}",{scale:1.04,duration:${d},ease:"none"},${t + 0.5});`),
  activate: (sel, t, next) => {
    T(`tl.to("${sel}",{borderColor:"#B57BFF",backgroundColor:"rgba(139,47,232,.12)",duration:.2},${t});`);
    if (next) T(`tl.to("${sel}",{borderColor:"rgba(255,255,255,.14)",backgroundColor:"rgba(255,255,255,.04)",duration:.2},${next});`);
  },
  dots: (sel, t) => (S(t, "riser", .35), T(`tl.fromTo("${sel}",{opacity:0,scale:0},{opacity:1,scale:1,duration:.3,ease:"back.out(3)",stagger:{each:.035,from:"start"}},${t});`)),
  fan: (sels, t) => {
    const rot = [-14, 0, 14], x = [-520, 0, 520];
    sels.forEach((s, i) => T(`tl.fromTo("${s}",{opacity:0,x:0,y:200,rotation:0},{opacity:.9,x:${x[i]},y:${i === 1 ? -20 : 40},rotation:${rot[i]},duration:.55,ease:"back.out(1.6)"},${t + i * 0.08});`));
  },
  draw: (sel, t, d) => T(`(function(){const p=document.querySelector("${sel}");const L=p.getTotalLength();tl.fromTo(p,{strokeDasharray:L,strokeDashoffset:L},{strokeDashoffset:0,duration:${d},ease:"power2.inOut"},${t});})();`),
  follow: (t) => {
    T(`tl.fromTo("#s12-btn",{opacity:0,y:60,scale:.8},{opacity:1,y:0,scale:1,duration:.4,ease:"back.out(2)"},${t});`);
    T(`tl.fromTo("#s12-cur",{opacity:0,x:260,y:200},{opacity:1,x:0,y:0,duration:.45,ease:"power3.out"},${t + 0.2});`);
    S(t + 0.62, "click", .9); S(t + 0.7, "ding", .55);
    T(`tl.to("#s12-btn",{scale:.92,duration:.08,yoyo:true,repeat:1},${t + 0.65});`);
    T(`tl.to("#s12-btn",{backgroundColor:"#8B2FE8",borderColor:"#B57BFF",color:"#FFFFFF",duration:.1},${t + 0.7});`);
    T(`tl.fromTo("#s12-done",{yPercent:100},{yPercent:0,duration:.2,ease:"power2.out"},${t + 0.7});`);
    T(`tl.to("#s12-btn .f-a",{yPercent:-100,opacity:0,duration:.2},${t + 0.7});`);
  },
};

// Hook: slow push-in on the original clip + tag.
T(`tl.fromTo("#hook-wrap",{scale:1},{scale:1.12,duration:6.35,ease:"none"},0);`);
T(`tl.fromTo("#hook-tag",{opacity:0,y:-30},{opacity:1,y:0,duration:.4,ease:"back.out(2)"},0.15);`);
T(`tl.fromTo("#hook-tag2",{opacity:0,x:-40},{opacity:1,x:0,duration:.4,ease:"power3.out"},0.35);`);

words.forEach((x) => {
  if (/\b(xl|huge)\b/.test(x.cls)) S(x.t, "impact_lite", .55);
  else if (/\b(lg|hl)\b/.test(x.cls)) S(x.t, "pop", .5);
  else S(x.t, "tick", .28);
  T(`tl.fromTo("#${x.id} .wi",{opacity:0,yPercent:70,scale:.8},{opacity:1,yPercent:0,scale:1,duration:.26,ease:"back.out(2.2)"},${x.t});`);
  if (/\b(xl|huge)\b/.test(x.cls)) T(`tl.fromTo("#${x.id}",{scale:1.25},{scale:1,duration:.35,ease:"power3.out"},${x.t});`);
  if (/\bhl\b/.test(x.cls)) T(`tl.fromTo("#${x.id}",{"--hl":0},{"--hl":1,duration:.25,ease:"power2.out"},${x.t + 0.08});`);
});

scenes.forEach((s) => {
  if (!s.noDrift) T(`tl.fromTo("#${s.id}-stage",{scale:1},{scale:1.05,duration:${(s.end - s.start).toFixed(2)},ease:"none"},${s.start});`);
  if (s.shake) S(s.shake, "impact", .75);
  if (s.shake) T(`tl.fromTo("#${s.id}-stage",{x:-14},{x:0,duration:.35,ease:"elastic.out(1.4,.3)",immediateRender:false},${s.shake});`);
  if (s.tweens) s.tweens(A);
});

// Counter 1→3 on the "3".

// Transitions: purple wipe + white flash.
wipes.forEach((t, i) => {
  S(t - 0.33, "whoosh", .7);
  T(`tl.fromTo("#wipe .wp",{xPercent:-130},{xPercent:130,duration:.42,ease:"power3.inOut"${i ? ",immediateRender:false" : ""}},${(t - 0.21).toFixed(2)});`);
});
T(`tl.fromTo("#flash",{opacity:.85},{opacity:0,duration:.25,ease:"power2.out",immediateRender:false},6.35);`);

S(5.45, "riser", .6); S(6.35, "impact", .9); S(32.0, "cash", .5);
S(0.15, "pop", .4);
T(`tl.fromTo("#bg-ring1",{rotation:0},{rotation:120,duration:${DUR},ease:"none"},0);`);
T(`tl.fromTo("#bg-ring2",{rotation:0},{rotation:-90,duration:${DUR},ease:"none"},0);`);
T(`tl.fromTo("#brand .bi",{opacity:0,y:-20},{opacity:1,y:0,duration:.4,ease:"power3.out"},0.2);`);
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
      :root { --bg:#040206; --ink:#F7F4FF; --acc:#B57BFF; --pur:#8B2FE8; --pur2:#A65CFF; --dim:#9C94B0; --red:#FF3D3D; --wa:#25D366; }
      * { margin:0; padding:0; box-sizing:border-box; }
      html, body { width:1920px; height:1080px; overflow:hidden; background:var(--bg); }
      #root { position:relative; width:100%; height:100%; overflow:hidden; font-family:"Display", sans-serif; color:var(--ink); }
      .bg { position:absolute; inset:0; background:var(--bg); }
      .grid { position:absolute; inset:0; background-image:linear-gradient(rgba(181,123,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(181,123,255,.045) 1px,transparent 1px); background-size:80px 80px; }
      #glow { position:absolute; left:360px; top:90px; width:1200px; height:900px; border-radius:50%; background:radial-gradient(closest-side,rgba(139,47,232,.30),rgba(139,47,232,0)); }
      .bg-ring { position:absolute; left:50%; top:50%; border-radius:50%; border:2px solid rgba(166,92,255,.35); box-shadow:0 0 40px rgba(139,47,232,.25), inset 0 0 40px rgba(139,47,232,.15); }
      #bg-ring1 { width:1300px; height:1300px; margin:-650px 0 0 -650px; border-top-color:rgba(200,160,255,.85); border-right-color:transparent; }
      #bg-ring2 { width:980px; height:980px; margin:-490px 0 0 -490px; border-color:rgba(166,92,255,.18); border-left-color:rgba(200,160,255,.6); border-bottom-color:transparent; }
      .vignette { position:absolute; inset:0; background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.6) 100%); }

      #hook-wrap { position:absolute; inset:0; overflow:hidden; }
      #hook { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
      .hook-ui { position:absolute; inset:0; }
      #hook-tag { position:absolute; left:80px; top:70px; background:linear-gradient(90deg,var(--pur),var(--pur2)); color:#fff; box-shadow:0 0 40px rgba(139,47,232,.6); font-weight:900; font-size:40px; padding:14px 28px; border-radius:14px; letter-spacing:.02em; }
      #hook-tag2 { position:absolute; left:80px; top:160px; background:rgba(7,8,12,.94); color:var(--ink); font-weight:700; font-size:34px; padding:12px 24px; border-radius:12px; border:2px solid rgba(139,47,232,.6); }

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
      .acc { color:var(--acc); text-shadow:0 0 50px rgba(139,47,232,.75), 0 0 12px rgba(181,123,255,.35); }
      .red { color:var(--red); }
      .dim { color:var(--dim); letter-spacing:.2em; }
      .wa { color:var(--wa); font-size:150px; }
      .ig .wi { background:linear-gradient(90deg,#FEDA75,#FA7E1E,#D62976,#962FBF,#4F5BD5); -webkit-background-clip:text; background-clip:text; color:transparent; padding:0 6px; }
      .hl { --hl:0; color:#fff; }
      .hl::before { content:""; position:absolute; left:-12px; right:-12px; top:8%; bottom:4%; background:linear-gradient(90deg,var(--pur),var(--pur2)); box-shadow:0 0 40px rgba(139,47,232,.55); border-radius:14px; z-index:-1; transform-origin:left center; transform:scaleX(var(--hl)); }
      .hl .wi { z-index:1; }

      .ui-card { width:900px; padding:44px 50px; border-radius:28px; background:rgba(255,255,255,.05); border:2px solid rgba(255,255,255,.14); display:flex; flex-direction:column; gap:30px; }
      .ui-label { font-size:28px; font-weight:700; color:var(--dim); letter-spacing:.2em; }
      .chips { display:flex; gap:20px; }
      .chip { font-size:40px; font-weight:700; padding:16px 30px; border-radius:999px; border:2px solid rgba(255,255,255,.2); color:var(--dim); }
      .chip.on { background:var(--pur); color:#fff; border-color:var(--pur2); }
      .tick { font-weight:900; }
      .ui-row { display:flex; justify-content:space-between; align-items:center; font-size:48px; padding-top:22px; border-top:2px solid rgba(255,255,255,.1); }
      .ui-k { color:var(--dim); font-weight:600; }
      .ui-v { color:var(--acc); font-weight:900; font-size:64px; display:inline-block; }
      .ui-foot { font-size:56px; font-weight:700; text-align:center; }
      .w-inline { display:inline-block; }

      .sets { display:flex; gap:44px; margin-top:40px; }
      .set { width:500px; height:520px; border-radius:32px; border:3px solid rgba(255,255,255,.14); background:rgba(255,255,255,.04); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:36px; position:relative; }
      .set-n { position:absolute; top:28px; left:34px; font-size:40px; font-weight:900; color:var(--acc); }
      .set-name { font-size:58px; font-weight:900; text-align:center; line-height:1.05; padding:0 30px; }
      .ico { width:150px; height:150px; position:relative; }
      .ico-globe { border:10px solid var(--acc); border-radius:50%; }
      .ico-globe::before { content:""; position:absolute; inset:0 38px; border:8px solid var(--acc); border-radius:50%; }
      .ico-globe::after { content:""; position:absolute; left:0; right:0; top:61px; height:8px; background:var(--acc); }
      .ico-target { border:10px solid var(--acc); border-radius:50%; }
      .ico-target::before { content:""; position:absolute; inset:24px; border:10px solid var(--acc); border-radius:50%; }
      .ico-target::after { content:""; position:absolute; inset:54px; background:var(--acc); border-radius:50%; }
      .ico-people::before, .ico-people::after { content:""; position:absolute; width:62px; height:62px; border-radius:50%; background:var(--acc); top:14px; box-shadow:0 78px 0 18px var(--acc); }
      .ico-people::before { left:10px; opacity:.45; }
      .ico-people::after { right:22px; }

      .browser { position:absolute; left:110px; top:234px; width:900px; border-radius:22px; overflow:hidden; background:#fff; box-shadow:0 40px 120px rgba(0,0,0,.6), 0 0 0 3px rgba(139,47,232,.5); order:1; }
      .bar { height:56px; background:#1A1D24; display:flex; align-items:center; gap:12px; padding:0 22px; }
      .bar i { width:16px; height:16px; border-radius:50%; background:#3A3F4A; }
      .bar i:first-child { background:#FF5F57; } .bar i:nth-child(2) { background:#FEBC2E; } .bar i:nth-child(3) { background:#28C840; }
      .url { margin-left:20px; flex:1; height:34px; border-radius:10px; background:#0B0D12; color:var(--dim); font-size:20px; font-weight:600; display:flex; align-items:center; padding-left:18px; }
      .viewport { position:relative; width:900px; height:556px; background:#fff; }
      #website { position:absolute; left:110px; top:290px; width:900px; height:556px; object-fit:cover; }

      .float { position:absolute; font-size:44px; font-weight:900; padding:16px 28px; border-radius:20px; background:rgba(255,255,255,.08); border:2px solid rgba(255,255,255,.18); }
      .f1 { left:170px; top:230px; color:#FF4D79; }
      .f2 { right:180px; top:280px; }
      .f3 { right:300px; bottom:170px; color:var(--acc); }
      .ad1 .ad-img { background:linear-gradient(135deg,#B57BFF,#4B0F94) !important; }

      .dots { position:absolute; left:50%; bottom:110px; width:720px; margin-left:-360px; display:flex; flex-wrap:wrap; gap:18px; justify-content:center; }
      .dot { display:block; width:42px; height:42px; border-radius:50%; background:var(--acc); }
      .dot:nth-child(-n+6) { background:var(--ink); }

      .cards { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; z-index:-1; }
      .ad { position:absolute; width:400px; height:560px; border-radius:28px; background:#151821; border:2px solid rgba(255,255,255,.12); padding:24px; display:flex; flex-direction:column; gap:18px; }
      .ad-img { height:380px; border-radius:18px; background:linear-gradient(135deg,#2A3140,#11141B); }
      .ad1 .ad-img { background:linear-gradient(135deg,#B57BFF,#4E7A00); }
      .ad3 .ad-img { background:linear-gradient(135deg,#FA7E1E,#962FBF); }
      .ad-l { height:22px; border-radius:11px; background:rgba(255,255,255,.18); }
      .ad-l.s { width:60%; }
      #s10 .text { position:relative; z-index:2; background:rgba(7,8,12,.78); padding:30px 60px; border-radius:30px; }

      .chart { position:absolute; left:160px; bottom:120px; width:1600px; height:600px; z-index:-1; }
      .chart path { fill:none; stroke:var(--pur2); stroke-width:14; stroke-linecap:round; stroke-linejoin:round; opacity:.8; filter:drop-shadow(0 0 18px rgba(139,47,232,.9)); }

      .follow { position:relative; overflow:hidden; height:110px; width:520px; border-radius:24px; background:#2F6BFF; border:4px solid #2F6BFF; color:#fff; font-size:50px; font-weight:900; }
      .f-a, .f-b { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }
            .cursor { position:absolute; left:1080px; top:780px; width:0; height:0; border-left:28px solid transparent; border-right:28px solid transparent; border-bottom:70px solid #fff; transform-origin:center; rotate:-30deg; filter:drop-shadow(0 6px 10px rgba(0,0,0,.6)); }

      .cmt { display:flex; align-items:center; gap:22px; width:1100px; padding:22px 26px; border-radius:26px; background:rgba(255,255,255,.06); border:2px solid rgba(166,92,255,.5); box-shadow:0 0 60px rgba(139,47,232,.35); }
      .cmt-av { width:84px; height:84px; border-radius:50%; overflow:hidden; border:3px solid var(--pur2); flex:none; }
      .cmt-av img { width:100%; height:100%; object-fit:cover; }
      .cmt-in { position:relative; flex:1; height:84px; border-radius:42px; background:rgba(4,2,6,.8); display:flex; align-items:center; padding:0 34px; font-size:44px; }
      .cmt-ph { position:absolute; left:34px; color:var(--dim); font-weight:600; }
      .cmt-txt b { display:inline-block; font-weight:900; color:#fff; letter-spacing:.04em; }
      .cmt-send { flex:none; font-size:40px; font-weight:900; padding:18px 34px; border-radius:20px; color:var(--acc); border:2px solid var(--pur2); }
      #s13 .huge { font-size:290px; margin-top:34px; }
      .dm { font-size:58px; font-weight:700; }
      .dm span { color:var(--acc); font-weight:900; }
      .cta { display:flex; flex-direction:column; align-items:center; gap:30px; margin-top:30px; }
      .pill { background:linear-gradient(90deg,var(--pur),var(--pur2)); color:#fff; box-shadow:0 0 50px rgba(139,47,232,.6); font-size:64px; font-weight:900; padding:22px 56px; border-radius:999px; }
      .mail { font-size:46px; font-weight:700; padding:18px 40px; border-radius:20px; background:rgba(255,255,255,.06); border:2px solid rgba(255,255,255,.2); }
      .mail-ico { color:var(--acc); }

      #wipe { position:absolute; inset:0; overflow:hidden; pointer-events:none; }
      #wipe .wp { position:absolute; top:-20%; bottom:-20%; left:0; width:100%; background:linear-gradient(90deg,#5B12B0,var(--pur) 40%,var(--pur2) 85%,#fff 100%); transform:skewX(-18deg); }
      #flash { position:absolute; inset:0; background:#fff; opacity:0; }
      #progress { position:absolute; left:0; right:0; bottom:0; height:10px; background:rgba(255,255,255,.08); }
      #progress i { display:block; height:100%; background:linear-gradient(90deg,var(--pur),var(--pur2)); box-shadow:0 0 16px var(--pur); transform-origin:left center; }
      #brand { position:absolute; right:50px; top:36px; }
      #brand .bi { display:flex; align-items:center; gap:16px; padding:8px 22px 8px 8px; border-radius:999px; background:rgba(4,2,6,.82); border:2px solid rgba(166,92,255,.45); }
      #brand img { width:72px; height:72px; border-radius:50%; object-fit:cover; }
      #brand span { font-size:26px; font-weight:900; letter-spacing:.14em; color:#fff; }
      #brand b { color:var(--acc); }
      .outro { display:flex; align-items:center; gap:90px; }
      .logo-wrap { position:relative; width:560px; height:560px; }
      .logo-big { width:100%; height:100%; border-radius:50%; box-shadow:0 0 120px rgba(139,47,232,.55); }
      .logo-ring { position:absolute; inset:0; border-radius:50%; border:6px solid var(--acc); }
      .outro-r { display:flex; flex-direction:column; align-items:flex-start; gap:36px; }
      .tagline { font-size:34px; font-weight:700; letter-spacing:.35em; color:var(--ink); }
      .tagline i { font-style:normal; color:var(--acc); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${DUR}" data-width="1920" data-height="1080">
      <div class="bg"></div>
      <div class="grid"></div>
      <div id="glow"></div>
      <div class="bg-ring" id="bg-ring1"></div>
      <div class="bg-ring" id="bg-ring2"></div>
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
      <div id="brand" class="clip" data-start="0" data-duration="38.9" data-track-index="8"><div class="bi"><img src="brand/logo-mark.png" alt="GX" /><span>THE GROWTH<b>X</b> STUDIO</span></div></div>
      <div id="progress" class="clip" data-start="0" data-duration="${DUR}" data-track-index="9"><i></i></div>

      <audio id="vo" src="assets/voiceover.m4a" data-start="0" data-duration="36.2" data-track-index="10" data-volume="1"></audio>
      <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="${DUR}" data-track-index="11" data-volume="0.6"></audio>
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
sfx.sort((a, b) => a.t - b.t);
fs.writeFileSync(require("path").join(require("path").dirname(out), "sfx.json"), JSON.stringify({ duration: DUR, cues: sfx }, null, 1));
console.log("wrote", out, words.length, "words");
