$CAMP = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
$V2 = "$CAMP/code/bench_v2"
$SNAP = "$V2/repro/snapshot_2a8362b2f348"
$DEP = 'C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks'
$LOWP = "$CAMP/code/bench_lowp"
$out = "$V2/review/checker/check1_hashes.txt"
function Sha($p) { if (Test-Path -LiteralPath $p) { (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLower() } else { 'MISSING' } }
$lines = @()
$files = @()
foreach ($m in 'F1_Lasso','F2_ElasticNet','F3_AdaptiveLasso') {
  $files += "$m/config.R"; $files += "$m/common.R"; $files += "$m/run_case.R"
  $files += "$m/methods/glmnet_helpers.R"
  $files += "$m/methods/" + $(if ($m -eq 'F1_Lasso') {'fit_F1_lasso.R'} elseif ($m -eq 'F2_ElasticNet') {'fit_F2_enet.R'} else {'fit_F3_alasso.R'})
}
$lines += "== A. v2 vs snapshot_2a8362b2f348 (15 files) and v2 vs deployed =="
$lines += "file | v2 | snap==v2 | dep==v2 | v2sha"
$nsnap = 0; $ndepeq = 0
foreach ($f in $files) {
  $h = Sha "$V2/$f"; $s = Sha "$SNAP/$f"; $d = Sha "$DEP/$f"
  $se = ($h -eq $s); if ($se) { $nsnap++ }
  $de = ($h -eq $d); if ($de) { $ndepeq++ }
  $lines += "$f | $(($h).Substring(0,12)) | $se | $de | $h"
}
$lines += "snapshot-equal: $nsnap / $($files.Count); deployed-equal: $ndepeq"
$lines += ""
$lines += "== B. deployed hashes (current on disk) vs BASELINE_SHA256.txt deployed column =="
$base = Get-Content -LiteralPath "$V2/BASELINE_SHA256.txt" | Where-Object { $_ -match '^F[123]_\S+ \| [0-9a-f]{64} \|' }
foreach ($b in $base) {
  $p = $b -split ' \| '
  $f = $p[0].Trim(); $dh = $p[1].Trim(); $vh = $p[2].Trim(); $ident = $p[3].Trim()
  $ondep = Sha "$DEP/$f"; $onv2 = Sha "$V2/$f"
  $lines += "$f | dep_disk==baseline_dep: $($ondep -eq $dh) | v2_disk==baseline_v2: $($onv2 -eq $vh) | claims_identical=$ident | actual_dep==v2: $($ondep -eq $onv2)"
}
$lines += ""
$lines += "== C. bench_lowp copies vs bench_v2 =="
$map = @(
  @('R/methods/fit_F1_lasso.R','F1_Lasso/methods/fit_F1_lasso.R'),
  @('R/methods/fit_F2_enet.R','F2_ElasticNet/methods/fit_F2_enet.R'),
  @('R/methods/fit_F3_alasso.R','F3_AdaptiveLasso/methods/fit_F3_alasso.R'),
  @('R/methods/glmnet_helpers_F1.R','F1_Lasso/methods/glmnet_helpers.R'),
  @('R/methods/glmnet_helpers_F2.R','F2_ElasticNet/methods/glmnet_helpers.R'),
  @('R/methods/glmnet_helpers_F3.R','F3_AdaptiveLasso/methods/glmnet_helpers.R'),
  @('R/production_helpers/common_F1.R','F1_Lasso/common.R'),
  @('R/production_helpers/common_F2.R','F2_ElasticNet/common.R'),
  @('R/production_helpers/common_F3.R','F3_AdaptiveLasso/common.R')
)
foreach ($m in $map) {
  $a = Sha "$LOWP/$($m[0])"; $b = Sha "$V2/$($m[1])"
  $lines += "$($m[0]) == $($m[1]) : $($a -eq $b) ($($a.Substring(0,12)) / $($b.Substring(0,12)))"
}
$lines += ""
$lines += "== D. CHANGED_SHA256.txt current column vs disk =="
$ch = Get-Content -LiteralPath "$V2/lowp_port/CHANGED_SHA256.txt" | Where-Object { $_ -notmatch '^#' -and $_.Trim() }
foreach ($c in $ch) {
  $p = $c -split '\s+'
  $cur = Sha "$LOWP/$($p[0])"
  $lines += "$($p[0]) | disk==claimed_current: $($cur -eq $p[2])"
}
$lines | Set-Content -LiteralPath $out -Encoding utf8
Write-Output "done"
