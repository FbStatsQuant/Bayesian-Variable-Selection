param([Parameter(Mandatory=$true)][string]$Name,[Parameter(Mandatory=$true)][string]$Target,[string[]]$Extra=@())
$root = 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/lowp_port'
$active = @(Get-CimInstance Win32_Process -Filter "Name = 'Rscript.exe'" | Where-Object { $_.CommandLine -match 'bench_v2|bench_lowp' })
if ($active.Count -gt 10) { Write-Output "REFUSED: $($active.Count) campaign Rscript processes"; exit 1 }
$jobs = @(Get-CimInstance Win32_Process -Filter "Name = 'Rscript.exe'" | Where-Object { $_.CommandLine -match 'lowp_port[\\/]tests[\\/]entry.R' })
if ($jobs.Count -ge 4) { Write-Output 'REFUSED: W2 already has two jobs'; exit 1 }
$dir = Join-Path $root 'runs'
New-Item -ItemType Directory -Path $dir -Force | Out-Null
$tmp = Join-Path $root 'tmp'
New-Item -ItemType Directory -Path $tmp -Force | Out-Null
$env:TEMP = $tmp; $env:TMP = $tmp; $env:R_LIBS_USER = 'C:/Users/felip/AppData/Local/Temp/lowp_Rlib;C:/Users/felip/AppData/Local/R/win-library/4.4'
$marker = Join-Path $dir "$Name.script_exit"
if (Test-Path -LiteralPath $marker) { Write-Output 'REFUSED: marker already exists'; exit 1 }
$entry = Join-Path $root 'tests/entry.R'
$arg = @('--vanilla', ('"' + $entry + '"'), ('"' + $Target + '"'), ('"' + $marker + '"')) + @($Extra | ForEach-Object { '"' + $_ + '"' })
$proc = Start-Process -FilePath 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' -ArgumentList $arg -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $dir "$Name.log") -RedirectStandardError (Join-Path $dir "$Name.stderr.log")
Write-Output "STARTED $Name PID=$($proc.Id) campaign_processes_before=$($active.Count)"
