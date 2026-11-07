# Specification — `msgqueue.h` (Point-to-Point Message Queues)

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/msgqueue.yaml` (9 records)
Harvest basis: Message Queue Point-to-Point Reference — 9 (CE 6.0) / 8 (CE 5.0) pages.

## 1. Purpose and scope

The CE-only point-to-point message queue API (`MsgQueue`), the documented inter-process/streaming data path used by drivers (power, battery, file change notification via `FILECHANGEINFO`), the GWES message queue reference (`GetMsgQueueInfo` consumers) and application IPC. There is no desktop Win32 counterpart — the entire header is **ce-only**.

## 2. Dependencies

`windef.h`, `winnt.h` (`HANDLE`, `DWORD`). `FILECHANGEINFO` (extfile.h) is the payload type of the file-change queue (`spec-winbase-file-io.md` §3.2).

## 3. Enumeration (complete)

| Item | Kind | Introduced | Lib | Notes |
| --- | --- | --- | --- | --- |
| `CreateMsgQueue` | function | 4.0 | coredll.lib | `HANDLE CreateMsgQueue(LPCWSTR lpszName, LPMSGQUEUEOPTIONS lpOptions)` |
| `OpenMsgQueue` | function | 4.0 | coredll.lib | opening a queue by name from another process |
| `ReadMsgQueue` | function | 4.0 | coredll.lib | blocking read with timeout |
| `ReadMsgQueueEx` | function | **6.0** | coredll.lib | CE 6.0 docset only — extended read (returns source process info) |
| `WriteMsgQueue` | function | 4.0 | coredll.lib | |
| `GetMsgQueueInfo` | function | 4.0 | coredll.lib | fills `MSGQUEUEINFO` |
| `CloseMsgQueue` | function | 4.0 | coredll.lib | |
| `MSGQUEUEOPTIONS` | structure | 4.0 | — | documented members: `dwSize`, `dwFlags`, `dwMaxMessages`, `cbMaxMessage`, `bReadables` (ce50 page glue repaired; verify member order at Role C) |
| `MSGQUEUEINFO` | structure | 4.0 | — | query-result twin |

## 4. A/W and export-form notes

Names are wide (`LPCWSTR lpszName`); no A/W pairs. `ReadMsgQueueEx` is an explicit-`Ex` export (CE 6.0 only).

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0400` | whole API (documented "Windows CE .NET 4.0 and later") |
| `_WIN32_WCE >= 0x0600` | `ReadMsgQueueEx` |

## 6. Implementation notes for Role B

1. **R-HDR-13**: `msgqueue.h` is its own header (CE-documented), included from nothing else; do not fold into `winbase.h`.
2. Flag constants named on the pages (`MSGQUEUE_ALLOW_BROWSE`, `MSGQUEUE_MSGSIZE_*`, `MSGQUEUE_FIFO`, `MSGQUEUE_PRIORITY_NORMAL`, …): values not stated in the CE docs — cross-check channel is the public-domain w32api CE-adapted lineage; two constants are recorded with lineage values (`verify-runtime`), the rest are flagged in open-questions (OQ-23) for Role C probing.
3. `WaitForSingleObject` works on queue handles — document in the header comment (already recorded in `spec-winbase-os.md` §3.3).

## 7. Closure statement

9+8 pages → 9 records (all unique names; docset merge complete). Nothing excluded. The GWES-side "Message Queue Reference" (19+19 pages: GetMessage/PeekMessage family) is the window-message queue of `winuser.h`, already closed by `spec-winuser-core.md` — a documentation-name collision only, recorded here to prevent double-mapping.

## 8. Verification hooks

L2: `sizeof(MSGQUEUEOPTIONS)`; flag constant values. L3: producer/consumer roundtrip across two processes; `ReadMsgQueueEx` present on CE 6.0 image only; `FILECHANGEINFO` delivery via `FindFirstChangeNotification`-adjacent queue on a hive-registry image.
