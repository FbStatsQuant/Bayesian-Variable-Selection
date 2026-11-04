# MEET-THM · Synthesis of Round 2 and check wave 2 (chair, non-voting)

2026-11-04.

**Sources:**
- Seat files `R2_A.md`–`R2_D.md`, cited `A:123` etc. (R2 line numbers). Round 1 files are cited `R1_A:123`.
- The clerk's `evidence/R2_SIDE_BY_SIDE.md`, cited `SBS2 U#` or `SBS2:line`.
- Check verdicts:
  - `evidence/W2_PC1/VERDICTS.md` (PC1, gpt-6.1-sol, on Seats A, B, D), cited `W2PC1`;
  - `evidence/W2_PC2/VERDICTS.md` (PC2, Opus 5.5, on Seat C), cited `W2PC2`;
  - `evidence/CHK_INHERITED/REPORT.md`, cited `CHK`.
- HQ rulings: `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md` and `evidence/2026-11-04_HQ_RULING_Q5.md`.

Nothing here upgrades a status. TRUE-AS-WRITTEN means "no counterexample found".

**What this synthesis is.** §2 is the chair's **proposal**: a reconciled list built from the seats' Round 2 positions and the check evidence. It is not a vote. Round 3 confirms or objects item by item (§5).

## 0. New facts since Round 2

1. **Check wave 2, PC2 on Seat C** (W2PC2 §0):
   - 29 of 29 claim rows TRUE-AS-WRITTEN and DESIGN-VERIFIED; 0 COUNTEREXAMPLE.
   - 2 GAP: the self-flagged LS0/GUARD-W and execution-DAG audits, NOT REPAIRED (audit obligations, not statement errors).
   - 22 REPAIRED. K73's region certification was withdrawn.
2. **Check wave 2, PC1 on Seats A, B, D** (W2PC1 summary):
   - 91 rows: 70 TRUE-AS-WRITTEN, 9 COUNTEREXAMPLE, 8 NEEDS-HYPOTHESIS, 4 AMBIGUOUS.
   - 83 DESIGN-VERIFIED, 1 DESIGN-FAILS; 1 IMPLAUSIBLE.
   - Repairs: 57 REPAIRED, 16 REPAIRED DIFFERENTLY, 3 NOT REPAIRED. All three NOT REPAIRED rows are the SL cards: the iteration-uniform null-BF/prior-odds step is still open.
   - The adverse rows are all new Round 2 clauses or the SL step: necessity propositions, a jump corollary, continuity wording, one run-card rescaling, one leakage-order theorem, and duplicate-limit scope. §3 lists them.
3. **HQ Q1(c) met.** CHK verdicts: WS3, WS4 VERIFIED; WS6(d), WS7 VERIFIED WITH AMENDMENT. The one-shot refutation survives in the shipped bounded-block setting (CHK §6).
4. **HQ Q5 ACCEPTED** (`2026-11-04_HQ_RULING_Q5.md`). The stage-count content of Q1(b) is three things:
   - the sandwich T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}), with η → 0;
   - local constancy at non-critical thresholds;
   - a continuous upper envelope.

   Two conditions:
   - **(1)** the real-valued parts (per-stage χ², weight-dispersion bounds, constants) are stated as genuine continuity or Lipschitz statements in ε on the correlated family;
   - **(2)** the theorem says that T is a step function of ε that can jump, citing PC1's example (T = 3 between {2, 4} at ε = 10⁻⁵).
5. **§5.3 scale.** Both checkers confirm that the useful (O(1)) constants need ε ≲ n^{−1/2}/p on C's family (W2PC2 §0 item 4; W2PC1 A/B/D scale rows).
   - **Every necessity proposition from A, B and D is a COUNTEREXAMPLE as stated** (W2PC1: A.R3 N-d; B.R3 NEC; D.R3 NEC).
   - C's necessity claim is TRUE only as a range obstruction for the D_* route, not as a weight-variance necessity (W2PC2 §0 item 5).
   - So **no necessity proposition ships**; the sharp scale is future work (§2.4).
6. **IC3 exhibits.**
   - **SMC-dispatched exhibit:** C's family, groups of nine, blocks = groups for n ≥ 9⁶, verified with the method's own partition actually computed (W2PC2 §0 item 3).
     - At ε = 1/(np), the cross-block term is negligible (b_X ≈ 5·10⁻⁴ to 3·10⁻⁵).
     - The **stronger exhibit ε = n^{−1/2}/p** has b_X ≈ 0.35 and D_* ≈ 1.73–1.90, also verified.
   - **Component checks only:** the finite exhibits of A (n = 64, p = 16, B = 4) and of B and D (n = 40, p = 8, B = 2) recover their groups, but production dispatches the exact branch at those sizes (W2PC1 evidence notes). They are cited as component checks.

## 1. What converged in Round 2 (SBS2 U1)

- **D2, thesis CD** (K96): a scoped **remark**, not a theorem. All four agree (A:18; B:57; C:16; D:18; SBS2 U1 D2).
- **D8, target consistency** (K93): **supplement** (short, cited in the main text). All four agree.
- **D10, delivery** (K82): **FUTURE_WORK** (no route). Every output theorem is stated jointly with the output event in liminf form. All four agree.
- **D4, §5.3:** all four merge into **one package** with HQ parts (a), (b), (c). They differ only on where B's leakage clauses (F), (S) sit (§2.1, M2).
- **D12, masked statement:** all four name the **Z𝒯/certificate masked clause** (K43/K45/K42) composed with the reported-HPM theorem on LH (SBS2 U6). They differ only in which consequence is headlined (§2.2).
- **D13, size:** A, B and D have 8 main theorems, C has 7 (SBS2 U2).
- **D15, Song–Liang wording: largely converged.**
  - **Shared restrictions** (SBS2 U8): Hellinger contraction is not delivered and goes to FUTURE_WORK; "compared, not exceeded" for Thm 4; same-units accounting with no speed claim for §6.
  - **Remaining differences:**
    - Thm 2: B calls it "not applicable, fixed design" (B:70); A gives "selection matched" (A:31); C and D give a fixed-design selection counterpart (C:393; D:235).
    - Cor 2: A, "a comparison" (A:31); B, "null exclusion is SL's separate GAP" (B:70); C, "no analytic null-exclusion/FDR separation established" (C:397); D, "covered by SL′ only if it ships" (D:235).
  - These go to R3-7.

## 2. Chair's reconciled list (proposal for Round 3)

Each main row lists the seats that place it in main (SBS2 U2).

### 2.1 Main text (proposal: 6 shared main packages + STG proposed + an optional eighth slot for Round 3)

| # | Theorem (K-IDs) | Seats with it in main | Basis |
|---|---|---|---|
| M1 | **Theorem V/H: validity of v3.1 and accuracy of reported bounded functionals.** (a) the general-h identity N1, the frozen-𝒞 contract, islandwise identities, with SMC identities and N9 cited (K46, K32, K86, K35, K36, K50; cited K20, K21, K08, K47); (b)–(f) Theorem H, finite-R′ bounds, decision transfer (K51, K52, K48, K62) | All four. A and B as two cards, V+ and H (A:40, A:50; B:81, B:91); C and D as one (C:68; D:55) | One theorem with clause (a) = validity keeps main ≤ 8. Whether to split is decision R3-2 |
| M2 | **Theorem WS, the §5.3 package** (K102, K10, K11, K25, K53, K103/K104 as used). Parts (a), (b), (c) per §2.3 | All four (A:60; B:101; C:79; D:77) | Binding §5.3; HQ Q1 + Q5 |
| M3 | **Theorem START: deterministic mass, σ²-coupling decomposition, masking law, dilution** (K15, K17, K18, K10; K16 supplementary clause) | All four (A:75; B:105; C:105; D:79) | Unanimous |
| M4 | **Theorem Z𝒯 and the certificate card, including the masked-regime statement** (K42, K43, K45, K44; K36, K78 as output-event clauses; K95 placement in §2.2) | All four (A:85; B:115; C:94; D:71) | Unanimous; it carries the HQ Q3 masked statement |
| M5 | **Theorem HPM: composition at every n and reported-HPM consistency with LS0 on LH** (K72, K69, K65, K68, K63 as hypothesis; K70 as a labelled no-LS0 variant clause) | All four (A:95; B:125; C:83; D:65) | Unanimous |
| M6 | **Theorem SEP + Lemma KL** (K19, K106, K105) | All four (A:115; B:145; C:116; D:87) | Unanimous |
| M7 | **Theorem STG: stage laws as coded, coverage identity** (K26, K25, K27, K30; K28 cited; K33 per R3-4) | A, B, D (A:105; B:135; D:81). C: supplement C8 (C:143, C:361) | 3 of 4; a proposal, not agreement |
| M8 | **Open slot; Round 3 decides between:**<br>(i) **Proposition D**, island-level work/depth (K87, K88; K89, K90 accounting). C has it main (C:127; list C:357). A, B, D have it in the supplement (A:22; B:61; D:22).<br>(ii) a **standalone validity proposition V+**, if M1 is split (A, B).<br>(iii) none (7 main) | — | The chair notes, for IC5, that with (i) in the supplement **no main theorem serves objective (2), parallel scalability**. Felipe lists that objective second (dossier §1 item 7). This is a fact for the seats to weigh, not a vote |

**Not main.**
- **SL (K97) → FUTURE_WORK** (proposal). C: FUTURE_WORK (C:17). D: main (D:92). A and B: supplement (A:19; B:58). W2PC1 marks the SL cards of A, B and D **NOT REPAIRED**: the iteration-uniform null-BF/prior-odds step is still asserted, not established. Its key step is therefore an unproved hypothesis about SL's algorithm, not a model/design condition (ground rule 6, IC1/IC2).
  - Proposal: the analytic separation goes to FUTURE_WORK, with that reason.
  - The paper may still cite the numerical LIT-PAR G4 comparison as evidence, labelled as such.
  - Round 3 decides (R3-3).
- **Thesis CD:** a remark (converged).

### 2.2 Supplement (proposal; placement by majority of SBS2 U3/U4)

| Card | K-IDs | Placement |
|---|---|---|
| S-T | Theorem 1, target consistency (T03♯): K93, K04 | All four: supplement |
| S-D | Proposition D, work/depth: K87–K90, K06, K64 | A, B, D (unless chosen for M8) |
| S-Z | Theorem Z, evidence variance and masked tails: K37–K41, K53 | A, B, D. C cites them as lemmas |
| S-TARGET | Propriety, invariance, envelopes, exact branch: K01–K05, K76, K95 | A, B, D. C has C12. K95: in A's main Z𝒯 (A:85); supplement for B and D; cited by C. Proposal: supplement |
| S-KERNEL | N9 kernel facts, graph, start sampler, minorisation: K20, K21, K08, K09, K22, K103 | B (S5), A (S6/S10), D (S2/S8), C (C10/C11) |
| S-CERT | Local search, certificate semantics, B&B soundness, perturbation: K64, K73, K74, K05, K108 | A, B, D. C withdrew K73's region certification (C:44). Proposal: K73 is stated without the region-certificate clause |
| S-LIM | Limitations as theorems: K79, K81, K100, K101; K99 qualitative remark | A, B, D. C cites them |
| S-POOL | Pooling, equal-weight PIP, R_eff: K49, K50, K54, K56, K57 | A, B, D. C cites them, with K57 FW (C:28). Proposal: supplement |
| S-IDENT | Restricted-ESS coverage identity, TI/KL/TV calculus: K25 lemma, K104, K55, K103 | All four in some form (C has C15) |
| S-BLOCKS | Separation ⇒ groups kept; SIZE ⇒ equality: K07, K14, K06 | All four (C has C11) |
| S-OUT | Output-event validity, worker equivalence, stacking: K77, K78, K83–K86, K63 | A (S6), D (S4), C (C13). B places K63/K86 in main M1/M6 (B:81, B:125) as clauses |
| S-STGI | Ideal-grid and conditional stage clauses: K29 conditional on (LL), K30 ideal | A (S11), B (STG(f)), C (C14), D (S10) |
| S-REP | Reporting corollaries for Ĵ and ε̂ (§2.5) | C's C16 (C:359); the others put them in §R5 |

### 2.3 The §5.3 package, M2 (proposal assembled from the checked clauses)

**(a) Discrepancy half** (HQ Q1(a)).
- **Hypotheses:**
  - C's computational specification A (C:50): the shipped prior and hyperparameters, the actual partition and tables, exact arithmetic, and a successful frozen calibration record.
  - The matrix domain (C:64), all computed from the design and data:
    - a = nz′H_D⁻¹z/Q̄ < 1;
    - δ_A = ‖A_D^{−1/2}EA_D^{−1/2}‖ < 1;
    - δ_H = ‖(n+1)H_D^{−1/2}EH_D^{−1/2}‖ < 1;
    - r = δ_H·a/[(1−δ_H)(1−a)] < 1.
- **Definitions** (C:65):
  - C_σ = νa²/[2(1−a)];
  - b_X = (K/2)[−log(1−δ_A) − log(1−δ_H)] − ν·log(1−r);
  - D_* = C_σ + 2b_X;
  - d_σ(S) = ν[Σ_b log(1−x_b) − log(1−Σ_b x_b)].
- **Then:** d = d_σ + d_X, with 0 ≤ d_σ ≤ C_σ (σ²-coupling) and |d_X| ≤ b_X (cross-block) (W2PC2:101). Also KL(π‖π₀), KL(π₀‖π), J ≤ D_*.
- The η-form alternative from WS3/WS4 (VERIFIED, CHK §§3–4) applies where its hypotheses hold.
- Evidence: W2PC2 §0 item 1 (0 violations on 104 designs); W2PC1 A/B/D (a) TRUE-AS-WRITTEN.

**(b) Bridge-form stability** (HQ Q1(b) + Q5).
- Per-stage χ²(q_{u+Δ}‖q_u) ≤ e^{ΔD_*} − 1.
- Four-normaliser transfer of 1 + χ², with factors e^{±4η}.
- Normalised first-stage evidence variance.
- Doeblin constants.
- M₂ ≤ e^{D_*} on every successful coded grid (pathwise W bounds).
- **Stage count:**
  - **The sandwich.** T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}). Its scope (W2PC1:55, 81):
    - the comparison is at exact frontiers;
    - a fixed, common, nonempty V and common pilot targets;
    - .9e^{4η} < 1;
    - the baseline is the same-data block-diagonal d_σ computation, on a fixed partition;
    - for the coded grid, the resolution qualifications (2^{−60} bisection and the 10^{−12} snap/validation).
  - **Local constancy** at non-critical thresholds.
  - **Integer bound and continuous envelope** (C:141, 274; W2PC2:105). Under C8's premises, including a global range bound D_* and 2^{−60} ≤ h/2:
    - the integer bound T ≤ 2⌈D_*/c_ρ⌉ + 2;
    - the **continuous envelope** T ≤ 4 + 2D_*/c_ρ;
    - if D_* = 0, then T = 1.
  - The checked fallback is T ≤ P + ⌈D_*/c_ρ⌉ + 1.
- **Q5 condition (1), to be written as statements:**
  - On the fixed-partition family, the bounds are continuous in ε: η(ε) → 0 as ε → 0 (and b_X(ε) → 0 as ε → 0 on C's family), the transfer factors e^{±4η}, the Doeblin constants, and the χ²/M₂ envelopes through D_*.
  - Lipschitz constants are given where the seat's derivation supplies them.
- **Q5 condition (2), to be written as a statement:** "T(ε) is a step function of ε. It can jump at critical thresholds: PC1 exhibits an actual design with one-sided baseline counts {2, 4} and T = 3 at ε = 10⁻⁵. 'Stable stage count' means the sandwich, and nothing more." 
- **Evidence:** W2PC1 A/B/D (b)(i),(ii),(iv) and the sandwich TRUE-AS-WRITTEN; W2PC2 §0 item 2 (envelope against the coded pilot, 600 runs).
- **Removed** (W2PC1 adverse rows):
  - A's zero-range clause: use max{1, ·};
  - D's two-value jump corollary: replace it by the integer interval;
  - B's "every constant tends to its BO value" for T: local constancy only;
  - A's growth exhibit.

**(c) One-shot refutation** (HQ Q1(c), met).
- WS6(d) with its CHK amendment: χ² divergence at zero cross-block dependence; the TV clause in the bounded-block setting.
- WS7 with its CHK amendment: the masked obstruction, whose H3 / joint-ratio premises are instantiated on LH.

**Scale disclosure** (not a theorem).
- Useful constants need ε ≲ n^{−1/2}/p, with signal energy O(√n), on the exhibited family.
- A sharp necessity statement is future work (§2.4).

**IC3.** Both families are SMC-dispatched with the method's own partition (W2PC2 §0 item 3):
- C's family at ε = 1/(np), where the cross-block term is negligible;
- C's family at ε = n^{−1/2}/p, where b_X ≈ 0.35 is visible.

The finite exhibits of A, B and D are cited as component checks.

**Placement of B's leakage clauses** (F), (S): a supplementary leakage corollary. A puts them in the supplement (A:20). B and D keep them inside the card (SBS2 U1 D4). Proposal: supplement, since the main card is already long (R3-5).

### 2.4 FUTURE_WORK (proposal; union of the seats' lists, SBS2 U3, with reasons)

- **Seat-proposed items:**
  - K13: start-mode consistency under orthogonal blocks and a σ²-inflated beta-min margin. Needs TG4-type probability bounds not supplied (R0_DIFF K13).
  - K24: polynomial mixing of the φ = 1 round (YWJ transfer). N10 OPEN.
  - K23: Dirichlet/spectral comparison. Its only consumer, K24, is deferred. It is FW for A and D, supplement for B, cited by C; proposal FW.
  - K31 (Conjecture P OPEN).
  - K58: masked consistency of the equal-weight PIP/MPM. It reduces to population delivery, and FMP-DELIVPOP is OPEN.
  - K59: R vs N at fixed total particles. PROOF SKETCH only (A:240).
  - K71 ((b1-LH-iid) GAP).
  - K75: NP-completeness for the fixed prior and penalty. Needs a score-specific reduction that has not been supplied.
  - K92: a separation from single-chain flip/swap MCMC. The moat construction and the accuracy-matched comparator are unproved; speed-up claims are empirical by decision (D:224).
  - K82 (delivery P(U) → 0; no route).
  - K94 (finite-n Π(X): envelope GAP).
  - K99 quantitative (k-way barrier unproved).
  - K107 (validated arithmetic; N16 OPEN).
  - K80 (flag power: no sampling law for the flags). It is drop / "nothing provable" for A and D, FW for B and C; proposal FW, with the reason "flags are heuristics by decision; no sampling law".
- **Scope items:**
  - N12 / exponential p.
  - Hellinger / predictive contraction (Song–Liang Thm 1).
- **New this round:**
  - **SL analytic separation** (K97, if R3-3 confirms).
  - **A sharp ε-scale necessity statement for §5.3.** All three proposed forms are COUNTEREXAMPLEs, and C's is a range obstruction for the D_* route only.
- **Already listed:** FW1 (frequentist coverage) and FW2 (masked final-estimate TV/KL).
- **Drop, with reasons:**
  - K12: a test oracle, not a guarantee. A, B and D drop it; C would defer it.
  - K34: TI evidence is not in the method; the Ĵ half ships as reporting (§2.5). A, B and D drop it; C would defer it.
  - K66: HP3 landscape, PARTLY-FALSE (C3-PGD, CEX-localmax(A2)).
  - K67: relies on K66.
  - K91: the particles-vs-depth speed-up; no accuracy-matched comparator, and OPW2-cex refutes the perfect-mixing formula (D:224; A:240).
  - K98: naive merge, KNOWN-FALSE (SHARE-M(b), FD-NM).

### 2.5 Run-card definitions (HQ Q4; proposal for AMENDMENT_HQ_02)

**Ĵ: the form of B, C and D** (B:244–245; C:293–296; D:178–179).
- Definition: Ĵ := Σ_r Ẑ_r·d̄_{r,meas} / Σ_r Ẑ_r − (1/R′)·Σ_r d̄_{r,0}.
  - d̄_{r,0} is island r's mean of d over its initial iid start particles.
  - d̄_{r,meas} is its measured-round mean of d.
- Identity: J = E_π d − E_{π₀} d (KNOWN—CITE).
- Finite-R′ bound: C16, TRUE-AS-WRITTEN (W2PC2).
- Label (C:296): "post hoc Monte Carlo estimate".
- Seat A's trapezoid-TI form (A:198) is an alternative. W2PC1:155 marks its definition / T-J1 **AMBIGUOUS / GAP**. It must specify pre-resampling particles with their incremental weights, and must not reweight post-mutation states. T-J2/T-J3 have separate TRUE verdicts. Chair's proposal: B/C/D's form (3 of 4).

**Leakage proxy** (all four):
- ε̂_× := max over b ≠ b′ of |r_jl|, with label `cross_block_rmax`;
- companions:
  - κ̂ := min_b λ_min(R_{C_b}) (A, D);
  - δ̂ := (K − 1)·ε̂/κ̂ (D:182). A uses δ̂ := K·ε̂/κ̂ (A:200). The chair proposes D's (K − 1) form;
  - ū̂, the maximal fit fraction on V (D:182).
- the derived η̂ is printed "n/a" unless the domain below holds.

Theorems about it:
- ε_S ≤ (|S| − 1)·ε̂/κ̂;
- the global discrepancy bound sup|d − d_σ| ≤ η(δ̂) holds only on the domain κ̂ > 0, δ̂ < 1, ū̂ < 1 and δ̂ū̂ < (1 − δ̂)(1 − ū̂), with "n/a" otherwise (W2PC1:157, 165; D T4/T5). A's residual-margin form (A:200) is an alternative only if stated with its own domain;
- **drop D's T6 (NEC):** COUNTEREXAMPLE, W2PC1.

Also:
- **Repair:** B's T2 needs κ > 0, δ < 1, ū < 1 and δū < (1 − δ)(1 − ū), with "n/a" on failure (W2PC1 B.R5(ii)).
- **Drop D's "V rescaling" clause:** COUNTEREXAMPLE (W2PC1 D.R5(i)).

**Implementation note** (W2PC2 §0): the per-particle d values are not retained today. A read-only accumulator is needed. It reads no random numbers and has no feedback, so it stays within HQ Q4's conditions.

### 2.6 Growth rates (agenda 7; the explicit edit under ground rule 5)

**R′ stacking** (optional configuration), on families where D_* = O_P(1):
- **(i)** R′_n = 4⌈log₂(n + p + 1)⌉, for any fixed finite set of declared summaries. A and B write ⌈log₂(n + p)⌉ (A:206; B:254); D writes ℓ = ⌈log₂(n + p + 1)⌉ (D:192). Proposal: D's form, which avoids log₂ 1 at tiny sizes.
- **(ii)** R′_n = 4⌈(n + p)⁶/4⌉, for simultaneous control over ≤ (n + p)² declared summaries (C:321; B:254).

W2PC1 item 6 and W2PC2 find both TRUE-AS-WRITTEN on C's family.

**No growth needed:** ℓ = ⌈log₂(n + p + 1)⌉ as shipped suffices on LH. L = max{4, ⌈log₂(n + 1)⌉} as shipped. No N edit (all four, SBS2 U8 item 7).

**Status:** both rates are **proposed configurations**, for confirmation in Round 3 and then recording in AMENDMENT_HQ_02. "Shipped R′ = 4" carries only the fixed-R statements (PC2 W1 §0 item 4).

### 2.7 Binding-goal safeguards (carried into the charters)

- **§13.1** (K46/N1): if the general measured-record identity cannot be closed, the narrower checked theorem ships (marginal records, fixed finite classes), and the unmet §13.1 goal **escalates to HQ** (C:76, C:404).
- **§5.3** (M2): if both the general D_* route and the explicit correlated-family route fail, the unmet goal **escalates to HQ** (C:404; HQ Q1, `2026-11-04_HQ_RULINGS_Q1-Q4.md`:7). An orthogonal-only substitute does not close it.
- **§5.4:** HQ Q3's fallback set (SYNTH_R1 §0.1) plus the masked statement in M4. FW2 is not binding.

## 3. Statement repairs required by check wave 2 (for the final cards)

| Card · clause | Verdict (W2PC1) | Required final form |
|---|---|---|
| A.R3(b)(iii) zero range | COUNTEREXAMPLE | max{1, ⌈range/const⌉} |
| A.R3(b)(iv) | NEEDS-HYPOTHESIS | M₂ is an upper bound only, not an e^{cη} comparison to the BO M₂ |
| A, B, D necessity propositions | COUNTEREXAMPLE | Removed; FUTURE_WORK (§2.4) |
| A.R3 growth exhibit | NEEDS-HYPOTHESIS, DESIGN-FAILS | Use C's family |
| B.R3(b) continuity sentence | NEEDS-HYPOTHESIS | Local constancy at non-critical thresholds (Q5) |
| D.R3(b)(iii) jump corollary | COUNTEREXAMPLE, IMPLAUSIBLE | Integer interval [T_bd(.9e^{−4η}), T_bd(.9e^{4η})] |
| SL cards (A.S2, B.S1, D.SL′(b)) | NEEDS-HYPOTHESIS, NOT REPAIRED | → FUTURE_WORK (R3-3) |
| B.R4 M₂ aside | NEEDS-HYPOTHESIS | Remove the aside |
| B.R5(ii) T2 | NEEDS-HYPOTHESIS | κ > 0, δ < 1, ū < 1, δū < (1 − δ)(1 − ū); "n/a" otherwise |
| D.R5(i) V rescaling | COUNTEREXAMPLE | Removed |
| D.R5(ii) T6 | COUNTEREXAMPLE | Removed |
| A.S9, B.S6 duplicate limit | COUNTEREXAMPLE without p = 2 | PIP = E[number selected in the group]/d; the numeric limit (2/3) only for p = 2; with an orthogonal null it is 3/5 |
| D.M3′ status | flag (b) | Restore MZ-C1's "candidate, not reviewed, not adopted", AUTHOR-ONLY |
| C3 (K69), C7 (K87/K88) audits | GAP, NOT REPAIRED (W2PC2) | They stay as named implementation premises (LS0/GUARD-W/emitted centre; execution DAG) in the charters |

## 4. Remaining disagreements (for Round 3)

| # | Item | Positions | Settled by |
|---|---|---|---|
| R3-1 | The M8 slot | (i) Prop D main (C); (ii) standalone V+ (A, B, by splitting M1); (iii) 7 main | Each seat's choice, with reason; IC5/objective (2) noted |
| R3-2 | M1: one theorem or two (V+ and H) | A, B two; C, D one | Each seat's choice; tied to R3-1 |
| R3-3 | SL (K97) | FW (C); supplement (A, B); main (D) | NOT REPAIRED in all three checked cards; proposal FW |
| R3-4 | Minor placements | K63/K86: main clauses for B (and A/D headers) vs supplement S-OUT. K23: FW vs supplement. K80: FW vs drop. K12/K34: drop vs FW. K33 in STG or S-IDENT. K95 main (A) vs supplement | Proposal in §2.2/§2.4; object only with a reason |
| R3-5 | B's leakage clauses (F), (S) | Supplement (A) vs inside M2 (B, D) | Proposal: supplement corollary |
| R3-6 | Ĵ form | B/C/D form vs A's TI form | Proposal: B/C/D form |
| R3-7 | Song–Liang wording, Thm 2 and Cor 2 | See §1 D15 | Final COVERAGE_MATRIX wording per item |
| R3-8 | Clause placements still split | **K29:** A supplement (S11), B supplement STG(f), D supplement conditional on (LL); C FUTURE_WORK (C:19). **K30:** A supplement (S11), B main STG, D main STG′, C supplement C14. **K27:** A, B main STG; D supplement (D:21); C supplement C8. **K57 general accuracy:** A, B, D supplement; C FUTURE_WORK (C:28). **K70:** A, B main variant clause; D supplementary corollary (D:25); C attributed variant. **K73:** A, B, D supplement; C withdraws the operational region certification (C:44). Cited foundations (K28, K47, K60, K61, …) are not numbered supplement claims | Proposal in §2.1–§2.4; object only with a reason |

## 5. Round 3 agenda (frozen at dispatch)

1. **Confirm or object**, item by item, to §2 (2.1–2.7) and §3. Answer R3-1 to R3-8 (≤ 60 words each).
2. **Agenda 12, the HQ plan:**
   - the dependency graph between the final theorems and lemmas;
   - launch waves of 3–4, foundations first;
   - for each main theorem, a charter: goal, final statement, key lemma, fallback, stop rule, Lean core, check plan, numerical companion (≤ 20 seeds).
3. **Final card drafting:** each seat drafts final cards for its assigned theorems (assignments in `ROUND3_BRIEF.md`).
4. **"Nothing missing":** confirm that no proposal goal, Song–Liang item, THM-INV cell or N-obligation is left without a theorem, a FUTURE_WORK entry with a reason, or a cited lemma; or name what is missing.

## 6. Correction log (audit `SYNTH_R2_AUDIT.md`, PASS WITH CORRECTIONS; v1 kept as `SYNTH_R2_v1.md`)

| # | Change |
|---|---|
| 1 | §1 D15 rewritten: shared restrictions and the remaining Thm 2 / Cor 2 differences; new R3-7 |
| 2 | §2.1 heading: 6 shared + STG proposed + optional slot; M7 basis "a proposal, not agreement" (C:143, 361) |
| 3 | §2.3(a): computational specification A, the matrix domain and the definitions of C_σ, b_X, D_*, d_σ added (C:50, 64, 65) |
| 4 | §2.3(b): the integer bound under C8's premises (2^{−60} ≤ h/2), then the continuous envelope 4 + 2D_*/c_ρ |
| 5 | §2.3(b): sandwich scope restored (exact frontiers, fixed common nonempty V, same-data d_σ baseline, fixed partition, resolution/snap); Q5 (1), (2) written as statements |
| 6 | §2.5: A's TI form reported as AMBIGUOUS/GAP (W2PC1:155) |
| 7 | §2.5: (K − 1) attributed to D; A uses K; adoption marked as the chair's proposal |
| 8 | §2.5: full domain κ̂ > 0, δ̂ < 1, ū̂ < 1, δ̂ū̂ < (1 − δ̂)(1 − ū̂), "n/a" otherwise |
| 9 | §4: new R3-8 (K29, K30, K27, K57, K70, K73 placements; cited foundations distinguished) |
| 10 | §2.6: rates are "proposed configurations", not adopted |
| 11 | §2.4: K13, K24, K23, K58, K59, K75, K92 described separately with reasons; drop reasons for K12, K34, K66, K67, K91, K98 |
| 12 | New §2.7: binding-goal safeguards (§13.1, §5.3, §5.4) with seat-line traces |

