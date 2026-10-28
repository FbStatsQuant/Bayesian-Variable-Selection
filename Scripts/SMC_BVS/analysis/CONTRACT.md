# Schema, scoring and uncertainty contract

Full BRIEF including Amendments 1/2, RULINGS_LEAD.md R-1/R-2/R-3, master IV.1, integration notes, unchanged benchmark scoring and frozen PREREG_c050 govern. Local mock tests are authorized. Assessment: r1..10, S1..S6, p500/p1000, separate c100/c050; 120 datasets, 240 fits, 480 expected rows; denominators 10/cell and 60/p-scale pooled. Full historical reproduction is separate.

## Inputs, selection and source integrity

run_pipeline.py accepts synthetic or assessment mode, with absolute paths. Output is a NEW directory under output_root, the owning pipeline directory. Local tests need no Owls host/nice guard; Owls resource checks apply only on Owls. No networking or scheduler work occurs.

Config: mode, out, output_root, rscript, benchmark_scoring, inputs_manifest, truth_manifest, truth_dir, mapping_ruling, assessment_selector, benchmark_sources, smc_sources. Assessment also requires ops_outputs and both combined_references canonical versions. source_inventory records runs.tsv. Optional mapping_csv is an audit artifact only. Hashing evidence is not independent substantive approval.

Selector:
    {"p":[500,1000],"scenario":[1,2,3,4,5,6],"replicate":[1,2,3,4,5,6,7,8,9,10],"scale_key":["c100","c050"]}

Manifest dataset IDs are unique and identify exact design rows. Full benchmark rows are checked against authoritative stored X/Y hashes, row identities and design BEFORE filtering; retained rows are checked again afterward. Bad excluded-r11..100 hashes cannot hide. Equal hashes on legitimate repeated designs are allowed. Missing selected rows and whole method-rule groups remain in denominators. Selected cases/manifest and selector hashes are saved. Internal standardization never changes stored-input hashes.

Sources supply scored_rows.csv, coverage.csv, problems.csv, truth_signals.csv and score_log.txt from unchanged Phase1 scoring. Blocking problems are rejected. Unchanged aggregate/combine code regenerates full-design tables. All eleven CSV claims have explicit unique key sorts (combined includes run_id); R identical() compares cells/types; byte equality is separate. Absent originals are disclosure gaps, never passes. No Markdown/log byte-equality claim.

Every registry and derived rule remains in summaries/figures. Explicit additional_registry_csv and method_alias may label separate long-chain sensitivities after their original tables reproduce. Baseline A3 is never replaced. No absent raw long-chain source is invented.

## Adopted mapping R-1 and actual A schema

The full ruling is frozen at vendor/RULINGS_LEAD.md and pinned to SHA-256 3bf2e514065ff4ccdaf5f2dd9ec82375df147f3bd6f308f75c965f5975bbe88a. A changed ruling fails closed for explicit review. SOURCE_SHA256.csv identifies the actual copied A adapter used by the completed suite. Historical pre-R1 source is preserved separately.

Roles: hpm primary; pip05 S0. converged, fold_seed, fold_sha256 MUST be NA. The benchmark manifest's fold values are not copied onto SMC rows.

exact/completed yield ok, or warning iff an R warning OR message was captured; captured text stays verbatim. Other native statuses (including y_constant/no_predictors/adapter_error) yield failed, support/k NA, with returned support kept in support_audit. timeout/not_run are reconciliation-only and never invented as native sampler outcomes.

diag_flag is identical on both rows and TRUE iff final numerical checks fail (checks_passed_final FALSE / E1-E3), low_empirical_ESS, grid_unconverged or local_limit. It NEVER changes status or selection. Codes final_check_E1/E2/E3, low_empirical_ESS, grid_unconverged and local_limit identify fired diagnostics. escalated, cut_group, near_tie_truncated, forced_pilot_steps, exact_branch, local_certified_false and global_certified are informational only.

Native CSV fields are v3_status/v3_flags_json. RDS top-level pip, rows, fit, estimates_available and policy identity are retained, including all native stages, pooled/island logZ, full PIPs, labelled heuristic bound and timings. JSON flags must agree with the retained fit. No invented native_status/native_flags CSV interface is required.

Each present SMC CSV requires .rds/.sha256/.done in pPPPP/case_id. Sidecars verify both files. All IV.1 columns, exact design/provenance/hashes, data_seed and method_seed=data_seed+4,000,000 are checked. CSV/RDS statuses/selection/native/policy fields agree. Unadopted policy markers fail closed. Per-fit shared provenance/runtime/native/policy values agree. Prefilled truth is rejected. Failed audit supports are never scored. Successful blank support is a genuine null model.

Available primary PIP is finite, length p, in [0,1]; pip05 equals strictly {j:pip[j]>.5}. Unavailable PIP remains unavailable, including failed degenerate cases. No PIP or support is fabricated from failure.

The unchanged load_truth, parse_support, read_pip and score_fit_rows functions perform scoring. The closed-registry score_run CLI rejects SMCBVS, so its unchanged kernel is called with explicit interface validation. Scorer/registry/aggregator/combiner hashes are pinned; all code/derived_rules copies are byte-identical. Only scoring opens named selected truth RDS files; they are hashed before/after. No broad truth/holdout traversal or fitting rerun.

## Metrics and uncertainty

Scales remain separate because they share datasets/noise. Exact all-saved uses expected denominator with failed/missing zero. Passing requires diag_flag exactly FALSE, with the same expected denominator. Among-success exact is secondary. FP/FN use successful rows only, saving n/sum/mean/sample variance/MCSE; failures remain NA.

Sample variance=sum((x-mean)^2)/(n-1), MCSE=sqrt(s2/n), including binary rates. n<2 is NA. Zero observed variance is not certainty. Scenario-pooled MCSE uses fixed strata: sqrt(sum_h (n_h/N)^2*s_h2/n_h). Pooled mixture variance is descriptive, distinct from stratified MCSE.

Crucial caveat: pooled FP/FN and complete-success-pair MCSEs condition on observed successful stratum counts and their observed weights. They DO NOT include randomness of failure-driven mixture weights or selection. A positive stratum with n<2 yields NA.

Paired differences are SMC minus comparator within case, with paired-difference sample variance. Exact/passing/failure use all expected cases; FP/FN use complete-success pairs with their own n. Observed coverage is separate from expected pairing. No independent-arm SE substitutes for pairing.

T4 uses each case's mean selection proportion over the group's variables, then across-case/fixed-stratum uncertainty. Failed/missing cases contribute zero. Integer selected/opportunity counts and n_signals remain inspectable. Do not treat n*signals as independent. Variable, abs(beta) and S6-rho groupings are saved.

T5 retains one original runtime per fit, including available failure times. Median, type-7 p95 and max are descriptive, with no fabricated SE. Twenty-eight SVG figures retain every rule, role and preregistered/post-hoc label by scenario/p/scale and pooled; whiskers are one MCSE, not confidence intervals.

## Validation and gates

The README command regenerates all mock artifacts and freezes evidence after passing. This is a D-owned SCHEMA-LEVEL MOCK using current A CSV/RDS layout plus R-1 semantics, NOT certification/execution of A's updated adapter. Immutable pre-R1 helpers supply extraction/layout; D reference row/persistence functions produce the positive fixture with gzip encoding. Formal A R-1 handoff and actual frozen-A mock rerun remain an explicit integration gate. Earlier old-A debug attempts are preserved separately. R-1 tests cover native statuses, warnings, messages, diagnostic-only flags, every informational code, failed audit, NA folds and unchanged selection. The full deterministic fixture covers every benchmark/derived rule, exact/extra/missed/mixed/null/flagged/failed/timeout/not_run, audit supports, missing fit/rule, excluded r11, repeated hashes and strict PIP threshold. Saved adversarial tests include duplicate/hash defects (also outside selection), stale truth, sidecars/bundles, unavailable/mismatched PIPs, CSV/RDS disagreement and unadopted policies.

This is implementer regression evidence, not independent review. Parent's 15 mathematical cases at ../review_metrics/20261022T194630Z/report.json are hash-specific and not full verification. The final source requires a NEW independent review. R-2 candidates stay here for lead merge; no root writes. R-3: D4 build/D2 during C batch on Owls; nice19, shared limits. Independent production raw-cell recount and lead review remain required. No cancelled review is counted.


## R4: native integrity and actual development smoke (review F1-F4)

native_contract.R reconstructs original-index primary PIPs independently from fit$pip_primary and the strict kept/dropped preprocessing partition. Retained/exported HPM/MPM and full PIPs must match native sources. Native fit$status, record$native_status and CSV v3_status must agree. The sole adapter_error exception is before any core fit returned: fit=NULL, nonempty recorded error and unavailable estimates. Retained-fit adapter errors are rejected until an explicit supported schema is adopted.

Completed SMC records require branch_run=smc, available native estimates, final diagnostic flags, stage_table with actual phase/island/ess/cum_log_Z columns, pooled log_Z, log_Z_r (the actual A field, four islands), four streams, log_Z_lower95, heuristic label/annotation, and timings$total. NA ESS is allowed on non-ESS stage rows; finite stage ESS must exist. Exact records require nested exact evidence/PIPs/HPM and explicitly absent SMC stages/island streams. Early native failures must not fabricate completed payload. Missing and invalid payloads fail before truth opens.

All represented v3_flags_json fields are compared with the retained fit: flags, cut_group, cut_group_count, cut_group_components, local_limit, local_certified, global_certified and near_tie_truncated. Failed support_audit is checked against native HPM and returned native PIP-derived MPM, including partial estimates; NA is unavailable and empty string is a returned null model.

The one-command suite includes the real A dev smoke outputs (p500/p1000) read-only. validate_native mode performs schema/native checks only and never reads truth or scores. Untouched legacy copies pass native integrity and are expected to fail R-1 because roles/diagnostics/mapping/folds remain pre-R1. D-owned R-1-adapted copies change interface mapping and add an explicitly D-owned heuristic-bound annotation only. All native fit values/attributes remain identical with num.eq=FALSE; serialization representation bytes are not treated as object equality. Original output files are SHA-256 checked before/after and at freeze. This is not execution or certification of an updated A R-1 adapter. That gate and a NEW independent review remain pending.
