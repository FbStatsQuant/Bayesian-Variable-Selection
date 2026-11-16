# P7 — same-family pre-check of `work/api_attempts/dist1b/F-b-r2.md` (counterexample: the exponential distance clause fails without (ND))

Checker: Claude Opus 5.5 (Claude Third), effort high. Read-only apart from this file. No git, no agents.
Read: `briefs/PRECHECK_COMMON.md`, `briefs/BRIEF_P7_NEC_precheck.md`, the object file (all of §1–§8), `STATEMENT.md` (v1.4 on
disk; §0, §1, §3 incl. Lemma X, Lemma X′, (1.1), (1.2)), `API_CARDS.md` "Common definitions" and Card F, [P1] `PROOF_v3.tex`
`lem:spec`, `lem:prior`, `lem:num`. Not read: `reviews/` (other than writing this file), `LOG.md`, `CHECKPOINT_*`, `DEPS.*`.
Note: the brief names STATEMENT v1.3.1; the file on disk is v1.4. Lemma X, Lemma X′, (1.1), (1.2) and the §0 interfaces
used here match the Card X / Card F wording, so the version difference has no effect on this check.

Scripts (outside the repo, in the session scratchpad):
`p7_nec.py` (exact model posterior on the design, all models of size ≤ 4 or ≤ 3), `p7_alg.py` (numerical check of the exact
identities and inequalities (2.1)–(2.3) and Step C, plus the elementary-symmetric bound), `p7_events.py` (Monte Carlo of the
good-event components). Raw output: `results.txt` in the same scratchpad.

---

## 0. Bottom line

The Proposition (§6) and the refutation (§7) are **correct**. I checked every line of §1–§7 by hand and recomputed the key
steps; the exact spectra, determinants, the plug-in identity and Step C also pass numerically to rounding error. No error
invalidates the counterexample. The findings below are wording overclaims in the commentary (§7 "Consequences", §8) and one
missing argument in a side remark (the in-probability form "holds trivially" in this design). None of them touches the
Proposition or the refutation of Lemma X without (ND).

**What is established.** Take Lemma X (STATEMENT §3) and delete the hypothesis (ND; c_D, m_n(t)). The resulting statement
is false for every choice of (c, C, C′, M₀, n₀), and for every (s₀^r, A ≥ 1, σ*², M, M′, κ₀). Indeed its distance part alone
fails:

  P_e[Π(‖μ̂ − μ‖² > Cσ*²t | y) > e^{−ct}] ≤ 2e^{−ct}.

It fails already at t = M log n for a fixed large M, on a fixed design with s₀ = 0 and μ = 0, which lies in every
(E; M) ∩ (C; M′) class and has p ≤ n^A. The weaker "(16)-type" form also fails: inner level e^{−ct} = n^{−cM} with an
outer failure probability that only has to tend to 0. The variance clause and the size clause play no role (the size
clause was already known to fail). Not established, and not claimed by the file as proved: anything about the
in-probability form under (E), (C) alone (GAP 2); the constant-mass variant (GAP 1); any statement at the level of DIST-1
in (RD) with the Hellinger distance (see F-1).

---

## 1. Findings

**F-1 (MINOR; §7 "Consequences", bullet 3; §0 Verdict line "Stretch S-FIT in its exponential form is dead").**
What is proved is a fixed-design, in-sample statement: Lemma X without (ND) is false. S-FIT is a stretch version of
DIST-1, i.e. it lives in (RD), with a random design, the population Hellinger distance and the (ND) remainder removed. To
transfer the counterexample there one needs two further steps, neither of which is in the file:
(a) a law ν_x (a triangular array) whose sample design reproduces the structure with constant probability: an anchor
plus ⌊√n⌋ near-copies at Schur eigenvalue ≍ log n/n, after sample standardisation and with only approximate sample
orthogonality of the u_j;
(b) a lower bound on the population quantity E_x min{1, Δ(x)²/4σ*²} for the far draws in terms of ‖μ̂ − μ‖²/n. Lemma T
only goes the other way, from sample to population upper bound.
Both are plausible, since the near-copy design is easy to realise with x_j = x₀ + τ′w_j, but they are unproved.
*Repair:* replace "Stretch S-FIT in its exponential form is dead" with: "the exponential (and (16)-type) form of S-FIT
cannot be proved through a fixed-design Lemma X without (ND); a random-design version of the counterexample (realisation
of the design + Hellinger lower bound) would refute S-FIT itself and is not done here."
Also make explicit that DIST-1 (1.1) itself is **not** contradicted: this design violates (ND), so the remainder of
(1.1) equals 1.

**F-2 (MINOR; §7 "Consequences", bullet 4).** The bullet says "The Proposition gives mass ≥ n^{−1}e^{−c′R/log n} at radius
R = (k/24) log n for fixed k", and concludes that "the extra logarithm [of Lemma X′] is not removable design-free". Two
problems:
(i) The constant is c₄(k) = (k+1)e^{−c_k/2−1}c₃^k/16 with c_k = k/β + 4k²/(3β). The term 4k²/(3β) is quadratic in k, so
c₄(k) = e^{−Θ(k²)} once k ≫ β. That is not of the form e^{−c′k} = e^{−24c′R/log n} uniformly in k. For each fixed k the
display is trivially true with a k-dependent constant, and then it says nothing about the shape in R.
(ii) Showing that the extra log of Lemma X′ is necessary would need the Proposition uniformly for k up to ≍ log n:
radius ≍ (log n)² ≍ tℓ_n at t ≍ log n, with mass ≥ n^{−cM}. The file proves it only for fixed k with n ≥ n₄(k) and n₄
unspecified. At k ≍ log n the quadratic loss e^{−2k²/(3β)} = n^{−Θ(log n)} is super-polynomial, so the route as written
cannot give it. The k² comes from the crude bound (Σ_J z_j)² ≤ k²L in (2.3); for random signs the typical size is kL, so a
signed selection of 𝒢 might remove it.
*Repair:* delete the display, or state it as "for each fixed k: mass ≥ c₄(k)/(2n) at radius (k/24) log n". Downgrade
"suggesting that the extra logarithm there is not removable design-free" to an explicit open question that needs (a) a
version uniform in k ≤ κ log n and (b) removal of the k² term.

**F-3 (MINOR; §8 "In-probability form", first sentence).** The file says the in-probability form "holds trivially" in this
design because Step A gives π(∅) ≥ 1 − e³d/√n on 𝓔. But P(𝓔) ≥ 0.6 only, so this does not give 1 − π(∅) → 0 in
probability: three components of 𝓔 have non-vanishing failure probability as defined (𝓔₀: 0.046, 𝓔₁: 1/8, 𝓔₃ via
Markov: 0.16).
The claim is true, with this easy repair:
- replace 𝓔₀ by |z₀| ≤ ω_n, with ω_n → ∞ and e^{ω_n²}d/√n → 0;
- replace 𝓔₁ by the window ω_n√N; then ε = O(ω_n/√n) in (i);
- control 𝓔₃ by Chebyshev instead of Markov. Var(Ã′) ≤ d^{−1}p′E[e^{(1+ε)z²}1{z² ≤ 2L}] ≤ C p′² e^{2εL}/(βL^{3/2}), so
  Var(Ã′)/p² → 0 and P(Ã′ > p/2) → 0, because E Ã′ ≤ 0.08p;
- note P(𝒯ᶜ) ≤ 1/√(πL) → 0.
Then Π(‖μ̂‖² > 0 | y) ≤ 1 − π(∅) → 0 in probability, since μ̂ = 0 under ∅. *Repair:* add these three sentences.

**F-4 (MINOR; §8 bullets 1–4, "More generally this mechanism cannot break it").** This is a heuristic. "E BF_j ≤ 1 for
superset directions at fixed variance" is not a statement with its hypotheses checked: H1 Lemma V(b) has the factor
(1 + η)^{s₀+|J|/2} and the D′ split, not BF_j ≤ 1. The step from "expected relative mass ≲ 2^{−j}" to "at best geometric in
M" is not proved either. The file does not claim it as a theorem, but the wording ("cannot break it") reads as one.
*Repair:* label the paragraph "Heuristic (not proved)".

**F-5 (NIT; §7).** The letter M has two meanings in one paragraph: the energy constant of (E; M), where the design has
M = 0, and the multiplier in t = M log n. Rename the second one (e.g. t = T log n).
Related: the refutation is stronger than §7 says. The design lies in (E; M) ∩ (C; M′) for **every** M, M′ ≥ 0, so no
constants depending on (s₀^r, A, σ*², M, M′, κ₀) can work. Saying "(E; 0), (C; 0)" is correct but undersells this; say it
explicitly.

**F-6 (NIT; §3, threshold n₁).** P(𝓔) ≥ 0.6 needs P(𝒯ᶜ) + 2/p′ + 4/(√p′m₁) ≤ 0.069. With P(𝒯ᶜ) ≤ 1/√(πL), this forces
L ≳ 67, i.e. n ≳ e^{134}. That is legitimate (n₁ is only claimed to exist) but needlessly huge.
The bound is loose. Monte Carlo (`p7_events.py`, 2000/2000/300 draws) gives P(𝓔) ≈ 0.78–0.80 at n = 10⁶, 10⁸, 10¹².
- P(𝒯) ≈ 0.83–0.84 is the main loss.
- Each other component is ≥ 0.95; 𝓔₃ is about 0.99 against the Markov bound of 0.84.
Truncating at z² ≤ 3L instead of 2L would make P(𝒯ᶜ) polynomially small and keep E Ã′ ≤ 0.09p (Markov: 0.18). Also, 𝒯 is
used only to bound P(𝓔₃ᶜ), not in any deduction on 𝓔, so it need not be part of 𝓔. Optional.

**F-7 (NIT; §2(b)).** "λ₊ ∈ [N, N(k+1)]": the upper end comes from trace = N(1 + k − (k−1)τ²) ≤ N(k+1). Fine, but state
it, because the bound f(λ₊) ≤ n + 1 used for D_S ≤ (n+1)d^k only needs f < n + 1 anyway.

**F-8 (NIT; §1).** The design exists only when d = 1 + 256 log⌊√n⌋ < n + 1; for example it is undefined at n = 400. State
this as part of "n large". The regime the construction is about (Nτ² = (d−1)/(n+1−d) ≪ 1) needs n ≫ 256 log n. At
n = 1600 one has Nτ² = 1.44; at n = 6400, Nτ² = 0.21.

No CRITICAL or MAJOR finding.

---

## 2. Line check, section by section

### §1 Design — VERIFIED
- Scale reduction σ* = 1: b = 0.01‖y_c‖²/N and Q^c_S are both quadratic in y_c, so π(S) is invariant under y_c ↦ σ*y_c,
  and θ_S | v, S, y and μ̂ scale by σ*. ✓ This agrees with bridge B0.
- u₀, …, u_{p′} orthonormal in ℝ^N needs p ≤ N, true for n ≥ 4. Columns x_j = U x_{c,j} are centred because col U = 1^⊥.
  ‖x_{c,j}‖² = N(a² + τ²) = N. ✓
- f(Nτ²) = d: with λ = (d−1)/(n+1−d), (n+1)λ + 1 = nd/(n+1−d) and λ + 1 = n/(n+1−d). ✓
  h = (d−1)/d, so 1 − h = 1/d. ✓ 1/h = (n+1)/n + 1/(nλ). ✓
  f(N) = ((n+1)(n−1) + 1)/n = n. ✓
  nNτ² = n(d−1)/(n+1−d) ≥ (n/(n+1))βL ≥ ¾βL. ✓ τ² ≍ log n/n². ✓
- K = min(p, ⌊n/2⌋) = p once ⌊√n⌋ + 1 ≤ n/2, so Ω = 2^{[p]}. ✓ Truth θ* = 0, S₀ = ∅, μ = 0, y_c = e. ✓
- z_j = u_jᵀe are iid N(0, 1) for j = 0..p′, and ‖e‖² − Σ_{j≤p′}z_j² ~ χ²_{N−p} is independent of them. ✓

### §2 Exact spectra and determinants — VERIFIED (F-7 nit)
- (a) G_J = N(a²11ᵀ + τ²I): eigenvalues N(ka² + τ²) ≥ N (once) and Nτ² (k − 1 times).
  D = f(N(ka² + τ²))d^{k−1} ≥ n d^{k−1}. ✓ ([P1] `lem:spec`(e): D = ∏f(λ_i), f increasing.)
- (b) The block form is right. Vectors (0, c) with c ⊥ 1 give eigenvalue Nτ² (k − 1 of them).
  In the basis (1, 0), (0, 1/√k) the remaining 2×2 block is N[[1, a√k], [a√k, a²k + τ²]], with det N²τ². ✓
  λ₊ ≥ max diagonal ≥ N and λ₊ ≤ trace ≤ N(k+1); λ₋ = N²τ²/λ₊ ≤ Nτ². ✓
  Hence n d^{k−1} ≤ D_S ≤ (n+1)d^k. ✓
- (c) D_{0} = n. ✓
- (2.1) checked case by case: (a) gives n^{−1/2}d^{1/2}d^{−|S|/2}; (b) gives n^{−1/2}d·d^{−|S|/2}; (c) gives n^{−1/2} ≤
  n^{−1/2}d^{1/2}. ✓
- (2.2): col X_{c,S} ⊆ span(u₀, u_j : j ∈ S∖{0}) holds also when 0 ∉ S. Q_∅ − Q_S = eᵀM_Se (M_∅ = 0) ≤ ‖P_Se‖² by
  M_S ⪯ P_S ([P1] `lem:spec`(b)). ✓
- Plug-in (2.3): X_{c,S}φ = √N u₀(φ₀ + aΣφ_j) + Σφ_j√Nτ u_j = Σh z_j u_j with the stated φ. ✓
  ‖e − Σh z_j u_j‖² = ‖e‖² − W + (1 − h)²W. ✓
  ‖Xφ‖²/n + ‖φ‖²/n = h²W(1/n + 1/(nNτ²)) + φ₀²/n. The bracket is (1 − h)² + h(1 − h) = 1 − h, using 1/h − 1 =
  1/n + 1/(nNτ²). ✓
  φ₀²/n = a²h²(Σz_j)²/(nNτ²). ✓
  With W_J ≤ kL and (Σz_j)² ≤ kW_J ≤ k²L: Q_∅ − Q_S ≥ W_J − kL/d − 4k²/(3β) ≥ W_J − c_k. ✓
- Numerical check (`p7_alg.py`, 300 random S per setting at (n, β) = (10⁵, 256), (10⁶, 256), (6400, 1)):
  - max of [lhs − rhs] over all trials is ≤ 0 for (2.1), both D bounds, (2.2), the exact plug-in inequality, (2.3) and
    the Step-C inequality;
  - the lower D bound is attained with equality at S = {j}, where D = n.

### §3 Good event — VERIFIED (F-6 nit)
- m₁ = (1/√(2π))·|{√L/2 ≤ |z| ≤ √L}| = √L/√(2π). ✓
  E a_j² = (2/√(2π))∫_{√L/2}^{√L}e^{z²/2}dz ≤ e^{L/2}m₁ = √p′m₁. ✓
- 𝓔₀: 0.0455. ✓ 𝓔₁: Chebyshev with Var χ²_N = 2N gives 1/8. ✓
  𝓔₂: 2/p′ (with j = 1..p′; if j = 0 is included the bound is still o(1)). ✓
  𝒯: p′·2φ(√(2L))/√(2L) = 1/√(πL). ✓
  𝓔₄: Var A ≤ p′√p′m₁, which gives 4/(√p′m₁). ✓
- 𝓔₃: on 𝒯, Ã = Ã′. E e^{(1+ε)z²/2}1{z² ≤ 2L} = (2/√(2π))∫₀^{√(2L)}e^{εz²/2}dz ≤ 2√(L/π)e^{εL}.
  With d^{−1/2} ≤ (βL)^{−1/2}, the constant is 2/√(πβ) = 0.0705 at β = 256 (recomputed). ✓
  E Ã′ ≤ 0.08p for large n, since εL = 8L/√n → 0. Markov gives 0.16. ✓
  P(𝓔₃ᶜ) ≤ P(𝒯ᶜ) + 0.16.
- Total P(𝓔ᶜ) ≤ 0.331 + o(1) ≤ 0.4 for n ≥ n₁. ✓
  Monte Carlo: P(𝓔) ≈ 0.78–0.80 at n ∈ {10⁶, 10⁸, 10¹²}.
- (i) Q_S ≥ N − 4√N − 4 − 2p′ ≥ n − 7√n for √n ≥ 5. (1+ε)(n − 7√n)/2 = (n + √n − 56)/2 ≥ ν when √n ≥ 56.02. ✓
- (ii) B = (1 + 0.02/N)‖e‖² ≤ N + 4√N + 0.1 ≤ n(1 + 5/√n), and ν/B ≥ ½(1 − 5/√n). ✓

### §4 Step A — VERIFIED
- D_∅ = 1. (1 + x)^ν ≤ e^{νx} with x ≥ 0. ν/(2b + Q_S) ≤ (1+ε)/2 by (i). Then (2.2), (2.1).
  Pulling out e^{(1+ε)z₀²/2} for all S is an upper bound. ✓
- e_{k′}(ã) ≤ Ã^{k′}/k′! for nonnegative weights. ✓
  [w(k′)/w(0)]/k′! = ∏_{i<k′}(2p−1−i)^{−1} ≤ p^{−k′} for k′ ≤ p = K. ✓
- On 𝓔₀ ∩ 𝓔₃: Σ ≤ e^{2(1+ε)}·d·n^{−1/2}·Σ_{k′≥1}2^{−k′} ≤ e³(1 + βL)/√n → 0. ✓
  (The threshold is large, about √n ≳ 2·10⁴L, but finite.)
- Numerically, π(∅) has median 0.98–0.995 and is ≥ ½ in ≥ 97.5% of draws at every (n, β) tried (§3 of this report),
  even far below n₂.

### §5 Step B — VERIFIED
- x = (Q_∅ − Q_S)/B ∈ [0, 1), and (1 − x)^{−ν} ≥ e^{νx}. ✓ νx ≥ ½(1 − 5/√n)(Q_∅ − Q_S) by (ii).
  Lower bound by (2.3) (valid: J ⊆ 𝒢 gives z_j² ≤ L); upper bound Q_∅ − Q_S ≤ z₀² + W_J ≤ 4 + kL on 𝓔₀.
  (5/(2√n))(4 + kL) ≤ 1 for n ≥ n(k). e^{W_J/2} = ∏_J a_j. ✓
- w(k+1)/w(0) = 1/C(2p−1, k+1) ≥ (k+1)!/(2p)^{k+1}. ✓ D_S ≤ (n+1)d^k by §2(b). ✓ |S| = k + 1 ≤ K. ✓
- Elementary symmetric bound: tuples with i_l = i_m for a fixed pair contribute Σ_i a_i²A^{k−2} ≤ (max a)A^{k−1}.
  There are C(k, 2) ≤ k²/2 pairs, so k!e_k ≥ A^k(1 − k² max a/(2A)). ✓
  max a ≤ √p′ and A ≥ p′m₁/2 give k² max a/(2A) ≤ k²/(√p′m₁) → 0. ✓
  (Checked numerically on random positive vectors.)
- Assembly: (k+1)e^{−c_k/2−1}/(4p√(n+1))·((p′/p)m₁/(4√d))^k. m₁/√d ≥ 1/√(2π(β+1)) iff L ≥ 1. ✓
  c₃ = 1/(8√(2π·257)) = 3.11·10⁻³. p√(n+1) ≤ 2n. π(∅) ≥ ½.
  Hence π(𝒮_k) ≥ c₄(k)/n. ✓
- Uniformity: 𝓔 does not depend on k, so on one event of probability ≥ 0.6 the bound holds simultaneously for all
  k ≤ k_max once n ≥ max_{k≤k_max} n₃(k). ✓

### §6 Step C and the Proposition — VERIFIED
- X_{c,S}θ | v, S, y ~ N(M_Se, vM_S). ‖μ̂ − μ‖ = ‖UX_{c,S}θ‖ = ‖X_{c,S}θ‖ since μ = 0 and U is an isometry. ✓
  With ω symmetric, P(mᵀω ≥ 0) ≥ ½, and then ‖m + ω‖² ≥ ‖m‖². ✓ This holds for each v, hence after integrating v. ✓
- eᵀM_Se = (P_Se)ᵀM_Se because M_Se ∈ col X_{c,S}. Cauchy–Schwarz and (2.2) give the bound
  ‖M_Se‖² ≥ (W − c_k)²/(W + z₀²), valid since W_J ≥ kL/4 ≥ c_k for large n.
  (W − c)² − (W − 2c − z²)(W + z²) = c² + 2cz² + z⁴ ≥ 0. ✓
  kL/4 − 2c_k − 4 ≥ kL/8 ≥ (k/24) log n, since L = log⌊√n⌋ ≥ (log n)/3 for large n. ✓
- Proposition: Π(‖μ̂‖² ≥ (k/24) log n | y) ≥ ½π(𝒮_k) ≥ c₄(k)/(2n) on 𝓔. ✓

### §7 Refutation — VERIFIED (F-1, F-2, F-5)
- The quoted form drops the size clause and keeps distance and variance. Π(A ∪ B | y) ≥ Π(A | y), so the distance part
  alone suffices. ✓
- M := max(M₀, 2/c), t = M log n. t ≤ n^{1−κ₀} for large n. ✓
  k = ⌈24CM⌉ + 1 gives k/24 > CM, so {‖μ̂‖² ≥ (k/24) log n} ⊆ {‖μ̂‖² > CMσ*² log n}. ✓
  c₄(k)/(2n) > n^{−2} ≥ n^{−cM}, and 0.6 > 2n^{−cM}. ✓
- The design is in (E; M) ∩ (C; M′) for every M, M′ ≥ 0. p = ⌊√n⌋ + 1 ≤ n^A, p ≥ 2, s₀ = 0 ≤ K, Gaussian noise. ✓
- The design violates (ND; c_D, m_n(t)) for every fixed c_D > 0 and large n:
  - m_n(t) ≥ 2;
  - every pair J has D_J ≤ (n+1)d (both pair types, §2(a)/(b));
  - so the j = 2 average is ≥ ((n+1)d)^{−1/2} > [c_D(n+1)]^{−1} once d < c_D²(n+1).
  ✓ (j = 1 holds when c_D ≤ n/(n+1).)
- "(16)-form": for fixed M the probability 0.6 does not tend to 0, so that form also fails. ✓
- "(ND) or a substitute excluding ≍ n^a directions at Schur eigenvalue ≍ log n/n": consistent. The same computation
  with p′ = ⌊n^a⌋ gives mass ≍ n^{−1/2−a}, still polynomial. With p′ ≍ log n near-copies, each direction fits only
  O(log log n), so polynomially many copies are needed. The file does not prove this extension; it is a remark.

### §8 What is not broken — the remarks are acceptable as commentary (F-3, F-4). GAP 1 and GAP 2 are correctly stated as open.

---

## 3. Numerical check (duty 2)

Set-up: the design of §1 in the coordinates (u₀, …, u_{p′}) plus the orthogonal remainder.
‖e‖² = Σz_j² + χ²_{N−p} (exact). M_S, D_S are computed from H_S = (n+1)G_S + I (exact, per model).
The exact model posterior π(S) ∝ w(|S|)D_S^{−1/2}(2b + Q_S)^{−ν} is computed over **all models of size ≤ 4** (size ≤ 3 at
n = 25600). The mass of the omitted sizes is negligible: mean mass by size decays geometrically, e.g. at n = 6400,
β = 256 it is 0.981 / 1.8·10⁻² / 9.2·10⁻⁴ / 4.2·10⁻⁵ / 1.8·10⁻⁶. There were 200 noise draws per setting (seed = n).

Quantities reported:
- n·π(𝒮_k), the model mass of Step B's family;
- n·Π_models(‖M_Se‖² ≥ R) at R = (k/24) log n (the Proposition's radius) and at R = (k/2) log n (a stricter radius).

The posterior noise factor ½ of Step C is a proved bound and is not simulated.

**β = 256 (the file's constant).** The design does not exist at n = 400, since d = 768 > n + 1 (F-8).

| n | p | Nτ² | median π(∅) | med n·π(𝒮₁) | med n·π(𝒮₂) | med n·π(𝒮₃) | freq{nΠ(‖M_Se‖² ≥ (k/24)log n) ≥ c₄(k)}, k = 1, 2 |
|---|---|---|---|---|---|---|---|
| 1600 | 41 | 1.44 | 0.983 | 2.02·10⁻² | 4.33·10⁻⁴ | 6.7·10⁻⁶ | 1.000, 1.000 |
| 6400 | 81 | 0.21 | 0.991 | 2.17·10⁻² | 5.02·10⁻⁴ | 8.7·10⁻⁶ | 1.000, 1.000 |
| 25600 | 161 | 0.053 | 0.995 | 2.30·10⁻² | 5.23·10⁻⁴ | (size 4 not enumerated) | 1.000, 1.000 |

Here c₄(1) = 1.42·10⁻⁴, c₄(2) = 6.6·10⁻⁷, c₄(3) = 2.7·10⁻⁹. n·π(𝒮_k) ≥ c₄(k) in 100% of draws for k = 1, 2, 3 at every
n where 𝒮_k was enumerated.

**β = 4 and β = 1 (same mechanism, d ≪ n already at these n; the Proposition's probability bookkeeping needs β large,
but Steps A–C do not).**

| β | n | median π(∅) | med n·π(𝒮₁) | med n·π(𝒮₂) | med n·π(𝒮₃) | freq k = 1, 2 at radius (k/24) log n (level c₄(k)) |
|---|---|---|---|---|---|---|
| 4 | 400 | 0.949 | 0.145 | 1.94·10⁻² | 1.85·10⁻³ | 1.000, 1.000 |
| 4 | 1600 | 0.977 | 0.158 | 2.45·10⁻² | 2.67·10⁻³ | 1.000, 1.000 |
| 4 | 6400 | 0.988 | 0.152 | 2.41·10⁻² | 2.85·10⁻³ | 1.000, 1.000 |
| 1 | 400 | 0.940 | 0.194 | 3.77·10⁻² | 5.03·10⁻³ | 1.000, 1.000 |
| 1 | 1600 | 0.972 | 0.210 | 4.78·10⁻² | 8.15·10⁻³ | 1.000, 1.000 |
| 1 | 6400 | 0.986 | 0.201 | 4.75·10⁻² | 8.25·10⁻³ | 1.000, 1.000 |

**Reading.**
- *The n⁻¹ scaling is visible.* For each fixed k, the median of n·π(𝒮_k) is flat in n over a 16-fold (β = 4, 1) or
  64-fold (β = 256, k ≤ 2) range of n, within sampling noise, with a slight upward drift. So the far model mass is ≍ c(k)/n,
  not n^{−ck}.
- *Geometric dependence on k.* The ratio from k to k + 1 is roughly constant: about 1/45 at β = 256, 1/7 at β = 4, 1/5 at
  β = 1. This is the c₃^k shape, with empirical ratios far larger than the proof's c₃ = 3.1·10⁻³. The proof's constants
  are conservative by orders of magnitude.
- *The stated radius (k/24) log n is weak at these n.* At k = 1 most of the far mass there comes from models of size ≤ 1
  fitting z₀ (e.g. median n·mass 52.8 of 55.7 at n = 6400, β = 256). At the stricter radius (k/2) log n:
  - β = 256, median n·mass for k = 1, 2, 3: 0.52, 0.19, 1.7·10⁻³ (n = 1600); 1.13, 0.39, 3.8·10⁻³ (n = 6400);
    2.28, 0.80, 9.9·10⁻³ (n = 25600). Again flat or increasing in n.
  - The frequency of n·mass ≥ c₄(k) at that radius is 1.00 / 0.99–1.00 / 0.88–0.99 for k = 1, 2, 3. The k = 3 values are
    limited by the size cap and by needing three near-copies with z² ≳ log n/2.
- The freq{π(∅) ≥ ½} is ≥ 0.975 in every setting.

Conclusion: the numerics confirm the Proposition qualitatively, and quantitatively with large margin. Over k ≤ 3 the far
model mass is ≍ c(k)/n with c(k) geometric in k and flat in n.
[CONTROL — orthonormal design, see §3a.]

---

## 4. Lemma X′ and display (1.2) (duty 3) — no contradiction (verified)

Lemma X′: P_e[Π(‖μ̂ − μ‖² > Cσ*²tℓ_n or … | y) > e^{−ct}] ≤ 2e^{−ct} for t ≥ M₀ log n. Here ℓ_n = log(p ∨ n) = log n.
- The bad radius is ≥ CM₀(log n)². The Proposition bounds mass from below only at radius (k/24) log n for fixed k. For
  n large, (k/24) log n < CM₀(log n)², so the X′ bad set is a subset of the Proposition's set. A lower bound on the
  larger set implies nothing about the smaller one.
- Using growing k to reach (log n)² would need k ≍ 24CM₀ log n. The Proposition is not proved uniformly in k (n₄(k)), and
  its own constant c₄(k) ≤ e^{−2k²/(3β)} = n^{−Θ(log n)} at that k, far below n^{−cM₀}. So even a formal extrapolation
  gives no contradiction.
- Heuristically X′ is consistent with the design. Each direction fits at most 2L + O(1) ≈ log n of noise on 𝒯. Reaching
  radius CM₀(log n)ℓ_n needs ≳ CM₀ℓ_n/2 directions, which costs ≈ 2^{−CM₀ℓ_n/2} (prior, geometric size tail; Lemma S
  type) = n^{−Θ(CM₀)} ≤ n^{−cM₀} for c ≤ (C log 2)/2.
- (1.2), DIST-2: radius C√(tℓ_n/n) in Hellinger, i.e. d_H² ≍ tℓ_n/n ≍ (log n)²/n at the smallest t. The same argument
  applies, and (1.2) is a random-design statement with no (ND) in its remainder, which this fixed design does not reach
  anyway (F-1).
- (1.1), DIST-1 is not contradicted, because (ND) fails for this design and its remainder is 1.

The file's own statement "Lemma X′ (radius tℓ_n) is not contradicted" is correct.

---

## 5. What is established and what is open (duty 4)

Established (subject to the amendments above, none of which affects it):
1. **Lemma X without (ND) is false, in its exponential form.** For every (c, C, C′, M₀, n₀) and every (s₀^r ≥ 0, A ≥ 1,
   σ*², M, M′ ≥ 0, κ₀), there is a design in (E; M) ∩ (C; M′) with p ≤ n^A, s₀ = 0, on which
   P_e[Π(‖μ̂ − μ‖² > Cσ*²t | y) > e^{−ct}] ≥ 0.6 > 2e^{−ct} at t = max(M₀, 2/c)·log n for all large n.
   The clause that fails is the **distance clause** (hence the joint conclusion). The variance clause is not involved,
   and the size clause was already known to fail.
2. **It also fails in the "(16)-type" form**: inner level e^{−ct} = n^{−cM}, outer probability only required to tend to 0.
3. More quantitatively: on this design, with probability ≥ 0.6, Π(‖μ̂ − μ‖² ≥ (k/24)σ*² log n | y) ≥ c₄(k)/(2n) for every
   fixed k. At any radius of order log n the posterior can put mass of exact order n⁻¹, not n^{−cM}, when (ND) fails. So
   an (ND)-type condition (or a substitute excluding polynomially many directions at Schur eigenvalue ≍ log n/n) is
   **necessary for the exponential distance clause of Lemma X**, not only for its size clause.

Not established:
- **In-probability form** under (E), (C) alone: Π(‖μ̂ − μ‖² > M_n log n | y) → 0 for M_n → ∞. Neither proved nor broken
  (GAP 2; non-supersets open, route F-c). In this particular design it holds (with the F-3 repair). The general "cannot
  break it" argument is heuristic (F-4).
- **GAP 1** (constant-mass c^{CM} variant with s₀ = 1): heuristic only. It needs Step A relative to S₀ = {0}, including
  non-supersets J ∌ 0.
- **Lemma X′'s extra logarithm being necessary**: not shown (F-2); it needs a k-uniform version without the k² loss.
- **Theorem-level consequences** (S-FIT exponential in (RD), Hellinger): need a random-design realisation and a
  population lower bound (F-1).
- The conjectured design-free statement (§8) is a conjecture.

---

## 6. Verdicts

| section | verdict |
|---|---|
| §1 Design | VERIFIED |
| §2 Spectra, determinants, (2.1)–(2.3) | VERIFIED (F-7 nit) |
| §3 Good event, P(𝓔) ≥ 0.6, (i), (ii) | VERIFIED (F-6 nit) |
| §4 Step A | VERIFIED |
| §5 Step B, (5.1) | VERIFIED |
| §6 Step C, Proposition | VERIFIED |
| §7 Refutation of the exponential clause | VERIFIED-WITH-AMENDMENTS (F-1, F-2, F-5: commentary bullets overclaim; the refutation itself is correct) |
| §8 What is not broken; GAP 1, GAP 2 | VERIFIED-WITH-AMENDMENTS (F-3 missing argument for "holds trivially"; F-4 heuristic to be labelled) |
| Numerical check | CONFIRMS (n⁻¹ scaling flat in n, geometric in k; 100% of draws above c₄(k) for k = 1, 2) |

STATEMENT-CHANGE REQUESTS in the file: none.

**Overall verdict: VERIFIED-WITH-AMENDMENTS.** The Proposition and the refutation of Lemma X without (ND)
(exponential and (16)-type forms, distance clause) are correct. The amendments are confined to the commentary: F-1 (S-FIT
claim), F-2 (the "extra log not removable" remark and the e^{−c′R/log n} display), F-3 and F-4 (§8 wording).
