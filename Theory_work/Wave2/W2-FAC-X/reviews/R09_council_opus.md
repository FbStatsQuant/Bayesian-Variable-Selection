# R09 — Council seat (Claude Opus 5.5): Theorem FAC-CS-iid (W2-FAC-X, round 1)

Deliverable reviewed: STATEMENT.md v3 (locked), lemmas/X1–X6, REPORT.md §1–§4, §6 (brief: reviews/COUNCIL_BRIEF.md).
Not reviewed: Target 2 (REPORT §5, X7, T2/). Earlier reviews R01–R07 were read, but every step below was re-derived or
re-computed here. Scope rule applied: all results are asymptotic. I did not count the size of n₀ as a defect.

## Verdict

| gate | verdict |
|---|---|
| G1 correctness of every step | **PASS** |
| G2 hypotheses used = hypotheses stated | **PASS** |
| G3 no hidden assumptions | **PASS** |
| G4 cited lemmas have adequate status | **PASS** |
| G5 constants / rates tracked | **PASS** |
| G6 fidelity to the method | **PASS** |

**Overall score: 9.0 / 10.** No REQUIRED fixes. Items 1–6 below are recommended (minor or editorial).

## What I re-derived or re-computed (scratch: reviews/R09_scratch/)

1. **X1 algebra (symbolic, c1_identities.py).** The swap identity
   (1+γ_{k−1})[(1−γ_k)²(τ_l+γ_{k−1}τ_j)² − τ_j²] = τ_l² − τ_j² − γ_k(τ_l−τ_j)², the addition factor
   (1+γ_k)(1−γ_{k+1})² = 1−γ_{k+1}, 1/(1−γ_k) = 1+γ_{k−1}, and γ_k = ℓ²φ²/(N+kℓ²φ²) = 1/(k+κ) all reduce to 0 in sympy.
2. **X1 representation from explicit rows (c2_rotation.py; n = 300, p = 25, ρ = 0.6, random mean, two truths).** I
   built e₁, e₂, ξ, a, η, φ, W directly from the rows, without using iid_core.
   * g_j decomposition error is 1e−14.
   * RSS_T = ‖e‖²/(1+q_T) holds to 3e−16 (relative), and the Schur identity q_T − q_{T∖j} = ω_j² holds to 1e−17.
   * For the production score (SoP D0: H = (n+1)G + I, ψ = 0.02 + Q, ν = 0.01 + n/2, w(k) = ½/C(2p−1,k)), X1.4 (g3)
     without the r_j term reproduces the exact G_del = 3.08524852 to 5e−7 (that remainder is the ridge term r_j).
     M_T = 0.478 lies inside the stated band.
3. **Hand re-derivation of each step.** I re-derived the following:
   * X1.1 (conditional-independence argument);
   * X1.2–X1.4 (g1)–(g5), including the prior ratio (2p−k)/k from w(k) = ½/C(2p−1,k);
   * Proposition X2 (i)–(v), including the D5 decomposition T⁰∖j = ([p]∖j) ∖ (I(a,b)∖j) with both sets in 𝒜_j, and
     the second-order bound, which needs p ≤ √n;
   * X3 (iii) (both cases), (iv), (vii) and (viii);
   * the X4.1 envelope |x_T| ≤ 1.5H̄ (the discriminant d(d−3k) < 0 for d ≤ 2, k ≥ 1) and the slack lemma (the
     common factor (1+γ_{k−1})M_T is T-only);
   * D6, D7 (both μ regimes) and D8 (pair-separation bound);
   * (B1)–(B4) of X4.4, including Case A's J″ ≤ 5m bootstrap, Case B, and the wide-phase B1 contradiction;
   * the X4.5 entry, exact-structure induction and (E-side) margin (x ≥ H̄/(2(s₀+m₁+κ)) ≫ δ_e + ϖ in regime L);
   * X4.6 (truth moves);
   * X5.2: the population c(U,l) formula is recomputed from Σ = (1−ρ)I + ρ11ᵀ,
     Cov(r_l, x_i) = ρ(1−ρ)/(1+(u−1)ρ) and Var(r_l) = (1−ρ)(1+uρ)/(1+(u−1)ρ); this yields exactly FACB's
     (1−ρ)[ϑ_l + ρϑ(S₀∖U)/(1+(u−1)ρ)], so (FS)(a),(b) are exactly the nonvanishing conditions;
   * the X5.3 dichotomy and the uniqueness argument;
   * X6.1's (H0) list against T03♯'s hypotheses (FINAL s3_posterior.tex:5-13: R, SE_λ(j₀), SE_w(m♯;g₀), BM-∞, p ≤ n^A);
     all of them follow from the full-matrix floor on 𝒜_n with z-free constants.
4. **Exact-δ path stress test at extreme ρ (c3_paths.py → c3_out.txt).** N1X only used ρ ∈ {0.3, 0.7} and an
   empirical proxy for δ. I computed the **exact** δ_j(T) = τ̂_j(T) − (ξ_j − x_T) from the Bartlett coordinates along
   production LS0 paths from [p]. Configurations: ρ ∈ {0.02, 0.05, 0.95}, n ∈ {10⁴, 10⁵, 10⁶}, p ∈ {100, 300}
   (log p/log n up to 0.62), s₀ ∈ {1, 2, 3}, 2 seeds each; 16 runs. Results:
   * 16/16 paths are pure null deletions of length p − s₀ ending at S₀;
   * max|δ| / (H̄√(p log n/n)) ∈ [0.18, 0.25];
   * the (R_ϖ) excess |ξ_{j°} − x_T| − d_T is ≤ 1.59·max|δ|, below the claimed 2ϖ;
   * the band overshoot is ≤ 1.63·max|δ|, below the claimed 4.3ϖ;
   * max addition gain/log n ≤ −0.29.

   So the scale of ϖ and the constants 2 and 4.3 are consistent with the exact perturbation.

## Gate reasons

**G1 (PASS).** I found no incorrect step. These are the load-bearing points, each checked:
* **Exact independence of ξ and W (X1.1).** This is what lets D5 union-bound over the ξ-measurable family of interval
  sets. The path sets depend on W, but only through which (a,b) is selected and through the band. The band is
  controlled crudely by counts (D6/D7) and fed back through the condition p H̄√(log n/n) → 0.
* **The induction in X4.** It only uses the established prefix (the dependency table is accurate).
* **X3's crossing lemma.** Its general-|K| constant c(κ′) is correctly used in regime (S) and in the end phase, where
  |K| < 3 can occur.
* **X4.5's claim that FACB L4.4 holds "verbatim with τ̂".** It is argued in aggregate rather than bound by bound. I
  checked E-del, E-side, E-add and E-swap individually: each margin is Θ(log n), or (H̄−x)·x ≫ ϖ for E-side. The
  perturbations are O(H̄ϖ + ϖ² + H̄⁶/n) = o(1) because H̄ϖ → 0. The import is sound (recommendation 4).

**G2 (PASS).**
* (FS) is used only in X5, and X4 explicitly does not need it.
* (P-½) is used through A₁ ∈ (limsup, ½): in the second-order bound (p ≤ √n), band absorption, D2's p² ≤ n union
  bound, the bulk addition margin, and T03♯ with A = ½.
* (θ) is used through fixed sign-corrected raw coefficients ϑ (X4.6 uses |β_j| = |ϑ_j|; X5/X6 use θ* = D_xβ with
  |sd_j − 1| ≤ δ′_n).
* Model R's Gaussianity and the independence of ε are used in X1 and X5. The arbitrary mean is removed by centring.
* (CS-R) is used with Υ_n = I w.l.o.g.
* σ² > 0 fixed and s₀ ≥ 1 fixed are both used. No unused or missing hypotheses.

**G3 (PASS).**
* The random partition and N₀ are handled by uniformity over all |𝔫| ≤ 15, and in X5 by conditioning on Z.
* Nondegeneracy is an almost-sure event (ND_n) intersected into 𝔊_n.
* Ties are handled because every maximiser satisfies (R_ϖ).
* p bounded and p = s₀ are covered by the empty-max conventions and regime (S).
* K = p eventually.
* I found no implicit sample-splitting, independence or rate assumption.

**G4 (PASS).** Statuses quoted in STATEMENT §7, REPORT §3 and X6 match the sources (CITECHECK 13/13; I spot-checked
s3_posterior.tex:5-20 and the FACB and FACA status lines). The inputs are:
* FACB L1–L5: theorem-level PROVED-CHECKED (template, L2.4, L4.4, L5.2, L5.4);
* FACA L5.1 de-randomisation pattern: PROVED-CHECKED;
* T03♯, M5(0), Lemma CR, Lemma CAP, Proposition F, and A2 (PROVED (A2), checked by A3);
* [OP]: "PROVED (by this seat, unchecked)" inside the PROVED-CHECKED Theorem GEN, with that qualification carried
  into X6.4.

Each of these is adequate for its use.

**G5 (PASS).**
* ε_b, K₁, m₁, T₀, c_w and c₁ are explicit, and the slack constants are explicit: 2ϖ and 4.3ϖ, ¾ϖ, ϖ/10, and
  4.1ϖ → 4.3ϖ.
* The margins are explicit: 0.35 log n, −0.7(½ − A₁) log n, −0.6(½ − A₁) log n, c_D log n, and
  c = min{0.29, c_D/2, 0.6(½ − A₁)}.
* n₀ depends only on (ρ, ϑ, σ, s₀, A₁).
* The rate ϖ_n = C₀H̄√(p log n/n) + n^{−1/3} is tracked, and the absorption criterion is stated as sufficient, not
  necessary.
* One traceability gap remains (recommendation 2).

**G6 (PASS).** All of these match SoP 02_method.tex:93-96 / 04_theory.tex:69-74, and iid_core uses the same forms:
* score: H = (n+1)G + I, i.e. (n+1)(G + ε₁I); Q = yᵀy − n zᵀH⁻¹z; ν = 0.01 + n/2; ψ = 0.02 + Q;
* prior: w(k) = ½/C(2p−1,k), with cap K = min(p, ⌊n/2⌋);
* standardisation: ‖x_j‖² = n−1, y = Y/s.

The method itself is also matched:
* The local search (SoP 02_method.tex:463-469 and code lines cited there) scans every feasible flip and swap and moves
  to the best strict improvement with lexicographic ties. X4 bounds every swap, which covers this.
* MR1 cap a_n = ℓ_n + |S̃₀| as on main 4676af6.
* The start mode is the unique maximiser of γ₀ (block-product with BB prior), so e4/e4′ are irrelevant.
* No method change.

## Numbered issues (none REQUIRED)

1. **MINOR — REPORT §6, row "idiosyncratic Ψ ∝ I".**
   * *Already fixed:* REPORT.md was edited on disk while this review was running. The closing "Population-level
     restatement" sentence, which presented X7 content as established, was replaced by a correct split into the
     checked class and unchecked Target-2 extensions. The "equal loadings" row now says FAC-NCS is outside this
     verdict.
   * *Still open:* "diagonal Ψ with unequal entries is absorbed by whitening (X7 uses this)" is misleading. After
     standardisation, unequal Ψ with equal loadings becomes a one-factor model with **unequal** loadings
     λ_j/√(λ_j² + ψ_j), i.e. Target 2. That case is not covered by FAC-CS-iid, and is reached only through unchecked
     §5 results.

   *Fix:* "reduces to general loadings (§5, unchecked; outside this verdict)". This matters because W2-UNI will read
   §6 as an ingredient list.
2. **MINOR — STATEMENT §3 / X2 header (traceability of C₀).**
   * STATEMENT §3 says "C₀ = C₀(ρ) from lemmas/X2–X4". The actual choice is C₀ = 6C_X (X4.0).
   * X2's preamble says its constants depend on ρ "and, where stated, on σ, ϑ, s₀". C_X in Proposition X2 depends on
     ρ only (it involves only W, ξ, a, η, φ), but this is not said explicitly.

   *Fix:* write "C₀ := 6C_X, with C_X = C_X(ρ) the constant of Proposition X2" in STATEMENT §3 and X2.
3. **EDITORIAL — REPORT §6 "sparse eigenvalue floor" row:** "from Bai–Yin" should be "from Davidson–Szarek (X2 D1)".
   That is the bound actually used.
4. **MINOR (presentation) — X4.5.** The transfer of FACB L4.4 is argued in aggregate ("every FACB L4.4 bound has a
   margin of order log n …"). Only (E-side) is re-done explicitly; I checked the other three myself and found them
   sound. *Suggestion:* add a 4-row table (bound, FACB margin, perturbation size) so the transfer can be audited
   without re-deriving L4.4.
5. **EDITORIAL — X2 status line:** the text "(empirical the fitted empirical proxy δ̂ …" is garbled (duplicated
   words).
6. **EDITORIAL (evidence) — REPORT §3 / N1X.** N1X covers only ρ ∈ {0.3, 0.7} and uses a fitted proxy for δ.
   *Suggestion:* cite R09_scratch/c3_out.txt, or rerun N1X with exact δ at extreme ρ. My 16 exact-δ runs at
   ρ ∈ {0.02, 0.05, 0.95} give max|δ| ≈ 0.2·H̄√(p log n/n), an (R_ϖ) excess ≤ 1.6·max|δ| and a band ≤ 1.63·max|δ|.

## Attempts to break the result (all failed)

* **Path-dependent T and D5.** T on the path is not ξ-measurable. Resolved because T⁰(a,b) ranges over a ξ-measurable
  family covered by the union bound, T Δ T⁰ ⊆ band ∪ 𝔫, and the band is bounded by counts. Correct.
* **Second-order term at A₁ → ½.** r_n²√k H̄ ≍ p^{3/2}H̄/n ≤ √(p/n)H̄ needs p ≤ √n. It holds under (P-½).
* **Approximate argmin making holes non-intervals.** This is exactly X3. The R03 counterexamples are correctly
  excluded by the d_i-based (not side-based) crossing bound. In regime (S) and in the end phase, the general-|K|
  constant c(κ′) < c₁ makes crossings impossible.
* **End-phase side choice under a ϖ error.** With I ≥ 1 the margin is 2x − 2δ_e > 2ϖ because H̄/m₁ ≫ δ_e + ϖ in
  regime (L). With I = 0 either side is allowed.
* **c_D → 0 (ρ → 1, s₀ = 1).** c_D stays a fixed positive constant for fixed ρ. End-phase swap bounds are o(log n)
  when |I| ≤ 1, and ≤ 8ε_b log n < ½ log n when |I| ≥ 2. Holds.
* **Random N₀ correlated with ξ.** Removed by uniformity over all |𝔫| ≤ 15. In X5 it is handled by conditioning on Z
  with z-free constants.
* **(H0) under the random design.** Every T03♯ hypothesis holds on the Z-event 𝒜_n with common constants. The
  every-sequence de-randomisation is sound (1 − π is bounded, so O_P implies convergence in expectation).
* **Numerics at extreme ρ.** No violation (above).
