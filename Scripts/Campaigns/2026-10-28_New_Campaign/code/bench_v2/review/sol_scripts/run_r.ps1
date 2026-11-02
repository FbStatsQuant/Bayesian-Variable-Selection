param([string]$Name)
$reviewRoot='C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review'
New-Item -ItemType Directory -Force -Path "$reviewRoot/sol_scripts/tmp" | Out-Null
$env:TEMP="$reviewRoot/sol_scripts/tmp"
$env:TMP=$env:TEMP
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
& 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' --vanilla "$reviewRoot/sol_scripts/$Name.R" 1> "$reviewRoot/sol_scripts/$Name.log" 2> "$reviewRoot/sol_scripts/$Name.stderr.log"
$rExit=$LASTEXITCODE
Set-Content -LiteralPath "$reviewRoot/sol_scripts/$Name.exit" -Value $rExit
exit $rExit
