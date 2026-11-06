# Specification — `wingdi.h` (core set)

Status: final (Phase 1 core set) | Priority: P1 | Fact source: `data/facts/wingdi-core.yaml` (176 records), page records `data/mslearn-facts/ce50-ce60-gdi-facts.json` (344 pages), raster-op tables in `ce-style-tables.json`

## 1. Purpose and scope

The GDI drawing surface documented by the CE GWES "GDI Reference": bitmaps, brushes, pens, fonts, text, regions, clipping, palettes, raster operations, the imaging extension (`AlphaBlend`, `GradientFill`, `TransparentBlt`), and display-mode queries. 123 function records, 29 structure/type records, 48 documented binary raster-op names, 5 documented GDI messages.

## 2. Dependencies

`windef.h`, `winnt.h`; interplays with `winuser.h` for the paint cycle (`BeginPaint`/`EndPaint`/`InvalidateRect`/`GetDC` etc. are documented under the GDI area but are window-management functions — those 16 records are routed to `winuser-core.yaml` per the project header map; the docs' header lines (`windows.h`) are preserved in the record notes).

## 3. Documented import-library map

| Library | Fn count | Representative functions |
| --- | --- | --- |
| `coredll.lib` | 100 | `BitBlt`, `CreateCompatibleDC`, `CreateFontIndirect`, `AlphaBlend`, `GradientFill`, `TransparentBlt`, `GetDeviceCaps`, `EnumDisplayDevices`, `ChangeDisplaySettingsEx`, `SetStretchBltMode`, … |
| `rectapi.lib` | 11 | `CopyRect`, `EqualRect`, `InflateRect`, `IntersectRect`, `IsRectEmpty`, `OffsetRect`, `PtInRect`, `SetRect`, `SubtractRect`, `UnionRect` (RECT helpers) |
| *(none documented)* | 10 | e.g. `CreateDIBSection` page carries no Link Library line |
| `nclient.lib` | 1 | `DrawFrameControl` |
| `loadbmp.lib` | 1 | `LoadBitmap` |

CE 5.0 → CE 6.0: **zero real binding changes** (only the case normalisation `Coredll.lib` → `coredll.lib`). All documented headers are the umbrella `windows.h` (104 records) or `winuser.h` (15) — the project's canonical `wingdi.h` split is a design decision (R-HDR); the documented header is preserved in every record's notes.

## 4. Functions (complete harvested set: 123 records)

Every record carries the verbatim documented signature. Groups and notable entries:

* **Object creation/selection**: `CreateBitmap`, `CreateCompatibleBitmap`, `CreateDIBSection`, `CreatePen`, `CreateSolidBrush`, `CreatePatternBrush`, `CreateDIBPatternBrushPt` (CE spelling of the desktop `CreateDIBPatternBrush` family — point-based form only), `CreatePalette`, `CreateFontIndirect`, `SelectObject`, `DeleteObject`, `GetObject`.
* **Drawing**: `SetPixel(V)`, `LineTo`, `MoveToEx`, `Rectangle`, `Ellipse`, `Polygon`, `PolyPolygon`, `Polyline`, `RoundRect`, `FillRect`, `FrameRect`, `InvertRect`, `DrawText`, `ExtTextOut`, `TextOut`, `GrayString`.
* **Blitting and raster**: `BitBlt`, `StretchBlt`, `PatBlt`, `MaskBlt`, `PlgBlt`, `TransparentBlt`, `AlphaBlend`, `GradientFill`, `SetStretchBltMode`, `GetStretchBltMode`, `SetROP2`, `GetROP2`, `StretchDIBits`, `SetDIBitsToDevice`.
* **Imaging (CE extension set)**: `AlphaBlend`, `GradientFill`, `TransparentBlt` — documented with `imgrender`-family semantics; these are the Windows CE 3.0+ imaging additions shared with later Windows mobile platforms.
* **Display**: `GetDeviceCaps`, `EnumDisplayDevices`, `ChangeDisplaySettingsEx`, `EnumDisplaySettings`?, `SetWindowRgn` (window-routing note: documented under GDI area; project header winuser per desktop family — note in record).
* **Coordinate/mapping**: `SetMapMode`, `GetMapMode`, `DPtoLP`, `LPtoDP`, `SetViewportOrgEx`, `SetWindowOrgEx`, `GetClipBox`, `SelectClipRgn`, `IntersectClipRgn`, `OffsetClipRgn`, `ExcludeClipRect`.
* **Palettes**: `SelectPalette`, `RealizePalette`, `GetNearestPaletteIndex`, `GetSystemPaletteEntries`-family as documented.
* **Fonts/text metrics**: `GetTextMetrics`, `GetTextExtentExPoint`, `GetCharWidth(32)`, `EnumFontFamilies`, `AddFontResource`, `RemoveFontResource`, `CreateFontIndirect`.
* **Regions**: `CombineRgn`, `CreateRectRgn(Indirect)`, `CreateRoundRectRgn`, `CreateEllipticRgn`, `CreatePolygonRgn`, `OffsetRgn`, `GetRgnBox`, `PtInRegion`, `RectInRegion`.

## 5. Structures (documented layouts)

`BITMAP`, `BITMAPINFOHEADER`, `BITMAPINFO`, `RGBQUAD`, `LOGBRUSH`, `LOGPEN`, `LOGFONT`, `TEXTMETRIC`, `PALETTEENTRY`, `LOGPALETTE`, `POINT`, `POINTFX`?, `SIZE`, `RECT`, `XFORM`, `PIXELFORMATDESCRIPTOR`?, `GCPARAMS`? — complete verbatim layouts in the YAML (`kind: structure`); all documented generic (`windows.h` umbrella). CE deltas observed: `LOGFONT` documented with the desktop-member set (lfFaceName size 32 → `LF_FACESIZE`); `TEXTMETRIC` documented without desktop-only printing members (tmDigitizedAspectX/Y present; verify at P2 detail pass).

## 6. Raster operations (documented name sets)

* **Binary (R2_*, 48 names)**: documented with boolean expressions (`R2_COPYPEN = P`, `R2_MASKPEN = DPa`, …) — the CE pages state the *name and boolean form*, not the numeric index; numeric values (R2_BLACK=1 … R2_WHITE=16) come from the w32api lineage (`verify-runtime`), e.g. `R2_BLACK 1`, `R2_NOTMERGEPEN 2`, `R2_MASKNOTPEN 3`, `R2_NOTCOPYPEN 4`, `R2_MASKPENNOT 5`, `R2_NOT 6`, `R2_XORPEN 7`, `R2_NOTMASKPEN 8`, `R2_MASKPEN 9`, `R2_NOTXORPEN 10`, `R2_NOP 11`, `R2_MERGENOTPEN 12`, `R2_COPYPEN 13`, `R2_MERGEPENNOT 14`, `R2_MERGEPEN 15`, `R2_WHITE 16`.
* **Ternary (ROP codes)**: the Ternary Raster Operations page (276 table rows) uses a name|hex layout not captured by the table extractor (P2: extend `extract_flag_tables.py` for the `<dt><strong>NAME</strong></dt><dt>0x…</dt>` pattern — the same pattern as the desktop extended-styles pages); the common subset (`SRCCOPY 0x00CC0020`, `SRCPAINT 0x00EE0086`, `SRCAND 0x008800C6`, `SRCINVERT 0x00660046`, `SRCERASE 0x00440328`, `NOTSRCCOPY 0x00330008`, `NOTSRCERASE 0x001100A6`, `MERGECOPY 0x00C000CA`, `MERGEPAINT 0x00BB0226`, `PATCOPY 0x00F00021`, `PATPAINT 0x00FB0A09`, `PATINVERT 0x005A0049`, `DSTINVERT 0x00550009`, `BLACKNESS 0x00000042`, `WHITENESS 0x00FF0062`) carries w32api-lineage values recorded `verify-runtime` in the YAML.

## 7. GDI messages

`WM_PAINT`, `WM_SETREDRAW`, `WM_SYSCOLORCHANGE`, `WM_PALETTECHANGED`, `WM_QUERYNEWPALETTE` — documented as pages in the GDI area; message records live in `winuser-core.yaml` family table (§5.3 of that spec).

## 8. A/W and export-form notes

Generic documented names (`GetTextExtentExPoint` etc.), wide-only platform (R-AW-4). Font enumeration callbacks (`FONTENUMPROC`) take generic `LOGFONT*`/`ENUMLOGFONT*` — CE documents the plain `LOGFONT` form; `ENUMLOGFONTEX`-family not documented (P2 gap). `CreateDC` is documented via `CreateDCW`-style page title ("CreateDC (GDI)") with generic signature — export-form confirmation at Role C (OQ-2).

## 9. Open items forwarded

* OQ-17 *(new)*: ternary-ROP table extraction (extractor pattern extension) and value cross-check.
* OQ-18 *(new)*: `TEXTMETRIC`/`LOGFONT` member-level CE deltas (documented pages exist; detailed diff against desktop at P2).
