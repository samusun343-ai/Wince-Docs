# Rejected Sources

Status: Normative | These MUST NOT be consulted by any project role (see `cleanroom-policy.md` §3)

## R-1. Windows CE Shared Source (all variants: Shared Source, Shared Source Premium, academic licenses)

* **What:** the source subset shipped with Platform Builder / offered for kernel and driver debugging ("Windows CE 5.0 Shared Source", "Windows Embedded CE 6.0 Shared Source").
* **Evidence of its nature:** the CE 6.0 documentation itself documents Shared Source as a license-restricted mechanism for modifying/debugging OS designs ("Using Shared Source Code in an OS Design" — `learn.microsoft.com/en-us/previous-versions/windows/embedded/ee482553(v=winembedded.60)`, retrieved 2026-11-07); contemporary MSDN coverage describes the license as permitting learning/debugging and non-commercial kernel building, not reuse in competing redistributable SDK material.
* **Decision:** rejected as an information source in any form (reading, quoting, deriving). *Explicitly confirmed by project directive.*

## R-2. Platform Builder / eMbedded Visual C++ / Visual Studio device SDKs (headers, libraries, import libs)

* **What:** Microsoft's proprietary SDK material (`.h`, `.lib`, `.def` shipped with PB/eVC/VS/standalone SDKs such as Pocket PC / Smartphone SDKs).
* **Why rejected:** Microsoft-copyrighted and EULA-restricted; the classic contamination channel for "wince headers".
* **Consequence:** no fact in this project may be sourced from SDK headers. Where a value is only known this way in the wild, the fact is marked `verify-runtime` and confirmed behaviourally on devices instead.

## R-3. Unauthorized mirrors of Microsoft SDK material on GitHub & elsewhere

* **What:** repositories containing dumps of Windows CE SDK headers, Platform Builder trees, or "all wince headers" collections.
* **Why rejected:** unauthorized redistribution of Microsoft-copyrighted material; provenance unverifiable; legally unsound to derive from.
* **Note:** this does **not** include permissively-licensed OSS that happens to interoperate with WinCE (e.g. CeGCC component repos, which are aggregate GPL/liberal-licensed works of their own).

## R-4. Third-party re-publishers of MSDN documentation (CHM mirrors, doc scrapers)

* **What:** sites/GitHub repos redistributing Microsoft's compiled Help or scraped HTML for CE 4.x/5.0/6.0.
* **Why rejected:** unauthorized redistribution. The same content is available from the publisher (MS Learn previous-versions, or Wayback snapshots of the original MSDN URLs) — those are the approved channels (`wayback-msdn`).

## R-5. Reverse-engineered internals without official documentation

* **What:** undocumented export lists, ordinal maps, or struct layouts circulating without documentation provenance.
* **Why rejected:** EULA/legal risk and unverifiable provenance.
* **Compliant alternative:** derive export lists from the documented `Link Library` requirements (see `def-requirements.md`) and verify behaviourally on-device (`verification-policy.md`).

## R-6. Anything of unverifiable origin

Per project directive: sources whose origin cannot be confirmed are not adopted. This includes anonymous paste-site dumps, forum attachments, and dead-project code with no license file.
