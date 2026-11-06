# Audit — Wine and ReactOS (structural reference only)

Registry ids: `wine`, `reactos`
Retrieved / verified: 2026-11-07

## 1. Wine

* Identity: the Windows-on-Unix implementation; headers under `include/` of the source tree.
* License evidence: `https://raw.githubusercontent.com/wine-mirror/wine/master/LICENSE` (fetched 2026-11-07) — *"Copyright (c) 1993-2026 the Wine project authors […] under the terms of the **GNU Lesser General Public License** […] version 2.1"*.
* Assessment: LGPL-2.1+; neither the license nor the platform (Wine targets desktop Win32, **not** Windows CE — per project directive Wine is not a WinCE information source) permits/justifies content adoption. **Structural reference only**: e.g. how a large, self-consistent Win32 header set organizes A/W macro layering and per-version gating.

## 2. ReactOS

* Identity: the open-source Windows-compatible OS; SDK headers under `sdk/include/`.
* License evidence: `https://raw.githubusercontent.com/reactos/reactos/master/COPYING` (fetched 2026-11-07) — **GNU GPL version 2**.
* Assessment: GPL-2.0 and desktop-Win32-oriented — same conclusion as Wine. **Structural reference only** (e.g. its `sdk/include/reactos/wine`-style layering and `psdk` headers are instructive for organization, nothing more).

## 3. Usage rules (both)

1. May be studied for architecture, file organization, and build technique.
2. No content (code, comments, tables) may be copied into this repository or the future implementation.
3. Facts about Windows CE MUST NOT be sourced from either project (they are not WinCE implementations — project directive).

## 4. Conclusion

**APPROVED (Class C — structural reference only).**
