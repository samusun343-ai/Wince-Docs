#!/usr/bin/env python3
"""Extract the documented constant-name tables from the CE 'Window and Control
Styles' pages (they carry names + descriptions but no values).

Output: data/mslearn-facts/ce-style-tables.json
  {"pages": [{"page","docset","url","retrieved","constants":[{"name","desc"}]}]}

These name sets are the Class A record of *which* styles/messages the CE docs
document for the platform; numeric values come from the cross-check pipeline.
"""
import json
import os
import re
import subprocess
import datetime

REPO = '/home/z/my-project/repos/Wince-Docs'
OUT = os.path.join(REPO, 'data', 'mslearn-facts', 'ce-style-tables.json')
TODAY = datetime.date.today().isoformat()
BASE = 'https://learn.microsoft.com/en-us/previous-versions/windows/embedded/'

facts = json.load(open(os.path.join(REPO, 'data', 'mslearn-facts/ce50-ce60-winuser-facts.json')))
style_pages = [r for r in facts if r['sub'] == 'Window and Control Styles']


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
            # first sentence, capped
            d = re.split(r'(?<=[\.\!\?])\s+', desc)[0][:220]
            out.append({'name': m.group(1), 'desc': d})
    return out


pages = []
for r in sorted(style_pages, key=lambda x: (x['docset'], x['name'])):
    html = subprocess.run(['curl', '-sL', '--max-time', '60', r['url']],
                          capture_output=True, text=True).stdout
    consts = parse_tables(html)
    pages.append({'page': r['name'], 'docset': r['docset'], 'url': r['url'],
                  'retrieved': TODAY, 'constants': consts})
    print(f"{r['docset']} {r['name']}: {len(consts)} constants")

json.dump({'pages': pages}, open(OUT, 'w'), ensure_ascii=False, indent=1)
tot = sum(len(p['constants']) for p in pages)
print(f'== {len(pages)} pages, {tot} constant rows -> {os.path.basename(OUT)}')
