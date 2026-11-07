> **Archive note.** In this archive, "02a" means `02_theory.md` (final state), "02b" means `02b_theory_campaign_history.md` (campaign history), and "REG-A"/"REG-B" or "registry A/B" mean parts A and B of `ID_REGISTRY.md`. Paths like `branch_snapshots/...` and `transcript/...` are relative to this folder.

# 05 · Open questions and next steps

Archive of the T3 thread "New BVS Headquarters" (threadId `5e38497d-7dfd-48f9-88e9-b21895922f58`), ending at [pos 1676] (2026-11-04T15:16Z). Companions: `03_results_and_conclusions.md` (03), `02a_theory_final.md` (02a), `02b_theory_campaign.md` (02b), `ID_REGISTRY_A.md` (REG-A), `ID_REGISTRY_B.md` (REG-B).

Conventions as in 03: IDs are `ID (native name)`; `[pos N]` are transcript positions; snapshot paths are relative to `branch_snapshots/`; "Summary:" marks editor text; **UNCERTAIN:** marks a conflict or gap in the sources.

Contents: §1 pending decisions of Felipe. §2 future work CJ01–CJ27 and drops. §3 the 17 obligations. §4 open conflicts and UNCERTAIN items. §5 engineering TODOs. §6 planned next steps. §7 infrastructure issues and rules.

---

# §1 Pending decisions and approvals (Felipe)

State at the end of the archive: HQ has approved the method (v3.1) and the theorem package; **Felipe had not yet approved the theorem list**. His last instruction ([pos 1673], 2026-11-04T15:10Z): "I will take a look at the theorems and give you feedback / questions later so we can keep working. Today we will use Claude through the remaining $19 of cloud and the remaining $121 of the other credit." HQ at [pos 1669]: "The only thing still waiting is your approval of the theorem list in FOR_FELIPE_THEOREM_LIST.md. After that, wave 1 launches: M1 (validity and accuracy), M3 (the start) and the foundations pack. I'm holding everything else until you've seen the list."

| # | Pending item | Exact content (source) | Position / file |
|---|---|---|---|
| P1 | Approve the paper-1 list | "8 main theorems plus 12 supplement cards": TH01 (M1 V/H) … TH08 (M8 Prop D), TH09–TH20 supplements. Statements: `MEET-THM/THEOREM_LIST_FINAL.md`; plain-language file `MEET-THM/FOR_FELIPE_THEOREM_LIST.md` | [pos 1650], [pos 1669] |
| P2 | Song–Liang separation scout | "The Song–Liang separation is not proved. The meeting couldn't get a sound proof that their split-and-merge loses true predictors under correlation. The paper compares with their results and cites the numerical counterexample as labelled evidence; our side, validity under any correlation, is proved (M1). I recommend one small scout HQ on the separation alongside wave 1. If it succeeds it becomes a ninth main theorem; nothing else waits on it." = CJ21 (FW21, K97) + CL23 (LIT-PAR G4, labelled numerical evidence, 5/318 vs 20/20) | [pos 1650]; `MEET-THM/MINUTES.md` §3 item 3 |
| P3 | Prop D (TH08) main or supplement | "Prop D (M8) in the main text or the supplement. I recommend main, for parallel scalability. The alternative leaves 7 main theorems." (Seat D's alternative: main = 7.) | [pos 1650]; MINUTES §3 item 2 |
| P4 | Reading of §5.3 (bridge form) | RL01 (HQ ruling Q1 (§5.3)) and RL05 (HQ ruling Q5): "§5.3 is met by the bridge form. One caveat: the example family gives useful constants only for very weak cross-block correlation, of order ε ≲ n^(−1/2)/p." The sharp ε-scale necessity is CJ22 (FW22). Felipe may overrule. | [pos 1650]; `MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`, `..._HQ_RULING_Q5.md` |
| P5 | Reading of §5.4 | RL02 (HQ ruling Q2): "coverage" means distance from the exact posterior's credible quantities (posterior-content error plus MC error), not frequentist coverage (CJ01, FW1). RL03 (HQ ruling Q3): TV/KL of the final estimate under masking is future work (CJ02, FW2), with at least one masked-regime accuracy statement shipped (TH04.f). | [pos 1650] |
| P6 | The stage count | "The stage count is a step function of correlation strength, held within two-sided bounds." = TH02.b6 (stage-count sandwich), TH02.b8 (step-function statement, example n = 40, p = 2, B = 1, T = 3 at ε = 10⁻⁵), TH07 (M7); RL05. | [pos 1650], [pos 1624] |
| P7 | Items HQ did on its own authority (for Felipe to see) | (i) "Two new run-card numbers added to the method as reporting only: a Jeffreys-divergence estimate and a cross-block correlation measure" = DF19 (Ĵ), DF20 (ε̂_×), AMENDMENT_HQ_02 (`MEET-v31/AMENDMENT_HQ_02.md`, theory/MEET-v31 @ 6a80fe5); (ii) growth rate (ii) R′_n = 4⌈(n+p)⁶/4⌉ "kept only inside a theorem, not as a method setting" = RL06 ("Felipe may overrule"); (iii) the overnight kill fixed by systemd units (§7). | [pos 1650], [pos 1639] |
| P8 | Registry updates for the registry owner | `MEET-THM/REGISTRY_PAPER1.md` §9: "five recommended registry updates for the registry owner" | [pos 1626] |
| P9 | The four method decisions (already approved) | Approved: (1) growth rates may be made explicit functions of (n, p), "limited to growth rates only, with no other method change"; (2) paper 1 claims island-level depth only (MD06); (3) confirmatory local-to-global test (done: ABL-CONF); (4) same seats. Recorded "All approved" at [pos 1304]. Kept here because the date of the island-depth decision differs across sources (02a §A7 U14). | [pos 1302], [pos 1304], [pos 1316] |
| P10 | Safeguard rule | "if a theorem behind one of your mandatory proposal goals (§5.1–5.4, §13.1) fails, it comes back to you. It is never silently dropped" (`MEET-v31/FOR_FELIPE_FINAL_METHOD.md` §5). Currently live for OB01 (N1, binding §13.1). | [pos 1584] |
| P11 | Older items not shown as closed | PR #1 (spine correction, `E-SPINE`): "It isn't merged" ([pos 850], part_04 line 175); LH-SCALE (referee's one compute ask, see §6): "Needs your OK" ([pos 824]). **UNCERTAIN:** later resolution of PR #1 and of LH-SCALE is not recorded in the positions read (LEDGER 20:45 UTC records "make all necessary changes to the spine claim" before PR #1 was opened). | [pos 824], [pos 850], [pos 893]; `campaign/LEDGER.md` |
| P12 | Method summary addendum | HQ "added [ABL-CONF] to your method summary" (`MEET-v31/FOR_FELIPE_FINAL_METHOD.md` §2) | [pos 1669] |

Standing user instructions that govern the next phase (verbatim positions):
- "extract until the last drop of information the method has into provable results. No rock can remain unturned" ([pos 1150]); every proposal goal is a hard gate ([pos 1148]).
- "unless I'm blind I don't see a reason for which it should deviate fundamentally from this approach … I'd need irrefutable reasons" (method stays composite-likelihood/SMC/HPM, [pos 1155]).
- The method must apply to any (n, p) with no arbitrary choices ([pos 1214], [pos 1226]).
- Biometrika first, "Down to Lean certificates", harder results after ([pos 1015]).
- "Use CW instead of CP" for subscription work; API credit for the main work ([pos 1061]); "no API" was said at [pos 1324]–[pos 1326] and reversed at [pos 1673].

---

# §2 Future work (CJ01–CJ27 = FW1–FW27) and drops (DR01–DR06)

Source: `MEET-THM/FUTURE_WORK.md` (reasons verbatim there; 02a §A5.1 quotes the table whole; REG-A rows CJ01–CJ27). Items here get no per-theorem HQ for paper 1. Positions: [pos 1626].

| ID (native) | Item | Reason (abridged from FUTURE_WORK.md) |
|---|---|---|
| CJ01 (FW1) | Frequentist coverage of the exact posterior's credible intervals | Target-theory question outside §5.4 (HQ ruling Q2) |
| CJ02 (FW2) | TV/KL error bound for the final pooled estimate in the masked regime | Not binding (HQ ruling Q3); needs V11 or N10, both OPEN |
| CJ03 (FW3, K13) | Start-mode consistency under orthogonal blocks and a σ²-inflated beta-min margin | Needs TG4-type probability bounds not supplied |
| CJ04 (FW4, K24) | Polynomial mixing of the φ = 1 round (Yang–Wainwright–Jordan transfer); production mixing; masked population accuracy (N10) | N10 OPEN; YWJ/ZYVR route blocked as stated |
| CJ05 (FW5, K23) | Dirichlet/spectral comparison of the random-order round with the random-scan mixture | Only consumer is K24; Seat C dissents (DS02 (Dissent K23)); optional citation as CL22 |
| CJ06 (FW6, K31, N5(b)) | As-coded masked stage count (Conjecture P OPEN); rebuild convergence, P(S₀ ∈ V), P(schedule_limit), calibration-failure probabilities | Conjecture P OPEN; V's complement never inspected (I9(d)); successful-grid properties do not prove successful calibration |
| CJ07 (FW7, K58) | Masked consistency of the equal-weight PIP/MPM | Reduces to population delivery; FMP-DELIVPOP OPEN |
| CJ08 (FW8, K57) | General fixed-budget equal-weight accuracy (only P1 ships in TH17) | Bias bound does not close estimator accuracy; dissent DS06 (Dissent K57) |
| CJ09 (FW9, K59) | R vs N at fixed total particles | PROOF SKETCH only |
| CJ10 (FW10, K71) | (b1-LH-iid) on LH with iid final draws | GAP; T38-b1-LH-iidfail XF ERROR |
| CJ11 (FW11, K75) | NP-completeness of the global-certificate decision problem | Needs a score-specific reduction |
| CJ12 (FW12, K92) | Separation from single-chain flip/swap MCMC (moat construction) | Moat construction and accuracy-matched comparator unproved |
| CJ13 (FW13, K82) | Delivery, P(U) → 0; resource-failure laws | No route; output theorems stated jointly with 𝒪 in liminf form |
| CJ14 (FW14, K94) | Finite-n bound on the posterior-miss probability Π(X) | Envelope GAP (API-N200 brackets only) |
| CJ15 (FW15, K99) | k-way barrier for cross-block masked contrasts | Quantitative barrier unproved (qualitative remark in TH18) |
| CJ16 (FW16, K107, N16) | Validated arithmetic / rounding-error bound | N16 OPEN; T33-errbound COUNTEREXAMPLE |
| CJ17 (FW17, K80) | Positive power of E1/E2/E3 and low_empirical_ESS flags | Heuristics by decision |
| CJ18 (FW18, N12) | Exponential p: contraction and selection (Song–Liang Cor 1) | No completed prior-tail/contraction route; p ≤ n^A stays in scope |
| CJ19 (FW19, N11/N12) | Growing support and cap non-binding | Fixed-support LH does not discharge it |
| CJ20 (FW20) | Hellinger / predictive contraction (Song–Liang Thm 1) | Not delivered |
| CJ21 (FW21, K97) | Song–Liang analytic separation | Iteration-uniform null-BF/prior-odds step NOT REPAIRED (W2PC1); LIT-PAR G4 cited as numerical evidence; scout HQ recommended (P2) |
| CJ22 (FW22) | Sharp ε-scale necessity for §5.3 | All three seat forms COUNTEREXAMPLE; scale disclosure ships |
| CJ23 (FW23, K29) | Favourable O(1) stage law, unconditional | (LL)/over-tilted q_w input is not a model/design condition; S-STGI dissolved (TH21; DS03) |
| CJ24 (FW24, N4(iii)/V11) | Useful two-sided masked evidence precision | V11 OPEN |
| CJ25 (FW25, N8, K71) | Random/adaptive partition quality; study packing (PART-pairing, g = 5, 2g ≤ B) | PART-pairing OPEN; the study design is not the LH exhibit |
| CJ26 (FW26) | Finite-n Gibbs discovery (HPM residual) | ThmB-T24 vacuous at n = 200; no route |
| CJ27 (FW27) | Unbounded functionals: integrability extensions of M1 (§13.1) | M1 is stated for bounded h ∈ [0,1] |

Drops (REG-A): DR01 (K12) "A test oracle, not a guarantee"; DR02 (K34) "TI evidence is not in the method (the Ĵ half ships as reporting, S-REP)"; DR03 (K66) "PARTLY-FALSE (C3-PGD, CEX-localmax(A2))"; DR04 (K67) "Relies on K66"; DR05 (K91) "No accuracy-matched comparator; OPW2-cex"; DR06 (K98) "KNOWN-FALSE (SHARE-M(b), FD-NM)". Recorded dissents on placements: DS01 (K33), DS02 (K23), DS03 (K29/S-STGI), DS04 (K30), DS05 (K70), DS06 (K57).

Also not in FUTURE_WORK but dispositioned "outside the fixed method": adaptive/overlapping partitions and the backfit/residualised start (REG-B CJ162, "candidate, unproven … recorded as future work"); the harder results HQ listed at [pos 1348]: two-sided evidence bounds under masking, PIP consistency under masking, delivery, finite-n posterior-miss bound, R-vs-N, calibration convergence, as-coded masked stage law, iid separation, exponential-p scope, TV/KL and coverage.

---

# §3 The 17 obligations (OB01–OB17 = N1–N17)

Source: `MEET-v31/THEOREM_REVISION_INPUTS.md` §3; final placement `MEET-THM/COVERAGE_MATRIX.md` §(d); REG-A rows. Positions [pos 1280], [pos 1290].

| ID (native) | Obligation | Status (REG-A, verbatim) | Next action implied |
|---|---|---|---|
| OB01 (N1) | Measured-round island identity for general bounded h (Theorem H crux; V1(a2)) | "PROOF SKETCH; PC1 claim 3 takes it as a premise. Binding §13.1: if it fails the goal is not met by withdrawal; HQ escalates to Felipe" | M1 HQ wave 1 ("N1 (binding §13.1) is the longest pole and starts first") |
| OB02 (N2) | Integrated v3.1 core: Prop W, W-cal, LS0, stacking, GUARD-W | "Lemma S PROVED. (a) PROVED by code reading, executed on smoke + 3/3 designs. (b) PROVED by code reading, not executed. (c) not in the production core. (d) PROVED (PC1 claim 6, deterministic). (e) not audited" | W-cal replay; merged-LS0 replay; GUARD-W audit (§5) |
| OB03 (N3) | LS0-based T38(b1-LH) about the shipped method; e4 tie-DP invariant | "(b1-LH) PROVED (candidate), XF VERIFIED (A-REV8) for 'v3 + LS0'; bridge to code = N2(c), not done. DP invariant OPEN" | M5 HQ (wave 3) |
| OB04 (N4) | Finite-R accuracy of Ẑ-weighted PIP and μ̂(h); constant M under masking | "(i) PROVED, given N1 …; (ii) PROVED (candidate); (iii) Obligation: CONJECTURE, OPEN for c ≥ 2" | (iii) = CJ24 / V11 |
| OB05 (N5) | Calibration contract | "(a) assembly of T12/T31(i) …, IND-T …, Lemma RO; (b) OPEN" | (b) = CJ06 |
| OB06 (N6) | Output-event coverage statements | "(a) PROVED (potential run; output form CORRECT WITH AMENDMENT). (b) PROVED modulo premise (i), whose GUARD-W part is the code-audit obligation N2(e)" | GUARD-W audit |
| OB07 (N7) | Certificate card G1/G2/L/R | "G1 PROVED; G2 PROVED; L1 CORRECT WITH AMENDMENT; L2 PROVED; L3 amended form PROVED; R PROVED with amendments; Card bound (C6) PROVED modulo premise (i); C6′ PROVED. Open sub-obligation SC(η_F)/VAL-FP (N16)" | VAL-FP |
| OB08 (N8) | PART-pairing for the study generator g = 5 (2g ≤ B) | "OPEN; Prop Q PROOF SKETCH; W7-PART CE2 COUNTEREXAMPLE" | = CJ25 |
| OB09 (N9) | V5 kernel reversibility, self-adjointness, exact start sampler (closure gate) | "gate closed: N9-KERNEL 'PROVED (candidate)' with exact numerical verification on production headers ([pos 1550]: 7 sub-claims; [pos 1593]: 8 sub-claims); cross-family VERIFIED WITH AMENDMENT (CHK_INHERITED)" — **UNCERTAIN:** 7 vs 8 sub-claims (02a §A7 U6) | LP-FOUND |
| OB10 (N10) | V10: L = max(4, ⌈log₂(n+1)⌉) terminal rounds vs mixing time | "NONE / OPEN" | = CJ04 |
| OB11 (N11) | ℓ = ⌈log₂(n+p+1)⌉ ≥ max{Φ(S°) − 1, 0}; caps not binding w.p. → 1 | "on LH with c ≤ s₀ fixed, 'eventually true' (elementary, unchecked); growing s₀: OPEN" | = CJ19 |
| OB12 (N12) | General (n, p) scope, per regime | "p ≤ e^{Cn^α}: OPEN, not impossible" | = CJ18 |
| OB13 (N13) | Retention lemma | "PROVED (PC1 claim 5; R2C D7)" | closed (TH04.c) |
| OB14 (N14) | Stacking statements | "(a) PROVED (PC1 claim 6); (c) code audit, not done" | IND-T audit (§5) |
| OB15 (N15) | Work and depth at the implemented level | "Prop D PROVED (counting); calibration share seat-derived (R2A, R2B), not proof-checked" | M8 HQ; timing tabulation |
| OB16 (N16) | Floating-point contract SC(η_F), VAL-FP(η, ε) | "OPEN. VAL-FP MEASURED at p ≤ 40 only" | = CJ16 |
| OB17 (N17) | Analytic bounds on Z and π(Ŝ) | "PROVED (PC1 claim 1; PC2 C1(c))" | closed (TH04.d) |

---

# §4 Open conflicts and UNCERTAIN items

## 4.1 From 02a §A7 (final state; numbering U1–U14 as in 02a)
- U1: second growth rate (ii) R′_n = 4⌈(n+p)⁶/4⌉: MINUTES, AMENDMENT_HQ_02_DEFINITIONS §B and NOTATION say "two optional rates"; HQ adopted only (i) as a method setting, (ii) "only as a sufficient rate inside the theorem". How the final M1 states (ii) is not recorded; the task text paraphrases it as "R′ ≥ c(n+p)⁶".
- U2: draft list "19 items" ([pos 1280], [pos 1302], [pos 1201]) vs "24 entries, not 19" ([pos 1492]; MINUTES §1 uses 24).
- U3: three counts of "inherent limitations" (MINUTES §5: 9; THEOREM_REVISION_INPUTS §4.A: I1–I7, I9–I11; FOR_FELIPE_FINAL_METHOD §4: 7). Registered: the MINUTES nine (LIM01–LIM09).
- U4: M1 K-ID header differs between card and MINUTES §2.1 (registry follows MINUTES).
- U5: M5 δ₁ defined as an expectation then used pointwise; integration note 4 (CLOSE_AUDIT #7) fixes pointwise reading.
- U6: N9 sub-claims 7 ([pos 1550]; MEET-v31 MINUTES §9) vs 8 ([pos 1593]).
- U7: S-STGI/K29/K30 propagation: treat "K30 = M7(d); K29 = FW23 (CJ23)" as final; REGISTRY_PAPER1.md not re-audited.
- U8: label N2(b) (W-cal) is defined in THEOREM_REVISION_INPUTS (on MEET-v31), not in the R3 files.
- U9: line-number drift in FUTURE_WORK citations (content identical).
- U10: supplement-card order differs between MINUTES §2.2 and the TLF header table (IDs follow the TLF order).
- U11: "Seat D" is "fresh-eyes Fable" in FOR_FELIPE and [pos 1584]; NOTATION lists the seats as A (Fable 5.1), B (Fable 5.1), C (gpt-6-astra), D (Fable 5.1).
- U12: METH31 header "Not yet approved by HQ or Felipe" predates approvals; Felipe's approval of the theorem list is **not recorded**.
- U13: seat-checker names: the task text calls the waves "Sol" and "Opus"; files call them PC1 (gpt-6.1-sol on Seats A, B, D) and PC2 (Opus 5.5 on Seat C); CHK = PC1.
- U14: date of Felipe's island-level depth decision (METH31 §3 says 2026-11-03; transcript: proposed [pos 1263] and [pos 1302], approved [pos 1304] on 2026-11-04T00:05Z).

## 4.2 From 03 (empirical and bookkeeping)
- Concurrency "32 islands within 2e-4": only S1 (max ΔPIP 2e-4); S4 2.3e-3, S5 7e-4; log Z gaps 0.027, 0.012, 0.47 nats (03 §2.5).
- Favourable count of the unmodified v3 start: 0/2,400 (API-RESID) vs 1/2,394 (O-DILUTE §1) (03 §2.4).
- Thresholds for "favourable from n": 590–730 (O-DILUTE), 800–1,600 (W3-VEXP), 1,050–3,200 (W5-FAVIID); other numerical inconsistencies in `W8-SYNTH/SYNTHESIS.md` §4.13: start mode misses "6–12 of 14" vs "holds 2.5–6 of 14" vs "7 of 14 masked"; beta-min shortfall ≥ 43× vs "about 100×" (old); SE columns ≤ 114 vs 215–229; stopped fits 6 vs 4 (O-SWAP); LS0 cost "about ℓ·p" vs 1 + (ℓ+1)·max_k[p + k(p−k)] (≈ 1.7·10⁵ at p = 1,000); terminal segment L+4 vs L+5 (resolved: both right for different boundaries). Recommendation there: use S-ELS for counts, O-DILUTE for start masses, W6-FIXREV1 for LS0 cost, drop or attribute the "favourable from n ≈ …" threshold.
- Cloud credits $245 vs $250; $21 (LEDGER) vs $19 ([pos 1673]); API spend by run (≈ $31 for 7 measured runs + others) vs the implied $79 ($200 − $121) (03 §2.13).
- Lean "101 declarations" vs "101 theorems/results"; 56 audited for axioms (03 §1.4).
- Conflict counts 26 (REGISTRY_v2) vs 37 (MEET-THM registrar index) (03 §1.3).
- HQ's SSL numbers (569/582) vs SSL-RS (suppl.) 593/592 at c = 1 (03 §2.1).
- Venue view shifts ([pos 933] → [pos 1009]) (03 §3.4).
- Whether `T11Miss.lean` is reused for TH06.a: not stated (03 §1.1).
- PR #1 and LH-SCALE resolution not recorded (§1 P11).

## 4.3 Registry conflicts C1–C26 (02b Part II P.1; REGISTRY_v2 §A2; all "both sides recorded", none closed by a new review unless stated)
- C1 Lemma0(b) [RF167], R2-dichotomy [RF168]: W1-T37R PROVED vs W3-VT37R/A-REV2 ERROR; W6-FIXREV2 replaces by Lemma 0(b′) and three-way Prop. F (same-family, unreviewed).
- C2 TDP-iff-DS [RF169]: SF VERIFIED vs XF ERROR (ties); W6-FIXREV2 Lemma T + Lemma NT.
- C3 PropU [TH227]: SF VERIFIED (bookkeeping) vs XF ERROR; Theorem B unaffected.
- C4 LemmaS-attain [LM174]: "tight" claim VERIFIED vs XF ERROR on full domain; the inequality itself VERIFIED.
- C5 E3(ii) [RF188]: SF VERIFIED vs XF ERROR (omits q < 1).
- C6 EXP-const [RF134]: 0.52/c_* vs actual 0.51/c_*; finite bound unaffected.
- C7 Thm4-iff [RF135]: "iff" gloss ERROR; VEXP's added claim not justified.
- C8 T38b-R(whole) [TH241]: SF VERIFIED whole vs A-REV1 GAP (superseded by W6-FIXREV1 files, see C11).
- C9 ORTH-joint [CJ210], T26-PropC [TH325]: PROOF SKETCH (weaker) recorded.
- C10 Thm2-BO label mismatch (author PROOF SKETCH kept).
- C11 T38-(0) [TH281]/T38b-R(whole): scope of A-REV1 (reviewed W1-T38E, not W4-T38FULL); W6-FIXREV1 supersedes.
- C12 Lemma0(a,c) [LM144]: wording dispute on "initial centre is the truth".
- C13 Version W1-T37R: reviewed at d492f22 (unfinished REPORT) vs 3bcc429; PROOF.md identical.
- C14 Legend ARCHITECTURE: F-REFINE "[P]" is same-family only.
- C15 ThmW [TH204] vs VPGD-PropT [TH217]: Theorem W (region form) fails with an exact tie on masked LH (c ≥ 2); lattice form W_Lat holds.
- C16 PXN-P6 [TH153]: W5-VMASK verified vs A-REV3 GAP (A-REV3 did not read W5-VMASK).
- C17 SHARE-M(b) [RF203], SHARE-B2W4 [TH254]: PROOF SKETCH/upgrade vs A-REV3 ERROR.
- C18 Cost-T38 [TH289], T32(i) [CJ112]: stale CONJECTURE labels vs W5-LOCKBOOK PROVED (same family only).
- C19 SEP-E [TH386]: same staleness.
- C20 T38-b1′ [TH285], T38-b2 [TH286], OBG-T38b-BG3 [TH263], FSH-T38b2 [TH267], B2E-D2LH [TH269]: no-LS0 masked candidates on LH, none XF reviewed at the time (later A-REV7).
- C21 OCERT-§4: O-VCERT "§4 empty" vs later illustration (not reviewed).
- C22 STG-Wp [TH367]: O-STAGES Cor. W′ rests on (LL) vs O-WSTAB COUNTEREXAMPLE on the divergent side.
- C23 OMIX-C1 [TH183]: common plug-in σ² vs O-DILUTE/F-SIGMA; rejected (E-SPINE §2.2).
- C24 T38-b1-LH [TH287], T38-b1-LH-iidfail [RF217]: A-REV5 ERROR vs A-REV8 GAP on "Q_fπ₀(S₀) → 0 when c ≥ 2".
- C25 SEP-GU [TH388]: A-REV7 VERIFIED vs A-REV9 GAP (import not re-audited).
- C26 LH-LAT [TH293], LH-LAT-sharp [RF144]: m₀ "sharp" false on 32/94 heterogeneous settings; exact margin formula R5.
- Plus: W8-SYNTH §4 (15 conflict groups, 02b P.4); retired/refuted checklist (02b P.2); UNCERTAIN markers by the theme authors (02b P.5, e.g. BASIN used for two different objects; "D18" low-p finding not in the snapshots; P8 counterexample identity; label-collision proposals 02b P.3 / W8-SYNTH §4.15).
- Standing: repairs of Claude results found wrong by Astra "have not been re-checked by Astra" for those not covered by A-REV5–A-REV9 ([pos 796]).

---

# §5 Engineering TODOs

Source: `MEET-v31/METHOD_v3.1_FINAL.md` §6 ("None of these can change a method decision … Each one gates only the claim named") and "Points settled by the chair" (02a §A1.12); MD06; `MEET-v31/FOR_FELIPE_FINAL_METHOD.md`.

| # | TODO | Gates which claim | Status in sources |
|---|---|---|---|
| E1 | **W-cal**: bitwise replay of `v3_calibrate` with concurrent diagnostic islands on the 3 replay designs (S1 r001, S4 r001, S5 r002), about 1 h on Owls with the METH-AUDIT harness | "bitwise" for the calibration; any wall-clock claim (calibration is on the critical path); REG-B TH395 (Prop W-cal) | not executed |
| E2 | **LS0 merge into the production core** plus merged-LS0 replay (integrated core vs the O-LS0 export on the 3 designs: HPM, stores, flags, E3 unchanged, `ls0_improved`, stream endpoints, a deterministic eviction/tie example) | "LS0 is in the shipped core"; T38(b1-LH) as a theorem about the shipped method (OB02(c), OB03); REG-B CJ178 (LS0-4) | API-AUDIT: "LS0 exists only in a test export, not the production code" ([pos 1009]); MD03 decides LS0 in the shipped core |
| E3 | **Stop-handling / GUARD-W audit**: worker, merge and LS0 paths satisfy "any worker stop, LS0 stop or guard stop ⇒ no output"; API-AUDIT's forced-stop table (10 fits) after the `log_Z` NA fix | premise (i) of G2 and of every P{𝒪, ·} statement (OB02(e), OB06(b)) | open; API-AUDIT: SR, GUARD, scan-before-limit, IND-T hold ("four of the five code properties hold") |
| E4 | **IND-T for streams 10..9+R′**: independence of final streams from calibration streams for every declared R′ | stacking theorems; frozen-𝓒 contract (OB14(c)) | not done |
| E5 | **VAL-FP at production size**: long-double replay on 2 study designs at p = 500 (measured only at p ≤ 40); validated arithmetic SC | removal of the label "numerical implementation of an exact-arithmetic certificate" (OB16, CJ16) | open; "a long-double replay alone is not enough" |
| E6 | Preflight fixes (e6) and an allocation audit of concurrent peak memory and stop behaviour | `resource_limit` estimates labelled "estimate" | open |
| E7 | Checked arithmetic (e7): boundary tests for integer, stream-id and allocation overflow | support at huge (n, p); status `unsupported_size` | open |
| E8 | **Full Ẑ-weighted PIP rescoring of all 2,394 fits on NOTS/laptop bundles** (`pip_rescore.R` `score_one()` over `SMCBVS.rds`; no refit; about 2,394 small reads), with R_eff per fit | Ẑ-weighted primary PIP and MPM_Ẑ for the 2,400 fits (MD08); A's D5 reversal criterion | only 3 designs done (max ΔPIP 1.29e-3); HQ planned copying per-fit summaries to Owls ([pos 1302]), not confirmed done |
| E9 | **Calibration timing tabulation** (`timings$calibration`, `timings$final`, rebuilds, tier, T from ≤ 20 saved fits; Owls ≤ 8 cores, read-only) | cost wording (§2 #19); the 0.46/0.67/1.69 vs 0.45/0.62/1.76 formula (03 §2.9) | open |
| E10 | e4 tie-DP invariant (N3) and n = 2 boundary tests (e3) | LS0 under truncation; n = 2 support | open (OB03) |
| E11 | **Certificate card on saved fits**: "computable wherever the saved top store exists (NOTS bundles; HQ action), otherwise not claimed"; C5 screening event {S₀ ⊆ U(X,y,Ŝ)} over the 2,400 fits (REG-B CJ238); per-dataset matching of O-SWAP realised check with SMC outputs | certificate statements on study fits; per-fit certified discovery term | open |
| E12 | **Per-particle random streams (C6) — trigger**: implemented and law-checked iff paper 1 claims particle-parallel depth **or** demonstrates any fit with p > 2,500 (union trigger, HQ disposition); Felipe: island-level depth only, study p ≤ 1,000, so neither trigger currently fires (MD06). LAW-PRESERVING, not bitwise | particle-parallel depth claim (v3.2) | not triggered |
| E13 | **XᵀX-free scorer (C7)**: Gram-free scoring, declared v3.2 path with C6; a private 8p² Gram per worker is "not inherent" (LIM02) | scalability beyond p ≈ 2,500; ceilings Θ(p²) memory (TH08.e) | v3.2 path |
| E14 | Joint summaries (pair inclusion, model size): "need a small new run, because those particles weren't saved" (FOR_FELIPE_FINAL_METHOD §1) | joint-h accuracy numerics (TH01.g) | open |
| E15 | Reporting fields of AMENDMENT_HQ_02 (Ĵ, ε̂_× with companions, d in 𝓗, read-only accumulator): recorded on theory/MEET-v31 @ 6a80fe5 | TH19 (S-REP) reporting | **UNCERTAIN:** implementation in the code is not recorded |
| E16 | Data caveat: Owls regeneration ≠ NOTS bits (F(S₀) agrees to 5e-8; `data_hash_check.csv`: "5/7 match=FALSE rows" to be interpreted, W8-SYNTH §8 task 3) | any claim mixing Owls and NOTS records | **UNCERTAIN:** interpretation not recorded |
| E17 | Reproducible record for ABL-CONF fits: raw per-fit CSVs live outside git for O-LS0 (§8 of its report); the NOTS reorganisation (`projects/BVS`) is where v3 scripts and results will sit | all empirical claims | in progress ([pos 1673]) |

---

# §6 Planned next steps

## 6.1 Theorem work: per-theorem HQs (after Felipe's approval, P1)
- Charters: `MEET-THM/HQ_CHARTERS/M1.md … M8.md` (8 main-theorem charters, verbatim from the seats' §S3(c)) and 5 lemma-pack charters `LP-FOUND.md`, `LP-IDENT.md`, `LP-AUDIT.md`, `LP-REST.md`, `LP-REP.md`. Each has the wave, covered K-IDs, dependencies (A/B/C/D §S3(a) edge lists), Lean core, risks, numerical companion (≤ 20 seeds) and fallback (IC7 "narrowest supported form"; CLOSE_AUDIT #8: S-CERT's deterministic perturbation fallback and S-LEAK's finite-law identity fallback must be named explicitly in LP-AUDIT and LP-REP).
- Waves (MINUTES §2.5, verbatim):

| Wave | HQs | Reason |
|---|---|---|
| 1 | **M1** V/H; **M3** START; **LP-FOUND** = S-TARGET + S-BLOCKS + S-KERNEL (+ S-T cited) | Foundations. N1 (binding §13.1) is the longest pole and starts first |
| 2 | **M2** WS (binding §5.3); **M7** STG; **M6** SEP + KL; **LP-IDENT** = S-IDENT | The §5.3 package and its inputs (d_σ from M3, the count from M7, the lower bound from M6) |
| 3 | **M5** HPM; **M4** Z𝒯 + masked statement; **M8** Prop D; **LP-AUDIT** = S-CERT + S-OUT | Code-audit wave: N2, N3, LS0, GUARD-W and the DAG serve M5, M4 and M8 together. M4(f) needs M5 |
| 4 | **LP-REST** = S-Z + S-POOL + S-LIM; **LP-REP** = S-REP + S-LEAK | Consequences and reporting corollaries. Nothing binding waits on them |

- Mapping to IDs: M1 = TH01, M2 = TH02, M3 = TH03, M4 = TH04, M5 = TH05, M6 = TH06, M7 = TH07, M8 = TH08; LP-FOUND = TH10 (S-TARGET) + TH11 (S-BLOCKS) + TH12 (S-KERNEL) (+ TH09 cited); LP-IDENT = TH13; LP-AUDIT = TH14 (S-CERT) + TH15 (S-OUT); LP-REST = TH16 (S-Z) + TH17 (S-POOL) + TH18 (S-LIM); LP-REP = TH19 (S-REP) + TH20 (S-LEAK).
- Process rules to carry over: each HQ "loops all the way to Lean"; waves of 3–4 because subscriptions cannot run 14 HQs at once ([pos 1348]); cross-family check on every claim; batch math claims into one proof check; label every self-proved claim "unchecked"; freeze the agenda before dispatch; cap seat output (method-meeting format fixes, [pos 1302]).
- Scout HQ on the Song–Liang separation alongside wave 1 if approved (P2). If it succeeds: a ninth main theorem.
- Order of 22 theorems estimate ([pos 1348]): about 14 for paper 1 (resolved into the 8 + 12 structure), about 8 harder ones to follow.
- Lean: extend sorry-free coverage per the "Lean core" rows (T12 `hstep` discharge for multinomial resampling is the first named target; `L-LEAN/T12_PLAN.md`), keep `stmtdiff.py` frozen-statement check; Astra/Fable fidelity checks per file.
- Checkpoint plan ([pos 1015], [pos 1018]): version 1 = Biometrika paper; "The key results get Lean certificates"; harder results after.

## 6.2 Simulation and empirical program
- **LH-SCALE** (NOTS Slurm proposal; = F-REFEREE R2; `W8-SYNTH/SYNTHESIS.md` §8 task 5; `F-REFEREE/RESPONSE_PLAN.md` R2): production code on the LH family at growing n. Design: "3 × 4 × 2 × 100 fits; n ∈ {400, 1600, 6400, 25600}; g = 9; ρ ∈ {0.6, 0.85}; ψ ∈ {0.3, 0.5}; s₀ = 2c + 4; v3 as run, plus LS0 post hoc with `emit_centre = true`" (about 2,400 fits). Report P(Ŝ = S₀), which mechanism first scored S₀ (pilot, bridge Gibbs, terminal, LS0), π₀(S₀) against the T27 rate, stage counts. (ρ, ψ) = (0.85, 0.5) is where STAB-LH fails, so it doubles as a stress test. Awaiting Felipe's OK ([pos 824]); needs NOTS.
- **Real data** and **head-to-head comparisons** (LIT-VENUE expectations not yet met): PARNI, MAdaSub, TGS (LIT-MH), SuSiE, SSL, and **Song–Liang** (split-and-merge) numerics; simulations at growing n; "a main theorem not tied to the constructed LH family". No Ẑ/PIP head-to-head against other Bayesian methods exists ([pos 933]).
- Exact-recovery pitch: not "beats everything": SMC-BVS is behind SuSiE/SSL at c = 1 (559/560 vs 585/582) and clearly best at c = 0.5 (370/340 vs at most 303/255) (03 §2.1); explain the c = 0.5 advantage (same-size swaps, T07 ceiling) and the c = 1 superset misses as posterior-target facts.
- Pending quantitative bookkeeping: C5 screening event on the 2,400 fits; per-dataset N200 matching; `Π(X)` upper bound (CJ14).
- Reduce/clarify the n = 200 disclosure: "beta-min fails by 43× (not 100×), thresholds near n ≈ 2·10⁶, 0 search misses, 6 stopped fits" ([pos 796]).
- Optional method-side investment (not decided): residualised start (CJ162); HQ said it "attacks the method's main weakness at its source" ([pos 937]) but it remains an unproven candidate; MEET-v31 item 1 rejected it for paper 1.

## 6.3 Referees and review
- **Sol 6.1 as a second referee / auditor**: Sol 1 (proof check) and Sol 2 (audit) were used on the method documents and Sol 6.1 as auditor and PC1 checker in the theorem meeting ([pos 1480], [pos 1584], `MEET-THM/CLOSE_AUDIT.md`). The task brief lists "Sol as a second referee" as a next step; the sources do not record a plan beyond HQ's earlier offer "If you want to try Sol, I'd add it as a fourth seat or as a proof checker, not as a replacement for Astra" ([pos 1302]). Cross-family re-check of Claude repairs by Astra is still outstanding for repairs not covered by A-REV5–9 (`campaign/LEDGER.md`; [pos 796]).
- External human review of proofs is absent (LIT-VENUE): everything is AI-checked (Claude, Astra/gpt-6-astra, Sol 6.1, Lean on finite cores).

## 6.4 Credits and funding (as of [pos 1673])
- Cloud: remaining $19 (Felipe; **UNCERTAIN** vs $21 in the LEDGER and $245 vs $250 initial); the cloud credits expire 2026-11-05 07:59 UTC (LEDGER header). Cloud runs are Opus 5.5 only; launch with `claude --cloud` (never routines) via `~/.config/bvs-hq/launch_cloud.sh`; the LEDGER at 20:35 UTC says "the launcher … must not be used" after exhaustion.
- API: remaining $121 of the $200 promotional credit, which expires 2026-11-17 and covers the Agent SDK (not the CLI); launcher `~/.config/bvs-hq/launch_api.sh TASK_ID [MODEL] [MAX_USD] [EFFORT]` (hard per-run cap, default $15); daily Console rate limits about 100K Fable / 400K Opus output tokens per day.
- New $200 API credit arrives 2026-11-15 ("we will burn it as well on theory", [pos 987]); HQ's plan: keep about $60 of the first credit to start the per-theorem HQs before Nov 17; the Nov 15 credit "continues them" ([pos 1059]); it funds the deeper theory work after the Phase-2 checkpoint ([pos 989]).
- Subscriptions: Claude Work (CW) and Claude Personal (CP) as complements ("main work is via credits", [pos 1061]); wait for resets on limits; weekly Ultra plan was at 84% at [pos 783].
- Today's instruction ([pos 1673]): use the remaining $19 cloud and $121 API credit.

## 6.5 NOTS reorganisation and the old HQ
- Felipe: "I commanded the old HQ [SMC_BVS Headquarters] to lead a file transfer and reorganization towards NOTS, all scripts, results etc of v3 will be put in projects / BVS, it is on going, feel free to head over there if you need access to those files" ([pos 1673]; thread `thread_mcp-5e4b26e1-e27b-4f82-a11e-f0b274127549-072d63595627ee8a`). Until it completes the new Theory Meta HQ should read that thread for file locations; NOTS paths seen in the sources: `/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_*/results/` (originals, "not deleted"), laptop `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\claude\prod_p{0500,1000}_20261023T1227Z\...`, Owls `/home/fb31/Bayesian-Variable-Selection`, `/home/fb31/ls0_work/`, `/home/fb31/api_workers/`, `/home/fb31/hq_reviews/`, `/home/fb31/fresh_eyes/`.
- Repository state at the archive (git `main`): the `theory/*` branches hold all campaign work; `main` has not been edited by the campaign (E-SPINE amendments live in PR #1, not merged: 02b RF104 note).

---

# §7 Known infrastructure issues and rules (carry over to the new HQ)

1. **T3 server restarts cancel delegated agents** (A-REV1 cancelled at [pos 410]; the Owls guard killed by a restart [pos 603]; O-LS0's original agent cancelled by a T3 restart before writing up; the second ABL relaunch needed because a restart killed the first, `MEET-v31/ITEM1_ABL_START.md`). Rule: long jobs must not depend on the agent session.
2. **systemd-scope kill rule** (root cause of every rc 143 kill, [pos 1584]): "T3 runs each agent in its own system container, and when the agent's session ends it kills everything that agent started; launching jobs 'detached' [`setsid`] doesn't escape that." Fix: launch long jobs as independent `systemd-run --user` units; the rule is in the Owls `POLICY.md` for every agent. Applied to ABL-CONF (killed 01:25 UTC, relaunched 01:29 UTC). The Owls guard was relaunched as a self-restarting systemd service ([pos 603], [pos 611]).
3. **Owls limits and guard** (OWLS-STEWARD, [pos 459]–[pos 479]): all compute through `owls_run`; low priority, single-threaded linear algebra, 2 cores per job by default, 8 cores total; a background guard lowers priority, pauses over-budget jobs and logs; cron `@reboot` entry; `POLICY.md`: "Big work goes to NOTS, one ssh connection at a time"; `owls_run` refuses a fourth job. Incident: Owls' resource monitor flagged the campaign above the 8-core budget (923%) at 18:05 UTC and killed the first ablation jobs ([pos 1251]); system load on Owls is about 550–590 from other users.
4. **Routines vs cloud billing rule**: routines (RemoteTrigger / triggers API) bill the weekly plan, not the cloud credit; only `claude --cloud` sessions bill the credit ([pos 301], [pos 342]); Wave 1 was run as routines.
5. **Agent SDK vs CLI on the promotional API credit**: the $200 promotional credit covers the Agent SDK but not the Claude Code CLI ("Credit balance is too low"); workers must be Agent-SDK based ([pos 894]; LEDGER 21:25 UTC). The org has no payment method on file and a monthly spend limit of $195; the extra-usage toggle risk was flagged ([pos 7], [pos 24]).
6. **64K output-token failure rule**: LH-LOCK (Fable, CW) failed on a 64K-output-token API error before its first commit (LEDGER 21:55 UTC): "tell agents to write long proofs in several files/commits, never one giant response." Related: Console daily rate limits (Fable 100K / Opus 400K output tokens per day) cap parallel runs ([pos 863], [pos 911]).
7. **Thread-launch pitfall**: a meeting thread launched with a branch name that existed only on GitHub failed; relaunch from the GitHub copy; the failed thread is renamed "(failed launch - ignore) Theorems - Final meeting" ([pos 1606]).
8. **Lessons recorded for briefs**: agents' "N/3" type headlines may overclaim (METH-AUDIT 3/3 vs smoke + 1 design until the HQ re-run); wait-for-run agents exit early; stale branch heads can mislead reviews (conflict C13).
9. **Local laptop availability**: the laptop was unreachable for a period ([pos 616]); laptop agents (O-CERT, O-SWAP, O-DILUTE, O-BGIBBS …) ran in the "CP window" ([pos 551]–[pos 807]).
10. **Authority and safeguards**: HQ has "full authority" for method and theorem decisions ([pos 1061]) but never adopts or locks results (adoption/locking is Felipe's decision: REG-B "not adopted" tags, LOCKABLE_v2 header); the burden of proof is on any method change (the "investment rule", [pos 1128]–[pos 1162]); Felipe's preference "Remember to use CW instead of CP" ([pos 1061]).
