# CHECKPOINT_1 — W3-SCALE (track 3, scaling), leg A

Lead: Claude Fable 5.2 (effort high, Claude Work). Branch `theory/W3-SCALE` (base main 613f063). Written 2026-11-12
04:15 CT. Everything is committed on the branch; nothing was pushed to main.

## 0. Summary

1. **Profile of v3.1 on NOTS** at p = 1k, 2k (full fits), 20k (one island, N = 2,500): done. **p = 5k: pending** —
   calibration finished after 5.40 h (11 rebuilds, then an escalation), the tier-1 final run was still running at
   8.6 h. **No 10k fit was admitted** (§1.3).
2. **v3.2-dev** (`Scripts/SMC_BVS/core_v32dev/`, code frozen at bbdfea0): Gram, neighbour graph, block tables and the
   LS0 preflight scan bound. Setup at 20k: 85.6 s → 23.1 s, peak 9.24 → 6.26 GiB.
3. **Bit-identity verdict: PASS on everything tested.** v3.1 against v3.2-dev on NOTS (PROD-H node type and
   toolchain): 24 of 24 PROD-H units and 10 of 10 supplementary units identical in every output field except
   wall-clock numbers and the preflight record; header dumps and R exports identical. Two Sol reviews found no
   difference on valid fits; what they did find is fixed (§3.3).
4. **sd(log Ẑ_r):** ≤ 0.09 in the median at N = 2,500 for p ≤ 2k, with a tail to 0.7–1.0; **0.5–2.5 between the
   diagnostic islands of the one 5k calibration** (§4). The old PROD-H records were not reachable; the table is built
   from this leg's own fits.
5. **DESIGN_v1.md** is written (revision 2). Astra judged revision 1 UNSOUND; all 18 findings were applied.
   **Revision 2 has not been re-reviewed.**
6. **NOTS:** 27.8 task-hours used by finished jobs + the 5k job (8.6 h so far, limit 24 h): at most 51.8 of 150.
7. The two reserved questions are framed in DESIGN_v1 §7 and not decided.

## 1. Profile of v3.1 (leg A item 1)

One thread, sapphirerapids (Xeon Platinum 8468), GCC 14.3.0, R 4.5.2, pinned flags; n = 200. Driver
`scripts/profile_fit.R`: the `v3_fit` call sequence on the unmodified core, with only the memory preflight gating the
run. Source tables: `results/profile_v31_{phases,stages,step_cost}.tsv`. Memory is peak resident, GiB.

### 1.1 Time and memory by phase

| | p = 1k | p = 2k | p = 5k | p = 20k, one island |
|---|---|---|---|---|
| data | PROD-H `p1000_S3_r001_c100` | S3-type | S3-type | S3-type |
| particles N | 2,500 | 2,500 | 5,000, then 20,000 (escalated) | 2,500 (by choice; the rule gives 20,000) |
| preprocessing (s) | 0.06 | 0.07 | 0.15 | 0.31 |
| Gram and context (s) | 0.06 | 0.22 | 1.09 | 16.2 |
| setup (s): blocks / tables / start / neighbour graph | 0.18: 0.03 / 0.03 / 0.02 / 0.08 | 0.61: 0.13 / 0.06 / 0.05 / 0.36 | 3.29: 0.90 / 0.12 / 0.10 / 2.15 | 84.9: 25.3 / 0.50 / 0.39 / 58.7 |
| calibration (s) | 520 | 2,049 | 19,444 (tier 0: 13,261; tier 1: 6,181) | pilot island, H = 2,500: 2,184 |
| final run (s) | 500 (4 islands) | 1,235 (4 islands) | **running** | one island: 2,392 |
| final local search / LS0 (s) | 0.02 / 0.11 | 0.04 / 0.16 | pending | 0.40 / 2.06 |
| total (s) | 1,028 | 3,293 | **pending (> 8.6 h)** | 4,707 |
| peak memory, setup | 0.13 | 0.19 | 0.69 | 9.23 |
| peak memory, calibration | 0.23 | 0.39 | 0.99 | 5.40 (pilot island) |
| peak memory, final run | 0.33 | 0.63 | pending | 6.30 |
| v3.1 preflight at 24 h | admits (LS0 charge 2.7 h) | admits (11.2 h) | **refuses** (53–94 h charged) | **refuses** (934–1,372 h; memory model 14.8 GiB against the 8 GiB default) |

### 1.2 Stage counts and step costs (T was UNVERIFIED in v0)

| | 1k | 2k | 5k | 20k island |
|---|---|---|---|---|
| pilot stages | 20 | 28 | 23 (tier 0), 23 (tier 1) | 22 |
| rebuilds I (cap ℓ) | 5 (11) | 8 (12) | 11 (13), then 1 at tier 1 | — |
| stages of the final grid T | 26 | 33 | 33 | 29 |
| escalated | no | no | **yes (E2 at the last tier-0 rebuild)** | — |
| candidate set \|V\| | 40,001 | 80,001 | 200,001 | 800,001 |
| µs per elementary step, bridge | 1.14 | 1.16 | 1.11 (tier-0 diagnostic stages), 1.24 (tier 1) | 0.90 |
| µs per elementary step, φ = 1 | 1.64 | 1.90 | pending | 1.80 |
| one final island (s) | 125 | 308 | pending | 2,383 |
| score-cache hit rate | 0.38 | 0.38 | pending | 0.38 |
| sd(log Ẑ_r), final islands | 0.70 | 0.04 | pending | — |
| HPM = true model | yes | yes | pending | yes |

Over the 24 PROD-H units (`results/leg_a_units_calibration.tsv`): T = 26–40; I = 2–8 (median 4) at p = 500 and 2–10
(median 6) at p = 1000; calibration is 45% (p = 500) and 56% (p = 1000) of calibration + final time in the median.

### 1.3 Readings

- An island costs about N·(p + 16)·(T + 21.6) µs (errors −3%, −11%, +6% on the three measured final islands): 0.41 of
  v0's estimate. A v3.1 fit is about 4.2 + 0.82·I islands in sequence.
- **Calibration, not the final run, is the first wall.** It is half of a fit or more, sequential, and at 5k it took
  5.4 h and ended in an escalation.
- **10k full fit: not admitted.** By the formula it needs 17–23 h without an escalation (commons limit 24 h), and the
  5k fit escalated. Leg A's changes do not speed up islands.
- Setup is negligible to 5k and 85 s at 20k; its memory (24 p²) is what binds: 9.2 GiB at 20k.
- The preflight refusal that v0 read from the code is confirmed from 5k up.

## 2. v3.2-dev (leg A item 2)

`Scripts/SMC_BVS/core_v32dev/` is a copy of the v3.1 core; v3.1 is untouched. Four files differ (`cpp/v3_score.h`,
`cpp/v3_blocks.h`, `cpp/v3_start.h`, `v3_fit.R`); the other 14 are identical modulo CR. Its README states the claim,
its domain and the tests.

| change | what | measured on NOTS (v3.1 → v3.2-dev) |
|---|---|---|
| Gram | row-major tiles, 16 accumulators per pass with the v3.1 order of additions, one triangle + blocked mirror | 20k: 39.4 → 6.6 s; 10k: 4.2 → 2.6 s (round C, both including the copy to R, shared nodes) |
| neighbour graph | per-column correlations, `partial_sort` under the v3.1 total order | 20k: 59.1 → 3.6 s; 10k: 10.4 → 0.5 s |
| linkage distances | computed straight from the Gram (no correlation copy) | setup peak at 20k: 9.24 → 6.26 GiB; 10k: 2.44 → 1.69 GiB |
| block tables | depth-first, row-appended Cholesky; production scorer on every unusual event | 20k: 0.50 → 0.12 s |
| LS0 preflight | scan bound p + k\*(p − k\*) instead of p + p²/4 (admission only) | charge at 24 h: 5k 53–94 → 5.8–7.0 h; 10k 231 → 9.2–13.7 h; 20k 936–1,372 → 18.8 h (admitted) |
| whole setup | | 5k: 4.2 → 1.6 s; 10k: 16.3 → 4.6 s; 20k: 85.6 → 23.1 s (round A) |

Sources: `results/leg_a_setup_compare_round{A,C}.tsv`. Not in leg A, by HQ's ruling: Gram-free scoring. Nothing here
changes the islands, which are where the time goes.

## 3. Bit-identity (leg A item 3; also track 1's gate 0 for these units)

### 3.1 Claim

For the same (X, y, seed, compiler, flags), every output field of `v3_fit` under v3.2-dev equals v3.1 bit for bit,
except wall-clock and memory numbers and the preflight record, on fits where both versions take the same admission
decisions (initial preflight, pre-escalation preflight, runtime guard). The preflight change alters admission by
design. Domain of the argument: finite inputs with numeric correlations, which is what `v3_fit` produces; outside it
the headers call the v3.1 code itself.

### 3.2 Evidence (all on NOTS, sapphirerapids, GCC 14.3.0, R 4.5.2, unless marked local)

| test | what is compared | result |
|---|---|---|
| unit harness `tests/bitid_units.cpp`, one source compiled against each core | byte dumps of Gram, dendrogram, blocks, neighbour graph, tables, route counters, start, start mode, a small island and a local search; 50 cases that assert their branches (QR route, refactor route, Q recomputation, numerical failure, sub-models above K, tile boundaries, NaN and Inf inputs, the A-pivot case) | dumps identical (sha256 964091b0…), 0 in-process reference mismatches, 0 branches missed (job 2695486) |
| `scripts/export_units.R` | 10–12 R exports on each of 11 raw contexts, including the failure return of `cpp_setup` | identical (job 2695321) |
| setup only at p = 5k, 10k, 20k | hashes of the whole Gram, blocks, tables, start, neighbour graph, duplicate components, cut group, route counters | identical at all three p (job 2695332) |
| **24 PROD-H units**, one per p × S × c cell, replicate r001, inputs regenerated and checked against the frozen manifest, PROD-H allocation passed to `v3_fit` | fingerprint of the whole fit (version 2) | **24 of 24 identical**, v3.1 against the final code bbdfea0 (`results/bitid_prodh_v31_vs_v32C.tsv`) |
| the same 24 + 10 supplementary units, first revision e5afee7 | same | 34 of 34 identical (`results/bitid_roundA_v31_vs_v32A.tsv`) |
| **10 supplementary units** (3 exact-branch fits, 4 small SMC fits with duplicated, integer and near-constant columns, `y_constant`, `no_predictors`, the tie-DP design) | same | **10 of 10 identical** against bbdfea0 (`results/bitid_supp_v31_vs_v32C.tsv`) |
| fingerprint self-test | 14 mutations of non-timing fields must change the hash, 6 timing mutations must not, on 4 saved fits | passed |

What the 24 units cover: both p, all six designs, both signal scales; one escalated fit (`p1000_S5_r001_c100`, tier 1)
plus the escalated tie-DP unit; T = 26–40; every unit returned the same status under both cores, and none was refused by the v3.1 preflight at the
PROD-H allocations (LS0 charge at most 2,456 s of 6,300 s at p = 500 and 10,244 s of 24,000 s at p = 1000). Every score of
every fit took the Cholesky route: the fallback routes cannot be reached from standardised data, so they are covered
by the unit harness and the export test on raw data.

### 3.3 Reviews

- **R01, Sol (code review):** no difference on valid fits; two real counterexamples on raw non-finite inputs (NaN
  payloads in the Gram; NaN correlations in the neighbour graph), a fingerprint that dropped too much, coverage gaps.
  All fixed: fallbacks to the v3.1 code, fingerprint version 2, branch-asserting cases, the export test.
  `reviews/R01_code_sol.md`, `R01_disposition.md`.
- **R02, Sol (blind re-read of the final code):** no mismatch in 49 + 116 private cases, 20,000 extreme Gram cases,
  the export test and four fits; verdict NOT ESTABLISHED because the comparison script was not fail-closed and one
  README statement was false. Fixed in scripts, tests and README; **no core code changed after R02**.
  `reviews/R02_code_sol.md`, `R02_disposition.md`. The fixes after R02 were not sent to a third review.

### 3.4 Limits

1. One replicate per cell; one escalated PROD-H fit; no PROD-H unit near its runtime guard.
2. **Comparison with the old v2.2.1 study records (RERUN_SPEC A1–A8 against the published fits) was not possible**:
   the OneDrive mirror is on the PC "Felipe_Bedoya", unreachable from here. What was shown is v3.1 = v3.2-dev. The
   saved v3.1 fits are on NOTS for that comparison (§9).
3. Fits above p = 1000 are compared only through the setup objects (5k, 10k, 20k), not end to end.
4. For raw inputs with NaN correlations the statement is "same code as v3.1, equal on the tested cases", not a
   guarantee: v3.1's own sort is undefined there.
5. The round-C v3.1 run of the tie-DP unit hit its 1 h Slurm limit; its comparison uses the round-A v3.1 record of
   the same unit and core.

## 4. sd(log Ẑ_r) by p (leg A item 4)

Sources: `results/sd_logZ_by_p.tsv`, `sd_logZ_long.tsv` (this leg's 24 PROD-H fits, the tie design and the profiles).
The 2,394 old PROD-H records could not be read; the repo holds only their medians (`ev_pip_rb_plain.csv`), which
agree with the first block below: 0.06 and 0.15 at p = 500 (c050, c100), 0.08 and 0.25 at p = 1000.

| islands | p | particles | fits | sets of 4 islands | median | 90% | max |
|---|---|---|---|---|---|---|---|
| final | 500 | 2,500 | 12 | 12 | 0.065 | 0.096 | 0.17 |
| final | 1000 | 2,500 | 11 | 11 | 0.088 | 0.25 | 0.70 |
| final | 2000 | 2,500 | 1 | 1 | 0.042 | | |
| final, escalated | 1000 (S5 c100) | 10,000 | 1 | 1 | 1.00 | | |
| final, escalated | 400 (tie design) | 10,000 | 1 | 1 | 0.82 | | |
| diagnostic | 500 | 512 | 12 | 53 | 0.15 | 0.36 | 0.96 |
| diagnostic | 1000 | 512 | 12 | 76 | 0.18 | 0.75 | 1.95 |
| diagnostic | 2000 | 512 | 1 | 8 | 0.22 | 0.29 | 0.36 |
| **diagnostic** | **5000** | **1,024** | 1 | 11 | **1.39** | 2.51 | 2.52 |
| diagnostic, tier 1 | 5000 | 4,096 | 1 | 1 | 1.56 | | |
| diagnostic | 400 (tie design) | 512 / 2,048 | 1 | 2 / 1 | 5.9 / 4.2 | | |

W3-P6 (n ≤ 100) stores only the E2 flag (sd > 1): at n = 50, 0/137, 2/40, 13/105, 6/16 completed fits at p = 50, 125,
250, 500 (`results/p6_E2_by_np.tsv`; designs and tiers pooled, every flagged fit at p ≥ 250 escalated).

Reading, with its limits: at p ≤ 2k and N = 2,500 four islands agree closely in most fits; the 5k calibration is the
only point above 2k and its diagnostic islands disagree by 0.5 to 2.5 in log Ẑ. One dataset, diagnostic islands, a
different N: it does not say what final islands of fixed N do at 5k, but it is the first sign that the degeneracy
question is live already at p = 5k.

## 5. DESIGN_v1.md (leg A item 5)

Written, revision 2: measured walls, the fixed-size-island pipeline and what must be built for it, merge estimators
with their bias and variance, the dispersion evidence, the memory path, the theory obligations (O1 and O3 routed
through f01 as HQ directed, with qualifications; new O17–O21) and the framing of the two reserved questions.
Astra's break review of revision 1 (`reviews/R03_design_astra.md`): **UNSOUND**, 18 findings (a wrong normalisation
in the cross-fitted identity, numbers that did not recompute, MiB reported as GB, over-reading of the dispersion
data, steering in §7, missing worker, merge and census contracts). All accepted (`reviews/R03_disposition.md`).
**Revision 2 has not been re-reviewed**; a second Astra round belongs to leg B's start. The design decides nothing.

## 6. NOTS ledger (hard cap 150 task-hours; sacct, 2026-11-12 04:03 CT)

| job | run | tasks | task-hours |
|---|---|---|---|
| 2692663, 2692676 | smokes (the first failed at start: quoting) | 2 | 0.02 |
| 2692688 / 2692689 / 2692691 | profiles p1k / p2k / p20k | 3 | 0.29 / 0.92 / 1.31 |
| **2692690** | **profile p5k — RUNNING**, limit 24 h, fit guard 23 h | 1 | 8.58 so far |
| 2693103, 2693104 | round A: supplementary + unit harness; setup comparison | 9 | 1.55 |
| 2693105 / 2693106 / 2693139 / 2693141 | round A: 24 PROD-H units under both cores | 48 | 14.01 |
| 2695321, 2695332, 2695486 | round C: supplementary (one task timed out at 1 h), setup comparison, final unit harness | 12 | 2.06 |
| 2695333 / 2695334 / 2695335 / 2695336 | round C: 24 PROD-H units under the final v3.2-dev | 24 | 7.61 |
| | **finished jobs** | 98 | **27.77** |
| | **finished + worst case of the running job** | | **51.8 of 150** |

Commons only (plus two scavenge smokes); every job pinned to sapphirerapids; at most about 45 tasks at once; W3-P6 had 4
running tasks throughout and nothing queued behind mine. HOLDS.md was read before every submission: no hold.
The largest worst case admitted at any time was 131 task-hours.

## 7. Leg B proposal (bit-identical work and measurements only)

| item | content | why | NOTS (task-hours) |
|---|---|---|---|
| B1 | Engine, [OP-bit]: preallocated scorer scratch (v0 S1), flips in place instead of whole-particle copies (v0 P1), order-buffer reuse (P7). Same harness and the same 24 units as the gate. | The islands are over 97% of the time in every profile and leg A did not touch them. | 30 |
| B2 | Island-only worker and merge as specified in DESIGN_v1 §4.1, checked against the serial run at R′ = 4; the four diagnostic islands of a rebuild run concurrently. | Removes the sequential depth that stops 5k–10k fits at 24 h. **Needs an HQ ruling first (O17):** estimates, HPM and top store are identical, the `fresh` counters and cache statistics are not. | 40 |
| B3 | Measurement, no core change: final islands of N = 2,500 on frozen grids at p = 2k, 5k, 10k, 20k (16 islands each), and N = 10,000 at 2k and 5k. | σ̂ against p and N: the number both reserved questions hinge on; today there is one calibration above 2k. | 50 |
| B4 | LS0 preflight after the setup, charged with the actual start-mode size (admission only). | The worst-case charge refuses fits again between 20k and 30k. | 5 |
| B5 | Second Astra round on DESIGN_v1 revision 2; gate 0 against the old PROD-H records once the mirror is reachable. | Open review debt of leg A. | 10 |

Total about 135 task-hours, under a new 150 cap; Claude Work comparable to leg A (lead, two Sol reviews, one Astra).
Not proposed for leg B, because they are law-changing or await the owner: fixed N in production, the primary-PIP
switch, the census rule, Gram-free scoring (Phase 2, bit-identical by v0's local check but excluded by HQ so far).

## 8. Reserved for Felipe (framed, not decided: DESIGN_v1 §7)

- **(i) p = 1M with a fixed N per island.** By the cost formula one island with N = p costs 5.7 h at 20k, 6 days at
  100k and 1.6 years at 1M; with N = 2,500 it costs 0.66 h at 20k (measured), 3.6 h at 100k and 36 h at 1M
  (extrapolated). The price is theory (O1, O3, O4, O18) and an unknown: the dispersion of island evidences at fixed N,
  for which the only data above 2k is the 5k calibration (0.5–2.5).
- **(ii) Primary PIP.** On 25 fits with 4 islands the two estimators differ by at most 0.0023 (up to 1.3 standard
  errors) and give the same median-probability model in all 25. Four islands cannot show their many-island behaviour:
  equal weights keep the island bias, evidence weights lose effective islands when the dispersion is large.

## 9. Pending, and where things are

- **p = 5k profile (job 2692690).** Expected to end by about 08:00 CT (4 islands of N = 20,000, about 1.7 h each); the
  fit's own guard stops it at 23 h in any case. Result: `/scratch/fb31/w3scale/out/prof_p5k/res/prof_p5k.rds`. To
  fold it in: copy it to a folder `<D>/prof_p5k/res/` next to the other profile records and run
  `Rscript analysis/profile_table.R <D> results/profile_v31` and `analysis/sd_logZ_table.R`.
- NOTS workspace `/scratch/fb31/w3scale` (scratch is purged by age): `code/` (v3.1 613f063, v3.2-dev e5afee7 and
  bbdfea0, each with SHA256SUMS), `runs/<id>/` (frozen scripts and tasks per job, read-only), `out/<id>/res/` (records
  and the saved fits of all 34 units under v3.1 and v3.2-dev). The saved v3.1 fits are what gate 0 against the old
  study needs.
- In the repo: `LOG.md`, `PLAN.md`, `DESIGN_v1.md`, `scripts/`, `tests/`, `nots/`, `tasks/`, `analysis/`, `results/`,
  `reviews/` (R01–R03 with dispositions).
- Agents used: lead (Fable 5.2, Claude Work, high); Sol R01, Sol R02 (Codex gpt-6.1-sol, high); Astra R03 (Codex
  gpt-6-astra, high). No Claude helper agents; `claude-personal` never used.

## 10. For HQ's audit

1. The bit-identity verdict rests on `scripts/bitid_compare.R` (fail-closed) over the records listed in §3.2; rerun
   it on `out/*/res` to check.
2. Two things were done beyond the brief's list and are bit-identical: linkage distances straight from the Gram
   (memory), and the non-finite fallbacks (after R01).
3. The v3.2-dev directory is a development copy, not a release: no `source_manifest.json`, README states the scope.
4. Decisions wanted: the O17 ruling (B2), approval of leg B, and whether the 5k result should be folded in by this
   lead or by HQ.
