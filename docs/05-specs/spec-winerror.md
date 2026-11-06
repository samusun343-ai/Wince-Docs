# Specification — `winerror.h`

Status: final (complete enumeration) | Priority: P0 | Fact source: `data/mslearn-facts/ce60-system-errors.json` (+ `ce50-system-errors.json`)

## 1. Purpose and scope

The system error code constants for the CE 4/5/6 target family. This header's content is **fully enumerated** — the complete documented tables were extracted from the official documentation:

* **Windows Embedded CE 6.0**: `System Errors - Numerical Order` — `https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ee488398(v=winembedded.60)` — **571 codes** (values 0–6118), retrieved 2026-11-07.
* **Windows CE 5.0**: `System Errors - Numerical Order` — `https://learn.microsoft.com/en-us/previous-versions/windows/embedded/aa450919(v=msdn.10)` — **570 codes**, retrieved 2026-11-07.

Cross-version diff (mechanically computed, both tables extracted in full):

* Value/name assignments: **identical** for all 570 shared codes (no value differences).
* CE 6.0 adds exactly one code: `ERROR_DEVICE_REMOVED`.
* CE 5.0 has no code absent from CE 6.0.

⇒ A single `winerror.h` enum covers the CE 4/5/6 target family; `ERROR_DEVICE_REMOVED` is gated `_WIN32_WCE >= 0x0500`-era availability **only if** runtime verification shows absence on 4.x (its presence is documented in both CE 5.0 and 6.0 tables; see OQ-10 for the CE 4.x check).

## 2. Structure of the generated header (normative)

1. Constants are emitted as `#define ERROR_SUCCESS 0L`-style definitions (w32api-compatible), grouped by numeric range with the docset citation in a banner comment.
2. Every constant maps 1:1 to a record in the fact JSON (fields: `code`, `name`, `desc`). Descriptions are one-line factual strings from the documentation; the header itself emits **only** `name → value`, while the `.map` sidecar retains descriptions + source URL (R-DEF-3-style traceability).
3. Codes outside the documented table (undocumented ranges) MUST NOT be invented.

## 3. Sample (first 20 of 571 — see the data file for the complete list)

| Value | Constant |
| --- | --- |
| 0 | `ERROR_SUCCESS` |
| 1 | `ERROR_INVALID_FUNCTION` |
| 2 | `ERROR_FILE_NOT_FOUND` |
| 3 | `ERROR_PATH_NOT_FOUND` |
| 4 | `ERROR_TOO_MANY_OPEN_FILES` |
| 5 | `ERROR_ACCESS_DENIED` |
| 6 | `ERROR_INVALID_HANDLE` |
| 7 | `ERROR_ARENA_TRASHED` |
| 8 | `ERROR_NOT_ENOUGH_MEMORY` |
| 9 | `ERROR_INVALID_BLOCK` |
| 10 | `ERROR_BAD_ENVIRONMENT` |
| 11 | `ERROR_BAD_FORMAT` |
| 12 | `ERROR_INVALID_ACCESS` |
| 13 | `ERROR_INVALID_DATA` |
| 14 | `ERROR_OUTOFMEMORY` |
| 15 | `ERROR_INVALID_DRIVE` |
| 16 | `ERROR_CURRENT_DIRECTORY` |
| 17 | `ERROR_NOT_SAME_DEVICE` |
| 18 | `ERROR_NO_MORE_FILES` |
| 19 | `ERROR_WRITE_PROTECT` |

Highest documented value: **6118** (`ERROR_NO_BROWSER_SERVERS_FOUND`). Known high blocks include 4xxx (installer/static-init/backup) and 61xx (browser) ranges.

## 4. Related pages (documentation closure)

The `Error Values` area also contains (CE 6.0 index): Net Errors (alphabetical/numerical), RAS error values, NTE/CRYPT/CERTSRV/TRUST error codes, `Error Functions` (GetLastError/SetLastError → winbase spec), and `Formatting Specifications` — the non-"System Errors" tables are **P1/P2 tail** (Wininet/RAS/crypto headers), tracked in `data/mslearn-inventories/ce60/error-values.json`.

## 5. Implementation notes for Role B

1. Guard `_WINERROR_H`; depends only on `winnt.h` types (`DWORD`-valued defines).
2. Emit codes sorted numerically with range-group comments mirroring the documentation's ranges.
3. The header must NOT include desktop-only error codes absent from the CE tables (e.g. no Win32 codes ≥ 6119 unless documented for CE).

## 6. Verification hooks

L2: `_Static_assert(ERROR_SUCCESS == 0)`, `(_Static_assert(ERROR_NO_BROWSER_SERVERS_FOUND == 6118)`, spot asserts per range.
L3: documented-failure probes — e.g. `CreateFile(L"\\nonexistent\\file", ...)` must yield `GetLastError() == ERROR_FILE_NOT_FOUND (2)`; `SetLastError(1234)`/`GetLastError()` round-trip.
