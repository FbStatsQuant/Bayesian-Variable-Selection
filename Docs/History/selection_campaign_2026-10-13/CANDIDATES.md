# CANDIDATES — every candidate considered, with its fate and a one-line reason

Fates: PROPOSED, SHORTLISTED, DOSSIER, KILLED (reason), SELECTED (rank), DEFERRED.

## Inherited from the 6 Oct brainstorm (Others/2_BVS_brainstorm_20261005/FINAL_RECOMMENDATIONS.md)
| id | candidate | fate | reason |
|---|---|---|---|
| B1 | Beta-binomial BB(1,p) model prior | carried in as strongest existing candidate | 93/90/76/33/73 HPM on dev S1–S5 by V-reweighting; no S6, no in-engine run, no fresh seeds |
| B2 | HPM over V + P(HPM) certificate, median secondary | carried in | 0-1-loss Bayes rule; certificate reliable when it fires |
| B3 | Exact visited-set posterior + hybrid outside-mass correction | carried in (estimation layer) | 15-25x smaller log Z error |
| B4 | BLiP resolution-adaptive regions | carried in (companion) | changes the reported object |
| B5 | Eve-genealogy single-run SEs | carried in (large-p certification) | PIP SEs calibrated under systematic resampling |

## Round 1 (2026-10-13)
| id | candidate | source | fate | reason |
|---|---|---|---|---|
| T1-C1 | Moment-tilted slab (non-local, uncapped) | T1 | DESK-SCORED: KILLED as primary | τ=.348: 351 (Bern) / 360 (BB) < 365; τ=.70 ≈ BB prior (362); S6 −3 vs BB-HPM; kill rule (omissions > BB) met |
| T1-C2 | Cluster dilution prior det(R)^a | T1 | DESK-SCORED: neutral | 346 (Bern) / 364 (BB); net −1 vs BB-HPM; S4 −3 |
| T1-C3/T3-4/T2-5 | Two-level cluster beta-binomial / CA2L | T1,T3,T2 | DESK-SCORED: KILLED | 334; S2 −10, S3 −8 vs BB-HPM; X-clusters ≠ population blocks in S6 (0/50) |
| T1-C4/T3-1 | Occupancy/count-pattern MAP then conditional HPM | T1,T3 | DESK-SCORED: KILLED | 358 (BB); net −7 vs BB-HPM (S6 +1) |
| T2-2 | OF-HPM (occupancy > .5 then conditional HPM) | T2 | DESK-SCORED: KILLED | 361 (BB); 3 fixed / 7 broken vs BB-HPM; S6 +1 |
| T3-2 | Count-level hierarchical BFDR | T3 | DESK-SCORED: SURVIVES as BFDR replacement | q=.05 @ Bern 354 (93/88/74/29/70, S6 37) vs old BFDR5 305; below BB-HPM 365 (net −11) |
| T2-1 | PC-Γ maximin over size priors | T2 | DESK-SCORED: KILLED as rule | 351; net −14 vs BB-HPM; its prior-continuation PATH survives as an in-engine route to BB |
| T3-3 | Γ-persistence HPM | T3 | DESK-SCORED: identical to BB-HPM | differs in 1/550 datasets |
| T2-4 | κ-MPM | T2 | DESK-SCORED: KILLED | κ=2 @ BB 362; κ=4 366 = HPM ± noise; no loss justifies it |
| T2-3 | Anneal past φ=1 (AP1) for HPM + certificate | T2 | PROPOSED (large-p) | no decision change at p=30 by construction; needed for HPM at large p |
| T2-6 | g-path / hyper-g | T2 | KILLED (theory) | T1 §0: only reparametrises size prior; ĝ effect ±1 |
| T1-C5 | δ-relevance HPM | T1 | KILLED (theory) | needs δ ≈ .35 to bite, threatens β = .5 signals |
| T1-C6 | BB(1, p_eff) | T1 | KILLED (desk) | BB(1,p/2) ≈ BB(1,p) on S1–S6 |
| T3-5 | BayesBag HPM | T3 | DEFERRED | weak mechanism (a only), costly; not run |
| T3-6 | Model-level credible sets (u65/u80) | T3 | PROPOSED (companion, other metric) | honest S4/S6 output |
| L1 | Size-mode / size-median then best model (under BB family) | lead | DESK-SCORED: KILLED | best 360 (ywj) < 365 |
| L2 | Evidence-chosen size prior per dataset | D1 | DESK-SCORED: KILLED | Bern(0.2) has max Z_V in 500/500 |
| F1 | Occupancy-then-marginal identity (OMI) + F1b | Fable | DESK-SCORED: KILLED | 325 (Bern) / 358 (BB) vs HPM 337/365; swap+mixed S4/S6 unchanged (51/12 @ BB); only the median reduces swaps, by trading them for omissions |
| F2 | h-augmented exact composite start (BB via latent h; Z_0 by exact Gauss–Jacobi quadrature) | Fable | SHORTLISTED (in-engine route) | keeps Z_0 exact and the validated φ-bridge; cross-check vs T2-1 prior path |
| F3 | Pattern-stratified enumerator | Fable | SHORTLISTED (infrastructure) | exact for every cluster-exchangeable prior/rule |
| F4 | Fixed mixtures ½Bern(.2)+½BB(1,p) | Fable | KILLED (arithmetic) | ≈ Bern(.2) at sizes 5–6 |
| M6-check | log T of true weak signals at S* (τ=.348) | Fable check | done | median −0.2 to −0.4 nats for var 19, p10 ≈ −0.9; var 8/22/30 ≈ neutral (desk/DX/DX2) |
| M7-check | share of BB-HPM superset/mixed extras sharing an X-cluster with a true variable (S3–S6) | Fable check | done | 31 % of extras (15/48) → cluster priors can fix at most a third |

## Round-1 selection (Fable, after red team) — 2026-10-13
| rank | plan | built from |
|---|---|---|
| 1 | BB(1,p)+HPM in-engine, corrected size-convolution start (confirmatory) | B1, B2, F2 (repaired by red team), T2-1 path as cross-check |
| 2 | S10-dev weak-signal stress (hedge: decides BB-HPM vs Bern(0.2)-HPM for the confirmatory slot) | red team |
| 3 | p = 60 exact scaling test + certified HPM, annealing past φ = 1 | red team sixth idea, T2-3 |
| 4 | Count-level hierarchical BFDR (FDR family, exploratory) | T3-2 |
| 5 | P(HPM) certificate + u65 model sets + BLiP (companion) | B2, T3-6, B4 |

## Phase 2 update (2026-10-13)
- BB(1,p)+HPM (round-1 frontier): KILLED as the proposed change by the pre-registered weak-signal rule (R1–R3 all fire; RESULTS_PHASE2.md). Kept as a
  documented strong-signal/low-FP option only.
- Bern(0.2)+HPM: becomes the confirmatory candidate (existing baseline; no target or engine change). S 400 vs median 382; W 128 vs 104.

## Confirmation (2026-10-14, sealed C S1–S6 × 200)
- BB(1,p)+HPM: pooled 846/1,200 vs median 775 (p = 5e-10) and Bern-HPM 810 (p = 2e-4); guardrail G1 fails in S4 (71 vs 84). Not "CONFIRMED" under
  the frozen label; kept as the candidate per Felipe (S4/weak-signal limitation documented). confirm/CONFIRMATION_RESULTS.md.
