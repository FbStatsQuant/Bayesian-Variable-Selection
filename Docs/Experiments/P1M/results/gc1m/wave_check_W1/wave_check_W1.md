# wave check W1 (HQ H-48 / H-49)

**no FLAG: no fit has low_empirical_ESS together with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0**

| fit | HPM = S0 | MPM = S0 | E1 / E2 / E3 | sigma-hat (sd log Z_r) | C2 | min ESS / N | island, stage | phi step (dphi) at the dip | low_empirical_ESS (engine / sections) | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| 6-ADJOPP-n200-r01-V-s1 | yes | yes | False / False / False | 0.8747 (0.8747) | PASS (M1 0.0206, M2 0.00104, evid gap 0.0630 <= 0.6562) | **0.738** (ESS 1846.0 of N 2500) | island_3.bin, stage 5 | 0.2010 -> 0.2678, **dphi 0.0668** | False / False | - |
| 6-AR-n200-r02-V-s1 | yes | yes | False / False / False | 0.0449 (0.0449) | PASS (M1 0.0154, M2 0.00092, evid gap 0.0041 <= 0.0356) | **0.759** (ESS 1897.4 of N 2500) | island_11.bin, stage 24 | 0.7117 -> 0.8390, **dphi 0.1273** | False / False | - |

## Every low_ESS fit (island-stages with ESS < 0.5 N)
- none in this wave

## Island timing (H-50 / H-51): elapsed vs engine time, pre-engine wait, billed vs engine-time cost, node types
- **6-AR-n200-r02-V-s1** (16 islands): Slurm elapsed min / mean / max **462 / 990 / 1560 s**; engine `seconds.total` 392 / 464 / 625 s; **pre-engine wait (elapsed - engine) 69 / 526 / 995 s**; **Slurm-billed island cost 422.3 core-h** beside the **engine-time cost 197.8 core-h** (max single island 16.7 core-h; K2 compute line 33.6).
- **6-ADJOPP-n200-r01-V-s1** (16 islands): Slurm elapsed min / mean / max **440 / 821 / 1441 s**; engine `seconds.total` 370 / 448 / 667 s; **pre-engine wait (elapsed - engine) 68 / 373 / 899 s**; **Slurm-billed island cost 350.3 core-h** beside the **engine-time cost 191.0 core-h** (max single island 17.8 core-h; K2 compute line 33.6).
- node type **c**: 16 islands, elapsed min / mean / max 462 / 949 / 1560 s; engine mean 498 s; pre-engine wait mean 452 s.
- node type **g**: 16 islands, elapsed min / mean / max 440 / 862 / 1408 s; engine mean 414 s; pre-engine wait mean 448 s.
- Node constraint, one sentence: Proposal only (a node constraint to type g): the c-type islands average 949 s elapsed against 862 s on type g; had every island run at the g mean, the wave would have billed about 96.2 core-h less of 772.6 island core-h (12.5 %), before any extra queue wait that a constraint could add (not measured here), so it pays for itself only if the wait of the constrained type stays small.

H-48 rule: STOP only for low_ESS with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0; low_ESS alone is reported (H-49: expected about 1 fit in 7). The ESS values are read from the island sections st_ess / st_phi (the engine's own per-stage ESS; Delta-phi = st_phi[t] - st_phi[t-1], the first stage from 0).
