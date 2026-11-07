# Specification — Security: Cryptography, Certificates, SSPI, Smart Card, Credential Manager, LASS

Status: final (P3 harvest batch) | Priority: P2 | Fact sources: `data/facts/wincrypt.yaml` (203), `sspi.yaml` (52), `winscard.yaml` (31), `credman.yaml` (16), `lass.yaml` (19) — 321 records
Harvest basis: Security areas, three docsets — Cryptography Reference 118×2 (+ce40 crypt subset), Certificates Reference 85+83, Credential Manager Reference 16+16, Smart Card Reference 32+32, Authentication Services Reference 52+51, LASS Reference 19+11 — 799 harvested pages.

## 1. Purpose and scope

The complete documented CE security application surface: CryptoAPI (`wincrypt.h`: CSP functions `CPAcquireContext`…, `CryptAcquireContext` family, hashing, key exchange), the certificate store API (`Cert*` family, also `wincrypt.h` on CE — no separate `crypt32` header split), SSPI (`sspi.h`: `AcquireCredentialsHandle`, `InitializeSecurityContext`, `QueryContextAttributes` …), WinSCard smart-card resource manager (`winscard.h`), the CE Credential Manager (`credui.h`/`credmgr.h`: `CredRead`-family + `PromptForCredentials` dialog), and the CE-only Local Authentication Subsystem (`lass.h`: `LapInit`, `LAP-Exported Functions` set).

## 2. Dependencies

`windef.h`, `winnt.h` (`SECURITY_*` descriptors are CE-truncated — see A/W notes), `windows.h` for `credui.h` dialog types.

## 3. Enumeration by family (counts post-merge)

| Family | Records | Functions | Structures | Lib binding | Notable CE facts |
| --- | --- | --- | --- | --- | --- |
| Cryptography (`wincrypt.h`) | 203 | 128 (43 `Crypt*`/`CP*` + 85 `Cert*`) | 70 (CRYPTOAPI_BLOB, CERT_CONTEXT, CRYPT_*DESC…) | crypt32.lib (90), coredll.lib (35) | `Cert*` classified `common` (desktop-shared); CSP (`CP*`) is provider-side; introduced mostly 2.1/3.0, later waves 4.0/5.0 |
| SSPI (`sspi.h`) | 52 | 30 | 21 (SecHandle, CredHandle, SecBuffer…) | secur32.lib (19), **ntlmssp.lib (10)** | CE SSPI subset; `SEC_E_*`/`SEC_I_*` values already closed in `spec-winerror.md` |
| Smart Card (`winscard.h`) | 31 | 28 | 3 | winscard.lib (28) | `SCARD_*` constants symbolic (no numeric in CE docs) — OQ-30 class |
| Credential Manager | 16 | 11 | 2 | coredll.lib (8), secur32.lib (3) | documented headers credui.h + credmgr.h; 4.0 base, 5.0 additions |
| LASS (`lass.h`) | 19 | 17 (incl. LAP-Exported Functions) | 1 | coredll.lib (4) | **ce-only** subsystem (5.0) — whole area gated |

## 4. A/W and export-form notes

Wide-only at the boundary (`LPCWSTR` names, wide `CERT_NAME_BLOB` strings). SSPI package names (`NEGOSSP_NAME`, `MICROSOFT_KERBEROS_NAME`) are wide constants. Smart-card reader names wide. No A-variants documented anywhere in this area.

## 5. Version gates

| Gate | Items |
| --- | --- |
| `_WIN32_WCE >= 0x0500` | LASS (whole), Credential Manager 5.0 additions, later crypt records (12× 5.0, 2× 6.0) |
| `_WIN32_WCE >= 0x0400` | crypt 4.0 wave (23) |
| `_WIN32_WCE >= 0x0420` | SSPI 4.2 records (19) |
| per-record | bulk 2.1/3.0 |

SSPI shows the second-largest Nkstub-family adjacency (`ntlmssp.lib` direct binding) — no CE5→CE6 binding flips recorded here.

## 6. Implementation notes for Role B

1. **R-HDR-19**: keep the desktop split — `wincrypt.h` (crypto + certificates, CE does not use a separate crypt32 header naming), `sspi.h` (with `security.h` umbrella including it, desktop-compatible), `winscard.h`, `credui.h` + `credmgr.h` (both CE-documented), `lass.h` (ce-only standalone).
2. `CALG_*`, `PROV_*`, `KP_*`, `PP_*` constants: symbolic definitions from the w32api lineage where present, else value-open (Role C probes); `szOID_*` are string constants — emit as `#define szOID_… L"…" **only** when the CE page states the OID string (recorded per-record).
3. Structures are pointer-heavy; static-assert `sizeof(CERT_CONTEXT)`, `sizeof(SecBuffer)`, `sizeof(SCARD_READERSTATE)` on 32-bit.
4. CSP (`CP*`) functions are the provider contract — declare under a `WCE_CSP` gate comment; application headers need them for custom CSP authors.
5. LASS: whole-subsystem gate `_WIN32_WCE >= 0x0500` + runtime `LapInit` presence check documented in the header comment.

## 7. Closure statement

799 pages → 321 records (docset merge incl. ce40 crypt subset for 4.x differentiation). Nothing excluded: no internal/driver surface in this area (smart-card *driver* reference 40 pages is the `smclib`/WCSMDD surface — outside the application set, recorded in the inventory as excluded-by-area, consistent with the FSD treatment of `spec-database-storemgr.md` §6).

## 8. Verification hooks

L2: `sizeof` battery; `SEC_E_*` numeric equality vs `spec-winerror.md`. L3: `CryptAcquireContext`/`CryptReleaseContext` roundtrip with the default CSP; `CertOpenStore`/`CertCloseStore`; `SCardEstablishContext` on a smart-card image; LASS gated probe.
