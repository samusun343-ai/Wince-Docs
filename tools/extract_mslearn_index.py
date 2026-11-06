#!/usr/bin/env python3
"""Extract the full leaf-page index for each Windows CE documentation set
from the MS Learn previous-versions TOC.

Usage:
  curl -s "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/toc.json" \\
      -o /tmp/embedded-root-toc.json
  python3 tools/extract_mslearn_index.py [--root /tmp/embedded-root-toc.json]

Writes: data/mslearn-doc-index/<set>-doc-index.json (+ .gz snapshots)
Record: { "t": title, "u": relative-href, "p": [toc-path...] }
"""
import json, os, re, sys, gzip

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUTDIR = os.path.join(REPO, 'data', 'mslearn-doc-index')

def children(node):
    return node.get('children') or []

def title(node):
    return node.get('toc_title') or '?'

def href(node):
    return node.get('href') or ''

def index_leaves(node, path, out):
    kids = children(node)
    if not kids:
        h = href(node)
        if h:
            out.append({'t': title(node), 'u': h, 'p': list(path)})
        return
    for c in kids:
        index_leaves(c, path + [title(node)], out)

def main():
    root_json = sys.argv[sys.argv.index('--root') + 1] if '--root' in sys.argv else '/tmp/embedded-root-toc.json'
    with open(root_json) as f:
        d = json.load(f)

    compact = None
    for top in d.get('items', []):
        if title(top) == 'Windows Embedded':
            for c in children(top):
                if title(c) == 'Windows Embedded Compact':
                    compact = c
    if compact is None:
        sys.exit('Windows Embedded Compact node not found in TOC')

    sets = {
        'ce60': r'^Windows Embedded CE 6\.0$',
        'ce50': r'^Windows CE 5\.0$',
        'ce40': r'^Windows CE \.NET$',
        'ce30': r'^Windows CE 3\.0$',
        'wec2013': r'^Windows Embedded Compact 2013$',
        'wec7': r'^Windows Embedded Compact 7$',
    }
    os.makedirs(OUTDIR, exist_ok=True)
    stats = {}
    for key, pat in sets.items():
        target = None
        for c in children(compact):
            if re.search(pat, title(c)):
                target = c
                break
        if target is None:
            print(f'!! {key}: not found in TOC')
            continue
        out = []
        index_leaves(target, [], out)
        seen = set()
        uniq = []
        for e in out:
            if e['u'] in seen:
                continue
            seen.add(e['u'])
            uniq.append(e)
        path = os.path.join(OUTDIR, f'{key}-doc-index.json')
        with open(path, 'w') as f:
            json.dump(uniq, f, ensure_ascii=False, separators=(',', ':'))
        with gzip.open(path + '.gz', 'wt', encoding='utf-8') as f:
            json.dump(uniq, f, ensure_ascii=False, separators=(',', ':'))
        stats[key] = len(uniq)
        print(f'{key}: {len(uniq)} unique leaf pages -> {os.path.basename(path)}')
    with open(os.path.join(OUTDIR, 'stats.json'), 'w') as f:
        json.dump({'retrieved': 'auto', 'counts': stats}, f, indent=1)
    print('stats.json written (update the retrieved date in data/README.md if counts changed)')

if __name__ == '__main__':
    main()
