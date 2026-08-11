# Session handoff — Aug 11 2026 (launch day)

## What shipped today
1. **reasoning-core commits (all pushed):**
   - `21d7ca2` — launch batch: standard social post format, title card 1280, outreach letters complete
   - `9ff1631` — full 8-transcript corpus (critique/debate/deep-dive) in `references/transcripts/`
   - Trail: 43ebcd7 → 85e5a5a → 3e0e6c7 → 8318cde → 5a4f415 → 21d7ca2 → 9ff1631

2. **YouTube** — 6 Paper-A-batch videos published on @MachineOfLovingGrace:
   - tRUw2AH4TiY · s-9h4wsP2R0 · 4FIyBlPkAes · buyVYWb9i5o · uR4RElrx6uI · zKo3SqmgZ-I
   - (Also auto-published a Short: "How AI Separates Reasoning From Memory" = youtube.com/shorts/QCig_HM5gxU)

3. **X** — all 6 videos posted, verified (each redirected to /home = posted).

4. **LinkedIn** — 3 projects live on g0dsend profile, each 1 clean card:
   - reasoning-core: The Separation Hypothesis (498 chars, clean)
   - Mirror Mind: Longitudinal Personality Modeling (424 chars)
   - EILT: Emergent Informational Ledger Theory (391 chars)

5. **Full 8-transcript audio corpus** transcribed via cloud Whisper (whisper-1).

## Still open / blocked
- **LinkedIn 6 video posts** — composer is a hard SPA wall (synthetic CDP and computer_use foreground both fail to pierce the Start-a-post / compose modal). Content is copy-paste ready in `references/posts_launch_batch.md`. Manual paste needed.
- **Levin letter + CASY/Bach/Jessica** — armed, not yet sent (awaiting final go).
- **LFM2.5 350M candidate** — Gene tried on S25U LM Playground (90 tok/s, instant load) — notes it as a fine-tune candidate for Mirror-Mind edge node.

## Critical lessons (banked to memory)
- **Only CDP `Input.insertText` completes long strings char-perfect** on LinkedIn/Studio forms. The `computer_use` SendInput path drops chars/spaces on strings >~400 chars (AI's→I's, the judge→thejudge, grokking→grkking, github.com/Godsend→github.comGodsend).
- **Trusted `Input.dispatchMouseEvent`, not synthetic `.click()`** — LinkedIn React ignores element.click() but accepts trusted mouse events.
- **Always read back the field value before advancing** (this caught the corruption before publish).
- **The browser-exec session and the desktop-visible window can be different tabs** of the same Chrome — verify against the SAME tab the user sees, or you'll check the wrong render.
- **`/post/new/` on LinkedIn routes to the ARTICLE editor, not the post composer** — the post composer only opens from the feed's Start-a-post box.

## Bug report filed
- `references/CUA_BUG_REPORT.md` — ready to paste into https://github.com/trycua/cua/issues (repo trycua/cua, libs/cua-driver, v0.19.2). Title: "cua-driver (Windows): background SendInput `type` silently drops characters/spaces on long strings". Related: #2084, #2239. API filing failed (personal token lacks triage access to third-party repo) — needs manual paste by Gene.
