# Summary: test2

specs (tasks::raw): pilot/test_tasks.tsv::pilot
planned units 4; used 3; missing 1; conflicting 0; provenance-excluded 0; reference module sha256: {"pk_core.py": "6a94ab497e2bd771ae459a03a8693251c22ed239c4f437b9f0c38d55ae5e2907", "cs_core.py": "14b14cfd277bd2b52f0c16cf1404ebf83c3e05a158078dba5b89567302d3f074", "bvs_core.py": "e8283f5600f203a7f6016d62c55d07fd56bd9bbad4b7af1b9a9c87e05e0cc603", "fac_core.py": "e06d7dc50e132dcf40061b32383385a518ba9482cf6d9efca63ee77af1521f24"}

Counts out of N (used units of the cell); endpoint/m*/k_hit/excess statistics over uncensored units only. Medians [min, max]. W = leading swaps; excess = k_hit − (ℓ_n + |S̃₀|) (≤ 0 ⇔ MR1 scores S₀), over the k_hit_finite units. runs_* = number of runs with ≥ 1 event; events_* = total events.

| design | rho | n | p | layout | N | censored | K | saturated | start_size | start_has_S0 | W | W_minus_ell_s0 | m_star_over_K | runs_swaps_after_del | events_swaps_after_del | runs_adds | final_is_S0 | k_hit_finite | MR1_scores | MR1_scores_saturated | cap2_scores | excess_over_MR1 | runs_ties | runs_near_ties | max_direct_absdiff | direct_order_fail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cs0.5 | None | 200 | 500 | aligned | 1 | 0 | 100 | 1 | 100 [100, 100] | 1 | 9 [9, 9] | -5 [-5, -5] | 1.08 [1.08, 1.08] | 1 | 3 | 0 | 1 | 1 | 1 | 1 | 1 | -3 [-3, -3] | 0 | 0 | 9.549694368615746e-12 | 0 |
| cs_exact | 0.5 | 6000 | 4800 | mixed | 1 | 0 | 3000 | 0 | 1805 [1805, 1805] | 1 | 69 [69, 69] | 51 [51, 51] | 0.623 [0.623, 0.623] | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 50 [50, 50] | 0 | 0 | None | 0 |
| s5_exact | None | 600 | 480 | aligned | 1 | 0 | 300 | 0 | 154 [154, 154] | 1 | 7 [7, 7] | -8 [-8, -8] | 0.523 [0.523, 0.523] | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | -9 [-9, -9] | 0 | 0 | 7.071321306284517e-11 | 0 |

## Descriptive n-trend of the median leading-swap count W (log-log LS slope; evidence, not a limit)

| exp | design | rho | p/n | layout | n values | median W | slope |
|---|---|---|---|---|---|---|---|

## Exceptional units (0)


## Missing units (1)

nothere

## Conflicting units (0)

none

## Provenance-excluded units (0)

none
