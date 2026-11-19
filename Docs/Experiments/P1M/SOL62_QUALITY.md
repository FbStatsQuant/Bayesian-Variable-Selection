# gpt-6.2-sol gate-review quality vs the 6.1 family (owner via HQ, 11-17)

One row per 6.2 gate review. Each point is BETTER / SAME / WORSE than 6.1, judged against the 6.1 Sol reviews in reviews/
(e.g. PR50, PR52, PR53, PR57). Bugs means real defects confirmed on re-check. FP means false positives and nitpicks
(BETTER = fewer). Brief means it checked what the brief asked and stayed in scope. Speed/cost means wall time and tokens.
**Escalation rule:** two WORSE in a row on substance (bugs or FP) → tell HQ at once. The daily report carries a one-line tally.

| date | PR | bugs | FP | brief | speed/cost | reason |
|---|---|---|---|---|---|---|
| 2026-11-17 | #68 list-PIP (v3 + v4, gate) | BETTER | SAME | BETTER | SAME | Found a real public-output defect the golden could not see (v4 mpm_list in internal 0-based indices + logZ_list name), the v3 compute-before-finish leak into peak RSS, and that the R order oracle passed under a reversed sum (shown by its own negative control); built the pre-change binary for a byte-level old/new check. No false positives seen; ≈ 1.5 h wall, like 6.1 gate reviews. Final message terse (≤ 6 lines) but the file is thorough. |
| 2026-11-19 | #88 V-N mini-leg (engine, post-freeze gate; score 7.0 ACCEPT-WITH-FIXES) | BETTER | BETTER | SAME | SAME | 5 findings, all genuine and adopted by HQ (bffe257c): 2 real validation defects the Opus review missed (M1 merge ESS ≤ N rejects valid equal-weight islands by float rounding; M2 driver silently resolves top-level N vs params.N mismatch) + 3 minor (m3 pre-cast range, m4 bare --N, m5 identity test skip→fail + baseline sha); 0 false positives; independently confirmed the default-N bit-identity expectation. Speed/cost not observed (HQ seat). |

**Tally:** 2 reviews; on substance (bugs, FP) BETTER 3 · SAME 1 · WORSE 0; no WORSE streak.
