#!/usr/bin/env python3
"""P2-area fact YAML generator.

Routes the P2-session area harvests into per-header fact databases:
  inputs : data/mslearn-facts/{ce50-ce60-fileio-app, ce50-ce60-coreos-app,
           ce50-ce60-gwes-rest, ce50-ce60-shell-spi, ce60-cc-rest,
           ce50-cc-rest}-facts.json
  outputs: data/facts/{winbase-fileio,winreg,windbase,winbase-os,toolhelp,msgqueue,
           dbgapi,notify,aygshell,ws2spi,shellapi,commctrl-controls,winuser-gwes,
           wingdi-print,internal-excluded}.yaml

Complements tools/gen_area_yaml.py (P0/P1 areas) and never rewrites its outputs.
Records whose canonical name is already covered by a pre-existing fact YAML are
skipped (cross-area name-level dedupe against a snapshot of data/facts/*.yaml
taken at start).

Routing is by the page's documented Requirements header (normalised), with the
internal/OEM surface (GWES OS C++ classes, Notifext.hxx, CeNotifyPrivate_*,
Resource-Definition statements, oomui.h) recorded in internal-excluded.yaml as
explicit closure exclusions rather than silently dropped.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_area_yaml import (scan_w32, introduced_from, norm_header, clean_sig,
                           repair_sig, canon_name, value_channels, emit)

REPO = os.path.dirname(HERE)
FD = f'{REPO}/data/mslearn-facts'
FACTS = f'{REPO}/data/facts'

# ---------------------------------------------------------------- w32api maps
W32BASE, _ = scan_w32(['winbase.h', 'winnt.h', 'winnls.h'])
W32REG, _ = scan_w32(['winreg.h'])
W32TOOL, _ = scan_w32(['tlhelp32.h'])
W32SHELL, _ = scan_w32(['shellapi.h', 'shlobj.h', 'cpl.h'])
W32COMM, _ = scan_w32(['commctrl.h', 'prsht.h'])
W32SPI, _ = scan_w32(['ws2spi.h'])
W32USER, _ = scan_w32(['winuser.h', 'windows.h'])
W32GDI, _ = scan_w32(['wingdi.h'])

# ---------------------------------------------------------------- routing
# documented header (normalised) -> (area, w32map)
HEADER_ROUTE = [
    ('winreg.h', 'winreg', None, W32REG),
    ('pwinreg.h', 'winreg', None, W32REG),
    ('windbase.h', 'windbase', None, None),
    ('tlhelp32.h', 'toolhelp', None, W32TOOL),
    ('msgqueue.h', 'msgqueue', None, None),
    ('dbgapi.h', 'dbgapi', None, None),
    ('notify.h', 'notify', None, None),
    ('aygshell.h', 'aygshell', None, None),
    ('ws2spi.h', 'ws2spi', None, W32SPI),
    ('shellapi.h', 'shellapi', None, W32SHELL),
    ('shlobj.h', 'shellapi', None, W32SHELL),
    ('shobjidl.h', 'shellapi', None, None),
    ('shobjidl.idl', 'shellapi', None, None),
    ('newmenu.h', 'shellapi', None, None),
    ('cpl.h', 'shellapi', None, None),
    ('console.h', 'shellapi', None, None),
    ('commctrl.h', 'commctrl-controls', None, W32COMM),
    ('commctrl.h.se', 'commctrl-controls', None, W32COMM),
    ('pcommctrl.h', 'commctrl-controls', None, W32COMM),
    ('prsht.h', 'commctrl-controls', None, W32COMM),
    ('wingdi.h', 'wingdi-print', None, W32GDI),
    ('extfile.h', 'winbase-fileio', None, W32BASE),
    ('winuser.h', 'winuser-gwes', None, W32USER),
    ('winbase.h', None, None, W32BASE),        # resolved per-source below
    ('pwinbase.h', None, None, W32BASE),
    ('winnt.h', None, None, W32BASE),
    ('kfuncs.h', 'kfuncs-note', None, W32BASE),
    ('pkfuncs.h', 'pkfuncs-note', None, W32BASE),
]
INTERNAL_HDR_EXT = ('.hpp', '.hxx')

FILES = [
    ('ce50-ce60-fileio-app', 'fileio'),
    ('ce50-ce60-coreos-app', 'coreos'),
    ('ce50-ce60-gwes-rest', 'gwes'),
    ('ce50-ce60-shell-spi', 'shell'),
    ('ce60-cc-rest', 'cc'),
    ('ce50-cc-rest', 'cc'),
]

# winbase-bearing sources split into two areas
WINBASE_AREA = {'fileio': 'winbase-fileio', 'coreos': 'winbase-os',
                'gwes': 'winbase-os', 'shell': 'winbase-os', 'cc': 'winbase-os'}

CE_FN_PREFIX = (
    'Ce', 'SH', 'CommandBar', 'CommandBands', 'MsgQueue', 'CreateMsgQueue',
    'OpenMsgQueue', 'ReadMsgQueue', 'WriteMsgQueue', 'CloseMsgQueue',
    'GetMsgQueueInfo', 'SetMsgQueueInfo', 'GetMsgQueueWaitCount',
)
CE_MSG_ONLY = {'WM_HIBERNATE', 'WM_IM_INFO', 'WM_FILECHANGEINFO'}  # CE-only messages
# pages whose documented signature parses as a call but which are structures
FORCE_STRUCT = {'BROWSEINFO'}
CE_FN_EXACT = {
    'CheckPassword', 'GetPasswordActive', 'SetPasswordActive', 'GetPasswordStatus',
    'SetPasswordStatus', 'GetUserDirectory', 'SetCurrentUser', 'SetUserData',
    'SetPassword',
    'CreateFileForMapping', 'CreateFileForMappingW', 'GetDeviceUniqueID',
    'KernelIoControl', 'GetSystemPowerStatusEx', 'GetSystemPowerStatusEx2',
    'SetSystemPowerState', 'CeGetCallerTrust',
    'SystemIdleTimerReset', 'RefreshDLLs', 'DumpCap', 'GetHeapSnapshot',
}
CE_STRUCT_PREFIX = ('CE', 'MSGQUEUE', 'FILECHANGE', 'NOTIFICATION', 'DBGPARAM')
AREA_ALL_CEONLY = {'msgqueue', 'dbgapi', 'notify', 'aygshell'}

# control message / notification families -> kind "message"
MSG_RE = re.compile(
    r'^(WM|BM|CB|EM|LB|STM|SBM|DM|NM|LVM|LVN|TVM|TVN|HDM|HDN|TCM|TCN|UDM|UDN|'
    r'RBM|RBN|PBM|PBN|DTM|DTN|MCM|MCN|TBM|TBN|TTM|TTN|PSM|PSN|NMN|BFFM|CBN|'
    r'LVEVN?|WM_|WM_FILECHANGEINFO|PSN_)[A-Z0-9_]*$')
CONST_RE = re.compile(
    r'^(REG|KEY|HKEY|RTL|VAL|GMEM|LMEM|GHND|GPTR|LPTR|LHND|NONZERO|PAGE|MEM|'
    r'FILE|CREATE|GENERIC|READ|WRITE|SHARE|SEEK|MOVE|COPY|LOCK|INVALID|HFILE|'
    r'OF_|MAX_|DRIVE|EXE|SECURITY_|ACCESS_|SECTION_|FILEMAP|THREAD_PRIORITY|'
    r'THREAD|NORMAL_|IDLE_|ABOVE_|BELOW_|TIME_|TIMER|WAIT|INFINITE|MAXIMUM|'
    r'STILL_ACTIVE|DUPLICATE|STARTF|DEBUG|EXCEPTION|SPI|TLS|LANG|SUBLANG|'
    r'NORM_|SORT|LCID|NLS|CP_|MB_|WC_|CT_|LCMAP|CAL_|TH32|HF32|MSGQUEUE|'
    r'MQ_|MAX_|CNT_|RTC_|DISP_|SHRG|NIN|NOTIFICATION|SHNL|SHNF|SHNIF|SEE_|'
    r'FO_|FOF|NIM|NIF|NIIF|ABM|ABE|ABP|SLGP|SFGAO|CSIDL|SHGFI|DROP|CF_|'
    r'LVS|LVM|LVIF|LVIR|LVHT|LVIS|LVA|LVC|LVI|LVGA|LVGIT|LVCD|TBS|TBM|TBN|'
    r'TBC|TBCD|TCS|TCM|TCIF|TCIS|TVS|TVM|TVN|TVIF|TVIS|TVHT|TVC|TVGN|'
    r'HDS|HDM|HDN|HDI|HDHT|MCS|MCM|MCN|MCINFO|DTS|DTM|DTN|UDS|UDM|UDN|'
    r'UDACCEL|RBS|RBB|RBIM|RBN|RBI|CCS|CD|CDDS|CDDT|CDIS|CDRF|'
    r'TBSTATE|TBSTYLE|TB_|TBN|TBCUST|TBTF|TTS|TTM|TTN|TTIFT|TTPP|PBS|PBM|PBN|'
    r'PRSHT|PSN|PSCB|PSM|PSP|PSPCB|PSWIZB|PSBTN|ILC|ILT|ILIF|NMHDR|'
    r'SHID|SHBI|SHBIF|SHRGI|SHG|CMD|SW_HIDE|DLG|HDM_LAYOUT|IOCTL_CONSOLE|'
    r'SHELL|BACKLIGHT|FILE_FLAG|FILE_ATTRIBUTE|FILE_SHARE|FILE_BEGIN|'
    r'FILE_CURRENT|FILE_END|FILE_TYPE|FILE_CACHE|VOLUME|CE_'
    r')[A-Z0-9_]*$')

CE_ONLY_CONST_EXACT = {
    'MSGQUEUE_ALLOW_BROWSE', 'MSGQUEUE_ALLOW_ISOLATED', 'MSGQUEUE_MSGSIZE_MAX',
    'MSGQUEUE_MSGSIZE_MIN', 'MSGQUEUE_MSGSIZE_UNLIMITED', 'MSGQUEUE_PRIORITY_NORMAL',
    'MSGQUEUE_FIFO', 'INVALID_HANDLE_VALUE',  # sentinel libdefs, classify below
}

# existing (pre-P2) fact names, for cross-area dedupe — the output areas of
# THIS generator are excluded from the snapshot so re-runs are idempotent
OWN_OUTPUTS = {
    'winbase-fileio', 'winreg', 'windbase', 'winbase-os', 'toolhelp', 'msgqueue',
    'dbgapi', 'notify', 'aygshell', 'ws2spi', 'shellapi', 'commctrl-controls',
    'winuser-gwes', 'wingdi-print', 'internal-excluded',
}
EXISTING_NAMES = set()
for _p in os.listdir(FACTS):
    if not _p.endswith('.yaml') or _p[:-5] in OWN_OUTPUTS:
        continue
    for _m in re.finditer(r'-[CFSTN]-([A-Za-z0-9_]+)",', open(f'{FACTS}/{_p}').read()):
        EXISTING_NAMES.add(_m.group(1))

CURATED = {
    'WM_FILECHANGEINFO': 'CE-only message sent to shell file-change windows '
                         '(documented on the shlobj.h page); value is w32api-lineage.',
    'UDM_SETPOS32': 'Documented in the CE 6.0 docset only (32-bit position message); '
                    'CE 5.0 tree has no page — gate to 6.0 pending Role C check.',
    'UDM_GETPOS32': 'Documented in the CE 6.0 docset only (32-bit position message); '
                    'CE 5.0 tree has no page — gate to 6.0 pending Role C check.',
    'GetSystemTimeAsFileTime': 'Absent from the CE 5.0 docset index but present in '
                               'CE 6.0; desktop-common since NT 3.5 — verify-runtime '
                               'for CE 4.x/5.x availability.',
    'ExtractIconEx': 'Documented in the CE Resources Reference with Shellapi.h header '
                     'and Icon.lib binding (CE documents the icon set; see spec).',
    'WM_HIBERNATE': 'CE-only low-memory broadcast (object-store hibernate); value '
                    '0x3FF from the w32api CE-gated lineage.',
    'WM_IM_INFO': 'CE-only IME information message; numeric value not in the '
                  'w32api lineage — Role C must probe on device.',
}


def classify_fn(name, area):
    if area in AREA_ALL_CEONLY:
        return 'ce-only'
    if name.startswith(CE_FN_PREFIX) or name in CE_FN_EXACT:
        return 'ce-only'
    return 'common'


def classify_const(name, area):
    if area in AREA_ALL_CEONLY:
        return 'ce-only'
    if name in CE_MSG_ONLY or name.startswith('IOCTL_CONSOLE'):
        return 'ce-only'
    if name in CE_ONLY_CONST_EXACT or name in CURATED and 'CE-only' in CURATED[name]:
        return 'ce-only'
    if name.startswith(('REG_', 'MSGQUEUE_', 'FILECHANGE', 'CEOID', 'CEDB')):
        return 'ce-only' if name.startswith(('MSGQUEUE_', 'CEOID', 'CEDB')) else 'common'
    return 'common'


def route(rec, source):
    """Return (area, header, w32map) or ('internal', header, None)."""
    req = rec.get('requirements') or {}
    hdr = norm_header(req.get('header')) or ''
    sub = rec.get('sub', '')
    name = rec['name']
    # internal surface first
    if (hdr.endswith(INTERNAL_HDR_EXT) or '::' in name
            or name.startswith('CeNotifyPrivate_') or name.startswith('CeNotifyPublic_')
            or sub == 'Resource-Definition Statements' or sub == 'GWES OS Reference'):
        return 'internal-excluded', hdr or '(none)', None
    if sub == 'Printing Reference' and hdr in ('wingdi.h',):
        return 'wingdi-print', 'wingdi.h', W32GDI
    for h, area, _ovr, w32 in HEADER_ROUTE:
        if hdr == h:
            if area is None:
                area = WINBASE_AREA.get(source, 'winbase-os')
            if area in ('kfuncs-note', 'pkfuncs-note'):
                # documented under Kfuncs.h/pkfuncs.h (PB headers) — keep the
                # canonical placement note, prefer a winbase.h page if one exists
                return ('winbase-os', 'winbase.h', W32BASE, hdr)
            return area, hdr, w32
    if hdr in ('', 'developer'):
        # overview/table pages without requirements: keep as notes of the source area
        if source == 'shell':
            return 'shellapi', 'shellapi.h', W32SHELL
        if source == 'cc':
            return 'commctrl-controls', 'commctrl.h', W32COMM
        return 'winbase-os' if source == 'coreos' else 'winuser-gwes', \
               'winbase.h' if source == 'coreos' else 'winuser.h', W32BASE if source == 'coreos' else W32USER
    return 'internal-excluded', hdr, None


def const_or_msg_record(area, rec, name, header, w32, kind='message'):
    """Constant/message record using the w32api numeric value when available,
    falling back to the public-domain symbolic expansion (e.g. LVM_FIRST+4)."""
    val, status, vsrc, vnote = value_channels(name, w32 or {})
    wv = (w32 or {}).get(name)
    definition = f'#define {name} {val}' if val else (
        f'#define {name} {wv[1]}' if wv and wv[1] else f'#define {name} <?>')
    note = f'Documented on CE page "{rec.get("sub")}" ({rec["docset"]}).'
    if name in CURATED:
        note += ' ' + CURATED[name]
    if not val and wv and wv[1]:
        note += ' symbolic definition from the public-domain w32api lineage; ' \
                'numeric value not stated in the CE docs.'
    if vnote:
        note += ' ' + vnote
    return {
        'id': f'{area}-C-{name}', 'kind': kind,
        'class': classify_const(name, area), 'status': status,
        'introduced': introduced_from(rec.get('requirements')),
        'value': val or '~', 'definition': definition,
        'target_header': header,
        'src': list(set([f"mslearn-{rec['docset']}"] + vsrc)) or [f"mslearn-{rec['docset']}"],
        'notes': note,
    }


def main():
    out = {}
    stats = {}
    seen = {}
    for fname, source in FILES:
        recs = json.load(open(f'{FD}/{fname}-facts.json'))
        recs.sort(key=lambda r: 0 if r['docset'] == 'ce60' else 1)
        for rec in recs:
            r = route(rec, source)
            if r and len(r) == 4:
                area, header, w32, doc_hdr = r
            else:
                area, header, w32 = r
                doc_hdr = header
            name = canon_name(rec['name'])
            if area != 'internal-excluded' and name in EXISTING_NAMES:
                stats['skipped-existing'] = stats.get('skipped-existing', 0) + 1
                continue
            key = (area, name)
            if key in seen:
                # merge docset provenance
                out[area][seen[key]]['src'] = sorted(
                    set(out[area][seen[key]]['src']) | {f"mslearn-{rec['docset']}"})
                continue
            sig = repair_sig(clean_sig(rec.get('signature')))
            req = rec.get('requirements') or {}
            lib = (req.get('library') or '').strip().rstrip('.')
            lib = (lib.lower() if lib and lib.lower() not in
                   ('developer', 'implementation', 'application-defined',
                    'send', 'additional', 'none', '') else None)
            intro = introduced_from(req)
            srcs = [f"mslearn-{rec['docset']}"]
            notes = (rec.get('ce_notes_excerpt') or '')[:260]
            if doc_hdr and doc_hdr not in (header, '(none)') and area != 'internal-excluded':
                notes = (notes + ' ' if notes else '') + \
                    f'Documented header: {doc_hdr} (PB-side header).'
            if ' ' in name or not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
                recd = {
                    'id': f'{area}-N-{re.sub(r"[^A-Za-z0-9]+", "", name)[:60]}',
                    'kind': 'note', 'class': 'common', 'status': 'verified',
                    'introduced': intro,
                    'definition': f'Family/overview page: {name} ({rec.get("sub")}).',
                    'target_header': header, 'src': srcs,
                    'notes': notes or f'CE documentation page ({rec.get("sub")}).',
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if area == 'internal-excluded':
                recd = {
                    'id': f'internal-excluded-N-{re.sub(r"[^A-Za-z0-9]+", "", name)[:60]}',
                    'kind': 'note', 'class': 'ce-only', 'status': 'verified',
                    'introduced': intro,
                    'definition': f'Internal/OEM surface: {name} ({doc_hdr or "no header"}).',
                    'target_header': '(excluded)',
                    'src': srcs,
                    'notes': (f'Excluded from the application header set: {rec.get("sub")} '
                              f'is GWES/OEM implementation documentation, not an exported '
                              f'application API. Recorded for closure only.'),
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if MSG_RE.match(name) and not name.startswith(('NM_', 'NMHDR')):
                recd = const_or_msg_record(area, rec, name, header, w32, kind='message')
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig and ('{' in sig and sig.startswith('typedef')
                       and 'CALLBACK' not in sig and '(' not in sig.split('{')[0]):
                # covers both 'typedef struct tagX {...' and the glued CE 5.0
                # form 'typedef MSGQUEUEOPTIONS_OS{...'
                recd = {
                    'id': f'{area}-S-{name}', 'kind': 'structure',
                    'class': 'ce-only' if name.startswith(CE_STRUCT_PREFIX)
                             or classify_fn(name, area) == 'ce-only' else 'common',
                    'status': 'verified', 'introduced': intro,
                    'definition': sig, 'target_header': header,
                    'target_lib': lib, 'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig.startswith('typedef') and ('CALLBACK' in sig or 'WINAPI' in sig):
                recd = {
                    'id': f'{area}-T-{name}', 'kind': 'type',
                    'class': classify_fn(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig,
                    'target_header': header, 'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if name in FORCE_STRUCT:
                recd = {
                    'id': f'{area}-S-{name}', 'kind': 'structure',
                    'class': classify_fn(name, area), 'status': 'verified',
                    'introduced': intro,
                    'definition': sig or f'{name} (see page)',
                    'target_header': header, 'target_lib': lib,
                    'src': srcs, 'notes': notes or 'Documented structure page.',
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if (sig and '(' in sig and not sig.startswith('#')) or \
                    (rec.get('sub', '').endswith('Functions') and not sig):
                if not sig and not name[0].isupper():
                    continue  # stray token
                recd = {
                    'id': f'{area}-F-{name}', 'kind': 'function',
                    'class': classify_fn(name, area), 'status': 'verified',
                    'introduced': intro,
                    'definition': sig or f'{name} (see page)',
                    'target_header': header, 'target_lib': lib,
                    'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig and sig.startswith('#'):
                recd = const_or_msg_record(area, rec, name, header, w32, kind='constant')
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if CONST_RE.match(name):
                recd = const_or_msg_record(area, rec, name, header, w32, kind='constant')
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig:
                recd = {
                    'id': f'{area}-F-{name}', 'kind': 'function',
                    'class': classify_fn(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig,
                    'target_header': header, 'target_lib': lib,
                    'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            # remaining: page without signature and not constant-shaped
            recd = {
                'id': f'{area}-N-{re.sub(r"[^A-Za-z0-9]+", "", name)[:60]}',
                'kind': 'note', 'class': 'common', 'status': 'verified',
                'introduced': intro,
                'definition': f'Documentation page: {name} ({rec.get("sub")}).',
                'target_header': header, 'src': srcs,
                'notes': notes or f'CE documentation page ({rec.get("sub")}).',
            }
            out.setdefault(area, []).append(recd)
            seen[key] = len(out[area]) - 1

    total = 0
    for area in sorted(out):
        records = out[area]
        records.sort(key=lambda r: (r['kind'], r['id']))
        # uniqueness guard for ids
        ids = [r['id'] for r in records]
        assert len(ids) == len(set(ids)), f'dup ids in {area}'
        path = f'{FACTS}/{area}.yaml'
        n = emit(records, path,
                 f'# Fact database — {area} (machine-generated from P2 area harvests)\n'
                 f'# Schema: docs/01-methodology/verification-policy.md §1\n'
                 f'# Generated by tools/gen_area_yaml2.py — DO NOT hand-edit IDs\n'
                 f'# Sources: mslearn-ce60/ce50 pages (Class A), mingw-org-w32api '
                 f'(Class B, public domain), mslearn-win32 (Class A values)')
        total += n
        print(f'{area}.yaml: {n} records')
        stats[area] = n
    print('stats:', json.dumps(stats))
    print('total:', total, '| skipped (already in pre-P2 fact DB):',
          stats.get('skipped-existing', 0))


if __name__ == '__main__':
    main()
