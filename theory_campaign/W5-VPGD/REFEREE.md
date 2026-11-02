# W5-VPGD — line-by-line referee of W3-PGD `PROOF.md` (Theorem W and its lemmas)

Source refereed: `origin/theory/W3-PGD:theory_campaign/W3-PGD/PROOF.md` (448 lines). Notation is that file's,
which follows 00_COMMON and W1-T37R. Verdicts: **VERIFIED** (every step re-derived here), **GAP** (a step is
missing or under-justified; repair in `REPAIRS.md`), **ERROR** (a step is false). A verdict here is a single
same-family referee pass. It is not an adoption.

Summary: **no ERROR in any proof step.** Four GAPs, all minor or presentational (G1–G4 below), and one
interpretive claim (the "factor 3–4" comparison of (★) with C-LD) that is misleading; see `STAR.md`.

---------------------------------------------------------------------------------------------------------

## §0 Setting

- Contrast coordinates, Y = μ + e, e ~ N(0, σ²I_N), N = n − 1, ‖x_j‖² = N. Consistent with 00_COMMON §1 and T01.
- 𝒯 := {T ⊆ S₀ ∪ J : J ⊆ S₀ᶜ, |J| ≤ d+1}. Every comparison set of the proofs lies in 𝒯: a state of R_{a,d}(𝒟)
  is ⊆ S₀ ∪ P with |P| ≤ d, and a neighbour adds at most one column. **VERIFIED.**
- c_k ≥ c_* for k ≤ s₀+d requires 2p − 1 − k ≥ p, i.e. k ≤ p − 1. True since k ≤ K ≤ p. Also c_k > 0 for all
  k < K (used tacitly in Lemma G: 2p−1−k ≥ k+1). **VERIFIED.**

## §1 Population side

| Step | Verdict | Note |
|---|---|---|
| Lemma 1.1(a) | VERIFIED | rank-one projection update. |
| Lemma 1.1(b) | VERIFIED | both telescopes re-derived: through S−i, and through S+x with a_i(S−i+x) = ‖r_{S−i+x}‖² − ‖r_{S+x}‖². |
| Lemma 1.1(c) | VERIFIED | nested: range(P_B − P_A) ⊆ col X_B ⟂ r_B. |
| Lemma 1.2 | VERIFIED | needs M ∩ S = ∅ (true) so that ‖X_Mv − X_Sw‖² = ‖X_{S∪M}(v,−w)‖² ≥ λ_min‖v‖². ‖θ_M‖₁² ≤ m‖θ_M‖². Used with λ_min(G_{S∪S₀}) ≥ Nφ₀² from SE_λ(d) (S ∪ S₀ = S₀ ∪ P). |
| Lemma 1.3 | VERIFIED | r_S ∈ span X̃_M; Cauchy–Schwarz on the projection coefficients. |
| Prop P1 | VERIFIED | The five non-progress types (N1)–(N5) exhaust the non-progress moves (add null; delete truth; swap truth→null; swap extra→null; swap truth→truth). (N3): S−u ∈ 𝓡⁺ because m(S−u) = m+1 ≤ min(a+1, s₀); both branches of the bracket sign re-checked. (N4): the progress swap e→j* is size-preserving hence always feasible. Adding a missing truth is feasible because |S| ≤ s₀+d−1 < K. GERC is quantified over **all** nulls (also those outside 𝒟), as needed. |
| Remark (a) tightness | VERIFIED | extra fact used: ρ⁺(S) = max_{j∈M} a_j(S) exactly (an add of j dominates every swap e→j, since S−e+j ⊆ S+j; deleting an extra has red ≤ 0). So "GERC ⟺ add-null part of PGD for every θ" is exact. |
| Remark (b) coherence | VERIFIED | ‖Ĝ⁻¹‖_{1→1} ≤ 1/(1−(m−1)ν). |
| Remark (c) Exp 3 | VERIFIED | ERC(∅,3) = √2·0.85 = 1.202. |
| Prop P2 (iff) | VERIFIED | additivity ‖r_S‖² = Σ_{g out} D_g(S∩N_g) re-derived; every move class re-derived (12 sub-cases); necessity states have m = 1 so a ≥ 1 suffices. (B1) quantifies l over all of N_g∖P (also mates outside 𝒟), which is what PGD needs. Also checked numerically by brute force (`scripts/check_P2_bruteforce.py`). |
| Cor P2′ | VERIFIED | R²(j|P) = kρ²/(1+(k−1)ρ) and pcorr(j,l|P) = ρ/(1+kρ) re-derived (partial covariance ρ(1−ρ)/(1+(k−1)ρ), partial variances (1−ρ)(1+kρ)/(1+(k−1)ρ)). Worst (B1) case k = 0; (B2) holds with η = 1; worst (B3) case P = ∅, |Q| = min(d, b_h−1). κ_h(d) < 1 ⟺ ρ_h < 1. Numbers re-computed in `results/eta_block.txt`. |
| Prop P3(a),(b) | VERIFIED | (a): S−u+j misses only u, so a_u(S−u+j) = θ_u²‖(I−P_{S−u+j})x_u‖² ≥ Nφ₀²θ_u² (SE on S+j = S₀∪P). |
| Prop P4 | VERIFIED | g ≥ ερ⁺; ‖r_{S′} − r_{S″}‖² ≤ (2 + 4s₀/(εφ₀²))g; Lemma G with L_n = log n. Interpretation "only the boundary is open" is fair (see the remark on vanishing η in REPAIRS R0). |
| Lemma P5(i)–(iii) | VERIFIED | (ii): both directions re-derived; 2(s₀+ε) ≤ 4s₀ uses ε ≤ φ₀²/2 ≤ ½. (iii): ρ̂⁰ ≤ (1−η)ρ̂⁺ + 4NLε‖θ‖² and ρ̂⁺ ≥ Nφ₀⁴θ²_min/4 give the stated ε bound exactly. |
| Lemma P5, LD♭ stability sentence | **GAP (G3)**, minor | Only asserted. True, with O(ε/φ₀⁸) (not O(ε/φ₀⁴)); written out in REPAIRS R3. |
| Cor P6 | VERIFIED **given** the cited concentration bound, with **GAP (G2)** | The composition "realised design satisfies the hypotheses w.p. → 1 ⇒ Theorem W's conclusion jointly" needs Theorem W's o(1) to be uniform over designs with the same constants. It is (every threshold in Lemmas R, G, U, S depends only on s₀, d, A, φ₀, η, M, σ, M_n and the counts), but this is not said. REPAIRS R2. The cited max-entry bound (Bickel–Levina 2008, Lemma A.3) is for covariances; the passage to correlations is standard but was not re-derived here either. |

## §2 Noise side

| Step | Verdict | Note |
|---|---|---|
| Lemma Q(i)–(iii) | VERIFIED | Laurent–Massart; 2Φ̄(x) ≤ e^{−x²/2} holds for all x ≥ 0. |
| Lemma R | VERIFIED | Q_T(y) = Q_T(Y)/s_y² (homogeneous quadratic form); ε¹_T ∈ [0, |T|/(2Nφ₀²)]; ξ_T formula re-derived from the eigen-decomposition; ν/N ≤ 1 for n ≥ 3. E₀: (p+1)^{d+1} subspaces of dim ≤ k̄; the proof gives RSS_T ≥ Nσ²(1−δ_n) for **every** T ∈ 𝒯 (the statement only claims it for T ⊇ S₀; harmless). C₀ = 5 + 4M/σ² is a valid (loose) constant. |
| Lemma G | VERIFIED | RSS decomposition; P_B − P_C projection of rank ≤ 2; N₁ Gaussian with variance 4σ²‖r_B − r_A‖²; log(1+x) ≥ ½min(x,1); ν ≥ N/2; |pen(|B|) − pen(|A|)| ≤ 2c̄_n because ||A|−|B|| ≤ 2 and c_k > 0. |
| Lemma U | VERIFIED | μ ∈ col X_A so the RSS difference is pure noise; −log(1−x) ≤ x/(1−x); ν/N ≤ ½(1+2/n) for n ≥ 3. |
| Chain rule | VERIFIED | Gram–Schmidt. |

## §3 Superset states

| Step | Verdict | Note |
|---|---|---|
| Definition LD♭, (★) | definitions | The illustrative "ρ* ≈ 0.14/A for d = 2" is fine at A = 1: the exact root of (★) there is ρ* = 0.149 (`results/star_thresholds.txt`). For large A the root is ≈ 0.177/A (first order: 2√2ρ* < 1/(2A)). |
| Lemma LD | VERIFIED | I − P_{A∪F} = (I − P_A) − P_Ṽ; |⟨P_Ṽx̌_l, P_Ṽe⟩| ≤ ρ‖x̌_l‖‖P_Ṽe‖. |
| Lemma S, list of comparators | VERIFIED | At S = S₀ ∪ P the non-progress neighbours are exactly S, S+l, S−e′+l, S−u, S−u+l (no missing truth, so no truth→truth swap). (T)+(α)+(β)+(γ) ⇒ D_S, and (T)+(L′) ⇒ (L): re-derived. |
| Lemma S (T) | VERIFIED | g ≥ θ_u²λ_min(G_{S∪l}) ≥ Nφ₀²θ²_min needs SE_λ(d+1). C₁ = 1 because r_S = 0. |
| Lemma S (L′) | VERIFIED | |
| Lemma S (α),(β),(γ) under (H1)/(H2) | VERIFIED | counts (D+1)^d, (D+1)^d p, (D+1)^{d−1}p; the three exponents re-derived. **G1 (presentational):** (H1) is the special case d = 1 of (H2) ((D+1)⁰ = 1). |
| Lemma S under (H3) | VERIFIED | f(ρ) = (a + ρb)/√(1−ρ²) is increasing on [0,1) for a, b ≥ 0, so ρ ≤ ρ* may be used; counts p2^{B′} and (2p+1)^d re-checked; ½Z² ≤ τ²λ + o(log n) uniformly. The constant is **not sharp**; see `STAR.md` for a proved sharpening (★′) and a new lower-bound family. |
| Remark "why d = 1 needs nothing" | VERIFIED | |

## §4 Main theorem

| Step | Verdict | Note |
|---|---|---|
| Lemma A′ | VERIFIED | strictness of D_S makes every top move a progress move; R_{a,d}(𝒟) is progress-closed (add truth, delete extra, swap extra→truth keep U ⊆ S₀, P ⊆ 𝒟, m ≤ a); Φ_max = a + d; Lemma 0(c) (W3-VT37R: VERIFIED). |
| Theorem W, m ≥ 1 part | VERIFIED | S′(S) deterministic; |A∖B|, |B∖A| ≤ 2; g ≥ ηρ⁺ ≥ ηNφ₀⁴θ²_min; ‖r_A − r_B‖² ≤ (2 + 4s₀/(ηφ₀²))g; count 2^{s₀}(D+1)^d(1 + (s₀+d+1)(p+1)); BM-∞ gives γ_n/L_n → ∞. |
| Theorem W, m = 0 part and (L) | VERIFIED | Lemma S. |
| Theorem W, consequence for data-dependent S_c | VERIFIED | TD′_P is one event uniform in the centre. "Up to exact ties" is inherited from W1-T37R Lemma 0(c) / Prop 1 and is not re-proved here. |
| Cor W′(i),(ii) | VERIFIED | (ii) needs SE_λ(d+1), which under BO with equicorrelated groups holds with φ₀² = min_g(1 − ρ_g). |
| Cor W′, random designs under (H3) | **GAP (G2/G3)** | relies on the LD♭ stability sentence (REPAIRS R3) and on uniformity (R2). |

## §5 Counterexample C-LD

| Step | Verdict | Note |
|---|---|---|
| Design and hypotheses | VERIFIED | p = N − 1 ≤ n; λ_min = 1 − r; PGD(1) since every null is ⟂ x₁ (ρ⁰ = 0); ρ(l,{e₁,e₂}|S₀) = r√(2/(1+r)). |
| Probability argument | VERIFIED | Mills bound Φ̄(u) ≥ φ(u)/(2u) for u ≥ 1; mΦ̄(u_m) ≥ e^{ω_m}/(4√π); min(t_a², t_b²) ≥ (1+r)·2 log m − O(√(log m)ω_m); lower direction of Lemma R with RSS_{S−a} ≤ ‖e‖². Conclusion F(S) − F(S−a) ≥ (r − ½)log n − o(log n). |
| Script `ld_counterexample.py` | consistent, weak | the failure frequency at r = 0.55 is 0.02–0.035 up to n = 2·10⁵: the o(log n) terms dominate at every feasible n. The script illustrates the direction (r = 0.9: 0.28 → 0.68), not the threshold. |
| Interpretation "with p ≍ n^A the same computation needs r > 1/(2A)" | **GAP (G4)** | p > n cannot be realised with the exact orthonormal construction; this is a PROOF SKETCH (it needs a random-design version), not part of the counterexample. |
| "(★) is off by a factor ≈ 3–4 from C-LD's 1/(2A)" | misleading | C-LD is not the extremal family, and (★) uses |T| ≤ d where (α),(γ) only need |T| ≤ d − 1. See `STAR.md`: (★′) is proved; a grouped family fails at r > 1/3 (A = 1) where C-LD needs r > 1/2. |

## §6 Summary claims

- "PGD is the sharp population condition up to the boundary": VERIFIED (Theorem W + Prop P4).
- "LD is needed only at supersets and only for d ≥ 2 with unrestricted extras": VERIFIED (Lemma S + C-LD).
- "|𝒟| ≤ s₀(B−1) ≤ 15s₀ for the truth blocks of the start partition": VERIFIED as arithmetic; note that the start
  partition is X-measurable, which Theorem W allows (fixed design).
