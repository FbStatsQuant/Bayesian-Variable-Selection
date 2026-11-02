# W2-T26 REPORT — T26 (i)–(ii): evidence and PIP consistency, favourable regime

Cloud run W2-T26, branch `theory/W2-T26`, 2026-11-02. Everything here is a **candidate**: not reviewed, not adopted.
Full statements and proofs: `PROOF.md` (this folder). Scripts: `scripts/`. Raw outputs: `results/`.

## 1. Headline

- **Theorem A (premise form) — PROVED (candidate composition).** Under EX-A, EX-S, CAL, START, the output bookkeeping
  OUT, (Ω) s₀ ≤ K eventually, and **one** premise (P1) (T_n+1)Δ_n → 0 (plus its exact-branch twin (P1-ex) δ₁ → 0),
  Ẑ/Z → 1, every Ẑ_r/Z → 1, log Ẑ − log Z → 0, max_j |PIP̂_j − 1{j∈S₀}| → 0 and MPM̂ = S₀, all in the form
  P(output available ∧ error > ε) → 0, never conditioning on completion. Inputs: T14(i), T15, T23(ii-a,b), T22(iv-b),
  T09(ii), T12(i.a,i.b) (all locked). No G, R, SE, BM or EXP.
- **The frozen second premise (L_n+4)ρ*_n → 0 is redundant — PROVED.** T15 holds at every terminal-round prefix
  (through T12(i.b)), so occupancy is re-controlled at the start of each measured round and only one round's departure
  ρ̄ ≤ (B+3)u_π is paid (Lemmas 2, 3). Numerically this matters: at p = 18, n = 163,840 the frozen P2 quantity is ≈ 1.7
  (not small), while the term that actually enters is ≈ 0.03.
- **Lemma 1 — PROVED:** Δ_n = max{1 − π₀(S₀), 1 − π(S₀)} exactly (T22(iv-b) plus the endpoints). So (P1) splits into
  (T_n+1)δ₁ → 0, discharged by T03 (no EXP), and **(T_n+1)(1 − π₀(S₀)) → 0, the only genuinely open input and the
  only place EXP′ enters** (via T22(iii)).
- **Theorem B (discharged form) — PROVED as a composition, CONDITIONAL** on T03's G, R, SE, BM and T22(iii)'s EXP′,
  VIS, NL_η, NL_avg(κ). **Proposition C — PROOF SKETCH:** on the exact-orthogonal family (p ≤ n − 1) all of Theorem B's
  hypotheses hold jointly, including EXP′ with max|R| = O_P(1); numerically max|R| ≈ 0.11–0.16 over every within-block
  addition. So Theorem B is not vacuous, but the family is not the p ≫ n study design.
- **Numerics.** The premises are non-vacuous at exact p = 18 (smallest p the method does not enumerate): with the
  realised (ideal-grid) T, (T+1)Δ_n falls like n^{−1/2} to ≈ 0.02 at n = 163,840. With the deterministic cap
  T^max = 4,000 they need n far beyond 10⁸. All finite-n (A-0) bounds hold in final-run simulations, with 30–200× slack.

## 2. Statements (full versions in PROOF.md §1)

Notation (new symbols): Δ_n = 1 − inf_{φ∈[0,1]} q_φ(S₀); ρ̄ = probability that one φ = 1 round started at S₀ leaves S₀
somewhere on its path; 𝒢_n = SMC branch and calibration success; ℰ_n = exact branch; 𝒪_n = output available (status
`exact` or `completed`); T^max = 4max(1000, ℓ²); b(𝓒) = 2(T+1)Δ_n/(1−Δ_n). Potential uninterrupted run: the final run
of T12's I(𝓒), defined on 𝒢_n whether or not the job finishes; its outputs carry a °.

**OUT (bookkeeping, declared).** 𝒪_n ⊆ ℰ_n ∪ 𝒢_n; on 𝒪_n ∩ 𝒢_n the reported outputs equal the potential run's; on
𝒪_n ∩ ℰ_n, Ẑ = Z and PIP̂ = PIP.

**Theorem A.** Assume EX-A, EX-S, CAL, START, OUT, (Ω) P₀(s₀ ≤ K_n) → 1, (P1) P(𝒢_n ∩ {(T_n+1)Δ_n > ε}) → 0 for all
ε > 0 (sufficient: (T^max_n+1)Δ_n → 0 in P₀-probability), and (P1-ex) P₀(ℰ_n ∩ {δ₁ > ε}) → 0 for all ε > 0 (implied by
the deterministic form of (P1), by T03, or vacuous when ℰ_n eventually fails).
- (A-0) For fixed n, data with S₀ ∈ Ω, 𝓒 ∈ 𝒢_n, island r:
  E_𝓒|Ẑ°_r/Z − 1| ≤ b(𝓒), E_𝓒|Ẑ°/Z − 1| ≤ b(𝓒);
  occupancy off S₀ at the end of stage T and at the start of each measured round ≤ min{1, 2δ₁ + 2b(𝓒)} in E_𝓒-mean;
  E_𝓒 max_j|PIP̂°_{rj} − 1{j∈S₀}| ≤ min{1, 2δ₁ + 2b(𝓒)} + ρ̄ + u_π (also for the primary PIP);
  P_𝓒(MPM̂° ≠ S₀) ≤ 2 × that; ρ̄ = 1 − ∏_e(1 − K_e(S₀, Ω∖{S₀})) ≤ (B+3)u_π.
- (A-i) P(𝒪_n ∩ {|Ẑ/Z − 1| > ε}), P(𝒪_n ∩ {max_r|Ẑ_r/Z − 1| > ε}), P(𝒪_n ∩ {|log Ẑ − log Z| > ε}) → 0.
- (A-ii) P(𝒪_n ∩ {max_j|PIP̂_j − 1{j∈S₀}| > ε}) → 0 (also islandwise), P(𝒪_n ∩ {MPM̂ ≠ S₀}) → 0.
- Not claimed: P(𝒪_n) → 1; masked regime; secondary PIP; HPM; any rate in N; flag- or completion-selected runs;
  floating point.

**Theorem B.** Add, in R1: G, R, SE, BM-C or BM-∞ (T03, with T02(i)); EXP′ (strict or weak), VIS, NL_η, NL_avg(κ), κ > 0
fixed, method blocks (T22(iii)). Then (Ω), (P1) (deterministic-budget form) and (P1-ex) hold, with
(T^max+1)Δ_n = O_P(log²n·[2^B√(log n)n^{−κ} + e_n + √(log n/n)]) → 0, so Theorem A's conclusions hold.
EXP′ is used only for (T^max+1)(1 − π₀(S₀)) → 0.

**Proposition C (ORTH compatibility).** On X ᵀX = (n−1)I_p, p ≤ min(n−1, n^A), fixed s₀ and fixed nonzero θ on S₀:
G, R, SE, BM-C, VIS, NL_η (η = 0), NL_avg(κ) (κ ≤ ½) and strict EXP′ hold. PROOF SKETCH (PROOF.md §6).

## 3. Proofs (skeleton; details in PROOF.md §§2–4, 6)

1. **Lemma 1 (PROVED).** T22(iv-b) gives sup_φ(1 − q_φ(S₀)) ≤ max of the endpoint deficits; φ ∈ {0,1} gives ≥.
2. **Lemma 2 (PROVED).** π-reversibility (T09(ii)) gives K_e(x,y) ≤ π(y)/π(x). Gibbs-j at S₀ can only move to
   S₀Δ{j}, and these p targets are distinct, so the Gibbs labels together contribute ≤ u_π; each of the other B + 2
   labels contributes ≤ u_π. Given the order, the stay probability is ∏_e(1 − K_e(S₀, ·ᶜ)), which does not depend on
   the order.
3. **Lemma 3 (PROVED).** B_{i,h} ≤ 1{X_{i,L+h−1} ≠ S₀} + 1{X_{i,L+h−1} = S₀, round L+h departs}; by T12's (R3) the
   second term has conditional probability ≤ ρ̄.
4. **(A-0) (PROVED).** T14(i) with S° = S₀ (η_t ≤ Δ_n); T15(iii)+(i) with 𝔄 = {S₀}, c = ½, at the end of stage T and
   at each measured-round start (positions (a), (b) of 𝒯; H-T12 = T12(i.a), (i.b)); T23(ii-a,b) pathwise; Lemmas 2, 3.
5. **(A-i), (A-ii) (PROVED).** On A_x = 𝒢_n ∩ {S₀∈Ω} ∩ {(T+1)Δ_n ≤ x}: b < 3x, δ₁ ≤ x/2, u_π ≤ x, ρ̄ ≤ 19x, so the
   conditional means are ≤ 3x (evidence) and ≤ 27x (PIPs). Markov inequality, plus (P1) and (Ω), then x ↓ 0. Exact
   branch through (P1-ex). The output-available event is only ever intersected, never conditioned on.
6. **Theorem B (PROVED as a composition).** T^max = O(log²n); T03(i) gives δ₁ = O_P(√(log n/n)); within-block SE
   follows from SE once m_n + s₀ ≥ 16; T22(iii) gives 1 − π₀(S₀) = O_P(2^B√(log n)n^{−κ} + e_n); then Lemma 1.

**Crux.** There is no crux left inside the composition. The content is entirely in its inputs: start concentration
at rate o(1/T_n) (T22(iii), i.e. EXP′, VIS, NL) and T03's SE and beta-min.

## 4. Evidence

All scripts are in `scripts/`, with fixed seeds stated in each file header. Exact enumeration is at p = 18, B = 4,
s₀ = 3. That is the smallest p at which v3 takes the SMC branch for n ≥ 22, because 2¹⁸ > 12,560·18.

**4.1 Premise scan** (`premise_scan.py`, `summarise.py` → `results/premise_summary.md`; 8 seeds for n ≤ 5120,
6 for n ≥ 10240). Designs: `fav_iid` (iid columns), `fav_cor` (6 groups of 3, within-group correlation 0.5), β = 0.6
on S₀ = {0, 6, 12}; `masked` (x₃ correlated 0.6 with x₀ across groups, β₃ = −0.6, so x₃ has zero marginal signal).
Medians:

| design | n | 1−π₀(S₀) | δ₁ | Δ_n | T_ideal | (T_ideal+1)Δ_n | (T^max+1)Δ_n | ρ̄-bound + u_π | frozen (L+4)ρ* |
|---|---|---|---|---|---|---|---|---|---|
| fav_iid | 40 | 9.67e-01 | 9.24e-01 | 9.83e-01 | 6 | 6.18e+00 | 3.93e+03 | 5.28e+01 | 1.00e+01 |
| fav_iid | 80 | 6.61e-01 | 3.68e-01 | 7.34e-01 | 5 | 4.40e+00 | 2.94e+03 | 1.21e+00 | 1.10e+01 |
| fav_iid | 160 | 2.87e-01 | 2.66e-01 | 3.19e-01 | 2 | 9.84e-01 | 1.28e+03 | 8.45e-01 | 1.20e+01 |
| fav_iid | 320 | 1.41e-01 | 1.48e-01 | 1.48e-01 | 1 | 2.96e-01 | 5.93e+02 | 4.44e-01 | 1.30e+01 |
| fav_iid | 640 | 1.15e-01 | 1.25e-01 | 1.31e-01 | 2 | 3.28e-01 | 5.23e+02 | 3.65e-01 | 1.35e+01 |
| fav_iid | 1280 | 1.28e-01 | 1.21e-01 | 1.42e-01 | 2 | 4.10e-01 | 5.66e+02 | 3.29e-01 | 1.44e+01 |
| fav_iid | 2560 | 4.91e-02 | 7.50e-02 | 7.50e-02 | 1 | 1.50e-01 | 3.00e+02 | 2.02e-01 | 9.08e+00 |
| fav_iid | 5120 | 4.97e-02 | 5.20e-02 | 5.56e-02 | 1 | 1.11e-01 | 2.23e+02 | 1.46e-01 | 6.53e+00 |
| fav_iid | 10240 | 4.04e-02 | 3.25e-02 | 4.04e-02 | 1 | 8.09e-02 | 1.62e+02 | 9.39e-02 | 4.23e+00 |
| fav_iid | 40960 | 1.42e-02 | 1.71e-02 | 1.86e-02 | 1 | 3.71e-02 | 7.43e+01 | 4.68e-02 | 2.43e+00 |
| fav_iid | 163840 | 8.51e-03 | 1.12e-02 | 1.12e-02 | 1 | 2.25e-02 | 4.49e+01 | 2.94e-02 | 1.75e+00 |
| fav_cor | 40 | 9.95e-01 | 9.21e-01 | 9.95e-01 | 5 | 5.92e+00 | 3.98e+03 | 1.31e+01 | 1.00e+01 |
| fav_cor | 80 | 8.23e-01 | 4.57e-01 | 8.23e-01 | 5 | 4.43e+00 | 3.29e+03 | 1.45e+00 | 1.10e+01 |
| fav_cor | 160 | 2.57e-01 | 2.43e-01 | 2.78e-01 | 2 | 7.01e-01 | 1.11e+03 | 7.36e-01 | 1.20e+01 |
| fav_cor | 320 | 2.08e-01 | 1.85e-01 | 2.31e-01 | 2 | 5.99e-01 | 9.25e+02 | 5.57e-01 | 1.30e+01 |
| fav_cor | 640 | 1.51e-01 | 1.53e-01 | 1.86e-01 | 2 | 5.59e-01 | 7.46e+02 | 4.33e-01 | 1.40e+01 |
| fav_cor | 1280 | 8.54e-02 | 8.56e-02 | 1.02e-01 | 1 | 2.13e-01 | 4.09e+02 | 2.52e-01 | 9.83e+00 |
| fav_cor | 2560 | 6.87e-02 | 7.84e-02 | 1.04e-01 | 1 | 2.63e-01 | 4.15e+02 | 2.12e-01 | 9.54e+00 |
| fav_cor | 5120 | 7.02e-02 | 5.31e-02 | 7.41e-02 | 1 | 1.58e-01 | 2.96e+02 | 1.51e-01 | 6.68e+00 |
| fav_cor | 10240 | 3.73e-02 | 4.09e-02 | 4.38e-02 | 2 | 1.11e-01 | 1.75e+02 | 1.12e-01 | 5.37e+00 |
| fav_cor | 40960 | 3.24e-02 | 2.73e-02 | 3.36e-02 | 1 | 6.72e-02 | 1.34e+02 | 7.02e-02 | 3.94e+00 |
| fav_cor | 163840 | 8.60e-03 | 1.07e-02 | 1.10e-02 | 1 | 2.20e-02 | 4.41e+01 | 2.92e-02 | 1.67e+00 |
| masked | 40 | 9.98e-01 | 9.92e-01 | 9.98e-01 | 4 | 4.47e+00 | 3.99e+03 | 1.41e+02 | 1.00e+01 |
| masked | 80 | 9.77e-01 | 5.35e-01 | 9.77e-01 | 6 | 6.96e+00 | 3.91e+03 | 1.84e+00 | 1.10e+01 |
| masked | 160 | 6.23e-01 | 2.44e-01 | 6.53e-01 | 5 | 3.92e+00 | 2.61e+03 | 6.85e-01 | 1.20e+01 |
| masked | 320 | 9.92e-01 | 2.23e-01 | 9.92e-01 | 9 | 9.92e+00 | 3.97e+03 | 5.76e-01 | 1.30e+01 |
| masked | 640 | 9.99e-01 | 1.23e-01 | 9.99e-01 | 10 | 1.10e+01 | 4.00e+03 | 2.69e-01 | 1.36e+01 |
| masked | 1280 | 1.00e+00 | 1.20e-01 | 1.00e+00 | 12 | 1.30e+01 | 4.00e+03 | 2.61e-01 | 1.34e+01 |
| masked | 2560 | 1.00e+00 | 9.54e-02 | 1.00e+00 | 18 | 1.90e+01 | 4.00e+03 | 2.05e-01 | 1.18e+01 |
| masked | 5120 | 1.00e+00 | 4.63e-02 | 1.00e+00 | 20 | 2.10e+01 | 4.00e+03 | 9.56e-02 | 5.79e+00 |
| masked | 10240 | 1.00e+00 | 3.64e-02 | 1.00e+00 | 22 | 2.30e+01 | 4.00e+03 | 7.44e-02 | 4.76e+00 |
| masked | 40960 | 1.00e+00 | 2.28e-02 | 1.00e+00 | 25 | 2.60e+01 | 4.00e+03 | 4.64e-02 | 3.27e+00 |
| masked | 163840 | 1.00e+00 | 8.01e-03 | 1.00e+00 | 27 | 2.80e+01 | 4.00e+03 | 1.61e-02 | 1.24e+00 |

- Lemma 1 check: the grid minimum of q_φ(S₀) over 201 values of φ equalled the endpoint minimum in every one of the
  246 runs (max |Δ_grid − Δ| = 0.0e+00).
- In the favourable designs Δ_n ≈ c·n^{−1/2}, as T03 and T22(iii) at κ = ½ predict. With the realised (ideal-grid)
  T ∈ {1, 2}, (P1) is met in the limit and is ≈ 0.02 at n = 163,840. **With T^max = 4,000 it is ≥ 44 even at
  n = 163,840**, so the deterministic-budget form of (P1) needs n of order 10⁸–10⁹ in these designs.
- The frozen P2 quantity (L+4)ρ* is still ≥ 1 at n = 163,840, while ρ̄ + u_π ≈ 0.03. Removing P2 (Lemma 3) is
  therefore not cosmetic.
- `masked`: as n grows, 1 − π₀(S₀) → 1 (T27-type masking) and the ideal T grows (22 at n = 10,240). (P1) fails, as
  it should; the theorem is silent there.
- `T_ideal` is the full-space-ESS grid (threshold 0.9, 60 halvings). It is only a **proxy** for the method's grid
  (pilot plus restricted V-ESS). The bounds hold for any frozen grid; only the size of T is proxied.

**4.2 ORTH family** (`orth_check.py` → `results/orth_check.csv`; p = n/2, s₀ = 3, θ = 0.6, 3 seeds):

| n | p | B | max|R| (max over seeds) | median 1−π₀(S₀) | median (T^max+1)(1−π₀(S₀)) |
|---|---|---|---|---|---|
| 200 | 100 | 10 | 0.164 | 1.896e-01 | 758.5 |
| 400 | 200 | 14 | 0.153 | 1.306e-01 | 522.4 |
| 800 | 400 | 16 | 0.125 | 9.433e-02 | 377.4 |
| 1600 | 800 | 16 | 0.122 | 6.713e-02 | 268.6 |
| 3200 | 1600 | 16 | 0.116 | 4.898e-02 | 196.0 |
| 6400 | 3200 | 16 | 0.113 | 3.464e-02 | 138.6 |

max|R| (the EXP′ remainder over every within-block addition) stays bounded, as Proposition C claims. 1 − π₀(S₀)
decays like √(log n/n), which is the T22(iii) rate at κ = ½. So T22(iii) is attained here, not loose, and
(T^max+1)(1 − π₀(S₀)) stays ≫ 1 for every n tried.

**4.3 Final-run simulations** (`smc_sim.py`, `run_sims.sh` → `results/smc_sim.jsonl`). These are exact-score
simulations of the potential uninterrupted final run: the 4-island SMC with the actual move round, multinomial
resampling, L burn-in and 4 measured rounds, run on the ideal grid. Means over reps × 4 islands:

| design | n | N | reps | T | Δ_n | E|W_r−1| | bound b | E occupancy (end T / round starts) | its bound | E max_j PIP err (island) | bound (A-0)(c) | old (L+5/2)ρ̄ bound | exact-posterior PIP err | MPM wrong |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fav_iid | 320 | 2500 | 10 | 1 | 0.142 | 3.30e-03 | 6.61e-01 | 0.142 / 0.142 | 1.000 | 2.89e-02 | 1.42e+00 | 4.14 | 2.89e-02 | 0.00 |
| fav_iid | 5120 | 2500 | 10 | 1 | 0.0553 | 2.19e-03 | 2.34e-01 | 0.056 / 0.055 | 0.579 | 1.42e-02 | 7.31e-01 | 2.08 | 1.42e-02 | 0.00 |
| fav_cor | 5120 | 2500 | 10 | 1 | 0.0528 | 4.88e-03 | 2.23e-01 | 0.048 / 0.049 | 0.542 | 1.15e-02 | 6.73e-01 | 1.84 | 1.15e-02 | 0.00 |
| fav_cor | 163840 | 2500 | 10 | 1 | 0.00842 | 1.02e-03 | 3.40e-02 | 0.008 / 0.008 | 0.084 | 1.34e-03 | 1.05e-01 | 0.38 | 1.34e-03 | 0.00 |
| masked | 640 | 2500 | 10 | 10 | 1 | 1.43e-02 | 1.49e+05 | 0.121 / 0.121 | 1.000 | 3.91e-02 | 1.26e+00 | 2.69 | 3.91e-02 | 0.00 |
| masked | 5120 | 2500 | 10 | 20 | 1 | 2.13e-02 | ∞ (Δ_n = 1 to double precision) | 0.037 / 0.037 | 1.000 | 6.72e-03 | 1.08e+00 | 1.62 | 6.72e-03 | 0.00 |
| fav_iid | 320 | 50 | 40 | 1 | 0.142 | 2.49e-02 | 6.61e-01 | 0.137 / 0.143 | 1.000 | 2.89e-02 | 1.42e+00 | 4.14 | 2.89e-02 | 0.00 |
| fav_cor | 5120 | 50 | 40 | 1 | 0.0528 | 2.96e-02 | 2.23e-01 | 0.051 / 0.048 | 0.542 | 1.15e-02 | 6.73e-01 | 1.84 | 1.15e-02 | 0.00 |
| masked | 5120 | 50 | 40 | 20 | 1 | 1.63e-01 | ∞ (Δ_n = 1 to double precision) | 0.036 / 0.036 | 1.000 | 6.71e-03 | 1.08e+00 | 1.62 | 6.72e-03 | 0.00 |

Every (A-0) bound holds. The realised occupancy matches δ₁, and the PIP error equals the exact-posterior PIP error, so
the Monte Carlo error is negligible at these sizes. The bounds are loose by about 30–200× for the evidence and 50–80× for the PIPs, mostly from the factor 2 in
2δ₁ + 2b and the (T+1) sum in b. Runs with N = 50 also satisfy the bounds, which are free of N.

**4.4 Lemma 2 check** (`check_rho_bar.py` → `results/check_rho_bar.txt`; 200,000 one-round paths from S₀): the
simulated departure frequency agrees with the exact ρ̄ = 1 − ∏_e(1 − k_e) to within 1 s.e. in all 3 designs
(e.g. 0.1162 vs 0.1155). The sum bound is ≤ 10% above ρ̄, while (B+3)u_π, i.e. ρ*, is 4–8× above ρ̄.

## 5. What fails and why

- **The frozen (L+4)ρ* route** (T23(ii-c) with BASIN({S₀})) is valid but wasteful. It pays departure in all L + 4
  terminal rounds, because occupancy is controlled only at the end of stage T. It is replaced, not refuted.
- **Removing the (T+1) factor from (P1)** is not possible on the locked evidence route. T14 is a telescoping
  first-moment bound summed over stages, and T14(i-d) shows its endpoint term is essential. Any premise weaker than
  (T+1)Δ_n → 0 needs a new evidence theorem (for example PW2 → T25(iv), not assumed here).
- **Replacing realised T by something bounded.** In the favourable scans T_ideal ≤ 2, but there is no locked result
  bounding the method's realised T. The weights entering the ESS at φ = 2v − u > 1 are not controlled by Δ_n, so even
  "Δ_n small ⇒ T small" is not available. Hence the honest deterministic form uses T^max = 4,000, which makes (P1)
  practically vacuous (§4.1).
- **Secondary PIP:** dropped, as required (FROZEN_LIST); not needed.
- **Masked regime:** Δ_n → 1, so the bound is vacuous. No claim.
- **Study scale (n = 200, p ∈ {500, 1000}):** the preliminary data put the median π₀(S₀) at about 10⁻¹², so Δ_n ≈ 1,
  and SE is impossible. The theorem explains the mechanism only.

## 6. Needs escalation

1. **Lemma 3's use of T15 at position (b).** The step reads "after L + h − 1 complete terminal rounds" as a "fixed
   elementary prefix" (T15 𝒯(b) ← T12(i.b)). I believe this is exactly T12(i.b), but the redundancy of the frozen
   premise rests on it, so an independent reviewer should confirm it.
2. **Proposition C (EXP′ under ORTH).** It is a sketch. The χ² lower tail and union bound are not written out, and the
   method's partition under exact ties was not traced. It overlaps W1-EXP.
3. **OUT.** Whether any v3 failure mode (`resource_limit` after allocation, `numerical_failure` in the final run) can
   return a *partial* evidence or PIP that differs from the potential run's. This is an implementation question for
   Felipe. If OUT fails, the composition needs an extra term.
4. **T03 + T02(i) combined** (used by Theorem B) has not been separately reviewed (register scope note).

## 7. Outside scope

- In the `masked` design (Δ_n = 1), the simulated final run still estimates Z within 1.4% (n = 640, T = 10) and 2.1%
  (n = 5120, T = 20) in mean absolute relative error, with PIP errors equal to the exact-posterior ones, at N = 2,500
  (16% evidence error at N = 50) (`results/smc_sim.jsonl`). The sampler works where T26 is silent; at
  p = 18 this is unsurprising, but it is a reminder that T26 is sufficient only.
- Under ORTH with zero leakage, 1 − π₀(S₀) ≈ c√(log n/n): each null variable's table contributes about
  (1/2p)·n^{−1/2}·e^{χ²₁/2}, and the heavy-tailed sum over p nulls is of order √(log p). This makes T22(iii)'s κ = ½
  rate attained, and it is relevant to T38(a) via T11(iii): Q_f·π₀(S₀) is then huge, so the favourable-regime HPM
  route is fine even though (P1) with T^max is not.
- ρ* = (B+3)u_π overstates the true departure ρ̄ by 4–8× in these designs; the exact form ρ̄ = 1 − ∏(1 − k_e) is cheap
  and could replace ρ* in T24/T37-type statements.

## 8. Confidence card

| Item | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| T26(i) evidence | Theorem A (A-i) under (Ω), (P1), (P1-ex), OUT | high | high (done here, candidate) | none inside; input is (P1) | no |
| T26(ii) PIPs / MPM | Theorem A (A-ii), **without** (L+4)ρ* → 0 | high | high (done; Lemma 3 needs the check in §6.1) | T15 at terminal prefixes | no |
| (P1) in R1 | (T^max+1)Δ_n → 0 ⇐ T03 + T22(iii) | high (asymptotic) | medium: conditional on EXP′, VIS, NL being proved for a family; Prop C does it for ORTH (sketch) | EXP′ for the actual partition in p ≫ n designs | no |
| Joint compatibility (Astra) | ORTH-F satisfies all Theorem B hypotheses | high | high (sketch → full proof is routine) | χ² tail bookkeeping | no |
| Finite-n relevance | (A-0) bounds | true but loose; vacuous at n = 200 and whenever T^max is used | — | Δ_n ≈ 1 at study scale | no (would need a different evidence theorem) |
