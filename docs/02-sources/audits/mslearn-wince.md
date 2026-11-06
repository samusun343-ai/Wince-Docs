# Audit — MS Learn Windows CE documentation sets (primary fact source)

Registry ids: `mslearn-ce60`, `mslearn-ce50`, `mslearn-ce40`, `mslearn-ce30-legacy`, `mslearn-wec7-2013`, `wayback-msdn`
Retrieved / verified: 2026-11-07

## 1. Identity and accessibility

* Entry point: `https://learn.microsoft.com/en-us/previous-versions/windows/embedded/` — landing page listing the retired Windows Embedded doc sets (Windows Embedded Compact 2013 / 7, **Windows Embedded CE 6.0**, **Windows CE 5.0**, **Windows CE .NET**, **Windows CE 3.0**, plus others).
* The complete TOC is served as JSON: `https://learn.microsoft.com/en-us/previous-versions/windows/embedded/toc.json` (~12 MB; `children`/`toc_title` nodes, `href` leaf links). This is how the full page inventories in `data/mslearn-doc-index/` were extracted.
* Landing-page links for CE 6.0/5.0/.NET redirect to the Learn home (the doc sets are de-listed), **but the pages themselves remain live** and are served under:
  * CE 6.0: `https://learn.microsoft.com/en-us/previous-versions/windows/embedded/<id>(v=winembedded.60)` (ids `ee4xxxxx`/`ee5xxxxx`)
  * CE 5.0 / CE .NET: `https://learn.microsoft.com/en-us/previous-versions/windows/embedded/<id>(v=msdn.10)` (ids `ms89xxxx`/`aa45xxxx`/`aa51xxxx`…)
  * CE 3.0 legacy: `https://learn.microsoft.com/en-us/previous-versions/<id>(v=msdn.10)` (no `/windows/embedded/` segment; e.g. `ms958493`)

## 2. Measured inventory (extracted 2026-11-07, deduplicated by URL)

| Doc set | Unique leaf pages | Snapshot |
| --- | --- | --- |
| Windows Embedded CE 6.0 (incl. R2/R3 content) | 23,713 | `data/mslearn-doc-index/ce60-doc-index.json.gz` |
| Windows CE 5.0 | 22,889 | `…/ce50-doc-index.json.gz` |
| Windows CE .NET (4.x, partially migrated) | 6,362 | `…/ce40-doc-index.json.gz` |
| Windows Embedded Compact 2013 / 7 (context) | 16,863 / 20,286 | `…/wec2013-doc-index.json.gz`, `…/wec7-doc-index.json.gz` |
| Windows CE 3.0 | TOC reduced to a single landing node; legacy pages survive as orphans | n/a |

## 3. Structure relevant to fact extraction

Each API reference page follows the classic MSDN layout and contains, verifiably:

* `<h1>` title of the form `<Name> (Windows Embedded CE 6.0)` / `(Windows CE 5.0)`;
* a **Syntax** code block (C signature or `typedef struct`);
* a **Requirements** block stating **OS Versions** (e.g. "Windows CE 1.0 and later"), **Header** (e.g. `winbase.h`), and **Link Library** (e.g. `coredll.lib`);
* **Remarks** with CE-specific behavioural notes;
* **See Also** cross-links.

Worked examples captured in `data/mslearn-facts/`:

| Example | Evidence |
| --- | --- |
| `CreateProcess` (CE 6.0) | header `winbase.h`, library `coredll.lib`, "Windows CE 1.0 and later"; CE search-order remarks |
| `MessageBox` (CE 5.0 & 6.0) | header `Windows.h`, library `Msgbox.lib` (CE-specific import library) |
| `WaitForMultipleObjects` | CE 5.0 page: library `Nk.lib`; CE 6.0 page: library `Nk.lib`; nCount "maximum number of object handles is MAXIMUM_WAIT_OBJECTS" |
| `WSAStartup` | header `Winsock2.h`, library `Ws2.lib` (CE-specific — desktop uses `Ws2_32.lib`) |
| `BY_HANDLE_FILE_INFORMATION` (CE 6.0) | structure **includes the CE-only member `DWORD dwOID`** — direct evidence of a CE-modified struct |
| `System Errors - Numerical Order` (CE 5.0 `aa450919` / CE 6.0 `ee488398`) | full error-code tables (570 / 571 entries, codes 0–6118) extracted to `data/mslearn-facts/ce50-system-errors.json` / `ce60-system-errors.json` |

## 4. License / rights assessment

* Content is Microsoft's copyrighted documentation, published at public URLs. Pages carry the standard Learn footer (Terms of Use / Trademarks; the archived doc sets additionally note they are no longer maintained).
* **Permitted use for this project:** extraction of interoperability facts (identifiers, signatures, numeric values, requirement mappings) with citation — consistent with the clean-room policy (facts ≠ expression; `cleanroom-policy.md` R-1/R-2).
* **Not permitted:** wholesale copying of documentation text, re-hosting, or removing attribution.
* Because these doc sets are retired and link-rot is ongoing, all harvested records carry `retrieved` dates; the full page indexes are snapshotted in this repository so the collection survives removal.

## 5. Wayback channel (`wayback-msdn`)

For pages that have already disappeared from Learn (notably most CE 1.x–3.0-era content), the Wayback Machine snapshots of the original `msdn.microsoft.com`/`docs.microsoft.com` URLs are the approved fallback; cite the original URL plus snapshot. Not yet needed for the Phase 1 fact set.

## 6. Conclusion

**APPROVED (Class A)** as the primary fact source for all Windows CE versions in collection scope.
