#!/usr/bin/env python3
"""Extract documented flag/metric tables from specific CE function pages
(GetSystemMetrics SM_ set, SetWindowPos SWP_ set, ShowWindow SW_ set).
Merges results into data/mslearn-facts/ce-style-tables.json as extra pages."""
import json
import re
import subprocess
import datetime

REPO = '/home/z/my-project/repos/Wince-Docs'
PATH = f'{REPO}/data/mslearn-facts/ce-style-tables.json'
TODAY = datetime.date.today().isoformat()

PAGES = ['GetSystemMetrics', 'SetWindowPos', 'ShowWindow', 'MessageBox',
         'CreateWindow', 'GetWindowLong', 'SetWindowLong']

facts = json.load(open(f'{REPO}/data/mslearn-facts/ce50-ce60-winuser-facts.json'))
sel = [r for r in facts if r['name'] in PAGES]


def textify(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    return re.sub(r'\s+', ' ', s).strip()


def parse_tables(html):
    out = []
    for t in re.findall(r'<table[^>]*>(.*?)</table>', html, re.S):
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
            cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.S)
            cells = [textify(c) for c in cells]
            if not cells:
                continue
            m = re.match(r'^([A-Z][A-Z0-9_]{2,})$', cells[0])
            if not m:
                continue
            desc = cells[1] if len(cells) > 1 else ''
            d = re.split(r'(?<=[\.\!\?])\s+', desc)[0][:220]
            out.append({'name': m.group(1), 'desc': d})
    return out


data = json.load(open(PATH))
existing = {(p['docset'], p['page']) for p in data['pages']}
for r in sorted(sel, key=lambda x: (x['docset'], x['name'])):
    key = (r['docset'], r['name'])
    if key in existing:
        continue
    html = subprocess.run(['curl', '-sL', '--max-time', '60', r['url']],
                          capture_output=True, text=True).stdout
    consts = parse_tables(html)
    data['pages'].append({'page': r['name'], 'docset': r['docset'], 'url': r['url'],
                          'retrieved': TODAY, 'constants': consts})
    print(f"{r['docset']} {r['name']}: {len(consts)} table constants")

# raster operation code pages (GDI area) — name sets, boolean forms documented
gdi = json.load(open(f'{REPO}/data/mslearn-facts/ce50-ce60-gdi-facts.json'))
for r in sorted(gdi, key=lambda x: (x['docset'], x['name'])):
    if r.get('sub') != 'Raster Operation Codes':
        continue
    key = (r['docset'], r['name'])
    if key in existing:
        continue
    html = subprocess.run(['curl', '-sL', '--max-time', '60', r['url']],
                          capture_output=True, text=True).stdout
    consts = parse_tables(html)
    data['pages'].append({'page': r['name'], 'docset': r['docset'], 'url': r['url'],
                          'retrieved': TODAY, 'constants': consts})
    print(f"{r['docset']} {r['name']}: {len(consts)} raster-op names")

json.dump(data, open(PATH, 'w'), ensure_ascii=False, indent=1)
print('total pages now:', len(data['pages']))
