# C-DLV — PLAN (v1)

1. Statement lock: Codex gpt-6.1-sol (high) cross-checks INVENTORY.md against the production code (every path:line,
   completeness, classification) and STATEMENT.md/PLAN.md against SoP (02_method, 04_theory, A_notation). Fix → lock.
2. Lemma files (lemmas/):
   - L1_resources.md — Lemma R: operation and word counts per phase (setup, tables, pilot, diagnostics × ≤ ℓ rebuilds ×
     2 tiers, V/grid construction, final islands, local searches, LS0 (PXN (K) count), exact branch), explicit W̄, M̄;
     guard rule elapsed+op > allocation ⇒ allocation ≥ 2·total suffices.
   - L2_degenerate.md — Lemma S: P = 0 events; EX-A ⇒ scorer never throws (PD argument, Q_S ≥ yᵀy/(n+1)).
   - L3_grid.md — Lemma G: convexity of F_V, ρ_V(u,v) = exp{−Δ²F}, Δ²F ≤ (v−u)² sup Var; pilot schedule properties
     (strictly increasing, ends at 1, ≤ T_e steps); construction appends every target ⇒ returns the pilot schedule.
     Λ_V ≤ Ψ_n when S₀ ∈ V (q_t^V(S) ≤ γ_t(S)/γ_t(S₀); log-linearity in t ⇒ endpoint max).
   - L4_delivery.md — Theorem D: assembly over tiers/rebuilds; S₀ ∈ V persistence (leader store keeps the γ₁-maximiser).
   - L5_classes.md — (D7)(a) Ψ_n → 0 conditions on favourable designs; (D7)(b) masked: Ψ_n → ∞, two-state N_b bound,
     residual obstruction.
3. Numerics (Sonnet helper, numerics/BRIEF_numerics.md): production core on masked and favourable LH-type designs at
   increasing (n,p): statuses, N_p, N_b, T_e, S₀ ∈ V, Λ_V < c₀. Plus exact Ψ_n on small-p designs (enumeration) — lead.
4. Lemma checks (Codex, one per lemma file, fresh each), falsification numerics per lemma.
5. Mid-point (fresh Codex, STATEMENT + proofs only) after L3/L4.
6. Exhaustive sweep, CITECHECK, council (Codex + Opus), CHECKPOINT at 01:30, REPORT by 04:30.
