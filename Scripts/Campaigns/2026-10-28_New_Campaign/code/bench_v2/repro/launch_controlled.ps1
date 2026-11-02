$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'repro/controlled_2a8362b2f348'
$rscript = 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$tmp = Join-Path $root 'tests/local_tmp'
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$env:TEMP = $tmp
$env:TMP = $tmp
$limit = [Math]::Max(1, [Environment]::ProcessorCount - 4)
New-Item -ItemType Directory -Force -Path $out | Out-Null
[IO.File]::WriteAllText((Join-Path $out 'controller.pid'), [string]$PID)
while (Get-Process -Id 36468 -ErrorAction SilentlyContinue) {
  $completed = @(Get-ChildItem -LiteralPath (Join-Path $root 'repro') -Filter '*.rds').Count
  $active = @(Get-CimInstance Win32_Process -Filter 'ParentProcessId=36468' |
    Where-Object { $_.Name -eq 'Rscript.exe' }).Count
  if ($completed -ge 13 -and $active -le 11) { break }
  Start-Sleep -Seconds 20
}
if (!(Test-Path -LiteralPath (Join-Path $out 'runner.exit'))) {
  $runner = Join-Path $root 'tests/run_local_runner.R'
  $ep = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $runner + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'runner.log') -RedirectStandardError (Join-Path $out 'runner.stderr.log')
  $null = $ep.Handle
  $ep.WaitForExit()
  [IO.File]::WriteAllText((Join-Path $out 'runner.exit'), [string]$ep.ExitCode)
}
$script = Join-Path $root 'repro/run_controlled_case.R'
$jobs = @()
$pending = @()
foreach ($p in @('p0500','p1000')) {
  foreach ($s in 1..6) {
    foreach ($scale in @('c100','c050')) {
      $pending += [pscustomobject]@{id="dev_${p}_S${s}_r001"; scale=$scale}
    }
  }
}
while ($pending.Count -gt 0 -or $jobs.Count -gt 0) {
  $originalRunning = $null -ne (Get-Process -Id 36468 -ErrorAction SilentlyContinue)
  if ($originalRunning) {
    $activeOriginal = @(Get-CimInstance Win32_Process -Filter 'ParentProcessId=36468' |
      Where-Object { $_.Name -eq 'Rscript.exe' }).Count
    $limit = [Math]::Max(0, [Environment]::ProcessorCount - 3 - $activeOriginal)
  } elseif (Test-Path -LiteralPath (Join-Path $out 'validator_controls.exit')) {
    $limit = [Math]::Max(1, [Environment]::ProcessorCount - 3)
  } else {
    $limit = [Math]::Max(1, [Environment]::ProcessorCount - 4)
  }
  while ($pending.Count -gt 0 -and $jobs.Count -lt $limit) {
    $pick = -1
    for ($j = 0; $j -lt $pending.Count; $j++) {
      $candidate = $pending[$j]
      $stem = "$($candidate.id)_$($candidate.scale)"
      if (!$originalRunning -or
          ((Test-Path -LiteralPath (Join-Path $root "repro/$stem.rds")) -and
           (Test-Path -LiteralPath (Join-Path $root "repro/$stem.exit")))) { $pick = $j; break }
    }
    if ($pick -lt 0) { break }
    $case = $pending[$pick]
    $pending = @($pending | Where-Object { $_ -ne $case })
    $name = "$($case.id)_$($case.scale)"
    $proc = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $script + '"'), $case.id, $case.scale) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out "$name.log") -RedirectStandardError (Join-Path $out "$name.stderr.log")
    $null = $proc.Handle
    $jobs += [pscustomobject]@{process=$proc; exitFile=(Join-Path $out "$name.exit")}
  }
  $running = @()
  foreach ($job in $jobs) {
    if ($job.process.HasExited) { $job.process.WaitForExit(); [IO.File]::WriteAllText($job.exitFile, [string]$job.process.ExitCode) }
    else { $running += $job }
  }
  $jobs = $running
  if ($pending.Count -gt 0 -or $jobs.Count -gt 0) { Start-Sleep -Seconds 5 }
}
