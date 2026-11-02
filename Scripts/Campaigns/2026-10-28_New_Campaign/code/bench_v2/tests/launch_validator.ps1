$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'repro/controlled_2a8362b2f348'
$rscript = 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe'
$env:TEMP = Join-Path $root 'tests/local_tmp'
$env:TMP = $env:TEMP
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
if (Get-Process -Id 36468 -ErrorAction SilentlyContinue) { Wait-Process -Id 36468 }
while (!(Test-Path -LiteralPath (Join-Path $out 'runner.exit'))) {
  $controllerFile = Join-Path $out 'controller.pid'
  $controllerId = if (Test-Path -LiteralPath $controllerFile) { [int](Get-Content -LiteralPath $controllerFile -Raw) } else { 0 }
  if ($controllerId -gt 0 -and !(Get-Process -Id $controllerId -ErrorAction SilentlyContinue)) {
    [IO.File]::WriteAllText((Join-Path $out 'validator.exit'), 'controller_exited_before_runner')
    exit 1
  }
  Start-Sleep -Seconds 5
}
if ((Get-Content -LiteralPath (Join-Path $out 'runner.exit') -Raw).Trim() -ne '0') {
  [IO.File]::WriteAllText((Join-Path $out 'validator.exit'), 'runner_failed')
  exit 1
}
$pair = Join-Path $root 'tests/compare_f1_nointercept.R'
$p = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $pair + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'F1_nointercept_paired.log') -RedirectStandardError (Join-Path $out 'F1_nointercept_paired.stderr.log')
$null = $p.Handle
$p.WaitForExit()
[IO.File]::WriteAllText((Join-Path $out 'F1_nointercept_paired.exit'), [string]$p.ExitCode)
$validator = Join-Path $root 'F3_AdaptiveLasso/tests/validate_outputs.R'
$results = Join-Path $root 'tests/runner_output/results/v2_local_e2e'
$p = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $validator + '"'), '--results', ('"' + $results + '"'), '--expect', '1') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'validator.log') -RedirectStandardError (Join-Path $out 'validator.stderr.log')
$null = $p.Handle
$p.WaitForExit()
[IO.File]::WriteAllText((Join-Path $out 'validator.exit'), [string]$p.ExitCode)
$controls = Join-Path $root 'tests/validator_negative_controls.R'
$p = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $controls + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'validator_controls.log') -RedirectStandardError (Join-Path $out 'validator_controls.stderr.log')
$null = $p.Handle
$p.WaitForExit()
[IO.File]::WriteAllText((Join-Path $out 'validator_controls.exit'), [string]$p.ExitCode)
