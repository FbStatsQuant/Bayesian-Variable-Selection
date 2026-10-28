# Review round 2 finding closure (R4 implementation)

All four findings addressed by code and passing regressions; NEW independent review of these hashes is pending. This is not approval from the prior REQUEST CHANGES report.

Clean evidence: C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\H_2026-10-22_smcbvs_v3_deploy\D_analysis\pipeline\validation\local_20261022T204616_272585Z

| Finding | Change | Saved rejecting adapter cases |
|---|---|---|
| F1 | Reconstruct original-index primary PIPs through a strict kept/dropped partition; compare native HPM/MPM and retained/exported copies before truth access. | hpm_disagrees, pip_disagrees, bad_preprocessing_map, wrong_native_pip_names |
| F2 | Require fit$status = record native_status = CSV v3_status. Sole documented exception is before-core adapter_error with fit=NULL, nonempty error, unavailable estimates; retained-fit adapter errors fail closed. | native_status_disagrees, reverse_failure_status, degenerate_status_disagrees |
| F3 | Require actual branch payload (SMC stages, log_Z/log_Z_r, four streams, PIPs, timings and bound annotation; exact payload without fabricated SMC data); compare all eight represented native JSON fields. | missing_native_payload, missing_native_pip, missing_native_stage, missing_island_evidence, missing_native_streams, missing_bound_label, native_json_disagrees, json_cut_group_count, json_cut_group_components, json_local_limit, json_local_certified, json_global_certified, json_near_tie_truncated |
| F4 | Compare failed HPM and actually returned PIP-derived MPM audits to native sources; distinguish unavailable NA from returned empty support. Positive and negative partial-MPM controls pass. | missing_failure_audit, changed_failure_audit, null_failure_as_NA, unavailable_failure_as_empty |

Additional native controls: 13; see suite/native_controls/native_control_checks.csv.
Each mutation refreshes CSV/RDS sidecars and fails with the specified native-integrity error. Invalid-native calls use a nonexistent truth directory, so reaching truth would fail the expected-error assertion.

Actual A dev p500/p1000: raw schema/native integrity PASS; legacy R-1 rejection EXPECTED; labelled D-owned adapted copies PASS with numeric-byte/attribute-identical native fit. Stage rows 587/769. No truth or production scoring. Eight original output files unchanged before/after and rechecked at freeze.
Legacy native log_Z_lower95 has no explicit heuristic label; only the D reference copy carries a clearly labelled separate R-1 annotation. No native evidence value is changed.
Actual updated A R-1 adapter integration and fresh independent review remain pending.
