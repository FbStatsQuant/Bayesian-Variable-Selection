# LOWP pilot revision 7d — independent Sol review

Reviewer: Sol 6.1 for Felipe. Date: 2026-10-30 UTC. Scope: D44 B1–B3 only; no SSH, NOTS access, or submission. Reviewed files were read only. New evidence and test fixtures are under `<PC_TEMP_PATH>`.

**Overall pilot verdict: READY WITH MINOR FIXES.** The cross-platform numeric check and sealed-byte checks are sound, and the ordinary never-locked unlock and in-place cleanup cases work. Three small fixes remain: compare array names exactly, establish unique/exhaustive checksum-list coverage, and preserve the interpretation of relative cleanup environment paths. Apply these before declaring the revised bundle unconditionally READY for OPS restaging; no re-seal or frozen-core change is needed.

| Fix | Verdict | Reason |
|---|---|---|
| B1: P0a regeneration check | **PARTIAL** | D44 numeric and sealed-byte checks work, but a regenerated pilot X name change can PASS. |
| B2: never-locked unlock | **PARTIAL** | Correct for the generated staging list and normal failure paths; a malformed 1,260-line list can omit a changed truth file and still verify. |
| B3: cleanup from inside deleted tree | **PARTIAL** | Memory re-exec fixes the original case with absolute/default paths; unconditional `cd /` changes relative-path and dry-run behavior. |

## Findings

### R7D-1 — Low: regenerated array names are not all checked exactly

Location: `code/lowp/R/lowp_verify_nots.R:45` and `:131`.

The numeric comparator checks lengths/dimensions and drops names during double conversion. The pilot exact check compares X/Y dimensions and Y column names, but not X column names or all dimnames. I wrapped the generator in a test only and assigned `changed_1`, ..., `changed_30` as X column names for `p0030_S4_r050`, leaving every numeric value, seed, foldid, sealed file, and manifest unchanged. The full verifier still reported **PASS (exit 0), 0 failed checks**, with all maxima zero. See `name_checks.R`, `names.log/.rc`, and `out_X_colnames/NOTS_REGEN_REPORT.md`. The old whole-record `identical()` comparison would reject this metadata difference.

This does not alter fit-consumed sealed bytes, but it falls short of the explicitly requested exact names check. Concrete fix: require `identical(dimnames(regen), dimnames(sealed))` for both X and Y, and exact `names()` for vector arrays where applicable, alongside the current shape/finite/numeric comparisons. Add a name-only mutation test expected to fail.

### R7D-2 — Low: checksum line count does not prove all truth files were verified

Location: `code/lowp/pilot/truth_wave.sh:39`–`41`.

The fallback selects truth checksum lines and requires `nlist == 1260`, but neither rejects duplicate paths nor compares the listed path set with the files present. In a copy of the supplied test fixture, I replaced the checksum line for `truth/p0020/f7.rds` with a second valid line for another truth file, then changed `f7.rds`. Both tree counts remained correct; the list still contained 1,260 selected lines, covering only 1,259 distinct files. Unlock returned **0**, `staged_equal(1260)`, and `WAVE_UNLOCK_VERIFIED` while the omitted file was changed. See `extra_duplicate_omits_tamper.log` and `.rc` in the evidence folder.

This requires a malformed staging list; `stage_local.sh` itself emits a unique list, and an altered file against the intact list is correctly rejected. It is a coverage gap in the fallback's claim to verify every file, rather than a failure of the normal staging path.

Concrete fix: normalize the optional `*` and leading `./` for comparison, reject duplicate paths, and require exact equality between the selected path set and a fresh enumeration of both truth trees (1,200 production + 60 dev) before running `sha256sum -c`. Preserve the original checksum lines for checksum validation. Add an omitted-file/duplicate-line negative test.

### R7D-3 — Low: `cd /` changes relative environment paths, including dry runs

Location: `code/lowp/pilot/cleanup_pilot.sh:21`–`29`.

The re-exec changes directory before reading `NC_HOME_ROOT`, `NC_SCR_ROOT`, `GUARD`, `SQUEUE`, and `SACCT`; line 24 also changes directory during a dry run. Relative root overrides that previously worked are consequently interpreted relative to `/`. Reproduction from a temporary fixture root with `NC_HOME_ROOT=home/New_Campaign` and `NC_SCR_ROOT=scr/New_Campaign`: the revision-6 script's dry run exits **0** and lists the expected targets, whereas 7d exits **4**, `REFUSED: cannot canonicalise home/New_Campaign`. See `relative_old.log/.rc` and `relative_new.log/.rc`. Relative override paths containing `/` for the guard or scheduler commands are affected by the same change.

Concrete fix: retain the original working directory, resolve relative roots and path-valued overrides against it before changing directory, export those resolved values through the memory re-exec, and leave bare scheduler command names subject to PATH lookup. Remove the unconditional `cd /` from the dry-run path. Add relative-root and relative-helper tests. The documented absolute defaults and OPS absolute-path invocation already work.

### R7D-4 — Low, optional test correction: the ulp helper does not cycle its perturbations

Location: `code/lowp/pilot/tests/test_p0a_tolerance.R:27`.

`((seq_along(x) * 7L) %% 7L) - 3L` is always `-3L`, although the comment says it cycles from -3 to +3. The test still injects nonzero rounding-scale noise and correctly exercises the intended PASS path; this does not invalidate the numeric portion of B1. Change it to `(seq_along(x) %% 7L) - 3L` (or another deterministic mixed-sign pattern) and rerun that test.

## B1 checks and gate semantics

- `lowp_verify_nots.R:75`–`85` calls the unchanged shared manifest validator. Schema, unique/full grid, canonical paths, active/beta design text, and all three seed fields remain exact. Regenerated `foldid` hashes remain exact for all 1,260 rows (line 99); each pilot copy's `foldid` and other metadata remain `identical()` (lines 135–136).
- All 1,260 truth files must be present. Their whole-file SHA-256 and sealed signal/eps array hashes are compared exactly with the manifests (lines 103–116). All six pilot input copies retain exact whole-file SHA-256, sealed X/Y array hashes, list field names/order, X/Y dimensions, Y column names, foldid, and metadata checks (lines 121–139). The tolerance does not substitute for any of those byte checks.
- `lowp_tol_cmp` (lines 43–50) rejects nonnumeric arrays, length/dimension differences, and non-finite values on either side. It checks each element against `1e-12 * max(1, abs(sealed))`, rather than using one large element to set a whole-array tolerance. Absolute and scaled maxima are saved in `NOTS_REGEN_MAXIMA.csv`. Array name checks are incomplete as described in R7D-1. The truth beta/signal comparisons are additional checks on the sealed truth records. Regenerated X/Y hashes outside the six pilot copies are informational; this gate does not claim to load unavailable production input files.
- Status selection (lines 141–153) cannot promote missing/malformed evidence to PASS: mismatches give 1; otherwise any incomplete prerequisite or fewer than six pilot copies gives 3. A CLI exception also gives 3 (lines 178–180). `s0_verify.sbatch` still records a failed unit and fails through the unchanged `pilot_finish`; fitting jobs remain dependent on its success. The unchanged summarizer recognizes the new PASS/MISMATCH/INCOMPLETE report header. The never-locked finalizer's success does not make an aborted pilot accepted: the missing wave lock and other original gates remain required.
- Reading all truth files at P0a respects the stated separation design: P0a uses `STUDY`, the staged study copy; P0c follows it, and the verified wave lock follows P0c. Fitting jobs use the separate truth-free `DEV_STUDY` and depend on the lock. No truth records are written into the fitting input tree or passed from this R process to fits.
- The existing 30-minute allocation is adequate on inspected evidence: this independent cold-cache full P0a baseline took 188 seconds; subsequent full checks took about 13–14 seconds. This is one P0a invocation per job, not the entire multi-case local suite. New-version NOTS/NFS elapsed time remains unmeasured because remote execution was excluded from this review.
- The actual reported NOTS magnitudes PASS the D44 numeric rule: eps relative differences at most `5.5e-16` imply scaled differences no larger than that; X absolute differences at most `1.3e-15` and Y at most `3.6e-15` are below the minimum absolute allowance `1e-12`. X's larger relative error near zero does not cause a failure. Independent comparator probes confirmed these cases. All exact checks must still pass; this is not a claim of a newly executed NOTS PASS.

## B2 and B3 mechanism review

Both missing pre-lock lists is the appropriate fallback discriminator for the pilot dependency graph: the truth-lock test writes both lists before its first lock, and the wave lock depends on that test succeeding. Exactly one list present remains a failure. Absence alone is not proof that a lock never occurred, but the fallback independently verifies open modes/counts and staging checksums; the R7D-2 coverage correction makes that proof exhaustive. With no PRE argument, the old optional hash-skipping behavior remains; the real finalizer always supplies PRE.

For `STUDY=<campaign>/runs/<PID>/study`, line 35 correctly derives `<campaign>` and finds `<campaign>/runs/<PID>/STAGED_SHA256.txt`. Prefix filtering accepts `find .` paths and an optional binary `*` marker without altering the lines sent to `sha256sum -c`. I independently exercised the binary-marker variant successfully. Original tests reject changed/missing files, missing staging lists, a single pre-lock list, and real pre/post-lock checksum mismatches. Production mode verification is still the unchanged `tl_verify_open` (755 directories, 444 files, 1,200 + 60 files). Windows tests stub those Linux permission helpers; I did not claim to rerun Linux/NFS permission tests.

The cleanup re-exec itself is correct for absolute/default paths: arguments are validated before re-exec, `$0` is read before `cd /`, `bash -c` receives an explicit `$0` and the original validated STAMP/`--yes`, exported environment values are inherited, and `CLEANUP_FROM_MEMORY=1` prevents recursion. There is no later script-relative source/reference using `$0`. `exec` closes the old script context, and the new shell is outside the removed tree. Local in-place cleanup and dry-run tests passed; the old script failed the analogous local in-place run. Actual NFS execution was outside scope. R7D-3 is the remaining path-interpretation regression.

## Checks run and evidence

Independent checks were launched detached, with commands, PIDs, UTC timestamps, logs, and exit-code files in the temp evidence folder. `launch_checks.py` and `run_extra.py` preserve the launch procedure. A copy of the existing `SEALED_OK` study was used: no new seal was produced and the original seal was not modified.

| Independent check | Inspected result |
|---|---|
| P0a tolerance suite, existing seal copied into new temp folder | **8/8**, rc 0; unmodified/ulp PASS; 1e-9 eps/X, fold swap, changed truth fail; missing truth INCOMPLETE |
| Never-locked unlock suite | **7/7**, rc 0 |
| Cleanup in-place suite | **3/3**, rc 0; old script's analogous run UNVERIFIED |
| GNU time suite | **37/37**, rc 0 |
| Independent tolerance/manifest probes | **18/18**, rc 0; boundaries, per-element scaling, NA/NaN/Inf, length/shape/type, seeds, short manifest, off-grid id, NOTS magnitudes |
| Name-only generator mutation, full P0a | False PASS reproduced, rc **0**, all numeric maxima 0; R7D-1 |
| Staging list with optional binary marker | Verified, rc 0 |
| Duplicate staging entry omitting an altered file | False VERIFIED reproduced, rc **0**; 1,260 lines / 1,259 unique paths; R7D-2 |
| Relative roots, old versus 7d dry run | Old rc **0**, new rc **4**; R7D-3 |
| Redundant independent full shell rerun | Stopped after **38** completed passing checks, **0** wrong/skipped; **not** counted as a full 54/54 pass |

The redundant broad rerun was stopped once the narrow review, focused suites, archive comparison, and required fix reproductions were complete. Its negative-suite step was not run. The complete saved 54/54 shell and 89/89 negative results below are inspected CONF-2b evidence, not claimed as new independent full reruns. `broad_rerun_stopped.json` records the cancellation, tracked process IDs, and partial coverage.

Inspected original CONF-2b evidence: `conformance/work/conf2b_runs/pilot7d_20261030T0520Z/`, including DONE, all six rc files (0), logs, P0a's 8/8, unlock 7/7, cleanup 3/3, shell 54/54, GNU time 37/37, and negative 89/89. I also read D44, the OPS failure report and recovery diagnostic, and compared the frozen code and archived pre-7d source.

The archived pre-7d verifier has SHA-256 `866ab494e877c09694868fab746d31e9cbda7e804e734dc6df843d6c79d3819a`, matching the ledger prefix. Against the OPS archive, 105 existing source files are byte-identical; only the seven stated production/documentation files differ. In particular, the generator, submission graph, staging logic, summarizer, shared timing/gate helpers, truth permission helpers, and recovery code are unchanged. See `archive_comparison.json`.

## Frozen tree and write audit

`code/core/v2_2_1.SHA256SUMS` SHA-256: **`d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1`** — exact required value. **27/27 files verify; no unlisted files.** Evidence: `frozen_check.json`.

Final source check at 2026-10-30T06:01:22.464966+00:00: all **79/79** snapshotted LOWP R/pilot and frozen-tree files are byte-identical to the start of this review. See `reviewed_before.json` and `source_unchanged_final.json`. Only this review file and scratch files in the new temp folder were intentionally written. No reviewed source was changed; no remote connection or submission was made.
