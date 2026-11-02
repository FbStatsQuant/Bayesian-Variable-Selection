$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'repro/controlled_2a8362b2f348'
$rscript = 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe'
$env:TEMP = Join-Path $root 'tests/local_tmp'
$env:TMP = $env:TEMP
$env:BENCH_V2_LOCAL_TEST = '1'
$env:BENCH_LIB = 'C:/Users/felip/AppData/Local/R/win-library/4.4'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
[IO.File]::WriteAllText((Join-Path $out 'capped_controller.pid'), [string]$PID)
$inputs = 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs'
$pending = @(
  [pscustomobject]@{name='verify_initial'; script=(Join-Path $root 'repro/verify_capped_outputs.R'); args=@(); kind='verify'},
  [pscustomobject]@{name='F1_nointercept_paired_capped'; script=(Join-Path $root 'tests/compare_f1_nointercept.R'); args=@(); kind='test'},
  [pscustomobject]@{name='mutation_suite_capped'; script=(Join-Path $root 'tests/run_all_tests.R'); args=@(); kind='test'},
  [pscustomobject]@{name='F1_legacy_capped'; script=(Join-Path $root 'F1_Lasso/tests/test_F1_lasso.R'); args=@((Join-Path $root 'F1_Lasso'),$inputs,(Join-Path $root 'tests/legacy_runs/F1_capped')); kind='test'}
)
foreach ($p in @('p0500','p1000')) {
  foreach ($s in 1..6) {
    foreach ($scale in @('c100','c050')) {
      $id = "dev_${p}_S${s}_r001"
      $pending += [pscustomobject]@{name="${id}_$scale"; script=(Join-Path $root 'repro/run_controlled_case.R'); args=@($id,$scale); kind='case'}
    }
  }
}
$jobs = @()
while ($pending.Count -gt 0 -or $jobs.Count -gt 0) {
  $remaining = @()
  foreach ($j in $jobs) {
    if ($j.process.HasExited) {
      $j.process.WaitForExit()
      [IO.File]::WriteAllText((Join-Path $out "$($j.name).capped_exit"), [string]$j.process.ExitCode)
    } else { $remaining += $j }
  }
  $jobs = $remaining
  $old = @(Get-CimInstance Win32_Process -Filter "Name='Rscript.exe'" | Where-Object { $_.ParentProcessId -in @(36468,20212,36104) })
  $used = 0
  foreach ($j in $jobs) { $used += $j.slots }
  $legacyReserve = if (@($old | Where-Object { $_.ParentProcessId -eq 36104 }).Count -gt 0) { 1 } else { 0 }
  $capacity = [Math]::Max(0, 4 - $old.Count - $legacyReserve - $used)
  while ($capacity -gt 0 -and $pending.Count -gt 0) {
    $pick = -1
    for ($i=0; $i -lt $pending.Count; $i++) {
      $item = $pending[$i]
      $slots = if ($item.name -in @('mutation_suite_capped','F1_legacy_capped')) { 2 } else { 1 }
      if ($slots -gt $capacity) { continue }
      if ($item.kind -ne 'case') { $pick = $i; break }
      $name = $item.name
      $rds = Join-Path $out "$name.rds"
      $sexit = Join-Path $out "$name.script_exit"
      $log = Join-Path $out "$name.log"
      $runningOld = @($old | Where-Object { $_.CommandLine -like "*$($item.args[0])*" -and $_.CommandLine -like "*$($item.args[1])*" }).Count -gt 0
      if ($runningOld) { continue }
      if ((Test-Path -LiteralPath $rds) -and (Test-Path -LiteralPath $sexit) -and (Test-Path -LiteralPath $log) -and ((Get-Content -Raw -LiteralPath $sexit).Trim() -eq '0')) {
        $lines = Get-Content -LiteralPath $log
        if (($lines -match '^finish ').Count -gt 0 -and ($lines -match 'FATAL:|Error:|Execution halted').Count -eq 0) {
          $pending = @($pending | Where-Object { $_ -ne $item })
          $pick = -2; break
        }
      }
      $orig = Join-Path $root "repro/$name.rds"
      if (Test-Path -LiteralPath $orig) { $pick = $i; break }
    }
    if ($pick -eq -2) { continue }
    if ($pick -lt 0) { break }
    $item = $pending[$pick]
    $pending = @($pending | Where-Object { $_ -ne $item })
    $quoted = @('--vanilla', ('"' + $item.script + '"'))
    foreach ($arg in $item.args) { $quoted += ('"' + $arg + '"') }
    $proc = Start-Process -FilePath $rscript -ArgumentList $quoted -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out "$($item.name).log") -RedirectStandardError (Join-Path $out "$($item.name).stderr.log")
    $null = $proc.Handle
    $slots = if ($item.name -in @('mutation_suite_capped','F1_legacy_capped')) { 2 } else { 1 }
    $jobs += [pscustomobject]@{name=$item.name; process=$proc; slots=$slots}
    $capacity -= $slots
  }
  if ($pending.Count -gt 0 -or $jobs.Count -gt 0) { Start-Sleep -Seconds 10 }
}
[IO.File]::WriteAllText((Join-Path $out 'capped_controller.done'), (Get-Date).ToUniversalTime().ToString('o'))
