# Version Gating and Feature Macros

Status: Normative | Governs `_WIN32_WCE` and related preprocessor gating

## 1. The version macros

| Macro | Meaning | Status |
| --- | --- | --- |
| `_WIN32_WCE` | Compile-time CE version selector — **the** gating macro for the CE family | encoding specified in §2 |
| `UNDER_CE` | Defined when targeting Windows CE (toolchain-level) | documented by CeGCC predefinitions (`cegcc` audit) |
| `_WIN32`, `WIN32` | 32-bit Windows environment | CeGCC `-mwin32` behaviour; desktop-common semantics |
| `WINVER`, `_WIN32_WINNT` | Desktop version gates — **NOT meaningful on CE**; headers MUST NOT require them (CeGCC explicitly treats `_WIN32_IE` requirements as header bugs to fix; same stance adopted) | policy §4 |
| `UNICODE`, `_UNICODE` | Predefined by CE-targeting compilers ("Windows CE is a Unicode platform") | `unicode-aw-policy.md` |
| `__COREDLL__` | Signals coredll-based runtime (CeGCC/mingw32ce lineage) | informational |
| Processor macros: `ARM`/`_M_ARM`, MIPS (`_M_MIPS…`), SH (`_M_SH…`), `_M_IX86`/`_X86_` | target arch | target-matrix §2 |

## 2. `_WIN32_WCE` value encoding (normative)

The macro encodes `major.minor` as a 16-bit value: **`(major << 8) | bcd(minor)`** — the minor version as two BCD digits:

| CE version | `_WIN32_WCE` |
| --- | --- |
| 3.0 | `0x0300` |
| 4.0 | `0x0400` |
| 4.1 | `0x0410` |
| 4.2 | `0x0420` |
| 5.0 | `0x0500` |
| 6.0 | `0x0600` |

Evidence: CeGCC documentation — *"a device that runs a version of CE that identifies itself as 4.20.0, would match with a value of 0x0420 or lower"* (`cegcc` audit, docs/details.html) — and the w32api lineage gating usage (`_WIN32_WCE >= 0x0400`, `>= 0x0500`, … observed in `mingw-org-w32api` headers, including its `#ifndef _WIN32_WCE / #define _WIN32_WCE 0x0300` default for CE builds). The public-domain default in that lineage is `0x0300`.

Status: encoding = `verified` (two independent sources agree); **an official Microsoft statement of the encoding is not yet located** (OQ-1). Role C runtime-verification: assert `OSVERSIONINFO.dwMajorVersion/dwMinorVersion` consistency with the toolchain's predefined `_WIN32_WCE` on CE 4/5/6 images.

## 3. Gating rules (normative)

* **R-VG-1.** Feature availability gates use `_WIN32_WCE` exclusively for CE-version differences:
  `#if (_WIN32_WCE >= 0x0500)` …
* **R-VG-2.** The mapping from a fact's `introduced`/`removed` (documented "OS Versions" wording) to a gate is mechanical and is generated from the fact DB (e.g. "Windows CE 2.10 and later" ⇒ `_WIN32_WCE >= 0x0210`; "Windows CE .NET 4.0 and later" ⇒ `>= 0x0400`).
* **R-VG-3.** Items present in *all* collection-range versions (e.g. `CreateProcess`, "Windows CE 1.0 and later") carry no gate.
* **R-VG-4.** Architecture gates use the processor macros; combined gates compose with `&&`.
* **R-VG-5.** Headers MUST compile with `_WIN32_WCE` set to any of `0x0400`…`0x0600`; undefined `_WIN32_WCE` in a CE-targeting build is an error the umbrella headers SHOULD diagnose (not silently default, unlike the CeGCC lineage's `0x0300` fallback — this project's targets start at 4.0).

## 4. Desktop-gate hygiene

* `_WIN32_WINNT`, `_WIN32_IE`, `WINVER` MUST NOT be *required* to be defined by user code on CE (per the CeGCC-mingw32ce position: dependencies on `_WIN32_IE` in CE headers are considered bugs). Where desktop-common facts carry such gates in their w32api expression, the CE spec drops the gate in favour of `_WIN32_WCE`/`introduced` fields.
* `WIN32_LEAN_AND_MEAN`-style include-thinning MAY be honoured for source compatibility.

## 5. PE subsystem version (conformance cross-link)

Executable targeting data: the PE optional header's subsystem version carries the CE version — CeGCC documents the linker invocation for CE 4.20 as `-Wl,--major-subsystem-version,4 -Wl,--minor-subsystem-version,20` (`cegcc` audit). Conformance tests verify the toolchain sets this consistently with the gated `_WIN32_WCE` (see `conformance-testing.md`).
