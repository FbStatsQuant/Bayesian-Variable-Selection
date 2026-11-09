# Blind proposal (Claude Fable 5.2) — a theorem package for SMC-BVS v3.1

Date: 2026-11-09. Proposer: Claude Fable 5.2, blind, no coordination with the other proposer.

**What I read.** `BRIEF_BLIND.md`; `State_of_Project/sections/02_method.tex` (method, settings table, pipeline);
`A_notation.tex` (I used the method symbols only and disregarded the rows that describe earlier theorem cards);
production code `Scripts/SMC_BVS/core/` (the LS0 block of `cpp/v3_core.cpp`, `Engine::local_search` in
`cpp/v3_engine.h`, README); Song & Liang (2015), pp. 947–960. Nothing else under `Theory_work/` or `Docs/Theory/`.

**Status of the content.** Statements below are proposals with proof sketches I worked out for this document; none is
checked line by line. Places where I am guessing are marked **[S]** (speculation). Literature page numbers are from
memory and must be verified before citation.

---

## 0. The proposal in six lines

1. **Target.** The coded posterior (g = n, unit ridge, BB(1,p), cap K = ⌊n/2⌋) is an EBIC-type criterion with γ = 1.
   It concentrates on the true model S₀ for every fixed A under Song–Liang-type conditions. The one new ingredient is a
   **design-free size-reduction lemma** that makes the large cap harmless.
2. **Reported model.** The reported HPM is the best model ever scored. So "Ŝ = S₀" needs exactly two facts: S₀ is the
   global maximiser of F, and S₀ is scored at least once. The second fact is carried by **LS0 from the block start
   mode**, which is deterministic (no uniforms).
3. **Misspecification.** Song–Liang's Section 2.3 maps onto the block tables. Each table is *exactly* a correctly
   specified regression of dimension ≤ B for the block projection of the mean, with inflated noise variance.
4. **Sampler outputs.** In the regime where the start is consistent, an elementary argument (unbiasedness of the
   unnormalised particle measure plus one deterministic inequality) gives consistency of the reported evidence, PIPs and
   MPM for the sampler *as coded*, with no growth condition on N or R′ and for any frozen calibration.
5. **General designs.** With no condition on the start, a "certified screening" theorem still holds: a sparse,
   locally certified reported model contains S₀.
6. **Not claimed:** rapid mixing or sampler accuracy for general designs. I give a calculation (Appendix A2)
   suggesting the score landscape is multimodal for this prior unless the design is nearly orthogonal **[S]**.

---

## 1. Setting and assumptions

X is the standardised design (columns centred, ‖x_j‖² = n−1), treated as deterministic (triangular array).
Notation of the method file: F, ϖ, m, Q_S, G_S, K, B, ℓ, π₀, γ₀, S̃₀, d, q_φ, Ẑ_r, N_e, R′, 𝒪.

- **A1 (model).** y_raw = α1 + X b* + ε, ε ~ N_n(0, σ*² I). S₀ = supp(b*), |S₀| = s fixed.
- **A2 (dimension).** p ≤ n^A for a fixed A > 0.
- **A3 (bounded signal).** ‖X b*‖² ≤ M n σ*². Write ρ_s = ‖Xb*‖² / (‖Xb*‖² + nσ*²) < 1 for the signal fraction and
  σ_y² = σ*²/(1−ρ_s) for the total variance.
- **A4 (sparse identifiability).** λ_min(X_T′X_T/(n−1)) ≥ κ > 0 for every T ⊇ S₀ with |T| ≤ s + k_n, where
  k_n = ⌈((A+½)s + 1) log₂ n⌉.
- **A5 (beta-min).** n · min_{t∈S₀} b*_t² ≥ C_β σ*² log n, with C_β = C_β(A, s, κ, M).

Two further assumptions, used only for the start and the search (Theorems 2–4), are stated relative to the
partition C₁,…,C_J that the method itself computes from X. For a block b, U ⊆ C_b and j ∈ C_b∖U define the
**noiseless gain** g(j | U) = (x_j′(I−P_U) X b*)² / ‖(I−P_U) x_j‖² (how much of the mean is newly explained by j).

- **B1 (block visibility).** For every t ∈ S₀ with block b and every U ⊆ C_b∖{t}: g(t | U) ≥ C_v σ_y² log n.
- **B2 (leakage budget).** There is a deterministic set 𝓛 ⊆ S₀ᶜ with |𝓛| ≤ (1−ε₀) log n such that
  Λ_n = Σ_{l ∉ S₀∪𝓛} max_U P( |g(l | U)^{1/2} + σ* Z| ≥ σ_y τ_n ) → 0, where Z ~ N(0,1), τ_n² = 2 log p + log n,
  and the max is over U ⊆ C_{b(l)}∖{l}. "Zero leakage" means 𝓛 = ∅.

### Why these are mild (comparison with Song–Liang)

| Song–Liang (2015) | Here | Comment |
|---|---|---|
| Model (1), Gaussian errors; strict sparsity (4) | A1 | Identical. |
| P_n < exp(Cn^α) | A2: p ≤ n^A | Narrower by Felipe's goal 3. |
| Conditions 1–2 (moments of linear combinations of predictors; bounded predictors, Σ\|β_j\| < ∞) | A3 | A3 is the fixed-design form of "bounded signal". No moment condition on X is needed because X is standardised. |
| Condition 3 (identifiability: no combination of r̄_n other predictors mimics x_k; implied by a lower bound on the smallest eigenvalue of every (r̄_n+1)-sub-covariance) | A4 | Same idea, at size O(s log n) and only for sets containing S₀. Holds with high probability for sub-Gaussian rows with covariance eigenvalues bounded below when s·log n·log p = o(n) (Raskutti, Wainwright & Yu 2010; Rudelson & Zhou 2013). Equicorrelated, AR, block and factor designs all satisfy it. |
| Prior conditions (9)–(14): size cap r̄_n with r̄_n log P_n ≺ nε_n²; prior size r_n ≻ 1 | none | The coded cap K = ⌊n/2⌋ **violates** their (10), and BB(1,p) has prior mean size ≈ 1, not r_n → ∞. So their Theorems 1–3 cannot be quoted for the coded prior. Lemma A below replaces the cap condition. |
| Implicit fixed coefficients (a missed true predictor moves the density by ≥ ε_n) | A5 | Explicit and at the minimax scale √(log p / n) (Wainwright 2009). Fixed coefficients satisfy it. |
| Condition 4 and Condition 5 (\|cov(x_t, y)\| > 0 for true predictors in a subset) | B1 | Quantitative version of Condition 5, block by block. |
| Remark (a) after Condition 5: "only a small proportion of predictors are linearly correlated with X_t" (informal) | B2 | A formal budget: at most log n noise columns may be strongly correlated with out-of-block signal; the rest must be at the chance scale *in aggregate*. Independent or population block-structured columns give Λ_n ≈ n^{-1/2} with 𝓛 = ∅ (the diluted z-score of such a column is exactly N(0,1)). |

B1–B2 are assumptions on (X, b*) through a deterministic functional of X. They are not a design family. Their role is
the same as Song–Liang's Section 2.3 conditions for the split stage.

---

## 2. The theorem package

### Theorem 1 (posterior concentration on the true model) — Song–Liang Theorems 1–3 and S for the coded target

**Statement.** Under A1–A5, π(S₀ | y) → 1 in probability, and E_π|S △ S₀| → 0 in probability.
Expected rate: 1 − π(S₀ | y) = O_P(n^{-1/2} · polylog n) **[S for the exact rate]**.

**Corollary 1.1 (exact-posterior outputs).** With probability → 1: (i) S₀ is the unique maximiser of F over Ω (exact
HPM = S₀, the analogue of their Theorem S); (ii) min_{j∈S₀} PIP_j → 1 and max_{j∉S₀} PIP_j → 0, in fact
Σ_{j∉S₀} PIP_j → 0 (sure screening *and* specificity, stronger than their Theorem 3); (iii) the exact MPM equals S₀;
(iv) Z = e^{F(S₀)}(1+o_P(1)); (v) the posterior of the fitted density contracts in Hellinger distance (their Theorems
1–2), as a consequence of (i) and fixed-dimensional theory on S₀.

**Corollary 1.2 (exact branch).** Whenever the run takes the enumeration branch (status `exact`), every reported
output inherits Corollary 1.1. For fixed p this is eventually every run.

**Lemma A (design-free size reduction) — the new ingredient.** Under A1–A3 only (no condition on X at all),
π(|S| > k_n | y) → 0 in probability, with k_n as in A4.

**What it buys.** The consistency story of Song–Liang for the model actually coded, for all A, with p ≫ n, and
without their cap condition. Everything else in the package rests on the single event "S₀ is the global maximiser with
a gap". Remark for the paper: false-positive control needs much less than A4 because of the unit ridge (a spurious
column needs only residual norm² ≳ 1, not ≳ κn, to be penalised at the full ½ log n) **[S: I checked one-column
additions only]**.

### Theorem 2 (the block start under misspecification) — Song–Liang Theorem 4 and Corollary 2

**Statement.** (a) *Exact reduction.* For each block b let θ^(b) be the least-squares coefficient of X b* on X_{C_b}.
Every table entry r_b(U), U ⊆ C_b, is a function of (P_U y, ‖y‖). Hence the block table is the table of a correctly
specified regression with at most B predictors, coefficient θ^(b) and noise variance
σ_b² = σ*² + ‖(I−P_{C_b})Xb*‖²/n ≤ σ_y². The unexplained signal acts only as extra variance ("dilution"), never as
bias.
(b) *Screening by the start mode.* Under A1–A3, B1, B2: P(S₀ ⊆ S̃₀ ⊆ S₀ ∪ 𝓛) → 1.
(c) *Consistent start.* If moreover 𝓛 = ∅ and the leak sum decays polynomially (Λ_n ≤ n^{-c}), then S̃₀ = S₀ with
probability → 1 and π₀(S₀) ≥ 1 − n^{-c′}.

**Why mild.** See the table. (a) needs nothing. The dilution costs only a constant in the detection threshold, because
A3 bounds σ_y²/σ*².

**What it buys.** The exact counterpart of Song–Liang's split stage: what the composite start selects, when it screens,
and when it is already consistent. It also explains honestly when the start is *bad*: a pervasive common factor makes
every block projection non-zero, and S̃₀ becomes dense.

### Theorem 3 (the reported HPM equals S₀) — carried by LS0

**Statement.** Under A1–A5, B1, B2, in exact arithmetic: P(𝒪 ∩ {Ŝ ≠ S₀}) → 0. On the same event the LS0 path is
S̃₀ → … → S₀ by exactly |S̃₀∖S₀| single deletions of leak variables, the last scan certifies S₀
(`local_certified`), and |S̃₀∖S₀| ≤ |𝓛| ≤ ℓ. The statement holds **for every seed, every N_e, every R′ and every
calibration outcome**, because LS0 reads no uniforms and the HPM is the maximum over all scored models.

**Note on the move cap.** The method text gives LS0 the cap ℓ; the production code uses ℓ + |S̃₀|
(`cpp/v3_core.cpp:473`). The theorem holds under both, since |𝓛| ≤ log n < ℓ.

**What it buys.** The headline: selection consistency of what the method outputs, with no Monte Carlo premise. This is
strictly more than Song–Liang, who prove consistency of the MAP of the posterior, not of anything SAMC returns.

**Extension [S].** One masked true variable (B1 failing for a single t) can be handled: at any superset of S₀∖{t},
adding t beats adding any proxy by Cauchy–Schwarz plus A4. Two or more masked variables need a forward-selection
condition of Tropp (2004) type restricted to S₀ ∪ 𝓛; I would not promise it.

### Theorem 4 (reported evidence, PIPs and MPM)

**Statement.** (a) *Always (any n, p, N).* Conditional on any frozen calibration record 𝒞 and under ideal uniforms:
E[Ẑ_r | 𝒞] = Z, and E[Ẑ_r · H_r(h) | 𝒞] = Z · π(h) for every bounded h, including the recorded Gibbs conditionals
o_j. For fixed data, N_e → ∞ gives consistency of Ẑ and of both PIP poolings (standard SMC theory).
(b) *Joint asymptotics, concentrated bridge.* Let δ̄_n be the larger of the odds π₀(S₀ᶜ)/π₀(S₀) and
π(S₀ᶜ)/π(S₀), and let T be the number of stages of the frozen grid. If T² δ̄_n → 0 in probability, then for every
N_e ≥ 1 and R′ ≥ 1, conditional on 𝒞: (i) Ẑ_r / Z → 1; (ii) at every stage and in every measured round the fraction
of particles not at S₀ tends to 0; (iii) max_j |PIP̂_j − 1{j ∈ S₀}| → 0 for the primary and the equal-weight pooling;
(iv) both reported MPMs equal S₀ with probability → 1.
(c) Under A1–A5, B1 and zero leakage (Theorem 2(c)), δ̄_n ≤ n^{-c}, and T ≤ T_e ≤ 4·max(1000, ℓ²) by the coded
ceiling, so the condition of (b) holds automatically.

**What it buys.** A complete end-to-end consistency theorem for the sampler as coded (one round per stage, logarithmic
burn-in, default budgets), valid for *any* frozen schedule. No artificial growth rate for islands or particles
appears anywhere in the package. Honest label: this is the regime where the start already finds S₀ and the bridge has
no mass to transport.

### Theorem 5 (certified screening for general designs) — no condition on the start

**Statement.** Let q_n ≤ c n / log p. Assume A1–A3, A4 for sets of size ≤ q_n + s, and the strengthened beta-min
n · min_t b*_t² ≥ C q_n σ*² log p (true for fixed coefficients and any q_n = o(n / log n)). Then
P(𝒪 ∩ {`local_certified`} ∩ {|Ŝ| ≤ q_n} ∩ {S₀ ⊄ Ŝ}) → 0.
(b) **[S]** If in addition the ratio of largest to smallest sparse eigenvalue over sets of size ≤ q_n + s is below
1 + 1/(2A), the same event with {Ŝ ≠ S₀} has probability → 0.

**What it buys.** A sure-screening guarantee (Song–Liang's Theorem 3 in spirit: sensitivity, not specificity) for the
reported model in *any* design satisfying A4, including equicorrelated and factor designs where Theorems 2–4 do not
apply. Both conditions in the event are printed by the method (`local_certified`, |Ŝ|).

**Remark (outside the as-coded scope; not claimed).** The certificate card already enumerates all subsets of Ŝ (item
L2). If the method reported the best subset of Ŝ instead of only printing the gap, Theorem 5 plus Theorem 1 would give
exact selection for general designs. This is a method change and Felipe's call.

---

## 3. Which part of the method carries the reported-model guarantee

**The structure of the output decides it.** Ŝ = argmax of F over everything scored. With Corollary 1.1(i), "Ŝ = S₀"
is equivalent to "S₀ was scored". There are three ways S₀ can get scored.

| Route | Mechanism | Regime where I can prove it | Main obstacle |
|---|---|---|---|
| **Search from the start mode (LS0)** — recommended carrier | Deterministic backward elimination from S̃₀ | B1 + leakage budget ≤ log n (Theorem 3) | The path is data-dependent. Uniform control is only available over a small deterministic family (subsets of S₀ ∪ 𝓛). With pervasive leakage (common factor) S̃₀ is dense and nothing is controlled. |
| Start draws / particles | iid π₀ draws and Gibbs sweeps score S₀ | Consistent start (Theorem 4) | Same regime as above with 𝓛 = ∅; gives nothing new for the HPM, but gives PIPs and evidence. |
| Posterior concentration + sampler accuracy | Particles approximate π, and π(S₀) → 1 | Not provable in general | (i) Joint-asymptotic SMC error bounds need mixing; the code has one round per stage and log n burn-in. (ii) For this prior the per-variable penalty exceeds the noise level only by the factor 1 + 1/(2A), so the landscape is not unimodal unless the design is near-orthogonal (Appendix A2), and the rapid-mixing theory of Yang, Wainwright & Jordan (2016), which needs a much heavier prior, does not transfer. (iii) Between a wrong start mode and S₀ the bridge has a first-order transition, the classical hard case for tempering. |

**Conclusion.** The reported-model guarantee should be carried by **Theorem 1 (global optimality) + LS0 (discovery)**.
The sampler carries the *uncertainty* outputs (PIPs, evidence), with a full theorem only where the bridge is
concentrated and exact identities elsewhere. The final local search from the SMC best contributes Theorem 5 only: its
starting point is random and uncontrolled, but its certificate is informative for any design.

---

## 4. Proof strategy, hardest steps and risk

### Theorem 1 — risk: low to medium

Key lemmas.
- **L0 (score algebra).** Q_S = min_β {‖y − X_Sβ‖² + β′(G_S+I)β/n}; hence Q is monotone under nesting and
  Q_S ≥ ‖y‖²/(n+1). The Occam term is Σ_i ½ log(((n+1)λ_i+1)/(λ_i+1)) ∈ [0, (|S|/2) log(n+1)]. One-column update:
  fit factor a = n r²/((n+1) r²+1) and penalty factor (1−a)^{1/2}, with r² the residual norm² of the new column.
- **L1 (direction reduction).** The coded Bayes factor depends on y through its direction, up to the IG(0.01, 0.01)
  term. Coded BF(T : S₀) ≤ C n^{0.51} × the likelihood ratio of two angular central Gaussian laws (Tyler 1987) on the
  centred sphere. The b₀ effect is O(1) because Q_{S₀} ≍ n.
- **Lemma A.** Under the prior predictive of S₀ the expected Bayes factor of any T is exactly 1. So the expected
  posterior odds of the whole size class k equal its prior odds, C(p,k)w(k)/w(s) ≤ 2^{-k}(2p)^s. Moving from the prior
  predictive to the true law costs a factor n^{s/2} on a high-probability event (prior mass near the truth, as in
  Ghosal, Ghosh & van der Vaart 2000, Lemma 8.1). Summing the geometric tail from k_n gives the claim.
- **Lemma B (supersets of size ≤ s + k_n).** Truncated first moment: on the event where every χ²_j(T) is below its
  union-bound level, E Σ_T BF ≤ C(s+j, j) 2^{-j} (C log p / n)^{j/2}. The plain first moment is useless here (it equals
  the prior odds); the truncation supplies the ½ log n margin. This is the EBIC γ = 1 calculation of Chen & Chen
  (2008), done as a sum instead of a maximum.
- **Lemma C (models missing a true variable).** Factor F(T) − F(S₀) through T ∪ S₀. If T has more than (2A+1)r spurious
  variables (r missing truths), Lemma B's smallness beats the at most r·(A+½) log n saved in penalty. Otherwise finitely
  many spurious variables: union bound plus A4, A5.

Tools: χ² tails (Laurent & Massart 2000); Chen & Chen (2008); Narisetty & He (2014) and Castillo, Schmidt-Hieber & van
der Vaart (2015) as templates for the organisation.
**Hardest step:** Lemma A with standardisation and the proper IG prior (making the martingale identity exact on the
direction, and the change of measure uniform). **Would fail if:** the n^{0.51} and n^{s/2} factors are larger than
polynomial (I do not expect it), or errors are non-Gaussian (then Lemma A needs a different argument; restricting to
Gaussian errors matches Song–Liang).

### Theorem 2 — risk: low to medium

(a) is linear algebra. (b)–(c): there are at most 2^B·J ≤ 2^16·p table entries, so a *finite polynomial union bound*
concentrates all of them at once. The start mode is then read off the block DP, using that the size-prior increment
log((2p−1−k)/(k+1)) is monotone in k. For (c), sum the per-block odds; the same truncated-moment computation as Lemma B.
Template: Song–Liang Theorem 4 and Corollary 2; Kleijn & van der Vaart (2006) for misspecification in general.
**Hardest step:** the exact form of B2. Per-column worst-case bounds are too crude for random designs (the noiseless
leak and the noise cannot be maximised by the same column), which is why B2 is an aggregate condition. **Would fail
if:** the constants in B1/B2 cannot be made explicit; then state (b) with a gap condition on θ^(b).

### Theorem 3 — risk: medium

Work on the event of Theorem 1 and Theorem 2(b), with A = S₀ ∪ 𝓛 deterministic and a = |𝓛|. For every T with
S₀ ⊆ T ⊆ A:
- every spurious t-statistic satisfies t²_{T,j} ≤ ‖(P_A − P_{S₀})ε‖²/σ̂², a **single** χ²_a variable (no union over
  subsets), so t² ≤ a(1+o(1)) < log n < 2·penalty: every leak deletion improves F;
- for l ∉ A, split (I−P_T)x_l = (I−P_A)x_l + (P_A−P_T)x_l (orthogonal). The first part needs a union over p only; the
  second is bounded by the same χ²_a. Hence t² ≤ 2 log p + a + o(log n) < 2 log p + log n: no addition improves F;
- a swap is a deletion followed by an addition, so every swap is dominated by a deletion; deleting a true variable is
  excluded by A4–A5.
So the best move at every such T is a leak deletion, the path stays in the family and ends at S₀.
**Hardest step:** keeping the variance-ratio factor uniform over the family and making the premises on the DP argmax
and exact arithmetic explicit. **Would fail if:** the leak set is larger than log n. Larger budgets need a bound on
partial correlations between outside columns and 𝓛 **[S]**.

### Theorem 4 — risk: low to medium for (a)–(c); high beyond

(a) Unbiasedness of unnormalised Feynman–Kac particle measures (Del Moral 2004, ch. 7; Del Moral, Doucet & Jasra
2006); consistency in N from Chopin (2004). (b) Three elementary facts:
1. *Deterministic inequality.* Ẑ_r / Z ≥ (π(S₀)/π₀(S₀)) · Π_t A_{t−1}, where A_t is the fraction of particles at S₀
   after stage t (drop all other particles from each mean weight).
2. *Unbiasedness.* E[(Ẑ_t/Z_t)·(1 − A_t)] = 1 − q_{φ_t}(S₀), also mid-round and in measured rounds, because every
   elementary step is invariant.
3. *Hölder.* The odds q_φ(S₀ᶜ)/q_φ(S₀) are at most the larger endpoint odds, for every φ.
Markov plus a union over the T stages, then induction on Π A_t ≥ ½, gives all claims when T² δ̄_n → 0. The upper tail
of Ẑ/Z follows from mean one. For PIPs use fact 2 with h = o_j and sum over j ∉ S₀ (Corollary 1.1(ii)).
**Hardest step:** none is deep; care is needed with the mid-round recording of o_j. **Would fail if:** the coded
kernel were not invariant step by step (the method file records this as verified).
**Beyond the concentrated bridge [S, high risk].** With leaks, the bridge lives on the cube between S₀ and S₀ ∪ 𝓛
(≤ n^{0.7} models, fewer than N_e). A Gibbs flip equilibrates two models differing in one coordinate *exactly*, so if
the mode path drops one leak at a time, each sweep re-equilibrates. I think a theorem exists here, but I would not
budget for it.

### Theorem 5 — risk: medium

If a q_n-sparse T misses r ≥ 1 true variables, an OMP-type inequality (Tropp 2004; Zhang 2011) gives a true variable
whose addition gains ≥ nκ² b_min²; the noise, uniformly over q_n-sparse sets, is ≤ 2σ² q_n log p. So T has an improving
addition and is not locally certified. **Hardest step:** the uniform noise bound forces the strengthened beta-min.
**Would fail if:** signals are at the minimal scale and the returned model is not very sparse; then state it for
fixed coefficients only. Part (b) is the first-moment count of Appendix A2 and is **[S]**.

---

## 5. What not to claim, and the cleanest honest scope

Do not claim:
1. **Rapid mixing or sampler accuracy for general designs** in joint asymptotics. Outside the concentrated bridge the
   package offers exact identities and fixed-data N → ∞ only.
2. **Reported-HPM consistency for every design satisfying A4.** With pervasive leakage (strong common factor, many
   columns correlated with the signal) the start mode is dense, B2 fails, and only Theorems 1 and 5 apply.
3. **That the start gives speed or depth**, or that the bridge "does the work" in the proved regime. In Theorem 4 the
   start already sits at S₀.
4. **Any reading of E1–E3, the ESS rule, `global_certified` or the restricted grid as accuracy guarantees.** They enter
   only through "any frozen 𝒞".
5. **Exact selection below the beta-min scale.** Without A5 the natural statement is no false positives plus
   recovery of the strong signals **[S]**.
6. **Non-Gaussian errors, super-polynomial p, growing s** (extensions, not part of the package), or floating-point
   validity (all statements are for exact arithmetic and ideal uniforms).
7. **Probabilities conditional on delivery.** State everything as P(𝒪 ∩ ·), as the method's output convention does.

**Cleanest honest scope, as one sentence for the paper.** *For Gaussian sparse regression with p ≤ n^A and a design
with sparse eigenvalues bounded below, the coded posterior concentrates on the true model; if in addition the method's
own blocks leak at most logarithmically many columns, the reported HPM equals the true model for every seed, and with
no leakage the reported PIPs, MPM and evidence are consistent as well; for any other design, a sparse certified
reported model contains the true model.*

---

## 6. Recommendation

I would bet the multi-week budget on **Theorems 1, 2 and 3 as the core, Theorem 4 as the second priority, and Theorem
5(a) as a cheap general-design safety net**. Theorem 1 with Lemma A is the Song–Liang story for the coded prior and is
low risk because it is the EBIC γ = 1 calculation plus one new, short, design-free lemma. Theorems 2–3 put the
reported-model guarantee where the method can actually bear it: on the deterministic chain "block tables → start mode
→ LS0 → best scored model", under one formal leakage budget that mirrors Song–Liang's Section 2.3. Theorem 4(b) is the
best value in the package: about a page of proof for an end-to-end sampler theorem with no growth conditions.
I would explicitly *not* spend budget on general-design sampler accuracy or on rapid mixing, and I would decide early
whether the leak extension of Theorem 4 and the near-orthogonal part of Theorem 5 are worth a small exploratory
ticket each. Order of work: Lemma A (it is the only place where the whole package could surprise us), then Theorem 1,
then Theorem 2(a)–(b), Theorem 3, Theorem 4(b), Theorem 5(a).

---

## Appendix A. Two calculations behind the proposal

**A1. The margin of the coded prior.** Adding one spurious variable to a model of size k costs
log((2p−1−k)/(k+1)) + ½ log(n+1) ≈ log(2p) + ½ log n in F (prior plus Occam factor). The best of p noise directions
gains about log p. The margin is ½ log n, whatever A is. This is EBIC with γ = 1, which satisfies Chen & Chen's
γ > 1 − 1/(2A) for every A. It also means penalty/noise = 1 + 1/(2A): the prior is consistent but only just, and
arguments that take a maximum over all sparse models times a count (instead of a sum) fail for p > √n.

**A2. Why I expect multimodality [S].** A superset T ⊋ S₀ with j ≥ 2 spurious variables is stable under single
deletions when all j spurious t-statistics exceed 2·penalty ≈ (2A+1) log n. Since Σ_j t_j² ≤ (condition number) ×
χ²_j(T), the expected number of such supersets is about n^{j(A − (A+½)/cond)}. This vanishes only if
cond < 1 + 1/(2A) (for two columns with correlation ρ: ρ < 1/(4A+1)). Above that threshold spurious local maxima of F
should exist in worst-case designs. Their posterior mass is negligible (Theorem 1), but a greedy search or a sampler
with log n rounds can sit on them. This is the reason the package routes the HPM guarantee through a controlled start
instead of through global landscape properties.

## References (verify volume and pages before citing)

- Song & Liang (2015), JRSSB 77(5), 947–972. Jiang (2007), Ann. Statist. 35(4), 1487–1511.
- Chen & Chen (2008), Biometrika 95(3), 759–771. Scott & Berger (2010), Ann. Statist. 38(5), 2587–2619.
- Narisetty & He (2014), Ann. Statist. 42(2), 789–817. Castillo, Schmidt-Hieber & van der Vaart (2015), Ann. Statist.
  43(5), 1986–2018. Yang, Wainwright & Jordan (2016), Ann. Statist. 44(6), 2497–2532.
- Ghosal, Ghosh & van der Vaart (2000), Ann. Statist. 28(2), 500–531. Kleijn & van der Vaart (2006), Ann. Statist.
  34(2), 837–877. Tyler (1987), Biometrika 74(3), 579–589. Laurent & Massart (2000), Ann. Statist. 28(5), 1302–1338.
- Wainwright (2009), IEEE Trans. Inf. Theory 55(12), 5728–5741. Raskutti, Wainwright & Yu (2010), JMLR 11, 2241–2259.
  Rudelson & Zhou (2013), IEEE Trans. Inf. Theory 59(6), 3434–3447.
- Tropp (2004), IEEE Trans. Inf. Theory 50(10), 2231–2242. Zhang (2011), IEEE Trans. Inf. Theory 57(7), 4689–4708.
- Del Moral (2004), *Feynman–Kac Formulae*, Springer. Chopin (2004), Ann. Statist. 32(6), 2385–2411. Del Moral, Doucet
  & Jasra (2006), JRSSB 68(3), 411–436. Barbieri & Berger (2004), Ann. Statist. 32(3), 870–897.
