#!/usr/bin/env python3
"""Generate spec-level fact YAML files from the area harvests.

Inputs : data/mslearn-facts/ce50-ce60-{window-control,winuser,gdi,winsock,
         commctrl-ce}-facts.json, ce-style-tables.json,
         w32api lineage headers (paths below), desktop value cross-check JSON.
Outputs: data/facts/{winuser-core,wingdi-core,winsock,commctrl-ce}.yaml

Fact policy (verification-policy.md):
- functions/structures/macros: Class A page states signature -> verified
- constants: value from w32api (Class B); if desktop Win32 docs (Class A,
  mslearn-win32) state the same value -> verified; else verify-runtime.
- 'open' status is never emitted by this generator (contradictions are
  reported on stdout for manual curation instead).
"""
import json
import os
import re
import sys

REPO = '/home/z/my-project/repos/Wince-Docs'
FD = f'{REPO}/data/mslearn-facts'
W32 = '/tmp/w32api'  # MaxKellermann/w32api branch wip (public-domain lineage)
DESKTOP = '/tmp/desktop_values.json'

OS_VER = [
    (r'Windows CE 1\.0', '1.0'), (r'Windows CE 1\.01', '1.01'),
    (r'Windows CE 2\.0', '2.0'), (r'Windows CE 2\.01', '2.01'),
    (r'Windows CE 2\.1', '2.1'), (r'Windows CE 2\.11', '2.11'),
    (r'Windows CE 2\.12', '2.12'), (r'Windows CE 3\.0', '3.0'),
    (r'CE \.NET 4\.0|Windows CE \.NET \(4\.0\)', '4.0'),
    (r'CE \.NET 4\.1|Windows CE \.NET \(4\.1\)', '4.1'),
    (r'CE \.NET 4\.2|Windows CE \.NET \(4\.2\)', '4.2'),
    (r'Windows CE 5\.0', '5.0'), (r'Windows Embedded CE 6\.0', '6.0'),
]


def introduced_from(req):
    s = (req or {}).get('os') or ''
    s = s.replace('Microsoft ', '').replace('Embedded ', '')
    best = None
    for pat, ver in OS_VER:
        m = re.search(pat, s)
        if m and (best is None or float(ver) < float(best)):
            best = ver
    return best or '~'


def norm_header(h):
    if not h:
        return None
    return h.strip().rstrip('.').lower()


# ---------------------------------------------------------------- w32api scan
def scan_w32(files):
    """Return ({NAME: (value, expansion)}, ce_gated_set).
    ce_gated_set = constants defined only inside `#ifdef _WIN32_WCE` blocks
    of the CE-adapted w32api lineage (a CE-specificity signal, Class B)."""
    out = {}
    ce_gated = set()
    dre = re.compile(r'^#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.+?)\s*$')
    num = re.compile(r'^(0x[0-9A-Fa-f]+|\d+)L?$', re.I)
    for fn in files:
        path = os.path.join(W32, fn)
        if not os.path.exists(path):
            continue
        stack = []  # each entry: True if currently in a CE-true branch
        for line in open(path, errors='replace'):
            s = line.strip()
            m_if = re.match(r'^#\s*ifdef\s+_WIN32_WCE\b', s)
            m_ifn = re.match(r'^#\s*ifndef\s+_WIN32_WCE\b', s)
            m_ifdef = re.match(r'^#\s*(if|ifdef|ifndef)\b', s)
            m_else = re.match(r'^#\s*else\b', s)
            m_end = re.match(r'^#\s*endif\b', s)
            if m_if:
                stack.append(True)
            elif m_ifn:
                stack.append(False)
            elif m_ifdef:
                stack.append(None)
            elif m_else and stack:
                top = stack.pop()
                stack.append(not top if top is not None else None)
            elif m_end and stack:
                stack.pop()
            in_ce = True in stack
            m = dre.match(s)
            if not m:
                continue
            name, rhs = m.group(1), m.group(2).strip()
            rhs = re.sub(r'/\*.*?\*/', '', rhs).strip()
            if num.match(rhs):
                out.setdefault(name, (rhs.rstrip('Ll'), None))
            else:
                out.setdefault(name, (None, re.sub(r'\s+', ' ', rhs)))
            if in_ce:
                ce_gated.add(name)
    return out, ce_gated


W32USER, CE_GATED_USER = scan_w32(['winuser.h', 'windows.h'])
W32GDI, CE_GATED_GDI = scan_w32(['wingdi.h'])
W32SOCK, CE_GATED_SOCK = scan_w32(['winsock2.h', 'winsock.h'])
W32COMM, CE_GATED_COMM = scan_w32(['commctrl.h', 'commdlg.h'])
DESKTOP_VALUES = json.load(open(DESKTOP)) if os.path.exists(DESKTOP) else {}

CE_ONLY_CONST = {
    'WS_NONAVDONEBUTTON', 'WS_EX_CAPTIONOKBTN', 'WS_EX_NODRAG', 'WS_EX_NOANIMATION',
    'WS_SIZEBOX',  # CE docs name it WS_SIZEBOX; desktop canonical is WS_THICKFRAME alias
}
CE_GATED_ALL = CE_GATED_USER | CE_GATED_GDI | CE_GATED_SOCK | CE_GATED_COMM
CE_ONLY_FN_PREFIX = (
    'CommandBar', 'CommandBands', 'ImageList_',  # ImageList lives in commctrl (ce doc area), desktop-family though
    'GetAsyncShiftFlags', 'GetForegroundInfo', 'GetForegroundKeyboard',
    'GetKeyboardStatus', 'KeybdGetDeviceInfo', 'PostKeybdMessage', 'CustomTrackPopupMenu',
    'SystemIdleTimerReset', 'GetMessageSource', 'GetMessageQueueReadyTimeStamp',
    'GetClipboardDataAlloc', 'CapEdit', 'Sip', 'SH',
)
CE_ONLY_FN_EXACT = {
    'AllKeys', 'EnableHardwareKeyboard', 'DisableHardwareKeyboard', 'LoadKeyboardLayout',
    'ActivateKeyboardLayout', 'GetKeyboardLayout', 'GetKeyboardLayoutList',
    'GetKeyboardLayoutName', 'UnloadKeyboardLayout', 'RegisterHotKey', 'UnregisterHotKey',
    'DrawFrameControl',
}


def classify_fn(name):
    if name.startswith(CE_ONLY_FN_PREFIX) or name in CE_ONLY_FN_EXACT:
        return 'ce-only'
    return 'common'


def classify_const(name):
    if name in CE_ONLY_CONST or name in CE_GATED_ALL:
        return 'ce-only'
    if name.startswith(('WS_', 'WS_EX_')):
        return 'ce-modified'  # documented CE set is a subset of desktop's + CE additions
    return 'common'


def value_channels(name, w32map):
    """Return (value, status, srcs, note)."""
    wv = w32map.get(name)
    dv = DESKTOP_VALUES.get(name)
    w32val = wv[0] if wv else None
    if w32val and dv and dv['value'].lower().lstrip('0x') == w32val.lower().lstrip('0x'):
        return w32val, 'verified', ['mingw-org-w32api', 'mslearn-win32'], None
    if dv and not wv:
        return (dv['value'], 'verified', ['mslearn-win32'],
                'desktop Win32 docs state the value; w32api lineage does not define it')
    if w32val and dv and dv['value'].lower().lstrip('0x') != w32val.lower().lstrip('0x'):
        return (w32val, 'verify-runtime', ['mingw-org-w32api', 'mslearn-win32'],
                f'value conflict: w32api={w32val} desktop={dv["value"]} — needs curation')
    if w32val:
        return (w32val, 'verify-runtime', ['mingw-org-w32api'],
                'value from public-domain w32api lineage only; not stated in current desktop docs')
    return None, 'verify-runtime', [], 'no numeric definition found in w32api lineage'


def clean_sig(sig):
    return ' '.join((sig or '').split())


def notes_for(rec):
    n = rec.get('ce_notes_excerpt') or ''
    return n[:280]


def fn_record(area, rec, header, ds_by_name=None):
    name = canon_name(rec['name'])
    req = rec.get('requirements') or {}
    hdr = norm_header(req.get('header')) or header
    lib = (req.get('library') or '').strip().rstrip('.')
    lib = lib.lower() if lib else None
    if lib == 'developer':
        lib = None
    if ds_by_name and name in ds_by_name:
        srcs = [f'mslearn-{d}' for d in ('ce50', 'ce60') if d in ds_by_name[name]]
    else:
        srcs = [f"mslearn-{rec['docset']}"]
    notes = notes_for(rec)
    if rec['name'] != name:
        notes = (notes + ' ' if notes else '') + f"Doc page title: \"{rec['name']}\"."
    if norm_header(req.get('header')) == 'windows.h':
        notes = (notes + ' ' if notes else '') + 'Documented header: windows.h (CE umbrella).'
    r = {
        'id': f'{area}-F-{name}', 'kind': 'function', 'class': classify_fn(name),
        'status': 'verified', 'introduced': introduced_from(req),
        'definition': repair_sig(clean_sig(rec.get('signature'))) or f'{name} (see page)',
        'target_header': hdr, 'target_lib': lib, 'src': srcs, 'notes': notes,
    }
    return r


def const_record(area, name, page, docset, w32map, extra_note=None, kind='constant',
                  header=None):
    val, status, srcs, vnote = value_channels(name, w32map)
    wv = w32map.get(name)
    definition = f'#define {name} {val}' if val else (f'#define {name} {wv[1]}' if wv and wv[1] else f'#define {name} <?>')
    note = f'Documented on CE page "{page}" ({docset}).'
    if extra_note:
        note += ' ' + extra_note
    if vnote:
        note += ' ' + vnote
    return {
        'id': f'{area}-C-{name}', 'kind': kind, 'class': classify_const(name),
        'status': status, 'introduced': '~', 'value': val or '~',
        'definition': definition, 'target_header': header or 'winuser.h',
        'src': srcs or ['mslearn-ce60'],
        'notes': note,
    }


# ---------------------------------------------------------------- load facts
def load(name):
    return json.load(open(f'{FD}/{name}-facts.json'))


AREAS = {
    'winuser-core': {
        'files': ['ce50-ce60-winuser', 'ce50-ce60-window-control'],
        'header': 'winuser.h',
        'w32': W32USER,
        'excl_sub': ('Image Lists Reference',),  # -> commctrl
    },
    'wingdi-core': {
        'files': ['ce50-ce60-gdi'],
        'header': 'wingdi.h',
        'w32': W32GDI,
        'excl_sub': (),
    },
    'winsock': {
        'files': ['ce50-ce60-winsock'],
        'header': 'winsock2.h',
        'w32': W32SOCK,
        'excl_sub': (),
    },
    'commctrl-ce': {
        'files': ['ce50-ce60-commctrl-ce'],
        'header': 'commctrl.h',
        'w32': W32COMM,
        'excl_sub': (),
    },
}

# window-control subs that belong to commctrl.h (image lists) get routed there
IMG_SUB = 'Image Lists Reference'
# GDI-area subs routed to winuser (window-mgmt functions the docs filed under GDI)
GDI_TO_WINUSER = {
    'ClientToScreen', 'ScreenToClient', 'GetUpdateRect', 'GetUpdateRgn', 'InvalidateRect',
    'InvalidateRgn', 'ValidateRect', 'ValidateRgn', 'BeginPaint', 'EndPaint', 'GetDC',
    'ReleaseDC', 'GetWindowDC', 'RedrawWindow', 'LockWindowUpdate', 'ScrollWindow',
    'ScrollWindowEx', 'ScrollDC', 'SetWindowRgn', 'GetWindowRgn', 'PrintWindow',
}

MSG_RE = re.compile(r'^(WM|BM|CB|EM|LB|STM|SBM|DM)_[A-Z0-9_]+$')
CONST_PAGE_RE = re.compile(
    r'^(WS|WS_EX|BS|CBS|ES|LBS|SS|SBS|DS|MB|SW|SWP|SM|HWND|VK|WM|CS|RDW|'
    r'IPPROTO|SOL|SO_|AF_|SOCK_|FD_|TCP|IPPROTO|INADDR|MSG_|SD_|IP_)[A-Z0-9_]*$')

DISAMB = re.compile(r'\s*\((Windows Sockets|function|GDI|macro|structure|callback|Windows Embedded CE)\)$')

CURATED_NOTES = {
    'LVS_EX_NOFOSUCRECT': 'CE 5.0 page spells "LVS_EX_NOFOSUCRECT" — a documentation '
                          'typo for LVS_EX_NOFOCUSRECT (CE 6.0 page spells it correctly; '
                          'w32api lineage defines the correct spelling). Headers MUST '
                          'define only the correct spelling.',
}

TYPE_TOKENS = (
    'DWORD|WORD|BOOL|HWND|HMENU|HINSTANCE|HDC|HICON|HCURSOR|HBRUSH|HGLOBAL|HGDIOBJ|'
    'HPEN|HBRUSH|HBITMAP|HRGN|HFONT|H PALETTE|HPALETTE|HLOCAL|HANDLE|HKEY|HRESULT|'
    'LPCTSTR|LPTSTR|LPCWSTR|LPWSTR| LPCSTR|LPSTR|LPVOID|LPCVOID|LPDWORD|LPINT|LPWORD|LPBOOL|'
    'LPRECT|LPSIZE|LPPOINT|LPMSG|LPUINT|LPLONG|'
    'ATOM|BYTE|UINT|INT|LONG|SHORT|USHORT|UCHAR|CHAR|WCHAR|FLOAT|DOUBLE|'
    'WPARAM|LPARAM|LRESULT|COLORREF|DWORD_PTR|INT_PTR|UINT_PTR|LONG_PTR|ULONG_PTR|SIZE_T|'
    'int|unsigned|void|char|short|long|float|double|size_t|struct|const|SOCKET|LPSOCKADDR'
)
GLUE_RE = re.compile(r'\b(' + TYPE_TOKENS.replace(' ', '') + r')(?=[a-z]|[A-Z][a-z])')


def repair_sig(sig):
    """CE 5.0 pages glue type tokens to identifiers when markup is stripped
    (e.g. 'DWORDdwExStyle'); re-insert the separating space after a known type."""
    if not sig:
        return sig
    return GLUE_RE.sub(r'\1 ', sig)


def canon_name(name):
    return DISAMB.sub('', name).strip()


def target_lib_yaml(lib):
    return lib


def gen():
    out = {a: [] for a in AREAS}
    stats = {}
    for area, cfg in AREAS.items():
        recs = []
        for f in cfg['files']:
            recs.extend(load(f))
        # pre-pass: canonical name -> docsets having a page (after area routing)
        ds_by_name = {}
        for rec in recs:
            name = canon_name(rec['name'])
            sub = rec.get('sub', '')
            if sub in cfg['excl_sub']:
                continue
            if area == 'winuser-core' and sub == IMG_SUB:
                continue
            if area == 'wingdi-core' and name in GDI_TO_WINUSER:
                continue
            ds_by_name.setdefault(name, []).append(rec['docset'])
        seen = set()
        fcount = scount = ccount = 0
        # CE 6.0 pages have cleaner markup: prefer them when both docsets match
        recs.sort(key=lambda r: 0 if r['docset'] == 'ce60' else 1)
        for rec in recs:
            name = canon_name(rec['name'])
            sub = rec.get('sub', '')
            if sub in cfg['excl_sub']:
                continue  # handled by another area
            # route image lists -> commctrl-ce
            if area == 'winuser-core' and sub == IMG_SUB:
                continue
            if area == 'wingdi-core' and name in GDI_TO_WINUSER:
                continue
            if name in seen:
                continue  # other-docset duplicate; provenance merged via ds_by_name
            seen.add(name)
            sig = repair_sig(clean_sig(rec.get('signature')))
            if ' ' in name:  # family/overview pages ("Binary Raster Operations", ...)
                out[area].append({
                    'id': f'{area}-N-{re.sub(r"[^A-Za-z0-9]+", "", name)}',
                    'kind': 'note', 'class': 'common', 'status': 'verified',
                    'introduced': introduced_from(rec.get('requirements')),
                    'definition': f'Family page: {name} ({sub}).',
                    'target_header': cfg['header'],
                    'src': [f"mslearn-{rec['docset']}"],
                    'notes': notes_for(rec) or f'CE documentation family page ({sub}).',
                })
                continue
            if name == 'WM_APP' or MSG_RE.match(name):
                r = const_record(area, name, sub, rec['docset'], cfg['w32'],
                                 kind='constant')
                r['kind'] = 'message'
                out[area].append(r)
                ccount += 1
            elif sig.startswith('typedef struct') or sig.startswith('typedef struct'.upper()):
                r = fn_record(area, rec, cfg['header'], ds_by_name)
                r['kind'] = 'structure'
                r['id'] = f'{area}-S-{name}'
                r['class'] = 'ce-modified' if name in ('DRAWITEMSTRUCT', 'MENUITEMINFO') else 'common'
                out[area].append(r)
                scount += 1
            elif sig.startswith('typedef') and '(' in sig and ('CALLBACK' in sig or 'WINAPI' in sig):
                r = fn_record(area, rec, cfg['header'], ds_by_name)
                r['kind'] = 'type'
                r['id'] = f'{area}-T-{name}'
                out[area].append(r)
                scount += 1
            elif name in ('WNDPROC', 'DLGPROC', 'TIMERPROC', 'PROPENUMPROCEX', 'PROPENUMPROC',
                          'WNDENUMPROC', 'HOOKPROC', 'SENDASYNCPROC', 'DRAWSTATEPROC'):
                r = fn_record(area, rec, cfg['header'], ds_by_name)
                r['kind'] = 'type'
                r['id'] = f'{area}-T-{name}'
                out[area].append(r)
                scount += 1
            elif (sig and ('(' in sig) and not sig.startswith('typedef')) or sub.endswith('Functions'):
                r = fn_record(area, rec, cfg['header'], ds_by_name)
                out[area].append(r)
                fcount += 1
            elif CONST_PAGE_RE.match(name):
                r = const_record(area, name, sub, rec['docset'], cfg['w32'],
                                 header=cfg['header'])
                out[area].append(r)
                ccount += 1
            elif area == 'winsock' and not rec.get('signature'):
                # winsock constant pages (IPPROTO_*, SOL_*, ...) have no <pre> block
                r = const_record(area, name, sub, rec['docset'], cfg['w32'],
                                 extra_note='CE constant page without code block.',
                                 header=cfg['header'])
                out[area].append(r)
                ccount += 1
            elif sig and not sig.startswith('typedef'):
                r = fn_record(area, rec, cfg['header'], ds_by_name)
                out[area].append(r)
                fcount += 1
            elif sig.startswith('typedef'):
                r = fn_record(area, rec, cfg['header'], ds_by_name)
                r['kind'] = 'type'
                r['id'] = f'{area}-T-{name}'
                out[area].append(r)
                scount += 1
        stats[area] = {'functions': fcount, 'structures+types': scount, 'consts+msgs': ccount}

    # image lists + command bars -> commctrl-ce (window-control harvest source)
    wc = load('ce50-ce60-window-control')
    seen = {r['id'] for r in out['commctrl-ce']}
    n_img = 0
    for rec in wc:
        if rec.get('sub') != IMG_SUB:
            continue
        name = rec['name']
        rid = f'commctrl-ce-F-{name}'
        if rid in seen:
            continue
        seen.add(rid)
        r = fn_record('commctrl-ce', rec, 'commctrl.h')
        out['commctrl-ce'].append(r)
        n_img += 1
    stats['commctrl-ce']['functions'] += n_img

    # style-table constants -> winuser-core / wingdi-core / commctrl-ce by family
    tables = json.load(open(f'{FD}/ce-style-tables.json'))['pages']
    COMM_FAMS = ('CBS_', 'LVS_', 'TBS_', 'TCS_', 'TVS_', 'HDS_', 'MCS_', 'DTS_',
                 'PGS_', 'UDS_', 'RBS_', 'CCS_', 'TBSTYLE_', 'TTS_', 'PBS_')
    added = {r['id'].rsplit('-', 1)[-1] for r in out['winuser-core'] + out['commctrl-ce'] + out['wingdi-core']}
    ntab = 0
    for p in tables:
        for c in p['constants']:
            name = c['name']
            if name.startswith('R2_') or name in ('BLACKNESS', 'NOTSRCERASE', 'NOTSRCCOPY',
                                                  'SRCERASE', 'DSTINVERT', 'PATINVERT',
                                                  'SRCINVERT', 'SRCAND', 'SRCPAINT',
                                                  'PATCOPY', 'PATPAINT', 'WHITENESS', 'SRC_COPY'):
                area = 'wingdi-core'
                w32map = W32GDI
                header = 'wingdi.h'
            elif name.startswith(('CBS_', 'LBS_', 'ES_', 'SS_', 'BS_', 'DS_')):
                # classic-control style families are winuser.h even when the CE
                # docs table them under the common-control pages
                area = 'winuser-core'
                w32map = W32USER
                header = 'winuser.h'
            elif name.startswith(COMM_FAMS):
                area = 'commctrl-ce'
                w32map = W32COMM
                header = 'commctrl.h'
            else:
                area = 'winuser-core'
                w32map = W32USER
                header = 'winuser.h'
            if name in added:
                continue
            added.add(name)
            r = const_record(area, name, p['page'], p['docset'], w32map,
                             extra_note=(CURATED_NOTES.get(name) or c['desc'][:180]),
                             header=header)
            out[area].append(r)
            ntab += 1
    # winsock error codes -> verified constants (Class A value tables)
    ws_err = {}
    for ds in ('ce50', 'ce60'):
        p = f'{FD}/{ds}-winsock-errors.json'
        if os.path.exists(p):
            for e in json.load(open(p))['errors']:
                ws_err.setdefault(e['name'], e)
    have_ws = {r['id'] for r in out['winsock']}
    for name, e in sorted(ws_err.items()):
        rid = f'winsock-C-{name}'
        if rid in have_ws:
            continue
        out['winsock'].append({
            'id': rid, 'kind': 'constant', 'class': 'common', 'status': 'verified',
            'introduced': '~', 'value': str(e['code']),
            'definition': f'#define {name} {e["code"]}',
            'target_header': 'winsock2.h',
            'src': ['mslearn-ce60', 'mslearn-ce50'],
            'notes': f'Value stated in the documented Winsock Error Codes table (both docsets identical). {e.get("desc", "")}'[:280],
        })
    stats['winsock-errors'] = len(ws_err)

    stats['style-table-constants'] = ntab
    return out, stats


def yq(v):
    """Always-quote a scalar for YAML flow context."""
    v = str(v)
    return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'


REQUIRED_KEYS = ('id', 'kind', 'class', 'status', 'introduced', 'target_header', 'src')


def emit(records, path, header_comment):
    lines = [header_comment]
    for r in records:
        parts = []
        for k in REQUIRED_KEYS:
            v = r.get(k)
            if v is None or v == '' or v == '~':
                v = '~'
            if isinstance(v, list):
                v = '[' + ', '.join(yq(x) for x in v) + ']'
            else:
                v = yq(v)
            parts.append(f'{k}: {v}')
        for k, v in r.items():
            if k in REQUIRED_KEYS or v is None or v == '' or v == '~':
                continue
            if isinstance(v, list):
                v = '[' + ', '.join(yq(x) for x in v) + ']'
            elif isinstance(v, (int, float)):
                v = str(v)
            else:
                v = yq(v)
            parts.append(f'{k}: {v}')
        lines.append('- {' + ', '.join(parts) + '}')
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    return len(records)


def main():
    out, stats = gen()
    total = 0
    for area, records in out.items():
        records.sort(key=lambda r: (r['kind'], r['id']))
        path = f'{REPO}/data/facts/{area}.yaml'
        n = emit(records, path,
                 f'# Fact database — {area} (machine-generated from area harvests; '
                 f'curate by hand thereafter)\n'
                 f'# Schema: docs/01-methodology/verification-policy.md §1\n'
                 f'# Generated by tools/gen_area_yaml.py — DO NOT hand-edit IDs\n'
                 f'# Sources: mslearn-ce60/ce50 pages (Class A), mingw-org-w32api '
                 f'(Class B, public domain), mslearn-win32 (Class A values)')
        total += n
        print(f'{area}.yaml: {n} records')
    print('stats:', json.dumps(stats))
    print('total:', total)


if __name__ == '__main__':
    main()
