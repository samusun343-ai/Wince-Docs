# Specification — `winbase.h` (OS services: process/thread/memory/sync/time/string/serial/debug) + `dbgapi.h`

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/winbase-os.yaml` (207 records), `data/facts/dbgapi.yaml` (14 records)
Harvest basis: Process and Thread (39+39), Memory Management (35+26), Synchronization (25+25), Time (26+23), String/Strings (13+13), Unicode (8+8), ToolHelp (routed to `spec-toolhelp.md`), DLL (12+11), Exception (10+7), System Management (17+15), Message Queue P2P (routed to `spec-msgqueue.md`), Debugging (32+29), Serial Communications (20+20), Fiber (7+7) — 520 harvested pages.

## 1. Purpose and scope

The remaining documented `winbase.h` application surface of the Core OS reference beyond the P0 core set: process/thread control (incl. the CE 6.0 `*Ex` process-memory family), the CE-native thread-priority and quantum API (`CeSetThreadPriority`, `CeSetThreadQuantum`), memory management (`VirtualAlloc` family, `CeHeapCreate`, remote heaps), synchronization, time (incl. CE raw-time API), string/Unicode/NLS boundary, DLL loading, structured exceptions, serial communications, fibers, and the debug event loop. `dbgapi.h` debug macros (`DEBUGMSG`, `RETAILMSG`, …) are specified here because they are the documented debug output surface used by both application and OEM code.

## 2. Dependencies

`winnt.h`, `winerror.h`, `windef.h`. Serial structures (`DCB`, `COMMTIMEOUTS`, `COMMPROP`, `COMSTAT`) interlock with `CreateFile`-opened `COMx:` handles (`spec-winbase-file-io.md`).

## 3. Enumeration highlights (full lists in the fact YAML)

### 3.1 Process and thread — CE deltas recorded per page

* `CreateProcess` documented CE delta (both docsets): `lpApplicationName` must be NULL and the executable is taken from `lpCommandLine`; no environment block (`lpEnvironment` = NULL); `psiStartInfo` ignored fields; executable search order per version.
* CE-native priority model (**ce-only**, coredll.lib): `CeSetThreadPriority`/`CeGetThreadPriority` (0–255, 0 highest), `CeSetThreadQuantum`/`CeGetThreadQuantum` (ms), `CeGetCallerTrust`. The w32-style `SetThreadPriority` constants remain the compatibility layer; the CE docs define the 256-level API as the primary real-time interface.
* CE 6.0 additions (gate `_WIN32_WCE >= 0x0600`): `VirtualAllocEx`/`VirtualFreeEx`/`VirtualProtectEx`/`VirtualQueryEx`/`VirtualCopyEx`/`VirtualSetAttributesEx`/`VirtualAllocCopyEx` (cross-process VM, kernel-surface documented in pkfuncs.h — R-HDR-11 note), `OpenThread`, `CeSetProcessVersion`, `CeRemoteHeapCreate`/`CeRemoteHeapTranslatePointer`, `CheckRemoteDebuggerPresent`/`IsDebuggerPresent`, `DebugActiveProcessStop`, `AddVectoredExceptionHandler`/`RemoveVectoredExceptionHandler` (+ `VectoredHandler` callback type).
* Debug event loop (documented, coredll.lib): `WaitForDebugEvent`, `ContinueDebugEvent`, `DebugActiveProcess`, plus the `DEBUG_EVENT` structure family (`EXCEPTION_DEBUG_INFO`, `CREATE_PROCESS_DEBUG_INFO`, `CREATE_THREAD_DEBUG_INFO`, `EXIT_PROCESS_DEBUG_INFO`, `EXIT_THREAD_DEBUG_INFO`, `LOAD_DLL_DEBUG_INFO`, `UNLOAD_DLL_DEBUG_INFO`, `OUTPUT_DEBUG_STRING_INFO`, `EXCEPTION_RECORD`).

### 3.2 Memory management

`VirtualAlloc`/`VirtualFree`/`VirtualProtect`/`VirtualQuery` (1.0), `HeapCreate`/`HeapAlloc` family, `LocalAlloc` family, `CeHeapCreate` (**ce-only**, remote heap variant documented 5.0), `CeZeroPointer` (**ce-only**, 6.0), `GlobalMemoryStatus` + `MEMORYSTATUS`, `MEMORY_BASIC_INFORMATION`, `GetProcessMemoryInfo`? — not documented in this harvest (toolhelp-adjacent; see `spec-toolhelp.md`).

### 3.3 Synchronization (25+25 pages)

`CreateEvent`/`SetEvent`/`ResetEvent`/`PulseEvent`, `CreateMutex`/`ReleaseMutex`, `CreateSemaphore`/`ReleaseSemaphore` (CE 3.0+), `WaitForSingleObject`/`WaitForMultipleObjects`/`MsgWaitForMultipleObjects(Ex)` (the GWES-tree page records the message-queue interplay), `InitializeCriticalSection` family incl. `TryEnterCriticalSection`, `Interlocked*` family, `CreateMsgQueue`-family crosslink (§`spec-msgqueue.md`). Documented lib note: `WaitForMultipleObjects` = Nk.lib (both docsets, recorded in P0).

### 3.4 Time (26+23 pages) — library split finding

`GetSystemTime`/`GetLocalTime`/`SetLocalTime`, `SystemTimeToFileTime`/`FileTimeToSystemTime`/`FileTimeToLocalFileTime`/`LocalFileTimeToFileTime`/`CompareFileTime`, `GetTickCount`, `GetTimeZoneInformation` + `TIME_ZONE_INFORMATION`, `SystemTimeToTzSpecificLocalTime`, `CeGetRawTime`/`CeGetRawTimeOffset` (**ce-only**, 6.0 — raw tick time without Tz conversion).
**Lib5→Lib6 differences (documented):** `CompareFileTime`, `FileTimeToSystemTime`, `SystemTimeToFileTime`: coredll.lib → **Nkstub.lib**; `GetTickCount`: coredll.lib → **Oemmain.lib**; `IsProcessorFeaturePresent` → Oemmain.lib. All recorded in the fact YAML `target_lib` and the `.def` sidecar per `def-requirements.md` §2.

### 3.5 String / Unicode / NLS boundary (13+13, 8+8)

`lstrlen` family (wide-only), `wcsspn`-family documented shims, `MultiByteToWideChar`/`WideCharToMultiByte` (coredll.lib; the documented CE notes: code pages limited to installed ones; CP_ACP on CE = CP 1252 unless locale set), `LCMapString`, `GetStringTypeEx`, `IsDBCSLeadByte` (far-east builds), `CompareString`. Version-info reading structs (`VS_VERSIONINFO`, `VS_FIXEDFILEINFO`, `StringFileInfo`, `StringTable`, `VarFileInfo`, `Var`) are documented here and consumed by `GetFileVersionInfo` (`spec-winbase-file-io.md` §3.1).

### 3.6 DLL / module (12+11 pages)

`LoadLibrary`/`FreeLibrary`/`GetProcAddress`/`GetModuleHandle`/`GetModuleFileName` + `LoadDriver` (**ce-only**, trust-level driver load; documented `Coreloc.lib` binding on CE 6.0 pages — see §5), `RegisterDbgZones` (dbgapi crosslink), `DllMain` documented callback form.

### 3.7 Exceptions (10+7)

`SetUnhandledExceptionFilter`, `UnhandledExceptionFilter`, `RaiseException`, `GetExceptionInformation` macro-form pages, `EXCEPTION_POINTERS` usage — plus the CE 6.0 vectored-handler family (§3.1). CE note recorded: `EXCEPTION_CONTINUE_EXECUTION` semantics with the CE scheduler.

### 3.8 System management (17+15)

`GetSystemInfo`/`SYSTEM_INFO` (P0), `GetVersionEx`, `GetSystemMetrics` crosslinks, `IsProcessorFeaturePresent`, `GetUserDirectory`-adjacent user pages (winreg spec), `SetSystemPowerState`/`GetSystemPowerStatusEx(2)` (**ce-only**, power management core; both docsets), `SystemIdleTimerReset` (**ce-only**), `CeGetCallerTrust` (**ce-only**, trust levels), `KernelIoControl` (**ce-only** kernel ioctl surface, documented 6.0).

### 3.9 Serial communications (20+20 pages, **Serdev.lib** binding)

`BuildCommDCB(AndTimeouts)`, `SetCommState`/`GetCommState` (`DCB`), `SetCommTimeouts`/`GetCommTimeouts` (`COMMTIMEOUTS`), `SetCommMask`/`GetCommMask`/`WaitCommEvent`, `ClearCommError` (`COMSTAT`, `COMMPROP`), `EscapeCommFunction`, `PurgeComm`, `SetupComm`, `TransmitCommChar`. The whole subarea is documented with **Serdev.lib** on the CE 6.0 pages (CE 5.0 pages: Serdev.lib as well) — the strongest binding split in the harvest.

### 3.10 Fibers (7+7)

`CreateFiber`/`SwitchToFiber`/`DeleteFiber`/`ConvertThreadToFiber` — documented (contrary to desktop expectations, CE 5.0/6.0 docsets carry the fiber reference).

### 3.11 `dbgapi.h` debug macros (14 records, all **ce-only**)

`DEBUGMSG`, `RETAILMSG`, `ERRORMSG`, `ASSERT`, `ASSERTMSG`, `DEBUGCHK`, `DEBUGLED`, `RETAILLED`, `DEBUGREGISTER`, `RETAILREGISTERZONES`, `DEBUGZONE`, `NKDbgPrintfW`, `RegisterDbgZones`, `WriteDebugLED` (+ `DBGPARAM` structure). These are the Platform Builder debug-zone macros, exported and documented for application use; they have no desktop counterpart. Lib note: `WriteDebugLED` binding moves coredll.lib (CE 5.0) → **Oemmain.lib** (CE 6.0).

## 4. A/W and export-form notes

String APIs documented in generic form, wide-only exports (R-AW-4). `LoadLibrary` documented wide-only. `NKDbgPrintfW` is the only explicitly-wide-suffixed function name in this batch.

## 5. Version gates / library summary

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0600` | `VirtualAllocEx` family, `OpenThread`, `CeSetProcessVersion`, `CeRemoteHeap*`, `CeGetRawTime(Offset)`, `CeZeroPointer`, vectored exception handlers, `CheckRemoteDebuggerPresent`, `DebugActiveProcessStop`, `KernelIoControl` page, `ReadMsgQueueEx` (msgqueue spec) |
| `_WIN32_WCE >= 0x0500` | `CeHeapCreate` remote-heap form, `IsProcessorFeaturePresent` pages |
| none | fiber set (documented 1.0–3.0 range), serial set, debug event loop |

Documented libraries beyond coredll: **Serdev.lib** (serial, 32 records), **Coreloc.lib** (LoadDriver/locale, 22), **Nk.lib** (7), **Coremain.lib** (8), **Nkstub.lib** (kernel-split exports, CE 6.0 pages), **Oemmain.lib** (GetTickCount/IsProcessorFeaturePresent/WriteDebugLED, CE 6.0 pages).

## 6. Implementation notes for Role B

1. **R-HDR-11.** Functions whose documented header is `Kfuncs.h` (GetCurrentProcess, GetCurrentThread, DebugBreak, SetEvent, ResetEvent, …) are declared in the project's `winbase.h`; `kfuncs.h` ships as an include-compatibility shim. Functions documented only under `pkfuncs.h` (`CeRemoteHeapCreate`, `VirtualAllocCopyEx`, `VirtualCopyEx`, …) are kernel/OAL-surface: declare in `winbase.h` under a `#if defined(_WIN32_WCE) && _WIN32_WCE >= 0x0600` gate with a doc-comment marking them kernel-surface, and list them in the `.def` only if Role C confirms export from coredll.
2. Thread-priority constants: provide the w32 `THREAD_PRIORITY_*` set (values from the w32api lineage) AND the CE-native 0–255 model documentation comment; `CeSetThreadPriority` clamps per docs.
3. `TIME_ZONE_INFORMATION` and `GetTimeZoneInformation` are documented; standard-time names are wide char arrays — no A/W pair.
4. Serial structures require exact packing (DCB layout is hardware-facing): static asserts on member offsets.

## 7. Closure statement

520 harvested pages → 207 winbase.h-bound records + 16 toolhelp + 9 msgqueue + 14 dbgapi + internal-excluded routing (CeLog/NAT/State-Broker subareas NOT harvested this batch — they are recorded in `header-inventory.md` as remaining P2 core-os closure: CeLog 77+76, NAT 20+20, State and Notifications Broker 17, Kernel Buffer Marshaling 10). The remaining `(none)`-header overview pages are recorded as note-kind facts.

## 8. Verification hooks

L2: `sizeof(DEBUG_EVENT)`, `sizeof(DCB)`, `sizeof(TIME_ZONE_INFORMATION)`, `sizeof(MEMORY_BASIC_INFORMATION)`. L3: `CeSetThreadPriority(h, 249)` observable scheduling; `VirtualAllocEx` cross-process on CE 6.0 only; serial `WaitCommEvent` on CEPC with a loopback; `DEBUGMSG` zone output via `RegisterDbgZones`.
