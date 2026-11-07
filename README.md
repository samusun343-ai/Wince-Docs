# Wince-Docs — Clean-Room Research & Specification for Windows CE `include`/`def`

**Status:** Phase 0/1/2 — Information collection and specification (this repository's current scope).
**Target platforms:** Windows CE 4.x / 5.0 / 6.0 (information collection additionally covers all releases, CE 1.0 through 6.0 R3).
**Goal:** produce a complete, license-clean, engineering-grade **specification suite and machine-readable fact database** sufficient for a separate implementation role to build a MinGW-class header and import-library set (`include/` + `def/`) for Windows CE application development — *without* the implementer ever having to consult license-restricted or provenance-uncertain material.

This repository intentionally contains **no Microsoft-copyrighted header code and no SDK dumps**. Every fact in it is either:

1. extracted from publicly accessible, official Microsoft documentation (MS Learn / archived MSDN content) and recorded with a source citation and retrieval date, or
2. taken from permissively-licensed open-source material whose license and provenance have been audited (see `docs/02-sources/`), or
3. explicitly marked as an open question with a defined verification method.

## Why this is a specification, not prose

The deliverable is designed to be directly consumable by an implementation role:

* **Normative language** (RFC 2119) throughout `docs/`.
* **Machine-readable fact database** under `data/` (JSON/YAML) with a fixed record schema (`docs/05-specs/spec-template.md`) — every record carries `src[]` provenance that a validator can check.
* **Complete inventories**: the full MS Learn CE 4/5/6 documentation page indexes (23,713 / 22,889 / 6,362 pages) are snapshotted, plus curated per-area API reference inventories that define the *entire* scope of the future header set — nothing is left implicit.
* **Worked full-enumeration specs** for the foundation batch (`windef.h`, `winnt.h` core, `winerror.h` complete with all 571 documented CE system error codes, `winbase.h` core), the P1 application-surface batch (`winuser.h` core, `wingdi.h` core, `winsock2.h` + `ws2spi.h` + `ws2tcpip.h`, `commctrl.h` command surface + `commdlg.h` CE subset), and the **P2 coverage batch** (10 further specs: `winbase.h` file-I/O + OS services, `winreg.h`, `toolhelp.h`, `msgqueue.h`, `notify.h`, `aygshell.h`, `shellapi.h`/`shlobj.h`/`cpl.h`/`newmenu.h`/`console.h`, the full common-controls set incl. `prsht.h`, GWES remainder with the internal-surface exclusion register) — **3,177 machine-checked fact records** behind them.
* **Tooling**: every dataset is regenerable with the scripts under `tools/` (index → inventory → area harvest → table extraction → YAML generation, all scripted); `tools/validate.py` enforces schema and citation integrity.

## Document map

| Path | Content |
| --- | --- |
| `docs/00-charter/` | Project charter, scope, role separation (research/spec vs. implementation vs. verification) |
| `docs/01-methodology/` | Clean-room policy, source admission policy, fact verification policy, licensing decision record |
| `docs/02-sources/` | Approved source registry, per-source license audits, rejected sources with rationale |
| `docs/03-requirements/` | Target environment matrix, Unicode A/W policy, header inventory (full roadmap), `.def` requirements |
| `docs/04-architecture/` | Include tree layout, version gating, `.def` generation, conformance testing strategy |
| `docs/05-specs/` | Per-header specification template + foundation-batch, P1-batch and P2-batch full-enumeration specs (19 spec documents) |
| `docs/06-appendix/` | CE version history, open questions with verification methods |
| `data/` | Documentation indexes, curated API inventories, harvested fact records (**5,032 pages**: 64 core + 1,795 P1 + 3,173 P2), documented constant tables, spec-level fact YAML (**3,177 records**) |
| `tools/` | Regeneration and validation scripts (index → inventory → area harvest → tables → YAML → validate) |

## Key findings so far (Phase 0 + P1 + P2 highlights)

* The **entire Windows CE 5.0 and Windows Embedded CE 6.0 product documentation trees are still live on Microsoft Learn** under `previous-versions/windows/embedded/` (CE 6.0: 23,713 pages; CE 5.0: 22,889; Windows CE .NET 4.x: 6,362) — confirmed by walking the official TOC JSON. This is the primary clean fact source. (`data/mslearn-doc-index/`, audit `docs/02-sources/audits/mslearn-wince.md`)
* The complete documented **CE 6.0 system error table (571 codes, 0–6118)** and **Winsock error table (35 codes, 10004–10101)** were extracted from the official docs; the system table differs CE5→CE6 only by `ERROR_DEVICE_REMOVED`; the winsock table is identical in both. (`data/mslearn-facts/`)
* **The documented import-library surface is heavily fragmented — 26 libraries so far** (P1 area harvest, 1,795 pages): beyond `coredll.lib` / `Ws2.lib` / `Msgbox.lib` / `Nk.lib`, the GWES pages bind functions to `menu.lib`, `dlgmgr.lib`, `clipbd.lib`, `caret.lib`, `kbdui.lib`, `icon.lib`, `accel.lib`, `sbcmn.lib`, `rectapi.lib`, `winmgr.lib`, `wmgr_c.lib`, `wmbase.lib`, `uibase.lib`, `coreimm.lib`, `drawmbar.lib`, `loadbmp.lib`, `loadimg.lib`, `msgbeep.lib`, `hotkey.lib`, `nclient.lib`, `commctrl.lib`, `commdlg.lib`, and `fileopen.lib` (the file-dialog split). At P1 closure only `Sleep`'s `Nkstub.lib` was a core-set CE5→CE6 change — the P2 findings below add nine more. (`docs/03-requirements/def-requirements.md` §2)
* **CE-only API surface documented and enumerated**: Command Bars/Bands (24 functions, `commctrl.lib`), the keyboard set incl. `pwinuser.h`-documented functions (`GetForegroundInfo`, `PostKeybdMessage`, `AllKeys`, …), `GetClipboardDataAlloc`, `GetMessageSource`, `CustomTrackPopupMenu` (CE 6.0 only), IrDA socket level `SOL_IRLMP`, and the CE-only window styles (`WS_EX_CAPTIONOKBTN`, `WS_EX_NODRAG`, `WS_EX_NOANIMATION`, `WS_NONAVDONEBUTTON`). (`docs/05-specs/spec-winuser-core.md`, `spec-commctrl-ce.md`)
* **CE-documented structure deltas**: `DRAWITEMSTRUCT.itemData` is `ULONG_PTR` while `MEASUREITEMSTRUCT.itemData` is `DWORD` and `DELETEITEMSTRUCT.itemData` is `UINT`; `WNDCLASS.hInstance` is `HANDLE`; `MENUITEMINFO.dwTypeData` is `LPTSTR` (wide at export). (spec §5.1 tables)
* **Documentation quirks recorded as facts**: CE 5.0 "List View Styles" page typo `LVS_EX_NOFOSUCRECT` (headers must define the correct `LVS_EX_NOFOCUSRECT` only); `WS_OVERLAPPEDWINDOW` documented as unsupported (compose-from-parts remark); `WSAAsyncSelect` has no CE page (`WSAEventSelect` is the documented async model); the CE 6.0 TOC hides the Keyboard Reference node the CE 5.0 tree exposes.
* CeGCC (which this project deliberately is *not* a fork of) itself **borrowed its headers from the MinGW project's w32api module** — public-domain licensed with audited exceptions. That lineage is adopted here as the value cross-check channel (facts only) and as the sole code-reuse candidate for the implementation phase. (`docs/02-sources/audits/cegcc.md`, `docs/02-sources/audits/mingw-org-w32api.md`)
* **Windows CE Shared Source** and all Platform Builder / SDK header material are **rejected as information sources** (license-restricted, per project constraints).

### P2 session findings (3,173-page coverage expansion)

* **The documented import-library map grew to 34 libraries.** New documented bindings: `Serdev.lib` (whole serial-communications set, 32 pages), `Toolhelp.lib` (ToolHelp), `Mgprint.lib` (CE printing subset of GDI: `StartDoc`/`EndDoc`/`StartPage`/`AbortDoc`…), `Coreloc.lib` (`LoadDriver` + locale), `Coremain.lib`, `Oemmain.lib` (`GetTickCount`/`IsProcessorFeaturePresent`/`WriteDebugLED` on CE 6.0 pages), `Msgque.lib`, `ceshell.lib` (shell file-change group), per-page `aygshell.lib` (88), and an expanded `Icon.lib` set (10).
* **Nine more CE5→CE6 import-library migrations to `Nkstub.lib`** beyond `Sleep`: the five core registry functions (`RegCloseKey`, `RegCreateKeyEx`, `RegFlushKey`, `RegOpenKeyEx`, `RegQueryValueEx`) and three time conversions (`CompareFileTime`, `FileTimeToSystemTime`, `SystemTimeToFileTime`) — the CE 6.0 kernel-split is now visible as a systematic pattern, recorded per-record in the fact DB.
* **CE 6.0-only documented API set enumerated**: `VirtualAllocEx`/`VirtualFreeEx`/`VirtualProtectEx`/`VirtualQueryEx`/`VirtualCopyEx`/`VirtualSetAttributesEx`/`VirtualAllocCopyEx`, `OpenThread`, `CeRemoteHeapCreate`/`CeRemoteHeapTranslatePointer`, `CeZeroPointer`, `CeGetRawTime(Offset)`, `CeSetProcessVersion`, vectored exception handlers, `CheckRemoteDebuggerPresent`/`IsDebuggerPresent`/`DebugActiveProcessStop`, `KernelIoControl`, `GetDeviceUniqueID`, `ReadMsgQueueEx`, `CeRegGetInfo`/`CeRegGetNotificationInfo`, `UDM_SETPOS32`/`UDM_GETPOS32`, the `newmenu.h` and `console.h` sets.
* **CE-native real-time thread model documented as primary**: `CeSetThreadPriority`/`CeGetThreadPriority` (0–255), `CeSetThreadQuantum`/`CeGetThreadQuantum`, `CeGetCallerTrust` — alongside the w32-style compatibility layer.
* **Icon support IS documented on CE** (resolves a long-standing uncertainty): `LoadIcon`, `LoadImage`, `CreateIconIndirect`, `DestroyIcon`, `DrawIconEx`, `GetIconInfo`, `ExtractIconEx` with `Icon.lib` — plus `WM_HIBERNATE` (0x3FF, CE-only low-memory broadcast) and `WM_IM_INFO` (value open, OQ-28).
* **The GWES internal C++ surface (GWES OS Reference, 270 pages) is harvested and registered as an explicit exclusion register** (`internal-excluded.yaml`, 448 records: `*View_t::` classes, `Gdi::*_I` thunk bypass, `CeNotifyPrivate_*`, RC-grammar statements, `oomui.h`) — the closure rule now has documented evidence for every excluded page, and OQ-27 records the observation that GWES internally implements region/alpha primitives (`Gdi::CombineRgn_I`) that the public GDI pages omit.
* **Documented headers that are not classic Win32 headers**: `pwinreg.h` (multi-user registry), `kfuncs.h`/`pkfuncs.h` (kernel surface basics), `dbgapi.h` (debug macros), `windbase.h` (object-store/password), `extfile.h` (`FILECHANGEINFO`), `newmenu.h`, `console.h` — each mapped to a project header + compatibility shim decision (R-HDR-10 … R-HDR-17).
* **Fibers ARE documented** on CE 5.0/6.0 (`CreateFiber`/`SwitchToFiber`/`DeleteFiber`/`ConvertThreadToFiber`), as is the full serial-communications set and the debug-event loop (`WaitForDebugEvent`/`ContinueDebugEvent` + `DEBUG_EVENT` family).

## Repository layout

```
Wince-Docs/
├── README.md                  <- you are here
├── docs/
│   ├── 00-charter/  01-methodology/  02-sources/
│   ├── 03-requirements/  04-architecture/
│   ├── 05-specs/  06-appendix/
├── data/
│   ├── mslearn-doc-index/     <- full page indexes (gzip snapshots + stats)
│   ├── mslearn-inventories/   <- curated per-area API reference inventories
│   ├── mslearn-facts/         <- harvested per-page fact records + error tables
│   └── facts/                 <- spec-level enumerated facts (YAML)
└── tools/                     <- regeneration + validation scripts
```

## Regenerating the data

```sh
# 1. download the MS Learn embedded TOC (single JSON, ~12 MB)
curl -s "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/toc.json" -o /tmp/embedded-root-toc.json
# 2. extract the per-version page indexes
python3 tools/extract_mslearn_index.py
# 3. build the curated inventories
python3 tools/build_inventories.py
# 4. harvest the fact records (core subset + full areas; see data/README.md for the area commands)
python3 tools/harvest_facts.py
python3 tools/harvest_area.py ce60:window-control ce50:window-control
# 5. extract documented constant/error tables and generate the spec-level YAML
python3 tools/extract_style_tables.py && python3 tools/extract_flag_tables.py
python3 tools/extract_winsock_errors.py
python3 tools/gen_area_yaml.py
# 6. validate everything
python3 tools/validate.py
```

## License / rights posture

* **`docs/` is CC-BY-4.0; `data/` and `tools/` are MIT.** The split, rationale and re-user obligations are recorded in [`docs/01-methodology/licensing.md`](docs/01-methodology/licensing.md); full texts live under [`LICENSES/`](LICENSES/) and the root [`LICENSE`](LICENSE) states the scheme.
* Data under `data/` consists of **factual extractions** (identifiers, numeric values, signatures, requirement mappings) from the sources cited in each record, with attribution. Prose is excerpted only in short, attributed fragments for technical necessity.
* No Microsoft-copyrighted source code is included. See `docs/01-methodology/source-policy.md` for the rules that guarantee this.
