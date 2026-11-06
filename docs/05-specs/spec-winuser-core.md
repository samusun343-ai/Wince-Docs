# Specification — `winuser.h` (core set)

Status: final (Phase 1 core set) | Priority: P1 | Fact source: `data/facts/winuser-core.yaml` (688 records), page records `data/mslearn-facts/ce50-ce60-winuser-facts.json` (430 pages), `ce50-ce60-window-control-facts.json` (609 pages), `ce-style-tables.json`

Full `winuser.h` closure (keyboard input, accelerators, clipboard formats beyond the documented set, drag-drop, DDE, hooks) extends into P2; this spec enumerates **everything harvested from the CE 5.0 and CE 6.0 GWES documentation** for window management, window classes, messages, dialogs, menus, scroll bars, carets, atoms, window properties, timers, system information, resources, and the classic controls (button, combo, edit, list box, static), plus the CE keyboard reference.

## 1. Purpose and scope

The user/GWES surface of the API: windows, classes, the message system, dialogs, menus, classic controls, carets, clipboard, timers, keyboard input and system metrics. CE-specific findings: a heavily fragmented documented import-library map (§3), CE-only window styles (§5.2), a CE-specific documented header `pwinuser.h` for keyboard-internal functions (§8), and `WS_OVERLAPPEDWINDOW` being documented as unsupported.

## 2. Dependencies

`windef.h` (types, callbacks), `winnt.h` (constant macros), `winerror.h` (failure semantics), `wingdi.h` (HDC, paint interplay).

## 3. Documented import-library map (the `.def`-driving result)

The CE pages' Requirements blocks name **twenty different link libraries** for this header's functions (CE 5.0 and CE 6.0 agree after case normalisation — zero real binding deltas). Counts are per canonical function records in `winuser-core.yaml`:

| Library | Fn count | Representative functions (complete lists in the YAML) |
| --- | --- | --- |
| `coredll.lib` | 39 | `CheckDlgButton`, `GlobalAddAtom`, `ScrollDC`, `FindResource`, `LoadResource`, `LockResource`, `SizeofResource`, `KeybdGetDeviceInfo`, `GetSystemPowerStatusEx(2)` |
| *(none documented)* | 98 | `CreateWindowEx`, `RegisterClass`, `DefWindowProc`, `GetMessage`, `ShowWindow`, `SetFocus`, … — pages carry a Header line but no Link Library line |
| `dlgmgr.lib` | 18 | `CreateDialogIndirect(Param)`, `DialogBoxIndirectParam`, `DefDlgProc`, `EndDialog`, `GetDlgCtrlID`, `CheckRadioButton`, … |
| `menu.lib` | 16 | `CreateMenu`, `CreatePopupMenu`, `DeleteMenu`, `DestroyMenu`, `EnableMenuItem`, `GetMenuItemInfo`, `CheckMenuItem`, … |
| `clipbd.lib` | 14 | `OpenClipboard`, `CloseClipboard`, `EmptyClipboard`, `GetClipboardData`, `GetClipboardDataAlloc` (CE-only fn), … |
| `caret.lib` | 12 | `CreateCaret`, `DestroyCaret`, `ShowCaret`, `HideCaret`, `GetCaretPos`, `SetCaretBlinkTime`, … |
| `kbdui.lib` | 8 | `GetAsyncShiftFlags` (CE-only), keyboard-layout functions |
| `icon.lib` | 5 | icon enumeration/lookup functions |
| `accel.lib` | 4 | `CreateAcceleratorTable`, `DestroyAcceleratorTable`, `LoadAccelerators`, `TranslateAccelerator` |
| `sbcmn.lib` | 4 | `GetScrollInfo`, `SetScrollInfo`, `SetScrollPos`, `SetScrollRange` |
| `wmgr_c.lib` | 3 | window-manager internals group |
| `uibase.lib` | 2 | base UI group |
| `drawmbar.lib` | 1 | `DrawMenuBar` |
| `coreimm.lib` | 1 | immediate-mode core group |
| `wmbase.lib` | 1 | window-manager base |
| `loadimg.lib` | 1 | image-loading group |
| `msgbeep.lib` | 1 | `MessageBeep` |
| `msgbox.lib` | 1 | `MessageBox` |
| `hotkey.lib` | 1 | `RegisterHotKey`/`UnregisterHotKey` group |
| `winmgr.lib` | 1 | window-manager group |

**Design consequence (R-DEF):** the generated `.def`/import-library surface for GWES functions cannot be a single `coredll.def`. The project's `.def` generator MUST emit one import-library per documented library name, each backed by the runtime module resolved at Role C time (OQ-6); the 98 undocumented-binding functions default to the GWES runtime module hypothesis (`coredll.dll`/`gwes.dll` — OQ-14).

## 4. Functions (complete harvested set: 231 records)

All records: `winuser-core.yaml` (`kind: function`), each with the verbatim documented signature (CE 6.0 form; CE 5.0 pages glue type tokens — repaired mechanically, raw text preserved in the page records), documented header, documented library, and "OS Versions" (`introduced`). Highlights requiring spec-level attention:

| Function | Documented signature (CE 6.0) | Notes (documented) |
| --- | --- | --- |
| `CreateWindowEx` | `HWND CreateWindowEx(DWORD dwExStyle, LPCTSTR lpClassName, LPCTSTR lpWindowName, DWORD dwStyle, int x, int y, int nWidth, int nHeight, HWND hWndParent, HMENU hMenu, HINSTANCE hInstance, LPVOID lpParam)` | `WS_OVERLAPPEDWINDOW` **not supported on CE**; compose `WS_OVERLAPPED\|WS_CAPTION\|WS_SYSMENU\|WS_THICKFRAME\|WS_MINIMIZEBOX\|WS_MAXIMIZEBOX` (documented remark, both docsets) |
| `RegisterClass` / `GetClassInfo` / `UnregisterClass` | see YAML | consume `WNDCLASS` (§5.1) |
| `GetMessage` / `PeekMessage` / `PostMessage` / `SendMessage` / `SendMessageTimeout` / `SendNotifyMessage` / `PostThreadMessage` / `DispatchMessage` / `TranslateMessage` | see YAML | `GetMessage`: `coredll.lib` documented |
| `GetMessageSource` | `UINT GetMessageSource( )` | **CE-only function** (no desktop counterpart) |
| `SetTimer` / `KillTimer` / `SystemIdleTimerReset` | see YAML | `SystemIdleTimerReset` is CE-specific (idle timer); `KillTimer` page documents header winbase.h (docs inconsistency — kept in winuser per project header map, note recorded) |
| `GetSystemMetrics` | `int GetSystemMetrics(int nIndex)` | documented 28-entry SM_ table + an explicit **unsupported list** (below §5.4) |
| `SystemParametersInfo`, `GetSysColor`, `SetSysColors` | see YAML | system information area |
| `GetSystemPowerStatusEx` / `GetSystemPowerStatusEx2` | see YAML | CE battery status API; headers documented as winbase.h — project placement winbase.h, cross-linked here |
| clipboard set | see YAML | incl. CE-only `GetClipboardDataAlloc` |
| keyboard set (51 pages) | see YAML | incl. CE-only `GetForegroundInfo`, `GetForegroundKeyboardLayoutHandle`, `GetForegroundKeyboardTarget`, `GetKeyboardStatus`, `KeybdGetDeviceInfo`, `PostKeybdMessage`, `GetAsyncShiftFlags`, `AllKeys`, `EnableHardwareKeyboard` |

## 5. Structures, styles and messages

### 5.1 Structures (documented layouts, `kind: structure`)

| Structure | Documented layout highlights | Class |
| --- | --- | --- |
| `MSG` | `typedef struct tagMSG { HWND hwnd; UINT message; WPARAM wParam; LPARAM lParam; DWORD time; POINT pt; } MSG;` (both docsets) | common |
| `WNDCLASS` | `{ UINT style; WNDPROC lpfnWndProc; int cbClsExtra; int cbWndExtra; HANDLE hInstance; HICON hIcon; HCURSOR hCursor; HBRUSH hbrBackground; LPCTSTR lpszMenuName; LPCTSTR lpszClassName; }` — `HANDLE hInstance` where desktop uses `HINSTANCE`; `WNDCLASS` not `WNDCLASSEX` in the documented CE set | ce-modified (type detail) |
| `CREATESTRUCT` | `{ LPVOID lpCreateParams; HINSTANCE hInstance; HMENU hMenu; HWND hwndParent; int cy; int cx; int y; int x; LONG style; LPCTSTR lpszName; LPCTSTR lpszClass; }` | common |
| `WINDOWPOS` | `{ HWND hwnd; HWND hwndInsertAfter; int x; int y; int cx; int cy; UINT flags; }` | common |
| `STYLESTRUCT` | `{ DWORD styleOld; DWORD styleNew; }` | common |
| `MENUITEMINFO` | incl. `LPTSTR dwTypeData` — **UNICODE string member on CE** (desktop: LPTSTR via generic) | ce-modified (member type) |
| `SCROLLINFO` | standard 7-member layout (documented verbatim) | common |
| `DLGTEMPLATE` / `DLGITEMTEMPLATE` | word-aligned in-memory dialog templates (documented layouts; no `DLGTEMPLATEEX` page) | common |
| `COMBOBOXINFO` | `{ cbSize; rcItem; rcButton; stateButton; hwndCombo; hwndItem; hwndList; }` | common |
| `DRAWITEMSTRUCT` | CE docs: `ULONG_PTR itemData` | ce-modified (older desktop layouts used DWORD; modern desktop matches) |
| `MEASUREITEMSTRUCT` | CE docs: `DWORD itemData` | common |
| `DELETEITEMSTRUCT` | CE docs: `UINT itemData` (desktop modern: `ULONG_PTR`) | ce-modified (member width) |
| `ACCEL`, `INPUT`, `KEYBDINPUT`, `MOUSEINPUT`, `GET_FOREGROUND_INFO` | see YAML (keyboard area) | GET_FOREGROUND_INFO is ce-only |

Callback types documented as pages: `WNDPROC`, `DLGPROC` (`DialogProc`), `TIMERPROC`, `PropEnumProcEx`.

### 5.2 Window styles (documented CE set, `ce-style-tables.json`)

"Basic Window Styles" + "Non-client Area Styles" pages document exactly these names (identical CE 5.0/CE 6.0 sets):

* Basic: `WS_CHILD`, `WS_CLIPCHILDREN`, `WS_CLIPSIBLINGS`, `WS_DISABLED`, `WS_GROUP`, `WS_NONAVDONEBUTTON`, `WS_POPUP`, `WS_TABSTOP`, `WS_VISIBLE`, plus extended `WS_EX_NOACTIVATE`, `WS_EX_NOANIMATION`, `WS_EX_NODRAG`, `WS_EX_TOPMOST`.
* Non-client: `WS_BORDER`, `WS_CAPTION`, `WS_DLGFRAME`, `WS_HSCROLL`, `WS_VSCROLL`, `WS_OVERLAPPED`, `WS_SIZEBOX`, `WS_SYSMENU`, `WS_EX_CAPTIONOKBTN`, `WS_EX_CLIENTEDGE`, `WS_EX_CONTEXTHELP`, `WS_EX_DLGMODALFRAME`, `WS_EX_OVERLAPPEDWINDOW`, `WS_EX_STATICEDGE`, `WS_EX_WINDOWEDGE`.

CE-only styles and their evidence state:

| Constant | Value | Status | Note |
| --- | --- | --- | --- |
| `WS_EX_CAPTIONOKBTN` | 0x80000000 | verify-runtime | w32api lineage only; CE semantics: adds OK button to caption |
| `WS_EX_NODRAG` | 0x40000000 | verify-runtime | w32api lineage only; stationary window |
| `WS_EX_NOANIMATION` | *(none)* | verify-runtime | CE-documented name; no value in any approved source yet — Role C probe (OQ-15) |
| `WS_NONAVDONEBUTTON` | *(none)* | verify-runtime | CE-documented name (nav bar Done button); no value yet — OQ-15 |
| `WS_SIZEBOX` | 0x40000 | verified (w32api + desktop, alias of `WS_THICKFRAME`) | CE docs use the `WS_SIZEBOX` spelling; headers MUST define both spellings |

Cross-family verification: `WS_*`/`WS_EX_*` values agree between the w32api lineage and the desktop Win32 docs for every constant present in both (24 + 25 constants cross-checked) — recorded `verified`; the remaining control-style families (BS/ES/CBS/LBS/SS/SBS/DS/MB/SW/SM/SWP…) carry w32api-lineage values recorded `verify-runtime` pending Role C (full table in the YAML).

### 5.3 Messages (documented set: 177 records, `kind: message`)

Per family (pages exist in the CE docs, message syntax as `wParam`/`lParam` forms): `WM_*` 57, `LB_*` 37, `CB_*` 34, `EM_*` 32, `SBM_*` 7, `BM_*` 6, `STM_*` 2, `DM_*` 2. `WM_APP` and `RegisterWindowMessage` document the reserved ranges (`WM_USER`-based) — value records from the w32api lineage (`verify-runtime`). The documented set is **not** the complete desktop set; absent message pages (e.g. `WM_PAINT` is documented under the GDI area) are covered by their owning-area specs. Headers MUST NOT promise undocumented messages as functional; the `.def` surface is unaffected (messages are constants).

### 5.4 `GetSystemMetrics` (documented 28-entry table)

Supported set (names documented; values from w32api lineage, `verify-runtime`): `SM_CXSCREEN`, `SM_CYSCREEN`, `SM_CXVSCROLL`, `SM_CYHSCROLL`, `SM_CYCAPTION`, `SM_CXBORDER`, `SM_CYBORDER`, `SM_CXDLGFRAME`, `SM_CYDLGFRAME`, `SM_CYMENU`, `SM_CXFULLSCREEN`, `SM_CYFULLSCREEN`, `SM_CYVTHUMB`, `SM_CXHTHUMB`, `SM_CXICON`, `SM_CYICON`, `SM_CXSMICON`, `SM_CYSMICON`, `SM_CYSMCAPTION`, `SM_DEBUG`, `SM_MOUSEPRESENT`, `SM_SWAPBUTTON`, `SM_CMONITORS`, `SM_SAMEDISPLAYFORMAT`, `SM_CXMIN`, `SM_CYMIN`, … (complete list in YAML; 28 entries). Documented **unsupported** (must NOT be advertised): `SM_ARRANGE`, `SM_CLEANBOOT`, `SM_CMETRICS`, `SM_CMOUSEBUTTONS`, `SM_CXDRAG`, `SM_CYDRAG`, `SM_CXFRAME`, `SM_CYFRAME`, `SM_CXMINIMIZED`, `SM_CYMINIMIZED`, `SM_CXMINSPACING`, `SM_CYMINSPACING`, `SM_CXMINTRACK`, `SM_CYMINTRACK`, `SM_CXSIZE`, `SM_CYSIZE`, `SM_CXSIZEFRAME`, `SM_CYSIZEFRAME`, `SM_CXSMICON`-adjacent metrics flagged in the page remarks, `SM_MIDEASTENABLED`, `SM_NETWORK`, `SM_SECURE`, `SM_SHOWSOUNDS`, `SM_SLOWMACHINE`. Values for supported indices: `SM_CXSCREEN = 0`, `SM_CYSCREEN = 1`, … (complete mapping in YAML).

## 6. Menus, dialogs, scroll bars (subarea completeness)

Menu set (16 functions, `menu.lib`): creation, destruction, item queries, `TrackPopupMenu`, and CE 6.0-only `CustomTrackPopupMenu` (only page present in CE 6.0; CE 5.0 has no page — recorded `introduced: 6.0`, note kept). Dialog set (`dlgmgr.lib`, 18): indirect creation, `DefDlgProc`, `EndDialog`, `GetDialogBaseUnits`. Scroll bar API (17 pages incl. `sbcmn.lib` bindings).

## 7. Classic controls (button, combo, edit, list box, static)

Function + message + notification sets per control, harvested complete from the "Window Control Reference" pages: Buttons 11 pages, Combo Boxes 50, Edit Boxes 42, List Boxes 46, Static 6. Owner-draw structs (`DRAWITEMSTRUCT` family) in §5.1. Style name sets documented (§ `ce-style-tables.json`, e.g. Edit 15 names, List Box 16 names); values `verify-runtime` from the w32api lineage.

## 8. Keyboard input and `pwinuser.h` (CE-specific finding)

The CE 5.0 tree has a "Keyboard Reference" (49 pages); the CE 6.0 TOC keeps the pages under a node the inventory walker missed — supplemented from the CE 6.0 doc index (51 pages, `tools/harvest_ce60_keyboard.py`). Documented set includes desktop-family `GetAsyncKeyState`, `GetKeyState`, `MapVirtualKey`, `keybd_event`, `SendInput`, `LoadKeyboardLayout`, `GetKeyboardLayout(List/Name)`, `RegisterHotKey`, plus CE-only `GetForegroundInfo`, `GET_FOREGROUND_INFO`, `GetForegroundKeyboardLayoutHandle`, `GetForegroundKeyboardTarget`, `GetKeyboardStatus`, `KeybdGetDeviceInfo`, `PostKeybdMessage`, `GetAsyncShiftFlags`, `AllKeys`, `EnableHardwareKeyboard`.

**`pwinuser.h`**: the Requirements blocks of `GetAsyncShiftFlags`, `GetForegroundInfo`, `GetForegroundKeyboardLayoutHandle`, `GetForegroundKeyboardTarget`, `KeybdGetDeviceInfo` document header **`pwinuser.h`** — a CE-specific documented header not present in desktop Win32. Header-placement decision: the project emits these declarations in `winuser.h` (single public window header; `pwinuser.h` becomes an include-compat shim), recorded as requirement R-HDR-9 in `header-inventory.md`.

## 9. A/W and export-form notes

* All documented signatures are generic-name; the platform is wide-only (R-AW-3/R-AW-4). String-bearing members (`MENUITEMINFO.dwTypeData`, `WNDCLASS.lpszMenuName`) are `LPTSTR` in the documented generic form → `WCHAR*` at export.
* `MessageBox` remains the only documented `Msgbox.lib` binding in this header; runtime module resolution is OQ-6.

## 10. Open items forwarded

* OQ-6 (runtime modules behind the 20 documented libraries).
* OQ-14 *(new)*: binding hypothesis for the 98 functions whose pages document no link library.
* OQ-15 *(new)*: numeric values for `WS_EX_NOANIMATION`, `WS_NONAVDONEBUTTON` (no approved source states them).
* OQ-16 *(new)*: `SM_` index values on-device confirmation (w32api-lineage values are single-channel).
