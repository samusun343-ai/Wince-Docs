# Glossary

| Term | Meaning |
| --- | --- |
| **A/W** | The desktop Win32 convention of exporting ANSI (`A`) and Unicode (`W`) variants of text APIs. Windows CE is Unicode-native and only partially follows this convention (`unicode-aw-policy.md`) |
| **AYGShell** | "Aygshell" — the PocketPC-era shell extension API (`aygshell.h`, `aygshell.lib`, `SHCreateMenuBar` etc.) |
| **Class (fact)** | Classification of every fact: `common` (identical to desktop Win32), `ce-modified` (same name, CE-specific delta), `ce-only` (no desktop counterpart) |
| **coredll** | `coredll.dll` / `coredll.lib` — the single dominant CE system library binding most of the Win32-equivalent surface |
| **FSD** | Installable File System Driver (FSD Manager); source of `ReadFileWithSeek`-family CE-only APIs |
| **GWES** | Graphics, Windowing and Events Subsystem — the CE window manager/graphics stack (`winuser`/`wingdi` surfaces) |
| **HLBASE / IABASE** | Headless vs GUI base OS configurations in CE platform documentation |
| **Message Queue (point-to-point)** | CE-specific `msgqueue.h` API (`CreateMsgQueue` etc.) |
| **Object store** | CE's RAM-based compressed file/registry database (pre-6.0 semantics; documented in `CreateFile` remarks) |
| **PB** | Platform Builder — Microsoft's (license-restricted) OS build toolchain; rejected source |
| **RAPI** | Remote API — desktop-side functions (`Ce*`) calling into a connected CE device |
| **Shared Source** | Microsoft's restricted source-availability program for CE; rejected source (audit `rejected-shared-source.md`) |
| **ToolHelp** | CE process/memory snapshot API (`toolhelp.h`) |
| **w32api** | MinGW.org's public-domain Win32 header set; the lineage CeGCC borrowed for CE (`mingw-org-w32api` audit) |
| **ws2** | CE's Winsock import library (`Ws2.lib`), distinct from the desktop's `Ws2_32.lib` |
