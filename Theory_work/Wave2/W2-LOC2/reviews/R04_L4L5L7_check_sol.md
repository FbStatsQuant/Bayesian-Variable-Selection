# R04 — Line-by-line check of L4, L5 and L7

**Verdicts**

- `lemmas/L4_LOCd.md`: **VERIFIED-WITH-AMENDMENTS** (findings 1–2).
- `lemmas/L5_assembly.md`: **VERIFIED-WITH-AMENDMENTS** (finding 2).
- `lemmas/L7_delivery.md`: **VERIFIED**.

No FATAL or MAJOR finding. The two amendments below repair incorrect intermediate statements without changing the hypotheses or conclusions. These verdicts are conditional on the named inputs and implementation premises, with their existing status qualifications. In particular, L1_toolkit, L2_NAR and L3_CTd are treated as given, as requested.

## Numbered findings and fixes

1. **MINOR — L4:81: the automatic PTV calculation is false for negative truth coefficients as displayed.**

   The setting permits either sign of θ*_j. The equality
   `Cov(W_j, Σ θ*_k W_k | W_U) = θ*_j Var(W_j | W_U)`
   is correct, but its claimed lower bound `≥ c_B θ_lo` is false whenever θ*_j < 0. For example, take independent unit-variance coordinates, one truth with coefficient −1, and U empty. The displayed covariance is −1. This counterexample persists along an asymptotic sequence; it is not a finite-n objection.

   **Fix:** replace the concluding display with

   `|Cov(W_j, Σ θ*_k W_k | W_U)| = |θ*_j| Var(W_j | W_U) ≥ c_B θ_lo`.

   PTV is already defined with an absolute value, so this repairs its verification and leaves the theorem intact. No positivity assumption on the truth coefficients should be added.

2. **MINOR — L4:97 and L5:23–24: correct the justification of q ≤ K_n.**

   L4:97 asserts `|Q| ≤ (log n)^(κ+1) ≤ K_n eventually`. The second inequality need not hold: for a fixed-p sequence, K_n = p eventually while the logarithmic expression diverges. Even growing p can be smaller than that upper envelope. The conclusion q ≤ K_n is nevertheless true. L5:24's parenthetical “the dichotomy and K_n ≤ p” also omits the needed argument in the Q = [p] branch: K_n ≤ p supplies the wrong direction to conclude p ≤ K_n.

   **Fix in both places:** write

   `q ≤ p, and q ≤ (log n)^h = o(n); hence q ≤ floor(n/2) eventually and q ≤ min(p, floor(n/2)) = K_n.`

   Use h = κ+1 in L4 Part B and h = κ in L5. Equivalently, handle Q = [p] separately: p = q is polylogarithmic, so K_n = p eventually. L4 A.5 correctly cites L1.2 for this fact and needs no corresponding change. This is an asymptotic proof correction, not a request for finite-n hypotheses.

## Delta audit: L4 Part A and its inherited sources

I read APP L3_LOC §§L3.2–L3.8B, GROW L6_random_AR1 §§L6.2–L6.7 and §7, and GROW L3_sandwich. The surviving uses of logarithmic cardinality, line geometry and AR(1) structure are accounted for as follows.

| Step | Source dependence and check |
|---|---|
| A.1 / APP L3.2 / L6.2 | Entrywise concentration uses only Gaussian rows, unit marginal variances, p ≤ n^A, and the independent noise coordinate. For sets of size J = polylog(n), the sample operator error J·O(√(log n/n)) still tends to zero. L1.2 explicitly supplies this replacement. The posterior sparse cutoff m♯ remains O(log n), independently of q. Energy is bounded by the fixed number and magnitudes of true coefficients. TV uses PTV and bounded-dimensional inverse perturbation. The lattice score family is handled by L0′ rather than incorrectly described as polynomial in n. |
| A.2 / APP L3.3 / L6.3 | The only geometric counting is the size of H_l. Packing yields O((log n)^d), and at most 15 conditioning variables gives O((log n)^(15d)) patterns. The recursive correlation calculation still has bounded dimension, so its O(ħ_n²) correlation error and O(n ħ_n³) squared-statistic error are unchanged. CD_d applies after arbitrary conditioning, including the selected local subset. Distances to l and to every truth are both included in H_l; neither far-covariance estimate is lost. |
| A.3 / APP L3.4 / L6.4 | The covariance vector for regression on the truth residuals has fixed dimension s₀ and entries bounded by K₂ exp(−t₂ d_n). The conditional covariance floor gives the asserted α bound; bounded-size regression gives the b_j bound. Thus the centred mean perturbation has bounded norm. Gaussian regression supplies an isotropic innovation independent of W_(U₀∪S₀). Crucially, Y's random true-column normalizers depend only on those conditioned columns, so the inherited spherical conditioning remains valid. As in the source, use CN_D before integration, not a sphere law conditional on A_cov. |
| A.3 tail/count rates | The enlarged pattern count contributes exp(O(log log n)); the spherical shift contributes exp(O(√log n)). Together these are n^o(1), uniformly over k. Thus E[1_Acov J(t_n(k))] ≤ k n^(−1/2+o(1)), and the maximum-statistic tail in (6.7) is n^(−1/4+o(1)). The p·L_n exp(−c√n) error remains negligible. No q-dependent exponential enters either count. |
| A.4 / APP L3.5 / L6.5 | Per-block optimality and the exact prior ratio are deterministic and independent of geometry. The counting inequality k ≤ k₀+16J(t_n(k)) still holds with k₀=q+16s₀. The ladder has O(log n) relevant indices because K_n ≤ n/2, irrespective of the polylogarithmic size of k₀. Its probability bound still vanishes. Truth additions use only fixed-size TV and a polynomial union over truth/conditioning pairs. In the enlarged branch q=p=polylog(n), K_n=p eventually; otherwise the feasibility dichotomy gives room for an addition after the ladder. The final deletion margin remains positive because log(2k₀)=O(log log n). |
| GROW L3_sandwich | L4 does not silently retain its NEG(η) hypothesis or its W_b count. Those parts are replaced by L6.3–L6.5's full RSS-normalized add-statistic tail and J count. The retained per-block optimality, prior ratios and truth-addition reasoning do not require one-dimensional geometry. |
| L6.6 / APP L3.6 | Neither the AR(1) nearest-neighbour innovation count nor APP's O(log n)-size projection-error estimate is imported. A.5 replaces this entire step with NA-R. |
| A.6 / APP L3.7 / L6.7 | L0′ controls the larger lattice family. With fixed beta-min, missing-truth signal is bounded below by a positive constant times n and dominates every polylogarithmic error term. The old claim that all such errors are O(log n) is not needed. Conditional bounds are uniform over the regularity event and can be integrated. |

The relevance construction actually gives q=O((log n)^d), including enlargement, as required by locked STATEMENT D1. The weaker displayed envelope (log n)^(d+1) merely absorbs constants and suffices for the toolkit. Fixed d is essential throughout.

### A.5: explicit (R1)–(R3) check

- **Windows/frames:** T′ ⊆ T ⊆ Q and l ∉ T, so each proposed frame is a deterministic population residual functional. Radius log log n tends to infinity, and packing gives log N_n ≤ log p+O((log log n)^d)=log p+o(log n). There is no fitted frame or random coefficient. Counting all subsets of B_l, even those not realized by lattice T, is a valid upper bound.
- **Atoms/decomposition:** zero-pad β_(T′) into T. Then e_T = e_(T′)−W_T(β_T−β̄_(T′)) exactly. All its atoms belong to Q and have variance one. RB bounds both coefficient vectors uniformly, so their difference has ℓ¹ norm at most 2L₀, independently of q. Consequently the atom cost is O(log log n), not O(q).
- **Variance ratio:** TAIL gives Var(e_(T′))=Var(e_T)+Var(D) ≤ Var(e_T)+κ(log log n). The floor c converts this to R3. Even a very small fixed decay exponent suffices: κ(log log n)→0. NA-R only needs η_n→0; it does not demand η_n log n→0 or an o(1) difference between normalized statistics. This avoids imposing an unwarranted stronger rate.

## Delta audit: L4 Part B

After finding 1's sign correction, F1–F3 supply the required population facts. Conditional independence of distinct groups is preserved because the Gaussian law factors by groups; conditioning on a subset of coordinates does not couple them. The global floor is c_B. An upper spectral bound is unnecessary: bounded-dimensional covariance matrices have upper norm bounded by their dimension under unit diagonal, energy uses only s₀ fixed true columns, and the remaining inverse estimates use lower floors.

For sandwich selection removal, H_l=G(l)∪Q⁰ contains l's entire group and every truth group. Thus all relevant far population covariances are exactly zero, with O((log n)^(15κ)) possible conditioning patterns. For l outside Q, its group is truth-free; regression on the truth residuals has α=0, so the spherical shift is exactly zero. A.4's ladder and deletion margin continue to apply with polylogarithmic k₀. Neither APP's B-χ bound nor its enlarged-case small-logarithmic bound survives into this proof; both were NA-specific and have been replaced.

### B.2: explicit latent/frame/atom check

The latent extension construction is valid. Start with the independent factor/idiosyncratic Gaussian representation for each one-factor group. Its W marginal is the given group law. Sampling its Gaussian conditional kernel given each observed W_G, independently over rows/groups using fresh auxiliary randomness independent of (W,ε), reconstructs precisely that joint law. The resulting extension may be singular; L2 permits singular extensions. It is iid by rows, jointly Gaussian, and independent of the entire noise vector. When b_v=0, ξ_v=W_v causes no problem.

For bounded groups, β_T(l) is supported in A=T∩G(l); a single exact-residual frame and zero atom coefficients work. At most p2^g₀ such frames are needed, and R3 is equality.

For one-factor groups, D_A is uniformly positive and Sherman–Morrison gives exactly the displayed β_A. In particular,

`b_l−β_Aᵀb_A = b_l/(1+s₂)`.

The first two terms therefore belong to span(F_G,ξ_l), a frame of fixed dimension two independent of A. Each subtracted ξ_v has v∈A⊆Q. Nonnegative loadings and the positive lower bound on nonzero loadings give the stated uniform ℓ¹ bound 1/b_lo; zero loadings contribute nothing. Because l∉A, these atoms are independent of both frame members within the generative representation, giving the exact variance identity τ²=ϱ²+Σλ_v² and R3 with η_n=0. For empty A the same identities hold with s₂=0 and empty sums. The combined family has log N_n≤log p+O(1), at most q atoms, and O(log log n) atom cost. Thus there is no hidden union over 2^g_n frame directions.

## L5 assembly check

After finding 2, all lattice models and the contrast sets used by GROW L2 are feasible or contained in Q∪{l} with the required sample floor. The local population floor (N1) is sufficient for C-i: the enlarged family in GROW L2.0, including truth-deleting swaps, stays in such sets. Fixed beta-min and L0′ give TL; NA-R and the score reduction give NA. Neither TV nor a global sparse floor is needed once sandwich is assumed.

The pathwise GROW L1.2 argument does not impose any cardinality bound beyond q≤K_n. The shipped cap is at least the number of extras, so it scores S₀ and completes its certifying scan. [OP] is used in the correct direction. The event bound for D_n needs no independence between its three events.

C-ii correctly adds LSF rather than inferring posterior concentration from (N1). APP POST supplies the joint-law O_P rate via its uniform diagonal tightness argument. Boundedness of 1−π(S₀) then gives convergence of its expectation to zero; no expectation rate is asserted. Integrating M5(0) and subtracting the error event from output gives exactly the two reported-model conclusions. Both L4 classes have a global floor, so they satisfy this additional premise. No circularity arises: L4 supplies the three events before using L5 for the consequences.

## L7 delivery check

The comparison with FACA L7 and FIN s6 passes. Nonconstant columns and a nonconstant centred response hold almost surely; the scorer positivity argument does not require full sample rank. The declared allocation imports the amended W_G/M_G envelopes and A4's added preflight bounds, with the raw dimension. Its worst-case LS0 count depends on K_n, not on the probabilistic size of Q. Thus enlarging the relevance set causes no new unbudgeted scan term. The total frozen-grid fallback is part of the hypotheses.

Step 3 independently bounds P(𝒦_nᶜ) by the three data-event failures; it does not reverse [OP]'s inequality for D_n. The posterior input follows from L5's LSF clause, supplied by both classes. The scored-set argument is pathwise and independent of CAL or successful restricted-ESS calibration. Together with the delivery result it proves the unconditional consistency conclusion. The final qualifications retain the e4/N3 and S.3 audit limitations rather than upgrading those inputs.

## Numerical evidence and limits

I read `numerics/D1_SUMMARY.md` and `numerics/n4_out.txt`. Their component-port paths and sampled/adversarial lattice searches are observations, not uniform proofs. The logged 1.0009 ratio is a sample norm ratio; the R3 verifications above use population variances and TAIL or an exact latent variance identity. Neither the numerical lattice maxima nor their finite sample margins are used to infer an asymptotic event. No finding above concerns finite-n performance.

**Disposition:** apply findings 1–2 to the indicated proof lines; the reviewed asymptotic results then stand with the inherited dependency qualifications.
