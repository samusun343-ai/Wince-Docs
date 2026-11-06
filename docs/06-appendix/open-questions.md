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

## OQ-11 — Repository distribution license

* **Question:** which open license should this documentation suite carry?
* **Recommendation (Role A):** CC-BY-4.0 for docs + MIT/CC0 for data and tools; decision belongs to the repository owner.

## OQ-12 — GWES function library bindings

* **State:** `CreateWindow`/`RegisterClass`/`DefWindowProc` pages document header but no link library; `GetMessage` documents `coredll.lib`.
* **Resolution (Role A/C):** P1 harvest of the full GWES area + runtime probing; expected resolution: coredll-bound.
