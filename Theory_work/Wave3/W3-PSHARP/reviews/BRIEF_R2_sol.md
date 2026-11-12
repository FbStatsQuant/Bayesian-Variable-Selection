# BRIEF R2 — council seat `sol` (blind first read) — W3-PSHARP

You are one of two independent council seats (gpt-6.1-sol, reasoning effort high). You decide whether the frozen content below is correct and
honestly reported. Be adversarial: a pass from you means you re-derived the mathematics, not that it read well.

## Content under review (frozen as `MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14`, file `Theory_work/Wave3/W3-PSHARP/reviews/MANIFEST_R2.txt`)
Everything in `Theory_work/Wave3/W3-PSHARP/` **except** `reviews/`, `LOG.md`, `CHECKPOINT_*.md`:
`STATEMENT.md` (v1.2.2), `lemmas/S_one_step.md`, `lemmas/A_log_factor.md`, `lemmas/B_sparsity.md`,
`lemmas/C_counterexample.md`, `REPORT.md`, `ASSUMPTION_MAP.md`, `PLAN.md`, `BRIEF.md` (the ticket's task),
`citecheck.py` (you may run it; it also reads `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md` lines 72-79), `numerics/` (scripts and outputs).
External inputs (definitions and the statements being sharpened; listed in `reviews/INPUTS.txt`):
`Theory_work/Wave3/W3-POST/STATEMENT.md` (§0 lines 16-39 define the coded target π), `W3-POST/lemmas/L1a_size_tail.md`,
`W3-POST/lemmas/LB_rate_lower_bound.md`, `W3-POST/REPORT.md`, `Theory_work/Wave3/W3-POST2/STATEMENT.md`, `W3-POST2/REPORT.md`,
`W3-POST2/lemmas/A_occam.md`, `W3-POST2/lemmas/B_tail_approx.md`. For G6 you may also read the code that defines the
target: `Scripts/SMC_BVS/core/cpp/v3_score.h` (lines 40-71, 196-224).
**Do not read** anything else under `Theory_work/Wave3/W3-PSHARP/reviews/` (no other brief, review, disposition,
scratch or score), nor `LOG.md`, nor `CHECKPOINT_*.md`. You may write and run code (`py -3.13 -I`; numpy, scipy,
mpmath); keep it under `Theory_work/Wave3/W3-PSHARP/reviews/R2_scratch_sol/`. Change no other file; do not commit;
start no subagents.

## What the ticket claims
Three sharpness records (lower bounds / a counterexample) for the posterior of a Bayesian variable-selection method,
each proved from the definition of π alone: Lemma S; Claim A (Proposition A, Corollaries A1–A2; Remark A3 is a
reading, conditional on parent results for the upper bound); Claim B (Corollary B, B1–B3); Claim C (Proposition C).

## Gates (each PASS or FAIL, with reasons)
- **G1 correctness.** Re-derive every proof step of the four lemma files (identities, inequalities, constants,
  probabilistic steps, limits). Try to refute each claim, including numerically on small exact cases.
- **G2 hypotheses used = stated.** Each proof uses exactly the hypotheses of its statement item and proves exactly its
  conclusion; every item of STATEMENT v1.2.2 is covered.
- **G3 no hidden assumptions.** Domains (n, p, s₀, K, ranks, empty sets), uniformity claims, what is random, what is
  conditioned on, independence actually available.
- **G4 statuses and citations.** Statuses are stated verbatim and not inflated; cited line ranges say what is
  claimed; the REPORT does not present a parent's result as proved here, nor a numerical observation as a theorem;
  the "what fails" reading of Lemma 1a′ / Lemma 1a″ in Claim C is accurate.
- **G5 constants and rates.** Λ_n and its constant 1/√π; c(p, s₀), 𝒪^{lb}_n, the e^{−λ/2} limit; every constant of
  Claim C (k = ⌈12 log n⌉, n₀ = 200, C_b = 1200, c₁ = 1/(73(σ*²+b̄²)), the cutoff bound) for **all** n ≥ 200.
- **G6 fidelity to the coded target and to the numerics.** The π used is the coded one; the numerics compute what
  they say (re-run or re-implement what you doubt) and the REPORT describes their scope honestly.

## Output
Write your review to `Theory_work/Wave3/W3-PSHARP/reviews/R2_council_sol.md`: the six gate verdicts with reasons;
findings labelled FATAL / MAJOR / MINOR / NIT with exact place (file:line) and exact correction; an overall score
(0.0–10.0, one decimal; ≥ 8.0 means "correct and honestly reported; remaining findings are minor").

## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14` (round R2, seat `sol`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14 seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.

Reply with your score, the gate verdicts and the counts of findings by severity.
