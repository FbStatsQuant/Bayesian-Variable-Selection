# MEET-THM · Synthesis of Round 1 and check wave 1 (chair, non-voting) — v2

2026-11-04. **v2 corrects v1** (`SYNTH_R1_v1.md`) per the auditor's report `SYNTH_R1_AUDIT.md` (verdict FAIL, 15 findings). The correction log is in §5.

**Sources.**
- Seat files `R1_A.md`–`R1_D.md`, cited `A:123` (= R1_A.md line 123).
- The clerk's side-by-side `evidence/R1_SIDE_BY_SIDE.md`, cited `SBS:line` or `SBS T#`.
- Check verdicts:
  - `evidence/W1_PC1/VERDICTS.md`, by PC1 (gpt-6.1-sol) on Seats A, B, D, cited `PC1:line`;
  - `evidence/W1_PC2/VERDICTS.md`, by PC2 (Opus 5.5) on Seat C, cited `PC2:line`.
- HQ rulings `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`, cited `HQ:line`.

Candidate IDs are K01–K108 (`R0_DIFF.md`). Nothing here upgrades a status. Check verdicts are about statement sanity: TRUE-AS-WRITTEN means "no counterexample found", not a proof.

## 0. New facts since Round 1

### 0.1 HQ rulings, 2026-11-04 (HQ:4–24), binding on Round 2

**Q1, §5.3 (HQ:4–7).** The bridge form is accepted if paper 1 ships **all** of the following.
- **(a) Discrepancy half.** The divergence between π₀ and π (via d = d_σ + d_X, Jeffreys J, or KL) is controlled by the cross-block dependence terms **plus the explicit σ²-coupling term**, on a genuinely correlated family (ε > 0), **with constants**.
- **(b) Bridge-form stability theorem.** Per-stage χ²/weights, **stage count** and constants are **continuous in ε** around the block-orthogonal baseline, on a genuinely correlated family. IC3 must be exhibited, not asserted.
- **(c) Refutation of the one-shot form** (OWS-WS6(d), WS7), stated as a proposition. It ships only after an independent cross-family check **passes**. If that check fails, the one-shot question reopens with HQ. The correlated-family requirement applies to (a) and (b), not to (c).
- **Failure rule.** If (a) or (b) has no credible route by close, it escalates to HQ as an unmet binding goal. It is never dropped.

**Q2, §5.4 coverage (HQ:9).** Coverage error means |π(C(π̂)) − nominal| for the credible quantities the method reports, plus their Monte Carlo error. Frequentist coverage of the exact posterior → FW1.

**Q3, §5.4 masked TV/KL (HQ:11–16).** Not binding. It is carried as an **obligation with a fallback**:
- The masked final-estimate TV/KL bound → FW2, with **V11 and N10 cited as OPEN**.
- The **reverse-KL obstruction** (infinite on missed support) is stated as a definitional fact.
- The binding part "quantify the approximation error" is met by:
  - the PIP and joint-inclusion bounds;
  - the deterministic reported-posterior TV = 1 − Z_𝒯/Z;
  - the start TV/KL and Lemma KL;
  - the terminal-law and favourable-regime TV results.
- **Requirement:** the list names at least one masked-regime accuracy statement that paper 1 proves.

**Q4, run card (HQ:18–22).** Ĵ and the cross-block leakage proxy are allowed as **reporting**, under these conditions:
- computed **only from quantities the run already has** (X, the blocks, the bridge's existing particles and weights);
- they read **no random numbers**;
- they **never feed back** into calibration, the schedule or the decision (POST HOC);
- they are specified with the **estimator's definition and its numerical label**.

HQ adds them as AMENDMENT_HQ_02 when the definitions are sent at close.

### 0.2 Check wave 1, PC2 on Seat C (PC2:22–45)

Over 56 clauses:
- 54 TRUE-AS-WRITTEN, 2 AMBIGUOUS, 0 COUNTEREXAMPLE, 0 NEEDS-HYPOTHESIS;
- 53 DESIGN-VERIFIED, 2 DESIGN-ASSERTED, 0 DESIGN-FAILS;
- 53 PLAUSIBLE, 3 GAP, 0 IMPLAUSIBLE.

The three GAPs are implementation gaps that Seat C itself flagged: the region-certificate route, the integrated execution DAG, and the LS0/GUARD-W audits.

Three registry qualifiers were omitted (PC2 flag (b)):
- Thm5-LH SAME-FAMILY-ONLY;
- MZ-P3 AUTHOR-ONLY;
- T01 "external review queued".

### 0.3 Check wave 1, PC1 on Seats A, B, D (PC1:7–15)

Over 101 rows:
- 53 TRUE-AS-WRITTEN, 11 COUNTEREXAMPLE, 25 NEEDS-HYPOTHESIS, 12 AMBIGUOUS;
- 71 DESIGN-VERIFIED, 24 DESIGN-ASSERTED, 3 DESIGN-FAILS, 3 NONE-GIVEN;
- 82 PLAUSIBLE, 17 GAP, 2 IMPLAUSIBLE.

The index of adverse rows is at PC1:17–52. §3 lists every repair it implies.

### 0.4 §5.3, what the checks established and what they did not

**Seat C's bound (PC2:47–63).**
- osc d ≤ D_*: no counterexample in 124 exact cases at p ≤ 10 (PC2:48–50). D_* is the design-computable quantity built from a, δ_A, δ_H, r (C:349–351).
- On a coded-grid replica (1,600 islands, good and poor V), every island's W lay pathwise in [e^{−osc d}, e^{osc d}] (PC2:53–54); with E W = 1 this gives the moment statement M₂ ≤ e^{D_*} on every successful coded grid (PC2:55, 125). Both remain Seat C's PROOF SKETCH.

**On the examined exhibit family** — one coefficient n^{−1/4} in each of two groups, σ² = 1, so signal energy is of order √n (C:364) — PC2 observed:
- D_* is O(1) up to ε ≈ n^{−1/2}/p and grows at fixed ε;
- the true osc d also grows, roughly like √n·ε at fixed p (`d14_bound.py`; PC2:56–61).

Scope of that observation:
- It is **numerical evidence on that family and those assumptions, not a proved necessity statement** (PC2:63 qualifies it "with signal energy O(√n)").
- A finite bound remains **valid** at any ε where its hypotheses hold. What the evidence suggests is that its constants are **useful (O(1))** only at small ε.
- Whether this is intrinsic is a question for Round 2 (a candidate necessity proposition; R2.3).

**Seat B is not perturbative.** Seat B's route explicitly is **not** a perturbation of the orthogonal case: it goes through cross-block leakage CBL(η) and effective beta-min (B:499, 505).
- PC1 found its favourable clause (F) and its every-grid χ² clause (S) TRUE-AS-WRITTEN, with design verified (PC1:143–144).
- But its necessity clause (N) has a COUNTEREXAMPLE (PC1:147), and its new q₂ lemma route is IMPLAUSIBLE as stated (PC1:145).
- So "every true form is perturbative" (v1) was wrong. Leakage-based clauses are on a different scale.

**Seats A and D.**
- Their finite-η perturbation inequalities are TRUE-AS-WRITTEN on PC1's design Dε, with cross-correlation 10⁻⁵–10⁻⁴ (PC1:136, 149).
- Their named exhibits fail: the method's B = 2 splits the four-variable groups, and D has δ > 1 at ε = 0.1 (PC1:142, 152).
- A's "(c) hence within" variance transfer is a COUNTEREXAMPLE (PC1:138).
- D's stage-count sandwich M10(iii) (aliased in M11(b)) has the wrong order; the correct order is T_bd(.9e^{−4η}) ≤ T_true(.9) ≤ T_bd(.9e^{4η}) (PC1:150).

### 0.5 Ground rule 6 (PC1 "Ground rule 6"; PC2:64–67)

- The growth premises on R_n/M_n in A.C5(d), B.D2(f) and D.M2(d) are sampler conditions, not model/design conditions.
- Seat C's finite-R bounds in D1/D15 are vacuous at the shipped R′ = 4. They are informative only under stacking, with R′ growing (a declared rate, per ground rule 5).

## 1. Per agenda item: agreement and disagreement

**Item 1, coverage sweep (SBS T8).**
- The **mappings** coincide: Song–Liang Thms 1–3 and Thm S → K93 plus K68–K72; Thm 4/Cor 2 → K10/K17/K18 (+K97); §6 → K87/K88 (+K90 for A, B, D) (A:34–40, B:36–42, C:52–59, D:51–58).
- The **verdicts on those mappings differ.**
  - C: K93 establishes selection concentration, **"not their Hellinger contraction theorem … Do not mark this 'exceeded'"** (C:52).
  - C: the start results "do not replace general KL-projection theory" for Thm 4 (C:55).
  - Hellinger/predictive contraction is future work for C and D (C:52, D:51).
  - This is row D15 in §2.
- Cor 1 (p up to e^{Cn^α}) is not delivered: N12 is OPEN (A:38, B:38, C:56, D:53). → agenda 9.
- **Proposal goals:** HQ Q1–Q3 fix §5.3/§5.4. §5.1/§5.2 → the validity cluster; §13.1 → K46/K51 (the N1 crux).
- **THM-INV §1 cells are not uniformly agreed.** Flag power (K80), spectral comparison (K23) and validated numerics (K107) get conflicting dispositions (row D16).

**Item 2, the draft list (SBS T1).**
- All four seats give the same verdict on 7 entries: A1 keep, D4 defer, S2 keep, S3 drop, R1 keep, R2 demote to cited lemma, R7 defer.
- Of the 17 "differs" rows, several differ only in merge wording. The substantive ones are in §2.

**Item 3, new candidates (SBS T2).**
- 33 of 108 K-IDs have identical placement.
- The core that all four place in main at **clause level** (corrected per audit finding 10):
  - start: K10, K15, K17, K18;
  - SEP and Lemma KL: K19, K105, K106;
  - Z𝒯 and certificates: K42, K43, K45;
  - general-h identity and Theorem H: K46, K48, K50, K51, K52;
  - reported HPM and composition: K65, K68, K69, K72;
  - §5.3: K102.
- K16 (the favourable rate) is **supplementary for A, B and D** (A:299, B:224, D:257) and a cited lemma for C (C:121; SBS:67), so it is not a main-core item.
- Unanimous drops: K66, K91, K98. Unanimous future work: K13, K24, K58, K75, K92.

**Item 4, §5.3.**
- All four ship a bridge form (SBS T4), which HQ accepts under conditions (a)–(c).
- The statements differ in kind: perturbative (A, D), design-computable energy bound (C), leakage-based (B).
- Their scales and their failures are in §0.4, and in row D4.

**Item 5, §5.4.**
- Settled in substance by HQ Q2/Q3 (SBS T5).
- Open in Round 2:
  - the masked-regime statement HQ requires (D12);
  - the coverage-wording repairs (§3, cluster 16).

**Item 8, fidelity.**
- PC1's registry ledger (PC1:75–103, S1–S23) is the meeting's fidelity record, and seats carry its qualifiers verbatim:
  - no-LS0 and IID variants are labelled as variants;
  - ideal grid vs coded grid;
  - W-cal not executed;
  - GUARD-W and N3/e4 are audit gates;
  - general LH locking is XF ERROR (A-REV7).
- Plus PC2's three omitted qualifiers (§0.2).

## 2. Disagreement table (Round 2 answers row by row)

| # | Item | Positions | Crux | Settled by |
|---|---|---|---|---|
| D1 | Validity cluster K08, K20, K21, K32, K35, K46 | All four cite the standard SMC identities as lemmas. They differ on the package. A: main card C2 "VALID" (A:84). B: main "Proposition V+", with K20/K21/K08 cited and the general-h identity N1 as content (B:79, 662), plus a supplement KERNEL card (B:675). D: main "Theorem V": N9 lemma + frozen-𝓒 contract + islandwise identities (D:88). C: cited lemmas; only the measured-record extension K46 is new (C:80) | Which clauses are method-specific (N1, the N9 kernel facts, the frozen-calibration contract) and which are KNOWN—CITE; whether that content is a main theorem or a proposition | Each seat lists the clauses that are not cited lemmas; the chair applies IC4; the N9 cross-family check (running) |
| D2 | Thesis theorem CD, K96 | A, B, D: main assembly (A:94, B:89, D:98). C: drop as a theorem; a scoped paragraph (C:90) | Does CD state anything not implied by its parts? PC1:38 — the assembly must first absorb the weight, grid, SL and delivery repairs | Agenda 6: the seat keeping CD writes the non-corollary sentence; else it becomes a remark |
| D3 | Theorem SL, K97 | A, B, D: main (A:100, B:95, D:104). C: defer (C:96) | PC1:37: SL's actual prior/λ_s rate, an iteration-uniform bound, and an FDR threshold bounded away from 0; B.D9(b) is a COUNTEREXAMPLE | Round 2 statements, check wave 2; otherwise FUTURE_WORK |
| D4 | §5.3 package K102 (+K10, K11, K25, K53) | Four statements (SBS T4): C design-computable D_*; A, D η-perturbation; B leakage CBL + favourable start | Which statements survive the checks (§0.4); at what ε the constants are useful; whether a necessity proposition is provable; an IC3 exhibit on the method's own partition | One merged package with HQ's (a), (b), (c); check wave 2 |
| D5 | Stage laws K25–K31 (clause level) | K26/K30: A, B, D main; C supplement. K28 (thermodynamic-length / fine-grid limit): cited KNOWN—CITE inside the A, B, D packages (A:341, 346; B:264, 269; D:308, 313) and a cited lemma for C (C:127). K29: A, D main; B supplementary (B:264); C future (C:128). K25: A, D main; B supplement (B:125); C supplement. K27: A, B main; D supplement (D:135); C merged into K25. K31 (Conjecture P, OPEN): A, D in main as OPEN; B, C future | An OPEN conjecture cannot be a list theorem. PC1 cluster 9: "exact/minimal coded grid" wording is false | Rule: OPEN → FUTURE_WORK or a provable fallback; restated clauses |
| D6 | Work/depth K87–K90 | A, C, D main (A:92, C:88, D:96); B supplement (B:87); C drops K90 as a theorem | PC1:39: the SL §6 comparison needs worker counts, n-vs-p scaling, T, score cost and a loss criterion | Agenda 11; restated comparison |
| D7 | Evidence Z, K37–K41 | A main; B, D supplement; C cited lemmas (A:89, B:84, C:85, D:93) | IC4; PC1 cluster 15: the terminal-off COUNTEREXAMPLE | IC4 + agenda 11 |
| D8 | Target consistency K93 | A, B, D main (short); C supplement (C:97) | MODEST novelty; it is an input to other cards | Agenda 11 |
| D9 | Reported HPM details | **K71** (b1-LH-iid): all four defer. A defers "(b1-LH-iid) v2 (GAP)" (A:105), although A's card header lists it (A:474; SBS:122 flags the extraction conflict). **K70** ((b2-LH), the no-LS0 corollary on STAB-LH): D a supplementary corollary (D:109); B keeps it as a main-package subfamily clause (B:100, 279, 283); A inside main card C18 (A:470); C a cited lemma (C:148). **R5 split**: C keeps the no-LS0 STAB-LH variant "attributed" (C:101) | PC1 cluster 6: A.C18 needs SIZE (g_max ≤ B < 2g_min; DESIGN-FAILS without it); D.M5(a) needs ℓ ≥ τ(C) and a completed scan; liminf delivery form (D10) | Repairs; K71 → FUTURE_WORK (no seat holds it) |
| D10 | Delivery K82 (R6) | A: OPEN limitation (A:106). B: not a theorem and not a limitation (B:101). C: defer (C:102). D: OPEN obligation (D:110) | The no-open-questions rule: a limitation must be PROVED impossible. PC1:30: liminf P(correct output) = 1 − limsup P(U_n) | Chair proposal: FUTURE_WORK (no route); every output theorem joint with the output event, in liminf form |
| D11 | R_n in H(f); finite-R bounds | A, B, D: R_n a hypothesis via M_n (B:690). C: a stacking budget R′(n, p) | GR6: M_n is not a design condition. Where a design-computable bound on M₂ exists (e.g. C's e^{D_*}, PC2:52–55), R′_n can be written through it | Chair proposal: R′_n stated through a design-computable bound on families where it is finite (a growth-rate edit), else the fixed-R statement only |
| D12 | Masked-regime accuracy statement (HQ Q3) | Not asked in Round 1 | Which one: certificate detection of underestimation (K42/K43/K45), a PIP bound conditional on delivery, or K69 (b1-LH) | Each seat names one |
| D13 | List size | Main counts: A 18, B 11, D 13, C 7 (SBS T3) | Biometrika: about 6–8 main | Agenda 11: main ≤ 8 |
| D14 | Minor placements | K16 supplementary for A, B, D; cited lemma for C. K11 (OWS-WS4): A, C, D main; B remark. K57: A, B, D supplement; C defer | — | Agenda 11 |
| D15 | Song–Liang coverage verdicts, per item | **Thm 1:** all four say selection only; Hellinger/coefficient contraction is not delivered (A:34, B:36, D:51); C adds "Do not mark this 'exceeded'" (C:52). **Thm 2:** the tail condition does not arise for fixed designs (A:35, B:37); D writes "same" as Thm 1, i.e. it keeps its contraction qualification (D:52); C: fixed sparse support only (C:53). **Thm 3:** A "matched for π; exceeded for the reported PIP" (A:36); B "delivered" (B:39); D no verdict (D:54); C: estimated PIPs need K46/K52 (C:54). **Thm 4 / Cor 2:** A "exceeded" (A:37); B "delivered and exceeded" (B:41); D "EXCEED in kind" for Thm 4 (D:55) and gives no verdict for Cor 2 (D:56); C: a cited comparison, not a theorem of our algorithm, and K97 needs a separate null-exclusion argument (C:55, 57). **Thm S:** A, B, D "exceeded" (A:39, B:40, D:57); C: covered, with SL's supplementary hypotheses unverified (C:58). **§6:** all, same-units accounting with no speed claim (A:40, B:42, D:58, C:59) | What may be called "matched/exceeded" in COVERAGE_MATRIX | Round 2: each seat's wording per SL item; Hellinger contraction → FUTURE_WORK unless routed |
| D16 | THM-INV cells: K23, K80, K107 | **K23** (spectral comparison): A, B supplement lemma (A:59, B:123); C, D future (C:123, D:132). **K80** (flag power): A, D drop / nothing provable (A:76, D:153); B supplement (B:70, 144); C future (C:155). **K107** (validated numerics): A, C future/defer, N16 OPEN (A:157, C:171); B, D supplement (B:154, D:163) | Whether each is a provable paper-1 statement or "nothing provable / future work" with a reason | Item 1 closure in Round 2 |
| D17 | Smaller substantive splits | **K02** equivariance: A main clause, ties break per-seed equivariance (A:114); C: target invariance only, algorithmic equivariance not assured under partition ties (C:108); B, D supplement. **K07** blocks: A, lemma (gap ⇒ recovery; A:118); C, preservation from separation but equality needs packing size (C:113). **K12** σ²-mixture oracle: A test oracle (A:122); B, D drop; C future (C:118). **K34** TI reporting: A, B, D drop; C future (C:131). **K67**: A defer as CONJECTURE (A:142); B, C, D drop (B:139, C:147). **K94** averaged finite-n: B supplement candidate (B:102); A, C, D future. **K99** barriers: B supplement (B:149); D, qualitative barrier as a remark via SHARE-PB, quantitative k-way bound future (D:158); A, C future (A:152, C:166) | For each: a provable statement now, or future work with a reason | Round 2 per K-ID |
| D18 | Placements still split in eight groups (target/envelopes; start machinery and blocks; calibration; evidence bounds; pooling; output validity and worker equivalence; certificates and decision rules; inherited calculus and limitations) | Per K-ID in §2.1; there is no uniform pattern (e.g. C places K62, K73 in main and K49 as a cited lemma and K103 in supplement; B places K36, K78 in main; K59 is future for A, C, D) | IC4 (cited lemma vs our proposition) and paper fit | Agenda 11 + IC4, per group |

### 2.1 Row D18 in detail: placement per K-ID (extracted from SBS T2, verbatim cells with the seats' line refs; "≠" marks a conflict between a seat's §B/§C entry and its card header, as the clerk flagged it)

| Group | K-ID | A | B | C | D | SBS line |
|---|---|---|---|---|---|---|
| Target, envelopes, invariance | K01 | main → C1 · A:113 | supplement → D17 · B:110 | supplement → D11 · C:107 | supplement → S1 · D:117 | SBS:52 |
| Target, envelopes, invariance | K02 | main, folded into C1 · A:114 | supplement → D17 · B:111 | supplement, merged into D11 · C:108 | supplement → S1 · D:118 | SBS:53 |
| Target, envelopes, invariance | K03 | main, folded into C1 · A:115 | supplement → D17 · B:112 | supplement, merged into D11 · C:109 | supplement → S1 · D:119 | SBS:54 |
| Target, envelopes, invariance | K04 | main, folded into C1 · A:116 | cited lemma · B:113 | supplement, merged into D11 · C:110 | supplement → S1, feeds M12 · D:120 | SBS:55 |
| Target, envelopes, invariance | K05 | main, folded into C16 · A:117 | supplement → D18 · B:114 | supplement, merged into D11 · C:111 | supplement → S9 · D:121 | SBS:56 |
| Target, envelopes, invariance | K76 | supplement → S1 · A:146 | supplement → D17 · B:143 | supplement, merged into K01 · C:153 | supplement → S12 · D:152 | SBS:127 |
| Target, envelopes, invariance | K95 | main → C7 · A:151 | supplement → D17 · B:148 | cited lemma · C:165 | supplement → S3 · D:157 | SBS:146 |
| Start machinery and blocks | K06 | main → C12 · A:356 | supplement → D11, D21 · B:336 | supplement, merged into D10 · C:112 | supplement → S2 · D:122 | SBS:57 |
| Start machinery and blocks | K14 | main, folded into C16 · A:124 | supplement → D21 · B:121 | cited lemma · C:120 | supplement → S2 · D:130 | SBS:65 |
| Calibration | K33 | main → C11 · A:130 | supplement · B:127 | supplement, merged into K25 · C:130 | supplement → S10 · D:136 | SBS:84 |
| Evidence bounds | K44 | main → C6 · A:133 | main → D3 · B:201 | main, merged into K43 · C:136 | supplement → S6 remark · D:139 | SBS:95 |
| Pooling | K47 | cited lemma → C4 · A:219 | cited lemma (V1) · B:79 | cited lemma · C:80 | supplement → S5 ≠ V1 · D:434 | SBS:98 |
| Pooling | K49 | main → C4 · A:219 | supplement → D14 · B:393 | cited lemma · C:70, C:82 (auditor correction; SBS:100 read "main, merged into K46") | supplement → S5 · D:434 | SBS:100 |
| Pooling | K54 | main → C4 · A:136 | supplement → D19 · B:133 | cited lemma · C:140 | supplement → S5 · D:142 | SBS:105 |
| Pooling | K56 | main → C4 (one-step) · A:138 | supplement · B:135 | cited lemma · C:142 | supplement → S5 remark · D:144 | SBS:107 |
| Pooling | K59 | future work (defer) · A:62, A:95 | supplement → D14 · B:393 ≠ defer · B:90 | future work · C:91 | future work · D:99 | SBS:110 |
| Output validity, worker equivalence | K36 | main → C3 · A:200 | main → D1, D3 · B:163 | cited lemma (V1 cite) · C:80 | main → M3 · D:202 | SBS:87 |
| Output validity, worker equivalence | K77 | main → C3 · A:200 | supplement (V4) · B:82 | supplement, rank 14 · C:460 | supplement → S4 · D:420 | SBS:128 |
| Output validity, worker equivalence | K78 | main → C3 · A:200 | main → D3 · B:201 | supplement, rank 14 · C:460 | main → M3 · D:202 | SBS:129 |
| Output validity, worker equivalence | K83 | supplement → S1 · A:489 | supplement (V2) · B:80 | cited lemma · C:157 | supplement → S4 · D:420 | SBS:134 |
| Output validity, worker equivalence | K84 | supplement → S1 · A:489 | supplement (V2) · B:80 | cited lemma · C:158 | supplement → S4 · D:420 | SBS:135 |
| Output validity, worker equivalence | K85 | main → C3, C4 · A:200, A:86 | supplement (V3(v)) · B:81 (auditor correction; SBS:136 read "main, merged into D2") | cited lemma · C:159 | main → M1 · D:168 | SBS:136 |
| Output validity, worker equivalence | K86 | main → C2 · A:181 | main → D1 ≠ supplement (V2) · B:163, B:80 | cited lemma · C:160 | main → M1 · D:168 | SBS:137 |
| Certificates and decision rules | K60 | cited lemma → S5 · A:102, A:565 | cited lemma (R2) · B:97 | cited lemma · C:98 | supplement → S3 ≠ R2 · D:406, D:106 | SBS:111 |
| Certificates and decision rules | K61 | cited lemma → S5 · A:139 | cited lemma · B:136 | cited lemma · C:143 | supplement → S3 · D:145 | SBS:112 |
| Certificates and decision rules | K62 | main → C7 · A:140 | main → D8 · B:137 | main, lemma in K46 · C:144 | supplement → S3 · D:146 | SBS:113 |
| Certificates and decision rules | K63 | main → C16 · A:432 | main → D8 · B:279 ≠ supplement lemma · B:80 | cited lemma (V2) · C:81 | supplement → S4 · D:420 | SBS:114 |
| Certificates and decision rules | K64 | main → C12, C16 · A:356 | supplement → D11, D18 · B:336 | cited lemma · C:145 | supplement → S9 · D:475 | SBS:115 |
| Certificates and decision rules | K73 | main → C16 · A:143 | supplement → D18 · B:140 | main, merged into K43 · C:150 | supplement → S9 · D:149 | SBS:124 |
| Certificates and decision rules | K74 | main → C16 · A:144 | supplement → D15 · B:141 | cited lemma · C:151 | supplement → S9 · D:150 | SBS:125 |
| Inherited calculus and limitations | K79 | supplement → S3 · A:527 | supplement → D15 · B:406 | cited lemma · C:154 | supplement → S11 · D:493 | SBS:130 |
| Inherited calculus and limitations | K81 | supplement → S3 · A:148 | supplement → D15 · B:145 | cited lemma · C:156 | supplement → S11 · D:154 | SBS:132 |
| Inherited calculus and limitations | K100 | supplement → S3 · A:153 | supplement → D15 · B:150 | cited lemma · C:167 | supplement → S11 · D:159 | SBS:151 |
| Inherited calculus and limitations | K101 | supplement → S3 · A:154 | supplement → D15 · B:151 | cited lemma · C:168 | supplement → S3 · D:160 | SBS:152 |
| Inherited calculus and limitations | K103 | supplement → S6 · A:155 | supplement → D16 · B:152 | supplement → D15-TV · C:169 | supplement → S8 · D:161 | SBS:154 |
| Inherited calculus and limitations | K104 | supplement → S4 · A:156 | supplement → D19 · B:153 | cited lemma · C:170 | supplement → S8 · D:162 | SBS:155 |
| Inherited calculus and limitations | K108 | supplement → S4 · A:158 | supplement → D18 · B:155 | cited lemma · C:172 | supplement → S9 · D:164 | SBS:159 |

## 3. Repairs required by check wave 1 (each seat restates its affected clause in Round 2 or concedes)

Complete list of PC1's adverse index rows (PC1:17–52) and PC2's non-clean rows (PC2:22–45; cluster 4 at PC2:119–130):

| Cluster | Card · clause | Verdict | Repair (from the checker) |
|---|---|---|---|
| 3 | B.D3(b) bounded-h | COUNTEREXAMPLE | Scale by the range of h |
| 4 | A.C9(c) | COUNTEREXAMPLE | Transfer 1 + N_e·Var, not Var |
| 4 | A.C9(d) comparison; uniform grid | NEEDS-HYPOTHESIS | .9e^{8η} < 1 and common pilot targets; W = Ω for the full-space grid |
| 4 | A.C9 exhibit; D.M10 exhibit | NEEDS-HYPOTHESIS, DESIGN-FAILS | A design on which the method's own partition recovers the groups. Label any arbitrary-partition test as such; verify a finite η per run |
| 4 | B.D6(N) | COUNTEREXAMPLE | The contrapositive gives failure of effective beta-min OR CBL, not cancellation |
| 4 | B.D6 q₂ lemma | NEEDS-HYPOTHESIS, IMPLAUSIBLE | Separate tilt-tail control |
| 4 | D.M10(iii) and its alias D.M11(b) | COUNTEREXAMPLE | Reverse the threshold order |
| 4 | D.M10(v) | NEEDS-HYPOTHESIS | 4η_n = o(log(1 + χ²_bd)) or bounded η_n |
| 5 | A.C8 guarantee | COUNTEREXAMPLE (z = 0, BO) | A non-degeneracy hypothesis |
| 6 | D.M5(a) | NEEDS-HYPOTHESIS | ℓ ≥ τ(C) and a completed final scan |
| 6 | A.C18 clustering lemma | NEEDS-HYPOTHESIS, DESIGN-FAILS | SIZE: g_max ≤ B < 2g_min |
| 6 | A.C18, B.D8, D.M5 guarantees; A.C13(d) | NEEDS-HYPOTHESIS | P(U_n) converges, or the liminf form |
| 8 | A.C10, B.D5, D.M7 | NEEDS-HYPOTHESIS | IID discovery and the stated losses; ideal stage count ≠ total work; no universal one-shot wording |
| 9 | A.C11(a), B.D7(a), D.M9(a) exact/minimal | COUNTEREXAMPLE | Drop "exact/minimal" for the coded grid |
| 9 | A.C11(c) stage-count conclusion | COUNTEREXAMPLE | Flat d gives T = 4 > 1 |
| 9 | B.D7(b) count; A.C11(c) range existence | NEEDS-HYPOTHESIS | Name σ_max over [0, 2] and a quantitative bisection-slack/progress allowance |
| 9 | A.C11(d), B.D7(e), D.M9(c), thesis favourable clauses | NEEDS-HYPOTHESIS | Over-tilted q_w bound or (LL) |
| 9 | C.D7 | AMBIGUOUS | "At most h/2" |
| 10 | B.D9(b) | COUNTEREXAMPLE | Population, not sample, covariance |
| 10 | A.C14(b,e), B.D9(b), D.M8(b) | NEEDS-HYPOTHESIS | SL's actual prior/λ_s rate, an iteration-uniform bound, an FDR inclusion threshold bounded away from 0 |
| 11 | A.C13(b,d), B.D10(c,d), D.M11(b,d) | NEEDS-HYPOTHESIS | Repair the weight, grid, SL and delivery clauses before assembling |
| 13 | A.C12(d), B.D11 SL comparison, D.M13 SL clause | NEEDS-HYPOTHESIS | Worker counts, n-vs-p scaling, T, score cost and a loss criterion (accuracy-matched); finite SMC does not output π exactly |
| 14 | A.C4(ii) | NEEDS-HYPOTHESIS | 0 ≤ h ≤ 1, or include the oscillation |
| 15 | A.C6(iii), B.D12(ii) | COUNTEREXAMPLE | The source's exception-probability form |
| 15 | A.C6(vii), B.D12(vi), D.S6 crude bound | NEEDS-HYPOTHESIS | D as a deterministic full-space range |
| 15 | D.S6 U_rest bracket | NEEDS-HYPOTHESIS | Verified per-region upper bounds and a complete covering of Ω∖𝒯 |
| 16 | A.§F reverse KL | NEEDS-HYPOTHESIS | π(𝒯^c) > 0 |
| 16 | A.§F "any interval / exact interval"; D.M2(c) | NEEDS-HYPOTHESIS | A simultaneous/uniform CDF or model-TV event **and** quantile margins on a finite endpoint grid, or inverse-CDF regularity |
| 17 | A.C16(c), B.D18 local clause | COUNTEREXAMPLE (duplicate-column tie) | Ties allowed |
| 17 | B.D18 rounding; D.S9 rounding | NEEDS-HYPOTHESIS | An explicit arithmetic model, backward-error constants, stable Q evaluation and a residual-scale/cancellation term |
| 18 | A.S3(c), B.D15(e), D.S11 duplicates | COUNTEREXAMPLE | By symmetry, PIP = E[number selected in the group]/d. The limit is 1/d only if exactly one is included asymptotically; under the actual ridge/BB target with two duplicates it is 2/3 |
| 18 | B.D15(d) | NEEDS-HYPOTHESIS, IMPLAUSIBLE | An explicit landscape, the actual partition/ties/cap, and proposal bounds |
| 18 | B.D15(g) | NEEDS-HYPOTHESIS | Exactly Gaussian log-evidences, or a justified approximation with an error bound |
| 19 | A.S6(c), B.D16 graph, D.S2 graph | NEEDS-HYPOTHESIS | p ≥ 2 |
| 20 | B.D17 odds certificate | NEEDS-HYPOTHESIS | η < 1 |
| C | C.D14 "within/between separation gives the groups as blocks" | AMBIGUOUS | True only once B ≥ 9 (p ≥ 81, n ≥ 9⁶) |
| C | C.D9 tie DP; C.D5 region certification | DESIGN-ASSERTED | Exhibit a design |
| C | C.D5 region route; C.D6 full count; C.D4 LS0 route | GAP (self-flagged) | Branch-cover invariant and validated envelopes (N16); execution-DAG audit; LS0/N2(c)/GUARD-W audits |

## 4. Round 2 agenda (frozen at dispatch)

- **R2.1 Rebuttal** of every row D1–D18 of §2: concede / hold / amend, plus the evidence that would change your position. ≤ 80 words per row.
- **R2.2 Final statements** for every card you keep. Apply the §3 repairs or concede the clause. Do not re-derive results with a filed check.
- **R2.3 The §5.3 package** under HQ Q1 (§0.1), one card:
  - (a) the discrepancy half, with constants and the σ²-coupling term, on a correlated family with ε > 0;
  - (b) the bridge-form stability theorem (per-stage χ²/weights, stage count, constants continuous in ε) on such a family;
  - (c) the one-shot refutation, conditional on the cross-family check passing (else back to HQ);
  - the ε-scale at which (a) and (b) have useful constants, and whether a necessity proposition is provable;
  - an IC3 exhibit on the method's own partition.
  - If (a) or (b) lacks a credible route, say so: that escalates.
- **R2.4 Masked-regime accuracy statement** (HQ Q3): name it (D12). Confirm the fallback set for §5.4 and the reverse-KL definitional statement. The masked final-estimate TV/KL is FW2 (V11, N10 OPEN).
- **R2.5 Run-card definitions** (HQ Q4):
  - inputs only from existing run quantities;
  - no random numbers;
  - no feedback;
  - the estimator's definition and numerical label for Ĵ and for the leakage proxy;
  - the theorem stated about each.
- **R2.6 Agenda items 6** (thesis scope), **7** (growth rates; D11), **9** (p ≤ n^A; exponential p → FUTURE_WORK with a reason), **10** (novelty risks, citations checked), **11** (main ≤ 8 vs supplement). **Item 1 closure:** "nothing provable" cells (D16) and the Song–Liang wording (D15).

## 5. Correction log (v1 → v2, per `SYNTH_R1_AUDIT.md`)

| Audit # | Change |
|---|---|
| 1, 2 | §0.1 Q1 rewritten: the correlated-family requirement applies to (a)/(b); (c) needs the check to **pass**; constants, σ²-coupling, stage count, continuity and both failure dispositions stated; R2.3 aligned |
| 3 | §0.1 Q3: obligation with fallback, V11/N10 OPEN, reverse-KL obstruction, the shipped fallback set; R2.4 aligned |
| 4 | §0.1 Q4 and R2.5: the full reporting constraints |
| 5 | §0.4 rewritten: the scale observation restricted to PC2's examined family (signal energy O(√n)); validity vs useful constants separated; growth of osc d marked numerical evidence; B's leakage clauses recorded as not perturbative |
| 6 | §1 item 1: C's qualifications (C:52, 55) recorded; new row D15 |
| 7 | §1: THM-INV not uniformly agreed; new row D16 (K23, K80, K107) |
| 8 | D1 rewritten: package placement separated from the novelty of clauses; each seat's method-specific content stated |
| 9 | D9: K71 is deferred by all four (A:105); the header-based extraction conflict noted (SBS:122) |
| 10 | §1 item 3 and D5/D14: placements by clause (K16 supplementary for A, B, D; K25/K27/K28 per seat) |
| 11 | New row D17 (K02, K07, K12, K34, K67, K94, K99; D's qualitative vs quantitative barrier distinguished) |
| 12 | New row D18 (grouped placement splits) |
| 13, 14, 15 | §3 completed: B.D7(b)/A.C11(c) progress; SL hypotheses; thesis assembly; SL complexity; D.M11(b) alias; A.C13(d); A.C18 DESIGN-FAILS; D.S9 rounding; quantile margins; the duplicate rule PIP = E[selected in group]/d |
| 16 | No change (OK) |
| Re-audit N1–N6 (`SYNTH_R1_REAUDIT.md`) | N1: PC1 refs for B.D6(N)/q₂ swapped back. N2: D15 rewritten per SL item with every seat's own qualification. N3: K28 recorded as cited inside the packages; B's K29 supplementary. N4: K70 placements stated per seat, with the header conflict. N5: D18 replaced by the per-K table §2.1 (adds K06, K14, K33, K44, K83, K84). N6: pathwise W bounds separated from the M₂ moment bound |
| Verification (`SYNTH_R1_VERIFY.md`, PASS WITH CORRECTIONS) | v2.2: D15 keeps D:52's qualification and separates D:55 (Thm 4) from D:56 (Cor 2); D9: B's K70 is a main-package subfamily clause (B:100, 279, 283), no conflict; §2.1: C's K49 → cited lemma (C:70, 82), B's K85 → supplement (B:81) |
