# Specification — `commctrl.h` + `prsht.h` (common controls, full documented set)

Status: final (P2 harvest batch) | Priority: P1 (the control families beyond the P1 command-surface batch) | Fact source: `data/facts/commctrl-controls.yaml` (760 records) + `commctrl-ce.yaml` (237)
Harvest basis: remaining Common Controls Reference subareas, both docsets — Animation 13+13, CapEdit 3+3, Controls 2+2, Custom Draw 2+2, Date and Time Picker 32+32, Header 45+45, List-View 216+216, Month Calendar 50+50, Progress Bar 9+9, Property Sheets 52+52, Rebar 33+33, SbEdit 1+1, Status Bars 16+16, Tab 57+57, Toolbar 65+65, ToolTips 35+35, Trackbar 30+30, Tree View 84+84, Up-Down 18+16 — 1,524 harvested pages.

## 1. Purpose and scope

The complete documented CE common-control application surface beyond the command bars/bands and dialogs of `spec-commctrl-ce.md`: all control styles, messages, notifications, structures and macros for list-view, tree-view, toolbar, tab, tooltip, rebar, status, trackbar, up-down, progress, animation, header, month-calendar, date-time-picker, property sheets (`prsht.h`), plus the CE-only **CapEdit**/**SbEdit** control extensions and the custom-draw protocol. 760 new records; together with `commctrl-ce.yaml` (237) this closes the common-controls area to 997 records against 828+826 documented pages.

## 2. Dependencies

`winuser.h` (messages, NMHDR), `wingdi.h` (COLORREF), `prsht.h` standalone (property sheets); `commctrl.h` includes neither on desktop — same here.

## 3. Enumeration by family (record counts are post-merge; full lists in the fact YAML)

| Family | Functions/macros | Messages/notifications | Structures | Constants | Notable CE facts |
| --- | --- | --- | --- | --- | --- |
| List-View | 60 (LVM macros `ListView_*`) | 96 (LVM_*, LVN_*) | 26 (LVITEM, LV_COLUMN, NMLVDISPINFO, NMLVODSTATECHANGE, …) | 33+ (LVS_* in style tables) | CE style subset documented; `LVS_EX_NOFOCUSRECT` (CE 5.0 page typo `NOFOSUCRECT` — P1 finding, headers define correct spelling only) |
| Tree View | 26 | 42 (TVM_*, TVN_*) | 12 (TVITEM, NMTVDISPINFO, …) | 9 | `TreeView_InsertItem` macro documented "Windows CE 1.0 and later" |
| Toolbar | 18 | 30 (TB_*, TBN_*) | 10 (TBBUTTON, TBADDBITMAP, NMTBHOTITEM, …) | 13+ | `TBSTATE_`/`TBSTYLE_` subset documented; command-bar bridging per `spec-commctrl-ce.md` |
| Tab | 12 | 25 (TCM_*, TCN_*) | 5 | 18 | |
| Property Sheets (`prsht.h`) | 14 (PSP/PSN macros, `PropertySheet`) | 18 (PSN_*, PSM_*) | 9 (PROPSHEETHEADER, PROPSHEETPAGE, NMPSHNOTIFY, …) | — | documented header **prsht.h** on all 32+32 records — R-HDR-17 keeps it a standalone header |
| Month Calendar | 10 | 20 (MCM_*, MCN_*) | 8 (SYSTEMTIME-based ranges, NMSELCHANGE, …) | 6 | |
| Header | 10 | 20 (HDM_*, HDN_*) | 7 (HDITEM, HD_LAYOUT, NMHDDISPINFO, …) | 5 | |
| ToolTips | 8 | 18 (TTM_*, TTN_*) | 4 | 2 | |
| Rebar | 6 | 16 (RB_*, RBN_*) | 5 (REBARINFO, REBARBANDINFO, NMRBAUTOSIZE, …) | 6 | |
| Date and Time Picker | 6 | 14 (DTM_*, DTN_*) | 3 (SYSTEMTIME pairs) | 8 | |
| Trackbar | 6 | 16 (TBM_*, TBN_*) | 2 | 6 | |
| Up-Down | 4 | 10 (UDM_*, UDN_*) | 2 | 8 | **`UDM_SETPOS32`/`UDM_GETPOS32` documented CE 6.0 only** — gate `_WIN32_WCE >= 0x0600` |
| Status Bars | 4 | 9 | 3 | — | `SB_*` parts; draws via drawmbar-lib bridging (P1 lib finding) |
| Progress Bar | 3 | 6 (PBM_*, PBN_*) | 1 | 2 | |
| Animation | 2 | 6 | 1 (ANIMATEINFO) | — | AVI playback via `ACM_OPEN` (multimedia crosslink) |
| CapEdit (ce-only) | 3 | — | — | — | CE-specific edit variant (`CapEdit Controls Reference`) |
| SbEdit (ce-only) | 1 | — | — | — | single documented function `SbEdit`? — see record; CE soft-button edit control |
| Custom Draw | 2 | 4 (NM_CUSTOMDRAW, CDDS_*, CDRF_*) | 2 (NMCUSTOMDRAW) | — | protocol pages; `CDDS_*`/`CDIS_*` constants in style tables |
| Common | ImageList crosslink | WM_NOTIFY plumbing | NMHDR | CCS_*/ILC_* | already in `commctrl-ce.yaml` |

## 4. A/W and export-form notes

CE is Unicode-only: the generic `LVM_GETITEM`-style macros resolve to the `W` forms only (w32api lineage defines e.g. `#define LVM_GETITEM LVM_GETITEMW`); the header set defines both the generic macro and the `W` constant, never the `A` constant. No `A`-suffixed control message is documented on CE.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0600` | `UDM_SETPOS32`, `UDM_GETPOS32` (only docset delta found in the area) |
| per-record `introduced` | 1.0 (most macros/messages), 2.0/2.1 (rebar, month calendar, DTP on some pages) |

Zero CE5→CE6 library binding changes in this area (commctrl.lib on the six records that state a library; the majority of pages state none — macro-only pages).

## 6. Implementation notes for Role B

1. **R-HDR-17**: `prsht.h` remains a standalone header included by application code; `commctrl.h` does not include it.
2. Message constants without numeric values in the CE docs carry **symbolic definitions** from the public-domain w32api lineage (e.g. `#define LVM_GETITEM LVM_GETITEMW`, `#define UDM_SETPOS32 (WM_USER+113)`) — emit them as-is; Role C probes numeric equality on device.
3. Structure packing: all documented structures are natural-aligned 32-bit; static-assert sizes for `LVITEM`, `TVITEM`, `TBBUTTON`, `REBARBANDINFO`, `PROPSHEETHEADER`, `PROPSHEETPAGE` (largest ABI surface in the whole header set).
4. CapEdit/SbEdit: CE-only controls — declare their messages under a `_WIN32_WCE` invariant (no desktop guard).
5. `ListView_*`/`TreeView_*`/`Header_*` macro families are message wrappers — define as macros, no `.def` entries.

## 7. Closure statement

1,524 of 1,524 pages of the remaining control subareas are represented (760 records after docset merge and 191-name cross-dedupe against the P1 batch). Combined with `commctrl-ce.yaml`, the Common Controls Reference closure is: 828 (ce60) + 826 (ce50) pages → 997 records + 64 style-table pages (793 constant rows, recorded in P1). Excluded: none. Remaining known gaps: none in this area; the `shobjidl.idl` COM interfaces deferred to P2 (see `spec-shellapi.md` §7).

## 8. Verification hooks

L2: family `sizeof` asserts listed in §6.3; `WM_USER`-based message arithmetic. L3: create each control class on CE 5.0 and CE 6.0 images and send the documented minimum message set; verify `UDM_SETPOS32` absence on CE 5.0; custom-draw cycle on list-view.
