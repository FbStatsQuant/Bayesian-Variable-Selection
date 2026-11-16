L7 line check — lemmas/NEC.md sha256 54340e87b89336a1

Independent cross-family review of the permitted packet. No other review, attempt, log, checkpoint, dependency file, or source was consulted. The numerical calculation below ran inline and created no temporary file. No agents or state-changing git commands were used.

The Proposition, Corollary, and current manuscript are VERIFIED. The initial review of v0.1 (sha256 c88d10a4555cf0d7) found the three presentation issues recorded below. During final verification the source changed to v0.2 (the hash in the first line), applying all three repairs. I reread the revised permitted proof file and checked those amendments. There are no outstanding findings. The mathematical proof, constants, and probability guarantee did not change.

## Findings and amendment recheck

The following findings concern the initial v0.1 snapshot. All are **RESOLVED** in the current v0.2 snapshot; severity records the original issue.

**L7-01 — MINOR — §0, originally lines 20–21 — RESOLVED.** The original sentence gave Lemma X′ and display (1.2) the common radius `Cσ*²tℓ_n`. That is Lemma X′'s squared in-sample radius, whereas (1.2) has Hellinger radius `C√(tℓ_n/n)`. These are different distances and units. **Minimal repair:** distinguish the two distances and state why the fixed-design in-sample lower bound supplies no random-design Hellinger counterexample. **Recheck:** current lines 21–23 make exactly that distinction and are correct.

**L7-02 — NIT — §3, originally line 98 — RESOLVED.** The original equality replaced `2/√(πβ)` by the downward-rounded `0.0705`; its value is `0.07052369794346953…`, so the equality and any upper bound using that rounded coefficient were false. The subsequent eventual `0.08p` bound was unaffected. **Minimal repair:** retain the exact coefficient or use `0.0706` as an upper bound. **Recheck:** current line 100 retains the exact coefficient and then uses the valid upper bound `0.0706`.

**L7-03 — MINOR — §8(d), originally lines 178–180 — RESOLVED.** The original numerical remark called an enumeration through size four an “exact posterior” calculation although Ω contains every subset. Normalizing only through size four gives the conditional posterior given `|S|≤4`, and overestimates each corresponding full-posterior model-family mass. No omitted-mass bound was supplied. **Minimal repair:** identify the calculation as restricted, or document full normalization or a sufficient omitted-mass bound. **Recheck:** current lines 180–182 explicitly describe the restricted posterior, conditional normalization, and unsummed larger models. The reported numerical event checks are understood with that same stated restriction; they do not independently certify the full-posterior event. This numerical remark is evidence only and is not used in the proof. The cited review was outside the permitted packet and was not read.

## Line checks

### §0 — statements and four limitations

The design is a single sequence `X^(n)` independent of k. For each fixed k, all subsequent lower thresholds can be included in `n₄(k)`. There is no interchange requiring uniformity over growing k. The positive constant in (5.1) depends only on k and the fixed numerical choices. Scaling from unit noise restores `σ*²` in the distance threshold and leaves model probabilities unchanged.

The null truth satisfies both interfaces for every nonnegative M and M′, and is allowed in the fixed-design formulation for every sparsity bound `s₀^r ≥ 0`. The dimension bound holds for every A ≥ 1 eventually.

Limitation (1) is substantively correct: the design fails (ND), so it is outside Lemma X's hypotheses. The phrase about the remainder of (1.1) must be read at the level of its design-failure event: this design belongs to that event. A numerical value for the unconditional random-design probability in (1.1) would additionally require a law of the design; if (ND) failed almost surely under such a law, that remainder would equal one. No such law is constructed here. Limitation (2), amended in response to L7-01, now states both radii correctly, and its non-contradiction conclusion is correct. Limitations (3) and (4) correctly distinguish the fixed-design in-sample exponential claim from a random-design Hellinger claim and from convergence in probability.

### §1 — design

For all sufficiently large n, `p = floor(√n)+1 ≤ N` and also `p ≤ floor(n/2)`, so the orthonormal vectors exist and the inherited cap is exactly K = p. The contrast isometry U makes every column centered and preserves its squared norm N.

The definition gives `Nτ² = βL/(n−βL)`, so `τ² ~ βL/n²` and τ² is eventually in (0,1). Strictly, positivity of `1−τ²` requires `d < n`, stronger than `d < n+1`; this also holds eventually and therefore creates no gap in the stated large-n result. At n = 400 the stated construction indeed fails. The design does not depend on the noise realization.

Direct substitution verifies `f(Nτ²)=d`, `1−h=1/d`, `1/h=1+1/n+1/(nNτ²)`, and `f(N)=n`. The last lower bound follows from `n/(n+1) ≥ 3/4` for n ≥ 3. The scale argument follows both for model weights, since b and every Q scale quadratically, and for the conditional posterior by `(θ,v) ↦ (σ*θ,σ*²v)`.

### §2 — spectra, determinants, and plug-in calculation

For unanchored k-subsets, the Gram matrix is `N(a²11ᵀ+τ²I)`; its large eigenvalue is `N(ka²+τ²) ≥ N` and its other k−1 eigenvalues equal `Nτ²`. This proves case (a), including k = 1.

For anchored subsets, the k−1 contrast eigenvalues again equal `Nτ²`. The displayed two-dimensional block has determinant `N²τ²`, trace `N(1+k−(k−1)τ²)`, and largest eigenvalue at least N by its first coordinate Rayleigh quotient. Thus `0 < λ₋ ≤ Nτ²`, giving exactly the two determinant bounds in case (b). Case (c) follows from `f(N)=n`.

For an anchored model of size r, the lower determinant bound is `n d^(r−2)`; this yields (2.1) directly. The unanchored bound is stronger by one factor d. The singleton anchor also satisfies (2.1). The range of M is contained in the model column space and `0 ⪯ M ⪯ P` by the locked spectral lemma. The ambient span inclusion consequently proves both parts of (2.2).

The trial coefficients cancel the u₀ component exactly. The fitted vector is `h Σ_J z_j u_j`. Its residual and coefficient penalties give precisely the displayed expansion, including the separate term

`φ₀²/n = a²h²(Σ_J z_j)²/(nNτ²)`.

Since `1/n+1/(nNτ²)=1/h−1`, the bracket recomputes to

`(1−h)²+h²(1/h−1) = (1−h)²+h(1−h) = 1−h`.

Finally `kL/d ≤ k/β`, `a²h² ≤ 1`, `(Σ_J z_j)² ≤ k²L`, and `nNτ² ≥ 3βL/4`. These give exactly (2.3) with the stated c_k. No anchor penalty is missing.

### §3 — good event

The Gaussian density cancellation gives `m₁=√L/√(2π)` and `E a_j² ≤ m₁√p′`. Independence gives `Var(A) ≤ p′m₁√p′`, hence the stated failure bound for 𝓔₄.

The other entries check as follows: the standard-normal two-sided tail at two is approximately 0.0455003; `Var(‖e‖²)=2N`; `Var(Σ_{j=1}^{p′}z_j²)=2p′`; and the normal Mills bound plus a union bound gives `P(𝒯ᶜ) ≤ 1/√(πL)`. No independence between the listed events is needed.

The truncation is essential and is used correctly: 𝓔₃ need not itself have failure probability at most 0.16, but

`P(𝒯ᶜ ∪ 𝓔₃ᶜ) ≤ P(𝒯ᶜ)+P(Ã′>p/2)`.

The amended mean calculation for Ã′ is correct, including its exact coefficient and numerical upper bound. Because `εL→0`, it is eventually at most `0.08p`; Markov then yields 0.16. All other displayed failure terms vanish except 0.046 and 0.125. Their sum with 0.16 is 0.331, leaving positive slack to the required failure bound 0.4. Thus `P(𝓔) ≥ 0.6` for all sufficiently large n.

For (i), (2.2) gives `Q_S ≥ n−7√n` uniformly over all models. Writing `x=√n`, the asserted comparison of `ν/Q_S` with `(1+8/√n)/2` follows, for example, once `x ≥ 56.02`. For (ii), the identity for B is exact, its upper bound follows from 𝓔₁, and `1/(1+u) ≥ 1−u` gives the last inequality.

### §4 — Step A

The ratio identity uses `D_∅=1` and the exact prior weights. Applying `log(1+x) ≤ x`, consequence (i), and (2.2) yields the likelihood upper bound. The global z₀ exponential is a permissible upper bound for both anchored and unanchored models; `ã₀=d^(−1/2)` supplies only its determinant contribution, so there is no missing or double-counted necessary z₀ factor.

The ordered-tuple expansion proves the elementary symmetric upper bound. The prior identity is exact:

`[w(r)/w(0)]/r! = 1/[(2p−1)(2p−2)…(2p−r)] ≤ p^(−r)` for r ≤ p.

On 𝓔₃ the geometric series from r = 1 is at most one. On 𝓔₀ the remaining exponential is at most e³ eventually. Consequently the nonempty-to-empty odds are bounded by `e³d/√n→0`, proving the claimed lower bound on π(∅).

### §5 — Step B

Here `x=(Q_∅−Q_S)/B` lies in [0,1), since b > 0 almost surely and Q_S ≥ 0. The likelihood inequality follows from `−log(1−x) ≥ x`. More explicitly, consequence (ii) gives the exponent at least

`(Q_∅−Q_S)/2 − 5(Q_∅−Q_S)/(2√n)`.

Use (2.3) on the first term and `Q_∅−Q_S ≤ 4+kL` on the subtracted term. This proves the displayed likelihood lower bound, since k is fixed and `(4+kL)/√n→0`. The determinant and prior lower bounds have the correct directions.

For k ≥ 2, fixing any colliding pair in the tuple expansion contributes at most `(Σ_j a_j²)A^(k−2) ≤ (max a_j)A^(k−1)`. A union bound over the `binom(k,2)` pairs proves the displayed symmetric-polynomial bound. For k = 1 the conclusion is immediate. On 𝓔₄ the relative collision bound is at most `k²/(√p′m₁)→0`; in particular, the model family has enough distinct indices eventually.

For L ≥ 1, `m₁/√d ≥ 1/√(2π(β+1))`. Substitution into the displayed model-family odds bound gives

`[(k+1)e^(−c_k/2−1)/(4p√(n+1))] [(p′/p)(m₁/√d)/4]^k`,

which implies the next displayed bound with exactly the stated c₃. Finally `p√(n+1) ≤ 2n` eventually and `π(∅) ≥ 1/2` give (5.1) with the stated denominator 16. The factors of two are correct.

### §6 — Step C and Proposition

The conditional mean and covariance follow directly from the locked slab integral: multiplying `N(nH_S^(−1)X_{c,S}ᵀe, nvH_S^(−1))` by X gives `N(M_Se,vM_S)`. U preserves the fitted norm. For every v, symmetry implies `P(mᵀω ≥ 0) ≥ 1/2`, and on that event `‖m+ω‖² ≥ ‖m‖²`. Mixing over v preserves the lower bound.

Cauchy–Schwarz gives the first distance bound once `W_J−c_k ≥ 0`, which holds eventually for fixed k. With `r=z₀²`, the next algebraic inequality is justified exactly by

`(W−c)²/(W+r) − (W−2c−r) = (c+r)²/(W+r) ≥ 0`.

On the selected family, `W_J ≥ kL/4` and r ≤ 4. For each fixed k, increasing n makes `kL/4−2c_k−4 ≥ kL/8`. Also `L ≥ (log n)/3` eventually. Thus every selected model has conditional far mass at least 1/2 at the stated radius. Multiplying by (5.1) proves the Proposition on 𝓔, whose probability is at least 0.6. One may take n₄(k) to exceed every preceding threshold and ensure `k+1≤p`. All required quantifiers are satisfied.

### §7 — Corollary and failure of (ND)

For any proposed finite positive constants, T is fixed and `t=T log n` is eventually in the allowed range because `κ₀<1`. The chosen integer k is fixed, is strictly larger than 24CT, and therefore changes the Proposition's weak distance inequality into the Corollary's strict one. For sufficiently large n,

`c₄(k)/(2n) > n^(−2) ≥ n^(−cT) = e^(−ct)`.

The outer event thus has probability at least 0.6, contradicting either `2e^(−ct)` or any proposed outer bound tending to zero along this t sequence. Arbitrary dependence of the constants on the listed fixed parameters does not evade this argument. If nonpositive C were allowed literally, impossibility would already follow from the case of any larger positive C; the usual positive-constant convention suffices for the displayed choice of k.

The (ND) assertion must concern its average, not a single pair. Here the averaging checks explicitly. Since `S₀=∅` and `D_∅=1`, the average at j = 2 is at least

`[binom(p′,2)/binom(p′+1,2)] / √((n+1)d) = [(p′−1)/(p′+1)] / √((n+1)d)`.

Its ratio to the permitted (ND) upper bound `1/[c_D(n+1)]` is

`[(p′−1)/(p′+1)] c_D √((n+1)/d) → ∞`

for every fixed c_D > 0. Thus (ND) fails at j = 2 for large n, including the cutoff range relevant to Lemma X.

### §8 — four remarks

(a) The non-contradiction conclusion is correct. At the minimum t, Lemma X′ has a squared in-sample radius of order log² n. The Proposition covers every fixed k, not k growing with n; its specified constant indeed satisfies `log c₄(k)=−Θ(k²)`. It supplies no contradiction at the larger radius. The separate Hellinger distance in (1.2) is now correctly distinguished by the amendment addressing L7-01.

(b) Nothing proved here establishes necessity of the full additional logarithm. A uniform extension to growing k with improved losses would be a further argument, not a consequence of the present fixed-k Proposition. The stated open question is consistent with the permitted packet; this review makes no claim to establish a literature-wide open status.

(c) The asserted convergence on this design is correct. Here is a completion of the brief parenthetical argument. Replace the z₀ window by `|z₀|≤ω_n`, the 𝓔₁ window by `|‖e‖²−N|≤ω_n√N`, and take, for example, `ω_n=√(log log n)`. Their failure probabilities vanish. Keep 𝓔₂ and 𝒯, whose failure probabilities also vanish. Consequence (i) then holds with some `ε_n=O(ω_n/√n)` satisfying `ε_nL→0`. For the same truncated sum,

`E(Ã′)/p → 2/√(πβ) < 1/2`,

and

`Var(Ã′)/p² = O(e^(2ε_nL)/L^(3/2)) → 0`.

The latter follows by integrating the second truncated moment: `∫_0^√(2L) exp((1/2+ε_n)z²) dz = O(p′e^(2ε_nL)/√L)`. Chebyshev applies to this truncated variable, not to the untruncated sum, whose mean is infinite when ε_n > 0. Step A now holds on events with probability tending to one, with upper bound `n^(−1/2)d exp((1+ε_n)ω_n²/2)→0`. Hence `π(∅)→1` in probability, and the asserted posterior distance mass tends to zero. This stronger consistency on the example is compatible with its polynomially small far mass.

(d) The large-threshold comment is correct. The numerical description now explicitly identifies the conditional-on-size posterior, resolving L7-03. The independent restricted calculation below supports its scale of numerical values but does not authenticate the cited 200-draw experiment. The conditional numerical event checks are not used to prove the full-posterior Proposition.

## Independent numerical check

At n = 6400, with Python's standard-library Gaussian generator seeded by 20261115, I generated the contrast noise coordinates and the independent remaining chi-square contribution. I enumerated all 88,642 models of size at most three, computing exact spectra, Q reductions, and smoother means from the one- and two-dimensional blocks above. No approximate Gram eigenvalues were needed.

- `d = 1122.7988184765136`, `Nτ² = 0.2125343047558336`.
- `Π(S=∅ | y, |S|≤3) = 0.9930214441727634`.
- `n Π(𝒮₁ | y, |S|≤3) = 0.018032102700121188`.
- `n Π(𝒮₂ | y, |S|≤3) = 0.0003970643204170872`.
- Among the checked selected anchored models, the minimum slack in (2.3) was `0.13003067667636303`.
- Among those models, the minimum slack in the claimed mean-distance threshold `‖M_Se‖² ≥ (k/24)log n` was `0.8643830589858326`.

These are explicitly conditional-on-size numerical posterior values, not estimates of an uncomputed full normalizing constant. The analytic proof, rather than this experiment, verifies the full-posterior claim.

## Verdicts

| Item | Verdict |
|---|---|
| §0 | VERIFIED |
| §1 | VERIFIED |
| §2 | VERIFIED |
| §3 | VERIFIED |
| §4 | VERIFIED |
| §5 | VERIFIED |
| §6 | VERIFIED |
| §7 | VERIFIED |
| §8 | VERIFIED |
| Proposition NEC | VERIFIED |
| Corollary NEC | VERIFIED |

Overall verdict: VERIFIED.
