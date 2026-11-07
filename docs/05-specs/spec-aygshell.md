# Specification — `aygshell.h` (AYGShell / Pocket PC shell extensions)

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/aygshell.yaml` (46 records) + 45 AYGShell names already recorded in `winuser-core.yaml` (GWES-tree pages)
Harvest basis: AYGShell Reference — 60+60 pages.

## 1. Purpose and scope

The AYGShell surface (Pocket PC/Windows Mobile-class shell on Windows CE): menu bars (`SHCreateMenuBar`, `SHMENUBARINFO`), full-screen dialog handling (`SHInitDialog`, `SHDoneButton`), SIP (soft input panel) control (`SHSipPreference`, `SHSipInfo`), gestures (`SHRecognizeGesture`), notifications (`SHNotificationAdd/Remove/Update`), shell change notification, and the app-key/hardware-button bindings. The entire header is **ce-only** (Aygshell.lib binding on 88 of the records).

**Two-file fact note:** the prior P1 harvest already captured 45 AYGShell function/structure pages through the GWES tree (they are in `winuser-core.yaml` with documented header `aygshell.h`); this batch adds the 46 records unique to the AYGShell Reference area. Role B consumes the union filtered on `target_header == aygshell.h`.

## 2. Dependencies

`winuser.h` (HWND, messages), `windef.h`. `SHACTIVATEINFO` interlocks with `WM_ACTIVATE`/`SHHandleWMActivate`; `SHRGINFO` with `SHRecognizeGesture`.

## 3. Enumeration (46 new records; union with winuser-core listed by family)

### 3.1 Shell/UI functions (Aygshell.lib)

`SHCreateMenuBar`, `SHFindMenuBar`, `SHGetMenu`, `SHGetSubMenu`, `SHSetSubMenu`, `SHInitDialog`, `SHDoneButton`, `SHFullScreen`, `SHHandleWMActivate`, `SHHandleWMSettingChange`, `SHInitExtraControls`, `SHInputDialog`, `SHNavigateBack`, `SHSetNavBarText`, `SHCloseApps`, `SHShowOutOfMemory`*.

### 3.2 SIP / input

`SHSipPreference`, `SHSipInfo` (the `sip.h`-adjacent API documented under aygshell.h), `SHGetInputContext`, `SHSetInputContext`, `WC_SIPPREF` (window class, ce-only constant).

### 3.3 Notifications / shell change

`SHNotificationAdd`, `SHNotificationGetData`, `SHNotificationRemove`, `SHNotificationUpdate` (+ `SHNOTIFICATIONDATA`), `SHChangeNotifyRegister`/`Deregister`/`Free` (+ `SHCHANGENOTIFYENTRY`), `SHCreateNewItem`, `SHGetEmergencyCallList`.

### 3.4 Context menus / property sheets / keys

`SHLoadContextMenuExtensions`, `SHFreeContextMenuExtensions`, `SHEnumPropSheetHandlers`, `SHInvokeContextMenuCommand`, `SHGetAppKeyAssoc`, `SHSetAppKeyWndAssoc`, `SHRecognizeGesture` (+ `SHRGINFO`), `SHSetBack`.

### 3.5 Command-bar messages (ce-only, documented `SHCMBM_*`)

`SHCMBM_GETMENU`, `SHCMBM_GETSUBMENU`, `SHCMBM_SETSUBMENU` — menubar messages with `SHMENUBARINFO`/`SHACTIVATEINFO`/`SHINITDLGINFO` structures and the `NMNEWMENU` family (see `spec-shellapi.md` §3.4 for the newmenu.h twins).

## 4. A/W and export-form notes

All wide/generic-only; `SHSipInfo` has an `SHSIPINFO` struct form; no A/W pairs exist in the documented set.

## 5. Version gates

Base set documented "Windows CE 3.0 and later" for the dialog/menubar core; `SHNotification*` and `SHGetInputContext`/`SHSetInputContext` pages state "Windows CE 4.0 and later"/"5.0" as recorded per record (`introduced` field). No CE5→CE6 binding changes (Aygshell.lib stable, one record differs — `SHNOTIFICATIONDATA` CE 6.0 page repeats the binding).

## 6. Implementation notes for Role B

1. **R-HDR-15**: `aygshell.h` is its own header; `shlobj.h`/`shellapi.h` do not re-export it. The project's `windows.h` does NOT include it (shell-optional component).
2. `SHCreateMenuBar` replaces `CommandBar_Create` on Pocket PC-class devices — the spec's `commctrl.h` command-bar set remains for generic CE shells; both are exported (documented).
3. `SHGetMenu`/`SHGetSubMenu`/`SHSetSubMenu` are documented as **macros/messages** (they wrap `SHCMBM_*`) — define them as macros, not imports; no `.def` entries.
4. Value channel: `SHCMBM_*` and `SHID*`/`SHBI*` constants carry w32api-lineage values (`verify-runtime`); no desktop counterpart exists.

## 7. Closure statement

60+60 AYGShell pages → 46 new + 45 pre-existing records = full coverage of the documented name set (dupes merged at harvest level; 191 cross-file skips were AYGShell/GWES overlaps). The `SipGetInfo`/`SipSetInfo`/`SipShowIM` core SIP functions documented under `pwinuser.h`-family pages are already in `winuser-core.yaml` (R-HDR-9 note).

## 8. Verification hooks

L2: `sizeof(SHMENUBARINFO)`, `sizeof(SHACTIVATEINFO)`, `sizeof(SHNOTIFICATIONDATA)`; `SHCMBM_*` values. L3: `SHCreateMenuBar` renders on Pocket PC emulator; `SHSipPreference(SIP_UP)` raises the SIP; `SHRecognizeGesture` returns `SHRG_RETURNCMD` on a gesture.
