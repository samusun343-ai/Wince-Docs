#!/usr/bin/env python3
"""Repository validator: schema, provenance and hygiene checks.

Usage: python3 tools/validate.py
Exits non-zero on any failure.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

FAIL = []

def err(msg):
    FAIL.append(msg)
    print('FAIL:', msg)

def ok(msg):
    print('ok  :', msg)

# ---------------------------------------------------------------- registry
REGISTRY_IDS = set()
AUDIT_FILES = {
    'mslearn-wince', 'mslearn-win32', 'microsoftdocs-win32', 'pinvoke-net',
    'mingw-org-w32api', 'mingw-w64', 'cegcc', 'wine-reactos', 'rejected-shared-source',
}

def load_registry():
    src = open(os.path.join(REPO, 'docs/02-sources/approved-sources.md')).read()
    ids = re.findall(r'^\| `([a-z0-9\-]+)` \|', src, re.M)
    REGISTRY_IDS.update(ids)
    # also ids referenced inside the reference table (cegcc, pinvoke-net, wine, reactos)
    for extra in ['cegcc', 'pinvoke-net', 'wine', 'reactos']:
        REGISTRY_IDS.add(extra)
    if len(REGISTRY_IDS) < 10:
        err(f'registry parse suspicious: only {len(REGISTRY_IDS)} ids')
    else:
        ok(f'registry ids parsed: {len(REGISTRY_IDS)}')

def check_audits():
    for a in AUDIT_FILES:
        p = os.path.join(REPO, f'docs/02-sources/audits/{a}.md')
        if not os.path.exists(p):
            err(f'missing audit file: {a}.md')
    ok(f'audit files present: {len(AUDIT_FILES)}')

# ---------------------------------------------------------------- fact YAML
try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False
    print('warn: PyYAML not installed — YAML checks skipped (pip install pyyaml)')

REQUIRED_FIELDS = {'id', 'kind', 'class', 'status', 'introduced', 'target_header', 'src'}
VALID_CLASS = {'common', 'ce-modified', 'ce-only'}
VALID_STATUS = {'verified', 'verify-runtime', 'open', 'quarantine'}

def check_facts():
    if not HAVE_YAML:
        return
    all_ids = []
    for path in sorted(glob.glob(os.path.join(REPO, 'data/facts/*.yaml'))):
        docs = yaml.safe_load(open(path))
        if not isinstance(docs, list):
            err(f'{path}: not a list')
            continue
        for rec in docs:
            rid = rec.get('id', '?')
            missing = REQUIRED_FIELDS - set(rec.keys())
            if missing:
                err(f'{path} [{rid}]: missing fields {sorted(missing)}')
            if rec.get('class') not in VALID_CLASS:
                err(f'{path} [{rid}]: bad class {rec.get("class")}')
            if rec.get('status') not in VALID_STATUS:
                err(f'{path} [{rid}]: bad status {rec.get("status")}')
            srcs = rec.get('src') or []
            if not srcs:
                err(f'{path} [{rid}]: empty src')
            for s in srcs:
                if s not in REGISTRY_IDS:
                    err(f'{path} [{rid}]: unknown source id "{s}"')
            all_ids.append(rid)
        ok(f'{os.path.basename(path)}: {len(docs)} records')
    if len(all_ids) != len(set(all_ids)):
        dupes = [i for i in all_ids if all_ids.count(i) > 1]
        err(f'duplicate fact ids: {sorted(set(dupes))}')
    else:
        ok(f'fact ids unique: {len(all_ids)}')

# ---------------------------------------------------------------- harvested JSON
def check_harvested():
    for path in sorted(glob.glob(os.path.join(REPO, 'data/mslearn-facts/*.json'))):
        try:
            d = json.load(open(path))
        except Exception as e:
            err(f'{path}: JSON parse error {e}')
            continue
        if isinstance(d, dict):  # system errors envelope
            errs = d.get('errors')
            if not errs or not d.get('url') or not d.get('retrieved'):
                err(f'{path}: envelope missing url/retrieved/errors')
                continue
            names = [e['name'] for e in errs]
            if len(names) != len(set(names)):
                err(f'{path}: duplicate error names')
            bad = [e for e in errs if not e['name'].startswith('ERROR_') or not isinstance(e['code'], int)]
            if bad:
                err(f'{path}: {len(bad)} malformed error records')
            ok(f'{os.path.basename(path)}: {len(errs)} error codes, range 0..{max(e["code"] for e in errs)}')
        else:  # fact records list
            for rec in d:
                for f in ('name', 'url', 'retrieved', 'requirements'):
                    if f not in rec:
                        err(f'{path} [{rec.get("name","?")}]: missing {f}')
                if not rec.get('signature'):
                    err(f'{path} [{rec.get("name","?")}]: missing signature')
            ok(f'{os.path.basename(path)}: {len(d)} records')

def check_error_tables():
    p6 = os.path.join(REPO, 'data/mslearn-facts/ce60-system-errors.json')
    p5 = os.path.join(REPO, 'data/mslearn-facts/ce50-system-errors.json')
    if os.path.exists(p6) and os.path.exists(p5):
        e6 = {e['name']: e['code'] for e in json.load(open(p6))['errors']}
        e5 = {e['name']: e['code'] for e in json.load(open(p5))['errors']}
        if len(e6) != 571:
            err(f'ce60 error count {len(e6)} != 571 (spec claims 571)')
        if len(e5) != 570:
            err(f'ce50 error count {len(e5)} != 570 (spec claims 570)')
        if set(e6) - set(e5) != {'ERROR_DEVICE_REMOVED'}:
            err(f'ce60-ce5 error delta unexpected: {sorted(set(e6)-set(e5))[:5]}')
        if set(e5) - set(e6):
            err('ce5 has codes absent from ce6 (spec claims none)')
        valdiff = [n for n in set(e5) & set(e6) if e5[n] != e6[n]]
        if valdiff:
            err(f'value differences between ce5/ce6: {valdiff[:5]}')
        ok('error tables consistent with spec-winerror.md claims')

# ---------------------------------------------------------------- indexes
def check_indexes():
    for s, n in [('ce60', 23713), ('ce50', 22889), ('ce40', 6362)]:
        p = os.path.join(REPO, f'data/mslearn-doc-index/{s}-doc-index.json.gz')
        if not os.path.exists(p):
            err(f'missing gz snapshot: {s}')
            continue
        import gzip
        d = json.load(gzip.open(p, 'rt', encoding='utf-8'))
        if len(d) != n:
            err(f'{s} index count {len(d)} != documented {n}')
        ok(f'{s}-doc-index.json.gz: {len(d)} pages')
    for s in ('ce60', 'ce50'):
        for a in ('core-os', 'file-io', 'gwes', 'winsock'):
            p = os.path.join(REPO, f'data/mslearn-inventories/{s}/{a}.json')
            if not os.path.exists(p):
                err(f'missing inventory {s}/{a}')
    ok('inventories present')

# ---------------------------------------------------------------- hygiene
def check_hygiene():
    bad_pat = re.compile(r'\b(TODO|TBD|XXX)\b')  # case-sensitive, whole-word
    for path in glob.glob(os.path.join(REPO, 'docs/**/*.md'), recursive=True) + \
               glob.glob(os.path.join(REPO, '*.md')) + \
               glob.glob(os.path.join(REPO, 'data/facts/*.yaml')):
        try:
            txt = open(path, encoding='utf-8').read()
        except Exception:
            continue
        clean = re.sub(r'`[^`]*`', '``', txt)  # ignore inline code spans (id patterns etc.)
        for m in bad_pat.finditer(clean):
            frag = clean[max(0, m.start()-30):m.end()+30].replace('\n', ' ')
            err(f'placeholder in {os.path.relpath(path, REPO)}: …{frag}…')
    ok('placeholder scan done')

def check_links_local():
    """Every audit file referenced from approved-sources must exist."""
    src = open(os.path.join(REPO, 'docs/02-sources/approved-sources.md')).read()
    for m in re.finditer(r'\((audits/[a-z\-]+\.md)\)', src):
        if not os.path.exists(os.path.join(REPO, 'docs/02-sources', m.group(1))):
            err(f'broken audit link: {m.group(1)}')
    ok('audit links resolve')

def main():
    print(f'validating {REPO}\n' + '-' * 60)
    load_registry()
    check_audits()
    check_facts()
    check_harvested()
    check_error_tables()
    check_indexes()
    check_hygiene()
    check_links_local()
    print('-' * 60)
    if FAIL:
        print(f'FAILED with {len(FAIL)} problem(s)')
        sys.exit(1)
    print('ALL CHECKS PASSED')

if __name__ == '__main__':
    main()
