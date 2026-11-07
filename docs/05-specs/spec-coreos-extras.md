# Specification — Core-OS extras: CeLog, State Broker, NAT, Kernel Marshaling, Kernel reference, Power

Status: final (P3 harvest batch) | Priority: P2 | Fact sources: `data/facts/celog.yaml` (77), `statebroker.yaml` (17), `nat.yaml` (20), `marshal.yaml` (10), `kernel-ref.yaml` (102), `power.yaml` (30) — 256 records
Harvest basis: CeLog Event Tracking Reference 73+66, State and Notifications Broker (CE 6.0) 17, Network Address Translation Reference 20+20, Kernel Buffer Marshaling (CE 6.0) 10, Kernel Reference 102+84, Power Management Reference 29+29 — 460 harvested pages.

## 1. Purpose and scope

The remaining documented Core-OS and kernel/power surfaces: CeLog event tracking (`celog.h` — the instrumentation structures `CEL_*` and `LogPageInfo`-family functions), the State and Notifications Broker (`regext.h` — `RegistryGetDWORD`/`GetString`, `RegistryNotify*`, `NOTIFICATIONCONDITION`, `REG_COMPARISONTYPE` enum; documented binding **aygshell.lib** on CE 6.0), NAT helper (`nat.h`), kernel buffer marshaling (CE 6.0 `marshal.h` — `MarshalStore*` family), the kernel reference surface (`pkfuncs.h` 71, `nkintr.h` 10, `profiler.h` 7 records — kernel/OAL contract), and the power-management API (`pwinbase.h`: `GetSystemPowerState`, `SetSystemPowerState`, `GetSystemPowerStatusEx(2)`; `pm.h` records).

## 2. Dependencies

`windef.h`, `winnt.h`; state broker builds on `winreg.h` (`spec-winreg.md`); power on `winbase.h` conventions (`spec-winbase-os.md`).

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Structures | Constants/enums | Lib | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| CeLog (`celog.h`) | 77 | 7 (`LogPageInfo`? family) | 65 (`CEL_*` zone/header structs) | 1 enum | coredll.lib (6) | ce-only; 3.0-era (54) |
| State Broker (`regext.h`) | 17 | 13 (`RegistryGetDWORD`, `RegistryNotifyApp`, `RegistryBatchNotification`…) | 2 (`NOTIFICATIONCONDITION`, `NOTIFYMSGQUEUEPACKET`) | `REG_COMPARISONTYPE` enum | **aygshell.lib (13)** | ce-only; **6.0 docset only**; page typo `RegistryBatchNotificaton` recorded verbatim |
| NAT (`nat.h`) | 20 | 12 | 3 | 1 const + 4 types | coredll.dll (12) | ce-only; 3.0/4.1 |
| Kernel marshaling (`marshal.h`) | 10 | 10 (`MarshalStoreDWORD` family) | — | — | coredll.lib | ce-only; **6.0 only** |
| Kernel reference | 102 | 84 | 11 | 3 | coredll.lib (58), **nkstub.lib (11)**, oemmain.lib (5), nk.lib (4) | pkfuncs.h 71 / nkintr.h 10 / profiler.h 7 / romldr.h 3 — kernel+OAL contract |
| Power | 30 | 19 (`GetSystemPowerState`, `SetSystemPowerState`, `GetSystemPowerStatusEx`, `SetSystemPowerState`…) | 3 (SYSTEM_POWER_STATUS(2), POWER_BROADCAST?) | 1 const + 1 enum | (none stated) | documented header **pwinbase.h** (25), `pm.h` (5) |

All families class **ce-only** except power (mixed — the `SetSystemPowerState`/status names are desktop-shared but the CE semantics differ; classification `common` with CE-gated notes).

## 4. A/W and export-form notes

Wide-only across all families. Power functions are `pwinbase.h`-documented (the PB-side header split — same R-HDR-11 treatment as `kfuncs.h`/`pkfuncs.h`: declarations land in `winbase.h`, the PB name ships as shim).

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0600` | State Broker (17), kernel marshaling (10), 6.0 kernel-ref wave (17) |
| `_WIN32_WCE >= 0x0500` | CeLog 5.0 wave (13), kernel 5.0 wave (23) |
| `_WIN32_WCE >= 0x0300` | CeLog base (54), NAT base (16) |
| kernel-surface | pkfuncs/nkintr/profiler records: **gated declarations, `.def` entry only after Role C confirms export** (R-HDR-11 rule) |

## 6. Implementation notes for Role B

1. **R-HDR-28**: `celog.h`, `regext.h`, `nat.h`, `marshal.h` are ce-only standalone headers (not included by `windows.h`); `pkfuncs.h`/`nkintr.h`/`profiler.h`/`romldr.h` declarations route to `winbase.h`/kernel-surface headers per R-HDR-11 with export gating.
2. State broker: the documented CE 6.0 binding is **aygshell.lib** — on 6.0 the broker lives in the shell component; `.def` matrix records `regext → aygshell.lib` (CE6) with the 5.0-era SYSGEN note.
3. `CEL_*` structures are the event-record grammar — emit verbatim from records, natural-aligned; they are consumed by `celog*.dll` tooling, not applications directly (keep the header but mark it instrumentation-surface).
4. Kernel reference: `nkstub.lib` bindings (11 records) are the CE 6.0 kernel-split pattern (third confirmed area after registry/time/Sleep) — the `.def` generator must emit per-OS-version library variants.
5. Power: `GetSystemPowerStatusEx2` docset notes vs `SYSTEM_POWER_STATUS` layout — static-assert battery; `PWR_`/`POWER_STATE_` constants value-open (probe list).

## 7. Closure statement

460 pages → 256 records. With this spec the **Core OS Services area is fully closed** (CeLog/NAT/State-Broker/Marshaling were the last four unharvested subareas of the 408-page CE 6.0 Core OS Reference). Kernel-reference and power close their areas too. The `developer`-header noise records (3) are page-level artifacts retained as notes. Nothing else excluded.

## 8. Verification hooks

L2: `sizeof(NOTIFICATIONCONDITION)`, `sizeof(SYSTEM_POWER_STATUS_EX2)`-family, `CEL_*` struct battery. L3: `RegistryGetDWORD`+`RegistryNotifyApp` roundtrip on CE 6.0; `GetSystemPowerState`/`SetSystemPowerState` on battery-equipped image; `LogPageInfo` presence probe. Role C: kernel-surface export sweep (pkfuncs/nkintr/profiler), `PWR_*` values.
