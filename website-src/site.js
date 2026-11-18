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
        '<div class="legend"><span><i style="background:var(--violet)"></i>Reel</span><span><i style="background:var(--pale)"></i>Post or carousel</span>' + (shoot ? '<span><i style="background:var(--ink)"></i>Shoot day</span>' : '') + '</div>' +
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
