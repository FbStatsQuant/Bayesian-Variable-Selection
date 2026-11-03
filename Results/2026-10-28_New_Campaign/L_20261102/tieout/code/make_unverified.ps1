$base = 'C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\I_2026-10-28_New_Campaign\analysis\L_20261102\tieout'
Import-Csv -LiteralPath (Join-Path $base 'CLAIMS.csv') | ForEach-Object {
    [PSCustomObject]@{ cell_no = $_.cell_no; claimed = $_.claimed; recomputed = ''; verdict = 'UNVERIFIED'; n_cases_used = 0; note = 'Raw records not recomputed: specified Windows data and output paths are not accessible on Owls; remote staging would write outside the permitted tieout folder.' }
} | Export-Csv -LiteralPath (Join-Path $base 'TIEOUT_RESULT.csv') -NoTypeInformation -Encoding UTF8
