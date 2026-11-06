# Source Admission Policy

Status: Normative | Governs: which information sources this project may use, and how

## 1. Source classes

| Class | Definition | Permitted use | Examples |
| --- | --- | --- | --- |
| **A** | Official, publicly accessible documentation of the platform owner | Fact extraction with citation; short attributed excerpts | MS Learn Windows CE 5.0 / CE 6.0 / CE .NET docs, desktop Win32 docs, MSDN Magazine archive on Learn, lifecycle pages |
| **B** | Permissively-licensed open-source code with auditable provenance | Fact extraction **and** conditional code reuse per audit | MinGW.org w32api (public domain, with per-file exceptions), MinGW-w64 (ZPL 2.1 + marked exceptions — Win64 content excluded per charter C-1) |
| **C** | Copyleft open-source projects relevant structurally | Structure/design study only; never copying | Wine (LGPL-2.1+), ReactOS (GPL-2.0) |
| **D** | Public community resources with unclear or unverifiable licensing | Manual fact cross-checking only; no copying whatsoever | pinvoke.net |
| **R** | Rejected | None | see §4 |

## 2. Admission criteria (all MUST hold)

1. **Identifiable origin** — the publisher/author is known (official Microsoft property, or a named OSS project with a public repository).
2. **License clarity** — for code: an explicit license with redistribution and derivative-work permissions sufficient for the intended use (facts-only use does not require this, but reuse does). For documentation: public accessibility without NDA/EULA-gated content.
3. **Verifiability** — a stable URL (or archival identity) that others can re-check.
4. **No contamination chain** — the source itself must not be an unauthorized copy of restricted material (this disqualifies SDK mirrors and MSDN CHM re-publishers).

Class B additions additionally require a per-file license scan when reuse (not just fact extraction) is intended.

## 3. Admission procedure

1. File an audit record under `docs/02-sources/audits/<source>.md` containing: description, URLs, license evidence (quote + retrieval date), scope of permitted use, and any file-level exceptions.
2. Add the source to `approved-sources.md` with a unique `id` (`src[]` references in fact records use this id).
3. If rejected, document it in `rejected-sources.md` with rationale.

## 4. Rejected classes (Class R)

| Rejected class | Rationale |
| --- | --- |
| Windows CE Shared Source (all variants) | License-limited to learning/debugging; explicitly excluded by project directive |
| Platform Builder / eVC / VS device SDK headers & libraries | Microsoft-copyrighted, EULA-restricted |
| Unauthorized mirrors of the above (GitHub "wince sdk headers", etc.) | Unauthorized redistribution; provenance/contamination risk |
| Third-party re-publishers of MSDN CHM content | Unauthorized redistribution; prefer live Learn pages or Wayback snapshots of original URLs |
| Reverse-engineered dumps of undocumented internals without official documentation | Legal risk and unverifiable provenance; runtime behavioural probing is the compliant alternative |
| Anything whose origin cannot be confirmed | Project directive: unverifiable origin ⇒ not adopted |

## 5. Current registry summary

The authoritative list lives in `approved-sources.md` / `rejected-sources.md`. Summary counts as of 2026-11-07: Class A: 10 sources; Class B: 2; Class C: 2; Class D: 1; Rejected: 6 classes.
