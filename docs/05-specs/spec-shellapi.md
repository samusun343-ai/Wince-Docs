# Specification — `shellapi.h` / `shlobj.h` / `newmenu.h` / `cpl.h` / `console.h` (Standard Shell)

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/shellapi.yaml` (56 records)
Harvest basis: Standard Shell Reference — 83+83 pages; Console Reference — 10 (CE 6.0); Shell OS Reference — 4 (CE 6.0).

## 1. Purpose and scope

The standard-shell application surface of CE: file operations (`SHFileOperation`), shortcuts (`SHCreateShortcut(Ex)`, `SHGetShortcutTarget`), special folders (`SHGetSpecialFolderPath`/`Location`, `CSIDL`), icon notification (`Shell_NotifyIcon`), `ShellExecuteEx`, the folder browser (`SHBrowseForFolder`, `BFFM_*`), version/resource DIB loading (`SHLoadDIBitmap`, `SHGetFileInfo`), out-of-memory shell dialog (`SHShowOutOfMemory`), the CE control-panel applet protocol (`CPlApplet`, `CPL_*`), the CE 6.0 **new menu** (`newmenu.h`, `NMN_*`), and the CE 6.0 **console** ioctl surface (`console.h`). COM interfaces documented in the same area (`shobjidl.idl`: `IShellFolder` chain) are recorded with their idl header and are P2 for vtable layout.

## 2. Dependencies

`winuser.h`, `windef.h`, `shellapi.h` → `shlobj.h` ordering (ITEMIDLIST types), `prsht.h` for property-sheet-hosting applets.

## 3. Enumeration highlights (full list in the fact YAML)

### 3.1 shellapi.h (documented Coredll.lib/Ceshell.lib)

`ShellExecuteEx` (+ `SHELLEXECUTEINFO`), `Shell_NotifyIcon` (+ `NOTIFYICONDATA`), `SHFileOperation` (+ `SHFILEOPSTRUCT`), `SHGetFileInfo` (+ `SHFILEINFO`), `SHAddToRecentDocs`, `ExtractIconEx` (Icon.lib — documented in the Resources area), `SHGetSpecialFolderPath`, `SHGetSpecialFolderLocation`, `SHBrowseForFolder` (+ `BROWSEINFO`), `SHGetPathFromIDList`, `SHBindToParent`, `SHGetDesktopFolder`, `SHGetMalloc`, `SHLoadDIBitmap`, `SHCreateShortcut(Ex)`, `SHGetShortcutTarget`, `SHShowOutOfMemory`.
CE deltas captured in record notes: `SHFileOperation` flags subset (no `FOF_*` multi-threaded forms), `SHGetSpecialFolderPath` replaces the desktop `SHGetFolderPath` chain, `SEE_MASK_*` set is the documented subset.

### 3.2 shlobj.h

`BFFM_*` message set (`BFFM_INITIALIZED`, `BFFM_SELCHANGED`, `BFFM_SETSTATUSTEXT`, `BFFM_ENABLEOK`, `BFFM_SETSELECTION`, `BFFM_VALIDATEFAILED`), `WM_FILECHANGEINFO` (**ce-only** message, values lineage-supplied), `ITEMIDLIST`, `BrowseCallbackProc`, `FILECHANGENOTIFY`/`SHCHANGENOTIFYENTRY` struct pages (Ceshell.lib on CE 5.0 pages).

### 3.3 cpl.h — control panel applets

`CPlApplet` callback + `CPL_INIT`/`CPL_GETCOUNT`/`CPL_NEWINQUIRE`/`CPL_DBLCLK`/`CPL_STOP`/`CPL_EXIT` message records + `CPLINFO`/`NEWCPLINFO` structures. The `CPL_*` values are desktop-common (w32api cpl.h lineage, verify-runtime); CE documents the applet protocol for its own control panel.

### 3.4 newmenu.h (CE 6.0, **ce-only**)

`NMNEWMENU` structure + `NMN_GETAPPREGKEY`, `NMN_GETPROPERTYBAG`, `NMN_INVOKECOMMAND`, `NMN_NEWBUTTONUPDATED`, `NMN_NEWMENUDESTROY` messages — the shell "New" button extension. Values lineage-supplied (`verify-runtime`, OQ-19).

### 3.5 console.h (CE 6.0, **ce-only**)

The CE 6.0 console (cmd/CMD shell) ioctl interface: `IOCTL_CONSOLE_CLS`, `IOCTL_CONSOLE_FLUSHINPUT`, `IOCTL_CONSOLE_GETMODE`, `IOCTL_CONSOLE_SETMODE`, `IOCTL_CONSOLE_GETSCREENCOLS`, `IOCTL_CONSOLE_GETSCREENROWS`, `IOCTL_CONSOLE_GETTITLE`, `IOCTL_CONSOLE_SETTITLE`, `IOCTL_CONSOLE_SETCONTROLCEVENT` — all with documented 3.0+ page text but no numeric values (CTL_CODE composition unknown → OQ-26; Role C probes via `DeviceIoControl` on `CONIN$`/`CONOUT$`-class handles). `ShellRegisterCallbacks`/`SHELLCALLBACKS` (Shell OS Reference) are OEM shell integration — kept as note records, excluded from the application set.

## 4. A/W and export-form notes

Wide-only documented forms throughout. `SHGetSpecialFolderPath` exists only in the base form on CE (no `A`/`W` twins documented). `ShellExecuteEx` consumes `SHELLEXECUTEINFO` with wide `lpFile`.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0600` | `newmenu.h` set, `console.h` ioctl set, `IOCTL_CONSOLE_*` |
| 3.0/4.0 per record | base shell set (`introduced` fields) |

Libraries: **Ceshell.lib** (24 records), Coredll.lib, Aygshell.lib (1 record), Icon.lib (icon pages), Ws2.lib (SPI crosslink only).

## 6. Implementation notes for Role B

1. Header order: `shellapi.h` standalone; `shlobj.h` requires `shellapi.h` types; `newmenu.h`, `cpl.h`, `console.h` are standalone CE-only headers (**R-HDR-16**).
2. `CPL_*` constants: define from lineage values; add static assert against desktop docs channel when Role C confirms.
3. `IOCTL_CONSOLE_*`: reserve a `console.h` block with values marked open (OQ-26) — do NOT invent CTL_CODE values.
4. `SHGetMalloc` documents the OLE allocator binding — include guard comment (`__OBJC_NO_OLE`-style note; full COM surface is P2).

## 7. Closure statement

83+83 Standard Shell + 10 Console + 4 Shell OS pages → 56 records (docset-merged; overlaps with the P1 GWES/aygshell harvests — `SHNOTIFICATIONDATA` etc. — deduped into their prior files). `shobjidl.idl` COM interface pages (62 records) are recorded with `target_header: shobjidl.h, shobjidl.idl` and deferred to the P2 COM/OLE batch for vtable ordering. Nothing else excluded.

## 8. Verification hooks

L2: `sizeof(SHELLEXECUTEINFO)`, `sizeof(NOTIFYICONDATA)`, `sizeof(SHFILEOPSTRUCT)`, `CSIDL_*` values. L3: `SHCreateShortcut` + `SHGetShortcutTarget` roundtrip; `Shell_NotifyIcon` NIM_ADD visible on standard shell; `CPlApplet` protocol in a test applet; console ioctl probe on CE 6.0.
