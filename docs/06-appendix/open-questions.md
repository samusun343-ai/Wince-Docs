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

## OQ-21a — Common-control structure closure — RESOLVED (P2 session)

* **State (resolved):** the remaining ~700 common-control pages (1,524 page harvests incl. both docsets) are now in `data/facts/commctrl-controls.yaml` (760 records); structure pages (`REBARBANDINFO`, `TBBUTTON`, `NMCUSTOMDRAW` family, …) carry verbatim layouts. Member-level diff vs desktop continues under OQ-18's method.

## OQ-22 — ToolHelp predecessor spellings (CE 1.x–2.x)

* **State:** the docs document `CreateToolhelp32Snapshot` (2.0+); early-era spellings (`Toolhelp32CreateSnapshot`) are historical.
* **Resolution (Role A):** only if CE 1/2 support is ever targeted (OQ-9); headers document the modern names only.

## OQ-23 — `MSGQUEUE_*` flag values

* **State:** `MSGQUEUE_ALLOW_BROWSE`, `MSGQUEUE_MSGSIZE_*`, `MSGQUEUE_FIFO`, `MSGQUEUE_PRIORITY_NORMAL` etc. are CE-documented names without numeric values; two carry w32api-lineage values (`verify-runtime`).
* **Resolution (Role C):** behaviour probe — create queues with candidate flag bits and observe semantics; record before use.

## OQ-24 — `NOTIFICATION_EVENT_*` values

* **State:** event-type names documented on the `CeRunAppAtEvent` page; values lineage-only.
* **Resolution (Role C):** behaviour probe with candidate values on CE 5/6 (event ids are stable GWES constants).

## OQ-25 — `NMN_*` new-menu message values

* **State:** CE 6.0 newmenu.h set (`NMN_GETAPPREGKEY`, `NMN_INVOKECOMMAND`, …) documented without values; w32api lineage predates them.
* **Resolution (Role A):** locate a permissively-licensed Windows Mobile-era article; else Role C behaviour probe on a CE 6.0 standard-shell image.

## OQ-26 — `IOCTL_CONSOLE_*` numeric values

* **State:** the nine CE 6.0 console ioctls (`console.h`) are documented by name only.
* **Resolution (Role C):** `DeviceIoControl` sweep on a CE 6.0 console image with CTL_CODE candidates derived from the documented console device type; record before defining.

## OQ-27 — Undocumented region/alpha exports in GWES

* **State:** the GWES internal reference documents `Gdi::CombineRgn_I`, `Gdi::AlphaBlend_I`, `Gdi::CreateRectRgn_I` — internal implementations with no public API page (public GDI pages omit regions entirely on CE).
* **Resolution (Role C):** `GetProcAddress(L"CombineRgn")`-class probes on CE 5/6 images. Even if exported, headers stay documentation-driven (absent a Class A page) — findings feed a documented-exports addendum, not the base set.

## OQ-28 — `WM_IM_INFO` value

* **State:** CE-only IME message documented by name (winuser.h page) with no value in any approved source.
* **Resolution (Role A):** permissively-licensed IME-era article; else the name ships in a commented block only (never an invented value).

## OQ-29 — TAPI constant-family numeric values

* **State:** the 64 documented TAPI constant families (`LINEADDRCAPFLAGS`, `LINEBEARERMODE`, `LINECALLFEATURE`, `PHONEBUTTONMODE`, …, `tapi.yaml`) are name-complete but value-open: `tapi.h` is not in the audited w32api lineage, and mingw-w64's `tapi.h` reuse is deferred pending its per-file license scan (`docs/02-sources/audits/mingw-w64.md` §4.2).
* **Resolution:** Role A: complete the mingw-w64 per-file audit for `tapi.h` specifically (public-domain marking check) — if clean, add as Class B channel; else Role C on-device probing with desktop-known candidates (TAPI 2.x values are desktop-stable).

## OQ-30 — Bluetooth constant values (`BTH_*`, `OBEX_*`)

* **State:** the CE Bluetooth/OBEX constants (24 `BTH_*` records, OBEX enum) are documented by name only; no audited lineage header covers them (`ws2bth.h` is not in the w32api lineage).
* **Resolution:** Role C probe sweep on a BT-equipped CE 5/6 image; values recorded to the fact DB before any header emission.

## OQ-31 — CEDB vs EDB same-name layout divergence

* **State:** the Database Reference documents structurally different APIs under equal names (`CEDBASEINFOEX`, `CeChangeDatabaseLCID`, … — variant-suffixed records `_CEDB`/`_EDB` in `database.yaml`).
* **Resolution:** Role C `sizeof`/field-probe battery on 4.x (CEDB) vs 5.0+ (EDB) images; the two declarations stay separately gated and are never merged.

## OQ-32 — GPS Intermediate Driver constants (`GPS_*`)

* **State:** `gpsapi.h`/`gpsdev.h` constants and enums documented CE 6.0 only, values not stated.
* **Resolution:** Role C probe on a GPSID image; desktop `gpsapi.h` (Windows 7-era) is a different lineage — do not cross-copy.

## OQ-33 — CE-only waveform gain-control message values

* **State:** `MM_WOM_ATTENUATED`, `MM_WOM_FORCESPEAKER`, `MM_WOM_SETSECONDARYGAINCLASS`, `MM_WOM_SETSECONDARYGAINLIMIT` are CE-only documented messages with no numeric value in any approved source.
* **Resolution:** Role C message-id sweep on CE 5/6 audio images (candidates derived from the documented `MM_WOM_*` neighbourhood); never invented in headers.
