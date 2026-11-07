# Specification — Remote API (`rapi.h`, `rapi2.h`, `rapitypes.h`)

Status: final (P3 harvest batch) | Priority: P2 | Fact source: `data/facts/rapi.yaml` (112 records)
Harvest basis: RAPI Reference 105 + RAPI2 Reference 102 (CE 6.0 docset only) — 207 harvested pages.

## 1. Purpose and scope

The **desktop-side** CE remote API: the `Ce*` function family that a Windows host application links against (`rapi.lib`) to manipulate an attached Windows CE device — file system, registry, database (CEDB remote mirror), system info, and the RAPI2 COM object model (`IRAPIDesktop`, `IRAPIEnumDevices`, `IRAPIDevice`, `IRAPISession`, `IRAPISink`, `IRAPIStream`).

Whole area is class **ce-only** by definition (the API exists only for CE connectivity — there is no desktop counterpart of these semantics even though the code runs on the desktop). Documented headers: `rapi.h` (83 records), `rapitypes.h` (19), `rapitypes2.h` (6), `rapi2.h` (5), `dccole2.h` (1), `rrapi.h` (1).

## 2. Dependencies

Runs on the host: `windows.h` (desktop Win32), `objbase.h` for RAPI2 COM. In the project include tree RAPI is a **host-side adjunct** — see R-HDR-22.

## 3. Enumeration (counts post-merge)

| Kind | Count | Examples |
| --- | --- | --- |
| functions | 82 | `CeRapiInit`/`CeRapiUninit`, `CeCreateFile`, `CeCopyFile`, `CeFindFirstFile`, `CeRegOpenKeyEx`, `CeCreateDatabase`, `CeGetSystemInfo`, `CeGetStoreInformation`… |
| structures | 17 | RAPI equivalents of CE types (`CE_FIND_DATA`, `RAPIVERSION`?) — see `rapitypes.h` records |
| interfaces | 7 | the RAPI2 COM set, methods aggregated |
| enums/types | 6 | `RAPI_GETDEVICE_STATE`? etc. |

Introduced: 3.0 for the RAPI1 bulk (103 records), **6.0 for the RAPI2 object model (11)**. Library: `rapi.lib` on the 3 records that state one; RAPI2 interfaces bind `ole32.lib` usage on the host.

## 4. A/W and export-form notes

RAPI1 `Ce*` functions are wide (`CeCreateFile` takes `LPCWSTR`); no A-variants. RAPI2 is COM (wide). `rapi.h` on the desktop w32api lineage defines the same family — it is one of the lineage headers (cross-check channel available; 5 records skipped as already-known names in the pre-P3 DB are lineage-visible).

## 5. Version gates

| Gate | Items |
| --- | --- |
| host-side, no `_WIN32_WCE` gate | whole header set — RAPI compiles against desktop Win32 |
| CE 6.0 device-side counterpart | RAPI2 requires a CE 6.0-class device (11 records) |

## 6. Implementation notes for Role B

1. **R-HDR-22**: `rapi.h`, `rapi2.h`, `rapitypes.h`, `rapitypes2.h` ship in a `rapi/` subdirectory of the include tree (host-side adjunct set, mirrored from the desktop side of the SDK model); they are NOT included by `windows.h` and are not gated on `_WIN32_WCE`. `dccole2.h`/`rrapi.h` (1 record each) ride along.
2. The `Ce*` names duplicate CE-side database/file semantics — but RAPI runs on the host: no `.def` collision with the device `coredll` set (different import library: `rapi.lib`).
3. Structure records from `rapitypes.h` mirror device types — sizes are 32-bit host sizes; static-assert `CE_FIND_DATA` layout.
4. RAPI2 interfaces: vtable-comment emission like the rest of the COM set.

## 7. Closure statement

207 pages → 112 records (method-page aggregation for RAPI2; docset merge N/A — RAPI exists only in the CE 6.0 tree; the CE 5.0 docset carries no RAPI pages, which matches the P2 finding pattern for other 6.0-era trees). Nothing excluded. `IRAPISink`-family advise-sink pages are part of the aggregated interface records.

## 8. Verification hooks

Host-side L3: `CeRapiInit`/`CeRapiUninit` roundtrip against an emulated device; RAPI2 `IRAPIDesktop::EnumDevices` on a CE 6.0 class device. L2: header self-consistency (no `_WIN32_WCE` dependency).
