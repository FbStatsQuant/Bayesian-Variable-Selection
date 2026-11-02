# Pilot revision 7d: disposition of Sol's narrow check (CONF-2b manager, 2026-10-30)

Review: `PILOT7D_SOL.md`. Verdict: READY WITH MINOR FIXES. Every finding was rated Low. The frozen tree verifies 27/27.

All four findings are accepted and fixed:

| # | Fix | Test |
|---|---|---|
| R7D-1 | `code/lowp/R/lowp_verify_nots.R` `lowp_tol_cmp`: `names()` and `dimnames()` of every compared array must be `identical()` (metadata is exact; only floating-point values get the tolerance). | `tests/test_p0a_tolerance.R`, new case N: regenerated X column names changed with values identical gives MISMATCH ("names / dimnames differ") |
| R7D-2 | `code/lowp/pilot/truth_wave.sh`, never-locked fallback: the normalised path set of the selected staging lines must have no duplicate and must equal a fresh enumeration of both truth trees before `sha256sum -c` runs on the original lines. | `tests/test_unlock_never_locked.sh`: a duplicate line hiding an omitted, changed file FAILS; an unlisted file plus an absent listed file (counts unchanged) FAILS; after restoring, it VERIFIES (10/10 in total) |
| R7D-3 | `code/lowp/pilot/cleanup_pilot.sh`: path-valued overrides (`NC_HOME_ROOT`, `NC_SCR_ROOT`, `GUARD`, `SQUEUE`, `SACCT`) given relative to the caller's directory are resolved against it before `cd /` and exported through the re-exec. Bare command names stay on PATH. The dry run no longer changes directory. | `tests/test_cleanup_inplace.sh`: relative roots in the dry run (exit 0) and relative roots plus a relative GUARD with `--yes` (VERIFIED) (5/5 in total) |
| R7D-4 | `tests/test_p0a_tolerance.R`: the ULP helper now cycles from −3 to +3. | case B reruns with mixed-sign noise |

The suites were rerun on the final files: `conformance/work/conf2b_runs/pilot7d_20261030T0710Z/`; results are recorded in `code/lowp/pilot/LOCAL_TEST.md`, Revision 7d (follow-up).
