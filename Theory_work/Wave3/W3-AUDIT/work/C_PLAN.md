# W3-AUDIT track C — PLAN (light empirical check; internal only, not for the paper)
Planner: Claude Sonnet 5.5, 2026-11-16; v2 (manager revision: A_inventory reconciliation §2b, proxies P8–P10 added); **v3 (track C lead, Opus 5.5, 2026-11-16, HQ rule 11-16): explicit-constant checks are removed (explicit constants from the proof are conservative); the proxies measure the QUALITATIVE conditions and their trend in n: floors bounded below, β_min on the √(log n/n) scale, leakage/visibility/localisation sizes bounded or slowly growing, margins positive.** Implementation: Python (numpy/scipy) in `track_C/scripts/` (see §4).
Kind-B list: `work/A_inventory.md` (commit 2e6c7d86; 57 kind-B rows, 41 distinct assumption ids) for CLAIMS_CARD v1.6 rows 1.1, 1.2, 1.3, 2.1, 3.1, 3.5, 3.6; reconciliation in §2b.
File:line citations are relative to `Theory_work/Wave3/` unless noted. Abbreviations: POST = `W3-POST/STATEMENT.md`, POST2 = `W3-POST2/STATEMENT.md`, RM = `W3-RM/STATEMENT.md`, RM2 = `W3-RM2/STATEMENT.md`, DIST = `W3-DIST/STATEMENT.md`, DL = `../Wave2/W2-APP/data_diag/diag_lib.R`.

**Row → design-side assumption.** 1.1: (E) POST:67, (F_λ) POST:68, (F_w) POST:71, (BM) POST:74; Thm 1′ (ID^M; c) POST2:40-41, (OS)/(DG) POST2:35-38. 1.2: Cor 1R floors LSF (i)/(ii) POST:106. 1.3: witness designs (orthogonal or Gaussian null columns) = IND, inside by construction, no proxy. 2.1: (A4) DIST:179 (population Corr, window q_n = min{p, ⌈C_q M log n⌉}, C_q = 2(s(A+2)+4)/log 2, DIST:168); (A3) and (A5) are automatic for Gaussian rows with bounded β. 3.1 and 3.6: T1-R/FL-R/V-R/L-R RM:129-137; RM2 (FL-Q), (V), (L^b), (BM-W), (W-loc) RM2:130-159; (L-R^b) RM2:176. 3.5: no design condition, no proxy.

## 1. Designs (Gaussian rows N(0, Σ), standardised; s₀ = 4, σ = 1; 19 designs)
Common truth, two placements per X: **spread** = study positions (`gen_dev_data.R:33`, step = ⌊p/s₀⌋), β = (1.4, −1.0, 1.8, −1.2); **clustered** = four consecutive columns inside one correlated group or block, aligned β = (1.4, 1.0, 1.8, 1.2) (the NEG regime of P6, `W3-P6/DESIGN.md` §1).
| ID | Σ (unit diagonal) | parameters |
|---|---|---|
| D01 | IND | I (= S1, `gen_dev_data.R:18`) |
| D02–D04 | AR(ρ) | ρ = 0.5 (= S2), 0.8, 0.95 |
| D05–D06 | block compound symmetry, blocks of 5 | ρ_b = 0.7 (= S3), 0.85 (= S4) |
| D07 | block CS, growing blocks | block size ⌈√p⌉, ρ_b = 0.5 (growing one-factor groups, RM) |
| D08–D09 | Toeplitz, algebraic decay | Σ_jk = (1+\|j−k\|)^(−α), α = 1, 2 (outside the exponential-decay class of W2-APP LOC) |
| D10–D15 | factor, spike λ₁ ≈ 0.5 p^a | x = √h_p Lf + √(1−h_p) e, h_p = 0.5 p^(a−1) split over k_f factors; a ∈ {0.5, 0.75, 1}, k_f ∈ {1, 3}; a = 1, k_f = 1 is P6 cs(0.5); k_f = 3 uses loadings 1, (−1)^j, group-wise ±1 (P6 `fac2`) |
| D16–D17 | study S5, S6 | 0.3·11ᵀ + 0.4H + 0.3I; block ρ = 0.4 + 0.1·((g−1) mod 6) (`gen_dev_data.R:21-22`) |
| D18 | real-data-like: riboflavin | Σ_δ = 0.9 R + 0.1 I, δ = 0.1, R = riboflavin sample correlation (n_data = 71, p = 4088, rank 70; hdi 0.1-10, CRAN Archive). Exact factor form is in `Wave2/W2-SIM/X/data/riboflavin_L.csv` (made by `make_real_lambda.R:1-30`). p < 4088: fixed-seed random column subset. p > 4088: block-diagonal tiling of independent copies |
| D19 | real-data-like: FRED-QD | same recipe, `fred_qd_L.csv` (p = 170, tiled; macro series, one mild factor, top-1 trace share 0.26) |
Seeds: `seed = base + 10000·design + rep`, `RNGkind("Mersenne-Twister","Inversion","Rejection")`, X drawn first (`gen_dev_data.R:52-54`). 10 replicates of X per (design, n, p); both placements are scored on the same X.

## 2. Proxies (what each STATEMENT assumption becomes a number)
Sample proxies use the realised standardised X; "pop" proxies use Σ (n-free). A sparse minimum found by search is an UPPER bound on the true minimum, so it can refute but never certify; certification uses the refined Gershgorin lower bound already in DL:161.
| P | Assumption (source) | Exact formula | Method, source | Cost, largest cell |
|---|---|---|---|---|
| P1 | (F_λ) anchored sparse floor, POST:68; LSF(i) POST:106 | φ̂²(k) = min over \|J\| ≤ k of λ_min(R̂_{S₀∪J}), k ∈ {0, 2, 4, 8, 16, j₀}, j₀ = ⌈(2A+1)s₀⌉+1, A = log p/log n (s₀ = 4: 13 at A = 1, 21 at A = 2) | k = 2 exact (1−max\|r\|); exact enumeration when C(p,k) ≤ 2·10⁵; otherwise greedy chain started at S₀ (`DL:123`) plus swap refinement, and Gershgorin lower bound (`DL:161`) | ≤ 120 s |
| P2 | (F_w; g₀) POST:71; (A4) DIST:179; LSF(ii) POST:106 | λ̂_min(R̂_T) over \|T\| ≤ m♯_n (m♯ from `DL:83` = POST:37; sizes 2…64 also reported), unanchored greedy chain from the top pair; pop: λ_min(Σ) itself (exact, a lower bound for every set size, so it certifies the population floors of (A4)/LSF(ii)) | same chain extended to k = m♯_n (≈ 85 at s₀ = 4, p = 2·10⁴, n = 200) | in the P1 run; pop 60 s |
| P3 | (FL-Q) RM:94, RM2:130 | min over l ∈ [p] of λ_min(R̂_{Q̂∪{l}}), Q̂ from P5 | exact for all l (bordered eigenvalue, O(p\|Q̂\|²)) | 10 s |
| P4 | (V) RM:95 (RM2:130); pop (V-R) = PTV(a₀) RM:135 | v̂ = min over j ∈ S₀, \|U\| ≤ 15 of δ²_{U,j}/log n, δ²_{U,j} = ‖(P_{U∪j} − P_U)μ‖², μ = Xθ*; pop â₀ = min \|Cov(W_j, Σ_k θ*_k W_k \| W_U)\| | greedy masking: add the column that most lowers the gain, updated by rank-one residual products (O(np) per step), plus exact search over \|U\| ≤ 2 on the top-200 candidates | 15 s |
| P5 | (L^b)/(L-R^b) leakage RM2:132, :176; (L-gain) RM:99; b < β(η,A) = ½ − η/2 − √(2Aη) RM2:35 | **pop (Form R, the one for Gaussian rows):** g_l = max over \|U\| ≤ 15, j ∈ S₀∖U of \|Cov(W_l, W_j \| W_U)\|; Q̂_ε(n) = S₀ ∪ {l : g_l > ε√(log n/n)}, ε ∈ {0.5, 0.2, 0.1}; report \|Q̂_ε(n)\| and its trend in n (bounded or slowly growing = inside; growing like a power of n or = [p] = outside). (v3: the β(η, A) exponent comparison and the Form F sample diagnostic are dropped.) | U family = {∅, S₀∖j, every prefix of the population greedy masking path of each j}, all l scored, so Q̂ is a SUBSET of the true leak set (b̂ is a lower bound) | 30 s |
| P6 | (W-loc) RM2:159; \|H_l\| ≤ n^ρ, 15ρ + b < ½ RM2:176 | for l ∈ [p], lattice sets T ∈ {S₀ ∪ random subsets of Q̂ of sizes 0, \|Q̂\|/4, \|Q̂\|/2, all}, 5 draws each: L̂(ν) = smallest ℓ¹ tail ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ with N_l the ν largest coefficients; report ν̂ at L = 0.1 and 0.05 (bounded or slowly growing in n = inside); and degrees #{k : \|r_lk\| > τ}, τ ∈ {2√(log n/n), 0.3, 0.5} (`DL:257`) as \|H_l\| | regression of all p columns on each T: one Cholesky of X_T and one Xᵀ·residual product (n p \|T\|) | 20 s |
| P7 | (BM) POST:74; (ID^M) POST2:40-41; (E) | M̂ = ‖μ‖²/n = θᵀR̂θ (bounded); BM rate = θ_min² n φ̂₀²/(σ² log n) (β_min on the √(log n/n) scale: growing = inside); margin Δ̂/(σ² log n), Δ̂ = min over j ∈ S₀ and greedily chosen \|J\| ≤ j₀ of ‖(I − P_{(S₀∖j)∪J})μ‖² (positive and growing = inside) | greedy forward selection of proxies for the removed truth (an upper bound on the min) | 10 s |
| P8 | (OS)/(ADG)/(DG) POST2:35-38 and the necessity bound A2 POST2:58 (δ_n ≥ 𝒪⁰_n/(1+𝒪⁰_n)) | 𝒪¹_n = [(s₀+1)/(2p−1−s₀)]·Σ_{l∉S₀}(D_{S₀}/D_{S₀∪{l}})^{1/2}, D_S = det H_S/det(G_S+I), H_S = (n+1)G_S + I (POST:22); compare with r_n = √(log n/n). j = 2 term: pairs among the top-200 l by D-ratio | exact over all l from one Cholesky of X_{S₀} (Schur complement of H); the j = 1 term is Prop LB's term, a LOWER bound on 𝒪⁰_n, so a large value refutes, a small one does not certify | 5 s |
| P9 | (W-R)/(W) lattice width RM2:80, :140, :194; (W-χ) RM2:141 | (a) \|Q̂∖S₀\|/log n bounded ((W-χ) qualitative: Q = O(log n)); (b) 𝔴̂⁰ = mean over 20 draws g ~ N(0,I) of max over l and the P6 lattice sample T of \|u_{T,l}ᵀg\| − a⁰_n(\|T\|), a⁰_n(k) = √(log(n+1) + 2 log(p/(k+1))) | shares the P6 residual products; max over a SAMPLE of 𝔓 is a lower bound on the max over 𝔓, so 𝔴̂⁰ ≥ 0 refutes, < 0 does not certify | 10 s |
| P10 | (AG) Gram operator bound W2-FAC-A/STATEMENT.md:90 (W2-UNI:F-UNI, row 3.1) | δ̂_n√(p log log n), δ̂_n = ‖R̂ − Σ‖_op | 100 Lanczos steps, matvecs R̂v = Xᵀ(Xv/(n−1)) and Σv (dense) | 10 s |
Pre-announced expectations: global CS and strong factors (a = 1) give Q̂ = [p], so (L-size^b) fails (matches FAC and START).

**Reading conventions (internal; qualitative, v3).** Trend = log-log slope of the proxy in n at fixed p/n (p = n and p = 10n series; p = 2·10⁴ cells give the equal-n comparison). Floors (P1, P2, P3): *inside* if the search value is bounded away from 0 and flat or rising in n (the search value is an upper bound, so this is "not refuted, consistent"); population floors are *certified* by λ_min(Σ) > 0; *outside* if the search value falls toward 0 as n grows. P4 v̂ = δ̂²/log n and P7 BM rate / margin Δ̂/log n: *inside* if positive and growing in n; *outside* if bounded or falling to 0. P5 \|Q̂\|, P6 ν̂ and \|H_l\|, P9 \|Q̂∖S₀\|/log n: *inside* if bounded or slowly (≲ log n) growing; *outside* if Q̂ = [p] or growing like a power of n; P5 is never "inside" outright (Q̂ is a subset): "not refuted". P8: *inside* if 𝒪¹_n/r_n is bounded and non-increasing (a large value refutes; a small one does not certify). P9 width: *inside* if 𝔴̂⁰ < 0 and falling (a sample max is a lower bound on the lattice max). P10: inside if δ̂_n√(p log log n) → 0 (expected outside for every p ≥ n, since ‖R̂ − Σ‖_op ≳ √(p/n)). Mixed or flat-near-zero = *unclear*.

## 2b. Reconciliation with A_inventory (kind-B ids, deduplicated over the tiers D/R/S; id → proxy)
| Proxy | A_inventory ids covered |
|---|---|
| P1 | SPARSE-EIG, POST2-FLAMBDA, POST2-F0 (k = 0), COEF-REP (S₀ floor + M̂ from P7), RM-FLR (k = 16 + s₀ part, pop) |
| P2 | SPARSE-EIG (O(log n) part), LSF, DIST-A4, DIST-ND (= (ADG), implied by (F_w) via B2), POST2-C-ALT (the three alternatives = P1 ∧ P2, or P1 ∧ P8, or P8 ∧ P7) |
| P3 | GRAM-FLOOR-LATTICE, RM-FLR (Q ∪ {l} part) |
| P4 | PTV, BLOCK-VIS (block-relative is weaker than the full-U search of P4, so covered conservatively) |
| P5 | RELEVANCE-SIZE, RM2-LSIZE-B-R, RM2-LFEAS (add the arithmetic check \|Q̂\| ≤ K and K ≥ 2\|Q̂\| + 32 s₀ + 1), RM2-LGAIN-R |
| P6 | RM2-LLOC-R, RM2-HSIZE-RHO (marginal degrees and sampled conditional covariances only; the full "every U" form is not computable) |
| P7 | BETAMIN (rate form), POST2-IDM (margin positive and growing), ENERGY (M̂), DIST-L0 (B ≤ (‖μ‖² + ‖θ‖²)/n, a function of M̂) |
| P8 | POST2-OS, DIST-ND (second route) |
| P9 | RM2-W-R |
| P10 | GRAM-OP-BOUND |
**B assumptions with no proxy, and why.** (i) *Data-law, true by the generator, nothing to measure:* GAUSS-NOISE, IID-GAUSS-ROWS, DIST-A1, DIST-A3 (Gaussian rows are sub-Gaussian with K = 1), DIST-RD, MISR-GRC (discharged from A1 by W3-DIST:B0). (ii) *Fixed by the experiment's parameters, recorded not tested:* FIXED-S0, DIST-SPARSE, DIST-A2, P-POLY (A_cell = log p/log n is printed per cell), COEF-BOUNDED and DIST-A5 (β_min ∈ [1, 1.8], σ = 1), EXT-FEAS and DIST-DOM (arithmetic: s₀ + 1 ≤ ⌊n/2⌋, p ≥ 2; hold in every cell). (iii) *Not computable by search:* DIST-TR0 (population vs sample second moments on S₀; the quantity is the sample covariance error on a fixed 4-set, O_P(n^{-1/2}) for Gaussian rows, so a measurement would only confirm the CLT; it is covered by P1 at k = 0, which reports λ_min(R̂_{S₀}) next to the population value). The exact lattice supremum in P9 and the exact infimum over all U in P4/P5/P6 are also not computable; those proxies are one-sided as stated.

## 3. Grid
n ∈ {200, 400, 800, 1600}; p ∈ {n, 10n, min(n², 2·10⁴)}: p = 200, 2000, 2·10⁴; 400, 4000, 2·10⁴; 800, 8000, 2·10⁴; 1600, 16000 (at n = 1600 the cap and 10n nearly coincide, so the third p is dropped). 11 cells × 19 designs × 10 X-replicates × 2 placements. A_cell = log p/log n (1 to 1.9). Question per proxy and design: is it inside at the largest n (1600, p = 10n), and does the proxy's trend in n (slope of log proxy on log n, p/n fixed) move toward inside? A second question: does inside-ness depend on p/n (cells at equal n). Scientific caution: j₀ = 21 and k log p/n ≈ 1 at (n = 200, p = 2·10⁴), so P1 is expected to fail for every design at the smallest n and recover with n; the trend is the point.

## 4. Compute (proxy computations; no SMC fits)
Per-instance seconds at the cell, 1 core (OPENBLAS_NUM_THREADS = 1), dense R at p = 2·10⁴ is 3.2 GB (so `--mem=12G`); E = time-capped sparse search (`tlimit_total` = 120):
| n | p = n | p = 10n | p = cap (2·10⁴) |
|---|---|---|---|
| 200 | 6 | 30 | 170 (Gram 8 + E 60 + P3–P9 ×2 placements 80 + P10 10 + I/O 12) |
| 400 | 10 | 55 | 215 |
| 800 | 18 | 105 | 270 |
| 1600 | 45 | 325 (p = 16000) | — |
Per design, one replicate set: 1249 s; 10 replicates: 3.47 core-h; 19 designs: **65.9 core-h**.
| | cells | core-h nominal |
|---|---|---|
| Owls (p ≤ 2000 cells, pilot, development) | 5 of 11 per design: 109 s × 10 × 19 = 5.75 | 5.75 + population layer 1.0 + pilot calibration 1.5 = **8.3** |
| NOTS (p ≥ 4000 cells) | 6 per design: 1140 s × 10 × 19 = 114 array tasks (60.2); plus 19 population tasks (2.5) | **62.7** |
| Total nominal | | **71.0** |
Hard cap: each NOTS task gets a time limit of 2.0 × its estimate (max 4 h), so the NOTS worst case is 2.0 × 62.7 = 125 core-h ≤ 150 (25 core-h reserve for one rerun round). Gate: the Owls pilot (3 designs × 4 cells) gives measured seconds; if measured > 1.3 × estimate, reduce to 5 replicates and drop D19 before NOTS submission (nominal then ≈ 31 core-h NOTS). Wall time ≈ 4 h at 60 concurrent tasks.
**v3 measured basis (Owls pilot 2026-11-16, supersedes the estimates above).** Python implementation; s/replicate (max over D01, D05, D14, D18): (200, 2·10⁴) 84, (400, 4000) 5, (400, 2·10⁴) 83, (800, 8000) 24, (800, 2·10⁴) 199, (1600, 16000) 166; population layer computed inside each task (≈ 6 s). NOTS: 114 tasks, **29.8 core-h nominal, 66.5 core-h ceiling** at 2× limits; Owls part (p ≤ 2000) took 0.30 core-h. Package and README: `track_C/nots/`. Scripts are in `track_C/scripts/` (Python: c_designs.py, c_proxies.py, c_run_cell.py, c_test.py, c_collect.py), replacing the R file names below.
**Scripts (v2 naming, superseded by the v3 note above)** (all in `Theory_work/Wave3/W3-AUDIT/work/trackC/`; sourced from `DL` where it exists, no change to `DL`):
- `c_proxies.R` — P1–P10 functions plus a brute-force test on p ≤ 30 (exact enumeration vs the greedy); **Opus helper** (subtle logic: anchored chains, rank-one visibility updates, lattice sampling).
- `c_designs.R` — `design_sigma(id, p)` and `draw_X(id, n, p, rep)` (D01–D19, `gen_dev_data.R:18` and `riboflavin_L.csv` reused), **Sonnet helper**.
- `c_run_cell.R` (args: design n p reps; writes `out/<id>_<n>_<p>.csv`), `c_make_tasks.R` (task table with the time limits above), `c_collect.R` (builds the output table below), **Sonnet helper**.
- `c_submit.sh` — Slurm array, copy of the P6 pattern (`W3-P6/nots/submit_table.sh:23`; account commons, 1 CPU); **Engineering schedules it; they write no analysis code**.
No Fable time; reviewer = the Opus helper's brute-force test passing, then the manager reads the table.

## 5. Output
`track_C/RESULTS.md` plus `track_C/summary.csv` (v3 path): ONE table, rows = 19 designs, columns = P1 … P10. Each cell: verdict (inside / outside / unclear / not refuted) at (n = 1600, p = 10n), the key number, and the trend over n = 200 → 1600 (↑, →, ↓ with the log-log slope). Footer: the pre-announced items of §2 (confirmed or not). Internal only: the advisor report does not cite it, and a "designs outside" result goes to the correctness route (SUSPECT/NARROW) only through Fable's track B reading.
