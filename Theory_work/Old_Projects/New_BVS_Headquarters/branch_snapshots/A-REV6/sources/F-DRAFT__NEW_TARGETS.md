# F-DRAFT: new theorem targets from the draft, with precise statements and proof skeletons

Branch `theory/F-DRAFT`, 2026-11-02. Candidates only; nothing reviewed or adopted. Notation of `00_COMMON.md` and
`METHODOLOGY_v3.md` §§5–6.3. Status words: PROVED / PROOF SKETCH / CONJECTURE / OPEN, never upgraded. Numerical
references are to `scripts/wstab_check.out` (exact enumeration, p = 12, two blocks of 6, base R, seed 20261102).

## 0. Notation and standing objects

- Standardised X, y (‖x_j‖² = ‖y‖² = n − 1); Ω = {S : |S| ≤ K}; m(S), BF(S) = m(S)/m(∅); ϖ(S) = w(|S|)/W_K;
  π = ϖ·BF/Z̄₁; ν = a₀ + n/2; t_S = n z_SᵀH_S⁻¹z_S; Q_S = yᵀy − t_S; D_S = det H_S/det(G_S + I).
- Blocks C₁..C_J (any partition, |C_b| ≤ K; the method's is deterministic in X); tables r_b(U) = BF(U), U ⊆ C_b;
  γ₀ = ϖ ∏_b r_b(S ∩ C_b); π₀ = γ₀/Z̄₀; d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b); q_φ ∝ γ₀e^{φd}; Z̄_ψ = Σ_Ω γ₀e^{ψd};
  ρ_V(u, v) = Z̄_v(V)²/(Z̄_u(V)Z̄_{2v−u}(V)) (T13).
- Leakage quantities (00_COMMON §2): P_T, u_{T,l}, δ_{T,l} = u_{T,l}ᵀμ, Z_{T,l} = u_{T,l}ᵀε/σ, Δ_T = ‖(I − P_T)μ‖²/(n−1),
  v_T = σ² + Δ_T. Partial R²: x_{T,l} = (RSS_T − RSS_{T+l})/RSS_T.
- **Dilution fraction.** For a reference S° and block b, T_b := S° ∩ C_b and κ_b(S°) := Δ_{T_b}/v_{T_b} ∈ [0, 1).
  Under BO at S° = S₀, Δ_{T_b} is the signal energy outside block b; for every signal-free block κ_b = Δ_∅/v_∅ =
  R²_pop := ‖μ‖²/(‖μ‖² + (n−1)σ²), the population R² (on the data; in the Gaussian model it is the fixed-design R²).
- BO: X_{C_b}ᵀX_{C_b′} = 0 for b ≠ b′ (00_COMMON). SE-blk, BM-blk, R-lite as in W1-EXP. G, R, SE, BM-∞ as in 00_COMMON.
- Favourable regime: 1 − π₀(S₀) → 0 and 1 − π(S₀) → 0 in P₀-probability (T22(iii)/W1-EXP Thm 2 and T03).
  Masked regime: π₀(S₀) → 0 while π(S₀) → 1 (T27(i), Prop NM).

## W0. Three faces of the start discrepancy (deterministic; EX-A)

**Proposition W0.** For every data set and partition:

(i) π(S)/π₀(S) = e^{d(S)}/E_{π₀}[e^{d}] for all S ∈ Ω, with E_{π₀}[e^d] = Z̄₁/Z̄₀.

(ii) 1 + χ²(π‖π₀) = E_{π₀}[e^{2d}]/(E_{π₀}[e^d])² = Z̄₀Z̄₂/Z̄₁² = 1/ρ_Ω(0, 1). It is the reciprocal of the population ESS
fraction of one-step importance sampling from π₀ to π, and equals 1 + Var_{π₀}(w̄) for the normalised weight
w̄ = e^d/E_{π₀}e^d. (T13(i) with V = Ω, u = 0, v = 1.)

(iii) KL(π‖π₀) = E_π[d] − log E_{π₀}[e^d] ≤ log(1 + χ²(π‖π₀)); TV(π, π₀) ≤ √(KL/2). Lower bounds: for every S,
1 + χ²(π‖π₀) ≥ π(S)²/π₀(S); in particular ≥ π(S₀)²/π₀(S₀).

(iv) Let M := sup_S π(S)/π₀(S) = e^{max_Ω d}/E_{π₀}e^d < ∞. The independence move at φ = 1 (T09(ii)) is the Metropolised
independence sampler with proposal π₀; its second-largest eigenvalue is 1 − 1/M (Liu 1996, Thm 1) and
‖K^t(x, ·) − π‖_TV ≤ (1 − 1/M)^t (Mengersen and Tweedie 1996). In particular 1 + χ²(π‖π₀) ≤ M and M ≥ π(S₀)/π₀(S₀).

(v) (T11(iii)) P(S₀ absent from Q iid π₀ draws) = (1 − π₀(S₀))^Q; and π(S₀)/π₀(S₀) ≤ M.

So the draft's three correction mechanisms (importance weighting, MH, iid/SMC discovery) are the L², L^∞ and pointwise
norms of one ratio. **Status: PROVED** (definitions, T13(i), T09(ii), T11(iii), Liu 1996). Check: in the proxy-split run,
1 + χ² = 4.9·10⁴⁰ against the single-term lower bound π(S₀)²/π₀(S₀) = 4.4·10⁴⁰.

## W1. Exact structure of d under block orthogonality

**Lemma W1.** Assume BO. For S ∈ Ω write S_b = S ∩ C_b, c := 2b₀ + yᵀy = 2b₀ + n − 1, ξ_b := t_{S_b}/c ∈ [0, 1). Then
D_S = ∏_b D_{S_b}, t_S = Σ_b t_{S_b}, and

    d(S) = ν [ Σ_b log(1 − ξ_b) − log(1 − Σ_b ξ_b) ]  ≥ 0,

with d(S) = 0 iff at most one block has ξ_b > 0. Moreover, if the tables and the posterior are computed with a known
noise variance σ² (g-prior slab N(0, nσ²(G_S + I)⁻¹), no IG integration), then d ≡ 0 and π₀ = π exactly.

*Proof.* G_S and H_S are block diagonal under BO, so det H_S/det(G_S+I) and z_SᵀH_S⁻¹z_S split over blocks; log BF(S)
= −½ log D_S − ν log((2b₀ + Q_S)/(2b₀ + Q_∅)) and 2b₀ + Q_S = c(1 − Σ_b ξ_b). Subadditivity of log(1 − ·) on [0,1)
(concave, 0 at 0) gives ≥ 0 with the stated equality case. With known σ², log BF(S) = −½ log D_S + t_S/(2σ²), additive.
**PROVED.** Check: min_Ω d = 0 in all six BO runs; d(S₀) = 57.1 (n = 200) and 254.1 (n = 800) nats with one truth per
block; d(S₀) = 0 with both truths in one block.

*Consequence.* Under BO the entire discrepancy between the composite start and the posterior is the per-block
integration of σ² against the full-y residual (dilution). The draft's premise "small cross-block covariance ⇒ product ≈
posterior" is exact for known-σ² tables and false for v3's tables by a Θ(n) amount on models whose R² is spread over
two or more blocks.

## W2. The null log-odds gap is the dilution fraction times the posterior gain

**Lemma W2.** Assume BO and G. Fix S° ∈ Ω and l ∉ S° in block b, T := S° ∩ C_b. Then exactly

    LR_l := log[π(S°+l)/π(S°)] − log[π₀(S°+l)/π₀(S°)] = d(S°+l) − d(S°)
          = ν [ log(1 − x_{T,l}) − log(1 − x_{S°,l}) ],   x_{S°,l} = x_{T,l} · (2b₀ + Q_T)/(2b₀ + Q_{S°}),

(the determinant parts cancel under BO and the explained increment t_{S°+l} − t_{S°} = t_{T+l} − t_T). With
(2b₀ + Q_T)/(2b₀ + Q_{S°}) = v_T/v_{S°}·(1 + O_P(n^{−1/2})) and, at S° = S₀, v_{S₀} = σ²(1 + o_P(1)):

    LR_l = κ_b · G_l · (1 + o_P(1)),   G_l := −ν log(1 − x_{S₀,l}) = Z_{S₀,l}²/2 · (1 + o_P(1)),

uniformly over l ∉ S₀ on the EXP′ event of W1-EXP Thm 1 / W2-PREM Lemma U (the remainder of the expansion is the same
R on both sides and cancels up to the RSS-ratio term). **PROVED** up to the two uniform expansions, which are candidate
theorems. Check (n = 800): LR = 0.620 vs κG = 0.621; 1.050 vs 1.050; 0.429 vs 0.437; with κ = 0 (same block as all the
signal) LR = 0.000 exactly.

Sign and size: the posterior rewards a chance correlation Z² of a null with the full exponent Z²/2; the diluted table
rewards it with (1 − κ_b)Z²/2. Hence π/π₀ on S₀ + l is e^{κ_b Z²/2}·(1 + o(1)) relative to its value at S₀.

## W3. The cross-block covariance term (the draft's mechanism)

**Lemma W3 (PROOF SKETCH).** Drop BO. Let R_S = D_S + E_S with D_S block diagonal and E_S the cross-block correlations
among the members of S, and β̂_b := D_{S_b}⁻¹ρ_{S_b} the block-local standardised LS coefficients (ρ = correlations with
y). Then

    d(S) = d_BO(S) + (n/2) · Σ_{b≠b′} β̂_bᵀ E_{bb′} β̂_{b′} / (1 − R²_S) + O(n ‖E_S‖² ‖β̂‖²) + O(|S|/(nφ₀²)),

where d_BO is the expression of Lemma W1 evaluated at the block R²'s R²_{S_b} = ρ_{S_b}ᵀD_{S_b}⁻¹ρ_{S_b}, and the
last term is the determinant non-additivity (W1-EXP Lemma 1.2). The table side also acquires leakage: for a null l with
δ_{T,l} ≠ 0 the table gain is (δ_{T,l} + σZ)²/(2v_T) instead of σ²Z²/(2v_T) (T22(iii)'s family; CL(L) of W1-EXP).
*Sketch:* Neumann expansion of (D + E)⁻¹ in ρᵀ(D+E)⁻¹ρ, then −ν log(1 − R²) − Σ_b[−ν log(1 − R²_b)] as in W1.
**Status: PROOF SKETCH.** This is the draft's "divergence controlled by cross-block covariance", now a second additive
term beside dilution, first order in E_S and scaled by n.

## W. One-step weight stability in the favourable block-orthogonal regime

**Theorem W.** Assume G, BO, SE-blk(φ₀), BM-blk, R-lite (p ≤ n^A, ‖μ‖² ≤ Mn), s₀ fixed, the v3 blocks (|C_b| ≤ B ≤ 16), and
that the signal occupies at most s₀ blocks (automatic). Let R² := R²_pop ∈ (0, 1) be fixed. Then:

(a) [lower bound, PROVED modulo W2] For every ε > 0, with P₀-probability → 1,
    1 + χ²(π‖π₀) ≥ p^{R² − ε} n^{−1/2}.

(b) [upper bound, PROOF SKETCH] For every ε > 0, with P₀-probability → 1,
    1 + χ²(π‖π₀) ≤ 1 + p^{R² + ε} n^{−1/2} + o(1).

(c) [expected sharp form, CONJECTURE] log(1 + χ²(π‖π₀)) = [R² log p − ½ log n]₊ + O_P(log log p).

Equivalently the one-step ESS fraction ρ_Ω(0, 1) → 1 if R² log p − ½ log n → −∞ and → 0 if it → +∞. KL(π‖π₀) and
TV(π, π₀) are O_P(n^{−1/2}·polylog) throughout (Prop W4), so the dichotomy is invisible to KL and TV.

*Proof skeleton.*
1. (Concentration.) W1-EXP Thm 2 (candidate; verbatim corollary of locked T22(iii) with η = 0 per W3-VEXP) gives
   1 − π₀(S₀) = O_P(2^B√(log n) n^{−1/2}); under BO, SE follows from SE-blk (R_T block diagonal), so locked T03 gives
   1 − π(S₀) = O_P(√(log n/n)). Hence π(S₀)²/π₀(S₀) = 1 + O_P(2^B√(log n)n^{−1/2}).
2. (Layer decomposition.) 1 + χ² = Σ_S π(S)²/π₀(S) = [S₀ term] + Σ_{l∉S₀} π(S₀+l)²/π₀(S₀+l) + Σ_{j∈S₀} π(S₀−j)²/π₀(S₀−j)
   + (rest). By W2 the single-null layer is Σ_l π(S₀)² a_l · e^{LR_l}/π₀(S₀) with a_l = π(S₀+l)/π(S₀) =
   [(s₀+1)/(2p−1−s₀)]·(n+1)^{−1/2}·e^{G_l + R}, so each term is ≍ p^{−1}n^{−1/2}e^{(1+κ_b)Z_l²/2}.
3. (Extreme values, lower bound.) The nulls of the signal-free blocks number ≥ p − s₀B and have κ_b = R². Their
   Z_l = x_lᵀε/(σ‖x_l‖) are jointly Gaussian with unit variance, independent across blocks (BO) and at most B-dependent
   within a block. Hence max_l Z_l² ≥ (2 − ε) log(p/B) w.p. → 1, giving one term ≥ p^{−1}n^{−1/2}p^{(1+R²)(1−ε)} and (a).
4. (Heavy-tailed sum, single layer.) e^{(1+R²)Z²/2} has tail P(· > t) ≍ t^{−1/(1+R²)}(log t)^{−1/2}, index α = 1/(1+R²) < 1,
   so the sum over ≈ p such terms is p^{1+R²}·L(p) for a slowly varying L, w.p. → 1 (truncate at p^{(1+R²)(1+ε)} and use
   the union bound over the ≤ p/B independent blocks, as in W3-VEXP; never take expectations: E e^{(1+R²)Z²/2} = ∞).
   Blocks that carry signal have κ_b ≤ R² and at most s₀B nulls; they contribute less.
5. (Other layers, the crux.) Deletions: π(S₀−j)²/π₀(S₀−j) ≤ π(S₀−j)·[π(S₀−j)/π(S₀)]/[π₀(S₀−j)/π₀(S₀)] and the bracket
   ratio is ≤ 1 because the posterior gain of a truth exceeds its diluted table gain; the layer is ≤ 1 − π(S₀) → 0.
   Multi-extra supersets S₀ ∪ E: under BO and up to the σ-coupling, the term factorises over blocks into products of
   single-null factors times a prior factor ≤ ((s₀+e)/(2p−s₀−e))^e; summing with T22(i)'s machinery (a⁽²⁾_{bj} :=
   Σ_{|U∖U*_b|=j} [posterior odds]²/[table odds], D⁽²⁾_b = max_j (j! a⁽²⁾_{bj})^{1/j}, q⁽²⁾ = (p−s₀)⁻¹Σ_b D⁽²⁾_b) gives
   Σ_{E≠∅} ≤ (1 − q⁽²⁾)^{−(s₀+1)} − 1 ≈ (s₀+1)q⁽²⁾ when q⁽²⁾ < 1, and q⁽²⁾ ≍ p^{R²}n^{−1/2}·L(p). Models missing a truth and
   carrying extras: multiply the deletion factor (→ 0 exponentially under BM-blk) by the extras factor. Hence (b).
   *Crux:* the second-moment aggregation lemma (the T22(i) proof with squared posterior odds in the numerator) and the
   control of the σ-coupling across extras in different blocks (Lemma W1 with the added ξ's: the coupling only increases
   d, i.e. increases π relative to π₀, so it must be bounded above on the extras layer; e.g. by e^{νΣ_{b<b′}ξ_bξ_{b′}/(1−Σξ)}
   with the extras' ξ's of order Z²/n).
6. (c) follows from the sharp extreme-value constant in step 4.

*What is true at finite n.* The formula is asymptotic. In the p = 12 check at n = 200 with one truth per block the
posterior itself is not concentrated (π(S₀) = 0.21) and 1 + χ² = 19.6 (ESS 5%) comes mostly from two-extra models; at
n = 800 all BO runs have 1 + χ² ≤ 1.03, as the formula predicts for p = 12. At the study design (R² ≈ 0.9, p = 500,
n = 200) the bracket in (c) is 5.5 − 2.6 = 2.9 nats: one-shot correction would have ESS ≈ 5% *even with a favourable
start*; the actual start is dilution-masked, adding ≈ 28 nats (W3-VEXP).

## W′. Stage count of the ideal adaptive grid (favourable BO regime)

**Conjecture W′.** Under the hypotheses of Theorem W, let the ideal grid be: from u, take the largest v ≤ 1 with
ρ_Ω(u, v) ≥ 0.9 (60 halvings), until v = 1. Let g := log(√n/9)/(R² log p). Then w.p. → 1 the number of stages is

    T_ideal = ⌈log₂(1 + 1/g)⌉ + O(1)   if g > 0,   and T_ideal = 1 if g ≥ 1;

in particular T_ideal = O(1) whenever p ≤ n^A (since 1/g ≤ 2AR²/(1 − 2 log 9/log n)).

*Skeleton.* q_φ(S₀+l)/q_φ(S₀) = a_l^φ(a⁰_l)^{1−φ} ∝ n^{−1/2}e^{(1 − κ(1−φ))Z_l²/2}, so by the layer argument of Theorem W,
χ²(q_v‖q_u) ≍ p^{κ(2v−u−1)}n^{−1/2}·L(p) with the T13 point w = 2v − u governing. The acceptance rule χ² ≤ 1/9 reads
w ≤ 1 + g, i.e. 1 − v_t = (1 − v_{t−1} − g)/2: the remaining gap halves and loses g per stage; it reaches 0 after
⌈log₂(1 + 1/g)⌉ stages. Obligations: (1) the bisection returns the largest passing endpoint up to 2^{−60}, so
monotonicity of v ↦ ρ_Ω(u, v) on the relevant range is needed (true in the two-point limit; OPEN in general);
(2) the method's grid is the V-restricted construction from pilot temperatures, not the ideal grid: ρ_V = ρ_Ω under
COVER at the points u, v, 2v − u (T13(ii)); the relation between the pilot's population ESS and ρ_Ω is a sampling
statement (OPEN, V12-type). *Payoff:* W′ is exactly the input W2-T26 Theorem B lacks: with T_n = O(1),
(T_n + 1)Δ_n → 0 follows from Δ_n → 0 and JRSS-B Thm 6 becomes non-vacuous on the BO family with p ≤ n^A.
Check: T_ideal = 1 in all BO runs at n = 800 (p = 12, g ≫ 1), 6 at n = 200 with one truth per block, 2 with both in
one block. **Status: CONJECTURE** (PROOF SKETCH for the recursion given the χ² law).

## W″. A masked-regime crossing costs a bounded number of stages

**Proposition W″ (two-state part).** Let the bridge be restricted to two states {S°, S₀} with log-odds
log[q_φ(S₀)/q_φ(S°)] = c₀ + φD, D = d(S₀) − d(S°). Then Var_{q_φ}(d) = D²a_φ(1−a_φ) with a_φ = q_φ(S₀), and

    ∫₀¹ sd_{q_φ}(d) dφ → π   as D → ∞   (exactly ∫_{a_0}^{a_1} da/√(a(1−a)) ≤ π),

independent of D. With small steps, χ²(q_{φ+Δ}‖q_φ) = Δ²Var_{q_φ}(d)(1 + o(1)), so the ESS-0.9 rule (Δ·sd ≤ 1/3) needs
≈ 3π ≈ 9.4 stages across the crossing whatever the size of the odds gap D (Θ(n) in Prop NM; c log p + (c/2) log n +
Θ(n) under T27). **PROVED** (calculus; d²/dφ² log Z̄_φ = Var_{q_φ}(d)). Check: 14 and 16 stages in the proxy-split
runs, where the window is not exactly two-state.

**Conjecture (window form).** If the bridge is pair-dominated on a window (PD of METHODOLOGY V11) the ideal grid spends
3π + O(1) stages in the window and the Theorem W count outside it. Together with T13(iii) (the restricted grid sees
the crossing iff the pair is in V) this is the quantitative content of the candidate-grid design: *weight* stability
in the masked regime is cheap; *finding* the window (V) and *occupying* S₀ (delivery, T38(b)) are the hard parts.
**Status: CONJECTURE.**

## W4. Divergence versus weight variance

**Proposition W4 (PROOF SKETCH).** In the favourable BO regime of Theorem W,
    KL(π‖π₀) ≤ (1 − π₀(S₀))(1 + o(1)) + Σ_{l∉S₀} π(S₀+l)·LR_l = O_P(2^B√(log n) n^{−1/2}·polylog p),
    TV(π, π₀) ≤ (1 − π(S₀)) + (1 − π₀(S₀)) = O_P(2^B√(log n) n^{−1/2}),
while log(1 + χ²(π‖π₀)) = [R² log p − ½ log n]₊ + O_P(log log p). *Sketch:* W0(iii) with E_{π₀}e^d ≥ π₀(S₀)e^{d(S₀)}; the
null layer of E_π[d − d(S₀)] has summands p^{−1}n^{−1/2}e^{Z²/2}·κZ²/2 whose sum is p^{0}n^{−1/2}·L(p) (tail index 1: no
polynomial growth). Thus the draft's "divergence small ⇒ weights stable" is false in the χ² sense that matters for
importance sampling; the content of §5.3 is entirely in the step from KL/TV to χ².

## W5. Remark: dilution and leakage pull in opposite directions

Under BO (no leakage) the null tables' exponent is lowered from Z²/2 to (1 − κ_b)Z²/2: this makes E e^{(1−κ)Z²/2} finite
and is what W1-EXP Thm 6 (SPREAD) uses to concentrate the start at rate n^{−1/2} without the √(log n); the same
lowering inflates π/π₀ on nulls (Lemma W2) and drives Theorem W. Leakage (δ_{T,l} ≠ 0) raises the table exponent to
(δ + σZ)²/(2v_T): it hurts start concentration (NL_avg of T22(iii)) and lowers π²/π₀ on those nulls (helps χ²) until it
is large enough to move π₀'s mode, when the S₀ term explodes instead. The block partition therefore trades delivery
against weight stability; this is the precise form of the draft's §4.4 "sensitivity to block construction".

## NM. Naive merge fails (the draft's §3.2, rigorous)

**Proposition NM.** Assume G with σ² > 0. Let S₀ = {j} with θ_j = θ ≠ 0 fixed, and let ℓ ≠ j satisfy r := r_{jℓ} with
0 < |r| < 1 and x_ℓ ⊥ x_k for all k ∉ {j, ℓ} (a pure proxy); the other columns are arbitrary with λ_min(R_T) ≥ φ₀² on the
sets used. Let the partition separate j and ℓ (b(j) ≠ b(ℓ)). Write BF_b for the block-b table law π_b(U) ∝ w(|U|)r_b(U) on
U ⊆ C_b (the draft's local posterior). As n → ∞ with p ≤ n^A, with P₀-probability → 1:

(i) [local analyses] π_{b(j)}(j ∈ U) → 1 and π_{b(ℓ)}(ℓ ∈ U) → 1; precisely
    log r_{b(ℓ)}({ℓ}) = (n/2) log[1/(1 − r²θ²/(σ²+θ²))] − ½ log n + O_P(1) → +∞ linearly in n.
    Hence the naive union Ŝ_∪ = {j, ℓ}.

(ii) [the composite start inherits it] By T22(ii-a) exactly, π₀({j,ℓ})/π₀({j}) = [w(2)/w(1)]·r_{b(ℓ)}({ℓ}) =
    (2/(2p−2))·r_{b(ℓ)}({ℓ}) → ∞; so π₀({j}) → 0 and π₀(j, ℓ ∈ S) → 1 (double counting).

(iii) [the posterior does not] π({j,ℓ})/π({j}) = (2/(2p−2))·(n+1)^{−1/2}e^{Z²/2 + O_P(1)} → 0, where Z is the standardised
    residual correlation of x_ℓ on x_j with ε (δ_{{j},ℓ} = 0 since (I − P_j)μ = 0), and
    π({ℓ})/π({j}) = exp{−(n/2) log(1 + θ²(1 − r²)/σ²)(1 + o_P(1))} → 0 (the look-alike margin; linearised it is T37's
    (n−1)θ²(1−r²)/(2σ²)). With T03 (or directly) π({j}) → 1, PIP_ℓ → 0.

(iv) [uncertainty distortion] |π_{b(ℓ)}(ℓ ∈ U) − PIP_ℓ| → 1; |π₀(j,ℓ ∈ S) − π(j,ℓ ∈ S)| → 1; TV(π, π₀) → 1;
    1 + χ²(π‖π₀) ≥ π({j})²/π₀({j}) = exp{(n/2) log[1/(1 − r²θ²/(σ²+θ²))] (1 + o_P(1))}, so by Prop W0 one-shot importance
    correction, independence-MH from π₀ and iid discovery from π₀ all fail at every polynomial budget.

(v) [the correction is cheap] S₀ = {j} is at Hamming distance 1 from the start mode {j, ℓ}: in every terminal round at
    φ = 1 the Gibbs label of ℓ scores {j} (SR), with probability ≥ a₁({j,ℓ}) (W1-T24G Cor. P1; a₁ ≥ 0.14 at n = 200 in
    the p = 20 designs), and by W″ the ideal grid crosses from {j,ℓ} to {j} in O(1) stages.

*Proof.* (i) r_{b(ℓ)}({ℓ}) = BF({ℓ}) = (n+1)^{−1/2}(1 + O(1/n))·(1 − x_{∅,ℓ})^{−ν}, x_{∅,ℓ} = r_{ℓy}² → r²θ²/(σ²+θ²) > 0;
the prior ratio w(1)/w(0) = 1/(2p−1) costs log(2p) ≤ A log n + log 2. (ii) is T22(ii-a) with S° = {j}, S = {j,ℓ}
(the identity holds for any two models, not only S₀). (iii) EXP′ at T = {j} with δ = 0 (W1-EXP Thm 1 or W2-PREM Lemma U,
candidates; or the direct χ²₁ computation since the design is fixed), and the two-model comparison BF({ℓ})/BF({j}) =
[(1 − r_{ℓy}²)/(1 − r_{jy}²)]^{−ν}·(1 + O(1/n)) with r_{jy}² → θ²/(σ²+θ²), r_{ℓy}² → r²θ²/(σ²+θ²). (iv) from (ii)–(iii) and
W0(iii)–(v). (v) from SR and W1-T24G Cor. P1 (candidate), and W″. **Status: PROVED** modulo the cited candidates; a
fully self-contained finite-n version is available because every quantity is a closed form in (r_{jy}, r_{ℓy}, r, n, p).
Check: proxy-split runs give argmax π₀ = {1,7}, argmax π = {1}, π₀({1}) = 1.7·10⁻⁴¹ (n = 200) and 1.0·10⁻¹⁴⁶ (n = 800),
π({1}) = 0.86 and 0.95, TV = 0.985 and 0.996, 1 + χ² = 4.9·10⁴⁰, T_ideal = 14 and 16.

*Not implied by T06/T07/T27.* T06(iii) is the |r| = 1 limit; T07(i) is the posterior-side swap ceiling; T27(i) is
undercounting by cancellation. NM is overcounting by double counting; (ii) is a corollary of T22(ii-a).
*Where v3 meets it.* The method's complete-linkage partition separates a pair with |r| near 1 only when the cluster
containing it exceeds B (then the top-down cut splits it); the proposition should be stated for an arbitrary separating
partition, with that remark. The empirical instance is W1-T24G's S3/S4/S6 start modes at p = 20, B = 4.

## P. The partition as a random variable

**Proposition P.** (i) [validity is partition-free; PROVED] For any partition 𝒫 of [p] into blocks of size ≤ K and any
positive tables, T09, T12, T13, T21, T22(i)(ii)(iv) and T31(i) hold with 𝒫 in place of the method's partition
(their proofs use only the product form of γ₀, γ₀ > 0 and the move definitions; T22(i)'s statement already quantifies
over all partitions and positive tables). Hence if 𝒫 is drawn from any law Λ measurable with respect to (X, y) and
streams 0–9, all of them hold conditionally on 𝒫 and E[Ẑ] = Σ_𝒫 Λ(𝒫)E[Ẑ | 𝒫] = Z. The target π does not depend on 𝒫.
Therefore "the partition as a random variable to be inferred" is not an inference about the model; it is an adaptation
of the start (like the schedule), and its objects are π₀^𝒫(S₀) (delivery), the dilution fractions κ_b(𝒫) and the
leakages δ_{T,l}(𝒫) (weight stability; Theorem W, Lemma W3), and Z̄₀^𝒫.

(ii) [mixture start; PROVED, elementary] For partitions 𝒫₁..𝒫_m and weights λ_i > 0, Σλ_i = 1, let
π₀^{mix} := Σ_i λ_i π₀^{(i)}. Then: π₀^{mix} is exactly samplable (draw i, then the backward sampler of T09(i));
its density is π₀^{mix}(S) = Σ_i λ_i γ₀^{(i)}(S)/Z̄₀^{(i)} (m table lookups and the m exact normalisers); the bridge
γ_φ := (π₀^{mix})^{1−φ}(ϖBF)^{φ}·const with d^{mix}(S) = log(ϖ(S)BF(S)) − log π₀^{mix}(S) ends at π, and every move of
T09(ii) with the independence proposal from π₀^{mix} is q_φ-invariant (T09's proof uses only exact sampling and an
evaluable density). Moreover π₀^{mix}(S₀) ≥ max_i λ_i π₀^{(i)}(S₀) and sup_S π/π₀^{mix} ≤ min_i λ_i⁻¹ sup_S π/π₀^{(i)}, so
one favourable partition in the mixture bounds the iid discovery budget of T11(iii) by that partition's budget times
1/λ_i, and the independence-sampler rate (W0(iv)) likewise. Cost: m times the table and convolution work of §6.3.
This is the draft's "multiple random partitions" (§8.4) and a method extension not in the 2,400 fits (investment rule);
it is the natural companion of T39 and of W3-VEXP's finding that packing both hubs of a linked pair into one block
removes the LH masking.

(iii) [stochastic scheduling; PROVED by T12] An adaptive schedule is valid iff it is frozen before the final run's
randomness (CAL); T12(iv) shows that a state-dependent stopping rule inside the final run breaks E[Ẑ] = Z. v3's
calibration plus frozen final run is exactly this.

## H. Remark: general h(θ)

For bounded h of (S, β_S, σ²), E_π[h] = Σ_S π(S) E[h | S, y] with the conjugate normal–inverse-gamma conditional in
closed form; recording h̄(S) := E[h | S, y] at the T12 recording positions gives E[Ẑ_r·ĥ_r] = Z·E_π[h] by the same proof
as T12(i) (h̄ is a bounded function of the state). v3 reports no such h; the draft's §13.1 is covered for h = 1{j ∈ S}
(PIPs) and h ≡ 1 (Z) by T12, T23(ii), W2-T26 Theorem A, and extends in one line otherwise. **PROVED** (one line).

## Summary of statuses

| Label | Statement | Status |
|---|---|---|
| W0 | three faces of π/π₀ (χ², sup ratio, π₀(S₀)) | PROVED |
| W1 | exact d under BO; known σ² ⇒ π₀ = π | PROVED |
| W2 | LR_l = κ_b·G_l | PROVED modulo EXP′ (candidate) |
| W3 | cross-block covariance term | PROOF SKETCH |
| W(a) | 1 + χ² ≥ p^{R²−ε}/√n | PROVED modulo W2 |
| W(b) | 1 + χ² ≤ 1 + p^{R²+ε}/√n + o(1) | PROOF SKETCH (crux: second-moment aggregation) |
| W(c) | sharp log log form | CONJECTURE |
| W′ | ideal grid stage count ⌈log₂(1 + 1/g)⌉ + O(1) | CONJECTURE (skeleton) |
| W″ | crossing costs ≈ 3π stages | two-state PROVED; window CONJECTURE |
| W4 | KL, TV small while χ² large | PROOF SKETCH |
| W5 | dilution vs leakage trade-off | remark |
| NM | naive merge overcovers; start inherits; posterior does not; correction is one flip | PROVED modulo T03/EXP′/Cor. P1 |
| P | partition: validity-free, mixture start, stochastic scheduling | PROVED |
| H | general h | PROVED |

References outside the project: Liu, J. S. (1996) Metropolized independent sampling with comparisons to rejection
sampling and importance sampling, *Statistics and Computing* 6, 113–119; Mengersen, K. L. and Tweedie, R. L. (1996)
Rates of convergence of the Hastings and Metropolis algorithms, *Ann. Statist.* 24, 101–121; Del Moral, Doucet and
Jasra (2006) as in the draft.
