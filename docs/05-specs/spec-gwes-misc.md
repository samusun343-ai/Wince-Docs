# Specification — GWES remainder: resources, printing, system info + internal-surface exclusion register

Status: final (P2 harvest batch) | Priority: P1 | Fact sources: `data/facts/winuser-gwes.yaml` (62), `data/facts/wingdi-print.yaml` (11), `data/facts/internal-excluded.yaml` (448)
Harvest basis: GWES remainder subareas — Message Queue Reference (dupes, skipped), Message Synchronization (2+2), System Information Reference (dupes, skipped), Resources Reference (re-harvest; icon/resource function pages kept), Resource-Definition Statements (51, ce50 tree; note-kind), Printing Reference (8+8), Startup User Interface (6, ce60), Out of Memory UI (12, ce60), Interprocess Communication (3+3), GWES OS Reference (270, ce60 — internal), Notification Reference (23, ce60 — internal), Notifext.hxx/oomui.hpp/menuview.hpp/nclientview.hpp/gwebypasscoredllthunk.hpp pages — 546 pages total.

## 1. Purpose and scope

Three things at once: (a) the `winuser.h` resource/icon surface re-harvested through the CE 6.0 tree (creating the definitive icon-function list), (b) the CE printing subset of `wingdi.h` (**Mgprint.lib**), and (c) the **explicit exclusion register** for the GWES internal C++ implementation documentation (GWES OS Reference: `ButtonView_t::`, `EditView_t::`, `Gdi::*_I`, `gwebypasscoredllthunk.hpp`, …) — required by the closure rule so the implementation role never mistakes OEM-internal surface for application API.

## 2. Dependencies

`winuser.h`, `wingdi.h`, `winreg.h` (startup UI reads registry).

## 3. Enumeration

### 3.1 Resources / icons (winuser-gwes.yaml, 62 records)

The icon set IS documented on CE (resolves the P1 open question on icon support): `LoadIcon`, `LoadImage`, `CreateIconIndirect`, `DestroyIcon`, `DrawIconEx`, `GetIconInfo` (Winuser.h; **Icon.lib** binding on 10 records), `ExtractIconEx` (Shellapi.h, Icon.lib), plus `FindResource`/`LoadResource`/`LockResource`/`SizeofResource`/`MAKEINTRESOURCE` (Winbase.h/Winuser.h). Messages: `WM_COPYDATA`, `WM_GETFONT`/`WM_SETFONT`, `WM_HELP`, `WM_KEYFIRST`/`WM_KEYLAST`, **`WM_HIBERNATE`** (0x3FF, ce-only low-memory broadcast), **`WM_IM_INFO`** (ce-only, value open). The remaining 52 records are note-kind: the resource-**script statement** pages (ACCELERATORS, BITMAP, CAPTION, CLASS, CONTROL, CTEXT, … — the RC grammar), recorded as documentation affecting the future resource-compiler tooling, not `include/`.

### 3.2 Printing (wingdi-print.yaml, 11 records, **Mgprint.lib**)

`StartDoc`/`EndDoc`/`StartPage`/`EndPage`/`AbortDoc`/`SetAbortProc`/`AbortProc` (+ `DOCINFO`) — documented "Windows CE 2.0 and later", binding **Mgprint.lib** on both docsets. Also captured in this area: `TranslateCharsetInfo` (+ `CHARSETINFO`, `FONTSIGNATURE`, coredll.lib, "OEM code pages are not supported") — the NLS-adjacent GDI helper. CE printing notes recorded per page: "Windows Embedded CE does not support printing to files"; DC attribute persistence differs for CE 1.0–2.01.

### 3.3 Internal/OEM surface (internal-excluded.yaml, 448 records — the exclusion register)

| Group | Records | Reason for exclusion |
| --- | --- | --- |
| GWES OS Reference C++ view classes (`ButtonView_t::*`, `CacheView_t::*`, `ComboBoxView_t::*`, `CommCtrlView_t::*`, `EditView_t::*`, …) | ~270 | GWES internal implementation classes (OEM GWES source); not exported application API |
| `Gdi::*_I` thunk bypass family (gwebypasscoredllthunk.hpp) | ~60 | internal GWES→GDI thunk layer |
| `CeNotifyPrivate_*` / `CeNotifyPublic_*` (Notifext.hxx, Notification Reference) | ~44 | notification broker internals |
| Resource-Definition Statements (RC grammar pages) | ~51 | resource-compiler grammar, not header content (tooling note only) |
| `oomui.h` OOM UI reference | 12 | OEM out-of-memory UI customization |
| Startup UI / remaining `(none)`-requirement pages | ~11 | OEM startup screen documentation |

Recorded evidence kept for Phase-2 decisions (examples): `Gdi::AlphaBlend_I`, `Gdi::CombineRgn_I`, `Gdi::CreateRectRgn_I` — the GWES internal layer *implements* region/alpha primitives even though the public GDI pages do not document the public exports; this informs OQ-27 (whether any CE image exports `CombineRgn` despite no public doc page) but does NOT license declaring them.

## 4. A/W and export-form notes

Wide-only throughout; `DrawIconEx`/`LoadImage` generic forms only.

## 5. Version gates

Printing set: `_WIN32_WCE >= 0x0200`. `WM_HIBERNATE`: documented 1.0+ (value from lineage). No CE5→CE6 binding changes (Mgprint.lib/Icon.lib stable).

## 6. Implementation notes for Role B

1. The icon functions are declared in `winuser.h` (Winuser.h-documented) and `shellapi.h` (`ExtractIconEx`); `Icon.lib` bindings go to the `.def` sidecar.
2. `WM_HIBERNATE` = 0x3FF (lineage value, ce-only): define unconditionally in the CE header set; document the object-store hibernate contract.
3. `WM_IM_INFO`: reserve the name with no value (OQ-28) — do not invent.
4. The exclusion register is normative: nothing in `internal-excluded.yaml` may appear in `include/` or any `.def`.
5. RC-grammar note records: consumed by the future resource-compiler spec (`docs/04-architecture/` P2 tooling note), not by headers.

## 7. Closure statement

546 harvested pages → 62 + 11 + 448 records + 191 cross-file skips (Resources/SysInfo/Message Queue pages already in `winuser-core.yaml` from the P1 GWES harvest). With this spec the GWES documentation tree is fully closed except the Printing/Startup/OOM/Notify pages itemized above. No page of the harvest is unrepresented.

## 8. Verification hooks

L2: `sizeof(DOCINFO)`, `WM_HIBERNATE` value assert. L3: `LoadIcon`/`DrawIconEx` roundtrip (Icon.lib linkage); `StartDoc`+`EndDoc` on a print-image CE build; `WM_HIBERNATE` received after triggering a low-memory simulation on CEPC.
