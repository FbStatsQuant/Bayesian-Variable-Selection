# CHECKPOINT_2 — W3-SCALE (track 3, scaling), leg B

Branch `theory/W3-SCALE`; leg B approved at CP1 (HQ_DECISIONS "W3-SCALE CP1"): B1–B5, bit-identical work only, cap
150 task-hours. Lead: Fable 5.2 (Claude Work) until the 11-12 limit, then Opus 5.5 high (Claude Personal). Every
NOTS number below is from Sapphire Rapids nodes (bb*, Xeon Platinum 8468); nothing is pooled across node types.

## 0. Summary

| item | status | one line |
|---|---|---|
| 5k fold-in | done | v3.1 fit at p = 5k: 12.2 h (calibration 5.40 h incl. escalation; final run 6.82 h at N = 20,000); HPM = truth; σ̂ 0.77 |
| B1 engine | done, gate PASS | joint Cholesky, in-place proposals, store quick reject: 1.69 → 1.22 µs/step (2k), 1.76 → 1.27 (20k); 24/24 PROD-H + 10/10 supplementary units IDENTICAL |
| B4 LS0 preflight | done | charged after setup with the actual start mode; at 20k the charge is 10.4 h instead of 969 h, so the fit is admitted |
| B5 Astra R04 | done | DESIGN_v1 rev 2 UNSOUND as a build spec (4 CRITICAL, 5 MAJOR, 1 MINOR); all accepted; rev 3 (not re-reviewed) |
| B3 σ̂ census | done (3 of 6 runs cut by budget) | σ̂ at N = 2,500: 0.09 at 2k, 0.76–1.15 at 5k–20k; at 5k N = 10,000 does not shrink it (right tail) |
| B2 workers | **not built** | O17 case (a) fails; case (b) needs a lookup-trace replay (0.3 TB per fit at 5k). Options in §5 |

NOTS: 54.06 task-hours of 150 (§7). No hold was in force at any submission.

## 1. Gate round D (B1 + B4; revision D = 6866f57, core key dd37d323a353)

Fail-closed comparison (`scripts/bitid_compare.R`, fingerprint version 2) of the round-A v3.1 records against revision D:
- PROD-H: **24 of 24 IDENTICAL** (0 DIFFERENT / ADMISSION_DIFFERS / INVALID / MISSING) — `results/bitid_prodh_v31_vs_v32D.tsv`.
- Supplementary units, both cores in round D: **10 of 10 IDENTICAL** (the tie-DP v3.1 run finished this time) — `results/bitid_supp_v31_vs_v32D.tsv`.
- Setup only at 5k / 10k / 20k: tables, setup objects, whole Gram and routes identical; setup 1.05 / 5.41 / 22.8 s
  (v3.1: 4.27 / 16.8 / 85.8 s) — `results/leg_b_setup_compare_roundD.tsv`.
- Engine benchmark (two islands + both local searches, every output byte dumped): dumps identical; p = 2k 1.69 →
  1.21–1.23 µs/step, p = 20k 1.756–1.766 → 1.257–1.287 µs/step.
- Unit harness (50 cases) dumps identical; B4 preflight tests passed on NOTS (`tests/preflight_b4.R`).
- B4 is admission only: the v3.2-only record `preflight_ls0` goes to the delivery record and is compared as an
  admission decision. `v3.ls0_preflight = "worst_case"` restores leg A's rule.

Limit: revision D's code was not given a Sol code review in leg B (leg A's R01/R02 covered revisions A–C); the claim
rests on the empirical gate above.

## 2. p = 5k profile, folded in (job 2692690, bb4u17c1)

Calibration 19,444 s (tier 0: 11 rebuilds, E2 fired → tier 1, 1 rebuild); tier-1 final run N = 20,000, T = 33:
24,562 s (one island 1.71 h; 1.19 µs per bridge step; hit rate 0.31; 4,977 cache clears); whole fit 44,025 s = 12.2 h;
peak 1.62 GB; HPM = truth; log Ẑ = −114.89; σ̂ of the 4 final islands 0.77 (R_eff / R 0.56). Tables regenerated
(`results/profile_v31_*.tsv`, `results/sd_logZ_*.tsv`; the only new rows are the 5k final run) and DESIGN_v1 §0, §2
item 1 updated. CHECKPOINT_1.md left as committed.

## 3. B3: dispersion of island evidences against p and N

Driver `scripts/census_measure.R` (measurement only, revision D = v3.1 outputs): one S3-type dataset per p (the leg A
profile datasets), tier-0 calibration with the fixed-size budget H = 512, its grid frozen, then R islands per N on that
grid (streams 10…), no escalation. Table `results/b3_census.tsv` (script `analysis/b3_census_table.R`; node and CPU per row).

| p | N | node | islands | σ̂ | robust σ̂ (1.4826·MAD) | max − median | R_eff / R | max W | island (s, median) | calibration (h; rebuilds; T) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2k | 2,500 | bb2u24c1 | 16 | 0.086 | 0.154 | 0.16 | 0.99 | 0.07 | 226 | 0.41; 8; 33 |
| 2k | 10,000 | bb2u24c1 | 16 | 0.029 | 0.048 | 0.06 | 1.00 | 0.07 | 905 | (same grid) |
| 5k | 2,500 | bb2u19c1 | 16 | 0.755 | 0.999 | 1.72 | 0.56 | 0.22 | 629 | 1.89; 13; 36 |
| 5k | 10,000 | bb2u19c1 | 14 of 16 | 1.348 | 0.544 | 4.39 | 0.11 | 0.79 | 2,647 | (same grid) |
| 10k | 2,500 | bb3u13c1 | 6 of 16 | 1.152 | 0.959 | 2.56 | 0.33 | 0.69 | 2,503 | 5.91; 14; 28 |
| 20k | 2,500 | bb3u11c1 | 11 of 12 | 0.954 | 0.723 | 2.49 | 0.38 | 0.42 | 2,948 | 6.68; 15; 30 |

Readings (measurements, one dataset and one seed per p; p is confounded with the dataset):
1. Between 2k and 5k σ̂ at N = 2,500 rises from 0.09 to 0.76; at 10k and 20k it is 0.95–1.15. R_eff / R falls to
   0.33–0.56.
2. At 2k σ̂ falls by 2.9× from N = 2,500 to 10,000 (1/√N predicts 2×). At 5k the bulk narrows (robust σ̂ 1.00 → 0.54,
   and the median log Ẑ_r rises by 0.7) but one island sits 4.4 above the median, so σ̂ rises to 1.35 and one island
   carries 79% of the weight: a right tail that 4× more particles did not remove.
3. Every island of every run found the same best model (= truth); per-island PIPs agree (sd ≤ 0.001); max_j
   |PIP_Z − PIP_eq| ≤ 0.0005 in all six runs. The dispersion is in the evidence estimates, not in which models the
   islands visit.
4. Cost at fixed N = 2,500 (revision D): one island 0.70 h at 10k and 0.82 h at 20k (0.55–0.88 h on one node), about
   2× and 1.1× DESIGN_v1's formula (0.36, 0.72 h); island time is linear in N at 5k (629 → 2,647 s). The fixed-size
   calibration alone takes 5.9–6.7 h at 10k–20k, i.e. it is the sequential part that remains once islands are parallel.
5. Three runs hit the driver's budget (my estimates were too low): 10k has only 6 islands, so its σ̂ is loose (with 5
   degrees of freedom the 95% interval for σ is about 0.6×–2.5× the estimate).

## 4. B5: second Astra round (R04) on DESIGN_v1 revision 2

UNSOUND as a build specification: 4 CRITICAL, 5 MAJOR, 1 MINOR. Central: `fresh` counts feed published tables and cannot
be rebuilt from worker summaries, because the serial run shares one score cache over the four islands and both searches
and clears it when full (verified, `evidence_h2.py:98-105,139-141`); N1 did not cover the RB PIP; leader stores are
outputs; the merge memory bound was wrong. All accepted (`reviews/R04_disposition.md`): DESIGN_v1 revision 3 with a
worker-equivalence contract at R′ = 4 (§4.1). Revision 3 has not been re-reviewed. B3 numbers added to §4.4 and §7.

## 5. B2 under the O17 ruling — options for HQ

The ruling: everything statistical and every quantity in a published table or theorem check must be identical; the
`fresh` / cache counters may differ only if (a) none feeds a published table, or (b) the worker reports serial-equivalent
totals that match exactly. **(a) fails**: `fresh` feeds the EVIDENCE §8 / RERUN_SPEC cost column. Everything else in
the contract (estimates, PIPs, HPM, evidences, top store) can be made identical by DESIGN_v1 §4.1.

Size of the serial cache history (final run only): 3.9·10⁸ lookups at 1k, 9.1·10⁸ at 2k, **1.8·10¹⁰ at 5k**
(N = 20,000), i.e. 6 GB, 15 GB and **about 290 GB** at 16 bytes per lookup.

| option | what it is | meets O17 | cost / risk |
|---|---|---|---|
| **B2-1 trace replay** (case b) | workers write the ordered lookup trace (model key, phase, mechanism, incl. non-emitting lookups); the merge replays it in island order through the serial cache rule (capacity, clear-when-full) and continues through the tail; route counters attach to replayed misses | yes, exactly | trace I/O 6–15 GB per fit at 1k–2k, ~0.3 TB at 5k, more beyond; one sequential replay pass (~10⁹–10¹⁰ lookups); the replay itself must be gated against serial runs. Feasible for the R′ = 4 equivalence build at p ≤ 2k; heavy as a production path at p ≥ 5k |
| **B2-2 serial-only cost column** (case a by scope) | process-parallel runs publish no `fresh` / cache numbers; the cost column stays serial-only and is filled only by serial runs; worker counters are reported as a separately named, worker-local quantity outside the published table | yes, if HQ confirms that a run outside the published table may report worker-local counters | no trace; the cost column cannot be produced for fits that only run in parallel (exactly the large-p fits) |
| **B2-3 redefine the cost column** | publish worker-local `fresh` totals (deterministic, per-island caches) as the cost measure for all new runs, with a note; old tables keep their values | no — changes a published quantity; needs an HQ/owner ruling beyond O17 | cheapest to build; registry and lifecycle change for the cost column |
| **B2-4 defer** | build nothing in leg C beyond the contract tests; keep fits serial (≤ about 10k under 24 h with B1/B4) | n/a | blocks the 5k–20k scaling runs that motivated B2 |

Lead's recommendation (HQ decides): **B2-1 for the R′ = 4 equivalence build at p ≤ 2k only** (it is the only option that
proves the contract under O17 as ruled), **together with B2-2 for production runs at p ≥ 5k** (no trace; the cost
column stays serial). B2-3 is the long-run simplification but needs a ruling. Estimated leg-C NOTS for B2-1 + gate:
about 40 task-hours (CP1 estimate), plus about 15 GB of scratch per 2k fit while its trace exists.

## 6. Reserved for Felipe (framed with the new numbers; not decided)

- **(i) p = 1M with fixed N per island.** New: at N = 2,500, σ̂ is 0.76–1.15 for 5k–20k (R_eff / R 0.33–0.56), and
  at 5k quadrupling N did not shrink the right tail. One island costs 0.70 h at 10k and 0.82 h at 20k (measured), and
  the fixed-size calibration 5.9–6.7 h (sequential). DESIGN_v1 §7 keeps the formula's 3.6 h at 100k and 35.8 h at 1M
  per island as an extrapolation; the measured 10k point is 2× above that formula.
- **(ii) Primary PIP.** New: in six many-island runs (6–16 islands) with R_eff / R down to 0.11, max_j |PIP_Z − PIP_eq|
  ≤ 0.0005 because all islands agree on the PIPs. On these data the choice does not move the PIPs; it matters only
  where islands disagree, and these runs contain no such case.

## 7. NOTS ledger (cap 150 task-hours; sacct)

| jobs | content | task-hours |
|---|---|---|
| 2697743–2697749 | gate round D (bench, supplementary, setup, 24 PROD-H) | 7.17 |
| 2698177 | B3 p = 2k | 5.40 |
| 2698178 | B3 p = 5k | 15.50 |
| 2698179 | B3 p = 10k | 10.49 |
| 2698180 | B3 p = 20k | 15.50 |
| **leg B total** | | **54.06** |

The 5k profile (2692690, 12.23 h) stays on leg A's ledger. Commons only, `--constraint=sapphirerapids`; at most 38
tasks at once (gate D), W3-P6 had one job running at the B3 submission and nothing queued behind ours; HOLDS.md (main checkout) read before
every submission: empty. No job of others touched; nothing running now.

## 8. Where things are

- Repo (this branch): `LOG.md` (ledger B1–B11 with actuals), `DESIGN_v1.md` (rev 3 + 5k fold-in + B3), `results/`
  (new: `bitid_*_v32D.tsv`, `leg_b_setup_compare_roundD.tsv`, `b3_census.tsv`; regenerated profile and σ̂ tables),
  `analysis/b3_census_table.R` (new), `reviews/R04_*`.
- NOTS `/scratch/fb31/w3scale`: `code/v32dev_6866f57`, `runs/<id>` (frozen), `out/{bench_D, bitid_*_D, setup_cmp_D,
  b3_p*}/res`, `stage/s8` (scripts of the B3 runs, from 1da2ff6).
- Agents in leg B: lead; Astra R04 (Codex gpt-6-astra, high). No Claude helpers.
- Files of this run (CP2, B3 fold-in, DESIGN_v1 B3 text, ledger actuals) are **uncommitted** in the worktree, per HQ's
  "change no git state"; HQ commits.

## 9. Decisions wanted from HQ

1. B2 option (§5).
2. Whether to re-review DESIGN_v1 rev 3 (Astra) and to have Sol review revision D's code before anything builds on it.
3. Whether to repeat B3 at 5k–20k over more datasets/seeds (σ̂ is one dataset per p; per dataset at N = 2,500 with 16
   islands: about 5 task-hours at 5k, 17 at 10k, 20 at 20k, if the islands run as separate tasks after one calibration), which both reserved questions need before they can be decided.
