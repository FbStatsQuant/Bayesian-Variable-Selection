# R03 — Adversarial check of L4 / (C2-R)

**Verdict: VERIFIED-WITH-AMENDMENTS.** No fatal issue or unresolved major issue found in (C2-R). Three minor amendments are required below. The conditional path, the stated δ/8 margins, the linear-in-n loss for truth-removing moves, and the cap conclusion survive these amendments without changing the locked claim or the definition of CC.

Reviewer: Codex Sol; 2026-11-09. Read STATEMENT v2, L1, L3, all of L4, SoP `02_method.tex` (model space and local-search rules), FINAL `s7_impl.tex` (especially (L3)), and FAC-B's checked L4 template. Only this report was written by this reviewer.

Input-version note: L1 and L3 changed during this review to incorporate R02. The final input check uses L1 SHA256 `3d0f4828f3b05c4c6f471acf7e8113c61622684d47c5bbe130184fe58a3be2de` and L3 SHA256 `2a1debbb80120d6c5aa392746bd6b27678c80f94b978f9632ad9cbc213114ecb`. L4 reviewed here has SHA256 `85621c41cbfebde46e865189dc74fe22929315d0be2a3426ff8a9310f345e336`. Locations below refer to these versions.

## Numbered findings

1. **MINOR — Two threshold assertions are false for allowed sequences, although the δ log n slack repairs both.** Location: L4.1 lines 25–27 and L4.3 lines 38, 41.

   First, a feasible addition to a size-k path centre has

   `2Δ(T∪l,l) − Λ_k = log(1+1/n) + 2 log(1−1/(2p−k)) + o(1)`.

   The second term is not o(1) uniformly under the hypotheses: bounded p is allowed. For p=5, k=1 its limit is `2 log(8/9) = −0.235566...`. Thus the claimed `2Δ ≥ Λ_k − o(1)` is literally false. The determinant error tending to zero does not make this separate prior-ratio error tend to zero.

   Second, `Λ_k ≥ log n` fails at the full model: `Λ_p = log n − 2 log(1+1/p)`. For p=5 the deficit is `0.364643...`. The full model is a permitted starting centre when N₀ is empty. No addition or swap is feasible there, but a null deletion can be feasible, so this case must be included in (a).

   **Fix:** Let `b_n = 2p/((n−1)d) = o(1)`. Use, uniformly,

   - null deletion from T: `2Δ ≥ Λ_k − b_n`;
   - feasible addition to T, hence k≤p−1: `2Δ ≥ Λ_k − 2/p − b_n`;
   - addition after a null deletion from T: `2Δ ≥ Λ_k − b_n`;
   - `log n − 2/p ≤ Λ_k ≤ log n + 2 log(2p)`.

   Keep the determinant remainder in the last display of L4.1 as well. These bounds follow directly from the displayed logarithm inequality and L1.4.1. After L4.2.1 they give deletion gain at least `(δ/4)Λ_k − o(1)` and addition gain at most `−(δ/4)Λ_k + O(1) + o(1)`. Both imply the advertised δ/8 bounds for sufficiently large n, including fixed p. No extra assumption p→∞ is needed.

2. **MINOR — Make the null-only quantifier explicit before applying CC.** Location: L4.2 lines 30–33; L4.3 lines 42–44.

   The phrase “for retained j ≠ l” in line 31 should read “for retained null j ∈ T∖S₀.” The Gaussian bound involving `e_{T∖j}` itself holds even when j is a truth, but the subsequent assertion that *all these* statistics satisfy `τ² ≤ (1−δ)Λ_k` does not follow from CC for truth j. CC contains only null one-deletion sets. Also, the null signal-leakage approximation cannot be applied to an addition based at T∖j when that set is missing a truth.

   **Fix:** Restrict this sentence and the collection used in L4.2.1 to null j. Keep truth-out swaps entirely in L4.4. The actual proof of (b) already does this, so no enlargement of CC is required. With the updated L3 input, change the multiplier citation in line 32 from L3 “(c1)” to “(c1′).”

3. **MINOR — The explanatory satisfiability restriction uses an upper exponent as though it were the actual exponent, and unnecessarily excludes the boundary.** Location: L4 lines 10–11; the same parenthetical occurs in locked STATEMENT lines 100–102.

   From `log p/log n ≤ α` one cannot deduce the displayed necessary upper bound on |e| with `√(2α)`: H_q can be much smaller than that upper envelope. For example, fixed p, α=.49, δ=.2 and e=0 satisfy CC eventually, whereas the displayed right-hand side is negative. The assertion “only when α < (1−δ)/2” therefore is not a necessary condition under the stated meaning of α.

   Even if `log p/log n → a` is the actual exponent, strict inequality is not necessary for bare satisfiability. At `a=(1−δ)/2`, take `p≈n^a/(log n)^C`, C>1, and e_R=0: `H_q²=(1−δ)log n−2(C−1)log log n+O(1)`, leaving room at bulk centres despite the limiting exponent being exactly the boundary.

   **Fix:** State the exact requirement `κ₀|e_R| ≤ √((1−δ)Λ_k)−H_q`. If explaining exponents, say that at k≍p and actual exponent a, a positive leading-order allowance for e requires `a<(1−δ)/2`; only `a≤(1−δ)/2` is necessary at leading order. This does not restrict the conditional implication (C2-R). Flag the corresponding prose in the locked statement for its owner's disposition; no locked file was edited here.

## Input approximation: independently broken, then rechecked after the concurrent repair

The original L1 single-term ε estimate was false. This was independently reproduced during this review before observing R02's concurrent repair. With R consisting of one truth of coefficient 1, a null in the same group, ρ_w=.7, σ=1, and g=0, write a=n²−1. Exactly,

`σ_l = .7/(a+1)`,

`ṽ_l = 1+1/a−.7²/(1+1/a)`,

`ε_l = √(n−1) .7 / ((a+1)√ṽ_l) ∼ (.7/√.51)n^(−3/2)`.

Thus no fixed constant can bound it by `C k/n²` at fixed k. Numerically, `n^(3/2) ε` was .979704, .980147, .980196, .980196 at n=10³, 10⁴, 10⁶, 10⁸. This is also a pointwise counterexample inside E_n∩CC eventually: use all latent normals zero, fixed p, and r=n−1−p. It does not break the path claim.

The revised L1 lines 80–84 now give the correct exact decomposition and bound

`|ε| ≤ C[(1+|τ|+max|g|)k/n² + √k/n^(3/2)]`,

using k+1 for an addition. Revised L3(c4) correctly implies `sup |ε| ≤ n^(−1/2)`. I checked the missing signal factor and both noise/variance terms directly. This input defect is **resolved in the reviewed final inputs**, not an outstanding major finding against L4.

## Coverage and uniformity audit

| L4 component / attempted break | Result |
| --- | --- |
| Feasibility at k=p | Eventually K=p under (P_α). At the full model there are no outside variables, so additions and swaps are empty collections. Deletions are feasible. Item 1 repairs the only false numerical inequality used here. |
| Null deletion j | Its statistic uses R=T∖j, with j null. Exactly this set is present in CC, with the threshold indexed by the original size k. |
| Addition l, including l∈N₀ | Every outside variable is null because T⊇S₀. E_A ranges over all null labels and all within-group mate sets, including initially omitted N₀. Its centre error is e_T, present in CC. No special treatment of N₀ is needed. |
| Null-out swap j→l | Exact telescoping gives deletion at T plus addition at T∖j. Both bases contain S₀. The latter addition uses e_{T∖j}, included in CC with Λ_k, and its larger model has size k. Its threshold is the deletion threshold at size k, not the direct-addition threshold at size k+1. |
| Swap with a truth coming in | Impossible at a path centre: all truths are already retained, and a feasible incoming index must lie outside T. |
| Truth deletion / truth-out swap | Covered together by L4.4, without invoking CC at T∖j or T∖j∪l and without applying the null approximation there. |
| Ridge, determinant and multiplier uniformity | Revised ε is uniform over all truth-containing bases. L1.4.1 gives error O(p/n) uniformly for every relevant determinant increment, including the larger set of a feasible addition. L3(c1′) gives M=½(1+η), |η|≤η_n, on the entire truth-containing lattice, including all null one-deletion bases. Hence data-dependent path selection requires no further union bound. |
| Nonlinear logarithms | Set x=M(τ+ε)². CC gives x=O(log n) uniformly, since Λ_k=O(log n). The absolute correction is O(x²/ν)=O((log n)²/n)=o(1), not merely a relative o(1). This justifies the additive o(1) in L4.3 once the threshold terms in item 1 are retained. |
| Exact deletion order and ties | Π is defined through the exact ridge score, not the noise proxy. All competing move types lose strictly; ties among null deletions use the same lexicographic ordering of resulting sets. No probability-one no-tie event or monotonicity in τ is required. |
| Terminal and zero-length path | CC explicitly includes T=S₀. At that centre only additions and truth-removing moves remain, all strictly negative. The same argument covers m₀=0. |

### L4.4: separate truth-move check

The bias argument is valid for both neighbour types. T′ retains every truth except j. Minimizing the quadratic form for the residual of x_j over T′, with coefficient of x_j fixed at 1, and using `λ_min(Σ_{T′∪j})≥d`, gives the stated `(n−1)d` floor. This remains true if the incoming null is a same-group mate or T′ contains nearly all other predictors.

The cross term is exactly the unstandardized Gaussian residual conditional on T′. E3 bounds its within-group A_j(U) for every possible U, while the crude L3(c2) bounds e_{T′} over **all** subsets, not only truth-containing subsets or path subsets. Since s_u≤1 and c_u≤1, the cross term is uniformly O(√(n log n)). The fitted noise energy is at most `σ²gᵀΣ⁻¹g≤σ²(p+n^(2/3))=o(n)`. Consequently the claimed uniform positive linear RSS difference holds.

There is no invalid extension of a truth-containing upper Q bound to T′: only the general lower bound `Q_{T′}≥RSS_{T′}/s²` is used there. The upper bound is used at T⊇S₀. To make the final logarithm comparison exact in the presence of the .02 offset, record the stronger identity `Q_T≤n−1` from its definition; thus `ψ_T≤n−.98<n` and `ψ_{T′}/ψ_T≥1+c₃` follows from `Q_{T′}−Q_T≥c₃n`.

For the determinant comparison across a swap, use both sides of L1's f bound: uniformly `L(U)=|U|log(n+1)+O(p/n)`, even for U missing a truth. Hence equal-size swaps contribute O(p/n), and truth deletions contribute at most log(n+1)+O(p/n). The looser bound in L4.4 is valid. The O(log n) prior/determinant contribution is dominated by `νlog(1+c₃)`, proving the stated fixed c_θ>0 uniformly.

### Caps

The conclusion agrees with the actual scan-before-cap-test rule, FINAL s7 (L3), line 40. At cap a=m₀ the search reaches S₀, completes its extra scan there, finds no improvement, and certifies **before** the cap test could return local_limit. At a=m₀−1 (m₀≥1) its last scan at T_{m₀−1} scores S₀ but does not scan S₀ as a centre. At m₀=0 any nonnegative integer cap certifies immediately. These are statements about this deterministic search endpoint; they do not assert the public flag of a different final HPM. The pathwise prefix reasoning is valid even for a<ℓ_n; it does not misuse CAP's separate cross-method integration assertion. MR1's a_n=ℓ_n+|S*| is certainly at least m₀.

## Local falsification numerics

All computations used `py -3.13`, ran in memory with bytecode writing disabled, and wrote no diagnostic artifacts. They are finite-n checks, not substitutes for the uniform argument above.

- `s1_path.run(..., exhaustive=True)`, equivalent to its `exh` option: (p,n,seed)=(40,10⁸,1), (100,10¹⁰,2), (200,10¹⁰,3). Every pair was scanned; all three searches made only null deletions and ended at S₀. These runs were not asserted to satisfy CC.
- A separate 24-run scan at n=10¹⁴ used S5 covariance, seeds 1–6 with RNG seed `10007*seed+p`, and configurations (p,s₀,|N₀|)=(40,4,0), (40,1,4), (5,1,4), (5,1,0). Four-truth coefficients/positions used `bcs_core.layout`; one-truth cases used θ₀=1.4. N₀, when nonempty, was indices 1–4 in a block containing the single truth. Each path was defined by exact best null deletions. At **every** centre, all deletions, additions and all retained/outside swap pairs were evaluated, with truth-out pairs separately inspected; CC was evaluated on T and every null one-deletion set, including the endpoint.
- 23/24 paths satisfied CC_n(.1); the remaining one was not counted as a CC instance. Across all 24, the smallest nonterminal best-deletion gain was at least .460595 log n; the smallest gap against additions/null-out swaps was at least .380088 log n; every truth-removing gain was at most −.155344 n; every endpoint neighbour gain was at most −.460595 log n. The p=5, |N₀|=4 cases tested m₀=0. These scans did not separately certify every E_n component.

No change to CC, the claimed path Π, the δ/8 margin, or the cap threshold is needed. The remaining amendments concern literal proof/prose statements identified above, not an unproved high-probability assertion about CC or the Tier-2 result.
