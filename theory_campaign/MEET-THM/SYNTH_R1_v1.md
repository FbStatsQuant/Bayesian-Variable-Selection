# MEET-THM · Synthesis of Round 1 and check wave 1 (chair, non-voting)

2026-11-04. **Sources:**
- seat files `R1_A.md`–`R1_D.md`, cited as `A:123` for R1_A.md line 123, and so on;
- the clerk's side-by-side `evidence/R1_SIDE_BY_SIDE.md`, cited as `SBS T1`–`T8`, with line refs to the seat files;
- check verdicts `evidence/W1_PC1/VERDICTS.md` (PC1, gpt-6.1-sol, on A, B and D) and `evidence/W1_PC2/VERDICTS.md` (PC2, Opus 5.5, on C), cited as `PC1 §n` / `PC2 §n` by cluster;
- HQ rulings `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`.

Candidate IDs are K01–K108 (`R0_DIFF.md`). Nothing here upgrades a status. Check verdicts are about statement sanity: TRUE-AS-WRITTEN means no counterexample was found, not that the result is proved.

## 0. New facts since Round 1

1. **HQ rulings** (2026-11-04):
   - **Q1, §5.3:** the bridge form is accepted if paper 1 ships three parts, all on a genuinely correlated family with ε > 0:
     - (a) the discrepancy half;
     - (b) the bridge-form stability theorem;
     - (c) the refutation of the one-shot form, after a cross-family check.
   - **Q2:** "coverage error" means |π(C(π̂)) − nominal| for reported credible quantities, plus their Monte Carlo error. Frequentist coverage → FW1.
   - **Q3:** the masked final-estimate TV/KL is not binding → FW2. **But the list must name at least one masked-regime accuracy statement that paper 1 proves.**
   - **Q4:** Ĵ and the cross-block leakage proxy are allowed as POST HOC reporting; their exact definitions are due at close.
2. **Check wave 1, PC2 on Seat C** (56 clauses):
   - 54 TRUE-AS-WRITTEN, 2 AMBIGUOUS, 0 COUNTEREXAMPLE.
   - 53 DESIGN-VERIFIED, 2 DESIGN-ASSERTED.
   - 3 GAP. All three are implementation gaps Seat C had already flagged: the region-certificate route, the integrated execution DAG, and the LS0/GUARD-W audits (PC2 §0).
   - Three registry qualifiers were omitted (PC2 flags (b)): Thm5-LH SAME-FAMILY-ONLY; MZ-P3 AUTHOR-ONLY; T01 "external review queued". Seat C restores them in Round 2.
3. **Check wave 1, PC1 on Seats A, B and D** (101 review rows):
   - 53 TRUE-AS-WRITTEN, 11 COUNTEREXAMPLE, 25 NEEDS-HYPOTHESIS, 12 AMBIGUOUS.
   - 3 DESIGN-FAILS; 2 IMPLAUSIBLE routes; 17 GAP.
   - The index is at PC1 "Summary". §3 below lists every repair it implies.
4. **§5.3, both checkers.** The scale result is the single most consequential fact of the round.
   - **Every true bridge-form statement is perturbative in the cross-block correlation ε.**
   - Seat C's bound osc d ≤ D_* is TRUE-AS-WRITTEN: no counterexample in 124 exact cases at p ≤ 10, and M₂ ≤ e^{D_*} holds on a coded-grid replica (PC2 §0 items 1–2).
   - But D_* stays O(1) only up to ε ≈ n^{−1/2}/p, and it diverges at any fixed ε.
   - **The true osc d itself grows like √n·ε at fixed p**, so this is intrinsic, not slack (PC2 §0 item 3).
   - Seats A and D give finite-η perturbation bounds whose inequalities are TRUE-AS-WRITTEN on PC1's design Dε (cross-correlation 10⁻⁵–10⁻⁴; PC1 §4).
   - **Both seats' named exhibits fail:**
     - the method's B = 2 splits the four-variable groups;
     - D's δ > 1 at ε = 0.1;
     - A's (c) "hence within" variance transfer is a COUNTEREXAMPLE;
     - D's stage-count sandwich M10(iii) has the wrong order: it should read T_bd(.9e^{−4η}) ≤ T_true(.9) ≤ T_bd(.9e^{4η}).
   - **Seat B's two clauses fail:**
     - (N) "failure ⇒ cancellation or leakage" has a COUNTEREXAMPLE: an orthogonal design with θ₁ = n^{−1/2}.
     - Its new q₂ lemma is IMPLAUSIBLE as stated: WS6(d) gives q₂ → 0 under its own hypotheses (PC1 §4).
5. **Ground rule 6.**
   - The growth premises on R_n / M_n in A.C5(d), B.D2(f) and D.M2(d) are sampler conditions, not model or design conditions (PC1 "Ground rule 6").
   - Seat C's finite-R bounds in D1/D15 say nothing at the shipped R′ = 4 (PC2 §0 item 4).

## 1. Per agenda item: agreement and disagreement

**Item 1, coverage sweep.**
- **Song–Liang map (SBS T8):** the four seats agree.
  - Thms 1–3 and Thm S → K93, plus the reported-HPM cluster K68–K72.
  - Thm 4 / Cor 2 → the start cluster K10/K17/K18, plus K97.
  - §6 → K87/K88 (with K90 for A, B and D).
  - Cor 1 (p up to e^{Cn^α}) is not delivered: N12 OPEN (A:38, B:38, C:56, D:53). This goes to agenda 9 in Round 2.
- **Proposal map:** HQ's Q1–Q3 now fix §5.3 and §5.4. §5.1/§5.2 → the validity cluster; §13.1 → K46/K51 (N1 crux).
- **THM-INV §1 cells:** filled differently but without conflict (SBS T2). Each seat's final "nothing provable" list is due in Round 2 (§4, R2.6).

**Item 2, the draft list (SBS T1).**
- Same verdict from all four seats on 7 entries: A1 keep; D4 defer; S2 keep; S3 drop; R1 keep; R2 demote to cited lemma; R7 defer.
- Of the 17 "differs" rows, most differ only in the wording of merges (keep → merged card). The substantive splits are D3, C1, A2, V1, V2/V4, D1/D2 and R5/R6. They appear in §2.

**Item 3, new candidates (SBS T2).**
- 33 of 108 K-IDs have the same placement from all four seats. The common main core (all four "main") is:
  - the start: K10, K15, K17, K18;
  - SEP / Lemma KL: K19, K105, K106;
  - Z𝒯 and certificates: K42, K43, K45;
  - general-h and Theorem H: K46, K48, K50, K51, K52;
  - HPM, LS0 and composition: K65, K68, K69, K72;
  - §5.3: K102.
- Unanimous drops: K66 (HP3), K91, K98. Unanimous future work: K13, K24, K58, K75, K92.

**Item 4, §5.3.** All four seats ship a bridge form (SBS T4); HQ accepted that form. The ε-scale is the crux (§0.4 and row D4 below).

**Item 5, §5.4.** Settled in substance by HQ Q2/Q3 (SBS T5). Open in Round 2:
- the masked-regime accuracy statement HQ requires;
- the repairs to the coverage wording (§3, cluster 16).

**Item 8, fidelity.** PC1's registry ledger S1–S23 is the meeting's fidelity record. Seats must carry its qualifiers verbatim:
- no-LS0 and IID variants labelled as variants;
- ideal grid vs coded grid;
- W-cal not executed;
- GUARD-W and N3/e4 as audit gates;
- general LH locking XF ERROR (A-REV7).

## 2. Disagreement table (Round 2 answers row by row)

| # | Item | Positions | Crux | Settled by |
|---|---|---|---|---|
| D1 | Validity cluster K08, K20, K21, K32, K35 | A, B, D: main Theorem V (A:84, B:79, D:88). C: SMC identities cited; only the measured-record extension K46 is new (C:80) | IC4: is there method-specific content beyond Del Moral / standard SMC identities, beyond N1 and N9? | Each seat names the clause that is not a cited lemma; the chair applies IC4. N9 check in wave 2 |
| D2 | Thesis theorem CD, K96 | A, B, D: main assembly theorem (A:94, B:89, D:98). C: drop as a theorem; a scoped paragraph (C:90) | Does CD state anything not implied by its parts? PC1 §11: the assembly must also absorb the weight, grid, SL and delivery repairs | Agenda 6: a seat keeping CD writes the one sentence that is not a corollary; otherwise it becomes a remark |
| D3 | Theorem SL, K97 | A, B, D: main (A:100, B:95, D:104). C: defer, since random-partition isolation does not show SL's FDR procedure drops the hub (C:96) | PC1 §10: every SL card needs SL's actual prior/λ rate, an iteration-uniform bound, and an FDR threshold bounded away from 0. B.D9(b) "cov(x_t, y) = 0" is a COUNTEREXAMPLE | Round 2 statements with those hypotheses, then check wave 2; if no credible route, FUTURE_WORK |
| D4 | §5.3 package, K102 (+K10, K11, K25, K53) | Four statements (SBS T4). C: D_* energy bound. A, D: η-perturbation. B: leakage CBL + favourable start | ε-scale: all true forms are perturbative, valid for ε ≲ n^{−1/2}/p; at fixed ε, osc d grows like √n·ε (PC2 §0.3). Is a fixed-ε non-result itself a provable proposition (a necessity bound)? | One merged package with HQ parts (a), (b), (c). IC3 by an exhibit that runs the method's partition (PC1 Dε, PC2 §E family). Check wave 2 |
| D5 | Stage laws K25–K31 | A, B, D main (A:93, B:88, D:97); C supplement, K29 future (C:89). K31 (Conjecture P, OPEN): A and D in main as OPEN; B and C future | An OPEN conjecture cannot be a list theorem; PC1 §9: "exact/minimal coded grid" wording is false (flat-d counterexample) | Rule: OPEN → FUTURE_WORK or a stated fallback; seats restate (a) without "exact/minimal" |
| D6 | Work/depth K87–K90 | A, C, D: main (A:92, C:88, D:96). B: supplement (B:87). C drops K90 as a theorem | PC1 §13: the SL §6 comparison needs worker counts, n-vs-p scaling, T, score cost and a loss criterion | Paper fit (agenda 11); restated comparison clause |
| D7 | Evidence Z, K37–K41 | A main; B, D supplement; C cited lemmas (A:89, B:84, C:85, D:93) | IC4 for classical evidence facts; PC1 §15: the terminal-off clause is a COUNTEREXAMPLE | Agenda 11 + IC4; repair per §3 |
| D8 | Target consistency K93 | A, B, D main (short); C supplement (C:97) | Novelty MODEST; needed as input to D2/D9 | Agenda 11 |
| D9 | Reported HPM: K70, K71; R5 split | K71 (b1-LH-iid): A main, the others future. K70: C cites | PC1 §6: A.C18 needs SIZE (g_max ≤ B < 2g_min). D.M5(a) needs ℓ ≥ τ(C). All guarantees need the delivery limit stated as liminf (row D10) | Concession or check; K71 → FUTURE_WORK unless a route is named |
| D10 | Delivery K82 (R6) | A: OPEN limitation (A:106). B: not a theorem, not a limitation (B:101). C: defer (C:102). D: OPEN obligation (D:110) | The no-open-questions rule: a limitation must be PROVED impossible. PC1 §6: state liminf P(correct output) = 1 − limsup P(U_n) | Chair proposal: FUTURE_WORK (delivery P(U) → 0, no route), and every output theorem joint with the output event, in the liminf form |
| D11 | R_n in H(f) and finite-R bounds (B:690) | A, B, D: R_n a hypothesis via M_n. C: a stacking budget R′ = R′(n, p) | GR6: M_n is not a design condition. On the §5.3 family, M₂ ≤ e^{D_*} is design-computable (PC2 §0.2) | Chair proposal: either R′_n stated through a design-computable bound (e.g. R′_n ≥ c·e^{D_*}/ε² on families with finite D_*), recorded as a growth-rate edit; or only the fixed-R finite statement ships |
| D12 | Masked-regime accuracy statement (HQ Q3) | not yet asked | Which statement paper 1 proves in the masked regime: certificate card's detection of underestimation (K42/K43/K45), a PIP bound conditional on delivery, or K69 (b1-LH)? | Each seat names one in Round 2 |
| D13 | List size | Main counts: A 18, B 11, D 13, C 7 (SBS T3) | Biometrika: about 6–8 main theorems (dossier §6 item 11) | Agenda 11: each seat gives a main list of ≤ 8 and moves the rest to the supplement |
| D14 | K16 favourable rate; K11 OWS-WS4; K57 equal-weight PIP | K16: A, B, D main vs C cited. K11: A, C, D main vs B remark. K57: A, B, D supplement vs C defer | Minor placement | Agenda 11 |

## 3. Repairs required by check wave 1 (each seat restates its affected clause in Round 2 or concedes)

| Cluster | Card · clause | Verdict | Repair (from the checker) |
|---|---|---|---|
| 3 | B.D3(b) bounded-h | COUNTEREXAMPLE (π = (.9, .1), h = (0, 100)) | Scale the error by the range of h |
| 4 | A.C9(c) | COUNTEREXAMPLE | Transfer 1 + N_e·Var, not Var |
| 4 | A.C9(d) | NEEDS-HYPOTHESIS | .9e^{8η} < 1, common pilot targets; W = Ω for the full-space grid |
| 4 | A.C9, D.M10 exhibits | DESIGN-FAILS | Use a design on which the method's own partition recovers the groups (PC1 Dε; PC2 §E family from n ≈ 5·10⁵) |
| 4 | B.D6(N) | COUNTEREXAMPLE | Contrapositive gives failure of effective beta-min OR CBL, not cancellation |
| 4 | B.D6 q₂ lemma | IMPLAUSIBLE | Needs separate tilt-tail control |
| 4 | D.M10(iii) | COUNTEREXAMPLE | Reverse the threshold order |
| 4 | D.M10(v) | NEEDS-HYPOTHESIS | 4η_n = o(log(1 + χ²_bd)) or bounded η_n |
| 5 | A.C8 guarantee | COUNTEREXAMPLE (z = 0, block-orthogonal) | Non-degeneracy hypothesis |
| 6 | D.M5(a); A.C18 lemma; all HPM guarantees | NEEDS-HYPOTHESIS | ℓ ≥ τ(C) and a completed final scan; SIZE; liminf delivery form |
| 8 | A.C10, B.D5, D.M7 | NEEDS-HYPOTHESIS | Restrict to IID discovery and the stated losses; ideal stage count ≠ total work; no universal one-shot wording |
| 9 | A.C11(a,c), B.D7(a), D.M9(a) | COUNTEREXAMPLE | Drop "exact/minimal" for the coded grid; flat d gives T = 4 |
| 9 | Favourable clauses (A.C11(d), B.D7(e), D.M9(c)) | NEEDS-HYPOTHESIS | Over-tilted q_w bound or (LL) |
| 9 | C.D7 | AMBIGUOUS | "At most h/2" |
| 10 | B.D9(b) | COUNTEREXAMPLE | Population, not sample, covariance |
| 14 | A.C4(ii) | NEEDS-HYPOTHESIS | 0 ≤ h ≤ 1, or include the oscillation |
| 15 | A.C6(iii), B.D12(ii) | COUNTEREXAMPLE (terminal-off) | Restate as the source's exception-probability form |
| 15 | A.C6(vii), B.D12(vi), D.S6 | NEEDS-HYPOTHESIS | Define D as a deterministic full-space range; complete covering for U_rest |
| 16 | A.§F reverse KL; A.§F / D.M2(c) interval wording | NEEDS-HYPOTHESIS | π(T^c) > 0; a simultaneous/uniform CDF event |
| 17 | A.C16(c), B.D18 "strict local maximum" | COUNTEREXAMPLE (duplicate columns tie) | Ties allowed; the rounding needs an arithmetic model (N16) |
| 18 | A.S3(c), B.D15(e), D.S11 duplicates | COUNTEREXAMPLE | PIP → 2/3, not 1/2, under the actual ridge/BB target |
| 18 | B.D15(d), (g) | IMPLAUSIBLE / NEEDS-HYPOTHESIS | An explicit landscape construction; a Gaussian model or a stated approximation |
| 19 | Graph clauses | NEEDS-HYPOTHESIS | p ≥ 2 |
| 20 | B.D17 odds certificate | NEEDS-HYPOTHESIS | η < 1 |
| C | C.D9 tie DP; C.D5 region certification | DESIGN-ASSERTED | Exhibit a design |

## 4. Round 2 agenda (frozen at dispatch)

- **R2.1 Rebuttal** of every row D1–D14 of §2: concede / hold, the evidence that would change your position, ≤ 80 words per row.
- **R2.2 Final statements** for every card you keep. Apply the §3 repairs, or concede the clause. Do not re-derive results that have a filed check.
- **R2.3 The §5.3 package** under HQ Q1, one card with:
  - parts (a), (b) and (c), plus the ε-scale stated honestly;
  - whether a matching necessity proposition (at fixed ε, osc d ≳ √n·ε) is provable;
  - an IC3 exhibit on which the method's own partition recovers the groups.
- **R2.4 Masked-regime accuracy statement** (HQ Q3): name it (row D12).
- **R2.5 Run-card definitions** (HQ Q4): the exact estimator and numerical label for Ĵ and for the leakage proxy.
- **R2.6 Agenda 6** (thesis scope), **7** (growth rates, including D11), **9** (scope p ≤ n^A; exponential p → FUTURE_WORK with reason), **10** (novelty risks, each citation checked), **11** (main ≤ 8 vs supplement). Also the final "nothing provable" list for THM-INV §1 (item 1).
