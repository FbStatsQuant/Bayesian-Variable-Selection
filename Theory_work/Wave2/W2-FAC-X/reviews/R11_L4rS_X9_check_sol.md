# R11 — Key-lemma check of L4r-S and X9

Reviewer: Codex Sol, acting as the requested cross-family key-lemma checker.
Scope: locked `STATEMENT_T2.md` v2, claim (G2); `T2/L4r_path.md` §§L4r.0–L4r.3 and `lemmas/X9_iid_general.md`, with the specified inputs. No proof or statement file was edited. L4r.4–L4r.6 are not certified by this review.

## Verdicts

| File / checked scope | Verdict |
|---|---|
| `T2/L4r_path.md`, §§L4r.0–L4r.3 | **VERIFIED** |
| `lemmas/X9_iid_general.md`, §§X9.1–X9.3 | **VERIFIED-WITH-AMENDMENTS** — issues 1–2 below, both MINOR |
| `T2/STATEMENT_T2.md`, §§1–3, as the exact-Gram setting/reference input | **VERIFIED-WITH-AMENDMENTS** — issue 3 below, MINOR and unused by the proof |
| `lemmas/X1_representation.md`, X1.1–X1.4, as reused by X9 | **VERIFIED** in this use, with constants depending on the loading endpoints |
| `lemmas/X2_perturbation.md`, D1–D4 and proof steps (i)–(iii), (v), as reused by X9 | **VERIFIED** in this use, with the normalisation adjustment detailed below |
| `lemmas/X4_path.md`, §X4.6 | **VERIFIED** in the general-loading use |
| FAC-B `lemmas/L1_cs_reduction.md`, `L3_event.md`, `L4_path.md`, and `STATEMENT.md` §1 | **VERIFIED** for the identified reused identities, event arguments, score/move rule and prefix property; not a fresh audit of their other claims |

**FATAL: none. MAJOR: none.** I find no counterexample to (G2) in its locked exponent range and no missing path invariant needed by these proofs. The two X9 corrections below preserve the stated perturbation rate and both logarithmic margins. The incorrect limit in the auxiliary exact-Gram setting must not be used to simplify the centre, but L4r itself uses the correct centre throughout.

## Numbered issues

### 1. MINOR — X9.2 drops the logarithmic part of the second-order bound

**Location:** `lemmas/X9_iid_general.md:39`, “Second order ≤ r_n²‖c‖ ≤ C(p^{3/2}/n)H̄”.

**Reason:** D1 defines `r_n = 3√(p/N) + 3√(2 log n/N)`. Consequently the justified bound is

\[
 C\left(\frac{p^{3/2}}n+\frac{\sqrt p\log n}n\right)\bar H.
\]

The second term cannot be absorbed into `Cp^{3/2}H̄/n` when, for example, p is fixed; bounded p is allowed. This is a false intermediate rate comparison, not a failure of the final lemma.

**Fix:** retain both terms, as X2 step (ii) actually does. For `p ≤ √n`,

\[
 \frac{p^{3/2}}n\le\frac p{\sqrt n},\qquad
 \frac{\sqrt p\log n}n\le\sqrt{\frac{p\log n}n}
\]

eventually. Thus the displayed `δ̄_n` still dominates the complete remainder. Alternatively use the one-step resolvent bound below, which avoids a separate second-order calculation.

### 2. MINOR — X9.3(ii) should take the absolute value before squaring

**Location:** `lemmas/X9_iid_general.md:57`, the addition upper bound involving `(s_l(T ∪ l) + δ̄_n)²`.

**Reason:** the reference statistic s is signed. From `|δ| ≤ δ̄_n` it does not follow that `(s + δ)² ≤ (s + δ̄_n)²`. For `s = -1` and `δ = -δ̄_n < 0`, the proposed square has the wrong ordering. The unspecified `o(1)` could absorb this discrepancy, but that must be justified rather than treated as the square's monotonicity.

**Fix:** replace that expression by `(|s_l(T ∪ l)| + δ̄_n)²`, or by `s_l(T ∪ l)² + 2C H̄ δ̄_n + δ̄_n²`. The error is `o(1)` uniformly because `|s| ≤ C H̄` and `δ̄_n H̄ → 0`. The subsequent reduction to `τ_l² + o(1)` and the addition exponent are unchanged.

### 3. MINOR — auxiliary exact-Gram setting states a false limiting offset/centre

**Location:** `T2/STATEMENT_T2.md` §2, final parenthetical: “ϱ → η, X_T → (ℓᵀξ_K − η)/(1 + ‖ℓ_T‖²)”.

**Reason:** its own exact definition gives

\[
 \varrho=\eta-\sum_{i\in S_0}\ell_i\xi_i+o_P(1),
\]

not `η + o_P(1)`. For one truth with fixed loading λ = 0.6, `ℓ = 0.75`, the difference `ϱ − η` converges in distribution to `−0.75 ξ_truth`; it does not tend to zero in probability. The numerator of the corresponding limiting centre contains the truth noise terms as well. Bounded p is a direct counterexample to the parenthetical.

**Fix:** write `ϱ = η − Σ_{S₀}ℓ_iξ_i + o_P(1)` and replace the limiting centre's numerator by `Σ_{i∈T}ℓ_iξ_i − η`, or delete the parenthetical. L4r.0(e), L4r.1(s3), and L4r.2 all retain the correct exact ϱ, so this does not invalidate L4r-S. X9 independently retains the truth-noise terms as well.

## Exact-Gram audit

### L4r.0: ridge, drift, determinant and gains

The scaling is correct: `H_U = (n² − 1)Σ_UU + I` and

\[
 H_U=\Delta(I+\ell'_U\ell_U'^T)\Delta,\quad
 \widetilde z_i=\kappa_1(\ell'_i\varrho_0+\check\zeta_i),\quad
 \kappa_1^2=\frac{\sigma^2}{s^2(n+1)}.
\]

Applying the principal-submatrix Schur identity gives precisely the factor `D'_U/(D'_U − ℓ_j'²)` in deletion. The two centre drifts follow by subtracting the single numerator term and denominator term; addition then has `D'_U/(D'_U + ℓ_l'²)`. No unregularised/ridge substitution occurs here. The cancellation of truth signal in (e) leaves exactly the ϱ stated before issue 3, including its truth-noise term.

The determinant calculation also tracks: `(n + 1)d_j''² = d_j² + n` and

\[
 \ell_j'^2-\ell_j''^2
 =\frac{\lambda_j^2 n(n-1)}{d_j^2d_j''^2}
 =\ell_j''^2\frac n{d_j^2}.
\]

Both the removed diagonal factor and the difference of the two log rank-one factors are bounded by `δ_n = 1/((n−1)ψ_lo)`. Thus even `|e_j| ≤ 2δ_n` is established; the stated `3δ_n` is safe. For fixed U, equal loadings give identical `e_j`, `γ'_j`, and `ε_j`; dependence on the rest of U does not invalidate the within-loading ordering. The gain formulas have the correct prior ratio, determinant signs and ν factors. Telescoping is an identity of F, not an approximation to a swap statistic.

### L4r.1: event, multiplier and truth moves

E1–E4′ need no compound symmetry: the null ξ's are iid, the relevant normalised signal-noise inner product is standard normal, and `gᵀΣ⁻¹g + r` has the required chi-square law. The E4 dyadic order-statistic proof in FAC-B L3 applies over the entire deterministic null set. Its top-square bound is simultaneous for all m, and hence all subsets of size m. Empty null sets make E3′/E4′ vacuous.

The RSS comparison is valid for arbitrary principal submatrices with `λ_min(Σ_UU) ≥ ψ_lo`, including sets omitting truths. For supersets of truth,

\[
 \Phi(T)\le \sum_{i\in T}(\xi_i+\ell_i\eta)^2=o(n/\log n)
\]

on the stated event, since `p ≤ n^{A₁}`, `A₁ < 1`. This yields the claimed uniform `M_T ≤ ½(1 + 2/log n)` eventually. The bound `ψ_U ≤ n` is valid directly from `quad_U ≥ 0`, namely `ψ_U ≤ n − 0.98`; it need not be inferred solely from the preceding RSS upper comparison.

For a truth-out move, `r_j ∈ span(X_U)` and `‖r_j‖² ≥ (n−1)ψ_lo`, while `|r_jᵀe|/‖r_j‖ ≤ σ√Φ(U) = o(√n)`. The lower bound is squared only eventually, when the signal term exceeds the noise bound. Removing the possible improvement from adding l costs at most `σ²Φ(U) = o(n)`. The two Q/RSS comparisons then give `Q_{T′} − Q_T ≥ c_θ n`; `ψ_T ≤ n` converts this to an order-n loss in log score. Determinant changes in swaps cancel the `log(n+1)` terms. No sparsity or fixed-size restriction on T is used. Dependence of this truth-loss constant and of n₀ on ϑ and σ agrees with the locked statement.

### L4r.2(a): sign argument

The identity `Σ_K ℓ'_i τ_i = κ'_S X_T + ϱ` is exact, with `κ'_S > 0` and strictly positive loading weights. If `X_T ≥ 0`, every τ is at most H̄. Were every τ less than `−(H̄ + |ϱ|/ℓ'_lo)`, their positively weighted sum would be strictly less than `−|ϱ|`, contradicting the identity. Reversing signs treats `X_T < 0`. The strict inequality in the contradiction handles equality/ties; no nondegeneracy event or path assumption is required.

### L4r.2(b): Cauchy–Schwarz centre bound

For an arbitrary kept set K of size m, `Σ_K ξ_i² ≤ m(Z_m² + 2)`. With `Q′ = Σ_K ℓ_i'²`, Cauchy–Schwarz and `D'_T ≥ Q′ ≥ mℓ_lo'²` give

\[
 \frac{|\sum_K\ell'_i\zeta_i|}{D'_T}
 \le \sqrt{\frac{m(Z_m^2+2)}{Q'}}
 \le\frac{\sqrt{Z_m^2+2}}{\ell'_{lo}}.
\]

The residual term is at most `|ϱ|`; for m = 0 use `D'_{S₀} ≥ 1`. This does not require comparable loadings within K or sign balance.

### L4r.3: exponents and assembly

For deletion, cancellation of `log p` against `½H̄²` leaves `½log n − log k − γ_m log(2p) − o(log n)`. If `m ≤ log n`, `log k = O(log log n)` and `γ_m ≤ γ̄(1 + O(n⁻²))`. If `m > log n`, `γ_m = O(1/log n)` and `log k ≤ A₁log n`. These yield the stated deletion margin; no untracked factor of `(1 + γ̄)` remains on the whole `log p` term.

For addition, the v expansion is legitimate because the centre bound first gives `τ_l² = O(log n)`, uniformly, so `v = O(log n/n)`. For `m ≥ 1`, the size penalty contributes `−½Z_m²` up to `O(log log n)`. Therefore the expression to maximise is

\[
 f(Z)=\bar H^2+2R'\bar H Z+(R'^2-1)Z^2.
\]

It is increasing for `Z ≥ 0` because `R′ ≥ 1`. The bound is `Z² ≤ H̄² + 2L_n + 2`, not literally `Z ≤ H̄`; replacing Z by this upper bound changes f by `O(L_n)` for fixed loading endpoints. This gives coefficient `(1 + R)² − 1`, exactly as claimed. The m = 0 computation instead gives `−½log n + o(log n)`. All remainders are uniform; bounded p is included.

Null-out swaps are below the deletion of the same j by the uniform negative addition bound at `T ∖ j`, which still contains S₀. This is why no path-only no-addition premise is needed. Truth-out swaps use TL. At S₀ the remaining neighbours all lose. Induction now works for every start in the full lattice on this single event, regardless of how a start or N₀ was selected. Every maximiser is a null deletion, so ties cause no gap. With K = p, all intermediate moves used in telescoping are feasible. A cap at least `|T₀ ∖ S₀|` reaches S₀ and allows its final certifying scan under the cited prefix property.

One fixed valid margin is half the smaller of `½ − A₁ max(1,γ̄)` and `½ − A₁((1+R)²−1)`, once n₀ is enlarged. This has precisely the parameter dependence allowed in locked (G2).

## Iid-transfer audit

### Representation, reference and the κ₀ change

X1.1's orthogonal rotation acts on the independent Gaussian factor and idiosyncratic vectors before loadings are applied. It therefore preserves its distributions and independence with arbitrary deterministic loadings. Whitening by √ψ and subsequent column standardisation preserve spans and noise partial projection statistics. They do not make the ridge score invariant to scaling; X9 correctly uses the normalised Gram for X1.4's separate ridge-error comparison.

Sherman–Morrison gives the stated X9 reference exactly:

\[
 N(A_T^0)^{-1}\widetilde v_1=\xi_T-\ell_TX_T,
 \quad N((A_T^0)^{-1})_{jj}=d_j^0:=1-\ell_j^2/D_T,
 \quad \varrho=\kappa_0\eta.
\]

It follows that `s_j = (ξ_j − ℓ_jX_T)/√d_j^0`, not the unnormalised residual. The two drift identities and the addition identity for `s_l(T ∪ l)²` follow exactly. The effective null-only offset is `κ₀η − Σ_{S₀}ℓ_iξ_i = O(√L_n)`, independent of T. The sign and Cauchy–Schwarz proofs therefore transfer with this offset, `ε ≡ 1`, and positive base denominator `κ₀ + Σ_{S₀}ℓ_i²`.

D3 gives more than `κ₀ ∈ [½,2]`: `κ₀ = 1 + O(n⁻¹/³)` and `κ₀ ≥ 1 − n⁻¹/³`. This supplies `γ_m ≤ γ̄(1 + O(n⁻¹/³))`, so the exact-Gram deletion exponent survives. Using only `[½,2]` would not justify that sharp γ̄, but X9 explicitly uses the stronger D3 statement.

### Uniform perturbation: no missing band/path hypothesis

Here is a direct closure of the imported normalisation/resolvent argument, also verifying that the change of δ definition from X2 is harmless. Write

\[
 B=I+R+bb^T,\quad B_0=I+bb^T,\quad
 b=b^0+\alpha,\quad b^0=\phi\ell_T/\sqrt N,
 \quad c=B_0^{-1}\widetilde v_1,
 \quad c^0=\xi_T-\ell_TX_T.
\]

For every principal set simultaneously, D1 gives `‖R‖ ≤ r_n`, D3 gives `‖α‖∞ ≤ C√(log n/n)`, and the centre bound gives `‖c⁰‖ ≤ C√p H̄`. X2(i)'s scalar quotient estimates, with `ℓ_lo ≤ ℓ_i ≤ ℓ_hi`, give

\[
 \|c-c^0\|_\infty\le C\sqrt{\log n/n}\,\bar H,
 \qquad \|c\|\le C\sqrt p\bar H.
\]

There is a shorter alternative to expanding to second order:

\[
 B^{-1}\widetilde v_1-c=-B^{-1}Rc,
 \qquad
 \|B^{-1}\widetilde v_1-c\|
 \le\frac{r_n}{1-r_n}\|c\|.
\]

For `d_j = (B⁻¹)_jj`, the resolvent and the explicit diagonal formula for `B₀⁻¹` give

\[
 |d_j-d_j^0|\le C(r_n+\sqrt{\log n/n}),\qquad
 d_j,d_j^0\ge c(\ell_{hi})>0
\]

eventually. For example `d_j^0 ≥ κ₀/(κ₀ + ℓ_hi²)`; the analogous `B₀` bound and small r_n give the other lower bound. Hence

\[
 \left|\frac{(B^{-1}\widetilde v_1)_j}{\sqrt{d_j}}
       -\frac{c_j^0}{\sqrt{d_j^0}}\right|
 \le C\left(r_n\sqrt p+\sqrt{\log n/n}\right)\bar H
 \le C\left(\frac p{\sqrt n}+\sqrt{\frac{p\log n}n}
                 +\sqrt{\frac{\log n}n}\right)\bar H.
\]

The left side is exactly X9's `|δ_j|`. Every bound used a full-matrix operator norm, a coordinate maximum, or a deterministic inequality for an arbitrary subset. There is no union bound over exponentially many T, no use of D5/D6, no conditioning on a selected path, and no independence assumption about a selected T. Thus the final perturbation rate is valid, and its product with H̄ vanishes for `A₁ < ½`.

### X1.4 errors, additions, truth moves and starts

D1–D4 imply `sd_j² ∈ [½,2]`, `λ_min(G^r_U) ≥ ψ_lo N/2`, `λ_min(G_U) ≥ c₀(n−1)` with `c₀ = ψ_lo/5`, and `q_U ≤ CpH̄²/n = o(1)` simultaneously. On the fixed truth support the raw sample covariance tends to its population value, and `eᵀμ/(n−1) = o(1)`, giving uniform positive fixed bounds on s². Thus X1.4's hypotheses hold with endpoint-dependent constants; no additional X5 event beyond these consequences is necessary.

For null j, the normalisation just checked gives `Nω_j² ≤ C H̄²`. Consequently `ε_j^d ≤ C H̄²/n`, the ridge remainder satisfies `|r_j/ψ_T| ≤ Cn⁻⁵/²(1 + H̄²)`, and multiplying the latter by ν costs only `O(n⁻³/²(1 + H̄²)) = o(1)`. Determinant errors are `O(1/n)`. The upper multiplier `½(1+C/n)` follows from the RSS lower comparison and does not require q to be much smaller than its available bound. These errors cannot consume a positive multiple of log n.

After issue 2's correction, the addition proof uses the reference statistic at `T ∪ l` and its exact reduction to the centre at T. It does not incorrectly use a deletion statistic at T for an outside coordinate. The deletion proof uses the sign lemma with the effective offset above. Both import only the audited uniform bounds from L4r.3. Their remainders include `O(n⁻¹/³ log n) = o(log n)` from κ₀. Swaps then telescope exactly at `T ∖ j`.

For truth moves, X4.6 uses raw coefficients β, which are fixed in model (R); no fixed-θ* assumption is smuggled into the iid case. The lower residual norm comes from `λ_min(G^r_U)`, and `‖P_Ue‖ ≤ C√p H̄ = o(√n)` follows from q. RSS loss is therefore order n uniformly over all U. The Q/RSS bound, or X4.6's ridge comparison, makes the corresponding score gain negative of order n. No part of X4's band, gap, spacing or end-phase events is used. The same uniform-over-T induction as the exact case covers every start and the random N₀.

## Numerical checks and limits of evidence

The supplied N_T2 and N2X summaries and the two exact-Gram numerical source files were read as diagnostics only. Their large-exponent paths are not evidence for the uniform claim at those exponents; neither the simulations nor the adversarial examples establish sharpness of A_S. The proof above uses the strict margin `A₁ < A_S` and does not infer it from those numerics.

Independent checks are in `R11_scratch/check.py`; results are recorded in `R11_scratch/check_output.txt`. These checks compare direct matrix identities and enumerate all supersets for small p; they supplement, rather than replace, the uniform algebra above.

* **Algebra stress test:** n = 173, p = 8, distinct loadings spanning [0.1, 0.98], two truths with opposite coefficient signs, all 256 subsets U. Maximum absolute errors: deletion/addition quad increments `3.89 × 10⁻¹⁶`, drift `2.22 × 10⁻¹⁵`, determinant increment `2.13 × 10⁻¹⁴`, reduced versus full centre `2.22 × 10⁻¹⁶`. The determinant error bound and both uniform lemmas (using empirical null maxima/top-square sums) passed. This tests identities outside the asymptotic exponent regime, not a path claim there.
* **Exhaustive uniform scans within the exponent range:** n = 10⁸, p = 10, distinct loadings spanning [0.59, 0.61], one truth, seeds 112–114 for each of exact-Gram and iid models. Here `log p/log n = 0.125 < A_S = 0.15543648`. Direct D0 matrix scores were computed independently of `eg_core.py`. All 512 supersets per data set were checked, including every addition, truth deletion/truth-out swap, and 9,216 null-out swaps: 3,072 superset checks and 55,296 null-out swaps overall. Across the six data sets, the smallest best-null-deletion gain divided by log n was `0.407694`; the largest addition gain divided by log n was `−0.258019`; the largest null-swap-minus-best-deletion difference was `−4.87105`. All truth moves were negative. The iid reference numerator identity agreed to `1.34 × 10⁻¹⁵`; the largest observed null perturbation was `0.001464`.

**Disposition:** accept L4r.0–L4r.3; accept X9 after the two local MINOR corrections. Correct the unused parenthetical in its exact-Gram setting input. No weakening of locked (G2), change to A_S, extra loading-class restriction, or path-dependent hypothesis is needed.
