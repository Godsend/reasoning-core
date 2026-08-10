# v0.4 Revision Plan — from re_critique_v03

Source: `references/artifacts/re_critique_v03.txt` (auto-title: "Hardening the
epiplexity hypergraph reasoning account"). This critique is a major rigor
upgrade. It accepts the DIRECTION of both falsifiers but shows both are too
coarse, and gives four precisely-specified fixes. It also flags a self-defeating
tension: §5's formation/operation binary fights the very MDL math the paper
builds on.

## FIX 1 — Latency falsifier: needs a UNIQUE scaling law (not just "latency exists")

**The problem:** dense neural nets with redundant sub-circuits ALSO show routing
delays when perturbed. "Latency scales with perturbation" proves *some* network
exists, not the specific persistence-closure hypergraph / EILT topology. The
current falsifier hands critics a club: "sure, latency — you're just measuring
messy brute-force redundancy."

**The fix (v0.4):** derive a specific mathematical slope for the latency function
$\tau(\pi)$, unique to EILT topology, and contrast it against a standard
architecture (e.g., ResNet under structured pruning). Concretely:
- Does rerouting cost in a scale-free/small-world hypergraph grow at
  $O(\log n)$ (small-world property) vs linear for a redundant MLP?
- Anchor in Finzi's Rule 54 CA result: a computationally-bounded judge model
  learns *geometric collision rules* (gliders) rather than unrolling the
  simulation. So EILT predicts the latency curve matches "executing geometric
  collision rules," a **mechanically different signature** from "unrolling a
  brute-force recalculation." State this as the divergent prediction.

## FIX 2 — §5 Scarred-Tissue defense: stop fighting MDL; reframe as transferability

**The problem:** the formation/operation binary is brittle BECAUSE epiplexity IS
defined as minimum-description-length. If weights literally ARE compressed
data, then "the judge is separate from the record of the data" fights the math
the paper is built on.

**The fix (v0.4):** embrace MDL. Don't claim the judge is non-data. Claim:
- **Judge = the high-epiplexity, transferable subset of the compression.**
- **Witness = the non-transferable, domain-specific entropy.**
- Anchor in Finzi's reverse-order Lichess result: reverse-ordered training
  forces higher epiplexity (deeper board representations). That acquired
  structure, though technically compressed Fenboard data, *operates
  independently on OOD tasks* like centipawn evaluation. Utility decouples from
  the specific memories that carved it — that's the actual separation claim.
- Also reframe the "spiritual bliss attractor" the same way: not mystical
  data-independence, but a **high-epiplexity structural motif** models converge
  on to compress human psychological data; once formed it guides novel inputs
  even when training tokens are purged.

## FIX 3 — Purge test: target internal weight parameters, NOT context window

**The problem:** clearing a context window proves only that context is
transient — a first-year-undergrad fact. It says nothing about the weights.
The witness isn't in the KV cache; clearing the desk isn't purging the
filing cabinet.

**The fix (v0.4):** redesign the purge to **target FFN layers** (associated with
factual/episodic memory stores), via **targeted rank reduction / structured
pruning**, leaving attention heads intact (associated with routing/induction/
structure = the judge). Then:
1. Rank-reduce FFN layers to destroy factual knowledge.
2. Measure model epiplexity before/after.
3. Feed novel OOD reasoning tasks (no trivia reliance).
4. Predict: trivia performance dies, but epiplexity stays stable → SH proven
   *within the weights*, not just behaviorally.

## FIX 4 — Regime boundary: quantify it, or the admission makes SH unfalsifiable

**The problem:** the honest "SH holds within a regime" concession is a get-out-
of-jail-free card unless the boundary is mathematically defined. A critic runs
the FFN ablation, epiplexity collapses, and the author says "you perturbed too
hard — still true." Unfalsifiable.

**The fix (v0.4):** define the boundary precisely with time-bounded quantities:
- Conjecture: SH holds strictly while the **Kolmogorov complexity of the
  perturbation ≤ time-bounded epiplexity of the judge**. If damage < structural
  complexity, geometry survives; if damage > complexity, geometry collapses.
- Or anchor to Rule 54 emergence thresholds: establish a predictive ratio —
  regime holds while (structural info / random content) stays above a constant.
- This turns the biggest vulnerability into a bold falsifiable prediction.

## Net v0.4 moves
1. §3.1: replace qualitative latency with a specific scaling-law prediction
   (O(log n)? geometric-collision signature) + ResNet contrast.
2. §5.2: replace formation/operation binary with MDL-transferability framing
   (judge = transferable epiplexity subset; witness = domain entropy).
3. §6.7: replace context-clear purge with FFN targeted rank-reduction purge.
4. §5.3/§8: replace vague regime admission with quantified computational-bound
   threshold (perturbation complexity ≤ judge epiplexity) OR Rule 54 ratio.
5. §9 Contributions: preserve; add "revision loops against adversarial
   synthesis" as the demonstrated method.
