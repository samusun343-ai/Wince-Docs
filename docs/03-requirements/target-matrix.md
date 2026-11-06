# Target Environment Matrix

Status: Normative (requirements) | Sources: see per-row citations

## 1. Operating-system targets

| Target | Identity (`GetVersionEx`) | Notes |
| --- | --- | --- |
| Windows CE 4.0 / 4.1 / 4.2 ("Windows CE .NET") | `dwPlatformId = 3` (`VER_PLATFORM_WIN32_CE`), `dwMajorVersion = 4` | Documentation partially live on Learn (6,362 pages indexed); per-function "OS Versions" fields in CE 5.0/6.0 docs frequently state "Windows CE .NET 4.0 and later", which is the primary availability channel for CE 4.x facts |
| Windows CE 5.0 | `dwMajorVersion = 5` | Full documentation live (22,889 pages) |
| Windows Embedded CE 6.0 (incl. R2/R3) | `dwMajorVersion = 6` | Full documentation live (23,713 pages); redesigned kernel |

`dwPlatformId = 3` for Windows CE: stated in MSDN Magazine (June 2001, Learn archive) — *"the constant for Windows CE is defined only in the headers file for Windows CE, it's easy to find out that the value is 3"* — and independently defined as `VER_PLATFORM_WIN32_CE 3` in the public-domain MinGW w32api `winnt.h`. Record `winnt-VER_PLATFORM_WIN32_CE` therefore carries two independent sources (`msdn-mag-archive`, `mingw-org-w32api`).

Out of collection-target scope but indexed for context: Windows Embedded Compact 7 (20,286 pages) and 2013 (16,863 pages).

## 2. Processor architectures

Evidence status: CE 6.0 official documentation confirms the families below; the exact per-version variant matrix for CE 4.x/5.0 is an open item (OQ-4) to be completed from the CE 5.0 BSP documentation tree.

| Family | CE 6.0 evidence (MS Learn) | Notes for headers |
| --- | --- | --- |
| **ARM** (ARMv4/ARMv4I/ARMv4T; VFP support; VIVT/VIPT cache) | "ARM Architecture Support" (`ee482755`); "ARM Family Processors" branch incl. "ARM Calling Sequence Specification" | Primary CE target; single calling convention (AAPCS-style); `_M_ARM`, `ARM` predefined in CeGCC front ends (evidence: `cegcc` docs) |
| **MIPS** (MIPS II / MIPS IV; MIPS16 ASE) | "MIPSII and MIPSIV Kernel" (`ee478776`); "MIPS Family Processors" branch (compiler options `/QMmips16`, `/QMmipsNN`) | MIPS16 function attribute handling is a header/toolchain consideration |
| **SH (Renesas)** (SH-4; SH-3 in earlier versions) | "Renesas Family Processors" branch; "Renesas SH-4 Calling Sequence Specification"; SHx BSP section | Older CE versions also ran SH-3 |
| **x86** (CEPC) | "x86 Kernel" (`ee478298`); CEPC BSP documentation | `cdecl`/`stdcall` distinction is real here (see `unicode-aw-policy.md` §5 / `spec-windef.md`) |

Normative for the future headers: no `#pragma pack` assumptions beyond documented defaults; alignment-sensitive structures (e.g. `SYSTEM_INFO` union) are taken verbatim from documented layouts.

## 3. Kernel and process model (context for spec decisions)

| Property | CE ≤ 5.0 | CE 6.0 |
| --- | --- | --- |
| Process count / VM | 32 processes; 32 MB VM per process | ~32,000 processes; 2 GB VM per process (kernel redesign) — source: MSDN Magazine, December 2006 CE 6.0 article (`msdn-mag-archive`) |
| Kernel mode drivers | Drivers and OS largely in-kernel (`nk.exe`); `SetKMode` exists | User/kernel split with kernel.dll; driver model revised |
| Consequence for us | Version gating on `_WIN32_WCE >= 0x0600` for CE6-only APIs (e.g. new memory APIs) | |

## 4. Filesystem and object store (behavioural constraints affecting headers)

Documented CE facts (CE 5.0/6.0 docs, `CreateFile`/`CreateProcess` pages):

* **No current directory** — "The OS does not support the concept of a current directory." ⇒ APIs taking relative paths resolve against the root; the header set must not assume `SetCurrentDirectory` semantics exist (function presence is version-gated).
* **Object store** — RAM file system with compression behaviour tied to `FILE_FLAG_RANDOM_ACCESS` (CE 5.0 `CreateFile` remarks).
* **`FILE_FLAG_OVERLAPPED` not supported** — "This flag is not supported; however, multiple read/write operations pending on a device at a time are allowed."
* Executable search order (CreateProcess) differs by CE version (documented lists; recorded in `data/mslearn-facts/`).

## 5. Import-library model (summary; full spec in `def-requirements.md`)

| Library | Binds to | Documented evidence (examples) |
| --- | --- | --- |
| `coredll.lib` | `coredll.dll` | CreateProcess, CreateFile, ReadFile, GetVersionEx, VirtualAlloc, … (CE 5.0 + 6.0 pages) |
| `Nk.lib` | kernel | WaitForMultipleObjects (CE 5.0 and CE 6.0 pages list `Nk.lib`) |
| `Msgbox.lib` | `msgbox.dll`* | MessageBox (CE 5.0 + 6.0 pages) — *CE-specific import library for a single API family |
| `Ws2.lib` | `ws2.dll`* | WSAStartup (header `Winsock2.h`) — desktop uses `Ws2_32.lib`; CE's is a distinct library name |
| `aygshell.lib`, `commctrl.lib`, `commdlg.lib`, `ole32.lib`, … | shell/UI/COM satellites | AYGShell Reference, Common Controls Reference, … (inventories under `data/mslearn-inventories/`) |

(*DLL names inferred from library names; exact module names are a Phase 2 runtime-verification item — OQ-6.)

## 6. What CE is *not* (normative reminders)

* Not 64-bit (charter C-1): no `WOW64*`, no `*_64` file APIs, no pointer-size-dependent handles.
* Not Win32-desktop: no ANSI default, no `SetCurrentDirectory` pre-3.0? (function exists but semantics differ), no LSA/ACL-complete model in older versions, no desktop `kernel32/user32/gdi32` split.
* Not PocketPC-locked: the base OS surface (coredll) is broader than any device shell; shell APIs (AYGShell) are gated separately.
