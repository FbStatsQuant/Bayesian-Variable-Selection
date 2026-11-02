# Builder A build notes

Local checks on 2026-10-30; no NOTS connection. Test artifacts are under
`<PC_TEMP_PATH>`. The sealed study was read only.

- Git Bash `bash -n`, individually, returned 0 for all 12 assigned sbatch
  scripts and all 6 assigned shell helpers/runner. R's parser returned
  `R parse PASS` for `R/prodl_inputs_check.R`.
- Batch smoke, local test enabled, dry run unset, modules skipped, stub hook:
  `ok` task exit 0, ledger rc=0/outcome=ok; two-second budget with a
  ten-second sleep task exit 1, ledger rc=124/outcome=killed_timeout; large
  clock offset task exit 0, ledger reason=deadline and inventory=deferred.
  Each inventory was inspected. The local machine had no verified GNU time;
  the smoke used the pilot's wall-clock fallback (arm smcrep).
- P0b on the sealed study: exit 0, PASS, 1200 rows, zero issues.
- P0b on the temporary study copy after flipping one byte of
  p0020_S1_r001.rds: exit 1, MISMATCH, one issue. Expected SHA-256
  570b361a83b9e995090c25987e8fb058e5124f6fa2c2517706b63c691309ca91;
  observed b2452f88af78de63b3f8666c0b95bf3fe61de411770cde1b3766ad69e0eb841b.
  R emitted locale startup warnings on this Windows host in both runs.
- The independent `B/tests/` suite was not run.

## Deviations

- The staging design includes the PROD-L bundle but does not stage
  `code/lowp/pilot/R/pilot_build.R`, and Builder A was not assigned an
  additional R build file. The accepted pilot build program is therefore
  embedded in `s0_build.sbatch` and called with the same arguments; it
  still produces BUILD_REPORT.txt.
- The request for Bash syntax checks on every file includes an R script and
  this Markdown note, which are not Bash programs. Bash checks cover every
  assigned shell file; R syntax was checked with R itself.
- The pilot's common helper only requires GNU time for its named arms; the
  new smcrep and p5 wrappers explicitly enforce the same exit-68 gate.
- The collector includes its own running scheduler row in its snapshot and
  excludes that row from the predecessor-terminal check.
