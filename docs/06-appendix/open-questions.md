# Open Questions and Verification Register

Status: living document | Each item has an owner-role and a resolution method. No `status: open` fact may exist without an entry here (validator-enforced).

## OQ-1 — Official Microsoft statement of the `_WIN32_WCE` encoding

* **Fact state:** encoding `(major<<8)|bcd(minor)` is `verified` via two independent sources (CeGCC docs; MinGW w32api lineage usage incl. `0x0420` for 4.20).
* **Missing:** an official Microsoft page stating the values (eVC4/VS2005-era smart-device docs are not on Learn).
* **Resolution (Role A):** search Wayback MSDN for eMbedded Visual C++ documentation of predefined macros; alternatively the MSDN Library CD archives (Internet Archive).
* **Cross-check (Role C):** on-device probe comparing `GetVersionEx` output with the toolchain-predefined `_WIN32_WCE`.

## OQ-2 — Genuine `A`-suffix exports on Windows CE

* **Question:** do any CE system modules export ANSI (`A`) functions (as occasionally claimed for compatibility layers)?
* **Resolution (Role C):** systematic `GetProcAddress` probing of `coredll.dll` / `ws2.dll` / `aygshell.dll` etc. on CE 4/5/6 images for `FooA` variants of documented functions; results recorded as verification report.
* **Default until resolved:** no ANSI surface in headers (R-AW-3).

## OQ-3 — x86 CEPC calling convention for `WINAPI`

* **Question:** on x86 CE, are exported APIs `stdcall` or `cdecl`? (ARM/MIPS/SH are single-convention.)
* **Resolution (Role C):** runtime probe on a CEPC image; also link-test both conventions in a stub DLL.
* **Default until resolved:** `WINAPI = __stdcall` (w32api lineage precedent).

## OQ-4 — Exact per-version processor variant matrix (CE 4.x/5.0)

* **Have:** CE 6.0 official pages (ARM/MIPS II-IV/SH-4/x86 evidence, `target-matrix.md` §2).
* **Missing:** official CE 5.0/4.x page enumerating ARMv4I/MIPS16/SH3/SH4 variants.
* **Resolution (Role A):** harvest the CE 5.0 BSP/processor documentation branch from the already-indexed CE 5.0 tree.

## OQ-5 — Ordinal exports in CE system DLLs

* **Question:** are any OS exports ordinal-only (affecting `.def` R-DEF-2)?
* **Resolution (Role C):** runtime export-table inspection via documented tooling on owned devices; any finding becomes a fact record first.
* **Default:** name-only exports.

## OQ-6 — DLL names behind the import libraries

* **Question:** exact module file names for `Msgbox.lib` (`msgbox.dll`?), `Ws2.lib` (`ws2.dll`?), `Nk.lib`/`Nkstub.lib` (kernel mapping in CE 5 vs 6).
* **Resolution (Role C):** on-device module list + `LoadLibrary` probing; documentation only names the import libraries.
* **Impact:** `LIBRARY` lines in generated `.def` files.

## OQ-7 — Default structure packing on ARM/MIPS/SH

* **Question:** confirm 8-byte default packing (and no per-arch deviation) for the documented structures.
* **Resolution (Role C):** `sizeof`/offset probes on-device for `SYSTEM_INFO`, `OSVERSIONINFO`, `BY_HANDLE_FILE_INFORMATION`.

## OQ-8 — `MAXIMUM_WAIT_OBJECTS` value on CE

* **State:** `verify-runtime` (value 64 from the w32api lineage + desktop docs; CE docs reference the constant without a value).
* **Resolution (Role C):** on-device wait-limit probe across CE 5/6.

## OQ-9 — CE 1.x/2.x documentation sources

* **Question:** the earliest versions' docs are not on Learn; the Internet Archive hosts MSDN Library CD images of the era.
* **Resolution (Role A, when CE 1/2 facts become necessary):** audit the specific archive.org items and record them as `wayback-msdn`-class sources. (CE 4/5/6 work does not block on this.)

## OQ-10 — `ERROR_DEVICE_REMOVED` availability on CE 4.x

* **State:** present in both CE 5.0 and 6.0 tables (only CE5→CE6 difference); CE .NET (4.x) error table page not yet located in the partially-live tree.
* **Resolution (Role A):** locate the CE .NET-era `System Errors` page in the indexed tree; else Role C on-device probe.

## OQ-11 — Repository distribution license — RESOLVED

* **Decision (repository owner session, 2026-11-07):** CC-BY-4.0 for `docs/`, MIT for `data/` and `tools/`.
* Full rationale, scope boundaries and re-user obligations: `docs/01-methodology/licensing.md`; texts under `LICENSES/`; split stated in the root `LICENSE`.
* Kept in this register (rather than deleted) to preserve numbering; no open sub-questions remain.

## OQ-12 — GWES function library bindings — RESOLVED (P1 harvest)

* **Resolution:** the full P1 area harvest (1,795 pages: window-control, winuser subareas, GDI, winsock, commctrl subset) documents the bindings: `coredll.lib`, `commctrl.lib`, `dlgmgr.lib`, `menu.lib`, `clipbd.lib`, `caret.lib`, `kbdui.lib`, `icon.lib`, `accel.lib`, `sbcmn.lib`, `rectapi.lib`, `winmgr.lib`, `wmgr_c.lib`, `wmbase.lib`, `uibase.lib`, `coreimm.lib`, `drawmbar.lib`, `loadbmp.lib`, `loadimg.lib`, `msgbeep.lib`, `msgbox.lib`, `hotkey.lib`, `nclient.lib`, `commdlg.lib`, `fileopen.lib`, `ws2.lib` — all recorded per-record in `data/facts/*.yaml` (`target_lib`).
* **Zero real CE 5.0→6.0 binding changes** in the harvested areas (the only case-normalisation difference `Coredll.lib`→`coredll.lib` is cosmetic).
* Remaining: the runtime **module** (DLL) behind each import library stays OQ-6; the 98 no-library-line functions are OQ-14.

## OQ-13 — *(number retired — the license question was OQ-11, resolved)*

## OQ-14 — Binding hypothesis for pages without a Link Library line

* **State:** 98 winuser + 10 GDI + 34 commctrl-area function pages document a header but no link library (e.g. `CreateWindowEx`, `RegisterClass`, `DefWindowProc`, `ShowWindow`).
* **Hypothesis (Role A):** GWES-bound (`coredll.dll`/`gwes.dll`); on CE 5/6 the SDK linked such functions via coredll exports.
* **Resolution (Role C):** `LoadLibrary`/`GetProcAddress` probe on CE 4/5/6 images; record module facts first, then fix the `.def` LIBRARY lines.

## OQ-15 — Numeric values with no approved source

* **State:** `WS_EX_NOANIMATION`, `WS_NONAVDONEBUTTON`, `LVS_EX_NOFOCUSRECT` are CE-documented names with no value in any approved source (w32api wip predates them; desktop docs lack them).
* **Resolution (Role C):** on-device constant confirmation is impossible (constants are compile-time) — resolve via *behaviour probes* (does setting the documented bit produce the documented behaviour for value candidates?) or by locating a permissively-licensed SDK-era article; if neither succeeds, mark `quarantine` and exclude from headers until proven.

## OQ-16 — `SM_*` index values on-device confirmation

* **State:** the CE pages document the supported/unsupported SM_ name sets; values are w32api-lineage only (`verify-runtime`).
* **Resolution (Role C):** `GetSystemMetrics` sweep on CE 5/6 comparing returns against the w32api values (e.g. `SM_CXSCREEN=0`).

## OQ-17 — Ternary raster operation table extraction

* **State:** the CE "Ternary Raster Operations" page (276 rows) uses a `<dt><strong>NAME</strong></dt><dt>0x…</dt>` layout the current table extractor does not parse; common-subset values carry w32api-lineage records.
* **Resolution (Role A):** extend `tools/extract_flag_tables.py` with the dt-pattern (same as desktop extended-styles pages); cross-check the full 256-entry space.

## OQ-18 — `TEXTMETRIC` / `LOGFONT` member-level CE deltas

* **State:** structure pages harvested with verbatim layouts; a member-by-member diff against desktop has not been run.
* **Resolution (Role A):** scripted layout diff (YAML definitions vs microsoftdocs-win32 structures), then Role C `sizeof`/offset probes.

## OQ-19 — Winsock option constants and `WSAAsyncSelect` absence

* **State:** `SO_*`/`IP_*`/`TCP_*` option families not yet harvested (P2); `WSAAsyncSelect` has no CE page (event-based `WSAEventSelect` is the documented model).
* **Resolution (Role A):** option-family page harvest; (Role C) `GetProcAddress(L"WSAAsyncSelect")` probe to prove absence.

## OQ-20 — `WSAPROTOCOL_INFO` / `WSAQUERYSET` member-level CE deltas

* **State:** pages harvested (verbatim layouts in YAML); detailed member diff pending.
* **Resolution:** as OQ-18.

## OQ-21 — Common-control structure closure (P2)

* **State:** `REBARBANDINFO`, `OPENFILENAME`, `CHOOSECOLOR`, `TBBUTTON`, `NMCUSTOMDRAW`-family pages live in the unharvested ~700 pages of the common-controls area.
* **Resolution (Role A):** extend the commctrl harvest to the full area (mechanical; `tools/harvest_area.py` ready).
