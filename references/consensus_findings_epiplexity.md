# Consensus.app Literature Findings — Epiplexity (Aug 10 2026)

Source: https://consensus.app — query "epiplexity", synthesized + source-panel.
Log: Gene's account (sidebar shows prior EILT threads: Hypergraph Framework for
Biological Agency, Unified Informational Ledger Theory, Unified Informational
Geometric Collapse, Emergent Integrated Layered Theory, Computational
Informational Universe Model).

## Core synthesis (what Consensus agrees on)
Epiplexity = structural content a computationally bounded observer can extract
from data, distinct from Shannon entropy (idealized channels, unlimited compute)
and Kolmogorov complexity (unbounded). Key property: **observer-relative** — same
data has different epiplexity for different computational budgets. Decomposes
total description length into epiplexity (learnable structure) + time-bounded
entropy (unlearnable noise). Addresses three paradoxes: (1) deterministic
transformations can create info; (2) data ordering matters; (3) likelihood
modeling can exceed the generating process. Practical measurement: area under
training loss curve above final loss, or cumulative teacher-student KL.

## Directly relevant citations for the paper's Related Work (all citable)

1. **Finzi, Qiu, Jiang, Izmailov, Kolter, Wilson (2026)** — "From Entropy to
   Epiplexity." arXiv:2601.03220. The primary source (already used).

2. **Hu (2026)** — "Speculating for Epiplexity: How to Learn the Most from
   Speculative Design." Extends epiplexity to design/creative artifacts
   (structured epistemic info vs entropic noise). Clip: "learnably surprising."

3. **Li (2026)** — "A Controlled Counterexample to Strong Proxy-Based
   Explanations of OOD Performance." **THE ANTI-RESULT. Critically important:**
   proxy structural measures can FAIL to track task-relevant OOD structure, even
   in a controlled fixed pretraining-and-probing setup. Hardens the paper's §6
   prediction #2/#5 — we must acknowledge a proxy's structural measure may diverge
   from task-relevant structure. This is exactly the circularity/observability
   caveat. MUST cite and address in §8.

4. **Takahashi & Hayashi (2026)** — "Thermodynamic Limits of Physical
   Intelligence." Distinguishes two epiplexity layers (normative mutual-info
   target vs operational compute-bounded MDL). Defines **acquired epiplexity** =
   conditional mutual info: bits about the environment newly encoded in an
   agent's state. Gives thermodynamic bits-per-joule efficiency metrics. This
   connects epiplexity to energy — relevant to the paper's C_anticipate<=C_absorb
   threshold and the hardware-core economics.

5. **Alonso (2026)** — "Financial Epiplexity: A Theory of Learnable Market
   Structure under Bounded Computation." Financial-markets instantiation
   (equal entropy != equal epiplexity; alpha decay as public migration).

6. **Moriondo & Azizi (2026)** — "From Embedding Geometry to Spectral Search:
   Energy Dispersion Networks for Vector Retrieval." Connects epiplexity to
   embedding geometry / spectral search — **directly supports the geometry
   claim** (latent-space topology as the substrate of structural info).

7. **Ohzeki (2026)** — "Non-Equilibrium Model Selection via Finite-Time
   Thermodynamics." Model-selection link (finite-time singular complexity).

## Consensus auto-proposed follow-up questions (== validation of the thesis)
- "Epiplexity and thermodynamic limits of intelligence"
- "How does epiplexity relate to embedding geometry and spectral search?"
These are consensus's OWN suggested directions — i.e., the literature is already
moving toward the geometry/epiplexity/energy convergence the paper claims.

## Noise results to ignore
Epiploic appendages, choroid plexus, hyperekplexia (medical homonym collisions
on "epiplexy"/"epiplex"). Not relevant.

## How to use in the paper
- Add Takahashi & Hayashi acquired-epiplexity + thermodynamic metrics to §2/§4
  (observer/energy grounding).
- Add Moriondo & Azizi to §7 geometry support (spectral search in latent space).
- **Mandatory:** cite Li (2026) anti-result in §6 and §8.1 as the bounded-honesty
  admission — epiplexity (proxy) may not equal task-relevant OOD structure. This
  preempts the strongest reviewer objection and is exactly what the Scarred
  Tissue and circularity critiques demand.
- Alonso + Ohzeki + Hu as breadth in Related Work.
