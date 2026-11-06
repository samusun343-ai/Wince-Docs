# Fact Verification Policy

Status: Normative | Governs: how facts are recorded, cross-checked and marked

## 1. Fact record schema (normative)

Every fact lives in a machine-readable record (JSON under `data/mslearn-facts/`, YAML under `data/facts/`). Minimal normative fields:

```yaml
id: winnt-VER_PLATFORM_WIN32_CE        # unique, namespaced
kind: constant                          # constant | function | structure | macro | header | library | note
class: common                           # common | ce-modified | ce-only  (charter C-2)
status: verified                        # verified | verify-runtime | open | quarantine
introduced: "1.0"                       # earliest documented CE version (string; see §4 for encoding)
removed: ~                              # last CE version containing it, if any
value: "3"                              # for constants
definition: "VER_PLATFORM_WIN32_CE = 3" # canonical textual form
target_header: winnt.h
target_lib: ~                           # importing library, for functions
src:                                     # provenance: registry ids (+ optional fragment refs)
  - mslearn-ce60
  - mingw-org-w32api
  - msdn-mag-archive
notes: >-
  Free-form original-wording notes; attributed quotes allowed per cleanroom-policy R-2.
```

* `status` semantics:
  * `verified` — at least one Class A source states the fact (or one Class A + one Class B agree).
  * `verify-runtime` — value known only from Class B/community sources; Role C MUST confirm on-device before Phase 2 release.
  * `open` — value/behaviour not yet established; an entry MUST exist in `docs/06-appendix/open-questions.md`.
  * `quarantine` — contamination suspicion; see `roles.md` §4.

## 2. The two-channel rule

A fact reaches `verified` only through one of:

1. **Single official statement** — one Class A page explicitly states it (e.g. the CE 6.0 `System Errors` table states `ERROR_SUCCESS = 0`), **or**
2. **Independent agreement** — two sources of different classes agree (e.g. `VER_PLATFORM_WIN32_CE = 3`: MSDN Magazine article states the value; MinGW w32api defines it; CE docs define the struct field consuming it).

Same-class agreement (e.g. two community wikis) does **not** qualify.

## 3. Contradiction resolution

1. If two approved sources disagree, record both statements in `notes`, set `status: open`, and add an open question.
2. Prefer the source *specific to Windows CE* over desktop Win32 documentation (per charter C-2, CE-specific facts override common assumptions — e.g. `MAXIMUM_WAIT_OBJECTS` is referenced by CE docs but its *value* is only common knowledge; it is therefore recorded as `verify-runtime`, not `verified`).
3. Prefer the newer official docset for a CE-version-scoped fact (CE 6.0 docs supersede CE 5.0 docs for CE 6.0 behaviour; both are recorded when they differ — e.g. `WaitForMultipleObjects` link library: `coredll.lib`/`Nk.lib` in CE 5.0 docs vs `Nk.lib` in the CE 6.0 page harvested here; see `spec-winbase-core.md`).

## 4. CE version encoding in records

`introduced`/`removed` use the documented "OS Versions" wording from the Requirements block, normalised as: `1.0`, `1.01`, `2.0`, `2.01`, `2.1`, `2.11`, `2.12`, `3.0`, `4.0`, `4.1`, `4.2`, `5.0`, `6.0`. The compile-time macro `_WIN32_WCE` encoding is specified in `docs/04-architecture/versioning-gating.md`.

## 5. Citation format

* Fact records cite source registry ids in `src[]`.
* Audit records (and specs, where useful) cite full URLs with retrieval dates.
* Harvest scripts stamp `retrieved: YYYY-MM-DD` automatically.

## 6. Mechanical checks (enforced by `tools/validate.py`)

* Every `src[]` id exists in the approved registry.
* Every registry id has an audit file.
* No record has an empty `src[]`.
* Enumerated spec tables cross-check against the fact YAML/JSON (counts and ids).
* Placeholder scan: no `TODO`/`TBD`/`XXX`/`【…】` strings in delivered documents.
