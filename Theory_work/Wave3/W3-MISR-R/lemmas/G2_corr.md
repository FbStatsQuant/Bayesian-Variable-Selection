# G2 — Corollary G(b)⁺ (W3-MISR-R:CorGb-plus): copy of BASE G.2 with changed lines marked [R-#]

Status (verbatim source for the registry):
- CorGb-plus: **PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, SOP:TH09, SOP:TH128, C-MIS:GDb**
(Same conditions as W3-MISR:Cor-G(b)@1.0.0 minus C-MIS:Prop-P: the Gaussian-conditioning step is replaced by CorG-min
(`G1_min.md`), proved here. C-MIS:GDb = C-MIS:GD(b) (steps (1)–(2) of its proof are cited); MIS-R (ii) brings W3-POST2:C,
E, A1, SOP:TH09, SOP:TH128; A0 is the bridge (F_w) ⇒ (OS).)

Source copied: BASE `Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md:36-65` (G.2, line-checked K2, registry
W3-MISR:Cor-G(b)@1.0.0 "PROVED-CHECKED, …"). [L2] = `Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md`; [A] =
`Theory_work/Wave3/W3-POST2/lemmas/A_occam.md`; [P3] as in BASE. Statement: `../STATEMENT.md` §3 (v1.2).

**[R-1] Reduction to unit variances.** Λ := D_Σ^{−1/2} (deterministic, positive diagonal). Replace X^r_𝒞 by X̌ := X^r_𝒞Λ and
(β_𝒞, γ) by (Λ⁻¹β_𝒞, Λ⁻¹γ); keep a, τ², σ², X^r_𝓜, β_𝓜, α, ε. Then y^r = α1 + X̌(Λ⁻¹β_𝒞) + X^r_𝓜β_𝓜 + ε, the rows of X̌ are iid
N(Λm_𝒞, R), and (OV) holds for X̌ with (a, Λ⁻¹γ, τ²) (X̌Λ⁻¹γ = Xγ; σ(X̌) = σ(X)). The coded target is unchanged: the
standardised design is C X̌ D_{X̌}⁻¹ with D_{X̌} = D_xΛ (sample SDs scale with the column), i.e. CxΛΛ⁻¹D_x⁻¹ = CxD_x⁻¹ = X, and
π_𝒞 depends on x only through X and p ([W3P] `STATEMENT.md:18-25`). The configuration κ̌_n = (X̌, Λ⁻¹β^𝒞, σ²_𝒞) has the same
θ = D_{X̌}Λ⁻¹β^𝒞 = D_xβ^𝒞, μ, S₀ and v as κ_n = (X, β^𝒞, σ²_𝒞), hence the same class memberships and the same δ_n, HPM.
Support, β̌ᵀRβ̌ = β^𝒞ᵀΣ_𝒞𝒞β^𝒞 and ρ_n^{BM} (Ř_jj = 1, β̌_j² = Σ_jj(β^𝒞_j)²) are unchanged. **So assume Σ_jj = 1 for all j,
Σ_𝒞𝒞 = R**; then the hypotheses read: λ_min(Σ_TT) ≥ c_R for |T| ≤ k_n, max_j Σ_jj = 1.

Hypotheses as in the statement. Put φ₀² := c_R/8 [R-1: = c_pop/(8C₀) with (c_pop, C₀) = (c_R, 1)], M := 2M₀ + 1, g₀ := 1, and
(n_OS, C_OS) := those of [A] Lemma A0 for (s, A, c_D = ½) ([A] lines 14-15, 25-27: (F_w; 1) ⇒ (DG; ½) ⇒ (ADG; ½) ⇒ (OS; C_OS) for
n ≥ n_OS). **[R-3]** Let L := liminf_n ρ_n^{BM} ∈ (16c₀/c_R, ∞]; fix c := c₀(s, A) + 1 if L = ∞ and c := (c₀(s, A) + c_RL/16)/2 if
L < ∞; in both cases c > c₀(s, A). Follow [L2] lines 88-105 (proof of Lemma GD(b)); W := UᵀX^r_𝒞 has iid N(0, Σ_𝒞𝒞) rows
([L2] lines 88-90: X^r_𝒞 = 1m_𝒞ᵀ + ZΣ_𝒞𝒞^{1/2}, which needs only Σ_𝒞𝒞 ⪰ 0 [R-2]).
1. *SDs* ([L2] lines 91-93; no variance of the response involved): with probability ≥ 1 − 2n^{−2}, ½ ≤ σ̂_j² ≤ 2 for all
   j ∈ 𝒞, for n ≥ n₀(A).
2. *Sparse eigenvalues* ([L2] lines 94-100; design only; it uses λ_min(Σ_TT) only for |T| ≤ k_n, never a global floor
   [R-2]). Raw event: with probability ≥ 1 − 2k_n n^{−2}, for n ≥ n₀, λ_min(W_TᵀW_T) ≥ c_RN/2 for every non-empty T ⊆ 𝒞 with
   |T| ≤ min(p, k_n). On the intersection with the event of step 1 (σ̂_j² ≤ 2), standardisation gives
   λ_min(R̂_T) = λ_min(G_T)/N ≥ (c_R/2)/2 = c_R/4 ≥ φ₀² and λ_min(G_T) ≥ Nφ₀² ≥ 1 for all such T (the last for
   n ≥ 1 + 1/φ₀²). This gives (F₀; φ₀), (F_λ; φ₀) (S₀ ∪ J with |J| ≤ j₀ has size ≤ k_n) and (F_w; 1) (S₀ ∪ J with
   |J| ≤ m♯_n), hence (OS; C_OS) for n ≥ n_OS.
3. *Energy, in signal-to-noise form*: Wβ^𝒞 ~ N_N(0, (β^𝒞ᵀΣ_𝒞𝒞β^𝒞)I_N) and β^𝒞ᵀΣ_𝒞𝒞β^𝒞 = β^𝒞_SᵀΣ_SSβ^𝒞_S ≥ c_R‖β^𝒞_S‖² > 0 for
   S := supp β^𝒞 (|S| = s ≤ k_n, β^𝒞 ≠ 0) **[R-2]**, so ‖Wβ^𝒞‖²/(β^𝒞ᵀΣ_𝒞𝒞β^𝒞) ~ χ²_N ≤ 2N with probability ≥ 1 − 1/n for
   n ≥ n₀ ([P3] `lem:chi`(a), as there). On that event ‖μ(κ_n)‖² = ‖Wβ^𝒞‖² ≤ 2NM₀σ²_𝒞 ≤ nMσ²_𝒞: (E^σ; M).
4. *Relative beta-min* **[R-3]**: on the event of step 1, θ_j(κ_n)² = σ̂_j²(β^𝒞_j)² ≥ ½(β^𝒞_j)² = ½Σ_jj(β^𝒞_j)², so
   min_j θ_j(κ_n)²·nφ₀²/(σ²_𝒞 log n) ≥ ½φ₀²ρ_n^{BM} = (c_R/16)ρ_n^{BM}. If L = ∞ then ρ_n^{BM} → ∞; if L < ∞ then c < c_RL/16
   and, by the definition of liminf, (c_R/16)ρ_n^{BM} > c for all large n. In both cases there is n_BM (depending on the
   sequence) with (c_R/16)ρ_n^{BM} ≥ c for n ≥ n_BM: (BM^σ; c).
5. *Sizes*: 2 ≤ p ≤ n^A by hypothesis; s ≤ K = min(p, ⌊n/2⌋) for n ≥ 2s (p ≥ s); s(κ_n) = s (β^𝒞 deterministic).
Let 𝒜_n ∈ σ(X^r_𝒞) be the intersection of the SD event of step 1, the raw eigenvalue event of step 2 and the energy
event of step 3. For n ≥ n* (the largest threshold above, n_OS, n_BM and the n₀ of MIS-R (i) for 𝒦^λ_n included),
𝒜_n ⊆ {κ_n ∈ 𝒦^λ_n(s, A, M, φ₀, C_OS, c)} and P(𝒜_nᶜ) ≤ 2n^{−2} + 2k_n n^{−2} + n^{−1} = (2 + 2k_n)n^{−2} + n^{−1}, with
k_n = O(log n) ([L2] lines 96-97, 105). **[R-4]** By CorG-min (a) (`G1_min.md` G1.1; here γ, τ² are constants, so
β^𝒞, σ²_𝒞 are deterministic), (GR^c | σ(X^r_𝒞)) holds for κ_n = (X^r_𝒞, β^𝒞, σ²_𝒞). **[R-5]** MIS-R (ii)(a) on 𝒦^λ_n
(c > c₀(s, A); BASE `STATEMENT.md:151-154`) gives, for n ≥ n*,
  E δ_n ≤ C r_n + P(𝒜_nᶜ) ≤ C r_n + (2 + 2k_n)n^{−2} + n^{−1},  P(HPM ≠ supp β^𝒞) ≤ 2C r_n + (2 + 2k_n)n^{−2} + n^{−1},
with C the constant of MIS-R (i) on 𝒦^λ_n(s, A, M, φ₀, C_OS, c) (S₀(κ_n) = supp β^𝒞). Both are O(r_n) since
k_n n^{−2} = O(log n/n²) and n^{−1} = o(r_n). ∎
(Compared with BASE G.2: no joint Gaussianity of candidate and omitted rows (only (OV)); the floor is on the correlation
matrix and only on |T| ≤ k_n; no variance bound C₀; the beta-min may hold at a fixed level above 16c₀/c_R; the explicit
finite-n bound is displayed.)
**Implication BASE Cor-G(b) (STATEMENT §8).** Under BASE's hypotheses (jointly Gaussian rows, Σ_𝒞𝒞 ≻ 0, λ_min(Σ_TT) ≥ c_pop,
Σ_jj ≤ C₀, ρ_n^{BM} → ∞): (E1) gives (N) + (OV) with constant (a, γ, τ²); λ_min(R_TT) = λ_min(D_T^{−1/2}Σ_TTD_T^{−1/2}) ≥
λ_min(Σ_TT)/max_{j∈T}Σ_jj ≥ c_pop/C₀ =: c_R; L = ∞. So CorGb-plus applies and gives E δ_n = O(r_n),
P(HPM ≠ supp β^𝒞) = O(r_n), BASE's conclusion.
