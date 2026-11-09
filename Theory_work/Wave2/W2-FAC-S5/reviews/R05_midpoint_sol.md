# Independent midpoint review — W2-FAC-S5

**Verdict: CONTINUE.** Tier 1 is sound under the stated statistical and implementation hypotheses and with the dependency qualifications retained in L5. I found no fatal or major gap and no reason to restate (C1)–(C4-R). The programme is worth continuing toward KL. The present result is a reduction theorem, not unconditional discovery or consistency beyond the previously established range. Failure to prove KL must leave the ticket PARTIAL, as the statement already requires.

Reviewed independently from the locked STATEMENT and L1–L5. I consulted the permitted SoP/FINAL sections and FACB statement and proof files to check the score, posterior, cap and delivery interfaces. I did not read LOG.md, CHECKPOINT.md, prior reviews, or numerical summaries. Status assertions embedded in the supplied files were not treated as evidence that their arguments are correct.

## Tier 1: checks that matter

**L1: the reduction and regularisation errors are adequate.** The Gaussian representation follows from the orthogonal design/noise projections. The BCS inverse formula and eigenvalue floor are correct. The posterior normal equation for the common factor gives

\[
e_R=\frac{h/\rho_b-\sum_g\sum_{j\in R\cap G_g}y_j/(d+b|R\cap G_g|)}{\rho_b^{-1}+\sum_g|R\cap G_g|/(d+b|R\cap G_g|)}.
\]

Within a group, the residual of predicting an unretained coordinate from its retained mates is independent of the retained observations and of h. Thus the decomposition into the group residual and the common-factor error, its variance, and the bound by |A|+κ₀|e_R| are valid. These are identities for each deterministic set; substituting a selected set uses their simultaneous algebraic validity, not a claim that a statistic remains standard normal after selection.

The score increments use the correct prior ratios and Schur complements. For null moves over a base containing S₀, the signal leakage is a⁻¹β̃ᵀϑ, giving the stated √k/n^(3/2) contribution in addition to the k/n² perturbation terms. The determinant remainder is uniformly o(1) in the path regime. The RSS comparison gives M_T=½(1+o(1)) uniformly over all supersets of S₀ because p=o(n); L3 correctly does not extend that assertion to p comparable to n.

**L2–L3: the start and probability event work.** The nonzero partial covariances range over finitely many incidence patterns, so FS-BCS supplies a fixed positive gap. This makes every nonzero block-table addition dominate its logarithmic penalty even when p≤n/2. Zero pairs occur only in the block containing all truths and have negative table increments. The resulting single-flip argument proves uniqueness of S*, rather than merely local optimality. The Gaussian unions in L3 involve O(p) group/mate pairs and only finitely many truth or special-block pairs; the stated cutoffs give probability tending to one. No union over the entire subset lattice is being smuggled into E_A.

**L4: all competitors are covered, including swaps.** CC controls e_T and e_(T−j) for *every* retained null j, not just the deletion selected by Π. Consequently the null statistic bound applies to a deletion, an addition, and an addition after any null deletion. The last of these is essential: a swap decomposes exactly into its outgoing deletion plus the addition from that deletion's base. Each such addition is negative by a logarithmic margin, while its outgoing deletion cannot beat the best null deletion. This proves the claimed comparison against every null-out swap, including swaps involving N₀. It does not need a within-group re-add invariant.

Truth-removing moves are handled separately and correctly. The Gram floor leaves order-n omitted-signal energy even after a replacement variable is added. E3 and the all-set common-factor bound control the cross term uniformly; the full noise projection costs at most O(p+n^(2/3))=o(n). Ridge residual errors are O(1), and size/determinant terms are logarithmic. Thus the order-n negative truth-move bound does not depend on CC. The terminal index in CC supplies the addition bound at S₀. Exact-score selection and the same tie rule make the path induction valid without assuming the deletion ranking of an approximate score.

**L5: the probability and delivery transfers are in the right direction.** The energy, eigenvalue and beta-min hypotheses of T03♯ hold, hence the posterior error has expectation tending to zero by boundedness. The deterministic LS0 event satisfies E_n∩CC_n⊆𝒦_n, so P(𝒦_nᶜ)≤P̃(CC_nᶜ)+o(1). There is no need for independence here. The enlargement preserves the data law; CC need not be observable from the data. The cap exceeds the required number of moves, and enumeration branches already supply discovery. Operational closure bounds D_n by failure of discovery; it is not used backwards. Delivery then follows from the separate pathwise posterior/discovery inclusion and Proposition F's machinery, with the amended allocation and fallback expressly required. This remains an ideal-machine result relative to the inherited premises and audits.

## Is CC meaningful?

Yes. Π is an oracle *forced-deletion* path defined for every data realisation, whether its moves improve F or not. Defining this path does not assert that the unrestricted search follows it. CC is a sufficient bound on Gaussian prediction errors along that independently specified path and its one-null-deletion bases. The proof then shows the unrestricted path agrees. This is a legitimate reduction, not an assumption of the desired algorithmic conclusion. FS-BCS forces the start structure, and the structural hypotheses imply exact-posterior consistency; neither supplies search discovery in the substantive growing-p regime.

There are concrete feasibility and non-vacuity checks:

* **Some parameter choices make CC empty.** For p→∞, k₀=p−O(1), so Λ_(k₀)=log n+o(1). Since the left side is at least H_q², if log p/log n→a>(1−δ)/2, CC is deterministically false eventually. At equality, lower-order terms still matter; for p asymptotic to n^((1−δ)/2), the positive log-log term already defeats the condition. This does not invalidate the conditional theorem for arbitrary δ, but it rules out KL for such a δ and growth range.
* **CC is not merely satisfiable on exceptional finite-dimensional data.** Put a*=limsup log p/log n and κ₀=(1−ρ_b)^(-1/2). On E_n, simultaneously for all R, |e_R|≤G_n+2L_n. Hence CC holds for all sufficiently large n on E_n whenever
  \[
  2a^*(1+\kappa_0)^2<1-\delta,
  \]
  using Λ_k≥log n−2 and L_n=o(√log n). Thus P̃(CC_n)→1 in a nonempty polynomial-growth range without any path argument. For the S5 correlations, δ=0.1 and a*=0.05 satisfy this conservative inequality. Such p grows faster than log n, so this is not just eventual exhaustive enumeration. This witness does **not** establish the desired improvement beyond 1/6.
* **It is not a finite-sample tautology.** The terminal set is always S₀ and e_(S₀) has positive Gaussian variance V_(S₀). Its unbounded support precludes CC holding almost surely at a finite n with a finite threshold. Conversely, when H_q²<(1−δ)min_k Λ_k, a sufficiently small neighbourhood of h=y₁=⋯=y_p=0 satisfies the common-factor inequalities for every set and has positive probability.

The open part is genuinely quantitative: prove a suitable probability bound for these adaptively selected centres and all their null-deletion bases in a range above 1/6. Unconditional success could still hold when this particular sufficient event fails. KL is the obstruction to *this reduction route*, not a necessary condition for statistical or algorithmic success.

As an additional falsification check, I ran an independent, self-contained Python 3.13 calculation on 240 BCS instances (ρ_b=0.3, ρ_w=0.7, groups of size at most 3, p∈{2,5,9,12}, n=10⁸; random truth locations, method blocks different from the BCS groups). The Gaussian residual/variance identities agreed within 8.33×10⁻¹⁶. In 156 instances passing CC and the checked E1/E2/E3/E_A cutoffs, exhaustive flip/swap comparisons along the forced path produced zero violations of the tested logarithmic margins or truth-move negativity. This is a finite-dimensional algebra/scan check, not evidence establishing KL or an asymptotic substitute for the proof above.

## Numbered issues

1. **MINOR — stale Tier-2 parameter and quantifiers.** Location: `STATEMENT.md:41–42`. The overview still describes KL using an undefined c>0, α(c), and “if every c>0 works,” although the locked condition and (C5) use δ. This is leftover wording from a different centre condition and obscures the actual feasibility restriction. **Fix:** use δ consistently and state: for a chosen α₀<1/2, seek a fixed δ>0 with α₀≤(1−δ)/2 and P̃(CC_n(δ))→1 throughout that range. The ideal claim is “for every α₀<1/2 there exists such a δ,” not an unspecified assertion about every c. No change to Tier 1 is needed.

2. **MINOR — unsupported BCS sharpness assertion outside the theorem.** Location: `lemmas/L4_path.md:81–82` (L4.6, remark 2). “Then (b) fails as soon as … >1/6” and “same computation here” go beyond the supplied BCS argument. A large |e_T|, or failure of its sufficient envelope, does not by itself prove that an actual swap beats the best deletion: the joint group residuals and their signs also enter. The cited CS sharpness result can support the CS benchmark (and an obstruction for the whole class, which contains singleton groups), but a fixed non-singleton BCS/S5 assertion needs an explicit construction and score comparison. **Fix:** restrict this remark to the checked CS benchmark/failure of the sufficient lattice estimate, or supply the BCS construction and comparison. This does not affect L4's proof or require changing the locked Tier-1 target.

**Fatal issues: none. Major issues: none.** Continue the proof programme; retain the conditional/PARTIAL framing until KL is proved and checked.
