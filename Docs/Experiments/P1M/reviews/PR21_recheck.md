# PR #21 re-check: WP3 slice 1, review fixes (`exp/P1M-wp3-island2` @ `afa7a0d7`)

Reviewer: Opus 5.5 (high), independent of the author. Date: 2026-11-16.
- First review: `PR21_review.md` (head `cd1a7e02`; 3 MAJOR, 10 MINOR).
- Fix diff: `cd1a7e02..afa7a0d7` (10 files, +287/−47).
- Contract: INTERFACES v0.1.7. Spec: ENGINEERING_SPEC §0-v3.
- Read-only: detached worktree under the tmp folder. Nothing was pushed or commented.

## Verdict: **MERGE**

- M1 and M2 are fixed. M3 is deferred to the CLI-wiring PR; the manager accepted this, and the PR description says so (with the
  test the CLI PR must carry).
- All 13 claimed minors are done.
- m1 is in fact closed by INTERFACES v0.1.7 (§5.1: `st_moves` T × 12, `rb_round` Hm × p).
- m5, m6b, m6d and m9 stay open. They are tracked in the PR description ("noted for the next slice"); m5 is also listed in #24.
- **No regression.**
  - The T3 hashes are unchanged: bit `44a15bfc6fb8d233`, class A `d2df149413596a19`. They are identical for PM/LM, threads 1–3,
    G ∈ {1, 7, 16, 48} and tiles 64–256.
  - Golden island vs `v3::Engine::run_island` passes (PM and LM).
  - 13,000 flip scores vs `v3::Scorer`: 0 mismatches.
- **Tests: 61 of 61 pass** (Owls).
- New findings: 0 CRITICAL, 0 MAJOR, 3 MINOR (n1–n3), 2 nits. None blocks the merge.

## Test run
- Machine and setup: Owls (Xeon Gold 6148, load ≈ 600 on 80 CPUs), gcc 11.5.0, `nice -n 19`, OMP 3.
- TMPDIR: `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-21-24`, removed after.
- Command: `tests/run_tests.sh --build-dir …/b2`.
- Result: **61 test cases, 0 failed, 0 check failures**, exit 0, 1 min 25 s. `git_commit` in the binary = `afa7a0d7…`.
- Lines from the new tests:
  - `numerical_failure_status_deterministic`: "initial draw, particle 4: numerical_failure: score failed after Cholesky,
    refactor and augmented QR …". The text is identical for bit and A, PM/LM, threads 1 and 3.
  - `numerical_failure_in_flip_deterministic`: "bridge stage 1, particle 1, position 211: Gibbs label 151: …". The text is
    identical across all 8 configurations.
  - `store_snapshots_released`: at most 3 kept runs alive, 0 after the island, 12 merges.
  - `flip_large_supports`: 1,200 flips at k = 25/40/99, 0 bit mismatches, class A ≤ 1.28e-15 relative.
  - `gibbs_cap_island` (K = 6): 223 Gibbs steps at the cap, PM = LM, I4 holds.

## The three MAJOR findings

### M1 (numerical failure aborts): **FIXED**
I traced every scorer call that can run inside an OpenMP region at `afa7a0d7`:

| path | handling |
|---|---|
| `build_support` deletions (`kernel.h:133-136`) | caught → `del_logm` NaN, `del_odds = ODDS_FAILED` (−1) |
| `eval8_add` fallback lanes (`kernel.h:249-256`) | caught per lane → odds −1 |
| `eval1` slow path (`kernel.h:276-279`) | caught → odds −1 |
| PM Gibbs (`island_impl.h:276`) | `o < 0` at a **consumed** position → `fail.record(i, …)`, the particle stops |
| PM U/N/I, canonical (`:281-294`) | `try` around the whole particle round → `fail.record(i, pos_cur, …)` |
| LM phase A (`:441-442`) | `oj < 0` counts as an event at its position (so a failed score is never skipped over) |
| LM walk (`:478-491`) | consumed failed Gibbs at `f` or a U/N/I throw → `etype = 3`, `e = q` (nothing consumed) |
| LM apply / canonical (`:536`) | caught → `etype = 3` |
| initial draws (`:772`) | caught → `fail.record` |

- After each region, `throw_if_failed()` rethrows outside it: once after every LM group and once after a PM round.
- **The choice of reason is deterministic and the same in PM and LM.** Particles are independent within a round, so:
  - PM records each particle's first consumed failure; the smallest particle index wins.
  - LM groups run in particle order, and every particle of a group runs to completion or failure. The first group with a
    failure therefore holds the round's smallest failing particle.
  - This is also core's serial rule: core runs particle 1's whole round first.
- Positions agree: the PM `pos` equals the LM `f`, or `gb.e` for a canonical failure.
- Scores of labels a particle does not consume are only flagged, never reported (spec §3 rule 2). Cap rows (lb NaN, ob 0) and
  failed rows (ob −1) cannot be confused.
- A failed island reports no store and no estimate (`island_impl.h:847`; GUARD-W in the file test).
- The HPM-so-far is the master ledger up to the previous step boundary: the failing round's thread ledgers are not merged.
  It is therefore the same in PM and LM.

### M2 (snapshots keep kept runs alive): **FIXED for the production kernel; the bound is "in practice", not strict (n3)**
- A worker releases its snapshot in three places:
  - in `flush()` (`store.h:146`);
  - at a phase-B tile start if a newer kept run was published (`island_impl.h:509`);
  - at every step boundary (`sync_ledgers`).
- The new `kept_live` counter counts every `Kept`. It reads 3 in the test island (12 merges), and 0 kept runs remain after
  the island.
- WP3_DESIGN §1.5 v0.1.1 now carries the corrected 10⁶ figure (≈ 7 GB compaction + one stale generation ≈ 9.4–9.8 GB).
- PR #24 adds `release_snapshots()` before every boundary compaction, which closes the remaining window for the deferred
  label-major path (see the PR #24 review).

### M3 (fingerprint does not bind the inputs): **DEFERRED, accepted**
- The PR description states the deferral, the manager's decision of 11-16, the planned fix (content hashes of the
  data/setup/calib files plus `require_binary_compatible(…, Restart)`) and the test.
- It also says no production checkpoint is written before that PR.
- Keep this on the CLI-wiring PR's checklist.

## The minors
| # | status | evidence |
|---|---|---|
| m1 | **closed by INTERFACES v0.1.7** | §5.1 l. 297 `st_moves` T × 12, l. 304 `rb_round` Hm × p |
| m2 | done | `island_file.cpp:41`: `st_inc`/`st_cum` only when completed; reader tolerates their absence |
| m3 | done | `v4::Error(Status::…)` everywhere; status 1 → `to_record` and `write_island_file` throw (no file, no record); test updated |
| m4a | done | directory `fsync` after `rename` (`island_impl.h:662-668`) |
| m4b | done | `<stem>.{a,b}.tmp.*` removed at load; tested (`.b.tmp.12345` gone) |
| m4c | done | checksum-valid but unparsable → `internal_error`, never a fresh start over partial state |
| m4d | done | `key_io` writes EventKey field by field |
| m6a | done | `flip_large_supports` |
| m6c | done | `gibbs_cap_island` |
| m6e | done | golden checks `xph`, `sub`, `seg`, `unit` |
| m7 | done | `TopStore::offer` flags NaN; `sync_ledgers` raises `internal_error` outside any region |
| m8a | done | I1 is linear (`find(ref(i)) == i`), allocation-free; `check_store` option |
| m8b | done | store vectors moved into the result; `return std::move(res)` |
| m10 | done | `island.h` comments fixed; `stop_after_step` without `ckpt_path` → `invalid_input` |
| m5, m6b, m6d, m9 | open, tracked | PR description "Open: …" |

## New findings (all MINOR; none blocks the merge)

**n1. Exceptions other than `NumericalFailure` still terminate the process inside OpenMP regions.**
- Where: every `try` in `island_impl.h` (`:281-294`, `:478-491`, `:536`, `:772`) and `kernel.h`.
- Evidence: these handlers catch only `v4::NumericalFailure`. A `std::bad_alloc` thrown in a region still calls
  `std::terminate`. So does a `v4::Error` thrown by `slot_of` / `address_key` on overflow.
- Impact:
  - Overflow is unreachable at the planned sizes, so that case is theoretical.
  - `bad_alloc` is the case that matters: at 10⁶ it is the failure mode that the `--mem-budget` admission (#24) is meant to
    turn into `resource_limit`, and today it aborts instead.
- Fix: store any `std::exception` thrown in a region in `FailSlot` (`internal` = true for non-numerical ones, or map
  `bad_alloc` to `resource_limit`), then rethrow after the region.

**n2. The M1 tests always fail at particle 1, so they do not exercise the deterministic choice.**
- Where: `numerical_failure_*` in `tests/test_island.cpp`.
- Evidence: every particle hits a bad column, so particle 1 in group 0 always fails first.
- Not exercised:
  - the cross-group rule (the smallest failing particle sits in a later G-group);
  - a lower particle failing at a *later* position than a higher one.
- My reading says both cases are correct (see M1).
- Fix: add a case where only some particles can fail. For example, scale one column, and let only particles whose π₀ draw
  contains a chosen marker column reach it, or edit `logr` so the bad column is drawable only together with a marker. Then
  run it with G ∈ {1, 7, 16}.

**n3. The snapshot bound is not strict, for the particle-major kernel and the label-major walk.**
- Where: `store.h:115-118` (`refresh`), `island_impl.h` PM round / LM walk.
- Evidence: a worker that makes no offer above τ and does not flush keeps its snapshot while other workers' flushes trigger
  compactions.
  - In PM this lasts a whole particle-round (m ≈ p positions).
  - In the LM walk it lasts until the next phase-B tile.
  - Each worker holds at most one generation, but several workers can hold *different* stale ones. WP3_DESIGN §1.5 says
    "in practice ≤ 3".
- Impact: small. PM is ≤ 10⁴ by D-21, and #24's deferred mode compacts only at boundaries after `release_snapshots()`.
  The in-pass serial fallback is the exception (see the PR #24 review).
- Fix: none needed for production. State the bound as "≤ 2 + stale generations held across in-pass compactions" in §1.5.

Nits:
- `kept_live_max` is a process-wide static that `run_island` never resets. In the benchmark's thread sweeps, the per-island
  value printed is the process maximum.
- The m4a directory derivation turns `"/name"` into `"."` instead of `"/"`. This is an edge case only.

## Discipline
- All changed files are under `Scripts/SMC_BVS/engine_v4/`, and `core/` is untouched.
- No hard-coded paths, no large files.
- PR description: test machine and numbers are labelled, and the open minors are listed.
