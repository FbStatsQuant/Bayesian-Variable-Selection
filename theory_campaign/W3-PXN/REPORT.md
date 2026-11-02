# W3-PXN — REPORT: a p ≫ n family that carries all of T38(b)'s premises jointly

Run of 2026-11-02, branch `theory/W3-PXN`. Proofs: `PROOF.md`. Scripts: `scripts/` (fixed seeds in each file). Raw
results: `results/*.jsonl`. Tables: `results/summary.txt`, `results/check_*.txt`. Every result is a **candidate pending
cross-family review**. Status words never upgraded.

## 1. Headline

1. **PROVED (candidate), one p ≫ n family that carries every premise jointly.** The family is LH-iid. Its rows are iid
   Gaussian with W1-EXP's linked-hub correlation: equicorrelated groups of size g, with 9 ≤ g ≤ 16 so that g ≤ B < 2g. c
   linked pairs carry a suppressor coefficient, some groups are visible and the rest are null. The dimension satisfies
   n^a ≤ p ≤ n^A, so p ≫ n is allowed. On the actual X-dependent partition, with probability → 1, the family satisfies:
   - blocks = groups;
   - G, R, the locked SE, SE-blk and W1-T03R's anchored SE;
   - BM-∞;
   - near-truth start mass 1 − π₀(S°) = O_P(√(log n/n));
   - T27 masking with an exact limit law, log π₀(S₀) + c log p + (c/2)log n →_d Σ log((s+i)/2) + ½χ²_c;
   - S̃₀ = S°;
   - the TD′ lattice condition of W1-T37R Thm A at S̃₀, so LS0 scores and certifies S₀ in c moves (scoring rests on
     Θ(n) margins; certification rests on the slow (L) margin, which fails with probability ≈
     (s₀+1)/√(2π(n+1)t_n), about 1% at n = 1600);
   - π(S₀) → 1.

   T38(b) (W1-T38E composition) therefore holds on this family through route (b1), the LS0 tweak, for every fixed c.
2. **The no-tweak route works for one masked variable.** For c = 1 the original method scores S₀ in the first pilot round
   (route D2). The hypotheses D2-a, D2-b and D2-c, including Dep = O_P(√(log n/n)), are PROVED; D2-d (NB) is a PROOF
   SKETCH. For c ≥ 2 the no-tweak route stays OPEN, because it needs delivery (b2).
3. **The partition limits masking (PROOF SKETCH).** When a linked unit fits in half a block (2g ≤ B, e.g. the study's
   groups of 5), complete linkage puts the cancelling variables in one block and the masking disappears. Cancellation
   masking therefore survives the method's own partition only for units larger than B/2.
4. **The study's n = 200 masking is not the masking of T27/LH.** It is *dilution masking*: the start's block view treats
   the other 13 truths' signal as noise (v_T ≈ 7–26σ²). The masked truths have L² = δ²/σ² ≈ 50–200, not O(1). The
   CL(L) rate overshoots log₁₀π₀(S₀) by 17–29, and the effect is scale-free and gone by n ≈ 1600. W1-EXP's "weak-signal
   masking" is right only in the block-SNR sense, and its "bounded L" version is rejected (numerics, §5). Under the frozen
   setting (s₀ fixed, BM-∞) dilution vanishes, so **no fixed-s₀ BM-∞ theorem describes the n = 200 numbers**
   (Proposition W, PROOF SKETCH).

## 2. Statements (full proofs in PROOF.md; section numbers refer there)

**Family LH-iid (PROOF §0).** The fixed parameters are:
- g, c ≥ 1, v ≥ 0, and ρ ∈ (0,1);
- 0 < |ψ_i| < ρ, and nonzero β_i, β^vis_h;
- σ² > 0, and 1 ≤ a ≤ A.

The design has p = Gg with n^a ≤ p ≤ n^A, and g ≤ B_n < 2g eventually, i.e. 9 ≤ g ≤ 16. Rows are iid N(0, Σ_LH) and
ε ~ N(0, σ²I) is independent of the rows. The truth is θ_{j_a} = β, θ_{j_b} = −ψβ and θ_{j_h} = β^vis_h. Write
S° = S₀∖M with M the masked hubs, s = |S°| = c + v, and s₀ = s + c. Regime R1, with s₀ fixed.

| # | Statement | Hypotheses beyond LH-iid | Status |
|---|---|---|---|
| P1 | The v3 partition equals the groups w.p. → 1 | Gaussian correlation concentration (cited, Lemma C1) | PROVED |
| P2 | G; R; locked SE at size m_n + s₀; SE-blk; SE_λ(j₀), SE_w(m♯; g₀); BM-∞, all w.p. → 1 | C1 | PROVED |
| B | Exact Beta laws: X_{h,V} ~ Beta(\|V\|/2, (n−1−\|U°\|−\|V\|)/2); neutral x_{A,l} ~ Beta(½, ·); masked hubs independent of y | — | PROVED |
| P3 | q = O_P(√(log n/n)), e = O_P(p√n e^{−c₆n}), so **1 − π₀(S°) = O_P(√(log n/n))** and b_n := π₀(𝓡_d) ≥ π₀(S°) → 1 | W1-EXP Thm 1 (EXP′), locked T22(i) | PROVED |
| P4 | **Mstat_n →_d Σ_{i≤c}log((s+i)/2) + ½χ²_c**; hence π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, and T27's H1–H3 hold with CL(L), L = O_P(1) | locked T22(ii-a), P3 | PROVED |
| P5 | S̃₀ = S° w.p. → 1 (eligibility for LS0) | P3 | PROVED |
| P6 | TD′ lattice condition at S°: (L) and D_S for all S ∈ Lat(S°)∖S₀ w.p. → 1, so LS0 returns S₀ certified in c ≤ ℓ_n moves | W1-EXP Lemmas 1.1, 1.2, 1.4 (general-set form), W1-T37R Thm A(A3) | PROVED |
| P7 | D2 with x° = S°, 𝒟 = C_b∖j_b, b = ½ (c = 1): D2-a, b, c PROVED (Dep = O_P(√(log n/n))); D2-d (NB) PROOF SKETCH; so P(S₀ ∉ 𝒮_cal) → 0 | EX-A, EX-S, SR, W1-T38E D2 | PROVED / PROOF SKETCH |
| P8 | 1 − π(S₀) = O_P(√(log n/n)) | locked T03, plus a design de-randomisation lemma (PROVED) | PROVED |
| Cor | liminf P(Uᶜ, Ŝ⁺ = S₀) ≥ 1 − limsup P(U): via LS0 for all c; via the original method for c = 1 | the above, plus W1-T38E T38(b)-R | PROVED (b1); PROVED modulo NB sketch (b1′) |
| Q | If 2g ≤ B, linked pairs are co-blocked and LH masking disappears | — | PROOF SKETCH |
| W | Dilution: LO₀(j) = −log((2p−s₀)/s₀) − ½log(n+1) + (n/2)θ_j²Var(x_j\|X_T)/v_T(1+o_P(1)); under s₀ fixed + BM-∞ every block-orthogonal family is favourable | block-orthogonal population | PROOF SKETCH |
| W′ | A fixed-s₀ dilution family (local alternatives in the window (1+2A) < κ < (1+2A)v_T/σ²) has π₀(S₀) → 0 with LO₁ → ∞ | — | CONJECTURE (π(S₀) → 1 needs a sharp-constant T03) |

**The key new argument (P3).** In LH-iid every quantity the start law needs at the reference S° has an *exact* Beta law
that is independent of the response. This holds for null, neutral and masked-group subsets alike (Lemma B), because of
the population identities Cov(X_V, μ | X_{U°}) = 0. EXP′ turns each block ratio into
(n+1)^{−j/2}e^{O(1)}(1 − X)^{−ν}. The truncated moment E[(1−X)^{−ν}1{X ≤ τ}] ≤ 2^{e₁}(mτ/2)^{j/2}/Γ(j/2+1)
(Lemma Tr) then bounds every a_bj. Truncation is essential, since E(1−X)^{−ν} = ∞. Jensen applied to (j!a_bj)^{1/j}
gives E[q1_𝒢] = O(√(log n/n)), and locked T22(i) concludes. No NL_η, VIS-lin or exact-zero-leakage hypothesis is
needed. This closes W1-EXP's §4.3 PROOF SKETCH, and it does so at p ≫ n with a better rate.

## 3. Proofs or sketches

All are in `PROOF.md` §§0–14. The cruxes:
- P3: Lemma B (independence through F1–F3) and Lemma Tr.
- P6: the component decomposition of the population residual λ (Lemma Λ) and the margin table in §9.3. Every
  non-progress neighbour of a lattice state exceeds the best progress move by a fixed amount c₂ > 0. The (L) part at S₀
  uses max_l Z_l² ≤ 2log p + 2log log n against −½log n − log 2p.
- P7 (NB): three bad sets of initial draws, each with H₀·π₀ → 0, and d varying by only O(log n) on the good set,
  against a threshold of order log²n.

## 4. Evidence: LH-iid (exact start law by convolution; `scripts/lh_iid.py`)

The configurations are as follows.
- **A:** c = 1. One linked pair (β = 1, ψ = 0.5) and one visible group (β = 1); ρ = 0.7 (S3-like), g = 10.
- **B:** c = 2. Pairs with β = ±1, plus one visible group.
- **P:** config A at n = 200 with p ∈ {500, 1000, 2000, 4000}.

p ≈ n^{1.25} in A and B. Everything is computed exactly:
- the full v3 partition (scipy complete linkage + R13 left-child rule + top-down cut + next-fit; when p > 4300 the
  sufficient margin condition of Lemma P1 is checked instead);
- all block tables, π₀ by convolution, π₀(𝓡_d) by bivariate convolution, and the start mode by max-plus convolution;
- iid π₀ draws by the backward sampler, and the production local search from S̃₀;
- D2's Dep, and NB over the H₀ draws.

The library is checked against brute-force enumeration in `results/sanity.txt` (agreement to 1e-15).

Columns:
- **b=g:** blocks = groups (actual partition; at p > 4300, the margin condition of Lemma P1).
- **SE-blk:** min_b λ_min(R_{C_b}).
- **√(n/log n)(1−π₀(S°)):** median.
- **pi0(R0), pi0(R2):** medians.
- **mode=S°, LS0 cert/scored:** counts. LS0 cert = ends at S₀ certified; scored = S₀ scored.
- **F(S₀)−F(S°):** median.
- **Dep:** median, c = 1 only.
- **NB:** number of replicates where NB holds; d-range is the median, against the threshold 655.

| cfg | n | p | reps | b=g | SE-blk | med log₁₀π₀(S₀) | Mstat q05/med/q95 (limit) | √(n/log n)(1−π₀(S°)) | π₀(𝓡₀) | π₀(𝓡₂) | mode=S° | med q | T22(i) bound ≤ π₀(S°) | LS0 cert / scored | F(S₀)−F(S°) | Dep | NB (d-range) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A (c=1) | 200 | 750 | 20 | 20/20 | 0.147 | −3.91 | −1.59/0.26/2.55 (0.41/0.63/2.33) | 1.83 | 0.70 | 0.990 | 17/20 | 0.227 | 20/20 | 17/20 / 20/20 | 10.3 | 0.459 | 20/20 (10.2) |
| A | 400 | 1790 | 20 | 20/20 | 0.176 | −4.38 | 0.01/0.40/1.41 | 2.01 | 0.75 | 0.995 | 20/20 | 0.196 | 20/20 | 20/20 / 20/20 | 22.7 | 0.399 | 20/20 (10.7) |
| A | 800 | 4260 | 12 | 12/12 | 0.204 | −4.97 | −0.25/0.25/0.70 | 2.00 | 0.82 | 0.998 | 12/12 | 0.140 | 12/12 | 12/12 / 12/12 | 53.1 | 0.307 | 12/12 (10.2) |
| A | 1600 | 10120 | 6 | 6/6 (margin) | 0.230 | −5.06 | 0.63/1.27/2.46 | 1.71 | 0.88 | 0.999 | 6/6 | 0.089 | 6/6 | 6/6 / 6/6 | 121.3 | 0.186 | 6/6 (10.6) |
| B (c=2) | 200 | 750 | 20 | 20/20 | 0.144 | −7.37 | −0.44/1.58/3.50 (1.66/2.30/4.61) | 2.59 | 0.65 | 0.984 | 16/20 | 0.206 | 20/20 | 16/20 / 19/20 | 17.7 | – | 20/20 (26.1) |
| B | 400 | 1790 | 20 | 20/20 | 0.182 | −8.36 | 1.30/1.73/3.92 | 2.39 | 0.71 | 0.992 | 20/20 | 0.182 | 20/20 | 20/20 / 20/20 | 43.3 | – | 20/20 (19.4) |
| B | 800 | 4260 | 12 | 12/12 | 0.210 | −9.27 | 1.42/2.06/3.92 | 2.28 | 0.79 | 0.997 | 12/12 | 0.125 | 12/12 | 12/12 / 12/12 | 101.3 | – | 12/12 (12.9) |
| B | 1600 | 10120 | 6 | 6/6 (margin) | 0.232 | −9.95 | 1.53/2.92/3.85 | 2.07 | 0.86 | 0.999 | 6/6 | 0.081 | 6/6 | 5/6 / 6/6 | 224.6 | – | 6/6 (38.9) |
| P (c=1) | 200 | 500 | 20 | 20/20 | 0.148 | −3.69 | −0.10/0.36/1.74 | 1.50 | 0.76 | 0.995 | 20/20 | 0.189 | 20/20 | 17/20 / 20/20 | 6.1 | 0.434 | 20/20 (13.5) |
| P | 200 | 1000 | 20 | 20/20 | 0.146 | −4.04 | −0.08/0.25/0.82 | 1.68 | 0.73 | 0.992 | 19/20 | 0.219 | 20/20 | 20/20 / 20/20 | 10.2 | 0.442 | 20/20 (12.8) |
| P | 200 | 2000 | 20 | 20/20 | 0.136 | −4.37 | −1.09/0.20/1.16 | 1.78 | 0.71 | 0.990 | 17/20 | 0.233 | 20/20 | 18/20 / 20/20 | 7.2 | 0.540 | 20/20 (11.6) |
| P | 200 | 4000 | 10 | 10/10 | 0.144 | −4.67 | −0.70/0.20/1.83 | 2.51 | 0.59 | 0.980 | 9/10 | 0.291 | 10/10 | 8/10 / 10/10 | 1.7 | 0.621 | 10/10 (15.3) |

Reading:
- **Masking rate.** log₁₀π₀(S₀) falls by (c/2)log₁₀2 + c·log₁₀(p ratio) per doubling of n. With p ∝ n^{1.25} that is a
  predicted −0.52 (A) and −1.05 (B) per doubling; observed −0.47, −0.59, −0.09 (A, noisy at 6 reps) and −0.99, −0.91,
  −0.68 (B). At fixed n = 200, Mstat is flat in p ∈ [500, 4000] (P), so the c·log p scaling is exact.
- **Near-truth mass.** q decreases like √(log n/n), and the T22(i) lower bound held in 186/186 replicates.
  π₀(𝓡₂) → 1 and π₀(𝓡₀) = π₀(S°) → 1 at the slow √(log n/n) rate. Dep → 0.
- **Eligibility and repair.** S̃₀ = S° in 174/186 replicates, and in all of them at n ≥ 400. LS0 *scored* S₀ in 185/186
  (the exception is a B, n = 200 replicate whose mode was {proxy of j_a} instead of j_a). The certified-end failures are
  finite-n failures of (L) (S₀ + null beats S₀; PROOF §9.3 remark) or, at n = 200, proxy-for-hub substitutions, a D_S
  failure at a finite-n margin.
- **NB.** The d-range is ≈ 10–40 nats against the 655-nat threshold.

Checks (`results/check_lemmas.txt`, `results/check_mstat.txt`):
- **Lemma B:** KS tests of six exact Beta laws (a-group neutral, visible neutral and null additions given S°;
  |V| = 2 block statistics in a null group and in the masked group; the masked hub). All p-values are in [0.17, 0.62]
  (400 reps each).
- **Theorem P4:** T_n = Mstat − log π₀(S°) − prior term matches its exact finite-n law in every configuration (PIT KS
  p = 0.85 for A, 0.43 for B, 0.89 for P). The slow approach of Mstat to its limit comes *only* from log π₀(S°).
- **Theorem P6 margins:** an exhaustive population check over 81 parameter settings (c ∈ {1,2,3}, ρ ∈ {.4,.7,.85},
  ψ up to ρ − .05, β ∈ {.5,1,2}). The smallest D_S margin is 0.0027 > 0 and the smallest (L) margin is 0.0027 > 0.

## 5. Evidence: the study design at n = 200 (`scripts/study_n200.py`, `study_ls0.py`)

The generator is `gen_dev_data.R` re-implemented in numpy, so the data are distributionally equal but not bitwise equal:
- n = 200; s₀ = 14, one truth per group of 5;
- β pattern (1.4, −1.0, 1.8, −1.2, 0.8, −1.6) × scale ∈ {1, 0.5};
- scenarios S1, S3, S4, S6; p ∈ {500, 1000}; 10 replicates per cell;
- actual v3 partition (B = 14), exact π₀.

For each truth j the script computes:
- the exact start keep-odds LO₀(j) = log π₀(S₀) − log π₀(S₀ − j) and posterior keep-odds LO₁(j) = F(S₀) − F(S₀ − j);
- the block statistic V₀ = −ν log(1 − x^blk);
- its population (dilution) prediction V₀pop = δ²_pop/(2v_T) + ½.

| scen | p | scale | med log₁₀π₀(S₀) | med π₀(𝓡₂) | mean # start-masked truths (LO₀<0) | dilution-predicted # | frac masked with LO₁>0 | masked: V₀ / V₀pop / V₁ (medians) | masked: L² = δ²_pop/σ² | v_T/σ² | log₁₀π₀(S₀)−log₁₀π₀(S̃₀) | CL(0) prediction |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 500 | 0.5 | −13.0 | 0.95 | 7.5 | 7.0 | 0.99 | 3.6 / 4.1 / 22.9 | 50 | 7.2 | −12.0 | −34.6 |
| S1 | 500 | 1.0 | −12.1 | 0.91 | 6.3 | 7.0 | 1.00 | 3.2 / 4.4 / 69.7 | 199 | 25.6 | −11.0 | −28.9 |
| S1 | 1000 | 0.5 | −17.4 | 0.96 | 8.4 | 9.7 | 0.99 | 3.7 / 5.5 / 29.0 | 72 | 7.2 | −16.6 | −41.5 |
| S1 | 1000 | 1.0 | −13.8 | 0.89 | 7.1 | 7.0 | 1.00 | 3.4 / 4.4 / 74.1 | 199 | 25.6 | −12.6 | −31.1 |
| S3 | 500 | 0.5 | −13.2 | 0.70 | 7.5 | 7.0 | 0.99 | 3.6 / 4.0 / 23.7 | 50 | 7.2 | −11.8 | −34.6 |
| S3 | 500 | 1.0 | −13.8 | 0.72 | 7.5 | 7.0 | 1.00 | 3.7 / 4.4 / 70.6 | 199 | 25.6 | −12.6 | −34.6 |
| S3 | 1000 | 0.5 | −17.8 | 0.84 | 8.2 | 9.6 | 1.00 | 3.7 / 4.1 / 26.7 | 50 | 7.2 | −16.5 | −45.7 |
| S3 | 1000 | 1.0 | −16.3 | 0.67 | 8.1 | 7.0 | 1.00 | 4.4 / 4.4 / 78.2 | 199 | 25.6 | −14.7 | −39.4 |
| S4 | 500 | 0.5 | −16.9 | 0.32 | 8.8 | 7.0 | 0.99 | 3.6 / 4.4 / 28.5 | 50 | 7.2 | −14.9 | −40.4 |
| S4 | 500 | 1.0 | −13.4 | 0.11 | 7.1 | 7.0 | 1.00 | 4.4 / 4.4 / 75.6 | 199 | 25.6 | −11.4 | −38.5 |
| S4 | 1000 | 0.5 | −17.8 | 0.29 | 8.5 | 10.0 | 0.99 | 3.8 / 4.0 / 23.5 | 50 | 7.2 | −16.2 | −43.6 |
| S4 | 1000 | 1.0 | −17.6 | 0.25 | 8.0 | 7.0 | 1.00 | 3.5 / 4.4 / 77.0 | 199 | 25.6 | −15.9 | −43.6 |
| S6 | 500 | 0.5 | −16.8 | 0.73 | 8.9 | 7.0 | 0.96 | 3.6 / 4.0 / 26.4 | 50 | 7.2 | −15.7 | −40.4 |
| S6 | 500 | 1.0 | −12.4 | 0.47 | 7.5 | 7.0 | 1.00 | 4.4 / 4.4 / 74.1 | 199 | 25.6 | −10.8 | −34.6 |
| S6 | 1000 | 0.5 | −18.4 | 0.84 | 9.0 | 9.9 | 0.98 | 4.1 / 4.0 / 25.8 | 50 | 7.2 | −17.1 | −41.5 |
| S6 | 1000 | 1.0 | −12.8 | 0.70 | 7.2 | 7.0 | 1.00 | 4.2 / 4.4 / 70.2 | 199 | 25.6 | −11.1 | −33.2 |

Dilution threshold τ = log((2p−s₀)/s₀) + ½log(n+1) = 7.0 (p = 500) and 7.6 (p = 1000). Per-truth agreement between
"V₀pop < τ" and "LO₀ < 0" is 0.71–0.82 at n = 200; corr(V₀, V₀pop) = 0.69 over 2240 truths.

**n-sweep** (p = 1000, scale 0.5, 8 replicates per cell): median log₁₀π₀(S₀) and mean number of start-masked truths.

| scen | n = 200 | 400 | 800 | 1600 |
|---|---|---|---|---|
| S1 | −17.4 (8.4) | −7.6 (4.2) | −1.9 (1.4) | −0.3 (0.1) |
| S3 | −17.8 (8.2) | −8.4 (4.4) | −2.6 (1.8) | −0.3 (0.0) |
| S4 | −17.8 (8.5) | −7.7 (4.1) | −3.1 (1.0) | −1.1 (0.1) |
| S6 | −18.4 (9.0) | −9.0 (4.4) | −3.0 (1.5) | −0.3 (0.0) |

In the sweep corr(V₀, V₀pop) = 0.95 over 1344 truths and the per-truth prediction agreement rises to 0.77–1.00.

**Answer to the task's question.** The study's masking (median π₀(S₀) ≈ 10⁻¹²–10⁻¹⁸) is weak-signal masking only in the
block-SNR sense, which here is dilution. It is not consistent with W1-EXP's specific mechanism ("CL(L) with bounded L,
T27's law with c = number of weak truths"). The evidence:
- **Signal leaks strongly into the blocks.** The masked truths have L² = δ²_pop/σ² ≈ 50 (scale 0.5) to 199 (scale 1),
  not O(1). The CL(0) prediction −#missing·log₁₀(p√n) ≈ −29 to −46 overshoots the observed
  log₁₀π₀(S₀) − log₁₀π₀(S̃₀) ≈ −11 to −17 by 17–29 orders of magnitude.
- **The dilution prediction fits.** Masked truths have V₀ ≈ 3.2–4.4 against a threshold τ = log((2p−s₀)/s₀) + ½log(n+1)
  ≈ 7.0–7.6. The posterior sees V₁ ≈ 23–78, and 96–100% of the start-masked truths have LO₁ > 0. corr(V₀, V₀pop) is 0.69
  at n = 200 and 0.95 in the n-sweep. The predicted number of masked truths (7.0–10.0 per fit) matches the observed
  6.3–9.0, with 71–82% per-truth agreement at n = 200.
- **It is scale-free.** V₀ of the masked truths is the same at scale 0.5 and 1 (v_T = 7.2 vs 25.6 cancels the 4× signal),
  as Proposition W predicts. Stronger signals do not remove it at n = 200.
- **It is a finite-n effect.** In the n-sweep at p = 1000, scale 0.5, the mean number of start-masked truths falls
  8.4 → 4.2 → 1.4 → 0.1 (S1) and 8.2 → 4.4 → 1.8 → 0.0 (S3) for n = 200, 400, 800, 1600; median log₁₀π₀(S₀) goes
  −17.4 → −7.6 → −1.9 → −0.3. This is the favourable regime asymptotically, as Proposition W says for fixed s₀ + BM-∞.
- **Partition co-blocking is the other half.** The study's groups of 5 fit in a block (B = 14), so by Proposition Q
  LH-type cancellation could not survive the partition even if it were planted. S1/S3/S4/S6 have none at population
  level anyway (W1-EXP).

**LS0 on the study data** (`study_ls0.py`; HQ-relevant input for the LS0 tweak, outside the strict scope):

| scen | p | scale | ℓ | med \|S̃₀ Δ S₀\| | LS0 ends at S₀ certified | LS0 scores S₀ | among dist ≤ ℓ+1: scored | among dist > ℓ+1: scored |
|---|---|---|---|---|---|---|---|---|
| S1 | 500 | 0.5 / 1.0 | 10 | 9 / 8 | 7/10, 10/10 | 10/10, 10/10 | 20/20 | – |
| S1 | 1000 | 0.5 / 1.0 | 11 | 10 / 8 | 7/10, 10/10 | 10/10, 10/10 | 20/20 | – |
| S3 | 500 | 0.5 / 1.0 | 10 | 10 / 9 | 5/10, 9/10 | 8/10, 9/10 | 15/16 | 2/4 |
| S3 | 1000 | 0.5 / 1.0 | 11 | 11 / 10 | 5/10, 8/10 | 7/10, 9/10 | 15/19 | 1/1 |
| S4 | 500 | 0.5 / 1.0 | 10 | 12 / 12 | 2/10, 4/10 | 3/10, 8/10 | 6/7 | 5/13 |
| S4 | 1000 | 0.5 / 1.0 | 11 | 12 / 12 | 1/10, 5/10 | 4/10, 7/10 | 8/14 | 3/6 |
| S6 | 500 | 0.5 / 1.0 | 10 | 11 / 10 | 1/10, 9/10 | 4/10, 9/10 | 11/14 | 2/6 |
| S6 | 1000 | 0.5 / 1.0 | 11 | 12 / 8 | 3/10, 9/10 | 8/10, 10/10 | 18/18 | 0/2 |

Reading: when |S̃₀ Δ S₀| ≤ ℓ + 1, LS0 scored S₀ in 113/128 fits (S1 40/40, S3 30/35, S4 14/21, S6 29/32). When the
distance exceeds ℓ + 1 it scored S₀ in 13/32 (swaps can cut the distance by 2 per move). In S4 (ρ = 0.85) and S6 at
scale 0.5 the start mode is often 12–14 moves away, beyond ℓ = 10–11.
There LS0 fails or ends at a better-scoring wrong model, which would be a posterior miss and not a search miss. Dilution
masking with c ≈ s₀/2–3s₀/4 masked truths is exactly the case where the fixed-c theory says nothing about ℓ.

## 6. What fails and why

- **D2 for c ≥ 2.** D2 needs Gibbs distance 1 from a start-heavy state. At distance ≥ 2 the intermediate addition has
  start odds ≈ n^{−1/2}/p, so a crossing temperature must be reached first. That is the (b2) delivery problem (SHARE,
  W1-T38E C1). The original method's masked-regime theorem on LH-iid is therefore OPEN for c ≥ 2. With LS0 it is PROVED.
- **The study's group size is outside the family.** g = 5 ≤ B/2 is outside LH-iid (Proposition Q); the family needs
  9 ≤ g ≤ 16. A study-like p ≫ n *masked* family with g = 5 would have to use cancellation between units larger than a
  block, or non-clustering weak links. Neither is constructed.
- **LH-iid at n = 200 is near the edge.** In config A at n = 200, F(S₀) − F(S°) < 0 in 3/20 replicates (the masked
  coefficient −ψβ = −0.5 is weak), and Mstat has a heavy lower tail because π₀(S°) is only 0.70 in median. The theorems
  are asymptotic. Their margins are positive but small at the study size.
- **The dilution regime has no fixed-s₀ BM-∞ theorem.** It vanishes asymptotically (Proposition W). A theory for it
  needs either s₀ ≍ n/log n (outside the frozen setting) or local alternatives with a sharp-constant selection theorem
  (T03♯'s c₀ = L* is far too large). It is recorded as CONJECTURE W′, not pursued.
- **W1-EXP's random-design remark "NL_η fails, truncation essential".** Confirmed. Lemma Tr's truncation at
  τ_n = 4(A+3)log n/n is the device, and E(1−X)^{−ν} = ∞ for every Beta statistic here.
- **Certification is slow, scoring is not.** (L) at S₀ (no null addition improves on S₀) has margin
  ½log n + log(2p/(s₀+1)) − ½max_l Z_l². It fails with probability ≈ (s₀+1)/√(2π(n+1)t_n): 4% at n = 200 and 1.2% at
  n = 1600 (`results/check_L_failure.txt`). One such event occurred among the 12 replicates at n = 1600 (Z² = 24.5
  against 23.6). It is a posterior event (S₀ + null beats S₀), counted in T21's 2E₀δ₁. It is not a discovery failure,
  and LS0 still scores S₀.
- **The rate.** √(n/log n)·(1 − π₀(S°)) stays in 1.5–2.6 across n ∈ [200, 1600]. The √log n factor of P3 looks
  genuine: it comes from the max of p chi-squares. W1-EXP's exact-Gram realisation has n^{−1/2} because it has no null
  sample correlations.

## 7. Needs escalation

1. **Independent check of Lemma B and Theorem P3.** These are the new load-bearing arguments: conditional-independence
   identities F1–F3; the Grassmannian/Beta step after standardisation; the truncated moment; Jensen on (j!a)^{1/j}. A
   cross-family reviewer should redo them.
2. **W1-EXP Lemmas 1.1, 1.2, 1.4 at full generality.** PROOF §9.1 uses them for arbitrary sets of size ≤ s₀ + 2 rather
   than within-block sets. I checked that the proofs never use block membership; the reviewer should confirm.
3. **P7 (D2-d, NB) bookkeeping.** The π₀(S ⊉ S°) peeling bound and the uniform d-range bound are sketched. They are low
   risk, but they are the only non-PROVED step of route (b1′).
4. **HQ decision.** T38(b) can now be stated on an explicit p ≫ n family (LH-iid). The paper must **not** present it as
   the explanation of the n = 200 masking, which is dilution (a different, finite-n mechanism). Suggested wording: "the
   masked regime of Thm 5 is realised by cross-block cancellation; at the study size the start is masked by dilution,
   which disappears asymptotically; LS0 from the start mode repaired it in 113/128 simulated fits with |S̃₀ Δ S₀| ≤ ℓ + 1".
5. **Felipe / method.** The LS0 numbers at n = 200 suggest that ℓ (10–11) binds in S4/S6. If LS0 is adopted, consider
   letting the LS0 search run to certification. This is a cost change of a few scans, and it would need its own
   validation under the investment rule.

## 8. Outside scope (recorded, not pursued)

- **Correction to W1-EXP.** Its claim that under weak-signal masking "π(S₀) is also small, unlike LH" is not supported
  locally: 96–100% of start-masked truths have LO₁ > 0. Whether the study's posterior misses (565/2394) come from
  elsewhere (supersets at c = 1, swaps at c = 0.5) is the statistical-half question.
- **Start mass on 𝓡₂ at n = 200.** π₀(𝓡₂) is 0.7–0.96 in S1/S3/S6 but only 0.1–0.3 in S4 (ρ = 0.85). The study's
  "median π₀(𝓡₂) ≈ 0.8" hides a scenario split.
- **Sharpened T22(iii).** Theorem P3's method (exact Beta laws plus truncation) should give T22(iii) in the
  *favourable* regime for iid S1/S3/S4/S6 designs with the actual partition, rate √(log n/n) (W1-EXP card "T22(iii) iid
  designs", 0.8/0.6). The only changes are U_h° = S₀ ∩ C_h and the visible-group computation. Not written.

## 9. Confidence cards

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Joint p ≫ n family (task goal) | LH-iid carries G, R, SE (all variants), BM-∞, P3, P4, P5, P6, P8 jointly on the actual partition | 0.93 | done (PROVED, candidate) | Lemma B + Lemma Tr (P3); margin table (P6) | No (LS0 for the eligibility route) |
| Near-truth start mass b_n (T22(i) on LH-iid) | 1 − π₀(S°) = O_P(√(log n/n)) | 0.95 | done | exact Beta laws + truncation | No |
| T27 masking at the CL(L) rate | Mstat →_d Σlog((s+i)/2) + ½χ²_c | 0.97 | done | — | No |
| Eligibility (LS0) | S̃₀ = S° w.p. → 1 | 0.97 | done | — | Yes, minor (LS0) |
| Repair input TD′ (W1-T37R Thm A) | lattice condition at S° | 0.93 | done | population margins c₂ > 0 | No |
| D2 (no tweak), c = 1 | S₀ ∈ 𝒮_cal w.p. → 1 | 0.88 | 0.85 (NB bookkeeping left) | NB: H₀π₀(bad) → 0 | No (needs SR) |
| No-tweak route, c ≥ 2 | Ŝ = S₀ w.p. → 1 − P(U) without LS0 | 0.6 | 0.15 | delivery/SHARE (W1-T38E C1) | No, but unproved |
| π(S₀) → 1 on LH-iid | 1 − π(S₀) = O_P(√(log n/n)) | 0.97 | done (via locked T03) | de-randomisation lemma | No |
| Co-blocking (Prop. Q) | 2g ≤ B ⇒ linked pair co-blocked, no masking | 0.9 | 0.85 | merge-order argument | No |
| Dilution explains n = 200 masking (Prop. W) | start-masked ⇔ nθ²Var/(2v_T) < τ; vanishes for fixed s₀ + BM-∞ | 0.9 (mechanism); 0.85 (asymptotic statement) | 0.7 | uniform x_{T,j} → population with v_T | No |
| Fixed-s₀ dilution family with π(S₀) → 1 (W′) | local alternatives in the window | 0.7 | 0.3 | sharp-constant T03 | No |
