param(
  [Parameter(Mandatory=$true)][string]$Script,
  [Parameter(ValueFromRemainingArguments=$true)][string[]]$RArgs
)
$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$tmp = Join-Path $root 'tests/local_tmp'
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$env:TEMP = $tmp
$env:TMP = $tmp
& 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' --vanilla $Script @RArgs
exit $LASTEXITCODE
