# Reasoning Core — Paper Iteration Ledger

**Repo:** github.com/Godsend/reasoning-core (public, MIT code / CC-BY text)
**This folder:** Drive-shareable mirror of the paper lineage + iteration log.
**Last synced:** 2026-08-10 (commit `9663b51`)

---

## How to read this folder (file order)

| File | Version | What it is |
|---|---|---|
| `paper_v0.1.md` | v0.1 | Original Separation Hypothesis draft |
| `paper_v0.2.md` | v0.2 | Hypergraph-ledger rewrite (occluded ledger, separable reason) |
| `paper_v0.3.md` | v0.3 | **Current draft.** Adversarial-hardened: latency falsifier, epiplexity-after-purge test, Scarred Tissue objection, Contributions & Process |
| `v04_revision_plan.md` | v0.4 plan | 5 fixes from re_critique_v03: unique latency scaling law, MDL-transferability reframe, FFN purge, quantified regime boundary, **+ FIX 5: attribution-based edge extraction** |
| `v04_graph_extraction_section.md` | v0.4 draft §3.2 | New section: how to *induce* the hypergraph from a transformer (judge = data-invariant subgraph; digital NCC of the competency). Ready to merge |

**Reading order for a newcomer:** v0.1 → v0.2 → v0.3 (the current claim) →
v04_revision_plan (where it's going) → v04_graph_extraction_section (the
newest operational piece).

---

## Commit log (chronological, newest last)

| Commit | Date | What changed |
|---|---|---|
| `73c340a` | 2026-08-09 | Reasoning Core: Separation Hypothesis draft + NBLM synthesis pipeline |
| `8b28e71` | 2026-08-09 | Add poll script |
| `850a723` | 2026-08-09 | Fix NotebookLM audio download (auth-aware client; .m4a not .mp3) |
| `531b3c7` | 2026-08-09 | **v0.2:** hypergraph-ledger rewrite + preserve v0.1 |
| `14a111d` | 2026-08-09 | README: reflect v0.2 + generation scripts |
| `286e0dd` | 2026-08-09 | remove stray task-id file |
| `211d8ce` | 2026-08-09 | poll_artifacts.py: poll+download+transcribe (idempotent, 55min cap) |
| `977d3ec` | 2026-08-09 | CASY outreach draft (Jou / Prince-Hughes) — collaboration + arXiv endorsement |
| `9394f80` | 2026-08-09 | Synthesis findings (critique+debate) + artifact transcripts; gitignore media |
| `f26cddd` | 2026-08-09 | untrack media artifact |
| `acdc999` | 2026-08-09 | **v0.3:** adversarial-hardened — latency falsifier, epiplexity-after-purge, Scarred Tissue, Contributions |
| `768150a` | 2026-08-09 | Consensus epiplexity lit findings (7 refs incl. **Li 2026 anti-result**) + resynth script |
| `22ec80b` | 2026-08-09 | v0.4 plan from re_critique_v03 (4 rigor fixes) |
| `60ca472` | 2026-08-09 | Outreach letters READY (CASY + Levin cowrite + Bach + Jessica intro) |
| `7b61107` | 2026-08-09 | All artifacts + v0.3 re-synthesis transcripts (deepdive + critique) |
| `9663b51` | 2026-08-10 | **v0.4 §3.2 draft:** attribution-based edge extraction (judge = data-invariant subgraph; digital NCC) + FIX 5 wiring |

---

## Open questions (living list — append as they surface)

**Experimental / falsifier design:**
- [ ] Edge-extraction: what threshold θ and intersection ratio k/N make the
      "stable subgraph" claim robust vs. noise? Pre-register before running.
- [ ] Discretization defense: what *is* an edge in a transformer? (attention
      is dense — we induce the sparse graph via EAP/ACDC/SAE features; this
      modeling commitment needs its own section)
- [ ] Latency baseline isolation: how much of τ(π) is hardware friction vs
      topological rerouting? (Design answer: deltas + ordering fingerprint +
      substrate-swap stability — but needs concrete numbers)
- [ ] Does the extracted subgraph actually show small-world / scale-free
      topology (O(log n) rerouting), or is it closer to a redundant MLP
      (linear)? The divergent prediction.

**Theory / framing:**
- [ ] "Digital NCC of the competency" — is the NCC analogy load-bearing or
      decorative? Does it invite unfair consciousness baggage?
- [ ] MDL-transferability reframe (v0.4 FIX 2): judge = transferable
      epiplexity subset vs witness = domain entropy — does this survive
      contact with Finzi's reverse-order Lichess result?
- [ ] Regime boundary: can we make "SH holds within a regime" quantitative
      (perturbation complexity ≤ judge epiplexity) or is it still a
      get-out-of-jail card?

**Outreach / publication:**
- [ ] Which venue first? arXiv (Jou endorsement offered) vs conference.
- [ ] Letters to CASY / Levin / Bach / Jessica — sent? Follow-ups?
- [ ] Does the extraction protocol belong in the paper or a separate
      methods/preprint companion?

---

## Process notes (how this got fast)

- **Loop:** human (Gene) as audit-Judge + AI (Oryon/Hermes) + NotebookLM
  re-synthesis + Consensus lit map = adversarial Witnesses.
- **Each revision passes through** re-synthesis critique → 4-rigor-fix plan →
  implementation → commit → next critique. See `v04_revision_plan.md` for
  the current cycle's source.
- **Honesty rule:** falsifiable proposals only; null results get published;
  no data cooked to fit the theory. "Either it produces tangible results or
  leads, or it doesn't — iterate or move on. A published indexed paper has
  its own merits regardless."
