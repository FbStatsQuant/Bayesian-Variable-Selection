$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'tests/legacy_runs'
$tmp = Join-Path $root 'tests/local_tmp'
$env:TEMP = $tmp
$env:TMP = $tmp
$env:BENCH_V2_LOCAL_TEST = '1'
$env:BENCH_LIB = 'C:/Users/felip/AppData/Local/R/win-library/4.4'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
if (Get-Process -Id 36104 -ErrorAction SilentlyContinue) { Wait-Process -Id 36104 }
$rscript = 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe'
$code = Join-Path $root 'F1_Lasso'
$test = Join-Path $code 'tests/test_F1_lasso.R'
$inputs = 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs'
$dest = Join-Path $out 'F1_Lasso_reclassified'
$p = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $test + '"'), ('"' + $code + '"'), ('"' + $inputs + '"'), ('"' + $dest + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'F1_reclassified.log') -RedirectStandardError (Join-Path $out 'F1_reclassified.stderr.log')
$null = $p.Handle
$p.WaitForExit()
[IO.File]::WriteAllText((Join-Path $out 'F1_reclassified.exit'), [string]$p.ExitCode)
