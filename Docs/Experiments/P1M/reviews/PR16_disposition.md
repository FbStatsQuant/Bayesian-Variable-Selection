# PR #16 (WP4 slice 1: calibration, merge, tail) — disposition of the independent review (`PR16_review.md`), 2026-11-16

Verdict: ACCEPT-WITH-FIXES (0 CRITICAL, 1 MAJOR, 7 MINOR, 3 INFO).
- The reviewer reproduced 974,641 golden checks and added 533,657 more on untested coded paths (no-fallback
  schedule_limit, preflight-blocked escalation, tier-1 start, ℓ = 0/1, bounded vs core tier 0): all identical.
- The harness reference equals core built the normal way (92,541 checks).
- D-2 and the refinement grid are confirmed; the tail is thread-invariant, ties included.

| # | finding | disposition |
|---|---|---|
| MAJOR | `merge_and_tail` keeps all R′ = 16 island ledgers in memory (≈ 45 GB at 10⁶, estimate) | **ADOPT, before slice 2**: the merge streams islands one at a time into one merged ledger (top-c of the union is order-free; the HPM with the smallest key is order-free; counters add). Peak = merged store (≈ 5.4 GB) + one island's store + buffers. A `--mem-budget` admission for merge (target ≤ 16 GB) |
| minor | the coded rule's local_limit trigger, the last_successful_construction fallback and the failure paths are not compared with core | ADOPT: add golden cases; reuse the reviewer's extra harness cases (533,657 checks) as committed tests |
| minor | inherited-HPM provenance by v3's after-the-fact relabel, not the v0.1.6 rule; inherited events use particle 0 instead of i; PR17's two provenance tests missing | ADOPT: implement the v0.1.6 rule directly (calibration EventCtx on the offer); particle index i; add the three-case provenance tests (table / inherited / neither) |
| other minors and INFO | as listed in the review | ADOPT as listed |
| D-26 (new, Theory PSMC-S0) | the bounded rule in V: no tier escalation; I_max ≤ ℓ required; construction failure installs the last good grid, else the pilot schedule; never "no output"; flag grid_fallback | ADOPT in slice 2, with a test per path |

Merge rule: WP4 pushes the fixes (incl. the streaming merge), then the same reviewer re-checks; merge; then slice 2 (file
I/O) builds on the streaming API.
