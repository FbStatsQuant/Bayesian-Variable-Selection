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
public static class BenchV2MutationSlot {
  [DllImport("ntdll.dll")] public static extern int NtSuspendProcess(IntPtr handle);
  [DllImport("ntdll.dll")] public static extern int NtResumeProcess(IntPtr handle);
}
'@
Add-Type -TypeDefinition $signature
$controller = Get-Process -Id 29376 -ErrorAction Stop
if ([BenchV2MutationSlot]::NtSuspendProcess($controller.Handle) -ne 0) { throw 'suspend failed' }
try {
  $old = @(Get-CimInstance Win32_Process -Filter "Name='Rscript.exe'" | Where-Object { $_.ParentProcessId -in @(20212,29376) })
  if ($old.Count -gt 3) { throw "no W1 capacity: $($old.Count) active" }
  $script = Join-Path $root 'tests/mutation_only.R'
  $proc = Start-Process -FilePath 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' -ArgumentList @('--vanilla', ('"' + $script + '"')) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $out 'mutation_only.log') -RedirectStandardError (Join-Path $out 'mutation_only.stderr.log')
  $null = $proc.Handle
  $proc.WaitForExit()
  [IO.File]::WriteAllText((Join-Path $out 'mutation_only.exit'), [string]$proc.ExitCode)
} finally {
  $null = [BenchV2MutationSlot]::NtResumeProcess($controller.Handle)
}
