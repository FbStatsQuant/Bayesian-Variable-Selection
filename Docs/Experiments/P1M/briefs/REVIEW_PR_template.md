# Independent PR review brief (SMC - Engineering; PROTOCOL §2). Reviewer: Opus 5.5, high, independent of the author.

You review one pull request of the large-p engine (`Scripts/SMC_BVS/engine_v4/`) against its work-package brief, the
binding `INTERFACES.md` and `ENGINEERING_SPEC.md` §0-v2. Docs are at `/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/`.
Checkout: your own worktree (`git fetch origin && git checkout --detach origin/<branch>`). Read only: never push, comment
on GitHub or change any branch.

## Check
1. **Correctness.** Does every function claimed bit-identical to `Scripts/SMC_BVS/core/` really copy the arithmetic
   (order of operations, flags `-ffp-contract=off`, no reassociation)? Look for silent divergences, off-by-one errors,
   wrong index conventions (0- vs 1-based, original vs internal indices), integer overflow at p = 10⁶ (n·p, 40p + 1,
   2^B), uninitialised memory, races.
2. **Tests.** Build and run `engine_v4/tests/run_tests.sh` yourself on Owls (`nice -n 19`, ≤ 3 cores,
   `TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/<YYYYMMDD>-review-<PR>`; remove it after). Do the golden tests
   actually compare against `core/` outputs, and do they cover the edge cases (ties, empty model, k = K, routes,
   constant columns)?
3. **Contract.** Does the PR conform to INTERFACES.md (types, file formats, addressing, statuses)? List every deviation.
4. **Scale.** Will it work at p = 10⁶, n = 200 (memory, time, 32-bit limits)?
5. **Discipline.** Is anything written outside `engine_v4/`? Are there hard-coded paths, or files over 50 MB?

## Output
`Docs/Experiments/P1M/reviews/PR<N>_review.md`: a verdict (ACCEPT / ACCEPT-WITH-FIXES / REJECT) and numbered findings
graded CRITICAL / MAJOR / MINOR, each with file:line, the evidence and a suggested fix, plus the test run you did.
Final message: at most 10 lines (verdict, counts by grade, the top 3 findings). No sub-agents; no NOTS; no expensive
resources. Report big problems at once.
