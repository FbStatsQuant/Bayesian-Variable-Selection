$R = 'C:\Program Files\R\R-4.4.1\bin\Rscript.exe'
$script = 'C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\02_Experiments\I_2026-10-28_New_Campaign\analysis\H2_20261102\tieout\terra_code\scores.R'
foreach ($i in 45..49) { & $R $script $i; if ($LASTEXITCODE -ne 0) { throw "score $i failed" } }
