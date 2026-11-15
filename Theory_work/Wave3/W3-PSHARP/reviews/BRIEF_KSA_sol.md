# BRIEF KSA — line-by-line proof check (blind first read) — W3-PSHARP

You are an independent checker (gpt-6.1-sol, reasoning effort high). Check the proofs below **line by line** and try
to break them. Assume nothing is right because it looks routine.

## Files under check
- `Theory_work/Wave3/W3-PSHARP/lemmas/S_one_step.md` (Lemma V, Lemma S)
- `Theory_work/Wave3/W3-PSHARP/lemmas/A_log_factor.md` (Lemma W, Lemma R, Proposition A under both witnesses, Corollaries A1–A2, remarks)
Statement they must prove: `Theory_work/Wave3/W3-PSHARP/STATEMENT.md` (v1.2). Definitions: `Theory_work/Wave3/W3-POST/STATEMENT.md`
§0 (lines 16-39, the coded target π) and, only where a lemma file quotes them, `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md`
(lines 9-19), `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md` (lines 6-14), `Theory_work/Wave3/W3-POST2/STATEMENT.md` (line 44).
You may read `Theory_work/Wave3/W3-PSHARP/lemmas/S_one_step.md` (Lemma V, Lemma S) as a dependency, and the scripts and
outputs under `Theory_work/Wave3/W3-PSHARP/numerics/`. Read nothing else in `Theory_work/Wave3/W3-PSHARP/` (no LOG, PLAN,
CHECKPOINT, ASSUMPTION_MAP, and nothing under `reviews/` except this brief). You may run code (`py -3.13 -I`; numpy,
scipy, mpmath); keep it under `Theory_work/Wave3/W3-PSHARP/reviews/KSA_scratch/`.

## What to do
1. Re-derive every display and every inequality, with its constants and its domain (n, p, s₀, K, d, τ, ranks, empty
   sets). For each step say: VERIFIED, or what is wrong and the exact repair.
2. Check that each proof proves **exactly** the corresponding item of STATEMENT v1.2 — no stronger hypothesis used
   silently, no weaker conclusion reached; list every statement item that is not covered by a proof.
3. Check every probabilistic step: what is random, what is conditioned on, which independence is used, uniformity.
4. Test numerically whatever can be tested (identities on random small cases; explicit constants at the boundary
   of their domain).
5. Specific attack points: Lemma W(ii) (sphere density, the Gamma-ratio bound, the two-sided bound on e^{t²/2}h_d(t));
   Lemma R (the ϵ-bookkeeping); §3 (the bound on V and the fact that the g_j also enter V); §4 (conditional law of
   the ζ_j; the identity for Q_{S₀} − ‖ρ̃‖²; the bound with rank r₀ and no eigenvalue floor; the three events and
   their probabilities); §5 (transfer to random (X_{S₀}, θ*)); §6 (A1: odds → δ_n and the expectation; A2 (i), (ii));
   Remark 2 (do the two example sequences satisfy what is claimed, read against W3-POST STATEMENT §2 and Corollary 1R).

## Output
Write the full check to `Theory_work/Wave3/W3-PSHARP/reviews/KSA_check_sol.md`: per file a verdict
`VERIFIED` / `VERIFIED-WITH-AMENDMENTS` / `GAP` / `WRONG`; findings labelled FATAL / MAJOR / MINOR / NIT with exact place
(file:line) and exact correction. Change no file other than your check file and scratch directory; do not commit;
start no subagents. Reply with the per-file verdicts and the counts of findings by severity.
