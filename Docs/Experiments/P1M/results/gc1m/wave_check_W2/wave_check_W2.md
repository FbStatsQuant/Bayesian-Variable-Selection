# wave check W2 (HQ H-48 / H-49)

**no FLAG: no fit has low_empirical_ESS together with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0**

| fit | HPM = S0 | MPM = S0 | pi-hat(S0) | E1 / E2 / E3 | sigma-hat (sd log Z_r) | C2 | min ESS / N | island, stage | phi step (dphi) at the dip | low_empirical_ESS (engine / sections) | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6-AR-n200-r03-V-s1 | yes | yes | 0.375 | False / False / False | 0.1222 (0.1222) | PASS (M1 0.0244, M2 0.00167, evid gap 0.0004 <= 0.0934) | **0.692** (ESS 1731.2 of N 2500) | island_10.bin, stage 23 | 0.6073 -> 0.7737, **dphi 0.1665** | False / False | - |
| 6-AR-n200-r04-V-s1 | yes | yes | 0.405 | False / False / False | 0.0194 (0.0194) | PASS (M1 0.0236, M2 0.00049, evid gap 0.0228 <= 0.0229) | **0.815** (ESS 2037.7 of N 2500) | island_9.bin, stage 25 | 0.8835 -> 0.9714, **dphi 0.0879** | False / False | - |

## Every low_ESS fit (island-stages with ESS < 0.5 N)
- none in this wave

## Island timing (H-50 / H-51): elapsed vs engine time, pre-engine wait, billed vs engine-time cost, node types
- **6-AR-n200-r03-V-s1** (16 islands): Slurm elapsed min / mean / max **442 / 702 / 1729 s**; engine `seconds.total` 370 / 416 / 484 s; **pre-engine wait (elapsed - engine) 69 / 286 / 1272 s**; **Slurm-billed island cost 299.7 core-h** beside the **engine-time cost 177.7 core-h** (max single island 12.9 core-h; K2 compute line 33.6).
- **6-AR-n200-r04-V-s1** (16 islands): Slurm elapsed min / mean / max **453 / 852 / 1785 s**; engine `seconds.total` 383 / 460 / 599 s; **pre-engine wait (elapsed - engine) 69 / 392 / 1229 s**; **Slurm-billed island cost 363.4 core-h** beside the **engine-time cost 196.2 core-h** (max single island 16.0 core-h; K2 compute line 33.6).
- node type **c**: 21 islands, elapsed min / mean / max 442 / 806 / 1785 s; engine mean 449 s; pre-engine wait mean 357 s.
- node type **g**: 11 islands, elapsed min / mean / max 444 / 723 / 1404 s; engine mean 418 s; pre-engine wait mean 305 s.
- **Wave: mean pre-engine wait per island 339 s over 32 islands (W1: 526 / 373 s per fit; pilot 205 s); Slurm-billed island cost 663.1 core-h vs engine-time 373.8 core-h. HQ H-52 rule: mean wait > 300 s: W3 onward %8 island-array throttle per fit, stagger kept.**
- Node constraint, one sentence: Proposal only (a node constraint to type g): the c-type islands average 806 s elapsed against 723 s on type g; had every island run at the g mean, the wave would have billed about 121.3 core-h less of 663.1 island core-h (18.3 %), before any extra queue wait that a constraint could add (not measured here), so it pays for itself only if the wait of the constrained type stays small.

H-48 rule: STOP only for low_ESS with an E-flag, sigma-hat > 0.5, a C2 failure or HPM != S0; low_ESS alone is reported (H-49: expected about 1 fit in 7). The ESS values are read from the island sections st_ess / st_phi (the engine's own per-stage ESS; Delta-phi = st_phi[t] - st_phi[t-1], the first stage from 0).
