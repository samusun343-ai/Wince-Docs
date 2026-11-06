# Windows CE Version History (collection-range context)

Status: informational | Sources cited per row

| Version | Date (evidence) | Notes relevant to this project |
| --- | --- | --- |
| CE 1.0 | 1996 (handheld PCs) | First release; Unicode-native; `PegGetVersionEx` naming remnant noted in CE docs RAPI page ("When writing applications for Windows CE 1.0 and 1.01, use the PegGetVersionEx function") |
| CE 1.01 / 2.0 / 2.01 | 1997 | `WaitForMultipleObjects` documented availability "CE 1.01 and later" |
| CE 2.1 / 2.11 / 2.12 | 1998–1999 | docs index on Learn retains a "Windows CE 2.1" landing stub (`dn467909`); wait-object-type gaps documented ("CE 1.0 through 2.12 do not support waiting for semaphores, change notification objects, input, and timers") |
| CE 3.0 | 2000 | docs partially live as orphan pages (`msXXXXXX`); Pocket PC 2000/2002 based on CE 3.0 (MSDN Mag, July 2002); `dwPlatformId == 3` evidenced (MSDN Mag, June 2001) |
| CE .NET 4.0 | announced 2002 (MSDN Mag July 2002: "Windows CE .NET" platform revamp) | documentation partially live (6,362 pages); per-function availability fields frequently say "Windows CE .NET 4.0 and later" |
| CE 4.1 / 4.2 | 2002–2003 | 4.2 used by later Pocket PC-era devices; `_WIN32_WCE = 0x0420` encoding evidence (cegcc docs) |
| CE 5.0 | GA 2004-05 (lifecycle: `learn.microsoft.com/en-us/lifecycle/products/windows-ce-50`, verified live) | full docs live (22,889 pages); target platform |
| CE 6.0 | GA 2006-11-30 (lifecycle `windows-embedded-ce-60`); R2 (2007), R3 (2009) | redesigned kernel (MSDN Mag Dec 2006); full docs live (23,713 pages); target platform |
| Compact 7 / 2013 | 2011 / 2013 | out of target scope; docs indexed for context (20,286 / 16,863 pages) |

Support-end dating (lifecycle pages): CE 5.0 and CE 6.0 are both past end of support — one more reason a clean, redistributable header set must not depend on SDK availability.
