# W3-AUDIT track C — PLAN (light empirical check; internal only, not for the paper)
Planner: Claude Sonnet 5.5, 2026-11-16. Plan only; nothing was run. Constants below marked "hand" are arithmetic from the STATEMENTs, to be re-checked by the helper.
`work/A_inventory.md` does not exist yet, so the kind-B list is read from CLAIMS_CARD v1.6 rows 1.1, 1.2, 1.3, 2.1, 3.1, 3.5, 3.6 and their STATEMENTs. Reconcile with A's kind-B rows when A lands (add or drop a proxy; nothing else changes).
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
| P1 | (F_λ) anchored sparse floor, POST:68; LSF(i) POST:106 | φ̂²(k) = min over \|J\| ≤ k of λ_min(R̂_{S₀∪J}), k ∈ {2, 4, 8, j₀}, j₀ = ⌈(2A+1)s₀⌉+1, A = log p/log n (s₀ = 4: 13 at A = 1, 21 at A = 2) | k = 2 exact (1−max\|r\|); exact enumeration when C(p,k) ≤ 2·10⁵; otherwise greedy chain started at S₀ (`DL:123`) plus swap refinement, and Gershgorin lower bound (`DL:161`) | ≤ 120 s |
| P2 | (F_w; g₀) POST:71; (A4) DIST:179; LSF(ii) POST:106 | ĝ = (n−1)·λ̂_min(R̂_T) over \|T\| ≤ m♯_n (m♯ from `DL:83` = POST:37); pop: ψ̂_n√n/(log n)^(3/2), ψ̂_n = λ̂_min(Σ_S) over \|S\| ≤ k̄_n (POST:106); pop: n·λ̂_min(Σ_T) over \|T\| ≤ q_n(M = 1) (= the c_ψ of (A4)) | same chain extended to k = m♯_n (≈ 85 at s₀ = 4, p = 2·10⁴, n = 200) | in the P1 run; pop 60 s |
| P3 | (FL-Q) RM:94, RM2:130 | min over l ∈ [p] of λ_min(R̂_{Q̂∪{l}}), Q̂ from P5 | exact for all l (bordered eigenvalue, O(p\|Q̂\|²)) | 10 s |
| P4 | (V) RM:95 (RM2:130); pop (V-R) = PTV(a₀) RM:135 | v̂ = min over j ∈ S₀, \|U\| ≤ 15 of δ²_{U,j}/log n, δ²_{U,j} = ‖(P_{U∪j} − P_U)μ‖², μ = Xθ*; pop â₀ = min \|Cov(W_j, Σ_k θ*_k W_k \| W_U)\| | greedy masking: add the column that most lowers the gain, updated by rank-one residual products (O(np) per step), plus exact search over \|U\| ≤ 2 on the top-200 candidates | 15 s |
| P5 | (L^b)/(L-R^b) leakage RM2:132, :176; (L-gain) RM:99; b < β(η,A) = ½ − η/2 − √(2Aη) RM2:35 | **pop (Form R, the one for Gaussian rows):** g_l = max over \|U\| ≤ 15, j ∈ S₀∖U of \|Cov(W_l, W_j \| W_U)\|; Q̂_ε(n) = S₀ ∪ {l : g_l > ε√(log n/n)}, ε ∈ {0.5, 0.2, 0.1}; b̂ = log\|Q̂_ε\|/log n against β(η, A_cell), η ∈ {0.01, η_A/2}, η_A = (√(2A+1) − √(2A))² (0.101 at A = 1, 0.056 at A = 2). **Sample diagnostic (Form F as written):** g_l^F = max δ²_{U,l}/τ²_U against η log n | greedy over U for the 2000 columns with the largest marginal \|Σ_lj\| plus 2000 random columns, so Q̂ is a SUBSET of the true leak set (b̂ is a lower bound) | 30 s |
| P6 | (W-loc) RM2:159; \|H_l\| ≤ n^ρ, 15ρ + b < ½ RM2:176 | for l ∈ [p], lattice sets T ∈ {S₀ ∪ random subsets of Q̂ of sizes 0, \|Q̂\|/4, \|Q̂\|/2, all}, 5 draws each: L̂(ν) = smallest ℓ¹ tail ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ with N_l the ν largest coefficients; report ν̂ at L = 0.1 and 0.05 against h·log n/log 2, h = ½ − b̂ − 0.05; and degrees #{k : \|r_lk\| > τ}, τ ∈ {2√(log n/n), 0.3, 0.5} (`DL:257`) as \|H_l\| | regression of all p columns on each T: one Cholesky of X_T and one Xᵀ·residual product (n p \|T\|) | 20 s |
| P7 | (BM) POST:74; (ID^M; c) POST2:40-41 with c > c₁ POST2:127-128; BM(c) with c > c₀ POST:74 | BM ratio = θ_min² n φ̂₀²/(σ² log n) divided by c₀(s₀,A) ≥ 32[s₀(A+1)+2]; margin ratio = Δ̂/(σ² log n c₁), Δ̂ = min over j ∈ S₀ and greedily chosen \|J\| ≤ j₀ of ‖(I − P_{(S₀∖j)∪J})μ‖², c₁ = (√(2C_x) + √(2C_x + C_A j₀ + (2/log 2)(s₀(A+1)+2)))², C_x = A j₀ + s₀ + log(j₀+1) + 2, C_A = 8+3A | greedy forward selection of proxies for the removed truth; also report n* = the n at which the ratio reaches 1 by extrapolating n/log n | 10 s |
**Hand-computed expectations, pre-announced (to be confirmed):** c₀ ≥ 320 and c₁ ≈ 452 at (s₀, A) = (4, 1); c₀ ≥ 448 and c₁ ≈ 961 at (4, 2). With β_min = 1, σ = 1 and IND, Δ_S ≤ n·β_min², so the explicit constants need n/ln n ≳ 450, i.e. n ≈ 3.7·10³ for c₁ and ≈ 2.5·10³ for c₀ (both with φ₀ = 1). So P7 will say "outside at every n ≤ 1600 with explicit constants, inside in rate form" for every design. Form F leakage (P5 sample diagnostic) will fail for Gaussian rows: a null column's sample gain δ² has mean θᵀΣθ ≈ 4.4 ≫ η τ² log n ≈ 0.4 (η = 0.01, n = 1600). It is a fixed-design condition, not a statement about Form R. Global CS and strong factors (a = 1) give Q̂ = [p], so (L-size^b) fails (matches the FAC and START results).

**Reading conventions (internal; not assumptions).** P1/P2/P3: "inside" if the Gershgorin lower bound is flat or rising in n and ≥ 0.05; "outside" if the search upper bound is ≤ 0.05 and non-increasing; else "unclear". P4: "inside" if the log-log slope of v̂ in n is > 0.5 and v̂ is bounded below by M_n log-growth; "outside" if v̂ < 1. P5: "outside" if b̂ ≥ β; "not refuted" otherwise (never "inside", since Q̂ is a subset). P6: "inside" if ν̂ ≤ h log n/log 2 and L̂ falls with n. P7: ratio ≥ 1.

## 3. Grid
n ∈ {200, 400, 800, 1600}; p ∈ {n, 10n, min(n², 2·10⁴)}: p = 200, 2000, 2·10⁴; 400, 4000, 2·10⁴; 800, 8000, 2·10⁴; 1600, 16000 (at n = 1600 the cap and 10n nearly coincide, so the third p is dropped). 11 cells × 19 designs × 10 X-replicates × 2 placements. A_cell = log p/log n (1 to 1.9). Question per proxy and design: is it inside at the largest n (1600, p = 10n), and does the proxy's trend in n (slope of log proxy on log n, p/n fixed) move toward inside? A second question: does inside-ness depend on p/n (cells at equal n). Scientific caution: j₀ = 21 and k log p/n ≈ 1 at (n = 200, p = 2·10⁴), so P1 is expected to fail for every design at the smallest n and recover with n; the trend is the point.

## 4. Compute (proxy computations; no SMC fits)
Per-instance seconds at the cell, 1 core (OPENBLAS_NUM_THREADS = 1), dense R at p = 2·10⁴ is 3.2 GB (so `--mem=12G`); E = time-capped sparse search (`tlimit_total` = 120):
| n | p = n | p = 10n | p = cap (2·10⁴) |
|---|---|---|---|
| 200 | 5 | 25 | 130 (Gram 8 + E 60 + P3–P7 ×2 placements 60) |
| 400 | 8 | 45 | 175 |
| 800 | 15 | 90 | 230 |
| 1600 | 40 | 285 (p = 16000) | — |
Per design, one replicate set: 1048 s; 10 replicates: 2.91 core-h; 19 designs: **55.3 core-h**.
| | cells | core-h nominal |
|---|---|---|
| Owls (p ≤ 2000 cells, pilot, development) | 5 of 11 per design: 93 s × 10 × 19 | 4.9 + population layer 1.0 + pilot calibration 1.5 = **7.4** |
| NOTS (p ≥ 4000 cells) | 6 per design: 955 s × 10 × 19 = 114 array tasks; plus 19 population tasks | 50.4 + 2.5 = **52.9** |
| Total nominal | | **60.3** |
Hard cap: each NOTS task gets a time limit of 2.5 × its estimate (max 4 h), so the NOTS worst case is 2.5 × 52.9 = 132 core-h ≤ 150 (18 core-h reserve for one rerun round). Gate: the Owls pilot (3 designs × 4 cells) gives measured seconds; if measured > 1.5 × estimate, reduce to 5 replicates and drop D19 before NOTS submission. Wall time ≈ 4 h at 60 concurrent tasks.
**Scripts** (all in `Theory_work/Wave3/W3-AUDIT/work/trackC/`; sourced from `DL` where it exists, no change to `DL`):
- `c_proxies.R` — P1–P7 functions plus a brute-force test on p ≤ 30 (exact enumeration vs the greedy); **Opus helper** (subtle logic: anchored chains, rank-one visibility updates, lattice sampling).
- `c_designs.R` — `design_sigma(id, p)` and `draw_X(id, n, p, rep)` (D01–D19, `gen_dev_data.R:18` and `riboflavin_L.csv` reused), **Sonnet helper**.
- `c_run_cell.R` (args: design n p reps; writes `out/<id>_<n>_<p>.csv`), `c_make_tasks.R` (task table with the time limits above), `c_collect.R` (builds the output table below), **Sonnet helper**.
- `c_submit.sh` — Slurm array, copy of the P6 pattern (`W3-P6/nots/submit_table.sh:23`; account commons, 1 CPU); **Engineering schedules it; they write no analysis code**.
No Fable time; reviewer = the Opus helper's brute-force test passing, then the manager reads the table.

## 5. Output
`work/C_RESULT.md` plus `work/C_summary.csv`: ONE table, rows = 19 designs, columns = P1 … P7. Each cell: verdict (inside / outside / unclear / not refuted) at (n = 1600, p = 10n), the key number, and the trend over n = 200 → 1600 (↑, →, ↓ with the log-log slope). Footers: the three pre-announced items of §2 (confirmed or not), and the n* values for P7. Internal only: the advisor report does not cite it, and a "designs outside" result goes to the correctness route (SUSPECT/NARROW) only through Fable's track B reading.
