# W5-FAVIID — REPORT: a 2^B-free favourable-regime start rate on iid designs with the actual partition, and (P1)

Run of 2026-11-02, branch `theory/W5-FAVIID`. Proofs: `PROOF.md` (section numbers below refer to it). Scripts: `scripts/`
(fixed seeds in each header). Raw results: `results/*.jsonl`; tables: `results/*.txt`. Every result is a **candidate**,
not reviewed and not adopted. Status words are the protocol's and are never upgraded.

## 1. Headline

1. **PROVED (candidate): a 2^B-free favourable-regime start rate on iid block-diagonal designs with a fixed partition
   (Theorem A).** On P_n = {v3 blocks = a fixed union of groups}, 1 − π₀(S₀) = O_P((s₀+1)√(log n/n)) with leading constant
   3.83(s₀+1)√((1+ε₀)A). The constant depends on neither B nor g; B enters only through log(2^Bp) inside the rate. The
   ingredients: (i) a new one-sided table bound (Lemma X⁺: the O(1) EXP′ remainder is nonpositive, so κ_EXP ≈ 100+ nats
   drops out of every upper bound); (ii) exact Beta laws (Lemma B′); (iii) a Mittag-Leffler aggregation bound for
   D = max_j(j!a_j)^{1/j} (Lemma M), which is where 2^B disappears; (iv) locked T22(i).
2. **PROVED (candidate): the study's actual, noise-dependent packing (Theorem B).** For groups of 5 there is **no** fixed
   limit partition (Proposition N, PROOF SKETCH; numerically two designs share almost no co-blocked group pairs). Instead,
   blocks are unions of whole groups w.p. → 1 (Lemma P1′). Block ratios also factor across population-independent groups up
   to e^{o(1)}, for every packing at once. Hence 1 − π₀(S₀) = O_P(√(log n/n)) **unconditionally for S3, S4 and S6**, at a
   price of |𝒲| ≤ 106 truth contexts (15 while B = 14). This closes W3-VEXP's partition–noise GAP without a
   leave-one-column-out lemma. S1 (Prop. B1) has rate n^{−1/2}(log n)^{(s₀+1)/2} unconditionally. CONJECTURE: the |𝒲|
   factor is an artefact (the realised context changes the bound by ≤ 5%).
3. **PROVED (composition): Thm 6's (P1) and Thm 5(a) on S3/S4/S6-type designs (C2, C3),** with no EXP′/VIS/NL hypothesis.
   The conditional inputs are locked T03, T21 and W2-T26 Theorem A.
4. **Finite n: these are asymptotic statements. In iid designs the start's deficit is dominated by null-addition mass, not
   by dilution.** The mass is 1 − π₀(S₀) ≈ 1 − exp(−(s₀+1)M_p/(2√n)), independent of θ, B and the partition (CONJECTURE;
   it matches exact π₀ within ±15% at n = 3,200). Exact π₀ over 1,600 designs: median π₀(S₀) > ½ from n = 1,600 (S1; S3 at
   p = 500) or 3,200 (S3 at p = 1000, S4, S6). Discovery by iid final draws needs only n ≈ 330–440. The T22(i) certificate
   is valid in 1,600/1,600 designs but vacuous at every n ≤ 3,200 in S3/S4/S6.
5. **(P1) with the realised grid is far from satisfied at study-like n.** The simulated pilot plus grid gives T_n ≈ 4–5
   (not 1). (T_n + 1)Δ_n < 1 holds in 0/56 runs at n ≤ 3,200 and in 3/16 at n = 6,400, and its median is ≈ 1.5 at 12,800.
   With T^max = 4,000 it would need n ≈ 10¹⁰.

## 2. Statements (full text and proofs in PROOF.md)

**Family FAV (PROOF §0).** Rows of X^r iid N(0, Σ_n), Σ_n unit-diagonal and block-diagonal over a deterministic partition
𝒦_n of [p] into groups of size ≤ g ≤ 16, λ_min(Σ_n) ≥ λ₀ > 0; s₀ < p ≤ n^A; fixed S₀ (s₀ fixed) and fixed nonzero β;
y^r = Σ_{k∈S₀}β_k x^r_k/ŝ_k + ε with ŝ_k = 1 or the sample SD (the study generator's convention); ε ~ N(0, σ²I). S1, S3, S4
and S6 are instances (groups of 5, one truth per group; S1 with singleton groups). S2 and S5 are not (not block-diagonal).

| # | Statement | Hypotheses beyond FAV | Status |
|---|---|---|---|
| X⁺ | For U ⊊ A with λ_min(G_A) ≥ φ²(n−1): BF(A)/BF(U) ≤ e^{κ⁺}(n+1)^{−\|A∖U\|/2}(RSS_A/RSS_U)^{−ν}, κ⁺ = O(\|A∖U\|/(φ⁴n) + 1/(φ²RSS^y_U)) — the EXP′ remainder is ≤ O(1/n) *from above*; its O(1) part is nonpositive | none (deterministic) | PROVED |
| X⁻ | matching lower bound with κ⁻ = O(1) (for deletions) | none | PROVED |
| B′ | For any fixed union of groups Γ, any fixed W outside Γ, U = (S₀∩Γ)∪W, V ⊆ Γ∖S₀: X_{U,V} ~ Beta(\|V\|/2, (n−1−\|U\|−\|V\|)/2), independent of (X_U, y); y may be any function of (X_{S₀}, ε) | none | PROVED |
| Tr′ | E[(1−X)^{−ν}1{X ≤ τ}] ≤ (1−τ)^{−e₁}(mτ/2)^{j/2}/Γ(j/2+1); truncation at τ_n = 2(1+ε₀)log max(N_n,n)/n has P → 1 over N_n ≤ Cn^A variables | — | PROVED |
| M | If E[j!a_j] ≤ C₀(Nξ)^j/Γ(j/2+1) for all j, then E max_j(j!a_j)^{1/j} ≤ 3.8311·C₀Nξ (Mittag-Leffler constant; no 2^B, no Σ_j) | — | PROVED |
| S | ‖P_{A₁+⋯+A_r}y‖² ≤ (1−(r−1)c)^{−1}Σ‖P_{A_i}y‖² when pairwise ‖P_{A_i}P_{A_k}‖ ≤ c | — | PROVED |
| G | partition-free good events (SE on sets of size ≤ max(B, 2g+s₀), RSS floor, cross-group angles O(√(log p/n)), uniform visibility, truncation) have P → 1 | [C1] (Gaussian covariance concentration, cited) | PROVED given [C1] |
| **A** | **Fixed partition 𝒫_n (blocks = unions of groups):** on P_n = {v3 blocks = 𝒫_n}, E[q 1_𝒢] ≤ 3.83(1+o(1))ξ_n, ξ_n = √((1+ε₀)log max(2^Bp, n)/(n+1)); e = O(p√n e^{−νx₁/2}); hence **1 − π₀(S₀) = O_P((s₀+1)√(log n/n))** with leading constant 3.83(s₀+1)√((1+ε₀)A) — **no 2^B, no g** (B enters only via log 2^B inside ξ_n and o(1) terms) | [C1], locked T22(i), W1-EXP L1.1–1.2 | PROVED |
| P1′ | If every group has size ≤ B and min within-group \|Σ_jk\| > 0: P(every v3 block is a union of whole groups) → 1; for groups of 5 each block holds ≤ ⌊B/5⌋ groups | [C1] | PROVED given [C1] |
| N | For the study's groups of 5 there is no deterministic limit partition: each fixed pair of groups is co-clustered with probability ≤ (m−1)/(G−1) | exchangeability of the group-level dendrogram (packing step not equivariant) | PROOF SKETCH (+ numerics §4.2) |
| **B** | **Actual, noise-dependent packing:** on Q_n(m) = {blocks are unions of groups; each group's block holds ≤ m−1 other truth-carrying groups}, q ≤ e^{o(1)}Q̄_n with Q̄_n **partition-free**, E Q̄_n ≤ 3.83(1+o(1))\|𝒲(m)\|ξ_n; hence 1_{Q_n(m)}(1 − π₀(S₀)) = O_P(\|𝒲(m)\|(s₀+1)√(log n/n)), \|𝒲(m)\| ≤ Σ_{i<m}C(h₀, i). **For S3/S4/S6, P(Q_n(3)) → 1, so 1 − π₀(S₀) = O_P(√(log n/n)) unconditionally** (constant ×≤106; ×15 while B = 14) | [C1], locked T22(i), W1-EXP L1.1–1.2 | PROVED |
| B′-conj | Theorem B holds without the \|𝒲(m)\| factor | — | CONJECTURE (numerics §4.1: realised truth context changes Q̄ by ≤ 4%) |
| §10 | Sharp first order: 1 − π₀(S₀) ≈ 1 − exp(−N_add), N_add ≈ (s₀+1)(p−s₀)M(p,n)/((2p−s₀−1)√(n+1)), M ≈ 1 + (2/√π)√(log p) — independent of B, g, θ | — | CONJECTURE (PROOF SKETCH of the mechanism; numerics agree to ±15% at n = 3200) |
| F | One-change ceiling π₀(S₀) ≤ [1 + N_add + ΣO^del + ΣO^swp]^{−1} (exact odds, any data) | none | PROVED |
| §11 | Population plug-in thresholds n*_null, n*_del, n*_swp, n*_half, n*_hit as explicit functions of (θ, v, p, s₀, ρ) | — | CONJECTURE (median-level formulas; checked §4.4) |
| C1 | δ₁ = 1 − π(S₀) = O_P(√(log n/n)) on FAV | locked T03, W3-PXN de-randomisation lemma | PROVED (composition) |
| C2 | **Thm 6's (P1) on S3/S4/S6:** Δ_n = O_P(√(log n/n)), (T^max+1)Δ_n = O_P(log^{5/2}n/√n) → 0, so T26(i)–(ii) hold with the actual partition and budgets, without EXP′/VIS/NL | W2-T26 Thm A + Lemma 1 (candidates), idealisations EX-A, EX-S, CAL, START, OUT | PROVED (composition) |
| C3 | **Thm 5(a) (T38(a)) on S3/S4/S6:** liminf P(Ŝ = S₀) ≥ 1 − limsup P(U) | locked T21 route (a), C1, EX-S | PROVED (composition) |

## 3. Proofs (skeleton; details in PROOF.md)

**Theorem A (fixed partition).** Five ingredients, each short:
1. *Lemma X⁺ removes the EXP′ constant.* W1-EXP's remainder R is O(1) (κ_EXP ≈ 100–1,700 nats at study SNR), but its O(1)
   part is ν[a_U/RSS^y_U − a_A/RSS^y_A] with a_S = 0.02 + y'P_Sy/(n+1) + O(1/n) increasing in S and RSS^y decreasing, so it is
   **nonpositive up to O(1/n)**. Upper bounds on start mass off the truth therefore need no EXP′ constant and no chain.
2. *Lemma B′ gives exact Beta laws* for the block statistics X_{U_b*,V} at the reference S₀, for every fixed union of groups
   and every fixed outside conditioning set, with y any function of (X_{S₀}, ε) (so the generator's sample-SD convention is
   exact, not approximate).
3. *Lemma Tr′:* truncated moment E[(1−X)^{−ν}1{X ≤ τ_n}] ≤ (1+o(1))(t_n/2)^{j/2}/Γ(j/2+1) and a truncation event of probability
   → 1 (W3-PXN's Lemma Tr with the crude 2^{e₁} replaced by (1−τ_n)^{−e₁} → 1).
4. *Lemma M:* for D = max_j(j!a_j)^{1/j}, max_j Y_j ≤ λ(1 + Σ_j(Y_j/λ)^j) and the Mittag-Leffler sum give
   E D ≤ 3.8311·C₀·Nξ — **this is where 2^B disappears** (the locked T22(iii) sums over all T ⊆ C_b; W3-PXN summed over j).
5. *Locked T22(i):* 1 − π₀(S₀) ≤ (s₀+1)q/(1−q) + s₀e, with e = O(p√n e^{−νx₁/2}) from Lemma X⁻ and uniform visibility (G4).

**Theorem B (the actual packing).** The crux is a **factorisation across population-independent groups**: inside a realised
block b = K₁ ∪ ⋯ ∪ K_R, the residualised spans of different groups are nearly orthogonal (principal cosines
c_n = O(√(log p/n)) uniformly, (G3)), so by Lemma S the block statistic is at most (1 − Bc_n)^{−1} times the sum of the
per-group statistics, and since all statistics are O(log n/n) on the truncation event the error in the exponent is
O(B²t_n(τ_n + c_n)) → 0. Then a_bj ≤ e^{o(1)}Σ_{j₁+⋯+j_R=j}∏_i a′_{K_i,W_i,j_i}, the multinomial theorem gives
D_b ≤ e^{o(1)}Σ_iD′_{K_i,W_i}, and q ≤ e^{o(1)}Q̄_n where **Q̄_n sums D′_{K,W} over all groups K and all possible truth contexts
W ∈ 𝒲_K(m)** — a fixed, partition-free family with exact Beta laws (Lemma B′ with Γ = K). The packing's dependence on the null
columns never has to be decoupled: the inequality holds for every packing at once. The price is the number of truth contexts
|𝒲(m)|. Lemma P1′ (laminarity of complete linkage w.r.t. groups, then the cut and the packing keep whole groups) gives
P(Q_n(3)) → 1 for S3/S4/S6.

**Proposition B1 (S1).** For independent null columns, every truth context is dominated at once by the column's projection
on span(X_{S₀}, Y), a Beta((s₀+1)/2, ·) variable: rate n^{−1/2}(log n)^{(s₀+1)/2} with no event on the packing.

**Corollaries C1–C3.** δ₁ = O_P(√(log n/n)) from locked T03 by W3-PXN's de-randomisation lemma; Δ_n = max(1 − π₀(S₀), δ₁)
(W2-T26 Lemma 1); T^max = O(log²n); W2-T26 Theorem A and locked T21 do the rest.

## 4. Evidence

All numbers are exact (EX-A): v3 partition (port of `v3_blocks.h`, W3-PXN's library, re-checked in `results/sanity.txt`),
all block tables, π₀ by capped convolution. Designs follow `gen_dev_data.R` in distribution (numpy port: groups of 5,
truths at the generator's positions, signal on sample-standardised columns, ε ~ N(0,1), the same X and ε for both scales).
Sweep: S1/S3/S4/S6 × p ∈ {500, 1000} × scale ∈ {0.5, 1} × n ∈ {200, 400, 800, 1600, 3200}, 20 designs per cell
(1,600 design-scale rows; `scripts/study_sweep.py`, `results/sweep.jsonl`, table `results/sweep_summary.txt`).

### 4.1 Lemma checks and Theorems A/B on the study designs
- **Lemma checks** (`results/sanity.txt`): FastTables = W3-PXN tables (0.0); brute-force = convolution normaliser (0.0);
  Lemma X⁺ on 6,000 random (U, A) pairs: max(R⁺ − κ⁺) = −0.005 ≤ 0; Lemma S: 0 violations in 2,000 tests; Lemma B′ KS
  p-values 0.71/0.77/0.73 for three (Γ, W, V) configurations; c_ML = 3.8311.
- **T22(i) bound** (s₀+1)q/(1−q) + s₀e ≥ 1 − π₀(S₀) in **1,600/1,600** rows (0 violations). But it is **vacuous (> 1) in
  every S3/S4/S6 cell up to n = 3,200** (medians 10²–10⁵) and in S1 up to n = 1,600: the e term (proxy-saturated U) dominates;
  q itself is small (0.044–0.059 at n = 3,200).
- **Theorem A's moment bound**: the realised q divided by ξ_n(ε₀ = 0) = √(log(2^Bp)/(n+1)) is 0.60–0.82 in every cell
  (Theorem A: E q ≤ 3.83(1+o(1))ξ_n) — the bound holds with a factor ≈ 5 to spare, and q falls like √(log n/n).
- **Theorem B's factorisation** q ≤ e^{o(1)}Q_real (Q_real = Q̄ at the realised truth contexts, computed exactly): the
  ratio q/Q_real is ≤ 0.996 in all 1,200 S3/S4/S6 rows (the inequality holds even without the e^{o(1)}). **Q₀/Q_real
  (all contexts replaced by W = ∅) is 0.999–1.050** (medians per cell): the truth context barely matters, which is the
  numerical case for Conjecture B′ (no |𝒲| factor).
- **Union of whole groups (Q_n)**: held in 1,598/1,600 designs; the two exceptions are S6 at n = 200 (ρ = 0.4 groups against
  cross-group noise ≈ √(4 log p/n) ≈ 0.35). Realised truth context m_real ≤ 3 in S3/S4/S6.

### 4.2 No fixed partition (Proposition N) and S1's contexts (`results/propN.txt`, `results/s1_contexts.txt`)
For S3/S4/S6, 90–100% of groups share a block with another group (100% for n ≥ 400, B = 16), but **two independent designs at
the same (scenario, p, n) share almost no co-blocked group pairs**: mean Jaccard 0.0007–0.0096, at or below the 0.0045–0.014
expected if pairs were placed uniformly at random, at every n up to 3,200. The packing does not converge; Theorem B, not
VEXP's R3 device, is the right tool. In S1 the largest number of truths sharing a block is 1–3 in 199/200 designs (one design
at n = 200 had 5), so Theorem B's |𝒲(m)| with m = 3–4 (≤ 106–470) is the relevant S1 constant in practice.

### 4.3 The rate and the sharp constant
Median √(n/log n)(1 − π₀(S₀)) falls from ≈ 10 (n = 800) to 5.5–7.1 (n = 3,200) in every scenario: the √(log n/n) rate is
reached by n ≈ 3,200 and the remaining decay before that is the deletion/swap terms dying. **The null-addition prediction
1 − exp(−N_add^pred) (§10, no fitted constant) matches the exact 1 − π₀(S₀) to within a factor 0.86–1.11 at n = 3,200** in all
16 cells (and 0.96–1.07 at n = 1,600 in S1/S3 p = 500); at n ≤ 1,600 in S4/S6 the exact deficit is up to 2.2× the null-only
prediction because deletions and proxy swaps still contribute.

### 4.4 Dilution threshold n*(design) (`results/threshold.txt`, columns "pred" in `results/sweep_summary.txt`)
Exact medians of log₁₀π₀(S₀) (p = 500, scale 1; p = 1000 similar, ≈ 0.5–2 decades lower at n ≤ 800):

| scen | n = 200 | 400 | 800 | 1600 | 3200 | frac π₀(S₀) > ½ at 1600 / 3200 |
|---|---|---|---|---|---|---|
| S1 | −10.7 | −4.2 | −0.61 | −0.22 | −0.16 | 0.90 / 0.95 |
| S3 | −12.9 | −5.1 | −1.54 | −0.23 | −0.14 | 0.80 / 0.95 |
| S4 | −13.6 | −5.9 | −2.28 | −0.85 | −0.15 | 0.25 / 0.85 |
| S6 | −12.9 | −5.9 | −1.27 | −0.38 | −0.16 | 0.30 / 0.95 |

Predicted thresholds (population plug-in, PROOF §11):

| design | n*_null | n*_del | n*_half (pred) | empirical first n with median π₀(S₀) > ½ | n*_hit (pred) |
|---|---|---|---|---|---|
| S1 p=500 / 1000 | 1,020 / 1,130 | 670–750 / 730–820 | 1,050–1,080 / 1,140–1,175 | 1,600 / 1,600 | 330–370 / 380–420 |
| S3 p=500 / 1000 | 1,020 / 1,130 | 680–770 / 740–830 | 1,065–1,111 / 1,158–1,191 | 1,600 / 3,200 | 340–380 / 380–430 |
| S4 p=500 / 1000 | 1,020 / 1,130 | 810–900 / 830–940 | 1,314–1,409 / 1,370–1,449 | 3,200 / 3,200 | 360–400 / 400–440 |
| S6 p=500 / 1000 | 1,020 / 1,130 | 710–800 / 760–850 | 1,142–1,208 / 1,225–1,277 | 3,200 / 3,200 | 340–380 / 380–430 |

(ranges are over the two scales; the empirical column is on the grid {200, …, 3200}.) Reading:
- **The favourable threshold is set by the null-addition mass, not by dilution.** n*_null (≈ ((s₀+1)M/(2 log 2))², independent of
  θ and of v) exceeds n*_del in every design; dilution and proxy swaps add 5–40% (most in S4, ρ = 0.85).
- **Scale-free**: thresholds differ by ≤ 10% between scale 0.5 and 1 (θ_j²/v depends on shares), confirming W3-PXN/VEXP.
- **The predictor is optimistic by a factor ≈ 1.5–2.5 in n.** It reproduces log₁₀π₀(S₀) to ±0.1 at n ≥ 1,600 in S1/S3/S6 and at
  n = 3,200 everywhere, but at n ≤ 800 it is 1–4 decades too high (median-level plug-in ignores the noncentral fluctuation of
  the keep statistics, which enters through E e^{−V}, not e^{−median V}), and in S4 at n = 1,600 it misses 0.6 decades (proxy
  swaps). The exact one-change decomposition (11.1) is within 0.1 decades at n ≥ 800 and 0.5–2.4 decades at n ≤ 400
  ("decomposition" column), so the gap is in the population plug-in, not in (11.1). n*_half(pred) should be read as a lower
  bound; the empirical thresholds are 1,600 (S1, S3 p = 500) and 3,200 (S3 p = 1,000, S4, S6).
- **Discovery (Thm 5(a) route (a)) needs only n ≳ 330–440**: there Q_f^min·π₀(S₀) ≥ 3 by the predictor; exact medians of
  π₀(S₀) at n = 400 (10⁻⁴·² to 10⁻⁹·⁴) bracket the 2·10⁻⁵ requirement and at n = 800 (≥ 10⁻²·⁹) clear it in every cell.

### 4.5 (P1) with the realised pilot/grid stage count (`results/pilot_summary.txt`)
Simulated (`scripts/pilot_sim.py`): the v3 pilot exactly as in M §6.6 / `v3_calib.h` (H_e = ⌈512N₀/2500⌉ particles from exact
iid π₀ draws, ESS ≥ 0.9H bisection with the 1/T_e floor, multinomial resampling, one full move round per stage: p Gibbs
flips, uniform swap, B neighbour swaps on the v3 neighbour graph, independence proposal, random order), then one candidate-grid
construction (`build_grid`, pilot temperatures as targets) with V = top-20p by log γ₀ and by log γ₁ among the pilot-scored
models plus ∅. Approximations, stated: no diagnostic-island rebuild loop and no table sub-models in V (both can only add grid
points, so T_grid is a lower bound for the method's T). δ₁ is not computable exactly at p ≥ 500; I use the product estimate
1 − exp(−u₁), u₁ = exact sum of π(S)/π(S₀) over the one-move neighbourhood of S₀ (the lower bound u₁/(1+u₁) is also stored);
δ̂₁ ≈ 0.99·(1 − π₀(S₀)) at n ≥ 3200, so Δ_n is driven by both endpoints equally. Scale 1 unless stated; 2 replicates per cell;
74 runs (`results/pilot.jsonl`, `results/pilot_summary.txt`).

| n | runs | T_pilot median [range] | T_grid median [range] | Δ_n median | (T_grid+1)Δ_n median | runs with (T_grid+1)Δ_n < 1 |
|---|---|---|---|---|---|---|
| 800 | 16 | 10.5 [5, 24] | 13 [6, 33] | 0.89 | 12.5 | 0/16 |
| 1,600 | 20 | 6 [3, 12] | 7.5 [4, 18] | 0.53 | 4.9 | 0/20 |
| 3,200 | 20 | 4 [2, 8] | 4.5 [3, 13] | 0.33 | 1.9 | 1/20 |
| 6,400 | 16 | 3 [2, 6] | 5 [3, 11] | 0.26 | 1.5 | 3/16 |
| 12,800 | 2 (S3, S4, p = 500) | 3.5 [2, 5] | 5 [3, 7] | 0.24 | 1.6 | 1/2 |

Per scenario at n = 6,400 ((T_grid+1)Δ over the 4 runs): S1 1.06–2.24, S3 0.80–1.77, S4 0.91–5.85, S6 1.45–1.91. Reading:
- **The first n at which (T_n + 1)Δ_n < 1 is ≈ 6,400 for the best cells (S3, p = 500) and, in median, beyond 12,800.** Using §10's
  Δ_n ≈ (s₀+1)M(p,n)/(2√n) and the observed T_grid ≈ 4–5 (flat from n = 3,200 on), the median crosses 1 near
  n ≈ ((T+1)(s₀+1)M/2)² ≈ 2–5·10⁴ (extrapolation, CONJECTURE). With T^max = 4,000 it is ≈ 10¹⁰.
- **T_n does not fall to 1.** The realised grid settles at 3–5 stages (pilot 2–4) for n ≥ 3,200 instead of decreasing: the pilot's
  first-stage ESS is pinned at exactly 0.90 (the bisection binds), because the off-truth particles' weights e^{d(S)−d(S₀)} are
  heavy-tailed (§5). This supports T_n = O_P(1) with a constant ≈ 4–5, not T_n → 1 (CONJECTURE).
- At n ≤ 1,600 the start is still (partly) masked in S4/S6 and T_grid reaches 13–33, consistent with W2-T26's masked design.

## 5. What fails and why

- **A fixed limit partition for groups of 5 (the task's P_n device).** It does not exist: once each block is a union of whole
  groups, which groups share a block is decided by cross-group sample correlations whose population values are all 0, i.e.
  by noise (Proposition N; §4.2 numerics: two independent designs share almost no co-blocked group pairs). W3-VEXP R3's
  device works only when g ≤ B < 2g (blocks = groups), e.g. groups of 9–16 at B = 16; Theorem A covers that case.
- **Union over candidate blocks / Hölder decoupling** (W3-VEXP's attempts): lose a polynomial factor. Not needed — the
  factorisation inequality is deterministic on a partition-free event.
- **Removing the |𝒲(m)| factor (Conjecture B′).** The realised truth context W(K) is X-measurable while D′_{K,W} depends on y;
  conditioning on X turns D′ into an e^{δ²/(2Δ)}-type leakage functional (W1-EXP's NL_avg route, abandoned by W3-VEXP), and
  the index-1 heavy tail of e^{χ²/2} makes "max over contexts" as large as the sum, so a max-based bound does not help either.
  Numerically the context changes Q̄ by ≤ 4% (§4.1), so I believe the factor is an artefact.
- **S1 constant.** With singleton groups the context count can reach 2^{s₀}; Proposition B1 trades it for (log n)^{(s₀+1)/2}.
  Neither is a usable finite-n constant at s₀ = 14. The realised contexts are small (§4.2).
- **T22(i) as a finite-n certificate.** It is valid in every one of the 1,600 designs, but it is **vacuous at every n ≤ 3,200**
  (§4.1): the deletion quantity e is a maximum over all U ⊆ C_b, including U that contain all of a truth's group mates, where
  the truth's visible gain is θ_j²Var(x_j | mates)/v (Var = 0.19 in S4). That is a finite-n weakness of the locked aggregation
  bound, not of the rate; Proposition F's one-change ceiling and the exact convolution are the finite-n tools.
- **(P1) with T^max.** (T^max + 1)Δ_n < 1 needs Δ_n < 2.5·10⁻⁴, i.e. n ≈ 10¹⁰ at s₀ = 14 (§10's sharp constant). The
  asymptotic statement C2 is true but has no finite-n content; the realised T_n is what matters (§4.5).
- **T_n = O_P(1) in the favourable regime.** I could not prove it. The pilot's first ESS step sees weights e^{d(S)−d(S₀)} whose
  off-truth part (posterior versus block null-addition statistics, (Z_f² − Z_b²)/2) is heavy-tailed, so the realised T_n need
  not settle to 1; the simulations show T_n of order 1–5 at n ∈ [800, 6400] (§4.5). OPEN.

## 6. Needs escalation

1. **Independent check of the three new load-bearing steps:** Lemma X⁺ (sign of the EXP′ remainder; short but everything
   uses it), Lemma M (the Mittag-Leffler aggregation; replaces 2^B), and Theorem B's factorisation (Lemma S + (G3) + the
   multinomial step). The rest is W3-PXN's machinery with sharper constants.
2. **[C1] and the routine perturbation steps** in Lemma G ((G3) Schur-complement Lipschitz bound; (G4) uniform residual
   variances over |T| ≤ B with the generator's sample-SD coefficients): standard, written at proof level but not with every
   constant explicit.
3. **HQ decision (Thm 2(iii), Thm 6):** T22(iii)'s favourable branch can be stated for S3/S4/S6-type iid designs on the
   actual partition with no EXP′/VIS/NL hypothesis and no 2^B (Theorem B + C2). This also discharges W2-T26 Theorem B's
   CONDITIONAL input for these designs. The paper must not claim finite-n relevance: n*_half ≈ 1,050–1,450 for the study's
   s₀ = 14 designs, and (P1) with the realised grid needs n ≈ 6,400 in the best cells and, in median, n ≈ 2–5·10⁴ (§4.5).
4. **Felipe / method (no change proposed):** the start's dominant finite-n defect in iid designs is the null-addition mass
   (s₀+1)M(p,n)/(2√n), which no signal strength removes and which depends on neither B nor the partition. Only a change of
   the start (e.g. a sharper null-addition penalty in the tables) would move it; that is outside this run.

## 7. Outside scope

- **W3-PXN Theorem P3's constant improves the same way.** Lemmas X⁺ and M apply verbatim to LH-iid (blocks = groups): its
  E[q̃] ≤ 2.3·2^{g+3}gξ_n becomes 3.83(1+o(1))ξ_n, and e^{jκ} disappears. Not rewritten.
- **The locked T22(i) e-quantity is pessimistic at finite n** (proxy-saturated U). A refined aggregation that weights U by its
  start mass would give a usable finite-n certificate; this would be an edit of a locked statement.
- **Sharp first-order law of the start in iid designs** (§10): 1 − π₀(S₀) ≈ 1 − exp(−N_add) with N_add independent of θ, v, B
  and g. The same null-addition mechanism drives δ₁ (posterior null additions), so Δ_n ≈ (s₀+1)√(log p/(πn)) is a floor for
  both endpoints of the bridge in iid designs.
- **Discovery needs much less than favourability.** T38(a)'s route (a) needs only Q_f·π₀(S₀) → ∞; at the study budgets
  that happens at n*_hit ≈ 330–440, a factor ≈ 3 below n*_half.

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Thm 2(iii) / T22(iii), favourable, iid, fixed partition | Theorem A: 1_{P_n}(1 − π₀(S₀)) = O_P((s₀+1)√(log n/n)), constant 3.83(s₀+1)√((1+ε₀)A), no 2^B | 0.95 | done (PROVED, candidate) | Lemma X⁺ sign; Lemma M | No |
| Thm 2(iii), actual packing, S3/S4/S6 | Theorem B: 1 − π₀(S₀) = O_P(√(log n/n)) unconditionally, constant ×\|𝒲(3)\| ≤ 106 | 0.92 | done (PROVED, candidate) | factorisation across groups (Lemma S + (G3)) | No |
| Same, without \|𝒲\| | Conjecture B′ | 0.85 | 0.35 | decoupling the X-measurable truth context from y-dependent group statistics | No |
| S1 | Prop. B1: O_P(n^{−1/2}(log n)^{(s₀+1)/2}); O_P(√(log n/n)) on {≤ m truths per block} | 0.95 | done; sharp rate 0.4 | same as B′ | No |
| No fixed limit partition for g = 5 | Prop. N | 0.95 | 0.6 (packing not equivariant) | index-dependent leaf order | No |
| Sharp first order (§10) | 1 − π₀(S₀) ≈ 1 − exp(−(s₀+1)M_p(p−s₀)/((2p−s₀−1)√n)) | 0.85 | 0.5 | index-1 stable sum of within-group dependent e^{χ²/2} | No |
| Dilution threshold (goal 3) | n*_half ≈ max(n*_null, n*_del) (+ proxy swaps), predictor optimistic by 1.5–2.5× in n; empirical 1,600–3,200 | 0.8 (mechanism) / 0.6 (formula) | 0.4 | median-level plug-in vs E e^{−V} | No |
| Thm 5(a) (T38(a)) on S3/S4/S6 | C3: liminf P(Ŝ = S₀) ≥ 1 − limsup P(U); discovery from n ≈ 400 | 0.95 | done (composition of locked T21, T03 + Thm B) | — | No |
| Thm 6 (P1) | C2: (T^max+1)Δ_n = O_P(log^{5/2}n/√n) → 0, so T26(i)–(ii) hold | 0.95 | done (composition) | — | No |
| (P1) at finite n with realised T_n | first n with (T_n+1)Δ_n < 1: ≈ 6,400 (best cells), median ≈ 2–5·10⁴ | 0.8 | numerical only | T_n = O_P(1) (≈ 4–5) is OPEN | No (a sharper start penalty on null additions would be one) |
