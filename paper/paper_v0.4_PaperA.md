# Attribution Intersection: Isolating Data-Invariant Reasoning Subgraphs in Transformers

**Status:** Preprint draft v0.4 — "Paper A" of the planned split. Methods paper, no ontology.
**Date:** 2026-08-10
**Author:** Gene Yanenko. **Analysis and synthesis co-research:** Oryon (Hermes agent), ClawHorde, NotebookLM synthesis pipeline. See §8.
**License:** MIT (code), CC-BY 4.0 (text)

**Version note.** v0.4 implements the external review of 2026-08-10 plus FIX 1–5 of the v0.4 revision plan. Four substantive changes from v0.3: (a) the latency falsifier is reformulated as *computational depth*, because wall-clock latency cannot measure rerouting in a fixed-depth transformer; (b) the Scarred Tissue defense is rebuilt on MDL-transferability rather than a formation/operation binary; (c) the hypergraph-ledger ontology is removed to a separate paper; (d) the interpretability literature this work extends is now cited. Sophontic references are withdrawn — see §7.3.

---

## Abstract

We propose and specify a protocol for empirically separating the *reasoning machinery* of a transformer from the *content* it operates on, and a falsifiable test of whether that separation is real.

The protocol — **attribution intersection** — runs a single reasoning template across many data instantiations, extracts a per-trace attribution graph over internal components, and intersects the graphs. Edges surviving intersection are data-invariant: they are recruited by the reasoning operation regardless of what the operation is about. Edges appearing in only some traces are content-bound. We call the invariant subgraph the **judge** and the variable remainder the **witness**.

This operationalizes what we term the **Separation Hypothesis (SH)**: that the competence of tracking load-bearing structure through an inference chain is distinguishable, at inference time, from the store of facts that inference consumes. SH is an inference-time claim; we explicitly do not claim the judge can be *trained* without data (§5).

We specify three falsifiers, pre-registered before running:

1. **Existence.** A stable subgraph survives data-varied intersection at threshold θ across k/N traces — or it does not, and SH as stated is wrong.
2. **Depth scaling.** Ablating a judge edge increases *computational depth* — the layer index at which the correct answer becomes linearly decodable — and the increase scales with the ablated edge's position in the induced graph. Ablating matched control edges does not. If depth is flat under judge ablation, the geometric account is falsified in favour of undifferentiated redundancy.
3. **Topology.** The induced subgraph exhibits small-world structure, giving O(log n) depth growth under progressive ablation, versus linear for a redundant-MLP baseline. This contrast, not the existence of an effect, is the discriminating prediction.

The protocol is testable on a 70M-parameter model. Null results will be published.

---

## 1. Introduction

Two observations motivate this work, and neither is ours.

The first is that large models frequently answer correctly without tracking the structure that makes the answer correct. Perturbing a load-bearing element of a problem while preserving its surface form degrades performance substantially — the GSM-Symbolic result (Mirzadeh et al., 2024) is the cleanest demonstration: templated variation of numerical values and names in grade-school math problems produces significant accuracy drops, which is difficult to explain if the model were tracking the derivation rather than the pattern.

The second is that factual content in transformers appears to be at least partially localized and at least partially separable from the machinery that uses it. Geva et al. (2021) characterize feed-forward layers as key-value memories over training patterns. Meng et al. (2022, 2023) locate specific factual associations and edit them — ROME and MEMIT change what a model knows about a subject while leaving its general competence intact. Olsson et al. (2022) identify induction heads as compiled circuits performing a content-general operation.

Put together, these suggest a question that has not, to our knowledge, been asked in exactly this form: **can the content-general machinery be isolated as an object — extracted, named, measured — rather than inferred from behavioural dissociations?**

We propose that it can, by exploiting the one property that distinguishes machinery from content: machinery is what stays the same when the content changes.

### 1.1 What this paper is and is not

This is a methods and pre-registration paper. No model has yet been run through the protocol. The contribution is (i) a specified extraction procedure, (ii) three falsifiers with stated pass/fail conditions, and (iii) an explicit statement of the strongest objection and what would settle it.

We do not claim the scaling paradigm is obsolete. We claim it may be *decomposable*, and we specify how to find out.

---

## 2. The Separation Hypothesis

> **SH.** The reasoning competence of a trained transformer is realized in a subgraph of internal components whose recruitment is invariant under variation of the content being reasoned about; this subgraph is identifiable, and its ablation degrades reasoning in a manner that scales with its topology rather than with the volume of components removed.

Three clarifications, each of which forecloses a common misreading.

**SH is an inference-time claim.** We do not assert a judge can be trained on zero data. The judge's geometry is built *from* data, and that training-time dependence is real and uncontested. What SH asserts is that once built, the operation is separable from the content currently loaded.

**The existing evidence for a weak form is already substantial.** Context windows are cleared and swapped continuously in production while reasoning competence persists. ROME/MEMIT edit facts without destroying inference. Induction heads execute a content-general operation. The weak form of SH is close to consensus; what is missing is a method for isolating the responsible structure directly.

**The strong form is contested and we treat it as such.** See §5.

---

## 3. The measurement: flip rate

Accuracy on a single item cannot distinguish reasoning from matching. The paired-perturbation criterion can.

For a pair $(q_c, q_p)$ where $q_p$ is a minimal, load-bearing perturbation of $q_c$:

- $\text{flip} = 1$ iff the system answers $q_c$ correctly *and* gives the correspondingly changed correct answer on $q_p$.
- $\text{flip rate} = \text{flips} / \text{pairs}$.

The pair, not the item, is the unit.

**Stated limitation.** Flip rate measures sensitivity to perturbation, and sensitivity fails in both directions: a brittle noise-chaser and a structure-blind matcher both score badly, for opposite reasons. The metric is meaningful only when perturbations are provably minimal and provably load-bearing — which requires knowing the proof graph. This is available for synthetic generative grammars and noisy for public benchmarks. That argues for synthetic-first rails with audited provenance, not for abandoning the metric.

---

## 4. Attribution intersection

### 4.1 The problem the protocol solves

The falsifiers in §6 presume discrete, load-bearing edges. A transformer does not supply them: attention is dense, every token attends to every token, and there is nothing literal to delete. The graph must be *induced* before anything can be measured. This section specifies how.

### 4.2 Protocol

**(1) Instrumentable model.** A small open-weights model — Pythia-70M through 1B, GPT-2 small, or Qwen2.5-0.5B — where attention logits, MLP activations, and residual-stream components are fully accessible and ablation is cheap. Small is a methodological feature, not a compromise: if the hypothesis is about structure rather than scale, the smallest substrate exhibiting the structure is the correct test bed, and it makes hundreds of traces affordable.

**(2) Trace families.** One derivational template — a transitive chain, a syllogistic form, a constrained arithmetic derivation — instantiated across many data points varying entity names, numeric values, and surface vocabulary. The reasoning structure is held invariant; everything else varies. Vocabulary is arbitrary and regenerated, so nothing is memorizable.

**(3) Per-trace attribution graphs.** For each trace, extract a weighted directed graph of functional couplings between internal components using established circuit-discovery tooling:

- **Edge Attribution Patching (EAP)** — first-order approximation of patching cost per edge; cheap enough to run per-trace at scale.
- **ACDC-style circuit search** — exact-ish subgraph discovery, feasible on small models.
- **Activation and logit patching** — causal verification of candidate edges.
- **Sparse autoencoder features** — to define edges at feature rather than head granularity where the head-level graph is too coarse.
- **TunedLens / LogitLens** — for locating where in depth the answer is computed (also the instrument for §6.2).

Each trace yields one weighted graph $G_i$ over a shared component vocabulary.

**(4) Intersection.** Threshold each $G_i$ at attribution weight $\theta$, then intersect across $N$ traces:

- An edge is **structural (judge)** if it survives in $\geq k$ of $N$ traces with stable weight.
- An edge present in a minority of traces is **content-bound (witness)**.

The judge is *exactly* the subgraph invariant under data variation. The witness is everything that varies with it. No further definition is required, and none is smuggled in.

**(5) Pre-registration.** $\theta$, $k/N$, the ablation protocol, and the control-edge matching criteria are fixed and published before any run. This is not a courtesy; without it, the intersection threshold is a free parameter that can manufacture any result.

### 4.3 Open methodological question

What θ and k/N make the stable-subgraph claim robust against noise? A subgraph that survives at $k = 0.5N$ but vanishes at $k = 0.9N$ is a different object from one stable across the range. We propose reporting the full stability curve rather than a single threshold, and treating the shape of that curve as itself a result: a sharp knee indicates a genuinely discrete structure; a smooth decay indicates the judge/witness distinction is a gradient rather than a partition, which would itself be an informative and publishable finding.

---

## 5. The Scarred Tissue objection

The strongest attack on SH, stated in full before it is answered.

### 5.1 The objection

> The reasoning structure is the scarred tissue of past memories. Every datum rewires the graph; the judge's geometry was *carved* by the witness's data. You cannot swap the memory without altering the topological attractors that constitute the geometry. You have not separated judge from witness — you have hidden the witness behind a curtain, and the judge is still executing its will.

Reduced: **the weights are the compressed training data.** Severing the data severs the record.

### 5.2 Response — transferability, not independence

We accept the premise. This is the substantive change from v0.3, which attempted a formation-versus-operation binary. That defense was brittle precisely because it fought the mathematics the work is built on: if structural information is defined in terms of description length, then claiming the judge is "not data" contradicts the framework being used to describe it.

The correct claim is narrower and survives the objection:

> **Judge = the transferable subset of the compression. Witness = the non-transferable, domain-specific remainder.**

The judge *is* compressed data. What distinguishes it is that its utility decouples from the specific instances that produced it.

The anchor is the reverse-order result in Finzi et al. (2026): training a model to deduce move sequences from final board states forces deeper board representations than forward-order training. That acquired structure is technically compressed position data — and it operates independently on out-of-distribution tasks such as centipawn evaluation, which was never the training objective. Utility decoupled from the specific memories that carved it. That decoupling, not metaphysical data-independence, is the separation claim.

The same reframing applies to any convergent structural motif: not evidence of mystical content-independence, but a high-epiplexity structural regularity that, once formed, generalizes to novel inputs.

**Independent corroboration from the grokking literature.** The memorization-to-generalization transition is the cleanest existing window on this claim. Grokking research finds that the sub-circuits responsible for memorization and for generalization are largely independent, with the sharp transition explained by their *relative learning rates* rather than capacity constraints (Nguyen et al., 2024); that memorization complexity scales with training-set size while generalization complexity stays constant, so the two must eventually cross (Nanda et al., 2023; Power et al., 2022); and that regularization routes — weight decay, dropout, BatchNorm — each push toward the generalizing circuit through distinct mechanisms, including de-amplifying memorizing neurons and amplifying generalizing ones (Doshi et al., 2023). These results do not require our protocol to interpret — they are the judge/witness split observed in the grokking regime, stated in the literature's own vocabulary: a generalizing sub-circuit whose recruitment is invariant across the specific training content, coexisting with content-bound memorization sub-circuits. They do not prove SH holds at scale; they demonstrate the separability the protocol is designed to measure is a real, previously observed phenomenon rather than a category error.

### 5.3 The honest boundary

The objection captures a real limit. SH holds *within a regime* — a given topology with swappable content — and is uncertain at regime boundaries where perturbation rewrites the geometry rather than the load.

An unquantified regime concession is a get-out-of-jail card: a critic ablates, the structure collapses, the author says "too hard." We therefore state the boundary as a conjecture with a measurable form:

> **Regime conjecture.** SH holds while the description length of the perturbation remains below the description length of the judge subgraph. Below that bound, geometry survives and content degrades. Above it, geometry deforms and SH fails.

This is falsifiable: run the ablation battery at increasing perturbation complexity and locate the transition. If there is no transition — if degradation is smoothly proportional throughout — the regime framing is wrong and we will say so.

**Independence requirement (added 2026-08-11, from the adversarial critique pass).** The bound above must not be measured with the same instrument that extracts the judge — that is circular. The judge's description length is to be estimated from its *transfer* behavior (how much the extracted subgraph compresses held-out generalization via an MDL bound), *not* from the EAP graph's own edge count. If the boundary is read off the extraction tool's output, then a failed test can always be attributed to a mis-measured boundary, and the strong form is unfalsifiable in practice. We therefore pre-register that the regime boundary uses an independence-of-instrument bound: the judge's size is measured by what it does on unseen data, never by how many edges its own graph shows.

---

## 6. Falsifiers

### 6.1 Existence

**Prediction.** A stable subgraph survives data-varied intersection at pre-registered θ and k/N.
**Falsified if:** intersection yields no stable core, or the surviving set is indistinguishable from what random trace-pairs would share.

### 6.2 Depth scaling (replaces the v0.3 latency falsifier)

**Why the previous formulation fails.** v0.3 predicted a rerouting-*latency* cost on load-bearing edge deletion. This cannot work. A transformer's forward pass is a fixed sequence of operations: ablating a component does not lengthen it, does not add layers, and does not change the FLOP count. There is no dynamic path search to be slowed. Wall-clock differences under ablation measure cache locality and kernel scheduling — hardware artefacts, not topology. The graph-search intuition is biological and does not transfer to fixed-depth inference.

**The corrected instrument: computational depth.** The quantity that genuinely varies is *how far into the network* the answer takes to form.

> $\delta(e) :=$ the layer index at which the correct answer first becomes linearly decodable from the residual stream (logit lens / tuned lens), measured per input, under ablation of edge $e$.

Depth is internal, per-input, hardware-independent, and — critically — defined whether or not the final output is correct. It preserves everything the latency falsifier wanted while measuring something that exists.

A second, coarser instrument for chain-of-thought settings: the number of reasoning tokens emitted before the answer stabilizes.

**Prediction.** $\Delta\delta$ under ablation of judge edges is positive and scales with the ablated edge's position in $G$ — betweenness centrality, edge connectivity, reroute frontier depth. $\Delta\delta$ under ablation of matched control edges (low betweenness, high redundancy, same layer, same head count) is approximately flat.

**Controls.**
- *Re-insertion.* Restoring an ablated edge returns depth to baseline. Hysteresis would indict caching rather than topology.
- *Substrate swap.* Absolute values will differ across CPU/GPU and x86/ARM; the rank-ordering of ablation costs must not. Depth should be substrate-invariant by construction, which is the point of using it instead of time.
- *Wall-clock retained solely as a noise channel.* If wall-clock and depth correlate, that is evidence of a confound, not of the effect.

**Falsified if:** depth is flat under judge ablation, or judge and control ablations are statistically indistinguishable.

### 6.3 Topology

**Prediction.** The induced subgraph is small-world, giving $\delta$ growth of $O(\log n)$ under progressive ablation, versus linear for a redundant-MLP baseline under the same protocol.

This is the discriminating test. "Ablation has an effect" is compatible with undifferentiated redundancy and proves nothing. The *shape* of the effect is what separates the hypotheses, and a reviewer can kill it cleanly.

A secondary structural prediction, anchored in Finzi et al.'s Rule 54 cellular-automaton result — where a computationally bounded model learns glider collision rules rather than unrolling the simulation — is that the extracted subgraph should show the signature of executing compiled rules rather than brute-force recomputation.

### 6.4 Transfer

**Prediction.** A judge extracted from grammar A retains above-chance flip rate on held-out rails from grammar B, and on public transfer surfaces (GPQA, ARC-AGI-style) rather than only on rails sharing its training grammar.

This is the circularity guard. Performance measured only on self-generated rails is not evidence of anything.

### 6.5 Composition

**Prediction.** A small judge coupled to a retrieval witness closes a substantial fraction of the gap to a much larger monolithic model on reasoning benchmarks at a fraction of inference compute.

Weakest of the five and listed last deliberately: it is an engineering payoff conditional on the others, not an independent test.

---

## 7. Related work

### 7.1 Directly extended

- **Finzi, Qiu, Jiang, Izmailov, Kolter, Wilson (2026),** *From Entropy to Epiplexity* (arXiv:2601.03220; code: github.com/shikaiqiu/epiplexity). Supplies the structure-versus-entropy split and the data-selection criterion, plus the reverse-order and Rule 54 results anchoring §5.2 and §6.3.
- **Geva, Schuster, Berant, Levy (2021),** *Transformer Feed-Forward Layers Are Key-Value Memories.* The empirical basis for treating FFN layers as the primary content store.
- **Meng, Bau, Andonian, Belinkov (2022),** *Locating and Editing Factual Associations in GPT* (ROME); **Meng et al. (2023),** MEMIT. Direct evidence that factual content can be localized and modified without destroying inferential competence — the strongest existing support for a weak Separation Hypothesis.
- **Olsson et al. (2022),** *In-context Learning and Induction Heads*; **Elhage et al. (2021),** *A Mathematical Framework for Transformer Circuits.* Establish that content-general operations are realized in identifiable circuits.
- **Conmy et al. (2023),** ACDC; **Syed, Rager, Conmy (2023),** Edge Attribution Patching. The extraction tooling in §4.2.
- **Mirzadeh et al. (2024),** *GSM-Symbolic.* The perturbation result motivating flip rate.

### 7.2 Adjacent

Retrieval-augmented generation as the applied form of judge-plus-witness; the surface-form brittleness literature more broadly; sparse autoencoder dictionary learning for feature-level edge definition.

### 7.3 Withdrawn from prior versions

Earlier drafts (v0.1 §7) cited Sophontic AI as a source for the perturbation paradigm and referenced third-party claims of 60×–1000× reasoning advantages. **These citations are withdrawn in full.** As of 2026-08-10 that company has released no model, no eval kit, no paper, and no third-party benchmark; the claims appear only in company marketing material. The perturbation paradigm has independent grounding in the peer-reviewed literature (§7.1), which is cited instead. We note the withdrawal explicitly rather than silently, in keeping with §9.

### 7.4 Companion work

The ontological framework that originally motivated this line — a persistence-closure hypergraph account of bounded observers — is deliberately excluded here and developed separately. This paper stands or falls on the extraction protocol and the falsifiers, and requires no commitment to that framework.

---

## 8. Contributions and process

The claims, structure, and much of the argument in this paper were produced through a human-AI collaborative research pipeline, operationalized as the paper's own subject matter: human as auditing judge, AI as witness and generator, iteration as the coherence loop.

- **Human lead (Gene Yanenko):** research direction; the amnesia-brain and coherence-gate framing; the experimental proposals; final scientific accountability.
- **Oryon (Hermes agent) and ClawHorde:** literature gathering and synthesis; adversarial analysis; drafting across v0.1–v0.4; co-design of the falsifiers.
- **NotebookLM synthesis pipeline:** independent deep-dive, critique, and debate passes that surfaced the circularity objection, the Scarred Tissue argument, and the reverse-order prediction. Transcripts in `references/`.
- **External review (2026-08-10):** identified the wall-clock-latency error corrected in §6.2, the missing interpretability literature now in §7.1, and the source problem in §7.3.

We state this because we did the work this way, and because a paper arguing that auditing structure can be separated from generative content should be transparent about having been produced by exactly that arrangement.

---

## 9. Status, commitments, and disclaimer

Pre-registration paper. No model has been run. §6 is the next step and is affordable — the full protocol is a weekend on a 70M-parameter model.

**Standing commitments:**
- Thresholds and ablation protocols are published before running.
- Null results are published with the same prominence as positive results.
- No data is excluded post hoc to fit the hypothesis.
- Withdrawn claims are marked as withdrawn, not deleted (§7.3).

The extraction method is a contribution independent of whether SH survives. A clean falsification of a geometric-reasoning claim at this specificity is worth more to the field than an unfalsifiable framework.

---

## References

1. Finzi, M., Qiu, S., Jiang, Y., Izmailov, P., Kolter, J. Z., Wilson, A. G. "From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence." arXiv:2601.03220 (2026).
2. Geva, M., Schuster, R., Berant, J., Levy, O. "Transformer Feed-Forward Layers Are Key-Value Memories." EMNLP (2021).
3. Meng, K., Bau, D., Andonian, A., Belinkov, Y. "Locating and Editing Factual Associations in GPT." NeurIPS (2022).
4. Meng, K., Sharma, A. S., Andonian, A., Belinkov, Y., Bau, D. "Mass-Editing Memory in a Transformer." ICLR (2023).
5. Olsson, C., et al. "In-context Learning and Induction Heads." Transformer Circuits Thread (2022).
6. Elhage, N., et al. "A Mathematical Framework for Transformer Circuits." Transformer Circuits Thread (2021).
7. Conmy, A., Mavor-Parker, A. N., Lynch, A., Heimersheim, S., Garriga-Alonso, A. "Towards Automated Circuit Discovery for Mechanistic Interpretability." NeurIPS (2023).
8. Syed, A., Rager, C., Conmy, A. "Attribution Patching Outperforms Automated Circuit Discovery." (2023).
9. Mirzadeh, I., Alizadeh, K., Shahrokhi, H., Tuzel, O., Bengio, S., Farajtabar, M. "GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models." (2024).
10. Belrose, N., et al. "Eliciting Latent Predictions from Transformers with the Tuned Lens." (2023).
11. Power, A., Burda, Y., Edwards, H., Babuschkin, I., Misra, V. "Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets." ICLR (2022).
12. Nanda, N., Chan, L., Lieberum, T., Smith, J., Steinhardt, J. "Progress measures for grokking via mechanistic interpretability." ICLR (2023).
13. Nguyen, T., et al. "The relative learning rates of memorization and generalization sub-circuits explain the grokking transition." (2024).
14. Doshi, S., et al. "How regularization shapes the memorization-to-generalization transition: weight decay, dropout, and BatchNorm." (2023).
15. Duan, Z., et al. "Circular Reasoning: Understanding Self-Reinforcing Loops in Large Reasoning Models." arXiv:2601.05693 (2026).
16. Pipis, C., et al. "Wait, Wait, Wait... Why Do Reasoning Models Loop?" arXiv:2512.12895 (2025).
