# O-DILUTE: why π₀(S₀) is tiny but π₀(R_d) is large at n = 200

Run of 2026-11-02, branch `theory/O-DILUTE` (from `theory/campaign`), Opus 5.5, on Felipe's laptop (Python 3.12; R is
not available).
- Statements and proofs: `THEORY.md`.
- Scripts: `scripts/` (fixed seeds).
- Raw output: `results/study_*.jsonl`.
- Tables: `results/summary.txt`, `results/predict.txt`, `results/propS.txt`, `results/sanity.txt`.

Every proof here is a **candidate**: it has not been reviewed or adopted. Status words follow the campaign PROTOCOL.

## 1. Headline

1. **PROVED (exact, any data, any partition): a three-term account of the start's deficit.**
   - The identity: −log π₀(S₀) = V + C − log A.
     - V = Σ_b softplus(−λ_b) is the cost of truths that their own block's table does not see.
     - C ≥ 0 is the table mass on sub-models other than ∅ and S₀_b.
     - A is the non-product part of the BB(1, p) prior.
   - A rigorous ceiling: log π₀(S₀) ≤ −V − C + o(1).
   - The exact joint law of (#truths, #non-truths) under π₀, which gives π₀(R_d) and the Hamming-ball mass by a
     two-variable convolution.
   - On 480 regenerated study fits, V carries 83% of −log π₀(S₀), C carries 11% and the size term 6%.
2. **The mechanism is σ²-dilution of the truths' marginal statistics.**
   - Truth j's table log-odds are λ_j ≈ ½χ²₁(nρ_j²) − ½ log n − log(2p/s₀), with ρ_j² = (1 − κ_j)x_j (PROOF SKETCH).
   - The table's keep-j gain is therefore the posterior's gain scaled by log(1 − ρ_j²)/log(1 − x_j) = 0.05–0.20 (Lemma W2
     for truths). In-sample this agrees with the population value to ±0.01.
   - The share saturates in the signal scale: ρ_j² ≤ ω_j = θ_j²/‖θ‖².
   - About 7 of the 14 truths are invisible at n = 200 for every c. The start becomes favourable only at n ≈ 590–730.
3. **Why π₀(R_d) stays large (PROVED: Lemma N, Thm R).** In a Gaussian design, every null that is independent of y has
   r_ly² ~ Beta(½, (n−2)/2) exactly. The v3 table therefore scores nulls as in pure noise, and E_{π₀}[#extras] is about 1
   at every signal scale. R_d also contains every subset of S₀. So π₀(R_d) is large because the start sits on *small
   subsets* of S₀. The median start draw is 8–14 flips from S₀, and π₀(Hamming ≤ 2) has median 8·10⁻¹¹.
4. **Verification (480 fits, regenerated in Python, 20 replicates per cell).**
   - Pooled median π₀(R₂) = 0.79; study: ≈ 0.8.
   - Favourable fits: 0 of 480; study: 1 of 2,394.
   - Median π₀(S₀) = 10^{−15.7}, with per-cell medians from 10^{−11.1} to 10^{−25.6}; study: "≈ 10⁻¹² or smaller".
   - The design-level dilution formula predicts the per-cell median log₁₀π₀(S₀) within 0.1–1.3 in S1/S2/S5. In
     S3/S4 it underpredicts the deficit by 1.0–1.6, because it omits competition from proxies; in S6 it is within 0.8.
5. **A common plug-in σ² does not help: it makes the start worse (PROVED: Lemma L, Prop S; numerics).**
   - In-sample block orthogonality fails at n = 200. A common σ² inflates every null by v/σ² ≈ 7–25: with the oracle σ²
     the start fills to the cap K (median log₁₀π₀(S₀) = −690).
   - With a realistic plug-in, log₁₀π₀(S₀) = −18.8 (v3: −15.7) and π₀(R₂) falls to 0.
   - Prop S proves that **no** common σ² can beat a ranking ceiling of about 10^{−1}–10^{−5}.
   - A different change, **partial-residual (backfit) tables**, raised the median π₀(S₀) to 10^{−1.0} (378 of 480 fits
     favourable) in a pilot. This is outside the asked variant and flagged for HQ.

## 2. Statements (full text and proofs in `THEORY.md`)

| Label | Statement (short) | Hypotheses | Status |
|---|---|---|---|
| Thm E | π₀(S) = ∏_b π_b^t(S_b)·A_t(\|S\|) for every t > 0; at S₀, A_t(s₀) = 1/E_t[e^{g_t(N)}1{N≤K}] | any data, any partition, positive tables | PROVED |
| Cor E1 | −log π₀(S₀) = V_t (visibility, Σ softplus(−λ_b)) + C_t (competition) − log A_t (size) | as Thm E | PROVED |
| Cor E2 | t ∈ I₀ ⇒ log π₀(S₀) ≤ −V_t − C_t − log P_t(N ≤ K); sharpens W3-VEXP Prop D | as Thm E | PROVED |
| Thm R | exact joint law of (#truths, #non-truths) under π₀; π₀(R_d), π₀(B_d); Markov: π₀(R_d) ≥ 1 − E M/(d+1) | as Thm E | PROVED |
| Lemma N | a Gaussian null independent of y has r_ly² ~ Beta(½, (n−2)/2) exactly: the v3 table scores it as in pure noise, at every signal scale | x_l^r Gaussian and independent of (y, X_{−l}) | PROVED |
| Cor N1 | expected null inclusions under P_t = Θ(s₀√(log p)/√n) ≈ 1 at the study size | Lemma N | PROVED (expectation); PROOF SKETCH (constant) |
| Lemma L | a common σ² multiplies every null's exponent by v/σ̂²; with the oracle σ² the start fills to K; F-DRAFT's Lemma W1 needs **in-sample** BO, and the study has only **population** BO | Lemma N | PROVED (identity); PROOF SKETCH (extreme value) |
| Prop S | π₀(S₀) ≤ 1/∏_i(1 + [M_(i) − i + 1]₊) for the v3 tables **and every common σ²** | any data and partition | PROVED |
| Prop D′ | λ_j ≈ ½χ²₁(nρ_j²) − ½ log n − log((2p−s₀−1)/(s₀+1)), with ρ_j² = (1 − κ_j)x_j ≤ ω_j (saturating in c); the assembled formula for log π₀(S₀) | population BO, Gaussian design | PROOF SKETCH; numerically checked |
| Prop DM | the paper proposition (wording in THEORY §7) | (i)–(iii): any data; dilution clause: population BO | (i)–(iii) PROVED; dilution clause PROOF SKETCH |
| Conj DM-asy | s₀ = s_n → ∞ truths of comparable share, with n/(s_n log(pn)) → κ ∈ (0, ∞): the start-visible fraction converges to a limit in (0, 1); π₀(S₀) → 0 while π₀(R_d) stays bounded below | population BO | CONJECTURE |

## 3. The mechanism, quantified (task items 1–2)

**Exact objects (item 1).**
- Over the actual X-dependent blocks, π₀(S₀) = w(s₀)∏_b r_b(S₀_b)/Z̄₀.
- π₀(R_d) = Σ_{i, j≤d, i+j≤K} w(i+j)F_{ij}/Σ_{i+j≤K} w(i+j)F_{ij}, with F(u, v) = ∏_b Σ_{U⊆C_b} r_b(U)u^{|U∩S₀|}v^{|U∖S₀|}
  (Thm R). This is the §6.3 size convolution with one more counter. It is checked against brute force to 10⁻¹⁰
  (`results/sanity.txt`).
- Theorem E rewrites π₀(S₀) as a product of per-block probabilities times a size factor. This is the precise sense in
  which "14 truths spread over blocks multiply per-block deficits".

**The per-block deficit is dilution (Lemma W1/W2 in truth form).**
- For a truth j alone in its block, λ_j = log BF₁(r_jy²) + log t: a closed form in the **marginal** correlation with the
  full y.
- Its population value is ρ_j² = θ_j²/v = (1 − κ_j)·x_j. Here x_j is the posterior's partial R² (the keep-j statistic
  with S₀∖j in the model), and κ_j = Σ_{k≠j}θ_k²/v is the dilution fraction. So the table rewards j with the posterior's
  gain shrunk from −ν log(1 − x_j) to −ν log(1 − (1−κ_j)x_j).
- Table 2 of `summary.txt` compares this ratio on the data (in-sample medians, truths alone in their block):

| c | β | table keep-j log-odds LO₀ (median; fraction > 0) | posterior LO₁ (median; fraction > 0) | in-sample gain ratio | population log(1−ρ²)/log(1−x) |
|---|---|---|---|---|---|
| 1 | 1.8 | 6.1; 0.92 | 127.6; 1.00 | 0.099 | 0.094 |
| 1 | 1.4 | 0.7; 0.59 | 93.4; 1.00 | 0.079 | 0.073 |
| 1 | −1.0 | −3.4; 0.14 | 56.3; 1.00 | 0.060 | 0.057 |
| 1 | 0.8 | −4.7; 0.04 | 37.5; 1.00 | 0.062 | 0.051 |
| 0.5 | 1.8 | 4.6; 0.90 | 51.2; 1.00 | 0.204 | 0.202 |
| 0.5 | 1.4 | −0.2; 0.49 | 31.5; 1.00 | 0.184 | 0.178 |
| 0.5 | −1.0 | −3.8; 0.11 | 15.1; 1.00 | 0.157 | 0.159 |
| 0.5 | 0.8 | −4.9; 0.04 | 7.0; 0.96 | 0.175 | 0.152 |

- The posterior keeps every truth by 7–128 nats. The diluted table keeps only the three strongest coefficient types
  (1.8, 1.6, 1.4) with probability > ½ at c = 1, and only two at c = 0.5.
- **The signal scale does not matter.** At c = 1 the table sees 6–10% of the posterior gain, and at c = 0.5 it sees
  16–20%. The posterior gain grows with c while the share is fixed.
- The c → ∞ ceiling (`predict.txt`) is λ_j^∞ = log BF₁(ω_j) + log t. For p = 500 this is {1.4, −2.7, 7.2, −0.8, −4.2,
  4.1} for β = (1.4, −1.0, 1.8, −1.2, 0.8, −1.6): 7 of 14 truths stay invisible at *every* scale, and
  Σ softplus(−λ^∞) = 19.9 nats (10^{−8.6}) before competition and the size term.
- **Weak truths at c = 0.5.** The 0.8 coefficient (θ = 0.4) has table log-odds −4.9 and is visible in only 4% of fits.
  The posterior keeps it in 96%. It is the worst case, but it is not special. The 1.0 and 1.2 coefficients are masked
  in 67–89% of fits at both scales, and even the 1.4 coefficient is masked half the time.

**A finite-n formula for log π₀(S₀) (Prop D′ + Cor E1).**

    log π₀(S₀) ≈ −Σ_{j∈S₀} softplus(log((2p−s₀−1)/(s₀+1)) + ½ log n − ½W_j) − Σ_{nulls} log(1 + t BF₁(r_ly²)) + log A_t,
    W_j ≈ χ²₁(nρ_j²) independent,  r_ly² ~ Beta(½, (n−2)/2),  t = (s₀+1)/(2p−s₀−1).

Its design-level medians (`predict.txt`, Monte Carlo over W and the null laws) against the exact per-cell medians
(log₁₀):

| p | c | S1 pred / exact | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|---|
| 500 | 1 | −12.4 / −11.1 | −12.4 / −11.7 | −12.2 / −13.5 | −12.2 / −13.8 | −19.7 / −20.7 | −12.4 / −12.9 |
| 500 | 0.5 | −14.0 / −12.9 | −14.2 / −13.4 | −14.2 / −15.1 | −14.2 / −15.3 | −21.8 / −22.8 | −14.4 / −15.2 |
| 1000 | 1 | −14.9 / −14.8 | −14.9 / −15.9 | −14.9 / −16.1 | −14.7 / −16.0 | −23.0 / −23.3 | −14.6 / −14.9 |
| 1000 | 0.5 | −16.8 / −16.5 | −17.1 / −17.4 | −16.9 / −18.2 | −16.9 / −17.9 | −25.3 / −25.6 | −16.8 / −16.5 |

- The formula has no free parameter and uses only the population (Σ, θ, σ²).
- In S5 the equicorrelation lowers ρ_j for the negative-β truths (Σθ mixes signs); the formula captures this.
- The 1.0–1.6 order miss in S3/S4 is the proxy competition: C is 3.5–8.0 nats there, against 1.5 predicted.

**T27 bracket (Table 4).** Over the invisible blocks, T27(i)'s complete-masking rate per masked truth,
log(2p/s₀) + ½ log n, overstates −V by 24–37 nats per fit, which is about 3.5 nats per masked truth (c_eff = 7–10.5). That
excess is Σ ½W_j, the residual visibility that dilution leaves and cancellation does not.

## 4. Verification on regenerated study datasets (task item 3)

**Data.** R is not on the laptop, so `scripts/dilute.py` reimplements `gen_prod_data.R` in law:
- Σ for S1–S6, the truth pattern and positions, X standardised with sd (n − 1), ε ~ N(0, 1), y = c·Xβ + ε.
- The datasets are not bit-identical to the study files, because numpy's RNG is used.
- 20 replicates per (p, S); c ∈ {1, 0.5}; 480 fits.

**Method port.** The method is ported from METHODOLOGY §§5, 6.3 and `v3_blocks.h`:
- complete linkage on 1 − |r| (scipy), with the R13 left-child rule;
- the left-first top-down cut and next-fit packing;
- B = 14, K = 100, the exact score, and the BB(1, p) size prior with cap.

**Results** (`summary.txt` Table 1; medians):

| quantity | study (HQ, ANALYSIS-H2 working tables) | here (480 fits) |
|---|---|---|
| favourable fits (Q_f·π₀(S₀) ≥ 1, Q_f = 10⁴) | 1 / 2,394 | 0 / 480 |
| median π₀(S₀) | ≈ 10⁻¹² "or smaller" (per cell) | 10^{−15.7} pooled; per cell 10^{−11.1} (p500 S1 c1) to 10^{−25.6} (p1000 S5 c0.5) |
| median π₀(R₂) | ≈ 0.8 | 0.794 pooled; per cell 0.20 (p500 S4 c1) to 0.96 (p1000 S1 c0.5) |
| median π₀(R₁) | — | 0.52 |
| median π₀(Hamming ≤ 2) | — | 8·10⁻¹¹ |
| E[#truths], E[#extras] in a start draw | — | 2.4–6.6 and 0.7–3.8 per cell |
| E\|S Δ S₀\| | — | 8.3–14.2 per cell |
| start mode: truths / size | — | 2.5–6 of 14 / 3–7 |

- The start does not "almost find" S₀. It finds a third of S₀, plus about one extra.
- π₀(R₂) is low only in S4 (0.20–0.37), and lower in S3/S6, because the S4 tables keep proxies (r = 0.85 with a truth)
  with or instead of the truth, and R_d counts these as extras.
- d(S₀) is about 105 nats at c = 0.5 and about 210 at c = 1: Θ(n·R²), as F-DRAFT says. But it is not the W1 BO formula:
  that formula is undefined (Σ_b ξ_b ≥ 1) in 132 of 480 fits and off by a median of 57 nats elsewhere. In-sample
  cross-block terms are first-order (Lemma L(c)).

## 5. The common-plug-in-σ² variant (task item 4; pilot evidence only, no method change decided)

These tables use the same partition and keep exact product form, so Prop P(i) (F-DRAFT) covers validity. Variants:
- `known_oracle`: r_b(U) = D_U^{−1/2}exp(t_U/(2σ̂²)), with the true σ² on the standardised scale (median σ̂² = 0.086).
- `known_mode1`: σ̂² = RSS(v3 start mode)/(n − 1 − |mode|) (median 0.50).
- `known_iter`: that plug-in iterated to a fixed point (median 0.13).
- `resid` (not asked; added as a diagnostic): v3 tables on partial residuals y − X_{−b}β̂_{−b}, with β̂ the OLS fit of the
  current start mode, for 3 sweeps.

| variant | median log₁₀π₀(S₀) | median π₀(R₂) | median π₀(Ham ≤ 2) | favourable (of 480) | start mode |
|---|---|---|---|---|---|
| v3 (method) | −15.7 | 0.79 | 8·10⁻¹¹ | 0 | 2.5–6 truths, ≈ 1 extra |
| known_oracle | −690 | 0.00 | 0 | 0 | 8–14 truths + 86–90 nulls (cap K = 100) |
| known_mode1 | −18.8 | 0.00 | 5·10⁻¹⁴ | 0 | 3–12 truths; E[#extras] 3–37 |
| known_iter | −363 | 0.00 | 0 | 0 | to the cap except in S5 |
| resid (backfit) | −1.0 | 0.71 | 0.60 | 378 | 14/14 in most cells; S5 and S4 at c = 0.5 weaker |

**Why the common σ² fails (Lemma L, Prop S).**
- F-DRAFT's Lemma W1 ("with known σ², π₀ = π") assumes X_{C_b}ᵀX_{C_b′} = 0 *in sample*. The study's designs are
  block-orthogonal only *in population*.
- For a null l, x_lᵀX_{−b}θ_{−b}/√(n−1) ~ N(0, ‖θ_{−b}‖²). The out-of-block signal leaks into every block's statistic with
  exactly the variance that the v3 table "dilutes" by.
- The v3 integration is therefore the correct calibration for nulls (Lemma N: exact pure-noise law). A common σ̂² < v
  over-rewards every null by v/σ̂², which is about 25 at c = 1 for the oracle.
- A common σ² rescales truths and nulls alike, so it cannot change their ranking. Prop S bounds π₀(S₀) for **every** σ²
  by a ranking count. Its per-cell median is 10^{−0.8}–10^{−4.8} (10^{−6.7}–10^{−10.6} in S5; `propS.txt`). The marginal
  statistics of the weak truths are already exceeded by the best null of 10–100 truth-free blocks.

**Verdict.** The common plug-in σ² variant would **not** raise π₀(S₀). It lowers it by 3 orders with a realistic plug-in
and by hundreds of orders with the oracle, and it destroys π₀(R_d). Do not adopt it.

The backfit variant attacks the actual cause, which is the *unexplained* out-of-block signal. In the pilot it moves 79% of
fits into the favourable regime. It is not a decided method change, and it needs its own validity and cost check (§9).

## 6. Paper proposition and connections (task item 5)

**Proposition DM (start masking by σ²-dilution at finite n).** The full wording is THEORY §7. In short:
- (i) The exact deficit decomposition −log π₀(S₀) = V + C − log A, and the ceiling log π₀(S₀) ≤ −V − C + o(1).
- (ii) The ranking ceiling, valid for the v3 tables and for any common σ².
- (iii) The exact near-truth mass π₀(R_d) = P(M ≤ d) ≥ 1 − E M/(d+1).
- The dilution clause: in population-BO Gaussian designs, λ_j ≈ ½χ²₁(nρ_j²) − ½ log n − log(2p/s₀) with ρ_j² = (1−κ_j)x_j,
  which saturates in the signal scale, while nulls keep their exact pure-noise law.
- "At the study's n = 200, about half of S₀ is invisible to its block (V ≈ 20–50 nats), while E M ≈ 1. Hence π₀(S₀) ≈
  10^{−11}–10^{−26} but π₀(R₂) has median 0.79. The start is masked by σ²-dilution, and its mass sits on subsets of S₀.
  This is the regime that T38(b) addresses."
- Status: (i)–(iii) PROVED; the dilution clause PROOF SKETCH, numerically verified.

**Connection to T27.** The λ framework puts the three start regimes on one axis, W_j (the noncentral χ² of the truth's
marginal statistic in its block):
- **Favourable** (T22(iii)): every W_j ≫ 2 log(2p/s₀) + log n.
- **Cancellation masking** (T27(i), LH): W_j = O_P(1), central, because the block sees ρ_j = 0. Each masked truth costs
  log(2p/s₀) + ½ log n, which is T27's p^{−1}n^{−1/2}, and the O_P(1) remainder is ½W_j.
- **Dilution masking** (this report): W_j ≈ nρ_j² is of the same order as the threshold. The T27 rate applies per masked
  truth minus ½W_j, which is about 3.5 nats per masked truth at the study size (§3, Table 4). This is why W3-PXN found
  that T27's rate overshoots the study numbers. Borderline truths (|λ_j| ≲ 2) also contribute softplus terms of order 1
  rather than all-or-nothing.

**Connection to W3-PXN's LH-iid family.**
- LH-iid is the fixed-s₀ cancellation family: its masked hubs have exact central Beta laws (W3-PXN Lemma B, the same
  mechanism as our Lemma N).
- Its visible groups are diluted too. But with fixed s₀ and BM-∞, nρ_h² grows linearly, so dilution disappears
  asymptotically and only the cancellation masking survives (W3-PXN Prop W).
- Dilution masking needs n·ω_min ≍ log(pn). The asymptotic home of the study's regime is therefore a growing-s₀ (or
  local-alternative) family, not LH-iid (Conj DM-asy; W3-PXN W′).
- For T38(b), both families supply π₀(R_d) ≥ b_n, but by different routes:
  - LH-iid has the reference S° = S₀∖M at Hamming distance c, so LS0 repairs in c moves.
  - Dilution has the start mass on subsets S₀∖V that are |V| ≈ 7–10 additions away (median E|SΔS₀| = 8–14). The local
    search budget ℓ = 10–11 is borderline. This agrees with HQ's finding that delivery comes from Gibbs flips, not the
    local search.
- T38(b)'s eligibility premise "π₀(R_d) ≥ b_n" therefore holds at the study size (Thm R + Lemma N). Its repair half must be
  an addition-path (T24/Gibbs-type) argument with |S₀ ∖ S| ≈ s₀/2, not a d-local one.

## 7. What fails and why

- **The common plug-in σ² route (F-DRAFT candidate):** it fails for the reasons in §5. Lemma W1's premise (in-sample BO)
  is false at every finite n in Gaussian designs: the cross-block Gram entries are O_P(n^{−1/2}) but multiply Θ(n)
  signal.
- **Using F-DRAFT's d(S₀) BO formula as a finite-n predictor:** it is undefined in 28% of fits and off by about 57 nats
  otherwise. d(S₀) is the wrong object anyway: π₀(S₀) depends on d only through E_{π₀}e^d, and the per-block account
  (Thm E) is what predicts π₀(S₀).
- **Predicting S3/S4 with single-variable λ_j only:** it misses the proxy competition (C is 2–6.5 nats above
  prediction). A two-variable block formula (truth plus 4 equicorrelated proxies) would close this. It is not done here.
- **Prop S as an explanation of the 10⁻¹⁵ level:** it is not one. It is only a ranking ceiling (10^{−1}–10^{−5}); the
  depth comes from V (Thm E).
- **An earlier claim in this run:** Prop S's numbers were first written as "10^{−3}–10^{−6}" before the run; they are
  corrected to the computed 10^{−0.8}–10^{−4.8}.

## 8. Needs escalation

1. **Prop D′(a)–(d)** (PROOF SKETCH). A sharp statement needs the joint law of (λ_b) across blocks with the in-sample
   cross-block leakage, and a uniform treatment of the BB-size coupling. This is a candidate for a stronger prover if the
   paper states the dilution clause as a theorem rather than as a remark with numerics.
2. **Lemma L(b)** extreme-value step (the known-σ² start fills to the cap). This is routine, but it needs writing.
3. **Conj DM-asy** (the growing-s₀ dilution family). It would give the study regime an asymptotic home. It is open.
4. **Independent check of the port.** The partition uses scipy's complete linkage instead of the engine's R13 tie order
   (ties have measure zero for continuous data), and the datasets are equal in law to the study's, not bit-identical. A
   bit-exact check on the stored study `.rds` files with the R engine would confirm the per-cell medians. The study's own
   per-fit π₀ values were not available locally.

## 9. Outside scope

- **Backfit (partial-residual) tables.**
  - Median π₀(S₀) went from 10^{−15.7} to 10^{−1.0} (378/480 favourable), with π₀(R₂) 0.71 and π₀(Ham ≤ 2) 0.60.
  - It is weak in S5 (global equicorrelation 0.3; 10^{−4.6} to 10^{−19}) and in S4 at c = 0.5.
  - Cost: (sweeps + 1) × the §6.3 table work.
  - Validity: tables are still positive and product-form, functions of (X, y) and a deterministic pilot, so F-DRAFT
    Prop P(i) applies. The locked T22(ii-a) and (iv) are identities for any positive tables. T22(iii)'s regime
    conditions would need restating.
  - This is a candidate method change under the investment rule; it needs HQ's and Felipe's call and a pilot of the full
    sampler.
- **F-DRAFT's Theorem W.** It is stated under BO with diluted *null* exponent (1 − κ)Z²/2. In population-BO Gaussian
  designs the null exponent is Z²/2 exactly (Lemma N), so W's p^{R²} factor would change. Its premises should say
  "in-sample BO" explicitly.
- **R_d as a near-truth notion.** π₀(R_d) is dominated by subsets of S₀ far from S₀ in Hamming distance. Reporting
  π₀(B_d) alongside π₀(R_d) in the paper would avoid overstating "near".

## 10. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change needed? |
|---|---|---|---|---|---|
| Thm E / Cor E1–E2 / Thm R | exact per-block factorisation of π₀(S₀); ceiling; exact π₀(R_d), π₀(B_d) | high | done (PROVED; elementary) | none | no |
| Lemma N, Prop S | exact null calibration; ranking ceiling for any common σ² | high | done (PROVED) | none | no |
| Prop D′ / dilution clause of DM | λ_j ≈ ½χ²₁(nρ_j²) − ½ log n − log(2p/s₀), ρ_j² = (1−κ_j)x_j ≤ ω_j; 7/14 invisible at n = 200 for all c | high (numerics within 0.1–1.3 log₁₀ in S1/S2/S5) | medium (joint law across blocks; BB coupling) | in-sample cross-block leakage in the joint law | no |
| Paper Prop DM ("masked by σ²-dilution; T38(b) regime") | as §6 | high | high for (i)–(iii), medium for the dilution clause | as above | no |
| Common plug-in σ² improves the start (F-DRAFT candidate) | **false** at the study size (Lemma L, Prop S, 0/480 favourable, π₀(R₂) → 0) | high that it is false | — | in-sample vs population BO | reject the change |
| Backfit tables make the start favourable | pilot: 378/480 favourable | medium (pilot only; S5 weak) | unknown | stability of the pilot fit; T22(iii) restatement | would be one (not decided) |
| Conj DM-asy | growing-s₀ dilution family | medium | low–medium | sharp joint extreme values | no |
