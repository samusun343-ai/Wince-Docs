# Audit — mingw-w64

Registry id: `mingw-w64`
Retrieved / verified: 2026-11-07

## 1. Identity

* Project: mingw-w64 — the successor MinGW runtime/header set for Win32/Win64.
* Examined artifact: GitHub mirror `https://github.com/mirror/mingw-w64`; `COPYING` fetched from `raw.githubusercontent.com/mirror/mingw-w64/master/COPYING` (HTTP 200).

## 2. License evidence (quoted from `COPYING`)

> "With exception of certain parts that are prominently marked as being in the Public Domain, BSD, or LGPL this Software is provided under the **Zope Public License (ZPL) Version 2.1**.
> Copyright (c) 2009 - 2013 by the mingw-w64 project […]"

The COPYING does not enumerate which parts carry which exception license; those are marked in the individual files.

## 3. Assessment for this project

* ZPL 2.1 is GPL-compatible and permissive enough for reuse; however:
  1. mingw-w64's header set is **Win32/Win64-oriented** — per charter C-1 (**"w64 is not wince; excluded"**), its Win64 dimension and any desktop-only structures are out of scope for reuse;
  2. the per-file license marking ("prominently marked" exceptions) makes file-level reuse contingent on a per-file scan that has not been performed here.
* Its **organization** (header layering, `psdk-inc`-style grouping, def/import-library tooling, header test suites) is an excellent structural reference.

## 4. Usage rules

1. **Structural reference only** in this phase (include-tree organization, def generation tooling design, conformance-test patterns).
2. Any future code reuse requires: per-file license scan + attribution + exclusion of Win64-only content; a new audit entry MUST document the scan.

## 5. Conclusion

**APPROVED (Class B, structural-reference scope)** — code reuse deferred pending per-file audit; Win64 content permanently excluded.
