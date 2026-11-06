# Specification — `winbase.h` (core function set)

Status: final (Phase 1 core set) | Priority: P0 | Fact source: `data/mslearn-facts/ce60-core-facts.json`, `data/mslearn-facts/ce50-core-facts.json`
Full `winbase.h` closure (all 408 Core-OS pages + 48 File-I/O pages + Registry/Database areas) is P1; this spec enumerates the **core function set** harvested and verified for both CE 5.0 and CE 6.0 (64 doc pages), plus the P0 structures.

## 1. Purpose and scope

Process/thread, memory, synchronization, system information, DLL loading, file I/O core, and error functions — the `coredll`-bound heart of the API. GWES functions whose *pages* live in the GWES tree but whose types interlock with P0 (WinMain, CreateWindow family) are specified in `spec-winuser` (P1); only their P0-relevant facts (library binding) are recorded here.

## 2. Dependencies

`winnt.h` (types), `winerror.h` (error semantics), `minwindef`-equivalent macros from `windef.h`.

## 3. Function enumeration (complete for the harvested core set)

Columns — **Lib5/Lib6**: documented link library per the CE 5.0 / CE 6.0 pages. All signatures below are the **documented generic forms** (Unicode platform ⇒ wide types per `unicode-aw-policy.md` R-AW-4; export-form notes in §5). All pages state "Windows CE 1.0 and later" unless noted.

### 3.1 Process and thread

| Function | Documented signature (CE 6.0 page, verbatim) | Header | Lib5 | Lib6 | Notes |
| --- | --- | --- | --- | --- | --- |
| `CreateProcess` | `BOOL CreateProcess(LPCWSTR pszImageName, LPCWSTR pszCmdLine, LPSECURITY_ATTRIBUTES psaProcess, LPSECURITY_ATTRIBUTES psaThread, BOOL fInheritHandles, DWORD fdwCreate, LPVOID pvEnvironment, LPWSTR pszCurDir, LPSTARTUPINFOW psiStartInfo, LPPROCESS_INFORMATION pProcInfo)` | winbase.h | coredll.lib | coredll.lib | CE deltas (documented): `psaProcess`/`psaThread` "Not supported; set to NULL"; `fInheritHandles` "Not supported; set to FALSE"; `CREATE_DEFAULT_ERROR_MODE`, `CREATE_NEW_PROCESS_GROUP`, `CREATE_SEPARATE/SHARED_WOW_VDM`, `CREATE_UNICODE_ENVIRONMENT` flags not supported; executable search order differs per CE version; `HKLM\Loader\SystemPath` honoured |
| `CreateThread` | (see fact record) | winbase.h | coredll.lib | coredll.lib | |
| `OpenProcess`, `TerminateProcess` | (fact records; also RAPI-visible) | winbase.h | coredll.lib | coredll.lib | CE 6.0 remarks: ReadProcessMemory/WriteProcessMemory/TerminateProcess must use the handle from OpenProcess (privilege model) |

### 3.2 Memory management

| Function | Header | Lib5 | Lib6 | Notes |
| --- | --- | --- | --- | --- |
| `VirtualAlloc` | winbase.h | coredll.lib | coredll.lib | 32-bit only address space (charter C-1) |
| `LocalAlloc` | winbase.h | coredll.lib | coredll.lib | |
| `HeapCreate` | winbase.h | coredll.lib | coredll.lib | |

### 3.3 Synchronization

| Function | Header | Lib5 | Lib6 | Notes |
| --- | --- | --- | --- | --- |
| `WaitForSingleObject` | winbase.h | coredll.lib | coredll.lib | |
| `WaitForMultipleObjects` | winbase.h | **Nk.lib** | **Nk.lib** | documented: "The maximum number of object handles is MAXIMUM_WAIT_OBJECTS"; CE 1.0–2.12 cannot wait on semaphores/change-notification/input/timers; CE 3.0+ supports semaphores; CE 1.0/1.01 cannot wait on process/thread handles |
| `CreateEvent` | winbase.h | coredll.lib | coredll.lib | |
| `CreateMutex` | winbase.h | coredll.lib | coredll.lib | |

### 3.4 System management / time / errors

| Function | Header | Lib5 | Lib6 | Notes |
| --- | --- | --- | --- | --- |
| `GetVersionEx` | winbase.h | coredll.lib | coredll.lib | fills `OSVERSIONINFO`; `dwPlatformId == 3` on CE |
| `GetSystemInfo` | winbase.h | coredll.lib | coredll.lib | `SYSTEM_INFO` layout documented (see §4) |
| `GetLastError` / `SetLastError` | winbase.h | coredll.lib | coredll.lib | values per `spec-winerror.md` |
| `Sleep` | winbase.h | coredll.lib | **Nkstub.lib** | the single real CE5→CE6 library change in the core set (CE 6.0 kernel split) — both recorded; `.def` union keeps the symbol, sidecar carries both bindings |
| `GetLocalTime` | winbase.h | coredll.lib | coredll.lib | (CE 5.0 page; CE 6.0 page in inventory) |

### 3.5 DLL loading

| Function | Header | Lib5 | Lib6 |
| --- | --- | --- | --- |
| `LoadLibrary` (→ wide-only) | winbase.h | coredll.lib | coredll.lib |
| `GetProcAddress` | winbase.h | coredll.lib | coredll.lib |

### 3.6 File I/O core (File I/O Reference area, 48 pages)

| Function | Header | Lib5 | Lib6 | Notes |
| --- | --- | --- | --- | --- |
| `CreateFile` | winbase.h | coredll.lib | coredll.lib | CE deltas (documented, CE 5.0 page): `FILE_FLAG_OVERLAPPED` "not supported; however, multiple read/write operations pending on a device at a time are allowed"; no current-directory concept; `FILE_FLAG_RANDOM_ACCESS` interacts with object-store compression; CE ≤ 2.01 `GetLastError` caveat |
| `ReadFile` | winbase.h | coredll.lib | coredll.lib | `lpOverlapped` must be NULL (no async file I/O on CE — documented in FSD/ReadFile remarks) |
| `WriteFile` | winbase.h | coredll.lib | coredll.lib | same |
| `CloseHandle` | winbase.h | coredll.lib | coredll.lib | |
| `FindFirstFile` | winbase.h | coredll.lib | coredll.lib | `WIN32_FIND_DATA` documented (structure page `ee489924`) |

### 3.7 GWES-crosslink (library facts only; full specs in P1)

| Function | Header | Lib5/Lib6 | Notes |
| --- | --- | --- | --- |
| `WinMain` | winuser.h | — (entry point, not an import) | `int WINAPI WinMain(HINSTANCE, HINSTANCE, LPWSTR, int)` — wide `lpCmdLine` on both docsets |
| `CreateWindow`, `RegisterClass`, `DefWindowProc`, `GetMessage` | winuser.h | no library documented on page (GetMessage: coredll.lib both docsets) | `WS_OVERLAPPEDWINDOW` "not supported in Windows Embedded CE" (documented) — compose from WS_OVERLAPPED\|WS_CAPTION\|WS_SYSMENU\|WS_THICKFRAME\|WS_MINIMIZEBOX\|WS_MAXIMIZEBOX |

### 3.8 Winsock crosslink

| Function | Header | Lib5 | Lib6 |
| --- | --- | --- | --- |
| `WSAStartup` | winsock2.h | **Ws2.lib** | **Ws2.lib** |

## 4. Structures (complete for P0)

| Structure | Documented layout (source) | Class / notes |
| --- | --- | --- |
| `OSVERSIONINFO` | see `spec-winnt.md` §3.5 (544 bytes) | ce-modified (TCHAR→WCHAR) |
| `SYSTEM_INFO` | `typedef struct _SYSTEM_INFO { union { DWORD dwOemId; struct { WORD wProcessorArchitecture; WORD wReserved; }; }; DWORD dwPageSize; LPVOID lpMinimumApplicationAddress; LPVOID lpMaximumApplicationAddress; DWORD dwActiveProcessorMask; DWORD dwNumberOfProcessors; DWORD dwProcessorType; DWORD dwAllocationGranularity; WORD wProcessorLevel; WORD wProcessorRevision; } SYSTEM_INFO, *LPSYSTEM_INFO;` (CE 6.0 `ee488780`; CE 5.0 `aa450921` identical) | common layout; `dwProcessorType`/`wProcessorLevel` reflect ARM/MIPS/SH/x86 families (target-matrix §2) |
| `PROCESS_INFORMATION` | `{ HANDLE hProcess; HANDLE hThread; DWORD dwProcessId; DWORD dwThreadId; }` (CE 6.0 `ee488245`; CE 5.0 `ms886775` identical) | common |
| `FILETIME` | `{ DWORD dwLowDateTime; DWORD dwHighDateTime; }` (`ee488581`) | common |
| `OVERLAPPED` | documented page `ee490367` — struct exists for signature compatibility; `lpOverlapped` must be NULL in file APIs (no async I/O) | ce-modified (behavioural) |
| `WIN32_FIND_DATA` | documented page `ee489924` | ce-modified — desktop-common core + CE `dwOID`-related members per docs (verify at P1 harvest of the page) |
| `BY_HANDLE_FILE_INFORMATION` | `{ DWORD dwFileAttributes; FILETIME ftCreationTime; FILETIME ftLastAccessTime; FILETIME ftLastWriteTime; DWORD dwVolumeSerialNumber; DWORD nFileSizeHigh; DWORD nFileSizeLow; DWORD nNumberOfLinks; DWORD nFileIndexHigh; DWORD nFileIndexLow; DWORD dwOID; }` (CE 6.0 `ee490365` **verbatim documented, incl. `dwOID`**) | **ce-modified** — the flagship CE-specific struct delta; w32api lineage gates `dwOID` on `_WIN32_WCE` (independent agreement) |
| `STARTUPINFO(W)` | consumed by `CreateProcess` as `LPSTARTUPINFOW`; no standalone doc page in the CE docset — desktop-common layout per `microsoftdocs-win32`, CE subset of flags | ce-modified (flags subset) — P1 full record |
| `SECURITY_ATTRIBUTES` | type exists; documented as ignored ("Not supported; set to NULL") in process creation | ce-modified |

## 5. A/W and export-form notes

* Documented signatures use generic names; the platform is wide-only (R-AW-4). `CreateProcess`'s documented parameter types are already explicit `LPCWSTR`/`LPWSTR` — i.e. the *documented generic form is itself wide*; export-form (`CreateFileW` vs suffix-less) is a per-function fact collected at Phase 2 def-build time (R-DEF-4) with runtime confirmation (OQ-2/OQ-6).
* No ANSI variants are to be declared (R-AW-3).

## 6. Version gates

All core functions above are documented "Windows CE 1.0 and later" ⇒ no `_WIN32_WCE` gates. Behavioural deltas are runtime facts recorded in `notes`, not gates. `Sleep`'s CE 6.0 `Nkstub.lib` binding is a *library-side* difference only.

## 7. Closure statement

Harvested: 33 CE 6.0 + 31 CE 5.0 core pages (both sets in `data/mslearn-facts/`, with URLs, signatures, requirements, CE-note excerpts). Remaining P1 closure: full Core OS Reference (408 pages), File I/O (48), File Mapping, Registry (30), Database (134) areas — page lists already inventoried in `data/mslearn-inventories/`.

## 8. Verification hooks

L2: `sizeof(PROCESS_INFORMATION) == 16`, `sizeof(SYSTEM_INFO) == 36` (verify-runtime on ARM alignment — OQ-7), `sizeof(BY_HANDLE_FILE_INFORMATION) == 44` incl. `dwOID` (ce-modified assertion).
L3: on-device probes — `GetVersionEx` platform/major checks; `GetSystemInfo().wProcessorArchitecture` matches the image's CPU family; `CreateFile` on missing path → `ERROR_FILE_NOT_FOUND`; `WaitForMultipleObjects` handle-count limit probe (OQ-8).
