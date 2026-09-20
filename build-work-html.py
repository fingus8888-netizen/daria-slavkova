#!/usr/bin/env python3
"""Генерация work.html из work-data.json (лента листа /work макета)."""
import json, re, html

data = json.load(open('work-data.json'))
ROLE = re.compile(r'(?=(?:Ph|model|makeup artist|makeup|hair|stylist|Stylist)\s*:)')

def credit(t):
    t = t.replace(' ', ' ').replace(' ', ' ')
    parts = [p.strip(' ,') for p in ROLE.split(t) if p.strip(' ,')]
    return ''.join(f'<span>{html.escape(p)}</span>' for p in parts)

blocks, shot = [], 0
for b in data:
    if b['type'] == 'section':
        lines = [l.strip() for l in b['text'].split('\n') if l.strip()]
        head = f'<h2>{html.escape(lines[0])}</h2>'
        if len(lines) > 1:
            head += f'<p class="sub">{html.escape(lines[1])}</p>'
        blocks.append(f'    <div class="w-section">{head}</div>')
    elif b['type'] == 'credit':
        blocks.append(f'    <p class="w-credit">{credit(b["text"])}</p>')
    else:
        cells = []
        for src in b['images']:
            shot += 1
            small = src.replace('.webp', '-s.webp')
            lazy = '' if shot <= 2 else ' loading="lazy"'
            cells.append(
                f'      <button type="button" data-full="{src}" aria-label="Open photo {shot}">'
                f'<img src="{small}" alt="Work by Daria Slavkova, photo {shot}"{lazy} decoding="async"></button>')
        blocks.append('    <div class="w-pair">\n' + '\n'.join(cells) + '\n    </div>')

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Selected work — Daria Slavkova</title>
<meta name="description" content="Selected work of Daria Slavkova — editorial, beauty, fashion, clients makeup, runway and backstage.">
<meta property="og:title" content="Selected work — Daria Slavkova">
<meta property="og:image" content="assets/img/work/w01.webp">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23F0EEDE'/%3E%3Ctext x='16' y='22' font-family='Arial' font-size='15' text-anchor='middle' fill='%23000'%3ED.S%3C/text%3E%3C/svg%3E">
<link rel="preload" href="assets/fonts/nats.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<script>if('scrollRestoration' in history)history.scrollRestoration='manual';</script>
</head>
<body class="work-page">

<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="logo" href="index.html">D. S.</a>
    <nav class="nav">
      <a href="work.html" aria-current="page">Work</a>
      <a href="index.html#about">About</a>
      <a href="index.html#contact">Contact</a>
    </nav>
  </div>
</header>

<main class="w-main">
  <div class="wrap">
    <h1 class="name">Daria Slavkova</h1>
{chr(10).join(blocks)}
  </div>
</main>

<footer class="site-footer site-footer--dark">
  <div class="wrap">
    <div class="foot-row foot-row--top">
      <span>Daria Slavkova</span>
      <span>Makeup and hair artist</span>
      <span>Worldwide</span>
    </div>
    <div class="foot-row foot-row--links">
      <a href="mailto:dariawacc1@gmail.com">Email<br>dariawacc1@gmail.com</a>
      <a href="https://instagram.com/deardarla.mua" target="_blank" rel="noopener">Insta<br>@deardarla.mua</a>
      <span>WeChat<br>Sdarcy002</span>
    </div>
    <div class="initials" aria-hidden="true"><span>D</span><span>.</span><span>S</span></div>
  </div>
</footer>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer" hidden>
  <button class="lb-btn lb-close" type="button" aria-label="Close">&times;</button>
  <button class="lb-btn lb-prev" type="button" aria-label="Previous">&#8249;</button>
  <button class="lb-btn lb-next" type="button" aria-label="Next">&#8250;</button>
  <img class="lb-img" id="lbImg" alt="">
  <p class="lb-count" id="lbCount"></p>
</div>

<script src="assets/js/main.js"></script>
</body>
</html>
'''
open('work.html', 'w').write(page)
print('work.html:', len(page), 'bytes |', shot, 'photos |',
      sum(1 for b in data if b['type'] == 'pair'), 'pairs')
