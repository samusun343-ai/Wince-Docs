# Specification — `windef.h`

Status: final (Phase 1) | Priority: P0 | Fact source: `data/facts/windef.yaml`
Sources: `mingw-org-w32api` (public-domain structure baseline), `cegcc` (CE integration evidence), `mslearn-ce60`/`mslearn-ce50` (documented signatures/requirements)

## 1. Purpose and scope

`windef.h` is the foundation header: basic scalar types, pointer-style aliases, calling-convention macros, small helper macros, and the `RECT`/`POINT`/`SIZE` geometry types. It declares no OS functions and depends only on `winnt.h` for `HANDLE`-family types (or forward-declares them — see §6).

## 2. Dependencies

Included first by every header. Includes: `winnt.h` (in the w32api organization `windef.h` is included *by* `winnt.h`; the implementation MUST keep a single, acyclic order — see `include-tree.md` §3).

## 3. Enumeration (complete)

### 3.1 Environment / identity macros

| Item | Definition | Class | CE versions | Sources | Status |
| --- | --- | --- | --- | --- | --- |
| `WIN32`, `_WIN32` | defined (no value) | common | all | mingw-org-w32api; cegcc | verified |
| `UNDER_CE` | defined (no value) | ce-only | all | cegcc | verified |
| `_WIN32_WCE` | **not defined by the header** (toolchain/pre-include responsibility); headers gate on it (see `versioning-gating.md`) | ce-only | all | cegcc; mingw-org-w32api | verified |
| `FAR`, `far`, `NEAR`, `near` | empty | common | all | mingw-org-w32api | verified |
| `CONST` | `const` | common | all | mingw-org-w32api | verified |
| `MAX_PATH` | `260` | common | all | mingw-org-w32api; mslearn-ce60 (CreateProcess remarks: "If the length of the SystemPath value exceeds 260 characters…") | verified |
| `NULL` | `((void*)0)` / `0` in C++ | common | all | mingw-org-w32api | verified |
| `FALSE` / `TRUE` | `0` / `1` | common | all | mingw-org-w32api | verified |
| `IN` / `OUT` / `OPTIONAL` | empty SAL-legacy macros | common | all | mingw-org-w32api | verified |

### 3.2 Calling conventions (see `unicode-aw-policy.md` §5)

| Item | Definition (GNUC path) | Class | Notes | Sources | Status |
| --- | --- | --- | --- | --- | --- |
| `__stdcall` / `_stdcall` / `STDCALL` | compiler attribute | common | | mingw-org-w32api | verified |
| `__cdecl` / `_cdecl` / `CDECL` | compiler attribute | common | | mingw-org-w32api | verified |
| `__fastcall` / `FASTCALL` | compiler attribute | common | | mingw-org-w32api | verified |
| `pascal` / `_pascal` / `__pascal` / `PASCAL` | → `__stdcall` | common | | mingw-org-w32api | verified |
| `WINAPI` | `__stdcall` | common | cosmetic on ARM/MIPS/SH; x86 CEPC convention is OQ-3 | mingw-org-w32api; mslearn-ce60 (WinMain) | verify-runtime (x86) |
| `WINAPIV` | `__cdecl` | common | | mingw-org-w32api | verified |
| `APIENTRY` | `__stdcall` | common | | mingw-org-w32api | verified |
| `CALLBACK` | `__stdcall` | common | | mingw-org-w32api | verified |
| `APIPRIVATE` | `__stdcall` | common | | mingw-org-w32api | verified |
| `DECLARE_STDCALL_P(type)` | `__stdcall type` | common | | mingw-org-w32api | verified |
| `DECLSPEC_IMPORT` / `DECLSPEC_EXPORT` / `DECLSPEC_NORETURN` | `__declspec(...)` mapping | common | | mingw-org-w32api | verified |
| `PACKED` | `__attribute__((packed))` | common | see packing note §6 | mingw-org-w32api | verified |
| `_ANONYMOUS_UNION` / `_ANONYMOUS_STRUCT` / `_UNION_NAME(x)` | compiler-extension mappings | common | used by `SYSTEM_INFO` union | mingw-org-w32api; mslearn-ce60 (SYSTEM_INFO layout) | verified |
| `DUMMYUNIONNAME`…`DUMMYUNIONNAME8` | `u`, `u2`…`u8` | common | | mingw-org-w32api | verified |

### 3.3 Basic types

| Item | Definition | Class | Sources | Status |
| --- | --- | --- | --- | --- |
| `DWORD` | `typedef unsigned long DWORD;` | common | mingw-org-w32api | verified |
| `BOOL` / `WINBOOL` | `typedef int WINBOOL; typedef WINBOOL BOOL;` | common | mingw-org-w32api | verified |
| `BYTE` | `typedef unsigned char BYTE;` | common | mingw-org-w32api | verified |
| `WORD` | `typedef unsigned short WORD;` | common | mingw-org-w32api | verified |
| `FLOAT` | `typedef float FLOAT;` | common | mingw-org-w32api | verified |
| `INT` | `typedef int INT;` | common | mingw-org-w32api | verified |
| `UINT` | `typedef unsigned int UINT;` | common | mingw-org-w32api | verified |
| `WPARAM` | `typedef UINT_PTR WPARAM;` | common | mingw-org-w32api (`UINT_PTR` from winnt) | verified |
| `LPARAM` | `typedef LONG_PTR LPARAM;` | common | mingw-org-w32api | verified |
| `LRESULT` | `typedef LONG_PTR LRESULT;` | common | mingw-org-w32api | verified |
| `HRESULT` | `typedef LONG HRESULT;` | common | mingw-org-w32api | verified |
| `ATOM` | `typedef WORD ATOM;` | common | mingw-org-w32api | verified |
| `COLORREF` | `typedef DWORD COLORREF;` | common | mingw-org-w32api | verified |
| `HFILE` | `typedef int HFILE;` | common | mingw-org-w32api | verified |
| Pointer aliases `PBOOL`/`LPBOOL`, `PBYTE`/`LPBYTE`, `PINT`/`LPINT`, `PWORD`/`LPWORD`, `LPLONG`, `PDWORD`/`LPDWORD`, `PFLOAT`, `PUINT`/`LPUINT`, `PCVOID`/`LPCVOID` | corresponding `T *` | common | mingw-org-w32api | verified |
| `FARPROC` / `NEARPROC` / `PROC` | `typedef int (WINAPI *FARPROC)();` etc. | common | mingw-org-w32api | verified |
| Handle-family aliases `HHOOK`, `HGLOBAL`, `HLOCAL`, `GLOBALHANDLE`, `LOCALHANDLE`, `HGDIOBJ` (`void *`), `HMODULE` (→ `HINSTANCE`), `HCURSOR` (→ `HICON`), `PHKEY` | base handles from `winnt.h` | common | mingw-org-w32api | verified |

### 3.4 Helper macros

| Item | Definition | Class | Sources | Status |
| --- | --- | --- | --- | --- |
| `MAKEWORD(a,b)` | `((WORD)(((BYTE)(a))\|(((WORD)((BYTE)(b)))<<8)))` | common | mingw-org-w32api | verified |
| `MAKELONG(a,b)` | `((LONG)(((WORD)(a))\|(((DWORD)((WORD)(b)))<<16)))` | common | mingw-org-w32api | verified |
| `LOWORD(l)` | `((WORD)((DWORD)(l)))` | common | mingw-org-w32api | verified |
| `HIWORD(l)` | `((WORD)(((DWORD)(l)>>16)&0xFFFF))` | common | mingw-org-w32api | verified |
| `LOBYTE(w)` | `((BYTE)(w))` | common | mingw-org-w32api | verified |
| `HIBYTE(w)` | `((BYTE)(((WORD)(w)>>8)&0xFF))` | common | mingw-org-w32api | verified |
| `min(a,b)` / `max(a,b)` | classic min/max (guarded by `NOMINMAX` at umbrella level) | common | mingw-org-w32api | verified |
| `UNREFERENCED_PARAMETER(P)` / `UNREFERENCED_LOCAL_VARIABLE(L)` / `DBG_UNREFERENCED_PARAMETER(P)` / `DBG_UNREFERENCED_LOCAL_VARIABLE(L)` | no-op reference keepers | common | mingw-org-w32api | verified |
| `_export` / `__export` | empty | common | mingw-org-w32api | verified |

### 3.5 Geometry types

| Item | Definition | Class | Sources | Status |
| --- | --- | --- | --- | --- |
| `RECT` / `PRECT` / `LPRECT` / `LPCRECT` | `typedef struct tagRECT { LONG left, top, right, bottom; } RECT;` | common | mingw-org-w32api | verified |
| `RECTL` / `PRECTL` / `LPRECTL` | LONG-field variant | common | mingw-org-w32api | verified |
| `POINT` / `PPOINT` / `LPPOINT`, `POINTL` | consumed by GWES/GDI pages (e.g. `MonitorFromPoint`, CE6 docs) | common | mingw-org-w32api; mslearn-ce60 | verified |
| `SIZE` / `PSIZE` / `LPSIZE`, `SIZEL` | `typedef struct tagSIZE { LONG cx, cy; } SIZE;` | common | mingw-org-w32api | verified |
| `MAKEINTATOM(i)` | `((LPTSTR)((ULONG_PTR)((WORD)(i))))` | common | mingw-org-w32api | verify-runtime (ULONG_PTR from winnt) |

### 3.6 CE integration macros (from the CeGCC lineage — adopted as facts)

| Item | Definition | Class | Notes | Sources | Status |
| --- | --- | --- | --- | --- | --- |
| `_WNAME(name)` | `name` under `_WIN32_WCE`, `name##W` otherwise | ce-only | encodes the "implicitly wide, no suffix" export rule (`unicode-aw-policy.md` §2); implementation MAY keep this as internal machinery | mingw-org-w32api | verified |

## 4. A/W notes

`windef.h` is type-level; no A/W surface. The `TCHAR`-family (`LPTSTR` etc.) resolution rules live in `winnt.h`/umbrella per `unicode-aw-policy.md` R-AW-4.

## 5. Version gates

None — every item is present in all CE versions (types/macros are compile-time).

## 6. Implementation notes for Role B

1. Include guard `#ifndef _WINDEF_H`. Do NOT default `_WIN32_WCE` inside the header (unlike the CeGCC lineage's `0x0300` fallback — see `versioning-gating.md` R-VG-5); emit a diagnostic if `_WIN32_WCE` is undefined in a CE build.
2. `DWORD` stays `unsigned long` (32-bit on our targets; there is no WinCE LP64 — charter C-1).
3. Default packing: no `#pragma pack` in this header; packing-sensitive structures elsewhere record their own (OQ-7).
4. Generation source: `data/facts/windef.yaml` — one fact id per row above; assertion tags use those ids.

## 7. Closure statement

Documentation areas mapped to this header: none directly (the official docs reference `windows.h`/`winbase.h`/`winuser.h` per function; `windef.h` content is cross-cutting infrastructure). Baseline enumeration is the audited public-domain w32api `windef.h` (361 lines, 658-file tree, `mingw-org-w32api`) with CE deltas from the CeGCC lineage. Excluded: Win64-only branches (`_WIN64` paths), GCC-nonx86 compatibility cruft without CE relevance.

## 8. Verification hooks

L2 assertions: `MAX_PATH == 260`, `sizeof(DWORD) == 4`, `sizeof(WPARAM) == sizeof(UINT)`, `sizeof(LPARAM) == sizeof(LONG)` (32-bit only, per C-1). L3: none required (no runtime surface).
