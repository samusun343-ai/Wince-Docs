# Audit — Windows CE Shared Source (REJECTED)

Registry id: — (rejected; see `rejected-sources.md` R-1)
Reviewed: 2026-11-07, following explicit project directive

## 1. What was reviewed

The existence and licensing nature of Microsoft's "Shared Source" program for Windows CE (Windows CE 5.0 / Windows Embedded CE 6.0 Shared Source, incl. the Premium variants), as offered through Platform Builder and MSDN.

## 2. Evidence examined (from approved channels only)

* The CE 6.0 official documentation describes Shared Source strictly as an OS-design modification/debugging mechanism: "Using Shared Source Code in an OS Design" (`https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ee482553(v=winembedded.60)`, retrieved 2026-11-07), with sibling pages "Locating Shared Source Code" (`ee482109`), "Compiling Modules Containing Both Public and Shared Source Files" (`ee482618`), "Debugging Shared Source Code" (`ee482321`).
* The MSDN Magazine CE .NET overview (July 2002, Learn archive) characterizes the license similarly: source is provided "to help you learn about Windows CE and to help you debug your systems"; the license agreement restricts what may be built and shipped from it.
* The Windows Embedded CE 6.0 feature article (December 2006, Learn archive) discusses the CE 6.0 shared-source-based implementation in the same frame (learning/debugging, non-commercial kernel building).

## 3. Assessment

"Shared Source" is **not open source**: the licenses restrict use, do not grant redistribution rights for competing SDK material, and reading it for the purpose of producing a redistributable API definition set would create exactly the contamination this project exists to avoid.

## 4. Decision

**REJECTED as an information source in any form** — no reading, quoting, deriving, or "orientation" use by any project role. Facts must come from the approved Class A/B channels; anything only knowable from Shared Source is out of scope until documented officially.
