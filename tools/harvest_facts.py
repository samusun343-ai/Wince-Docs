#!/usr/bin/env python3
"""Harvest structured facts from MS Learn Windows CE doc pages.

Usage: python3 tools/harvest_facts.py [ce60] [ce50] ...
Writes: data/mslearn-facts/<set>-core-facts.json

Each record: name/title/docset/url/retrieved/signature/code_blocks/
             requirements{os,header,library}/ce_notes_excerpt
"""
import json, os, re, subprocess, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUTDIR = os.path.join(REPO, 'data', 'mslearn-facts')
BASE = 'https://learn.microsoft.com/en-us/previous-versions/windows/embedded/'
TODAY = datetime.date.today().isoformat()

PAGES = {
    'ce60': {
        'CreateProcess': 'ee488927', 'CreateThread': 'ee488162', 'OpenProcess': 'ee488418',
        'TerminateProcess': 'ee488378', 'VirtualAlloc': 'ee488564', 'LocalAlloc': 'ee487963',
        'HeapCreate': 'ee488381', 'WaitForSingleObject': 'ee488762', 'WaitForMultipleObjects': 'ee487972',
        'CreateEvent': 'ee488008', 'CreateMutex': 'ee488798', 'GetVersionEx': 'ee488165',
        'OSVERSIONINFO': 'ee488619', 'GetSystemInfo': 'ee488900', 'SYSTEM_INFO': 'ee488780',
        'GetLastError': 'ee488182', 'SetLastError': 'ee487957', 'Sleep': 'ee488158',
        'LoadLibrary': 'ee488148', 'GetProcAddress': 'ee488623', 'CreateFile': 'ee490417',
        'ReadFile': 'ee489594', 'WriteFile': 'ee490774', 'CloseHandle': 'ee490442',
        'FindFirstFile': 'ee489744', 'MessageBox': 'ee503608', 'CreateWindow': 'ee500617',
        'RegisterClass': 'ee506270', 'DefWindowProc': 'ee503409', 'GetMessage': 'ee503715',
        'WinMain': 'ee499679', 'PROCESS_INFORMATION': 'ee488245', 'WSAStartup': 'ee495252',
    },
    'ce50': {
        'CreateProcess': 'ms885182', 'CreateThread': 'ms885186', 'VirtualAlloc': 'aa450975',
        'LocalAlloc': 'ms886739', 'HeapCreate': 'ms885656', 'WaitForSingleObject': 'aa450988',
        'WaitForMultipleObjects': 'aa450987', 'CreateEvent': 'ms885177', 'CreateMutex': 'ms885181',
        'GetVersionEx': 'ms885648', 'OSVERSIONINFO': 'ms886768', 'GetSystemInfo': 'ms885638',
        'SYSTEM_INFO': 'aa450921', 'GetLastError': 'ms885627', 'SetLastError': 'ms886817',
        'Sleep': 'aa450900', 'LoadLibrary': 'ms886736', 'GetProcAddress': 'ms885634',
        'CreateFile': 'aa517318', 'ReadFile': 'ms891445', 'WriteFile': 'ms892380',
        'CloseHandle': 'aa517300', 'FindFirstFile': 'ms889678', 'MessageBox': 'ms911827',
        'CreateWindow': 'ms908192', 'RegisterClass': 'ms913089', 'DefWindowProc': 'aa452929',
        'GetMessage': 'aa453135', 'WinMain': 'ms914104', 'PROCESS_INFORMATION': 'ms886775',
        'WSAStartup': 'ms898774',
    },
}

CE_KEYWORDS = re.compile(
    r'(Windows CE|Windows Embedded CE|object store|is not supported|are not supported|'
    r'is unsupported|must be (NULL|set to NULL)|is ignored|are ignored|does not support|'
    r'do not support|Unicode|ANSI|differs from the desktop|desktop Windows|'
    r'In Windows Embedded CE|In Windows CE|only the Unicode)', re.I)

def fetch(url):
    r = subprocess.run(['curl', '-sL', '--max-time', '60', url], capture_output=True, text=True)
    return r.stdout

def textify(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def unescape_md(s):
    return s.replace('\\(', '(').replace('\\)', ')').replace('\\_', '_').replace('\\*', '*')

def parse(html, url, docset, name):
    m = re.search(r'<main[^>]*>(.*?)</main>', html, re.S)
    main = m.group(1) if m else html
    tm = re.search(r'<h1[^>]*>(.*?)</h1>', main, re.S)
    title = textify(tm.group(1)) if tm else name
    codes = [unescape_md(textify(c.group(1))) for c in re.finditer(r'<pre[^>]*>(.*?)</pre>', main, re.S)]
    req = {}
    rm = re.search(r'Requirements(.{0,3000})', main, re.S)
    if rm:
        seg = textify(rm.group(1))
        hm = re.search(r'Header\s*[:\s]*([\w\.\-]+(?:\s*,\s*[\w\.\-]+)*)', seg)
        lm = re.search(r'(?:Link )?Library\s*[:\s]*([\w\.\-]+)', seg)
        om = re.search(r'(?:OS Versions|Windows Embedded CE|Windows CE)\s*[:\s]*(.*?)(?:See Also|Header|$)', seg)
        if hm: req['header'] = hm.group(1).strip().rstrip('.')
        if lm: req['library'] = lm.group(1).strip().rstrip('.')
        if om: req['os'] = om.group(1).strip()[:120]
    remarks = ''
    rmm = re.search(r'Remarks(.*?)(?:Requirements|See Also|</main>|$)', main, re.S)
    if rmm:
        body = textify(rmm.group(1))
        sents = re.split(r'(?<=[\.\!\?])\s+', body)
        keep = [s for s in sents if CE_KEYWORDS.search(s)]
        remarks = ' '.join(keep)[:900]
    return {
        'name': name, 'title': title, 'docset': docset, 'url': url, 'retrieved': TODAY,
        'signature': codes[0] if codes else None,
        'code_blocks': codes[:6],
        'requirements': req,
        'ce_notes_excerpt': remarks,
    }

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    which = sys.argv[1:] or list(PAGES)
    for docset in which:
        pages = PAGES[docset]
        suffix = '(v=winembedded.60)' if docset == 'ce60' else '(v=msdn.10)'
        recs = []
        for name, slug in pages.items():
            url = BASE + slug + suffix
            html = fetch(url)
            if len(html) < 5000:
                print(f'!! {docset} {name}: fetch failed ({len(html)} bytes)')
                continue
            recs.append(parse(html, url, docset, name))
            print(f'OK {docset} {name}')
        out = os.path.join(OUTDIR, f'{docset}-core-facts.json')
        with open(out, 'w') as f:
            json.dump(recs, f, ensure_ascii=False, indent=1)
        print(f'== {docset}: {len(recs)} records -> {os.path.basename(out)}')

if __name__ == '__main__':
    main()
