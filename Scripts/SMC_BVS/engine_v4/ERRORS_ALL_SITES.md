# Every error site in the engine source (generated inventory)

Companion of [ERRORS.md](ERRORS.md). Generated from the source at commit `c8a30d39` by scanning every `throw` statement under `src/` and `include/` (496 sites) and every place that sets a record's `reason` without throwing. **The line numbers are exact for that commit and drift as the source changes**; regenerate rather than edit. In the messages, `…` stands for a value filled in at run time (a path, a number, a name). "status" is the status the site raises (the exit code is 10 + status). A plain exception or a `std::bad_alloc` is caught in `src/cli/main.cpp:121-124` and becomes `internal_error` (15) or `resource_limit` (11). Messages are shown as written in the source, so they keep their internal labels; ERRORS.md §6 lists the ones to rewrite.

| status at the throw site | sites |
|---|---:|
| invalid_input | 384 |
| internal_error | 57 |
| other | 19 |
| io_error | 17 |
| bad_alloc | 7 |
| resource_limit | 7 |
| numerical_failure | 5 |

## `include/v4/calib.h` (4)

| line | status | message |
|---:|---|---|
| 176 | invalid_input | coded calibration (theory mode) requires SumMode::Serial and refine_m = 1 |
| 177 | invalid_input | bounded calibration has no tier escalation: tier0 must be 0 (D-26) |
| 179 | invalid_input | bounded calibration requires 0 <= I_max <= ell (D-26) |
| 180 | invalid_input | refine_m must be >= 1 |

## `include/v4/calib_backend.h` (2)

| line | status | message |
|---:|---|---|
| 172 | internal_error | calibration island …: ledger … |
| 186 | other | calibration island (tier …, iter …, island …): … |

## `include/v4/calib_rules.h` (3)

| line | status | message |
|---:|---|---|
| 76 | other | FV: lg0 and d differ in length |
| 196 | other | refine_grid: m must be >= 1 |
| 205 | internal_error | refine_grid: an interval is too short to split into m parts |

## `include/v4/cmd_args.h` (7)

| line | status | message |
|---:|---|---|
| 24 | invalid_input | : --manifest is not a JSON object |
| 26 | invalid_input | : the manifest is not a … manifest (command) |
| 45 | invalid_input | : --… … differs from the manifest's params.… … |
| 54 | invalid_input | : the manifest's inputs name … twice |
| 59 | invalid_input | : --… must be a path |
| 62 | invalid_input | : --… differs from the manifest's … |
| 63 | invalid_input | : no … (give --… or a manifest input) |

## `include/v4/format.h` (1)

| line | status | message |
|---:|---|---|
| 83 | invalid_input | section …: wrong dtype |

## `include/v4/island/amath.h` (1)

| line | status | message |
|---:|---|---|
| 41 | bad_alloc | throw std::bad_alloc() |

## `include/v4/island/calib_runner.h` (1)

| line | status | message |
|---:|---|---|
| 64 | other | throw (invalid_input): not an island outcome v4::calib::IslandOut o |

## `include/v4/island/island.h` (2)

| line | status | message |
|---:|---|---|
| 63 | bad_alloc | throw std::bad_alloc inside phase A at this pass (resource_limit path) int test_oom_merge = -1 |
| 64 | bad_alloc | throw std::bad_alloc in the parallel compaction from this merge on int test_corrupt_store_step = -1 |

## `include/v4/island/pilot_only.h` (5)

| line | status | message |
|---:|---|---|
| 49 | invalid_input | pilot: --data, --setup, --seed (1..2^31-1), --threads and --cost-dir are required |
| 63 | invalid_input | setup.bin was built from another data.bin |
| 79 | invalid_input | data.bin changed between the plan and the load |
| 81 | invalid_input | setup.bin changed between the plan and the load |
| 86 | io_error | cannot create --cost-dir … |

## `include/v4/island/setup_load.h` (37)

| line | status | message |
|---:|---|---|
| 28 | invalid_input | : code_ptr end marker != \|logr\| |
| 31 | invalid_input | partition shape |
| 36 | invalid_input | block tables shape |
| 39 | invalid_input | blk_members is not a partition of 0..p-1 |
| 44 | invalid_input | blk_members is not a partition of 0..p-1 (variable … in no block) |
| 52 | invalid_input | size_cum differs from the island's rebuild of the start law (core/cpp/v3_start.h) |
| 98 | invalid_input | : not a setup file |
| 106 | invalid_input | no section … (the admission plan needs it; INTERFACES §5.1) |
| 108 | invalid_input | partition shape |
| 112 | invalid_input | block size outside 1..20 |
| 126 | invalid_input | nb_ptr has … entries, expected p + 1 = … |
| 128 | invalid_input | size_logmass has … entries, expected K + 1 = … |
| 198 | invalid_input | : not a setup file |
| 199 | invalid_input | : setup.bin changed between the plan and the load |
| 209 | invalid_input | scalars_f64 is empty (log Zbar0) |
| 212 | invalid_input | n, p or K differ from the data |
| 213 | invalid_input | partition shape |
| 216 | invalid_input | blk / pos / blk_members length != p |
| 217 | invalid_input | code_ptr shape (J + 1 entries ending at \|logr\|) |
| 218 | invalid_input | logprof_ptr shape |
| 219 | invalid_input | logF / cond0 / size_logmass / size_cum shape |
| 222 | invalid_input | block size outside 1..20 |
| 223 | invalid_input | code_ptr: block … does not have 2^m codes |
| 224 | invalid_input | logprof_ptr: block … does not have min(m, K) + 1 rows |
| 229 | invalid_input | blk / pos / blk_members are not one partition of 0..p-1 (variable …) |
| 239 | invalid_input | size_cum is not a non-decreasing cumulative in [0, 1] (index …) |
| 240 | invalid_input | size_logmass has a NaN or +inf |
| 242 | invalid_input | size_cum does not end at exactly 1 |
| 243 | invalid_input | logF has a NaN or +inf |
| 244 | invalid_input | logprof has a NaN or +inf |
| 249 | invalid_input | size_cum differs from the rebuild from logF and the prior (core/cpp/v3_start.h:151) |
| 261 | invalid_input |  scan entries of cond0 differ from the rows rebuilt from logprof and logF (D-31) |
| 303 | invalid_input | : setup.bin changed between the plan and the load |
| 304 | invalid_input | : no neighbour lists (nb_ptr / nb_idx) |
| 306 | invalid_input | : nb_ptr shape (… entries for p = …, ptr[0] = …, ptr[p] = …, \|idx\| = …) |
| 308 | invalid_input | : nb_ptr not increasing |
| 309 | invalid_input | : nb_idx out of range |

## `include/v4/island/start_view.h` (1)

| line | status | message |
|---:|---|---|
| 111 | internal_error | StartView: draw scratch not prepared for thread … |

## `include/v4/island/store.h` (2)

| line | status | message |
|---:|---|---|
| 59 | bad_alloc | throw std::bad_alloc: caught by the owner) const int C = threads |
| 296 | bad_alloc | throw std::bad_alloc() |

## `include/v4/merge.h` (1)

| line | status | message |
|---:|---|---|
| 363 | internal_error | LS0 move cap out of range |

## `include/v4/offer_floor.h` (4)

| line | status | message |
|---:|---|---|
| 27 | invalid_input | : not a \"0x\" + 16 hex digits f64 |
| 65 | invalid_input | calib.bin meta.tau_cal is NaN or +inf |
| 90 | invalid_input | : the offer floor is NaN or +inf |
| 93 | invalid_input | : an offer floor without offer_floor_calib |

## `include/v4/rng.h` (10)

| line | status | message |
|---:|---|---|
| 58 | other | slot index >= 2^28 |
| 63 | other | address key field out of range |
| 67 | other | address counter field out of range |
| 106 | other | compat pilot tier (v3 has tiers 0, 1) |
| 108 | other | compat diag tier (v3 has tiers 0, 1) |
| 109 | other | compat diag island |
| 111 | other | compat final island |
| 113 | other | role has no compat stream |
| 164 | other | I5: address not increasing in the serial order |
| 168 | other | I5: address used twice |

## `include/v4/stubs.h` (1)

| line | status | message |
|---:|---|---|
| 1 | other | not implemented… |

## `include/v4/tail.h` (2)

| line | status | message |
|---:|---|---|
| 131 | numerical_failure | NaN score in the local search |
| 149 | numerical_failure | throw NumericalFailure(strip_status_prefix(fmsg)) |

## `include/v4/wp4_terminal.h` (3)

| line | status | message |
|---:|---|---|
| 21 | invalid_input | terminal_S: expected N + 1 = … offsets covering the pool |
| 24 | invalid_input | terminal_S: offsets not monotone or past the pool |
| 28 | invalid_input | terminal_S: support not sorted / unique / in range |

## `src/calib/calib_run.cpp` (15)

| line | status | message |
|---:|---|---|
| 41 | invalid_input | calibrate: --… must be a string |
| 48 | invalid_input | calibrate: --… must be a number |
| 51 | invalid_input | calibrate: --… must be a whole number in […, …] |
| 108 | invalid_input | calibrate: the manifest's mode must be a string |
| 109 | invalid_input | calibrate: --mode differs from the manifest's mode |
| 112 | invalid_input | calibrate: --mode must be compat, law or V |
| 116 | invalid_input | calibrate: --I_max / --refine_m apply to the bounded rule (mode V) only |
| 129 | invalid_input | calibrate: --data is required (or --n and --p with --plan-only) |
| 141 | invalid_input | calibrate: --setup is required |
| 143 | invalid_input | calibrate: setup.bin was built from another data.bin |
| 177 | invalid_input | calibrate: --out is required |
| 179 | invalid_input | calibrate: --seed is required (a whole number in [1, 2^31 - 1]) |
| 183 | invalid_input | calibrate: data.bin changed between the plan and the load |
| 185 | invalid_input | calibrate: setup.bin changed between the plan and the load |
| 194 | io_error | calibrate: cannot create --cost-dir …: … |

## `src/cli/main.cpp` (3)

| line | status | message |
|---:|---|---|
| 55 | invalid_input | bad argument … |
| 92 | invalid_input | info: the file is required (info FILE, or --in FILE) |
| 117 | invalid_input | unknown command … |

## `src/common/data.cpp` (3)

| line | status | message |
|---:|---|---|
| 29 | invalid_input | make_data: n and p must be positive |
| 30 | invalid_input | make_data: X/y size mismatch |
| 42 | invalid_input | make_data: orig size mismatch |

## `src/common/format.cpp` (27)

| line | status | message |
|---:|---|---|
| 19 | invalid_input | unknown dtype … |
| 32 | internal_error | section name length: … |
| 33 | internal_error | duplicate section … |
| 34 | internal_error | null section data: … |
| 51 | io_error | write failed: … |
| 79 | io_error | cannot create … |
| 90 | io_error | fsync failed: … |
| 91 | other | throw |
| 93 | io_error | rename failed: … |
| 98 | io_error | directory fsync failed: … |
| 104 | invalid_input | cannot open … |
| 106 | io_error | fstat … |
| 108 | invalid_input | file too short: … |
| 111 | io_error | mmap … |
| 116 | invalid_input | bad magic: … |
| 117 | invalid_input | unsupported format version: … |
| 118 | invalid_input | file size mismatch (truncated?): … |
| 120 | invalid_input | section table out of range: … |
| 124 | invalid_input | section table hash mismatch: … |
| 126 | invalid_input | header hash mismatch (header altered): … |
| 132 | invalid_input | section out of range: … |
| 134 | invalid_input | section length not a multiple of its dtype: … |
| 143 | invalid_input | section hash mismatch: … in … |
| 149 | invalid_input | section hash mismatch: … in … |
| 157 | invalid_input | missing section … in … |
| 161 | invalid_input | section … is not json |
| 176 | invalid_input | unknown mode … |

## `src/common/gen.cpp` (10)

| line | status | message |
|---:|---|---|
| 21 | invalid_input | unknown design … |
| 36 | invalid_input | gen: need n >= 3, p >= 1, seed in [1, 2^31-1] |
| 37 | invalid_input | gen: rho must be in [0, 1) |
| 38 | invalid_input | gen: b >= 1 |
| 39 | invalid_input | gen: s0 in 0..min(5, p) |
| 40 | invalid_input | gen: ADJ-OPP needs s0 >= 2 and p >= 10 |
| 62 | invalid_input | gen: truths do not fit in p columns |
| 76 | internal_error | gen: polar method did not accept |
| 123 | invalid_input | gen test: bad row range |
| 128 | invalid_input | gen test: column out of range |

## `src/common/json.cpp` (15)

| line | status | message |
|---:|---|---|
| 14 | internal_error | json: u64 above 2^53 must be written as a hex string |
| 18 | internal_error | json: not an object |
| 22 | invalid_input | json: not an object (key …) |
| 24 | invalid_input | json: missing key … |
| 28 | invalid_input | json: bad array index |
| 33 | internal_error | json: not an array |
| 36 | invalid_input | json: not a number |
| 39 | invalid_input | json: not an integer |
| 42 | invalid_input | json: not a bool |
| 43 | invalid_input | json: not a string |
| 96 | invalid_input | json parse: … at … |
| 171 | invalid_input | cannot open … |
| 177 | io_error | cannot write … |
| 177 | io_error | write failed … |
| 178 | io_error | rename failed … |

## `src/common/ledger.cpp` (5)

| line | status | message |
|---:|---|---|
| 33 | internal_error | ledger merge: config mismatch |
| 40 | internal_error | ledger: bad phase/mech |
| 70 | internal_error | absorb: thread ledger belongs to another island |
| 95 | internal_error | store: NaN value (breaks the strict order) |
| 97 | internal_error | store: model too large |

## `src/common/prep.cpp` (13)

| line | status | message |
|---:|---|---|
| 124 | invalid_input |  is not a data file |
| 128 | invalid_input | data.bin: bad n / p / p_raw |
| 131 | invalid_input | data.bin: section … has the wrong length |
| 139 | invalid_input | data.bin: kept has the wrong length |
| 140 | invalid_input | data.bin: dropped has the wrong length |
| 145 | invalid_input | data.bin: stored constants differ from the recomputed ones (libm or binary mismatch) |
| 153 | invalid_input | cannot open … |
| 156 | invalid_input | short file … |
| 181 | invalid_input | from_r: kept / dropped sizes do not match p, p_raw |
| 184 | invalid_input | from_r: kept / dropped is not a partition of 1..p_raw |
| 187 | invalid_input | from_r: kept not increasing |
| 195 | invalid_input |  is not a raw file |
| 205 | invalid_input | prep: … |

## `src/common/provenance.cpp` (3)

| line | status | message |
|---:|---|---|
| 101 | invalid_input | binary blocks incompatible: … |
| 109 | invalid_input | libm self-test failed for …: bit-form results would differ from the reference (Owls = NOTS) bits (INTERFACES §6) |
| 118 | invalid_input | input hash mismatch: … |

## `src/common/score.cpp` (2)

| line | status | message |
|---:|---|---|
| 160 | internal_error | score: \|S\| > K (infeasible model; callers never pass these, R1) |
| 166 | numerical_failure | score failed after Cholesky, refactor and augmented QR for a model of size … |

## `src/common/sha256.cpp` (1)

| line | status | message |
|---:|---|---|
| 74 | io_error | cannot open … |

## `src/common/status.cpp` (1)

| line | status | message |
|---:|---|---|
| 19 | invalid_input | unknown status … |

## `src/common/store.cpp` (9)

| line | status | message |
|---:|---|---|
| 43 | internal_error | store: NaN value (breaks the strict order) |
| 46 | internal_error | store: model too large |
| 169 | internal_error | load_unique_sorted: the store is not empty |
| 170 | invalid_input | store load: … entries > cap … |
| 173 | invalid_input | store load: pool range out of bounds |
| 174 | invalid_input | store load: NaN value |
| 176 | invalid_input | store load: a model is not sorted / has repeats |
| 178 | invalid_input | store load: entries not strictly sorted under the store order |
| 195 | invalid_input | store load: the same model appears twice (I1) |

## `src/eval/dist.cpp` (10)

| line | status | message |
|---:|---|---|
| 46 | invalid_input | quad_form: unknown design … |
| 93 | internal_error | gauss_hermite: no convergence |
| 107 | internal_error | gamma_draw: shape <= 0 |
| 117 | internal_error | gamma_draw: too many rejections |
| 134 | invalid_input | draw_x: design covariance not positive definite |
| 152 | internal_error | draw_y: S0 column missing |
| 278 | internal_error | comp_at: column missing |
| 289 | internal_error | comp_at: column missing |
| 447 | internal_error | dist_metrics: empty law |
| 450 | internal_error | dist_metrics: weights do not sum to 1 |

## `src/eval/io.cpp` (9)

| line | status | message |
|---:|---|---|
| 15 | invalid_input | : not a fit.bin (kind != 6) |
| 20 | invalid_input | fit.bin: top_off size |
| 21 | invalid_input | fit.bin: top_len size |
| 22 | invalid_input | fit.bin: top_hash size |
| 25 | invalid_input | fit.bin: store entry beyond pool |
| 26 | invalid_input | fit.bin: top store not sorted (I1) |
| 40 | invalid_input | fit.bin: a model appears twice in the top store (I1; re-merge with the current engine) |
| 49 | invalid_input | argument …: expected a string |
| 56 | invalid_input | argument …: expected a number |

## `src/eval/metrics.cpp` (2)

| line | status | message |
|---:|---|---|
| 71 | invalid_input | pip_metrics: length != p |
| 80 | invalid_input | pip_metrics: PIP outside [0,1] |

## `src/eval/model.cpp` (8)

| line | status | message |
|---:|---|---|
| 34 | invalid_input | truth.json: S0 and beta lengths differ |
| 39 | invalid_input | truth.json: bad S0 |
| 42 | invalid_input | truth.json: sigma must be > 0 |
| 55 | invalid_input | unknown design … |
| 65 | invalid_input | component_from_post: Data has no column statistics |
| 74 | invalid_input | component_gaussian: sizes differ |
| 75 | invalid_input | component_gaussian: orig not sorted |
| 76 | invalid_input | component_gaussian: sigma2 must be > 0 |

## `src/eval/posterior.cpp` (5)

| line | status | message |
|---:|---|---|
| 19 | invalid_input | data_from_raw: … … |
| 29 | invalid_input | model_post: model not sorted/unique |
| 30 | invalid_input | model_post: \|S\| > K |
| 50 | internal_error | model_post: Cholesky failed on the scorer's route |
| 60 | internal_error | model_post: QR failed on the scorer's route |

## `src/eval/run.cpp` (15)

| line | status | message |
|---:|---|---|
| 21 | invalid_input | fit.bin: … not sorted/unique |
| 26 | invalid_input | fit.bin: section … has wrong length |
| 53 | invalid_input | eval: bad mixture-predictive sizes |
| 54 | invalid_input | eval: bad Monte Carlo sizes |
| 102 | invalid_input | eval: --fit, --data, --truth and --out are required |
| 108 | invalid_input | truth.json: content hash differs from the manifest |
| 121 | invalid_input | fit.bin: meta.status missing |
| 196 | invalid_input | fit.bin: pip_r must be Rp × p |
| 273 | invalid_input | eval --competitor: --competitor, --data and --truth are required |
| 275 | invalid_input | : not a smcbvs4.competitor/1 record |
| 299 | invalid_input | competitor pip: idx and val lengths differ |
| 315 | invalid_input | competitor predictive: idx and coef lengths differ |
| 319 | invalid_input | competitor predictive: duplicate idx |
| 324 | invalid_input | competitor model_law: bad sizes |
| 335 | invalid_input | competitor predictive: unknown type … |

## `src/island/island_cmd.cpp` (35)

| line | status | message |
|---:|---|---|
| 54 | invalid_input |  must be a number |
| 57 | invalid_input |  must be a whole number in […, …] |
| 65 | invalid_input | --… must be a string |
| 70 | invalid_input | give --mem-budget or --mem-budget-gb, not both |
| 73 | invalid_input | --mem-budget-gb must be a number |
| 97 | invalid_input | the manifest's mode must be a string |
| 101 | invalid_input | --mode differs from the manifest's mode |
| 103 | invalid_input | --mode must be compat, law or V |
| 116 | invalid_input |  = … differs from … = … |
| 125 | invalid_input | island r = … > R' = … |
| 128 | invalid_input | --role must be final (pilot and diagnostic islands run inside calibrate) |
| 139 | invalid_input | : not a calib file |
| 143 | invalid_input | : calibration status … (no frozen grid) |
| 147 | invalid_input | : k_store missing, or not finite and > 0 |
| 156 | invalid_input | : frozen grid does not run from 0 to 1 |
| 157 | invalid_input | : frozen grid not strictly increasing |
| 188 | invalid_input | --plan-only with files needs --data, --setup and --calib |
| 193 | invalid_input | --plan-only needs --data/--setup/--calib, or --n and --p |
| 197 | invalid_input | --B differs from the engine's N-swap budget B = … |
| 211 | invalid_input | the island index is required (--island r, or manifest params.id / params.island) |
| 212 | invalid_input | --out is required |
| 213 | invalid_input | --seed is required (a whole number in [1, 2^31 - 1]) |
| 216 | invalid_input | calib.bin's mode is …, not … |
| 219 | invalid_input | calib.bin vs this binary: … |
| 222 | invalid_input | --seed … differs from the calibration's seed … |
| 224 | invalid_input | N differs from calib.bin's frozen N = … |
| 228 | invalid_input |  is not a data file |
| 238 | invalid_input | data.bin K = … differs from min(p, n / 2) = … |
| 242 | invalid_input | --B differs from the engine's N-swap budget B = min(isqrt n, isqrt p, 16) = … (n = …, p = …) |
| 244 | invalid_input | setup.bin was built from another data.bin |
| 246 | invalid_input | calib.bin's meta.inputs differ from the data.bin / setup.bin in use |
| 298 | invalid_input | data.bin changed between the metadata and the load |
| 300 | internal_error | the mapped start law differs from the planned sections |
| 306 | invalid_input | --stop-after-s must be a number > 0 |
| 317 | internal_error | island interrupted without a stop request |

## `src/island/island_file.cpp` (7)

| line | status | message |
|---:|---|---|
| 24 | internal_error | write_island_file: an interrupted island (stop_after_step) has no island file |
| 85 | invalid_input | : not an island file |
| 89 | invalid_input | : an offer floor outside V mode (D-29) |
| 110 | invalid_input | : inconsistent top store sections |
| 113 | invalid_input | : meta.p must be positive |
| 118 | invalid_input | : top store label out of range |
| 119 | invalid_input | : top store hash differs from the model's |

## `src/island/island_lm.h` (1)

| line | status | message |
|---:|---|---|
| 247 | bad_alloc | throw std::bad_alloc() |

## `src/island/island_pm.h` (2)

| line | status | message |
|---:|---|---|
| 28 | numerical_failure | score failed (test hook: I proposal) |
| 120 | bad_alloc | throw std::bad_alloc() |

## `src/island/island_run.h` (33)

| line | status | message |
|---:|---|---|
| 90 | internal_error | to_record: an interrupted island (stop_after_step) has no record |
| 204 | internal_error | throw v4::Error(v4::Status::internal_error, m) |
| 205 | resource_limit | throw v4::Error(v4::Status::resource_limit, m) |
| 206 | numerical_failure | throw v4::NumericalFailure(m) |
| 343 | internal_error | leader store: a NaN value was offered |
| 347 | internal_error | store: a NaN value was offered (INTERFACES v0.1.3) |
| 396 | internal_error | store invariant I1 violated (…) |
| 568 | io_error | cannot open checkpoint … |
| 579 | io_error | checkpoint write failed: … |
| 583 | io_error | directory fsync failed for … |
| 609 | invalid_input | checkpoint … is of the older format (serial checksum, before WP7 O4): remove it or finish the run with the binary that wrote it |
| 632 | invalid_input | checkpoint … belongs to another configuration or binary |
| 637 | internal_error | checkpoint …: checksum valid but payload unreadable |
| 856 | other | throw |
| 952 | invalid_input | run_island: the pilot is island 0, iteration 0 |
| 953 | invalid_input | run_island: a diagnostic island is 1..4 at iteration k >= 1 |
| 954 | invalid_input | run_island: calibration tier < 4 and iteration < 64 (INTERFACES §3) |
| 955 | invalid_input | run_island: calibration islands have no checkpoints |
| 956 | invalid_input | run_island: a compat calibration island needs the caller's stream (compat_src) |
| 958 | invalid_input | run_island: a final island is r >= 1 |
| 959 | invalid_input | run_island: grid must run from 0 to 1 |
| 960 | invalid_input | run_island: grid not strictly increasing (I3) |
| 961 | invalid_input | run_island: the adaptive schedule has no checkpoints |
| 963 | invalid_input | run_island: compat mode needs Arith::Bit, the particle-major kernel and 1 thread (serial v3 streams) |
| 965 | invalid_input | run_island: the bit-form label-major kernel is test-only (D-21, manager Q1); theory mode runs particle-major |
| 966 | invalid_input | run_island: stop_after_step needs a checkpoint path |
| 967 | invalid_input | run_island: stop_after_s must be >= 0 |
| 969 | invalid_input | run_island: stop_after_s needs a checkpoint path and a final island |
| 970 | invalid_input | run_island: G must be in 0..256 (0 = chosen by mem_budget; manager Q3) |
| 975 | invalid_input | run_island: the offer floor must be -inf or finite (D-29) |
| 978 | invalid_input | run_island: an offer floor is for V-mode final islands only (not compat, law, leaders or calibration roles; D-29) |
| 979 | invalid_input | run_island: an offer floor needs the calib.bin content hash it came from (D-29) |
| 984 | invalid_input | run_island: a final island at p >= 1e5 needs k_store (the calibration-measured mean stored \|S\|, calib.bin) |

## `src/merge/wp4_io.cpp` (126)

| line | status | message |
|---:|---|---|
| 42 | invalid_input | : model larger than K |
| 45 | invalid_input | : index out of range [0, p) |
| 46 | invalid_input | : model not strictly increasing |
| 51 | invalid_input | : not finite |
| 56 | invalid_input | : offsets do not cover the pool |
| 58 | invalid_input | : offsets not monotone or past the pool |
| 71 | internal_error | add_store: store … is not compacted |
| 92 | invalid_input | store …: inconsistent sections |
| 94 | invalid_input | store …: pool out of range |
| 97 | invalid_input | store …: hash differs from the model's |
| 100 | invalid_input | store …: not a valid sorted store (I1) |
| 123 | invalid_input | unknown phase/mechanism name … |
| 147 | invalid_input | logical: wrong size |
| 220 | internal_error | write_calib: a non-finite inherited F |
| 253 | internal_error | write_calib: extra meta key … is reserved |
| 271 | invalid_input | : tau_cal outside V mode (D-29) |
| 277 | invalid_input | : calib: inherited arrays differ in length |
| 278 | invalid_input | : inh: offsets do not cover the pool |
| 280 | invalid_input | : inh: offsets not monotone or past the pool |
| 290 | invalid_input | : more than … inherited models and not in canonical (lexicographic) order |
| 293 | invalid_input | : inherited models are not distinct (D-29: tau_cal is over distinct models) |
| 296 | invalid_input | : tau_cal is not the c-th best F of the distinct inherited models (D-29) |
| 309 | invalid_input | inh: offsets do not cover the pool |
| 311 | invalid_input | inh: offsets not monotone or past the pool |
| 312 | invalid_input | calib: inherited arrays differ in length |
| 323 | invalid_input | : not a calib file |
| 328 | invalid_input | : calib meta N / L / Hm / tier out of range |
| 330 | invalid_input | : frozen grid is not a valid grid |
| 336 | invalid_input | : a V calib.bin must have the bounded rule, tier 0 and N = 2500 (D-1, D-26) |
| 337 | invalid_input | : I_used <= I_max <= ell violated |
| 338 | invalid_input | : a theory-mode calib.bin must have the coded rule |
| 342 | invalid_input | : meta.inputs differ from the data / setup in use |
| 347 | invalid_input | : k_store (calibration mean stored \|S\|) missing or not finite and > 0 |
| 359 | invalid_input | calib: inherited arrays differ in length |
| 375 | invalid_input | : calib.bin changed between the read and the inherited offers |
| 379 | invalid_input | : inherited arrays changed |
| 383 | invalid_input | : inherited offsets changed since they were validated |
| 386 | invalid_input | : inherited offsets changed since they were validated |
| 387 | invalid_input | : an inherited model label changed since it was validated |
| 415 | internal_error | write_island: store not compacted |
| 467 | invalid_input | : meta.mode '…' differs from the container header's mode |
| 468 | invalid_input | : an offer floor needs meta.mode = V (D-29) |
| 485 | invalid_input | p differs from data.bin |
| 486 | invalid_input | meta r / N / T / L / Hm out of range |
| 490 | invalid_input | grid / st_ess length differs from T |
| 491 | invalid_input | st_ess: not in [0, N] |
| 493 | invalid_input | grid differs from calib.bin's frozen grid |
| 494 | invalid_input | L / Hm differ from calib.bin |
| 501 | invalid_input | inconsistent top store sections |
| 503 | invalid_input | top store: pool offset out of range |
| 507 | invalid_input | top store: hash differs from the model's |
| 512 | invalid_input | top store not sorted / unique (I1) |
| 515 | invalid_input | hpm_val / hpm_ev size |
| 524 | invalid_input | hpm_S / hpm_val differ from the store's best entry |
| 526 | invalid_input | hpm_ev phase / mech out of range |
| 527 | invalid_input | hpm_ev is not a final event of this island |
| 528 | invalid_input | hpm_ev xph out of range |
| 529 | invalid_input | hpm_ev field out of range |
| 530 | invalid_input | hpm_ev iter out of range |
| 531 | invalid_input | hpm_ev tier is not the frozen tier |
| 532 | invalid_input | hpm_ev sub out of range |
| 533 | invalid_input | hpm_ev stage out of range [0, T] |
| 541 | invalid_input | a completed island with an empty store |
| 544 | invalid_input | island_best length is not r + 1 |
| 545 | invalid_input | island_best: not finite |
| 547 | invalid_input | island_best[r] differs from the island HPM's F |
| 551 | invalid_input | logical size |
| 555 | invalid_input | logZ size |
| 558 | invalid_input | pip_r has the wrong length |
| 559 | invalid_input | pip_r: not in [0, 1] |
| 561 | invalid_input | rb_round is not Hm x p |
| 650 | invalid_input | table store model spans blocks |
| 666 | invalid_input | size_logmass length != K + 1 |
| 669 | invalid_input | size_logmass not a log probability |
| 672 | invalid_input | size_logmass does not sum to 1 |
| 679 | invalid_input | section … too long for a plan read |
| 681 | invalid_input | section … hash mismatch |
| 686 | invalid_input | section … is not json |
| 688 | invalid_input | section … too long for a plan read |
| 691 | invalid_input | cannot open … |
| 694 | io_error | short read of section … |
| 704 | invalid_input |  is not a data file |
| 707 | invalid_input | meta has no n / p / K |
| 709 | invalid_input | bad n / p / K |
| 715 | invalid_input | : not a setup file |
| 724 | invalid_input | blk / pos / blk_members length != p |
| 727 | invalid_input | code_ptr must have J + 1 entries like blk_ptr |
| 729 | invalid_input | blk_ptr shape |
| 730 | invalid_input | code_ptr[0] != 0 or code_ptr[J] != \|logr\| |
| 733 | invalid_input | block size outside 1..20 |
| 735 | invalid_input | code_ptr / logr out of range |
| 736 | invalid_input | code_ptr: block table length != 2^m |
| 737 | invalid_input | logr not finite for a code with \|U\| <= K |
| 741 | invalid_input | blk out of range |
| 742 | invalid_input | pos out of range of its block |
| 743 | invalid_input | blk / pos / blk_members inconsistent |
| 758 | internal_error | write_setup_min: code_ptr must have J + 1 entries with code_ptr[J] = \|logr\| (INTERFACES v0.1.19) |
| 935 | invalid_input | merge: --manifest is not a JSON object |
| 941 | invalid_input | merge: manifest inputs name … twice |
| 951 | invalid_input | merge: --… must be a path |
| 952 | invalid_input | merge: --… differs from the manifest's … |
| 953 | invalid_input | merge: no … (give --… or a manifest input) |
| 958 | invalid_input | merge: --out is required |
| 962 | invalid_input | merge: … must be a number |
| 964 | invalid_input | merge: … must be a whole number in [1, 10^6] |
| 970 | invalid_input | merge: --Rp differs from the manifest's params.Rp |
| 972 | invalid_input | merge: R' must be given (manifest params.Rp or --Rp) |
| 983 | invalid_input | merge: bad island input name … |
| 985 | invalid_input | merge: island … named twice in the manifest |
| 989 | invalid_input | merge: island index … outside 1..R' |
| 991 | invalid_input | merge: island … of R' = … is not in the manifest |
| 994 | invalid_input | merge: the manifest names no island inputs |
| 1000 | invalid_input | merge: --islands entries must be paths |
| 1008 | invalid_input | merge: empty entry in --islands |
| 1012 | invalid_input | merge: --islands must be a list of paths |
| 1014 | invalid_input | merge: an island path appears twice |
| 1015 | invalid_input | merge: --islands differs from the manifest's island inputs (r = 1..R') |
| 1018 | invalid_input | merge: … island files for R' = … (no subset is ever pooled) |
| 1022 | invalid_input | merge: --mode differs from the manifest's mode |
| 1024 | invalid_input | merge: mode not given (--mode or the manifest's mode) |
| 1045 | invalid_input | merge: … must be a number |
| 1048 | invalid_input | merge: … must be a whole number of bytes in [0, 2^50] (0 = off) |
| 1052 | invalid_input | merge: give --mem-budget or --mem-budget-gb, not both |
| 1105 | invalid_input | : content hash differs from the manifest |
| 1107 | invalid_input | calib.bin status …: no frozen grid |
| 1108 | invalid_input | calib.bin mode differs from the merge mode |

## `src/post/law.cpp` (8)

| line | status | message |
|---:|---|---|
| 23 | invalid_input | build_law: empty store |
| 129 | invalid_input | : not a law.bin (kind != 7) |
| 131 | invalid_input | : unknown law schema |
| 140 | invalid_input | law.bin: model_ptr |
| 142 | invalid_input | law.bin: model_idx size |
| 153 | invalid_input | law.bin: LH block size |
| 173 | invalid_input | post: --fit, --data and --out are required |
| 182 | invalid_input | fit.bin: meta.status missing |

## `src/setup/account.cpp` (2)

| line | status | message |
|---:|---|---|
| 185 | internal_error | edges_by_filter: AVX-512F not available |
| 228 | resource_limit | edges_by_filter: allocation failed |

## `src/setup/corr.cpp` (3)

| line | status | message |
|---:|---|---|
| 71 | invalid_input | correlation_pass: B out of range |
| 120 | resource_limit | correlation_pass: more than max_edges edges in the uncapped threshold graph (hub design); raise max_edges |
| 159 | resource_limit | correlation_pass: more than max_edges edges (hub design); raise max_edges |

## `src/setup/partition.cpp` (5)

| line | status | message |
|---:|---|---|
| 191 | internal_error | cut_and_pack: leaf order needs one root |
| 215 | internal_error | cut_and_pack: blocks do not cover every column |
| 222 | invalid_input | partition: B outside 1..16 (core/cpp/v3_core.cpp:180) |
| 223 | invalid_input | partition: bv_cap outside 1..16 |
| 231 | internal_error | partition: tau differs from the correlation pass's tau |

## `src/setup/setup_island.cpp` (3)

| line | status | message |
|---:|---|---|
| 10 | invalid_input | setup: K or p differ from the data |
| 47 | invalid_input | : n, p or K differ from the data |
| 49 | invalid_input | : built from another data.bin (meta.inputs differs) |

## `src/setup/setup_run.cpp` (15)

| line | status | message |
|---:|---|---|
| 45 | resource_limit | throw Error(Status::resource_limit, b) |
| 58 | resource_limit | throw Error(Status::resource_limit, b) |
| 98 | internal_error | write_setup_bin: setup did not complete (GUARD-W) |
| 144 | invalid_input |  is not a setup file |
| 152 | invalid_input | setup.bin: scalars missing |
| 160 | invalid_input | setup.bin: cond0 size differs from J x (K + 1) |
| 185 | invalid_input | setup: the manifest names data.bin twice |
| 190 | invalid_input | setup: --data must be a path |
| 192 | invalid_input | setup: --data differs from the manifest's data.bin |
| 195 | invalid_input | setup: no data.bin (give --data or a manifest input data.bin) |
| 196 | invalid_input | setup: --out is required |
| 202 | invalid_input | setup: the manifest's … differs from data.bin |
| 210 | invalid_input | setup: the manifest's mode must be a string |
| 217 | invalid_input | setup: partition must be truncated or exact |
| 228 | invalid_input | setup: compat mode uses the exact partition (v3 rule) |

## `src/setup/start.cpp` (4)

| line | status | message |
|---:|---|---|
| 264 | internal_error | start_mode tie DP: no tight path from (J, kbest) (invalid tables) |
| 291 | invalid_input | start_mode: the e4 tie-aware fallback requires cap >= 2 (C-PACK MR2) |
| 294 | internal_error | start_mode: no feasible size (invalid tables) |
| 310 | internal_error | start_mode: truncated enumeration without tie DP needs ModeAlgo::Enumerate |

## `src/setup/tables.cpp` (5)

| line | status | message |
|---:|---|---|
| 172 | invalid_input | build_tables: block size outside 1..16 |
| 238 | internal_error | tables: non-finite table value |
| 266 | other | tables: … |
| 333 | internal_error | codes_of_size: m or j out of range |
| 432 | internal_error | cond_row: a block has more than 16 members |

## `src/setup/tiles.h` (3)

| line | status | message |
|---:|---|---|
| 111 | resource_limit | correlation tiles: out of memory |
| 112 | other | throw Error(est, msg) |
| 113 | internal_error | correlation tiles: unexpected exception |

## `src/stubs/stubs.cpp` (1)

| line | status | message |
|---:|---|---|
| 6 | internal_error | : not implemented (…) |

## Reasons set without a throw (records of refused or failed runs)

| file:line | text of the assignment |
|---|---|
| src/calib/calib_run.cpp:160 | if (!resident_ok) { rec["status"] = "resource_limit"; rec["reason"] = "calibrate not admitted: calibration state " + std::to_string(plan.resident) + " B >= --mem-budget"; } |
| src/calib/calib_run.cpp:163 | rec["reason"] = "calibration island not admitted (N-1): resident + island plan " + std::to_string(ipl.ip.total) + " B > --mem-budget"; |
| src/calib/calib_run.cpp:168 | rec["status"] = "resource_limit"; rec["reason"] = "calibrate not admitted: calibration state " + std::to_string(plan.resident) + " B >= --mem-budget"; |
| src/calib/calib_run.cpp:174 | rec["reason"] = "calibration island not admitted (N-1): resident + island plan " + std::to_string(ipl.ip.total) + " B > --mem-budget"; |
| src/cli/main.cpp:120 | st = e.st; rec = Json::object(); rec["reason"] = e.what(); |
| src/cli/main.cpp:122 | st = Status::resource_limit; rec = Json::object(); rec["reason"] = "out of memory"; |
| src/cli/main.cpp:124 | st = Status::internal_error; rec = Json::object(); rec["reason"] = e.what(); |
| src/common/prep.cpp:73 | auto bad = [&](const char* why) { r.status = "invalid_input"; r.reason = why; return r; }; |
| src/eval/run.cpp:126 | rec["reason"] = "fit not completed: no metrics"; |
| src/eval/run.cpp:286 | if (cst != "completed") { rec["reason"] = jstr_or(C, "reason", "competitor did not complete"); rec["status"] = "completed"; return rec; } |
| src/island/island_cmd.cpp:205 | if (budget && mp.total > budget) rec["reason"] = "island not admitted: plan " + std::to_string(mp.total) + " B > --mem-budget"; |
| src/island/island_cmd.cpp:284 | if (!admitted) rec["reason"] = "island not admitted: " + refusal; |
| src/island/island_cmd.cpp:289 | IslandRun r; r.status = 3; r.reason = refusal; r.r = (int)in.r; r.N = C.N; r.p = (int)p; r.L = C.L; r.Hm = C.Hm; r.G_used = mp.G; r.mem_plan = mem_plan_text(mp); |
| src/island/island_cmd.cpp:292 | rec["status"] = "resource_limit"; rec["reason"] = refusal; rec["G_used"] = mp.G; |
| src/island/island_cmd.cpp:311 | rec["status"] = "completed"; rec["island_status"] = "interrupted_resumable"; rec["reason"] = r.reason; |
| src/island/island_cmd.cpp:322 | if (!r.reason.empty()) rec["reason"] = r.reason; |
| src/island/island_file.cpp:32 | m["status"] = status_str(r.status); m["reason"] = r.reason; m["inputs"] = inputs; m["binary"] = binary_block(); |
| src/island/island_run.h:375 | res.status = 3; res.reason = "mem_budget: predicted peak " + std::to_string(mp.total >> 20) + " MiB > budget " + std::to_string(cfg.mem_budget >> 20) + |
| src/island/island_run.h:853 | res.status = 2; res.reason = e.what(); |
| src/island/island_run.h:857 | res.status = 3; res.reason = e.what(); |
| src/island/island_run.h:859 | res.status = 3; res.reason = "resource_limit: out of memory"; |
| src/island/island_run.h:862 | try { sync_ledgers(); } catch (const std::bad_alloc&) { res.status = 3; res.reason = "resource_limit: out of memory"; } |
| src/island/island_run.h:874 | res.reason = time_stop ? "interrupted after checkpoint (stop_after_s: resumable)" : "interrupted after checkpoint (stop_after_step)"; |
| src/island/island_run.h:994 | r.reason = "mem_budget: predicted peak " + std::to_string(mp.total >> 20) + " MiB > budget " + std::to_string(cfg.mem_budget >> 20) + " MiB [" + r.mem_plan + "]"; |
| src/merge/wp4_io.cpp:404 | meta["status"] = status_name(isl.status); meta["reason"] = isl.message; meta["inputs"] = inputs; |
| src/merge/wp4_io.cpp:820 | meta["status"] = status_name(fo.status); meta["fit_state"] = fo.fit_state; meta["reason"] = fo.reason; |
| src/merge/wp4_io.cpp:889 | rec["status"] = status_name(fo.status); rec["fit_state"] = fo.fit_state; rec["reason"] = fo.reason; |
| src/merge/wp4_io.cpp:1076 | merge::FitOut fo; fo.mem = est; fo.status = Status::resource_limit; fo.fit_state = "not_admitted"; fo.reason = why; |
| src/post/law.cpp:184 | rec["fit_status"] = ff.meta.at("status").str(); rec["reason"] = "fit not completed: no law"; rec["status"] = "completed"; |
| src/setup/setup_run.cpp:70 | R.status = e.st; R.reason = e.what(); |
| src/setup/setup_run.cpp:72 | R.status = Status::resource_limit; R.reason = "out of memory"; |
| src/setup/setup_run.cpp:74 | R.status = Status::internal_error; R.reason = e.what(); |
| src/setup/setup_run.cpp:247 | if (r.status != Status::completed) { rec["reason"] = r.reason; return rec; } // GUARD-W: no setup.bin |
| include/v4/merge.h:261 | if (ms.Rp < 1) { out.status = Status::invalid_input; out.fit_state = "incomplete"; out.reason = "R' < 1: nothing to merge (review PR20 C-1)"; return false; } |
| include/v4/merge.h:262 | if (src.count() != ms.Rp) { out.status = Status::invalid_input; out.fit_state = "incomplete"; out.reason = "manifest R' != number of islands"; return false; } |
| include/v4/merge.h:278 | out.reason = "merge refused (GUARD-W): " + std::to_string(out.missing.size()) + " missing, " + std::to_string(out.invalid.size()) + |
| include/v4/merge.h:296 | out.reason = "merge not admitted: estimated peak " + std::to_string(out.mem.total) + " B > --mem-budget " + std::to_string(ms.mem_budget_bytes) + " B"; |
| include/v4/merge.h:301 | out.reason = "merge refused: the pre-island ledger has leader stores (final-run ledgers need leaders = false, INTERFACES v0.1.7)"; |
| include/v4/merge.h:315 | out.reason = "merge refused (GUARD-W): island " + std::to_string(r) + ": malformed (" + I.message + ")"; |
| include/v4/merge.h:321 | out.reason = "merge refused (GUARD-W): island " + std::to_string(r) + " changed between the head check and its load"; |
| include/v4/merge.h:327 | out.reason = "merge refused (GUARD-W): island " + std::to_string(r) + " has leader stores (INTERFACES v0.1.7)"; |
| include/v4/merge.h:333 | out.reason = "merge refused (GUARD-W): island " + std::to_string(r) + " has " + std::to_string(I.terminal.size()) + |
| include/v4/merge.h:356 | out.status = Status::resource_limit; out.fit_state = "failed"; out.reason = "runtime guard after the final local search"; |
| include/v4/merge.h:369 | out.status = Status::resource_limit; out.fit_state = "failed"; out.reason = "runtime guard after LS0"; |
| include/v4/merge.h:373 | out.status = Status::numerical_failure; out.fit_state = "failed"; out.reason = e.what(); |
| include/v4/merge.h:375 | out.status = e.st; out.fit_state = "failed"; out.reason = e.what(); |
| include/v4/merge.h:488 | bad.reason = "a non-finite estimate at assembly (internal check)"; bad.has_hpm = out.has_hpm; bad.hpm = out.hpm; bad.hpm_F = out.hpm_F; |
