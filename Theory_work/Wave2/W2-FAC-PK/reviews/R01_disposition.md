# R01 disposition (statement lock, Codex Sol high: REJECT)

Reviewer reply verbatim: reviews/R01_statement_lock_sol.md. Every item is applied in STATEMENT v2 or made moot by the
change of route for (P3); none is argued away.

1. **Scope.** Applied. STATEMENT v2 §0 flags the narrowing: exact-Gram stage K < p ≤ n − 1 only; p ≫ n kept as open
   deliverable (F1) with W2-SIM R3 requested; (P2) frontier K < p ≤ (16/15)K stated (F2).
2. **False "argmin-retained out" swap rule.** Accepted (the reviewer's formula V = (1 − γ)τ_l² + 2γτ_lτ_j − (1 + γ)τ_j² and
   the N2 counts are correct). Moot for the proofs: the dynamic plan (swap phase / band / deletion invariants) is
   abandoned. The new route (L3) uses only lower bounds on the best *deletion* gain at every set above S₀ (the chosen
   move gains at least that much, whatever it is), so no swap-selection rule is used. L2 (NEG) also uses only "some swap
   gains more than every deletion", never which swap. PLAN v2 updated.
3. **Transition/deletion invariants, W ≤ p − K, empirical regularity.** Moot: (P3) no longer claims phase structure or
   W ≤ p − K; it claims "path ends at S₀ and m* ≤ (1 + δ)K", proved by static gain bounds plus an F-budget — exactly the
   reviewer's suggested fallback ("a bounded-total-move theorem sufficient for discovery").
4. **P1 uniformity.** The within-block exchange in L1(b) already uses the factorised form (gap × positive bracket); the
   bracket bound is uniform on E^S_n. L1.2 gives the population discrete-concavity gap of the block log-table
   (second differences ≤ −c_g n) and the uniform perturbation bound |ν log(1 − N_U/ψ(u))| ≤ C√n H̄; (c) is derived from
   both. Kept; wording checked.
5. **Truth retention at saturation; partition.** (TK) and the truth-retention claim are dropped: L3/L3.4 handle a start
   missing truths (phase A: every size-K set without S₀ has a swap gaining ≥ c₃n, so at most O(log n) such moves). (PB)
   is stated as a hypothesis; the consecutive partition of the coded rule is a remark with numerical checks only.
6. **P2(ii).** Applied: threshold renamed t_n; the count N_n ≥ n^{1/2−o(1)} (t_n² = log n + O(√log n)) supports every
   β < ½; "first ⌊n^β⌋ moves are swaps" stated as Lemma L2.3 (separate from the scoring consequence); nonnegative integer
   caps; [OP] wording "upper bound asymptotically uninformative; no lower bound on D_n". The uniform centre/retained-point
   and missing-truth bounds are in L2.2 (i)–(iii).
7. **Doubling ≠ minimal.** Applied: (P4) is stated for every cap ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉) and lists alternatives
   (ℓ_n + ⌈(1 + δ)|S̃₀|⌉; under (PK) max(ℓ_n + |S̃₀|, p)); (P5) states what "minimal" means: allowances ≤ n^β fail,
   ≥ δ|S̃₀| suffice, no optimality claim. (The reviewer's max(ℓ_n, p) argument relied on W ≤ p − K, which is no longer
   claimed; max(ℓ_n + |S̃₀|, p) is covered via p ≥ (1 + 1/16)K under (PK).) METHOD_REQUIREMENTS.md to be revised
   accordingly.
8. **P6.** Applied: pending; the three resource_limit attempts are recorded as operational outcomes (preflight LS0
   worst-case charge ≈ 146 h at n = 600, p = 450), not as discovery failures; completed runs requested from W2-SIM R2
   with source revision. PLAN no longer allows P6 to be labelled checked.
9. **P4 obligations.** Applied in STATEMENT (P4)(iii) and to be carried in L4: Lemma S extension, Proposition F/A2
   no-output argument with all premises, direct use of P(LS0 scores S₀) → 1 through D′'s pathwise inclusion, explicit
   score-request bound 1 + (ℓ_n + 2K + 1)q(p); FACB L4.0(d)'s M_T ≤ 1 + o(1) is not imported (L3 (E4) replaces it by a
   uniform bound M_T ≤ C_M valid for p ≤ n − 1). (P5) restricted to LS0 worst-case terms.
10. **Numerics.** Applied: N1 recount 53/60 MR1 misses (all saturated), 0/60 with ℓ_n + 2|S̃₀|; deletions = |S̃₀| − s₀;
    N3 frozen at 360 rows (N3_raw_final360.jsonl, FROZEN_SNAPSHOTS.sha256).
