# Occluded Ledger, Separable Reason: An Epiplexity-Grounded Hypergraph Account of the Judge/Witness Split

**Status:** Preprint draft (v0.3 — adversarial-hardened)
**Date:** 2026-08-10
**Author:** Gene Yanenko. **Analysis/synthesis co-research:** Oryon (Hermes agent) +
ClawHoarde + NotebookLM synthesis pipeline. See §9 Contributions & Process.
**Version note:** v0.3 integrates the two falsifiers surfaced by adversarial NBLM
synthesis (latency-based circularity break; epiplexity-after-purge test) and
adds a dedicated section confronting the strongest objection (the Scarred
Tissue argument). Prior: paper_v0.1, paper_v0.2.

---

## Abstract

We unify two apparently separate results — the epiplexity measure of structural
information extractable by a computationally bounded observer (Finzi et al.,
arXiv:2601.03220) and the perturbation-flip-rate criterion for reasoning rather
than recall — and show both are *consequences* of a single substrate-native
model: the **persistence-closure hypergraph ledger**. Reality is a relational
hypergraph $H=(V,E)$ updated by local, scale-free causal-invariant rewrite
rules; a bounded observer $S$ is a local pattern enclosed by a Markov blanket of
bandwidth $\mathcal{C}(\mathcal{B}_S)\ll\mathcal{D}(H)$.

From this we derive the **Separation Hypothesis (SH)** and then — unlike most
framing papers — we attempt to *break it*. We state the strongest objection
(the Scarred Tissue argument: the judge's geometry is carved from the witness's
data, so the two cannot be cleanly split) and provide two independently
falsifiable experiments that would distinguish the claims:

1. **The latency falsifier.** If reasoning is path-recalculation over a real
   hypergraph topology, deleting a load-bearing edge should produce a
   measurable routing-latency cost that scales predictably with the surrounding
   geometry — a mechanical signature independent of whether the final answer is
   correct. Absence of such a signature falsifies the geometric account.
2. **The epiplexity-after-purge test.** Wipe the content/witness store of a
   trained system, then measure the description-length/epiplexity of the
   residual weights. If geometry is separable, epiplexity stays stable while
   the episodic layer's time-bounded entropy spikes; if not, both collapse.

The intelligence core functions as a **coherence gate** (a bullshit detector):
its competence is defined over path existence under edge rewiring. Flip rate is
the operationalization — does the inference path survive edge deletion?

---

## 1. Introduction: The Free Lunch, Reread

[Section 1 of v0.2 — Levin's Platonic ingress as occluded ledger activity;
the free lunch is paid in full in a currency the observer's blanket cannot
audit. Extend the same occlusion argument from morphogenesis to reasoning.]

## 2. The Ledger Model

[Section 2 of v0.2 — relational hypergraph; bounded observer + Markov blanket;
structural content (epiplexity) vs time-bounded entropy; epiplexity is
observer-dependent = ledger topology the blanket does not occlude.]

## 3. Reasoning as Path Existence Under Edge Rewiring

[Section 3 of v0.2 — perturbation = edge rewiring; flip = answer survives the
rewire; flip rate = path-existence under load-bearing edge deletion. Two-sided
hazard: over- and under-sensitive systems both fail; requires provably-minimal,
load-bearing perturbation sets (known for synthetic grammars).]

### 3.1 The circularity problem, and the latency falsifier (NEW in v0.3)

A skeptical reviewer objects: "You define robust reasoning as *paths that
survive*, then use the fact that they survived as proof of reasoning. Circular."
Abstractly: we assert reasoning $\iff$ path survives edge deletion, then measure
"reasoning" by survival. This is the classic measure-defines-the-result trap.

**The break:** measure the *computational cost of rerouting*, not just the
outcome. For a genuine hypergraph, deleting a load-bearing edge does not merely
change an answer — it forces path recomputation, and that recomputation costs
*time and energy in amounts that scale with the local geometry* (the number and
conditioning of alternative paths). Concretely:

- Predict a **latency function** $\tau(\pi)$ over perturbations: minimal edge
  deletions produce small, bounded rerouting; large coherent deletions near the
  answer's dependence set produce steeply rising latency; the curve should track
  the graph distance/connectivity of the deleted region.
- Separately predict it will be **camera-independent**: the latency signature
  exists whether or not the model outputs the correct answer, so it is not
  confounded by accuracy.

If no such scaling latency exists — if output correctness fully determines
"reasoning" with no mechanical trace — the geometric-path account is
falsified in favor of a black-box-matching account. This turns the flip-rate
claim from a behavioral observation into a claim about an underlying, measurable
topology.

## 4. The Separation Hypothesis and the Judge/Witness Split

[Section 4 of v0.2 — SH statement; amnesia test; judge/witness/router.]
### 4.1 The inference/training distinction (tightened in v0.3)
SH is an **inference-time** claim, not a training-time one. We never assert that
a judge can be *trained* with zero data; the judge's geometry is built *from*
high-epiplexity data (training-time dependence is real and acknowledged). What
SH asserts is that once built, the *operation* of reasoning is separable from
the *content* it currently holds. The strongest existing evidence is the context
window: modern LMs can have their entire context window (the in-the-moment
witness) cleared and swapped, and reason identically. That is functional
inference-time separation running in production. Training-time dependence is
explicitly not contested (see §5, the Scarred Tissue objection).

## 5. The Scarred Tissue Objection (NEW in v0.3)

The strongest attack on SH, surfaced by adversarial synthesis. We state it in
full, then respond.

### 5.1 The objection
> "The reasoning structure is the scarred tissue of past memories. Every
> high-epiplexity datum rewires the graph; the judge's geometry was *carved* by
> the witness's data. You cannot swap the memory without altering the
> topological attractors that constitute the geometry. You have not separated
> the judge and the witness — you have hidden the witness behind a curtain; the
> judge is still executing the will of the witness."

This reduces to: **the weights *are* the compressed training data.** The
geometry is not an independent substrate-agnostic shape; it is the
internalized record of the data's regularities, and severing the data severs the
record.

### 5.2 Why it fails (mechanically)
The objection confuses **formation** with **operation**. That a structure was
*formed* by data does not entail that its *ongoing operation* depends on the
data it no longer holds — any more than a building's load path depends on the
quarry its stones came from. Three independent responses:

1. **The compression argument.** If the weights *were* the data, then two models
   trained on disjoint data could not converge on the same reasoning capability.
   But transfer results (epiplexity §6: language pretraining transfers across
   domains; structured training generalizes OOD) show the *operation* — the
   compiled subcircuits, induction heads, constraint paths — outlives and
   generalizes beyond the specific data that in-formed it. The capability
   semantics is not tied to the source instance.
2. **The negation test.** The objection implies memory-loss ⇒ reasoning-collapse.
   This is empirically false at the behavioral level: amnesic humans retain
   procedural reasoning, puzzle-solving, and anomaly detection (the BS-detector
   survives). And it is the exact claim our §6.2 experiment is designed to test
   mechanically, not just behaviorally. The objection stops being a philosophical
   wall the moment you measure epiplexity-after-purge.
3. **The honest limit.** The objection *does* capture a real boundary: SH holds
   *within a regime* (a given topology + swappable content) and is uncertain at
   regime boundaries — where the perturbation is so severe it rewrites the
   geometry itself, not just the loaded content. We do not claim separation
   survives a rewrite of the attractor structure. That is the boundary we flag,
   not hand-wave away. If the latency and purge experiments show the geometry
   deforms continuously with content, SH is weakened to a regime-relative claim —
   which is still a non-trivial, useful result (the context-window evidence
   already establishes a wide and useful regime).

### 5.3 The convergence (the safe claim)
Both sides of the adversarial split agree: whatever the answer on *perfect*
separation, the shift from counting Shannon entropy/tokens to measuring
**epiplexity / latent-space topology** is real and important. We build the paper
primarily on that measurement shift; the stronger SH is the contested claim
with explicit falsifiers.

## 6. Testable Predictions

1. **Density.** Core-trained (high-epiplexity synthetic) models show a better
   epiplexity-per-parameter Pareto frontier than scraped-text models of
   equivalent volume.
2. **Transfer.** Flip rate on held-out rails from a different grammar is above
   chance for ledger-trained models (competence transfers across domains).
3. **Factor-order.** Reverse-ordered complex data (deduce move-sequence from
   final board state; the epiplexity paper's Lichess result) forces higher
   epiplexity and better OOD generalization.
4. **Composition.** A small ledger-trained judge + retrieval witness closes most
   of the gap to a much larger monolithic model at a fraction of inference
   compute.
5. **Circularity test.** Core-trained models must also perform on public
   transfer surfaces (GPQA, ARC-AGI-style), not only on rails sharing their
   training grammar.
6. **THE LATENCY FALSIFIER (NEW).** Prediction: a measurable, geometry-scaling
   rerouting-latency cost $\tau(\pi)$ exists on load-bearing edge deletion,
   independent of output correctness. *If it does not exist, the geometric
   account is falsified.*
7. **THE EPIPLEXITY-AFTER-PURGE TEST (NEW).** Prediction: purging the content/
   witness store leaves weight-epiplexity (description length) stable while
   episodic-layer time-bounded entropy spikes. *If both collapse together, SH
   fails.* (Operationalized on an AlphaZero-style system: wipe board-state
   memory; judge should retain time-bounded epiplexity on novel randomized
   states.)

## 7. Related Work and Provenance

[Section 7 of v0.2 — epiplexity; Persistence-Closure Hypergraph Framework
(EILT); perturbation evals (GSM-Symbolic, Sophontic — unverified numbers not
adopted); functionalist substrate-agnosticism (EILT; CASY Neuro-Holographic);
first-person neurodivergent data.]

## 8. Holes to Fill

[Section 8 of v0.2, updated: #1 formalize epiplexity on hypergraph; #2 minimal
load-bearing perturbation construction; #3 error-signal primitive; #4 borrowable
experiments now including latency + purge tests; #5 decentralization out of
scope; #6 compute-inference separability (now central, §4.1/§5); #7 plural
authorship/endorsement.]

## 9. Contributions & Process (NEW in v0.3)

This paper's claims, structure, and much of its argument were produced through
a **human-AI collaborative research pipeline**, operationalized exactly as the
paper's own thesis (human as auditing Judge, AI as Witness/generator, iteration
as the coherence loop). No contribution is being papered over:

- **Human lead (Gene Yanenko):** the Persistence-Closure Hypergraph Framework
  and EILT ontology; the experimental proposals (bioelectric morphogenesis);
  final scientific accountability; the amnesia-brain and BS-detector framing.
- **Oryon (Hermes agent) / ClawHoarde:** primary research gathering and
  synthesis; adversarial analysis of Sophontic and the epiplexity paper;
  drafting (v0.1-v0.3); co-design of the falsifiers; CASY/Literature threading.
- **NotebookLM synthesis pipeline:** independent Deep Dive + Critique + Debate
  audio overviews that surfaced the jigsaw-puzzle mechanism, the reverse-order
  prediction, the latency circularity-break, and the Scarred Tissue objection
  (transcripts in references/).
- **Process honesty:** we include ourselves because we did the work. This
  section is the paper's own argument demonstrated: AI collaboration compounds
  reasoning when the human remains the auditing agent — and this paper is the
  record of exactly that.

## 10. Status and Disclaimer

Position/framework paper with two specified falsifiers, not yet a results
paper. No model has been trained to test §6 yet; the experiments are next.
We assert decomposition, not obsoletion; third-party 60-1000x claims are
unverified and not adopted.

---

## References

[Full reference list in v0.4 — see §8.7]
