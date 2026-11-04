# THM-INV working notes

Plan: six digest agents (sonnet) read the sources and write `digests/` (REG = registry/T38/architecture,
API = nine API reports, AREV = Astra reviews A-REV5..9, LIT = five LIT reports + API-POS, SL = Song–Liang 2015,
LITGAP = primary-source pass on the uncovered literature themes). I read THEORY_PRIORITIES, LEDGER,
METHODOLOGY_v3 and the proposal (§§1–5, 7, 11–13) myself. REPORT.md is assembled from these.
Digests are working material, not reviewed; REPORT.md cites the underlying branch files.

## Components of v3 (METHODOLOGY_v3 §§2–9), for the component map
1. Target posterior (g = n, τ = 1, IG(0.01,0.01), BB(1,p) capped at K = ⌊n/2⌋) + reduction (V1).
2. Exact branch (Σ C(p,k) ≤ (5H₀+4N₀)p): enumerate; global_certified.
3. Blocks (complete linkage on 1−|r|, cut at B, next-fit packing), tables r_b(U), composite start π₀ = ϖ∏r_b / Z̄₀
   with exact Z̄₀ by convolution and exact iid draws. [the parallel "split" + "merge"]
4. Discrepancy d(S) and bridge γ_φ = γ₀ e^{φ d}.
5. Neighbour graph (r_n = √(2 log p / n)).
6. Move round: p Gibbs + uniform swap + B neighbour swaps + independence proposal from π₀, random order (self-adjoint).
7. Resampling (multinomial) and pilot adaptive-ESS schedule (0.90), forced steps.
8. Candidate set V and candidate grid (restricted ESS ρ_V), rebuild loop ≤ ℓ, grid_unconverged.
9. Calibration tiers (e ∈ {0,1}), triggers E1–E3 etc., escalation; freeze; FINAL run fresh streams.
10. Islands: R = 4 final islands × N_e (and 4 diagnostic islands) — independent streams; "Islands may run sequentially".
11. Ẑ_r, pooled Ẑ (mean), 0.05·Ẑ Markov lower bound.
12. PIPs: Rao–Blackwellised o_j over 4 measured rounds; primary equal-weight, secondary Ẑ-weighted; MPM.
13. Local search (≤ ℓ moves + scan), local_certified, local_limit; HPM = best-ever-scored; near-tie list; tie rule.
14. Flags: escalated, checks_passed_*, forced_pilot_steps, grid_unconverged, local_limit, low_empirical_ESS, near_tie_truncated.
15. Statuses / resource limits: schedule_limit, numerical_failure, resource_limit (preflight), numerics (Cholesky/QR).
16. Parallel structure: tables (embarrassingly parallel over blocks), islands (R independent), particles within a stage;
    sequential depth = number of stages T + (L+4) rounds + calibration rebuild iterations (≤ ℓ) + tier escalation.
METHODOLOGY_v3 §9 itself lists "not guaranteed": HPM = global mode; accuracy of Ẑ/PIPs at a budget; detection of unreached modes.
