# Independent midpoint review — W3-POST2 v1.2

**Verdict: CONTINUE.** The program is worth continuing as stated. I found no fatal or major defect in the seven principal claims. In particular, the stronger expectation bound in C is supported by a valid deterministic lower bound on the reference marginal likelihood, and the floor-free arguments in E and D(b) survive independent examination. D(b) needs a small repair to its presentation of simultaneous event bounds; no stronger hypothesis or weaker rate is needed.

The statements are design-agnostic: the hypotheses constrain determinants, approximation losses, or the true-support Gram matrix, rather than specifying a design family. The polynomial dimension restriction and fixed support size are used in the counting and cutoff arguments. B is deliberately more general and does not need that dimension restriction. The distinction between in-sample marginal Hellinger contraction and an out-of-sample predictive theorem is maintained.

Scope: I read STATEMENT v1.2 and A–E, and checked the relevant inherited arguments against W1-T03R/PROOF.md, the two specified locked TeX proofs, and W3-POST/STATEMENT.md and both of its lemma files. I did not read W3-POST2 LOG.md, REPORT, or existing review files. References to earlier reviews embedded in the supplied proof files were not treated as evidence. No numerical claims were independently certified; the assessment below rests on the analytical arguments.

## Per-claim assessment

| Claim | Assessment | Reason / required repair |
|---|---|---|
| A1 | **Sound** | Rank domination replaces full rank in the chi-square event, while the exact determinant weights are retained in the sums. The upper smoother comparison needs a floor only on S₀. The amplified OS tail covers the comparison unions, including unions outside Ω. Beta-min qualifications are inherited, as explicitly clarified in A's own statement. |
| A2 | **Sound** | Monotonicity of Q under adjoining columns gives a lower bound on every superset odds ratio. Summing distinct supersets gives δ ≥ (1−δ)𝒪⁰. The deterministic and random-design necessity consequences follow from this inequality. |
| B | **Sound** | The variational comparison produces the stated bounded approximation cost plus a Gaussian cross term. The fixed-rate numerator identity holds for arbitrary positive Gaussian truth density, including means outside col X. The normalization retains the exact determinant. The asymptotic consequence requires the fixed/common M and B already used in the uniform statement; clarify the growing-cost remark as in finding 3. |
| C | **Sound** | C1's choice of integration interval according to the sign of E′−N is legitimate in a pointwise lower bound. It removes the adverse linear term without requiring independence. C2 can then take the expectation of the nonnegative fixed-rate numerator. The remaining contributions have controlled truncated expectations, rather than merely O_P bounds. |
| D(a) | **Sound** | Conditional on S₀, fitted mean error is tight, the variance has parametric posterior concentration, and F₀ transfers the prediction bound to coefficients. Vanishing wrong-model mass suffices for the stated posterior probability conclusions; no unbounded-loss expectation is inferred. |
| D(b) | **Repairable (minor proof bookkeeping)** | The retained-set strategy and rates are sound. Make the S₀ cross-term bound on the working event explicit, and explicitly justify the uniform conditional variance constant before applying Chebyshev; see finding 1. No change to the theorem is needed. |
| E | **Sound** | The ridge-loss cross-term event has the advertised union bound. The likelihood comparison uses only F₀ to control Q at the true model and rank-based noise increments for competing unions. The threshold c₁ gives strict asymptotic slack after the prior/determinant prefactor. Fix the event-probability typo in the statement. |

## Stress checks of the three riskiest steps

### C1: the denominator improvement is valid

The reference comparison is deterministic:

`Q^c_{S₀} ≤ ||e||² + ρ`, with `ρ = (||μ||² + ||θ*||²)/n`.

The quoted bound on ρ is consistent with F₀: `||θ*||² ≤ nM/((n−1)φ₀²)`, hence `ρ ≤ M + M/((n−1)φ₀²) ≤ M + M/(2φ₀²)`. There is no missing signal/noise cross term because the variational argument evaluates at the exact true coefficient.

For `F(u) = −N log(u)/2 + E′(1−1/u)/2`, the chosen interval makes `F′(1)(u−1) ≥ 0`. On that interval, `|F″| ≤ (8/9 + 128/27)N < 6N`, so `F ≥ −3`. The interval is allowed to depend on E′: it is merely a subset of the domain of a positive integral, selected separately for each observed data vector. Its length and the IG density lower bound are deterministic. Dividing by f₀ is also correct, since the exponent in f₀ is exactly −E′/2.

In C2, `E[N_m 1_event] ≤ E N_m = ϖ(E_m)` uses nonnegativity, not independence. The exceptional probability is O(1/n). This is sufficient to turn the reference tail into an expectation estimate of order n^(−1/2). I find no reason to retreat to the older subpolynomial-loss bound.

### E1: the floor-free comparison closes

The critical lower bound is

`D ≥ L_S − 2σ*sqrt(2C_x L_S log n) − σ*² C_A j₀ log n − 8(M+σ*²)`.

It follows by comparing Q_S to Q_{S₀}, not by claiming a floor on S or S′. The projection increment `P_{S′}−P_{S₀}` has rank at most the number of extra columns; rank deficiency causes no problem. The cross-term variance is at most `σ*² L_S` because `(I−M_S)² ≼ I−M_S`. Counting at most `2^{s₀}(j₀+1)p^{j₀}` models gives the stated event probability.

After setting `L_S = λσ*² log n`, the function `λ−2sqrt(2C_x λ)−C_A j₀` is increasing in the relevant range. The stated c₁ is exactly the root needed to exceed `(2/log 2)(s₀(A+1)+2)`. The strict inequality c > c₁ absorbs the bounded ridge remainder and the vanishing denominator error. The separate D ≥ B′ case is valid. No hidden full-rank condition is needed on the comparison unions.

### D(b): a growing collection does not invalidate uniform control

The retained collection is deterministic given the design and truth. Its members have bounded size and ridge loss O(log n), even though the number of members may grow polynomially. The proof already uses simultaneous projection and cross-term events, so it does not rely on taking a supremum of unrelated pointwise O_P bounds over this growing collection.

Outside the retained collection, the large-size tail and strict supersets are controlled without beta-min. For far underfits, E1 is applied modelwise only where its loss threshold holds; the remainder is handled by the amplified OS tail. This is a legitimate restriction of the assembly argument and does not assume global ID^M.

Within the collection, the leading variance fluctuation `||e||²−Nσ*²` is common to all models; the model-specific remainder is O(log n). Consequently the supremum of the conditional variance means differs from σ*² by O_P(n^(−1/2)). This supports the parametric variance rate. A bounded conditional fitted-mean covariance trace then gives vanishing mass beyond a sufficiently large fixed multiple of log n. Choosing M_n = sqrt(log n) for the Hellinger consequence is valid.

## Numbered findings

1. **MINOR — D(b) mixes stochastic bounds with bounds asserted on a particular event.** `lemmas/D_hellinger.md:59–66` (especially the S₀ parenthesis at line 63). The cross-term event 𝒢⁵ covers the underfits, not S₀. Saying the S₀ remainder is O_P(1), “a fortiori,” does not by itself establish the displayed deterministic bound on every outcome of 𝒢^sup ∩ 𝒢⁵. Similarly, uniform O_P convergence of E[v|S,y] should not silently become a deterministic variance bound on that event.

   **Proposed fix:** use the existing event, with no additional union bound. Put `a₀ = (I−M_{S₀})μ_c`. This vector lies in col X_{c,S₀} and `||a₀||² ≤ L_{S₀} ≤ ρ̄`. On G2*,

   `|eᵀa₀| ≤ ||P_{S₀}e|| ||a₀|| ≤ σ*sqrt(C_A s₀ ρ̄ log n)`.

   For sufficiently large n this is at most `σ*² sqrt(2C_x c₂) log n`, since ρ̄ is fixed. This supplies line 62 for S₀ too. Then G1 and the displayed Q bound imply deterministically on the working event `sup_S |E[v|S,y]/σ*²−1| = O(sqrt(log n/n))`. In particular, it is eventually at most 1/4. The exact IG variance formula then gives `sup_S Var(v|S,y) ≤ 4σ*⁴/n` for sufficiently large n. Separately retain the sharper O_P(n^(−1/2)) assertion using the actual chi-square fluctuation, as the proof intends. All advertised constants and rates can be retained.

2. **NIT — probability of the good event is written as small.** `STATEMENT.md:19` describes 𝒢⁵_n with “(P ≤ 1/n)”. Literally this suggests the good event has probability at most 1/n, whereas E1 proves its complement has that probability.

   **Proposed fix:** write `P((𝒢⁵_n)^c) ≤ 1/n` explicitly, matching `lemmas/E_visibility.md:19` and its proof.

3. **MINOR — growing approximation cost needs a probabilistic qualification.** `lemmas/B_tail_approx.md:59–60` says a cutoff “must absorb a factor e^{O(B_n)}.” The displayed first-moment argument establishes `Λ″_n = O_P(B_n)` when B_n → ∞; it does not, by itself, establish tightness of `exp(Λ″_n−C B_n)` for a fixed C. Nor does a sufficient upper-bound argument establish what a cutoff must do.

   **Proposed fix:** replace this sentence by: “The displayed bound yields an exponential factor exp(O_P(B_n)); for example, choosing L_n with log L_n/B_n → ∞ makes its last term vanish. The fixed-B tightness conclusion above should not be transferred verbatim to growing B_n.” If a fixed exponential-in-B_n normalization is desired, prove it separately using the Gaussian tail of εᵀr. This does not affect Claim B's fixed-B conclusion.

No FATAL or MAJOR findings. The next stage should preserve the stronger C, D(b), and E targets and make these local corrections before final verification.
