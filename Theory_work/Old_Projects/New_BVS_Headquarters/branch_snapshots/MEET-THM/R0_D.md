# Round 0, Seat D (fresh-eyes Fable 5.1, Claude Personal, high): theory plan from the method alone

Verbatim copy of /home/fb31/fresh_eyes/fable/THEORY_PLAN.md (thread completed 2026-11-04 01:10 UTC). The author saw only the method packet (METHOD_v3 §§1–8 with theory references removed, a v3.1 additions sheet, the v3 code, and BRIEF.md); no prior theory work. Everything in it is the author's proposal or PROOF SKETCH, unchecked.

---

# THEORY_PLAN.md — a fresh-eyes theory plan for SMC-BVS v3.1

**Status of everything below:** proposal. Every "theorem" is a *candidate* with a *proof sketch by me, unchecked*.
Nothing here has been refereed, formalised or checked against the project's existing theory, which I was not shown.
Where I say "known" I cite only results I am confident exist in the stated form; where I am not sure, I say so.

**What I read:** `METHOD_v3.md` (sections 1–8), `METHOD_v3.1_ADDITIONS.md`, and the v3 code (`cpp/v3_engine.h`,
`v3_start.h`, `v3_calib.h`, `v3_blocks.h`, `v3_score.h`, `v3_ledger.h`, `v3_calib.R`, `v3_run.R`, `README.md`).
Where the code pins down a detail the prose leaves open (e.g. Gibbs records `o_j` before the draw; `rb_acc` is averaged
over `N·Hm`; the ledger offers models to the stores only on fresh evaluations; the grid validates `rho_V ≥ 0.9` at every
appended point; multinomial resampling after every stage including the terminal one) I use the code's version.

**What I ran (one core, under a minute each; scripts and output reproduced in Appendix A):**
(SC1) a numerical check that, with exactly orthogonal blocks, the discrepancy d(S) equals a closed-form σ²-coupling
term for every model up to size 5 (agreement 5·10⁻¹⁴); (SC2) the exact ESS-0.9 bisection rule of `v3_calib.h`
applied to synthetic two-state, three-state and Gaussian-spread bridges, to see how the stage count scales.
SC2 changed my mind about one thing: a two-model dominance crossing costs ≈ log₂(gap) + 7 stages, not a constant, while
smooth spreads follow the thermodynamic-length prediction T ≈ 3.08·∫₀¹ sd_φ(d) dφ closely. Both facts are used below.

---

## 0. Notation and conventions used throughout

| Symbol | Meaning |
|---|---|
| 𝕊_K | model space {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋) |
| F(S) | log ϖ(S) + log m(S), the score; HPM = argmax F over the scored set |
| BF(S) | m(S)/m(∅); log BF(S) = −½[log det H_S − log det(G_S+I)] − ν log((2b₀+Q_S)/(2b₀+yᵀy)), ν = a₀ + n/2 |
| γ₀, Z̄₀, π₀ | composite start γ₀(S) = ϖ(S)∏_b r_b(S∩C_b); Z̄₀ = Σ_{𝕊_K} γ₀; π₀ = γ₀/Z̄₀ |
| d(S) | discrepancy log BF(S) − Σ_b log r_b(S∩C_b); γ_φ = γ₀e^{φd}; Z_φ = Σ γ_φ; π_φ = γ_φ/Z_φ; Z = m(∅)Z₁ |
| Δ_b(U), u_b(S) | Δ_b(U) = n z_UᵀH_U⁻¹z_U (fit of the block-local model U ⊆ C_b); u_b(S) = Δ_b(S∩C_b)/(2b₀+yᵀy) ∈ [0, 1) |
| d_σ(S) | −ν[log(1 − Σ_b u_b(S)) − Σ_b log(1 − u_b(S))] ≥ 0 (the σ²-coupling term, Prop. ST2) |
| d_X(S) | d(S) − d_σ(S) (the cross-block correlation term; ≡ 0 under orthogonal blocks) |
| χ²_t, ρ_t | χ²(π_{φ_t} ‖ π_{φ_{t−1}}); ρ_t = 1/(1+χ²_t) = population ESS fraction of the stage-t weights (Lemma BR1) |
| Λ | thermodynamic length ∫₀¹ sd_{π_φ}(d) dφ; Λ_V the same under the V-restricted laws |
| J(π₀, π) | Jeffreys divergence E_π d − E_{π₀} d = ∫₀¹ Var_{π_φ}(d) dφ (Lemma ST10) |
| M_φ | max_S π_φ(S)/π₀(S) = e^{φ d_max} Z̄₀/Z_φ ≤ exp{φ(d_max − E_{π₀}d)} |
| m, Q_φ | m = p + B + 2 labelled steps; Q_φ = the random-order round kernel at temperature φ |
| T, T_cal | number of bridge stages of the frozen grid; total stages run in calibration |
| S₀, s₀, β_min | true support, its size, the smallest standardised true coefficient (selection results only) |
| "perfect mixing" | the idealisation in which every round returns an exact π_φ draw (used only for sharp constants) |

Objectives (PI's order): **O1** posterior accuracy (Z, PIPs, joint inclusion, general h); **O2** parallel scalability over
particles/islands; **O3** selection accuracy, in particular under correlated designs.

Difficulty words: *routine* (a competent PhD student, days), *substantial* (weeks, new lemmas), *hard* (open-ended).
"Lean core" names the finite/combinatorial/algebraic part that could be certified; the rest rests on cited probability.

---

## 1. Component × property map

Cell entries: candidate-result IDs (defined in §2–§3), or "—" with a one-line reason. The columns are the properties the
brief asks for; "corr/mask" = behaviour under correlation and masking; "depth" = stage count / sequential depth.

| Component | exact / valid at fixed data | unbiased | consistent in N | consistent in R | finite-sample bound | corr / mask | depth | work / memory | selection n,p→∞ | finite-n selection | impossibility | vs split-merge / MCMC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Preprocessing (drop, standardise, duplicates) | TG1 (invariances) | — not an estimator | — | — | NU1 (rounding) | PI4 (duplicates split mass) | — | PA3 | — | — | NG9 (fixed-seed equivariance fails) | — |
| Target posterior & prior | TG1 (propriety), TG2 (reduction, IG bound), TG3 (monotonicity) | — | — | — | TG5 | TG4 needs RE conditions | — | — | TG4 | TG5 | NG8 (HPM NP-hard) | — |
| Exact branch | HP1, HP6 (global certificate) | exact | exact | exact | NU1 | none needed | — | ST6-type count | TG4 applies directly | TG5 | — | trivially dominates |
| Blocks (clustering, cut, packing) | ST5, ST6 | — deterministic | — | — | ST6 (J ≤ 2⌈p/B⌉) | ST5 (ε-separation) | — | ST6, NG10 (Ω(p²)) | — | — | NG10 | — |
| Tables & composite start π₀ | ST1 (exact Z̄₀, exact sampler, DP mode) | — | — | — | ST2, ST4 (size of d) | ST2, ST7 (within-block masking free), ST9 (cross-block exploration) | ST2→BR3 | ST6 | ST8/HP4 (start mode) | HP4 | NG1 (cross-block masking) | ST10 (π₀ *is* split-and-merge's answer) |
| Neighbour graph | KN1 (Hastings ratio) | — | — | — | KN6 | KN6 | — | O(p² log p) | — | — | — | — |
| Gibbs step (with cap) | KN1 | — | — | — | — | — | — | 1 score | — | — | — | — |
| Uniform / neighbour swap | KN1 | — | — | — | — | KN5 (proxy swaps) | — | 1 score | — | — | — | — |
| Independence proposal | KN1, KN4 (Doeblin) | — | — | — | KN4 (explicit TV rate) | KN4 (M_φ), NG1 | — | 1 score | — | — | NG1 | PA6 |
| Round kernel Q_φ | KN2 (self-adjoint, invariant) | — | — | — | KN3 (gap ≥ ½ mixture), KN4 | KN5 (rapid mixing at φ=1) | PA1 (m per round) | PA1 | — | — | — | KN5 |
| Resampling (multinomial) | EV1 | EV1 | PI1 | — | EV2–3 | — | O(log N) parallel | PA1 | — | — | — known: higher variance than stratified (Douc et al. 2005) | — |
| Pilot schedule (adaptive ESS) | BR2, BR6 | — adaptive: NG6 | — | — | BR3, BR4 | BR4 (crossings) | BR3, BR4, NG5 | T_e cap | — | — | NG4, NG6 | — |
| Candidate set V & grid | BR1, BR5 | — deterministic given V | — | — | BR1 (coverage), CL5 | NG4 | BR3, BR4 | ≤ 60·|V|·T_e lse | — | — | NG4 | — |
| Rebuild loop, checks, escalation | CL1, CL2 | — | — | — | CL3 (power of E1–E3) | NG1, NG12 | CL1 | CL1 | — | — | NG1, NG12 | — |
| Final islands (bridge + terminal rounds) | EV1, KN7 | EV1 | PI1, EV4 (CLT) | EV1 | EV2, EV3 | KN4, KN5 | PA1 | PA1 | — | — | NG1 | PA5 |
| Stacking (R′ islands) | PA4 | PA4 | PA4 | PI2 | PA4 | — | PA4 (depth constant) | PA4 | — | — | — | PA4/PA5 |
| Local search & LS0 | HP2 | — deterministic | — | — | HP3 | HP3, NG11 | ≤ (ℓ+1) scans | HP2 | HP4 | HP4 | NG11 | HP4 (mixing-free) |
| HPM / MPM decisions | HP1, PI4 | — | HP1+PI1 | — | HP3, PI4 | PI4 (duplicates) | — | — | TG4+HP4 | TG5 | NG7, NG8 | — |
| PIP poolings (Ẑ-weighted, equal) | PI1 | PI2 (Ẑ·PIP unbiased) | PI1 | PI2 (Ẑ-weighted only) | PI3 | — | — | — | — | — | NG2 (equal weight) | — |
| General-h summaries | PI1 | PI2 | PI1 | PI2 | PI3 | PI4 (cluster-level h) | — | O(N·|𝓗|) | — | — | — | — |
| Evidence estimator | EV1, EV7 | EV1 | EV4 | EV1 | EV2, EV3, EV5 | KN4 (M_φ in EV3) | BR3 | — | — | — | EV6 (log Ẑ biased), NG3 | BR7 (TI by-product), ST10 |
| Run card (Z_𝒯, gaps, BnB) | EV5, HP6 | — | — | — | EV5 | — | — | declared budget | — | — | NG3 (one-sided only) | — |
| Parallel layer | PA2 (bitwise identity) | — | — | — | — | — | PA1 | PA1, PA3 | — | — | PA1 (depth Ω(T·m)) | PA5 |
| Numerics (Cholesky, lse, fallbacks) | NU1 | — | — | — | NU1 | — | — | — | — | — | — | — |

---
## 2. Candidate theorems

Format for each item: **ID. Name.** *Statement* (draft, with hypotheses) · *Guarantee / objective* · *Known or new* ·
*Proof route (key lemma)* · *Difficulty* · *Lean core / cited probability* · *Depends on*.

### 2.1 TG — the target posterior

**TG1. Propriety, boundedness and invariance of the target.**
*Statement.* For every real X (n×p, n ≥ 2, columns not constant) and every y with ‖Cy‖ > 0, and every S ∈ 𝕊_K:
(a) H_S = (n+1)G_S + I ≻ 0 and G_S + I ≻ 0, so log m(S) is finite even when X_S is rank-deficient;
(b) Q_S ≥ yᵀy/(n+1) > 0, hence log m(S) ≤ log C_n − ν log(2b₀ + yᵀy/(n+1));
(c) 0 ≤ log BF(S) ≤ ν log((2b₀+yᵀy)(n+1)/(2b₀(n+1)+yᵀy)) ≤ ν log(n+1), and the det term lies in [−|S|·½log(n+1), 0];
(d) the standardised data, hence π(·|y), Z/m(∅) and all PIPs, are invariant under y ↦ ay + b1 (a ≠ 0) and under
x_j ↦ a_j x_j + b_j 1 (a_j ≠ 0), and equivariant under column permutations.
*Guarantee.* The target is a legitimate finite probability law for every input the preprocessing passes (O1, O3).
*Known/new.* Routine facts; (b) is stated in the method report without proof.
*Proof route.* (a) positive definiteness of the ridge; (b) z_SᵀH_S⁻¹z_S ≤ z_Sᵀ((n+1)G_S)⁺z_S = yᵀP_Sy/(n+1) ≤ yᵀy/(n+1)
by Loewner monotonicity of inversion; (c) from (b) and det(H_S)/det(G_S+I) ∈ [1, (n+1)^{|S|}] by eigenvalue interlacing of
(n+1)λ+1 versus λ+1; (d) algebra of C and D_x.
*Difficulty.* Routine. *Lean core.* All of it (finite-dimensional linear algebra; Mathlib has Loewner order and Cholesky-free
determinant facts). *Depends on.* Nothing.

**TG2. Reduction identity and the IG-prior bound.**
*Statement.* (a) The working posterior over S equals the posterior of the contrast regression Uᵀy^r on UᵀX with n−1 Gaussian
errors, slab θ_S | v, S ~ N(0, n v (G_S+I)⁻¹) and v ~ IG(a₀ + ½, b₀ s_y²), as stated in §5 of the method.
(b) For any two models, |[log m(S₁) − log m(S₂)] − [log m⁰(S₁) − log m⁰(S₂)]| ≤ 2νb₀|1/Q_{S₁} − 1/Q_{S₂}|, where m⁰ is the
same score with b₀ = 0 (improper limit), so the proper IG prior changes any pairwise comparison by at most
≈ n b₀ |1/Q₁ − 1/Q₂| ≤ n b₀ (n+1)/yᵀy.
*Guarantee.* The "evidence" is the evidence of a well-defined, intercept-integrated model; the proper noise prior is a
negligible perturbation of comparisons (O1).
*Known/new.* (a) standard (integrating an intercept = contrasts); (b) elementary.
*Proof route.* (a) orthogonal change of variables; (b) log(1 + 2b₀/Q) is 2b₀/Q-Lipschitz in 1/Q.
*Difficulty.* Routine. *Lean core.* (b) completely; (a) the algebraic identity. *Depends on.* TG1.

**TG3. Monotonicity of the fit and a superset bound (the leaps-and-bounds lemma).**
*Statement.* For S ⊆ S′ ∈ 𝕊_K: (a) Q_{S′} ≤ Q_S; (b) log det H_{S′} − log det(G_{S′}+I) ≥ log det H_S − log det(G_S+I);
(c) hence for every S′ with S ⊆ S′ ⊆ S ∪ R,
F(S′) ≤ max_{|S|≤k≤|S∪R|} log ϖ(k) + log C_n − ½[log det H_S − log det(G_S+I)] − ν log(2b₀ + Q_{S∪R}).
*Guarantee.* A computable upper bound on every score in a region from two scores; this makes the run card's optional
branch-and-bound a *proof* of regional optimality (O3) and gives `global_certified`-style certificates outside the exact branch.
*Known/new.* (a)–(c) are the classical Furnival–Wilson (1974, Technometrics, "Regressions by leaps and bounds") idea
adapted to this score; the ridge and the det term need a two-line extra argument.
*Proof route.* (a) z_SᵀH_S⁻¹z_S = max_β{2βᵀz_S − βᵀH_Sβ} over β supported on S: enlarging S enlarges the feasible set.
(b) Cauchy interlacing applied to the function λ ↦ log((n+1)λ+1) − log(λ+1), which is increasing in λ.
*Difficulty.* Routine. *Lean core.* All (finite matrices). *Depends on.* TG1.

**TG4. Selection consistency of the target (the posterior itself, not the algorithm).**
*Statement (draft).* Let y = Xβ₀ + ε with ε ~ N(0, σ²I), S₀ = supp(β₀), s₀ = |S₀|, X standardised as in §4. Assume
(A1) sparse-eigenvalue: λ_min(G_S/(n−1)) ≥ κ > 0 for all |S| ≤ C s₀ (C a fixed constant ≥ 2), and |S₀| ≤ K/2;
(A2) beta-min: min_{j∈S₀} |β₀j| ≥ c₀ sqrt(s₀ log p / n) with c₀ = c₀(κ) large enough;
(A3) s₀ log p = o(n) and log p = o(n).
Then π(S₀ | y) → 1 in probability as n → ∞ (p = p_n allowed to grow), and hence HPM = MPM = S₀ with probability → 1,
PIP_j → 1{j ∈ S₀} uniformly in j, and Z is attained (to a 1 + o(1) factor) by the single term ϖ(S₀)m(S₀).
*Guarantee.* The method's *target* is selection-consistent in the sparse high-dimensional regime (O3); if the algorithm
is accurate (O1) it inherits this.
*Known/new.* Known in essence: Yang, Wainwright & Jordan (2016, Ann. Statist., "On the computational complexity of
high-dimensional Bayesian variable selection") prove this for a g-prior with g ≍ p^{2α} and a p^{−κ|S|} size prior;
Narisetty & He (2014, Ann. Statist.) for spike-and-slab with shrinking spikes; Castillo, Schmidt-Hieber & van der Vaart
(2015, Ann. Statist.) for Laplace spike-and-slab with complexity priors. The exact configuration here (g = n, ridge τ = 1,
BB(1,p) with per-variable cost log((2p−k−1)/(k+1)) ≈ log(2p/(k+1)), IG(0.01, 0.01), cap K = ⌊n/2⌋) is, as far as I know,
not covered verbatim; the adaptation is the work. Note the per-variable penalty here is log(2p) (prior) + ½log(n+1) (det
term), so it behaves like EBIC with γ = 1 (Chen & Chen 2008, Biometrika), which is known to be consistent for p = O(n^κ).
*Proof route.* Union bound over models by size and overlap with S₀. Key lemma A (spurious inclusion): for T ∩ S₀ = ∅,
log BF(S₀ ∪ T : S₀) ≤ ν log(1/(1 − R²_{T|S₀})) − ½|T| log(n+1) + O(|T|), with R²_{T|S₀} ~ Beta(|T|/2, (n−s₀−|T|)/2) under the
null, so P(log BF > −|T| log(2p/(|T|+1)) + ...) ≤ C(p,|T|)^{−1}·n^{−|T|/2}·poly; sum over |T| ≤ K − s₀ (the cap makes the sum
finite and the Beta tail, not the χ² tail, must be used for |T| ≍ n). Key lemma B (missed signal): for S ⊉ S₀ with
|S| ≤ Cs₀, Q_S − Q_{S₀∪S} ≥ (n−1)κ‖β₀,S₀\S‖²(1 − o(1)) by (A1), which beats the maximal prior+det gain by (A2).
The σ²-coupling means log BF differences are ν·log-ratios of Q's, not differences; the lemma must be stated multiplicatively.
*Difficulty.* Substantial (not hard: the route is standard, the bookkeeping at the cap and with the ridge is new).
*Lean core.* The deterministic inequalities of lemmas A/B (given the Beta quantile as a hypothesis); the Beta-tail and
union-bound probability rests on cited theory. *Depends on.* TG1, TG3.

**TG5. Finite-n selection bound.**
*Statement (draft).* Under (A1)–(A3) with explicit constants, for all n, p:
P(π(S₀|y) ≥ 1 − ε) ≥ 1 − C₁ n^{−1/2} − C₂ exp{−c n κ β_min² + C₃ s₀ log p} − ε⁻¹·(same).
*Guarantee.* A usable finite-sample statement for O3 (replaces "→ 1" by a rate).
*Known/new.* Rates of this shape are known (Narisetty–He); the explicit constants for this target are new.
*Proof route.* The same union bound as TG4 kept non-asymptotic. *Difficulty.* Substantial. *Lean core.* As TG4. *Depends on.* TG4.

### 2.2 ST — blocks, tables and the composite start

**ST1. Exactness of the start machinery.**
*Statement.* (a) Z̄₀ computed by the size convolution log F_b(k) = log Σ_j e_b(j) F_{b−1}(k−j), truncated at K, equals
Σ_{S∈𝕊_K} ϖ(S)∏_b r_b(S∩C_b) exactly (as real numbers); (b) the sampler "size k ~ ϖ(k)F_J(k)/Z̄₀; block sizes backwards
with P(k_b = j | r) = e_b(j)F_{b−1}(r−j)/F_b(r); sub-model within size class ∝ r_b(U)" returns S with probability exactly
π₀(S); (c) the max-plus DP in `start_mode` returns argmax_{𝕊_K} γ₀ with the stated tie rule; (d) π₀ is invariant to the
packing order of blocks and to the within-block index order.
*Guarantee.* The start is an *exactly* sampleable, exactly normalised law: the SMC bridge starts from a known constant
(O1; the whole evidence identity EV7 rests on this).
*Known/new.* Routine (convolution of independent block laws conditional on total size); worth stating because every
later identity uses it.
*Proof route.* Induction over blocks; the law of S under π₀ is a product over blocks *conditional on the size vector*,
and the size vector's law is the convolution. *Difficulty.* Routine. *Lean core.* All of (a)–(d) (finite sums; a model
Lean target for the campaign). *Depends on.* Nothing.

**ST2. Structure of the discrepancy: d = d_σ + d_X, and d = d_σ ≥ 0 under orthogonal blocks.** (Checked numerically, SC1.)
*Statement.* Let a = 2b₀ + yᵀy, u_b(S) = Δ_b(S∩C_b)/a. Define
d_σ(S) = −ν[log(1 − Σ_b u_b(S)) − Σ_b log(1 − u_b(S))] and d_X(S) = d(S) − d_σ(S).
(a) If X_{C_b}ᵀX_{C_b′} = 0 for all b ≠ b′ (orthogonal blocks), then d_X ≡ 0, so d = d_σ exactly.
(b) In general d_σ(S) ≥ 0, with d_σ(S) = 0 iff at most one block of S has Δ_b > 0; and
ν Σ_{b<b′} u_b u_{b′} ≤ d_σ(S) ≤ ν [−log(1 − Σ_b u_b) − Σ_b u_b] (so d_σ ≈ ν Σ_{b<b′} u_b u_{b′} when Σu_b is small).
(c) d_σ(S) depends on S only through the vector (u_b(S))_b, is increasing in each u_b, and changes by at most
ν·δ/(1 − Σu) when one u_b changes by δ.
*Guarantee.* Interpretation of what the bridge has to correct: even with *no* cross-block correlation the product start is
wrong by a σ²-coupling term that is Θ(n·R²_b·R²_{b′}) for pairs of signal blocks — so the bridge is never trivial, and the
"cost of correlation" must be measured relative to this baseline (O1, and the headline theorem).
*Known/new.* New to me; I have not seen the decomposition stated. (The underlying fact — block-marginal Bayes factors
with unknown σ² do not multiply — is folklore.)
*Proof route.* Under orthogonality G_S is block-diagonal, so log-det terms add and z_SᵀH_S⁻¹z_S = Σ_b Δ_b; then
log BF(S) = Σ_b[det terms]_b − ν log(1 − Σu_b) and Σ_b log r_b = Σ_b[det terms]_b − ν Σ_b log(1 − u_b). (b): ∏(1−u_b) ≥
1 − Σu_b (Weierstrass product inequality) with the second-order expansion for the bounds.
*Difficulty.* Routine. *Lean core.* All (an identity and two inequalities on finitely many reals). *Depends on.* TG1.

**ST3. σ²-mixture representation and an exact polynomial-time evidence under orthogonal blocks.**
*Statement.* Under orthogonal blocks, with t = 1/(2σ²):
π(S | y) = ∫₀^∞ π(S | t, y) π(t | y) dt, where for each fixed t the law π(S | t, y) ∝ ϖ(|S|) ∏_b [c_b(S∩C_b) e^{t Δ_b(S∩C_b)}]
(c_b the det ratios) is a "product-with-size-convolution" law of exactly the form of π₀, hence exactly normalisable by the
ST1 convolution for each t; consequently Z = C_n' ∫₀^∞ t^{ν−1} e^{−ta} N(t) dt with N(t) = Σ_k ϖ(k) F_J(k; t) computable in
O(J·K·B + J·2^B) per t, and the integral is one-dimensional and log-concave-ish in t (so Gauss–Laguerre or adaptive
quadrature gives Z to relative error 10⁻¹⁰ in O(10²) evaluations).
*Guarantee.* A ground truth for Z and PIPs under orthogonal blocks at any p (enumeration-free), usable to *test* the SMC
pipeline at scale and to prove ST8/HP4 (O1, O3). Also shows exactly which single coupling (σ²) the product start ignores.
*Known/new.* The conditional-on-σ² factorisation is immediate once seen; I have not seen it used as a test oracle. New-ish.
*Proof route.* (a − Σ_bΔ_b)^{−ν} = Γ(ν)⁻¹ ∫ t^{ν−1} e^{−t(a − ΣΔ_b)} dt and the integrand factorises over blocks.
*Difficulty.* Routine. *Lean core.* The finite-sum identity for fixed t (the integral representation is standard analysis).
*Depends on.* ST1, ST2.

**ST4. Perturbation bound for d_X under ε-separated blocks.**
*Statement (draft).* Let ε = max_{b≠b′} max_{j∈C_b, l∈C_b′} |r_jl| and suppose λ_min(G_S/(n−1)) ≥ κ for all |S| ≤ k.
Then for every S with |S| ≤ k, |d_X(S)| ≤ C(k, κ)·ε·[k + ν·R²(S)], explicitly
|d_X(S)| ≤ k·log(1 + 2kε/κ) + ν·(2kε/κ)·Σ_b u_b(S)/(1 − Σ_b u_b(S) − 2kε/κ) (valid when the denominator is > 0).
*Guarantee.* Quantifies how cross-block correlation enters the discrepancy: linearly in ε with a factor n·R² from the fit
term and k from the det term. Feeds the stage-count and mixing bounds under weak cross-block correlation (headline, O1).
*Known/new.* New (routine matrix perturbation).
*Proof route.* G_S = G_S^{bd} + E_S with ‖E_S‖_op ≤ (n−1)kε (Gershgorin); Weyl for the log-det difference; for the fit term,
|z_SᵀH_S⁻¹z_S − z_Sᵀ(H_S^{bd})⁻¹z_S| ≤ ‖H_S^{−1/2}‖²‖E‖‖(H^{bd})^{−1/2}‖²‖z_S‖²-type bound using the resolvent identity.
*Difficulty.* Routine but messy. *Lean core.* The matrix inequalities (Weyl, Gershgorin are in Mathlib or close).
*Depends on.* ST2.

**ST5. The clustering recovers well-separated clusters and never splits them.**
*Statement.* Suppose [p] partitions into groups 𝒢₁..𝒢_m with |𝒢_i| ≤ B, and
min_{j,l in the same group} |r_jl| > max_{j,l in different groups} |r_jl|   (strict separation).
Then (a) every group is a node of the complete-linkage dendrogram; (b) the top-down size cut retains each group as a
whole cluster or as a union of groups; (c) next-fit packing never splits a retained cluster, so every block is a union of
whole groups; hence (d) cross-block |r| ≤ ε := max between-group |r|.
If strict separation holds only up to ties, the same holds for the lexicographic tie rule provided no cross-group tie
precedes a within-group merge.
*Guarantee.* The ε of ST4 is a property of the *design*, not of the algorithm's luck, under separation (O1, O3).
*Known/new.* (a) is the classical "complete linkage recovers well-separated clusters" fact (any hierarchical linkage does
under strict separation); (b)–(d) are specific to this cut/packing and routine.
*Proof route.* Induction on merges: all within-group distances are smaller than all between-group distances, so all
within-group merges precede any between-group merge (Lance–Williams max keeps between-group distances between-group).
*Difficulty.* Routine. *Lean core.* All (finite combinatorics on the dendrogram). *Depends on.* Nothing.

**ST6. Block count and table cost.**
*Statement.* ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉ (next-fit uses at most twice the optimal number of bins, each cluster ≤ B); table scores
Σ_b 2^{|C_b|} ≤ J·2^B ≤ (2p/B + 2)·2^B; and with B = min(⌊√n⌋, ⌊√p⌋, 16) this is O(p·2^B/B) = O(p·2^{√min(n,p)}/√min(n,p))
until the cap 16 binds.
*Guarantee.* Work bound for the tables (O2).
*Known/new.* Next-fit ≤ 2·OPT is classical bin-packing (Johnson 1973); the rest is arithmetic.
*Proof route.* Any two consecutive next-fit bins hold > B items together. *Difficulty.* Routine. *Lean core.* All.

**ST7. Within-block masking immunity.**
*Statement.* Every S ⊆ C_b with |S| ≤ K is scored at table time; hence (a) the HPM satisfies F(HPM) ≥ max_b max_{U⊆C_b} F(U)
deterministically, before any randomness; (b) a masked set M (all proper subsets at noise level, M itself strong) that lies
inside a single block has π₀(M ⊆ S) = π₀-mass of its exact block posterior, i.e. masking of any order ≤ B within a block costs
nothing; (c) the independence proposal proposes M ⊆ S′ with probability π₀(M ⊆ S′), which is ≥ the exact block-posterior
inclusion times the size-coupling factor (ST9).
*Guarantee.* The method's answer to "split-and-merge breaks under correlation": correlated clusters of size ≤ B are
handled *exactly* at the start (O3). *Known/new.* Trivial once stated; worth a proposition because NG1 is its converse.
*Difficulty.* Trivial. *Lean core.* All. *Depends on.* ST1.

**ST8. Conservativeness of the start under orthogonal blocks (σ² inflation).**
*Statement (draft).* Under orthogonal blocks, for every block b, every U ⊆ C_b and every S_{−b} ⊆ [p]\C_b:
the fit part of the block-local Bayes factor, ν log(1/(1 − u_b)), is at most the fit part of the conditional Bayes factor
given S_{−b}, ν log((1 − u_{−b})/(1 − u_{−b} − u_b)), while the det parts coincide under orthogonality; so log r_b(U) ≤ log m(U ∪ S_{−b}) − log m(S_{−b}),
with equality iff Δ_{−b} = 0. Consequently, under (A1)–(A3) with the
beta-min constant enlarged by the factor (1 − R²_{tot})⁻¹ where R²_tot = Σ_b u_b(S₀), the start mode satisfies S̃₀ = S₀
with probability → 1; without the enlarged margin, S̃₀ ⊆ S₀ with probability → 1 (no false inclusions) and S₀ \ S̃₀ consists
of variables whose block-local evidence falls below log(2p/(k+1)) + ½log(n+1).
*Guarantee.* The deterministic start mode is a selection-consistent estimator in its own right under orthogonal blocks and
a slightly stronger signal condition (O3); and its errors are omissions only, which LS0 repairs (HP4).
*Known/new.* New (it is the statistical content of ST2).
*Proof route.* The first inequality is 1/(1−u_{−b}−u_b) ≥ ... monotonicity of x ↦ (1−u_{−b})/(1−u_{−b}−x) vs 1/(1−x);
then run the TG4 union bound block by block with the inflated noise level σ² + (signal variance of other blocks).
*Difficulty.* Substantial (the probabilistic part). *Lean core.* The deterministic inequality. *Depends on.* ST2, TG4.

**ST9. The start as a combinatorial explorer (cross-block hitting).**
*Statement.* For disjoint sets M_b ⊆ C_b (b in a set of blocks 𝔅) and M = ∪M_b,
π₀(M ⊆ S) = Σ_k [ϖ(k) F_J^{(M)}(k)] / Z̄₀, where F_J^{(M)} is the ST1 convolution with block b's profile replaced by
e_b^{(M)}(j) = Σ_{|U|=j, U⊇M_b} r_b(U); in particular, if the size prior were flat, π₀(M ⊆ S) = ∏_b π_b(M_b ⊆ U)
(product of exact block-posterior inclusions), and in general
π₀(M ⊆ S) ≥ ∏_b π_b(M_b ⊆ U) · min_k [ϖ(k + |M|)/ϖ(k)] over the support, i.e. ≥ ∏_b π_b(M_b ⊆ U)·∏_{i<|M|}(k_max+i+1)/(2p−k_max−i−1).
Hence the probability that at least one of the N initial draws (or of the N·T·R independence proposals) contains M is
1 − (1 − π₀(M ⊆ S))^{N(1+TR)}.
*Guarantee.* Quantifies the mechanism by which the product start resolves *cross-block* masking when each component has
moderate block-local evidence: masked sets whose parts are individually plausible are found at the start with high
probability; those whose parts are individually implausible are not (NG1). This is the "particles" half of the headline (O1, O3).
*Known/new.* Elementary consequence of ST1; new as a stated mechanism.
*Difficulty.* Routine. *Lean core.* All. *Depends on.* ST1.

**ST10. Thermodynamic identities: what split-and-merge gets wrong is what the bridge must traverse.**
*Statement.* With Z_φ as in §0: (a) d/dφ log Z_φ = E_{π_φ} d and d²/dφ² log Z_φ = Var_{π_φ} d ≥ 0 (log-convexity);
(b) log(Z/(m(∅)Z̄₀)) = ∫₀¹ E_{π_φ} d dφ (thermodynamic integration);
(c) KL(π₀‖π) = log(Z/(m(∅)Z̄₀)) − E_{π₀}d ≥ 0 and KL(π‖π₀) = E_π d − log(Z/(m(∅)Z̄₀)) ≥ 0;
(d) J(π₀, π) := KL(π₀‖π) + KL(π‖π₀) = E_π d − E_{π₀} d = ∫₀¹ Var_{π_φ}(d) dφ;
(e) Λ := ∫₀¹ sd_{π_φ}(d) dφ ≤ sqrt(J(π₀, π)) (Cauchy–Schwarz).
*Guarantee.* Interpretation: π₀ is exactly the "split-and-merge" answer (exact block posteriors glued by the size prior);
its Jeffreys error J is a computable statistic of (X, y) (E_π d from the measured rounds, E_{π₀} d from the initial
population); and the sequential depth is controlled by Λ ≤ √J (BR3). This is the quantitative bridge between "how wrong
is split-and-merge here" and "how many stages does SMC-BVS need" (headline, O1 vs split-and-merge).
*Known/new.* (a)–(d) are standard exponential-family/TI identities (e.g. Gelman & Meng 1998, Statist. Sci.); (e) trivial;
the *use* (π₀ = split-and-merge; report Ĵ on the run card) is a proposal.
*Difficulty.* Routine. *Lean core.* All of (a)–(e) on a finite state space. *Depends on.* ST1.

### 2.3 KN — the move kernels

**KN1. Every elementary step is γ_φ-reversible on 𝕊_K.**
*Statement.* For every φ ∈ [0,1]: (a) the Gibbs coordinate step with "addition at |S| = K excluded" is the exact conditional
update of γ_φ (because ϖ(k) = 0 for k > K, the conditional of j given S\{j} puts mass 0 on the infeasible configuration);
(b) the uniform swap is a Metropolis step with a symmetric proposal on {S′ = S − j + l}, so acceptance 1 ∧ γ_φ(S′)/γ_φ(S) is
correct; (c) the neighbour swap with proposal q(S→S′) = |S|⁻¹|N(j)\S|⁻¹ and reverse q(S′→S) = |S|⁻¹|N(l)\S′|⁻¹ (the reverse
exists because the graph is symmetric and j ∈ N(l)\S′) has Hastings ratio exactly |N(j)\S|/|N(l)\S′| as coded; the "reject
without score when N(j)\S = ∅" is a self-loop; (d) the independence step with proposal π₀ and acceptance
1 ∧ e^{φ[d(S′) − d(S)]} is the Metropolised independence sampler for π_φ since π_φ/π₀ ∝ e^{φd}.
All four are reversible with respect to π_φ; the recorded o_j equals π_φ(j ∈ S | S\{j}).
*Guarantee.* The elementary validity of the sampler (O1). *Known/new.* Routine. *Difficulty.* Routine.
*Lean core.* All four detailed-balance identities on the finite space (a flagship Lean target: small, exact, and it
certifies the code's acceptance formulas including the cap rule). *Depends on.* TG1, ST1.

**KN2. The random-order round kernel is π_φ-invariant and self-adjoint; the bridge is a Feynman–Kac model.**
*Statement.* Q_φ := (1/m!) Σ_σ P_{σ(1)}⋯P_{σ(m)} satisfies π_φ Q_φ = π_φ and Q_φ* = Q_φ on L²(π_φ) (the uniform law on
permutations is reversal-invariant and each P_j is self-adjoint). The final island is the Feynman–Kac particle model with
initial law π₀, potentials G_t(S) = e^{(φ_t − φ_{t−1})d(S)}, mutation kernels Q_{φ_t}, multinomial resampling, N particles,
followed by L + 4 further Q₁ mutations without reweighting.
*Guarantee.* Places the method exactly inside the Del Moral (2004) framework so that EV1, EV3, EV4, PI1 are citations plus
bookkeeping (O1). *Known/new.* Routine. *Lean core.* Invariance and self-adjointness on the finite space. *Depends on.* KN1.

**KN3. Dirichlet-form comparison: the random-order round dominates half the random-scan mixture.** (Possibly known; I
have no citation.)
*Statement.* Let P₁..P_m be self-adjoint Markov contractions on L²(π) (any reversible kernels) and Q = E_σ[P_{σ(1)}⋯P_{σ(m)}]
with σ uniform. Then for every f with π f = 0,
ℰ_Q(f) := ⟨f,(I − Q)f⟩ ≥ (1/(2m)) Σ_j ⟨f,(I − P_j²)f⟩ = ½ ℰ_{R₂}(f), R₂ := (1/m)Σ_j P_j².
If P_j is a projection (every Gibbs step is), P_j² = P_j. Consequently
gap(Q_φ) ≥ ½ gap(R₂) ≥ (p/(2m))·gap(G^{rs}_φ) + (1/(2m))·gap(P_U²) + (B/(2m))·gap(P̄_N²) + (1/(2m))·gap(P_I²),
where G^{rs}_φ = (1/p)Σ_j P_{G_j} is the random-scan Gibbs sampler on π_φ, and the sum is in the Loewner sense (each term is
a lower bound for the corresponding part of ℰ_{R₂}). In particular the round is never slower (in gap, per round) than half
the random-scan Gibbs sampler, and any lower bound on the gap of a random-scan flip/swap chain transfers with a factor
1/(2m) per step counted, i.e. with no loss per *score* for the Gibbs part.
*Guarantee.* Turns known mixing-time bounds for random-scan add/delete/swap chains (KN5) into bounds for the actual round
kernel; also shows that adding steps to the round can only increase ℰ_Q's lower bound (O1).
*Known/new.* The inequality follows from a two-line argument (below) and may well be folklore; I could not name a
reference. It is *not* the systematic-scan-vs-random-scan comparison, which is known to fail in general (Roberts &
Rosenthal 2015, and He, De Sa, Mitliagkas & Ré 2016 give counterexamples for fixed scans); the random permutation is
what makes it work.
*Proof route.* ⟨f, P_σ f⟩ = ⟨P_{σ(1)}f, P_{σ(2)}⋯P_{σ(m)}f⟩ ≤ ‖P_{σ(1)}f‖·‖f‖ (self-adjointness, contraction); average over σ:
ℰ_Q(f) ≥ ‖f‖·(1/m)Σ_j(‖f‖ − ‖P_jf‖) and ‖f‖ − ‖P_jf‖ ≥ (‖f‖² − ‖P_jf‖²)/(2‖f‖) = ⟨f,(I−P_j²)f⟩/(2‖f‖).
*Difficulty.* Routine. *Lean core.* All (finite-dimensional inner-product inequality; Mathlib has what is needed).
*Depends on.* KN2.

**KN4. Uniform Doeblin minorisation from the independence step; explicit TV contraction at every temperature.**
*Statement.* For every φ and every S, S′: P_I(S, S′) ≥ π_φ(S′)/M_φ with M_φ = max_S π_φ(S)/π₀(S) = e^{φ d_max}Z̄₀/Z_φ, hence
Q_φ(S, ·) ≥ (1/(m M_φ)) π_φ(·) (the independence label is first in the order with probability 1/m and the remaining steps
preserve π_φ), so ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1 − 1/(mM_φ))^k for all S, and the Dobrushin coefficient satisfies
β(Q_φ) ≤ 1 − 1/(mM_φ). Moreover (a) M_φ ≤ exp{φ(d_max − E_{π₀} d)} (Jensen on Z_φ/Z̄₀ = E_{π₀}e^{φd}); (b) by Liu (1996,
Statist. Comput., "Metropolized independent sampling") the independence step alone has spectral gap exactly
min_S π₀(S)/π_φ(S) = 1/M_φ; (c) under orthogonal blocks d_max − E_{π₀}d ≤ ν·max_S Σ_{b<b′}[u_bu_{b′}](S) − ν·E_{π₀}Σ_{b<b′}u_bu_{b′}
+ O(ν(Σu)³), which is O((#boundary signals)·R²_tot·log p) when all strong signals are included under π₀ (sketch: only
variables with block-local evidence near the inclusion threshold have non-degenerate inclusion under π₀, and each such
variable moves u_b by O(log p/n)).
*Guarantee.* The only *unconditional*, explicit mixing statement available for every design: the chain at every temperature
is uniformly ergodic with a rate that depends on the design only through the range of the discrepancy relative to its π₀-mean.
Under weak cross-block correlation this is polynomial in p; under strong masking it is exponential, and NG1 shows that this
is not an artefact of the proof (O1; the "particles" half of the headline).
*Known/new.* (a)–(b) are textbook (Mengersen & Tweedie 1996, Ann. Statist.; Liu 1996); the use for the round kernel and the
π₀-mean form of the bound are new but routine. (c) is a sketch and needs the TG4 machinery.
*Difficulty.* Routine for the minorisation; substantial for (c). *Lean core.* The minorisation inequality and Jensen step
on the finite space. *Depends on.* KN1, KN2, ST2.

**KN5. Rapid mixing of the round kernel at φ = 1 under selection-consistency conditions.**
*Statement (draft).* Under (A1)–(A3) of TG4 (with the sparse-eigenvalue condition on sets of size ≤ C s₀ and a
sparsity-projection condition of the Yang–Wainwright–Jordan type), with probability → 1 over y, the random-scan chain
R = (1/m)Σ_j P_j² on π = π₁ has spectral gap ≥ c/(m·s₀²·n·log p)-type (polynomial), and therefore (KN3) the round kernel
Q₁ mixes to total-variation ε in O(s₀²·n·log p·log(1/ε)·(polylog)) rounds from any start in 𝕊_K.
*Guarantee.* The terminal rounds and, more importantly, the φ = 1 end of the bridge are provably fast in the regime where the
target is consistent (O1, O3); i.e. "if the posterior is well-behaved enough to select, the sampler can see it".
*Known/new.* The core is Yang, Wainwright & Jordan (2016) Theorem 2 (polynomial mixing of a lazy add/delete/swap Metropolis
chain restricted to |S| ≤ s₀-ish under their conditions). Transfer requires: (i) their g ≍ p^{2α} prior → g = n with ridge
(penalty log 2p + ½log n per variable; I believe the canonical-path argument needs only "each spurious variable costs ≥ c log p
and each missed signal costs ≥ c′ n κ β²_min", both available); (ii) their size truncation → K = ⌊n/2⌋ (the canonical paths
from large models proceed by deletions; the posterior mass above size C s₀ must be shown exponentially small — TG4 lemma A at
the cap); (iii) their chain → the round kernel via KN3 (Gibbs flips ≥ ½ MH flips by Peskun since r/(1+r) ≥ ½ min(1, r);
uniform swap present with weight 1/m; neighbour swaps help only if the canonical paths can be routed through the graph).
*Proof route.* Canonical paths (Sinclair 1992) as in YWJ with the landscape lemma HP3; the swap weight 1/m costs a factor m
in the gap bound (not in the score count) unless neighbour-graph routing (KN6) is used.
*Difficulty.* Substantial to hard (the adaptation is where the work is; the architecture is known).
*Lean core.* The landscape inequalities (HP3) and the Dirichlet-form comparisons; the canonical-path theorem is cited.
*Depends on.* TG4, HP3, KN3.

**KN6. Neighbour graph: validity, size, and what it contains.**
*Statement.* (a) The graph is symmetric by construction, so KN1(c) holds; degrees are ≥ 1 for p ≥ 2 and ≤ B before
symmetrisation (unbounded after). (b) For a column x_j independent of all others with Gaussian rows and n → ∞,
P(j acquires an edge beyond its forced best partner) = P(max_{l≠j}|r_jl| > sqrt(2 log p/n)) → 1 − e^{−1/sqrt(π log p)}·…;
more simply, the expected number of spurious edges per null row is ≤ 2(p−1)·Φ̄(sqrt(2 log p)) ≈ 1/sqrt(π log p) → 0 slowly,
so the total number of spurious edges is O(p/sqrt(log p)) and the graph has O(p) edges in expectation. (c) Under ε-separated
groups with within-group |r| > r_n (ST5), every variable's B strongest partners lie in its own group when the group has ≤ B+1
members, so the neighbour swap moves within groups: it is exactly the "swap a proxy for its correlated alternative" move that
canonical-path arguments under correlation need.
*Guarantee.* The neighbour swap is a valid, cheap, correlation-aware move whose target set is where proxies live (O3 under
correlation). *Known/new.* (b) is the standard Gaussian maximum-correlation calculation (r_jl√n ≈ N(0,1)); routine.
*Difficulty.* Routine. *Lean core.* (a) and (c). *Depends on.* ST5.

**KN7. Rao–Blackwellised recording is unbiased at every position of the round.**
*Statement.* If the particle's state at the start of a measured round is distributed as π, then for every coordinate j the
recorded o_j has E[o_j] = PIP_j regardless of the (random, state-independent) position of label G_j in the round, because
the state immediately before the Gibbs draw of j is π-distributed (every preceding step is π-invariant and the order is
independent of the state) and o_j = π(j ∈ S | S\{j}) at that state. The same holds for any h evaluated after a complete
round (the H_r(h) accumulators).
*Guarantee.* The PIP and general-h estimators have no bias from the within-round position (O1). *Known/new.* Routine;
worth one line in the paper because the "record before the draw at a random position" convention is unusual.
*Lean core.* All (finite). *Depends on.* KN1, KN2.

### 2.4 BR — the bridge, ESS rule and the grid

**BR1. ESS fractions are χ²-divergences; the restricted ESS is the full ESS times an explicit coverage factor.**
*Statement.* For u < v: (a) the population ESS fraction of the weights e^{(v−u)d} under π_u equals ρ(u,v) =
exp{2F(v) − F(u) − F(2v−u)} = 1/(1 + χ²(π_v ‖ π_u)), where F(t) = log Z_t; (b) for any V ⊆ 𝕊_K with η_t := π_t(V^c),
ρ_V(u, v) = ρ(u, v) · (1 − η_v)² / ((1 − η_u)(1 − η_{2v−u}))   (exact identity);
hence (c) ρ(u, v) ≥ ρ_V(u, v)·(1 − η_u)(1 − η_{2v−u}) ≥ 0.9(1 − η_u)(1 − η_{2v−u}) on every grid interval, and the full
χ² satisfies 1 + χ²(π_v‖π_u) ≤ (10/9)/((1 − η_u)(1 − η_{2v−u})).
*Guarantee.* Says exactly what the certified grid guarantees about the *full* bridge: a χ² ≤ 1/9 per stage up to the mass
V misses at the stage's left end and at its "look-ahead" point 2v − u (which can exceed 1: a finite-sum, not a run
temperature). Everything the grid cannot see is in η (NG4) (O1).
*Known/new.* (a) is standard (ESS ↔ χ², e.g. in the SMC-samplers literature); (b)–(c) are new but immediate.
*Proof route.* F_V(t) = F(t) + log(1 − η_t). *Difficulty.* Routine. *Lean core.* All. *Depends on.* Nothing.

**BR2. Mean-value form of the stage χ².**
*Statement.* For u < v, log(1 + χ²(π_v‖π_u)) = (v − u)² · Var_{π_ξ}(d) for some ξ ∈ (u, 2v − u); the same holds for the
V-restricted laws. (Λ(s) := F(u + s) − F(u) is C^∞ with Λ″(s) = Var_{π_{u+s}}(d); log(1+χ²) = Λ(2δ) − 2Λ(δ) + Λ(0) is a second
difference.)
*Guarantee.* Converts the ESS rule into a statement about the variance of d along the path: a step δ is admissible iff
δ² Var_{π_ξ}(d) ≤ log(10/9) ≈ 0.1054 at the relevant ξ, i.e. δ·sd_ξ(d) ≤ 0.3246. This is the lemma behind all depth results.
*Known/new.* Routine calculus; the use is new. *Lean core.* Second-order mean value theorem (Mathlib) on a finite
log-sum-exp. *Depends on.* BR1.

**BR3. Stage-count bounds in terms of the thermodynamic length (checked in SC2 for smooth spreads).**
*Statement (draft).* Let σ_max := sup_{φ∈[0,2]} sd_{π_φ|V}(d) and Λ_V = ∫₀¹ sd_{π_φ|V}(d) dφ. The grid built from any set of
targets satisfies (a) T ≤ 1 + ⌈σ_max/0.3246⌉ + (number of pilot targets that are appended without bisection);
(b) under the regularity condition "sd_{π_φ|V}(d) varies by at most a factor 2 over any admissible interval and its
look-ahead", T ≥ Λ_V/(2·0.3246) and T ≤ 2Λ_V/0.3246 + 1; (c) SC2 shows T ≈ Λ_V/0.3246 to within 10% for Gaussian-like
spreads of d under γ₀, and (d) by ST10(e), T ≲ 3.1·sqrt(J_V(π₀, π)) under (b).
*Guarantee.* The sequential depth is a path-length functional of the discrepancy, hence of the design through ST2/ST4; this
is the "depth" half of the headline (O2). Under orthogonal blocks with all strong signals included under π₀, Λ = O(sqrt(s_bdry)·R²_tot·log p)
(sketch as in KN4(c)), so T = O(log p) stages — polynomial depth with no correlation.
*Known/new.* The identification of ESS-schedules with thermodynamic length is folklore in the tempering literature (Crooks
2007 "thermodynamic length"; Syed, Bouchard-Côté, Deligiannidis & Doucet 2022, JRSSB, use the related "global communication
barrier" ∫ E|d − d′| dφ for parallel tempering); the two-sided bound for this bisection rule is new and routine. (b) is where
honesty matters: without regularity the lower bound fails (BR4 gives the failure mode).
*Proof route.* BR2 for each interval; summation; Riemann-sum comparison under regularity.
*Difficulty.* Routine with regularity; the regularity-free version is substantial. *Lean core.* The per-interval inequality
and the summation; the sup/inf bookkeeping. *Depends on.* BR2.

**BR4. Two-state crossing lemma: a dominance crossing costs log₂(gap) + O(1) stages, not O(1).** (Checked in SC2.)
*Statement.* Let the bridge be pair-dominated: V = {A, B} (or two groups with constant d within each), d(A) = 0, d(B) = D > 0,
log γ₀(B) − log γ₀(A) = −Dφ* with crossing temperature φ* ∈ (0, 1). Write x = φ* − u for the distance to the crossing.
(a) *Halving lemma.* While x > (log 9)/D, every admissible step from u satisfies v − u ≤ x/2 + (log 9)/(2D) + O(e^{−Dx}/D):
the look-ahead term F(2v − u) forces the step to stop at half the distance. Hence at least log₂(Dφ*/log 9) − 1 stages are
spent before the crossing. (b) Inside the crossing (π_u(B) ∈ [1/(9e²), 0.9]) each stage advances the log-odds by at most
≈ log 11 ≈ 2.4, so at most ⌈(logit 0.9 − logit(1/81))/1.2⌉ + 1 ≈ 7 stages are spent there. (c) Once π_u(B) ≥ 0.9 the step to
v = 1 is admissible (the ESS fraction of two-point weights tends to π_u(B) as the weight ratio → ∞). Therefore
log₂(Dφ*) + c₁ ≤ T ≤ log₂(Dφ*) + c₂ with explicit c₁, c₂ (numerically T = log₂ D + 7 ± 1 for D ∈ [20, 10⁵] at φ* = ½).
(d) With K separated crossings the counts add (SC2: two crossings with gaps 400 and 800 gave 28 ≈ 15.6 + 16.6 − O(1)).
*Guarantee.* Sharp depth cost of each competing-model takeover (the situation the grid was designed for): logarithmic in the
score gap (so O(log n) per crossing for Θ(n) gaps), additive over crossings (O2; headline). It also shows that the
thermodynamic length Λ (= π per crossing, independent of D) *underestimates* the ESS-rule's stage count for crossings by a
log D factor, which is why BR3 needs its regularity condition.
*Known/new.* New (the method report mentions a two-state analysis by someone else for the evidence error; this is about the
stage count and the halving mechanism).
*Proof route.* Explicit two-point formulas: with p = π_u(B) and x_w = e^{δD}, ESS fraction = ((1−p) + p x_w)²/((1−p) + p x_w²);
solve ≥ 0.9 for x_w; p = 1/(1 + e^{Dx}) gives the halving.
*Difficulty.* Routine. *Lean core.* All of (a)–(c): explicit inequalities in three real parameters — an ideal certificate.
*Depends on.* BR1.

**BR5. Correctness and cost of the grid construction; the frozen object is calibration-measurable.**
*Statement.* (a) `build_grid` terminates; every appended v satisfies v > u, ρ_V(u, v) ≥ 0.9, and the grid is a subset of
{pilot temperatures} ∪ {dyadic bisection points}; it fails only with one of the four named reasons; the number of F_V evaluations
is ≤ 3(1 + 60)·(T + #targets). (b) The frozen tuple (grid, tier, N_e, L) is a function of (X, y, seed, streams 0–9) only, and
the final streams 10–13 are independent of it (distinct SplitMix64 seeds of a single xoshiro family, under the usual
"independent streams" modelling assumption). (c) Consequently every statement of EV1/PI2 that holds "for a fixed grid" holds
conditionally on the calibration σ-field, hence unconditionally.
*Guarantee.* Justifies the calibrate-then-freeze architecture as the device that restores exact unbiasedness (adaptive SMC
is biased: NG6) (O1). *Known/new.* Routine engineering + a measurability lemma. *Lean core.* (a). *Depends on.* BR1.

**BR6. Forced pilot steps certify a large empirical spread.**
*Statement.* A pilot step is forced iff no v ≤ u + 1/T_e passes the empirical ESS test; by BR2 applied to the empirical
population law, this implies sd_{ξ}(d) > 0.3246·T_e for some ξ ∈ (u, u + 2/T_e), i.e. an empirical spread of the discrepancy
exceeding ≈ 325 nats at T_e = 1000 — which can only happen when a few particles carry d values Θ(n) above the bulk (an
impending crossing with a rare state, BR4 regime). A fully forced pilot has exactly T_e stages (RC-2).
*Guarantee.* Interprets the `forced_pilot_steps` trigger as a detector of rare-state crossings rather than a tuning accident (O1).
*Known/new.* Routine. *Lean core.* All. *Depends on.* BR2.

**BR7. Free by-products: a thermodynamic-integration evidence estimate and a Jeffreys-divergence run-card statistic.**
*Statement.* With the per-stage populations {S_i^{(t)}} (after resampling, before the move) the trapezoid TI estimate
log Ẑ_TI = log m(∅) + log Z̄₀ + Σ_t ½(φ_t − φ_{t−1})[d̄_{t−1} + d̄_t], d̄_t the population mean of d at stage t, is consistent in
N for every grid (not unbiased), with discretisation bias ≤ ½ Σ_t (φ_t − φ_{t−1})² · max_ξ Var_ξ(d) ≤ (T/2)·0.1054·(max/typical
ratio)... ≈ 0.05·T nats worst case per the admissibility of every interval (BR2); and Ĵ = d̄_final − d̄_0 is a consistent
estimate of J(π₀, π) (ST10). Disagreement between log Ẑ_SMC and log Ẑ_TI beyond their joint Monte Carlo error is a
*run diagnostic with power against weight degeneracy* that the ESS checks lack (it compares two estimators with different
failure modes), although not against unseen modes (NG1).
*Guarantee.* Two additional reportable quantities at zero scoring cost (O1). *Known/new.* TI is classical (Gelman & Meng
1998); using it as a cross-check against the SMC product estimator is standard practice but not in the method. *Difficulty.*
Routine. *Lean core.* The discretisation bound. *Depends on.* ST10, BR2.

### 2.5 EV — the evidence estimator

**EV1. Unbiasedness of each island's evidence and of every "unnormalised" summary, for every frozen grid.**
*Statement.* For a fixed grid 0 = φ₀ < … < φ_T = 1, fixed N, L, Hm: (a) E[Ẑ_r] = Z, where
Ẑ_r = m(∅)Z̄₀∏_{t=1}^T (1/N)Σ_i e^{(φ_t−φ_{t−1})d(S_i^{(t−1)})}; (b) for every bounded h and every measured round, 
E[Ẑ_r · (1/N)Σ_i h(S_i)] = Z·π(h), hence E[Ẑ_r·H_r(h)] = Z·π(h) and E[Ẑ_r·PIP̂_rj] = Z·PIP_j (using KN7 for the
within-round o_j); (c) Ẑ_1..Ẑ_R are iid across islands (independent streams, same law), so E[(1/R)ΣẐ_r] = Z; (d) all of
(a)–(c) hold conditionally on the calibration σ-field (BR5), hence unconditionally for the complete method including escalation.
*Guarantee.* The evidence and the Ẑ-weighted PIP/h numerators are exactly unbiased for the true posterior quantities at every
finite budget, for every design and every seed rule (O1). This is the "never correctness" half of the headline.
*Known/new.* Known: Del Moral (2004, *Feynman–Kac Formulae*, Prop. 7.4.1/Thm 7.4.2 on unbiasedness of the unnormalised
particle measures γ̂_n(f)); the method report records it as P6/P7. The terminal-round extension (b) uses invariance of Q₁.
*Proof route.* Martingale/induction over stages: E[γ̂_{t}(f) | 𝔉_{t−1}] = γ̂_{t−1}(G_t Q_t f)... with multinomial resampling the
standard argument applies verbatim because the resampled empirical measure has conditional expectation equal to the weighted one.
*Difficulty.* Routine (citation + bookkeeping). *Lean core.* Possible but heavy: finite state space, finitely many stages,
continuous uniforms; a certificate of the one-stage identity E[(1/N)Σ_i e^{δd(S_{a_i})} f(S'_{a_i}) | past] = (1/N)Σ_i e^{δd(S_i)}(Q f)(S_i)
is small; the induction is mechanical. *Depends on.* KN1, KN2, ST1, BR5.

**EV2. Sharp relative variance under perfect mixing; what the ESS-0.9 grid buys.**
*Statement.* If at every stage the moved particles are iid π_{φ_t} (perfect mixing), then the stage factors are independent and
Var(Ẑ_r/Z) = ∏_{t=1}^T (1 + χ²_t/N) − 1 ≤ exp{Σ_t χ²_t/N} − 1; with the certified grid and coverage η (BR1(c)),
Σ_t χ²_t ≤ T·[(10/9)/((1−η)²) − 1] ≈ T/9 + 2.2·T·η, so the relative RMSE of Ẑ_r is ≈ sqrt(T/(9N)) (e.g. 3% at T = 22, N = 2,500)
and that of the 4-island pool half of that. Conversely Var(Ẑ_r/Z) ≥ Σ_t χ²_t/N − O(1/N²), so the bound is tight to first order.
*Guarantee.* An honest, explicit, first-order finite-sample error for the evidence in the ideal case, with the stage count T as
the only design-dependent quantity (O1; headline). *Known/new.* Standard (this is the textbook variance of a product of
independent importance-sampling estimates); the identification of the ESS-rule threshold with the per-stage relative variance
1/(9N) is the point.
*Difficulty.* Routine. *Lean core.* All (finite). *Depends on.* BR1.

**EV3. Non-asymptotic variance with imperfect mixing (explicit, design-dependent).**
*Statement (draft).* For every grid and design, E[(Ẑ_r/Z − 1)²] ≤ (C/N)·Σ_{t=1}^{T} osc_t·(1/(1 − β_t))·(...) + O(1/N²), where
osc_t = sup G_t/inf G_t over the support ≤ e^{(φ_t−φ_{t−1})(d_max − d_min)} and β_t = β(Q_{φ_t}) ≤ 1 − 1/(mM_{φ_t}) (KN4).
With Cérou, Del Moral & Guyader (2011, Ann. IHP, "A nonasymptotic theorem for unnormalized Feynman–Kac particle models") the
leading term is exactly (1/N)Σ_t Var-type quantities of the semigroup, and the bound above follows by bounding the semigroup
by Dobrushin coefficients.
*Guarantee.* A rigorous finite-N bound valid for *every* design, in which correlation enters only through (i) the range of d
(osc_t and M_φ, polynomial under weak cross-block correlation, exponential under strong masking) and (ii) T (O1; headline).
*Known/new.* Known architecture (Del Moral 2004 Thm 7.4.4-type L_p bounds; CDG 2011); the instantiation is routine but the
constants will be crude; I would present it with KN4's M_φ to make the design dependence explicit and honest.
*Difficulty.* Substantial (keeping constants explicit and small). *Lean core.* None (cited probability); the algebra
relating osc_t and M_φ to d is finite. *Depends on.* KN4, EV1, BR1.

**EV4. Central limit theorems in N.**
*Statement.* For every fixed grid, √N(Ẑ_r/Z − 1) ⇒ N(0, σ²_Z), √N(PIP̂_rj − PIP_j) ⇒ N(0, σ²_j), √N(H_r(h) − π(h)) ⇒ N(0, σ²_h),
with the Feynman–Kac asymptotic variances (Chopin 2004, Ann. Statist., "Central limit theorem for sequential Monte Carlo
methods and its application to Bayesian inference"; Del Moral 2004 Ch. 9); under perfect mixing σ²_Z = Σ_t χ²_t ≤ T/9 (EV2).
*Guarantee.* Rates for O1. *Known/new.* Known (citation). *Lean core.* None. *Depends on.* KN2.

**EV5. Lower confidence bounds for Z: three valid ones, and the best is the island minimum.**
*Statement.* With Ẑ_1..Ẑ_R iid, unbiased and nonnegative (EV1): (a) P(Z ≥ 0.05·(1/R)ΣẐ_r) ≥ 0.95 (Markov; the method's bound);
(b) P(Z ≥ δ_R·min_r Ẑ_r) ≥ 0.95 with δ_R = 0.05^{1/R} (δ_4 = 0.473), since P(min_r Ẑ_r > Z/δ) = ∏_r P(Ẑ_r > Z/δ) ≤ δ^R;
(c) Z ≥ Z_𝒯 := m(∅)Σ_{S∈𝒯}γ₁(S) deterministically for any set 𝒯 of scored models;
(d) Z ≥ Z_𝒯 is sure, so max{Z_𝒯, δ_R·min_r Ẑ_r} is a valid 95% lower bound, as is the method's max{Z_𝒯, 0.05·Ẑ};
combining (a) and (b) into a single bound needs a Bonferroni split (97.5% each: 0.025·Ẑ and 0.025^{1/R}·min_r Ẑ_r = 0.40·min for R = 4).
(e) No upper confidence bound on Z follows from any of these without coverage (NG3).
*Guarantee.* A better one-sided interval at no cost (0.47·min instead of 0.05·mean typically improves the bound by a factor
≈ 9 when islands agree), plus a deterministic floor (O1). *Known/new.* (b) is an elementary trick I have seen used informally
(independent unbiased copies under Markov); I cannot cite a source and would present it as elementary.
*Difficulty.* Routine. *Lean core.* All of (a)–(d) given independence and unbiasedness. *Depends on.* EV1.

**EV6. Bias of log-scale summaries.**
*Statement.* E[log Ẑ_r] ≤ log Z and E[log((1/R)ΣẐ_r)] ≤ log Z (Jensen), with log Z − E log Ẑ_r ≤ ½·Var(Ẑ_r/Z)/(1 − ...)
under a second-moment condition; the pooled log-mean-exp is less biased than the mean of logs. The reported
"95% lower bound" is therefore a bound on Z, not on log Z's sampling error, as the method says.
*Guarantee.* Clarifies reporting (O1). *Known/new.* Standard. *Difficulty.* Trivial. *Lean core.* Jensen on finite sums.

**EV7. The evidence identity (bookkeeping).**
*Statement.* Z = m(∅)·Z̄₀·∏_t E_{π_{φ_{t−1}}}[e^{(φ_t−φ_{t−1})d}] exactly, with W_K appearing once (inside ϖ in γ₀); the
estimator replaces each expectation by its particle average; and Z/m(∅) = Σ_{𝕊_K} ϖ(S)BF(S) so Z's normalisation by W_K is the
same as the target's. *Guarantee.* Rules out a class of scaling mistakes; a Lean micro-target. *Difficulty.* Trivial.

### 2.6 PI — PIPs, MPM, general summaries, poolings

**PI1. Consistency in N of every island-level summary.**
*Statement.* For a fixed grid, as N → ∞: PIP̂_rj → PIP_j, H_r(h) → π(h), Ẑ_r → Z almost surely; the terminal L burn-in rounds
are not needed for this limit (the post-bridge population is already π-consistent) and any L ≥ 0 preserves it.
*Guarantee.* O1 at the island level. *Known/new.* Known (Del Moral 2004 strong laws; the terminal-round extension is the
continuity of f ↦ f Q₁ on the finite space). *Lean core.* None (cited). *Depends on.* KN2, EV1.

**PI2. Pooling over islands: Ẑ-weighted pooling is consistent in R at fixed N; equal-weight pooling is not.**
*Statement.* At fixed N, as R → ∞: (a) Σ_r Ẑ_r PIP̂_rj / Σ_r Ẑ_r → E[Ẑ_r PIP̂_rj]/E[Ẑ_r] = PIP_j a.s. (SLLN + EV1(b)); the same for
general h; (b) the equal-weight mean (1/R)Σ_r PIP̂_rj → E[PIP̂_rj] which in general ≠ PIP_j (NG2 gives an explicit two-model,
N = 2 counterexample with a bias of order 1/N that does not vanish in R); (c) the Ẑ-weighted pool has asymptotic variance
Var(Ẑ_r(PIP̂_rj − PIP_j))/(R Z²) and R_eff = (ΣẐ_r)²/ΣẐ_r² is the standard Kish effective number of islands for that ratio
estimator; (d) both pools are consistent as N → ∞ at fixed R (PI1).
*Guarantee.* Justifies v3.1's switch of the primary PIP to Ẑ-weighting and tells the user what R_eff means (O1, O2:
stacking more islands at fixed per-island N is a *consistent* use of parallel resources only under Ẑ-weighting).
*Known/new.* The ratio-of-unbiased-estimators argument is standard (it is the "island / parallel SMC" pooling rule of
e.g. Whiteley, Lee & Heine 2016, Bernoulli, "On the role of interaction in sequential Monte Carlo algorithms", in spirit);
the explicit counterexample for equal weighting is new but trivial.
*Difficulty.* Routine. *Lean core.* (b)'s counterexample and the ratio identity. *Depends on.* EV1.

**PI3. Rao–Blackwell variance reduction.**
*Statement.* Var_π(o_j) ≤ Var_π(1{j∈S}) = PIP_j(1 − PIP_j) (law of total variance), so under perfect mixing
Var(PIP̂_rj) ≤ PIP_j(1 − PIP_j)/(4N) and in general the RB estimator's asymptotic variance is ≤ that of the indicator average
for every kernel (this needs the standard "Rao–Blackwellisation never hurts for reversible chains" argument, which is *not*
automatic for MCMC averages; for iid particles it is). *Guarantee.* O1. *Known/new.* Standard. *Difficulty.* Routine.

**PI4. MPM: a posterior false-discovery guarantee, and why duplicates break it.**
*Statement.* (a) For the exact PIPs, E[|MPM \ S| | y] ≤ ½|MPM| for S ~ π(·|y): the posterior expected false-discovery proportion
of the MPM is ≤ ½, and more generally the rule {j : PIP_j > 1 − q} has posterior FDP ≤ q (Müller, Parmigiani & Rice 2007-type
Bayesian FDR). (b) Barbieri & Berger (2004, Ann. Statist.) optimality of the MPM for prediction holds under orthogonal
designs (and some extensions), not in general. (c) For exact or near-duplicate columns j, l: PIP_j = PIP_l = π(j only) +
π(both) while π(j or l) = 2π(j only) + π(both); when the ridge makes π(both) small, PIP_j ≈ π(j or l)/2, so the MPM excludes
both members of a duplicate pair whose union is almost surely in the model. (d) The general-h summary with
h_C(S) = 1{S ∩ C ≠ ∅} for the reported duplicate components C (or the neighbour-graph components) gives the cluster-level
inclusion probability, and {C : π(h_C) > ½} is the natural cluster-level MPM; it is consistent in N and R by PI1/PI2.
*Guarantee.* States what the MPM does and does not guarantee and gives a provably consistent repair inside the v3.1
reporting layer (O3 under correlation). *Known/new.* (a)–(c) known/trivial; (d) is a recommendation.
*Difficulty.* Trivial. *Lean core.* (a), (c). *Depends on.* PI1, PI2.

### 2.7 HP — HPM, local search, LS0, certificates

**HP1. The HPM is a deterministic, merge-invariant function of the scored set.**
*Statement.* (a) F induces a strict total order on 𝕊_K via (F, −|S|, lex); the HPM is its maximum over the scored set 𝒜 and
depends on 𝒜 only, not on the order in which models were scored; (b) the top-(40p+1) store equals the first 40p+1 elements of
𝒜 in that order; (c) merging per-worker stores by set union then truncation gives the same store as serial processing
(the operation is a commutative idempotent monoid); (d) "provenance = the event at which the model became best" equals
"the model's first fresh score" in any execution, and is schedule-independent if ties in time are broken by the serial order.
*Guarantee.* The HPM decision and the parallel merge are exact (O2, O3). *Known/new.* Trivial. *Lean core.* All (a flagship
small certificate for the parallel layer). *Depends on.* Nothing.

**HP2. Local search: termination, cost, and the meaning of `local_certified`.**
*Statement.* The search performs ≤ ℓ + 1 scans of ≤ p + |S|(p − |S|) ≤ p + K(p − K) scores each, moves only on strict F
improvement, and returns `local_certified` iff the returned model is a strict local maximum of F under single flips (within
the cap) and single swaps; `local_limit` iff the (ℓ+1)-th scan still improves. Every scanned model enters 𝒜.
*Guarantee.* Deterministic cost bound and an exact certificate semantics (O3). *Difficulty.* Trivial. *Lean core.* All.

**HP3. Landscape theorem: under selection conditions S₀ is the unique local maximum and every model has an improving move toward it.**
*Statement (draft).* Under (A1)–(A3) with the constant in (A2) enlarged, with probability → 1 over y, simultaneously for all
S ∈ 𝕊_K with |S| ≤ C s₀: if S ⊋ S₀ then deleting any j ∈ S \ S₀ increases F; if S ⊉ S₀ then either adding some j ∈ S₀ \ S
increases F (when |S| < C s₀) or swapping some j ∈ S \ S₀ for some l ∈ S₀ \ S increases F; and for |S| > C s₀ deleting any
j ∈ S \ S₀ increases F. Hence S₀ is the unique flip/swap-local maximum of F on 𝕊_K, and any local search started at S reaches
S₀ in at most |S Δ S₀| moves (at most ℓ moves if |S Δ S₀| ≤ ℓ), returning it `local_certified`.
*Guarantee.* Under the regime where selection is possible at all, the local search is a *proof* of global optimality once it
certifies, and the HPM equals S₀ whenever any scored model is within ℓ moves of S₀ (O3).
*Known/new.* The "improving move exists" statement is the core lemma of Yang, Wainwright & Jordan (2016) (their canonical-path
construction); the uniqueness-of-local-maximum corollary and its use as a certificate are an easy consequence they do not
emphasise. Needs re-proving for this target (g = n, ridge, BB(1,p), cap).
*Proof route.* Lemma A/B of TG4 applied to single flips and swaps uniformly over S (a union bound over p·C(p, Cs₀)-many
neighbour pairs, which is why the (A2) constant grows).
*Difficulty.* Substantial. *Lean core.* The deterministic inequalities; probability cited. *Depends on.* TG4.

**HP4. Mixing-free selection consistency of the method via LS0 (the deterministic path).**
*Statement (draft).* Under orthogonal blocks and (A1)–(A3) with the σ²-inflation margin of ST8, with probability → 1:
S̃₀ = S₀, LS0 returns S₀ `local_certified`, and therefore the reported HPM equals S₀ — *for every seed and irrespective of the
SMC's mixing or schedule*, because the HPM is the maximum of F over a scored set that contains S₀ and (by HP3) no model scores
above S₀. Under ε-separated blocks (ST5) the same holds for ε ≤ ε₀(κ, s₀, n, p) via ST4. Without the inflation margin,
S̃₀ ⊆ S₀ w.h.p. and the conclusion holds provided |S₀ \ S̃₀| ≤ ℓ (LS0 adds one missed signal per move: HP3 guarantees an
improving addition exists at each step).
*Guarantee.* A selection-consistency theorem for the *algorithm's output* (not just its target) whose proof does not
touch Monte Carlo error — the cleanest route to O3 and, I think, underrated: the tables + DP mode + ℓ-move local search form a
deterministic estimator with a consistency proof, and the SMC can only improve on it. *Known/new.* New.
*Proof route.* ST8 + HP3 + HP1. *Difficulty.* Substantial (inherits TG4/ST8). *Lean core.* HP1 and the DP (ST1(c)); the
statistical part is cited/derived. *Depends on.* ST1, ST8, HP3, HP1.

**HP5. Tables alone solve the problem when S₀ sits in one block.** Trivial corollary of ST7: if S₀ ⊆ C_b and HP3 holds, the HPM
is S₀ after table scoring. (Listed for completeness; it is what "exact local enumeration" buys in the simplest case.)

**HP6. Branch-and-bound certificate and the semantics of `global_certified`.**
*Statement.* With the superset bound TG3(c), a depth-first search over the region 𝓡 = {S′ : S′ ⊆ Ŝ ∪ R, |S′| ≤ K} that prunes a
subtree rooted at S (with remaining candidates R_S) whenever the bound ≤ F(Ŝ) is *exact*: on completion, F(Ŝ) ≥ F(S′) for all
S′ ∈ 𝓡 (ties resolved by the HPM order). The exact branch is the degenerate case 𝓡 = 𝕊_K without pruning, and its
`global_certified` is correct modulo NU1.
*Guarantee.* A regional global-optimality certificate for the HPM (O3). *Known/new.* Furnival–Wilson (1974). *Difficulty.*
Routine. *Lean core.* All (the pruning soundness is a finite statement given TG3). *Depends on.* TG3.

**HP7. NP-hardness of the HPM for this target (negative; see also NG8).**
*Statement (draft).* The decision problem "given X, y (rational, standardised) and a threshold, is there S ∈ 𝕊_K with F(S) ≥
threshold?" is NP-complete; hence no polynomial-time algorithm computes the HPM for all inputs unless P = NP, and no
polynomial-size certificate of global optimality exists in general unless NP = coNP.
*Guarantee.* Explains why `global_certified` is restricted to the exact branch and why the local certificate is the honest
general-case statement (O3). *Known/new.* Known for L₀-penalised least squares and sparse approximation (Natarajan 1995,
SIAM J. Comput.; also Welch 1982 for subset selection); the reduction must be re-done with this *fixed* prior/penalty
structure (the penalty per variable is log(2p/(k+1)) + ½log(n+1) + O(1) and the fit term is ν log Q_S; Exact-Cover-by-3-Sets
instances give Q_S at the ridge floor exactly for covers and bounded away otherwise, so the fit gap dominates the penalty for
n large enough relative to the instance — the standardisation and the cap need care).
*Difficulty.* Substantial. *Lean core.* The gap inequality of the reduction; the NP-completeness framework is cited.

### 2.8 CL — calibration, checks, escalation

**CL1. Termination and cost of calibration.** Trivial: ≤ 2 tiers × [1 pilot (≤ T_e stages) + ≤ ℓ rebuilds × 4 islands ×
(≤ T_e + L + 4) rounds × H_e particles × m scores + grid constructions ≤ 3·61·(T_e + #targets)·|V| lse evaluations + local
searches (HP2)]. *Lean core.* All.

**CL2. The escalation decision is a calibration-measurable event; unbiasedness survives escalation.** (= BR5(b)–(c); listed
separately because the paper should state it as a lemma about the *procedure*, including the "keep score leaders across
tiers" rule, which affects only 𝒜 and V, not the final streams.)

**CL3. What the checks can and cannot detect (power statements).**
*Statement (draft).* (a) E2 (sd of 4 log Ẑ_r > 1 nat): under EV4 with relative SD s of Ẑ_r, the test statistic ≈ s·χ₃/√3, so E2
fires with probability ≈ P(χ²₃ > 3/s²): 5% at s ≈ 0.62, 50% at s ≈ 1.1 — it detects only relative evidence errors of order one
and is blind to common-mode error (all islands missing the same mode: NG1, NG12). (b) E1 (an island's best ≥ 1 nat below the
overall best) detects islands that never scored a top model; it is blind to modes no island scored. (c) E3 (local search
improved the best) detects that the particle system had not reached a local maximum; it is a *necessary* condition for
equilibration near the HPM, not a sufficient one. (d) `low_empirical_ESS` detects weight degeneracy at a stage; with coverage
η at that stage's look-ahead, BR1 bounds its probability under good mixing: P(ESS < 0.5N) ≤ P(empirical χ² > 1) which is
exponentially small in N when the true χ² ≤ 1/9 + 2.2η (concentration of the empirical ESS, a bounded-weights argument
needs osc_t; otherwise a Chebyshev bound with the fourth moment).
*Guarantee.* Honest description of the checks' power for the paper's "diagnostics" section (O1). *Known/new.* Routine.
*Lean core.* None essential. *Depends on.* EV4, BR1.

**CL4. Forced-step semantics** (= BR6).

**CL5. Coverage sufficient condition for the frozen grid.**
*Statement.* If for every interval (u, v] of the frozen grid the candidate set used at the last construction satisfies
π_u(V^c) ≤ η and π_{2v−u}(V^c) ≤ η, then every full-space stage χ² is ≤ (10/9)(1−η)^{−2} − 1, and EV2 applies with that
constant. (Direct from BR1.) The condition is not checkable from the run (NG3/NG4) but is the precise hypothesis under which
the restricted certificate becomes a full one.

### 2.9 PA — parallel layer, work and depth, comparisons

**PA1. Work and depth of the complete method (Brent-type scalability).**
*Statement.* Count scores (each s(k) = O(k³) with k ≤ K). Work W = W_tables + W_cal + W_final + W_local with
W_tables ≤ J2^B, W_cal ≤ 2(1 + 4ℓ)·H_e·(T_e + L + 4)·m (worst case), W_final = R′·N_e·(T + L + 4)·m, W_local ≤ (ℓ+1)(p + K(p−K))
per search. Sequential depth (critical path with unbounded processors, islands and particles in parallel, scoring of a
local-search scan in parallel, resampling by parallel prefix): D = D_tables + D_cal + D_final + D_local with
D_tables = O(s(B)) (all sub-models in parallel), D_cal = O((1 + rebuilds)·(T_cal + L + 4)·m·s(K) + T_cal·log H_e) — the pilot and
each rebuild are sequential in stages and each particle's round is sequential in its m steps —, D_final = O((T + L + 4)·m·s(K)
+ T log N_e), D_local = O((ℓ+1)·s(K)). Hence with P processors, time ≤ W/P + D, and D does not depend on N_e, H_e or R′:
accuracy (∝ 1/sqrt(N_e R′) by EV2/PI2) can be bought with processors at constant wall-clock, which is the precise form of
"scales to p values you could not reach sequentially" (O2). The depth is Ω((T + T_cal)·m·s(k_typ)) for this design because
a particle's Gibbs sweep is inherently sequential and the PI excludes parallelism over variables.
*Guarantee.* The parallel complexity statement the brief asks for (O2). *Known/new.* Routine counting; the Brent bound is
classical. *Lean core.* The counts. *Depends on.* ST6, HP2, CL1.

**PA2. Bitwise determinism of the parallel execution.**
*Statement.* The reported estimates, HPM, near-tie list, stores and flags are functions of (X, y, seed) alone, and the v3.1
worker layout computes the same functions provided: (i) each island's stream is consumed by exactly one worker in serial
order; (ii) per-worker caches never alter values (the scorer is a pure function of S, including its fallback route);
(iii) store merges are the set-union-then-truncate of HP1(c); (iv) all cross-island reductions (log-sum-exp over islands,
Ẑ-weighted PIP sums, R_eff) are performed in island order; (v) the local-search scan's max-reduction uses the total order of
HP1(a). What is *not* schedule-invariant: fresh/logical score counts (cache-dependent), timings, and provenance unless (iv)'s
rule is applied to it. *Guarantee.* O2 reproducibility. *Known/new.* Engineering lemma. *Lean core.* (iii), (v), and the
pure-function claim for the merge. *Depends on.* HP1.

**PA3. Memory.** Peak words = O(np + p² + J2^B + N_e·p/64 + 40p·K + |V|·K + 500p·K) with p² from the Gram/correlation/clustering;
a Gram-free scorer (declared future path) reduces the SMC phase to O(np + N_e p/64) at O(nk²) per score instead of O(k³): the
trade is exact and worth stating (O2). Trivial.

**PA4. Stacking theorem.**
*Statement.* For R′ = 4k islands at fixed N_e declared before final randomness: EV1, EV5(b) with δ_{R′} = 0.05^{1/R′}, PI2 and
PA1 hold with R replaced by R′; the pooled evidence has relative variance Var(Ẑ_r/Z)/R′, the Ẑ-weighted PIP has variance
∝ 1/R′, and the depth D_final is unchanged; the baseline record (islands 1–4) is itself a valid run, so both records are
valid and the expanded one dominates in variance. *Guarantee.* "Parallel scalability over islands" as a theorem (O2).
*Difficulty.* Routine. *Depends on.* EV1, PI2, PA1.

**PA5. Comparison with sequential MCMC for the evidence.**
*Statement (draft).* To estimate Z with relative RMSE ε by a single tempered chain (parallel tempering + TI or power-posterior
TI) over the same geometric path, one needs Ω(T·τ_mix/ε²) sequential rounds, where τ_mix is the rounds-to-mix of the slowest
tempered chain; SMC-BVS needs O(T + T_cal) sequential rounds and N_e R′ = O(T/ε²) particle-trajectories in parallel (EV2 under
perfect mixing; EV3 otherwise, where τ_mix enters N multiplicatively rather than the depth). In words: particles convert the
1/ε² factor from depth into work. *Guarantee.* The honest form of "SMC beats MCMC": not in work, in depth (O2).
*Known/new.* Folklore; stating it with EV2's constants is new. *Difficulty.* Routine. *Depends on.* EV2, EV3, PA1.

**PA6. Separation example: product start versus a single chain from ∅.**
*Statement (draft).* There exist designs (two blocks, a cross-block masked pair whose members each have moderate block-local
evidence q ∈ (0, 1) but near-zero marginal evidence) for which any single flip/swap chain started at ∅ needs e^{Ω(n)} expected
steps to visit the pair (a moat of depth Θ(n) around it: both singles are rejected at rate e^{−Θ(n)}... precisely, the chain
must pass through a single whose posterior odds are e^{−c n}), while the initial population of SMC-BVS contains the pair with
probability ≥ 1 − (1 − q²c_K)^{N} (ST9) and keeps it (its d is Θ(n) > 0). *Guarantee.* A provable advantage of local-to-global
over plain MCMC under correlation (O1, O3 vs MCMC). *Known/new.* New construction; slow-mixing examples for BVS chains exist in
the literature (YWJ 2016 §4 discuss failure without their conditions) but not this contrast. *Difficulty.* Substantial.
*Lean core.* The hitting-probability inequalities (finite). *Depends on.* ST9, NG1's moat lemma.

### 2.10 NU — numerics

**NU1. Rounding-error bound for the score and its consequences.**
*Statement (draft).* With IEEE double (u = 2⁻⁵³), the Cholesky route computes log m(S) with absolute error ≤ c·k·κ₂(H_S)·u·
[ν + k] + (error in Q from cancellation), where κ₂(H_S) ≤ (n+1)(n−1)k + 1 (ridge), so the error is ≤ c′·k²·n²·ν·u ≈ 10⁻⁷ for
n = 200, k = 100 in the worst case and ≈ 10⁻¹² for typical k ≤ 20; the non-negative recomputation of Q removes the
cancellation term. Consequences: (a) the near-tie tolerance 10⁻⁹ is below the worst-case bound for large k, so the near-tie
list should be declared relative to the bound (or the bound reported); (b) `global_certified` on the exact branch is
justified iff the best-vs-second-best gap exceeds twice the bound; (c) the HPM tie rule (exact equality) is reproducible
because the scorer's operation order is fixed. *Guarantee.* Makes certification statements honest (O3). *Known/new.*
Standard backward-error analysis (Higham, *Accuracy and Stability of Numerical Algorithms*, Cholesky and triangular solves).
*Difficulty.* Routine but careful. *Lean core.* None realistic (floating point); the inequality chain is paper-checkable.

---

## 3. Negative results and limitations I expect to be provable

**NG1. Cross-block masked contrasts in a saturated cluster are unreachable at any fixed budget, and every diagnostic passes.**
*Construction (draft).* Fix k ≥ 2 and n. Take a cluster 𝒞 of 2kB equicorrelated columns (pairwise |r| = ρ close to 1) plus
p − 2kB independent noise columns; complete linkage must split 𝒞 (it exceeds B), and for a constant fraction of designs the k
chosen members j₁..j_k of 𝒞 land in k distinct blocks. Let y ∝ Σ_i c_i x_{j_i} with Σ c_i = 0 (a within-cluster contrast)
plus small noise; as computed in SC-style algebra, every proper subset of M = {j₁..j_k} has R² ≤ (1 − ρ)·O(1) while R²(M) ≈ 1.
Choose ρ, n so that each proper subset of M has F below F(∅) by at least δ := log(2p) − O(n(1−ρ)) > 0 per element.
*Claims.* (a) (moat lemma) Every path of single flips/swaps from any model not containing M to a model containing M passes
through a model whose γ_φ-ratio to its predecessor is ≤ e^{−δ} at every φ, for at least k − 1 consecutive steps; hence the
expected number of visits to the moat's innermost layer is ≤ (total steps)·e^{−(k−1)δ}. (b) π₀(M ⊆ S) ≤ ∏_i [ϖ-cost] ≤
(2p)^{−k}·e^{O(k n(1−ρ))}, so the independence proposals hit M with probability ≤ (total proposals)·(2p)^{−k}e^{O(kn(1−ρ))}.
(c) With the method's budget M_tot ≤ W (PA1), P(M ever scored) ≤ W·max(e^{−(k−1)δ}, (2p)^{−k}e^{O(kn(1−ρ))}) =: ε(k), which is
< 0.01 for k ≥ 4 at the study sizes (W ≈ 10⁹, p = 1,000: (2p)^{−4}W ≈ 6·10⁻⁵) — for k = 3 it is *not* small, consistent with my
earlier back-of-envelope that the budget brute-forces three-way masking at p = 1,000 (ST9 is the positive side).
(d) On the event {M never scored} the run is identical in law to the run on the modified score function F′ = F outside
{S ⊇ M}, F′ = F − Θ(n) on {S ⊇ M}, under which all checks (E1–E3, ESS, grid convergence) have their nominal behaviour; so all
diagnostics pass with probability ≥ 1 − ε(k) − (nominal failure rate), while log Ẑ − log Z ≤ −Θ(n), PIP̂_{j_i} ≈ 0 versus
PIP_{j_i} ≈ 1, and HPM ≠ S₀ with `local_certified` = TRUE (NG11).
*Status.* New; substantial (the construction must survive the clustering's tie rules and the neighbour graph: because the
cluster is equicorrelated, N(j_i) contains other cluster members, and swaps within M's complement do not help; the Gibbs
conditional at M's elements evaluates F(S ∪ j_i) which is low unless S already contains M \ {j_i}). *Lean core.* (a)–(c):
union bounds over a finite trajectory space given the per-step acceptance bounds. *Depends on.* ST1, ST9, KN1, PA1.
*What it shows.* The limitation is intrinsic to any sampler built from local moves and product-start proposals; and it is
the exact complement of ST7: masking of order ≤ B *inside* a block is free, masking of order k *across* blocks costs
(2p)^k proposals. It also fixes the meaning of "genuinely correlated design" for this method: clusters larger than B.

**NG2. Equal-weight PIP pooling has a bias that does not vanish with the number of islands.**
*Construction.* Two models {∅, {1}} (p = 1 would be enumerated; take p = 2 with the second variable forced out by a
huge penalty, or state it for an abstract two-state Feynman–Kac model), T = 1 stage, N = 2, no moves. Then PIP̂_r is a
function of two weighted coin flips and E[PIP̂_r] ≠ PIP_1 by an explicit rational amount of order 1/N; averaging over R
islands converges to that wrong value. *Status.* Trivial; Lean-able exactly. Justifies PI2(b).

**NG3. One-sidedness: nothing computed from scored models bounds Z from above or PIPs from below.**
*Statement.* For any set 𝒜 of scored models and any value of their scores, and any target score function F agreeing with
the observed scores on 𝒜, the quantities Z and PIP_j can be made arbitrarily large / close to 1 by changing F outside 𝒜
(trivial), and — the content — the method's *entire output distribution* is unchanged by such a change on the event that no
model outside 𝒜 is scored (NG1(d)). Hence any upper bound on Z or lower bound on a PIP that holds with probability ≥ 1 − α
for all score functions must be trivial. *Caveat (important for honesty).* F is not an arbitrary function: it is determined
by (X, y) ∈ ℝ^{n×p}×ℝⁿ, and a scored set of size ≳ n generically pins y (up to sign) and hence every score. So NG3 is a
statement about score-oracle algorithms, not an information-theoretic impossibility for this model; the information-theoretic
version is false, the computational version (NG8) is the right one. The paper should say exactly this.

**NG4. The restricted grid is blind to V's complement: ρ_V ≥ 0.9 on every interval while the full ESS collapses.**
*Construction.* V = {A}, one hidden state B with γ₀(B) ≪ γ₀(A) and d(B) ≫ d(A): ρ_V ≡ 1 (a single state has ESS 1) so the
grid is [0, 1] in one step, while the full ρ(0, 1) = 1/(1 + χ²) ≈ π₀(B)·e^{2d(B)}/(…) ≈ 0. BR1(b) gives the exact factor:
(1−η_1)²/((1−η_0)(1−η_2)) with η_2 ≈ 1. *Status.* Trivial; Lean-able; it is the formal content of "the pilot cannot see a
mode it has not sampled".

**NG5. Lower bound on sequential depth: crossings must be paid for.**
*Statement.* For any pair-dominated bridge with K separated crossings of gaps D_1..D_K, any ESS-0.9 schedule on the
geometric path has T ≥ Σ_c [log₂(D_c φ*_c/log 9) − 1] + K·c₁ (BR4(a)–(b)); in particular for gaps Θ(n), T = Ω(K log n). No
choice of V, N or seed changes this; only a different path (not geometric, or with a different start) could. This is the
"correlation costs depth" statement in its unavoidable form: competing explanations (proxies in different blocks that
take over at different temperatures) are crossings.

**NG6. An adaptively chosen schedule used directly would bias Ẑ.**
Known: adaptive-ESS SMC estimators are consistent but not unbiased (Beskos, Jasra, Kantas & Thiery 2016, Ann. Appl. Probab.,
"On the convergence of adaptive sequential Monte Carlo methods"), and the bias is of order 1/N. A two-state, N = 2 example
makes the bias explicit (Lean-able). This is the theorem that justifies the pilot/freeze/final architecture; the paper
should state it as the reason for the design rather than as folklore.

**NG7. Decision-rule limitations under duplicates and the cap.**
(a) PI4(c): for an exact duplicate pair the MPM can exclude both although their union has posterior probability ≈ 1;
(b) the MPM can have more than K members, and then it is not a model of 𝕊_K; (c) HPM and MPM can differ for any n (classical:
Barbieri–Berger examples), and the HPM is not predictive-optimal in general. All trivial; worth one remark each.

**NG8. Computing the HPM is NP-hard; certifying it is coNP-hard** (= HP7). Consequence: `global_certified` must stay
restricted to enumeration/branch-and-bound completions; no run diagnostic can be a general certificate.

**NG9. Equivariance holds in law, not per seed.** For a fixed seed the output is not equivariant under column permutations
(the Fisher–Yates order consumes uniforms in label order); the law of the output is equivariant when the dendrogram, cut,
packing and neighbour-graph tie-breaks are not activated. With activated ties (exact duplicates), even the law is not
equivariant. Trivial; the paper should state the invariance claim of §4 precisely in this form.

**NG10. Preprocessing is Ω(p²).** Complete linkage on all pairs reads p(p−1)/2 correlations; any method that clusters on all
pairwise correlations has time Ω(p²) and (as implemented) memory Θ(p²). This is a limitation of the block construction, not
of the SMC; the "Gram-free scorer" future path does not remove it unless the clustering is also replaced (e.g. by a
sparse-correlation screen at threshold r_n, which is Õ(p²) time but O(p + #edges) memory). Trivial.

**NG11. `local_certified` can hold at a model e^{Θ(n)} below the mode.** Immediate from NG1 (the HPM there is a certified local
maximum). Hence the certificate must be read as "no single flip or swap improves", never as "mode found".

**NG12. E1/E2 are blind to common-mode failure.** Immediate from NG1(d): all islands miss the same mode and agree with each
other. The island replication tests *reproducibility*, not *correctness* — the paper should say so in those words.

**NG13 (speculative). No polynomial depth in general.** If the k-way masked construction of NG1 is taken with k ≈ log W/log(2p)
growing, then for any sampler in the class "local moves + product-start proposals" the work needed to find the mode is
≥ (2p)^{k}, i.e. super-polynomial in the masking order; combined with NG8 this suggests, but does not prove, that no
polynomial-work method is exact on all designs. I would state NG1 and NG8 and *not* claim more.

---

## 4. Design conditions

| Code | Condition on X (and y) | Needed by | Covers genuinely correlated designs? |
|---|---|---|---|
| D0 | none beyond finiteness, non-constant columns, non-constant y | TG1–3, ST1, ST2(b), ST6, ST7, ST9, ST10, KN1–4, KN7, BR1–7, EV1–7, PI1–4, HP1–2, HP6, CL1–5, PA1–5, NU1, all NG | yes — these are the exactness/unbiasedness/consistency-in-N-and-R results and the explicit cost functionals (Λ, M_φ, J). Correlation enters them only through computable statistics of (X, y), never through a hypothesis. |
| D1 | **orthogonal blocks**: X_{C_b}ᵀX_{C_b′} = 0 for b ≠ b′, i.e. the design is a union of mutually orthogonal groups each of size ≤ B, and the clustering recovers them (ST5 with ε = 0 requires within-group |r| > 0 and no cross-group ties, or a tie rule that respects groups) | ST2(a), ST3, ST8, HP4 (first form), KN4(c), BR3's O(log p) depth sketch | partially: *arbitrary* correlation **within** blocks (any structure on ≤ B variables, including exact duplicates and within-block masking) is allowed and handled exactly; cross-block correlation is excluded. This is already the regime where split-and-merge with the same groups is biased (ST2: d_σ ≠ 0), so D1 results are not vacuous comparisons. |
| D2 | **ε-separated blocks**: groups of size ≤ B with within-group |r| strictly above all between-group |r| (ST5), and max between-group |r| ≤ ε | ST4, ST5, KN6(c), HP4 (second form), the polynomial versions of KN4/EV3/BR3 (need ε ≲ log p/(n K²)-type smallness for *explicit* polynomial constants) | yes for weak cross-block correlation; the ε needed for explicit polynomial bounds is small (because the fit term multiplies ε by n·R²), which is honest: the bounds degrade continuously, correctness does not. |
| D3 | **sparse-eigenvalue / restricted-eigenvalue**: λ_min(G_S/(n−1)) ≥ κ for all |S| ≤ C s₀ (plus a sparsity-projection condition of the YWJ type for mixing) | TG4, TG5, HP3, KN5, HP4 (statistical part), PA6 | yes: this is the standard condition under which *any* method can select; it allows strong correlation as long as small sets are well-conditioned; it does not control cross-block structure, which is why it gives mixing only at φ = 1 (KN5), not along the bridge. |
| D4 | **beta-min and sparsity**: min |β₀j| ≥ c₀ sqrt(s₀ log p/n), s₀ log p = o(n) (with the (1−R²_tot)⁻¹ inflation margin for ST8/HP4) | TG4, TG5, HP3, HP4, KN5 | — (a signal condition, not a design condition). |
| D5 | **saturated clusters**: a correlation cluster with more than B members (the only situation in which ST5 fails by necessity) | the negative results NG1, NG5, NG11–13 are *about* this regime; the D0 results still hold in it | this is what "genuinely correlated" means for this method. Positive statements available here: D0 results; ST9 (masked sets whose parts have moderate block-local evidence are found at the start); KN5 at φ = 1 if D3 holds; BR4/NG5 (depth cost of each crossing is logarithmic in its gap). Negative: NG1 (cross-block masking of order ≥ 4 at p = 1,000 is out of budget). |

**Masking, precisely.** Three regimes should be named in the paper: (i) masking inside a block (any order ≤ B) — free (ST7);
(ii) cross-block masking whose components have block-local inclusion probability q each — found at the start with probability
1 − (1 − q^k·c)^N (ST9), so "particles" resolve it; (iii) cross-block masking whose components are individually at noise level
— cost (2p)^k proposals (NG1). Correlation structure decides which regime a given masked set falls in through the clustering
(ST5) and B.

**Duplicates and near-duplicates.** Allowed everywhere (ridge; TG1). They affect only decisions (PI4, NG7) and the
equivariance statement (NG9).

**Whether D1/D2 are checkable.** D2's ε is computable from X before the run (max cross-block |r| after blocks are built) and
should be reported on the run card; D3 is not checkable in general (restricted eigenvalues over all small sets) but the
smallest eigenvalue of G_S over the scored top models is a reportable proxy.

---

## 5. Recommended list for paper 1 (ranked) and what to defer

Ranking criterion: value to the three objectives × provability at Biometrika length × Lean-certifiable core. Each main
theorem is listed with the lemmas it needs (IDs from §2–§3). I would aim for 14 main results; the rest go to a supplement
or paper 2.

1. **Main Theorem 1 (headline; §6).** Correctness for every design + explicit cost functionals. Lemmas: KN1, KN2, ST1, BR5, EV1,
   EV2, BR1, BR2, KN4, ST10. *Lean:* KN1, ST1, BR1, EV7, the Doeblin inequality.
2. **Theorem 2 (unbiasedness and R-consistency of the reporting layer).** EV1 + PI2 + PA4: Ẑ_r unbiased; Ẑ_r·PIP̂_rj and
   Ẑ_r·H_r(h) unbiased; Ẑ-weighted pools consistent in R; equal-weight pools are not (NG2). *Lean:* KN7, the N = 2 counterexample.
3. **Theorem 3 (structure of the discrepancy).** ST2 + ST3 + ST4: d = d_σ + d_X, closed form and sign of d_σ, exact
   σ²-mixture evidence under orthogonal blocks, ε-perturbation of d_X. *Lean:* ST2 entirely.
4. **Theorem 4 (sequential depth).** BR3 + BR4 + NG5: T is governed by the thermodynamic length (smooth part) plus
   log₂(gap) + O(1) per crossing (sharp two-sided), with NG5 as the matching lower bound. *Lean:* BR4 entirely, BR2.
5. **Theorem 5 (restricted-grid certificate).** BR1 + CL5 + NG4: what ρ_V ≥ 0.9 certifies, exactly, and what it cannot.
   *Lean:* BR1 entirely.
6. **Theorem 6 (mixing-free selection consistency of the output).** HP4 with ST8, HP3, HP1, ST1(c). The deterministic
   tables → DP start mode → LS0 path returns S₀ under D1/D2 + D3/D4, for every seed. *Lean:* HP1, ST1(c).
7. **Theorem 7 (selection consistency of the target and the landscape lemma).** TG4 + TG5 + HP3 for g = n, ridge, BB(1,p),
   cap. Needed by 6 and 8; the adaptation of YWJ/Narisetty–He is the main statistical labour of the paper.
8. **Theorem 8 (rapid mixing at φ = 1).** KN3 + KN5 (+ KN6(c) for the neighbour-swap routing). *Lean:* KN3 entirely.
9. **Theorem 9 (lower confidence bounds for Z).** EV5 (Markov, island-minimum, deterministic Z_𝒯) + EV6. *Lean:* EV5.
10. **Theorem 10 (the limitation theorem).** NG1 + NG11 + NG12 + ST7 + ST9 as one statement with three regimes of masking
    (§4). *Lean:* the moat union bound, ST7, ST9.
11. **Theorem 11 (parallel complexity).** PA1 + PA2 + PA4 + PA5: work/depth, Brent, bitwise determinism, stacking, and the
    "particles convert 1/ε² from depth into work" comparison. *Lean:* HP1(c), PA2(iii)/(v).
12. **Theorem 12 (certificates).** TG3 + HP6 + HP2 + NU1: the leaps-and-bounds superset bound, soundness of the run-card
    branch-and-bound, exact semantics of `local_certified`/`global_certified` including the rounding bound. *Lean:* TG3, HP6.
13. **Theorem 13 (blocks).** ST5 + ST6 + KN6: recovery of separated clusters, never splitting, block count, graph size.
    *Lean:* ST5, ST6.
14. **Theorem 14 (target).** TG1 + TG2: propriety, bounds, invariances, reduction identity, IG bound. *Lean:* all.

Supporting propositions to include in the supplement: EV3 (explicit finite-N bound with Dobrushin constants), EV4 (CLTs),
PI1, PI3, PI4 (cluster-level MPM), CL3 (power of the checks), BR6/BR7 (forced steps; TI and Ĵ by-products), NG6 (why freeze),
NG9 (equivariance), NG10.

**Defer to paper 2 or later:** HP7/NG8 (NP-hardness with the fixed prior — valuable but a different kind of paper);
PA6 (separation example versus single-chain MCMC — needs its own simulation study); the regularity-free version of BR3;
the explicit polynomial constants of KN4(c)/EV3 under D1 (needs TG4-level machinery just for a constant); a finite-sample
analysis of the calibration loop's convergence (I see nothing provable beyond termination and cost; I would not promise more);
anything about the pilot's *adaptive* schedule beyond BR6 (it is a heuristic by design, and the freeze makes its properties
irrelevant to correctness).

**Two reporting changes that would make theorems cheaper (recommendations, not theorems):** (i) report Ĵ (BR7) and the
cross-block ε (D2) on the run card, so Theorems 1, 3, 4 become statements about reported numbers; (ii) report the island-minimum
lower bound (EV5(b)) next to the Markov bound.

---

## 6. The headline theorem

**Theorem H (local-to-global SMC: correlation costs sequential depth and particles, never correctness).** *Draft; proof
sketch only.*

*Setting.* X ∈ ℝ^{n×p} and y ∈ ℝⁿ pass preprocessing; blocks, tables, π₀, the neighbour graph and the frozen grid
0 = φ₀ < ⋯ < φ_T = 1 are built as in §6 of the method (the grid from streams 0–9 at tier e); R′ final islands with N particles
each run on streams independent of the grid. Let d, d_σ, d_X, Λ, J, M_φ, χ²_t be as in §0. No assumption is made on the
correlation structure of X.

*(A) Correctness at every finite budget.* For every such (X, y), grid and N:
(A1) each Ẑ_r is an unbiased estimator of Z, and Ẑ_r PIP̂_rj, Ẑ_r H_r(h) are unbiased for Z·PIP_j, Z·π(h) (EV1, KN7);
(A2) PIP̂_rj → PIP_j, H_r(h) → π(h), Ẑ_r → Z a.s. as N → ∞ (PI1), and the Ẑ-weighted pools converge to PIP_j, π(h) a.s. as
R′ → ∞ at fixed N (PI2);
(A3) Z ≥ max{Z_𝒯, 0.05^{1/R′} min_r Ẑ_r} with probability ≥ 0.95 (EV5);
(A4) the HPM is the exact maximiser of F over the scored set, which contains every sub-model of every block (ST7, HP1).
None of (A1)–(A4) depends on X beyond the construction of the blocks.

*(B) Where the design enters: three computable functionals of (X, y).*
(B1) *Depth.* Every grid interval satisfies χ²_V(π_{φ_t}‖π_{φ_{t−1}}) ≤ 1/9 (BR1), equivalently (φ_t − φ_{t−1})² Var_{π_ξ|V}(d) ≤
log(10/9) for some ξ in the interval's look-ahead (BR2); consequently T ≤ 1 + ⌈3.08·sup_{φ∈[0,2]} sd_{π_φ|V}(d)⌉, and under the
regularity condition of BR3, Λ_V/0.65 ≤ T ≤ 3.08·Λ_V + 1 ≤ 3.08·sqrt(J_V(π₀, π)) + 1, while each pair-dominance crossing of gap
D contributes log₂(D) + O(1) stages (BR4, NG5). Under orthogonal blocks d = d_σ (ST2), and Λ is then driven by the σ²-coupling
of boundary signals only (O(log p)-type stages in the sketch of BR3); under ε-separated blocks the extra length is controlled
by ST4.
(B2) *Particles.* Under perfect mixing, Var(Ẑ_r/Z) = ∏_t (1 + χ²_t/N) − 1 ≤ exp{T[(10/9)(1−η)^{−2} − 1]/N} − 1 ≈ T/(9N) with η the
coverage deficit of V (EV2, CL5); in general E(Ẑ_r/Z − 1)² ≤ (C/N)Σ_t osc_t·m·M_{φ_t} + O(N⁻²) with M_φ ≤ exp{φ(d_max − E_{π₀}d)}
(EV3, KN4). Thus the particles needed for a relative error ε scale as T/ε² times a factor that is 1 under coverage and perfect
mixing, polynomial in p under orthogonal/ε-separated blocks with strong signals included under π₀ (KN4(c), ST4), and
exponential in the cross-block masking strength d_max − E_{π₀}d in the worst case.
(B3) *Mixing.* At every temperature Q_φ(S, ·) ≥ (mM_φ)⁻¹ π_φ(·) uniformly in S (KN4), and at φ = 1 the gap of Q₁ is at least
half that of the random-scan mixture (KN3), which is polynomial under D3/D4 (KN5).

*(C) Sharpness.* (C1) For pair-dominated bridges the depth bound of (B1) is attained up to an additive constant (BR4, NG5);
(C2) the first-order particle bound of (B2) is attained under perfect mixing (EV2 lower bound); (C3) the exponential dependence
in (B2)/(B3) cannot be removed within the class of local-move + product-start samplers: for cross-block masked contrasts of
order k in a saturated cluster, no budget below (2p)^k finds the mode with probability bounded away from 0, and all run
diagnostics pass (NG1, NG12).

*(D) Comparison.* π₀ is exactly the split-and-merge posterior with the same blocks; its Jeffreys error J(π₀, π) = ∫₀¹ Var_φ(d) dφ
(ST10) is the same functional that bounds the SMC depth in (B1): SMC-BVS removes the split-and-merge bias at a sequential cost
of order sqrt(J) stages and a particle cost of order T/ε², instead of a bias that does not vanish with any resource.

*Scope and honest limits.* (A) is unconditional; (B1)–(B2) are explicit but their constants are sharp only under coverage of V
and perfect mixing (EV2) or at the price of the Dobrushin constants (EV3), which are polynomial only under D1/D2 with
block-locally strong signals; (B1)'s identification with Λ needs the regularity condition or the crossing count (BR3/BR4);
(C3) is the matching lower bound only within the sampler class and only for masked contrasts spanning several blocks. The
theorem says nothing about the pilot's adaptive schedule or the rebuild loop beyond "they produce a grid" (BR5).

*Proof sketch.* (A) is Del Moral's unbiasedness and strong law applied to the Feynman–Kac model of KN2 with the terminal
rounds (KN7), conditional on the calibration σ-field (BR5), plus the SLLN for the Ẑ-weighted ratio (PI2) and Markov/product
bounds (EV5). (B1): BR1(a) identifies the certified ESS with χ²; BR2 is the second-order mean-value theorem for the finite
log-sum-exp; summation gives the sup bound; the regularity condition turns the sum into a Riemann sum for Λ_V; ST10(e) is
Cauchy–Schwarz; BR4 is explicit two-point algebra. (B2): under perfect mixing the stage factors are independent with relative
variance χ²_t/N; BR1(c) bounds χ²_t; in general cite CDG 2011 with KN4's minorisation. (B3): KN4 is the Doeblin bound through
the independence label placed first with probability 1/m; KN3 is the two-line Dirichlet inequality. (C) and (D) are the
constructions and identities of BR4, EV2, NG1, ST10. *Lean-certifiable core:* KN1, KN2, ST1, BR1, BR2 (modulo MVT), BR4, EV2's
product identity, EV5, KN3, KN4's minorisation inequality, ST2, ST10 — all finite-state or finite-real-parameter statements.

---

## Appendix A. Sanity checks run (one core, R 4.x, under one minute each)

**SC1 (orthogonal-block discrepancy identity, supports ST2).** n = 60, p = 8, two blocks of 4; block 2 orthogonalised against
block 1 after centring (max cross-block |G_jl| = 7.5·10⁻¹⁵ after standardising); y = x₁ + 0.8x₆ + noise, standardised.
Score exactly as §5 of the method (a₀ = b₀ = 0.01, g = n, ridge 1). Over all 219 models of size ≤ 5:
max |d(S) − d_σ(S)| = 5.4·10⁻¹⁴, d_σ ≥ 0 throughout, max d = 7.54. Example S = {1, 6}: u = (0.280, 0.297), d = d_σ = 5.396
(the second-order approximation ν u₁u₂ = 2.50 underestimates at these R²; the exact expression is the right object).

**SC2 (stage counts of the exact bisection rule of `v3_calib.h`, supports BR3/BR4/NG5).** Implemented `rho = exp(2F(v) −
F(u) − F(2v−u))`, threshold 0.9, 60 halvings, targets {1} only (so every step is a bisection), log-space weights.
Two states d = (0, D), log γ₀ = (0, −D/2) (crossing at φ* = ½): stages = 11, 12, 14, 17, 19, 21, 23 for D = 20, 50, 200, 10³,
5·10³, 2·10⁴, 10⁵ — i.e. T ≈ log₂D + 6.7 ± 0.5; the thermodynamic length Λ = π (= 3.142 to three decimals for D ≥ 50) predicts
9.7 stages and is therefore too optimistic for crossings. Three states with two separated crossings (gaps 400 and 800 at
φ* = 0.25 and 0.75): 28 stages ≈ sum of the single-crossing counts. Gaussian spread of d under a flat γ₀ (20,000 states,
d ~ N(0, s²)): stages = 4, 9, 15, 18 for s = 1, 3, 10, 30, against Λ/0.3246 = 3.1, 8.9, 15.8, 19.2 — within 10%, confirming the
thermodynamic-length rule for smooth spreads (the tilt concentrates the population, so T grows much slower than 3.08·s).

Scripts: `check1.R`, `check2.R` in the session scratchpad (not part of the project folder; reproducible from the description
above).

**Not run (and should be, before any of these are promised):** an end-to-end exact-vs-SMC comparison on a D1 design using
the ST3 oracle at p ≈ 200; a k = 3 and k = 4 instance of the NG1 construction at p = 1,000 with the production budget.

