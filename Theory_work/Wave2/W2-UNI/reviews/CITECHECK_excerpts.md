# CITECHECK excerpts (one entry per citation; for the manual content audit)

* **STATEMENT.md:76** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:28-28`
  - context: APP `lemmas/L3_LOC.md:28`). PTV is not used for (i); for (iii) it is one sufficient visibility condition (see (iii)).
  - cited: * (PTV(a₀)) for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with |U| ≤ 15: |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀, a₀ > 0 fixed.

* **C_corollaries.md:19** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:26-27`
  - context: | 2 | APP Theorem LOC (exp. decay along an ordering π; "PROVED-CHECKED" inside W2-APP) | UNI-0 | (G-line); LOC ⇒ Σ ∈ LOC_M with (K, a) of APP L3_LOC.md:26-27 and spectrum [c, C]; PTV is APP's hypothesis (L3_LOC.md:28). |
  - cited: * (LOC) Σ_n ∈ LOC(c, C, K, a) with fixed constants (L2_CT §L2.2): spectrum in [c, C] and exponential decay of Σ_n or of Σ_n⁻¹ along a bijection π_n : [p] → [p]; d(j, k) := |π_n(j) − π_n(k)|. (K₂, t₂) are the constants of Lemma CD.

* **C_corollaries.md:19** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:28-28`
  - context: | 2 | APP Theorem LOC (exp. decay along an ordering π; "PROVED-CHECKED" inside W2-APP) | UNI-0 | (G-line); LOC ⇒ Σ ∈ LOC_M with (K, a) of APP L3_LOC.md:26-27 and spectrum [c, C]; PTV is APP's hypothesis (L3_LOC.md:28). |
  - cited: * (PTV(a₀)) for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with |U| ≤ 15: |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀, a₀ > 0 fixed.

* **C_corollaries.md:20** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:62-64`
  - context: | 3 | GROW (C5)(c) AR(1), study S2 (C-GROW "PROVED-CHECKED") | UNI-0 | Σ_jk = ρ^{|j−k|}: (G-line), K = 1, a = −log|ρ|, spectrum [(1−|ρ|)/(1+|ρ|), (1+|ρ|)/(1−|ρ|)]. PTV: GROW's separation (6.0) yields the residual-covariance floor for |U| ≤ 15 (APP `lemmas/L3_LOC.md:62-64`: "[L6] uses P3/P4 + (6.0) t
  - cited: * m♯_n = O(log n), SE_w with g₀ = 1, φ₀² = c/2, energy, BM-∞: unchanged (also L1_POST). * TV (G3b): [L6] uses P3/P4 + (6.0) to get a population residual covariance ≥ a₀ for every j ∈ S₀, |U| ≤ 15; here PTV gives it directly. The perturbation argument (bounded dimension, inverse norms ≤ 2/c, fixed coefficients θ*_j,

* **C_corollaries.md:20** → `Theory_work/Wave1C/C-GROW/STATEMENT.md:146-146`
  - context: | 3 | GROW (C5)(c) AR(1), study S2 (C-GROW "PROVED-CHECKED") | UNI-0 | Σ_jk = ρ^{|j−k|}: (G-line), K = 1, a = −log|ρ|, spectrum [(1−|ρ|)/(1+|ρ|), (1+|ρ|)/(1−|ρ|)]. PTV: GROW's separation (6.0) yields the residual-covariance floor for |U| ≤ 15 (APP `lemmas/L3_LOC.md:62-64`: "[L6] uses P3/P4 + (6.0) t
  - cited: generator's S2 layouts (p = 500, 1000; 14 truths; ρ = 0.5) satisfy separation for every signal scale c > 0, so the

* **C_corollaries.md:21** → `Scripts/Data_generators/gen_dev_data.R:18-29`
  - context: | 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen_dev_data.R:18-29` [R05a-12] (S1 :24, S3 :26, S4 :27, S6 :29): S1 = I; S3 = 0.7H + 0.3I; S4 = 0.85H + 0.15I; S6 = within-group ρ_g ∈ {0.4,…,0.9}, groups of 5 (H = same-group indicator): (G-block) w
  - cited: scenario_covariance <- function(scenario, p=500L) { stopifnot(length(scenario)==1L, scenario %in% 1:6, p>=1L, p==as.integer(p)) group <- ceiling(seq_len(p)/5) H <- outer(group,group,"==") I <- diag(p) switch(as.integer(scenario),

* **C_corollaries.md:21** → `Scripts/Data_generators/gen_dev_data.R:32-42`
  - context: | 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen_dev_data.R:18-29` [R05a-12] (S1 :24, S3 :26, S4 :27, S6 :29): S1 = I; S3 = 0.7H + 0.3I; S4 = 0.85H + 0.15I; S6 = within-group ρ_g ∈ {0.4,…,0.9}, groups of 5 (H = same-group indicator): (G-block) w
  - cited: # Port of tools/scenario_check.py::truth (§II.3, §II.9). Uses no random numbers. truth <- function(p) { s0   <- c(`30` = 5L, `500` = 14L, `1000` = 14L)[[as.character(p)]] step <- c(`30` = 1L, `500` = 7L, `1000` = 13L)[[as.character(p)]] pos  <- c(3L, 2L, 4L, 1L, 5L, 3L) pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)

* **C_corollaries.md:21** → `Scripts/Data_generators/gen_dev_data.R:24-24`
  - context: | 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen_dev_data.R:18-29` [R05a-12] (S1 :24, S3 :26, S4 :27, S6 :29): S1 = I; S3 = 0.7H + 0.3I; S4 = 0.85H + 0.15I; S6 = within-group ρ_g ∈ {0.4,…,0.9}, groups of 5 (H = same-group indicator): (G-block) w
  - cited: I,

* **C_corollaries.md:21** → `Scripts/Data_generators/gen_dev_data.R:26-26`
  - context: | 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen_dev_data.R:18-29` [R05a-12] (S1 :24, S3 :26, S4 :27, S6 :29): S1 = I; S3 = 0.7H + 0.3I; S4 = 0.85H + 0.15I; S6 = within-group ρ_g ∈ {0.4,…,0.9}, groups of 5 (H = same-group indicator): (G-block) w
  - cited: 0.7*H+0.3*I,

* **C_corollaries.md:21** → `Scripts/Data_generators/gen_dev_data.R:27-27`
  - context: | 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen_dev_data.R:18-29` [R05a-12] (S1 :24, S3 :26, S4 :27, S6 :29): S1 = I; S3 = 0.7H + 0.3I; S4 = 0.85H + 0.15I; S6 = within-group ρ_g ∈ {0.4,…,0.9}, groups of 5 (H = same-group indicator): (G-block) w
  - cited: 0.85*H+0.15*I,

* **C_corollaries.md:21** → `Scripts/Data_generators/gen_dev_data.R:29-29`
  - context: | 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen_dev_data.R:18-29` [R05a-12] (S1 :24, S3 :26, S4 :27, S6 :29): S1 = I; S3 = 0.7H + 0.3I; S4 = 0.85H + 0.15I; S6 = within-group ρ_g ∈ {0.4,…,0.9}, groups of 5 (H = same-group indicator): (G-block) w
  - cited: {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})

* **C_corollaries.md:26** → `Scripts/Data_generators/gen_dev_data.R:28-28`
  - context: | 9 | Study S5 (FACA (I)(c), "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" inside FAC-A) | UNI-1 | `Scripts/Data_generators/gen_dev_data.R:28` [R05a-12]: Σ = 0.3·11ᵀ + 0.4H + 0.3I: λ = √0.3·1, Ψ = 0.4H + 0.3I (block CS, groups of 5) ⇒ κ = 1, α₀ = 1/6; TV-pop with FACA's certi
  - cited: 0.3*matrix(1,p,p)+0.4*H+0.3*I,

* **C_corollaries.md:26** → `Scripts/Data_generators/gen_dev_data.R:37-37`
  - context: | 9 | Study S5 (FACA (I)(c), "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" inside FAC-A) | UNI-1 | `Scripts/Data_generators/gen_dev_data.R:28` [R05a-12]: Σ = 0.3·11ᵀ + 0.4H + 0.3I: λ = √0.3·1, Ψ = 0.4H + 0.3I (block CS, groups of 5) ⇒ κ = 1, α₀ = 1/6; TV-pop with FACA's certi
  - cited: pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)

* **C_corollaries.md:26** → `Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md:144-146`
  - context: | 9 | Study S5 (FACA (I)(c), "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" inside FAC-A) | UNI-1 | `Scripts/Data_generators/gen_dev_data.R:28` [R05a-12]: Σ = 0.3·11ᵀ + 0.4H + 0.3I: λ = √0.3·1, Ψ = 0.4H + 0.3I (block CS, groups of 5) ⇒ κ = 1, α₀ = 1/6; TV-pop with FACA's certi
  - cited: diagnostic layout (s₀ = 4): min τ = 2023/32500 ≈ 0.06225 over 11,060 configurations; study layouts (s₀ = 14, step 7 and step 13): min τ = 7/2080 ≈ 0.003365 over 612,710 configurations each. Hence (TV-pop) holds with τ₀ = c²·2023/32500, resp. c²·7/2080, for the fixed scale c > 0. (GC-CS) exact minima for the study patterns: a = 1/10: 39/50, 7/25;

* **L1_metric.md:5** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:143-151`
  - context: Target: `W2-UNI/STATEMENT.md:143-151` (R1, as amended by `reviews/R01_statement_lock_sol.md:63-77`, required change 4).
  - cited: * **R1 Metric toolkit.** CT_M, CD_M, RB_M, TAIL_M and LOCL. [R01-4] All shell sums begin at m = 0, with shell counts bounded by C₀(m + 2)^{d₀}. For matrices with spectrum in [c, C], use Var(ζ_l | ζ_T) ≤ C, not ≤ 1, and hence (B⁻¹)_ll ≥ 1/C in the regression formula. Constants in RB_M, TAIL_M and LOCL may depend on C. Prove the bounds uniformly for principal submatrices and conditional covariances.

* **L1_metric.md:5** → `Theory_work/Wave2/W2-UNI/reviews/R01_statement_lock_sol.md:63-77`
  - context: Target: `W2-UNI/STATEMENT.md:143-151` (R1, as amended by `reviews/R01_statement_lock_sol.md:63-77`, required change 4).
  - cited: ### 4. Make the metric toolkit and idiosyncratic remainder specifications valid for non-unit Ψ  **Locations:** STATEMENT R1/R3(b), PLAN steps 2 and 4(b). The pseudometric extension is sound in principle: restricted balls obey the same growth bound, and i↦δ(i,j) is 1-Lipschitz by the triangle inequality. No Euclidean property is needed in LOC2 L3's conjugation argument. However, separation was used

* **L1_metric.md:7** → `Theory_work/Wave2/W2-LOC2/REPORT.md:3-3`
  - context: check R02 "VERIFIED-WITH-AMENDMENTS"; inside W2-LOC2 "PROVED-CHECKED", `W2-LOC2/REPORT.md:3`), itself modelled on APP
  - cited: **RESULT: PROVED-CHECKED** — council round 1 PASSED (Codex gpt-6.1-sol xhigh 9.3, Claude Opus 5.5 high 9.1; all six gates

* **L1_metric.md:15** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:50-53`
  - context: (`STATEMENT.md:50-53`); necessarily C₀ ≥ 1, d₀ ≥ 0 real. Empty index sets carry zero vectors and empty sums are 0.
  - cited: > **Definition (metric locality, LOC_M).** A symmetric matrix Ψ on [p] is in 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) if its spectrum > lies in [c, C] (0 < c ≤ C), and there is a pseudometric δ on [p] with **polynomial growth** > N_δ(r) := max_i |{k : δ(i, k) ≤ r}| ≤ C₀(1 + r)^{d₀} for all r ≥ 0, such that either (Σ-branch) > |Ψ_jk| ≤ K e^{−a δ(j,k)} (j ≠ k) or (Θ-branch) |(Ψ⁻¹)_jk| ≤ K e^{−a δ(j,k)} (j ≠ k).

* **L1_metric.md:25** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:15-21`
  - context: (Replaces the packing fact of LOC2 `L3_CTd.md:15-21`, which needed site separation ≥ 1 and started shells at m = 1.)
  - cited: ## L3.0 Sites and packing A *site map* is x : I → ℝ^d (I finite) with ‖x_i − x_j‖ ≥ 1 for i ≠ j (Euclidean norm; d ≥ 1 fixed); d_ij := ‖x_i − x_j‖. **Packing fact.** For every i and R > 0, #{j : d_ij < R} ≤ (2R + 1)^d; hence for every integer m ≥ 1, #{j : m ≤ d_ij < m + 1} ≤ (2m + 3)^d. *Proof.* The balls B(x_j, ½) are pairwise disjoint (separation ≥ 1); for d_ij < R they lie in B(x_i, R + ½). Com

* **L1_metric.md:61** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:23-43`
  - context: Delta to LOC2 `L3_CTd.md:23-43`: (2m + 3)^d → C₀(m + 2)^{d₀}; shells m ≥ 1 → m ≥ 0 (no separation); φ(y) = ‖y − x_j‖ →
  - cited: ## L3.1 Lemma CT_d Let A be real symmetric on I with λ_min(A) ≥ α > 0 (no upper spectral bound needed) [R07-14], and |A_ij| ≤ K e^{−a d_ij} for i ≠ j (K, a > 0). For 0 ≤ t < a put S(t) := K Σ_{m≥1} (2m + 3)^d e^{−(a−t)m}(1 − e^{−t(m+1)}). S is finite, continuous and nondecreasing on [0, a), S(0) = 0, and S(t) → ∞ as t ↑ a. Let t* = t*(α, K, a, d) := max{t ∈ [0, a) : S(t) ≤ α/2} ∈ (0, a). Then for 

* **L1_metric.md:66** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:50-53`
  - context: 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) is as in `STATEMENT.md:50-53` (symmetric Ψ on [p], spectrum in [c, C], 0 < c ≤ C; pseudometric of
  - cited: > **Definition (metric locality, LOC_M).** A symmetric matrix Ψ on [p] is in 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) if its spectrum > lies in [c, C] (0 < c ≤ C), and there is a pseudometric δ on [p] with **polynomial growth** > N_δ(r) := max_i |{k : δ(i, k) ≤ r}| ≤ C₀(1 + r)^{d₀} for all r ≥ 0, such that either (Σ-branch) > |Ψ_jk| ≤ K e^{−a δ(j,k)} (j ≠ k) or (Θ-branch) |(Ψ⁻¹)_jk| ≤ K e^{−a δ(j,k)} (j ≠ k).

* **L1_metric.md:85** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:50-65`
  - context: Delta to LOC2 `L3_CTd.md:50-65`: CT_d → CT_M; "Var(W_j | W_U) ≤ 1" → "≤ min(Ψ_jj, C)" (the only use of unit diagonal there).
  - cited: **Lemma CD_d.** Let Σ ∈ LOC_d(c, C, K, a), W ~ N(0, Σ). Define (LOC_d-Σ): t₁ := t*(c, K, a, d), K₁ := 2/c;   (LOC_d-Θ): t₁ := a, K₁ := K;   t₂ := t*(1/C, K₁, t₁, d), K₂ := 2C. Then for every U ⊆ [p] and distinct j, k ∉ U: (a) |Cov(W_j, W_k | W_U)| ≤ K₂e^{−t₂d_jk}; (b) c ≤ Var(W_j | W_U) ≤ 1, and for every V ⊆ [p] ∖ U the conditional covariance matrix Cov(W_V | W_U) has spectrum in [c, C];

* **L1_metric.md:99** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:67-75`
  - context: *Simplification (unit-diagonal Ψ, e.g. UNI-0's Σ):* G_ll ≥ 1 and B may be replaced by 2/c, as in LOC2 `L3_CTd.md:67-75`.
  - cited: ## L3.3 Lemma RB (ℓ¹ bound for population regression coefficients) Let Σ ∈ LOC_d(c, C, K, a). Let (K_Σ, t_Σ) := (K, a) under (LOC_d-Σ) with t_Σ′ := t*(c, K, a, d), and under (LOC_d-Θ) (K_Σ, t_Σ) := (2C, t*(1/C, K, a, d)) (CD_d(c)) with t_Σ′ := t*(c, 2C, t_Σ, d). For l ∈ [p] and A ⊆ [p] ∖ {l}, let β_A(l) := Σ_AA⁻¹Σ_{Al} (coefficients of E[W_l | W_A] = W_Aβ_A(l)). Then |β_A(l)_v| ≤ (2/c)e^{−t_Σ′ d_l

* **L1_metric.md:115** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:77-85`
  - context: (Delta to LOC2 `L3_CTd.md:77-85`: shells m ≥ ⌊r⌋, m ≥ 1 → m ≥ ⌊r⌋ ≥ 0 with counts C₀(m + 2)^{d₀}.)
  - cited: ## L3.4 Lemma TAIL (far conditioning) Let Σ ∈ LOC_d, l ∈ [p], T ⊆ [p] ∖ {l}, r > 0, T′ := {v ∈ T : d_lv ≤ r}. Then (a) Var(E[W_l | W_T] − E[W_l | W_{T′}]) ≤ κ(r) := (K₂²/c) Σ_{m ≥ ⌊r⌋, m≥1} (2m + 3)^d e^{−2t₂m}, and κ(r) → 0 as r → ∞; (b) Var(W_l | W_{T′}) = Var(W_l | W_T) + Var(E[W_l | W_T] − E[W_l | W_{T′}]). *Proof.* (b) e_T := W_l − E[W_l | W_T] is uncorrelated with every linear function of W_

* **L1_metric.md:120** → `Theory_work/Wave2/W2-UNI/reviews/R01_statement_lock_sol.md:73-73`
  - context: `reviews/R01_statement_lock_sol.md:73`); ε(r) ≤ ε̄ e^{−t′⌊r⌋/2} with ε̄ := (1 + L₀)BC₀μ(t′)/(1 − e^{−t′/2}) (G-tail);
  - cited: > Establish constants B,t>0 such that |β_T^Ψ(l)_v|≤B exp(−tδ(l,v)) uniformly in T,l,v, and a uniform ℓ¹ regression bound L₀. For U=T∩B(l,r), V=T∖U, show β_U−β_{T,U}=Ψ_UU^{-1}Ψ_UVβ_{T,V}, whence ‖β_T−β̄_U‖₁≤(1+L₀)‖β_{T,V}‖₁≤ε(r), with ε(r)=(1+L₀)B C₀Σ_{m≥⌊r⌋}(m+2)^{d₀}e^{-tm}→0. Empty index sets have zero coefficient vectors.

* **L1_metric.md:149** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:51-53`
  - context: ‖Δ‖₁ ≤ ‖β_T‖₁ + ‖β_U‖₁ ≤ 2L₀ (used by LOC2 `L4_LOCd.md:51-53` for NA-R's (R2)), LOCL makes the atom coefficient
  - cited: * (R2) Atoms 𝒜_n := {e_v : v ∈ Q} (Var = 1, |𝒜_n| ≤ |Q|). Since W_Tβ_T(l) − W_{T′}β_{T′}(l) = Σ_{v∈T}λ_{T,l,v}W_v with λ_{T,l} := β_T(l) − β̄_{T′}(l) (zero-padded), e_{T,l} = r_{T,l} − Σ_v λ_{T,l,v}W_v, and by Lemma RB ‖λ_{T,l}‖₁ ≤ 2L₀ =: L. Then L²(log(|𝒜_n| + 1) + log log n) = O(log log n) = o(log n).

* **L1_metric.md:151** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:158-161`
  - context: `STATEMENT.md:158-161` needs. Sample usage: with r_n = ⌈(log log n)²⌉, ε(r_n) ≤ ε̄e^{−t′((log log n)²−1)/2} = o((log n)^{−M})
  - cited: (b) [R01-4] for U = T ∩ B(l, r_n), control the local standard normals (ζ_l − β_Uᵀζ_U)/√ψ_{l|U} over at most p·2^{C₀(1+r_n)^{d₀}} references. Use TAIL_M to compare ψ_{l|U}/ψ_{l|T} = 1 + o(1) uniformly, and use LOCL with coordinate atoms to bound |(β_T − β̄_U)ᵀζ| ≤ ε(r_n) max_j |ζ_j|. With r_n = ⌈(log log n)²⌉, log(reference count) ≤ log p + o(log n), max_j |ζ_j| = O_P(√(log p + log log n)), and the

* **L1_metric.md:161** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:22-23`
  - context: |(R⁻¹)_jk| ≤ C|(Ψ⁻¹)_jk|. ∎ (This is what makes "Σ_n unit diagonal WLOG" of `STATEMENT.md:22-23` compatible with membership in
  - cited: * **Design.** Either (R) *random design*: raw rows iid N(m_n, Σ_n), Σ_n unit-diagonal (WLOG by scale invariance; m_n arbitrary), X = centred, sample-standardised raw design; or (E) *approximate-Gram fixed design*: X centred and

* **L2_k0.md:5** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:103-110`
  - context: the statuses copied below. Seat: parallel prover (Claude Opus 5.5 subagent), 2026-11-09. Target: `STATEMENT.md:103-110`
  - cited: **(ii) Theorem UNI-0 (reported model, k = 0).** (R), Σ_n ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) (unit diagonal), (A3) with PTV, any p ≤ n^A. Relevance set [R01-8]: with the conditional-decay constants (K₂, t₂) of CD_M, let d_n = ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉ and Q⁰ = {l : min_{j∈S₀} δ(l, j) ≤ d_n}. Set Q = Q⁰ if p ≥ 2|Q⁰| + 32s₀ + 1, and Q = [p] otherwise. Then |Q| = O((log n)^{d₀}); eventually Q = [p] or

* **L2_k0.md:6** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:152-154`
  - context: (UNI-0) and R2 `STATEMENT.md:152-154`; relevance set as amended by `reviews/R01_statement_lock_sol.md:136-140` (change 8).
  - cited: * **R2 k = 0 engine inputs.** (A2, k = 0) + (A3) ⇒ the hypotheses of Theorem PLR: P(Sand_n) → 1 with Q of (ii) (selection removal, spherical tail, size ladder), (N0)–(N1), (R1)–(R3) of Lemma NA-R, TL inputs. (Delta to LOC2 L4 Part A with packing replaced by the growth function.)

* **L2_k0.md:6** → `Theory_work/Wave2/W2-UNI/reviews/R01_statement_lock_sol.md:136-140`
  - context: (UNI-0) and R2 `STATEMENT.md:152-154`; relevance set as amended by `reviews/R01_statement_lock_sol.md:136-140` (change 8).
  - cited: **Locations:** UNI-0 line 83; R4 lines 118–119. The enlargement test currently uses the already-enlarged Q. Use Q⁰, as LOC2 L4 does. R4 should specify the interval lattice and exact start-mode premise, since these are what permit the descent argument.  **Replace UNI-0's relevance-set clause with:**  > With the conditional-decay constants (K₂,t₂), let d_n=⌈(½log n+log(1+s₀θ_hiK₂))/t₂⌉ and Q⁰={l:min

* **L2_k0.md:7** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:9-66`
  - context: Form: a **line-by-line delta** of LOC2 `lemmas/L4_LOCd.md` Part A (A.1–A.6; `L4_LOCd.md:9-66`), which is itself a delta to
  - cited: ## Part A — Theorem LOC-d  **Hypotheses.** Setting of STATEMENT §1; Σ_n ∈ LOC_d(c, C, K, a) (L3_CTd §L3.2; K = K_dec, the decay constant) with fixed constants and fixed d ≥ 1; PTV(a₀): |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀ for every j ∈ S₀, U ⊆ [p] ∖ {j}, |U| ≤ 15. (K₂, t₂) of Lemma CD_d; distances d(j, k) := ‖x(j) − x(k)‖. **Relevance set.** d_n := ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉, Q⁰ := S₀ ∪ 

* **L2_k0.md:16** → `Theory_work/Wave2/W2-LOC2/REPORT.md:3-3`
  - context: "PROVED-CHECKED" (`W2-LOC2/REPORT.md:3`), HQ audit B4 "HOLDS-WITH-AMENDMENTS" (`Wave2/HQ_AUDIT/B4_loc2_redteam.md:1`; its one
  - cited: **RESULT: PROVED-CHECKED** — council round 1 PASSED (Codex gpt-6.1-sol xhigh 9.3, Claude Opus 5.5 high 9.1; all six gates

* **L2_k0.md:16** → `Theory_work/Wave2/HQ_AUDIT/B4_loc2_redteam.md:1-1`
  - context: "PROVED-CHECKED" (`W2-LOC2/REPORT.md:3`), HQ audit B4 "HOLDS-WITH-AMENDMENTS" (`Wave2/HQ_AUDIT/B4_loc2_redteam.md:1`; its one
  - cited: # Verdict: HOLDS-WITH-AMENDMENTS

* **L2_k0.md:18** → `Theory_work/Wave2/W2-APP/REPORT.md:3-3`
  - context: "VERIFIED-WITH-AMENDMENTS"; W2-APP "PROVED-CHECKED" (`W2-APP/REPORT.md:3`). GROW L6 "PROVED (by this seat, unchecked)",
  - cited: **RESULT: PROVED-CHECKED** — council round 3 PASSED (Codex gpt-6.1-sol xhigh 9.1, Claude Opus 5.5 high 9.1, all six gates

* **L2_k0.md:19** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:3-5`
  - context: R07 Sol "VERIFIED", R06 Opus "VERIFIED-WITH-AMENDMENTS" (APP `L3_LOC.md:3-5`) [C1-B NIT-6], inside C-GROW "PROVED-CHECKED". [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED";
  - cited: Status: **PROVED (by this seat, unchecked)** — a generalisation of GROW `lemmas/L6_random_AR1.md` (cited as [L6]; status there: PROVED (by this seat, unchecked); checks R07 Codex Sol xhigh VERIFIED, R06 Opus VERIFIED-WITH-AMENDMENTS, applied; inside C-GROW "PROVED-CHECKED"). This file is written as a **delta proof**: each

* **L2_k0.md:26** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:22-26`
  - context: Setting (R) of `STATEMENT.md:22-26` (signal bounds `STATEMENT.md:74-75`): raw rows iid N(m_n, Σ_n), **Σ_n unit diagonal**, p ≤ n^A; Y = Xθ* + Cε; fixed s₀,
  - cited: * **Design.** Either (R) *random design*: raw rows iid N(m_n, Σ_n), Σ_n unit-diagonal (WLOG by scale invariance; m_n arbitrary), X = centred, sample-standardised raw design; or (E) *approximate-Gram fixed design*: X centred and standardised with R̂ := XᵀX/(n − 1) satisfying ‖R̂ − Σ_n‖_op ≤ δ_n (δ_n = 0: exact Gram, p ≤ n − 1). p = p_n ≤ n^A, A ≥ 1 fixed. * **Response.** Y = Xθ* + Cε, ε ~ N(0, σ²I_

* **L2_k0.md:26** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:74-75`
  - context: Setting (R) of `STATEMENT.md:22-26` (signal bounds `STATEMENT.md:74-75`): raw rows iid N(m_n, Σ_n), **Σ_n unit diagonal**, p ≤ n^A; Y = Xθ* + Cε; fixed s₀,
  - cited: **(A3) Signal.** s₀ = |S₀| ≥ 1 fixed; |θ*_j| ∈ [θ_lo, θ_hi] on S₀ (fixed beta-min θ_lo > 0); non-masking **PTV(a₀)**: for every j ∈ S₀ and U ⊆ [p] ∖ {j} with |U| ≤ 15, |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀ (W a population row;

* **L2_k0.md:28** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:50-53`
  - context: δ = δ_n, either branch (`STATEMENT.md:50-53`); **PTV(a₀)** (`STATEMENT.md:74-76`); method and premises of
  - cited: > **Definition (metric locality, LOC_M).** A symmetric matrix Ψ on [p] is in 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) if its spectrum > lies in [c, C] (0 < c ≤ C), and there is a pseudometric δ on [p] with **polynomial growth** > N_δ(r) := max_i |{k : δ(i, k) ≤ r}| ≤ C₀(1 + r)^{d₀} for all r ≥ 0, such that either (Σ-branch) > |Ψ_jk| ≤ K e^{−a δ(j,k)} (j ≠ k) or (Θ-branch) |(Ψ⁻¹)_jk| ≤ K e^{−a δ(j,k)} (j ≠ k).

* **L2_k0.md:28** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:74-76`
  - context: δ = δ_n, either branch (`STATEMENT.md:50-53`); **PTV(a₀)** (`STATEMENT.md:74-76`); method and premises of
  - cited: **(A3) Signal.** s₀ = |S₀| ≥ 1 fixed; |θ*_j| ∈ [θ_lo, θ_hi] on S₀ (fixed beta-min θ_lo > 0); non-masking **PTV(a₀)**: for every j ∈ S₀ and U ⊆ [p] ∖ {j} with |U| ≤ 15, |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀ (W a population row; APP `lemmas/L3_LOC.md:28`). PTV is not used for (i); for (iii) it is one sufficient visibility condition (see (iii)).

* **L2_k0.md:29** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:26-34`
  - context: `STATEMENT.md:26-34`; any X-measurable partition with blocks ≤ 16. Unit diagonal gives c ≤ 1 ≤ C. W denotes a population row.
  - cited: * **Response.** Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the raw design, σ² > 0 fixed; S₀ := supp θ*; response scaled inside the score (FIN s1). * **Method and premises.** D0 score, capped BB(1, p) prior, K_n := min(p, ⌊n/2⌋), Ω = {|S| ≤ K_n}, block tables, start γ₀, start mode S̃₀, LS0 cap ℓ_n + |S̃₀|; implementation premises EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans, IND-T and the

* **L2_k0.md:32** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:15-17`
  - context: `L3_LOC.md:15-17`).
  - cited: **Zero-mean reduction [R03-2].** Replace the raw matrix by W − 1mᵀ and call it W. This leaves CW, X, Y, the partition and every scored model unchanged; hence WLOG m = 0, and all Gaussian regression/norm statements below (e_A, D_{T,l} with iid centred entries, χ² laws) hold as written.

* **L2_k0.md:42** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:15-21`
  - context: | G1 | LOC2 `L3_CTd.md:15-21` (L3.0) | Packing for separated sites: #{d < R} ≤ (2R+1)^d; shells (2m+3)^d, m ≥ 1 | all counts below; CT/RB/TAIL series | (G-shell) of `L1_metric.md` §M0: N_δ(r) ≤ C₀(1+r)^{d₀}, shells m ≥ 0 with counts C₀(m+2)^{d₀} |
  - cited: ## L3.0 Sites and packing A *site map* is x : I → ℝ^d (I finite) with ‖x_i − x_j‖ ≥ 1 for i ≠ j (Euclidean norm; d ≥ 1 fixed); d_ij := ‖x_i − x_j‖. **Packing fact.** For every i and R > 0, #{j : d_ij < R} ≤ (2R + 1)^d; hence for every integer m ≥ 1, #{j : m ≤ d_ij < m + 1} ≤ (2m + 3)^d. *Proof.* The balls B(x_j, ½) are pairwise disjoint (separation ≥ 1); for d_ij < R they lie in B(x_i, R + ½). Com

* **L2_k0.md:43** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:37-38`
  - context: | G2 | LOC2 `L3_CTd.md:37-38` (CT_d (iii)) | Separation ≥ 1 ⇒ shells start at m = 1 | Schur row sums | m ≥ 0; zero-distance pairs give E_ik = 0 (`L1_metric.md` §M1 (ii)–(iii)) |
  - cited: (iii) Schur test. For fixed i, group k by the shell m ≤ d_ik < m + 1 (m ≥ 1 since d_ik ≥ 1). On such a shell, e^{−ad}(e^{t*d} − 1) = e^{−(a−t*)d}(1 − e^{−t*d}) ≤ e^{−(a−t*)m}(1 − e^{−t*(m+1)}). With the packing fact,

* **L2_k0.md:44** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:34-36`
  - context: | G3 | LOC2 `L3_CTd.md:34-36` (CT_d (ii)) | Euclidean φ(y) = ‖y − x_j‖ is 1-Lipschitz | conjugation | φ(i) = δ(i, j), 1-Lipschitz by the triangle inequality (§M1 (ii)) |
  - cited: (ii) Fix j and φ(y) := ‖y − x_j‖ (1-Lipschitz). D := diag(e^{t*φ(x_i)}), A_t := DAD⁻¹ (entries A_ik e^{t*(φ(x_i)−φ(x_k))}), E := A_t − A. E_ii = 0, and for i ≠ k, |E_ik| ≤ |A_ik|(e^{t*|φ(x_i)−φ(x_k)|} − 1) ≤ K e^{−a d_ik}(e^{t*d_ik} − 1) (|e^s − 1| ≤ e^{|s|} − 1, and |φ(x_i) − φ(x_k)| ≤ d_ik).

* **L2_k0.md:45** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:58-65`
  - context: | G4 | LOC2 `L3_CTd.md:58-65`, `:72-75`, `:79-85` (CD_d, RB, TAIL) | CT_d; shells m ≥ 1; "Var ≤ 1", "Ψ_ll ≥ 1" (unit diagonal) | conditional decay, ℓ¹ bound, far-conditioning | CD_M, RB_M, TAIL_M (§M2–M4). Unit diagonal holds for Σ_n here, so even the R01-4 correction is not needed for UNI-0 (it is 
  - cited: *Proof* [R02-1]. As APP L2_CT Lemma CD with Lemma CT replaced by Lemma CT_d. Under either branch, |Θ_jk| ≤ K₁e^{−t₁d_jk} (j ≠ k): under (LOC_d-Σ) by CT_d applied to Σ (α = c), under (LOC_d-Θ) by assumption; this with CT_d applied to Θ (α = 1/C) also gives (c). Let H := [p] ∖ U (the FULL unconditioned complement). For Gaussian W, block inversion gives Cov(W_H | W_U) = (Θ_HH)⁻¹. Θ_HH is a principal 

* **L2_k0.md:45** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:72-75`
  - context: | G4 | LOC2 `L3_CTd.md:58-65`, `:72-75`, `:79-85` (CD_d, RB, TAIL) | CT_d; shells m ≥ 1; "Var ≤ 1", "Ψ_ll ≥ 1" (unit diagonal) | conditional decay, ℓ¹ bound, far-conditioning | CD_M, RB_M, TAIL_M (§M2–M4). Unit diagonal holds for Σ_n here, so even the R01-4 correction is not needed for UNI-0 (it is 
  - cited: *Proof.* B := Σ_{A∪{l}} is a principal submatrix: spectrum in [c, C], off-diagonal entries ≤ K_Σe^{−t_Σ d}. Let Ψ := B⁻¹. Block inversion gives β_A(l)_v = −Ψ_vl/Ψ_ll and Ψ_ll = 1/Var(W_l | W_A) ≥ 1. Lemma CT_d applied to B (α = c, constants (K_Σ, t_Σ)) gives |Ψ_vl| ≤ (2/c)e^{−t_Σ′d_vl}. Sum over shells with the packing fact (d_lv ≥ 1). ∎

* **L2_k0.md:45** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:79-85`
  - context: | G4 | LOC2 `L3_CTd.md:58-65`, `:72-75`, `:79-85` (CD_d, RB, TAIL) | CT_d; shells m ≥ 1; "Var ≤ 1", "Ψ_ll ≥ 1" (unit diagonal) | conditional decay, ℓ¹ bound, far-conditioning | CD_M, RB_M, TAIL_M (§M2–M4). Unit diagonal holds for Σ_n here, so even the R01-4 correction is not needed for UNI-0 (it is 
  - cited: (a) Var(E[W_l | W_T] − E[W_l | W_{T′}]) ≤ κ(r) := (K₂²/c) Σ_{m ≥ ⌊r⌋, m≥1} (2m + 3)^d e^{−2t₂m}, and κ(r) → 0 as r → ∞; (b) Var(W_l | W_{T′}) = Var(W_l | W_T) + Var(E[W_l | W_T] − E[W_l | W_{T′}]). *Proof.* (b) e_T := W_l − E[W_l | W_T] is uncorrelated with every linear function of W_T, in particular with D := E[W_l | W_T] − E[W_l | W_{T′}]; e_{T′} = e_T + D. (a) As in APP L3.6 Step 3: with V := W

* **L2_k0.md:46** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:11-13`
  - context: | G5 | LOC2 `L4_LOCd.md:11-13` | Σ_n ∈ LOC_d: site map x : [p] → ℝ^d, separation ≥ 1, d_jk = ‖x_j − x_k‖ | hypotheses | Σ_n ∈ 𝓛𝓞𝓒 with pseudometric δ (zero distances, distances < 1, any n-dependence allowed) |
  - cited: **Hypotheses.** Setting of STATEMENT §1; Σ_n ∈ LOC_d(c, C, K, a) (L3_CTd §L3.2; K = K_dec, the decay constant) with fixed constants and fixed d ≥ 1; PTV(a₀): |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀ for every j ∈ S₀, U ⊆ [p] ∖ {j}, |U| ≤ 15. (K₂, t₂) of Lemma CD_d; distances d(j, k) := ‖x(j) − x(k)‖.

* **L2_k0.md:47** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:14-16`
  - context: | G6 | LOC2 `L4_LOCd.md:14-16` | "By packing, \|Q⁰\| ≤ s₀(2d_n + 3)^d" | (N0), size ladder, L0′ | \|Q⁰\| ≤ s₀C₀(1 + d_n)^{d₀} (§2) |
  - cited: **Relevance set.** d_n := ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉, Q⁰ := S₀ ∪ {l ∉ S₀ : min_{k∈S₀}d(l, k) ≤ d_n}; Q := Q⁰ if p ≥ 2|Q⁰| + 32s₀ + 1, else Q := [p]. By packing (L3.0), |Q⁰| ≤ s₀(2d_n + 3)^d, so |Q| ≤ 2s₀(2d_n + 3)^d + 32s₀ ≤ (log n)^{d+1} for n ≥ n₀. 𝓛 := {T : S₀ ⊆ T ⊆ Q}.

* **L2_k0.md:48** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:21-21`
  - context: | G7 | LOC2 `L4_LOCd.md:21` (A.1) | κ = d + 1 | Gram floors, L0′ | κ = d₀ + 1 (§3) |
  - cited: ### A.1 Regularity (APP L3.2) — L1_toolkit §L1.2 with κ = d + 1, (P1) → spectrum in [c, C], (P3) → CD_d(b), (P4) → CD_d(a).

* **L2_k0.md:49** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:25-27`
  - context: | G8 | LOC2 `L4_LOCd.md:25-27` (A.2) | "By packing, \|H_l\| ≤ (s₀+1)(2R_n+3)^d" | reference count \|I_l\| = n^{o(1)} | \|H_l\| ≤ (s₀+1)C₀(1+R_n)^{d₀} (§4) |
  - cited: R_n := ⌈(2 log n + log K₂ + log(1 + s₀θ_hi))/t₂⌉, H_l := {j : min_{k∈{l}∪S₀}d(j, k) ≤ R_n}. By packing, |H_l| ≤ (s₀ + 1)(2R_n + 3)^d = O((log n)^d) (was O(log n)), so |I_l| ≤ (|H_l| + 1)^{15} = O((log n)^{15d}) =: N^ref_n [C1-Opus-7] — still exp(O(log log n)), which is all APP L3.3/L3.4 and GROW L6.4 use. Population inputs (i)–(iii) of APP L3.3 by CD_d(a)

* **L2_k0.md:50** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:27-31`
  - context: | G9 | LOC2 `L4_LOCd.md:27-31`, `:33-36` (A.2, A.3) | CD_d(a), (b) with Euclidean d | selection removal, spherical tail | CD_M(a), (b) with δ (§4, §5) |
  - cited: exp(O(log log n)), which is all APP L3.3/L3.4 and GROW L6.4 use. Population inputs (i)–(iii) of APP L3.3 by CD_d(a) (e^{−t₂d} ≤ n^{−2}/(K₂(1 + s₀θ_hi)) for d > R_n; ≤ n^{−1/2}/(1 + s₀θ_hiK₂) for d > d_n) and CD_d(b) (residual variances ≥ min(c, σ²)). The recursive partial-correlation algebra uses only bounded dimensions (|U| ≤ 15) and the entrywise event. Conclusion (6.4) unchanged: |h_{U,l} − h_{

* **L2_k0.md:50** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:33-36`
  - context: | G9 | LOC2 `L4_LOCd.md:27-31`, `:33-36` (A.2, A.3) | CD_d(a), (b) with Euclidean d | selection removal, spherical tail | CD_M(a), (b) with δ (§4, §5) |
  - cited: ### A.3 Spherical tail (APP L3.4) Unchanged with CD_d: ‖α‖ ≤ C K₂ s₀^{1/2}e^{−t₂d_n}/c (each truth residual covariance with W_l given U₀ is ≤ K₂e^{−t₂d_n}, the conditional truth covariance has eigenvalues ≥ c), ‖b_j‖ ≤ √15/c, τ² ∈ [c, 1]; ‖m‖ ≤ C√n e^{−t₂d_n} ≤ C. (6.5)–(6.7) and the counting p·N^ref_n·exp(−t_n(k)/2) ≤ Ck n^{−1/2+o(1)} hold since N^ref_n = n^{o(1)}.

* **L2_k0.md:51** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:38-43`
  - context: | G10 | LOC2 `L4_LOCd.md:38-43` (A.4) | k₀ = O((log n)^{d+1}) | ladder, junk exclusion | k₀ = O((log n)^{d₀}) (§6) |
  - cited: ### A.4 Sandwich incl. the global size ladder (APP L3.5 = GROW L6.5) Unchanged; the only size facts it uses are: k₀ := |Q| + 16s₀ (now O((log n)^{d+1})); the ladder m_i = 2^{i+1}k₀ with at most O(log n) indices below K_n ≤ n/2, giving P(some maximiser has k > 2k₀) ≤ O(log n)·n^{−1/2+o(1)} → 0; feasibility of a truth addition when k ≤ 2k₀ < K_n (Q ≠ [p], K_n ≥ 2|Q| + 32s₀ + 1 by L1.2) or Q = [p]; a

* **L2_k0.md:52** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:46-49`
  - context: | G11 | LOC2 `L4_LOCd.md:46-49` (A.5) | B_l = {v ≠ l : d(v,l) ≤ r_n}, \|B_l\| ≤ (2r_n+3)^d (uses separation: v ≠ l ⇒ d ≥ 1) | frame count N_n | B_l := B(l, r_n) ∖ {l} (may contain v ≠ l at distance 0), \|B_l\| ≤ C₀(1+r_n)^{d₀} (§7) |
  - cited: (N0): |Q| ≤ (log n)^{d+1}, |Q| ≤ K_n (L1.2), p ≤ n^A. (N1): λ_min(Σ_n) ≥ c. Put r_n := log log n and B_l := {v ≠ l : d(v, l) ≤ r_n}; |B_l| ≤ (2r_n + 3)^d. * (R1) For (T, l) ∈ 𝔓 let T′ := T ∩ B_l; frame ι(T, l) := the single functional ψ_{T,l} := e_l − Σ_{v∈T′}β_{T′}(l)_v e_v (e_v coordinate functionals; r_{T,l} = W_l − W_{T′}β_{T′}(l) = e_{T′,l}). Frames are indexed by (l, T′ ⊆ B_l):

* **L2_k0.md:53** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:50-55`
  - context: | G12 | LOC2 `L4_LOCd.md:50-55` (A.5) | Lemma RB (ℓ¹), Lemma TAIL | (R2), (R3) | RB_M, TAIL_M (§7) |
  - cited: N_n ≤ p·2^{(2r_n+3)^d}, log N_n ≤ log p + (2 log log n + 3)^d log 2 = log p + o(log n). m₀ = 1. * (R2) Atoms 𝒜_n := {e_v : v ∈ Q} (Var = 1, |𝒜_n| ≤ |Q|). Since W_Tβ_T(l) − W_{T′}β_{T′}(l) = Σ_{v∈T}λ_{T,l,v}W_v with λ_{T,l} := β_T(l) − β̄_{T′}(l) (zero-padded), e_{T,l} = r_{T,l} − Σ_v λ_{T,l,v}W_v, and by Lemma RB ‖λ_{T,l}‖₁ ≤ 2L₀ =: L. Then L²(log(|𝒜_n| + 1) + log log n) = O(log log n) = o(log n).

* **L2_k0.md:54** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:51-52`
  - context: | G13 | APP `L3_LOC.md:51-52` | Linear-growth fact for the 1-D ordering π_n (≤ 2R+1 per ball, ≤ 2 per distance) | \|Q\|, \|H_l\| = O(log n); L3.6 windows | already replaced by packing in LOC2 (G6, G8); here by growth. APP's ordering metric \|π(j) − π(k)\| has N ≤ 2r + 1 ≤ 2(1 + r): C₀ = 2, d₀ = 1 |
  - cited: **Linear-growth fact (replaces "index line" counting).** Because π_n is a bijection onto [p] ⊂ ℤ, for every l and R ≥ 0, |{v : d(v, l) ≤ R}| ≤ 2R + 1, and for every d ≥ 1 at most two v have d(v, l) = d.

* **L2_k0.md:55** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:30-32`
  - context: | G14 | APP `L3_LOC.md:30-32`, `:75-77` | \|Q\| ≤ s₀(2d_n+1), \|H_l\| ≤ (s₀+1)(2R_n+1) | as G6, G8 | as G6, G8 |
  - cited: **Relevance set.** d_n := ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉, 𝒫⁰ := {l ∉ S₀ : min_{k∈S₀} d(l, k) ≤ d_n}, Q⁰ := S₀ ∪ 𝒫⁰; Q := Q⁰ if Q⁰ = [p] or p ≥ 2|Q⁰| + 32s₀ + 1, else Q := [p]. Then |Q| ≤ s₀(2d_n + 1) ∨ (2|Q⁰| + 32s₀) = O(log n); 𝓛 := {T : S₀ ⊆ T ⊆ Q}.

* **L2_k0.md:55** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:75-77`
  - context: | G14 | APP `L3_LOC.md:30-32`, `:75-77` | \|Q\| ≤ s₀(2d_n+1), \|H_l\| ≤ (s₀+1)(2R_n+1) | as G6, G8 | as G6, G8 |
  - cited: Replace R_n := ⌈2 log n/log(1/r)⌉ by R_n := ⌈(2 log n + log K₂ + log(1 + s₀θ_hi))/t₂⌉ and the neighbourhood by H_l := {j : min_{k∈{l}∪S₀} d(j, k) ≤ R_n}; |H_l| ≤ (s₀ + 1)(2R_n + 1) = O(log n) by the linear-growth fact, so |I_l| ≤ C(1 + log n)^{15}. The proof's population inputs: (i) |Cov(W_l, W_v | W_{U₀})| ≤ K₂e^{−t₂d(l,v)} ≤ n^{−2} for

* **L2_k0.md:56** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:98-156`
  - context: | G15 | APP `L3_LOC.md:98-156` (L3.6, window NA) | windows on the line, "at most two v per distance" | NA | **not used**: LOC2 replaced L3.6 by NA-R (A.5); so is UNI-0 |
  - cited: ## L3.6 NA without the Markov property (replaces [L6] L6.6) — new **Lemma L3.6.** Under the hypotheses of Theorem LOC (PTV not needed), P(NA(𝓛)) → 1.  *Proof.* By GROW L2.2 (on the L0 event for the lattice family, which holds w.p. → 1 under the joint law as in [L6] §1 / L3.2), it suffices to show P(max_{T∈𝓛, l∉T} Z²_{T,l} ≤ c_n) → 1, where c_n := log(n + 1) + 2 log p − 2 log(|Q| + 1) − 4κ_E − 2 an

* **L2_k0.md:57** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:171-177`
  - context: | G16 | GROW `L6_random_AR1.md:171-177`, `:194-201`, `:256`, `:263` | AR(1) index distance, P2 Markov (L6.6 only), P4 decay r^{\|j−k\|}, R_n with log(1/r), "H_l has O(log n) elements" | L6.3, L6.4 | replaced by APP (P4 → CD(a), P3 → CD(b), `L3_LOC.md:45-50`), then LOC2 (CD_d), here CD_M; P2 not used
  - cited: For all l outside Q define the deterministic neighborhood  H_l={j: dist(j,{l} union S0)<=R_n}, R_n=ceil(2 log n/log(1/r)).  It has O(log n) elements. Let I_l be all U0 subset H_l minus {l} with

* **L2_k0.md:57** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:45-50`
  - context: | G16 | GROW `L6_random_AR1.md:171-177`, `:194-201`, `:256`, `:263` | AR(1) index distance, P2 Markov (L6.6 only), P4 decay r^{\|j−k\|}, R_n with log(1/r), "H_l has O(log n) elements" | L6.3, L6.4 | replaced by APP (P4 → CD(a), P3 → CD(b), `L3_LOC.md:45-50`), then LOC2 (CD_d), here CD_M; P2 not used
  - cited: **AR(1) facts used by [L6]** (GROW L5 (P1)–(P4)): (P1) spectrum in [c₋, c₊]; (P2) Markov nearest-neighbour regression; (P3) Var(W_l | W_U) ≥ c₋-type floor; (P4) |Cov(W_j, W_k | W_U)| ≤ r^{|j−k|} for all U. **Replacements:** (P1) → spectrum in [c, C]; (P3) → Lemma CD(b) (Var(W_j | W_U) ≥ c, and every conditional covariance matrix has spectrum in [c, C]); (P4) → Lemma CD(a) (|Cov(W_j, W_k | W_U)| ≤ 

* **L2_k0.md:57** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:194-201`
  - context: | G16 | GROW `L6_random_AR1.md:171-177`, `:194-201`, `:256`, `:263` | AR(1) index distance, P2 Markov (L6.6 only), P4 decay r^{\|j−k\|}, R_n with log(1/r), "H_l has O(log n) elements" | L6.3, L6.4 | replaced by APP (P4 → CD(a), P3 → CD(b), `L3_LOC.md:45-50`), then LOC2 (CD_d), here CD_M; P2 not used
  - cited: *Proof.* Put U0=U intersect H_l, V=U minus U0. In the population, conditional covariance of W_l with any W_v, v in V, given W_U0 is at most r^{|l-v|}<=r^{R_n}<=n^{-2}. Likewise conditional covariance of Y with W_v is at most C sum_{j in S0 minus U0}r^{|j-v|}<=C n^{-2}, using P4 and the bounded coefficients theta_j/t_j. Noise has zero population covariance. The population residual correlation of W_

* **L2_k0.md:57** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:256-256`
  - context: | G16 | GROW `L6_random_AR1.md:171-177`, `:194-201`, `:256`, `:263` | AR(1) index distance, P2 Markov (L6.6 only), P4 decay r^{\|j−k\|}, R_n with log(1/r), "H_l has O(log n) elements" | L6.3, L6.4 | replaced by APP (P4 → CD(a), P3 → CD(b), `L3_LOC.md:45-50`), then LOC2 (CD_d), here CD_M; P2 not used
  - cited: bound of Sigma. Hence ||alpha||<=C r^{d_n}. The coefficients b_j are

* **L2_k0.md:57** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:263-263`
  - context: | G16 | GROW `L6_random_AR1.md:171-177`, `:194-201`, `:256`, `:263` | AR(1) index distance, P2 Markov (L6.6 only), P4 decay r^{\|j−k\|}, R_n with log(1/r), "H_l has O(log n) elements" | L6.3, L6.4 | replaced by APP (P4 → CD(a), P3 → CD(b), `L3_LOC.md:45-50`), then LOC2 (CD_d), here CD_M; P2 not used
  - cited: entries, and c_-<=tau^2<=1. Conditional on W_D and eps, the residual

* **L2_k0.md:58** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:108-112`
  - context: | G17 | GROW `L6_random_AR1.md:108-112`, `:162-163`, `:332`, `:387` | sizes "C_m log n", "C p 2^q", "k ≤ 2k₀ = O(log n)" (consequences of q = O(log n), not geometry) | Gram floors, A_score, junk exclusion | LOC2 L1 (L0′ and L1.2, `L1_toolkit.md:9-59`) for \|Q\| ≤ (log n)^κ, any fixed κ; κ = d₀ + 1 h
  - cited: For any fixed C_m, EVERY standardized Gram submatrix of size at most C_m log n has operator error at most C_m log n O(ħ_n)=o(1), since operator norm is bounded by size times maximal entry. Population eigenvalues are in [c_-,c_+], so the sample lower bound is c_-/2 for n large. This simultaneously covers (G2), all blocks, and fixed-order anchored SE; no union over subsets

* **L2_k0.md:58** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:9-59`
  - context: | G17 | GROW `L6_random_AR1.md:108-112`, `:162-163`, `:332`, `:387` | sizes "C_m log n", "C p 2^q", "k ≤ 2k₀ = O(log n)" (consequences of q = O(log n), not geometry) | Gram floors, A_score, junk exclusion | LOC2 L1 (L0′ and L1.2, `L1_toolkit.md:9-59`) for \|Q\| ≤ (log n)^κ, any fixed κ; κ = d₀ + 1 h
  - cited: ## L1.1 Lemma L0′ Let 𝔉 = 𝔉_n be a deterministic family of subsets of [p] with ∅ ∈ 𝔉, |A| ≤ J_n for A ∈ 𝔉, a Gram floor λ_min(R̂_A) ≥ φ₀² > 0 on nonempty A ∈ 𝔉, ‖μ‖² ≤ Mn, and 𝒱𝒱 = 𝒱𝒱_n a deterministic vector set, with J_n ≤ (log n)^κ, log|𝔉_n| ≤ (log n)^κ, log|𝒱𝒱_n| ≤ (log n)^κ  (κ ≥ 1 fixed). Replace in [GEN-L1] t_n := 4(D + 2) log n by t_n := 4(log|𝔉_n| + 2 log n + J_n), and h_n := √(2(D_V + 1)

* **L2_k0.md:58** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:162-163`
  - context: | G17 | GROW `L6_random_AR1.md:108-112`, `:162-163`, `:332`, `:387` | sizes "C_m log n", "C p 2^q", "k ≤ 2k₀ = O(log n)" (consequences of q = O(log n), not geometry) | Gram floors, A_score, junk exclusion | LOC2 L1 (L0′ and L1.2, `L1_toolkit.md:9-59`) for \|Q\| ≤ (log n)^κ, any fixed κ; κ = d₀ + 1 h
  - cited: X in A_X, the first family has size <=17(p+1)^16 and the second has size <=C p 2^q, all have the required Gram floors and energy bound. Their

* **L2_k0.md:58** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:332-332`
  - context: | G17 | GROW `L6_random_AR1.md:108-112`, `:162-163`, `:332`, `:387` | sizes "C_m log n", "C p 2^q", "k ≤ 2k₀ = O(log n)" (consequences of q = O(log n), not geometry) | Gram floors, A_score, junk exclusion | LOC2 L1 (L0′ and L1.2, `L1_toolkit.md:9-59`) for \|Q\| ≤ (log n)^κ, any fixed κ; κ = d₀ + 1 h
  - cited: block let N_b=U_b minus Q. With k0=q+16s0,

* **L2_k0.md:58** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:387-387`
  - context: | G17 | GROW `L6_random_AR1.md:108-112`, `:162-163`, `:332`, `:387` | sizes "C_m log n", "C p 2^q", "k ≤ 2k₀ = O(log n)" (consequences of q = O(log n), not geometry) | Gram floors, A_score, junk exclusion | LOC2 L1 (L0′ and L1.2, `L1_toolkit.md:9-59`) for \|Q\| ≤ (log n)^κ, any fixed κ; κ = d₀ + 1 h
  - cited: since k<=2k0=O(log n). This contradicts maximality. If Q=[p]

* **L2_k0.md:67** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:14-14`
  - context: S₀ ∪ {…}, `L4_LOCd.md:14`); Q := Q⁰ if p ≥ 2|Q⁰| + 32s₀ + 1, Q := [p] otherwise (the test uses Q⁰, not Q). Q is
  - cited: **Relevance set.** d_n := ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉, Q⁰ := S₀ ∪ {l ∉ S₀ : min_{k∈S₀}d(l, k) ≤ d_n};

* **L2_k0.md:74** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:57-59`
  - context: K_n = min(p, ⌊n/2⌋) ≥ 2|Q| + 32s₀ + 1. Otherwise Q = [p]. Exactly as LOC2 `L1_toolkit.md:57-59`. Also |Q| ≤ K_n
  - cited: * **(G1)** Q = [p] or K_n ≥ 2|Q| + 32s₀ + 1: by the enlargement rule (Q⁰ kept iff p ≥ 2|Q⁰| + 32s₀ + 1) and K_n = min(p, ⌊n/2⌋) ≥ 2|Q| + 32s₀ + 1 once ⌊n/2⌋ ≥ 2(log n)^κ + 32s₀ + 1; in the enlarged case Q = [p], |Q| = p ≤ 2|Q⁰| + 32s₀ = O((log n)^κ) and K_n = p eventually.

* **L2_k0.md:75** → `Theory_work/Wave2/W2-LOC2/lemmas/L5_assembly.md:24-24`
  - context: eventually (q ≤ p and q = o(n)), as LOC2 `L5_assembly.md:24` [R04-2].
  - cited: |Q| ≤ K_n (q ≤ p and q ≤ (log n)^κ = o(n), so q ≤ ⌊n/2⌋ eventually and q ≤ min(p, ⌊n/2⌋) = K_n [R04-2]), (N1) is assumed; so P(max_𝔓 Z²_{T,l} ≤ c_n) → 1, and GROW L2.2 on 𝓔_n ∩ {that event}

* **L2_k0.md:79** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:21-22`
  - context: ## 3. A.1 Regularity (delta to LOC2 `L4_LOCd.md:21-22` → APP `L3_LOC.md:54-72` → GROW `L6_random_AR1.md:84-167`)
  - cited: ### A.1 Regularity (APP L3.2) — L1_toolkit §L1.2 with κ = d + 1, (P1) → spectrum in [c, C], (P3) → CD_d(b), (P4) → CD_d(a). TV from PTV verbatim. Lattice family A_score by L0′.

* **L2_k0.md:79** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:54-72`
  - context: ## 3. A.1 Regularity (delta to LOC2 `L4_LOCd.md:21-22` → APP `L3_LOC.md:54-72` → GROW `L6_random_AR1.md:84-167`)
  - cited: ## L3.2 Regularity (= [L6] L6.2) [L6] L6.2 proves: an entrywise event (raw centred columns + noise column, error ħ_n = C_A√(log n/n)), X-events A_X and a joint event A_cov, on which (H0), (G1), (G2), (G3a), (G3b) hold with common constants and bounded-size sample partial correlations are within O(ħ_n) of population values. Step by step: * entrywise concentration, polarisation, union over (p + 1)² 

* **L2_k0.md:79** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:84-167`
  - context: ## 3. A.1 Regularity (delta to LOC2 `L4_LOCd.md:21-22` → APP `L3_LOC.md:54-72` → GROW `L6_random_AR1.md:84-167`)
  - cited:  *Proof.* Adjoin the independent noise column eps/sigma to W. An orthonormal basis of 1-perp turns these centered columns into N independent Gaussian rows with the same covariance, enlarged by an independent unit coordinate. For a scalar standard Gaussian G, its squared-sum mgf is E exp(t sum G_i^2)=(1-2t)^(-N/2). Chernoff, using

* **L2_k0.md:81** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:45-59`
  - context: LOC2 L1.2 (`L1_toolkit.md:45-59`) with κ = d₀ + 1. Step by step:
  - cited: Setting: raw rows iid N(0, Σ_n), Σ_n unit diagonal with λ_min(Σ_n) ≥ c (or, for (N1) only, on Q ∪ {l}); ħ_n := C_A√(log n/n). GROW L6.2's entrywise event (raw centred columns + noise column; union over (p + 1)² entries; Gaussian + unit variances only) and its standardised version A_X hold with probability → 1, unchanged. On it: * **Gram floors for polylog sets.** For every S with |S| ≤ J_n := (log

* **L2_k0.md:82** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:85-104`
  - context: * Entrywise event (GROW `L6_random_AR1.md:85-104`): Gaussian rows, **unit variances** (polarisation needs variances of
  - cited: *Proof.* Adjoin the independent noise column eps/sigma to W. An orthonormal basis of 1-perp turns these centered columns into N independent Gaussian rows with the same covariance, enlarged by an independent unit coordinate. For a scalar standard Gaussian G, its squared-sum mgf is E exp(t sum G_i^2)=(1-2t)^(-N/2). Chernoff, using -log(1-u)-u <= u^2 for |u|<=1/2, gives

* **L2_k0.md:84** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:48-50`
  - context: * Gram floors for every |S| ≤ (log n)^{κ′} (`W2-LOC2/lemmas/L1_toolkit.md:48-50`): needs only λ_min(Σ_S) ≥ c (spectrum ⊆ [c, C]) — lower
  - cited: * **Gram floors for polylog sets.** For every S with |S| ≤ J_n := (log n)^{κ′}, any fixed κ′ [C1-Opus-4], ‖R̂_S − Σ_S‖_op ≤ |S|·max entry error ≤ C J_n ħ_n → 0; hence λ_min(R̂_S) ≥ c/2 for n ≥ n₀ whenever λ_min(Σ_S) ≥ c. This covers (G2) (|Q ∪ {l}| ≤ (log n)^κ), all blocks (≤ 16), within-block SE and the lattice family (no union over subsets is needed after the entrywise event).

* **L2_k0.md:87** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:63-66`
  - context: * TV from PTV (APP `L3_LOC.md:63-66`; GROW `L6_random_AR1.md:128-141`): bounded dimensions, inverse norms ≤ 2/c, residual
  - cited: * TV (G3b): [L6] uses P3/P4 + (6.0) to get a population residual covariance ≥ a₀ for every j ∈ S₀, |U| ≤ 15; here PTV gives it directly. The perturbation argument (bounded dimension, inverse norms ≤ 2/c, fixed coefficients θ*_j, sample-scale coefficients θ*_j/t_j within O(ħ_n) of θ*_j) is unchanged, with residual column variance ≤ 1. Hence δ²_{U,j} ≥ N a₀²/4 eventually, M_n := N a₀²/(4 log n).

* **L2_k0.md:87** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:128-141`
  - context: * TV from PTV (APP `L3_LOC.md:63-66`; GROW `L6_random_AR1.md:128-141`): bounded dimensions, inverse norms ≤ 2/c, residual
  - cited: For TV, for every j in S0 and every U not containing j with |U|<=15, the population residual covariance with sum theta_k W_k is, by P3/P4 and (6.0), at least in absolute value  a0=(theta_min/2)(1-r^2)/(1+r^2)>0. 

* **L2_k0.md:89** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:143-155`
  - context: * A_cov (GROW `L6_random_AR1.md:143-155`): bounded-size conditional covariances; needs Var(W_j | W_U) ≥ c (CD_M(b)) and
  - cited: For later partial correlations involving Y, use raw centered columns and write mu=C sum theta_j W_j/t_j [A1]. On the entrywise event these coefficients are bounded and differ from theta by O(ħ_n). All fixed-dimensional sample conditional covariances therefore differ by O(ħ_n) from the population algebra using the same coefficients theta_j/t_j. This is a uniform algebraic bound for all coefficient 

* **L2_k0.md:91** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:54-56`
  - context: * (G1): §2. A_score (`W2-LOC2/lemmas/L1_toolkit.md:54-56`): first family (subsets ≤ 16, ≤ 17(p+1)^{16} members) by L0; lattice family by
  - cited: * **A_score** (GROW L6.2 [A3]): the L0 events for the first family (all subsets of size ≤ 16; ≤ 17(p + 1)^{16} members) and, by L0′, for the lattice family (log size O((log n)^κ)); conditional on X ∈ A_X the Gram floors hold with common constants, so L0′'s conditional Gaussian bounds give a uniform o(1) failure probability; integrate.

* **L2_k0.md:93** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:28-32`
  - context: κ_tool = d₀ + 2 (`W2-LOC2/lemmas/L1_toolkit.md:28-32`).
  - cited: **Consequence for GROW L2.0–L2.2.** For S₀ ⊆ Q, |Q| ≤ (log n)^κ, and the lattice family 𝔉 of GROW L2.0 (|A| ≤ |Q| + 1, |𝔉| ≤ 1 + 2^{|Q∖S₀|}(1 + p + s₀ + s₀p), 𝒱𝒱 := {r_A − r_{A′}} ∪ {r_A}, |𝒱𝒱| ≤ 2|𝔉|²): J_n = |Q| + 1, log|𝔉| ≤ |Q| log 2 + (A + 1) log n + log(4s₀) and log|𝒱𝒱| ≤ log 2 + 2 log|𝔉| are O((log n)^κ), hence each is ≤ (log n)^{κ+1} for n ≥ n₀; so L0′ applies with envelope exponent κ_tool

* **L2_k0.md:95** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:24-31`
  - context: ## 4. A.2 Selection removal (delta to LOC2 `L4_LOCd.md:24-31` → APP `L3_LOC.md:74-83` → GROW `L6_random_AR1.md:171-212`)
  - cited: ### A.2 Selection removal (APP L3.3) R_n := ⌈(2 log n + log K₂ + log(1 + s₀θ_hi))/t₂⌉, H_l := {j : min_{k∈{l}∪S₀}d(j, k) ≤ R_n}. By packing, |H_l| ≤ (s₀ + 1)(2R_n + 3)^d = O((log n)^d) (was O(log n)), so |I_l| ≤ (|H_l| + 1)^{15} = O((log n)^{15d}) =: N^ref_n [C1-Opus-7] — still exp(O(log log n)), which is all APP L3.3/L3.4 and GROW L6.4 use. Population inputs (i)–(iii) of APP L3.3 by CD_d(a) (e^{−

* **L2_k0.md:95** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:74-83`
  - context: ## 4. A.2 Selection removal (delta to LOC2 `L4_LOCd.md:24-31` → APP `L3_LOC.md:74-83` → GROW `L6_random_AR1.md:171-212`)
  - cited: ## L3.3 Selection removal (= [L6] L6.3) Replace R_n := ⌈2 log n/log(1/r)⌉ by R_n := ⌈(2 log n + log K₂ + log(1 + s₀θ_hi))/t₂⌉ and the neighbourhood by H_l := {j : min_{k∈{l}∪S₀} d(j, k) ≤ R_n}; |H_l| ≤ (s₀ + 1)(2R_n + 1) = O(log n) by the linear-growth fact, so |I_l| ≤ C(1 + log n)^{15}. The proof's population inputs: (i) |Cov(W_l, W_v | W_{U₀})| ≤ K₂e^{−t₂d(l,v)} ≤ n^{−2} for v ∉ H_l (CD(a)); (ii

* **L2_k0.md:95** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:171-212`
  - context: ## 4. A.2 Selection removal (delta to LOC2 `L4_LOCd.md:24-31` → APP `L3_LOC.md:74-83` → GROW `L6_random_AR1.md:171-212`)
  - cited: For all l outside Q define the deterministic neighborhood  H_l={j: dist(j,{l} union S0)<=R_n}, R_n=ceil(2 log n/log(1/r)).  It has O(log n) elements. Let I_l be all U0 subset H_l minus {l} with

* **L2_k0.md:112** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:203-212`
  - context: The recursive partial-correlation algebra (GROW `L6_random_AR1.md:203-212`) uses only |U| ≤ 15, the entrywise event and
  - cited: Let a,b be the sample vectors of partial correlations of W_l and Y, respectively, with W_V given U0, and R their sample conditional correlation matrix. Lemma L6.2 gives ||a||+||b||<=C ħ_n, ||R^{-1}||<=C, uniformly. The inverse bound follows also directly from Schur complements of the bounded-size joint Gram. The exact recursive correlation formula is 

* **L2_k0.md:116** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:33-36`
  - context: ## 5. A.3 Spherical tail (delta to LOC2 `L4_LOCd.md:33-36` → APP `L3_LOC.md:85-91` → GROW `L6_random_AR1.md:223-310`)
  - cited: ### A.3 Spherical tail (APP L3.4) Unchanged with CD_d: ‖α‖ ≤ C K₂ s₀^{1/2}e^{−t₂d_n}/c (each truth residual covariance with W_l given U₀ is ≤ K₂e^{−t₂d_n}, the conditional truth covariance has eigenvalues ≥ c), ‖b_j‖ ≤ √15/c, τ² ∈ [c, 1]; ‖m‖ ≤ C√n e^{−t₂d_n} ≤ C. (6.5)–(6.7) and the counting p·N^ref_n·exp(−t_n(k)/2) ≤ Ck n^{−1/2+o(1)} hold since N^ref_n = n^{o(1)}.

* **L2_k0.md:116** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:85-91`
  - context: ## 5. A.3 Spherical tail (delta to LOC2 `L4_LOCd.md:33-36` → APP `L3_LOC.md:85-91` → GROW `L6_random_AR1.md:223-310`)
  - cited: ## L3.4 Spherical tail (= [L6] L6.4) Regression W_l = W_{U₀}b + m_raw + e with D := U₀ ∪ S₀: (i) ‖α‖ ≤ C e^{−t₂d_n}·K₂ s₀^{1/2}/c, because the covariance of W_l with the truth residuals given U₀ has entries ≤ K₂e^{−t₂d_n} (CD(a)) and the conditional truth covariance has eigenvalues ≥ c (CD(b)); (ii) the b_j (regressions of truths on U₀, |U₀| ≤ 15) are bounded: ‖b_j‖ ≤ ‖Σ_{U₀U₀}⁻¹‖‖Σ_{U₀j}‖ ≤ √15/c

* **L2_k0.md:116** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:223-310`
  - context: ## 5. A.3 Spherical tail (delta to LOC2 `L4_LOCd.md:33-36` → APP `L3_LOC.md:85-91` → GROW `L6_random_AR1.md:223-310`)
  - cited: **Lemma L6.4. PROVED (by this seat, unchecked).** There are constants C,c>0 such that, uniformly in l outside Q, fixed U0 in I_l, and log n/2 <= t <= (2A+3)log n,  P(A_cov intersect {h_{U0,l}>=t}) <= C exp(-t/2+C sqrt(log n)) + C exp(-c sqrt(n)).          (6.5)

* **L2_k0.md:125** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:38-43`
  - context: ## 6. A.4 Sandwich incl. global size ladder (delta to LOC2 `L4_LOCd.md:38-43` → APP `L3_LOC.md:93-96` → GROW `L6_random_AR1.md:313-388`)
  - cited: ### A.4 Sandwich incl. the global size ladder (APP L3.5 = GROW L6.5) Unchanged; the only size facts it uses are: k₀ := |Q| + 16s₀ (now O((log n)^{d+1})); the ladder m_i = 2^{i+1}k₀ with at most O(log n) indices below K_n ≤ n/2, giving P(some maximiser has k > 2k₀) ≤ O(log n)·n^{−1/2+o(1)} → 0; feasibility of a truth addition when k ≤ 2k₀ < K_n (Q ≠ [p], K_n ≥ 2|Q| + 32s₀ + 1 by L1.2) or Q = [p]; a

* **L2_k0.md:125** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:93-96`
  - context: ## 6. A.4 Sandwich incl. global size ladder (delta to LOC2 `L4_LOCd.md:38-43` → APP `L3_LOC.md:93-96` → GROW `L6_random_AR1.md:313-388`)
  - cited: ## L3.5 Sandwich incl. the global size ladder (= [L6] L6.5) Unchanged: it uses (6.10) (from L0.2(c) and L3.3), per-block optimality and the exact prior ratio, block size ≤ 16, the counts J(t) of L3.4, the TV part of L3.2, and the construction of Q (feasibility of additions when Q ≠ [p]; Q = [p] case). No AR(1) fact is used beyond those replaced in L3.2–L3.4. Conclusion: P(S₀ ⊆ S̃ ⊆ Q for every max

* **L2_k0.md:125** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:313-388`
  - context: ## 6. A.4 Sandwich incl. global size ladder (delta to LOC2 `L4_LOCd.md:38-43` → APP `L3_LOC.md:93-96` → GROW `L6_random_AR1.md:313-388`)
  - cited: **Lemma L6.5. PROVED (by this seat, unchecked).** The first event in (6.1) has probability tending to one.  *Proof.* On A_cov intersect A_score, for any l outside Q, |U|<=15, the table increment obeys, uniformly, 

* **L2_k0.md:129** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:366-378`
  - context: s₀Σ_{a≤15}C(p, a) = n^{O(1)} unit normals (GROW `L6_random_AR1.md:366-378`), TV from §3, feasibility of an addition when
  - cited: Truth inclusion follows from the TV part of L6.2 and the same argument as L3.3(a), detailed here to record uniformity. Conditional on X, all Z_{U,j}, j in S0, |U|<=15, j notin U, are unit normals. There are at most s0 sum_{a<=15}binom(p,a)=n^{O(1)}, so a normal union bound gives max Z^2<=C log n with probability tending to one. Hence each missing truth has add gain RSS_U-RSS_{U+j}=(delta+sigma Z)^

* **L2_k0.md:131** → `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:380-388`
  - context: l ∈ S̃ ∖ Q gains ≥ ¼ log n − log k − 2κ_E − o(1) > 0 since log k ≤ log 2k₀ = O(log log n) (GROW `L6_random_AR1.md:380-388`).
  - cited: Finally work also on (6.7)'s complementary high-probability event. If l in S_tilde minus Q, deleting l gains at least  log(p/k)+(1/2)log(n+1)-(1/2)h_{U_b minus {l},l} -2 kappa_E-o(1) >= (1/4)log n-log k-2 kappa_E-o(1)>0,

* **L2_k0.md:135** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:45-56`
  - context: ## 7. A.5 NA via Lemma NA-R (delta to LOC2 `L4_LOCd.md:45-56`; hypotheses `L2_NAR.md:23-36`)
  - cited: ### A.5 NA via Lemma NA-R (N0): |Q| ≤ (log n)^{d+1}, |Q| ≤ K_n (L1.2), p ≤ n^A. (N1): λ_min(Σ_n) ≥ c. Put r_n := log log n and B_l := {v ≠ l : d(v, l) ≤ r_n}; |B_l| ≤ (2r_n + 3)^d. * (R1) For (T, l) ∈ 𝔓 let T′ := T ∩ B_l; frame ι(T, l) := the single functional ψ_{T,l} := e_l − Σ_{v∈T′}β_{T′}(l)_v e_v (e_v coordinate functionals; r_{T,l} = W_l − W_{T′}β_{T′}(l) = e_{T′,l}). Frames are indexed by (l

* **L2_k0.md:135** → `Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md:23-36`
  - context: ## 7. A.5 NA via Lemma NA-R (delta to LOC2 `L4_LOCd.md:45-56`; hypotheses `L2_NAR.md:23-36`)
  - cited: * (N0) p ≤ n^A; S₀ ⊆ Q ⊆ [p]; q := |Q| ≤ (log n)^κ; q ≤ K_n = min(p, ⌊n/2⌋) (so every T ∈ 𝓛 := {T : S₀ ⊆ T ⊆ Q} is feasible). * (N1) λ_min(Σ_{Q∪{l}}) ≥ c > 0 for every l ∈ [p]. Let 𝔓 := {(T, l) : T ∈ 𝓛, l ∈ [p] ∖ T}; for (T, l) ∈ 𝔓, β_{T,l} := Σ_TT⁻¹Σ_{Tl}, e_{T,l} := W_l − W_Tβ_{T,l}, τ²_{T,l} := Var(W_l | W_T) (the common variance of the iid entries of e_{T,l}). By (N1), τ²_{T,l} ≥ c. * (R1) *Re

* **L2_k0.md:150** → `Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md:38-41`
  - context: Lemma NA-R (`W2-LOC2/lemmas/L2_NAR.md:38-41`) gives P(max_𝔓 Z²_{T,l} ≤ c_n) → 1; with GROW L2.2 on the L0′ event 𝓔_n
  - cited: **Lemma NA-R.** Under (N0)–(N1), (R1)–(R3): with c_n := log(n + 1) + 2 log p − 2 log(|Q| + 1) − 4κ_E − 2 (GROW L2.2; κ_E the constant of the common score expansion, L0/L0′), P(Z_{T,l} is defined and Z²_{T,l} ≤ c_n for all (T, l) ∈ 𝔓) → 1 (vacuous if 𝔓 = ∅); Z_{T,l} is formed from the SAMPLE normalised residual u_{T,l} (GROW L2.0). Combined with GROW L2.2 on the L0′ event of the lattice family (L1_

* **L2_k0.md:151** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:37-42`
  - context: (`W2-LOC2/lemmas/L1_toolkit.md:37-42`), **P(NA(𝓛)) → 1.** (NA-R uses no PTV, partition or signal.)
  - cited: * GROW L2.2 (NA reduction) holds on 𝓔_n ∩ {max Z²_{T,l} ≤ c_n}: its proof uses k ≤ |Q| (prior term ≤ log(|Q| + 1) − log p), x := σ²Z²/RSS_T ≤ c_n/(n(1 − ω_n)) ≤ ¼ (c_n = O(log n)), and an excess O(log n)(ϑ_n + log n/n) → 0 with ϑ_n := (1 + 0.02/n)/(1 − ω_n) − 1 = O(ω_n + 1/n). The last step needs the RATE [R02-3]: ω_n log n = O(n^{−1/3}log n + (log n)^{κ+1}/n) → 0 (from t_n + h_n² = O((log n)^κ)),

* **L2_k0.md:153** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:58-58`
  - context: ## 8. A.6 TL (delta to LOC2 `L4_LOCd.md:58`)
  - cited: ### A.6 TL — GROW L2.1 on 𝓔_n (L1_toolkit L1.1), conditional on X ∈ A_X, integrated (as APP L3.7). ∎ (Part A, with L5.)

* **L2_k0.md:154** → `Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md:33-36`
  - context: GROW L2.1 on 𝓔_n (`W2-LOC2/lemmas/L1_toolkit.md:33-36`) conditionally on X ∈ A_X (Gram floor c/2 on Q ∪ {l} from §3), fixed θ_lo > 0,
  - cited: * GROW L2.1 (TL) holds on 𝓔_n for n ≥ n₀, under (G2) and the FIXED beta-min θ_lo > 0 of STATEMENT §1 (signal ≍ n; no general BM-∞ version is claimed — the signal must dominate t_n + h_n², not only log n) [R01-6]: its proof uses RSS_A − RSS_T ≥ Λ_A − 2σh_n√Λ_A − σ²t_n ≥ Λ_A/4 for Λ_A ≥ L′_n = (n − 1)φ₀²θ²_min, true since h_n², t_n = O((log n)^κ) = o(n); the final comparison (A + 1) log n + 1 + 2κ_E

* **L2_k0.md:155** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:158-160`
  - context: integrated (APP `L3_LOC.md:158-160`). No geometry. **P(TL(𝓛)) → 1.**
  - cited: ## L3.7 TL (= [L6] L6.7) Unchanged: conditional on X in A_X the hypotheses of GROW L2.1 hold with common constants; missing-truth signal ≥ cn by (G2)-type floors and θ_lo; integrate.

* **L2_k0.md:157** → `Theory_work/Wave2/W2-LOC2/lemmas/L5_assembly.md:13-33`
  - context: ## 9. Assembly via Theorem PLR (LOC2 `L5_assembly.md:13-33`)
  - cited: **Theorem PLR** [R01-1: split]. Setting of STATEMENT §1 (fixed θ_lo > 0). Let Q ⊇ S₀ be deterministic with |Q| ≤ (log n)^κ and the feasibility dichotomy (Q = [p] or K_n ≥ 2|Q| + 32s₀ + 1), with the floor (N1) λ_min(Σ_{n,Q∪{l}}) ≥ c for all l, and suppose (i) P(Sand_n) → 1, (ii) for some latent extension as in Lemma NA-R, (R1)–(R3) hold for Q [C1-Opus-6]. Then, under the joint law of (X, ε) and the

* **L2_k0.md:161** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:45-45`
  - context: for all S (sufficient, `STATEMENT.md:45`), so APP L1_POST(b) gives 1 − π(S₀) = O_P(√(log n/n)), hence E[1 − π(S₀)] → 0, and
  - cited: they are not asserted necessary. (Sufficient: λ_min(Σ_n) ≥ c.)

* **L2_k0.md:164** → `Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:7-35`
  - context: ## 10. Delivery (R4; LOC2 `L7_delivery.md:7-35`, FACA `L7_delivery.md:7-49`)
  - cited: **Method, premises, allocation.** Exactly those of Proposition F-FAC (FACA L7, first paragraph): v3.1 with deterministic complete-scan LS0 from the exact e4 start-mode maximiser (TDP-IMPL), LS0 move cap a_n = ℓ_n + |S̃₀| (the merged cap), all other caps ℓ_n; total tier-1 fallback with complete fallback-grid freezing; EX-A, IDEAL-W, EX-S, SR, e4, GUARD-W, MACH, CONFIG (fixed R′ = 4k, fixed worker c

* **L2_k0.md:164** → `Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md:7-49`
  - context: ## 10. Delivery (R4; LOC2 `L7_delivery.md:7-35`, FACA `L7_delivery.md:7-49`)
  - cited: **Method, premises, allocation** (exactly those of FINAL s6 Proposition F / A1's corrected statement with the A4 preflight addition): v3.1 with deterministic complete-scan LS0 from the exact e4 start-mode maximiser (TDP-IMPL), LS0 move cap a_n = ℓ_n + |S̃₀| (= the merged MR1 (C-GROW) cap), all other caps ℓ_n; total tier-1 fallback with complete fallback-grid freezing; EX-A (unit-cost exact reals),

* **L2_k0.md:166** → `Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:14-15`
  - context: (LOC-d, LOC-BF, L6_poly; `L7_delivery.md:14-15`); its proof uses the class only at two places, both verified here:
  - cited: **Classes.** Iid Gaussian rows satisfying Theorem LOC-d (L4 Part A), Theorem LOC-BF (L4 Part B), or the polynomial-decay theorem of L6_poly (α > 17/2; added after its checks R06a/R06b).

* **L2_k0.md:167** → `Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:21-25`
  - context: * **Step 1 (input validity, design setting (R)).** Needs λ_min(Σ_n) ≥ c > 0 (LOC2 `L7_delivery.md:21-25`; FACA
  - cited: *Proof.* **Step 1 (input validity; FACA L7 Step 1).** λ_min(Σ_n) ≥ c > 0 (LOC_d and L6: spectrum in [c, C]; LOC-BF: c_B), so each raw column has iid nondegenerate Gaussian entries and is nonconstant a.s.; no column is dropped, the retained p equals p_raw a.s., and the allocation depends only on (n, p_raw). A constant centred response is a null event (conditionally on X, Cε has a nondegenerate law 

* **L2_k0.md:168** → `Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md:26-34`
  - context: `L7_delivery.md:26-34`): true (spectrum ⊆ [c, C]). Each raw column has iid nondegenerate Gaussian entries, no column is
  - cited: *Proof.* **Step 1 (Lemma S extends; A2 step 1).** Fixed designs: nonconstant raw columns by G; standardisation gives centred columns of squared norm n − 1. Iid rows: Σ_n is a correlation matrix with λ_min ≥ ψ₀ > 0, so each raw column has iid nondegenerate Gaussian entries and is nonconstant a.s.; the finite union of constant-column events is null; no column is dropped, so the retained p equals p_r

* **L2_k0.md:171** → `Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:26-28`
  - context: * **Step 2** is design-independent (LOC2 `L7_delivery.md:26-28`): P(no output) = 0.
  - cited: **Step 2 (no-output exits; FACA L7 Step 2).** Unchanged and design-independent: the merged cap a_n ≤ ℓ_n + K permits at most ℓ_n + K + 1 LS0 scans, covered by W_G, M_G; Corollary R's guard/preflight/allocation argument applies; with the total fallback schedule_limit is empty; Theorem D's exit walk leaves only null exits: P(no output) = 0.

* **L2_k0.md:175** → `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:65-77`
  - context: scored-set argument of Corollary D′ (`Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:65-77`, as cited at LOC2
  - cited: *Claim.* 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ (for n large enough that S₀ is feasible, |S₀| ≤ K). *Proof.* On a delivered SMC fit, OP-LS0, e4 and the absence of interruption (delivery) imply that LS0 ran to completion from S̃₀ and every model it scored joined the all-scored set (SoP/02_method.tex:490-501); on the exact branch every feasible model is scored. So on 𝒪 ∩ 𝒦_n, S₀ is scored; if moreov

* **L2_k0.md:176** → `Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:32-32`
  - context: `L7_delivery.md:32`), P(output and Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ) → 0 (s₀ ≤ K_n since p ≥ s₀ and n large), and
  - cited: E[1 − π(S₀)] → 0 (L5 (c)). The scored-set argument of Corollary D′ (FACA L7 Step 3; `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:65-77` [R07-15]): on

* **L2_k0.md:178** → `Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:37-39`
  - context: Inherited qualifications (verbatim from LOC2 `L7_delivery.md:37-39`): [OP] "PROVED (by this seat, unchecked)"; e4 rests on
  - cited: Qualifications inherited verbatim from FACA L7: [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only "some maximiser" is used for consistency; delivery keeps e4 with TDP-IMPL as in Proposition F); S.3 is a code-reading audit; the fallback is merged on main (4676af6).

* **L2_k0.md:186** → `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md:183-184`
  - context: CD(a)", `L3_LOC.md:183-184`). Gram floors, TV, A_cov, NA-R (N1), PLR, L1_POST (LSF) and delivery Step 1 use only the lower
  - cited: Var(W_j | W_U) ≥ c, spectrum of conditional covariance matrices ≥ c (Schur complement ≥ λ_min(Σ_n)); the upper spectral bound C was used in L3.2–L3.5 only through CD(a) (all other uses are "Var ≤ 1"). (L3.2) Sets of size O(log n) have

* **L2_k0.md:189** → `Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md:31-31`
  - context: and τ² ≤ 1 (§5), atoms Var e_v ≤ 1 (§7, required by NA-R (R2) `W2-LOC2/lemmas/L2_NAR.md:31`), and the B = 2/c form of RB (optional).
  - cited: * (R2) *Atoms.* A set 𝒜_n of functionals with Var a ≤ 1 (a ∈ 𝒜_n; no cardinality bound beyond the display below), and

* **L2_k0.md:190** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:22-23`
  - context: All hold because UNI-0 assumes Σ_n unit diagonal (`W2-UNI/STATEMENT.md:22-23`, `W2-UNI/STATEMENT.md:103`) [C1-A1]. The general toolkit (`L1_metric.md`)
  - cited: * **Design.** Either (R) *random design*: raw rows iid N(m_n, Σ_n), Σ_n unit-diagonal (WLOG by scale invariance; m_n arbitrary), X = centred, sample-standardised raw design; or (E) *approximate-Gram fixed design*: X centred and

* **L2_k0.md:190** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:103-103`
  - context: All hold because UNI-0 assumes Σ_n unit diagonal (`W2-UNI/STATEMENT.md:22-23`, `W2-UNI/STATEMENT.md:103`) [C1-A1]. The general toolkit (`L1_metric.md`)
  - cited: **(ii) Theorem UNI-0 (reported model, k = 0).** (R), Σ_n ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) (unit diagonal), (A3) with PTV, any

* **L2_k0.md:204** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:28-32`
  - context: implementation premises of `W2-UNI/STATEMENT.md:28-32`. These are named premises, not gaps of this reduction.
  - cited: * **Method and premises.** D0 score, capped BB(1, p) prior, K_n := min(p, ⌊n/2⌋), Ω = {|S| ≤ K_n}, block tables, start γ₀, start mode S̃₀, LS0 cap ℓ_n + |S̃₀|; implementation premises EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans, IND-T and the c₄ search when R′ > 4, "the emitted LS0 centre is some maximiser of γ₀" (named, not proved). Delivery claims use the premises and allocation of FACA

* **L2_k0.md:208** → `Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md:6-7`
  - context: sandwich/NA probes (`W2-LOC2/numerics/d1_diag.py`, `n4_nar_check.py`, cited at LOC2 `L4_LOCd.md:6-7`) cover the
  - cited: Falsification numerics: `numerics/d1_diag.py` (sandwich: S₀ ⊆ start mode in all 74 runs; extras' distances are ℓ∞ grid distances, not the theorem's Euclidean ones [R07-16]; numerics/D1_SUMMARY.md), `numerics/n4_nar_check.py` (frames/atoms decomposition, (R3) ratio ≤ 1.0009).

* **L2_k0.md:220** → `Theory_work/Wave2/W2-LOC2/numerics/D1_SUMMARY.md:44-48`
  - context: for n = 500 → 2000 → 8000), the same finite-n pattern as LOC2's separated-site probe (`W2-LOC2/numerics/D1_SUMMARY.md:44-48`:
  - cited: 3. **Whole-lattice NA vs path**: the estimated lattice supremum (a LOWER estimate of the true lattice sup) exceeds the path maximum by at most 9.19 h-units per run (max at G2A, n = 800, seed 3; recomputed from d1_results.csv) [R07-6]; this observed gap does not bound the true lattice–path gap. The estimated lattice sup falls below c_n′ at the largest n for G2E/G2A(p = 900)/TP; for EBM and G2A(p = 

* **L2_k0.md:230** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:26-34`
  - context: premises of `STATEMENT.md:26-34`, any X-measurable partition with blocks ≤ 16. With (K₂, t₂) of CD_M, d_n :=
  - cited: * **Response.** Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the raw design, σ² > 0 fixed; S₀ := supp θ*; response scaled inside the score (FIN s1). * **Method and premises.** D0 score, capped BB(1, p) prior, K_n := min(p, ⌊n/2⌋), Ω = {|S| ≤ K_n}, block tables, start γ₀, start mode S̃₀, LS0 cap ℓ_n + |S̃₀|; implementation premises EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans, IND-T and the

* **L2_k0.md:238** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:103-110`
  - context: and polynomial growth. This matches `STATEMENT.md:103-110`.
  - cited: **(ii) Theorem UNI-0 (reported model, k = 0).** (R), Σ_n ∈ 𝓛𝓞𝓒(C₀, d₀, c, C, K, a) (unit diagonal), (A3) with PTV, any p ≤ n^A. Relevance set [R01-8]: with the conditional-decay constants (K₂, t₂) of CD_M, let d_n = ⌈(½ log n + log(1 + s₀θ_hiK₂))/t₂⌉ and Q⁰ = {l : min_{j∈S₀} δ(l, j) ≤ d_n}. Set Q = Q⁰ if p ≥ 2|Q⁰| + 32s₀ + 1, and Q = [p] otherwise. Then |Q| = O((log n)^{d₀}); eventually Q = [p] or

* **L2_k0.md:241** → `Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md:17-20`
  - context: separated sites, δ = ‖x_j − x_k‖, N_δ(r) ≤ (2r + 1)^d ≤ 2^d(1 + r)^d (`L3_CTd.md:17-20`), C₀ = 2^d, d₀ = d. Bounded blocks of
  - cited: **Packing fact.** For every i and R > 0, #{j : d_ij < R} ≤ (2R + 1)^d; hence for every integer m ≥ 1, #{j : m ≤ d_ij < m + 1} ≤ (2m + 3)^d. *Proof.* The balls B(x_j, ½) are pairwise disjoint (separation ≥ 1); for d_ij < R they lie in B(x_i, R + ½). Comparing volumes, the count is ≤ ((R + ½)/½)^d = (2R + 1)^d; for the shell take R = m + 1. ∎

* **L2_k0.md:242** → `Theory_work/Wave2/W2-UNI/STATEMENT.md:56-57`
  - context: size ≤ γ̄: δ = 0 within / p between blocks, C₀ = γ̄, d₀ = 1 (`STATEMENT.md:56-57`). In each case the source's spectrum and PTV
  - cited: function enters. Examples: index distance on a line (d₀ = 1); Euclidean distance between separated sites in ℝ^d (d₀ = d); graph distance on a graph of polynomial growth; distance 0 within / p between blocks of size ≤ γ̄ (C₀ = γ̄, d₀ = 1).

* **L4_k1.md:40** → `Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md:11-13`
  - context: envelope θ_lo²n/log n and the TV-pop Lipschitz constant (via ‖θ*‖ ≤ √s₀θ_hi) (FACA `L5_random_instances.md:11-13`, `:28-29`, `:40-41`, `:45-46`);
  - cited: Every probability bound and every threshold n₀ in L1 (Corollary U), L2, L3 and L4 depends on the design X only through the constants (γ̄, ψ₀, κ̄, A, α₁ (from (P)), M, s₀, σ², the BM-∞ envelope θ*²_min n/log n, the TV envelope M_n, the (AG) envelope δ_n) and through n, p. Hence: if 𝒜_n is a set of designs on which these hypotheses hold with common

* **L4_k1.md:40** → `Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md:28-29`
  - context: envelope θ_lo²n/log n and the TV-pop Lipschitz constant (via ‖θ*‖ ≤ √s₀θ_hi) (FACA `L5_random_instances.md:11-13`, `:28-29`, `:40-41`, `:45-46`);
  - cited: **Setting.** Rows of X^r iid N(m, Σ_n), Σ_n ∈ 𝔉(γ̄, ψ₀, κ̄) a correlation matrix; X the standardised design; ε ⊥ X^r; fixed s₀, σ² > 0, fixed nonzero θ*_{S₀}; (P); (TV-pop) with 𝔅_n, 𝓔'_n, τ₀.

* **L4_k1.md:40** → `Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md:40-41`
  - context: envelope θ_lo²n/log n and the TV-pop Lipschitz constant (via ‖θ*‖ ≤ √s₀θ_hi) (FACA `L5_random_instances.md:11-13`, `:28-29`, `:40-41`, `:45-46`);
  - cited: unnormalised ≥ (n − 1)3ψ₀/4 ≥ g₀); energy: ‖μ‖² = (n − 1)θ*_{S₀}ᵀR̂_{S₀S₀}θ*_{S₀} ≤ (n − 1)s₀‖θ*‖² =: Mn-type bound with M := s₀‖θ*‖² (‖R̂_{S₀S₀}‖ ≤ s₀ since its entries are bounded by 1 in absolute value; R08 suggestion 1); BM-∞ since θ* is fixed and nonzero; s₀ ≤ K.

* **L4_k1.md:40** → `Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md:45-46`
  - context: envelope θ_lo²n/log n and the TV-pop Lipschitz constant (via ‖θ*‖ ≤ √s₀θ_hi) (FACA `L5_random_instances.md:11-13`, `:28-29`, `:40-41`, `:45-46`);
  - cited: and f(Σ_V)² = (Σ_{jμ|U})²/Σ_{jj|U} ≥ τ₀ by (TV-pop). On {‖M − Σ_V‖_op ≤ |V|δ'_n ≤ ψ₀/4}, f is Lipschitz with a constant depending only on (ψ₀, |V|, ‖θ*‖) (the same Schur-complement bounds as L1 U(d): regression vector norm

* **L5_delivery.md:33** → `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:65-77`
  - context: `lemmas/L4_delivery.md:65-77`, as used in FACA L7 Step 3). Hence P(output, Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ) → 0 (s₀ ≤ K
  - cited: *Claim.* 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ (for n large enough that S₀ is feasible, |S₀| ≤ K). *Proof.* On a delivered SMC fit, OP-LS0, e4 and the absence of interruption (delivery) imply that LS0 ran to completion from S̃₀ and every model it scored joined the all-scored set (SoP/02_method.tex:490-501); on the exact branch every feasible model is scored. So on 𝒪 ∩ 𝒦_n, S₀ is scored; if moreov


# Quoted status occurrences (for the manual audit: is the status attached to the cited result?)

* STATUS **STATEMENT.md:93** "PROVED (by this seat, unchecked)" → LOC2; context: ire verification of the T03♯ sample-design hypotheses and are not covered by population LSF alone. (i′) Theorem PLR (general reported-model engine; LOC2 L5: "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS, inside W

* STATUS **STATEMENT.md:93** "PROVED-CHECKED" → W2-LOC2; context: lation LSF alone. (i′) Theorem PLR (general reported-model engine; LOC2 L5: "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS, inside W2-LOC2 "PROVED-CHECKED" [C1-B NIT-3]) [R01 optional]. Stated

* STATUS **C_corollaries.md:18** "PROVED-CHECKED" → W2-APP; context: .0 (F3); so PTV(θ_lo c). | # | Source result (status verbatim) | Instance of | Exact assumption check | |---|---|---|---| | 1 | APP Lemma POST (W2-APP REPORT: "PROVED-CHECKED"; lemma "PROVED (by this seat, unchecked

* STATUS **C_corollaries.md:18** "PROVED (by this seat, unchecked)" → W2-APP; context: | # | Source result (status verbatim) | Instance of | Exact assumption check | |---|---|---|---| | 1 | APP Lemma POST (W2-APP REPORT: "PROVED-CHECKED"; lemma "PROVED (by this seat, unchecked)", R02 V-W-A) | UNI-P | identical hypothe

* STATUS **C_corollaries.md:19** "PROVED-CHECKED" → APP; context: cked)", R02 V-W-A) | UNI-P | identical hypotheses (A1-post = LSF of APP L1_POST); exact Gram: POST(c). | | 2 | APP Theorem LOC (exp. decay along an ordering π; "PROVED-CHECKED" inside W2-APP) | UNI-0 | (G-line); LOC

* STATUS **C_corollaries.md:20** "PROVED-CHECKED" → C-GROW; context: ); LOC ⇒ Σ ∈ LOC_M with (K, a) of APP L3_LOC.md:26-27 and spectrum [c, C]; PTV is APP's hypothesis (L3_LOC.md:28). | | 3 | GROW (C5)(c) AR(1), study S2 (C-GROW "PROVED-CHECKED") | UNI-0 | Σ_jk = ρ^{|j−k|}: (G-line),

* STATUS **C_corollaries.md:21** "PROVED-CHECKED" → W1-GEN; context: ariance ≥ a₀ for every j ∈ S₀, \|U\| ≤ 15"); (6.0) holds for the study's S2 layouts (C-GROW STATEMENT.md:146). | | 4 | GEN (C5)(d) study S1, S3, S4, S6 (W1-GEN "PROVED-CHECKED") | UNI-0 | `Scripts/Data_generators/gen

* STATUS **C_corollaries.md:22** "PROVED-CHECKED" → W2-LOC2; context: ep·k, step ∈ {7, 13} ⇒ ≤ 1 truth per group ⇒ PTV(θ_lo c). (GEN's masked-truth theorems — LH, LH-iid, W — are not imported.) | | 5 | LOC2 Theorem LOC-d (W2-LOC2 "PROVED-CHECKED") | UNI-0 | (G-sites), both branches, sp

* STATUS **C_corollaries.md:23** "PROVED-CHECKED" → LOC2; context: PROVED-CHECKED") | UNI-0 | (G-sites), both branches, spectrum [c, C], PTV — LOC2's hypotheses verbatim. | | 6 | LOC2 Theorem LOC-BF (growing one-factor groups; "PROVED-CHECKED") | Theorem PLR (STATEMENT (i′)); not co

* STATUS **C_corollaries.md:24** "PROVED-CHECKED" → LOC2; context: LOC_M; overlapping subclasses (e.g. all b_v = 0, Σ = I) may satisfy UNI-0. Uses LOC2 L4 Part B's latent-factor frames. | | 7 | LOC2 polynomial decay α > 17/2 ("PROVED-CHECKED") | separate extension of the engine | L

* STATUS **C_corollaries.md:25** "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" → FACA; context: ply LOC_M, although the classes overlap (e.g. banded or exponentially decaying members) [R05b-4]. | | 8 | FACA Theorem FAC-L ((L4) fixed design, (L5) iid rows; "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" [R05b-11]) | UNI-1 for its fixed-positi

* STATUS **C_corollaries.md:26** "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" → FACA; context: rics/n3b_out.txt last line: S5 block CS c_𝒢 = 0.4286 = 0.3/0.7, κ = 1.0000); (AG) = (E); (P) identical; (TV)/(TV-pop) identical. | | 9 | Study S5 (FACA (I)(c), "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" inside FAC-A) | UNI-1 | `Scripts/Data_g

* STATUS **C_corollaries.md:27** "PROVED-CHECKED" → FACB; context: four-truth diagnostic layout (FACA `lemmas/L5_random_instances.md:144-146`, §L5.3) [R04-4]. Covered for limsup log p/log n < 1/6. | | 10 | FACB Theorem FAC-CS ("PROVED-CHECKED") | partly UNI-1(E); otherwise partial v

* STATUS **C_corollaries.md:28** "PROVED-CHECKED" → APP; context: ); for 1/6 ≤ … , p ≤ ⌊n/2⌋, and for masked truths under (FS′): FACB only (family-specific partial version of "(iii) for all p ≤ n^A"). | | 11 | APP Lemma ENUM ("PROVED-CHECKED" inside W2-APP) | separate override | ne

* STATUS **L1_metric.md:6** "PROVED (by this seat, unchecked)" → LOC2; context: as amended by `reviews/R01_statement_lock_sol.md:63-77`, required change 4). Model (delta source): LOC2 `lemmas/L3_CTd.md` (CT_d, CD_d, RB, TAIL; status there "PROVED (by this seat, unchecked)", check R02 "VERIFIED-WITH-AMENDMENTS";

* STATUS **L1_metric.md:7** "VERIFIED-WITH-AMENDMENTS" → LOC2; context: .md:63-77`, required change 4). Model (delta source): LOC2 `lemmas/L3_CTd.md` (CT_d, CD_d, RB, TAIL; status there "PROVED (by this seat, unchecked)", check R02 "VERIFIED-WITH-AMENDMENTS"; inside W2-LOC2 "PROVED-CHECKED", `W2-L

* STATUS **L1_metric.md:7** "PROVED-CHECKED" → W2-LOC2; context: a source): LOC2 `lemmas/L3_CTd.md` (CT_d, CD_d, RB, TAIL; status there "PROVED (by this seat, unchecked)", check R02 "VERIFIED-WITH-AMENDMENTS"; inside W2-LOC2 "PROVED-CHECKED", `W2-LOC2/REPORT.md:3`), itself modelle

* STATUS **L2_k0.md:14** "PROVED (by this seat, unchecked)" → LOC2; context: sults asymptotic. Inputs and statuses (verbatim from the sources). LOC2 L1 (L0′, L1.2), L2 (NA-R), L3 (CT_d etc.), L4 (LOC-d), L5 (PLR), L7 (F-LOC2): each "PROVED (by this seat, unchecked)" with checks R02 "VERIFIED-WITH-AMENDMEN

* STATUS **L2_k0.md:14** "VERIFIED-WITH-AMENDMENTS" → LOC2; context: from the sources). LOC2 L1 (L0′, L1.2), L2 (NA-R), L3 (CT_d etc.), L4 (LOC-d), L5 (PLR), L7 (F-LOC2): each "PROVED (by this seat, unchecked)" with checks R02 "VERIFIED-WITH-AMENDMENTS" (L1, L3), R03 "VERIFIED-WITH-AMENDMENTS

* STATUS **L2_k0.md:15** "VERIFIED-WITH-AMENDMENTS" → LOC2; context: L2 (NA-R), L3 (CT_d etc.), L4 (LOC-d), L5 (PLR), L7 (F-LOC2): each "PROVED (by this seat, unchecked)" with checks R02 "VERIFIED-WITH-AMENDMENTS" (L1, L3), R03 "VERIFIED-WITH-AMENDMENTS" (L2), R04 "VERIFIED-WITH-AMENDMENTS" (L

* STATUS **L2_k0.md:15** "VERIFIED-WITH-AMENDMENTS" → LOC2; context: ), L5 (PLR), L7 (F-LOC2): each "PROVED (by this seat, unchecked)" with checks R02 "VERIFIED-WITH-AMENDMENTS" (L1, L3), R03 "VERIFIED-WITH-AMENDMENTS" (L2), R04 "VERIFIED-WITH-AMENDMENTS" (L4, L5) / "VERIFIED" (L7); W2-LOC2 as

* STATUS **L2_k0.md:15** "VERIFIED" → LOC2; context: (by this seat, unchecked)" with checks R02 "VERIFIED-WITH-AMENDMENTS" (L1, L3), R03 "VERIFIED-WITH-AMENDMENTS" (L2), R04 "VERIFIED-WITH-AMENDMENTS" (L4, L5) / "VERIFIED" (L7); W2-LOC2 as a whole "PROVED-CHECKE

* STATUS **L2_k0.md:16** "PROVED-CHECKED" → W2-LOC2; context: cks R02 "VERIFIED-WITH-AMENDMENTS" (L1, L3), R03 "VERIFIED-WITH-AMENDMENTS" (L2), R04 "VERIFIED-WITH-AMENDMENTS" (L4, L5) / "VERIFIED" (L7); W2-LOC2 as a whole "PROVED-CHECKED" (`W2-LOC2/REPORT.md:3`), HQ audit B4 "H

* STATUS **L2_k0.md:17** "PROVED (by this seat, unchecked)" → APP; context: Q audit B4 "HOLDS-WITH-AMENDMENTS" (`Wave2/HQ_AUDIT/B4_loc2_redteam.md:1`; its one MINOR amendment concerns a numerics docstring, not a proof step). APP L3_LOC "PROVED (by this seat, unchecked)", R03 "VERIFIED-WITH-AMENDMENTS"; W2-APP

* STATUS **L2_k0.md:18** "VERIFIED-WITH-AMENDMENTS" → APP; context: e2/HQ_AUDIT/B4_loc2_redteam.md:1`; its one MINOR amendment concerns a numerics docstring, not a proof step). APP L3_LOC "PROVED (by this seat, unchecked)", R03 "VERIFIED-WITH-AMENDMENTS"; W2-APP "PROVED-CHECKED" (`W2-APP/REPOR

* STATUS **L2_k0.md:18** "PROVED-CHECKED" → W2-APP; context: its one MINOR amendment concerns a numerics docstring, not a proof step). APP L3_LOC "PROVED (by this seat, unchecked)", R03 "VERIFIED-WITH-AMENDMENTS"; W2-APP "PROVED-CHECKED" (`W2-APP/REPORT.md:3`). GROW L6 "PROVED

* STATUS **L2_k0.md:18** "PROVED (by this seat, unchecked)" → GROW; context: ring, not a proof step). APP L3_LOC "PROVED (by this seat, unchecked)", R03 "VERIFIED-WITH-AMENDMENTS"; W2-APP "PROVED-CHECKED" (`W2-APP/REPORT.md:3`). GROW L6 "PROVED (by this seat, unchecked)", R07 Sol "VERIFIED", R06 Opus "VERIFIED

* STATUS **L2_k0.md:19** "VERIFIED" → GROW; context: (by this seat, unchecked)", R03 "VERIFIED-WITH-AMENDMENTS"; W2-APP "PROVED-CHECKED" (`W2-APP/REPORT.md:3`). GROW L6 "PROVED (by this seat, unchecked)", R07 Sol "VERIFIED", R06 Opus "VERIFIED-WITH-AMENDMENTS" (A

* STATUS **L2_k0.md:19** "VERIFIED-WITH-AMENDMENTS" → GROW; context: ked)", R03 "VERIFIED-WITH-AMENDMENTS"; W2-APP "PROVED-CHECKED" (`W2-APP/REPORT.md:3`). GROW L6 "PROVED (by this seat, unchecked)", R07 Sol "VERIFIED", R06 Opus "VERIFIED-WITH-AMENDMENTS" (APP `L3_LOC.md:3-5`) [C1-B NIT-6], ins

* STATUS **L2_k0.md:19** "PROVED-CHECKED" → C-GROW; context: T.md:3`). GROW L6 "PROVED (by this seat, unchecked)", R07 Sol "VERIFIED", R06 Opus "VERIFIED-WITH-AMENDMENTS" (APP `L3_LOC.md:3-5`) [C1-B NIT-6], inside C-GROW "PROVED-CHECKED". [OP] "PROVED (by this seat, unchecked)

* STATUS **L2_k0.md:19** "PROVED (by this seat, unchecked)" → C-GROW; context: ED (by this seat, unchecked)", R07 Sol "VERIFIED", R06 Opus "VERIFIED-WITH-AMENDMENTS" (APP `L3_LOC.md:3-5`) [C1-B NIT-6], inside C-GROW "PROVED-CHECKED". [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; T0

* STATUS **L2_k0.md:19** "PROVED-CHECKED" → GEN; context: Opus "VERIFIED-WITH-AMENDMENTS" (APP `L3_LOC.md:3-5`) [C1-B NIT-6], inside C-GROW "PROVED-CHECKED". [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; T03♯ "PROVED; SF VERIFIED (W2-VT03R);

* STATUS **L2_k0.md:20** "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" → GEN; context: ENDMENTS" (APP `L3_LOC.md:3-5`) [C1-B NIT-6], inside C-GROW "PROVED-CHECKED". [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; M5(0)/T38-(0) "PROVED (SF: VERIFIED (W

* STATUS **L2_k0.md:20** "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" → GEN; context: ECKED". [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; APP L1_POST "PROVED (by this seat, unc

* STATUS **L2_k0.md:21** "PROVED (by this seat, unchecked)" → APP; context: ED-CHECKED"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; APP L1_POST "PROVED (by this seat, unchecked)", R02 "VERIFIED-WITH-AMENDMENTS"; FACA L

* STATUS **L2_k0.md:21** "VERIFIED-WITH-AMENDMENTS" → APP; context: W2-VT03R); XF VERIFIED (A-REV2)"; M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; APP L1_POST "PROVED (by this seat, unchecked)", R02 "VERIFIED-WITH-AMENDMENTS"; FACA L7 "PROVED (by this seat, uncheck

* STATUS **L2_k0.md:21** "PROVED (by this seat, unchecked)" → FACA; context: (0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; APP L1_POST "PROVED (by this seat, unchecked)", R02 "VERIFIED-WITH-AMENDMENTS"; FACA L7 "PROVED (by this seat, unchecked)", R04 "VERIFIED-WITH-AMENDMENTS"; e4 res

* STATUS **L2_k0.md:22** "VERIFIED-WITH-AMENDMENTS" → FACA; context: 38E); XF: VERIFIED* (A-REV5))"; APP L1_POST "PROVED (by this seat, unchecked)", R02 "VERIFIED-WITH-AMENDMENTS"; FACA L7 "PROVED (by this seat, unchecked)", R04 "VERIFIED-WITH-AMENDMENTS"; e4 rests on N3 "OPEN" (only "some maxi

* STATUS **L2_k0.md:22** "OPEN" → FACA; context: "PROVED (by this seat, unchecked)", R02 "VERIFIED-WITH-AMENDMENTS"; FACA L7 "PROVED (by this seat, unchecked)", R04 "VERIFIED-WITH-AMENDMENTS"; e4 rests on N3 "OPEN" (only "some maximiser" is used for cons

* STATUS **L2_k0.md:178** "PROVED (by this seat, unchecked)" → LOC2; context: s₀ ≤ K_n since p ≥ s₀ and n large), and with P(no output) = 0, P(Ŝ⁺ = S₀) → 1. Inherited qualifications (verbatim from LOC2 `L7_delivery.md:37-39`): [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only "some max

* STATUS **L2_k0.md:179** "OPEN" → LOC2; context: output) = 0, P(Ŝ⁺ = S₀) → 1. Inherited qualifications (verbatim from LOC2 `L7_delivery.md:37-39`): [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only "some maximiser" is used for cons

* STATUS **L2_k0.md:203** "OPEN" → cited-ticket set; context: ontain indices at distance 0 from l — harmless, they are just in the frame pattern; (g) the enlargement test uses Q⁰ (R01-8). * Inherited, not new: e4/N3 "OPEN" and the code-reading audits (S.3, P1 ex

* STATUS **L3_ULOC.md:10** "PROVED (by this seat, unchecked)" → W2-FAC-A; context: ript was corrected to include T = [p] in the c_𝒢 enumeration and re-run [R03-3]. Generalises W2-FAC-A `lemmas/L1_uniform_add.md` (Lemma U(a)–(c), Corollary U; "PROVED (by this seat, unchecked)", R02 Sol xhigh VERIFIED-WITH-AMENDMENTS

* STATUS **L3_ULOC.md:11** "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" → W2-FAC-A; context: s W2-FAC-A `lemmas/L1_uniform_add.md` (Lemma U(a)–(c), Corollary U; "PROVED (by this seat, unchecked)", R02 Sol xhigh VERIFIED-WITH-AMENDMENTS, inside W2-FAC-A "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)") from block-diagonal Ψ to Ψ ∈ 𝓛𝓞𝓒 (STAT

* STATUS **L4_k1.md:7** "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" → W2-FAC-A; context: t-6.1-sol xhigh, `reviews/R03_L3L6_check_sol.md`): VERIFIED-WITH-AMENDMENTS (items 1, 3, 6), applied (v1.1). Inputs (statuses verbatim). W2-FAC-A (REPORT: "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)"): L2_sandwich (Lemma L2, "PROVED (by th

* STATUS **L4_k1.md:8** "PROVED (by this seat, unchecked)" → W2-FAC-A; context: plied (v1.1). Inputs (statuses verbatim). W2-FAC-A (REPORT: "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)"): L2_sandwich (Lemma L2, "PROVED (by this seat, unchecked)", R03 VERIFIED-WITH-AMENDMENTS), L3_NA_T

* STATUS **L4_k1.md:9** "PROVED (by this seat, unchecked)" → W2-FAC-A; context: ed, flagged target STATEMENT.md v1.2)"): L2_sandwich (Lemma L2, "PROVED (by this seat, unchecked)", R03 VERIFIED-WITH-AMENDMENTS), L3_NA_TL (Lemmas L3.1, L3.2, "PROVED (by this seat, unchecked)", R03 VERIFIED-WITH-AMENDMENTS), L4_asse

* STATUS **L5_delivery.md:4** "PROVED (by this seat, unchecked)" → W2-FAC-A; context: agnostic delivery reduction, R4) Status: PROVED (by this seat, unchecked) — v1, 2026-11-09. Template: W2-FAC-A `lemmas/L7_delivery.md` (Proposition F-FAC, "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS) and W2-L

* STATUS **L5_delivery.md:5** "PROVED (by this seat, unchecked)" → W2-LOC2; context: /L7_delivery.md` (Proposition F-FAC, "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS) and W2-LOC2 `lemmas/L7_delivery.md` (Proposition F-LOC2, "PROVED (by this seat, unchecked)", R04 VERIFIED), both inside "PROVED-CHE

* STATUS **L5_delivery.md:5** "PROVED-CHECKED" → W2-LOC2; context: hecked)", R04 VERIFIED-WITH-AMENDMENTS) and W2-LOC2 `lemmas/L7_delivery.md` (Proposition F-LOC2, "PROVED (by this seat, unchecked)", R04 VERIFIED), both inside "PROVED-CHECKED" tickets; FIN s6 Proposition F / F-GROW.

* STATUS **L5_delivery.md:12** "AUDITED (code reading)" → FIN; context: s6 Proposition F with A1's envelopes and A4's preflight bounds, LS0 score count ≤ 1 + (ℓ_n + K + 1)q(p), evaluated at (n, p_raw). CAL not assumed. P1/S.3 keep "AUDITED (code reading)". Proposition F-UNI. Let a design s

* STATUS **L5_delivery.md:29** "PROVED (by this seat, unchecked)" → C-GROW; context: n, run on the data, scores S₀}. On Sand_n(Q_n) ∩ NA(𝓛_n) ∩ TL(𝓛_n) the exact start mode lies in 𝓛_n (Sand) and, by C-GROW L1.2 (hypotheses S₀ ⊆ Q_n, |Q_n| ≤ K; "PROVED (by this seat, unchecked)", R03 VERIFIED, inside C-GROW "PROVED-CH

* STATUS **L5_delivery.md:30** "PROVED-CHECKED" → C-GROW; context: n) the exact start mode lies in 𝓛_n (Sand) and, by C-GROW L1.2 (hypotheses S₀ ⊆ Q_n, |Q_n| ≤ K; "PROVED (by this seat, unchecked)", R03 VERIFIED, inside C-GROW "PROVED-CHECKED"), LS0 deletes one extra per move and sc

* STATUS **L5_delivery.md:39** "PROVED (by this seat, unchecked)" → FACA; context: from T03♯ under (H0) (fixed design, FACA L4 Note (5)) or UNI-P / FACA L5.1's every-sequence argument (R). Qualifications inherited verbatim from FACA L7: [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only "some max

* STATUS **L5_delivery.md:39** "OPEN" → FACA; context: )) or UNI-P / FACA L5.1's every-sequence argument (R). Qualifications inherited verbatim from FACA L7: [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only "some maximiser" is used for cons

* STATUS **L6_frontier.md:32** "PROVED-CHECKED" → FACB; context: idual loadings, stratification of sets when justified, or a path argument. ## L6.2 Partial versions (family-specific, beyond UNI-1) * FACB Theorem FAC-CS ("PROVED-CHECKED", W2-FAC-B/REPORT.md): exact-Gram compou

* STATUS **L6_frontier.md:35** "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" → FACA; context: − ρ)I, κ = 1: beyond α₀(1) = 1/6 via the path route. A clearly-marked partial version of the target "UNI-1 for every p ≤ n^A". * FACA Proposition SHARP ("PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" inside W2-FAC-A) [R03-6]: for exact CS,

* STATUS **REPORT.md:23** "PROVED-CHECKED" → LOC2; context: , key lemma U-LOC, Proposition F-UNI) and Lemma OBS-k (R5). UNI-P (i) and PLR (i′) are restated from APP L1_POST and LOC2 L5 with their source statuses (inside "PROVED-CHECKED" tickets) and scopes. Council round 1 pa

* STATUS **REPORT.md:84** "PROVED (by this seat, unchecked)" → LOC2; context: | sources' statements | ## 4. Status per clause (statuses verbatim; review files in reviews/) Lemma files L1–L5 and Lemma OBS-k (L6) keep their header status "PROVED (by this seat, unchecked)" (the rest of L6 is a plan; C_corollarie

* STATUS **REPORT.md:97** "PROVED-CHECKED" → cited-ticket set; context: ries | assumption checks (by this seat) | R04 mid-point (2 items fixed); sweeps R05a (5 items), R05b (2 items) fixed; C1 (1 item fixed) | Inputs (verbatim): * "PROVED-CHECKED": W2-LOC2, W2-FAC-B, W2-APP, C-GROW, W1-

* STATUS **REPORT.md:97** "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" → W2-FAC-A; context: ; sweeps R05a (5 items), R05b (2 items) fixed; C1 (1 item fixed) | Inputs (verbatim): * "PROVED-CHECKED": W2-LOC2, W2-FAC-B, W2-APP, C-GROW, W1-GEN. W2-FAC-A: "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)". * APP L1_POST: "PROVED (by this seat,

* STATUS **REPORT.md:99** "PROVED (by this seat, unchecked)" → APP; context: "PROVED-CHECKED": W2-LOC2, W2-FAC-B, W2-APP, C-GROW, W1-GEN. W2-FAC-A: "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)". * APP L1_POST: "PROVED (by this seat, unchecked)" (R02 V-W-A). * LOC2 L5 (PLR): "PROVED (

* STATUS **REPORT.md:100** "PROVED (by this seat, unchecked)" → LOC2; context: FAC-A: "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)". * APP L1_POST: "PROVED (by this seat, unchecked)" (R02 V-W-A). * LOC2 L5 (PLR): "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS. * T03♯:

* STATUS **REPORT.md:101** "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" → LOC2; context: .2)". * APP L1_POST: "PROVED (by this seat, unchecked)" (R02 V-W-A). * LOC2 L5 (PLR): "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS. * T03♯: "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)". * M5(0): "PROVED (SF: VERIFIED (W3-VT3

* STATUS **REPORT.md:102** "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" → LOC2; context: A). * LOC2 L5 (PLR): "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS. * T03♯: "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)". * M5(0): "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))". * Inherited: e4/N3 "OPEN" (only "some

* STATUS **REPORT.md:103** "OPEN" → LOC2; context: DMENTS. * T03♯: "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)". * M5(0): "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))". * Inherited: e4/N3 "OPEN" (only "some maximiser" is used for cons

* STATUS **REPORT.md:104** "AUDITED (code reading)" → FACA; context: 8E); XF: VERIFIED* (A-REV5))". * Inherited: e4/N3 "OPEN" (only "some maximiser" is used for consistency). As recorded in FACA `lemmas/L7_delivery.md`: S.3/P1 "AUDITED (code reading)". ## 5. Review trail * R01 statement
