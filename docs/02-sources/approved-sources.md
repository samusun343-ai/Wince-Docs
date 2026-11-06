# Approved Source Registry

Status: Normative registry | Last audited: 2026-11-07

`src[]` references in fact records MUST use the `id` column below. Every entry links to an audit record with license evidence.

## Class A — official documentation (fact extraction with citation)

| id | Source | License / basis | Audit |
| --- | --- | --- | --- |
| `mslearn-ce60` | **Windows Embedded CE 6.0 documentation** (MS Learn, previous-versions; live TOC with 23,713 pages incl. R2/R3-era content) | Publicly accessible official Microsoft documentation; facts cited, no wholesale copying | [audits/mslearn-wince.md](audits/mslearn-wince.md) |
| `mslearn-ce50` | **Windows CE 5.0 documentation** (MS Learn, previous-versions; 22,889 pages) | same | [audits/mslearn-wince.md](audits/mslearn-wince.md) |
| `mslearn-ce40` | **Windows CE .NET (4.x) documentation** (MS Learn, previous-versions; 6,362 pages; partially migrated) | same | [audits/mslearn-wince.md](audits/mslearn-wince.md) |
| `mslearn-ce30-legacy` | Orphaned **Windows CE 3.0** pages under `previous-versions/msXXXXXX(v=msdn.10)` (e.g. `ms958493`) | same | [audits/mslearn-wince.md](audits/mslearn-wince.md) |
| `mslearn-wec7-2013` | Windows Embedded Compact 7 / 2013 documentation (context only; out of target scope) | same | [audits/mslearn-wince.md](audits/mslearn-wince.md) |
| `mslearn-win32` | **Desktop Win32 API documentation** (live MS Learn `windows/win32` tree) — for the *common* subset of constants/signatures per charter C-2 | Publicly accessible official Microsoft documentation | [audits/mslearn-win32.md](audits/mslearn-win32.md) |
| `microsoftdocs-win32` | **MicrosoftDocs/win32 GitHub repository** (source repo of the desktop Win32 docs) | Content **CC-BY-4.0**, code snippets **MIT** (LICENSE fetched and verified) | [audits/microsoftdocs-win32.md](audits/microsoftdocs-win32.md) |
| `msdn-mag-archive` | **MSDN Magazine archive on Microsoft Learn** (e.g. CE 6.0 and CE .NET feature articles) | Publicly accessible official Microsoft archive | [audits/mslearn-win32.md](audits/mslearn-win32.md) |
| `mslearn-lifecycle` | Microsoft Learn **product lifecycle** pages (version dating) | Publicly accessible | [audits/mslearn-win32.md](audits/mslearn-win32.md) |
| `wayback-msdn` | Wayback Machine snapshots of original `msdn.microsoft.com` / `docs.microsoft.com` URLs (for pages removed from Learn) | Archived copy of Microsoft's own publication; cite original + snapshot URL | [audits/mslearn-wince.md](audits/mslearn-wince.md) |

## Class B — permissive open-source code (facts + conditional reuse)

| id | Source | License / basis | Audit |
| --- | --- | --- | --- |
| `mingw-org-w32api` | **MinGW.org w32api** ("Free headers and libraries for the Win32 API"), including the CE-adapted lineage maintained as `MaxKellermann/w32api` (branch `wip`, used by CeGCC; `ChangeLog.ce` documents the CE deltas) | **Public domain** per `README.w32api`, with per-file exceptions: `winsock.h`, `winsock2.h`, `ws2tcpip.h` (BSD Regents/DEC), `gl.h` (Mesa), `glext.h`/`glu.h` (SGI FreeB 1.1) | [audits/mingw-org-w32api.md](audits/mingw-org-w32api.md) |
| `mingw-w64` | **mingw-w64** headers (mirror `mirror/mingw-w64`) | **ZPL 2.1** overall, "with exception of certain parts that are prominently marked as being in the Public Domain, BSD, or LGPL" (COPYING verified). Win64-specific content **excluded** from all reuse per charter C-1; structural reference only | [audits/mingw-w64.md](audits/mingw-w64.md) |

## Class C — structural reference only (never copy)

| id | Source | License / basis | Audit |
| --- | --- | --- | --- |
| `wine` | Wine project (`wine-mirror/wine` on GitHub; include/ tree organization) | **LGPL-2.1+** (LICENSE verified) | [audits/wine-reactos.md](audits/wine-reactos.md) |
| `reactos` | ReactOS (`reactos/reactos`; `sdk/include/` organization) | **GPL-2.0** (COPYING verified) | [audits/wine-reactos.md](audits/wine-reactos.md) |

## Class D — restricted (cross-check only, no copying)

| id | Source | License / basis | Audit |
| --- | --- | --- | --- |
| `pinvoke-net` | pinvoke.net interop wiki (includes `coredll`, `aygshell`, `ipaqutil` modules) | **No machine-readable license statement could be located** on the site (checked homepage, FAQ, content pages on 2026-11-07); user-contributed wiki | [audits/pinvoke-net.md](audits/pinvoke-net.md) |

## Reference (not fact sources)

| id | Source | Use | Audit |
| --- | --- | --- | --- |
| `cegcc` | CeGCC project (SourceForge; docs at `cegcc.sourceforge.net/docs/`) | Adopted-*sources* reference (it borrowed its headers from MinGW w32api — confirmed in its own docs) and toolchain-behaviour reference. **Not** a code source; this project is not a CeGCC fork | [audits/cegcc.md](audits/cegcc.md) |

## Rules of use

1. `mslearn-ce60`/`mslearn-ce50`/`mslearn-ce40` are the **primary** fact sources; every other source is secondary or cross-check.
2. `mingw-org-w32api` is the only asset from which implementation-phase code may be reused, and only from files whose license allows it (exceptions above MUST be respected; reuse requires attribution notes in the generated files).
3. `wine`/`reactos`/`mingw-w64` influence *organization and technique* only (e.g. how to layer A/W macros, how to structure `.def` tooling). No content may be copied from them into either this repository or the implementation.
4. `pinvoke-net` may be consulted to cross-check a signature or constant, but MUST NOT be quoted, and cannot be a sole source for any fact (two-channel rule, `verification-policy.md` §2).
