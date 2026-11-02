$reviewRoot='C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts'
$ownedRoot=Get-CimInstance Win32_Process -Filter 'ProcessId=39200'
if (-not $ownedRoot) { Write-Output 'Already ended'; exit 0 }
if ($ownedRoot.CommandLine -notmatch 'full_10b[.]R') { throw 'PID no longer identifies this review check' }
function Stop-OwnedDescendants([uint32]$ownedParent) {
    $children=Get-CimInstance Win32_Process -Filter "ParentProcessId=$ownedParent"
    foreach ($child in $children) {
        Stop-OwnedDescendants $child.ProcessId
        Write-Output "Stopping owned descendant $($child.ProcessId): $($child.CommandLine)"
        Stop-Process -Id $child.ProcessId -ErrorAction SilentlyContinue
    }
}
Write-Output "Bounded additional full_10b check stopped at $([DateTime]::UtcNow.ToString('o')); first fit still running, two full fits cannot finish within roughly 15 minutes."
Stop-OwnedDescendants 39200
Stop-Process -Id 39200 -ErrorAction SilentlyContinue
