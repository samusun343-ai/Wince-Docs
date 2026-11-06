# `.def` Generation Pipeline (Architecture)

Status: Normative (design) | Companion to `def-requirements.md`

## 1. Stages

```
[Stage 1] Inventory      data/mslearn-inventories/<set>/<area>.json
            │  page lists per documentation area (already delivered)
            ▼
[Stage 2] Requirements harvest (tools/harvest_facts.py, extended)
            │  per page: Header / Link Library / OS Versions / signature
            ▼
            data/mslearn-facts/<set>-<area>-facts.json
            ▼
[Stage 3] Dedup & merge (tools/build_defs.py — Phase 2)
            │  same function documented in CE5 + CE6 docsets:
            │    - identical requirements  ⇒ single record (union of evidence)
            │    - differing requirements ⇒ record both, flag for spec review
            ▼
[Stage 4] Emit            def/<lib>.def + def/<lib>.def.map (provenance sidecar)
            ▼
[Stage 5] Import libs     dlltool -d def/<lib>.def -l lib<lib>.a  (and .lib via lib.exe-class tool)
            ▼
[Stage 6] Verify          link conformance binaries; runtime GetProcAddress sampling (Role C)
```

## 2. Merge rules (Stage 3, normative)

* **M-1.** Function identity = documented generic name + resolved export form (A/W policy §2).
* **M-2.** Library conflicts between docsets (none observed between CE5/CE6 in the harvested set so far, but the design must handle it) are surfaced, not auto-resolved.
* **M-3.** A function documented under multiple areas (e.g. a GWES function appearing in both "Windows Reference" and "Dialog Boxes") is a single export; the sidecar keeps all doc pages.
* **M-4.** Pages documenting the *same* function for different CE versions keep the earliest `introduced`.

## 3. Sidecar format (`.def.map`, machine-readable JSON)

```json
{
  "library": "coredll",
  "exports": {
    "CreateFileW": {
      "doc_pages": [
        "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ee490417(v=winembedded.60)",
        "https://learn.microsoft.com/en-us/previous-versions/windows/embedded/aa517318(v=msdn.10)"
      ],
      "header": "winbase.h",
      "introduced": "1.0"
    }
  }
}
```

Every line of every `.def` is thus traceable to at least one official page (R-DEF-3).

## 4. Tooling constraints

* Deterministic output (sorted exports) so diffs are meaningful.
* No network access required at generation time beyond the already-harvested facts (facts are committed; re-harvesting is optional refresh).
* dlltool compatibility: plain `LIBRARY`/`EXPORTS` syntax only (no ordinals — R-DEF-2; no `DATA` unless a documented data export is ever recorded).

## 5. Cross-checks against the header specs

* Every function declared in a P0/P1 header spec MUST appear in exactly one `.def.map` (closure check in `tools/validate.py`, extended in Phase 2).
* Every `.def` export MUST have a declaration in some header spec (no orphan exports).
