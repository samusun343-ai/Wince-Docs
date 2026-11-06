# Specification — `winsock2.h` / `ws2tcpip.h` / `ws2spi.h`

Status: final (Phase 1 core set) | Priority: P1 | Fact source: `data/facts/winsock.yaml` (202 records), page records `data/mslearn-facts/ce50-ce60-winsock-facts.json` (332 pages), error tables `ce{50,60}-winsock-errors.json`

## 1. Purpose and scope

The Windows Sockets 2 surface documented by the CE "Winsock Reference" + "Winsock SPI Reference": 131 function records, 28 structure/type records, 8 documented constant pages (`IPPROTO_*`, `SOL_*`), and the complete documented **Winsock error table (35 unique codes, values stated by the docs)**.

## 2. Dependencies

`windef.h`, `winnt.h` (error macros, `WSAAPI` calling convention). The CE winsock headers are self-contained w.r.t. the desktop `windows.h` chain.

## 3. Documented import-library map

| Library | Fn count | Notes |
| --- | --- | --- |
| `Ws2.lib` | 117 | **every** function page that documents a library states `Ws2.lib`, both docsets, identical CE 5.0 → CE 6.0 |
| *(none documented)* | 12 | structure/constant pages without Requirements library lines |

Runtime module: `ws2.dll` hypothesis (OQ-6); CE 4/5 devices also expose Winsock 1.1 (`winsock.dll`) for legacy apps — the project targets Winsock 2.2 (`MAKEWORD(2,2)` in the documented `WSAStartup` example).

Headers documented: `winsock2.h` (70 records), `ws2spi.h` (53), `ws2tcpip.h` (6). The w32api-lineage license exception applies (`winsock2.h` derives from BSD-licensed code — reuse requires the Regents/DEC attribution note; recorded in the mingw-org-w32api audit).

## 4. Functions (complete harvested set: 131 records)

* **Core BSD surface**: `accept`, `bind`, `closesocket`, `connect`, `getpeername`, `getsockname`, `getsockopt`, `htonl`, `htons`, `ioctlsocket`, `inet_addr`, `inet_ntoa`, `listen`, `ntohl`, `ntohs`, `recv`, `recvfrom`, `select`, `send`, `sendto`, `setsockopt`, `shutdown`, `socket`.
* **Winsock 2 additions**: `WSAStartup`, `WSACleanup`, `WSAGetLastError`, `WSASetLastError`, `WSACreateEvent`, `WSACloseEvent`, `WSASetEvent`, `WSAResetEvent`, `WSAWaitForMultipleEvents`, `WSAEventSelect`, `WSAEnumNetworkEvents`, `WSASocket`, `WSARecv`, `WSASend`, `WSARecvFrom`, `WSASendTo`, `WSAAccept`, `WSAConnect`, `WSADuplicateSocket`, `WSAIoctl`, `WSAAsyncSelect` *(absent — see §8)*.
* **Name resolution**: `gethostbyname`, `gethostname`, `getprotobyname/number`, `getservbyname/port`, `getpeername`; Winsock 2 name-space APIs `WSALookupServiceBegin/Next/End`, `WSASetService`, `WSAInstallServiceClass` (SPI-side), `WSAGetServiceClassInfo`.
* **SPI (`ws2spi.h`)**: the provider-facing `WSP*` (52: `WSPAccept`, `WSPBind`, `WSPCloseSocket`, `WSPConnect`, `WSPRecv`, `WSPSend`, `WSPSocket`, …) and `WPU*` (`WPUCreateSocketHandle`, `WPUCloseSocketHandle`, `WPUQuerySocketHandleContext`, …) sets, plus `NSP*` name-space provider functions. These belong in a separate `ws2spi.h` consumed only by transport vendors.

## 5. Structures (documented layouts)

`WSADATA`, `sockaddr`, `sockaddr_in`, `hostent`, `protoent`, `servent`, `fd_set`, `timeval`, `in_addr`, `LINGER`, `WSABUF`, `WSANETWORKEVENTS`, `WSAPROTOCOL_INFO`, `WSAQUERYSET`, `WSASERVICECLASSINFO`, `AFPROTOCOLS`, `BLOB` — verbatim layouts in the YAML. Note: the CE `hostent` page documents the classic 4-member layout (`h_name`, `h_aliases`, `h_addrtype`, `h_length`, `h_addr_list` via `char FAR* FAR*`); `SOCKADDR_IRDA` has no page (IrDA constants only, §6).

## 6. Constants and IrDA (CE-specific surface)

Documented constant pages: `IPPROTO_IP`, `IPPROTO_TCP`, `IPPROTO_UDP`, `IPPROTO_RAW` (CE 6.0 page only), `SOL_SOCKET`, `SOL_IRLMP` (CE-only level — IrDA is a first-class CE transport), `_DSCP_TRAFFIC_TYPE` (CE 6.0 only). Values from the w32api lineage (`IPPROTO_TCP 6`, `IPPROTO_UDP 17`, `SOL_SOCKET 0xffff`, `SOL_IRLMP 0xff`) recorded `verify-runtime`. The full socket option families (`SO_*`) are P2 constant harvests.

## 7. Winsock error codes (documented values — Class A)

The "Winsock Error Codes" page states value tables (identical in CE 5.0 and CE 6.0; 37 rows, 35 unique — the page repeats `WSAEISCONN` and `WSAETIMEDOUT`): `WSAEINTR 10004`, `WSAEACCES 10013`, `WSAEFAULT 10014`, `WSAEINVAL 10022`, `WSAEMFILE 10024`, `WSAEWOULDBLOCK 10035`, `WSAEINPROGRESS 10036`, `WSAEALREADY 10037`, `WSAENOTSOCK 10038`, `WSAEDESTADDRREQ 10039`, `WSAEMSGSIZE 10040`, `WSAEPROTOTYPE 10041`, `WSAENOPROTOOPT 10042`, `WSAEPROTONOSUPPORT 10043`, `WSAESOCKTNOSUPPORT 10044`, `WSAEOPNOTSUPP 10045`, `WSAEPFNOSUPPORT 10046`, `WSAEAFNOSUPPORT 10047`, `WSAEADDRINUSE 10048`, `WSAEADDRNOTAVAIL 10049`, `WSAENETDOWN 10050`, `WSAENETUNREACH 10051`, `WSAENETRESET 10052`, `WSAECONNABORTED 10053`, `WSAECONNRESET 10054`, `WSAENOBUFS 10055`, `WSAEISCONN 10056`, `WSAENOTCONN 10057`, `WSAESHUTDOWN 10058`, `WSAETIMEDOUT 10060`, `WSAECONNREFUSED 10061`, `WSAEHOSTDOWN 10064`, `WSAEHOSTUNREACH 10065`, `WSAEPROCLIM 10067`, `WSASYSNOTREADY 10091`, `WSAVERNOTSUPPORTED 10092`, `WSANOTINITIALISED 10093` — all `verified` (documented value tables, both docsets). `WSAEAGAIN`-style aliases and the extended `WSA_E_*` codes are not documented (P2 cross-check against the desktop winsock2 docs).

## 8. A/W and CE-specific notes

* `WSAAsyncSelect` has **no page** in the CE 5.0/6.0 docsets (window-message async I/O is not the CE model — CE documents `WSAEventSelect` instead). The header set MUST NOT reference `WSAAsyncSelect` without a Role C confirmation (recorded as a `verify-runtime`-class absence; OQ-19).
* Documented remark (accept page): "ATM is not supported in Microsoft Windows CE" — IrDA replaces it as the CE-specific transport.
* Sockets are `SOCKET` (unsigned) on CE as on desktop; `INVALID_SOCKET`/`SOCKET_ERROR` values from the w32api lineage (`verify-runtime`).

## 9. Open items forwarded

* OQ-19 *(new)*: complete `SO_*`/`IP_*`/`TCP_*` option-value harvest + `WSAAsyncSelect` absence confirmation on-device.
* OQ-20 *(new)*: `WSAPROTOCOL_INFO`/`WSAQUERYSET` member-level CE deltas (pages harvested; detailed diff at P2).
