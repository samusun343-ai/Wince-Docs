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

*Status update (P1 session):* `windef.h` (92 facts), `winnt.h` core (47), `winerror.h` (571 documented codes), `winbase.h` core functions — specs final.

| Header | Documentation source area (CE6/CE5 pages) | Spec status |
| --- | --- | --- |
| `windef.h` | cross-cutting; calling conventions, base types, `MAX_PATH` (docs reference `windows.h` umbrella; conventions per `unicode-aw-policy.md` §5) | **full enumeration delivered** (`spec-windef.md`) |
| `winnt.h` (core subset) | cross-cutting; `OSVERSIONINFO` (Core OS › System Management Structures), platform id, base types | **core subset enumerated** (`spec-winnt.md`); full winnt expansion is P1 |
| `winerror.h` | Core OS › Error Values › System Errors tables (571 codes CE6 / 570 CE5) | **complete enumeration delivered** (`spec-winerror.md` + `data/mslearn-facts/ce60-system-errors.json`) |
| `winbase.h` (core) | Core OS › Process and Thread (39), Memory Management (35), Synchronization (25), Time (26), System Management, DLL, String, ToolHelp, Debugging (32) reference areas; File I/O Reference (48) | **core function set enumerated** (`spec-winbase-core.md`; 64 pages harvested); remainder P1 |

### P1 — common application surface

*Status update (P1 session):* **`winuser.h` core, `wingdi.h` core, `winsock2.h`, `commctrl.h`/`commdlg.h` CE core specs delivered** (`spec-winuser-core.md`, `spec-wingdi-core.md`, `spec-winsock2.md`, `spec-commctrl-ce.md`); fact DBs `winuser-core.yaml` (688), `wingdi-core.yaml` (176), `winsock.yaml` (202), `commctrl-ce.yaml` (237).

*Status update (P2 session):* **3,173 further pages harvested (0 failures)** — the remaining Core-OS app subareas, File I/O/Registry/User-Mgmt/File-Sys-Password, the GWES remainder (incl. the internal-surface exclusion register), AYGShell/Standard Shell/Console/Winsock-SPI, and the full remaining common-controls set. Ten further specs delivered (`spec-winbase-file-io.md`, `spec-winreg.md`, `spec-winbase-os.md`, `spec-toolhelp.md`, `spec-msgqueue.md`, `spec-notify.md`, `spec-aygshell.md`, `spec-shellapi.md`, `spec-commctrl-controls.md`, `spec-gwes-misc.md`); 14 new fact YAMLs bring the DB to **3,177 unique records**.

| Header | Documentation source area (CE6/CE5 pages) | Notes |
| --- | --- | --- |
| `winbase.h` (remainder) | File I/O (48), File Mapping, Registry (30 CE6), Database (134 CE6 — legacy CE database API), Find/FindNext pages, ToolHelp, Interlocked/other subareas of Core OS Reference (408 total) | **File I/O + File Mapping + User Mgmt + File Sys Password + all Core-OS app subareas delivered (P2)**: `spec-winbase-file-io.md`, `spec-winbase-os.md`; remaining within this row: CeLog/NAT/State-Broker/Kernel-Marshaling subareas + Database area (P2) |
| `winreg.h` | Registry Reference (30 CE6 / 14 CE5) + pwinreg.h multi-user set | **delivered (P2)** — `spec-winreg.md` (33 records; Nkstub.lib CE6 bindings recorded) |
| `toolhelp.h` | ToolHelp Reference (18+18) | **delivered (P2)** — `spec-toolhelp.md` (Toolhelp.lib) |
| `msgqueue.h` | Message Queue Point-to-Point (9+8) | **delivered (P2)** — `spec-msgqueue.md` (ce-only) |
| `notify.h` | Notify Reference (13+13) | **delivered (P2)** — `spec-notify.md` (ce-only) |
| `windbase.h` (initial) | object-store structs + password API (File Sys Password 6+6) | **initial set delivered (P2)** in `spec-winbase-file-io.md` §3.3; full Database area (134) remains P2 |
| `winuser.h` | GWES › Windows Reference (56), Window and Control Styles (24), Window Class Reference, Window Properties, Windows Timer, Keyboard Reference (49 CE5 tree / 51 CE6 index supplement), Menus, Carets, Atoms | **core spec delivered**; 20 documented link libraries; `pwinuser.h` finding below |
| `wingdi.h` | GDI Reference — Functions (132), Structures (29), Macros (7), Messages (5), Raster Operation Codes (2) | **core spec delivered**; `coredll.lib`+`rectapi.lib`+4 specialty libs |
| `windowsx.h`, `winuser` macros | Window Control Reference pages | P1 tail (macros; message records already in fact DB) |
| `winsock2.h` / `winsock.h` | Winsock Reference (110 CE6) + SPI (57) | **core spec delivered**; `Ws2.lib` for all documented bindings; 35 documented WSAE values |
| `ws2tcpip.h`, `ws2ip6.h` | Winsock IPv6 / getaddrinfo pages; CeGCC ChangeLog.ce documents the CE availability of `getaddrinfo` family | |
| `msgqueue.h` | Core OS › Message Queue Point-to-Point (msqueued APIs) | CE-only header |
| `toolhelp.h` | Core OS › ToolHelp Reference (snapshot/process APIs) | CE-specific toolhelp surface |
| `pwindow.h`/`aygshell.h` | AYGShell Reference (60) | **delivered (P2)** — `spec-aygshell.md` (46 new + 45 pre-existing records; Aygshell.lib per-page) |
| `commctrl.h` | Common Controls Reference (828 CE6/826 CE5) | **complete (P2)** — `spec-commctrl-controls.md` adds the 760-record full control set to the P1 command surface; `prsht.h` standalone (R-HDR-17) |
| `commdlg.h` | Common Dialog Boxes (within Common Controls area, 37 Dialog Boxes pages + others) | **CE subset spec delivered**; `fileopen.lib` split recorded |
| `shellapi.h`/`shlobj.h`/`cpl.h`/`newmenu.h`/`console.h` | Standard Shell (83+83) + Console (10) + Shell OS (4) | **delivered (P2)** — `spec-shellapi.md` (56 records; shobjidl COM interfaces deferred to P2) |
| `dbgapi.h` | Debugging Reference debug macros | **delivered (P2)** — `spec-winbase-os.md` §3.11 (ce-only) |
| `stdlib`-boundary | n/a — see `include-tree.md` §5 (CRT is out of the OS-header set) | |

### P1 header-placement decisions

* **R-HDR-9.** `pwinuser.h` (documented header of `GetAsyncShiftFlags`, `GetForegroundInfo`, `GetForegroundKeyboardLayoutHandle`, `GetForegroundKeyboardTarget`, `KeybdGetDeviceInfo`): declarations live in the project's `winuser.h`; `pwinuser.h` ships as an include-compatibility shim only.
* **R-HDR-10 (P2).** `pwinreg.h`-documented functions (`SetCurrentUser`, `SetUserData`, `GetUserDirectory`): declarations in the project's `winreg.h`; `pwinreg.h` ships as shim.
* **R-HDR-11 (P2).** `Kfuncs.h`-documented basics (`GetCurrentProcess`, `SetEvent`, `DebugBreak`, …): declarations in `winbase.h`; `kfuncs.h` ships as shim. `pkfuncs.h`-only functions (`VirtualCopyEx` family, `CeRemoteHeap*`): kernel-surface — gated declarations, `.def` entry only after Role C confirms export.
* **R-HDR-12 (P2).** ToolHelp ships as `tlhelp32.h` (desktop-conventional lowercase) with documented-casing compatibility.
* **R-HDR-13 (P2).** `msgqueue.h` is its own header (ce-only); not folded into `winbase.h`.
* **R-HDR-14 (P2).** `notify.h` is its own header (ce-only); `windows.h` does not include it.
* **R-HDR-15 (P2).** `aygshell.h` is its own header; not re-exported by `shlobj.h`/`shellapi.h`.
* **R-HDR-16 (P2).** `newmenu.h`, `cpl.h`, `console.h` are standalone CE-only headers.
* **R-HDR-17 (P2).** `prsht.h` remains a standalone header; `commctrl.h` does not include it.

### CE-only register additions (P2 session)

| `WM_HIBERNATE` (0x3FF, ce-only low-memory broadcast) | ce-only | CE Resources Reference pages + w32api CE-gated lineage |
| `CeSetThreadPriority`/`CeGetThreadPriority`/`CeSetThreadQuantum`/`CeGetThreadQuantum` (0–255 native model) | ce-only | Process and Thread Reference |
| `VirtualAllocEx`/`VirtualFreeEx`/`VirtualProtectEx`/`VirtualQueryEx`/`VirtualCopyEx`/`VirtualSetAttributesEx`/`VirtualAllocCopyEx` (pkfuncs.h, CE 6.0) | ce-only | Memory Management Reference (CE 6.0 docset only) |
| `CeRemoteHeapCreate`/`CeRemoteHeapTranslatePointer`, `CeZeroPointer`, `CeGetRawTime(Offset)`, `KernelIoControl`, `GetDeviceUniqueID` | ce-only | CE 6.0 pages |
| `ReadMsgQueueEx` (6.0), `CeRegGetInfo`/`CeRegGetNotificationInfo` (6.0), `CeFindFirst/Next/CloseRegChange` (5.0), `CeRegTestSetValueW` | ce-only | msgqueue/registry pages |
| `CreateFileForMapping`, `CeGenRandom`, `CeGetCanonicalPathName`, `CeGetFileNotificationInfo`, `GetStoreInformation`, `DeleteAndRenameFile` | ce-only | File I/O Reference |
| `ReadRegData`/`WriteRegData`/`ReadGenericData`/`WriteGenericData`/`RegistryOperation` (4.2 multi-user registry) | ce-only | Registry Reference |
| `MSGQUEUE` API (`CreateMsgQueue` family) | ce-only (whole header) | Message Queue Point-to-Point Reference |
| `CeSetUserNotification(Ex)` / `CeRunAppAtTime` / `CeRunAppAtEvent` family | ce-only (whole header) | Notify Reference |
| `dbgapi.h` debug macros (`DEBUGMSG`, `RETAILMSG`, `NKDbgPrintfW`, …) | ce-only (whole header) | Debugging Reference |
| `UDM_SETPOS32`/`UDM_GETPOS32` (CE 6.0 docset only) | ce-only | Up-Down Controls Reference |
| `IOCTL_CONSOLE_*` (9 ioctls), `NMN_*` new-menu set, CapEdit/SbEdit controls | ce-only | Console/newmenu/controls references (CE 6.0) |
| Serdev/Coreloc/Coremain/Oemmain/Toolhelp/Mgprint/Msgque/ceshell import-library bindings | ce-only bindings | P2 harvest Requirements blocks |

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
| `WS_EX_CAPTIONOKBTN`, `WS_EX_NODRAG`, `WS_EX_NOANIMATION`, `WS_NONAVDONEBUTTON` | ce-only styles | CE style pages; values w32api-lineage/`verify-runtime` (OQ-15) |
| `WS_SIZEBOX` spelling (desktop `WS_THICKFRAME` alias) | ce-modified | CE Non-client Area Styles page |
| `GetClipboardDataAlloc` | ce-only function | clipboard pages (both docsets) |
| `CommandBar_*` / `CommandBands_*` (24 functions) | ce-only | Command Bars/Bands references, `commctrl.lib` |
| `GetForegroundInfo`, `GET_FOREGROUND_INFO`, `GetAsyncShiftFlags`, `GetKeyboardStatus`, `KeybdGetDeviceInfo`, `PostKeybdMessage`, `AllKeys`, `EnableHardwareKeyboard`, `GetForegroundKeyboardLayoutHandle/Target` | ce-only keyboard set | Keyboard references; documented header `pwinuser.h` (R-HDR-9) |
| `GetMessageSource`, `GetMessageQueueReadyTimeStamp`, `CustomTrackPopupMenu` (CE 6.0 only) | ce-only | Windows/Message Queue references |
| `SOL_IRLMP` (IrDA socket level) | ce-only constant | Winsock Reference |
| `LVS_EX_NOFOCUSRECT` (CE 5.0 page typo `NOFOSUCRECT`) | ce-only | List View Styles pages |
| `fileopen.lib` binding for `GetOpenFileName`/`GetSaveFileName` | ce-only binding | Common Dialog pages |

## 4. Version coverage rules

1. Every header's items carry `introduced`/`removed` from the documented "OS Versions" field (e.g. `WaitForMultipleObjects`: "Windows CE 1.01 and later").
2. The header set targets CE 4/5/6 by default; items introduced after 6.0 do not exist in this lineage (Compact 7/2013 are out of scope).
3. Where CE 5.0 and CE 6.0 documentation differ on a requirement (e.g. link library), both records are kept and the difference is visible in the spec (`spec-winbase-core.md` shows the CE5/CE6 columns).

## 5. Definition of done per header (summary; full template in `spec-template.md`)

1. All pages of the mapped documentation area are represented as fact records (inventory closure).
2. Every record: classified (common/ce-modified/ce-only), versioned, sourced (`src[]`), statused.
3. Enumeration spec written per template; validator passes.
4. For P0/P1 headers: runtime spot-verification list produced for Role C.
