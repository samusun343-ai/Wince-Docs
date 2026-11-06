#!/usr/bin/env python3
"""Area-scoped mass harvester: pulls every page of selected inventory areas.

Usage:
  python3 tools/harvest_area.py <docset>:<area> [<docset>:<area> ...]
      [--sub REGEX] [--out NAME] [--workers N] [--limit N]

Example:
  python3 tools/harvest_area.py ce60:window-control ce50:window-control
  python3 tools/harvest_area.py ce60:common-controls --out ce60-commctrl-ce \
      --sub '^(Command Bands|Command Bars|Common Control|Common Dialog Boxes) Reference$'

Reads data/mslearn-inventories/<docset>/<area>.json, fetches each page
(threads, curl, one retry), parses with the shared audited parser from
harvest_facts.py, and writes data/mslearn-facts/<NAME>-facts.json.

Record = harvest_facts record + area + sub. Records whose page has no
<pre> block keep signature=None (counted in the summary; the validator
treats area files as inventory-grade, not curated-grade).
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from harvest_facts import BASE, fetch, parse  # shared, audited parser

REPO = os.path.dirname(HERE)
INV = os.path.join(REPO, 'data', 'mslearn-inventories')
OUT = os.path.join(REPO, 'data', 'mslearn-facts')

print_lock = threading.Lock()
stats = {'ok': 0, 'retry_ok': 0, 'fail': 0, 'no_sig': 0}


def fetch_retry(url):
    html = fetch(url)
    if len(html) < 5000:
        html = fetch(url)  # one retry
    return html


def worker(entry, docset):
    url = BASE + entry['u']
    html = fetch_retry(url)
    if len(html) < 5000:
        with print_lock:
            stats['fail'] += 1
            print(f'!! {docset} {entry["t"]}: fetch failed ({len(html)} bytes)', flush=True)
        return None
    try:
        rec = parse(html, url, docset, entry['t'])
    except Exception as e:  # defensive: never lose the run for one page
        with print_lock:
            stats['fail'] += 1
            print(f'!! {docset} {entry["t"]}: parse error {e}', flush=True)
        return None
    rec['area'] = entry['area']
    rec['sub'] = entry['sub']
    if not rec.get('signature'):
        stats['no_sig'] += 1
    with print_lock:
        stats['ok'] += 1
        if stats['ok'] % 50 == 0:
            print(f'   ... {stats["ok"]} pages parsed', flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('specs', nargs='+', help='docset:area pairs')
    ap.add_argument('--sub', default=None, help='regex filter on subarea title')
    ap.add_argument('--out', default=None, help='output basename (default <docset>-<area>)')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--limit', type=int, default=0, help='cap pages (smoke test)')
    args = ap.parse_args()

    sub_re = re.compile(args.sub) if args.sub else None
    entries = []
    for spec in args.specs:
        docset, area = spec.split(':', 1)
        path = os.path.join(INV, docset, f'{area}.json')
        data = json.load(open(path))
        sel = [e for e in data if not sub_re or sub_re.search(e['sub'])]
        entries.extend((docset, e) for e in sel)
        print(f'{spec}: {len(sel)}/{len(data)} pages selected')
    if args.limit:
        entries = entries[:args.limit]

    records = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(worker, e, ds) for ds, e in entries]
        for f in cf.as_completed(futs):
            r = f.result()
            if r:
                records.append(r)

    # stable order: docset, subarea, name
    records.sort(key=lambda r: (r['docset'], r.get('sub', ''), r['name']))

    docsets = sorted({ds for ds, _ in entries})
    default = '-'.join(docsets) if len(docsets) > 1 else docsets[0]
    area0 = entries[0][1]['area']
    name = args.out or f'{default}-{area0}'
    out = os.path.join(OUT, f'{name}-facts.json')
    with open(out, 'w') as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    print(f'== {name}: {len(records)} records '
          f'(no-signature: {stats["no_sig"]}, failed: {stats["fail"]}) -> {os.path.basename(out)}')


if __name__ == '__main__':
    main()
