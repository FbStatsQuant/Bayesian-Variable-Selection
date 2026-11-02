# W5-VPGD — REPORT: verification and completion of the asymptotic repair theorem (Theorem W, Thm 3(iii))

Branch `theory/W5-VPGD`. Refereed source: `origin/theory/W3-PGD:theory_campaign/W3-PGD/PROOF.md` (Theorem W and its
lemmas). This report is also the **completed REPORT for W3-PGD's results** (its own REPORT.md is a stub), so that
Thm 3(iii) has a citable source. Files here: `REFEREE.md` (line-by-line verdicts), `REPAIRS.md` (R0–R6),
`STAR.md` (the constant in (★)), `scripts/` (fixed seeds or deterministic), `results/`. Everything is a **candidate**:
one same-family referee pass, not reviewed cross-family, not adopted.

---------------------------------------------------------------------------------------------------------

## 1. Headline

1. **Theorem W VERIFIED** (no ERROR in any step). Four minor GAPs, all repaired (REPAIRS R1–R4): uniformity for random
   designs, LD♭ stability, (H1) ⊂ (H2), and an A > 1 sketch in C-LD. Status after repair: **PROVED (candidate)**, same-family referee.
2. **Discrepancy: the region form does not cover the masked regime (COUNTEREXAMPLE, R6.1).** On LH with ≥ 2 linked
   pairs, population PGD on R_{2,0} fails with an exact tie (η = 0, 20/20 cases), and TD′_P(R_{2,0}) fails w.p. → 1
   (200/200 fits at n = 200, 2000, 20000). The **lattice form Theorem W_Lat is PROVED** (R6.2). It needs no LD, and it
   holds on LH with an explicit constant η_LH (Prop. LH-PGD, PROVED, sharp in 20/20 cases). POP-LAT(S°, m₀) implies
   PGD(m₀/R_max) on the lattice: consistent with Prop. LH-LAT.
3. **(★) sharpened (Prop. S′, PROVED).** C-LD is not the worst family: grouped equicorrelated nulls already break
   TD′_P(R_{0,2}) at r > 1/3 (Prop. G, COUNTEREXAMPLE; C-LD needs r > 1/2). At A = 1, d = 2 the gap between proved and
   known-failing goes from 4.5× to 2.3×. On the (α)/(γ) statistic the remaining loss is intrinsic to the local/far
   method but second order in r.
4. **Study designs (population): PGD(η) holds in all six scenarios** on R_{2,2}(truth-block mates):
   η = 0.198 (S1), 0.148 (S2), 0.084 (S3), 0.043 (S4), 0.108 (S5), 0.057 (S6). Every time the binding move is a
   truth→truth swap (a θ-ratio effect). Cor P2′ = (B1)–(B3) enumeration = brute force, to 4 decimals, for d = 1, 2, 3.
5. **Realised designs, p = 500 (81 Python-generated designs).** PGD(η_pop/2) holds in 2/30 designs at n = 200,
   23/30 at n = 800 and 21/21 at n = 3200. TD′_P(R_{2,2}(𝒟)) holds in 9/30, 29/30 and 20/21 at c = 1, and in
   0/30, 27/30 and 20/21 at c = 0.5. Transfer is real but late. Cor P6's own constant is vacuous at every feasible n
   (it needs n ≈ 10^15–10^22).

---------------------------------------------------------------------------------------------------------

## 2. Verdict table (details: `REFEREE.md`)

| Item (W3-PGD PROOF label) | Verdict | Repair |
|---|---|---|
| Lemma 1.1 (a)–(c) move algebra | VERIFIED | — |
| Lemma 1.2 best truth addition (ρ⁺ ≥ (φ₀²/m)‖r_S‖² ≥ Nφ₀⁴θ²_min) | VERIFIED | — |
| GERC / TRC definitions; Lemma 1.3 (ERC controls null leakage) | VERIFIED | — |
| Prop P1 (GERC + TRC ⇒ PGD; five non-progress types N1–N5) | VERIFIED | — |
| Remarks (a)–(c) on GERC (tightness over θ; coherence bound; Exp 3) | VERIFIED | (a) uses ρ⁺ = max_j a_j(S), checked |
| Prop P2 (block iff (B1)–(B3)) | VERIFIED + brute force | — |
| Cor P2′ (equicorrelated closed form) | VERIFIED + numerics | — |
| Prop P3 (TRC sufficient conditions) | VERIFIED | — |
| Prop P4 (sharpness: reverse margin ⇒ failure) | VERIFIED | R0: vanishing η allowed |
| Lemma P5 (i)–(iii) (stability of Δ, PGD, SE) | VERIFIED | — |
| Lemma P5, LD♭ stability sentence | GAP (G3) | R3: |Δρ²| ≤ 8ε/φ₀⁸, PROVED |
| Cor P6 (random designs; cited Bickel–Levina) | VERIFIED given the citation; GAP (G2) in composition | R2: uniform form, PROVED |
| Lemma Q, Lemma R (score representation with ridge), Lemma G (pair geometry ‖r_A − r_B‖² ≤ C₁g), Lemma U, chain rule | VERIFIED | — |
| Lemma LD (local/far decomposition) | VERIFIED | — |
| Lemma S (α), (β), (γ) under (H1)/(H2)/(H3); (T); (L′) | VERIFIED | G1: (H1) ⊂ (H2), R1 |
| (★) constant | correct but loose | STAR.md: Prop. S′ (sharper, PROVED) |
| Lemma A′ | VERIFIED | — |
| **Theorem W** | **VERIFIED** | scope warning R6 (region form) |
| Cor W′ (i), (ii); random-design clause | VERIFIED; random-design clause after R2, R3 | — |
| Prop C-LD (COUNTEREXAMPLE) | VERIFIED (A = 1) | G4: A > 1 sentence → CONJECTURE (R4) |
| "(★) off by factor 3–4 from C-LD" | misleading | R5 / STAR.md §4 |

---------------------------------------------------------------------------------------------------------

## 3. Statements (in full)

Common setting (W3-PGD §0; 00_COMMON): G (fixed design, contrast coordinates, Gaussian noise), R (s₀ fixed,
p ≤ n^A, ‖μ‖² ≤ nM, s₀ + d + 1 ≤ K eventually), SE_λ(d+1): λ_min(R_{S₀∪J}) ≥ φ₀² for every J ⊆ S₀ᶜ, |J| ≤ d+1,
BM-∞: θ²_min ≥ M_nσ² log n/(nφ₀²), M_n → ∞. R_{a,d}(𝒟) = {U ∪ P : U ⊆ S₀, |S₀∖U| ≤ a, P ⊆ 𝒟, |P| ≤ d} for a
deterministic (X-measurable) 𝒟 ⊆ S₀ᶜ. PGD(η) on a family 𝓡: ρ⁰(S) ≤ (1 − η)ρ⁺(S) for every S ∈ 𝓡 with m(S) ≥ 1
(ρ⁺/ρ⁰ = the largest population residual reduction ‖r_S‖² − ‖r_{S′}‖² over progress / non-progress feasible
neighbours). TD′_P(𝓡) = (L) ∧ ⋂_{S∈𝓡∖S₀} D_S (W1-T37R).

**Theorem W (W3-PGD; refined T37(iii)). Status: PROVED (candidate; VERIFIED here).**
Regime R1, s₀, a ≤ s₀, d fixed. Assume EX-A, G, R, SE_λ(d+1), BM-∞, PGD(η) on R_{a,d}(𝒟) for a fixed η ∈ (0, 1], and
one of (H1) d ≤ 1; (H2) (|𝒟|+1)^{d−1} ≤ n^{1/2−ε}; (H3) LD♭(d; B′, ρ*) with (★) τ² < 1 + 1/(2A),
τ = (1 + ρ*√d)/√(1 − ρ*²). [Sharper alternative to (H3): (★′) of STAR.md Prop. S′.] Then
P₀(TD′_P(R_{a,d}(𝒟))) → 1, and for every data-dependent centre S_c and all n with ℓ_n ≥ a + d,
P(the production local search from S_c does not return S₀ with local_certified) ≤ P(S_c ∉ R_{a,d}(𝒟)) + o(1); on the
complement Ŝ = S₀ after the search (up to exact ties). The o(1) is uniform over designs with the same constants
(R2). η may tend to 0 as long as η_n²nθ²_min/log n → ∞ (R0).
**Scope warning (R6.1).** PGD on R_{a,d}(𝒟) with a ≥ 2 fails (exact tie) whenever some truth is worthless at some
state of the region, as in every masked design (LH with ≥ 2 pairs). For the masked regime use Theorem W_Lat.

**Theorem W_Lat (lattice form; REPAIRS R6.2). Status: PROVED (candidate).**
Same setting, with a deterministic centre S° = U° ∪ P°, |P°| ≤ d. If PGD(η) holds on Lat(S°) (states S ∈ Lat(S°) with
m(S) ≥ 1), then w.p. → 1, (L) ∧ ⋂_{S∈Lat(S°)∖S₀} D_S holds, and for ℓ_n ≥ Φ(S°) the search from any centre in Lat(S°)
returns S₀ certified: P(failure) ≤ P(S_c ∉ Lat(S°)) + o(1). No LD condition is needed.

**Corollary W′ (W3-PGD; sufficient design conditions). Status: PROVED (composition).** PGD(η) may be replaced by
(i) GERC(R_{a+1,d}(𝒟); η₁) ∧ TRC(R_{a,d}(𝒟); η₂), η = min(η₁, η₂) (Prop P1); or (ii) block orthogonality with one truth per
group and (B1)–(B3) (Prop P2), for equicorrelated groups the closed form of Cor P2′:
η*(d) = min{min_g(1 − ρ_g²), min_{g≠h}(θ_h²/θ_g²)(1 − κ_h(d))}, κ_h(d) = kρ_h²/(1 + (k−1)ρ_h), k = min(d, b_h − 1).
For Gaussian random designs, population PGD(η) and SE transfer to PGD(η/2) and SE(φ₀²/2) w.p. → 1 (Lemma P5,
Cor P6), and the conclusion holds jointly over (X, ε) by R2. Under (H3) LD♭ transfers too (R3).

**Proposition S′ (STAR.md §2). Status: PROVED (candidate).** In Lemma S, (H3) may be replaced by
(★′a) (τ_{d−1}² − 1)A < ½ and (★′b) (τ_{d−1}² + τ_d² − 2)A < 1 or (|𝒟|+1)^d ≤ p·n^{1−ε},
with τ_k := (1 + ρ*_k√k)/√(1 − ρ*_k²) and ρ*_k the LD♭ level over |T| ≤ k. (★) ⇒ (★′).

**Proposition G (STAR.md §3). Status: COUNTEREXAMPLE (construction + proof for d = 2; d ≥ 3 PROOF SKETCH).** Exact
design with A = 1, s₀ = 1, nulls in ≍ N^{1−β} orthogonal groups of size N^β with within-group correlation r. G, R,
SE, BM-∞, PGD(1) and GERC hold. If r > 1/3 (and β = (1+r)²/(1+3r)), TD′_P(R_{0,2}) fails w.p. → 1.

**Proposition LH-PGD (REPAIRS R6.3). Status: PROVED (candidate); sharpness numerical.** On LH (exact Gram),
PGD(η_LH) holds on Lat(S°)∖{S₀}, S° = S₀∖M, with η_LH = min{1, 1 − κ_max, D_min/R_max} and
D_min = min{min_i R_i, min_i β_i²(1−ψ_i²)², min_h θ_h²}. Also m₀ ≤ η_LH·R_max, so Prop. LH-LAT's POP-LAT(S°, m₀)
implies PGD(m₀/R_max). In general, PGD(η) on Lat(S°) ⇔ POP-LAT(S°, ·) up to the factor R⁺_max/R⁺_min.

**Proposition T (tie; REPAIRS R6.1). Status: PROVED.** If at S ∈ 𝓡 a present truth u is worthless at S + j for a missing
truth j (a_u(S + j − u) = 0), then ρ⁰(S) ≥ ρ⁺(S), so PGD(η) fails on 𝓡 for all η > 0. Under BM-∞ the neutral swap u → j
beats "add j" w.p. → 1.

**Prop C-LD (W3-PGD §5). Status: COUNTEREXAMPLE (VERIFIED, A = 1).** One equicorrelated null block, r > ½:
TD′_P(R_{0,2}) fails w.p. → 1. So LD-type conditions cannot be dropped for d ≥ 2 with unrestricted extras.

---------------------------------------------------------------------------------------------------------

## 4. Proofs (by label)

- Theorem W and every lemma: W3-PGD `PROOF.md` §§1–4 (labels as in §2's table), checked step by step in
  `REFEREE.md`. Proof skeleton:
  - **m ≥ 1 states.** The population gap ηNφ₀⁴θ²_min (Lemma 1.2 + PGD) beats the noise √(gap·log n) (Lemma G, with
    the union-model bound ‖r_A − r_B‖² ≤ C₁g) and the O(log n) penalties under BM-∞.
  - **Superset states.** The gap is zero, so these are χ² tails against the penalty ½ log n + log p (Lemma U), paid by
    (H1)/(H2)/(H3) (Lemma S).
  - **Path.** Lemma A′ turns TD′_P into certified repair.
- Repairs R0–R3 and the lattice form W_Lat: `REPAIRS.md` (complete proofs).
- Prop. S′ and Prop. G: `STAR.md` (complete proofs; Prop. G for d ≥ 3 sketched).
- Prop. LH-PGD: `REPAIRS.md` R6.3. It uses Prop. LH-LAT's unit algebra (W4-T38FULL §3.4, same-family VERIFIED there).
- Cor P2′ numbers: closed form, re-derived in `REFEREE.md` §1.

---------------------------------------------------------------------------------------------------------

## 5. Evidence

### 5.1 Engine validation
`scripts/engine.py` was written independently of W3-PGD's `pgd_core.py`. It evaluates every add/delete/swap neighbour
by rank-one updates. Against brute force (direct projections; the exact score F of 00_COMMON with ridge and BB(1,p)):
max error 3·10⁻¹⁵ (Δ) and 3·10⁻¹⁴ (F) (`results/test_engine.txt`). `scripts/popcheck.py` (PGD/GERC/TRC scanner) and
`realised.td_check` (TD′_P) agree with fully brute-force enumerations on small designs (`results/check_P2_bruteforce.txt`,
`results/test_td_check.txt`).

### 5.2 Population PGD on the study's designs (p = 500; gen_dev_data.R covariances and β pattern; 𝒟 = 56 truth-block mates)

| Scenario | structure | η*(1) | η*(2) | η*(3) | method | binding move | GERC_max (R_{3,2}) | TRC_min (R_{2,2}) |
|---|---|---|---|---|---|---|---|---|
| S1 | identity | 0.1975 | 0.1975 | 0.1975 | P2′ = (B1–B3) = scan | truth→truth | 0 | 0.1975 |
| S3 | ρ = 0.7 groups | 0.1007 | 0.0837 | 0.0765 | P2′ = (B1–B3) = scan | truth→truth | — | = η |
| S4 | ρ = 0.85 groups | 0.0548 | 0.0432 | 0.0390 | P2′ = (B1–B3) = scan | truth→truth | — | = η |
| S6 | ρ_g ∈ {.4,…,.9} | 0.0711 | 0.0571 | 0.0517 | P2′ = (B1–B3) = scan | truth→truth | — | = η |
| S2 | AR(1), 0.5 | — | 0.1481 (R_{2,2}) | — | exact scan, all 500 columns | truth→truth | 0.500 (η₁ = 0.75) | 0.1481 |
| S5 | factor 0.3 + groups 0.4 | — | 0.1079 (R_{2,2}) | — | exact scan (exchangeable reduction) | truth→truth | 0.650 (η₁ = 0.58) | 0.1079 |

Sources: `results/study_pop_A.txt` (S1, S3, S4, S6: scan on R_{1,1}, R_{2,1}, R_{1,2}, R_{2,2}, R_{1,3}, all equal to the
formula for their d), `results/study_pop_B.txt` (S2, S5). Exact reductions: block-orthogonal scenarios use the 70
truth-group columns plus one pure-null representative (every other null is orthogonal to all of them). S5 uses the
same set (pure-null groups are exchangeable given a state without pure nulls). S2 uses all columns.
- **Answer for S2 and S5:** yes, PGD(η) holds for some η > 0 on R_{2,2}(𝒟): η = 0.148 and 0.108. Via Prop P1, GERC
  holds with η₁ = 0.75 / 0.58, and TRC is the binding half (η₂ = η).
- **p = 30 (generator's small configuration, 𝒟 = all nulls, R_{2,2}, exact):** η = 0.198, 0.126, 0.084, 0.043, 0.099,
  0.057 for S1–S6 (`results/study_pop_C.txt`). The formula matches the block scenarios exactly.
- **What drives η.** It is never the look-alike leakage (B1) (1 − ρ² ≥ 0.19). It is always the truth→truth swap
  (B3): the θ ratio θ²_min/θ²_max = 0.64/3.24 = 0.198, discounted by (1 − κ_h(d)) for the group of the smallest truth.
  The F-REFINE values (S1 0.20; S3 0.10/0.08; S4 0.055/0.043) are confirmed. S6 = 0.071/0.057/0.052 is new.

### 5.3 Realised designs (Cor P6 transfer), p = 500, n ∈ {200, 800, 3200}

Generator re-implemented in Python (same law as `gen_dev_data.R`, not the same bits). Each design is evaluated on
R_{2,2}(𝒟), 𝒟 = 56 truth-block mates, with moves over all 500 columns: 167,685 states with m ≥ 1 for PGD, and 169,280
states plus (L) for TD′_P. There are 81 designs in total (3–5 per cell; seeds 20261102 + 1000·scen + n + rep, plus a
second block with base 30261102). Sources: `results/realised.jsonl`, `results/realised_summary.md`, `scripts/realised.py`.
"PGD(η/2)" means η̂ ≥ η_pop/2, the conclusion of Cor P6.

| scen | n | designs | eta_pop | median eta_hat [min, max] | PGD(eta_pop/2) | eta_hat > 0 | TD'_P c=1 | TD'_P c=0.5 | (L) c=1 / c=0.5 | median #failing states c=1 / c=0.5 | failing (m,e) classes c=0.5 | binding non-progress (c=0.5) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 200 | 5 | 0.1975 | 0.0786 [0.0748, 0.1126] | 1/5 | 5/5 | 3/5 | 0/5 | 4/5 / 3/5 | 0 / 73 | m0e1:112, m0e2:2882, m2e0:106, m2e1:6 | swap extra->null:2994, swap truth->truth:112 |
| S1 | 800 | 5 | 0.1975 | 0.1399 [0.1116, 0.1531] | 5/5 | 5/5 | 4/5 | 4/5 | 4/5 / 4/5 | 0 / 0 | m0e1:56, m0e2:1540 | swap extra->null:1596 |
| S1 | 3200 | 4 | 0.1975 | 0.1723 [0.1408, 0.1811] | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 / 4/4 | 0 / 0 | - | - |
| S2 | 200 | 5 | 0.1481 | 0.0501 [0.0427, 0.0826] | 1/5 | 5/5 | 2/5 | 0/5 | 5/5 / 4/5 | 1 / 87 | m0e1:56, m0e2:1498, m2e0:127, m2e1:180, m2e2:137 | swap extra->null:1597, swap truth->truth:401 |
| S2 | 800 | 5 | 0.1481 | 0.1072 [0.0824, 0.1181] | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 / 5/5 | 0 / 0 | - | - |
| S2 | 3200 | 4 | 0.1481 | 0.1272 [0.1202, 0.1298] | 4/4 | 4/4 | 3/4 | 3/4 | 4/4 / 4/4 | 0 / 0 | m0e2:203 | swap extra->null:203 |
| S3 | 200 | 5 | 0.0837 | 0.0229 [0.0154, 0.0308] | 0/5 | 5/5 | 2/5 | 0/5 | 5/5 / 4/5 | 4 / 467 | m0e1:2, m0e2:6, m1e0:1, m1e1:69, m1e2:1439, m2e0:117, m2e1:606, m2e2:6398 | swap truth->truth:5092, swap extra->null:3530, delete truth:10 |
| S3 | 800 | 5 | 0.0837 | 0.0485 [0.0374, 0.0526] | 4/5 | 5/5 | 5/5 | 5/5 | 5/5 / 5/5 | 0 / 0 | - | - |
| S3 | 3200 | 4 | 0.0837 | 0.0633 [0.0536, 0.0683] | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 / 4/4 | 0 / 0 | - | - |
| S4 | 200 | 5 | 0.0432 | 0.0054 [0.0000, 0.0114] | 0/5 | 5/5 | 0/5 | 0/5 | 5/5 / 2/5 | 684 / 10979 | m0e1:62, m0e2:1316, m1e0:3, m1e1:248, m1e2:6400, m2e0:155, m2e1:1726, m2e2:42142 | swap extra->null:30676, swap truth->truth:20666, swap truth->null:447 |
| S4 | 800 | 5 | 0.0432 | 0.0179 [0.0104, 0.0240] | 1/5 | 5/5 | 5/5 | 3/5 | 5/5 / 5/5 | 0 / 0 | m2e1:7, m2e2:238 | swap extra->null:218, swap truth->truth:27 |
| S4 | 3200 | 3 | 0.0432 | 0.0283 [0.0259, 0.0323] | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 / 3/3 | 0 / 0 | - | - |
| S5 | 200 | 5 | 0.1079 | 0.0372 [0.0170, 0.0501] | 0/5 | 5/5 | 2/5 | 0/5 | 5/5 / 4/5 | 1 / 108 | m0e1:1, m0e2:147, m1e0:1, m1e1:69, m1e2:1036, m2e0:177, m2e1:585, m2e2:3971 | swap extra->null:4877, swap truth->truth:1092, swap truth->null:11 |
| S5 | 800 | 5 | 0.1079 | 0.0645 [0.0574, 0.0683] | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 / 5/5 | 0 / 0 | - | - |
| S5 | 3200 | 3 | 0.1079 | 0.0929 [0.0913, 0.0949] | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 / 3/3 | 0 / 0 | - | - |
| S6 | 200 | 5 | 0.0571 | 0.0066 [-0.0324, 0.0157] | 0/5 | 4/5 | 0/5 | 0/5 | 5/5 / 2/5 | 234 / 3599 | m0e1:3, m0e2:18, m1e0:3, m1e1:207, m1e2:4279, m2e0:108, m2e1:994, m2e2:20176 | swap extra->null:19209, swap truth->truth:6356, swap truth->null:133 |
| S6 | 800 | 5 | 0.0571 | 0.0288 [0.0242, 0.0347] | 3/5 | 5/5 | 5/5 | 5/5 | 5/5 / 5/5 | 0 / 0 | - | - |
| S6 | 3200 | 3 | 0.0571 | 0.0413 [0.0391, 0.0489] | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 / 3/3 | 0 / 0 | - | - |

Totals over scenarios:

| n | PGD(η_pop/2) | η̂ > 0 | TD′_P, c = 1 | TD′_P, c = 0.5 |
|---|---|---|---|---|
| 200 | 2/30 | 29/30 | 9/30 | 0/30 |
| 800 | 23/30 | 30/30 | 29/30 | 27/30 |
| 3200 | 21/21 | 21/21 | 20/21 | 20/21 |

**Reading.**
- **Cor P6 transfer happens, but late.** η̂ rises towards η_pop with n (S1: medians 0.079, 0.140, 0.172 against
  0.198; S4: 0.005, 0.018, 0.028 against 0.043). PGD(η_pop/2) holds in every design at n = 3200, in 23/30 at
  n = 800, and in 2/30 at n = 200. At n = 200 one S6 design has η̂ < 0 (a reverse margin, Prop P4's regime), and
  one S4 design has η̂ = 0.0000.
- **TD′_P(R_{2,2}(𝒟)) holds at n ≥ 800 in 96/102 (design, c) cases.** The 6 failures are: superset-state noise
  (extra→null swaps at S₀ ∪ P, Lemma S's (γ) event: S1 n = 800, one design; S2 n = 3200, one design), and S4 at
  n = 800, c = 0.5 (m = 2 states via extra→null and truth→truth swaps, the move that binds PGD in S4).
- **At n = 200 the two failure mechanisms separate by scenario.** In S1 and S2 the failures sit at superset states
  (m0e1, m0e2), and (L) itself fails in 1–2 of 5 designs. These are posterior-side noise events, the penalty against
  max-χ², not greedy-dominance failures. In S3, S4 and S6 most failures sit at m = 2 states, through truth→truth and
  extra→null swaps: the realised η̂ is 0.005–0.03, too small for the signal at n = 200.
- TD′_P can hold where PGD(η/2) does not (S2/S5 at n = 200, c = 1; S3, S4, S6 at n = 800). PGD is a sufficient
  population condition, while TD′_P is the data event.

**Cor P6's own constant is vacuous here.** Lemma P5(iii) needs ε ≤ ηφ₀⁶θ²_min/(128s₀‖θ‖²). That is 2.9·10⁻⁶ (S1) down to
8·10⁻¹⁰ (S6), i.e. n ≈ 10¹⁵–10²² (`results/corP6_constants.txt`). The numerics above are the only evidence on transfer.

### 5.4 LH (goal 4)
- 20 LH cases (W4's referee set, same seed): PGD constant on Lat(S°) = η_LH formula (20/20); ≥ m₀/R_max (20/20).
  On R_{c,0}: η = 0 exactly (20/20), binding truth→truth swap (`results/lh_pgd.txt`).
- Realised exact-Gram LH (case 0, c = 2): D_S fails at S₀∖{a₁,a₂} in 200/200 fits at n = 200, 2000, 20000; it holds
  at S° = S₀∖{b₁,b₂} in 200/200 (`results/lh_tie.txt`).

### 5.5 The (★) constant (goal 2)
`results/star_thresholds.txt`, `results/beta_rate.txt`. At A = 1, d = 2, for grouped equicorrelated nulls:
(★) certifies r < 0.111; (★′) certifies r < 0.143 ((★′a) alone: 0.200); C-LD fails for r > 0.5; Prop. G fails for
r > 0.333. The first-order slopes of the local/far bound and of the achievable sup agree (2, 4, 6 for d = 2, 3, 4).
The certified/failing ratio for (★′a) is 1.67, 1.29, 1.13, 1.06 at A = 1, 2, 4, 8 (A > 1 is a formula comparison).

### 5.6 W3-PGD's own numerics (for the record)
W3-PGD's `results/` contains only the S1 population check (η = 0.1975 on R_{14,0}, R_{14,1}, R_{3,2}; p = 500 and 1000)
and the C-LD script output. Its `n200_check.py` has no result file. The C-LD script illustrates direction only: the
failure frequency at r = 0.55 is 2–3.5% up to n = 2·10⁵, since the o(log n) terms dominate at any feasible n.

---------------------------------------------------------------------------------------------------------

## 6. What fails and why

- **The region form for masked designs** (R6.1). PGD needs every present truth to keep a population value whenever a
  missing truth is added. Masking (b_i worthless without a_i) breaks this exactly, not approximately. So Theorem W
  with a ≥ 2 is silent on the masked regime. The lattice form at the delivered centre is the right statement.
- **Cor P6 as a quantitative tool.** The perturbation constant is ~10⁻⁶–10⁻⁹ on the study designs. The transfer is an
  asymptotic existence statement only.
- **Sharpening (★) via C-LD.** C-LD is not extremal. The right comparator family has many large groups, so the
  group factor itself is extreme (Prop. G).
- **Removing (β)'s slack.** The local/far method bounds the two summands of the (β) statistic separately. I found no
  argument that bounds them jointly. A heuristic large-deviation relaxation says (β) is far from binding in the grouped
  family. Left as CONJECTURE.
- **Optimality of Prop. G's configuration** among all designs with a given LD♭ level: not attempted beyond the LD-rate
  relaxation within the family. OPEN.

## 7. Needs escalation

1. **Cross-family review of Theorem W** (and of R2, R6.2). This was one same-family pass, although it did check every
   step. The steps most worth a second look are Lemma R's ridge bookkeeping (ζ_T, C₀) and Lemma G's pair counting. The
   proof is long but elementary.
2. **The (β)-removal conjecture** (STAR.md §4). If true, the certified threshold at A = 1, d = 2 rises from 0.143 to
   0.200 against a failing 0.333. It needs a joint bound on Z²_{S−e,e} + Z²_{S,l}, a Gaussian-process supremum argument,
   probably via Slepian or Sudakov–Fernique on the pair process.
3. **Random-design (A > 1) version of Props. G and C-LD.** Needed for any claim about thresholds in r as functions of A.
4. **The bibliographic claim** that GERC is Tropp's ERC as used for OLS (Soussen–Gribonval–Idier–Herzet, IEEE-TIT 2013)
   was not re-checked. No proof here depends on it.
5. **Bickel–Levina citation in Cor P6** (correlation, not covariance, version). Standard, but not re-derived.

## 8. Outside scope

- **TD′_P is too strict for masked designs.** At S₀∖{a₁,a₂} on LH the greedy path swaps b₂ → a₁ (neutral), then adds
  a₂ and b₂. It reaches S₀ in 3 moves for Φ = 2. A potential counting "effective" truths would make this a progress
  path and could give a region-form statement for masked designs. Not pursued.
- **Relevance at n = 200.** The study's η values are small (0.04–0.20), and Theorem W's guaranteed population gap is
  ηNφ₀⁴θ²_min. For S4 with c = 0.5 this is 0.043 · 199 · 0.15² · 0.4² ≈ 0.03 (σ² = 1), against penalties of
  ½ log n + log p ≈ 9 nats. So the proof's lower bound says nothing at n = 200 for the correlated scenarios (the actual
  gaps are larger than this worst-case bound). §5.3 shows what actually happens.

## 9. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Thm 3(iii), region form (Theorem W) | as §3, with the scope warning | 0.95 (as stated) | done (candidate); 0.9 that cross-family review passes without a substantive error | Lemma G pair geometry + Lemma S tails; scope: PGD fails exactly under masking | no |
| Thm 3(iii), lattice form (W_Lat) | as §3 | 0.95 | done (candidate) | the same proof restricted to Lat(S°); fixed extras so no LD | no (uses LS0's centre S° in T38) |
| LH: PGD on Lat(S°) (Prop. LH-PGD) | η_LH = min{1, 1−κ_max, D_min/R_max} | 0.97 | done | rests on LH-LAT's unit algebra | no |
| (★) sharpening (Prop. S′) | (★′a) ∧ (★′b) | 0.95 | done | splitting |T| ≤ d−1 from |T| ≤ d | no |
| (★′a) alone suffices (β-removal) | CONJECTURE | 0.7 | 0.4 | joint Gaussian supremum for (β) | no |
| Grouped-family failure (Prop. G) | r > 1/3 at A = 1, d = 2 | 0.95 | done for d = 2; sketch d ≥ 3 | order statistics of the best group | no |
| Realised transfer on study designs | PGD(η/2) and TD′_P on R_{2,2}(𝒟) hold for n ≥ 800 in most designs and for n = 3200 in all but one; not at n = 200 | — (empirical, 81 designs) | — | Cor P6 vacuous quantitatively; superset noise persists at p = 500 | no |

**Bottom line for the paper.** Thm 3(iii) can cite Theorem W (VERIFIED, candidate) for "TD′ w.p. → 1 under PGD + LD♭".
For the masked regime (T38(b1), LH) it must cite Theorem W_Lat with Prop. LH-PGD, not the region form. The study's
population designs satisfy PGD with η = 0.04–0.20. Nothing in this asymptotic statement explains n = 200 behaviour.
