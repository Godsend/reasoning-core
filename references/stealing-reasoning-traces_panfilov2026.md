# External Reference: Stealing Reasoning Traces from Proprietary LLM APIs

**arXiv:2608.09867** (cs.CR) — Submitted 10 Aug 2026
https://arxiv.org/abs/2608.09867 | https://arxiv.org/html/2608.09867v1

**Authors:** Alexander Panfilov, David Schmotz, Ilia Shumailov, Luca Beurer-Kellner,
Joachim Schaeffer, Ameya Prabhu, Jonas Geiping, Maksym Andriushchenko

## Why this matters to the Separation Hypothesis

This paper is direct, real-world corroboration that **reasoning trajectories are a
separable, transferable, and distillable thing in their own right** — the core claim
of Paper A's Separation Hypothesis (judge + swappable witness, reasoning trained
independently of the content it consumes).

### The three findings most relevant to us

1. **Encrypted CoT is replayable across the provider's model ecosystem.**
   Opus 4.8's encrypted reasoning blob, injected into Haiku 4.5 (a weaker, less
   safeguarded sibling) with a jailbreak prompt, makes Haiku transcribe Opus's hidden
   reasoning verbatim — recovered-token counts matching billed "thinking tokens"
   almost 1:1. The anti-distillation "protection" is a cryptographic side channel:
   a globally-shared encryption key (stateless architecture) makes the blob portable
   across sessions/users/models.

2. **Reasoning-as-fingerprint measurement.** The authors measure how few queries a
   model needs to reproduce the *next 16 tokens* of a source reasoning trace. This is
   a flip-rate-style metric for reasoning-memory entanglement — the same axis Paper A
   tries to isolate between the judge (stable reasoning core) and witness (memory).
   Kimi-K3 needed 4-6 orders of magnitude fewer queries than DeepSeek-V4-Flash /
   Inkling to reproduce Claude/GPT reasoning fragments.

3. **Reasoning prefix shifts behavior (style drift).** Feeding Kimi-K3 only the first
   1% of Opus's decoded reasoning changed its *visible* answer style toward Opus's,
   with n-gram overlap tracking Opus's real output. Control (Inkling) showed no shift.
   The reasoning path itself, not just the answer, is the transferred signal.

### Methodological resonance

- Their "extract → fingerprint → reproduce next-N-tokens" protocol is structurally
  similar to Paper A's proposed flip-rate / trace-intersection methodology.
- Their finding that reasoning is *distillable as a thing* supports the Separation
  Hypothesis' claim that a reasoning core can be trained from epiplexity-dense traces
  (arXiv:2601.03220, Finzi et al.) independent of downstream factual content.
- Cautions: the paper itself notes fingerprints are evidence *consistent with*
  distillation, not proof of it — the same epistemic discipline Paper A applies
  (hypothesis-for-testing, not settled claim).

### Cautionary counterpoint (why this is not naive)

This is also evidence that "reasoning can't leak because CoT is encrypted" is false.
Any safety framing that relies on hidden reasoning as a protected layer must account
for cross-model replay attacks. For our judge/witness separation: if reasoning traces
are this portable and replayable, the *judge* (reasoning core) is the durable asset,
and the *witness* (memory/CoT) is even more swappable than we assumed — arguably
strengthening the separation thesis.

## BibTeX

```bibtex
@article{panfilov2026stealing,
  title={Stealing Reasoning Traces from Proprietary {LLM} {APIs}},
  author={Panfilov, Alexander and Schmotz, David and Shumailov, Ilia and
          Beurer-Kellner, Luca and Schaeffer, Joachim and Prabhu, Ameya and
          Geiping, Jonas and Andriushchenko, Maksym},
  journal={arXiv preprint arXiv:2608.09867},
  year={2026}
}
```

## Related coverage
- Reddit r/LocalLLM thread: /r/LocalLLM/comments/1vljw88/
- HN: news.ycombinator.com/item?id=49257876
- Nathan Lambert (comment): "likely one of the most influential scientific papers this year"
