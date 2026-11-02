# Disposition of Sol's conformance review (CONF manager, 2026-10-28)

Review: `CONFORMANCE_REVIEW_sol.md`, verdict ACCEPT WITH FIXES. All nine findings are adopted in CONFORMANCE.md revision 2.

| # | Sev. | Disposition |
|---|---|---|
| 1 | should-fix | Adopted. S1 is reclassified as behavioural at the study/resource-policy level, authorized by GO_2400 C1, and it affects output availability. "Not the method's outputs" is removed, and the verdict no longer leans on D5/P5. S2 is wording, on the basis of the written SCHEMA R-1 policy. |
| 2 | should-fix | Adopted. D30 is reclassified as conditional behavioural, and "impossible" is removed. A population scan of all 2,400 RDS found the fallback fired 0 times, for X and for y (`work/C_population/`). |
| 3 | should-fix | Adopted. D03 is reclassified as conditional behavioural, pending the T wording. The inclusive interpretation is stated, and no stop occurred at a grid checkpoint. |
| 4 | should-fix | Adopted. D12 is corrected with the p1000_S5_r044_c100 overshoot. The population scan adds that no completed fit exceeded its allocation. |
| 5 | should-fix | Adopted. The population scan now checks escalated ⇔ any tier-0 trigger in both directions, tier IDs, N budgets, φ = grid[−1] for every final island, and grid = frozen grid: 0 failures. Trigger storage is described as stored, not recomputed. |
| 6 | note | Adopted. The limits of the assembly checks are stated explicitly. |
| 7 | should-fix | Adopted. Worker, manager and reviewer evidence are now separated. The resource checks are population-wide: guard inequality, support NA, and support_audit = HPM, 6 of 6. The budget values are attributed to whoever checked them. |
| 8 | should-fix | Adopted. D41 has its own row as a T reporting item, and the table is repaired. |
| 9 | should-fix | Adopted. The count is now 31 D-rows. Final-check counts carry their denominator. The stage summary is now population-wide (2,394). Prior audits are described as cross-checked, not re-certified. |
