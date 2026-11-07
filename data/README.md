# Data Directory — Contents and Regeneration

All datasets in this directory are **factual extractions** with per-record provenance (see `docs/01-methodology/verification-policy.md`). Nothing here is copied expressive content. Licensing: MIT (see `docs/01-methodology/licensing.md`).

## Layout

| Path | Content | How produced |
| --- | --- | --- |
| `mslearn-doc-index/` | Full page indexes of the MS Learn Windows CE documentation sets (one JSON per doc set; gzip snapshots + stats) | `tools/extract_mslearn_index.py` |
| `mslearn-inventories/` | Curated per-area API reference page lists (`ce60/`, `ce50/`, `ce40/`; areas: core-os, file-io, gwes, gdi, window-control, shell, winsock, common-controls, error-values) | `tools/build_inventories.py` |
| `mslearn-facts/` | Harvested per-page fact records — core sets (`ce60-core-facts.json` 33, `ce50-core-facts.json` 31), area sets: P1 (`ce50-ce60-window-control-facts.json` 609, `ce50-ce60-winuser-facts.json` 430 incl. the CE 6.0 keyboard supplement, `ce50-ce60-gdi-facts.json` 344, `ce50-ce60-winsock-facts.json` 332, `ce50-ce60-commctrl-ce-facts.json` 130), P2 (`ce50-ce60-fileio-app-facts.json` 169, `ce50-ce60-coreos-app-facts.json` 520, `ce50-ce60-gwes-rest-facts.json` 546, `ce50-ce60-shell-spi-facts.json` 414, `ce60-cc-rest-facts.json` 763, `ce50-cc-rest-facts.json` 761 — 3,173 new pages, 0 fetch failures), error tables (`ce60-system-errors.json` 571, `ce50-system-errors.json` 570, `ce{50,60}-winsock-errors.json` 37 rows / 35 unique), and the documented constant-name tables (`ce-style-tables.json`: 64 pages, 793 rows) | `tools/harvest_facts.py`, `tools/harvest_area.py`, `tools/harvest_ce60_keyboard.py`, `tools/extract_winsock_errors.py`, `tools/extract_style_tables.py` + `tools/extract_flag_tables.py` |
| `facts/` | Spec-level enumerated fact databases: `windef.yaml` (92), `winnt-core.yaml` (47), `winuser-core.yaml` (688), `wingdi-core.yaml` (176), `winsock.yaml` (202), `commctrl-ce.yaml` (237), and the P2 set — `winbase-fileio.yaml` (54), `winreg.yaml` (33), `windbase.yaml` (6), `winbase-os.yaml` (207), `toolhelp.yaml` (16), `msgqueue.yaml` (9), `dbgapi.yaml` (14), `notify.yaml` (13), `aygshell.yaml` (46), `shellapi.yaml` (56), `commctrl-controls.yaml` (760), `winuser-gwes.yaml` (62), `wingdi-print.yaml` (11), `internal-excluded.yaml` (448, the closure exclusion register) — **3,177 unique ids total** | curated (P0) + `tools/gen_area_yaml.py` (P1) + `tools/gen_area_yaml2.py` (P2, both machine-generated then hand-curatable) |

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
