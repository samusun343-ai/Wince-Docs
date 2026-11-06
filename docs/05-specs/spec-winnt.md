# Specification — `winnt.h` (core subset)

Status: final (Phase 1 core subset) | Priority: P0 | Fact source: `data/facts/winnt-core.yaml`
Full `winnt.h` expansion (LGUIDs, security, exceptions, power, locale tables) is P1; this spec enumerates the **core subset** required by the P0 headers and the conformance harness.

## 1. Purpose and scope

Fixed-width and pointer-precision types, RTL structures, the platform-identity constants, `FILETIME`, `OSVERSIONINFO`, and the pointer-polymorphism types required by the P0 API surface. Excludes (P1): `LANG*` tables, `SID`/ACL definitions beyond stubs, exception debugging records, `LUID`/privileges.

## 2. Dependencies

Includes `windef.h`. Included by everything else.

## 3. Enumeration (core subset — complete for this phase)

### 3.1 Character and generic-text types (per `unicode-aw-policy.md` R-AW-4)

| Item | Definition | Class | Sources | Status |
| --- | --- | --- | --- | --- |
| `CHAR` / `UCHAR` | `char` / `unsigned char` | common | mingw-org-w32api | verified |
| `SHORT` / `USHORT` | `short` / `unsigned short` | common | mingw-org-w32api | verified |
| `LONG` / `ULONG` | `long` / `unsigned long` | common | mingw-org-w32api | verified |
| `WCHAR` | `unsigned short` (2 bytes, Unicode UTF-16 code unit) | common | mingw-org-w32api | verified |
| `TCHAR` | **→ `WCHAR` on CE** | ce-modified | mslearn-ce60 (OSVERSIONINFO documented with `TCHAR szCSDVersion[128]` in a Unicode platform); cegcc | verified |
| `LPSTR`/`LPCSTR`/`PSTR`… | `CHAR *` const variants (present for type completeness) | common | mingw-org-w32api | verified |
| `LPWSTR`/`LPCWSTR`/`PWSTR`… | `WCHAR *` const variants | common | mingw-org-w32api | verified |
| `LPTSTR`/`LPCTSTR`/`PTSTR`… | **→ `LPWSTR`/`LPCWSTR` family on CE** | ce-modified | per R-AW-4 | verified |
| `LPVOID`/`PVOID`/`LPCVOID`/`PCVOID` | `void *` family | common | mingw-org-w32api | verified |

### 3.2 Pointer-precision types (32-bit ONLY — charter C-1)

| Item | Definition | Class | Notes | Sources | Status |
| --- | --- | --- | --- | --- | --- |
| `ULONG_PTR`, `UINT_PTR`, `LONG_PTR`, `INT_PTR` | unsigned/signed integral, pointer-sized (**32-bit on all CE targets**) | ce-modified | on desktop these became 64-bit under LLP64; on CE they remain 32-bit — the Win64 polymorphism is excluded | mingw-org-w32api; charter C-1 | verified |
| `DWORD_PTR` | `ULONG_PTR` | common | | mingw-org-w32api | verified |
| `SIZE_T` / `SSIZE_T` | `ULONG_PTR`/`LONG_PTR` | common | | mingw-org-w32api | verified |
| `ULONGONGLONG`? — no: `ULONGLONG`, `LONGLONG` | 64-bit signed/unsigned | common | supported by compilers on CE 4+ | mingw-org-w32api | verified |
| `LARGE_INTEGER` / `ULARGE_INTEGER` | anonymous-union 64-bit types (QuadPart / LowPart / HighPart) | common | consumed by documented CE APIs (file offsets, times) | mingw-org-w32api | verified |

### 3.3 Handle types

| Item | Definition | Class | Sources | Status |
| --- | --- | --- | --- | --- |
| `HANDLE` | `typedef void *HANDLE;` | common | mingw-org-w32api | verified |
| `PHANDLE`/`LPHANDLE` | `HANDLE *` | common | mingw-org-w32api | verified |
| `HINSTANCE`, `HWND`, `HDC`, `HMENU`, `HICON`, `HBITMAP`, `HBRUSH`, `HFONT`, `HPEN`, `HRGN`, `HKEY`, `HCOLORSPACE`, `HRSRC`… | `DECLARE_HANDLE`-style void-pointer handles (full list in the YAML) | common | mingw-org-w32api; consumption evidenced by mslearn-ce60 pages (MessageBox `HWND`, CreateWindow returns `HWND`, etc.) | verified |
| `INVALID_HANDLE_VALUE` | `((HANDLE)(LONG_PTR)-1)` — used by documented CE CreateFile failure semantics (see `spec-winbase-core.md`) | common | mingw-org-w32api; mslearn-ce60 | verify-runtime |

### 3.4 RTL structures

| Item | Definition | Class | Sources | Status |
| --- | --- | --- | --- | --- |
| `LIST_ENTRY` | `{ LIST_ENTRY *Flink, *Blink; }` + `LIST_HEAD` | common | mingw-org-w32api | verified |
| `SINGLE_LIST_ENTRY` | `{ struct _SINGLE_LIST_ENTRY *Next; }` | common | mingw-org-w32api | verified |
| `CRITICAL_SECTION` | RTL critical section (opaque debug-info-bearing layout; desktop-compatible members `DebugInfo` etc. — **CE behaviour**: EnterCriticalSection/InitializeCriticalSection documented, CE5+ pages) | ce-modified (layout verify) | mingw-org-w32api; mslearn-ce60 (InitializeCriticalSection page, winbase.h/coredll.lib) | verify-runtime |
| `FILETIME` | `{ DWORD dwLowDateTime; DWORD dwHighDateTime; }` | common | mslearn-ce60 (FILETIME page `ee488581`, System Management/Time structures); mingw-org-w32api | verified |

### 3.5 Platform identity

| Item | Definition | Class | CE versions | Sources | Status |
| --- | --- | --- | --- | --- | --- |
| `OSVERSIONINFO` | `typedef struct _OSVERSIONINFO { DWORD dwOSVersionInfoSize; DWORD dwMajorVersion; DWORD dwMinorVersion; DWORD dwBuildNumber; DWORD dwPlatformId; TCHAR szCSDVersion[128]; } OSVERSIONINFO;` (`szCSDVersion` is `WCHAR[128]` — R-AW-4) | ce-modified (TCHAR→WCHAR; size 544 bytes on CE) | 1.0+ | **mslearn-ce60** (`ee488619`, verbatim documented layout); **mslearn-ce50** (`ms886768`, identical) | verified |
| `VER_PLATFORM_WIN32_CE` | `3` | ce-only (constant value) | 1.0+ | msdn-mag-archive (June 2001: "the value is 3"); mingw-org-w32api | verified (two channels) |
| `VER_PLATFORM_WIN32s` / `VER_PLATFORM_WIN32_WINDOWS` / `VER_PLATFORM_WIN32_NT` | `0` / `1` / `2` | common (desktop values, kept for portable code) | n/a on CE | mingw-org-w32api; mslearn-win32 | verified |
| `MAXIMUM_WAIT_OBJECTS` | `64` | common-value; CE docs reference the constant without stating its value | n/a | mingw-org-w32api (`winbase.h` there; placed in winnt core here); mslearn-ce60 (WaitForMultipleObjects: "The maximum number of object handles is MAXIMUM_WAIT_OBJECTS") | **verify-runtime** (OQ-8) |
| `VER_MAJORVERSION`/`VER_MINORVERSION`/`VER_BUILDNUMBER`/`VER_PLATFORMID` (VerifyVersion info masks) | `0x0000001`…? | common | P1 tail | mingw-org-w32api | open (values P1) |

### 3.6 Security stubs (minimal)

| Item | Definition | Class | Notes | Sources | Status |
| --- | --- | --- | --- | --- | --- |
| `SECURITY_ATTRIBUTES` | `{ DWORD nLength; LPVOID lpSecurityDescriptor; BOOL bInheritHandle; }` | ce-modified | CE documents the parameter as "Not supported; set to NULL" (CreateProcess CE 6.0 page) — type must exist for signature compatibility | mingw-org-w32api; mslearn-ce60 (CreateProcess) | verified (type), behaviour documented as ignored |
| `PSECURITY_ATTRIBUTES`/`LPSECURITY_ATTRIBUTES` | pointer aliases | common | | mingw-org-w32api | verified |

## 4. A/W notes

`OSVERSIONINFO` is the worked example: documented with `TCHAR`, realized as `WCHAR` (wide-only). The desktop's `OSVERSIONINFOA` does **not** exist on CE (R-AW-3).

## 5. Version gates

`LONGLONG`/`ULONGLONG` availability is compiler-driven (documented device compilers support them on CE 4+); no OS gate. All other items: no gates.

## 6. Implementation notes for Role B

1. `#include <windef.h>` first; guard `_WINNT_H`.
2. `DECLARE_HANDLE(name)` macro generates `struct name##__ *name`-style opaque handles — keep the w32api-compatible form so portable sources type-check.
3. Do NOT emit any `#ifdef _WIN64` branch (charter C-1).
4. `OSVERSIONINFO` MUST be exactly 544 bytes (compile-time assertion hook).

## 7. Closure statement

Mapped documentation areas: Core OS › System Management Structures (OSVERSIONINFO, SYSTEM_INFO→winbase spec, FILETIME); the handle/type surface is cross-cutting (baseline: `mingw-org-w32api` `winnt.h`, 4,058 lines — full closure of that file is the P1 expansion task). Explicitly excluded from this phase: LANGID tables, SIDs/ACLs beyond `SECURITY_ATTRIBUTES`, exception records (`EXCEPTION_RECORD` — P1, needed by `spec-winbase-core` exception functions tail), `LUID`/privilege constants.

## 8. Verification hooks

L2: `_Static_assert(VER_PLATFORM_WIN32_CE == 3)`, `sizeof(OSVERSIONINFO) == 544`, `sizeof(WCHAR) == 2`, `sizeof(LONG_PTR) == 4`, `sizeof(LARGE_INTEGER) == 8`.
L3: on-device `GetVersionEx` probe fills `OSVERSIONINFO` with `dwPlatformId == 3` and `dwMajorVersion/dwMinorVersion` matching the image (resolves OQ-1 empirically; also validates the 544-byte size).
