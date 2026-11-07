# Specification — Telephony, RAS, WNet (`tapi.h`, `ras.h`, `winnetwk.h`)

Status: final (P3 harvest batch) | Priority: P2 | Fact sources: `data/facts/tapi.yaml` (206), `ras.yaml` (35), `wnet.yaml` (16) — 257 records
Harvest basis: TAPI Reference 205+205+204 (three docsets), RAS Reference 35+35+35, Windows Networking API/Redirector Reference 16+16+16 — 795 harvested pages.

## 1. Purpose and scope

The documented CE telephony surface: TAPI 2.x (`tapi.h` — `line*`/`phone*` function set, the huge `LINE*`/`PHONE*` constant families, line-device structures), Remote Access Service (`ras.h` — `RasDial` family, `RASENTRYNAME`), and the Windows Networking / redirector API (`winnetwk.h` — `WNetAddConnection*` family).

CE facts: TAPI binds **coredll.lib** on 91 records (no tapi32 — the CE convention); introduced distribution is bimodal: 1.0 (78 — the `line*` base set documented since CE 1.0) and 3.0 (121 — the TAPI 2.x wave). RAS is 1.0-era (21 records) with a 4.0 wave. WNet is 2.0 (all 16). Three records document `unimodem.h` — the modem SPI user-level bits.

## 2. Dependencies

`windef.h`, `winnt.h`; TAPI needs `winuser.h`-style handle typedefs (but not its messages). RAS posts progress messages via `WM_RASDIALEVENT` (recorded as message record, `winuser.h`-adjacent — see A/W notes).

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Structures | Constants | Notes |
| --- | --- | --- | --- | --- | --- |
| TAPI (`tapi.h`) | 206 | 95 (`lineOpen`, `lineGetCallInfo`, `phoneSetHookSwitch`…) | 28 (LINECALLINFO, LINEDEVCAPS, VARSTRING…) | 64 constant-family pages (`LINEADDRCAPFLAGS`, `LINEBEARERMODE`, `LINECALLFEATURE`, `LINEERR`?, `PHONEBUTTONMODE`…) + 19 family notes | 3 records document `unimodem.h` |
| RAS (`ras.h`) | 35 | 21 (`RasDial`, `RasEnumConnections`…) | 9 (RASDIALPARAMS, RASENTRYNAME…) | 2 constants + 2 enums + 1 message (`WM_RASDIALEVENT`) | `autoras.h` on one record |
| WNet (`winnetwk.h`) | 16 | 11 (`WNetAddConnection*`, `WNetCancelConnection*`…) | 5 (NETRESOURCE family) | — | all introduced 2.0 |

## 4. A/W and export-form notes

TAPI: `lineGetAppPriority`-family are wide (LPCWSTR); no A pages. RAS: `RasDialW`-only semantics (generic resolves W). WNet: `WNetAddConnection2W`-style (the documented CE pages are generic-named; A/W policy applies). `WM_RASDIALEVENT` is a documented message constant whose value is symbolic (lineage channel).

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0300` | the TAPI 2.x wave (121 records) |
| `_WIN32_WCE >= 0x0400` | RAS 4.0 wave (9), TAPI 4.0 additions (4) |
| `_WIN32_WCE >= 0x0100` | TAPI/RAS 1.0-era base |
| per-record | full distribution in the fact YAML |

No CE5→CE6 binding changes; tapi constants show **no numeric values in the CE docs** — see OQ-29.

## 6. Implementation notes for Role B

1. **R-HDR-23**: `tapi.h`, `ras.h`, `winnetwk.h` standalone (desktop-compatible split); `unimodem.h` rides as its own small header; `autoras.h` as shim-level adjunct.
2. **OQ-29**: the 64 TAPI constant families are name-complete but value-open (tapi.h is not in the audited w32api lineage; mingw-w64 has it but reuse is deferred pending per-file license scan — see `docs/02-sources/audits/mingw-w64.md` §4.2). Values MUST NOT be invented; Role C probes on device, or a future per-file-scoped mingw-w64 audit unlocks the Class B channel.
3. TAPI structures use the VARSTRING/dynamic-size idiom — static-assert only the fixed headers (`LINEDEVCAPS` prefix layout).
4. `WM_RASDIALEVENT`: symbolic from lineage; probe list entry.
5. WNet: `NETRESOURCE` layout matches desktop; `WNetOpenEnumW` round-trip documented.

## 7. Closure statement

795 pages → 257 records (three-docset merge; ce40 tapi confirms 4.x continuity of the 3.0 wave). The TSPI (service-provider) Reference (102+102 pages) is deliberately NOT harvested into the application set — it is the driver-side telephony contract; registered in the inventory as excluded-by-area with the same rationale as FSD/GWES-internal. CellCore (675 pages: SMS/SIM/phone-book ext APIs) is a separate CE-only telephony area scheduled for the P4 roadmap.

## 8. Verification hooks

L2: `sizeof(RASDIALPARAMS)`, `LINEDEVCAPS` fixed-prefix layout. L3: `lineInitialize`/`lineShutdown` roundtrip on a telephony image; `RasEnumConnections` on a RAS image; `WNetAddConnection3W` against a share. Role C: TAPI constant-value sweep (OQ-29).
