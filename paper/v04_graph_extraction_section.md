# v0.4 Draft Section — Operationalizing the Hypergraph: Attribution-Based Edge Extraction

> Status: DRAFT for v0.4. Proposed placement: new §3.2 (after the latency
> falsifier, before §4), or as the operational core of Fix 1's scaling-law
> prediction. This section is deliberately framed as a **falsifiable research
> proposal**, not a claim. It either produces a stable subgraph with
> structure-tracking latency, or it doesn't — and both outcomes are published
> as the result.

## 3.2 Where do the edges come from? Attribution-based extraction

The latency falsifier (§3.1) assumes a hypergraph with discrete, load-bearing
edges. A transformer does not hand us that graph: attention is dense and
continuous, every token attends to every token, and there are no literal edges
to delete. Before $\tau(\pi)$ can be measured, the graph must be **induced**
from the model. This section specifies how.

### 3.2.1 The extraction protocol

The proposal: find edges **programmatically**, by running parallel reasoning
traces that vary the data while holding the reasoning structure fixed, then
intersecting the functional-coupling graphs each trace produces.

1. **Instrumentable model.** Use a small open-weights model (Pythia-70M–1B,
   TinyStories, GPT-2 small, or Qwen2.5-0.5B) where full internals — attention
   logits, MLP activations, residual-stream components — are accessible and
   ablation is cheap. Small is a feature here: the hypothesis is
   substrate-agnostic, so the *smallest substrate that exhibits the structure*
   is the correct test bed, and it makes hundreds of traces affordable.

2. **Trace families.** Construct a reasoning family: one logical/derivational
   template (e.g., "given premises P, derive conclusion C" or a transitive
   chain), instantiated across many different data points (different entities,
   numbers, surface vocabulary). The reasoning structure is the invariant; the
   data is the variable.

3. **Per-trace attribution graph.** For each trace, extract a weighted
   directed graph of functional couplings between internal components
   (attention heads, MLP neurons, residual-stream features) using standard
   circuit-discovery tooling:
   - **Edge Attribution Patching (EAP)** — first-order approximation of
     patching cost per edge, cheap enough to run per-trace at scale.
   - **ACDC-style circuit search** — exact-ish subgraph discovery on small
     models.
   - **Activation/logit patching** — causal verification of candidate edges.
   - **Sparse autoencoder features** (Anthropic dictionary learning) — to
     define edges at the feature level rather than the head level, if desired.
   - Optionally **TunedLens/LogitLens** for a quick sanity read on where the
     answer is computed.
   Each trace yields one weighted graph $G_i$ over the same component
   vocabulary.

4. **Intersection = the judge; difference = the witness.** Threshold each
   $G_i$ at an attribution weight $\theta$, then intersect across the $N$
   traces:
   - An edge is **structural** if it survives in $\geq k$ of $N$ traces with
     stable weight (e.g., $k = 0.8N$). These are data-invariant functional
     dependencies — the reasoning geometry.
   - Edges present in only some traces are **content-bound** — the witness's
     transient couplings to this particular data.

   This is the cleanest possible operationalization of the Judge/Witness
   split: the judge is *exactly* the subgraph invariant under data variation;
   the witness is everything that varies with it.

### 3.2.2 The NCC framing

The persistent subgraph is the **digital equivalent of a neural correlate** —
not of consciousness (we make no phenomenal claim) but of the *reasoning
competency itself*: the minimal functional substrate sufficient to execute the
derivation, isolated by systematically varying everything non-structural.

Just as NCC research seeks the minimal neural state sufficient for an
experience, this protocol seeks the minimal functional subgraph sufficient for
a competency, identified by content-invariance. The name is earned precisely
because the method mirrors the logic: perturb the inputs, hold the machinery
constant, and what remains stable is the correlate.

### 3.2.3 Feeding the falsifier

The induced graph $G$ is the object the latency falsifier operates on:

- **Delete structural edges** by ablating the corresponding components
  (zeroing the attention head's contribution or the MLP path), then measure
  $\tau(\pi)$: the rerouting cost should scale with $G$'s local geometry —
  betweenness centrality, edge connectivity, reroute frontier depth — per the
  parametric form in §3.1's fix (FIX 1, v0.4):
  $$\tau(e) = \tau_0 + \alpha\, \lambda(e)^{-1} e^{\beta B(e)} + \gamma\, h(e)$$
- **Delete control edges** (low betweenness, high redundancy): flat
  $\Delta\tau$ within the same model, same tokens, same hardware state.
- **Re-insert** a deleted edge: latency returns to baseline (reversibility;
  hysteresis would indict caching, not topology).
- **Cross-substrate replication:** run the same deletion battery on CPU/GPU,
  x86/ARM. Absolute latencies will differ — that is hardware friction — but
  if the *rank-ordering* of deletion costs survives the substrate swap, the
  structure's signature is camera-independent in the strongest sense.

### 3.2.4 The unique scaling-law hook (FIX 1 integration)

The extracted graph's *topology* is itself the divergent prediction:

- If $G$ is scale-free/small-world (as EILT predicts), rerouting cost should
  grow $O(\log n)$ with graph size — vs. linear for a brute-force redundant
  MLP under the same deletion protocol. That contrast, not "latency exists,"
  is the falsifiable signature.
- Anchor in Finzi's Rule 54 result: a computationally-bounded judge learns
  *geometric collision rules* (gliders) rather than unrolling the simulation.
  EILT therefore predicts the extracted subgraph looks like *executing
  collision rules* — a mechanically different trace from brute-force
  recalculation. State this as the divergent prediction; a reviewer can kill
  it cleanly.

### 3.2.5 Epistemic posture (why this is a proposal, not a claim)

We are not asserting the extracted graph *is* the reasoning. We are asserting
the following, each falsifiable:

1. A stable subgraph survives data-varied intersection (or it doesn't).
2. Its topology is scale-free/small-world with $O(\log n)$ rerouting (or it
   isn't — and SH as stated is wrong, and we will say so).
3. Latency tracks structure, not token count or hardware state (or it doesn't,
   and the geometric-path account is falsified in favor of
   black-box-matching).

No data will be cooked to fit the theory. The protocol is specified in
advance; the threshold $\theta$, intersection ratio $k/N$, and ablation
protocol are pre-registered in the paper before running. If the structure is
there, the paper reports it with its measured scaling law. If it is not, the
paper reports the null result — which is itself a contribution, because the
protocol is now public and the falsification is sharp.

**Either way, a published, indexed paper has merit:** the method (attribution
intersection across data-varied traces as a judge-extraction protocol) is
reusable regardless of whether this particular hypothesis survives; and a
clean falsification of a geometric-reasoning claim at this specificity is
worth more to the field than another unfalsifiable manifesto.
