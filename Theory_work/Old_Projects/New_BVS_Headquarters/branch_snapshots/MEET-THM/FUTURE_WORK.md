# MEET-THM · Future work (deferred items, each with a reason)

Opened by the chair 2026-11-04; completed at close. Items here get no per-theorem HQ for paper 1.

FW1 and FW2 are unchanged. FW3–FW27 were added by the clerk from MINUTES §2.3/§2.4, SYNTH_R2 §2.4 and R3_C §S4 "Required additions"; reasons are as the sources give them. Paths are `theory_campaign/MEET-THM/…`; `MINUTES` = `MINUTES.md`, `SYNTH_R2` = `SYNTH_R2.md`.

| ID | Item | Reason | Source |
|---|---|---|---|
| FW1 | Frequentist coverage of the exact posterior's credible intervals | A target-theory question outside proposal §5.4, which concerns the computed vs the exact posterior (HQ ruling Q2, 2026-11-04) | `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md` |
| FW2 | TV/KL error bound for the final pooled estimate in the masked regime | Not binding (§5.4 lists "possible metrics"; HQ ruling Q3); needs V11 or N10, both OPEN | `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`; R1_D:602; R1_A:645–646 |
| FW3 | K13: start-mode consistency under orthogonal blocks and a σ²-inflated beta-min margin | Needs TG4-type probability bounds not supplied | `SYNTH_R2.md:173` (R0_DIFF K13) |
| FW4 | K24: polynomial mixing of the φ = 1 round (Yang–Wainwright–Jordan transfer); also useful general production mixing and masked population accuracy (N10) | N10 OPEN; the YWJ/ZYVR route is blocked as stated | `SYNTH_R2.md:174`; `R3_C.md:385` |
| FW5 | K23: Dirichlet/spectral comparison of the random-order round with the random-scan mixture | Its only consumer, K24, is deferred (A, B, D, R3-4). Seat C dissents: it would keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL; MINUTES allows the S-KERNEL HQ to cite it without a theorem number | `SYNTH_R2.md:175`; `MINUTES.md:79`; `R3_C.md:59` |
| FW6 | K31: as-coded masked stage count (realised T_n; Conjecture P OPEN); N5(b): rebuild convergence within ℓ rebuilds, candidate-pair coverage / P(S₀ ∈ V), P(schedule_limit) and calibration-failure probabilities | Conjecture P OPEN; V's complement is never inspected (I9(d)); only T ≤ T_e and the coverage identity are provable; successful-grid properties do not prove successful calibration. Rebuild convergence is FW in either placement of K33 | `SYNTH_R2.md:176`; `MINUTES.md:82`; `R3_C.md:325`; `R3_D.md:247` |
| FW7 | K58: masked consistency of the equal-weight PIP/MPM | Reduces to population delivery; FMP-DELIVPOP is OPEN | `SYNTH_R2.md:177` |
| FW8 | K57, general fixed-budget equal-weight accuracy (only the recording-marginal bias comparison P1 ships in S-POOL) | A recording-marginal bias bound does not close estimator accuracy or DELIV-POP; needs a checked estimator-level theorem for the actual records and budgets | `MINUTES.md:66`; `R3_C.md:323`; `R3_C.md:36`; `R3_B.md:86` |
| FW9 | K59: R vs N at fixed total particles (allocation) | PROOF SKETCH only | `SYNTH_R2.md:178` |
| FW10 | K71: (b1-LH-iid) on LH with iid final draws, also under general DELIV | (b1-LH-iid) GAP; T38-b1-LH-iidfail XF ERROR | `SYNTH_R2.md:179` (R0_DIFF K71) |
| FW11 | K75: NP-completeness of the global-certificate decision problem for the fixed prior and penalty | Needs a score-specific reduction that has not been supplied | `SYNTH_R2.md:180` |
| FW12 | K92: separation from single-chain flip/swap MCMC (moat construction) | The moat construction and the accuracy-matched comparator are unproved; speed-up claims are empirical by decision | `SYNTH_R2.md:181` |
| FW13 | K82: delivery, P(U) → 0 (also delivery/resource-failure laws, P(resource_limit)) | No route; every output theorem is stated jointly with the output event in liminf form | `SYNTH_R2.md:182`; `R3_C.md:372` |
| FW14 | K94: finite-n bound on the posterior-miss probability Π(X) | Envelope GAP | `SYNTH_R2.md:183` |
| FW15 | K99 quantitative: k-way barrier for cross-block masked contrasts | k-way barrier unproved (the qualitative remark ships in S-LIM) | `SYNTH_R2.md:184` |
| FW16 | K107: validated arithmetic / rounding-error bound; production validated numerics (N16) | N16 OPEN; T33-errbound COUNTEREXAMPLE; exact-arithmetic bounds do not validate rounded production computations. K108 (deterministic perturbation lemma) stays in S-CERT | `SYNTH_R2.md:185`; `R3_C.md:331` |
| FW17 | K80: positive power of the E1/E2/E3 and low_empirical_ESS flags | Flags are heuristics by decision; no sampling law for the flags | `SYNTH_R2.md:186`; `MINUTES.md:80` |
| FW18 | N12 / exponential p: exponential-dimension contraction and selection (Song–Liang Cor 1) | No completed prior-tail/contraction route; p ≤ n^A stays in scope | `SYNTH_R2.md:188`; `R3_C.md:352,387` |
| FW19 | Growing support and cap non-binding (N11/N12) | Fixed-support LH does not discharge these extensions | `R3_C.md:328` |
| FW20 | Hellinger / predictive contraction (Song–Liang Thm 1) | Not delivered; selection counterpart in S-T only | `SYNTH_R2.md:189` |
| FW21 | K97: Song–Liang analytic separation (null-exclusion/FDR) | The iteration-uniform null-BF/prior-odds step is NOT REPAIRED (W2PC1) and is an unproved hypothesis about SL's algorithm, not a model/design condition. LIT-PAR G4 is cited in the paper as labelled numerical evidence | `MINUTES.md:78,84`; `SYNTH_R2.md:191` |
| FW22 | Sharp ε-scale necessity statement for §5.3 | All three seat forms are COUNTEREXAMPLEs; C's is a range obstruction for the D_* route only. The scale disclosure ships (not a theorem) | `SYNTH_R2.md:192` |
| FW23 | K29: favourable O(1) stage law, unconditional application | The (LL)/over-tilted q_w input is not a model/design condition and no family exhibits it (W2PC1:187 DESIGN-ASSERTED, GAP). Only the conditional implication is cited in S-STGI | `MINUTES.md:70`; `R3_C.md:324`; `R3_A.md:43,67`; `R3_B.md:61` |
| FW24 | Useful two-sided masked evidence precision (N4(iii)/V11) | Distinct from FW2's final-estimate TV/KL and from one-shot variance failure; V11 OPEN | `R3_C.md:326` |
| FW25 | Random/adaptive partition quality and study packing (N8; K71 as C pairs them), including the study generator (PART-pairing, g = 5, 2g ≤ B) | SIZE does not determine pairings when two groups fit in one block; PART-pairing OPEN; the study design is not the LH exhibit | `R3_C.md:327`; `R3_D.md:246` |
| FW26 | Finite-n Gibbs discovery (HPM residual) | Existing asymptotic or vacuous bounds do not supply useful finite-n discovery (ThmB-T24 vacuous at n = 200; no route) | `R3_C.md:329`; `R3_B.md:303`; `R3_D.md:248` |
| FW27 | Unbounded functionals: integrability extensions of M1 (§13.1) | M1 is stated for bounded h ∈ [0, 1]; unbounded functionals require integrability extensions (from C's coverage table, not its "Required additions" table) | `R3_C.md:344` |

## Dropped (MINUTES §2.4; not FUTURE_WORK)

| Candidate | Reason | Source |
|---|---|---|
| K12 | A test oracle, not a guarantee | `MINUTES.md:94`; `SYNTH_R2.md:195` |
| K34 | TI evidence is not in the method (the Ĵ half ships as reporting, S-REP) | `MINUTES.md:95`; `SYNTH_R2.md:196` |
| K66 | PARTLY-FALSE (C3-PGD, CEX-localmax(A2)) | `MINUTES.md:96`; `SYNTH_R2.md:197` |
| K67 | Relies on K66 | `MINUTES.md:97`; `SYNTH_R2.md:198` |
| K91 | No accuracy-matched comparator; OPW2-cex | `MINUTES.md:98`; `SYNTH_R2.md:199` |
| K98 | KNOWN-FALSE (SHARE-M(b), FD-NM) | `MINUTES.md:99`; `SYNTH_R2.md:200` |

Items recorded as "outside the fixed method" (adaptive/overlapping partitions; backfit start) are dispositions in `COVERAGE_MATRIX.md`, not FUTURE_WORK. The audit obligations (N2(b),(c),(e), N14(c), the N3 DP invariant, the integrated streams/LS0/GUARD-W/DAG audits) are named implementation premises in `HQ_CHARTERS/`, not FUTURE_WORK (MINUTES §2.3).
