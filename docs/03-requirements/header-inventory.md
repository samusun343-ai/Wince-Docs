# Header Inventory and Construction Roadmap

Status: Normative roadmap | Defines the COMPLETE scope of the future `include/` tree, with per-header source mapping and priorities

## 1. Derivation principle

The header set is derived from the **official API reference organization** (inventories under `data/mslearn-inventories/`), not from any SDK's file layout. Mapping rule: each documentation reference area maps to the header(s) named by that area's per-page `Requirements: Header` fields — which are harvested per function and recorded in the fact DB. The counts below are the measured documentation page counts (CE 6.0 / CE 5.0) and represent the authoritative scope of each header's content.

## 2. Priority classes

* **P0** — required for "hello world"-level CE development and for the conformance harness (Phase 2 entry criteria).
* **P1** — the common application surface (files, registry, memory, sync, time, strings, UI core, GDI core, Winsock).
* **P2** — the full documented surface (controls, shell, COM/OLE, DB, security, device management, …).

## 3. Inventory

### P0 — foundation (first-batch specs already delivered in `docs/05-specs/`)

| Header | Documentation source area (CE6/CE5 pages) | Spec status |
| --- | --- | --- |
| `windef.h` | cross-cutting; calling conventions, base types, `MAX_PATH` (docs reference `windows.h` umbrella; conventions per `unicode-aw-policy.md` §5) | **full enumeration delivered** (`spec-windef.md`) |
| `winnt.h` (core subset) | cross-cutting; `OSVERSIONINFO` (Core OS › System Management Structures), platform id, base types | **core subset enumerated** (`spec-winnt.md`); full winnt expansion is P1 |
| `winerror.h` | Core OS › Error Values › System Errors tables (571 codes CE6 / 570 CE5) | **complete enumeration delivered** (`spec-winerror.md` + `data/mslearn-facts/ce60-system-errors.json`) |
| `winbase.h` (core) | Core OS › Process and Thread (39), Memory Management (35), Synchronization (25), Time (26), System Management, DLL, String, ToolHelp, Debugging (32) reference areas; File I/O Reference (48) | **core function set enumerated** (`spec-winbase-core.md`; 64 pages harvested); remainder P1 |

### P1 — common application surface

| Header | Documentation source area (CE6/CE5 pages) | Notes |
| --- | --- | --- |
| `winbase.h` (remainder) | File I/O (48), File Mapping, Registry (30 CE6), Database (134 CE6 — legacy CE database API), Find/FindNext pages, ToolHelp, Interlocked/other subareas of Core OS Reference (408 total) | includes CE-modified items e.g. `BY_HANDLE_FILE_INFORMATION.dwOID` |
| `winuser.h` | GWES › Windows Reference (56), Window and Control Styles (24), Window Class Reference, Window Properties, Windows Timer, Keyboard Reference (49), Menus, Carets, Atoms | message constants (`WM_*` pages exist per message, values from desktop-common records) |
| `wingdi.h` | GDI Reference — Functions (132), Structures (29), Macros (7), Messages (5), Raster Operation Codes (2) | |
| `windowsx.h`, `winuser` macros | Window Control Reference pages | P1 tail |
| `winsock2.h` / `winsock.h` | Winsock Reference (110 CE6) + SPI (57) | header `Winsock2.h`, library `Ws2.lib` per Requirements; **BSD-licensed portions if reused from w32api carry file-level attribution** (`mingw-org-w32api` audit) |
| `ws2tcpip.h`, `ws2ip6.h` | Winsock IPv6 / getaddrinfo pages; CeGCC ChangeLog.ce documents the CE availability of `getaddrinfo` family | |
| `msgqueue.h` | Core OS › Message Queue Point-to-Point (msqueued APIs) | CE-only header |
| `toolhelp.h` | Core OS › ToolHelp Reference (snapshot/process APIs) | CE-specific toolhelp surface |
| `pwindow.h`/`aygshell.h` | AYGShell Reference (60) | CE/PocketPC shell extension |
| `commctrl.h` | Common Controls Reference (828 CE6/826 CE5) | largest single area; includes command bands/bars (CE-specific) |
| `commdlg.h` | Common Dialog Boxes (within Common Controls area, 37 Dialog Boxes pages + others) | `OPENFILENAME` structure page documented |
| `stdlib`-boundary | n/a — see `include-tree.md` §5 (CRT is out of the OS-header set) | |

### P2 — full documented surface (selection; full lists in `data/mslearn-inventories/`)

| Header | Documentation source area | Pages (CE6) |
| --- | --- | --- |
| `shellapi.h`, `ceshell`/shell items | Standard Shell Reference, Console Reference | 93 |
| `ole2.h`, `oleauto.h`, `oaidl.h`… | Automation Reference (303), COM/DCOM Reference (860), OLE | 1,163+ |
| `cred.h`? `security` headers | Security (Crypt, Certificates) areas | ~300 |
| `db_*.h`? | Database Reference (legacy CE data store) | 134 |
| `storemgr.h`, `fsdmgr.h`, `bootpart.h` | Storage Manager / FSD / Partition references | ~150 |
| `ndis.h`, `ntddndis.h` | Network Driver Reference (765) | driver-facing |
| `windows.h` umbrella | — | includes everything P0–P2 applicable |

### CE-only / CE-modified items register

Facts classified `ce-modified` or `ce-only` are tracked in the fact DB; known examples so far:

| Item | Class | Evidence |
| --- | --- | --- |
| `BY_HANDLE_FILE_INFORMATION` + `dwOID` | ce-modified | CE 6.0 page `ee490365` (struct includes `DWORD dwOID`); w32api `#ifdef _WIN32_WCE` block |
| `WaitForMultipleObjects` link `Nk.lib` | ce-modified | CE 5.0 + 6.0 Requirements tables |
| `MessageBox` → `Msgbox.lib` | ce-only binding | CE 5.0 + 6.0 Requirements tables |
| `WSAStartup` → `Ws2.lib` | ce-modified (desktop: `Ws2_32.lib`) | Requirements tables |
| `ReadFileWithSeek`/`WriteFileWithSeek` (FSD surface) | ce-only | Core OS/File Sys docs |
| `SHCreateMenuBar` | ce-only (AYGShell) | AYGShell Reference |
| `WinMain` entry with `LPWSTR` | ce-modified | CE 5.0 + 6.0 pages |

## 4. Version coverage rules

1. Every header's items carry `introduced`/`removed` from the documented "OS Versions" field (e.g. `WaitForMultipleObjects`: "Windows CE 1.01 and later").
2. The header set targets CE 4/5/6 by default; items introduced after 6.0 do not exist in this lineage (Compact 7/2013 are out of scope).
3. Where CE 5.0 and CE 6.0 documentation differ on a requirement (e.g. link library), both records are kept and the difference is visible in the spec (`spec-winbase-core.md` shows the CE5/CE6 columns).

## 5. Definition of done per header (summary; full template in `spec-template.md`)

1. All pages of the mapped documentation area are represented as fact records (inventory closure).
2. Every record: classified (common/ce-modified/ce-only), versioned, sourced (`src[]`), statused.
3. Enumeration spec written per template; validator passes.
4. For P0/P1 headers: runtime spot-verification list produced for Role C.
