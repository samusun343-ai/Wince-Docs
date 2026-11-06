# Specification — `commctrl.h` (CE command surface) + `commdlg.h` (CE subset)

Status: final (Phase 1 core set) | Priority: P1 | Fact source: `data/facts/commctrl-ce.yaml` (237 records), page records `data/mslearn-facts/ce50-ce60-commctrl-ce-facts.json` (130 pages) + image-list pages from the window-control harvest

## 1. Purpose and scope

The Windows CE-specific command UI surface and the documented common-dialog subset: **Command Bars** and **Command Bands** (the CE replacement for desktop toolbars/menu bars, no `CreateWindow`-based menubar idiom), **image lists**, `InitCommonControls(Ex)`, the `WM_NOTIFY` protocol, and the CE common dialogs (`GetOpenFileName`, `GetSaveFileName`, `ChooseColor`, `ChooseFont`, `PrintDlg`, `PageSetupDlg`). 90 function records, 12 structure/type records, 1 message record family (`WM_NOTIFY` + `NM_*` notifications), plus the classic-control style constants the CE docs table under "Control Styles" pages (CBS/LVS/TBS/TCS/TVS/… name sets).

The full common-control set (list-view, tree-view, header, tab, date-time picker, month calendar, property sheets, up-down, animation, capedit, rebar, status bars, toolbars, tooltips, trackbar — 828 inventory pages) is **P2**; this spec covers the CE-differentiating core the docs group under "Command Bands Reference", "Command Bars Reference", "Common Control Reference" and "Common Dialog Boxes Reference".

## 2. Dependencies

`winuser.h` (windows, messages), `windef.h`, `wingdi.h` (bitmaps in image lists/command bars), `commctrl.h`-internal version gating (`_WIN32_WCE` per versioning-gating.md).

## 3. Documented import-library map

| Library | Fn count | Representative functions |
| --- | --- | --- |
| `commctrl.lib` | 50 | all `CommandBar_*`, `CommandBands_*`, `ImageList_*`, `InitCommonControls(Ex)` |
| `commdlg.lib` | 4 | `ChooseColor`, `CommDlgExtendedError`, `PageSetupDlg`, `PrintDlg` |
| `fileopen.lib` | 2 | `GetOpenFileName`, `GetSaveFileName` |
| *(none documented)* | 34 | notifications (NM_*), hook procedures, macros, constants |

CE 5.0 → CE 6.0: zero real binding deltas. `GetOpenFileName`/`GetSaveFileName` binding to `fileopen.lib` (not `commdlg.lib`) is a **CE-specific library split** the `.def` layer MUST reproduce (R-DEF).

## 4. Command Bars (CE-only API, 16 pages)

`CommandBar_Create(HINSTANCE hInst, HWND hwndParent, int idCmdBar)`, `CommandBar_AddBitmap`, `CommandBar_AddButtons`, `CommandBar_AddToolTips`, `CommandBar_AddAdornments`, `CommandBar_AlignAdornments`, `CommandBar_Destroy`, `CommandBar_DrawMenuBar`, `CommandBar_GetMenu`, `CommandBar_Height`, `CommandBar_InsertButton`, `CommandBar_InsertComboBox`, `CommandBar_InsertMenubar(Ex)`, `CommandBar_IsVisible`, `CommandBar_Show`. Documented signatures verbatim in the YAML; all `commctrl.lib`, all CE-only (no desktop counterpart — desktop uses `CreateToolbarEx`/`CreateWindow(TOOLBARCLASSNAME)`).

## 5. Command Bands (CE-only API, 8 pages)

`CommandBands_Create`, `CommandBands_AddBands`, `CommandBands_AddAdornments`, `CommandBands_Show`, `CommandBands_GetCommandBar`, `CommandBands_GetRestoreInformation`, `CommandBands_Height` — the banded (multiple-row, collapsible) command surface for handheld form factors. `REBARBANDINFO`-family structures are consumed via `CommandBands_AddBands` (structure pages belong to the P2 rebar area).

## 6. Image lists (31 functions)

Complete documented set (`ImageList_Add`, `_AddMasked`, `_BeginDrag`, `_Copy`, `_Create`, `_Destroy`, `_DragEnter`, `_DragLeave`, `_DragMove`, `_DragShowNolock`, `_Draw`, `_DrawEx`, `_Duplicate`, `_EndDrag`, `_GetBkColor`, `_GetDragImage`, `_GetIcon`, `_GetIconSize`, `_GetImageCount`, `_GetImageInfo`, `_GetOverlayImage`, `_Read`, `_Remove`, `_Replace`, `_ReplaceIcon`, `_SetBkColor`, `_SetDragCursorImage`, `_SetIconSize`, `_SetImageCount`, `_SetOverlayImage`, `_Write`) — desktop-family API, `commctrl.lib`, documented on CE 4.0+ pages.

## 7. `WM_NOTIFY` protocol and notifications

`WM_NOTIFY` page documents the `NMHDR`-based protocol; notification constants documented as pages: `NM_CLICK`, `NM_DBLCLK`, `NM_HOVER`, `NM_KEYDOWN`, `NM_KILLFOCUS`, `NM_OUTOFMEMORY`, `NM_RCLICK`, `NM_RDBLCLK`, `NM_RETURN`, `NM_SETFOCUS`; macros `FORWARD_WM_NOTIFY`, `HANDLE_WM_NOTIFY`, `INDEXTOSTATEIMAGEMASK`. Values from the w32api lineage (`verify-runtime`); the classic-control notifications (`BN_`, `EN_`, `LBN_`, `CBN_`) are documented inside the control pages of the window-control area (winuser spec §5.3 covers the message families).

## 8. Common dialogs (CE subset)

| Function | Library | Notes |
| --- | --- | --- |
| `GetOpenFileName` / `GetSaveFileName` | `fileopen.lib` | consume `OPENFILENAME` (structure page in P2 set); CE file dialogs are full-screen |
| `ChooseColor` | `commdlg.lib` | `CHOOSECOLOR` |
| `ChooseFont` | *(page: no library line)* | `CHOOSEFONT` |
| `PrintDlg` / `PageSetupDlg` | `commdlg.lib` | printing on CE via PCL/Bluetooth-transport printers |
| `CommDlgExtendedError` | `commdlg.lib` | returns `CDERR_*` codes (P2 constant set) |

Hook procedures documented as pages: `CCHookProc`, `CFHookProc`, `PagePaintHook`, `PageSetupHook`, `PrintHookProc`; dialog messages `CDM_SETDEFEXT`, `CDN_TYPECHANGE` (generic file-dialog customization — the full `CDM_*`/`CDN_*` set is P2).

`GetOpenFileName` in CE defaults to full-screen behaviour and the `OFN_EXPLORER`-style flags are not the CE model (flag-level diff at P2 against the documented parameter tables).

## 9. Classic-control style constants (documented name sets)

The CE "Control Styles" pages document the name sets routed into this YAML: Combo Box 11 (`CBS_SIMPLE`, `CBS_DROPDOWN`, `CBS_DROPDOWNLIST`, …), List View 17 (+ extended list including CE-only `LVS_EX_NOFOCUSRECT`), Header 5, Month Calendar 6, Date/Time Picker 8, Progress Bar 2, Rebar 8, Tab 18, Toolbar 13, ToolTip 2, Trackbar 13, Tree View 9, Up-down 8, and the basic common-control styles 11 (`CCS_TOP`, `CCS_NOMOVEY`, `CCS_NORESIZE`, …). Values from the w32api lineage (`verify-runtime`), with two special cases:

* `LVS_EX_NOFOCUSRECT` — CE-only; **no value in any approved source** (w32api wip branch predates it) — OQ-15.
* CE 5.0's "List View Styles" page contains the typo `LVS_EX_NOFOSUCRECT` (CE 6.0 spells it correctly) — the header set MUST define only the correct spelling; the typo is recorded as documentation evidence, never as an identifier.

## 10. A/W and export-form notes

All command-bar/band and dialog functions are generic-named, wide-only (R-AW-4); `OPENFILENAME.lpwstrFilter`-style members are wide at export form. `InitCommonControlsEx (function)` page title carries a disambiguation suffix — canonical name `InitCommonControlsEx` (normalisation recorded in the generator).

## 11. Open items forwarded

* OQ-21 *(new)*: `REBARBANDINFO`/`OPENFILENAME`/`CHOOSECOLOR`/`TBBUTTON`-family structure pages (P2 harvest of the remaining 700 common-control pages).
* OQ-15 *(shared)*: `LVS_EX_NOFOCUSRECT` value.
