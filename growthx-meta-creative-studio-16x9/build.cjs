// Run: node build.cjs  (regenerates index.html; edit word timings in the scenes list)
// Generates growthx-meta-creative-studio-16x9/index.html (static clips, one paused GSAP timeline).
const fs = require("fs");
const out = process.argv[2] || require("path").join(__dirname, "index.html");
const DUR = +(JSON.parse(fs.readFileSync(require("path").join(__dirname, "phrases.json"))).duration + 2.9).toFixed(2);
const sfx = [];
const S = (t, type, vol = 1) => sfx.push({ t: +t.toFixed(3), type, vol });

// w(text, t, cls) — one spoken word, revealed at global time t.
const w = (text, t, cls = "") => ({ text, t, cls });
// Voiceover: ElevenLabs "Bunty – Fun Podcast Host" (assets/voiceover.wav), starts at 0.
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
const wl = (str, cls = "") => str.split(" ").map((x) => [x, cls]);

// Caption bar for the UI-mock scenes (most viewers watch muted).
let capN = 0;
const capBar = (phrases) => {
  const html = phrases.map((ws) => {
    const id = `cap${capN++}`;
    return { id, ws, html: `<div class="cap" id="${id}">${ws.map((x, i) => `<span class="cw" id="${id}-${i}">${x.text}</span>`).join(" ")}</div>` };
  });
  return {
    html: `<div class="capbar">${html.map((h) => h.html).join("")}</div>`,
    tweens: () => html.forEach((h, k) => {
      const next = html[k + 1];
      T(`tl.fromTo("#${h.id}",{opacity:0},{opacity:1,duration:.08},${h.ws[0].t});`);
      if (next) T(`tl.to("#${h.id}",{opacity:0,duration:.06},${(next.ws[0].t - 0.02).toFixed(2)});`);
      h.ws.forEach((x, i) => T(`tl.fromTo("#${h.id}-${i}",{opacity:.35},{opacity:1,duration:.1},${x.t});`));
    }),
  };
};
// Cursor helpers: move to (x, y) at t, click at t.
const curTo = (id, x, y, t, d = 0.35) => T(`tl.to("#${id}",{x:${x},y:${y},duration:${d},ease:"power3.inOut"},${t.toFixed(2)});`);
const click = (id, target, t) => {
  S(t, "click", .8);
  T(`tl.to("#${id}",{scale:.82,duration:.07,yoyo:true,repeat:1},${t.toFixed(2)});`);
  if (target) T(`tl.to("${target}",{scale:.95,duration:.07,yoyo:true,repeat:1},${t.toFixed(2)});`);
};
const on = (sel, t, bg = "#8B2FE8", color = "#FFFFFF") => T(`tl.to("${sel}",{backgroundColor:"${bg}",borderColor:"#B57BFF",color:"${color}",duration:.15},${t.toFixed(2)});`);

// Phrase spans of assets/voiceover.wav (ElevenLabs "Bunty – Fun Podcast Host", eleven_v4) live in
// phrases.json, measured with silencedetect and checked phrase by phrase with local Whisper.
const SP = JSON.parse(fs.readFileSync(require("path").join(__dirname, "phrases.json"))).spans;
const ph = (i, toks) => seg(SP[i][0], SP[i][1], toks);
const tw = (str, cls = "md") => str.split(" ").map((x) => [x, cls]);

const P0 = ph(0, [["Meta", "lg acc"], ["ne", "md"], ["AD", "lg"], ["BANANE", "lg"], ["ka", "md"], ["tareeka", "md"], ["hi", "md"], ["BADAL", "xl acc"], ["diya", "lg"], ["hai!", "lg"]]);
const P1 = ph(1, tw("Naya Ads Creative Studio launch hua hai,"));
const P2 = ph(2, [["aur", "md"], ["jo", "md"], ["log", "md"], ["PAID", "lg acc"], ["ADS", "lg acc"], ["chalate", "md"], ["hain,", "md"], ["unhe", "sm"], ["isse", "sm"], ["MASSIVE", "xl"], ["ADVANTAGE", "xl acc"], ["milega.", "md"]]);
const P3 = ph(3, [["Ise", "md"], ["ek", "md"], ["END-TO-END", "xl acc"], ["creative", "md"], ["solution", "md"], ["samjhiye.", "md"]]);
const P4 = ph(4, tw("Pehle, ye batata hai ki aapke best ads mein actually kya kaam kar raha hai."));
const P5 = ph(5, tw("Phir aapke ads ko aapki niche ke top performers se compare karta hai,"));
const P6 = ph(6, tw("aur batata hai ki kya change karna hai."));
const P7 = ph(7, [["Ab", "lg"], ["BEST", "huge acc"], ["PART:", "huge"]]);
const P8 = ph(8, tw("Meta ka Gen AI, inhi insights se naye ad concepts khud bana deta hai,"));
const P9 = ph(9, tw("aapke brand ki messaging, branding aur guidelines ke hisaab se."));
const P10 = ph(10, tw("Aap comment, guide aur iterate kar sakte hain, ya seedha A/B test launch kar sakte hain."));
const P11 = ph(11, tw("Performance data ke saath, ye creatives ko lagatar behtar karta rehta hai."));
const P12 = ph(12, [["Aur", "md"], ["aapki", "md"], ["PERMISSION", "lg acc"], ["ke", "md"], ["bina,", "md"], ["kuch", "md"], ["bhi", "md"], ["PUBLISH", "lg"], ["NAHI", "lg red"], ["hota.", "md"]]);
const P13 = ph(13, tw("Winners ko scale kijiye, aur naye styles ya products ke liye nayi variations banaiye."));
const P14 = ph(14, tw("Ye ek self-improving loop hai, jo aapke business aur customers ko samajhta hai."));
const P15 = ph(15, tw("Paid ads ka future yahi hai, aur rollout shuru ho chuka hai."));
const P16 = ph(16, [["Comment", "lg"], ["kijiye", "lg"], ["“STUDIO”", "huge acc"]]);
const P17 = ph(17, [["aur"], ["poora"], ["setup"], ["guide"], ["main"], ["aapko"], ["DM"], ["kar"], ["dunga"]]).map((x) => x.t);
const at = (ws, i) => ws[i].t;

const capA = capBar([P1]);
const capC = capBar([P4, P5, P6]);
const capD = capBar([P8, P9]);
const capE = capBar([P10, P11]);
const capG = capBar([P13]);
const capH = capBar([P14, P15]);

const VOEND = SP[SP.length - 1][1];
const cut = (i) => +(SP[i][0] - 0.1).toFixed(2);
const CUT = { a: 0, b1: cut(2), b2: cut(3), c: cut(4), d1: cut(7), d: cut(8), e: cut(10), f: cut(12), g: cut(13), h: cut(14), i: cut(16), out: +(VOEND + 0.15).toFixed(2) };
const stepPill = (n, label) => `<div class="steppill"><b>STEP ${n}/3</b></div><div class="stepbig" id="sb${n}"><b>0${n}</b><span>${label}</span></div>`;
const winBar = (title) => `<div class="wbar"><i></i><i></i><i></i><span>${title}</span></div>`;
const thumb = (cls, emo) => `<div class="thumb ${cls}"><span>${emo}</span></div>`;
const loopNodes = [["🔍", "Insights"], ["✨", "Create"], ["🧪", "Test"], ["📈", "Learn"]];

const scenes = [
  { id: "a", start: CUT.a, end: CUT.b1, split: true, noDrift: true, lines: [P0.slice(0, 2), P0.slice(2, 7), P0.slice(7)], extra: `
      <div class="rcol">
        <div class="newcard" id="a-card"><em>NEW</em><b>∞ Meta</b><span>Ads Creative Studio</span><i>Insights · Gen AI · Testing</i></div>
      </div>` + capA.html,
    tweens: (A) => {
      capA.tweens();
      T(`tl.fromTo("#a-card",{opacity:0,scale:.6,rotation:-8},{opacity:1,scale:1,rotation:0,duration:.6,ease:"back.out(1.7)"},${at(P1, 1)});`);
      S(at(P1, 1), "impact_lite", .5); S(at(P1, 1) + 0.1, "shimmer", .4);
      T(`tl.to("#a-card",{y:-14,duration:1.2,yoyo:true,repeat:1,ease:"sine.inOut"},${(at(P1, 1) + 0.6).toFixed(2)});`);
    } },

  { id: "b1", start: CUT.b1, end: CUT.b2, lines: [P2.slice(0, 7), P2.slice(7, 9), P2.slice(9)], extra: `
      <div class="bars" id="b1-bars">${[30, 48, 66, 92, 130].map((h, i) => `<i id="b1-b${i}" style="height:${h}px"></i>`).join("")}<span id="b1-up">📈</span></div>`,
    tweens: (A) => {
      T(`tl.fromTo("#b1-bars i",{scaleY:0},{scaleY:1,duration:.35,ease:"back.out(2)",stagger:.08},${at(P2, 9)});`);
      A.pop("#b1-up", +(at(P2, 10) + 0.2).toFixed(2), 0.35); S(at(P2, 10), "riser", .35);
    } },

  { id: "b2", start: CUT.b2, end: CUT.c, top: true, lines: [P3.slice(0, 2), P3.slice(2, 3), P3.slice(3)], extra: `
      <div class="pipe">${loopNodes.map(([e, n], i) => `${i ? `<b class="parr" id="b2-a${i}">➜</b>` : ""}<div class="pnode" id="b2-n${i}"><span>${e}</span>${n}</div>`).join("")}</div>`,
    tweens: (A) => {
      loopNodes.forEach((_, i) => { A.pop(`#b2-n${i}`, +(at(P3, 3) + i * 0.22).toFixed(2), 0.3); if (i) T(`tl.fromTo("#b2-a${i}",{opacity:0,x:-20},{opacity:1,x:0,duration:.2},${(at(P3, 3) + i * 0.22 - 0.08).toFixed(2)});`); });
    } },

  { id: "c", win: true, start: CUT.c, end: CUT.d1, noDrift: true, lines: [], extra: stepPill(1, "Insights") + `
      <div class="win" id="c-win">${winBar("Ads Creative Studio · Insights")}
        <div class="wbody">
          <div class="adrow" id="c-r0">${thumb("t1", "🧴")}<div><b>UGC hook · Serum</b><i>Spend ₹18k</i></div><em class="met">ROAS 4.1x</em><span class="toptag" id="c-top">🏆 Best</span></div>
          <div class="adrow" id="c-r1">${thumb("t2", "✨")}<div><b>Before / after</b><i>Spend ₹12k</i></div><em class="met">ROAS 2.6x</em></div>
          <div class="adrow" id="c-r2">${thumb("t3", "🛍️")}<div><b>Static · Offer</b><i>Spend ₹9k</i></div><em class="met low">ROAS 1.2x</em></div>
          <div class="bench" id="c-bench">
            <div class="brow"><span>Your ad · hook rate</span><div class="bbar"><i id="c-bb0" style="width:42%"></i></div></div>
            <div class="brow"><span>Niche top performers</span><div class="bbar top"><i id="c-bb1" style="width:78%"></i></div></div>
          </div>
          <div class="seorow"><span class="chip4 sm" id="c-s0">💡 Hook in first 2 sec</span><span class="chip4 sm" id="c-s1">💡 Show product in use</span><span class="chip4 sm" id="c-s2">💡 Add the offer</span></div>
        </div>
      </div>` + capC.html,
    tweens: (A) => {
      capC.tweens();
      T(`tl.fromTo("#c-win",{opacity:0,y:80},{opacity:1,y:0,duration:.45,ease:"power3.out"},${CUT.c});`);
      [0, 1, 2].forEach((i) => A.pop(`#c-r${i}`, +(at(P4, 4) + i * 0.15).toFixed(2), 0.3));
      A.pop("#c-top", at(P4, 10), 0.35); S(at(P4, 10), "ding", .45);
      A.pop("#c-bench", at(P5, 3), 0.35);
      T(`tl.fromTo("#c-bb0, #c-bb1",{scaleX:0},{scaleX:1,duration:.6,ease:"power2.out",stagger:.25},${at(P5, 8)});`); S(at(P5, 8), "riser", .3);
      [0, 1, 2].forEach((i) => A.pop(`#c-s${i}`, +(at(P6, 3) + i * 0.18).toFixed(2), 0.3));
    } },

  { id: "d1", start: CUT.d1, end: CUT.d, noDrift: true, shake: at(P7, 1) + 0.05, lines: [P7.slice(0, 1), P7.slice(1)], extra: "" },

  { id: "d", win: true, start: CUT.d, end: CUT.e, noDrift: true, lines: [], extra: stepPill(2, "Gen AI concepts") + `
      <div class="win" id="d-win">${winBar("Ads Creative Studio · Generate")}
        <div class="wbody">
          <div class="gen" id="d-gen"><span>✨ Generating new ad concepts…</span><div class="gbar"><i id="d-gb"></i></div></div>
          <div class="concepts">
            <div class="ccard" id="d-k0">${thumb("t1", "🧴")}<b>Glow in 7 days</b><i>UGC · 9:16</i></div>
            <div class="ccard" id="d-k1">${thumb("t2", "💧")}<b>Your skin, upgraded</b><i>Static · 1:1</i></div>
            <div class="ccard" id="d-k2">${thumb("t3", "🌿")}<b>Dermat approved</b><i>Carousel</i></div>
          </div>
          <div class="seorow"><span class="chip4 sm" id="d-b0">🗣 Messaging ✓</span><span class="chip4 sm" id="d-b1">🎨 Branding ✓</span><span class="chip4 sm" id="d-b2">📋 Guidelines ✓</span></div>
        </div>
      </div>` + capD.html,
    tweens: (A) => {
      capD.tweens();
      T(`tl.fromTo("#d-win",{opacity:0,y:80},{opacity:1,y:0,duration:.45,ease:"power3.out"},${CUT.d});`);
      T(`tl.fromTo("#d-gb",{scaleX:0},{scaleX:1,duration:${(at(P8, 9) - at(P8, 1)).toFixed(2)},ease:"power1.inOut"},${at(P8, 1)});`); S(at(P8, 1), "riser", .35);
      [0, 1, 2].forEach((i) => A.pop(`#d-k${i}`, +(at(P8, 8) + i * 0.15).toFixed(2), 0.35));
      S(at(P8, 9), "shimmer", .45);
      [3, 5, 7].forEach((w, i) => A.pop(`#d-b${i}`, at(P9, w), 0.3));
    } },

  { id: "e", win: true, start: CUT.e, end: CUT.f, noDrift: true, lines: [], extra: stepPill(3, "Iterate & test") + `
      <div class="win" id="e-win">${winBar("Ads Creative Studio · Glow in 7 days")}
        <div class="wbody">
          <div class="adrow sel">${thumb("t1", "🧴")}<div><b>Glow in 7 days</b><i>Concept v2 · ready</i></div></div>
          <div class="acts"><span class="actb" id="e-x0">💬 Comment</span><span class="actb" id="e-x1">🧭 Guide</span><span class="actb" id="e-x2">🔁 Iterate</span></div>
          <div class="abbtn" id="e-ab">🧪 Launch A/B test<i class="tap" id="e-tap"></i></div>
          <div class="chart" id="e-chart"><svg viewBox="0 0 800 200" preserveAspectRatio="none"><path id="e-line" d="M10 180 C140 170 200 150 300 120 S500 70 580 55 S720 25 790 15"/></svg><span class="vv" id="e-v">v1 → v2 → v3</span></div>
          <span class="chip4 sm" id="e-opt">📈 Optimizing with performance data</span>
        </div>
      </div>` + capE.html,
    tweens: (A) => {
      capE.tweens();
      T(`tl.fromTo("#e-win",{opacity:0,y:80},{opacity:1,y:0,duration:.45,ease:"power3.out"},${CUT.e});`);
      [1, 2, 4].forEach((w, i) => on(`#e-x${i}`, at(P10, w)));
      [1, 2, 4].forEach((w) => S(at(P10, w), "click", .6));
      A.pop("#e-ab", at(P10, 9), 0.35);
      const tap = at(P10, 11);
      S(tap, "click", .9);
      T(`tl.fromTo("#e-tap",{opacity:.9,scale:.2},{opacity:0,scale:2.4,duration:.5,ease:"power2.out"},${tap});`);
      T(`tl.to("#e-ab",{scale:.94,duration:.07,yoyo:true,repeat:1},${tap});`);
      A.pop("#e-chart", at(P11, 0), 0.35);
      A.draw("#e-line", at(P11, 1), 1.6); S(at(P11, 1), "riser", .3);
      A.pop("#e-v", at(P11, 7), 0.3); A.pop("#e-opt", at(P11, 9), 0.3);
    } },

  { id: "f", start: CUT.f, end: CUT.g, lines: [P12.slice(0, 5), P12.slice(5)], extra: `
      <div class="approve" id="f-ap"><span class="lock">🔒</span><div><b>3 new ads ready</b><i>Nothing goes live without you</i></div><span class="apbtn" id="f-btn">✅ Approve</span></div>`,
    tweens: (A) => {
      A.pop("#f-ap", at(P12, 2), 0.4); S(at(P12, 2), "click", .5);
      T(`tl.fromTo("#f-ap .lock",{rotation:0},{rotation:-14,duration:.12,yoyo:true,repeat:3},${at(P12, 8)});`);
    } },

  { id: "g", start: CUT.g, end: CUT.h, top: true, lines: [[w("WINNERS", at(P13, 0), "xl acc"), w("ko", at(P13, 1), "md"), w("SCALE", at(P13, 2), "xl"), w("kijiye", at(P13, 3), "md")]], extra: `
      <div class="scale">
        <div class="ccard win1" id="g-w">${thumb("t1", "🧴")}<b>Glow in 7 days</b><i>🏆 Winner · ROAS 4.1x</i></div>
        <b class="parr big" id="g-arr">➜</b>
        <div class="vars">
          <div class="ccard sm2" id="g-v0">${thumb("t2", "🎬")}<b>New style</b><i>Video · 9:16</i></div>
          <div class="ccard sm2" id="g-v1">${thumb("t3", "🧴")}<b>New product</b><i>Night cream</i></div>
          <div class="ccard sm2" id="g-v2">${thumb("t4", "🖼️")}<b>New format</b><i>Carousel</i></div>
        </div>
      </div>` + capG.html,
    tweens: (A) => {
      capG.tweens();
      A.pop("#g-w", at(P13, 0), 0.4); S(at(P13, 0), "cash", .45);
      T(`tl.fromTo("#g-arr",{opacity:0,x:-30},{opacity:1,x:0,duration:.25},${at(P13, 3)});`);
      [0, 1, 2].forEach((i) => A.pop(`#g-v${i}`, +(at(P13, 6) + i * 0.25).toFixed(2), 0.35));
    } },

  { id: "h", start: CUT.h, end: CUT.i, top: true, lines: [[w("SELF-IMPROVING", at(P14, 3), "lg acc"), w("LOOP", at(P14, 3) + 0.15, "lg")]], extra: `
      <div class="loop" id="h-loop">
        <div class="lring" id="h-ring"></div>
        ${loopNodes.map(([e, n], i) => `<div class="lnode l${i}" id="h-n${i}"><span>${e}</span>${n}</div>`).join("")}
        <div class="lcore" id="h-core">∞ Meta<br><i>knows your business</i></div>
      </div>
      <div class="rollout" id="h-roll">🚀 Rollout started</div>` + capH.html,
    tweens: (A) => {
      capH.tweens();
      loopNodes.forEach((_, i) => A.pop(`#h-n${i}`, +(at(P14, 0) + i * 0.2).toFixed(2), 0.3));
      T(`tl.fromTo("#h-ring",{rotation:0,opacity:0},{rotation:360,opacity:1,duration:${(CUT.i - at(P14, 0)).toFixed(2)},ease:"none"},${at(P14, 0)});`);
      A.pop("#h-core", at(P14, 8), 0.35);
      A.pop("#h-roll", at(P15, 7), 0.4); S(at(P15, 7), "impact_lite", .5);
    } },

  { id: "i", start: CUT.i, end: CUT.out, lines: [P16.slice(0, 2), P16.slice(2)], shake: at(P16, 2) + 0.05, extra: `
      <div class="cmt" id="i-cmt">
        <div class="cmt-av"><img src="brand/logo-mark.png" alt="" /></div>
        <div class="cmt-in"><span class="cmt-ph">Add a comment…</span><span class="cmt-txt">${[..."STUDIO"].map((c, i) => `<b id="i-k${i}">${c}</b>`).join("")}</span></div>
        <div class="cmt-send" id="i-send">Post</div>
      </div>
      <div class="dm">${["aur", "poora", "setup", "guide", "main", "aapko", "DM", "kar", "dunga 📩"].map((x, i) => `<span class="w-inline${x === "DM" || x === "setup" || x === "guide" ? " dmk" : ""}" id="i-d${i}">${x}</span>`).join(" ")}</div>`,
    tweens: (A) => {
      const c0 = at(P16, 2) + 0.2;
      A.pop("#i-cmt", +(c0 - 0.05).toFixed(2), 0.3);
      T(`tl.fromTo("#i-cmt .cmt-ph",{opacity:1},{opacity:0,duration:.05,immediateRender:false},${(c0 + 0.15).toFixed(2)});`);
      [..."STUDIO"].forEach((_, i) => { const t = +(c0 + 0.2 + i * 0.06).toFixed(2); S(t, "tick", .45); T(`tl.fromTo("#i-k${i}",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.1,ease:"back.out(3)"},${t});`); });
      const post = P17[1];
      S(post, "click", .9); S(post + 0.06, "ding", .55);
      T(`tl.to("#i-send",{scale:.88,duration:.07,yoyo:true,repeat:1},${post});`);
      T(`tl.to("#i-send",{backgroundColor:"#8B2FE8",color:"#FFFFFF",duration:.1},${(post + 0.06).toFixed(2)});`);
      P17.forEach((t, i) => T(`tl.fromTo("#i-d${i}",{opacity:0,y:30},{opacity:1,y:0,duration:.22,ease:"back.out(2)"},${t});`));
    } },

  { id: "out", start: CUT.out, end: DUR, lines: [], noDrift: true, extra: `
      <div class="outro">
        <div class="logo-wrap" id="out-logo"><div class="logo-ring" id="out-ring"></div><img class="logo-big" src="brand/logo.png" alt="The GrowthX Studio" /></div>
        <div class="outro-r">
          <div class="pill" id="out-pill">COMMENT “STUDIO” 💬</div>
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

const wipes = [CUT.b1, CUT.b2, CUT.c, CUT.d1, CUT.e, CUT.f, CUT.g, CUT.h, CUT.i, CUT.out];

let wordId = 0;
const words = [];
const sceneHtml = scenes.map((s, si) => {
  const lines = s.lines.map((line) => `<div class="line">${line.map((x) => {
    const id = `w${wordId++}`; words.push({ id, t: x.t, cls: x.cls });
    return `<span class="w ${x.cls}" id="${id}"><span class="wi">${x.text}</span></span>`;
  }).join("")}</div>`).join("\n");
  const layout = s.split ? "split" : s.top ? "top" : "center";
  return `
    <section id="${s.id}" class="clip scene ${layout}${s.win ? " wscene" : ""}" data-start="${s.start}" data-duration="${(s.end - s.start).toFixed(2)}" data-track-index="${2 + (si % 2)}">
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

// Background shapes drift (seek-safe, deterministic).
[["#sh0",40,60,180],["#sh1",-50,40,-200],["#sh2",30,-40,90],["#sh3",-60,-30,0],["#sh4",50,-50,160],["#sh5",-40,30,-120]].forEach(([sel,x,y,r]) => T(`tl.fromTo("${sel}",{x:0,y:0,rotation:0},{x:${x},y:${y},rotation:${r},duration:${DUR},ease:"sine.inOut"},0);`));
T(`tl.fromTo("#bg-stripe",{x:-120},{x:120,duration:${DUR},ease:"none"},0);`);
// Background glow drift.
T(`tl.fromTo("#glow",{xPercent:-20,yPercent:-10},{xPercent:20,yPercent:10,duration:${DUR},ease:"sine.inOut"},0);`);
// Progress bar.
T(`tl.fromTo("#progress i",{scaleX:0},{scaleX:1,duration:${DUR},ease:"none"},0);`);

const html = `<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>GrowthX Meta Ads Creative Studio</title>
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
      /* Ads Manager-style mocks (generic, no Meta branding) */
      .app { position:absolute; left:210px; top:110px; width:1500px; height:700px; border-radius:28px; background:#0E0A14; border:2px solid rgba(166,92,255,.45); overflow:hidden; display:flex; }
      .side { width:300px; padding-top:40px; background:#120C1A; border-right:2px solid rgba(166,92,255,.2); }
      .logo-s { height:0; overflow:visible; position:relative; top:-30px; left:30px; font-size:22px; font-weight:900; color:var(--acc); letter-spacing:.08em; }
      .si { height:70px; margin:0 16px; padding-left:24px; display:flex; align-items:center; font-size:30px; font-weight:700; color:var(--dim); border-radius:14px; border:2px solid transparent; }
      .main { position:relative; flex:1; }
      .mh { height:110px; display:flex; align-items:center; justify-content:space-between; padding:0 40px; border-bottom:2px solid rgba(166,92,255,.15); }
      .mh.full { position:absolute; left:0; right:0; top:0; }
      .mt { font-size:40px; font-weight:900; }
      .step { font-size:24px; font-weight:900; letter-spacing:.16em; color:var(--acc); }
      .btn { width:300px; height:60px; border-radius:14px; background:var(--pur); border:2px solid var(--pur2); display:flex; align-items:center; justify-content:center; font-size:26px; font-weight:900; }
      .rows { padding:40px; display:flex; flex-direction:column; gap:22px; }
      .rows i { display:block; height:56px; border-radius:12px; background:rgba(255,255,255,.04); }
      .menu { position:absolute; right:40px; top:100px; width:400px; padding:10px; border-radius:18px; background:#1A1224; border:2px solid rgba(166,92,255,.5); }
      .mi { height:70px; display:flex; align-items:center; padding-left:20px; font-size:28px; font-weight:700; border-radius:12px; border:2px solid transparent; }
      .grid { position:absolute; left:90px; top:140px; width:1320px; display:grid; grid-template-columns:1fr 1fr; gap:40px; }
      .src { height:200px; border-radius:22px; background:rgba(255,255,255,.04); border:2px solid rgba(255,255,255,.12); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; font-size:38px; font-weight:800; }
      .src span { font-size:22px; font-weight:700; letter-spacing:.12em; color:inherit; text-transform:uppercase; }
      .evs { position:absolute; left:90px; top:140px; width:1320px; display:flex; flex-direction:column; gap:20px; }
      .ev { height:80px; display:flex; align-items:center; gap:26px; padding-left:30px; border-radius:16px; background:rgba(255,255,255,.04); border:2px solid rgba(255,255,255,.12); font-size:32px; font-weight:700; opacity:0; }
      .box { --ck:0; position:relative; width:34px; height:34px; border-radius:8px; border:3px solid var(--acc); flex:none; }
      .box::after { content:"✓"; position:absolute; inset:-6px 0 0 3px; font-size:30px; font-weight:900; color:#fff; opacity:var(--ck); }
      .cursor2 { position:absolute; left:0; top:0; width:44px; height:56px; background:#fff; clip-path:polygon(0 0,0 80%,22% 62%,40% 100%,55% 94%,38% 58%,70% 58%); z-index:20; }
      .capbar { position:absolute; left:0; right:0; top:850px; height:120px; }
      .cap { position:absolute; left:50%; top:0; transform:translateX(-50%); white-space:nowrap; padding:16px 36px; border-radius:18px; background:#000; border:2px solid rgba(166,92,255,.5); font-size:46px; font-weight:800; opacity:0; }
      .cw { display:inline-block; }
      .card { position:absolute; left:360px; top:120px; width:1200px; padding:46px 56px; border-radius:28px; background:#0E0A14; border:2px solid rgba(166,92,255,.45); display:flex; flex-direction:column; gap:34px; }
      .card.wide { left:260px; width:1400px; }
      .ch { font-size:44px; font-weight:900; }
      .row { display:flex; align-items:center; justify-content:space-between; font-size:34px; padding-top:22px; border-top:2px solid rgba(166,92,255,.15); }
      .row.col { flex-direction:column; align-items:stretch; gap:22px; }
      .k { color:var(--dim); font-weight:700; } .v { font-weight:800; }
      .pill2 { padding:10px 24px; border-radius:999px; background:var(--pur); font-weight:900; }
      .slider { position:relative; height:44px; }
      .track { position:absolute; left:0; right:0; top:16px; height:12px; border-radius:6px; background:rgba(255,255,255,.1); overflow:hidden; }
      .track i { display:block; height:100%; background:var(--pur2); transform-origin:left center; }
      .knob { position:absolute; left:0; top:0; width:44px; height:44px; border-radius:50%; background:#fff; border:6px solid var(--pur); }
      .ticks { display:flex; justify-content:space-between; font-size:26px; font-weight:700; color:var(--dim); }
      .big1 { position:absolute; right:150px; top:640px; font-size:200px; font-weight:900; color:var(--acc); line-height:1; }
      .search { height:96px; border-radius:18px; border:3px solid var(--pur2); background:#000; display:flex; align-items:center; gap:20px; padding:0 30px; font-size:40px; font-weight:800; }
      .typed b { display:inline-block; font-weight:800; }
      .caret { width:4px; height:46px; background:var(--acc); }
      .res { display:flex; flex-direction:column; gap:14px; }
      .ri { display:flex; align-items:center; justify-content:space-between; padding:20px 26px; border-radius:16px; background:rgba(255,255,255,.05); border:2px solid rgba(255,255,255,.1); }
      .ri.dim { opacity:.55; }
      .ri b { display:block; font-size:36px; } .ri span { display:block; font-size:24px; color:var(--dim); margin-top:6px; }
      .add { padding:12px 28px; border-radius:12px; border:2px solid var(--pur2); font-size:28px; font-weight:900; color:var(--acc); }
      .selrow { display:flex; align-items:center; gap:24px; font-size:32px; }
      .chip3 { padding:10px 24px; border-radius:999px; background:var(--pur); font-weight:900; }
      .stamp { position:absolute; right:180px; top:640px; padding:10px 46px; border:10px solid var(--acc); border-radius:24px; font-size:180px; font-weight:900; color:var(--acc); line-height:1; }
      .crowd { display:flex; gap:18px; flex-wrap:wrap; justify-content:center; width:1100px; font-size:52px; }
      .pp { display:block; }
      #s8 .huge { font-size:290px; margin-top:20px; }
      /* No glow anywhere */
      #root * { text-shadow:none !important; }
      #glow { display:none !important; }
      .bg-ring { box-shadow:none !important; }
      #bg-ring1 { border-color:rgba(166,92,255,.28); border-top-color:rgba(181,123,255,.75); border-right-color:transparent; }
      #bg-ring2 { border-color:rgba(166,92,255,.16); border-left-color:rgba(181,123,255,.55); border-bottom-color:transparent; }
      .wash { position:absolute; inset:0; background:linear-gradient(135deg,rgba(139,47,232,.22) 0%,rgba(139,47,232,0) 38%,rgba(139,47,232,0) 62%,rgba(139,47,232,.26) 100%); }
      .dots-bg { position:absolute; width:420px; height:300px; background-image:radial-gradient(rgba(181,123,255,.55) 3px,transparent 3.5px); background-size:34px 34px; }
      .dots-bg.dl { left:40px; bottom:60px; } .dots-bg.dr { right:40px; top:140px; }
      .stripe { position:absolute; left:-200px; top:930px; width:2400px; height:70px; background:repeating-linear-gradient(-45deg,rgba(139,47,232,.35) 0 18px,transparent 18px 40px); transform-origin:center; rotate:-4deg; }
      .shp { position:absolute; }
      .sh-c { left:140px; top:180px; width:120px; height:120px; border-radius:50%; border:8px solid rgba(166,92,255,.55); }
      .sh-c2 { right:220px; bottom:200px; width:70px; height:70px; border-radius:50%; background:rgba(139,47,232,.55); }
      .sh-s { right:120px; top:420px; width:90px; height:90px; border-radius:18px; border:8px solid rgba(166,92,255,.45); }
      .sh-t { left:260px; bottom:260px; width:0; height:0; border-left:55px solid transparent; border-right:55px solid transparent; border-bottom:95px solid rgba(139,47,232,.45); }
      .sh-p, .sh-p2 { width:90px; height:90px; }
      .sh-p::before, .sh-p::after, .sh-p2::before, .sh-p2::after { content:""; position:absolute; background:rgba(181,123,255,.6); border-radius:6px; }
      .sh-p::before, .sh-p2::before { left:36%; top:0; width:28%; height:100%; }
      .sh-p::after, .sh-p2::after { left:0; top:36%; width:100%; height:28%; }
      .sh-p { left:880px; top:40px; } .sh-p2 { right:520px; bottom:20px; width:64px; height:64px; }
      .pill, .hlw, .tool, .logo-big, .ext, .cmt, #hook-tag, #progress i, .chart path { box-shadow:none !important; filter:none !important; }
      .hl::before { box-shadow:none !important; }
      .shot { position:absolute; border-radius:24px; overflow:hidden; border:5px solid var(--pur); background:#fff; }
      .zoom { position:absolute; left:0; top:0; transform-origin:0 0; }
      .simg { position:absolute; left:0; top:0; }
      .ring { position:absolute; border:6px solid var(--pur); border-radius:14px; opacity:0; }
      .cursor3 { position:absolute; left:0; top:0; width:44px; height:56px; background:#111; border:0; clip-path:polygon(0 0,0 80%,22% 62%,40% 100%,55% 94%,38% 58%,70% 58%); }
      .evcard { position:absolute; right:150px; bottom:250px; width:860px; padding:26px 30px; border-radius:22px; background:#0E0A14; border:3px solid var(--pur2); display:flex; flex-direction:column; gap:14px; }
      .evh { font-size:30px; font-weight:900; color:var(--acc); letter-spacing:.1em; }
      .ev2 { display:flex; align-items:center; gap:20px; padding:14px 18px; border-radius:14px; border:2px solid rgba(255,255,255,.12); font-size:28px; font-weight:700; }
      .ev2.dim { opacity:.55; }
      .big1.b1l { right:auto; left:150px; top:470px; font-size:180px; }
      .locchip { position:absolute; left:150px; top:700px; padding:16px 28px; border-radius:999px; background:var(--pur); font-size:36px; font-weight:900; }
      .locchip span { font-weight:600; font-size:28px; opacity:.85; }
      /* ---- 16:9 layout: UI windows right, step number + captions left ---- */
      #brand { right:50px; top:36px; }
      .sh-p { left:auto; right:90px; top:560px; } .sh-t { left:140px; bottom:140px; }
      .sm { font-size:52px; } .md { font-size:72px; } .lg { font-size:110px; } .xl { font-size:150px; } .huge { font-size:260px; }
      .line { gap:0 22px; }
      .scene.split .stage { padding:0 110px; gap:60px; }
      .scene.split .text { width:820px; margin-left:0; }
      .capbar { position:absolute; left:0; right:0; top:960px; height:90px; }
      .cap { font-size:40px; padding:12px 32px; }
      .wscene .capbar { left:110px; right:auto; top:640px; width:700px; height:260px; }
      .wscene .cap { left:0; transform:none; white-space:normal; width:700px; font-size:46px; line-height:1.3; padding:22px 30px; }
      .org { display:flex; flex-direction:column; align-items:center; width:860px; }
      .root-node { padding:18px 44px; border-radius:22px; background:var(--pur); font-size:48px; font-weight:900; }
      .branch { width:760px; height:40px; border:4px solid var(--pur2); border-bottom:0; border-radius:20px 20px 0 0; margin-top:22px; transform-origin:center top; }
      .agents { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; width:860px; margin-top:10px; }
      .ag { display:flex; flex-direction:column; align-items:center; gap:8px; padding:22px 10px; border-radius:22px; background:#0E0A14; border:3px solid rgba(166,92,255,.55); font-size:30px; font-weight:800; }
      .ag span { font-size:52px; }
      .jobs { display:grid; grid-template-columns:1fr 1fr; gap:22px; width:1300px; margin-top:10px; }
      .job { display:flex; align-items:center; gap:24px; padding:26px 30px; border-radius:26px; background:#0E0A14; border:3px solid rgba(255,255,255,.14); }
      .job span { font-size:64px; } .job b { display:block; font-size:44px; font-weight:900; } .job i { display:block; font-style:normal; font-size:28px; color:var(--dim); margin-top:4px; }
      .scene.top .stage { padding-top:120px; gap:30px; }
      .steps5 { display:flex; gap:28px; margin-top:20px; }
      .steps5 b { width:120px; height:120px; border-radius:50%; background:var(--pur); display:flex; align-items:center; justify-content:center; font-size:60px; font-weight:900; }
      .steppill { position:absolute; left:110px; top:170px; padding:14px 28px; border-radius:999px; background:#0E0A14; border:3px solid var(--pur2); font-size:32px; font-weight:800; }
      .steppill b { color:var(--acc); margin-right:10px; }
      .stepbig { position:absolute; left:110px; top:250px; width:720px; }
      .stepbig b { display:block; font-size:230px; font-weight:900; line-height:.9; color:#24103A; -webkit-text-stroke:4px var(--pur2); letter-spacing:-.03em; }
      .stepbig span { display:block; margin-top:14px; font-size:62px; font-weight:900; line-height:1.05; }
      .win { position:absolute; left:910px; top:130px; width:900px; border-radius:30px; background:#0E0A14; border:3px solid rgba(166,92,255,.55); overflow:hidden; }
      .wbar { height:66px; display:flex; align-items:center; gap:14px; padding:0 26px; background:#170F21; border-bottom:2px solid rgba(166,92,255,.25); }
      .wbar i { width:16px; height:16px; border-radius:50%; background:#3A2F4A; } .wbar i:first-child { background:#FF5F57; } .wbar i:nth-child(2) { background:#FEBC2E; } .wbar i:nth-child(3) { background:#28C840; }
      .wbar span { margin-left:14px; font-size:28px; font-weight:800; color:var(--dim); }
      .wbody { padding:30px 34px; display:flex; flex-direction:column; gap:22px; }
      .btnp { align-self:flex-start; padding:16px 30px; border-radius:16px; border:3px solid var(--pur2); font-size:34px; font-weight:900; color:var(--acc); }
      .pname { display:flex; flex-direction:column; gap:6px; padding:18px 24px; border-radius:16px; background:rgba(255,255,255,.05); }
      .pname span, .plabel { font-size:24px; color:var(--dim); font-weight:700; } .pname b { font-size:38px; }
      .prompt { padding:20px 24px; border-radius:16px; border:2px solid rgba(166,92,255,.45); background:#000; }
      .prompt p { margin-top:8px; font-size:31px; font-weight:600; line-height:1.35; }
      .chip4 { align-self:flex-start; padding:16px 26px; border-radius:999px; background:var(--pur); font-size:31px; font-weight:900; }
      .chip4.sm { font-size:28px; padding:12px 22px; }
      .conn { display:flex; justify-content:space-between; align-items:center; padding:18px 26px; border-radius:16px; border:2px solid rgba(255,255,255,.12); font-size:36px; font-weight:800; }
      .conn.dim { opacity:.5; }
      .tog { width:100px; height:54px; border-radius:27px; background:#3A2F4A; padding:6px; } .tog i { display:block; width:42px; height:42px; border-radius:50%; background:#fff; }
      .scan { --scan:0; position:relative; display:flex; flex-direction:column; gap:12px; }
      .scan::after { content:""; position:absolute; left:0; right:0; top:calc(var(--scan) * 100%); height:6px; background:var(--acc); }
      .comp { padding:14px 22px; border-radius:14px; background:rgba(255,255,255,.05); } .comp b { display:block; font-size:32px; } .comp i { font-style:normal; font-size:24px; color:var(--dim); }
      .doc h4 { font-size:44px; font-weight:900; line-height:1.15; margin-bottom:18px; }
      .ln { height:22px; border-radius:11px; background:rgba(255,255,255,.18); margin:16px 0; transform-origin:left center; } .ln.s { width:62%; }
      .seorow { display:flex; gap:16px; flex-wrap:wrap; }
      .player { position:relative; height:400px; border-radius:22px; overflow:hidden; }
      .pbg { position:absolute; inset:0; background:linear-gradient(135deg,#8B2FE8,#2A0F4D 60%,#040206); }
      .play { position:absolute; left:50%; top:50%; width:140px; height:140px; margin:-70px 0 0 -70px; border-radius:50%; background:rgba(255,255,255,.9); color:#8B2FE8; font-size:64px; display:flex; align-items:center; justify-content:center; padding-left:12px; }
      .pbar { position:absolute; left:30px; right:30px; bottom:26px; height:12px; border-radius:6px; background:rgba(255,255,255,.25); } .pbar i { display:block; height:100%; background:#fff; border-radius:6px; transform-origin:left center; }
      .frames { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; } .frames b { height:110px; border-radius:14px; background:linear-gradient(135deg,#3A1F5E,#120C1A); border:2px solid rgba(166,92,255,.4); display:block; }
      .queue { display:flex; flex-direction:column; gap:16px; }
      .qi { display:flex; align-items:center; gap:24px; padding:22px 26px; border-radius:18px; background:rgba(255,255,255,.05); font-size:36px; }
      .qi b { color:var(--acc); width:90px; } .qi span { flex:1; font-weight:700; } .qi i { font-style:normal; font-size:28px; color:#7CE38B; font-weight:800; }
      .gtm { position:absolute; left:34px; right:34px; top:96px; }
      .gh { font-size:42px; font-weight:900; color:var(--acc); letter-spacing:.06em; margin-bottom:22px; }
      .tiles { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
      .tile { padding:20px 22px; border-radius:20px; background:rgba(139,47,232,.18); border:2px solid rgba(166,92,255,.5); display:flex; flex-direction:column; gap:6px; }
      .tile span { font-size:44px; } .tile b { font-size:32px; } .tile i { font-style:normal; font-size:26px; color:#7CE38B; font-weight:800; }
      #h .wbody { min-height:560px; position:relative; }
      #i .stage { gap:30px; }
      #i .huge { font-size:240px; margin-top:0; }
      .cmt { width:1100px; } .dm { font-size:54px; text-align:center; }
      /* ---- Meta Ads Creative Studio visuals ---- */
      .newcard { position:relative; width:640px; padding:56px 56px 50px; border-radius:36px; background:linear-gradient(150deg,#22103A,#0E0A14 60%); border:3px solid var(--pur2); display:flex; flex-direction:column; gap:14px; }
      .newcard em { position:absolute; right:34px; top:30px; font-style:normal; font-size:30px; font-weight:900; padding:8px 20px; border-radius:999px; background:var(--red); }
      .newcard b { font-size:44px; font-weight:900; color:var(--acc); } .newcard span { font-size:72px; font-weight:900; line-height:1.02; } .newcard i { font-style:normal; font-size:32px; color:var(--dim); font-weight:700; }
      .bars { display:flex; align-items:flex-end; gap:18px; height:160px; margin-top:24px; } .bars i { display:block; width:56px; border-radius:12px 12px 4px 4px; background:linear-gradient(180deg,var(--pur2),var(--pur)); transform-origin:bottom center; } .bars span { font-size:80px; margin-left:16px; }
      .pipe { display:flex; align-items:center; gap:22px; margin-top:40px; }
      .pnode { width:300px; padding:30px 20px; border-radius:28px; background:#0E0A14; border:3px solid rgba(166,92,255,.6); display:flex; flex-direction:column; align-items:center; gap:10px; font-size:40px; font-weight:900; } .pnode span { font-size:76px; }
      .parr { font-size:56px; color:var(--acc); font-weight:900; } .parr.big { font-size:90px; }
      .thumb { flex:none; width:96px; height:96px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:48px; }
      .thumb.t1 { background:linear-gradient(135deg,#8B2FE8,#3A1275); } .thumb.t2 { background:linear-gradient(135deg,#C060FF,#5B1E9E); } .thumb.t3 { background:linear-gradient(135deg,#5B3A8F,#1C1030); } .thumb.t4 { background:linear-gradient(135deg,#A65CFF,#2A0F4D); }
      .adrow { position:relative; display:flex; align-items:center; gap:20px; padding:14px 18px; border-radius:18px; background:rgba(255,255,255,.05); border:2px solid rgba(166,92,255,.25); }
      .adrow b { display:block; font-size:30px; } .adrow i { font-style:normal; font-size:22px; color:var(--dim); font-weight:700; }
      .adrow.sel { border-color:var(--pur2); background:rgba(139,47,232,.15); }
      .met { margin-left:auto; font-style:normal; font-size:30px; font-weight:900; color:#7CE38B; } .met.low { color:#FF8A8A; }
      .toptag { position:absolute; right:14px; top:-18px; padding:6px 16px; border-radius:999px; background:#F5C542; color:#3A2600; font-size:22px; font-weight:900; }
      .bench { display:flex; flex-direction:column; gap:12px; padding:16px 20px; border-radius:18px; border:2px dashed rgba(166,92,255,.45); }
      .brow { display:flex; align-items:center; gap:18px; } .brow span { width:300px; font-size:24px; font-weight:800; color:var(--dim); }
      .bbar { flex:1; height:22px; border-radius:11px; background:rgba(255,255,255,.08); } .bbar i { display:block; height:100%; border-radius:11px; background:var(--dim); transform-origin:left center; } .bbar.top i { background:linear-gradient(90deg,var(--pur),var(--acc)); }
      .gen span { font-size:30px; font-weight:800; color:var(--acc); } .gbar { margin-top:12px; height:14px; border-radius:7px; background:rgba(255,255,255,.08); } .gbar i { display:block; height:100%; border-radius:7px; background:linear-gradient(90deg,var(--pur),var(--acc)); transform-origin:left center; }
      .concepts { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }
      .ccard { display:flex; flex-direction:column; gap:10px; padding:16px; border-radius:22px; background:#0E0A14; border:3px solid rgba(166,92,255,.5); }
      .ccard .thumb { width:100%; height:170px; font-size:80px; } .ccard b { font-size:28px; } .ccard i { font-style:normal; font-size:22px; color:var(--dim); font-weight:700; }
      .acts { display:flex; gap:16px; } .actb { padding:14px 24px; border-radius:16px; border:2px solid rgba(255,255,255,.18); font-size:28px; font-weight:800; color:var(--dim); }
      .abbtn { position:relative; align-self:flex-start; padding:18px 34px; border-radius:18px; background:var(--pur); font-size:32px; font-weight:900; }
      .chart { position:relative; height:200px; border-radius:18px; background:rgba(255,255,255,.04); border:2px solid rgba(166,92,255,.25); overflow:hidden; }
      .chart svg { position:absolute; inset:14px; width:calc(100% - 28px); height:calc(100% - 28px); } .chart path { fill:none; stroke:var(--acc); stroke-width:8; stroke-linecap:round; }
      .vv { position:absolute; left:20px; top:14px; font-size:24px; font-weight:900; color:var(--acc); }
      .approve { display:flex; align-items:center; gap:30px; padding:34px 44px; border-radius:30px; background:#0E0A14; border:3px solid rgba(166,92,255,.6); margin-top:20px; }
      .approve .lock { font-size:90px; } .approve b { display:block; font-size:44px; } .approve i { font-style:normal; font-size:30px; color:var(--dim); font-weight:700; }
      .apbtn { margin-left:30px; padding:20px 34px; border-radius:18px; background:#0B2A16; border:3px solid #3DDC84; color:#7CE38B; font-size:34px; font-weight:900; }
      .scale { display:flex; align-items:center; gap:40px; margin-top:30px; }
      .ccard.win1 { width:400px; border-color:#F5C542; } .ccard.win1 .thumb { height:240px; } .ccard.win1 b { font-size:36px; } .ccard.win1 i { color:#F5C542; font-size:26px; }
      .vars { display:flex; gap:22px; } .ccard.sm2 { width:280px; } .ccard.sm2 .thumb { height:150px; }
      .loop { position:relative; width:760px; height:560px; margin-top:10px; }
      .lring { position:absolute; left:50%; top:50%; width:420px; height:420px; margin:-210px 0 0 -210px; border-radius:50%; border:6px dashed rgba(181,123,255,.7); }
      .lnode { position:absolute; width:220px; padding:18px; border-radius:22px; background:#0E0A14; border:3px solid var(--pur2); display:flex; flex-direction:column; align-items:center; gap:4px; font-size:30px; font-weight:900; } .lnode span { font-size:52px; }
      .lnode.l0 { left:270px; top:-10px; } .lnode.l1 { right:-10px; top:200px; } .lnode.l2 { left:270px; bottom:-30px; } .lnode.l3 { left:-10px; top:200px; }
      .lcore { position:absolute; left:50%; top:50%; width:240px; margin-left:-120px; margin-top:-56px; text-align:center; font-size:40px; font-weight:900; color:var(--acc); line-height:1.15; } .lcore i { font-style:normal; font-size:24px; color:var(--dim); }
      .rollout { position:absolute; right:110px; top:780px; padding:20px 36px; border-radius:999px; background:linear-gradient(90deg,var(--pur),var(--pur2)); font-size:40px; font-weight:900; }
      #d1 .huge { font-size:220px; }
      #e .wbody { gap:18px; }
      /* ---- Jaal aur Paani visuals ---- */
      .rcol { position:relative; width:860px; display:flex; flex-direction:column; align-items:center; gap:30px; }
      .rcol.abs { position:absolute; left:960px; top:200px; }
      .site-spacer { width:820px; height:470px; }
      .siteabs { position:absolute; left:980px; top:200px; }
      .site-vid { position:relative; display:block; width:100%; aspect-ratio:1280/616; object-fit:cover; background:#080618; }
      .site { width:820px; border-radius:26px; background:#0E0A14; border:3px solid rgba(166,92,255,.55); overflow:hidden; }
      .site-body { padding:26px 32px 32px; display:flex; flex-direction:column; gap:24px; background:linear-gradient(160deg,#1B0F2B,#0B0710); }
      .site-nav { display:flex; gap:30px; align-items:center; font-size:24px; color:var(--dim); font-weight:700; } .site-nav b { color:#fff; font-size:28px; margin-right:auto; }
      .site-hero { display:flex; flex-direction:column; gap:6px; padding:20px 0; } .site-hero b { font-size:58px; font-weight:900; line-height:1.05; } .site-hero .acc2 { color:var(--acc); }
      .site-btn { align-self:flex-start; margin-top:18px; padding:16px 30px; border-radius:14px; background:var(--pur); font-size:28px; font-weight:900; }
      .site-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; } .site-grid i { height:120px; border-radius:16px; background:linear-gradient(135deg,#3A1F5E,#160D22); border:2px solid rgba(166,92,255,.3); }
      .visitors { padding:18px 34px; border-radius:999px; background:#0E0A14; border:3px solid rgba(255,61,61,.7); font-size:38px; font-weight:800; } .visitors b { color:var(--red); font-size:46px; }
      #d-wait { border-color:rgba(166,92,255,.6); color:var(--dim); }
      .net { width:460px; height:504px; overflow:visible; }
      .net .nh { stroke:#E9DDFF; stroke-width:14; stroke-linecap:round; fill:none; }
      .net .nbo { stroke:var(--acc); stroke-width:5; fill:none; }
      .net .nr { stroke:var(--acc); stroke-width:10; fill:none; }
      .net.dry .nh, .net.dry .nr, .net.dry .nbo { stroke:#6E6478; } .net.dry .nb { opacity:.35; }
      .net.mini { width:150px; height:164px; }
      #d2-net { position:absolute; right:90px; top:110px; width:300px; height:328px; }
      #b2-water { height:250px; }
      .spark { padding:14px 28px; border-radius:999px; background:var(--pur); font-size:32px; font-weight:900; }
      .water { position:absolute; left:0; right:0; bottom:0; height:400px; background:linear-gradient(180deg,#7B2FE0 0%,#3A1275 45%,#12051F 100%); z-index:-1; }
      .water svg { position:absolute; left:0; top:-78px; width:2400px; height:80px; } .water svg path { fill:#7B2FE8; }
      .cards3 { display:grid; grid-template-columns:repeat(3,1fr); gap:30px; width:1580px; margin-top:30px; }
      .card3 { position:relative; display:flex; flex-direction:column; gap:10px; padding:34px 34px 30px; border-radius:28px; background:#0E0A14; border:3px solid rgba(255,255,255,.14); }
      .card3 span { font-size:72px; } .card3 b { font-size:54px; font-weight:900; } .card3 i { font-style:normal; font-size:32px; color:var(--dim); font-weight:600; }
      .card3 em { position:absolute; right:26px; top:30px; font-style:normal; font-size:26px; font-weight:900; padding:8px 16px; border-radius:10px; background:rgba(139,47,232,.25); color:var(--acc); letter-spacing:.08em; }
      .dry .wi { color:#B9AFC4; } .huge.dry { font-size:300px; letter-spacing:-.02em; }
      .dryfx { position:absolute; inset:0; background:radial-gradient(ellipse at center,#2A2230 0%,#17121B 70%); z-index:-1; }
      .dryfx svg { position:absolute; inset:0; width:100%; height:100%; } .dryfx path { stroke:#4A3F52; stroke-width:6; fill:none; stroke-linecap:round; }
      .flow { display:flex; align-items:center; gap:26px; width:860px; justify-content:flex-end; }
      .adcard { width:260px; padding:16px; border-radius:22px; background:#0E0A14; border:3px solid rgba(166,92,255,.55); display:flex; flex-direction:column; gap:8px; }
      .ad-th { height:150px; border-radius:14px; background:linear-gradient(135deg,#8B2FE8,#2A0F4D); display:flex; align-items:center; justify-content:center; font-size:70px; }
      .adcard b { font-size:26px; } .adcard i { font-style:normal; font-size:20px; color:var(--dim); }
      .arrow { font-size:70px; color:var(--acc); font-weight:900; }
      .phone { position:relative; width:420px; height:760px; border-radius:56px; background:#0E0A14; border:6px solid #3A2F4A; padding:70px 26px 26px; display:flex; flex-direction:column; gap:20px; }
      .ph-notch { position:absolute; left:50%; top:18px; width:140px; height:30px; margin-left:-70px; border-radius:15px; background:#000; }
      .ph-hero { height:170px; border-radius:22px; background:linear-gradient(135deg,#8B2FE8,#2A0F4D); display:flex; align-items:flex-end; padding:18px; font-size:32px; font-weight:900; }
      .prow { display:flex; flex-direction:column; gap:4px; padding:16px 20px; border-radius:16px; background:rgba(255,255,255,.06); border:2px solid rgba(166,92,255,.3); }
      .prow span { font-size:22px; color:var(--dim); font-weight:700; } .prow b { font-size:32px; }
      .pbtn { position:relative; padding:22px; border-radius:18px; background:var(--pur); text-align:center; font-size:34px; font-weight:900; }
      .tap { position:absolute; left:50%; top:50%; width:90px; height:90px; margin:-45px 0 0 -45px; border-radius:50%; border:6px solid #fff; opacity:0; }
      .won { align-self:center; padding:14px 26px; border-radius:999px; background:#0B2A16; border:3px solid #3DDC84; color:#7CE38B; font-size:30px; font-weight:900; }
      .pair { display:flex; align-items:center; gap:40px; margin-top:30px; }
      .ptile { position:relative; width:340px; height:280px; border-radius:30px; background:#0E0A14; border:3px solid rgba(166,92,255,.55); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; }
      .ptile span { font-size:100px; } .ptile b { font-size:44px; font-weight:900; letter-spacing:.06em; }
      .pair.small .ptile { width:300px; height:250px; }
      .plus2 { font-size:110px; font-weight:900; color:var(--acc); }
      .xbad { position:absolute; bottom:-26px; left:50%; transform:translateX(-50%); white-space:nowrap; font-style:normal; padding:10px 22px; border-radius:999px; background:#2A0B0B; border:3px solid var(--red); color:#FF8A8A; font-size:28px; font-weight:900; }
      .coins { position:absolute; left:560px; top:430px; display:flex; gap:40px; } .coins b { display:flex; align-items:center; justify-content:center; width:80px; height:80px; border-radius:50%; background:#F5C542; color:#5A3A00; font-size:46px; font-weight:900; border:5px solid #C99A1E; }
      .dmpill { margin-top:20px; padding:22px 50px; border-radius:999px; background:linear-gradient(90deg,var(--pur),var(--pur2)); font-size:52px; font-weight:900; }
      #g .stage { gap:50px; }
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
      <div class="wash"></div>
      <div class="dots-bg dl"></div><div class="dots-bg dr"></div>
      <div class="stripe" id="bg-stripe"></div>
      <div class="shp sh-c" id="sh0"></div><div class="shp sh-s" id="sh1"></div><div class="shp sh-p" id="sh2"></div>
      <div class="shp sh-c2" id="sh3"></div><div class="shp sh-t" id="sh4"></div><div class="shp sh-p2" id="sh5"></div>
      <div class="bg-ring" id="bg-ring1"></div>
      <div class="bg-ring" id="bg-ring2"></div>
      <div class="vignette"></div>

      <div class="hook-ui clip" id="hook-ui" data-start="0" data-duration="${CUT.b1}" data-track-index="4">
        <div id="hook-tag">🆕 META ADS UPDATE</div>
      </div>

      ${sceneHtml}


      <div id="wipe" class="clip" data-start="0" data-duration="${DUR}" data-track-index="6"><div class="wp"></div></div>
      <div id="brand" class="clip" data-start="0" data-duration="${CUT.out}" data-track-index="8"><div class="bi"><img src="brand/logo-mark.png" alt="GX" /><span>THE GROWTH<b>X</b> STUDIO</span></div></div>
      <div id="progress" class="clip" data-start="0" data-duration="${DUR}" data-track-index="9"><i></i></div>

      <audio id="vo" src="assets/voiceover.wav" data-start="0" data-duration="${VOEND.toFixed(2)}" data-track-index="12" data-volume="1"></audio>
      <audio id="music" src="assets/music.wav" data-start="0" data-duration="${DUR}" data-track-index="10" data-volume="0.4"></audio>
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
