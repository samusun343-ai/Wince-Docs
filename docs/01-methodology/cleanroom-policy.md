# Clean-Room Policy

Status: Normative | Scope: all repositories and roles of this project

## 1. Objective

Guarantee that the deliverable (`include/` + `def/` for Windows CE) can be distributed without violating any license or copyright, by ensuring no Microsoft-copyrighted or otherwise restricted *expression* flows into it, and that all *facts* flow through documented, license-clean channels.

## 2. Fact vs. expression

* **Facts** — API names, calling signatures, numeric constant values, structure member names/types/order, library bindings, OS-version availability, and documented behavioural differences. Facts are not copyrightable; this project collects them aggressively, with citation.
* **Expression** — prose, comments, file organisation as a creative whole, macros' stylistic formulation, documentation text. Expression of others MUST NOT be reproduced.

Rules:

* R-1. Fact records MAY contain a verbatim signature or constant definition, because a C declaration or `#define` needed for interoperability is functional/factual.
* R-2. Prose excerpts from Class A sources are limited to short attributed fragments (≤ ~25 words per fragment, ≤ 3 fragments per record) used to evidence a technical claim. Whole paragraphs MUST be summarised in original wording instead.
* R-3. Code reuse is permitted **only** from audited Class B assets, with per-file attribution; the audit trail in `docs/02-sources/audits/` is mandatory.
* R-4. If a Class B file mixes licenses (e.g. MinGW w32api's `winsock2.h` carries BSD/DEC-copyrighted portions), the stricter license governs that file and the implementation role MUST be told explicitly in the spec.

## 3. Prohibited inputs (non-exhaustive but decisive)

| Prohibited input | Why |
| --- | --- |
| Windows CE / Embedded **Shared Source** (any variant, incl. the Shared Source Premium and academic licenses) | License restricts use to debugging/learning; it is not an information source for this project (user directive; see audit `rejected-shared-source.md`) |
| Platform Builder, eVC, VS SDK **headers and libs** | Microsoft-copyrighted, EULA-restricted |
| GitHub repos that mirror the above (SDK header dumps, "wince headers" collections without provenance) | Unauthorized redistribution of Microsoft material |
| CHM/HTML mirrors of MSDN content republished by third parties without permission | Unauthorized redistribution; use MS Learn or Wayback Machine snapshots of the original URLs instead |
| Export lists scraped from ROM dumps with no documentation cross-check | Provenance cannot be established from approved sources (see `def-requirements.md` for the compliant method) |

## 4. Boundary cases

* **Wayback Machine snapshots** of `msdn.microsoft.com` / `learn.microsoft.com` pages: permitted, because the content is Microsoft's own publication at a public URL, archived; cite both the original URL form and the snapshot.
* **Internet Archive MSDN Library CD images** (for CE 1.x/2.x-era docs not online): permitted as an offline reading source; facts extracted still carry the MSDN Library identity as citation. Not yet used in Phase 1 (open question OQ-9).
* **pinvoke.net**: Class D — facts may be cross-checked there, but nothing may be copied from it (license status unverifiable; see audit).
* **Decompilation / disassembly** of Microsoft binaries: prohibited outright (EULA + legal risk). Runtime behavioural probing on owned hardware is the compliant alternative (see `verification-policy.md`).

## 5. Practical workflow for adding a fact

1. Confirm the source is in the approved registry; if not, run the source admission procedure (`source-policy.md` §3) first.
2. Extract the fact into a schema-valid record with `src[]` referencing registry IDs and `retrieved` dates.
3. Classify it (`common` / `ce-modified` / `ce-only`) per charter C-2.
4. Where the value is only known from a Class B asset or community source, mark `status: verify-runtime` so Role C will confirm it on-device.

## 6. Review gates

* Every PR touching `data/` or specs MUST state which sources were consulted. Reviewers reject changes that cite unregistered sources.
* `tools/validate.py` enforces that every `src[]` resolves to the registry and every registry entry has an audit file — mechanical traceability is part of the definition of done.
