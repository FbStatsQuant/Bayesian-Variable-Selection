# MEET-THM · Minutes ("Theorems — Final meeting", paper 1 of SMC-BVS)

Chair (Opus 5.5, non-voting), 2026-11-04. Branch `theory/MEET-THM`.

The dossier (`DOSSIER.md`) was frozen at 02:00 UTC. HQ approves this package and brings it to Felipe, who approves the theorem list.

**Open questions at close: none.** Every candidate K01–K108 (`R0_DIFF.md`) is in one of these states:
- on the list, with a fallback;
- FUTURE_WORK, with a reason;
- a cited lemma;
- dropped, with a reason.

The registry of where each one landed is `REGISTRY_PAPER1.md`. The coverage check is `COVERAGE_MATRIX.md`.

## 1. Record of the meeting

| Step | Files | Outcome |
|---|---|---|
| Round 0 | `R0_D.md`, `R0_E.md`; `R0_DIFF.md` (registrar + chair) | 24 draft entries + 72 D items + 44 E packages (+15 E negatives) + N1–N17 → 108 candidates K01–K108; coverage complete |
| Round 1 | `R1_A.md`–`R1_D.md`; `evidence/R1_SIDE_BY_SIDE.md` | Independent positions on agenda 1–5 and 8; about 85 cards |
| HQ Q1–Q4 | `HQ_QUESTIONS.md`; `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md` | §5.3 bridge form accepted with three parts (a)(b)(c); §5.4 coverage = posterior-content/MC error; masked final TV/KL not binding (FW2); Ĵ and the leakage proxy allowed as reporting |
| Check wave 1 | `CHECK_W1_BRIEF.md`; `evidence/W1_PC1/`, `evidence/W1_PC2/` | PC1 (gpt-6.1-sol) on A, B, D: 11 COUNTEREXAMPLE, 25 NEEDS-HYPOTHESIS. PC2 (Opus 5.5) on C: 0 COUNTEREXAMPLE |
| Inherited-proof check | `CHECK_INHERITED_BRIEF.md`; `evidence/CHK_INHERITED/` | OWS-WS3, WS4 VERIFIED; WS6(d), WS7, N9 VERIFIED WITH AMENDMENT (cross-family, line by line). The one-shot refutation survives, so HQ Q1(c) is met |
| Synthesis 1 | `SYNTH_R1.md` (v2.2); audits `SYNTH_R1_AUDIT.md` (FAIL), `SYNTH_R1_REAUDIT.md` (FAIL), `SYNTH_R1_VERIFY.md` (PASS WITH CORRECTIONS) | Disagreement table D1–D18; repairs list |
| Round 2 | `R2_A.md`–`R2_D.md`; `evidence/R2_SIDE_BY_SIDE.md` | Rebuttals, final statements, §5.3 package, masked statement, run-card definitions, agenda 6, 7, 9, 10, 11 |
| Check wave 2 | `CHECK_W2_BRIEF.md`; `evidence/W2_PC1/`, `evidence/W2_PC2/` | PC1: 9 COUNTEREXAMPLE (all new R2 clauses: necessity propositions, jump corollary, two run-card clauses, duplicate scope), 3 NOT REPAIRED (SL). PC2: 29/29 TRUE-AS-WRITTEN |
| HQ Q5 | `evidence/2026-11-04_HQ_RULING_Q5.md` | Stage count in Q1(b) = sandwich + local constancy + continuous envelope. T is a step function, stated with PC1's example |
| Synthesis 2 | `SYNTH_R2.md` (v2); `SYNTH_R2_AUDIT.md` (PASS WITH CORRECTIONS) | Reconciled-list proposal; R3-1…R3-8 |
| Round 3 | `R3_A.md`–`R3_D.md` | Confirmations, final cards, HQ plan, "nothing missing" |

## 2. Decisions

The rule applied: a decision is a unanimous Round 3 confirmation, or the majority of the four seats where Round 3 left a split. Every split is recorded with its dissent. The chair did not vote. The chair decided procedure only: wave merging, charter bundling, and the form of the deliverables.

### 2.1 Main text: 8 theorems (unanimous in Round 3)

| # | Theorem | K-IDs | Final card (verbatim) |
|---|---|---|---|
| M1 | **Theorem V/H.** Validity of v3.1 (general-h identity N1, frozen-𝒞 contract, islandwise identities; SMC identities and N9 cited) and accuracy of reported bounded functionals (finite R′, decision transfer, growth-rate clause) | K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47 | `R3_A.md` §S2 M1 |
| M2 | **Theorem WS, the §5.3 package.** (a) discrepancy half; (b) bridge-form stability with the Q5 stage-count content and the step-function statement; (c) Proposition ONE-SHOT (WS6(d), WS7 with CHK amendments) | K102, K10, K11, K25, K53; K103/K104 as used | `R3_B.md` §S2 M2 |
| M3 | **Theorem START.** Deterministic mass, σ²-coupling decomposition, masking law, dilution; K16 as a supplementary clause | K15, K17, K18, K10 | `R3_C.md` §S2 M3 |
| M4 | **Theorem Z𝒯 and the certificate card, with the masked-regime statement** (HQ Q3) | K42, K43, K45, K44; K36, K78 output-event clauses | `R3_B.md` §S2 M4 |
| M5 | **Theorem HPM.** Composition at every n; reported-HPM consistency with LS0 on LH; Theorem A; K70 as a labelled no-LS0 variant | K72, K69, K65, K68; K63 hypothesis | `R3_D.md` §S2 M5 |
| M6 | **Theorem SEP + Lemma KL** | K19, K106, K105 | `R3_C.md` §S2 M6 |
| M7 | **Theorem STG.** Stage laws as coded, coverage identity; K28 cited; K30 as the labelled ideal-grid clause; K33 in its deterministic termination/count form | K26, K25, K27, K30, K33 | `R3_A.md` §S2 M7 |
| M8 | **Proposition D.** Work, depth and width at the island level; the Song–Liang §6 comparison in the same units, with no speed claim; K90 as a remark | K87, K88, K89, K06, K64 | `R3_D.md` §S2 Prop D |

**R3-1, slot 8:** Proposition D, unanimous (A:101; B:138; C:119; D:128). The stated reason is IC5, objective (2).

Seat D's note for Felipe: if objective (2) is to be served by a sentence in the introduction citing the supplement instead, Prop D moves to the supplement and main = 7. Nothing else changes (D §S5).

**R3-2:** one theorem V/H, unanimous.

**Thesis CD (K96):** a scoped remark after the main theorems, unanimous since Round 2.

### 2.2 Supplement cards (statements as in the cited R2/R3 cards, with the SYNTH_R2 §3 repairs)

| Card | Content (K-IDs) | Notes and decisions |
|---|---|---|
| S-T | Theorem 1, target consistency T03♯ (K93, K04) | Unanimous since Round 2; cited in the main text |
| S-Z | Evidence variance, masked tails (K37–K41, K53) | Terminal-off clause only in the exception-probability form |
| S-TARGET | Propriety, invariance, envelopes, exact branch, odds certificate (K01–K05, K76, K95) | K95 here (R3-4 unanimous) |
| S-KERNEL | N9 kernel facts, graph (p ≥ 2), start sampler, minorisation (K20, K21, K08, K09, K22, K103) | N9 with CHK amendments. K09 is the tie-DP proposition (C10) |
| S-CERT | Local search (weak local maximum, ties allowed), certificate semantics, B&B soundness, perturbation lemma (K64, K73 without the region-certification clause, K74, K05, K108) | K73 per C's withdrawal (R3-8) |
| S-LIM | Limitations as theorems (K79, K81, K100, K101); K99 qualitative remark | Duplicates: PIP = E[# selected in group]/d; numeric limits only with their p qualification |
| S-POOL | Pooling rules, the checked recording-marginal equal-weight bias comparison P1, R_eff (K49, K50, K54, K56, K57-P1) | General K57 accuracy → FW (B, C; R3-8) |
| S-IDENT | Restricted-ESS coverage identity, TI/KL/TV calculus, **C15-CI posterior-content credible-set clause, named** (K25 lemma, K104, K55, K103) | Seat B's "missing" item 1 (R3_B §S4) adopted: HQ Q2's posterior-content reading needs a named clause |
| S-BLOCKS | Separation ⇒ groups kept; SIZE ⇒ equality (K07, K14, K06) | — |
| S-OUT | Output-event validity, worker equivalence, stacking (K77, K78, K83–K86, K63) | K63/K86 are also named as premises in M1/M5 |
| S-STGI | Ideal two-state crossing depth (K30 restated); **K29 only as a cited conditional implication** under (LL) or the over-tilted q_w bound | Its unconditional favourable application → FW. B (FW) and C (conditional cited) prevail over A and D (supplement conditional), whose substance is the same conditional implication |
| S-LEAK | B's leakage clauses (F), (S) as a supplementary corollary to M2 | R3-5, unanimous |
| S-REP | Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions | Final card `R3_C.md` §S2 S-REP. **ū̂ is D's global block-table envelope ū̂ = Σ_b max_{U⊆C_b} x_b(U)**, not a maximum over V (C's objection, R3_C §S1, adopted, since a maximum over V ⊊ Ω does not bound all fits) |

### 2.3 Other Round 3 decisions

| Item | Decision | Dissent |
|---|---|---|
| R3-3, SL K97 | FUTURE_WORK, unanimous. LIT-PAR G4 is cited in the paper as labelled numerical evidence | — |
| R3-4, K23 | FUTURE_WORK (A, B, D) | C: keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL (R3_C §S1). Recorded; the HQ of S-KERNEL may cite it as an attributed lemma without a theorem number |
| R3-4, K80 | FUTURE_WORK (A, B, C, D) | — |
| R3-4, K12, K34 | Drop (A, B, C, D in Round 3) | — |
| R3-4, K33 | M7, deterministic termination/count form (A, B, C) | D: S-IDENT (R3_D §S1). Rebuild convergence N5(b) → FW in either case |
| R3-6, Ĵ | B/C/D form, unanimous. A withdrew its TI form | — |
| R3-7, Song–Liang wording | **Thm 2:** "fixed-design, fixed-sparsity selection counterpart only; SL's predictor-tail and prior hypotheses are not transferred". **Cor 2:** "no analytic null-exclusion/FDR separation established; LIT-PAR G4 numerical evidence" (C's wording; adopted by B and D) | — |
| §2.6, growth rates | Two optional stacking configurations, on families with D_* = O_P(1): (i) R′_n = 4⌈log₂(n + p + 1)⌉ for a fixed finite set of declared summaries; (ii) R′_n = 4⌈(n + p)⁶/4⌉ for simultaneous control over ≤ (n + p)² declared summaries. ℓ, L and N need no edit. The shipped R′ = 4 carries only the fixed-R statements | Confirmed by all four in §S1 §2.6 |
| §2.7, safeguards | §13.1: if N1's general record identity fails, the narrower theorem ships and §13.1 escalates. §5.3: if both the D_* route and the correlated-family route fail, it escalates. Also: loss of the masked statement without an approved replacement escalates (C §S5) | — |
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |

### 2.4 FUTURE_WORK and drops

Complete in `FUTURE_WORK.md`, which adds C's residual obligations (R3_C §S4) to SYNTH_R2 §2.4.

**Drops, with reasons:**
- K12: a test oracle, not a guarantee.
- K34: TI evidence is not in the method.
- K66: PARTLY-FALSE (C3-PGD, CEX-localmax(A2)).
- K67: relies on K66.
- K91: no accuracy-matched comparator; OPW2-cex.
- K98: KNOWN-FALSE (SHARE-M(b), FD-NM).

### 2.5 HQ plan (agenda 12): waves

The chair merged the seats' proposals (A §S3(b), B §S3(b), C §S3, D §S3(b)) as a procedural decision. B and D nearly coincide, and A differs only in placing M1 in wave 2. Supplement cards are bundled into lemma-pack HQs, as D proposed.

| Wave | HQs | Reason |
|---|---|---|
| 1 | **M1** V/H; **M3** START; **LP-FOUND** = S-TARGET + S-BLOCKS + S-KERNEL (+ S-T cited) | Foundations. N1 (binding §13.1) is the longest pole and starts first (B, D) |
| 2 | **M2** WS (binding §5.3); **M7** STG; **M6** SEP + KL; **LP-IDENT** = S-IDENT + S-STGI | The §5.3 package and its inputs (d_σ from M3, the count from M7, the lower bound from M6) |
| 3 | **M5** HPM; **M4** Z𝒯 + masked statement; **M8** Prop D; **LP-AUDIT** = S-CERT + S-OUT | Code-audit wave: N2, N3, LS0, GUARD-W and the DAG serve M5, M4 and M8 together. M4(f) needs M5 |
| 4 | **LP-REST** = S-Z + S-POOL + S-LIM; **LP-REP** = S-REP + S-LEAK | Consequences and reporting corollaries. Nothing binding waits on them |

**Dependency graph:** the union of the seats' edge lists (A §S3(a), B §S3(a), C §S3, D §S3(a)), consolidated in `REGISTRY_PAPER1.md` §dependencies.

## 3. Items for HQ to carry to Felipe (no open question; readings he may overrule)

1. HQ readings Q1–Q5:
   - §5.3 is met in bridge form (a)(b)(c), with the disclosed scale: useful constants need ε ≲ n^{−1/2}/p on the exhibited family;
   - a sharp necessity statement is FW;
   - §5.4 coverage means posterior-content error;
   - the masked final-estimate TV/KL is FW2;
   - the stage count is a step function, controlled by the sandwich.
2. Prop D is in the main text for objective (2) (Seat D's alternative: main = 7).
3. The Song–Liang analytic separation (Cor 2) is FUTURE_WORK. Paper 1 compares, and does not claim to exceed, Thm 1, Thm 2 and Thm 4.
4. Proposed reporting amendment AMENDMENT_HQ_02 (`AMENDMENT_HQ_02_DEFINITIONS.md`):
   - the Ĵ estimator;
   - ε̂_× with its companions;
   - d as a default member of the declared list 𝓗 (A, B);
   - the read-only accumulator;
   - the two R′ growth rates.

## 4. Deliverables (DOSSIER §9)

| File | State |
|---|---|
| `THEOREM_LIST_FINAL.md` | Assembled from the verbatim final cards (§2.1) and the supplement statements (§2.2) |
| `COVERAGE_MATRIX.md` | Proposal goals, Song–Liang items, THM-INV §1 cells and N1–N17 → list items, FW or cited lemmas |
| `HQ_CHARTERS/` | 8 main-theorem charters (verbatim from the seats' §S3(c)) + 4 lemma-pack charters |
| `REGISTRY_PAPER1.md`, `NOTATION.md` | Registrar |
| `FUTURE_WORK.md` | Complete |
| `MINUTES.md` | This file |
| `FORMAT_NOTES.md` | Chair |
| `AMENDMENT_HQ_02_DEFINITIONS.md` | Definitions for HQ |
