# THM-INV digest: API-* reports (9)

Sources: `git show origin/theory/<ID>:theory_campaign/<ID>/REPORT.md` for API-PXNGAP, API-N200, API-VSTAB, API-MASKZPIP,
API-T26BUD, API-POS, API-FAVIID, API-RESID, API-AUDIT; plus skims of API-AUDIT/AUDIT.md, API-T26BUD/PROOF.md and
API-MASKZPIP/PROOF.md (statement parts). Slot names follow `Docs/THEORY_PRIORITIES.md` (Thm 1 = T03; Thm 2 = T22+T27; Thm 3 = T37/T24;
Thm 4 = T21; Thm 5 = T38; Thm 6 = T26(i)-(ii); Prop 2 = T12/T31(i)).

Conventions in this file. Every result in every report below is a **candidate** (not reviewed, not adopted) unless the report says
otherwise. Status words are copied verbatim from the reports; nothing is upgraded. "(?)" marks my own uncertainty. "Idealisation tags":
LS0 = local search also from the start mode (NOT in the production core, see API-AUDIT); iid-final = iid final draws; frozen-C =
frozen calibration object; exact-Gram/LH = exact centred Gram LH design (p <= n-1); LH-iid = rows iid N(0, Sigma_LH); p-fixed; one-stage
= grid {0,1}. Method components: START (start/blocks/pi0), BRIDGE (bridge/schedule), MOVES (move kernel), CAL (calibration and
rebuilds), ISL (islands and pooling), ZHAT (Z-hat and lower bound), PIP, DEC (HPM/MPM decision), LS (local search and certification),
FLAGS (flags/diagnostics), RES (resource limits), POST (statistical posterior).

Study as run (context repeated from THEORY_PRIORITIES): n = 200, p in {500, 1000}, s0 = 14, B = 14, K = 100, six scenarios S1-S6, c in {1, 0.5},
100 replicates per cell, 2,400 fits; production v3 has no LS0.

---------------------------------------------------------------------------------------------------------------------

## 1. API-PXNGAP (Fable 5.1): closing A-REV3's p >> n gap for Thm 5(b1), LS0 route, LH-iid

**Task question.** Can Thm 5(b1) (masked regime; start mode plus LS0 repair) be proved on LH-iid for every polynomial p <= n^A, p >> n included, with every premise discharged on the random design?

**Headline.**
- **PROVED (candidate), given the locked [T22i], [T22ii], [T03], the classical [CONC], and W7-PART Theorem B:** Thm 5(b1) with LS0 holds on LH-iid for every polynomial p <= n^A, every premise discharged on the random design (partition recovery, start-mass control, eligibility, TD' for LS0, pi(S0) -> 1, composition inequality).
- **COUNTEREXAMPLE (deterministic), stated as an obstruction:** the family needs (SIZE) g <= B_n < 2g; with the study's groups of 5 (2g <= B) the partition packs >= 2 groups per block and LH masking is not available, "so the theorem does not describe the study's own generator" (PROOF 11 (O1)).
- The proof is **asymptotic**: the proven (D_S) margin is negative at n = 200 for typical parameters (PROOF 11 (O5)); exact small-scale checks show the route succeeding at n in {100, 200, 400} because actual margins are much larger than the proven bound.
- **Not claimed:** P(U) -> 0; the original method without LS0 (P7 / W5-R1 remain GAP, c = 1 only); masked PIP/evidence accuracy; anything about adaptive packing of groups of 5.

| Result | Statement (one line) | Status | Hypotheses (named) | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| Thm 5(b1) LS0, LH-iid (PROOF 10), conclusions (R)(S)(E)(T)(P)(C)(K) | P(blocks != groups) <= (2/(sqrt(pi)(1-rho))) p^2 sqrt(n) e^{-(n-4)I*}; 1 - pi0(S°) = O_P(sqrt(log n/n)), pi0(S0) = p^{-c}n^{-c/2}e^{O_P(1)}; P(LS0 scores S0) -> 1 and certifies -> 1; 1 - pi(S0) = O_P(sqrt(log n/n)); P(O and S+ != S0) <= 2E0 d1 + D_n; liminf P(O, S+ = S0) = 1 - limsup P(U); LS0 cost <= 1 + (l_n+1) max_k[p + k(p-k)] scores | PROVED (candidate) | (F) LH-iid with fixed g, c >= 1, v >= 0, rho, psi, beta, sigma^2; (SIZE) g <= B_n < 2g; 18 <= p <= n^A, p -> infinity; s0 = 2c+v fixed; (OP) EX-A, EX-S, CAL, SR, GUARD, OP-LS0; v3 budgets indexed by n; inputs T22i, T22ii, T03 (locked), CONC, W7-B | **Idealised**: LS0 (method change, not in production), LH-iid, groups of 9-16 with (SIZE), s0 = 2c+v fixed; asymptotic only. Not the study generator (groups of 5) | START, LS, DEC, POST | validity (consistency of reported HPM), cost (LS0 score count) |
| Theorem R = W7 Thm B on (SIZE) | partition recovery probability bound | VERIFIED on SIZE by A-REV6 (candidate input) | (SIZE); LH-iid | idealisation (design) | START | validity |
| Lemma Tr-J | truncated Beta moment / uniform tail for any fixed dimension J, u <= n/4, polynomial families, t_n = 8(D+1) log n | PROVED (candidate) | Laurent-Massart; Wendel | analytic tool; limit statement (explicit bound > 1 at n <= 3,200) | POST | validity (asymptotic) |
| Lemma E | explicit score expansion F(A) = log w - ... + R_A, |R_A| <= kappa_E = 0.52/c_E + 1 on polynomial families with Gram lower bound | PROVED (candidate) | lambda_min(R_A) >= phi_0^2 | analytic tool; bound loose ~100x in checks | POST | validity |
| Lemma U(U3), Lemma Lambda(a), Lemma T, Lemma LS | signal margin; random-partition quantifier discipline; LS0 lattice route (c moves; S0 scored iff l >= c-1; certified iff (L) and l >= c) | PROVED (candidate) | as above | LS0 | LS | validity |
| Sup. p range | theorem needs no p-restriction beyond p <= n^A | PROVED (candidate) (part of above) | | | | |
| p superpolynomial (log p = o(n)) | discovery half plausibly survives, but T03 locked only for p <= n^A | CONJECTURE (O2) | | | | |
| Dilution masking family (study regime, groups of 5) | the right object for the study regime | CONJECTURE (PXN 14) (outside task) | | | | |
| P7 / W5-R1 no-tweak route, c = 1 | no-LS0 theorem on c = 1 | GAP (A-REV6, kept); Lemma Tr-J(c) covers R1 Step 2's call "not re-verified here beyond the lemma substitution" | | as-run algorithm but c = 1 only | | |

**Empirical facts for coverage (exact small-scale, not the study; g = 10, rho = .7, psi = .5, c in {1,2}, v = 1, B = floor(sqrt n)).**
- Partition recovered 60/60. Masking: log pi0(S0) ~ -c(log p + 0.5 log n) + O(1) (-8.7 vs -8.8 predicted at (200, 500, c=1)).
- 1 - pi0(S°) is 0.2-0.5 at n in {200, 400}: the T22 bound is often vacuous. Start mode = S° in 33/36 cells at n >= 200; 0/10 at n = 100, c = 2.
- LS0 scores S0 in 56/60 overall, 35/36 at n >= 200; certifies in 33/36 at n >= 200 (11/60 overall (L) failures, 3/36 at n >= 200; these are posterior misses charged to 2E0 d1).
- Proven (D_S) margin negative at every cell; observed lattice margins -4 to +11 nats decide at these n. The one n >= 200 scoring failure (c=2, p=1000) is a genuine D_S failure.
- Lemma checks: Tr-J 0 violations; margins 60/60; Lemma E remainder range 0.31-0.41 nats vs proven 2kappa_E ~ 38.

**Disagreements / tensions.**
- vs THEORY_PRIORITIES section 5 and API-N200: LS0 route repairs through "LS0 scores S0"; data say S0 is scored in 2,394/2,394 completed fits by the Gibbs route anyway, "the final local search repaired 0 fits" (PRIORITIES, preliminary). API-N200: "no (LS0 would not change it: S0 is scored anyway)". Also API-AUDIT: production has no LS0.
- vs study generator: "the theorem does not describe the study's own generator" (groups of 5, 2g <= B).
- PXNGAP proves p >> n on LH-iid; API-VSTAB's no-LS0 theorem is exact-Gram with p <= n-1 (p_n = 9 floor(n/18)); the two cover different designs and different methods (with vs without LS0).

**Needs escalation.** (1) Lemma Tr-J(c) constants (x = t'/2 - sqrt(jt'), t' >= 6j; family counts D = A(s0+2)). (2) Lemma E (E2) commuting-matrix identity and bound ||P_A y||^2 <= n-1; (E3) minimisation. (3) Lemma Lambda(a): Haar span of null columns given equicorrelated null groups. (4) Theorem R cited as W7 Thm B; Hotelling-density bound (W7 Lemma 2) cited not re-proved. (5) OP-LS0 + GUARD closure taken from W6; confirm against engine ledger behaviour (centre emission) (cf. API-AUDIT item 3). (6) Lean-readiness: Lemma LS, (C), Tr-J(a), (E1), (E2) are finite. Confidence card: true "high", provable "high", method change **yes, LS0**.

**Property with NO guarantee (quotes).** "Not claimed: P(U) -> 0; the original method without LS0 (P7 / W5-R1 remain GAP, c = 1 only); masked PIP/evidence accuracy; anything about adaptive packing of groups of 5." Also: "Making the (D_S) bound non-vacuous at n = 200. Not attempted."

---------------------------------------------------------------------------------------------------------------------

## 2. API-N200 (Fable 5.1): a quantitative finite-n theorem that speaks to n = 200

**Task question.** Is there a finite-n statement, not vacuous at the study's n = 200, for the reported HPM of the method as run?

**Headline.**
- **Theorem N200 (PROVED, elementary, every n):** P(U or S-hat != S0) <= P(U) + Pi(X) + P(O, S0 never scored), with Pi(X) := P0(S† != S0 | X) the posterior-miss probability of the design (algorithm-free); matching lower bound P(U) + P(O, S† != S0) - P(O, S† not scored). Implies T21's (C1) term by term; first version whose middle term is not vacuous at n = 200 (2E0 d1 > 1 there; Pi(X) is 5-75% per cell).
- Rigor stops at Pi(X): lower bracket max_e p_e <= P0(L|X) <= P0(L2|X) <= Pi(X) PROVED (exact score); closed forms p_e are "PA-exact", not rigorous; **"An upper bound on Pi(X) at finite n is OPEN"**.
- Discovery term at n = 200 is **measured**, not proved: S0 scored in 2,394/2,394 completed fits, 0 search misses; exact 95% UB 0.125% per fit; a-priori routes vacuous (Q_f pi0(S0) <~ 1e-6, sigma^2-dilution).
- n = 200 table: predicted wrong 558 vs observed 571 over 2,400 fits (RMS z = 1.08 over 24 cells, max |z| = 2.5).

| Result | Statement | Status | Hypotheses | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| Lemma 1 | on O: {S-hat ≻ S0} ⊆ {S† != S0}; {S0 ≻ S-hat} ⊆ {S0 not scored}; {S† scored} ⊆ {S-hat = S†}; {S† != S0} ⊆ {pi(S0) <= 1/2} | PROVED | EX-A, total order ≻ (larger F, smaller size, lexicographic) | **As-run** (no sampler hypothesis) | DEC | validity |
| Theorem N200 (i)-(iv) | identity; upper bound (ii); lower bound (iii); (iv) P(O, S† != S0) <= P(pi(S0) <= 1/2) <= 2E0 d1 | PROVED | EX-A and definition of S-hat; G; nothing about the sampler | As-run (exact scores) | DEC, POST | validity (finite-n, any n) |
| Proposition 2 (brackets for Pi) | max_e p_e <= P0(L|X) <= P0(L2|X) <= Pi(X); P0(L|X) <= sum_e p_e | PROVED (exact score); closed forms for p_e: PA-exact (O-SWAP Props 1-3), not rigorous | G, EX-A; PA for closed forms | As-run designs (study's own regenerated designs) | POST | accuracy (lower bracket) |
| Finite-n upper bound on Pi(X) | P0(L|X) + r_n(X) with explicit r_n | OPEN (union bound over Hamming balls provably fails; convexity "shell" argument: PROOF SKETCH, only orthogonal nulls, remainder ~6e-4) | | | POST | accuracy |
| Discovery term | P(O, S0 not scored) <= T21 routes a-f (a priori, vacuous at n = 200); <= box-certificate route (O-CERT C5, per fit without S0); observed 0/2,394 | a priori: vacuous; measured: 0/2,394 (95% UB 0.125%); C5 tabulation not yet run | | As-run (measured) | MOVES, LS, FLAGS | failure mode (search miss) |
| n = 200 table | predicted wrong = U + sum P-hat0(L|X): 558.1 vs observed 571; per (p,c): 41.5 vs 41, 40.3 vs 40, 228.3 vs 230, 248.0 vs 260 | empirical | O-SWAP exact-score MC (R = 40 draws/design) | As-run | POST | accuracy |
| p = 12 exact enumeration | Pi vs P(L), P(L2), 2E0 d1 at n = 40: Pi 0.08-0.79 vs 2E0 d1 0.93-1.95 | empirical | n = 40, s0 = 3, three designs | not the study | POST | accuracy |

**Empirical facts.** U = 6/2,400 (resource limit); posterior misses 565; observed wrong 571; supersets at c = 1, same-size swaps and dropped truths at c = 0.5 (predicted type matches); O-CERT: pi(S0) <= 0.37 even on correct fits; pi0(S0) medians 1e-11 to 1e-26 (O-DILUTE); T21's 2E0 d1 is 0.93-1.95 in the p = 12 exact study, vacuous. Per-cell: |z| <= 1.5 in 20/24 cells.

**Disagreements / tensions.** None with other reports in this set; consistent with API-RESID (565 posterior misses, 0 search misses, 6 resource-limit) and with PRIORITIES section 5. Tension with PXNGAP: discovery bounds there need LS0; here "LS0 would not change it". It supersedes (as a finite-n form) T21 "2E0 d1" at n = 200.

**Needs escalation.** (1) Independent check / Lean formalisation of Lemma 1 / Thm N200 (next to `T21HPM.lean`). (2) A finite-n upper bound on Pi(X) (stronger prover; shell argument for correlated nulls, drops/swaps at distance 2, tail >= 3). (3) Tabulate O-CERT C5 screening event over the 2,400 fits (bookkeeping). (4) Dataset-by-dataset matching of O-SWAP realised check with SMC outputs.

**Property with NO guarantee (quotes).** "It does **not** give a proved upper bound on the miss rate at n = 200: that needs either a finite-n upper bound on Pi(X) (OPEN; the T03 restatement in finite form) or a finite-n discovery bound for the Gibbs route (OPEN, T38(b))." "Nothing here concerns PIPs, Z-hat, or the masked-regime delivery theorem."

---------------------------------------------------------------------------------------------------------------------

## 3. API-VSTAB (Claude Opus 5.5): check of A-REV7's STAB-LH certificate and the no-LS0 masked theorem

**Task question.** Is A-REV7's analytic STAB certificate (and the B2-LH no-LS0 masked theorem built on it) correct?

**Headline.**
- Every step of A-REV7 section 4 (and named section 3 pieces) is **VERIFIED**; no GAP, no ERROR; five remarks R1-R5 (clarifications).
- **STAB certificate PROVED:** if lambda0 b_vis^2 > R_M then m_STAB >= lambda0 b_vis^2 - R_M; exact numerical check on A-REV7's instance (m_STAB = 0.5728 >= 0.4032) and 0/1500 violations.
- **Composite theorem PROVED (candidate), given the cited inputs:** unchanged v3 with no LS0 has P(O and S-hat != S0) -> 0 on an explicit masked, growing-p, exact-Gram LH subfamily.
- **Corollary PROVED:** on the same region, A-REV7 section 3's strict-gap hypotheses C1-C3 hold at every fixed p.

| Result | Statement | Status | Hypotheses | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| STAB certificate | (CERT) lambda0 b_vis^2 > R_M implies m_STAB >= lambda0 b_vis^2 - R_M | PROVED (here); VERIFIED | exact Gram LH; lambda0 = (1-max|psi|)(1-max rho_h), R_M = sum beta_i^2 psi_i^2 (1-psi_i^2), b_vis^2 = min beta^2 | Idealised design (exact-Gram LH) | MOVES, POST | validity |
| Theorem (no-LS0 masked consistency on F_cert) | P(S0 not scored | C, data) <= N pi0(N^c) + N T_e a_n + (1 - c_* + r_n)^N -> 0 on event E_n; hence P(O and S-hat != S0) -> 0; liminf P(O and S-hat = S0) >= 1 - limsup P(no output) | PROVED (candidate), given cited inputs ([E-T1], [E-L4], [E-T5d] VERIFIED; T03 locked; T38E-R VERIFIED; IND-T VERIFIED* by A-REV1 only) | F_cert: exact centred Gram X'X = (n-1) Sigma_LH; fixed g, c >= 1, v >= 0; rho_h in compact subset of (0,1); 0<|psi_i|<min rho; fixed beta, sigma^2; p = p_n <= n-1; g <= B_n < 2g; (CERT). Method: v3 as run with no LS0; EX-A, EX-S, SR, CAL, output-potential convention, (P) from T03, IND-T | **As-run method (no LS0)** but **idealised design** (exact Gram, g <= B < 2g, p <= n-1, fixed s0), frozen-C (any frozen grid with T <= T_e, one final island N = N_e), asymptotic | START, MOVES, CAL, DEC | validity |
| Explicit member | g = 9, c = 2, v = 0, rho_h = 0.4, psi = 0.2, beta = 1, sigma^2 = 1, p_n = 9 floor(n/18) | VERIFIED (with remark R1: specify rho_h for null groups) | B = min(floor sqrt n, floor sqrt p, 16) = 16 once p >= 256 | idealised (not study: study groups of 5? (?)) | START | validity |
| Corollary (fixed-p BG3/LH-lock component) | on (CERT) A-REV7 section 3 C1-C3 hold strictly at every fixed p | PROVED | C1, C2 by certificate; C3 by W5 (G) | idealised; "remains a component result, because fixed-p production problems are eventually enumerated (Methodology 6.2)" | MOVES | validity |
| Verdict items 1-14 (common data event, start mass, all move types, terminal repair order 1/m!, BG3 inequality, U1-U3/Lemma J, eta_n correction (n^{-1/3} not sqrt(log n/n)), CONF, repair R1, ...) | each | VERIFIED | | | | |
| Unrestricted LH no-LS0 | | low/unknown; false for general locking (A-REV7 section 5 counterexample, reproduced exactly: improvement 0.004789) | | | MOVES | failure mode |

**Empirical facts.** Purely deterministic/numerical checks (script `vstab_check.py`, 1500 random LH configs, 0 violations of certificate; min slack 2.7e-4). No SMC run. Constants: c_* ~ 10^-18.65 and c0(S°) ~ 10^-11.87 on the instance, so (1 - c_*)^N -> 0 only for astronomically large N: "The theorem is asymptotic only".

**Disagreements / tensions.** With PXNGAP: this theorem needs no LS0 but is exact-Gram p <= n-1; PXNGAP needs LS0 but covers p >> n LH-iid. Both need g <= B < 2g (study groups of 5 outside). With API-POS: POS notes exact-Gram LH (p <= n-1, p fixed) lies outside YWJ/ZYVR's regime; this report's theorem covers it. R5: IND-T (fresh randomness per particle-round vs one shared stream) "has no Claude verifier".

**Needs escalation.** IND-T (VERIFIED* by A-REV1 only; matters unless paper assumes fresh randomness per particle-round). W5 PROOF.md section 4 (Lemma 2.2 start tails, Lemma T case i = 0) not read with line-by-line care. Possible record of fixed-p corollary next to `OBG-T38b-BG3`.

**Property with NO guarantee (quotes).** "Not claimed: completion (an output is not guaranteed); an unconditional numerical rate; finite-n accuracy; unrestricted LH (general locking is false: A-REV7 section 5, reproduced here); random or iid designs."

---------------------------------------------------------------------------------------------------------------------

## 4. API-MASKZPIP (Opus 5.5): two-sided evidence and PIP accuracy in the masked regime

**Task question.** In the masked regime, what can be proved about Z-hat's accuracy and the PIPs (T26(i)-(ii) masked)?

**Headline.**
- **PROVED (Thms E1, E2):** the lower tail of Z-hat is decided by the temperature tau_A at which the population first reaches the truth's basin: P(Z-hat_r/Z > (T/eta)[pi0(A^c)/pi0(x_m)] e^{-phi_tau D_A}) <= eta + N pi0(A). Z-hat underestimates by the log-odds overshoot of a late switch.
- Positive side **CONJECTURE** (V11: log Z-hat - log Z = O_P(sqrt(T/N)) when V contains the competing pair), idealised case **PROVED** (E3, Lemma J); beyond it PROOF SKETCH.
- Two-sided consistent evidence exists for the top-store sum Z_T: **PROVED, deterministic (Prop. P3)**: 1 - d1 <= Z_T/Z <= 1 and |PIP^T_j - PIP_j| <= d1 whenever S0 in T.
- PIPs: bias of RB PIPs <= TV(delivered population, pi) **PROVED (Thm P1)**; after locking bias <= d1, L1 error <= (L+4) rho-bar + u_pi + d1 **PROVED as a composition (P2)**; locking itself is O-BGIBBS BG3 (candidate, LH p fixed).
- Per-fit (finite n): **PROVED (Prop C1)** Z-hat/Z <= Z-hat/Z_T surely, so Z-hat < Z_T certifies underestimation.

| Result | Statement | Status | Hypotheses | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| E1 two-phase sandwich | |log W - Psi_t| <= phi_t eta + (1-phi_t) eta'; Psi_t = (a+Lambda)(phi* - phi_t) + log pi(x*) - log pi0(x°) | PROVED (deterministic, any kernel, any grid, any N) | frozen C (EX-A, EX-S, CAL, START), one island, v3 round kernels q_t-invariant, populations in M / M' | **frozen-C, one island**; needs near-frozen path | BRIDGE, ZHAT, ISL | accuracy (Z-hat lower tail), failure mode |
| E1a/E1b/E1c | late switch gives underestimation e^{(a+Lambda)(phi_t - phi*)}; island agreement uninformative; one-sided relaxation | PROVED | as E1 | frozen-C | ZHAT, ISL, FLAGS | failure mode, diagnostics |
| E2 miss bound | E[W 1{no stage-(t-1) particle in A}] <= kappa_t(A) <= [pi0(A^c)/pi0(x_m)] e^{-phi_t D_A}; Markov and arrival-temperature forms | PROVED (any kernel, any grid, any N) | Feynman-Kac martingale of O-PW2 Thm A1 (candidate; standard) | frozen-C | ZHAT, BRIDGE | accuracy |
| Lemma J | chi^2(q_t||q_{t-1}) <= chi-bar implies q_t(A)^2 <= (1+chi-bar) q_{t-1}(A) | PROVED | | generic; full-space ESS >= 0.9 grid cannot make a blind step | CAL, BRIDGE | failure mode |
| E3 | exact refresh: E(W-1)^2 = prod(1 + chi^2_t/N) - 1 | PROVED in the idealisation (exact pair refresh); pair-dominated perturbation PROOF SKETCH | | idealised (exact pair refresh) | ZHAT | accuracy |
| E4 dichotomy | upper tail always O_P(1) (T31(i)); lower tail -phi_tauA D_A + O_P(log T + log 1/pi0(x_m)) if blind; O_P(sqrt(T/N)) if the grid resolves the crossing | PARTLY PROVED; blind half PROVED; resolved half CONJECTURE | pair-dominated masked bridge; XM hypothesis log 1/pi0(x_m) = O_P(log n) | LH consequence PROOF SKETCH; for c >= 2 "the resolved case is OPEN" | ZHAT, CAL | accuracy |
| P1 | |E PIP-hat_rj - PIP_j| <= TV(nu-bar_r P^L, pi) <= E f_{r,0} + d1 | PROVED | terminal rounds pi-invariant, fresh randomness | frozen-C; bound not certified per fit | PIP | accuracy |
| P2 | E[max_j |PIP-hat_rj - PIP_j| | F_T] <= f_{r,0} + (L+4) rho-bar + u_pi + d1 | PROVED as a composition of locked T23(ii) and T12 (R3) | locked delivery event | needs locking (BG3, LH p fixed) | PIP | accuracy |
| P3 top store | Z_T/Z = pi(T), |PIP^T_j - PIP_j| <= pi(T^c) | PROVED (deterministic) | top store of scored models with exact scores | as-run (reporting object) | ZHAT, PIP, DEC | accuracy |
| P3' | Z_T/Z -> 1 at rate d1 on the masked family | PROVED as composition, CONDITIONAL on T03 + discovery (BG3 on LH) | P(O and S0 not in T) -> 0 | LH p fixed | | accuracy |
| C1-C3 (per fit) | W <= Z-hat/Z_T surely; band log Z >= max(log Z_T, log Z-hat - log 20) w.p. >= 0.95 (no upper bound); |PIP-hat - PIP| <= |PIP-hat - PIP^T| + pi(T^c) | PROVED | O-CERT Thm C1 | as-run (per fit) | ZHAT, FLAGS | validity (one-sided) |
| LH consequence of E4 | blind grid on LH: log Z-hat_r - log Z <= -Theta(n) phi_1 + O_P(log n) | PROOF SKETCH | exact-Gram LH, XM | idealised | | failure mode |

**Empirical facts.** At p = 18 exact enumeration (engine-faithful simulator): the engine's log W equals an exact-refresh SMC's log W on the same grid in every setting ("the evidence loss is a grid effect, not a kernel effect"); method-like V contained S0 in 9/9 pilots with |median log Z-hat_r/Z| <= 0.04, blind V gave -10.8 to -11.7 nats (islands agree to +/-0.01 while wrong). In the 4 study fits re-scored by O-CERT, Z-hat/Z_T = e^{0.18...0.59}: no underestimation certified; sd of log Z-hat_r 0.02-0.08. O-CERT: pi(S0) <= 0.37 even on correct fits (d1 >= 0.63), "so every bound involving u_pi is vacuous at the study's n". The report's section 4 results table is a literal placeholder (`RESULTS_TABLES_PLACEHOLDER`) (not filled).

**Disagreements / tensions.** A first-draft claim that Z-hat underestimates by e^{-Theta(n)/T_e} on LH was withdrawn: floor 1/T_e belongs to the pilot not the final grid; final grid built on V which contains the top 20p scored models; the collapse survives only for a blind grid. Says F-MASKPIP's G3 proxy is "blinder than the method's V". Relation to PRIORITIES Thm 6/T26: T26(i)-(ii) Z-hat/PIP consistency in the masked regime is not delivered; it is replaced by Z_T/PIP^T consistency (top-store) and a blind/resolved dichotomy. T26 is stated "favourable regime only" in PRIORITIES; this report agrees that at n = 200 PIP consistency is not claimable.

**Needs escalation.** V11 / E3(c): pair-dominated perturbation, leakage control uniformly near phi* (independent prover; sup-norm control of h_{s,T}). Independent check of FK martingale (O-PW2 A1) for v3's exact stage order (resample, mutate, record). (XM) on LH.

**Properties with NO guarantee (quotes).** "What the paper cannot claim: Any upper bound on Z, or any relative accuracy of Z-hat. That agreement of the four islands ... shows accuracy." "'PIPs ~ the 0/1 truth' is not claimable at n = 200: the posterior itself is diffuse." "A conditional evidence theorem from first moments. It is impossible (F-MASKPIP M3)". "p >> n transfer: ... LH-specific rates (D_A = Theta(n), locking, discovery) are proved only for exact-Gram p < n / p fixed". "The PIP consistency results (P1-P3) are asymptotic statements on the masked family LH."

---------------------------------------------------------------------------------------------------------------------

## 5. API-T26BUD (task R5, T26-BUDGET): Theorem 6 with a proved stage count

**Task question.** Can (P1) of Thm 6 (a bound on the number of grid stages T_n, hence budget) be proved for the calibration rule as coded?

**Headline.**
- **Theorem G (grid stage count). PROVED, deterministic.** Applies to `v3_calib.h::build_grid`: on any successful construction with S0 in V, T = N^pil + k^bis, k^bis <= ceil(log2(1/eta_n)).
- **Theorem 1 (one-stage regime). PROVED, given its inputs:** if 1 - pi0(S0) -> 0, 1 - pi(S0) -> 0, chi^2(pi||pi0) -> 0 and HPM of pi is S0 w.p. -> 1, then T_n = 1 w.p. -> 1.
- **ORTH (Prop. O). PROOF SKETCH;** number of pilot stages O_P(1) only **CONJECTURE** (Conjecture P). **Rule CAP. PROVED** (a method change: interval cap; "inactive in the study").
- Numerics [filled in sec. 4] and sec. 7 are literal placeholders in the report (`[filled in after the sweep]`, `[filled in]`); no numerical evidence is delivered by the REPORT.md (?: PROOF.md may have script outputs; not read).

| Result | Statement | Status | Hypotheses | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| Fact 1 | rho_V(u, .) and pilot ESS monotone, so bisections find the frontier | PROVED | | As-run (`v3_calib.h`) | CAL | cost |
| Fact 2 | -log rho_V(u,v) <= log(1+R_V(u)) + log(1+R_V(2v-u)), R convex | PROVED | S0 in V | As-run | CAL | cost |
| Theorem G | N^pil <= T <= N^pil + ceil(log2(1/eta_n)); T = N^pil if eta_n = 1 | PROVED (deterministic) | successful pilot, frozen V with S0 in V; eta_n = largest eta <= 1 with R(0), R(1+eta) <= eps0 = 0.9^{-1/2} - 1 | **As-run rule** (every rebuild, since pilot targets unchanged); conditional on S0 in V | CAL, BRIDGE | cost |
| Lemma P | pilot stage advances >= min{1-phi, a/D_k} and >= 1/T_e; N^pil <= 1 + ceil(D-bar/a), N^pil <= T_e | PROVED | a = 0.5124 | As-run | CAL | cost |
| Corollary 1 | T_n <= min{T_e, 1 + ceil(D-bar_n/a) + ceil(log2(1/eta_n))} on G_n and S0 in V; (P1) holds if P(G_n, S0 not in V) -> 0, eta_n bounded below w.p. -> 1, (N^pil+1) Delta_n ->_P 0 | PROVED | T03 + 1 - pi0(S0) -> 0 for S0 in V | partly favourable regime | CAL | cost |
| Theorem 1 | T_n = 1 w.p. -> 1 | PROVED given inputs | 1 - pi0(S0), 1 - pi(S0), chi^2(pi||pi0) -> 0; P(HPM(pi) = S0) -> 1; uses only the iid first pilot stage | **Idealised: one-stage (favourable) regime**; the study is masked (pi0(S0) ~ 1e-15), so does not apply there (?) | BRIDGE, CAL, START | cost, Thm 6 premise (P1) |
| Prop O (ORTH) | R(1+eta) = O_P(n^{-1/2+A eta (1-lambda*)} polylog) with 1 - lambda* <= R0^2, so T_n = 1 when A(1-lambda*) < 1/2 | PROOF SKETCH | ORTH-F, Gaussian errors, p <= n^A | idealised (orthogonal design) | | cost |
| Conjecture P | N^pil = O_P(1) on ORTH-F | CONJECTURE | occupancy control of adaptive pilot | | CAL | cost |
| Rule CAP / Cor 2 | cap "more than min{T_e, T^cap_n} intervals -> fail" with T^cap_n Delta_n ->_P 0 (e.g. ceil(log2 n)) gives (P1) deterministically | PROVED | | **Method change** (one line); T_e = O(log^2 n) already gives asymptotic statement; constant 1000 vacuous at finite n | CAL, RES | cost |

**Empirical facts.** None in the REPORT.md (placeholders). Claimed intent: exact p = 18 with actual pilot/grid rules.

**Disagreements / tensions.** With API-FAVIID: both about (P1); FAVIID reports finite-n evidence (T_n+1)Delta_n < 1 in only 1/56 runs at n <= 3,200 and 3/16 at n = 6,400 (numerical), "T_n = O_P(1) stays OPEN"; consistent with Conjecture P being open. T26BUD's Theorem 1 is the favourable-start regime, which PRIORITIES section 5 says is 1/2,394 fits in the study.

**Needs escalation.** Prop. O steps (1)-(4) (uniform h-expansions, T02-type truncation for the tilted law q_{1+eta}, MxE cross-terms, sigma-hat plug-in); Conjecture P (occupancy of adaptive pilot); independent check of Theorem G's count argument ("the main new claim").

**Properties with NO guarantee (quotes).** "A bound of the form T_n <= C1 + C2 log(1/Delta_n) does not follow from the rules alone." "The bisection count is controlled by the bridge past phi = 1, not by Delta_n."

---------------------------------------------------------------------------------------------------------------------

## 6. API-POS (referee task R3, MIX-POS): positioning against the rapid-mixing literature

**Task question.** Does the rapid-mixing literature (Yang-Wainwright-Jordan 2016, Zhou-Yang-Vats-Roberts-Rosenthal 2022, Zanella-Roberts 2019, Griffin et al. 2021) already imply Theorem 5 / polynomial-time recovery on LH, and what does Theorem 5 add?

**Headline.**
- On LH, masking is a property of the method's start law pi0, **not of the posterior pi**: the target posterior has the property every rapid-mixing proof rests on (every underfitted model has a missing true variable whose addition raises pi by a large factor; ZYVR Condition 1(b)). Exact enumeration at p = 16, 20: S0 the unique local mode; YWJ random-walk MH hits S0 from the empty model in median ~70-140 iterations, flat in n. For p = o(n), **PROOF SKETCH**; p <= 20 enumeration is evidence only.
- **With their own priors, both theorems apply to LH in the iid realisation** (p >= n, p <= n^A, fixed beta), so "polynomial-time recovery of S0 on LH is **not new**". **PROOF SKETCH** (hypotheses checked by standard arguments, not line by line). The referee's suspicion (M6) "is correct in substance".
- **For the paper's own target, neither theorem applies as stated:** prior strength (g = n, kappa_eff ~ 1 vs ZYVR's explicit kappa >= 18; Condition 1(a) holds only with c0 ~ 1/2 not 2 when p ~ n), size cap K = floor(n/2) breaks YWJ's D(s0), exact-Gram LH (p <= n-1, possibly fixed p) is outside both papers' regime. "So no published theorem covers the SMC-BVS output on LH. This is a formal gap, not a substantive one."
- ZR section 4.5 and GLS say nothing quantitative about LH. Citation check OK, one correction (ZYVR has five authors incl. Rosenthal; its sampler is LIT-MH, not a Zanella locally balanced sampler).

| Result | Statement | Status | Hypotheses | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| R3(i) YWJ Thm 2 / Cor 2 and ZYVR Thm 1 apply to LH-iid under YWJ-prior | iterates reach/mix to S0 from any start in M(s0): O(alpha p n s0^2 log p) iterations (YWJ), O(n) informed iterations ~ O(np) scores (ZYVR); posterior concentration pi(S0|Y) >= 1 - c1/p | PROOF SKETCH (applicability) | LH-iid, p >= n, p <= n^A, fixed beta, fixed s0 cap; YWJ-prior = Zellner g-prior g ~ p^{2alpha}, p^{-kappa0|gamma|} size prior capped at s0; RE(s0), SI(s0), beta-min with unspecified universal constants | **Idealised / different algorithm** (symmetric add/delete/swap MH or LIT-MH, not SMC-BVS) | POST, MOVES | cost (mixing), validity |
| R3(ii) not applicable to the paper's target | Y0, Y7, Y8, Z4(1a, c0 = 2) fail; Y1 fails for exact-Gram LH | PROVED for Y0, Y8, Z2 (definitional); PROOF SKETCH for Z4(1a) | paper-prior: beta ~ N(0, n sigma^2 (G+I)^-1), IG(0.01, 0.01), BB(1,p), cap K = min(p, floor(n/2)) | **As-run target** (the paper's prior) | POST | validity gap |
| R3(iii) | the property driving both proofs, Condition (1b)/(1c), does hold for the paper's target on LH; a YWJ-style analysis for the paper's prior on LH "would very likely succeed" | CONJECTURE (the latter); (1b)/(1c) via Prop U PROOF SKETCH | | | POST | accuracy |
| Prop U | underfitted models are never local modes of the paper's target on LH-G: some j in S0\gamma has log pi(gamma+j)/pi(gamma) >= c n, w.p. -> 1, for all gamma in M(K) with S0 not in gamma, |gamma| < K | PROOF SKETCH | G; LH-G with p <= delta n small fixed delta; s0, beta, rho, psi fixed; paper target on M(K) | exact-Gram LH, p <= delta n (idealised; p up to n-1 unsettled) | POST | accuracy |
| Cor U' | every local mode of pi under add/delete/swap on M(K) is overfitted; S0 is unique local mode: OPEN in general (holds in every case enumerated, p <= 20) | PROOF SKETCH (Cor U'); uniqueness OPEN | | | POST | |
| YWJ extension to LH-G with p_n -> infinity | | CONJECTURE ("very likely true") | | | | |
| Conj: YWJ-type spectral gap for the paper's prior with cap K = floor(n/2) | | OPEN | | | | |
| ZR section 4.5; GLS Thm 1 | no quantitative consequence on LH; GLS: ergodicity/SLLN, no rate | (literature) | | | | |
| RE(s0) on LH-G for every s <= p | nu = phi0^2 (n-1)/n | PROVED (Lemma 4.1(a) + Cauchy interlacing) | exact-Gram LH | idealised design | POST | |

**What exactly it claims about rapid-mixing theorems covering our target (for the discussion).**
- Which design: LH, in two realisations. Exact-Gram (X'X = (n-1) Sigma, p <= n-1, possibly fixed p) and iid (rows iid N(0, Sigma_LH), p <= n^A, p > n allowed). Scale: p >= n for YWJ's regime ("throughout ... p >= n"); ZYVR needs n = O(p), s0 log p = O(n). Both theorems are stated for their own priors (Zellner g with g ~ p^{2alpha}; size prior p^{-kappa|gamma|} on |gamma| <= s0 with s0 <~ n/log p) and a fixed s0.
- Covered: LH-iid, p >= n, with their priors (PROOF SKETCH).
- NOT covered: the paper's own target (BB(1,p), g = n ridge, IG(0.01,0.01), cap K = floor(n/2)); exact-Gram LH with p <= n-1; fixed p; the algorithm SMC-BVS itself. The study's regime (n = 200, weak signal) is reached by neither: "YWJ explicitly leave the intermediate-signal regime (their (10)) open and suspect slow mixing there. Theorem 5 does not reach it either, so this is a shared limitation, not an advantage."
- Hitting times are not mixing times: enumeration is p <= 20, fixed p; "evidence for the qualitative claim only".

**What it says about novelty (quotes / near-quotes).**
- "It does not add: Polynomial-time discovery of S0 on LH by some sampler. ... Evidence that LH is computationally hard. ... Mixing to pi. ... Any claim of being 'first' to give computational guarantees for BVS samplers."
- "LH is hard only for the method's own block-product start law. The masking is a blind spot of pi0 and does not reside in pi."
- It does add (narrower): (1) a guarantee about the algorithm and target actually used (BB(1,p) capped at floor(n/2), g = n, proper sigma^2 prior), including exact-Gram LH and fixed p, "Theorem 5 needs no mixing, so it needs no such cap"; (2) output is an estimator (HPM ledger, unbiased Z-hat with Markov certificate, RB PIPs) with deterministic polynomial score count (T32(i), Thm 5(c)); (3) the start is exact and proved masked (T27 via W1-EXP Thm 5(b): pi0(S0) = p^{-c} n^{-c/2} e^{O_P(1)}; W7-SEP SEP(A)/(B): start-only iid draws and one-shot reweighting need p^c n^{c/2} draws), the method's moves repair it; (4) neither literature reaches the study's regime (shared limitation).
- "Honest bottom line": mixing literature implies a simpler sampler finds S0 on LH in polynomial time: "**yes for their priors** (PROOF SKETCH of applicability) and **almost certainly yes for ours** (Prop. U plus enumeration; not a published theorem). Theorem 5's contribution is therefore not computational hardness."
- "A cheaper repair. Prop. U means a greedy add-only search from empty or from S° finds S0 on LH in <= s0 steps ... If the paper wants a family where the SMC bridge is needed against local MCMC, LH is the wrong family". Draft paper paragraph (245 words) and one-sentence contribution statement included in sections 8-9.

**Empirical facts (exact enumeration, fixed p, paper's exact target, W1-EXP `log_m`).** LH c = 1 (p = 16, rho = 0.7, psi = 0.5, cap 6): n = 200: log10 pi0(S0) = -2.12, pi(S0) = 0.63, c1(1b) = 2.81, c0(1a) = -0.30; n = 1.02e5: pi(S0) = 0.99, c1 = 1508.66, c0 = 1.87; modes M(K) = 1 in all rows; YWJ hit from empty median 87 (n = 200) ... 67. LH c = 2 (p = 20, rho = 0.85, cap 8): n = 200: pi(S0) = 0.55, c1(1b) = -0.34 (negative, i.e. Condition (1b) not satisfied at n = 200), c0 = 0.22; start slope matches -(1/2) log10 n per masked variable. c0 small/negative at n = 200: the failure vs YWJ/ZYVR is on the overfitted side. Not a study design (p <= 20).

**Disagreements / tensions.**
- vs THEORY_PRIORITIES section 5 (preliminary, pending ANALYSIS-H2): POS leans on W7-SEP Prop. GU / SEP(C): "the production local search from the start mode suffices" and "a greedy add-only search from empty or S° finds S0 on LH in <= s0 steps"; PRIORITIES reports "the final local search repaired 0 fits; in 541 fits the search centre was in R2 but not S0, and it never returned S0" (at n = 200, p >> n, study scenarios). Different designs and scales (POS: LH, p <= 20 enumeration; sketched asymptotics).
- vs API-N200 / API-MASKZPIP: pi(S0) <= 0.37 on correct study fits (n = 200, p = 500/1000) vs POS's pi(S0) = 0.63 (c = 1) and 0.55 (c = 2) at n = 200 in the p = 16/20 enumeration: POS's "unique local mode" at n = 200 does not mean posterior mass concentrated; (1b) is negative at n = 200 for c = 2.
- With PRIORITIES Thm 2 "T27 bounds iid start draws only, not the hybrid sampler": consistent.
- POS says the paper's weak per-addition penalty bears on "posterior misses towards supersets at n = 200 (F-REFEREE section 4)" and is "a prior-choice matter fixed by Felipe".

**Needs escalation.** (1) Check YWJ and ZYVR theorem/assumption numbers against the published journal PDFs (arXiv v1 / v3 only were read). (2) Line-by-line check of YWJ Thm 2 and ZYVR Thm S2 on LH-iid (RE union bound, sparse projection, omega(X), Assumption A with the chosen g). (3) Write Prop U in full (s_y standardisation, uniform noise bound with p <= delta n; whether p up to n-1 is reachable). (4) The analytic c0 ~ 1/2 claim (max-chi^2 asymptotics) independent check. (5) Conjecture (Y1 extension, (iii)): YWJ-type spectral-gap bound for the paper's prior on LH-G with cap K = floor(n/2) is OPEN; unimodality on M(K) beyond p <= 20 is OPEN.

**Property with NO guarantee (quote).** "Neither literature reaches the study's regime." "(iii) ... A YWJ-style canonical-path or drift analysis for the paper's prior on LH would very likely succeed (CONJECTURE, supported by section 6)." No theorem covers the SMC-BVS output on LH: "So no published theorem covers the SMC-BVS output on LH."

---------------------------------------------------------------------------------------------------------------------

## 7. API-FAVIID (synthesis task 9, FAVIID-CLOSE, Part 1): audit of W5-FAVIID

**Task question.** Complete and audit W5-FAVIID's report on the favourable-start (iid final draws) regime for S3/S4/S6: Thm 2(iii) branch, T26 (P1), Thm 5(a).

**Headline.**
- Placeholders in W5-FAVIID were already filled at branch tip 31695b1 (74 pilot runs, n up to 12,800); audit recomputed every number: tables reproduce exactly; one factual error: "(T_n+1)Delta_n < 1 in 0/56 runs at n <= 3,200" is actually **1/56** (S3, p = 500, n = 3,200, value 0.997).
- Three claims hold only at the cell median (truth-context effect on Q-bar, "factor ~ 5 to spare" in Theorem A's moment check, "T22(i) vacuous at every n <= 3,200"); corrected in `W5-FAVIID_REPORT_AMENDED.md`. "No statement, proof or status word changes."
- Same-family read of Lemma X+, Lemma M, Theorem B's factorisation, C1-C3: no error found; c_ML = 3.83114 confirmed. "This is not verification." All stay **PROVED (candidate, author only)** pending the cross-family referee.

| Result (W5-FAVIID items as carried by this report; statements not re-stated here) | Statement | Status | Hypotheses | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| Thm B (M5 / Thm 2(iii), favourable branch, S3/S4/S6) | 1_{Q_n(3)}(1 - pi0(S0)) = O_P(|W(3)|(s0+1) sqrt(log n/n)); unconditional given Lemma P1' | PROVED (candidate, author only); confidence card P(true) 0.9 | [C1] (W3-PXN P2 transfer to equicorrelated Sigma), (G3) uniform angle bound / Lipschitz, Lemma S; locked T22(i) | **Favourable-start regime, scenarios S3/S4/S6; asymptotic; pilot n up to 12,800 (not n = 200)** | START | accuracy (start mass near truth) |
| Theorem A | (analogous bound with factor 1 instead of |W|) | PROVED (candidate, author only) (?) | (A1) bounds E[q 1_G] asymptotically | as above | START | accuracy |
| Lemma X+ | kappa+ = O(1/n) on the RSS floor | PROVED (candidate, author only) | [W1-L1.1]-[W1-L1.2] | | START | |
| Lemma M | elementary inequality, c_ML = 3.8311 | PROVED (candidate, author only) | | | | |
| Lemma P1' | load-bearing for "unconditional on S3/S4/S6", "not on the R6 list" | PROVED given [C1], author only | | | START | |
| Thm 6 (P1) on S3/S4/S6 (C2) | asymptotic (T^max + 1) Delta_n -> 0 | PROVED (candidate) (conf 0.9) (?: status word not repeated in this report beyond "asymptotic") | C1; W2-T26 idealisations | favourable regime only | BRIDGE, CAL | cost |
| Thm 5(a) on S3/S4/S6 (C3) | liminf P(S-hat = S0) >= 1 - limsup P(U) | (inherits Thm B and C1); conf 0.9 | | favourable regime | DEC | validity |
| (P1) at finite n | (T_n+1) Delta_n < 1 in 1/56 runs at n <= 3,200 and 3/16 at n = 6,400 | numerical only (conf 0.8); "T_n = O_P(1) stays OPEN" | delta-hat_1 = product-form estimate (1 - e^{-u1}); rigorous lower bound u1/(1+u1) gives 0/16, 0/20, 3/20, 4/16, 1/2 | | | |
| Conjecture B' (no |W| factor) | | CONJECTURE (conf 0.75, down from 0.85; per-design context effects reach x5) | decoupling X-measurable context from y | | | |

**Empirical facts.** T22(i) valid in 1,600/1,600 rows; Q_n in 1,598/1,600 (failures: S6 at n = 200); max q/Q_real 0.9957; first-stage ESS pinned at 0.90 in all 74 runs, no forced stages; "T22(i) bound ... vacuous in the cell median"; 5/80 S3 designs at n = 3,200 have bound <= 1; delta-hat_1 median 0.985 (range 0.26-2.19) at n >= 3,200, sets Delta in 24/74 runs; empirical first n with condition: 1,600 (S1 both p; S3 p = 500), 3,200 otherwise. Note: Q_n fails at n = 200 (S6).

**Disagreements / tensions.** Tension between PRIORITIES section 5 ("1 of 2,394 evaluated fits is favourable"; per-cell median pi0(S0) ~ 1e-12 or smaller) and this regime: favourable-regime results here only start to bite at n >= 1,600-3,200 and (P1) in 3/16 at n = 6,400, not at n = 200. Report says "I propose no new statements".

**Needs escalation.** Part 2 (XF referee) using `REFEREE_HANDOFF.md`; highest-risk step: uniform Lipschitz/[C1] argument in (G3); next: C1's transfer of W3-PXN P2 to equicorrelated Sigma, and Lemma P1' (add to referee list). HQ: adopt `W5-FAVIID_REPORT_AMENDED.md` or apply five marked errata; update synthesis (M5 "unfinished REPORT" done). Any paper sentence quoting "first n with (T_n+1)Delta_n < 1" should say which delta_1 it uses.

**Property with NO guarantee (quotes).** "T_n = O_P(1) stays OPEN"; Conjecture B' is CONJECTURE; "An exact delta_1 is not computable at p >= 500."

---------------------------------------------------------------------------------------------------------------------

## 8. API-RESID (RESID-STEP0): post hoc start-table check on the 2,400 PROD-H fits

**Task question.** On the 2,400 study fits, does a common sigma-hat^2 or residualised (backfit) start table give a favourable start, and would a start change help the reported accuracy?

**Headline.**
- **Common sigma-hat^2: settled against.** 0/2,400 favourable for each of three feasible plug-ins; F-SIGMA stop rule fires (C-fix floods to cap K = 100 in 2,113/2,400 fits). "No SMC pilot for common sigma-hat^2."
- **Residualised (backfit) tables, 3 sweeps: O-DILUTE pilot replicates on real fits**: median log10 pi0(S0) from -15.65 (v3) to -1.07; 1,888/2,400 favourable (78.7% vs 78.8% on O-DILUTE's regenerated 378/480); start mode = S0 in 1,245/2,400. At fixed point (<= 10 sweeps): favourable 2,203/2,400, mode = S0 in 1,672, median pi0(R2) 0.77; weak spot S5 at c = 0.5 (47 and 19 favourable per 100).
- **"A start change cannot move the study's headline accuracy":** 1,829 exact recoveries, 565 posterior misses, 6 resource-limit stops (all S5); most any start change can add to HPM = S0 is those 6 fits (0.25%).
- Status "unchanged": residualised tables remain an **unproven candidate**; no theorem covers them; T22(iii) would need restating.

| Result | Statement | Status | Hypotheses | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|---|
| Step 0 reproduction | rebuilt v3 tables match engine to 3.1e-13; log pi0(S0) matches O-LS0 record to 1.6e-12; start-mode size equals in 2,400/2,400 | empirical (post hoc, no SMC) | | **As-run** (the study's own start law, exact) | START | diagnostic |
| v3 start on study fits | median log10 pi0(S0) = -15.65 [IQR -18.5, -13.4], median pi0(R2) = 0.813, favourable (pi0(S0) >= 1e-4) = 0/2,400 | empirical | | As-run | START | accuracy/failure mode (masking/dilution) |
| Common sigma-hat^2 variants (sigma-tilde^2_{S-tilde0}, C-fix, s_y^2) | no feasible plug-in favourable; C-fix floods (97-100/100 in every non-S5 cell); sigma-tilde^2 destroys pi0(R2) (0.81 -> 4.6e-6); s_y^2 reproduces v3 | empirical; confirms rejection; F-SIGMA Thm S6 stays PROVED | | Method variants (not run via SMC) | START | |
| Backfit (residualised) start | see Headline | candidate, unproven; "fixed-point convergence of the sweep iteration unproven (90/2,400 unsettled at 10)" | validity rests on F-DRAFT Prop P(i) (positive, product-form, data-measurable tables), argued by O-DILUTE section 9 but "no one has written out for these tables" | **Method change**; no SMC evidence | START | cost/stability possible; accuracy cap 6/2,400 |

**Empirical facts for coverage.**
- Study outcomes (via O-LS0 `paired_per_fit.csv`): 1,829 exact recovery, 565 posterior miss (S0 scored and lost on posterior; "no start or search change can report S0 there"), 6 no final ledger (resource limit, all S5). "There are also no search misses in the study."
- Start mode under v3: 0 fits with mode = S0; 1 fit with >= 10 extras; pi0(R2) median 0.81 (so the start is near truth but never on S0, i.e. masked-by-dilution regime almost everywhere; consistent with PRIORITIES section 5).
- Resource-limit fits (6, all S5): backfit start mode = S0 in 2 (3 sweeps) or 4 (fixed point); v3 median log10 pi0(S0) for them -33.26, pi0(R2) 0.00.
- Backfit lowers pi0(R2) in posterior misses (0.77 -> 0.55 at last sweep); one-sided risk on the 1,829 correct fits (can turn exact recovery into a posterior-mode correction; "same asymmetry S-ELS found for LS0"), only SMC can measure it.
- T38(b) eligibility premise pi0(R_d) >= b_n: holds for v3 at the study size (O-DILUTE); at backfit fixed point "does not visibly fail in any cell"; at 3 sweeps fails in S5.

**Disagreements / tensions.** Consistent with API-N200 (565/6/0 counts). Tension in slot terms: T22(iii) favourable regime "currently false (0/2,400 favourable for v3)"; backfit would make it true on 78.7-91.8% of fits but is a method change with no theorem. API-PXNGAP / T38(b) eligibility relies on start mode S° being in R_d; RESID shows the v3 start mode has 4 truths + 0 extras (median) (not S0) while pi0(R2) is 0.81: supports delivery premise empirically.

**Needs escalation / not done.** No SMC runs (no evidence on HPM accuracy, harm, ESS, run time under any new start); no proof that backfit sweep iteration converges; no check of Hamming-ball mass pi0(B_d); cost of backfit in production C++ engine not measured. Pilot (if Felipe wants) design given: paired datasets, iterate-to-fixed-point sweep rule with cap 10, cells S4 p = 500 (c = 0.5, 1), S5 p = 1000 (c = 0.5, 1) and the 6 resource-limit fits, 20 datasets per cell, pass: no paired harm beyond 1 dataset per cell plus measurable gain.

**Property with NO guarantee (quote).** "Residualised tables remain an unproven candidate. No theorem covers them, and T22(iii) would need restating." "A start change cannot move the study's headline accuracy."

---------------------------------------------------------------------------------------------------------------------

## 9. API-AUDIT (referee task R10, CODE-AUDIT): verdicts on the implementation facts the proofs use

**Task question.** Do the implementation facts the proofs rely on (SR, GUARD, emit_centre/LS0 logging, scan-before-limit, IND-T, VAL-FP) hold in the code?

**Headline (verdict words verbatim).**
- SR **HOLDS** (read as "both *feasible* configurations"); GUARD **HOLDS** (code reading plus executed bitwise on 10/10 fits) with **a hazard in the R layer**; emit_centre/LS0 **HOLDS in the O-LS0 export only. Production v3 has no LS0**; scan-before-limit **HOLDS**; IND-T sequential stream reading **HOLDS**; VAL-FP **MEASURED**.
- Code version: branch base e58a949; last commit touching `Scripts/SMC_BVS/core` is 39db138; sha256 prefixes of nine audited files equal W5-LOCKBOOK's.
- "Production has no LS0. All three `local_search` calls (`cpp/v3_core.cpp:447, 610, 657`) start at `led->hpmS` with `emit_centre = false`. No call starts at the start mode."

| Fact | Verdict | Hypotheses / reading | As-run vs idealisation | Component | Property |
|---|---|---|---|---|---|
| 1 SR: both feasible configurations scored and offered before the accept draw; no call site disables emission | HOLDS (`v3_engine.h:118-130`; only `emit=false` at `:381` with already-offered HPM) | infeasible other configuration (|S| = K for addition): nothing scored, o_j = 0, one uniform still read; "offered" = ledger event reaching stores on first fresh evaluation | **As-run** | MOVES, DEC, LS | validity (scoring set includes everything visited) |
| 2 GUARD: no guard path reads an RNG or changes a setting; a run no guard stops equals the R-bar computation | HOLDS (executed: bitwise identical on 10/10 fits; forced stop on 10/10 gives `resource_limit`, `estimates_available = FALSE`, `hpm_incomplete = TRUE`) | stop inside the final run (`v3_run.R:111-116`) not executed, code reading only | As-run (10 synthetic fits, n = 200, p in {20,30,40}, tier 0, T = 3-21) | RES, FLAGS | validity |
| 2b A stopped fit is "no output" | HOLDS for status and flags. **HAZARD:** `fit$log_Z` on a stopped SMC fit silently returns `log_Zbar0` (R partial matching) | executed 10/10; positive number (e.g. 66.89) where a completed fit gives about -250 | As-run (R layer) | RES, FLAGS | failure mode (silent wrong number); "Consequence for the proofs: none"; 55 R files use `$log_Z`, not swept |
| 3 emit_centre / LS0 logging | HOLDS in the O-LS0 export (`cpp_final_run_ls0`) only; **production v3 has no LS0**; `emit_centre = true` is required, not cosmetic | LS0 audited by code reading only; not executed in this run | **LS0 is an idealisation relative to production**: "As committed, the production core is v3 without LS0"; supplement must cite the export or merge it into `cpp/v3_core.cpp` | LS | validity (premise of PXNGAP, T38 b1) |
| 4 Scan before limit | HOLDS (`v3_engine.h:384-415`): at most l moves, l+1 complete scans, no RNG, ties lexicographic | | As-run | LS | validity (certification) |
| 5 IND-T sequential stream reading | HOLDS: one stream per island (`v3_core.cpp:434-437`, streams 10-13; calibration 0-9), read sequentially particle by particle; `run_island` calls `run_island_s` | | As-run | ISL | validity (independence assumption used in proofs) |
| 6 VAL-FP (Prop 2(f)) | MEASURED: eta <= 2.6e-13 (pooled log Z-hat); 0 path disagreements in 110 replays; first-order eps ~ 2.4e-7 to 2.2e-6 per final run (dominated by N^2 multinomial-resampling boundary comparisons) | contract restated as **given the frozen object C^fp** (replaces W5's "exact run has the same status and C"); long double replay as proxy of exact; one-sided CP 95% UB 0.027 on eps from replays alone | As-run only for p <= 40, n = 200, tier 0; production size "should be expected to have proportionally larger eps" | ZHAT, CAL | accuracy (floating-point) |
| SR-3 (new, harmless in production) | table and inherited models enter the stores without entering the cache | idempotent re-offer | As-run | MOVES | |
| LS0-2 | `emit_centre = false` from an unscored centre would not offer it | PROVED by code reading (repeats W5 IMPL-EMIT) | LS0 only | LS | |

**Empirical facts.** 10 synthetic fits (not the 2,400); guard bitwise 10/10; 110 fp/ld replays 0 path disagreements; deterministic F-comparison flips (HPM order, local-search tests) 0 in 110 replays, a data property (near ties).

**Disagreements / tensions.** The code facts the proofs use for LS0 (emit_centre) are verified for a test export, but PXNGAP's theorem (and any "v3 + LS0" theorem) is not about the production core; consistent with API-VSTAB (no-LS0 theorem for v3 as run). Task text corrections: local_search is `cpp/v3_engine.h:378-418` (not 369-420); final run calls `run_island` wrapper.

**Open items.** (1) Stop path inside the final run not executed. (2) LS0 not executed, code reading only. (3) No sweep of consumers for unguarded `$log_Z`. (4) eps, eta measured only at p <= 40, n = 200, tier 0. Recommended one-line fix: set `fit$log_Z <- NA_real_` (and `log_Z_r`, `log_Z_rel_m0`) whenever `estimates_available` is not TRUE (in `finish`, `v3_fit.R:55-62`), flagged to core owner, not made.

**Property with NO guarantee (quote).** "As committed, the production core is v3 without LS0." "ε and η were measured at p ≤ 40, n = 200, tier 0. Production-size fits were not replayed."

---------------------------------------------------------------------------------------------------------------------

## Cross-report summary of tensions (for the inventory)

1. **LS0 is not production.** API-AUDIT (no LS0 in core) vs API-PXNGAP (Thm 5(b1) needs LS0; "Method change needed: yes, LS0"). API-VSTAB gives the no-LS0 alternative, but only exact-Gram LH, p <= n-1, growing p, g <= B < 2g.
2. **Study generator excluded.** API-PXNGAP (O1): groups of 5 outside (SIZE); API-VSTAB also needs g <= B < 2g (groups of 9 in the explicit member).
3. **Search vs posterior.** API-N200 / API-RESID: all errors are posterior misses (565), S0 scored in 2,394/2,394, 0 search misses; so the repair-theorem content (PXNGAP, T37/T38(b)) does not change the study's accuracy; PRIORITIES section 5 adds "final local search repaired 0 fits". API-POS' argument that greedy local search from S° suffices (W7-SEP Prop GU, Prop U) is for LH, p <= 20 enumerations and asymptotic sketches.
4. **n = 200 vacuity.** pi(S0) <= 0.37 on correct fits (O-CERT; API-MASKZPIP, API-N200): 2E0 d1 > 1, u_pi bounds vacuous; API-N200 replaces with Pi(X); PXNGAP's proven margin negative at n = 200; VSTAB constants ~1e-18.65; FAVIID favourable-regime conditions not met at n <= 3,200 (1/56).
5. **Evidence/PIP in masked regime.** API-MASKZPIP: no relative-accuracy claim for Z-hat; only one-sided T12/T31(i), blind/resolved dichotomy (resolved half CONJECTURE; OPEN for c >= 2), and top-store Z_T. This is below what Thm 6 (T26 (i)-(ii)) states, though PRIORITIES already restricts T26 to the favourable regime.
6. **Start modifications (RESID).** Backfit start is empirically favourable on 78.7%-91.8% of study fits but has no theorem and no SMC evidence; common sigma-hat^2 rejected.
7. **Mixing positioning (POS).** Thm 5 is not a hardness or "first" result; paper-prior target is outside YWJ/ZYVR hypotheses; claimed novelty is an output-level guarantee under the paper's prior with a proved start diagnosis.
