# Specification — `winbase.h` (file I/O, file mapping, object-store and password surface)

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/winbase-fileio.yaml` (54 records), `data/facts/windbase.yaml` (6 records)
Harvest basis: File I/O Reference (48+48 pages), File Mapping Reference (5+5), User Management Reference (7), File System Password Reference (12) from the CE 6.0 and CE 5.0 docsets.

## 1. Purpose and scope

The complete documented CE file surface of `winbase.h`: create/read/write, find, attributes, change notification, file mapping (incl. the CE-only `CreateFileForMapping` model), version info, temp files, store information — plus the `windbase.h`-documented object-store structures and password API that close the File I/O area. Registry functions documented on the same pages are specified in `spec-winreg.md`; database (CEDB) APIs are P2.

## 2. Dependencies

`winnt.h` (types), `winerror.h`, `windef.h` macros. `FILECHANGEINFO` (extfile.h) is consumed by the message-queue file-change mechanism (`spec-msgqueue.md`).

## 3. Enumeration (all records in the fact YAML; notable rows here)

### 3.1 Functions (45)

| Function | Header | Lib5/Lib6 | Introduced | Notes |
| --- | --- | --- | --- | --- |
| `CreateFile` | winbase.h | coredll | 1.0 | documented deltas: no current directory; `FILE_FLAG_OVERLAPPED` unsupported (but pending I/O on devices allowed); security attributes NULL |
| `CreateFileForMapping` | winbase.h | coredll | 1.0 | **ce-only** — required predecessor of `CreateFileMapping` (see §6 R-FM-1) |
| `CreateFileMapping` | winbase.h | coredll | 1.0 | operates on handles from `CreateFileForMapping` (Windows CE model) |
| `MapViewOfFile` / `FlushViewOfFile` / `UnmapViewOfFile` | winbase.h | coredll | 1.0 | |
| `ReadFile` / `WriteFile` | winbase.h | coredll | 1.0 | `lpOverlapped` must be NULL (no async file I/O) |
| `FindFirstFile` / `FindNextFile` / `FindClose` | winbase.h | coredll | 1.0 | `WIN32_FIND_DATA` documented; OID variants via `CEDIRINFO`/`CEFILEINFO` (windbase.h) |
| `FindFirstFileEx` | winbase.h | coredll | 1.0 | `FINDEX_INFO_LEVELS` / `FINDEX_SEARCH_OPS` documented; only `FindExInfoStandard`+`FindExSearchNameMatch` guaranteed |
| `FindFirstChangeNotification` family (3) | winbase.h | coredll | 1.0 | object-store/file-system change notification |
| `GetFileAttributesEx` | winbase.h | coredll | 1.0 | `GET_FILEEX_INFO_LEVELS` + `WIN32_FILE_ATTRIBUTE_DATA` documented |
| `GetFileInformationByHandle` | winbase.h | coredll | 1.0 | fills CE-modified `BY_HANDLE_FILE_INFORMATION` (`dwOID`) |
| `GetDiskFreeSpaceEx` | winbase.h | coredll | 1.0 | |
| `GetFileVersionInfo(Size)` | winbase.h | coredll | 1.0 | version-resource read side; structs in `data/facts/winbase-os.yaml` |
| `CeGenRandom` | winbase.h | coredll | 1.0 | **ce-only** cryptographic random (no desktop `SystemFunction036` page) |
| `CeGetCanonicalPathName` | winbase.h | coredll | 1.0 | **ce-only** |
| `CeGetFileNotificationInfo` | winbase.h | coredll | 1.0 | **ce-only** (message-queue based notification) |
| `GetStoreInformation` | winbase.h | coredll | 1.0 | **ce-only** (object store statistics) |
| `GetUserNameEx` | winbase.h | coredll | 6.0 (ce60 page) | user management; CE 5.0 docset files the page under a different node |
| `CopyFile(Ex)`, `MoveFile`, `DeleteFile`, `DeleteAndRenameFile` | winbase.h | coredll | 1.0–2.0 | `DeleteAndRenameFile` is **ce-only** |
| `LockFileEx` / `UnlockFileEx` | winbase.h | coredll | 2.1 | |
| `GetTempPath` / `GetTempFileName` | winbase.h | coredll | 1.0 | |
| `SetFilePointer`, `SetEndOfFile`, `FlushFileBuffers`, `GetFileSize` | winbase.h | coredll | 1.0 | |
| `CreateDirectory`, `RemoveDirectory`, `SetFileAttributes` | winbase.h | coredll | 1.0 | |

### 3.2 Structures (winbase.h, 8)

`BY_HANDLE_FILE_INFORMATION` (ce-modified, `dwOID`), `WIN32_FIND_DATA`, `WIN32_FILE_ATTRIBUTE_DATA`, `OVERLAPPED` (compatibility-only; must be NULL), `FILE_NOTIFY_INFORMATION` (winnt.h), `FINDEX_INFO_LEVELS`, `FINDEX_SEARCH_OPS`, `GET_FILEEX_INFO_LEVELS`, and the `FILECHANGEINFO` record (documented header **extfile.h**, binding `ceshell.lib` on the CE 6.0 page) used with `ReadMsgQueue`-based file change notification.

### 3.3 Object-store and password surface (documented header windbase.h)

| Item | Kind | Introduced | Notes |
| --- | --- | --- | --- |
| `CEDIRINFO`, `CEFILEINFO` | structure | 1.0 | **ce-only** object-store variants carrying `CEOID` (docs: "Earlier versions of Windows Embedded CE assigned OIDs to objects …"); consumed instead of `WIN32_FIND_DATA` when OID-level results are needed |
| `CheckPassword`, `SetPassword`, `GetPasswordActive`, `SetPasswordActive` | function | 2.1 | password model of the File System Password area; no documented link library |
| `GetPasswordStatus` / `SetPasswordStatus` | function | 2.1 | documented header **pwinbase.h** (PB-side); project placement in `winbase.h` per R-HDR-11 |

## 4. A/W and export-form notes

All file functions are documented in generic (TCHAR) form; on CE the only export is the wide form (`ReadFile` operates on wide paths — `unicode-aw-policy.md` R-AW-4). `RegSetValueEx`-style A/W twin pages do not exist in this area; `CreateFileForMapping` has a documented `CreateFileForMappingW` alias (recorded as ce-only twin).

## 5. Version gates

| Gate | Items | Evidence |
| --- | --- | --- |
| `_WIN32_WCE >= 0x0400` | `FILECHANGEINFO` extfile.h record (ce60 binding only) | page Requirements |
| none required for 4.x | `LockFileEx`/`UnlockFileEx` (2.1), `CopyFileEx` (2.1) | OS Versions fields |

No CE5→CE6 binding changes in this area except the `FILECHANGEINFO` → `ceshell.lib` CE 6.0-only binding (CE 5.0 page states no library).

## 6. Implementation notes for Role B

1. **R-FM-1.** `CreateFileForMapping` MUST be declared before `CreateFileMapping` usage guidance; it is not a desktop API — guard with plain definition (no `_WIN32_WINNT` style guards; use `_WIN32_WCE` presence as the header-set invariant).
2. **R-FM-2.** `FILECHANGEINFO` is declared in the project's `winbase.h` with an `extfile.h` include-compatibility shim (same pattern as R-HDR-9/pwinuser).
3. **R-FM-3.** `CEDIRINFO`/`CEFILEINFO` go in `windbase.h`; the full legacy database area (134 pages, P2) extends that header later.
4. `GetPasswordStatus`/`SetPasswordStatus` declared in `winbase.h`; `pwinbase.h` ships as shim.

## 7. Closure statement

All 169 harvested pages of the four subareas are represented: 93 unique page names → 54 fact records after docset merge + dedupe against P0 (`CreateFile`, `ReadFile`, `FindFirstFile`, `CloseHandle`, `OVERLAPPED`… already in `spec-winbase-core.md`). Registry-Reference pages within the same harvest are closed by `spec-winreg.md`; nothing else is excluded.

## 8. Verification hooks

L2 static asserts: `sizeof(BY_HANDLE_FILE_INFORMATION)` (contains trailing `dwOID`); `sizeof(WIN32_FIND_DATA)`; `sizeof(FILECHANGEINFO)`. L3 runtime probes: `CreateFileForMapping` → `CreateFileMapping` → `MapViewOfFile` roundtrip; `CeGenRandom` output non-constant; `GetStoreInformation` fills struct.
