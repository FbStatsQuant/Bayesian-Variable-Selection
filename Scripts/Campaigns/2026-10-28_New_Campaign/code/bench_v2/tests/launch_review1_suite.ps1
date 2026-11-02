$testRoot = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/tests'
$env:TEMP = "$testRoot/local_tmp"
$env:TMP = $env:TEMP
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
Remove-Item Env:BENCH_V2_LOCAL_TEST -ErrorAction SilentlyContinue
$run = Start-Process -FilePath 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' -ArgumentList @('--vanilla', "`"$testRoot/run_review1_suite.R`"") -RedirectStandardOutput "$testRoot/review1_suite.log" -RedirectStandardError "$testRoot/review1_suite.stderr.log" -WindowStyle Hidden -PassThru -Wait
exit $run.ExitCode
