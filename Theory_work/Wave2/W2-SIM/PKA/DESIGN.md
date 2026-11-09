# W2-SIM family PKA — experimental design (v1, 2026-11-09)

Informs **W2-FAC-PKA** (compound symmetry with p > K). Governs: `W2-FAC-PKA/numerics/SIM_REQUEST.md` Priorities 1 and 2
(Priority 3, production core on population CS, is run by the W2-SIM lead, not here). Independence: nothing from
W2-FAC-PK, W2-SIM/PK or results/FAC-PK is read or used. Theory statuses quoted below are copied verbatim from the
ticket files (STATEMENT.md v2 LOCKED, SINGLETON_TARGET v2 LOCKED, lemmas/L2 "PROVED (by this seat, unchecked)").

## Code and provenance
* Scorers (read-only): `W2-FAC-B/numerics/cs_core.py` (closed-form exact-CS score `CS.F_stats`, O(p) scan path
  `ls0_path_cs`), `bvs_core.py` (partition, start DP `start_mode`, `ell_cap`, `block_size`), `fac_core.py` (dense
  reference path, validation only) — from the NOTS archive of main @ 11dc9b7 (`code/main_11dc9b7`).
* Ticket numerics (read-only): `W2-FAC-PKA/numerics/n1_exact_grid.py` (`TableAdapter`, `run_path` = `ls0_path_cs`
  patched by asserted single replacements to start from a given set; post-R02 version with the `dtype=bool` empty-model
  fix) and `n3_singletons.py` (`singleton_start`). A new NOTS snapshot `code/tickets_<ts>_pka/` with its own SHA256SUMS
  is uploaded because n1 changed after the 09:43 snapshot (old sha 7512ea90…, new 13983c75…).
* Family code: `PKA/scripts/` — `pka_lib.py` (imports, replacements, path analysis), `p1_run.py`, `p2_run.py`,
  `validate.py`, `make_tasks.py`, `summarise.py`. Every run is frozen by `submit_table.sh` (manifest with sha256).
* Environment: NOTS `sim/env_sim.sh` (GCC 14.3.0, Python 3.13.5, numpy 2.3.2, scipy 1.16.1, one thread,
  PYTHONDONTWRITEBYTECODE=1; scripts also run with `python3 -B`).

## Replacements (rule 3) and their validation (`validate.py`, output saved in results/FAC-PKA/validation/)
* **Partition.** `bc.partition_from_corr(Sigma_CS, B)` is O(p^3). Under exact CS every linkage distance equals 1−ρ;
  the source tie rule (tolerance 1e-10, pair with smallest minimum index, lexicographic union) builds a caterpillar,
  and the top-down cut + next-fit packing returns consecutive index blocks of size B = `block_size(n,p)` (= 16 for all
  P1 cells). `fast_partition_cs(p,B)` returns these blocks. V1: exact equality of block lists for n ∈ {100,…,1600},
  c ∈ {.6,.85,.98}, ρ ∈ {.2,.5,.8} (ρ = .5 only when p > 700). **Label:** this is the FAC-B *baseline source
  partition* (population Σ, tie tolerance 1e-10). Production computes linkage on a floating-point sample Gram, where
  the exact ties are broken by round-off; the production partition on exact CS is therefore NOT this one. P1 results
  are about this partition only.
* **Start DP.** `fast_start_mode` repeats the arithmetic of `bc.start_mode(TableAdapter(P), blocks, tie_tol=0)`
  (same `itertools.combinations` index arrays, same `F_stats` call, same max-plus loop), with combinations cached and
  the tie enumeration done by an iterative backtrack (the source recursion has depth = #blocks, > 1000 for n ≥ 25600).
  Any exact float tie in the backtrack → fall back to the source enumeration (flag `start_fallback`). V2: exact
  equality (==) of mode, size, log γ0(mode) and per-block per-size maxima against the source on 79 cases
  (n ≤ 1600 all c, ρ; n = 3200, c ∈ {.6,.98}; n = 6400, c = .98).
* **Path:** none replaced — the reference `run_path` is used. V3 re-checks it against the dense `fac_core.ls0_path`
  (explicit Gram, `bvs_core.Problem` scorer) from DP, size-K and size-(K−1) starts: final set, move count and F after
  every move (< 1e-7). V4: `n3.singleton_start` == `bc.start_mode` on singleton blocks.

## Analysis definitions (pka_lib.analyse_path), common to P1 and P2
Path = uncapped reference path computed once; C_t = centre after t moves (C_0 = start), m* = number of moves to the
certified mode. Scan t scores C_t and its full feasible flip/swap neighbourhood (additions only if |C_t| < K).
* first_scoring_scan = min t with S0 ∈ {C_t} ∪ N(C_t) (exact set test). first_arrival = min t with C_t = S0.
* Cap a: scans t = 0..min(a, m*). **scored(a)** ⇔ first_scoring_scan ≤ a; arrived(a) ⇔ first_arrival ≤ a;
  local_limit(a) ⇔ m* > a; terminal centre C_min(a,m*) (is it S0, its size, missing truths). Caps
  a = ℓ+|start|, a2 = ℓ+2|start|, ℓ = ⌈log2(n+p+1)⌉. Valid because LS0 under any cap is a prefix of the uncapped
  path (deterministic best strict improvement, same tie rule).
* Move tags (truth-in/out split, R02 F5): sNN null↔null swap, sTi null out/truth in, sTo truth out/null in, sTT,
  −N, −T, +N, +T. initial_swaps = number of moves before the first non-swap; initial_null_swaps = leading sNN run;
  first_deletion_index; end_of_swap_index (= index of last swap); swaps_after_first_deletion (swap reappearance);
  reentries (a variable re-entering after leaving), in_then_out (entered, later left); additions.
* Centre (xi units): x_T = (γ_k B_T − b)/d with B_T = Σ_T z_j, γ_k = β/(α+kβ), null z_j = b + d ξ_j,
  b = [(n−1)ρθ̄ + √((n−1)ρ) η]/s, d = √((n−1)(1−ρ))/s. Recorded: x_0, max |x_T| over the path (and where),
  max |x_T − x_0| over the initial-swap phase (early centre drift). Residual Q_T and multiplier
  M_T = ν n d²/(α(0.02+Q_T)) at the start and their minimum over the initial-swap phase.
* Start: |start| vs K, truths missing from start, retained-null ξ mean and quantiles, block occupancy profile
  (P1), size margin of the DP.
* slack = ℓ + s0 + 1 (STATEMENT T2: if the path starts containing truth and uses only deletions and swaps up to
  first arrival, d = |start| − s0 + swaps, so swaps ≤ ℓ+s0+1 is *sufficient* for arrival within a+1 moves). Used
  only as a reference line; scoring/misses are decided by the exact scan test above.

## E1 — Priority 1 main (ρ = .5)
Informs **T2** (key path target: LS0(a) scores S0 → 1 vs liminf P(miss) > 0), the cap remedy candidate **T4**
(a2 = ℓ+2|start|), and descriptively **T1a/T1b** (saturation, truth inclusion, retained-null allocation) — all OPEN
or "PROVED (by this seat, unchecked)" in the ticket; nothing here proves a limit.
Design: exact-Gram CS (cs_core.CS), p = ⌊cn⌋ ≤ n−1, c ∈ {.6,.85,.98}, truths (2,26,53,75), θ = .5·(1.4,1,1.8,1.2),
σ = 1; start = actual capped block DP on the baseline partition (blocks of 16; the four truths in four distinct
blocks 0,1,3,4). n ∈ {800,1600,3200,6400,12800,25600} with 100 seeds; n = 51200 with 20 seeds (n-growth prioritised).
**Theory-changing outcomes (from the request):** initial/total null swaps growing beyond ℓ+s0+1 together with misses
under a whose frequency does not shrink with n → motivates an asymptotic LS0-route counterexample on this partition;
bounded swaps or a miss frequency shrinking with n → redirects toward original-cap consistency. Additions, repeated
exchanges, or misses under a2 → invalidate a simple two-phase / one-swap-per-null remedy. Arrival after a alone is not
a miss (the scan test decides).
Statistics per cell: miss rate under a and a2 with exact Clopper–Pearson 95% CIs; quantiles of initial swaps, total
swaps, swaps/(ℓ+s0+1), first_scoring_scan − a; counts of additions, truth-out moves, reentries, swap reappearance,
truth missing from start, non-saturated starts, ties, DP fallbacks. Descriptive n-trend: OLS slope of
log(median initial swaps) on log n across n (and of initial swaps / log n) with a seed-bootstrap CI — evidence only.

## E2 — Priority 1 sensitivity (ρ = .2, .8)
Same as E1, 20 seeds, n ≤ 25600. Informs whether E1's pattern depends on ρ.

## E3/E4 — Priority 2: singleton partition (EXPLICITLY NONPRODUCTION)
Informs SINGLETON_TARGET v2 S1/S2 and L2 (status "PROVED (by this seat, unchecked)"): S1 — start has size K, contains
truth, nulls = top K−s0 ξ, retained-null mean → μ = φ(t)/q, q = 1/(2c); S2 — the first ⌈C log n⌉ moves are null swaps
for every C (so initial swaps / log n diverges), early centre drift o(1), M_T ≥ .5 − o(1); consequence: merged-cap LS0
miss once initial swaps ≥ ℓ+s0+2 (deterministic size argument, recorded as merged_miss_by_size). For s0 = 1 the full
method scores S0 through table ingestion (ticket's statement) — P2 says nothing about D_n.
E3 (v1): s0 = 1, θ0 = 1, ρ = .5, c ∈ {.6,.85,.98}, 20 seeds; full uncapped path for n ∈ {1000, 3162, 10000, 31623,
100000}; early phase only (path until the first non-swap move) for n ∈ {316228, 10^6}.
E4 (v2): s0 = 2, θ = (1, −.1), same grid: weak-truth exclusion from start, index of the truth-in swap, then swaps.
**Theory-changing outcomes:** initial swaps / log n not increasing in n (or initial swaps < ℓ+s0+2 at large n), drift
not small, or truth-out/deletion moves inside the first O(log n) moves would contradict L2's S2 as stated (proof
error to locate); start not equal to top-ξ selection would contradict S1. Agreement is evidence, not a proof.
P2 outcomes are never pooled with P1.

## Seeds
seed = SeedSequence([20261109, 7, prio, n, round(100c), round(10ρ) or variant, rep]).generate_state → 63-bit int;
distinct across cells, recorded per row; validation uses prio key 99. cs_core.CS draws ξ (p), η, χ² in that order.

## Batches (NOTS, ≤ 25 concurrent 1-CPU tasks; RUN_ID prefix pka_)
val (4 tasks) → pilot (P1 ρ=.5 20 seeds n ≤ 6400, 5 seeds at 12800/25600; P2 n ∈ {1000,10000} full 20 seeds,
n = 1e5 early 2 seeds) → **Codex design review** → main_a (P1 ρ=.5 to 100 seeds, n ≤ 25600) → p2main → sens →
main_b (n = 51200). Local pilot timing (Windows, 1 thread): P1 c=.98 n=800/1600/3200 = 4/5/10 s per seed;
P2 full n=1e4 ≈ 30 s; P2 early n=1e5 ≈ 200 s.

## Outputs
results/FAC-PKA/{validation,P1,P2}/: per-seed summary JSONL (all scalars above, per-cap outcomes), compact move
records (null deletions run-length coded; every other move with index, tag, out, in, F), cell summaries (CSV/MD),
NOTS RUN_IDs, job ids and manifests. Full move lists stay in /scratch/fb31/theory_w2/<RUN_ID>/raw/.
