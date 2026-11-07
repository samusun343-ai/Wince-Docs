# Specification — Networking extras: IP Helper, DNS, IPv6, OBEX, ConnMgr, GPS, Bluetooth, SNMP

Status: final (P3 harvest batch) | Priority: P2 | Fact sources: `data/facts/iphlp.yaml` (96), `dnsapi.yaml` (32), `ws2tcpip.yaml` (35), `obex.yaml` (16), `connmgr.yaml` (30), `gps.yaml` (17), `bluetooth.yaml` (189), `snmp.yaml` (42) — 457 records
Harvest basis: IP Helper Reference 86×2 (+ICMP 10×2 folded), DNS Reference 32×2, IPv6 Application Development 35×2, OBEX Reference 58+57+48, Connection Manager Reference 31 (CE 6.0), GPS Intermediate Driver Reference 17 (CE 6.0), Bluetooth Reference 216+194+63, SNMP Reference 42×3 — 1,537 harvested pages.

## 1. Purpose and scope

The remaining documented networking/adjacent application areas: IP Helper (`iphlpapi.h` + `iprtrmib.h`/`iptypes.h`/`icmpapi.h`/`ipexport.h` — `GetIpAddrTable`, `GetIfTable`, route/ARP management, `IcmpSendEcho`), the DNS resolver API (`windns.h` — `DnsQuery` family), the IPv6 conceptual set (dual-stack guidance), OBEX (`obex.h`/`obexserver.h` — the COM-based Object Exchange contract: `IObex`, `IObexDevice`, `IHeaderCollection`…), Connection Manager (`connmgr.h` — `ConnMgrMapURL`-family + `CONNMGR_*` constants), the GPS Intermediate Driver (`gpsapi.h`/`gpsdev.h` — `GPSOpenDevice` family), the Bluetooth application surface (`bt_api.h`, `bthutil.h`, `ws2bth.h`, `bthsdpdef.h`, `btagpub.h` audio-gateway, `btdrt.lib`-bound set), and WinSNMP (`snmp.h`/`snmpexts.h`/`snmpapi.h`).

## 2. Dependencies

`winsock2.h` (ws2bth, dual-stack), `windows.h` (connmgr/gps), COM (`spec-ole-com.md`) for OBEX interfaces, `spec-winsock2.md` for the socket base.

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Structures | Interfaces | Constants/enums | Lib | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IP Helper | 96 | 56 | 34 | 1 | 5 enums (`IF_OPER_STATUS`, `IP_DAD_STATE`…) | iphlpapi.lib (56) | headers: iphlpapi.h 48, iprtrmib.h 19, iptypes.h 15, icmpapi.h 10 |
| DNS (`windns.h`) | 32 | 4 (`DnsQuery`…) | 28 (DNS_RECORD family) | — | — | dnsapi.lib (4) | introduced **5.0** — the whole documented DNS set is CE 5.0-era |
| IPv6 concepts (`ws2tcpip.h`) | 35 | — | — | — | — | — | conceptual/how-to pages; **the actual v6 functions (`getaddrinfo`, `freeaddrinfo`, `addrinfo`) are documented in the Winsock Reference and already closed by `spec-winsock2.md` (introduced 4.1)** |
| OBEX | 16 | — | 5 | 8 (`IObex`, `IObexDevice`, `IObexSession`?, `IHeaderCollection`…) | 1 enum | uuid.lib (8) | ce-only; `obexserver.h` subset |
| Connection Manager | 30 | 14 | 6 | — | 1 enum + `CONNMGR_*` | cellcore.lib (14) | ce-only; introduced 4.2 (29) |
| GPS ID | 17 | 4 (`GPSOpenDevice`, `GPSCloseDevice`…) | 2 | — | 3 consts + 3 enums | gpsapi.lib (4) | ce-only; **6.0 only**; `gpsdev.h` records (5) |
| Bluetooth | 189 | 89 | 33 | 4 | 24 consts + 3 enums | **btdrt.lib (59)**, btagsvc_* (21), bthutil.lib (2) | ce-only; headers: bt_api.h 68, **bt_ddi.h 41 (driver DDI)**, btagpub.h 30, winsock2.h 13, ws2bth.h 10, bthsdpdef.h 9 |
| WinSNMP | 42 | 36 | 6 | — | — | snmpapi.lib (29), snmp.lib (7) | 3.0-era; `snmpexts.h` is the extension-agent subset |

## 4. A/W and export-form notes

Wide-only everywhere documented (`GetIpAddrTable` generic, DNS `DnsQuery_W` semantics, OBEX/COM wide). Bluetooth SDP records use byte-arrays (no A/W dimension). `IcmpSendEcho`/`IcmpCreateFile` take narrow ANSI strings for hosts in the icmpapi subset on desktop — the CE pages document generic form; policy: resolve to W and note the icmp narrow-host anomaly for Role C.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0600` | GPS Intermediate Driver set (17); the CE 6.0-only bluetooth additions (16) |
| `_WIN32_WCE >= 0x0500` | DNS API (32), bluetooth 5.0 wave (42) |
| `_WIN32_WCE >= 0x0420` | ConnMgr (29), bluetooth 4.2 wave (53) |
| `_WIN32_WCE >= 0x0400` | bluetooth base wave (76), OBEX (14) |
| runtime SYSGEN | OBEX/BT/ConnMgr/GPS components are optional image features |

## 6. Implementation notes for Role B

1. **R-HDR-24**: `iphlpapi.h`/`iprtrmib.h`/`iptypes.h`/`ipexport.h`/`icmpapi.h` desktop-split kept; `windns.h`, `ws2tcpip.h`, `obex.h`+`obexserver.h`, `connmgr.h`, `gpsapi.h`+`gpsdev.h`, `snmp.h`(+`snmpexts.h`,`snmpapi.h`) standalone.
2. **R-HDR-25**: Bluetooth app headers: `bt_api.h`, `bthutil.h`, `ws2bth.h`, `bthsdpdef.h`, `btagpub.h` ship in the app set; **`bt_ddi.h` (41 records) is driver-DDI surface — excluded from the application include set** (registered, not deleted, consistent with fsdriver-excluded policy). Emit the exclusion list in the spec's addendum at header-generation time.
3. `MIB_*`/`IP_*`/`IF_*` constant values: iptypes/iprtrmib are in the audited w32api lineage — verified channel; `CONNMGR_*`, `BTH_*`, `OBEX_*`, `GPS_*` value-open (OQ-30/OQ-32) — no invented values.
4. OBEX interface records: vtable-comment emission; uuid.lib bindings recorded.
5. `btagsvc_network.lib`/`btagsvc_phoneext.lib` are the documented bindings for the audio-gateway extension set — third/fourth CE-specific bluetooth libraries; keep all four in the `.def` matrix (`btdrt`, `bthutil`, `btd`, `btagsvc_*`).
6. SNMP: `snmpexts.h` extension-agent records ride in `snmp.yaml` but gate as agent-side.

## 7. Closure statement

1,537 pages → 457 records. Exclusions: `bt_ddi.h` DDI (kept as records, excluded from app headers per R-HDR-25); the IPv6 conceptual pages resolve to no API (documented here to prevent re-harvesting). NAT is documented in `spec-coreos-extras.md` (Core OS area, not networking tree). Deferred to P4 roadmap: CellCore (675), NDIS/driver references, Network Utilities (44 — tool how-tos, no API).

## 8. Verification hooks

L2: `sizeof(MIB_IFTABLE)`-family fixed prefixes; `DNS_RECORD` layout; `CONNMGR_CONNECTIONINFO`. L3: `GetIpAddrTable` roundtrip; `DnsQuery` A-record; `IcmpSendEcho` loopback; GPS `GPSOpenDevice`/`GPSCloseDevice` on a GPSID image; `BthSetMode` on a BT image. Role C: OQ-30 (BTH_*), OQ-32 (GPS_*) value sweeps.
