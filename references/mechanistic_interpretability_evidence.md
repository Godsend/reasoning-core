# Mechanistic Interpretability — Evidence Base for the "Digital NCC" (§3.2)

> Why this exists: §3.2 of the reasoning-core paper claims the "judge" is a
> data-invariant subgraph extractable from reasoning traces. That claim needs a
> literature spine. These three sources are that spine — they supply both the
> *techniques* the protocol uses and an *existence proof* that a minimal,
> necessary-and-sufficient reasoning subgraph exists in practice.

## 1. The survey — where the techniques come from

- **Rai, Zhou, Feng, Saparov, Yao (2025)** — *A Practical Review of Mechanistic
  Interpretability for Transformer-Based Language Models.* arXiv:2407.02646v4
  (Oct 13 2025). Task-centric survey; the canonical beginner's roadmap.
- Organizes MI into three studies: **features**, **circuits**, **universality**.
  A circuit is "a sub-graph of M responsible for implementing specific LM
  behaviors," with features as nodes and weighted connections as edges.
- **Why it matters for the paper:** the §3.2 protocol (parallel reasoning
  traces → EAP attribution intersection → the judge) is standard *circuit study*.
  This survey is the methods reference for every step:
  - Localization techniques: **activation patching** (localize nodes),
    **path patching** (localize edges) — both are perturbation-based, i.e. the
    flip-rate operationalization.
  - **ACDC** (Conmy et al. 2023) — automated circuit discovery by iteratively
    removing edges whose effect on a target metric is minimal. Directly the
    "delete load-bearing edge, measure outcome" pattern.
  - **EAP** (Syed et al. 2023) / **EAP-IG** (Hanna et al. 2024) — Edge
    Attribution Patching, gradient-based approximation of edge patching, two
    forward + one backward passes. The paper's §3.2 explicitly proposes EAP
    for attribution intersection.
  - **Universality** — whether circuits persist across LMs/tasks. The paper's
    judge-is-data-invariant claim is a universality claim; this survey defines
    the verification framing (dimensions of variation: across models, across
    tasks).
- **Key framing for the paper:** MI already defines a circuit as "meaningful
  computational pathways connecting features" that "facilitate specific LM
  behaviors" — the paper's contribution is turning that descriptive object
  (a circuit exists) into the *operationalized* Separation Hypothesis (the
  data-invariant circuit = the judge; varies the data, hold machinery constant,
  intersect).

## 2. The overview — definitional grounding

- **Wikipedia: Mechanistic interpretability.** Coined by Chris Olah (circuit
  analysis). Distinguishes MI (reverse-engineering concrete structures /
  algorithms / circuits) from gradient-based black-box attribution (saliency
  maps, etc.).
- Key concepts: **linear representation hypothesis** (high-level concepts =
  linear directions in activation space), **sparse autoencoders** (SAEs —
  Anthropic; disentangle activations into sparse human-understandable
  features), **features and circuits** (circuits = causal chains of feature
  activations; map, activate, inhibit to analyze).
- **Why it matters:** gives the paper clean definitions to cite — the judge is
  a *circuit* (causal chain under perturbation), extraction uses SAE-free EAP,
  and the data-invariance claim inherits the linear-representation /
  universality framing.
- Primary citations available: Olah et al. 2020 (Zoom In: An Introduction to
  Circuits, Distill); Conmy et al. 2023 (ACDC); Geiger et al. 2025 (Causal
  Abstraction, JMLR); Lindsey et al. 2025 (On the Biology of a large LM,
  Anthropic attribution graphs — directly supports the "attribution graph"
  framing the paper's §3.2 uses).

## 3. THE EXISTENCE PROOF — OpenAI Sparse Circuits (the linchpin)

- **Gao, Rajaram, Coxon, Govande, Baker, Mossing (OpenAI, Nov 13 2025)** —
  *Understanding Neural Networks Through Sparse Circuits.* arXiv:2511.13653.
- Trained language models (GPT-2-like) with the vast majority of weights forced
  to zero, so each neuron connects to only a few dozen others. The result:
  networks with small, **disentangled circuits**.
- The key result, in the paper's own words:
  > "In our definition, the exact connections shown above are **sufficient** to
  > perform the task — if we remove the rest of the model, this small circuit
  > still works. They are also **necessary** — deleting these few edges causes
  > the model to fail."
- **Why this is the empirical linchpin for reasoning-core:**
  - Necessity = **flip-rate operationalized**. "Deleting these few edges causes
    the model to fail" is exactly the reasoning-core claim that a load-bearing
    edge's deletion flips the inference path. OpenAI has demonstrated this holds
    in real trained transformers, not just synthetic grammars.
  - Sufficiency = **the judge is real**. A minimal circuit that "still works"
    with the rest of the model removed is a data-invariant functional substrate
    — the digital NCC. It exists, it is sparse, and it does the task on its own.
  - It is also a *construction* recipe: train sparse → extract circuits
    directly, rather than post-hoc analysis of dense networks. The paper's
    §3.2 protocol (induce sparse graphs from traces via attribution) aligns
    with this forward path.
- Scaling caveat (cite-able ground truth): OpenAI explicitly notes sparse
  models are "much smaller than frontier models," large parts remain
  uninterpreted, and the approach is "no guarantee this will extend to more
  capable systems." The reasoning-core paper should adopt this honest scope:
  the judge exists in tractable transformers; whether it persists at frontier
  scale is exactly what the falsifiers test.

## How this maps onto reasoning-core §3.2

| Reasoning-core claim | MI source |
|---|---|
| Reasoning = path existence under edge rewiring (flip rate) | Conmy et al. 2023 (ACDC edge deletion); OpenAI 2025 (deleting edges → failure) |
| Judge = data-invariant subgraph across traces | Universality (across-tasks); OpenAI 2025 sufficiency (circuit works with rest removed) |
| Extraction via EAP attribution intersection | Syed 2023 / Hanna 2024 (EAP / EAP-IG); survey §5.2.3 |
| Latency falsifier (rerouting cost scales with geometry) | Path patching / activation patching (perturbation cost) — the paper's novel extension |
| Falsifiable at scale (honest scope) | OpenAI 2025 scaling caveat; survey §9 gaps |

## Files
- Survey full text: `C:/Users/geney/AppData/Local/hermes/cache/web/arxiv.org-5c88f75e68.md`
- Wikipedia: `C:/Users/geney/AppData/Local/hermes/cache/web/en.wikipedia.org-c4db38b093.md`
- OpenAI sparse circuits (extract inline above): arxiv.org/abs/2511.13653
