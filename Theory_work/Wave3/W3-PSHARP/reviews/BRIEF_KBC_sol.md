# BRIEF KBC — line-by-line proof check (blind first read) — W3-PSHARP

You are an independent checker (gpt-6.1-sol, reasoning effort high). Check the proofs below **line by line** and try
to break them. Assume nothing is right because it looks routine.

## Files under check
- `Theory_work/Wave3/W3-PSHARP/lemmas/B_sparsity.md` (Corollary B, B1 incl. the critical scale, B2, B3)
- `Theory_work/Wave3/W3-PSHARP/lemmas/C_counterexample.md` (Proposition C items 1–3, Lemma P, §4 'What fails')
Statement they must prove: `Theory_work/Wave3/W3-PSHARP/STATEMENT.md` (v1.2). Definitions: `Theory_work/Wave3/W3-POST/STATEMENT.md`
§0 (lines 16-39, the coded target π) and, only where a lemma file quotes them, `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md`
(lines 9-19), `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md` (lines 6-14), `Theory_work/Wave3/W3-POST2/STATEMENT.md` (line 44).
You may read `Theory_work/Wave3/W3-PSHARP/lemmas/S_one_step.md` (Lemma V, Lemma S) as a dependency, and the scripts and
outputs under `Theory_work/Wave3/W3-PSHARP/numerics/`. Read nothing else in `Theory_work/Wave3/W3-PSHARP/` (no LOG, PLAN,
CHECKPOINT, ASSUMPTION_MAP, and nothing under `reviews/` except this brief). You may run code (`py -3.13 -I`; numpy,
scipy, mpmath); keep it under `Theory_work/Wave3/W3-PSHARP/reviews/KBC_scratch/`.

## What to do
1. Re-derive every display and every inequality, with its constants and its domain (n, p, s₀, K, d, τ, ranks, empty
   sets). For each step say: VERIFIED, or what is wrong and the exact repair.
2. Check that each proof proves **exactly** the corresponding item of STATEMENT v1.2 — no stronger hypothesis used
   silently, no weaker conclusion reached; list every statement item that is not covered by a proof.
3. Check every probabilistic step: what is random, what is conditioned on, which independence is used, uniformity.
4. Test numerically whatever can be tested (identities on random small cases; explicit constants at the boundary
   of their domain).
5. Specific attack points: B — the closed form of the sum, the constants, the critical-scale limit (exchange of limit
   and sum; K − s₀ → ∞), B2's use of O_P. C — existence and standardisation of the design; Lemma P when S contains
   x₁ and/or x₂; every numerical constant in §2–§3 for all n ≥ 200 (k = ⌈12 log n⌉ has ceiling effects: scan n);
   the event F_n; the chain Δ ≥ nb²/10 → fit ≤ exp(−nb²/(42V₀)) → c₁ = 1/(73V₀); whether §4 states accurately what
   Lemma 1a′ and Lemma 1a″ assert and what fails; the last claim about cost allowances B_n.

## Output
Write the full check to `Theory_work/Wave3/W3-PSHARP/reviews/KBC_check_sol.md`: per file a verdict
`VERIFIED` / `VERIFIED-WITH-AMENDMENTS` / `GAP` / `WRONG`; findings labelled FATAL / MAJOR / MINOR / NIT with exact place
(file:line) and exact correction. Change no file other than your check file and scratch directory; do not commit;
start no subagents. Reply with the per-file verdicts and the counts of findings by severity.
