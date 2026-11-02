$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'repro/controlled_2a8362b2f348'
$pidFile = Join-Path $out 'controller.pid'
$controller = [int](Get-Content -LiteralPath $pidFile -Raw)
if (Get-Process -Id $controller -ErrorAction SilentlyContinue) { Wait-Process -Id $controller }
$rscript = 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe'
$env:TEMP = Join-Path $root 'tests/local_tmp'
$env:TMP = $env:TEMP
$script = Join-Path $root 'repro/summarise_controlled.R'
$p = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $script + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'summary.log') -RedirectStandardError (Join-Path $out 'summary.stderr.log')
$null = $p.Handle
$p.WaitForExit()
[IO.File]::WriteAllText((Join-Path $out 'summary.exit'), [string]$p.ExitCode)
