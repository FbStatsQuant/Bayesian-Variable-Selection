$reviewRoot='C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r3'
$env:TEMP="$reviewRoot/tmp"
$env:TMP=$env:TEMP
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
& python -B "$reviewRoot/check_python_integrity.py" 1> "$reviewRoot/check_python_integrity.log" 2> "$reviewRoot/check_python_integrity.stderr.log"
$pExit=$LASTEXITCODE
Set-Content -LiteralPath "$reviewRoot/check_python_integrity.exit" -Value $pExit
exit $pExit
