# Role Separation (Clean-Room Organization)

Status: Normative | Applies to: all project roles and all phases

## 1. Purpose

This project enforces classic clean-room separation so that the future header implementation is provably free of license contamination. Roles are separated by **what they are allowed to read**, and information flows in one direction only.

## 2. Roles

### Role A — Researcher / Specification writer (operates this repository)

* **Produces:** source audits, documentation indexes, fact records, normative specifications.
* **May read:** any *approved* source (Class A fact sources, Class B permissive code for analysis, Class C structural references, Class D restricted wikis for cross-checking).
* **Must not:** copy expressive content (prose, comments, layout) from Class A sources beyond short attributed factual excerpts; read rejected sources (Class R) even for "orientation"; use rejected material to correct or complete facts.

### Role B — Implementer (future, operates the header repository)

* **Produces:** the actual `include/` and `def/` trees.
* **May read:** this repository (specs + fact DB) **and** the approved permissive code assets named in `docs/02-sources/approved-sources.md` (MinGW.org w32api public-domain parts, after audit).
* **Must not:** consult MS SDK headers, Platform Builder, Windows CE Shared Source, unauthorized GitHub mirrors of any of these, or any Class D source, while writing implementation code. If an implementation question is not answerable from the specs, the implementer **MUST** file a specification defect in this repository instead of looking elsewhere.

### Role C — Verifier (future, optional but recommended)

* **Produces:** conformance and runtime verification reports.
* **May:** run generated headers/tests against real CE devices or emulators and compare *behaviour* (runtime values, exported symbol resolution, `sizeof`, layout offsets) — behaviour comparison, not source comparison, is the untainted verification channel.
* **Must not:** feed rejected-source-derived *expected values* into the specification. A verification mismatch is recorded as an open question and resolved by Role A through approved sources.

## 3. Information flow

```
Approved sources (Class A/B/C/D)
        │  (Role A: extract facts, cite, classify)
        ▼
This repository: specs + fact DB (the ONLY input)
        │  (Role B: generate include/ + def/)
        ▼
Header implementation
        │  (Role C: runtime/behaviour verification)
        ▼
Verification reports ──► open questions ──► back to Role A
```

The flow is strictly one-way. Findings that flow backwards (from verification to specification) MUST enter through Role A, which resolves them using approved sources only.

## 4. Contamination handling

If any contributor discovers that a fact or text in this repository may derive from a rejected source:

1. Mark the record `status: quarantine` immediately (fact schema supports this).
2. Open an issue documenting the suspicion.
3. Role A re-establishes the fact from an approved source or deletes it.
4. The quarantine is lifted only with a new `src[]` provenance chain.

Records that cannot be re-established are deleted, and dependent specs are updated in the same change.
