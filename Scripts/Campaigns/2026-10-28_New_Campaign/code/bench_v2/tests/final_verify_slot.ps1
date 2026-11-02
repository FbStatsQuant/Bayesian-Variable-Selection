$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
$out = Join-Path $root 'repro/controlled_2a8362b2f348'
$env:TEMP = Join-Path $root 'tests/local_tmp'
$env:TMP = $env:TEMP
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$signature = @'
using System;
using System.Runtime.InteropServices;
public static class BenchV2FinalSlot {
  [DllImport("ntdll.dll")] public static extern int NtSuspendProcess(IntPtr handle);
  [DllImport("ntdll.dll")] public static extern int NtResumeProcess(IntPtr handle);
}
'@
Add-Type -TypeDefinition $signature
$suite = Get-Process -Id 39080 -ErrorAction Stop
if ([BenchV2FinalSlot]::NtSuspendProcess($suite.Handle) -ne 0) { throw 'suspend failed' }
try {
  $count = @(Get-Process -Name Rscript -ErrorAction SilentlyContinue).Count
  if ($count -gt 6) { throw "no safe capacity: $count Rscript processes" }
  $script = Join-Path $root 'repro/verify_capped_outputs.R'
  $proc = Start-Process -FilePath 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' -ArgumentList @('--vanilla', ('"' + $script + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'verify_final.log') -RedirectStandardError (Join-Path $out 'verify_final.stderr.log')
  $null = $proc.Handle
  $proc.WaitForExit()
  [IO.File]::WriteAllText((Join-Path $out 'verify_final.exit'), [string]$proc.ExitCode)
} finally {
  $null = [BenchV2FinalSlot]::NtResumeProcess($suite.Handle)
}
