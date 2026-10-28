# Thread B independent oracle

The method source is master Part I, SHA-256
`7d77dddb968135d86a6b6431a7a3e04e122eb0c09f5ec9a6a8329e9a20757b6e`,
supported by METHODOLOGY_v3, SHA-256
`93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c`.
No prototype code was used. B's original implementation and pre-A criteria
were created without inspecting A code or notes. See STATUS.md for the
current independence boundary, execution state and outstanding work.

`PASS_CRITERIA_v1.md` governs acceptance; `AMENDMENT_LOG.md` records changes
made before A inspection. Scoped criteria/review notes are supporting records,
not permission to weaken that document. No B-oracle self-test establishes an
A implementation pass. Phase 2 uses a frozen A handoff and a separate verdict.

## Modules

- `oracle_score.py`: stable preprocessing, original-column mapping, log m/BF,
  capped normalized prior, F, numerical routes and heuristic error estimate;
  exhaustive p<=20 posterior/evidence/HPM; independent arbitrary-precision
  observation-covariance reference.
- `oracle_start.py`: exact complete-linkage tie/leaf/cut/packing rules,
  cut_group predicate, block log tables, size-profile convolution,
  normalized pi0, backward sampler and full-enumeration reference.
- `oracle_moves.py`: exhaustive elementary transition matrices and exact
  uniform-permutation round average, plus within-round conditional recordings.
- `oracle_semantics.py`: strict all-scored HPM, informational near ties,
  local scan/certification, primary PIPs, pip05, flags and scoped status checks.
- `oracle_protocol.py`: specified PRNG, naive inverse-CDF reference,
  pilot/grid endpoint rules, evidence arithmetic and operational budgets.

All public model IDs are **zero-based original columns**. Convert A's
one-based original IDs by subtracting one, never by compacting retained
positions. Arrays use retained order only where explicitly documented.

## Execution and evidence

Amendment 1 forbids NOTS and Slurm. Run on Owls from a new frozen snapshot
under B's own folder, one core, nice 19, thread counts one. The launch scripts
enforce load/memory checks and a 2 GiB virtual-memory limit. Do not launch a
second copy of an existing run. A worker PID, source hashes, exact command,
timestamps, versions, raw sampler draws and exit statuses accompany results.

The deterministic runner imports `test_<module>.run_tests()`. The primary
statistical battery uses 100000 iid draws in each of four fixed fixtures,
seeds 2026102201 through 2026102204, expected-mass pooling, four joint G-tests
and Holm familywise alpha=0.001. Pearson and marginal tests are diagnostic.
Reference and A sampler families must be separately labeled. An untestable
test never counts as passed; dependent terminal SMC particles are not iid
sampler draws.

Historical local results were explicitly authorized by the intervening SSH
moratorium before Amendment 1. Keep them intact. Subsequent runs use Owls.
The pipeline requires both independent code review and inspected execution
evidence before a core unit is marked verified. See individual review reports
for limits of each helper: a pure matrix or semantic adapter does not test
production orchestration, draw consumption or full fit-record completeness.

## A integration

After `A_build/HANDOFF_v1.md` exists and B's source/criteria are frozen,
verify A's frozen checksums, adapt its outputs without replacing its behavior
with oracle behavior, run the canaries, fill `CLAUSE_REVIEW_v1.md`, and rescore
the saved dev-smoke HPMs from their X/y. Each failure must retain a minimal
reproducer and expected/observed values in `VERDICT_v1.md`.

Truth and holdout are never inputs to this verifier's fitting tests. The
benchmark adapter mapping left open in Part I I.7 needs the managing lead's
explicit ruling; method statuses/flags must not be guessed from warnings.
