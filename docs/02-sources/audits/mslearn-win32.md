# Audit — MS Learn desktop Win32 docs, MSDN Magazine archive, lifecycle pages

Registry ids: `mslearn-win32`, `msdn-mag-archive`, `mslearn-lifecycle`
Retrieved / verified: 2026-11-07

## 1. `mslearn-win32` — desktop Win32 API documentation

* Location: `https://learn.microsoft.com/en-us/windows/win32/` (live, maintained).
* Relevance: per charter C-2, the Win32-**common** subset of the CE surface (names, signatures, constant values shared with desktop). CE-specific facts always take precedence (see `verification-policy.md` §3).
* Verified example: the desktop docs are the only official place where e.g. `MAXIMUM_WAIT_OBJECTS`' numeric value (64) is stated for the desktop platform — on CE docs the constant is *referenced* but not *valued*, so CE-side adoption is recorded as `verify-runtime` rather than `verified`.
* License: publicly accessible Microsoft documentation; same fact-citation basis as the CE docs (MS Learn Terms of Use).
* **APPROVED (Class A)** — restricted to the common subset; CE docsets override on conflict.

## 2. `msdn-mag-archive` — MSDN Magazine archive on Microsoft Learn

* Location: `https://learn.microsoft.com/en-us/archive/msdn-magazine/…` (official archive; pages carry an "archived content" notice).
* Verified, relevant items:
  * *"Mobilize: Explore The New Features In Windows Embedded CE 6.0"* (December 2006, Paul Yao) — `https://learn.microsoft.com/en-us/archive/msdn-magazine/2006/december/mobilize-explore-the-new-features-in-windows-embedded-ce-6-0` — CE 6.0 kernel/architecture facts (e.g. the redesigned kernel, shared-source-based implementation discussion).
  * *"Windows CE .NET: New Version Offers Revamped Platform"* (July 2002) — `https://learn.microsoft.com/en-us/archive/msdn-magazine/2002/july/windows-ce-net-new-version-offers-revamped-platform-builder-improved-tools-enhanced-api-and-source-code` — CE .NET 4.0-era facts; notably documents the author's method of comparing Platform Builder DEF files (historical context for the `.def` requirements; **not** a method this project may copy, since PB DEFs are restricted material — see `rejected-sources.md` R-2).
  * *"Pocket PC: Seamless App Integration…"* (June 2001) — contains an explicit statement of `dwPlatformId == 3` for Windows CE (`VER_PLATFORM_WIN32_CE`), used as Class A cross-evidence in `spec-winnt.md`.
* **APPROVED (Class A)**.

## 3. `mslearn-lifecycle` — product lifecycle pages

* Location: `https://learn.microsoft.com/en-us/lifecycle/products/…` (verified live: `windows-embedded-ce-60`, `windows-ce-50`).
* Use: version dating only (e.g. CE 6.0 GA 2006-11-30, end of support 2018-04-10). No API facts.
* **APPROVED (Class A)** for dating facts in `ce-version-history.md`.
