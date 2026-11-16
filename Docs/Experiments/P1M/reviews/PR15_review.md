# PR #15 review — WP1: INTERFACES v0.1.4 + v0.1.5 (D-18, x87 guard rows, binary_compatible, Sol F4a/b/c, F10, F11)

**Reviewer:** Opus 5.5 (reviewer of PRs #11 and #14), 2026-11-16.

**PR:** `5e3d5bf` → `exp/P1M-engine`.

**Scope:** `git diff origin/exp/P1M-engine...5e3d5bf` only.
- One commit, 20 files, +490 / −74, all inside `Scripts/SMC_BVS/engine_v4/`.
- The branch's `INTERFACES.md` (v0.1.5) is identical to the docs copy.
- Sol review sections used: `EXP_CP1_sol.md` §F4, §F10, §F11.
- Worked read-only in my own worktree. I made one temporary edit to a tracked file to test `-dirty` detection, then
  reverted it. Nothing was pushed or posted.

## Verdict: **MERGE**

The two points you asked me to check most carefully both hold:
- **The address domain is injective.** The field widths are checked, there is no overflow at p = 10⁶, and addresses are
  keyed by the destination particle.
- **The EventKey order equals the serial traversal** of `core/cpp/v3_core.cpp:408-476`. I checked it field by field
  against `v3_engine.h` and `v3_core.cpp` (details below).

All the listed items are present and tested.

I have six MINOR notes and two informational notes (N1–N8). None blocks the merge:
- N1 is a one-line wording fix to INTERFACES §4.2, needed before WP4 codes the inherited-HPM provenance.
- N5 is the pending NOTS re-run for the x87 rows, needed before the first NOTS job.

## Test run (MEASURED)

**Main run:**

| Item | Value |
|---|---|
| Machine | Owls, GCC 11.5.0, glibc 2.34 |
| Command | `TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261116-review-pr15 tests/run_tests.sh --full --threads 3` (nice 19, -j3), clean build |
| Result | **40 / 40 PASS**, 0 check failures, 47.5 s wall |
| New cases | `i5_multi_rebuild_calibration_and_final` (65,238 addresses, 42 units, all unique and serial-ordered); `binary_compatible_rules`; `cli_info_skips_self_test`; `fixtures_pinned_reference_matches_core` (20 core files pinned, commit `72785fe8…`); `pmath_binding_is_libm` (8 rows) |
| Golden counts | Unchanged: 1,608 / 773,998 / 5 / 231 |
| Fixtures | 74 files, all match `MANIFEST.json`; 13 MB |

**`-dirty` detection.** Running `cmake -P cmake/git_version.cmake` directly gives `5e3d5bf…` on the clean tree. After
appending one byte to a tracked `core/README.md`, it gives `5e3d5bf…-dirty`. I reverted the byte afterwards.

**Guard with FMA masked.** With `GLIBC_TUNABLES=…-AVX2,-FMA`, the 6 double rows fail and the x87 `expl` / `logl` rows
pass. That is expected, because x87 code is not selected by CPU features at load time (no ifunc). So the new rows detect
a different libm build, not a CPU variant.

**Start-up cost.** The self-test now takes **1.76 s** per command (`version`, measured twice), up from about 1.1 s,
because of the 2 extra rows. That is still negligible against tasks of several minutes to hours. `info` skips it.

## Point 1 — is the address domain injective?

**The packing is a bijection.**
- key = (seed 32 bits, role 4 | tier 2 | iter 6 | island 20); counter = (slot 32, position 32, particle 32, xph 8 |
  stage 24).
- `address_key` and `address_ctr` (`include/v4/rng.h`) throw outside these limits. `slot_of` throws for index ≥ 2²⁸.
- Distinct in-range addresses therefore give distinct Philox (key, counter) pairs.

**No field overflows at our scale:**

| Field | Our values | Limit |
|---|---|---|
| Order draws d | ≤ m − 2 ≈ 10⁶ + 16 (m = p + B + 2) | 2²⁸ |
| Block index b | < J ≤ p | 2²⁸ |
| Stage (bridge stages) | ~10³–10⁴ (T₀ = max(1000, ℓ²), × 4 per tier) | 2²⁴ |
| Particle (N ≤ a few 10⁴) | 1-based | 2³² |
| Position q | ≤ m | 2³² |
| Island (R′ = 16) | | 2²⁰ |
| Rebuild iterations | | 64 |
| Tiers (0 and 1) | | 4 |
| Polar attempts (role GEN) | now capped at 2²⁸ | 2²⁸ (cannot be reached in practice) |

**No two draws can share an address in the control flow:**
- **Initial draws:** `INIT` with position 0.
- **Resampling:** `RESAMPLE` at stage t, keyed by the destination particle i, one uniform each. This matches
  `core/v3_run.R`: "all N resample uniforms first", one per destination.
- **Round order:** position 0, `SK_ORDER` d.
- **Steps:** position q ≥ 1. Exactly one label per position per round.
  - G uses `ACCEPT`.
  - U and N_b use `MOVE_J`, `MOVE_L`, `ACCEPT`.
  - I uses the π₀ kinds, then `ACCEPT`. In one π₀ draw each block index appears at most once per kind.
- **Burn-in and measured rounds** have their own `xph`, so they cannot collide with bridge stages.
- **Calibration:** pilot = (`PILOT`, e, iter 0, island 0); diagnostics = (`DIAG`, e, k ≥ 1, r = 1–4); escalation changes
  e. **Final islands:** (`FINAL`, 0, 0, r). **Generated data:** role `GEN`, keyed by row, column and xph.

**Destination particle after resampling.** In v3, `population_round` sets `ev.particle = i + 1` on the resampled array
(`v3_engine.h:216`, after `Pn[i] = P[a[i]]` at `:325-327`). The address table keys `particle` the same way. Two
descendants of one parent therefore get distinct addresses, and no stream is inherited.

**Compat serial order.** `serial_key` puts all resampling uniforms before the bridge rounds within a stage. Within a
step it orders the kinds ORDER < PI0_SIZE < PI0_BLOCKSIZE (b decreasing) < PI0_SUBMODEL (b increasing) < MOVE_J <
MOVE_L < ACCEPT. That is exactly the variate order documented in `core/v3_run.R:24-37`, and the v3 step code agrees:
- Gibbs takes one uniform even when capped;
- U takes none at |S| ∈ {0, p}, otherwise j, l, accept;
- N takes none at empty S, takes j only when N(j)\S is empty, otherwise j, l, accept;
- I takes a complete π₀ draw, then accept (`v3_engine.h:111-191`);
- the round order takes m − 1 uniforms (`:193-198`).

**Test.** `tests/test_rng.cpp` `i5_multi_rebuild_calibration_and_final` drives this control flow: 2 tiers × (pilot +
3 rebuilds × 4 islands) + 16 final islands. It includes random self-loops, no-score N steps and variable-length π₀ draws.
UNIQUE mode passes over 65,238 addresses, and INCREASING mode passes per unit. It is a simulation of the control flow;
WP3 must also wrap its real sources (N7).

## Point 2 — does the EventKey order equal core's serial traversal?

**Segments** run TABLE 0 < INHERITED 1 < CALIB 2 < FINAL 3 < LOCAL 4 < LS0 5. This is the order of
`v3_core.cpp:408-476`: `ingest_tables` → inherited models → islands r = 1…R → final local search → LS0.

**Tables.** `ingest_tables` (`v3_core.cpp:372-386`) runs b = 0…J−1, then c ascending, skipping NaN codes (|U| > K). It
sets `ev.stage = b + 1`, `ev.position = c`, which gives the key (stage, position) = (b + 1, c) ✓. "Once per ledger that
ingests tables" matches v3: the calibration ledger at `:613` and the final ledger at `:408`.

**Islands:**
- Initial draws: particle i ascending.
- Each bridge stage: resampling (no events), then particles in order, each a full round, positions q = 1…m in draw
  order.
- Then burn-in rounds l, then measured rounds h.
- The key order (xph INIT < BRIDGE < BURN < MEASURED, stage, round, particle, position, sub) reproduces this, using v3's
  own stage and round values (`v3_engine.h:282-352`; calibration measured round = L + h at `:352`).
- Within a Gibbs step, v3 emits `held` before `eval(ME_GIBBS_FLIP)` (`:113-120`), which matches sub 0 then sub 1 ✓.

**Calibration.** For each tier e: pilot `run_island_s(0, …, PH_PILOT, 0)`, then its local search with `iter = 0`
(`v3_core.cpp:632-642`). Then for each rebuild k: diagnostic islands r = 1…4 with `iter = k`, then their local search
with `iter = k` (`:668-689`). The key (tier, iter, unit with `UNIT_LOCAL` = 0xFFFFFFFF last) gives the same order ✓.

**Local search.** The centre is emitted with stage 0, round 0, position 0. After that each scan has stage = scans + 1,
round = moves (non-decreasing) and position = ++pos (`v3_engine.h:381-390`). The key is monotone along the traversal ✓.

**Provenance.** The smallest key among a model's offered (fresh) events is its first offered event in the serial
traversal, which is v3's "became best at its first score" rule. Held events are not fresh, as in v3. Top-c content
remains order-free.

**I4 (F4c).** `i4_expected` (`include/v4/records.h`) matches v3's counters exactly:
- gibbs_held = `gibbs`;
- gibbs_flip = `gibbs − gibbs_cap`;
- uswap = `us_exec` (self-loops are excluded before `us_exec++`, `v3_engine.h:148-149`);
- nswap = `ns_exec − ns_noscore` (`:165-170`);
- indep = `in_exec`.

`gibbs_cap` is a v4-only counter, and the stage tables keep v3's columns.

**N1 (MINOR, wording) — inherited HPM.** §4.2 says "The inherited HPM keeps its calibration key" and "Provenance = the
smallest key among the winning model's events".
- **Problem:** the inherited HPM is also offered as an inherited model, with key (seg INHERITED = 1, particle i), and
  that key is smaller than its calibration key (seg CALIB = 2). A literal min-key rule therefore gives "inherited",
  whereas v3 replaces it with the calibration provenance (`v3_core.cpp:426-437`).
- **Fix:** state that the inherited HPM model's inherited offer **carries its calibration EventKey instead of**
  (INHERITED, i).
- **Consequences, both identical to v3 with that wording:**
  - if the same model is also a table model, TABLE (seg 0) still wins;
  - later final-island rescoring never wins, because CALIB < FINAL.

## Other items

| Item | Status | Evidence |
|---|---|---|
| D-18 | OK (contract) | INTERFACES §2 and §5.1 drop `cbs_*` / `sub_*` from `setup.bin`; recomputed on demand. The gate "draws identical with and without the stored sections" belongs to WP2 |
| x87 rows (PR14 F1) | OK | `pmath_info.cpp`: `expl` on [−11000, 0] (double-valued, as `log_sum_exp` passes them); `logl` on [1, 1001) (64-bit mantissas, covering the sum's range up to K + 1 ≤ 1001); 10 significant bytes hashed; included in `require_bit_libm()`; `v4_pmath_check` reports them against libquadmath |
| `binary_compatible()` (PR14 F2) | OK | `provenance.cpp`; rules MergeV / MergeTheory (clean, known, equal commit) / Restart (same executable sha256 and commit); test `binary_compatible_rules` (`tests/test_cli.cpp`) |
| `git_commit` with `-dirty` | OK | `cmake/git_version.cmake` runs at every build and is rewritten only on change; verified above |
| `info` skips the self-test (PR14 F3) | OK | `main.cpp:109`; test `cli_info_skips_self_test`; the stale "≈ 0.3 s" comment is corrected |
| F10 reference block | OK | `make_fixtures.R` writes `reference` (core commit, 20 per-file SHA-256, R, Rcpp, compiler, flags, libm) into `MANIFEST.json`; `fixtures_pinned_reference_matches_core` fails on drift |
| F11 neighbour bound | OK (contract) | INTERFACES §2: ≤ pB selections, ≤ 2pB entries, no per-column maximum, hubs tested; the threshold graph is a separate object (WP2) |

## Notes (MINOR unless marked)

- **N1 — inherited-HPM key wording.** See point 2. Fix before WP4 codes provenance.
- **N2 — drift test misses new core files.** The test compares only the files pinned when the fixtures were made. A
  newly added `core/` file would not be flagged. Also compare the file set, excluding `.cpp_cache`.
- **N3 — `-dirty` covers the whole repository.** `git diff-index HEAD --` looks at every tracked file. A tracked change
  outside the engine (another script, a tracked doc) therefore marks the build `-dirty` and blocks theory-mode merges.
  Failing closed is acceptable, but:
  - production binaries must be built from clean checkouts; or
  - limit the check to `Scripts/SMC_BVS/{engine_v4,core}`.

  Untracked files are ignored (an untracked header would go unnoticed).
- **N4 (nit) — `binary_compatible` edge cases.**
  - It throws instead of returning `{false, …}` when `libm.binding` is missing or is not a string.
  - Restart accepts two blocks whose executable sha256 are both `"unreadable"`. Treat `"unreadable"` as no identity.
- **N5 — the x87 rows have an Owls reference only.**
  - They fail closed, so if NOTS's x87 bits differ, every NOTS command refuses.
  - Run `v4_pmath_check` on NOTS (manager, one sequential ssh) before the first NOTS job, then update
    `PMATH_NOTS.md`.
- **N6 — some roles have no full address assignment.** Role POST (WP5) and role TEST (π₀ test draws, compat stream 200)
  have only role and xph assigned; particle, position and slot are unspecified. Add their rows to the §3 table before
  those draws are coded.
- **N7 (info) — the I5 test is a simulation.** WP3 must wrap its real sources in `CheckedSource` in its tests; the
  contract already says so.
- **N8 (info) — self-test cost.** It is now about 1.8 s per command (MEASURED), which is acceptable.

Temporary files: `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-pr15` was removed after the run.
