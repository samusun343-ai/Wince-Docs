# Audit — MinGW.org w32api (including the CeGCC-maintained lineage)

Registry id: `mingw-org-w32api`
Retrieved / verified: 2026-11-07

## 1. Identity

* Project: **w32api — "Free headers and libraries for the Win32 API"**, originally by Anders Norlander, maintained by the MinGW project (`README.w32api`).
* Examined artifact: the CeGCC-lineage maintenance fork `https://github.com/MaxKellermann/w32api` (default branch `wip`), tarball fetched 2026-11-07 (1.37 MB, 658 files). This is the artifact CeGCC builds against (see `cegcc.md`), i.e. the header set whose lineage this project adopts as its permissive-code anchor.

## 2. License evidence (quoted from `README.w32api` in the fetched tree)

> "Unless otherwise stated in individual source files,
>
> **THIS SOFTWARE IS NOT COPYRIGHTED**
>
> This source code is offered for use in the public domain. You may use, modify or distribute it freely. […] This source code is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY."

**Per-file exceptions stated in the same README (must be respected on any reuse):**

| Files | Copyright / license |
| --- | --- |
| `winsock.h`, `winsock2.h`, `ws2tcpip.h` (portions) | © 1980, 1983, 1988, 1993 The Regents of the University of California; © 1993 Digital Equipment Corporation (BSD-style) |
| `gl.h` | © 1999–2001 Brian Paul (Mesa 3-D) |
| `glext.h`, `glu.h` | © 1991–2000 Silicon Graphics, Inc. — SGI Free Software License B, v1.1 |

## 3. CE-specific content observed in the CeGCC lineage (facts for our specs)

* `ChangeLog.ce` (Danny Backx, Pedro Alves, 2009–2010) documents CE adaptations, e.g.: `BY_HANDLE_FILE_INFORMATION` gains `DWORD dwOID` on CE; `DebugBreak` becomes a macro on CE (arm/x86); `ws2tcpip.h` `getaddrinfo` family defined for CE.
* `include/windef.h` contains the CE integration layer:
  * defaults `_WIN32_WCE` to `0x0300` when building with `__CEGCC__`/`__MINGW32CE__`;
  * defines the `_WNAME` macro with the comment: *"WinCE functions not receiving LPTSTR directly don't have W suffix, even though they are implicitly wide"* — direct engineering evidence for the A/W policy (`unicode-aw-policy.md`);
  * `MAX_PATH 260`, standard calling-convention macros.
* `include/winbase.h`: `#define MAXIMUM_WAIT_OBJECTS 64` (Class B evidence; CE docs reference the constant without a value ⇒ recorded `verify-runtime`).
* `include/winnt.h`: `#define VER_PLATFORM_WIN32_CE 3` (agrees with the MSDN Magazine statement).
* CE-only headers present: `aygshell.h`, `phone.h`, `sms.h`, `simmgr.h`, `kfuncs.h`, … plus `af_irda.h` etc.

## 4. Assessment

* **Public domain** (with per-file exceptions) ⇒ both fact extraction and code reuse are permitted.
* Provenance caveat (recorded honestly): the historical MinGW w32api was itself authored from public documentation and PD contributions; this project still **prefers official documentation for every fact** and uses w32api as (a) cross-evidence, (b) the architectural reference for the include tree, and (c) the licensed reuse base for the desktop-common parts, per the project's "permissive parts only, after audit" directive.
* Reuse rules for the implementation role: file-level license exceptions above MUST be honored with attribution; CE-specific deltas in the CeGCC lineage (ChangeLog.ce items) are facts to re-verify against official docs, not code to import blindly.

## 5. Conclusion

**APPROVED (Class B)** — the designated permissive-code anchor; reuse permitted within the audited boundaries.
