# Consensus Literature Findings — Batch 2 (Aug 11 2026)

> Themes surfaced by the critique/debate/explainer batch + the scarred-tissue
> objection. Run through Consensus (authed Chrome session) Aug 11 2026.
> These are NEW citations for Paper A, largely absent from the v0.4 draft.

## Theme 1: Doom loops / repetitive degeneration (from Liquid's Antidoom blog)
Directly relevant to the flip-rate / path-failure story. Confirmed canonical refs:

- **Duan et al. (2026)** — "Circular Reasoning: Understanding Self-Reinforcing
  Loops in Large Reasoning Models." arXiv:2601.05693. Defines circular
  reasoning as a self-reinforcing trap where generated content acts as a
  logical premise for its own recurrence; links it to a V-shaped attention
  pattern; **semantic repetition precedes textual repetition** (the model gets
  stuck on an idea before the words loop).
- **Pipis et al. (2025)** — "Wait, Wait, Wait... Why Do Reasoning Models Loop?"
  arXiv:2512.12895. Repetitive loops at low temperature / greedy decoding in
  LRMs; inference failure + computational waste.
- **Liquid AI (2026)** — "Reducing Doom Loops with Final Token Preference
  Optimization" (Antidoom/FTPO). blog + github.com/Liquid4All/antidoom.
  Identifies the exact first token of the first repeat; trains only that
  position; "overtrained tokens + uncertainty + prior reinforcement" mechanism.
  **Key result: once doom loops are eliminated, near-greedy sampling beats
  high temperature — the "higher temp is better" intuition was conflated with
  the looping artifact.**
- Related classic: Holtzman et al. (2020), The Curious Case of Neural Text
  Degeneration (ICLR); Paech et al. (2026) Antislop (ICLR).

**Why it matters for Paper A:** doom loops are a *flip-rate phenomenon in
disguise* — the model fails at a decision point and the same token keeps
winning. The "semantic repetition precedes textual repetition" result is a
mechanistic account of why an inference path fails, which is the load-bearing
edge data the flip-rate framework predicts. Cite in the falsifier / related
work section as evidence that path-failure is measurable and mechanistic.

## Theme 2: Grokking — memorization vs generalization circuits (scarred tissue)
The strongest independent support for the Separation Hypothesis:

- **Power et al. (2022)** — "Grokking: Generalization Beyond Overfitting on
  Small Algorithmic Datasets" (arXiv:2201.02177; ICLR 2022) — the original.
- **Nanda et al. (2023)** — "Progress measures for grokking via mechanistic
  interpretability" — Fourier circuit amplification; memorization complexity
  scales with training set size, generalization complexity stays constant, so
  the two must cross.
- **Nguyen et al. (2024)** — **"the sub-circuits responsible for memorization
  and generalization can be viewed as largely independent, and the relative
  rates at which they learn — rather than capacity constraints — explain the
  sharp transition."** This is the judge/witness split already demonstrated in
  the grokking regime. DIRECT citation for the Separation Hypothesis.
- **Liu et al. (2022)** — four learning phases (comprehension, grokking,
  memorization, confusion); representation learning in the "Goldilocks zone."
- **Doshi et al. (2023)** — weight decay / dropout / BatchNorm each push toward
  generalizing representations via distinct mechanistic routes (de-amplifying
  memorizing neurons, amplifying generalizing ones).
- **Manir et al. (2026)** — depth effects non-monotonic (depth-4 MLPs fail to
  grok, depth-8 residual recover); GELU up to 4.3x faster than ReLU when
  regularization permits initial memorization; bounded spherical normalization
  reduces grokking onset 20x+.

**Why it matters:** the scarred-tissue objection (judge = compressed training
data) is answered *in the literature*: memorization and generalization
sub-circuits are largely independent, and generalization complexity is
constant regardless of training set size. The judge isn't the witness's scar —
it's a separate circuit that forms at its own rate. Paper A's §5 (Scarred
Tissue defense) should cite Nguyen 2024 + Nanda 2023 + Power 2022.

## Theme 3: Logit lens / depth probes (falsifier instrumentation)
- **Belrose et al. (2023)** — "Eliciting Latent Predictions from Transformers
  with the Tuned Lens" (arXiv:2303.08112) — already in Paper A's citation list.
- Consensus confirms the logit-lens family is the standard instrument for
  reading intermediate layers; depth-to-convergence (Paper A's falsifier #2)
  is a novel *application* of an established instrument.

## Action items for Paper A
1. Add Nguyen et al. 2024 to §5 (Scarred Tissue defense) — independent
   empirical support for judge/witness separability.
2. Add Power 2022 + Nanda 2023 to §1 or §5 — grokking as the phase-transition
   window where the split is observable.
3. Add Duan 2026 + Pipis 2025 to the falsifier / related-work — doom loops as
   flip-rate evidence.
4. Optionally cite Liquid AI Antidoom as a recent applied instance (blog, not
   peer-reviewed — mark as such).
