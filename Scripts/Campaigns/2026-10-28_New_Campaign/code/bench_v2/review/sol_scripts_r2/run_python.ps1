param([string]$Name)
$reviewRoot='C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONIOENCODING='utf-8'
$env:TEMP="$reviewRoot/tmp"
$env:TMP=$env:TEMP
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
py -3 -B "$reviewRoot/$Name.py" 1> "$reviewRoot/$Name.log" 2> "$reviewRoot/$Name.stderr.log"
$pExit=$LASTEXITCODE
Set-Content -LiteralPath "$reviewRoot/$Name.exit" -Value $pExit
exit $pExit
