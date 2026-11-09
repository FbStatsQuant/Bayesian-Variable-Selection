# C — Corollary table: existing family results as instances of the general theorems

Status: assumption checks by this seat (unchecked); each row cites the source result and status verbatim. Families are
**examples** of (A1)–(A3) (Felipe's requirement), not separate theorems. Notation: STATEMENT §2; Σ-branch constants
(K, a), growth (C₀, d₀).

**Growth facts used.** (G-line) index distance δ(j, k) = |π(j) − π(k)| for a bijection π onto [p]: N_δ(r) ≤ 2r + 1 ≤ 2(1 + r)
(C₀ = 2, d₀ = 1). (G-sites) Euclidean distance between sites in ℝ^d with separation ≥ 1: N_δ(r) ≤ (2r + 1)^d ≤ 2^d(1 + r)^d
(LOC2 `lemmas/L3_CTd.md` §L3.0 packing fact applied with R ↓ r; C₀ = 2^d, d₀ = d). (G-block) partition into blocks of size
≤ γ̄, δ = 0 inside a block and p across: N_δ(r) ≤ γ̄ for r < p and = p ≤ γ̄(1 + r) for r ≥ p (C₀ = γ̄, d₀ = 1); any
block-diagonal Ψ with entries ≤ 1 satisfies the Σ-branch with K = 1 (any a > 0) and λ_max ≤ γ̄.
**PTV fact.** If Σ is block-diagonal and every block contains ≤ 1 truth, then for j ∈ S₀, U ∌ j:
|Cov(W_j, Σθ*_kW_k | W_U)| = |θ*_j| Var(W_j | W_U) ≥ θ_lo λ_min(Σ) [R04-2] (other truths are in other, independent blocks) — LOC2
`lemmas/L4_LOCd.md` B.0 (F3); so PTV(θ_lo c).

| # | Source result (status verbatim) | Instance of | Exact assumption check |
|---|---|---|---|
| 1 | APP Lemma POST (W2-APP REPORT: "PROVED-CHECKED"; lemma "PROVED (by this seat, unchecked)", R02 V-W-A) | UNI-P | identical hypotheses (A1-post = LSF of APP L1_POST); exact Gram: POST(c). |
| 2 | APP Theorem LOC (exp. decay along an ordering π; "PROVED-CHECKED" inside W2-APP) | UNI-0 | (G-line); LOC ⇒ Σ ∈ LOC_M with (K, a) of APP L3_LOC.md:27 and spectrum [c, C]; PTV is APP's hypothesis (L3_LOC.md:28). |
| 3 | GROW (C5)(c) AR(1), study S2 (C-GROW "PROVED-CHECKED") | UNI-0 | Σ_jk = ρ^{|j−k|}: (G-line), K = 1, a = −log|ρ|, spectrum [(1−|ρ|)/(1+|ρ|), (1+|ρ|)/(1−|ρ|)]. PTV: GROW's separation (6.0) yields the residual-covariance floor for |U| ≤ 15 (APP `lemmas/L3_LOC.md:62-64`: "[L6] uses P3/P4 + (6.0) to get a population residual covariance ≥ a₀ for every j ∈ S₀, \|U\| ≤ 15"); (6.0) holds for the study's S2 layouts (C-GROW STATEMENT.md:146). |
| 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen_dev_data.R:18-28`: S1 = I; S3 = 0.7H + 0.3I; S4 = 0.85H + 0.15I; S6 = within-group ρ_g ∈ {0.4,…,0.9}, groups of 5 (H = same-group indicator): (G-block) with γ̄ = 5, spectral floor 0.3 / 0.15 / ≥ 0.1 (S6: 1 − ρ_g ≥ 0.1), λ_max ≤ 5. Truths: `truth()` (gen_dev_data.R:32-41) puts truth k in group 1 + step·k, step ∈ {7, 13} ⇒ ≤ 1 truth per group ⇒ PTV(θ_lo c). (GEN's masked-truth theorems — LH, LH-iid, W — are not imported.) |
| 5 | LOC2 Theorem LOC-d (W2-LOC2 "PROVED-CHECKED") | UNI-0 | (G-sites), both branches, spectrum [c, C], PTV — LOC2's hypotheses verbatim. |
| 6 | LOC2 Theorem LOC-BF (growing one-factor groups; "PROVED-CHECKED") | Theorem PLR (STATEMENT (i′)), not UNI-0 | growing groups violate fixed C₀; uses LOC2 L4 Part B's latent-factor frames. |
| 7 | LOC2 polynomial decay α > 17/2 ("PROVED-CHECKED") | separate extension of the engine | LOC2 L6 re-runs toolkit/NA/assembly at polynomial |Q|; outside LOC_M (polynomial decay). |
| 8 | FACA Theorem FAC-L ((L4) fixed design, (L5) iid rows; "PROVED-CHECKED (for the narrowed, flagged target …)") | UNI-1 | Ψ block-diagonal over 𝒢 (≤ γ̄) with λ_min ≥ ψ₀: (G-block) ⇒ Ψ ∈ LOC_M(γ̄, 1, ψ₀, γ̄, 1, a); c_𝒢 = c_min and κ_UNI = κ_FACA (L3_ULOC §L3.4 remark; numerics/n3b_out.txt last line: S5 block CS c_𝒢 = 0.4286 = 0.3/0.7, κ = 1.0000); (AG) = (E); (P) identical; (TV)/(TV-pop) identical. |
| 9 | Study S5 (FACA (I)(c), "PROVED-CHECKED" inside FAC-A) | UNI-1 | gen_dev_data.R:26: Σ = 0.3·11ᵀ + 0.4H + 0.3I: λ = √0.3·1, Ψ = 0.4H + 0.3I (block CS, groups of 5) ⇒ κ = 1, α₀ = 1/6; TV-pop with FACA's certified covering family (unions of ≤ 3 whole groups, Lemma P5) and τ₀ = c²·7/2080 for the study's 14-truth layouts (steps 7 and 13), and τ₀ = c²·2023/32500 for the four-truth diagnostic layout (FACA `lemmas/L5_random_instances.md` §L5.3) [R04-4]. Covered for limsup log p/log n < 1/6. |
| 10 | FACB Theorem FAC-CS ("PROVED-CHECKED") | partly UNI-1(E); otherwise partial version | Exact-Gram CS (up to column signs): λ = √ρ·Υ1, Ψ = (1 − ρ)I, κ = 1. For limsup log p/log n < 1/6 and actual-block TV, an instance of UNI-1(E); for 1/6 ≤ … , p ≤ ⌊n/2⌋, and for masked truths under (FS′): FACB only (family-specific partial version of "(iii) for all p ≤ n^A"). |
| 11 | APP Lemma ENUM ("PROVED-CHECKED" inside W2-APP) | separate override | needs the coded (EXB) inequality eventually, EX-A, and posterior consistency (UNI-P); output-intersected selection consistency, no independent delivery claim. |
| 12 | APP Lemma VN / STAR (route obstructions) | consistent with UNI | VN: GROW/LOC sandwich with |Q| = O(log n) fails for pervasive designs — UNI-1 uses Q = [p]; STAR: bounded spectrum alone is not enough for the route — UNI-0 requires locality (exp. decay along a polynomial-growth geometry). |

**Exponents for UNI-1 instances** (κ̄ = max(1, κ)): compound symmetry and every block compound symmetry with its groups:
κ = 1 ⇒ 1/6. Heterogeneous random-sign loadings on AR/GMRF/cluster Ψ (numerics/n3b_out.txt): κ ∈ [3.3, 7.3] ⇒ α₀ ∈
[0.0074, 0.0284]. Diagonal Ψ with loadings λ_j ∈ [λ_lo, λ_hi] of one sign: κ′ = max_j λ_j/√(1 − λ_j²),
c_𝒢 = min_j λ_j²/(1 − λ_j²) (singletons), so κ = max(λ/√(1−λ²))/min(λ/√(1−λ²)) — FACA's singleton formula (as recorded in
W2-FAC-XA STATEMENT).
