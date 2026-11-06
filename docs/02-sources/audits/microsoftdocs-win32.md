# Audit — MicrosoftDocs/win32 GitHub repository

Registry id: `microsoftdocs-win32`
Retrieved / verified: 2026-11-07

## 1. Identity

* Repository: `https://github.com/MicrosoftDocs/win32` — the public source repository ("public mirror for win32-pr") of the desktop Win32 API documentation on MS Learn; content lives under `desktop-src/`. As of the audit date: 13,136 commits, 65 branches, actively maintained.

## 2. License evidence (verified directly)

* `https://raw.githubusercontent.com/MicrosoftDocs/win32/main/LICENSE` (HTTP 200 on both `main` and `master`) contains the **Creative Commons Attribution 4.0 International** legal code.
* Repository metadata additionally marks code snippets as **MIT** (the standard Microsoft Docs dual-marking: prose CC-BY-4.0, sample code MIT).

## 3. Assessment for this project

* **Permitted:** extraction of facts (signatures, constant values, structure layouts for the desktop-common subset) under CC-BY-4.0 with attribution — this is the machine-readable channel for the same content as `mslearn-win32`, and its license is explicit, which makes it the *preferred* citation for desktop-common facts that appear in repo form.
* **Not permitted:** presenting its content as our own, or misrepresenting attribution.
* Scope limitation per charter C-1/C-2: **desktop-common subset only**; anything Win64-specific or conflicting with CE docs is out of scope / overridden.

## 4. Conclusion

**APPROVED (Class A)** — the explicit CC-BY-4.0/MIT marking makes this the cleanest channel for desktop-common Win32 facts.
