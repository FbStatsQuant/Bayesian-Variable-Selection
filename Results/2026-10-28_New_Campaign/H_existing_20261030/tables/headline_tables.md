### Exact recovery, c = 1 (strong signal)

| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS HPM** | primary | 95 | 96 | 94 | 91 | 89 | 94 | **559** | 95 | 95 | 97 | 93 | 84 | 96 | **560** |
| **SMC-BVS MPM (RB PIP > 0.5)** | secondary | 92 | 97 | 93 | 93 | 90 | 94 | **559** | 94 | 95 | 97 | 94 | 85 | 96 | **561** |
| SuSiE | primary | 99 | 98 | 97 | 95 | 98 | 98 | **585** | 100 | 96 | 98 | 95 | 94 | 99 | **582** |
| SuSiE-refine | companion (R4); arm added after the c = 1 results were seen; fit selection by ELBO | 99 | 98 | 97 | 95 | 98 | 98 | **585** | 100 | 96 | 98 | 95 | 93 | 99 | **581** |
| Spike-and-slab lasso | primary | 99 | 99 | 97 | 84 | 93 | 97 | **569** | 100 | 96 | 98 | 92 | 97 | 99 | **582** |
| Horseshoe (95% CI) | primary | 92 | 98 | 100 | 87 | 98 | 99 | **574** | 91 | 95 | 100 | 91 | 98 | 100 | **575** |
| MCP `ebic1` | pre-declared primary | 39 | 69 | 77 | 44 | 78 | 70 | **377** | 18 | 28 | 60 | 32 | 49 | 48 | **235** |
| MCP `ebic1_K37` | post hoc | 69 | 79 | 77 | 44 | 78 | 70 | **417** | 66 | 74 | 80 | 32 | 69 | 65 | **386** |
| ABESS (splicing heuristic) `ebic1` | pre-declared primary | 66 | 77 | 71 | 26 | 76 | 49 | **365** | 40 | 63 | 76 | 24 | 66 | 54 | **323** |
| ABESS (splicing heuristic) `ebic1_K37` | post hoc | 68 | 77 | 71 | 26 | 76 | 49 | **367** | 63 | 72 | 76 | 24 | 67 | 54 | **356** |
| Lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `ebic1_K37` | companion (R2), post hoc | 67 | 29 | 2 | 0 | 9 | 4 | **111** | 48 | 28 | 4 | 0 | 5 | 4 | **89** |
| Elastic net `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `ebic1_K37` | companion (R2), post hoc | 48 | 11 | 0 | 0 | 2 | 0 | **61** | 38 | 12 | 0 | 0 | 0 | 0 | **50** |
| Adaptive lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `cv_1se` | companion (R2) | 3 | 4 | 0 | 0 | 1 | 1 | **9** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `ebic1_K37` | companion (R2), post hoc | 74 | 60 | 26 | 14 | 47 | 26 | **247** | 36 | 27 | 9 | 4 | 11 | 9 | **96** |

### Exact recovery, c = 0.5 (weak signal)

| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS HPM** | primary | 79 | 84 | 64 | 25 | 59 | 59 | **370** | 71 | 75 | 67 | 35 | 31 | 61 | **340** |
| **SMC-BVS MPM (RB PIP > 0.5)** | secondary | 74 | 83 | 63 | 18 | 53 | 47 | **338** | 70 | 76 | 63 | 24 | 32 | 56 | **321** |
| SuSiE | primary | 65 | 70 | 34 | 9 | 3 | 39 | **220** | 49 | 57 | 47 | 21 | 0 | 31 | **205** |
| SuSiE-refine | companion (R4), pre-registered; fit selection by ELBO | 66 | 71 | 43 | 17 | 6 | 46 | **249** | 49 | 57 | 49 | 22 | 3 | 32 | **212** |
| Spike-and-slab lasso | primary | 80 | 84 | 53 | 9 | 42 | 35 | **303** | 67 | 64 | 43 | 15 | 28 | 38 | **255** |
| Horseshoe (95% CI) | primary | 74 | 69 | 18 | 0 | 10 | 14 | **185** | 60 | 50 | 11 | 0 | 11 | 4 | **136** |
| MCP `ebic1_K37` | pre-registered primary | 62 | 71 | 42 | 1 | 45 | 19 | **240** | 49 | 59 | 45 | 1 | 20 | 18 | **192** |
| MCP `ebic1` | pre-declared, non-primary at c = 0.5 | 38 | 58 | 42 | 1 | 45 | 19 | **203** | 13 | 26 | 34 | 1 | 18 | 10 | **102** |
| ABESS (splicing heuristic) `ebic1_K37` | pre-registered primary | 67 | 72 | 34 | 4 | 48 | 31 | **256** | 54 | 64 | 42 | 3 | 23 | 28 | **214** |
| ABESS (splicing heuristic) `ebic1` | pre-declared, non-primary at c = 0.5 | 65 | 72 | 34 | 4 | 48 | 31 | **254** | 36 | 55 | 42 | 3 | 22 | 28 | **186** |
| Lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Lasso `ebic1_K37` | companion (R2), pre-registered | 17 | 5 | 0 | 0 | 1 | 1 | **24** | 11 | 3 | 1 | 0 | 0 | 0 | **15** |
| Elastic net `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Elastic net `ebic1_K37` | companion (R2), pre-registered | 11 | 3 | 0 | 0 | 0 | 0 | **14** | 8 | 2 | 0 | 0 | 0 | 0 | **10** |
| Adaptive lasso `cv_min` | primary | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Adaptive lasso `ebic1_K37` | companion (R2), pre-registered | 10 | 17 | 1 | 0 | 2 | 6 | **36** | 10 | 2 | 0 | 0 | 0 | 0 | **12** |
