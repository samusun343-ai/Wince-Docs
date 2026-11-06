# Unicode / A-W Policy for the Windows CE Header Set

Status: Normative | Applies to: every header spec and every function record

## 1. The platform reality

Windows CE is a **Unicode-native** platform:

* CeGCC's toolchain documentation states it directly — preprocessor defaults include `UNICODE` and `_UNICODE` with the gloss *"Windows CE is a Unicode platform"* (source `cegcc`, docs/details.html).
* The official CE documentation's generic `TCHAR`-based signatures resolve to wide types in the CE environment; e.g. the documented `WinMain` entry point takes `LPWSTR lpCmdLine` (CE 5.0 & 6.0 pages, `data/mslearn-facts/`), and `CreateProcess` takes `LPCWSTR`/`LPWSTR` throughout (`ee488927`).
* The MSDN Magazine Pocket PC article (June 2001) records the same for CE 3.0-era devices.

## 2. The CE export-naming anomaly (critical difference from desktop Win32)

Desktop Win32 exports strict `A`/`W` pairs (`MessageBoxA`/`MessageBoxW`). Windows CE does **not** follow this uniformly:

1. Many APIs are exported **with the `W` suffix only** (wide-only, no ANSI counterpart).
2. Many APIs are exported **without any suffix while still being wide-only**. Engineering evidence — the CeGCC-lineage w32api defines a dedicated macro with the comment:
   > "Macro to deal with wide names — WinCE functions not receiving LPTSTR directly don't have W suffix, even though they are implicitly wide (expect wide strings in structures passed, etc.)" (`include/windef.h`, public-domain source `mingw-org-w32api`).
3. Documentation pages use the **generic name** (`CreateFile`, `MessageBox`) regardless of the exported symbol's suffix, so the suffix truth is per-function and must be captured per-function in the fact DB.

Consequence: for every function record, the fact schema carries `export:` with the actual documented/verified exported symbol form, and the header macro layer must map generic → actual per function, not by a blanket rule.

## 3. Header generation rules (normative)

* **R-AW-1.** The headers MUST define the generic (suffix-less) programmer-level name for every documented function, resolving to the wide-only reality. `TCHAR`-neutral code from desktop sources must compile against CE headers unchanged wherever the API exists on CE.
* **R-AW-2.** The macro layer MUST be per-function fact-driven:
  * function documented/exported as `FooW` ⇒ `#define Foo FooW` (e.g. the `CreateFile` family pattern where applicable);
  * function exported as `Foo` (suffix-less, implicitly wide) ⇒ no renaming macro; the prototype is declared once, wide-only (the `_WNAME` evidence);
  * function genuinely present in both forms on CE (rare; to be inventoried — OQ-2) ⇒ both declared, generic mapped to `W`.
* **R-AW-3.** ANSI (`A`) prototypes MUST NOT be invented for CE. If a CE module genuinely exports an `A` symbol (known examples exist in third-party compatibility layers, not the OS), it is recorded per-function with `status: verify-runtime`; the default header stance is **no ANSI surface**.
* **R-AW-4.** `TCHAR`, `LPTSTR`, `LPCTSTR` etc. MUST resolve to wide types (`WCHAR`, `LPWSTR`, `LPCWSTR`) — CE headers are compiled in an implicitly-Unicode environment; the specs' generic-type usage mirrors the official documentation.
* **R-AW-5.** CRT-facing string functions follow the CRT boundary rules (`include-tree.md` §5): the OS API surface (coredll) and the C runtime are separate concerns; the header set does not fake CRT behaviour.

## 4. Structure member types

Structures documented with `TCHAR szMember[n]` (e.g. `OSVERSIONINFO.szCSDVersion[128]`, CE 5.0/6.0 pages) are specified in the fact DB as `WCHAR` arrays, per R-AW-4, with the generic form kept as documentation alias.

## 5. Calling conventions (closely coupled to A/W layer)

* The documented entry point uses `WINAPI` (`int WINAPI WinMain(...)`, CE 5.0 & 6.0 pages) — the conventional macro set (`WINAPI`, `CALLBACK`, `APIENTRY`) is required surface.
* On **ARM/MIPS/SH** there is effectively a single calling convention, so the macro choice is cosmetic; on **x86 CEPC** the desktop-style distinction exists. The spec records the macro *definitions* as a per-architecture implementation detail with `verify-runtime` status (OQ-3), since the official CE documentation does not state the x86 convention per function.
* CeGCC lineage precedent: w32api keeps `WINAPI __stdcall` (public-domain evidence) — adopted as the default assumption, subject to runtime verification.

## 6. Version availability

Unicode-only-ness is constant across the collection range (CE 1.0 was already a Unicode platform per early documentation; `WaitForMultipleObjects` CE remarks record CE 1.x/2.x object-type gaps instead). A/W facts therefore do not carry separate version gates except where a function itself is version-gated.

## 7. Open items

* **OQ-2** — inventory of any genuine `A`-suffix exports in CE system modules (verification: runtime `GetProcAddress` probing on CE 4/5/6 images; none documented so far).
* **OQ-3** — x86 CEPC calling-convention confirmation (runtime probe: call an API with a mismatched convention candidate and observe stack behaviour, or link a test DLL that exports both conventions).
