# Sol review 1 fixes - W1 (2026-10-30)

| Finding | Change | Test | Result |
|---|---|---|---|
| R1-2 rank gate | Source an isolated mutated `ebic_candidates` with rank gate removed, restore the original | Run the same rank-deficient-candidate guard | Original PASS; mutant assertion fails as intended |
| R1-2 RSS gate | Mutate `ebic_candidates` to allow invalid RSS and compute finite scores, restore the original | Same zero and nonfinite RSS guards | Both originals PASS; both mutant assertions fail as intended |
| R1-2 tie order | Mutate `ebic_pick` to reverse actual key ordering, restore the original | Same criterion/k/key tie guard | Original PASS; mutant assertion fails as intended |
| R1-2 selected KKT | Mutate `alasso_fit_body` to bypass selected CV-min KKT failure while leaving injected second-stage fault in place, restore the original | Same failed-status and retained coefficient/support-audit guard at p=20, 30 and 120 | Originals PASS; mutant assertions fail at all three p values |
| R1-2 preservation | Keep prior five implementation mutations and deployed ridge canary | Full single runner | All five mutant guards detect their faults; v2 ridge-weakness guard passes and deployed fails as intended |
| R1-5 | Add frozen current-state sections to changes, consumers and test report; preserve prior text as historical; disclose F1 union and open consumer gates | Compare against Sol review and 24-case, suite and manifest evidence | Sections written; 23/23 high-p frozen members rehashed successfully |

Detached `tests/run_review1_suite.R` under local R 4.4.1/glmnet 4.1-10 wrote `tests/review1_suite.script_exit` = 0; `tests/review1_suite.log` contains 72/72 top-level PASS and individual control results. The Rscript parent plus nested checks stayed within the two-job cap. The optional legacy F2 subprocess was not repeated; the earlier separate 24/24 result remains the evidence. Four locale startup warnings are in `tests/review1_suite.stderr.log`. The frozen manifest SHA-256 remains `8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373`. No file under F1_Lasso, F2_ElasticNet or F3_AdaptiveLasso was modified. R1-1, R1-3 and R1-4 belong to other review work; the consumer release checks remain open.
