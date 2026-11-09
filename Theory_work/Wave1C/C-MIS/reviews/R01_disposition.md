# R01 disposition (statement lock, Codex gpt-6.1-sol high: LOCK-WITH-CHANGES, 7 required changes)

Lead check of the SL attribution: rendered SL p. 957 (scratchpad image of PDF page 11): Corollary 2 reads
π(s̃ ⊂ ξ | D_n^s) →p 1 — the reviewer is right (inclusion, not exact-model concentration).

| # | Required change | Disposition | Where |
|---|---|---|---|
| 1 | SL attribution: Thm 4 = density consistency, Cor 2 = support inclusion; MIS stronger under stronger hypotheses; EP separate | ACCEPTED | STATEMENT §0 rewritten |
| 2 | ε ⊥ X_𝒞 (or ε given X_𝒞 Gaussian), valid inputs; s₀^𝒞 ≥ 1 explicit | ACCEPTED (empty support excluded, not claimed) | STATEMENT §1, §2 (H-MIS); L1.2 remark (c); L1.4 hypotheses |
| 3 | MIS(ii) in deterministic-sequence / envelope form; GD(a) with parameter assumptions; GD(b) conditional | ACCEPTED (GD(b) kept as an optional proof under explicitly assumed projection sparsity, restricted eigenvalues, energy and projected beta-min) | STATEMENT §2 (ii), (iii); L1.4; L2 GD |
| 4 | Prop P: one active omitted variable, null-candidate status, cancellation, beta-min; coefficient criterion instead of slogan | ACCEPTED (also added the partial-correlation identity −Θ_jk/√(Θ_jjΘ_kk) and the intercept formula) | STATEMENT §2 (iii); L2 P(d) |
| 5 | Theorem F: coordinates; σ²_{𝒞,n} in the large-signal clause; Δ_S with μ^𝒞; full changed-step inventory incl. C4/C5/C8 sequences and the response-dependent IG rate | ACCEPTED — L4 (drafted before the reply) already uses contrast coordinates, δ_n^𝒞 propagated to υ, ε, q, E_n^𝒞, Δ_S with μ^𝒞, the (P_{S′} − P_S)r = 0 replacement, and the actual common b | STATEMENT §4; L4 |
| 6 | Frontier: unrestricted span vs capped feasibility; numerator identity survives; explicit KL experiment, no unqualified e^{−c·rank} | ACCEPTED | STATEMENT §5; L5 §1–§2 (Lemma O2 is stated for the full contrast experiment, with explicit Δ-dependence; reduced-experiment loss marked conjectural) |
| 7 | Narrow deliverables | ACCEPTED: GD(b) and Corollary D′ (W instance) marked optional; N5 exploratory; numerics already run (none used as a proof of failure — N3's Δ = 4 run is reported as "consistent with", not as a failure theorem) | STATEMENT §2, §3; numerics/SUMMARY.md |

Other reviewer remarks adopted: the exact form 2b + Q^c_S = 2b̃ + Q̃_S + (1 + 2b₀/N)(‖r‖² + 2rᵀe) is noted; L4 keeps the
actual b throughout (it enters only through 2b ≥ 0 and b ≤ 6b₀(M + σ²)). EP uniqueness: θ^𝒞 is the unique representation
among supports T with |T ∖ S₀^𝒞| ≤ j₀ (by SE_λ(j₀)).

Addition not reviewed at lock: Lemma T / Corollary F(b) (TAIL^𝒞 under a large omitted residual), drafted while R01 ran;
it goes to the L4 lemma check.
