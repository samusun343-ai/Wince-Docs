# Project Charter

Status: Approved for Phase 0/1 | Language authority: English | Normative references: RFC 2119

## 1. Mission

Produce the **complete information base and specification** required to construct a MinGW-equivalent header and import-library set (`include/` + `def/`) for Windows CE 4.x / 5.0 / 6.0 application development, under a strict clean-room methodology, using only sources that are verifiably public and license-clean.

## 2. Background and problem statement

Developing native C/C++ applications for Windows CE today requires either:

1. Microsoft's proprietary SDKs / Platform Builder (license-restricted, unredistributable), or
2. CeGCC (GPL toolchain aggregation; headers borrowed from the MinGW project's w32api module; last general-availability state dates from ~2010), or
3. Hand-made headers of uncertain provenance copied from SDK leaks (legally unsound).

There is no maintained, license-audited, redistributable WinCE API definition set. The equivalent for desktop Win32 exists: the MinGW / MinGW-w64 projects. This project aims at the same quality bar for Windows CE **without inheriting any license-tainted material**.

### 2.1 Platform characterisation (normative constraints)

The following constraints govern every technical decision in this project:

* **C-1 — WinCE is not Win64.** Windows CE is a 32-bit-only operating system. There is no LLP64 model, no 64-bit handle scheme, no WOW layer. Any Win64-only concept (pointer-size polymorphism, `*_32`/`*_64` API pairs, `LONG_PTR` semantics differing from `LONG`, etc.) is **out of scope** and MUST NOT be imported from Win64-oriented sources.
* **C-2 — WinCE partially shares Win32.** A substantial subset of the surface is identical in name, signature and semantics to desktop Win32; another subset shares names but has **CE-specific values, struct fields, parameter behaviour or limits** (e.g. `BY_HANDLE_FILE_INFORMATION` gains `dwOID` on CE; `CreateFile` rejects `FILE_FLAG_OVERLAPPED`; there is no current directory); and a third subset is **CE-only** (e.g. `ReadFileWithSeek`, `SHCreateMenuBar`). Every fact record MUST classify into one of these categories (`class: common | ce-modified | ce-only`; see the fact schema).
* **C-3 — Unicode-native with a non-standard A/W surface.** CE is a Unicode platform; however, unlike desktop Win32, exported symbol naming is inconsistent: some APIs are exported with a `W` suffix, others without any suffix while still being wide-only. The A/W layer is specified in `docs/03-requirements/unicode-aw-policy.md`.
* **C-4 — Single-dominant-DLL import model.** The core API surface resolves overwhelmingly to `coredll.dll`, with CE-specific satellite libraries (`Msgbox.lib`, `Ws2.lib`, `aygshell.lib`, …). The `.def` requirements are specified in `docs/03-requirements/def-requirements.md`.

## 3. Scope

### 3.1 In scope (Phase 0/1 — this repository)

1. Identification, license-audit and registration of usable public information sources (MSDN/MS Learn, pinvoke.net, GitHub-hosted Win32 documentation projects, permissively-licensed OSS, CeGCC's *sources* — not its code).
2. Machine-readable **documentation inventories** covering the full CE 1.0–6.0 collection range (with emphasis on the CE 4/5/6 targets).
3. **Fact database**: per-function / per-structure / per-constant records with values, signatures, header and library mapping, OS-version availability, provenance.
4. **Normative specifications** for the header set architecture, version gating, A/W mapping, and import-library (`.def`) generation.
5. First-batch **full-enumeration header specifications** (`windef.h`, `winnt.h` core, `winerror.h`, `winbase.h` core).

### 3.2 Out of scope (Phase 0/1)

* Writing any actual `.h` / `.def` files (implementation role, Phase 1).
* Building or modifying a compiler toolchain (CeGCC or otherwise).
* Distributing any Microsoft material.
* Targeting Windows Embedded Compact 7 / 2013 (kept in the documentation index only as context).

### 3.3 Target matrix summary

| Dimension | Value |
| --- | --- |
| Build targets | CE 4.0, 4.1, 4.2, 5.0, 6.0 (incl. 6.0 R2/R3 where documented) |
| Collection range | CE 1.0 → 6.0 R3 (all releases) |
| Architectures | ARM (v4/v4I/v4T…), MIPS (II/IV, MIPS16), SH-3/SH-4, x86 — see `docs/03-requirements/target-matrix.md` |
| API surface | Application-level Win32-equivalent + CE-specific APIs as documented in the official reference |

## 4. Deliverables and their acceptance criteria

| ID | Deliverable | Acceptance criterion |
| --- | --- | --- |
| D1 | Source registry + audits (`docs/02-sources/`) | Every source used by any fact record has an audit entry with license evidence and retrieval date |
| D2 | Documentation indexes (`data/mslearn-doc-index/`) | Regenerable by `tools/extract_mslearn_index.py`; counts reproducible |
| D3 | Curated inventories (`data/mslearn-inventories/`) | One file per area per version; page lists match the live TOC |
| D4 | Fact database (`data/mslearn-facts/`, `data/facts/`) | Every record schema-valid; every `src[]` resolves to the source registry |
| D5 | Architecture + requirement specs (`docs/03-requirements/`, `docs/04-architecture/`) | No normative statement without a source or an explicit open-question marker |
| D6 | First-batch header specs (`docs/05-specs/`) | Full enumeration with values for the declared batch; classification per C-2 for every item |
| D7 | Validation tooling (`tools/validate.py`) | Passes on the repository as delivered |

## 5. Relationship to prior art

| Project | Relationship |
| --- | --- |
| MinGW.org / w32api | **Adopted source** (public-domain headers, audited). Architecture reference and the only permitted code-reuse candidate |
| MinGW-w64 | Structural reference only; its Win64 dimension is excluded by C-1 |
| CeGCC | *Not* a code source and this project is not a CeGCC fork. Its **adopted sources** are adopted here (chiefly: MinGW w32api + Microsoft documentation) |
| Wine, ReactOS | **Structural/design reference only** (LGPL/GPL respectively; never WinCE anyway per C-1/C-2) |
| Windows CE Shared Source / PB / SDKs | **Rejected** as sources (license-restricted) |

## 6. Phase plan

* **Phase 0 (complete):** source discovery, license audits, full documentation indexing.
* **Phase 1 (this delivery):** methodology + framework specs + first-batch enumerations + tooling.
* **Phase 2 (future, implementation role):** generate headers/defs from the fact database; conformance testing per `docs/04-architecture/conformance-testing.md`.
* **Phase 3 (future):** expand coverage area-by-area following the priority order in `docs/03-requirements/header-inventory.md`.

## 7. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as described in RFC 2119.
