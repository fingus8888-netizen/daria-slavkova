#!/usr/bin/env python3
"""Разбор листа /work: пары снимков, подписи, разделы -> картинки + work-data.json"""
import json, os, re, urllib.request, concurrent.futures
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None

doc = json.load(open('figma/work.json'))['nodes']['1:172']['document']
fills = json.load(open('figma/fills.json'))['meta']['images']

SECTION_TITLES = {'selected work', 'art', 'clients makeup', 'runway , backstage'}

pairs, notes = [], []  # пары снимков и подписи между ними
def walk(n):
    if n['type'] == 'FRAME' and n['name'].startswith('Project item'):
        imgs = []
        def pick(m):
            for f in (m.get('fills') or []):
                if f.get('type') == 'IMAGE' and f.get('imageRef'):
                    imgs.append((f['imageRef'], f.get('imageTransform'), m['name']))
            for c in m.get('children', []): pick(c)
        pick(n)
        bb = n.get('absoluteBoundingBox') or {}
        if imgs: pairs.append(dict(kind='pair', y=bb.get('y', 0), imgs=imgs, name=n['name']))
        return
    if n['type'] == 'TEXT':
        txt = re.sub(r'[ \t]+', ' ', n.get('characters', '')).strip()
        bb = n.get('absoluteBoundingBox') or {}
        st = n.get('style', {})
        if txt and st.get('fontSize', 0) >= 20 and n['name'] not in ('Daria slavkova', 'D. S', 'A', '.', 'D'):
            notes.append(dict(kind='text', y=bb.get('y', 0), text=txt))
        return
    for c in n.get('children', []): walk(c)

for c in doc['children'][0]['children']:          # внутри Desktop
    if c['name'] in ('Header Navigation', 'Footer'): continue
    walk(c)

feed = sorted(pairs + notes, key=lambda i: i['y'])

out = feed

# --- скачиваем и режем ---
os.makedirs('figma/raw/work', exist_ok=True)
os.makedirs('assets/img/work', exist_ok=True)

def crop(im, tr):
    if not tr: return im
    w, h = im.size
    sx, tx, sy, ty = tr[0][0], tr[0][2], tr[1][1], tr[1][2]
    box = (max(0, round(tx*w)), max(0, round(ty*h)), min(w, round((tx+sx)*w)), min(h, round((ty+sy)*h)))
    return im.crop(box)

def fetch(ref):
    p = f'figma/raw/work/{ref}.img'
    if not os.path.exists(p):
        urllib.request.urlretrieve(fills[ref], p)
    return p

def make(job):
    idx, ref, tr = job
    src = fetch(ref)
    im = crop(ImageOps.exif_transpose(Image.open(src)).convert('RGB'), tr)
    w, h = im.size
    r = 1300 / max(w, h)
    if r < 1: im = im.resize((round(w*r), round(h*r)), Image.LANCZOS)
    dst = f'assets/img/work/w{idx:02d}.webp'
    im.save(dst, 'WEBP', quality=80, method=6)
    im2 = im.copy(); im2.thumbnail((760, 760), Image.LANCZOS)
    im2.save(dst.replace('.webp', '-s.webp'), 'WEBP', quality=78, method=6)
    return dst, im.size, os.path.getsize(dst)//1024

data, jobs, idx = [], [], 0
for item in out:
    if item['kind'] == 'text':
        t = item['text']
        data.append({'type': 'section' if t.lower() in SECTION_TITLES or '\n' in t else 'credit',
                     'text': t})
    else:
        shots = []
        for ref, tr, nm in item['imgs']:
            idx += 1
            jobs.append((idx, ref, tr))
            shots.append(f'assets/img/work/w{idx:02d}.webp')
        data.append({'type': 'pair', 'images': shots})

with concurrent.futures.ThreadPoolExecutor(6) as ex:
    for d, size, kb in ex.map(make, jobs): print(d, size, f'{kb}KB')

json.dump(data, open('work-data.json', 'w'), ensure_ascii=False, indent=1)
print('\nfeed:', len(data), 'blocks |', sum(1 for d in data if d['type']=='pair'), 'pairs |',
      idx, 'images | sections:', [d['text'] for d in data if d['type']=='section'])
