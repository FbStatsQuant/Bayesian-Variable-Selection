L1 line check — lemmas/X.md sha256 4c3a657742455bef

Independent cross-family review of v0.3. Line numbers below refer to `lemmas/X.md` unless a source is named. The hash was checked again after reading the proof and sources.

## Findings

No CRITICAL, MAJOR, MINOR or NIT findings in the proof of Lemma X (§0–§7) or Lemma X′ (§9). No amendment is required for either stated conclusion.

This verdict concerns the statements in STATEMENT.md §3, lines 322–335. In particular, Lemma X explicitly uses `d_t = s₀ + ⌈C′t/log n⌉`; it does not require removal of the ceiling. Lemma X′ explicitly uses `ℓ_n = log(p_raw ∨ n)` in its mean threshold.

## Scope and limits

Read the supplied brief and only the permitted source files: X.md, STATEMENT.md, API_CARDS.md, [P1] PROOF_v3.tex, and W3-POST2/lemmas/B_tail_approx.md. No other reviews, alternative proofs, logs, checkpoints, dependency files or work files were consulted. No agents were started and no git command was run. Only this report was written.

The proof was checked algebraically, including its constants and its uses of inherited results. The external books/articles named in F1 were not opened, so their bibliographic section/page attribution is not independently certified. The needed Gamma and chi-square inequalities are nevertheless verified from the displayed moment-generating-function bounds, without relying on that attribution. Sections 8 and 10 are excluded from the proof verdict, as instructed. No numerical counterexample search is claimed.

## §0 and setup: constants and uniformity

Lines 21–56 check.

- Evaluating the ridge criterion at θ* gives `L_{S₀} ≤ ρ′ = (‖μ‖² + ‖θ*‖²)/n ≤ B`. When s₀ = 0, both μ and θ* vanish and ρ′ = 0. Replacing c_D by min(c_D,1) weakens (ND) and retains the allowed dependence of constants.
- F1 follows by Chernoff from the stated Gamma log-MGF inequalities. F2 is exactly the usable bound in [P1] `lem:chi`(a). F3 is the elementary Gaussian Chernoff bound. F4 follows by diagonalizing a symmetric matrix with eigenvalues strictly below one and integrating independent standard normals.
- All constants displayed in lines 32–35 are finite and depend only on the permitted tuple. In particular `K_s = Σ(1+i)^s 2^{-i}` is finite for fixed s. They dominate the corresponding quantities for every integer s₀ ≤ s.
- On the stated range, t ≥ 16, log n ≤ t, and `(A+1)s₀ log n ≤ t`. Also `n/(n−1) ≤ 3/2`, giving the stated upper bound on t/N.
- The cutoff bound used later can be obtained explicitly. Since `log(n+1) ≤ 2 log n`,

  `m_n(t)+s₀ ≤ 2s₀+1 + [s₀ log 2 + (s₀(A+1)+2)log n + 3t]/log 2 ≤ C_m t`.

  Here t ≥ 1 and log n ≤ t justify the last step. Capping m at K only improves it.
- Each of ε₁, ε₂ and ε₃ tends to zero at t = n^{1−κ₀}; the largest additional term is of order `n^{-κ₀} log n`. The denominator defining ε₃ is positive under (c). All t-dependent restrictions become easier when t decreases. Conditions (d) and (g) are t-independent and hold for all sufficiently large n. Conditions (e) and (f) also hold eventually. Thus the “for every n ≥ n₀” definition gives a finite, single n₀ with the required parameter dependence.
- Since log n ≥ 8, `32/log n ≤ 3/log 2`. Monotonicity of the ceiling and the nonnegative other terms in m_n(t) imply `min(d_t,K) ≤ m_n(t)`. This covers d_t > K as well.
- S₀ ∈ Ω is an explicit hypothesis of Lemma X, inherited by X′; it is not being inferred from an unstated lower bound on n. The common setting also explains its eventual validity from fixed s₀^r.

## §1: VERIFIED

Lines 60–73 check, including singular designs and the empty model.

Completing the square gives the displayed M_T^(c). Its nonzero spectral values are `g/[g+c(g+1)/n]`, strictly below one. The two Young inequalities apply to the positive definite penalty matrix; evaluating the shifted coefficient θ*+φ′ gives respectively `Q_{S₀} ≤ Q_{S₀}^{(2)}(e)+2ρ′` and `Q_S ≥ Q_S^{(1/2)}(e)−ρ′`.

Zero-padding preserves the penalty quadratic form because the smaller Gram matrix is a principal block. Thus Q_T^(c) is nonincreasing in T and nondecreasing in c. Consequently `0 ⪯ D′_J ⪯ M_S^(1/2) ≺ I`. Both summands in D′_J vanish on the orthogonal complement of col X_{c,S}; hence its rank is at most rank X_{c,S}, and therefore at most s₀+j. No eigenvalue floor is used.

## §2: VERIFIED

Lines 77–92 check.

- N1 has failure probability at most 2e^{-t} by the two chi-square tails.
- For N2, the threshold comparison reduces to `2 log 2+4 ≤ 6 log n`, valid already for n ≥ 3. The union sum is bounded by `e^{-t}Σ_{k≥1}e^{-k} < e^{-t}`. The result applies to sets outside Ω as long as they are within the stated size range.
- For N3, `(I−M_S)^2 ⪯ I−M_S` gives the claimed variance bound. Summing `2e^{-(k(log p+1)+t+1)}` over at most p^k sets yields `2e^{-t}/(e−1) ≤ 2e^{-t}`. A zero variance cross term satisfies the bound deterministically. Including S = ∅ is necessary and sufficient for the subsequent scale control.
- For E2, N3 at ∅ initially gives `2|μ_cᵀe| ≤ 2σ‖μ‖√(2(t+1)) ≤ 4σ‖μ‖√t`, since t ≥ 1. The two displayed Young bounds then prove the lower and upper bounds on s_y² using (b) and `‖μ‖²/N ≤ 1.5M`. In particular 𝓔_t is contained in the exact inherited event 𝓑_n, and `2b = .02s_y² ≤ .04(M+σ²) = b̄`.
- For E3, μ_c lies in the span of S₀∪J, even if that union is outside Ω. The projector bound applies with at most m_n(t)+s₀ columns. The cutoff estimate above and log n ≥ 1 give the stated ε₂. Since `2ν = n+.02`, the bound on ν/Q_S has exactly the stated ε₃.
- For E4, `|S|log n ≤ (s₀+1)log n+32t ≤ (s+33)t`. Hence the projection and x_k bounds hold with C_P and C_x. For S = ∅ the projection bound holds directly, without needing N2 at size zero.

The total failure bound 5e^{-t} is valid without independence between the noise-event components.

## §3: VERIFIED

Lines 96–129 check.

1. **Pointwise bound (99–100).** Q_{S₀} ≥ Q_{S_J} > 0 on 𝓔_t. Adding the same positive 2b reduces their ratio. The inequalities `log(1+u) ≤ u`, E3, and §1 give the displayed BF bound. The data dependence of b causes no problem in this pointwise comparison.
2. **Moment (102–105).** Direct algebra gives

   `λ[1+1/(8A+2)] = 1−1/(8A+4) < 1`.

   Diagonalizing D′_J gives the exact determinant formula. Its eigenvalues are in [0,1), and there are at most s₀+j nonzero ones, so each nontrivial factor is at most `(1−λ₁)^{-1/2}`. The deterministic signal factor is at most `exp(3B/(2σ²))`, because λ₁ ≤ 1. This proves line 105 for the expectation with indicator 1_{𝓔_t}; it does not condition a Gaussian law on 𝓔_t.
3. **ND and summation (108–114).** With `a_J=(D_{S₀}/D_{S_J})^{1/2}`, concavity gives `Σa_J^λ ≤ binom(p−s₀,j)[mean(a_J)]^λ`. This is precisely the asserted use of (ND). [P1] `lem:prior`(e), raised to λ, and `binom(p−s₀,j) ≤ p^j ≤ n^{Aj}` give line 109; discarding `2^{-λj}` and enlarging `(j+1)^{λs₀}` is valid. Since c_D ≤ 1 and n+1 ≥ n, the determinant factor is bounded above by `c_D^{-j/2}n^{-λj/2}`. Finally,

   `A(1−λ)−λ/2 = −1/4`.

   Thus q is valid. Condition (d) gives `e^{s₀}q ≤ n^{-1/8} ≤ 1/2`. Writing j=j₁+1+i, using `(j₁+2+i)^{s₀} ≤ (j₁+2)^{s₀}(1+i)^s`, and then `j₁+2 ≤ e^{j₁+1}`, proves line 114. The final factor is at most e^{-4t} because j₁+1 ≥ 32t/log n. Extending this numerical geometric majorant beyond the admissible j range does not assume (ND) beyond that range.
4. **Union device (116–124).** For a nonsuperset, `j=|S\S₀| ≥ |S|−s₀ > j₁` and j ≤ min(m_n(t),p−s₀). The prior-ratio bound uses at most s₀ successive ratios, each at most 2p. For increasing eigenvalue order, interlacing gives `λ_i(G_{S′}) ≤ λ_i(G_S)` for i≤|S|. Multiplying f of these eigenvalues and bounding each remaining factor by n+1 proves `D_{S′}/D_S ≤ (n+1)^{|S′|−|S|}`. The likelihood factor is at most one by monotonicity of Q. For each fixed J there are at most `2^{s₀}−1` nonsupersets, plus the one possible superset. Formal weights ℓ on sets outside Ω are legitimate here: the normalization lower bound uses only ℓ(S₀), with S₀∈Ω. The bound `A_n ≤ 2·4^{s₀}n^{(A+1)s₀} ≤ 2·4^{s₀}e^t` follows from n+1 ≤ n². No posterior mass is assigned outside Ω.
5. **Markov (126–127).** Applying Markov to `1_{𝓔_t}(A_nV)^λ` gives exactly `e^{λt}A_n^λ E[1_{𝓔_t}V^λ]`. Subadditivity at power λ bounds the last expectation by the sum of the quantities in line 105. The constants multiply to at most C₅ and the exponential factors to e^{-2t}. Since t≥log C₅, the asserted e^{-t} probability follows. No independence assumption is used.

## §4: VERIFIED

Lines 133–140 check, including the denominator replacement flagged for review.

- If m=K the size tail is identically zero; F₁ may be taken to be the whole sample space in this case. Otherwise the displayed uncapped formula for m is exact.
- The normalization W_K cancels from R_m. The ratio of q terms is at most 1/2 for k≥1; q₁≤1/3 for p≥2. Therefore `Σ_{k>m}q_k ≤ 2q_{m+1} ≤ 2^{-m}` for m≥0 (with zero terms beyond p). Also `1/w(s₀)=2 binom(2p−1,s₀) ≤ 2(2p)^{s₀}`. Substituting the cutoff gives the stronger intermediate bound

  `R_m√D_{S₀}√n ≤ 2^{1−s₀}√n/(n+1) · e^{-3t} ≤ 2n^{-1/2}e^{-3t}`.

- The numerator uses fixed b₋ and a set of models deterministic conditional on the fixed design. [P1] `lem:num` therefore gives its expectation exactly. Markov gives P(F₁ᶜ)≤e^{-t}.
- The minimum representation evaluated at θ* gives `Q_{S₀} ≤ σ²E′+ρ′`. In [P1] lines 340–357, restrict v to `[σ²,σ²(1+n^{-1/2})]`. For u=v/σ², the exponent is bounded below by

  `−|E′−N|/(2√n) − E′/(2n) − ρ′/(2σ²)`.

  This uses only ρ′≥0, `log u≤u−1`, and `1/u≥2−u`. Integration contributes exactly `c_IG σ²n^{-1/2}`, and D_{S₀}^{-1/2} is retained. Thus line 138 is correct. The spectral-floor part and mean bound of the original `lem:den` are not imported. The independently read B_tail_approx.md Steps 2–3 agree with this calculation at zero residual.
- The endpoints b₋, b₊, κ and 𝓑_n are those in [P1] line 58. E2 establishes the required event, and S₀∈Ω licenses the last inequality of `thm:Ta`. Its numerator is the prior-weighted integral at b₋, matching N_m after division by f₀.
- On N1, `|E′−N|/(2√n) ≤ √t+t/√n`. Also E′/(2n)≤1, using ε₁≤1/2 from (b). For t≥16 and n≥16, `√t+t/√n ≤ t/2`. The resulting factors are `e^t e^{t/2} e^{-3t}=e^{-1.5t}`. Condition (g) removes exactly the remaining factor `2c♯e^{1+B/(2σ²)}n^{-1/2}`.

All constants used here depend only on the permitted parameters; c_IG and c♯ depend on σ² and M, with no hidden spectral-floor constant.

## §5: VERIFIED

Lines 144–151 check.

The cross-term and projection bounds give the stated lower bound on Q_S. After subtracting Q_{S₀}, the signal-cost subtraction is actually B/(σ²t) inside the bracket; replacing it by B/σ² is valid because t≥1. For λ_S≥Λ, the cross term consumes at most λ_S/2 and C_P and B/σ² each consume at most λ_S/8. Therefore Δ≥Λσ²t/4.

Condition (e) bounds `2b+Q_{S₀} ≤ 2Nσ²`. Hence `Δ/(2b+Q_{S₀}) ≥ Λt/(8N)`. The inequality `log(1+u) ≥ (log 2)min(u,1)`, ν≥n/2, and n/N≥1 give line 149. The second term is the minimum because t≤8n/Λ, and Λ≥48/log 2 makes it at least 3t.

The prior sum is `Σ_{S∈Ω}w(|S|)=W_K≤1`. The determinant and prior factors are at most `2(2p)^{s₀}(n+1)^{s₀/2} ≤ 2^{s₀+1}e^t`. Finally t≥(s₀+1)log 2 follows from M₀≥max{16,(A+1)s}, A≥1, including s₀=0. The far-model mass bound follows with the stated constants.

## §6: VERIFIED

Lines 155–164 check.

- The centre bound follows from the two squared norms and the inequality `‖a+b‖²≤2‖a‖²+2‖b‖²`.
- The scale expansion yields `|Q_S−‖e‖²|≤σ²C_Qt`. Using N=n−1 and N1 gives the numerator bound in line 158; `t≤√(nt)` follows from t≤n. The constant b̄/σ²+5+C_Q includes both the n versus N correction and the noise fluctuation.
- Under the posterior, β_S/v has shape ν, so its doubled mean is n+.02, not N. F1 gives the displayed deviation `0.02+2√((n+.02)t)+2t ≤ 6√(nt)` on this range. With h=√(t/n), condition (f) gives C_vh≤1. Since C_v=2(C_β+6)≥22, it also gives 6h≤1/2. Dividing `(1+a)/(1+g)` then yields `|v/σ²−1|≤2(C_β+6)h` and v≤2σ².
- The conditional fitted-coefficient covariance is exactly vM_S by [P1] `thm:T01i`. Its eigenvalues divided by v lie in [0,1), so the squared norm is dominated by χ²_rank(M_S). F2 applies also at rank zero; `2|S|log 2+4t ≤ (2C_d+4)t` follows from E4 and log n≥1.
- Combining the variance event and the conditional Gaussian event costs at most 3e^{-t}, by integration over v and a union bound. The squared mean-error bound is exactly dominated by the displayed `4(2C_d+4+C_P+Λ)σ²t`. Taking C to dominate C_v proves line 164 simultaneously for all good S.

## §7: VERIFIED

Lines 168–172 prove exactly Lemma X in STATEMENT.md lines 322–325, with C′=32 and c=1/2.

The relation min(d_t,K)≤m_n(t) ensures that the four model classes cover Ω, including when d_t≥K. On 𝓔_t∩F₁∩F₂ the bad posterior mass is at most `e^{-1.5t}+5e^{-t}≤6e^{-t}≤e^{-t/2}`. For the sampling failure event, the valid union bound is

`P(𝓔_tᶜ)+P(F₁ᶜ)+P(𝓔_t∩F₂ᶜ) ≤ 7e^{-t} ≤ 2e^{-t/2}`.

Thus only the intersection probability supplied by §3 is needed; an unconditional bound on P(F₂ᶜ) is not being assumed. The constants absorb the numerical prefactors since t≥16. Uniformity means the same constants and n₀ work for every admissible t; the statement does not demand a single noise event holding simultaneously for all real t.

## §9: VERIFIED

Lines 191–215 prove exactly Lemma X′ in STATEMENT.md lines 333–335.

- Only 𝓔_t and F₁ are retained. Their construction and the conclusions used from §2 and §4 require no (ND). The final paragraph supplies M₀′ and n₀′ independently of c_D; these are the constants used for X′ in place of §0's M₀ and n₀.
- The cutoff bound m≤C_mt and N2 give C_P′. The displayed C_x′ bounds x_{|S|} since p≤n^A and log n≥1. Thus the far-model calculation is valid with t′=t log n, and `Λ′t log n≤8n` supplies the needed upper-range restriction. Keeping only e^{-3t} from the stronger e^{-3t′} suppression is legitimate.
- The good-model centre and Q_S bounds are the same deterministic calculations at scale t′. The variance calculation retains noise level t. Its additional term obeys

  `t′/n = √(t/n)·[√(t/n)log n] ≤ √(t/n)`

  by the explicitly imposed restriction. Condition (f′) supplies both a valid denominator in the variance ratio and v≤2σ². The conditional coefficient tail stays at level t and uses `|S|≤C_mt`; no missing log n appears in its probability.
- The displayed C₁′ and C_v′ dominate respectively the mean and variance bounds. Since `log(p_raw∨n)≥log n`, the established mean threshold C₁′σ²t log n is no larger than the stated Cσ²tℓ_n. This is the correct event inclusion for the desired upper bound, regardless of retained versus raw dimension.
- The posterior bad mass is at most `e^{-1.5t}+4e^{-t}≤e^{-t/2}` for t≥16; sampling failure is at most `6e^{-t}≤2e^{-t/2}`. M₀′≥max{16,(A+1)s} pays the prior factor exactly as before.
- Every requirement defining n₀′ holds eventually: in particular `n^{-κ₀}log n→0` and `n^{-κ₀/2}log n→0`. They hold throughout the t range once imposed at its upper endpoint. No condition involving c_D, λ, ε₃ or §3 is needed.

## Citation audit

All [P1] labels used in the proof exist and supply the claimed content:

| Citation | [P1] lines | Hypotheses and use checked |
|---|---:|---|
| `thm:T01i` | 173–208 | Exact posterior transformation and the two conditional laws; valid standardized input, almost surely under Gaussian noise. |
| `lem:slab` | 68–80 | Integral and minimum representation for arbitrary matrices, including singular and empty designs. |
| `lem:spec`(b),(d),(e) | 90–110 | Projector domination, monotonicity and determinant factors. The preliminaries apply to arbitrary matrices, so use outside Ω is allowed. The upper determinant ratio in §3 is independently derived by interlacing, not misquoted as the lower-ratio assertion of part (e). |
| `lem:prior`(b),(c),(e) | 113–136 | Successive weight ratios, the uncapped q-tail bound in the proof of (c), and the superset combinatorial bound. Indices are within 0,…,p and p≥2. |
| `lem:chi`(a) | 139–148 | Chi-square upper tail with rank≤d, including rank zero at the positive thresholds used. |
| `lem:num` | 317–321 | Expectation identity with a data-free rate and fixed-design model set. |
| proof of `lem:den` | 340–357 | Integral lower bound after replacing the nonnegative remainder by ρ′. Neither the spectral-floor hypothesis used to construct R_n nor the subsequent mean estimate is imported. |
| `thm:Ta` | 255–264 | Deterministic mixed-endpoint transfer on 𝓑_n, with S₀∈Ω for the denominator simplification. |

The additional B_tail_approx.md citation is correct at lines 23–35 of that file; it is used only for the same zero-residual denominator calculation checked directly above.

## Adversarial and boundary checks

No counterexample to Lemma X was found. The following potential failure mechanisms were checked analytically:

- **Null truth (s₀=0):** θ*=μ=ρ′=0, D_{S₀}=1, the nonsuperset class is empty, and the overcount A_n=2 is harmless. All sums, moments and constants remain defined. B need not be zero for the displayed upper bounds to hold.
- **p=2, or p=s₀:** The q₁ bound is valid at its p=2 endpoint. Empty ranges of admissible additions give V=0. If p=s₀, (ND) is vacuous but all models already satisfy the size cutoff; the mean and variance arguments still apply.
- **Singular true blocks and cancellation by large coefficients:** The argument uses the variational cost ρ′ rather than inversion of G_{S₀}. Under (E) and (C), that cost is bounded even in a singular block. No hidden identifiability or beta-min requirement is introduced.
- **Duplicates and exceptional degenerate additions:** (ND) is an average condition. The proof never replaces it by a pointwise determinant lower bound: Jensen controls exactly the required fractional-power average. Exact duplication of all added directions would violate fixed-c_D (ND) for large n; a smaller exceptional collection is accounted for by the same average. For s₀=0, the fractional power λ<1 preserves a determinant penalty rather than losing it to the full exponential moment.
- **Nonsupersets whose union exceeds K:** ℓ(S∪S₀) is a positive formal weight on all subsets, and the required matrix bounds are valid there. Neither S∪S₀∈Ω nor a rank/eigenvalue floor is assumed.
- **Largest t and near-cap cutoffs:** The n^{-κ₀}log n and n^{-κ₀/2}log n terms are explicitly controlled. If m=K, the tail above m is zero. If d_t≥K, all posterior models are eligible for the small-model analysis.

These checks, together with the verified inequalities, leave no identified design/truth mechanism satisfying all three interfaces that invalidates the conclusion. This is an algebraic verification, not a claim of exhaustive numerical enumeration.

## Section verdicts

| Section | Verdict |
|---|---|
| §1 | VERIFIED |
| §2 | VERIFIED |
| §3 | VERIFIED |
| §4 | VERIFIED |
| §5 | VERIFIED |
| §6 | VERIFIED |
| §7 | VERIFIED |
| §9 | VERIFIED |

Findings summary: none at any severity.

Overall verdict — Lemma X: VERIFIED; Lemma X′: VERIFIED.
