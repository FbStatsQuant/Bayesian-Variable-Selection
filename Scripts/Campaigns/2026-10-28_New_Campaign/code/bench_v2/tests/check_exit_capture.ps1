$p = Start-Process -FilePath 'C:/Windows/System32/cmd.exe' -ArgumentList @('/c','exit','7') -WindowStyle Hidden -PassThru
$null = $p.Handle
$p.WaitForExit()
if ($p.ExitCode -ne 7) { throw "expected exit 7, observed $($p.ExitCode)" }
Write-Output "exit capture PASS: $($p.ExitCode)"
