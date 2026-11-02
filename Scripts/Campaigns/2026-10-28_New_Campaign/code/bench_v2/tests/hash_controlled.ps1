$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$files = @('repro/run_controlled_case.R','repro/launch_controlled.ps1','tests/run_local_runner.R',
  'tests/launch_validator.ps1','tests/validator_negative_controls.R','tests/compare_f1_nointercept.R',
  'tests/launch_legacy.ps1','tests/recheck_f1.ps1','tests/local_glmnet_compat.R',
  'F1_Lasso/tests/test_F1_lasso.R','F2_ElasticNet/tests/test_F2_enet.R',
  'F3_AdaptiveLasso/tests/test_F3_alasso.R','F3_AdaptiveLasso/tests/test_F3_v2_canaries.R',
  'F3_AdaptiveLasso/tests/validate_outputs.R','repro/launch_summary.ps1')
$files | ForEach-Object {
  '{0}  {1}' -f (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root $_)).Hash.ToLower(), $_
}
