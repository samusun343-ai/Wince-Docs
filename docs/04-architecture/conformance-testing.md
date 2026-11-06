# Conformance Testing Strategy (for the Phase 2 implementation)

Status: Normative (requirements for the implementation's test suite) | Author of tests: Role B/C

## 1. Test levels

### L1 — Compile-matrix (host, no target required)

* Every generated header MUST compile standalone and via `windows.h`, for each `_WIN32_WCE` in {0x0400, 0x0410, 0x0420, 0x0500, 0x0600}, with strict flags (`-Wall -Wextra -Werror -std=c99` and a C++ pass).
* Compilers: any desktop GCC/Clang in 32-bit mode (syntax/semantic level; the OS headers are target-agnostic C), plus a CE-targeting compiler as available (CeGCC front ends are permissible *as test compilers* — they are open-source tools, and using them to compile does not import their code).

### L2 — Static assertions (compile-time fact verification)

The fact DB's `verified` values are asserted directly:

```c
/* generated from data/facts/winnt.yaml */
_Static_assert(VER_PLATFORM_WIN32_CE == 3, "winnt-VER_PLATFORM_WIN32_CE");
_Static_assert(MAXIMUM_WAIT_OBJECTS == 64, "winnt-MAXIMUM_WAIT_OBJECTS [verify-runtime]");
typedef char assert_osversioninfo_size[sizeof(OSVERSIONINFO) == 544 ? 1 : -1]; /* per fact record */
```

* Every P0 fact with a value generates one assertion; `verify-runtime` facts assert too but are additionally probed at L3.

### L3 — Runtime verification on real CE images (Role C)

* Environment: owned CE 4.x / 5.0 / 6.0 devices or legally obtained emulator images. (Platform Builder's emulator itself is restricted software; using an already-licensed installation for *testing* is a user-side licensing matter, noted here for completeness — no PB material enters the header set.)
* Probes (behaviour-only, no source comparison):
  * `sizeof`/offset checks of documented structures vs. the on-device compiler's results;
  * `GetProcAddress(GetModuleHandle(L"coredll.dll"), ...)` presence sampling for every `.def` export (record presence/absence per OS image — resolves OQ-2/OQ-6);
  * `GetVersionEx` → assert `dwPlatformId == 3`, `dwMajorVersion` matches the image, cross-checked against the toolchain's predefined `_WIN32_WCE` (resolves OQ-1 empirically);
  * calling-convention probe on x86 CEPC (OQ-3);
  * error-code sampling: call documented failing APIs (e.g. `CreateFile` on a nonexistent path → `ERROR_FILE_NOT_FOUND == 2`).
* Results flow back as **verification reports** (never as values into headers) — mismatches become open questions for Role A (roles.md §3).

### L4 — Link and smoke tests

* A conformance binary per priority area: process/thread, memory, sync, file I/O, Winsock, GWES smoke (create window + message loop), linking against the generated import libraries.

## 2. Regression policy

* The test suite lives in the implementation repository and is required for its CI.
* Any spec change in this repository MUST list the L1/L2 test deltas it implies (validator cross-checks fact ids ↔ assertion tags).

## 3. Explicitly out of scope

* Comparing generated headers against Microsoft SDK headers (prohibited channel, `cleanroom-policy.md` §3).
* Performance/compatibility testing of CeGCC itself.
