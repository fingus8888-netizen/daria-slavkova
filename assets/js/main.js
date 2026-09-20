(function () {
  'use strict';

  /* страница всегда открывается сверху, если в адресе нет якоря */
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  if (!location.hash) {
    window.scrollTo(0, 0);
    addEventListener('load', function () { if (!location.hash) window.scrollTo(0, 0); });
  }

  /* --- сетка работ на главной --- */
  var grid = document.getElementById('grid');
  if (grid) {
    var TILES = 28;
    var frag = document.createDocumentFragment();
    for (var i = 1; i <= TILES; i++) {
      var n = String(i).padStart(2, '0');
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Open photo ' + i + ' of ' + TILES);
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
  }

  /* --- лайтбокс: любые кнопки с data-full на странице --- */
  var lb = document.getElementById('lightbox');
  var items = [].slice.call(document.querySelectorAll('button[data-full]'));
  if (lb && items.length) {
    var lbImg = document.getElementById('lbImg');
    var lbCount = document.getElementById('lbCount');
    var total = items.length;
    var current = -1, lastFocus = null;

    function show(idx) {
      current = (idx + total) % total;
      var btn = items[current];
      lbImg.src = btn.dataset.full;
      lbImg.alt = btn.querySelector('img').alt;
      lbCount.textContent = (current + 1) + ' / ' + total;
      new Image().src = items[(current + 1) % total].dataset.full;
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

    items.forEach(function (btn, idx) {
      btn.addEventListener('click', function () { open(idx); });
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
  }

  /* --- появление блоков при скролле --- */
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

  /* --- шапка светлеет над тёмными секциями --- */
  var header = document.querySelector('.site-header');
  var dark = [].slice.call(document.querySelectorAll('.about, .contact'));
  if (header && dark.length) {
    var syncHeader = function () {
      var h = header.offsetHeight;
      header.classList.toggle('on-dark', dark.some(function (s) {
        var r = s.getBoundingClientRect();
        return r.top <= h - 1 && r.bottom > h - 1;
      }));
    };
    addEventListener('scroll', syncHeader, { passive: true });
    addEventListener('resize', syncHeader);
    syncHeader();
  }
})();
