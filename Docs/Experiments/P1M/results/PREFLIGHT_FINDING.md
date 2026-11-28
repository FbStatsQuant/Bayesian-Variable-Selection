# Writing's preflight finding: what each study used, and the doc fix (Engineering, 2026-11-16)

**Finding (Writing D1, via HQ_NOW):** in core v3.1 the default `v3_fit` preflight is NOT memory-only. With `ls0 = TRUE`
(default) and `v3.ls0_cap` = `ell_n_plus_mode` (default), `ls0_wc = TRUE` (`Scripts/SMC_BVS/core/v3_fit.R:113-115`,
again at :145 before escalation), so the LS0 worst-case time is charged against `allocation$hours` (default 24 h):
≈ 563 h at n = 200, p = 10⁴, so a default fit returns `resource_limit` before setup.

## Which settings each study used (checked in code)
| study | code | preflight in effect | affected? |
|---|---|---|---|
| 2,400-fit study, 2026-10-28 campaign | `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2*/` | memory-only: the v2.2 / v2.2.1 cores contain no LS0 code (0 matches for `ls0`) | no |
| **W3-P6** (corrected 11-16; my first entry wrongly read PLAN.md phase P6 / campaign D14 as this ticket) | `Theory_work/Wave3/W3-P6/scripts/p6_fit.R:56` calls `v3_fit` on core = `git archive` of main 2252d57 (DESIGN.md:10; core identical to 11dc9b7 and to the pin 4676af6 / 72785fe8), LS0 on, arms mr1 (cap ℓ_n + \|S̃₀\|) and wide (`v3.ls0_ell` = ℓ_n + K, :55), allocation hours = 22.5, mem 8–12 GB | **v3.1 with LS0: the LS0 worst-case charge WAS in effect** (DESIGN.md:20, :34: the preflight charges ℓ_n + K + 1 LS0 scans); P6 sized its hours for it | not a doc victim; it used the charge knowingly |
| G0 stage runs (5k / 10k) | `g0/stage/stage_measure.R`: calls the core internals, `v3_run_settings(..., ls0 = FALSE)`, own `--hours` guard (23 h) | no `v3_fit` preflight | no |
| 10⁴ overlap rung (T = law mode and V) and the 1M plan | engine v4 (`smcbvs4`), driver `tools/slurm/p1m_driver.py` | **memory admission only** (`--mem-budget` = 90% of the task; INTERFACES §7), per-task wall limits from the driver (no task above `max_task_hours` = 2 h; worst case = Σ CPUs × limit). No LS0 worst-case charge (EXPERIMENT_PLAN R8 / O14). LS0 runs in `merge` with cap ℓ + \|S̃₀\| (`merge.h:83`, C-GROW MR1) | no |

**Residual risk (mine, not a doc issue):** LS0 time in v4 has not been measured at 10⁴–10⁶ (G0 ran with LS0 off). A
long LS0 in the merge task ends in GUARD-W (no output). The T5 harness (builder 7, O5) and the 10⁶ calibration pilot
will record the tail and LS0 seconds; the merge task's time limit is re-sized with the island and calibrate tasks.

## Doc fix (prepared, not yet applied)
Both files are under the theory freeze: `core/v3_fit.R` is hashed in 5 theory manifests (W2-APP PC1, W3-SCR R2/R3,
W3-MISR R2r/R2r2) and line-cited in ≈ 114 Theory documents, and `core/README.md` is hashed in the Wave1C C-ENG
manifests. Proposed: a PR on an Engineering branch, merged after the Fri 11-20 freeze or on Theory's OK.
- `core/README.md:19`: "Memory-only SMC preflight …" → "SMC preflight: memory, plus (v3.1, `ls0 = TRUE` with the default
  cap ℓ_n + |S̃₀|) the LS0 worst-case time 2·(ℓ_n+K+1)·(p+p²/4)·s(K) against `allocation$hours`. With the defaults
  (24 h) this refuses at p ≈ 10⁴ (≈ 563 h at n = 200). `ls0 = FALSE` or `options(v3.ls0_cap = "ell_n")` gives the
  memory-only v3 preflight. …" (rest unchanged); line 7's example gets a comment saying the same.
- `core/v3_fit.R:16`: "SMC preflight is memory only." → "SMC preflight: memory; with v3.1 LS0 at the default cap it
  also charges LS0's worst-case time (see :25, :113)." Same line count, so no line pointer moves; the hash changes,
  so the manifests above are re-frozen CITATION-ONLY by Theory.
