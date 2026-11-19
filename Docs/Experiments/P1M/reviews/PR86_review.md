# PR #86 review: driver law-mode island/merge N from calib N_final; T island time scales with N

- Reviewer: the ONE Opus review child (HQ_DECISIONS e8aab325), read-only. No pushes, no merge, no NOTS access.
- Head `4b84e585`, base `exp/P1M-engine` = `1b6ddd59`. The diff touches 4 files under `tools/slurm`, +378/−13. No engine source changed (checked with `git diff --stat`).
- Date: 2026-11-18, about 19:30 CST.

## Verdict: ACCEPT-WITH-FIXES

The N logic is correct, and it matches the engine's own definition of the frozen N. The engine stays a hard backstop, so a wrong N can only cause a refusal, never a silent change to the science. V output is byte-identical. The new tests are real.

One fix is required before merge (F1, policy): the scaled island limit must not exceed 2 h. The 3:00 limit in this PR comes from the plan-wide `max_task_hours = 3.0`, which was granted for the T calibrate only. Using it for islands creates a second, unapproved exception to the 2-h rule.

F2 and F3 are small hardening fixes that should go in the same push. Everything else is informational.

---

## What I verified

### 1. The N definition matches the engine
- **Writer.** `src/calib/calib_run.cpp:222` writes calib.bin meta `N` as `frozen_N(b, rule, co.tier_final)`. `calib_run.cpp:62` writes the sidecar's `settings.tiers[e].N_final` with the same `frozen_N(b, rule, e)`, and `calib_run.cpp:217` writes `rec["tier_final"] = co.tier_final`. `include/v4/calib_run.h:53` defines `frozen_N` as `V_N` (2,500) under the bounded rule and `b.N[tier]` under the coded rule, where `b.N[1] = 4·max(2500, n, p)` (`calib_run.h:31-34`).
- **Rule.** `calib_run.cpp:114` uses the coded rule for compat and law, and the bounded rule for V. So `settings.tiers[tier_final].N_final`, which is what `p1m_calib_n.calib_n` reads, equals the binary's meta N by construction. The field names and the meaning of `tier_final` match.
- **Status.** The engine's record `status` is `"completed"` only for `cal_status ok` (`calib_run.cpp:217`). The helper requires `"completed"`, and `p1m_manifest fill` already requires the same of `calib.bin.json` and verifies calib.bin's content hash.
- **Island reader.** `src/island/island_cmd.cpp:223` refuses a manifest/argument N that differs from calib.bin meta N. That is the error W0 hit. The island then uses `C.N` regardless (`island_cmd.cpp:247`).
- **Merge.** The merge never reads `params.N`. It checks each island's meta N against calib.bin's N (`include/v4/merge.h:274`, `:323`; `ms.N = C.N` at `src/merge/wp4_io.cpp:1138`). So the merge `set-n` only affects the record (see I1).
- **Eval and post.** Their templates carry no N (`p1m_driver.py` template build; eval/post params are only `truth_sha256`/`threads`). Calibrate and setup receive `params.N` in `base_params` but do not read it.
- **Other places the plan's N could survive:**
  - `budget.task_seconds` follows the scaled island limit; the engine does not read `task_seconds`.
  - `fit_core_h` = worst case / fits, which is informational.
  - R′ does not depend on N.
  - `--mem-budget` is 90% of the Slurm allocation and does not depend on N.

  None of these can carry a stale N into the science.

### 2. Island memory at N = 40,000 is not a concern
I ran the engine's own planner from the PR builder's build of `4b84e585`: `smcbvs4 island --plan-only 1 --mode law --n 200 --p 10000 --threads 24 --mem-budget 14.4 GiB`.

| N | k = 8 | k = 16 | k = 32 |
|---|---|---|---|
| 10,000 | 284 MiB | 420 MiB | 696 MiB |
| 40,000 | 291 MiB | 430 MiB | 712 MiB |

- Only `particles` grows with N (2 → 8 MiB at k = 8). The total is dominated by the store and the worker buffers, which scale with k and the threads.
- The 16G request (`MEMB` = 14.4 GiB) has more than 20× headroom.
- The tier-1 calibration of AR-T2 already ran at N 40,000 within 16G.
- The merge at N 10⁴ took 28 s and peaked at 213 MB. Its size is driven by the island stores, not N, so the merge's 8G / 0:20 is not at risk.

**AR rescue (islands 2783938, 1:30 limit, 16G).** It was submitted at 00:37:50 UTC and had not been logged as finished when I reviewed (LOG.md ends at 19:21 CST; OPS_W0.md §10). I could not read sacct (no NOTS). **Read its elapsed time and MaxRSS before W1's limits are fixed (see I3).**

### 3. Stage order and failure modes
- **Order.** In `submit.sh`, islands run `afterok` calibrate_i, merge runs afterok islands, and the scripts use `--kill-on-invalid-dep=yes`. So `calib.bin.json` exists, with status completed, before any island starts.
- **Where it runs.** `set-n` runs on the compute node after `fill` and before the engine, under the header's `set -euo pipefail`. A refusal exits non-zero, the island fails, and the merge never starts. Tested: no `island_1.bin` and no `fit.bin` are produced.
- **No race with SHA256SUMS.** `set-n` rewrites only the run-dir copy (`$RUN/manifests/island_$R.json`, `merge.json`), atomically (`p1m_calib_n.py:54`, tmp + `os.replace`). The templates under `$SCR/manifests/` (covered by SHA256SUMS) are never touched. Each restart attempt re-fills and re-sets, which is idempotent.
- **Honest record.** The template and `run_manifest.params.N` keep the plan's N as the pre-calibration record. `run_manifest.calib_N` = `{N_plan, N_final, tier_final, differs, source}`. The filled island manifest carries the frozen N, and the island's output record carries `N` and `tier` from calib.bin. `record-n` is deliberately non-fatal (`|| echo WARNING`), which is acceptable because the islands re-read the record themselves.

### 4. V output is byte-identical (independent spot-check)
I extracted base `1b6ddd59` and head `4b84e585` `tools/slurm` with `git archive` and ran `p1m_driver.py --now 2026-11-18T00:00:00Z` on the same plans:

| plan | files | base vs head |
|---|---|---|
| staging `F_eefcbc4a/plans/OV_W1_V.json` | 68 | identical (`diff -r`) |
| staging `F_eefcbc4a/plans/OV_W0_V2.json` | 32 | identical |
| `precision_p10000_n200_V_N10000_R64_b1` | 32 | identical |
| `optionD_p1000000_n1000_V_N2500_R16_b1` (10⁶) | 23 | identical |

**T plans.** `OV_W0_T2` and `OV_W1_T` are refused at head (`worst case 881.3 > cap 449.4`, `2644.0 > 1348.1`), as the author says. With the cap lifted, the head-vs-base diff of `OV_W0_T2` is exactly:
- `--time=03:00:00` plus a two-line comment in `stage_islands.sbatch`;
- the `set-n` line in `stage_islands.sbatch` and `stage_merge.sbatch`;
- the `record-n` line in `stage_calibrate.sbatch`;
- `task_seconds` 2700 → 10800 and `fit_core_h` in the manifests;
- `islands_time_base` and the worst case in `plan.resolved.json`;
- the ledger row, plus the shipped `p1m_calib_n.py`.

Nothing else changed.

### 5. Tests
- **What I ran.** `TestLawN` (9) and `TestCells` (10): 19/19 pass. My attempt at the full `test_p1m_driver` was killed by the harness (exit 137) before it reported, so I did not re-confirm the author's 69/69 or the engine quick suite.
- **The tests are not vacuous (mutation check).** With `set-n` removed from `stage_body`, `test_escalated_law_fit` and `test_missing_or_corrupt_calib_json_refused[noN]` FAIL, and `test_non_escalated_law_fit` still passes, as it should. The stub calibrate writes the engine's real sidecar shape (`tier_final`, `settings.tiers[e].N_final`).
- **Cases covered.** Escalated, non-escalated, a stale plan N (2,500 at p = 10⁴), V, a missing record, a corrupt record, a record without N, the merge-time loss of N, validation of `calib_n` types and ranges, the time-scale rules, and restart with the scaled `LIMIT_S`.
- **Gaps:**
  - The stub merge refuses on `params.N`, which the real merge does not do (I1). Harmless, but it overstates the engine.
  - No test covers `isa_check` in a theory plan (F2).
  - No test covers a hand-written `islands_time_base` (F3).
  - Several `open(...)` calls without `with` produce ResourceWarnings (nit).

### 6. Science and the frozen engine are untouched
- No file under `src/`, `include/`, `core/` or `CMakeLists.txt` changed.
- The N used is the one the engine already forces (`island_cmd.cpp:247`, `c.N = C.N`). The driver now writes the same value the engine would demand.
- The grid, L, Hm, B and the seeds are untouched.

---

## Findings, by severity

### F1, MAJOR (policy): the 3:00 island limit is a second exception to the 2-h rule
- **Where:** `tools/slurm/p1m_driver.py:141-148` (`law_islands_time`), `p1m_cells.py:69-70`.
- **Problem.** `law_islands_time` caps the scaled limit at `P["max_task_hours"]`. The T overlap plans set that to 3.0 for the T calibrate, the one HQ exception (§0-v2.5 / H-18). The islands therefore inherit 3:00 without anyone having approved it.
- **Evidence it is not needed.** At N 10⁴ the ADJ-OPP-T2 islands took about 8 min, so a 4× N escalation suggests roughly 32 min. 2:00 still leaves about 3.7× headroom over that.
- **Why not `min(4, ceil(...))`.** The factor `min(4, …)` suggested in the brief adds nothing once the 2-h cap is there, and for a stale plan N (2,500 at p = 10⁴, factor 16) it would understate the limit. Keep the factor uncapped and cap the hours.

**Fix:**
```python
# p1m_driver.py, next to THEORY_TIER_MULT
THEORY_ISLANDS_MAX_H = 2.0   # §0-v2.5 / H-18: islands stay <= 2 h; the only > 2 h exception is the T calibrate (HQ)

def law_islands_time(P, f, base):
    factor = max(1, -(-theory_n_max(f) // f["N"]))
    return hhmmss(min(hours(base) * factor, THEORY_ISLANDS_MAX_H, P["max_task_hours"], QOS_WALL_H)), factor
```
Then make these follow-up changes:
- In the docstring and the stage-script comment, change "capped by max_task_hours" to "capped at 2 h (and max_task_hours)".
- In `p1m_cells.py:69-70`, change the comment to: 0:45 × 4 = 3:00 → capped at 2:00, so a T fit's worst case is 224.7 + 120 = 344.7 core-h.
- In the tests, change `03:00:00` to `02:00:00` at `test_p1m_driver.py:1166, 1169, 1179, 1258, 1267, 1269`, change `task_seconds` to `2 * 3600`, change `LIMIT_S=10800` to `7200`, and change the TestCells figure to `224.7 + 4 * 24 * 1.25`.
- Keep the `max_task_hours = 2.0` case at 2:00 and the `N = 20000` case at 0:40.

**Effect on worst cases (driver figures):**

| batch | before PR | PR (3:00) | proposed (2:00) |
|---|---|---|---|
| per T fit | 224.7 | 440.7 | **344.7** |
| `OV_W0_T` / `OV_W0_T2` (2 fits) | 449.3 | 881.3 | **689.3** |
| `OV_W1_T` (6 fits) | 1,348.0 | 2,644.0 | **2,068.0** |

The staged caps (`OV_W0_T`, `OV_W0_T2`, `OV_W1_T`) must be re-issued at the new worst cases or re-sized per H-18 after W0's read-back. That is HQ's decision; the driver correctly refuses the old caps. Billing is still by use: a tier-0 island that finishes in 8 min is billed 8 min.

**If an escalated island ever needs more than 2 h,** the policy-compliant route is the existing restart mechanism (WP7 O4: `restart.attempts`, soft stop + checkpoint). It is not a longer limit. It costs `(attempts − 1) · Rp · cpus · limit` of extra worst case, so do not enable it pre-emptively.

### F2, MINOR (latent): the `isa_check` stage skips `set-n` and is not scaled
- **Where:** `p1m_driver.py:717-731`.
- **Problem.** The D-32 `isa_check` stage fills the island template, with the plan's N, and runs `smcbvs4_isa_check island` without `set-n`. Its `isa_check.time` (default 0:40) is not scaled either. `resolve()` does not refuse `isa_check` in a theory-mode plan.
- **Failure.** Any such fit that escalates is refused (`N differs from calib.bin's frozen N`) and the D-32 check fails. No current T plan has `isa_check`; T plans are ISA-free, with `island_isa` set to `""`. The failure is real but latent.
- **Fix (either one):**
  - (a) Preferred, the smallest: in `resolve()`, refuse when `P.get("isa_check") is not None and any(f["mode"] != "V" for f in P["fits"])`, with the message "isa_check is a V (class-A) check; theory plans are ISA-free". Add a one-line test.
  - (b) Add `set_n('"$RUN/manifests/island_${R}_isa_check.json"')` after its fill, and scale `isa_check.time` with the same rule.

### F3, MINOR: a hand-written `islands_time_base` silently disables scaling
- **Where:** `p1m_driver.py:78-79` (added to `KNOWN_FIT_KEYS`) and `:424` (`"islands_time_base" not in f` skips scaling).
- **Problem.** A plan that carries `islands_time_base`, for example one copied from a resolved plan and then edited, gets no scaling and no check. Its islands then run with an unscaled limit, which an escalated N would overrun.
- **Fix.** Make the scaling idempotent by recomputing it from the base, not by skipping it:
```python
if f["mode"] != "V":
    base = f.get("islands_time_base", res["islands"]["time"])
    lim, factor = law_islands_time(P, f, base)
    if factor > 1:
        if "islands_time_base" in f and res["islands"]["time"] != lim:
            raise PlanError("fit %s: islands time %s is not the scaled limit %s of islands_time_base %s"
                            % (f["run_id"], res["islands"]["time"], lim, base))
        f["islands_time_base"] = base; res["islands"]["time"] = lim
```
The fed-back resolved plan in `test_time_scale_rules` still passes. Add a test in which an edited time is refused.

### I1, INFO: the merge `set-n` only affects the record
The real merge ignores `params.N` (see §1). Keep the call, because it keeps `merge.json` honest. Fix the wording in two places:
- the `p1m_calib_n.py` docstring and the driver docstring ("the merge's N");
- the test stub comment ("the stub island / merge refuse, as the engine does").

Both should say the engine refuses at the island and checks island N against calib N at the merge.

### I2, INFO: the sidecar and the binary are read in two places
`set-n` reads `calib.bin.json`, while the engine reads calib.bin meta. They are equal by construction (§1), and `fill` has already verified calib.bin's hash and the sidecar status. If they ever diverged (tampering), the island would refuse. Nothing to do.

### I3, INFO for HQ: the cost-linear-in-N bound assumes the same grid length
- **Assumption.** The rule assumes island time scales with N alone.
- **What can break it.** At tier 1 the calibration's budget is 4·T0 as well (`calib_run.h:34`). The frozen grid of an escalated fit can therefore be longer than a tier-0 grid, and the true time factor can exceed 4.
- **How to check.** The AR rescue (2783938) is the first measurement. Its island elapsed time divided by 8 min gives the real factor; tier-1 AR has 4× N plus its own grid. If an escalated island takes more than about 1:20 (headroom under 1.5×), revisit F1's cap with HQ, or use restart attempts. Do not raise the limit above 2 h.

### I4, nit
- The docstring's "mixed batch" note on `set-n` is moot whenever the factor is > 1: a V fit and a scaled law fit cannot share one `stage_islands.sbatch`, and `generate()` refuses such a batch ("all fits of one batch must share resources"). That is fine, just worth saying.
- Several new tests open files without `with`, which produces ResourceWarnings.

---

## Summary
1. **ACCEPT-WITH-FIXES.** The N logic matches the engine exactly (`frozen_N(b, rule, tier_final)` = meta N = `settings.tiers[tier_final].N_final`), and the engine still refuses any mismatch. The science and the frozen engine are untouched.
2. Memory at N 40,000: the engine's own plan is under 0.75 GiB against a 14.4 GiB budget. The 16G request is fine.
3. V output is byte-identical: confirmed on 4 V plans (155 files), including OV_W1_V, OV_W0_V2 and a 10⁶ plan. The tests are non-vacuous (mutation check), and 19/19 targeted tests pass. The full suite run was killed by the harness, so 69/69 is not re-confirmed.
4. **F1 (required):** cap the scaled island limit at 2:00 (`THEORY_ISLANDS_MAX_H = 2.0`), not at `max_task_hours`. A 3:00 island limit is a second exception. Effect: a T fit's worst case is 344.7 instead of 440.7; OV_W0_T/T2 689.3 instead of 881.3; OV_W1_T 2,068.0 instead of 2,644.0. The caps must be re-issued.
5. **F2:** refuse `isa_check` in theory-mode plans (it skips `set-n`; latent). **F3:** recompute the scaling from `islands_time_base` rather than skipping it.
6. Before W1's limits are fixed: read the AR rescue's elapsed time and MaxRSS. A longer tier-1 grid can push the time factor above 4.
