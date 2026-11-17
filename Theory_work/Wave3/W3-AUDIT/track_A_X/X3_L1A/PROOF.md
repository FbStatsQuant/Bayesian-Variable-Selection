# X3 · Re-check of `W3-POST:Lemma-1a'` — PROOF v1 (line check)

L1a′ = `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md`; [P1] = `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`;
[T03R] = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`. Notation of L1a′ and [P1] §1:
U is the n × (n − 1) contrast basis (UᵀU = I, UUᵀ = C = I − 11ᵀ/n), y_c = Uᵀy^r, X_c = UᵀX, ε_c = Uᵀε ~ N_{n−1}(0, σ*²I).

## Step 1 — the changed step (bound on Q^c_T), `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:27-32`
- [P1] `lem:slab` with A = X_{c,T}, Y = y_c gives Q^c_T = min_ϑ {‖y_c − X_{c,T}ϑ‖² + ϑᵀ(G_T + I)ϑ/n}, G_T = X_{c,T}ᵀX_{c,T}
  (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:68-72`). Checked.
- G_T = X_TᵀUUᵀX_T = X_TᵀCX_T = X_TᵀX_T since the standardised columns are centred. Checked.
- y_c = Uᵀ(α1 + X^rβ + ε) = UᵀX^rβ + ε_c (Uᵀ1 = 0) = UᵀCX^rβ + ε_c (UᵀC = Uᵀ) = Uᵀμ + ε_c with μ = CX^rβ. And
  X_{c,T}θ = UᵀX_Tθ = Uᵀμ. So ϑ = θ gives ‖y_c − X_{c,T}θ‖² = ‖ε_c‖² and θᵀ(G_T + I)θ/n = (‖X_Tθ‖² + ‖θ‖²)/n =
  (‖μ‖² + ‖θ‖²)/n ≤ M + M′. Hence Q^c_T ≤ σ*²E′ + ρ with ρ ≤ M + M′, deterministically, E′ := ‖ε_c‖²/σ*² ~ χ²_{n−1}.
  Checked; t = 0 (μ = 0, Q^c_∅ = ‖ε_c‖², ρ = 0) also checked.

## Step 2 — the rest of den′ with R_n → ρ, `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:34-37`
[P1] `lem:den`'s integral representation and exponent bound (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:340-353`)
use Q^c_{S₀} only through Q^c_{S₀} ≤ σ*²E′ + R_n with R_n ≥ 0: for v = σ*²u, 1 ≤ u ≤ 1 + n^{−1/2},
−((n−1)/2)log u + E′/2 − Q/(2σ*²u) ≥ (u − 1)/2·(E′/u − (n − 1)) − R/(2σ*²) ≥ −|E′ − (n − 1)|/(2√n) − E′/(2n) − R/(2σ*²).
I re-derived both inequalities (log u ≤ u − 1; 1/u ≥ 2 − u; 0 ≤ u − 1 ≤ n^{−1/2}); they hold with R replaced by any
deterministic ρ ≥ 0. Restricting to v ∈ [σ*², σ*²(1 + n^{−1/2})] ⊆ [σ*², 2σ*²], where IG(v; 0.51, b₊) ≥ c_IG, gives
m^c_{b₊}(T)/f₀(y_c) ≥ D_T^{−1/2}c_IGσ*²n^{−1/2}e^{−Λ′_n}, and D_T ≤ (n + 1)^t by `lem:spec`(e) (1 ≤ D ≤ (n + 1)^k, no
condition; `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:97`). f₀ is the true density of y_c
(`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:344-345`). E Λ′_n: E|E′ − (n − 1)| ≤ √(2(n − 1)) ≤ √(2n)
(`lem:chi`(b), d = n − 1 ≥ 2), E E′ = n − 1, ρ deterministic, so E Λ′_n ≤ 1/√2 + (n − 1)/(2n) + (M + M′)/(2σ*²) ≤ C′_Λ.
Checked.

## Step 3 — assembly, `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:39-42` (cf. [T03R] T02(i♯))
- [P1] `thm:Ta` on 𝓑_n: π(E) ≤ κ²I_{b₋}(E)/Z^c_{b₊} (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:255-264`).
  Its second inequality, written for S₀, holds for any T ∈ Ω because Z^c_{b₊} is a sum over Ω of nonnegative terms
  ϖ(S)m^c_{b₊}(S) and contains the term of T. Checked.
- v_m := ϖ(E_m) with E_m = {|S| > m}: ϖ(E_m) = Σ_{k>m} q_k/W_K and ϖ(T) = w(t)/W_K, q_k = C(p, k)w(k)
  (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:128`), so v_m = R^T_mϖ(T) with
  R^T_m = Σ_{k=max(m+1,0)}^K q_k/w(t), as defined in L1a′ and in [T03R] for S₀
  (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md:16-17`). Checked.
- N_m := I_{b₋}(E_m)/f₀(y_c); `lem:num` with the data-free rate b₋ gives E N_m = v_m
  (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:317-323`); Θ^{(1)}_{n,m} := N_m/v_m ≥ 0, E Θ^{(1)} = 1. Checked.
- On 𝓑_n: π(E_m) ≤ κ²v_mΘ^{(1)}/(ϖ(T)m^c_{b₊}(T)/f₀) ≤ κ²R^T_mΘ^{(1)}(n + 1)^{t/2}√n e^{Λ′_n}/(c_IGσ*²)
  = R^T_m(n + 1)^{t/2}√n·c♯e^{Λ′_n}Θ^{(1)}, c♯ = κ²/(c_IGσ*²); so Θ^T_{n,m} ≤ c♯e^{Λ′_n}Θ^{(1)}_{n,m}. Checked.
- For L > c♯²: {c♯e^{Λ′}Θ^{(1)} > L} ⊆ {Θ^{(1)} > √L} ∪ {Λ′ > log(√L/c♯)}; Markov for the nonnegative Θ^{(1)} (mean 1)
  and Λ′ (mean ≤ C′_Λ); P(𝓑_nᶜ) ≤ (8 + 24M/σ*²)/(n − 1) by `thm:T01iii`, which uses only ‖μ‖² ≤ nM
  (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:234-240`). The bound is free of m. Checked.
- At m = m^T_n(ω) (exists: R^T_K = 0 and K ≥ t since T ∈ Ω), R^T_m ≤ n^{−(t+1)/2}e^{−ω}, so
  π(|S| > m) ≤ n^{−(t+1)/2}e^{−ω}(n + 1)^{t/2}√nΘ^T = (1 + 1/n)^{t/2}e^{−ω}Θ^T. Checked. ∎

## Verdict and precisions
**VERIFIED.** Precisions (no change to the claim): (i) the uniformity "over all designs" holds because every constant
— κ, b±, c_IG, c♯, C′_Λ — depends on (σ*², M, M′) only (b₊ = b₀(2(σ*² + M) + 1), [T03R] constants
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md:76`); (ii) the conclusion at m = m^T_n(ω)
uses Θ^T at that (data-free) m, so `sup_m` covers it, as in [T03R].
