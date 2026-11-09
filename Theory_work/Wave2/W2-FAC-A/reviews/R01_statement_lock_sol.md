LOCK-WITH-CHANGES

1. **Make the hypotheses of each clause explicit; do not derive H0 from sparsity.**

   Fix STATEMENT.md:100–106 by adding: “(L2) assumes G, the energy bound in H0, (AG), (P), and (TV). (L3) assumes G, (H0), (AG), and (P). (L4) additionally assumes (TV) and the named method premises. (L5) retains fixed s₀, fixed σ² > 0, fixed nonzero signal coefficients on S₀, and the method premises of (L4), interpreted conditionally on the design.” Name the event in (L2) Sand_n and replace P(L2ᶜ) by P(Sand_nᶜ).

   Replace PLAN item 4's “H0 from (AG) ... ‖μ‖² ≤ Mn since θ* is s₀-sparse” with: “(AG) supplies the anchored eigenvalue conditions with fixed constants. The energy bound and BM-∞ remain assumptions in the general fixed-design theorem. For fixed, bounded nonzero signal coefficients they follow from fixed s₀, unit column norms, and the Gram floor.” Sparsity alone does not bound coefficient magnitudes or imply beta-min. For example, a fixed-support coefficient growing like n violates the asserted energy implication, while a coefficient of order n^{-1/2} violates BM-∞. The general theorem already assumes H0; retain it rather than silently replacing it by a false implication.

2. **State the L1 coupling, uniformity, and small-s_T control precisely. The exact decomposition applies to the factor Gram, not to an arbitrary approximate Gram.**

   Replace the end of STATEMENT.md:99 with: “For the exact factor Gram, put s_T = λ_TᵀΨ_TT^{-1}λ_T, U = T ∩ g(l), and W_T = (ξ₀ − λ_TᵀΨ_TT^{-1}ζ_T)/√(1+s_T), where g = λξ₀+ζ, ξ₀ and ζ are independent, and ζ ∼ N(0,Ψ). The displayed Gaussian decomposition is exact for this g. Under (AG), transfer the bound by coupling to this factor-Gram Gaussian vector with a uniform additive error O_P(δ_n√(p log log n)) = o_P(1). The o(1) terms and the constant in O(√(log log n)) are deterministic and uniform in T,l; constants depend only on the fixed class parameters.” Include the empty-set conventions.

   In PLAN item 1(a), replace “the factor part ... is bounded uniformly by κ̄ √(top-h mean ...)” with an explicit split. If h_T is the number of groups meeting T and V_g = ζ_gᵀΨ_gg^{-1}ζ_g, then

   |λ_TᵀΨ_TT^{-1}ζ_T| ≤ √s_T √(Σ_{g:g∩T≠∅} V_g),

   and the normalized factor contribution is at most

   |ξ₀| + κ̄ [s_T/(1+s_T)] √((1/h_T)Σ_{g:g∩T≠∅} V_g).

   Here s_T ≥ c_min h_T and h_T ≥ |T|/γ̄. The V_g are independent χ²_{|g|}; partial-group quadratic forms are bounded by these full-group forms. Use a simultaneous top-h bound for every h. This handles small s_T without assuming c_min is uniformly bounded away from zero. The common ξ₀ term cannot simply be dropped; it fits the stated O(√(log log n)) allowance, including T=∅. I find the decomposition and the proposed leading bound plausible with this repair. No extra lower bound on c_min appears necessary: its possible decay is compensated by the stated κ bound.

   In PLAN item 1(b), add: “For a_M(T,l) = (e_l − embedded M_TT^{-1}M_Tl)/√M_{l|T}, prove sup_{T,l}‖a_R−a_Σ‖ ≤ C(ψ₀)δ and sup‖a_M‖ ≤ C(ψ₀), then use ‖Σ^{1/2}−R^{1/2}‖ ≤ C(ψ₀)δ.” These assertions are credible despite ‖Σ‖_op = O(p): the regression vector has bounded Euclidean norm because its fitted variance is at most M_ll = 1 and M_TT has a fixed floor; Schur complements can be compared using the two minimizing residual vectors. The square-root difference bound uses a lower spectral bound, not an upper one. Since tr R = tr Σ = p, the Gaussian vector norms have the required high-probability bound. Do not substitute an estimate involving ‖Σ‖_op or assume the coupling matrix is orthogonal.

3. **Repair the growing-lattice score proof, especially TL under BM-∞.**

   Replace PLAN item 3's “TL ⇐ signal θ²_min(n−1)ψ₀/2 vs uniform noise O(√(n log p))” with: “For a truth-removing neighbor A of T, Λ_A ≥ (n−1)(ψ₀/2)θ_i^{*2}. Bound the signal-noise cross term by C√(Λ_A(log p+log log n)), and the noise projection difference by C(log p+log log n), uniformly over these neighbors, using L1 and one- or two-dimensional nested projection decompositions. BM-∞ then makes both errors o(Λ_A).” A generic O(√(n log p)) error does not prove the stated theorem: BM-∞ allows Λ_A much smaller than √(n log p).

   Also make the uniform expansion a new lemma rather than an invocation of the old O(log n)-model toolkit. State an NA expansion with error o(log n), uniformly in k and the lattice, and the corresponding TL comparison. The determinant and ridge bounds in the plan are promising, but one must track response normalization and the RSS floor quantitatively enough that the coefficient error times O(log p+log log n) is o(log n). For example, ‖P_[p]ε‖²/σ² = O_P(p+log log n) and χ² concentration for ‖Cε‖² give a polynomially vanishing relative RSS error under (P). The family is exponential; C-GROW L0/L2 cannot be imported with their original polynomial family count. This is a proof obligation, not a counterexample to the proposed result.

4. **Record the exponent calculation and restrict the sharpness language to what Part II proves.**

   After the α₀ definition, insert: “The class is nonempty only with κ̄ ≥ 1: taking a singleton in c_min and U=∅ shows κ ≥ 1. For p→∞ and k≥1 put r² = log(p/k)/log p. The leading L1 squared bound is 2 log p(1+κ̄r)², whereas the NA budget is log n + 2r² log p + O(1). Thus the required strict inequality is 2(log p/log n) max_{0≤r≤1}[(1+κ̄r)²−r²] < 1. For κ̄≥1 the maximum is κ̄(κ̄+2), attained at r=1.” Handle bounded or subpolynomial p separately using the log log n allowance.

   This confirms the formula, including 1/6, from the actual BB ratio. Keeping that ratio is essential; charging only log n would incorrectly yield 1/8 for κ̄=1.

   Replace “up to the sharp exponent α₀ of the lattice route” and the general “holds iff” language in STATEMENT.md:24–38 with: “under the sufficient strict growth condition (P); Part II proves that the exponent 1/6 is optimal for exact-Gram compound symmetry. Necessity for S5, arbitrary factor-class members, approximate Grams, or random rows is not asserted.” A κ̄ upper bound need not be attained, so (1+κ̄) cannot generally describe the actual supremum. Part II does not establish a matching necessity theorem for those other classes. Replace informal “p ≤ n^{α₀}” summaries by the actual strict limsup condition; no boundary result is presently stated.

5. **Re-prove the Q=[p] sandwich branch under its reduced assumptions; do not cite the complete GROW sandwich theorem verbatim.**

   Replace PLAN item 2 with: “Re-prove GROW L3.3(a) using its block events and the Q=[p], K=p branch. The earlier size ladder and the assumption |Q|=O(log n) are unnecessary in this branch: if a maximizer misses a truth it cannot have size p, so adding that truth is feasible, and TV contradicts maximality. NEG is vacuous. Establish the block events under the energy bound, within-block Gram floor, polynomial p, and |C_b|≤16.”

   The original GROW G1 still contains |Q|≤C_Q log n even when Q=[p]; its disjunction removes only the alternative capacity condition. Thus the published L3 theorem is not literally applicable when p grows polynomially. Its proof does extend as above. In contrast, GROW L1_descent.md is genuinely reusable as written: it explicitly requires only S₀⊆Q and |Q|≤K, not logarithmic size. Here κ̄≥1 implies α₀≤1/6, so (P) gives p=o(n), hence K=p eventually. State this deduction once; it also justifies the full-lattice definition and the cap check. There is no missing requirement K≥2p+32s₀+1 in this branch.

6. **Replace the undefined random-design “margin event” with an actual hypothesis.**

   Replace STATEMENT.md:88–91 by: “For each n specify a deterministic family B_n of subsets of [p] of size at most 16 and a measurable design event E_n with P(E_n)→1 such that every realized method block belongs to B_n on E_n. Assume inf_n min_{j∈S₀,C∈B_n:j∈C,U⊆C\{j}} (Σ_{jμ|U})²/Σ_{jj|U} ≥ τ₀ > 0. One may take B_n to contain every set of size at most 16, in which case no partition-margin event is needed.” Require nonvacuous coverage of the realized blocks, rather than allowing an unspecified event to select an artificially favorable family.

   In PLAN item 5 add: “Intersect E_n with the entrywise concentration event. Uniformly over all relevant bounded-size U, fixed-support bounded θ* and the population Gram floor transfer population partial signals to sample partial signals, giving δ²_{U,j} ≥ c n and a common deterministic TV envelope. Verify H0 on these same events and apply the every-deterministic-sequence/common-envelope argument.” The displayed p^{3/2} concentration calculation is sufficient under (P); the growing operator norm of Σ is not a counterexample to that entrywise argument. Conditional convergence alone is insufficient, as FINAL s3 explicitly warns.

7. **Finish the instance hypotheses before claiming them locked.**

   Replace (I)(a)'s “under an explicit genericity condition” by the condition itself: “For every j∈S₀ and U⊆[p]\{j}, |U|≤15, require θ_j + a(Θ−Σ_{i∈U}θ_i)/(1−a+a|U|) ≠ 0, where Θ=Σ_{i∈S₀}θ_i and null coefficients are zero.” With fixed s₀ and fixed coefficients, there are only finitely many distinct expressions as p varies, so this implies a uniform positive population partial-signal minimum. In (I)(b) explicitly retain this condition, fixed a, fixed nonzero coefficients, and independent noise; “same exponent” alone is insufficient.

   In (I)(c) identify the actual truth indices/group occupancies, coefficient vectors and fixed positive scale, or give exact file/section pointers defining them and their asymptotic extensions. In PLAN item 7 replace “all block configurations (unions of ≤3 groups)” by “all configurations in B_n; justify that the actual complete-linkage cut and next-fit packing yield the claimed family on E_n, or certify all blocks of size ≤16.” The three-group restriction needs proof; bounded block size alone permits intersection with up to sixteen groups. Do not transfer the existing p=100 diagnostic certificate to the fourteen-truth layouts without checking them.

   The κ=1 block-CS example itself survives scrutiny. Writing d=1−ρ_w, b=ρ_w−ρ_b, and u=|U| gives λ̃=√ρ_b d/(d+ub), ψ_{l|U}=d[d+(u+1)b]/(d+ub), and c_min=ρ_b/(1−ρ_b). The squared ratio is d(d+b)/[(d+ub)(d+(u+1)b)]≤1, with equality at u=0. This establishes the advertised sufficient exponent for fixed admissible correlations and bounded group sizes; it does not prove S5 necessity.

8. **Specify the SHARP witness and separate its proof from the subcritical expansion.**

   Replace PLAN item 8 with: “Under exact-Gram CS, take m=⌈log p⌉, T=S₀ plus the m null coordinates with largest idiosyncratic ζ, and l the null coordinate with smallest ζ. Then |T|<K eventually, s_T→∞, and Gaussian order statistics give |Z_{T,l}|=(2+o_P(1))√(2 log p). The BB budget is log n+2 log p+o(log p). Establish a lower score comparison for this witness, uniformly under p≤K, giving an improving add when liminf log p/log n>1/6.”

   This is a meaningful, plausible necessity statement for full-lattice NA: the witness may depend on noise because NA quantifies over every subset. It is not a method inconsistency result. Do not reuse the p=o(n) expansion from Part I without adjustment: Part II permits p comparable to n. The selected witness has only O(log p) variables, which supplies an alternative small-model score argument. Fixed s₀, fixed nonzero θ*, fixed σ² and the exact-Gram sampling model must be explicitly retained. No conclusion at equality 1/6 follows.

9. **Keep delivery's inherited premises and statuses explicit.**

   Add to (D): “This extension is relative to Proposition F's abstract unit-cost/unbounded-word machine, MACH, CONFIG, fixed declared R′ and workers, exact e4/TDP-IMPL, complete fallback-grid freezing, raw-dimension allocation including A4, and the inherited P1/S.3 code-audit qualifications. Retained p equals p_raw almost surely for these design classes.” This is substantially stronger operational structure than the ‘some maximizer’ premise sufficient for (L4), so do not conflate the two lists.

   PLAN item 6 correctly uses K_n, the event that deterministic LS0 scores S₀. Retain that argument: D_n→0 alone does not imply P(K_nᶜ)→0, because OP gives the inequality in the other direction. The A2 template is otherwise correctly scoped: nonconstant columns and a null centered-response failure event extend, ridge positivity is design-independent, and the larger-cap resource envelopes already cover this lattice. CAL need not be assumed. Keep the exact no-output assertion as an inherited Proposition F conclusion, with asymptotic consistency as the new statistical assertion.

10. **Remove unsupported diagnostic and frontier generalizations.**

    STATEMENT.md:26 attributes lattice NA violations at p=400,n=10⁷ to D2, but D2_summary.md and D2_CS3_summary.md report “lattice NA fail (sets) = 0/0” throughout the relevant rows. Replace that citation by the actual saved script/output exhibiting tested violating sets, or remove the numerical violation claim. Likewise, replace Part III's “pure deletion paths ... in all tested runs” by a scoped statement naming the relevant rows: D2 contains swaps and path-NA failures, including CS3 p=400,n=10⁴ and S5 p=200,n=10⁴. Successful MR1 discovery is supported there; universal pure deletion is not.

    Replace Part III(iii)'s categorical assertion for “k≥2 global factors with continuous loadings” by: “The present scalar residual-factor proof does not cover multiple global factors. Any claimed faster lattice supremum requires a specified loading array and a proved lower bound; otherwise it remains a conjectured obstruction.” Continuity alone is no quantitative nondegeneracy condition; two-factor arrays can approach a one-factor array arbitrarily fast. Also qualify the general diagnosis that every null is block-visible: nonzero marginal factor signal can cancel after conditioning within a block. These claims are not needed for FAC-L and should not become unproved conclusions inside an ‘evidence only’ paragraph.

Optional suggestions:

- Define the factor class using a chosen admissible representation (λ,Ψ,G), or define κ by an infimum over such representations. As written κ(Σ) is representation-dependent; the same Σ can admit different factor/local decompositions. The existential class interpretation is adequate once stated explicitly.
- Add adversarial L1 tests with shrinking c_min, heterogeneous/sign-changing loadings, negative within-group correlations compatible with Ψ≻0, and approximate Grams. CS/S5 alone do not stress the class-wide hypotheses. Include bounded p and slowly growing p to exercise the log log n term.
- The narrowing to one global factor and the strict subcritical exponent is honestly flagged. Preserve that flag in REPORT.md and distinguish optimality for CS from a universal optimality claim. I found no reason to reject this narrowed research target; the conditions and proof repairs above must be incorporated before locking it.
