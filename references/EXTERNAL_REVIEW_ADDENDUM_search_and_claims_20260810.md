# Addendum to EXTERNAL_REVIEW_v03 — search surface, domains, claim propagation

**Date:** 2026-08-10 (later same day)
**Companion to:** EXTERNAL_REVIEW_v03_20260810.md
**Trigger:** search audit of the public identity ahead of preprint publication

---

## 1. Claim propagation — the RLHF finding has escaped

Google's AI summary for "gene yanenko" now states, as fact:

> "A key finding in his research corpus indicates that Reinforcement Learning from Human Feedback (RLHF) false-positive cascades — rather than genuine malicious alignment shifts — are a dominant cause of system failure, which multi-agent setups are better equipped to survive."

Attribution given: **themachinesoflovinggrace.com** — i.e. the site, not a video. The site copy is the authority being read.

**Why this matters now specifically.** Paper A's entire posture is pre-registration, stated falsifiers, and withdrawn claims marked as withdrawn. A reviewer doing due diligence will search the author and find a search engine asserting an unpublished, unvalidated claim as an established research finding. That is the one thing that could make the paper's epistemics look performative rather than real.

**Root cause on the site (three locations, only one of which was hedged):**

| Location | State before | Fixed |
|---|---|---|
| §01 Research Thesis | "The central finding so far: … RLHF false-positive cascades … were the dominant failure mode" | Now: "Preliminary observation, not a result… single-deployment observation from an unvalidated self-audit… should not be cited as a finding" |
| §04 Case Study action block | "ARCHIVED FINDING: RLHF false-positive cascades were the dominant safety-system failure mode" | Now: "PRELIMINARY OBSERVATION (UNVALIDATED)… labeling pass pending" |
| §04 same block | "Convergent with Anthropic research published May 2026" | Now: "Compared against… comparison, not replication" |
| Feature card 02 | already carried the withdrawal note | unchanged — this one was correct |

The Thesis section was almost certainly the scraped source: it is the first substantive prose on the page and stated the claim most strongly.

**Standing rule going forward:** any claim on the public site is a claim a summarizer will restate without its qualifiers unless the qualifier is inside the same sentence. Hedges in a neighbouring paragraph do not survive summarization. Put the caveat in the clause, not the context.

---

## 2. Domain architecture — do not split yet

Currently held: fus10n.net, themachinesoflovinggrace.com, themachineoflovinggrace.com. Plan under consideration was to split research / ClawHorde / personal across all three, cross-linked.

**Recommendation: don't.** Google is already treating themachinesoflovinggrace.com as a distinct source for content that also lives on fus10n.net — that is split authority, not redundancy, and it is likely one reason indexing outside Google is thin.

Better: one canonical domain, separation by path or subdomain.

- `fus10n.net` — canonical, research
- `fus10n.net/horde` or `horde.fus10n.net`
- `fus10n.net/personal` or the existing `/the_cybernetic_architect.html`
- 301 both `themachine(s)oflovinggrace.com` → `fus10n.net`, or set `rel=canonical`

Everything compounds into one index. The other domains stay registered as defensive holdings and can be split later once there is authority worth splitting.

---

## 3. Search surface, measured

Searched 2026-08-10 against a non-Google index:

**Surfaces:** LinkedIn (top hit, cached ~March — still leads with "IT transformation, data center operations, and Microsoft enterprise environments"), Quora, Instagram, one EILT YouTube video, and `fus10n.net/?p=1` — the default WordPress "Hello world!" post from January, still live and indexed.

**Does not surface:** github.com/Godsend, reasoning-core, ClawHorde, the paper, anything from the last two weeks.

**Actions:**
- [ ] Delete the WordPress default post at `/?p=1`
- [ ] Update the LinkedIn About — it is the single paragraph Google quotes verbatim under "Professional Background"
- [ ] Link the GitHub repo from fus10n.net so crawlers find it

**Name collision note:** "Machine of Loving Grace" alone is unwinnable as a search term — Brautigan, Adam Curtis, Markoff, Amodei, an industrial rock band, a CalArts exhibition, a typewriter collection. The personal name is the only disambiguator. Always pair them.

---

## 4. Terminology drift — freeze before publication

Three strings currently in circulation for the same framework:
- **Emergent Informational Ledger Theory (EILT)** — papers, applications
- "Emergent Integrated Layered Theory" — earlier site copy (corrected)
- "Informational Ledger Theory (ILT)" — Google's current summary

Below publication threshold this costs little. Above it, citations will not converge. **Pick the canonical string before the preprint ships, and use that exact string identically in the paper, the repo, the site, and the abstract.** After that, downstream acronym drift is harmless because citations resolve to the published form.

---

## 5. Observation worth filing as data

The mechanism that produced the Google summary is the same one behind two earlier incidents in this corpus:

1. **Corvo (July 2026)** — retrieval stripped provenance from genuine prior-session content; the receiving agent correctly distrusted true information and wrongly concluded fabrication.
2. **The 217 figure** — an unvalidated automated self-audit propagated across documents for months as an established number.
3. **This** — high-volume synthetic content plus site copy summarized into an authoritative third-party statement of a finding that has no published evidence, with provenance discarded in the summarization step.

Same failure: **provenance does not survive summarization**, and confidence is manufactured at each hop. Three independent instances, all timestamped, all in one corpus, one of which has the author's own claim as the payload.

This is a stronger empirical anchor for the companion paper than any of the cosmology, and it is worth writing up as a standalone incident note.
