# Specification — `notify.h` (User Notifications)

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/notify.yaml` (13 records)
Harvest basis: Notify Reference — 13+13 pages (ce60 tree adds the Notification Reference internals, routed to `internal-excluded.yaml`).

## 1. Purpose and scope

The CE-only user-notification API: scheduled application launches (`CeRunAppAtTime`), event-triggered launches (`CeRunAppAtEvent`), and the user-notification dialogs (`CeSetUserNotification(Ex)`). Desktop has no counterpart (desktop notifications went through the taskbar/`Shell_NotifyIcon`, which CE documents separately in `spec-shellapi.md`). The whole surface is **ce-only**.

## 2. Dependencies

`windef.h`, `winnt.h`. The trigger struct consumes `SYSTEMTIME` (`winbase.h`); event types (`NOTIFICATION_EVENT_*`) are value-supplied from the w32api CE-adapted lineage (verify-runtime).

## 3. Enumeration (complete)

| Item | Kind | Introduced | Lib | Notes |
| --- | --- | --- | --- | --- |
| `CeRunAppAtTime` | function | 1.0 | coredll.lib | scheduled app launch; doc note on CE 1.0 predecessor naming (`PegRunAppAtTime` era, see record note) |
| `CeRunAppAtEvent` | function | 1.0 | coredll.lib | event-triggered launch (event id per `NOTIFICATION_EVENT_*`) |
| `CeSetUserNotification` | function | 1.0 | coredll.lib | |
| `CeGetUserNotificationPreferences` | function | 1.0 | coredll.lib | |
| `CeHandleAppNotifications` | function | 1.0 | coredll.lib | |
| `CeClearUserNotification` | function | 1.0 | coredll.lib | CE 1.0 note references the `Peg`-prefixed predecessor |
| `CeGetUserNotification` / `CeGetUserNotificationHandles` | function | 2.1 | coredll.lib | |
| `CeSetUserNotificationEx` | function | 2.1 | coredll.lib | trigger-based extended form |
| `CeEventHasOccurred` | function | 2.0 | coredll.lib | signals an event type occurred (notification broker entry point) |
| `CE_USER_NOTIFICATION` | structure | 1.0 | — | dialog/sound trigger description |
| `CE_NOTIFICATION_TRIGGER` | structure | 2.1 | — | |
| `CE_NOTIFICATION_INFO_HEADER` | structure | 2.1 | — | |

## 4. A/W and export-form notes

Unicode-only (documented generic forms are wide). No A/W pairs; `CeSetUserNotificationEx` has no non-Ex twin conflict.

## 5. Version gates

`_WIN32_WCE >= 0x0201` for the Ex/handles/get forms; base set 1.0. No CE5→CE6 binding changes (coredll.lib throughout).

## 6. Implementation notes for Role B

1. **R-HDR-14**: `notify.h` is its own header; `windows.h` does not include it on desktop and will not here (explicit include required — matches documented Requirements header field).
2. The CE 6.0 "Notification Reference" internal pages (`CeNotifyPrivate_*`, `CeNotifyPublic_*`, Notifext.hxx) are GWES implementation documentation — recorded in `internal-excluded.yaml`, NOT declared.
3. `NOTIFICATION_EVENT_*` constants: names documented on the `CeRunAppAtEvent` page; values via the w32api CE lineage — Role C probes on device (OQ-24).

## 7. Closure statement

13+13 Notify Reference pages → 13 records. The 23 CE 6.0-only "Notification Reference" pages are closed as internal (448-record exclusion register, see `spec-gwes-misc.md` §4). Nothing else excluded.

## 8. Verification hooks

L2: `sizeof(CE_USER_NOTIFICATION)`, `sizeof(CE_NOTIFICATION_TRIGGER)`. L3: `CeRunAppAtTime` +2s fires the app on CEPC; `CeSetUserNotificationEx` dialog appears; `CeClearUserNotification` cancels.
