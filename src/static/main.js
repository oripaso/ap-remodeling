/* =============================================================
   A&P Remodeling and Consulting — interactions
   Zero dependencies. Restrained motion. Reduced-motion aware.
   ============================================================= */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* =========================================================
     LEAD DELIVERY — configure this and leads go to a real inbox.
     Set ENDPOINT to a Formspree / Basin / Zapier / Make / n8n /
     Google Apps Script webhook URL. It receives JSON via POST.
     Leave it empty and the form falls back to opening a
     pre-filled email or text so no lead is ever lost.
     ========================================================= */
  var LEAD = {
    ENDPOINT: '',                 /* e.g. 'https://formspree.io/f/xxxxxxx' */
    METHOD: 'POST',
    PHONE: '+13106335777',
    EMAIL: ''                     /* e.g. 'info@aproofla.com' */
  };

  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- reveal ---------- */
  var targets = $$('.rv, .lines, .fr, .hero__media');

  /* Reveal WELL before an element reaches the viewport. iOS Safari defers
     IntersectionObserver callbacks during momentum scrolling, so anything
     revealed exactly at the viewport edge shows up blank on a fast flick.
     A generous margin plus the sweep below means content is never late. */
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0, rootMargin: '500px 0px 500px 0px' }) : null;

  if (io) targets.forEach(function (el) { io.observe(el); });
  else targets.forEach(function (el) { el.classList.add('in'); });

  /* Failsafe: anything actually on screen is visible, observer or not. */
  var sweeping = false;
  function sweep() {
    if (sweeping) return;
    sweeping = true;
    requestAnimationFrame(function () {
      sweeping = false;
      var h = window.innerHeight, left = false;
      for (var n = 0; n < targets.length; n++) {
        var el = targets[n];
        if (el.classList.contains('in')) continue;
        left = true;
        var r = el.getBoundingClientRect();
        if (r.top < h + 240 && r.bottom > -240) { el.classList.add('in'); if (io) io.unobserve(el); }
      }
      if (!left) window.removeEventListener('scroll', sweep);
    });
  }
  window.addEventListener('scroll', sweep, { passive: true });
  window.addEventListener('resize', sweep);
  window.addEventListener('pageshow', sweep);
  window.addEventListener('load', sweep);
  sweep();

  requestAnimationFrame(function () {
    $$('.hero__media, .hero .lines, .hero .rv').forEach(function (el) { el.classList.add('in'); });
  });

  /* ---------- image skeletons ---------- */
  $$('.fr').forEach(function (fr) {
    var img = fr.querySelector('img');
    if (!img) { fr.classList.add('ready'); return; }
    var ok = function () { fr.classList.add('ready'); };
    if (img.complete && img.naturalWidth > 0) ok();
    else {
      img.addEventListener('load', ok);
      img.addEventListener('error', ok);
      setTimeout(ok, 7000);           /* never shimmer forever on a slow host */
    }
  });

  /* ---------- header ---------- */
  var hdr = $('#hdr'), mbar = $('#mbar'), lastY = window.pageYOffset;
  var heroEl = $('.hero') || $('.phero');

  function onScroll() {
    var y = window.pageYOffset;
    if (hdr) {
      var over = !!heroEl && y < (heroEl.offsetHeight - 76);
      hdr.classList.toggle('over', over);
      hdr.classList.toggle('stuck', y > 20 && !over);
      hdr.classList.toggle('away', y > lastY && y > 460 && !document.body.classList.contains('lock'));
    }
    if (mbar) mbar.classList.toggle('on', y > window.innerHeight * 0.6);
    lastY = y;
    procSync();
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- drawer ---------- */
  (function () {
    var burger = $('#burger'), drawer = $('#drawer');
    if (!burger || !drawer) return;
    var last = null;
    function open() {
      last = document.activeElement;
      drawer.hidden = false;
      requestAnimationFrame(function () { drawer.classList.add('open'); });
      burger.setAttribute('aria-expanded', 'true');
      burger.setAttribute('aria-label', 'Close menu');
      document.body.classList.add('lock');
      var a = drawer.querySelector('a'); if (a) setTimeout(function () { a.focus(); }, 220);
    }
    function close() {
      drawer.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('lock');
      setTimeout(function () { drawer.hidden = true; }, 400);
      if (last) last.focus();
    }
    burger.addEventListener('click', function () {
      burger.getAttribute('aria-expanded') === 'true' ? close() : open();
    });
    $$('a', drawer).forEach(function (a) { a.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') close();
    });
  })();

  /* ---------- in-page anchors ---------- */
  $$('a[href*="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var href = a.getAttribute('href') || '';
      var hash = href.indexOf('#') === 0 ? href : null;
      if (!hash || hash === '#') return;
      var t = document.querySelector(hash);
      if (!t) return;
      e.preventDefault();
      window.scrollTo({ top: t.getBoundingClientRect().top + window.pageYOffset - 84,
                        behavior: reduce ? 'auto' : 'smooth' });
      history.replaceState(null, '', hash);
    });
  });

  /* ---------- FAQ ---------- */
  $$('.faq__q').forEach(function (btn) {
    var panel = btn.parentNode.nextElementSibling;
    if (!panel) return;
    panel.style.height = '0px';
    btn.addEventListener('click', function () {
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      $$('.faq__q').forEach(function (o) {
        if (o === btn) return;
        o.setAttribute('aria-expanded', 'false');
        var p = o.parentNode.nextElementSibling; if (p) p.style.height = '0px';
      });
      btn.setAttribute('aria-expanded', String(!isOpen));
      panel.style.height = isOpen ? '0px' : panel.scrollHeight + 'px';
    });
  });
  window.addEventListener('resize', function () {
    $$('.faq__q[aria-expanded="true"]').forEach(function (b) {
      var p = b.parentNode.nextElementSibling; if (p) p.style.height = p.scrollHeight + 'px';
    });
  });

  /* ---------- before / after ---------- */
  (function () {
    var wrap = $('#ba'), clip = $('#baClip'), handle = $('#baHandle'), range = $('#baRange');
    if (!wrap || !clip || !handle || !range) return;
    function paint(v) {
      clip.style.clipPath = 'inset(0 ' + (100 - v) + '% 0 0)';
      handle.style.left = v + '%';
      range.setAttribute('aria-valuetext', Math.round(v) + '% before');
    }
    paint(50);
    range.addEventListener('input', function () { paint(parseFloat(range.value)); });
    var dragging = false;
    function at(e) {
      var r = wrap.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX);
      var v = clamp(((x - r.left) / r.width) * 100, 0, 100);
      range.value = v; paint(v);
    }
    wrap.addEventListener('pointerdown', function (e) {
      if (e.target === range) return;
      dragging = true; at(e);
      if (wrap.setPointerCapture) wrap.setPointerCapture(e.pointerId);
    });
    wrap.addEventListener('pointermove', function (e) { if (dragging) at(e); });
    window.addEventListener('pointerup', function () { dragging = false; });
    ['pointerdown', 'touchstart', 'keydown'].forEach(function (ev) {
      wrap.addEventListener(ev, function () { wrap.classList.add('touched'); }, { once: true, passive: true });
    });
  })();

  /* ---------- process ---------- */
  var pSteps = $$('.proc__s'), pImgs = $$('.proc__fig img'), pAt = -1;
  function procSync() {
    if (!pSteps.length || !pImgs.length) return;
    var best = 0, bd = Infinity;
    pSteps.forEach(function (s, i) {
      var r = s.getBoundingClientRect();
      var d = Math.abs(r.top + r.height / 2 - window.innerHeight * 0.45);
      if (d < bd) { bd = d; best = i; }
    });
    if (best === pAt) return;
    pAt = best;
    pSteps.forEach(function (s, i) { s.classList.toggle('on', i === best); });
    pImgs.forEach(function (im, i) { im.classList.toggle('on', i === best); });
  }

  /* ---------- lead form ---------- */
  (function () {
    var form = $('#leadForm');
    if (!form) return;

    var steps = $$('.step', form), total = steps.length, i = 0, dir = 1, first = true;
    var bars = $$('#pbar i'), lbl = $('#pstep'), nm = $('#pname');
    var back = $('#lBack'), next = $('#lNext'), done = $('#leadDone'), again = $('#lAgain');
    var names = ['Project', 'Location', 'Timing', 'Details', 'Contact'];

    function render() {
      steps.forEach(function (s, n) {
        s.classList.remove('on', 'back');
        if (n === i) { s.classList.add('on'); if (dir < 0) s.classList.add('back'); }
      });
      bars.forEach(function (b, n) { b.classList.toggle('on', n <= i); });
      if (lbl) lbl.textContent = 'Step ' + (i + 1) + ' / ' + total;
      if (nm) nm.textContent = names[i];
      if (back) back.hidden = i === 0;
      if (next) next.firstChild.nodeValue = (i === total - 1) ? 'Send my project ' : 'Continue ';
      if (!first) {
        var f = steps[i].querySelector('input:not([type=radio]):not([type=file]), textarea, select');
        if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 60);
      }
      first = false;
    }

    function bad(id, msg) {
      var el = $('#' + id), box = el.closest('.f'), slot = $('#' + id + 'E');
      if (box) box.classList.toggle('bad', !!msg);
      if (slot) slot.textContent = msg || '';
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      return !msg;
    }

    function valid() {
      if (i !== total - 1) return true;
      var ok = true;
      if (!$('#lName').value.trim()) ok = bad('lName', 'Please add your name.') && ok;
      else bad('lName', '');
      var ph = $('#lPhone').value.trim();
      if (!ph) ok = bad('lPhone', 'We need a number to reach you.') && ok;
      else if (ph.replace(/\D/g, '').length < 10) ok = bad('lPhone', 'That number looks incomplete.') && ok;
      else bad('lPhone', '');
      return ok;
    }

    function val(n) {
      var el = form.querySelector('[name="' + n + '"]:checked') || form.querySelector('[name="' + n + '"]');
      return el ? el.value : '';
    }

    function payload() {
      var files = $('#lPhotos');
      return {
        source: 'aproofla.com',
        submitted_at: new Date().toISOString(),
        project_type: val('project'),
        area: $('#lArea').value.trim(),
        zip: $('#lZip').value.trim(),
        timeline: val('timing'),
        message: $('#lMsg').value.trim(),
        photo_count: files && files.files ? files.files.length : 0,
        name: $('#lName').value.trim(),
        phone: $('#lPhone').value.trim(),
        email: $('#lEmail').value.trim(),
        preferred_contact: val('preferred')
      };
    }

    function asText(d) {
      return [
        'Name: ' + d.name, 'Phone: ' + d.phone,
        d.email ? 'Email: ' + d.email : '',
        'Preferred contact: ' + d.preferred_contact, '',
        'Project: ' + d.project_type,
        'Location: ' + [d.area, d.zip].filter(Boolean).join(', '),
        'Timeline: ' + d.timeline,
        d.message ? '\nDetails: ' + d.message : '',
        d.photo_count ? '\n(' + d.photo_count + ' photo(s) to follow)' : ''
      ].filter(function (l) { return l !== ''; }).join('\n');
    }

    function succeed() {
      form.style.display = 'none';
      if (done) { done.classList.add('on'); done.setAttribute('tabindex', '-1'); done.focus(); }
    }

    function fallback(d) {
      var subject = 'Project enquiry - ' + d.project_type;
      var body = asText(d);
      var url;
      if (LEAD.EMAIL) url = 'mailto:' + LEAD.EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      else {
        var apple = /iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent);
        url = 'sms:' + LEAD.PHONE + (apple ? '&' : '?') + 'body=' + encodeURIComponent(subject + '\n' + body);
      }
      succeed();
      setTimeout(function () { window.location.href = url; }, 400);
    }

    function submit() {
      var d = payload();
      if (!LEAD.ENDPOINT) { fallback(d); return; }
      next.disabled = true;
      next.firstChild.nodeValue = 'Sending ';
      fetch(LEAD.ENDPOINT, {
        method: LEAD.METHOD,
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(d)
      }).then(function (r) {
        if (!r.ok) throw new Error('bad status ' + r.status);
        succeed();
      }).catch(function () {
        fallback(d);
      }).then(function () {
        next.disabled = false;
      });
    }

    next.addEventListener('click', function () {
      if (!valid()) return;
      if (i < total - 1) { dir = 1; i++; render(); } else submit();
    });
    back.addEventListener('click', function () { if (i > 0) { dir = -1; i--; render(); } });
    form.addEventListener('submit', function (e) { e.preventDefault(); next.click(); });
    form.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') { e.preventDefault(); next.click(); }
    });
    if (again) again.addEventListener('click', function () {
      done.classList.remove('on'); form.style.display = ''; form.reset();
      var t = $('#lThumbs'); if (t) t.innerHTML = '';
      dir = 1; i = 0; first = true; render();
    });

    var photos = $('#lPhotos'), thumbs = $('#lThumbs'), drop = $('#lDrop');
    if (photos && thumbs) {
      photos.addEventListener('change', function () {
        thumbs.innerHTML = '';
        Array.prototype.slice.call(photos.files).slice(0, 8).forEach(function (f) {
          if (!/^image\//.test(f.type)) return;
          var fig = document.createElement('figure'), img = document.createElement('img');
          img.alt = ''; img.src = URL.createObjectURL(f);
          img.onload = function () { URL.revokeObjectURL(img.src); };
          fig.appendChild(img); thumbs.appendChild(fig);
        });
      });
      ['dragenter', 'dragover'].forEach(function (ev) {
        drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('over'); });
      });
      ['dragleave', 'drop'].forEach(function (ev) {
        drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('over'); });
      });
      drop.addEventListener('drop', function (e) {
        if (e.dataTransfer && e.dataTransfer.files.length) {
          photos.files = e.dataTransfer.files;
          photos.dispatchEvent(new Event('change'));
        }
      });
    }

    render();
  })();

  /* ---------- sticky bar retreats at the form ---------- */
  (function () {
    var bar = $('#mbar'), zone = $('#start');
    if (!bar || !zone || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { bar.classList.toggle('hide', e.isIntersecting); });
    }, { threshold: 0.15 }).observe(zone);
  })();

  onScroll();
})();
