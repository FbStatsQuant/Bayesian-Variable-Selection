# F3 independent tie-out

Cells checked: 44
Matches: 41
Mismatches: 3
Unscorable: 0

## Mismatches (claimed -> recomputed)
- Cell 2: 86 -> 89
- Cell 21: 29 -> 32
- Cell 36: 2 -> 0

## Data problems
- None detected.

Missing completion markers and non-ok rows count as misses. Diagnostic tokens are counted from cv_min rows regardless of status or completion marker.

## Reproduce

```powershell
& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "<OLD_ROOT>/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout/terra_f3_code/tieout.R"
```
