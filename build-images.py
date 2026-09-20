#!/usr/bin/env python3
"""Пересборка картинок из figma/raw в assets/img с кропом по imageTransform макета."""
import json, os, glob, concurrent.futures
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None

nodes = json.load(open('figma/nodes.json'))['nodes']
items = []
def walk(n, path=''):
    for f in (n.get('fills') or []):
        if f.get('type') == 'IMAGE' and f.get('imageRef'):
            bb = n.get('absoluteBoundingBox') or {}
            items.append(dict(path=path, name=n['name'], type=n['type'], ref=f['imageRef'],
                              mode=f.get('scaleMode'), tr=f.get('imageTransform'),
                              x=bb.get('x'), y=bb.get('y')))
    for c in n.get('children', []):
        walk(c, path + '/' + n['name'])
for v in nodes.values():
    walk(v['document'])

hero = [i for i in items if 'Hero' in i['path']][0]
portrait = [i for i in items if 'Image and bio' in i['path']][0]
grid = sorted([i for i in items if '/Images' in i['path'] and i['type'] == 'RECTANGLE'],
              key=lambda i: (round(i['y'] / 60), i['x']))

def load(src):
    return ImageOps.exif_transpose(Image.open(src)).convert('RGB')

def crop_by_transform(im, tr):
    """imageTransform = [[sx,0,tx],[0,sy,ty]] в долях исходника."""
    if not tr:
        return im
    w, h = im.size
    sx, tx = tr[0][0], tr[0][2]
    sy, ty = tr[1][1], tr[1][2]
    box = (round(tx * w), round(ty * h), round((tx + sx) * w), round((ty + sy) * h))
    box = (max(0, box[0]), max(0, box[1]), min(w, box[2]), min(h, box[3]))
    return im.crop(box)

def square(im):
    w, h = im.size
    s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))

def out(im, dst, maxside, q=80):
    w, h = im.size
    if max(w, h) > maxside:
        r = maxside / max(w, h)
        im = im.resize((round(w * r), round(h * r)), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=q, method=6)
    return f'{im.size[0]}x{im.size[1]} {os.path.getsize(dst)//1024}KB'

os.makedirs('assets/img', exist_ok=True)
log = []
log.append(('hero.webp', out(crop_by_transform(load('figma/raw/hero.png'), hero['tr']), 'assets/img/hero.webp', 2000, 82)))
log.append(('portrait.webp', out(square(load('figma/raw/portrait.png')), 'assets/img/portrait.webp', 1000, 84)))

def do_grid(k):
    i, g = k
    n = f'g{i+1:02d}'
    im = crop_by_transform(load(f'figma/raw/{n}.png'), g['tr'])
    a = out(im, f'assets/img/{n}.webp', 560, 80)
    b = out(im, f'assets/img/{n}-full.webp', 1500, 82)
    return (n, g['name'], a, b)

with concurrent.futures.ThreadPoolExecutor(6) as ex:
    rows = list(ex.map(do_grid, enumerate(grid)))
for r in rows:
    log.append((r[0], f'{r[1]} | thumb {r[2]} | full {r[3]}'))
for a, b in log:
    print(a, '->', b)
