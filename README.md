# Reasoning Core

**Separation Hypothesis for intelligence: a stable reasoning core (judge),
swappable memory (witness), and a router between them.**

This repository is a stake-claim + working draft around the idea that
reasoning competence can be trained *independently of* the factual content it
will later consume — a brain with amnesia, provided with memory. The
theoretical foundation is **epiplexity** (arXiv:2601.03220): the learnable
content for computationally bounded observers, separated from time-bounded
entropy.

## The thesis in one line

Intelligence is a **judge** (small, stable, checks coherence under
perturbation — a bullshit detector), a **witness** (large, swappable, holds
the facts), and a **router** (decides which competence applies). Some
components live in hardware, some in software — same as biology.

## Contents

- `paper/paper_v0.2.md` — the preprint draft: **Occluded Ledger, Separable Reason**
  (hypergraph-ledger rewrite; judge/witness/router; explicit holes-to-fill)
- `paper/paper_v0.1.md` — earlier position draft (riff on the perturbation paradigm)
- `experiments/` — (planned) flip-rate eval rails, epiplexity estimators,
  core-training experiments
- `references/` — source material (epiplexity paper, Sophontic transcript,
  EILT brief, NBLM synthesis transcripts)
- `reasoning_core_nblm.py` — NotebookLM synthesis pipeline (init/synth/status)
- `fire_all_generations.py` — queue all video + audio generations
- `poll_synthesis.py` — poll + download completed artifacts

## Key concepts

- **Separation Hypothesis:** reasoning geometry can be trained from
  high-epiplexity synthetic data (generative grammars, ~zero memorized
  content) and coupled to external memory to recover monolithic-model
  performance.
- **Flip rate:** paired canonical/perturbed evaluation. The pair is the unit
  of measurement. Tracks structure, punishes surface matching.
- **Judge/witness/router:** the three-component decomposition.

## Status

- [x] Position paper draft (v0.1)
- [ ] Flip-rate eval rails (synthetic grammar generator)
- [ ] Epiplexity estimation on rails (using github.com/shikaiqiu/epiplexity)
- [ ] Core-training experiment (small model on perturbation pairs)
- [ ] Transfer + circularity tests (public benchmarks)

## License

MIT (code). CC-BY 4.0 (text).
