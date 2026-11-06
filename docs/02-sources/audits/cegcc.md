# Audit — CeGCC

Registry id: `cegcc`
Retrieved / verified: 2026-11-07

## 1. Identity

* `http://cegcc.sourceforge.net/` — "The CeGCC project: cross compile for Windows CE". A GCC/binutils-based cross toolchain aggregation targeting Windows CE (ARM), with two front ends: `arm-wince-cegcc-*` (Unix-like layer) and `arm-wince-mingw32ce-*` (MinGW-style).
* Components live in SVN (`svn.code.sf.net/p/cegcc/code/trunk`); GitHub mirrors exist (`svn2github/cegcc`, component repos such as `jkoan/cegcc-w32api`, `MaxKellermann/cegcc-build`).

## 2. What this project adopts from CeGCC — its *sources*, not its code

Per project directive ("we want something separate from CeGCC, but adopt the information sources CeGCC used"), the following CeGCC-documented facts define our adopted lineage:

1. **Header provenance.** CeGCC's own documentation (`http://cegcc.sourceforge.net/docs/details.html`) states:
   > "A target include file is an include file, in our case **borrowed from the MinGW project's w32api module**, which our compiler uses to know things about the target environment."

   ⇒ CeGCC's header source = MinGW.org w32api (public domain, audited at `mingw-org-w32api.md`). This project adopts the same anchor.
2. **Microsoft documentation** as the behavioural reference (same as our Class A).
3. **Toolchain conventions** documented in `details.html`, relevant to our versioning/A-W specs:
   * predefined macros of the two front ends (`__CEGCC__`, `__MINGW32CE__`, `__COREDLL__`, `UNICODE`/`_UNICODE` "Windows CE is a Unicode platform", `UNDER_CE`, `_M_ARM`, …);
   * `_WIN32_WCE` usage note: *"a device that runs a version of CE that identifies itself as 4.20.0, would match with a value of 0x0420 or lower"* — the BCD-style encoding evidence used in `versioning-gating.md`;
   * `_WIN32_IE` legacy-dependency note (their fix: headers should not require it on CE);
   * linker version fields (`--major-subsystem-version 4 --minor-subsystem-version 20` for CE 4.20) — input to the PE header conformance requirements.

## 3. License posture of CeGCC itself (why it is not a code source here)

* `http://cegcc.sourceforge.net/docs/license.html` describes an **aggregation**: GPL-family licenses on the toolchain components (which never end up inside developed applications), original licenses of each aggregated piece, and "the most liberal license we can apply" for CeGCC-authored additions (per-file statements).
* This project is **not a CeGCC fork** and does not copy CeGCC-authored code. The CeGCC-maintained w32api *lineage* is consumed only through its audited upstream anchor (MinGW.org w32api) and its documented facts.

## 4. Conclusion

**APPROVED as a reference (adopted-sources + toolchain-behaviour documentation).** Not a code source.
