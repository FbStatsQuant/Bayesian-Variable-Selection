# Statement-lock round 2 — disposition (lead, 2026-11-11)

Reviews: `reviews/SL2_statement_lock_sol.md` (fresh blind Sol; verdict LOCK WITH CHANGES; digest 3c89e73a… quoted) and
`reviews/RC2_reconciliation_sol.md` (reconciliation Sol; "ALL CRITICAL/MAJOR RESOLVED: yes"; one PLAN edit).

| # | class | finding | disposition (STATEMENT v1.2) |
|---|---|---|---|
| SL2-1 | CRITICAL (local) | §0 (iv) used the upper exponent A for the weak-truth limit; (N3) correctly uses liminf log p/log n | APPLIED verbatim: §0 (iv) now refers to the hypotheses and quantifiers of (N2), (N3) with Ā and A̲. (N2)/(N3) unchanged. |
| SL2-2 | MINOR | valid inputs allowed p = 0 | APPLIED: "at least one retained non-constant predictor (p ≥ 1)". |
| SL2-3 | MINOR | IF-START: κ range must be positive | APPLIED: 0 < κ < κ_V. |
| SL2-O1 | optional | qualify "o₀ → 0 forces Ξ → 0" by s₀ + 16 ≤ K | APPLIED in (AGG-b). |
| SL2-O2 | optional | give c_n; θ*_min only for s₀ ≥ 1 | APPLIED in §1. |
| SL2-O3 | optional | §6: narrow the saturated-model exclusion | APPLIED. |
| RC2 | — | PLAN.md displayed max{T₁, c_sΞ} ≤ o₀ without the feasibility condition | APPLIED: PLAN §2 item 1 now states the conditions (s₀ < K, U < 1; s₀ + 16 ≤ K for the Ξ lower bound). |

Result: **STATEMENT v1.2 is LOCKED.** Every change above is the reviewer's exact edit; no hypothesis or claim of §5 changed
between v1.1 and v1.2. The blind reviewer's "Not checked" list (full proofs of AGG, (B-V1)/(B-V2) remainders, finite-n
uniformity, (B-R), OVL) is the proof work of CP2/CP3.
