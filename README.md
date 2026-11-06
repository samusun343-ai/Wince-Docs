# Wince-Docs — Clean-Room Research & Specification for Windows CE `include`/`def`

**Status:** Phase 0/1 — Information collection and specification (this repository's current scope).
**Target platforms:** Windows CE 4.x / 5.0 / 6.0 (information collection additionally covers all releases, CE 1.0 through 6.0 R3).
**Goal:** produce a complete, license-clean, engineering-grade **specification suite and machine-readable fact database** sufficient for a separate implementation role to build a MinGW-class header and import-library set (`include/` + `def/`) for Windows CE application development — *without* the implementer ever having to consult license-restricted or provenance-uncertain material.

This repository intentionally contains **no Microsoft-copyrighted header code and no SDK dumps**. Every fact in it is either:

1. extracted from publicly accessible, official Microsoft documentation (MS Learn / archived MSDN content) and recorded with a source citation and retrieval date, or
2. taken from permissively-licensed open-source material whose license and provenance have been audited (see `docs/02-sources/`), or
3. explicitly marked as an open question with a defined verification method.

## Why this is a specification, not prose

The deliverable is designed to be directly consumable by an implementation role:

* **Normative language** (RFC 2119) throughout `docs/`.
* **Machine-readable fact database** under `data/` (JSON/YAML) with a fixed record schema (`docs/05-specs/spec-template.md`) — every record carries `src[]` provenance that a validator can check.
* **Complete inventories**: the full MS Learn CE 4/5/6 documentation page indexes (23,713 / 22,889 / 6,362 pages) are snapshotted, plus curated per-area API reference inventories that define the *entire* scope of the future header set — nothing is left implicit.
* **Worked full-enumeration specs** for the first batch (`windef.h`, `winnt.h` core, `winerror.h` complete with all 571 documented CE system error codes, `winbase.h` core functions) that establish the pattern every subsequent header spec must follow.
* **Tooling**: every dataset is regenerable with the scripts under `tools/`; `tools/validate.py` enforces schema and citation integrity.

## Document map

| Path | Content |
| --- | --- |
| `docs/00-charter/` | Project charter, scope, role separation (research/spec vs. implementation vs. verification) |
| `docs/01-methodology/` | Clean-room policy, source admission policy, fact verification policy |
| `docs/02-sources/` | Approved source registry, per-source license audits, rejected sources with rationale |
| `docs/03-requirements/` | Target environment matrix, Unicode A/W policy, header inventory (full roadmap), `.def` requirements |
| `docs/04-architecture/` | Include tree layout, version gating, `.def` generation, conformance testing strategy |
| `docs/05-specs/` | Per-header specification template + first-batch full-enumeration specs |
| `docs/06-appendix/` | CE version history, open questions with verification methods |
| `data/` | Documentation indexes, curated API inventories, harvested fact records, spec-level fact YAML |
| `tools/` | Regeneration and validation scripts |

## Key findings so far (Phase 0 highlights)

* The **entire Windows CE 5.0 and Windows Embedded CE 6.0 product documentation trees are still live on Microsoft Learn** under `previous-versions/windows/embedded/` (CE 6.0: 23,713 pages; CE 5.0: 22,889; Windows CE .NET 4.x: 6,362) — confirmed by walking the official TOC JSON. This is the primary clean fact source. (`data/mslearn-doc-index/`, audit `docs/02-sources/audits/mslearn-wince.md`)
* Every CE function page carries a **Requirements** block (`Header: …`, `Link Library: …`, `OS Versions: …`). 64 core pages harvested so far show the import-library model: `coredll.lib` for the core, `Msgbox.lib` for `MessageBox`, `Ws2.lib` for Winsock, and a CE 5.0 quirk of `Nk.lib` for `WaitForMultipleObjects`. (`data/mslearn-facts/`)
* The complete documented **CE 6.0 system error table (571 codes, 0–6118) was extracted** from the official docs and is byte-for-byte consistent with CE 5.0's table except for one CE 6.0 addition (`ERROR_DEVICE_REMOVED`). (`data/mslearn-facts/ce60-system-errors.json`)
* CeGCC (which this project deliberately is *not* a fork of) itself **borrowed its headers from the MinGW project's w32api module** — public-domain licensed with audited exceptions. That lineage is adopted here as the reference for header architecture and as the only code-reuse candidate. (`docs/02-sources/audits/cegcc.md`, `docs/02-sources/audits/mingw-org-w32api.md`)
* **Windows CE Shared Source** and all Platform Builder / SDK header material are **rejected as information sources** (license-restricted, per project constraints).

## Repository layout

```
Wince-Docs/
├── README.md                  <- you are here
├── docs/
│   ├── 00-charter/  01-methodology/  02-sources/
│   ├── 03-requirements/  04-architecture/
│   ├── 05-specs/  06-appendix/
├── data/
│   ├── mslearn-doc-index/     <- full page indexes (gzip snapshots + stats)
│   ├── mslearn-inventories/   <- curated per-area API reference inventories
│   ├── mslearn-facts/         <- harvested per-page fact records + error tables
│   └── facts/                 <- spec-level enumerated facts (YAML)
└── tools/                     <- regeneration + validation scripts
```

## Regenerating the data

```sh
# 1. download the MS Learn embedded TOC (single JSON, ~12 MB)
curl -s "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/toc.json" -o /tmp/embedded-root-toc.json
# 2. extract the per-version page indexes
python3 tools/extract_mslearn_index.py
# 3. build the curated inventories
python3 tools/build_inventories.py
# 4. harvest the fact records (subset list is defined inside the script)
python3 tools/harvest_facts.py
# 5. validate everything
python3 tools/validate.py
```

## License / rights posture

* All documents in `docs/` are original work of this project. The repository does not yet declare a distribution license (deliberate; see `docs/06-appendix/open-questions.md`).
* Data under `data/` consists of **factual extractions** (identifiers, numeric values, signatures, requirement mappings) from the sources cited in each record, with attribution. Prose is excerpted only in short, attributed fragments for technical necessity.
* No Microsoft-copyrighted source code is included. See `docs/01-methodology/source-policy.md` for the rules that guarantee this.
