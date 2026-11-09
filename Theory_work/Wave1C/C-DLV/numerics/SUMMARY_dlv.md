# C-DLV numerics summary (numbers only)

Core: byte-identical copy of Scripts/SMC_BVS/core (hashes in core_copy_hashes.txt). Per fit: data seed = seed, method seed = 1000 + seed, allocation mem_gb 16 / hours 24. Designs M, F as in the brief; S0 = {1,10} (M), {1,19} (F) (1-based; F second signal = hub of 0-based group 2, the first unlinked group).
Per-construction detail: dlv_constructions.csv. Per-fit: dlv_runs.csv, rds/.
peak_mem = process-lifetime peak working set (Windows, one R process runs 16 fits in sequence, so it is a running maximum); fit$peak_memory_kb is NA on Windows.

| design | n | p | fits | status counts | non-smc | esc rate | hpm==S0 | mean N_p | max N_p | max N_b | max intervals | T_0 / T_1 | frac cons S0 in V | frac Lambda_V<log(10/9) (n eval) | max Lambda_V | max sec | max peak_mem MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M | 100 | 27 | 8 | completed:8 | 0 | 0.000 | 0/8 | 5.62 | 10 | 6 | 16 | 1000 / 4000 | 1.000 (23/23) | 0.000 (0/23) | 16.86 | 15.2 | 146 |
| M | 200 | 54 | 8 | completed:8 | 0 | 0.000 | 0/8 | 9.12 | 12 | 6 | 16 | 1000 / 4000 | 1.000 (24/24) | 0.000 (0/24) | 41.7 | 23.2 | 171 |
| M | 400 | 81 | 8 | completed:8 | 0 | 0.000 | 4/8 | 2.12 | 5 | 9 | 11 | 1000 / 4000 | 1.000 (22/22) | 0.000 (0/22) | 34.25 | 24.5 | 177 |
| M | 800 | 108 | 8 | completed:8 | 0 | 0.000 | 8/8 | 4.12 | 12 | 9 | 15 | 1000 / 4000 | 1.000 (24/24) | 0.000 (0/24) | 138.5 | 57.5 | 181 |
| M | 1600 | 135 | 8 | completed:8 | 0 | 0.000 | 8/8 | 3.88 | 13 | 10 | 17 | 1000 / 4000 | 1.000 (29/29) | 0.000 (0/29) | 335.2 | 65.5 | 193 |
| F | 100 | 27 | 8 | completed:8 | 0 | 0.000 | 8/8 | 5.88 | 10 | 5 | 15 | 1000 / 4000 | 1.000 (21/21) | 0.000 (0/21) | 19.57 | 10.8 | 167 |
| F | 200 | 54 | 8 | completed:8 | 0 | 0.000 | 8/8 | 9.00 | 11 | 5 | 16 | 1000 / 4000 | 1.000 (22/22) | 0.000 (0/22) | 24.04 | 27.3 | 172 |
| F | 400 | 81 | 8 | completed:8 | 0 | 0.000 | 8/8 | 2.12 | 3 | 1 | 4 | 1000 / 4000 | 1.000 (19/19) | 0.105 (2/19) | 4.007 | 25.2 | 184 |
| F | 800 | 108 | 8 | completed:8 | 0 | 0.000 | 8/8 | 4.25 | 7 | 4 | 11 | 1000 / 4000 | 1.000 (26/26) | 0.000 (0/26) | 16.77 | 46.5 | 191 |
| F | 1600 | 135 | 8 | completed:8 | 0 | 0.000 | 8/8 | 6.00 | 9 | 9 | 15 | 1000 / 4000 | 1.000 (26/26) | 0.000 (0/26) | 69.27 | 67.5 | 203 |

Tier-wise max intervals vs T_e (all constructions):
```
 design    n tier  T_e intervals
      F  100    0 1000        15
      M  100    0 1000        16
      F  200    0 1000        16
      M  200    0 1000        16
      F  400    0 1000         4
      M  400    0 1000        11
      F  800    0 1000        11
      M  800    0 1000        15
      F 1600    0 1000        15
      M 1600    0 1000        17
```

Constructions with ok == FALSE:
```
[1] design       n            seed         tier         construction
[6] reason       intervals   
<0 rows> (or 0-length row.names)
```

Trigger strings (tier:fired) counts:
```
, ,  = t0:

   
    100 200 400 800 1600
  F   8   8   8   8    8
  M   8   8   8   8    8

```

Escalated fits:
```
[1] design           n                seed             status          
[5] tier_final       triggers_by_tier hpm              hpm_eq_S0       
<0 rows> (or 0-length row.names)
```

Non-completed statuses:
none

Guard exceeded in any fit: FALSE. Fits with estimates_available FALSE: 0. Converged (final tier) false: 0.

hpm by (design, n):
```
, ,  = 1

   
    100 200 400 800 1600
  F   0   0   0   0    0
  M   8   8   4   0    0

, ,  = 1+10

   
    100 200 400 800 1600
  F   0   0   0   0    0
  M   0   0   4   8    8

, ,  = 1+19

   
    100 200 400 800 1600
  F   8   8   8   8    8
  M   0   0   0   0    0

```

**Lead note (council C1 Opus #8):** no fit escalated (here and in N4); tier 1 was never reached, so schedule_limit was never at risk in these runs. The numerics bear on route (O-a) (no tier-0 trigger), not on (O-b) (tier-1 construction failure).
