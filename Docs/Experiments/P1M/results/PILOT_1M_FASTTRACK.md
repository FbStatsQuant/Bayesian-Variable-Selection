# 1M fast-track pilot plan (Engineering, 2026-11-16 16:40 CT; owner-approved side track, for HQ)

**Goal:** one 1M fit, `6-AR-n200-r01-V-s1` (AR-strong, n = 200, rep 1, V mode, seed 1; MANIFEST_CELLS §1), finished
and evaluated before the advisor report (Dec 1–4). It is the manifest's own 1M pilot moved earlier, not a new cell.
**Answer: Dec 1–4 is reachable under the 4-agent cap.** Fit submitted Wed 11-25 to Thu 11-26, results by Fri 11-27,
evaluated by Tue 12-1. That leaves ≈ 3 days of slack, enough for one failed attempt and a retry.

## Gates (all required, in order; H-11 unchanged)
| gate | content | owner | target |
|---|---|---|---|
| P0 | #39 / #42 / #43 merged (m3 is in) | manager | **done 11-16** (engine 8b7f89be) |
| P1 | lever 1 = O1 (store check off the step path) merged, reviewed, same bits | builder 7 | Wed 11-18 |
| P2 | WP2 #13 merged, then D-31 (cond_cum on demand + scan table) | WP2 | Wed 11-18 / Fri 11-20 |
| P3 | lever 2 = K1 (bounded scoring) merged, same bits | builder 6 | Fri 11-20 |
| P4 | **T5 end-to-end at 10⁵** passes on NOTS (all stages via the driver; tail and LS0 seconds recorded) | builder 7 (O2 lean + O5), manager submits | Sat 11-21 – Mon 11-23 |
| P5 | WP3 StartView merged; `--plan-only` includes the island plan (#39 MAJOR); the driver re-sized from the printed real-table plan (island, calibrate **and merge** memory, PR45 INFO-3) | WP3, manager | Mon 11-23 |
| P6 | lever 3 = K3 (Gram rows) merged, same bits | builder 6 | Mon 11-23 |
| P7 | **H-11 measurement: the 10⁶ calibration pilot** on SPR with the production setup (levers 1–3 + m3), pre-announced | builder 7 command, manager submits | Tue 11-24 |
| P8 | offer floor O6 merged (D-29 contract: WP4 answer + WP1 INTERFACES line) | builder 7, WP1 | Wed 11-25 |
| P9 | re-size from P7's MEASURED numbers: per-fit central ≤ 1,188 core-h and the campaign total ≤ 28.3k (else ranked cuts) → **HQ GO** for the fit | manager → HQ | Wed 11-25 |
| P10 | the fit (setup → calibrate → 16 islands → merge/tail/LS0 → eval: selection + predictive d_H) | manager | submit Wed 11-25 to Thu 11-26 |
If any of P1–P8 fails, the fit waits. Nothing in H-11 is relaxed.

## NOTS core-h
| item | expected | ceiling | authority |
|---|---|---|---|
| T5 at 10⁵ (P4) | ≈ 200 | the driver's printed worst case (pre-announced) | already in the plan (MANIFEST_CELLS T5 row) |
| 10⁶ calibration pilot (P7) | 27–50 | ≈ 100 | standing authority, pre-announced (H-11) |
| **per 1M fit attempt** (P10) | **≈ 770–860** with levers 1–3 + m3 + floor (R1 bracket 700–1,000); 1,000–1,100 without the floor | manifest 1,188 per fit; HQ is told before submission if the driver's worst case (Σ CPUs × limits) is > 1.5 × the quote (PROTOCOL v1.2) | **HQ GO (P9)** |
| retry (if attempt 1 fails) | same as one attempt | — | HQ told; retries above one need a new GO |
Budget effect: if the configuration is unchanged after the pilot, the fit counts as replicate 1 (pilot rule, Sol F7;
K2/K5/O3/O4 after it are same-bits changes, so they don't change it), so it costs 0 extra. Otherwise it costs one more fit,
≈ 0.8–1.1k (the manifest's r04 rule), and the total stays ≤ 28.3k with the floor (R1: 22.3–23.4k + 1.1k).

## Agent schedule under the cap (4 concurrent Claude agents; Codex reviews outside the cap, one per gate PR)
| window | slot 1 | slot 2 | slot 3 | slot 4 (rotating, short) |
|---|---|---|---|---|
| Mon 11-16 – Wed 11-18 | builder 6: K1 | builder 7: O1 → O2 | WP2: #13 → D-31 | WP4 D-29 answer (minutes) → WP1 contract v0.1.15 (D-29 + PR45 minors) |
| Thu 11-19 – Mon 11-23 | builder 6: K3 | builder 7: O5 (T5 + pilot commands) | WP3: StartView + `--plan-only` (takes WP2's slot) | Sonnet reviews of small diffs; WP2 if D-31 runs over |
| Tue 11-24 – Fri 11-27 | builder 6: K2 → K5 (main ladder) | builder 7: O6 → O3 → O4 | WP3: real-table memory + main ladder | free (fit monitoring is the manager's) |
Builders 6–7 started 11-16 16:15 CT inside the cap: WP1, WP4 and the architect are done; the architect and the
finished reviewers are settled. Gate reviews (#46, #13 re-check, O1, K1, K3, StartView, O6) go to Codex (one each, from
16:20 CT). Sonnet takes the small diffs.

## Why the main ladder and January are not delayed
- Every gate above is also on the main path (H-11, T5, levers, StartView, floor). The pilot only brings T5 and the
  calibration pilot forward, and pushes K2/K5 and O3/O4 (restart at scale) back by ≈ 3 days.
- The 10⁵ rung (H-8: mid-December) starts after T5, as planned. O4 (restart at scale) is needed for the long 10⁵/1M
  campaign fits, and it lands ≈ Nov 30.
- NOTS: one fit's island tasks hold ≈ 8 SPR nodes (2 × 64G islands per node) for ≈ 1 h. Owner priority holds, and the fit
  is submitted at a quiet time.

## Risks and what happens then
- **K1 or K3 slips by more than 3 days:** the fit lands Dec 4–7. HQ decides between reporting the calibration pilot + T5 as
  the 1M evidence on Dec 1–4 and waiting.
- **P7 measures above the R1 bracket (> 1.2k per fit):** no fit, HQ gets ranked cuts (H-11 (4)).
- **LS0/tail time at 10⁶ is unmeasured (G0 ran with LS0 off):** T5 and P7 record it, and the merge task's limit is set from that.
- **Queue wait for 16 × 96-CPU tasks:** submitted as one job array; the delay goes to the slack.
