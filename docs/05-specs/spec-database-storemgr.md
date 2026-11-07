# Specification — Database (CEDB/EDB) and Storage Manager (`windbase.h`, `storemgr.h`)

Status: final (P3 harvest batch) | Priority: P2 | Fact sources: `data/facts/database.yaml` (135), `storemgr.yaml` (67), `fsdriver-excluded.yaml` (125 closure register) — 327 records
Harvest basis: Database Reference 134+98 (EDB 60+42, CEDB 44+44, replication 17, messages/macros 12), Storage Manager Reference 27+27, Partition Manager 19+19, FAT File System 21+21, FSD Reference 99+85, Bootpart 8, Disk Cache Manager 9, Copy External 7 — 541 harvested pages.

## 1. Purpose and scope

The CE-only object-store database APIs in both generations — **CEDB** (CE 1.0-era `windbase.h`: `CeCreateDatabaseEx2`, `CeOpenDatabaseEx2`, sort orders, properties) and **EDB** (CE 5.0+ SQL-flavoured successor: transactions `CeBeginTransaction`, streams, `CeAddDatabaseProps`) — plus the storage-management surface (`storemgr.h`: `FindFirstStore`/`FindNextStore`+`STOREINFO`, `OpenStore`/`DismountStore`, partition functions; `partdrv.h` partition-driver records) and the FAT utility surface (`fatutil.h` — format/scan; documented binding **fatutil.dll**, the only DLL-named library binding found so far).

The FSD/Bootpart/Disk-Cache/Copy-External driver surface (215 pages → 125 records) is registered in `fsdriver-excluded.yaml` as an explicit closure exclusion (same policy as the GWES internal register of P2).

## 2. Dependencies

`windef.h`, `winnt.h`; CEDB uses `CEOID`/`CEPROPVAL` (records in the area); storage manager uses `HANDLE`-based enumeration idioms.

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Structures | Constants/messages | Notes |
| --- | --- | --- | --- | --- | --- |
| CEDB (`windbase.h`, `pwindbas.h`) | variant `_CEDB` set | `CeCreateDatabaseEx2_CEDB`, `CeOpenDatabaseEx2_CEDB`, `CeSeekDatabase(Ex)_CEDB`, `CeOidGetInfoEx_CEDB`… | `CEDBASEINFOEX_CEDB`, `CEPROPVAL_CEDB`, `CEOIDINFO_CEDB`… | `WM_DBNOTIFICATION`, `CHECK_*/CREATE_*GUID`, `TypeFromPropID` | legacy API — desktop-shared lineage via w32api `_WIN32_WCE` gates |
| EDB | variant `_EDB` set | `CeAddDatabaseProps_EDB`, `CeBeginTransaction_EDB`, `CeMountDBVol_EDB`-overlap… | `CEDBASEINFOEX_EDB`, `CEPROPSPEC_EDB`… | — | 5.0+ generation — same names, **different layouts** (see §6.3) |
| Storage Manager (`storemgr.h`) | 67 | 48 (`FindFirstStore`, `OpenStore`, `CreatePartition`, `FormatStore`…) | 16 (STOREINFO, PARTINFO, SD_REQUEST…) | 2 interfaces | storeapi.lib (22) |
| Partition/FAT | 19 `partdrv.h` + 7 `fatutil.h` + defrag/scandisk/format (14) | `FormatVolume`? family | — | — | fatutil.dll (9) |
| FSD/bootpart/diskcache/copyext | 125 closure notes | — | — | — | **excluded from app set** |

Whole area class **ce-only** (135 + 67 records). Introduced: CEDB 1.0/2.1/3.0 waves (24/23/7), EDB and 5.0-era records (43+18 6.0), storage manager 4.0 (53).

## 4. A/W and export-form notes

CEDB/EDB function pages are generic-named; the pwindbas.h "p" variants are the Pocket PC header-split of the same declarations (R-HDR-10 pattern). Storage manager wide-only. No A/W pairs anywhere in the area.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0500` | EDB variant records (transactions, props, streams) |
| `_WIN32_WCE >= 0x0600` | 6.0 database records (18) |
| `_WIN32_WCE >= 0x0400` | storage manager base (53) |
| `_WIN32_WCE >= 0x0100` | CEDB legacy set |

## 6. Implementation notes for Role B

1. **R-HDR-27**: `windbase.h` ships both CEDB and EDB declarations gated `#if (_WIN32_WCE >= 0x0500)` for EDB; `windbase_edb.h` (1 record) and `pwindbas.h` (18 records) ride as compat shims per the R-HDR-10 pattern. `storemgr.h` standalone; `partdrv.h`/`fatutil.h`/`defragdisk.h`/`scandisk.h`/`formatdisk.h` are the documented tool-surface headers (fatutil is DLL-bound).
2. **Same-name CEDB/EDB divergence**: variant-suffixed ids in the fact DB (`CeChangeDatabaseLCID_CEDB` vs `_EDB`) MUST become two distinct declarations gated by version; **never merge their signatures** (documented layouts differ — e.g. `CEDBASEINFOEX` CEDB vs EDB field sets are not identical; Role C probes sizes).
3. `WM_DBNOTIFICATION`: ce-only message, value-open (probe list).
4. Storage-manager `SD_REQUEST`/secure-digit requests overlap `storemgr.h`/`sdapi`-family — keep the documented split.
5. The replication set (17 pages: DesktopDataBaseCopy?/sync) is recorded; desktop-side counterpart headers (adoce/sql) are NOT in scope.

## 7. Closure statement

541 pages → 327 records incl. the 125-record driver exclusion register (FSD 99+85 pages merged to 99 + 26 tool-level). CEDB/EDB/StorageMgr/Partition/FAT application surfaces closed. `wm_dbnotification` macros and the replication family ride in the records. Object-store structs already delivered in P2 (`windbase.yaml` 6 records) remain the base layer — no overlap (name-level dedupe confirmed: skipped-existing = 5 across P3).

## 8. Verification hooks

L2: CEDB vs EDB `sizeof(CEDBASEINFOEX)` divergence probe; `sizeof(STOREINFO)`. L3: CEDB `CeCreateDatabaseEx2`+`CeOpenDatabaseEx2`+`CeSeekDatabaseEx` roundtrip on 4.x/5.x; EDB transaction roundtrip on 5.0+; `FindFirstStore`/`FindNextStore` enumeration; `FormatVolume` on a scratch volume. Role C: `WM_DBNOTIFICATION` value.
