// Run: node build.cjs  (regenerates index.html; edit word timings in the scenes list)
// Generates growthx-meta-ads-16x9/index.html (static clips, one paused GSAP timeline).
const fs = require("fs");
const out = process.argv[2] || require("path").join(__dirname, "index.html");
const DUR = 41.2;
const sfx = [];
const S = (t, type, vol = 1) => sfx.push({ t: +t.toFixed(3), type, vol });

// w(text, t, cls) — one spoken word, revealed at global time t.
const w = (text, t, cls = "") => ({ text, t, cls });

// Voiceover (Bunty, ElevenLabs) starts after the Shark Tank hook.
const VO = 6.5;
// Phrase spans in the voiceover file (seconds), from its pauses + a local ASR check.
// seg(start, end, tokens): spreads the words across the phrase by character count.
const seg = (s, e, toks) => {
  const total = toks.reduce((n, [t]) => n + t.length + 1, 0);
  let cum = 0;
  return toks.map(([text, cls]) => {
    const t = VO + s + (cum / total) * (e - s) - 0.03;
    cum += text.length + 1;
    return w(text, +Math.max(t, VO + s - 0.03).toFixed(2), cls);
  });
};
const g = (t) => +(VO + t).toFixed(2); // VO-file time → global time

const A_ = seg(0, 2.67, [["agar", "sm"], ["apne", "sm"], ["D2C", "xl acc"], ["BRAND", "xl acc"], ["abhi", "md"], ["start", "md"], ["kiya", "md"], ["hai", "md"]]);
const B_ = seg(2.87, 5.83, [["to", "sm"], ["yeh", "sm"], ["META", "lg hl"], ["AD", "lg hl"], ["STRATEGY", "lg hl"], ["apko", "md"], ["direct", "md"], ["CUSTOMER", "lg acc"], ["lake", "md"], ["degi", "md"]]);
const C_ = seg(6.2, 6.9, [["karna", "md"], ["kuch", "md"], ["NAHI", "xl red"], ["HAI", "xl red"]]);
const D_ = seg(7.4, 8.45, [["bss", "md"], ["EK", "lg acc"], ["campaign", "md"], ["bnao", "md"]]);
const E_ = seg(8.65, 10.07, [["Sales"], ["Conversion"], ["objective"], ["ke"]]).map((x) => x.t);
const F_ = seg(10.39, 10.76, [["aur", "md"], ["usmei", "md"]]);
const G_ = seg(10.96, 12.05, [["3", "huge acc"], ["AD SETS", "lg"], ["add", "md"], ["karo", "md"]]);
const SETS = [g(12.51), g(13.56), g(14.61)];
const K_ = seg(16.03, 18.69, [["jo", "md"], ["apki", "md"], ["WEBSITE", "lg acc"], ["VISIT", "lg acc"], ["ya", "md"], ["VIDEO", "lg"], ["VIEWS", "lg"], ["pe", "md"], ["based", "md"], ["ho", "md"]]);
const L_ = seg(19.13, 21.36, [["aur", "md"], ["jisne", "md"], ["apke", "md"], ["INSTAGRAM", "xl ig"], ["pe", "md"], ["engage", "md acc"], ["kiya", "md"], ["hai", "md"]]);
const M_ = seg(21.56, 22.63, [["usko", "md"], ["LOOKALIKE", "xl acc"], ["mei", "md"], ["daldo", "md"]]);
const N_ = seg(23.05, 23.75, [["aur", "md"], ["CREATIVE", "xl acc"]]);
const O_ = seg(23.97, 26.63, [["jo", "md"], ["sabse", "md"], ["IMPORTANT", "lg hl"], ["hai", "md"], ["SALES", "xl acc"], ["ko", "md"], ["scale", "md"], ["karne", "md"], ["ke", "md"], ["liye", "md"]]);
const P_ = seg(27.16, 28.41, [["Full", "lg"], ["Detailed", "lg"], ["PDF", "xl acc"], ["chahiye?", "lg"]]);
const Q_ = seg(28.82, 29.88, [["Comment", "lg"], ["karo", "lg"], ["“META”", "huge acc"]]);
const R_ = seg(30.14, 31.83, [["aur"], ["PDF"], ["seedha"], ["aapke"], ["DM"], ["mein"]]).map((x) => x.t);

// Scene cuts sit in the pauses between phrases.
const CUT = { s1: 6.35, s2: g(2.77), s3: g(6.05), s4: g(7.15), s5: g(10.25), s6: g(12.3), s7: g(15.9), s8: g(18.95), s9: g(21.46), s10: g(22.85), s11: O_[4].t - 0.12, s12: g(26.9), s13: g(28.62), s15: g(32.1) };

// Scenes: start, end, lines of words, plus optional extra HTML + extra tweens.
const scenes = [
  { id: "s1", start: CUT.s1, end: CUT.s2, lines: [A_.slice(0, 2), A_.slice(2, 4), A_.slice(4)] },
  { id: "s2", start: CUT.s2, end: CUT.s3, lines: [B_.slice(0, 2), B_.slice(2, 5), B_.slice(5, 7), B_.slice(7)] },
  { id: "s3", start: CUT.s3, end: CUT.s4, lines: [C_.slice(0, 2), C_.slice(2)], shake: C_[2].t + 0.05 },
  { id: "s4", start: CUT.s4, end: CUT.s5, top: true, lines: [D_], extra: `
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
      A.pop("#s4-card", D_[3].t + 0.15, 0.45);
      A.pop("#s4-c1", E_[0] - 0.2); A.pop("#s4-c2", E_[0] - 0.1); A.pop("#s4-c3", E_[0]);
      A.flash("#s4-c3", E_[0] + 0.05);
      A.pop("#s4-conv", E_[1]);
      A.pop("#s4-ob", E_[2]); A.pop("#s4-ke", E_[3]);
    } },
  { id: "s5", start: CUT.s5, end: CUT.s6, lines: [F_, G_.slice(0, 2), G_.slice(2)], shake: G_[0].t + 0.05 },
  { id: "s6", start: CUT.s6, end: CUT.s7, top: true, lines: [[w("3 AD SETS", CUT.s6 + 0.05, "sm dim")]], extra: `
      <div class="sets">
        ${["Broad Audience|globe|01", "Interest Targeting|target|02", "Lookalike Audience|people|03"].map((s, i) => {
          const [name, icon, n] = s.split("|");
          return `<div class="set" id="s6-set${i}"><div class="set-n">${n}</div><div class="ico ico-${icon}"></div><div class="set-name">${name}</div></div>`;
        }).join("")}
      </div>`,
    tweens: (A) => {
      SETS.forEach((t, i) => { A.pop(`#s6-set${i}`, t, 0.45); A.activate(`#s6-set${i}`, t, SETS[i + 1]); });
    } },
  { id: "s7", start: CUT.s7, end: CUT.s8, split: true, lines: [K_.slice(0, 2), K_.slice(2, 4), K_.slice(4, 7), K_.slice(7)], extra: `
      <div class="browser" id="s7-browser">
        <div class="bar"><i></i><i></i><i></i><div class="url">yourbrand.com</div></div>
        <div class="viewport"></div>
      </div>`,
    noDrift: true,
    tweens: (A) => { T(`tl.fromTo("#s7-browser",{opacity:0},{opacity:1,duration:.15},${CUT.s7});`); } },
  { id: "s8", start: CUT.s8, end: CUT.s9, lines: [L_.slice(0, 3), L_.slice(3, 4), L_.slice(4)], extra: `
      <div class="float f1" id="s8-f1">♥ 2.4K</div>
      <div class="float f2" id="s8-f2">💬 318</div>
      <div class="float f3" id="s8-f3">↗ 1.1K</div>`,
    tweens: (A) => { A.pop("#s8-f1", L_[5].t - 0.1); A.pop("#s8-f2", L_[5].t + 0.1); A.pop("#s8-f3", L_[5].t + 0.3); } },
  { id: "s9", start: CUT.s9, end: CUT.s10, lines: [M_.slice(0, 1), M_.slice(1, 2), M_.slice(2)],
    extra: `<div class="dots" id="s9-dots">${Array.from({ length: 24 }, (_, i) => `<b class="dot" style="--i:${i}"></b>`).join("")}</div>`,
    tweens: (A) => { A.dots("#s9-dots .dot", M_[1].t - 0.1); } },
  { id: "s10", start: CUT.s10, end: CUT.s11, lines: [N_.slice(0, 1), N_.slice(1), O_.slice(0, 2), O_.slice(2, 4)], extra: `
      <div class="cards">
        <div class="ad ad1" id="s10-a1"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
        <div class="ad ad2" id="s10-a2"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
        <div class="ad ad3" id="s10-a3"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
      </div>`,
    tweens: (A) => { A.fan(["#s10-a1", "#s10-a2", "#s10-a3"], N_[1].t); } },
  { id: "s11", start: CUT.s11, end: CUT.s12, lines: [O_.slice(4, 5), O_.slice(5)], extra: `
      <svg class="chart" viewBox="0 0 1600 600" id="s11-chart"><path id="s11-line" d="M0 560 L260 500 L480 520 L720 380 L960 400 L1200 210 L1420 120 L1600 30" /><path id="s11-arrow" d="M1530 20 L1610 26 L1585 100" /></svg>`,
    tweens: (A) => { A.draw("#s11-line", O_[4].t, 1.2); T(`tl.fromTo("#s11-arrow",{opacity:0},{opacity:1,duration:.15},${(O_[4].t + 1.15).toFixed(2)});`); S(O_[4].t, "cash", .5); } },
  { id: "s12", start: CUT.s12, end: CUT.s13, lines: [P_.slice(0, 2), P_.slice(2)] },
  { id: "s13", start: CUT.s13, end: CUT.s15, lines: [Q_.slice(0, 2), Q_.slice(2)], shake: Q_[2].t + 0.05, extra: `
      <div class="cmt" id="s13-cmt">
        <div class="cmt-av"><img src="brand/logo-mark.png" alt="" /></div>
        <div class="cmt-in"><span class="cmt-ph">Add a comment…</span><span class="cmt-txt">${["M", "E", "T", "A"].map((c, i) => `<b id="s13-k${i}">${c}</b>`).join("")}</span></div>
        <div class="cmt-send" id="s13-send">Post</div>
      </div>
      <div class="dm"><span class="w-inline" id="s13-d0">aur</span> <span class="w-inline" id="s13-d1">PDF</span> <span class="w-inline" id="s13-d2">seedha</span> <span class="w-inline" id="s13-d3">aapke</span> <span class="w-inline dmk" id="s13-d4">DM</span> <span class="w-inline" id="s13-d5">mein ✉</span></div>`,
    tweens: (A) => {
      const c0 = Q_[2].t + 0.3;
      A.pop("#s13-cmt", c0 - 0.05, 0.35);
      T(`tl.fromTo("#s13-cmt .cmt-ph",{opacity:1},{opacity:0,duration:.05,immediateRender:false},${(c0 + 0.2).toFixed(2)});`);
      [0, 1, 2, 3].forEach((i) => { const t = +(c0 + 0.25 + i * 0.08).toFixed(2); S(t, "tick", .5); T(`tl.fromTo("#s13-k${i}",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.12,ease:"back.out(3)"},${t});`); });
      const post = R_[1];
      S(post, "click", .9); S(post + 0.06, "ding", .55);
      T(`tl.to("#s13-send",{scale:.88,duration:.07,yoyo:true,repeat:1},${post});`);
      T(`tl.to("#s13-send",{backgroundColor:"#8B2FE8",color:"#FFFFFF",duration:.1},${(post + 0.06).toFixed(2)});`);
      R_.forEach((t, i) => T(`tl.fromTo("#s13-d${i}",{opacity:0,y:30},{opacity:1,y:0,duration:.22,ease:"back.out(2)"},${t});`));
    } },
  { id: "s15", start: CUT.s15, end: DUR, lines: [], noDrift: true, extra: `
      <div class="outro">
        <div class="logo-wrap" id="s15-logo"><div class="logo-ring" id="s15-ring"></div><img class="logo-big" src="brand/logo.png" alt="The GrowthX Studio" /></div>
        <div class="outro-r">
          <div class="pill" id="s15-pill">COMMENT “META” 💬</div>
          <div class="mail" id="s15-mail"><span class="mail-ico">✉</span> thegrowthxstudio@gmail.com</div>
          <div class="tagline" id="s15-tag">BUILD <i>•</i> GROW <i>•</i> SCALE</div>
        </div>
      </div>`,
    tweens: (A) => {
      const o = CUT.s15;
      T(`tl.fromTo("#s15-logo",{opacity:0,scale:.5,rotation:-25},{opacity:1,scale:1,rotation:0,duration:.7,ease:"back.out(1.7)"},${o + 0.05});`);
      T(`tl.fromTo("#s15-ring",{opacity:.9,scale:1},{opacity:0,scale:1.6,duration:.9,ease:"power2.out"},${o + 0.2});`);
      T(`tl.to("#s15-logo",{scale:1.04,duration:2,ease:"sine.inOut"},${o + 0.75});`);
      A.pop("#s15-pill", +(o + 0.5).toFixed(2), 0.45); A.pop("#s15-mail", +(o + 0.75).toFixed(2), 0.45);
      T(`tl.fromTo("#s15-tag",{opacity:0,x:-40},{opacity:1,x:0,duration:.6,ease:"power3.out"},${(o + 1.0).toFixed(2)});`);
      S(o + 0.05, "impact", .8); S(o + 0.1, "shimmer", .55);
    } },
];

const wipes = [CUT.s1, CUT.s4, CUT.s6, CUT.s7, CUT.s8, CUT.s10, CUT.s12, CUT.s13, CUT.s15];

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

S(5.45, "riser", .6); S(6.35, "impact", .9); 
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
      .dm .dmk { color:var(--acc); font-weight:900; }
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

      <video id="website" src="assets/website.mp4" muted playsinline data-start="${(CUT.s7 + 0.05).toFixed(2)}" data-duration="${(CUT.s8 - CUT.s7 - 0.05).toFixed(2)}" data-playback-rate="${(2.4 / (CUT.s8 - CUT.s7 - 0.05)).toFixed(3)}" data-track-index="5"></video>

      <div id="wipe" class="clip" data-start="0" data-duration="${DUR}" data-track-index="6"><div class="wp"></div></div>
      <div id="flash" class="clip" data-start="0" data-duration="${DUR}" data-track-index="7"></div>
      <div id="brand" class="clip" data-start="0" data-duration="${CUT.s15}" data-track-index="8"><div class="bi"><img src="brand/logo-mark.png" alt="GX" /><span>THE GROWTH<b>X</b> STUDIO</span></div></div>
      <div id="progress" class="clip" data-start="0" data-duration="${DUR}" data-track-index="9"><i></i></div>

      <audio id="hook-audio" src="assets/hook-audio.m4a" data-start="0" data-duration="6.35" data-track-index="10" data-volume="1"></audio>
      <audio id="vo" src="assets/voiceover.m4a" data-start="${VO}" data-duration="32.03" data-track-index="12" data-volume="1"></audio>
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
