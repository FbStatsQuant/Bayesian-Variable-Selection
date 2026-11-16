# PR #13 (WP2 setup) — disposition of the independent review (`PR13_review.md`), Engineering manager, 2026-11-16

Verdict: ACCEPT-WITH-FIXES (0 CRITICAL, 2 MAJOR, 9 MINOR).
- Every bit-identity claim and T11 hold, including the reviewer's extra exact-tie tests and start-mode ties up to 1,728
  optima.
- No 32-bit overflow at 10⁶. The setup peak at 10⁶ is ≈ 18–25 GB (estimate).

| # | finding | disposition |
|---|---|---|
| M1 | conflicts with the base (CMakeLists.txt, run_tests.sh); the `/tmp` fallback | ADOPT: already ordered (rebase onto exp/P1M-engine; take main's files, re-add lines; `"$TMPDIR/…"` only) |
| M2 | setup.bin meta lacks the binary block (v0.1.2+) | ADOPT |
| m1 | T11 tie coverage thin | ADOPT: add the reviewer's exact-tie design as a unit case |
| m2 | the setup peak at 10⁶ is set by the table stage (≈ 17–25 GB); D-18 only removes sections from the file | ADOPT, with the D-18 implementation: never materialise codes_by_size/sub_cum; choose the table-store threshold without the 8·NG `tmp` (per-block pre-filter or a bounded heap); stream logm. Target setup peak ≤ 12 GB at 10⁶ (X + logr + tables' working set), confirmed by `--count-only` accounting. Until then the run plan states a large-memory setup task |
| m3 | the setup.bin file hash changes per run (timings in meta); the test clears them | ADOPT: consistent with v0.1.3, file identity = this run's content hash and data identity = the named data sections. The invariance test compares the named data sections (no clearing hack); timings stay in meta |
| m4 | setup's own libm guard + bypass flag, superseded by v0.1.3 | ADOPT: delete after the rebase |
| m5 | truncation is a height predicate (d = fl(1 − \|r\|) ≤ fl(1 − τ_n)); D-4 states it as an edge predicate | ADOPT: D-4 reworded (DECISIONS) to the height predicate, with ≥/> as the `strict` parameter (Theory no longer audits it after the scope change) |
| m6 | "packing by minimum index" untested | ADOPT: shape test recomputing retained clusters from the forest |
| m7 | exact mode has no memory guard | ADOPT: refuse `partition=exact` up front when 8p² exceeds the budget (resource_limit) |
| m8 | non-`Error` exceptions inside OpenMP regions terminate the process | ADOPT: catch inside the regions, rethrow after |
| m9 | small items | ADOPT as listed |

Merge rule: after WP2's rebase + D-18/D-19 + the F1 items (count-only, mem-budget, streamed tables, hub guard) + these
fixes, the same reviewer re-checks the diff; then merge.
