# R-5 v2 regression integration

Test-source integration is ready for the parent's freeze and Owls execution.
Nothing in this handoff is an executed PASS. This agent read the complete
deployment BRIEF, RULINGS_LEAD including R-5, and B_verify/VERDICT_v1.md;
performed local source inspection/edits and SHA-256 file audits only; made no
SSH/SCP calls, ran no R parsing, compilation or numerical/local tests, and
changed no root files, production sources or frozen snapshots.

Owned changes: common.R, worker.R, compare.R, changed_units.R and this note.
metadata_units.R required no change. The preprocessing and runtime agents own
their respective new units and runtime export header. Both units and the
header were read when available. Their implementation remains provisional
until the saved remote results are inspected.

## Production-only integration

The worker first saves its unchanged ordinary regression bundle, then sources
changed_units.R (including metadata_units.R), v2_preprocess_units.R and
v2_runtime_units.R in that order. Both v2 unit sources are mandatory, and each
must register at least one unit. Duplicate labels fail immediately. The
prototype worker does not execute the new production units.

common.R appends the contents of optional v2_runtime_exports.h after
wrappers.cpp in the production testing translation unit. This lets Rcpp see
the actual export annotations; merely including an external header would not
provide that export discovery. The prototype translation unit is unchanged.
The compile-cache identity now includes each appended file's literal-byte
SHA-256 in addition to its parsed lines and the existing production/header,
compiler, R, Rcpp and environment identity. No test export is added to the
production loader or source tree.

The original seeds.tsv and wrappers.cpp have byte-identical SHA-256 values
against snapshots/v1/tests/: seeds
7170c08e1fc09f8072ec465f2ef0332d24da974e207d6a4dea5617dba6c644cc;
wrappers c8aceafbac808e48def9be38c6880161c3feb82af74ad9a93269822709a7072d.
All original 32 fixtures, endpoints, arithmetic/RNG comparisons and existing
metadata units remain enabled. exact() is unchanged: storage types,
attributes and every double byte remain strict. No tolerance or projection
was added for ordinary preprocessing. Stable nearconstant behavior is tested
separately by the preprocessing units below.

## Cache exception, explicitly bounded

The original worker micro-run ro cache override remains max(500p,32768) on
both sides. The real v3_run_settings resolver is observed separately without
overrides. Before any new normalization, compare.R requires exactly 500p in
production and max(500p,32768) in the reference, both in that resolver output
and in the real full-calibration cache record. Mutations restoring the old
production floor must fail.

Only calibration_full$cache[["capacity"]] is then set to the already-validated
reference value for the existing complete calibration byte comparison. The
cache vector, names, type, attributes, hits, misses, inserts, clears and all
other records/counters remain in the comparison. A separate mutation check
changes each noncapacity counter in turn and requires byte-comparison
rejection after the projection. No recursive or name-pattern cache removal
is used. Other micro/final/calibration records keep their existing exact
comparisons and preexisting documented v1 exceptions.

## New unit inventory

Preprocessing agent's six production units:

- r5_preprocess_ordinary_prototype_bits: direct legacy arithmetic comparison
  for ordinary vectors, including large/small scales.
- r5_preprocess_B_N1_hand_Q_and_affine_score: B's four-row represented
  nearconstant reproducer for X and y, exact expected standardized vector,
  hand Q=57/20 and bounded affine score error.
- r5_preprocess_nearconstant_multi_ulp_scales_and_permutations: independent
  small-integer contrast oracle, signed/extreme scales and scaled SD.
- r5_preprocess_split_center_map_retained: original-index map and exact
  reconstruction from saved split-centering metadata.
- r5_preprocess_strict_numeric_shapes_without_coercion: unsupported X/y
  shapes/types and finite/dimension failures through preprocessing and fit.
- r5_preprocess_exact_constants_precedence_and_duplicates: exact-only
  removal, duplicate connectivity, minimum-subnormal contrast and statuses.

The numerical bounds in those new nearconstant units belong only to those
independent expected-value checks. They do not relax the ordinary 32-seed
prototype comparison.

Runtime agent's five production units:

- v2_cache_capacity_exactly_500p_run_and_calibration: both tiers, dimensions
  below/above the former floor, real constructor/final cache observations.
- v2_actual_score_timing_exact_size_including_stride_seven_reproducer:
  actual 200-score route count and exact accumulated score sink for six p/k
  combinations, including the p14/k7 size-two defect and k=0.
- v2_exact_hpm_phase_and_mechanism: B's smallest exact provenance reproducer.
- v2_inherited_rescore_failure_retains_hpm_and_is_contained: test-copy
  corruption reaches the real scorer, native handler and assembly; checks
  the retained ledger/HPM and restoration.
- v2_V_rescore_failure_propagates_preliminary_and_rebuild_and_calibration:
  real scorer failure before the preliminary grid and after a completed
  grid/diagnostic iteration; checks status, containment and prior archives.

The injected-failure tests establish conditional containment using fresh
testing objects. They do not claim natural finite-input reachability of
those scorer failures. Runtime units use local expression environments.

worker.R also adds test_source_bytes_unchanged on both sides. compare.R adds
R5_cache_capacity_expected_difference_before_normalization,
R5_cache_projection_preserves_every_counter, and each side's
unit_and_source_inventory check.

## Saved evidence and parent execution

Each worker now saves test_source_bytes.rds containing the literal bytes of
every frozen test file, including new units/header/notes. metadata.rds saves
the complete test-source SHA-256 inventory before and after execution.
unit_catalog.rds maps every old/new label to its source filename and hash;
unit_results.rds retains its actual result, timestamp and returned evidence.
The comparator checks catalog/result label identity, source presence/hashes,
rehashed saved bytes, unchanged sources and registration of both v2 suites.
Prototype/production metadata must also identify identical test-source hashes.
The existing prepare.py freeze and finish inventories include all new files
and outputs without a runner change.

Parent may freeze the integrated candidate and use the existing
run_all_seeds.sh entry point on Owls, first index 1 if desired, then all 32.
Inspect compilation, both workers' exit status/logs, comparison.json,
unit_results.rds, unit_catalog.rds, source byte inventories and the aggregate
summary. A missing unit file/export, compilation error, original byte mismatch
or failed unit remains a failure to investigate in a new candidate; it is not
grounds to widen tolerance or remove fields. Parent owns remote instructions,
resource admission, persistent jobs, manifests, seeds/process IDs, evidence
inspection, fresh dev smokes and final freeze/handoff. B v2 PASS remains a
separate gate.
