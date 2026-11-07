#!/usr/bin/env python3
"""Build curated API-documentation inventories from the doc indexes.

Usage: python3 tools/build_inventories.py
Reads:  data/mslearn-doc-index/<set>-doc-index.json
Writes: data/mslearn-inventories/<set>/<area>.json (+ _summary.json)
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
IDXDIR = os.path.join(REPO, 'data', 'mslearn-doc-index')
OUTDIR = os.path.join(REPO, 'data', 'mslearn-inventories')

AREAS = {
    'core-os': r'^(Core OS Reference|Core OS Services Reference)$',
    'file-io': r'^(File I/O Reference|File Systems and (Storage Management|Data Store) Reference)$',
    'gwes': r'^GWES Reference$',
    'gdi': r'^GDI Reference$',
    'window-control': r'^Window Control Reference$',
    'shell': r'^Shell Reference$',
    'winsock': r'^(Windows Sockets Reference|Winsock Reference)$',
    'common-controls': r'^Common Controls Reference$',
    'error-values': r'^(Error Values|Error Messages|System Errors.*)$',
    # ---- P3 additions (application-surface areas outside the original nine) ----
    'ole-com': r'^COM and DCOM Reference$',
    'security': r'^(Cryptography Reference|Certificates Reference|Credential Manager Reference|'
                r'Smart Card Reference|Authentication Services Reference|LASS Reference)$',
    'nls': r'^National Language Support \(NLS\) Reference$',
    'imm': r'^Input Method Manager \(IMM\) Reference$',
    'mui': r'^Multilingual User Interface \(MUI\) Reference$',
    'wininet': r'^WinInet Reference$',
    'urlmon': r'^(URL Moniker Services|URL Security Zones|Asynchronous Pluggable Protocols) Reference$',
    'obex': r'^OBEX Reference$',
    'rapi': r'^(RAPI|RAPI2) Reference$',
    'tapi': r'^TAPI Reference$',
    'ras': r'^RAS Reference$',
    'wnet': r'^Windows Networking API/Redirector Reference$',
    'tcpip': r'^TCP/IP Reference$',
    'ipv6': r'^IPv6 Application Development$',
    'audio': r'^(Waveform Audio Reference|Hardware Audio Mixer( Reference)?)$',
    'power': r'^Power Management Reference$',
    'connmgr': r'^Connection Manager Reference$',
    'bluetooth': r'^Bluetooth Reference$',
    'fonts': r'^Fonts Reference$',
    'kernel': r'^Kernel Reference$',
    'gps': r'^GPS Intermediate Driver Reference$',
    'snmp': r'^SNMP Reference$',
}

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for s in ['ce60', 'ce50', 'ce40']:
        src = os.path.join(IDXDIR, f'{s}-doc-index.json')
        if not os.path.exists(src):
            srcgz = src + '.gz'
            if not os.path.exists(srcgz):
                print(f'!! {s}: index missing, skipped')
                continue
            import gzip
            with gzip.open(srcgz, 'rt', encoding='utf-8') as f:
                d = json.load(f)
        else:
            with open(src) as f:
                d = json.load(f)
        os.makedirs(os.path.join(OUTDIR, s), exist_ok=True)
        summary = {}
        for area, rx in AREAS.items():
            recs = []
            for e in d:
                matched = None
                for i, seg in enumerate(e['p']):
                    if re.search(rx, seg):
                        matched = i
                        break
                if matched is None:
                    continue
                sub = e['p'][matched + 1] if len(e['p']) > matched + 1 else '(top)'
                recs.append({'area': area, 'sub': sub, 't': e['t'], 'u': e['u']})
            if recs:
                with open(os.path.join(OUTDIR, s, f'{area}.json'), 'w') as f:
                    json.dump(recs, f, ensure_ascii=False, indent=0)
                subs = {}
                for r in recs:
                    subs[r['sub']] = subs.get(r['sub'], 0) + 1
                summary[area] = {'pages': len(recs), 'subareas': subs}
                print(f'{s}/{area}: {len(recs)} pages, {len(subs)} subareas')
            else:
                print(f'{s}/{area}: (none)')
        with open(os.path.join(OUTDIR, s, '_summary.json'), 'w') as f:
            json.dump(summary, f, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
