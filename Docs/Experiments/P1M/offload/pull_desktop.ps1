<#
pull_desktop.ps1 -- SMC Engineering offload, PC side (OFFLOAD.md step 3; desktop = primary, laptop = mirror).
One pull = ONE ssh connection to Owls: our verified-unit list goes up on stdin, a tar of the next pending units
(oldest first, at most -MaxPullGB) comes back on stdout. Each unit carries SHA256SUMS; every file is verified with
Get-FileHash before the unit is moved into <DestRoot>\records\. Nothing is ever deleted on Owls or NOTS by this script.

Guards: skips 03:00-03:15 Central (BNP backups); one pull at a time (lock file); refuses if our data plus this pull would
exceed -MaxUsePct of the drive or leave less than -MinFreePct free.
Exit codes: 0 ok / nothing to do / skipped, 3 disk guard refusal, 4 ssh failed, 5 tar failed, 6 a unit failed verification,
7 unexpected error.
Usage: powershell -NoProfile -ExecutionPolicy Bypass -File pull_desktop.ps1 [-DestRoot D:\SMC_Engineering_Department]
#>
param(
  [string]$SshHost   = 'smc-eng-owls',
  [string]$DestRoot  = 'D:\SMC_Engineering_Department',
  [string]$Client    = 'desktop',
  [int]$MaxPullGB    = 50,
  [int]$MaxUsePct    = 70,
  [int]$MinFreePct   = 15,
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$records  = Join-Path $DestRoot 'records'
$incoming = Join-Path $DestRoot 'incoming'
$quar     = Join-Path $DestRoot 'quarantine'
$logs     = Join-Path $DestRoot 'logs'
New-Item -ItemType Directory -Force -Path $records, $incoming, $quar, $logs | Out-Null
$logFile = Join-Path $logs ('pull_' + (Get-Date -Format 'yyyyMMdd') + '.log')
function Log([string]$m) { $l = (Get-Date -Format 's') + ' ' + $m; Add-Content -Path $logFile -Value $l; Write-Output $l }

# 1. BNP backup window (03:00-03:15 US Central): skip
$ct = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Central Standard Time')
if ($ct.Hour -eq 3 -and $ct.Minute -lt 15) { Log 'skip: BNP backup window (03:00-03:15 CT)'; exit 0 }

# 2. one pull at a time
$lockPath = Join-Path $DestRoot 'pull.lock'
try { $lock = [System.IO.File]::Open($lockPath, 'OpenOrCreate', 'ReadWrite', 'None') }
catch { Log 'skip: another pull is running'; exit 0 }

$script:stage = $null; $script:tar = $null
function Invoke-Pull {
  $rc = 0
  # 3. disk guard (our data = everything under DestRoot)
  $drive = Get-PSDrive -Name ((Get-Item $DestRoot).PSDrive.Name)
  $total = [double]($drive.Used + $drive.Free)
  $ours  = (Get-ChildItem $DestRoot -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
  if (-not $ours) { $ours = 0 }
  $cap = [double]$MaxPullGB * 1GB
  if (($ours + $cap) -gt ($MaxUsePct / 100.0) * $total) { Log ("refuse: our data {0:N1} GB + pull cap {1} GB > {2}% of the drive" -f ($ours/1GB), $MaxPullGB, $MaxUsePct); return 3 }
  if (($drive.Free - $cap) -lt ($MinFreePct / 100.0) * $total) { Log ("refuse: free {0:N1} GB - pull cap would leave < {1}% free" -f ($drive.Free/1GB), $MinFreePct); return 3 }

  # 4. the pull: one ssh connection (cmd.exe redirection keeps the tar byte-exact)
  $have = Join-Path $DestRoot 'verified_units.txt'
  if (-not (Test-Path $have)) { New-Item -ItemType File -Path $have | Out-Null }
  $stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
  $tar    = Join-Path $incoming "pull_$stamp.tar"; $script:tar = $tar
  $remote = "bash /home/fb31/Bayesian-Variable-Selection/_local/engineering/crews/offload/serve_pull.sh $Client $MaxPullGB"
  if ($DryRun) { Log "dry run: would run ssh $SshHost `"$remote`" < $have > $tar"; return 0 }
  $bat = Join-Path $incoming "pull_$stamp.cmd"
  Set-Content -Path $bat -Encoding ASCII -Value @(
    '@echo off',
    ('ssh -o BatchMode=yes -o ConnectTimeout=30 -o ServerAliveInterval=30 ' + $SshHost + ' "' + $remote + '" < "' + $have + '" > "' + $tar + '"'),
    'exit /b %ERRORLEVEL%')
  & cmd.exe /d /c $bat
  $sshrc = $LASTEXITCODE
  Remove-Item $bat -ErrorAction SilentlyContinue
  if ($sshrc -ne 0) { Log "error: ssh exit $sshrc"; Remove-Item $tar -ErrorAction SilentlyContinue; return 4 }

  # 5. unpack into a staging folder
  $stage = Join-Path $incoming "x_$stamp"; $script:stage = $stage
  New-Item -ItemType Directory -Path $stage | Out-Null
  & tar.exe -xf $tar -C $stage
  if ($LASTEXITCODE -ne 0) { Log "error: tar exit $LASTEXITCODE"; return 5 }

  # 6. verify each unit (a folder holding SHA256SUMS), then move it into records\ and record it
  # top-level units only: a SHA256SUMS nested inside another unit is that unit's DATA, not a unit (fix 2026-11-18)
  $all = @(Get-ChildItem $stage -Recurse -File -Filter 'SHA256SUMS' | ForEach-Object { $_.Directory.FullName } | Sort-Object Length)
  $units = @()
  foreach ($c in $all) { if (-not ($units | Where-Object { $c.StartsWith($_ + '\') })) { $units += $c } }
  if ($units.Count -eq 0) { Log 'nothing pending' }
  foreach ($u in $units) {
    if (-not (Test-Path -LiteralPath (Join-Path $u 'SHA256SUMS'))) { Log "skip: $u vanished"; continue }
    $rel = $u.Substring($stage.Length + 1)
    $ok = $true; $nfiles = 0; $bytes = 0
    foreach ($line in Get-Content (Join-Path $u 'SHA256SUMS')) {
      if ($line -notmatch '^([0-9a-fA-F]{64}) [ *](.+)$') { continue }
      $h = $Matches[1].ToLower(); $f = Join-Path $u ($Matches[2] -replace '/', '\')
      if (-not (Test-Path -LiteralPath $f)) { $ok = $false; Log "FAIL $rel missing $($Matches[2])"; break }
      if ((Get-FileHash -LiteralPath $f -Algorithm SHA256).Hash.ToLower() -ne $h) { $ok = $false; Log "FAIL $rel hash $($Matches[2])"; break }
      $nfiles++; $bytes += (Get-Item -LiteralPath $f).Length
    }
    if (-not $ok) {
      $q = Join-Path $quar ($rel -replace '\\', '__'); Move-Item -LiteralPath $u -Destination ($q + "_$stamp"); $rc = 6; continue
    }
    $dest = Join-Path $records $rel
    if (Test-Path -LiteralPath $dest) { $dest = $dest + "_dup_$stamp"; Log "note: $rel already present; kept as $dest" }
    New-Item -ItemType Directory -Force -Path (Split-Path $dest -Parent) | Out-Null
    Move-Item -LiteralPath $u -Destination $dest
    $relFwd = $rel -replace '\\', '/'
    @{ unit = $relFwd; files = $nfiles; bytes = $bytes; verified = (Get-Date -Format 's'); host = $env:COMPUTERNAME } |
      ConvertTo-Json | Set-Content -Path (Join-Path $dest 'verified.json') -Encoding UTF8
    Add-Content -Path $have -Value $relFwd
    Log ("verified {0}: {1} files, {2:N2} GB" -f $relFwd, $nfiles, ($bytes / 1GB))
  }
  return $rc
}

$rc = 0
try { $rc = Invoke-Pull | Select-Object -Last 1 }
catch { Log ("error: " + $_.Exception.Message); $rc = 7 }
finally {
  $stage = $script:stage; $tar = $script:tar
  if ($stage -and (Test-Path $stage)) { Remove-Item -Recurse -Force $stage -ErrorAction SilentlyContinue }
  if ($tar -and (Test-Path $tar)) { Remove-Item -Force $tar -ErrorAction SilentlyContinue }
  $lock.Close(); Remove-Item $lockPath -ErrorAction SilentlyContinue
}
exit $rc
