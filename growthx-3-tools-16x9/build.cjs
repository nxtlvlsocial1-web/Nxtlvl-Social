// Run: node build.cjs  (regenerates index.html; edit word timings in the scenes list)
// Generates growthx-3-tools-16x9/index.html (static clips, one paused GSAP timeline).
const fs = require("fs");
const out = process.argv[2] || require("path").join(__dirname, "index.html");
const DUR = 40.8;
const sfx = [];
const S = (t, type, vol = 1) => sfx.push({ t: +t.toFixed(3), type, vol });

// w(text, t, cls) — one spoken word, revealed at global time t.
const w = (text, t, cls = "") => ({ text, t, cls });
// Voiceover: ElevenLabs "Bunty – Fun Podcast Host" (assets/voiceover.m4a), starts at 0.
const VO = 0;
// seg(start, end, tokens): phrase span in the voiceover (from its pauses, checked with local ASR);
// words are spread across the span by character count.
const seg = (s, e, toks) => {
  const total = toks.reduce((n, [t]) => n + t.length + 1, 0);
  let cum = 0;
  return toks.map(([text, cls]) => {
    const t = VO + s + (cum / total) * (e - s) - 0.03;
    cum += text.length + 1;
    return w(text, +Math.max(t, 0).toFixed(2), cls);
  });
};

const toolCard = (id, n, icon, name, tag) => `
      <div class="tool" id="${id}">
        <div class="tool-n">#${n}</div>
        <div class="tool-ic">${icon}</div>
        <div class="tool-b"><div class="tool-t">${name}</div><div class="tool-s">${tag}</div></div>
      </div>`;

const A_ = seg(0.02, 1.84, [["kya", "md"], ["aap", "md"], ["E-COMMERCE", "xl acc"], ["brand", "lg"], ["banaoge?", "lg"]]);
const B_ = seg(2.16, 4.11, [["Agar", "md"], ["yeh", "md"], ["3", "huge acc"], ["EXTENSIONS", "lg"], ["hi", "md"], ["use", "md"], ["nahi", "md"], ["ki?", "md"]]);
const D_ = seg(4.63, 6.57, [["kyunki", "md acc"], ["yeh", "md"], ["tools", "md"], ["tumhe", "md"], ["BEGINNER", "lg"], ["se", "md"]]);
const E_ = seg(6.72, 7.43, [["PRO", "xl acc"], ["bana", "md"], ["denge", "md"]]);
const F_ = seg(7.75, 11.21, [["aur", "md"], ["tumhare", "md"], ["COMPETITORS", "xl acc"], ["ka", "md"], ["saara", "md"], ["DATA", "lg hl"], ["tumhare", "md"], ["saamne", "md"], ["rakh", "md"], ["denge", "md"]]);
const G_ = seg(11.73, 12.25, [["Pehla", "lg"], ["hai", "lg acc"]]);
const TOOL1 = 12.39;
const J_ = seg(14.69, 19.99, [["Yeh", "md"], ["competitors", "md acc"], ["ke", "md"], ["saare", "md"], ["best", ""], ["sellers,", ""], ["traffic", ""], ["source", ""], ["aur", ""], ["theme", ""], ["ki", ""], ["saari", ""], ["information", ""], ["tumhe", ""], ["de", ""], ["dega", ""]]).map((x) => x.t);
const K_ = seg(20.43, 21.08, [["Doosra", "lg"], ["hai", "lg acc"]]);
const TOOL2 = 21.26;
const M_ = seg(23.21, 25.8, [["Yeh", "md"], ["tumhe", "md"], ["product", "lg acc"], ["add", "md"], ["karne", "md"], ["se", "md"], ["PEHLE", "lg hl"], ["HI", "lg hl"], ["bata", "md"], ["dega", "md"]]);
const N_ = seg(25.92, 27.26, [["ki", "md"], ["kitna", "md"], ["PROFIT", "lg acc"], ["MARGIN", "lg acc"], ["banega", "md"]]);
const O_ = seg(27.67, 28.38, [["Aur", "md"], ["3RD", "xl acc"], ["hai", "lg"]]);
const P_ = seg(28.73, 31.76, [["is", "md"], ["tool", "md"], ["ki", "md"], ["help", "md"], ["se", "md"], ["tum", "md"], ["apne", "md"], ["COMPETITOR", "xl acc"], ["ke", "md"], ["WINNING", "lg hl"], ["ADS", "lg hl"], ["SPY", "lg acc"]]);
const Q_ = seg(31.88, 32.63, [["kar", "md"], ["sakte", "md"], ["ho", "md"]]);
const R_ = seg(33.07, 34.56, [["Aur", "md"], ["in", "md"], ["teeno", "md"], ["TOOLS", "lg acc"], ["ka", "md"], ["LINK", "lg hl"], ["chahiye?", "lg"]]);
const S_ = seg(34.91, 35.89, [["Toh", "md"], ["comment", "lg"], ["karo", "lg"], ["“META”", "huge acc"]]);
const T_ = seg(36.24, 37.88, [["aur"], ["link"], ["seedha"], ["aapke"], ["DM"], ["mein"]]).map((x) => x.t);

const CUT = { c1: 0, c2: 2.0, c3: 4.37, c4: 7.59, c5: 11.47, c6: 14.45, c7: 20.21, c8: 22.98, c9: 27.47, c10: P_[5].t - 0.1, c11: 32.85, c12: 34.73, out: 38.0 };

const scenes = [
  { id: "c1", start: CUT.c1, end: CUT.c2, lines: [A_.slice(0, 2), A_.slice(2, 3), A_.slice(3)] },
  { id: "c2", start: CUT.c2, end: CUT.c3, lines: [B_.slice(0, 2), B_.slice(2, 4), B_.slice(4)], shake: B_[2].t + 0.05, extra: `
      <div class="exts">${["🧩", "🧮", "🔍"].map((e, i) => `<div class="ext" id="c2-e${i}">${e}</div>`).join("")}</div>`,
    tweens: (A) => { [0, 0.1, 0.2].forEach((d, i) => A.pop(`#c2-e${i}`, +(B_[3].t + d).toFixed(2))); } },
  { id: "c3", start: CUT.c3, end: CUT.c4, lines: [D_.slice(0, 4), [D_[4], D_[5], E_[0]], E_.slice(1)], extra: `
      <div class="lvl"><span class="lvl-a">BEGINNER</span><div class="lvl-bar"><i id="c3-fill"></i></div><span class="lvl-b">PRO</span></div>`,
    tweens: (A) => { T(`tl.fromTo("#c3-fill",{scaleX:0},{scaleX:1,duration:${(E_[0].t - D_[4].t + 0.1).toFixed(2)},ease:"power2.inOut"},${D_[4].t});`); S(D_[4].t, "riser", .35); } },
  { id: "c4", start: CUT.c4, end: CUT.c5, lines: [F_.slice(0, 2), F_.slice(2, 3), F_.slice(3, 6), F_.slice(6)], extra: `
      <div class="dash" id="c4-dash">${[38, 62, 48, 80, 66, 95].map((h, i) => `<b id="c4-b${i}" style="height:${h}%"></b>`).join("")}</div>`,
    tweens: (A) => { T(`tl.fromTo("#c4-dash b",{scaleY:0},{scaleY:1,duration:.45,ease:"back.out(1.6)",stagger:.06},${F_[5].t});`); } },
  { id: "c5", start: CUT.c5, end: CUT.c6, lines: [G_], extra: toolCard("c5-tool", 1, "🧩", "Free Trendtrack Chrome Extension", "FREE · CHROME EXTENSION"),
    tweens: (A) => { A.pop("#c5-tool", TOOL1, 0.5); S(TOOL1, "impact_lite", .5); } },
  { id: "c6", start: CUT.c6, end: CUT.c7, top: true, lines: [[w("Yeh", J_[0], "md"), w("competitors", J_[1], "md acc"), w("ke", J_[2], "md"), w("saare", J_[3], "md")]], extra: `
      <div class="chips2">
        <div class="chip2" id="c6-k0"><span>01</span>BEST SELLERS</div>
        <div class="chip2" id="c6-k1"><span>02</span>TRAFFIC SOURCE</div>
        <div class="chip2" id="c6-k2"><span>03</span>THEME</div>
      </div>
      <div class="line c6-end"><span class="w-inline hlw" id="c6-info">INFORMATION</span> <span class="w-inline" id="c6-t">tumhe</span> <span class="w-inline" id="c6-d">de dega</span></div>`,
    tweens: (A) => {
      const k = [J_[4], J_[6], J_[9]], nxt = [J_[6], J_[9], J_[12]];
      k.forEach((t, i) => { A.pop(`#c6-k${i}`, t, 0.4); A.activate(`#c6-k${i}`, t, nxt[i]); });
      A.pop("#c6-info", J_[12]);
      T(`tl.fromTo("#c6-t",{opacity:0,y:30},{opacity:1,y:0,duration:.22},${J_[13]});`); T(`tl.fromTo("#c6-d",{opacity:0,y:30},{opacity:1,y:0,duration:.22},${J_[14]});`);
    } },
  { id: "c7", start: CUT.c7, end: CUT.c8, lines: [K_], extra: toolCard("c7-tool", 2, "🧮", "E-Commerce Profit Calculator", "COST → PRICE → PROFIT") + `
      <div class="calc" id="c7-calc">
        <div class="cr"><span>Product cost</span><b>₹ 450</b></div>
        <div class="cr"><span>Selling price</span><b>₹ 1,199</b></div>
        <div class="cr"><span>Shipping + fees</span><b>₹ 260</b></div>
        <div class="cr tot"><span>Profit</span><b>₹ 489</b></div>
      </div>`,
    tweens: (A) => {
      A.pop("#c7-tool", TOOL2, 0.5); S(TOOL2, "impact_lite", .5);
      T(`tl.fromTo("#c7-calc .cr",{opacity:0,x:40},{opacity:1,x:0,duration:.3,ease:"power3.out",stagger:.15},${TOOL2 + 0.5});`);
    } },
  { id: "c8", start: CUT.c8, end: CUT.c9, lines: [M_.slice(0, 3), M_.slice(3, 6), M_.slice(6), N_], extra: `<div class="margin"><div class="m-bar"><i id="c8-fill"></i></div><span id="c8-pct">MARGIN ✓</span></div>`,
    tweens: (A) => { T(`tl.fromTo("#c8-fill",{scaleX:0},{scaleX:.72,duration:.6,ease:"power2.out"},${N_[2].t});`); A.pop("#c8-pct", N_[4].t); S(N_[4].t, "cash", .45); } },
  { id: "c9", start: CUT.c9, end: CUT.c10, lines: [O_.slice(0, 1), O_.slice(1), P_.slice(0, 5)], shake: O_[1].t + 0.05, extra: toolCard("c9-tool", 3, "🔍", "Winning-ads spy tool", "SEE WHAT YOUR COMPETITORS RUN"),
    tweens: (A) => { A.pop("#c9-tool", P_[0].t, 0.45); } },
  { id: "c10", start: CUT.c10, end: CUT.c11, lines: [P_.slice(5, 7), P_.slice(7, 9), P_.slice(9, 11), [P_[11], ...Q_]], extra: `
      <div class="cards">
        <div class="ad ad1" id="c10-a1"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
        <div class="ad ad2" id="c10-a2"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
        <div class="ad ad3" id="c10-a3"><div class="ad-img"></div><div class="ad-l"></div><div class="ad-l s"></div></div>
      </div>`,
    tweens: (A) => { A.fan(["#c10-a1", "#c10-a2", "#c10-a3"], P_[9].t); } },
  { id: "c11", start: CUT.c11, end: CUT.c12, lines: [R_.slice(0, 3), R_.slice(3, 6), R_.slice(6)], extra: `
      <div class="exts">${["🧩", "🧮", "🔍"].map((e, i) => `<div class="ext" id="c11-e${i}">${e}</div>`).join("")}</div>`,
    tweens: (A) => { [0, 0.1, 0.2].forEach((d, i) => A.pop(`#c11-e${i}`, +(R_[3].t + d).toFixed(2))); } },
  { id: "c12", start: CUT.c12, end: CUT.out, lines: [S_.slice(0, 3), S_.slice(3)], shake: S_[3].t + 0.05, extra: `
      <div class="cmt" id="c12-cmt">
        <div class="cmt-av"><img src="brand/logo-mark.png" alt="" /></div>
        <div class="cmt-in"><span class="cmt-ph">Add a comment…</span><span class="cmt-txt">${["M", "E", "T", "A"].map((c, i) => `<b id="c12-k${i}">${c}</b>`).join("")}</span></div>
        <div class="cmt-send" id="c12-send">Post</div>
      </div>
      <div class="dm">${["aur", "link", "seedha", "aapke", "DM", "mein ✉"].map((x, i) => `<span class="w-inline${x === "DM" ? " dmk" : ""}" id="c12-d${i}">${x}</span>`).join(" ")}</div>`,
    tweens: (A) => {
      const c0 = S_[3].t + 0.3;
      A.pop("#c12-cmt", +(c0 - 0.05).toFixed(2), 0.35);
      T(`tl.fromTo("#c12-cmt .cmt-ph",{opacity:1},{opacity:0,duration:.05,immediateRender:false},${(c0 + 0.2).toFixed(2)});`);
      [0, 1, 2, 3].forEach((i) => { const t = +(c0 + 0.25 + i * 0.08).toFixed(2); S(t, "tick", .5); T(`tl.fromTo("#c12-k${i}",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.12,ease:"back.out(3)"},${t});`); });
      const post = T_[1];
      S(post, "click", .9); S(post + 0.06, "ding", .55);
      T(`tl.to("#c12-send",{scale:.88,duration:.07,yoyo:true,repeat:1},${post});`);
      T(`tl.to("#c12-send",{backgroundColor:"#8B2FE8",color:"#FFFFFF",duration:.1},${(post + 0.06).toFixed(2)});`);
      T_.forEach((t, i) => T(`tl.fromTo("#c12-d${i}",{opacity:0,y:30},{opacity:1,y:0,duration:.22,ease:"back.out(2)"},${t});`));
    } },
  { id: "out", start: CUT.out, end: DUR, lines: [], noDrift: true, extra: `
      <div class="outro">
        <div class="logo-wrap" id="out-logo"><div class="logo-ring" id="out-ring"></div><img class="logo-big" src="brand/logo.png" alt="The GrowthX Studio" /></div>
        <div class="outro-r">
          <div class="pill" id="out-pill">COMMENT “META” 💬</div>
          <div class="mail" id="out-mail"><span class="mail-ico">✉</span> thegrowthxstudio@gmail.com</div>
          <div class="tagline" id="out-tag">BUILD <i>•</i> GROW <i>•</i> SCALE</div>
        </div>
      </div>`,
    tweens: (A) => {
      const o = CUT.out;
      T(`tl.fromTo("#out-logo",{opacity:0,scale:.5,rotation:-25},{opacity:1,scale:1,rotation:0,duration:.7,ease:"back.out(1.7)"},${o + 0.05});`);
      T(`tl.fromTo("#out-ring",{opacity:.9,scale:1},{opacity:0,scale:1.6,duration:.9,ease:"power2.out"},${o + 0.2});`);
      T(`tl.to("#out-logo",{scale:1.04,duration:2,ease:"sine.inOut"},${o + 0.75});`);
      A.pop("#out-pill", +(o + 0.5).toFixed(2), 0.45); A.pop("#out-mail", +(o + 0.75).toFixed(2), 0.45);
      T(`tl.fromTo("#out-tag",{opacity:0,x:-40},{opacity:1,x:0,duration:.6,ease:"power3.out"},${(o + 1.0).toFixed(2)});`);
      S(o + 0.05, "impact", .8); S(o + 0.1, "shimmer", .55);
    } },
];

const wipes = [CUT.c2, CUT.c3, CUT.c4, CUT.c5, CUT.c6, CUT.c7, CUT.c8, CUT.c9, CUT.c10, CUT.c11, CUT.c12, CUT.out];

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
// Hook tag, on screen from the first frame.
T(`tl.fromTo("#hook-tag",{scale:.85},{scale:1,duration:.4,ease:"back.out(2)"},0);`);

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

S(0.0, "impact", .6); S(0.55, "impact_lite", .4);
T(`tl.fromTo("#bg-ring1",{rotation:0},{rotation:120,duration:${DUR},ease:"none"},0);`);
T(`tl.fromTo("#bg-ring2",{rotation:0},{rotation:-90,duration:${DUR},ease:"none"},0);`);

// Background glow drift.
T(`tl.fromTo("#glow",{xPercent:-20,yPercent:-10},{xPercent:20,yPercent:10,duration:${DUR},ease:"sine.inOut"},0);`);
// Progress bar.
T(`tl.fromTo("#progress i",{scaleX:0},{scaleX:1,duration:${DUR},ease:"none"},0);`);

const html = `<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>GrowthX 3 Ecom Tools</title>
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
      #hook-tag { top:44px; }
      .exts { display:flex; gap:40px; }
      .ext { width:150px; height:150px; border-radius:36px; display:flex; align-items:center; justify-content:center; font-size:84px; background:rgba(255,255,255,.06); border:3px solid var(--pur2); box-shadow:0 0 50px rgba(139,47,232,.45); }
      .lvl { display:flex; align-items:center; gap:28px; font-size:32px; font-weight:900; letter-spacing:.14em; }
      .lvl-a { color:var(--dim); } .lvl-b { color:var(--acc); }
      .lvl-bar { width:760px; height:34px; border-radius:17px; background:rgba(255,255,255,.08); border:2px solid rgba(166,92,255,.4); overflow:hidden; }
      .lvl-bar i, .m-bar i { display:block; height:100%; background:linear-gradient(90deg,var(--pur),var(--pur2),#fff); transform-origin:left center; box-shadow:0 0 24px var(--pur); }
      .dash { position:absolute; right:140px; bottom:120px; width:420px; height:300px; display:flex; align-items:flex-end; gap:22px; z-index:-1; opacity:.6; }
      .dash b { flex:1; display:block; border-radius:12px 12px 0 0; background:linear-gradient(180deg,var(--pur2),rgba(139,47,232,.2)); transform-origin:bottom center; }
      .tool { display:flex; align-items:center; gap:40px; padding:40px 56px; border-radius:36px; background:linear-gradient(135deg,rgba(139,47,232,.22),rgba(255,255,255,.04)); border:3px solid var(--pur2); box-shadow:0 0 90px rgba(139,47,232,.45); max-width:1500px; }
      .tool-n { font-size:120px; font-weight:900; color:var(--acc); line-height:1; text-shadow:0 0 40px rgba(139,47,232,.8); }
      .tool-ic { font-size:110px; line-height:1; }
      .tool-t { font-size:76px; font-weight:900; line-height:1.02; }
      .tool-s { margin-top:14px; font-size:30px; font-weight:700; letter-spacing:.16em; color:var(--acc); }
      .chips2 { display:flex; gap:36px; margin-top:50px; }
      .chip2 { display:flex; align-items:center; gap:22px; font-size:52px; font-weight:900; padding:30px 44px; border-radius:26px; border:3px solid rgba(255,255,255,.14); background:rgba(255,255,255,.04); }
      .chip2 span { font-size:30px; color:var(--acc); }
      .c6-end { margin-top:60px; font-size:84px; font-weight:700; gap:0 26px; }
      .hlw { font-size:128px; font-weight:900; color:#fff; padding:0 18px; border-radius:16px; background:linear-gradient(90deg,var(--pur),var(--pur2)); box-shadow:0 0 40px rgba(139,47,232,.55); }
      .calc { position:absolute; right:150px; bottom:90px; width:560px; padding:26px 32px; border-radius:24px; background:rgba(4,2,6,.85); border:2px solid rgba(166,92,255,.45); display:flex; flex-direction:column; gap:14px; }
      .cr { display:flex; justify-content:space-between; font-size:32px; font-weight:600; color:var(--dim); }
      .cr b { color:var(--ink); font-weight:900; }
      .cr.tot { border-top:2px solid rgba(166,92,255,.35); padding-top:14px; color:var(--acc); font-size:40px; }
      .cr.tot b { color:var(--acc); }
      #c7 .stage { gap:30px; } #c7 .tool { margin-bottom:200px; }
      .margin { display:flex; align-items:center; gap:30px; margin-top:20px; }
      .m-bar { width:700px; height:30px; border-radius:15px; background:rgba(255,255,255,.08); overflow:hidden; }
      #c8-pct { font-size:40px; font-weight:900; color:var(--acc); letter-spacing:.1em; }
      #c8 .stage { gap:10px; }
      #c12 .huge { font-size:290px; margin-top:20px; }
      #c11 .wa { font-size:128px; }
      #c10 .text { position:relative; z-index:2; background:rgba(4,2,6,.78); padding:24px 56px; border-radius:30px; }
      #c4 .dash { right:50px; width:340px; height:260px; }
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

      <div class="hook-ui clip" id="hook-ui" data-start="0" data-duration="${CUT.c2}" data-track-index="4">
        <div id="hook-tag">3 FREE E-COM TOOLS</div>
      </div>

      ${sceneHtml}


      <div id="wipe" class="clip" data-start="0" data-duration="${DUR}" data-track-index="6"><div class="wp"></div></div>
      <div id="brand" class="clip" data-start="0" data-duration="${CUT.out}" data-track-index="8"><div class="bi"><img src="brand/logo-mark.png" alt="GX" /><span>THE GROWTH<b>X</b> STUDIO</span></div></div>
      <div id="progress" class="clip" data-start="0" data-duration="${DUR}" data-track-index="9"><i></i></div>

      <audio id="vo" src="assets/voiceover.m4a" data-start="0" data-duration="38.11" data-track-index="12" data-volume="1"></audio>
      <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="${DUR}" data-track-index="11" data-volume="0.55"></audio>
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
