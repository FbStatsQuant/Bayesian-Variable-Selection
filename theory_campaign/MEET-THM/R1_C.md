# Round 1, Seat C (gpt-6-astra, Codex, high)

Verbatim final message, extracted by the chair from `~/.codex/sessions/2026/11/03/rollout-2026-11-03T20-07-25-01a1a44f-a4aa-7d61-8d02-425fff3f695e.jsonl` (completed 2026-11-04 02:21 UTC). Everything in it is the seat's position; its own arguments are unchecked.

---

| MEET-THM Round 1 | Seat C |
|---|---|
| Recommendation | Fifteen merged packages: seven main-text results and eight supplement propositions/theorems. Published machinery remains cited lemmas. Acceptance of new statements is conditional on check wave 1; no status is upgraded here. |
| Scope | Amended v3.1, exact arithmetic and independent ideal uniforms unless stated otherwise. Calibration is frozen before final randomness. Actual-output guarantees are joint with output, never conditioned on completion. Island-level depth only. |
| Work performed | Fetched origin; read the brief, dossier, candidate diff, method amendments, registry/index, reviews, proposals and supporting sources. No repository edits, commits, pushes, delegated work or numerical experiments. |
| Package convention | Several K-IDs may become clauses or lemmas of one merged candidate. Each accepted package has one card below; K102’s card is §E and K103’s cards are §F. |
| Source notation | D: and E: denote Round 0 item IDs. N denotes a method obligation. Draft labels retain their original meanings. “Cited lemma” includes an explicitly attributed inherited project lemma; this does not convert an unchecked proposal into an established result. |

| Reference alias | Exact source |
|---|---|
| IDX | `origin/theory/MEET-THM-REG:theory_campaign/MEET-THM/evidence/REGISTRY_INDEX.md` |
| REG | `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/REGISTRY_v2.md` |
| M | `origin/theory/MEET-v31:theory_campaign/MEET-v31/METHOD_v3.1_FINAL.md` |
| INP | `origin/theory/MEET-v31:theory_campaign/MEET-v31/THEOREM_REVISION_INPUTS.md` |
| FIX | `origin/theory/W6-FIXREV2:theory_campaign/W6-FIXREV2/STATEMENTS.md` |
| N9R | `origin/theory/N9-KERNEL:theory_campaign/N9-KERNEL/REPORT.md` |
| T38 | `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/T38_STATEMENT.md` |
| Status convention | An inherited author status and its adverse review verdict are both retained. “PROOF SKETCH” on a package describes the new assembly or extension, not its already-checked ingredients. |

| Shared notation/hypotheses | Definition |
|---|---|
| A: computational hypotheses | Admissible standardized data; fixed v3.1 target and partition; exact scores/arithmetic; independent uniforms; exact start sampler; multinomial resampling; actual invariant move rounds; successful frozen calibration \(\mathcal C\); declared \(R\), independent final islands. |
| Output convention | \(\mathcal O\): actual output exists. Mathematical final-run statements first concern the potential uninterrupted run following successful calibration. GUARD-W must identify actual statistical outputs with that run on \(\mathcal O\). |
| Posterior objects | \(\Omega=\{S:|S|\le K\}\), \(\pi(S)\propto\varpi(S)m(S)\), \(d(S)=\log BF(S)-\sum_b\log r_b(S_b)\), \(D=\max d-\min d\), \(W_r=\widehat Z_r/Z\), \(M_2=E(W_r^2\mid\mathcal C)\). |
| Summary objects | \(0\le h\le1\), fixed before final randomness and measurable in the full frozen calibration information. \(H_r(h)\) is the prescribed measured-endpoint average; marginal PIPs use their prescribed Gibbs conditional records. |
| Gaussian model G | Raw response \(y^r=\alpha1+X^r\beta+\epsilon\), \(\epsilon\sim N(0,\sigma^2I)\), fixed design, \(\sigma^2>0\). Standardization is applied afterwards; standardized errors are not assumed conditionally Gaussian. |
| Explicit LH family | Groups of nine, within-group correlation \(0.4\); two disjoint hub links of correlation \(0.2\); all other cross-group correlations zero. Linked coefficients are \((1,-0.2)\); remaining coefficients zero. Take \(p=9\lfloor n^{1/3}/9\rfloor\), eventually at least 36, and centered \(X'X=(n-1)\Sigma\). |
| LH non-vacuity | \(\lambda_{\min}(\Sigma)\ge0.6-0.2=0.4\); centered realization exists for \(p\le n-1\). Eventually \(B=16\), so \(9\le B<18\), and complete linkage recovers the groups. The two masked hubs have zero marginal population covariance with the response. |
| Numerical companions | None run by this seat. Previously filed numerical checks retain their original provenance and seed counts; they are not new verification. |

| §A1 — Proposal coverage | Deliverable or explicit gap |
|---|---|
| §5.1 exact correction | K08/K20/K21 [V1; N9; D:ST1,KN1–2; E:T06,T09], cited through T09 and N9R. K46 [A1; N1] supplies the measured-summary interface. |
| §5.2 SMC consistency | K47/K48 [V1,V3; D:PI1–2; E:T18,T21], cited SMC/SLLN results, with K46 [N1] verifying the actual records. Fixed data and a fixed successful calibration record are explicit. |
| §5.3 weak-dependence weight stability | K102 [S4; D:ST2,ST4; E:T12,T19], with K10/K11/K53, supplies a nonzero-correlation, shared-variance-aware bound valid on every successful coded grid; §E. |
| §5.4 PIPs | K46/K51/K52 [A1; N1,N4] give finite-\(R\) bounds for primary evidence-weighted PIPs. K43 [A3] separately controls restricted-store PIPs. |
| §5.4 joint PIPs | K46/K52 [N1,N4; E:T17,T19] apply to predeclared pair indicators and other bounded functions. Joint records were not retained for the existing 2,400-fit study. |
| §5.4 TV | K103 [D:KN4; E:T10; N10], extended in §F: distinguish terminal-law TV, realized empirical TV, and TV after a predeclared coarsening. |
| §5.4 KL | K103/K104 [E:T10–11] in §F: finite bounds for terminal-law KL; forward empirical KL; reverse empirical KL can be infinite because of missing support. K105 [S2] concerns start error, not final approximation error. |
| §5.4 credible-interval coverage | K103 [§F extension] transfers simultaneous TV control to posterior content of model-size intervals or other sets. Frequentist coefficient-interval coverage is not established; binding interpretation requires §I disposition. |
| §13.1 posterior expectations | K46/K52 [N1,N4] establish consistency for bounded model-space functionals; bounded analytically integrated conditional functionals can be supplied as \(h(S)\). Unbounded functionals need additional integrability, not a blanket extension. |
| §4.4 / §8.2 diagnostics | K25 [D:BR1; E:T14] quantifies restricted/full ESS discrepancy. K43/K44 [A3; N17] provide positive mass/error certificates. K79 [A2; E:T39] gives the scoped unseen-mode warning. No universal flag-power assertion. |

| §A2 — Song–Liang item | Counterpart or reason |
|---|---|
| Theorem 1 | K93 [R1; E:T35–36] establishes selection concentration for our target, not their Hellinger contraction theorem. Approximate sparsity and predictive-density contraction remain future work. Do not mark this “exceeded.” |
| Theorem 2 | Same distinction: K93 [R1] handles fixed sparse support under its own design/prior hypotheses. Their predictor-tail assumption and prior cannot simply be imported. |
| Theorem 3 | K93 [R1; T03♯(iv)] supplies large-signal PIP inclusion without full beta-min. Estimated PIPs additionally require K46/K52 [N1,N4]. |
| Theorem 4 | Misspecified-subset concentration is a cited comparison, not a theorem of our algorithm. K18/K17 [S1] quantify a specific block-start distortion; they do not replace general KL-projection theory. |
| Corollary 1 | No exponential-\(p\) analogue established. K93 [R1] is polynomial-\(p\), under its named hypotheses. Exponential-\(p\) theory is an obligation deferred for lack of a proved tail route, not an impossibility. |
| Corollary 2 | Their sure screening of nonzero projection coordinates does not prove exclusion of zero projection coordinates. K97 [C1] therefore needs a separate null-exclusion/FDR argument and is deferred. |
| Supplementary Theorem S | K93 [R1] covers exact-posterior HPM consistency; K69/K72 [R5,R4] address the reported HPM. The supplied main paper identifies Theorem S as MAP consistency; its supplementary hypotheses were not independently verified here. |
| §6 complexity | K87/K88 [D1; N15] give actual island-level work/depth. K90 [D1(d)] becomes comparison bookkeeping only: Song–Liang’s assumed iteration scaling is not an accuracy-matched lower bound for our comparator. |

| §A3 — THM-INV §1 row | Empty/partial cells and disposition |
|---|---|
| 1 Target | V: K01/K03 [D:TG1–2]. A: K93 [R1]; finite-\(n\) upper bounds K94 [R7] deferred. C: scoring costs enter K87 [D1]. F: K60/K100 [R2; E:T37] cited qualifications. Growing support and coefficient contraction remain future obligations. |
| 2 Exact branch | V/A/C/F: K76 within K01 [E:T04; N12]. Enumeration is exact in real arithmetic; eventual fixed-\(p\) dispatch is included. Floating-point certification is not inferred from the current flag. |
| 3 Partition | V/A: K07 [D:ST5; N8] proves preservation under strict separation, not arbitrary group equality. C: K06 [D:ST6]. F: retain PART-CE2. Study-group pairing, overlapping/random partitions remain future work. |
| 4 Start | V: K08 [N9]. A/F: K18/K17 [S1], K106 [S2]. C: K06/K09 [D:ST6; E:T07]. Adaptive random-design quality and backfit starts remain outside the accepted theorem package. |
| 5 Bridge/grid | V: K32/K35 [V1]. A: K102 [S4]. C: K25/K27/K33 [D:BR1–6], plus K30 [D2(c)] explicitly idealized. Coded masked-stage asymptotics K31 remain OPEN and deferred. |
| 6 Moves | V: K20/K21 [N9]. A: K103 [N10] gives a valid, possibly tiny minorization. C: K87/K88 [D1]. F: cite the general-LH-locking refutation. Polynomial mixing K24 is deferred; sparse eigenvalues alone do not discharge it. |
| 7 Calibration | V: K32/K86 [N5,N14]. A: K102 bounds weights independently of calibration quality on successful grids. C: K33/K87 [N15]. F: K25/K79 identify restricted-ESS blind spots. K31’s convergence, discovery and failure probabilities remain deferred obligations. |
| 8 Islands | V/A: K46/K52 [N1,N4]. C: K87/K88 [N15]. F: K49/K50/K85 [V3] cited. Correlation dependence enters K102. Optimal fixed-work \(R:N\) allocation K59 remains deferred. |
| 9 Evidence | V: K35/K36 [V1], cited. A: K102/K52 [S4,N4] give two-sided control on their design class. C: K87. F: K42/K44/K77 [A3,N17,V4]. Strong masked-family precision and validated production arithmetic remain unproved. |
| 10 PIPs/MPM | V/A: K46/K51/K52/K62 [A1,N1,N4; E:T28]. C: include summary accumulation in K87. F: K100/K101 [E:T37,T28]. Model-size posterior-content coverage: K103. General frequentist coverage remains outside the proved scope. |
| 11 HPM | V/A: K69/K72 [R5,R4], with K63/K45 [V2,N13]. C: K87. F: retain statistical/discovery/delivery decomposition. K82/K94 and study-generator discovery remain future work, not inherent impossibilities. |
| 12 Local search | V/A: K65 within K69 [R3,R5]. C: K64 within K87 [N11,N15], corrected \(k_*=\min(K,\lfloor p/2\rfloor)\). F: K74 cited; positive global conclusions require additional hypotheses. Integrated LS0 remains an audit gate. |
| 13 Flags | V: flags describe their predicates, not truth. A: K43/K44 provide certificates, not general flag power. C: K87 includes declared certificate budgets. F: K79/K81 cited. K80’s positive-power formulas are deferred. |
| 14 Resources/numerics | V/F: K77/K78 [V4,N6]. C: K87/K88. A: K107 [N16] remains OPEN; K108 is only a conditional perturbation lemma. No delivery-rate theorem K82. Fixed allocation excludes unrestricted growth by definition. |

| §B — Entry | K-ID(s) | Decision | Corrected statement/reason | Deciding IC |
|---|---|---|---|---|
| V1 | K08,K20,K21,K32,K35–36,K46–48,K50 [V1] | Split | Cite exact-start/kernel/SMC results; retain actual measured-record extension in K46. No completion-conditioned unbiasedness. | IC1,4 |
| V2 | K63,K83,K84,K86 [V2; N2,N14] | Demote to cited lemmas | Execution/merge propositions support K87. Stacking preserves the baseline search only with the extra search retained. Audit gaps remain explicit. | IC1,4,5 |
| V3 | K48–52,K85 [V3; N4,N14] | Merge with K46 | Primary pooling is evidence-weighted. SLLN and equal-pool bias are cited; finite-\(R\) accuracy is retained. | IC1,4 |
| V4 | K77,K78 [V4; N6] | Keep, supplement | State potential-run coupling and joint-output coverage; audit GUARD-W separately. | IC1,5,7 |
| A1 | K46,K48,K51,K52 [A1; N1,N4] | Keep, main | General bounded summaries, actual marginal RB records, finite-\(R\) error around \(\pi(h)\), and separate statistical-error transfer. | IC1–7 |
| A2 | K35–42,K53,K79 [A2] | Split | Classical evidence facts cited; K102 carries design-based stability; K43 carries certificates. Masked downward-failure statements retain their event qualifications. | IC1,3,4 |
| A3 | K42,K43 [A3] | Merge with K44,K45,K73 | Stored-mass and residual-envelope certificate theorem; no assumption that the store automatically retains every scored model. | IC1,2,5 |
| A4 | K57,K58 [A4] | Defer | Equal-weight secondary estimator; unrestricted locking false, DELIV-POP OPEN. Keep the elementary TV comparison as a cited lemma. | IC1–3 |
| D1 | K06,K64,K87–90 [D1] | Split | Main K87/K88: island-level complexity. Counting/merge facts are lemmas; particle-parallel and same-order Song–Liang assertions removed. | IC1,4 |
| D2 | K26,K28–31 [D2] | Split | Coded-grid geometry joins K25; K30 retained as ideal-grid supplement. Fine-grid literature cited; K29/K31 deferred. | IC1–4 |
| D3 | K96 [D3] | Drop as theorem | Replace by a carefully scoped synthesis paragraph. No independent result; no M3 dependency and no finite-budget normalized exactness slogan. | IC1,4 |
| D4 | K39,K59 [D4] | Defer | Exact \(1/R\) evidence variance is a lemma. Fixed-total-work trade-offs require uniform remainders and actual kernels. | IC1,2,4 |
| S1 | K15–18 [S1] | Split | Main K18/K17 with deterministic K15 support. Favourable K16 stays an inherited conditional lemma; never combine favourable and masked assumptions on one sequence. | IC1,3 |
| S2 | K19,K105,K106 [S2] | Keep, main | LH discovery and one-shot importance limitations, with the exact estimand named. KL lower bound is a supporting lemma. | IC1–7 |
| S3 | K98 [S3] | Drop | SHARE-M(b), FD-NM have ERROR verdicts. No unrepaired naive-merge claim. | IC1,2 |
| S4 | K102 [S4] | Keep, main, replace statement | Nonzero cross-block perturbation plus shared-variance energy control; actual-grid moment bound, §E. | IC1–7 |
| C1 | K97 [C1] | Defer | Random partition isolation is insufficient to prove the actual Song–Liang FDR procedure drops the hub. Do not identify our \(\pi_0\) with their merged output. | IC1,2 |
| R1 | K93 [R1] | Keep, supplement | T03♯ for the exact shipped prior, all fixed-support/eigenvalue assumptions retained. MODEST novelty; no informative \(n=200\) claim. | IC1,3,4 |
| R2 | K60 [R2] | Demote to cited lemma | Bayes actions, size-prior cancellation, and corrected strict same-size competitor statement. | IC4 |
| R3 | K65 [R3] | Merge with K69 | Retain capped lattice, tie-aware progress hypothesis and nonnegative LS0 move count. | IC1,3,6 |
| R4 | K72,K78 [R4] | Merge with K69/K77 | Exact statistical/discovery/delivery decomposition; no unconditional recovery without delivery. | IC1,4 |
| R5 | K19,K68–72,K87 [R5] | Split | Main LS0 exact-Gram route; favourable discovery lemma; no-LS0 STAB-LH only as attributed variant. LH-iid and its repaired side clauses deferred. | IC1–3 |
| R6 | K82 [R6] | Defer | Status NONE. Delivery is an unproved property, not an inherent impossibility except under a fixed insufficient allocation. | IC2 |
| R7 | K94 [R7] | Defer | Fractional-odds algebra is a lemma; no explicit design-uniform finite-\(n\) bound is supplied by naming its unknown expectations. | IC2,3 |

| §C — K-ID [source] | Placement | Reason |
|---|---|---|
| K01 [D:TG1; E:T02] | Supplement, target package | Propriety and envelopes for the actual ridge/IG target, including deficient rank. |
| K02 [D:TG1,NG9; E:T01; N12] | Supplement, merge K01 | Target invariance only. General algorithmic permutation equivariance is not assured when index-based partition ties change. |
| K03 [D:TG2; E:T02] | Supplement, merge K01 | Retain contrast-regression reduction and exact \(2\nu b_0\) perturbation constant. |
| K04 [E:T03] | Supplement, merge K01 | Prior normalization/tail bookkeeping supports the actual target. |
| K05 [D:TG3] | Supplement, merge K01 | Deterministic score envelope; no new search algorithm. |
| K06 [D:ST6; E:T05] | Supplement, merge K07 | Block-count/table-work counting with next-fit packing. |
| K07 [D:ST5; E:T05; N8] | Supplement | Strict separation gives preservation; equality requires a packing-size condition. |
| K08 [D:ST1; E:T06; N9] | Cited lemma | T09/N9R already cover exact sampling and normalization. |
| K09 [D:ST1; E:T07; N3] | Supplement | Prove the already-adopted tie-DP invariant; implementation fidelity remains a gate. |
| K10 [D:ST2; E:T12] | Main, merge K102 | Shared variance creates discrepancy even at zero cross-block correlation. |
| K11 [D:ST4; E:T12] | Main, merge K102 | Relative matrix perturbation supplies the missing genuinely correlated extension. |
| K12 [D:ST3] | Future work | Useful quadrature oracle; not a property of the shipped correction algorithm. |
| K13 [D:ST8] | Future work | Requires a new start-mode theorem; orthogonal blocks alone do not establish the claimed omission-only behaviour. |
| K14 [D:ST7,HP5; E:T38] | Cited lemma | Every block-local subset is scored. Drop landscape-based global-recovery addendum. |
| K16 [S1(b)] | Cited lemma | Preserve T22(iii)’s conditional status; no new favourable-family theorem proposed. |
| K22 [D:KN6; E:T08] | Supplement, merge K07 | Keep deterministic symmetric-graph/edge-count facts; omit unproved spurious-edge asymptotics. |
| K23 [D:KN3] | Future work | Random-order spectral comparison needs a valid operator proof and novelty check. |
| K24 [D:KN5; N10] | Future work | Transfer from another prior and the proposed landscape route are unproved. |
| K25 [D:BR1; E:T14] | Supplement | Exact restricted/full ESS correction exposes the actual calibration information gap. |
| K27 [D:BR2–3; E:T13] | Supplement, merge K25 | Range-based existence/bisection bound; retain pilot endpoints and resolution qualification. |
| K28 [D2(d); D:BR3] | Cited lemma | Thermodynamic-length limit is known; not a production-threshold guarantee. |
| K29 [D2(b)] | Future work | STG-Wp has an unresolved layer-law dependency; do not reuse the refuted unrestricted \(O(1)\) claim. |
| K31 [D2; N5] | Future work | Calibration convergence, candidate coverage and coded masked-stage laws remain obligations. |
| K33 [D:BR5–6,CL1,CL4; E:T13; N15] | Supplement, merge K25 | Finite termination and successful-grid properties; no claim of probabilistic convergence. |
| K34 [D:BR7] | Future work | TI reporting is not in the fixed method; numerical integration would add a distinct approximation. |
| K37 [D:EV5; E:T23] | Cited lemma | Independence-plus-Markov and bounded-variable concentration; no new reporting field proposed. |
| K39 [A2,D4; D:EV2; E:T20] | Cited lemma | Attribute OPW2 results; classical second-moment expansion is not a new main theorem. Never substitute perfect refresh for the actual kernel. |
| K40 [A2; D:NG1; E:T38] | Cited lemma | Retain FMP-M2 and corrected finite-index event statements, not “only fails downward.” |
| K41 [A2(v)] | Cited lemma | T26-ThmA with every hypothesis retained; no upgraded assembled consistency theorem. |
| K44 [D:TG1; E:T24; N17] | Main, merge K43 | Analytic/residual upper bounds complement stored-mass lower bounds. |
| K45 [N13] | Main, merge K43 | Retention follows from scored truth plus posterior mass greater than one half. |
| K52 [D:PI2; E:T19,T21; N4] | Main, merge K46 | PC1c3 supplies a checked finite-\(R\) inequality, conditional on N1. |
| K53 [D:EV3; E:T19–20; N4] | Main, narrowed into K102 | Keep the range-based actual-grid moment bound. Defer uniform \(O(T/N)\) semigroup stability. |
| K54 [D:PI2; E:T22; N4] | Cited lemma | Kish limit and ratio CLT are standard; four islands do not establish interval coverage. |
| K55 [D:EV4,PI1; E:T18,T21] | Cited lemma | Fixed-calibration SMC and ratio CLTs; unconditional calibration mixtures need separate wording. |
| K56 [D:PI3; E:T17] | Cited lemma | One-record Rao–Blackwell variance reduction only; no universal variance ordering for the full correlated ratio estimator. |
| K61 [D:PI4] | Cited lemma | Posterior expected FDP identity, using exact PIPs; not frequentist FDR. |
| K62 [E:T28,T44] | Main, lemma in K46 | Uniform PIP error below the half-threshold margin transfers the MPM decision. |
| K64 [D:HP2; E:T26; N7,N11] | Cited lemma | Correct local scan count and certificate semantics support K87/K43. |
| K66 [D:HP3] | Drop | Proposed sparse-eigenvalue/beta-min landscape package does not address C3-PGD, VPGD-PropG or CEX-localmax(A2). |
| K67 [D:HP4] | Drop | Its proof depends on K66’s unrepaired landscape assertion. K69 is the narrower verified replacement. |
| K70 [R5(b2-LH)] | Cited lemma | Named no-LS0/STAB-LH variant only; no general LH locking inference. |
| K71 [R5(b1-LH-iid)] | Future work | Preserve XF ERROR/GAP on the recorded side clause and remaining random-design proof gaps. |
| K73 [D:HP6; E:T41; N7] | Main, merge K43 | Region certificates require covering/pruning invariants and validated bounds; current numerical flag is not a rigorous certificate. |
| K74 [D:NG11; E:T26,T41] | Cited lemma | Cite existing local-trap counterexamples; do not re-prove them. |
| K75 [D:HP7,NG8] | Future work | NP-hardness needs a reduction for this integrated score and an appropriate numerical decision model. |
| K76 [D:HP6; E:T04; N12] | Supplement, merge K01 | Exact enumeration and eventual fixed-\(p\) dispatch; no wall-time conclusion. |
| K79 [A2; D:NG3,NG12; E:T39] | Cited lemma | Oracle/transcript limitation, not a regression-family impossibility or denial of analytic certificates. |
| K80 [D:CL3] | Future work | Proposed detection probabilities lack a validated sampling law for the actual flags. |
| K81 [E:T42] | Cited lemma | Neutral-resampling counterexample; identity mutation is not the production kernel. |
| K83 [D:PA2; E:T30; N2] | Cited lemma | Execution audit evidence supports claims only within checked binary/reduction conventions. |
| K84 [D:PA4; E:T27; N14] | Cited lemma | Preserve baseline search and streams; otherwise monotonicity is refuted. |
| K85 [V3; E:T43; N14] | Cited lemma | Declared-\(R\) rule and selection counterexamples, not a claim that every adaptive rule necessarily fails. |
| K86 [D:BR5; E:T30; N5,N14] | Cited lemma | Ideal stream independence plus a separately required implementation audit. |
| K89 [D:PA1,PA3; E:T32] | Cited lemma | Sequential-round and Gram-storage costs; no universal private-copy lower bound. |
| K90 [D1(d)] | Drop as theorem | Retain attributed complexity comparison in discussion; equal-\(p\)-order and accuracy-matched claims are unsupported. |
| K91 [D:PA5; E:T40] | Drop | Claimed SMC-versus-MCMC depth advantage uses unavailable particle parallelism and unjustified comparator lower bounds. |
| K92 [D:PA6,NG1; E:T40] | Future work | Requires an actual-design bottleneck, production clustering and matched comparator construction. |
| K95 [E:T33] | Cited lemma | Exact odds identity; computing all odds is not an inexpensive certificate. |
| K99 [D:NG1,NG13; E:T38] | Future work | Production-compatible moat and “all diagnostics pass” construction not yet proved. |
| K100 [D:PI4,NG7; E:T37] | Cited lemma, corrected | Exact duplicates imply symmetry; \(PIP\to1/d\) additionally needs posterior concentration on exactly one cluster member. Near-duplicates need quantitative assumptions. |
| K101 [D:NG7; E:T28] | Cited lemma | Exact-posterior Hamming decision under a cap; RB estimates need not obey the exact size-sum constraint. |
| K103 [D:KN4; E:T10; N10] | Supplement | Combined actual-round, empirical-measure and posterior-content package, §F. Generic independence-sampler theorem is cited. |
| K104 [D:ST10,BR7; E:T11] | Cited lemma | Standard exponential-family identities; use as start-divergence bookkeeping, not final-estimator error. |
| K107 [D:NU1; E:T29; N16] | Future work | Validated arithmetic remains OPEN. Existing heuristic error expression cannot certify production-size accuracy. |
| K108 [E:T29] | Cited lemma | Conditional mass/kernel perturbation inequalities; score bounds alone do not control an implemented sampler. |

| §D — Card conventions | Application |
|---|---|
| Fields shared by all cards | Each card uses the shared hypotheses only where explicitly invoked. “None” in numerical companion means no new experiment. No proposed Lean core is an existing certificate unless a filename is given. |
| Checked literature: SMC | [Dai–Heng–Jacob–Whiteley, *An invitation to SMC samplers*](https://arxiv.org/html/2007.11936v3), especially frozen tuning and independent-run pooling. These are cited foundations, not novelty claims. |
| Checked literature: second moments | [Cérou–Del Moral–Guyader (2011), Theorems 1.4–1.5](https://www.numdam.org/item/10.1214/10-AIHP358.pdf): the expansion and its stability conditions explain why a perfect-refresh variance formula cannot be substituted without proof. |
| Checked literature: independence sampler | [Mengersen–Tweedie (1996)](https://www.stat.rice.edu/~dcox/Stat552/Mcmc/MengersonTweedieAnnStat1996.pdf), bounded-density-ratio uniform ergodicity. The new obligation is matching the entire production round and reported objects. |

| Card D1 — K46/K51/K52/K62 [A1; N1,N4; E:T17,T19,T28] | Content |
|---|---|
| Statement/hypotheses | Under A, for each prescribed bounded summary record, \(E[W_rH_r(h)\mid\mathcal C]=\pi(h)\). For primary marginal RB records the same identity holds. The weighted ratio obeys \(P(|\widehat\mu-\pi(h)|>\varepsilon\mid\mathcal C)\le \min\{1,4(M_2-1)/R+4M_2/(R\varepsilon^2)\}\). |
| Guarantee | Accurate posterior expectations follow from independent stacking and a controlled island evidence second moment. |
| Goals | O1/O3; proposal §5.2, §5.4 PIP/joint-PIP, §13.1; Song–Liang screening transfer. |
| Status/fidelity | N1: **PROOF SKETCH**. PC1c3: **PROVED**, taking N1 as premise. FMP-M1: **PROVED**, XF **VERIFIED**. Package: **PROOF SKETCH**; actual coded grid and primary pooling; LS0 is irrelevant to these records. |
| Self-check/novelty | New assembly unchecked; not a new SMC theorem. **NEW-COMP** for the actual measured records and statistical/Monte Carlo error separation; cited SMC/SLLN foundations. |
| Route/key lemma | Discharge the marked endpoint identity using T12; handle each RB record at its pre-Gibbs position. Cite PC1c3. Union-bound a predeclared class; add \(|\pi(h)-h(S_0)|\le1-\pi(S_0)\). |
| Difficulty/Lean | Substantial interface proof. Extend `T12Core.lean` beyond its explicit `hstep` assumption; finite ratio-denominator and MPM-margin lemmas. |
| Dependencies/risk | N9, IND-T, T12, PC1c3; main risk is marking/conditioning fidelity and large \(M_2\), not convergence of calibration. |
| Fallback/stop | Fixed finite classes and the checked marginal identity first. Stop the general-\(h\) extension if its record identity fails; §13.1 then escalates, rather than being silently withdrawn. |
| IC3/design/numerics | §E’s genuinely correlated family gives \(M_2=O_P(1)\). LH remains covered by the identity, without an efficiency promise. Numerical companion: none. |

| Card D2 — K18/K15/K17 [S1; D:NG1; E:T38] | Content |
|---|---|
| Statement/hypotheses | For positive production tables define \(B_b=\sum_Ur_b(U)\), \(q_b(U)=r_b(U)/B_b\), and \(A(k)=\varpi(k)\prod_bB_b/\bar Z_0\). For every feasible \(S\), \(\pi_0(S)=A(|S|)\prod_bq_b(S_b)\). On the explicit LH family under G, \(\pi_0(S_0)=p^{-2}n^{-1}e^{O_P(1)}\), while \(\pi(S_0)\to1\). |
| Guarantee | The exact start decomposition identifies how block-local information can suppress the truth despite a consistent full posterior. |
| Goals | O1/O3; §5.3–5.4; misspecified-subset comparison. |
| Status/fidelity | DIL-E: **PROVED**, XF **VERIFIED**; DIL-E1: **PROVED**, XF **VERIFIED***. T27(i): **PROVED-LOCKED, CONDITIONAL**; LH discharges its hypotheses through Thm3/4-EXP and Thm5-LH. Start unchanged in v3.1. |
| Self-check/novelty | Filed checks exist; no re-derivation. **NEW** method-specific start analysis; generic block computation is not new. |
| Route/key lemma | Cite DIL-E/E1 and the checked LH masking law. Retain feasibility/cap and production-table normalization; exclude DIL-DM(i). |
| Difficulty/Lean | Routine assembly. Finite factorization, prior correction and logarithmic decomposition. |
| Dependencies/risk | Checked start lemmas and actual partition equality. Risk: conflating independent block probabilities with the size-coupled start. |
| Fallback/stop | Exact decomposition for arbitrary partitions plus the explicit LH law. Do not extend to random adaptive packing without a new proof. |
| IC3/design/numerics | Explicit LH family above; favourable and masked sequences remain separate. Numerical companion: none. |

| Card D3 — K106/K19/K105 [S2; D:ST9; E:T25,T38] | Content |
|---|---|
| Statement/hypotheses | On the explicit LH family, let \(a_n=\pi_0(S_0)\), \(Q_n^\star=p^2n\). For \(Q\) iid start draws, the miss probability is \((1-a_n)^Q\). Further \(1+\chi^2(\pi\|\pi_0)\ge\pi(S_0)^2/a_n\), and \(KL(\pi\|\pi_0)\ge\pi(S_0)\log(1/a_n)-\log2\). |
| Guarantee | Start-only discovery and one-shot correction incur the masked start’s inverse-mass cost. |
| Goals | O1/O2; §5.3–5.4; explains why moving beyond the start matters. |
| Status/fidelity | SEP-A/SEP-B: **PROVED**, XF **VERIFIED**. KL: **PROOF SKETCH**. The comparison algorithms are iid start-only/one-shot variants, explicitly not production SMC. |
| Self-check/novelty | Checked separation cores; KL addendum unchecked. **NEW-COMP** for this LH family. Generic importance-sampling inequalities are lemmas. |
| Route/key lemma | Cite SEP-A/B; use the singleton event in finite divergence inequalities. State unnormalized evidence relative variance exactly as \(\chi^2/Q\); do not call that the general self-normalized ratio variance. |
| Difficulty/Lean | Routine. Binomial miss probability, event coarsening and finite divergence inequality. |
| Dependencies/risk | K18 masking law and posterior concentration. Risk: turning this estimand-specific comparison into a universal algorithm lower bound. |
| Fallback/stop | Ship the checked discovery threshold and evidence-IS variance. Remove any unsupported general-ratio claim; retain the bridge motivation without claiming tempering is uniquely necessary. |
| IC3/design/numerics | Explicit LH family. Numerical companion: none. |

| Card D4 — K69/K65/K68/K72 [R3–R5; N3,N11] | Content |
|---|---|
| Statement/hypotheses | Under G on the explicit LH family, A, SR, GUARD-W and OP-LS0, use the prescribed emitted start-mode center, complete scans and \(\ell\ge c-1=1\). Then \(P(\mathcal O,\widehat S^+\ne S_0)\to0\). Deterministically, the capped tie-aware TD′ progress condition gives LS-score’s \(\max\{\Phi(S^\circ)-1,0\}\) scoring bound. |
| Guarantee | The decided LS0 mechanism repairs an explicit correlated masked family, subject to output and implementation fidelity. |
| Goals | O3; Song–Liang MAP comparison; finite search interpretation. |
| Status/fidelity | T38-b1-LH: **PROVED**, SF/XF **VERIFIED***. TheoremA and LS-score: **PROVED**, qualified filed checks. T38-(0): **PROVED**, XF **VERIFIED***. Theory covers v3+LS0; integrated-core/tie-DP gaps remain. |
| Self-check/novelty | Inherited checked cores; new package unchecked. **NEW-COMP**; no universal landscape claim. |
| Route/key lemma | Cite LH start-center concentration, LH-LAT, LS-score and T38-(0). Preserve posterior/discovery/delivery decomposition; the favourable iid-start bound is a separate corollary. |
| Difficulty/Lean | Substantial fidelity assembly. Existing `T37Greedy.lean`, `T37Lattice.lean`, `T21HPM.lean`; add emitted-center/move-count interface. |
| Dependencies/risk | K09, K07, K93, N2(c,e). No use of C3-PGD’s refuted implication or general LH locking. |
| Fallback/stop | Checked deterministic capped-lattice theorem plus exact-Gram conditional implication. If code fidelity fails, retain the specification theorem with the gap explicit; no claim about shipped output until repaired. |
| IC3/design/numerics | Explicit LH family, fixed support four; current logarithmic \(\ell\) eventually suffices. Numerical companion: none. |

| Card D5 — K43/K42/K44/K45/K73 [A3; N7,N13,N17; E:T24,T41] | Content |
|---|---|
| Statement/hypotheses | Under A, let \(\mathcal T\) contain distinct stored models and \(Z_{\mathcal T}=\sum_{\mathcal T}\varpi m\). A valid envelope \(m(S)\le U_m\) gives \(U=Z_{\mathcal T}+U_m[1-\sum_{\mathcal T}\varpi(S)]\ge Z\). For \(\pi^{\mathcal T}=\pi(\cdot\mid\mathcal T)\), \(TV(\pi,\pi^{\mathcal T})=1-Z_{\mathcal T}/Z\le1-Z_{\mathcal T}/U\). |
| Additional guarantees | \(Z_{\mathcal T}\le Z\) certifies underestimation whenever \(\widehat Z<Z_{\mathcal T}\). The joint-output lower confidence bound is \(\max\{Z_{\mathcal T},\alpha\widehat Z\}\). Region certification requires valid subtree envelopes covering the declared region; budget exhaustion is unresolved. |
| Goals | O1/O3; §5.4; positive diagnostics. |
| Status/fidelity | N17: **PROVED**. MZ-P3: **PROVED**. N13: **PROVED**. N6 output form: **CORRECT WITH AMENDMENT**. OCERT-LemmaM: **PROVED**, XF **VERIFIED**. Residual-envelope/TV assembly: **PROOF SKETCH**. |
| Self-check/novelty | Mixed filed checks and unchecked assembly. **NEW-COMP** for the adopted card/store; no new Markov inequality. |
| Route/key lemma | Positivity, residual prior mass, conditioning identity and branch-cover invariant; cite amended PC1/PC2 results, not erroneous OCERT-C1 clauses. |
| Difficulty/Lean | Substantial. Finite sums, top-store retention, event containment and branch-cover induction. |
| Dependencies/risk | N13 and merge semantics; GUARD-W for output transfer. Floating-point envelopes require N16; current numerical flags do not discharge it. |
| Fallback/stop | Deterministic stored-mass lower bound plus real-arithmetic TV certificate. If envelopes are loose, report their actual bound; never call replay a validation proof. |
| IC3/design/numerics | Any admissible correlated design, including explicit LH and §E families. Numerical companion: none. |

| Card D6 — K87/K88 [D1; R5(c); N15; E:T31–32] | Content |
|---|---|
| Statement/hypotheses | For declared budgets and the actual execution DAG, write \(m=p+B+2\), \(k_*=\min(K,\lfloor p/2\rfloor)\). Final work is \(RN(T+L+4)m\) elementary-step slots; final island depth is \(N(T+L+4)m\), multiplied by island waves when workers are fewer than \(R\). |
| Remaining costs | Add setup/clustering, table scoring, convolution, summaries, reductions and declared certificates. Tier-\(e\) calibration uses at most \((1+4I_e)H_e\) population trajectories in work and \((1+I_e)H_e\) in four-worker depth; \(I_e\le\ell\). Each local search uses at most \((\ell+1)[p+k_*(p-k_*)]\) score evaluations. |
| Guarantee/goals | Honest work and island-level depth accounting; O2 and Song–Liang §6 comparison. |
| Status/fidelity | MA-PropD: **PROVED (counting, given the code’s structure)**. T32(i): **PROVED**, SF **VERIFIED**, XF none. Cost-T38: **PROVED-UNDER**, XF **GAP**. Updated full count: **PROOF SKETCH**. |
| Self-check/novelty | Existing counting partly author/same-family checked. **MODEST**, method-specific execution accounting. |
| Route/key lemma | Count executed loops, both tiers, baseline-retaining search and LS0. Attach score-operation costs separately; a step slot is not a constant-time score. |
| Difficulty/Lean | Substantial audit, routine mathematics. Finite loop-count and task-DAG sums. |
| Dependencies/risk | MA merge/worker facts, K06/K64 and N15. Main risk: missing rebuild factor or asserting unimplemented particle parallelism. |
| Fallback/stop | Explicit operation-count formula with no simplified rate or speed-up. Stop simplification at the first unaudited component. |
| IC3/design/numerics | Every admissible input; LH and §E families exhibit growing dimensions. Numerical companion: none; no new timing claim. |

| Card D7 — K25/K26/K27/K33 [D:BR1–6; E:T13–14; N5,N15] | Content |
|---|---|
| Statement/hypotheses | Positive finite \(\gamma_0\), nonempty fixed \(V\), \(u<v\), \(w=2v-u\), \(a_t=q_t(V)\). Then \(\rho_{\rm full}(u,v)=\rho_V(u,v)a_ua_w/a_v^2\). If \(a_u,a_w\ge1-\eta\), restricted ESS at least \(0.9\) implies full ESS at least \(0.9(1-\eta)^2\). |
| Coded-grid clause | For \(D_V=\operatorname{osc}_Vd>0\), every increment at most \(h=2\sqrt{\log(10/9)}/D_V\) passes. With \(P\) pilot targets and bisection resolution at least \(h/2\), a conservative insertion count is \(P+\lceil2/h\rceil+1\), absent ceiling/snap failure. |
| Guarantee/goals | Quantifies exactly what restricted ESS certifies; O1/O2 and §4.4/§8.2. |
| Status/fidelity | New identity/assembled bound: **PROOF SKETCH**. STG-L0/L1/G: **PROVED**, no checks recorded. T26BUD-G: **PROVED, deterministic**. Actual restricted construction; exact-frontier optimality remains a separate idealization. |
| Self-check/novelty | New assembly unchecked. **NEW-COMP** for restricted/full transfer and coded resolution; generic convexity/greedy results are cited. |
| Route/key lemma | Three-normalizer cancellation; bounded variance of \(d\); count full versus target-truncated steps. Control mass at the look-ahead \(w\), not merely at \(u,v\). |
| Difficulty/Lean | Substantial numerical-interface proof. Finite normalizer algebra, monotone predicate and bisection invariant. |
| Dependencies/risk | Positive tables and legal endpoints. Restricted coverage is not established by observing good ESS. |
| Fallback/stop | Exact correction identity and finite termination/cap accounting. Drop a stage-count simplification if snap/resolution cannot be justified. |
| IC3/design/numerics | §E family supplies bounded \(D_V\le D\), with nonzero cross-block correlation. Numerical companion: none. |

| Card D8 — K93 [R1; D:TG4; E:T35–36] | Content |
|---|---|
| Statement/hypotheses | Use FIX §1.1 verbatim: R1, G, R, \(\mathrm{SE}_\lambda(j_0)\), \(\mathrm{SE}_w(m_n^\sharp;g_0)\), and BM-∞ or BM\((c>c_0)\). Then \(1-\pi(S_0)=O_P(\sqrt{\log n/n})\); exact HPM/MPM are consistent. Without beta-min, retain only T03♯’s large-signal inclusion clause. |
| Hypothesis expansion | \(s_0\) fixed, \(p\le n^A\); bounded signal energy; fixed positive normalized small-set eigenvalue; fixed positive unnormalized eigenvalue through deterministic exact-prior-tail cutoff \(m_n^\sharp\); \(j_0=\lceil(2A+1)s_0\rceil+1\). BM-∞ requires \(\theta_{\min}^2n\phi_0^2/(\sigma^2\log n)\to\infty\). |
| Guarantee/goals | The exact target supports sparse selection under explicit design conditions; O3, Song–Liang screening/MAP. |
| Status/fidelity | T03♯, T02(i♯), T02(ii♯): **PROVED**, SF/XF **VERIFIED**. Target unchanged; independent of LS0/grid/pooling. |
| Self-check/novelty | Filed checks; no re-derivation. **MODEST** target-specific extension. Rossell’s posterior-to-decision inequality is cited, not claimed new. |
| Route/key lemma | Cite exact BB tail, underfit separation and overfit summation. Preserve the distinction between an \(O_P\) rate and an unproved corresponding expectation rate. |
| Difficulty/Lean | Routine restatement. Finite prior-tail algebra; Gaussian asymptotics remain prose. |
| Dependencies/risk | FIX and REG:134. Proof thresholds are asymptotic and can exceed two million in recorded examples. |
| Fallback/stop | Fixed-\(p\), uniformly nonsingular correlated Gaussian design. If broader hypotheses cannot be matched, narrow explicitly; never report study-scale guarantees. |
| IC3/design/numerics | Explicit LH has eigenvalues bounded below by \(0.4\), fixed nonzero coefficients and bounded energy. Numerical companion: none. |

| Card D9 — K09 [D:ST1(c); E:T07; N3] | Content |
|---|---|
| Statement/hypotheses | Positive finite block tables, size-only capped prior, exact comparisons. Max-plus convolution gives the optimal score for each total size. Choose the smallest maximizing size; successively include the smallest index whenever an optimal completion consistent with earlier choices exists. The resulting model is the prescribed lexicographically smallest start maximizer. |
| Guarantee/goals | LS0’s launch rule can be implemented without enumerating exponentially many ties; O3 and K69 fidelity. |
| Status/fidelity | N3 tie-DP invariant: **OPEN**. Proposed proof: **PROOF SKETCH**. Already-decided e4 rule; actual integration remains unverified. |
| Self-check/novelty | Unchecked. **MODEST** implementation-specific correctness proposition. |
| Route/key lemma | Max-plus feasibility invariant under a fixed prefix; induction on indices and the selected total size. |
| Difficulty/Lean | Routine/substantial. Finite optimization, feasibility and lexicographic minimality. |
| Dependencies/risk | Exact score/size tie semantics; no reliance on the old million-tie enumerator. |
| Fallback/stop | Unique-maximizer instances, where tie enumeration is irrelevant. If the prefix invariant fails, stop the general tie claim and retain the explicit integration gap. |
| IC3/design/numerics | Identical standardized columns produce symmetric table ties; \(n=40,p=20\) permits SMC dispatch. Unique-maximizer LH supplies the simpler fallback. Numerical companion: none. |

| Card D10 — K07/K06/K22 [D:ST5–6,KN6; E:T05,T08; N8] | Content |
|---|---|
| Statement/hypotheses | Suppose all within-group distances are strictly smaller than all between-group distances, with group sizes at most \(B\). Complete linkage forms each group before merging groups; cutting and whole-cluster packing preserve groups. If additionally every group exceeds \(B/2\), output blocks equal groups. |
| Counting clauses | \(\lceil p/B\rceil\le J\le2\lceil p/B\rceil\), and \(\sum_b2^{|C_b|}\le p2^B/B\). The symmetrized capped graph has at most \(pB\) edges and, for \(p>1\), no isolated vertex. No false-edge probability is claimed. |
| Guarantee/goals | Gives checkable partition fidelity and deterministic setup bounds; O1/O2/O3. |
| Status/fidelity | PART-ThmA: **PROVED**, XF **VERIFIED***. PART-pairing: **OPEN**. Additional counting/graph assembly: **PROOF SKETCH**. Uses actual cut/packing and graph rules. |
| Self-check/novelty | Inherited partition check; assembly unchecked. **MODEST** production-specific proposition. |
| Route/key lemma | Agglomeration induction, no-split packing invariant and charging adjacent next-fit bins. |
| Difficulty/Lean | Routine. Finite partitions, bin counting and graph union. |
| Dependencies/risk | Exact strict separation, not merely “block structure.” PART-CE2 forbids unconditional block-equals-group claims. |
| Fallback/stop | Group preservation and deterministic cost only. Do not infer which size-five groups are paired. |
| IC3/design/numerics | Both explicit LH and §E have groups of nine, within correlation larger than every cross correlation, and eventually \(B=16\). Numerical companion: none. |

| Card D11 — K01/K02/K03/K04/K05/K76 [D:TG1–3; E:T01–04; N12,N17] | Content |
|---|---|
| Statement/hypotheses | For finite nonconstant standardized data, \(n\ge3,p\ge1\), the shipped ridge/IG target is proper even with rank-deficient submodels. \(Q_S\ge Y/(n+1)\), \(1\le\det H_S/\det(G_S+I)\le(n+1)^{|S|}\), and \(Z\le C_n(2b_0+Y/(n+1))^{-\nu}\). |
| Other clauses | The normalized capped BB prior is used once. Target probabilities are affine-invariant and permutation-equivariant. Contrast regression uses IG shape \(a_0+1/2\) and rate \(b_0s_y^2\). Exact enumeration returns exact target summaries; every fixed-\(p\) sequence eventually satisfies the dispatch threshold. |
| Guarantee/goals | Defines precisely what posterior/evidence the method computes; supports all three objectives and §5.1. |
| Status/fidelity | N17: **PROVED**. T01 reduction: **PROVED-LOCKED**. Remaining assembly: **PROOF SKETCH**. Target/exact branch; no n=2 implementation claim. |
| Self-check/novelty | Mixed checked inputs and unchecked assembly. **MODEST** actual-target foundation. |
| Route/key lemma | Spectral bounds, finite prior sums, contrast change of variables and growing enumeration threshold. Monotone fit/determinant terms give valid score envelopes; no monotonicity of the full score is asserted. |
| Difficulty/Lean | Routine. Matrix order, determinant bounds, finite prior normalization and enumeration. |
| Dependencies/risk | Standardization/reduction conventions; current floating-point flag is heuristic. The exact pairwise IG perturbation coefficient is \(2\nu b_0\), not universally \(nb_0\). |
| Fallback/stop | Proper target and exact-arithmetic enumeration on the current \(n\ge3\) domain. Keep uncertain invariance/output extensions out. |
| IC3/design/numerics | Duplicate and correlated columns are allowed; e.g. two identical standardized columns plus an independent column. Numerical companion: none. |

| Card D12 — K77/K78 [V4,R4; N6; E:T15,T43] | Content |
|---|---|
| Statement/hypotheses | A plus stop-only statistical coupling/GUARD-W. If potential-run failure event \(B\) has conditional probability at most \(\alpha\), actual output with that failure satisfies \(P(\mathcal O\cap B\mid\mathcal C)\le\alpha\). No claim follows for \(P(B\mid\mathcal O,\mathcal C)\) without additional independence or delivery control. |
| Guarantee/goals | Prevents stopping and availability selection from invalidating the paper’s stated coverage interpretation; O1/O3. |
| Status/fidelity | LemmaRO: **PROVED**, XF **VERIFIED***. CEX-guard: **COUNTEREXAMPLE**, XF **VERIFIED***. N6: **PROVED** for potential run; output form **CORRECT WITH AMENDMENT**. GUARD-W **not audited**. |
| Self-check/novelty | Filed checks; revised execution scope pending. **MODEST** method-specific reporting proposition; elementary probability is cited. |
| Route/key lemma | Existing coupling plus event containment. Preserve statistical-output scope, not equality of clocks or diagnostics. |
| Difficulty/Lean | Routine mathematics, substantial code audit. Finite event containment/counterexample. |
| Dependencies/risk | N2(e), NA interface, worker and LS0 interruption handling. A capped completed local search is not operational interruption. |
| Fallback/stop | Potential-run theorem, clearly labelled, while the audit is repaired. Do not condition on completion or substitute calibration estimates. |
| IC3/design/numerics | Any admissible correlated input, including both exhibited families. Numerical companion: none. |

| Card D13 — K30 [D2(c); D:BR4,NG5; E:T38] | Content |
|---|---|
| Statement/hypotheses | Consider the ideal full-support two-state bridge with initial log odds \(-A\), \(A\to\infty\), and terminal log odds bounded away from zero on the other side. Use the exact maximal-increment ESS-\(0.9\) grid. Then its crossing cost is \(\log_2A+O(1)\), in the scope of STG-M. |
| Guarantee/goals | Sharp crossings can require growing sequential stage depth despite a bounded thermodynamic-length heuristic; O2. |
| Status/fidelity | STG-M: **PROVED**, XF **VERIFIED*** for logarithmic order; explicit decimal constants **GAP**. Ideal-grid component, not coded calibration. |
| Self-check/novelty | Filed qualified check; no re-derivation. **NEW** coarse-grid crossing result; fine-grid thermodynamic-length limits are cited. |
| Route/key lemma | Cite STG-M’s exact two-state recurrence; retain its endpoint assumptions and discard disputed decimal constants. |
| Difficulty/Lean | Routine assembly. Two-point normalizer algebra and recurrence bounds. |
| Dependencies/risk | STG-M only; extension from pair dominance or to the coded grid is not automatic. |
| Fallback/stop | Checked logarithmic-order statement on the ideal two-state bridge. No production-stage asymptotic unless K31 is separately proved. |
| IC3/design/numerics | The explicit LH family has masked/full-model log-odds reversal; the two-state restriction is expressly a comparison object, not the complete regression posterior. Numerical companion: none. |

| §E — Card D14: K102/K10/K11/K53 [S4; D:ST2,ST4,EV3; E:T12,T19] | Content |
|---|---|
| Primitive hypotheses | A. Write \(G_D\) for the actual partition’s block-diagonal Gram, \(E=G-G_D\), \(H_D=(n+1)G_D+I\), \(A_D=G_D+I\), \(Y=y'y\), \(\nu=a_0+n/2\). |
| Checkable quantities | \(a=nz'H_D^{-1}z/(2b_0+Y)<1\); \(\delta_A=\|A_D^{-1/2}EA_D^{-1/2}\|<1\); \(\delta_H=\|(n+1)H_D^{-1/2}EH_D^{-1/2}\|<1\); \(r=\delta_Ha/[(1-\delta_H)(1-a)]<1\). |
| Bound | Put \(b_X=\frac K2[-\log(1-\delta_A)-\log(1-\delta_H)]-\nu\log(1-r)\) and \(D_*=\nu a^2/[2(1-a)]+2b_X\). Proposed conclusion: \(\operatorname{osc}d\le D_*\). |
| Weight guarantee | For every successful coded grid, \(E_{\pi_0}[(\pi/\pi_0)^2]\le e^{D_*}\), \(M_2\le e^{D_*}\), and each increment \(\Delta\) has \(\chi^2(q_{u+\Delta}\|q_u)\le e^{\Delta D_*}-1\). Actual invariant kernels are retained. |
| Goals/status | O1; binding §5.3. New extension **PROOF SKETCH**, unchecked. Existing O-WSTAB results retain their H-ORTH/ideal-grid statuses and are not used as proof of this extension. |
| Novelty/route | **NEW-COMP**. Shared-variance identity plus relative resolvent/log-determinant perturbation; then telescoping bounded potential ranges and cited evidence unbiasedness. |
| Difficulty/Lean | Substantial. Principal-submatrix perturbation and scalar logarithmic bounds; finite product-range argument. |
| Dependencies/risk | N9/T12; no perfect-refresh approximation. Low cross-block correlation alone is insufficient: \(a\) controls shared-variance coupling. |
| Fallback/stop | Prove the explicit family below directly if the general matrix bound stalls. Stop after failure of both routes; an orthogonal-only substitute fails the binding goal and escalates. |
| IC3/numerics | Nonzero-correlation family below; no new numerical experiment. |

| §E — IC3 exhibit and proof-route assessment | Detail |
|---|---|
| Design | \(p=9\lfloor n^{1/3}/9\rfloor\). Groups of nine have correlation \(1/4\); every cross-group correlation is \(\varepsilon_n=1/(np)>0\). Centered \(X'X=(n-1)\Sigma_n\), which exists eventually. Within/between separation gives the actual groups as blocks. |
| Positive definiteness | The block-diagonal correlation matrix has minimum eigenvalue \(3/4\). The cross-block perturbation has operator norm at most \(p\varepsilon_n=1/n\). Thus \(\lambda_{\min}(\Sigma_n)\ge3/4-1/n\). |
| Signal/noise | Under G, put one coefficient \(n^{-1/4}\) in each of two groups and all others zero, with \(\sigma^2=1\). Signal energy is order \(\sqrt n\); projected noise energy is \(O_P(p)\). Standardization preserves the relevant explained-energy ratio. |
| Primitive rates | \(a=O_P(n^{-1/2})\); \(\delta_A,\delta_H=O(n^{-1})\); \(K=p=O(n^{1/3})\). Consequently \(\nu a^2=O_P(1)\), \(K\delta_A+K\delta_H=o(1)\), and \(\nu r=o_P(1)\). Hence \(D_*=O_P(1)\). |
| Why the key lemma is credible | Replacing \(G\) by \(G_D\) while holding \(z,Y\) fixed is an algebraic comparison. Its residual correction is controlled by the resolvent bound. The remaining orthogonal-block discrepancy is exactly the shared-noise term, bounded by \(\nu a^2/[2(1-a)]\). |
| Why the grid gap disappears | Every realized incremental average lies between \(e^{\Delta d_{\min}}\) and \(e^{\Delta d_{\max}}\). The increments sum to one. Thus \(\widehat Z/Z\le e^{D_*}\) pathwise; using \(EW=1\) gives \(EW^2\le e^{D_*}\), regardless of grid quality or mutation mixing. |
| Strength and boundary | This controls one-shot weights, stage weights and actual island evidence moments with genuinely nonzero dependence. It does not establish a sharp \(T/N\) variance rate, useful constants under fixed strong signals, or calibration delivery. Those remain separate obligations. |
| Budget consequence | For a predeclared class of at most \((n+p)^2\) bounded summaries, \(R=4\lceil(n+p)^6/4\rceil\) suffices for simultaneous error \(o_P(1)\) on this family by K46/K52 [N1,N4]. This is a conservative existence rate, not a recommended allocation or wall-time claim. |

| §F — Approximation objects | Interpretation |
|---|---|
| Exact correction | \(\gamma_1\) is the exact working posterior. Approximation error concerns finite Monte Carlo output, a deliberately restricted store, numerical perturbation, or an uncorrected start—not a residual composite-posterior target bias. |
| Empirical measure | Let \(\eta_r\) average the four measured endpoint empirical measures. Define \(\widehat\pi=\sum_rW_r\eta_r/\sum_rW_r\). This is the mathematical measure underlying general-\(h\) averages; storing all its atoms is not a proposed method change. |
| RB distinction | Primary RB PIPs are not necessarily marginals of this single \(\widehat\pi\). They use K46/K52 [N1,N4] directly. Do not use their coordinate vector as though it defined a joint posterior. |

| Card D15-TV — K103 [D:KN4; E:T10; N10], merged TV package | Content |
|---|---|
| Statement/hypotheses | Under A, let \(M_\phi=\max_Sq_\phi(S)/\pi_0(S)\). The full production round minorizes \(q_\phi\) by \(1/M_\phi\), without a \(1/m\) factor. Thus terminal-particle marginal TV after \(L\) rounds is at most \(q^L\), \(q=1-1/M_1\). |
| Realized-measure bound | For any predeclared partition of \(\Omega\) into \(d_0\) cells, the weighted empirical cell law satisfies \(P(TV>\varepsilon\mid\mathcal C)\le\min\{1,4(M_2-1)/R+4d_0M_2/(R\varepsilon^2)\}\). Taking singleton cells gives full model-space TV. |
| Guarantee/goals | Separates a mixing-law guarantee from random empirical error; O1, §5.4 and §13.1. |
| Status/fidelity | Production-round/empirical assembly: **PROOF SKETCH**, unchecked; no registry row. Actual kernel, coded grid and weighted endpoint pooling. Independence-sampler theorem itself is **KNOWN—CITE**. |
| Novelty/route | **NEW-COMP**. Every round contains the independence move; surrounding invariant kernels preserve its minorization. For empirical TV, use N1 for cell indicators, independence across islands, Cauchy–Schwarz and a denominator event. |
| Difficulty/Lean | Substantial interface; finite minorization composition and vector-ratio inequalities. |
| Dependencies/risk | N9, N1, stream contract. Full-state dimension may make the empirical bound unusable; particle-law accuracy does not imply empirical-TV accuracy. |
| Fallback/stop | Fixed-dimensional/coarsened TV and exact per-functional bounds. If all claimed objects cannot be matched to actual records, narrow the object explicitly; binding coverage remains subject to §I. |
| IC3/design/numerics | §E family has \(M_1\le e^{D_*}=O_P(1)\); current \(L\to\infty\) yields terminal-law convergence. Numerical companion: none. |

| Card D15-KL — K103/K104 [E:T10–11], KL clauses | Content |
|---|---|
| Statement/hypotheses | Under D15-TV, let \(\lambda_L\) be a terminal particle’s potential-run marginal law and \(q=1-1/M_1\). Then \(\lambda_L=(1-q^L)\pi+q^L\nu_L\), yielding \(KL(\pi\|\lambda_L)\le-\log(1-q^L)\) and \(KL(\lambda_L\|\pi)\le q^L\log(1/\pi_{\min})\). |
| Empirical direction | Since \(\pi_{\min}>0\), \(KL(\widehat\pi\|\pi)\le\chi^2(\widehat\pi\|\pi)\le4TV(\widehat\pi,\pi)^2/\pi_{\min}\). The same statement holds for a finite coarsening with its minimum cell mass. |
| Reverse empirical obstruction | If any positive-posterior state is absent from the endpoint record, \(KL(\pi\|\widehat\pi)=\infty\). In particular this happens surely when \(|\Omega|>4NR\). This is a support obstruction, not an unproved mixing property. |
| Guarantee/goals | Names which KL quantities admit finite error guarantees; §5.4. |
| Status/novelty | New assembly **PROOF SKETCH**, unchecked; support implication holds directly by definition. **NEW-COMP** only for the actual reported-measure interpretation; convexity/divergence inequalities are cited lemmas. |
| Route/difficulty/Lean | Minorization-mixture decomposition and finite log-sum inequalities; routine after D15-TV. |
| Dependencies/risk | D15-TV; \(\pi_{\min}\) can be tiny, so forward-KL convergence needs stronger rates than TV. No empirical smoothing is assumed. |
| Fallback/stop | Fixed-data terminal-law KL and forward empirical KL. A finite reverse-empirical-KL requirement cannot be met by this unsmoothed measure; escalate rather than change the estimator silently. |
| IC3/design/numerics | Every finite admissible correlated design; uniform rates require the explicit displayed minimum-mass condition. Numerical companion: none. |

| Card D15-CI — K103 [§5.4 extension], posterior-content clauses | Content |
|---|---|
| Statement/hypotheses | Under D15-TV, suppose \(P(TV(\widehat\pi,\pi)>\varepsilon\mid\mathcal C)\le\delta\). For any possibly output-selected set \(C\) with \(\widehat\pi(C)\ge1-\alpha\), \(P(\mathcal O,\pi(C)<1-\alpha-\varepsilon\mid\mathcal C)\le\delta\), provided GUARD-W holds. |
| Coarsened interval version | Use the model-size partition, with \(d_0=K+1\), to obtain the same statement for an interval of model sizes computed from the size-distribution accumulator. This avoids full-state dimension. |
| Guarantee/goals | Bounds Monte Carlo error in the posterior content of credible sets; §5.4. It is not a frequentist coefficient-coverage theorem. |
| Status/fidelity | **PROOF SKETCH**, unchecked; consequence of simultaneous TV, not an additional sampling algorithm. Applicable to specified summary records; unavailable historical records cannot be reconstructed by assertion. |
| Novelty/route | **NEW-COMP** reporting consequence; deterministic event-set transfer is elementary. Simultaneity permits selecting the interval after seeing the estimated distribution. |
| Difficulty/Lean | Routine after TV; finite set-mass inequality and output-event containment. |
| Dependencies/risk | D15-TV, N1 and GUARD-W. A fixed-\(h\) bound alone does not validate arbitrary output-selected sets. |
| Fallback/stop | Predeclared interval endpoints with simultaneous bounded-CDF control. If frequentist coefficient intervals are mandatory, this fallback does not satisfy that goal; §I requires an explicit decision. |
| IC3/design/numerics | §E correlated family; size has finitely many possible values. Numerical companion: none. |

| §G — Fidelity convention | Meaning |
|---|---|
| Yes / no / unknown | “Yes” means the mathematical result is compatible with that v3.1 feature, including when the feature is irrelevant. It does not assert that the integrated code was audited. “No” identifies a different variant. “Unknown” identifies a missing transfer/audit. Each row records LS0 / coded grid / weighted pooling in that order. |

| Inherited result relied on | LS0 / coded grid / weighted pooling; source | Gap | Gap lemma or required audit statement |
|---|---|---|---|
| T09; N9K | Yes / yes / yes; N9R:3–9,18–26; IDX:71–72 | Ideal uniforms/exact arithmetic; no finite-precision equality claim. | Preserve exact start law, normalizer and invariant round under the declared idealization; N16 handles machine perturbations separately. |
| T12; T31(i) | Yes / yes / yes; IDX:68–69 | General measured marks and extended streams require matching. | N1: each actual endpoint/RB record has the appropriate evidence-weighted expectation, conditionally on full \(\mathcal C\). |
| Prop2(a,b,d,e) | Yes / yes / unknown; REG:260 | Author **PROVED**, XF **GAP**; output wording and general marks cannot be inherited wholesale. | Use T12 for potential-run identities; transfer only by GUARD-W/event containment. |
| PC1c3 | Yes / yes / yes; IDX:114; INP:151–155 | N1 remains a premise. | Prove N1 for the actual general-\(h\) accumulator before invoking the finite-\(R\) bound. |
| FMP-M1 | Yes / yes / yes; REG:570 | Existing theorem concerns prescribed marginal PIPs, not arbitrary marks. | General-\(h\) accuracy uses N1 and its own deviation argument; do not infer it from M1 by renaming a variable. |
| MA-PropP; Prop2(c) | Yes / yes / yes for primary/secondary comparison; IDX:70; REG:261 | MA-PropP is author-only; finite-\(R\) monotonicity of normalized accuracy is absent. | Preserve declared independent islands and correct within-island products; use PC1c3 for finite-\(R\) claims. |
| DIL-E/E1 | Yes / yes / yes; REG:709–710 | Production-table normalization and feasibility must be retained. | Identify the actual capped start with the theorem’s factors for every feasible model. |
| T22(i)(ii)(iv) | Yes / yes / yes; IDX:337 | No favorable-rate conclusion follows from the deterministic statement alone. | Keep its reference-model hypotheses; use only the deterministic clauses in the accepted start package. |
| T27(i); Thm3/4-EXP; Thm5-LH | Yes / yes / yes; IDX:321–325,339; T38:159–166 | Exact-Gram, separate-block hypotheses; not the study’s adaptive iid design. | K07 verifies actual partition equality on the exhibited LH family. |
| SEP-A/SEP-B | Yes, irrelevant / no, comparison variant / no, one-shot variant; REG:641–643 | These are start-only/IS comparisons. | Label comparison algorithm and estimand explicitly; no production-SMC lower bound follows. |
| TheoremA; LS-score | Unknown / yes, irrelevant / yes, irrelevant; REG:150,326; M:399 | LS0 integration, emitted center and tie selection. | Integrated LS0 implements the capped tie-aware greedy map, emits its center and completes required scans on every delivered fit. |
| T38-b1-LH | Unknown / yes / yes, irrelevant; REG:330; INP:143–148 | N2(c,e), N3 tie-DP; mathematical v3+LS0 differs from unaudited integrated execution. | Combine the preceding LS0 audit with GUARD-W and the prescribed center invariant. |
| T38-(0); Thm4-C1 | Unknown / yes / yes, irrelevant; REG:264,324; M:400 | Correct all-scored ledger and output coupling. | Actual delivered HPM is the total-order maximum of all required scored models, including LS0 and retained baseline search. |
| T03♯; T02(i♯),T02(ii♯) | Yes / yes / yes, all irrelevant; REG:130–134; FIX:16–56 | Exact prior/standardization and full hypothesis match. | No new statistical proof; verify the unchanged target is exactly the theorem’s target. |
| MZ-P3; N13/PC1c5 | Unknown / yes / yes, restricted-store object; IDX:201–202; INP:224–226 | Bounded store is not a superset after additions. | Union-then-top-\(c\) merge preserves the score winner; scored \(S_0\) with \(\pi(S_0)>1/2\) survives truncation. |
| N17/PC1 claim 1 | Yes / yes / yes, all irrelevant; INP:247–249 | Machine upper bounds not validated. | Exact analytic envelope suffices mathematically; outward-rounded arithmetic is needed for a numerical certificate. |
| PC1c2; N6 | Unknown / yes / yes; IDX:187; INP:165–172 | GUARD-W premise, amended joint event. | Delivered bound equals the potential-run bound on output; then intersect the failure event with \(\mathcal O\). |
| OCERT-LemmaM; OCERT-C4 | Unknown / yes, irrelevant / yes, irrelevant; REG:403,407; INP:175–181 | Amended region/cap semantics and validated envelopes. | Every unvisited feasible region is covered by a valid bound; final certificate refers to the current returned winner. |
| MA-LemmaS; MA-PropW | Unknown / yes / yes; IDX:91–93; M:398–399 | W-cal execution and integrated LS0 remain unverified. | Deterministic reductions and private streams preserve serial statistical records; test calibration and integrated merge separately. |
| MA-CorWR/PC1c6 | Unknown / yes / yes; IDX:94,652; INP:228–232 | Requires the extra baseline-center search. | Expanded execution retains baseline streams and baseline search work before taking the all-scored maximum. |
| IND-T; Lemma-STREAM | Yes / yes / unknown for arbitrary \(R'\); REG:190,365; M:401 | Extended final-stream namespace not audited. | Final streams 10 through \(9+R'\) are disjoint from calibration and each other under the ideal stream model. |
| MA-PropD; T32(i) | Unknown for added LS0 / yes / yes; IDX:237–242; INP:236–240 | Updated searches, rebuild factor and scorer costs. | Recount the amended execution DAG with both tiers, baseline search, LS0, summaries and certificates. |
| STG-L0/L1/G; T26BUD-G | Yes, irrelevant / mixed / yes, irrelevant; REG:694–696; IDX:268 | Exact-frontier optimality is not finite-bisection equality. | Establish the production lower-endpoint/resolution invariant and count mandatory pilot targets. |
| STG-M | Yes, irrelevant / no / yes, irrelevant; REG:700 | Ideal two-state exact-frontier grid only; constants qualified. | No coded-grid transfer claimed. A future transfer must control off-pair mass and actual endpoint error. |
| LemmaRO; CEX-guard | Unknown / yes / yes; REG:258–259; M:400 | Serial guard check does not cover worker/merge/LS0 paths. | GUARD-W statistical coupling and all-unavailable output convention. No completion-conditioned unbiasedness. |

| §H — Rank | K-ID package [source] | Name | Placement | Reason |
|---|---|---|---|---|
| 1 | K46/K51/K52/K62 [A1; N1,N4] | Actual measured-summary accuracy | Main | Closes the central posterior-expectation obligation. |
| 2 | K102/K10/K11/K53 [S4; E:T12,T19] | Weak nonzero dependence and weight stability | Main | Directly addresses the binding missing §5.3 theorem. |
| 3 | K69/K65/K68/K72 [R3–R5] | Reported HPM on a masked correlated family | Main | Strongest checked output-selection route for the decided method. |
| 4 | K43/K42/K44/K45/K73 [A3; N7,N13,N17] | Stored-mass and region certificates | Main | Positive, inspectable posterior-error information. |
| 5 | K18/K15/K17 [S1] | Exact start decomposition and masking | Main | Explains the method-specific obstacle. |
| 6 | K106/K19/K105 [S2] | Start-only and one-shot correction cost | Main | Quantifies the obstacle without universal lower-bound rhetoric. |
| 7 | K87/K88 [D1; N15] | Actual island-level work and depth | Main | Supplies honest scalability accounting. |
| 8 | K103 [D:KN4; E:T10; §F extensions] | TV, directional KL and posterior content | Supplement | Makes the approximation object and guarantee precise. |
| 9 | K25/K26/K27/K33 [D:BR1–6; E:T13–14] | Restricted ESS and coded-grid geometry | Supplement | Separates calibration diagnostics from full-target guarantees. |
| 10 | K93 [R1] | Exact-target sparse selection | Supplement | Necessary statistical foundation, modest novelty. |
| 11 | K07/K06/K22 [D:ST5–6,KN6; N8] | Partition fidelity and setup bounds | Supplement | Exhibits actual correlated designs satisfying the hypotheses. |
| 12 | K09 [N3; E:T07] | Exact start-mode tie DP | Supplement | Closes a concrete LS0 fidelity obligation. |
| 13 | K01/K02/K03/K04/K05/K76 [D:TG1–3; E:T01–04] | Target, envelopes and exact branch | Supplement | Fixes estimands and boundary semantics. |
| 14 | K77/K78 [V4; N6] | Output-event validity | Supplement | Keeps availability selection out of coverage claims. |
| 15 | K30 [D2(c)] | Ideal two-state crossing depth | Supplement | Useful checked mechanism, explicitly separated from coded-grid claims. |

| §I — Decisions for HQ only | Requested disposition |
|---|---|
| §5.4 coverage interpretation — K103 [§F] | Does posterior-content error for existing model-space summaries satisfy the binding credible-interval goal? If frequentist coefficient-interval coverage is mandatory, record it as unmet and commission the necessary extension or explicit scope decision. This seat does not waive it. |
| Reverse empirical KL — K103/K104 [§F; E:T10–11] | Accept terminal-law KL and forward empirical KL, with the reverse empirical support obstruction stated explicitly; otherwise a full-support approximation/reporting change requires HQ authorization. A finite reverse-KL theorem for the unsmoothed sparse empirical measure is unavailable by definition when support is missed. |
| Binding fallback trigger — K46 [N1], K102 [S4] | If both the main and explicit-family fallback proofs fail, escalate the unmet §13.1 or §5.3 goal to Felipe. Neither an orthogonal-only replacement nor “descriptive summary, no theorem” closes the binding requirement. |
| Other method changes | None requested. Budget-growth formulas stay within meeting authority. Mixing, delivery, calibration convergence, random-design selection and validated numerics remain explicitly assigned theorem obligations or future work—not relabelled inherent limitations. |