# Specification — `toolhelp.h`

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/toolhelp.yaml` (16 records)
Harvest basis: ToolHelp Reference — 18+18 pages.

## 1. Purpose and scope

The CE ToolHelp snapshot API: process/thread/module/heap walking and cross-process memory read. This is the CE-specific diagnostics surface used by task managers and debuggers; on CE it replaces several desktop PSAPI/Diagnostics functions that do not exist.

## 2. Dependencies

`windef.h`, `winnt.h` (`HANDLE`, `DWORD`). No GWES dependency (usable from console/services processes on CE 6.0 images that include the console).

## 3. Enumeration (complete)

| Item | Kind | Introduced | Lib | Notes |
| --- | --- | --- | --- | --- |
| `CreateToolhelp32Snapshot` | function | 2.0 | **Toolhelp.lib** | documented signature: `HANDLE WINAPI CreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID)` |
| `CloseToolhelp32Snapshot` | function | 2.0 | Toolhelp.lib | **ce-only counterpart of a desktop-free surface** — CE requires explicit close of the snapshot |
| `Process32First` / `Process32Next` | function | 2.0 | Toolhelp.lib | fill `PROCESSENTRY32` |
| `Thread32First` / `Thread32Next` | function | 2.0 | Toolhelp.lib | fill `THREADENTRY32` |
| `Module32First` / `Module32Next` | function | 2.0 | Toolhelp.lib | fill `MODULEENTRY32` |
| `Heap32ListFirst`? — not present; `Heap32ListNext` / `Heap32Next` | function | 2.0 | Toolhelp.lib | heap walking pair; list-open via `CreateToolhelp32Snapshot(TH32CS_SNAPHEAPLIST)` + `Heap32ListFirst` page routed from the winbase harvest (see closure §7) |
| `Toolhelp32ReadProcessMemory` | function | 2.0 | Toolhelp.lib | **ce-only** cross-process read (desktop uses `ReadProcessMemory`; the CE page documents the toolhelp form) |
| `PROCESSENTRY32`, `THREADENTRY32`, `MODULEENTRY32`, `HEAPENTRY32`, `HEAPLIST32` | structure | 1.0 | — | documented notes: "All strings are Unicode" (PROCESSENTRY32); "Windows Embedded CE does not support movable blocks" (HEAPENTRY32) |

## 4. A/W and export-form notes

Unicode-only struct strings (documented). No A/W function pairs.

## 5. Version gates

Introduced 2.0 across the API per the documented OS Versions fields (the CE 1.0–1.01 predecessor names `Toolhelp32CreateSnapshot`/`Toolhelp32ReadProcessMemory` spellings are historical; the docs document the modern names — see open-questions OQ-22).

## 6. Implementation notes for Role B

1. Header name follows desktop convention `tlhelp32.h` vs the CE-documented `Tlhelp32.h` — **R-HDR-12: the project ships `tlhelp32.h`** (lowercase) as the canonical name with case-insensitive include compatibility; the fact records preserve the documented casing.
2. `TH32CS_*` flag values and `MAX_MODULE_NAME32` / `HF32_*` constants: values from the public-domain w32api `tlhelp32.h` (Class B, `verify-runtime` — the CE pages document names, not values).
3. `.def` binding: **toolhelp.lib** (documented on every function page) — a distinct import library from coredll for this family.

## 7. Closure statement

18+18 pages harvested; 16 records after docset merge (the two subarea index pages produce no records). `Heap32ListFirst` appears in the winbase harvest routing (documented winbase.h header on its page) — cross-referenced here; its fact record lives in `winbase-os.yaml`. Remaining ToolHelp pages: none.

## 8. Verification hooks

L2: `sizeof(PROCESSENTRY32)` against documented member widths (wide `szExeFile[MAX_PATH]`). L3: snapshot → `Process32First`/`Next` enumerates self; `Toolhelp32ReadProcessMemory` reads a known pattern from a launched child on CE 5.0 and CE 6.0.
