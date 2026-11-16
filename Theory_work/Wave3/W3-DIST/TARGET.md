# W3-DIST — TARGET (PROTOCOL_v4 §3.2 evidence file for the `lit:`, `necessity:`, `better:` gates; 2026-11-15)

Everything is at candidate level: "matches / beats / short" compares the **candidate statement** (STATEMENT v1.1) with
Song & Liang (2015), assuming the candidate is proved. Nothing here is proved.

## 1. Assumption map (summary; full table `ASSUMPTION_MAP.md` §1–2)
| hypothesis | enters | necessity reading |
|---|---|---|
| Gaussian noise independent of the design | conjugacy, χ² tails | as in [SL] model (1); not a target to weaken |
| i.i.d. rows | Lemma T only | needed for a population distance |
| **no** condition on ν_x in the transfer | Lemma T | strong form; N2, N6 show no degradation with infinite 4th moments |
| strict sparsity, s₀^r fixed | constant M₀ ∝ (1 + s₀^r)(A + 1); Lemma S | approximate sparsity = stretch S-APX |
| p_raw ≤ n^A | constants | proof device; S-EXP stretch |
| 𝒟_n = {p_ret ≥ 2} | remainder | proof device |
| (E; M) energy | s_y bracket, X3, S | some bound on signal energy is needed with the s_y-scaled prior |
| (C; M′) / (L₀; B) coefficient cost | X3, S through L_{S₀} | very weak; replaces the floor on S₀ |
| **(ND)** average determinant growth | X4 only | **not needed for consistency** (DIST-2); needed by this proof for the sharp rate and the full exponent; absent from [SL]; `improvable` (N4; S-FIT open) |
| (TR₀) second moments on supp β* | DIST-3 only | needed by this route at scale 1/n |
| beta-min, identifiability ([SL] Condition 3) | **not assumed** | — |

## 2. Parity table (A1 checklist + PROGRAM goals + our best registered result)
Our best registered result for comparison: W3-POST2:D — fixed design, in-sample average Hellinger, in probability,
D(a) M_n/√n given δ_n → 0, D(b) log n/n under (E), (F₀), (OS) (HQ note: D(b) repaired after council; diff round in progress).
| item | Song–Liang | candidate | vs [SL] | vs PROGRAM goals | vs W3-POST2:D |
|---|---|---|---|---|---|
| **P1 metric** | Hellinger between joint (x, y) densities, x-marginal integrated (d² = 2d_H²) | the same distance, d_H (DIST-1/2/3); sample → population by Lemma H + Lemma T | **matches**; the transfer step needs no condition on the predictor law, where [SL] need bounded predictors or Condition 1/2 | design-agnostic ✓ | **beats** (out-of-sample, random design) |
| **P2 mode (15)** | P*[π(d > ε_n) > e^{−c₁nε_n²}] < e^{−c₁nε_n²} under Condition 1 | DIST-1 (1.1): the same display with remainder P*(interfaces fail); for all ε_n² ∈ [C²M₀ log n/n, C²n^{−κ₀}] | **matches in form**, under (ND). Tail condition: only the probability of (E), (C), (ND); in the reader form (§6), sub-Gaussian predictors and bounded signal (bridges B1, B2). **Short** in two respects: needs (ND), which [SL] do not; sequences with ε_n² > n^{−κ₀} get exponent c n^{1−κ₀} only | ✓ | **beats** (exponential vs in probability) |
| **P2 mode (16)** | lim P*[π(d > ε_n) > e^{−c₁nε_n²}] = 0 under second moments (Condition 2) | DIST-1(b) when P*(interfaces fail) → 0; (E), (C) need only second moments of the true signal coordinates | **matches** given (ND) w.p. → 1; **beats** on the moment condition for the transfer. No primitive second-moment condition for (ND) is claimed (an atom of mass 1 − 1/n makes two sample columns identical with probability ≈ e⁻¹: P1-02) | ✓ | **beats** |
| P2 without (ND) | — ([SL] need no design geometry) | DIST-2 (1.2): exponential form with exponent c nε_n²/ℓ_n | **short**: exponent reduced by ℓ_n. Reason: the coded size prior is ≈ geometric(½), [SL] hard-cap the size at r̄_n; closing it = stretch S-FIT (kill budget: 1 attempt + 1 break review) | ✓ no geometric condition | new |
| **P3 rate** | Thm 2 at polynomial p: any ε_n with r_n → ∞, r̄_n ≥ r_n, r̄_n log n = o(nε_n²) — i.e. ε_n² = ω_n log n/n with ω_n → ∞ tied to the prior's cap; Cor 1 as printed (fixed α ∈ (0, 1)): ε_n² = n^{−(1−α)} log^k n | DIST-1: ε_n² ≍ (1 + s₀^r)(A + 1) log n/n ≍ (1 + s₀) log p/n, no diverging factor, no tuning; DIST-3: √(u/n) oracle/parametric given selection; DIST-2: (1 + s₀^r) log n·ℓ_n/n | DIST-1 **beats** both (constant × log n/n; and beats Cor 1's printed rate for every fixed α). DIST-3 **beats** (parametric; [SL] have none). DIST-2 **beats Cor 1 as printed** but is **short** of Thm 2's best (ω_n log n/n, any ω_n → ∞) by the factor log n/ω_n | p ≫ n ✓ | **beats** D(b) in generality ((OS) → (ND) is stronger, but no (F₀)); equal rate |
| **P4 sparsity** | Thm 2: strict (4). Thm 1: approximate (3) with bounded predictors | strict, s₀^r fixed | **matches** Thm 2; **short** of Thm 1 (approximate sparsity) → stretch S-APX (kill budget: 1 attempt after CP2) | ✓ | equal |
| **P5 prior** | a family of priors: Bernoulli(r_n/P_n) with r_n → ∞, hard cap r̄_n tied to ε_n, V_ξ with envelopes (9)–(14) | the prior **as coded**, no tuning: BB(1, p) capped at K = min(p, ⌊n/2⌋), data-dependent slab and IG rate | **matches the checklist** (coded prior, no tuning). [SL]'s own conditions (9), (10), (11) and "r_n ≻ 1" **fail** for it (cap ⌊n/2⌋; mean size O(1)); their sieve route is incompatible with a geometric size prior when log p → ∞ (H1 §2, unchecked; S1-04 agrees on (9)–(11)). Route that works: conditional on the design, closed-form marginal likelihoods, Occam factor | method as coded ✓ | equal |
| **P6 coded output** | none (exact posterior only) | DIST-C: deterministic domination transfer to any output-defined law Q ≤ L_nπ; store BMA and HPM/MPM plug-ins; delivery premises explicit | **beats** (beyond [SL]); conditional on discovery / P-STORE / P-HIT; **the run returns no distribution**, so P6 is about distributions reconstructed from the returned store/HPM/MPM | method as coded ✓ (jointly with output) | new (extends C-PACK SL2 from PIPs to the joint parameter law) |
| **Scope** | P_n ≻ n^θ, P_n < exp(Cn^α) | 2 ≤ p_ret ≤ p_raw ≤ n^A, p ≫ n | **short** on exponential p → stretch S-EXP (by-product if Lemma X tracks ℓ_n); no lower growth bound needed (**beats** on small p) | ✓ | equal |
| **Design-agnostic** | tail conditions on x only; no eigenvalue/identifiability condition in Thm 1–2 | sample-level interfaces (E), (C), (ND); no identifiability, no beta-min | **short** by (ND) in DIST-1; **matches** in DIST-2 | ✓ (no family in any statement) | — |

## 3. Boundary numerics (summary; `ASSUMPTION_MAP.md` §3, `work/numerics/RESULTS.md`)
Exact enumeration at p = 12, n = 50…800, 40 replications per cell; p ≫ n on a restricted family. Nothing contradicts a
candidate statement. Outside each assumption: heavy tails (t₂.₅, Pareto 2.1, spikes) — no degradation, transfer ratio
≤ 1.004; (ND) violated by near-duplicates — selection fails, Hellinger numbers unchanged (flag `improvable`); weak
signals — log n-type growth only. Limits (S1-10): averaged, not nested, tails; the scale τ² ≍ log n/n² is untested.

## 4. Better-theorem review (S1; its brief asked for a strictly better statement)
BT1 (drop (F₀) in DIST-3) — adopted. BT2 (oracle exponential bound with additive δ_n) — adopted. BT3
(reference-adaptive size lemma, no p ≤ n^A) — adopted. BT4 (domination transfer for any output law) — adopted.
Details and evidence: `reviews/S1_disposition.md`. S1 also attacked the comparison rows (S1-04); the table above is
the corrected one.

## 5. Target clauses (proposed for HQ to fix at CP1; a WEAKER change to any of them is an early checkpoint)
- **TC1 (metric).** d_H between the joint (x, y) laws f_{S,θ,v} and f*, x-marginal ν_x integrated; rows i.i.d.; ν_x arbitrary.
- **TC2 (DIST-1, conclusion).** Display (1.1): inner threshold e^{−ct}, outer bound 3e^{−ct} + P*(interfaces fail), radius
  C√(t/n), for all t ∈ [M₀ log n, n^{1−κ₀}].
- **TC3 (DIST-1, rate).** Best radius ε_n² = C²M₀ log n/n with M₀ = O((1 + s₀^r)(A + 1)).
- **TC4 (DIST-1, hypotheses).** (RD) — Gaussian noise independent of the design, strict sparsity, p_raw ≤ n^A — and the
  interfaces 𝒟_n, (E; M), (C; M′), (ND; c_D, m_n(t)). No beta-min, no identifiability, no condition on ν_x beyond the
  probability of the interfaces.
- **TC5 (prior).** The coded prior, unchanged and untuned.
- **TC6 (DIST-2).** Display (1.2), radius C√(tℓ_n/n), hypotheses (RD), 𝒟_n, (E), (C).
- **TC7 (DIST-3).** The oracle display Π(d_H > C√(u/n) | D_n) ≤ δ_n + Ce^{−cu} under (E), (L₀), (TR₀), 1 ≤ u ≤ n^{1−κ₀}.
- **TC8 (DIST-C).** (C-0) and the deterministic parts of (C-i), (C-iii); every delivery statement jointly with
  {completed} and under its named premise.
Not target clauses: bridges B1, B2; the stretch statements S-APX, S-EXP, S-FIT; the internal form of Lemmas T, S, V, X,
X′ (their changes are tracked in DEPS and the changelog).

## 6. Reader versions (PROGRAM "Readability"; PROTOCOL_v4 H6; HQ steers A5 and the settled note) — proposed main-text wording
The text between the rules is identical to STATEMENT.md §1R (the checked object is there). Its form is the lead's
choice: a complete setup, numbered assumptions in standard terms, two displays with the rate explicit, a plain-words
paragraph, the statement without (A4), an example, and a notation table; no internal ids. Master versions: (1.1),
(1.2), DIST-3, DIST-C; bridges B0–B3 in STATEMENT.md §3. Candidates. Review record: `DEPS.tsv`.

---
**Setup.** We observe D_n = {(x_i, y_i) : i = 1, …, n}: n independent copies of a pair (x, y), where x ∈ ℝ^p is a
vector of p predictors and y is a real response. The number of predictors p may grow with n and may be much larger
than n; the law of (x, y) may change with n.

*What the method does.* (1) It removes the predictors that are constant in the sample, and centres and scales every
other predictor, and the response, by its sample mean and sample standard deviation. Let r be the number of predictors
that remain (r ≤ p). (2) On the standardised data it uses one fixed prior, with no tuning parameter: the number of
included predictors has the beta-binomial BB(1, r) distribution restricted to at most min(r, ⌊n/2⌋), and given that
number all sets S of that size are equally likely; given S and the noise variance, the coefficients of the predictors
in S are jointly normal with mean zero and covariance n × (noise variance) × (G_S + I)⁻¹, where G_S is the sample Gram
matrix of the standardised predictors in S and I is the identity matrix of the same size; the noise variance has an
inverse-gamma prior with shape 0.01 and rate 0.01. (3) The posterior is mapped back to the original units.
Π(· | D_n) denotes the resulting posterior distribution of (S, β, σ²): S is the set of included predictors, β ∈ ℝ^p the
coefficient vector in the original units (zero outside S and for removed predictors), and σ² the noise variance in the
original units. If fewer than two predictors remain, or the response is constant in the sample, the posterior is not
defined here; under the assumptions below such data sets have probability smaller than the exceptional probabilities
in the theorems and are counted in them (in particular r = p outside them).

*The distribution attached to a posterior draw.* A draw (S, β, σ²) defines a joint density f for a new pair (x, y): x
has its true distribution and, given x, y is normal with mean ȳ + (x − x̄)ᵀβ and variance σ², where ȳ and x̄ are the
sample means of the response and of the predictors. f* is the true joint density of (x, y).

*Notation.* d_H(f, g) = (1 − ∫√(fg))^{1/2} is the Hellinger distance between two densities. P* is the distribution of the
data D_n. sd(·), Var(·) and Corr(·) are population standard deviations, variances and correlation matrices.
z_j = (x_j − E x_j)/sd(x_j) is the j-th standardised predictor and z = (z_1, …, z_p). For a set T of predictors, x_T is
the sub-vector of x. λ_min(·) is the smallest eigenvalue of a symmetric matrix. |S| is the number of predictors in S.
log is the natural logarithm.

**Constants, the level M and the window q_n.** s ≥ 0 is an integer and A ≥ 1, K ≥ 1, c_ψ > 0, b̄ > 0 are constants; none
depends on n. Fix a number M ≥ 1, the *level*: a larger M gives a larger ball and a smaller exceptional probability.
The *window* is

    q_n = min{ p, ⌈C_q·M·log n⌉ },   where C_q = 2(s(A + 2) + 4)/log 2.

It is the largest number of predictors that assumptions (A3) and (A4) constrain jointly; for a fixed level M it is of
order log n. (K below is the constant of (A3); the cap on the model size is always written min(r, ⌊n/2⌋).)

**Assumptions.**
- **(A1) Gaussian linear model.** y = α* + xᵀβ* + ε, where ε is normal with mean 0 and variance σ*² > 0 and is independent
  of x. (α*, β*, σ* and the law of x may depend on n.)
- **(A2) Sparsity and dimension.** At most s coordinates of β* are nonzero, and 2 ≤ p ≤ n^A.
- **(A3) Sub-Gaussian predictors.** Every predictor has positive variance, and for every vector u ∈ ℝ^p with at most q_n
  nonzero entries and every real λ:   E exp(λ·uᵀz) ≤ exp(K²λ²·Var(uᵀz)/2).
- **(A4) No near-exact collinearity.** For every set T of at most q_n predictors:   λ_min(Corr(x_T)) ≥ c_ψ/n.
- **(A5) Bounded signal.** |β*_j|·sd(x_j) ≤ b̄·σ* for every j.
No lower bound on the nonzero coefficients is assumed (no beta-min condition), and no fixed lower bound on
eigenvalues: under (A4) predictors may be correlated up to 1 − c_ψ/n. ((A4) still makes sparse coefficient vectors
distinguishable in principle; the statement without (A4) below needs no such condition.)

**Theorem A (the posterior recovers the joint distribution of predictors and response).** There are constants c > 0,
C₁, M₀ and n₀, depending only on (s, A, K, c_ψ, b̄), such that the following holds whenever n ≥ n₀, M₀ ≤ M ≤ √n/log n and
(A1)–(A5) hold with the window q_n of this M:

    (i)   P*[ Π( d_H(f, f*) > √(M·log n / n) | D_n ) > n^{−cM} ] ≤ n^{−cM},

    (ii)  P*[ Π( |S| > s + C₁·M | D_n ) > n^{−cM} ] ≤ n^{−cM}.

In words. (i) Except on a set of data sets of probability at most n^{−cM}, the posterior gives probability at most
n^{−cM} to joint distributions farther than √(M log n/n) from the truth in Hellinger distance: the posterior contracts
at the rate √(log n/n). (ii) On the same data sets the posterior gives probability at most n^{−cM} to models with more
than s + C₁M predictors. Statement (ii) bounds the number of selected predictors; it does not say that they are the
true ones. The two exceptional sets of data sets can be taken to be the same set. The bounds are uniform over all laws
of the data that satisfy (A1)–(A5) with the given constants.

*Without (A4).* If (A4) is dropped, and (A3) is required only for single predictors (vectors u with one nonzero
entry), then (i) holds with the radius √(M·log n·log(p ∨ n)/n), which is larger by the factor √(log(p ∨ n)), and (ii) holds
with s + C₁·M·log n in place of s + C₁·M. (Here p ∨ n is the larger of p and n.)

*Example.* Jointly Gaussian predictors satisfy (A3) with K = 1; independent predictors satisfy it when each of them
satisfies it with a common constant K. (A4) holds for all large n whenever every q_n × q_n principal block of the correlation matrix has
smallest eigenvalue at least a fixed ψ > 0: for instance correlation ρ^{|j−k|} with |ρ| < 1, or equal correlation
ρ ∈ [0, 1).

**Theorem B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window q_n of M = 1
and with exactly s ≥ 1 nonzero coordinates of β*, **and in addition**
- **(A6) Detectable signal.** (a) λ_min(Corr(x_T)) ≥ ψ for a constant ψ > 0 and every set T of at most (2A + 3)s + 2
  predictors; (b) min{ |β*_j|·sd(x_j)/σ* : β*_j ≠ 0 } ≥ b_n, where b_n > 0 and b_n²·n/log n → ∞.
Then for every sequence M_n → ∞:

    Π( d_H(f, f*) > M_n/√n | D_n ) → 0   in P*-probability.

**Corollary C (the output of the sampler).** The method uses a sequential Monte Carlo sampler to explore the models and to compute summaries
of the posterior; it does not compute the full posterior
(small problems that it solves by exact enumeration are not covered here). A run is *completed* when the method
reports the status "completed"; runs that stop early are not covered. The output of a completed run contains a list 𝒯
of at most 40r + 1 distinct models: the best-scoring models among those offered to the final run of the sampler —
the models scored in that run, together with models the method scored earlier and carries into it (its precomputed
tables for small groups of predictors, and models kept from its calibration stage). Each model in the list comes with
the logarithm of its unnormalised posterior weight, which we take to be computed in exact arithmetic. The output
contains no draws of (β, σ²). Let π(𝒯) be the posterior probability of the list, and let Π̂ — not computed by the method —
be the posterior restricted to the list: the models in 𝒯, weighted in proportion to the exponentials of their returned
log-weights, each with its exact conditional posterior distribution of (β, σ²). Under the conditions of Theorem A,
with P*-probability at least 1 − n^{−cM} over the data, **every** completed run (whatever its random numbers) with
π(𝒯) ≥ n^{−cM/2} satisfies

    Π̂( d_H(f, f*) > √(M·log n / n) ) ≤ n^{−cM/2}.

If a completed run scored the true model {j : β*_j ≠ 0} and the posterior probability of that model exceeds ½, then the
list contains it, it is the model the method reports as most probable, and π(𝒯) > ½. In general, whether the list
carries enough posterior probability is a property of the run: this corollary does not assert it, and the output does
not certify it.

**Notation table.**
| symbol | meaning |
|---|---|
| n, p, r | number of observations; number of predictors (p ≤ n^A, possibly p ≫ n); number of predictors not constant in the sample |
| (x, y), D_n | a predictor vector and its response; the n observed pairs |
| α*, β*, σ* | true intercept, coefficient vector and noise standard deviation |
| s | maximal number of nonzero coordinates of β* |
| S, β, σ² | a set of included predictors, a coefficient vector and a noise variance (a posterior draw) |
| Π(· \| D_n) | the posterior distribution of (S, β, σ²) under the method's prior |
| f, f* | joint density of (x, y) defined by a posterior draw; true joint density |
| d_H | Hellinger distance, d_H(f, g) = (1 − ∫√(fg))^{1/2} |
| P* | distribution of the data |
| sd, Var, Corr | population standard deviation, variance, correlation matrix |
| z_j, z | standardised predictor (x_j − E x_j)/sd(x_j); the vector of all of them |
| x_T, λ_min | sub-vector of x for a set T of predictors; smallest eigenvalue |
| M, q_n | the level (M ≥ 1, chosen by the reader); the window min{p, ⌈C_q M log n⌉} |
| K, c_ψ, b̄, ψ, b_n | constants of (A3), (A4), (A5); eigenvalue bound and beta-min level (b_n > 0) of (A6) |
| c, C₁, M₀, n₀ | constants of Theorem A, depending only on (s, A, K, c_ψ, b̄) |
| 𝒯, π(𝒯), Π̂ | the sampler's returned list of models; its posterior probability; the posterior restricted to it |

---
### One line per assumption: why it is there, and whether it is necessary
| assumption | why it is there | necessary? |
|---|---|---|
| (A1) Gaussian linear model, noise independent of x, any σ* > 0 | it is the model under which the method's likelihood is correct; it gives the posterior a closed form given the predictors and χ² tails. σ* is free because, when the response is rescaled, the posterior over models does not change and the posterior of (β, σ²) rescales with it | not known to be necessary; sub-Gaussian noise is open and is not a target |
| (A2) at most s nonzero coefficients; p ≤ n^A | posterior model size is controlled relative to s; the constants depend on s and A | over a class of designs as general as this one, some sparsity is needed for a rate of order log p/n (not for every particular design); exact sparsity and the polynomial bound on p are proof devices (stretch items: approximate sparsity, exponential p) |
| (A3) sub-Gaussian predictors | only to make the sample variances of the predictors and the sample covariances of small groups of predictors track their population values, with probability 1 − n^{−cM} | **not necessary**: the general (master) theorem needs only three properties of the sample, whatever the tails, and the passage from the sample to the population distance uses no tail condition; simulations with infinite fourth moments show no degradation (finite-n evidence only). This is a statement about the master theorem's interface form; no primitive statement under weaker tails is claimed |
| (A4) no near-exact collinearity (eigenvalue ≥ c_ψ/n on groups of order log n) | keeps the prior's penalty for each extra predictor (a factor of order n^{−1/2}) in force; this gives the rate √(log n/n), the exponent n^{−cM} and the bounded model size | **not necessary for consistency**: without it the rate loses one logarithm (stated under the theorem). Whether it is needed for the sharp rate is open. Any fixed ψ > 0 satisfies it. It is far weaker than a fixed eigenvalue bound, but it does make sparse coefficient vectors distinguishable in principle |
| (A5) bounded signal per predictor | bounds the signal in units of the noise; excludes huge coefficients that cancel, for which the prior (scaled to the response) is badly centred | the proof needs it in a weaker form (bounded sample signal energy and standardised coefficient norm at most const·√n). When cancelling coefficients of size n break that weaker form, the proof's interface fails and simulations show n·d² growing like n; this is evidence about the proof's condition, not a necessity theorem |
| (A6) detectable signal (Theorem B only) | makes the posterior select the true model, which removes the logarithm | selection consistency is what this route to the rate 1/√n uses; Theorem A's rate holds without it |

### Proposed additional target clauses
- **TC9 (reader Theorem A).** Assumptions (A1)–(A5) as written; displays (i) and (ii) with radius √(M log n/n), size bound
  s + C₁M and level n^{−cM} for M₀ ≤ M ≤ √n/log n; the sentence without (A4). Faithfulness: Theorem A = DIST-1/DIST-2 + B0, B1, B2.
  **Fixed by HQ at CP1.** v1.4 (after the blind read S2) changes the Setup's description of the prior (r, the number of
  non-constant predictors, in place of p) and one descriptive sentence ("no identifiability condition"); assumptions
  (A1)–(A5), displays (i), (ii) and the sentence without (A4) are unchanged.
- **TC10 (reader Theorem B and Corollary C), if HQ makes them headline.** As written; Theorem B conditional on
  W3-POST:Thm-1; Corollary C with its premise on the returned list stated in the display.
