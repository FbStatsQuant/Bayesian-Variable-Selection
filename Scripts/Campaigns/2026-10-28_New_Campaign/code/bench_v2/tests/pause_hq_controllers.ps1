$signature = @'
using System;
using System.Runtime.InteropServices;
public static class BenchV2ProcessPause {
  [DllImport("ntdll.dll")] public static extern int NtSuspendProcess(IntPtr handle);
}
'@
Add-Type -TypeDefinition $signature
foreach ($id in @(20212, 20864, 40968, 10604)) {
  $process = Get-Process -Id $id -ErrorAction SilentlyContinue
  if ($null -eq $process) { Write-Output "PID $id absent"; continue }
  $status = [BenchV2ProcessPause]::NtSuspendProcess($process.Handle)
  Write-Output "PID $id suspend status $status"
}
