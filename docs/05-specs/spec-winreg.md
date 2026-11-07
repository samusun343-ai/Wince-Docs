# Specification — `winreg.h`

Status: final (P2 harvest batch) | Priority: P1 | Fact source: `data/facts/winreg.yaml` (33 records)
Harvest basis: Registry Reference — 30 pages (CE 6.0) / 14 pages (CE 5.0); multi-user registry functions documented on User Management pages (pwinreg.h).

## 1. Purpose and scope

The complete documented CE registry application surface: core `Reg*` functions, the CE change-notification family (`CeFindFirstRegChange`), hive/backup functions (`RegSaveKey`, `RegCopyFile`, `RegReplaceKey`, `RegRestoreFile`), security/locking structs, and the multi-user registry functions documented under pwinreg.h (`SetCurrentUser`, `SetUserData`, `GetUserDirectory`). Mounting, hive loading and `FSDMGR` registry functions are driver-facing and out of scope.

## 2. Dependencies

`winnt.h` (types), `winerror.h`. Constants `REG_*`/`KEY_*` are value-supplied by the w32api public-domain lineage (`verify-runtime` until Role C probing) and by desktop-docs agreement where stated.

## 3. Enumeration (33 records)

### 3.1 Core registry functions (documented 1.0, coredll.lib / Nkstub.lib — see §5)

`RegCloseKey`, `RegCreateKeyEx`, `RegOpenKeyEx`, `RegQueryValueEx`, `RegSetValueEx`, `RegDeleteKey`, `RegDeleteValue`, `RegEnumKeyEx`, `RegEnumValue`, `RegQueryInfoKey`, `RegFlushKey`.
Documented CE notes captured per record: `RegCreateKeyEx`/`RegOpenKeyEx` etc. operate on `HKEY` handles pre-defined for the object-store/hive registry; `RegEnumKeyEx` supports the `REG_SZ`/`REG_DWORD`-oriented query path; `RegQueryValueEx` requires the value-type awareness documented on the page (no automatic type coercion); `RegCloseKey` "always writes information to the registry before closing" (no lazy close); `RegFlushKey` "By default, Windows Embedded CE does not support a lazy flush…" (explicit flush discipline).

### 3.2 Backup / hive functions (ce-modified set)

| Function | Introduced | Notes |
| --- | --- | --- |
| `RegCopyFile` | 2.1 | exports the object-store registry to a file |
| `RegRestoreFile` | 2.1 | "supported only for the object store-based registry" |
| `RegSaveKey` | 4.0 | hive-aware save; doc note: object-store save/restore pairing |
| `RegReplaceKey` | 4.0 | |
| `HiveRAMInfo`, `HiveRAMRegion` (structs) | 4.0 | RAM hive region description (boot-time hive layout) |
| `RegSecureKey`, `RegSecureKeyList` (structs) | 4.0 | registry ACL precursor (see `RegSecureKeyList` consumption on the security pages) |

### 3.3 CE change notification (ce-only family)

`CeFindFirstRegChange` (5.0), `CeFindNextRegChange` (5.0), `CeFindCloseRegChange` (5.0) — handle-based registry change watching; the CE 6.0 docset adds `CeRegGetInfo` and `CeRegGetNotificationInfo` (6.0 only) and `CeRegTestSetValueW` (5.0, wide-explicit export name).

### 3.4 Multi-user registry (documented header pwinreg.h — R-HDR-10)

`SetCurrentUser`, `SetUserData`, `GetUserDirectory` (4.0, coredll.lib): user-profile registry redirection. Declarations live in the project's `winreg.h`; `pwinreg.h` ships as an include-compatibility shim (pattern R-HDR-9).

### 3.5 Multi-user data access (4.2, ce-only)

`ReadRegData` / `WriteRegData` / `ReadGenericData` / `WriteGenericData` / `RegistryOperation` — the documented per-user registry collation API of CE 4.1/4.2 (multi-user CE devices).

## 4. A/W and export-form notes

`RegSetValueEx` page: "Windows Embedded CE supports only the Unicode version of this function" — the header exports generic + wide forms, no ANSI forms (R-AW-4). `CeRegTestSetValueW` is documented with an explicit W suffix (wide-only export recorded).

## 5. Version gates and library bindings

| Item | CE 5.0 page lib | CE 6.0 page lib | Gate |
| --- | --- | --- | --- |
| `RegCloseKey`, `RegCreateKeyEx`, `RegFlushKey`, `RegOpenKeyEx`, `RegQueryValueEx` | coredll.lib | **Nkstub.lib** | no gate; `.def` union + sidecar records both bindings (same treatment as `Sleep` in `spec-winbase-core.md` §3.4) |
| `CeFindFirst/Next/CloseRegChange`, `CeRegTestSetValueW` | — | coredll.lib | `_WIN32_WCE >= 0x0500` |
| `CeRegGetInfo`, `CeRegGetNotificationInfo` | no page | coredll.lib | `_WIN32_WCE >= 0x0600` |
| `ReadRegData` family | — | coredll.lib | `_WIN32_WCE >= 0x0420` (documented "CE .NET 4.2") |
| `RegSaveKey`/`RegReplaceKey` | — | coredll.lib | `_WIN32_WCE >= 0x0400` |

## 6. Implementation notes for Role B

1. Root keys `HKEY_CLASSES_ROOT`…`HKEY_LOCAL_MACHINE` are pointer-like sentinels per CE docs; define per w32api lineage values and keep `verify-runtime` until probed (already recorded in `winnt-core.yaml` where documented).
2. `HiveRAMInfo`/`HiveRAMRegion`/`RegSecureKey(List)` are structure-only records — no application-facing function pages exist for them in the harvest (consumed by boot/security components); declare but do not document as callable surface.
3. `KEY_ALL_ACCESS`-style access masks and `REG_*` type constants: values from the w32api lineage (public domain), desktop-docs cross-check where the desktop pages state them.

## 7. Closure statement

All 44 harvested Registry Reference pages + the 7 User Management pages are represented (33 records after docset merge and P0 dedupe). Not harvested (out of scope, driver/installer-facing): `FSDMGR` registry filters, `RegisterClipboardFormat`-adjacent pages, and the `OEMCertificate` security chain — listed in `header-inventory.md` P2 rows.

## 8. Verification hooks

L2: `sizeof(CE_NOTIFICATION…)` not applicable here; assert `HKEY` is pointer-sized; `REG_SZ`/`REG_BINARY`/`REG_DWORD` values from the lineage compile. L3 probes: `CeFindFirstRegChange` roundtrip on CE 5.0+ only; `RegCopyFile`+`RegRestoreFile` pair on object-store registry builds; `Nkstub.lib` symbol resolution on a CE 6.0 image (`dumpbin /exports coredll.dll` equivalent via `tools/` Role C harness).
