// Run: node build.cjs  (regenerates index.html; edit word timings in the scenes list)
// Generates growthx-steal-audience-16x9/index.html (static clips, one paused GSAP timeline).
const fs = require("fs");
const out = process.argv[2] || require("path").join(__dirname, "index.html");
const DUR = 39.2;
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

const P1 = seg(0.02, 0.4, [["Bhai,", "md"]]);
const P2 = seg(0.61, 2.31, [["META", "xl acc"], ["ADS", "xl acc"], ["mein", "md"], ["yeh", "md"], ["bhi", "md"], ["ho", "md"], ["sakta", "md"], ["hai?", "md"]]);
const P3 = seg(2.69, 3.81, [["mujhe", "md"], ["aaj", "md"], ["hi", "md"], ["pata", "lg hl"], ["chala!", "lg hl"]]);
const P4 = seg(4.4, 5.27, wl("Audiences mein jao,"));
const P5 = seg(5.59, 6.92, wl("Create Audience pe click karo,"));
const P67 = [...seg(7.21, 7.33, wl("aur")), ...seg(7.48, 8.71, wl("Custom Audience select karo."))];
const P8 = seg(9.22, 11.43, wl("Source mein apna Instagram account choose karo,"));
const P10 = [...seg(11.67, 11.82, wl("aur")), ...seg(11.98, 14.61, wl("“everyone who engaged with your profile” select karo."))];
const P11 = seg(15.07, 17.02, wl("Ab isi audience se Lookalike banao,"));
const P1213 = [...seg(17.36, 17.72, wl("India,")), ...seg(18.04, 18.61, wl("1 percent."))];
const P14 = seg(19.05, 22.46, wl("Aur detailed targeting mein apne competitor ka brand naam search karo,"));
const P1516 = [...seg(22.81, 23.79, wl("agar interest mein dikhe")), ...seg(23.98, 24.55, wl("toh add kar do."))];
const P17 = seg(24.92, 25.42, [["BAS!", "huge acc"]]);
const P18 = seg(25.77, 30.73, [["Ab", "md"], ["tumhare", "md"], ["ads", "md"], ["seedha", "md"], ["UN", "lg hl"], ["LOGON", "lg hl"], ["tak", "md"], ["jayenge", "md"], ["jo", "md"], ["tumhare", "md"], ["COMPETITOR", "lg acc"], ["jaise", "md"], ["brands", "md"], ["PASAND", "lg acc"], ["karte", "md"], ["hain", "md"]]);
const P19 = seg(31.15, 32.15, [["Kya", "lg"], ["mast", "xl acc"], ["trick", "xl acc"], ["hai", "lg"], ["na?", "lg"]]);
const P20 = seg(32.63, 33.58, [["Comment", "lg"], ["karo", "lg"], ["“STEAL”", "huge acc"]]);
const P21 = [...seg(33.81, 33.93, [["aur"]]), ...seg(34.05, 36.33, [["poora"], ["step-by-step"], ["guide"], ["main"], ["tumhe"], ["DM"], ["kar"], ["dunga"]])].map((x) => x.t);

const CUT = { s1: 0, s2: 4.1, s3: 9.0, s4: 14.85, s5: 18.85, s6: 25.6, s7: 30.95, s8: 32.42, out: 36.45 };
const at = (ws, i) => ws[i].t;

const capA = capBar([P4, P5, P67]);
const capB = capBar([P8, P10]);
const capC = capBar([P11, P1213]);
const capD = capBar([P14, P1516]);

const scenes = [
  { id: "s1", start: CUT.s1, end: CUT.s2, lines: [P1, P2.slice(0, 2), P2.slice(2), P3], shake: P2[0].t + 0.05 },

  { id: "s2", start: CUT.s2, end: CUT.s3, noDrift: true, lines: [], extra: `
      <div class="app" id="s2-app">
        <div class="side"><div class="logo-s">Ads Manager</div><div class="si">Campaigns</div><div class="si">Ad sets</div><div class="si" id="s2-aud">👥 Audiences</div><div class="si">Billing</div></div>
        <div class="main">
          <div class="mh"><span class="mt">Audiences</span><div class="btn" id="s2-create">+ Create audience</div></div>
          <div class="rows"><i></i><i></i><i></i><i></i></div>
          <div class="menu" id="s2-menu"><div class="mi" id="s2-m0">⚙️ Custom audience</div><div class="mi">👥 Lookalike audience</div><div class="mi">💾 Saved audience</div></div>
        </div>
      </div>
      <div class="cursor2" id="s2-cur"></div>${capA.html}`,
    tweens: (A) => {
      capA.tweens();
      T(`tl.fromTo("#s2-app",{opacity:0,y:60,scale:.94},{opacity:1,y:0,scale:1,duration:.45,ease:"power3.out"},${CUT.s2});`);
      T(`tl.set("#s2-cur",{x:1100,y:700},${CUT.s2});`);
      curTo("s2-cur", 300, 315, at(P4, 0) - 0.1); click("s2-cur", "#s2-aud", at(P4, 0) + 0.35); on("#s2-aud", at(P4, 0) + 0.38);
      curTo("s2-cur", 1520, 160, at(P5, 0) - 0.05); click("s2-cur", "#s2-create", at(P5, 3)); on("#s2-create", at(P5, 3) + 0.03, "#B57BFF", "#040206");
      T(`tl.fromTo("#s2-menu",{opacity:0,y:-20},{opacity:1,y:0,duration:.25,ease:"power2.out"},${(at(P5, 3) + 0.12).toFixed(2)});`); S(at(P5, 3) + 0.12, "pop", .45);
      curTo("s2-cur", 1450, 262, at(P67, 1) - 0.05); click("s2-cur", "#s2-m0", at(P67, 3)); on("#s2-m0", at(P67, 3) + 0.03);
    } },

  { id: "s3", start: CUT.s3, end: CUT.s4, noDrift: true, lines: [], extra: `
      <div class="app" id="s3-app">
        <div class="mh full"><span class="mt">Create a custom audience</span><span class="step">STEP 1 · SOURCE</span></div>
        <div class="grid" id="s3-grid">
          <div class="src">🌐 Website</div><div class="src">📋 Customer list</div>
          <div class="src">📱 App activity</div><div class="src" id="s3-ig"><b>📸 Instagram account</b><span>Meta source</span></div>
        </div>
        <div class="evs" id="s3-evs">
          <div class="ev" id="s3-e0"><span class="box" id="s3-x0"></span>Everyone who engaged with your profile</div>
          <div class="ev"><span class="box"></span>Anyone who visited your profile</div>
          <div class="ev"><span class="box"></span>People who sent a message to your account</div>
          <div class="ev"><span class="box"></span>People who saved any post or ad</div>
        </div>
      </div>
      <div class="cursor2" id="s3-cur"></div>${capB.html}`,
    tweens: (A) => {
      capB.tweens();
      T(`tl.fromTo("#s3-app",{opacity:0,y:60},{opacity:1,y:0,duration:.4,ease:"power3.out"},${CUT.s3});`);
      T(`tl.fromTo("#s3-grid .src",{opacity:0,scale:.9},{opacity:1,scale:1,duration:.3,ease:"back.out(2)",stagger:.08},${(CUT.s3 + 0.15).toFixed(2)});`);
      T(`tl.set("#s3-cur",{x:700,y:900},${CUT.s3});`);
      curTo("s3-cur", 1320, 590, at(P8, 3) - 0.35); click("s3-cur", "#s3-ig", at(P8, 3)); on("#s3-ig", at(P8, 3) + 0.03);
      T(`tl.to("#s3-grid",{opacity:0,y:-30,duration:.25},${(at(P10, 0) - 0.15).toFixed(2)});`);
      T(`tl.fromTo("#s3-evs .ev",{opacity:0,x:60},{opacity:1,x:0,duration:.3,ease:"power3.out",stagger:.07},${at(P10, 0).toFixed(2)});`);
      curTo("s3-cur", 340, 285, at(P10, 2)); const sel = at(P10, P10.length - 2);
      click("s3-cur", "#s3-e0", sel); on("#s3-e0", sel + 0.03); T(`tl.fromTo("#s3-x0",{"--ck":0},{"--ck":1,duration:.15},${(sel + 0.03).toFixed(2)});`); S(sel + 0.06, "ding", .45);
    } },

  { id: "s4", start: CUT.s4, end: CUT.s5, noDrift: true, lines: [], extra: `
      <div class="card" id="s4-card">
        <div class="ch">Create a lookalike audience</div>
        <div class="row"><span class="k">Source</span><span class="v">📸 IG profile engagers</span></div>
        <div class="row"><span class="k">Location</span><span class="pill2" id="s4-in">🇮🇳 India</span></div>
        <div class="row col"><span class="k">Audience size</span>
          <div class="slider"><div class="track"><i id="s4-fill"></i></div><div class="knob" id="s4-knob"></div></div>
          <div class="ticks"><span>1%</span><span>5%</span><span>10%</span></div>
        </div>
      </div>
      <div class="big1" id="s4-big">1%</div>${capC.html}`,
    tweens: (A) => {
      capC.tweens();
      T(`tl.fromTo("#s4-card",{opacity:0,y:60},{opacity:1,y:0,duration:.4,ease:"power3.out"},${CUT.s4});`);
      T(`tl.fromTo("#s4-knob",{x:900},{x:900,duration:.01},${CUT.s4});`);
      A.pop("#s4-in", at(P1213, 0)); 
      T(`tl.to("#s4-knob",{x:0,duration:.45,ease:"power3.inOut"},${at(P1213, 1).toFixed(2)});`);
      T(`tl.fromTo("#s4-fill",{scaleX:1},{scaleX:0.02,duration:.45,ease:"power3.inOut",immediateRender:false},${at(P1213, 1).toFixed(2)});`);
      T(`tl.fromTo("#s4-big",{opacity:0,scale:1.6},{opacity:1,scale:1,duration:.35,ease:"back.out(2)"},${(at(P1213, 1) + 0.35).toFixed(2)});`); S(at(P1213, 1) + 0.35, "impact_lite", .55);
    } },

  { id: "s5", start: CUT.s5, end: CUT.s6, noDrift: true, lines: [], extra: `
      <div class="card wide" id="s5-card">
        <div class="ch">Detailed targeting</div>
        <div class="search"><span class="mag">🔍</span><span class="typed">${"Your competitor".split("").map((c, i) => `<b id="s5-c${i}">${c === " " ? "&nbsp;" : c}</b>`).join("")}</span><span class="caret" id="s5-caret"></span></div>
        <div class="res" id="s5-res">
          <div class="ri"><div><b>Your Competitor</b><span>Interest · Shopping and fashion</span></div><div class="add" id="s5-add">+ Add</div></div>
          <div class="ri dim"><div><b>Your Competitor Store</b><span>Interest · Business</span></div><div class="add">+ Add</div></div>
        </div>
        <div class="selrow" id="s5-sel"><span class="k">Included</span><span class="chip3" id="s5-chip">Your Competitor ✕</span></div>
      </div>
      <div class="cursor2" id="s5-cur"></div>
      <div class="stamp" id="s5-bas">${P17[0].text}</div>${capD.html}`,
    tweens: (A) => {
      capD.tweens();
      T(`tl.fromTo("#s5-card",{opacity:0,y:60},{opacity:1,y:0,duration:.4,ease:"power3.out"},${CUT.s5});`);
      const t0 = at(P14, 9);
      "Your competitor".split("").forEach((c, i) => { const t = +(t0 + i * 0.07).toFixed(2); if (i % 2 === 0) S(t, "tick", .35); T(`tl.fromTo("#s5-c${i}",{opacity:0},{opacity:1,duration:.02},${t});`); });
      T(`tl.fromTo("#s5-res .ri",{opacity:0,y:-15},{opacity:1,y:0,duration:.25,stagger:.08},${(t0 + 1.15).toFixed(2)});`);
      T(`tl.set("#s5-cur",{x:1200,y:950},${CUT.s5});`);
      curTo("s5-cur", 1500, 432, at(P1516, 2)); const addT = at(P1516, 5);
      click("s5-cur", "#s5-add", addT); on("#s5-add", addT + 0.03);
      A.pop("#s5-chip", addT + 0.12); S(addT + 0.12, "ding", .45);
      T(`tl.fromTo("#s5-bas",{opacity:0,scale:2.2,rotation:-12},{opacity:1,scale:1,rotation:-8,duration:.3,ease:"back.out(2.4)"},${P17[0].t});`); S(P17[0].t, "impact", .8);
    } },

  { id: "s6", start: CUT.s6, end: CUT.s7, lines: [P18.slice(0, 4), P18.slice(4, 8), P18.slice(8, 12), P18.slice(12)], extra: `
      <div class="crowd" id="s6-crowd">${Array.from({ length: 18 }, (_, i) => `<b class="pp" id="s6-p${i}">👤</b>`).join("")}</div>`,
    tweens: (A) => { T(`tl.fromTo("#s6-crowd .pp",{opacity:0,scale:0,y:40},{opacity:1,scale:1,y:0,duration:.3,ease:"back.out(2)",stagger:.05},${at(P18, 4).toFixed(2)});`); } },

  { id: "s7", start: CUT.s7, end: CUT.s8, lines: [P19.slice(0, 1), P19.slice(1, 3), P19.slice(3)], shake: P19[1].t + 0.05 },

  { id: "s8", start: CUT.s8, end: CUT.out, lines: [P20.slice(0, 2), P20.slice(2)], shake: P20[2].t + 0.05, extra: `
      <div class="cmt" id="s8-cmt">
        <div class="cmt-av"><img src="brand/logo-mark.png" alt="" /></div>
        <div class="cmt-in"><span class="cmt-ph">Add a comment…</span><span class="cmt-txt">${["S", "T", "E", "A", "L"].map((c, i) => `<b id="s8-k${i}">${c}</b>`).join("")}</span></div>
        <div class="cmt-send" id="s8-send">Post</div>
      </div>
      <div class="dm">${["aur", "poora", "step-by-step", "guide", "main", "tumhe", "DM", "kar dunga 📩"].map((x, i) => `<span class="w-inline${x === "DM" || x === "step-by-step" ? " dmk" : ""}" id="s8-d${i}">${x}</span>`).join(" ")}</div>`,
    tweens: (A) => {
      const c0 = P20[2].t + 0.3;
      A.pop("#s8-cmt", +(c0 - 0.05).toFixed(2), 0.35);
      T(`tl.fromTo("#s8-cmt .cmt-ph",{opacity:1},{opacity:0,duration:.05,immediateRender:false},${(c0 + 0.2).toFixed(2)});`);
      [0, 1, 2, 3, 4].forEach((i) => { const t = +(c0 + 0.25 + i * 0.07).toFixed(2); S(t, "tick", .5); T(`tl.fromTo("#s8-k${i}",{opacity:0,scale:.4},{opacity:1,scale:1,duration:.12,ease:"back.out(3)"},${t});`); });
      const post = P21[1];
      S(post, "click", .9); S(post + 0.06, "ding", .55);
      T(`tl.to("#s8-send",{scale:.88,duration:.07,yoyo:true,repeat:1},${post});`);
      T(`tl.to("#s8-send",{backgroundColor:"#8B2FE8",color:"#FFFFFF",duration:.1},${(post + 0.06).toFixed(2)});`);
      [P21[0], P21[1], P21[2], P21[3], P21[4], P21[5], P21[6], P21[7]].forEach((t, i) => T(`tl.fromTo("#s8-d${i}",{opacity:0,y:30},{opacity:1,y:0,duration:.22,ease:"back.out(2)"},${t});`));
    } },

  { id: "out", start: CUT.out, end: DUR, lines: [], noDrift: true, extra: `
      <div class="outro">
        <div class="logo-wrap" id="out-logo"><div class="logo-ring" id="out-ring"></div><img class="logo-big" src="brand/logo.png" alt="The GrowthX Studio" /></div>
        <div class="outro-r">
          <div class="pill" id="out-pill">COMMENT “STEAL” 💬</div>
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

const wipes = [CUT.s2, CUT.s3, CUT.s4, CUT.s5, CUT.s6, CUT.s7, CUT.s8, CUT.out];

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
    <title>GrowthX Steal Audience</title>
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

      <div class="hook-ui clip" id="hook-ui" data-start="0" data-duration="${CUT.s2}" data-track-index="4">
        <div id="hook-tag">🔥 META ADS HACK</div>
      </div>

      ${sceneHtml}


      <div id="wipe" class="clip" data-start="0" data-duration="${DUR}" data-track-index="6"><div class="wp"></div></div>
      <div id="brand" class="clip" data-start="0" data-duration="${CUT.out}" data-track-index="8"><div class="bi"><img src="brand/logo-mark.png" alt="GX" /><span>THE GROWTH<b>X</b> STUDIO</span></div></div>
      <div id="progress" class="clip" data-start="0" data-duration="${DUR}" data-track-index="9"><i></i></div>

      <audio id="vo" src="assets/voiceover.m4a" data-start="0" data-duration="36.52" data-track-index="12" data-volume="1"></audio>
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
