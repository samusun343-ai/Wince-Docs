# Include Tree Architecture

Status: Normative (target layout for the Phase 2 implementation)

## 1. Design inputs

* The header organization of the public-domain **MinGW.org w32api** (`mingw-org-w32api` audit) — the same lineage CeGCC adopted — is the architectural baseline: flat `include/` tree, `windows.h` umbrella, dependency-ordered includes.
* Deviations are driven by: (a) CE-specific modules (`coredll`, `msgqueue`, `toolhelp`, `aygshell`, …); (b) charter C-1 (no Win64 layer); (c) the fact-DB-driven generation process.

## 2. Target layout

```
include/
├── windows.h            umbrella (windef → winnt → winerror? no—see order below → winbase → winuser → wingdi …)
├── windef.h             base types, calling conventions, basic macros        [P0 spec delivered]
├── winnt.h              core types, RTL structs, platform constants          [P0 core spec delivered]
├── winerror.h           system error codes (571 documented)                  [P0 spec delivered]
├── winbase.h            core OS API (process/mem/sync/time/file/dll/…)       [P0 core spec delivered]
├── winuser.h            GWES windowing/messages                              [P1]
├── wingdi.h             GDI                                                  [P1]
├── windowsx.h           window/control helper macros                         [P1]
├── commctrl.h           common controls (incl. CE command bands/bars)        [P1]
├── commdlg.h            common dialogs                                       [P1]
├── winsock.h / winsock2.h / ws2tcpip.h                                        [P1; w32api file-level BSD notices if reused]
├── msgqueue.h           point-to-point message queues (CE-only area)         [P1]
├── toolhelp.h           toolhelp snapshots                                   [P1]
├── aygshell.h           PocketPC shell extension                             [P1]
├── kfuncs.h             kernel helper functions (CE)                          [P2; cegcc-lineage evidence)
├── …                    (P2 headers follow the inventory in header-inventory.md)
└── cefixup/             (optional) CE-compat shims for portable sources: e.g. ANSI-stub macros
def/
├── coredll.def (+ .def.map sidecars)
├── msgbox.def
├── ws2.def
├── nk.def
└── …                    (per def-requirements.md)
```

## 3. Include order and dependency DAG (normative subset)

```
windef.h  ←  winnt.h  ←  winerror.h? (no: winerror depends only on winnt types)
                 ↑
             winbase.h  ←  winuser.h  ←  wingdi.h …
```

* `windows.h` includes, in order: `windef.h`, `winnt.h`, `winerror.h`*, `winbase.h`, `winuser.h`, `wingdi.h`, then (gated) `winsock2.h`-family, `commctrl.h`/`commdlg.h` behind `WIN32_LEAN_AND_MEAN`-style gates. (*Desktop `winerror.h` is pulled by `windows.h`; the spec keeps the same order for source compatibility.)
* A header MUST NOT include a "higher" header (no cycles): `winnt.h` includes only `windef.h`(types) — the exact edge list is generated from the fact DB's `target_header`/dependency fields during Phase 2.
* Every header carries an include guard named `_<FILE>_H` (w32api-compatible) and a provenance banner citing the spec files and source registry ids it was generated from (clean-room traceability requirement).

## 4. Naming and macro conventions

* File names mirror the documented `Requirements → Header` values (e.g. `Winsock2.h` → `winsock2.h`), preserving source compatibility for portable code.
* `#define`s use documented names verbatim; CE-only additions live in CE-named headers, never silently inside common headers.
* Packing: no `#pragma pack` unless a documented structure requires non-default packing; recorded per-structure in the fact DB (default packing assumption: 8-byte, `verify-runtime` on ARM/MIPS/SH — OQ-7).

## 5. CRT boundary

* The OS header set declares only the OS API surface (coredll & satellites). It does **not** provide the C runtime.
* The implementation phase MAY pair the headers with any clean CRT strategy (newlib, a from-scratch coredll-CRT, or CeGCC-compatible glue), but CRT headers (`stdio.h` etc.) are a separate deliverable with a separate spec — deliberately out of this repository's current scope to remain CeGCC-independent.
* R-AW-5 reminder: no OS header fakes CRT symbols.

## 6. Generation, not authoring

The implementation SHOULD be generated from `data/facts/` + `data/mslearn-facts/` by a build script (Phase 2), so that the specs remain the single source of truth and the clean-room chain is mechanical:

```
data/facts/*.yaml  ──tools/gen_headers.py (Phase 2)──►  include/*.h
data/mslearn-facts/*.json + def-requirements §4 ──►    def/*.def
```
