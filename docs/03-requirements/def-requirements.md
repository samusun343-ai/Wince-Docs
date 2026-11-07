# Import Library (`.def`) Requirements

Status: Normative | Governs the future `def/` tree and import-library generation

## 1. Objective

Produce `.def` files (and derived import libraries) equivalent in role to mingw's `lib/*.def` set, but for Windows CE's module layout — without ever touching restricted SDK/PB material.

## 2. Module set (documented)

The documentation's per-function `Requirements → Link Library` field is the authoritative, license-clean source for the function→library mapping. Libraries observed in the harvested P0+P1 sets (per-page evidence in `data/mslearn-facts/`, per-record bindings in `data/facts/*.yaml`):

| Import library | Bindings (P0+P1 harvests) | Status |
| --- | --- | --- |
| `coredll.lib` | core OS (§ winbase spec) + 39 winuser + 100 wingdi + `GetMessage` … | documented (CE 5.0 + 6.0 pages; case-normalised identical) |
| `Nk.lib` | `WaitForMultipleObjects` (both docsets) + 7 further core-os bindings (P2 harvest) | documented |
| `Nkstub.lib` | `Sleep` + `RegCloseKey`/`RegCreateKeyEx`/`RegFlushKey`/`RegOpenKeyEx`/`RegQueryValueEx` + `CompareFileTime`/`FileTimeToSystemTime`/`SystemTimeToFileTime` (all CE 6.0 pages; CE 5.0 pages say coredll.lib) | documented (CE5→CE6 binding change) |
| `Oemmain.lib` | `GetTickCount`, `IsProcessorFeaturePresent`, `WriteDebugLED` (CE 6.0 pages) | documented (new, P2 harvest) |
| `Serdev.lib` | serial communications set (32 bindings: `SetCommState`, `WaitCommEvent`, `EscapeCommFunction`, …) | documented (new, P2 harvest) |
| `Coreloc.lib` | `LoadDriver` + locale group (22 bindings) | documented (new, P2 harvest) |
| `Coremain.lib` | core-main group (8 bindings) | documented (new, P2 harvest) |
| `Toolhelp.lib` | ToolHelp set (26 bindings: `CreateToolhelp32Snapshot`, `Process32*`, `Toolhelp32ReadProcessMemory`, …) | documented (new, P2 harvest) |
| `Mgprint.lib` | printing set (14 bindings: `StartDoc`, `EndDoc`, `StartPage`, `AbortDoc`, …) | documented (new, P2 harvest) |
| `Msgque.lib` | GWES message-queue sub-group (4 bindings) | documented (new, P2 harvest) |
| `ceshell.lib` | shell file-change group (24 bindings: `FILECHANGENOTIFY`, `SHChangeNotify*`, `FILECHANGEINFO` CE 6.0 page) | documented (new, P2 harvest) |
| `Msgbox.lib` | `MessageBox` | documented |
| `Ws2.lib` | **all 117 winsock function pages that document a library** | documented |
| `commctrl.lib` | Command Bars/Bands, image lists, `InitCommonControls(Ex)` — 50 bindings | documented |
| `commdlg.lib` | `ChooseColor`, `CommDlgExtendedError`, `PageSetupDlg`, `PrintDlg` | documented |
| `fileopen.lib` | `GetOpenFileName`, `GetSaveFileName` — **CE-specific library split** | documented |
| `dlgmgr.lib` | dialog manager set (18: `CreateDialogIndirectParam`, `EndDialog`, `DefDlgProc`, …) | documented |
| `menu.lib` | menu set (16: `CreateMenu`, `TrackPopupMenu`, …) | documented |
| `clipbd.lib` | clipboard set (14, incl. CE-only `GetClipboardDataAlloc`) | documented |
| `caret.lib` | caret set (12) | documented |
| `kbdui.lib` | keyboard-UI set (8, incl. CE-only `GetAsyncShiftFlags`) | documented |
| `icon.lib` | icon set (10 bindings: `LoadIcon`, `LoadImage`, `DrawIconEx`, `CreateIconIndirect`, …) | documented (P2 harvest: icon support IS documented on CE) |
| `accel.lib` | accelerator set (4) | documented |
| `sbcmn.lib` | scroll-bar set (4) | documented |
| `rectapi.lib` | RECT helpers (11) | documented |
| `winmgr.lib`, `wmgr_c.lib`, `wmbase.lib`, `uibase.lib`, `coreimm.lib` | window-manager sub-groups (3+3+1+2+1) | documented |
| `drawmbar.lib` | `DrawMenuBar` | documented |
| `loadbmp.lib` | `LoadBitmap` | documented |
| `loadimg.lib` | image-load group (1) | documented |
| `msgbeep.lib` | `MessageBeep` | documented |
| `hotkey.lib` | `RegisterHotKey`/`UnregisterHotKey` group | documented |
| `nclient.lib` | `DrawFrameControl` | documented |
| `aygshell.lib` | AYGShell Reference area (88 per-page bindings, P2 harvest) | documented (per-page harvest complete) |
| `ole32.lib`, `oleaut32.lib`, `uuid.lib`, … | COM areas | per-page harvest pending (P2) |

The complete module set SHALL be derived by harvesting the Requirements blocks of the full inventories (`data/mslearn-inventories/`), which is a mechanical extension of `tools/harvest_facts.py` (realised for area harvests as `tools/harvest_area.py`). Functions whose pages document **no** Link Library line (98 in the winuser set, 10 in the GDI set, ~700 macro-only common-control pages) are tracked as binding-hypothesis items (OQ-14) and default to the GWES runtime-module hypothesis. The P2 session added the CE 6.0 kernel-split bindings (`Nkstub.lib`, `Oemmain.lib` above) — nine functions total change import library between CE 5.0 and CE 6.0 documentation, joining `Sleep`.

## 3. `.def` file requirements (normative)

* **R-DEF-1.** One `.def` per documented import library: `coredll.def`, `msgbox.def`, `ws2.def`, `nk.def`, `aygshell.def`, `commctrl.def`, …
* **R-DEF-2.** Export lists contain **documented function names only** (name-based exports). Windows CE exports are name-based in all documentation observed; **ordinal exports MUST NOT be invented**. If an ordinal-only export is ever proven at runtime (OQ-5), it is recorded in the fact DB first, and only then may a `.def` carry an `@ordinal` entry.
* **R-DEF-3.** Each export entry's provenance: at least one documentation page whose Requirements block binds that function to that library. The generated `.def` files MUST be accompanied by a machine-generated sidecar mapping (`export → doc page URL`) so that every line is traceable.
* **R-DEF-4.** A/W: export names are the *actual documented/exported* symbol forms per the A/W policy (`unicode-aw-policy.md` §2) — suffix truth is per-function; the `.def` reflects real symbols, the headers provide the generic aliases.
* **R-DEF-5.** Version scoping: where a function's documented availability differs by CE version ("Windows CE 2.10 and later"), the sidecar records it; the `.def` itself remains a union for the target family (CE 4/5/6), and per-version def variants are generated only if runtime verification proves export absence in specific versions (OQ-6).
* **R-DEF-6.** Format: standard module-definition syntax consumable by GNU `dlltool`/`lib.exe`-class tools:

  ```
  LIBRARY COREDLL.DLL
  EXPORTS
      CreateProcess
      CreateFileW
      ...
  ```

  (Exact symbol casing per documentation/runtime evidence; the `LIBRARY` line records the target DLL name — see OQ-6 for DLL-name confirmation.)

## 4. Generation pipeline (spec for Phase 2 tooling)

```
data/mslearn-inventories/<set>/<area>.json     (page lists)
        │ tools/harvest_facts.py (extended: full Requirements harvest)
        ▼
data/mslearn-facts/<set>-<area>-facts.json     (per-page: header, library, signature, versions)
        │ tools/build_defs.py (to be written in Phase 2)
        ▼
def/<lib>.def  +  def/<lib>.def.map            (sidecar provenance)
        │ dlltool → lib<lib>.a / .lib
        ▼
import libraries
```

The pipeline is fully deterministic and re-runnable; no manual editing steps are permitted without a corresponding fact-DB change.

## 5. Verification

* **Completeness:** every function page in an area's inventory MUST appear in exactly one `.def`'s sidecar (or be explicitly marked `no-library-documented`).
* **Runtime:** on owned CE 4/5/6 devices/emulators, Role C probes `LoadLibrary`/`GetProcAddress` for a sample of exports and records presence/absence — behaviour-only verification per `verification-policy.md` §1.
* **Cross-check:** the resulting import libraries must link a conformance binary per `conformance-testing.md`.

## 6. Explicitly prohibited shortcuts

* Using Platform Builder `.def` files (rejected source R-2) — including "just to check".
* Using export lists scraped from ROM images without documentation cross-check (R-5).
* Copying mingw-w64's Win32 def files (Win64/Win32-desktop scope; charter C-1 — and their def provenance is desktop PE analysis, not CE documentation).
