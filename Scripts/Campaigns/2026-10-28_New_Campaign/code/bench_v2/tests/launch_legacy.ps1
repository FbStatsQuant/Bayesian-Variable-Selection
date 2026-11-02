$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'tests/legacy_runs'
$tmp = Join-Path $root 'tests/local_tmp'
New-Item -ItemType Directory -Force -Path $out,$tmp | Out-Null
$env:TEMP = $tmp
$env:TMP = $tmp
$env:BENCH_V2_LOCAL_TEST = '1'
$env:BENCH_LIB = 'C:/Users/felip/AppData/Local/R/win-library/4.4'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
while (Get-Process -Id 36468 -ErrorAction SilentlyContinue) {
  $completed = @(Get-ChildItem -LiteralPath (Join-Path $root 'repro') -Filter '*.rds').Count
  $active = @(Get-CimInstance Win32_Process -Filter 'ParentProcessId=36468' |
    Where-Object { $_.Name -eq 'Rscript.exe' }).Count
  $runnerExit = Join-Path $root 'repro/controlled_2a8362b2f348/runner.exit'
  if ($completed -ge 13 -and $active -le 11 -and (Test-Path -LiteralPath $runnerExit)) { break }
  Start-Sleep -Seconds 20
}
$rscript = 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe'
$inputs = 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs'
foreach ($method in @('F1_Lasso','F2_ElasticNet')) {
  $code = Join-Path $root $method
  $name = if ($method -eq 'F1_Lasso') { 'test_F1_lasso.R' } else { 'test_F2_enet.R' }
  $test = Join-Path (Join-Path $code 'tests') $name
  $destination = Join-Path $out $method
  $p = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $test + '"'), ('"' + $code + '"'), ('"' + $inputs + '"'), ('"' + $destination + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out "$method.log") -RedirectStandardError (Join-Path $out "$method.stderr.log")
  $null = $p.Handle
  $p.WaitForExit()
  [IO.File]::WriteAllText((Join-Path $out "$method.exit"), [string]$p.ExitCode)
}
