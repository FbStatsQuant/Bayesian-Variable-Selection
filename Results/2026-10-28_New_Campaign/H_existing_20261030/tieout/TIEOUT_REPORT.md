# Independent tie-out

Cells checked: 44. Matches: 39. Mismatches: 5 (cells 1, 10, 12, 30, 35).

Mismatches (claimed -> recomputed): 1: 373.0 -> 370, 10: 90.0 -> 93, 12: 91.0 -> 93, 30: 2.0 -> 0, 35: 0.42 -> 0.0500.

Truth: 1200 RDS files independently read by R and compared as sets against manifest; 0 disagreements.

Reconciliation: a bundle is a case folder, whether or not its files are present; resource limits count hpm rows once per case. Presence of CSV and RDS files is recorded in result notes. Paired comparisons treat missing or unsuccessful comparator fits as not exact, as specified.

Files used count includes distinct existing fit/derived CSV files, truth RDS files and the manifest and run map where applicable; reconciliation counts only existing SMC CSVs. Missing expected fit rows are treated as misses.

Data problems: none identified.

Reproduce all results (Python invokes the R helper):

```powershell
py -3 -I "<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\H_existing_20261030\tieout\code\tieout.py"
```

R subprocess: "C:\Program Files\R\R-4.4.1\bin\Rscript.exe" "<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\H_existing_20261030\tieout\code\truth.R" "<OLD_ROOT>\02_Experiments\F_2026-10-19_benchmark_study_n200\Benchmark_Study_20261019\verify\recount\c050\inputs\truth_scoring" "<OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\analysis\H_existing_20261030\tieout\code\truth_extracted.csv"
