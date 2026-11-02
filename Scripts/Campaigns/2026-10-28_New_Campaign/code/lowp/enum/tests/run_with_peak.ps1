# run_with_peak.ps1 -- run an R script in Rterm.exe (the R process itself, not the Rscript launcher) and report its peak
# working set (PeakWorkingSet64 polled every 50 ms until exit; the peak is cumulative so the last poll is the peak) and wall time.
param([string]$Script, [string]$ScriptArgs = "")
$rt = "C:/Program Files/R/R-4.4.1/bin/x64/Rterm.exe"
$p = Start-Process -FilePath $rt -ArgumentList @("--vanilla", "--quiet", "-f", "`"$Script`"", "--args", $ScriptArgs) -PassThru -NoNewWindow
$peak = 0; $sw = [Diagnostics.Stopwatch]::StartNew()
while (-not $p.HasExited) { try { $p.Refresh(); if ($p.PeakWorkingSet64 -gt $peak) { $peak = $p.PeakWorkingSet64 } } catch {}; Start-Sleep -Milliseconds 50 }
$sw.Stop()
"PEAK_WORKING_SET_MB={0:N1} PROCESS_WALL_S={1:N1}" -f ($peak / 1MB), $sw.Elapsed.TotalSeconds
