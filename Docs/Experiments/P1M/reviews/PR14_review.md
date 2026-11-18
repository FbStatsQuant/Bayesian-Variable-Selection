# PR #14 review — WP1: INTERFACES v0.1.3 (identity rules, V4_CHECK_ADDRESSES, libm rule and self-test guard)

**Reviewer:** Opus 5.5 (the reviewer of PR #11), 2026-11-15.

**PR:** `exp/P1M-wp1-v013` @ `aacaf29` → `exp/P1M-engine`.

**Scope:** `git diff origin/exp/P1M-engine...origin/exp/P1M-wp1-v013` only.
- One commit, 15 files, +181 / −41, all inside `Scripts/SMC_BVS/engine_v4/`.
- INTERFACES v0.1.3 in the branch is identical to the docs copy.

**Method:** worked read-only in my own worktree; nothing pushed, nothing posted on GitHub.

## Verdict: **MERGE**

Everything asked for is present and correct:
- the identity rules (R1, as contract);
- the `V4_CHECK_ADDRESSES` option (R2);
- the test gaps (R3);
- the NaN guard;
- moving log1p/expm1 to class A.

I verified that no bit-form path can reach log1p or expm1, by symbols in the built binaries.

The six-row guard is sound for what it covers, and about 1 s of start-up is acceptable at our job sizes.

There are three MINOR follow-ups. None blocks the merge, but F1 should be done before the first NOTS bit-form run.

## Test run (MEASURED)

**Main run:**

| Item | Value |
|---|---|
| Machine | Owls, GCC 11.5.0, glibc 2.34 |
| Command | `TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261115-review-pr14 tests/run_tests.sh --full --threads 3` (nice 19, -j3), clean build |
| Result | **36 / 36 PASS**, 0 check failures; 42.3 s wall (was 28.6 s; the extra time is the self-test inside each CLI-level test) |
| New case | `format_malformed_entries_rejected` |
| Self-test inside the suite | `pmath_binding_is_libm`: all 6 rows ok |
| Golden counts | 1,608 / 773,998 / 5 prep cases, unchanged |

**Extra checks:**
- **Build with the option on.** `cmake -DV4_CHECK_ADDRESSES=ON` builds `smcbvs4` with no warnings, and
  `V4_CHECK_ADDRESSES=1` appears in `v4_bit`'s `flags.make`.
- **Guard with FMA masked.** With `GLIBC_TUNABLES=glibc.cpu.hwcaps=-AVX2,-FMA`, `gen` is refused (`invalid_input`) and the
  message names all 6 rows. The guard detects the variant from function results alone.

**Start-up cost**, from `/usr/bin/time` under nice 19 on a busy Owls:

| Command | Wall | RSS |
|---|---|---|
| `smcbvs4 version` (three runs) | 1.07 / 1.10 / 1.39 s | 35 MB |
| tiny `gen` | 1.12 s | — |
| `info` | 1.08 s | — |

`pmath.h` says the self-test takes "≈ 0.3 s". The measured cost is about 1 s, so that comment needs correcting.

## (1) R1: file identity vs data identity; binary consistency

**The contract text is correct and complete** (INTERFACES §5.1, lines 207–217). It names three identities and says they
are never mixed:
- **File identity is `content_sha256`, always.** This covers manifests, the merge's input validation (each island's
  `meta.inputs` against the manifest's data/setup/calib hashes) and restart.
- **Data identity across builds uses named sections only.** These are `X_cm` and `y` in raw files, and `Xs_cm`, `ys` and
  `kept` in data files. It is never used for setup, calib, island, fit or law files.
- **Cross-machine bit identity (T2)** uses the non-meta section hashes or the fit fingerprint.

**Binary consistency.** The merge refuses islands whose binary blocks differ in libm self-test, flags or, in theory
mode, git commit. A checkpoint restart refuses a different binary block. This matches what I asked for in the PR #11
re-check.

**There is no code yet.** The merge refusal and the restart refusal are contract rules only. `merge::run` and the island
checkpoint are still WP4 and WP3 stubs, and WP1 provides no helper to compare blocks (grep for `binary_compatible` /
`same_binary` finds nothing). So I can confirm the rule, but no implementation exists to confirm.

**F2 (MINOR) — one shared comparison rule, and a precise git commit.**
- Add `bool binary_compatible(const Json& a, const Json& b, Mode m)` to `provenance.h`, with a unit test, so that WP3
  and WP4 apply one identical rule.
- Note that "libm self-test" is stored as pass booleans only. Every job that ran has passed, so comparing that field is
  vacuous. That is acceptable, but the comparison should then be "both pass", with flags and git commit compared
  exactly.
- `V4_GIT_COMMIT` comes from `git rev-parse HEAD` at configure time (`CMakeLists.txt`). It does not see a dirty tree, and
  it goes stale after a commit without re-running cmake. For the theory-mode git-commit rule, use
  `git describe --always --dirty --abbrev=40`. Also make the merge refuse `-dirty` or `unknown` in theory mode.

## (2) R2 and R3

**R2 — FIXED.**
- The option is defined in `cmake/flags.cmake:11-14` (`option(V4_CHECK_ADDRESSES …)` → `V4_CHECK_ADDRESSES=1`).
- `include/v4/rng.h:126-130` gives `constexpr bool kCheckAddresses`.
- INTERFACES:106-107 says the same.
- The ON build was verified (above).
- No engine code reads `kCheckAddresses` yet; WP3 and WP4 will.

**R3 — FIXED.**
- `tests/test_format.cpp:45` `format_malformed_entries_rejected` covers two crafted cases. Every hash is recomputed in
  both, so only the range check can catch them:
  - an entry whose offset + length wraps around;
  - an entry pointing into the header.
- `tests/test_prep.cpp:128` checks the length of `_consts.f64` (4 values).

**Also fixed: NaN guard.** NaN values are refused with `internal_error` in `src/common/store.cpp:37` and
`src/common/ledger.cpp:95`.

## (3) log1p / expm1 unreachable from bit form; the six-row guard

### Source grep
- Outside `pmath.h:23-24` (`pm::machine::log1p`, `expm1`), the only references are in two places:
  - `tools/pmath_check.cpp:30-31`, the measurement tool;
  - `tests/test_pmath.cpp:15`, a binding identity check.
- There are no `std::` transcendental calls in `src/` or `include/` outside `pmath.h`.

### Build-graph grep (`nm` on the built objects)
- `libv4_bit.a`, `libv4_a.a`, `smcbvs4` and `v4_tests` reference **no** log1p or expm1 symbol.
- Only `v4_pmath_check` does (4 references).
- `libv4_bit.a` imports only these libm functions:
  - `log` (`data.cpp`, `gen.cpp`, `score.cpp`, `pmath_info.cpp`);
  - `exp` (`pmath_info.cpp`);
  - `lgamma` (`data.cpp`, `pmath_info.cpp`);
  - `logl` and `expl` (`data.cpp`, from `log_sum_exp`).

### Consistent with `core/`
- `core/` calls log1p/expm1 only inside `log_add` (`v3_util.h:71`) and `log1mexp_v3` (`:86`). Neither has a caller.
- `plogis_log` (`v3_engine.h:126`, which WP3 will copy) uses `exp` only.
- `lgamma` is only ever called with arguments ≥ 0.01: a0, n/2 + a0, and k + 1, n + 1 inside `lchoose_d`. glibc's
  negative-argument path (`lgamma_neg`, which uses log1p internally) is therefore never reached.

### Is the guard sound?
**Yes, as a detector of a different libm variant or build.**
- It hashes `f(x)` over the same 2·10⁶-argument rows that were measured equal on Owls and NOTS, and compares against
  reference hashes. It keys on results, so it accepts NOTS although the libm file differs, which the old file-hash idea
  would not have done.
- The sample size is justified. Between the FMA and SSE2 variants, the wide `log` row differs in only a handful of
  arguments (3 vs 5 not correctly rounded). Detection rests on `log_near1` (about 2,600 differences), `exp` and `lgamma`
  (about 20–30%).
- Shrinking N to save start-up time would weaken the `log` evidence, so keep 2·10⁶.
- The rows cover the engine's argument ranges:
  - `lgamma_int` reaches 3·10⁶ (2p at 10⁶);
  - `exp` covers [−745, 700];
  - `log` covers [1e-300, 1e12].
- The arguments are themselves generated with `pm::exp` and `pm::log`. A different libm therefore changes the arguments
  too, and the guard still fails closed.

**F1 (MINOR) — the guard does not cover x87 `logl` / `expl`.**
- INTERFACES §6 (line 276) lists `pm::logl` and `pm::expl` as bit-form functions.
- They feed `log_sum_exp`, which gives `logWK`, then `logprior[k]`, then `F`. `F` drives the HPM, the stores and every
  ordering.
- Neither `PMATH_NOTS.md` nor the self-test measures them. G0 on NOTS compared `logm` only, which does not involve
  `logprior`.
- They are x87 assembly in glibc and probably identical on both machines, but that is unmeasured.
- **Fix:** add `logl` and `expl` rows to `check_arguments` and `self_test`:
  - over the `log_sum_exp` ranges: `expl` on [−745, 0] in long double, `logl` on [1, K + 1];
  - hash the 80-bit results, or the results rounded to double.
- Taking the reference hash from Owls fails closed on NOTS if the bits differ, so a NOTS mismatch would show up at once.
- Do this before the first NOTS bit-form run. A one-line `v4_pmath_check` re-run on NOTS (manager, one sequential ssh)
  would also settle it.

### Start-up cost
- Measured about 1.0–1.4 s wall and 35 MB per command, for 12·10⁶ libm calls plus about 100 MB of SHA-256.
- **Acceptable:**
  - island and calibration tasks run against a 7,200 s budget, so 1 s is about 0.015%;
  - `gen`, `prep`, `setup` and `merge` take tens of seconds or more at p ≥ 10⁵;
  - the cost is paid once per process (a static cache).
- **Small costs:**
  - The test suite slows down (+14 s here).
  - `info` and `version` also pay, because `binary_block()` runs the self-test from `main.cpp:109` for every command,
    although only the guard needs it for the other commands.
- **F3 (MINOR):**
  - Let `info` skip the self-test, or show `self_test: "not run"` in its block.
  - Correct the "≈ 0.3 s" comment in `pmath.h` and `provenance.h` to the measured ~1 s.
  - Do not shrink N (see above).

## Findings

| # | Grade | Finding | Fix |
|---|---|---|---|
| F1 | MINOR | The bit-libm guard does not cover x87 `logl`/`expl` (`log_sum_exp` → `logWK` → `logprior` → F) | Add two rows; Owls reference (fails closed); before the first NOTS bit-form run |
| F2 | MINOR | The binary-consistency rule is contract-only, with no shared helper; the git commit misses dirty trees and is stale after a commit | Add `binary_compatible()` plus a test in WP1; use `git describe --dirty`; refuse dirty or unknown commits in theory mode |
| F3 | MINOR | The self-test runs for `info`/`version` too; the comment says 0.3 s but ~1 s is measured | Skip it for `info`; fix the comment |

Temporary files: `/home/fb31/SMC_Engineering_Department/tmp/20261115-review-pr14` was removed after the run.
