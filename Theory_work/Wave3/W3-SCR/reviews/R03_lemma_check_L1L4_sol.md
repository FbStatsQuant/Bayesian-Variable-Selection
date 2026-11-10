# R03: independent proof check of L1–L4

## Verdict per item

| Item | Verdict |
|---|---|
| L1.1 | CORRECT |
| L1.2 | CORRECT |
| L1.3 | CORRECT |
| L1.4 | CORRECT |
| L1.5 | CORRECT |
| L1.5° | CORRECT |
| L1.6 | CORRECT |
| L1.7 | CORRECT |
| witness | CORRECT |
| E1 | CORRECT |
| E4 | CORRECT |
| E2+ | CORRECT |
| E2− | CORRECT |
| E2chi | CORRECT |
| E3a | CORRECT |
| E3b | CORRECT-WITH-MINOR-FIX |
| SCR-A | CORRECT |
| A∞ | CORRECT |
| SCR-A° | CORRECT |
| A°∞ | CORRECT |
| A1 | CORRECT |
| A1° | CORRECT-WITH-MINOR-FIX |
| L4.0 | CORRECT |
| B1 | CORRECT |
| B2 | CORRECT |
| B2° | CORRECT |
| B3 | CORRECT |

No BLOCKER or MAJOR finding. The two minor fixes concern a parameter domain and a rate heading; neither changes the screening conclusions under the displayed hypotheses. All lines of all four lemma files, STATEMENT §0–§1 and the requested §2 results, and CODE_CHECK were read. The numbered NOTE entries below record independent derivations and potential failure modes that were checked and rejected; they are not additional defects. Line numbers refer to the files as read for this review.

## Numbered findings and derivation record

1. **MINOR — E3b must explicitly say x′ > 0.**

   Location: `lemmas/L2_noise.md:49–54`, especially the quoted lines
   > **E3b(q, x′) (noise captured by the excess directions).** For E ⊆ [p]∖S₀ with |E| = m ≥ 1 let
   > ≤ exp(−log C(p−s₀, m) − x′m); sum over E and m ≥ 1: ≤ Σ_{m≥1}e^{-x′m}.

   The statement introduces a new parameter x′ without declaring its domain. The geometric-series bound e^{-x′}/(1−e^{-x′}) requires x′ > 0. For negative x′ the displayed bound is negative and cannot upper-bound a probability; the square root defining U′ may also cease to be real. At x′ = 0 the displayed quotient is undefined. This is a missing local domain declaration, not a defect in the intended positive-parameter result.

   Derivation: for each feasible m, use a chi-square tail at z_m = log C(p−s₀,m)+mx′, then sum C(p−s₀,m)e^{-z_m} = e^{-mx′}. For positive x′, the sum over feasible m is bounded by the convergent infinite series e^{-x′}/(1−e^{-x′}).

   Fix: begin the statement “Let x′ > 0.” For q−s₀ < 1 or p=s₀, the event is the full space and its failure probability is zero. No downstream screening proof in L3 uses E3b.

2. **MINOR — A1°'s rate heading is stronger than the rate actually proved.**

   Location: `lemmas/L3_screening.md:77`:
   > ## Corollary A1° (beta-min at the rate σ√(log p/n))

   The same issue occurs in the `STATEMENT.md` heading:
   > **Corollary A1° (beta-min at the √(log p / n) rate; no bound on the total signal).**

   The displayed hypothesis and proof use θ_min ≥ 16σκ^{-1}√(L_n/n), L_n=(q_n+1)log p+log n. This is not generally a constant multiple of σ√(log p/n). For fixed p≥2 and q_n=0, L_n/log p diverges; for growing q_n, the ratio is at least q_n+1. The other assumptions do not force L_n=O(log p). The actual corollary is valid; this is a mismatch in its description, not an incorrect numerical constant or implication.

   Fix: title it “beta-min at rate σ√(L_n/n)” or spell out L_n. To advertise the shorter rate, restrict to q_n=O(1) and log n=O(log p). The phrase “no bound on the total signal” should be understood as no fixed bound M of A1: the explicit assumptions still include ‖μ‖=o(nσ) and a constraint on ‖θ*‖₂/θ_min. Prefer “without a fixed total-signal bound” to avoid suggesting these restrictions disappear.

3. **NOTE — L1.1 and L1.2: residual, block inverse, and n/(n+1) factors all check.**

   Locations: `lemmas/L1_score.md:7–33`, including
   > q_S(v) = ‖v‖²/(n+1) + (n/(n+1))·vᵀR_Sv
   > q_S(v) − q_{S∪t}(v) = (n/(n+1))·g_v(t|S)

   Independent derivation: the strictly positive eigenvalues of G_S+λI make the ridge objective strictly convex even when G_S is singular. Completing its square gives min_b{‖v−X_Sb‖²+λ‖b‖²}=vᵀR_{S,λ}v. The nontrivial eigenvalues of R_{S,λ} are λ/(d_i²+λ); on the orthogonal complement they are 1. Thus 0≺R≤I, R²≤R, and the unpenalised minimum is a lower bound. Centring is preserved since X_S and v are centred.

   H_S=(n+1)(G_S+λ₀I), so subtracting n/(n+1) times the ridge fitted energy gives exactly the quoted q formula. It yields Q in [(n−1)/(n+1),n−1], positivity of 0.02+Q, and nesting monotonicity. A larger model enlarges the variational feasible set by allowing additional coefficients equal to zero.

   With A=G_S+λI and b=X_Sᵀx_t, the block Schur complement is a_λ=n−1+λ−bᵀA^{-1}b=λ+min_b{‖x_t−X_Sb‖²+λ‖b‖²}>0. The block inverse adds (R_Sx_t)(R_Sx_t)ᵀ/a to the fitted operator at λ₀, hence subtracts it from R_S. Taking quadratic forms gives both gain identities and the factor (n+1)/n in the definition of γ. Determinants acquire a_λ, and H acquires the additional factor n+1. All four parts of L1.2 follow, including S=∅ with the standard empty determinant 1 and empty fitted operator 0. No fix required.

4. **NOTE — L1.3 and L1.4: determinant and score penalties have the correct signs and constants.**

   Locations: `lemmas/L1_score.md:35–47`, especially
   > D(t|S) := (n+1)·a(t|S)/a_1(t|S) satisfies 1 ≤ D(t|S) ≤ n+1
   > F(S∪t) − F(S) = −log[(2p−1−k)/(k+1)] − ½ log D(t|S) + ν·log[(0.02 + Q_S)/(0.02 + Q_{S∪t})]

   The minimum representation makes a_λ increasing in λ. Scaling the entire λ₀ objective by n+1 gives (n+1)a_{λ₀}=1+min_b{(n+1)‖x_t−X_Sb‖²+‖b‖²}≥a_1, whereas a_{λ₀}≤a_1. Therefore 1≤D≤n+1. Evaluating the a_1 objective at b=0 gives a_1≤n and consequently D≥(n+1)a/n. The prior ratio is (k+1)/(2p−1−k), not its reciprocal. The two determinant contributions combine into −½log D. Finally the negative log-residual score becomes a positive log of old/new residual. Quadratic scaling gives g_y=g_{y_c}/τ̂². No fix required.

5. **NOTE — L1.5, L1.5°, and L1.6: threshold equality still gives strict improvement; large x or huge p does not invalidate the implications.**

   Locations: `lemmas/L1_score.md:49–71`, including
   > νρ > (n/2)·(n/(n+1))·g_y/(n − 0.98) > n g_y/(2(n+1))
   > Finally ρ̄_n(n−1) = T_n·n(n−1)/((n+1)(n+0.02)) ≤ T_n.

   Write L=2log(2p−1)+log(n+1)>0. Then T_n=(n+1)L/n and the penalty upper bound is L/2=nT_n/[2(n+1)]. With δ=ng_y/(n+1), ρ=δ/(0.02+Q_S) lies in [0,1); under either sufficient hypothesis it is positive. Since ν>n/2 and 0.02+Q_S≤n−0.98<n, the L1.5 strict inequality is valid even at g_y=T_n. Its conclusion is strict F improvement, as needed by LO.

   In L1.5°, ρ̄=L/(n+0.02) and νρ̄=L/2 exactly. The hypothesis says ρ≥ρ̄>0. For 0<ρ<1, −log(1−ρ)>ρ; therefore a weak threshold inequality again produces strict improvement. The stated comparison ρ̄(n−1)/T_n=n(n−1)/[(n+1)(n+0.02)]≤1 is correct. If ρ̄≥1, the hypothesis cannot hold, so the implication is vacuous rather than false.

   For deletion, let A=log((2p−k)/k)+½log D. Non-improvement implies A≤νlog(1+δ/(0.02+Q_S))≤νδ/(0.02+Q_S). Rearranging gives exactly L1.6, with the displayed direction ≥. Feasible S has k≤K; this is inherited from the score's model space when invoking L1.4. No fix required.

6. **NOTE — L1.7: augmentation handles singular designs without treating centred noise as isotropic in n+p dimensions.**

   Location: `lemmas/L1_score.md:73–82`:
   > a(t|S) = ‖(I − P̃_S)x̃_t‖²
   > μ̃ = X̃θ* − b̃ with b̃ := [0; √λ₀θ*]

   The augmented Gram is G_S+λ₀I. For t∉S the lower coordinates of x̃_t are orthogonal to all selected columns' lower coordinates; expanding the projector gives x_tᵀR_Sv and the residual length squared a. For two zero-padded vectors it gives uᵀR_Sv. Idempotence of I−P̃_S turns these quadratic forms into squared projection norms, so the unit-vector expression for g is exact. The lower-coordinate discrepancy in μ̃ is precisely −b̃, with norm c_θ. None of these claims require G_S invertible. No fix required.

7. **NOTE — witness, E1 and E4: the probability counts use one scalar per S, not p scalars per S. Degenerate mean causes no failure.**

   Locations: `lemmas/L2_noise.md:9–24`, particularly
   > t(S) is a function of (X, θ*) only (not of ε)
   > there are at most N_q sets S (one Gaussian variable per S, because t(S) is deterministic).

   T=S₀∖S is a nonempty finite set, so the smallest-index maximiser exists even if all gains vanish. Normalising by σ_S²>0 preserves this maximiser. Because R_Sx_t is centred, the variance of x_tᵀR_SCε is σ²x_tᵀR_S²x_t≤σ²a. The threshold σr√a thus has failure probability ≤2e^{-r²/2}=e^{-x}/N_q. Only the fixed t(S) is controlled for each S; L3 never uses E1 at a data-chosen alternative witness.

   Similarly μᵀR_SCε has variance σ²μᵀR_S²μ≤σ²m_S². Its upper tail at σm_Sr is ≤e^{-r²/2}=e^{-x}/(2N_q). E4 actually has the stronger failure bound e^{-x}/2; the stated e^{-x} is safe. Only an upper bound on the cross term is needed in L3.

   Duplicate truth columns with cancelling mixed-sign coefficients can give μ=0 even though s₀≥1. Then μᵀε and μᵀR_SCε are identically zero, and the relevant events hold surely. The generic Gaussian formula printed in L2:3 and :24 has division by v², so at v=0 it should be read with this direct deterministic case, not evaluated as 0/0. An optional sentence “zero-variance variables are handled directly” makes this convention explicit. It does not require a nonzero-mean assumption or alter any event/proof conclusion. No mathematical fix required.

8. **NOTE — E2+, E2−, E2chi, E3a and E3b: chi-square degrees of freedom, covariance contractions, and counts check.**

   Locations: `lemmas/L2_noise.md:26–54`, including
   > τ̂² ≤ τ_n²(1 + (2+√2)a + 2a²) ≤ τ_n²(1 + 2a)²
   > A = CB₁B₁ᵀC, 0 ⪯ A ⪯ I
   > W(E) := span X̃_{S₀∪E} ⊖ span X̃_{S₀} (dimension m)

   C is rank n−1 and μ is centred, so ‖Cε‖²/σ² is χ²_{n−1} and ‖y_c‖²=‖μ‖²+2μᵀε+‖Cε‖². Put a=√(x/(n−1)). AM–GM gives 2σ‖μ‖/√(n−1)≤τ_n². The upper correction is at most τ_n²[(2+√2)a+2a²], bounded by τ_n²[4a+4a²] for every a≥0. The lower correction is at most τ_n²(2+√2)a≤4τ_n²a. Each event costs one chi-square and one one-sided Gaussian tail: 2e^{-x}, with no independence needed. For a>1/4 the last lower bound may be negative; it remains valid. E2chi is exactly the rank n−1 lower-tail event and costs e^{-x}.

   In E3a, the augmented span has dimension k even with duplicate original columns. An orthonormal B has B₁ᵀB₁≤I; hence CB₁B₁ᵀC is a positive contraction of rank ≤k. Dominating its quadratic form by a rank ≤k projection and then χ²_k is legitimate; no assertion that the actual augmented noise is isotropic is made. For z=log C(p,k)+x, the safe threshold (√k+√(2z))² exceeds k+2√(kz)+2z. Summing e^{-z} over sets and k gives qe^{-x} for each of the two families, hence 2qe^{-x}. For q=0 the event is vacuous and its failure probability is zero.

   In E3b, augmentation also makes span inclusion strict by exactly m dimensions, and the same contraction argument works for an orthonormal basis of W(E). The count is C(p−s₀,m), not C(p,m). The geometric sum is correct subject to finding 1. No other fix required.

9. **NOTE — SCR-A and SCR-A° deliver precisely the LO and coded-certificate statements.**

   Locations: `lemmas/L3_screening.md:7–24,38–56`, especially
   > g_{y_c}(t|S)^{1/2} ≥ √Γ_n(q) − σ r_n > τ̄_n(x)√T_n ≥ τ̂√T_n
   > 0.02τ̂² + ‖y_c‖²/(n+1) ≤ 1.02τ̂²
   > γ(t|S)/σ_S² ≥ Ψ_n(q)

   In SCR-A, reverse triangle inequality at the fixed witness gives the first inequality. MC makes its right side positive before squaring. On E2+, τ̂≤τ̄, hence g_y>T_n almost surely, giving an improving addition. The full-probability condition τ̂>0 from Model G can be intersected with both theorem events if literal pointwise events are desired. The probability cost is 1+2=3 tails.

   For SCR-A°, let d=n−1, B=2a+2a²+r/√d, m²=μᵀR_Sμ. The exact decomposition is
   0.02τ̂²+q_S(y_c)=[0.02+d/(n+1)]τ̂²+[n/(n+1)]y_cᵀR_Sy_c.
   The first coefficient is ≤1.02. On E4 and E2+, the second quadratic form is ≤m²+2σmr+σ²d(1+2a+2a²)≤dσ_S²(1+B), since 2σm≤√d σ_S². Therefore multiplying the residual bound by ρ̄(n+1)/n yields
   ρ̄ d σ_S²[1+B+1.02(n+1)τ̄²/(ndσ_S²)].
   Replacing σ_S² in the bracket's denominator by σ² increases that bracket, and ρ̄d≤T_n. This is exactly the ϑ° bound; the factors 1.02, n/(n+1), and (n+1)/n have not been lost. MC° and σ≤σ_S give √g_{y_c}>σ_S√(T_n(1+ϑ°)), which is positive and may be squared. L1.5° applies. The event costs 1+2+1=4 tails (or at most 3.5 using E4's sharper count).

   Every relevant |S|≤q≤K−1 has this addition in the coded neighbourhood, including |S|=K−1. Thus no such deficient S can be LO. The two set inclusions in L3:22 have the right direction: the selected certified deficient model is a member of the family, and existence of any deficient certified endpoint implies failure of the deterministic good event. An empty intersection is [p] as explicitly declared in STATEMENT. The proof covers all seeds simultaneously because the event depends only on the data and excludes all bad LO models. It requires no independence involving τ̂ or the fit. No fix required.

10. **NOTE — A∞ and A°∞: the o(1) bounds are in the required direction and remain valid for triangular arrays and q=0.**

    Locations: `lemmas/L3_screening.md:27–35,59–63`, including
    > N_q ≤ (p+1)^q
    > q log(p+1) ≤ q log p + q/p ≤ q log p + 1
    > τ̄_n² = (σ² + ‖μ‖²/(n−1))(1 + o(1)) = o(nσ²)

    Independently, C(p,k)≤p^k≤C(q,k)p^k for 0≤k≤q, so summing gives N_q≤(p+1)^q. When q=0 both sides are 1. Since q≤K−1≤p−1, q/p≤1, so log N_q≤qlog p+1. For x_n=√log n, define D_n=2log p+log n≥log n and e_n=2log 2+2+2√log n. Then
    T_n≤(1+1/n)(D_n+2log 2+1/n),
    r_n≤√(2qlog p)+√e_n,
    √e_n/√D_n=O((log n)^{-1/4})→0.
    These estimates are uniform in p≥2 and allowed q. Also a_{x_n}=O((log n)^{1/4}/√n)→0. Because σ≤τ_n, the extra σ√e_n is o(τ_n√D_n), even if σ varies or τ_n diverges. Thus the MC right side is bounded above by (1+η_n) times the displayed A∞ denominator for some nonnegative η_n→0. A liminf strictly greater than 1 gives a fixed gap eventually, not merely a subsequential gap. Finally 3exp(−√log n)→0.

    For A°∞, r_n²≤2qlog p+e_n=o(n) by the stated assumption. Moreover
    τ̄_n²/(nσ²)=(1/n+‖μ‖²/[n(n−1)σ²])(1+2a_{x_n})²→0
    from ‖μ‖=o(nσ). Therefore all four nonnegative components of ϑ° tend to zero. The same uniform T_n and r_n upper bounds give MC° eventually, and 4exp(−√log n)→0. This requires no unstated lower bound on σ, polynomial bound on p, or bounded s₀. No fix required.

11. **NOTE — L4.0 and B1: the augmented cross term is correct even for mixed signs.**

    Locations: `lemmas/L4_bridges.md:8–22`, including
    > Σ_{t∈T} θ*_t·x_tᵀR_Sμ = ... = ‖w‖² − wᵀb̃
    > the map Δ ↦ Δ(√Δ − c_θ)² is nondecreasing on [c_θ², ∞)

    Write A=I−P̃_S, w=AX̃_Tθ*_T, z=Ab̃. Since A kills the present true augmented columns, Aμ̃=w−z. The weighted correlation sum is wᵀ(w−z)=u²−wᵀb̃≥u(u−c_θ), u=‖w‖. The lower blocks for S and T have disjoint supports, giving
    u²=min_β{‖X_Tθ*_T−X_Sβ‖²+λ₀‖β‖²}+λ₀‖θ*_T‖₂²≥Δ(S).
    Under √Δ≥c_θ, u(u−c_θ)≥√Δ(√Δ−c_θ)≥0. Hölder bounds the weighted sum above by ‖θ*_T‖₁ max_t|x_tᵀR_Sμ| without any same-sign assumption. Also a_t≤n−1+λ₀<n, so max_t γ_t≥(max_t|x_tᵀR_Sμ|)²/n. Squaring the preceding nonnegative lower bound yields L4.0.

    For B1, f(d)=d(√d−c_θ)² has derivative (√d−c_θ)(2√d−c_θ)≥0 on d≥c_θ². Replacing Δ(S) by its minimum and ‖θ*_T‖₁ by the larger ‖θ*‖₁ decreases the right side. The min over S is over a nonempty family (it includes ∅), so no empty-min issue arises. No fix required.

12. **NOTE — B2 and B2°: there is no missing |T| factor; the factors 4 and 9 are justified.**

    Locations: `lemmas/L4_bridges.md:24–47`, especially
    > ≥ (φ^a(n−1)/n)·(√(φ^a(n−1))θ_min − c_θ/√|T|)²
    > For u ≥ 2c_θ: u − c_θ ≥ u/2 and u + c_θ ≤ 3u/2

    Let h=φ^a(n−1), m=|T|, V=‖θ*_T‖₂². The anchored definition gives Δ(S)≥hV and V≥mθ_min². L4.0 and ‖θ*_T‖₁²≤mV give
    max γ≥(h/n)(√h√V−c_θ)²/m
    ≥(h/n)(√h θ_min−c_θ/√m)²
    ≥(h/n)(√h θ_min−c_θ)².
    The premise √h θ_min≥c_θ makes each bracket nonnegative. Thus both squaring comparisons have the right direction for m=1 and m≥2. Taking minima proves precisely STATEMENT B2, including its unconditional lower bound on Δ_n(q).

    For B2°, with any 0<κ≤φ^a, u²≥κ(n−1)V=u₀² and u₀≥2c_θ. The unnormalised gain is ≥u²(u−c_θ)²/(n‖θ*_T‖₁²), while σ_S²≤σ²+(u+c_θ)²/(n−1). These are a lower numerator bound and an upper positive denominator bound, so dividing them gives a valid lower ratio bound. Replacing u−c_θ by u/2 and u+c_θ by 3u/2 produces
    (n−1)u⁴/[n‖θ*_T‖₁²(4σ²(n−1)+9u²)].
    For A>0, B>0, d[ u⁴/(A+Bu²)]/du=(4Au³+2Bu⁵)/(A+Bu²)²≥0; replacing u by u₀ is valid. Simplifying gives
    ((n−1)²/n) κ²V²/[‖θ*_T‖₁²(4σ²+9κV)]
    ≥((n−1)²/n) κ²V/[m(4σ²+9κV)].
    V/(4σ²+9κV) has positive derivative 4σ²/(4σ²+9κV)², so V≥mθ_min² yields denominator 4σ²+9κmθ_min² after cancellation. Since m≤s₀, replacing m by s₀ decreases the bound. This proves the stated general κ version and the exact STATEMENT version κ=φ^a. The premise of the latter forces φ^a>0 since c_θ>0. No hidden monotonicity in a varying κ is needed. No fix required.

13. **NOTE — B3 and the final design remark are valid with the ordinary empty-matrix convention.**

    Locations: `lemmas/L4_bridges.md:49–58`, particularly
    > for unit v, vᵀ(M/A)v = min_u [u; v]ᵀM[u; v] ≥ λ_min(M)
    > Non-true columns may be arbitrarily collinear among themselves (exact duplicates included)

    For S nonempty and S⊉S₀, |S∪T|≤q+s₀, so the sparse floor makes G_{S∪T} positive definite. For any unit v,
    min_u [u;v]ᵀG_{S∪T}[u;v]≥κ(n−1)min_u(‖u‖²+1)≥κ(n−1).
    This proves the anchored floor. For S=∅ the same conclusion is directly the assumed floor on G_{S₀}; no nonempty inverse is needed. The superset floor follows because its sets are among those in the premise. The phrase “every U” can equivalently be restricted to nonempty U to avoid referring to a minimum eigenvalue of an empty matrix. This is a conventional interpretation, not a restriction on designs. If q+s₀ exceeds attainable rank, the sparse-floor premise is impossible; the implication is still correct.

    The final remark concerns all eligible S: positive anchored floor excludes any nonzero linear combination of missing true columns in span X_S, including a dependence giving zero. It imposes no invertibility of G_S for a false-only S. Duplicates among false columns are therefore compatible with the anchored condition if their span is suitably separated from the truths; B3's stronger sparse floor forbids such duplicates whenever pairs are within its tested sizes. No fix required.

14. **NOTE — A1 and A1° constants and their links to Lemma B check.**

    Locations: `lemmas/L3_screening.md:66–85`, including
    > c₁ := κ²b²/(200(M² + σ²))
    > Ψ_n(q_n) ... ≥ (n/8)·min{κ²θ_min²/(4σ²), κ/(9s₀)} ≥ 8𝐋_n

    A1: τ_n²≤M²+σ²=:τ_*² by triangle inequality and column normalisation. For large n, √(κ(n−1))b≥2M/√(n+1). In B2 each prefactor and nonnegative bracket can be decreased using φ^a≥κ, θ_min≥b, c_θ≤M/√(n+1). Hence Γ≥κ²b²(n−1)²/(4n)≥κ²b²n/16, since (n−1)²≥n²/4 for n≥2. The A∞ denominator squared is at most 2τ_*²[2(q+1)log p+log n]≤4τ_*²c₁n. Its ratio to Γ therefore gives ρ²≥200/64>2. This is stronger than the asserted √2 margin. For p≤n^A and q=o(n/log n), ((q+1)log p+log n)/n→0; fixed positive c₁ eventually suffices. No condition on bounded s₀ is silently inserted (indeed b and M already imply s₀≤M/b).

    A1°: the norm hypothesis is exactly c_θ≤½√(κ(n−1))θ_min, so B2° applies with the fixed lower bound κ. Using a+b≤2max(a,b) and (n−1)²/n≥n/4 gives the quoted n/8 minimum bound. The beta-min inequality squared is κ²θ_min²n/(32σ²)≥(256/32)L_n=8L_n. The sparsity condition is κn/(72s₀)≥(576/72)L_n=8L_n. Both are required, and both are present. Thus Ψ≥8L_n. The A°∞ denominator squared is ≤2[2(q+1)log p+log n]≤4L_n. Consequently (ρ°)²≥2. Also qlog p=o(n) and ‖μ‖=o(nσ) are expressly assumed, completing the application of A°∞. These calculations work with σ depending on n. Only the heading fix in finding 2 is needed.

15. **NOTE — code interface spot-check agrees with the proof's use of CC1–CC5.**

    Locations and quoted source lines:
    `Scripts/SMC_BVS/core/cpp/v3_engine.h:397`:
    > else { if ((int)C.S.size() >= K) continue; add_var(Q, j); }
    `v3_engine.h:414`:
    > A.termination = "no_improvement"; A.local_certified = true; A.returned = C.S; A.returned_F = C.F; break;
    `Scripts/SMC_BVS/core/v3_run.R:179`:
    > out$local_certified <- isTRUE(ls$local_certified) && identical(as.integer(out$hpm), as.integer(ls$returned))
    `v3_run.R:194`:
    > out$local_certified <- cert_final || cert_ls0
    `Scripts/SMC_BVS/core/cpp/v3_score.h:223`:
    > o.logm = (arg > 0) ? D->logCn - 0.5 * (ldH - ldA) - D->nu * std::log(arg) : NEG_INF;

    Read the full requested code intervals. The scan includes all feasible flips and swaps, uses strict F improvement, and distinguishes an unscanned move-limit return from a certified scanned centre. In R the certificate requires equality to the reported HPM, and unsuccessful status resets it. The data setup uses K=min(p,n/2), ν=a₀+n/2 and logprior=logw−logWK, logw=−log2−log C(2p−1,k). The quadratic uses Q=yty−n*quad. This matches the mathematical score up to constants under EX-A. The enumeration branch was accepted from CODE_CHECK, as permitted; it was not independently executed. No code mismatch found in the spot-check. No fix required.

16. **NOTE — edge-case and numerical falsification record.**

    Locations anchoring the edge cases: `lemmas/L1_score.md:20` “Let t ∉ S”; `lemmas/L2_noise.md:9` “S ⊉ S₀”; `lemmas/L3_screening.md:7` “q ∈ {0, …, K−1}”; `lemmas/L4_bridges.md:3` “T := S₀∖S ≠ ∅.”

    S=∅ uses zero fitted operators and empty determinant 1. q=0 gives N_q=1 and a single witness. For p=1, K=1, q=0, log(2p−1)=0 but T_n=(1+1/n)log(n+1)>0, so the strict-threshold reasoning still works. K=1 similarly permits the needed addition only from ∅; nothing invokes an illegal second addition. If s₀>q, the theorems may exclude every LO model of size ≤q rather than assert a model of that size exists. This is consistent with their conditional output statements. If G_S is singular, every ridge inverse remains defined and every original-space projector P_S remains defined; only B3 demands nonsingular Grams. Mixed-sign coefficients are covered by absolute values and Hölder. Large x makes some lower bounds vacuous, not invalid. Scaling σ with n is explicitly handled in finding 10. The null set τ̂=0 has no probability effect and may be removed from the named events.

    Independent scratch code: `reviews/R03_scratch/check.py`, executed using `py -3.13` with OMP_NUM_THREADS=1 (and OPENBLAS_NUM_THREADS=1). It does not import scr_lib.py or the existing falsification script. It tests n∈{3,4,7,15}, p∈{1,2,5}, mixed-sign signals, random centred standardised designs, and exact duplicate columns. It directly computes the score from determinants and inverses; checks residual-operator updates, quadratic decrements, all D bounds, both sufficient-addition implications, and the per-model bridge bounds when their hypotheses hold. Counts: 136 base models, 366 additions, 125 applicable L4.0 checks, 29 ordinary sufficient-addition cases and 50 self-normalised sufficient-addition cases. Maximum absolute quadratic-decrement identity error: 7.105427357601002e−15. All assertions passed. Conditional B2° checks were included but not separately counted; the analytic derivation, rather than a claim of random-test coverage of every parameter regime, supports its verdict. These finite floating-point checks supplement the derivations; they do not establish the probability or asymptotic claims.

## Disposition

The requested theorem bodies and Lemma B follow from these proofs under Model G and EX-A. Add x′>0 to E3b and revise A1°'s descriptive heading. No changes to T_n, 1.02, the n/(n+1) factors, 3e^{-x}/4e^{-x}, c₁, the constants 16/576, or B2°'s 4/9 are warranted by this review. No repository source or lemma file was edited, and no git state-changing command was run.
