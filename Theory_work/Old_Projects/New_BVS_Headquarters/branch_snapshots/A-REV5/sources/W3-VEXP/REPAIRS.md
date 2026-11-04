# W3-VEXP: repairs, extra statements and proofs

These are referee additions to W1-EXP. Notation follows W1-EXP `PROOF.md` and `00_COMMON.md`. Status words
follow the protocol. Every item is a **candidate**: it has not been reviewed or adopted.

---------------------------------------------------------------------------------------------------

## R1. Data-computable EXP′ remainder certificate (any n, any data). Status: **PROVED**

**Corollary R1.** Fix any data set and any partition. Suppose SE-blk(φ) holds on the realised blocks, that is,
min_b λ_min(R_{C_b}) ≥ φ² > 0, and suppose y ∉ span X_{C_b} for every b. Then every within-block addition (b, T, l) satisfies

    |R_{n,b,T,l}| ≤ cert := (1 + φ^{-2}) / (2 φ² (n-1)) + ν (1.02 + 1/(n φ²)) / min_b RSS^y_{C_b},

where R is the exact EXP′ remainder, log r_b(T+l)/r_b(T) = −½ log(n+1) − ν log(1 − x_{T,l}) + R.

*Proof.* Lemma 1.3 of W1 is deterministic. Its bound is (1+φ^{-2})/(2φ²(n−1)) + ν(1.02 + 1/(nφ²))/min_{U⊆C_b} RSS^y_U.
For U ⊆ C_b we have P_U ≼ P_{C_b}, so RSS^y_U = y'(I−P_U)y ≥ y'(I−P_{C_b})y = RSS^y_{C_b} > 0. Hence the minimum
over U is RSS^y_{C_b}, and minimising over b gives a bound uniform in b. Lemmas 1.1 and 1.2 need
λ_min(G_S) ≥ φ²(n−1) for S ∈ {T, T+l}; this follows from SE-blk by Cauchy interlacing. ∎

**Why this is the right finite-n statement.** Theorem 1's κ_EXP replaces min_b RSS^y_{C_b} by the probabilistic
floor c_* n, with c_* = σ²/(8(M+2σ²)). At the study signal scale (M ≈ 25σ² at c = 1) this gives κ_EXP ≈ 100–125 nats,
and κ_EXP ≈ 1,700 at c = 4. The certificate is computable from the data and equals 0.59–1.52 nats in every simulated
study design (`results/study_exp.txt`, `results/study_nsweep_S3.txt`). The actual max |R| over every within-block
addition is ≤ 0.145 at n = 200 (all six scenarios, c ∈ {0.5, 1}). So EXP′ at the study size should be stated
with `cert`, not κ_EXP.

---------------------------------------------------------------------------------------------------

## R2. Theorem 2 is a direct corollary of the locked T22(iii). Status: verdict VERIFIED (composition complete)

W1 labels Theorem 2 PROOF SKETCH because it routes through Prop. 2.1 (NL_η → NL_C). That route is not needed.
Under BO, Lemma 2.3(i) gives δ_{T,l} = 0 on the whole leakage family 𝓛_n. That is the **locked** hypothesis NL_η
with η = 0, and the locked §"Admissible rates" then supplies NL_avg(½), since exact zero leakage permits κ = ½.
VIS follows from BM-blk (W1's displayed computation, checked). EXP′ is Theorem 1. The other locked hypotheses
(G, R, within-block SE) are hypotheses of Theorem 2. So the locked T22(iii) applies **verbatim**, and

    1 − π₀(S₀) = O_P(2^B √(log n) n^{-1/2}).

No step remains open. I do not change W1's status word; I record that I found no missing step.

---------------------------------------------------------------------------------------------------

## R3. LH family, iid-Gaussian realisation, part (a): closing W1's flagged gap. Status: **PROOF SKETCH** (non-routine steps complete; routine uniform-LLN step not written out)

W1 §4.3 leaves open "the conditioning argument for the leakage family uniformly over the X-dependent partition".
In LH (g ≤ B < 2g) this closes, because on its high-probability event the partition is a **fixed** set partition.

**Setting.** Rows of X^r are iid N(0, Σ_LH), independent of ε. Assume |ψ_i| < min(ρ_{a_i}, ρ_{b_i}), g ≤ B_n < 2g,
p ≤ n^A, s, c fixed, and fixed nonzero betas. Let 𝒢 be the group partition, which is deterministic.

1. **Partition event.** Let P_n = {method blocks = 𝒢}. The proof of Lemma 4.2 needs only, for every group h,
   min within-h |r_jk| > max |r_jk| over pairs with j ∈ h, k ∉ h. Population margins are ρ_- versus ψ_+ < ρ_-.
   Uniformly over the ≤ p² pairs, sample correlations are within O_P(√(log p / n)) of population, so
   P(P_n) → 1. On P_n the cut and the next-fit packing are deterministic and give 𝒢.
2. **Fixed-partition surrogate.** Define ũ_n like u_n° but over the blocks of 𝒢, and Ṽ_n = (p−s)^{-1} Σ_{l∉S°}
   Σ_{T: U°_h ⊆ T ⊆ C_h∖l} (1 − x_{T,l})^{−ν} 1{x_{T,l} ≤ t_n}, with h = h(l) and t_n = h_n²/n.
   On P_n, u_n° = ũ_n. This is an identity of random variables, so no conditioning on P_n is needed.
3. **Exact Beta law (the key step).** Fix l ∉ S° and T with U°_h ⊆ T ⊆ C_h∖{l}. Let w_l = x^r_l − X^r_T a, with
   a = Σ_TT^{-1}Σ_{T,l}. Then Cov(w_l, X^r_T) = 0. Also Cov(w_l, μ^r) = c_l − a'c_T, where c = Σβ = Cov(X^r, μ^r).
   By Lemma 4.1 the population block coefficient γ_h = Σ_hh^{-1} c_h is supported in U°_h, so
   c_h = Σ_{h,U°} γ_{U°} and c_l − a'c_T = Σ_{l,U°}γ − Σ_{l,T}Σ_TT^{-1}Σ_{T,U°}γ = 0, because U° ⊆ T.
   This holds for null l and for the masked hub j_b. The triple (w_l, X^r_T, μ^r) is jointly Gaussian with
   w_l uncorrelated with the other two, so w_l ⟂ (X_T, μ, ε) as n-vectors (rows iid).
   Hence (C − P_T) x_l = (C − P_T) C w_l is spherical in the (X_T)-measurable subspace range(C − P_T), of dimension
   m+1 with m = n − |T| − 2. The vector (C−P_T)Y is fixed given (X_T, Y). So x_{T,l} ~ Beta(½, m/2) exactly,
   and x_{T,l} is independent of (X_T, Y). Standardising x_l does not change x.
4. **Truncated moment.** With x ~ Beta(½, m/2) and ν = n/2 + 0.01, the integrand is
   x^{−1/2}(1−x)^{m/2−1−ν} = x^{−1/2}(1−x)^{−|T|/2−2.01}: the exponential factors cancel exactly. For t_n ≤ ½,
   E[(1−x)^{−ν} 1{x ≤ t_n}] ≤ 2^{10.01} · 2√t_n / B(½, m/2) ≤ C h_n, using B(½, m/2) ~ √(2π/m).
   By linearity alone, E Ṽ_n ≤ C 2^B h_n. (Without truncation the moment is infinite, as W1 notes.)
5. **Truncation event.** P(x_{T,l} > t_n) ≤ P(χ²_1 > h_n²/2) + P(χ²_m < m/2) ≤ 2e^{−h_n²/4} + e^{−cm}.
   A union over ≤ p 2^B pairs gives probability → 0 for h_n² = 4(A+1) log n.
6. **EXP′ given X.** On SE_n = {SE-blk(φ0) on 𝒢} ∩ {‖μ‖² ≤ Mn} (P → 1), apply Theorem 1 conditionally on X.
   Its event E_n has P(E_n | X) ≥ 1 − ε_n with ε_n free of X (Lemma 1.4 uses only p 2^B and χ² tails). On
   P_n ∩ SE_n ∩ E_n ∩ {all x ≤ t_n}: u_n° = ũ_n ≤ (n+1)^{−1/2} e^{κ_EXP} Ṽ_n. Hence
   u_n° = O_P(2^B √(log n) n^{−1/2}).
7. **Completion term and aggregation.** VIS-lin(S°) holds w.p. → 1, because sample gains converge uniformly over
   ≤ G 2^B fixed-dimension projections (routine; not written out). Step 2 of Theorem 6 is a fixed-design
   argument given X and applies verbatim, giving e_n° = O_P(e^{−cn}). T22(i) with reference S° gives

       1 − π₀(S°) = O_P(2^B √(log n) n^{−1/2}).

This is part (a) of W1 §4.3, with the √(log n) factor. That factor is genuine here: the observed
√n(1 − π₀(S°)) stays in [2.5, 3.1], against a flat 1.6 in the exact-Gram case (`results/lh_iid.txt`, `lh_gram.txt`).
Part (b) follows as W1 states: δ_{∅, j_b} = O_P(1) by step 3's independence, and Theorems 3–4 apply conditionally on X.

**Why this does not extend to S3/S4/S6 at B ≥ 2g (stays a GAP).** With ⌊B/g⌋ ≥ 2 groups per block, which groups are
packed together depends on cross-group sample correlations. Those depend on x_l itself, so step 2 fails: no fixed
surrogate partition exists. A union over candidate blocks costs a factor ≍ (p/g)^{⌊B/g⌋−1}, which is polynomial in n
and destroys the rate. Step 3's Beta law does hold for every candidate T, so the only missing ingredient is
partition–noise decoupling. Possible routes: (i) a leave-one-column-out stability bound showing the packing is
unchanged w.p. 1 − o(p^{-1}) when x_l is replaced by an independent copy; (ii) a method change, building the partition
on a held-out row split. Route (ii) violates the "fixed method" premise and would need the investment rule.

---------------------------------------------------------------------------------------------------

## R4. Wording corrections to W1 (no mathematical content changes)

* §1.5: "All six study covariances have κ_17 ≥ 0.15" is **wrong for S6**. The ρ = 0.9 groups give
  λ_min = 0.1, as the same sentence then says. The correct statement is κ_17 ≥ 0.1. This is harmless.
* Thm 4: "masking persists **iff** η < 1/2.02, a sufficient condition" is self-contradictory. It should read
  "η < 1/2.02 suffices". Note also that p^{−c} → 0 alone gives π₀(S₀) → 0 when p → ∞, whatever η is.
* Limit law (§3): the constant Σ log((s+i+1)/2) is the p → ∞ form. At fixed p it is Σ log((s+i+1)p/(2p−s−i−1)),
  which is what W1's numerics use (log(3·16/29) and so on). State both.
* Thm 3 / H1: W1's H1 requires a **deterministic** chain, whereas T27(i)'s H1 allows data-measurable chains. Theorem 3's
  "Z_i exactly N(0,1)" needs the deterministic version (or a chain chosen independently of ε). This restriction
  should be stated where H2 is replaced.
* Headline 6 "SE-blk holds at the study size, so EXP′ (Thm 1) applies there": Theorem 1 is asymptotic, and its κ_EXP is
  ≈ 100+ nats at study SNR. Replace with R1: the certificate is ≤ 1.52 nats on study-like designs (S1–S6, c ∈ {0.5, 1, 4}).
* Config B (p = 20) is in the method's SMC branch only for n < 10,435. For n ≥ 10,435, N₀ = n makes
  (5H₀ + 4N₀)p ≥ 2^20, so the exact branch applies, and the n ∈ {102400, 1638400} rows are component-law values,
  as at p = 16. W1 states this for p ≤ 17 only.

---------------------------------------------------------------------------------------------------

## D. The start's masking at the study size is **dilution**, not cancellation and not "a few weak truths"

This concerns W1's escalation item 3 (a CONJECTURE). It is not a W1 theorem, but it decides how W1's headline 6 should be read.

**Proposition D (deterministic start-mass ceiling).** Status: **PROVED** (two lines from locked T22(ii-a)).
Let U ⊆ S₀ consist of truths that are each the only member of S₀ in their block, and let a = |U|. Then, for every data set,

    π₀(S₀) ≤ [w(s₀)/w(s₀ − a)] · ∏_{j∈U} BF({j}),     w(s₀)/w(s₀−a) = ∏_{i=1}^{a} (s₀−a+i)/(2p−s₀+a−i),

    BF({j}) = (H/n)^{−1/2} ((0.02 + Q_j)/(0.02 + n − 1))^{−ν},
    H = (n+1)(n−1)+1,   Q_j = (n−1)(1 − n(n−1) r_{jy}²/H).

*Proof.* Apply T22(ii-a) with S° = S₀∖U ∈ Ω. Every block meeting U has S₀ ∩ C_b = {j} and S° ∩ C_b = ∅, with ratio
r_b({j})/r_b(∅) = BF({j}). Every other block has ratio 1. Finally use π₀(S°) ≤ 1. The BF formula is m({j})/m(∅) with
G = n−1, z = (n−1) r_{jy}, D = H/n, and Q from the definition. ∎

**Consequence (dilution; PROOF SKETCH for the population limit).** BF({j}) depends only on the marginal correlation
r_{jy} with the **full** response. If the truths are independent with unit variance, as in S1, S3, S4 and S6 (one truth
per independent group), then r_{jy}² → θ_j²/v with v = σ² + Σ_k θ_k². The start therefore includes truth j only if,
roughly,

    (n/2) · log(1/(1 − θ_j²/v)) > log((2p − s₀)/s₀) + ½ log n.

As the signal scale c → ∞, θ_j²/v → θ_j²/Σθ_k², which is a fixed share. So at fixed n **no signal scale removes the
masking**: the per-truth evidence saturates. For the study truth pattern (s₀ = 14, p = 500), the predicted number of
visible truths is 7 of 14 at n = 200 for every c ∈ {0.5, 1, 4}. All 14 become visible by n ≈ 600.

**Evidence** (`scripts/study_exp.py`, `scripts/dilution_ceiling.py`, exact π₀ by capped convolution; exact iid
π₀ draws by the backward sampler):
* n = 200, S1/S3, c ∈ {0.5, 1}: log₁₀π₀(S₀) ∈ [−15.6, −9.0]. Exact π₀ draws contain a median of 2–8 of the 14 truths (1–9 over all six scenarios).
  The start mode misses 6–12 truths (5–13 over all six scenarios), including |θ| = 1.8, 1.6 and 1.4 truths. π₀(R₂) = 0.67–0.96 (0.13–0.996 over all six scenarios), which reproduces
  HQ's "π₀(S₀) ≈ 1e-12, π₀(R₂) ≈ 0.8". The mass sits on **small subsets** of S₀, which R_d counts as "near the truth"
  because R_d contains every subset of S₀.
* S3, p = 500, n = 200 / 400 / 800 / 1600: median log₁₀π₀(S₀) ≈ −10 / −3.3 / −0.8 / −0.3, identical at c = 1 and c = 4.
  The median draw has 3–7 / 10–11 / 13 / 14 truths. The favourable regime appears between n = 800 and n = 1600.
* Prop D's ceiling is ≥ the exact π₀(S₀) in all 26 designs where both were computed (S1/S3/S4/S6, c ∈ {0.5, 1},
  plus S3 at c = 4). It accounts for most of the deficit (ceiling 10^{-4.1} to 10^{-16.6}; exact 10^{-9} to 10^{-18.5}).
* S1 (Σ = I) behaves like S3, so **no correlation is needed** for the start to be masked at n = 200.

**What this says about W1.** (i) Headline 6's population claim stands. The favourable regime for S1/S3/S4/S6 does
appear in-sample, but only for n ≳ 2v log(2p/s₀)/θ_min² ≈ 600–1600, not at n = 200. (ii) The conjecture in
"Needs escalation 3" ("weak-signal masking … c = number of weak truths … π₀ concentrates on S₀ minus those") has the
wrong mechanism and the wrong size. The masked set is about half to most of S₀, strong truths included. The cause
is that block tables score against the full y, so each truth's per-block noise is v ≈ 25σ², not σ². The
parametrisation that matters is θ_j²/v, not θ_j²/σ²: VIS in T22(iii) already carries v_T, so the theory is consistent,
but its regime is not reached. (iii) "In that mechanism π(S₀) is also small": dilution does not act on the posterior,
whose residual variance with S₀ in the model is σ². I did not compute π at p = 500, so this part is untested here.
(iv) For T38(b): π₀(R_d) ≥ b_n is satisfied at n = 200, but by models that are 6–11 additions from S₀. "Near-truth" in
the R_d sense is then not near in Hamming distance, so a repair step must make many additions (ℓ = 10 < 11).
