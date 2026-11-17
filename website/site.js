// Nxtlvl Social: header state, mobile menu, quiet section reveals and the booking form. No libraries.
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  var top = document.querySelector('.top');
  var onScroll = function () { if (top) top.classList.toggle('scrolled', window.scrollY > 8); };
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  var burger = document.querySelector('.burger'), mob = document.getElementById('mob');
  if (burger && mob) burger.addEventListener('click', function () {
    var open = mob.hasAttribute('hidden');
    if (open) mob.removeAttribute('hidden'); else mob.setAttribute('hidden', '');
    burger.setAttribute('aria-expanded', String(open));
  });

  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  // pre-select a service when a link carries ?need=...
  var need = new URLSearchParams(location.search).get('need');
  var sel = document.getElementById('need');
  if (need && sel && sel.querySelector('option[value="' + need + '"]')) sel.value = need;

  var form = document.querySelector('form.book');
  if (!form) return;
  var started = Date.now();
  var msg = form.querySelector('.form-msg');
  var show = function (text, ok) { msg.textContent = text; msg.className = 'form-msg ' + (ok ? 'ok' : 'err'); msg.hidden = false; };
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var btn = form.querySelector('button[type=submit]');
    var data = {
      name: form.name.value.trim(), business: form.business.value.trim(), email: form.email.value.trim(),
      need: form.need.value, message: form.message.value.trim(), website: form.website.value, t: started,
    };
    if (data.name.length < 2) { show('Please tell us your name.'); form.name.focus(); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email)) { show('Please enter a valid email so we can reply.'); form.email.focus(); return; }
    btn.disabled = true; var label = btn.textContent; btn.textContent = 'Sending…';
    fetch('/api/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (res) {
        if (res && res.ok) { form.reset(); show('Thanks, ' + data.name.split(' ')[0] + '. We have your request and will reply by email within one business day.', true); }
        else show((res && res.error) || 'Something went wrong. Please email connect@nxtlvlsocial.ai instead.');
      })
      .catch(function () { show('Could not send right now. Please email connect@nxtlvlsocial.ai instead.'); })
      .then(function () { btn.disabled = false; btn.textContent = label; });
  });
})();
