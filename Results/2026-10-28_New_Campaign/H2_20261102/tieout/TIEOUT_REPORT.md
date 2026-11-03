# Independent tie-out

Cells checked: 51 Matches: 46 Mismatches: 5

Mismatches (claimed -> recomputed):
-  5: 65 -> 67
- 25: 2397 -> 2400
- 37: 0.01 -> 0.0067
- 41: 35 -> 32
- 42: 2 -> 0

Data problems: No missing or unreadable SMC or truth records.
Benchmark missing/failed rows: Missing rows: 0 ; failed rows: 0 | Missing rows: 0 ; failed rows: 0 | Missing rows: 0 ; failed rows: 0 | Missing rows: 0 ; failed rows: 0 | Missing rows: 0 ; failed rows: 0 | Missing rows: 0 ; failed rows: 0

File counts exclude code and claims, and count input data files. Completed fits only for diagnostics; failed fits count as recovery misses.
The combined recount took approximately 25 minutes on this laptop, exceeding the requested roughly ten-minute script size; it completed successfully.

Reproduction: run each score invocation for the indicated integer, then produce the report:

```powershell
& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout/terra_code/recount.R"
& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout/terra_code/bench.R"
foreach ($i in 42..49) { & "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout/terra_code/scores.R" $i }
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout/terra_code/pi.ps1"
& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout/terra_code/report.R"
```
