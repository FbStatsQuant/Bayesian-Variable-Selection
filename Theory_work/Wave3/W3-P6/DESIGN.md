# W3-P6 — experiment DESIGN (v2, 2026-11-09; v1 + fixes of review R01 (NO-GO), reviews/R01_disposition.md)

Decides PROGRAM.md decision D1: on strong-factor designs with p > K = ⌊n/2⌋ and p ≫ n, does the **full method as coded**
(main 2252d57: calibration SMC islands → final SMC islands → final local search from the global best (cap ℓ_n) → LS0
from the start mode (merged cap ℓ_n + |S̃₀|), calibration grid fallback) report HPM = S₀ with probability → 1 as n grows;
and does the cap ℓ_n + 2|S̃₀| (W2-FAC-PK Theorem PATH) change the outcome? Theory status (copied): Theorem NEG (LS0 alone
fails for K < p ≤ n − 1, exact-Gram CS) PROVED-CHECKED; the full method (STATEMENT (P6)) open.

## 1. Objects
* **Code:** `git archive` of main 2252d5730c43b1d641d0b3b2afddeb79045bb4a5, path Scripts/SMC_BVS/core (sha256-identical to the
  W2-SIM deploy of 11dc9b7), at NOTS `theory_w3/code/main_2252d57/repo`. No source modified. Env = production env.sh
  (GCC 14.3.0, R 4.5.2, one thread). Driver `scripts/p6_fit.R` (frozen per run with sha256 in the run manifest).
* **Designs (iid Gaussian rows, unit variances; the method standardises):**
  `cs(ρ)` x = √ρ f + √(1−ρ) e, ρ ∈ {0.3, 0.5, 0.7}; `fac2` x_j = √.35 f₁ + √.25 (−1)^j f₂ + √.40 e_j (corr .60 / .10,
  two pervasive factors); `s5` x_j = √.3 f + √.4 g_{group(j)} + √.3 e_j, groups of 5 consecutive columns (corr .7 / .3).
* **Truth:** S₀_k = (k−1)·step + 3 + ((k−1) mod 2), step = ⌊p/s₀⌋ rounded down to even (v2, R01-8; v1 = ⌊p/s₀⌋, same when even), s₀ ∈ {4, 8}; β = (1.4, 1.0, 1.8, 1.2) repeated, aligned signs
  (factor signal bᵀθ ≠ 0, the NEG regime); σ = 1. Truths in distinct s5 groups and alternating fac2 parity.
* **Seeds:** data_seed = (7919 rep + 13n + p + 1000003·dcode + 50021 s₀ + 7·round(1000ρ)) mod (2³¹ − 4·10⁶ − 2), method seed
  = data seed + 4·10⁶. Production reps 1..20; probes used reps 900/901 (never pooled). Uniqueness checked at task generation.
* **Allocation:** `hours` = 22.5 (runtime guard + preflight), mem 8–12 GB; Slurm commons 24 h, 1 CPU. A fit that exceeds 22.5 h
  returns `resource_limit` with the HPM so far (flag hpm_incomplete) — this is the method as coded under that allocation and
  is reported as such (never as a completed fit).

## 2. Cap comparison without doubling the SMC cost
Each fit runs once with arm `wide` (documented testing option `v3.ls0_ell = ℓ_n + K`, cap ℓ_n + K + |S̃₀| ≥ ℓ_n + 2|S̃₀|).
LS0 is deterministic (reads no uniforms), runs last, on the same ledger; with cap a it scans centres C₀..C_min(a,m)
(v3_engine.h:385–415: at a scan with moves = a and an improving neighbour it returns that neighbour without moving). Hence
for a ∈ {MR1 = ℓ_n + |S̃₀|, cap2 = ℓ_n + 2|S̃₀|} (`p6_common.R::p6_derive`): LS0(a) scores S₀ ⇔ first scoring scan ≤ a + 1;
HPM(a) = better of hpm_before_ls0 and path entry a + 1 (or the endpoint). Returned as NA (never guessed) when censored (the
wide run stopped on its own cap before scan a + 1) or when two distinct candidate models tie exactly in F. Equal-F
neighbours not kept in the archive cannot be excluded: generic uniqueness (continuous data) is an assumption, checked by
the **validation pairs**: arm `mr1` fits with the same seeds at (50, 50) and (50, 125), 20 each, compared on exact sorted
HPM identity and F, seeds, start mode, pre-LS0 HPM/F, calibration tier and LS0 first scoring scan (fail closed).
The wide and mr1 runs share everything before LS0: the preflight charges ℓ_n + K + 1 LS0 scans in both (v3_fit.R:44–65 uses
b$ell, not the override). **cap2 is an algorithmic counterfactual** (what LS0 with that cap scores and which HPM results);
the delivery of a cap2 rule (its own preflight charge, METHOD_REQUIREMENTS) is not reproduced.

## 3. Metrics per fit
status; reported HPM = S₀ for MR1 (= the method as coded), cap2 and wide; **outcome class** per cap: S₀ / posterior
(F(HPM) > F(S₀): S₀ would not be reported even if scored) / search (F(S₀) > F(HPM): since the HPM is the best scored model,
S₀ was never scored in that run) / NA; F(S₀) by direct scoring with the core scorer on the method's own preprocessing,
checked against the ledger (|F_direct(HPM) − F_ledger(HPM)| recorded). **Snapshots** "HPM = S₀ after the SMC islands
(before the final local search)" and "before LS0" prove S₀ was scored by then; an unequal snapshot proves nothing unless the
class is "search". The phase/mechanism/φ at which S₀ became the running HPM (ledger provenance). Start-mode size vs K;
LS0 moves, first scoring scan, caps, swap/deletion counts, leading swaps; calibration tier/escalation/fallback/triggers;
timings; preflight LS0 charge; peak memory. All MR1→cap2 HPM changes are counted (not only changes to S₀).

## 4. Feasibility (probe01, job 2647903, one fit per cell, cs ρ = .5, s₀ = 4) — the binding constraint
| n | p | wall (s) | notes |
|---|---|---|---|
| 50 | 50 | 79 | tier 0 |
| 50 | 125 | 1276 | escalated to tier 1 |
| 50 | 250 | 3076 | tier 1 (grid_unconverged) |
| 50 | 500 | 4322 | tier 1 |
| 100 | 100 | 6419 | tier 1 |
| 100 | 250, 500, 1000; 150 ×4; 200 ×4; (50, 2500); (100, 5000); fac2/s5/s₀=8 at (100, 250) | > 3 h, still running at writing | |
Every completed probe escalated to tier 1 (4× particles/stages) once p > n/2 + O(1). Cost grows ~×80 from (50,50) to
(100,100). **A clean n-trend to n = 1600 or p/n = 50 at n ≥ 100 is not reachable with the method as coded** (single fits
would take ≫ 24 h; W2-SIM's own probes at n = 200–1200 have run > 6 h without finishing). The design therefore has:

## 5. Grid (costed manifest, frozen before submission of b2)
Cost per fit from probe01 (one seed; cs ρ = .5): (50,50) 0.02 h, (50,125) 0.35 h, (50,250) 0.85 h, (50,500) 1.2 h,
(100,100) 1.8 h; n = 100 with p ≥ 250 > 3.3 h (still running at freeze); extrapolated below (×20 seeds).
**A — completed-fit grid, arm wide, reps 1..20, allocation 22.5 h:**
* b1 (submitted before R01, early signal): n = 50: cs ρ = .5 s₀ = 4 at p/n ∈ {1, 2.5, 5, 10}; variants cs ρ = .3, cs ρ = .7,
  fac2, s5, cs ρ = .5 s₀ = 8 at p/n ∈ {1, 5}; validation pairs (mr1) at (50,50), (50,125). 320 fits, ≈ 160 core-h.
* b2 main sequence, cs ρ = .5, s₀ = 4: p/n = 1 at n ∈ {75, 100, 150}; p/n = 2.5 at n ∈ {75, 100}; p/n = 10 at n ∈ {75, 100}
  (with b1: three n values per ratio, four for p/n = 1). Est. ≈ 10 + 36 + 160 + 30 + 100 + 100 + 300 ≈ 740 core-h.
* b2 breadth at n = 100, p/n = 2.5 (p = 250): cs ρ = .3, cs ρ = .7, fac2, s5, cs ρ = .5 s₀ = 8 (with b1's n = 50 cells: two n
  values per variant at p/n ≈ 2.5–5). Est. ≈ 500 core-h.
* p/n = 50 (n = 50, p = 2500): 20 seeds only if its probe completes in < 12 h (decided when it ends; recorded in LOG).
**B — fixed 22.5-h allocation at larger n (conditional second wave, ≤ 450 core-h):** cs ρ = .5, s₀ = 4, n = 200,
p/n ∈ {1, 2.5}, 10 seeds — submitted only if the n = 200 probes show that a 22.5-h allocation gets past the calibration pilot
(otherwise the probes themselves are the evidence). Prefix coupling (R01-7): for identical inputs and environment, the
allocation enters only the initial preflight (v3_fit.R:113–117) and the escalation admission (v3_fit.R:144–150,
v3_calib.R:153–158), both of which stop rather than redirect the run, and the runtime guard, which truncates; so a truncated
run's scored set is a prefix of the run under a larger allocation *conditional on that run being admitted at the same
points*. A preflight stop (no HPM) is reported separately from a searched prefix. B is tabulated separately.
**C — LS0 at large n (context only):** W2-SIM PK R3 (results/FAC-PK; Python LS0 path, iid CS ρ = .5, n ≤ 4000, p/n ≤ 10).
**Policy:** every scheduled seed stays in the denominator; no re-seeding or replacement of slow seeds; Slurm failures are
rerun once with the same seeds (new RUN_ID, logged); fits stopped by the guard keep status resource_limit. Concurrency
≤ 150 tasks; long cells are ordered first.

## 6. Analysis and reading rules (fixed before b2 results)
* Estimands (finite n): per cell, reported HPM = S₀ (as coded), with Wilson 95% over evaluable fits and bounds over all
  scheduled seeds; class counts S₀ / posterior / search / NA per cap; snapshots; cap-change counts. No pooling across cells;
  trend read at fixed (design, s₀, p/n) across n.
* Reading: (i) **search failures** (class "search") are the method's failures; posterior failures are failures of the
  reported-HPM target but are not repairable by search (they fall under posterior concentration, PROGRAM item 1).
  (ii) "Evidence for success as coded": zero or vanishing search failures at every feasible n and ratio, with the as-coded
  rate rising with n where posterior failures dominate. (iii) "Evidence against": search failures that persist or grow with
  n at fixed p/n. (iv) "Insufficient evidence": otherwise, in particular when the feasible n range cannot separate the trend
  from posterior failures. No finite-n outcome proves or refutes the limit statement; D1's asymptotic claim stays with theory.
* Cap question: counted on fits where MR1 and cap2 HPMs differ; by construction they can differ only when LS0 with cap2
  scores a model better than everything scored earlier.
* Infeasibility is reported as an operational finding (time per fit vs (n, p), escalation rates, the guard/preflight).
