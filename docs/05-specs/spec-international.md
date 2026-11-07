# Specification — International: NLS, IMM, MUI (`winnls.h`, `imm.h`)

Status: final (P3 harvest batch) | Priority: P1 (NLS is application-common surface) | Fact sources: `data/facts/winnls.yaml` (47), `imm.yaml` (148), `mui.yaml` (5) — 200 records
Harvest basis: National Language Support (NLS) Reference 42+42, Input Method Manager (IMM) Reference 152+152, Multilingual User Interface (MUI) Reference 5+5 — 398 harvested pages.

## 1. Purpose and scope

The documented CE international surface: NLS (`winnls.h` — locale enquiry/conversion, `GetLocaleInfo`, `CompareString`, code-page presence, LCMapString family), the Input Method Manager (`imm.h` — the full IMM/IME application contract incl. its COM interface set `IEnumInputContext`, `IActiveIMM*` and the IME-side function identifiers), and MUI (`muireg`-family loader functions documented under `windows.h`).

Key CE fact: CE NLS binds **coreloc.lib** on 31 records — a CE-specific library with no desktop counterpart (desktop uses kernel32) — recorded per-record; `GetUserDefaultUILanguage`/MUI functions also coreloc.lib.

## 2. Dependencies

`windef.h`, `winnt.h` (`LANGID`, `LCID`, `LCTYPE` typedefs). IMM depends on `winuser.h` (window/message plumbing, `HIMC` handles).

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Interfaces | Structures | Constants/messages | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| NLS (`winnls.h`) | 47 | 36 | — | 3 (CPINFO family) | 8 note-records (family tables) | introduced bulk 4.0; 1.0-era base (`GetACP` family) |
| IMM (`imm.h`) | 148 | 62 | 31 | 12 (COMPOSITIONFORM, CANDIDATEFORM, IMECHARPOSITION…) | 12 messages (`WM_IME_*` via msg records) + `IME_ESC_*`/function identifiers | **coreimm.lib** (55) — CE-specific IMM library; bulk introduced 4.0 |
| MUI | 5 | 5 | — | — | — | `muireg`-style loaders, coreloc.lib |

IMM's 31 interfaces are the documented `IActiveIMMApp`/`IEnumRegisterWord*` set — aggregated from per-method pages.

## 4. A/W and export-form notes

NLS: `GetLocaleInfoW`-only on CE (generic macro → W). `LCMapStringW`, `CompareStringW` — no A exports documented. IMM: all functions wide (`ImmGetCompositionStringW` usage documented); the IMM function-identifier constants (`IDE_…`/`IME_ESC_…` families) are numeric-neutral names (symbolic channel). MUI functions take wide registry paths.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0400` | whole IMM (147 of 148 records) and the NLS 4.0 wave (35) |
| `_WIN32_WCE >= 0x0420` | one IMM addition |
| per-record | NLS base 1.0 |

No CE5→CE6 library changes (coreloc.lib/coreimm.lib stable across docsets).

## 6. Implementation notes for Role B

1. **R-HDR-20**: `winnls.h` and `imm.h` standalone, desktop-compatible split; `imm.h` does not drag `ole2.h` (its interfaces are declared structurally with CINTERFACE-style vtable comments, matching the w32api lineage approach).
2. `LOCALE_*`, `LANG_*`/`SUBLANG_*`, `CT_*`, `LCMAP_*`, `NORM_…`, `CP_…` constants: emit from the w32api lineage channel (verify-runtime statuses recorded); the `LGRPID_*`/`CALID` families likewise.
3. IMM messages: `WM_IME_*` values symbolic from lineage — Role C probe list.
4. `GetLocaleInfo`'s `LCTYPE` OR-combination (`LOCALE_RETURN_NUMBER` etc.) is a documentation remark, not a constant — captured in the record notes.
5. Static-asserts: `sizeof(COMPOSITIONFORM)`, `sizeof(CANDIDATELIST)`.

## 7. Closure statement

398 pages → 200 records. The IMM "Function Identifiers" subarea (60 pages) resolves to the identifier constants + note records (8 NLS family notes retained). The Unicode Script Processor (USP10, 52 pages) is **not** harvested into facts: it is a complex-script component documented separately — registered in the roadmap as a future area (see `header-inventory.md` P4 rows). Locale-specific Support (242 pages) is per-locale content, not API — excluded by scope rule (recorded in the inventory summary).

## 8. Verification hooks

L2: `sizeof` battery; `LOCALE_*` numeric equality vs desktop docs. L3: `GetLocaleInfoW(LOCALE_SDECIMAL)` roundtrip; `ImmCreateContext`/`ImmDestroyContext` pair on a CJK image; MUI `LoadMUILibrary`-family gated probe (coreloc.lib).
