# Audit — pinvoke.net

Registry id: `pinvoke-net`
Retrieved / verified: 2026-11-07

## 1. Identity

* `https://www.pinvoke.net/` — "the interop wiki": user-contributed P/Invoke signatures, constants and structures for calling unmanaged APIs from managed code (FlexWiki engine, per page metadata `Product name: FlexWiki, version 1.3.0.101`).
* Directly relevant content: the module list includes **`coredll`**, **`aygshell`**, and `ipaqutil` — i.e. Windows CE-specific modules exist alongside the desktop ones (`kernel32`, `user32`, …).

## 2. License investigation (negative result)

Checked on 2026-11-07:

* site homepage HTML — no license/terms statement found;
* FAQ page (`/default.aspx/misc/FAQ`) — no license terms in the extractable content;
* a content page (`/default.aspx/user32/MessageBox`) — only wiki editing links, no license footer.

No machine- or human-readable content license could be located. The site is user-contributed with no visible contribution-terms page.

## 3. Assessment

* **Facts** (a constant's value, a signature's shape) are not copyrightable and may be cross-checked against pinvoke.net like any community reference.
* However, per the project's source policy (unverifiable licensing ⇒ restricted) and the two-channel rule (`verification-policy.md` §2), pinvoke.net **cannot be a sole source** for any fact, and **no content may be copied** from it (no quoting enum tables, no reusing its struct comment blocks).

## 4. Usage rules for this project

1. Cross-check channel only; every pinvoke.net-consulted fact still requires an approved Class A/B anchor.
2. No `src: [pinvoke-net]` as sole entry on any `verified` record; it may appear alongside official anchors or on `verify-runtime` records as a hint.
3. Never reproduce its text.

## 5. Conclusion

**APPROVED as Class D (restricted, cross-check only).**
