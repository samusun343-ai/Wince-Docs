# Data Directory — Contents and Regeneration

All datasets in this directory are **factual extractions** with per-record provenance (see `docs/01-methodology/verification-policy.md`). Nothing here is copied expressive content. Licensing: MIT (see `docs/01-methodology/licensing.md`).

## Layout

| Path | Content | How produced |
| --- | --- | --- |
| `mslearn-doc-index/` | Full page indexes of the MS Learn Windows CE documentation sets (one JSON per doc set; gzip snapshots + stats) | `tools/extract_mslearn_index.py` |
| `mslearn-inventories/` | Curated per-area API reference page lists (`ce60/`, `ce50/`, `ce40/`; areas: core-os, file-io, gwes, gdi, window-control, shell, winsock, common-controls, error-values) | `tools/build_inventories.py` |
| `mslearn-facts/` | Harvested per-page fact records — core sets (`ce60-core-facts.json` 33, `ce50-core-facts.json` 31), area sets (`ce50-ce60-window-control-facts.json` 609, `ce50-ce60-winuser-facts.json` 430 incl. the CE 6.0 keyboard supplement, `ce50-ce60-gdi-facts.json` 344, `ce50-ce60-winsock-facts.json` 332, `ce50-ce60-commctrl-ce-facts.json` 130), error tables (`ce60-system-errors.json` 571, `ce50-system-errors.json` 570, `ce{50,60}-winsock-errors.json` 37 rows / 35 unique), and the documented constant-name tables (`ce-style-tables.json`: 64 pages, 793 rows) | `tools/harvest_facts.py`, `tools/harvest_area.py`, `tools/harvest_ce60_keyboard.py`, `tools/extract_winsock_errors.py`, `tools/extract_style_tables.py` + `tools/extract_flag_tables.py` |
| `facts/` | Spec-level enumerated fact databases: `windef.yaml` (92), `winnt-core.yaml` (47), `winuser-core.yaml` (688), `wingdi-core.yaml` (176), `winsock.yaml` (202), `commctrl-ce.yaml` (237) — 1,442 unique ids total | curated (P0) + `tools/gen_area_yaml.py` (P1, machine-generated then hand-curatable) |

## Regeneration

```sh
curl -s "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/toc.json" -o /tmp/embedded-root-toc.json
python3 tools/extract_mslearn_index.py   # writes mslearn-doc-index/ (+ gz snapshots)
python3 tools/build_inventories.py       # writes mslearn-inventories/
python3 tools/harvest_facts.py           # re-harvests the core fact pages (network)
python3 tools/harvest_area.py ce60:window-control ce50:window-control   # area harvests (network)
python3 tools/harvest_area.py ce60:gwes ce50:gwes --sub '^(Windows Reference|Window Class Reference|Window and Control Styles|Windows Timer Reference|Window Properties Reference|System Information Reference|Message Queue Reference|Keyboard Reference|Resources Reference)$' --out ce50-ce60-winuser
python3 tools/harvest_ce60_keyboard.py  # supplements the CE 6.0 keyboard pages from the doc index
python3 tools/extract_style_tables.py && python3 tools/extract_flag_tables.py
python3 tools/extract_winsock_errors.py
python3 tools/gen_area_yaml.py           # regenerates the four P1 fact YAMLs
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
