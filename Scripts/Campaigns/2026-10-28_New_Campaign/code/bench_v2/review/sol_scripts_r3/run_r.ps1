$reviewRoot='C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r3'
New-Item -ItemType Directory -Force -Path "$reviewRoot/tmp" | Out-Null
$env:TEMP="$reviewRoot/tmp"
$env:TMP=$env:TEMP
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
& 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' --vanilla "$reviewRoot/check_narrow.R" 1> "$reviewRoot/check_narrow.log" 2> "$reviewRoot/check_narrow.stderr.log"
$rExit=$LASTEXITCODE
Set-Content -LiteralPath "$reviewRoot/check_narrow.exit" -Value $rExit
exit $rExit
