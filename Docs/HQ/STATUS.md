# HQ status board (repo-based)

**State on 2026-11-03: the New Campaign's empirical phase is COMPLETE (HQ D94).**
- All runs are closed on NOTS, pulled and verified (OPS closed, D93).
- The final analyses are accepted.
- The old HQ stops after this GitHub refresh (D77): "the theory campaign is being executed elsewhere". No repo-based HQ exists yet.

| Field | Value |
|---|---|
| Sole writer (HQ) | old HQ (PC project), stopping per D77. A new HQ, if Felipe wants one, bootstraps from `Docs/HQ/BOOTSTRAP.md` |
| Pushed commits | `c4ef0dc` "Transfer" (first snapshot, 2026-11-02). The reviewed fixes and the post-campaign refresh are pending Felipe's commit and push (`Docs/PUSH_CHECKLIST.md`) |
| Watchdog | none bound to this repo; the old HQ disables its own at stop (D77) |
| Rehearsal (`BOOTSTRAP.md` §3) | not run |

## Results in one screen

Final reports:
- `Results/2026-10-28_New_Campaign/L_20261102/HEADLINE_L.md` and `EVIDENCE_L.md`;
- `Results/2026-10-28_New_Campaign/H2_20261102/HEADLINE_H.md` and `EVIDENCE_H.md`.

Run and NOTS record: `Scripts/Campaigns/2026-10-28_New_Campaign/ops/FINAL_NOTS_STATE.md`.

### Low p (n = 200, p ∈ {20, 30}, 2,400 cases; exact posterior by full enumeration)
Terra tie-outs PASS, Sol ACCEPT (D75, D94).

| Question | Answer |
|---|---|
| Is Ẑ accurate? | Yes. log Ẑ error RMSE 0.012; the 0.05·Ẑ lower bound covered Z in 100% of fits |
| Is the HPM accurate? | SMC HPM = exact HPM in 2,400/2,400 primary fits and 12,000/12,000 repeat fits. HPM = truth 92.3%. Every miss is a miss of the exact posterior itself; there are 0 search misses |
| Are the PIPs accurate? | Mean per-fit max \|PIP − exact\| is 0.0005 (RB) and 0.0020 (plain). MPM = exact MPM in 99.9% (RB) and 99.8% (plain) of fits |
| Seed stability | All 6 seeds give the same HPM in 100% of cases |

**Recovery, pooled /2,400:**

| Method | /2,400 |
|---|---|
| SSL | 2,251 |
| SMC-BVS HPM (= exact HPM) | 2,216 |
| SuSiE | 2,183 |
| Adaptive lasso | 2,066 |
| MCP | 2,061 |
| ABESS | 2,051 |
| Horseshoe | 2,028 |
| Lasso | 1,852 |
| Elastic net | 1,692 |

Disclosed, not audited (D94):
- SSL > exact HPM is organic (the exact posterior is our model's own, not an oracle).
- Lasso and EN are ≈ 0 under CV (as audited in D42).
- The horseshoe (`ci95`) drops at p = 30, c = 0.5.
- ABESS is RSS-optimal in 2,375/2,400 fits (D54.3).

### High p (n = 200, p ∈ {500, 1000}, 2,400 fits; BVS against the truth only, D22)
Terra tie-outs PASS, Sol ACCEPT WITH FIXES ×2, narrow F3 check ACCEPT (D78, D87).

- **Reproduction.** The v2.2.1 rerun reproduces the 2026-10-23 fits exactly (2,400/2,400, 11 fields).
- **Exact recovery /600, HPM** (p500 / p1000):

  | | p500 | p1000 |
  |---|---|---|
  | c = 1 | 559 | 560 |
  | c = 0.5 | 370 | 340 |

  The MPM rows (RB and plain) agree in 2,391/2,394 completed fits.
- **c = 0.5:** SMC-BVS is first or tied-first in 11 of 12 cells, ahead of the best benchmark (SSL) by 67 datasets at p500 and 85 at p1000.
- **c = 1:** SMC-BVS ranks 4th of 9, behind SuSiE, SSL and the horseshoe. It beats the adaptive lasso (rerun with the lasso pilot: 493 / 512 at c = 1) in 24/24 cells.
- **Disclosed:** 6 `resource_limit` stops counted as misses (P5 retry not run, D62); the lasso-family headline is `ebic1_K37` with CV as a sensitivity (D42); the EN α and aLasso `cv_min` last-grid-point disclosures.

### Theory evidence
Summarised in `Docs/THEORY_PRIORITIES.md` §5:
- the masked regime holds almost everywhere;
- **first discovery of the truth:**
  - at high p, it happens in the pilot SMC by Gibbs flips and swaps in the completed hits, and the final local search made no improving move;
  - at low p, every first truth score is in the pilot, mostly from initial draws or Gibbs flips. That does not rule out a later local-search role.
- **search misses:** 0 at low p (exact reference). At high p, 0 detected, but whether the truth was ever scored is unidentified for the 565 completed misses, and the T21 probability bound is silent there;
- the literal T37 premise fails in every audited case; the "toward" form has no counterexample (p ≤ 30, d = 1).
