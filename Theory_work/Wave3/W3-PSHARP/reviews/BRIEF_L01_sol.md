# BRIEF L01 — statement-lock review (blind first read) — W3-PSHARP

You are an independent reviewer (gpt-6.1-sol, reasoning effort high). Your job is to **break the statement** before
any proof is written. You are not asked to be constructive first; you are asked to find what is wrong, ill-posed,
false, or weaker/stronger than it says.

## What to read (and nothing else in `Theory_work/Wave3/W3-PSHARP/`)
- `Theory_work/Wave3/W3-PSHARP/STATEMENT.md` (v1.0) — the object under review.
- Definitions it relies on: `Theory_work/Wave3/W3-POST/STATEMENT.md` §0 (lines 16-39: the coded target π) and §1-§2
  (Lemma 1a′, Theorem 1, Corollary 1R as referred to); `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md` (lines 9-19:
  statement of Lemma 1a′; Remark 2); `Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md`;
  `Theory_work/Wave3/W3-POST2/STATEMENT.md` (Claims A2, B, C; line 44); `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md`
  (lines 6-14: statement of Lemma 1a″).
Do not read any other file of this ticket (no PLAN, LOG, numerics, other reviews). You may run your own small
computations (Python: `py -3.13 -I`, numpy available) to test claims; keep any script you write under
`Theory_work/Wave3/W3-PSHARP/reviews/L01_scratch/`.

## What to check
1. **Well-posedness.** Every object defined; domains (n, p, s₀, K) consistent; each hypothesis satisfiable; the witness
   designs exist; quantifiers and modes of convergence unambiguous ("uniformly", "in probability", "surely").
2. **Truth.** For each numbered item of Lemma S, Proposition A (+ Corollaries A1, A2, Remark A3), Corollary B
   (+ B1-B3) and Proposition C (items 1-3): try to derive it or to refute it. Derive the algebraic identities yourself
   (Schur complements, prior ratios, the constants c(p, s), the cutoff bound in C.2, the constants C_b, n₀). Test
   small cases numerically where you can (exact enumeration of π for small p). Look for a counterexample to each
   claim, especially: Lemma S items 1-2 (equality case, sign), the constant 1/√π and the factor 2N_n/(2p − 1 − s₀) in
   Λ_n, the claim that (W-sph) covers p ≫ n, the "surely" statements in B1, the claim B2, and Proposition C item 3.
3. **Faithfulness to the parents.** Does Proposition C really keep every hypothesis of Lemma 1a′ except the
   coefficient bound, and does its conclusion really contradict the conclusion of Lemma 1a′ / Lemma 1a″ for the
   reference T? Does Corollary B really contain Proposition LB? Is Remark A3 right that the two example sequences
   satisfy the hypotheses of Theorem 1 / Corollary 1R?
4. **Overclaiming / underclaiming.** Anything stated more strongly than can be true; anything obviously true in a
   stronger form at no cost.

## Output
Write your full review to `Theory_work/Wave3/W3-PSHARP/reviews/L01_statement_lock_sol.md`:
- a verdict line: `LOCK`, `LOCK-WITH-AMENDMENTS`, or `DO-NOT-LOCK`;
- findings, each labelled FATAL / MAJOR / MINOR / NIT, with the exact place (file:line) and the exact correction
  you propose; say for each claim item whether you derived it, tested it numerically, or could not check it;
- do not change any file other than your review file and your scratch directory. Do not commit.
Reply with the verdict line and the counts of findings by severity.
