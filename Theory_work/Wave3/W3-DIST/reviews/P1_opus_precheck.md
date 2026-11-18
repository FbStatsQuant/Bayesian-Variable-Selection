# W3-DIST — P1 same-family pre-check of the reader versions (§1R) and bridges (§3) — Claude Opus 5.5, effort high

Object: `STATEMENT.md` v1.2, §1R (Setup, (A1)–(A6), Theorem A, Theorem B, Corollary C, Remarks) and §3 "Bridges"
(B0, B1, B1′, B2-core, B2, B3), with `TARGET.md` §6 for Q7. The master statements (1.1), (1.2), DIST-3 and DIST-C are taken
as given. Files read: the files allowed by the brief and nothing else; none of W3-DIST `reviews/`, LOG, CHECKPOINT_* or
BRIEF.md. One numerical check (R script in my scratchpad, not in the repo) is reported under P1-04.
This is a same-family pre-check. It is not a review layer.

## Verdicts per clause

| clause | verdict | driving findings |
|---|---|---|
| Theorem A | REPAIRABLE | P1-03 (the hypothesis depends on M and on the unspecified M₀); P1-06; NITs |
| Theorem B | REPAIRABLE | P1-01 (wording of "(A4) strengthened to": read as a replacement, it drops the hypothesis that gives (F_w)) |
| Corollary C | SOUND-AS-STATED | P1-09 (last sentence says nothing), P1-12 (NIT) |
| B0 | REPAIRABLE | P1-05 (a statement about the law is not enough; the pathwise form via R′(a′) is needed and works) |
| B1 | SOUND-AS-STATED | P1-11 (NIT) |
| B2-core | REPAIRABLE | P1-07 (literally false when q ≥ ep; the application is unaffected) |
| B2 | REPAIRABLE | P1-04 (the stated determinant-ratio derivation is false; the conclusion holds by interlacing) |
| B3 | SOUND-AS-STATED | (given P1-01's wording repair in Theorem B) |

## Findings

### P1-01 — MAJOR — Theorem B, "(A4) strengthened to λ_min(Corr(x_T)) ≥ ψ … for every set T of at most (2A + 3)s + 2 predictors"
**Problem.** B3 uses two floors:
- (F_λ), from the fixed floor ψ on sets of bounded size;
- (F_w) with g₀ = c_ψ/8 on sets of size up to m♯_n + s. This comes from the **original** (A4) (floor c_ψ/n on sets of
  size up to q_n = ⌈C_q log n⌉) through B2.

The new condition is not a strengthening of (A4): it puts a larger floor on smaller sets. So it is neither stronger nor
weaker. Read as "replace (A4) by the following", which is how most readers will take "(A4) strengthened to", the hypothesis
that produces (F_w) is gone.

**Counterexample to the route under that reading.** Take L := (2A + 3)s + 3. Let x_{k_1}, …, x_{k_{L−1}} be i.i.d.
N(0, 1) nulls, let x_{k_L} := (x_{k_1} + … + x_{k_{L−1}})/√(L − 1), and let all other coordinates be independent N(0, 1).
- (A3) holds. It is a Gaussian vector, and directions with zero variance are allowed.
- (A5) and (A6) can be arranged on supp β*, which is disjoint from the k's.
- Every set of at most L − 1 coordinates has a correlation floor ψ(L) > 0. So the replacement reading holds with
  ψ = ψ(L).
- But G_T is singular almost surely for T = {k_1, …, k_L}. Since L ≤ m♯_n for large n, (F_w) fails for every n, and W3-POST
  Theorem 1 cannot be applied.

The conclusion of Theorem B may still hold in this example (a single exact dependence among nulls with a bounded
representation looks compatible with [P2] (OS), via [P2] A1). That is not the declared route (DIST-3 + W3-POST Thm 1 + B3).

**Minimal repair.** "Assume (A1)–(A5) with q_n := ⌈C_q log n⌉, and in addition λ_min(Corr(x_T)) ≥ ψ for a constant ψ > 0
and every set T of at most (2A + 3)s + 2 predictors." Optionally, B3 needs this only for the anchored sets S₀ ∪ J,
|J| ≤ j₀; the all-sets form is a convenient sufficient condition.

### P1-02 — MAJOR — `TARGET.md` §6, row (A3): "Under second moments one gets the same display with 'probability → 1' in place of n^{−cM}"
This is not established, and the master route cannot deliver it.

**Counterexample (finite second moments, (A4) holds even with a fixed floor).**
- Let W ~ N(0, 1), and let ξ be independent of W with P(ξ = 0) = 1 − 1/n and P(ξ = ±a) = 1/(2n), where a² = nτ² and
  τ² > 0 is fixed.
- Put x₁ := W + ξ/2 and x₂ := W − ξ/2. Then Var(x_j) = 1 + τ²/4 and λ_min(Corr(x₁, x₂)) = (τ²/2)/(1 + τ²/4), a fixed
  positive floor. Let all other coordinates be independent N(0, 1). E ξ⁴ = nτ⁴ → ∞, so there is no L⁴–L² equivalence.
- With probability (1 − 1/n)ⁿ → e^{−1}, every ξ_i = 0. The two sample columns are then identical after standardisation,
  G_{{1,2}} is singular, and (ND) fails.

So P*((ND)ᶜ) ≥ e^{−1} − o(1), and the remainder of (1.1) does not vanish. On this event the size clause of (1.1) is false
(duplicates; S-FIT). Whether the distance clause still holds there is stated as OPEN in STATEMENT S-FIT. Even the
slower second sentence (DIST-2) needs more than second moments:
- (E) holding with probability → 1 at a fixed M needs a weak law of large numbers for (β*ᵀz)², i.e. uniform
  integrability, along a triangular array.
- 𝒟_n can fail with probability bounded away from 0 if columns carry atoms of this kind.

**Minimal repair.** Delete the sentence. Or replace it with: "Under a small-ball (or L⁴–L²) condition on sparse
directions and uniform integrability, the master route should give the display with probability → 1 (not proved). With
second moments alone, the design event (ND) can fail with probability bounded away from 0 (exact sample duplicates)."
Also "three sample events" should read four: 𝒟_n, (E), (C), (ND).

### P1-03 — MAJOR (readability / quantifiers; not a falsity) — Theorem A (and Corollary C), "(A3), (A4) … q_n := ⌈C_q·M·log n⌉, with M the constant in the conclusion"
**Problem.** The hypotheses (A3) and (A4) are stated before M is quantified, but their size parameter q_n depends on M.
Two readings follow:
- **(i) Per M.** For each M ∈ [M₀, √n], if (A3) and (A4) hold at q_n(M), the display holds at M. This is the faithful
  reading.
- **(ii) Uniform.** The assumptions hold for every M ≤ √n, i.e. on sets of size ≈ C_q √n log n. This is a much stronger
  hypothesis: still true, but a weaker theorem.

In addition, the smallest admissible size, C_q M₀ log n, involves M₀, an **unspecified** constant that itself depends on
c_ψ, the constant of (A4). So the reader cannot know for which set sizes to check (A4).

Under reading (i) the theorem is faithful: see Q2 and Q4 below.

**Minimal repair.** State the quantifier explicitly: "There are c > 0, M₀ ≥ 1, n₀ depending only on (s, A, K, c_ψ, b̄)
such that for every n ≥ n₀ and every M ∈ [M₀, √n]: if (A1)–(A5) hold with q_n := ⌈C_q M log n⌉, then …". Add one line saying
that the assumptions are needed only on sets of size of order log n at the best rate.

### P1-04 — MINOR — B2, "([P2] A0, re-derived: one-column determinant ratio ((n+1)γ + 1)/(γ + 1) with Schur complement γ ≥ g₀)"
**Problem.** The one-column ratio D_{S∪{u}}/D_S is **not** ((n+1)γ + 1)/(γ + 1), and it is not even bounded below by it.

**Exact form.** Write G′ = [[G, b], [bᵀ, g]] and f(c) := c·g + 1 − c²bᵀ(cG + I)⁻¹b. Then the ratio is f(n + 1)/f(1), which
depends on b, not only on γ = g − bᵀG⁻¹b.

**Counterexample.** Two standardised columns with sample correlation ρ = 0.9 and n = 100:
- ratio = 92.258;
- the stated formula gives 95.952;
- the correct floor bound gives ((n+1)λ_min + 1)/(λ_min + 1) = 91.826, with λ_min = 9.9.

Random search (20 000 standardised designs, n ∈ [5, 400], |S| ≤ 5): the stated formula fails as a lower bound in 19 796
cases. The floor bound never fails.

**The conclusion of B2 is true.** Write φ(λ) := ((n+1)λ + 1)/(λ + 1), which is increasing, and use Cauchy interlacing
(μ₁ ≤ λ₁ ≤ μ₂ ≤ … ≤ λ_k ≤ μ_{k+1}):
  D_{S∪{u}}/D_S = φ(μ₁)·Π_i φ(μ_{i+1})/φ(λ_i) ≥ φ(λ_min(G_{S∪{u}})) ≥ φ(g₀) ≥ (n+1)g₀/(1 + g₀).
Iterating over the columns of J, each intermediate set of size ≤ q has floor ≥ g₀, which gives (DG; g₀/(1 + g₀)). This is
[P1] `lem:spec`(e) as cited by [P2] A0(i). (A Schur-only route needs γ ≥ g₀(1 + ‖G⁻¹b‖²), which does follow from the floor,
but even then it gives only g₀/(2 + g₀).)

**Minimal repair.** Replace the parenthetical with the interlacing line above.

### P1-05 — MINOR — B0, "the image of Π(· | x, y^r) … has the law it has in the unit-noise model …, and d_H(f, f*) is unchanged by this map applied to both arguments"
**Problem 1: a statement about the law is not enough.** Π(d_H(f, f*) > r | D_n) depends not only on the posterior of
(S, θ, v), but also on:
- the data, through the plug-in intercept â = ȳ^r − x̄ᵀb;
- (α*, σ*), through f*.

A statement about the law of the image of Π alone (R′(b), under GR^c, which allows an arbitrary random intercept) does
not fix the joint law of (image of Π, ȳ^r, x̄).

**Problem 2: the invariance wording.** The map (S, θ, v) ↦ (S, θ/σ*, v/σ*²) does not act on f*. "Applied to both
arguments" is not meaningful as written.

**The pathwise version works and makes the fixed-design → random-design failure point in ROUTES §2b moot.**
- Put ỹ := (y^r − α*)/σ* = xβ*/σ* + ε/σ*, with ε/σ* ~ N(0, I) independent of x.
- By R′(a′) with a = −α*/σ* and c = 1/σ* > 0 (deterministic, for every x), Π(· | x, ỹ) is the image of Π(· | x, y^r).
- The mapped draw has b̃ = b/σ* and ã = ȳ̃ − x̄ᵀb̃ = (â − α*)/σ*.
- Hellinger distance is invariant under the affine map y ↦ (y − α*)/σ*. Hence, pointwise in x,
  H²(N(â + xᵀb, v), N(α* + xᵀβ*, σ*²)) = H²(N(ã + xᵀb̃, v/σ*²), N(xᵀβ*/σ*, 1)).
  So d_H(f_{S,θ,v}[x, y^r], f*) = d_H(f_{S,θ/σ*,v/σ*²}[x, ỹ], f̃*), where f̃* has (α, β, σ) = (0, β*/σ*, 1).

Because the reduction is pathwise and per n, σ* and α* may depend on n. "σ* > 0 arbitrary, not fixed" is justified,
provided (A5) is in units of σ*. It is, so the constants (M, M′) = (2s²b̄², 2sb̄²) are free of σ*. W3-POST's δ_n is a
functional of π on Ω, which is invariant by R′(a); that settles B3's "fixed σ*²".

**Minimal repair.** State B0 in this pathwise form, citing R′(a′) (and R′(a) for model-space functionals). R′(b) is not
needed.

### P1-06 — MINOR — Setup (reader)
**(a) The symbol σ² is used for two scales.** The IG(0.01, 0.01) prior and the slab covariance n·σ²(G_S + I)⁻¹ are on the
**standardised** response scale. The posterior "of (S, β, σ²) (coefficients on the original scale)" and the density
y | x ~ N(intercept + xᵀβ, σ²) need the original-scale variance v = s_y²σ². Repair: "coefficients and noise variance
mapped back to the original scale".

**(b) Π is undefined when a column is constant in the sample.** Standardising a constant column divides by zero; the
code drops such columns. The event is in the remainder (Remark 4), but the Setup should say "constant sample columns are
dropped, as in the code".

**(c) The intercept wording.** "The intercept is estimated by the sample means" can be read as a fixed point estimate.
It is ȳ − x̄ᵀβ for each draw β.

### P1-07 — MINOR — B2-core, condition "q·log(ep/q) + log n ≤ c₂n/K⁴"
**Problem.** For q ≥ ep the term q log(ep/q) is ≤ 0, so the condition reduces to log n ≤ c₂n/K⁴. The conclusion then
covers all u ∈ ℝ^p, and it can fail.

**Counterexample.** p = n, q = 3n, z_i i.i.d. N(0, I_p). The centred Σ̂^z has rank ≤ n − 1 < p, so some u has
uᵀΣ̂^z u = 0 < ½‖u‖² = ½uᵀCorr(x)u.

**The application is unaffected.** q_n ≤ C_q√n log n + 1. If p < q_n, the dimension p + 1 ≤ q_n + 1 is still much smaller
than n/K⁴.

**Minimal repair.** Use q ∧ p in place of q in the condition (union over supports of size q ∧ p, net dimension
(q ∧ p) + 1). Rest of B2-core: see Q2. It is true as stated otherwise, including the intercept and degenerate directions.

### P1-08 — MINOR — `TARGET.md` §6, row (A5): "the master theorem needs only ‖coefficients‖² ≤ const·n in standardised units"
**Problem.** The master needs two things: (E) ‖μ‖² ≤ nM, and (C) ‖θ*‖² ≤ nM′ (or (L₀)). The coefficient bound alone gives
only ‖μ‖² ≤ λ_max(G_{S₀})‖θ*‖² ≤ s(n − 1)·nM′, which is not of order n.

**Repair.** "The master theorem needs only the two sample conditions ‖μ‖² ≤ const·n·σ*² and ‖θ*‖² ≤ const·n·σ*²."

### P1-09 — MINOR — Corollary C, "If the list contains the true model and the posterior probability of the true model exceeds ½, then π(𝒯) > ½."
**Problem.** As written this is just π(𝒯) ≥ π(S₀), so it says nothing. The content of DIST-C (C-ii)(α) is lost: if S₀ is
**offered** to the final-run ledger and δ_n < ½, then S₀ is **retained** in 𝒯, by the store order.

**Repair.** "If the final stage of the run proposes the true model at least once and the true model has posterior
probability above ½, the list keeps it; hence π(𝒯) > ½."

### NITs
- **P1-10 (Remark 3).** t = M log n ≤ √n log n lies inside t ≤ n^{0.6} only once log n ≤ n^{0.1}, i.e. for n ≳ e^{36}.
  That is a valid n₀ but an absurd one; the 1/C² factor in t helps only marginally. With any κ₀ < ½, e.g. κ₀ = 1/4 (log n ≤
  n^{1/4} for n ≳ 5.5·10³), or with the range M ≤ √n/log n, the statement is the same with a realistic n₀. Remark 1's
  upper end ε_n² ≤ n^{−1/2} log n has the same caveat.
- **P1-11 (B1).** ŝ_j²/Var(x_j) = (n/(n−1))(n⁻¹Σz_ij² − z̄_j²) ≤ (n/(n−1))·(5/4) ≤ 2 needs n ≥ 3. Covered by n₀; state it.
- **P1-12 (Corollary C).**
  - "Completed run" is not defined in the reader text.
  - "Exact … weights" means real arithmetic (EX-A); say so in one clause.
  - "With probability" is P* over the data. The run-uniform form is correct; say it.
  - The scope is the final SMC run, with the exact-enumeration branch excluded. The reader text says only "the sampler".
- **P1-13 (Theorem A).**
  - The constants are uniform over laws, so triangular arrays (the law of x, β*, σ* and α* depending on n) are covered.
    Say so.
  - "Of order √((1+s) log p/n)" hides the dependence of M₀ on (b̄, K, c_ψ). Through M = 2s²b̄², M₀ may grow faster than
    1 + s if DIST-1(c) is read with M fixed.
- **P1-14 (B1′).** A uniform ψ₂ bound on β*_j(x_j − Ex_j)/σ* implies (A5), with b̄ of the order of that ψ₂ constant, so B1′ is
  not an alternative to (A5). As worded it also states no conclusion or constants. It is off the critical path.
- **P1-15 (`TARGET.md` §6 preface).** It says the reader versions "have had an Opus same-family pre-check only
  (`reviews/P1_disposition.md`)". This anticipates this report and its disposition.
- **P1-16 (Theorem B).** The reader text does not mention its conditionality on W3-POST:Thm-1. The status is "SF VERIFIED;
  XF VERIFIED", so this is acceptable, but §1R's preface is the only place it appears.

## Answers to the brief's questions (checks that passed are recorded with the computation)

**Q1 (B1). Holds as stated.**
- **Constant K.** With u = e_j, (A3) gives E exp(λz_j) ≤ exp(K²λ²/2). Expanding at λ → 0 forces K ≥ 1. So ‖z_j‖_{ψ₂} ≲ K
  and ‖z_j²‖_{ψ₁} ≲ K².
- **Variances.** Bernstein gives P(|n⁻¹Σz_ij² − 1| > ¼) ≤ 2exp(−cn·min(1/K⁴, 1/K²)) = 2exp(−cn/K⁴). Hoeffding gives
  P(|z̄_j| > ¼) ≤ 2exp(−n/(32K²)). Hence ŝ_j²/Var(x_j) = (n/(n−1))(n⁻¹Σz² − z̄²) ∈ [(n/(n−1))·(11/16), (n/(n−1))·(5/4)] ⊂ [½, 2]
  for n ≥ 3, with probability ≥ 1 − 4p·exp(−c₁n/K⁴), c₁ absolute.
- **No dropped column.** No ŝ_j vanishes, so p_ret = p ≥ 2 and s₀ = |supp β*|.
- **Triangle step.** ‖μ‖ = ‖Σ_j β*_j Cx_j‖ ≤ Σ_j |β*_j| ŝ_j √(n−1) ≤ √2 √(n−1) Σ_j |β*_j| sd(x_j) ≤ √2 √(n−1) s b̄ σ*, so
  ‖μ‖² ≤ 2s²b̄²σ*²n.
- **Coefficients.** ‖θ*‖² = Σ ŝ_j²β*_j² ≤ 2sb̄²σ*². This is much stronger than (C; 2sb̄²).
- **Counterexample search.** Atoms (Rademacher, any bounded law with fixed K) and K = 1 (strictly sub-Gaussian laws) do not
  break B1. Laws with K → ∞ (e.g. Bernoulli(q_n), q_n → 0) are excluded because K is fixed.
- **DIST-2 note.** It is correct: the true coordinates plus two others give (E), (C) and 𝒟_n.

**Q2 (B2-core, B2).**
- **B2-core is true** (apart from P1-07).
  - For a support T with |T| = q, take w = (1, z_T) with E wwᵀ = diag(1, Corr(x_T)).
  - ψ₂–L₂ form: ‖a + uᵀz‖_{ψ₂} ≲ |a| + K·sd(uᵀz) ≲ K√2·(a² + Var(uᵀz))^{1/2}.
  - Whiten on the range of E wwᵀ. Degenerate directions are harmless: Var(uᵀz) = 0 together with (A3) forces uᵀz = 0
    almost surely, so the sample lies in the range too, and the claim reduces to a² ≥ a²/2.
  - In whitened coordinates, a two-sided Bernstein + ε-net bound on S^q (9^{q+1} points) and a union over C(p, q)
    supports give ‖Σ̂′ − I‖ ≤ ½ with failure probability ≤ exp(q log(ep/q) + (q+1) log 9 − cn/K⁴) ≤ exp(−c₂n/K⁴) for
    c₂ small. The term "+ log n" is not needed but is harmless.
  - The centred statement follows from min_a n⁻¹Σ(a + uᵀz_i)² = uᵀΣ̂^z u (1/n normalisation; the (n − 1)-normalised
    version is larger).
- **The chain λ_min(G_T) ≥ c_ψ/8 is correct.** G_T = (n−1)R̂_T, and R̂_T = D̂⁻¹S^z_T D̂⁻¹ with D̂_jj² = ŝ_j²/Var(x_j) ≤ 2. So
  λ_min(R̂_T) ≥ λ_min(S^z_T)/2 ≥ ½·½·c_ψ/n, and (n − 1)c_ψ/(4n) ≥ c_ψ/8 for n ≥ 2. This is (F_w; c_ψ/8) on all sets of
  size ≤ q.
- **From the floor to (DG) and (ND).** The floor gives (DG; c_D) and (ND; c_D, m), c_D = g₀/(1 + g₀), for m ≤ q − s. This
  holds via interlacing, not via the stated formula (P1-04).
- **q_n ≥ m_n(M log n) + s for M ≥ 1 and n ≥ n₀(s, A), uniformly in M.** m_n(t) + s ≤ 2s + 1 + [s(A log n + log 2) +
  ((s+2)/2)(log n + log 2) + 3M log n]/log 2. The log n part is (sA + s/2 + 1 + 3M) log n/log 2. Against
  C_q M log n = (2sAM + 4sM + 8M) log n/log 2, the excess at M = 1 is (sA + 3.5s + 4) log n/log 2, and it increases in M.
  It absorbs the O(s) constant terms once log n ≳ 1. In Theorem A, (1.1) is applied at t = M log n/C² with C ≥ 1, and
  m_n is increasing in t, so q_n(M) also covers m_n(t) + s.
- **The B2-core requirement holds for all M ≤ √n.** q_n ≤ C_q√n log n + 1 and log(ep/q_n) ≤ 1 + A log n, so
  q log(ep/q) ≲ C_q A √n (log n)² ≤ c₂n/K⁴ for n ≥ n₀(s, A, K).

**Q3 (B0).** See P1-05. The distributional wording is insufficient; the pathwise reduction via R′(a′) works, d_H is
invariant under it, and "σ* arbitrary, not fixed" is justified with (A5) in units of σ*.

**Q4 (Theorem A display). Correct after renaming, with one n₀.**
- **Renaming.** Take t := M log n/C², so that C√(t/n) = √(M log n/n) and e^{−ct} = n^{−(c/C²)M}. Pick c̃ < c/C².
  - Inner threshold: {Π > n^{−c̃M}} ⊆ {Π > e^{−ct}}.
  - Noise term: 3n^{−(c/C²)M} ≤ ½n^{−c̃M} once n^{(c/C² − c̃)M₀} ≥ 6. This is one n₀, since M ≥ M₀.
  - Design term: 5p·e^{−c′n/K⁴} ≤ 5n^A e^{−c′n/K⁴} ≤ ½n^{−c̃√n} ≤ ½n^{−c̃M} for n ≥ n₀(A, K, c̃).
- **Lower end.** It needs M ≥ C²M₀^{(1.1)} (and M ≥ 1 for Q2). Upper end: see P1-10.
- **"Depending only on (s, A, K, c_ψ, b̄)" is right.** After B0, σ* = 1. The remaining inputs are M = 2s²b̄², M′ = 2sb̄²,
  c_D = (c_ψ/8)/(1 + c_ψ/8) and κ₀ = 0.4; K enters through the bridge failure probabilities and n₀. The intercept α*
  enters nothing.
- **Second sentence.** (1.2) at the same t gives radius √(M log n·ℓ_n/n) with only B0 and B1. Its constants do not
  involve c_ψ.
- The size clause of (1.1) is dropped, which only weakens the statement.

**Q5 (Theorem B, B3).** With P1-01's repair, every input checks:
- **(F_λ).** Sets S₀ ∪ J with |J| ≤ j₀ = ⌈(2A+1)s⌉ + 1 have size ≤ (2A + 2)s + 2 ≤ (2A + 3)s + 2, which is covered. φ₀² = ψ/4
  follows from λ_min(R̂_T) ≥ (ψ/2)/2, and ψ ≤ 1 holds automatically (unit diagonal).
- **(F_w).** m♯_n + s ≤ 2s + 1 + (sA + s/2 + 1) log n/log 2 ≤ ⌈C_q log n⌉ for large n. This uses W3-POST's bound on m♯_n,
  valid for s₀ ≥ 1.
- **BM-∞.** θ*_j²/σ*² = ŝ_j²β*_j²/σ*² ≥ b_n²/2, so the deterministic envelope b_n²nφ₀²/(2 log n) → ∞.
- **Item 6.** On the B1 event, |supp θ*| = s, matching "exactly s ≥ 1" and item 6's "|supp θ*| = s₀ on 𝒜_n". Fixed σ*² is
  handled by R′(a) (δ_n is invariant). The constants are common, and P(𝒜_nᶜ) ≤ 5p·e^{−cn/K⁴} → 0.
- **(TR₀; 2).** a + uᵀx = a′ + u′ᵀz with u′ supported on supp β*, and B2-core gives E(a′ + u′ᵀz)² ≤ 2n⁻¹Σ(a′ + u′ᵀz_i)².
- **(L₀)** follows from (E) and (C).
- **DIST-3.** With u_n := min(M_n²/C², n^{1−κ₀}) → ∞ and δ_n = O_P(r_n), integrating over the design gives the display.

**Q6 (Corollary C). Correct.**
- Let G_n := {Π(B | D_n) ≤ n^{−cM}} be the data event of Theorem A, with P* ≥ 1 − n^{−cM}.
- On G_n, (C-0) with L_n = 1/π(𝒯) gives, deterministically and for **every** run, Π̂(B) ≤ n^{−cM}/π(𝒯) ≤ n^{−cM/2}
  whenever π(𝒯) ≥ n^{−cM/2}.
- This is uniform over stream realisations, so the data/run distinction is handled correctly. It is stronger than
  (C-i), which is stated per P⊗.
- The description "at most 40p + 1 models with exact unnormalised weights, no parameter draws" matches the code facts:
  p = p_ret ≤ p, the scores are F(S) = log ϖ(S) + log m(S), equal up to the constant W_K, and Π̂ = Π̂^𝒯.
- Caveats: P1-09 and P1-12.

**Q7 (readability, honesty).**
- (A1)–(A5) contain what the bridges use: p ≥ 2, positive and finite variances, at most s for Theorem A, exactly s for
  Theorem B, n ≥ n₀.
- (A4) at c_ψ/n is non-standard but weaker than the standard condition, and it is explained.
- The defects are P1-01, P1-03 and P1-06.
- `TARGET.md` §6 overclaims in the (A3) row (P1-02) and is inaccurate in the (A5) row (P1-08). The (A4), (A6) and σ* rows
  are accurate. "Invariant" in the σ* row is really equivariance of the parameter posterior plus invariance of d_H; this
  is acceptable.

**Overall verdict: REPAIRABLE.** No reader clause is false under its faithful reading. Wording repairs are needed before the
cross-family check: P1-01 (Theorem B hypothesis), P1-02 (TARGET overclaim) and P1-03 (Theorem A quantifier). P1-04 and
P1-05 (bridge derivations B2, B0) and P1-07 (B2-core domain) are one-line fixes.
