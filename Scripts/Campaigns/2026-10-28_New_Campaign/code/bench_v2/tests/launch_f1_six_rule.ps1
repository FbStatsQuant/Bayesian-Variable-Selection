$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'repro/controlled_2a8362b2f348'
$env:TEMP = Join-Path $root 'tests/local_tmp'
$env:TMP = $env:TEMP
$env:BENCH_V2_LOCAL_TEST = '1'
$env:BENCH_LIB = 'C:/Users/felip/AppData/Local/R/win-library/4.4'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$existing = @(Get-CimInstance Win32_Process -Filter "Name='Rscript.exe'" | Where-Object { $_.ParentProcessId -in @(20212,29376) })
if ($existing.Count -gt 1) { throw "W1 capacity unavailable: $($existing.Count) parent jobs" }
$script = Join-Path $root 'tests/run_local_f1_suite.R'
$code = Join-Path $root 'F1_Lasso'
$input = 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs'
$dest = Join-Path $root 'tests/legacy_runs/F1_six_rule'
$args = @('--vanilla', ('"' + $script + '"'), ('"' + $code + '"'), ('"' + $input + '"'), ('"' + $dest + '"'))
$proc = Start-Process -FilePath 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' -ArgumentList $args -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'F1_six_rule.log') -RedirectStandardError (Join-Path $out 'F1_six_rule.stderr.log')
$null = $proc.Handle
[IO.File]::WriteAllText((Join-Path $out 'F1_six_rule.pid'), [string]$proc.Id)
$proc.WaitForExit()
[IO.File]::WriteAllText((Join-Path $out 'F1_six_rule.exit'), [string]$proc.ExitCode)
