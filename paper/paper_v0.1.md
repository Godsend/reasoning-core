# Reasoning Without Memory: An Epiplexity-Framed Architecture for Separating Intelligence from Content

**Status:** Preprint draft (v0.1) — stake-claim / position paper
**Date:** 2026-08-10
**Author:** Gene Yanenko (with Oryon, as analysis partner)
**License:** MIT (code), CC-BY 4.0 (text)

---

## Abstract

The scaling paradigm treats intelligence as a byproduct of data volume and
parameter mass: ingest more, memorize more, generalize more. Recent work on
*epiplexity* (Finzi et al., 2026) formalizes what computationally bounded
observers can actually learn from data, separating structural content
(learnable by bounded computation) from time-bounded entropy (pseudorandom and
chaotic content that cannot be distilled). This paper argues that epiplexity
provides the theoretical foundation for a different engineering target: an
**intelligence core** whose reasoning competence is trained *independently of*
the factual content it will later be asked to use — a brain with amnesia,
provided with memory.

We make three claims:

1. **Reasoning is a separable competence.** The operations that track
   load-bearing structure through a chain of inference are distinguishable
   from the store of facts those operations consume. Synthetic generative
   grammar data (high epiplexity, near-zero memorized content) can train the
   former without instantiating the latter.

2. **The natural measurement is perturbation tracking, not accuracy.** A
   paired canonical/perturbed evaluation ("flip rate") tests whether a system
   tracks *structure* rather than matching *surface*. One-correct-item accuracy
   rewards memorization; flip rate punishes it. The pair is the unit of
   measurement.

3. **The core's function is coherence enforcement — a bullshit detector —
   not answer retrieval.** The intelligence core checks whether a chain of
   reasoning remains coherent under perturbation; factual grounding is the
   job of swappable memory. The architecture is therefore: **judge + witness
   + router**, where the judge is small and stable, the witness is large and
   swappable, and the router decides which competence is needed.

The integrated system is deliberately substrate-heterogeneous: some components
live in hardware (a fixed reasoning core), some in software (memory banks,
indexes, retrieval), exactly as biological cognition separates stable
procedural structure from episodic content.

---

## 1. Motivation: the amnesia test

Consider a system that has been trained on a large corpus, then loses access
to its episodic content. What remains? Under the scaling view, not much — a
model is its data. Under the epiplexity view, what remains is the *learned
structure*: the operations, the constraint-satisfaction machinery, the
geometry of coherent inference. A functionalist reading of cognition (substrate-
agnostic, pattern-first) predicts the survivor is exactly the structure — a
"brain with amnesia" that retains dispositions and procedures while losing
episodes.

This is not merely a philosophical framing. It is the testable engineering
target: can we train a compact model whose *reasoning geometry* is dense enough
that, when coupled to external memory, it performs as well as (or better than)
a monolithic model that memorized the content? We call this the **Separation
Hypothesis**:

> **Separation Hypothesis (SH):** The reasoning competence of a learning
> system can be trained from high-epiplexity, low-entropy synthetic data to a
> degree where coupling it with an external memory store recovers the
> performance of a system trained directly on the full content distribution.

If SH holds, the scaling paradigm is not "obsolete" but *decomposable*:
intelligence becomes a fixed hardware core; knowledge becomes a swappable
software load. This is the same division biology already makes: stable
procedural morphology (the organism's geometry) vs. context-dependent memory.

## 2. Epiplexity as the theoretical foundation

Finzi, Qiu, Jiang, Izmailov, Kolter, and Wilson (arXiv:2601.03220) define
epiplexity as the information a computationally bounded observer can extract
from data, excluding time-bounded entropy. Key results relevant here:

- **Information can be created by computation.** Deterministic transformations
  of data can increase learnable content — likelihood modeling can produce
  programs more complex than the generating process itself.
- **Ordering matters.** The sequence in which data is presented changes what a
  bounded learner can extract.
- **Likelihood modeling is not mere distribution matching.** It can exceed the
  generating process.

For the Separation Hypothesis, epiplexity supplies the *selection criterion*:
data with high epiplexity and low entropy is the material from which a
reasoning core can be trained without memorizing content. Synthetic generative
grammars — problems generated from a known rule set (e.g., trell/jrell-style
relational syllogisms with controlled hop counts and distractor density) — are
epiplexity-dense by construction. Every item instantiates the reasoning
pattern; nothing is memorizable because the vocabulary is arbitrary and
regenerated.

This is the difference between the two training regimes:

| Regime | Data | What is learned | Parameter requirement |
|---|---|---|---|
| Scaling | Scraped corpus (high entropy, sparse structure) | Structure mined from dilute solution | Massive (volume needed to find signal) |
| Core training | Synthetic grammar (dense structure, ~zero entropy) | The operations themselves | Compact (structure is the generator) |

## 3. The measurement: flip rate

Conventional accuracy rewards surface-feature heuristics: a model that matched
the training distribution can score well without reasoning. The perturbation
paradigm (paired canonical/perturbed items) precludes this. If a proof depends
on a fact, changing the load-bearing fact must change the answer. A system that
answers the canonical item correctly but fails the perturbed item has
*matched*, not reasoned.

Formally, for a pair $(q_c, q_p)$ where $q_p$ is a minimal load-bearing
perturbation of $q_c$:

- $\text{flip} = 1$ iff the system's answer is correct on $q_c$ and the
  *opposite* correct answer on $q_p$ (i.e., it tracked the change).
- $\text{flip rate} = \frac{\text{flips}}{\text{pairs}}$.

The pair is the unit. One correct item is not enough when the load-bearing fact
has moved.

**Limitation (stated honestly):** flip rate measures *sensitivity to
perturbation*, which cuts both ways. Over-sensitive systems (brittle
noise-chasers) and under-sensitive systems (ignore load-bearing change) both
fail. The metric is only meaningful when the perturbation is provably minimal
and load-bearing, which requires knowledge of the proof graph — available for
synthetic grammars, noisy for public transfer tasks. This is a measurement
hygiene problem, not a fatal flaw: it argues for synthetic-first rails with
audited provenance.

## 4. Architecture: judge, witness, router

The Separation Hypothesis implies a three-component architecture:

1. **Judge (intelligence core, hardware-fixed):** A compact model trained on
   high-epiplexity synthetic data. Its competence is coherence tracking:
   given a claim or chain, does it remain coherent under perturbation? Does
   the conclusion follow from the load-bearing premises? It does not need to
   *know* the facts; it needs to *check* the reasoning. Its failure mode is
   failing to flag incoherence — which is the failure mode of confident
   hallucination in current systems.

2. **Witness (memory, software-swappable):** The factual store — parametric
   knowledge, retrieval indexes, vector banks, tool-accessible sources. It
   can be updated, replaced, or versioned independently of the judge. This is
   the "amnesia brain provided with memory."

3. **Router:** Decides which competence applies — factual retrieval (witness)
   vs. coherence enforcement (judge) vs. logical constraint checking (a
   symbolic layer). A beautiful lie is structurally sound, so the judge alone
   is insufficient: coherence detects *incoherence*, semantics detects
   *falsehood*. Both are needed, and the router arbitrates.

Hardware/software split is a matter of engineering economics, not principle —
some components are better in silicon (the stable judge), some in swappable
storage (the witness). Biology does the same: stable morphogenetic geometry,
context-loaded memory.

## 5. The bullshit-detector function

The most immediately useful instantiation of the judge is not an answer engine
but a **coherence gate**: given a claim, a chain, or a model's output, flag
whether the structure holds under perturbation. This is:

- **Content-invariant:** the same geometry checks any domain.
- **Cheap:** small parameter count, fixed hardware.
- **Complementary:** pairs with retrieval-augmented generation, which supplies
  facts but not coherence guarantees.

A coherence gate in front of any LLM output catches the confident-hallucination
class of failure that accuracy benchmarks reward. It is the guard, not the
engine — and the guard is the part that must be stable.

## 6. Testable predictions

1. **Density:** A model trained on synthetic perturbation pairs (high
   epiplexity) will exhibit a better epiplexity-per-parameter Pareto frontier
   than a model trained on an equivalent volume of scraped text.
2. **Transfer:** Flip rate measured on held-out rails from a *different*
   grammar will be substantially above chance for core-trained models — i.e.,
   the competence transfers across content domains.
3. **Composition:** A small core-trained judge + retrieval witness will close
   most of the gap to a much larger monolithic model on reasoning benchmarks,
   while using a fraction of the inference compute.
4. **Circularity test:** Core-trained models must also perform on public
   transfer surfaces (e.g., GPQA, ARC-AGI-style), not only on rails sharing
   their own training grammar. Performance on self-generated rails alone is
   not evidence.

## 7. Related work and provenance

- **Epiplexity:** Finzi, Qiu, Jiang, Izmailov, Kolter, Wilson, "From Entropy
  to Epiplexity: Rethinking Information for Computationally Bounded
  Intelligence," arXiv:2601.03220 (2026). Code: github.com/shikaiqiu/epiplexity.
  The theoretical foundation for data selection and the 
  structure-vs-entropy split.
- **Perturbation evals:** the paired perturbation paradigm as popularized in
  the "geometric reasoning" discourse (Sophontic, 2026); the underlying
  concern — models matching rather than reasoning — is an established research
  thread (e.g., surface-form brittleness results such as GSM-Symbolic).
- **Functionalist substrate-agnosticism:** the framing that intelligence is a
  pattern, not a substance, and can be decomposed across hardware/software
  boundaries (relevant to EILT and related ontology work).

## 8. Status and disclaimer

This is a position paper and stake-claim, not a results paper. No model has
been trained by the author to test SH yet; the experiments in §6 are the next
step. Claims about the scaling paradigm's "obsoleteness" are deliberately not
made — decomposition is the claim, not obsolescence. Third-party claims of
60×–1000× reasoning advantages are referenced only as motivation, and are
unverified pending release of models and eval kits.

---

## References

1. Finzi, M., Qiu, S., Jiang, Y., Izmailov, P., Kolter, J. Z., Wilson, A. G.
   "From Entropy to Epiplexity: Rethinking Information for Computationally
   Bounded Intelligence." arXiv:2601.03220 (2026).
2. Sophontic AI. "Geometric reasoning, explained." (Interview, Aug 2026);
   sophontic.ai — motivating the perturbation paradigm; claims unverified.
3. Godsend (Yanenko, G.). "Ego-Intentional Latent Topology (EILT)" — 
   functionalist, substrate-agnostic ontology work; personal framework.
