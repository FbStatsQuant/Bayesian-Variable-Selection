# S2 disposition — Sol line check of the bridge leg (gpt-6.1-sol, high)

Review: `reviews/S2_linecheck_sol.md` on `reviews/S2_frozen/MANIFEST_S2.txt` (hashes verified by the reviewer).
Verdict: **"S2-VERDICT: FAIL AS WRITTEN — repair F1–F5 before acceptance; R1/R2, the POST2 rebase, R4's conditional rate
calculation and PoolZ are mathematically sound, with F6–F9 as listed and all inherited statuses unchanged."**
Lead: all 9 findings ACCEPTED and repaired. No finding is a counterexample to a target or a change to a master; F1–F3
are premises/scope the reader text must carry, F4–F5 card wording. The repairs and all other edits made after S2's
freeze go to one diff check (S3; fresh Opus 5.5 high under HQ's overnight rule).

| # | Sev. | Where | Repair | Tag |
|---|---|---|---|---|
| F1 | MAJOR | (S4), R3 MACH/CONFIG rows | (S4) rewritten: (i) idealised machine with MACH's time/memory constants $(\tau,\tau_0,\beta,\beta_0)$; (ii) covered configuration incl. TDP-IMPL's operation/storage contract, certificate budgets in the allocation, concurrency factor, grid fallback on; (iii) random numbers and stops; (iv) declared allocation ≥ the explicit envelopes incl. preflight and LS0 bounds; source of record `C-DLV/STATEMENT.md:21-46` and `FINAL/sections/s6_delivery.tex:29-62`. R3 rows MACH, CONFIG, TDP-IMPL, allocation updated to cite them. | convention list STRONGER (now faithful); theorem clauses EQUAL |
| F2 | MAJOR | (S5), Theorem 10 | (S5) rewritten to carry the full N1/SAMP contract: fresh i.i.d. uniforms per stream; final-run streams independent of calibration streams; exact π₀ draws **and** exact start normaliser; kernels with uniform state-independent order; calibration a function of data and its streams; measurability (code bridge); potential-run interpretation; source of record `W1-N1/STATEMENT.md:70-88`, `L1_bridge.md:33-55`, `W3-SAMP/STATEMENT.md`; inherited START/KERNEL status quoted. | convention list STRONGER (now faithful) |
| F3 | MAJOR | Theorem 10 statement | Sampler-branch scope stated; $\mathcal A$ = sampler branch and calibration status ok; estimates defined from the uninterrupted island records on $\mathcal A$, equal to the printed fields on completed runs; printed-field rate stated with the completion indicator; exact-branch remark (Theorem 2 directly); "intersections, not conditioning". R4 header states the same scope. | literal scope WEAKER (now faithful to C-v) |
| F4 | MAJOR | card row 3.6 | Rewritten: errors × indicator of calibration success are $O_P(\cdot)$; probabilities of "calibration succeeds and MPM wrong" and "run completes and reported model wrong" → 0; no lower bound on $P(\mathcal A)$; printed fields on completion. | card WEAKER (now faithful) |
| F5 | MAJOR | card row 3.6 | Setting stated as Theorem 10's: signal fixed on the standardised scale, Theorem 2's population floor, Theorem 5's visibility/no leakage; `W2-APP:POST` noted to cover this convention; no raw-coefficient claim. | card EQUAL to reader |
| F6 | MINOR | Theorem 1′ title, remark (o), card row 1.1 | "no eigenvalue condition off $S_0$ **beyond the vanishing floor (A5)**"; remark (o): the margin replaces the bounded-size floor (A4) off $S_0$ and beta-min, (A5) kept. Note for HQ: H5 card 6 asked for "no eigenvalue condition off $S_0$"; S2 shows that is literally false while (A5) is retained, so the qualifier is added (the consultant's intent — never "no eigenvalue condition" outright — is kept). | EQUAL (description) |
| F7 | MINOR | R4 status line | "An assembly conditional on `W2-APP:POST` … the other cited inputs are PROVED-CHECKED". | — |
| F8 | MINOR | R3 fallback row | Code condition stated exactly (`isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE))`); both defaults required by (S4)(ii); selection/freeze cited at `v3_calib.R:163-189`. | — |
| F9 | NIT | R1 line 8 | $d<2.4664$. | — |

Positive record from S2 (kept for CP3): R1 PASS-WITH-FIXES (only F9), R2 PASS, R4 rate calculation PASS (under N1),
PoolZ + REPORT block PASS, Theorems 1, 3, 4, 5, 8 PASS, Theorem 1′ mathematics PASS, Theorems 6–7 statistical clauses
and common-data-event clause PASS; all statuses verbatim.
