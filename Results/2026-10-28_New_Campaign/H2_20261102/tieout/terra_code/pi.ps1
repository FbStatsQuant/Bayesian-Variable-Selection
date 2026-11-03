$root='C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian'
$R='C:\Program Files\R\R-4.4.1\bin\Rscript.exe'
$script=Join-Path $root '02_Experiments\I_2026-10-28_New_Campaign\code\scoring\run_theory_H.R'
$new='C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign\results\20261030T0934Z_prodH'
$input='C:\Users\felip\Documents\NOTS_BVS\NOTS_projects_ml75\BVS\bench20261019\inputs'
$truth=Join-Path $root '02_Experiments\F_2026-10-19_benchmark_study_n200\Benchmark_Study_20261019\verify\recount\c050\inputs\truth_scoring'
$out=Join-Path $root '02_Experiments\I_2026-10-28_New_Campaign\analysis\H2_20261102\tieout\terra_code'
foreach ($item in @(@('50','p0500_S1_r001','c100'),@('51','p1000_S4_r050','c050'))) {
 $n=$item[0]; $ds=$item[1]; $scale=$item[2]; $pd=$ds.Substring(0,5)
 & $R $script --record (Join-Path $new "$pd\${ds}_${scale}\SMCBVS.rds") --inputs (Join-Path $input "$pd\$ds.rds") --truth (Join-Path $truth "$pd\$ds.rds") --scale $scale --td-d none --out (Join-Path $out "pi$n.csv")
 if ($LASTEXITCODE -ne 0) { throw "pi $n failed" }
}
