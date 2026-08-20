/* =============================================================
   A&P Remodeling and Consulting — interactions
   No dependencies. Progressive enhancement. Reduced-motion aware.
   ============================================================= */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var BUSINESS_PHONE = '+13106335777';
  var BUSINESS_EMAIL = ''; /* EDIT ME: set to e.g. 'info@aproofla.com' to send by email instead of SMS */

  /* ---------- year ---------- */
  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- reveal on scroll ---------- */
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' }) : null;

  var revealables = $$('.rv, .lines, .figr, .hero__bg');
  if (io) { revealables.forEach(function (el) { io.observe(el); }); }
  else { revealables.forEach(function (el) { el.classList.add('in'); }); }

  /* hero should never wait for scroll */
  requestAnimationFrame(function () {
    ['#heroBg', '#heroH1'].forEach(function (s) { var el = $(s); if (el) el.classList.add('in'); });
    $$('.hero .rv').forEach(function (el) { el.classList.add('in'); });
  });

  /* ---------- header ---------- */
  var hdr = $('#hdr'), lastY = window.pageYOffset, mbar = $('#mbar');
  var heroEl = $('.hero') || $('.phero');

  function onScroll() {
    var y = window.pageYOffset;
    if (hdr) {
      var overDark = !!heroEl && y < (heroEl.offsetHeight - 72);
      hdr.classList.toggle('onhero', overDark);
      hdr.classList.toggle('stuck', y > 20 && !overDark);
      var hidden = y > lastY && y > 420 && !document.body.classList.contains('lock');
      hdr.classList.toggle('away', hidden);
    }
    if (mbar) mbar.classList.toggle('on', y > window.innerHeight * 0.7);
    lastY = y;
    procScroll();
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- mobile drawer ---------- */
  (function () {
    var burger = $('#burger'), drawer = $('#drawer');
    if (!burger || !drawer) return;
    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      drawer.hidden = false;
      requestAnimationFrame(function () { drawer.classList.add('open'); });
      burger.setAttribute('aria-expanded', 'true');
      burger.setAttribute('aria-label', 'Close menu');
      document.body.classList.add('lock');
      var first = drawer.querySelector('a');
      if (first) setTimeout(function () { first.focus(); }, 260);
    }
    function close() {
      drawer.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('lock');
      setTimeout(function () { drawer.hidden = true; }, 450);
      if (lastFocus) lastFocus.focus();
    }
    burger.addEventListener('click', function () {
      burger.getAttribute('aria-expanded') === 'true' ? close() : open();
    });
    $$('a', drawer).forEach(function (a) { a.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') close();
    });
  })();

  /* ---------- active nav ---------- */
  (function () {
    var links = $$('.mainnav a[href^="#"]');
    if (!links.length) return;
    var secs = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
    function tick() {
      var y = window.pageYOffset + window.innerHeight * 0.3, best = -1;
      secs.forEach(function (s, i) { if (s && s.offsetTop <= y) best = i; });
      links.forEach(function (a, i) { a.classList.toggle('on', i === best); });
    }
    window.addEventListener('scroll', tick, { passive: true });
    tick();
  })();

  /* ---------- smooth anchors with header offset ---------- */
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (!id || id === '#') return;
      var t = document.querySelector(id);
      if (!t) return;
      e.preventDefault();
      var top = t.getBoundingClientRect().top + window.pageYOffset - 80;
      window.scrollTo({ top: top, behavior: reduce ? 'auto' : 'smooth' });
      if (t.id) history.replaceState(null, '', '#' + t.id);
    });
  });

  /* ---------- FAQ accordion ---------- */
  $$('.faq__q').forEach(function (btn) {
    var panel = btn.parentNode.nextElementSibling;
    if (!panel) return;
    panel.style.height = '0px';
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      $$('.faq__q').forEach(function (o) {
        if (o === btn) return;
        var p = o.parentNode.nextElementSibling;
        o.setAttribute('aria-expanded', 'false');
        if (p) p.style.height = '0px';
      });
      btn.setAttribute('aria-expanded', String(!open));
      panel.style.height = open ? '0px' : panel.scrollHeight + 'px';
    });
  });
  window.addEventListener('resize', function () {
    $$('.faq__q[aria-expanded="true"]').forEach(function (b) {
      var p = b.parentNode.nextElementSibling;
      if (p) p.style.height = p.scrollHeight + 'px';
    });
  });

  /* ---------- before / after ---------- */
  (function () {
    var wrap = $('#ba'), clip = $('#baClip'), handle = $('#baHandle'), range = $('#baRange');
    if (!wrap || !clip || !handle || !range) return;

    function paint(v) {
      clip.style.clipPath = 'inset(0 ' + (100 - v) + '% 0 0)';
      handle.style.left = v + '%';
      range.setAttribute('aria-valuetext', Math.round(v) + '% of the after image hidden');
    }
    paint(50);
    range.addEventListener('input', function () { paint(parseFloat(range.value)); });

    /* pointer drag anywhere on the image */
    var dragging = false;
    function fromEvent(e) {
      var r = wrap.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX);
      var v = clamp(((x - r.left) / r.width) * 100, 0, 100);
      range.value = v; paint(v);
    }
    wrap.addEventListener('pointerdown', function (e) {
      if (e.target === range) return;
      dragging = true; fromEvent(e); wrap.setPointerCapture && wrap.setPointerCapture(e.pointerId);
    });
    wrap.addEventListener('pointermove', function (e) { if (dragging) fromEvent(e); });
    window.addEventListener('pointerup', function () { dragging = false; });

    /* one gentle sweep the first time it is seen */
    if (!reduce && io) {
      var seen = false;
      var bio = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting || seen) return;
          seen = true; bio.disconnect();
          var t0 = null;
          function step(t) {
            if (!t0) t0 = t;
            var k = Math.min((t - t0) / 1600, 1);
            var eased = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
            var v = 50 + Math.sin(eased * Math.PI * 2) * 22;
            range.value = v; paint(v);
            if (k < 1) requestAnimationFrame(step); else { range.value = 50; paint(50); }
          }
          setTimeout(function () { requestAnimationFrame(step); }, 260);
        });
      }, { threshold: 0.45 });
      bio.observe(wrap);
    }
  })();

  /* ---------- process: sync image to step ---------- */
  var pSteps = $$('.proc__s'), pImgs = $$('#procFig img'), pActive = -1;
  function procScroll() {
    if (!pSteps.length || !pImgs.length) return;
    var best = 0, bestD = Infinity;
    pSteps.forEach(function (s, i) {
      var r = s.getBoundingClientRect();
      var d = Math.abs(r.top + r.height / 2 - window.innerHeight * 0.46);
      if (d < bestD) { bestD = d; best = i; }
    });
    if (best === pActive) return;
    pActive = best;
    pSteps.forEach(function (s, i) { s.classList.toggle('on', i === best); });
    pImgs.forEach(function (im, i) { im.classList.toggle('on', i === best); });
  }

  /* ---------- multi-step estimate form ---------- */
  (function () {
    var form = $('#estForm');
    if (!form) return;

    var steps = $$('.step', form);
    var total = steps.length;
    var i = 0;
    var bar = $('#estBarFill'), barEl = $('#estBar');
    var lbl = $('#estStepLabel'), nameLbl = $('#estStepName');
    var back = $('#estBack'), next = $('#estNext');
    var done = $('#estDone'), again = $('#estAgain'), doneMsg = $('#doneMsg');
    var first = true;
    var names = ["What you're planning", 'Property location', 'Timeline', 'Project details', 'Contact details'];

    var dir = 1;
    function render() {
      steps.forEach(function (s, n) {
        s.classList.remove('from-right', 'from-left');
        s.classList.toggle('on', n === i);
      });
      if (steps[i]) {
        void steps[i].offsetWidth;
        steps[i].classList.add(dir >= 0 ? 'from-right' : 'from-left');
      }
      if (bar) bar.style.width = ((i + 1) / total * 100) + '%';
      if (barEl) barEl.setAttribute('aria-valuenow', String(i + 1));
      if (lbl) lbl.textContent = 'Step ' + (i + 1) + ' of ' + total;
      if (nameLbl) nameLbl.textContent = names[i] || '';
      if (back) back.hidden = i === 0;
      if (next) next.firstChild.nodeValue = (i === total - 1) ? 'Send my request ' : 'Continue ';
      if (!first) {
        var focusable = steps[i].querySelector('input:not([type=radio]):not([type=file]), textarea, select, input[type=radio]:checked');
        if (focusable) setTimeout(function () { focusable.focus({ preventScroll: true }); }, 60);
      }
      first = false;
    }

    function err(id, msg) {
      var input = $('#' + id), box = input.parentNode, slot = $('#' + id + 'Err');
      box.classList.toggle('bad', !!msg);
      if (slot) slot.textContent = msg || '';
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      return !msg;
    }

    function validate() {
      if (i !== total - 1) return true;
      var ok = true;
      var name = $('#eName').value.trim();
      var phone = $('#ePhone').value.trim();
      if (!name) ok = err('eName', 'Please add your name.') && ok;
      else err('eName', '');
      var digits = phone.replace(/\D/g, '');
      if (!phone) ok = err('ePhone', 'We need a number to call you back.') && ok;
      else if (digits.length < 10) ok = err('ePhone', 'That looks short — please check the number.') && ok;
      else err('ePhone', '');
      return ok;
    }

    function value(nm) {
      var el = form.querySelector('[name="' + nm + '"]:checked') || form.querySelector('[name="' + nm + '"]');
      return el ? el.value : '';
    }

    function submit() {
      var photos = $('#ePhotos');
      var nPhotos = photos && photos.files ? photos.files.length : 0;
      var subject = 'Free estimate request - ' + value('project');
      var body = [
        'Name: ' + $('#eName').value.trim(),
        'Phone: ' + $('#ePhone').value.trim(),
        $('#eEmail').value.trim() ? 'Email: ' + $('#eEmail').value.trim() : '',
        'Preferred contact: ' + value('preferred'),
        '',
        'Project: ' + value('project'),
        'Location: ' + [$('#eArea').value.trim(), $('#eZip').value.trim()].filter(Boolean).join(', '),
        'Timeline: ' + value('timing'),
        $('#eMsg').value.trim() ? '\nDetails: ' + $('#eMsg').value.trim() : '',
        nPhotos ? '\n(' + nPhotos + ' photo' + (nPhotos > 1 ? 's' : '') + ' to follow)' : ''
      ].filter(function (l) { return l !== ''; }).join('\n');

      var url, how;
      if (BUSINESS_EMAIL) {
        url = 'mailto:' + BUSINESS_EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        how = 'email';
      } else {
        var apple = /iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent);
        url = 'sms:' + BUSINESS_PHONE + (apple ? '&' : '?') + 'body=' + encodeURIComponent(subject + '\n' + body);
        how = 'text message';
      }

      if (doneMsg) {
        doneMsg.textContent = 'We’ve opened a pre-filled ' + how + ' to A&P with everything you entered — send it and we’ll come back to you with next steps.'
          + (nPhotos ? ' Attach your ' + nPhotos + ' photo' + (nPhotos > 1 ? 's' : '') + ' to that message.' : '')
          + ' If nothing opened, call 310-633-5777 — that always works.';
      }
      form.style.display = 'none';
      if (done) { done.classList.add('on'); done.focus && done.focus(); }
      window.location.href = url;
    }

    next.addEventListener('click', function () {
      if (!validate()) return;
      if (i < total - 1) { dir = 1; i++; render(); } else { submit(); }
    });
    back.addEventListener('click', function () { if (i > 0) { dir = -1; i--; render(); } });

    form.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') { e.preventDefault(); next.click(); }
    });
    form.addEventListener('submit', function (e) { e.preventDefault(); next.click(); });

    if (again) again.addEventListener('click', function () {
      done.classList.remove('on');
      form.style.display = '';
      form.reset(); $('#eThumbs').innerHTML = '';
      dir = 1; i = 0; render();
    });

    /* photo previews */
    var photos = $('#ePhotos'), thumbs = $('#eThumbs'), drop = $('#eDrop');
    if (photos && thumbs) {
      photos.addEventListener('change', function () {
        thumbs.innerHTML = '';
        Array.prototype.slice.call(photos.files).slice(0, 8).forEach(function (f) {
          if (!/^image\//.test(f.type)) return;
          var fig = document.createElement('figure');
          var img = document.createElement('img');
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


  /* =============================================================
     MOBILE MOTION LAYER
     ============================================================= */
  var isTouch  = window.matchMedia('(hover:none)').matches;
  var isMobile = window.matchMedia('(max-width:900px)').matches;
  var hasSDA   = !!(window.CSS && CSS.supports && CSS.supports('animation-timeline', 'scroll()'));

  /* --- scroll progress rail (JS fallback where scroll timelines are missing) --- */
  (function () {
    if (reduce) return;
    var rail = document.createElement('div');
    rail.className = 'sprog'; rail.setAttribute('aria-hidden', 'true');
    rail.innerHTML = '<i></i>';
    document.body.appendChild(rail);
    if (hasSDA) return;
    var fill = rail.firstChild;
    window.addEventListener('scroll', function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      fill.style.width = (h > 0 ? (window.pageYOffset / h) * 100 : 0) + '%';
    }, { passive: true });
  })();

  /* --- pillar carousel: dots + snap tracking --- */
  (function () {
    var track = $('.pillars');
    if (!track) return;
    var cards = $$('.pillar', track);
    if (cards.length < 2) return;

    var dots = document.createElement('div');
    dots.className = 'dots';
    dots.setAttribute('role', 'group');
    dots.setAttribute('aria-label', 'Service categories');
    cards.forEach(function (c, i) {
      var b = document.createElement('button');
      b.type = 'button';
      var h = c.querySelector('h3');
      b.setAttribute('aria-label', h ? h.textContent : 'Slide ' + (i + 1));
      b.setAttribute('aria-current', i === 0 ? 'true' : 'false');
      b.addEventListener('click', function () {
        track.scrollTo({ left: c.offsetLeft - track.offsetLeft, behavior: reduce ? 'auto' : 'smooth' });
      });
      dots.appendChild(b);
    });
    track.parentNode.insertBefore(dots, track.nextSibling);

    var ticking = false;
    track.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var mid = track.scrollLeft + track.clientWidth / 2, best = 0, bd = Infinity;
        cards.forEach(function (c, i) {
          var d = Math.abs((c.offsetLeft - track.offsetLeft) + c.offsetWidth / 2 - mid);
          if (d < bd) { bd = d; best = i; }
        });
        $$('button', dots).forEach(function (b, i) {
          b.setAttribute('aria-current', i === best ? 'true' : 'false');
        });
        ticking = false;
      });
    }, { passive: true });
  })();

  /* --- before/after: touch hint until first interaction --- */
  (function () {
    var ba = $('#ba');
    if (!ba || reduce) return;
    var hint = document.createElement('div');
    hint.className = 'ba__hint';
    hint.setAttribute('aria-hidden', 'true');
    hint.innerHTML = '<svg viewBox="0 0 24 24"><path d="M9 6 4 12l5 6M15 6l5 6-5 6"/></svg>Drag to compare';
    ba.appendChild(hint);
    ['pointerdown', 'touchstart', 'keydown'].forEach(function (ev) {
      ba.addEventListener(ev, function () { ba.classList.add('touched'); }, { once: true, passive: true });
    });
  })();

  /* --- process rail fill --- */
  (function () {
    var steps = $('.proc__steps'), sec = $('.proc');
    if (!steps || !sec) return;
    function fill() {
      var r = sec.getBoundingClientRect();
      var span = r.height - window.innerHeight * 0.35;
      var p = clamp((-r.top + window.innerHeight * 0.55) / (span || 1), 0, 1);
      steps.style.setProperty('--rail', (p * 100) + '%');
    }
    window.addEventListener('scroll', fill, { passive: true });
    window.addEventListener('resize', fill);
    fill();
  })();

  /* --- sticky bar retreats while the estimate form is on screen --- */
  (function () {
    var bar = $('#mbar'), est = $('#estimate');
    if (!bar || !est || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { bar.classList.toggle('hide', e.isIntersecting); });
    }, { threshold: 0.18 }).observe(est);
  })();


  /* --- image skeletons: clear the shimmer as each image arrives --- */
  (function () {
    function done(frame) { frame && frame.classList.add('loaded'); }
    $$('.figr, .areas__map').forEach(function (frame) {
      var img = frame.querySelector('img');
      if (!img) { done(frame); return; }
      if (img.complete && img.naturalWidth > 0) { done(frame); return; }
      img.addEventListener('load', function () { done(frame); });
      img.addEventListener('error', function () { done(frame); });
    });
  })();

  /* ---------- graceful image failure ---------- */
  $$('img').forEach(function (img) {
    img.addEventListener('error', function () {
      img.style.background = 'linear-gradient(135deg,#EFE9DF,#DCD4C6)';
      img.style.objectFit = 'cover';
      img.removeAttribute('srcset');
    });
  });

  onScroll();
})();
