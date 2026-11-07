# Specification — Multimedia audio and fonts (`mmsystem.h`, fonts surface)

Status: final (P3 harvest batch) | Priority: P2 | Fact sources: `data/facts/mmedia.yaml` (99), `fonts.yaml` (50) — 149 records
Harvest basis: Waveform Audio Reference 72+62 (incl. mixer), Fonts Reference 50+32+27 — 243 harvested pages.

## 1. Purpose and scope

The documented CE audio application surface (`mmsystem.h` — waveform in/out, audio mixer, and the CE-specific gain-control messages) and the fonts application surface beyond `wingdi.h` core (font enumeration/enquiry functions documented under the Fonts area, plus the driver-DDI font subset).

CE facts: audio binds **coredll.lib** (53 records — no winmm on CE); `wfmtmidi.h` (5 records) and `audiosys.h` (3) are CE-specific audio headers. The CE waveform set adds gain-control messages desktop lacks: `MM_WOM_ATTENUATED`, `MM_WOM_FORCESPEAKER`, `MM_WOM_SETSECONDARYGAINCLASS`, `MM_WOM_SETSECONDARYGAINLIMIT` — ce-only message records.

## 2. Dependencies

`windef.h`, `winnt.h`; `windows.h` for message plumbing; `spec-wingdi-core.md` owns the base font/text functions.

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Structures | Messages/constants | Notes |
| --- | --- | --- | --- | --- | --- |
| Waveform audio (`mmsystem.h`) | 91 | 58 (`waveOutOpen`, `waveInOpen`, mixer `mixerOpen`…) | 16 (WAVEFORMATEX, WAVEHDR, MIXERLINE…) | 12 messages (`MM_WIM_*`, `MM_WOM_*`, `MM_MIXM_*`) | 6 constants incl. `WAVE_MAPPER` |
| CE audio extras | — | — | — | 4 ce-only gain messages (above) | `wfmtmidi.h` (5), `audiosys.h` (3) |
| Fonts (app surface) | 50 | 35 | 14 | 1 message | documented headers: `windows.h` (24), `wingdi.h` (8) |
| Fonts (driver DDI) | subset | — | — | — | `fontdrv.h` (7), `winddif.h` (5), `winddi.h` (5) — **driver-DDI, excluded from app headers (R-HDR-26)** |

Introduced: audio bulk 2.0/2.1 (Pocket PC-era audio), a 5.0/6.0 wave (15 records — mixer and gain control); fonts peak 1.0 (17) and 6.0 (18 — the 6.0 font-doc reorganization).

## 4. A/W and export-form notes

`mmsystem.h` on CE is the classic window-message callback model (`waveOutProc`); no A/W dimension (binary audio buffers, wide device names via `WAVEOUTCAPS`-family? — caps structs carry wide product names; recorded in struct definitions). Font functions: `EnumFontFamiliesW`-only semantics.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0500` | mixer set + gain messages (7), 5.0 fonts wave (5) |
| `_WIN32_WCE >= 0x0600` | 6.0 audio records (8), 6.0 fonts records (18) |
| `_WIN32_WCE >= 0x0200` | waveform base |
| runtime SYSGEN | audio/mixer components optional on headless images |

## 6. Implementation notes for Role B

1. **R-HDR-26**: `mmsystem.h` standalone (desktop-compatible); `wfmtmidi.h`, `audiosys.h` ride as CE-only audio adjuncts. Font **application** functions declared in `wingdi.h` (the docs' `windows.h` references are the umbrella convention); `fontdrv.h`/`winddi.h`/`winddif.h` are driver-DDI — excluded from the application include set, records retained (same policy as `bt_ddi.h`).
2. `WAVE_FORMAT_*`/`WHDR_*`/`MOD_*`/`SND_*` constants: mmsystem.h is in the audited w32api lineage — verified/symbolic channels per-record.
3. The 4 gain-control messages are **ce-only with no desktop value** — value-open (probe list; never invent).
4. Static-asserts: `sizeof(WAVEFORMATEX) == 18`, `sizeof(WAVEHDR)`, `sizeof(MIXERLINE)`.
5. Driver-message pages (Waveform Output/Input Driver Messages, 21+13) are the WDDM-side contract — NOT harvested into mmedia (excluded by area, like TSPI).

## 7. Closure statement

243 pages → 149 records. Exclusions: driver-message subsets and font DDI (recorded rationale); `Hardware Audio Mixer Reference` app pages are merged (the mixer function/struct records above). MIDI/aux/joystick/timer MCI surfaces have **no CE documentation pages** — the CE audio model is waveform+mixer only; do not emit desktop MCI/aux/joy APIs (absence is the documented fact).

## 8. Verification hooks

L2: struct-size battery; `WAVE_MAPPER` value. L3: `waveOutOpen`/`waveOutWrite`/`waveOutClose` sine roundtrip; `mixerGetLineInfo` on a mixer image; gain-message emission path. Role C: gain-message value sweep.
