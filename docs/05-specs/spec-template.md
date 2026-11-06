# Per-Header Specification Template (normative)

Every header specification in `docs/05-specs/` MUST follow this template. The template is what makes the suite an engineering specification rather than prose: each item row is backed by a fact record, each fact record is machine-checkable, and the closure against the documentation inventory is explicit.

## 1. Document skeleton

```markdown
# Specification — <header>.h

Status: draft|review|final | Priority: P0|P1|P2 | Fact source: data/facts/<file>.yaml

## 1. Purpose and scope
(what belongs in this header, what does not)

## 2. Dependencies
(include DAG position; which headers this one includes/consumes)

## 3. Enumeration
(the complete item table; columns below)

## 4. A/W and export-form notes
(per-function export-form deviations from generic naming)

## 5. Version gates
(items whose presence is version-conditional, with gate expressions)

## 6. Implementation notes for Role B
(normative instructions: guard names, packing, ordering, prohibited patterns)

## 7. Closure statement
(mapped documentation areas + page counts; explicit list of anything deliberately excluded)

## 8. Verification hooks
(which L2 static assertions / L3 runtime probes this header generates)
```

## 2. Enumeration table columns

| Column | Meaning |
| --- | --- |
| Item | Identifier as documented |
| Kind | `type` / `macro` / `constant` / `function` / `structure` / `handle-type` … |
| Definition | Canonical definition text (functional, factual) |
| Class | `common` / `ce-modified` / `ce-only` (charter C-2) |
| CE versions | `introduced`–`removed` (from documented "OS Versions") |
| Sources | `src[]` registry ids (must resolve) |
| Status | `verified` / `verify-runtime` / `open` |

## 3. Fact record schema (YAML, `data/facts/`)

As defined in `docs/01-methodology/verification-policy.md` §1. Additionally, per-kind fields:

```yaml
kind: constant      -> value, target_header
kind: macro         -> definition, target_header
kind: type          -> definition, target_header        # e.g. "typedef unsigned long DWORD;"
kind: structure     -> members[] (name, type, note), size, packing, target_header
kind: function      -> signature, export, target_header, target_lib, params_differ_from_win32
```

## 4. Closure rule

A header spec is **final** only when every page of its mapped documentation areas (per `header-inventory.md`) is either represented by ≥1 fact record or listed in an explicit "excluded" table with reason (e.g. driver-only OAL APIs excluded from the application header set).

## 5. Quality gates

1. `tools/validate.py` passes (schema, source resolution, id uniqueness, spec↔fact count agreement).
2. No `open` items without an entry in `docs/06-appendix/open-questions.md`.
3. Every `ce-modified`/`ce-only` item cites its Class A evidence.
