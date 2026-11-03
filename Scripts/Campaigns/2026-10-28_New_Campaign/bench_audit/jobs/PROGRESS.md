# F3 v2 bundles — progress

- Done: inspected charter, decisions, PROD-H patterns, OPS guard/transfer helpers, original F3 scripts and manifest headers. No SSH and no fitting computation.
- Done: deterministic mapping (2,400 production, 24 dev + 2 production timing fits); shared launcher, guarded staging, frozen-tree and source-hash checks, GNU time/module/library gate, per-task timing and validation, timeout-only one-time doubled-wall retry, sizing/resource fill, accounting, reconciliation, and transfer manifests.
- Done: draft DEV and PROD JOB.md hand-offs with OPS commands, resource assumptions, acceptance, transfer and reviewed cleanup. Pilot sizing feeds four independent production cells.
- Done: round 3 aligns with final PROD-H; see BENCH_F3_PROD/PROD_H_ALIGNMENT.md. Production cells launch sequentially at %30; dev uses %13. All fb31 arrays count toward the 100-task guard. Freeze still requires editing just runner/freeze.json.
- Done: local synthetic tests: 16/16 production Python tests, 2/2 sizing tests, 2/2 guard refusal probes, six shell syntax checks, GNU time stubs, and RDS validator positive/negative controls; see TESTS.md. Mock scheduler tests exercise sequential terminal checks, uncertain acceptance, accounting, timeout selection and one-retry refusal.
- The high-p freeze now exists and its two hashes are filled in `BENCH_F3_PROD/runner/freeze.json`. Real-tree preparation and synthetic transfer checks pass. Independent review of review-1 fixes and actual NOTS environment checks are pending.
- **NOT READY FOR SUBMISSION:** review-1 fixes need independent review and OPS validation; production also requires an accepted remote pilot and measured sizing.
- Decisions for manager: use p1000 S4 and S6 r001 c050 for the two production timings; use all eight p1000/c050 pilot samples in its p95/mean; OPS explicitly repeats the launcher after each cell is proven terminal. The all-array queue check is a snapshot; OPS coordinates launches. A structurally valid failed row is counted and reported rather than labeled successful.
- Historical note: the pre-freeze validator once still contained ridge diagnostics. The frozen validator was updated before the final source freeze and is now called by the bundle wrapper. The estimated <2 physical-core-hour pilot and 75–90 physical-core-hour production costs are not measured here.

## Review 1 response (2026-10-30)

- Done: R1-1 replacement invokes the now-frozen v2 validator and adds expected-input/manifest binding, coefficient, pilot, OLS/RSS and selected-point KKT checks; the real runner fixture passes and 10/10 Sol corruptions plus 7 additional/earlier controls fail for asserted reasons.
- Done: R1-3 upload membership and resume changes; real-freeze preparation and repeated simulated verification pass. R1-4 retry fsync and client-error controls pass. Physical/billed cost wording updated.
- Done: null/singleton/whole-fit-failure frozen-runner saved-record coverage: 3/3 positives and 6/6 rehashed corruptions. The all-NA CSV `k` type inference needed a wrapper normalization; the frozen validator still rejects the preserved original zero-runtime failure. See fixture README.
- Next: independent review, OPS execution of the actual task and full-run reconciliation on NOTS, and measured pilot sizing before production. No remote work was performed here.

## Review 2 fixes

- Done: bundle-only validator changes bind all three seeds to input/manifest/results, enforce the complete null contract, and reconstruct CV/EBIC selection, scores, candidate sets, weighted grid and selected occurrences using frozen helpers.
- Done: 14/14 saved R2 corruption controls, 3/3 failure-branch seed controls, all four positive fixtures, prior branch controls and earlier controls; Python 19/19 + 2/2. See `REVIEW2_FIXES.md`.
- Done: both JOB.md files document R2-4's zero-runtime quarantine/escalation rule.
- Next: narrow independent Sol check under D48; the bundles remain blocked pending that check. The OPS remote pilot and production sizing gates remain.
- 2026-10-30 (manager): Sol narrow check READY FOR OPS (DEV first). 2026-11-02: DEV run `20261030T1855Z_bench_f3v2_dev` done (26/26, OPS-4). HQ D64: PROD resources set to 30 min / 2 GiB all cells; authoritative ledgers rewritten (historical ones in `archive_ledgers/`). **BENCH_F3_PROD READY for OPS (resources set).** Details: `code/bench_v2/PROGRESS.md`, `TESTS.md`.
