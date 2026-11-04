# ABL-CONF pre-registration: confirmatory start test (block start vs singleton factors vs prior start)

Written 2026-11-03 (≈ 19:00 CST), before any ABL-CONF fit ran. Task spec: `theory_campaign/tasks/ABL-CONF.md` at
`origin/theory/campaign` 3b65de3. This file, `scripts/` and `results/dryrun/` are committed together in commit 1 on
`theory/ABL-CONF`; the fits are launched from a detached checkout of that commit. **The rule below is not changed after
launch.** Any later departure is recorded under "Deviations" in REPORT.md, with its reason.

This is **not a method question**: the block start ships whatever this run shows (MEET-v31 item 1, Outcome 2). The run
only licenses or refuses two sentences for the paper.

## 1. Claims under test

- **Claim 1 (cost):** "at equal accuracy, the block start (A) costs less than singleton factors (B)".
- **Claim 2 (accuracy):** "at equal declared budgets, the prior start (C) underestimates the evidence and is less
  accurate (than the block start A)". Here "accurate" means the log-evidence estimate; PIP errors for C are reported
  but do not enter the Claim-2 verdict.

Each claim ends as **LICENSED**, **REFUSED** or **INCONCLUSIVE**, by `scripts/apply_rule.py` (section 7).

## 2. Arms (exactly as ABL-START)

Every arm is the production `v3_fit` (preprocess, budgets, calibration with its caps, tiers and rebuild limit, final run
of 4 islands × N_e, kernel, local search, HPM), loaded from a hash-verified copy of `Scripts/SMC_BVS/core` (checked
against `core/source_manifest.json` at every load) plus ABL-START's appended test-only export. Only π₀ differs:

| arm | π₀ | mode of `cpp_abl_setup` |
|---|---|---|
| A | production block (local-to-global) start | 0 (bitwise equal to production, checked in ABL-START) |
| B | singleton factors × capped size prior (blocks of size 1, exact single-variable tables) | 1 |
| C | capped model prior | 2 |

Scripts `abl_core.R`, `abl_exports.cpp`, `abl_fit.R` are byte-identical copies of
`origin/theory/ABL-START:theory_campaign/ABL-START/scripts/` (commit 0cc3789; sha256 prefixes 7f4d5e001ef7efef,
15de1b27c094e85b, 298398a77a2dbb22). Arm D is not run.

## 3. Designs and seeds

Study data, read-only, from `/home/fb31/ls0_work/study/` (same X, y for all arms and all seeds of a design):

| design | role | ABL-START single-seed log Ẑ A / B / C (s) |
|---|---|---|
| `p0500_S1_r001 c100` | favourable | −69.59 / −69.55 / −82.88 (568 / 610 / 2,635 s) |
| `p0500_S4_r001 c100` | correlated / masked | −65.80 / — (B > 4 h) / −75.47 (1,696 / > 14,000 / 2,930 s) |
| `p0500_S5_r001 c100` | correlated / masked | −105.36 / −105.52 / −112.07 (1,072 / 1,603 / 3,031 s) |

Seeds are `study method_seed + offset`. Study method seeds lie in [5,420,001, 5,570,100], so no ABL-CONF seed equals any
study seed (in particular none equals the study seed of its design).

| role | what | offset | S1 seeds | S4 seeds | S5 seeds |
|---|---|---|---|---|---|
| test | arms A, B, C, k = 1..10 (paired: the three arms of pair (design, k) share the seed) | 1,000,000 + k | 6,420,002 … 6,420,011 | 6,450,002 … 6,450,011 | 6,460,002 … 6,460,011 |
| refA | reserved arm-A reference fits, k = 1..8 | 2,000,000 + k | 7,420,002 … 7,420,009 | 7,450,002 … 7,450,009 | 7,460,002 … 7,460,009 |
| refB | reserved arm-B guard fits (S1 only), k = 1..4 | 3,000,000 + k | 8,420,002 … 8,420,005 | — | — |

Total: 90 test fits + 24 refA + 4 refB = **118 fits**. The exact queue is `results/queue.txt` (from
`scripts/make_queue.py`). Pairing is by (design, k).

## 4. Per-fit wall cap and delivery

- **Cap: 4,500 s (75 min) of process wall time per fit**, enforced by `timeout` on the whole `Rscript` process (R start-up
  included; the compiled core is cached, so start-up is seconds). Reason for 75 rather than the suggested 60 min: arm C
  took 2,635–3,245 s on these and similar designs in ABL-START, which leaves only 10–27 % headroom at 60 min; capping C
  for reasons of machine load would make Claim 2 untestable. Arm B on S4 is expected to hit the cap on most seeds.
- A fit is **delivered** iff the process ends within the cap, the fit's own status is `completed`, and log Ẑ is finite.
  Every other terminal outcome (**capped**; **failed** = R error or a non-`completed` fit status) is a delivery failure.
- A delivery failure **counts against its arm for cost** (cost = +∞ in the cost sign test) and is **reported**. It is
  **excluded from accuracy comparisons only in the pairs where it failed**: an accuracy comparison of arms X and Y uses
  exactly the pairs where both X and Y delivered; a failure of arm C never removes an A-vs-B pair, and vice versa.
- A process killed from outside before the cap (server restart, reboot; rc 143/137/129/130) is not an outcome: it is
  re-run with the same seed (`scripts/relaunch.sh`) and logged. An R error is terminal; re-running it would be a recorded
  deviation.

## 5. Reference (fixed in advance, independent of the test fits)

Per design, from the delivered **refA** fits only (reserved seeds, never used as test fits):
- log Z_ref = log of the mean of all pooled island Ẑ_r (K fits × 4 islands; each island Ẑ_r is unbiased for Z);
- **its own error:** se_ref = SD over the K fits of the fit-level log Ẑ / √K (reported with the SD itself);
- PIP_ref = Ẑ_r-weighted mean of all pooled island PIP vectors;
- best-known mode = argmax F over the HPMs of every delivered fit of the design (any role or arm) and S₀.
A design whose reference has K < 6 delivered refA fits is inconclusive for both claims.

**Guard against a reference that favours arm A** (it shares A's start): (i) on the favourable design S1, the same
construction on the 4 reserved **refB** fits gives log Z_refB; the guard passes iff
|log Z_ref − log Z_refB| ≤ 0.25 + 2·√(se_ref² + se_refB²) nats (with KB ≥ 3). If the guard fails or is unavailable,
neither claim can be LICENSED. (ii) Both claims also carry a **head-to-head** condition that does not use the
reference (log Ẑ_A − log Ẑ_B within ±0.5 nat; log Ẑ_C below log Ẑ_A). The A-vs-B comparison is reported both against the
reference and head to head.

## 6. Metrics per fit (`scripts/summarise.R` → `per_fit.csv`)

Process wall time (cost), fit wall, calibration and final seconds; fresh score evaluations, calibration and final
separately (final excludes the table entries already counted in calibration); rebuilds (all tiers); tier; escalation;
T of the final grid; status; log Ẑ and its error vs log Z_ref; island log Ẑ SD; max and mean |PIP − PIP_ref| for
both PIP rules (equal-weight and Ẑ-weighted islands); HPM = best-known mode; HPM = S₀; min ESS fraction; E1–E3 flags.

## 7. Decision rules (written as code: `scripts/apply_rule.py`, sha256 prefix 8d5d888cf3fecf3d)

Constants: α = 0.05; non-inferiority / equivalence margin for log Ẑ **δ_Z = 0.5 nat** (a factor 1.65 in Z; in ABL-START
A and B agreed within 0.02–0.24 nats and island SDs were 0.02–0.17); margin for the Ẑ-weighted max PIP error
**δ_P = 0.05**; at least **6** delivered pairs for an accuracy test; at least **6** reference fits.
Confidence bounds are distribution-free bounds for a median by sign-test inversion (UCB/LCB one-sided at 95 %; UCB2/LCB2
at 97.5 % per side, i.e. a two-sided 95 % interval). With 10 pairs, UCB is the 2nd-largest value and LCB the
2nd-smallest; a one-sided sign test at α = 0.05 needs ≥ 9 wins of 10 (≥ 8 of 9, ≥ 7 of 8).

**Claim 1 (A vs B), per design.**
- Cost: one-sided sign test on process wall time per pair, failure = +∞; pairs where both failed and exact ties drop.
  `cost_holds` iff p_A ≤ α; `cost_rev` iff the same test favours B at p ≤ α.
- Accuracy, on pairs where A and B both delivered (testable iff ≥ 6 pairs and reference K ≥ 6):
  `acc_holds` iff UCB(|err_A| − |err_B|) ≤ δ_Z **and** UCB(pipzw_A − pipzw_B) ≤ δ_P **and**
  [LCB2, UCB2] of (log Ẑ_A − log Ẑ_B) ⊂ [−δ_Z, δ_Z]. `acc_rev` iff LCB(|err_A| − |err_B|) > δ_Z or LCB(pipzw_A − pipzw_B) > δ_P.
- Verdict: **refuted** if cost_rev or acc_rev; **holds** if cost_holds and acc_holds; **holds_nondeliv** if cost_holds,
  accuracy not testable, and B failed to deliver in ≥ 5 pairs where A delivered (B produced no estimate to compare;
  reported as "B did not deliver within the cap"); else **inconclusive**.
- Overall: **REFUSED** if any design is refuted; **LICENSED** iff every design is holds or holds_nondeliv, **at least two
  designs are holds** (equal accuracy actually tested), the guard passed and no fit is pending; else **INCONCLUSIVE**.

**Claim 2 (A vs C), per design**, on pairs where A and C both delivered (testable iff ≥ 6 pairs and K ≥ 6):
- `under` iff UCB(err_C) < −2·se_ref **and** UCB(log Ẑ_C − log Ẑ_A) < 0; `less` iff LCB(|err_C| − |err_A|) > 0.
- Verdict: **refuted** if testable and (UCB(|err_C| − |err_A|) < 0 or LCB(log Ẑ_C − log Ẑ_A) > 0 or LCB(err_C) > 2·se_ref);
  **holds** if testable, under and less; else **inconclusive**.
- Overall: **REFUSED** if any design refuted; **LICENSED** iff all three designs hold, the guard passed and no fit is
  pending; else **INCONCLUSIVE**.

Everything else in `per_fit.csv` (evaluations, rebuilds, tiers, island SD, PIP means, equal-weight PIP, HPM) is
reported descriptively and decides nothing.

## 8. Dry run of the rule (before launch; `scripts/dryrun.sh` → `results/dryrun/DRYRUN_OUTPUT.txt`)

| input | Claim 1 | Claim 2 |
|---|---|---|
| (i) ABL-START table, 12 designs × 1 seed, per design (stand-in A+B reference) | INCONCLUSIVE (n = 1 per design) | INCONCLUSIVE |
| (i) same, pooled as 12 pairs of one pseudo-design, no guard pool | INCONCLUSIVE (design holds; guard unavailable, < 2 designs) | INCONCLUSIVE (holds; guard unavailable) |
| (i) same, pooled, guard forced to pass (hypothetical) | INCONCLUSIVE (only 1 design) | LICENSED |
| (ii) synthetic `expected` (A cheaper at equal accuracy; B capped on S4; C −8 nats) | LICENSED | LICENSED |
| (ii) synthetic `no_difference` | INCONCLUSIVE | INCONCLUSIVE |
| (ii) synthetic `B_fails_badly` (B capped/failed everywhere) | INCONCLUSIVE (holds_nondeliv on all, 0 tested) | LICENSED (A–C unaffected) |
| (ii) synthetic `C_fails_badly` (C −30 nats, capped 3/10) | LICENSED (A–B unaffected) | LICENSED |
| (ii) synthetic `reversed` (B cheaper and more accurate; C more accurate) | REFUSED | REFUSED |
| (ii) synthetic `guard_fails` (refB 2 nats from refA) | INCONCLUSIVE | INCONCLUSIVE |

So the rule can return each of licensed / refused / inconclusive for both claims, and a badly failing arm does not make
the other pair's comparison vacuous (lesson 7). The pipeline `summarise.R` → `apply_rule.py` → `report_tables.py` was
also run end to end on ABL-START's existing fit files mapped into a scratch work directory (no new fits).

## 9. Compute plan

Owls only, 3 detached `owls_run -j 2` jobs (6 single-threaded fits at a time, 6 of the 8-core budget), all walking one
shared queue (`results/queue.txt`: reference block first, then seed blocks k = 1..10, longest fit first in each block).
Work directory `/home/fb31/ablconf_work` (fits, logs, status; outside git). Expected 59.9 core-hours and **≈ 10.2 h**
of wall time on ABL-START timings (`results/schedule_estimate.txt`); those timings were taken at an unknown Owls load,
and Owls load is ≈ 2 at launch, so it may be faster. This is at the top of the 8–10 h budget; no design or seed was cut.
No fit result is read before the queue is complete except through `scripts/progress.sh` (counts and the one-line log
of each fit); the rule is applied once, by `scripts/finalize.sh`, when every fit has a terminal outcome.
