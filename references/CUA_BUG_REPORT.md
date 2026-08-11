# cua-driver bug report — Windows background SendInput drops characters
# File at: https://github.com/trycua/cua/issues  (repo trycua/cua, libs/cua-driver)

## Title
cua-driver (Windows): background SendInput `type` silently drops characters/spaces on long strings (>~400 chars)

## Summary
On Windows, cua-driver's background text-input path (the `global_input` keyboard delivery used by `type` from clients like Hermes Agent) **silently drops characters and spaces when typing long strings**. Short strings commit fine; strings above roughly 400 chars lose spaces and occasional letters mid-stream, corrupting the committed value. No error is surfaced — the driver reports the type as delivered.

## Steps to reproduce
1. On Windows, connect a client (e.g. Hermes desktop) to `cua-driver`, driving a native Chrome window with a `contenteditable` or `<textarea>` (LinkedIn / Studio forms reproduce it).
2. `type` a string longer than ~400 characters containing spaces and an em-dash, via the background (non-foreground) delivery path.
3. Read back the committed field value.

## Observed input (excerpt)
> Falsifiable framework and methods for isolating an **AI's** reasoning machinery from its memorized content. The Separation Hypothesis: a transformer's logic (**the judge**) is separable from its factual data (the **witness**) ... **grokking**-circuit corroboration. Open source: **github.com/Godsend**/reasoning-core

## Observed committed value (drops marked)
> ... an **I's** reasoning machinery ... logic (**thejudge**) ... (the **witnes**), ... **grkking**-circuit corroboration. Open source: **github.comGodsend**/reasoning-core

Multiple independent losses on one string: `AI's` → `I's` (letter dropped), `the judge` → `thejudge` (space dropped), `witness` → `witnes` (letter dropped), `grokking` → `grkking` (letter dropped), `github.com/` → `github.com` (slash + spaces swallowed).

The identical full string committed **byte-perfect** via the CDP `Input.insertText` path, isolating the fault to cua-driver's SendInput delivery (not the page).

## Expected
Background `type` commits the full string faithfully, equal to foreground paste behavior.

## Actual
Characters and spaces dropped on long input; no error surfaced; agent believes typing succeeded.

## Environment
- cua-driver 0.19.2 (`install.ps1 -Release latest`)
- OS: Windows 10
- Target window class: `Chrome_WidgetWin_1`
- Delivery: background (no foreground swap)
- Client: Hermes Agent (Nous Research)

## Impact
Silent user-visible data corruption with no error — the agent commits wrong text believing it's right. In our case this produced multiple corrupted LinkedIn project descriptions that were only caught by re-reading committed field values, then deduping 4 duplicate project entries.

## Suspected cause
`libs/cua-driver` Windows keyboard backend — likely event pacing or string-chunking in the SendInput `global_input` loop that drops events on long, fast sequences. Related to #2084 (CDP insert_text falls through on Windows) and #2239 (text/keyboard delivery reliability).

## Labels
`bug`, `cua-driver`, `windows`
