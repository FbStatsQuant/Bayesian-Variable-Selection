# SMC-BVS v3 theory: status, results and paper plan

Draft of 2026-11-02 for the GH repository (`Docs/THEORY.md`). Drafted by Sonnet for review by Sol 6.1. Sources: `Docs/Theory/proofs/LOCKED_PROOFS.md` (the register), `PROOFS_STATUS.md`, `INVENTORY_20261028/THEORY_INVENTORY.md`, `PAPER_SELECTION_20261028/FROZEN_LIST.md`, `THEOREM_MAP.md`, `DROPPED.md`, `theorems/` and the per-theorem `STATEMENT.md` files. One page per item, T01 to T39, is in `Docs/Theory/one_pagers/`. All paths below are relative to `Docs/Theory/` unless they start with `Docs/`.

Nothing in this document is adopted. Where a source file and this summary disagree, the source file governs.

## 0. How to read this

**Status vocabulary** (used exactly, never upgraded):

| Term | Meaning |
|---|---|
| PROVED-LOCKED | The result is a row of `proofs/LOCKED_PROOFS.md`: statement file and final proof file are frozen with the SHA-256 recorded there. Always followed by the review depth and by "not adopted". |
| CONDITIONAL | The locked theorem carries open hypotheses that are assumed, not proved (H24, PW2, EXP', VIS, NL_eta, NL_avg, H2, H3, BASIN, COVER, exposure and occurrence conditions). The hypothesis is always named. |
| PARTLY PROVED | Only named parts are locked. The other parts are CONJECTURED. |
| CONJECTURED (not proved) | Every item of the 36 that is not in the register, and T37, T38, T39. |
| DROPPED | Two different senses, always distinguished: dropped from the paper selection (FROZEN_LIST) versus dropped as a conjecture (DROPPED.md). A theorem can be partly proved and dropped from the paper (T25(iv)). |

**Review depth by wave.** Wave 1 (10 results): Opus 5.5 lead; Astra #1 (Stage A); Astra #2 plus Opus 5.5 xhigh (Stage B); campaign review (Stage C) by Fable 5.1 (high) plus Astra xhigh. Wave 2 (4 results): Astra lead, two independent Sol 6.1 (high) reviewers, Astra xhigh closing review, Claude Opus audit. Wave 3 (5 folders, 7 theorem numbers): Opus 5.5 lead, two independent Opus 5.5 xhigh reviewers, statement checker where noted; the external (OpenAI) review is queued; no wave-level Fable campaign review is recorded and none is claimed.

**Locked is not adopted.** "Locked" means the statement and proof files named in the register are frozen and have passed their audits. "Adopted" means Felipe has accepted the result into the paper's theory. No result is adopted; the adoption of the 21 locked entries is an open decision of Felipe (section 5).

**Standing idealisations** (hypotheses only where a STATEMENT.md lists them; they are not H-xx labels): EX-A exact arithmetic; EX-S ideal independent uniform random streams; CAL calibration uses streams 0-9 only and the final run uses fresh streams 10-13; EXEC local-search scans are completed.

**n = 200.** The study design is n = 200, p = 500 or 1000. Every statistical theorem is an asymptotic statement; the numbers it gives at n = 200 are mostly not informative (section 5.3). Where the inventory states what a result means at n = 200 it is repeated in the item's one-pager and in section 3.

## 1. Orientation

SMC-BVS v3 targets the posterior of a Bayesian linear model on standardised data: a g = n slab with a unit ridge, an inverse-gamma IG(0.01, 0.01) variance prior and a beta-binomial BB(1, p) size prior capped at K = min(p, floor(n/2)). A sequential Monte Carlo sampler explores it: a composite start built from small blocks (exactly samplable), a tempering bridge, a hybrid move round (p Gibbs flips, one uniform swap, B neighbour swaps, one independence proposal in random order), four islands, a calibration stage followed by a frozen final run, and a local search. It reports the highest-posterior model (HPM) over all models it ever scored, PIPs by Rao-Blackwellisation, an evidence estimate and a 95% evidence lower bound.

The theory has two halves (THEORY_INVENTORY section D). The **statistical half** (T01-T08) asks whether the posterior puts its mass on the truth. The **computational half** (T09-T36) asks whether the algorithm finds, scores and reports what the posterior says. The structural fact that joins them: **the reported HPM is the best model ever scored**. So the computational half reduces largely to a scoring question (was the truth ever evaluated?), not a convergence question, and the HPM can work before the sampler has mixed. T21 is the composition that joins the halves; it is proved but conditional.

What the locked results establish and what they do not (INVENTORY section 0): 21 locked entries cover 20 of the 36 conjectures (12 in all parts, 8 in part); the theory describes the method that actually ran, with two caveats (mid-run `resource_limit` stops; global versus reported quantities); at n = 200 only the exact finite-sample layer is meaningful; and the single biggest open gap is an unconditional proof that the true model gets scored.

## 2. Master table

Counts (reconcile with THEORY_INVENTORY A.1): of T01-T36, **12 proved in all parts** (T01, T02, T03, T04, T06, T07, T09, T10, T12, T13, T15, T21; all core), **8 partly proved** (T11, T14, T20, T22, T23, T31 are core; T25, T27 are secondary), **16 not proved** (core: T17, T28, T32, T34; secondary: T05, T16, T18, T24, T26, T29, T33, T36; optional: T08, T19, T30, T35). Total by rank: core 22, secondary 10, optional 4. T37, T38, T39 are new conjectures (not proved).

Locked rows: 19 register rows, 21 theorem entries (T01 and T02, T06 and T07, and T10 are the wave-3 entries; T22 is split over two rows).

| ID | Title (old label) | Rank | Status | Paper role | Proof location | Open obligations |
|---|---|---|---|---|---|---|
| T01 | Contrast reduction and mixed-rate transfer (A0 = T1) | core | PROVED-LOCKED (all parts; wave 3) | Supplement lemma (of Thm 1) | `proofs/T01_T02_contrast_dimension/` | G, R (regime); external review queued |
| T02 | Dimension control and exclusion of strict supersets (A1 = T2) | core | PROVED-LOCKED (all parts; wave 3); (ii) needs SE | Supplement lemma (of Thm 1) | `proofs/T01_T02_contrast_dimension/` | SE (impossible at n = 200); external review queued |
| T03 | Selection, screening, PIPs and the global HPM (A2 = T3) | core | PROVED-LOCKED (all parts; wave 3; hypothesis H-T02 = T02(i)) | JRSS-B Thm 1; Biometrika Thm 1 | `proofs/T03_A2_selection_consistency/` | SE, BM-C; reported-output bridge is T21/T23; external review queued |
| T04 | Contraction without beta-min (A3 = T4) | core | PROVED-LOCKED (all parts; wave 3; hypothesis H-T02) | Supplement remark | `proofs/T04_A3_contraction/` | SE, DX; external review queued |
| T05 | Orthogonal threshold and benchmark gap (A4 = T5-S) | secondary | CONJECTURED (not proved) | Supplement remark (restored by both reviewers) | none (statement: `theorems/T05_A4_orthogonal_threshold.md`) | whole statement |
| T06 | Identifiability and exact ties (A5 = T-ID) | core | PROVED-LOCKED (all parts; wave 3); (ii)(b) uses H-T03 | Supplement remark (one sentence of T06(i) goes into Prop 1) | `proofs/T06_T07_identifiability_size_prior/` | H-T03 for (ii)(b); NIS / DUP where stated; external review queued |
| T07 | Size-only ranking ceiling and Bayes decisions (A6 = T5-C) | core | PROVED-LOCKED (all parts; wave 3) | JRSS-B Prop 1; Biometrika remark | `proofs/T06_T07_identifiability_size_prior/` | external review queued |
| T08 | Oracle joint Bernstein-von Mises limit (A7 = T6) | optional | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T08_A7_oracle_BvM.md`) | whole statement |
| T09 | Exact start, invariant kernels, whole-round minorisation (T7) | core | PROVED-LOCKED (all parts; wave 1) | Supplement lemma | `proofs/T09_T7_kernel_validity/` | none (EX-A, EX-S) |
| T10 | Feasible-addition hazards and ordered paths (T11) | core | PROVED-LOCKED (all parts; wave 3) | Supplement lemma | `proofs/T10_T11_addition_hazard/` | external review queued |
| T11 | Unified scoring and discovery ledger (L-LED / T14-D) | core | PARTLY PROVED: (iii) locked; rest conjectured | Supplement lemma | `proofs/T11_LLED_scoring_ledger/` | (i), (ii), (iv)-(vii) unproved; completion event |
| T12 | Frozen-run evidence and recorded-RB identities (T8) | core | PROVED-LOCKED (all parts; wave 1) | JRSS-B Prop 2; Biometrika remark | `proofs/T12_T8_frozen_run_identities/` | completion event (latent uninterrupted run) |
| T13 | Restricted ESS and omitted-mass identity (T10) | core | PROVED-LOCKED (all parts; wave 1); COVER / pool avoidance are clause premises | Supplement lemma | `proofs/T13_T10_restricted_ESS/` | COVER(W, eps_C), pool avoidance; snapping wording |
| T14 | First-moment evidence consistency (L-FM) | core | PARTLY PROVED: (i) locked; (ii), (iii) conjectured | Supplement lemma | `proofs/T14_LFM_first_moment_evidence/` | (ii), (iii) unproved; completion event |
| T15 | Occupancy from an evidence lower tail (L-OCC) | core | PROVED-LOCKED (all parts; wave 1); uses H-T12 | Supplement lemma | `proofs/T15_LOCC_occupancy/` | islandwise evidence lower-tail input |
| T16 | Frozen-particle and independent-island limits (T9) | secondary | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T16_T9_frozen_limits.md`) | whole statement |
| T17 | Reflection with output-specific coupling (L-RC) | core | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T17_LRC_reflection_coupling.md`) | whole statement |
| T18 | Reflected single-flip pair benchmark (B-RP) | secondary | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T18_BRP_reflected_pair.md`) | whole statement |
| T19 | Conservative working-set bounds with explicit reward targets (T12) | optional | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T19_T12_working_set_bounds.md`) | whole statement |
| T20 | Local-search semantics and conditional repair (T15) | core (i)-(ii); secondary (iii); optional (iv) | PARTLY PROVED: (i)-(ii) locked; (iii)-(v) conjectured | Supplement lemma | `proofs/T20_T15_local_search/` | (iii)-(v) unproved; H03 for (ii-C) |
| T21 | Composition theorem for the reported HPM (T14-H) | core | PROVED-LOCKED (C1, routes (a)-(f); wave 2); CONDITIONAL on H24 (route e), exposure/occurrence conditions | JRSS-B Thm 4; Biometrika Thm 4 | `proofs/T21_T14H_HPM_composition/` | H24; exposure / occurrence conditions; P(U) -> 0 |
| T22 | Aggregate start bounds and conditional concentration (T16) | core (i)(ii)(iv); secondary (iii)(v) | PARTLY PROVED: (i),(ii),(iv) locked; (iii) locked but CONDITIONAL (EXP', VIS, NL_eta, NL_avg); (v) conjectured | JRSS-B Thm 2 (with T27); Biometrika Thm 2 | `proofs/T22_T16_start_aggregation/` + `T22iii_T16_start_aggregation/` | (iii): EXP', VIS, NL_eta, NL_avg(kappa); (v) unproved |
| T23 | Basin-to-output guarantee with recording-prefix control (T18) | core (i)-(iv); secondary (v) | PARTLY PROVED: (ii) locked, (ii-c)/(ii-d) CONDITIONAL on BASIN; rest conjectured | Supplement lemma | `proofs/T23_T18_basin_prefix/` | BASIN for (ii-c), (ii-d); (i), (iii)-(v) unproved |
| T24 | Conservative terminal repair with a fixed extra-variable budget (T18') | secondary | CONJECTURED (not proved); alternative to T37 for Thm 3 | Alternative to JRSS-B Thm 3 (Gibbs-path route) | none (statement: `theorems/T24_T18p_terminal_repair.md`) | whole statement (source of H24) |
| T25 | Conditional evidence bounds through a crossing (T19) | secondary (i)-(iii); optional (iv) | PARTLY PROVED: (iv) locked, CONDITIONAL on PW2; (i)-(iii),(v) conjectured; dropped from paper selection | Dropped from paper selection (T25(iv) is nevertheless proved) | `proofs/T25iv_T19_crossing_evidence/` | PW2; (i)-(iii), (v) unproved |
| T26 | No-switch consistency at the actual budgets (T17) | secondary | CONJECTURED (not proved) | JRSS-B Thm 6 ((i)-(ii), favourable regime only); Biometrika remark | none (statement: `theorems/T26_T17_no_switch_consistency.md`) | whole statement; EXP, OP-s |
| T27 | Sequential cancellation and the iid-discovery budget (T20-C) | secondary | PARTLY PROVED: (i) locked, CONDITIONAL on H2, H3; (ii)-(iv) conjectured | Merged into JRSS-B Thm 2 with T22; Biometrika remark | `proofs/T27i_T20C_cancellation_budget/` | H2, H3; (ii)-(iv) unproved |
| T28 | Evidence loss under calibration avoidance and evidence coupling (T21-E) | core | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T28_T21E_evidence_loss.md`) | whole statement |
| T29 | HPM loss needs scoring avoidance; PIP loss needs reward control (T21-H) | secondary | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T29_T21H_HPM_PIP_loss.md`) | whole statement |
| T30 | Pilot discovery under the terminal-repair hypotheses (T21-X) | optional | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T30_T21X_pilot_discovery.md`) | whole statement |
| T31 | What the reported checks and certificates establish (T22) | core | PARTLY PROVED: (i) locked; (ii)-(vii) conjectured | (i) folded into JRSS-B Prop 2; other clauses: no explicit role | `proofs/T31_T22_certificates/` | (ii)-(vii) unproved; completion event |
| T32 | Branch-specific arithmetic and storage counts (T23-C) | core | CONJECTURED (not proved) | Supplement lemma (also supplies the cost corollary of T38(c)) | none (statement: `theorems/T32_T23C_resource_counts.md`) | whole statement |
| T33 | Numerical margins on a common scored set (T23-N) | secondary | CONJECTURED (not proved) | Supplement remark | none (statement: `theorems/T33_T23N_numerical_margins.md`) | whole statement |
| T34 | Statuses and allocation-dependent guarantees (T23-S) | core | CONJECTURED (not proved) | Supplement remark | none (statement: `theorems/T34_T23S_statuses.md`) | whole statement |
| T35 | Mass-qualified fixed-bisection obstruction and the discrepancy range (T23-R) | optional | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T35_T23R_bisection_obstruction.md`) | whole statement |
| T36 | The pilot limit as a finite-comparison rule (R-T13) | secondary | CONJECTURED (not proved); dropped from paper selection | Dropped from paper selection (FROZEN_LIST) | none (statement: `theorems/T36_RT13_pilot_finite_comparison.md`) | whole statement |
| T37 | Finite-n truth dominance and deterministic greedy repair (new, 2026-10-28) | core (new) | CONJECTURED (not proved); new 2026-10-28 | JRSS-B Thm 3 (new primary route); Biometrika Thm 3 | none (statement: `PAPER_SELECTION_20261028/new_conjectures/`) | whole statement |
| T38 | Two-regime consistency of the reported HPM (headline theorem) (new, 2026-10-28) | core (new) | CONJECTURED (not proved); new 2026-10-28 | JRSS-B Thm 5 (headline); Biometrika Thm 5 | none (statement: `PAPER_SELECTION_20261028/new_conjectures/`) | whole statement |
| T39 | Independent start-to-terminal scoring tracks with an explicit budget (contingency) (new, 2026-10-28; Astra C37) | contingency (new) | CONJECTURED (not proved); new contingency (method extension) | Contingency target only | none (statement: `PAPER_SELECTION_20261028/new_conjectures/`) | whole statement (method extension) |

Table notes. (1) "Proof location" paths are under `proofs/`; wave-1 proofs are also verbatim inside `proofs/COLLECTED_PROOFS_v2.pdf`. (2) T22: parts (i), (ii), (iv) are wave 1; part (iii) is wave 2 (EXP' etc.); part (v) is not proved. THEORY_INVENTORY's table calls T22 "(i)-(iv) partly proved"; LOCKED_PROOFS lists (i)(ii)(iv) in wave 1 and (iii) in wave 2, both locked; (v) is not locked. These agree once (iii) is read as locked but CONDITIONAL. (3) T01 and T02, and T06 and T07, share one folder and one proof file each; T25 is the folder `T25iv_...`, T27 the folder `T27i_...`.

## 3. Locked results in detail

Each entry: plain-language content, hypotheses, review record, n = 200 meaning. Hashes and files are in the one-pagers and the register.

### 3.1 Wave 1 (10 results: T09, T11(iii), T12, T13, T14(i), T15, T20(i)-(ii), T22(i)(ii)(iv), T23(ii), T31(i))

**T09 (T7)** - PROVED-LOCKED (all parts; wave 1).
- Content: The exact start sampler draws from pi0 with the right normaliser; every elementary move and the randomly ordered round leave the bridge distribution invariant; the round has a whole-round minorisation constant, and a tiny constant alone does not imply slow mixing.
- Hypotheses: EX-A (exact arithmetic), EX-S (ideal independent uniform streams). No H-xx hypothesis.
- Review: Stage A: 2 rounds (1 fatal in the lead's own gloss of (v), fixed). Stage B: 2 rounds, both verified. Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes (EX-A, EX-S): exact finite-sample statement; gives no mixing rate and no claim that a finite run reached the posterior. Per-order reversibility wording already corrected.

**T11 (L-LED / T14-D)** - PARTLY PROVED: (iii) locked; rest conjectured.
- Content: (iii) only. In the final run the chance that a chosen model S* is absent from all Q_f = 4 N_e (T + L + 5) iid start draws is exactly (1 - pi0(S*))^Q_f <= exp(-Q_f pi0(S*)). The calibration draw count is never used as an exponent.
- Hypotheses: (iii): EX-A, EX-S, CAL (calibration uses streams 0-9 only, final run streams 10-13). No H-xx.
- Review: (iii): Stage A 3 rounds, Stage B 3 rounds, all verified in the end. Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Partly: assumes the final run finishes (resource_limit caveat, 6 / 2,400 fits). Q_f >= 140,000 at n = 200, p = 500 (tier 0): for an uninterrupted final run any model fixed in advance with pi0 >= 2.1e-5 is scored with probability >= 95%.

**T12 (T8)** - PROVED-LOCKED (all parts; wave 1).
- Content: The frozen-run evidence estimate is unbiased in product form, E[Z-hat q-hat(f)] = Z q(f). For the recorded Rao-Blackwell PIP, the islandwise unnormalised product is unbiased: E_c[Z-hat_r PIP-hat_rj] = Z PIP_j. The normalised PIP estimate itself is not asserted to be unbiased. Pooled evidence is unbiased with Markov and Jensen consequences. State-dependent stopping, normalised PIPs, conditioning on favourable diagnostics and numerical perturbation each break an identity.
- Hypotheses: START (exact iid pi0 start, imported from T09(i), in the register; not an H-xx label); EX-A, EX-S, CAL.
- Review: Stage A: statement approved with changes; proof verified. Stage B round 1: both not verified (same gap, fixed); round 2: both verified. Stage C edits E12-1, E12-2 give PROOF_v6. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes, for the potential uninterrupted run (resource_limit caveat); the secondary-PIP clause is moot (D2: secondary PIP removed); unbiasedness is of the unnormalised PRODUCTS, not of the normalised PIP estimate.

**T13 (T10)** - PROVED-LOCKED (all parts; wave 1); COVER / pool avoidance are clause premises.
- Content: An exact identity links the restricted ESS to the chi-square distance between neighbouring tempered laws; on an accepted grid 1 + chi^2 <= 10/(9 (1 - eps_C)^2) under coverage. Coverage on [0,1] alone is not enough.
- Hypotheses: EX-A. Inside the corollaries: COVER(W, eps_C) (q_psi(W) >= 1 - eps_C at every psi in the evaluation grid) and pool avoidance (explicit premises, not proved for the actual run). No H-xx.
- Review: Stage A: v1 not verified (1 gap), then v2, v3 verified. Stage B: v3 not verified by both (same gap), v4 verified by both. Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes, with a wording amendment: the grid builder snaps the endpoint to 1 and re-checks ESS afterwards, so the statement's 'largest tested endpoint' needs a one-line change (RC-2 / N1-N2). COVER is unverified.

**T14 (L-FM)** - PARTLY PROVED: (i) locked; (ii), (iii) conjectured.
- Content: (i) only, singleton case. The island evidence ratio is exactly A_T/b_T; its L1 error is at most (2/(1 - eps*)) times the sum of the distances eta_t of the tempered laws from a reference model; the endpoint term cannot be dropped.
- Hypotheses: EX-A, EX-S, CAL, exact start, prescribed moves, successful calibration. EXP not needed. No H-xx.
- Review: All three Stage A/B reviewers verified v3; no fatal or gap finding. Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes for completed runs; a useful bound needs the tempered laws to stay concentrated near one model.

**T15 (L-OCC)** - PROVED-LOCKED (all parts; wave 1); uses H-T12.
- Content: If the island's evidence ratio is not too small (a lower-tail condition), the fraction of particles outside a set A is bounded in mean and tail by pi(A^c) divided by a constant plus that lower tail; an L1 bound on the ratio gives the lower tail; a pooled lower tail cannot replace the islandwise one.
- Hypotheses: H-T12 (= T12(i): E[Z-hat_r q-hat_{r,tau}(f)] = Z pi(f) at the recording positions; T12 is locked). EX-A, EX-S, CAL.
- Review: Astra #1 verified v1, v2. Astra #2 and Opus xhigh verified v2, v3, v4. No fatal or gap finding. Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes for completed runs; the island lower-tail input is open.

**T20 (T15)** - PARTLY PROVED: (i)-(ii) locked; (iii)-(v) conjectured.
- Content: (i)-(ii) only. `local_certified` means exactly weak local maximality over scored models. If S0 is the strict global maximiser (true when pi(S0) > 1/2), any completed scan centred at a neighbour of S0 scores S0 and the search moves to and certifies it.
- Hypotheses: EX-A, EXEC (scans completed). (ii-C) only: H03 (= T03(i): 1 - pi(S0) = O_P(sqrt(log n / n)), closed by T03 under T03's regime assumptions).
- Review: Astra #1 round 1 not verified (fixed), round 2 verified. Astra #2 and Opus xhigh verified rounds 1 and 2. Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes (EXEC): (ii) needs H03 and that a scan centres at a neighbour of S0.

**T22 (T16)** - PARTLY PROVED: (i),(ii),(iv) locked; (iii) locked but CONDITIONAL (EXP', VIS, NL_eta, NL_avg); (v) conjectured.
- Content: (i)(ii)(iv): the start puts mass at least (1 - q)^(s+1)/(1 + e)^s on a reference model; exact odds from reference to truth; the bridge keeps mass on S0 at every temperature (at least the smaller of the two endpoint masses). (iii): under EXP', VIS, NL_eta and a rate condition, 1 - pi0(S0) = O_P(2^B sqrt(log n) n^-kappa).
- Hypotheses: (i), (ii), (iv-a,b): EX-A only (no EXP / EXP' hypothesis); (ii), (iv) need S0 in Omega. (iv-c): premises = the conclusions of T03 and T22(iii). (iii): EXP' (assumed, not proved; Decision Point 2 D1), VIS, NL_eta, NL_avg(kappa), G, R, within-block SE; uses wave-1 T22(i). Not combinable with T27(i) on one sequence (different regimes).
- Review: Parts (i)(ii)(iv), wave 1 chain: Stage A 1 round (verified); Stage B 2 rounds, both reviewers verified v2 and v3; deferred Opus N1 (cosmetic dummy-variable rename); Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct. Part (iii), wave 2 chain: Wave 2: Astra lead (GPT-6 Astra high); two independent Sol 6.1 (high) reviewers; Astra xhigh closing review (proofs/WAVE2_REVIEW/REVIEW.md); Claude Opus audit (proofs/WAVE2_CLAUDE_AUDIT/): correct. Statement check Astra xhigh approved; Sol x2 round 1 verified, 0 findings; optional fix E-T22-1 applied (PROOF_v2).
- n = 200: (i), (ii), (iv): Yes (EX-A). (iii): correct object but EXP', VIS, NL are unverified (VIS and NL_eta doubtful); the concentration rate evaluates to >= 2,667 (B = 14), vacuous at n = 200. REGIME NOTE: R needs s0 = 14 fixed as n grows; the generator rule s0 = floor(sqrt(n)) would violate it.

**T23 (T18)** - PARTLY PROVED: (ii) locked, (ii-c)/(ii-d) CONDITIONAL on BASIN; rest conjectured.
- Content: (ii) only. Pathwise, each island's Rao-Blackwell PIP error is at most the fraction of bad rounds plus the truth term u_pi. Under BASIN the expected primary-PIP error is at most delta + (1 - a)^floor(L/r0) + (L+4)(eta + rho) + u_pi and the MPM error probability at most twice that.
- Hypotheses: EX-A, EX-S, CAL for the expectation bounds; (ii-c), (ii-d) assume BASIN(R, r0, a, eta, rho, delta) (not proved here; its statistical instances are T23(iii)-(v), not claimed). Pathwise (ii-a) uses only the setting and EX-A.
- Review: Stage A verified. Stage B 4 rounds, exposition findings only, no fatal or gap. Stage C edit E23-1 (STATEMENT.md and proof) gives PROOF_v5 (previous statement kept as STATEMENT_before_stageC.md). Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes for completed runs; BASIN is open. Note u_pi can be large: even paths that stay at the truth need not give 0/1 PIP values.

**T31 (T22)** - PARTLY PROVED: (i) locked; (ii)-(vii) conjectured.
- Content: (i) only. If the pooled evidence is unbiased (E[Z-hat] = Z) then P(Z >= alpha Z-hat) >= 1 - alpha, so 0.05 Z-hat is a 95% lower bound and E log Z-hat <= log Z; it is one-sided, not a relative-error interval, and conditioning on the final E2 flag can destroy the coverage.
- Hypotheses: H-T12 (= T12(iii): E_c[Z-hat] = Z for every successful calibration value; T12 is locked). EX-A, EX-S, CAL.
- Review: Stage A 1 round (verified). Stage B rounds 1-3, all verified by Astra #2 and Opus xhigh. Stage C: no edits. Wave 1: Opus 5.5 lead; Stage A Astra #1; Stage B Astra #2 + Opus 5.5 xhigh; Stage C campaign review Fable 5.1 (high) + Astra xhigh: correct.
- n = 200: Yes for completed runs: coverage is not conditional on completion or on flags (conditioning breaks it). 95% bound = log(0.05) + log Z-hat; the separate relative-scale field is not emitted (recoverable from log_Z_rel_m0 + log(0.05)). 'Flag not raised' is not a certificate.

### 3.2 Wave 2 (4 results: T22(iii), T21, T27(i), T25(iv))

T22(iii) is described under T22 above (wave 1 parts and the wave 2 part together). The remaining three:

**T21 (T14-H)** - PROVED-LOCKED (C1, routes (a)-(f); wave 2); CONDITIONAL on H24 (route e), exposure/occurrence conditions.
- Content: The method fails to report the truth only if no output exists, or the posterior has at most half its mass on the truth, or the truth was never scored: P(U or S-hat != S0) <= P(U) + 2 E0 delta1 + P(truth not scored). Routes (a)-(f) bound the last term.
- Hypotheses: H03 (= T03(i) conclusion; closed by T03 in its regime), H10 (= T10(i) addition floor; used only in (a)'s one-deletion corollary; closed by T10), H24 (T24 terminal-repair inputs K1(x,{S0}) >= a_n and one-round exit probability <= eta_n on R_d, plus a_n >= c_n/2 and (L+4) eta_n -> 0; used only in (e); OPEN since T24 is not proved). Also P(U) -> 0 and route-specific occurrence or exposure conditions (PX, ONE, E_G, E_TS, availability of an eligible particle). EX-A, EX-S, CAL, SR.
- Review: Wave 2: Astra lead (GPT-6 Astra high); two independent Sol 6.1 (high) reviewers; Astra xhigh closing review (proofs/WAVE2_REVIEW/REVIEW.md); Claude Opus audit (proofs/WAVE2_CLAUDE_AUDIT/): correct. Statement check Astra xhigh round 2: approved (1 restart). Sol x2: round 1 verified, no findings. Fixes E1, E3 applied; E2 (H10 may follow from the score formula) skipped; E4 optional, skipped.
- n = 200: Yes, as a conditional composition (INVENTORY B.5); H03, H24 and exposure are open. This is the bridge between the true posterior's best model (T03) and the reported HPM, which is the best model ever scored.

**T27 (T20-C)** - PARTLY PROVED: (i) locked, CONDITIONAL on H2, H3; (ii)-(iv) conjectured.
- Content: (i) only, a conditional implication. If along a chain of c feasible single additions each table ratio is about n^-1/2 (H2) and the starting model keeps normalised start mass at least c0 (H3), then pi0(S0) = p^-c n^-c/2 exp(O_P(1)).
- Hypotheses: H1 (fixed feasible completion chain; a definition), H2 (sequential ratio law, jointly two-sided O_P(1) remainders; assumed statistical input), H3 (normalised reference-mass lower bound; assumed statistical input), H4 (EX-A, EX-S, CAL, successful final execution). G / R, Gaussianity, eigenvalue or beta-min assumptions are NOT used to derive H2 or H3.
- Review: Wave 2: Astra lead (GPT-6 Astra high); two independent Sol 6.1 (high) reviewers; Astra xhigh closing review (proofs/WAVE2_REVIEW/REVIEW.md); Claude Opus audit (proofs/WAVE2_CLAUDE_AUDIT/): correct. Statement check Astra xhigh: approved. Sol x2 over 2 rounds: both verified v1 with one exposition point, both verified v2. Optional fix E-T27-1 applied (PROOF_v3).
- n = 200: Correct object; H2 and H3 unverified. Scale p^-d n^-d/2 (d = number of masked true variables) is 1.4e-4 / 7.1e-5 for d = 1 and 2e-8 / 5e-9 for d = 2 (p = 500 / 1000): potentially severe if H2/H3 hold; not established. Small iid discovery probability says nothing about Gibbs, swaps or scans.

**T25 (T19)** - PARTLY PROVED: (iv) locked, CONDITIONAL on PW2; (i)-(iii),(v) conjectured; dropped from paper selection.
- Content: (iv) only. Under the assumption PW2 (a one-step second-moment bound), Var(W_T) <= B_T by unrolling a one-line recursion, and the pooled four-island evidence ratio satisfies Var_c(Z-hat/Z) <= B_T/4, i.e. Var_c(Z-hat) <= Z^2 B_T/4. The theorem is equivalent to the PW2 recursion and adds nothing beyond it.
- Hypotheses: PW2 (assumed for the actual particle system; NOT proved; an optional partial attempt in helpers/OPTIONAL_PW2.md is unreviewed). EX-A, EX-S, CAL, completed final runs. Uses wave-1 T12(i.a), (iii), (iv.c).
- Review: Wave 2: Astra lead (GPT-6 Astra high); two independent Sol 6.1 (high) reviewers; Astra xhigh closing review (proofs/WAVE2_REVIEW/REVIEW.md); Claude Opus audit (proofs/WAVE2_CLAUDE_AUDIT/): correct. Sol x2: round 1 verified, 0 findings. Fix E5 applied (PROOF_v2); E6, E7 optional, skipped.
- n = 200: Yes for completed runs; PW2 is open.

### 3.3 Wave 3 (5 folders, 7 theorem numbers: T01, T02, T03, T04, T06, T07, T10)

**T01 (A0 = T1)** - PROVED-LOCKED (all parts; wave 3).
- Content: The v3 posterior on the standardised data is exactly the contrast-model posterior at inverse-gamma rate b0 s_y^2 (a deterministic identity). Scores at different rates differ by at most a fixed envelope; mixed-endpoint rates transfer a posterior bound at cost kappa^2, while same-rate bounds do not transfer.
- Hypotheses: (i), (ii), (iv): none beyond a valid input (n >= 3, no constant column, non-constant y). (iii) and (T): G (fixed design, Gaussian errors) and R (s0 fixed, p <= n^A, ||mu||^2/n <= M, lambda_min(R_S0) >= phi0^2, s0 <= K eventually). No SE, no beta-min, no H-xx. EX-A for exact arithmetic.
- Review: Statement checker (Opus xhigh): approved (round 2). Two rounds; both reviewers verified in both rounds; no fatal or gap finding. v3 = reviewed v2 plus notation-only fixes. Wave 3: Opus 5.5 lead; two independent Opus 5.5 xhigh reviewers (Claude Personal and Claude Work); external (OpenAI) review queued; no wave-level Fable campaign review is recorded or claimed.
- n = 200: Yes (EX-A): the exact identity (i) and the deterministic parts hold at n = 200 and are listed as meaningful at finite n (INVENTORY 0.4). Clauses (iii) and (T) are asymptotic and need G, R.

**T02 (A1 = T2)** - PROVED-LOCKED (all parts; wave 3); (ii) needs SE.
- Content: The posterior mass on models larger than m decays like 2^-m (times polynomial factors) with a tight constant, and strict supersets of the truth have mass O_P(sqrt(log n / n)) under SE.
- Hypotheses: G, R (both parts); SE (lambda_min(R_T) >= phi0^2 for every nonempty T with |T| <= min(p, m_n + s0), m_n = m_n(log n / 2)) for (ii) only. No H-xx hypotheses.
- Review: Same folder, same reviews as T01 (joint proof file). Wave 3: Opus 5.5 lead; two independent Opus 5.5 xhigh reviewers (Claude Personal and Claude Work); external (OpenAI) review queued; no wave-level Fable campaign review is recorded or claimed.
- n = 200: (i) is vacuous at n = 200: m_n = 201 / 215 (p = 500 / 1000) exceeds K = 100, so the cap already does more. (ii): the premise SE is impossible here (needs well-conditioned subsets of up to 215 / 229 columns; the data have rank <= 199). The superset rate sqrt(log n/n) = 0.163 is not small. Asymptotic only.

**T03 (A2 = T3)** - PROVED-LOCKED (all parts; wave 3; hypothesis H-T02 = T02(i)).
- Content: Under G, R, SE, a beta-min condition and H-T02, the posterior mass outside S0 is O_P(sqrt(log n / n)); PIPs are within that of the indicator of S0; the median-probability model and the global HPM equal S0 with probability tending to one; without beta-min, the large-signal variables still get PIPs tending to one.
- Hypotheses: G, R, SE, BM-C (explicit constant M* = 2 L* + 1, provisional; or BM-infinity with M_n -> infinity). H-T02 = T02(i), taken as a hypothesis (closed in the register: T02(i) is locked).
- Review: Statement unchanged (no checker needed). Two rounds: v1 both verified (exposition only), v2 both verified. Numerical check 1958/1958. Wave 3: Opus 5.5 lead; two independent Opus 5.5 xhigh reviewers (Claude Personal and Claude Work); external (OpenAI) review queued; no wave-level Fable campaign review is recorded or claimed. The combined statement 'T03 without H-T02' (T03 + T01_T02) was not separately reviewed.
- n = 200: Target: yes. As a guarantee for REPORTED outputs: no (needs T21 for scoring and T23 for PIPs). SE is impossible at n = 200 (rank <= 199). BM-C needs theta^2 >= 55.0 / 61.1 (p = 500 / 1000); executed signals are 0.64 (c = 1) and 0.16 (c = 0.5), largest 3.24, so T03(iv)'s set J_n contains none of them. Rate 0.163 times an unknown constant. Asymptotic only.

**T04 (A3 = T4)** - PROVED-LOCKED (all parts; wave 3; hypothesis H-T02).
- Content: Without any beta-min condition the posterior concentrates: prediction error, model size at most d*, parameter error and variance contract at the stated rates (a fallback rate holds if SE fails).
- Hypotheses: R1, G, R; H-T02 (= T02(i)); SE for (ii), (iv) and the sharper part of (iii); DX (min raw column SD >= d- > 0) for (iv).
- Review: Round 1: Claude Personal verified, Claude Work not verified (gap CW-F1, fixed). Round 2: both verified. Statement unchanged. Wave 3: Opus 5.5 lead; two independent Opus 5.5 xhigh reviewers (Claude Personal and Claude Work); external (OpenAI) review queued; no wave-level Fable campaign review is recorded or claimed.
- n = 200: Target: yes; it does not concern reported outputs (no coefficients are reported). Only the fallback branch survives SE failure: T04(i) and the fallback variance result of (iii) do not use SE. Fallback prediction rate eps_2^2 = 2.90 / 3.58 times an unknown C, larger than the noise variance 1: not informative. Asymptotic only.

**T06 (A5 = T-ID)** - PROVED-LOCKED (all parts; wave 3); (ii)(b) uses H-T03.
- Content: The score functions of two supports agree for every standardised response iff X_S X_S^T = X_S' X_S'^T; equal column spans alone do not suffice with this ridge prior, and under G observed exact ties almost surely have equal outer products; a fallback gives HPM = S0 when pi(S0) > 1/2; with duplicate columns two supports are indistinguishable and a two-point bound makes uniform recovery impossible.
- Hypotheses: Valid input; G for the probabilistic parts; NIS for (i)(c); DUP(a) for (iii)(a)-(d); H-T03 (= T03(i) conclusion, only as pi(S0) -> 1) for (ii)(b); 'mean-matched' pairs for the all-selector version of (iii)(c)-(d).
- Review: Statement checker (Opus xhigh): approved with required edits, applied. Round 1: both not verified (two gaps, fixed). Round 2: both verified. Wave 3: Opus 5.5 lead; two independent Opus 5.5 xhigh reviewers (Claude Personal and Claude Work); external (OpenAI) review queued; no wave-level Fable campaign review is recorded or claimed.
- n = 200: Yes (EX-A): the deterministic parts are meaningful at any n; they set what is achievable (ties and identifiability limits).

**T07 (A6 = T5-C)** - PROVED-LOCKED (all parts; wave 3).
- Content: No size-only prior can fix a within-size ranking error; the 0-1 loss is minimised by the HPM and the Hamming loss by the median-probability model; the PIP error bounds the excess risk.
- Hypotheses: Positive marginal likelihood m; a fixed total tie order; no statistical assumption for (i)-(iii)(c).
- Review: Statement checker (Opus xhigh): approved with required edits, applied. Round 1: both not verified (two gaps, fixed). Round 2: both verified. Wave 3: Opus 5.5 lead; two independent Opus 5.5 xhigh reviewers (Claude Personal and Claude Work); external (OpenAI) review queued; no wave-level Fable campaign review is recorded or claimed.
- n = 200: Yes: correctly separates global from reported quantities. Consistent (suggestive, not a test) with the c = 0.5 results where HPM beats PIP > 0.5 (370 vs 338; 340 vs 321); part of that gap may be PIP estimation error.

**T10 (T11)** - PROVED-LOCKED (all parts; wave 3).
- Content: For every data set, adding one feasible variable multiplies the start mass and the Gibbs-step score by at least r_k = (k+1)/((2p-k-1) sqrt(n+1)); a round visits an ordered set of additions with the stated probability; the visit bounds give no terminal occupancy or discovery guarantee.
- Hypotheses: EX-A, EX-S; no statistical assumption. Cites wave-1 T09(ii) and T22 Lemmas 1-3.
- Review: Statement checker (Opus xhigh): approved with changes, applied. Round 1: both not verified (same gap, fixed); round 2: both verified. Wave 3: Opus 5.5 lead; two independent Opus 5.5 xhigh reviewers (Claude Personal and Claude Work); external (OpenAI) review queued; no wave-level Fable campaign review is recorded or claimed.
- n = 200: Yes (EX-A, EX-S): visit bounds, not discovery. Gives a universal entry floor: adding any variable is never hopeless, only polynomially unlikely.

Scope notes from the register that follow from the statements: (a) T03 and T04 combined with T01_T02 give versions without H-T02, because the hypothesis text of H-T02 equals the conclusion text of T02(i); the combined statements were not separately reviewed. (b) T22(iii) (start concentrates on the truth) and T27(i) (start mass about p^-c n^-c/2) describe different regimes and must not be combined on one sequence. (c) T25(iv) adds nothing beyond PW2 (audit finding E5).

### 3.4 Index of the 19 locked folders (hashes recomputed 2026-11-02; full values in the register)

| Wave | Folder | Parts locked | Final proof | STATEMENT.md sha256 (first 16) | Proof .tex sha256 (first 16) |
|---|---|---|---|---|---|
| 1 | `T09_T7_kernel_validity` | T09 all | `PROOF_v3.tex` | `da944993732a9550` | `bab55fdf1074bdb5` |
| 1 | `T11_LLED_scoring_ledger` | T11(iii) | `PROOF_v5.tex` | `e18cefd79fe1e452` | `7f4e94c47415f2e4` |
| 1 | `T12_T8_frozen_run_identities` | T12 all | `PROOF_v6.tex` | `da90d5b0f6fb192c` | `d6b85fc0fea043a8` |
| 1 | `T13_T10_restricted_ESS` | T13 all | `PROOF_v4.tex` | `fb7fde4bac4cace6` | `4049019c683731dd` |
| 1 | `T14_LFM_first_moment_evidence` | T14(i) | `PROOF_v3.tex` | `7e94d7e38de93534` | `c12954d17b7f7383` |
| 1 | `T15_LOCC_occupancy` | T15 all | `PROOF_v4.tex` | `2c6caceb670a0a7a` | `246f07076f0d71fd` |
| 1 | `T20_T15_local_search` | T20(i)-(ii) | `PROOF_v3.tex` | `d3507eb4b44d02f5` | `2e34a79120c1e92f` |
| 1 | `T22_T16_start_aggregation` | T22(i)(ii)(iv) | `PROOF_v3.tex` | `4897c22a8bf5e913` | `08c3521c5ad28bc7` |
| 1 | `T23_T18_basin_prefix` | T23(ii) | `PROOF_v5.tex` | `050076081770fac1` | `36d38c99b7870cff` |
| 1 | `T31_T22_certificates` | T31(i) | `PROOF_v3.tex` | `0ad37b7370555f93` | `e140d9b81cd01b54` |
| 2 | `T22iii_T16_start_aggregation` | T22(iii) | `PROOF_v2.tex` | `30c4580b5396b83e` | `72cedcae732c05c9` |
| 2 | `T21_T14H_HPM_composition` | T21 (C1, a-f) | `PROOF_v3.tex` | `5a1adaa48c7d7dca` | `2dbd523465a605af` |
| 2 | `T27i_T20C_cancellation_budget` | T27(i) | `PROOF_v3.tex` | `da6d6e8a8d67ac94` | `7c875932d33165ed` |
| 2 | `T25iv_T19_crossing_evidence` | T25(iv) | `PROOF_v2.tex` | `f0f793adc40c4491` | `4f8d827f1d8a4ab1` |
| 3 | `T01_T02_contrast_dimension` | T01, T02 | `PROOF_v3.tex` | `3aa33d4477d18da6` | `626137f4bdc98a36` |
| 3 | `T03_A2_selection_consistency` | T03 | `PROOF_v2.tex` | `67e921493e5c4fa2` | `bbc0bc0a346a5147` |
| 3 | `T04_A3_contraction` | T04 | `PROOF_v2.tex` | `f844c51b9b16b451` | `81682c2623e9482f` |
| 3 | `T06_T07_identifiability_size_prior` | T06, T07 | `PROOF_v2.tex` | `ba3279b7f5a1ed90` | `fc6291c6999e1c15` |
| 3 | `T10_T11_addition_hazard` | T10 | `PROOF_v4.tex` | `92f5809afa940a1b` | `bc09ed2a15901684` |

All 38 statement and proof files match the register. The collected wave-1 document `COLLECTED_PROOFS_v2.tex` has sha256 prefix `acb3e26646196` and the PDF `c03460d790d5f` (register values).

## 4. Paper plan (FROZEN_LIST, 2026-10-28)

Premise (Felipe): every target is assumed provable after restating assumptions, minor methodology tweaks or budget sequences indexed by n; the campaign's job is to prove, restate, or establish that a target is false. Both reviewers (Fable 5.1, Astra) endorsed the proposal with changes; changes were made where both agreed, or where one raised a sound point the other did not contest. Proof status of every target is below; **none of the targets T37, T38, T39 is proved**.

### 4.1 Main text, JRSS-B version (8 results)

| Paper # | Targets | What it establishes | Proof status today |
|---|---|---|---|
| Thm 1 | T03 (lemmas T01, T02) | The posterior concentrates on the truth | T01, T02, T03 PROVED-LOCKED (wave 3); SE impossible at n = 200 |
| Prop 1 | T07 (+ one sentence of T06(i)) | The HPM is the Bayes rule for exact recovery; a size-only prior cannot fix a same-size swap | PROVED-LOCKED (wave 3) |
| Thm 2 | T22 + T27 | The start: provable mass on the truth or near it (favourable regime) and a masking lower bound (masked regime); T27 is a route-specific bound for iid start draws, not for the hybrid sampler | T22 PARTLY PROVED ((iii) CONDITIONAL on EXP' etc.); T27 PARTLY PROVED ((i) CONDITIONAL on H2, H3) |
| Thm 3 | T37 (NEW); T24 as alternative | Repair: from any near-truth centre the production local search reaches and scores the truth (finite-n bound); whichever of T37, T24 closes first becomes Thm 3 | T37 CONJECTURED (not proved); T24 CONJECTURED (not proved) |
| Thm 4 | T21 | P(wrong report) <= P(no output) + 2 E[posterior mass off the truth] + P(truth never scored); Thm 3 is intended to supply a repair route; the locked route (e) still assumes H24, and inserting T37 needs a restatement and review | PROVED-LOCKED (wave 2), CONDITIONAL on H24 (route e) and exposure / occurrence conditions |
| Thm 5 | T38 (NEW, main) | Consistency of the reported HPM in both regimes, including delivery of a near-truth centre, plus a polynomial-cost corollary; replaces T26(iii) as the headline | CONJECTURED (not proved) |
| Thm 6 | T26 (i)-(ii) | Consistency of the evidence and the PIPs, favourable regime only | CONJECTURED (not proved) |
| Prop 2 | T12 (+ T31(i)) | Unbiased evidence; islandwise E[Z-hat_r PIP-hat_rj] = Z PIP_j; Markov 95% bound folded in | T12 PROVED-LOCKED (wave 1); T31(i) PROVED-LOCKED (wave 1) |

### 4.2 Biometrika version (5 results)

Thm 1 (T03), Thm 2 (T22, with T27 as a remark), Thm 3 (T37 or T24), Thm 4 (T21), Thm 5 (T38). T07, T26 and T12 become remarks. Contingency target T39 (Astra's C37): independent scoring-only repair tracks with an explicit budget; use only if T38(b) cannot be proved for the original method; it is a method extension and would need new validation runs.

### 4.3 Supplement

- Lemmas (needed by the proofs): T01, T02, T09, T10, T11, T13, T14, T15, T20, T23, T32.
- Remarks: T04; T05 (restored by both reviewers: the g-prior + BB(1,p) HPM loses a sqrt(log n) factor to the oracle under orthogonal design, to be disclosed before a referee finds it); T06, T33, T34.
- Dropped from the paper selection: T08, T16, T17, T18, T19, T25, T28, T29, T30, T35, T36. This is a paper-selection decision; it is not a statement about whether the conjecture is true or false (DROPPED.md is a separate record of conjectures that did not survive the architecture run). T25(iv) is proved and dropped from the paper.
- Not assigned a role in FROZEN_LIST: T31 beyond its clause (i) (folded into Prop 2); T24 is the alternative to Thm 3.

### 4.4 The hole, and how it is filled

Both reviewers found the same hole: a guarantee that a near-truth particle is **delivered** and **repaired** with an explicit, finite budget. T24 and T26 alone do not provide it. The fill: **T37** (finite-n repair through the existing local search; TD(d, m) truth dominance; deterministic greedy path to S0), **T38** (a main theorem that contains the delivery step; two regimes; composes with T21, T22, T27, T37 or T24, T32), and **T39** as the fallback. Statements are in `PAPER_SELECTION_20261028/new_conjectures/`. Their risks, as recorded in the statements: the 2^s0 union in T37(ii) is loose at s0 = 14 (about 10 nats); at n = 200 the move cap l = 10 is below s0 + d = 15; eligibility of a centre in the masked regime; compatibility of T22(i) with T27 on one family; T24's factorial constant.

Rejected as targets (both reviewers): a comparative superiority theorem over SuSiE or SSL; PIP calibration; robustness to misspecification; minimax optimality. The correlated-design mechanism is instead made explicit by T37's look-alike margin (n-1) theta^2 (1 - r^2)/(2 sigma^2). No current theorem explains SMC-BVS's weak-signal advantage (INVENTORY C).

### 4.5 Restatement notes (concise)

- **Common setting.** Triangular array with s0 fixed (14 in the study), p_n <= n^A and B <= 16, so s0 = floor(sqrt(n)) is not covered. Separate the potential uninterrupted run from the output-available event and never condition on observed completion. Prove compatible premises jointly: one statistical family must satisfy every premise used in T38.
- **T03 / T02.** Replace T02(i)'s geometric tail 2^-m by the exact BB(1,p) tail (m_n falls from about 200 to s0 + O(s0 log n / log p), so SE on sets of size <= m_n + s0 <= K becomes meaningful at n = 200); restrict SE to the comparison unions actually used; use BM-infinity or an unnamed constant instead of M*. None of this yields a useful finite-n frequentist error rate.
- **T22.** Prove EXP, visibility and leakage for the actual X-dependent partition; for T38(b) use the deterministic reference bound (the reference may differ from S0). Failure points: normalised mass and uniform score remainders.
- **T27.** Replace the assumed ratio law by a bounded-leakage condition along the chain (two-sided law with a controlled multiplier); the exponent depends on the budget.
- **T37.** The union bound is the weak point; use the extra-scan rule or a closer centre because l = 10 < s0 + d = 15.
- **T24 (alternative).** Evaluate LK only at states containing S0 and charge look-alike additions to d; replace the 1/(s0+d+B+2)! constant by a progress argument of one correct step per round; failure point EXIT under internal non-Gibbs moves.
- **T38.** Eligibility in the masked regime (best-scored model lands in R_d, or use tweak LS0: local search also from the start mode, addable after the fact); compatibility of T22(i) with T27; cost corollary from T32.
- **T26 (i)-(ii).** Require (T_n + 1) Delta_n -> 0 and (L_n + 4) rho*_n -> 0; remove the secondary PIP; no claims about the masked regime.
- **T12.** Freeze everything before the final randomness; use the islandwise product identity (it is NOT an identity for the pooled Z-hat times the primary pooled PIP); drop the secondary PIP; validate floating point separately.
- **T21.** Keep P(U) and the non-launch terms; "scored" includes rejected proposals.

Suggested campaign order (both reviewers): T37; T02(i) tail sharpening and T03 restatement; T22(i)/(iii) and T27 on one compatible family; T38; T24 only if T37 fails; T39 only if T38(b) fails; bookkeeping restatements (T12, T21, T26(i)-(ii), T07, T05 remark).

## 5. Open obligations

### 5.1 Hypotheses and conditions still open (LOCKED_PROOFS section B)

| Open item | Appears in | What is missing |
|---|---|---|
| H24 (T24 terminal-repair inputs: K1(x,{S0}) >= a_n and one-round exit probability <= eta_n uniformly on R_d, plus a_n >= c_n/2 and (L+4) eta_n -> 0) | T21 route (e) | T24 is not proved and not in the register; the proof of (e) derives the H-round bound from these inputs but does not establish them |
| PW2 (one-step second-moment bound for the actual particle system) | T25(iv) | not proved for the actual method; the optional partial work in `T25iv_T19_crossing_evidence/helpers/OPTIONAL_PW2.md` is unreviewed |
| EXP' (log-ratio expansion with O_P(1) remainder; Decision Point 2 D1) | T22(iii) (assumed); discussed but not assumed in T27(i) | not proved; the audit sketch that EXP' may follow from G, R and within-block SE is unverified |
| VIS, NL_eta, NL_avg(kappa) | T22(iii) | regime or design conditions, not proved |
| H2 (sequential ratio law), H3 (normalised reference-mass lower bound) | T27(i) | statistical inputs, not proved (H1 is a definition, H4 collects EX-A, EX-S, CAL and successful execution) |
| BASIN(R, r0, a, eta, rho, delta) | T23(ii-c), (ii-d) | not proved; its statistical instances T23(iii)-(v) are not in the register |
| P(U) -> 0, PX, ONE, E_G, E_TS, availability of an eligible particle | T21 | conditions on the run, not proved |
| COVER(W, eps_C) and pool avoidance | T13 (ii), (iii), (iv) | explicit premises of those clauses |
| G, R, SE, BM-C or BM-infinity, DX, NIS, DUP(a) | T01_T02, T03, T04, T06_T07, T22(iii) | regime and design assumptions, not proved |
| EX-A, EX-S, CAL, EXEC | throughout | declared idealisations |

### 5.2 What would add the most (THEORY_INVENTORY section E, in the inventory's order)

1. **Cheap empirical check.** For each c = 1 miss, compare the exact posterior score of the truth with that of the reported model, including numerical and tie checks. If the truth scores higher it was a search failure (never scored); if lower, the target misranks it (prior / statistics). It does not exclude a concurrent search failure.
2. **Bookkeeping restatements with no new mathematics:** the completion / availability event for T11(iii), T12, T14, T15, T23, T25, T31; T13 snapping wording; dropping T12's secondary-PIP clause.
3. **A finite-n version of the statistical half:** measured premise checks on realised designs; a proof review of SE restricted to models of size <= K + s0; a sharper or explicit beta-min constant. Feasibility alone does not guarantee useful bounds.
4. **The main open gaps.** For the HPM: an unconditional route to "the truth is scored", through EXP'/VIS/NL in the favourable regime, or H2/H3 plus T24 (H24) in the masked regime (now the T37 / T38 programme). For PIPs and evidence: BASIN and PW2, as separate priorities.
5. **Method note.** cut_group fired in 2,398 of 2,400 fits, so it discriminates poorly at n = 200; investigate before redefining or dropping it. A method decision, not a theorem.

### 5.3 The resource_limit restatement and the n = 200 reading

**Potential uninterrupted run.** A runtime guard can stop a fit when its time / memory budget is hit, either partway through the final run or after the final local search; in both cases the fit reports no evidence or PIPs. 6 of 2,400 fits ended `resource_limit`, all in S5; the stopping phase is not recorded. T11(iii), T12, T14(i), T15, T23(ii), T25(iv), T27(i) (retained setting) and T31(i) describe a run that always finishes. Their distributional guarantees (unbiasedness, coverage, probability bounds) are about the **potential uninterrupted run** given calibration; pathwise identities hold on completed trajectories. Neither covers the stopped fits, nor statements "conditional on the fit finishing" (selecting on completion is a different statement). The fix is a restatement with a latent uninterrupted run plus a separate "output available" event (T21 already does this through P(U)); it needs little new mathematics but narrows the claim, and six failures cannot by themselves show the effect is negligible.

**Global versus reported.** T03's HPM / MPM / PIP consistency and T06(ii) concern the **true posterior**. The code reports the best **scored** model and **estimated** PIPs. "The method recovers the truth" is wrong without the computational bridge: T21 (scoring) plus T23 (PIP accuracy), both conditional. T07 states the distinction correctly (T07(iii)). The gap between the global and the reported object is T21's last term, P(truth never scored).

**What is meaningful at n = 200.** The exact finite-sample layer: the posterior identity (T01); tie and identifiability limits (T06); HPM / MPM decision theory and the size-prior ceiling (T07); exact start and valid moves (T09); the addition floor (T10); the iid miss probability (T11(iii)); the frozen-run identities (T12: the unnormalised product is unbiased, not the normalised PIP); the grid identity (T13); local-search semantics (T20(i)); the composition inequality (T21); the deterministic start bounds (T22(i)(ii)(iv)); the 95% evidence lower bound (T31). The asymptotic statements are not numerical guarantees: SE cannot hold (it needs well-conditioned subsets of up to 215 / 229 columns, rank <= 199); the explicit beta-min constant of T03 asks for squared signals >= 55 against 0.64 (c = 1) and 0.16 (c = 0.5); the rates evaluate to 0.16, 2.9 and even 2,667 (T22(iii)); T02(i)'s size cutoff 201 / 215 exceeds K = 100. This does not make the theorems wrong: the 2,400-fit results stand on their own and the theory explains mechanisms, not numbers. Regime conditions: G, R, NIS, DX and within-block SE are plausible; VIS and NL_eta are doubtful; EXP', NL_avg and BM-infinity are unknown. R needs s0 = 14 fixed as n grows; the generator's rule s0 = floor(sqrt(n)) would violate it.

**Link to the fits (suggestive, not tests).** At c = 1, 90-92% of wrong answers are "truth plus one or more extra variables" with nothing missed; the data do not show whether the posterior ranked the superset above the truth or the truth was never scored (item 1 above settles it). At c = 0.5, HPM beats PIP > 0.5 (370 vs 338; 340 vs 321), consistent with T07. No locked theorem explains the weak-signal advantage over the competitors.

### 5.4 Open decisions for Felipe (GAP_LIST section E, theory items 1, 7, 8, 10, 12)

1. **Adopt the 21 locked proof entries** (briefing section 6.1.1): never answered. Until then every theorem here is "not adopted".
7. **Novelty check:** "report the best model ever visited" versus Hans, Dobra and West (2007) shotgun stochastic search. Not done. It matters for the novelty claims of T21 and T38.
8. **THEORY.tex "Recommendations to the author" (10 items)**, the pair-addition move (LEVERS V10) and the never-firing warnings E1 / E3 / local_limit: deferred, not decided.
10. **Wave-3 proofs:** the external (OpenAI) review is still "queued" in LOCKED_PROOFS.md. A search of the proofs tree on 2026-11-02 found no file newer than the register and no record of an external wave-3 review, so "queued" is the only status the sources support. The v2.1 results never got a RESULTS.md or an external review.
12. **Tension** between "use all prior knowledge" (principle 4) and "I don't care about prior attempts" (D6) for the theory phase. This document follows D6 for the legacy results (section 7) and keeps their facts in one short table.

## 6. Dependency graph

The graph is in `THEOREM_MAP.md` (36 conjectures, ranks, the arrow list "A -> B: B uses A", and the recommended proof order). Where a theorem file's "Used by" line and the graph disagree, the graph governs (36 non-mirrored "Used by" citations are interpretive). T37-T39 are not in the map: T37 feeds Thm 3 and T38(b1); T38 composes T21, T22, T27, T37 or T24, T32; T39 is T38's fallback.

**Closure of hypotheses by locked results** (LOCKED_PROOFS section A):

| Hypothesis | Used by | Discharged by | Status |
|---|---|---|---|
| START | T12 | T09(i) | Closed (wave 1) |
| H-T12 (T12(i)) | T15 | T12 (i.a), (i.b), (i.c) | Closed (wave 1) |
| H-T12 (T12(iii)) | T31 | T12 (i.a) and (iii) | Closed (wave 1) |
| H03 (1 - pi(S0) = O_P(sqrt(log n / n))) | T20 (ii-C); T21 | T03(i) | Closed in the regime of T03 (G, R, SE, beta-min are T03's conditions; T20 and T21 do not list them) |
| H-T02 | T03, T04 | T02(i) | Closed (wave 3); by statement text match |
| H-T03 | T06(ii)(b) | T03(i) | Closed under T03's regime assumptions |
| H10 | T21 (a) one-deletion corollary | T10(i) | Closed (wave 3) |
| premise "1 - pi(S0) -> 0" | T22(iv-c) | T03(i) | Closed under T03's regime assumptions |
| premise "1 - pi0(S0) -> 0" | T22(iv-c) | T22(iii), conclusion 3 | Closed only under T22(iii)'s own assumptions (EXP', VIS, NL_eta, NL_avg(kappa), G, R, within-block SE) |
| wave-1 citations in waves 2 and 3 | T22(iii), T25(iv), T10 | wave-1 rows | Closed |
| H24 | T21 route (e) | none (T24 unproved) | **OPEN** |

Nothing is closed by the new conjectures: they are targets, not results.

## 7. Legacy results (pre-v3 method; not part of the v3 paper plan)

Campaign decision D6: old attempts are out of scope for the shipped method. These were proved on 2026-10-14/15 for the earlier "Proposed project" method (composite-start SMC, earlier draft), with a different statement set. They are listed so their existence is recorded, not so they can be cited for v3. Every row: **proved, not adopted, applies to the pre-v3 method**. Files (final proof and status only) are proposed for `legacy_pre_v3/<folder>/`; OLD means the old local project root.

| Old folder | Results | Proof file and version | Review rounds recorded | Remarks |
|---|---|---|---|---|
| foundations | F4, L4, L6, P6, P7 | `PROOF.md` v3 (post-audit edits 2026-10-15; `PROOF_pre_audit.md` kept) | 3 six-reviewer rounds (3 Opus + 3 Astra xhigh each); round 1 six "not verified", no fatal error in any proof; rounds 2 and 3 no fatal or gap finding | Three draft wording flags: L6(iii)-(v) need b_pi = p; P6 needs a symmetric neighbour list; resampling decisions must condition on the population |
| elementary_I | P1, T1, L1, L2, L3, L5, L7 | `PROOF.md` (v3 per the memory record; `review/` also holds `PROOF_v4.md`: final version to be confirmed) | 3 review rounds with 3 Opus + 3 Astra; no error found | Delta_det >= 0 (Theorem 4.4); L3 is an equality inf q_phi(S*) = min{pi0(S*), pi(S*)} |
| T3_T11 | T3, T11, (R-suff) | `PROOF.md` v3 | six blind reviewers (3 Opus + 3 Astra xhigh) on v2; all 18 rulings applied in v3; v3 remark-level fixes not re-reviewed | (R) needs only O(n^-1/2); T11(iv) is false under the cap floor(n/2) |
| T4 | T4 (two-state switch: schedule is cheap) | `PROOF.md` (post-review; v1 kept as `review/PROOF_v1_prereview.md`) | `review/` holds two Opus reports (REVIEW_A: "every step verified"; REVIEW_C); no STATUS file | Record of the final round: record not found |
| T5 | T5 (mode loss) | `PROOF.md`; `ADDENDUM_20261015.md` (stage-dependent leakage in (v)) | self-checked only; not reviewed by the six-reviewer cycle | all five parts true as stated with added hypotheses; adaptive schedules: (iii) survives only as a conditional-law statement |
| T6 | T6, T9a(i) | `PROOF.md` v4 (post-round-3 edits confined to a remark; not re-reviewed) | 3 rounds with 3 Opus + 3 Astra xhigh; T6 verified by all six; whole document verified by the 3 Opus, withheld by the 3 Astra only for the section 6.4 remark | nonasymptotic form; wording fix: T9a(i) is O((s0+1) l_n); do not claim "for every p" |
| T7_T8 | T7, T8, T10 | `PROOF.md` v2 | one blind round, 3 Opus xhigh, all "every step verified"; Astra reviewers not run | rate needs SE at the m_n built with omega_n >= (1/2) log n; beta-min scale sigma*^2; Laurent-Massart citation not checked |
| T9_C9 | T9, C9, T9a(iii) (sharp dimension bound, Theorem 13) | `PROOF.md` v3 | round 1: 3 Opus + 3 Astra; round 2: 3 Astra (the 3 Opus lost to a session reset); v3 not re-reviewed | C9 amended: needs centred rows and sub-Gaussianity uniform in n |
| P2 | P2 (several switches) | `PROOF.md` = `PROOF_v4.md` | 3 six-reviewer rounds, 0 fatal | K_1 explicit; additivity by tight greedy steps |
| Pb1 | Pb1 (exact selection error of the HPM under orthogonality) | `PROOF.md` v4 | 3 rounds, no error in the numbered results | sharp HPM threshold tau_n = log D + 2 log((2p - s0)/s0), limit Phi(c)^s0; conceptually related to v3 T05 |
| elementary_II | Ex1, Ex2, C1, P3, P4, Pb2 | `PROOF.md` (v1; round-1 reports present) | round-1 reports from 3 Opus + 3 Astra are on disk; STATUS ends at their launch | final review outcome: record not found |
| elementary_III | P5, P8, P9, P10, P11 | `PROOF.md` v2 (v1 in `review/PROOF.md`) | round 1 (3 Opus + 3 Astra) and rulings; round-2 packet prepared, no round-2 reports found | four of five true as stated; P8(iii) true in a corrected form |
| Pb4 | positive crossing result | none | none | STATUS: "nothing written yet beyond this file"; no result |
| _audit | Sol audit experiment of 2026-10-15 | edits to the above `PROOF.md` files (backups `PROOF_pre_audit.md`) | 22 GPT-6.1 Sol auditors, 3 Opus adjudicators | a process record, not a result; `PLAN.md` and `results.tsv` are proposed for import |

Sources for this table: each folder's STATUS and top-level files, and the project memory notes for the foundations, elementary_I, T3_T11, T5, T6, T7_T8, T9_C9, P2 and Pb1 threads. Where the two differ the folder files were preferred. Pb4 and T4 have no clear final record; elementary_II has no final-outcome record.

## 8. File map

Existing = present in the target repo baseline of 2026-11-02 (hash identical to the local file, checked). Proposed = in `THEORY_IMPORT_LIST.tsv` (not in the repo yet).

| What | Repo path | State |
|---|---|---|
| This document | `Docs/THEORY.md` | proposed |
| One-pagers T01-T39 | `Docs/Theory/one_pagers/T01.md` ... `T39.md` | proposed (this draft) |
| Conjecture statements T01-T36 and shared definitions | `Docs/Theory/theorems/T01_...md` ... `T36_...md`, `00_COMMON.md` | existing |
| New conjectures T37, T38, T39 | `Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/` | proposed |
| Paper-target selection (FROZEN_LIST, PROPOSAL, Fable and Astra reviews) | `Docs/Theory/PAPER_SELECTION_20261028/` | proposed |
| Theory inventory, empirical summary, plan, context | `Docs/Theory/INVENTORY_20261028/` | proposed |
| Register of locked proofs, proof status | `Docs/Theory/proofs/LOCKED_PROOFS.md`, `PROOFS_STATUS.md` | existing |
| Statements as proved (all 19 folders) | `Docs/Theory/proofs/<folder>/STATEMENT.md` | existing |
| Final proofs, wave 2 and wave 3 (tex + pdf) | `Docs/Theory/proofs/<folder>/PROOF_vN.tex` and `.pdf` for T01_T02, T03, T04, T06_T07, T10, T21, T22iii, T25iv, T27i | existing |
| Final proofs, wave 1 (tex only) | `Docs/Theory/proofs/<folder>/PROOF_vN.tex` for T09 (v3), T11 (v5), T12 (v6), T13 (v4), T14 (v3), T15 (v4), T20 (v3), T22 (v3), T23 (v5), T31 (v3) | proposed |
| Collected wave-1 proofs | `Docs/Theory/proofs/COLLECTED_PROOFS_v2.pdf` (157 pages) and `.tex` | existing |
| Collected-document assembly notes and Stage C reviews (Fable, Astra) | `Docs/Theory/proofs/COLLECTED/ASSEMBLY_NOTES.md`, `COLLECTED/review/` | proposed |
| Wave-2 closing review and Claude audit | `Docs/Theory/proofs/WAVE2_REVIEW/`, `WAVE2_CLAUDE_AUDIT/` | proposed |
| Final report, claims log, status of each locked proof | `Docs/Theory/proofs/<folder>/FINAL_REPORT.md`, `CLAIMS_OF_FATAL_FLAWS.md`, `STATUS.md` | proposed |
| Reviewer reports and rulings (final-round files only; logs and packets excluded) | `Docs/Theory/proofs/<folder>/review/` | proposed |
| Architecture-run records | `Docs/Theory/THEOREM_MAP.md`, `DROPPED.md`, `RULINGS.md`, `STATUS.md`, `THEORY_BRIEF.md`, `THEORY.tex`, `THEORY.pdf` | existing |
| Failed attempts of the theory run | `Docs/Theory/FAILED_ATTEMPTS.md` | proposed |
| Legacy results, final proof and status per folder | `Docs/Theory/legacy_pre_v3/<folder>/` | proposed |

Cautions for the import. (1) The `STATUS.md` files of the four wave-2 folders (T21, T22iii, T25iv, T27i) still name superseded proof versions; the register is the current record. (2) `PROOFS_STATUS.md` and several folder files carry the working-thread identifiers of the proof campaign and some carry local or cluster paths; see `SECRETS_SCAN_THEORY.md` and decide before publication. (3) The repo's `THEORY.pdf` and `THEORY.tex` are the 2026-10-20 architecture-run output; they predate the register and the paper selection. (4) `LOCKED_PROOFS.md` is a 2026-10-23 register; it has not been updated for the 2026-10-28 inventory, which only checked it (38 of 38 locked file hashes matched; recomputed again on 2026-11-02 for the 38 statement and proof files: all match).
