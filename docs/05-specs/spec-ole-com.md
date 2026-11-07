# Specification — COM / DCOM / Automation / OLE / Storage (`ole32` family)

Status: final (P3 harvest batch) | Priority: P2 (full documented surface) | Fact sources: `data/facts/ole-com.yaml` (305 records), `data/facts/oleauto.yaml` (201)
Harvest basis: COM and DCOM Reference subareas, both docsets — COM Reference 341+345, Automation Reference 303+303, OLE Reference 150+150, Storage Reference 66+66 — 1,724 harvested pages.

## 1. Purpose and scope

The complete documented CE COM/DCOM application surface: core COM (`objbase.h`, `objidl.h`, `ocidl.h`, `oleidl.h`, `ole2.h`), the CE DCOM additions (`dccole.h`), access-control interfaces (`iaccess.h`), structured storage (`istorage` family), monikers, `IDataObject`/clipboard-adjacent OLE, and the full Automation/`IDispatch` set (`oleauto.h`, `oaidl.h`). CE 4.x ships COM-inproc only at minimum; DCOM (remote) is a separately installable SYSGEN on 5.0/6.0 — the header set is common, the remote-gated records note it.

506 combined records; `CLSCTX_*` enumeration values are **documented numerically in the CE docs** (e.g. `CLSCTX_INPROC_SERVER = 0x1`, `CLSCTX_REMOTE_SERVER = 0x10`) — Class A values, no cross-check needed for those.

## 2. Dependencies

`windef.h`, `winnt.h` (`HRESULT`, `GUID`/`IID`/`CLSID` typedefs — see `spec-winnt.md`), `wtypes.h` (VARTYPE family). `ole2.h` is the umbrella that pulls `objbase.h`/`oleauto.h` as on desktop.

## 3. Enumeration by family (record counts post-merge; full lists in the fact YAMLs)

| Family | Functions | Interfaces | Structures | Enums/types/constants | Notable CE facts |
| --- | --- | --- | --- | --- | --- |
| Core COM (`objbase.h`) | 99 | — | — | — | `CoInitializeEx` documented with `COINIT_MULTITHREADED` usage; `CoCreateInstance` pages bind **ole32.lib** |
| `objidl.h` | 51 (page-level) | 51 incl. `IBindCtx` (8 methods aggregated), `IEnumUnknown`, `IPersist*`, `IMoniker` family | — | — | pages are per-method (`IFace::Method`) — aggregated into 71 interface records overall |
| `ocidl.h` | 25 | property-frame interfaces | — | — | |
| `oleidl.h` / `ole2.h` | 18 / 17 | `IDropTarget` family | — | — | CE drag-drop subset |
| Storage (`istorage`) | 40 | `IStorage`, `IStream` | — | `STGM_*` flags | documented `STG_E_*` errors live in `winerror.h` (Class A values, `spec-winerror.md`) |
| CE DCOM (`dccole.h`) | 11 | — | — | — | **ce-only header**: CE DCOM extensions — R-HDR-18 keeps it standalone |
| `iaccess.h` | 6 | access-control interfaces | — | — | |
| Automation (`oleauto.h`) | 159 | 14 (`IEnumVARIANT`, `ITypeLib`, …) | 18 (`SAFEARRAY` family, `VARIANT`—via oaidl) | 7 enums (`CALLCONV`, `DESCKIND`, `FUNCFLAGS`, `FUNCKIND`, `INVOKEKIND`, `TYPEKIND`, `VARTYPE`) | **oleaut32.lib** on 171 records — the largest single-library binding in the P3 set |
| `oaidl.h` | 42 pages | IDispatch | `DISPPARAMS`, `EXCEPINFO` | `DISPID`/`invokekind` constants | |

Class composition: all `common` (desktop-shared names) except where CE pages mark later introductions; introduced distribution peaks at CE 2.0/3.0 (Automation 2.0, DCOM 3.0+).

## 4. A/W and export-form notes

COM/ Automation on CE is wide-string at the public boundary (`LPOLESTR`, `BSTR` = wide); no A-variants documented. `SysAllocString` family takes/returns wide `BSTR`. `StringFromGUID2` wide-only (the ANSI `StringFromGUIDA` has no CE page).

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0300` | DCOM surface (`dccole.h`, `CoCreateInstanceEx` remote contexts) |
| `_WIN32_WCE >= 0x0400` | later COM additions introduced ".NET 4.0 and later" (10 records) |
| per-record `introduced` | 2.0/2.1 bulk (Automation), 1.0-era base typedefs |

No CE5→CE6 library-binding changes recorded in this area (ole32.lib/oleaut32.lib stable across both docsets).

## 6. Implementation notes for Role B

1. **R-HDR-18**: desktop header split is kept: `objbase.h`, `objidl.h`, `ocidl.h`, `oleidl.h`, `ole2.h`, `oleauto.h`, `oaidl.h`, `wtypes.h`; `dccole.h` and `iaccess.h` are CE additions shipped as own headers. `comdef.h`/`_com_ptr_t` are compiler-support, out of OS-header scope.
2. Interface records carry method lists in `definition` (aggregated from per-method pages) — emit as C++-neutral vtable comments or IDL-annotated comments; the `.def` surface is functions only, never interface methods.
3. GUID factory macros (`CLSIDFromString`, `IIDFromString`) are functions (corrected classification); `IsEqualGUID`-family are macros — no `.def` entries.
4. `VARIANT`/`DECIMAL` layout must match `spec-winnt.md` `wtypes.h` records; static-assert `sizeof(VARIANT) == 16` on 32-bit.
5. `CLSCTX_*`, `COINIT_*`, `STGM_*`, `OLERENDER_*`: emit documented values; the remaining symbolics (`VT_*` array) come from the w32api lineage channel (verify-runtime status as recorded).

## 7. Closure statement

1,724 pages → 506 records (docset-merge + per-method aggregation; 9 overview notes retained). OLE/Storage/COM/Automation subareas fully covered; nothing excluded. The `iaccess.h` set is small but complete. TSPI/service-provider and OLE-Document (DocObject) surfaces are NOT part of the CE documentation set and remain out of scope.

## 8. Verification hooks

L2: `sizeof(SAFEARRAY)` header layout; `CLSCTX_*` numeric equality vs desktop docs; `VariantClear` export presence. L3: `CoCreateInstance` in-proc roundtrip; `SysAllocString`/`SysFreeString` pair; on a DCOM image, `CoCreateInstanceEx` remote with `CLSCTX_REMOTE_SERVER`.
