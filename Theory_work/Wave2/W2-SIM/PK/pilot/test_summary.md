# Summary: pilot/test

raw files: pilot/p1.jsonl, pilot/r1_pilot.jsonl, pilot/s5e_pilot.jsonl
runs: 3 (duplicates dropped: 0)

Counts are out of N. Medians [min, max]. W = leading swaps; excess = k_hit − (ℓ_n + |S̃₀|) (≤ 0 ⇔ MR1 scores S₀).

| design | rho | n | p | layout | N | K | saturated | start_size | start_has_S0 | W | W_minus_ell_s0 | m_star_over_K | swaps_after_first_del | runs_with_adds | final_is_S0 | MR1_scores | cap2_scores | excess_over_MR1 | ties |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cs_exact | 0.5 | 20000 | 19800 | aligned | 1 | 10000 | 1 | 10000 [10000, 10000] | 1 | 429 [429, 429] | 409 [409, 409] | 1.04 [1.04, 1.04] | 0 | 0 | 1 | 0 | 1 | 408 [408, 408] | 0 |
| s5_exact | None | 600 | 480 | mixed | 1 | 300 | 0 | 6 [6, 6] | 1 | 0 [0, 0] | -15 [-15, -15] | 0.0067 [0.0067, 0.0067] | 0 | 0 | 1 | 1 | 1 | -16 [-16, -16] | 0 |
| cs0.5 | None | 200 | 500 | aligned | 1 | 100 | 1 | 100 [100, 100] | 1 | 5 [5, 5] | -9 [-9, -9] | 1.01 [1.01, 1.01] | 0 | 0 | 1 | 1 | 1 | -10 [-10, -10] | 0 |

## Exceptional runs (0)

