BR1 break review — lemmas/X.md sha256 4c3a657742455bef ; STATEMENT.md sha256 7c8fcb7754175acd

No CRITICAL or MAJOR finding. I found three MINOR omissions in the assembly sketches, with complete repairs below. I found no counterexample to Lemma X or Lemma X′ and no failed substantive step in their proofs. “NOT BROKEN” for the passages means that the claimed master displays follow under the stated setting and Lemma T, with the elementary assembly repairs supplied here; it does not certify an unexamined proof of Lemma T.

Scope and pins: I read the brief and only its permitted source files. I did not inspect other reviews, work files, other lemma files, or the STATEMENT changelog. The full-file hashes identify the captured source bytes; STATEMENT changed during this review, and the pin above is the final reread, headed v1.4.2. Sections 8 and 10 of X.md were not used as proof. No agents or git commands were used.

**1. Lemma X: attempted breaks and checks**

I attacked the pointwise Bayes-factor bound, the fractional moment, concentration of determinant defects in exceptional models, non-superset multiplicity, the empirical inverse-gamma rate, large models near the cap, the top of the t range, and the null truth. None broke the conclusion.

**Variational comparison and the pointwise bound.** Write σ = σ*, B = M + M′. Zero-padding preserves θ*ᵀ(G + I)θ* = nρ′. The two Young inequalities give exactly
Q₀(y) ≤ Q₀^(2)(e) + 2ρ′ and Q_J(y) ≥ Q_J^(1/2)(e) − ρ′.
Thus Q₀ − Q_J ≤ eᵀD′_Je + 3ρ′. Nesting and monotonicity in the penalty imply
0 ⪯ D′_J ⪯ M_(S₀∪J)^(1/2) ≺ I,
and its range is contained in the union's column span. This remains valid for singular Gram matrices and rank-deficient truth models. There is no eigenvalue floor here.

On the noise event, E3 supplies Q_J > 0 and ν/Q_J ≤ (1 + ε₃)/(2σ²). Since b > 0 and Q₀ ≥ Q_J,
(2b + Q₀)/(2b + Q_J) ≤ Q₀/Q_J.
Consequently the stated pointwise BF bound follows. This step neither treats b as independent of the data nor conditions a Gaussian moment on the noise event.

**Fractional moment and the exceptional-model attack.** For λ = (4A + 1)/(4A + 2), condition (c) gives λ₁ = λ(1 + ε₃) ≤ 1 − 1/(8A + 4). The unconditional Gaussian integral bounds the moment by (8A + 4)^((s₀+j)/2). Also λ₁ ≤ 1 bounds the deterministic signal factor by exp(3B/(2σ²)).

Put a_J = (D₀/D_(S₀∪J))^(1/2) and N_j = binom(p − s₀,j). The crucial direction of Jensen is correct:
Σ_J a_J^λ ≤ N_j (N_j^(-1)Σ_J a_J)^λ
             ≤ N_j[c_D(n+1)]^(−λj/2).
An exceptional subset on which a_J is near one does not invalidate this bound; Jensen already takes the worst distribution of the a_J under their mean constraint. Combining it with the prior ratio gives the exponent
A(1 − λ) − λ/2 = −1/4.
With the stated n₀, the remaining geometric factor is at most n^(−j/8) after paying the polynomial in j. The sum above j₁ = ceil(32t/log n) is therefore bounded by a constant times exp(−4t). Paying A_n^λ and the Markov threshold costs at most exp(2t), and the stated M₀ pays the constant. Hence an exceptional collection of determinant-deficient models does not defeat this size-tail estimate. Below the size cutoff, determinant growth is unnecessary: the small-far and good-model arguments control error directly.

**Non-supersets and unions outside Ω.** For S′ = S ∪ S₀, the prior ratio costs at most (2p)^s₀, Q_S′ ≤ Q_S, and interlacing in increasing order gives D_S′/D_S ≤ (n+1)^s₀. A fixed S′ has at most 2^s₀ preimages, including the superset if desired. The displayed A_n is an upper bound. If |S| > s₀ + j₁, then |S ∖ S₀| > j₁; if |S| ≤ m, that number is at most m. Thus the exact ND range needed is available. S′ need not lie in Ω: its ℓ(S′) is an auxiliary positive weight, whereas the actual posterior denominator is bounded using S₀ ∈ Ω. No posterior probability on an inadmissible union is asserted.

**Tail above m_n(t), including sizes near n/2.** I checked the consumed part of [P1] lem:den rather than importing its eigenvalue hypothesis. The variational trial θ* gives Q₀ ≤ σ²E′ + ρ′. In the integral for m^c_(b₊)(S₀)/f₀, set v = σ²u, 1 ≤ u ≤ 1 + n^(−1/2). Its log-likelihood exponent is at least
−|E′ − N|/(2√n) − E′/(2n) − ρ′/(2σ²).
The integration interval has length σ²/√n and IG density at least c_IG. This proves the denominator bound used in §4 without any eigenvalue information. It agrees with B_tail_approx Steps 2–3 at residual r = 0.

For the numerator, b₋ is fixed, so [P1] lem:num gives E N_m = ϖ(|S| > m). The data-dependent rate is handled only by the pointwise mixed-endpoint comparison on 𝓑_n. The prior normalizer W_K cancels in R_m. In particular,
R_m√D₀√n ≤ 2·2^(−s₀)√n/(n+1)·exp(−3t)
           ≤ 2n^(−1/2)exp(−3t).
On N1, E′/(2n) ≤ 1, and for t ≥ 16, n ≥ 16,
Λ″ ≤ √t + t/√n + 1 + B/(2σ²) ≤ t/2 + 1 + B/(2σ²).
Together with Markov at exp(t) and condition (g), this yields the claimed exp(−1.5t) posterior tail. There is no modelwise lower bound on Q required for these large models. Thus models near n/2 do not expose a missing likelihood bound. If m = K, the tail is identically zero.

**Small far models, conditional parameters, and endpoints.** The N2 and N3 unions have the stated probability budgets. In E2, N3 for the empty model gives the required bound on μᵀe, including μ = 0. The Λ choices in §5 imply Δ ≥ Λσ²t/4; the likelihood exponent is at least 3t. Its prior/determinant prefactor is paid by n^((A+1)s₀) ≤ exp(t) and the lower bound on t.

For good models, Q_S differs from ‖e‖² by O(σ²t). The coded posterior has shape ν = 0.01 + n/2, exactly as required by [P1]'s contrast representation with prior shape 0.51. The Gamma tail gives the variance bound; the conditional fitted-mean covariance is vM_S, so its rank, rather than invertibility of G_S, suffices for the Gaussian tail. The resulting posterior error is at most 3exp(−t) per good model.

At t = n^(1−κ₀), ε₂ = O(n^(−κ₀/2) + n^(−κ₀)log n) tends to zero, and the variance error is O(n^(−κ₀/2)). Each condition defining n₀ eventually holds for every larger n and is sufficient throughout the t interval. This is uniformity of constants and n₀, not an assertion of one success event simultaneous over all real t. For s₀ = 0, ρ′ = 0, S₀ is the admissible empty model, the non-superset family is empty, and all prior and denominator bounds remain valid. The assembly 6exp(−t) ≤ exp(−t/2) and 7exp(−t) ≤ 2exp(−t/2) is valid on the stated range.

**2. Passage Lemma X → (1.1): findings and full repair**

**BR1-01 — MINOR — STATEMENT §3, applications of Lemma T; ROUTES §2 Step 2 and the DIST-2 replacement.**

Argument: Lemma T is stated for a deterministic d. The proposed d uses s₀(X), and for DIST-2 also p_ret(X) through m_n(t). A probability bound for each fixed d does not, by itself, imply the same probability bound after choosing d from the observed sample. Conditioning on this choice would also destroy the i.i.d. premise. In addition, writing min(n−1, support bound) does not justify ignoring coordinates if the support bound exceeds n−1.

Minimal repair: put s = s₀^r and use the following deterministic envelopes, for each fixed n,t:
d₁ = min{p_raw, 2s + ceil(32t/log n)},
d₂ = min{p_raw, s + ceil(C_m t)},
where C_m is the constant in X.md §0. Enlarge n₀ once so both uncapped bounds are at most n−1 for all t ≤ n^(1−κ₀). This is possible because they are o(n), uniformly on that range. On 𝒟_n, d_i ≥ 1. The relevant coefficient difference has support at most |S| + s, including dropped true columns; |S| ≤ d_t is covered by d₁, and |S| ≤ m_n(t) ≤ C_m t is covered by d₂. Apply T unconditionally at these deterministic dimensions. With δ = exp(−t),
η²_n(d₁,δ) ≤ C_T t/n,
η²_n(d₂,δ) ≤ C_T′ t log n/n ≤ C_T′ tℓ_n/n.
The constants use only s,A and the declared cutoff constants. This closes the issue without an assumption on ν_x or an additional design remainder.

**BR1-02 — MINOR — ROUTES §2 Steps 2 and 5: omitted sample-mean noise event.**

Argument: Lemma X controls the contrast noise e = Uᵀε, not ε̄. Lemma H's sample identity includes ε̄². Keeping e fixed while replacing ε by ε + h1 leaves every contrast posterior quantity unchanged and changes the plug-in intercept by h. Thus X's success event alone cannot imply the proposed Hellinger ball, even for a fixed design. The missing control comes from (RD), not from Lemma X or from integration over X.

Minimal repair: add
𝓘_t = {ε̄² ≤ 2σ²t/n},  P*(𝓘_tᶜ) ≤ 2exp(−t).
This follows from √n ε̄/σ ∼ N(0,1). Use δ = exp(−t) for T, rather than spending exp(−t/2) on its failure. With c_X = 1/2, the total failure probability, before the interface remainder, is at most
2exp(−t/2) + exp(−t) + 2exp(−t)
≤ 3exp(−t/2),
since t ≥ 16. Therefore the exact prefactor 3 and exponent c = 1/2 of the master theorem remain available. No new hypothesis is needed.

**BR1-03 — MINOR — STATEMENT (1.1) versus Lemma X's rounded size cutoff.**

Argument: Lemma X controls |S| > s₀ + ceil(32t/log n). Display (1.1) uses the unrounded s₀ + C′t/log n. Reusing C′ = 32 would be an invalid set inclusion: when 32t/log n is not an integer, a model at size s₀ + ceil(32t/log n) lies in the master size-bad set and outside X's size-bad set. X gives no bound on the mass of that boundary size.

Minimal repair: distinguish the constants and take C′_master = 33. Since t/log n ≥ M₀ ≥ 16,
ceil(32t/log n) ≤ 32t/log n + 1 ≤ 33t/log n.
The master size-bad set is then a subset of X's size-bad set. The master statement asserts existence of C′, so this changes neither its hypotheses nor its rate.

**Completion of the implication.** On T's deterministic-d₁ event and 𝓘_t, H gives
d_H² ≤ (v/σ² − 1)² + (ε̄² + ‖μ̂ − μ‖²/n)/(2σ²) + η²_n(d₁,exp(−t)).
For any draw outside X's bad set this is at most
[C_X² + C_X/2 + 1 + C_T]t/n.
Choose the master's radius constant at least the square root of that bracket and use C′_master = 33. The entire joint bad set in (1.1), including the size clause, is contained in X's bad set.

Let G_t(X) be the intersection of 𝒟_n and the three interfaces. Given the raw design, the retained design, p, S₀, θ* and m_n(t) are deterministic, and e remains N(0,σ²I). The fixed-design proof is uniform with constants based on s₀^r. Consequently
P*(G_t ∩ {Π(Bad_X | D_n) > exp(−t/2)}) ≤ 2exp(−t/2).
Union with the T and intercept failures as in BR1-02, then with G_tᶜ, proves (1.1). No independence between T's event and the interfaces is used. Dependence of S₀ and p on the design creates no additional union penalty in this conditional integration.

I also tried rare unobserved predictor values and sample-constant true columns as attacks on this passage. They do not defeat the implication: T controls a bounded truncated loss over the raw sparse class and arbitrary intercepts. It does not require an untruncated second moment or population identifiability.

**3. Lemma X′ and passage to (1.2)**

In §9 the event 𝓕₂ and the whole ND-dependent fractional-moment step are absent. The size tail proved above still applies. Up to m_n(t) ≤ C_m t, N2 and N3 cost t log n, so far models can be excluded at ridge loss Λ′σ²t log n and good models have fitted-mean error O(σ²t log n).

The potentially dangerous variance term is handled correctly:
(t log n)/n = √(t/n)·[√(t/n)log n]
             ≤ √(t/n)
for all t ≤ n^(1−κ₀) once n₀′ is large enough. Likewise Λ′t log n ≤ 8n holds uniformly. The displayed n₀′ conditions use no c_D; they do not silently import conditions (c) or (d) from the ND proof. The posterior Gamma deviation is still taken at level t. Thus the mean radius gets the logarithm while the variance radius and exponential probabilities do not. Singular and duplicate-column designs, including a null truth, do not break this argument.

For the population passage use d₂ from BR1-01, the same intercept event from BR1-02, and H. Outside X′'s bad set,
d_H² ≤ C₂ tℓ_n/n,
since both the transfer remainder and the fitted-mean term have that order, while t/n ≤ tℓ_n/n. The tail |S| > m_n(t), although not displayed in (1.2), is already inside X′'s bad set. Conditional integration and the probability budget are identical to the preceding calculation, with G_t containing only 𝒟_n, (E), (C). This proves (1.2) from X′ and T as stated.

**4. Hidden dependence and limits of this review**

No unstated eigenvalue floor, identifiability condition, beta-min level, or bound on the raw coefficient magnitude is used in X's proof. The coefficient cost enters via ρ′ ≤ M + M′. The original eigenvalue-dependent construction of R_n in [P1] lem:den is not needed after the variational replacement; importing that lemma's full assumptions would be unnecessarily stronger than the actual proof.

Polynomial p is used in the noise unions, cutoff bounds, fractional-moment entropy cost, and multiplicity/prior prefactors. These are within X's explicit p ≤ n^A hypothesis. Population transfer uses p_raw ≤ n^A from (RD), so it does not incorrectly substitute the smaller retained dimension for the raw one.

The constants c_IG, κ, c♯, C and n₀ do depend on the fixed σ*² and on M,M′, as declared. X and X′ alone do not establish uniformity over arbitrary changing σ*_n without corresponding rescaling; that extension would need the separately stated scale bridge. There is no hidden fixed-σ assumption relative to the master setting, which explicitly fixes it.

I did not check the proof of Lemma T: its proof file is forbidden by the brief. The passage verdicts therefore take its displayed uniform inequality as an input, exactly as the requested implication does. I checked H's displayed algebra and the sample identity directly. I did not certify the separate reader-version bridge proofs, DIST-3, sampler results, stretch statements, or commentary claims in X §§8 and 10. No numerical search or external reference verification is claimed.

**Verdicts**

- Lemma X: **NOT BROKEN** — the BF, fractional-moment/Jensen, union, mixed-rate size-tail, endpoint and null-truth attacks above all close under its stated hypotheses.
- Passage Lemma X → (1.1): **NOT BROKEN** — the full implication is established above using T as stated; BR1-01–03 are explicit minor repairs to the written assembly, including its joint size clause.
- Lemma X′: **NOT BROKEN** — the duplicate/singular-design and top-range variance attacks fail; the proof has no surviving ND dependence.
- Passage Lemma X′ → (1.2): **NOT BROKEN** — deterministic sparsity and the Gaussian sample-mean event give the required population bound and exact probability budget, conditional on T as stated.

Checkpoint reasons: retain the fractional-moment route; I found no substantive break requiring a different lemma or target. Incorporate BR1-01–03 during the sweep and have the separate T check verify its uniform inequality. These repairs preserve the stated interfaces, rates and exponential form.

CP2: CONTINUE — Proceed on this route through the sweep and council with the three assembly repairs recorded above.

