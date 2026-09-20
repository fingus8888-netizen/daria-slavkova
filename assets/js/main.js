(function () {
  'use strict';

  var COUNT = 28;
  var grid = document.getElementById('grid');

  /* --- build the work grid --- */
  var frag = document.createDocumentFragment();
  for (var i = 1; i <= COUNT; i++) {
    var n = String(i).padStart(2, '0');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Open photo ' + i + ' of ' + COUNT);
    btn.dataset.index = i - 1;
    btn.dataset.full = 'assets/img/g' + n + '-full.webp';
    var img = new Image();
    img.src = 'assets/img/g' + n + '.webp';
    img.alt = 'Makeup work by Daria Slavkova, photo ' + i;
    img.loading = i > 7 ? 'lazy' : 'eager';
    img.decoding = 'async';
    img.width = 560; img.height = 560;
    btn.appendChild(img);
    frag.appendChild(btn);
  }
  grid.appendChild(frag);

  /* --- lightbox --- */
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lbImg');
  var lbCount = document.getElementById('lbCount');
  var items = [].slice.call(grid.querySelectorAll('button'));
  var current = -1, lastFocus = null;

  function show(idx) {
    current = (idx + COUNT) % COUNT;
    var btn = items[current];
    lbImg.src = btn.dataset.full;
    lbImg.alt = btn.querySelector('img').alt;
    lbCount.textContent = (current + 1) + ' / ' + COUNT;
    var nxt = items[(current + 1) % COUNT];
    new Image().src = nxt.dataset.full;
  }
  function open(idx) {
    lastFocus = document.activeElement;
    lb.hidden = false;
    document.body.classList.add('lb-open');
    show(idx);
    requestAnimationFrame(function () { lb.classList.add('open'); });
    lb.querySelector('.lb-close').focus();
  }
  function close() {
    lb.classList.remove('open');
    document.body.classList.remove('lb-open');
    setTimeout(function () { lb.hidden = true; lbImg.src = ''; }, 250);
    if (lastFocus) lastFocus.focus();
  }

  grid.addEventListener('click', function (e) {
    var btn = e.target.closest('button');
    if (btn) open(+btn.dataset.index);
  });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', function () { show(current - 1); });
  lb.querySelector('.lb-next').addEventListener('click', function () { show(current + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(current - 1);
    else if (e.key === 'ArrowRight') show(current + 1);
  });

  var touchX = null;
  lb.addEventListener('touchstart', function (e) { touchX = e.changedTouches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
    touchX = null;
  }, { passive: true });

  /* --- reveal on scroll --- */
  var targets = [].slice.call(document.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add('in'); });
  }

  /* --- header turns light over the dark sections --- */
  var header = document.querySelector('.site-header');
  var dark = [].slice.call(document.querySelectorAll('.about, .contact'));
  function syncHeader() {
    var h = header.offsetHeight;
    var over = dark.some(function (s) {
      var r = s.getBoundingClientRect();
      return r.top <= h - 1 && r.bottom > h - 1;
    });
    header.classList.toggle('on-dark', over);
  }
  addEventListener('scroll', syncHeader, { passive: true });
  addEventListener('resize', syncHeader);
  syncHeader();
})();
