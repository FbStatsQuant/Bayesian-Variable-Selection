# Recovery options for "first 1M fit before the holidays" (Engineering manager, 2026-11-15, for HQ's morning brief)

**Critical path:** WP3 island kernel (Sol: 12–18 agent-days) → WP4 calibration/merge integration → T5 end-to-end on NOTS
(10⁵) + the precision study → 10⁵ rung → 1M pilot. WP1 is done; WP2 and WP5 are in review; WP3 and WP4 are building.
Baseline (5 Opus builders, scope as is): first 1M fit ≈ **Jan 5–9**.

| option | what | cost (honest) | critical-path effect | first 1M fit |
|---|---|---|---|---|
| (a) 7 Opus builders | split WP3 into kernel+RNG / stores+ledger+checkpoint / reference+T3/T6 tests; split WP4 into calibration / merge+tail; one T5/integration engineer | ≈ +40% Claude Third load for ~3 weeks, plus 2 more reviewers; risks: contract churn (INTERFACES is at v0.1.5), merge conflicts (already seen once with WP2), my review bandwidth | saves ≈ 4–6 days | ≈ Dec 29 – Jan 2 |
| (b) +1 Fable on WP3, §9 request | 1 Fable 5.2, high, ≈ 3 days: architect review of the WP3 design (deterministic stores under threads, addressed sampling, restart) **before** the code hardens, then pairs on the label-major kernel and reviews WP3's first PR | expensive per day; small in total (1 agent, ~3 days); the account is the owner's choice | **de-risks rather than speeds up**: the hardest integration has no second design opinion today; a late redesign there would cost 1–2 weeks | removes a ≈ 1–2-week tail risk |
| (c) descope/parallelise (no harm to the 1M claim) | (1) no **bit-form label-major** kernel: the theory mode T on the overlap runs the slower particle-major bit path (needed only at ≤ 10⁴); (2) stage-boundary checkpoints only (1M islands ≈ 0.6–1.5 h; no intra-stage checkpoints); (3) competitors at 1M limited to lasso + one variational + SIS (Sol's minimum); (4) the precision study and the 10⁵ T5 gate run in parallel on the first working engine; (5) occupancy and terminal-support diagnostics deferred | ≈ 0 extra; slightly slower T runs at 10⁴ (≈ +50 core-h) | saves ≈ 5–7 days | ≈ Dec 28 – Jan 2 (with 5 builders) |
| (a) + (b) + (c) | all three | as above, combined | saves ≈ 10–13 days and removes the WP3 tail risk | **≈ Dec 21–23**: possible before the holidays, **not safe** (no slack for a failed gate) |

**Recommendation:** (c) now (my call, no extra cost); (b) as a §9 request (1 Fable, ~3 days, WP3 design and kernel review)
if the owner wants the before-holidays date to be realistic; (a) only with (b), since more builders without a stronger WP3
design increases churn. Honest bottom line: **before the holidays needs (a)+(b)+(c) and every gate passing first time;
the first week of January is the realistic date** with (c) alone.
