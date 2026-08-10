# Occluded Ledger, Separable Reason: An Epiplexity-Grounded Hypergraph Account of the Judge/Witness Split

**Status:** Preprint draft (v0.2 — hypergraph-ledger rewrite)
**Date:** 2026-08-10
**Author:** Gene Yanenko (with Oryon, as analysis partner)
**Version note:** v0.2 replaces the v0.1 "riff on the perturbation paradigm" with the
hypergraph-ledger framing native to the author's Persistence-Closure Hypergraph
Framework (EILT). The v0.1 file is preserved at paper/paper_v0.1.md.

---

## Abstract

We unify two apparently separate results — the epiplexity measure of structural
information extractable by a computationally bounded observer (Finzi et al.,
arXiv:2601.03220) and the perturbation-flip-rate criterion for reasoning rather
than recall — and show that both are *consequences* of a single, substrate-native
model: the **persistence-closure hypergraph ledger**. In this model reality is a
relational hypergraph $H = (V, E)$ updated by local, scale-free causal-invariant
rewrite rules; a bounded observer $S$ is a local pattern enclosed by a Markov
blanket of bandwidth $\mathcal{C}(\mathcal{B}_S) \ll \mathcal{D}(H)$.

From this we derive the **Separation Hypothesis**: reasoning competence — the
capacity to track load-bearing structure through inference — is a *property of the
ledger's invariant topology*, not of the content stored in it. It can therefore be
trained from high-epiplexity synthetic data (structure-dense, content-poor) and
deployed as a compact, stable **judge**, coupled to a swappable **witness** that
holds the time-bounded-entropy content. The architectural split *judge + witness +
router* is not an engineering convenience but the necessary form of any persistence-
closure system that must track structure across a bandwidth-limited blanket.

The intelligence core functions as a **coherence gate** — a bullshit detector —
because its competence is defined over *path existence under edge rewirure*: does
the inference path from premise to conclusion survive the deleption/rewiring of
load-bearing edges? Flip rate is the operationalization of exactly this.

---

## 1. Introduction: The Free Lunch, Reread

Michael Levin's *Ingressing Minds* (2026) documents an extraordinary empirical
fact: synthetic life forms (Xenobots, Anthrobots) with no evolutionary lineage for
their goals nonetheless self-organize toward functional target states —
navigating, repairing, persisting. Levin accounts for this by positing an
external, nonphysical "Platonic Space" whose causal templates "in-form" material
substrates. We have argued elsewhere (Persistence-Closure Hypergraph Framework)
that this is a bookkeeping error: the surplus is **occluded ledger activity** —
parallel constraint-satisfaction running on hypergraph regions the observer's
own Markov blanket prevents it from auditing. The "free lunch" is paid in full,
in a currency the local observer cannot spend.

This paper extends that argument from morphogenesis to *reasoning*. The same
occlusion argument that dissolves Levin's Platonic ingress explains both:

1. **Why bounded observers extract structure (epiplexity), not noise** — the
   structural content of a dataset is precisely the invariant topology that
   parallel, occluded computation can build; the noise is what cannot be compiled.
2. **Why a model can reason without recalling** — if the target morphology (or
   the reasoning path) is an attractor state of the ledger's constraint topology,
   then a system whose content store is wiped retains the *shape* of the answer:
   the surrounding geometry narrows what the missing piece must be. This is the
   judge/witness split, and it follows from the ledger model rather than being
   asserted as architecture.

---

## 2. The Ledger Model

### 2.1 Basin definitions

Reality is modeled as a relational hypergraph

$$H = (V, E), \quad E \subseteq \mathcal{P}(V) \setminus \{\emptyset\}$$

updated by local rewrite rules $\mathcal{R}$ that are **causally invariant**:
the history of rewrites obeys the same local rules at every scale (Wolfram,
1989). Physical law is not bedrock; it is the stable trace of rewrite invariants
— the constants are what survived.

A **bounded observer** $S$ is a local network pattern enclosed by a Markov
blanket $\mathcal{B}_S$ with channel capacity

$$\mathcal{C}(\mathcal{B}_S) \ll \mathcal{D}(H),$$

where $\mathcal{D}(H)$ is the total dimensional complexity of the ledger. Because
the ledger is computationally irreducible, the observer cannot shortcut occluded
regions: $t_{estimate} \ge t_{actual}$ for any reasoning done outside its blanket.

### 2.2 The ledger and information

Two kinds of content flow through the ledger:

- **Structural content (epiplexity $E_p$):** the invariant topology the observer
  can compile from the data it sees — reusable subcircuits, induction heads,
  load-bearing relations. This is learnable by bounded computation.
- **Time-bounded entropy $S_t$:** the pseudorandom/chaotic residue that cannot be
  compiled — proportional to what the observer's blanket occludes.

Epiplexity is *observer-dependent*: the same dataset is structure to a powerful
observer and noise to a weak one. In ledger terms: **epiplexity is the measure of
ledger topology the observer's blanket does not occlude.** The free lunch and the
learnable structure are the same phenomenon seen from inside and outside the
blanket.

---

## 3. Reasoning as Path Existence Under Edge Rewiring

### 3.1 The perturbation paradigm, in ledger terms

Conventional accuracy rewards surface-feature matching: a model that matched the
training distribution scores well without tracking structure. The intuitive
perturbation criterion (paired canonical/perturbed items) can be made precise:

Let a **reasoning instance** be an inference path $p: q \Rightarrow a$ through
the concept graph — a sequence of load-bearing edges from premise $q$ to answer
$a$ (in a hypergraph, a hyperedge binds arbitrary many vertices; a single
perturbation may rewrite several edges at once).

A **load-bearing perturbation** $\pi$ is a minimal rewrite of the concept graph
that deletes or reweights the edges $p$ depends on, such that the correct answer
flips to $a' \ne a$. Define:

$$\text{flip} = 1 \iff \left( f(p \Rightarrow a) \text{ correct} \right) \land
\left( f(p_\pi \Rightarrow a') \text{ correct} \right),$$

$$\text{flip rate} = \frac{\mathbb{E}[\text{flip}]}{\#\text{pairs}}.$$

A model that answers the canonical item correctly but fails the perturbed item has
**matched** on the unperturbed surface; it has not tracked the load-bearing
structure. The pair is the unit of measurement.

**Ledger reading:** flip rate measures whether the model's internal ledger
contains the *path* $p$ in a form robust to edge rewiring, or only the *surface*
coordinate of the answer. A reasoner has compiled the invariant topology
(subcircuit) $p$; a surface-matcher has stored the answer as a disconnected node.

### 3.2 Why sensitivity is insufficient alone (the two-sided hazard)

Flip rate measures sensitivity to perturbation — and sensitivity cuts both ways.
An over-sensitive model (brittle noise-chaser, rewires on any surface change)
and an under-sensitive model (ignores load-bearing change) both fail. The metric
is meaningful only when $\pi$ is *provably* minimal and load-bearing. This
requires knowing the proof graph — available by construction for synthetic
generative-grammar data, noisy for public transfer tasks. We therefore argue for
**synthetic-first rails with audited provenance** (see §6).

---

## 4. The Separation Hypothesis and the Judge/Witness Split

### 4.1 Statement

> **Separation Hypothesis (SH):** The reasoning competence of a persistence-closure
> system — its ledger topology — can be trained from high-epiplexity synthetic data
> to a degree where coupling it with an external content store (witness) recovers
> the performance of a system trained directly on the full content distribution.

SH is a *ledger claim*: the invariant topology (judge) is separable from the
stored content (witness) because they occupy different regions of the ledger —
the compiled constraints vs. the loaded values.

### 4.2 The amnesia argument

The strongest motivation is the **amnesia test**: train a system, then wipe its
episodic/content store. What survives? Under the scaling view, little — a model
is its data. Under SH, what survives is the compiled topology: the operations, the
constraint-satisfaction machinery. A functionalist reading — EILT's "I am what I
do, not what I remember" — predicts the survivor is exactly the structure: a brain
with amnesia, provided with memory.

This is not merely philosophical. It is the testable claim that a compact judge +
external witness can match a monolithic model on reasoning benchmarks (§6).

### 4.3 Architecture

- **Judge (intelligence core):** compact, stable, hardware-fixed. Competence =
  coherence tracking: given a claim/chain, does its inference path survive
  perturbation? Does it have the *shape* of the answer (the jigsaw with the
  center piece missing) even without the content?
- **Witness (memory):** large, swappable, software-loadable. Holds the
  time-bounded-entropy content — facts, retrieval indexes, tool-accessible
  sources. Updateable/versionable/detachable independently of the judge.
- **Router:** arbitrates — factual retrieval (witness) vs. coherence enforcement
  (judge) vs. logical constraint checking (symbolic layer). A beautiful lie is
  structurally sound, so the judge alone is insufficient: coherence detects
  *incoherence*, semantics detects *falsehood*. Both are needed.

The hardware/software split is an engineering-economics choice, not a principle —
some components favor silicon (the stable judge), some favor swappable storage
(the witness). Biology does the same: stable morphogenetic geometry, context-loaded
memory.

---

## 5. The Bullshit-Detector Function

The most immediately useful instantiation of the judge is a **coherence gate**:
given a claim or a model output, flag whether the structure holds under
perturbation. Properties:

- **Content-invariant** — the same geometry checks any domain.
- **Cheap** — small parameter count, fixed hardware.
- **Complementary** — pairs with retrieval-augmented generation, which supplies
  facts but not coherence guarantees.

A coherence gate in front of any LLM output catches the confident-hallucination
class of failure that accuracy benchmarks reward. This is the *guard*, not the
*engine* — and the guard is the part that must be stable.

---

## 6. Testable Predictions

1. **Density.** A model trained on synthetic perturbation pairs (high epiplexity)
   will show a better epiplexity-per-parameter Pareto frontier than a model trained
   on an equivalent volume of scraped text.
2. **Transfer.** Flip rate measured on held-out rails from a *different* generative
   grammar will be substantially above chance for ledger-trained models — the
   competence transfers across content domains.
3. **Factor-order (synthesis-surfaced).** Training on reverse-ordered complex data
   (e.g., deduce the move-sequence from a final chess board state, per the epiplexity
   paper's Lichess result) forces the model to compile the rules rather than follow a
   forward breadcrumb trail — higher epiplexity, better OOD generalization.
4. **Composition.** A small ledger-trained judge + retrieval witness closes most of
   the gap to a much larger monolithic model on reasoning benchmarks at a fraction
   of the inference compute.
5. **Circularity test.** Core-trained models must also perform on public transfer
   surfaces (GPQA, ARC-AGI-style), not only on rails sharing their training grammar.
   Performance on self-generated rails alone is not evidence.

---

## 7. Related Work and Provenance

- **Epiplexity.** Finzi, Qiu, Jiang, Izmailov, Kolter, Wilson, "From Entropy to
  Epiplexity: Rethinking Information for Computationally Bounded Intelligence,"
  arXiv:2601.03220 (2026); code github.com/shikaiqiu/epiplexity.
- **Persistence-Closure Hypergraph Framework (EILT).** The author's monograph
  resolving the Levin-Sweet dialectic: Levin's "Platonic ingress" as occluded
  ledger activity; the $C_{anticipate} \le C_{absorb}$ mind-boundary. This paper
  generalizes that framework from morphogenesis to reasoning.
- **Perturbation evals.** The paired-item flip paradigm (Sophontic, 2026,
  motivating; underlying matching-vs-reasoning concern established, e.g.,
  GSM-Symbolic). Claims of 60–1000× are **unverified** — referenced only as
  motivation, not evidence.
- **Functionalist substrate-agnosticism.** EILT; CASY's "Neuro-Holographic"
  framing of relational, non-hierarchical cognition (Prince-Hughes; Jou).
- **First-person neurodivergent data:** the author's aphantasia + SDAM +
  pre-verbal conceptual processing + functionalist identity claim.

---

## 8. Holes to Fill (explicit, before arXiv/journal)

We state the open problems rather than papering over them. These are the gaps a
rigorous version must close:

1. **Formalize epiplexity on the ledger.** In v0.2, epiplexity is defined
   informally as "ledger topology the blanket does not occlude." We need the
   definition of epiplexity (Definition 8, Finzi et al.) restated as a graph/
   hypergraph invariant, and the two-part-code / prequential estimators remapped
   to path-existence terms. *Status: informal.*
2. **Precise load-bearing-perturbation construction.** Flip rate requires
   provably minimal, load-bearing perturbation sets. For synthetic grammars this
   is known; formalize the generator and the minimality guarantee.
3. **The `epsilon` (error-signal) primitive.** The Jon-Quinn "stress is all you
   need" and the alpha-config are only gestured at. SH needs a defined error
   signal by which the ledger detects edge-rewire and recompiles — the analogue
   of bioelectric `V_mem` gradients in the morphogenetic case.
4. **Existing / borrowable experiments.** The epiplexity estimators and reverse-
   order Lichess result already exist; SH needs the specific ablations (scrub
   content from a small model's witness, measure judge survival).
5. **Decentralization / AI safety framing.** Clearly out of scope for the
   technical paper; separate essay. Do not let it bloat §5.
6. **Compute-inference separability.** SH claims the judge is cheap at *inference*
   and the witness swappable — but the judge still requires training compute to
   *build*. State explicitly that the separability is inference-time, not
   training-time; the concentration assumption (epiplexity dense in a small
   subspace) is what would make a hardware intelligence core viable, and it is
   unproven.
7. **Plural authorship & endorsement.** For arXiv: personal endorsement from an
   established domain author (per Jan 2026 policy — institutional email alone no
   longer suffices). Candidates: Levin (q-bio), Bach (cs.AI/cog-sci), Jou (Yale;
   CASY). The v0.1 framing, the letters, and the synthesis are supporting material.

---

## 9. Status and Disclaimer

Position/reference paper, not a results paper. No model has been trained to test
SH yet; §6 experiments are the next step. This is a decomposition claim, not an
"obsoletion" claim: we do not assert the scaling paradigm is dead, only that it
is decomposable. Third-party 60–1000× claims are unverified and are not adopted.

---

## References

[Full reference list to be completed in v0.3 — see §8.6]