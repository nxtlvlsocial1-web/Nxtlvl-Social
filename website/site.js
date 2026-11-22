// Nxtlvl Social: menu, staggered entrances, the live WhatsApp demo, the "build your month" planner and the booking form.
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // mobile menu
  var burger = $('.burger'), mob = $('#mob');
  if (burger && mob) burger.addEventListener('click', function () {
    var open = mob.hasAttribute('hidden');
    if (open) mob.removeAttribute('hidden'); else mob.setAttribute('hidden', '');
    burger.setAttribute('aria-expanded', String(open));
  });

  // entrances: the parts of each section rise in turn (heading, text, then the pictures)
  var groups = {};
  $$('[data-rise]').forEach(function (el) {
    var host = el.closest('[data-sec]') || document.body, key = host.dataset.secId || (host.dataset.secId = Math.random().toString(36).slice(2));
    groups[key] = (groups[key] || 0) + 1;
    el.style.setProperty('--d', Math.min(groups[key] - 1, 6) * 0.08 + 's');
  });
  var rise = $$('[data-rise]');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
    rise.forEach(function (el) { io.observe(el); });
  } else rise.forEach(function (el) { el.classList.add('in'); });

  // live clock in India time
  var clock = $('[data-ist]');
  var tick = function () {
    if (!clock) return;
    try { clock.textContent = new Date().toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit', timeZone: 'Asia/Kolkata' }).toLowerCase() + ' IST'; } catch (e) { /* old browsers keep the static text */ }
  };
  tick(); setInterval(tick, 15000);

  // the WhatsApp booking plays out, then starts again
  var chat = $('.chat');
  if (chat && !reduce) {
    var steps = $$('[data-step]', chat), typing = $('.typing', chat), stamp = $$('[data-time]', chat);
    var now = function () { try { return new Date().toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit', timeZone: 'Asia/Kolkata' }).toLowerCase(); } catch (e) { return ''; } };
    var run = function () {
      steps.forEach(function (s) { s.classList.remove('on'); });
      stamp.forEach(function (s) { s.textContent = now(); });
      var i = 0;
      var next = function () {
        if (i >= steps.length) { setTimeout(run, 6000); return; }
        var s = steps[i++], bot = s.classList.contains('out');
        if (bot && typing) { typing.classList.add('on'); chat.querySelector('.chat-body').appendChild(typing); }
        setTimeout(function () {
          if (typing) typing.classList.remove('on');
          s.classList.add('on'); chat.querySelector('.chat-body').appendChild(s);
          setTimeout(next, bot ? 1500 : 1100);
        }, bot ? 1100 : 500);
      };
      next();
    };
    var started = false;   // the whole conversation shows at rest; it replays once the visitor has had a look
    steps.forEach(function (s) { s.classList.add('on'); });
    var start = function () { if (!started) { started = true; setTimeout(run, 5000); } };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { start(); o.disconnect(); } }).observe(chat); else start();
  }

  // build your month
  var demo = $('#planner');
  if (demo) {
    var BIZ = {
      cafe: { name: 'café or restaurant', auto: ['Menu, timings and offers on DM', 'Table booking on WhatsApp'], shoot: 'Food and space shoot', lp: 'Order and reservation page' },
      clinic: { name: 'clinic', auto: ['Treatment and price questions', 'Appointment booking and reminders'], shoot: 'Clinic and team shoot', lp: 'Treatment landing page' },
      d2c: { name: 'D2C brand', auto: ['Order and delivery questions', 'Follow-ups for abandoned enquiries'], shoot: 'Product shoot', lp: 'Product launch page' },
      realestate: { name: 'real estate business', auto: ['Lead qualification: budget, area, timeline', 'Site-visit booking'], shoot: 'Property walkthrough shoot', lp: 'Project landing page' },
      education: { name: 'education business', auto: ['Admission and fee questions', 'Demo class booking'], shoot: 'Campus and faculty shoot', lp: 'Admissions landing page' },
      creator: { name: 'creator or personal brand', auto: ['Comment-to-DM links', 'Brand collab enquiry routing'], shoot: 'Content day shoot', lp: 'Link-in-bio page' },
    };
    var GOAL = { leads: { word: 'more leads', ad: 'Meta lead ads', g: 'Google Search ads for high-intent searches' }, sales: { word: 'more sales', ad: 'Meta sales campaigns with retargeting', g: 'Google Shopping and Search ads' },
      bookings: { word: 'more bookings', ad: 'Meta ads that open WhatsApp', g: 'Google Search ads with call and booking extensions' }, awareness: { word: 'brand awareness', ad: 'Meta reach and video-view campaigns', g: 'YouTube video ads' } };
    var form = $('form', demo), out = $('[data-plan]', demo);
    var val = function (n) { var el = form.elements[n]; return el && el.value; };
    var on = function (n) { var el = form.elements[n]; return !!(el && el.checked); };
    var render = function () {
      var b = BIZ[val('biz')] || BIZ.cafe, g = GOAL[val('goal')] || GOAL.leads, reels = +val('reels') || 8, shoot = +val('shoot') || 0;
      var ig = on('ch_ig'), wa = on('ch_wa'), meta = on('ch_meta'), goog = on('ch_google'), web = on('ch_web');
      var carousels = Math.max(4, Math.round(reels * 0.75)), stories = Math.max(4, Math.round(reels / 2));
      $('output[for="reels"]', demo).textContent = reels;
      var creative = [reels + ' reels with hooks, captions and covers', carousels + ' carousels and posts', stories + ' story sets'];
      if (shoot) creative.push(shoot + ' ' + (shoot > 1 ? 'shoot days: ' : 'shoot day: ') + b.shoot.toLowerCase());
      var marketing = []; if (ig) marketing.push('Instagram calendar, posting and replies'); if (meta) marketing.push(g.ad); if (goog) marketing.push(g.g); marketing.push('Monthly report on ' + g.word);
      var autos = []; if (ig || wa) autos = autos.concat(b.auto); autos.push('Every lead logged and sent to your WhatsApp');
      var webs = web ? [b.lp, 'Speed, SEO and AEO checks'] : [];
      var grp = function (t, list) { return list.length ? '<div class="group"><b>' + t + '</b><ul>' + list.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul></div>' : ''; };
      var total = reels + carousels + stories + shoot + Math.max(0, marketing.length - 1) + autos.length + webs.length;
      // calendar: reels and posts spread across four weeks, shoot days early in the month
      var cells = [], shootDays = [2, 15].slice(0, shoot);
      for (var d = 0; d < 28; d++) cells.push('');
      shootDays.forEach(function (d) { cells[d] = 'shoot'; });
      var free = []; for (var k = 0; k < 28; k++) if (!cells[k]) free.push(k);
      var slots = Math.min(free.length, reels + carousels);
      for (var p = 0; p < slots; p++) {   // exactly `reels` reels, spread evenly among the posts
        cells[free[Math.floor(p * free.length / slots)]] = Math.floor((p + 1) * reels / slots) > Math.floor(p * reels / slots) ? 'reel' : 'post';
      }
      out.innerHTML = '<div class="plan-head"><div><h3>Your month as a ' + b.name + '</h3><p>Planned for ' + g.word + '. AI drafts, your strategist approves.</p></div><span class="plan-count">' + total + ' deliverables</span></div>' +
        '<div class="cal" aria-hidden="true">' + cells.map(function (c, i) { return '<div class="' + c + '">' + (i + 1) + '</div>'; }).join('') + '</div>' +
        '<div class="legend"><span><i style="background:var(--violet)"></i>Reel</span><span><i style="background:rgba(169,92,255,.32)"></i>Post or carousel</span>' + (shoot ? '<span><i style="background:#fff"></i>Shoot day</span>' : '') + '</div>' +
        '<div class="groups">' + grp('Creative Studio', creative) + grp('AI Marketing', marketing) + grp('AI Automation', autos) + grp('Websites', webs) + '</div>';
      var summary = 'Business: ' + b.name + '. Goal: ' + g.word + '. ' + [ig && 'Instagram', wa && 'WhatsApp', meta && 'Meta ads', goog && 'Google ads', web && 'Website'].filter(Boolean).join(', ') + '. ' + reels + ' reels a month, ' + shoot + ' shoot day(s).';
      var cta = $('[data-plan-cta]', demo);
      if (cta) cta.href = '/contact?need=' + (meta || goog ? 'marketing' : (ig || wa) ? 'automation' : 'creative') + '&plan=' + encodeURIComponent(summary);
    };
    form.addEventListener('input', render); form.addEventListener('change', render);
    render();
  }

  // booking form: prefill from the planner or the closing email field, then send
  var params = new URLSearchParams(location.search);
  var bform = $('form.book');
  if (bform) {
    var need = params.get('need'), plan = params.get('plan'), em = params.get('email');
    if (need && bform.need.querySelector('option[value="' + need + '"]')) bform.need.value = need;
    if (plan) bform.message.value = 'I built this plan on your site and would like to discuss it: ' + plan.slice(0, 600);
    if (em) bform.email.value = em.slice(0, 120);
    var started2 = Date.now(), msg = $('.form-msg', bform);
    var show = function (text, ok) { msg.textContent = text; msg.className = 'form-msg ' + (ok ? 'ok' : 'err'); msg.hidden = false; };
    bform.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = $('button[type=submit]', bform);
      var data = { name: bform.name.value.trim(), business: bform.business.value.trim(), email: bform.email.value.trim(), need: bform.need.value, message: bform.message.value.trim(), website: bform.website.value, t: started2 };
      if (data.name.length < 2) { show('Please tell us your name.'); bform.name.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email)) { show('Please enter a valid email so we can reply.'); bform.email.focus(); return; }
      btn.disabled = true; var label = btn.textContent; btn.textContent = 'Sending…';
      fetch('/api/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res && res.ok) { bform.reset(); show('Thanks, ' + data.name.split(' ')[0] + '. We have your request and will reply by email within one business day.', true); }
          else show((res && res.error) || 'Something went wrong. Please email connect@nxtlvlsocial.ai instead.');
        })
        .catch(function () { show('Could not send right now. Please email connect@nxtlvlsocial.ai instead.'); })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  }
})();

// live product surfaces: agent feed, counters, typing, automation wires, the platform prompt
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var whenSeen = function (el, fn) {
    if (!el) return;
    if (!('IntersectionObserver' in window)) { fn(); return; }
    var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { o.disconnect(); fn(); } }, { threshold: 0.25 });
    o.observe(el);
  };
  var visible = true;
  document.addEventListener('visibilitychange', function () { visible = !document.hidden; });

  // count up numbers when they come into view
  var fmt = function (n, kind) { return kind === 'm' ? (n / 1e6).toFixed(1) + 'M' : Math.round(n).toLocaleString('en-IN'); };
  $$('[data-count]').forEach(function (el) {
    var target = +el.dataset.count, kind = el.dataset.fmt, final = el.textContent;
    if (reduce || !target) return;
    whenSeen(el, function () {
      var t0 = performance.now(), dur = 1600;
      var step = function (now) { var t = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - t, 4); el.textContent = t < 1 ? fmt(target * e, kind) : final; if (t < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    });
  });

  if (reduce) return;

  // agent activity feed
  var feed = $('[data-feed]');
  if (feed) {
    var icons = {}; $$('.row-f .av', feed).forEach(function (a, i) { icons[i] = a.innerHTML; });
    var items = [[3, 'Edit Agent', 'Captions synced on the menu reel'], [1, 'Reply Agent', 'Booked a table for 4 at 8 pm'], [0, 'Content Agent', 'Wrote 5 captions for next week'],
      [2, 'Ads Agent', 'Paused the weakest creative'], [4, 'Automation', 'Follow-up sent to Saturday leads'], [1, 'Reply Agent', 'Answered "do you deliver?" on WhatsApp'],
      [0, 'SEO Agent', 'Added 4 answers to the menu page'], [4, 'Report Agent', 'Weekly summary ready for review']];
    var k = 0;
    setInterval(function () {
      if (!visible) return;
      var it = items[k++ % items.length], row = document.createElement('div');
      row.className = 'row-f new';
      row.innerHTML = '<span class="av">' + icons[it[0]] + '</span><div><b>' + it[1] + '</b><small>' + it[2] + '</small></div><em>now</em>';
      $$('em', feed).forEach(function (m, i) { m.textContent = (i + 1) * 2 + 'm'; });
      feed.insertBefore(row, feed.firstChild);
      while (feed.children.length > 5) feed.removeChild(feed.lastChild);
    }, 2800);
  }
  // counters tick up now and then
  $$('[data-tick]').forEach(function (el, i) {
    var n = +el.dataset.tick;
    setInterval(function () { if (visible && Math.random() < 0.6) { n += 1; el.textContent = n; } }, 2200 + i * 900);
  });

  // the content agent types its hook, then starts the next one
  var typed = $('[data-type]');
  if (typed) {
    var lines = ['60 seconds inside our kitchen', 'Why regulars order this first', 'Rate our new menu, honestly'], li = 0;
    var type = function () {
      var text = lines[li++ % lines.length], j = 0;
      var t = setInterval(function () { typed.textContent = text.slice(0, ++j); if (j >= text.length) { clearInterval(t); setTimeout(type, 2600); } }, 55);
    };
    whenSeen(typed, function () { typed.textContent = ''; type(); });
  }

  // report numbers drift upward
  $$('.nums b[data-count]').forEach(function (el) {
    var n = +el.dataset.count;
    setTimeout(function () {
      setInterval(function () { if (visible && Math.random() < 0.5) { n += Math.max(1, Math.round(n * 0.002)); el.textContent = n.toLocaleString('en-IN'); } }, 1800);
    }, 2500);
  });

  // automation wires with travelling pulses
  var box = $('[data-flow]');
  if (box) {
    var svg = $('svg.wires', box), NS = 'http://www.w3.org/2000/svg';
    var clear = function () { $$('path, circle', svg).forEach(function (n) { n.parentNode.removeChild(n); }); };
    var draw = function () {
      clear();
      if (window.innerWidth <= 860) return;
      var b = box.getBoundingClientRect(), brain = $('[data-brain]', box);
      var pt = function (el, side) { var r = el.getBoundingClientRect(); return { x: (side === 'r' ? r.right : r.left) - b.left, y: r.top + r.height / 2 - b.top }; };
      var paths = [];
      $$('.c1 [data-n]', box).forEach(function (n) { paths.push([pt(n, 'r'), pt(brain, 'l')]); });
      $$('.c3 [data-n]', box).forEach(function (n) { paths.push([pt(brain, 'r'), pt(n, 'l')]); });
      var c3 = $$('.c3 [data-n]', box), c4 = $$('.c4 [data-n]', box);
      c3.forEach(function (n, i) { if (c4[i]) paths.push([pt(n, 'r'), pt(c4[i], 'l')]); });
      paths.forEach(function (p, i) {
        var a = p[0], z = p[1], mx = (a.x + z.x) / 2, d = 'M' + a.x + ' ' + a.y + ' C' + mx + ' ' + a.y + ' ' + mx + ' ' + z.y + ' ' + z.x + ' ' + z.y;
        var base = document.createElementNS(NS, 'path'); base.setAttribute('d', d); base.setAttribute('id', 'w' + i); svg.appendChild(base);
        var run = document.createElementNS(NS, 'path'); run.setAttribute('d', d); run.setAttribute('class', 'run'); svg.appendChild(run);
        var c = document.createElementNS(NS, 'circle'); c.setAttribute('r', '3.5');
        var m = document.createElementNS(NS, 'animateMotion'); m.setAttribute('dur', (2.2 + (i % 3) * 0.4) + 's'); m.setAttribute('repeatCount', 'indefinite'); m.setAttribute('begin', (i * 0.35) + 's');
        var mp = document.createElementNS(NS, 'mpath'); mp.setAttributeNS('http://www.w3.org/1999/xlink', 'href', '#w' + i); mp.setAttribute('href', '#w' + i);
        m.appendChild(mp); c.appendChild(m); svg.appendChild(c);
      });
    };
    var to; window.addEventListener('resize', function () { clearTimeout(to); to = setTimeout(draw, 150); });
    whenSeen(box, function () { setTimeout(draw, 900); });
  }

  // the platform prompt types itself, then the outputs appear
  var plat = $('.platform'), prompt = $('[data-prompt]');
  if (plat && prompt) {
    var full = prompt.textContent;
    whenSeen(plat, function () {
      prompt.textContent = ''; var j = 0;
      var t = setInterval(function () { prompt.textContent = full.slice(0, ++j); if (j >= full.length) clearInterval(t); }, 45);
    });
  }
})();

// hero sky: twinkling stars and shooting stars that rise like the logo's rocket
(function () {
  var c = document.querySelector('[data-sky]');
  if (!c || !c.getContext) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ctx = c.getContext('2d'), dpr = Math.min(2, window.devicePixelRatio || 1), W = 0, H = 0, stars = [], shots = [], last = 0, nextShot = 1200, running = true;
  var seed = 7; var rnd = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  var size = function () {
    var r = c.getBoundingClientRect(); W = r.width; H = r.height; c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    stars = []; var n = Math.round(W * H / 9000);
    for (var i = 0; i < n; i++) stars.push({ x: rnd() * W, y: rnd() * H, r: rnd() * 1.2 + 0.2, p: rnd() * Math.PI * 2, s: 0.4 + rnd() * 1.2, v: rnd() < 0.15 });
  };
  var shoot = function () {
    var x = W * (0.05 + Math.random() * 0.6), y = H * (0.45 + Math.random() * 0.5), sp = 0.55 + Math.random() * 0.35, len = 120 + Math.random() * 120;
    shots.push({ x: x, y: y, dx: sp, dy: -sp * 0.78, len: len, life: 0, max: 1600 + Math.random() * 700 });
  };
  var frame = function (t) {
    if (!running) return;
    var dt = Math.min(48, t - (last || t)); last = t;
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < stars.length; i++) {
      var s = stars[i], a = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t / 1000 * s.s + s.p));
      ctx.globalAlpha = a; ctx.fillStyle = s.v ? '#D8BBFF' : '#FFFFFF';
      ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();
    }
    nextShot -= dt; if (nextShot <= 0) { shoot(); nextShot = 3200 + Math.random() * 3200; }
    for (var j = shots.length - 1; j >= 0; j--) {
      var h = shots[j]; h.life += dt; h.x += h.dx * dt; h.y += h.dy * dt;
      var k = h.life / h.max, fade = k < 0.15 ? k / 0.15 : k > 0.75 ? Math.max(0, (1 - k) / 0.25) : 1;
      var n = Math.hypot(h.dx, h.dy), tx = h.x - h.dx / n * h.len, ty = h.y - h.dy / n * h.len;
      var g = ctx.createLinearGradient(tx, ty, h.x, h.y); g.addColorStop(0, 'rgba(169,92,255,0)'); g.addColorStop(0.6, 'rgba(216,187,255,' + 0.5 * fade + ')'); g.addColorStop(1, 'rgba(255,255,255,' + fade + ')');
      ctx.globalAlpha = 1; ctx.strokeStyle = g; ctx.lineWidth = 2; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(tx, ty); ctx.lineTo(h.x, h.y); ctx.stroke();
      ctx.globalAlpha = fade; ctx.fillStyle = '#FFFFFF'; ctx.beginPath(); ctx.arc(h.x, h.y, 2.2, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = fade * 0.35; ctx.beginPath(); ctx.arc(h.x, h.y, 7, 0, Math.PI * 2); ctx.fill();
      if (h.life >= h.max) shots.splice(j, 1);
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(frame);
  };
  size();
  var to; window.addEventListener('resize', function () { clearTimeout(to); to = setTimeout(size, 200); });
  if (reduce) { frame(0); running = false; return; }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { var vis = es[0].isIntersecting; if (vis && !running) { running = true; last = 0; requestAnimationFrame(frame); } else if (!vis) running = false; }).observe(c);
  document.addEventListener('visibilitychange', function () { if (document.hidden) running = false; else if (!running) { running = true; last = 0; requestAnimationFrame(frame); } });
  requestAnimationFrame(frame);
})();

// scroll progress bar in the logo gradient
(function () {
  var bar = document.createElement('div'); bar.className = 'progress'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
  var tick = false, set = function () { var d = document.documentElement, max = d.scrollHeight - d.clientHeight; bar.style.setProperty('--p', max > 0 ? (d.scrollTop / max).toFixed(4) : 0); tick = false; };
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(set); } }, { passive: true }); set();
})();

// ---------- agents chat app, scroll reveal, tilt and parallax ----------
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) document.documentElement.classList.add('js-motion');

  // agents: tabs that switch conversations; messages arrive one by one
  var app = document.querySelector('[data-agentapp]');
  if (app) {
    var tabs = [].slice.call(app.querySelectorAll('[role="tab"]')), cur = 0, timers = [], auto = null, inView = false, held = false;
    var clear = function () { timers.forEach(clearTimeout); timers = []; };
    var play = function (panel) {
      var box = panel.querySelector('.aa-msgs'), ms = [].slice.call(box.querySelectorAll('[data-m]'));
      clear();
      var chips = [].slice.call(box.querySelectorAll('.stp'));
      if (reduce) { ms.forEach(function (m) { m.classList.add('on'); }); chips.forEach(function (c) { c.classList.add('done'); }); return; }
      ms.forEach(function (m) { m.classList.remove('on'); }); chips.forEach(function (c) { c.classList.remove('done'); }); box.classList.remove('is-typing');
      var t = 300;
      ms.forEach(function (m) {
        if (m.hasAttribute('data-steps')) {
          timers.push(setTimeout(function () { m.classList.add('on'); }, t)); t += 350;
          chips.forEach(function (c) { t += 520; timers.push(setTimeout(function () { c.classList.add('done'); }, t)); });
          t += 300; return;
        }
        var isAgent = m.classList.contains('am');
        if (isAgent) { timers.push(setTimeout(function () { box.classList.add('is-typing'); }, t)); t += 900; }
        timers.push(setTimeout(function () { box.classList.remove('is-typing'); m.classList.add('on'); }, t));
        t += isAgent ? 1100 : 700;
      });
    };
    var select = function (i, focus) {
      cur = (i + tabs.length) % tabs.length;
      tabs.forEach(function (tb, k) {
        var on = k === cur, pn = document.getElementById(tb.getAttribute('aria-controls'));
        tb.setAttribute('aria-selected', on ? 'true' : 'false'); tb.tabIndex = on ? 0 : -1; pn.hidden = !on;
        if (on) play(pn);
        var bar = tb.querySelector('.aa-prog');
        if (bar) { bar.classList.remove('run'); if (on && !reduce) { void bar.offsetWidth; bar.classList.add('run'); } }
      });
      if (focus) tabs[cur].focus();
    };
    var loop = function () { clearInterval(auto); if (reduce) return; auto = setInterval(function () { if (inView && !held && !document.hidden) select(cur + 1); }, 11000); };
    tabs.forEach(function (tb, k) {
      tb.addEventListener('click', function () { select(k); loop(); });
      tb.addEventListener('keydown', function (e) {
        var d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); select(cur + d, true); loop(); }
        if (e.key === 'Home') { e.preventDefault(); select(0, true); } if (e.key === 'End') { e.preventDefault(); select(tabs.length - 1, true); }
      });
    });
    app.addEventListener('mouseenter', function () { held = true; }); app.addEventListener('mouseleave', function () { held = false; });
    app.addEventListener('focusin', function () { held = true; }); app.addEventListener('focusout', function () { held = false; });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { var was = inView; inView = es[0].isIntersecting; if (inView && !was) select(cur); }, { threshold: 0.35 }).observe(app);
    else select(0);
    loop();
  }

  // statement: words fill in as you scroll
  var words = document.querySelector('[data-words]');
  var spans = [];
  if (words && !reduce) {
    var hi = { agents: 1, experts: 1, every: 1, single: 1, day: 1 };
    words.innerHTML = words.textContent.trim().split(/\s+/).map(function (w) {
      var k = w.toLowerCase().replace(/[^a-z]/g, ''); return '<span' + (hi[k] ? ' data-hi' : '') + '>' + w + '</span>';
    }).join(' ');
    spans = [].slice.call(words.querySelectorAll('span'));
    spans.forEach(function (s) { if (s.hasAttribute('data-hi')) s.classList.add('hi'); });
  }

  // the workspace panel tilts flat as it scrolls in; the mascot drifts slower than the page
  var con = document.querySelector('.hero-in .console'), art = document.querySelector('.hero-art'), orb = art && art.querySelector('.orb'), mas = art && art.querySelector('.mascot');
  var ticking = false;
  var frame = function () {
    ticking = false;
    var vh = window.innerHeight, y = window.scrollY;
    if (spans.length) {
      var r = words.getBoundingClientRect(), p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      var n = Math.round(p * spans.length);
      for (var i = 0; i < spans.length; i++) spans[i].classList.toggle('on', i < n);
    }
    if (con && !reduce && window.innerWidth > 700) {
      var rc = con.getBoundingClientRect(), q = Math.min(1, Math.max(0, (vh - rc.top) / (vh * 0.75)));
      con.style.transform = 'perspective(1600px) rotateX(' + ((1 - q) * 14).toFixed(2) + 'deg) scale(' + (0.94 + 0.06 * q).toFixed(3) + ')';
    }
    if (art && !reduce && y < vh * 1.2) {
      if (mas) mas.style.translate = '0 ' + (y * -0.12).toFixed(1) + 'px';
      if (orb) orb.style.translate = '0 ' + (y * 0.08).toFixed(1) + 'px';
    }
  };
  var onScroll = function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); frame();
})();

// muted clips play only while on screen (and never under reduced motion)
(function () {
  var vids = document.querySelectorAll('video[data-autoplay]'); if (!vids.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) { vids.forEach(function (v) { v.setAttribute('controls', ''); v.preload = 'metadata'; }); return; }
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { var v = e.target; if (e.isIntersecting) { v.preload = 'auto'; var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); }); }, { threshold: 0.25 });
  vids.forEach(function (v) { io.observe(v); });
})();

// ---------- dark theme motion: rising sparks, card spotlight and tilt, headings word by word ----------
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;
  // sparks drifting up behind the page
  var box = document.createElement('div'); box.className = 'sparks'; box.setAttribute('aria-hidden', 'true');
  var n = window.innerWidth < 700 ? 14 : 28, html = '';
  for (var i = 0; i < n; i++) {
    var sz = (Math.random() * 2.5 + 1.5).toFixed(1);
    html += '<i style="left:' + (Math.random() * 100).toFixed(1) + '%;width:' + sz + 'px;height:' + sz + 'px;animation-duration:' + (14 + Math.random() * 18).toFixed(1) + 's;animation-delay:-' + (Math.random() * 30).toFixed(1) + 's"></i>';
  }
  box.innerHTML = html; document.body.appendChild(box);
  // spotlight follows the cursor; cards tilt a little
  var fine = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  if (fine) document.querySelectorAll('.svc-c, .ind, .guide, .band').forEach(function (c) {
    c.classList.add('tilt');
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      c.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
      if (!c.classList.contains('band')) { c.style.setProperty('--ry', ((x - 0.5) * 6).toFixed(2) + 'deg'); c.style.setProperty('--rx', ((0.5 - y) * 6).toFixed(2) + 'deg'); }
    });
    c.addEventListener('pointerleave', function () { c.style.setProperty('--rx', '0deg'); c.style.setProperty('--ry', '0deg'); });
  });
  // section headings rise word by word (text stays in the DOM for search)
  var heads = document.querySelectorAll('.sec-head h2, .faq h2, .close h2');
  heads.forEach(function (h) {
    if (h.querySelector('.w')) return;
    var k = 0;
    var walk = function (node) {
      [].slice.call(node.childNodes).forEach(function (ch) {
        if (ch.nodeType === 3) {
          var frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var sp = document.createElement('span'); sp.className = 'w'; sp.style.setProperty('--i', k++); sp.textContent = part; frag.appendChild(sp);
          });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1) walk(ch);
      });
    };
    walk(h); h.classList.add('split');
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: 0.4 });
    heads.forEach(function (h) { io.observe(h); });
  } else heads.forEach(function (h) { h.classList.add('in'); });
})();

// ---------- product UI motion: stat bumps, nav glide, read ticks, typed suggestions, sequenced automation flow ----------
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;
  var $$ = function (sel, r) { return [].slice.call((r || document).querySelectorAll(sel)); };
  // stat numbers glow when they tick
  $$('[data-tick]').forEach(function (b) { new MutationObserver(function () { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); }).observe(b, { childList: true, characterData: true, subtree: true }); });
  // sidebar: the active item moves through the workspace like someone is using it
  var nav = $$('.c-nav > span');
  if (nav.length) { var ni = 0; setInterval(function () { if (document.hidden) return; nav[ni].classList.remove('on'); ni = (ni + 1) % nav.length; nav[ni].classList.add('on'); }, 3200); }
  // whatsapp: outgoing messages turn "read" a moment after the chat plays
  setTimeout(function () { $$('.msg.out').forEach(function (m, i) { setTimeout(function () { m.classList.add('on'); }, i * 900); }); }, 2500);
  // message box types suggestions
  var ph = document.querySelector('[data-ph]');
  if (ph) {
    var tips = ['Plan next week\'s reels for the café', 'Reply to new WhatsApp leads', 'Move budget to the best ad', 'Write 3 FAQ answers for Google', 'Send me this month\'s report'], ti = 0;
    var typeTip = function () {
      var text = tips[ti++ % tips.length], j = 0;
      var t = setInterval(function () {
        ph.textContent = text.slice(0, ++j);
        if (j >= text.length) {
          clearInterval(t);
          setTimeout(function () { var k = text.length; var d = setInterval(function () { ph.textContent = text.slice(0, --k); if (k <= 0) { clearInterval(d); setTimeout(typeTip, 300); } }, 22); }, 1800);
        }
      }, 45);
    };
    setTimeout(typeTip, 1200);
  }
  // automation flow: a message comes in, the agent thinks, the outputs light up in order
  var box = document.querySelector('[data-flow]');
  if (box) {
    var ins = $$('.c1 [data-n]', box), outs = $$('.c3 [data-n]', box), ends = $$('.c4 [data-n]', box), brain = box.querySelector('[data-brain]'), say = box.querySelector('[data-brain-say]');
    var lines = ['Reading the message', 'Answering in your voice', 'Qualifying the lead', 'Booking and saving'], step = 0, timers = [];
    var later = function (fn, ms) { timers.push(setTimeout(fn, ms)); };
    var off = function () { $$('.live', box).forEach(function (n) { n.classList.remove('live'); }); };
    var cycle = function () {
      timers.forEach(clearTimeout); timers = [];
      var src = ins[step++ % ins.length]; off();
      src.classList.add('live');
      later(function () { brain.classList.add('think'); if (say) say.textContent = lines[0]; }, 700);
      later(function () { if (say) say.textContent = lines[1]; if (outs[0]) outs[0].classList.add('live'); }, 1500);
      later(function () { if (say) say.textContent = lines[2]; if (outs[1]) outs[1].classList.add('live'); }, 2200);
      later(function () { if (say) say.textContent = lines[3]; if (outs[2]) outs[2].classList.add('live'); src.classList.remove('live'); }, 2900);
      ends.forEach(function (n, i) { later(function () { n.classList.add('live'); }, 3500 + i * 450); });
      later(function () { brain.classList.remove('think'); if (say) say.textContent = 'Understands, answers, qualifies'; }, 5000);
      later(off, 5900);
    };
    var handled = box.querySelector('[data-handled]'), hn = 1284, running = false, loop;
    var start = function () {
      if (running) return; running = true; cycle();
      loop = setInterval(function () { if (!document.hidden) { cycle(); if (handled) { hn += 1 + Math.floor(Math.random() * 3); handled.textContent = hn.toLocaleString('en-IN'); } } }, 6400);
    };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting) start(); else { running = false; clearInterval(loop); } }, { threshold: 0.3 }).observe(box);
    else start();
  }
})();
