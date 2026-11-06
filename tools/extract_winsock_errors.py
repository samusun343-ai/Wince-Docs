#!/usr/bin/env python3
"""Extract the documented Winsock Error Codes table (WSAE*) from the CE docs.
The page lists Value | Name | Description — a Class A statement of the numeric
value, so these constants reach 'verified' on their own.

Output: data/mslearn-facts/ce{50,60}-winsock-errors.json
"""
import json
import re
import subprocess
import datetime

REPO = '/home/z/my-project/repos/Wince-Docs'
TODAY = datetime.date.today().isoformat()

facts = json.load(open(f'{REPO}/data/mslearn-facts/ce50-ce60-winsock-facts.json'))
sel = [r for r in facts if r['name'] == 'Winsock Error Codes']


def textify(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    return re.sub(r'\s+', ' ', s).strip()


for r in sel:
    html = subprocess.run(['curl', '-sL', '--max-time', '60', r['url']],
                          capture_output=True, text=True).stdout
    errors = []
    for t in re.findall(r'<table[^>]*>(.*?)</table>', html, re.S):
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
            cells = [textify(c) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.S)]
            if len(cells) < 2:
                continue
            vm = re.match(r'^(\d+)$', cells[0])
            nm = re.match(r'^(WSAE\w+)$', cells[1])
            if vm and nm:
                desc = re.split(r'(?<=[\.\!\?])\s+', cells[2])[0][:200] if len(cells) > 2 else ''
                errors.append({'name': nm.group(1), 'code': int(vm.group(1)), 'desc': desc})
    out = {'url': r['url'], 'retrieved': TODAY, 'errors': errors}
    path = f"{REPO}/data/mslearn-facts/{r['docset']}-winsock-errors.json"
    json.dump(out, open(path, 'w'), ensure_ascii=False, indent=1)
    print(f"{r['docset']}: {len(errors)} winsock error codes -> {path.split('/')[-1]}")
