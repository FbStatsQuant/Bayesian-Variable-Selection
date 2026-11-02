$a = 'C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks'
$b = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$roots = @((Join-Path $b 'F1_Lasso'), (Join-Path $b 'F2_ElasticNet'), (Join-Path $b 'F3_AdaptiveLasso'))
Get-ChildItem -File -Recurse -LiteralPath $roots | ForEach-Object {
  $rel = $_.FullName.Substring($b.Length + 1).Replace('\','/')
  $other = Join-Path $a $rel
  if (Test-Path -LiteralPath $other) {
    $h = (Get-FileHash -LiteralPath $other -Algorithm SHA256).Hash.ToLower()
    $v = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower()
    '{0} | {1} | {2} | {3}' -f $rel, $h, $v, ($h -eq $v)
  }
}
