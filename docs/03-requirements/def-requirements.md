# Import Library (`.def`) Requirements

Status: Normative | Governs the future `def/` tree and import-library generation

## 1. Objective

Produce `.def` files (and derived import libraries) equivalent in role to mingw's `lib/*.def` set, but for Windows CE's module layout — without ever touching restricted SDK/PB material.

## 2. Module set (documented)

The documentation's per-function `Requirements → Link Library` field is the authoritative, license-clean source for the function→library mapping. Libraries observed so far in the harvested core set (with per-page evidence in `data/mslearn-facts/`):

| Import library | Observed bindings | Status |
| --- | --- | --- |
| `coredll.lib` | `CreateProcess`, `CreateThread`, `CreateFile`, `ReadFile`, `WriteFile`, `CloseHandle`, `FindFirstFile`, `VirtualAlloc`, `LocalAlloc`, `HeapCreate`, `WaitForSingleObject`, `CreateEvent`, `CreateMutex`, `GetVersionEx`, `GetSystemInfo`, `GetLastError`, `SetLastError`, `Sleep`, `LoadLibrary`, `GetProcAddress`, `GetMessage`, … | documented (CE 5.0 + 6.0 pages) |
| `Nk.lib` | `WaitForMultipleObjects` (both CE 5.0 `aa450987` and CE 6.0 `ee487972` pages) | documented |
| `Msgbox.lib` | `MessageBox` (CE 5.0 `ms911827`, CE 6.0 `ee503608`) | documented |
| `Ws2.lib` | `WSAStartup` (header `Winsock2.h`) and the Winsock Reference area (110 CE6 pages) | documented |
| `aygshell.lib` | AYGShell Reference area (60 pages) | documented at area level; per-page harvest pending (P1) |
| `commctrl.lib`, `commdlg.lib`, `ole32.lib`, `oleaut32.lib`, `uuid.lib`, … | Common Controls / Common Dialogs / COM areas | per-page harvest pending (P1/P2) |

The complete module set SHALL be derived by harvesting the Requirements blocks of the full inventories (`data/mslearn-inventories/`), which is a mechanical extension of `tools/harvest_facts.py`.

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
