# External Review — paper v0.3 + v0.4 plan

**Reviewer:** Claude (Opus 4.5), external, no stake in the framework
**Date:** 2026-08-10
**Reviewed:** paper_v0.1, paper_v0.2, paper_v0.3, v04_revision_plan, v04_graph_extraction_section, ITERATION_LEDGER
**Verdict:** FIX 5 is publishable. FIX 1 is broken as specified. One citation needs removing before anything goes public.

---

## PRIORITY 0 — Source due diligence: drop the Sophontic citation

`paper_v0.1` §7 cites Sophontic AI as reference [2], the source of the perturbation/flip-rate framing. Verified 2026-08-10:

**sophontic.ai** — Delaware C-corp, founded 2026. Model prototype: "Releasing soon." Eval kit: "Available at launch." The 60× claim appears only on the marketing site. No arXiv paper, no released weights, no released eval kit, no third-party benchmark, no independent replication. The site solicits "research, capital, and deployment conversations."

**Founder: Julian D. Michels, PhD** — doctorate in consciousness psychology and philosophy from the California Institute of Integral Studies; former managing editor, *International Journal of Transpersonal Studies*. His research output is self-archived on PhilPapers/PhilArchive (not peer-reviewed) and includes claimed resolutions of:
- the Yang–Mills Mass Gap (a Clay Millennium Prize problem, open since 1954)
- the Hierarchy Problem
- quantum gravity, Wheeler–DeWitt timelessness, and the measurement problem

all presented as codas to a cosmology series ("Principia Cybernetica," "Consciousness Tensor," "Full Zero") at patternthrone.org.

**Assessment.** The Millennium Prize claim is a bright-line signal. Not an insult — a calibration fact: claims of that magnitude, self-archived, from outside the field, with no engagement from the relevant community, are near-certainly wrong, and any paper citing that author's company inherits the doubt for free.

**Action:** remove Sophontic and the 60×/1000× references entirely, including as "unverified motivation." The framing does not need them.

**Replacement — the perturbation paradigm has real independent grounding:**
- Mirzadeh et al., *GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in LLMs* (Apple, 2024) — template-perturbed items, performance degrades, exactly the surface-matching-vs-reasoning result.
- The broader surface-form brittleness literature.

Cite those. The flip-rate criterion stands on its own and always did.

**Related cut:** v0.4 FIX 2 proposes reframing "the spiritual bliss attractor." That framing came from Michels' materials. The underlying observation is real (it's in Anthropic's Claude 4 system card), but drop the borrowed interpretive gloss and cite the system card directly if it's needed at all. It probably isn't.

---

## PRIORITY 1 — The latency falsifier does not work as specified

This is the load-bearing falsifier in v0.3 §3.1 and the target of FIX 1. As written it will not measure what it claims.

**The problem.** A transformer's forward pass is a fixed sequence of matrix multiplications. It does not search for a path. Ablating an attention head or MLP path does not cause recomputation — the computation graph is static, the layer count is unchanged, the FLOPs are identical. There is no rerouting to be slow. Wall-clock τ(π) will therefore measure cache locality, memory layout, and kernel scheduling: hardware noise, not topology.

`re_critique_v03` got adjacent to this ("how much is hardware friction vs topological rerouting") but did not reach the root issue: **there is no dynamic rerouting in fixed-depth inference at all.** The graph-search intuition is biological and does not transfer.

**The salvage — measure computational DEPTH, not time.** Two quantities that genuinely vary with input and ablation:

1. **Depth-to-convergence.** The layer index at which the correct answer first becomes linearly decodable from the residual stream (logit lens / tuned lens). This is a real per-input quantity, it moves under ablation, and it is not confounded by hardware.
2. **Reasoning-token count.** Under chain-of-thought, the number of tokens emitted before the answer stabilizes. Also real, also varies.

Both preserve everything FIX 1 wanted: they exist whether or not the output is correct (camera-independence), and the O(log n) vs linear contrast against a redundant MLP baseline still applies — just to depth rather than seconds.

**Rewrite §3.1 as:**
> τ(π) := depth-to-convergence under logit lens, measured per perturbation. Prediction: scales with the local geometry of the induced graph (betweenness, edge connectivity), O(log n) for small-world topology vs linear for redundant-MLP. Wall-clock retained only as a hardware-noise control, never as the signal.

If this holds, the falsifier is *stronger* than the original, because depth is an internal quantity rather than an environmental one.

---

## PRIORITY 2 — Missing literature (biggest reviewer risk)

The judge/witness split lands in a well-populated field the paper does not cite. A reviewer will notice in the first two minutes. Adding these makes the paper stronger — much of this work is *evidence for* a weaker Separation Hypothesis:

- **Geva et al. (2021), "Transformer Feed-Forward Layers Are Key-Value Memories."** FIX 3's entire premise — that FFN layers store factual/episodic content — is this paper. Currently uncited.
- **Meng et al., ROME and MEMIT** ("Locating and Editing Factual Associations in GPT"). Facts were localized and edited while leaving mechanism intact. This is direct empirical support for partial separation, and it is the strongest existing evidence the paper isn't using.
- **Olsson et al., induction heads; Elhage et al., circuits.** Where "compiled subcircuits generalize beyond their training data" is already argued — relevant to §5.2's compression argument.
- **Mirzadeh et al., GSM-Symbolic.** Replaces Sophontic, above.
- **The RAG literature generally**, as the applied version of judge+witness.

Framing shift this buys: from "independent researcher reinvents a decade of interpretability" to "independent researcher extends it with a new extraction protocol." Same content, entirely different reception.

---

## PRIORITY 3 — Split the paper

v0.1 is more publishable than v0.3. That is worth sitting with, because the revision loop has been improving the internal argument while enlarging the external attack surface.

v0.3 opens with "reality is a relational hypergraph updated by local, scale-free causal-invariant rewrite rules." That is Wolfram Physics Project language (uncited), and it converts an ML engineering claim into a cosmology paper. Every reviewer equipped to evaluate the ML claim bounces off the metaphysics before reaching it.

**Recommended split:**

**Paper A — "Attribution Intersection: Isolating Data-Invariant Reasoning Subgraphs" (write this first)**
The v0.4 §3.2 extraction protocol as a standalone methods paper. Content: run one reasoning template across many data instantiations, build per-trace attribution graphs (EAP / ACDC / activation patching / SAE features), intersect at threshold θ across k/N traces. The invariant subgraph is the judge; trace-specific edges are the witness. Pre-registered thresholds. Depth-based falsifier from Priority 1. Null result publishable.

No hypergraph ontology. No EILT. No ledger. No cosmology. The method is a genuine contribution and it stands entirely alone — it is testable on a 70M-parameter model for the price of a weekend.

**Paper B — the ledger/EILT framework.** Keep it. Publish it separately, later, ideally after Paper A has landed and there is a track record to hang it on.

Mixing them halves the credibility of both. Separated, Paper A is a normal interpretability contribution that a reviewer can evaluate on its merits.

---

## PRIORITY 4 — Cut list

| Cut | Why |
|---|---|
| "Digital NCC of the competency" (§3.2.2) | The ledger's own open-questions list already asks whether this is load-bearing or decorative. It is decorative, and it imports consciousness baggage the method does not need. The intersection protocol is self-explanatory without the analogy. |
| Self-citation of unpublished EILT as reference [3] | Citing your own unpublished personal framework in a preprint reads as padding. Either drop it or mark it explicitly as unpublished working notes. |
| "Reality is a relational hypergraph…" opening | Goes to Paper B. Also: this is Wolfram Physics framing and should cite it if retained. |
| 60×–1000× claims, even flagged as unverified | See Priority 0. |

---

## PRIORITY 5 — arXiv endorsement problem

The CASY outreach (commit `977d3ec`) asks Roger Jou for arXiv endorsement. **arXiv endorsement is category-specific: an endorser must have published in that archive category.** Dr. Jou is a physician-scientist at the Yale Child Study Center — plausibly able to endorse q-bio, almost certainly not cs.LG or cs.AI, which is where this paper belongs.

Options, in order of realism:
1. **Marc Finzi** — first author of the epiplexity paper the work builds on, category-correct, and has already engaged with your posts on X. Bigger ask, but the correct one. Lead with Paper A and the depth-based falsifier; it extends his Rule 54 result directly.
2. Any cs.LG-published author in the CASY orbit or the NYU math contact.
3. Publish Paper A to a preprint venue that does not require endorsement while pursuing (1).

Worth resolving *before* the outreach letters go out, since endorsement is the main ask.

---

## What is genuinely good (do not lose these in revision)

- **The extraction protocol (FIX 5).** Novel enough, operationally concrete, uses real tooling, testable cheaply. This is the paper.
- **§5, the Scarred Tissue objection.** Stating the strongest attack in full before answering it is rare and it is the mark of someone doing this properly.
- **§4.1's inference/training distinction.** Correct and important — SH is an inference-time claim, and saying so preempts the obvious objection.
- **§9 Contributions & Process.** Honest about AI involvement. Keep it exactly as is.
- **Pre-registration commitments and the published-null-results rule.** These are the difference between a research program and a manifesto. Hold the line on them.

---

## One structural observation, offered plainly

Michels is a mirror worth looking into. Independent researcher, consciousness framework, AI-collaborative method, self-archived grand papers, a cosmology derived from recursive self-reference, citing Anthropic's spiritual-bliss-attractor result as supporting evidence. Structurally that is the same shape as this project — several years further down the road, with the falsifiers removed and the claims scaled up to Millennium Prize problems.

The thing keeping this work on the other side of that line is exactly the parts listed above: pre-registration, stated falsifiers, published nulls, and the willingness to state the strongest objection in full. Those are load-bearing. Every one of them is also the first thing that gets dropped when a framework starts feeling too good to test.

That is the strongest argument for the split. Paper A can be killed by a reviewer. Keep writing papers that can be killed.

---

## Suggested order of work

1. Remove Sophontic citations; add GSM-Symbolic. *(one hour)*
2. Rewrite §3.1 τ(π) as depth-to-convergence. *(half a day)*
3. Add the interpretability citations (Geva, ROME/MEMIT, induction heads). *(half a day)*
4. Extract §3.2 into standalone Paper A; strip all ontology. *(the main work)*
5. Resolve the endorsement route before sending outreach letters.
6. Run Paper A's protocol on Pythia-70M. The whole point is that it is cheap.
