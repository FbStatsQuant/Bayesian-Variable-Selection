# v1.4 change spec: the Proposers' converged response (Stage 2 of the senior review)

- **Sources:** the Lead proposal (`council/SENIOR_PROPOSAL_LEAD.md`) and the original drafting advisors' replies (`advisors/SENIOR_RESPONSE_FABLE.md`, `advisors/SENIOR_RESPONSE_ASTRA.md`).
- **Judged by:** the Final Council, i.e. the fresh senior judges (`council/SENIOR_FABLE.md`, `council/SENIOR_ASTRA.md`).
- **Status:** this file is the canonical text of every new or changed statement in v1.4; the package files carry it verbatim.

**Notation.**
- T = S0 and s = |T|.
- For a rival S ⊉ T: B := S ∩ Q_n (its **base**), N := S ∖ Q_n, d := |T∖B|, and k := |B∖T| + |N|, the number of added predictors.
- R_n(S) := n·E[(x_Tᵀβ*_T − L(x_Tᵀβ*_T | x_S))²] is n × the population **linear projection error** of the true signal on x_S. The Schur form n·β*_Dᵀ Σ_{DD·S} β*_D holds for any design with finite second moments.
- ϑ(B, N) := 1 − R_n(B ∪ N)/R_n(B) is the **leakage**: the share of the omitted signal that N explains beyond B.
- Coded coefficients are θ, and raw coefficients are β* (manuscript spec convention).

## 1. A-MARGIN-U: population form (the new headline)

**Price.** For the coded prior,
Pr_n(d) := max_{|D|=d} log[π(T∖D)/π(T)] + (d/2)·log(n+1).
For BB(1, p) this is the package's Σ_{k=s−d}^{s−1} price(k). For other priors the deletion refund at T need not bound the refund at T ∪ (S∖T), so the statement keeps the coded price; for any other prior, re-derive it.

**Rival range.** m̄_d := ⌈(2A+1)d⌉ + 1, as in delivered `asm:margin`(b) with s replaced by d. Rivals with more added predictors k > m̄_d need no signal condition: for p ≤ n^A their summed prior-plus-Occam odds are ≤ n^{−γ} for some γ > 0. Writing out this step is part of TS-b step 2.

**Statement.**
- Fix η > 0 and a deterministic **accounting set** Q_n ⊇ T with log|Q_n| = o(log n).
- Q_n is an accounting device, not an object to be found. Any such Q_n may be used. Enlarging it moves rivals from (b) to (a). Leakage outside Q_n need not vanish; it is priced by ā.
- For all large n:
  - **(U1) Deletions.** R_n(T∖D) ≥ 2(1+η)·σ*²·Pr_n(|D|) for every nonempty D ⊆ T. This is κ_n ≥ 1+η, and it is the case B = T∖D, N = ∅ of (U2a).
  - **(U2a) Bases.** R_n(B) ≥ 2(1+η)·σ*²·Pr_n(d) for every B ⊆ Q_n with B ⊉ T and |B∖T| ≤ m̄_d.
  - **(U2b) Outside nulls.** For every such B and every N ⊆ Q_n^c with 1 ≤ |N| = m and |B∖T| + m ≤ m̄_d:
    √(R_n(B ∪ N)/σ*²) ≥ √(2(1+η)·Pr_n(d)) + ā(B, N)·√(2 log C(p−s, m)),
    where ā(B, N) := min{1, √(2(1 − √(1 − ϑ(B, N))))}.

**Reading aids.**
- √ϑ ≤ ā ≤ √(2ϑ) for ϑ ≤ 3/4.
- Within one base, (U2b) for every N is the same as min_N √R_n(B∪N) ≥ … + max_N ā·√(2 log C), since both extremes sit at the maximum-leakage N.

**Special cases** (stated, not separate assumptions):
- (i) Q_n = T is the "no proxies" case. Every null is then priced by its own leakage.
- (ii) If max_{B,N} ϑ(B, N)·log p → 0 outside Q_n, then (U2a) with η implies (U2b) with every η′ < η for large n.
- (iii) ā ≡ 1 is the structure-free fallback (unit-vector bound). The coefficient is 1, not √2.

**Population sufficient conditions, displayed as corollaries.**
- **(C-i) Strong separation.** min R_n(S)/[σ*² log(p∨n)] → ∞ over feasible underfits with |S∖T| ≤ m̄_s implies (U1)–(U2) with Q_n = T.
- **(C-ii) Sparse eigenvalue plus beta-min.** Let φ² be a lower bound on λ_min(Corr(x_V)) over |V| ≤ s + m̄_s, and let β̄_min := min_{j∈T} |β*_j|·sd(x_j)/σ*. Then
  β̄_min ≥ (1+η)·(1 + √m̄_s)·√(2 log(2p√(n+1))/n)/φ
  implies (U1) and (U2) with ā ≡ 1. For an orthogonal design, a sufficient coordinatewise form of (U1) is β*_j²Var(x_j) ≥ 2(1+η)σ*²·log(2p√(n+1))/n for every j ∈ T; exact (U1) requires n·Σ_{j∈D} β*_j²Var(x_j) ≥ 2(1+η)σ*²·Pr_n(|D|) for each nonempty D (the displayed logarithm upper-bounds the average coded refund).

**Lemma W (bridge to the proof; low risk).**
- (W1) For S ⊇ B with positive residuals, ⟨v_S, v_B⟩ = √(R̂(S)/R̂(B)), so ‖v_S − v_B‖ = a(ϑ̂) exactly.
- (W2) On the two-sided sparse-isometry event on T ∪ B ∪ N (size ≤ s + m̄_d, relative error δ_n ≍ √(log(n∨p)/n)), ϑ̂ ≤ ϑ + 2δ_n/(1+δ_n). Because of the cap, ā(ϑ̂) ≤ ā(ϑ) + 2√δ_n.
- (W3) **Simultaneous Gaussian bound.** Let H ≤ 2^s Σ_{b ≤ m̄_s} C(|Q_n|−s, b) = n^{o(1)} be the number of bases and l_n := log(H+1) + t_n, with t_n → ∞ and t_n = o(log n). Conditionally on X, with probability 1 − O(e^{−t_n}), simultaneously over bases and N,
  −⟨v_S, g⟩ ≤ √(2l_n) + ‖v_S − v_B‖·√(2[log C(p−s, m) + l_n]). By the same union bound, simultaneously, −⟨v_S, g⟩ ≤ √(2[log C(p−s, m) + l_n]) directly; take the minimum of the two bounds before applying W2, so the effective chord coefficient is capped at 1 (the uncapped chord a(ϑ̂) exceeds 1 when ϑ̂ > 3/4).
  The surplus over ā·√(2 log C) is o_P(√log n), and the root-scale slack absorbs it because Pr_n(d) ≳ log n for d ≥ 1.
- **Consequence.** The population form implies the **base-indexed** conditional-width condition. TS-b step 3 is then run per base. For fixed D, each null set gives exactly one S, so the containing-model odds are summed once at the total null size k, with no multiplier of order H.
- **Not claimed.** The population form does not imply the v1.3 class-level conditional-width condition when Q_n ≠ T: across bases, the smallest residual and the largest width can occur at different bases. That condition is kept as a **parallel sufficient condition** (the "refined design-conditional form", ASSUMPTIONS §3.3). E9/E9b are diagnostics of it.

**Remark (weaker variant, not adopted).** Proxies inside Q_n could pay their own price. (U2a) could be weakened to:
- the single-rival price [log π(B)/π(T) + ((s−|B|)/2)log(n+1)]₊ for |B| < s;
- R_n(B)/(σ*²(1+log|Q_n|)) → ∞ for |B| = s;
- no condition for |B| > s.

This needs step 2 on the bases T ∪ (B∖T), which is not written. The headline (U2a) is therefore conservative: by a factor (1+ρ²)/(1−ρ²) on the signal when both AR(1) neighbours of an isolated true predictor are proxies, and similarly for block designs.

**Evidence** (moved out of the statement):
- On S1, over all 1,023 deletions D with B = (T∖D) plus at most two of the five tested proxies (the five nulls nearest S0), the minimum of R_n(B)/(2σ²Pr_n(d)) equals the exact κ_n; larger proxy sets were not tested. The value is 2.504–2.770 at SNR 2 and 0.626–0.692 at SNR 1; the binding D retain x_10, which screens every null (`.rc_tmp/lead_v14/u2a_check.py`).
- For the endpoint deletion (retained true predictors on one side), a single outside null at distance k beyond the deleted endpoint, with the intervening nulls not in the base, leaks ρ^{2k}(1−ρ²)/(1−ρ^{2k+2}) (0.265, 0.087, 0.030, 0.011 at ρ = 0.6 for k = 1–4). Special case (ii) needs the uniform bound max ϑ·log p → 0, which L_n → ∞ alone does not give: with Q_n = T plus the L_n nearest nulls, the worst outside leakage over d ≤ 3, up to 2 inside proxies and up to 3 outside nulls is ≈ 0.25ρ^{2L_n} (unit coefficients; `.rc_tmp/lead_v14/leak_uniform.py`), so choosing L_n with ρ^{2L_n}·log p → 0 (L_n of order log log p plus a slowly diverging term, keeping log|Q_n| = o(log n)) puts the S1 sequence in special case (ii).
- The fallback alone (ā ≡ 1): on the evaluated classes (d ≤ 3, selected D for d ≥ 2; m ≤ 2 at p = 500, m = 1 at p = 5,000) at η = 0, it fails at SNR 2 (minimum surplus −0.692 at d = 1, m = 1; −2.008 at m = 2) and holds at SNR 3 (minimum 1.412, d = 1, m = 2); m up to m̄_d is not evaluated (population computation on `tables/e9b_width_ext_s1.tsv` with the combinatorial width √(2 log C(p−s, m))).

## 2. Other changed statements
- **A-MARGIN-H (TS-a), diverging ratio.** For the predictor j and **every fixed k**, inf{R_n(S) : j ∉ S, |S| ≤ k}/(σ*² log n) → ∞. This gives screening at every fixed level M. A diverging ratio at an unspecified speed gives nothing uniform for M = M_n → ∞.
  - Remark (fixed-level form): at a fixed level M, inf R_n(S)/(σ*² log n) ≥ C_L·M over S with j ∉ S and |S| ≤ min(K, J(M)), with C_L above the inverse Hellinger-conversion constant, suffices. It is sharper for finite-ratio signals and gives the a.s. corollary at a large fixed level.
  - TS-a is stated first per predictor (any j satisfying its own margin, whatever the other signals do) and then jointly.
- **A-SUBG / A-NEC windows.** They are imposed on sets of size ≤ k_n, a deterministic design order with k_n ≥ q_n(M) at the claimed level.
  - For fixed-level statements it suffices, across all fixed levels, to impose them on sets of size ≤ c·log n for every fixed c; a single fixed level needs only one such window.
  - For M = M_n → ∞ (the delivered `thm:dist` range M ≤ √n/log n) it is q_n(M_n).
  - For TD′ it is the enlarged q_n.
  - The constants L and c_ψ are common.
- **A-NEC statement.** φ_min(k) := min_{1≤|V|≤k} λ_min(Corr(x_V)), and n·φ_min(k_n) ≥ c_ψ: the sparse eigenvalue may vanish, but no faster than the ridge scale τ/n (τ = 1 as coded). Excluding exact duplicates alone does not ensure it; for example, two predictors with correlation 1 − n^{−2} fail it.
- **A-DIM′.** log p = o(√n) is the conjecture's regime. The product form (s+1)M log p·log(p∨n) ≤ c·n is its proof budget. TD′ stays a high-risk conjecture.
- **A-BS′ (recorded, not adopted).** The recorded pair is V := Var(xᵀβ*)/σ*² = O(1) and E := Σ_j β*_j² Var(x_j)/(nσ*²) = o(1); at fixed s it is equivalent to the stated BS′. The open target is V = O(1) alone, i.e. population R² = V/(1+V) ≤ 1 − c. With A-NEC on T it gives E ≤ M_μ/c_ψ = O(1). Open: whether the size lemma and the ridge remainder hold at O(1) rather than o(1) energy.
- **A-MIS(iii), primitive form.** For the omitted true predictors O, x_Oᵀβ*_O = a + x_Cᵀγ + e with e ~ N(0, τ²) independent of x_C, τ² ≥ 0. Then β^C = β*_C + γ and σ_C² = σ*² + τ². This is equivalent to v1.3's statement (Cramér decomposition). Uniqueness comes from a sparse representation together with A-NEC; full rank is a sufficient version.
- **A-SPARSE-C (new label).** |supp β^C| ≤ s_C, fixed. It holds under Markov-type separation: in a Gaussian AR(1) (a Markov chain), the nearest retained candidates on each side separate an omitted predictor from all other candidates, so it projects on at most two of them. Local covariance dependence alone need not give a sparse regression. It can fail under pervasive factors, where the projection is typically dense (common factors alone do not force a dense projection). The relaxation is TD-A.
- **TM-a / TM-b** are corollaries of TD and TS-b, **conditional on each admissible C**, with the candidate dimension in the cap, price, window and prior. An unconditional statement needs common constants and a common validity threshold over admissible candidate sets, and then adds + P(C inadmissible), which vanishes identically under almost-sure admissibility. The a.s. corollary needs summable exception probabilities.
- **TM-a0-inc (new target, the SL Cor 2 counterpart).** Π(S ⊇ S0^C | data) → 1 a.s. under A-MOM's second moments only. Full rank and finitely many underfits give a positive risk gap. The score moments enter only for exclusion (TM-a0 exact).
- **Converse (TS-b).**
  - It is stated under its minimal set: A-GL, sparse isometry and A-NEC on T, and A-BS for the ridge term.
  - A price-scale restriction Pr_n(1) = O(log n) holds under A-DIM.
  - Boundary remainder: log odds = Pr_n(1) − (√λ̂ + Z)²/2 + O_P(1) at λ = O(log n), with V_n/n = 1 + O_P(n^{−1/2}) and λ̂ − λ = o_P(1) by fixed-support relative transfer.
  - The O_P(1) remainder suffices for P(the specified single-deletion rival beats T) → Φ(−c), hence liminf P(π(T|y) ≤ ½) ≥ Φ(−c), because the leading fluctuation is √(2Pr_n)·(c+Z). The local expansion requires Pr_n(1) = O(log n) and fixed-support relative error O_P(n^{−1/2}), supplied for instance by A-DIM and relative A-SUBG on T.
- **Sieve.** Classes satisfy s − d + k ≤ min(K, J) and k ≤ p − s.
- **Credit constant.** C = 1 by convention, with the multiplier in the tight remainder. "C ≍ (s0+1)² ≈ 121" is withdrawn; E9b's C = 121 column is a sensitivity setting. The single-rival price Pr_n(d, m) and the summed class bound B_Dm are distinct.

## 3. Map and defence additions
- **SL (3), p. 950:** lim Σ_j |β*_j| < ∞, with standardised predictors and fixed σ*, implies A-BS. It is A-BS's direct counterpart.
- **SL p. 951 cap remark (Jiang 2007 (38)):** the BB(1, p) size tail gives an effective prior-tail cutoff of the same order as SL's proposed sieve r̄_n ≍ M log n/log 2. q_n must still pay the true-model denominator, and it does not inherit SL's entropy conditions.
- **SL Condition 3, Gaussian sufficient form (pp. 955–956):** ch₁{var(x)} ≻ ε_n² is the precedent for vanishing floors. A-NEC at 1/n does not supply SL's screening separation, which is A-MARGIN-H's job.
- **Delivered alternatives in the SL-1/2/3 rows:**
  - `prop:dist(ii)`: no eigenfloor, SUBG on singletons only, slower radius;
  - `thm:dist-param`: a delivered rate analogue under detectable signals and a fixed floor on its own window.

  Neither recovers SL's growing-p second-moment theorem.
- **Four blocks:**
  - Model: A-GL, A-SPARSE, A-DIM, A-BS.
  - Design: A-SUBG, A-NEC.
  - Signal: A-MARGIN-H for screening, A-MARGIN-U for exact selection.
  - Omitted variables: A-MIS(iii) with A-SPARSE-C; A-MOM for the fixed-dimension result.
- **Worked cases (DOSSIER).** Each gives the conditioning set and coefficients. Leakage depends on both for multi-deletions. Checked numerically in `.rc_tmp/lead_v14/worked_cases.py`.
  - **Orthogonal:** R_n(T∖D) = nΣ_{j∈D} β*_j²Var(x_j), and leakage is 0.
  - **AR(1) ρ:** deleting an interior predictor whose neighbours are retained gives Var = (1−ρ²)/(1+ρ²) per unit β², and leakage 0 (screened). Deleting an endpoint (retained true predictors on one side) gives 1−ρ²; a single outside null at distance k beyond the endpoint, intervening nulls not in the base, leaks ρ^{2k}(1−ρ²)/(1−ρ^{2k+2}).
  - **Block, fixed size b, equicorrelation within blocks:** only same-block nulls leak, and Q_n = the blocks of T has |Q_n| ≤ s·b.
  - **Equicorrelation ρ, one omitted predictor, b retained, m nulls:** leakage mρ²/[(1+bρ)(1+(b+m−1)ρ)], which is ρ²/(1+bρ)² at m = 1 and tends to ρ/(1+bρ). Every null leaks equally, so no small Q_n makes outside leakage vanish; Q_n = T is admissible even with positive leakage, and the interpolated (U2b) is the operative form. The formula describes the equal-loading one-factor case.
- **No S1/S2 number in any statement.** D4 is rewritten: the form is chosen on generality grounds, and S1 is checked against it.

## 4. Engine decision (HQ, SMC-PERF closed, memo 1b319090)
- v3.1.1, g = n, truncated BB(1, p) and MPM are **confirmed**.
- Fix E (output-only) and C1 (compute-only) do not touch the theorems.
- Proof writing and Lean stay on hold.

## 5. What a referee will still raise (recorded in the DOSSIER weak points)
1. TS-b is a target, not a theorem. Still to be written: the truncated superset sum, the coded mixed odds per base, the size lemma under A-BS, and the k > m̄_d step. Polynomial p and fixed s remain, against SL Cor 1.
2. There is no necessity result for (U2b). Constant 2 is sharp only for deletions, and the common-base bound is conservative when many null sets leak in nearly the same direction.
3. The high-dimensional TM tier assumes a Gaussian-linear candidate law. Only TM-a0/TM-a0-inc tolerate a wrong response law.
4. TD′ must pay an O(M log p) testing budget on a sieve with a much larger entropy, so it stays a high-risk conjecture.
