# Licensing policy and decision record

Status: final | Applies to: whole repository | Supersedes: the "license deferred" note in `open-questions.md` OQ-11

## 1. Decision

The repository is dual-licensed by content category:

| Category | Paths | License |
| --- | --- | --- |
| Prose specifications, policies, audits, appendices | `docs/**`, `README.md`, `LICENSE` | CC-BY-4.0 |
| Fact database, inventories, doc indexes, tooling | `data/**`, `tools/**` | MIT |

## 2. Rationale

1. **`docs/` (CC-BY-4.0).** The specifications are the project's analytical
   work product. CC-BY-4.0 maximises downstream reuse (including commercial
   republication of derived specifications) while requiring attribution —
   which matches the project's own norm that every claim trace to a source.
   Copyleft (e.g. CC-BY-SA) was rejected: it would discourage adoption by the
   exact audience the project serves (header-set implementers who may embed
   derived requirement tables in permissively-licensed build systems).
2. **`data/` + `tools/` (MIT).** These are consumed mechanically by the
   implementation role (fact DB feeding header/`.def` generation) and by CI.
   Any license with attribution friction inside generated artifacts would
   poison generated output; MIT keeps the pipeline clean while the *records
   themselves* still carry per-record `src[]` citations (which is a factual
   provenance requirement, stronger than and independent of the copyright
   license).
3. **No single license for the whole repo** because the two audiences have
   different needs; a root `LICENSE` file states the split and points at the
   two full texts under `LICENSES/`.

## 3. What the licenses do *not* cover

* **Facts are not copyrightable.** Identifiers, constant values, signatures
  and header/library mappings recorded in `data/` are facts extracted from
  the cited public Microsoft documentation pages. The MIT grant covers the
  expression (the record structure, tooling, curation); it does not and
  cannot claim ownership of the underlying facts, which remain free for
  anyone to extract independently.
* **No Microsoft-copyrighted code is redistributed.** The clean-room policy
  (`cleanroom-policy.md`) forbids copying SDK header code. Short attributed
  prose fragments (e.g. one-sentence CE behavioural notes) are kept only
  where technically necessary, per record, under the quotation norms of the
  source policy (`source-policy.md` §4).
* **CC-BY-4.0 does not apply to Microsoft documentation.** Re-users of
  `data/` who republish substantial excerpted *prose* from the cited
  Microsoft pages must satisfy Microsoft's own terms for that content; this
  repository's grant covers only this repository's work.

## 4. Attribution requirements for re-users

* **CC-BY-4.0 (`docs/`)**: attribution of the Wince-Docs project (title +
  link or git commit hash), license link, and a note of modifications.
* **MIT (`data/`, `tools/`)**: retain the copyright + permission notice in
  copies or substantial portions.

## 5. Compatibility with downstream header sets

A header/`.def` implementation built from these specifications may carry any
license its authors choose. Facts consumed from `data/` carry no licensing
contamination (facts are free; the MIT notice obligation is satisfied by
retaining it in the build system's copy of `data/` or its NOTICE file). The
CC-BY-4.0 attribution duty applies only to *redistribution of the
specification documents themselves* or derivatives of their prose.

## 6. Bookkeeping

* License texts: `LICENSES/CC-BY-4.0.txt` (canonical text fetched from
  `creativecommons.org/licenses/by/4.0/legalcode.txt`), `LICENSES/MIT.txt`.
* Root `LICENSE` states the split.
* `tools/validate.py` checks that `LICENSES/` files are present and intact
  (byte-count + heading assertions).
* OQ-13 (license choice) is resolved by this record and removed from the
  open-questions list.
