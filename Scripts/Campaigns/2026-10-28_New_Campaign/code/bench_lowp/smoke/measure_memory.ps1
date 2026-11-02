$bench = (Resolve-Path (Join-Path $PSScriptRoot '../run_bench_case.R')).Path
$root = 'C:/Users/felip/AppData/Local/Temp/lowp_work/bench_smoke'
$env:LOWP_SMOKE_ALLOW_VERSION_MISMATCH = '1'
$rows = foreach ($id in @('F1','F2','F3','F4','F5','A1','A2','A3')) {
  $args = @('--vanilla', ('--file="' + $bench + '"'), '--args', ('"' + $root + '"'), 'memory', 'p0020_S1_r001', 'c100', $id)
  $p = Start-Process -FilePath 'C:/Program Files/R/R-4.4.1/bin/x64/Rterm.exe' -ArgumentList $args -PassThru -WindowStyle Hidden -RedirectStandardOutput "$root/memory_$id.log" -RedirectStandardError "$root/memory_${id}_err.log"
  $peak = 0
  do { try { $p.Refresh(); $peak = [Math]::Max($peak, $p.PeakWorkingSet64) } catch {}; if (!$p.HasExited) { Start-Sleep -Milliseconds 100 } } while (!$p.HasExited)
  $p.WaitForExit()
  [pscustomobject]@{method=$id; pid=$p.Id; peak_MB=[math]::Round($peak/1MB,2); exit=$p.ExitCode}
}
$rows | Export-Csv "$root/memory.csv" -NoTypeInformation
$rows | Format-Table