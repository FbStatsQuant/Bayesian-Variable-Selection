# W2-SIM / LOC — experimental design (v2, after design review R01; for re-review R02)

Family LOC (lead: Claude Opus 5.5). Informs a possible follow-up to W2-LOC2. W2-LOC2 statuses (verbatim, `W2-LOC2/REPORT.md`):
RESULT **PROVED-CHECKED**; (D3) polynomial decay "covered for α > 17/2"; **Open:** "1 < α ≤ 17/2 and long memory (α ≤ 1)";
(D2) LOC-BF: one-factor groups of size ≤ g_n ≤ (log n)^κ, at most one truth per group; "groups containing ≥ 2 truths" and
"one-factor groups of size > (log n)^κ (e.g. polynomial)" are in "Not claimed". Everything here is observation at finite n
(component port + production fits), never a proof or a limit statement. v1 → v2 changes: reviews/LOC_R01_disposition.md.

## 0. Method objects, code provenance, validation
* Scorer and method objects: `Theory_work/Wave2/W2-FAC-B/numerics/bvs_core.py` imported **unchanged** from the deployed
  main archive (`$CODE` = git archive of main @ 11dc9b7; deployed file has CRLF line endings, sha256 7e4d67ba…; its LF
  content = `git show 11dc9b7:…`, sha256 e8283f56…). Used: `Problem` (F(S) = log w(|S|) + log m(S), K = min(p, ⌊n/2⌋)),
  `block_size` (B = min(⌊√n⌋, ⌊√p⌋, 16)), `block_tables`, `start_mode` (block DP, size-then-lex tie rule), `ell_cap`
  (ℓ_n = ⌈log₂(n + p + 1)⌉), `standardize_X`, `make_y_std`; `partition` (fallback and validation), `local_search`,
  `neighbours` (validation).
* Fast re-implementations (`scripts/loc_core.py`):
  - `fast_partition`: scipy complete linkage + per-merge certificate against bvs_core's 1e-10 tie rule; uncertified ⇒
    `bc.partition` is used (exact reference). Flags per run.
  - `ls_loc`: the `bc.local_search` rule with rank-one-update screening and exact bvs_core re-scoring of every neighbour
    within the window (10⁻³, adaptive ×100) of the fast maximum, of every non-finite fast score, and of the add set within
    the window of the fast add maximum; decisions on exact scores; per-step spot check of 64 excluded neighbours.
    Certificate = **screened** (`ls_certified_screened`). At the move cap, `returned_prod` = best improving neighbour of
    the last centre (production semantics, cpp/v3_engine.h) besides the last centre `final`.
  - Validation `scripts/loc_validate.py` v2 (exit 1 on failure): partition (10 designs × 2 seeds + near-tie
    counterexample + duplicate column); LS paths vs `bc.local_search` from start mode / empty / start − truth /
    start + 3 nulls / cap 0 / cap 2 (+ `returned_prod` vs exhaustive best neighbour) / K = |centre| / exact ties /
    large start mode; all-neighbour fast-vs-exact score check. Outputs `results/LOC/validation_local_v2.txt` and the NOTS
    copy `results/LOC/validation_nots_v2.txt`.
* LS0 = `ls_loc` from the start mode S̃₀ with the shipped MR1 cap ℓ_n + |S̃₀| (main 4676af6 / 11dc9b7).
* Production (Q3): `scripts/loc_prod_fit.R` = copy of `W2-SIM/scripts/prod_fit.R` (working-copy sha256 a32a764d…) + design
  `file` (reads the X, y, S₀, β written by `loc_run.py` with `LOC_EXPORT`, the very same bytes as the port run in the same
  task; R read-back checked bit-identical) and integer `seedoff` (distinct method seeds across cells). The
  `v3_fit(X, y, seed = method_seed, allocation = list(mem_gb, hours))` call and recorded fields are unchanged.
  `hours = 1e7` (v3.1 preflight charges LS0's worst case: 1.45·10⁶ s at n = 2000, p = 500 — the Slurm wall time is the real
  limit), `mem_gb` 12 (n ≤ 2000) / 24 (n = 8000). `loc_prod_extract.R`: start mode, LS0 centre, full path (centre
  prepended), types, returned, HPM. The task exits non-zero if the fit or the extraction fails.
* Environment: NOTS `sim/env_sim.sh` (GCC 14.3.0, R 4.5.2, SciPy-bundle 2025.07: Python 3.13.5, numpy 2.3.2, scipy 1.16.1, one
  thread); runner `sim/submit_table.sh` (frozen scripts + manifest with sha256 of every frozen file).

## 1. Data-generating designs
Raw rows iid N(0, Σ) (unit diagonal); X = `standardize_X`; y = `make_y_std(X, θ, σ = 1)`. Seeds:
`SeedSequence([20261109, famcode, round(1000·par…), placecode, n, p, seed])`; uniqueness over all scheduled runs is
asserted by `make_tasks.py`; recorded per run as `seed_key`. Main seeds 1–10; production seeds 101–110.
* **PT(α)**: Σ_jk = (1 + |j − k|)^{−α}; α ∈ {1.5, 2.5, 4, 6} (open range 1 < α < 17/2), **8.5 (= 17/2, the open boundary —
  NOT in the proved range α > 17/2)**, **10 (positive control inside (D3))**, and α ∈ {0.5, 0.8} (long memory). PD:
  (1 + h)^{−α} is convex, decreasing to 0 ⇒ a valid autocorrelation (Pólya-type criterion); numerical check
  `loc_eigcheck.py` (λ_min, λ_max, Cholesky, truncated f(π)) for p ∈ {115, …, 8000}: `results/LOC/eigcheck.jsonl`. No PD
  variant needed.
* **AF(d)**: ARFIMA(0, d, 0) autocorrelation ρ(h) = Π_{i=1}^{h}(i − 1 + d)/(i − d) ~ C h^{2d−1}; d ∈ {0.1, 0.25, 0.4}
  (α = 1 − 2d = 0.8, 0.5, 0.2); λ_max(Σ_p) → ∞, λ_min bounded below. fGn not run separately (same decay class).
* Truths (PT/AF): `spread` S₀ = round(p·{.15, .5, .85}); `adj` S₀ = p//2 + {−1, 0, 1}; θ = (1, −0.8, 1.2).
* **CSG(b, ρ)**: block-diagonal compound symmetry, all groups of size g = ⌈n^b⌉, b ∈ {0.2, 0.35, 0.5}, ρ ∈ {0.5, 0.8},
  G = ⌊(n/4)/g⌋, p = gG. Arms: `one` 3 truths in 3 groups (θ 1, −.8, 1.2); `one4` (matched control) 4 truths in 4
  groups, θ (1, .8, 1.2, 1); `two` 4 truths, two per group in 2 groups, θ (1, .8 | 1.2, 1) — PTV(∅) holds (truth population
  marginals recorded); `twoM` **masking stress arm** θ (1, −.8 | 1.2, 1) (ρ = .8: second truth has zero marginal).
  `two` vs `one4` isolates "two truths share a group" (same |S₀| and coefficients).
* p rules (PT/AF): `q` p = n/4; `s` p = round(n^{0.6}). CSG: p ≈ n/4.

## 2. Experiments, statistics, analysis plan, outcomes that would change the theory
**Grid (main):** PT/AF 11 families × {spread, adj} × [q: n ∈ {500, 1000, 2000, 4000, 8000, 16000}; s: n ∈ {500, …, 64000}
doubling] × 10 seeds; CSG 3 b × 2 ρ × 4 arms × n ∈ {500, …, 32000} × 10 seeds. 4760 scheduled runs
(`configs/main_scheduled.txt`).
**Per run (loc_run.py):** |S̃₀|, missing truths, |S̃₀ ∖ S₀|, extras (full list), index distances (PT/AF) or truth-group
membership and per-truth-group block diagnostics (CSG); population visibility counts #{l ∉ S₀ : n ψ_l² ≥ 2 log p} and
≥ log n (ψ_l = corr_pop(x_l, y)) and radius; truth population marginals; LS0 moves vs cap; move types; `deletions_only`;
`pure_deletion_to_S0`; `truths_deleted`; `added`; final == S₀; `returned_prod` == S₀; screened certificate; local limit;
timeout; F(final) − F(S₀); NA diagnostics (`na_margin` per centre = F(T) − max_l F(T ∪ {l}); min over centres ⊇ S₀ and number
of centres ⊇ S₀ with an improving addition; exhaustive `na_at_S0_exhaustive` = F(S₀) − max over all p − s₀ additions);
OLS add statistic h at S₀ and on path centres ⊇ S₀ vs 2 log p and c_n′ = log(n+1) + 2 log p − 2 log(|S̃₀|+1) (proxy only);
screening diagnostics; timings; partition certificate.
**Analysis (prespecified):**
* Rates per cell (fam, par, place, prule, n): final == S₀, `returned_prod` == S₀, S₀ ⊆ S̃₀, pure deletion to S₀, any NA
  violation on centres ⊇ S₀, na_at_S0_exhaustive < 0 (S₀ not add-stable), local limit; denominators = scheduled runs;
  completed / timed-out / error / missing reported separately; Clopper–Pearson 95% intervals; failures are classified
  as (a) target failure: F(final) ≥ F(S₀) with final ≠ S₀ (S₀ not the local optimum reached — e.g. an addition beats S₀),
  (b) search failure: final ≠ S₀ with F(final) < F(S₀) or local limit, (c) start-mode failure: a truth missing from S̃₀.
* Growth of mean |S̃₀ ∖ S₀| in n, separately per p rule: log-log OLS slope on n ≥ 2000 (q; B = 16 for n ≥ 1024) or
  n ≥ 16000 (s; B = 16 iff p ≥ 256); means include zeros; a cell with a zero mean in its fit range is reported "bounded",
  not fitted; points flagged saturated (mean extras ≥ p/4 or population visible count ≥ (p − s₀)/2) are excluded from
  exponent fits and reported; slope compared with 1/(2α) (the L6 radius exponent) and with the slope of the population
  visible count on the same points; polylog alternatives a(log n)^j, j = 1, 2, 3, fitted on the same points (residual SS
  reported). With ≤ 4 fit points these are descriptive only.
* CSG: the same plus extras inside vs outside truth groups and blocks per truth group; `two` vs `one4` and `twoM` vs `two`.
**Outcomes that would change the theory** (Q1: (D3) below 17/2 / long memory; Q2: LOC-BF beyond (log n)^κ / two truths per
group): (i) final == S₀ by pure deletion in essentially all runs for 1 < α < 17/2 (and/or CSG with g = n^b, `two`) ⇒
supports a conjecture that the corresponding extension holds and that the binding step is the proof's counting, not the
method; (ii) start-mode failures, search failures (incl. local-limit) or NA violations whose frequency increases with n
in some cell ⇒ evidence of a genuine obstruction (sandwich S₀ ⊆ S̃₀ ⊆ Q, or NA) for the route or the method at that
parameter; target failures (S₀ not add-stable) increasing with n ⇒ the posterior target itself moves away from S₀, an
obstruction for any route; (iii) |S̃₀ ∖ S₀| growing polynomially (slope ≈ 1/(2α) or the visible-count slope) rather than
polylog ⇒ any proof below 17/2 must handle polynomial relevance sets (as L6 does); saturation (|S̃₀ ∖ S₀| ∝ p) for α ≤ 1 ⇒
long memory needs relevance sets of order p, where the shipped cap ℓ_n + |S̃₀| is what keeps the deletion path feasible;
(iv) `twoM` failures with `two` successes ⇒ the obstruction is PTV/masking, not multiplicity.

**Q3 (production, same data):** cells C1 PT(1.5) spread, C2 AF(0.25) spread, C3 CSG(.5, .8) one, C4 CSG(.5, .8) two,
C5 PT(0.5) adj, C6 CSG(.5, .8) twoM; p = n/4; n ∈ {500, 2000, 8000}; seeds 101–110 (180 fits; `configs/prod_tasks.tsv`).
Per fit: status, HPM == S₀, HPM before LS0 == S₀, start mode == port start mode, LS0 path == port path (exact models),
LS0 returned vs port `returned_prod`, local limit, timings, preflight estimates. Outcomes: production == port ⇒ the port
observations transfer to the method; a production failure where the port recovers S₀ (or vice versa) ⇒ inspect
(start-mode / partition / LS0 differences before invoking other phases), flag to HQ. Cells not finishing in 24 h are
reported with their denominators (no silent drop).

## 3. Pilot (v1 code): loc_pilot01 (job 2633109), loc_pilot02 (job 2633286); results/LOC/pilot_summary.md. Kept seed:
CSG(.5, .8) `one` n = 8000 seed 1: LS0 final = S₀ ∪ {1478} with F(final) − F(S₀) = 0.94 (target failure; h_S₀ = 24.6 vs
2 log p = 15.2; for that X a fresh-noise simulation gives P(max h > 22.8) ≈ 2.5·10⁻⁴; seeds 2–8 recover S₀).

## 4. Exclusions
fGn (ARFIMA covers the decay classes); polynomial decay in d ≥ 2 (not asked); p = n^{0.6} for CSG (too few groups at
b = .5); PT/AF with p = n/4 beyond n = 16000 (cost: |S̃₀| ~ 10³ for long memory; p = n^{0.6} reaches n = 64000 instead).
