# Reasoning Core — Paper Iteration Ledger

**Repo:** github.com/Godsend/reasoning-core (public, MIT code / CC-BY text)
**This folder:** Drive-shareable mirror of the paper lineage + iteration log.
**Last updated:** 2026-08-11
**Current draft:** `paper_v0.4_PaperA.md`

> **Canonical terminology (frozen 2026-08-11).** The framework is
> **Emergent Informational Ledger Theory (EILT)**. Use that exact string
> everywhere — paper, repo, site, abstracts, correspondence. Superseded
> variants that appear in older files and should be corrected on sight:
> "Emergent Integrated Layered Theory," "Informational Ledger Theory (ILT),"
> "Ego-Intentional Latent Topology," and the bare handle
> "Persistence-Closure Hypergraph Framework" used as a synonym for EILT.
> (Persistence-closure hypergraph is fine as a *description of the model*;
> it is not an alternative name for the theory.)

---

## The split (decided 2026-08-10)

The work is now two papers. Mixing them was halving the credibility of both.

| | Scope | Status |
|---|---|---|
| **Paper A** | Attribution intersection + the Separation Hypothesis, as an ML methods paper. No ontology, no cosmology. | `paper_v0.4_PaperA.md` — current, ready for Consensus pass |
| **Paper B** | The EILT / persistence-closure hypergraph framework. | Parked. Publish after Paper A lands. Source material is v0.2 and v0.3. |

Paper A is deliberately killable by a reviewer. That is the point.

---

## File map

| File | Version | Status |
|---|---|---|
| `paper_v0.4_PaperA.md` | **v0.4** | **CURRENT.** Paper A. Depth-based falsifier, interpretability citations, Sophontic withdrawn, ontology removed. |
| `EXTERNAL_REVIEW_v03_20260810.md` | — | External review that produced v0.4. Read second. |
| `EXTERNAL_REVIEW_ADDENDUM_search_and_claims_20260810.md` | — | Search surface, domain architecture, claim propagation. |
| `paper_v0.3.md` | v0.3 | **SUPERSEDED.** Historical. Contains the broken wall-clock latency falsifier. Do not send or cite. |
| `paper_v0.2.md` | v0.2 | Historical. Source material for Paper B. |
| `paper_v0.1.md` | v0.1 | Historical. Contains the withdrawn Sophontic citation. |
| `v04_revision_plan.md` | plan | Historical. FIX 1–5; FIX 1 as written was wrong (see below). |
| `v04_graph_extraction_section.md` | draft | ⚠️ **SUPERSEDED — DO NOT MERGE AS-IS.** See merge hazard below. |
| `outreach_letters_SEND.md` | — | Letters. Hold until Paper A is pushed. |
| `levin_podcast_reference.md` | — | **Internal aid only. Do not send to Levin.** |

**Reading order for a newcomer:** `paper_v0.4_PaperA.md` → external review → addendum. The v0.1–v0.3 lineage is provenance, not the current claim.

---

## ⚠️ Merge hazard — read before touching the extraction section

`v04_graph_extraction_section.md` is superseded by Paper A §4 (protocol) and §6.2 (falsifier). It still contains the **wall-clock latency framing that Paper A explicitly removed**:

- §3.2.3 — "then measure τ(π): the rerouting cost," including the parametric form τ(e) = τ₀ + α λ(e)⁻¹e^(βB(e)) + γh(e)
- §3.2.5 point 3 — "Latency tracks structure, not token count or hardware state"

**Why it's wrong:** a transformer's forward pass is a fixed sequence of operations. Ablating a component does not lengthen it, add layers, or change FLOP count. There is no dynamic rerouting to be slow. Wall-clock differences measure cache locality and kernel scheduling — hardware noise. The graph-search intuition is biological and does not transfer to fixed-depth inference.

**Replacement (already in Paper A §6.2):** depth-to-convergence — the layer index at which the correct answer first becomes linearly decodable from the residual stream (logit lens / tuned lens). Internal, per-input, hardware-independent, and defined whether or not the output is correct. Secondary instrument: reasoning-token count before answer stabilization under CoT. Wall-clock retained only as a noise control.

**Action:** merge nothing from this file into Paper A except §3.2.0, which is not yet in Paper A and should be — see below.

---

## Pending merge into Paper A: the §3.2.0 motivation

`v04_graph_extraction_section.md` §3.2.0 is the strongest paragraph in the bundle and has no equivalent in Paper A. It motivates the protocol with the same-lineage blind-spot finding and frames intersection as that failure inverted: *we refuse to trust any edge that only one data instantiation supports.* This turns the intersection threshold from an arbitrary parameter into a principled one.

Merge it as a new **§4.0** in Paper A, immediately before "§4.1 The problem the protocol solves." Strip the EILT reference; keep the empirical framing.

---

## Commit log (chronological, newest last)

| Commit | Date | What changed |
|---|---|---|
| `73c340a` | 2026-08-09 | Separation Hypothesis draft + NBLM synthesis pipeline |
| `8b28e71` | 2026-08-09 | Add poll script |
| `850a723` | 2026-08-09 | Fix NotebookLM audio download (auth-aware client; .m4a) |
| `531b3c7` | 2026-08-09 | v0.2: hypergraph-ledger rewrite + preserve v0.1 |
| `14a111d` | 2026-08-09 | README: reflect v0.2 + generation scripts |
| `286e0dd` | 2026-08-09 | remove stray task-id file |
| `211d8ce` | 2026-08-09 | poll_artifacts.py: poll+download+transcribe |
| `977d3ec` | 2026-08-09 | CASY outreach draft (Jou / Prince-Hughes) |
| `9394f80` | 2026-08-09 | Synthesis findings + artifact transcripts; gitignore media |
| `f26cddd` | 2026-08-09 | untrack media artifact |
| `acdc999` | 2026-08-09 | v0.3: adversarial-hardened |
| `768150a` | 2026-08-09 | Consensus epiplexity lit findings (7 refs incl. Li 2026 anti-result) |
| `22ec80b` | 2026-08-09 | v0.4 plan from re_critique_v03 |
| `60ca472` | 2026-08-09 | Outreach letters drafted |
| `7b61107` | 2026-08-09 | All artifacts + v0.3 re-synthesis transcripts |
| `9663b51` | 2026-08-10 | v0.4 §3.2 draft: attribution-based edge extraction |
| *(pending)* | 2026-08-11 | **v0.4 Paper A + external review + addendum + ledger rewrite** |

---

## Corrections log

Kept visibly rather than silently edited, per the honesty rule.

| Date | Correction |
|---|---|
| 2026-08-10 | **Sophontic AI citation withdrawn** (v0.1 ref [2]) and the 60×–1000× claims removed, including as "unverified motivation." No released model, no eval kit, no paper, no third-party benchmark; claims appear only on company marketing material. Replaced with Mirzadeh et al., GSM-Symbolic — which was the correct citation for the perturbation paradigm all along. Documented in Paper A §7.3. |
| 2026-08-10 | **Wall-clock latency falsifier retracted** and replaced with depth-to-convergence. The original could not measure what it claimed in a fixed-depth architecture. |
| 2026-08-10 | **Missing interpretability literature added** — Geva et al. (FFN key-value memories), Meng et al. (ROME/MEMIT), Olsson et al. (induction heads), Elhage et al. (circuits), Conmy et al. (ACDC), Syed et al. (EAP), Belrose et al. (tuned lens). The judge/witness framing landed in a populated field the earlier drafts did not cite. |
| 2026-08-10 | **"Digital NCC" framing cut** — decorative, and imported consciousness baggage the method does not need. |
| 2026-08-11 | **EILT expansion frozen** to "Emergent Informational Ledger Theory." Four variants had entered circulation across the repo, the site, and search summaries. |
| 2026-08-11 | **[VERIFY 1] arXiv endorsement: v1's claim was RIGHT.** The Jan 21, 2026 policy update closed the institutional-email-only path ("arXiv will no longer accept institutional email addresses... as the sole qualifier"). New submitters need institutional email AND prior authorship in the endorsement domain, OR personal endorsement. Paper A (cs.LG) → Marc Finzi is the correct endorser ask, not Roger Jou. |
| 2026-08-11 | **[VERIFY 2] Family timeline reconciled.** Thirteen years was the *sentence* (1980), not the time served — Gorbachev's amnesty freed Victor Yanenko in 1987; family transited Vienna → Ladispoli → Brooklyn 1990. Levin letter opening restored with dated specifics. Canonical record: `references/family_chronology.md`. |

---

## Open questions (living list)

**Extraction protocol:**
- [ ] What θ and k/N make the stable-subgraph claim robust vs. noise? Pre-register before running. Report the full stability curve; a sharp knee vs. smooth decay is itself a result (Paper A §4.3).
- [ ] Discretization: an edge in a transformer is a modeling commitment, not a given. EAP/ACDC/SAE features induce the sparse graph — this needs to survive a reviewer asking "why is that the right graph?"
- [ ] Does the extracted subgraph show small-world topology (O(log n) depth growth) or redundant-MLP behaviour (linear)? The divergent prediction.
- [ ] Control-edge matching criteria: same layer, same head count, low betweenness, high redundancy. Needs to be specified precisely enough that a critic cannot claim the controls were chosen to fail.

**Theory:**
- [ ] Does the MDL-transferability reframe survive contact with Finzi's reverse-order Lichess result, or does it lean on it too hard?
- [ ] Is the regime conjecture (perturbation description length ≤ judge description length) measurable in practice, or still a get-out-of-jail card?

**Publication:**
- [ ] **Endorsement route.** arXiv endorsement is category-specific — an endorser must have published in that archive. Paper A targets cs.LG. Roger Jou (Yale Child Study Center) can plausibly endorse q-bio, almost certainly not cs.LG. Correct ask is Marc Finzi or another cs.LG-published author. *Verify current arXiv endorsement policy directly before asserting anything about it in correspondence.*
- [ ] Zero-barrier venues to run concurrently: Zenodo (instant DOI, timestamps priority), OpenReview public preprint, LessWrong/Alignment Forum crosspost.
- [ ] Letters: hold until Paper A is pushed and is the repo's front door.

---

## Process

**Loop:** human (Gene) as auditing judge + AI (Oryon/Hermes) as generator + NotebookLM re-synthesis + Consensus lit map as adversarial witnesses. Each revision: critique → fix plan → implementation → commit → next critique.

**Honesty rules (standing):**
- Falsifiable proposals only.
- Null results get published with the same prominence as positive ones.
- No data excluded post hoc to fit the hypothesis.
- Withdrawn claims are marked as withdrawn, not deleted. See the corrections log.
- Thresholds and ablation protocols are published before running.

*"Either it produces tangible results or leads, or it doesn't — iterate or move on."*
