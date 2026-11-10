# W3-SCR — council round 1, Claude seat (Opus 5.5, effort high)

Scope: STATEMENT.md v3.3, CODE_CHECK.md, lemmas L1-L7, ASSUMPTION_MAP.md, the production core
(`Scripts/SMC_BVS/core/`, v3_fit.R, v3_run.R, v3_exact.R, v3_preprocess.R, cpp/v3_engine.h, v3_core.cpp, v3_ledger.h,
v3_score.h, v3_start.h), PROGRAM.md item 5, PROTOCOL.md. I did not read the other seat's report. Everything was re-derived
by hand. Independent numerical spot checks are in `reviews/C1_scratch_opus/check.py` → `check_out.txt`.

## 1. Gate verdicts

| Gate | Verdict | Justification |
|---|---|---|
| G1 correctness of every step | **PASS** | Every displayed inequality in L1-L7 re-derived. No incorrect step found (§4). M4 uses "for large n" steps that rely on κ, b, M being fixed (finding 1). This is a statement-convention issue, not a wrong step. |
| G2 hypotheses used = hypotheses stated | **PASS** | Each theorem's hypotheses match what its proof consumes: SCR-A ← MC; SCR-A° ← MC°; A∞/A°∞ ← liminf conditions plus q_n log p = o(n) and ‖μ‖ = o(nσ); A1/A1° ← φ^d floor plus the growth conditions; SCR-M ← nothing beyond Model G and EX-A; M1/M5 ← positive gaps; SCR-C ← NF plus s₀ = O(1), ‖θ*‖₂ = O(σ√n). One caveat: A1 does not say that κ, b, M are fixed. A1 itself does not need it, but M4/SCR-G does (finding 1). |
| G3 no hidden assumptions | **PASS** | The witness is deterministic (one Gaussian per model, so the union bounds are valid). The event families are deterministic. Every certified endpoint is LO through CC1-CC3. Additions exist because \|S\| ≤ q ≤ K−1. The argument uses nothing about the seed, uniforms, start mode, leakage or calibration: the inclusion {∃C ∈ 𝒞 : …} ⊆ 𝓔ᶜ holds pointwise for every seed. |
| G4 status of cited results | **PASS** | External results: Laurent–Massart Lemma 1; Gaussian concentration for Lipschitz functions (BLM 2013 Thm 5.6); the Gaussian maximal inequality and width ≤ √dim; Schur-complement and block-inverse identities; Gaussian tail T1. All are standard. Every internal citation points to a lemma proved in the package. Code facts are checked in §4. |
| G5 constants and rates tracked | **PASS** | Recomputed: T_n, ρ̄_n, the 1.02 terms, ϑ°_n, the 3e^{-x} and 4e^{-x} budgets, c₁ = κ²b²/(200(M²+σ²)) (ρ² ≥ 200/64), A1° (16 and 576, ρ°² ≥ 2), c₂ = κ²b²/(104(M²+σ²)) (n ≥ 34 step), B_n and its bounds, (EC′) including 1 − 1.02/n and η_n, the SCR-C budget (ε/2)𝐋 − O(√𝐋). All are correct. The o(1) terms in A∞, A°∞ and SCR-C are uniform in the model and in m. |
| G6 fidelity to the code | **PASS** | CC1-CC6 hold on the current tree. Line references are exact, and 8/8 hashes recomputed match SHA256SUMS_source.txt. The only non-emitting evaluation is the final search's initial centre (the HPM), so every scanned neighbour reaches the HPM running best. `scan_complete` is always 1. `scanned_F` and `hpm_F` are on the same scale (log prior + log m), so SCR-G is stated correctly in printed quantities. The scorer's Q, the determinants and the prior match §0. |

## 2. Score

**8.9 / 10.** The package is correct and complete. I found no blocker and no major issue. One MINOR point: the
fixed-constant convention needed by M4/SCR-G is not stated. The rest are NOTE-level documentation items. This is a
careful package: the reduction to deterministic families with a deterministic witness, the separation of the
certificate (CC) from the probability (L2/L7), and the handling of uncertified runs (M2/M5 with CC6) are all sound.

## 3. Findings

**1. MINOR — A1 / SCR-G: κ, b, M are not declared fixed, but M4 needs it.**
- *Location:* `STATEMENT.md` A1: "Assume φ^d_n(q_n) ≥ κ > 0 …, θ_min ≥ b > 0, ‖θ*‖₁ ≤ M, σ fixed". SCR-G: "Assume the
  hypotheses of Corollary A1 …". `L7_master.md` M4: "√(g⁻_S) ≥ √Γ_n(q_n) − σ r_n ≥ κb√n/5 for large n" and
  "B_S ≤ … = o(n) … δ_S ≥ nu*/2 − o(n) > nu*/4".
- *What is wrong:* only σ is said to be fixed. M4's "for large n" steps need σ r_n = o(κb√n) and B_S = o(n·u*), that
  is, κb/τ_* bounded below.
- *Derivation:* if κ, b, M may depend on n, the A1 growth condition alone gives only
  σ r_n ≤ σ√(2𝐋_n) + O(σ(log n)^{1/4}) ≤ κb√n/10 + lower order. With √Γ ≥ κb√n/4 this yields
  √g⁻ ≥ 0.15κb√n, not κb√n/5. So the constant 104 in c₂ is not established in that reading. The order-n gap survives
  with a worse constant.
- *A1 itself is not affected.* The step "let n be so large that √(κ(n−1))b ≥ 2M/√(n+1)" can be replaced by an
  every-n argument. The definition of φ^d at S = ∅ gives κ ≤ ‖θ*‖₁²/‖θ*‖₂². The growth condition gives
  κ²b² ≥ 200‖θ*‖₁² log n/n. Hence κb² ≥ 200‖θ*‖₂² log n/n, so κb²(n²−1) ≥ 4‖θ*‖₂², which is √(κ(n−1))b ≥ 2c_θ, for
  every n ≥ 3.
- *Fix:* write "κ, b, M > 0 and σ fixed (independent of n)" in A1, and therefore in SCR-G. Alternatively, restate M4
  with explicit constants valid for n-dependent κ, b, M. Optionally, replace the "large n" step in the A1 proof by the
  every-n argument above.

**2. NOTE — `ASSUMPTION_MAP.md`, AF/DF row: the attainment claim is not proved in the package.**
- *Location:* "The square κ² in Γ ≥ κ²nθ²_min is attained for card(T) ≥ 2 (masked pair) and absent for card(T) = 1."
- *What is wrong:* the map says "Necessary is used only where a proof is cited", but no proof or construction is cited
  for this claim.
- *Derivation:* the claim is true. Take S₀ = {1, 2}, θ* = (b, b) and corr(x₁, x₂) = −(1−κ). Then
  φ^a_n(0) = φ^d_n(0) = κ, and Γ_n(0) = γ(1|∅) = (n−1)²(n+1)κ²b²/n² ≍ κ²nb². For |T| = 1,
  γ(t|S) ≈ θ_t²·x_tᵀR_Sx_t ≍ κnθ_t², which is linear in κ.
- *Fix:* add this two-line construction, or mark the claim as an illustration.

**3. NOTE — `CODE_CHECK.md` CC5 omits the scorer's Q-recomputation branch and the fallback routes.**
- *Location:* `v3_score.h` `finish_from_factors`: when Q < 1e-8·y′y, Q is replaced by `q_nonneg` = rss + (‖Xβ‖² + ‖β‖²)/n,
  where β = nH_S^{-1}z_S. The scorer also has two fallback routes, chol_refactor and augmented QR.
- *What is wrong:* nothing mathematical. Under EX-A the branch and the routes give the same Q and determinants. I
  checked the identity: Hβ = nz gives (n+1)βᵀGβ + βᵀβ = nzᵀβ, so rss + (fit² + ‖β‖²)/n = y′y − zᵀβ = Q_S. The QR route
  factors [√(n+1)X_S; I] and [X_S; I], whose Gram matrices are H_S and G_S + I.
- *Fix:* add one sentence to CC5 so that the code-fact list covers every route the score can take.

**4. NOTE — notation clashes.**
- c₂ means 2 log(s₀+1) + log(1/ε) + 1 in the SCR-C proof (`L5_exact.md`) and κ²b²/(104(M²+σ²)) in SCR-G/M4.
- M means |𝓗⁻| in SCR-M and the bound on ‖θ*‖₁ in A1. STATEMENT disambiguates this once.
- The numerics write "deg" for "°" (MCdeg, B2deg).
- *Fix:* rename (for example c_S in L5, M_𝓗 for |𝓗⁻|).

**5. NOTE — the provenance line in `CODE_CHECK.md` is stale but harmless.**
- *Location:* "Source: main @ 2252d57".
- *What is wrong:* HEAD is now 2ac3896.
- *Evidence:* the core files are unchanged since 72785fe and match the recorded hashes (recomputed 8/8), so the code
  facts are current.
- *Fix (optional):* add "verified unchanged at 2ac3896".

## 4. What I verified (completely, found correct)

- **L1.1-L1.7:**
  - the variational form of R_S;
  - q_S(v) = ‖v‖²/(n+1) + (n/(n+1))vᵀR_Sv and the bounds on Q_S;
  - the Schur and determinant identities;
  - the rank-one update of R_S;
  - D ∈ [max(1, (n+1)a/n), n+1];
  - the one-step formula L1.4, with prior ratio (k+1)/(2p−1−k);
  - D-add (L1.5) with T_n and the bound n·T_n/(2(n+1)) on the penalty;
  - the self-normalised D-add (L1.5°) and ρ̄_n(n−1) ≤ T_n;
  - D-del (L1.6);
  - the augmented representation (L1.7).
  Numerically: the gap identity F(S∪t) − F(S) = −B_S − ν log(1−u) holds to 5e-14 on 300 random cases, and the D
  bounds are never violated.
- **L2:**
  - E1: the variance bound x_tᵀR_S²x_t ≤ a(t|S) and the per-model budget e^{-x}/N_q;
  - E4: one-sided, budget e^{-x}/(2N_q);
  - E2⁺ and E2⁻: the AM–GM step 2σ‖μ‖ ≤ √(n−1)τ_n², the constants (2+√2)a ≤ 4a, and τ̂ ≤ τ_n(1+2a);
  - E2ᶜʰⁱ;
  - E3a, where A = CB₁B₁ᵀC ⪯ Π, rank ≤ k;
  - E3b, with the geometric series bound.
- **L3:**
  - the SCR-A claim and conclusion;
  - A∞: uniform (1+o(1)) via (2 log 2 + 1)/log n, N_q ≤ (p+1)^q, and r_n ≤ √(2q log p) + o(√log n);
  - SCR-A° Steps 1-2 (ϑ°_n absorbs 1.02τ̄² because σ_S ≥ σ);
  - A°∞, including that the last term of ϑ° is o(1) under ‖μ‖ = o(nσ);
  - A1 (ρ² ≥ 200/64);
  - A1° (both branches of the minimum give ≥ 8𝐋_n; ρ°² ≥ 2).
- **L4:**
  - L4.0, including ‖w‖² ≥ Δ(S) and wᵀ(I−P̃)b̃ = wᵀb̃;
  - B1, B2, B2° (u⁴/(A+Bu²) is increasing; V/(4σ²+9κV) is increasing; m_S ≤ u + c_θ);
  - B2d;
  - B3 (λ_min of a Schur complement).
  Numerically: the L4.0 and B2° lower bounds are never violated (worst relative excess −0.074 and −0.76).
- **L5:**
  - facts (a)-(c), including ω ≤ (n−1+λ₀)/(φ(n−1)+λ₀) ≤ 1/φ;
  - Step 1, including D ≥ (n+1)α(n−1)/n and (n−1)/(2ν) ≥ 1 − 1.02/n;
  - Step 2: the dual basis is ∝ the conditional residuals, its Gram matrix is M^{-1}, and Σ(ũ_jᵀv)² ≤ ω‖P_Wv‖²;
  - Step 3 and (EC);
  - L5.2;
  - SCR-C: the uniform η → 0, Λ_k ≥ 2ℓ + log n − c, the RHS expansion, and the comparison φ𝐋 − 2 log p ≥ ε𝐋;
  - SCR-R: P_CC = P_C for centred columns, and X_CG_C^{-2}X_Cᵀ ⪯ P_C/λ_min.
  Numerically: fact (a) holds to 1e-15, ω ≤ 1/φ always, and the dual-basis inequality is never violated.
- **L6:**
  - the exact criterion (★) at ∅, which numerically matches the direct F comparison in 0 mismatches over 500 designs ×
    all singletons;
  - the B_n bounds;
  - the noise union bounds, with v < 1;
  - Consequence 1: the sequence is solvable, θ ≍ √(log n/n), and both (i) and (ii) hold for large n;
  - Consequence 2: γ ~ (log n)²/n, and the ratio of B1 to Γ is (n+1)/n;
  - the scaling remark.
- **L7:**
  - E1_𝓗 and E4_𝓗 (min of two deterministic radii; 1-Lipschitz max);
  - the numerator and the sign convention of d_S;
  - the denominator with both branches of Ū_S;
  - the gap;
  - M1, M2 (the addition is scanned because \|C\| ≤ K−1);
  - M5, both the deletion and swap cases (C∪{l} is scanned because \|C\| = \|N\| ≤ K−1, and N is the best neighbour);
  - M3 under MC and MC°;
  - M4 (u* ≤ 1/26 via κ ≤ M/b, the n ≥ 34 step, and c₂ = u*/4·(1/τ_*²)·…);
  - SCR-G (i)-(iii);
  - M6, including the illustration.
- **Code (CC1-CC6):**
  - `local_search`: complete scan, additions skipped at \|C\| ≥ K, strict improvement, lexicographic ties,
    `returned` on certification and on the move cap, `scan_complete` always 1;
  - `cpp_final_run`: a new ledger and cache; inherited models rescored and offered; the final search starts from
    `led.hpmS` with a non-emitting centre; LS0 emits its centre; any guard or NumericalFailure makes the status ≠
    completed;
  - `Ledger::event` offers on fresh evaluations, and every cache hit was offered earlier;
  - `v3_run.R:142-200` (cert_final, cert_ls0, `identical(hpm, returned)`, status gate);
  - `v3_exact.R:15`; `v3_fit.R:76`;
  - the score constants and formula (`v3_score.h:14, 57, 64-70, 223`), with H = (n+1)G + I and A = G + I in both the
    Cholesky and QR routes;
  - standardisation by the (n−1) SD; duplicate columns are only reported, never dropped;
  - π₀ and the start mode are supported on sizes ≤ K;
  - all cited line numbers; 8/8 hashes.
- **Statement ↔ lemma consistency:** SCR-A, A∞, SCR-A°, A°∞, SCR-M (B_S, g⁻, U_S, Ū_S, δ_S, b_𝓗, c_𝓗), SCR-G, B1-B3,
  B2°, B2d, A1, A1°, L5.1 and (EC′) with η_n and its probability, SCR-C, SCR-R, SCR-N. All match the lemma files
  verbatim. The side claims in A°∞ (A²/n²) and in §1 (σ ≤ σ_S ≤ τ_n; Ψ ≥ Γ/τ_n²; a ∈ (0, n)) are correct.
