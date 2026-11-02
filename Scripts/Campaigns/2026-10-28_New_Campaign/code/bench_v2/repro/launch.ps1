$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro'
$rscript = 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe'
$script = Join-Path $root 'run_case.R'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$limit = [Math]::Max(1, [Environment]::ProcessorCount - 2)
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
  while ($pending.Count -gt 0 -and $jobs.Count -lt $limit) {
    $case = $pending[0]
    $pending = @($pending | Select-Object -Skip 1)
    $name = "$($case.id)_$($case.scale)"
    $stdout = Join-Path $root "$name.log"
    $stderr = Join-Path $root "$name.stderr.log"
    $exitFile = Join-Path $root "$name.exit"
    $proc = Start-Process -FilePath $rscript -ArgumentList @('--vanilla', ('"' + $script + '"'), $case.id, $case.scale) -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    $jobs += [pscustomobject]@{process=$proc; exitFile=$exitFile; name=$name}
  }
  $running = @()
  foreach ($job in $jobs) {
    if ($job.process.HasExited) {
      [IO.File]::WriteAllText($job.exitFile, [string]$job.process.ExitCode)
    } else { $running += $job }
  }
  $jobs = $running
  if ($jobs.Count -gt 0) { Start-Sleep -Seconds 5 }
}
