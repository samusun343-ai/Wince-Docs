#!/usr/bin/env python3
"""P3-area fact YAML generator.

Routes the P3-session area harvests (6,986 pages) into per-header fact databases:
  inputs : data/mslearn-facts/{ce50-ce60-coreos-rest, ce50-ce60-fileio-rest-a,
           ce50-ce60-fileio-rest-b, ce40-ce50-ce60-security-crypt,
           ce50-ce60-security-auth, ce60-ole-com-ref, ce50-ole-com-ref,
           ce60-ole-auto, ce50-ole-auto, ce50-ce60-ole-storage,
           ce50-ce60-wininet, ce50-ce60-urlmon, ce40-urlmon, ce50-ce60-intl,
           ce40-ce50-ce60-fonts, ce50-ce60-tapi, ce40-tapi,
           ce40-ce50-ce60-ras-wnet, ce60-rapi-misc, ce40-ce50-ce60-obex,
           ce50-ce60-tcpip, ce50-ce60-audio, ce60-bluetooth,
           ce50-ce40-bluetooth, ce50-ce60-kernel, ce40-ce50-ce60-snmp}-facts.json
  outputs: data/facts/{celog,nat,statebroker,marshal,database,storemgr,
           fsdriver-excluded,wincrypt,sspi,winscard,credman,lass,ole-com,oleauto,
           wininet,urlmon,winnls,imm,mui,fonts,tapi,ras,wnet,rapi,connmgr,power,
           gps,obex,iphlp,dnsapi,ws2tcpip,mmedia,bluetooth,kernel-ref,snmp}.yaml

Complements gen_area_yaml.py (P1) / gen_area_yaml2.py (P2); never rewrites their
outputs. Cross-area name-level dedupe against a snapshot of the pre-P3 fact DB.
Routing is by subarea and documented Requirements header (normalised, first of a
comma list); the FSD/bootpart/disk-cache/copy-external driver surface goes to
fsdriver-excluded.yaml as an explicit closure register (same policy as the GWES
internal register of P2).
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
W32BASE, _ = scan_w32(['winbase.h', 'winnt.h'])
W32OLE, _ = scan_w32(['objbase.h', 'objidl.h', 'ole2.h', 'oleauto.h', 'oaidl.h',
                      'oleidl.h', 'olectl.h', 'ocidl.h'])
W32CRYPT, _ = scan_w32(['wincrypt.h', 'wintrust.h'])
W32SSPI, _ = scan_w32(['sspi.h', 'security.h'])
W32NLS, _ = scan_w32(['winnls.h'])
W32IMM, _ = scan_w32(['imm.h'])
W32INET, _ = scan_w32(['wininet.h'])
W32RAS, _ = scan_w32(['ras.h', 'raserror.h'])
W32WNET, _ = scan_w32(['winnetwk.h'])
W32IPHL, _ = scan_w32(['iphlpapi.h', 'iptypes.h', 'iprtrmib.h', 'ipexport.h'])
W32WS2T, _ = scan_w32(['ws2tcpip.h'])
W32MM, _ = scan_w32(['mmsystem.h', 'mmreg.h'])
W32RAPI, _ = scan_w32(['rapi.h'])
W32SNMP, _ = scan_w32(['snmp.h'])
W32GDI, _ = scan_w32(['wingdi.h'])
W32CARD, _ = scan_w32(['winscard.h', 'smclib.h'])

# ---------------------------------------------------------------- routing
FILES = [
    ('ce50-ce60-coreos-rest', 'coreos-rest'),
    ('ce50-ce60-fileio-rest-a', 'fileio-rest-a'),
    ('ce50-ce60-fileio-rest-b', 'fsdriver'),
    ('ce40-ce50-ce60-security-crypt', 'sec'),
    ('ce50-ce60-security-auth', 'sec'),
    ('ce60-ole-com-ref', 'ole-com'), ('ce50-ole-com-ref', 'ole-com'),
    ('ce60-ole-auto', 'ole-auto'), ('ce50-ole-auto', 'ole-auto'),
    ('ce50-ce60-ole-storage', 'ole-com'),
    ('ce50-ce60-wininet', 'wininet'),
    ('ce50-ce60-urlmon', 'urlmon'), ('ce40-urlmon', 'urlmon'),
    ('ce50-ce60-intl', 'intl'),
    ('ce40-ce50-ce60-fonts', 'fonts'),
    ('ce50-ce60-tapi', 'tapi'), ('ce40-tapi', 'tapi'),
    ('ce40-ce50-ce60-ras-wnet', 'raswnet'),
    ('ce60-rapi-misc', 'rapimisc'),
    ('ce40-ce50-ce60-obex', 'obex'),
    ('ce50-ce60-tcpip', 'tcpip'),
    ('ce50-ce60-audio', 'audio'),
    ('ce60-bluetooth', 'bluetooth'), ('ce50-ce40-bluetooth', 'bluetooth'),
    ('ce50-ce60-kernel', 'kernel'),
    ('ce40-ce50-ce60-snmp', 'snmp'),
]

AREA_ALL_CEONLY = {
    'celog', 'nat', 'statebroker', 'marshal', 'database', 'storemgr',
    'fsdriver-excluded', 'lass', 'connmgr', 'gps', 'obex', 'rapi',
    'kernel-ref', 'bluetooth',
}

# 'Ce' must be followed by an uppercase letter (CeOpenDatabase yes, CertCloseStore no)
CE_FN_RE = re.compile(
    r'^(Ce[A-Z_]|Obex|Bth|ConnMgr|Gps|Lap|LASS|Registry|Snapi|EDB|Bluetooth)')
CE_CONST_PREFIX = (
    'SN_', 'CELOG', 'OBEX', 'BTH', 'CONNMGR', 'NAT_', 'GPS', 'POWER_STATE',
    'MSGQUEUE', 'CEDB', 'CEOID', 'EDB',
)

MSG_RE = re.compile(r'^(MM_|MIM_|MOM_|PBT_|WM_|CB_|EM_)[A-Z0-9_]*$')
CONST_RE = re.compile(
    r'^(CLSCTX|COINIT|CO_|COINIT_|DV_|TYPE_|RPC_|DISP_|CACHE_|CLASS_|CTL_|MK_|'
    r'STG|STGM|STGC|STGTY|STGMOVE|VT_|VARTYPE|VAR_|DISPATCH_|TYPEKIND|TYPEFLAGS|'
    r'INVOKEKIND|IDLFLAG|IMPLTYPEFLAGS|PARAMFLAGS|OLERENDER|OLE_|OLECMD|OLEIVERB|'
    r'OLEMISC|OLECLOSE|OLECMDID|USERCLASSTYPE|CLSCTX|REGCLS|REGCLS_|SOFTWARE_|'
    r'CRYPT|CALG|PROV|KP_|PP_|CERT|CMSG|CTL_|X509|szOID|SEC_E|SEC_I|SECPKG|'
    r'SCARD|SC_|RASBASE|RAS_|LINEERR|LINE_|PHONEERR|PHONE_|TAPIERR|TAPIMODE|'
    r'WAVE|MIDI|MIXER|WIM_|WOM_|AUX|TIMERR|JOY|MMIO|MMSYSERR|WAVERR|MIDIERR|'
    r'MM_|DRVM|MOD_|INTERNET|HTTP_|FTP_|COOKIE_|URL_|URLMON|INET_E|DNS|IP_|'
    r'MAX_|IF_|MIB_|NETIO|ICMP|POWER|PWR|BATTERY|BTL|IRLMP|SOL_|AI_|NI_|EAI_|'
    r'IPV6|IN6|SN_|SNAPI|STATE_|CELOG|OBEX|BTH|CONNMGR|NAT_|GPS|IMM|CFS|CAND|'
    r'COMP|GCS|GGL|GL_|LOCALE|LCID|LANG|SUBLANG|NORM|SORT|CP_|CT_|LCMAP|CAL_|'
    r'DATE|LGRPID|HIGHCONTRAST|SNMP|ASN|SNMPAPI|ERROR|WAVEIN|WAVEOUT|WAVEFORM|'
    r'WHDR|WAVECAPS|MIDICAPS|SND_|MIXER_|MCI|MCIWN|FONT|GCP|TM_|OUT|'
    r'PWR_|BATTERY|XDETACH|DEVMODE|ENUM|CURRENTSETTINGS|RAPI|WNET|WN_|'
    r'LINE|PHONE|IME_|TAPIE|TAPI'
    r')[A-Z0-9_]*$')

IFACE_RE = re.compile(r'^I(?!ID)[A-Z][A-Za-z0-9_]{2,}$')
SUFFIX_STRIP = re.compile(
    r'\s+\((Windows Embedded CE|Compact 2013|Windows CE|function|structure|'
    r'enumeration|macro|interface|constant|message|method|property|object|'
    r'callback|GDI|Windows Sockets)\)$')

# API-variant suffixes: stripped from the canonical name but kept as a record
# variant (CEDB vs EDB document structurally different APIs under equal names)
VARIANT_RE = re.compile(r'\s+\((RAPI2?|EDB|CEDB)\)$')

NAME_SUFFIX = re.compile(
    r'\s+(Structure|Function|Functions|Enumeration|Macro|Interface|Constant|'
    r'Constants|Message|Messages|Method|Property|Type|Data Types|Callback)$')

OWN_OUTPUTS = {
    'celog', 'nat', 'statebroker', 'marshal', 'database', 'storemgr',
    'fsdriver-excluded', 'wincrypt', 'sspi', 'winscard', 'credman', 'lass',
    'ole-com', 'oleauto', 'wininet', 'urlmon', 'winnls', 'imm', 'mui', 'fonts',
    'tapi', 'ras', 'wnet', 'rapi', 'connmgr', 'power', 'gps', 'obex', 'iphlp',
    'dnsapi', 'ws2tcpip', 'mmedia', 'bluetooth', 'kernel-ref', 'snmp',
}
EXISTING_NAMES = set()
for _p in os.listdir(FACTS):
    if not _p.endswith('.yaml') or _p[:-5] in OWN_OUTPUTS:
        continue
    for _m in re.finditer(r'-[CFSTN]-([A-Za-z0-9_]+)",', open(f'{FACTS}/{_p}').read()):
        EXISTING_NAMES.add(_m.group(1))


def hdr_first(h):
    """Requirements headers come as 'objidl.h, objidl.idl' — take the first."""
    if not h:
        return None
    return norm_header(h.split(',')[0])


def classify(name, area):
    if area in AREA_ALL_CEONLY:
        return 'ce-only'
    if CE_FN_RE.match(name):
        return 'ce-only'
    if name.startswith(CE_CONST_PREFIX):
        return 'ce-only'
    return 'common'


def route(rec, source):
    """Return (area, default_header, w32map)."""
    req = rec.get('requirements') or {}
    hdr = hdr_first(req.get('header')) or ''
    hdr_raw = (req.get('header') or '').strip()
    sub = rec.get('sub', '')
    if source == 'coreos-rest':
        if sub.startswith('CeLog'):
            return 'celog', 'celog.h', None
        if sub.startswith('Network Address Translation'):
            return 'nat', 'nat.h', None
        if sub.startswith('State and Notifications Broker'):
            return 'statebroker', 'regext.h', None
        return 'marshal', 'marshal.h', None
    if source == 'fileio-rest-a':
        if sub.startswith('Database Reference'):
            return 'database', hdr or 'windbase.h', None
        return 'storemgr', hdr or 'storemgr.h', None
    if source == 'fsdriver':
        return 'fsdriver-excluded', hdr or '(driver surface)', None
    if source == 'sec':
        if hdr in ('sspi.h', 'security.h', 'rpcdce.h', 'rpcdcep.h'):
            return 'sspi', 'sspi.h', W32SSPI
        if hdr in ('winscard.h', 'smclib.h', 'smbprot.h'):
            return 'winscard', 'winscard.h', W32CARD
        if hdr in ('credui.h', 'credmgr.h', 'credsvc.h'):
            return 'credman', hdr, None
        if hdr in ('lass.h', 'lap.h', 'lassguid.h'):
            return 'lass', 'lass.h', None
        if sub.startswith(('Authentication', 'LASS', 'LAP')):
            return 'sspi' if sub.startswith('Auth') else 'lass', 'sspi.h' if sub.startswith('Auth') else 'lass.h', W32SSPI if sub.startswith('Auth') else None
        if sub.startswith(('Smart Card',)):
            return 'winscard', 'winscard.h', W32CARD
        if sub.startswith(('Credential',)):
            return 'credman', 'credui.h', None
        return 'wincrypt', 'wincrypt.h', W32CRYPT
    if source in ('ole-com',):
        return 'ole-com', hdr or 'objbase.h', W32OLE
    if source == 'ole-auto':
        return 'oleauto', hdr or 'oleauto.h', W32OLE
    if source == 'wininet':
        return 'wininet', 'wininet.h', W32INET
    if source == 'urlmon':
        return 'urlmon', hdr or 'urlmon.h', W32INET
    if source == 'intl':
        if hdr == 'imm.h' or sub.startswith('Input Method Manager'):
            return 'imm', 'imm.h', W32IMM
        if sub.startswith('Multilingual User Interface'):
            return 'mui', hdr or 'muireg.h', W32NLS
        return 'winnls', 'winnls.h', W32NLS
    if source == 'fonts':
        return 'fonts', hdr or 'wingdi.h', W32GDI
    if source == 'tapi':
        return 'tapi', hdr or 'tapi.h', None
    if source == 'raswnet':
        if sub.startswith('Windows Networking') or hdr in ('winnetwk.h', 'npapi.h', 'wnaspi32.h'):
            return 'wnet', 'winnetwk.h', W32WNET
        return 'ras', hdr or 'ras.h', W32RAS
    if source == 'rapimisc':
        if sub.startswith('RAPI'):
            return 'rapi', hdr or 'rapi.h', W32RAPI
        if sub.startswith('Connection Manager'):
            return 'connmgr', 'connmgr.h', None
        if sub.startswith('GPS'):
            return 'gps', hdr or 'gpsapi.h', None
        return 'power', hdr or 'pwinbase.h', W32BASE
    if source == 'obex':
        return 'obex', hdr or 'obex.h', None
    if source == 'tcpip':
        if sub.startswith('DNS'):
            return 'dnsapi', hdr or 'windns.h', None
        if 'ws2tcpip' in hdr_raw.lower() or sub.startswith(('Core Protocol Stack', 'Assigning', 'Converting')) or sub == '(top)':
            return 'ws2tcpip', hdr or 'ws2tcpip.h', W32WS2T
        if sub.startswith('ICMP'):
            return 'iphlp', hdr or 'iphlpapi.h', W32IPHL
        return 'iphlp', hdr or 'iphlpapi.h', W32IPHL
    if source == 'audio':
        return 'mmedia', hdr or 'mmsystem.h', W32MM
    if source == 'bluetooth':
        return 'bluetooth', hdr or 'bthutil.h', None
    if source == 'kernel':
        return 'kernel-ref', hdr or 'pkfuncs.h', W32BASE
    if source == 'snmp':
        return 'snmp', hdr or 'snmp.h', W32SNMP
    return 'kernel-ref', hdr or 'winbase.h', W32BASE


def clean_name(name):
    n = SUFFIX_STRIP.sub('', name)
    n = NAME_SUFFIX.sub('', n)
    return n.strip()


def split_variant(name):
    """Split an API-variant suffix: 'CEDBASEINFOEX (EDB)' -> (name, 'EDB')."""
    m = VARIANT_RE.search(name)
    if not m:
        return name, None
    return name[:m.start()].strip(), m.group(1)


def pick_intro(a, b):
    vals = [v for v in (a, b) if v and v != '~']
    if not vals:
        return '~'
    try:
        return min(vals, key=float)
    except ValueError:
        return vals[0]


def main():
    out = {}
    seen = {}
    stats = {}
    iface_groups = {}  # (area, IFaceName) -> {methods: {Method: {sig, srcs, intro}}, header, lib}
    for fname, source in FILES:
        recs = json.load(open(f'{FD}/{fname}-facts.json'))
        recs.sort(key=lambda r: 0 if r['docset'] == 'ce60' else (1 if r['docset'] == 'ce50' else 2))
        for rec in recs:
            area, header, w32 = route(rec, source)
            name = clean_name(canon_name(rec['name']))
            name, variant = split_variant(name)
            vid_suffix = f'_{variant}' if variant and variant.lower() != area else ''
            if '::' in rec['name']:
                # documented interface-method page (IFace::Method): aggregate per interface
                ifname, mname = rec['name'].split('::', 1)
                ifname, mname = ifname.strip(), mname.strip()
                g = iface_groups.setdefault(
                    (area, ifname),
                    {'methods': {}, 'header': header, 'lib': None})
                req_m = rec.get('requirements') or {}
                m = g['methods'].setdefault(
                    mname, {'sig': None, 'srcs': set(), 'intro': '~'})
                if not m['sig']:
                    m['sig'] = repair_sig(clean_sig(rec.get('signature')))
                m['srcs'].add(f"mslearn-{rec['docset']}")
                m['intro'] = pick_intro(m['intro'], introduced_from(req_m))
                if g['lib'] is None:
                    lib0 = (req_m.get('library') or '').strip().rstrip('.').lower()
                    g['lib'] = lib0 if lib0 and lib0 not in (
                        'developer', 'implementation', 'application-defined',
                        'send', 'additional', 'none', '', 'note') else None
                continue
            if area != 'fsdriver-excluded' and name in EXISTING_NAMES:
                stats['skipped-existing'] = stats.get('skipped-existing', 0) + 1
                continue
            key = (area, name, variant)
            if key in seen:
                out[area][seen[key]]['src'] = sorted(
                    set(out[area][seen[key]]['src']) | {f"mslearn-{rec['docset']}"})
                continue
            sig = repair_sig(clean_sig(rec.get('signature')))
            req = rec.get('requirements') or {}
            hdr_raw = (req.get('header') or '').strip()
            lib = (req.get('library') or '').strip().rstrip('.')
            lib = (lib.lower() if lib and lib.lower() not in
                   ('developer', 'implementation', 'application-defined', 'send',
                    'additional', 'none', '', 'note') else None)
            intro = introduced_from(req)
            srcs = [f"mslearn-{rec['docset']}"]
            notes = (rec.get('ce_notes_excerpt') or '')[:260]
            if hdr_raw and hdr_first(hdr_raw) not in (header, None) and area != 'fsdriver-excluded':
                notes = (notes + ' ' if notes else '') + f'Documented header: {hdr_raw}.'
            if rec['name'] != name:
                notes = (notes + ' ' if notes else '') + f'Doc page title: "{rec["name"]}".'
            if variant:
                notes = (notes + ' ' if notes else '') + f'API variant: {variant}.'
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
                recd = {
                    'id': f'{area}-N-{re.sub(r"[^A-Za-z0-9]+", "", name)[:60]}{vid_suffix}',
                    'kind': 'note', 'class': classify(name, area), 'status': 'verified',
                    'introduced': intro,
                    'definition': f'Family/overview page: {name} ({rec.get("sub")}).',
                    'target_header': header, 'src': srcs,
                    'notes': notes or f'CE documentation page ({rec.get("sub")}).',
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if area == 'fsdriver-excluded':
                recd = {
                    'id': f'fsdriver-excluded-N-{re.sub(r"[^A-Za-z0-9]+", "", name)[:60]}',
                    'kind': 'note', 'class': 'ce-only', 'status': 'verified',
                    'introduced': intro,
                    'definition': f'Driver/OEM surface: {name} ({hdr_raw or "no header"}).',
                    'target_header': '(excluded)',
                    'src': srcs,
                    'notes': (f'Excluded from the application header set: {rec.get("sub")} '
                              f'is FSD/bootpart/disk-cache/copy-external driver-facing '
                              f'documentation, not an exported application API. Recorded '
                              f'for closure only.'),
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            stmts = [s for s in (sig or '').split(';') if s.strip()]
            is_iface = bool(IFACE_RE.match(name)) and sig and (
                not sig.startswith(('typedef', '#', 'const', 'extern'))) and (
                'Interfaces' in (rec.get('sub') or '')
                or '.idl' in hdr_raw.lower()
                or len(stmts) >= 2)
            if is_iface:
                recd = {
                    'id': f'{area}-I-{name}{vid_suffix}', 'kind': 'interface',
                    'class': classify(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig or f'{name} (see page)',
                    'target_header': header, 'target_lib': lib, 'src': srcs,
                    'notes': notes or 'Documented COM interface page; methods listed in the definition.',
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if MSG_RE.match(name):
                val, status, vsrc, vnote = value_channels(name, w32 or {})
                wv = (w32 or {}).get(name)
                definition = f'#define {name} {val}' if val else (
                    f'#define {name} {wv[1]}' if wv and wv[1] else f'#define {name} <?>')
                note = f'Documented on CE page "{rec.get("sub")}" ({rec["docset"]}).'
                if vnote:
                    note += ' ' + vnote
                recd = {
                    'id': f'{area}-C-{name}{vid_suffix}', 'kind': 'message',
                    'class': classify(name, area), 'status': status,
                    'introduced': intro, 'value': val or '~', 'definition': definition,
                    'target_header': header,
                    'src': list(set(srcs + vsrc)) or srcs, 'notes': note,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if (sig and sig.lstrip().startswith('typedef struct')) or (
                    sig.startswith('typedef') and '{' in sig
                    and '(' not in sig.split('{')[0]
                    and not re.search(r'\benum\b', sig[:60])):
                # covers 'typedef struct tagX {...', 'typedef enum' handled below,
                # and the glued CE 5.0 form 'typedef MSGQUEUEOPTIONS_OS{...'
                recd = {
                    'id': f'{area}-S-{name}{vid_suffix}', 'kind': 'structure',
                    'class': classify(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig, 'target_header': header,
                    'target_lib': lib, 'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig.startswith('typedef') and ('CALLBACK' in sig or 'WINAPI' in sig):
                recd = {
                    'id': f'{area}-T-{name}{vid_suffix}', 'kind': 'type',
                    'class': classify(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig, 'target_header': header,
                    'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig.startswith('typedef') and re.search(r'\benum\b', sig[:60]):
                recd = {
                    'id': f'{area}-E-{name}{vid_suffix}', 'kind': 'enumeration',
                    'class': classify(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig, 'target_header': header,
                    'target_lib': lib, 'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig.startswith('typedef'):
                recd = {
                    'id': f'{area}-T-{name}{vid_suffix}', 'kind': 'type',
                    'class': classify(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig, 'target_header': header,
                    'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig and '(' in sig and not sig.startswith('#'):
                recd = {
                    'id': f'{area}-F-{name}{vid_suffix}', 'kind': 'function',
                    'class': classify(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig or f'{name} (see page)',
                    'target_header': header, 'target_lib': lib, 'src': srcs,
                    'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig and sig.startswith('#'):
                val, status, vsrc, vnote = value_channels(name, w32 or {})
                wv = (w32 or {}).get(name)
                definition = f'#define {name} {val}' if val else (
                    f'#define {name} {wv[1]}' if wv and wv[1] else f'#define {name} <?>')
                note = f'Documented on CE page "{rec.get("sub")}" ({rec["docset"]}).'
                if vnote:
                    note += ' ' + vnote
                recd = {
                    'id': f'{area}-C-{name}{vid_suffix}', 'kind': 'constant',
                    'class': classify(name, area), 'status': status,
                    'introduced': intro, 'value': val or '~', 'definition': definition,
                    'target_header': header,
                    'src': list(set(srcs + vsrc)) or srcs, 'notes': note,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if CONST_RE.match(name):
                val, status, vsrc, vnote = value_channels(name, w32 or {})
                wv = (w32 or {}).get(name)
                definition = f'#define {name} {val}' if val else (
                    f'#define {name} {wv[1]}' if wv and wv[1] else f'#define {name} <?>')
                note = f'Documented on CE page "{rec.get("sub")}" ({rec["docset"]}).'
                if not val and wv and wv[1]:
                    note += ' symbolic definition from the public-domain w32api lineage; numeric value not stated in the CE docs.'
                if vnote:
                    note += ' ' + vnote
                recd = {
                    'id': f'{area}-C-{name}{vid_suffix}', 'kind': 'constant',
                    'class': classify(name, area), 'status': status,
                    'introduced': intro, 'value': val or '~', 'definition': definition,
                    'target_header': header,
                    'src': list(set(srcs + vsrc)) or srcs, 'notes': note,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            if sig:
                recd = {
                    'id': f'{area}-F-{name}{vid_suffix}', 'kind': 'function',
                    'class': classify(name, area), 'status': 'verified',
                    'introduced': intro, 'definition': sig, 'target_header': header,
                    'target_lib': lib, 'src': srcs, 'notes': notes,
                }
                out.setdefault(area, []).append(recd)
                seen[key] = len(out[area]) - 1
                continue
            recd = {
                'id': f'{area}-N-{re.sub(r"[^A-Za-z0-9]+", "", name)[:60]}{vid_suffix}',
                'kind': 'note', 'class': classify(name, area), 'status': 'verified',
                'introduced': intro,
                'definition': f'Documentation page: {name} ({rec.get("sub")}).',
                'target_header': header, 'src': srcs,
                'notes': notes or f'CE documentation page ({rec.get("sub")}).',
            }
            out.setdefault(area, []).append(recd)
            seen[key] = len(out[area]) - 1

    # aggregated interface records from IFace::Method pages
    for (area, ifname), g in sorted(iface_groups.items()):
        methods = g['methods']
        intro = '~'
        for m in methods.values():
            intro = pick_intro(intro, m['intro'])
        definition = '; '.join(
            (m['sig'] or f'{mn} (see page)') for mn, m in sorted(methods.items()))
        srcs = sorted(set().union(*[m['srcs'] for m in methods.values()]))
        recd = {
            'id': f'{area}-I-{ifname}', 'kind': 'interface',
            'class': classify(ifname, area), 'status': 'verified',
            'introduced': intro, 'definition': definition,
            'target_header': g['header'], 'target_lib': g['lib'], 'src': srcs,
            'notes': f'Aggregated from {len(methods)} documented method pages '
                     f'({ifname}::Method).',
        }
        ids = [r['id'] for r in out.get(area, [])]
        if recd['id'] in ids:
            idx = ids.index(recd['id'])
            out[area][idx]['definition'] += ' ' + definition
            out[area][idx]['src'] = sorted(
                set(out[area][idx]['src']) | set(srcs))
            stats['iface-merged'] = stats.get('iface-merged', 0) + 1
        else:
            out.setdefault(area, []).append(recd)

    total = 0
    for area in sorted(out):
        records = out[area]
        records.sort(key=lambda r: (r['kind'], r['id']))
        ids = [r['id'] for r in records]
        assert len(ids) == len(set(ids)), f'dup ids in {area}'
        # name uniqueness inside the area (interface + function of same name etc.)
        path = f'{FACTS}/{area}.yaml'
        n = emit(records, path,
                 f'# Fact database — {area} (machine-generated from P3 area harvests)\n'
                 f'# Schema: docs/01-methodology/verification-policy.md §1\n'
                 f'# Generated by tools/gen_area_yaml3.py — DO NOT hand-edit IDs\n'
                 f'# Sources: mslearn-ce60/ce50/ce40 pages (Class A), mingw-org-w32api '
                 f'(Class B, public domain), mslearn-win32 (Class A values)')
        total += n
        print(f'{area}.yaml: {n} records')
        stats[area] = n
    print('stats:', json.dumps(stats))
    print('total:', total, '| skipped (already in pre-P3 fact DB):',
          stats.get('skipped-existing', 0))


if __name__ == '__main__':
    main()
