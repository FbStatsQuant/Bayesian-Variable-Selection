# RUN_DESIGN: Regime L production runs (proposal for HQ, gate G2)

Owner: LOWP thread, 2026-10-29. Design per `CHARTER.md` §1–§3, `DECISIONS.md` D1–D5, `LOWP_SPEC.md`. Costs marked **local** were measured on the laptop (shared, noisy, up to ~2× spread); **EST** are extrapolations; all are replaced by the NOTS pilot (`pilot/JOB.md`) before production is sized.

## 1. What runs

| Arm | Unit | Count | Notes |
|---|---|---|---|
| Exact enumeration | dataset (both scales in one pass) | 1,200 (600 at p = 20, 600 at p = 30) | `lowp/enum/run_enum_dataset.R`; reads `inputs/` only |
| SMC-BVS v2.2, primary seed | case | 2,400 (2 p × 6 S × 100 r × 2 c) | `core/v2_2_1/study/run_case.R` (v2.2.1; fork `lowp/smc/` retired); seed = data + 4,000,000 |
| SMC-BVS, repeat seeds | case × repeat | 2,400 (r = 1..20 × 5 repeats × 24 cells) | `--repeat m`, seed = data + 4,000,000 + 1,000·m |
| Benchmarks F1–F5, A1–A3 | case × method | 19,200 (2,400 × 8) | `bench_lowp/run_bench_case.R`, primary fits only |
| Scoring + theory measures | all | 1 pass | `scoring/run_scoring.R`, after downloads; truth opened only here |

**Repeat-seed subset (proposal: 20 replicates × 5 extra seeds per (p, scenario, c)).** Reason: the headline errors mix two sources, the dataset (which posterior is hard) and the SMC randomness (Monte Carlo error). Six seeds on each of 20 datasets give, per cell, 100 within-dataset degrees of freedom for the Monte Carlo variance of log Ẑ and of each PIP, and HPM agreement across seeds with standard error ≤ 0.05; with 24 cells this is enough to state whether misses are seed-stable (posterior hard) or seed-specific (sampler variance). Replicates 1..20 are the first 20 of the 100, so no selection on outcomes. Cost is the same as the primary SMC arm (~10–20 core-hours, §2), so HQ may extend to all 100 replicates (12,000 extra fits, ~50–100 core-hours) if it wants per-dataset Monte Carlo error everywhere.

## 2. Per-unit cost (local measurements)

| Arm | p = 20 | p = 30 | Memory (peak working set) | Source |
|---|---|---|---|---|
| Enumeration, both scales | ~1.3 s at 1 thread (0.45 s at 8) | **~890–1,090 core-s** (two full 14-thread runs: 222 s wall / 1,084 CPU-s and 140 s wall / 886 CPU-s; machine shared) | 82–95 MB | `enum/VALIDATION.md` |
| SMC-BVS one fit (no escalation seen) | 4.7–6.9 s | 18–24 s | 107 MB (p20), 187 MB (p30) | `tests/SMC_SMOKE.md` |
| Benchmarks, one case, median / max s (p = 20 and 30 pooled, 6 smoke cases) | F1 2.8 / 7.3; F2 5.5 / 11.3; F3 0.9 / 1.6; F4 0.4 / 1.3; F5 0.3 / 1.5; A1 3.0 / 22.8; A2 0.07 / 0.3; **A3 43.4 / 68.0**; all 8 ≈ 56 s median | | 77–273 MiB per method | `bench_lowp/smoke/SMOKE_REPORT.md` |
| Scoring + theory (TD d ≤ 2, π₀ DP) one case | < 1 s | < 1 s | < 300 MB | `scoring/tests/INTEGRATION_REPORT.md`, `enum/VALIDATION.md` |

**Totals (EST, with a ×2 margin for escalation and NOTS speed):** enumeration ≈ 175 core-h (p = 30) + 0.3 core-h (p = 20); SMC primary ≈ 10 core-h (×2 → 20); SMC repeats ≈ 10–20 core-h; benchmarks ≈ 2,400 × ~56 s ≈ 37 core-h (×2 → 75; A3 is 78 % of it); scoring ≈ 1 core-h. **Total ≈ 300 core-hours**, i.e. about 1.6 Sapphire Rapids node-hours (192 cores).

**p ≫ n theory measures (after the fact on the H outputs, separate later bundle):** TD(0, 0) at p = 1000, s₀ = 14 takes 1.3·10⁸ scores, 42.7 s on 14 threads locally (~600 core-s); over the 2,400 H fits ≈ 300 core-h (p = 500 cheaper). TD(1, 0) is 1.4·10¹¹ scores per fit (~13 h on 14 threads) and is not proposed at p ≫ n (decision for HQ).

## 3. Job layout on NOTS (all `--constraint=sapphirerapids`, account commons)

Run ids `<YYYYMMDDTHHMMZ>_lowp_<piece>`; pieces `enum20`, `enum30`, `smc`, `smcrep`, `bench`. Every output goes to `/scratch/fb31/New_Campaign/results/<run_id>/p{pppp}/<unit>/`; logs to `/scratch/fb31/New_Campaign/logs/<run_id>/` (charter §2.2 / D7: no logs in home); home holds only code, manifests and the small inputs. Each run folder is downloaded with `ops/transfer`, sha256-verified, then deleted from scratch (charter §2.3).

| Piece | Array | Per task | Request per task | Expected wall (EST) |
|---|---|---|---|---|
| enum30 | 24 tasks = 6 scenarios × 4 blocks of 25 replicates | 25 datasets sequentially, `--threads 16` | 16 CPU, 4 GB, 2 h | ~35 min |
| enum20 | 1 task | 600 datasets, `--threads 4` | 4 CPU, 4 GB, 1 h | ~5 min |
| smc | 96 tasks = 2 p × 6 S × 2 c × 4 blocks of 25 | 25 fits sequentially (1 CPU each, timing-clean) | 1 CPU, 2 GB, 4 h (`--mem-gb 2 --hours 4` passed to the core guard) | p30 ~10 min, p20 ~3 min; escalations longer |
| smcrep | 120 tasks = 24 cells × 5 repeats | 20 fits | 1 CPU, 2 GB, 4 h | ~8 min |
| bench | 96 tasks = 2 p × 6 S × 2 c × 4 blocks | 25 cases × 8 methods | 1 CPU, 4 GB, 4 h | ~25 min |

- Single-threaded BLAS in every task (`OMP/OPENBLAS/MKL_NUM_THREADS=1`) except the enumerator's own OpenMP threads.
- **Software.** The enumerator must be built with the same toolchain and flags as the v2.2 core (CONF's NOTS build; core `Makevars.v3` flags), so its scores stay bit-identical to the SMC scorer; the pilot re-checks this on NOTS. Benchmarks use the sealed bench20261019 R 4.5.2 study library read-only (pinned versions, §III.3.0); reading it is allowed under the benchmark freeze.
- **Disk.** Home: code (~5 MB plus compile caches), inputs + truth + manifests 72 MB, dev 3.4 MB: **≈ 0.1 GiB of the 0.5 GiB campaign ceiling** (D7; total home must stay < 9.6 GiB). Scratch (transient): EXACT ≈ 0.1 MB × 1,200 = 0.12 GB; SMC records 0.06–1 MB × 4,800 ≈ 2–3 GB (more if v2.2's instrumentation stores the full scored set — the pilot measures it); benchmark records ≈ 19,200 × ~0.05 MB ≈ 1 GB. Each piece is downloaded per run folder (`C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign\results\<run_id>\`).
- `guard.sh <planned MB>` before every submission; `truth/` is mode 000 during every fitting wave and restored only for scoring (which runs locally after download).
- Order: pilot → (HQ sizes) → enum30 ∥ smc ∥ bench (independent) → smcrep → download/verify/delete each → local scoring.

## 4. Pilot

`pilot/JOB.md` (charter §6 format) measures on NOTS: generator bit-identity (L.6 check 4(b)), enumerator thread scaling and per-dataset time at p = 30, enumerator-vs-SMC-scorer bit identity on NOTS, SMC per-fit time and memory and record size, benchmark per-method time and memory, on per-arm subsets of the dev datasets (excluded from counts): enumeration on all 30 p = 20 and 6 p = 30 dev datasets plus a 3-run thread-scaling series, SMC on 24 dev cases plus 4 repeat-seed fits, benchmarks on the same 24 cases × 8 methods; the generator check 4(b) covers all 1,200 + 60 datasets but is not a timing measurement. Truth is locked (mode 000) for the whole fitting wave and restored by a finalizer. The disk footprint per unit is recorded. Escalation tails are under-sampled at this size, so production requests keep a margin. Its acceptance check is a single summary table that replaces §2.

## 5. Decisions for HQ

1. Repeat seeds: 20 × 5 per cell (proposed) or all 100 replicates.
2. Home budget (D7): the low-p study needs ≈ 0.1 GiB of the 0.5 GiB campaign home cap; `guard.sh` must be updated to the D7 limits before the pilot (OPS; the pilot bundle refuses otherwise).
3. p ≫ n TD audit limited to d = 0 (≈ 300 core-h over 2,400 fits); d = 1 is infeasible there.
4. T37's literal TD clause is generically violated whenever a truth-in swap is available (see `scoring/THEORY_MEASURES.md`); the audit reports the literal wording and a "toward S₀" variant. The theory side should decide which one T37 means.
