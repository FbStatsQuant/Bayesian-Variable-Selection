# Diff round R2 — disposition (lead), 2026-11-17

R2 (Opus-only, MANIFEST 7431d66d…): all 13 R1 findings RESOLVED; per-claim LIST-K, LIST-CODE, LIST-R ACCEPT; score 8.8;
gates=FAIL on one new F in CARD.md only (a proposal text for HQ, not a claim or its proof).

| finding | tag | decision | repair |
|---|---|---|---|
| R2-F-1 CARD Options A/B state the pathwise bounds without Theorem 6's data event | F | ACCEPT | Option A: "On Theorem 6's data event, `pip_list` (on either branch) is within …"; Option B: "on Theorem 6's data event (probability → 1), …" |
| R2-E-1 CARD A rate sentence lacks "(where printed)" | E | applied | added |
| R2-E-2 L3 (0.5) "after everything else" not in IMPL-LIST's text | E | applied | phrase dropped; replaced by the guard argument the seat gave (`v3_fit.R:121-122`, `:162`, `:79-87`) |
| R2-E-3 "Both PIP fields" ambiguous | E | applied | "`pip_list` (on either branch)" |
| R2-E-4 "log evidence of the posterior renormalised" | E | applied | "the log of the list's total unnormalised weight (the list evidence)" |
| R2-E-5 Option B "computed from the returned list" on the exact branch | E | applied | "`pip_list` (the list-renormalised PIPs; the exact PIPs on exact enumeration)" |

Council cap (PROTOCOL_v4 §5.8): R1 + one diff round are used. A targeted re-check of this repair (candidate round R3,
`reviews/MANIFEST_R3.txt`) needs HQ's order; requested through the manager.
