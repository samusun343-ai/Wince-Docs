#!/usr/bin/env python3
"""Supplement: the CE 6.0 doc tree keeps the Keyboard Reference under a TOC
node the gwes inventory walker missed. Harvest those pages from the doc
index and append them to the winuser area facts file.
"""
import concurrent.futures as cf
import gzip
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from harvest_facts import BASE, fetch, parse

REPO = os.path.dirname(HERE)
IDX = f'{REPO}/data/mslearn-doc-index/ce60-doc-index.json.gz'
OUT = f'{REPO}/data/mslearn-facts/ce50-ce60-winuser-facts.json'

idx = json.load(gzip.open(IDX, 'rt', encoding='utf-8'))
kb = [e for e in idx if 'Keyboard Reference' in e.get('p', [])]
print('ce60 keyboard pages to harvest:', len(kb))

facts = json.load(open(OUT))
have = {(r['docset'], r['name']) for r in facts}
# also skip names already present from the ce50 keyboard harvest
ce50_names = {r['name'] for r in facts if r['docset'] == 'ce50'}


def work(e):
    url = BASE + e['u']
    html = fetch(url)
    if len(html) < 5000:
        html = fetch(url)
    if len(html) < 5000:
        return None
    rec = parse(html, url, 'ce60', e['t'])
    rec['area'] = 'gwes'
    rec['sub'] = '/'.join(e.get('p', [])[-1:])
    return rec


with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for rec in ex.map(work, kb):
        if rec and ('ce60', rec['name']) not in have:
            facts.append(rec)
            have.add(('ce60', rec['name']))

facts.sort(key=lambda r: (r['docset'], r.get('sub', ''), r['name']))
json.dump(facts, open(OUT, 'w'), ensure_ascii=False, indent=1)
print('winuser facts now:', len(facts))
