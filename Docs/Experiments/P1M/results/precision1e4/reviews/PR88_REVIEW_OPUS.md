# PR #88 REVIEW (Opus engine-diff reviewer, H-26 Q1): V-N mini-leg, `exp/P1M-VN` → `exp/P1M-engine`

**Decision: ACCEPT-WITH-FIXES. No fix is blocking.** The diff is minimal and is N plumbing only. I found no remaining N = 2,500 assumption in the V runtime (engine or driver) that could make N = 10⁴ or 5,000 silently wrong. At default N the outputs are bit-identical to F; I verified this myself on a fresh build of the PR head (§2). The fixes are a test gap, a stale comment, a planning-tool parser and doc lines. All of them can ride in the PR before the freeze tag without changing any `smcbvs4` object. The builder's cost sketch is about 5 % low and its batch count is wrong (F1). That matters for the HQ quote, not for this PR.

- **Reviewer:** one Opus child. PR head `c682dfc7` (DRAFT, OPEN, base `exp/P1M-engine`), F = `eefcbc4a`.
- **Scratch:** `~/SMC_Engineering_Department/tmp/20261119-pr88review/` only. Nothing was written under /tmp, nothing touched NOTS, nothing was pushed or commented, and no BNP file was touched.
- **The one shared tool:** the fit re-run calls the staging copy of `p1m_manifest.py fill`, read-only, exactly as the builder's `run_fit.sh` does. Nothing in staging was modified.

## 0. What I verified myself
| claim | result |
|---|---|
| diff scope (`git diff eefcbc4a c682dfc7`, 10 files, +164/−25) | **Minimal.** Engine changes:<br>• `calib_run.h:37-40,53-54`: constants `V_N_MIN`/`V_N_MAX`, and `frozen_N` gains `v_N` (defaulted).<br>• `calib_run.cpp:55,62,117-124,157,230`: reads `N` in V only and threads it to `N_final` / `cw.N`.<br>• `wp4_io.cpp:335-336`: the predicate is relaxed to [1, 2²⁴].<br>• A comment in `wp4_io.h:64`.<br>Tool: `plan_tables.cpp` gets `--N`. The rest is tests and docs. Nothing beyond the N plumbing |
| builder at `5d87ca53` vs head | `git diff 5d87ca53 c682dfc7` = docs + `test_wp4_io.cpp` only, so the builder's binaries are the PR's engine |
| builder's `F_src` | `diff -r` against `git archive eefcbc4a` (engine_v4): identical |
| object identity | **My own** build of `git archive c682dfc7` (same flags: Release, x86-64-v4, g++ 11.5.0) against the builder's F build: **35 of 37 objects byte-identical**. Only `calib_run.cpp.o` and `wp4_io.cpp.o` differ. The builder's 34/37 included `provenance.o`, which differs only because its branch build had a git commit while mine, from an archive, says "unknown". `island_*.o`, `island_cmd.o`, eval, post, setup and `main.o` are identical |
| default-N bit identity, end to end | **Re-verified** (§2):<br>(a) an independent no-drop-list re-compare of both builder fits;<br>(b) **a fresh re-run of AR r01 s1** with my build of the head: 567/567 sections identical to F, and 75/75 identical to the NOTS record;<br>(c) the T mode (law) check (calibrate + 4 islands) |
| unit tests (my build) | `v_mode_N_parameter` PASS (93.8 s) **with `V4_F_SMCBVS4` = the F build**: "default-N calib.bin vs F: sections identical", "default-N island vs F: sections identical". `wp4_io_calib_refusals` PASS. `calibrate_command_end_to_end` PASS. I did not re-run the full quick suite (the builder's log: cpp 208/0, driver 60, golden 568,269/0) |
| N-independence of calibration | p = 300 V fixture, seed 9: `calibrate --N 2500` vs `--N 10000` give **40/40 sections identical**, and meta differs **only in `N`** |
| mixed-N merge | N = 10⁴ calib + an N = 2,500 island, and the reverse: both **refused with exit 13**. A clean N = 10⁴ merge completes |

## 1. Findings
Severity: **M** = changes a number HQ will act on, or an operational risk; **L** = doc, test or tool; **I** = information.

| # | sev | file:line | issue | fix | blocking? |
|---|---|---|---|---|---|
| F1 | M | `VN_MINILEG_NOTE.md` §1 | **The 3.7× N-scaling divides an Owls N = 10⁴ island by a NOTS N = 2,500 island.** On the same machine (Owls, 4 threads, the same AR r01 s1 data and grid, T = 20):<br>• N = 2,500 islands take 59–79 s (4 runs, mean 70.7 s);<br>• N = 10⁴ islands take 270.5 / 274.4 s.<br>That is **3.85× (range 3.4–4.6×; Owls load noise is ±15 %)**, so effectively linear. Re-pricing factor 3.85/3.05 = **1.26** (not 1.21) gives **E ≈ 440, P90 ≈ 510** for the 12 fits, still under the 600 cap. The m = 4 class becomes E ≈ 52 against a soft line of 61.9 (P90 ≈ 79), so soft trips are likely unless the mini-leg commits its own class table.<br>**Batches:** "12 fits ≈ 2 batches" is wrong. 12 × (64 + 4) = 816 tasks, which at ≤ 150 per batch is **6 batches (3 waves × 2, as P1–P4)** | Quote with linear N scaling (factor 1.0 in `quote_model.py`). **Commit the mini-leg's class table before release**, so the H-26 Q3 soft/hard stops (1.5× / 2.5×) are pinned to it. Fix the batch count | no (it is the quote's) |
| F2 | L | `tests/test_island_cmd.cpp:716-717` | **The comment promises a check the test never makes.** It says "an island file of N = 2,500 cannot be merged under an N = 10⁴ calib.bin (and vice versa)", but `i25` is built and never merged under `cal`. I ran both directions: exit 13, refused by the `meta.inputs` (calib hash) guard before the N guard (`merge.h:274,323`) | Add the two `CHECK_EQ(sh(merge … --calib cal --islands <N10⁴ island>,i25 …), 13)` calls (and the reverse), or reword the comment | no |
| F3 | L | `include/v4/calib.h:8` | Stale comment: "NO tier escalation (N = 2,500, H = 512 always …)" | "N = the calibrate parameter (default 2,500), H = 512 always" | no |
| F4 | L | `tools/plan_tables.cpp:56` | `--N` is parsed with `std::stoi`:<br>• `2.5` → 2 and `1e4` → 1, silently;<br>• `abc` → an uncaught `std::invalid_argument` (abort).<br>This is not "refused as T's N". It is a planning tool, not in `smcbvs4`, and `--Rp`/`--q90` share the pattern | Parse with `stod`, require a whole number in [1, 2²⁴], else exit 2 | no |
| F5 | L | builder's `tools/vn_check.py` / `cross_check_V_copy.py:17` | The "identical() outside provenance" tool drops keys **by name anywhere in the tree** (`data`, `start`, `end`, `cost`, `inputs`, `mem_estimate`, …), so a scientific key with one of those names would be skipped. My no-drop re-compare (§2) shows nothing scientific is hidden in these 2 fits. **The only non-obvious non-provenance difference** is `fit.meta.mem_estimate.*` (±64 B; `sacct_upper` +320/+458 B). It comes from calib.bin's file size, which grows 64 B with the binary block's git-commit string, so it is provenance-derived. The `cost.columns` store counters (`flips`, `offers`, `dup_dropped`) also differ, but they do so between two F runs as well (§2) | For the NOTS / freeze identity record, use a no-drop compare (or list the drops), and name `mem_estimate` (provenance-derived) and `cost.columns.*` (run-to-run instrumentation) explicitly | no |
| F6 | L | `PREREG.md` §3.3 / §4 (N contrast), the mini-leg note | H = 512 does not depend on N (see §4). It is correct per D-26, but it is not stated where the N = 10⁴ result will be read | One sentence (see §4) | no |
| F7 | L | `tools/slurm/p1m_driver.py:95-120` (`DEFAULT_RES`) | Resources are set per rung and do not scale with N. Island time is ≈ linear in N, so the 10⁴ default (islands 0:15) is too short for N = 10⁴ (LEG_PLAN already overrides with 0:30 / 1:00). The 1M N = 5,000 self-check has the 2:00 default against ≈ 2× the N = 2,500 island time. Not silent: soft stop (exit 22), checkpoint resume, admission refusal (exit 11) | Size the 1M N = 5,000 plan's island time from 2× the measured 1M island (plan-level override) | no |
| F8 | I | `ERRORS_ALL_SITES.md` | `calib_run.cpp` line references are now 8 lines stale. The file says it is generated at `c8a30d…`, and the generic `whole_arg` refusal (line 198 of the doc) already covers `--N` | Regenerate at the freeze tag (optional) | no |

**Is the stale-assertion change correct?** Yes. `test_wp4_io.cpp` used to assert that `w.N = 50` is refused, which is exactly the B2 rule being removed. It now asserts that 50, 10⁴ and 2²⁴ are accepted and 0 and 2²⁴+1 refused, which pins both edges of the new predicate.

**Are the new tests non-vacuous?** Yes. Each assertion fails under F:
- F's calibrate ignores `--N`, so `I4.N == 10000` fails;
- F's `wp4_io.cpp:336` refuses the N = 10⁴ merge, so `CHECK_EQ(…, 0)` fails;
- F's calibrate accepts `--N 0`, so the exit-13 loop fails.

The test also checks:
- T mode is untouched (`N_final` = N0 and 2 tiers with `--N 10000`);
- the admission edge between the two plans (exit 0 vs 11);
- the merge-estimate delta, exactly.

One weakness: the F comparison runs only when `V4_F_SMCBVS4` is set (it is unset in the quick suite). It prints a line when skipped, which is acceptable because §2 covers it.

## 2. Bit identity at default N (task 4)
1. **The builder's two fits, re-compared by my own tool.** My comparator runs `info --meta 1 --record` on every container, compares every section (name, dtype, dims, bytes, sha256), and compares every flattened meta and sidecar key, with **no drop list**; then I classified each differing key by hand. Result for AR r01 s1 and ADJ-OPP r01 s1 (F vs branch): 46 files each, **567 sections each, 0 section differences**. 28,318 / 26,446 keys; every differing key is one of:
   - the binary block or git commit;
   - `content_sha256`, and input hashes of files that embed the binary block;
   - timings, RSS or wall times;
   - `mem_estimate` (F5);
   - the island store-work counters `meta.cost.columns.{flips, flips_per_step}`, plus `offers` and `dup_dropped` in ADJ-OPP. **These vary run to run within F itself.** I re-ran island 1 of AR r01 s1 twice with the F binary (same inputs, 4 threads): 0 section differences, and only `flips` / `flips_per_step` differ, at every step. They are thread-scheduling instrumentation, not science. The builder's tool drops them under `cost` (F5).

   Branch vs the **NOTS overlap record** of AR r01 s1:
   - 28 common files, 75 sections, 0 differences;
   - the other diffs: `island_isa` (x86-64-v4 vs sapphirerapids), the `island_bin` paths, and setup `accounted_peak_bytes` / `peak_rss_mb`.
2. **A fresh end-to-end re-run** (my build of `c682dfc7` from `git archive`, AR r01 s1, the builder's `run_fit.sh` with VN pointed at my scratch dir): **see §2a below.**
3. **T mode (law)**, on a generated AR dataset (n = 100, p = 300), with F and the branch:
   - calibrate, then islands 1–4: **144/144 sections identical**;
   - meta diffs are timings, provenance and three store-compaction counters (`cost.columns.offers / merges / dup_dropped`). A second F run against F differs in the same counters, so they are run-to-run noise.
   - The T merge refuses on both builds, because theory mode needs a known git commit (GUARD-W) and archive builds have none. T merge objects are therefore covered only by object identity (`wp4_io.o` changes only the `M_V` branch of `read_calib`) and by the golden suite.

**Are 2 fits enough? Yes.** At default N:
- object identity confines the runtime change to `calib_run.o` (the V argument read: `v_N = V_N` → the same `N_final` / `cw.N`) and `wp4_io.o` (the relaxed predicate takes the same branch at N = 2,500);
- `calib.bin` is the only channel by which N reaches island, merge and eval, and its sections **and full meta** match F in the 2 fits, the unit fixture and the T check.

No further fixture or unit-level identity test is needed. Keep the NOTS XB re-run (sapphirerapids / GCC 14.3 side) as planned.

### 2a. Fresh re-run result
Setup → calibrate → 16 islands → merge → eval → post. Owls, nice 19, 4 threads, 08:03–08:31. Run dir `~/SMC_Engineering_Department/tmp/20261119-pr88review/runs/rv/4-AR-n200-r01-V-s1`.
- **vs the builder's F run:** 46 files, **567/567 sections identical**, 28,318 keys. Every differing key is provenance, timing or RSS, `mem_estimate`, `offer_floor_calib` (the hash of the unit's own calib.bin, which embeds the binary block), or the F-nondeterministic `flips` counters.
- **vs the NOTS overlap record** (`records/overlap1e4/W0/4-AR-n200-r01-V-s1`, sapphirerapids): 28 common files (fit, eval, law, data and all sidecars), **75/75 sections identical**. The other diffs are `island_isa` and setup `accounted_peak_bytes` / `peak_rss_mb`.
- **Conclusion: re-verified.** At default N the PR head gives F's bits, on Owls and against the NOTS record.

## 3. Remaining N = 2,500 assumptions (task 2) and the range check (task 3)
**Engine.** `git grep` for `V_N`, `2500`, `2,500`, `"N"` and `.N` at the head finds:
- `calib_run.h` (the constants and the default);
- `island_cmd.cpp:189`: the default of `island --plan-only` without files. Planning only; it takes `--N`;
- `island.h:52`: the `IslandConfig` default, always overwritten from calib.bin (`island_cmd.cpp:250`);
- the `calib.h:8` comment (F3);
- the benchmark scripts' explicit N = 2,500 arguments.

Every consumer that does reach N reads it from calib.bin:
- island: `island_cmd.cpp:144,223,250`;
- merge: `wp4_io.cpp:1138` gives `ms.N`; with it, `merge.h:156` sizes the terminal supports, `:274,323,335` check island N and the support count, and `:486` sets the low-ESS flag at 0.5 N;
- the checkpoint: its header hash includes N, and N is checked on resume (`island_run.h:517,643`);
- the memory plan: `memory.h:95` (particles), and the test shows the admission edge moving with N;
- `rb` / PIP: `pip = rb_acc / ((double)N · Hm)`, with u128 fixed-point accumulators (`island_run.h:27-28,880`).

Eval and post do not read N. The store capacity is 40p + 1 (`island.h:67`) and the offer floor is fixed by calibration: both are independent of N by design, as in T.

**Driver.** No change is needed:
- `p1m_driver.py:365-367` defaults N to 2,500 and checks [1, 2²⁴];
- `:720` writes `params.N` into **every** manifest, including calibrate's. F's V calibrate ignored it and the island then refused (B2); the branch honours it, and existing V plans (all N = 2,500) are unchanged;
- a plan with N ≠ 2,500 run against an **F** calibrate still fails safe: the island refuses (exit 13), and F's merge refuses an F′ calib.bin with N ≠ 2,500;
- `p1m_cells.py:143-152,300,315` are planning filters (cost scales with N; the A3 / ablation pairings deliberately select N = 2,500).

**Silent-failure hunt (N = 10⁴ / 5,000).** Nothing found:
- **RNG:** N is in no key field. The particle index is a full 32-bit counter word (`rng.h:70`), and slot indices do not involve N (`SK_RESAMPLE` index 0; order draws are indexed by label).
- **Integers:** no `int` products in N (the only one is in double).
- **Buffers:** no buffer is sized by the constant.
- **Merge weights:** equal-weight over islands; the N checks are exact.

**The range [1, 2²⁴] is safe** and equal to T's island N range (`island_cmd.cpp:144,189,223`).
- **Memory:** at 2²⁴ the particle arrays are ≈ 3 GB, but admission refuses deterministically.
- **Floor:** N = 1 is degenerate but harmless (the low-ESS flag). Keep it, for parity with T, as HQ asked.

**Refusal parity:** it holds. The same rule ("a whole number in [1, 2²⁴]", via `whole_arg`, the same semantics as the island's `whole`), the same exit 13 (`invalid_input`), no calib.bin written, and an explicit `--N` that conflicts with the manifest is refused (as for seed / I_max / refine_m). Two remarks:
- the message wording differs (`calibrate: --N must be a whole number in [1, 16777216]`);
- T's calibrate still ignores `--N`, unchanged from F, as HQ requires; T's refusal happens at the island.

## 4. H = 512 independent of N (task 5): **OK as is; document it**
- D-26 fixes "N = 2,500 and H = 512 always" for V.
- ENGINEERING_SPEC §0-v2.2 row 1 lists "fixed N **per island** … (N = 10⁴ arm in the precision study; one 1M doubling fit)". Row 6 is calibration, and calibration is studied through m and I_max.
- The overlap hypothesis the arm tests is finite-**island**-N bias in log Ẑ, given the grid.
- So the spec means the island N, and the branch does exactly that: same seed gives an identical grid law (calib sections identical across N, meta differs only in `N`).
- This is a pure island-N contrast at a fixed calibration law. It does **not** test T's coupling, in which H0 = ⌈512 N0 / 2,500⌉ grows with N (`calib_run.h:21,32`).
- No larger change is warranted. Coupling H to N would make the N arm a joint (island + calibration) change, confounded with the m and I_max knobs.
- **Add to the mini-leg addendum / PREREG §3.3:** "the N = 10⁴ arm changes the final islands' N only; the calibration (H = 512, the grid rule) is the same law as at N = 2,500 (D-26); c_X is islands-only (R16), consistent with this".

## 5. Cost sketch (task 7)
- **The 12 held fits.** The arithmetic checks: 6 × 17.0 + 6 × 41.3 = 349.8, and 6 × 20.4 + 6 × 49.8 = 421. P90 ≈ 490 = 421 × (403/349).
  - With the same-machine ratio (F1): **E ≈ 440, P90 ≈ 510**, under the 600 cap. This is slightly conservative, since the factor is applied to whole fits while calibration (≈ 10 % at R′ = 64) does not scale.
  - Memory is a non-issue (island RSS 0.29 GB).
  - Time limits 0:30 / 1:00 stand (m = 4 island ≈ 13–14 min at 4 threads, at the 3.85× scaling).
  - **6 batches, not 2.**
- **The NOTS identity check, 5–7 core-h: confirmed.** It is the AR XB re-run (2.46 measured in A0), plus optionally ADJ-OPP (2.4), plus the 10⁵ freeze island (≈ 2): 4.5–6.9. The golden suite runs on Owls for free.

## 6. For the Sol 6.2 reviewer: the places most worth a second look
1. **`src/calib/calib_run.cpp:117-124`.** The manifest/explicit semantics of the V-only `N` read:
   - `args` already holds the manifest params (`cmd_args.h`), and `refuse_manifest_conflicts` compares JSON `dump()` strings;
   - T mode skips the block entirely.
   - Is there any path where V gets an N without `whole_arg` (e.g. `--plan-only`)?
2. **`src/merge/wp4_io.cpp:335-336`.** The only change in merge's objects. Confirm that nothing downstream of `read_calib` in V still assumes 2,500: `merge.h:156,274,323,335,486` and `wp4_io.cpp:1138`.
3. **Calibration independence of N, and what the precision N contrast can claim.** H = 512 and the grid law are fixed, so the contrast is island N only (§4). Also: could PREREG's ADOPT rule for N (r ≤ 1/√c_X with c ≈ 3.85) be met at all? 1/√3.85 = 0.51 on each of M1–M3 at R′ = 64. Recall R3's resolution figures.
4. **The identity argument by object files.** 35/37 objects are identical. Confirm that the two changed objects take the F path at N = 2,500 for both rules, coded and bounded (`frozen_N`, `settings_json`).
5. **Quote and stops (F1).** Same-machine linear scaling, and pinning the mini-leg's committed class table before H1–H3 (H-26 Q3/Q4).
