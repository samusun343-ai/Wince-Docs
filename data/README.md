# Data Directory — Contents and Regeneration

All datasets in this directory are **factual extractions** with per-record provenance (see `docs/01-methodology/verification-policy.md`). Nothing here is copied expressive content. Licensing: MIT (see `docs/01-methodology/licensing.md`).

## Layout

| Path | Content | How produced |
| --- | --- | --- |
| `mslearn-doc-index/` | Full page indexes of the MS Learn Windows CE documentation sets (one JSON per doc set; gzip snapshots + stats) | `tools/extract_mslearn_index.py` |
| `mslearn-inventories/` | Curated per-area API reference page lists (`ce60/`, `ce50/`, `ce40/`; 32 areas: core-os, file-io, gwes, gdi, window-control, shell, winsock, common-controls, error-values + the P3 set — ole-com, security, nls, imm, mui, wininet, urlmon, obex, rapi, tapi, ras, wnet, tcpip, ipv6, audio, power, connmgr, bluetooth, fonts, kernel, gps, snmp) | `tools/build_inventories.py` |
| `mslearn-facts/` | Harvested per-page fact records — core sets (`ce60-core-facts.json` 33, `ce50-core-facts.json` 31), area sets: P1 (`ce50-ce60-window-control-facts.json` 609, `ce50-ce60-winuser-facts.json` 430 incl. the CE 6.0 keyboard supplement, `ce50-ce60-gdi-facts.json` 344, `ce50-ce60-winsock-facts.json` 332, `ce50-ce60-commctrl-ce-facts.json` 130), P2 (`ce50-ce60-fileio-app-facts.json` 169, `ce50-ce60-coreos-app-facts.json` 520, `ce50-ce60-gwes-rest-facts.json` 546, `ce50-ce60-shell-spi-facts.json` 414, `ce60-cc-rest-facts.json` 763, `ce50-cc-rest-facts.json` 761 — 3,173 new pages, 0 fetch failures), P3 (26 files, **6,986 pages, 0 failures**: `ce50-ce60-coreos-rest` 220, `ce50-ce60-fileio-rest-a` 326, `ce50-ce60-fileio-rest-b` 215, `ce40-ce50-ce60-security-crypt` 573, `ce50-ce60-security-auth` 226, `ce60-ole-com-ref` 341, `ce50-ole-com-ref` 345, `ce60-ole-auto` 303, `ce50-ole-auto` 303, `ce50-ce60-ole-storage` 432, `ce50-ce60-wininet` 213, `ce50-ce60-urlmon` 296, `ce40-urlmon` 144, `ce50-ce60-intl` 398, `ce40-ce50-ce60-fonts` 109, `ce50-ce60-tapi` 410, `ce40-tapi` 204, `ce40-ce50-ce60-ras-wnet` 153, `ce60-rapi-misc` 313, `ce40-ce50-ce60-obex` 163, `ce50-ce60-tcpip` 326, `ce50-ce60-audio` 188, `ce60-bluetooth` 216, `ce50-ce40-bluetooth` 257, `ce50-ce60-kernel` 186, `ce40-ce50-ce60-snmp` 126), error tables (`ce60-system-errors.json` 571, `ce50-system-errors.json` 570, `ce{50,60}-winsock-errors.json` 37 rows / 35 unique), and the documented constant-name tables (`ce-style-tables.json`: 64 pages, 793 rows) | `tools/harvest_facts.py`, `tools/harvest_area.py`, `tools/harvest_ce60_keyboard.py`, `tools/extract_winsock_errors.py`, `tools/extract_style_tables.py` + `tools/extract_flag_tables.py` |
| `facts/` | Spec-level enumerated fact databases: `windef.yaml` (92), `winnt-core.yaml` (47), `winuser-core.yaml` (688), `wingdi-core.yaml` (176), `winsock.yaml` (202), `commctrl-ce.yaml` (237), the P2 set — `winbase-fileio.yaml` (54), `winreg.yaml` (33), `windbase.yaml` (6), `winbase-os.yaml` (207), `toolhelp.yaml` (16), `msgqueue.yaml` (9), `dbgapi.yaml` (14), `notify.yaml` (13), `aygshell.yaml` (46), `shellapi.yaml` (56), `commctrl-controls.yaml` (760), `winuser-gwes.yaml` (62), `wingdi-print.yaml` (11), `internal-excluded.yaml` (448, the closure exclusion register) — and the **P3 set (35 files, 2,789 records)**: `ole-com` (305), `oleauto` (201), `wincrypt` (203), `sspi` (52), `winscard` (31), `credman` (16), `lass` (19), `winnls` (47), `imm` (148), `mui` (5), `wininet` (108), `urlmon` (96), `rapi` (112), `tapi` (206), `ras` (35), `wnet` (16), `iphlp` (96), `dnsapi` (32), `ws2tcpip` (35), `obex` (16), `connmgr` (30), `gps` (17), `bluetooth` (189), `mmedia` (99), `fonts` (50), `database` (135), `storemgr` (67), `fsdriver-excluded` (125), `celog` (77), `statebroker` (17), `nat` (20), `marshal` (10), `kernel-ref` (102), `snmp` (42), `power` (30) — **5,966 unique ids total** | curated (P0) + `tools/gen_area_yaml.py` (P1) + `tools/gen_area_yaml2.py` (P2) + `tools/gen_area_yaml3.py` (P3, all machine-generated then hand-curatable) |

## Regeneration

```sh
curl -s "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/toc.json" -o /tmp/embedded-root-toc.json
python3 tools/extract_mslearn_index.py   # writes mslearn-doc-index/ (+ gz snapshots)
python3 tools/build_inventories.py       # writes mslearn-inventories/
python3 tools/harvest_facts.py           # re-harvests the core fact pages (network)
python3 tools/harvest_area.py ce60:window-control ce50:window-control   # area harvests (network)
python3 tools/harvest_area.py ce60:gwes ce50:gwes --sub '^(Windows Reference|Window Class Reference|Window and Control Styles|Windows Timer Reference|Window Properties Reference|System Information Reference|Message Queue Reference|Keyboard Reference|Resources Reference)$' --out ce50-ce60-winuser
python3 tools/harvest_ce60_keyboard.py  # supplements the CE 6.0 keyboard pages from the doc index
# P2 session harvests (all network; ~3,100 pages):
python3 tools/harvest_area.py ce60:file-io ce50:file-io --sub '^(File I/O|File Mapping|Registry|User Management|File System Password) Reference$' --out ce50-ce60-fileio-app
python3 tools/harvest_area.py ce60:core-os ce50:core-os --sub '^(Process and Thread|Memory Management|Synchronization|Time|String|Strings|Unicode|ToolHelp|DLL|Exception|System Management|Message Queue Point-to-Point|Debugging|Serial Communications|Fiber) Reference$' --out ce50-ce60-coreos-app
python3 tools/harvest_area.py ce60:gwes ce50:gwes --sub '^(GWES OS|Resources|Resource-Definition Statements|System Information|Message Queue|Notify|Notification|Printing|Startup User Interface|Out of Memory User Interface|Interprocess Communication|Message Synchronization)' --out ce50-ce60-gwes-rest
python3 tools/harvest_area.py ce60:shell ce50:shell ce60:winsock ce50:winsock --sub '^(AYGShell|Standard Shell|Console|Shell OS) Reference$|^Winsock SPI Reference$' --out ce50-ce60-shell-spi
python3 tools/harvest_area.py ce60:common-controls --sub '^(Animation|CapEdit|Controls|Custom Draw|Date and Time Picker|Header|List-View|Month Calendar|Progress Bar|Property Sheets|Rebar|SbEdit|Status Bars|Tab|Toolbar|ToolTips|Trackbar|Tree View|Up-Down) ' --out ce60-cc-rest
python3 tools/harvest_area.py ce50:common-controls --sub '^(Animation|CapEdit|Controls|Custom Draw|Date and Time Picker|Header|List-View|Month Calendar|Progress Bar|Property Sheets|Rebar|SbEdit|Status Bars|Tab|Toolbar|ToolTips|Trackbar|Tree View|Up-Down) ' --out ce50-cc-rest
python3 tools/extract_style_tables.py && python3 tools/extract_flag_tables.py
python3 tools/extract_winsock_errors.py
python3 tools/gen_area_yaml.py           # regenerates the four P1 fact YAMLs
python3 tools/gen_area_yaml2.py          # regenerates the fourteen P2 fact YAMLs
# P3 session harvests (all network; 6,986 pages, chunked runs):
python3 tools/harvest_area.py ce60:core-os ce50:core-os --sub '^(CeLog Event Tracking|Network Address Translation|State and Notifications Broker|Kernel Buffer Marshaling) Reference$' --out ce50-ce60-coreos-rest
python3 tools/harvest_area.py ce60:file-io ce50:file-io --sub '^(Database|Storage Manager|FAT File System|Partition Manager) Reference$' --out ce50-ce60-fileio-rest-a
python3 tools/harvest_area.py ce60:file-io ce50:file-io --sub '^(FSD|Bootpart|Disk Cache Manager|Copy External) Reference$' --out ce50-ce60-fileio-rest-b
python3 tools/harvest_area.py ce60:security ce50:security ce40:security --sub '^(Cryptography|Certificates)' --out ce40-ce50-ce60-security-crypt
python3 tools/harvest_area.py ce60:security ce50:security --sub '^(Credential Manager|Smart Card|Authentication Services|LASS|LAP)' --out ce50-ce60-security-auth
python3 tools/harvest_area.py ce60:ole-com --sub '^COM Reference$' --out ce60-ole-com-ref
python3 tools/harvest_area.py ce50:ole-com --sub '^COM Reference$' --out ce50-ole-com-ref
python3 tools/harvest_area.py ce60:ole-com --sub '^Automation Reference$' --out ce60-ole-auto
python3 tools/harvest_area.py ce50:ole-com --sub '^Automation Reference$' --out ce50-ole-auto
python3 tools/harvest_area.py ce60:ole-com ce50:ole-com --sub '^(OLE Reference|Storage Reference)$' --out ce50-ce60-ole-storage
python3 tools/harvest_area.py ce60:wininet ce50:wininet --out ce50-ce60-wininet
python3 tools/harvest_area.py ce60:urlmon ce50:urlmon --out ce50-ce60-urlmon
python3 tools/harvest_area.py ce40:urlmon --out ce40-urlmon
python3 tools/harvest_area.py ce60:nls ce50:nls ce60:imm ce50:imm ce60:mui ce50:mui --out ce50-ce60-intl
python3 tools/harvest_area.py ce60:fonts ce50:fonts ce40:fonts --out ce40-ce50-ce60-fonts
python3 tools/harvest_area.py ce60:tapi ce50:tapi --out ce50-ce60-tapi
python3 tools/harvest_area.py ce40:tapi --out ce40-tapi
python3 tools/harvest_area.py ce60:ras ce50:ras ce40:ras ce60:wnet ce50:wnet ce40:wnet --out ce40-ce50-ce60-ras-wnet
python3 tools/harvest_area.py ce60:rapi ce60:connmgr ce60:power ce50:power ce60:gps --out ce60-rapi-misc
python3 tools/harvest_area.py ce60:obex ce50:obex ce40:obex --out ce40-ce50-ce60-obex
python3 tools/harvest_area.py ce60:tcpip ce50:tcpip ce60:ipv6 ce50:ipv6 --out ce50-ce60-tcpip
python3 tools/harvest_area.py ce60:audio ce50:audio --out ce50-ce60-audio
python3 tools/harvest_area.py ce60:bluetooth --out ce60-bluetooth
python3 tools/harvest_area.py ce50:bluetooth ce40:bluetooth --out ce50-ce40-bluetooth
python3 tools/harvest_area.py ce60:kernel ce50:kernel --out ce50-ce60-kernel
python3 tools/harvest_area.py ce60:snmp ce50:snmp ce40:snmp --out ce40-ce50-ce60-snmp
python3 tools/gen_area_yaml3.py          # regenerates the thirty-five P3 fact YAMLs
python3 tools/validate.py               # schema + provenance validation
```

## Index snapshot statistics (2026-11-07)

| Doc set | Unique pages | JSON size | gzip |
| --- | --- | --- | --- |
| ce60 | 23,713 | 7.4 MB | ~1.1 MB |
| ce50 | 22,889 | 5.7 MB | ~0.9 MB |
| ce40 | 6,362 | 1.4 MB | ~0.25 MB |
| wec7 | 20,286 | 4.5 MB | ~0.8 MB |
| wec2013 | 16,863 | 3.7 MB | ~0.7 MB |

## Record formats

* **doc-index**: `{ "t": title, "u": relative-url, "p": [toc-path…] }`
* **inventories**: `{ "area", "sub", "t", "u" }`
* **harvested facts (area records)**: `{ name, title, docset, url, retrieved, signature, code_blocks[], requirements{os,header,library}, ce_notes_excerpt, area, sub }`
* **style/flag tables**: `{ pages: [ { page, docset, url, retrieved, constants: [ {name, desc} ] } ] }`
* **system errors**: `{ "code": int, "name": "ERROR_…", "desc": "one-line factual description" }` (+ docset/url/retrieved envelope)
* **winsock errors**: `{ "code": int, "name": "WSAE…", "desc": … }` (same envelope)
* **fact YAML**: `docs/01-methodology/verification-policy.md` §1 (normative schema)

## Rights note

Facts are extracted from the official Microsoft documentation pages cited in each record (`retrieved` dates included). The indexes are bibliographies of Microsoft-published pages, not copies of their content. Value cross-checks additionally cite the public-domain MinGW.org w32api lineage (`MaxKellermann/w32api`, branch `wip`) and the desktop Win32 documentation; numeric values are facts, recorded with their per-record sources.
