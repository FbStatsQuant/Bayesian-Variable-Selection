# Round 1, Seat B (Fable 5.1, Claude Work, high)

Verbatim final message, extracted by the chair from `~/.claude/projects/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-THM/2db7a6f1-74cd-4d9e-9177-cf0f228331e3.jsonl` (completed 2026-11-04 02:21 UTC). Everything in it is the seat's position; its own arguments are unchecked.

---

# MEET-THM · Round 1 · Seat B

**Read:** DOSSIER, R0_DIFF (K01–K108), AMENDMENT_HQ_01, METHOD_v3.1_FINAL (§0–§6), THEOREM_REVISION_INPUTS (N1–N17, §4, §5), N9-KERNEL REPORT, HQ_DISPOSITIONS, REGISTRY_INDEX §3.4–§5.B, THEOREM_LIST (all 24 entries), THM-INV REPORT (§1, §3, §5), O-WSTAB PROOF.md (§0–§8 statements), REGISTRY_v2 rows OWS-*/FD-W*, R0_D (items, §4–§6), R0_E (T01–T22, T34, T38, T44, §4–§6), proposal §4.4/§5/§8.2/§13, Song–Liang Thms 1–4, Cors 1–2, Cond. 1–5, §6 (JRSS-B text). No LIT report re-read beyond what THM-INV/THEOREM_LIST quote; citations below are "checked" only to that extent unless stated.

**Local check (one script, 20 runs, 40 s; script and output in §E).** On a two-block design with genuinely weak non-zero cross-block correlation, the start-to-posterior χ² stays O(1) and the ESS-0.9 grid uses 1–6 stages, while the registry's WS4(e) perturbation constant η_W is vacuous (51–∞) at every ε ≥ 0, and the BO-equivalent bridge can be *worse* than the true one. Consequence for §E: the §5.3 theorem must go through leakage (WS5.3) and the exact χ² identity (WS6(b)), not through perturbation of the orthogonal case (K11/WS4).

---

## §A Coverage sweep (item 1)

### A1 Proposal goals → K-IDs

| Goal | K-ID(s) delivering it | Reason if not delivered / remark |
|---|---|---|
| §5.1 exactness under MH correction | K20, K21 (N9K PROVED (candidate), code-checked), K08; stated as a cited lemma (Mengersen–Tweedie; Del Moral 2006) with the method's kernels, plus the Lean target of card D16 | Delivered. Binding goal met by N9 as filed (no registry row yet: index §5.B B2 must be closed by the registrar). |
| §5.2 SMC consistency | K35, K47 (ADRAFT-ThmA, Astra-only), K48 (MA-PropP), K55 (CLT) as cited lemmas; method hypotheses (frozen 𝓒, R′ declared, GUARD-W) as the paper's Proposition (card D1) | Delivered (KNOWN—CITE). |
| §5.3 weight stability, weak cross-block dependence | **K102 restated** (card D6, §E): WS5.3(F)+WS6(b)+WS7 on a cross-block-leakage family; inputs K10, K25, K27; K11 demoted to supplement | Delivered as a theorem with genuinely weak non-zero cross-block correlation (CBL(η), not H-ORTH). The *island second moment* E[W²|𝓒] on the as-coded hybrid system stays OPEN (WS8d): disclosed in the card. |
| §5.4 PIP error | K51 (A1(a),(b)), K52 (PC1 claim 3, PROVED given N1), K43 (restricted PIP^𝒯, deterministic) | Delivered. |
| §5.4 joint-PIP error | K46 (N1, PROOF SKETCH, binding) + K51 with h_A = 1{A ⊆ S}, plain measured-round averages (c_h = 0, M9) | Delivered conditional on N1; if N1 fails → escalation (binding §13.1). |
| §5.4 TV error | K57 (bias ≤ TV, PROVED), K103 (minorisation TV rate, supplement), K108 (perturbation TV ≤ tanh ε) | Partly: a TV bound on the delivered population law exists (K103) but its rate is vacuous under masking; see §F. |
| §5.4 KL error | K104 (exact KL/J identities), K105 (Lemma KL, lower bound) | Identities and lower bounds only; no KL *error bound for the final estimate* is meaningful: see §F. |
| §5.4 credible-interval coverage | **Not delivered as such**; replaced by output-event coverage of the certificate card: K36, K42, K78 (N6 PROVED modulo GUARD-W) | The method estimates model-space functionals; credible intervals for β need h̄(S) = E[h|S,X,y] and a coverage theorem for a Monte-Carlo-plus-posterior interval; no route; §F, §I Q1. |
| §13.1 E_π[h] → truth | K46 (N1) + K51(d) + K52; truth as n → ∞ via K93 (T03♯) | Delivered as "estimate → π(h)" (fixed data) and "→ h(S₀) in probability" with R_n a hypothesis (lower bound on R_n disclosed). |
| §4.4 / §8.2 diagnostics as a device | K25 (what restricted ESS certifies, exact identity), K42 (positive certificate Ẑ < Z_𝒯), K79 (no universal detection, PROVED), K80 (detection probabilities of E1–E3, supplement), K54 (R_eff) | Delivered as "what diagnostics prove and cannot prove"; positive universal power is impossible (K79) and is stated so. |

### A2 Song–Liang 2015 → K-IDs

| SL item | K-ID(s) | Reason if it does not apply |
|---|---|---|
| Thm 1 (Hellinger consistency, bounded predictors) | K93 (T03♯: selection consistency, p ≤ n^A) | Hellinger/coefficient contraction not delivered: not a paper-1 target (THM-INV §3b); future work. |
| Thm 2 (Condition 1 tails) | K93 | As above; our T03♯ is fixed-design. |
| Cor 1 (P_n < e^{Cn^α}, rates) | K94 (N12: OPEN, not impossible) | Cannot be imported (their prior/conditions); future work with reason (METHOD §5.2). |
| Thm 3 (sure screening) | K93 (large signals get PIP → 1 without beta-min); estimated PIPs: K51, K52 | Delivered for the exact posterior; for the reported PIP via Thm H. |
| Thm S (MAP consistency) | K93 (HPM of π) + K72, K68, K69, K70 (reported HPM) | Exceeded: SL has no theorem for the composed output. |
| Thm 4 / Cor 2 (misspecified subset → KL projection; eq. (19)) | K17, K18, K10 (our blocks are misspecified-subset posteriors; dilution identity; σ²-coupling), K97 (Condition 5/eq. (19) failure on LH) | Delivered and exceeded (we quantify the failure; correctness does not depend on it). |
| §6 complexity (K_n = √P_n; O(P_n^{(1+α)/2}) + O(nP_n)) | K87, K88, K90 (D1(d) same-units comparison, accounting only) | Delivered at the island level; no speed-up claim (K91 dropped). |

### A3 THM-INV §1 empty or partial cells → K-ID or "nothing provable"

| INV cell | K-ID / verdict |
|---|---|
| 1·F: Π(X) upper bound | K94 (R7): future work; no route for Π(X) given the design. Supplement candidate: E₀-averaged finite-n bound by fractional odds (T34 route), card D20. |
| 1: contraction / coefficient rates | nothing provable in paper 1: no target result for the ridge-BB posterior; future work. |
| 1: growing s₀ | nothing provable: T03♯ needs fixed s₀; N12 future work. |
| 2: n = 2 extension, eventual exact dispatch | K76 (supplement remark; seat-proved, unchecked → check wave). |
| 3: partition law for the study packing (g = 5, 2g ≤ B) | K07 (N8, OPEN): supplement proposition *conditional* on strict separation (PART-ThmA PROVED, XF VERIFIED*); the study generator stays disclosed as uncovered. |
| 4·V: exact sampler, Z̄₀ | K08 (N9K PROVED (candidate)); cited lemma + Lean (card D16). |
| 4: backfit start | rejected (METHOD §4); nothing. |
| 5: realised masked T_n (Conjecture P) | K31: defer (OPEN); the as-coded guarantee is T ≤ T_e (K26). |
| 5: depth vs correlation | K30 (STG-M, ideal grid) + K27/K28 (spread bound) + §E card; as-coded OPEN. |
| 6: mixing of the φ = 1 round | K103 (uniform minorisation, supplement, honest rate); K24 deferred (route blocked; HP3 PARTLY-FALSE). |
| 7: rebuild convergence, P(S₀ ∈ V), P(schedule_limit) | K31, K25: OPEN; only termination/cost (K33) provable now. Reason: V is a data-and-MC-dependent top-20p set with no stability theorem; no route in any source. |
| 8: work–depth theorem | K87, K88, K89 (card D11). |
| 8: R vs N | K59: defer (PROOF SKETCH); v1 states the two PROVED halves (K48, K49). |
| 8: island variance vs correlation | K53 (coarse, supplement) + §E card (E[W²] under IID idealisation; hybrid OPEN). |
| 8: speed-up vs MCMC | K91 drop: empirical only (INP §5 row 8); no comparator theorem. |
| 9: two-sided masked Ẑ | K40 limitation + K53; two-sided OPEN (V11): defer. |
| 9: floating point | K107, K108 supplement; VAL-FP remains measured only (N16). |
| 10: joint inclusion | K46 + K51 (N1). |
| 10: credible sets | nothing (rejected target; §F). |
| 11: P(U) → 0 | K82: not a theorem; every statement joint with 𝒪; OPEN delivery, not a limitation. |
| 11: finite-n Gibbs-route discovery | nothing provable: no route (ThmB-T24 vacuous at n = 200). |
| 12: meaning of `local_certified` | K64 + card L1 (K73): deterministic semantics, supplement. |
| 13: positive flag power | K80 (detection probabilities of E1–E3 under stated alternatives, supplement); universal power impossible (K79). |
| 14: P(resource_limit) etc. | K82 (OPEN delivery); fp theorem K107. |

---

## §B The draft list, item by item (item 2)

| entry | K-ID | verdict | corrected statement or reason | IC |
|---|---|---|---|---|
| V1 | K35, K36, K46, K47, K48, K50, K32, K86, K20, K21, K08 | **split**: (a1) Ẑ and RB-PIP identities → cited lemma (Del Moral 2006; WLH 2016) stated as Proposition V with method hypotheses; (a2) general h → **keep** as Theorem clause (N1) | Hypotheses: EX-A, EX-S, frozen 𝓒 on streams 0–9, R′ = 4k and N_e declared before stream 10, GUARD-W, q_φ-invariant rounds (N9). (b) in output-event form P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05. (d) negative clause kept. | IC4, IC1 |
| V2 | K63, K83, K84, K86 | **demote** to supplement lemma (Lemma S + Cor W-R(b)); Prop W/W-cal stay code-audit facts | Lemma S and top_c merge: theorem-grade finite combinatorics (Lean); "bitwise" claims scoped per METHOD §2 #1–#2; W-cal not executed. | IC5 |
| V3 | K48, K49, K50, K51, K85 | **merge**: (ii),(iii) into Thm H (card D2); (i),(iv),(v) supplement Proposition P | (iii) replaced by PC1 claim 3 form (K52) plus A1(a); "R declared before stream 10" rule stated once. | IC4, IC5 |
| V4 | K77, K78 | **demote** to supplement lemma; GUARD-W enters every output-event theorem as a named hypothesis (N2(e)) | Lemma RO as recorded (XF VERIFIED); CEX-guard as the motivating counterexample; literal "every output equals" wording struck (A-REV8). | IC1 |
| A1 | K51, K46, K48 | **keep** (main, card D2), restated per M9 | h ∈ 𝓗 measurable in (X, y, 𝓒); plain measured-round averages, c_h = 0 for joint h; RB marginal only; (d) with R_n a hypothesis and the Cauchy–Schwarz lower bound disclosed; do not cite FMP-M3. | IC1, IC2 |
| A2 | K35, K36, K38, K39, K40, K41, K42, K53, K79 | **split**: (i),(iv) → certificate theorem (card D3); (ii),(iii) → supplement Thm Z (card D12); (v) → remark | Mandatory wording PC1 claim 4 ("underestimates w.h.p.; compensating rare overestimates; P(Ẑ > 20Z) ≤ 0.05"); add N17 analytic bound; (ii) novelty vs Cérou–Del Moral–Guyader 2011 Thm 1.4 unchecked → check wave. | IC1, IC4 |
| A3 | K42, K43 | **merge** with N13 (K45) and card G1/G2 (K42, K36, K78) into Theorem Z𝒯/CARD (main, card D3) | Add: S₀ ∈ 𝒮 and δ₁ < ½ ⇒ S₀ ∈ 𝒯 and MPM^𝒯 = S₀ (sharp ½); holds under LS0 via 𝒯_new = top_c(𝒯_old ∪ 𝒮_added). | IC1 |
| A4 | K57, K58 | **split**: P1 → supplement (card D14); Thm R → **defer** (DELIV-POP OPEN) | Equal-weight is secondary; P2 needs locking (general LH locking FALSE, A-REV7): state P2 only at fixed p on LH under C1–C3. | IC2 |
| D1 | K06, K64, K87, K88, K89, K90 | **keep** as island-level Theorem D (supplement, card D11) | Strike "free of N, H, R" (v3.2 only); depth = N_e(T+L+4)(p+B+2) sequential step slots per island + setup + calibration (1+I_e)H_e; scan bound p + k*(p−k*), k* = min(K,⌊p/2⌋); (d) SL comparison as accounting remark. | IC1 |
| D2 | K26, K28, K29, K30, K31 | **keep** (main, card D7): (a) as-coded G with G(i) cited (SVV 2009); (c) STG-M; (b) STG-F supplement; (d) cited (Syed et al. 2024); Conjecture P **defer** | State the ESS-0.90 hypothesis (pilot = grid) explicitly; (c) on the ideal two-state grid, as-coded T ≤ T_e. | IC4, IC3 |
| D3 | K96 | **keep** as the assembly theorem (main, card D10); exact scope at agenda 6 | Replace "free of N, H, R" by island-level depth; remove M3 (XF ERROR) from the assembly; (c) uses K52 and the E[W²] lower bound. | IC1 |
| D4 | K59, K39 | **defer** (PROOF SKETCH); v1 states K48, K49 and the design decision | No route beyond the exact-refresh idealisation (OPW2-cex warns against a_t = χ²_t). | IC2 |
| S1 | K15, K16, K17, K18, (K10) | **keep** (main, card D4); (b) supplement | Add ST2/WS3 σ²-coupling clause (K10) as (e); never combine (b) and (c) on one sequence; do not cite DIL-DM(i). | IC3 (LH exhibited) |
| S2 | K105, K106, K19 | **keep** (main, card D5) | Lemma KL to check wave 1; "moving off the start is needed", not "tempering is needed". | IC1 |
| S3 | K98 | **drop** (known-false: SHARE-M(b), FD-NM ERROR) | Replaced by S2 + a one-sentence Prop M-LH remark. | IC1, IC2 |
| S4 | K102 | **keep, restated** (main, card D6, §E) | Weight stability under weak cross-block *leakage* CBL(η), EBM(M_n), SE-blk(φ₀): per-stage χ² ≤ 1/m² − 1 for every grid; obstruction WS6(d). | IC3 |
| C1 | K97 | **keep** (main, card D9) | Crux (ii): orthogonal-null PIP → 0 under SL's IG + Gaussian + λ_s prior; re-run numerics on LH with g ≥ 2, K ∈ {2,4,√p}; LH-iid future work. | IC2, IC3 |
| R1 | K93 | **keep** (main, short; MODEST) | Disclose n ≳ 2·10⁶; T03♯(3) is Rossell 2022 Prop. 1 (cited lemma); scope sentence N12. | IC4 |
| R2 | K60 | **demote** to cited lemma (Barbieri–Berger 2004); (iii) size-prior ceiling as a remark | Prop1-wrongHPM data paragraph not to be cited (XF ERROR). | IC4 |
| R3 | K65 | **keep** as the lemma feeding Thm 5 (card D8); Lean sorry-free | New hypotheses: LS0 centre = prescribed start mode (e4, N3 OPEN), ℓ ≥ max{Φ(S°)−1, 0} (N11), completed scans (OP-LS0); capped lattice only. | IC1 |
| R4 | K72, K78 | **merge** with R5 into Theorem HPM (card D8) | Output-event form; add PC1 claim 5(a); the 2E₀δ₁ term cited (Rossell); no "first finite-n" wording (Hou–Wang–Atchadé). | IC1, IC4 |
| R5 | K19, K68, K69, K70, K71, K72, K87 | **keep** headline (b1-LH) with LS0 + (b2-LH) subfamily; **split** off (b1-LH-iid) (K71) → future work; (a) favourable supplement | Hypotheses OP-LS0, e4, SIZE g_max ≤ B < 2g_min, GUARD-W; study generator → N8 disclosure. | IC1, IC3 |
| R6 | K82 | **reject as theorem**; not a limitation; stated as "delivery OPEN, every result joint with 𝒪" | Remove "≈ 4× headroom". | IC2 |
| R7 | K94 | **defer** Π(X) given design (future work); supplement candidate for the E₀-averaged bound (card D20) | T34/TG5 route is credible for E₀[1 − π(S₀)], not for Π(X). | IC2 |

---

## §C New candidates (item 3)

| K-ID | placement | reason (≤ 40 words) |
|---|---|---|
| K01 | supplement (card D17) | Propriety and envelopes; finite algebra, Lean-able; composes with N17. |
| K02 | supplement (card D17) | Invariance/equivariance; needed once; the tie limitation is a remark. |
| K03 | supplement (card D17) | Reduction identity + IG bound; resolve the 2νb₀ vs n·b constant in check wave 1. |
| K04 | cited lemma (BB(1,p) identities) | Known beta-binomial facts; the geometric-tail warning is a remark. |
| K05 | supplement (card D18) | Furnival–Wilson superset bound makes card R's B&B bound explicit. |
| K07 | supplement (card D21) | PART-ThmA (PROVED, XF VERIFIED*) restated with strict separation; N8 stays OPEN. |
| K09 | supplement (card D16) | Tie-aware DP invariant is obligation N3; needed for LS0 hypotheses. |
| K10 | main (inside card D4/D6) | σ²-coupling d_σ ≥ 0 under BO: WS3 PROVED (no review); the baseline for §5.3. |
| K11 | supplement (card D6 remark) | WS4 PROVED; my check shows the constant is vacuous at n^{−1/2} correlation: honest remark only. |
| K12 | drop (engineering) | Test oracle, not a guarantee. |
| K13 | defer | Needs TG4-type bounds plus the start-mode landscape; no route independent of HP3/HP4. |
| K14 | supplement (card D21) | Within-block masking immunity: trivial, deterministic; converse of K99. |
| K22 | supplement (card D16) | Graph facts; (b) heuristic only, not familywise. |
| K23 | supplement (card D16) | Dirichlet-form comparison, finite, Lean-able; feeds no paper-1 mixing claim. |
| K24 | defer (future work) | Route blocked as stated (N10); relies on PARTLY-FALSE landscape row. |
| K25 | supplement (card D19) | Exact coverage factor a_u a_w/a_v²: what the restricted ESS certifies. |
| K27 | main (inside card D7) | Per-interval (v−u)²Var_ξ(d) ≤ log(10/9); the lemma behind stage counts. |
| K33 | supplement (engineering) | Termination/cost of build_grid; N15 share seat-derived. |
| K34 | drop | TI reporting is not in v3.1 (method change). |
| K37 | supplement (card D12) | Island-minimum bound needs independence; Hoeffding bracket may be vacuous. |
| K44 | main (inside card D3) | N17 PROVED analytic upper bound; U_rest bracket E-only (check). |
| K45 | main (inside card D3) | N13 retention lemma PROVED (PC1 claim 5). |
| K52 | main (inside card D2) | PC1 claim 3 finite-R bound; given N1 for general h. |
| K54 | supplement (card D19) | R_eff limit and variance estimator; no coverage at R = 4. |
| K55 | cited lemma | Chopin 2004 / Del Moral 2004 CLTs. |
| K56 | supplement (one step) | One-step RB variance reduction only; general claim deferred (D–E disagreement). |
| K61 | cited lemma | Müller–Parmigiani–Rice-type FDR fact for exact PIPs. |
| K62 | main (inside card D8) | Margin transfer: estimated MPM = exact MPM; deterministic. |
| K66 | drop (PARTLY-FALSE) | Cannot escape C3-PGD/VPGD-PropG/CEX-localmax without a new hypothesis none has supplied. |
| K67 | drop (PARTLY-FALSE) | Relies on K66; LH analogue already covered by K69. |
| K73 | supplement (card D18) | Card R soundness: OCERT-LemmaM, C4 PROVED, XF VERIFIED. |
| K74 | supplement (card D15) | Restates CEX-localmax, CEX2 as limitation. |
| K75 | future work | NP-hardness needs its own reduction; D–E disagree; paper 2. |
| K76 | supplement (card D17) | Eventual exact dispatch; correction of T26-exact-branch-paren. |
| K80 | supplement (card D15) | Detection probabilities of E1–E3 under declared alternatives; modest. |
| K81 | supplement (card D15) | Restates CEX-ESSneutral(A3). |
| K91 | drop | No comparator; empirical only. |
| K92 | future work | Built on the unproved moat lemma; D defers it. |
| K95 | supplement (card D17) | Finite posterior-odds identity; Lean-friendly; sums over Ω so not a run certificate. |
| K99 | supplement (card D15) | Limitation; construction must respect clustering ties and the cap. |
| K100 | supplement (card D15) | Duplicates: PIP → 1/d; cites PropD-T03, CEX-ties. |
| K101 | supplement (card D15) | MPM may exceed K; trivial. |
| K103 | supplement (card D16; §F TV) | Textbook minorisation; constant 1/M_φ (E) vs 1/(mM_φ) (D) to settle. |
| K104 | supplement (card D19; §F KL) | Gelman–Meng identities; cited. |
| K107 | supplement (card D18) | Rounding bound and exact semantics; T33-errbound warns the engine's η is not a bound at large n. |
| K108 | supplement (card D18) | Deterministic perturbation lemma. |

---

## §D Theorem cards

Fields: ID · statement · guarantee · goal · status verbatim (registry ID) and fidelity · self-checked? · novelty · route/key lemma · difficulty · Lean core · depends · risk · fallback + stop rule · IC3 design · numerical companion.

### D1 · Proposition V+ (fixed-data validity; the general-h identity) · **main** · K35, K46, K32, K86, K36, K50, K20, K21, K08

| field | content |
|---|---|
| statement | EX-A, EX-S; 𝓒 frozen on streams 0–9; R′ = 4k, N_e declared before stream 10; GUARD-W; every elementary move γ_φ-reversible and the random-order round q_φ-invariant (N9). For each island r, conditionally on 𝓒: E[Ẑ_r] = Z; E[Ẑ_r PIP̂_rj] = Z·PIP_j (RB record before the Gibbs draw); **E[Ẑ_r H_r(h)] = Z·π(h)** for every h ∈ 𝓗 measurable in (X, y, 𝓒) (M9 accumulation); P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05; the pooled product Ẑ·PIP^eq is not unbiased (bias −(1−1/R)Cov). |
| guarantee | Whatever the correlation, every island's unnormalised evidence and summaries are exactly unbiased, and the frozen calibration cannot bias them. |
| goal | §5.1, §5.2, §13.1 (crux N1); objective 1. |
| status | T12: PROVED-LOCKED; T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); Prop2(c): PROVED (XF VERIFIED); N1: PROOF SKETCH; N9K: PROVED (candidate); IND-T: PROVED (XF VERIFIED*). Fidelity: LS0 n/a (reads no uniforms), coded grid yes (any frozen 𝓒), Ẑ-weighted pooling yes. |
| self-checked? | N9K author-only (consultant); N1 unchecked; IND-T for streams 10..9+R′ code audit pending. |
| novelty | KNOWN—CITE (Del Moral et al. 2006; WLH 2016 §5.1; Dai et al. 2022 (4.8); Grosse et al. 2015). New: N1 at the measured-round accumulation point with random-position RB; the negative clause. |
| route | Finite-state resample–move recursion: E[offspring avg f | particles] = weighted avg Kf; terminal rounds π-invariant; prefix-invariance for the random position (E T17, D KN7). Key lemma: "T15 at a terminal-round prefix" for general bounded h. |
| difficulty | S–M. |
| Lean | T12Core partial (hstep); island identity (a) and clause (d) certifiable on an abstract finite space; N9 detailed-balance matrices. |
| depends | N9, GUARD-W audit (N2(e)), IND-T. |
| risk | N1 fails → §13.1 escalation (binding). |
| fallback | (a1) marginal PIPs only (locked); stop rule: one check wave on N1's prefix lemma; if GAP persists, escalate. |
| IC3 | any design (no design hypothesis). |
| numerical | N9-KERNEL CHECK (detailed balance ≤ 2.3e-12); none needed for N1 beyond a 2-state enumeration (check wave). |

### D2 · Theorem H (Ẑ-weighted estimates of bounded h; finite-R) · **main** · K51, K52, K48, K46

| field | content |
|---|---|
| statement | Setting D1; h: Ω → [0,1] in 𝓗; ĥ_r = H_r(h) (plain measured-round average; RB only for marginal PIPs). (a) islandwise, every regime, every frozen grid: E[W_r·|ĥ_r − h(S₀)| | 𝓒] ≤ 2δ₁, δ₁ = 1 − π(S₀); (b) P(|μ̂_w(h) − π(h)| > ε | 𝓒) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}, M = E[(Ẑ_r/Z)²|𝓒]; (c) P(|μ̂_w − h(S₀)| > t | 𝓒) ≤ exp{−R(1−s)²/(2M)} + 2δ₁/(st); (d) joint inclusion h_A = 1{A ⊆ S}; (e) fixed data: μ̂_w → π(h) a.s. as R → ∞ at fixed N; (f) n → ∞ under T03♯: with R_n(1−s)²/M_n → ∞ in probability, μ̂_w → h(S₀). |
| guarantee | Any declared summary is right on the islands that carry evidence weight, and pooling enough islands by Ẑ makes it right; the price is R ≍ M. |
| goal | §13.1 (binding), §5.4 PIP/joint-PIP error; objective 1. |
| status | A1new: PROOF SKETCH (NEW-SYNTH); FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)); PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r] = π(h) is still a premise'; MA-PropP: PROVED (elementary); N4(i): PROVED, given N1. Fidelity: Ẑ-weighted primary yes; LS0 n/a; coded grid yes. |
| self-checked? | PC1 claim 3 Astra-authored, Opus-checked; M1 XF VERIFIED; (a) for general h unchecked. |
| novelty | NEW-COMP (mechanism F-MASKPIP; SLLN WLH). LIT-SMC: masked-regime results sit where general bounds are vacuous. |
| route | (a): |ĥ_r − h(S₀)| ≤ fraction of measured particles off S₀; island identity for 1{S ≠ S₀} (N1). (b): PC1 claim 3 (Chebyshev + denominator event). (c): Maurer on W̄_R + Markov. Key lemma: N1. |
| difficulty | M (copy M1 with h; compose). |
| Lean | (a) deterministic step and (b) finite inequality certifiable; Maurer/SLLN cited. |
| depends | D1 (N1), D13 (T03♯) for (f). |
| risk | M unbounded under masking (N4(iii) OPEN); (f)'s R_n uncheckable; disclose E[W²] ≳ 1/P_𝓒(cross). |
| fallback | marginal PIPs (locked identity) with (b),(c); stop: if N1 GAP after wave 1 → escalation. |
| IC3 | any design; non-vacuity: M finite for every finite grid (envelopes K44/T11). |
| numerical | none required; optional 2-state enumeration of (b). |

### D3 · Theorem Z𝒯 / CARD (deterministic brackets and output-event coverage) · **main** · K42, K43, K45, K36, K78, K44

| field | content |
|---|---|
| statement | 𝒯 the deduplicated top store, Z_𝒯 = Σ_𝒯 ϖm. (a) Z_𝒯 ≤ Z; π(S) ≤ e^{F(S)}/Z_𝒯; Ẑ < Z_𝒯 ⇒ Ẑ < Z. (b) If S₀ ∈ 𝒯: 1−δ₁ ≤ Z_𝒯/Z ≤ 1, |PIP^𝒯_j − PIP_j| ≤ δ₁, |π_𝒯(h) − π(h)| ≤ 2δ₁ for bounded h. (c) If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 and MPM^𝒯 = S₀ (½ sharp); holds under LS0 (𝒯_new = top_c(𝒯_old ∪ 𝒮_added)). (d) Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}. (e) P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; card-level: P(𝒪 ∩ {some G2/L/R item false}) ≤ 0.05, never conditional on completion. |
| guarantee | The run's own record gives two-sided evidence/PIP accuracy whenever the truth was scored, and a 95% certificate joint with output. |
| goal | §5.4 (evidence coverage), §4.4/§8.2 diagnostics; objective 1. |
| status | MZ-P3: PROVED (P3 top store, deterministic); PC1c5: (a) PROVED, ½ sharp; N13: PROVED (PC1 claim 5); PC1c2: PROVED for the potential run; output-event version CORRECT WITH AMENDMENT; N6(b): PROVED modulo premise (i); N17: PROVED (PC1 claim 1); OCERT-C1: XF ERROR as quantified (use O-VCERT R1 wording). Fidelity: LS0 yes (R3_B), coded grid yes, pooling n/a. |
| self-checked? | PC1/PC2 cross-family; GUARD-W premise un-audited. |
| novelty | NEW in kind (reported-quantity trick), elementary; Markov bound KNOWN—CITE (Grosse et al. 2015). |
| route | Finite sums; Lemma S + inheritance merge for (c); Markov + Lemma RO + GUARD-W for (e). Key lemma: N13 retention. |
| difficulty | S. |
| Lean | (a)–(c) finite inequalities; (e) finite event algebra given Lemma RO. |
| depends | GUARD-W audit; D8 for "S₀ ∈ 𝒮". |
| risk | fp label until SC + VAL-FP (N16). |
| fallback | exact-arithmetic statement with numerical label (already the adopted text); stop: none needed. |
| IC3 | any design. |
| numerical | PC2 exact-rational test (60 cases) exists. |

### D4 · Theorem 2 (the start: deterministic mass, σ²-coupling, masking law, dilution) · **main** · K15, K16, K17, K18, K10

| field | content |
|---|---|
| statement | Blocks any partition; tables r_b; π₀ = γ₀/Z̄₀. (a) π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s; odds π₀(S₀)/π₀(S°) exact; bridge mass ≥ min(π₀(S₀), π(S₀)). (b) Under BO: d(S) = d_σ(S) = ν[Σ_b log(1−x_b) − log(1−x̄_S)] ≥ 0, zero iff ≤ 1 active block; with known σ² the start equals the posterior (FD-W1). (c) Masked chain (H2, H3): π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}; on LH exact Gram no open hypothesis. (d) −log π₀(S₀) = V + C − log A for any data and partition. (e) [supplement] favourable rate 1 − π₀(S₀) = O_P(2^B√log n·n^{−κ}) under EXP′, VIS, NL. |
| guarantee | The merge is exactly computable, carries the truth when blocks see it, and provably loses it polynomially when truths cancel across blocks; even orthogonal blocks leave a σ²-sharing discrepancy. |
| goal | SL Thm 4/Cor 2 (exceeded); §5.3 baseline; objective 1, 3. |
| status | T22(i)(ii)(iv): PROVED-LOCKED; T22(iii): PROVED-LOCKED CONDITIONAL; T27(i): PROVED-LOCKED, CONDITIONAL; Thm3-EXP, Thm4-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)); DIL-E: PROVED (XF: VERIFIED (A-REV9)); OWS-WS3: PROVED (no review); FD-W1: PROVED, XF VERIFIED (A-REV4); DIL-DM: XF ERROR (do not cite). Fidelity: production start; LS0, grid, pooling n/a. |
| self-checked? | WS3 unreviewed (Fable-authored); D ST2 independently restates it (SC1 5e-14). |
| novelty | NEW ((c),(d): "strongest novelty claim", LIT-STAT); block start KNOWN (Papaspiliopoulos–Rossell 2017). |
| route | Finite algebra on tables; Gaussian probability for (c),(e). Key lemma: WS3(b) mean-field representation (π₀ = π with an independent noise precision per block). |
| difficulty | S (restatement). |
| Lean | (a), (b), (d) finite identities; good first G4 target. |
| depends | nothing; feeds D5, D6, D7, D9. |
| risk | none material. |
| fallback | drop (e) to the supplement (already); stop: none. |
| IC3 | LH exact Gram (c linked pairs) for (c); any partition for (a),(d); any BO design for (b). |
| numerical | D's SC1; registry DIL 480 fits. |

### D5 · Theorem SEP + Lemma KL · **main** · K106, K105, K19

| field | content |
|---|---|
| statement | LH exact Gram, cancellation depth c, Q* = p^c n^{c/2}. (a) P₀(S₀ scored by Q iid π₀ draws + tables) → 0 if Q/Q* → 0, → 1 if Q/Q* → ∞. (b) 1 + χ²(π‖π₀) ≥ Q*e^{O_P(1)}; the self-normalised one-shot estimate of π(S₀) is 0 w.p. → 1 below Q*. (c) KL(π‖π₀) ≥ (1−δ₁)log(1/π₀(S₀)) − log 2, so the Chatterjee–Diaconis sample size exp(KL) ≥ ½Q*^{1−δ₁}e^{O_P(1)}. (d) Q draws miss the HPM S* w.p. ≤ exp(−Qπ₀(S*)) (general). |
| guarantee | Keeping or one-shot-correcting the merge costs p^c n^{c/2} draws; this is necessary and sufficient for any one-shot scheme. |
| goal | §5.4 (KL), §5.3 contrast; objective 1. |
| status | SEP-A: PROVED (XF: VERIFIED (A-REV9)); SEP-B: PROVED (XF: VERIFIED (A-REV9)); SEP-A-iid: PROVED-UNDER; KL: PROOF SKETCH (NEW-SYNTH); OWS-WS7(a): PROVED (no review) proves the same KL inequality with π(S₀) in place of 1−δ₁. Fidelity: iid draws, no LS0 (as stated). |
| self-checked? | Lemma KL unreviewed (two lines; WS7(a) is an independent same-family proof). |
| novelty | SEP NEW (no BVS tempering separation published, LIT-SMC); exp(KL) scale KNOWN—CITE (Chatterjee–Diaconis 2018 Thms 1.1/1.2). |
| route | Data processing on {S₀, S₀ᶜ}; SEP by W7-SEP. |
| difficulty | S. |
| Lean | Lemma KL (finite KL, log-sum); (d) elementary. |
| depends | D4(c). |
| risk | none; wording discipline ("moving off the start is needed"). |
| fallback | cite WS7(a) form; stop: none. |
| IC3 | LH exact Gram, explicit (g, c, ρ, ψ). |
| numerical | THM-SYNTH check_lemmas.py. |

### D6 · Theorem WSTAB-C (weight stability under weak cross-block leakage) · **main** · K102 restated; K10, K25, K27 · full card in §E

### D7 · Theorem STG (stage laws of the grid) · **main** · K26, K27, K30, K28, K29

| field | content |
|---|---|
| statement | Grid rule as coded, threshold ρ* = 0.9 on V, pilot targets. (a) ρ_V(u,v) is nonincreasing in v, bisection finds the exact frontier, the greedy grid is the shortest valid grid, T ≤ T_e on success (ESS 0.90 for pilot and grid is a hypothesis). (b) every interval satisfies (v−u)²Var_{q_ξ|V}(d) ≤ log(10/9) for some ξ ∈ (u, 2v−u); hence T ≤ 1 + ⌈σ_max/0.3246⌉ + #pilot targets. (c) ideal two-state exact-frontier grid: a dominance crossing of log-odds gap A₀ costs log₂A₀ + O(1) stages, and no V, N or seed removes this. (d) [cited] √c·T*(c) → Λ as c → 0. (e) [supplement] favourable BO: T* bounded through q_w(S₀). |
| guarantee | Correlation enters depth only through computable functionals of d: the spread of d (smooth part) plus log₂ of each crossing's gap. |
| goal | objective 2; thesis (b); SL §6 contrast. |
| status | STG-G: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic; STG-L0/L1/L: PROVED (SF: none; XF: none); STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)); STG-F: PROVED; STG-Wp: PROVED-UNDER (conflict C22); STG-cexW2: COUNTEREXAMPLE to "O(1) stages"; ConjP: OPEN. Fidelity: (a),(b) as-coded rule; (c) ideal two-state grid (**not coded grid**). |
| self-checked? | STG-G/L author-only (O-STAGES); D's BR2/BR3 restate (b). |
| novelty | G(i) KNOWN—CITE (Štefankovič–Vempala–Vigoda 2009); (d) KNOWN—CITE (Syed et al. 2024 Thm 3); (b),(c) NEW, elementary. |
| route | WS1(a)/BR1: 1+χ² = exp(Λ(w) − 2Λ(v) + Λ(u)); second-order mean value; two-point algebra. Key lemma: K27. |
| difficulty | S (v1); Conjecture P M–L (deferred). |
| Lean | Lemma RS, monotonicity, greedy optimality, two-state asymptotics (real analysis). |
| depends | D4 (A₀). |
| risk | (c) on the ideal grid only; disclose. |
| fallback | (a),(b) only with T ≤ T_e; stop: Conjecture P not attempted in paper 1. |
| IC3 | two-state family (c); any V (a),(b). |
| numerical | D's SC2 (≤ 20 runs): log₂(gap) + 6.7 ± 0.5. |

### D8 · Theorem HPM (composition for every n; two-regime consistency with LS0) · **main** · K72, K68, K69, K70, K65, K63, K62

| field | content |
|---|---|
| statement | EX-A, EX-S, CAL, SR, GUARD-W, (P), OP-LS0, e4 centre rule, ℓ ≥ max{Φ(S°)−1,0}. (0) P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n; N200 bracket with Π(X). (1) Lemma A/LS-score: under TD′ on Lat(S°) the search from any centre in Lat(S°) scores S₀ in ≤ Φ moves; LS0 scores S₀ within max{Φ(S°)−1,0}. (2) (b1-LH): on LH exact Gram (p ≤ n−1, g_max ≤ B < 2g_min) with LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with no open statistical hypothesis. (3) (b2-LH): without LS0 on the STAB-LH subfamily (g = 9, c = 2, ρ = 0.4, ψ = 0.2), any frozen grid. (4) margin transfer: exact PIPs ≥ δ from ½ and uniform error < δ ⇒ reported MPM = exact MPM. (5) cost polynomial (T32(i) + LS0 term). |
| guarantee | The reported model is the truth w.p. → 1 − limsup P(U) on an explicit correlated masked family, for the shipped method. |
| goal | objective 3; SL Thm S (exceeded). |
| status | Thm4-C1: PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none); T38-(0): PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5)); N200: PROVED (elementary, every n); TheoremA: PROVED (SF: VERIFIED; XF: VERIFIED* (A-REV2)); LS-score: PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8)); T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)); Thm-b1: PROVED-UNDER (XF: VERIFIED (A-REV8)); B2E-B2LH: PROVED-UNDER (XF: VERIFIED* (A-REV7)); T38-b1-LH-iidfail: XF ERROR (c = 2 clause repaired). Fidelity: LS0 yes ("v3 + LS0"; bridge to code N2(c) pending); coded grid: any frozen grid; pooling n/a. |
| self-checked? | N200 author-only; STAB certificate Astra-authored, Claude-verified. |
| novelty | NEW for this target and method; "corollary of YWJ/ZYVR under their prior" (LIT-MCMC): say both; no "first finite-n" wording. |
| route | Statement of record T38_STATEMENT v3; Lean sorry-free for (0) and Theorem A. |
| difficulty | S (assembly). |
| Lean | T21HPM.lean, T37Greedy/Lattice.lean sorry-free; LS-score move count short addition. |
| depends | D13 (δ₁), N3 (e4 DP invariant OPEN), N2(c) merged-LS0 replay. |
| risk | e4 invariant OPEN; study generator uncovered (N8). |
| fallback | (b2-LH) on STAB-LH without LS0; stop: if N3 fails, LS0 route carries e4 as hypothesis. |
| IC3 | LH exact Gram, explicit (g, c, ρ, ψ); STAB-LH subfamily. |
| numerical | LS0 changed 0/2,394 HPMs; 0/2,400 tie truncations. |

### D9 · Theorem SL (separation from split-and-merge) · **main** · K97

| field | content |
|---|---|
| statement | LH exact Gram (c linked pairs). SL procedure as in JRSS-B §3.1 with uniform equipartition into K_n subsets. (a) P(masked hub isolated from its partner and group) ≥ 1 − c·g/K_n → 1 when K_n → ∞ (hypergeometric). (b) On that event the hub is an exact orthogonal null column in its subset: cov(x_t, y) = 0 (Condition 5 fails), β_{0,t} = 0 in eq. (19) at every iteration, π(t ∈ ξ | D_n^s) = O_P(λ_s n^{−1/2}) → 0; SL's output cannot contain it. (c) The exact posterior has 1 − π(S₀) → 0 (Thm5-LH/T03♯). (d) v3.1 on the same family: D1 holds and (D8) the HPM → S₀. |
| guarantee | SL's correctness condition is violated exactly by a cancelling pair; v3.1's correctness has no such condition. |
| goal | ground rule 2 (SL comparison), objective 3 under correlation; thesis (d). |
| status | C1new: COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (NEW-SYNTH); Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none); T38-b1-LH as D8. Fidelity: (d) shipped method. |
| self-checked? | sketch unchecked; numerics on Liang's slides family (g = 1), not LH. |
| novelty | NEW (no analytic SaM failure published); citation checked against the JRSS-B text (Thm 4, Cor 2, eq. (19), Condition 5). |
| route | finite combinatorics for (a); linear algebra x_tᵀμ = (n−1)(θ_t + ψθ_a) = 0 for (b); null-column Bayes factor under SL's IG + Gaussian + λ_s prior (one page, Laplace/ratio bound). Key lemma: (b)'s PIP → 0. |
| difficulty | M. |
| Lean | (a), (b)'s identity, (e) 2×2 inverse: certifiable. |
| depends | D4(c), D8, D13. |
| risk | FDR threshold data-driven: state for fixed q ∈ (0,1), add FDR rule as escalation. |
| fallback | numerical counterexample on LH (g ≥ 2, K ∈ {2,4,√p}) + (a) as theorem; stop: if (b)'s PIP step fails under SL's prior, ship (a)+(c)+(d) and the numerical (b). |
| IC3 | LH, c = 1, g = 4, ρ = 0.5, ψ = 0.2, p = 64, K_n = 8. |
| numerical | re-run ≤ 20 seeds on LH (HQ-SL step 1). |

### D10 · Theorem CD (thesis assembly) · **main** · K96

| field | content |
|---|---|
| statement (v1 scope, agenda 6 fixes wording) | Fix any design and data, EX-A, EX-S, CAL, R′ declared. (a) never correctness: D1 + D2(a),(e) with no premise on X. (b) costs depth: island-level depth N_e(T+L+4)(p+B+2) + calibration, T ≤ T_e; on the ideal grid T = log₂A₀ + O(1) per masked crossing, A₀ a functional of X through the blocks (D4, D7). (c) costs islands/particles: D2(b),(c) with M = E[W²|𝓒] ≳ 1/P_𝓒(cross) (Cauchy–Schwarz + FMP-M2) and, under weak leakage, D6's bound on per-stage χ². (d) selection: D8, D9. |
| guarantee | Correlation enters only T, R, N and delivery; never the target, the identities or the limits. |
| goal | thesis; objectives 1–3. |
| status | D3 draft: assembly (A1 PROOF SKETCH, D2 ideal grid/OPEN as-coded); FMP-M3 (XF ERROR) removed from the assembly; FMP-M2 PROVED (XF VERIFIED). Fidelity: island-level only (Felipe). |
| self-checked? | assembly only. |
| novelty | NEW-COMP (LIT-PAR S-GAP). |
| route | assembly; no new lemma. |
| difficulty | that of D2, D6, D9. |
| Lean | none beyond parts. |
| depends | D1, D2, D4, D6, D7, D8, D9. |
| risk | exact scope (fixed data vs asymptotic, favourable vs masked) is agenda 6. |
| fallback | state (a),(b),(d) with (c) as a bound in M; stop: none. |
| IC3 | inherited from parts. |
| numerical | none. |

### D11 · Theorem D (work, depth, width; SL §6 comparison) · **supplement** · K87, K88, K89, K90, K06, K64

| field | content |
|---|---|
| statement | Work W = J·2^B s(B) + calibration [H_e(1+4I_e)(T+L+4)]m s̄ + R′N_e(T+L+4)m s̄ + (ℓ+1)(p + k*(p−k*))s̄ (final search, extra search, LS0) + O(np²) + clustering; island-parallel depth = setup + Σ_e(1+I_e)H_e(T+L+4)m + N_e(T+L+4)m slots + local search, width R′; ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉, Σ_b 2^{|C_b|} ≤ p2^B/B; Brent time ≤ W/P + D; depth Ω((T+T_cal)·m) and Θ(p²) Gram memory are ceilings. SL §6: O(p^{(1+α)/2}) + O(np) with K = √p, output restricted; v3.1 same order in p at α = 1 with more width, output π exactly. |
| guarantee | Honest work/depth/width accounting at the implemented level; no speed-up claim. |
| goal | objective 2; SL §6. |
| status | MA-PropD: PROVED (counting); T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none), displayed rate GAP (A-REV5); Cost-T38: PROVED-UNDER (XF: GAP); N15 calibration share seat-derived, not proof-checked. Fidelity: LS0 term added; island level; "free of N,H,R" struck. |
| self-checked? | yes (counting; share unchecked). |
| novelty | accounting (TCS style); KNOWN. |
| route | copy Prop D; next-fit ≤ 2·OPT (Johnson 1973). |
| difficulty | S. |
| Lean | counting identities; low value. |
| depends | D7 (T). |
| risk | METH-AUDIT measured table placeholder: check before citing. |
| fallback | work only; stop: none. |
| IC3 | n/a. |
| numerical | timings tabulation (METHOD §6 #9). |

### D12 · Theorem Z (evidence variance, masked lower tail, bounds) · **supplement** · K39, K40, K38, K37, K41, K53

| field | content |
|---|---|
| statement | (i) exact variance identity N·Var(W_T|𝓒) = Σ_s(1−1/N)^{T−1−s}(E[W_s²μ_s(h²_{s,T})] − 1); under exact refresh ∏(1+χ²_t/N) − 1 (idealisation, not the kernel: OPW2-cex). (ii) masked lower tail: P(W > (T/η)[π₀(Aᶜ)/π₀(x_m)]e^{−φ_{τ_A}D_A}) ≤ η + Nπ₀(A); if the terminal population is off S₀ w.p. ≥ κ then Ẑ_r ≤ √δ₁Z there. (iii) E[log Ẑ_r] ≤ log Z. (iv) island-minimum bound 0.05^{1/R}min_rẐ_r (independence). (v) favourable: Ẑ/Z → 1 under (P1) (remark). (vi) design-free Var(Ẑ_r/Z|𝓒) ≤ (T+1)e^{2D}/N (crude). |
| guarantee | What Ẑ's error looks like in each regime, with the mandatory PC1 claim 4 wording. |
| goal | objective 1; §5.4. |
| status | OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); OPW2-ThmB: PROVED (XF: VERIFIED*); MZ-E1E2: PROVED (candidate); FMP-Na: PROVED (XF: GAP); PC1c4: PROVED; T26-ThmA: PROVED (XF: VERIFIED*); A2 Thm 6 overall CONJECTURE; N4(iii): OPEN/CONJECTURE. Fidelity: frozen calibration; (i) exact-refresh clause is a variant. |
| self-checked? | E1/E2 candidate (Fable); (vi) E-only sketch. |
| novelty | (ii) NEW; (i) "same kind as Cérou–Del Moral–Guyader 2011 Thm 1.4" **unchecked** → citation checker. |
| route | two-lineage expansion; frozen-path log W = (a+Λ)(φ* − φ_τ) + O(1). |
| difficulty | S assembly; two-sided masked (V11) deferred. |
| Lean | (i),(iii) finite identities. |
| depends | D1, D7. |
| risk | novelty of (i). |
| fallback | (ii),(iii),(iv) only; stop: none. |
| IC3 | two-state masked family. |
| numerical | OPW2 enumeration p ≤ 10 exists. |

### D13 · Theorem 1 (target consistency, T03♯) · **main (short)** · K93

| field | content |
|---|---|
| statement | R1 (s₀ fixed, p ≤ n^A), G, R, SE_λ, SE_w, BM-∞ or BM(c > c₀), fixed design: 1 − π(S₀) = O_P(√(log n/n)); HPM and MPM of π equal S₀ w.p. → 1; P(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] [cited]; large signals get PIP → 1 without beta-min. |
| guarantee | The target is right asymptotically. |
| goal | objective 3; SL Thms 1–3, S. |
| status | T01-T03: PROVED-LOCKED (wave 3; external review queued); T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T03-1.2e5: ERROR (repaired: n ≳ 2·10⁶). Fidelity: algorithm-free. |
| self-checked? | no (cross-family). |
| novelty | MODEST (Rossell 2022; Moreno–Girón–Casella 2015); LIT-VENUE "do not sell it". |
| route | as locked. |
| difficulty | S. |
| Lean | T02(i♯) tail partly. |
| depends | nothing. |
| risk | vacuous at study n; disclose. |
| fallback | cite; stop: none. |
| IC3 | fixed designs satisfying SE; LH. |
| numerical | none. |

### D14 · Proposition PIP-eq (equal-weight pooling; R vs N) · **supplement** · K49, K50, K57, K59

| field | content |
|---|---|
| statement | PIP^eq → E[PIP̂_1j|𝓒] ≠ PIP_j at fixed N; E[Ẑ̄·PIP^eq] − Z·PIP = −(1−1/R)Cov; |E[PIP̂_rj] − PIP_j| ≤ TV(delivered population, π); splitting N_e into more islands is neutral for Ẑ to first order (exact-refresh idealisation) but not for PIP^eq. |
| guarantee | Why the Ẑ-weighted PIP is primary and N_e is never split. |
| goal | M4, M7 motivation. |
| status | MA-PropP: PROVED (elementary); Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH. Fidelity: equal-weight secondary. |
| self-checked? | PropP author-only. |
| novelty | KNOWN—CITE (Vergé et al. 2015) + elementary. |
| route | elementary. | difficulty | S. | Lean | (iv) identity. |
| depends | D1. | risk | none. | fallback | drop Cor V; stop: none. | IC3 | any. | numerical | E's two-state check. |

### D15 · Proposition LIM (what runs cannot certify) · **supplement** · K79, K74, K81, K99, K100, K101, K80

| field | content |
|---|---|
| statement | (a) no diagnostic from the transcript certifies absence of an unqueried mode (changing its mass leaves the transcript unchanged); (b) a certified flip/swap local maximum can be far below the mode; (c) ESS = N throughout is compatible with genealogical collapse; (d) cross-block masked contrasts of order k ≥ 4 in a saturated cluster are unreachable at budget W·(2p)^{−k} while every diagnostic passes; (e) duplicates: PIP → 1/d, group inclusion → 1; (f) MPM may exceed K; (g) E2 fires w.p. ≈ P(χ²₃ > 3/s²) under a declared alternative. |
| guarantee | Limitations stated as theorems, not inherent-by-assertion. |
| goal | §4.4/§8.2 diagnostics; ground rule "no open questions". |
| status | MZ-E1E2 PROVED (candidate); INP I5 PROVED; CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, CEX-ties(A2): COUNTEREXAMPLE; (d),(g): proposal (author's PROOF SKETCH, unchecked); SHARE-PB COUNTEREXAMPLE related. |
| self-checked? | (d),(g) unchecked. |
| novelty | (a) Chatterjee–Diaconis 2018 Thm 2.1 kind; rest constructions. |
| route | oracle-algorithm argument; explicit constructions respecting clustering ties and the cap. |
| difficulty | S–M ((d) M). |
| Lean | moat union bound; (c) two-state. |
| depends | nothing. | risk | (d) construction must match the as-coded partition. |
| fallback | (a)–(c),(e),(f) only; stop: one attempt on (d). | IC3 | saturated cluster of size > B. | numerical | D's k = 3 brute force at p = 1,000. |

### D16 · Proposition KERNEL (N9, graph, minorisation, Dirichlet comparison) · **supplement, cited lemma + Lean** · K20, K21, K08, K09, K22, K23, K103

| field | content |
|---|---|
| statement | Each elementary move is γ_φ-reversible (cap and self-loops included); the uniformly random order is self-adjoint on L²(q_φ) (a realised order is not); draw_pi0 exact, Z̄₀ exact; tie-aware DP returns the prescribed maximiser (N3 OPEN); the symmetrised capped graph has no isolated vertex and ≤ pB edges; Q_φ(S,·) ≥ π_φ/(mM_φ) with M_φ ≤ exp{φ(d_max − E_{π₀}d)}, so ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1 − 1/(mM_φ))^k; ℰ_Q ≥ ½ℰ_{R₂}. |
| guarantee | §5.1 exactness; the only unconditional mixing statement, with its honest constant. |
| goal | §5.1; §5.4 TV (§F). |
| status | N9K: PROVED (candidate) (code-checked at 39db138); T09: PROVED-LOCKED (wave 1); N3 DP invariant: OPEN; K22, K23, K103: proposal (author's PROOF SKETCH, unchecked). Fidelity: production kernels, exact arithmetic, (H-U). |
| self-checked? | N9 consultant-only (independent line review requested, N9 §5). |
| novelty | KNOWN—CITE (Mengersen–Tweedie 1996; Liu 1996); K23 possibly folklore. |
| route | detailed balance case analysis; independence label first w.p. 1/m. Settle D's 1/(mM) vs E's 1/M. |
| difficulty | S. |
| Lean | flagship finite target: transition matrices, permutation reversal, convolution/backward sampler, max-plus DP. |
| depends | nothing. | risk | constant useless under masking (say so). |
| fallback | cite; stop: none. | IC3 | any. | numerical | N9 CHECK. |

### D17 · Proposition TARGET (propriety, invariance, reduction, odds identity, exact branch) · **supplement** · K01, K02, K03, K04, K95, K76

| field | content |
|---|---|
| statement | H_S ≻ 0 for rank-deficient X_S; Q_S ≥ yᵀy/(n+1); −(|S|/2)log(n+1) ≤ log BF(S) ≤ ν log[(2b₀+Y)/(2b₀+Y/(n+1))]; affine invariance and permutation equivariance (ties break fixed-seed equivariance); contrast reduction with IG(a₀+½, b₀s_y²); |Δ log BF| ≤ 2νb₀|1/Q₁ − 1/Q₂| when b₀ → 0; BB(1,p) identities; π(S₀) = 1/(1+A(S₀)) and A ≤ η ⇒ HPM = MPM = S₀; fixed p is eventually enumerated exactly. |
| guarantee | The target is a proper, invariant finite law with explicit envelopes; fixed p is eventually exact. |
| goal | objective 1 foundations; N17, N12. |
| status | N17: PROVED (PC1 claim 1); N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected); rest: proposal (author's PROOF SKETCH, unchecked). |
| self-checked? | yes. | novelty | routine. | route | linear algebra, Woodbury, gamma integral. | difficulty | S. |
| Lean | all finite algebra (good targets). | depends | nothing. | risk | 2νb₀ vs n·b constant (D vs E). | fallback | drop K03(b); stop: none. | IC3 | any. | numerical | none. |

### D18 · Proposition CERT (local search semantics, B&B soundness, rounding) · **supplement** · K64, K73, K05, K107, K108

| field | content |
|---|---|
| statement | Local search moves only on strict improvement, ≤ (ℓ+1) scans of ≤ p + k*(p−k*) models, `local_certified` = strict flip/swap local maximum at the scanned centre; B&B over [∅, U] with the Furnival–Wilson superset bound is exact when it completes, "unresolved" otherwise; score rounding error ≲ c·k·κ₂(H_S)·u·(ν+k); if every log mass moves ≤ ε then Z̃/Z ∈ [e^{−ε}, e^{ε}], TV ≤ tanh ε, winners with gap > 2ε unchanged. |
| guarantee | Exact semantics of every flag; certificates in exact arithmetic with a labelled numerical layer. |
| goal | §4.4/§8.2; N7, N16. |
| status | N7: L1 CORRECT WITH AMENDMENT, L2 PROVED, R PROVED with amendments; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*); N16: OPEN; T33-errbound: COUNTEREXAMPLE (engine η not a bound at large n). |
| self-checked? | K05, K107, K108 unchecked. | novelty | NEW in kind (certificates), elementary. |
| route | finite; Furnival–Wilson 1974. | difficulty | S. | Lean | all finite. | depends | nothing. | risk | η heuristic (e5). | fallback | exact-arithmetic only; stop: none. | IC3 | any. | numerical | PC2 60-case test. |

### D19 · Proposition IDENT (restricted-ESS coverage identity; TI/KL identities; R_eff) · **supplement** · K25, K104, K54, K55

| field | content |
|---|---|
| statement | ρ_full(u,v) = ρ_V(u,v)·a_u a_w/a_v², a_t = q_t(V), w = 2v−u; (log Z_φ)′ = E d, ″ = Var d; KL(π‖π₀) + KL(π₀‖π) = ∫₀¹Var_{q_φ}(d)dφ =: J; Λ ≤ √J; R_eff/R → Z²/E[Ẑ²|𝓒]; sandwich variance estimator consistent as R → ∞; √N and √R CLTs [cited]. |
| guarantee | What the certified restricted ESS says about the full bridge, and the computable Jeffreys error of the merge. |
| goal | §4.4/§8.2; §5.4 KL (§F). |
| status | proposal (author's PROOF SKETCH, unchecked) (D BR1/ST10/PI2, E T14/T11/T22); OWS-WS1: PROVED (no review) gives the exponential-family identity. |
| self-checked? | unchecked; WS1 same-family. | novelty | KNOWN (Gelman–Meng 1998; Chopin 2004); the coverage identity NEW but immediate. |
| route | F_V(t) = F(t) + log(1 − η_t). | difficulty | S. | Lean | all finite. | depends | nothing. | risk | none. | fallback | cite; stop: none. | IC3 | any. | numerical | none. |

### D20 · Proposition FIN-n (finite-n posterior-miss bound, data-averaged) · **supplement candidate** · K94

| field | content |
|---|---|
| statement (proposed) | Sampling model y = Xβ* + σ*ε, Gaussian; for q ∈ (0,1): E₀[1 − π(S₀)] ≤ B_q := Σ_{S≠S₀}E₀[R(S,S₀)^q], R the posterior odds; P₀(π(S₀) ≤ 1−ε) ≤ ((1−ε)/ε)^q B_q; with the ridge/g = n score, E₀[R^q] has an explicit envelope per (|S∖S₀|, |S₀∖S|) class under SE on S ∪ S₀ and a projected-signal gap. |
| guarantee | A non-asymptotic selection statement (replacing "→ 1"), averaged over data, not given the design. |
| goal | objective 3; SL Thms 1–2 finite form; R7 partial. |
| status | R7 draft status: OPEN (API-N200); K94: proposal (author's PROOF SKETCH, unchecked) (D TG5, E T34). |
| self-checked? | unchecked. | novelty | rates of this shape KNOWN (Narisetty–He 2014; Castillo–Schmidt-Hieber–van der Vaart 2015); constants for this target NEW. |
| route | fractional-moment bound E₀[R^q] via Gaussian quadratic-form MGFs; classwise counting with the BB(1,p) tail (T02(i♯)). Key lemma: the all-large-model tail (E's obligation). |
| difficulty | M–L. | Lean | class counting. | depends | D13 machinery. | risk | vacuous at n = 200 (disclose); Π(X) given X stays OPEN. |
| fallback | future work; stop: one HQ wave; if the all-size tail fails, drop. | IC3 | fixed design with SE on sets ≤ 2s₀ (LH). | numerical | ≤ 20 seeds at p = 8 for B_q vs exact 1 − π(S₀). |

### D21 · Proposition BLOCKS (separation ⇒ groups kept; within-block immunity) · **supplement** · K07, K14, K06

| field | content |
|---|---|
| statement | If every within-group distance is strictly below every between-group distance and groups have size ≤ B, complete linkage forms each group first and cut/packing never splits a group (so cross-block |r| ≤ max between-group |r|); every sub-model inside a block is scored at table time, so the HPM beats every block-local model and within-block masking of any order ≤ B costs nothing; study packing (2g ≤ B) is N8, OPEN. |
| guarantee | Correlated clusters of size ≤ B are handled exactly at the start. |
| goal | objective 3 under correlation; §5.3 hypothesis supply. |
| status | PART-ThmA: PROVED (SF: none; XF: VERIFIED* (A-REV9)); PART-pairing: OPEN; PART-CE2: COUNTEREXAMPLE (unequal-size header XF ERROR); K14: proposal (author's PROOF SKETCH, unchecked). |
| self-checked? | K14 unchecked. | novelty | classical (single/complete linkage recovers separated clusters). |
| route | induction on merges (Lance–Williams max). | difficulty | S. | Lean | finite dendrogram combinatorics. | depends | nothing. | risk | PART-CE2 for 2g ≤ B. | fallback | state for g_max ≤ B < 2g_min only; stop: none. | IC3 | LH with g ≤ B < 2g. | numerical | none. |

---

## §E Proposal §5.3: weight stability under weak cross-block dependence (item 4)

**Position.** A paper-1 theorem exists with genuinely weak, non-zero cross-block correlation. It is *not* the perturbation of the orthogonal case (K11, WS4): my check below shows that constant is vacuous at the natural n^{−1/2} correlation scale, exactly as O-WSTAB's own "scale of the perturbation regime" remark warns. The theorem goes through **cross-block leakage** (WS5.3), the **exact χ² identity** (WS1/WS6(b)), and the **masked obstruction** (WS7), all already PROVED (no review) in the registry on *any* partition and for *every* grid.

### Card D6 · Theorem WSTAB-C

| field | content |
|---|---|
| statement | Blocks any partition (the v3 one included); SE-blk(φ₀): λ_min(R_{C_b}) ≥ φ₀² ∀b; G, R; cross-block leakage CBL(η): max_b Λ_b ≤ ησ*²log n with Λ_b = ‖(P_{C_b} − P_{U*_b})μ_{−b}‖² (the energy other blocks' signal leaks into block b beyond its own truths), η < η_A; EBM(M_n): min_{b,j∈U*_b}|θ̃_{b,j}| ≥ [√(M_n(σ*²+2M)log n) + √Λ_b]/(φ₀√(n−1)), M_n → ∞. Then: (F) 1 − π₀(S₀) = O_P(2^B√log n·n^{−κ}) (favourable start). (S) For **every** grid 0 = φ₀ < … < φ_T = 1 and every t: χ²(q_{φ_t}‖q_{φ_{t−1}}) ≤ 1/m² − 1, m := min{π₀(S₀), q₂(S₀)}, and 1 + χ²(π‖π₀) = π(S₀)²/(π₀(S₀)q₂(S₀)) exactly; with T = 1, Var_𝓒(Ẑ_r/Z) = χ²(π‖π₀)/N. (O) Obstruction: under ORTH with |N₀| truth-free null predictors and p = n−1, χ²(π‖π₀) → ∞ for every R̄² > ½ while TV(π, π₀) → 0; conversely under masking ESS_∞ ≤ π₀(S₀)/π(S₀)² = p^{−c}n^{−c/2}e^{O_P(1)}. (N) Necessity: if π₀(S₀) ↛ 1 then infinitely often coefficients cancel or leakage is large. |
| guarantee | Weak cross-block leakage (not zero correlation) makes the start favourable and bounds every stage's importance-weight variance through one explicit quantity m; weight stability can still fail by noise-chasing in many null blocks, and must fail under masking. |
| goal | proposal §5.3 (binding), Thm 1 "possible direction" made exact; objective 1. |
| status | OWS-WS53F: PROVED-UNDER (G, R, SE-blk, EBM(M_n), CBL(η), η < η_A; composition with locked T22(iii) and W1-EXP Thm 1, since VERIFIED by W3-VEXP and A-REV2); OWS-WS53M, WS53N, WS6abc, WS6d, WS7, WS1, WS2: PROVED (SF: none; XF: none); OWS-WS6e: CONJECTURE; OWS-WS8d: OPEN; AREV9-OWSTAB: W(a)–(f) VERIFIED under H-ORTH only. Fidelity: any partition (coded blocks yes); every real φ and any grid (coded grid yes); LS0 n/a; pooling n/a; (S)'s Var clause is per island. |
| self-checked? | **yes**: WS1–WS8 are Fable-authored, no review; A-REV9 verified only the H-ORTH W(a)–(f). Route to check wave 1. |
| novelty | NEW (not assessed by any LIT report); the mean-field reading (π₀ = π with an independent noise precision per block) and the leakage dichotomy are method-specific; Frazier et al. 2023 Assumption 6(iv) is the generic χ²-type precedent (cite). |
| route | WS1(a): 1+χ²(q_v‖q_u) = q_v(S)²/(q_u(S)q_w(S)) for every S (cumulant identity); take S = S₀ and q_φ(S₀) ≥ min{q₀(S₀), q₂(S₀)} on [0,2] (WS1(e)). WS5.3(F): leakage bounds give VIS and NL_η, then locked T22(iii). Key lemma: **WS5.2 leakage formulas** (Λ_b controls NL_η) and the q₂(S₀) tilt-control lower bound (needs a tail bound on Σ_{S≠S₀}[π(S)/π(S₀)]e^{d(S)−d(S₀)}, available from T03's size/odds tail plus EBM). |
| difficulty | M (q₂(S₀) bound is the new piece; everything else is composition). |
| Lean | WS1 identity, WS6(a),(b) on a finite space: certifiable; WS5.2 leakage algebra: finite; probability cited. |
| depends | D4, D13 (T03 tail), D7 (per-stage use). |
| risk | (i) q₂(S₀) → 0 under noise-chasing (WS6(d)): then m → 0 and the bound is vacuous — the theorem says so; (ii) E[W²|𝓒] for the *hybrid* particle system at t ≥ 2 is OPEN (WS8d): only the IID-idealised product ∏(1+χ²_t/N) − 1 is PROVED; (iii) same-family only. |
| fallback | (F)+(S) with T = 1 exact variance and the per-stage χ² bound for any grid, plus (O),(N) as limitations; **stop rule**: if the q₂(S₀) tail bound fails after one HQ wave, ship (F), the exact identity, and (O); if (F)'s CBL family is found vacuous (IC3 below fails), escalate to HQ (binding goal not met by withdrawal). |
| IC3 design (exhibited) | Block-equicorrelated rows: Σ = blockdiag(Σ_g(ρ)) + ψ_n·(off-block entries), groups of size g ≤ B, within-group ρ ∈ (0,1) arbitrary, cross-block ψ_n = c₀√(log n/n) (the METHOD §10 w1 scale; non-zero at every n), s₀ truths in s₀ distinct blocks with |θ*| ≥ M_n√(log n/n)·(1+o(1)). Then Λ_b ≈ n ψ_n² g‖θ*‖² ≍ c₀² g‖θ*‖² log n ≤ ησ*² log n for c₀ small: CBL holds with η > 0; EBM holds; SE-blk holds for ρ < 1. Cross-block correlation is non-zero and above the sample noise scale when c₀√2 > √(2 log p/n)/√(log n/n), i.e. for p polynomial it is of the same order as the neighbour threshold r_n. Not H-ORTH, not an ideal grid. |
| numerical companion | the check below (20 runs) plus, for the HQ: ≤ 20 seeds on the IC3 family at n = 400, p = 12, g = 3, ρ = 0.6, ψ = 0.1, computing exact π₀(S₀), q₂(S₀), per-stage χ² of the as-coded grid and the T = 1 Var(Ẑ_r/Z). |

**Why the route is credible.** WS1 is an identity (two lines, Lean-able). WS6(b) follows from it with S = S₀. WS5.3(F) is a composition of PROVED leakage formulas with a locked theorem whose inputs were cross-family VERIFIED. The only genuinely new lemma is a lower bound on q₂(S₀), i.e. on 1/(1 + Σ_{S≠S₀}[π(S)/π(S₀)]e^{d(S)−d(S₀)}); under BO, d(S) − d(S₀) ≤ ν·Σ_{b<c}x_bx_c/(1−x̄) (WS3(c)) and under CBL the cross-block part is O(η log n), so the sum is dominated by the T03 odds tail with an extra n^{O(η)} factor; choosing η small relative to the T03 exponent closes it. A referee can follow every step; the failure modes are stated as theorems (O), (N), not hidden.

**Local check (script, 40 s).**

```python
# Seat B local check: weak non-zero cross-block correlation vs the BO-equivalent bridge.
# n=60, p=6, blocks {0,1,2},{3,4,5}, within rho=0.5, cross eps, S0={0,3}, beta=(1,0.8); exact enumeration of Omega.
# Computes chi2(pi||pi0) via WS1(a), the BO-equivalent chi2 (d replaced by d_sigma), the WS4(e) bound 4*eta_W,
# and the greedy ESS-0.9 grid length (60 halvings) for both bridges.
import numpy as np, itertools, math
from scipy.special import comb, logsumexp
def run(n,p,eps,seed,rho=0.5,beta=(1.0,0.8)):
    rng=np.random.default_rng(seed); K=min(p,n//2); blocks=[list(range(p//2)),list(range(p//2,p))]
    Sig=np.full((p,p),eps)
    for b in blocks:
        for i in b:
            for j in b: Sig[i,j]=rho if i!=j else 1.0
    X=rng.multivariate_normal(np.zeros(p),Sig,size=n); y=beta[0]*X[:,0]+beta[1]*X[:,p//2]+rng.normal(size=n)
    X=X-X.mean(0); X/=X.std(0,ddof=1); y=y-y.mean(); y/=y.std(ddof=1)
    a0=b0=0.01; nu=a0+n/2; Qbar=2*b0+y@y
    def logBF(S):
        if not S: return 0.0,0.0
        Xs=X[:,S]; G=Xs.T@Xs; H=(n+1)*G+np.eye(len(S)); z=Xs.T@y
        t=n*z@np.linalg.solve(H,z); D=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(S)))[1]
        return -0.5*D-nu*math.log(1-t/Qbar), t/Qbar
    models=[list(S) for k in range(K+1) for S in itertools.combinations(range(p),k)]
    lw=lambda k: -math.log(2)-math.log(comb(2*p-1,k,exact=True))
    lg0=[];d=[];ds=[];etas=[]
    for S in models:
        lb,xS=logBF(S); parts=[[j for j in S if j in b] for b in blocks]
        lr=[logBF(u)[0] for u in parts]; xb=[logBF(u)[1] for u in parts]
        lg0.append(lw(len(S))+sum(lr)); d.append(lb-sum(lr)); ds.append(nu*(sum(math.log(1-x) for x in xb)-math.log(1-sum(xb))))
        if len(S)>=2 and all(parts):
            R=(X[:,S].T@X[:,S])/(n-1); A=np.array([[R[i,k] if (S[i] in blocks[0])==(S[k] in blocks[0]) else 0 for k in range(len(S))] for i in range(len(S))])
            Ah=np.linalg.inv(np.linalg.cholesky(A)); M=Ah@(R-A)@Ah.T; e=np.linalg.norm(M,2); F=np.linalg.norm(M,'fro')**2; xbar=sum(xb)
            etas.append((nu*e*xbar/(1-e-xbar)+F/(4*(1-e))) if (e<1 and xbar<1-e) else math.inf)
    lg0=np.array(lg0); d=np.array(d); ds=np.array(ds); eta=max(etas)
    Lam=lambda phi,dd: logsumexp(lg0+phi*dd)-logsumexp(lg0)
    chi=lambda u,v,dd: math.exp(Lam(2*v-u,dd)-2*Lam(v,dd)+Lam(u,dd))-1
    def grid(dd):
        u=0.0;T=0
        while u<1:
            if chi(u,1.0,dd)<=1/9: return T+1
            lo,hi=u,1.0
            for _ in range(60):
                mid=(lo+hi)/2
                if chi(u,mid,dd)<=1/9: lo=mid
                else: hi=mid
            u=lo;T+=1
        return T
    return chi(0,1,d),chi(0,1,ds),4*eta,grid(d),grid(ds),float(np.max(np.abs(d-ds)))
print("eps seed chi2 chi2_BOequiv 4eta_W T T_sig max|d-d_sig|")
for eps in (0.0,0.02,0.05,0.10,0.20):
    for seed in range(4): print(eps,seed,*["%.3g"%v for v in run(60,6,eps,seed)])
```

Output (columns: ε, seed, χ²(π‖π₀), χ² of the BO-equivalent bridge, WS4(e) bound 4η_W, stage counts T, T_σ, max|d − d_σ|):

```
eps  seed  chi2   chi2_BO  4eta_W   T  T_sig  max|d-d_sig|
0.00  0   0.043   0.036    186      1   1      1.78
0.00  1   0.507   0.181     51      3   2      3.78
0.00  2   0.289   0.180    467      2   2      3.07
0.00  3   3.265   1.013    148      6   4      5.19
0.02  0   0.094   0.094    inf      1   1      8.75
0.02  1   0.333   0.560    inf      2   3      3.22
0.02  2   0.020   0.026    200      1   1      1.63
0.02  3   0.109   1.515    inf      1   4      6.95
0.05  0   0.031   0.462    inf      1   2     15.03
0.05  1   0.631   1.096    inf      3   4      4.32
0.05  2   0.177   1.104    inf      2   3     11.50
0.05  3   1.885   1.137    151      5   4      4.36
0.10  0   0.154   0.009    inf      2   1     17.34
0.10  1   1.147   3.365    inf      4   5     11.94
0.10  2   0.055   1.568   2860      1   3      9.10
0.10  3   0.021   4.797    inf      1   5     19.14
0.20  0   0.031   4.069    inf      1   5     25.35
0.20  1   1.652   4.899    inf      4   6     15.88
0.20  2   0.021   4.931    inf      1   6     23.74
0.20  3   0.161  58.385    inf      2   9     28.05
```

Reading: (1) the true χ²(π‖π₀) is O(1) and T ≤ 6 for all ε ≤ 0.2; (2) the WS4(e) transfer constant is never informative (≥ 51, mostly ∞ because x̄_S > 1 − ε_S), even at population ε = 0, since sample cross-correlations are ≈ n^{−1/2} = 0.13; (3) the BO-equivalent bridge is often *worse* than the true one, so "weak correlation = small perturbation of BO" is the wrong picture; cross-correlation can offset the σ²-sharing term. Hence D6 is stated through leakage and the exact identity, and K11/WS4 is a remark. (This is a check of a route, not evidence for the theorem; ≤ 20 runs.)

---

## §F Proposal §5.4: approximation error (item 5)

**What "approximation error" refers to here.** The method corrects exactly (q₁ = π; D1). The approximation is (i) π₀ itself, the merge, whose distance from π is quantified by D4(c),(d), D5 and D6(O); and (ii) the finite-budget Monte Carlo error of the output (D2, D3, D12). TV/KL/coverage must be read in that sense.

| metric | card or reason | what ships against the goal |
|---|---|---|
| PIP error | D2 (K51, K52), D3(b) (K43) | Islandwise ≤ 2δ₁ in W-weighted mean; finite-R Chebyshev bound; deterministic restricted bracket. |
| joint-PIP error | D2(d) with h_A, conditional on N1 (K46) | Same bounds; plain averages, declared pairs ≤ 2pB. |
| TV error | **Card (supplement):** (a) |E[PIP̂_rj] − PIP_j| ≤ TV(law of delivered population, π) (MZ-P1 PROVED); (b) TV(law of one particle after L terminal rounds, π) ≤ (1 − 1/(mM₁))^L (K103, textbook); (c) TV(π̃, π) ≤ tanh ε under log-mass perturbation ε (K108). **Not meaningful as a rate:** M₁ = exp{d_max − E_{π₀}d} is exponential under masking, and the delivered population's law has no TV theorem beyond (b) (DELIV-POP OPEN). State (a)–(c) as what is provable; do not promise a TV rate. | The merge's TV error from below: TV(π, π₀) ≥ π(S₀) − π₀(S₀) → 1 under masking (WS7); TV → 0 while χ² → ∞ in the noise-chasing regime (WS6(d)): both as theorems in D6. |
| KL error | **Identities and lower bounds only** (K104 cited; K105 Lemma KL; WS6(c) upper bounds KL(π‖π₀) ≤ log(π(S₀)/π₀(S₀)) + (π(S₀)/θ)(1/q_{1+θ}(S₀) − 1)). A KL "error of the final estimate" is not a meaningful quantity for a finite-particle estimator of expectations (the estimator is not a law); the meaningful object is KL(π‖π₀), which D5/D6 bound two-sided. | Lemma KL + the exp(KL) one-shot cost (D5) and the WS6(c) upper bound (D6) ship; the Jeffreys J = ∫Var_φ(d)dφ is reportable (D19). |
| credible-interval coverage | **Not provable/meaningful for this method as posed:** outputs are PIPs, MPM/HPM and declared bounded summaries, not credible intervals for β; a Monte-Carlo credible interval for μ̂(h) would need a CLT-based interval at R = 4 (K54: no coverage at R = 4, E). What *is* proved is **output-event coverage of certificates**: P(𝒪 ∩ {card false}) ≤ 0.05 (D3(e)), two-sided deterministic brackets when S₀ ∈ 𝒯 (D3(b)), and the Markov lower bound. | D3; plus, if HQ wants intervals for continuous functionals, h̄(S) = E[h|S,X,y] inside D2 gives point estimates with the same error bounds, not coverage. **Binding-goal question → §I Q1.** |

Nothing in this table drops a binding goal silently: PIP/joint-PIP are delivered; TV/KL are delivered as the merge's divergences and as what-is-provable for the output; coverage is re-interpreted and escalated.

---

## §G Fidelity (item 8)

| registry ID | about v3.1 as shipped? (LS0 / coded grid / Ẑ-weighted pooling) | gap | gap lemma to prove |
|---|---|---|---|
| T12, T31(i), Prop2(a,b,d,e) | LS0 n/a (reads no uniforms; islands unchanged, METHOD §2 #8); coded grid yes (any frozen 𝓒, INP N5(a)); pooling yes (per island) | XF GAP on output-Markov wording (A-REV4); R′ > 4 streams | Lemma: identities hold per island for streams 10..9+R′ given IND-T′ (N14(c), code audit). |
| N1 (PROOF SKETCH) | LS0 n/a; coded grid yes; pooling yes (μ̂_w) | the general-h prefix lemma | "E[Ẑ_r H_r(h)|𝓒] = Zπ(h) at the M9 accumulation point, random RB position" (D1). |
| N9K / T09 | production kernels at 39db138 (N9 REPORT §1); exact arithmetic, (H-U) | no registry row; fp departures 2⁻⁵³ (N9 §4) | none mathematical; registrar to open the row; optional remark bounding fp effects. |
| ADRAFT-ThmA | frozen run; LS0 n/a; grid yes; pooling: per island | Astra-only check | cite Del Moral 2006 instead (IC4). |
| MA-PropP, PC1c3 | pooling: Ẑ-weighted yes (primary, M4); grid yes; LS0 n/a | PropP author-only; PC1c3 takes N1 as premise | none beyond N1. |
| FMP-M1, FMP-M2 | one island, any frozen grid: yes; LS0 n/a; pooling n/a | none | — |
| MZ-P3, PC1c5, N13 | LS0 **yes** (𝒯_new = top_c(𝒯_old ∪ 𝒮_added), R3_B R3-1); grid n/a; pooling n/a | PC2 code facts (inheritance merge) | none. |
| PC1c2 / N6 | GUARD-W premise (i): **unknown** (code audit N2(e)) | audit | none mathematical. |
| N17 | algorithm-free | — | — |
| OPW2-ThmA/B | frozen calibration, any invariant kernels: grid yes; LS0 n/a; per island | exact-refresh clause is an idealisation (OPW2-cex) | none for ThmA; do not use a_t = χ²_t. |
| MZ-E1E2, FMP-Na | frozen; any grid, kernel, N: yes | E1/E2 candidate | — |
| T26-ThmA | favourable; frozen run; (P1) hypothesis | iid draws? EX-S only | remark. |
| T22(i)(ii)(iv), T27(i), DIL-E, Thm3/4-EXP, Thm5-LH | production start: yes; LS0/grid/pooling n/a | T27(i) conditional (H2, H3) | — |
| OWS-WS1–WS8, FD-W1 | any partition (incl. coded blocks); every real φ and any grid: yes; LS0/pooling n/a; WS8(b) IID idealisation only | same-family only; H-ORTH only in WS6(d) and A-REV9's W(a)–(f) | WS8(d): PW2 for the hybrid system (OPEN) — not needed for D6 as stated. |
| SEP-A/B, SEP-E | iid draws from π₀ plus tables; no LS0 (as stated) | — | none (statement is about one-shot schemes). |
| STG-G, T26BUD-G, STG-L0/L1/L | as-coded rule: yes (pilot = grid ESS 0.90 hypothesis) | author-only | — |
| STG-M | ideal two-state exact-frontier grid: **no** (coded grid) | Conjecture P | "as-coded masked T_n = log₂A₀ + O_P(1)" (OPEN, deferred; stated as hypothesis). |
| STG-F, STG-Wp | ideal; (LL) conflict C22 | — | supplement only. |
| Thm4-C1, T38-(0), N200 | yes (any run; LS0 enlarges 𝒮, nested) | N200 author-only | — |
| TheoremA, LS-score, LemmaM, Prop1-TD | LS0 yes ("v3 + LS0", fidelity GREEN Astra r2); scans completed | e4 centre invariant (N3 OPEN); ℓ ≥ Φ(S°)−1 (N11) | "tie-aware DP returns the prescribed maximiser" (N3). |
| T38-b1-LH, Thm-b1 | LS0 yes; any frozen grid; pooling n/a | bridge to code N2(c) (merged-LS0 replay) | none mathematical. |
| B2E-B2LH, STAB | **no LS0** (v3 as run); any frozen grid | variant (corollary) | — |
| T03♯, T01–T03, Prop1-T07 | algorithm-free | — | — |
| MA-PropD, T32(i), Cost-T38 | counting; LS0 and extra-search terms added (INP row 12); island level | displayed rate GAP | recount only. |
| LemmaRO, CEX-guard | serial v3 guard audited; v3.1 worker/merge/LS0 **unknown** (GUARD-W) | audit | none mathematical. |
| IND-T, Lemma-STREAM | streams 10–13 yes; 10..9+R′ **unknown** | audit | restate IND-T over the extended map (one line). |
| OCERT-LemmaM, C4 | scored set: yes | C1 as quantified ERROR (use R1) | — |
| C1new (Thm SL numerics) | p = 16, g = 1, slides family: **not** LH | re-run | numerical companion on LH (D9). |
| PART-ThmA | clustering rule as coded; SIZE g_max ≤ B < 2g_min; LH-iid | study g = 5 (N8 OPEN) | PART-pairing (OPEN; disclosed). |

---

## §H My list (ranked, main / supplement)

| rank | K-ID(s) | name | main / supplement | one-line reason |
|---|---|---|---|---|
| 1 | K35, K46, K32, K86, K36, K50 (+K20, K21, K08 cited) | Proposition V+ / general-h identity (N1) | main | Binding §5.1, §5.2, §13.1 crux; everything else conditions on it. |
| 2 | K51, K52, K48 | Theorem H | main | Objective 1 and §5.4 PIP/joint-PIP; the only regime-free accuracy theorem. |
| 3 | K102 (restated), K10, K25, K27 | Theorem WSTAB-C | main | Binding §5.3 with genuinely weak non-zero cross-block correlation; obstruction included. |
| 4 | K15, K16, K17, K18, K10 | Theorem 2 (start, masking, dilution) | main | Strongest novelty; input A₀ to depth; SL Thm 4 exceeded. |
| 5 | K72, K68, K69, K70, K65, K63, K62 | Theorem HPM (composition; LS0 route on LH) | main | Objective 3 for the shipped method; Lean cores exist. |
| 6 | K42, K43, K45, K36, K78, K44 | Theorem Z𝒯 / CARD | main | Two-sided reported-quantity accuracy and 95% output-event certificates. |
| 7 | K26, K27, K30, K28 | Theorem STG | main | Depth as a functional of d; the "costs depth" half. |
| 8 | K106, K105, K19 | Theorem SEP + Lemma KL | main | Why one-shot fails; exp(KL) scale; SL contrast. |
| 9 | K97 | Theorem SL | main | Ground rule 2's "works under correlation, unlike SL" as a theorem. |
| 10 | K96 | Theorem CD (assembly) | main | The thesis sentence, island-level scope. |
| 11 | K93 | Theorem 1 (T03♯) | main (short) | Target consistency; MODEST, disclosed. |
| 12 | K39, K40, K38, K37, K41, K53 | Theorem Z (variance, masked tail) | supplement | Honest evidence-error mechanisms; novelty of (i) to check. |
| 13 | K87, K88, K89, K90, K06, K64 | Theorem D (work/depth/width) | supplement | Objective 2 accounting at the island level; SL §6 comparison. |
| 14 | K20, K21, K08, K09, K22, K23, K103 | Proposition KERNEL (N9; minorisation) | supplement + Lean | Cited lemma with the method's kernels; flagship Lean. |
| 15 | K79, K74, K81, K99, K100, K101, K80 | Proposition LIM | supplement | Limitations as theorems (no open questions). |
| 16 | K01, K02, K03, K04, K95, K76 | Proposition TARGET | supplement | Propriety, invariance, envelopes; Lean-able. |
| 17 | K64, K73, K05, K107, K108 | Proposition CERT | supplement | Exact semantics of flags; B&B soundness; rounding. |
| 18 | K25, K104, K54, K55 | Proposition IDENT | supplement | What restricted ESS certifies; KL/TI identities; R_eff. |
| 19 | K49, K50, K57, K59 | Proposition PIP-eq | supplement | Why Ẑ-weighted is primary; R vs N halves. |
| 20 | K07, K14, K06 | Proposition BLOCKS | supplement | Separated groups kept; within-block masking free. |

Not ranked but supplement candidate: K94 (D20, finite-n E₀ bound; one HQ wave, else future work). Future work with reasons: K71 (LH-iid, Λ(a)/Tr(c) GAP), K31 (Conjecture P), K58 (DELIV-POP), K24 (mixing route blocked), K75, K92, K13, N12 (e^{Cn^α}), R7 (Π(X) given X), two-sided masked Ẑ (V11). Dropped: K98, K66, K67, K12, K34, K91.

---

## §I Questions for HQ

1. **§5.4 "credible-interval coverage" (binding goal).** My reading (§F) is that for this method the deliverable is output-event coverage of certificates (D3(e)) plus deterministic brackets, and that credible intervals for continuous functionals are outside paper 1 (point estimates via h̄(S) only). If HQ reads the goal as requiring a coverage theorem for intervals, that is a scope decision (new estimator and theorem), not a theorem obligation the meeting can place: please rule.
2. **Growth of R′ in Theorem H(f).** The n → ∞ clause needs R_n ≥ C·E[W²|𝓒_n]; the meeting may set R′ = R′(n, p) (ground rule 5), but E[W²|𝓒_n] has no upper bound (N4(iii) OPEN), so no explicit rate can be written. I propose stating R_n as a hypothesis with the Cauchy–Schwarz lower bound disclosed. Confirm this is acceptable rather than a growth-rate edit.
3. **Run-card additions (reporting only):** the cross-block leakage proxy (max cross-block |r| after blocks, D's D2) and the Jeffreys estimate Ĵ (D19). POST HOC, no law change. Confirm these are reporting additions the meeting may assume, not method changes.
4. **N9 as the V5 citation.** Paper 1 would cite N9-KERNEL (PROVED (candidate), consultant-checked) for §5.1; N9 §5 requests an independent line review. Confirm that review is scheduled before the per-theorem HQs, and that the registrar opens the registry row (index §5.B B2).