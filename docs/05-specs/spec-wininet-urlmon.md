# Specification — WinInet and URL Moniker Services (`wininet.h`, `urlmon.h`)

Status: final (P3 harvest batch) | Priority: P2 | Fact sources: `data/facts/wininet.yaml` (108), `urlmon.yaml` (96) — 204 records
Harvest basis: WinInet Reference 108+105, URL Moniker Services Reference 72+72, URL Security Zones Reference 41+39, Asynchronous Pluggable Protocols Reference 36+36, plus the ce40 urlmon subset 144 — 860 harvested pages.

## 1. Purpose and scope

The documented CE HTTP/FTP client stack: WinInet (`wininet.h` — `InternetOpen*`/`InternetConnect`/`HttpOpenRequest`/`InternetReadFile` family, cookie and cache subsets as documented) and URL Moniker Services (`urlmon.h` — `URLDownloadToFile`, the `IBindStatusCallback`/`IInternetProtocol` interface set, URL security zones, and the asynchronous pluggable protocol APP contract).

CE facts: **wininet.lib** (84) and **urlmon.lib** (67) are direct import libraries — no coredll involvement. Introduced distribution peaks 2.0/2.1 (the Pocket PC-era browser stack) with a 4.0 wave (31 wininet records) — CE 4.x devices shipped the browser components optionally.

## 2. Dependencies

`windef.h`, `winnt.h`, `windows.h`; `urlmon.h` depends on the COM object model (`spec-ole-com.md`) for its interface records.

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Interfaces | Structures | Enums | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| WinInet (`wininet.h`) | 108 | 84 | 11 aggregated from method pages (status-callback shapes) | 13 (INTERNET_BUFFERS, URL_COMPONENTS…) | 2 | introduced: 2.1 (35), 4.0 (31), 2.0 (30), 5.0 (11) |
| URL Moniker (`urlmon.h`) | 96 | 38 | 23 (`IBindStatusCallback`, `IInternetProtocol`, `IInternetSecurityMgrSite`…) | 5 | 19 (BINDF_*, URLZONEREG, PUAF…) | introduced: 4.0 (88) — the documented CE urlmon is the 4.x-generation stack |

## 4. A/W and export-form notes

Wide-only throughout (`InternetOpenUrlW` usage; `URLDownloadToFileW`?). The CE pages document generic names; the A/W policy resolves generic → W as everywhere else on CE. No A-variant pages exist in either docset.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0400` | the documented urlmon surface (88 records introduced 4.0) |
| `_WIN32_WCE >= 0x0210` | WinInet base wave |
| `_WIN32_WCE >= 0x0500` | WinInet 5.0 additions (11) |
| runtime | components are SYSGEN-optional (`SYSGEN_IE*`); headers unconditional, exports depend on image |

## 6. Implementation notes for Role B

1. **R-HDR-21**: `wininet.h` and `urlmon.h` standalone, desktop-compatible; do not fold urlmon's interfaces into `objidl.h`.
2. `INTERNET_FLAG_*`, `BINDF_*`, `PUAF_*`, `URLZONE_*` constants: values from w32api lineage channel where present (`wininet.h` is in the audited lineage — good coverage); the rest symbolic (verify-runtime recorded per-record).
3. Interface records (aggregated method pages) are the complete documented protocol set — emit vtable-comment style; `.def` covers functions only.
4. The ce40 urlmon subset (144 pages) confirms 4.x availability of the same names — per-record `introduced` keeps the earliest docset value (4.0).
5. Static-asserts: `sizeof(URL_COMPONENTS)`, `sizeof(INTERNET_BUFFERS)`.

## 7. Closure statement

860 pages → 204 records (three-docset merge for urlmon; two for wininet). Nothing excluded. The IE-embedded MSHTML/DHTML (52) and TV-Style/Multi-Language (130) areas are separate documentation trees deferred to the roadmap (P4); their COM interfaces are not part of this closure.

## 8. Verification hooks

L2: `INTERNET_FLAG_*` numeric equality vs desktop docs. L3: `InternetOpenW` + `InternetCloseHandle` roundtrip; `URLDownloadToFileW` against a local HTTP server on a browser-equipped image.
