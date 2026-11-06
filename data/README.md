# Data Directory — Contents and Regeneration

All datasets in this directory are **factual extractions** with per-record provenance (see `docs/01-methodology/verification-policy.md`). Nothing here is copied expressive content.

## Layout

| Path | Content | How produced |
| --- | --- | --- |
| `mslearn-doc-index/` | Full page indexes of the MS Learn Windows CE documentation sets (one JSON per doc set; gzip snapshots + stats) | `tools/extract_mslearn_index.py` |
| `mslearn-inventories/` | Curated per-area API reference page lists (`ce60/`, `ce50/`, `ce40/`; areas: core-os, file-io, gwes, gdi, window-control, shell, winsock, common-controls, error-values) | `tools/build_inventories.py` |
| `mslearn-facts/` | Harvested per-page fact records: `ce60-core-facts.json` (33 pages), `ce50-core-facts.json` (31 pages), `ce60-system-errors.json` (571 codes), `ce50-system-errors.json` (570 codes) | `tools/harvest_facts.py` |
| `facts/` | Spec-level enumerated fact databases: `windef.yaml` (93 records), `winnt-core.yaml` (46 records) | curated from the audited sources |

## Regeneration

```sh
curl -s "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/toc.json" -o /tmp/embedded-root-toc.json
python3 tools/extract_mslearn_index.py   # writes mslearn-doc-index/ (+ gz snapshots)
python3 tools/build_inventories.py       # writes mslearn-inventories/
python3 tools/harvest_facts.py           # re-harvests the core fact pages (network)
python3 tools/validate.py                # schema + provenance validation
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
* **harvested facts**: see `docs/05-specs/spec-template.md` §3 and the samples in any JSON
* **system errors**: `{ "code": int, "name": "ERROR_…", "desc": "one-line factual description" }` (+ docset/url/retrieved envelope)

## Rights note

Facts are extracted from the official Microsoft documentation pages cited in each record (`retrieved` dates included). The indexes are bibliographies of Microsoft-published pages, not copies of their content. Distribution licensing of this dataset is pending the repository-license decision (OQ-11).
