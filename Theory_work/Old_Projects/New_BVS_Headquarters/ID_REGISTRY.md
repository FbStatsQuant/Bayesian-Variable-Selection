# ID_REGISTRY: every stable archive ID

Two disjoint ID spaces:
- **Part A, final state** (two-digit IDs): TH01–TH22 (TH01–TH08 = paper-1 main cards M1–M8; TH09–TH20 = supplement cards; clause rows like TH01.a), CJ01–CJ27 = FW1–FW27, DR01–DR06 drops, LIM01–LIM09 inherent limitations, OB01–OB17 obligations N1–N17, DF definitions, RL HQ rulings, MD method-meeting decisions, DS dissents, CL cited lemmas. Defined in `02_theory.md`.
- **Part B, campaign history** (three-digit IDs ≥ 101): TH101+ theorems/propositions, LM101+ lemmas, CJ101+ conjectures/hypotheses/open targets, RF101+ refuted or false claims, CE101+ counterexamples. Defined in `02b_theory_campaign_history.md`. Part B ends with an alias index from native names (T03♯, Theorem A, BG3, EXP′, …) to IDs.

To find any result: `grep -n 'native name' ID_REGISTRY.md`.

---

> **Archive note.** In this archive, "02a" means `02_theory.md` (final state), "02b" means `02b_theory_campaign_history.md` (campaign history), and "REG-A"/"REG-B" or "registry A/B" mean parts A and B of `ID_REGISTRY.md`. Paths like `branch_snapshots/...` and `transcript/...` are relative to this folder.

# ID registry A (final state): method v3.1 and the paper-1 theorem list

Companion of `02_theory.md` (02a) and `notation_and_conventions.md`. One row per ID. Columns: archive ID | native name(s) | kind | one-line plain description | status (exact) | defining file and section | positions.

Conventions. "Status (exact)" is copied from the cited source (card status rows, MINUTES, FUTURE_WORK); for the 8 main cards it is the card's own Status row, verbatim. Clause rows (e.g. TH02.b6) carry the clause-specific part of the card's status words where the card attaches one, otherwise the status block of the clause group. File paths are relative to `branch_snapshots/` (TLF = MEET-THM/THEOREM_LIST_FINAL.md). The descriptions are plain-language summaries by the editor; the exact statements are in 02a. No ID here is ≥ 101 (the other drafting agent uses 101 upward).

ID ranges used: TH01–TH22 (+ clause rows TH01.a … TH08.e), CJ01–CJ27, DR01–DR06, LIM01–LIM09, OB01–OB17, DF01–DF25, RL01–RL06, MD01–MD13, DS01–DS06, CL01–CL23.

| archive ID | native name(s) | kind | one-line plain description | status (exact) | defining file and section | positions |
|---|---|---|---|---|---|---|
| TH01 | M1 · Theorem V/H (validity of v3.1 and accuracy of reported bounded functionals); K46, K32, K86, K35, K36, K50, K51, K52, K48, K62 | theorem | Validity of v3.1 (island identities, frozen-𝓒 contract, output event) and accuracy of reported bounded summaries (islandwise bound, finite-R′ bound, declared classes, decision transfer, growth-rate asymptotics) | T12, T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N9K: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT; N1: PROOF SKETCH; A1new: PROOF SKETCH (NEW-SYNTH); FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)); PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r] = π(h) is still a premise'; MA-PropP: PROVED (elementary), author-only; IND-T: PROVED (SF: none; XF: VERIFIED* (A-REV1)); LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)); CEX-guard: COUNTEREXAMPLE; N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT); T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); (h), (i): PROVED (by this seat, unchecked). | MEET-THM/THEOREM_LIST_FINAL.md Part I M1, lines 94–129 (R3_A.md:112–137); charter HQ_CHARTERS/M1.md | [pos 1626], [pos 1639], [pos 1650] |
| TH02 | M2 · Theorem WS, the §5.3 package; K102, K10, K11, K25, K53; K103/K104; K27 | theorem | §5.3 package: (a) discrepancy between start and posterior controlled by cross-block terms plus σ²-coupling; (b) bridge-form stability incl. stage-count sandwich and step-function statement; (c) one-shot reading is false (ONE-SHOT) | OWS-WS3, OWS-WS4: PROVED (SF: none; XF: none) + CHK "VERIFIED (PC1, cross-family, line by line)". OWS-WS6d, OWS-WS7: PROVED (SF: none; XF: none) + CHK "VERIFIED WITH AMENDMENT". OWS-WS1: PROVED, AUTHOR-ONLY. FD-W1: PROVED, XF VERIFIED (A-REV4). AREV9-OWSTAB: "VERIFIED under H-ORTH exactly as stated" (not used beyond H-ORTH). Seat C's D_* decomposition and actual-grid moment: PROOF SKETCH (NEW-COMP); W1PC2/W2PC2 TRUE-AS-WRITTEN (statement sanity, not a proof). (b2)–(b4), (b6) assemblies: PROVED (by Seats A/B/D, unchecked), W2PC1 TRUE-AS-WRITTEN. C8 pilot extension: PROOF SKETCH, unchecked (W2PC2 PLAUSIBLE); T26BUD-G: PROVED, deterministic, AUTHOR-ONLY. (b7): PROVED (by this seat, unchecked). T03: PROVED-LOCKED; T27(i): PROVED-LOCKED, CONDITIONAL. OWS-WS6e: CONJECTURE; OWS-WS8d: OPEN (neither used). | MEET-THM/THEOREM_LIST_FINAL.md Part I M2, lines 136–180 (R3_B.md:151–187); HQ_CHARTERS/M2.md | [pos 1614], [pos 1624], [pos 1626], [pos 1650] |
| TH03 | M3 · Theorem START; K15, K17, K18, K10 (K16 supplementary) | theorem | Deterministic start mass, exact factorization, dilution, σ²-coupling decomposition, and the masking law on LH | Status: deterministic: T22(i)(ii)(iv): **PROVED-LOCKED**. DIL-E: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. DIL-E1: **PROVED; SF: none; XF: VERIFIED* (A-REV9)**. Status: statistical: T27(i): **PROVED-LOCKED, CONDITIONAL**. Thm3/4-EXP: **PROVED; SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)**. Thm5-LH: **PROVED; SF: VERIFIED (W3-VEXP); XF: none; SAME-FAMILY-ONLY**. Status: coupling/assembly: OWS-WS3: **PROVED; SF: none; XF: none; AUTHOR-ONLY** in the inherited ledger; CHK separately records **VERIFIED (PC1, cross-family, line by line)**. Final assembly: **PROOF SKETCH, unchecked**. | MEET-THM/THEOREM_LIST_FINAL.md Part I M3, lines 187–227 (R3_C.md:144–177); HQ_CHARTERS/M3.md | [pos 1626], [pos 1650] |
| TH04 | M4 · Theorem Z𝒯 and the certificate card, with the masked-regime statement; K42, K43, K45, K44; K36, K78; K95 cited | theorem | Deterministic two-sided brackets from the reported store, retention at δ₁ < ½, analytic envelope, output-event certificate, and the masked-regime statement (HQ Q3) | MZ-P3: "PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery"; "candidate: not reviewed, not adopted"; AUTHOR-ONLY. N13: PROVED (PC1 claim 5). PC1c5: (a) PROVED, ½ sharp. N17: PROVED (PC1 claim 1; PC2 C1(c)). PC1c2: PROVED for the potential run; N6(a) output form CORRECT WITH AMENDMENT; N6(b) PROVED modulo premise (i) (GUARD-W not audited). LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)). CEX-guard: COUNTEREXAMPLE (XF VERIFIED*). OCERT-C1: XF ERROR as quantified (O-VCERT R1 wording used). T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)). Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none), SAME-FAMILY-ONLY. T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)). (f) assembly: PROOF SKETCH (seat-assembled; W2PC1/W2PC2 TRUE-AS-WRITTEN as an assembly). | MEET-THM/THEOREM_LIST_FINAL.md Part I M4, lines 235–271 (R3_B.md:189–216); HQ_CHARTERS/M4.md | [pos 1614], [pos 1626], [pos 1650] |
| TH05 | M5 · Theorem HPM; K72, K69, K65, K68; K63 hyp.; K70 variant; K82 remark | theorem | Composition bound for the reported HPM at every n; Theorem A / LS-score; reported HPM with LS0 on LH (b1-LH); labelled variants (a-fav), (b2-LH) | Thm4-C1 "PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none)"; T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; N200 "PROVED (elementary, every n); Π(X) upper bound OPEN" (author-only); TheoremA "PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2))"; LS-score "PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8))"; T38-b1-LH "PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))" (registry ⚑ CONFLICT on the iid sub-claim, excluded); Thm-b1 "PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8))"; T38-(a) "PROVED-UNDER (SF: VERIFIED* (inputs); XF: none)"; B2E-B2LH "PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7))"; STAB-cert(A7) "REFEREE (Astra-authored)"; PART-ThmA "PROVED (XF: VERIFIED* (A-REV9))"; N3 "OPEN"; Thm5-LH (input via M3) "PROVED (SF: VERIFIED (W3-VEXP); XF: none)" SAME-FAMILY-ONLY. Assembly: PROOF SKETCH (by this seat, unchecked). **Fidelity:** v3.1 with LS0 (METHOD #8) for (0), (a), (b1-LH); any frozen grid; pooling not involved (scored-set maximum); (b2-LH) is v3 without LS0, labelled; (a-fav) is an iid-draw variant, labelled. | MEET-THM/THEOREM_LIST_FINAL.md Part I M5, lines 279–306 (R3_D.md:141–158); HQ_CHARTERS/M5.md | [pos 1626], [pos 1650] |
| TH06 | M6 · Theorem SEP + Lemma KL; K19, K106, K105 | theorem | Start-only discovery obstruction (LH threshold p²n), singleton second-moment bound for one-shot evidence, and Lemma KL | SEP-A/SEP-B: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. KL: **PROOF SKETCH (NEW-SYNTH)**, **AUTHOR-ONLY** in IDX. Statement checks remain TRUE-AS-WRITTEN; they do not upgrade KL. Final assembly: **PROOF SKETCH, unchecked**. | MEET-THM/THEOREM_LIST_FINAL.md Part I M6, lines 313–347 (R3_C.md:179–206); HQ_CHARTERS/M6.md | [pos 1626], [pos 1650] |
| TH07 | M7 · Theorem STG; K26, K25, K27, K30, K33; K28 cited | theorem | Stage laws of the coded grid: monotonicity/termination, restricted-ESS coverage identity, interval inequality and stage-count bound, ideal-grid crossing log₂A₀ + O(1) | STG-G, STG-L0, STG-L1: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic (AUTHOR-ONLY, W2PC2:155); STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)), explicit decimal constants GAP (W2PC2 C14); STG-L: PROVED (SF: none; XF: none); ConjP: OPEN; STG-cexW2: COUNTEREXAMPLE; OWS-WS7(d): PROVED (SF: none; XF: none) + CHK VERIFIED WITH AMENDMENT; (b), (c): D/E proposals, TRUE-AS-WRITTEN (W1PC1:192–193); (c′): PROOF SKETCH (Seat C, unchecked), W2PC2 TRUE-AS-WRITTEN; STG-F: PROVED (SF: none; XF: none), cited only (K29 FW). | MEET-THM/THEOREM_LIST_FINAL.md Part I M7, lines 355–387 (R3_A.md:139–162); HQ_CHARTERS/M7.md | [pos 1624], [pos 1626], [pos 1650] |
| TH08 | M8 · Proposition D; K87, K88, K89, K06, K64; K90 remark | proposition | Island-level work, depth and width accounting (final run, calibration, searches), polynomial work and Brent scheduling, ceilings; no speed claim | MA-PropD "PROVED (counting, given the code's structure)" AUTHOR-ONLY; T32(i) "PROVED (SF: VERIFIED (W7-SEC); XF: none)", displayed rate GAP (A-REV5), registry ⚑ CONFLICT marker carried; Cost-T38 "PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))"; calibration share "seat-derived, unchecked" (N15); assembly PROOF SKETCH (by this seat, unchecked). **Fidelity:** island level, v3.1 as shipped; "depth free of N, H, R" struck (MEET-v31 decision 6); K88's particle-parallel critical path is v3.2 and not claimed. | MEET-THM/THEOREM_LIST_FINAL.md Part I M8, lines 395–421 (R3_D.md:160–177); HQ_CHARTERS/M8.md | [pos 1304], [pos 1626], [pos 1650] |
| TH01.a | M1(a) Validity [cited] | theorem | Each elementary move γ_φ-reversible; random-order round q_φ-invariant and self-adjoint; draw_pi0 and Z̄₀ exact; E[Ẑ_r\|𝒞] = Z; E[Ẑ_r PIP̂_rj\|𝒞] = Z·PIP_j | T12, T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N9K: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1550], [pos 1593], [pos 1626] |
| TH01.b | M1(b) Lemma N1 | lemma | E[Ẑ_r H_r(h)\|𝒞] = Z·π(h) with H_r the plain measured-endpoint average (obligation OB01) | N1: PROOF SKETCH | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1626] |
| TH01.c | M1(c) Contract | theorem | (a),(b) hold conditionally on any successful frozen 𝒞; any R′ declared before stream 10 keeps them; adaptive R′ or conditioning on completion need not | CEX-guard: COUNTEREXAMPLE; W1PC1:127 AMBIGUOUS → "need not" (W2PC1:92 REPAIRED) | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1626] |
| TH01.d | M1(d) Output event | theorem | P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05, never conditional on 𝒪 | N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT); LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)); GUARD-W audit open | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1626] |
| TH01.e | M1(e) Islandwise bound | theorem | Every regime and frozen grid: E[W_r·\|H_r(h) − h(S₀)\| \| 𝒞] ≤ 2δ₁, δ₁ = 1 − π(S₀) | PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r] = π(h) is still a premise' (card status row); verdict rows W1PC1:118,120; W2PC1:93 TRUE | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1626] |
| TH01.f | M1(f) Finite-R′ bound | theorem | P(\|μ̂(h) − π(h)\| > ε \| 𝒞) ≤ min{1, 4(M₂−1)/R′ + 4M₂/(R′ε²)}; second tail bound; vacuous at R′ = 4 | same as TH01.e (PC1c3: PROVED, N1 a premise); fixed data μ̂(h) → π(h) a.s. [cited] | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1626] |
| TH01.g | M1(g) Declared classes | theorem | Joint inclusions h_A on ≤ 2pB declared pairs (plain averages); interval probabilities h_I for a finite declared list, union bound; posterior-content error only, no quantile claim (HQ Q2) | verdicts W1PC1:263 (interval claim narrowed); same status block as TH01.e | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1614], [pos 1626] |
| TH01.h | M1(h) Decision transfer | theorem | Exact PIPs ≥ δ from ½ and uniform error < δ ⇒ reported MPM = exact MPM | (h), (i): PROVED (by this seat, unchecked) | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1626] |
| TH01.i | M1(i) Asymptotic with R′_n | theorem | With R′_n = 4⌈log₂(n+p+1)⌉: μ̂(h) → h(S₀) in probability, jointly with output; liminf P(𝒪 ∩ correct) = 1 − limsup P(U_n) | (h), (i): PROVED (by this seat, unchecked); T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); second rate: see U1 | MEET-THM/THEOREM_LIST_FINAL.md M1 (clause list in the Statement row, line 111) | [pos 1639] |
| TH02.a1 | M2(a1) Decomposition | theorem | Under H-DOM, d = d_σ + d_X with 0 ≤ d_σ ≤ C_σ, \|d_X\| ≤ b_X; osc_Ω d ≤ D_* | Seat C's D_* decomposition: PROOF SKETCH (NEW-COMP); W1PC2/W2PC2 TRUE-AS-WRITTEN (statement sanity, not a proof) | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1614] |
| TH02.a2 | M2(a2) Divergences | theorem | KL(π‖π₀), KL(π₀‖π), J ≤ D_*; TV(π,π₀) ≤ tanh(osc d/2); 1 + χ²(π‖π₀) ≤ e^{osc d} | as a1; W1PC1 §16 KL/TV rows TRUE-AS-WRITTEN | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1614] |
| TH02.a3 | M2(a3) Block-orthogonal case and per-model η-form | theorem | E = 0: d = d_σ ≥ 0; per-model \|d_X(S)\| ≤ η_S | OWS-WS3, OWS-WS4: PROVED (SF: none; XF: none) + CHK "VERIFIED (PC1, cross-family, line by line)"; FD-W1: PROVED, XF VERIFIED (A-REV4) | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1614] |
| TH02.b1 | M2(b1) Per-stage χ² | theorem | χ²(q_{u+Δ}‖q_u) ≤ e^{ΔD_*} − 1 | W2PC2 C2(b)·increments TRUE-AS-WRITTEN (statement sanity) | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b2 | M2(b2) Four-normaliser transfer | theorem | e^{±4vb_X} and e^{±4vη_W} bounds between same-data and block-diagonal-baseline χ² | (b2)–(b4), (b6) assemblies: PROVED (by Seats A/B/D, unchecked), W2PC1 TRUE-AS-WRITTEN | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b3 | M2(b3) First stage | theorem | 1 + N_e Var(Ẑ_stage1/…) = 1 + χ²(q_{φ₁}‖π₀) exactly; within e^{±4φ₁η} of block-orthogonal value | as b2 | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b4 | M2(b4) Doeblin constants | theorem | M_φ ≤ e^{2φη}M^σ_φ; minorisation constant ≥ e^{−2φη}/M^σ_φ | as b2 | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b5 | M2(b5) Pathwise island moment | theorem | W_r ∈ [e^{−osc d}, e^{osc d}], E[W_r\|𝒞] = 1, M₂ ≤ e^{D_*} | Seat C's D_* decomposition and actual-grid moment: PROOF SKETCH (NEW-COMP); W1PC2/W2PC2 TRUE-AS-WRITTEN (statement sanity, not a proof) | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b6 | M2(b6) Stage count: the sandwich | theorem | T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}) on exact-frontier greedy ESS-.9 grids | (b2)–(b4), (b6) assemblies: PROVED (by Seats A/B/D, unchecked), W2PC1 TRUE-AS-WRITTEN | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b6p | M2(b6′) Local constancy, integer bound, envelope (b6′) | theorem | T = T_bd(.9) for small ε off critical thresholds; T ≤ 2⌈D_*/c_ρ⌉ + 2; checked fallback T ≤ P + ⌈D_*/c_ρ⌉ + 1 | C8 pilot extension: PROOF SKETCH, unchecked (W2PC2 PLAUSIBLE); T26BUD-G: PROVED, deterministic, AUTHOR-ONLY | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b7 | M2(b7) Q5 condition (1): continuity/Lipschitz in ε | theorem | On E = εE₁: δ_A(ε) = c_Aε, δ_H(ε) = c_Hε; b_X, D_*, per-stage χ² bounds continuous, b_X Lipschitz with constant L(ε₁) | PROVED (by this seat, unchecked), elementary calculus on the checked formulas | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.b8 | M2(b8) Q5 condition (2): step function statement | theorem | "T(ε) is a step function of ε. It can jump at critical thresholds: PC1 exhibits an actual design (n = 40, p = 2, B = 1) with one-sided baseline counts {2, 4} and T = 3 at ε = 10⁻⁵." | stated verbatim in the theorem (card row (b8)); required by HQ Q5 condition (2); no proof status needed | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1624] |
| TH02.c1 | M2(c1) Zero-dependence obstruction (WS6(d) with CHK amendment) | proposition | Under G, ORTH, fixed S₀, null count m → ∞ …: D_α(π‖π₀) → ∞ in probability; χ²(π‖π₀) → ∞; TV → 0 in bounded-block setting | OWS-WS6d: PROVED (SF: none; XF: none) + CHK "VERIFIED WITH AMENDMENT" | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1614] |
| TH02.c2 | M2(c2) Masked obstruction (WS7 with CHK amendments) | proposition | If π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} and π(S₀) → 1: ESS_∞ → 0, KL → ∞, TV → 1 | OWS-WS7: PROVED (SF: none; XF: none) + CHK "VERIFIED WITH AMENDMENT"; T27(i): PROVED-LOCKED, CONDITIONAL | MEET-THM/THEOREM_LIST_FINAL.md M2 (lines 147–179) | [pos 1614] |
| TH03.a | M3(a) deterministic mass | theorem | If q < 1, π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s; ratio formula for feasible S₀ | T22(i)(ii)(iv): PROVED-LOCKED | MEET-THM/THEOREM_LIST_FINAL.md M3 (lines 197–212) | [pos 1626] |
| TH03.b | M3(b) bridge mass | theorem | inf_{0≤t≤1} q_t(S₀) ≥ min{π₀(S₀), π(S₀)} | T22(iv): PROVED-LOCKED | MEET-THM/THEOREM_LIST_FINAL.md M3 (lines 197–212) | [pos 1626] |
| TH03.c | M3(c) exact factorization | theorem | π₀(S) = A(\|S\|) ∏_b q_b(S_b) | Final assembly: PROOF SKETCH, unchecked | MEET-THM/THEOREM_LIST_FINAL.md M3 (lines 197–212) | [pos 1626] |
| TH03.d | M3(d) dilution | theorem | −log π₀(S₀) = V + C − log A(\|S₀\|) | DIL-E: PROVED; SF: none; XF: VERIFIED (A-REV9). DIL-E1: PROVED; SF: none; XF: VERIFIED* (A-REV9) | MEET-THM/THEOREM_LIST_FINAL.md M3 (lines 197–212) | [pos 1626] |
| TH03.e | M3(e) shared variance | theorem | Under block orthogonality d_X = 0 and 0 ≤ d_σ ≤ νΣ_{b<c}x_bx_c/(1−x) | OWS-WS3: PROVED; SF: none; XF: none; AUTHOR-ONLY in the inherited ledger; CHK separately records VERIFIED (PC1, cross-family, line by line) | MEET-THM/THEOREM_LIST_FINAL.md M3 (lines 197–212) | [pos 1626] |
| TH03.f | M3(f) masked law | theorem | Under G on LH, log π₀(S₀) + 2 log p + log n = O_P(1) whereas π(S₀) → 1 | T27(i): PROVED-LOCKED, CONDITIONAL. Thm3/4-EXP: PROVED; SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2). Thm5-LH: PROVED; SF: VERIFIED (W3-VEXP); XF: none; SAME-FAMILY-ONLY | MEET-THM/THEOREM_LIST_FINAL.md M3 (lines 197–212) | [pos 1626] |
| TH03.K16 | K16 placement (supplementary conditional lemma) | theorem | Cite T22(iii), favourable rate regime, with G, R, within-block SE, EXP′, VIS, NL_η, NL_avg(κ) retained | T22(iii), PROVED-LOCKED CONDITIONAL | MEET-THM/THEOREM_LIST_FINAL.md M3 (lines 197–212) | [pos 1626] |
| TH04.a | M4(a) Deterministic identities | theorem | Z_𝒯 ≤ Z; TV(π_𝒯, π) = 1 − Z_𝒯/Z; KL(π_𝒯‖π) = log(Z/Z_𝒯); Ẑ < Z_𝒯 ⇒ Ẑ < Z | MZ-P3: "PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery"; "candidate: not reviewed, not adopted"; AUTHOR-ONLY; W1PC1 §3 TRUE-AS-WRITTEN | MEET-THM/THEOREM_LIST_FINAL.md M4 (lines 249–255) | [pos 1626] |
| TH04.b | M4(b) Brackets when the truth is stored | theorem | If S₀ ∈ 𝒯: 1 − δ₁ ≤ Z_𝒯/Z ≤ 1; TV ≤ δ₁; \|PIP^𝒯_j − PIP_j\| ≤ δ₁; \|π_𝒯(h) − π(h)\| ≤ 2δ₁‖h‖_∞ | same as (a); W1PC1 §3 B.D3(b) COUNTEREXAMPLE repaired with ‖h‖_∞ | MEET-THM/THEOREM_LIST_FINAL.md M4 (lines 249–255) | [pos 1626] |
| TH04.c | M4(c) Retention (N13) | theorem | If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 and MPM^𝒯 = S₀; ½ is sharp; unqualified retention is false | N13: PROVED (PC1 claim 5) | MEET-THM/THEOREM_LIST_FINAL.md M4 (lines 249–255) | [pos 1626] |
| TH04.d | M4(d) Analytic envelope (N17) | theorem | m(S) ≤ U_m := C_n(2b₀ + yᵀy/(n+1))^{−ν}; Z ≤ Z_𝒯 + U_m[1 − Σ_𝒯 ϖ] | N17: PROVED (PC1 claim 1; PC2 C1(c)) | MEET-THM/THEOREM_LIST_FINAL.md M4 (lines 249–255) | [pos 1626] |
| TH04.e | M4(e) Output-event certificate | theorem | P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; card level ≤ 0.05; never conditional on completion | PC1c2: PROVED for the potential run; N6(a) output form CORRECT WITH AMENDMENT; N6(b) PROVED modulo premise (i) (GUARD-W not audited); LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)); CEX-guard: COUNTEREXAMPLE (XF VERIFIED*) | MEET-THM/THEOREM_LIST_FINAL.md M4 (lines 249–255) | [pos 1626] |
| TH04.f | M4(f) Masked-regime statement (HQ Q3) | theorem | On LH under M5's hypotheses: P(𝒪 ∩ {TV(π_𝒯, π) > ε}) → 0; P(𝒪 ∩ {MPM^𝒯 ≠ S₀}) → 0; surely Ẑ < Z_𝒯 ⇒ Ẑ < Z. Reading: vanishing P(output and error), not conditional success | (f) assembly: PROOF SKETCH (seat-assembled; W2PC1/W2PC2 TRUE-AS-WRITTEN as an assembly); T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)); Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none), SAME-FAMILY-ONLY | MEET-THM/THEOREM_LIST_FINAL.md M4 (lines 249–255) | [pos 1614] |
| TH04.g | M4(g) Definitional facts | definition | For a proper store KL(π‖π_𝒯) = ∞; positive-mass state absent from records makes KL(π‖π̂) = ∞; masked final-estimate TV/KL bound is FW2 (CJ02) | definitional | MEET-THM/THEOREM_LIST_FINAL.md M4 (lines 249–255) | [pos 1626] |
| TH05.0 | M5(0) Composition at every n, any X | theorem | P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n; if S₀ ∈ 𝒮⁺ and 1 − π(S₀) < ½ then Ŝ⁺ = S₀ (see integration note 4 / U5) | T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; N200 "PROVED (elementary, every n); Π(X) upper bound OPEN" (author-only) | MEET-THM/THEOREM_LIST_FINAL.md M5 (Final statement row, line 292) | [pos 1626] |
| TH05.a | M5(a) Theorem A / LS-score | theorem | Under TD′_∞ on Lat(S°), local search from C reaches and certifies S₀ within Φ(C) moves; LS0 scores S₀ within max{Φ(S°) − 1, 0} moves | TheoremA "PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2))"; LS-score "PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8))" | MEET-THM/THEOREM_LIST_FINAL.md M5 (Final statement row, line 292) | [pos 1626] |
| TH05.b1LH | M5(b1-LH) HPM with LS0 on LH | theorem | P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n) | T38-b1-LH "PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))" (registry ⚑ CONFLICT on the iid sub-claim, excluded); Thm-b1 "PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8))"; N3 "OPEN" | MEET-THM/THEOREM_LIST_FINAL.md M5 (Final statement row, line 292) | [pos 1626] |
| TH05.afav | M5(a-fav) labelled variant | theorem | Under (F) with iid π₀ draws, D_n → 0 | T38-(a) "PROVED-UNDER (SF: VERIFIED* (inputs); XF: none)"; labelled variant | MEET-THM/THEOREM_LIST_FINAL.md M5 (Final statement row, line 292) | [pos 1626] |
| TH05.b2LH | M5(b2-LH) labelled variant (K70) | theorem | Without LS0 on STAB-LH (g = 9, c = 2, ρ = 0.4, ψ = 0.2), any frozen grid, same conclusion | B2E-B2LH "PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7))"; STAB-cert(A7) "REFEREE (Astra-authored)" | MEET-THM/THEOREM_LIST_FINAL.md M5 (Final statement row, line 292) | [pos 1626] |
| TH06.a | M6(a) discovery | theorem | P(S₀ absent from all Q iid draws from π₀) = (1−a)^Q ≤ e^{−Qa} | SEP-A/SEP-B: PROVED; SF: none; XF: VERIFIED (A-REV9) | MEET-THM/THEOREM_LIST_FINAL.md M6 (lines 326–333) | [pos 1626] |
| TH06.b | M6(b) LH threshold | theorem | Q*_n = p²n: Q_n/Q*_n → 0 ⇒ miss probability → 1; → ∞ ⇒ → 0 | SEP-A/SEP-B: PROVED; SF: none; XF: VERIFIED (A-REV9) | MEET-THM/THEOREM_LIST_FINAL.md M6 (lines 326–333) | [pos 1626] |
| TH06.c | M6(c) singleton second moment | theorem | 1 + χ²(π‖π₀) ≥ b²/a; evidence estimator variance identity | SEP: PROVED; XF VERIFIED (A-REV9); CHK §2(a),(b) | MEET-THM/THEOREM_LIST_FINAL.md M6 (lines 326–333) | [pos 1626] |
| TH06.KL | Lemma KL | lemma | KL(π‖π₀) ≥ b log(1/a) − log 2 | KL: PROOF SKETCH (NEW-SYNTH), AUTHOR-ONLY in IDX. Statement checks remain TRUE-AS-WRITTEN; they do not upgrade KL | MEET-THM/THEOREM_LIST_FINAL.md M6 (lines 326–333) | [pos 1626] |
| TH07.a | M7(a) Monotonicity and construction | theorem | ρ_V monotone; bisection accepts only intervals with ρ_V ≥ 0.9; build_grid terminates; T ≤ T_e on success; greedy optimality among refinements of the retained pilot targets | STG-G, STG-L0, STG-L1: PROVED (SF: none; XF: none); W1PC1:190 TRUE; exact/minimal W1PC1:191 COUNTEREXAMPLE repaired | MEET-THM/THEOREM_LIST_FINAL.md M7 (Statement row, line 371) | [pos 1626] |
| TH07.b | M7(b) Coverage identity | theorem | ρ_full(u,v) = ρ_V(u,v)·a_u a_w/a_v², w = 2v−u; a_u, a_w ≥ 1−η ⇒ ρ_full ≥ 0.9(1−η)² | (b), (c): D/E proposals, TRUE-AS-WRITTEN (W1PC1:192–193) | MEET-THM/THEOREM_LIST_FINAL.md M7 (Statement row, line 371) | [pos 1626] |
| TH07.c | M7(c) Interval inequality and count | theorem | T ≤ P + ⌈2/h_V⌉ + 1 = P + ⌈D_V/c_ρ⌉ + 1 with resolution ≤ h_V/2; uniform full-space grid existence | W1PC1:194 COUNTEREXAMPLE repaired to P + …; (b), (c) TRUE-AS-WRITTEN | MEET-THM/THEOREM_LIST_FINAL.md M7 (Statement row, line 371) | [pos 1624] |
| TH07.cp | M7(c′) Pilot-count clause (cited from M2(b)) | theorem | P ≤ ⌈2/h⌉ + 1, hence T ≤ 2⌈D_*/c_ρ⌉ + 2; D_* = 0 ⇒ T = 1 | (c′): PROOF SKETCH (Seat C, unchecked), W2PC2 TRUE-AS-WRITTEN | MEET-THM/THEOREM_LIST_FINAL.md M7 (Statement row, line 371) | [pos 1624] |
| TH07.d | M7(d) Ideal grid (K30), labelled, not the coded grid | theorem | Dominance crossing of gap A₀ costs log₂A₀ + O(1) stages; restricted ESS alone forces only log₂(9.5ℓ₀) stages | STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)), explicit decimal constants GAP (W2PC2 C14); OWS-WS7(d): PROVED (SF: none; XF: none) + CHK VERIFIED WITH AMENDMENT | MEET-THM/THEOREM_LIST_FINAL.md M7 (Statement row, line 371) | [pos 1626] |
| TH07.e | M7(e) [cited] | theorem | √c·T*(c) → Λ_len := ∫₀¹ sd_{q_φ}(d)dφ ≤ √J as c → 0 | KNOWN—CITE Syed et al. 2024 Thm 3, Gelman–Meng 1998 | MEET-THM/THEOREM_LIST_FINAL.md M7 (Statement row, line 371) | [pos 1626] |
| TH07.f | M7(f) as-coded masked T_n | conjecture | Conjecture P, OPEN → FUTURE_WORK (K31); shipped guarantee T ≤ T_e; favourable O(1) (K29) → FUTURE_WORK | ConjP: OPEN; STG-cexW2: COUNTEREXAMPLE; STG-F: PROVED (SF: none; XF: none), cited only | MEET-THM/THEOREM_LIST_FINAL.md M7 (Statement row, line 371) | [pos 1626] |
| TH08.a | M8(a) Final run | proposition | Work = R′·N_e·(T + L + 4)·m slots; island depth = N_e·(T + L + 4)·m in ⌈R′/w⌉ waves; width R′ | MA-PropD "PROVED (counting, given the code's structure)" AUTHOR-ONLY | MEET-THM/THEOREM_LIST_FINAL.md M8 (Final statement row, line 407) | [pos 1626] |
| TH08.b | M8(b) Calibration | proposition | Work = Σ_i N_i(T_i + L_i + 4)m over executed trajectories; per tier ≤ (1 + 4I_e)H_e trajectories in work | "calibration share seat-derived, unchecked" (N15) | MEET-THM/THEOREM_LIST_FINAL.md M8 (Final statement row, line 407) | [pos 1626] |
| TH08.c | M8(c) Searches | proposition | Each local search scores ≤ (ℓ + 1)[p + k*(p − k*)] models | T32(i) "PROVED (SF: VERIFIED (W7-SEC); XF: none)", displayed rate GAP (A-REV5) | MEET-THM/THEOREM_LIST_FINAL.md M8 (Final statement row, line 407) | [pos 1626] |
| TH08.d | M8(d) Polynomial work and scheduling | proposition | For p ≤ n^A total work polynomial in n; on w workers time ≤ W/w + D (Brent) | Cost-T38 "PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))" | MEET-THM/THEOREM_LIST_FINAL.md M8 (Final statement row, line 407) | [pos 1626] |
| TH08.e | M8(e) Ceilings | proposition | Θ(p) slots per round and Θ(p²) Gram memory are not removed by islands or particles | assembly PROOF SKETCH (by this seat, unchecked) | MEET-THM/THEOREM_LIST_FINAL.md M8 (Final statement row, line 407) | [pos 1626] |
| TH09 | S-T · Theorem 1, target consistency T03♯ (K93, K04) | theorem | Posterior concentration 1 − π(S₀) = O_P(√(log n/n)) under R1, G, R, SE_λ, SE_w, BM; exact HPM and MPM consistent; large-signal inclusion without beta-min | T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 434–499 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH10 | S-TARGET · Propriety, invariance, envelopes, exact branch, odds certificate (K01–K05, K76, K95) | proposition | Shipped target proper (incl. rank-deficient); Q_S ≥ Y/(n+1); analytic envelope; affine invariance and permutation equivariance of the target; exact branch; odds certificate A ≤ η < 1 ⇒ HPM = MPM = S₀ | N17: PROVED. T01: PROVED-LOCKED (wave 3; external review queued); SAME-FAMILY-ONLY. Remaining assembly: PROOF SKETCH, unchecked. N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected) | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 504–577 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH11 | S-BLOCKS · Separation ⇒ groups kept; SIZE ⇒ equality (K07, K14, K06) | proposition | Complete linkage keeps strictly separated groups; with B < 2g_min output blocks equal groups; ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉; Σ_b 2^{\|C_b\|} ≤ p2^B/B; capped graph ≤ pB edges, no isolated vertex for p > 1 | PART-ThmA: PROVED; SF none; XF VERIFIED*. Counting/graph assembly: PROOF SKETCH, unchecked. PART-pairing remains OPEN, excluded. PART-CE2: COUNTEREXAMPLE | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 581–630 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH12 | S-KERNEL · N9 kernel facts, graph (p ≥ 2), start sampler, minorisation (K20, K21, K08, K09, K22, K103) | proposition | Move reversibility under N9's sufficient conditions, exact start sampler, minorisation Q_φ(S,·) ≥ π_φ/M_φ, tie-aware start-mode DP (K09) | N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); T09: PROVED-LOCKED (wave 1); N3: OPEN; K22, K23, K103: PROVED (by this seat, unchecked), PC1 §19 TRUE-AS-WRITTEN. C10 (K09): PROOF SKETCH, unchecked | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 634–721 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH13 | S-IDENT · Restricted-ESS coverage identity, TI/KL/TV calculus, C15-CI clause (K25 lemma, K104, K55, K103) | proposition | Terminal-law TV ≤ q^L, KL bounds, empirical TV/content for predeclared cells, and the named posterior-content credible-set clause C15-CI | C15-TV, C15-KL, C15-CI: PROOF SKETCH, unchecked (assembly); Independence-sampler foundation: KNOWN—CITE; S9: PROVED (by this seat, unchecked); OWS-WS1: PROVED (SF: none; XF: none) | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 725–827 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626], [pos 1614] |
| TH14 | S-CERT · Local search, certificate semantics, B&B soundness, perturbation lemma (K64, K73, K74, K05, K108) | proposition | `local_certified` = weak local maximum (ties allowed); ≤ (ℓ+1) scans; card R exact on completion; perturbation lemma Z̃/Z ∈ e^{±ε}, TV ≤ tanh ε | N7 L1: CORRECT WITH AMENDMENT; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*) | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 930–965 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH15 | S-OUT · Output-event validity, worker equivalence, stacking (K77, K78, K83–K86, K63) | proposition | Under stop-only GUARD-W a potential-run event with P(B\|𝒞) ≤ α gives P(𝒪 ∩ B\|𝒞) ≤ α; not P(B\|𝒪,𝒞) ≤ α | LemmaRO: PROVED; SF VERIFIED; XF VERIFIED*. CEX-guard: COUNTEREXAMPLE; XF VERIFIED*. N6 potential-run: PROVED; output form: CORRECT WITH AMENDMENT. GUARD-W: not audited | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 968–1009 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH16 | S-Z · Evidence variance, masked tails (K37–K41, K53) | theorem | E[Ẑ_r\|𝒞] = Z; exact variance identity; masked lower tail in exception-probability form; Var(Ẑ_r/Z\|𝒞) ≤ (T+1)e^{2D}/N and Var(W_r\|𝒞) ≤ e^{2·osc d} − 1 (both ship) | OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)); PC1c4: PROVED; T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)); T26 overall CONJECTURE | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 1012–1047 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH17 | S-POOL · Pooling rules, recording-marginal equal-weight bias comparison P1, R_eff (K49, K50, K54, K56, K57-P1) | proposition | Pooling rules; P1: bias of the equal-weight PIP bounded by TV of the uniformly sampled one-record marginal; R_eff | MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH; ADRAFT-ThmA Astra-only, cite Del Moral; OBG-LH-lock-general: XF ERROR | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 1050–1099 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH18 | S-LIM · Limitations as theorems (K79, K81, K100, K101); K99 qualitative remark | proposition | No transcript diagnostic certifies an unqueried mode; certified weak local max can be far below the mode; ESS = N compatible with genealogical collapse; duplicates PIP = E[#selected in group]/d (2/3 for two duplicates, fixed noise); MPM may exceed K | CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB: COUNTEREXAMPLE (constructions); INP I5 PROVED | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 1103–1138 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH19 | S-REP · Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions (K104/K11) | proposition | Ĵ estimator with finite-R′ tail bound and zero-range convention; ε̂_× = cross_block_rmax with κ̂, δ̂, ū̂, r̂, η̂ and regularized proxy bounds; labels | Reporting assembly: PROOF SKETCH, unchecked. N1: PROOF SKETCH. PC1c3: PROVED, with N1 as premise. W2P2 C16 and repaired W2P1 T4/T5 are statement/route checks, not a full proof upgrade | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 1195–1244 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626], [pos 1614] |
| TH20 | S-LEAK · B's leakage clauses (F), (S) as a supplementary corollary to M2 | proposition | (S) exact identity 1 + χ²(π‖π₀) = π(S₀)²/(π₀(S₀)q₂(S₀)) and m ≥ π₀(S₀)e^{−2·osc d} with no design-uniform lower bound; (F) favourable start under leakage 1 − π₀(S₀) = O_P(2^B√log n·n^{−κ}) | OWS-WS6(b): PROVED (SF: none; XF: none), PC1 B.D6(S) TRUE; the m lower bound: PROVED (by this seat, unchecked); (b6) OWS-WS53F: PROVED-UNDER (SF: none; XF: none); PC1 B.D6(F) TRUE / DESIGN-VERIFIED (D_B) | MEET-THM/THEOREM_LIST_FINAL.md Part II lines 1141–1192 (lemma-pack charter in HQ_CHARTERS/) | [pos 1626] |
| TH21 | S-STGI · K29/K30 (DISSOLVED) | drop | Former supplement card; K30 is M7(d), K29 → FUTURE_WORK FW23 (CJ23); conditional implication citable as attributed lemma | DISSOLVED (MINUTES §2.2, corrected) | MEET-THM/THEOREM_LIST_FINAL.md lines 830–926; MEET-THM/MINUTES.md §2.2 | [pos 1626] |
| TH22 | Thesis CD (K96) | proposition | Scoped remark after the main theorems; "there is no retained non-corollary thesis sentence" (Seat C wording) | remark, not a theorem | MEET-THM/THEOREM_LIST_FINAL.md Part III lines 1250–1294; Chair's choices item 5 | [pos 1044], [pos 1626] |
| CJ01 | FW1 | future-work | Frequentist coverage of the exact posterior's credible intervals | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW1 | [pos 1626] |
| CJ02 | FW2 | future-work | TV/KL error bound for the final pooled estimate in the masked regime | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW2 | [pos 1626] |
| CJ03 | FW3 | future-work | K13: start-mode consistency under orthogonal blocks and a σ²-inflated beta-min margin | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW3 | [pos 1626] |
| CJ04 | FW4 | future-work | K24: polynomial mixing of the φ = 1 round (Yang–Wainwright–Jordan transfer); also useful general production mixing and masked population accuracy (N10) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW4 | [pos 1626] |
| CJ05 | FW5 | future-work | K23: Dirichlet/spectral comparison of the random-order round with the random-scan mixture | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW5 | [pos 1626] |
| CJ06 | FW6 | future-work | K31: as-coded masked stage count (realised T_n; Conjecture P OPEN); N5(b): rebuild convergence within ℓ rebuilds, candidate-pair coverage / P(S₀ ∈ V), P(schedule_limit) and calibration-failure probabilities | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW6 | [pos 1626] |
| CJ07 | FW7 | future-work | K58: masked consistency of the equal-weight PIP/MPM | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW7 | [pos 1626] |
| CJ08 | FW8 | future-work | K57, general fixed-budget equal-weight accuracy (only the recording-marginal bias comparison P1 ships in S-POOL) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW8 | [pos 1626] |
| CJ09 | FW9 | future-work | K59: R vs N at fixed total particles (allocation) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW9 | [pos 1626] |
| CJ10 | FW10 | future-work | K71: (b1-LH-iid) on LH with iid final draws, also under general DELIV | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW10 | [pos 1626] |
| CJ11 | FW11 | future-work | K75: NP-completeness of the global-certificate decision problem for the fixed prior and penalty | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW11 | [pos 1626] |
| CJ12 | FW12 | future-work | K92: separation from single-chain flip/swap MCMC (moat construction) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW12 | [pos 1626] |
| CJ13 | FW13 | future-work | K82: delivery, P(U) → 0 (also delivery/resource-failure laws, P(resource_limit)) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW13 | [pos 1626] |
| CJ14 | FW14 | future-work | K94: finite-n bound on the posterior-miss probability Π(X) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW14 | [pos 1626] |
| CJ15 | FW15 | future-work | K99 quantitative: k-way barrier for cross-block masked contrasts | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW15 | [pos 1626] |
| CJ16 | FW16 | future-work | K107: validated arithmetic / rounding-error bound; production validated numerics (N16) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW16 | [pos 1626] |
| CJ17 | FW17 | future-work | K80: positive power of the E1/E2/E3 and low_empirical_ESS flags | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW17 | [pos 1626] |
| CJ18 | FW18 | future-work | N12 / exponential p: exponential-dimension contraction and selection (Song–Liang Cor 1) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW18 | [pos 1626] |
| CJ19 | FW19 | future-work | Growing support and cap non-binding (N11/N12) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW19 | [pos 1626] |
| CJ20 | FW20 | future-work | Hellinger / predictive contraction (Song–Liang Thm 1) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW20 | [pos 1626] |
| CJ21 | FW21 | future-work | K97: Song–Liang analytic separation (null-exclusion/FDR) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW21 | [pos 1626] |
| CJ22 | FW22 | future-work | Sharp ε-scale necessity statement for §5.3 | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW22 | [pos 1626] |
| CJ23 | FW23 | future-work | K29: favourable O(1) stage law, unconditional application | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW23 | [pos 1626] |
| CJ24 | FW24 | future-work | Useful two-sided masked evidence precision (N4(iii)/V11) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW24 | [pos 1626] |
| CJ25 | FW25 | future-work | Random/adaptive partition quality and study packing (N8; K71 as C pairs them), including the study generator (PART-pairing, g = 5, 2g ≤ B) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW25 | [pos 1626] |
| CJ26 | FW26 | future-work | Finite-n Gibbs discovery (HPM residual) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW26 | [pos 1626] |
| CJ27 | FW27 | future-work | Unbounded functionals: integrability extensions of M1 (§13.1) | FUTURE_WORK (deferred; reason in 02a §A5.1) | MEET-THM/FUTURE_WORK.md table row FW27 | [pos 1626] |
| DR01 | K12 | drop | Dropped candidate K12 | DROPPED. Reason: A test oracle, not a guarantee | MEET-THM/FUTURE_WORK.md "Dropped"; MEET-THM/MINUTES.md §2.4 | [pos 1626] |
| DR02 | K34 | drop | Dropped candidate K34 | DROPPED. Reason: TI evidence is not in the method (the Ĵ half ships as reporting, S-REP) | MEET-THM/FUTURE_WORK.md "Dropped"; MEET-THM/MINUTES.md §2.4 | [pos 1626] |
| DR03 | K66 | drop | Dropped candidate K66 | DROPPED. Reason: PARTLY-FALSE (C3-PGD, CEX-localmax(A2)) | MEET-THM/FUTURE_WORK.md "Dropped"; MEET-THM/MINUTES.md §2.4 | [pos 1626] |
| DR04 | K67 | drop | Dropped candidate K67 | DROPPED. Reason: Relies on K66 | MEET-THM/FUTURE_WORK.md "Dropped"; MEET-THM/MINUTES.md §2.4 | [pos 1626] |
| DR05 | K91 | drop | Dropped candidate K91 | DROPPED. Reason: No accuracy-matched comparator; OPW2-cex | MEET-THM/FUTURE_WORK.md "Dropped"; MEET-THM/MINUTES.md §2.4 | [pos 1626] |
| DR06 | K98 | drop | Dropped candidate K98 | DROPPED. Reason: KNOWN-FALSE (SHARE-M(b), FD-NM) | MEET-THM/FUTURE_WORK.md "Dropped"; MEET-THM/MINUTES.md §2.4 | [pos 1626] |
| LIM01 | Inherent limitation 1: Per-round sequential factor m = p + B + 2 | limitation | True by definition of a random-scan full-coordinate Gibbs round; inherent to the chosen kernel, not to SMC or BVS (I1) | true by definition | MEET-v31/MINUTES.md §5 item 1 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM02 | Inherent limitation 2: Every worker needs scoring access to all predictors | limitation | X or sufficient statistics, 8np bytes; a private 8p² Gram per worker is not inherent (C7) (I2) | true by definition | MEET-v31/MINUTES.md §5 item 2 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM03 | Inherent limitation 3: Masking of the product-of-blocks start built from block-local scores against the full y, under T27(i)'s hypotheses (H2, H3; verified on LH) | limitation | Law for that construction and design class only (I3) | T27(i), PROVED-LOCKED (conditional, in its design class) | MEET-v31/MINUTES.md §5 item 3 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM04 | Inherent limitation 4: No diagnostic from the observed record has a universal detection guarantee for never-visited modes | limitation | Positive one-sided certificates (e.g. Ẑ < Z_𝒯) can still detect some failures (I5) | V12 and E1c PROVED; Chatterjee–Diaconis Thm 2.1 | MEET-v31/MINUTES.md §5 item 4 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM05 | Inherent limitation 5: The properties of Ẑ behind the 95% bound imply no two-sided relative-error bound | limitation | Non-implication from the estimator's law, not data-specific; analytic bound Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} exists (I7) | T31(c), PROVED-LOCKED; PC2 C1(c), PROVED relative to it | MEET-v31/MINUTES.md §5 item 5 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM06 | Inherent limitation 6: (Moved by HQ amendment 01) Markov sharpness of 0.05Ẑ | limitation | No longer listed as inherent: seat-derived, unchecked (I8) | NOT inherent (moved); seat-derived, unchecked | MEET-v31/MINUTES.md §5 item 6 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM07 | Inherent limitation 7: Posterior misses at n = 200 | limitation | 565 strict competitor defeats of S₀ among the 2,394 completed fits (six stops): at least 565 target-mode misses (I6) | true by definition of the fixed target (N200, T07) | MEET-v31/MINUTES.md §5 item 7 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM08 | Inherent limitation 8: The cap K excludes truths with s₀ > K; a fixed allocation cannot support unrestricted growth of (n, p) | limitation | (I9(a),(e)) | true by definition (V13) | MEET-v31/MINUTES.md §5 item 8 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| LIM09 | Inherent limitation 9: The restricted ESS on V cannot bound mass outside V without further assumptions | limitation | (I9(d)) | true by definition | MEET-v31/MINUTES.md §5 item 9 (cross-ref THEOREM_REVISION_INPUTS.md §4.A) | [pos 1128], [pos 1280], [pos 1302] |
| OB01 | N1 · Measured-round island identity for general bounded h (Theorem H crux; V1(a2)) | obligation | E[Ẑ_r·H_r(h)\|𝒞] = Z·π(h) for h ∈ 𝓗, 0 ≤ h ≤ 1, measurable in (X, y, 𝓒) | PROOF SKETCH; PC1 claim 3 takes it as a premise. Binding §13.1: if it fails the goal is not met by withdrawal; HQ escalates to Felipe | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N1; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB02 | N2 · Integrated v3.1 core: Prop W, W-cal, LS0, stacking, GUARD-W | obligation | Code-audit facts plus executed replays (a) final islands bitwise equal to serial, (b) diagnostic islands bitwise, (c) LS0 leaves islands unchanged, 𝒯_new = top_c(…), (d) R′ = 4k with extra search nests the scored set, (e) GUARD-W | Lemma S PROVED. (a) PROVED by code reading, executed on smoke + 3/3 designs. (b) PROVED by code reading, not executed. (c) not in the production core. (d) PROVED (PC1 claim 6, deterministic). (e) not audited | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N2; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB03 | N3 · LS0-based T38(b1-LH) about the shipped method; e4 tie-DP invariant | obligation | P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 on LH for v3.1 with LS0; sub-obligation: tie-aware DP returns the prescribed smallest-size, lexicographically smallest maximiser | (b1-LH) PROVED (candidate), XF VERIFIED (A-REV8) for "v3 + LS0"; bridge to code = N2(c), not done. DP invariant OPEN | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N3; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB04 | N4 · Finite-R accuracy of the Ẑ-weighted PIP and μ̂(h); the constant M under masking (V11) | obligation | (i) P(\|μ̂ − μ\| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}; (ii) regime-free distance to 1{j ∈ S₀}; (iii) upper bound on M through a masked crossing | (i) PROVED, given N1 for general h or the locked identity for PIPs; (ii) PROVED (candidate); (iii) Obligation: CONJECTURE, OPEN for c ≥ 2 | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N4; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB05 | N5 · Calibration contract | obligation | (a) validity for any frozen 𝓒; (b) OPEN: rebuild convergence, P(S₀ ∈ V), P(schedule_limit), P(grid_unconverged), as-coded masked T_n (Conjecture P) | (a) assembly of T12/T31(i) (PROVED-LOCKED, conditional on 𝓒), IND-T (PROVED, XF VERIFIED*, A-REV1 only), Lemma RO; (b) OPEN | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N5; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB06 | N6 · Output-event coverage statements | obligation | (a) P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; (b) card level; (c) joint with 𝒪, never conditional | (a) PROVED (potential run; output form CORRECT WITH AMENDMENT). (b) PROVED modulo premise (i), whose GUARD-W part is the code-audit obligation N2(e) | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N6; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB07 | N7 · Certificate card G1/G2/L/R (PC2 verdicts) | obligation | Per-item semantics of the card | G1 PROVED; G2 PROVED; L1 CORRECT WITH AMENDMENT; L2 PROVED; L3 amended form PROVED; R PROVED with amendments; Card bound (C6) PROVED modulo premise (i); C6′ PROVED. Open sub-obligation SC(η_F)/VAL-FP (N16) | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N7; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB08 | N8 · PART-pairing for the study generator g = 5 (2g ≤ B) | obligation | Partition law for complete linkage + size cut + next-fit packing with equal groups 2g ≤ B | OPEN; Prop Q PROOF SKETCH; W7-PART CE2 COUNTEREXAMPLE | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N8; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB09 | N9 · V5: kernel reversibility, self-adjointness, exact start sampler (closure gate) | obligation | Each elementary move γ_φ-reversible; uniformly random order self-adjoint; start sampler exact with exact Z̄₀ | "by construction, consultant-checked, no registry row"; gate closed: N9-KERNEL "PROVED (candidate)" with exact numerical verification on production headers ([pos 1550]: 7 sub-claims; [pos 1593]: 8 sub-claims); cross-family VERIFIED WITH AMENDMENT (CHK_INHERITED) | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N9; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB10 | N10 · V10: L versus t_mix | obligation | Do L = max(4, ⌈log₂(n+1)⌉) terminal φ = 1 rounds give populations close to π? | NONE / OPEN | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N10; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB11 | N11 · ℓ versus the moves needed | obligation | ℓ = ⌈log₂(n+p+1)⌉ ≥ max{Φ(S°) − 1, 0}; caps not binding w.p. → 1 | on LH with c ≤ s₀ fixed, "eventually true" (elementary, unchecked); growing s₀: OPEN | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N11; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB12 | N12 · General (n, p) scope, per regime | obligation | Per-regime table of what theory may claim | see the table in the source; p ≤ e^{Cn^α}: OPEN, not impossible | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N12; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB13 | N13 · Retention lemma | obligation | If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 = top_{40p+1}(𝒮), HPM and MPM^𝒯 certificates equivalent | PROVED (PC1 claim 5; R2C D7) | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N13; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB14 | N14 · Stacking statements | obligation | (a) post-search nesting HPM(R′) ⪰ HPM(4); (b) every bound holds per run for any R′ declared before final randomness; (c) IND-T for streams 10..9+R′; (d) one card per record | (a) PROVED (PC1 claim 6); (c) code audit, not done | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N14; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB15 | N15 · Work and depth at the implemented level | obligation | Island-parallel depth/work account (see TH08) | Prop D PROVED (counting); calibration share seat-derived (R2A, R2B), not proof-checked | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N15; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB16 | N16 · Floating-point contract | obligation | Validated SC(η_F) for scores, Φ, M, Z_𝒯⁻, and VAL-FP(η, ε) for Ẑ at production size | OPEN. VAL-FP MEASURED at p ≤ 40 only | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N16; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| OB17 | N17 · Analytic bounds on Z and π(Ŝ) | obligation | Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} | PROVED (PC1 claim 1; PC2 C1(c)) | MEET-v31/THEOREM_REVISION_INPUTS.md §3 N17; final placement in MEET-THM/COVERAGE_MATRIX.md §(d) | [pos 1280], [pos 1290] |
| DF01 | Model, likelihood, g-prior, σ² prior | definition | y \| β_S, σ², S ~ N_n(X_Sβ_S, σ²I_n); β_S \| σ², S ~ N_k(0, nσ²(G_S + I_k)⁻¹); σ² ~ IG(a₀, b₀), a₀ = b₀ = 0.01 | unchanged in v3.1 ("Felipe's model") | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §5; MEET-v31/METHOD_v3.1_FINAL.md §1 | [pos 1302] |
| DF02 | Size prior BB(1,p) and cap K | definition | ϖ(S) = w(k)1{k ≤ K}/W_K, w(k) = ½/C(2p−1, k), K = min(p, ⌊n/2⌋) | unchanged | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §3, §5 | [pos 1302] |
| DF03 | Score m(S), evidence Z, posterior π | definition | log m(S) formula with H_S = (n+1)G_S + I, Q_S; π = ϖm/Z | unchanged | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §5; TLF D0 "Score" | file only |
| DF04 | Preprocessing / standardisation | definition | max-abs, centre, SD (n−1); constant columns dropped; duplicates kept | rule 1 changed by e3 (n ≥ 2 proposed) | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §4; MEET-v31/METHOD_v3.1_FINAL.md #25 | [pos 1251] |
| DF05 | Blocks and tables | definition | complete linkage on 1 − \|r\|, size-only cut ≤ B, next-fit packing; exact tables r_b(U) = m(U)/m(∅) | unchanged; table stage parallel (#4) | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.3; MEET-v31/METHOD_v3.1_FINAL.md #4, #34 | [pos 1107] |
| DF06 | Block-product start π₀ | definition | γ₀ = ϖ∏_b r_b(S∩C_b); π₀ = γ₀/Z̄₀ exact; exact iid sampler | kept (item 1 Outcome 2: no depth/speed claim) | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.3; MEET-v31/METHOD_v3.1_FINAL.md row 0 | [pos 1280], [pos 1669] |
| DF07 | Discrepancy d and tempering bridge γ_φ | definition | d = log BF − Σ log r_b; γ_φ = γ₀ e^{φd}; q_t ∝ γ₀e^{td} | unchanged | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.3; TLF D0 | file only |
| DF08 | Kernel moves and round | definition | m = p + B + 2 steps: Gibbs, uniform swap, neighbour swaps, independence (π₀) in random order; γ_φ-reversible | unchanged; validity N9 (OB09, TH12) | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.5 | [pos 1550], [pos 1593] |
| DF09 | Resampling, pilot, ESS 0.90 | definition | multinomial; ESS 0.90; 60 halvings | unchanged; ESS class (c) | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.6; MEET-v31/METHOD_v3.1_FINAL.md §5 row 27 | file only |
| DF10 | Candidate set V, restricted ESS, grid, rebuild loop | definition | V = top 20p by γ₀ ∪ top 20p by γ₁ ∪ {∅}; ρ_V; ≤ ℓ rebuilds | unchanged; contract #18 | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.7; MEET-v31/METHOD_v3.1_FINAL.md #18 | [pos 1130] |
| DF11 | Calibration record 𝒞, tiers, final runs | definition | 𝒞 frozen before stream 10; tiers e ∈ {0,1}; final streams 10..9+R′ | contract #18; streams extended #7 | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.8–6.9; MEET-v31/METHOD_v3.1_FINAL.md #7, #18 | [pos 1251] |
| DF12 | Islands and stacking | definition | R = 4 default; optional R′ = 4k at unchanged N_e declared before stream 10; extra search from c₄; baseline and expanded records | new in v3.1 (#7) | MEET-v31/METHOD_v3.1_FINAL.md #7; AMENDMENT_HQ_02 | [pos 1107], [pos 1639] |
| DF13 | Evidence estimator Ẑ_r, pooled Ẑ, Markov bound | definition | Ẑ_r unbiased given 𝒞; 0.05Ẑ lower bound | unchanged; card adds max{Z_𝒯, 0.05Ẑ} | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.12; MEET-v31/METHOD_v3.1_FINAL.md #14, #17 | [pos 1251] |
| DF14 | PIP rules, MPM, R_eff | definition | Primary Ẑ-weighted; secondary equal-weight; MPM threshold ½; R_eff | swap of primary/secondary (#11) | MEET-v31/METHOD_v3.1_FINAL.md #11 | [pos 1107], [pos 1251] |
| DF15 | HPM decision and local search | definition | strict max over every scored model; ties \|S\| then lexicographic; ≤ ℓ moves + one scan | unchanged; scans parallel (#3) | main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md §6.10 | [pos 1142] |
| DF16 | LS0 | definition | one local search from the start mode after the final search; no uniforms; provenance ls0 | new (#8–#10) | MEET-v31/METHOD_v3.1_FINAL.md #8–#10 | [pos 1107], [pos 1251] |
| DF17 | Reported store 𝒯, Z_𝒯 and the certificate card | definition | top store 40p+1; Z_𝒯 = Σ_𝒯 ϖm; card G1, G2, L1–L3, R | new (#13, #14; §2.1) | MEET-v31/METHOD_v3.1_FINAL.md #13, #14, §2.1 | [pos 1251] |
| DF18 | General-h accumulator 𝓗 | definition | H_r(h) after each measured round; μ̂(h) = Σ Ẑ_r H_r(h)/Σ Ẑ_r; default 𝓗: sizes, neighbour-edge pairs; d added by AMENDMENT_HQ_02 | new (#12) | MEET-v31/METHOD_v3.1_FINAL.md #12 | [pos 1251], [pos 1626] |
| DF19 | Ĵ (J_hat) | definition | Ĵ = Σ_r Ẑ_r B_r/Σ_r Ẑ_r − (1/R′)Σ_r A_r | reporting amendment | MEET-THM/AMENDMENT_HQ_02_DEFINITIONS.md A1; MEET-v31/METHOD_v3.1_FINAL.md "Amendment HQ_02" | [pos 1614], [pos 1639] |
| DF20 | ε̂_× (cross_block_rmax) with κ̂, δ̂, ū̂, r̂, η̂ | definition | ε̂_× = max \|X_jᵀX_k\|/(n−1) over different blocks; δ̂ = (K−1)ε̂_×/κ̂; ū̂ = Σ_b max_U x_b(U); r̂, η̂ on the stated domain | reporting amendment | MEET-THM/AMENDMENT_HQ_02_DEFINITIONS.md A2 | [pos 1614], [pos 1639] |
| DF21 | Output convention and event 𝒪, GUARD-W | definition | estimates on 𝒪 are functions of (X, y, seed, binary); statements P{𝒪, ·}; any worker/LS0/guard stop ⇒ no output | new wording (#6, #16) | MEET-v31/METHOD_v3.1_FINAL.md #6, #16; TLF lines 74, 86 | [pos 1251] |
| DF22 | Shared implementation premises | definition | EX-A, EX-S/H-U, CAL, IND-T, SR, OP-LS0, e4, complete scans, MC contract | premises (not model conditions) | MEET-THM/THEOREM_LIST_FINAL.md lines 73–87 | [pos 1626] |
| DF23 | Design families G, LH, W, ORTH | definition | sampling model G; LH exact-Gram masked family; W reporting exhibit; ORTH | families used for IC3 | MEET-THM/THEOREM_LIST_FINAL.md lines 68–71; TH02 (c1) | [pos 1626] |
| DF24 | H-DOM and constants a, δ_A, δ_H, r, C_σ, b_X, D_* | definition | matrix domain of M2 | definition | MEET-THM/THEOREM_LIST_FINAL.md line 148 | [pos 1614], [pos 1624] |
| DF25 | Settings table (49 rows), classes (a)–(e) | definition | every setting classed; no class (e) | METH31 §5 (ground rule 9) | MEET-v31/METHOD_v3.1_FINAL.md §5 | [pos 1214], [pos 1226], [pos 1302] |
| RL01 | HQ ruling Q1 (§5.3) | definition | Bridge form ACCEPTED with three conditions: (a) discrepancy half, (b) bridge-form stability, (c) refutation of the one-shot form (OWS-WS6(d), WS7) after a cross-family check | ACCEPTED ("Q1 (§5.3): ACCEPTED, with three conditions"); Q1(c) met by CHK_INHERITED (VERIFIED WITH AMENDMENT) | MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md | [pos 1608], [pos 1614] |
| RL02 | HQ ruling Q2 (§5.4 coverage) | definition | Posterior-content / MC reading: "Coverage error" means \|π(C(π̂)) − nominal\| plus MC error; frequentist coverage → FUTURE_WORK (CJ01) | ACCEPTED | MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md | [pos 1608], [pos 1614] |
| RL03 | HQ ruling Q3 (§5.4 TV/KL under masking) | definition | NOT binding; obligation with fallback; list must contain at least one masked-regime accuracy statement paper 1 proves (→ TH04(f)); masked final-estimate TV/KL → CJ02 | NOT binding | MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md | [pos 1608], [pos 1614] |
| RL04 | HQ ruling Q4 (Ĵ and leakage proxy) | definition | REPORTING allowed: from existing quantities, no random numbers, no feedback, precisely specified | REPORTING, allowed | MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md | [pos 1608], [pos 1614] |
| RL05 | HQ ruling Q5 (stage count continuous in ε) | definition | Stage-count content of Q1(b) = sandwich + local constancy + continuous envelope; real-valued parts must be continuity/Lipschitz statements; theorem and paper must say T is a step function (T = 3 between {2, 4} at ε = 10⁻⁵) | ACCEPTED, with two conditions | MEET-THM/evidence/2026-11-04_HQ_RULING_Q5.md | [pos 1621], [pos 1624] |
| RL06 | HQ approval amendment (growth rate (ii)) | definition | Package approved; R′_n = 4⌈(n + p)⁶/4⌉ kept only as a sufficient rate inside the theorem (M1 simultaneous control), not as a method configuration (≈ 10¹⁷ islands at study sizes) | adopted by HQ; Felipe may overrule | MEET-v31/AMENDMENT_HQ_02.md; transcript | [pos 1639] |
| MD01 | MEET-v31 decision 1 | decision | **Block (local-to-global) start kept.** The backfit start is rejected for paper 1. Arm D is v2 evidence only. | decided (MEET-v31 MINUTES §2); closed in: R1 (all three); R2 rule; R3-6 procedure; result §3 | MEET-v31/MINUTES.md §2 row 1 | [pos 1280], [pos 1286] |
| MD02 | MEET-v31 decision 2 | decision | **HPM stays the only decision rule.** MPMs of both PIPs are reported as descriptions. No HPM-vs-MPM disagreement flag. | decided (MEET-v31 MINUTES §2); closed in: R1 (all three) | MEET-v31/MINUTES.md §2 row 2 | [pos 1280], [pos 1286] |
| MD03 | MEET-v31 decision 3 | decision | **LS0 in the shipped core,** after the final local search. Own provenance and `ls0_improved` flag. Does not fire E3. | decided (MEET-v31 MINUTES §2); closed in: R2 D3c | MEET-v31/MINUTES.md §2 row 3 | [pos 1280], [pos 1286] |
| MD04 | MEET-v31 decision 4 | decision | **Parallel layer** (each item ADDITIVE / bitwise unless stated): (a) concurrent final islands; (b) concurrent diagnostic islands; (c) parallel scans with lexicographic reduction; (h) the block-table stage in parallel; process workers (threads need private counters); GUARD-W "any worker / LS0 / guard stop ⇒ no output" (an LS0 stop is an operational interruption; a completed LS0 capped at `local_limit` still returns output, with L1 = n/a); (g) estimate fields NA on unavailable output. | decided (MEET-v31 MINUTES §2); closed in: R1–R2 (D3e, D3f) | MEET-v31/MINUTES.md §2 row 4 | [pos 1280], [pos 1286] |
| MD05 | MEET-v31 decision 5 | decision | **Stacking R′ = 4k at N_e,** declared before stream 10 (streams 10..9+R′). N_e is never split. Extra local search from the R = 4 centre. Baseline and expanded records each carry their own flags and card. | decided (MEET-v31 MINUTES §2); closed in: R2 D3a, D3b | MEET-v31/MINUTES.md §2 row 5 | [pos 1280], [pos 1286] |
| MD06 | MEET-v31 decision 6 | decision | **Depth and cost are stated at the implemented (island) level.** "Free of N, H, R" is removed. Calibration is counted. C6 (per-particle streams) and C7 (Gram-free scorer) are the declared v3.2 path. C6 is implemented and law-checked iff paper 1 claims particle-parallel depth **or** demonstrates any fit with p > 2,500. This trigger is HQ's disposition: the union of the two recorded conditions (Seats A/B: any p > 2,500, R2_A:23, R2_B:21, R3_B:44; Seat C: a particle-parallel depth claim). The narrower trigger was not unanimously adopted. Felipe decided (2026-11-03) that paper 1 claims island-level depth only, and the study has p ≤ 1,000, so neither trigger currently fires. | decided (MEET-v31 MINUTES §2); closed in: R2 D3d, D4; C6 trigger: HQ (AMENDMENT_HQ_01) | MEET-v31/MINUTES.md §2 row 6 | [pos 1280], [pos 1286] |
| MD07 | MEET-v31 decision 7 | decision | **Calibration kept unchanged, with a contract:** 𝓒 frozen before final randomness; validity holds for any frozen 𝓒; Theorem G cap; ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation); restricted ESS on V only; statuses distinguished. Shortening it (C9) is rejected. | decided (MEET-v31 MINUTES §2); closed in: R1–R2 (all three) | MEET-v31/MINUTES.md §2 row 7 | [pos 1280], [pos 1286] |
| MD08 | MEET-v31 decision 8 | decision | **Ẑ-weighted PIP is primary,** equal-weight is secondary, and both MPMs and R_eff are reported. POST HOC. | decided (MEET-v31 MINUTES §2); closed in: R2 D5 (all three) | MEET-v31/MINUTES.md §2 row 8 | [pos 1280], [pos 1286] |
| MD09 | MEET-v31 decision 9 | decision | **Flags E1–E3, ESS and grid flags kept** as calibration triggers (they define the law of 𝓒) and as labelled heuristics. No PSIS/R̂ flags. The certificate card never feeds back into calibration. | decided (MEET-v31 MINUTES §2); closed in: R1 (all three) | MEET-v31/MINUTES.md §2 row 9 | [pos 1280], [pos 1286] |
| MD10 | MEET-v31 decision 10 | decision | **Certificate card (POST HOC):** PC2's minimal card. G1 (deterministic store bounds, including Ẑ < Z_𝒯 ⇒ Ẑ < Z); G2 (π(S) ≤ e^{F(S)}/max(Z_𝒯, 0.05Ẑ), joint with output, ≥ 95%); L1–L3 (local, subset and best-of-scored certificates); R optional (box). One declared certificate budget, with "unresolved" on exhaustion. L1 is evaluated on the returned Ŝ (after LS0). Each number carries the label "numerical implementation of an exact-arithmetic certificate" until validated arithmetic (SC) and VAL-FP exist; a long-double replay alone does not remove it. | decided (MEET-v31 MINUTES §2); closed in: R2 D2; R3-1 | MEET-v31/MINUTES.md §2 row 10 | [pos 1280], [pos 1286] |
| MD11 | MEET-v31 decision 11 | decision | **General-h estimator:** H_r(h) after each complete measured round. Ẑ-weighted and equal-weight pools are reported. The default 𝓗 is model size and pairwise inclusion on neighbour-graph edges. h must be fixed from (X, y), or from (X, y, 𝓒) before stream 10. Plain averages for joint h; Rao–Blackwellisation for marginal PIPs only. HPM terminal frequency is descriptive only. ADDITIVE. | decided (MEET-v31 MINUTES §2); closed in: R2 D7; R3-3 | MEET-v31/MINUTES.md §2 row 11 | [pos 1280], [pos 1286] |
| MD12 | MEET-v31 decision 12 | decision | **Output convention:** every estimate on the output event 𝒪 is a function of (X, y, seed, binary). The allocation and hardware decide only whether output is delivered (stop-only guard, Lemma RO). Guarantees are stated for the potential run and as P{𝒪, ·}, never conditional on completion. | decided (MEET-v31 MINUTES §2); closed in: R2 item 9 e8 | MEET-v31/MINUTES.md §2 row 12 | [pos 1280], [pos 1286] |
| MD13 | MEET-v31 decision 13 | decision | **Item 9: generality in (n, p).** No setting is class (e) in the method's law. Fixes e1–e8 and wordings w1–w7 are adopted (list in §4). No separate p ≪ n / p ≫ n rule is needed. | decided (MEET-v31 MINUTES §2); closed in: R2–R3-4 | MEET-v31/MINUTES.md §2 row 13 | [pos 1280], [pos 1286] |
| DS01 | Dissent K33 (Seat D) | decision | D would place K33 (calibration deterministic termination/count form) in S-IDENT; A, B, C: M7; rebuild convergence N5(b) → FW either way | recorded dissent | MEET-THM/MINUTES.md §2.3 R3-4, K33 | [pos 1626] |
| DS02 | Dissent K23 (Seat C) | decision | C would keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL (no theorem number); A, B, D: FUTURE_WORK (CJ05) | recorded dissent | MEET-THM/MINUTES.md §2.3 R3-4, K23 | [pos 1626] |
| DS03 | Dissent K29 / S-STGI (Seat D) | decision | D: "confirm K29 here"; A, B, C prevail: S-STGI dissolved | recorded dissent | MEET-THM/MINUTES.md §2.2 S-STGI row | [pos 1626] |
| DS04 | Dissent K30 (Seat C) | decision | C: K30 in the supplement as S-STGI / C14; A, B, D: M7(d) | recorded dissent | MEET-THM/MINUTES.md §2.3 R3-8, K30 | [pos 1626] |
| DS05 | Dissent K70 (Seat C) | decision | C: K70 as a supplementary attributed variant; A, B, D: labelled no-LS0 variant clause of M5 | recorded dissent | MEET-THM/MINUTES.md §2.3 R3-8, K70 | [pos 1626] |
| DS06 | Dissent K57 (Seat D) | decision | D: general K57 in the supplement; B, C (and A:39,108): only P1 in S-POOL, general accuracy → FW (CJ08) | recorded dissent | MEET-THM/MINUTES.md §2.3 R3-8, K57 | [pos 1626] |
| CL01 | Cited lemma/result (TLF Part III) | lemma | N9 kernel facts: γ_φ-reversibility of each elementary move, q_φ-invariance and self-adjointness of the uniformly random-order round, exact draw_pi0 and Z̄₀ (K08, K20, K21), with the CHK amendments (VERIFIED WITH AMENDMENT) | cited (not a numbered claim of paper 1); used in: M1(a), S-KERNEL | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 1 (line 1303) | file only |
| CL02 | Cited lemma/result (TLF Part III) | lemma | K47 (pooling, cited) | cited (not a numbered claim of paper 1); used in: M1; S-POOL | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 2 (line 1304) | file only |
| CL03 | Cited lemma/result (TLF Part III) | lemma | SMC identities and fixed-data limits: Del Moral 2004; Del Moral–Doucet–Jasra 2006; Whiteley–Lee–Heine 2016; Dai et al. 2022 | cited (not a numbered claim of paper 1); used in: M1(a), (f) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 3 (line 1305) | file only |
| CL04 | Cited lemma/result (TLF Part III) | lemma | Markov lower bound: Grosse–Ghahramani–Adams 2015 | cited (not a numbered claim of paper 1); used in: M1(d), M4(e) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 4 (line 1306) | file only |
| CL05 | Cited lemma/result (TLF Part III) | lemma | Greedy-schedule optimality: Štefankovič–Vempala–Vigoda 2009 | cited (not a numbered claim of paper 1); used in: M7(a), M2(b6) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 5 (line 1307) | file only |
| CL06 | Cited lemma/result (TLF Part III) | lemma | K28: √c·T*(c) → Λ_len (Syed et al. 2024 Thm 3; Gelman–Meng 1998) | cited (not a numbered claim of paper 1); used in: M7(e) (cited) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 6 (line 1308) | file only |
| CL07 | Cited lemma/result (TLF Part III) | lemma | Chatterjee–Diaconis 2018 Thms 1.1–1.3 (exp(KL) scale; with log-weight-tail qualifications) | cited (not a numbered claim of paper 1); used in: M6, M2(c2) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 7 (line 1309) | file only |
| CL08 | Cited lemma/result (TLF Part III) | lemma | Cérou–Del Moral–Guyader 2011 Thms 1.4–1.5 (variance theorems; novelty of S-Z (i) to the citation checker) | cited (not a numbered claim of paper 1); used in: M2, S-Z | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 8 (line 1310) | file only |
| CL09 | Cited lemma/result (TLF Part III) | lemma | Frazier et al. 2023, Assumption 6(iv) (generic χ² precedent; not re-fetched) | cited (not a numbered claim of paper 1); used in: M2 | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 9 (line 1311) | file only |
| CL10 | Cited lemma/result (TLF Part III) | lemma | Papaspiliopoulos–Rossell 2017 §§3.1–3.2 (block computation precedent) | cited (not a numbered claim of paper 1); used in: M3 | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 10 (line 1312) | file only |
| CL11 | Cited lemma/result (TLF Part III) | lemma | Dai–Heng–Jacob–Whiteley §4.2 (independent-system evidence weighting) | cited (not a numbered claim of paper 1); used in: S-REP | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 11 (line 1313) | file only |
| CL12 | Cited lemma/result (TLF Part III) | lemma | K60, K61: Barbieri–Berger 2004 HPM/MPM facts (cited lemmas) | cited (not a numbered claim of paper 1); used in: M5, S-TARGET | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 12 (line 1314) | file only |
| CL13 | Cited lemma/result (TLF Part III) | lemma | Rossell 2022 Prop 1 (the 2E₀δ₁ term) | cited (not a numbered claim of paper 1); used in: M5(0) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 13 (line 1315) | file only |
| CL14 | Cited lemma/result (TLF Part III) | lemma | Yang–Wainwright–Jordan 2016; Zhou–Yang–Vats–Roberts–Rosenthal 2022 (context next to M5; "with their priors LH is covered by rapid mixing; ours is for the paper's own target and start") | cited (not a numbered claim of paper 1); used in: M5, M4 | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 14 (line 1316) | file only |
| CL15 | Cited lemma/result (TLF Part III) | lemma | Hou–Wang–Atchadé arXiv:2407.20580 (never "first finite-n") | cited (not a numbered claim of paper 1); used in: M5, M4 | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 15 (line 1317) | file only |
| CL16 | Cited lemma/result (TLF Part III) | lemma | Brent 1974 (W/w + D scheduling) | cited (not a numbered claim of paper 1); used in: M8(d) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 16 (line 1318) | file only |
| CL17 | Cited lemma/result (TLF Part III) | lemma | T22(iii) (K16) PROVED-LOCKED CONDITIONAL, with G, R, within-block SE, EXP′, VIS, NL_η, NL_avg(κ) retained | cited (not a numbered claim of paper 1); used in: M3 (supplementary clause) | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 17 (line 1319) | file only |
| CL18 | Cited lemma/result (TLF Part III) | lemma | CHK-verified WS3, WS4 (M2(a), M3(e)); WS6(d), WS7 with amendments (M2(c)) | cited (not a numbered claim of paper 1); used in: M2, M3 | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 18 (line 1320) | file only |
| CL19 | Cited lemma/result (TLF Part III) | lemma | T03♯ (S-T) target consistency, T01–T03 PROVED-LOCKED (external review queued) | cited (not a numbered claim of paper 1); used in: M1(i), M3, M4(f), M5, M6 | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 19 (line 1321) | file only |
| CL20 | Cited lemma/result (TLF Part III) | lemma | Lemma RO (event containment), GUARD-W (stop-only coupling; audit open) | cited (not a numbered claim of paper 1); used in: M1(d), M4(e), S-OUT | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 20 (line 1322) | file only |
| CL21 | Cited lemma/result (TLF Part III) | lemma | Furnival–Wilson 1974 (leaps-and-bounds superset bound, K05) | cited (not a numbered claim of paper 1); used in: S-CERT | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 21 (line 1323) | file only |
| CL22 | Cited lemma/result (TLF Part III) | lemma | K23 squared-kernel Dirichlet comparison, as an attributed lemma without theorem number (C's dissent; optional for the S-KERNEL HQ) | cited (not a numbered claim of paper 1); used in: S-KERNEL | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 22 (line 1324) | file only |
| CL23 | Cited lemma/result (TLF Part III) | lemma | LIT-PAR G4 (Song–Liang numerical comparison), cited as labelled numerical evidence; the analytic separation K97 is FUTURE_WORK | cited (not a numbered claim of paper 1); used in: Coverage Cor 2 | MEET-THM/THEOREM_LIST_FINAL.md Part III table row 23 (line 1325) | file only |


---

# ID registry B (campaign-history theory documentation: 02b_theory_campaign_history.md)

One row per archive ID in the blocks TH101+, LM101+, CJ101+, RF101+, CE101+ (dense numbering). Columns: archive ID | native name(s) | kind | description | final status (exact words of the source) | authoritative file | positions | feeds final card. Exact duplicates across themes were merged (the kept ID lists the other as an alias): theme-block IDs TH392 into TH369, TH393 into TH372, TH397 into TH341, RF224 into RF181, RF352 into RF269 (before dense renumbering).

Counts: TH 356, LM 156, CJ 227, RF 189, CE 121, total 1049.

## Theorems, propositions, corollaries

| ID | native name(s) | kind | description | final status | authoritative file | positions | feeds |
|---|---|---|---|---|---|---|---|
| TH101 | T01; A0; T1; contrast reduction; mixed-rate transfer; THEORY.md row T01 | lemma | Contrast reduction and mixed-rate transfer (old label A0 = T1) | PROVED-LOCKED (all parts, wave 3); not adopted (adoption is Felipe's decision) [review record: wave 3: Opus 5.5 lead; two Opus 5.5 xhigh (same-family Claude); statement checker where noted; external OpenAI review queued (no cross-family review done); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T01.md | [pos 119]; [pos 156]; [pos 178] | S-T / L-T03 (T01 reduction); S-TARGET (REGISTRY_PAPER1 mentions) |
| TH102 | T02; A1; T2; dimension control; strict supersets; T02(i); T02(ii); THEORY.md row T02 | lemma | Dimension control and exclusion of strict supersets (old label A1 = T2) | PROVED-LOCKED (all parts, wave 3); (ii) under SE; not adopted (adoption is Felipe's decision) [review record: wave 3: Opus 5.5 lead; two Opus 5.5 xhigh (same-family Claude); statement checker where noted; external OpenAI review queued (no cross-family review done); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T02.md | [pos 119]; [pos 156]; [pos 178]; later [pos 342]; [pos 355]; [pos 370] | S-T (T02(i♯), T02(ii♯)); L-T03 |
| TH103 | T03; A2; T3; selection consistency; JRSS-B Thm 1; THEORY.md row T03 | theorem | Selection, screening, PIPs and the global HPM (old label A2 = T3) | PROVED-LOCKED (all parts, wave 3), with H-T02 used as a hypothesis (closed by T02(i)); not adopted (adoption is Felipe's decision) [review record: wave 3: Opus 5.5 lead; two Opus 5.5 xhigh (same-family Claude); statement checker where noted; external OpenAI review queued (no cross-family review done); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex; main@c4ef0dc/Docs/Theory/one_pagers/T03.md | [pos 119]; [pos 156]; [pos 178]; later [pos 342]; [pos 370] | S-T (T03♯, Theorem 1); L-T03; M4 (uses T03) |
| TH104 | T04; A3; T4; contraction without beta-min; THEORY.md row T04 | theorem | Contraction without beta-min (old label A3 = T4) | PROVED-LOCKED (all parts, wave 3), with H-T02 as hypothesis (closed by T02(i)); not adopted (adoption is Felipe's decision) [review record: wave 3: Opus 5.5 lead; two Opus 5.5 xhigh (same-family Claude); statement checker where noted; external OpenAI review queued (no cross-family review done); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T04_A3_contraction/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T04_A3_contraction/PROOF_v2.tex; main@c4ef0dc/Docs/Theory/one_pagers/T04.md | [pos 119]; [pos 156]; [pos 178] | none identified (campaign-only mention in S-TARGET audit lines) |
| TH105 | T06; A5; T-ID; identifiability; exact ties; THEORY.md row T06 | proposition | Identifiability and exact ties (old label A5 = T-ID) | PROVED-LOCKED (all parts, wave 3); (ii)(b) conditional on H-T03 (= T03(i)); not adopted (adoption is Felipe's decision) [review record: wave 3: Opus 5.5 lead; two Opus 5.5 xhigh (same-family Claude); statement checker where noted; external OpenAI review queued (no cross-family review done); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T06_T07_identifiability_size_prior/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T06_T07_identifiability_size_prior/PROOF_v2.tex; main@c4ef0dc/Docs/Theory/one_pagers/T06.md | [pos 119]; [pos 156]; [pos 178] | L-DEC (via Prop1-T07; T06(i) tie sentence, per FROZEN_LIST) |
| TH106 | T07; A6; T5-C; size-only ranking ceiling; Bayes decisions; JRSS-B Prop 1; THEORY.md row T07 | proposition | Size-only ranking ceiling and Bayes decisions (old label A6 = T5-C) | PROVED-LOCKED (all parts, wave 3); not adopted (adoption is Felipe's decision) [review record: wave 3: Opus 5.5 lead; two Opus 5.5 xhigh (same-family Claude); statement checker where noted; external OpenAI review queued (no cross-family review done); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T06_T07_identifiability_size_prior/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T06_T07_identifiability_size_prior/PROOF_v2.tex; main@c4ef0dc/Docs/Theory/one_pagers/T07.md | [pos 119]; [pos 156]; [pos 178] | L-DEC (K60); S-TARGET (T07Bayes.lean) |
| TH107 | T09; T7; exact start; invariant kernels; whole-round minorisation; THEORY.md row T09 | proposition | Exact start, invariant kernels, whole-round minorisation (old label T7) | PROVED-LOCKED (all parts, wave 1); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T09_T7_kernel_validity/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T09_T7_kernel_validity/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T09.md | [pos 119]; [pos 156]; [pos 178] | S-KERNEL; M1; L-N9 |
| TH108 | T10; T11 (old label); feasible-addition hazards; ordered paths; addition floor r_k; THEORY.md row T10 | lemma | Feasible-addition hazards and ordered paths (old label T11) | PROVED-LOCKED (all parts, wave 3); not adopted (adoption is Felipe's decision) [review record: wave 3: Opus 5.5 lead; two Opus 5.5 xhigh (same-family Claude); statement checker where noted; external OpenAI review queued (no cross-family review done); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T10_T11_addition_hazard/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T10_T11_addition_hazard/PROOF_v4.tex; main@c4ef0dc/Docs/Theory/one_pagers/T10.md | [pos 119]; [pos 156]; [pos 178] | S-IDENT (source tag); T21 route (a) corollary (H10) |
| TH109 | T11; L-LED; T14-D; unified scoring and discovery ledger; T11(iii); THEORY.md row T11 | lemma | Unified scoring and discovery ledger (old label L-LED / T14-D) | PARTLY PROVED: (iii) PROVED-LOCKED (wave 1); (i), (ii), (iv)-(vii) not locked (CONJECTURED); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T11_LLED_scoring_ledger/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T11_LLED_scoring_ledger/PROOF_v5.tex; main@c4ef0dc/Docs/Theory/one_pagers/T11.md | [pos 119]; [pos 156]; [pos 178] | M5 (T38(a) uses T11(iii)); M6 (Lean T11Miss.lean) |
| TH110 | T12; T8; frozen-run evidence; recorded RB identities; JRSS-B Prop 2; THEORY.md row T12 | proposition | Frozen-run evidence and recorded-RB identities (old label T8) | PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex; main@c4ef0dc/Docs/Theory/one_pagers/T12.md | [pos 119]; [pos 156]; [pos 178] | M1; L-T12; S-Z; S-POOL |
| TH111 | T13; T10 (old label); restricted ESS; omitted-mass identity; THEORY.md row T13 | lemma | Restricted ESS and omitted-mass identity (old label T10) | PROVED-LOCKED (all parts, wave 1), with the explicit premises COVER(W, eps_C) and pool avoidance in clauses (ii)-(iv); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T13_T10_restricted_ESS/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T13_T10_restricted_ESS/PROOF_v4.tex; main@c4ef0dc/Docs/Theory/one_pagers/T13.md | [pos 119]; [pos 156]; [pos 178] | M7 (source tag); S-IDENT (coverage identity) |
| TH112 | T14; L-FM; first-moment evidence consistency; T14(i); THEORY.md row T14 | lemma | First-moment evidence consistency (old label L-FM) | PARTLY PROVED: (i) PROVED-LOCKED (singleton case, wave 1); (ii), (iii) not locked (CONJECTURED); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T14_LFM_first_moment_evidence/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T14_LFM_first_moment_evidence/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T14.md | [pos 119]; [pos 156]; [pos 178] | M7 (source tag) |
| TH113 | T15; L-OCC; occupancy from an evidence lower tail; THEORY.md row T15 | lemma | Occupancy from an evidence lower tail (old label L-OCC) | PROVED-LOCKED (all parts (i)-(iv), wave 1), conditional on H-T12 (= T12(i), closed); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T15_LOCC_occupancy/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T15_LOCC_occupancy/PROOF_v4.tex; main@c4ef0dc/Docs/Theory/one_pagers/T15.md | [pos 119]; [pos 156]; [pos 178] | none identified in REGISTRY_PAPER1 cards (used inside T26/D1 proofs) |
| TH114 | T20; T15 (old label); local-search semantics; conditional repair; T20(i); T20(ii); THEORY.md row T20 | lemma | Local-search semantics and conditional repair (old label T15) | PARTLY PROVED: (i)-(ii) PROVED-LOCKED (wave 1; (ii-C) needs H03); (iii), (iv), (v) not locked (CONJECTURED); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T20_T15_local_search/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T20_T15_local_search/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T20.md | [pos 119]; [pos 156]; [pos 178] | S-CERT (certificate semantics); T21 route (d) |
| TH115 | T21; T14-H; composition theorem for the reported HPM; JRSS-B Thm 4; C1; routes (a)-(f); THEORY.md row T21 | theorem | Composition theorem for the reported HPM (old label T14-H) | PROVED-LOCKED (C1 and routes (a)-(f), wave 2) + CONDITIONAL on open hypotheses: H24 (route (e)) and the route-specific occurrence / exposure conditions; not adopted (adoption is Felipe's decision) [review record: wave 2: Astra lead; two Sol 6.1 high; Astra xhigh closing review; Claude Opus audit: correct; conditional theorem; not adopted] | main@c4ef0dc/Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T21_T14H_HPM_composition/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T21.md | [pos 119]; [pos 156]; [pos 178]; later [pos 342]; [pos 370] | M5 (Theorem HPM); L-TA |
| TH116 | T22; T16 (old label); aggregate start bounds; conditional concentration; T22(i)(ii)(iv); T22(iii); JRSS-B Thm 2; THEORY.md row T22 | theorem | Aggregate start bounds and conditional concentration (old label T16) | PARTLY PROVED: (i), (ii), (iv) PROVED-LOCKED (wave 1; (iv-c) premises 1 - pi(S0) -> 0 from T03 and 1 - pi0(S0) -> 0 from (iii)); (iii) PROVED-LOCKED (wave 2) + CONDITIONAL on EXP', VIS, NL_eta, NL_avg(kappa); (v) CONJECTURED (not proved); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T22_T16_start_aggregation/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/proofs/T22iii_T16_start_aggregation/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T22iii_T16_start_aggregation/PROOF_v2.tex; main@c4ef0dc/Docs/Theory/one_pagers/T22.md | [pos 119]; [pos 156]; [pos 178]; later [pos 355] | M3 (Theorem START); L-MASK |
| TH117 | T23; T18 (old label); basin-to-output guarantee; recording-prefix control; T23(ii); THEORY.md row T23 | lemma | Basin-to-output guarantee with recording-prefix control (old label T18) | PARTLY PROVED: (ii) PROVED-LOCKED (wave 1; (ii-c), (ii-d) CONDITIONAL on BASIN); (i), (iii), (iv), (v) not locked (CONJECTURED); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T23_T18_basin_prefix/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T23_T18_basin_prefix/PROOF_v5.tex; main@c4ef0dc/Docs/Theory/one_pagers/T23.md | [pos 119]; [pos 156]; [pos 178] | S-POOL (MZ-P1P2) |
| TH118 | T25; T19 (old label); conditional evidence bounds through a crossing; T25(iv); THEORY.md row T25 | theorem | Conditional evidence bounds through a crossing (old label T19) | PARTLY PROVED: (iv) PROVED-LOCKED (wave 2) + CONDITIONAL on PW2; (i)-(iii), (v) not locked (CONJECTURED); DROPPED from paper selection (FROZEN_LIST); not adopted (adoption is Felipe's decision) [review record: wave 2: Astra lead; two Sol 6.1 high; Astra xhigh closing review; Claude Opus audit: correct; conditional theorem; not adopted] | main@c4ef0dc/Docs/Theory/proofs/T25iv_T19_crossing_evidence/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T25iv_T19_crossing_evidence/PROOF_v2.tex; main@c4ef0dc/Docs/Theory/one_pagers/T25.md | [pos 119]; [pos 156]; [pos 178] | S-Z (evidence variance and masked tails) |
| TH119 | T27; T20-C (old label); sequential cancellation; iid-discovery budget; T27(i); masking law; THEORY.md row T27 | corollary | Sequential cancellation and the iid-discovery budget (old label T20-C) | PARTLY PROVED: (i) PROVED-LOCKED (wave 2) + CONDITIONAL on H2, H3; (ii)-(iv) not locked (CONJECTURED); not adopted (adoption is Felipe's decision) [review record: wave 2: Astra lead; two Sol 6.1 high; Astra xhigh closing review; Claude Opus audit: correct; conditional theorem; not adopted] | main@c4ef0dc/Docs/Theory/proofs/T27i_T20C_cancellation_budget/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T27i_T20C_cancellation_budget/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T27.md | [pos 119]; [pos 156]; [pos 178] | M3; M2; L-MASK; L-WS6 |
| TH120 | T31; T22 (old label); what the reported checks and certificates establish; T31(i); 95% evidence lower bound; THEORY.md row T31 | proposition | What the reported checks and certificates establish (old label T22) | PARTLY PROVED: (i) PROVED-LOCKED (wave 1, conditional on H-T12 = T12(iii), closed); (ii)-(vii) not locked (CONJECTURED); not adopted (adoption is Felipe's decision) [review record: wave 1: Opus 5.5 lead; Astra #1 (Stage A); Astra #2 + Opus 5.5 xhigh (Stage B); Fable 5.1 high + Astra xhigh (Stage C): correct; same-family and cross-family (Astra); not adopted] | main@c4ef0dc/Docs/Theory/proofs/T31_T22_certificates/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T31_T22_certificates/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/one_pagers/T31.md | [pos 119]; [pos 156]; [pos 178] | M1; M4; L-T12 |
| TH121 | T01; A0; T1; contrast reduction and mixed-rate transfer; T01(i)-(iv); transfer rule (T) | theorem | Pre-campaign (locked): the v3 posterior equals the contrast-model posterior at IG rate b0*s_y^2; deterministic rate envelope; scale event P0(B_n)->1; rate derivative; mixed-endpoint transfer (a) at cost kappa^2 and no same-rate transfer (b). | PROVED-LOCKED (wave 3; statement checker approved; two review rounds, both reviewers verified; external OpenAI review queued); MEET-THM flag SAME-FAMILY-ONLY | main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md | [pos 119]; [pos 238] | feeds S-T / L-T03 (K03, K93, K04) and S-TARGET (K03 reduction part); flag T01-T03 SAME-FAMILY-ONLY |
| TH122 | T02; A1; T2; T02(i); T02(ii); H-T02; dimension control and strict supersets (locked form) | theorem | Pre-campaign (locked) T02: size tail Pi(/S/>m/y) <= 2^-m (2p)^s0 (n+1)^(s0/2) sqrt(n) Theta_{n,m} with Theta tight uniformly in m (G,R only); strict supersets O_P(r_n) under the full SE. | PROVED-LOCKED (wave 3; statement checker approved; two review rounds, both reviewers verified; external OpenAI review queued); MEET-THM flag SAME-FAMILY-ONLY; the (i) form is superseded for use by TH125 (T02(i-sharp)) | main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md | [pos 119]; [pos 238] | superseded by TH125/TH127 inside S-T (K93); locked form not on a final card |
| TH123 | T03; A2; T3; locked T03; PROOF_v2; H03 (= T03(i) conclusion) | theorem | Pre-campaign (locked) selection consistency: under G, R, full SE, BM-C (M*) or BM-inf and H-T02, 1-pi(S0)=O_P(r_n); PIP/MPM/HPM consistency; screening without beta-min; scale invariance. | PROVED-LOCKED (wave 3; statement checker approved; two review rounds, both reviewers verified; external OpenAI review queued); MEET-THM flag SAME-FAMILY-ONLY; numerical check 1958/1958; statement unchanged; conditional on H-T02 which T02(i) closes | main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md; main@c4ef0dc/Docs/Theory/theorems/T03_A2_selection_consistency.md | [pos 119]; [pos 238] | replaced for the paper by TH128 (T03-sharp) in S-T (K93); locked T03(i) is the premise H03 of T20, T21, T22(iv-c) |
| TH124 | T04; A3; contraction without beta-min; H-T02 use | theorem | Pre-campaign (locked) contraction: with H-T02 and R1, G, R (SE for (ii),(iv)): prediction-error, model-size (<= d*), parameter and variance contraction without any beta-min condition. | PROVED-LOCKED (wave 3; round 1 CP verified, CW not verified (gap CW-F1, fixed); round 2 both verified; external OpenAI review queued); NOT re-derived with T02(i-sharp)/SE_w in the campaign (W1-T03R section 6 item 3: not checked) | main@c4ef0dc/Docs/Theory/proofs/T04_A3_contraction/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/T04_A3_contraction/PROOF_v2.tex; W1-T03R/PROOF.md; W1-T03R/REPORT.md | [pos 119]; [pos 238] | feeds: none in paper-1 cards (COVERAGE_MATRIX: contraction rates / Hellinger = FW20 FUTURE_WORK) |
| TH125 | T02(i-sharp); T02(i#); T02(i♯); Theorem T02(i♯); sharpened size tail; exact Beta-Binomial size tail; S03 section 2 | theorem | Exact BB(1,p) size tail: Pi(/S/>m/y) = R_m (n+1)^(s0/2) sqrt(n) Theta#_{n,m} with sup_m P0(Theta#>L) <= (8+24M/sigma*^2)/(n-1)+L^(-1/2)+C_Lambda/log(sqrt(L)/c#) under G,R only; Pi(/S/>m#_n(omega_n)/y)=O_P(e^(-omega_n)). | PROVED (candidate) (W1-T03R); SF VERIFIED (W2-VT03R row 10); XF VERIFIED (A-REV2 section 2: den-prime and T02(i-sharp); quantifier is sup_m P, not P(sup_m)); final card C9: PROVED, SF/XF VERIFIED | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md | [pos 233]; [pos 296]; [pos 337]; [pos 370]; [pos 565]; [pos 570] | feeds S-T (K93, K04): supplement cited in main text (R2_C card C9) |
| TH126 | Proposition E3; E3-T03; barrier of the exact-tail route | proposition | Any size-tail bound of the form Markov numerator over S0 denominator needs m - s0 >= [s0 log(p/s0) + (s0+2)/2 log n]/log 2 - 1 - o(1) (or m# = K); a barrier for the proof route, not a posterior lower bound. | PROVED (candidate) (W1-T03R); SF VERIFIED (W2-VT03R row 8); XF VERIFIED* (A-REV2: only as a barrier for this cutoff/envelope route) | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 296]; [pos 342]; [pos 370]; [pos 570] | feeds S-T scope sentence (K93) only; not a stand-alone card |
| TH127 | T02(ii-sharp); T02(ii#); T02(ii♯); Theorem T02(ii♯) | theorem | Under R1, G, R and SE_w(m#_n; g0): Pi(S strictly containing S0 / y) = O_P(sqrt(log n/n)). | PROVED (candidate) (W1-T03R); SF VERIFIED (W2-VT03R row 14); XF VERIFIED (A-REV2: Lemmas I/B and T02(ii-sharp)); final card C9: PROVED, SF/XF VERIFIED | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 296]; [pos 370]; [pos 570] | feeds S-T (K93) |
| TH128 | Theorem 1; T03-sharp; T03 sharp; T03♯; T03#; S03; W6F2-T03; T03R | theorem | Posterior target consistency (statement of record W6-FIXREV2 section 1.2): under R1, G, R, SE_lambda(j0), SE_w(m#_n; g0) and BM-inf or BM(c>c0): 1-pi(S0)=O_P(sqrt(log n/n)); PIP/MPM/global-HPM consistency with P0(S_dagger != S0) <= 2E0[1-pi(S0)]; large signals get PIP->1 without beta-min. | PROVED (candidate) (W1-T03R); SF VERIFIED (W2-VT03R, no GAP/ERROR in the mathematics); XF VERIFIED under exactly its hypotheses (A-REV2); VERIFIED core (A-REV5, onset gloss ERROR); LIT-STAT: modest extension of Rossell 2022, clause (iii) known; final card: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2) | W6-FIXREV2/STATEMENTS.md; W1-T03R/REPORT.md; W1-T03R/PROOF.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md; A-REV5/REVIEW.md; LIT-STAT/REPORT.md; MEET-THM/THEOREM_LIST_FINAL.md | [pos 233]; [pos 296]; [pos 337]; [pos 370]; [pos 570]; [pos 736]; [pos 1009] | feeds S-T (Supplement S-T, cited in main text; K93, K04); used by M1(g), M4, M5 (pi(S0)->1 on LH); onset n >~ 2e6 disclosed |
| TH129 | Proposition D'; Prop. D'; PropD'-T03; PropD′-T03; scope of Prop. D | proposition | Under the T03-sharp hypotheses Pi(/S/>s0/y) <= 1-pi(S0) = O_P(r_n): the large cutoff m#_n is an artefact of the SE-free Markov route; Prop. D refutes the small cutoff only under G and R alone. | PROVED (author = verifier W2-VT03R; no second same-family check); XF: none (A-REV2 section 3.5 restates it without a verdict row) | W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 337]; [pos 370]; [pos 570] | feeds S-T scope sentence (K93); supplement remark |
| TH130 | Proposition W; Prop. W; PropW-SIG; SIG(c) | proposition | T03-sharp (i)-(iii) hold with SE_lambda(j0)+BM(c) replaced by SE_w + the direct signal-separation condition SIG(c), c >= L*; SE_lambda is needed only in lem:signal. | PROOF SKETCH (W2-VT03R); not in A-REV2 table; (iv) needs a per-coordinate SIG not written | W2-VT03R/REPORT.md | [pos 337]; [pos 370] | feeds: none (optional weakening, campaign-only) |
| TH131 | Prop 1; Proposition 1; Prop1-T07; T07; T06(i); Prop 1 (i-prime); Prop 1 (iii-prime); Decision rules and the size-prior ceiling; size-prior ceiling | proposition | HPM = Bayes rule for 0-1 support loss, MPM = Bayes rule for Hamming loss, plug-in excess risk <= 2//p_hat - PIP//_1; sharp size-prior ceiling: some positive size-only prior has HPM S0 iff S*_{s0}=S0; a strictly higher scored same-size competitor certifies no size prior recovers S0; equal scores for every response iff X_S X_S^T = X_S' X_S'^T. | PROVED (locked T07(i)-(iii), T06(i)(a); (i-prime), (iii-prime) new); SF VERIFIED* (W5-LOCKBOOK: (i-prime) CORRECT, (iii-prime) CORRECT with amendment strict beyond numerical error); XF VERIFIED* (A-REV4 BOOK_CHECK: sharp construction and strict same-size certificate sound; ERROR B5 on the data paragraph = RF125); A-REV6: ERROR in W5 paraphrase (RF126) with tie-aware R3 repair; Lean T07Bayes.lean sorry-free; LIT-STAT: standard/folklore, (i) and (ii)(c) unstated but trivial | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; W5-LOCKBOOK/PROOF.md; A-REV4/BOOK_CHECK.md; A-REV6/BOOK.md; main@c4ef0dc/Docs/Theory/proofs/T06_T07_identifiability_size_prior/STATEMENT.md; L-LEAN/STATUS.md; LIT-STAT/REPORT.md | [pos 334]; [pos 342]; [pos 424]; [pos 509]; [pos 550]; [pos 677]; [pos 807]; [pos 1009] | feeds S-TARGET (S3 decision rules; K60 cited lemma, K61, K62) and L-DEC; cited by M5 and M4 (1/2 sharp) |
| TH132 | T05-U; Theorem T05-U; Cor T05-U-infinity; T05(ii) failure half; finite-n failure bound for the global HPM | theorem | Under G and ORTH: P0(S_dagger=S0) <= exp(-d delta^2/4) + prod_{j in S0}[Phi(sqrt(lambda_j)-t_delta)+Phibar(sqrt(lambda_j)+t_delta)]; limsup P0(S_dagger=S0) <= Phi(c)^s0 when sqrt(lambda_n)-sqrt(tau_n)->c. | PROVED (author W7-SEC, line-by-line own check only; candidate); XF none: A-REV9 GAP = deferred, incomplete review, no mathematical rejection asserted; pre-campaign T05 was CONJECTURED (not proved) | W7-SEC/PROOF_T05.md; W7-SEC/REPORT.md; main@c4ef0dc/Docs/Theory/theorems/T05_A4_orthogonal_threshold.md | [pos 717]; [pos 751]; [pos 756] | feeds: none found in MEET-THM cards (T05 planned as a supplement remark, pos 957; UNCERTAIN whether dropped) |
| TH133 | T05-Shat; Cor T05-Shat; reported HPM version of T05-U | corollary | On the SMC branch P(S_hat=S0 reported) <= bound(U) + P(final local search ends with local_limit); on the exact branch S_hat = S_dagger. | PROVED-UNDER (author W7-SEC: given the code reading of local_search v3_engine.h:378-418; own check only); XF none (A-REV9 deferred) | W7-SEC/PROOF_T05.md; W7-SEC/REPORT.md | [pos 717]; [pos 751] | feeds: none found |
| TH134 | T05-L; Theorem T05-L; T05(ii) success half; threshold limit | theorem | Equal magnitudes, b_n^2/sigma*^2 bounded, sqrt(lambda_n)-sqrt(tau_n)->c in (-inf,inf]: liminf P0(S_dagger=S0) >= Phi(c)^s0; with U-infinity, P0(S_dagger=S0)->Phi(c)^s0 for every c in [-inf,inf]; explicit n0 useless (log n about 227). | PROVED (author W7-SEC, limit statement, crude explicit constants; own check only); XF none (A-REV9 deferred) | W7-SEC/PROOF_T05.md; W7-SEC/REPORT.md | [pos 717]; [pos 751] | feeds: none found |
| TH135 | T05-G; Theorem T05-G; Prop T05-O; T05(iii); benchmark gap; oracle gap | theorem | Known-size oracle bound P0(S_or != S0) <= e^-x + sum Phi(sqrt(2 log M + 2x) - sqrt(lambda_j)); gap sequences exist: oracle succeeds w.p.->1 while the global HPM fails w.p.->1; at p=n^a the amplitude gap is [sqrt(1+2a)-sqrt(2a)] sqrt(log n) + o(1). | PROVED (author W7-SEC, own check only); XF none (A-REV9 deferred); the wording "loses a sqrt(log n) factor" is RF127 | W7-SEC/PROOF_T05.md; W7-SEC/REPORT.md | [pos 717]; [pos 751]; [pos 957] | feeds: none found (planned supplement remark, pos 957) |
| TH136 | EXP′; EXP'; W1-EXP Thm 1; Thm1-EXP; Theorem 1 (EXP′); EXP-prime theorem | theorem | Every within-block addition satisfies log[r_b(T+l)/r_b(T)] = -(1/2)log(n+1) - nu log(1-x_{T,l}) + R with /R/ <= kappa_EXP on an event of probability -> 1, from G, R-lite(A,M), SE-blk (no block orthogonality) | PROVED (W1-EXP); SF VERIFIED (W3-VEXP rows 1-5); XF VERIFIED* (A-REV2: limiting constant ERROR 0.52 -> 0.51/c_*; A-REV5: fixed-design core VERIFIED) | W1-EXP/PROOF.md; W1-EXP/REPORT.md; W3-VEXP/REPORT.md; A-REV2/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 233] [pos 238] [pos 351] [pos 355] [pos 363] [pos 370] [pos 568] [pos 570] [pos 807] [pos 919] | M3 START (K16, as hypothesis of T22(iii); card L-MASK K15/K17/K18) |
| TH137 | R1-cert; W3-VEXP R1; Corollary R1; EXP′ remainder certificate | corollary | Data-computable bound /R/ <= (1+phi^-2)/(2phi^2(n-1)) + nu(1.02+1/(n phi^2))/min_b RSS^y_{C_b} valid at any n for any data under realised SE-blk (0.59-1.52 nats on study-like designs) | PROVED (W3-VEXP, author = verifier); XF VERIFIED (A-REV2) | W3-VEXP/REPAIRS.md; A-REV2/REVIEW.md | [pos 363] [pos 370] [pos 568] | feeds: none (campaign-only; finite-n certificates Theme 9) |
| TH138 | Thm2-BO; W1-EXP Thm 2; T22(iii) unconditional in BO; favourable regime BO | theorem | Under G, R, SE-blk, BO and block beta-min BM-blk: 1 - pi_0(S0) = O_P(2^B sqrt(log n) n^{-1/2}) (EXP′ discharged) | PROOF SKETCH (W1-EXP); SF VERIFIED (W3-VEXP row 10 and R2: verbatim corollary of locked T22(iii), no step open); XF none | W1-EXP/PROOF.md; W3-VEXP/REPAIRS.md | [pos 351] [pos 355] [pos 363] | M3 START (K16 supplementary favourable-regime lemma; not an unconditional claim) |
| TH139 | Prop2.1-2.2; W1-EXP Prop 2.1; W1-EXP Prop 2.2; T22(iii)°; NL_eta -> NL_C; reference transfer | proposition | T22(iii) holds under NL_C (instead of NL_eta) with EXP′ supplied; S0 may be replaced by any deterministic feasible reference S° (supp theta* = S0 never used) | PROOF SKETCH (W1-EXP); SF VERIFIED (W3-VEXP rows 7-8); XF none | W1-EXP/PROOF.md; W3-VEXP/REPORT.md | [pos 351] [pos 355] [pos 363] | feeds: none (campaign-only); idea of any feasible reference underlies M3(a) K15 |
| TH140 | Thm6-EXP; W1-EXP Thm 6; start concentration under exact zero leakage | theorem | Under G, R-lite, SE-blk, ZL(S°), SPREAD, VIS-lin(S°): 1 - pi_0(S°) = O_P(2^B n^{-1/2}) and e_n° = O_P(e^{-cn}) (favourable if S°=S0, masked otherwise) | PROVED (W1-EXP); SF VERIFIED (W3-VEXP row 11); XF none | W1-EXP/PROOF.md; W3-VEXP/REPORT.md | [pos 351] [pos 355] [pos 363] [pos 370] | feeds: none directly (input to TH144 Thm5-LH) |
| TH141 | Thm3-EXP; W1-EXP Thm 3; two-sided chain ratio law; CL(L) ratio law | theorem | Along a deterministic chain with chain leakage CL(L_n), -1-kappa_EXP <= E_{n,i} <= kappa_EXP + 1.01(L_n+/Z_i/)^2 w.p. -> 1; fixed L gives H2 | PROVED (W1-EXP); SF VERIFIED (W3-VEXP row 12, needs deterministic chain); XF VERIFIED (A-REV2 SEX Thm 3) | W1-EXP/PROOF.md; W3-VEXP/REPAIRS.md; A-REV2/REVIEW.md | [pos 351] [pos 355] [pos 363] [pos 568] [pos 570] | M3 START (K17 masked law); card L-MASK; cited in M2 Theorem WS status lines |
| TH142 | Thm4-EXP; W1-EXP Thm 4; Thm4-growL; T27(i) from chain leakage; CL(L) => T27(i) | theorem | Under CL(L), H3, p >= 2(s+c): log pi_0(S0) + c log p + (c/2) log n = O_P(1); with L_n -> inf upper side gains 1.01 c (L_n+O_P(1))^2 | PROVED given H3 (W1-EXP); SF VERIFIED (W3-VEXP row 13, wording E); XF VERIFIED (A-REV2: fixed CL + normalised H3; growing-L bound sufficiency only; 'iff' ERROR) | W1-EXP/PROOF.md; W3-VEXP/REPAIRS.md; A-REV2/REVIEW.md | [pos 351] [pos 355] [pos 363] [pos 568] [pos 570] | M3 START (K17, XF-VERIFIED); card L-MASK |
| TH143 | LimitLaw; W1-EXP limit law of Mstat; masking limit law (fixed-p form) | proposition | With zero leakage, T_i empty, pi_0(S^(0)) -> 1 and orthogonal chain directions: Mstat ->_d sum log((s+i+1)/2) + sum (sigma^2/(2 v_empty)) chi^2_{1,i} | PROOF SKETCH (W1-EXP); SF VERIFIED as sketch (W3-VEXP row 14); XF: remains a sketch (A-REV2 5.3) | W1-EXP/PROOF.md; W3-VEXP/REPAIRS.md | [pos 351] [pos 355] [pos 363] | feeds: none (campaign-only; rigorous LH-iid version is TH151) |
| TH144 | Thm5-LH; W1-EXP Thm 5; LH exact Gram; joint masked-regime family LH; Thm 5(b1-LH) premises | theorem | On the exact-Gram linked-hub family (p <= n-1, /psi/<rho, g<=B<2g): (a) 1-pi_0(S°)=O_P(2^B n^-1/2); (b) pi_0(S0)=p^-c n^-c/2 e^{O_P(1)}; (c) VIS fails at S0; (d) 1-pi(S0)=O_P(sqrt(log n/n)); (e) bridge endpoints | PROVED for (a)(b)(c)(e), (d) by locked T03, limit law in (b) PROOF SKETCH (W1-EXP); SF VERIFIED (W3-VEXP rows 18-21); XF none on the label (A-REV8 verified the exact-Gram premises; registry/final list: SAME-FAMILY-ONLY) | W1-EXP/PROOF.md; W1-EXP/REPORT.md; W3-VEXP/REPORT.md; A-REV8/REVIEW.md | [pos 351] [pos 355] [pos 363] [pos 370] [pos 919] | M3 START (K17 / M3(f) masked law on LH); M5 HPM context (K69/K72); card L-MASK |
| TH145 | R3-LHiid(VEXP); W3-VEXP R3; LH iid fixed-partition surrogate | proposition | Rows iid N(0,Sigma_LH), /psi/<rho, g<=B<2g, p<=n^A: 1-pi_0(S0\M)=O_P(2^B sqrt(log n) n^-1/2) via fixed partition on {blocks=groups} and exact Beta residual law | PROOF SKETCH (W3-VEXP); XF GAP (A-REV2: sound in restricted regime, adaptive packing unresolved) | W3-VEXP/REPAIRS.md; A-REV2/REVIEW.md | [pos 363] [pos 370] [pos 568] | feeds: none (superseded by TH150) |
| TH146 | PropD-dilution; W3-VEXP Prop D; Proposition D (deterministic start-mass ceiling) | proposition | For U ⊆ S0 of truths alone in their block, pi_0(S0) <= prod_{i=1}^{a}(s0-a+i)/(2p-s0+a-i) * prod_{j in U} BF({j}) for every data set | PROVED (W3-VEXP, author = verifier; two lines from T22(ii-a)); SF/XF none | W3-VEXP/REPAIRS.md | [pos 363] [pos 370] | feeds: none (campaign-only; Theme 3 dilution; final K18 is DIL-E) |
| TH147 | DilThreshold; W3-VEXP dilution threshold | proposition | Truth j enters the start mode only if (n/2)log(1/(1-theta_j^2/v)) > log((2p-s0)/s0) + (1/2)log n; favourable only for n >~ 2v log(2p/s0)/theta_min^2; no signal scale removes it at fixed n | PROOF SKETCH (population limit), numerically confirmed (W3-VEXP; W3-PXN) | W3-VEXP/REPAIRS.md; W3-VEXP/REPORT.md | [pos 363] [pos 370] | feeds: none (Theme 3 disclosure) |
| TH148 | PXN-P1; W3-PXN P1; Lemma P1; partition = groups on LH-iid | theorem | On LH-iid the v3 partition equals the groups w.p. -> 1 (D_in < D_out and g<=B<2g) | PROVED given C1 (W3-PXN); SF VERIFIED* (W5-VMASK rows 8, 8′); XF VERIFIED (A-REV3; A-REV6 via W7 Thm B) | W3-PXN/PROOF.md; W3-PXN/REPORT.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md; A-REV6/PARTITION.md | [pos 355] [pos 423] [pos 425] [pos 430] [pos 510] [pos 742] [pos 796] [pos 919] | feeds: none directly; S-BLOCKS K07 via PART-ThmA (TH162) |
| TH149 | PXN-P2; W3-PXN P2; Lemma P2 | theorem | On LH-iid, w.p. -> 1: locked SE at size m_n+s0, SE-blk, anchored SE_lambda/SE_w, R, BM-infinity, G | PROVED given C1 (W3-PXN); SF VERIFIED* (W5-VMASK row 9); XF VERIFIED (A-REV3) | W3-PXN/PROOF.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md | [pos 355] [pos 423] [pos 742] | feeds: none (campaign-only) |
| TH150 | PXN-P3; W3-PXN P3; near-truth start mass at p>>n; b_n -> 1 | theorem | On LH-iid: q = O_P(sqrt(log n/n)), e = O_P(p sqrt(n) e^{-c6 n}), hence 1-pi_0(S°) = O_P(sqrt(log n/n)) and pi_0(R_d) >= pi_0(S°) -> 1 (no 2^B, no NL_eta/VIS-lin/zero-leakage) | PROVED (W3-PXN); SF VERIFIED (W5-VMASK row 7); XF VERIFIED (A-REV3; W8-SYNTH: XF VERIFIED) | W3-PXN/PROOF.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md | [pos 355] [pos 423] [pos 425] [pos 430] [pos 742] [pos 796] | feeds: none in final list (K15-type start mass cited via T22(i)); FUTURE_WORK context FW10 |
| TH151 | PXN-P4; W3-PXN P4; masking limit law on LH-iid | theorem | On LH-iid Mstat_n = log pi_0(S0) + c log p + (c/2) log n ->_d sum_{i<=c} log((s+i)/2) + (1/2)chi^2_c; pi_0(S0)=p^-c n^-c/2 e^{O_P(1)}; T27(i) H1-H3 hold | PROVED (W3-PXN); SF VERIFIED (W5-VMASK row 10); XF VERIFIED* (A-REV3: literal T27 polynomial-scaling wording retained) | W3-PXN/PROOF.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md | [pos 355] [pos 423] [pos 742] [pos 796] | feeds: none directly (related M3 START K17 on exact-Gram LH) |
| TH152 | PXN-P5; W3-PXN P5; start mode = reference S°; eligibility | theorem | P(tilde S0 = S°) -> 1, so tilde S0 in R_0 and /tilde S0 Δ S0/ = c w.p. -> 1 | PROVED (W3-PXN); SF VERIFIED (W5-VMASK row 11); XF VERIFIED (A-REV3) | W3-PXN/PROOF.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md | [pos 355] [pos 423] [pos 742] | feeds: none (campaign-only) |
| TH153 | PXN-P6; W3-PXN P6; TD′ lattice condition at S°; LS0 scores and certifies S0 | theorem | On LH-iid w.p. -> 1: (L) S0 locally optimal and (D) D_S on Lat(S°)\{S0}, so the production local search from S° returns S0 certified in c moves; LS0 scores and certifies S0 | PROVED (W3-PXN); SF VERIFIED (W5-VMASK rows 14-15); XF GAP (A-REV3, A-REV6, A-REV8; conflict C16: Lambda(a) uses Tr(c) beyond range) | W3-PXN/PROOF.md; W5-VMASK/REPAIRS.md; A-REV3/REVIEW.md; A-REV6/PARTITION.md; A-REV8/REVIEW.md | [pos 355] [pos 423] [pos 742] [pos 796] [pos 919] | feeds: none in final list; nearest FUTURE_WORK FW10 (K71 clause named (b1-LH-iid), GAP); exact-Gram T38-b1-LH in M5 K65/K69/K72 |
| TH154 | PXN-P7; W3-PXN P7; D2 on LH-iid c=1; no-tweak route | theorem | On LH-iid with c=1: D2-a, b, c hold (Dep=O_P(sqrt(log n/n))) and D2-d (NB) gives P(S0 not in S_cal) -> 0 without LS0 | PROVED for D2-a,b,c, PROOF SKETCH for D2-d (W3-PXN); SF VERIFIED* (W5-VMASK rows 16-17); XF GAP (A-REV3; A-REV6; A-REV8) | W3-PXN/PROOF.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md | [pos 355] [pos 423] [pos 742] [pos 919] | feeds: none (campaign-only) |
| TH155 | PXN-P8; W3-PXN P8; posterior concentration on LH-iid | theorem | On LH-iid 1-pi(S0) = O_P(sqrt(log n/n)) under the joint law of (X, eps) (locked T03 plus design de-randomisation) | PROVED given T03 (W3-PXN); SF VERIFIED (W5-VMASK row 18); XF VERIFIED (A-REV3) | W3-PXN/PROOF.md; A-REV3/REVIEW.md | [pos 355] [pos 423] [pos 742] | feeds: none in final list (cf. S-T / T03♯, Theme 1) |
| TH156 | PXN-Cor; W3-PXN Corollary; T38(b) on LH-iid; Thm 5(b1) LH-iid corollary | corollary | Under EX-A, EX-S, CAL, SR: (b1) with LS0 for every c, liminf P(Uc ∩ {S+hat = S0}) >= 1 - limsup P(U); (b1′) without tweak for c=1 (conditional on D2-d) | PROVED given cited inputs (W3-PXN); SF VERIFIED* (W5-VMASK row 19); XF GAP (A-REV3, A-REV6, A-REV8) | W3-PXN/PROOF.md; W3-PXN/REPORT.md; A-REV3/REVIEW.md | [pos 355] [pos 423] [pos 742] [pos 919] | feeds: none (FUTURE_WORK FW10 context) |
| TH157 | PXN-Q; W3-PXN Prop Q; co-blocking; 2g<=B kills LH masking | proposition | With 2g <= B each linked pair lies in one block w.p. -> 1, the masked hub becomes visible within its block and LH loses its masking (study groups of 5 cannot carry LH masking) | PROOF SKETCH (W3-PXN); SF/XF none | W3-PXN/PROOF.md | [pos 355] [pos 423] | feeds: none (disclosure that the study generator is outside LH) |
| TH158 | PXN-W; W3-PXN Prop W; Proposition W; dilution masking | proposition | Block-orthogonal iid design: start keep-j log-odds LO_0(j) = -log((2p-s0)/s0) - (1/2)log(n+1) + V_0(j) + O_P(1) with V_0 = (n/2) theta_j^2 Var(x_j/X_T)/v_T; under fixed s0 + BM-infinity dilution vanishes | PROOF SKETCH (W3-PXN, asymptotic part); numerics in REPORT sec 5; no review | W3-PXN/PROOF.md; W3-PXN/REPORT.md | [pos 355] [pos 423] | feeds: M3 START K18 via Theme 3 (final card cites DIL-E); disclosure only |
| TH159 | VMASK-R1-NB; W5-VMASK R1; D2-d proof; Thm 5(b1′) LH-iid c=1; NB proof | theorem | Initial-pilot d-range max d - min d <= T0 log r* w.p. -> 1 on LH-iid c=1, r*=(11+2 sqrt(10))/9; with D2-a,b,c gives P(S0 not in S_cal) -> 0, no method change | PROVED (candidate, W5-VMASK, single run, unverified); XF GAP (A-REV6, A-REV8) | W5-VMASK/REPAIRS.md; W5-VMASK/REPORT.md; A-REV6/REVIEW.md; A-REV8/REVIEW.md | [pos 510] [pos 742] [pos 919] | feeds: none (campaign-only) |
| TH160 | Thm 5(b1-LH-iid) (W5-VMASK form); T38-b1-LH-iid (LH-iid family); PXN joint LS0 route | theorem | LH-iid (c linked pairs, g<=B<2g, n^a<=p<=n^A) + EX-A, EX-S, CAL, SR, GUARD/OP-LS0 + LS0 with emitted centre: P(O ∩ {S+hat != S0}) -> 0 and liminf P(O ∩ {S+hat = S0}) >= 1 - limsup P(U) | PROVED (candidate); SF VERIFIED (W5-VMASK); XF GAP (A-REV3, A-REV6, A-REV8) | W5-VMASK/REPORT.md; A-REV3/REVIEW.md; A-REV6/REVIEW.md; A-REV8/REVIEW.md | [pos 742] [pos 796] [pos 919] | feeds: none in paper-1 list; FUTURE_WORK FW10 uses the label (b1-LH-iid) for a different clause (name clash) |
| TH161 | API-PXNGAP theorem; Thm 5(b1) with LS0 on LH-iid p>>n; Theorem R/P3′/P6′/P8′ composition; PXNGAP main theorem | theorem | LH-iid with (SIZE), 18<=p<=n^A, p->inf, EX-A/EX-S/CAL/SR/GUARD/OP-LS0: (R) P(blocks != groups) <= (2/(sqrt(pi)(1-rho))) p^2 sqrt(n) e^{-(n-4)I*}; (S)(E)(T)(P) and (C) P(O ∩ {S+hat != S0}) <= 2E0 delta1 + D_n -> 0 | PROVED (candidate, API-PXNGAP) given T22(i),(ii), T03, CONC, W7 Thm B; no SF/XF review in the archive | API-PXNGAP/PROOF.md; API-PXNGAP/REPORT.md; campaign/LEDGER.md | [pos 911] [pos 978] | feeds: none in final list; FUTURE_WORK FW10 (K71) and M5 HPM K69/K72 (exact-Gram only) |
| TH162 | PART-ThmA; W7-PART Theorem A; partition = groups deterministic; laminarity | theorem | (A1) (C*) => laminar; (A2) partial converse; (A3) laminar and g_max<=B => blocks are unions of whole groups, and = groups if B<2 g_min; (A4) local margin (M) => (C*) | PROVED (W7-PART); XF VERIFIED* (A-REV9: A1-A4 VERIFIED, A2 extra premise; A-REV6: A0(c) GAP) | W7-PART/PROOF.md; W7-PART/REPORT.md; A-REV6/PARTITION.md | [pos 717] [pos 742] [pos 748] [pos 796] | S-BLOCKS (K07: separation => groups kept, SIZE => equality); M5 context |
| TH163 | PART-ThmB; PART-CorB; W7-PART Theorem B; Corollary B; partition-recovery lemma | theorem | Under GRP(rho,psi_bar) and SIZE: P(blocks != groups) <= sum_within P_rho(/r/<=t) + sum_cross P(/r/>=t) <= (2/(sqrt(pi)(1-rho))) p^2 sqrt(n) e^{-(n-4)I*}; <= p^-C for n>=n0 when p<=n^A | PROVED (W7-PART); Theorem B XF VERIFIED* (A-REV6 restricted scope; A-REV9 B-exact VERIFIED); Corollary B XF GAP (A-REV9, L2 constants) | W7-PART/PROOF.md; W7-PART/REPORT.md; A-REV6/PARTITION.md | [pos 717] [pos 742] [pos 796] [pos 919] | S-BLOCKS (K07) only via ThmA; replaces cited C1 in PXN P1; Theorem R of API-PXNGAP |
| TH164 | PART-ThmC; PART-CorC; W7-PART Theorem C; Corollary C; independent groups sharp bound | theorem | For independent groups with all /Sigma_jl/>=rho within: P(blocks != groups) <= G(G-1) K_g [H0(tau0) + sum H0(tau_{i+1}) min{1, g(g-1)P_rho(/r/<tau_i)}], exponent 2I* | PROVED (W7-PART); XF GAP (A-REV6: needs corrected Lemma 3) | W7-PART/PROOF.md; A-REV6/PARTITION.md | [pos 717] [pos 796] | feeds: none (campaign-only) |
| TH165 | PART-kappa; W7-PART kappa_C = 2I* | proposition | kappa_C(rho) = min_tau[I(tau;0)+I(tau;rho)] = 2I*(rho,0) exactly; asymptotic P <= poly e^{-n kappa_C} via mesh-1/n grid | identity PROVED; mesh-1/n bookkeeping PROOF SKETCH (W7-PART) | W7-PART/PROOF.md | [pos 717] [pos 796] | feeds: none |
| TH166 | VMASK-R5; W5-VMASK R5; m0-sharp; m0♯; LH-LAT sharp margin | proposition | m0 is a valid lower bound on the Phi>=2 population margin and sharp for homogeneous pairs; exact margin m0♯ = min over I (/I/>=2) of min{R_{i*(I)} - max κ_i R_i, min [del_t + R_{i*} - R_i]} | stated by W5-VMASK (brute-force confirmed 202/202 validity); XF: m0 valid not universally sharp (A-REV8) | W5-VMASK/REPAIRS.md; W5-VMASK/REPORT.md; A-REV8/REVIEW.md | [pos 742] [pos 919] | feeds: none (final list uses m0 in M5 IC3 only) |
| TH167 | VMASK-R2; W5-VMASK R2; U1 constant; kappa_2 | proposition | Replace the false bound nu log(1+a/RSS^y) <= 1 by <= 0.52/c_* + o(1) and kappa_2 := (1/2) sup_n (s0+2)(1+phi0^-2)/(phi0^2(n-1)) + 0.52/c_* + 1; only O(1) is used downstream | repair (same-family); XF VERIFIED (A-REV6 replacement constant; A-REV8) | W5-VMASK/REPAIRS.md; A-REV6/REVIEW.md; A-REV8/REVIEW.md | [pos 742] [pos 919] | feeds: none |
| TH168 | VMASK-R3; W5-VMASK R3; NB constant r* | proposition | Use r* = (11+2 sqrt(10))/9 (or NB′) instead of 1.925 for the pilot d-range threshold | repair (same-family); XF VERIFIED (A-REV8) | W5-VMASK/REPAIRS.md; A-REV8/REVIEW.md | [pos 742] [pos 919] | feeds: none |
| TH169 | VMASK-R7; W5-VMASK R7; LS0 cost +1 | proposition | LS0 score-call ceiling is 1 + (ell+1) max_{k<=K}[p + k(p-k)] (the +1 is the emitted centre) | repair (same-family); XF VERIFIED (A-REV8) | W5-VMASK/REPAIRS.md; A-REV8/REVIEW.md | [pos 742] [pos 919] | T38 (c) cost (Theme 7); no direct final card |
| TH170 | PXN (L)-failure formula; two speeds; certification slow, scoring not | proposition | P((L) fails) ≈ (s0+1)/sqrt(2π(n+1)t_n), t_n = 2log((2p-s0-1)/(s0+1)) + log(n+1); failure is a posterior miss charged to 2E0 delta1 | first-order formula; SF VERIFIED (W5-VMASK simulation, R4); XF none | W3-PXN/PROOF.md; W5-VMASK/REPAIRS.md | [pos 423] [pos 742] | feeds: none |
| TH171 | Theorem E; Thm E; DIL-E; exact block factorisation of the start | theorem | pi0(S)=prod_b pi_b^t(S_b) A_t(/S/) for every t>0, any data, any partition, positive tables | PROVED (author, O-DILUTE); SF none; XF VERIFIED with feasibility/cap retained (A-REV9) | O-DILUTE/THEORY.md; O-DILUTE/REPORT.md; A-REV9/REVIEW.md | [pos 579] [pos 588] [pos 666] [pos 763] [pos 821] | feeds M3 Theorem START clause (d) (K18; also K10 nearest row) |
| TH172 | Corollary E1; Cor. E1; DIL-E1; three deficits; V+C-log A identity | corollary | -log pi0(S0)=V+C-log A (visibility + competition - size) via softplus(-lambda_b), log(1+eta_b) | PROVED (author); SF none; XF VERIFIED* (A-REV9: production BF tables, r_b(empty)=1; GAP for arbitrary positive tables without normalisation) | O-DILUTE/THEORY.md; O-DILUTE/REPORT.md; A-REV9/REVIEW.md; MEET-THM/THEOREM_LIST_FINAL.md (M3(d)) | [pos 763] [pos 821] | feeds M3 Theorem START clause (d) (K18) |
| TH173 | Corollary E2; Cor. E2; rigorous ceiling; DIL-E1 (shared row) | corollary | t in I0 => log pi0(S0) <= -V-C-log P_t(N<=K) (sharpens W3-VEXP Prop D) | PROVED (author); XF VERIFIED* (A-REV9: interior-size/end-point conventions) | O-DILUTE/THEORY.md; O-DILUTE/REPORT.md; A-REV9/REVIEW.md | [pos 763] [pos 821] | feeds: none (campaign-only) |
| TH174 | Theorem R; Thm R; DIL-R; exact law of #truths/#nulls under pi0 | theorem | exact joint law of (/S cap S0/,/S minus S0/) under pi0; pi0(R_d)=P(M<=d), pi0(B_d), Markov bound | PROVED (author); SF none; XF VERIFIED (A-REV9: integer d>=0, feasible supports) | O-DILUTE/THEORY.md; O-DILUTE/REPORT.md; A-REV9/REVIEW.md | [pos 763] [pos 821] | feeds: none (campaign-only) |
| TH175 | Corollary N1; Cor. N1; DIL-N1; null inclusions O(1) | corollary | expected null inclusions under P_t are Theta(s0 sqrt(log p)/sqrt n), about 1 at study size, independent of c | PROVED (expectation bound); PROOF SKETCH (in-probability constant); XF ERROR on pointwise expectation bound, heavy-tail rate GAP (A-REV9) | O-DILUTE/THEORY.md; A-REV9/REVIEW.md | [pos 763] [pos 821] | feeds: none (A-REV9 LOCKABLE list excludes N1) |
| TH176 | Proposition S; Prop. S; DIL-S; ranking ceiling for every common sigma^2 | proposition | pi0(S0)<=1/prod_i(1+[M_(i)-(i-1)]_+) for v3 tables and any common sigma^2 | PROVED (author); SF none; XF GAP (A-REV9: replacement assignments not injective) | O-DILUTE/THEORY.md; O-DILUTE/REPORT.md; A-REV9/REVIEW.md | [pos 763] [pos 821] | feeds: none (A-REV9 excludes the product ceiling) |
| TH177 | Proposition D'; Prop. D'; Prop. D-prime; DIL-Dp; finite-n dilution formula | proposition | lambda_j ~ chi2_1(n rho_j^2)/2 - log(n)/2 - log((2p-s0-1)/(s0+1)), rho_j^2=(1-kappa_j)x_j<=omega_j saturating in c; assembled formula for log pi0(S0) | PROOF SKETCH (author); numerically checked; SF none; XF none | O-DILUTE/THEORY.md; O-DILUTE/REPORT.md | [pos 763] | feeds: none (campaign-only) |
| TH178 | Proposition DM; Prop. DM; DIL-DM; start masking by sigma^2-dilution at finite n | proposition | paper proposition: (i) exact deficit decomposition + ceiling, (ii) ranking ceiling, (iii) pi0(R_d)=P(M<=d); dilution clause | (i)-(iii) PROVED (author); dilution clause PROOF SKETCH; XF ERROR on DM(i) size sign (A-REV9); (ii) inherits Prop S GAP | O-DILUTE/THEORY.md §7; A-REV9/REVIEW.md | [pos 763] [pos 821] | feeds: none (MEET-THM: DIL-DM(i) is ERROR and must not be used) |
| TH179 | Proposition B1 (O-MIX); Prop. B1; OMIX-B1; mixture start exactly samplable | proposition | finite mixture of exact block starts: exact sampler, density, locked identities hold verbatim, T22(ii-a) becomes a sandwich, weight stability | PROVED (author only); SF none; XF none | O-MIX/REPORT.md | [pos 674] [pos 717] [pos 742] | feeds: none (campaign-only) |
| TH180 | Proposition B2; Prop. B2; OMIX-B2; random partitions do not undo LH masking | proposition | partition separating hub from its group mate gives pi0(S0)<=exp(-cn) w.p.->1; use structured not random mixtures | PROOF SKETCH (crux PROVED modulo W1-EXP Thm 1 = EXP', VERIFIED); author only | O-MIX/REPORT.md | [pos 674] [pos 717] | feeds: none (campaign-only) |
| TH181 | Theorem B3; Thm B3; OMIX-B3; (B-merge) on LH exact Gram | theorem | mixture of v3 partition and linked-merged partition: pi0mix(S0)>=1/2-O_P(2^{2g}n^{-1/2}); T38(b) on LH without LS0 by route (a); cost log 2 nats | PROVED-UNDER (verified W1-EXP Thm 6, locked T03, T11(iii), T21, Prop B1) (author only); LH-iid PROOF SKETCH; XF none | O-MIX/REPORT.md | [pos 674] [pos 717] [pos 742] | feeds: none (campaign-only; LS0 and no-LS0 routes carry T38(b)) |
| TH182 | Proposition C0; Prop. C0; OMIX-C0; validity of common-sigma-hat^2 tables | proposition | common-sigma-hat^2 tables are positive product-form tables: T09, T12, T13, T21, T22(i)(ii)(iv) hold verbatim | PROVED (author only) | O-MIX/REPORT.md | [pos 674] [pos 717] | feeds: none (campaign-only) |
| TH183 | Theorem C1 (O-MIX); Thm C1; OMIX-C1; dilution removed exactly under BO | theorem | under BO: pi0^C(S0)>=pi(S0)exp(-nu psi(u(S0))); plug-in with /Q_S'-Q_S0/=o(sqrt n) gives pi0^C(S0)>=pi(S0)(1-o_P(1)) | PROVED (author only; BO, deterministic); registry CONFLICT C23 (as a method recommendation); decision: rejected (E-SPINE 2.2); XF none | O-MIX/REPORT.md; T38-RECORD/REGISTRY_v2.md (C23); E-SPINE/Docs/Theory/AMENDMENTS_20261102.md | [pos 674] [pos 763] [pos 807] | feeds: none (campaign-only) |
| TH184 | Proposition C2; Prop. C2; OMIX-C2; sigma^2-grid mixture | proposition | uniform mixture over a sigma-hat^2 grid removes dilution at log cost 1/2 log n + log log n + O(1) nats without a plug-in (BO) | PROVED (under BO) (author only) | O-MIX/REPORT.md | [pos 674] [pos 717] | feeds: none (campaign-only) |
| TH185 | Proposition C3; Prop. C3; OMIX-C3; cancellation masking untouched by (C) | proposition | on any CL(0) chain pi0^C(S0)<=p^{-c}n^{-c/2}e^{O_P(1)}; (C) alone does not make T38(b) provable on LH | PROVED (author only); remainders need cross-family check (O-MIX 9.3) | O-MIX/REPORT.md | [pos 674] [pos 717] | feeds: none (campaign-only) |
| TH186 | Theorem S2; Thm S2; SIG-S2; start concentration dichotomy under common sigma-hat^2 | theorem | with a=sigma^2/sigma-hat^2: concentration iff a<1+1/(2A); rates n^{-1/2}, sqrt(log p)n^{-1/2}, p^{a-1}n^{-1/2}; flooding above threshold | PROVED-UNDER (BO) (author: 'PROVED under BO'); heavy-tail step to be re-checked; XF none | F-SIGMA/REPORT.md | [pos 727] [pos 733] [pos 763] | feeds: none (campaign-only) |
| TH187 | Theorem S3; Thm S3; SIG-S3; cancellation chains survive common sigma-hat^2 | theorem | pi0^C(S0)<=p^{-c}n^{-c/2}e^{O_P(1)} on CL(L) chains (exact exponent; = O-MIX Prop C3) | PROVED (author only) | F-SIGMA/REPORT.md | [pos 727] [pos 763] | feeds: none (campaign-only) |
| TH188 | Theorem S4; Thm S4; SIG-S4; T38 route (a) under common sigma-hat^2, no LS0 | theorem | under S2 with a_+<1+1/(2A) and T03 hypotheses: Q_f pi0^C(S0)->inf, P(S_hat != S0)->0 without LS0 (BO) | PROVED-UNDER (Theorem S2, locked T03, T11(iii), T21) (author only); 'vacuous as an improvement' over v3 in fixed-beta regime | F-SIGMA/REPORT.md | [pos 727] [pos 763] | feeds: none (campaign-only) |
| TH189 | Theorem S6; Thm S6; SIG-S6; random-design leakage catastrophe | theorem | in iid designs each null's table exponent under common sigma-hat^2 is (v_empty/sigma-hat^2) chi2_1/2 (inflation 1/(1-R^2)=26 at c=1); start floods to cap K; no single sigma-hat^2 serves truths and nulls | PROVED (mechanism exact; extreme-value step as S2(iv)); exact numerics (author only); real-fit numerics consistent (API-RESID); XF none | F-SIGMA/REPORT.md; API-RESID/REPORT.md | [pos 727] [pos 763] [pos 1009] | feeds: none (campaign rejection of common sigma^2; E-SPINE 2.2) |
| TH190 | Theorem A (W5-FAVIID); FAV-ThmA; 2^B-free favourable rate, fixed partition | theorem | on FAV with deterministic block-of-groups partition: 1-pi0(S0)=O_P((s0+1)sqrt(log n/n)), constant 3.83(s0+1)sqrt((1+eps0)A), no 2^B, no g | PROVED (candidate, given [C1],[T22i],[W1-L1.1-1.2]) (author only); API-FAVIID same-family read no error (not verification); SF none; XF none (FLAG AUTHOR-ONLY) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REPORT.md; API-FAVIID/W5-FAVIID_REPORT_AMENDED.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 507] [pos 742] [pos 748] [pos 978] | feeds: none (M3 K16 is T22(iii), PROVED-LOCKED CONDITIONAL; FAV flagged author-only) |
| TH191 | Theorem B (W5-FAVIID); FAV-ThmB; actual noise-dependent packing | theorem | on Q_n(m): 1_{Q_n(m)}(1-pi0(S0))=O_P(/W(m)/(s0+1)sqrt(log n/n)); unconditionally O_P(sqrt(log n/n)) for S3/S4/S6 (/W(3)/<=106, 15 while B=14) | PROVED (candidate, given [C1],[T22i],[W1-L1.1-1.2]) (author only); (G3) uniform Lipschitz step highest risk; Lemma P1' not on referee list; SF none; XF none (FLAG AUTHOR-ONLY) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REPORT.md; API-FAVIID/W5-FAVIID_REPORT_AMENDED.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 507] [pos 742] [pos 748] [pos 978] | feeds: none (campaign-only; FLAG AUTHOR-ONLY) |
| TH192 | Proposition N (W5-FAVIID); FAV-PropN; no deterministic limit partition for S3/S4 | proposition | for groups of 5 each fixed pair of groups is co-clustered with probability <= (m-1)/(G-1); partition does not stabilise | PROOF SKETCH (author only); numerics support | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REPORT.md; API-FAVIID/W5-FAVIID_REPORT_AMENDED.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| TH193 | Proposition B1 (W5-FAVIID); W5 Prop. B1; FAV-PropB1; S1 context-free bound | proposition | S1 (singleton groups): 1-pi0(S0)=O_P(n^{-1/2}(log n)^{(s0+1)/2}) with no event on the packing | PROVED (given [C1],[T22i]) (author only); asymptotic only | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| TH194 | Proposition F (W5-FAVIID); FAV-PropF; one-change ceiling | proposition | pi0(S0)<=[1+N_add+sum O_del+sum O_swp]^{-1}, exact odds, any data (sharpens W3-VEXP Prop D) | PROVED (deterministic) (author only) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| TH195 | Corollary C1 (W5-FAVIID); FAV-C1; posterior concentration on FAV | corollary | delta1=1-pi(S0)=O_P(sqrt(log n/n)) on FAV (via locked T03 and W3-PXN de-randomisation lemma P8) | PROVED (composition) (author only); 'verbatim' transfer of W3-PXN P2 to block-equicorrelated Sigma not checked | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REPORT.md; API-FAVIID/W5-FAVIID_REPORT_AMENDED.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| TH196 | Corollary C2 (W5-FAVIID); FAV-C2; Thm 6 (P1) on S3/S4/S6 | corollary | Delta_n=O_P(sqrt(log n/n)), (T_n+1)Delta_n=O_P(log^{5/2}n/sqrt n)->0: T26(i)-(ii) hold on study-like designs with actual partition, no EXP'/VIS/NL | PROVED (composition) (author only); needs ell=O(log n) for the stated rate | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REPORT.md; API-FAVIID/W5-FAVIID_REPORT_AMENDED.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| TH197 | Corollary C3 (W5-FAVIID); FAV-C3; Thm 5(a) on S3/S4/S6 | corollary | liminf P(S_hat=S0)>=1-limsup P(U) on the study-like family (route (a) of locked T21) | PROVED (composition of unreviewed Theorem B) (author only) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REPORT.md; API-FAVIID/W5-FAVIID_REPORT_AMENDED.md; API-FAVIID/REFEREE_HANDOFF.md; T38-RECORD/T38_STATEMENT.md | [pos 742] [pos 978] | feeds T38 (a) on S3/S4/S6 (campaign-only; author only) |
| TH198 | Prop 1; Prop1-TD; W1T37R-Prop1; literal TD unsatisfiable; swap identity SW | proposition | Literal TD(d,m) of T37 cannot hold for d>=1 (m=0 and F(S0+l)=F(S0) forced); P0(TD(d,0))=0 under G | PROVED; SF VERIFIED (W3-VT37R, 720 designs 0/720); XF VERIFIED (A-REV2, A-REV5) | W1-T37R/REPORT.md; W1-T37R/PROOF.md; W3-VT37R/REPORT.md; A-REV2/REVIEW.md | [pos 220] [pos 355] [pos 370] | L-TA card (supplement of M5 Theorem HPM, K65); negative result, K66/K67 DROP |
| TH199 | Theorem A; TheoremA; T37-A; W6F2-TheoremA; refined T37(i); Thm 3 (Theorem A); A1-A5; POS; R1-POS; A5(b) | theorem | Production greedy search from S_c in R_{a,d} returns S0 certified iff l>=tau(S_c) under TD'_P (A1-A4); A5 literal TD needs POS; TD'_P implies TD'_inf | PROVED (W6-FIXREV2 candidate); SF VERIFIED (W3-VT37R, 720 designs 0 violations); XF VERIFIED* (A-REV2 A1-A4 and POS-repaired A5; original A5(a) ERROR); A-REV5 core VERIFIED, literal cap-free lattice wording ERROR | W6-FIXREV2/STATEMENTS.md; W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md; A-REV2/REVIEW.md; A-REV5/REVIEW.md | [pos 220] [pos 355] [pos 370] [pos 570] [pos 742] [pos 919] | M5 Theorem HPM clause (a) (K65); S-CERT (K64); L-TA card (supplement of M5 Theorem HPM, K65) |
| TH200 | Proposition F; Prop F; failure partition I/II/III | proposition | Every fit with S-hat != S0 lies in exactly one class by F_pre, F_post vs F(S0): I (E_LS^c), II (search miss), III (explored competitor) | PROVED (immediate, W6-FIXREV2); XF VERIFIED (A-REV5) | W6-FIXREV2/STATEMENTS.md; A-REV2/REVIEW.md; A-REV5/REVIEW.md | [pos 569] [pos 742] [pos 919] | L-TA card (supplement of M5 Theorem HPM, K65); S-ELS classification uses it |
| TH201 | Theorem B (T37); refined T37(ii); ThmB-T37(incl); ThmB-T37(events) | theorem | Failure probability of the search <= P(S_c not in C)+P0(NA^c)+P0(TL^c)+sum over Lat(C) of P0(D_S^c) for a data-independent class C | PROVED (inclusions, union bound); PROOF SKETCH (single events); SF VERIFIED (W3-VT37R); XF VERIFIED (A-REV2; selected centre needs covering class); cap-count correction pending (A-REV5) | W1-T37R/REPORT.md; W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md; W6-FIXREV2/STATEMENTS.md | [pos 355] [pos 370] [pos 570] | feeds: none (campaign-only supplement; not the T24 Theorem B) |
| TH202 | Theorem C (C1); ThmC-C1; TL_d and NA_d w.p.->1 | theorem | TL_d holds w.p.->1 under SE+BM-inf; NA_d under local dependence LD (repaired LD*) | PROOF SKETCH; SF GAP (W3-VT37R, repaired at sketch level R4); XF GAP (A-REV2); superseded by Theorem W | W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md; W6-FIXREV2/STATEMENTS.md | [pos 355] [pos 370] | feeds: none (campaign-only; not in REGISTRY_PAPER1); K66/K67 DROP |
| TH203 | Theorem C (C2); ThmC-C2; TD'_P(R_{a,d}) under PGD | theorem | Under PGD(eta)+SE+BM-inf, TD'_P(R_{a,d}) w.p.->1 and repair from every centre of R_{a,d} | PROOF SKETCH; SF GAP (inequality ERROR repaired at sketch R5); XF GAP (A-REV2); superseded by Theorem W | W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md | [pos 355] [pos 370] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH204 | Theorem W; ThmW; Theorem PGD-W; refined T37(iii) | theorem | PGD(eta)+SE_lambda(d+1)+BM-inf+(H1/H2/H3) imply P0(TD'_P(R_{a,d}(D)))->1 and search from any centre in region returns S0 certified w.p.->1 | PROVED (candidate); SF VERIFIED (W5-VPGD, no ERROR, minor GAPs repaired R1-R4); XF none (A-REV5: implication only); region form fails on masked LH | W3-PGD/PROOF.md; W3-PGD/REPORT.md; W5-VPGD/REFEREE.md; W5-VPGD/REPORT.md | [pos 353] [pos 370] [pos 507] [pos 550] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1); SYNTHESIS Thm 3 row (W SF only) |
| TH205 | Prop P1; PGD-P1; GERC+TRC implies PGD; GERC Remarks | proposition | SE_lambda(d), GERC(R+;eta1), TRC(R;eta2) imply PGD(min eta) on R_{a,d}(D) | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md; W5-VPGD/REFEREE.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH206 | Prop P2; Cor P2'; PGD-P2; block reduction; eta*(d) | proposition | Under block orthogonality PGD(eta) holds iff (B1)-(B3); equicorrelated groups give closed-form eta*(d) | PROVED; SF VERIFIED + brute force (W5-VPGD) | W3-PGD/PROOF.md; W5-VPGD/REFEREE.md; W5-VPGD/REPORT.md | [pos 353] [pos 550] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH207 | Prop P3; PGD-P3; sufficient conditions for TRC | proposition | TRC with eta=phi0^2 theta_min^2/theta_max^2 holds for a=1 under SE or under block orthogonality | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH208 | Prop P4; PGD-P4; PGD sharpness | proposition | A reverse margin rho0>=(1+eps)rho+ at some state forces P0(D_S)->0 and TD'_P failure w.p.->1 | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH209 | Cor P6; PGD-P6; random Gaussian designs | corollary | Population Sigma with SE and PGD(eta) gives realised design with SE(phi0^2/2) and PGD(eta/2) w.p.->1 | PROVED given a cited concentration bound; SF VERIFIED* (W5-VPGD; constant vacuous at feasible n, needs n~1e15-1e22) | W3-PGD/PROOF.md; W5-VPGD/REPORT.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH210 | Cor W'; PGD-CorW'; design conditions | corollary | Theorem W holds with PGD replaced by GERC+TRC or by block orthogonality with (B1)-(B3) | PROVED (composition); SF VERIFIED* (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH211 | VPGD-R0; vanishing margin | theorem | Theorem W stays true with eta_n->0 provided eta_n^2 n theta_min^2/log n -> infinity | PROVED (re-reading of constants, W5-VPGD); no second check | W5-VPGD/REPAIRS.md | [pos 507] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH212 | VPGD-R2; Theorem W uniform form; Cor P6 repaired composition | theorem | Failure probability of TD'_P is <= delta_n uniformly over designs with the same constants; random-design composition P(E_X^c)+delta_n | PROVED (by inspection, W5-VPGD); no second check | W5-VPGD/REPAIRS.md | [pos 507] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH213 | Prop S'; VPGD-PropS'; sharper than star | proposition | In Lemma S, (H3) star may be replaced by (star'a) and (star'b); star implies star' | PROVED (candidate, W5-VPGD); registry clerk did not read STAR.md | W5-VPGD/STAR.md; W5-VPGD/REPORT.md | [pos 507] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| TH214 | Theorem W_Lat; VPGD-WLat; lattice form | theorem | PGD(eta) on Lat(S0deg) gives (L) and D_S on the whole lattice w.p.->1; search from any centre in the lattice returns S0 certified, no LD needed | PROVED (candidate, W5-VPGD); XF VERIFIED (A-REV8, reduction in stated lattice scope) | W5-VPGD/REPAIRS.md; W5-VPGD/REPORT.md | [pos 507] [pos 550] [pos 742] | Thm 5 (b1-LH) / M5 route via LM189 (LS-score), TH287 (T38-b1-LH); cited by SYNTHESIS instead of region Theorem W; feeds: none in REGISTRY_PAPER1 |
| TH215 | Prop LH-PGD; VPGD-LH-PGD | proposition | On linked-hub LH, PGD(eta_LH) holds on Lat(S0deg) minus S0 with eta_LH=min{1,1-kappa_max,D_min/R_max} | PROVED (candidate, W5-VPGD); XF VERIFIED (A-REV8, lower bound; sharpness numerical 20/20) | W5-VPGD/REPAIRS.md | [pos 507] [pos 742] | Thm 5 (b1-LH); TH293 (LH-LAT); feeds: none in REGISTRY_PAPER1 |
| TH216 | VPGD-equiv; PGD iff POP-LAT on a lattice | proposition | PGD(eta) on Lat gives POP-LAT(S0deg, eta R+_min); POP-LAT(S0deg,m) gives PGD(m/R+_max) on Lat with Phi>=2 | PROVED (candidate, W5-VPGD); no verifier | W5-VPGD/REPAIRS.md | [pos 507] [pos 742] | Thm 3/Thm 5 (b1); ⟦POP-LAT⟧; feeds: none in REGISTRY_PAPER1 |
| TH217 | Prop T; VPGD-PropT; tie | proposition | If a present truth u is worthless at S+j then rho0>=rho+ and PGD(eta) fails for all eta on the region; D_S fails w.p.->1 | PROVED (W5-VPGD); no second check; registry CONFLICT C15 with F-REFINE description | W5-VPGD/REPAIRS.md; W5-VPGD/REPORT.md | [pos 507] [pos 550] [pos 742] | negative result; supports RF176; feeds: none |
| TH218 | Theorem B; Theorem B (restated T24); ThmB-T24; restated T24; Gibbs-path repair; T24G Theorem B; W6F1-ThmB-conv (conventions, beta_H) | theorem | Restated T24: P_x(S0 not scored within H terminal rounds) <= P(Bin(H,c_*)<v)+H*eta <= v(1-c_*)^floor(H/v)+H*eta, exact polynomial constants (c2 >= 1/(B+3)-eps_del), no factorial | PROVED (candidate); SF VERIFIED* (W2-VT24G, after Lemma F' repair); XF VERIFIED after F' repair (A-REV1; statistical application GAP); XF VERIFIED finite feasible uninterrupted bound (A-REV5); vacuous at n=200 | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/PROOF.md; W2-VT24G/REPORT.md; W6-FIXREV1/CONSOLIDATED.md; A-REV1/REVIEW.md; A-REV5/REVIEW.md; T38-RECORD/LOCKABLE_v2.md | [pos 238] [pos 296] [pos 342] [pos 370] [pos 470] [pos 570] [pos 742] [pos 919] | K58 FUTURE_WORK (FW7); FW26 (finite-n Gibbs discovery dropped: ThmB-T24 vacuous at n=200); supplement item on LOCKABLE; feeds none of M1-M8 |
| TH219 | Theorem B'; B1'/B2'-VT24G; Props. B1'/B2'; Theorem B' (B sharpened) | theorem | Scoring sharpening: at Hamming distance one the Gibbs evaluation scores S0 so eps'_del(1)=0, c'2=1-H1>=1/(B+3) with no statistical premise | PROVED (candidate; authored by the verifier W2-VT24G, no SF); XF VERIFIED with empty-supremum convention (A-REV1) | W2-VT24G/PROOF.md; W2-VT24G/REPORT.md; A-REV1/REVIEW.md | [pos 370] [pos 470] [pos 557] | feeds: none (campaign-only) (carried inside beta_H of TH218) |
| TH220 | Theorem B-sharp; ThmB♯; B♯; Theorem B♯ (monotone look-alike map); Theorem B'/B♯ | theorem | Theorem B holds verbatim with a start-adapted family built from a monotone look-alike map (proof device) and c1# = max{1-eps_add#,(1-eps_pt#)//M(x)/} | PROVED (candidate; author only W2-PREM; closure (F3) flagged for review); not certified by A-REV5 (B-sharp/CMP not promoted) | W2-PREM/PROOF.md; W2-PREM/REPORT.md; A-REV5/REVIEW.md | [pos 342] [pos 424] | feeds: none (campaign-only) |
| TH221 | Prop. D; Proposition D; PropD-drift; drift form | proposition | Drift form of Theorem B: P_x(not scored within H) <= H*eta_ex + inf_{z>1} rho(z)^H z^{v-1}; only H*eta_ex -> 0 needed | PROVED (candidate); SF VERIFIED (W2-VT24G); XF none; vacuous when v>H | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md | [pos 296] [pos 370] | feeds: none (campaign-only) |
| TH222 | Cor. B-unif; Corollary B-unif; CorB-unif | corollary | Theorem B uniformly over a data-measurable eligible set fixed before selection (inf c_*, sup v, sup eta) | PROVED (candidate); SF VERIFIED (W2-VT24G); XF none | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md | [pos 296] [pos 370] | feeds: none (campaign-only) |
| TH223 | Cor. B-M; Corollary B-M; CorB-M; route (e-M) | corollary | Many particles: P(S0 unscored / population) <= prod_i beta_H(x_i), past-measurable selection, given IND-T | PROVED (candidate) given (R5)=IND-T; SF VERIFIED* (wording GAP, W2-VT24G); XF VERIFIED* (A-REV1); XF VERIFIED (A-REV5 after wording repair) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W6-FIXREV1/CONSOLIDATED.md; A-REV1/REVIEW.md; A-REV5/REVIEW.md | [pos 296] [pos 370] [pos 470] [pos 742] [pos 919] | feeds: none (campaign-only) (route (e-M) of T21; delivery counterpart DELIV) |
| TH224 | Cor. P1; Corollary P1; CorP1; distance-one scoring | corollary | If x differs from S0 by one coordinate, P(S0 scored next round) >= a1(x)=int prod(1-t q_e)dt; a1>=0.14 at n=200,B=4 | PROVED (candidate); SF VERIFIED (W2-VT24G; numerics only at B=4); XF VERIFIED (A-REV1) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md; A-REV1/REVIEW.md | [pos 296] [pos 370] [pos 470] | feeds: none (campaign-only) |
| TH225 | Prop. A; Proposition A; PropA-sweep; one-round sweep | proposition | Probability the round does not end at S0 is <= eps2(a); proves a whole repair inside one round but is numerically vacuous (eps2(1)~2.6) | PROVED (candidate); SF VERIFIED (proof); vacuous numerically | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md | [pos 296] [pos 370] | feeds: none (campaign-only) |
| TH226 | Props. B1, B2; PropB1-B2; Prop. B1; Prop. B2; phase-1 and phase-2 progress | proposition | Per-round no-bad-no-progress probability <= eps_add (phase 1) and <= eps_del+H_a (phase 2); c2 >= 1/(B+3)-eps_del | PROVED (candidate); SF VERIFIED (B2 after F'); XF VERIFIED* (A-REV1: B1 VERIFIED, B2 VERIFIED after F') | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/PROOF.md; A-REV1/REVIEW.md | [pos 296] [pos 370] [pos 470] | feeds: none (campaign-only) |
| TH227 | Prop. U'; Proposition U'; PropU; Prop. U; Proposition U; W6F1-PropU'; corrected undo classification; EXIT_d resolution | proposition | Bad(W) = leaves family or raises V or removes a truth, for every label; extra-for-extra swap neutral iff it stays in family; independence step charged by beta_I(W) | Original Prop. U: PROVED (candidate), SF VERIFIED as bookkeeping (W2-VT24G), XF ERROR (A-REV1) [CONFLICT C3]; repaired Prop. U': PROVED (W6-FIXREV1, same-family); XF VERIFIED (A-REV5); Theorem B unaffected | W6-FIXREV1/CONSOLIDATED.md; W1-T24G/PROOF.md; A-REV1/REVIEW.md; A-REV5/REVIEW.md | [pos 296] [pos 370] [pos 470] [pos 570] [pos 742] [pos 919] | feeds: none (campaign-only) (lockable only via W6 repair) |
| TH228 | IND-T; Theorem IND-T; conditional independence of terminal trajectories; (R5) | theorem | Given the stage-T history, terminal trajectories of distinct particles are independent Markov chains with the extended round kernel (stopping-time argument on the shared stream); H'=L+5 | PROVED (author only W2-PREM; SF none); XF VERIFIED* for the uninterrupted process (A-REV1); XF VERIFIED with uninterrupted-process scope (A-REV5) | W2-PREM/PROOF.md; W2-PREM/REPORT.md; A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md; A-REV5/REVIEW.md | [pos 342] [pos 424] [pos 470] [pos 742] [pos 919] | L-T12 (K86 via S-OUT); named premise of M1 (V/H) clauses (c),(d); S-OUT; IND-T extension audit pending (N14(c)) |
| TH229 | Prop. B1' (W2-PREM); Prop. PA; B1'-PREM+PA; pointwise addability; BTP replacement | proposition | Phase-1 progress >= (1-eps_pt)//M(W)/ from pointwise addability; PA: eps_pt=n^{-omega(1)} under G,R,SE(k),BM-inf; BTP not needed | PROVED (candidate; author only W2-PREM); J* independence flagged for review; no XF | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| TH230 | Prop. T2; PropT2-PREM; truth removal at supersets; tau_2 | proposition | Truth removal at supersets by Gibbs, uniform swap or neighbour swap is n^{-omega(1)} under SE(s0+a+2), BM-inf | PROVED (candidate; author only W2-PREM) | W2-PREM/PROOF.md | [pos 424] | feeds: none (campaign-only) |
| TH231 | NL0(0); UDEL(1); NL0(0)/UDEL(1) | proposition | Leakage at S0 itself and single-extra deletability are O_P(log n/sqrt n) with no design condition | PROVED (candidate; author only W2-PREM) | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| TH232 | NL0(a); UDEL(a>=2); NL0(a)/UDEL(a>=2); Prop. NL0; Prop. UDEL; PG(a); W6F1-NL0'; NL0'; Lambda_2(a) | proposition | Superset leakage Lambda_2(a)=sum_l sup_W o_l(W) and deletability decay under the partner-graph condition PG(a); correct sum-of-suprema quantifier form | PROVED UNDER PG(a) (author only W2-PREM); XF VERIFIED as quantifier correction (A-REV5; CMP not certified) | W2-PREM/PROOF.md; W6-FIXREV1/CONSOLIDATED.md; A-REV1/REVIEW.md; A-REV5/REVIEW.md | [pos 424] [pos 742] [pos 919] | feeds: none (campaign-only) |
| TH233 | TS; Prop. TS; TS(W) | proposition | Gibbs truth removal at incomplete states is n^{-omega(1)} under the coefficient non-cancellation condition TS(W) | PROVED UNDER TS(W) (author only W2-PREM); COUNTEREXAMPLE without (cancellation pair) | W2-PREM/PROOF.md | [pos 424] | feeds: none (campaign-only) |
| TH234 | FS/TL#/ULR; Prop. SW; Prop. TL; Prop. ULR; FS; TL-sharp; ZJL+CS; ULR | proposition | Swap truth removal, junk additions at budget and look-alike retention are controlled under explicit conditions FS(D',c0)+p/log n->inf, ZJL+CS(g0), ULR(c0) | PROVED UNDER explicit conditions (author only W2-PREM); random designs OPEN | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| TH235 | IND-M; Prop. IM; Prop. IND-M; IM; independence-proposal bad acceptance; IND(F) | proposition | Independence-move bad acceptance beta_I <= (1-pi0(S°)) + 1{S° bad}pi(S°)/(pi(W)pi0(S°)); o_P(1/log n) under SCR(S°)+GS(S°), x ⊇ S° | PROVED UNDER SCR(S°)+GS(S°) (author only W2-PREM); superset starts OPEN | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| TH236 | Corollary A; CorA-PREM; Cor. A (W2-PREM); assembly of premises | corollary | Under the listed premises sup over eligible starts of P(S0 unscored in L+5 rounds) -> 0 | PROVED UNDER the listed premises (author only W2-PREM); not reviewed | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| TH237 | Theorem L; Theorem L (Gibbs-path repair on LH); LH premise table | theorem | On the linked-hub family LH with exact Gram, every premise of Theorem B-sharp holds (all but two numerical population inequalities proved) | PROOF SKETCH (W2-PREM); not promoted by A-REV5 | W2-PREM/PROOF.md; W2-PREM/results/lh_table.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| TH238 | AsymPremises-T24; asymptotic premises table; W1 section 6 premises; NL0, UDEL, TS, TL, BTP, IND | proposition | Asymptotic conditions under which Theorem B's constants hold: c_*>=1/(B+3)-o_P(1) and (L+4)eta=o_P(1) | PROOF SKETCH; SF GAP (NL0 inflation ERROR inside, W2-VT24G); XF GAP (A-REV1) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md; A-REV1/REVIEW.md | [pos 296] [pos 370] [pos 470] | feeds: none (campaign-only) |
| TH239 | T21-e'; T21 route (e'); route (e'); route (e-M); (e')/(e-M) | corollary | Theorem B (via beta_H) replaces H24 in T21 route (e); multi-particle form (e-M) | PROVED (candidate) as an implication; SF VERIFIED* (W2-VT24G with three edits; W5-LOCKBOOK CONSISTENT); XF none for W2-BOOK Thm 4(e') | W1-T24G/REPORT.md; W2-VT24G/REPORT.md; T38-RECORD/REGISTRY_v2.md | [pos 296] [pos 342] [pos 370] [pos 510] [pos 550] | Thm 4 route (e') (T21); FW26 / K58 FUTURE_WORK for the finite-n Gibbs discovery clause |
| TH240 | Theorem E3'; E3'; W6F1-E3'; Theorem E3 corrected; E3 (LS0 eligibility) | theorem | LS0 eligibility: start mode in TD' set implies S0 scored; (ii) start-mass bound (1-q)^{s+1}/(1+e)^s > 1/2 requires 0<=q<1; LS0 cost 1+(l+1)max[p+k(p-k)] | Original E3: PROVED (W1-T38E), SF VERIFIED incl. (ii) (W3-VT38E), XF ERROR on (ii) (A-REV1); repaired E3': PROVED (W6-FIXREV1); XF VERIFIED (A-REV5); LOCKABLE (A-REV5 item 3) | W6-FIXREV1/CONSOLIDATED.md; W1-T38E/PROOF.md; A-REV1/REVIEW.md; A-REV5/REVIEW.md | [pos 470] [pos 570] [pos 742] [pos 919] | theme 6/7: T38 (b1) route; M5 via b1 |
| TH241 | T38b-R(whole); T38b-R(b1); T38b-R(b1′); T38b-R(b2); Theorem T38(b)-R; T38(b)-R composition; T38b-R(whole); T38(b)-R; Theorem T38(b)-R; v0; W1-T38E section 7; (duplicate entry TH241 merged) | theorem | Composition of the discovery term into liminf P(U^c, Shat+ = S0) >= 1 - limsup P(U) via routes (b1) LS0+TD', (b1') pilot D2, (b2) DELIV+REPAIR | PROVED given named inputs (W1-T38E); SF VERIFIED (W3-VT38E); XF GAP as supplied, composition and (b1) VERIFIED, (b1'),(b2) GAP, repaired formulation VERIFIED (A-REV1); superseded by T38-(0) (W6-FIXREV1 v2/T38-RECORD v3) | W1-T38E/PROOF.md; W1-T38E/REPORT.md; W3-VT38E/REPORT.md; T38-RECORD/T38_STATEMENT.md | [pos 238] [pos 370] [pos 557] [pos 570] [pos 201] [pos 238] [pos 342] [pos 370] [pos 570] | feeds M5 Theorem HPM only via T38-(0) (K72 composition); route (b1) content K65/K69 (theme 7); (b1'),(b2) none (campaign-only) |
| TH242 | D2; Theorem D2; Corollary D2-inf; D2-∞; D2-infinity; W6F1-D2inf; NB'; NB′; no-blow-up event; pilot one-flip discovery | theorem | If a one-flip neighbour x° of S0 has start mass > 1/10 the pilot's first round scores S0 with prob >= 1 - e^{-2Ht^2} - P(NB'^c) - exp{-H(1-Dep)g(b-t)/(k_D+B+3)}; D2-inf rate-margin corollary | PROVED (W1-T38E); SF VERIFIED* after r* repair and NB' weakening (W3-VT38E); XF VERIFIED (A-REV1, finite uninterrupted-pilot bound); D2-inf PROVED (implication) (W6-FIXREV1), rate margins VERIFIED (A-REV5) | W1-T38E/PROOF.md; W3-VT38E/REPORT.md; W6-FIXREV1/CONSOLIDATED.md | [pos 238] [pos 370] [pos 557] [pos 570] | feeds: none (campaign-only); route (b1') of T38 statement of record, not in final M5 card list |
| TH243 | E3-core; Theorem E3; Theorem E3′; E3'; E3(ii); LS0 eligibility | theorem | LS0 (local search from the start mode) scores S0 when S~0 lies in a TD' basin; pi0(x°) > 1/2 identifies the mode; corrected (ii) needs 0 <= q < 1; cost 1+(l+1)max_k[p+k(p-k)] | PROVED (W1-T38E); SF VERIFIED (W3-VT38E); XF (i),(iii) and core VERIFIED/VERIFIED*, (ii) ERROR (A-REV1); E3' PROVED (deterministic) (W6-FIXREV1) | W1-T38E/PROOF.md; W6-FIXREV1/CONSOLIDATED.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] [pos 557] [pos 570] | feeds M5 (b1-LH) / Theorem b1 (K65, K69; theme 7) |
| TH244 | D1; Theorem D1; T15 route | theorem | P(no R_d particle of island r at tau) <= pi(R_d^c)/c + P(Zhat_r/Z < c) (from locked T15) | PROVED from locked T15 (W1-T38E); SF VERIFIED (W3-VT38E); not viable in the masked regime | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | feeds: none (campaign-only) |
| TH245 | D3; Proposition D3; forward chain; SHARE/EXIT-end | proposition | P(A_T^c/C) <= (1-pi0(R_d))^N + sum_t(zeta_t+eta_t) under SHARE(zeta) and EXIT-end(eta) | PROVED (conditional on SHARE) (W1-T38E); SF VERIFIED (W3-VT38E: SHARE is nearly the conclusion); XF GAP (A-REV1 Section 7.2); superseded by W4-SHARE D4/D5 | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | feeds: none (campaign-only; superseded) |
| TH246 | E1-T38E; Proposition E1; E1 | proposition | F(S∪P) - F(S) >= -/P/[log 2p + 1/2 log(n+1)]; hence F(S0)-F(S°) > kappa_n(d) implies some S outside R_d beats S° | PROVED (deterministic) (W1-T38E); SF VERIFIED (W3-VT38E); margin step PROOF SKETCH | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | feeds: none (campaign-only) |
| TH247 | V1-TDfails; Proposition V1; TD(d,m) fails universally | proposition | On {pi(S0) > 1/2}, T37's TD(d,m) fails for every d >= 1 and m >= 0 in every design (swap l->j beats adding j) | PROVED (W3-VT38E, verifier-authored, two lines); not itemised by A-REV1 | W3-VT38E/REPORT.md; W1-T38E/PROOF.md | [pos 370] | feeds: TD' restatement (theme 4); supplement negative result |
| TH248 | SHARE-D4; Theorem D4; space-time potential delivery bound; envelope theorem | theorem | P(n_T(W)=0/C) <= P(tau<=T/C) + exp{-N pi0(h0)(1-e^{-theta0})} under (TRACK) K_t h_t >= (1-eta_t)h_{t-1} | PROVED (W4-SHARE); SF VERIFIED* (W5-B2ENV REFEREE: Steps 1-5 VERIFIED, citation GAP IND-T); XF VERIFIED (A-REV3) | W4-SHARE/PROOF.md; W4-SHARE/REPORT.md; W5-B2ENV/REFEREE.md; A-REV3/REVIEW.md | [pos 364] [pos 371] [pos 444] [pos 742] | feeds: none (campaign-only) |
| TH249 | SHARE-D5; Corollary D5; fitness oscillation corollary | corollary | Under confinement and (TRACK): P(n_T(W)=0/C) <= P(E^c/C)+exp{-N pi0(h0)(1-e^{-c})}, 1/c <= [1+(T-1)/(e-1)]e^Gamma/prod(1-eta_s); delivery when Gamma - sum log(1-eta_s) <= log(N pi0(h0)/T) - omega(1) | PROVED (W4-SHARE); SF VERIFIED (W5-B2ENV); XF VERIFIED (A-REV3: replaces SHARE by another stochastic control condition, does not establish it for BVS) | W4-SHARE/PROOF.md; A-REV3/REVIEW.md; W5-B2ENV/REFEREE.md | [pos 371] [pos 742] | feeds: none (campaign-only) |
| TH250 | SHARE-G; Proposition G; Prop G; PropG-wording | proposition | Gamma <= max_t kappa_t for every grid (sum Delta_t = 1); no ESS-grid condition can imply SHARE | PROVED (W4-SHARE) as an upper bound; SF VERIFIED* (W5-B2ENV, wording GAP: not grid independence of Gamma); XF VERIFIED* (A-REV3), unrestricted no-grid-condition/BVS extrapolation GAP | W4-SHARE/PROOF.md; W5-B2ENV/REFEREE.md; A-REV3/REVIEW.md | [pos 371] [pos 742] | feeds: none (campaign-only) |
| TH251 | SHARE-SH; Proposition SH; SHARE-SH-prose; sharpness of log N threshold | proposition | Two-state toy: extinction prob -> 0 if kappa <= log(N pi0(a)) - omega(1), -> 1 if kappa >= 2 log N + omega(1); exact one-stage law | PROVED (W4-SHARE); SF VERIFIED* (W5-B2ENV: transition location is a heuristic); XF VERIFIED* (A-REV3: (i),(ii),(iii exact) VERIFIED, universal sharp-transition prose GAP) | W4-SHARE/PROOF.md; A-REV3/REVIEW.md | [pos 371] [pos 742] | feeds: none (campaign-only) |
| TH252 | SHARE-X; Proposition X; gate obstruction; PropX-moreover | proposition | P(some particle ever in U) <= N pi0(U) + N sum_k a_k per island (U = set entered from outside with round-entry probability a_k); posterior barrier is a gate | PROVED (W4-SHARE) main inequality; SF VERIFIED* (W5-B2ENV: Moreover and Use clauses GAP); no XF row | W4-SHARE/PROOF.md; W5-B2ENV/REFEREE.md | [pos 371] [pos 742] | feeds: none (campaign-only); cited as related for K99 qualitative barrier remark |
| TH253 | SHARE-M(a); Proposition M(a); Prop M (a) | proposition | Deterministic core: if lambda_min(R_{T∪M})>0 and M=S0\T nonempty then max_j delta_{T,j}^2 >= (n-1) lambda^2 //theta_M//_2^4///theta_M//_1^2 >= (n-1) lambda^2 theta_min^2 | PROVED (W4-SHARE); SF VERIFIED (W5-B2ENV; 20,000 instances); XF VERIFIED (A-REV3) | W4-SHARE/PROOF.md; A-REV3/REVIEW.md | [pos 371] [pos 742] | feeds: none (campaign-only) |
| TH254 | SHARE-B2W4; Theorem B2-W4; B2-W4 assembly | theorem | Route (b2) assembly: P(S0 not in S/C) <= [eps_E + exp{-N pi0(h0)(1-e^{-c})}]^4 + eps_rep given (TRACK),(OSC), confinement and REPAIR on W | PROVED given inputs (W4-SHARE); SF VERIFIED (W5-B2ENV, L+5 rounds note); XF VERIFIED* (A-REV3: conditional inequality VERIFIED, exit-loss line ERROR) | W4-SHARE/PROOF.md; W4-SHARE/REPORT.md; A-REV3/REVIEW.md | [pos 371] [pos 742] | feeds: none (campaign-only) |
| TH255 | OBG-BG1; OBG-CorBG1inf; Theorem BG1; Corollary BG1-∞; BG1 | theorem | Pilot first-stage bridge-Gibbs discovery: P(z not in S_cal) <= H pi0(A) + exp{-H pi0(x°)/8} + 1/K + exp{-H beta/(1+2K rho_N)} | PROVED-UNDER (author only; stated for the PILOT with floor phi1 >= min(1,1/T_e)) | O-BGIBBS/REPORT.md | [pos 594] [pos 748] [pos 763] | feeds: none (campaign-only) |
| TH256 | OBG-BG1′; Corollary BG1′; BG1' | corollary | BG1 with temperature-dependent constant beta(phi); covers the final run's stage 1 at any phi_1^f; needs only N beta_* -> infinity | PROVED (author only; A-REV7 pending, no verdict) | O-BGIBBS/REPORT.md | [pos 748] [pos 763] | feeds: none (campaign-only) |
| TH257 | OBG-BG2; Theorem BG2; cumulative scoring hazard | theorem | P(z not scored in rounds 1..t1) <= P(Lambda_{t1} < Lambda) + e^{-Lambda}, Lambda_t = sum m_s beta_s: discovery is a hazard, not a survival event | PROVED (author only) | O-BGIBBS/REPORT.md | [pos 748] [pos 763] | feeds: none (campaign-only) |
| TH258 | OBG-BG3; Theorem BG3; BG3; locked start set + terminal downhill | theorem | P(z not scored in the island) <= N pi0(U^c) + N(T+L+4) eps_U + exp{-N(L+4) beta_1} (lock L1 and terminal downhill L2; terminal rounds have no resampling) | PROVED (deterministic given (L1),(L2)) (author only); XF VERIFIED (A-REV7: abstract round-boundary lock and terminal scoring inequality given EX-A/EX-S/SR; A-REV6 conditional template); inequality VERIFIED by API-VSTAB (Claude) | O-BGIBBS/REPORT.md; A-REV7/REVIEW.md; API-VSTAB/REPORT.md | [pos 748] [pos 763] [pos 919] [pos 978] | feeds: none as a card; fixed-p component lemma (T38 statement N4) |
| TH259 | OBG-LH-P1; OBG-LH-ii-iv; Proposition LH; Prop LH | proposition | Premises of BG1 on LH exact Gram: projection algebra (P1) and pi0(S°)->1 (i); H pi0(A)->0, rho_N = O_P(2^B n^{-1/2}), beta >= g^{-c}-type constants (ii)-(iv) | structure PROVED, (ii)-(iv) PROOF SKETCH (author only); (i) is W1-EXP Thm 5(a) VERIFIED by W3-VEXP | O-BGIBBS/REPORT.md | [pos 748] [pos 763] | feeds: none (campaign-only) |
| TH260 | OBG-LH-rate; Proposition LH-rate; LH-rate | proposition | Scoring rate from the start mode on LH: beta_S°(phi) >= P_c(1-o_P(1)) alphabar_phi^{c-1}; scoring temperature phi_sc | PROOF SKETCH (b_M part, a); uniform-in-phi proxy part CONJECTURE (author only) | O-BGIBBS/REPORT.md | [pos 748] [pos 763] | feeds: none (campaign-only) |
| TH261 | OBG-LH-lock; OBG-LH-lockC1p; LHlock-completion(A7); Proposition LH-lock; LH-lock; (C1′)/(C2′) | proposition | Premises of BG3 on LH exact Gram with p fixed under strict gaps C1-C3 (and block gaps C1',C2'): pi0(U^c) <= e^{-c3 n}, eps_U <= m e^{-c3 n}, beta_1 >= (1-o(1))/m! | PROOF SKETCH (author only); XF VERIFIED* as a conditional fixed-p implication from strict C1-C3 and block keep margins (A-REV7, Astra-authored completion); C1',C2' VERIFIED/PROVED on LH; unrestricted locking ERROR | O-BGIBBS/REPORT.md; A-REV7/REVIEW.md | [pos 748] [pos 763] [pos 919] [pos 941] [pos 945] | feeds: none (campaign-only) |
| TH262 | OBG-T38b-noLS0; T38(b) without LS0 via BG1 | theorem | P(S0 not in S) -> 0 on LH exact Gram for every fixed c >= 1 for the original method (pilot, BG1 + Prop LH (ii)-(iv) + T38(0)) | PROOF SKETCH (author only; author P(true) 0.85, P(provable) 0.7) | O-BGIBBS/REPORT.md | [pos 748] [pos 763] | feeds: none (campaign-only; superseded by TH263 and TH272) |
| TH263 | OBG-T38b-BG3; N4 of T38 v3; T38(b) without LS0 on LH, p fixed | theorem | P(O ∩ {Shat != S0}) -> 0 for v3 as run (no LS0) on LH exact Gram with p fixed, every fixed c (BG3 + LH-lock + T38(0)) | PROOF SKETCH (composite carries the weakest input's word); XF VERIFIED* (A-REV7: BG3 + conditional LH-lock for fixed p, component lemma not the headline) | O-BGIBBS/REPORT.md; A-REV7/REVIEW.md; T38-RECORD/T38_STATEMENT.md | [pos 763] [pos 919] | feeds: none (fixed-p component lemma) |
| TH264 | FSH-F1; Theorem F1; closed-class delivery; KEEP(W,eta) | theorem | Under KEEP, P(some particle ever outside W/C) <= N pi0(Omega\W) + N(T+L+4) eta per island; DELIV(W) with whole population eligible | PROVED (author run); XF VERIFIED (A-REV7: round-boundary closure given KEEP, does not supply repair; A-REV6 usable as conditional template) | F-SHARE/REPORT.md; F-SHARE/PROOF.md; A-REV7/REVIEW.md | [pos 444] [pos 474] [pos 748] [pos 919] | feeds: none (campaign-only); abstract closure lemma |
| TH265 | FSH-F3; Corollary F3; no C1 under KEEP | corollary | Under KEEP the W-count is N at every stage w.p. -> 1, the D4 envelope is deterministic prod(1-eta_s) and the C1 mechanism cannot start | PROVED (author run; no verifier) | F-SHARE/REPORT.md; F-SHARE/PROOF.md | [pos 748] | feeds: none (campaign-only) |
| TH266 | FSH-F2; Theorem F2; F2 (LH closed superset class) | theorem | LH exact Gram, p <= (1-c0)n, PK(g-1), DOM: the superset class W(S°) is closed with KEEP eta <= C p^2 e^{-cn}; DELIV(W) with every particle eligible | PROOF SKETCH (structure PROVED, Gaussian estimates PROOF SKETCH) (author run); XF GAP (A-REV7; c=1 DOM exemption ERROR; A-REV6 GAP) | F-SHARE/PROOF.md; F-SHARE/REPORT.md; A-REV7/REVIEW.md | [pos 748] [pos 763] [pos 919] | feeds: none (do not cite F2) |
| TH267 | FSH-T38b2; FSH-S4; T38(b2) on LH exact Gram no tweak; N5 of T38 v3 | theorem | Gibbs-path route with delivery by closure: F2 + scoring on W(S°) (Section 4) + T38(0), every fixed c, no LS0 | PROOF SKETCH (composite; no separate status word; author P(true) 0.85, P(provable) 0.5); XF GAP (A-REV7: not to be cited as a growing-p no-LS0 guarantee) | F-SHARE/REPORT.md; F-SHARE/PROOF.md; A-REV7/REVIEW.md | [pos 748] [pos 919] | feeds: none |
| TH268 | B2E-NBLH; Theorem NB′-LH; NB'-LH | theorem | On LH exact Gram with c=1, P(NB'^c/data) = O_P(sqrt(n)/p + n^{-1/2}) (via Lemma OF and start tails) | PROVED-UNDER (author, given W1-EXP Thm 1/6, Lemma 4.1-4.2); XF VERIFIED* (A-REV7, corrected NB') | W5-B2ENV/PROOF.md; A-REV7/REVIEW.md | [pos 510] [pos 742] [pos 919] | feeds: none (campaign-only) |
| TH269 | B2E-D2LH; Corollary D2-LH; D2-LH; (b1′-LH); N1 of T38 v3; (b1'-LH); (b1′-LH); Cor. D2-LH; Corollary D2-LH; B2E-D2LH; N1 (T38-RECORD I.D); (duplicate entry TH269 merged) | corollary | LH exact Gram, c=1, p/sqrt(n)->infinity: P(S0 not in S_cal) = O(sqrt(n)/p) + o(1) -> 0, so the original method (no LS0) is consistent | PROVED-UNDER (author, given D2, E-T1, E-L4, E-T5d); XF VERIFIED for qualitative consistency, GAP for the stated unconditional O(sqrt n/p) rate (A-REV7) | W5-B2ENV/PROOF.md; A-REV7/REVIEW.md; T38-RECORD/T38_STATEMENT.md | [pos 742] [pos 919] [pos 696] [pos 742] [pos 919] | feeds: none in final M5 card list (statement-of-record clause b1′-LH only) |
| TH270 | B2E-MLH; Proposition M-LH; Prop M-LH; Prop M(b) on LH | proposition | On LH the lattice edges toward S0 have log kappa_0 ≈ -log(2p/s) - 1/2 log n and log kappa_1 >= n g_*/2(1-o(1)), so gamma_phi increases along the lattice for phi >= phi_n = O(log n/n) | PROVED (author, given E-T1); XF VERIFIED (A-REV6 restricted fixed-coefficient lattice replacement; A-REV7: exact log-RSS argument, unaffected by A-REV3 ERROR) | W5-B2ENV/PROOF.md; A-REV7/REVIEW.md | [pos 742] [pos 919] | feeds: none (K98 dropped M(b)) |
| TH271 | B2E-CONF; Proposition CONF; Corollary CONF-run; one-round confinement | proposition | P_x(one round ends outside N) <= a_n = O_P((log n/n)^{3/2}) uniformly in phi and x in N = {S ⊇ S°, <= 19 neutral extras}; no final particle leaves N before stage T w.p. 1 - O_P(log^{3.5}n/sqrt n) | PROVED under STAB-LH (author); XF VERIFIED* (A-REV7: checked against actual moves); Claude check API-VSTAB item 8 VERIFIED | W5-B2ENV/PROOF.md; A-REV7/REVIEW.md; API-VSTAB/REPORT.md | [pos 742] [pos 919] [pos 978] | feeds: none (campaign-only; part of K70 proof) |
| TH272 | B2E-B2LH; Theorem B2-LH; B2-LH; (b2-LH); K70; N3 of T38 v3; STAB-LH; (b2-LH); Theorem B2-LH; B2E-B2LH; N3 (T38-RECORD I.D); K70; (duplicate entry TH272 merged) | theorem | LH exact Gram, every c, under STAB-LH, any frozen grid, no LS0: P(S0 not in S/C) <= N pi0(N^c) + N T_e a_n + (1-c0+r_n)^N -> 0, hence liminf P(U^c, Shat = S0) >= 1 - limsup P(U) for v3 as run | PROVED-UNDER STAB-LH (author, W5-B2ENV); XF VERIFIED* conditional theorem (A-REV7, eta_n corrected); theorem-specific parts cross-checked by Claude (API-VSTAB) | W5-B2ENV/PROOF.md; W5-B2ENV/REPORT.md; A-REV7/REVIEW.md; API-VSTAB/REPORT.md; MEET-THM/THEOREM_LIST_FINAL.md | [pos 510] [pos 742] [pos 919] [pos 957] [pos 1650] [pos 696] [pos 742] [pos 919] [pos 945] [pos 978] | feeds M5 Theorem HPM as the labelled no-LS0 variant clause (b2-LH), K70 |
| TH273 | B2E-latpot; B2ENV-finding; lattice-indicator potential negative | proposition | Lattice-indicator potentials have Gamma + sum eta >= log(NT) - O(1) while D5 needs <= log(N pi0(h0)/T) - omega(1): cannot certify delivery at any budget; on LH the right potential 1_N gives Gamma = 0 | PROOF SKETCH (author only; numerically confirmed) | W5-B2ENV/PROOF.md; W5-B2ENV/REPORT.md | [pos 742] | feeds: none (campaign-only) |
| TH274 | STAB-cert(A7); analytic STAB certificate; (CERT) | proposition | If lambda0 b_vis^2 > R_M then m_STAB >= lambda0 b_vis^2 - R_M for every proxy configuration and any number of null columns (lambda0=(1-max/psi/)(1-rho_max), R_M = sum beta_i^2 psi_i^2(1-psi_i^2)) | REFEREE (Astra-authored, Sol check agreed); PROVED and VERIFIED by Claude (API-VSTAB, exact check 0 violations in 1500 configurations) | A-REV7/REVIEW.md; API-VSTAB/REPORT.md | [pos 919] [pos 978] | feeds M5 variant clause (b2-LH) K70 (flag: STAB-cert Astra-authored, Claude-verified) |
| TH275 | B2LH-subfamily(A7); no-LS0 masked consistency on F_cert; explicit growing-p subfamily; g=9,c=2,rho=0.4,psi=0.2 | theorem | Unchanged v3, no LS0, on LH exact Gram satisfying (CERT) (explicit member g=9,c=2,rho=0.4,psi=0.2,beta=1,sigma^2=1,p_n=9 floor(n/18)): P(O ∩ {Shat != S0}) -> 0 | PROVED (candidate) given cited inputs (API-VSTAB); B2-LH XF VERIFIED* (A-REV7); certificate and subfamily Astra-authored, Claude VERIFIED; IND-T flagged without Claude verifier | API-VSTAB/REPORT.md; A-REV7/REVIEW.md; MEET-THM/THEOREM_LIST_FINAL.md | [pos 919] [pos 978] | feeds M5 labelled variant (b2-LH), K70 (hypothesis STAB-LH g=9, c=2, rho=0.4, psi=0.2) |
| TH276 | fixed-p component corollary on (CERT); Corollary fixed-p BG3/LH-lock on (CERT) | corollary | On (CERT) the strict gaps C1-C3 of LH-lock hold at every fixed p, so the fixed-p BG3/LH-lock bound holds with no further hypothesis | PROVED (API-VSTAB, one run) | API-VSTAB/REPORT.md | [pos 978] | feeds: none (campaign-only; component) |
| TH277 | T21; T21 (old label T14-H); Theorem 4 (locked T21); (C1) locked; T21 routes (a)-(f); T21_T14H_HPM_composition | theorem | Locked pre-campaign composition: P(U or S-hat != S0) <= P(U) + 2E0[delta1] + P(U^c, S0 not in S-scr), with discovery routes (a) fresh iid draws, (b) Gibbs execution, (c) swap execution, (d) tables and scans, (e) terminal repair under H24, (f) exact branch | PROVED-LOCKED (C1 and routes (a)-(f), wave 2) + CONDITIONAL on open hypotheses: H24 (route (e)) and the route-specific occurrence / exposure conditions; not adopted; checked pre-campaign by Astra lead, two Sol reviewers, Astra xhigh closing review, Claude Opus audit (fixes E1, E3 applied); Lean t21_C1 sorry-free, fidelity GREEN (L-LEAN) | main@c4ef0dc/Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md; main@c4ef0dc/Docs/Theory/one_pagers/T21.md; main@c4ef0dc/Docs/Theory/theorems/T21_T14H_HPM_composition.md | pos: n/a (pre-campaign); [pos 119] [pos 156] | M5 Theorem HPM (K72) as the descendant; Lean t21_C1 (L-TA) |
| TH278 | Thm4-C1; Theorem 4 (restated T21); Thm 4 (W2-BOOK); Theorem 4 composition (W5-LOCKBOOK STATEMENTS.tex); (C1') | theorem | Thm 4 restated on the potential uninterrupted run under GUARD: P(U or S-hat != S0) <= P(U) + 2E0[delta1] + P(U-bar^c, S0 not in S-bar), P(U) <= P(G) + P(U-bar); routes (a), (d), (d+), (e'), (e-M); H24 retired | PROVED (candidate) as an implication; (e') conditional on W1-T24G Theorem B; registry Thm4-C1 'PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none)' (A-REV1 s7.4 verifies the same set-inclusion argument inside T38(b)-R; W2-BOOK Theorem 4 itself has no direct XF verdict); needs convention G in U (G1) | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W2-BOOK/STATEMENTS.tex; W5-LOCKBOOK/STATEMENTS.tex; W5-LOCKBOOK/REPORT.md; W8-SYNTH/SYNTHESIS.md | [pos 328] [pos 342] [pos 463] [pos 550] [pos 742] | M5 Theorem HPM (K72 composition at every n); Lemma RO to S-OUT (K77) |
| TH279 | (d+); (d⁺); Thm 4 route (d+); T37 wiring; TD* route | theorem | If a restated T37(i) closes (event TD*), it enters Thm 4 as a strengthening of the scan route (d): P(U-bar^c, S0 not in S-bar) <= P0(TD'^c) + P(no local-search centre in R_d) + 1{l < s0+d-1}; with LS0 the middle term is at most P(S~0 not in R_d) | PROVED as an implication; T37 itself OPEN (W2-BOOK); W5-LOCKBOOK: CORRECT as an implication, sharpened (cap 1{l < s0+d-1}, scan-before-limit); feeds Theorem A route | W2-BOOK/PROOF.md s4.3; W2-BOOK/REPORT.md s2; W5-LOCKBOOK/STATEMENTS.tex; W5-LOCKBOOK/REPORT.md | [pos 328] [pos 342] [pos 742] | M5 (a) Theorem A / LS-score (K65, K64) |
| TH280 | (e'); (e′); (e-M); Thm 4 route (e'); Thm 4 route (e-M); route (e) via Theorem B | theorem | Gibbs-path terminal repair with H24 replaced by Theorem B at the selected state: P(U-bar^c, S0 not in S-bar) <= P(A^c) + E[1_A min{1, beta_H(X_sel)}], beta_H(x) = P(Bin(H, c_*(x)) < v(x)) + H eta(x), H <= L+5; (e-M) replaces min{1,beta_H(X_sel)} by the product over eligible particles | PROVED as an implication of Theorem B (W2-BOOK); W5-LOCKBOOK: (e') CORRECT, (e-M) CORRECT given (R5) = Lemma STREAM; inherits status of Theorem B (A-REV1: VERIFIED after F' repair; A-REV5: VERIFIED); statistical instantiation and delivery OPEN | W2-BOOK/PROOF.md s4.1; W5-LOCKBOOK/STATEMENTS.tex; W5-LOCKBOOK/REPORT.md; A-REV1/REVIEW.md; A-REV5/REVIEW.md | [pos 328] [pos 342] [pos 570] [pos 742] | supplement (Theorem B card, theme 5); not a main card (H24 dropped; (b2-LH) uses it) |
| TH281 | T38-(0); T38 (0); Theorem 5 (0); T38(b)-R composition; (0); K72; W6F1-T38 (0) | theorem | For every n (both variants, strict convention): P(O and S-hat+ != S0) <= 2E0[delta1] + D_n, D_n := P(O-bar and S0 not in S-bar+); if D_n -> 0 then P(O and S-hat+ != S0) -> 0 and P(O, S-hat+ = S0) - (1-P(U)) -> 0 (joint probability, not P(wrong / output)) | PROVED; SF VERIFIED (W3-VT38E); XF VERIFIED (A-REV1 s7.4; A-REV5 output/execution interface; A-REV8 'W6 versus A-REV1 s7'); Lean t21_C1 sorry-free, fidelity GREEN; registry T38-(0) 'PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))' | T38-RECORD/T38_STATEMENT.md I.C (0); W6-FIXREV1/T38_PROOF.md s1; W4-T38FULL/T38_PROOF.md s1; W1-T38E/PROOF.md s7; A-REV1/REVIEW.md s7.4; A-REV5/REV1_CHECK.md | [pos 201] [pos 370] [pos 570] [pos 919] | M5 Theorem HPM (0) (K72), K63 hypothesis |
| TH282 | (0_H); T38 (0_H); HPM convention composition; D_n^{sl} | theorem | Under the HPM output convention O_H: P(O_H and S-hat+ != S0) <= 2E0[delta1] + D_n + D_n^{sl}, D_n^{sl} := P(SMC and A^c and S0 not in S_cal u S_LS0) | PROVED; no SF check; XF VERIFIED (A-REV5, which keeps the schedule-limit discovery term); registry: 'HPM conv. PROVED, A-REV5 VERIFIED' | T38-RECORD/T38_STATEMENT.md I.C (0_H); W6-FIXREV1/T38_PROOF.md s1.3; A-REV5/REV1_CHECK.md | [pos 558] [pos 570] [pos 919] | not in M5 (strict convention only; HPM convention is an alternative, decision D1) |
| TH283 | T38-(a); Theorem 5 (a); T38 (a); favourable regime; K68 (a-fav) | theorem | Under (F): 1 - pi0(S0) -> 0 in probability, D_n -> 0 for both variants (HPM convention adds D_n^{sl} <= P(SMC and A^c), uncontrolled); inputs locked T11(iii), locked T22(iii) with EXP', W1-EXP Thms 2, 6 | PROVED-UNDER (F); SF VERIFIED* (inputs, W3-VEXP); ORTH joint family PROOF SKETCH; XF: none for the assembly (inputs A-REV2, A-REV5 VERIFIED for fixed designs) | T38-RECORD/T38_STATEMENT.md I.C (a); W4-T38FULL/T38_PROOF.md s2; W6-FIXREV1/T38_STATEMENT.md | [pos 364] [pos 370] [pos 919] | M5 (a-fav) labelled variant (K68) |
| TH284 | T38-(b1); (b1); Theorem b1; Thm-b1; LS0 route; T38b-R(b1); Theorem 5(b1) | theorem | With LS0: assume G, (P), OP-LS0, deterministic S°=U°∪P° with /P°/<=d and Phi(S°)<=phi-bar, (M1) ELIG, (M2) POP-LAT(S°, m_n), (M3); then S~0=S° and LS0 scores S0 within max{Phi(S°)-1,0} moves, D_n -> 0 and P(O and S-hat+ != S0) -> 0 | PROVED-UNDER (M1)-(M3); SF VERIFIED (W5-VMASK row 22); XF VERIFIED (A-REV8 'Thm 5(b1) conditional consistency VERIFIED'; A-REV5 'b1 direct route VERIFIED') | W4-T38FULL/T38_PROOF.md s3.3; W6-FIXREV1/T38_PROOF.md; W5-VMASK/REPORT.md; A-REV8/REVIEW.md; T38-RECORD/T38_STATEMENT.md | [pos 364] [pos 370] [pos 463] [pos 843] [pos 919] | M5 Theorem HPM (b1)/(b1-LH) (K69, K65) |
| TH285 | T38-(b1'); (b1'); (b1′); T38-b1′; T38b-R(b1′); D2 route; Theorem 5(b1′) | theorem | No method change: D2-infinity rate margins (fixed b0>1/10, /D_n/<=k_D, Dep_n<=1-c0, P(NB'^c)->0) imply the potential first stage of the tier-0 pilot scores S0, S-hat+ = S-hat | PROVED (implication) via D2-infinity; SF VERIFIED (W3-VT38E, finite D2); XF VERIFIED (A-REV1 finite D2 and D2-inf; A-REV5 rate margins); masked NB' instance on LH c=1 is part (b1'-LH); registry T38-b1' 'PROVED-UNDER ... GAP' for the statistical instance | T38-RECORD/T38_STATEMENT.md I.C (b1'); W6-FIXREV1/CONSOLIDATED.md s5; W1-T38E/PROOF.md s4; A-REV1/REVIEW.md s7.1; A-REV5/REVIEW.md | [pos 201] [pos 370] [pos 570] [pos 919] | not in M5 as a main part (supplement; delivery routes without LS0: theme 6) |
| TH286 | T38-(b2); (b2); T38-b2; T38b-R(b2); Gibbs-path route; Theorem 5(b2) | theorem | No method change: DELIV(X_n) (assumed) and REP(X_n) with a data-measurable eligible set X_n of repair-certificate states, H' = L+5 rounds at phi=1, capped beta_H; D_n -> 0 | PROVED (implication); XF VERIFIED as an interface (A-REV1 s7.2; A-REV5); DELIV(X_n) OPEN in general; D3 surrogate for DELIV GAP (A-REV5) | T38-RECORD/T38_STATEMENT.md I.C (b2); W6-FIXREV1/T38_PROOF.md s5; A-REV1/REVIEW.md s7.2; A-REV5/REV1_CHECK.md | [pos 201] [pos 570] [pos 919] | none (DELIV OPEN; FW13/FW26); (b2-LH) variant in M5 |
| TH287 | T38-b1-LH; (b1-LH); Corollary b1-LH; Cor. b1-LH; Theorem 5(b1-LH); K69 | corollary | Linked-hub family LH in exact Gram (p<=n-1): (P), (M1), (M2) with fixed margin m0>0, (M3) hold; pi0(S0)=p^{-c}n^{-c/2}e^{O_P(1)}; with LS0 P(O and S-hat+ != S0) -> 0 with no statistical hypothesis left open | PROVED (candidate); SF VERIFIED (W5-VMASK; W3-VEXP); XF VERIFIED (A-REV8 'exact-Gram b1-LH consistency VERIFIED ... with LS0; c=1 needs only its initial scan'); iid-failure clause ERROR (A-REV5) / GAP (A-REV8), repaired by V18 | W4-T38FULL/T38_PROOF.md s3.4; T38-RECORD/T38_STATEMENT.md I.C (b1-LH); A-REV8/REVIEW.md; A-REV5/REVIEW.md s2; W5-VMASK/REPORT.md | [pos 364] [pos 370] [pos 463] [pos 843] [pos 919] | M5 Theorem HPM (b1-LH) (K69) |
| TH288 | (b1-LH-iid); Theorem 5(b1-LH-iid); PXN Cor (b1); T38-b1-LH-iid; K71 | theorem | p >> n (LH-iid, g<=B_n<2g, n^a<=p<=n^A) with LS0: P(O and S-hat+ != S0) -> 0 for every fixed c (not in the headline) | PROVED (candidate); SF VERIFIED (W5-VMASK, with repairs R2-R7); XF GAP (A-REV3: P6, P7 and the joint route; A-REV6 and A-REV8: Lambda(a) Tr(c) range, P7 prints (n-3-s)/2); P1 VERIFIED via W7-PART B (A-REV6) | T38-RECORD/T38_STATEMENT.md I.C (b1-LH-iid); W5-VMASK/REPORT.md; W5-VMASK/REPAIRS.md; A-REV8/REVIEW.md; A-REV6/REVIEW.md | [pos 463] [pos 807] [pos 843] [pos 919] | FUTURE_WORK FW10 (K71); dropped from main cards |
| TH289 | T38-(c); (c); Theorem 5(c); Cost-T38; cost corollary of Theorem 5 | theorem | Score evaluations <= T32(i)'s ceiling plus 1 + (l+1) max_{k<=K}[p + k(p-k)] for LS0, polynomial in n under the v3 budgets; displayed order O((n+p)(p+B)log^2(n+p) + p^2 log^2(n+p)) carries an XF GAP | PROVED-UNDER T32(i); T32(i) PROVED (W5-LOCKBOOK), SF re-count W7-SEC; XF A-REV6 'supported by loop accounting' (no verdict word), A-REV9 deferred; displayed log^2 rate GAP (A-REV6); LS0 term PROVED and VERIFIED (A-REV1, A-REV5); registry Cost-T38 'PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))' | T38-RECORD/T38_STATEMENT.md I.C (c); W5-LOCKBOOK/PROOF.md s T32; A-REV6/BOOK.md R5; A-REV5/REV1_CHECK.md | [pos 201] [pos 370] [pos 742] [pos 919] | M8 Proposition D (K87 work, K64 scan term); polynomiality only |
| TH290 | T38-v3; T38_STATEMENT v3; Theorem 5 (T38) statement of record; T38-RECORD v3; paper Theorem 5 | theorem | Statement of record v3 of Theorem 5: (0), (0_H), (a), (b1), (b1'), (b2), (b1-LH), (b1'-LH), (b2-LH), (b1-LH-iid), (c), with change log V1-V21, Part III conflicts, Part IV decisions D1-D6; no new mathematics | PROVED-UNDER (registry 'T38-v3'); nobody reviewed v3 itself; every clause carries its source status; all PROVED are candidates | T38-RECORD/T38_STATEMENT.md; T38-RECORD/REGISTRY_v2.md; T38-RECORD/REPORT.md; T38-RECORD/LOCKABLE_v2.md | [pos 815] [pos 824] [pos 919] | M5 Theorem HPM (K72, K69, K65, K68; K63 hypothesis; K70 variant; K82 remark) |
| TH291 | W4-T38FULL T38_STATEMENT; Theorem 5 v1; T38 paper-ready statement (v1) | theorem | v1: first assembled Theorem 5 with parts (0), (a), (b1), (b1'), (b2), (b1-LH), (c), LS0 as an optional tweak, Lemma LS-score, Lemma M, Theorem b1, Prop. LH-LAT | candidate; SF: W4's own subagent VERIFIED the four new results, W5-VMASK VERIFIED; superseded by v2 (A-REV5: W6-FIXREV1 explicitly supersedes W4's statement) | W4-T38FULL/T38_STATEMENT.md; W4-T38FULL/T38_PROOF.md; W4-T38FULL/REPORT.md | [pos 364] [pos 370] [pos 474] | superseded by TH290 (v3) |
| TH292 | W6F1-T38; W6-FIXREV1 T38_STATEMENT; Theorem 5 v2; T38 corrected statement (v2) | theorem | v2: A-REV1 applied to v1: strict and HPM output conventions, GUARD (G1)/(G2), K=min(p, floor(n/2)), D2-infinity margins in (b1'), eligible set and repair certificates in (b2), direct set proof of (0), +1 in the LS0 cost | PROVED-UNDER (author); A-REV5 'T38 statement' overall ERROR (one clause: (b1-LH) iid-budget for c=2); interfaces (0), (0_H), b1, b1', b2 VERIFIED; A-REV8: v2 versus A-REV1 s7 VERIFIED; superseded by v3 | W6-FIXREV1/T38_STATEMENT.md; W6-FIXREV1/T38_PROOF.md; W6-FIXREV1/CONSOLIDATED.md; W6-FIXREV1/REPORT.md; A-REV5/REVIEW.md | [pos 558] [pos 570] [pos 611] [pos 919] | superseded by TH290 (v3) |
| TH293 | LH-LAT; Prop. LH-LAT; Proposition LH-LAT; POP-LAT on LH; VPGD LH-LAT | proposition | On LH (exact Gram), POP-LAT(S°, m0) holds with fixed m0 := min{(1-kappa_max)R_min, min_i beta_i^2(1-psi_i^2)^2, min_h theta_h^2} > 0; valid lower bound, sharp for homogeneous pairs, exact margin m0-sharp (W5-VMASK R5) | PROVED; SF VERIFIED (W5-VMASK rows 23, 23''; 'm0 is sharp' withdrawn as GAP overstatement); XF VERIFIED* (A-REV8: VERIFIED for fixed exact-Gram LH parameters; m0 a valid lower bound, not universal sharp margin) | W4-T38FULL/T38_PROOF.md s3.4; W5-VMASK/REPAIRS.md R5; A-REV8/REVIEW.md | [pos 364] [pos 370] [pos 463] [pos 843] | M5 (b1-LH) (LH-LAT m0 > 0 in the IC3 design); K69 |
| TH294 | T32(i); Theorem T32(i); T32(i-lit); Corollary T32(i-lit); T32(c); Corollary T32(c); score-evaluation ceiling of the SMC branch | theorem | Deterministic count: C_eval <= sum_b 2^{/C_b/} + sum_e {(1+4l) H_e [1+m(T_e+L+4)] + (l+1)[1+(l+1)M_p] + (l+1)(40p+1)} + 4N_{e*}[1+m(T_{e*}+L+4)] + (80p+1) + [1+(l+1)M_p]; conjectured form follows; polynomial in (n,p) | PROVED (W5-LOCKBOOK); SF re-count W7-SEC 'no error in the count'; XF A-REV6 'supported by loop accounting' (no verdict word); A-REV9 deferred; displayed T32(c) rate GAP (A-REV6); pre-campaign status CONJECTURED (not proved) | W5-LOCKBOOK/PROOF.md s T32; W5-LOCKBOOK/REPORT.md; main@c4ef0dc/Docs/Theory/one_pagers/T32.md; A-REV6/BOOK.md; W7-SEC/REPORT.md | [pos 463] [pos 510] [pos 711] [pos 742] | M8 Proposition D (search cost; K87/K64 context); registry conflict C18 |
| TH295 | T26-ThmA; W2-T26 Theorem A; Thm 6A; Theorem 6A; T26 (i)-(ii) premise form; Theorem A (T26) | theorem | Under EX-A, EX-S, CAL, START, OUT, (Omega), (P1) (T_n+1)Delta_n->0 and exact-branch twin (P1-ex): Z-hat/Z->1, PIPs->1{j in S0}, MPM=S0 in output form P(O_n and error>eps)->0; finite-n bounds (A-0); no (L+4)rho* premise | PROVED (candidate composition); SF CORRECT/VERIFIED (W5-LOCKBOOK); XF VERIFIED* (A-REV4) for the actual written statement, advertised single-premise shorthand GAP; A-REV6 VERIFIED; paper-1 table: Thm 6 overall CONJECTURE | W2-T26/PROOF.md; W2-T26/REPORT.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] [pos 919] | S-Z Proposition Z (vi) remark (K41, DRAFT-ONLY); registry flag T26-shorthand; not an M-card (Thm 6 overall CONJECTURE) |
| TH296 | T26-ThmB; W2-T26 Theorem B; Thm 6B; T26 discharged form | theorem | Adding T03 (G,R,SE,BM) and T22(iii) (EXP-prime,VIS,NL): (Omega),(P1) in deterministic-budget form and (P1-ex) hold with rate (T^max+1)Delta_n=O_P(log^2 n [2^B sqrt(log n) n^-kappa + e_n + sqrt(log n/n)]); EXP-prime only enters via 1-pi0(S0) | PROVED-UNDER (PROVED as a composition, CONDITIONAL on T03 and T22(iii)); SF CORRECT as conditional composition (W5-LOCKBOOK); XF VERIFIED* (A-REV4), VERIFIED (A-REV6) | W2-T26/PROOF.md; W2-T26/REPORT.md; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] [pos 919] | none directly (K41 DRAFT-ONLY); superseded on study-like designs by W5-FAVIID FAV-C2 |
| TH297 | Prop2(a,b,d,e); Proposition 2 (a),(b),(d),(e); Prop 2 restated T12+T31(i); islandwise unbiasedness; E[Z_r PIP_rj]=Z PIP_j; 0.05 Z-hat one-sided 95% lower bound | proposition | On the potential run given frozen C: E[Z_r]=Z, E[Z_r PIP_rj]=Z PIP_j, pooled island product unbiased, P(Z>=0.05 Z-hat)>=0.95, E log Z-hat<=log Z; output-level P(reported and 0.05 Z-hat>Z)<=0.05 P(A) with no conditioning on completion | PROVED (candidate; corollary of locked T12, T31(i), Lemma RO); SF VERIFIED/CORRECT (W5-LOCKBOOK); XF GAP (A-REV4: fixed-data probability convention B3, exact-branch extension B4); A-REV6 identity VERIFIED, convention GAP, W5 full-output expectation ERROR; repair [PENDING], A-REV6 R2 candidate | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | M1 Theorem V/H (K35,K36,K38,K46); M4 (K36 output-event clause); supplement L-T12 |
| TH298 | Prop2(c); Proposition 2 (c); pooled x pooled PIP bias; -3/4 Cov | proposition | E[Z-hat P-bar_j/C]=Z PIP_j - (3/4)Cov(PIP_1j,Z_1/C) (factor (I-1)/I for I islands); E[P-bar_j/C]-PIP_j=-Cov/Z; both nonzero in the T12(iv.b) instance (<-0.17 and <-0.1275 Z) | PROVED; SF VERIFIED/CORRECT (W5-LOCKBOOK, reproduced to 1e-58); XF VERIFIED (A-REV4, Owls 50-digit reproduction -0.1739741778 and -0.1317163950; A-REV6 VERIFIED) | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | M1 Theorem V/H (K50); supplement S-POOL; L-T12 |
| TH299 | Prop2(f); VAL-FP; VAL-FP(eta,epsilon); Proposition 2 (f) | proposition | If on G_fp the exact-arithmetic run on the same streams has the same status and C and /log Z-hat^fp - log Z-hat/<=eta, then P(reported and 0.05 Z-hat^fp>Z)<=0.05 e^eta + epsilon | PROVED-UNDER; SF GAP (wording; restated in W5-LOCKBOOK [APPLIED]); XF GAP (A-REV4: implication VERIFIED, no validated eta,epsilon; A-REV6 GAP operationally) | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | M1/disclosure; FUTURE_WORK FW16 (K107); related T33-Z (theme 9) |
| TH300 | FMP-M1; F-MASKPIP Proposition M1; M1; evidence-weighted PIP bound | proposition | For every data, frozen grid, N, island: E[W_r f_{r,s}]=delta1, E[W_r]=1, E[W_r Bbar_r]<=delta1+rho-bar, E[W_r err_r]<=delta1+rho-bar+u_pi with no premise on the start | PROVED (candidate); SF none; XF VERIFIED (A-REV9) under locked exact frozen-run assumptions | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | M1 Theorem V/H (K51 DRAFT-ONLY, masked h-bound); supplement L-T12 (FMP-M1); SYNTHESIS M7 |
| TH301 | FMP-M2; F-MASKPIP Corollary M2; M2; dichotomies | corollary | Markov consequences: non-crossing island has W_r<=sqrt(delta1) except w.p. 2 sqrt(delta1); island with W_r>=c has PIP error<=eps except w.p. (delta1+rho+u_pi)/(c eps); pooled/secondary and primary analogues; E[W_r 1{f>1/2}]<=2 delta1 | PROVED (candidate); SF none; XF VERIFIED (A-REV9) as intersection bounds, not completion-conditioned guarantees | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | S-Z masked tails (K40, exception-probability form only); SYNTHESIS M7 |
| TH302 | FMP-M3; F-MASKPIP Proposition M3; M3; no conditional evidence theorem from first moments | proposition | For crossing event C with P(C)=kappa: E[W_r/C]>=(1-2delta1)/kappa and E[W_r/C^c]<=2 delta1/(1-kappa); first moments cannot bound P(W_r<c/C) (valid conditional-mean part only, 0<kappa<1) | PROVED (author); XF ERROR on the printed probability-one instance, conditional means VERIFIED for 0<kappa<1 (A-REV9); registry row FMP-M3: PROVED (SF none; XF ERROR (A-REV9)) | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | K53 (R0_DIFF: FMP-M3 PROVED, XF ERROR); SYNTHESIS M7 |
| TH303 | FMP-ThmR; F-MASKPIP Theorem R; Theorem R (restart theorem for the PIPs); R | theorem | E err_r <= delta_X + beta_H + (L+4)rho-bar + u_pi and P(MPM!=S0)<=2[...] for a repair basin X, using no evidence quantity | PROVED as a composition, CONDITIONAL on DELIV-POP (OPEN) and REP (W1-T24G Theorem B, candidate); SF none; XF none (excluded by A-REV9) | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | FUTURE_WORK FW7 (K58); R0_DIFF K58 DRAFT-ONLY |
| TH304 | FMP-ThmRprime; F-MASKPIP Corollary R-prime; Corollary R'; n-indexed form of Theorem R | corollary | Under DELIV-POP, REP-ENT, T03 rate and (P-ex): P(O_n and max_j/PIP-hat_j-1{j in S0}/>eps)->0 and P(O_n and MPM!=S0)->0 | PROVED as a composition, CONDITIONAL on its inputs; SF none; XF none | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | FUTURE_WORK FW7 (K58) |
| TH305 | FMP-Na; F-MASKPIP Proposition N (a); N-a; evidence collapse on non-crossing realisations | proposition | If delta1->0 and liminf P(f_{r,0}>1/2)>=kappa then P(f>1/2 and W_r<sqrt(delta1))>=P(f>1/2)-2 sqrt(delta1); on non-crossing runs Z-hat_r underestimates Z by >=delta1^{-1/2} while T31(i) stays valid but uninformative | PROVED (author); SF none; XF GAP (A-REV9) on literal finite-n/unit-constant rate wording, corrected finite-index inequality VERIFIED | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | S-Z Proposition Z (iii) (K40, exception-probability form); SYNTHESIS |
| TH306 | FMP-Nb; F-MASKPIP Proposition N (b); N-b; reflected comparator | proposition | On a non-crossing realisation W_r is approximately pi(M)/pi0(M)<=delta1/pi0(M) for the region M the bridge explored | PROOF SKETCH; SF none; XF none | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | none (campaign-only; superseded by API-MASKZPIP E1/E2) |
| TH307 | FMP-Nc; F-MASKPIP Proposition N (c); N-c; explicit split family | proposition | On LH-type omission masking with one-stage grid T=1: W_r<=e^{-Theta(n)} w.p.->1 while terminal Gibbs path repairs the population, so evidence and PIPs separate; numerics p=18: median log W_r -4 to -12 with PIP error equal to exact posterior | PROOF SKETCH (deterministic core PROVED); family claims rest on W1-EXP Thm 6, O-BGIBBS Prop LH, W4-SHARE M(b) (A-REV3 ERROR); SF none; XF none | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | none (campaign-only); SYNTHESIS row masked-regime meaning of Z-hat and PIPs |
| TH308 | MZ-E1E2; API-MASKZPIP Theorem E1; E1 two-phase sandwich; Corollaries E1a E1b E1c | theorem | On a two-phase frozen path /log W - Psi_t/<=phi_t eta+(1-phi_t)eta'; late switch underestimates by e^{(a+Lambda)(phi_t-phi*)}; island agreement is uninformative | PROVED (candidate, deterministic); not reviewed (no SF, no XF); NOTE name collision: K40 XF-VERIFIED E1/E2 are W1-T03R lemmas | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | S-Z Proposition Z (iii) E1/E2 path-tail clause (K40) with full hypotheses or omitted; K79 |
| TH309 | MZ-E1E2; API-MASKZPIP Theorem E2; E2 miss bound | theorem | E[W 1{no stage-(t-1) particle in A}]<=kappa_t(A)<=[pi0(A^c)/pi0(x_m)]e^{-phi_t D_A}; P(W>(T/eta)[pi0(A^c)/pi0(x_m)]e^{-phi_tau D_A})<=eta+N pi0(A) with tau the arrival stage of A | PROVED (candidate, any kernel/grid/N); not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | S-Z Proposition Z (iii) (K40); FUTURE_WORK FW2 |
| TH310 | API-MASKZPIP Proposition E3; exact pair refresh; E3 | proposition | Exact refresh gives E(W-1)^2=prod(1+chi2_t/N)-1; a pure one-coordinate pair is exactly refreshed by the v3 round so E(W-1)^2<=e^{T/(9N)}-1; pair-dominated perturbation not completed | PROVED in the idealisation (a),(b); PROOF SKETCH for (c); not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | none (feeds CJ218) |
| TH311 | API-MASKZPIP Theorem E4; E4 evidence dichotomy; blind half | theorem | Blind case: log Z-hat_r - log Z <= -phi_{tau_A} D_A + log(T/eta) + log(1/pi0(x_m)) w.p.>=1-eta-N pi0(A); upper tail always O_P(1) by Markov; resolved case O_P(sqrt(T/N)) is conjectural | PARTLY PROVED (blind half PROVED, resolved half CONJECTURE, LH consequence PROOF SKETCH); not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | K40; FUTURE_WORK FW2 |
| TH312 | MZ-P1P2; API-MASKZPIP Theorem P1; P1 RB PIP bias bound | theorem | /E PIP-hat_rj - PIP_j/<=TV(nu-bar_r P^L,pi)<=E f_{r,0}+delta1; after locking (all particles at S0) bias<=delta1 with no L,B,rho-bar term | PROVED (candidate); not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | S-POOL TV error card (K57 P1 part, MZ-P1); FUTURE_WORK FW8 for general accuracy |
| TH313 | MZ-P1P2; API-MASKZPIP Theorem P2; P2 L1 error after delivery | theorem | E[max_j/PIP-hat_rj - PIP_j/ / F_T]<=f_{r,0}+(L+4)rho-bar+u_pi+delta1 and E[max_j/PIP-hat_rj-1{j in S0}/ / F_T]<=f_{r,0}+(L+4)rho-bar+u_pi | PROVED as a composition of locked T23(ii) and T12 (R3); not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | K57 (not carried beyond P1); FUTURE_WORK FW7/FW8 |
| TH314 | MZ-P3; API-MASKZPIP Proposition P3; Corollary P3-prime; top-store evidence and PIPs | proposition | For any exactly scored set T: Z_T/Z=pi(T), /PIP^T_j-PIP_j/<=pi(T^c); if S0 in T then 1-delta1<=Z_T/Z<=1 and /PIP^T_j-PIP_j/<=delta1; P3-prime conditional on T03 and discovery | PROVED (P3 deterministic); P3-prime PROVED as a composition, CONDITIONAL; author-only candidate, not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | M4 Theorem Z_T (K43) |
| TH315 | MZ-C1; API-MASKZPIP Propositions C1-C3; per-fit evidence band | proposition | Z-hat/Z<=Z-hat/Z_T surely (Z-hat<Z_T certifies underestimation); w.p.>=0.95 log Z>=max(log Z_T, log Z-hat - log 20); /PIP-hat_rj-PIP_j/<=/PIP-hat_rj-PIP^T_j/+pi(T^c) | PROVED (deterministic, candidate); not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | M4 (K42) |
| TH316 | OPW2-ThmA; O-PW2 Theorem A; exact variance identity; PW2 variance identity | theorem | Var_c(W_T)=(1/N) sum_s (1-1/N)^{T-1-s}(e_s-1) = (1/N) sum_s E[W_s^2 Var_{mu_s}(h_{s,T})] for any q_t-invariant round kernels, via a Feynman-Kac martingale; PW2 LHS equals V_t-V_{t-1} | PROVED (candidate); SF none; XF VERIFIED (A-REV9) | O-PW2/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | S-Z Proposition Z (ii) (K39); K53, K59 |
| TH317 | OPW2-ThmB; O-PW2 Theorem B; two-sided non-asymptotic bound; PW2-free variance bound | theorem | /N V_T - sum (1-1/N)^{T-1-s} sigma2_{s,T}/<=sum (1-1/N)^{T-1-s} H2_{s,T} sqrt(V_s(1+V_s)); recursion U_t>=V_t; Var(Z-hat/Z)<=U_T/4; closed form V_T<=sigma2_T/N+O(N^{-3/2}) | PROVED (candidate); SF none; XF VERIFIED* (A-REV9; O(N^-3/2) only for fixed inputs/grid or uniform constants) | O-PW2/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | S-Z (K39, K53); K59 (MA-CorV); T25(iv) conclusion without PW2 |
| TH318 | OPW2-ThmB Corollary B2; O-PW2 Corollary B2; PW2 holds with a_t=(S_t-S_{t-1})_+ | corollary | PW2 holds with a_t=(S_t-S_{t-1})_+ and nu_t=(eta_t+eta_{t-1})/N=O(N^-3/2); rate constant is the increment of the asymptotic variance, not chi2_t | PROVED (candidate) modulo author sign-check; XF helper: VERIFIED with scope GAP (fixed input/grid) (A-REV9 MASKED_PW2_CHECK) | O-PW2/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | S-Z / T25(iv); K39 |
| TH319 | OPW2-ThmC; O-PW2 Theorem C; primitive constants | theorem | sigma2_{s,T} and H_{s,T} obey recursions in chi2_t, delta2_t, g-bar_t, L2 mixing defect lambda_t, eps_t; with exact refresh reduces to prod(1+chi2_t/N)-1; vacuous with only locked T09 constants | PROVED (candidate); SF none; XF none (not reviewed by A-REV9) | O-PW2/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | none (campaign-only); related CJ219 |
| TH320 | ADRAFT-ThmA; A-DRAFT Theorem A; fixed-data particle consistency | theorem | At fixed data and successful calibration, as N->infinity all section-2.1 estimators (self-normalised, RB, joint draws) converge in probability and L2 to mu_h for bounded h, Z-hat/Z->1, uniform PIPs; MSE O(1/N) | PROVED (candidate); Astra-on-Astra VERIFIED* (A-REV4), A-REV6 VERIFIED; no Claude check; no CLT upgrade (T16 stays CONJECTURE) | A-DRAFT/REPORT.md; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 493] [pos 494] [pos 563] [pos 616] [pos 677] | M1 Theorem V/H via K47 (ASTRA-ONLY); L-PROPP, S-POOL |
| TH321 | ADRAFT-CorA1; A-DRAFT Corollary A1; finite-N identities for marked RB rewards | corollary | E_c[Z_r mu-hat_r(h)]=Z mu_h and E_c Z_r=Z at fixed boundaries/pre-label positions; E_c[Z-hat mu-bar]-Z mu_h=-(3/4)Cov(Z_1,mu_1); the numerator is unbiased, the self-normalised/RB estimate is not | PROVED from locked T12; Astra-on-Astra VERIFIED* (A-REV4); A-REV6 VERIFIED | A-DRAFT/REPORT.md; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 493] [pos 494] [pos 563] [pos 616] [pos 677] | M1 Theorem V/H (K46,K47,K50); L-PROPP |
| TH322 | ADRAFT-ThmD; ADRAFT-uniPIP; A-DRAFT Theorem D; n-indexed budgets; uniform PIPs without (L+4)rho*->0 | theorem | Under EX-A,EX-S,START,CAL,OUT and (P1),(P1-ex): P(O_n and /mu-hat_n-mu_n/>eps)->0 for bounded h_n, evidence and production PIPs consistent, with E max_j/PIP-hat-1{j in S0}/<=min{1,delta+b_c}+rho-bar+u_pi and no factor L | PROVED (candidate); Astra-on-Astra VERIFIED* (A-REV4); A-REV6 VERIFIED conditionally; no Claude check | A-DRAFT/REPORT.md; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 493] [pos 494] [pos 563] [pos 616] [pos 677] | M1 Theorem V/H via K51 (DRAFT-ONLY, masked h-bound); not a card by itself |
| TH323 | ADRAFT-CorD1; A-DRAFT Corollary D1; generating-value consistency under continuity | corollary | Under Theorem D plus posterior concentration about theta*_n and uniform local continuity of h_n: Pi_n h_n - h_n(theta*_n)->0; supplies replacement text for draft section 13.1 | PROVED, conditional; Astra-on-Astra VERIFIED* (A-REV4); A-REV6 VERIFIED with contraction/continuity qualifications | A-DRAFT/REPORT.md; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 493] [pos 494] [pos 563] [pos 616] [pos 677] | none in paper-1 cards (replacement text for draft 13.1) |
| TH324 | FD-H; F-DRAFT Remark H; general h(theta); NEW_TARGETS H | proposition | Recording h-bar(S)=E[h/S,y] at the T12 positions gives E[Z_r h-hat_r]=Z E_pi[h] by the proof of T12(i); draft 13.1 extends in one line | PROVED (one line); SF none; XF none (same identity as ADRAFT-CorA1 checked by A-REV4) | F-DRAFT/NEW_TARGETS.md; F-DRAFT/CROSSWALK.md | [pos 489] [pos 490] [pos 616] | M1 Theorem V/H via K46 (N1 premise form) |
| TH325 | T26-PropC; ORTH-joint; W2-T26 Proposition C; ORTH compatibility; Prop C | proposition | On XtX=(n-1)I_p, p<=min(n-1,n^A), fixed s0 and nonzero theta: G,R,SE,BM-C,VIS,NL_eta(eta=0),NL_avg(kappa<=1/2) and strict EXP-prime hold jointly (so Theorem B applies); numerics max/R/ 0.11-0.16 | PROOF SKETCH; SF PROOF SKETCH kept (W5-LOCKBOOK); XF GAP (A-REV4, A-REV6); conflict C9 with W4-T38FULL "no open statistical input on ORTH" | W2-T26/PROOF.md; W2-T26/REPORT.md; A-REV4/REVIEW.md; W5-LOCKBOOK/REPORT.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] [pos 919] | none (campaign-only); registry AREV4-PropC-repair (REFEREE, not applied) |
| TH326 | Theorem C1; Thm C1; OCERT-C1; one-sided global certificate; selection-proof | theorem | pi(S) <= e^F(S)/max(Z_T, alpha Zhat) simultaneously for every S, failing only on {Z < alpha Zhat}, output-level probability <= alpha P(A); no lower bound on pi(S-hat) from unbiasedness (C1(c)) | PROVED (candidate); SF VERIFIED* (O-VCERT; last sentence GAP repaired by R1); XF ERROR as literally quantified (A-REV9: C1(a) self-inclusive; Z_T bound VERIFIED; C1(b) with R1 VERIFIED; C1(c) VERIFIED) | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 575] O-CERT launch; [pos 706] result; [pos 729] O-VCERT launch; [pos 763] O-VCERT result; [pos 830] A-REV9 launch; [pos 917] [pos 919] reviews folded into registry | M4 Theorem Z_T K42 (Z >= Z_T deterministic; XF ERROR flag on the card cell); probabilistic part campaign-only |
| TH327 | Theorem C2; Thm C2; OCERT-C2; two-sided band conditional on PW2 | theorem | Under PW2 (Var(Zhat/Z) <= B_T/4) Cantelli gives P(exists S: pi(S) < (1-eps) e^F/Zhat) <= E[1_A B_T/(B_T+4 eps^2)]; conditional global-HPM certificate if (1-eps)e^F(S-hat)/Zhat > 1/2 | PROVED (candidate), CONDITIONAL (registry PROVED-UNDER PW2); SF VERIFIED (O-VCERT); XF VERIFIED as conditional implication (A-REV9) | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 575] O-CERT launch; [pos 706] result; [pos 729] O-VCERT launch; [pos 763] O-VCERT result; [pos 830] A-REV9 launch; [pos 917] [pos 919] reviews folded into registry | none (campaign-only) |
| TH328 | Theorem C3; Thm C3; OCERT-C3; exact relative certificates on fully scored regions | theorem | On any fully scored region R: pi(S-hat/R)=e^F(S-hat)/sum_R e^F and pi(S)/pi(S-hat)=e^(F(S)-F(S-hat)); local gaps g_add,g_del,g_swap, subset class, best-of-scored gap g | PROVED; SF VERIFIED (S-bar = SR logical scored set); XF VERIFIED* (A-REV9: ratios VERIFIED; GAP identifying returned centre with HPM without identity/tie check) | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md; HQ/SR_AUDIT.md | [pos 575] O-CERT launch; [pos 706] result; [pos 729] O-VCERT launch; [pos 763] O-VCERT result; [pos 830] A-REV9 launch; [pos 917] [pos 919] reviews folded into registry | S-CERT context (K64 local_certified semantics); no card for C3 itself |
| TH329 | Theorem C4; Thm C4; OCERT-C4; box certificate; box monotonicity | theorem | For L <= S <= U: F(S) <= Phi(L,U) and sum_box e^F <= e^M(L,U); a branch-and-bound over 2^U certifies S-hat is the exact HPM among all models built from U, with a conditional-mass lower bound and a refutation form | PROVED; SF VERIFIED (O-VCERT: 0 violations in 285,712 boxes on 48 designs; B&B = brute force 80/80); XF VERIFIED* (A-REV9: exact boxes VERIFIED; FP clause GAP) | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 575] O-CERT launch; [pos 706] result; [pos 729] O-VCERT launch; [pos 763] O-VCERT result; [pos 830] A-REV9 launch; [pos 917] [pos 919] reviews folded into registry | S-CERT K73 (region part withdrawn at meeting R3-8); status cell "OCERT-C4: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED* (A-REV9))" |
| TH330 | Corollary C5; Cor C5; OCERT-C5; posterior-miss certificate | corollary | On {S0 in U}: S-hat != S0 and C4(a) imply F(S0) <= F(S-hat), so the miss is a posterior miss; needs strict inequality (or the HPM total order) and /S0/ <= K | PROVED; SF VERIFIED* (O-VCERT tie caveat); XF ERROR on tie-insensitive prose, strict-score event inclusion VERIFIED (A-REV9) | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 575] O-CERT launch; [pos 706] result; [pos 729] O-VCERT launch; [pos 763] O-VCERT result; [pos 830] A-REV9 launch; [pos 917] [pos 919] reviews folded into registry | none (composition carried by N200 TH334) |
| TH331 | Theorem C6; Thm C6; OCERT-C6; per-fit certificate card; Remark C6' (deterministic regime); C6-prime | theorem | The card of L, R, G claims fails with probability <= alpha P(A) <= alpha at every n without conditioning on completion; Remark C6': the whole card is true surely on {Z_T >= alpha Zhat} | PROVED (candidate); SF VERIFIED* (GAP -> VERIFIED after R1, R2); XF GAP original card, repaired exact implication holds with R1, R2 and explicit L/R checks (A-REV9); C6' unreviewed | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 575] O-CERT launch; [pos 706] result; [pos 729] O-VCERT launch; [pos 763] O-VCERT result; [pos 830] A-REV9 launch; [pos 917] [pos 919] reviews folded into registry | none (K73 region-certification clause withdrawn) |
| TH332 | O-VCERT R1; repair R1; outside-store mass; not in T | proposition | Replace "unscored and unreported" by "not in T": pi(Omega minus T) >= 1 - Z_T/(alpha Zhat); optional pi(unscored) >= 1 - [Z_T + (Nbar-/T/)_+ e^F_min]/(alpha Zhat) | Referee repair (O-VCERT); XF VERIFIED repaired outside-store implication (A-REV9); optional unscored bound needs a full-phase score count | O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 729] O-VCERT launch; [pos 763] result; [pos 917] [pos 919] | none (K42/K43 use outside-store form) |
| TH333 | O-VCERT R2; repair R2; floating-point inflation of the G items | proposition | u_alpha^fp(S) = exp(F^fp(S)+eta_F)/max(e^-eta_F Z_T^fp, alpha Zhat^fp); failure probability <= alpha e^eta P(A) + eps under SC(eta_F) and VAL-FP | Referee repair (O-VCERT); XF "correctly supplies" the bound, a conditional validation contract, not a measured guarantee (A-REV9) | O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 729]; [pos 763]; [pos 917] [pos 919] | none (FUTURE_WORK FW16 collects validated arithmetic) |
| TH334 | Theorem N200; N200; finite-n composition theorem; Thm 4 finite-n form (K72) | theorem | P(U or S-hat != S0) = P(U) + P(O, S-hat after S0) + P(O, S0 after S-hat) <= P(U) + Pi(X) + P(O, S0 not scored), Pi(X)=P0(S-dagger != S0 / X); matching lower bound minus P(O, S-dagger not scored); implies T21 C1 term by term | PROVED (elementary, every n); author-only (no SF, no XF); Pi(X) upper bound OPEN | API-N200/PROOF.md; API-N200/REPORT.md; API-N200/results/n200_table.md | [pos 906] launch; [pos 911]; [pos 929]; [pos 978] result; [pos 1009]; [pos 1142]; [pos 1361] author-only flag | M5 Theorem HPM K72 (composition at every n); FUTURE_WORK FW14 (K94), FW26 |
| TH335 | Proposition 2 (API-N200); brackets for Pi(X) | proposition | max_e p_e <= P0(L/X) <= P0(L_2/X) <= ... <= Pi(X) and P0(L/X) <= sum_e p_e (one-move event L, Hamming balls L_d) | PROVED (exact score, no PA); author-only | API-N200/PROOF.md; API-N200/REPORT.md | [pos 906]; [pos 978] | FUTURE_WORK FW14 (K94) |
| TH336 | Proposition 1 (O-SWAP); OSWAP-P1; within-size swap | proposition | Swap j->l beats S0 iff (n/(n+1))(lambda B^2 - A^2) > (lambda-1)(...); at lambda=1 P_swap = Phi(-d_-)Phi(d_+) + Phi(d_-)Phi(-d_+), d_-+ = /delta_j/ sqrt((1-+rho)/2), no size-prior term | PROVED under PA (registry PROVED-UNDER); no SF; XF GAP (A-REV9) | O-SWAP/REPORT.md; A-REV9/REVIEW.md | [pos 577]; [pos 578]; [pos 742] | none (campaign-only) |
| TH337 | Proposition 2 (O-SWAP); OSWAP-P2; superset by one null | proposition | {F~(S0+l) > F~(S0)} = {B_l^2/(E+Omega_0) > tau_l}, P_add(l) = P(chi2_1 (1-lambda/(n+1)) > (lambda-1)(chi2_{n-2-s0}+omega_0)) | PROVED under PA (registry PROVED-UNDER); no SF; XF GAP; displayed identity ERROR if asserted under PA alone (A-REV9) | O-SWAP/REPORT.md; A-REV9/REVIEW.md | [pos 577]; [pos 742] | none (campaign-only) |
| TH338 | Corollary 2.1 (O-SWAP); superset rate p-free and rises as signal falls | corollary | t_add^2 = 2 kappa+ (1+eta)(1+O(kappa+/n)); family-wise superset rate depends on p only through p^-eta / t_add (7.1%/6.6% at c=1, 13.7%/13.6% at c=0.5 for p=500/1000) | PROOF SKETCH (expansion); numbers are exact evaluations of Prop. 2; no review | O-SWAP/REPORT.md | [pos 577]; [pos 742] | none (campaign-only) |
| TH339 | Proposition 3 (O-SWAP); OSWAP-P3; subset: a truth dropped | proposition | P_drop(j) = E[Phi(t-/delta_j/) - Phi(-t-/delta_j/)], t = sqrt((Lambda_j-1)(chi2_{n-1-s0}+omega_j)/(1-Lambda_j/(n+1))) | PROVED under PA (registry PROVED-UNDER); no SF; XF GAP | O-SWAP/REPORT.md; A-REV9/REVIEW.md | [pos 577]; [pos 742] | none (campaign-only) |
| TH340 | Theorem 4 (O-SWAP); OSWAP-T4; first-order bracket | theorem | max_e p_e <= P(L/X) <= P(S0 != S-dagger / X) and P(L/X) <= sum_e p_e | PROVED (exact F, no PA for the inequalities); author only; LOCKABLE_v2 3e no verification | O-SWAP/REPORT.md | [pos 577]; [pos 742] | none directly; reused as TH335 (FW14) |
| TH341 | Proposition 5 (O-SWAP); OSWAP-P5; swap ceiling is information-theoretic | proposition | For any selector (1/2)[P_mu(S-hat != S0) + P_mu'(S-hat != S')] >= Phi(-/delta_j/ sqrt(1-rho^2)/2) (Le Cam two-point bound); HPM swap error ~ Phi(-/delta_j/ sqrt((1-rho)/2)) | PROVED (standard two-point bound); author only; LOCKABLE_v2 3e no verification | O-SWAP/REPORT.md | [pos 577]; [pos 742]; [pos 937] | none (campaign-only; T07 carries the size-prior statement) |
| TH342 | Proposition 6 (O-SWAP); cluster representation; predictor T2 | proposition | B_jl = rho_jl A_j + sqrt(1-rho_jl^2) Z_jl with Z_jl central N(0,sigma^2) independent of A_j; predictor T2 = E_E[prod_l(1-q_l(E)) prod_j(1-P_j(E))] under three approximations | Prop. 6 PROVED (exact, no PA; no registry row, no review); T2 "an approximation, not a bound"; A-REV9 GAP on predicted aggregate rates | O-SWAP/REPORT.md; A-REV9/REVIEW.md | [pos 577]; [pos 578]; [pos 742] | none (campaign-only) |
| TH343 | Theorem T33-S; T33-S; floating-point error bound for one score (Cholesky route) | theorem | Under FP, NOUF, LIB, SMALL and eps_H, eps_A, eps_Q <= 1/2, theta_Q <= 1/2: Cholesky succeeds and /F^(S)-F(S)/ <= eta_F(S) with explicit constants; n=200,K=100 worst case allows eta_Q ~ 4.6e-3 nats, a-posteriori ~1e-9..1e-8, observed 1e-13..1e-11 | PROVED (given H1-H4, FP, NOUF, LIB, SMALL); registry PROVED-UNDER; author's own check only; A-REV9 deferred | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md | [pos 711] launch; [pos 717]; [pos 742]; [pos 748]; [pos 754] | FUTURE_WORK FW16 (K107) as the exact-vs-machine caveat |
| TH344 | Corollary T33-NF; numerical_failure impossible at n=200 | corollary | If eps_H, eps_A, eps_Q <= 1/2, (n+1) r_Q <= 1/2 and n+1 <= 10^7 for all feasible S, every score returns on route chol with q_recomputed=false; numerical_failure impossible at n=200 for every p and y; a-priori up to n=1,286 (K=n/2) | PROVED (author's own check only); A-REV9 does not endorse it without its FP/NOUF/LIB/SMALL domain | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md; A-REV9/REVIEW.md | [pos 711]; [pos 742]; [pos 937] | none |
| TH345 | Proposition T33-H; HPM decisions and ties on a common scored set | proposition | Computed HPM lies in {F >= F(S*) - 2 eta-bar'}; equals S* if the gap exceeds 2 eta-bar'; exact ties decided by rounding unless computed scores are bitwise equal; margin criterion for S0 | PROVED (author's own check only); A-REV9 deferred | W7-SEC/PROOF_T33.md | [pos 711]; [pos 742] | none (K108 perturbation lemma credited to another source) |
| TH346 | Proposition T33-Z; floating-point evidence and VAL-FP | proposition | On path agreement /log Zhat^fp - log Zhat^ex/ <= eta_Z (6e-11..4.5e-9 measured, ~1e-6 rigorous); a-priori epsilon union bound ranges 2e-3 to >1 (vacuous) and must be measured by replay | Deterministic part PROVED; a-priori epsilon part PROVED but vacuous at study budgets; author's check only; A-REV9 deferred | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md | [pos 711]; [pos 742] | FUTURE_WORK FW16 (K107); N16 OPEN |
| TH347 | T32-fp; T32(i) fp-pilot addendum; W7-SEC recount of T32(i) | proposition | Without EX-A the pilot has <= T_e+1 stages (fp-safe bound adds sum_e H_e m = +1,320,960 on 2.676e11 at (200,500)); recount of W5-LOCKBOOK T32(i): 267,610,872,968 at (200,500) matches W5 exactly | Addendum PROVED (author W7-SEC); recount "no error in the count" (same family); XF none (A-REV6 "supported by loop accounting", A-REV9 deferred) | W7-SEC/REPORT.md; W7-SEC/NOTES.md; W5-LOCKBOOK/REPORT.md | [pos 711] launch; [pos 742]; [pos 748]; [pos 754] | M8 Proposition D: "T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none)", SAME-FAMILY-ONLY |
| TH348 | Theorem WS1; WS1; OWS-WS1; exponential-family identities for the bridge | theorem | 1+chi2(q_v//q_u)=exp{Lambda(w)-2Lambda(v)+Lambda(u)}=q_v(S)^2/(q_u(S)q_w(S)) for every S; Renyi version, set bounds, variance/TV/log-concavity | PROVED (author; SF none; XF none; FLAG AUTHOR-ONLY) | O-WSTAB/PROOF.md | [pos 492] [pos 659] [pos 666] [pos 748] | feeds M2 Theorem WS (K102; K104 as used; (b2) cumulant identity) |
| TH349 | Theorem WS2; WS2; OWS-WS2; one importance step | theorem | ESS_inf=1/(1+chi2)=q_u(S)q_w(S)/q_v(S)^2; PW2 holds at the first stage of a final island with equality (Var(Zhat/Z)=chi2/(4N) when T=1) | PROVED (author; SF none; XF none) | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds M2 (b3) first-stage identity (same content, not cited by name) |
| TH350 | Theorem WS3; WS3; OWS-WS3; FD-W1; F-DRAFT Lemma W1; Lemma W1; BO exact structure of d | theorem | Under exact block orthogonality d=d_sigma>=0 is pure noise-variance sharing, zero iff at most one block active; with known sigma^2 d=0 and pi0=pi | PROVED; XF VERIFIED (A-REV4 F-DRAFT W1; A-REV6 exact sample-BO identity); CHK_INHERITED VERIFIED (PC1, cross-family, line by line) | O-WSTAB/PROOF.md; F-DRAFT/NEW_TARGETS.md | [pos 489] [pos 616] [pos 492] [pos 748] [pos 919] | feeds M2 Theorem WS (a3) (K102, K10, K11); M3 Theorem START K10 |
| TH351 | Theorem WS4; WS4; OWS-WS4; perturbation in standardised cross-block Gram | theorem | /d-d_sigma/<=eta_S=nu*eps*xbar/(1-eps-xbar)+F_S/(4(1-eps)); transfer bound on chi2 and TV; perturbative scale eps=o(1/n) only | PROVED (author; SF none); CHK_INHERITED VERIFIED (PC1, cross-family, line by line) | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds M2 (a3), (b2) four-normaliser transfer; K11 |
| TH352 | Proposition WS5.2; WS5.2; OWS-WS52; leakage formulas | proposition | Explicit leakage formulas delta_{T,l}, null comparisons, block-completing additions, visibility, cross-block bounds | PROVED (author; SF none; XF none) | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds: none directly (M2 card removed m-form of (S),(F) to the leakage corollary R3-5) |
| TH353 | Theorem WS5.3 (F); WS5.3(F); OWS-WS53F; WS5.3 (N); OWS-WS53N; weak leakage implies favourable start | theorem | CBL(eta), EBM => VIS, NL_eta, so 1-pi0(S0)=O_P(2^B sqrt(log n) n^-kappa); necessity form (N) | PROVED-UNDER (reduction PROVED; conclusion composes with locked T22(iii), inherits EXP-prime candidate status; SF none; XF none) | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds M2 leakage corollary (R3-5); none direct |
| TH354 | Theorem WS5.3 (M); WS5.3(M); OWS-WS53M; masking needs order-one cross-block cancellation | theorem | CL(L) forces /theta*_l+alpha_{b,l}/<=L sigma*/(phi0 sqrt(n-1)); no T27-type masking under BO | PROVED (deterministic; SF none; XF none) | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds: none directly (supports M3 Theorem START narrative, K17) |
| TH355 | Theorem WS6 (a)-(c); OWS-WS6abc | theorem | 1+chi2=pi(S)^2/(pi0(S)q2(S)); stable weights from start sees truth plus tilt control; KL needs less tilt control (theta-form) | PROVED (deterministic; SF none; XF none) | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds M2 (b) via WS6(b); TH358(b) |
| TH356 | Theorem WS6(d); OWS-WS6d; noise-chasing obstruction; Proposition ONE-SHOT; zero-dependence obstruction | theorem | Under ORTH and zero cross-block correlation chi2(pi//pi0)->inf (ESS fraction ->0) while TV->0, e.g. p=n-1, R2>1/2 | PROVED (author; SF none; XF none); CHK_INHERITED VERIFIED WITH AMENDMENT (bounded-block scope for TV) | O-WSTAB/PROOF.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md | [pos 492] [pos 748] [pos 616] | feeds M2 (c1) Proposition ONE-SHOT (K102) |
| TH357 | Theorem WS7; OWS-WS7; reweighting cannot create the truth; masked weights | theorem | ESS_inf<=pi0(S0)/pi(S0)^2; KL>=pi(S0)log(1/pi0(S0))-log2; population holds S0 w.p. <=N pi0(S0); restricted-ESS stages T>=log2[(l0+c)/(lT+c)] | PROVED (author; SF none; XF none); CHK_INHERITED VERIFIED WITH AMENDMENT | O-WSTAB/PROOF.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md | [pos 492] [pos 748] | feeds M2 (c2); M6 K105 (KL lower bound, PROOF SKETCH); M7 (d) restricted-ESS log2(9.5 l0); K17 |
| TH358 | Proposition WS8 (a)-(c); OWS-WS8abc; bridge and PW2 under IID | proposition | T=1: Var(Zhat/Z)=chi2/(4N); idealised product bound under IID; exact telescoping of sum log(1+chi2) | PROVED ((b) under IID idealisation; SF none; XF none); (d) OPEN see CJ262 | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds: none (campaign-only; PW2 resolved by O-PW2) |
| TH359 | Proposition W0; Prop W0; FD-W0; three faces of pi/pi0 | proposition | 1+chi2=E e^{2d}/(E e^d)^2=1/rho_Omega(0,1); chi2, sup ratio M and pi0(S0) are three norms; independence-move Doeblin rate (1-1/M)^t; iid discovery | PROVED (F-DRAFT FD-W0 and O-WSTAB self-contained re-proof; SF none; XF none) | O-WSTAB/REPORT.md; F-DRAFT/NEW_TARGETS.md | [pos 616] [pos 748] | feeds M6 / S-IDENT (K19, K103, K104) |
| TH360 | Proposition L; Prop L; ell-form of T13 | proposition | log(1+chi2(q_v//q_u))=ell(u)+ell(2v-u)-2ell(v) with ell=-log q_phi(S0) convex; sandwich ell(w)-2ell*<=log(1+chi2)<=ell(w)+ell* | PROVED (author); SF verified (CHECK_SEP_W); XF no separate row | O-WSTAB/REPORT.md | [pos 748] | feeds TH361, TH363; M7 Lemma RS (same identity) |
| TH361 | Proposition G; Prop G; ideal-grid sandwich | proposition | Ideal ESS-0.9 grid stage count between max{1,ceil(log2(1+1/g+))} and max{1,ceil(log2(1+1/g-))} | PROVED (author); SF verified (CHECK_SEP_W, F4 exposition); XF no separate row | O-WSTAB/REPORT.md | [pos 748] | feeds TH363; overlaps O-STAGES Theorem G/F |
| TH362 | Theorem W (ORTH); Theorem WS; Theorem W weight stability; H-ORTH; W(a)-(g); O-WSTAB Theorem W | theorem | Under ORTH, fixed s0,theta*, p log p=o(n): both ends concentrate, KL,TV->0, chi2 = p^{r+-eps}/sqrt(n) if p^r sqrt(log p)/sqrt(n)->0, log(1+chi2)>=e^{(L_n-C)/r} and <=C e^{L_n/r}(log p)^{5(1+r)/(2r)} on divergent side; threshold 2Ar<1 | PROVED (author); SF verified except W(d) upper half restricted (CHECK_SEP_W: F1 gap, F3 constant; SEP-prime and W(g) not reviewed); XF A-REV9 VERIFIED under H-ORTH exactly as stated for W(a)-(f) including the stronger upper-side premise; W(g) not covered | O-WSTAB/REPORT.md; O-WSTAB/review/CHECK_SEP_W.md; A-REV9/REVIEW.md | [pos 489] [pos 491] [pos 659] [pos 666] [pos 748] [pos 1441] [pos 1449] | feeds: none beyond H-ORTH (M2 card: not used beyond H-ORTH); replaces F-DRAFT Theorem W for chi2->inf under ORTH |
| TH363 | Theorem W prime; Theorem W′; W′ ideal grid; Cor. WS-W′ | theorem | Under H-ORTH the ideal ESS-0.9 grid has T=1 if 2Ar<1 and T=2 if 2Ar>1; always <=2 w.p.->1 | PROVED (author); SF verified (CHECK_SEP_W); XF A-REV9 VERIFIED ideal full-space grid under H-ORTH, production-grid transfer GAP; equality 2Ar=1 unresolved | O-WSTAB/REPORT.md; O-WSTAB/review/CHECK_SEP_W.md; A-REV9/REVIEW.md | [pos 748] [pos 616] | feeds: none (campaign-only); K29 DRAFT-ONLY, FUTURE_WORK FW23 |
| TH364 | O-STAGES Theorem G; STG-G; greedy optimality; shortest valid grid | theorem | Greedy ESS grid has the fewest intervals among valid grids; target-constrained construction is optimal among refinements of pilot targets; max(T*_V,T_P)<=T_grid<=T*_V+T_P | PROVED (author; SF none; XF none; FLAG AUTHOR-ONLY); known: Stefankovic-Vempala-Vigoda 2009 | O-STAGES/REPORT.md | [pos 728] [pos 733] [pos 748] [pos 1009] | feeds M7 Theorem STG (a) (K26); M2 (b6) |
| TH365 | O-STAGES Theorem L; STG-L; path length | theorem | sqrt(c) T*(c) -> L=int sd_{q_t}(d)dt as c->0 with kappa-regularity bounds; worst case T*<=ceil(1.54 D) | PROVED (author; SF none; XF none); known: Syed et al 2024 Thm 3, Gelman-Meng 1998 | O-STAGES/REPORT.md | [pos 733] [pos 748] | feeds M7 (e) cited; K28 |
| TH366 | O-STAGES Theorem F; STG-F; favourable sandwich | theorem | N(w+)<=T*<=N(w-) through q_w(S0), w in [1,2], when Delta<=0.0513 | PROVED (author; SF none; XF none) | O-STAGES/REPORT.md | [pos 733] [pos 748] | feeds: cited only (K29 DRAFT-ONLY; FUTURE_WORK FW23) |
| TH367 | O-STAGES Corollary W prime; Cor W′ (BO favourable); STG-Wp | corollary | Given layer law (LL): /T*-ceil(log2(1+1/g_n))/<=1 and T*<=ceil(log2(1+2AR2))+1=O(1) for p<=n^A | PROVED-UNDER (LL; PROOF SKETCH hypothesis); registry conflict C22 (LL may need restating for 2Ar>1); SF none; XF none | O-STAGES/REPORT.md | [pos 733] [pos 748] | feeds: none (K29 DRAFT-ONLY, FUTURE_WORK FW23) |
| TH368 | O-STAGES Theorem M; STG-M; masked two-state crossing; T*=log2 A0+O(1) | theorem | Two-state crossing with start masking depth A0 costs log2(A0-1.48)-0.95<=T*<=log2(A0-2.2)+11 ESS-0.9 stages, independent of A1 | PROVED (author); XF VERIFIED* (A-REV9: logarithmic order VERIFIED for ideal two-state exact-frontier grid; explicit decimal constants GAP); SF none | O-STAGES/REPORT.md; A-REV9/REVIEW.md | [pos 733] [pos 748] [pos 1028] [pos 1038] [pos 1044] | feeds M7 Theorem STG (d) (K30); FUTURE_WORK FW6 for as-coded count |
| TH369 | O-STAGES Corollary W‴; Cor W‴ (corrected W″); STG-W3p | corollary | Under PAIR, T*=log2 A0+O(1) for proxy-split (log2 n) and LH c=1 (log2(c log p+(c/2)log n)) masking | PROOF SKETCH for families; PROVED given PAIR (author); SF none; XF none | O-STAGES/REPORT.md | [pos 733] [pos 748] | feeds M7 (d) labelled ideal; K30 |
| TH370 | API-T26BUD Theorem G; T26BUD-G; grid stage count | theorem | On any successful build_grid with S0 in V: T=N^pil+k^bis, k^bis<=ceil(log2(1/eta_n)); N^pil<=T<=N^pil+ceil(log2(1/eta_n)) | PROVED, deterministic (candidate; SF none; XF none; AUTHOR-ONLY) | API-T26BUD/PROOF.md; API-T26BUD/REPORT.md | [pos 906] [pos 911] [pos 975] [pos 978] | feeds M7 Theorem STG (K26); FUTURE_WORK FW6 (K31) |
| TH371 | API-T26BUD Theorem 1; one-stage regime | theorem | If 1-pi0(S0), 1-pi(S0), chi2(pi//pi0)->0 and HPM(pi)=S0 w.p.->1 then T_n=1 w.p.->1; (P1) of Theorem 6 holds with no premise on the run | PROVED given its inputs (candidate; SF none; XF none) | API-T26BUD/PROOF.md; API-T26BUD/REPORT.md | [pos 906] [pos 975] [pos 978] | feeds Thm 6 (W2-T26 Theorem A) premise P1; no final card |
| TH372 | API-T26BUD Corollary 1; realised budget | corollary | T_n<=min{T_e,N^pil+ceil(log2(1/eta_n))}<=min{T_e,1+ceil(Dbar/a)+ceil(log2(1/eta_n))}; conditions for (P1) | PROVED (candidate; SF none; XF none) | API-T26BUD/PROOF.md | [pos 906] [pos 978] | feeds Thm 6 premise (P1); M7 (c) similar count |
| TH373 | API-T26BUD Rule CAP; Corollary 2 | corollary | Under a cap T^cap_n with T^cap_n Delta_n->0 (e.g. ceil(log2 n)), (P1) holds deterministically with no premise on the run | PROVED (candidate; SF none; XF none); method change not adopted | API-T26BUD/PROOF.md | [pos 906] [pos 978] | feeds: none |
| TH374 | API-T26BUD Proposition O; ORTH grid inputs | proposition | On ORTH-F, R(1+eta)=O_P(n^{-1/2+A eta(1-lambda*)} polylog)->0 for A eta(1-lambda*)<1/2, hence T_n=1 if A(1-lambda*)<1/2 | PROOF SKETCH (author; steps unverified); consistent with TH362/TH363; SF none; XF none | API-T26BUD/PROOF.md | [pos 906] [pos 975] | feeds: none |
| TH375 | F-DRAFT Proposition P; FD-P; partition as a random variable | proposition | Validity is partition-free; mixture start over partitions is exactly samplable with density and keeps the bridge valid; stochastic scheduling = frozen calibration | PROVED (author; SF none; XF none); (ii) is a method extension | F-DRAFT/NEW_TARGETS.md | [pos 616] | feeds: none (campaign-only); mixture start developed by O-MIX (theme 3) |
| TH376 | F-DRAFT Remark H; FD-H; general h(theta) | proposition | T12 product identity extends to general bounded h(S,beta_S,sigma2) through conjugate conditionals | PROVED (one line; SF none; XF none) | F-DRAFT/NEW_TARGETS.md | [pos 616] | feeds: none |
| TH377 | F-DRAFT W″ two-state part; FD-W″-two; path length <= pi | proposition | Two-state bridge: int sd_{q_phi}(d)dphi = int da/sqrt(a(1-a)) <= pi independent of D | PROVED (calculus; SF none; XF none); the inference 3pi stages is false (RF255, RF258) | F-DRAFT/NEW_TARGETS.md | [pos 616] | feeds: none (superseded by TH365, TH368); K28 cited |
| TH378 | A-REV6 W2-R; W2-R(a); W2-R(b); REV6-cands(A6) | proposition | Exact regularised identity d(S+l)-d(S)=nu[log(1-h_{T,l})-log(1-h_{S,l})] and ORTH uniform additive expansion max/d(S0+l)-d(S0)-kappa Z^2/2/=O_P(log n/sqrt n) | REFEREE (Astra-authored); GAP pending Claude verification | A-REV6/WEIGHTS.md | [pos 807] [pos 919] | feeds: none |
| TH379 | A-REV4 exact KL bound; AREV4-KLexact | proposition | KL(pi//pi0)<=-log pi0(S0)+sum_{S!=S0} pi(S)[d(S)-d(S0)] | REFEREE (referee-authored; exact two-line argument) | A-REV4/DRAFTS_CHECK.md; A-REV4/REVIEW.md | [pos 677] [pos 919] | feeds: none |
| TH380 | SEP(A); SEP-A; Theorem SEP (A); iid start discovery | theorem | Q iid pi0 draws score S0 w.p. -> 0 or 1 as Q/Q* -> 0 or inf, sharp Q*=p^c n^{c/2} on LH exact Gram; polynomial budget n^alpha fails iff alpha<c(a+1/2) (p~n^a) | PROVED (author W7-SEP, candidate; SF: none; XF: VERIFIED (A-REV9) as an implication from imported start-mass and concentration premises) | W7-SEP/PROOF.md; W7-SEP/REPORT.md; A-REV9/REVIEW.md; T38-RECORD/REGISTRY_v2.md (row SEP-A) | [pos 711] [pos 717] [pos 763] [pos 843] [pos 915] [pos 925] | M6 Theorem SEP + Lemma KL (K19; card states threshold p^2 n); cited as lower bound used by M2 |
| TH381 | SEP(A) on LH-iid; SEP-A-iid | theorem | Same threshold on the p>>n LH-iid family, through W3-PXN P1,P4 | PROVED-UNDER (W3-PXN P1,P4; SF: none; XF: none for SEP-A-iid; P1,P4 VERIFIED by A-REV3) | W7-SEP/PROOF.md; W7-SEP/REPORT.md; T38-RECORD/REGISTRY_v2.md (row SEP-A-iid) | [pos 763] | none (not imported into M6; AUTHOR-ONLY) |
| TH382 | SEP(B); SEP-B; Theorem SEP (B); one-shot importance correction; B1-B3 | theorem | 1+chi2(pi//pi0) >= pi(S0)^2/pi0(S0) = Q* e^{-Mstat}(1+o_P(1)); KL lower bound; relative variance (1/pi0(S0)-1)/Q; estimator of pi(S0) equals 0 w.p. -> 1 below Q* | PROVED (author W7-SEP, candidate; SF: none; XF: VERIFIED (A-REV9) as implications from imported premises) | W7-SEP/PROOF.md; W7-SEP/REPORT.md; A-REV9/REVIEW.md | [pos 763] [pos 843] [pos 915] [pos 925] | M6 Theorem SEP + Lemma KL (K106, K105) |
| TH383 | SEP(B) PIP version; PROOF section 3 Remark 3 | proposition | With Q=o(p sqrt n) no draw contains masked hub b_i w.p. -> 1 so IS estimates of PIP_{b_i} are 0 while PIP >= pi(S0) -> 1 | PROOF SKETCH (author; second-term bookkeeping not written); A-REV9: SEP verdicts do not prove a PIP statement | W7-SEP/PROOF.md | [pos 763] | none (campaign-only) |
| TH384 | SEP(C); SEP-C; start + one greedy search | theorem | On LH w.p. -> 1 production local search scores and certifies S0 from every C subset of R; LS0 and one iid draw + search score S0 at cost O(p^2 log n); clause (a) with local search is false on LH | PROVED (author, candidate; uses Lemma M same-family VERIFIED only; SF: none; XF: none) | W7-SEP/PROOF.md; W7-SEP/REPORT.md | [pos 717] [pos 763] [pos 796] | none (campaign-only); M6 scope boundary cites SEP-taska |
| TH385 | SEP(D); v3 succeeds (citation) | proposition | Citation: v3 with LS0 via T38(b1-LH); without LS0 c=1 via D2 and fixed c via BG1; cost T32(i)+LS0 term | citation: PROVED-UNDER (T38 b1-LH, unreviewed at W7-SEP date) / PROOF SKETCH (D2 NB step; BG1); stale (cites BG1 not BG3; T32(i) listed CONJECTURE) | W7-SEP/PROOF.md; T38-RECORD/REGISTRY_v2.md (conflicts C18-C20) | [pos 763] | none (citation) |
| TH386 | SEP(E); SEP-E; budget exponents | theorem | p~n^a: iid/IS exponent c(a+1/2) sharp; LS0 or draw+search <=2a; v3 with LS0 <= a+max(1,a); iid vs v3 separated iff c>=2; no super-polynomial gap in R1 | PROVED-UNDER (registry; v3 row conditional on T32(i) listed as CONJECTURE, stale; SF: none; XF: none); registry CONFLICT C19 | W7-SEP/PROOF.md; W7-SEP/REPORT.md; T38-RECORD/REGISTRY_v2.md (row SEP-E) | [pos 763] | none (broader exponent claims not imported into M6) |
| TH387 | Prop BASIN; Proposition BASIN; SEP-BASIN; scoring basin | proposition | Search from C scores S0 iff C in basin B_l; LS0 scores S0 iff S~0 in B_l; Q draws + search succeeds w.p. 1{S~0 in B_l} or [1-(1-pi0(B_l))^Q] | PROVED (deterministic; author candidate; SF: none; XF: none) | W7-SEP/PROOF.md; W7-SEP/REPORT.md | [pos 763] | none (campaign-only) |
| TH388 | Prop GU; Proposition GU; greedy universality; SEP-GU | proposition | Exact Gram, isolated relevant set R, SE on R, fixed signals: production local search from every C subset of R reaches, scores and certifies S0 within tau_GU moves w.p. -> 1; no PGD needed | PROVED (candidate; SF: none; XF: VERIFIED* (A-REV7) as greedy best-neighbour theorem, GAP as standalone no-LS0 growing-p theorem; A-REV9: GAP in that review, Lemma M not re-audited); registry CONFLICT C25 | W7-SEP/PROOF.md; W7-SEP/REPORT.md; A-REV7/REVIEW.md; A-REV9/REVIEW.md | [pos 763] [pos 796] [pos 807] [pos 919] | none (campaign-only; cited in T38 v3 Remark 6 and E-SPINE) |
| TH389 | Cor GU-LH; Corollary GU-LH; SEP-CorGULH | corollary | On LH exact Gram GU hypotheses hold with R = union of non-null groups; every C subset of R in scoring basin; LS0 and one draw + search score S0 w.p. -> 1; COUNTEREXAMPLE to task clause (a) | PROVED (candidate; SF: none; XF: VERIFIED* (A-REV7) as greedy repair on LH with LS0) | W7-SEP/PROOF.md; W7-SEP/REPORT.md; A-REV7/REVIEW.md | [pos 763] [pos 796] [pos 919] | none (consistent with M5 b1-LH search step; re-proves T38(b1-LH) search step) |
| TH390 | GU-iid; GU on LH-iid; SEP-GUiid | proposition | Random-design (p>>n) version of GU with extra union bound over nulls' sample correlations | PROOF SKETCH (author; not written line by line); XF: none | W7-SEP/PROOF.md | [pos 763] | none |
| TH391 | ADRAFT-v3exact; actual small-p v3 on Prop M family | proposition | At p=2, n>=4 v3 takes its exact branch so reported PIPs, evidence and HPM are full-posterior quantities; proxy PIP and joint inclusion -> 0, HPM/MPM -> {1} | PROVED (author A-DRAFT = Astra; no independent campaign verification; premises: exact scores, output availability) | A-DRAFT/REPORT.md | [pos 563] [pos 613] [pos 616] | none (campaign-only) |
| TH392 | ADRAFT-SMCcomp; forced SMC component on Prop M family | proposition | Forced SMC run converges to the full posterior as N -> infinity for each n; T26 cannot be cited for production-budget claim (Delta_n -> 1); production-budget forced-SMC claim OPEN | PROVED (author A-DRAFT = Astra; relies on ADRAFT-ThmA authored and checked by Astra only) | A-DRAFT/REPORT.md | [pos 616] [pos 1238] | none |
| TH393 | NM-R; A-REV6 four-state replacement of F-DRAFT NM | proposition | p=2 fixed-r two-column family: local singleton inclusions -> 1, naive union {j,l}, pi0({j,l}) -> 1, pi({j}) -> 1, log pi0({j}) = -n c_l + O_P(sqrt n + log n), TV -> 1, liminf (1/n) log[1+chi2] >= c_l | Astra-authored candidate; A-REV6: GAP pending Claude verification (original A-REV4 verdict ERROR on F-DRAFT NM preserved) | A-REV6/WEIGHTS.md; A-REV6/REVIEW.md | [pos 807] [pos 919] | none (naive merge dropped as K98) |
| TH394 | Proposition W; Prop W; MA-PropW; V2 (THM-SYNTH); worker equivalence of the final run; concurrent islands bitwise | proposition | Final islands run as concurrent workers (own ScoreCache and Ledger, stream sigma_r = 9+r), merged by Lemma S before the final local search, reproduce the serial run bitwise: Zhat_r, PIP_r, ESS, phi, increments, move counts, terminal table, merged HPM and stores (top 40p+1 by F, top 20p by log gamma0, top 20p by log gamma1), local-search path, pooled Zhat, PIPs, flags E1-E3 and low_empirical_ESS; not equal: cache and score counters, time stamps | PROVED (code reading; executed check in REPORT §6) [PROOFS.md heading]; candidate, not reviewed, author-only (MEET-THM IDX 92); executed bitwise by the author on the smoke problem and design p0500_S1_r001 only, then p0500_S4_r001 (pos 1175) and p0500_S5_r002 (pos 1241) by HQ re-run = 3/3 (MEET-v31 evidence/2026-11-03_concurrency_runs.md); source CONFLICT 1/1 vs 3/3 recorded in MEET-THM REGISTRY_INDEX §5.B B1; no cross-family check of the code reading | METH-AUDIT/PROOFS.md; METH-AUDIT/REPORT.md; MEET-v31/evidence/2026-11-03_concurrency_runs.md; THM-SYNTH/THEOREM_LIST.md (V2); MEET-v31/MINUTES.md (decision 4) | [pos 1068] [pos 1085] [pos 1103] [pos 1107] [pos 1175] [pos 1241] [pos 1276] | S-OUT (K83; K63, K86); MEET-v31 METHOD_v3.1_FINAL parallel layer (a); MEET-THM THEOREM_LIST_FINAL Prop D dependency (K83) |
| TH395 | Proposition W-cal; Prop W-cal; MA-Wcal; worker equivalence of the calibration diagnostic islands | proposition | The 4 diagnostic islands of cpp_cal_diag run as persistent workers (own stream state across iterations, own cache and ledger), stores and HPM merged into the calibration ledger before the local search and before V is built: island outputs, V, grid, local search, triggers E1-E3, grid_unconverged, escalation decision and the exported inherited set are equal to the serial calibration; only score counters differ | PROVED (code reading only; not executed) [PROOFS.md heading]; author-only; still not executed at MEET-v31 close (METHOD_v3.1_FINAL: "(b) has not been executed yet") | METH-AUDIT/PROOFS.md; METH-AUDIT/REPORT.md §8.1; MEET-v31/METHOD_v3.1_FINAL.md | [pos 1068] [pos 1107] [pos 1276] | S-OUT (K83) |
| TH396 | Corollary W-R; Cor W-R; MA-CorWR; stacking R prime > 4 | corollary | Stacking R prime > 4 final islands (islands 1-4 on streams 10-13, island r > 4 on a stream disjoint from 0-13, same N_e and calibration) leaves islands 1-4 bitwise those of the R = 4 run; the scored set before the final local search contains that of the R = 4 run, so the pre-local-search HPM is >= the R = 4 one; flags on islands 1-4 identical to v3; caveat: post-search HPM not necessarily >= R = 4 post-search HPM unless an extra local search is run from the R = 4 pre-search HPM | PROVED by Proposition W(a, b) and the definition of the HPM [PROOFS.md]; PC1 claim 6 (Claude Opus 5.5, Claude Work, read-only proof check for the MEET-v31 chair, same-family): Cor W-R with its caveat PROVED, amendment: E3 and local_certified on islands 1-4 match only if evaluated on the search from c4; monotonicity without the extra search FALSE (RF272, CE220) | METH-AUDIT/PROOFS.md; MEET-v31/evidence/2026-11-03_PC1_proof_check.md (Claim 6) | [pos 1107] [pos 1242] | S-OUT (K84); MEET-v31 METHOD_v3.1_FINAL item 5 (stacking R prime = 4k at N_e with extra local search from c4) |
| TH397 | Proposition P; Prop P; MA-PropP; V3 (THM-SYNTH); pooling as R grows at fixed N; Zhat-weighted PIP; R fixed in advance | proposition | Islands conditionally iid given the calibration: (i) equal-weight PIP converges a.s. to E[PIPhat_1j / C], keeping the single-island bias b_j(N); (ii) Zhat-weighted PIP is consistent as R -> infinity (SLLN); (iii) P(max_j /PIPzw_j - 1{j in S0}/ > t / C) <= exp{-R(1-s)^2/(2E[W_1^2/C])} + eps/(s t) with eps = E[W_r e_r / C] <= delta_1 + rho_bar + u_pi by F-MASKPIP M1; (iv) E[Zhat PIPeq_j / C] - Z PIP_j = -(1-1/R) Cov(Zhat_1, PIPhat_1j / C); (v) pooled Zhat conditionally unbiased for R fixed before final randomness, 0.05 Zhat 95% lower bound by Markov, adaptive R can break unbiasedness | PROVED (elementary) [PROOFS.md heading]; author-only (MEET-THM IDX 70, FLAG AUTHOR-ONLY); input M1 XF VERIFIED (A-REV9); (i)-(ii) known (Verge et al. 2015; Whiteley-Lee-Heine 2016 s5.1; Dai et al. 2022 (4.8)) per LIT-PAR/THM-SYNTH; PC1 consulted only its quoted statement; practical scope caveat: E[W^2] can be exponentially large in the masked regime | METH-AUDIT/PROOFS.md; THM-SYNTH/THEOREM_LIST.md (V3); LIT-PAR/REPORT.md | [pos 1107] [pos 1169] [pos 1177] | M1 Theorem V/H (K48, K49, K50, K85); S-POOL (K49, K50); L-PROPP (Prop P(iii), Maurer-type limit lemmas) |
| TH398 | Corollary V; Cor V; MA-CorV; D4 (THM-SYNTH); same total particles, R islands; split neutrality | corollary | From O-PW2 Theorem A: with R islands of N_r = N/R particles the pooled variance is Var(W)/R; to leading order N Var(Zhat_pooled/Z) = Sum_s (1-R/N)^{T-1-s} sigma^2_{s,T} + O((R/N)^{1/2})(...); the leading constant does not increase with R, the remainder grows as N_r shrinks; in the exact-refresh idealisation Var(W) = Prod_t (1+chi^2_t/N_r) - 1 so R N_r fixed is neutral while Sum chi^2_t << N_r | PROOF SKETCH [PROOFS.md heading]; "Crux not verified: the stage quantities V_s and H_{s,T} of O-PW2 Theorem B are not re-derived"; DELIV under a split OPEN; tiered v2 by THM-SYNTH (D4) | METH-AUDIT/PROOFS.md; THM-SYNTH/THEOREM_LIST.md (D4); MEET-THM/FUTURE_WORK.md (FW9) | [pos 1107] [pos 1177] | FUTURE_WORK FW9 (K59); S-Z (K53 context); S-POOL |
| TH399 | Proposition D; Prop D; MA-PropD; D1 (THM-SYNTH Theorem D precursor); depth with particle-parallel islands; work/depth/width | proposition | Critical path in score evaluations D = D_setup + Sum_{tiers e} [(T_pil+L+4) + Sum_{i=1}^{I_e} (T^(i)+L+4)] m + (T+L+4) m + (number of local searches)(l+1) ceil(scan/width) + O((T_pil + Sum_i T^(i) + T) log N), with m = p+B+2, one worker per particle per island; D does not depend on N, H or R; D = O(m l T_e) = O(p log^3(n+p)) worst case on success; work W = O(N m (l+2) T_e) matching the A-REV6 candidate cost bound O(max(n,p) p log^3(n+p) + p^2 log^2(n+p)) (V19) when N proportional to max(n,p) | PROVED (counting, given the code's structure) [PROOFS.md heading]; author-only; the clause "D does not depend on N, H or R" (particle-parallel width R N) was STRUCK for v3.1 by MEET-v31 decision 6 (island-level depth only; "free of N, H, R" removed; C6 per-particle streams = declared v3.2 path) -> RF271; final M8 restated at island level, status "MA-PropD PROVED (counting, given the code's structure) AUTHOR-ONLY" | METH-AUDIT/PROOFS.md; METH-AUDIT/REPORT.md §2; LIT-PAR/REPORT.md §3.3; THM-SYNTH/THEOREM_LIST.md (D1); MEET-v31/MINUTES.md (decision 6); MEET-THM/THEOREM_LIST_FINAL.md (Card Prop D) | [pos 1038] [pos 1072] [pos 1107] [pos 1177] | M8 Proposition D (K87, K88, K89, K06, K64; K90 remark) |
| TH400 | METH-AUDIT theorem robustness under parallel execution; METH-AUDIT s3 table; hypotheses-that-change list | proposition | Registry-level reading: with "4 islands" read as R islands fixed before final randomness, no registry result breaks under stacking (i-a), concurrency (ii), shared calibration (iii) or Zhat-weighted pooling (iv); six hypotheses change (R declared in advance; Prop 2(c) factor 3/4 -> 1-1/R; VAL-FP epsilon scales with total work; DELIV inside an island under a split OPEN; shortened calibration touches T38(b1 prime), Theorem G and (0_H); particle-level parallelism restates IND-T over (island, stage, particle) triples) | confidence card: medium-high ("registry-level reading of T26 Theorem A and T38 parts; not re-proved"); bookkeeping, author-only | METH-AUDIT/REPORT.md §3, §10 | [pos 1107] | none as a card (informs MEET-v31 METHOD_v3.1_FINAL parallel layer and C9 rejection) |
| TH401 | Proposition OB; Prop OB; LIT-MCMC Prop OB; overfitted-side bottleneck for the paper prior | proposition | For the paper target on M(s) (s0 < s <= K), gamma_e = S0 + {e}: (i) varpi(S0)/varpi(gamma_e) = w(k-1)/w(k) = (2p-k)/k; (ii) pi(S0)/pi(gamma_e) = [(2p-k)/k] sqrt(n+1) exp(-T_e/2)(1+o_P(1)); (iii) if max_e T_e >= (2-eps) log p w.p. -> 1 then R <= C p^{eps/2} sqrt(n)/s0 and R/M <= C p^{eps/2} sqrt(n)/(s0 (p-s)) -> 0 when p^{1-eps/2} >> sqrt(n); hence R > M of Chang-Zhou Thm 1/4, Zhou-Smith Assumption 1 and ZYVR c0 = 2 cannot hold for the paper prior when p >> sqrt(n) | (i) PROVED; (ii)-(iii) PROOF SKETCH [LIT-MCMC REPORT §2.2]; "the step the best neighbour of gamma_e* is S0 is used only as an upper bound ... not verified"; evidence: ob_check 12/12 (CE215), rz_lh (CE216); author-only | LIT-MCMC/REPORT.md §2.2, §3.1; LIT-MCMC/results/ob_check.md; LIT-MCMC/results/rz_lh.md | [pos 983] [pos 1009] | FUTURE_WORK FW4 (K24: YWJ/ZYVR route blocked as stated); positioning paragraph next to M5 in THEOREM_LIST_FINAL |
| TH402 | Proposition U (API-POS); API-POS Prop U; underfitted models are never local modes of the paper target on LH-G | proposition | LH-G with p = p_n <= delta n, s0, beta, rho, psi fixed, paper target on M(K): there is c_U > 0 such that w.p. -> 1, simultaneously for every gamma in M(K) with S0 not subset of gamma and /gamma/ < K, some j in S0 minus gamma has log pi(gamma+{j})/pi(gamma) >= c n; consequence: ZYVR Condition (1b) holds on all of M(K) with c1 of order n/log p | PROOF SKETCH [API-POS REPORT §5]; "constant bookkeeping and the replacement of y by its standardised version not yet written out"; author-only; THM-INV row 1: PROOF SKETCH | API-POS/REPORT.md §5; API-POS/results/cond1_lh.md | [pos 911] [pos 978] | none (campaign-only positioning input; positioning paragraph next to M5) |
| TH403 | Corollary U prime; Cor U'; API-POS unimodality on LH | corollary | Under the hypotheses of Prop U every local mode of pi under add/delete/swap on M(K) is overfitted; whether S0 is the unique local mode on M(K) is OPEN in general (holds in every enumerated case p <= 20) | PROOF SKETCH, from U [API-POS REPORT §5]; uniqueness OPEN in general | API-POS/REPORT.md §5 | [pos 978] | none (campaign-only) |
| TH404 | Statement R3; API-POS R3; MIX-POS; positioning against YWJ/ZYVR | proposition | (i) under the YWJ-prior with a fixed cap, YWJ Thm 2/Cor 2 and ZYVR Thm 1 apply to LH-iid (p >= n, p <= n^A): recovery of S0 and mixing from any sparse start in O(alpha p n log p) scores (YWJ) or O(n) informed iterations = O(np) scores (ZYVR); (ii) for the paper target Y0, Y7, Y8 and Z4(1a, c0 = 2) fail and Y1 fails for exact-Gram LH; (iii) Condition (1b)/(1c) does hold for the paper target on LH (Prop U): the failure concerns prior strength and size cap, not the landscape | (i) PROOF SKETCH; (ii) PROVED for the definitional failures Y0, Y8, Z2 and PROOF SKETCH for Z4(1a); (iii) via Prop U PROOF SKETCH, YWJ-type spectral-gap proof for the paper prior a CONJECTURE (CJ297); author-only; qualified by LIT-MCMC: R > M fails on LH at n = 200, 1600 and in 12/12 study-like data sets (RF274) | API-POS/REPORT.md §5, §7, §8; THM-INV/REPORT.md D1; LIT-MCMC/REPORT.md | [pos 911] [pos 978] [pos 1009] | positioning paragraph in THEOREM_LIST_FINAL (context next to M5: "with their priors LH is covered by rapid mixing; ours is for the paper's own target and start"); FUTURE_WORK FW4 |
| TH405 | N9 Claim G; N9-G; V5 Gibbs flip; Gibbs coordinate step reversible | proposition | Gibbs coordinate j (heat bath with cap rule: an addition at /S/ = K is a self-loop) is gamma_phi-reversible on S_K for every phi in [0,1]; gamma_phi(S) = varpi(S) BF(S)^phi prod_b r_b(S cap C_b)^{1-phi} [theory/N9-KERNEL PROOF.md §1] | PROVED (candidate) [N9-KERNEL PROOF.md §4 and REPORT.md §2]; author-only proof (Claude run); exact numerical check on production headers at 39db138 (DB rel <= 2.0e-14 (CHECK.md)); CHK_INHERITED (cross-family, gpt-6.1-sol, line by line against code): VERIFIED WITH AMENDMENT (section verdict; claims G, U, N, I, R, Z, S check against code); MEET-THM registry N9K stays PROVED (candidate) | N9-KERNEL/PROOF.md; N9-KERNEL/REPORT.md; N9-KERNEL/CHECK.md; N9-KERNEL/HQ_NOTE.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1454] [pos 1467] [pos 1546] [pos 1550] [pos 1593] [pos 1626] | S-KERNEL (K20) |
| TH406 | N9 Claim U; N9-U; V5 uniform swap | proposition | Uniform swap (q = 1/(k(p-k)), acceptance 1 ^ gamma'/gamma, self-loop at /S/ in {0,p}) is gamma_phi-reversible and size-preserving [theory/N9-KERNEL PROOF.md §1] | PROVED (candidate) [N9-KERNEL PROOF.md §4 and REPORT.md §2]; author-only proof (Claude run); exact numerical check on production headers at 39db138 (DB rel <= 8.2e-14); CHK_INHERITED (cross-family, gpt-6.1-sol, line by line against code): VERIFIED WITH AMENDMENT (section verdict; claims G, U, N, I, R, Z, S check against code); MEET-THM registry N9K stays PROVED (candidate) | N9-KERNEL/PROOF.md; N9-KERNEL/REPORT.md; N9-KERNEL/CHECK.md; N9-KERNEL/HQ_NOTE.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1454] [pos 1467] [pos 1546] [pos 1550] [pos 1593] [pos 1626] | S-KERNEL (K20) |
| TH407 | N9 Claim N; N9-N; V5 neighbour swap; Hastings factor | proposition | Neighbour swap with acceptance 1 ^ (gamma'/gamma) /N(j) minus S/ / /N(l) minus S'/ is gamma_phi-reversible for every symmetric loop-free duplicate-free graph N, whatever the degrees [theory/N9-KERNEL PROOF.md §1] | PROVED (candidate) [N9-KERNEL PROOF.md §4 and REPORT.md §2]; author-only proof (Claude run); exact numerical check on production headers at 39db138 (DB rel <= 1.1e-13; Hastings factor != 1 on 31-61% of proposals; control without the factor fails (rel 0.5-0.75)); CHK_INHERITED (cross-family, gpt-6.1-sol, line by line against code): VERIFIED WITH AMENDMENT (section verdict; claims G, U, N, I, R, Z, S check against code); MEET-THM registry N9K stays PROVED (candidate) | N9-KERNEL/PROOF.md; N9-KERNEL/REPORT.md; N9-KERNEL/CHECK.md; N9-KERNEL/HQ_NOTE.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1454] [pos 1467] [pos 1546] [pos 1550] [pos 1593] [pos 1626] | S-KERNEL (K20, K22) |
| TH408 | N9 Claim I; N9-I; V5 independence move | proposition | If the draw_pi0 law equals pi0 = gamma0/Zbar0 on S_K (Claim S) the independence step with acceptance 1 ^ exp(phi(d'-d)) is gamma_phi-reversible; Zbar0 cancels [theory/N9-KERNEL PROOF.md §1] | PROVED (candidate) [N9-KERNEL PROOF.md §4 and REPORT.md §2]; author-only proof (Claude run); exact numerical check on production headers at 39db138 (DB rel <= 2.3e-12; control with symmetric acceptance fails (rel 1.0)); CHK_INHERITED (cross-family, gpt-6.1-sol, line by line against code): VERIFIED WITH AMENDMENT (section verdict; claims G, U, N, I, R, Z, S check against code); MEET-THM registry N9K stays PROVED (candidate) | N9-KERNEL/PROOF.md; N9-KERNEL/REPORT.md; N9-KERNEL/CHECK.md; N9-KERNEL/HQ_NOTE.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1454] [pos 1467] [pos 1546] [pos 1550] [pos 1593] [pos 1626] | S-KERNEL (K20, K103) |
| TH409 | N9 Claim Z; N9-Z; Zbar0 exact; truncated size-profile convolution | proposition | F_J(k) = Sum_{/S/=k} prod_b r_b(S cap C_b) for k <= K and Zbar0 = Sum_{k<=K} varpi(k) F_J(k) = Sum_{S in S_K} gamma0(S) exactly (truncation of the convolution at K is exact for indices <= K) | PROVED (candidate) [N9 PROOF.md]; numerical: build_start vs brute force <= 4.5e-16, vs independent long-double spec <= 1.3e-14; CHK_INHERITED VERIFIED WITH AMENDMENT (cross-family, gpt-6.1-sol) | N9-KERNEL/PROOF.md §3; N9-KERNEL/REPORT.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1546] [pos 1550] [pos 1593] [pos 1626] | S-KERNEL (K08) |
| TH410 | N9 Claim S; N9-S; draw_pi0 exact start sampler; backward block-size sampler telescopes | proposition | draw_pi0 returns S with probability exactly pi0(S) for every S in S_K and never a set outside S_K: size k ~ varpi(k)F_J(k)/Zbar0, block sizes backwards from e_b(j)F_b(r-j)/F_{b+1}(r) (product telescopes to prod_b e_b(k_b)/F_J(k)), sub-model within its size class proportional to r_b; ties play no role | PROVED (candidate) [N9 PROOF.md]; numerical: DFS law vs gamma0/Zbar0 max rel <= 2.0e-13, TV <= 5e-16; production-RNG chi^2 p = 0.51, 0.97, 0.33; CHK_INHERITED VERIFIED WITH AMENDMENT (cross-family, gpt-6.1-sol) | N9-KERNEL/PROOF.md §3; N9-KERNEL/CHECK.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1546] [pos 1550] [pos 1593] [pos 1626] | S-KERNEL (K08) |
| TH411 | Theorem V; Thm V; V1 (THM-SYNTH); validity of v3.1 under parallel execution; fixed-data validity for any island count | theorem | Fixed data, frozen calibration C, R and stacking schedule declared before final randomness, EX-A, EX-S, V5: (a) E[W_r] = 1 and E[W_r hhat_r] = pi(h) for every N >= 1 and r; (b) E[Zhat] = Z and P(0.05 Zhat > Z) <= 0.05; (c) Sum_r Zhat_r hhat_r / Sum_r Zhat_r -> pi(h) a.s. as R -> infinity at fixed N, each hhat_r -> pi(h) as N -> infinity; (d) pooled product Zhat * mean PIPhat is not unbiased: bias -(1-1/R) Cov(Zhat_1, hhat_1 / C) | Assembled statement (THM-SYNTH): T12 and T31(i) PROVED-LOCKED; Prop 2(a,b,d,e) PROVED, XF A-REV4 GAP on output-Markov wording; ADRAFT-ThmA PROVED (Astra author, Astra check only); Prop P(ii),(iv),(v) PROVED (candidate); V5 now N9 PROVED (candidate); novelty KNOWN-CITE; tier v1 (cited lemma + Prop) | THM-SYNTH/THEOREM_LIST.md (V1); THM-SYNTH/REPORT.md | [pos 1099] [pos 1177] [pos 1185] | M1 Theorem V/H (K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47) |
| TH412 | Theorem H; Thm H; A1 (THM-SYNTH); Zhat-weighted estimates of bounded functionals; joint inclusion; NEW-SYNTH; A1new | theorem | h: Omega -> [0,1], hhat_r the island plain (or Rao-Blackwellised) estimate: (a) E[W_r /hhat_r - h(S0)/ / C] <= delta_1 for the plain average (<= 2 delta_1 + c_h(rho_bar+u_pi) for the RB version); (b) P(/hhat^zw - h(S0)/ > t / C) <= exp{-R(1-s)^2/(2E[W_1^2/C])} + delta_1/(s t), or with Hoeffding on W ^ M_C(eps): exp{-2R(1-eps-s)^2/M_C(eps)^2} + delta_1/(s t); (c) joint inclusion h_A(S) = 1{A subset S}; (d) on T03 hypotheses, if R_n(1-s)^2/E[W^2/C_n] -> infinity in probability then hhat^zw -> h(S0) in probability jointly with output; (e) fixed data: hhat^zw -> pi(h) a.s. as R -> infinity | PROOF SKETCH (NEW-SYNTH) [THM-SYNTH REPORT §2]; crux not verified: island identity E[W_r hhat_r] = pi(h) for the measured-round average; PC1 claim 3 (same-family Claude check): finite-R bound P(/muhat - mu/ > eps) <= min{1, 4(M-1)/R + 4M/(R eps^2)} PROVED (add W_r >= 0), the identity "is still a premise"; (d) R_n condition uncheckable without an upper bound on E[W^2/C_n]; final MEET-THM: N1 (general-h identity) PROOF SKETCH | THM-SYNTH/THEOREM_LIST.md (A1); THM-SYNTH/REPORT.md §2; MEET-v31/evidence/2026-11-03_PC1_proof_check.md (Claim 3); MEET-THM/THEOREM_LIST_FINAL.md (M1) | [pos 1099] [pos 1177] [pos 1242] | M1 Theorem V/H (K51, K52, K48); FUTURE_WORK FW27 (unbounded h) |
| TH413 | Theorem Z; Thm Z; A2 (THM-SYNTH); the evidence: what Zhat can and cannot do | theorem | One island: (i) E[Zhat_r/C] = Z, E[log Zhat_r] <= log Z, P(0.05 Zhat > Z) <= 0.05; (ii) exact variance identity (O-PW2 Thm A), pooled variance = this / R; (iii) masked regime lower tail (MASKZPIP E1/E2): P(W > (T/eta)[pi0(A^c)/pi0(x_m)] e^{-phi_{tau_A} D_A}) <= eta + N pi0(A); (iv) run certificate Zhat/Z <= Zhat/Z_T (MASKZPIP C1); (v) favourable regime (W2-T26 Thm A) Zhat/Z -> 1 under (P1); plain-language gloss "in the masked regime Zhat errs only downward" is literally false (RF233) | Assembled: T12/T31(i) PROVED-LOCKED; O-PW2 ThmA PROVED, XF VERIFIED (A-REV9); MASKZPIP E1/E2, C1 PROVED (candidate); T26-ThmA PROVED, XF VERIFIED*; Thm 6 overall CONJECTURE; two-sided masked Zhat tiered v2; PC1 claim 4: the "Plainly" sentence and table row COUNTEREXAMPLE valid (CE219), formal (iii) not refuted | THM-SYNTH/THEOREM_LIST.md (A2); MEET-v31/evidence/2026-11-03_PC1_proof_check.md (Claim 4); MEET-v31/R1_C.md | [pos 1177] [pos 1242] | S-Z (K37-K41, K53); M4 Theorem Z_T and certificate card (masked-regime statement); FUTURE_WORK FW24 |
| TH414 | Theorem D; Thm D; D1 (THM-SYNTH); work, depth and width of v3.1; comparison with Song-Liang s6 | theorem | (a) work W = J 2^B s(B) + Sum_e [H_e(T_pil+L+4) + 4 H_e Sum_i (T^(i)+L+4)] m sbar + R N (T+L+4) m sbar + n_LS (l+1)(p + kbar(p-kbar)) sbar + O(np^2) + O(p^2)-O(p^3); (b) island-parallel depth D_PEL; (c) particle-parallel depth D_PP free of N, H and R, worst case O(m l T_e) = O(p log^3(n+p)), declared v3.2 path; (d) comparison in the same units: Song-Liang s6 with K_n = sqrt(p) has wall time O(p^{(1+alpha)/2}) + O(np), v3.1 depth of the same order in p at alpha = 1 up to logs with far more width and work, output = pi exactly | Prop D PROVED (counting); T32(i) PROVED (W5-LOCKBOOK), displayed rate GAP (A-REV6); Song-Liang s6 figures from the JRSS-B text (SL digest); (c) struck for v3.1 (MEET-v31 decision 6, RF271); tier v1 | THM-SYNTH/THEOREM_LIST.md (D1); METH-AUDIT/PROOFS.md; MEET-THM/THEOREM_LIST_FINAL.md (Card Prop D) | [pos 1038] [pos 1107] [pos 1177] | M8 Proposition D (K87, K88, K89, K06, K64; K90 remark) |
| TH415 | Theorem STG; Thm STG; D2 (THM-SYNTH); stage laws of the v3 grid | theorem | Grid as coded, Phi_V(u,v) = D2(q_v//q_u), c = log(10/9): (a) structure (Theorem G, Lemma RS): greedy grid shortest valid, max(T*_V,T_P) <= T_grid <= T*_V + T_P, T <= T_e on success; (b) favourable: T* = O(1); (c) masked crossing on the ideal two-state grid T* = log2 A0 + O(1); (d) fine grid sqrt(c) T*(c) -> L = Syed et al. Lambda, L <= pi while T* -> infinity at the production c | Theorem G PROVED (deterministic, as coded); STG-F PROVED; STG-M PROVED on the ideal two-state grid, XF VERIFIED* (A-REV9); families PROOF SKETCH; as-coded masked T_n = Conjecture P OPEN; G(i) KNOWN-CITE (SVV 2009), (d) KNOWN-CITE (Syed et al.) | THM-SYNTH/THEOREM_LIST.md (D2); LIT-SMC/REPORT.md | [pos 1177] | M7 Theorem STG (K26, K25, K27, K30, K33); FUTURE_WORK FW6, FW23 |
| TH416 | Theorem CD; Thm CD; D3 (THM-SYNTH); the thesis sentence as a theorem; Thesis CD | theorem | Fix any design X and data, EX-A, EX-S, CAL, R declared: (a) never correctness: final stage targets pi exactly, E[Zhat_r/C] = Z, Zhat-weighted pooled estimates of bounded h converge, islandwise error <= 2 delta_1 + c_h(rho_bar+u_pi); (b) costs depth: critical path (I+2)(T+L+4) m free of N,H,R, T <= T_e, T = O(1) or log2 A0 + O(1) on the ideal grid; (c) costs islands: Zhat-weighted error exceeds t w.p. <= exp{-R(1-s)^2/(2E[W^2/C])} + (2 delta_1 + ...)/(s t), E[W^2/C] >= 1/P_C(crossing) (PROOF SKETCH); (d) selection: on exact-Gram LH reported HPM = S0 w.p. -> 1 - limsup P(U) while feature splitting loses the masked hub | Assembled from V1, A1 (PROOF SKETCH), D1, D2, M3, R5, C1 (COUNTEREXAMPLE + PROOF SKETCH); weakest links A1, C1 and the as-coded T_n law (OPEN); final disposition: "Remark only. There is no retained non-corollary thesis sentence" (MEET-THM) | THM-SYNTH/THEOREM_LIST.md (D3); THM-SYNTH/REPORT.md §3; MEET-THM/THEOREM_LIST_FINAL.md (Thesis CD) | [pos 1044] [pos 1177] [pos 1441] | Thesis CD (K96): scoped remark after the main theorems |
| TH417 | Theorem SL; Thm SL; C1 (THM-SYNTH); C1new; analytic split-and-merge failure on a masked LH family; NEW-SYNTH | theorem | LH exact Gram with c linked pairs, Song-Liang procedure (uniform equipartition into K_n subsets of size s_n, Stage-1 PIP threshold q, SL priors); E_n = some masked hub isolated in its subset from its partner and its own group: (a) P(isolated) = C(P_n-1-g, s_n-1)/C(P_n-1, s_n-1) >= 1 - g(s_n-1)/(P_n-1), P(E_n) -> 1 if K_n -> infinity; (b) on E_n cov(x_jb, y) = 0, Condition 5 fails exactly, beta_0 = 0, j_b not in S-tilde w.p. -> 1, so SL output cannot equal S0; (c) exact posterior concentrates on S0; (d) v3.1 targets pi exactly (T38 (b1-LH) with LS0, (b2-LH) on STAB-LH); (e) if the split keeps j_b with its group, beta_0 != 0 and Stage 1 retains it | COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (NEW-SYNTH); crux (b) PIP -> 0 under the SL priors "NOT REPAIRED (W2PC1)" at MEET-THM; LH-iid v2; final: FUTURE_WORK FW21, LIT-PAR G4 cited as labelled numerical evidence | THM-SYNTH/THEOREM_LIST.md (C1); THM-SYNTH/REPORT.md §2; LIT-PAR/REPORT.md §3.1 G4; LIT-PAR/notes/09_sam_lh_counterexample.md; MEET-THM/FUTURE_WORK.md (FW21) | [pos 1177] [pos 1185] | FUTURE_WORK FW21 (K97); Coverage Cor 2 numerical-evidence citation |
| TH418 | hpm_eq_truth; Lean T21 deterministic core; TH278 (Thm4-C1) core | theorem | If post F A S0 > 1/2, S0 in scored set (subset of A) and Shat maximises F over it, then Shat = S0 (any tie rule) | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only) | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/ASSUMPTIONS.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) via TH278 (Thm4-C1)/TH281 (T38-(0)) |
| TH419 | t21_decomposition; T21 decomposition (sharp form) | theorem | P(U or Shat != S0) <= P(U) + P(U^c, S0 not in scored) + P(U^c, S0 in scored, pi(S0) <= 1/2); no measurability needed | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only) | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) |
| TH420 | t21_decomposition'; T21 decomposition (L-LEAN brief form) | theorem | P(U or Shat != S0) <= P(U) + P(S0 not in scored) + P(U^c, S0 in scored, pi(S0) <= 1/2) | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only) | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) |
| TH421 | markov_half; Markov at level 1/2 | theorem | P.real{delta >= 1/2} <= 2 * integral of delta for integrable delta >= 0 | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only) | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) |
| TH422 | t21_C1; Lean (C1); TH278 (Thm4-C1) (Lean); T21 (C1); T21 C1 | theorem | P.real(U or Shat != S0) <= P.real(U) + 2*integral(1 - pi(S0)) + P.real(U^c, S0 not in scored); abstract probability space, measurable scores | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal TH278 (Thm4-C1) PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none); T21 pre-campaign PROVED-LOCKED, CONDITIONAL | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/REPORT.md; T38-RECORD/REGISTRY_v2.md (section G; row Thm4-C1) | [pos 714] [pos 796] [pos 929] | M5 Theorem HPM (K72) |
| TH423 | ceiling; T07(i) ceiling; Lean T07 ceiling | theorem | If S0 is the least argmax over Omega of (positive size-only prior) x m then s0 <= K and S0 is the least argmax of m in its size class | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); cited-lemma card L-DEC |
| TH424 | no_size_prior_repairs; W2-BOOK (iii'); no size-only prior repairs a within-size ranking error | theorem | If a same-size S' beats S0 in m (or ties and precedes in the tie order) then for every positive size-only prior S0 is not the global HPM | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH425 | ceiling_sharp; T07(i') sharpness; W2-BOOK Prop 1 (i') | theorem | If s0 <= K, m > 0 and S0 = S*_{s0}, some positive size-only prior makes S0 the global HPM | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH426 | risk01_min_iff; T07(ii)(a) | theorem | a minimises posterior 0-1 risk over all subsets iff a is in argmax_Omega F | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH427 | hpm_min_risk01; T07(ii)(a) HPM minimises 0-1 risk | theorem | The tie-selected HPM S-dagger minimises the posterior 0-1 risk | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH428 | mpm_min_riskH; T07(ii)(b) | theorem | MPM = J+(PIP) minimises posterior Hamming risk over all subsets | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH429 | mpm_unique_iff; T07(ii)(b) uniqueness | theorem | MPM is the unique Hamming-risk minimiser iff no PIP_j equals 1/2 | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH430 | capped_mpm_min_riskH; T07(ii)(c) | theorem | The capped MPM a* (top min(K,N+) PIPs in J+) is feasible and minimises Hamming risk over Omega | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH431 | reported_eq_hpm_iff; T07(iii)(a) | theorem | For nonempty scored set S in Omega: reported Shat = S-dagger iff S-dagger in scored set (common injective tie rank) | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH432 | reported_min_risk01_iff; T07(iii)(a) | theorem | Shat minimises 0-1 risk iff scored set meets argmax_Omega F | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH433 | reported_truth_needs_unscored; T07(iii)(b) | theorem | {Shat = S0} and {S*_{s0} != S0} imply S*_{s0} not in scored set (F = log(pw m), pw>0, m>0) | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH434 | excess_riskH_le; T07(iii)(c) | theorem | 0 <= rhoH(ahat) - rhoH(aopt) <= 2 sum over ahat symdiff aopt /qhat_j - PIP_j/ <= 2 //qhat - PIP//_1 for any real qhat and finite action class | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH435 | mpm_hat_eq_iff; T07(iii)(c) last clause | theorem | J+(qhat) = J+(PIP) iff for every j: qhat_j > 1/2 <=> PIP_j > 1/2 | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only); informal Prop1-T07 PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60); L-DEC |
| TH436 | t11_miss_pi; T11(iii) product-space form | theorem | Product measure of Q iid pi0 draws: P(s never drawn) = (1 - pi0{s})^Q (ENNReal) | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (scope-qualified: fixed-calibration iid identity); informal T11(iii) PROVED-LOCKED (pre-campaign), no registry row | L-LEAN/SmcBvs/SmcBvs/T11Miss.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/ASSUMPTIONS.md (A-T11-1) | [pos 714] [pos 796] | K19 by registrar statement-match only (REGISTRY_PAPER1 line 527) |
| TH437 | t11_miss_pi_real; T11(iii) real form | theorem | Real-valued identity (1 - pi0.real{s})^Q and bound <= exp(-Q pi0.real{s}) on the product space | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (scope-qualified: fixed-calibration iid identity); informal T11(iii) PROVED-LOCKED (pre-campaign), no registry row | L-LEAN/SmcBvs/SmcBvs/T11Miss.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | K19 by registrar statement-match only |
| TH438 | t11_miss_iid; T11(iii) random-variable form | theorem | For independent X_i with law pi0 (iIndepFun): P(s not among X_0..X_{Q-1}) = (1 - pi0{s})^Q | Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (scope-qualified: fixed-calibration iid identity); informal T11(iii) PROVED-LOCKED (pre-campaign), no registry row | L-LEAN/SmcBvs/SmcBvs/T11Miss.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | K19 by registrar statement-match only |
| TH439 | t11_miss_iid_real; T11(iii) iid real form | theorem | Real-valued iid miss identity and exp(-Q pi0{s}) bound | Lean: sorry-free; added after Fable remark 7; no Fable or Astra row (in neither fidelity packet) | L-LEAN/SmcBvs/SmcBvs/T11Miss.lean; L-LEAN/ADVISER_DECISIONS.md | [pos 714] [pos 796] | K19 by registrar statement-match only |
| TH440 | path_F_strictMono; Lemma 0(a); LM144 (Lemma0(a,c)) (a) | theorem | F strictly increases along the greedy moves actually made | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 GREEN; Astra r2 GREEN | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65); cited-lemma card L-TA |
| TH441 | theoremA1; Theorem A (A1 forward); TH199 (Theorem A) (A1) | theorem | Under TD'_inf(R) the greedy path from S in R stays in R and reaches S0 within r_R(S) moves, then stays | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 GREEN; Astra r2 GREEN | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH442 | theoremA1_converse; Theorem A (A1 reverse) | theorem | If from every S in R the path stays in R and terminates at S0 (M S0 = none) then TD'_inf(R) holds | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 GREEN; Astra r2 GREEN | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH443 | theoremA2; Theorem A (A2 abstract) | theorem | Under TD'_P(R) from S in R the path reaches S0 after tau <= Phi(S) moves, stays in R, Phi strictly decreases, then stays at S0 | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 RED (coverage, objections 1-3); Astra r2 GREEN after added theorems; informal Theorem A PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)) | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH444 | theoremA3; Theorem A (A3 abstract) | theorem | Under TD'_P(R), for every cap l >= tau (tau <= Phi(Sc)) the capped search returns S0 certified, and every centre and scanned neighbour has F <= F(S0) | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 RED (coverage, objections 1-3); Astra r2 GREEN after added theorems; informal Theorem A PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)) | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH445 | theoremA3_hpm; Theorem A (A3) HPM clause (ledger bound) | theorem | With pre-search scored set whose running best is the centre Sc, every model in pre and every scanned model has F <= F(S0) | Lean: sorry-free; Astra r2 GREEN; not in packet 1 so no Fable row; added after Fable remark 1 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH446 | lemma0c; Lemma 0(c) general form; LM144 (Lemma0(a,c)) (c) | theorem | If the greedy path reaches S0 after tau steps and M S0 = none then every centre path k (k<=tau) and every scanned neighbour has F <= F(S0); no region condition | Lean: sorry-free; Astra r2 GREEN; not in packet 1 so no Fable row; added after Astra r1 objection 3 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65); cited-lemma card L-TA |
| TH447 | lemma0c_hpm; Lemma 0(c) reported-HPM clause | theorem | Every maximiser Shat of F over the post-search ledger L has F(Shat) = F(S0); Shat = S0 if no tie; under an injective tie rank preferring S0, Shat = S0 | Lean: sorry-free; Astra r2 GREEN; not in packet 1 so no Fable row; added after Astra r1 objection 2 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65); cited-lemma card L-TA |
| TH448 | pd_of_reach; Theorem A (A4) PD part | theorem | If the greedy path from S != S0 reaches S0 then F S < F S0 | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 GREEN; Astra r2 GREEN | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH449 | lemma2a; Lemma 2(a); LM146 (Lemma2-T37) (a) | theorem | A progress flip/swap (Phi drops) maps Lat(S) into Lat(S) and R_{a,d} into R_{a,d} | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 GREEN; Astra r2 GREEN; informal LM146 (Lemma2-T37) PROVED (SF: VERIFIED (W3-VT37R); XF: none) | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH450 | theoremA2_lattice; Theorem A (A2 concrete lattice form) | theorem | Under TD'_P(R_{a,d}) on flip/swap neighbourhood: tau <= Phi(S), path stays in Rad and Lat(S), Phi strictly decreases | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 RED (coverage, objections 1-3); Astra r2 GREEN after added theorems; informal Theorem A PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)) | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH451 | theoremA2_lattice_count; Theorem A (A2) move count | theorem | max(mis S, ext S) <= tau <= Phi(S), each move drops Phi by 1 or 2, and tau + sigma = mis S + ext S where sigma counts the steps dropping Phi by 2 (extra->truth swaps) | Lean: sorry-free; Astra r2 GREEN; not in packet 1 so no Fable row; added after Astra r1 objection 1 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH452 | theoremA3_lattice; Theorem A (A3 concrete, cap l >= Phi) | theorem | Under TD'_P(R_{a,d}), Sc in R_{a,d}, l >= Phi(Sc) (in particular l >= a+d): capped search returns S0 with M(returned) = none | Lean: sorry-free; Fable 5.1 GREEN; Astra r1 RED (coverage, objections 1-3); Astra r2 GREEN after added theorems; informal Theorem A PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)) | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH453 | theoremA3_lattice_tau; Theorem A (A3) sharp cap l >= tau | theorem | Exists tau <= Phi(Sc) such that every cap l >= tau returns S0 certified and all scored models have F <= F(S0) | Lean: sorry-free; Astra r2 GREEN; not in packet 1 so no Fable row; added after Astra r1 objection 3 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH454 | theoremA3_lattice_only; Theorem A (A3) lattice-condition version | theorem | Under (L) and D_S at every S in Lat(Sc) minus S0 only, the path stays in Lat(Sc), reaches S0 in tau <= Phi(Sc) moves, and every cap l >= tau certifies | Lean: sorry-free; Astra r2 GREEN; not in packet 1 so no Fable row; added after Astra r1 objection 3 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH455 | card_le_of_mem_Rad; feasibility of Rad | theorem | If s0 + d <= K then every model of Rad S0 a d has size <= K | Lean: sorry-free; Astra r2 GREEN; not in packet 1 so no Fable row; added after Fable remark 3 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| TH456 | unbiased_of_step; T12(i.a) reduction; TH297 (Prop2(a,b,d,e)) (Lean part) | theorem | Given stage-0 identity h0 and recursion hstep, E_t f = sum_x gamma_t(x) f(x) for all t (induction; hstep is an explicit hypothesis) | Lean: sorry-free but PARTIAL (hstep and h0 explicit hypotheses); Fable 5.1 GREEN; Astra r1 GREEN; informal TH297 (Prop2(a,b,d,e)) PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); T12 pre-campaign PROVED-LOCKED | L-LEAN/SmcBvs/SmcBvs/T12Core.lean; L-LEAN/T12_PLAN.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] [pos 717] [pos 953] | M1 Theorem V/H (K35); cited-lemma card L-T12 |

## Lemmas

| ID | native name(s) | kind | description | final status | authoritative file | positions | feeds |
|---|---|---|---|---|---|---|---|
| LM101 | Lemma E1; E1; exact tail; BB(1,p) size marginal | lemma | The BB(1,p) size marginal has ratio rho_i=(p-i)/(2p-1-i)=1/2(1-(i-1)/(2p-1-i)); two-sided bounds (b),(c) on R_m; comparison (d): improvement over the locked tail by >= 4 s0! e^(gamma_m). | PROVED (W1-T03R); SF VERIFIED (W2-VT03R rows 1-4; exact rationals, 2,779 triples); XF VERIFIED (A-REV2: E1(a)-(d); E1(d) is a lower bound on the improvement factor) | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 296]; [pos 370]; [pos 570] | feeds S-T (K93) and S-TARGET (K04: geometric size masses ratio <= p/(2p-1)) |
| LM102 | Lemma E2; E2; cutoff m#_n; location of the exact-tail cutoff | lemma | m#_n(omega)=min{m>=s0: R_m <= n^(-(s0+1)/2) e^(-omega)} satisfies s0 <= m# <= min(K, m_n(omega)), closed-form upper bound, and a lower bound when m# <= K-1. | PROVED (W1-T03R); SF VERIFIED (W2-VT03R rows 5-7); XF VERIFIED (A-REV2: keep s0>=1 restrictions and n>=5 null-truth exception) | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 296]; [pos 370]; [pos 570] | feeds S-T (K93) |
| LM103 | Lemma den'; den′; den-prime; denominator lemma before the S0 prior bound | lemma | Under G, R, s0<=K: m^c_{b+}(S0)/f0(y_c) >= (n+1)^(-s0/2) c_IG sigma*^2 n^(-1/2) e^(-Lambda_n), E0 Lambda_n <= C_Lambda (the locked lem:den before varpi(S0) is bounded). | PROVED (W1-T03R); SF VERIFIED (W2-VT03R row 9); XF VERIFIED (A-REV2: constant c# = kappa^2/(c_IG sigma*^2), no stray factor 4) | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 296]; [pos 370]; [pos 570] | feeds S-T (K93) |
| LM104 | Lemma I; Lemma B; LemmaI-B; (B1); (B2); (B3); interlacing | lemma | Interlacing lambda_min(G_T) >= lambda_min(G_T') for T subset T'; SE_w gives full column rank, exact chi-square law and determinant bound on S0 union J (B1); (B2) for underfitting S with /J'/<=j0; (B3) upper half of cor:diff with eigenvalue condition on the smaller set only. | PROVED (W1-T03R); SF VERIFIED (W2-VT03R row 13; 9,000 random pairs); XF VERIFIED (A-REV2: fixed unnormalised g0>0 suffices; g0_n->0 not covered) | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 296]; [pos 370]; [pos 570] | feeds S-T (K93) |
| LM105 | Lemma A1; anchored = unanchored; LemmaA1 | lemma | For g>0, m>=0: lambda_min(G_{S0 u J}) >= g for all /J/<=m iff lambda_min(G_T) >= g for every nonempty T with /T minus S0/ <= m (interlacing); same for R and phi0^2; anchoring saves only s0 columns and forces spark(X) > m. | PROVED (author = verifier W2-VT03R); no second same-family check; XF: A-REV2 section 3.3 states the same equivalence without a verdict row | W2-VT03R/REPORT.md; A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md | [pos 337]; [pos 370]; [pos 570] | feeds S-T scope remark (K93); wording fix R2 |
| LM106 | Lemma T05-R; Cor T05-R1; exact representation under ORTH; T05(i) | lemma | Under G and ORTH: Q_S=(n-1)V_S/V_tot, D_S=n^/S/, F(S)=kappa+log varpi(/S/)-(/S//2)log n-nu log(c_n+V_S); S_dagger is the top-k set by T_j^2 at the best k. | PROVED (author W7-SEC; checked by enumeration 70/70 data sets; own check only); XF none (A-REV9 deferred) | W7-SEC/PROOF_T05.md; W7-SEC/REPORT.md | [pos 717]; [pos 751] | feeds: none found |
| LM107 | BB(1,p) is not a complexity prior; CSvdV (2.2) violated (LIT-STAT section 6) | lemma | The dimension prior ratio of BB(1,p) is (p-s+1)/(2p-s) -> 1/2, so the CSvdV exponential-decrease condition (2.2) holds for no fixed A4>0 uniformly in p (A4 = 0.100-0.108 at p=1000, 0.111-0.130 at p=500 for s<=100); CSvdV Thms 1, 4 and Cor 1 do not apply to the size prior. | PROVED (elementary algebra with exact rational confirmation; LIT-STAT, author only; no verifier) | LIT-STAT/REPORT.md | [pos 986]; [pos 1009] | feeds: none (positioning sentence for S-T; cited in paper text) |
| LM108 | BB(1,p) versus BB(1,1); geometric size tilt (LIT-STAT section 12) | lemma | w_{BB(1,p)}(k)/w_{BB(1,1)}(k) = (p+1)C(p,k)/(2C(2p-1,k)) = ((p+1)/2) 2^(-k)(1+o(1)) for k<<sqrt(p); BB(1,p) is BB(1,1) times a size-only factor <= ((p+1)/2)(2p/(2p-1))2^(-k) for k>=1. | PROVED (elementary; LIT-STAT, author only; first-draft line "<= 1/2 for every i>=0" was false at i=0 and corrected = RF131) | LIT-STAT/REPORT.md | [pos 1009] | feeds: none (positioning: T03-sharp is a modest extension of Rossell 2022) |
| LM109 | W1-EXP Lemma 1.1; Q_S versus RSS | lemma | For lambda_min(G_S) >= phi^2(n-1): Q_S = RSS^y_S + c_S with 0 <= c_S <= 1 + 1/(n phi^2), c_empty = 0 | PROVED; SF VERIFIED (W3-VEXP row 1); XF VERIFIED (A-REV2) | W1-EXP/PROOF.md; A-REV2/REVIEW.md | [pos 351] [pos 363] [pos 568] | feeds: via EXP′ (M3 K16 hypothesis) |
| LM110 | W1-EXP Lemma 1.2; determinant ratio | lemma | log D_{T+l} - log D_T = log(n+1) + eta_D with /eta_D/ <= (1+phi^-2)/(phi^2(n-1)) | PROVED; SF VERIFIED (row 2); XF VERIFIED (A-REV2) | W1-EXP/PROOF.md; A-REV2/REVIEW.md | [pos 351] [pos 363] [pos 568] | feeds: via EXP′ |
| LM111 | W1-EXP Lemma 1.3; exact decomposition of the EXP′ remainder | lemma | R = -(1/2)eta_D - nu[log(1+a_{T+l}/RSS^y_{T+l}) - log(1+a_T/RSS^y_T)] with a_U in [0.02, 1.02+1/(n phi0^2)]; hence the deterministic bound | PROVED; SF VERIFIED (row 3); XF VERIFIED (A-REV2) | W1-EXP/PROOF.md; A-REV2/REVIEW.md | [pos 351] [pos 363] [pos 568] | feeds: via EXP′ |
| LM112 | W1-EXP Lemma 1.4; RSS floor | lemma | P_0(min_{b,U} RSS^y_U >= c_* n) -> 1, c_* = sigma^2/(8(M+2 sigma^2)) | PROVED; SF VERIFIED (row 4); XF VERIFIED (A-REV2) | W1-EXP/PROOF.md; A-REV2/REVIEW.md | [pos 351] [pos 363] [pos 568] | feeds: via EXP′ |
| LM113 | W1-EXP Lemma 2.3; leakage bounds discrepancy; visibility from block gain | lemma | /delta_{T,l}/ <= sqrt(lambda_b(S°)) on L_n°; ZL gives NL_avg(1/2); VIS from block gain g_b(S°) | PROVED; SF VERIFIED (row 9) | W1-EXP/PROOF.md; W3-VEXP/REPORT.md | [pos 351] [pos 363] | feeds: none |
| LM114 | W1-EXP Lemma 4.1; LH population algebra | lemma | lambda_min(Sigma) >= (1-psi_+)(1-rho_+); masked groups orthogonal to signal; block projection support is exactly S° | PROVED; SF VERIFIED (row 16) | W1-EXP/PROOF.md; W3-VEXP/REPORT.md | [pos 351] [pos 363] | feeds: M3 K17 LH exhibit (via Thm5-LH) |
| LM115 | W1-EXP Lemma 4.2; method partition = groups on LH exact Gram | lemma | If R=Sigma, /psi_i/<min(rho_a,rho_b), g<=B<2g then the v3 partition has blocks exactly equal to the groups | PROVED; SF VERIFIED (row 17; boundary psi>rho found) | W1-EXP/PROOF.md; W3-VEXP/REPORT.md | [pos 351] [pos 363] | feeds: S-BLOCKS K07 idea (strict separation + SIZE) |
| LM116 | PXN Lemma B; W3-PXN Lemma B; exact Beta laws of start statistics | lemma | X_{h,V} ~ Beta(/V//2, (n-1-/U°/-/V/)/2); neutral x_{A,l} ~ Beta(1/2, (n-2-/A/)/2); masked hubs independent of y with (n-1) r_hat^2 ->d chi^2_1 | PROVED; SF VERIFIED (W5-VMASK rows 1-3, 16 KS tests); XF VERIFIED (A-REV3) | W3-PXN/PROOF.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md | [pos 423] [pos 742] | feeds: none (campaign-only) |
| LM117 | PXN Lemma Tr; truncated moment and tail of Beta statistics | lemma | E[(1-X)^-nu 1{X<=tau}] <= 2^{e1}(m tau/2)^{j/2}/Gamma(j/2+1); tails and uniform tail over n^{A+1}2^17 variables | PROVED; SF VERIFIED (W5-VMASK rows 4-5); XF VERIFIED* (A-REV3: in stated range only) | W3-PXN/PROOF.md; A-REV3/REVIEW.md | [pos 423] [pos 742] | feeds: none |
| LM118 | PXN Lemma U; (U1)-(U3); uniform score approximation on small sets | lemma | On sets of size <= s0+2: (U1) F(A) = log w - (/A//2)log(n+1) - nu log RSS_A + c_n + R_A, /R_A/<=kappa_2; (U2) /RSS_A - n sigma^2 - Lambda_A/ <= C2 n^{2/3}; (U3) fixed-margin score gap | PROVED; SF VERIFIED* (W5-VMASK row 12, U1 ERROR cosmetic); XF GAP (A-REV3; U1 false, RSS error); constant repaired R2 (VERIFIED A-REV6/A-REV8) | W3-PXN/PROOF.md; W5-VMASK/REPAIRS.md; A-REV3/REVIEW.md | [pos 423] [pos 742] | feeds: none |
| LM119 | PXN Lemma Lambda; population residuals of the LH components | lemma | (a) Lambda_A/n = lambda(A ∩ SV) + o_P(1) uniformly; (b) additivity over components; (c) explicit values lambda_i({j_a}) = G_i, lambda_i({j_b}) = beta^2(1-psi^2), lambda_i({j_a,j_b}) = 0, etc. | PROVED; SF VERIFIED (W5-VMASK row 13); XF GAP (A-REV3, A-REV6, A-REV8: Tr(c) range in part (a)) | W3-PXN/PROOF.md; W5-VMASK/REPORT.md; A-REV3/REVIEW.md | [pos 423] [pos 742] | feeds: none |
| LM120 | PXN design de-randomisation lemma; Lemma (design de-randomisation) | lemma | If Z_n = O_P(r_n) under P(./X=x_n) for every deterministic sequence x_n in A′_n with P(A′_n) -> 1 then Z_n = O_P(r_n) unconditionally | PROVED; SF VERIFIED (W5-VMASK row 18); XF VERIFIED (A-REV3) | W3-PXN/PROOF.md; A-REV3/REVIEW.md | [pos 423] [pos 742] | feeds: none |
| LM121 | PXN Lemma C1; Lemma C2; Lemma C3; CONC; Gaussian correlation concentration | lemma | C1 (cited): max/r_hat - Sigma/ <= C1 sqrt(log p/n) w.p. -> 1; C2: operator-norm of (R_hat_T - Sigma_T) <= /T/ max/r_hat - Sigma/; C3: finite sample moments converge a.s. | C1 cited (Bickel-Levina); C2, C3 PROVED | W3-PXN/PROOF.md; W5-VMASK/REPORT.md | [pos 423] [pos 742] | feeds: none |
| LM122 | PXNGAP Lemma Tr-J; Beta truncated moments any fixed dimension, polynomial families | lemma | (a) truncated moment bound for any j,u; (b) tail; (c) uniform tail over C n^D variables with j<=J, u<=n/4 at threshold 8(D+1)log n/n | PROVED (candidate, API-PXNGAP); no review | API-PXNGAP/PROOF.md; API-PXNGAP/REPORT.md | [pos 911] [pos 978] | feeds: none |
| LM123 | PXNGAP Lemma E; uniform score expansion on polynomial family of small sets | lemma | On a polynomial family of sets of size <= J with SE: (E1)-(E6) incl. /R_A/ <= kappa_E = 0.52/c_E + 1, c_E = sigma^2/(12(M+sigma^2)), RSS floor, and (E5) RSS approximation | PROVED (candidate, API-PXNGAP); no review | API-PXNGAP/PROOF.md; API-PXNGAP/REPORT.md | [pos 911] [pos 978] | feeds: none |
| LM124 | PXNGAP Lemma T; random-partition quantifier; transfer lemma | lemma | On {blocks = groups} every block object equals its group version; P(E) <= P(E~) + P(A_n^c); group statistics have unconditional laws, never conditioned on recovery | PROVED (candidate, API-PXNGAP); no review | API-PXNGAP/PROOF.md | [pos 911] [pos 978] | feeds: none |
| LM125 | PXNGAP Lemma LS; production local search on the lattice | lemma | Under D_S on Lat(S°)\{S0} (progress ties allowed): the search makes exactly c moves adding missing hubs, scores S0 iff ell >= c-1, certifies if (L) and ell >= c | PROVED (candidate, API-PXNGAP); no review | API-PXNGAP/PROOF.md | [pos 911] [pos 978] | feeds: relates to LS-score (M5/Theorem A card, Theme 7) |
| LM126 | VMASK Lemma B(i′); W5-VMASK R6 | lemma | For neutral l in a null/visible/a-group with U ⊇ U°_h: 1 - RSS_{U+l}/RSS_U ~ Beta(1/2, (n-2-/U/)/2) independent of (X_U, y) | stated and proved by W5-VMASK (author only); A-REV8: valid identity | W5-VMASK/REPAIRS.md; A-REV8/REVIEW.md | [pos 742] [pos 919] | feeds: none |
| LM127 | PART-L1; W7 Lemma 1; Corollary 1; pair-law representation; monotonicity in /r | /lemma | T = sqrt(k) r_hat/sqrt(1-r_hat^2) =_d (Z + a sqrt(W))/sqrt(V/k); P_r(/r_hat/>=t) nondecreasing in /r | PROVED (W7-PART); A-REV6: noncentral-t mixture proof correct | W7-PART/PROOF.md; A-REV6/PARTITION.md | [pos 717] [pos 796] | feeds: none |
| LM128 | PART-L2; W7 Lemma 2; Hotelling-density tail | lemma | P_r(r_hat >= t) <= a_n (1+/r/)^{3/2}(1-/r/)^-1 (1-t) Lambda_r(t)^{(n-4)/2} for t>=r, and the mirror bound | PROVED given Hotelling density (cited); XF GAP on constants (A-REV9) | W7-PART/PROOF.md; A-REV6/PARTITION.md | [pos 717] [pos 796] | feeds: none |
| LM129 | PART-L3; W7 Lemma 3; rotation invariance | lemma | For independent groups the cross correlations (r_hat_jk)_j are (<u_j, v>)_j with v uniform on the sphere, conditionally on (U_h, U_h′) [as written] | PROVED (W7-PART) as written; XF ERROR (A-REV6: literal full-vector conditioning false; condition on within-group Gram matrices) | W7-PART/PROOF.md; A-REV6/PARTITION.md | [pos 717] [pos 796] | feeds: none |
| LM130 | W7 Lemma A0; monotone heights and interleaving | lemma | Complete-linkage merge heights are nondecreasing; before the first bad merge each group runs its own dendrogram T_h; at the first bad merge the current clusters of h are the nodes with ht(A) < delta < pi(A) | PROVED (W7-PART, no ties); A-REV6 GAP (A0(c) quantifier) | W7-PART/PROOF.md; A-REV6/PARTITION.md | [pos 717] [pos 796] | feeds: via TH162 (S-BLOCKS K07) |
| LM131 | Lemma N; DIL-N; null score law (Beta(1/2,(n-2)/2)) | lemma | Gaussian null independent of (y,X_-l): r_ly^2~Beta(1/2,(n-2)/2) exactly; v3 table scores nulls as in pure noise at every signal scale | PROVED (author); XF VERIFIED* (A-REV9: VERIFIED under explicit joint independence; parenthetical implication ERROR) | O-DILUTE/THEORY.md §3; A-REV9/REVIEW.md | [pos 763] [pos 821] | feeds: none (campaign-only) |
| LM132 | Lemma L; DIL-Lw; common plug-in sigma^2 inflates every null | lemma | known-sigma^2 table exponent for nulls is chi2_1/(2(1-R^2)): inflation v/sigma^2 (7 at c=0.5, 25 at c=1); start fills to cap; F-DRAFT W1 needs in-sample BO | PROVED (identity); PROOF SKETCH (extreme-value consequence); SF none; XF none | O-DILUTE/THEORY.md §4 | [pos 763] | feeds: none (campaign-only) |
| LM133 | Lemma B-link; OMIX-Blink; link graph recovers linked pairs | lemma | thresholding max/r_jl/ at tau_n=3 sqrt(log p/n) recovers exactly the linked block pairs (exact Gram) | PROVED (exact Gram); PROOF SKETCH (iid) (author only) | O-MIX/REPORT.md | [pos 674] | feeds: none (campaign-only) |
| LM134 | Lemma S0; SIG-S0; variant invariance of locked identities under common sigma-hat^2 | lemma | T09,T11(iii),T12,T13,T21,T22(i)(ii)(iv),T31(i) hold verbatim; HPM ingestion must record log m(U); table-specific results must be re-derived | PROVED (author only) | F-SIGMA/REPORT.md | [pos 727] [pos 763] | feeds: none (campaign-only) |
| LM135 | Lemma S1 (F-SIGMA); SIG-S1; odds transfer under BO | lemma | under BO: log[pi0^C(S)/pi0^C(S')]=log[pi(S)/pi(S')]-nu[psi(u(S))-psi(u(S'))]; start odds <= e^{nu psi(u0)} posterior odds; W2 analogue (1-u0)Z^2/2; exact table increments | PROVED (author only; checked to 1e-13 by exact enumeration) | F-SIGMA/REPORT.md | [pos 727] [pos 763] | feeds: none (campaign-only) |
| LM136 | Lemma X+; Lemma X-plus; FAV-LemmaX; one-sided chain-free table bound | lemma | for U strictly in A with lambda_min(G_A)>=phi^2(n-1): BF(A)/BF(U)<=e^{kappa+}(n+1)^{-j/2}(1-X_{U,A minus U})^{-nu}; EXP' remainder <= O(1/n) from above | PROVED (author only); SF none; XF none | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 507] [pos 742] [pos 978] | feeds: none (campaign-only) |
| LM137 | Lemma X-; Lemma X-minus; FAV-LemmaXminus; matching lower bound | lemma | log BF(A)-log BF(U)>=-(j/2)log(n+1)-nu log(RSS_A/RSS_U)-kappa-, for deletions | PROVED (author only) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md | [pos 742] | feeds: none (campaign-only) |
| LM138 | Lemma B'; Lemma B-prime (W5-FAVIID); FAV-LemmaBp; exact Beta law for any group-union | lemma | X_{U,V}~Beta(/V//2,(m-/V/)/2) independent of (X_U,y) for fixed group-union Gamma, outside set W, V in Gamma minus S0; y any function of (X_S0,eps) | PROVED (author only) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md | [pos 742] | feeds: none (campaign-only) |
| LM139 | Lemma Tr'; FAV-LemmaTrp; truncated moment and truncation event | lemma | E[(1-X)^{-nu}1{X<=tau}]<=(1-tau)^{-e1}(m tau/2)^{j/2}/Gamma(j/2+1); truncation at tau_n has P->1 over N_n<=Cn^A variables | PROVED (author only) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md | [pos 742] | feeds: none (campaign-only) |
| LM140 | Lemma M (W5-FAVIID); Mittag-Leffler lemma; Lemma ML; FAV-LemmaM | lemma | if E[j! a_j]<=C0 (N xi)^j/Gamma(j/2+1) then E max_j (j! a_j)^{1/j}<=c_ML C0 N xi, c_ML=3.8311; removes the 2^B factor | PROVED (author only); c_ML=3.83114 confirmed independently by API-FAVIID | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REPORT.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| LM141 | Lemma S (W5-FAVIID); FAV-LemmaS; projection onto nearly orthogonal subspaces | lemma | //P_{A1+...+Ar} y//^2<=(1-(r-1)c)^{-1} sum //P_{Ai} y//^2 when pairwise //P_Ai P_Ak//<=c | PROVED (author only; API-FAVIID re-derived) | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| LM142 | Lemma G; FAV-LemmaG; partition-free good events (G1)-(G5) | lemma | SE on small sets, RSS floor, cross-group angles O(sqrt(log p/n)), uniform visibility, truncation, all with probability ->1 and not referring to the v3 partition | PROVED-UNDER (given [C1]) (author only); (G3) uniform Lipschitz step flagged | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| LM143 | Lemma P1'; FAV-LemmaP1p; blocks are unions of whole groups w.p. -> 1 | lemma | if within-group correlations are nonzero and group size <= B, P(Q_n)->1; S3/S4/S6: m=2 at B=14, m=3 at B in {15,16} | PROVED-UNDER (given [C1]) (author only); not on referee R6 list | W5-FAVIID/REPORT.md; W5-FAVIID/PROOF.md; API-FAVIID/REFEREE_HANDOFF.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| LM144 | Lemma 0(a),(c); Lemma0(a,c); monotonicity; certified repair gives S-hat=S0 | lemma | F strictly increases along the search path; certified stop at S0 gives S-hat=S0 up to ties without pi(S0)>1/2 | PROVED; SF VERIFIED (W3-VT37R); XF VERIFIED* (A-REV2, A-REV5) | W1-T37R/PROOF.md; W6-FIXREV2/STATEMENTS.md | [pos 355] [pos 570] | L-TA card (supplement of M5 Theorem HPM, K65); Lean T37Greedy.lean |
| LM145 | Lemma 0(b'); Lemma 0(b-prime); delivery inclusion | lemma | {S-hat=S0} subset {S0 in S_pre} or {F(S0)>F_pre} or tie; if S_c=S0 success iff M(S0)=bottom | PROVED (W6-FIXREV2); XF VERIFIED (A-REV5) | W6-FIXREV2/STATEMENTS.md; A-REV5/REVIEW.md | [pos 569] [pos 742] [pos 919] | L-TA card (supplement of M5 Theorem HPM, K65) |
| LM146 | Lemma 2 (T37); Lemma2-T37; lattice closure; superset reduction | lemma | Progress moves keep Lat(S) and R_{a,d} closed; under NA_d and TL_d S0 is a local max and extras are deleted first | PROVED; SF VERIFIED (W3-VT37R, 193 designs) | W1-T37R/PROOF.md; W3-VT37R/REPORT.md | [pos 355] [pos 370] | L-TA card (supplement of M5 Theorem HPM, K65) |
| LM147 | Lemma 3 (T37); Lemma3-T37; best truth addition under SE | lemma | If S not superset of S0 and lambda_min(R_{S u S0})>=phi0^2 then max_j delta^2 >= (n-1)phi0^4//theta_M//^2//M/ | PROVED; SF VERIFIED (W3-VT37R) | W1-T37R/PROOF.md | [pos 355] [pos 370] | L-TA card (supplement of M5 Theorem HPM, K65) |
| LM148 | Lemma T; tie lemma; D_S^lex | lemma | TD'_P iff (L) and all D_S^lex exactly; strict D_S implies D_S^lex; converse false with duplicate columns | PROVED (W6-FIXREV2); XF VERIFIED (A-REV5) | W6-FIXREV2/STATEMENTS.md; A-REV2/REVIEW.md | [pos 569] [pos 742] | L-TA card (supplement of M5 Theorem HPM, K65) |
| LM149 | Lemma NT; Corollary NT; null ties | lemma | Under G and joint non-degeneracy exact score ties between two models have probability zero, so D_S iff D_S^lex a.s. | PROVED (W6-FIXREV2, new); XF VERIFIED under nondegeneracy (A-REV5) | W6-FIXREV2/STATEMENTS.md; A-REV5/REVIEW.md | [pos 569] [pos 742] [pos 919] | L-TA card (supplement of M5 Theorem HPM, K65) |
| LM150 | PGD-L1.1; W3-PGD Lemma 1.1; move algebra | lemma | a_x(T)=<x~,r_T>^2///x~//^2; swap identity red(S-i+x)=a_x(S-i)-a_i(S-i); //r_A-r_B//^2<=2(...)+2(...) | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM151 | PGD-L1.2; W3-PGD Lemma 1.2; best truth addition residual bound | lemma | max_j a_j(S)>=(phi0^2/m)//r_S//^2>=N phi0^4 theta_min^2 | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM152 | PGD-L1.3; W3-PGD Lemma 1.3; ERC controls null leakage | lemma | a_l(S)<=ERC(S,l)^2 max_j a_j(S) | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM153 | Lemma A'; PGD-LA'; Theorem A for progress-closed regions | lemma | TD'_P on a progress-closed region gives progress paths and certified return from every centre if l>=Phi_max | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM154 | Lemma S; PGD-LS; superset states; H1; H2; H3 | lemma | Under (H1) d<=1, (H2) (/D/+1)^{d-1}<=n^{1/2-eps} or (H3) LD-flat with star, (L) and D_S at S0 u P hold w.p.->1 | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md; W5-VPGD/REPAIRS.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM155 | Lemma LD; PGD-LLD; local/far decomposition; LD-flat | lemma | /Z_{S0 u T,l}/<=(/Z_{A,l}/+rho //P_V e///sigma)/sqrt(1-rho^2) | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM156 | Lemma P5; PGD-P5; Gram-perturbation stability | lemma | lambda_min, Delta_T and PGD(eta)->PGD(eta/2) are stable under Gram perturbation of size eps | PROVED; SF VERIFIED* (W5-VPGD; LD-flat sentence GAP repaired as LM161) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM157 | PGD-LR; W3-PGD Lemma R; score representation | lemma | F(T)=Psi-pen(/T/)-nu log RSS_T+zeta_T with /zeta_T/<=C0 on an event of probability ->1 | PROVED; SF VERIFIED (W5-VPGD; ridge bookkeeping flagged for second look) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM158 | PGD-LG; PGD-LQ; W3-PGD Lemma G; Lemma Q; population-gap comparisons | lemma | Population gaps g>=gamma_n with //r_A-r_B//^2<=C1 g imply F(A)>F(B) for all pairs w.p.->1 | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM159 | PGD-LU; W3-PGD Lemma U; supersets of S0; chain rule | lemma | For S0 subset A subset B, F(B)-F(A)<=(1/2)W(B/A)(1+delta')-sum c_k+2C0 (name collision with W2-PREM Lemma U) | PROVED; SF VERIFIED (W5-VPGD) | W3-PGD/PROOF.md | [pos 353] [pos 550] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM160 | union-model projection bound; V37 R5 repaired bound; repaired C2 bound | lemma | //(P_A-P_B)mu//^2<=2(n-1)[(Delta_A-Delta_U)+(Delta_B-Delta_U)], U=A u B | PROVED (elementary, W3-VT37R); empirical ratio <=0.963 | W3-VT37R/REPAIRS.md | [pos 370] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM161 | VPGD-R3; LD-flat stability | lemma | /rho-hat^2-rho^2/<=8 eps/phi0^8 for Gram perturbation eps<=phi0^2/2 | PROVED (W5-VPGD); no second check | W5-VPGD/REPAIRS.md | [pos 507] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| LM162 | Lemma F; LemmaF; first-failure bound | lemma | Union over labels of sup of failure probability, if non-failing steps stay in the family | PROVED (candidate); SF GAP (closure hypothesis) fixed by F'; XF VERIFIED standalone, W1's use in B2 GAP repaired (A-REV1) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/PROOF.md | [pos 296] [pos 370] | feeds: none (campaign-only) |
| LM163 | Lemma F'; LemmaF'; Lemma F-prime; F' | lemma | First-failure union bound with no closure hypothesis via the permutation bijection | PROVED (authored by W2-VT24G; no SF); XF VERIFIED (A-REV1) | W2-VT24G/PROOF.md; A-REV1/REVIEW.md | [pos 370] [pos 470] | feeds: none (campaign-only) |
| LM164 | Lemma O; LemmaO; order facts | lemma | Order facts for a uniform label permutation: first-of-set probability, P(l before e)=1/2, E prod u_j = integral | PROVED (candidate); SF VERIFIED; XF VERIFIED (A-REV1) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; A-REV1/REVIEW.md | [pos 296] [pos 470] | feeds: none (campaign-only) |
| LM165 | Lemma C; LemmaC; binomial domination | lemma | Adapted indicators with conditional success >= c satisfy P(sum<k) <= P(Bin(H,c)<k) <= k(1-c)^floor(H/k) | PROVED (candidate); SF VERIFIED (exact rational check); XF VERIFIED (A-REV1) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md | [pos 296] [pos 370] [pos 470] | feeds: none (campaign-only) |
| LM166 | Lemma P; LemmaP; first-change progress; multi-target Lemma P; W6F1-LemmaP | lemma | Exact first-change progress probability P*(x) and polynomial lower bound s_min(/C//k)[1-Q/(k+1)] | PROVED (candidate); SF VERIFIED; XF VERIFIED* (A-REV1: multi-target sentence GAP, explicit version supplied); repaired W6-FIXREV1; XF VERIFIED (A-REV5) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W6-FIXREV1/CONSOLIDATED.md; A-REV1/REVIEW.md | [pos 296] [pos 370] [pos 470] [pos 742] [pos 919] | feeds: none (campaign-only) |
| LM167 | Lemma E; LemmaE | lemma | P_Y(exit) >= o*(Y)[1-Q_T/(B+m+d+4)]/(B+m+d+3) at boundary states of R_d | PROVED (authored by W2-VT24G; no SF); XF VERIFIED (A-REV1); two statistical limits (o*->1, Q_T->0) PROOF SKETCH | W2-VT24G/PROOF.md; A-REV1/REVIEW.md | [pos 370] [pos 470] | feeds: none (campaign-only) |
| LM168 | Lemma U; Lemma U(F); LemmaU-PREM; C3-upper; W6F1-LemmaU'; uniform log-BF expansion | lemma | Uniform expansion log BF(T+l)/BF(T) = -1/2 log(n+1) - nu log(1-x) + R, /R/<=kappa_n, over a polynomial family; kappa_n decreasing to 0.51/c_E | PROVED (author only W2-PREM); XF VERIFIED* (A-REV1: finite statement VERIFIED, limit 0.52 ERROR repaired to 0.51; A-REV2 VERIFIED on budgeted family; A-REV5 VERIFIED, printed arrow ERROR) | W2-PREM/PROOF.md; W6-FIXREV1/CONSOLIDATED.md; A-REV1/REVIEW.md; A-REV2/REVIEW.md; A-REV5/REVIEW.md | [pos 424] [pos 570] [pos 742] | feeds: none (campaign-only) |
| LM169 | Lemma S (shift); Lemma S (shift at a stopping time); stopping-time shift lemma | lemma | After an a.s. finite stopping time of an iid U(0,1) stream the shifted stream is iid and independent of the past | PROVED (author only W2-PREM) | W2-PREM/PROOF.md | [pos 424] | feeds: none (campaign-only) |
| LM170 | Lemma S'; Lemma S (ESS share); W6F1-LemmaS'; ESS share lemma | lemma | Weighted share of an index set >= max{0, f - sqrt(f(1-f)(1/e-1))}; two-level equality only for f>1-e | Original Lemma S: PROVED, SF tight (W3-VT38E), XF inequality VERIFIED, attainment ERROR (A-REV1); repaired Lemma S': PROVED (W6-FIXREV1); XF VERIFIED (A-REV5) | W6-FIXREV1/CONSOLIDATED.md; W1-T38E/PROOF.md; A-REV1/REVIEW.md; A-REV5/REVIEW.md | [pos 470] [pos 570] [pos 742] [pos 919] | feeds: none (campaign-only) |
| LM171 | Lemma CMP; comparison lemma | lemma | Z^2_{W,l} <= Z^2_{S0 ∪ P1,l} + eps_n under the partner graph PG | PROVED (author only W2-PREM); not independently certified (A-REV5) | W2-PREM/PROOF.md; A-REV5/REV1_CHECK.md | [pos 424] | feeds: none (campaign-only) |
| LM172 | LemmaA-T38E; Lemma A; [LA] | lemma | gamma_phi(S')/gamma_phi(S) = rho0^{1-phi} rho1^{phi} <= max(rho0,rho1); Gibbs change probability <= max{kappa_0,kappa_1} uniformly in phi | PROVED (W1-T38E); SF VERIFIED (W3-VT38E, 2,048,000 cases) | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | feeds: none (campaign-only) |
| LM173 | LemmaB-T38E; Lemma B | lemma | Structured bridge mass: q_phi(R_d^c) <= theta/(1-theta) + max{pi0(B),pi(B)}/[min{pi0(x),pi(y)}max{pi(x),pi0(y)}] | PROVED (deterministic) (W1-T38E); SF VERIFIED (W3-VT38E, 3,255 cases); asymptotic reading PROOF SKETCH | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | feeds: none (campaign-only) |
| LM174 | LemmaS-ineq; LemmaS-attain; Lemma S; Lemma S′; Lemma S'; Lemma ESS; ESS share lemma | lemma | Weights with ESS >= eH: any subset of fraction f has weighted share >= max{0, f - sqrt(f(1-f)(1/e - 1))}; attained only for 1-e < f < 1 | inequality PROVED (W1-T38E), SF VERIFIED (W3-VT38E), XF VERIFIED (A-REV1); 'attained by two-level weights' on the full domain ERROR (A-REV1); Lemma S' PROVED (W6-FIXREV1) | W1-T38E/PROOF.md; W6-FIXREV1/CONSOLIDATED.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] [pos 557] [pos 570] | feeds: none (campaign-only); not the K63 Lemma S |
| LM175 | SHARE-PD; Lemma PD; start mass x fitness = posterior | lemma | log gamma0(S) + d(S) = F(S) - log m(empty); an outsider takeover must beat the occupied W-states in the posterior by omega nats | PROVED (W4-SHARE); SF VERIFIED* (W5-B2ENV: identity VERIFIED, takeover-needs-premises is heuristic) | W4-SHARE/PROOF.md; W5-B2ENV/REFEREE.md | [pos 371] [pos 742] | feeds: none (campaign-only) |
| LM176 | OBG-LemmaR; Lemma R; Lemma MF; multi-flip round lemma | lemma | From x one round at phi scores z = x Δ Λ with probability >= P(O)(1-Dep_phi)_+ alpha_phi^{/Λ/-1}; D2's step is /Λ/=1 | PROVED (author only; confidence 0.97) | O-BGIBBS/REPORT.md | [pos 594] [pos 748] | feeds: none (campaign-only) |
| LM177 | B2E-LemmaOF; Lemma OF; orthogonal factorisation of the discrepancy | lemma | If S meets only mutually orthogonal blocks: d(S) = nu[-log(1 - sum e_h) + sum log(1 - e_h)], monotone in each e_h, and 0 <= d(S') - d(S) <= nu(Q_S - Q_{S'})/(2b0 + Q_{S'}) | PROVED (author only) | W5-B2ENV/PROOF.md | [pos 742] | feeds: none (campaign-only) |
| LM178 | B2E-L2.1; B2E-L2.2; Lemma 2.1; Lemma 2.2; start aggregation and tails on LH | lemma | LH start aggregation rates q, D_b = O_P(g n^{-1/2}), e_n exponentially small; start tails pi0(S ⊇ S°, >= k extras) <= 2e^s (eq)^k etc. | Lemma 2.1 PROVED (given E-T1, E-T6); Lemma 2.2 PROVED (author only) | W5-B2ENV/PROOF.md | [pos 742] | feeds: none (campaign-only) |
| LM179 | B2E-LemmaJ; Lemma J; junk and proxy inclusion odds | lemma | sum of neutral inclusion odds eps_n = O_P(v_max 4^g sqrt(log n/n)); single/proxy eps'_n = O_P(v_max 4^g log n/sqrt n) on N' | PROVED-UNDER (given U1-U3, author); XF VERIFIED* (A-REV7, eta_n corrected to O(n^{-1/3}+sqrt(log n/n))); API-VSTAB item 6 VERIFIED | W5-B2ENV/PROOF.md; A-REV7/REVIEW.md; API-VSTAB/REPORT.md | [pos 742] [pos 919] [pos 978] | feeds: none (campaign-only) |
| LM180 | B2E-LemmaT; Lemma T; truth retention; hub gain (G) | lemma | Under STAB-LH, gamma_i(V-t)/gamma_i(V) <= 2p e^{-c6 n} and gamma_i(V-t+l)/gamma_i(V) <= e^{-c6 n} for V in N', t in S°, i in {0,1}; (G) hub gain needs no hypothesis | PROVED-UNDER STAB-LH (author); deletion part and (G) VERIFIED within A-REV7 and API-VSTAB (items 9, 11) | W5-B2ENV/PROOF.md; A-REV7/REVIEW.md; API-VSTAB/REPORT.md | [pos 742] [pos 919] [pos 978] | feeds: none (campaign-only) |
| LM181 | B2E-LemmaR1; Lemma R1; one-round repair at phi=1 | lemma | From any x in N, P_x(S0 scored in one round at phi=1) >= c0(x) - r_n, c0(x) = g^{-c_x}/C(/Λ_x/+B+2,B+2) (order event) | PROVED-UNDER (deletion part of STAB-LH) (author); XF VERIFIED* (A-REV7, c_* = g^{-c}/C(2cg+19+B+2,B+2)); API-VSTAB item 9 VERIFIED | W5-B2ENV/PROOF.md; A-REV7/REVIEW.md; API-VSTAB/REPORT.md | [pos 742] [pos 919] [pos 978] | feeds: none (campaign-only) |
| LM182 | FSH-L1.2; Lemma 1.2; exit bound for the superset class | lemma | For W = W(S°): K_phi(x, Omega\W) <= sum_j max{kappa0,kappa1}(x,j) + (B+1) sum_j max{rho0,rho1}(x,j) + pi0(Omega\W) | PROVED (author run); XF GAP (A-REV7, A-REV6: pointwise display is not the proved bound; use suprema over intermediate states and Hastings factor) | F-SHARE/REPORT.md; F-SHARE/PROOF.md; A-REV7/REVIEW.md | [pos 748] [pos 919] | feeds: none (campaign-only) |
| LM183 | FSH-L3.1; Lemma 3.1; unit structure | lemma | LH exact Gram: the unit residual u_{x,j} depends on x only through x ∩ unit(j) and is orthogonal to columns of other units | PROVED (author run; no verifier) | F-SHARE/PROOF.md | [pos 748] | feeds: none (campaign-only) |
| LM184 | FSH-L3.2; Lemma 3.2; hub gain | lemma | For x in W(S°), b in M\x: delta_{x,b} = theta_b //(I-P_x)x_b// and delta^2 >= theta_b^2 (n-1) lambda_min(Sigma_LH) | PROVED (author run; no verifier) | F-SHARE/PROOF.md | [pos 748] | feeds: none (campaign-only) |
| LM185 | FSH-L3.3; Lemma 3.3; start keep odds | lemma | kappa0(x,j) <= 2p e^{-c1 n} uniformly over x in W(S°), j in S°; swap-out odds <= 2p e^{-cK c1 n} | PROVED-UNDER (given W1-EXP Thm 1 and PK) (author run) | F-SHARE/PROOF.md; F-SHARE/REPORT.md | [pos 748] | feeds: none (campaign-only) |
| LM186 | FSH-L3.4; Lemma 3.4; posterior keep and swap margins | lemma | F(x)-F(x-j) >= c2 n and F(x) - max_l F(x-j+l) >= c2 n uniformly over x in W(S°), j in S° | PROOF SKETCH (author run); XF ERROR (A-REV7: displayed Schur increment wrong by a factor, repairable) | F-SHARE/PROOF.md; A-REV7/REVIEW.md | [pos 748] [pos 919] | feeds: none (campaign-only) |
| LM187 | GP(d) implies TD′(R_d,l); GP(d) => TD'; W3-VT38E Section 3.5 | lemma | Under GP(d) with l+1 >= s0+d the production local search from any S in R_d reaches or flip-neighbours S0 and scores it | PROVED (W3-VT38E, fills a step W1 states without proof) | W3-VT38E/REPORT.md | [pos 370] | feeds: TD' (theme 4); supplement |
| LM188 | Lemma RO; LemmaRO; run/output split; RO | lemma | Under GUARD, O = G^c ∩ O-bar and for a reported output g with potential version g-bar: 1_O g = 1_O g-bar; P(O, g in A) <= P(O-bar, g-bar in A); P(O^c ∪ {g not in A}) <= P(G) + P(O-bar^c) + P(O-bar, g-bar not in A); E[1_O g] <= E[1_{O-bar} g-bar] for g-bar >= 0 on all of O-bar; no equality conditional on O | PROVED; SF VERIFIED (W5-LOCKBOOK 'CORRECT'); XF VERIFIED for statistical outputs with nonnegative potential values (A-REV4 BOOK_CHECK); VERIFIED* conditional implication (A-REV6, candidate repair R1); registry LemmaRO 'PROVED (SF: VERIFIED; XF: VERIFIED*)' | W2-BOOK/PROOF.md s0.2; W2-BOOK/REPORT.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/BOOK_CHECK.md; A-REV6/BOOK.md R1 | [pos 328] [pos 342] [pos 696] [pos 742] [pos 807] | S-OUT (K77 Lemma RO, K78); M1 and M5 premises |
| LM189 | LS-score; Lemma LS-score; Lemma LS | lemma | If D_S holds on Lat(C0) ∩ {Phi >= 2}, l >= Phi(C0)-1, and C0 != S0 or the centre is emitted, the production local search from C0 scores S0 (certification not needed); move count max{Phi(C0)-1,0} | PROVED; SF VERIFIED (W5-VMASK row 20); XF VERIFIED* (A-REV8: scoring VERIFIED; move count 'at most Phi(C0)-1' ERROR at C0=S0, repaired to max{Phi(C0)-1,0}) | W4-T38FULL/T38_PROOF.md s3.1; A-REV8/REVIEW.md; W5-VMASK/REPORT.md | [pos 364] [pos 463] [pos 843] [pos 919] | M5 (a) Theorem A / LS-score (K65); Lean T37Greedy/T37Lattice (theme 13) |
| LM190 | Lemma M; LemmaM; Lemma SC; uniform score comparison under population margins | lemma | Under G, p<=n^A, //mu//^2<=Mn, k>=s0, lambda_min(R_A)>=phi0^2, margin m_n >= M_n sqrt(log n/n), M_n -> inf: with probability -> 1, simultaneously for all pairs (A,B) with Delta(B)-Delta(A) >= m_n, F(A) > F(B), quantitatively F(A)-F(B) >= M_n sqrt(n log n)/(4C_R) - 2k log(2p(n+1)) - c0 | PROVED; SF VERIFIED (W5-VMASK row 21); XF VERIFIED (A-REV8: including uniformity and standardisation) | W4-T38FULL/T38_PROOF.md s3.2; W5-VMASK/REPORT.md; A-REV8/REVIEW.md | [pos 364] [pos 463] [pos 843] [pos 919] | M5 (b1-LH) key ingredient (K69) |
| LM191 | GUARD; IMPL-GUARD; IMPL-GUARD'; stop-only coupling; Lemma IMPL-GUARD | lemma | Implementation fact: every resource check either does nothing or ends the fit with status resource_limit; no check consumes a random number or changes a setting, the inherited store or the score cache; off resource_limit all statistical outputs equal R-bar's; caveats G1 (stopped fit returns incomplete HPM: need G in U), G2 (partial_final archive fields), G3 (non-status aborts), G4 (shared guard) | PROVED by code reading (W5-LOCKBOOK; read, not run); IMPLEMENTATION FACT supported by two cross-family code readings (A-REV5, A-REV8); API-AUDIT HOLDS (executed: bitwise equal to the guard-free pipeline on 10/10 fits); literal 'every reported output equals' ERROR (A-REV4, A-REV8 E2) | W5-LOCKBOOK/AUDIT.md s1; API-AUDIT/REPORT.md s2; W2-BOOK/PROOF.md s0.1; A-REV4/BOOK_CHECK.md; A-REV8/REVIEW.md | [pos 328] [pos 463] [pos 742] [pos 906] [pos 1009] | S-OUT (K77, K78 GUARD-W); M5 premise GUARD-W |
| LM192 | OUT; IMPL-OUT; Lemma IMPL-OUT | lemma | Implementation fact: evidence, lower bound, PIPs and MPM are written only when status is completed/exact; no failure mode reports a partial reported estimate (partial values only in labelled archive fields; the reported MPM is uncapped) | PROVED by code reading (W5-LOCKBOOK); not separately cross-family reviewed (registry: IMPLEMENTATION FACT - unaudited at the time) | W5-LOCKBOOK/AUDIT.md s2 | [pos 463] [pos 742] | S-OUT; M4 output clauses (K78) |
| LM193 | SR; IMPL-SR; Lemma IMPL-SR; scoring rule of step_gibbs | lemma | Implementation fact: every Gibbs step scores both feasible configurations before the accept draw; every swap/independence proposal is evaluated before acceptance; every evaluated model reaches the HPM running best; so the potential scored set S-bar is table models + inherited + all evaluated + final-search scans | PROVED by code reading (W5-LOCKBOOK); HQ SR_AUDIT (HQ read; Felipe delegated); API-AUDIT HOLDS (read as both feasible configurations); A-REV7 'substantively correct' (blanket 'no call passes emit=false' too strong) | W5-LOCKBOOK/AUDIT.md s3; campaign/HQ/SR_AUDIT.md; API-AUDIT/REPORT.md s1 | [pos 526] [pos 541] [pos 463] [pos 906] | M5 premise SR; S-OUT |
| LM194 | IMPL-STREAM; Lemma IMPL-STREAM; Lemma STREAM; Lemma-STREAM; IND-T stream premise | lemma | Sequential single-stream-per-island reading implies, under EX-S, conditional independence of particles' within-round and H-round trajectories given the boundary sigma-field (strong Markov argument at stopping times) | IMPL-STREAM PROVED by code reading; Lemma STREAM PROVED (under EX-S) by W5-LOCKBOOK, author only (registry SF none, XF none); API-AUDIT item 5 HOLDS | W5-LOCKBOOK/AUDIT.md s4; API-AUDIT/REPORT.md s5 | [pos 463] [pos 742] [pos 906] | S-OUT (K86); M1/M5 premise IND-T |
| LM195 | IMPL-LS; Lemma IMPL-LS; scan-before-limit; scan before limit | lemma | Every local-search pass completes a full scan of the current centre before the move limit is tested; all scanned models are scored and reach the HPM; at most l moves and l+1 scans, each at most p + k(p-k) evaluations | PROVED by code reading (W5-LOCKBOOK); API-AUDIT HOLDS; A-REV8 code reading consistent | W5-LOCKBOOK/AUDIT.md s5; API-AUDIT/REPORT.md s4 | [pos 463] [pos 906] [pos 919] | S-CERT (K64 scan semantics) |
| LM196 | IMPL-EMIT; emit_centre; LS0-EMIT; Finding (LS0 / emit_centre) | lemma | LS0 must set emit_centre = true (first evaluation offered to the HPM): with emit_centre=false a fresh centre is cached unoffered and every later cache hit is also not offered, so the reported HPM can fail to be the best scored model | PROVED by code reading (W5-LOCKBOOK); API-AUDIT: HOLDS in the O-LS0 export only, production v3 has no LS0; IMPLEMENTATION OBLIGATION (LS0 now part of the method); A-REV1 s6 and A-REV8 agree | W5-LOCKBOOK/AUDIT.md s5; API-AUDIT/REPORT.md s3; A-REV1/REVIEW.md s6; A-REV8/REVIEW.md | [pos 370] [pos 463] [pos 906] [pos 919] | M5 premise e4 / OP-LS0 (N2(c), N3) |
| LM197 | IMPL-T; IMPL-LOOP; Lemma IMPL-T | lemma | Under EX-A the pilot has at most T_e stages, every successful grid at most T_e intervals; per tier one pilot, at most l diagnostic iterations of 4 islands, at most l+1 V rebuilds; at most two tiers; one final run of 4 islands and one final local search | PROVED by code reading (W5-LOCKBOOK); not cross-family reviewed | W5-LOCKBOOK/AUDIT.md s6 | [pos 463] [pos 742] | supplement (T32(i) count) |
| LM198 | T26-Lemma1; W2-T26 Lemma 1; Delta identity | lemma | If S0 in Omega then Delta_n=max{1-pi0(S0),1-pi(S0)}<1 | PROVED; SF CORRECT/VERIFIED (W5-LOCKBOOK, grid check 66/66); XF VERIFIED (A-REV4) | W2-T26/PROOF.md; A-REV4/REVIEW.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] [pos 919] | underlies TH295/TH296; W5-FAVIID C2 |
| LM199 | T26-Lemmas2-3 (Lemma 2); W2-T26 Lemma 2; departure from the truth | lemma | rho-bar<=sum_e K_e(S0,Omega minus S0)<=(B+3)u_pi and exactly rho-bar=1-prod_e[1-K_e(S0,Omega minus S0)] | PROVED; SF CORRECT/VERIFIED (W5-LOCKBOOK); XF VERIFIED (A-REV4) | W2-T26/PROOF.md; A-REV4/REVIEW.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] [pos 919] | underlies TH295, TH300, TH313 |
| LM200 | T26-Lemmas2-3 (Lemma 3); W2-T26 Lemma 3; round-start occupancy | lemma | E_C Bbar_r<=(1/4) sum_h E_C g_{r,h} + rho-bar: occupancy re-controlled at each measured-round start via T12(i.b), removing the (L+4) factor | PROVED; SF CORRECT/VERIFIED (W5-LOCKBOOK; redundancy "CORRECT, and material"); XF VERIFIED (A-REV4); independently re-derived by A-DRAFT (D5,D8) | W2-T26/PROOF.md; A-REV4/REVIEW.md; A-DRAFT/REPORT.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] [pos 919] | supplement L-T12 (T26-Lemmas2-3 XF-VERIFIED); underlies TH295, TH300 |
| LM201 | O-PW2 Lemma 1; q_{t-1}(Q_t f)=q_t(f) | lemma | q_{t-1}(Q_t f)=q_t(f) hence q_s(h_{s,T})=1 | PROVED (candidate); XF helper VERIFIED (A-REV9 MASKED_PW2_CHECK) | O-PW2/REPORT.md; A-REV9/MASKED_PW2_CHECK.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | feeds TH316 |
| LM202 | O-PW2 Lemma 2; Fact F; weighted unbiasedness | lemma | W_t=W_{t-1} qhat_{t-1}(g_t), W_t mu_t(f)=E[W_t qhat_t(f)/F_{t-1}], E[W_t qhat_t(f)]=q_t(f); given F_{t-1} the N particles of stage t are iid mu_t | PROVED (candidate); XF helper VERIFIED (A-REV9 MASKED_PW2_CHECK) | O-PW2/REPORT.md; A-REV9/MASKED_PW2_CHECK.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | feeds TH316, TH317, TH309 |
| LM203 | API-MASKZPIP Lemma J; full-space ESS grid cannot jump a crossing | lemma | If chi2(q_t//q_{t-1})<=chi-bar then q_t(A)^2<=(1+chi-bar) q_{t-1}(A) for every A | PROVED (candidate); not reviewed | API-MASKZPIP/PROOF.md | [pos 909] [pos 911] [pos 957] [pos 978] | feeds TH311; diagnostic remark C4 |
| LM204 | Lemma M; OCERT-LemmaM; Lemma MON (proposed rename); O-CERT Lemma M (monotonicity of the score ingredients) | lemma | As S grows Q_S decreases and D_S increases (and w non-increasing on {0..K}); Q_S = y'y/(n+1) + n/(n+1) y'(I+(n+1)M_S)^-1 y; D_S = det(I+(n+1)M_S)/det(I+M_S) | PROVED; SF VERIFIED (O-VCERT: 0 violations in 476,160 exhaustive pairs); XF VERIFIED in exact arithmetic (A-REV9); LOCKABLE_v2 | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 575] O-CERT launch; [pos 706] result; [pos 729] O-VCERT launch; [pos 763] O-VCERT result; [pos 830] A-REV9 launch; [pos 917] [pos 919] reviews folded into registry | S-CERT K73 (B&B), K05 (superset bound); status cell "OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9))" |
| LM205 | Lemma 1 (API-N200); N200 deterministic inclusions | lemma | On the output event: posterior miss implies S-dagger != S0; search miss implies S0 not scored; S-dagger scored implies S-hat = S-dagger; S-dagger != S0 implies pi(S0) <= 1/2 | PROVED (author API-N200 only; no SF, no XF) | API-N200/PROOF.md; API-N200/REPORT.md | [pos 906] launch; [pos 911]; [pos 978] result | M5 Theorem HPM K72 (composition at every n) |
| LM206 | Lemma T33-M; T33(i) generalised; W7-SEC T33-M | lemma | I <= A_S <= (1+tr G_S) I and I <= H_S <= (1+(n+1) tr G_S) I, also with duplicate columns; exact Cholesky never fails | PROVED (author W7-SEC only); A-REV9 deferred | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md | [pos 711] launch; [pos 717]; [pos 742]; [pos 748]; [pos 754] | none (supplement remark; theme-0 T33) |
| LM207 | Lemma T33-Q; Q_S >= y'y/(n+1) | lemma | Q_S >= y'y - (n/(n+1))//P_S y//^2 >= y'y/(n+1) for every S and any real data; the non-negative Q fallback never fires in exact arithmetic for n+1<10^8 | PROVED (author W7-SEC only); A-REV9 deferred; independently equivalent to O-VCERT corollary of Lemma M(d) | W7-SEC/PROOF_T33.md; O-VCERT/REPORT.md | [pos 711] launch; [pos 729] O-VCERT; [pos 742] | none |
| LM208 | Lemma 0 (O-SWAP); OSWAP-L0; projection approximation PA | lemma | Q_S = Q~_S + eta_S with Q~_S = E_S + W_S/(n+1) and eta_S in [0, n W_S/((n+1)((n+1)lambda_min+1))]; defines PA used by Props 1-3 | PROVED (author O-SWAP only); LOCKABLE_v2 3e: no verification at all | O-SWAP/REPORT.md | [pos 577] launch; [pos 578]; [pos 594]; [pos 742] finished | none (campaign-only) |
| LM209 | O-WSTAB Lemma 0; Lemma WS0; fit-fraction form of the score | lemma | 0<=x_S<1 and log BF(S)=-1/2 log D_S - nu log(1-x_S) | PROVED (Woodbury; used throughout; SF/XF checked in passing) | O-WSTAB/PROOF.md | [pos 492] | feeds all of O-WSTAB; no final card |
| LM210 | Lemma Lambda; cumulant function of d | lemma | Lambda(phi)=log E_{pi0}e^{phi d} is real-analytic convex with Lambda′=E_{q_phi}d, Lambda″=Var_{q_phi}d | PROVED (trivial) | O-WSTAB/PROOF.md | [pos 492] | feeds TH348, TH360 |
| LM211 | Lemma WS5.1; leakage decomposition | lemma | P_{C_b}mu = X_{U*_b} theta~_b + rho_b with rho_b orthogonal to span X_{U*_b}, //rho_b//^2=Lambda_b | PROVED (author) | O-WSTAB/PROOF.md | [pos 492] | feeds TH352 |
| LM212 | Lemma W2 (O-WSTAB); exact dilution form; kappa G <= LR <= kappa G/(1-y) | lemma | Under BO LR=nu[g(y)-g((1-kappa)y)] and kappa G<=LR<=kappa G/(1-y), kappa the realised dilution fraction | PROVED (author); SF verified (CHECK_SEP_W, F5 exposition); replaces F-DRAFT W2 (ERROR, A-REV4) | O-WSTAB/REPORT.md; O-WSTAB/review/CHECK_SEP_W.md | [pos 616] [pos 748] | feeds LM213 (S2), TH362 |
| LM213 | Lemma SEP; separable domination under ORTH | lemma | l_{S0}(w)<=sum_{j in S0}log(1+2p sqrt(n)e^{-nu x_j})-(s0+1)log(1-q(w)) when q(w)<1 | PROVED; SF verified (CHECK_SEP_W); XF A-REV9 checked its proof steps within the W(a)-(f) verdict | O-WSTAB/REPORT.md; O-WSTAB/review/CHECK_SEP_W.md | [pos 748] | feeds TH362(b)(d) |
| LM214 | Lemma SEP prime; Lemma SEP′; integral form | lemma | l_{S0}(w)<=sum log(1+2p sqrt n e^{-nu x_j})+log[(1/s0!)int t^{s0}e^{-t}prod(1+t c_j(w)/p)dt] without q(w)<1 | PROVED (author); not reviewed (CHECK_SEP_W; not in A-REV9 list) | O-WSTAB/REPORT.md | [pos 748] | feeds TH362(g) |
| LM215 | HT heavy-tail lemma; (HT) | lemma | Sum_N e^{aZ_j^2/2}<=m^{a-1}Sum_N e^{Z_j^2/2}=m^a O_P(sqrt(log m)) for all a>=1 simultaneously on max Z^2<=2 log m | PROVED (author; used in verified W(a),(b)) | O-WSTAB/REPORT.md | [pos 748] | feeds TH362 |
| LM216 | O-STAGES Lemma 0; Lemma RS; STG-L0; reference-state identity | lemma | rho_V(u,v)=q_u(R)q_w(R)/q_v(R)^2 for every R in V, w=2v-u; Phi=ell_R(u)+ell_R(w)-2ell_R(v) | PROVED (author; SF none; XF none; FLAG AUTHOR-ONLY); same identity as TH360(ii) | O-STAGES/REPORT.md | [pos 733] [pos 748] | feeds M7 Theorem STG (Lemma RS key lemma; K26) |
| LM217 | O-STAGES Lemma 1; STG-L1; monotonicity of the ESS criterion | lemma | Phi_V is nondecreasing in v and nonincreasing in u; bisection finds the exact frontier; v*(u) nondecreasing | PROVED (author; SF none; XF none) | O-STAGES/REPORT.md | [pos 733] [pos 748] | feeds M7 (a) (K26) |
| LM218 | Halving count; N(w-bar) | lemma | Minimal number of intervals with 2v-u<=w-bar is max{1,ceil(log2(w-bar/(w-bar-1)))} | PROVED (author) | O-STAGES/REPORT.md | [pos 733] | feeds TH366 |
| LM219 | O-STAGES Lemma P; Lemma PERT; STG-P; perturbation | lemma | /F-F2/<=eta0 on [0,2] implies /Phi_F-Phi_F2/<=4 eta0 and T*_{F2}(c+4eta0)<=T*_F(c)<=T*_{F2}(c-4eta0) | PROVED (author; SF none; XF none) | O-STAGES/REPORT.md | [pos 733] | feeds TH369 |
| LM220 | API-T26BUD Fact 1; monotonicity of rho_V and pilot ESS | lemma | rho_V(u,.) and the pilot population ESS are monotone; passing set of a bisection is an interval | PROVED (candidate) | API-T26BUD/PROOF.md | [pos 906] | feeds TH370 |
| LM221 | API-T26BUD Fact 2; reference decomposition | lemma | -log rho_V(u,v)=L_V(u)+L_V(2v-u)-2L_V(v)<=L_V(u)+L_V(2v-u), L_V=log(1+R_V) | PROVED (candidate); same as LM216 | API-T26BUD/PROOF.md | [pos 906] | feeds TH370, TH371 |
| LM222 | API-T26BUD Lemma P; pilot step | lemma | A pilot stage advances by >=min{1-phi,a/D-2^-60} and >=1/T_e; N^pil<=1+ceil(Dbar/a) | PROVED (candidate) | API-T26BUD/PROOF.md | [pos 906] | feeds TH372; M7 (c′) uses a different pilot extension |
| LM223 | Frobenius monotonicity lemma (WS4) | lemma | For symmetric E and 0<=X<=Y (Loewner), tr(EXEX)<=tr(EYEY) | PROVED inside WS4 | O-WSTAB/PROOF.md | [pos 492] | feeds TH351 |
| LM224 | Lemma GU-1; SEP-GU1; population descent | lemma | For T subset R with Delta(T)>0: Delta(T) >= phi0^2 //theta_{M_T}//^2; best truth addition reduces Delta by >= Delta^2///theta//_1^2 >= (phi0^2/s0)Delta; Delta(T)=Delta(T cap R) | PROVED (author, candidate; SF: none; checked inside A-REV7 GU verdict and A-REV9 descent check) | W7-SEP/PROOF.md; A-REV7/REVIEW.md | [pos 763] [pos 919] | none (feeds TH388) |
| LM225 | Lemma GU-2; SEP-GU2; one addition at a superset | lemma | For T = S0 union E, E subset R, l not in T: F(T+l)-F(T) <= -1/2 log(n-1)+log(1/phi0)+log((r+1)/p)+W_{T,l}(1+eta_n)/2+c0 on Lemma M event, W~chi2_1 | PROVED (author, candidate; SF: none; checked inside A-REV7/A-REV9 verdicts) | W7-SEP/PROOF.md; A-REV7/REVIEW.md | [pos 763] [pos 919] | none (feeds TH388) |
| LM226 | Lemma S; MA-LemmaS; order independence of the bounded stores; top-c merge | lemma | A TopStore of capacity c under a strict total order on pairs (v,S), v = v(S) deterministic, returns the set of the c best distinct pairs of the offered multiset M whatever the offer order; hence top_c(M) = top_c(top_c(M_1) cup ... cup top_c(M_R)) for any partition; running HPM = case c = 1 | PROVED [PROOFS.md heading]; candidate, author-only; THM-SYNTH: finite combinatorics, Lean-certifiable (not done) | METH-AUDIT/PROOFS.md (Lemma S); THM-SYNTH/THEOREM_LIST.md (V2) | [pos 1107] [pos 1177] | S-OUT (K63); M5 Theorem HPM (K63 hypothesis) |
| LM227 | LIT-STAT BB(1,p) dimension ratio; BB(1,p) is not a complexity prior in the sense of CSvdV (2.2) | lemma | BB(1,p) has w(k) = (1/2)/C(2p-1,k) = B(k+1,2p-k)/B(1,p) and dimension ratio pi_p(s)/pi_p(s-1) = (p-s+1)/(2p-s) -> 1/2, so it satisfies Castillo-Schmidt-van der Vaart (2.2) for no fixed A4 > 0 uniformly in p; CSvdV Thms 1, 4 and Cor 1 do not cover it | PROVED (elementary algebra with exact rational-arithmetic confirmation, scripts/bb_ratios.py) [LIT-STAT REPORT §6]; author-only | LIT-STAT/REPORT.md §1 item 4, §6; LIT-STAT/notes/03_decision_sizeprior.md | [pos 983] [pos 1009] | none (supports S-T / Theorem 1 novelty wording) |
| LM228 | LIT-STAT BB(1,p) versus BB(1,1); BB(1,p) = BB(1,1) tilted by a geometric size factor | lemma | w_BB(1,p)(k)/w_BB(1,1)(k) = (p+1) C(p,k) / (2 C(2p-1,k)) <= ((p+1)/2)(2p/(2p-1)) 2^{-k} for k >= 1 (the i = 0 factor of C(p,k)/C(2p-1,k) is p/(2p-1) = (1/2)(2p/(2p-1)), every factor with i >= 1 is <= 1/2); per-model ratios (k+1)/(2p-1-k) vs (k+1)/(p-k) | PROVED (elementary; exact rationals, scripts/bb11_vs_bb1p.py) [LIT-STAT REPORT §12]; the first-draft line "<= 1/2 for every i >= 0" was false at i = 0 and corrected here; author-only | LIT-STAT/REPORT.md §12 | [pos 983] [pos 1009] | none (changes the novelty verdict of T02(i sharp), see CJ293) |
| LM229 | N9 Claim R; N9-R; random-order round self-adjointness; reversal-invariant random order of reversible kernels | lemma | K_1..K_m gamma-reversible kernels on a finite set, sigma a random permutation independent of the chain whose law mu satisfies mu(sigma) = mu(sigma o rho) (rho the reversal i -> m+1-i); then R = Sum_sigma mu(sigma) K_{sigma(1)}...K_{sigma(m)} is gamma-reversible (self-adjoint on L^2(gamma)); the uniform law on S_m satisfies the hypothesis, so the production round kernel is gamma_phi-reversible | PROVED (candidate) [N9 PROOF.md §2]; numerical: round DB rel <= 5.6e-14, production one_round MC matches R (27 chi^2 tests); CHK_INHERITED (cross-family) VERIFIED WITH AMENDMENT: the order conditions are sufficient, not necessary ("fails if" -> "is not guaranteed"); REPORT "A fixed order is not self-adjoint" -> "need not be" (RF278, CE218); RB consequence needs the round to start in q_phi | N9-KERNEL/PROOF.md §2; N9-KERNEL/REPORT.md; N9-KERNEL/CHECK.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1546] [pos 1550] [pos 1593] [pos 1626] | S-KERNEL (K21) |
| LM230 | Lemma KL; D3 KL bound; Chatterjee-Diaconis exp(KL) scale; NEW-SYNTH | lemma | For probability measures pi, pi0 on a finite Omega and a state S0 with delta_1 = 1 - pi(S0): KL(pi//pi0) >= (1-delta_1) log(1/pi0(S0)) - log 2 (data processing on {S0, Omega minus S0}, log-sum inequality, binary entropy <= log 2); under T27(i) the sample size exp(KL) is >= (1/2) Q*^{1-delta_1} e^{O_P(1)} | PROOF SKETCH (NEW-SYNTH; "only because unreviewed; the inequality is two lines") [THM-SYNTH]; numerical check scripts/check_lemmas.py; final MEET-THM M6: "KL: PROOF SKETCH (NEW-SYNTH), AUTHOR-ONLY in IDX; statement checks TRUE-AS-WRITTEN" | THM-SYNTH/THEOREM_LIST.md (S2(c)); THM-SYNTH/REPORT.md §2; MEET-THM/THEOREM_LIST_FINAL.md (M6) | [pos 1177] | M6 Theorem SEP + Lemma KL (K105; K19, K106) |
| LM231 | t21_event_subset | lemma | Event inclusion {U or Shat != S0} subset U union {U^c, S0 not in scored} union {U^c, S0 in scored, pi(S0) <= 1/2} | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) |
| LM232 | integral_le_eps_add_prob; finite step of H03 => E0 delta1 -> 0 | lemma | For 0 <= delta <= 1 and eps >= 0: E delta <= eps + P(delta > eps) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) |
| LM233 | measurable_post | lemma | omega -> post (F omega) A S0 is measurable when each omega -> F omega S is | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) |
| LM234 | strict_max_of_post_gt_half; post facts of Basic.lean | lemma | If 1/2 < post F A S0 then S0 in A and F S < F S0 for all other S in A | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/Basic.lean; L-LEAN/SmcBvs/SmcBvs/T21HPM.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M5 Theorem HPM (K72) |
| LM235 | risk01_eq | lemma | risk01 a = 1 - pi(a) (pi = 0 off Omega) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60) |
| LM236 | riskH_eq | lemma | riskH a = sum_j PIP_j + psi_PIP(a) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60) |
| LM237 | psi_Jplus_le; Lemma psi (a) | lemma | J+(q) minimises psi_q over all subsets of [p] | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60) |
| LM238 | psi_Jplus_unique_iff; Lemma psi (a) uniqueness | lemma | J+(q) is the unique minimiser of psi_q iff no q_j = 1/2 | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60) |
| LM239 | psi_capped_le; Lemma psi (b) | lemma | Capped a* subset of J+(q) with /a*/ = min(K',/J+/) and boundary ordering minimises psi_q over {/a/ <= K'} | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60) |
| LM240 | exists_capped; Lemma psi (b) existence | lemma | A capped action a* with the Lemma psi (b) properties exists | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T07Bayes.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | S-TARGET supplement (K60) |
| LM241 | t11_pow_le_exp | lemma | (1 - a)^Q <= exp(-(Q a)) for a <= 1 | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T11Miss.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | K19 by registrar statement-match only |
| LM242 | exists_bestImprovement | lemma | For every neighbourhood N and score F a best strict-improvement map exists (non-vacuity) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM243 | progress_mem_Lat; move-class table | lemma | A flip or swap with Phi T < Phi S lies in Lat(S) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM244 | drop_two_swap | lemma | A flip/swap lowering Phi by exactly 2 is an extra->truth swap | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry; added after Astra r1 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM245 | swap_extra_truth_drop_two | lemma | An extra->truth swap lowers Phi by exactly 2 | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry; added after Astra r1 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM246 | DS_move; D_S (one-state progress event) | lemma | Under D_S every best-improvement map makes a progress move at S, whatever the tie rule | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry; added after Astra r1 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM247 | Φ_le_of_mem_Rad | lemma | Phi(S) <= a + d on R_{a,d}, so the cap l >= a + d suffices | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM248 | invariance_step; T12 invariance algebra | lemma | sum_x gamma_{t-1}(x) G_t(x) (K_t f)(x) = sum_y gamma_t(y) f(y) for gamma_t-invariant K_t | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T12Core.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M1 Theorem V/H (K35); L-T12 |
| LM249 | resample_move_step; T12 one-step resample-move identity | lemma | For a fixed population with positive total weight, new evidence times the mean mixture-marginal expectation = Zhat (1/N) sum_k G(x_k) (K f)(x_k) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T12Core.lean; L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md | [pos 714] [pos 796] | M1 Theorem V/H (K35); L-T12 |
| LM250 | mis_ext_le_of_mem_Lat; Lat_subset; Lemma 2(a) helpers | lemma | Within a lattice mis and ext do not increase; lattices are nested (T in Lat S implies Lat T subset Lat S) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM251 | TDP_of_TDP' | lemma | Concrete TD'_P(R_{a,d}) gives the abstract Greedy.TDP (closure from Lemma 2(a)) | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM252 | mis_ext_step; flipSwap_sdiff_card; A2 lower-bound accounting | lemma | A flip/swap adds and removes at most one index; mis and ext drop by at most one per move | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry; added after Astra r1 | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM253 | path_stays | lemma | Once the greedy path is at a fixed point it stays there | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM254 | path_mem_of_TDinf | lemma | Under TD'_inf(R) the path from a state of R stays in R | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM255 | Φ_eq | lemma | Phi S = mis S + ext S | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; L-LEAN/SmcBvs/SmcBvs/T37Lattice.lean; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | [pos 714] [pos 796] [pos 787] | M5 Theorem HPM (K65) |
| LM256 | exists_isLeastArgmax; IsLeastArgmax.unique | lemma | Tie rule as injective rank: a nonempty finite set has a least argmax; it is unique under an injective rank | Lean: sorry-free supporting lemma; statement judged GREEN by the checkers named in the md entry | L-LEAN/SmcBvs/SmcBvs/Basic.lean | [pos 714] [pos 796] | S-TARGET supplement (K60); M5 (K72) |

## Conjectures, hypotheses, open problems

| ID | native name(s) | kind | description | final status | authoritative file | positions | feeds |
|---|---|---|---|---|---|---|---|
| CJ101 | T05; A4; T5-S; orthogonal threshold; benchmark gap; THEORY.md row T05 | conjecture | Orthogonal threshold and benchmark gap (old label A4 = T5-S) | CONJECTURED (not proved) | main@c4ef0dc/Docs/Theory/theorems/T05_A4_orthogonal_threshold.md; main@c4ef0dc/Docs/Theory/one_pagers/T05.md | [pos 119]; [pos 156]; [pos 178]; later [pos 717] | none in the final cards (supplement remark per FROZEN_LIST; W7-SEC results theme 9) |
| CJ102 | T08; A7; T6; oracle joint Bernstein-von Mises limit; THEORY.md row T08 | conjecture | Oracle joint Bernstein-von Mises limit (old label A7 = T6) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T08_A7_oracle_BvM.md; main@c4ef0dc/Docs/Theory/one_pagers/T08.md | [pos 119]; [pos 156]; [pos 178] | none (dropped from paper selection) |
| CJ103 | T16; T9; frozen-particle and independent-island limits; THEORY.md row T16 | conjecture | Frozen-particle and independent-island limits (old label T9) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T16_T9_frozen_limits.md; main@c4ef0dc/Docs/Theory/one_pagers/T16.md | [pos 119]; [pos 156]; [pos 178] | none (dropped from paper selection) |
| CJ104 | T17; L-RC; reflection with output-specific coupling; THEORY.md row T17 | conjecture | Reflection with output-specific coupling (old label L-RC) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T17_LRC_reflection_coupling.md; main@c4ef0dc/Docs/Theory/one_pagers/T17.md | [pos 119]; [pos 156]; [pos 178] | none (dropped) |
| CJ105 | T18; B-RP; reflected single-flip pair benchmark; THEORY.md row T18 | conjecture | Reflected single-flip pair benchmark (old label B-RP) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T18_BRP_reflected_pair.md; main@c4ef0dc/Docs/Theory/one_pagers/T18.md | [pos 119]; [pos 156]; [pos 178] | none (dropped) |
| CJ106 | T19; T12 (old label); conservative working-set bounds with explicit reward targets; THEORY.md row T19 | conjecture | Conservative working-set bounds with explicit reward targets (old label T12) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T19_T12_working_set_bounds.md; main@c4ef0dc/Docs/Theory/one_pagers/T19.md | [pos 119]; [pos 156]; [pos 178] | none (dropped) |
| CJ107 | T24; T18'; conservative terminal repair with a fixed extra-variable budget; source of H24; THEORY.md row T24 | conjecture | Conservative terminal repair with a fixed extra-variable budget (old label T18') | CONJECTURED (not proved); alternative route to paper Thm 3 (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T24_T18p_terminal_repair.md; main@c4ef0dc/Docs/Theory/one_pagers/T24.md | [pos 119]; [pos 156]; [pos 178]; later [pos 327]; [pos 342]; [pos 370] | M4 / L-PROPP mention; replaced in the final list by Theorem B (route e') |
| CJ108 | T26; T17 (old label); no-switch consistency at the actual budgets; JRSS-B Thm 6 (i)-(ii); THEORY.md row T26 | conjecture | No-switch consistency at the actual budgets (old label T17) | CONJECTURED (not proved); in the paper plan restricted to (i)-(ii) in the favourable regime | main@c4ef0dc/Docs/Theory/theorems/T26_T17_no_switch_consistency.md; main@c4ef0dc/Docs/Theory/one_pagers/T26.md | [pos 119]; [pos 156]; [pos 178]; later [pos 355] | S-Z; S-TARGET; M1; L-T12 (REGISTRY_PAPER1 mentions) |
| CJ109 | T28; T21-E; evidence loss under calibration avoidance and evidence coupling; THEORY.md row T28 | conjecture | Evidence loss under calibration avoidance and evidence coupling (old label T21-E) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T28_T21E_evidence_loss.md; main@c4ef0dc/Docs/Theory/one_pagers/T28.md | [pos 119]; [pos 156]; [pos 178] | none (dropped); source tag in M1 |
| CJ110 | T29; T21-H; HPM loss needs scoring avoidance; PIP loss needs reward control; THEORY.md row T29 | conjecture | HPM loss needs scoring avoidance; PIP loss needs reward control (old label T21-H) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T29_T21H_HPM_PIP_loss.md; main@c4ef0dc/Docs/Theory/one_pagers/T29.md | [pos 119]; [pos 156]; [pos 178] | none (dropped) |
| CJ111 | T30; T21-X; pilot discovery under the terminal-repair hypotheses; THEORY.md row T30 | conjecture | Pilot discovery under the terminal-repair hypotheses (old label T21-X) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T30_T21X_pilot_discovery.md; main@c4ef0dc/Docs/Theory/one_pagers/T30.md | [pos 119]; [pos 156]; [pos 178] | none (dropped) |
| CJ112 | T32; T23-C; branch-specific arithmetic and storage counts; T32(i); THEORY.md row T32 | conjecture | Branch-specific arithmetic and storage counts (old label T23-C) | CONJECTURED (not proved) | main@c4ef0dc/Docs/Theory/theorems/T32_T23C_resource_counts.md; main@c4ef0dc/Docs/Theory/one_pagers/T32.md | [pos 119]; [pos 156]; [pos 178]; later [pos 463]; [pos 510]; [pos 717] | M8 (Proposition D, cost corollary of T38(c)) |
| CJ113 | T33; T23-N; numerical margins on a common scored set; THEORY.md row T33 | conjecture | Numerical margins on a common scored set (old label T23-N) | CONJECTURED (not proved) | main@c4ef0dc/Docs/Theory/theorems/T33_T23N_numerical_margins.md; main@c4ef0dc/Docs/Theory/one_pagers/T33.md | [pos 119]; [pos 156]; [pos 178]; later [pos 717] | S-CERT; K107 -> FUTURE_WORK (N16 OPEN) |
| CJ114 | T34; T23-S; statuses and allocation-dependent guarantees; THEORY.md row T34 | conjecture | Statuses and allocation-dependent guarantees (old label T23-S) | CONJECTURED (not proved) | main@c4ef0dc/Docs/Theory/theorems/T34_T23S_statuses.md; main@c4ef0dc/Docs/Theory/one_pagers/T34.md | [pos 119]; [pos 156]; [pos 178] | none identified (supplement remark per FROZEN_LIST) |
| CJ115 | T35; T23-R; mass-qualified fixed-bisection obstruction and the discrepancy range; THEORY.md row T35 | conjecture | Mass-qualified fixed-bisection obstruction and the discrepancy range (old label T23-R) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T35_T23R_bisection_obstruction.md; main@c4ef0dc/Docs/Theory/one_pagers/T35.md | [pos 119]; [pos 156]; [pos 178] | none (dropped) |
| CJ116 | T36; R-T13; the pilot limit as a finite-comparison rule; THEORY.md row T36 | conjecture | The pilot limit as a finite-comparison rule (old label R-T13) | CONJECTURED (not proved); DROPPED from paper selection (FROZEN_LIST) | main@c4ef0dc/Docs/Theory/theorems/T36_RT13_pilot_finite_comparison.md; main@c4ef0dc/Docs/Theory/one_pagers/T36.md | [pos 119]; [pos 156]; [pos 178] | none (dropped) |
| CJ117 | T37; truth dominance; finite-n truth dominance and deterministic greedy repair; JRSS-B Thm 3 (new primary route); literal T37 | conjecture | Finite-n truth dominance and deterministic greedy repair (new conjecture, added 2026-10-28) | CONJECTURED (not proved); NEW, added 2026-10-28 to fill the finite-n repair hole | main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T37_truth_dominance_greedy_repair.md; main@c4ef0dc/Docs/Theory/one_pagers/T37.md | [pos 119]; [pos 156]; [pos 178]; [pos 355]; [pos 370] | M5 (Theorem A / LS-score / Lemma 0 route); literal statement feeds nothing |
| CJ118 | T38; two-regime consistency of the reported HPM; headline theorem; JRSS-B Thm 5; T38(a); T38(b); T38(c) | conjecture | Two-regime consistency of the reported HPM (headline theorem) (new conjecture, added 2026-10-28) | CONJECTURED (not proved); NEW, added 2026-10-28 (replaces T26(iii) as the HPM headline) | main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T38_two_regime_HPM_consistency.md; main@c4ef0dc/Docs/Theory/one_pagers/T38.md | [pos 119]; [pos 156]; [pos 178]; [pos 355]; [pos 510]; [pos 550]; [pos 929] | M5 (Theorem HPM); M8; L-TA |
| CJ119 | T39; independent start-to-terminal scoring tracks; Astra C37; contingency | conjecture | Independent start-to-terminal scoring tracks with an explicit budget (contingency) (new contingency conjecture, added 2026-10-28; Astra's C37) | CONJECTURED (not proved); NEW contingency target; requires a METHOD EXTENSION (not run in the 2,400 fits) | main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T39_independent_repair_tracks.md; main@c4ef0dc/Docs/Theory/one_pagers/T39.md | [pos 119]; [pos 156]; [pos 178]; [pos 355] | S-LIM (SHARE-PB) |
| CJ120 | H24; H24 inputs; T24(i) inputs; uniform exit hypothesis; K1(x,{S0}) >= a_n; first exit <= eta_n | hypothesis | Hypothesis of T21 route (e): uniform one-round truth-scoring floor a_n and exit bound eta_n on the near-truth region R_d, with a_n >= c_n/2 and (L+4)eta_n -> 0 | RETIRED (REGISTRY_v2 D): its asymptotic input (L+4)eta_n -> 0 is false in correlated designs (CE1, LemmaE); replaced by Theorem B / B-sharp (route e'). See RF102 for the refutation and CE row CE144 (CE1) (Theme 5). | main@c4ef0dc/Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md; main@c4ef0dc/Docs/Theory/theorems/T24_T18p_terminal_repair.md | [pos 119]; [pos 156]; [pos 327]; [pos 342]; [pos 370] | see TH239 (T21-e′) / TH218 (Theorem B) (M4 / L-PROPP mention); H24 itself feeds nothing |
| CJ121 | EXP'; EXP-prime; EXP′; EXP; Decision Point 2 D1; uniform actual-block expansion | hypothesis | Uniform actual-block expansion log[r_b(T+l)/r_b(T)] = -1/2 log(n+1) - nu log(1-x_{T,l}) + R with max/R/ = O_P(1) (weaker variant o_P(log n)) | PROVED (candidate) in the block-orthogonal benchmark design: CJ121 (EXP′) = W1-EXP Thm 1, SF VERIFIED (W3-VEXP), XF VERIFIED* (A-REV2; limiting constant 0.52 -> 0.51, RF134 (EXP-const)); finite-n certificate TH137 (R1-cert); for general X-dependent partitions still an obligation (FROZEN_LIST: 'Prove EXP, visibility and leakage for the actual partition dependent on X'). | main@c4ef0dc/Docs/Theory/proofs/T22iii_T16_start_aggregation/STATEMENT.md; main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md; main@c4ef0dc/Docs/Theory/proofs/T27i_T20C_cancellation_budget/STATEMENT.md | [pos 119]; [pos 156]; [pos 355] | M3 (Theorem START); L-MASK |
| CJ122 | PW2; one-step second-moment bound; a_t, nu_t slack | hypothesis | Hypothesis: E[W_{t-1}^2{(qhat_{t-1} g_t)^2 - 1}] <= (a_t/N) E[W_{t-1}^2] + nu_t for the actual particle system | STILL OPEN for the actual hybrid system (CJ262 (OWS-WS8d) OPEN); the guess a_t = chi2_t is false (RF228 (OPW2-cex) COUNTEREXAMPLE, numerical p=6); exact variance identity TH316 (OPW2-ThmA) PROVED, XF VERIFIED (A-REV9) (Themes 8, 10). | main@c4ef0dc/Docs/Theory/proofs/T25iv_T19_crossing_evidence/STATEMENT.md; main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md | [pos 119]; [pos 156] | S-Z (evidence variance and masked tails) |
| CJ123 | BASIN; BASIN(R, r0, a, eta, rho, delta); basin entrance exit departure occupancy | hypothesis | Abstract condition: entrance K_1^{r0}(x,{S0}) >= a on R, basin exit <= eta, truth departure <= rho, initial occupancy outside R <= delta | No campaign result proves BASIN in general. NOTE name reuse: W7-SEP's TH387 (SEP-BASIN) ('Proposition BASIN (deterministic)') is a different statement (LS0 scores S0 iff the start mode lies in ...). | main@c4ef0dc/Docs/Theory/proofs/T23_T18_basin_prefix/STATEMENT.md; main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md | [pos 119]; [pos 156] | S-POOL (MZ-P1P2 via T23(ii) and T12) |
| CJ124 | COVER; COVER(W, eps_C); full-space coverage; pool avoidance; P cap M empty | hypothesis | q_psi(W) >= 1 - eps_C at every evaluation point psi in E_grid; pool avoidance P cap M = empty implies V cap M = empty | No campaign result proves COVER for the actual calibration; T13 remains a source tag in the final cards. | main@c4ef0dc/Docs/Theory/proofs/T13_T10_restricted_ESS/STATEMENT.md; main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md | [pos 119] | S-IDENT (restricted-ESS coverage identity) |
| CJ125 | H2; H3; H1; H4; H2/H3; sequential ratio law; normalised reference mass | hypothesis | H1 fixed feasible completion chain (definition); H2 joint sequential log-ratio tightness; H3 normalised start-mass lower bound pi0(S^(0)) >= c0; H4 operational assumptions | H2 was to be replaced by a bounded-leakage condition along the chain (FROZEN_LIST); campaign: 'H2 is replaced by a checkable condition, and one explicit family carries masking and near-truth start mass at the same time' (HQ [pos 355]; W1-EXP, Theme 2). | main@c4ef0dc/Docs/Theory/proofs/T27i_T20C_cancellation_budget/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md | [pos 119]; [pos 156]; [pos 355] | M3 (Theorem START: masking law); L-MASK |
| CJ126 | H03; H10; H-T02; H-T03; H-T12; START; hypotheses of T21 used as inputs | hypothesis | H03: delta1 = 1 - pi(S0) = O_P(sqrt(log n / n)); H10: pi0(S+j) >= r_k pi0(S) with r_k = (k+1)/((2p-k-1) sqrt(n+1)) | H03 = T03(i) conclusion (restated as TH128 (T03♯), Theme 1); H10 = T10(i) addition floor (locked, no statistical assumption). | main@c4ef0dc/Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md | [pos 119]; [pos 156] | M5 (Theorem HPM uses delta1 = O_P(sqrt(log n / n))) |
| CJ127 | VIS; NL_eta; NL_η; NL_avg(kappa); NL_avg; TL; TL_avg; leakage; visibility | hypothesis | VIS: //(P_{T cup U*}-P_T)mu//^2 >= M_n^V v_T log n; NL_eta: delta_{T,l}^2 <= eta sigma^2 log n with eta < (sqrt(2A+1)-sqrt(2A))^2; NL_avg(kappa): average of e^{E_{T,l}} <= n^{1/2-kappa} | Partly addressed: TH139 (Prop2.1-2.2) (W1-EXP; NL_eta weakened, SF VERIFIED W3-VEXP) and the zero-leakage theorem TH140 (Thm6-EXP) (VIS-lin, ZL, SPREAD premises); n=200 dilution masking replaces weak-signal masking as the explanation (RF in registry D: 'W1-EXP weak-signal masking explains n = 200' -> evidence against). | main@c4ef0dc/Docs/Theory/proofs/T22iii_T16_start_aggregation/STATEMENT.md; main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md | [pos 119]; [pos 156]; [pos 355] | M3 (Theorem START) |
| CJ128 | SR; GUARD; stop-only coupling; IMPL-GUARD; both feasible configurations scored; emit_centre | hypothesis | SR: both Gibbs configurations (held and flipped) count as scored and reach the HPM store; GUARD: on non-resource_limit fits every statistical output equals that of the potential uninterrupted run | SR: IMPLEMENTATION FACT - HQ read, confirmed in substance by a cross-family reading (A-REV7); the blanket 'no call passes emit = false' is too strong (v3_core.cpp:447,610,657 pass false for already-scored HPM centres). GUARD: IMPLEMENTATION FACT - statistical stop-only coupling supported by two cross-family code readings (A-REV5, A-REV8); literal 'every output equals' ERROR (A-REV4, A-REV8): diagnostics differ. | main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md; campaign/HQ/SR_AUDIT.md; W2-BOOK/PROOF.md; T38-RECORD/REGISTRY_v2.md; W5-LOCKBOOK/AUDIT.md | [pos 540]; [pos 542]; [pos 551]; [pos 580] | all theorems that use SR: D2 (W1-T38E), Theorem B, T21 routes (d)/(e'), T38 (SR_AUDIT 'What SR asserts') |
| CJ129 | TD; TD(d,m); TD(d, 0); truth dominance; near-truth region R_d; TD-prime (later) | hypothesis | TD(d,m): for S in R_d not containing S0 some missing true variable has addition gain >= m + every other move; for S strictly containing S0 some extra has deletion gain >= m + every other move; at S0 every move has gain <= -m | REFUTED as written: 'false for d >= 1 on any design (Prop1-TD, V1-TDfails); false at d = 0 without positivity (CEX1)'; replaced by Theorem A + POS and Theorem W. See RF101; CE: RF101 (CEX1) (Theme 4). | main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T37_truth_dominance_greedy_repair.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md | [pos 156]; [pos 178]; [pos 355] | M5 (Theorem A / LS-score / Lemma 0) |
| CJ130 | EX-A; EX-S; CAL; EXEC; G; R; SE; BM-C; BM-infinity; BM-inf; BM-∞; DX; NIS; DUP; ORTH; COH; GL; R1; R2; R3; R4; regime assumptions | hypothesis | EX-A exact arithmetic; EX-S ideal independent streams; CAL calibration streams 0-9 / final streams 10-13; EXEC scans completed; G fixed-design Gaussian; R s0 fixed, p <= n^A, //mu//^2/n <= M, lambda_min(R_S0) >= phi0^2; SE; BM-C / BM-inf | Campaign changes to this block (pointers only): BM-C replaced by T03-sharp thresholds (TH128 (T03♯): valid only from n about 2e6, ⟦T03-1.2e5⟧); SE restricted to the comparison unions used and SE_w on at most 114 columns (E-SPINE 2.3); fixed-s0 triangular array convention ('s0 = floor(sqrt n) not covered'). | main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md; main@c4ef0dc/Docs/THEORY.md | [pos 119]; [pos 156] | S-T (T03♯ premises); S-TARGET |
| CJ131 | True posterior size cutoff; does the true posterior need m - s0 ~ s0 log p under G and R | open problem | Whether the TRUE posterior needs m - s0 of order s0 log p under G and R alone is open; Prop E3 is only a barrier for the proof technique and Prop D gives only (1/2)log2 n - O(1). | OPEN (W1-T03R confidence card: P(true)=0.3); not attempted | W1-T03R/REPORT.md; W1-T03R/PROOF.md; W2-VT03R/REPORT.md | [pos 296] | feeds: none (campaign-only) |
| CJ132 | Conjecture m - s0 = O(log n) under SE_w at all sizes <= K; route conjecture of W1-T03R section 4 | conjecture | Under SE_w at all sizes <= K, a per-eigendirection truncation of the Markov moment and a weak residual condition might give m - s0 = O(log n) suffices. | CONJECTURE (W1-T03R; P(true)=0.6, P(provable)=0.4); not attempted in full | W1-T03R/REPORT.md | [pos 296] | feeds: none (campaign-only) |
| CJ133 | Determinant-only SE; geometric-mean eigenvalue condition; W1-T03R PROOF section 7 remark 3 | conjecture | In (C4) only the determinant ratio D_{S0 u J}/D_{S0} >= [c(n+1)]^/J/ and full rank are used, so an assumption on determinants alone (a geometric-mean eigenvalue condition) would suffice for (C4)-(C5). | CONJECTURE (W1-T03R, not proved, not pursued) | W1-T03R/PROOF.md; W1-T03R/REPORT.md | [pos 296] | feeds: none (campaign-only) |
| CJ134 | T03-CONST; API-T03CONST; referee task R9; explicit c0(s0,A) and first-n table | hypothesis | Proposed target (F-REFEREE R9): make C* explicit in sigma*^2, M, phi0 giving an explicit c0(s0,A) in BM(c), and tabulate for (p,s0) in {(500,14),(1000,14)} the first n at which each deterministic step of W1-T03R holds, reproducing W2-VT03R R1. | OPEN: task spec written but run HELD (API rate limits) and no report found; not completed in the thread | campaign/tasks/API-T03CONST.md | [pos 906]; [pos 910]; [pos 996] | feeds: none (was planned for M1(ii) finite-n disclosure of Theorem 1) |
| CJ135 | T03-sharp extensions: growing s0, random design, exponential p; FW18; FW19; N11; N12 | open problem | Extensions outside T03-sharp: s0=floor(sqrt(n)) (the generator rule), growing support with non-binding cap, random design, p up to exp(Cn^alpha), universal finite-n onset n0; none is covered. | OPEN / FUTURE_WORK FW18, FW19 (MEET-THM); scope sentence in S-T: p <= n^A, e^(Cn^alpha) OPEN | MEET-THM/FUTURE_WORK.md; MEET-THM/COVERAGE_MATRIX.md; W6-FIXREV2/STATEMENTS.md | [pos 296]; [pos 929] | FUTURE_WORK FW18 (N12 exponential p), FW19 (growing support), FW20 (Hellinger/predictive contraction) |
| CJ136 | T05 explicit n0 via DKW-type uniform control of null order statistics | conjecture | A DKW-type uniform control of null chi-square order statistics should bring the explicit n0 of T05-L from log n about 227 to O(10^2); Monte Carlo suggests that is the truth. | CONJECTURE / not pursued (W7-SEC section 5) | W7-SEC/REPORT.md | [pos 751] | feeds: none |
| CJ137 | T04 and T03 downstream re-derivation with T02(i-sharp) and SE_w instead of H-T02 | hypothesis | W1-T03R section 6 item 3: T04 cites H-T02 with the old m_n; its SE branches could use m# and SE_w; not checked. T20, T21, T06 and T22(iv-c) use only the T03(i) conclusion, which is unchanged. | OPEN (stated by W1-T03R as not checked; no later branch addresses it) | W1-T03R/REPORT.md | [pos 296] | feeds: none (T04 not a paper-1 card) |
| CJ138 | LIT-STAT E1 and G1: no published BB(1,p^u) dimension/tail bound; Martin-Mess-Walker 2017 not read | open problem | Open literature question: is there really no published size-tail bound for a non-complexity BB(1,p^u), u<=1, prior with a unit-information slab? Candidates not read: Castillo-van der Vaart 2012 section 2, Martin-Mess-Walker 2017 (Rossell 2022 supplement was read later: BB(1,1), uniform, Complexity only). | OPEN (LIT-STAT escalation E1; partly updated in section 12; novelty of T02(i-sharp) rated modest) | LIT-STAT/REPORT.md | [pos 1009] | feeds: none (referee-defence note for S-T) |
| CJ139 | InSample-fav; in-sample favourable regime for iid S1/S3/S4/S6; partition-noise decoupling | conjecture | For iid designs with >= 2 groups per block, 1 - pi_0(S0) -> 0 (empirically n >~ 800-1600 at S3 p=500); needs partition-noise decoupling | CONJECTURE (W3-VEXP, P(true) 0.85); A-REV2/A-REV5: GAP for B>=2g packing | W3-VEXP/REPORT.md; W3-VEXP/REPAIRS.md; A-REV2/REVIEW.md | [pos 363] [pos 370] [pos 568] | feeds: none (W5-FAVIID Theorem B claims a 2^B-free version, Theme 3) |
| CJ140 | PXN-W′; W3-PXN Conjecture W′; fixed-s0 dilution family | conjecture | Local alternatives theta_j^2 = kappa sigma^2 log n/n in the window (1+2A) < kappa < (1+2A) v_T/sigma^2 give pi_0(S0) -> 0 polynomially while LO_1 -> inf; pi(S0) -> 1 needs a sharp-constant T03 | CONJECTURE (W3-PXN, P(true) 0.7) | W3-PXN/PROOF.md; W3-PXN/REPORT.md | [pos 423] | feeds: none |
| CJ141 | W1 card T22(iii) iid designs; T22(iii) for S3/S4/S6 | conjecture | 1-pi_0(S0) = O_P(2^B sqrt(log n) n^-1/2) for iid S3/S4/S6 with the actual partition (uniform truncated Beta average) | card-level target (W1-EXP P(true) 0.8, P(provable) 0.6); not written | W1-EXP/REPORT.md; W3-PXN/REPORT.md | [pos 351] [pos 423] | feeds: none (Theme 3 W5-FAVIID) |
| CJ142 | VMASK-LemmaB-psi; Lemma B beyond /psi/<rho | conjecture | Lemma B's exact Beta laws hold whenever the LH population identities hold, even for psi > rho (KS tests at psi=0.9 pass) | CONJECTURE (registry; author recorded VERIFIED (new), numerical only) | W5-VMASK/REPORT.md | [pos 742] | feeds: none |
| CJ143 | VMASK-psi-lt-1; LH-LAT algebra needs only /psi/<1 | conjecture | The pair unit is positive definite iff psi^2<1, so the lattice algebra holds beyond /psi/<rho; /psi/<rho is needed only for the partition | PROOF SKETCH (registry; one-line argument plus brute force) | W5-VMASK/REPORT.md | [pos 742] | feeds: none |
| CJ144 | VMASK-hetero-rho; heterogeneous within-group correlations | conjecture | Groups may have their own rho_h provided min_h rho_h > max_i /psi_i/; proofs nowhere use a common rho | CONJECTURE (registry; verified numerically, not proved) | W5-VMASK/REPORT.md | [pos 742] | feeds: none |
| CJ145 | VMASK-beyond-cliff; psi>rho transition to the favourable regime | conjecture | For psi > rho the LH masking is destroyed by the partition (hubs co-blocked), pi_0(S0) ~ 0.07-0.7: a transition to the favourable regime, not a method failure | CONJECTURE (registry; 10 replicates at n=200, 400) | W5-VMASK/REPORT.md | [pos 742] | feeds: none |
| CJ146 | PART-pairing; which groups share a block when 2g<=B | open problem | Pairing of whole groups into blocks for g=5, B=14 is decided by minimum cross /r_hat/ and depends on null columns; W3-VEXP GAP (b) partition-noise decoupling | OPEN (W7-PART; registry author OPEN, no review) | W7-PART/REPORT.md; W7-PART/PROOF.md; A-REV6/PARTITION.md | [pos 717] [pos 796] | S-BLOCKS (K07) excluded (PART-pairing remains OPEN); M5 context |
| CJ147 | PXNGAP O2; discovery half for log p = o(n) | conjecture | The discovery half (R, S, E, T) survives log p = o(n) with thresholds t_n proportional to log/family/; the posterior half does not because T03 is locked for p<=n^A only | CONJECTURE (API-PXNGAP, not written) | API-PXNGAP/PROOF.md; API-PXNGAP/REPORT.md | [pos 911] [pos 978] | FUTURE_WORK FW18 context (exponential p) |
| CJ148 | no-tweak route (b1′) for c>=2; D2 at Gibbs distance >=2 | open problem | Original method (no LS0) scores S0 w.p. -> 1 - P(U) on LH-iid for c>=2 (needs delivery at distance >=2, the SHARE problem) | OPEN (W3-PXN, W5-VMASK; P(true) 0.6, P(provable) 0.15) | W3-PXN/REPORT.md; W5-VMASK/REPORT.md | [pos 423] [pos 742] | feeds: none (no-LS0 candidates in Theme 6) |
| CJ149 | Theorem-C analogue for factor-dependent groups; S5-type global factor | conjecture | Partition recovery for the S5-type global factor (cross 0.3, within 0.7) by partialling out the common factor in the analysis, not in the method | proposed target (W7-PART: 'looks feasible'); unproved | W7-PART/REPORT.md | [pos 717] [pos 796] | feeds: none |
| CJ150 | rigorous n=200 partition bound for the LH linked pair | open problem | Replace the rigorous bound 0.17 (MC CP95 1.5e-4) by conditioning on the two hub columns and a Lemma-3-type rotation in span(1,x_a,x_b)^perp | proposed target (W7-PART escalation 3) | W7-PART/REPORT.md | [pos 717] [pos 796] | feeds: none |
| CJ151 | W1 sec 1.5; SE-blk and EXP′ for iid designs with X-dependent partition | conjecture | For iid N(0,Sigma) rows with kappa_17(Sigma) >= 2 phi0^2 and p<=n^A, SE-blk(phi0) holds w.p. -> 1 for every partition into blocks of size <= 16, so Thm 1 applies conditional on X | PROOF SKETCH (W1-EXP); SF VERIFIED as sketch (W3-VEXP row 6); scope retained by A-REV2 | W1-EXP/PROOF.md; A-REV2/REVIEW.md | [pos 351] [pos 363] [pos 568] | feeds: none |
| CJ152 | path-wise finite-n (D_S) bound at n=200 | open problem | A non-vacuous lattice margin at n=200 using the actual O(1) prior differences instead of the worst-case (2A+1)log n penalty | not attempted (API-PXNGAP outside scope) | API-PXNGAP/REPORT.md | [pos 978] | feeds: none (Theme 9 finite-n) |
| CJ153 | Conjecture DM-asy; Conj. DM-asy; DIL-DMasy | conjecture | growing s0 with n/(s_n log(pn))->kappa: start-visible fraction -> limit in (0,1); pi0(S0)->0 while pi0(R_d) bounded below (population BO) | CONJECTURE (author); open | O-DILUTE/REPORT.md §2,§6,§8 | [pos 763] | feeds: none (campaign-only) |
| CJ154 | Conjecture B' (W5-FAVIID); B'-conj; FAV-ConjBp | conjecture | Theorem B holds without the /W(m)/ factor | CONJECTURE (P(true) 0.75 after API-FAVIID, down from 0.85) | W5-FAVIID/REPORT.md §2,§5; API-FAVIID/REPORT.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| CJ155 | FAV sharp first order; FAV-sharp; W5-FAVIID section 10 | conjecture | 1-pi0(S0) ~ 1-exp(-N_add), N_add~(s0+1)(p-s0)M(p,n)/((2p-s0-1) sqrt(n+1)), independent of B,g,theta | CONJECTURE (REPORT label; PROOF SKETCH of mechanism); numerics within 0.86-1.11 at n=3200 | W5-FAVIID/REPORT.md §2,§4.3; W5-FAVIID/PROOF.md §10 | [pos 742] | feeds: none (campaign-only) |
| CJ156 | FAV plug-in thresholds; FAV-plugin; n*_null n*_del n*_swp n*_half n*_hit | conjecture | explicit population thresholds in (theta,v,p,s0,rho) for when the start sees the truth; median-level formulas | CONJECTURE (each limit PROOF SKETCH; checked numerically; predictor optimistic by 1.5-2.5 in n) | W5-FAVIID/REPORT.md §2,§4.4; W5-FAVIID/PROOF.md §11 | [pos 742] | feeds: none ('favourable from n ~' figures not quoted: RF160) |
| CJ157 | (C-fix) delivers S'; OMIX-Cfix; C-fix plug-in conjecture | conjecture | fixed point of S'<-argmax pi0^C[sigma-hat^2(S')] is close enough to S0 for Theorem C1 | CONJECTURE (numerics: S0 in mode in 92% of BO-D replicates); refuted in iid designs by C-E4 (F-SIGMA); real fits 2113/2400 at cap | O-MIX/REPORT.md; F-SIGMA/REPORT.md; API-RESID/REPORT.md | [pos 674] [pos 763] [pos 1009] | feeds: none (campaign-only) |
| CJ158 | OMIX-C-null; null-inflation risk of (C) | conjecture | common plug-in can inflate null models' start mass; start concentrated iff sigma-hat^2/sigma^2>2A/(2A+1) asymptotically; needs a floor | PROOF SKETCH (made rigorous as F-SIGMA Theorem S2) | O-MIX/REPORT.md §4.4 | [pos 674] | feeds: none (campaign-only) |
| CJ159 | OMIX-BiidLH; (B-merge) on LH-iid (p>>n) | conjecture | W3-PXN start argument at reference S0 on the merged partition | PROOF SKETCH (not checked line by line) | O-MIX/REPORT.md | [pos 674] | feeds: none (campaign-only) |
| CJ160 | Hub-move variant of (B-merge); O-MIX Thm B3 Remark 3 | conjecture | move one endpoint of each linked edge into the other's block, mix both orientations: 2^/E/ components, cost /E/ log 2 nats | PROOF SKETCH (acceptable only for small /E/) | O-MIX/REPORT.md | [pos 674] | feeds: none (campaign-only) |
| CJ161 | T_n = O_P(1) in the favourable regime; W5-FAVIID section 5 open item | open problem | realised stage count T_n settles to a constant (simulated 4-5, not 1) in the favourable regime | OPEN | W5-FAVIID/REPORT.md §4.5,§5; API-FAVIID/REPORT.md | [pos 742] [pos 978] | feeds: none (campaign-only) |
| CJ162 | Backfit start; residualised tables; partial-residual tables; resid sweeps; O-DILUTE resid variant | hypothesis | v3 tables scored on partial residuals y - X_{-b} beta_hat_{-b} (backfit): a favourable, usable start (3 sweeps 1888/2400, fixed point 2203/2400 favourable on real fits) | candidate, unproven (API-RESID: 'unproven candidate'; no theorem, no SMC evidence); rejected for paper 1, recorded as future work (MEET-v31 MINUTES item 1) | API-RESID/REPORT.md; O-DILUTE/REPORT.md §5,§9; F-SIGMA/REPORT.md §9; MEET-v31/MINUTES.md | [pos 763] [pos 894] [pos 973] [pos 1009] [pos 1130] [pos 1251] | feeds: none (outside the fixed method; COVERAGE_MATRIX disposition) |
| CJ163 | Backfit sweep iteration converges; fixed-point rule | conjecture | iteration of backfit sweeps reaches a repeated start mode (2310/2400 within 10 sweeps, 90 unsettled, 57 two-cycles) | unproven (API-RESID) | API-RESID/REPORT.md §3.4; API-RESID/results/sweeps_tables.md | [pos 1009] | feeds: none (campaign-only) |
| CJ164 | ABL-CONF Claim 1; cost claim | hypothesis | at equal accuracy the block start (A) costs less than singleton factors (B) | INCONCLUSIVE (pre-registered rule: S1 inconclusive, S4 holds_nondeliv, S5 holds); XF none | ABL-CONF/PREREG.md; ABL-CONF/REPORT.md; ABL-CONF/results/final/REPORT_TABLES.md | [pos 1429] [pos 1432] [pos 1449] [pos 1669] | feeds: none (method summary; no theorem card) |
| CJ165 | ABL-CONF Claim 2; accuracy claim | hypothesis | at equal declared budgets the prior start (C) underestimates the evidence and is less accurate than the block start (A) | LICENSED (pre-registered rule: holds on S1, S4, S5; median log Z error -13.4/-10.8/-5.7 nats); XF none | ABL-CONF/PREREG.md; ABL-CONF/REPORT.md; ABL-CONF/results/final/REPORT_TABLES.md | [pos 1429] [pos 1432] [pos 1449] [pos 1669] | feeds: none (method summary; no theorem card) |
| CJ166 | ABL-START Outcome 1 depth claim; block start reduces depth/stages at equal accuracy; local-to-global ablation | hypothesis | block start (A) needs no more stages/rebuilds than singleton (B) or prior (C) starts on >=9/12 designs with accuracy not worse | not licensed: Outcome 2 (keep, reframe; no depth or speed claim) under the pre-registered rule; v1 and corrected v2 script agree; arm C certified low on 10/12 designs | MEET-v31/ITEM1_ABL_START.md; MEET-v31/SYNTH_R2.md; MEET-v31/AMENDMENT_HQ_01.md; ABL-START/REPORT.md (design draft) | [pos 1130] [pos 1197] [pos 1248] [pos 1251] [pos 1412] [pos 1467] | feeds: none (METHOD_v3.1_FINAL row 0; no theorem card) |
| CJ167 | Refined finite-n aggregation for T22(i) weighting U by start mass | proposed target | usable finite-n certificate replacing the pessimistic locked e-quantity | not attempted (would edit a locked statement) | W5-FAVIID/REPORT.md §7 | [pos 742] | feeds: none (campaign-only) |
| CJ168 | Prop. D' dilution clause as sharp theorem; joint law of lambda_b across blocks | proposed target | joint law with in-sample cross-block leakage and BB-size coupling; Lemma L(b) extreme-value step; bit-exact check on stored .rds | not attempted (O-DILUTE needs escalation 1,2,4) | O-DILUTE/REPORT.md §8 | [pos 763] | feeds: none (campaign-only) |
| CJ169 | Two-variable block formula (truth + 4 equicorrelated proxies) | proposed target | closes the 1.0-1.6 decade miss in S3/S4 from proxy competition | not done | O-DILUTE/REPORT.md §7 | [pos 763] | feeds: none (campaign-only) |
| CJ170 | Theorem C (C4); C4 | conjecture | Under SE+BM-inf+LD(d+d1), TD'_inf(R_{a,d+d1}) holds w.p.->1 for a design-dependent d1 with move bound a+d+2d1 | CONJECTURE (W1-T37R; not assessed by SF; a version proved as TH388 (Prop GU)) | W1-T37R/REPORT.md; W1-T37R/PROOF.md | [pos 355] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| CJ171 | beta-removal conjecture; star-prime-a alone suffices | conjecture | Removing (beta) slack via a joint Gaussian supremum raises certified threshold at A=1,d=2 from 0.143 to 0.200 | CONJECTURE (W5-VPGD card P(true) 0.7) | W5-VPGD/STAR.md; W5-VPGD/REPORT.md | [pos 550] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| CJ172 | VPGD-R4; C-LD for p~n^A; r>1/(2A) | conjecture | Equicorrelated-null counterexample extends to p~n^A with threshold r>1/(2A) | CONJECTURE (downgraded from claim by W5-VPGD R4) | W5-VPGD/REPAIRS.md; W3-PGD/PROOF.md | [pos 550] [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| CJ173 | effective-truth potential for masked designs | open problem | A potential counting effective truths could make the masked LH path a progress path and give a region-form statement | not pursued (W5-VPGD outside scope) | W5-VPGD/REPORT.md | [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| CJ174 | optimality of Prop G; remaining gap in LD threshold | open problem | Is the Prop G configuration extremal for a given LD-flat level; random-design A>1 versions of Props G and C-LD | OPEN (W5-VPGD) | W5-VPGD/REPORT.md; W3-PGD/REPORT.md | [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| CJ175 | boundary band max rho0/rho+ -> 1 | open problem | Band between Theorem W and Prop P4: ratios 1-eta_n and [1,1+o(1)] | OPEN (narrowed by W5-VPGD R0) | W3-PGD/PROOF.md; W5-VPGD/REPAIRS.md | [pos 742] | feeds: none (campaign-only; not in REGISTRY_PAPER1) |
| CJ176 | 0/541 forced by monotonicity; Lemma 0 data remark | open problem | Whether all 541 unrepaired centres have F(S0)<F(S_c) (monotonicity-forced) rather than the CEX-2 pattern | OPEN (W3-VT37R, W6-FIXREV2); settled on study data by S-ELS (541/541 forced); logical claim stays refuted | W3-VT37R/REPORT.md; W6-FIXREV2/STATEMENTS.md; S-ELS/REPORT.md | [pos 370] [pos 715] [pos 763] | data fact ELS-3; feeds: none (data) |
| CJ177 | Gibbs-route restatement; T24 from Lat-neighbourhoods with Phi<=2 scored within one or two rounds; L+4 vs L+5 | hypothesis | From any particle in Lat-type neighbourhoods of S0 with Phi<=2, S0 is scored within one or two rounds w.p.>=1-eps (terminal segment L+4, conservative vs L+5) | proposal in W1-T37R REPORT section 7 (theme 5 owns T24 results) | W1-T37R/REPORT.md; W2-VT24G/NOTES.md; A-REV1/REVIEW.md | [pos 355] | TH218 (Theorem B) (T24 theme) |
| CJ178 | LS0-4; LS0-EMIT; integrated LS0 test fit | open problem | In-engine LS0 run with emit_centre=true and HPM tie rule untested; post hoc union equals integrated run unverified | OPEN implementation check (O-LS0) | O-LS0/REPORT.md | [pos 760] | LS0 part of the method (E-SPINE); feeds: none |
| CJ179 | 233/234 vs 0/541 discrepancy; sampled-centre rerun | hypothesis | W3-VT37R's sampled-centre 233/234 non-repaired with F>=F(S0) differ from ledger 0 because sampled centres are not the SMC's actual centres | UNCERTAIN (likely but unconfirmed; SYNTHESIS 4.6) | W3-VT37R/REPORT.md; S-ELS/REPORT.md; W8-SYNTH/SYNTHESIS.md | [pos 370] [pos 763] | feeds: none (data) |
| CJ180 | T24; T18'; T24 (T18'); Conservative terminal repair with a fixed extra-variable budget | conjecture | Pre-campaign conjecture: K1(x,S0)>=a_n, exit<=eta_n on R_d; (1-a_n)^H+H*eta_n bound; a_n built from c_n=1/(s0+d+B+2)! | CONJECTURED (not proved); superseded by Theorem B (TH218) | main@c4ef0dc/Docs/Theory/theorems/T24_T18p_terminal_repair.md; main@c4ef0dc/Docs/Theory/one_pagers/T24.md; main@c4ef0dc/Docs/THEORY_PRIORITIES.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md | [pos 119] [pos 178] [pos 238] | superseded by TH218; none of M1-M8 |
| CJ181 | layered version of Theorem B; layered potential (cancellation) | open problem | Layered phase-1 families T1 ⊆ T2 ⊆ ... when truths become addable only after partners | OPEN | W1-T24G/PROOF.md; W2-PREM/REPORT.md | [pos 296] [pos 424] | none |
| CJ182 | non-vacuous finite-n single-particle repair; drift with state-averaged rates; Lyapunov version | open problem | A finite-n bound for one particle that is non-vacuous at n=200 (needs state-averaged rates and multi-step credit) | OPEN | W1-T24G/REPORT.md; W2-VT24G/REPORT.md; MEET-THM/FUTURE_WORK.md | [pos 296] [pos 370] | FUTURE_WORK FW26 (finite-n Gibbs discovery; no route) |
| CJ183 | multi-step-per-round progress bound | open problem | A non-vacuous progress bound crediting several V-units per round (Prop. A is vacuous) | OPEN | W2-VT24G/PROOF.md; W2-VT24G/REPORT.md | [pos 370] | FW26 context; none |
| CJ184 | production-B conjecture c2 -> 1 - H_a | conjecture | With B=14-16 non-Gibbs labels rarely accept near the truth so c2 -> 1-H_a | CONJECTURE (W1-T24G) | W1-T24G/PROOF.md | [pos 296] | feeds: none (campaign-only) |
| CJ185 | IND-M for superset starts; superset start concentration S° ⊋ S0 | open problem | Independence-move bad acceptance when pi0 concentrates on a superset of S0 | OPEN (plausibly false at finite n) | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| CJ186 | TL-sharp in random designs; bounded-leakage ZJL | open problem | Junk-addition control in random designs (max-type NL_eta fails at fixed SNR) | OPEN | W2-PREM/PROOF.md | [pos 424] | feeds: none (campaign-only) |
| CJ187 | CE1 asymptotic sketch; H24 false in correlated designs (blanket) | conjecture | Broad claim that H24's uniform exit input fails in general correlated designs; two limits o*->1, Q_T->0 not written out | PROOF SKETCH (blanket claim retracted by A-REV1 / W6-FIXREV1 section 9; narrow version = CE145) | W1-T24G/PROOF.md; W2-VT24G/PROOF.md; W6-FIXREV1/CONSOLIDATED.md; A-REV1/REVIEW.md | [pos 296] [pos 370] [pos 470] [pos 742] | feeds: none (campaign-only) |
| CJ188 | a1>=0.14 at production B=14; Cor. P1 at production B | open problem | Corollary P1's non-vacuous 0.86^{N1} bound is shown only at B=4; unmeasured at B=14 | unmeasured (OPEN) | W2-VT24G/REPORT.md; W1-T24G/REPORT.md | [pos 370] | feeds: none (campaign-only) |
| CJ189 | SHARE; SHARE(zeta); per-stage share hypothesis | hypothesis | P(A_{t-1} ∩ {no stage-t resampled particle in R_d}) <= zeta_t | superseded by the D4 envelope; nearly the conclusion (W3-VT38E); cannot be iterated over stages (W4-SHARE) | W1-T38E/PROOF.md; W4-SHARE/REPORT.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] [pos 444] | feeds: none |
| CJ190 | LT; islandwise evidence lower tail; evidence lower tail | hypothesis | P_C(Zhat_r/Z < c) -> 0 for one c and one island, sufficient for delivery via T15 | not necessary (C1 without o and PB deliver with log Zhat/Z ≈ -1800 and -67); fails in the masked late-crossing case | W1-T38E/PROOF.md; W4-SHARE/REPORT.md | [pos 370] [pos 742] | feeds: none |
| CJ191 | DELIV; DELIV(X_n); delivery of an eligible particle | open problem | An eligible particle exists at the terminal boundary: P(U^c ∩ {no final-run particle in R_d after stage T}) -> 0 | OPEN in general (A-REV5 D3-surrogate conditioning GAP); proved instances only on LH (confinement under STAB-LH; closure F2 GAP; locked set at fixed p) | W1-T38E/PROOF.md; T38-RECORD/T38_STATEMENT.md | [pos 370] [pos 919] | feeds: none (Not claimed outside LH) |
| CJ192 | SHARE-TRACK; (TRACK)+(OSC) for BVS | conjecture | BVS-level inputs of the envelope route: occupancy-weighted exits near the R_d boundary and oscillation control | CONJECTURE (W4-SHARE; numerically supported; no verifier assigned) | W4-SHARE/REPORT.md | [pos 742] | feeds: none |
| CJ193 | SHARE-BGD; Bridge-Gibbs discovery; multi-flip D2 conjecture | conjecture | Under G,R,SE,BM-inf and EX-A/EX-S/SR, if pi0(R_d) >= b>0 then S0 is scored during the bridge w.p. -> 1 | CONJECTURE (W4-SHARE; 500/500 islands numerically; depends on Prop M(b) now ERROR); proved realisations only on LH (BG1-BG3, B2-LH) | W4-SHARE/REPORT.md | [pos 742] | feeds: none |
| CJ194 | SHARE-C1BVS; C1-type extinction in BVS only where REPAIR fails | conjecture | A BVS realisation of C1 with repair valid on the occupied region does not exist; C1-type extinction occurs only where REPAIR already fails (posterior barrier) | CONJECTURE (W4-SHARE; no verifier) | W4-SHARE/REPORT.md | [pos 742] | feeds: none |
| CJ195 | CF-compat; CF(c); explicit family CF(c) | conjecture | The explicit family CF(c) satisfies G,R,SE,BM-inf,T27 masking, start mass, ELIG and TD' jointly (asymptotically); numerics at n in {400,1600} | CONJECTURE (W1-T38E); SF GAP on status (W3-VT38E); superseded by LH | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | feeds: none |
| CJ196 | D2-instance; D2 statistical instance; Dep, NB′, pi0(x°)>1/10 on a masked family | conjecture | D2-inf's premises (Dep <= 1-c1 off a bounded set, P(NB'^c)->0, pi0(x°)>1/10) hold w.p. -> 1 on a masked one-cancellation family | PROOF SKETCH (W1-T38E, W3-PXN); XF GAP; proved on LH c=1 (TH268,TH269); c>=2 OPEN for D2 | W1-T38E/REPORT.md; W3-VT38E/REPORT.md; W5-B2ENV/PROOF.md | [pos 370] [pos 742] | feeds: none |
| CJ197 | FSH-PK; PK(d*); PK(g-1); proxy keep | conjecture | A truth is kept at every proxy configuration (finite population inequalities in (rho,psi,g)) | CONJECTURE in general (checked exactly for (0.7,0.5,4)); A-REV7: PK(g-1) coverage gap | F-SHARE/PROOF.md; F-SHARE/REPORT.md; A-REV7/REVIEW.md | [pos 748] [pos 919] | feeds: none |
| CJ198 | DOM; domination condition | hypothesis | min_{x,j}[F(x)-F(x-j)] >= max_{x,b'}[F(x+b')-F(x)] + c4 n: every truth in S° outweighs every missing hub | checkable condition (F-SHARE); fails marginally on LH20 at n=1600 (+4.7 nats); exemption for c=1 refuted (RF207) | F-SHARE/PROOF.md; A-REV7/REVIEW.md | [pos 748] [pos 919] | feeds: none |
| CJ199 | FSH-C4.3; CONJECTURE 4.3; extras count across resampling | conjecture | Re-weighting does not let extra-carrying particles accumulate across stages (bounded extras after each round) | CONJECTURE (F-SHARE; the only non-routine step of the scoring sketch) | F-SHARE/PROOF.md; F-SHARE/REPORT.md | [pos 748] | feeds: none |
| CJ200 | FSH-F1′; Theorem F1′; reversible leaks | conjecture | A class whose exits land in a less-fit set that returns w.p. >= 1-eta' is delivered (D4 with h = 1_W + rho 1_L) | CONJECTURE (author: routine from D4) | F-SHARE/PROOF.md; F-SHARE/REPORT.md | [pos 748] | feeds: none |
| CJ201 | FSH-F2iid; CONJECTURE F2-iid; F2-iid | conjecture | On LH-iid (p >> n) the bounded-extras class W_d(S°) satisfies F1' hypotheses, DELIV(W_d) -> 1 for fixed d >= 1 | CONJECTURE (F-SHARE; author P(true) 0.75, P(provable) 0.4) | F-SHARE/REPORT.md | [pos 748] | feeds: none (FUTURE_WORK FW10 related) |
| CJ202 | OBG-pinf; OBG-LHiid; LH-lock for p -> infinity | conjecture | BG3/LH-lock extends to growing p (exact Gram p ≍ n or LH-iid): uniform gaps over 2^{p-s0} supersets and a polynomial order constant | CONJECTURE (O-BGIBBS author only) | O-BGIBBS/REPORT.md | [pos 748] [pos 763] | feeds: none |
| CJ203 | OBG-final-run; bridge-stage discovery for c>=3 without BG3 | open problem | Final-run bridge-stage discovery needs survival of the start-mode count until phi_t >= phi_sc (D4/D5-type delivery input) | OPEN (O-BGIBBS); superseded on LH with p fixed by BG3 + LH-lock | O-BGIBBS/REPORT.md | [pos 748] [pos 763] | feeds: none |
| CJ204 | B2E-open47; B2-LH without STAB-LH | open problem | (b2) on LH when m_STAB < 0 (e.g. rho=0.85, psi=0.5; configuration B) | OPEN (W5-B2ENV; two plausible repairs; runs numerically unaffected) | W5-B2ENV/PROOF.md | [pos 742] | feeds: none |
| CJ205 | B2E-LHiid; LH-iid analogue of NB′ and B2-LH | conjecture | The LH exact-Gram arguments transfer to LH-iid (P(NB'^c) = O(g n^{-1/2})) | CONJECTURE (W5-B2ENV remarks only) | W5-B2ENV/PROOF.md | [pos 742] | feeds: none (FW10 related) |
| CJ206 | unrestricted LH no-LS0 theorem; A-REV7 minimal gap | open problem | No-LS0 consistency on every LH parameter value, LH-iid and the study's designs; needs control of profitable swaps out of the visible-superset class | OPEN (A-REV7 Section 8) | A-REV7/REVIEW.md; T38-RECORD/T38_STATEMENT.md | [pos 919] | feeds: none (Not claimed) |
| CJ207 | M-star; Astra candidate repair of Prop M(b); REV6-cands(A6) | conjecture | Candidate replacement of SHARE-M(b) with exact log-RSS and normalised Gram eigenvalues under BM-inf | REFEREE-authored candidate, GAP pending Claude (A-REV6); not applied to W4-SHARE | A-REV3/REVIEW.md; T38-RECORD/REGISTRY_v2.md | [pos 807] | feeds: none (K98 dropped) |
| CJ208 | T32(c) log^3; R5 (A-REV6 BOOK); Astra candidate bound; Corollary T32(c) corrected | conjecture | Proposed corrected cost rate C_eval = O(max(n,p) p log^3(n+p) + p^2 log^2(n+p)) (calibration-iteration factor), polynomial; Astra candidate proof | REFEREE (Astra-authored candidate proof R5, pending Claude verification); the displayed log^2 rate is GAP | A-REV6/BOOK.md R5; T38-RECORD/T38_STATEMENT.md V19 | [pos 802] [pos 807] [pos 919] | dropped (only polynomiality claimed) |
| CJ209 | N3; N3 DP invariant; e4 tie-DP invariant; start-mode DP tie rule | open problem | The max-plus DP for S~0 = argmax pi0 returns the prescribed smallest-size, lexicographically smallest start-mode maximiser without enumerating ties (needed so that the LS0 emitted centre equals the prescribed start mode) | OPEN (final cards: 'the only open mathematical obligation in the chain'; W1PC2 D9 TRUE on 400 random instances, DESIGN-ASSERTED); on {pi0(S°)>1/2} the tie rule is never used (W5-VMASK row 26) | MEET-THM/REGISTRY_PAPER1.md; MEET-THM/THEOREM_LIST_FINAL.md (M5 card); W5-VMASK/REPORT.md row 26 | pos: n/a (theorem meeting, after the campaign range) | M5 first lemma; fallback (b1-LH) conditional on N3 |
| CJ210 | ORTH-joint; ORTH joint family; ORTH composition; a6 | conjecture | Joint family for (a) with (P): X'X=(n-1)I, p<=n-1, fixed theta, so Theorem 1, Theorem 2(iii), Theorem 5(a) and Theorem 6 hold jointly | PROOF SKETCH (W2-T26 Prop. C); W4-T38FULL 'new composition checked line by line here' (a6 PROVED-UNDER the verified a3, no verifier); A-REV4 and A-REV6 GAP; registry ORTH-joint conflict | W4-T38FULL/T38_PROOF.md s2.3; W4-T38FULL/T38_STATEMENT.md a6; T38-RECORD/T38_STATEMENT.md III.6 | [pos 364] [pos 919] | none (campaign-only) |
| CJ211 | a8; in-sample favourable regime for iid S1/S3/S4/S6 designs; partition-noise decoupling | conjecture | In-sample favourability of the start for the iid study designs S1/S3/S4/S6 needs partition-noise decoupling | GAP; CONJECTURE (W4-T38FULL a8); not cross-family reviewed | W4-T38FULL/T38_STATEMENT.md II.2 a7-a8 | [pos 364] | none (campaign-only) |
| CJ212 | P(U) -> 0; delivery of output; K82; FW13; probability of resource_limit | open problem | Show P(U) -> 0 (or any law of G or of calibration failure); not provided by Theorem 5; every output theorem is joint with O in liminf form | OPEN (Not claimed); FUTURE_WORK FW13 (K82); no route | T38-RECORD/T38_STATEMENT.md I.E; MEET-THM/FUTURE_WORK.md; W6-FIXREV1/REPORT.md s8 | [pos 570] [pos 919] | FUTURE_WORK FW13 (K82) |
| CJ213 | N2(c); integrated LS0; OP-LS0; LS0 in the production core | open problem | LS0 is executed with its centre emitted and scans completed on every counted fit (OP-LS0); production core has no LS0; an in-engine integrated test fit (merged-LS0 replay) is still to run | OPEN as an implementation premise (T38-RECORD II.7 obligations; MEET-v31/METHOD_v3.1_FINAL.md line 48: 'not yet in the production core, and the integrated replay is pending'; final cards N2(c) pending); O-LS0 data: 0/2,394 HPM changes in the post hoc export | T38-RECORD/T38_STATEMENT.md II.7; API-AUDIT/REPORT.md s3; O-LS0/REPORT.md; campaign/HQ/SR_AUDIT.md; MEET-v31/METHOD_v3.1_FINAL.md | [pos 374] [pos 514] [pos 523] [pos 526] [pos 541] [pos 774] [pos 796] | M5 named premise OP-LS0 / N2(c) |
| CJ214 | D1; output convention decision; strict O versus HPM convention O_H | open problem | Decision: strict output convention O := {st in {exact, completed}} (default) or HPM convention O_H := {HPM reported and st != resource_limit} | open decision (HQ and Felipe); W8-SYNTH recommends strict; v3 states both; MEET-v31 decision 12 later fixes the guarantee form P{O, .} on the output event | T38-RECORD/T38_STATEMENT.md IV D1; W8-SYNTH/SYNTHESIS.md s4.12; MEET-v31/MINUTES.md decision 12 | [pos 570] [pos 919] | M5 (strict convention, joint with O) |
| CJ215 | D2 (T38-RECORD Part IV); Theorem 5(b) headline decision; LS0 headline versus no-LS0 headline | open problem | Decision: headline of Theorem 5(b) is (b1-LH) with LS0 or a no-LS0 LH theorem ((b2-LH) on STAB-LH, (b1'-LH) for c=1) | open at v3 (condition met: A-REV7 verified a route; API-VSTAB later verified the STAB certificate [pos 978]); v3 states both and does not choose; final M5 card: (b1-LH) with LS0 as main clause, (b2-LH) as labelled no-LS0 variant (K70) | T38-RECORD/T38_STATEMENT.md IV D2; W8-SYNTH/SYNTHESIS.md s1; MEET-THM/THEOREM_LIST_FINAL.md (M5) | [pos 796] [pos 919] [pos 978] | M5 (b1-LH) + (b2-LH) variant |
| CJ216 | III.8; (b1') under O_H; D_n^{sl} -> 0 for (b1') automatic | hypothesis | v2 sentence: under the HPM convention (b1') has D_n^{sl} -> 0 as well because S_cal contains the pilot | open (T38-RECORD III.8): A-REV1 s7.4 asks to add the usable no-score output term when the pilot stage does not execute; A-REV5 verified the output interface but did not address this sentence | T38-RECORD/T38_STATEMENT.md III.8; W6-FIXREV1/T38_STATEMENT.md; A-REV1/REVIEW.md s7.4 | [pos 570] [pos 919] | none (HPM convention not carried) |
| CJ217 | FMP-DELIVPOP; DELIV-POP; population delivery | open problem | Whether the end-of-stage-T population (not just one particle) lies in a repair basin X with delta_X->0 in the masked regime; stronger than T38 DELIV | OPEN (SF none; XF none) | F-MASKPIP/REPORT.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | FUTURE_WORK FW7 (K58) |
| CJ218 | E4 resolved half; V11; evidence O_P(sqrt(T/N)) when the grid resolves the crossing; N4(iii) | conjecture | If both members of the dominating pair are in V then log Z-hat_r - log Z = O_P(sqrt(T/N)) + leakage | CONJECTURE (PROOF SKETCH E3(c)); not reviewed | API-MASKZPIP/PROOF.md; API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | FUTURE_WORK FW2; K53 (N4(iii) OPEN/CONJECTURE) |
| CJ219 | O-PW2 non-vacuity; L2 mixing certification; BW_W | open problem | Certify per fit an L2 mixing premise lambda_t(1+g-bar_t lambda_t)<=kappa<1 and sup-norm control of h_{s,T} so that Theorem B/C are non-vacuous at study N,T | OPEN (confidence card medium) | O-PW2/REPORT.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | FUTURE_WORK FW2; K53 |
| CJ220 | ADRAFT-maskedPIP; masked-regime PIP/evidence guarantees for unmodified v3 | open problem | Whether PIPs and evidence are accurate in the masked regime for unmodified v3 | OPEN (author Astra; no review) | A-DRAFT/REPORT.md | [pos 493] [pos 494] [pos 563] [pos 616] [pos 677] | FUTURE_WORK FW2, FW7 |
| CJ221 | VAL-FP measurement; N16; validated arithmetic | open problem | Measure VAL-FP(eta,epsilon) by exact/long-double replay of production fits | OPEN (measured at p<=40 only, eta heuristic, per later meeting K107) | W2-BOOK/REPORT.md; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | FUTURE_WORK FW16 (K107) |
| CJ222 | ELS-1; E_LS ledger data fact; final local search 0 moves | hypothesis | [data fact] Final local search made 0 moves in 2,394/2,394 completed PROD-H fits; S0 scored in every completed fit (store F(S0) equals offline F(S0) to 1e-12); E_LS empty (0/2,394) | data from production ledgers (S-ELS); consistent with O-LS0 | S-ELS/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2 | [pos 715] S-ELS launch; [pos 717]; [pos 763] result; [pos 937]; [pos 1111] | none (campaign-only); n=200 disclosure CJ239 |
| CJ223 | ELS-2; classification of the 2,400 fits | hypothesis | [data fact] 1,829 exact recoveries, 565 strict posterior misses (F(S0)<F(S-hat); smallest margin 0.0049 nats; 23 within 0.1), 0 search misses, 0 ties, 6 resource-limit stops (all S5) | data (S-ELS); O-SWAP "4 no-output fits" superseded | S-ELS/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2 | [pos 715] S-ELS launch; [pos 717]; [pos 763] result; [pos 937]; [pos 1111]; [pos 796] | none (campaign-only) |
| CJ224 | ELS-3; the 541 unrepaired centres forced by Lemma 0 | hypothesis | [data fact] All 541 fits with S_c in R_2 minus {S0} have F(S0)<F(S_c) (median gap -1.33, range -9.05..-0.0049); S0 a one-move neighbour in 434; W3-VT37R sampled F(S0)>F(S_c) not reproducible | data; settles Lemma0(b) on the study data only | S-ELS/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2 | [pos 715] S-ELS launch; [pos 717]; [pos 763] result; [pos 937]; [pos 1111] | none (campaign-only) |
| CJ225 | ELS-4; strict same-size misses at c=0.5 | hypothesis | [data fact] 201 of the 488 posterior misses at c=0.5 are strict same-size (161 single swaps); size offsets -3..+2: 5, 21, 142, 201, 106, 13; only 6 same-size-offset misses at c=1 | data (the audit A-REV4 B5 asked for) | S-ELS/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2 | [pos 715] S-ELS launch; [pos 717]; [pos 763] result; [pos 937]; [pos 1111] | none (campaign-only) |
| CJ226 | LS0-1; LS0 post hoc outcome-neutral | hypothesis | [data fact] LS0 post hoc on all 2,400 regenerated fits: best LS0 model never beats the production HPM (0/2,394); recovery unchanged (1,119/1,200 at c=1, 710/1,200 at c=0.5); job B reproduced job A exactly | data (O-LS0-WRAP aggregation); Owls regeneration != NOTS bits (F(S0) agrees to 5e-8; every margin >= 0.002) | O-LS0/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2; campaign/LEDGER.md | [pos 399] [pos 400] launch; [pos 465] [pos 467] relaunch; [pos 514] [pos 526] LS0 approval conditional; [pos 760] O-LS0-WRAP; [pos 774]; [pos 793]; [pos 796]; [pos 1107] | M5 numerical companion (0/2,394 HPM changes); method decision LS0 part of v3.1 |
| CJ227 | LS0-2; T38(b1) premises at n=200 | hypothesis | [data fact] (M1) pi0(S~0)>1/2 in 18/2,400; (M2) D_S on all of Lat in 17/168 (c=1) and 1/129 (c=0.5); (M3) lambda_min >= 0.056; cap l >= Phi(S~0)-1 in 1,968/2,400; LS-score implication held in all 18 fits meeting its premise | data; (M1) evaluated at data-dependent S~0 | O-LS0/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2; campaign/LEDGER.md | [pos 399] [pos 400] launch; [pos 465] [pos 467] relaunch; [pos 514] [pos 526] LS0 approval conditional; [pos 760] O-LS0-WRAP; [pos 774]; [pos 793]; [pos 796]; [pos 1107] | none (campaign-only) |
| CJ228 | LS0-3; LS0 cost | hypothesis | [data fact] LS0 median 0.17 s (p=500), 0.37 s (p=1000), about 5e4 and 1.1e5 scores, under 0.1% of a fit | data | O-LS0/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2; campaign/LEDGER.md | [pos 399] [pos 400] launch; [pos 465] [pos 467] relaunch; [pos 514] [pos 526] LS0 approval conditional; [pos 760] O-LS0-WRAP; [pos 774]; [pos 793]; [pos 796]; [pos 1107] | none (campaign-only) |
| CJ229 | LS0-4; integrated LS0 test fit not run; LS0-EMIT | open problem | Whether the post hoc union equals an integrated in-engine LS0 run is untested (emit_centre=true and HPM tie rule for argmax pi0 required) | OPEN implementation check | O-LS0/REPORT.md; T38-RECORD/REGISTRY_v2.md section D2; campaign/LEDGER.md | [pos 399] [pos 400] launch; [pos 465] [pos 467] relaunch; [pos 514] [pos 526] LS0 approval conditional; [pos 760] O-LS0-WRAP; [pos 774]; [pos 793]; [pos 796]; [pos 1107] | M5 risk list (integrated-LS0 replay N2(c) pending) |
| CJ230 | Upper bound on Pi(X); Pi(X) finite-n envelope; K94 | open problem | Finite-n upper bound on the posterior-miss probability Pi(X)=P0(S-dagger != S0 / X) at n=200 (e.g. P0(L/X)+r_n(X)) | OPEN (Envelope GAP); remainder Pi-P0(L) measured <= 1.1 points per cell, not bounded | API-N200/REPORT.md; API-N200/PROOF.md | [pos 906]; [pos 929]; [pos 978] | FUTURE_WORK FW14 (K94) |
| CJ231 | SuSiE/SSL effective-threshold conjecture | conjecture | A selector with a higher effective inclusion threshold wins at c=1 (supersets removed) and loses at c=0.5 (weak-truth drops); SuSiE/SSL actual thresholds not derived | CONJECTURE (author O-SWAP); unreviewed | O-SWAP/REPORT.md | [pos 577]; [pos 742]; [pos 937] | none |
| CJ232 | Rigorous bracket for predictor T2; Sidak/Royen route | open problem | Two-sided bracket on P(L/X) at c=0.5 controlling the dependence of Z_jl across l | OPEN | O-SWAP/REPORT.md | [pos 577]; [pos 742] | none |
| CJ233 | Whole-model Assouad/Fano floor | open problem | Lower bound over the 14 truths and their look-alikes beyond the pairwise Le Cam floor | OPEN | O-SWAP/REPORT.md | [pos 577]; [pos 742] | none |
| CJ234 | Per-fit confidence certificate; upper bound on Z | open problem | A data-computable certificate of pi(S-hat) >= c or S-hat global HPM needs a certified upper bound on Z (PW2, UB, enumeration, bound on Delta) | OPEN as a practical per-fit item; no lower bound from unbiasedness alone (C1(c) VERIFIED non-implication) | O-CERT/REPORT.md; O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 706]; [pos 763]; [pos 917] [pos 919] | none |
| CJ235 | A-priori VAL-FP epsilon; path-free fp argument; preprocessing error | open problem | Control of the path-agreement probability epsilon of VAL-FP and of preprocessing error without replay | OPEN (epsilon a priori vacuous; measure by replay) | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md | [pos 711]; [pos 742] | FUTURE_WORK FW16 (K107); N16 |
| CJ236 | PA error to probability bound | open problem | Anti-concentration margin for the score gap at 0 to turn the O-SWAP PA error into a bound on miss probability | OPEN (routine but unwritten) | O-SWAP/REPORT.md; API-N200/PROOF.md | [pos 577]; [pos 978] | none |
| CJ237 | Finite-n Gibbs-route discovery bound; T38(b) at n=200 | open problem | A finite-n bound on P(O, S0 not scored) for the Gibbs route; a-priori routes give Q_f pi0(S0) <= 1e-6 | OPEN (discovery term measured 0/2,394, not proved) | API-N200/REPORT.md; API-N200/PROOF.md | [pos 906]; [pos 978] | FUTURE_WORK FW26 |
| CJ238 | Bookkeeping: C5 screening event over 2,400 fits; per-dataset matching; eta_F replay | open problem | Tabulate {S0 in U(X,y,S-hat)} over the 2,400 fits; match O-SWAP realised check with SMC outputs dataset by dataset; replay eta_F in long double/mpfr | OPEN bookkeeping | API-N200/REPORT.md; O-CERT/REPORT.md | [pos 906]; [pos 978]; [pos 706] | none |
| CJ239 | n=200 disclosure paragraph; W8-SYNTH section 1 decision 3 | hypothesis | [proposed target] Draft paragraph: 6 stopped, 1,829 exact, 565 posterior misses, 0 search misses; dilution start mass 1e-11..1e-26; thresholds ~2e6; beta-min shortfall 43x; 2^B >= 1e3; we bound P(reported and wrong) | Proposed wording (W8-SYNTH); HQ recommends use with corrected numbers [pos 796]; numerical caveats listed in the item | W8-SYNTH/SYNTHESIS.md; W8-SYNTH/BRIEF.md; W5-LOCKBOOK/STATEMENTS.tex | [pos 756] launch; [pos 763]; [pos 793]; [pos 796] | none (scale disclosure FW22 not a theorem) |
| CJ240 | API-N200 draft paragraph for the paper n=200 section | hypothesis | [proposed target] Paper wording of N200: P(no output or S-hat != S0) <= P(no output)+P0(S-dagger != S0 / X)+P(output, S0 never scored); lower bound predicts 552 posterior misses against 565 observed | Proposed wording (candidate); theorem author-only | API-N200/REPORT.md; API-N200/PROOF.md | [pos 906]; [pos 978] | M5 (via TH334) |
| CJ241 | O-SWAP realised one-move check reproduces observed misses | hypothesis | [data fact] Realised one-move check on the study's own regenerated data reproduces observed SMC-BVS miss counts in all 24 cells to within +-1: 39/37/227/257 against 40/37/230/259 | empirical; per-cell counts only; A-REV9: data provenance audit needed | O-SWAP/REPORT.md; O-SWAP/out/TABLES_local.md; API-N200/results/n200_table.md | [pos 578]; [pos 742]; [pos 978] | none |
| CJ242 | O-SWAP predicted rates T2 vs observed | hypothesis | [data fact] T2 gives 43/40 misses per 600 at c=1 vs 40/37 observed and 251/271 at c=0.5 vs 230/259; RMS z 0.86 (c=1) and 1.38 (c=0.5) against T2 | approximation vs data; unreviewed; A-REV9 GAP | O-SWAP/REPORT.md; O-SWAP/out/TABLES_local.md | [pos 577]; [pos 742] | none |
| CJ243 | API-N200 24-cell table; predicted 558 vs observed 571 | hypothesis | [data fact] Observed wrong 571 = U 6 + 565 posterior misses; predicted 558.1 = U + sum MC P0(L/X); c=1: 81.8 vs 81; c=0.5: 476.3 vs 490; RMS z 1.08 over 24 cells; max /z/ 2.52 | author-only; minor internal inconsistency in the z-count text | API-N200/REPORT.md; API-N200/results/n200_table.md | [pos 906]; [pos 978] | M5 evidence only |
| CJ244 | API-N200 exact enumeration at p=12 | hypothesis | [data fact] n=40, p=12, s0=3: nine tabulated rows: Pi between 0.077 and 0.789; 2 E0 delta1 between 0.934 and 1.812 (c=0.35 rows: Pi 0.89-0.96, 2 E0 delta1 1.85-1.95); P(pi(S0)<=1/2) 0.30..0.995; L within 0.2-1 point of Pi at c=1 | author-only computation; one design per kind | API-N200/REPORT.md; API-N200/results/small_p_exact.txt | [pos 978] | none |
| CJ245 | O-CERT section 4 illustration; registry OCERT-§4 conflict | hypothesis | [data fact] Four p=500 n=200 production fits: scores agree to <= 2.8e-12; local certified; box B&B certifies S-hat over 2^30..2^31 models in <= 38 s; pi(S-hat) <= 0.37 even when S-hat=S0; both c=0.5 misses certified posterior misses (g_del 1.19, 1.89) | candidate; added after O-VCERT review (heads 0edc58f/332bf3e); not reproduced or re-reviewed; source conflict C21 | O-CERT/REPORT.md; O-VCERT/REPORT.md; T38-RECORD/REGISTRY_v2.md | [pos 620]; [pos 702] [pos 706]; [pos 763] | none |
| CJ246 | W7-SEC measured T33 numerical margins at n=200 | hypothesis | [data fact] Production scorer vs 60-digit reference: max /Dlog m/ 1.3e-13..1.3e-10, ratio to rigorous eta_m <= 8.4e-3, to eta_eng <= 4.2e-2; constants errors <= 1.8e-12; chol route only, no Q recompute | author runs, seeded; unreviewed (A-REV9 deferred) | W7-SEC/REPORT.md; W7-SEC/PROOF_T33.md | [pos 711]; [pos 742] | FUTURE_WORK FW16 (K107) |
| CJ247 | W8-SYNTH 4.13 numerical inconsistencies | hypothesis | [data fact] Table of quantities with conflicting values across reports (start mode 6-12/2.5-6/7 of 14; favourable-n 590-730/800-1,600/1,050-3,200; beta-min 43x vs 100x; stopped fits 6 vs 4; LS0 cost; L+4 vs L+5) | Open reconciliation; recommendation: use S-ELS for counts | W8-SYNTH/SYNTHESIS.md | [pos 763]; [pos 796] | none (disclosure) |
| CJ248 | Box B&B cost heuristic 2^(ambiguous variables) | conjecture | Branch-and-bound tree size grows like 2^(number of ambiguous variables in U), not 2^/U/ | Heuristic remark, "not part of C4" (O-VCERT S4); measured 2e3-8e4 nodes at /U/=30-31 | O-CERT/REPORT.md; O-VCERT/REPORT.md | [pos 706]; [pos 763] | none |
| CJ249 | Prop 1; draft Prop 1 MH exactness | conjecture | Draft target: MH exactness (merge proposal inside MH with full posterior ratio) | proposed by the draft; F-DRAFT class (a) covered by T09(ii) PROVED-LOCKED | F-DRAFT/CROSSWALK.md | [pos 482] [pos 487] [pos 563] [pos 616] | feeds: none (covered by T09; remark W0(iv)) |
| CJ250 | Prop 2; draft Prop 2 SMC consistency | conjecture | Draft target: SMC consistency for a local-to-global path | proposed by the draft; class (a)/(b): T09, T12, T31(i), T14/T15, W2-T26 Thm A; T16 conjectured and dropped | F-DRAFT/CROSSWALK.md | [pos 482] [pos 563] [pos 616] | feeds M1 Theorem V/H; stage-count premise M7 K26, FW6 |
| CJ251 | Section 5.3 Theorem 1; draft weight stability under weak cross-block dependence | conjecture | Draft target: divergence between product of block posteriors and posterior controlled by cross-block covariance, so importance-weight variance bounded | proposed by the draft; class (b)+(d); mechanism false for v3 tables (RF256); replaced by TH350, TH362, TH363; final card M2 Theorem WS | F-DRAFT/CROSSWALK.md; F-DRAFT/NEW_TARGETS.md; O-WSTAB/REPORT.md | [pos 482] [pos 487] [pos 491] [pos 563] [pos 616] [pos 748] [pos 1441] [pos 1449] | feeds M2 Theorem WS (K102, K10, K11, K25, K53) |
| CJ252 | Section 5.4; draft approximation error | conjecture | Draft target: approximation error (KL, TV, PIP and joint-inclusion error) | proposed by the draft; class (b) largely covered; W4 sketch (CJ259) | F-DRAFT/CROSSWALK.md | [pos 563] [pos 616] | feeds: none (campaign-only) |
| CJ253 | Section 3.2; draft naive union merge distorts uncertainty | conjecture | Draft target: naive union merge distorts uncertainty | proposed by the draft; class (c); became F-DRAFT Prop NM (ERROR, A-REV4) and A-DRAFT Prop M (theme 11) | F-DRAFT/CROSSWALK.md | [pos 563] [pos 616] [pos 957] | feeds paper-1 introduction Prop 0 (theme 11) |
| CJ254 | Section 13.1; draft convergence of E[h(theta)] estimates | conjecture | Draft target: convergence of estimates of E[h(theta)] | proposed by the draft; class (a)/(b); A-DRAFT Theorem A/D (theme 8); Remark H = TH376 | F-DRAFT/CROSSWALK.md | [pos 563] [pos 616] | feeds: none here (theme 8) |
| CJ255 | Section 13.3; draft partition as a random variable; stochastic scheduling | conjecture | Draft target: the partition as a random variable to be inferred | proposed by the draft; class (c); fate Prop P = TH375 (design variable, not parameter) | F-DRAFT/CROSSWALK.md | [pos 563] [pos 616] | feeds: none (mixture start theme 3) |
| CJ256 | F-DRAFT Theorem W; FD-W(a); FD-W(b); FD-W(c) | conjecture | One-step weight stability in favourable BO regime: (a) 1+chi2>=p^{R2-eps}/sqrt n, (b) 1+chi2<=1+p^{R2+eps}/sqrt n+o(1), (c) log(1+chi2)=[R2 log p-1/2 log n]_+ +O_P(log log p) | (a) PROVED-UNDER modulo W2 (W2 ERROR per A-REV4); (b) PROOF SKETCH; (c) CONJECTURE; (b),(c) refuted on divergent side (RF252, RF253); SF none; XF none | F-DRAFT/NEW_TARGETS.md | [pos 489] [pos 616] [pos 748] | replaced by TH362; feeds M2 only through H-ORTH (not used) |
| CJ257 | F-DRAFT Conjecture W prime; FD-W′ ideal grid stage count | conjecture | Ideal ESS-0.9 grid has T=ceil(log2(1+1/g))+O(1) stages with g=log(sqrt n/9)/(R2 log p); T=O(1) for p<=n^A | CONJECTURE (skeleton); resolved under ORTH by TH363, conditionally by TH367 | F-DRAFT/NEW_TARGETS.md | [pos 616] [pos 733] | feeds: none (K29 DRAFT-ONLY) |
| CJ258 | F-DRAFT Lemma W3; FD-W3; cross-block covariance term | conjecture | Dropping BO adds a second additive term d=d_BO+(n/2)sum beta^T E beta/(1-R2)+O(n//E//^2//beta//^2) | PROOF SKETCH (no SF, no XF); O-WSTAB did not prove it; role taken by TH351 and card M2 (a1) | F-DRAFT/NEW_TARGETS.md | [pos 616] [pos 748] | feeds M2 (a1) route (K11) only as PROOF SKETCH of Seat C |
| CJ259 | F-DRAFT Proposition W4; FD-W4 | conjecture | KL and TV O_P(n^-1/2 polylog) while chi2 can diverge | PROOF SKETCH; A-REV4 GAP (TV VERIFIED; KL rate and chi2 assertion GAP); replaced by TH362(f), TH379 | F-DRAFT/NEW_TARGETS.md; A-REV4/DRAFTS_CHECK.md | [pos 616] [pos 677] | feeds: none |
| CJ260 | F-DRAFT Conjecture W″ window form; FD-W″-window | conjecture | Pair-dominated window costs 3pi+O(1) stages with the Theorem W count outside | CONJECTURE; the 3pi count refuted (RF255); replaced by TH368, TH369 | F-DRAFT/NEW_TARGETS.md | [pos 616] [pos 733] | feeds: none |
| CJ261 | WS6(e); OWS-WS6e; Renyi threshold alpha*=1+1/(2 A omega*) | conjecture | D_alpha(pi//pi0)->0 if A(alpha-1)omega*<1/2 and ->inf if >1/2; critical Renyi order alpha*=1+1/(2A omega*) | CONJECTURE (SF none; XF none); alpha=2 under ORTH resolved by TH362 | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds: none (M2 card: neither WS6e nor WS8d used) |
| CJ262 | WS8(d); OWS-WS8d; PW2 for the hybrid particle system | open problem | PW2 for the actual hybrid particle system at t>=2 (IID idealisation is not the method) | OPEN (SF none; XF none); replaced by O-PW2 Theorem A/B (theme 8) | O-WSTAB/PROOF.md | [pos 492] [pos 748] | feeds: none |
| CJ263 | Theorem W general BO with correlated blocks | open problem | Same dichotomy with r replaced by the realised dilution fraction; per-block SEP and EXP-prime | PROOF SKETCH / OPEN (P(true) 0.85, P(provable) 0.6 per author) | O-WSTAB/REPORT.md | [pos 748] | feeds M2 (a1) fallback route |
| CJ264 | Theorem W for p ~ n under ORTH | open problem | Dimension control for the doubled law q2 (T02 analogue for varpi BF^2/prod r_b) | OPEN (author) | O-WSTAB/REPORT.md | [pos 748] | feeds: none |
| CJ265 | W prime for the method V-restricted pilot grid | open problem | Same stage count for the V-restricted pilot grid as for the ideal grid; COVER at the points w_t; pilot ESS vs rho_Omega | OPEN (author); A-REV9 production-grid transfer GAP | O-WSTAB/REPORT.md; O-STAGES/REPORT.md; A-REV9/REVIEW.md | [pos 748] [pos 733] | feeds FUTURE_WORK FW6 (K31) |
| CJ266 | Theorem W(d) upper side window p^r/sqrt n->0 but p^r sqrt(log p)/sqrt n not ->0 | open problem | Upper half of W(d) not covered in the window | OPEN (CHECK_SEP_W F1 gap; statement restricted) | O-WSTAB/review/CHECK_SEP_W.md; O-WSTAB/REPORT.md | [pos 748] | feeds: none |
| CJ267 | Boundary case 2Ar=1 of Theorem W and W prime | open problem | Behaviour exactly at 2Ar=1 (Gumbel O_P(1) fluctuations) | OPEN (A-REV9: equality is not resolved) | A-REV9/REVIEW.md; O-WSTAB/REPORT.md | [pos 748] | feeds: none |
| CJ268 | API-T26BUD Conjecture P; pilot stage count O_P(1) | conjecture | On ORTH-F N^pil=O_P(1), more precisely N^pil<=1+ceil(log2(1/eta_A)) w.p.->1 | CONJECTURE (author); as-coded masked count OPEN in final list (FW6, K31) | API-T26BUD/PROOF.md; API-T26BUD/REPORT.md | [pos 906] [pos 975] [pos 978] | feeds FUTURE_WORK FW6 (K31) |
| CJ269 | Hypothesis (LL); layer law at general w | hypothesis | 1/q_w(S0)-1=eps_n(w) with /log(9 eps_n(w))-lambda_n(w-1-g_n)/<=r_n uniformly on [1,2] | PROOF SKETCH (author); conflicts with F-DRAFT W(b) refutation for 2Ar>1 (registry C22) | O-STAGES/REPORT.md | [pos 733] [pos 748] | feeds FUTURE_WORK FW23 (K29) |
| CJ270 | Hypothesis PAIR | hypothesis | sup_{t in [0,2]} q_t(Omega minus {S°,S0})->0 | unproven; numerically supported (pair_out_max falls with n) | O-STAGES/REPORT.md | [pos 733] | feeds M7 (d) assumption |
| CJ271 | LH masking c>=2 chain of crossings stage count | open problem | Stage count when intermediate states S° u M′ create a chain of crossings | OPEN (author) | O-STAGES/REPORT.md | [pos 733] | feeds: none |
| CJ272 | Pilot fidelity; finite-H pilot vs T*_Omega | open problem | Relation of the finite-H empirical-ESS pilot to the population greedy grid | OPEN (author) | O-STAGES/REPORT.md | [pos 733] | feeds FUTURE_WORK FW6 (K31) |
| CJ273 | F-DRAFT method note plug-in sigma^2 tables | hypothesis | Building every block table with one shared plug-in sigma^2 would make draft section 5.3 literally true and unmask the start at n=200 | F-DRAFT P(true)=0.6 pilot question; rejected by HQ ([pos 919] common-sigma^2 start rejected: floods the start in study-like designs) | F-DRAFT/CROSSWALK.md | [pos 616] [pos 666] [pos 919] [pos 937] | feeds: none (rejected; F-SIGMA, O-MIX theme 3) |
| CJ274 | K97; Prop SL; Proposition SL; Theorem SL; C1new; C14; D9; M8; FW21; Song-Liang analytic separation | open problem | On LH with c linked pairs Song-Liang split-and-merge loses every masked hub w.p. -> 1 (hub population null in its subset, subset PIP -> 0 under SL prior at every iteration, FDR threshold) while v3.1 HPM = S0 | FUTURE_WORK FW21 (unanimous R3-3); C1new: COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (NEW-SYNTH); key step NEEDS-HYPOTHESIS (W1 PC1) then NOT REPAIRED (W2 PC1) | MEET-THM/FUTURE_WORK.md; MEET-THM/MINUTES.md; MEET-THM/R2_B.md; MEET-THM/evidence/W2_PC1/VERDICTS.md; THM-INV/digests/SL.md | [pos 1072] [pos 1608] [pos 1621] [pos 1626] | FUTURE_WORK FW21 (K97); Cor 2 wording: no analytic null-exclusion/FDR separation established; LIT-PAR G4 numerical evidence |
| CJ275 | ADRAFT-uncert; stronger uncertainty than complete Song-Liang | open problem | Whether v3 uncertainty beats the full two-stage Song-Liang method; needs a faithful comparator | OPEN (A-DRAFT; registry ADRAFT-uncert) | A-DRAFT/REPORT.md; W8-SYNTH/SYNTHESIS.md | [pos 616] [pos 796] | FUTURE_WORK FW21 (same open comparison) |
| CJ276 | ADRAFT-novelty; novelty of local-to-global SMC for BVS | open problem | Priority of the generic local-to-global idea against six works; adverse evidence strong (Lindsten et al., Schafer-Chopin) | OPEN (A-DRAFT; registry ADRAFT-novelty); F-REFEREE M6 notes missing Yang-Wainwright-Jordan and Zhou et al. | A-DRAFT/REPORT.md; LIT-SMC/REPORT.md; F-REFEREE/REFEREE_REPORT.md | [pos 563] [pos 616] | none (positioning; paper framed as when and why a scored-HPM SMC succeeds) |
| CJ277 | SEP-GUnulls; GU with data-chosen nulls in the centre | open problem | Prop GU for centres containing data-chosen nulls (NA/LD issue of W1-T37R) | OPEN (registry SEP-GUnulls); XF: none | W7-SEP/PROOF.md; W7-SEP/REPORT.md | [pos 763] | none |
| CJ278 | SEP-noLS0; no-LS0 T38(b) via GU; final search from S_pre inside R | conjecture | If best-scored S_pre is inside R (or GU extends to bounded nulls) the final production search scores S0 on LH without LS0 for every c | CONJECTURE (author); XF: GAP (A-REV7: actual best-scored centre may contain nulls outside R); HQ pos 919 wording 'Refuted ... Prop GU as a standalone no-LS0 route' (UNCERTAIN vs GAP) | W7-SEP/REPORT.md; A-REV7/REVIEW.md; T38-RECORD/REGISTRY_v2.md (row SEP-noLS0) | [pos 763] [pos 919] | candidate N6 of T38 v3 (no-LS0 use); none in final list |
| CJ279 | separation outside the frozen setting; posterior barrier; growing c_n; weak signals; move-limit binding | open problem | Where a bridge-vs-search or super-polynomial separation could live; none has a proved v3 route | not claimed (W7-SEP section 5); W4-SHARE design PB not asymptotic | W7-SEP/PROOF.md; W7-SEP/REPORT.md | [pos 763] | none |
| CJ280 | separation for evidence/PIP accuracy | open problem | A separation for Z-hat/PIP accuracy would need a family where pi does not concentrate | not claimed (T38 does not claim masked evidence/PIP accuracy) | W7-SEP/PROOF.md | [pos 763] | none (cf. F-MASKPIP, A-DRAFT ADRAFT-maskedPIP OPEN) |
| CJ281 | naive merge at growing p; NM normalisation, label-time occupancy, O(1) ideal-grid stage count | open problem | Growing-p normalisation, label-time occupancy and finite-threshold ideal-grid stage bounds for the naive-merge phenomenon | OPEN (A-REV4, A-REV6 residual obligations) | A-REV4/REVIEW.md; A-REV4/DRAFTS_CHECK.md; A-REV6/WEIGHTS.md | [pos 796] [pos 919] | none (K98 dropped) |
| CJ282 | S-GAP; gap claim; thesis/positioning: no BVS method is parallel + correlation-robust + strongly guaranteed; LIT-PAR verdict TRUE WITH QUALIFICATIONS | conjecture | Among published BVS methods none simultaneously (a) targets the exact model posterior with an unbiased evidence estimate, (b) parallelises in communication-free width (islands), (c) has a proved sequential-depth (stage-count) bound on a correlated design whose start is masked; every parallel BVS method with a theorem needs cross-split faithfulness (SaM), weak correlation (DECO, BB-SSL, Ray-Szabo, Yang-Pati-Bhattacharya), block-diagonal Gram (Papaspiliopoulos-Rossell), large-n plug-in consistency (DFP) or fixed-dimension shards (WASP, M-posterior, Zhang-Lam-Lin) | CONJECTURE (about the literature; evidence from §2) [LIT-PAR REPORT §4.1]; headline verdict "TRUE WITH QUALIFICATIONS"; confidence medium-high ("a literature claim can always be overturned by a missed paper; 2023-2026 coverage was by search, not exhaustive"); the literal sentence "methods with guarantees are sequential" is FALSE (RF268); the planned Astra novelty cross-check is not found in the sources | LIT-PAR/REPORT.md §1, §4.1, §7; LIT-PAR/notes/01-09; campaign/LEDGER.md (13:03 UTC 2026-11-03) | [pos 1030] [pos 1038] [pos 1044] [pos 1070] [pos 1107] | Thesis CD (K96, scoped remark); M8 Proposition D remark (K90); FUTURE_WORK FW21 |
| CJ283 | LIT-PAR TH6; Mathews-Schmidler 2024 template; T38(a) and T32(i) as BVS instances of Mathews-Schmidler Thm 1 | open problem | Whether T38(a) (favourable) and T32(i) reduce to Mathews-Schmidler (AAP 34(1) 2024) Thm 1: SMC error <= eps w.p. >= 3/4 if N >~ poly(V,W,Z,1/mu_star)/eps^2 and t >= max local (restricted-kernel) mixing times; if so they become corollaries and must be framed as BVS verifications of that template | unchecked (LIT-PAR TH6 severity medium; §5 escalation item 2; THM-SYNTH REPORT §1 item 4: "left as escalations with a named check") | LIT-PAR/REPORT.md §2.3, §3.2 TH6, §5; THM-SYNTH/REPORT.md §1 | [pos 1070] [pos 1185] | M5 Theorem HPM novelty note (T38(a)); none |
| CJ284 | LIT-SMC T1; O-STAGES Theorem G(i) + Lemma 1 = Stefankovic-Vempala-Vigoda 2009; Chebyshev cooling schedule | conjecture | O-STAGES Theorem G(i) (the greedy ESS grid is the shortest valid grid), Lemma 1 (convexity => monotonicity) and implicitly Lemma 0 (Phi = Renyi-2) are in Stefankovic-Vempala-Vigoda (arXiv cs/0612058; FOCS 2007; J. ACM 56(3) 2009): the B-Chebyshev cooling schedule Z(2 beta_{i+1} - beta_i) Z(beta_i)/Z(beta_{i+1})^2 <= B equals the step rule exp Phi(u,v) <= 10/9 with w = 2v - u, and "the optimal Chebyshev cooling schedule can be obtained in a greedy manner" by convexity of ln Z; action: cite SVV and present G(i) as known; G(ii) pilot-refinement sandwich is a routine v3-specific extension | literature identification (LIT-SMC §0 item 1, §3 T1: "Threat"); confidence high / cheap to settle high (LIT-SMC card); journal version not read; THM-SYNTH D2: "G(i) KNOWN-CITE"; not a mathematical status change of O-STAGES | LIT-SMC/REPORT.md §0, §1B #9, §3 T1, §5; THM-SYNTH/THEOREM_LIST.md (D2) | [pos 983] [pos 1009] [pos 1177] | M7 Theorem STG (K26; citation wording) |
| CJ285 | LIT-SMC T2; LIT-PAR TH4; O-STAGES item 4 dense limit sqrt(c) T* -> L = Syed et al. global barrier Lambda | conjecture | The dense-schedule part of O-STAGES, sqrt(c) T*(c) -> L = Integral_0^1 sd_{q_phi}(d) dphi as c -> 0, is the Syed-Bouchard-Cote-Chern-Doucet (arXiv:2408.12057v2) global barrier Lambda (lim T Var[Zhat/Z] = E(phi)/N >= Lambda^2/N, Thm 3; lambda(beta) = sd_beta(V) for MCMC kernels on the geometric path); items 1-3 (coarse-grid T* = log2 A0 + O(1), L <= pi while T* -> infinity) are not in it | literature identification (LIT-SMC §3 T2; LIT-PAR §2.3, TH4 medium; notes/08); "Present item 4 as a corollary or analogue, not as new"; confidence high; THM-SYNTH D2(d) KNOWN-CITE | LIT-SMC/REPORT.md §3 T2; LIT-PAR/REPORT.md §2.3, §3.2 TH4; LIT-PAR/notes/08_syed_barrier_vs_ostages.md | [pos 983] [pos 1009] [pos 1070] | M7 Theorem STG (citation wording); none |
| CJ286 | LIT-SMC T4; O-PW2 Theorem A versus Cerou-Del Moral-Guyader 2011 Thm 1.4 | conjecture | O-PW2 Theorem A, N Var_c(W_T) = Sum_{s<T}(1-1/N)^{T-1-s}(E_c[W_s^2 mu_s(h^2_{s,T})] - 1), is an exact assumption-free second-moment identity of the same kind as CDG (AIHP 47(3) 2011) Thm 1.4, E[gamma_n^N(1)^2] = gamma_n(1)^2 Sum_{s=0}^{n+1}(1-1/N)^{(n+1)-s}(1/N^s) v_n(s) (alpha = 0, multinomial selection), so it should be presented as a form of the exact Feynman-Kac second-moment decomposition, not new; Theorem B (two-sided, O(N^{-3/2})) and Theorem C (PW2 counterexample a_t = chi^2_t) may carry novelty | CONJECTURE-level reading (forms compared, not derived) [LIT-SMC §3A]; confidence medium-high that Thm A is not new; escalated; O-PW2 Thm A itself PROVED, XF VERIFIED (A-REV9) | LIT-SMC/REPORT.md §1A #2, §3 T4, §3A, §5 item 1; THM-INV/REPORT.md §6 | [pos 1009] [pos 1107] | S-Z (K39); none |
| CJ287 | LIT-SMC T3; LIT-PAR TH2; Prop 2 / T12 / T31(i) are standard; KNOWN-CITE | conjecture | Frozen-run unbiasedness (Del Moral et al. 2006; Dai-Heng-Jacob-Whiteley 2022 two-pass recipe; Whiteley-Lee-Heine 2016), the Markov 0.05 Zhat lower bound (Grosse-Ghahramani-Adams 2015), islandwise averaging (Dai et al.; Verge et al. 2015) and Zhat-weighted pooling consistent as R -> infinity at fixed N (Whiteley-Lee-Heine 2016 s5.1; Dai et al. (4.8); Liang et al. 2024 Thm 3.1 "parallel strong scaling") are standard; only the negative items (pooled x pooled is not an identity; E[Zhat / completed] != Z) are genuinely non-standard | literature identification (LIT-SMC §3 T3; LIT-PAR §2.3, TH2 high, TH3 medium); confidence high (cheap to settle: cite); THM-SYNTH: KNOWN-CITE; THM-INV D4: Verge (plain averaging) and WLH (Zhat-weighted) are right about different poolings | LIT-SMC/REPORT.md §1A #3-6, §3 T3; LIT-PAR/REPORT.md §2.3, §3.2; THM-INV/REPORT.md §2 (D4) | [pos 1009] [pos 1070] [pos 1107] | M1 Theorem V/H (cited lemmas K35, K36, K48); S-POOL |
| CJ288 | LIT-SMC G1-G2; discovery gap; masked start = low persistence (Woodard-Schmidler-Huber 2009) | conjecture | No SMC theorem in the literature read addresses whether the run scores a given state or whether the best-scored model is correct (general finite-sample theory: Marion-Mathews-Schmidler 2023; Mathews-Schmidler 2024; Le Fay-Chopin-Vihola 2026; Paulin-Jasra-Thiery 2019 need bounded chi^2/weight ratios plus mixing times, and mu_star bounded below); the masked regime violates the premise (pi0(S0) ~ e^{-A0}) and is Woodard-Schmidler-Huber low persistence; on LH the low-conductance ingredient is absent (S0 unique local mode); T21/Thm 4, T38 and the masked Zhat results (F-MASKPIP M1-M3) are outside existing SMC theory | literature-gap claim (LIT-SMC §0 item 4, §2 G1-G2); confidence high that it is a gap; 2023-2026 SMC-for-BVS search by two web searches only, not exhaustive | LIT-SMC/REPORT.md §0 item 4, §1C #18-20, §2 G1-G5, §4 | [pos 983] [pos 1009] | M5 Theorem HPM novelty; M6 (framing) |
| CJ289 | LIT-MCMC L1; rapid-mixing hypotheses | conjecture | Every polynomial mixing-time theorem for BVS MCMC read (YWJ 2016, ZYVR 2022, Chang-Zhou, Zhou-Smith, Zhou-Chang, Atchade, Jiang) assumes (i) a unimodal-ratio landscape on a sparse space, R > M (RW-MH) or R > M^2 (informed), with a sparse cap s <~ n/log p and a prior penalty per extra variable of order p^kappa g^{1/2}, or (ii) a warm start whose support contains the truth; none assumes BB(1,p) with g = n and cap floor(n/2) | CONJECTURE (literature claim); high confidence for the works listed, unknown for unread works [LIT-MCMC §2.1 L1] | LIT-MCMC/REPORT.md §2.1 | [pos 983] [pos 1009] | FUTURE_WORK FW4 context; none |
| CJ290 | LIT-MCMC L2; no published BVS MCMC-slow / SMC-fast separation; OPEN | open problem | No published BVS family on which standard BVS MCMC provably mixes slowly while a tempering or SMC method provably succeeds; the only proved BVS slow-mixing example is YWJ App. A.2 (null truth, saturated-model trap), cured by a size cap, not by tempering; generic continuous-space separations (Mathews-Schmidler 2024) and tempering lower bounds (Woodard-Schmidler-Huber 2009) exist; Pozza-Zanella Cor 1 caps any multiproposal speed-up at the factor K | OPEN (as a literature claim); medium confidence [LIT-MCMC §2.1 L2]; search not exhaustive; consistent with the W7-SEP result "moving off the start is needed, not tempering" | LIT-MCMC/REPORT.md §0 item 2, §2.1, §6 Theta4 | [pos 983] [pos 1009] | FUTURE_WORK FW12 (K92 separation from single-chain MCMC) |
| CJ291 | LIT-MCMC L3; SMC theory needs global gaps or mode mass along the bridge | proposition | The general SMC finite-sample theorems (Mathews-Schmidler 2024; Le Fay-Chopin-Vihola 2026; Marion-Mathews-Schmidler) need either a spectral gap gamma > 0 for every kernel or local mixing plus mu_star = min mode mass along the bridge, with cost proportional to 1/mu_star; in the masked regime mu_star <= pi0(S0-basin) of order n^{-c/2} (T27 / Thm 2 masking law) | PROVED as a reading of the stated theorems (the hypotheses are quoted in N3 and N12); applying it to the masked start uses Thm 2's masking law (a candidate, not adopted) [LIT-MCMC §2.1 L3]; THM-INV D5: LIT-SMC and LIT-MCMC say "polynomially small", LIT-PAR "exponentially small"; THM-SYNTH settles: polynomially small on LH at fixed c, about 1e-12 on the study designs | LIT-MCMC/REPORT.md §2.1 L3; LIT-PAR/REPORT.md §2.3; THM-INV/REPORT.md §2 (D5); THM-SYNTH/REPORT.md §1 item 4 | [pos 983] [pos 1009] [pos 1177] | none (positioning) |
| CJ292 | LIT-MCMC G1; hitting/scoring time of S0 from conditions (1b)/(1c) alone is not published | conjecture | No published result gives a hitting or scoring time of S0 from the landscape conditions (1b) (underfitted models have a beneficial addition) and (1c) alone, without (1a) (overfitted-side drain), without a small cap and with a BB(1,p)/g = n prior; the repair theorems T37/GU and T38(b1) are of this type for greedy local search; Gamarnik-Zadik Thm 2.7 (local search from any k-sparse start, iid X, n >= C k log p) is the closest | CONJECTURE (literature), medium confidence [LIT-MCMC §0 item 4, §5 G1] | LIT-MCMC/REPORT.md §0 item 4, §5 G1, §6 Theta2 | [pos 983] [pos 1009] | M5 Theorem HPM novelty note; positioning paragraph |
| CJ293 | LIT-STAT H2; T03 sharp is a modest extension of Rossell 2022 and Moreno-Giron-Casella 2015; T02(i sharp) BB(1,p) tail novelty narrow | conjecture | Thm 1 (T03 sharp) is a modest extension of Rossell (2022, Bayesian Analysis 17(2)) and Moreno-Giron-Casella (2015): genuinely ours are BB(1,p) rather than BB(1,1), the cap K = floor(n/2) (not o(n)), the ridge slab and the size-cutoff device m-sharp_n; after the addendum BB(1,p) is BB(1,1) times a geometric size tilt (LM228), so T02(i sharp) is a modest extension, not a new mechanism; Prop 1 (T07) is standard or folklore (Barbieri-Berger 2004 Thm 1), Prop M (naive merge) is a known phenomenon for motivation (Papaspiliopoulos-Rossell 2017) | literature verdict (LIT-STAT REPORT §1, §11, §12): "Modest extension"; novelty confidence low-to-medium pending E1 (Martin-Mess-Walker 2017 not read); conflict: LIT-VENUE "standard in kind ... do not sell it"; Thm 1 itself PROVED, XF VERIFIED (T03 sharp) | LIT-STAT/REPORT.md §1, §4 H2-H9, §11, §12; LIT-VENUE/REPORT.md §5; THM-INV/REPORT.md §2 | [pos 983] [pos 1009] [pos 1107] | S-T (Theorem 1 T03 sharp, K93, K04); none |
| CJ294 | LIT-STAT H1; T03 sharp (3) P(S-dagger != S0) <= 2 E0[1 - pi(S0)] is Rossell 2022 Proposition 1 | conjecture | P(S-dagger != S0) <= 2 E_0[1 - pi(S0)] (T03 sharp clause (iii)) is Rossell (2022) Proposition 1 verbatim, and Rossell states it also holds for the MPM; the 2 E0 delta_1 term of Thm 4 (T21) and Thm 5(0) inherits it; the paper must cite it | KNOWN (LIT-STAT §1 item 2, §4 H1: "High for novelty, none for correctness"); wording proposed in §5 | LIT-STAT/REPORT.md §1 item 2, §4 H1, §5 | [pos 983] [pos 1009] | S-T (K93); M5 Theorem HPM (citation of the 2 E0 delta_1 term) |
| CJ295 | LIT-VENUE gaps G1-G5; nothing in the sample proves an SMC-BVS output theorem | conjecture | In a sample of 30 works no paper proves anything about the output of an SMC sampler for BVS (G1); no paper splits the reported-HPM error exactly into posterior miss + search miss + no output measurable per run (G2; informal precedent Garcia-Donato and Martinez-Beneito 2013 s4); none proves a lower bound for an iid start law with repair theorems (G3); per-fit certificates on model space at p ~ 1e3 are open (G4); no Lean-checked proofs (G5) | literature-gap claim (LIT-VENUE §1 item 4, §4); confidence medium-medium-high ("sample of 30 plus searches"); a second wider-net literature run was recommended (Shi-Dunson, South-Pettitt-Drovandi) and not found | LIT-VENUE/REPORT.md §1, §4, §8, §10 | [pos 983] [pos 1009] | M5 Theorem HPM; S-CERT; none |
| CJ296 | LIT-VENUE venue verdict; Biometrika conditional; JRSS-B a stretch | hypothesis | The package realistically supports Biometrika (5-result cut) only if Thm 5(b) is proved for the algorithm as run with the transition shown at growing n; JCGS, Bayesian Analysis, EJS or Statistics and Computing comfortably if the numerics are strengthened; JRSS-B a stretch; AoS not realistic; typically expected but missing: real-data analyses, head-to-head comparisons (LIT-MH, PARNI, MAdaSub, wTGS, SuSiE, SSL), simulations at growing n, a main theorem not tied to the LH family, external human review of AI-checked proofs | judgement, not a status word [LIT-VENUE §6]; confidence medium (Biometrika) / low (JRSS-B); later: HQ calibration at pos 933 "JRSS-B is realistic, probably after one major revision" (HQ opinion, conflicts in tone) | LIT-VENUE/REPORT.md §1 item 5, §6, §10 | [pos 1009] [pos 1018] [pos 933] | none (venue decision, outside cards) |
| CJ297 | API-POS open items; YWJ-type spectral gap for the paper prior on LH-G with cap K; unimodality beyond p <= 20; Y1 extension | conjecture | (a) a YWJ-style canonical-path or drift analysis for the paper prior (g = n, BB(1,p), cap K = floor(n/2)) on LH very likely succeeds; a spectral-gap bound for it on LH-G is OPEN; (b) S0 is the unique local mode on M(K) beyond the enumerated p <= 20 is OPEN; (c) the extension of YWJ/ZYVR from p >= n to LH-G with p_n -> infinity (Y1) is a CONJECTURE, very likely true | CONJECTURE (supported by §6 enumeration); (b) OPEN; author-only; LIT-MCMC Prop OB shows R > M cannot certify the paper prior, so a proof would need a different route | API-POS/REPORT.md §4.1 Y1, §5 R3(iii), §11 item 5, §13 | [pos 978] [pos 1009] | FUTURE_WORK FW4 (K24, N10) |
| CJ298 | THM-INV gap 1; accuracy of E_pi[h(S)] as n grows in the masked regime; joint inclusion probabilities; proposal s13.1 | open problem | Estimates of posterior expectations E_pi[h] (joint inclusion, functionals, PIPs at p >> n) converge to the truth as n grows in the masked (study) regime: nothing exists beyond the favourable-regime CONJECTURE (T26) and LH at fixed p (P1-P3); "the single most visible gap against the proposal" | NONE (no theorem of any status) [THM-INV §5 item 1]; addressed after the fact by THM-SYNTH Theorem H (PROOF SKETCH, TH412) and MEET-THM M1; unbounded h FW27 | THM-INV/REPORT.md §0 item 2, §3a, §5 item 1, §8 | [pos 1103] [pos 1107] [pos 1153] | M1 Theorem V/H (K51); FUTURE_WORK FW7, FW8, FW27 |
| CJ299 | THM-INV gap 3; a parallel work/depth theorem; the thesis sentence "correlation costs only depth and particles, never correctness" is not a theorem yet | open problem | No statement of work/depth versus p and correlation, no island-count theory beyond standard pooling, no comparison of depth with sequential MCMC; "never correctness" is fixed-data Monte Carlo validity (KNOWN-CITE), "costs only depth" is unproved; need depth as a function of p, correlation and masking and an R-versus-N trade-off; LIT-PAR warns the per-round depth is Theta(p) | NONE [THM-INV §0 item 3, §5 item 3]; answered at island level by Prop D (TH399; M8) and as a scoped remark (TH416) | THM-INV/REPORT.md §0 item 3, §3c, §5 item 3, §8 | [pos 1103] [pos 1107] [pos 1153] | M8 Proposition D; Thesis CD (K96) |
| CJ300 | THM-INV gap 4; delivery of output P(U) -> 0 | open problem | No theorem bounds P(resource_limit), P(schedule_limit), P(numerical_failure) or P(grid_unconverged); every consistency statement is joint with "output exists"; under v3.1 (concurrent islands, Prop W) the 6/2,400 wall-time stops get about 4x headroom | NONE [THM-INV §5 item 4]; THM-SYNTH R6: stated as a limitation in v1; final FUTURE_WORK FW13 ("No route") | THM-INV/REPORT.md §5 item 4; THM-SYNTH/THEOREM_LIST.md (R6); MEET-THM/FUTURE_WORK.md (FW13) | [pos 1103] [pos 1107] [pos 1177] | FUTURE_WORK FW13 (K82) |
| CJ301 | THM-INV gap 7; mixing / spectral gap of the phi = 1 move round (V10); D1 API-POS versus LIT-MCMC | open problem | No published or project theorem covers mixing of the phi = 1 round for the paper prior; the rapid-mixing route is blocked as stated; D1: API-POS puts the obstruction on the prior side and expects a YWJ-style proof to "very likely succeed", LIT-MCMC computes that R > M fails (n = 200, 1600 on LH; 12/12 study-like data sets, factor >= p^0.87) and concludes the unimodal-ratio route cannot certify the target; both can be right (a failed sufficient condition vs a CONJECTURE of fast mixing) | NONE; D1 flagged "needs an independent check" [THM-INV §2, §6]; THM-SYNTH REPORT §4.1 settles the wording: say both; final FUTURE_WORK FW4 (N10 OPEN; "the YWJ/ZYVR route is blocked as stated") | THM-INV/REPORT.md §2 (D1), §5 item 7; THM-SYNTH/REPORT.md §4; MEET-THM/FUTURE_WORK.md (FW4, FW5) | [pos 1009] [pos 1107] [pos 1177] | FUTURE_WORK FW4, FW5 (K23, K24) |
| CJ302 | THM-INV remaining gaps 2, 5, 6, 8-12; two-sided masked Zhat; production masked consistency beyond LH; finite-n; flag power; calibration; partition law; floating point; V5 exactness | open problem | 2 two-sided relative accuracy of Zhat in the masked regime (only the lower-tail mechanism PROVED); 5 masked-regime selection consistency of the production method on non-LH or random designs including the study generator (groups of 5, p >> n); 6 finite-n guarantees (upper bound on Pi(X) OPEN, finite-n Gibbs discovery OPEN); 8 positive power of flags (all theory negative: V12, E1c); 9 calibration behaviour (rebuild-loop convergence, P(S0 in V), T_n in the masked regime, Conjecture P OPEN); 10 partition law for the adaptive packing; 11 floating-point accuracy at production size (VAL-FP measured at p <= 40 only); 12 exactness of the composite start sampler and reversibility/self-adjointness of the move round (V5), "routine, but a paper claim needs a written proof or a citation" | NONE for each [THM-INV §5]; item 12 closed by N9-KERNEL (TH405-TH410, LM229); finals: FW24, FW10, FW25, FW14, FW26, FW17, FW6, FW16 | THM-INV/REPORT.md §5; MEET-THM/FUTURE_WORK.md | [pos 1103] [pos 1107] [pos 1153] | FUTURE_WORK FW6, FW10, FW14, FW16, FW17, FW24, FW25, FW26; S-KERNEL (item 12) |
| CJ303 | F-REFEREE M1 (JRSS-B referee simulation, major point) | hypothesis | All theory is asymptotic, thresholds at n of about 2e6, simulations at n = 200 [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: open (R2 LH-SCALE, R9 first-n table not started); S-ELS decomposition and O-LS0 data exist [registry H] | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | S-LIM (limitations as theorems) and the n = 200 disclosure; FUTURE_WORK FW2, FW13, FW14 |
| CJ304 | F-REFEREE M2 (JRSS-B referee simulation, major point) | hypothesis | The main theorem requires a method tweak (LS0) that the reported simulations did not run [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: answerable: LS0 is part of the method and outcome-neutral on the study (O-LS0: 0/2,394); A-REV7 VERIFIED a no-LS0 masked theorem (B2-LH under STAB-LH, Astra-authored analytic STAB certificate on an explicit growing-p LH subfamily) and D2-LH (c = 1, qualitative); the headline choice is HQ's [registry H] | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | M5 Theorem HPM (LS0 in the shipped core, K72, K69, K65, K68) |
| CJ305 | F-REFEREE M3 (JRSS-B referee simulation, major point) | hypothesis | The masked regime without LS0 rests on unproved particle-level hypotheses (DELIV, REP), and the n = 200 mechanism has no theorem [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: answered on LH: (b1 prime) by D2-LH, (b2) by B2-LH (A-REV7 VERIFIED); F2 GAP; general DELIV OPEN [registry H] | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | M5 Theorem HPM ((b2-LH) on the STAB-LH subfamily); FUTURE_WORK FW10, FW26 |
| CJ306 | F-REFEREE M4 (JRSS-B referee simulation, major point) | hypothesis | The favourable regime is where the sampler is unnecessary; what does the bridge provably buy (separation; masked Zhat/PIP statements) [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: in progress, with a twist: W7-SEP supports "moving off the start is needed", not "tempering is needed" (E-SPINE); F-MASKPIP M1-M3 [registry H] | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | M6 Theorem SEP + Lemma KL; M4 Theorem Z_T; M1 Theorem V/H (Theorem H) |
| CJ307 | F-REFEREE M5 (JRSS-B referee simulation, major point) | hypothesis | The 2^B factor, vacuous start rates, and Theorem 6 budgets / circular premise (P1) on the realised T_n [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: in progress: W5-FAVIID Theorem A/B 2^B-free (REPORT now complete, author only); O-STAGES Theorem M [registry H] | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | M3 Theorem START; M7 Theorem STG; FUTURE_WORK FW6, FW23 |
| CJ308 | F-REFEREE M6 (JRSS-B referee simulation, major point) | hypothesis | What is genuinely new, and the missing comparison with the rapid-mixing results for BVS (YWJ 2016, ZYVR 2022) [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: open (W8-SYNTH task 10) [registry H, written before API-POS landed]; answered afterwards by API-POS (TH404) and LIT-MCMC (TH401); referee suspicion "correct in substance" (API-POS headline 2) | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | positioning paragraph next to M5 (THEOREM_LIST_FINAL, LIT-MCMC #1-2); FUTURE_WORK FW4 |
| CJ309 | F-REFEREE M7 (JRSS-B referee simulation, major point) | hypothesis | The evidence and PIPs mean nothing in the masked regime, and the 95% bound is Markov [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: in progress: F-MASKPIP, O-PW2, O-CERT/O-VCERT [registry H] | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | M4 Theorem Z_T and certificate card; S-Z (K37-K41, K53); M1 Theorem V/H |
| CJ310 | F-REFEREE M8 (JRSS-B referee simulation, major point) | hypothesis | Verification status, the cost corollary T32(i), and implementation facts (SR, GUARD) as hypotheses [REFEREE_REPORT §1]; referee recommendation: "major revision"; the one change that most raises the tier: make Theorem 5(b) a theorem about the algorithm that produced the tables, on LH, with the production code at growing n | referee objection; state at T38-RECORD cut: largely answered: A-REV5-A-REV9 cross-family reviewed the W6 repairs, the LS0 route (A-REV8), the no-LS0 route (A-REV7) and the new results; GUARD read by A-REV5/A-REV8 (statistical scope); T32(i) still SF only (A-REV6 "supported", A-REV9 deferred) [registry H] | F-REFEREE/REFEREE_REPORT.md §0, §1; F-REFEREE/RESPONSE_PLAN.md; T38-RECORD/REGISTRY_v2.md §H | [pos 726] [pos 748] [pos 763] [pos 796] [pos 906] | S-CERT; S-OUT (Lemma RO, GUARD-W); M8 Proposition D (T32(i)) |
| CJ311 | F-REFINE CARDS/ARCHITECTURE; best believed versions of the eight paper targets; 8-target architecture; confidence cards (written before A-REV1/A-REV2) | hypothesis | Eight believed versions with P(true)/P(provable): Thm 1 T03 sharp 0.95/done; Prop 1 T07 0.98/done; Thm 2 T22+T27 0.95 (exact Gram) / 0.85 (LH-iid) / done, review; Thm 3 repair (A 0.97, W 0.85, B prime 0.95); Thm 4 T21 0.97/done; Thm 5 T38 0.9 (b1) / 0.5 (b2 instance) / review, 0.3; Thm 6 T26 0.95/done; Prop 2 T12 0.97/done; only method-change dependency LS0 for (b1); nothing proved describes the n = 200 numbers; dependency graph, joint families (ORTH, LH, LH-iid), journal cuts (JRSS-B 8, Biometrika 5), overstatement watch (15 items), n = 200 disclosure, open items ranked | F-REFINE's own words: "campaign PROVED, same-family VERIFIED" only; T38-RECORD C14 conflict: the legend [P] over-states cross-family review; amended 2026-11-02 by E-SPINE (wording only: "moving off the start", LS0 effective, S-ELS counts); several believed statements later retired (RF279, RF280) -- see Dead ends | F-REFINE/CARDS.md; F-REFINE/ARCHITECTURE.md; F-REFINE/NEXT_TASKS.md; T38-RECORD/REGISTRY_v2.md (C14, D) | [pos 474] [pos 463] [pos 953] [pos 957] | JRSS-B eight-result cut (Thm 1-6, Prop 1-2); superseded by MEET-THM THEOREM_LIST_FINAL M1-M8 |
| CJ312 | T12 hstep; T12(i.a) probabilistic step; T12_PLAN | open problem | Derive the recursion hstep and stage-0 identity h0 from a probabilistic island model (PMF on populations, multinomial resampling, product law); est. 300-600 lines | OPEN (plan only) | L-LEAN/T12_PLAN.md; L-LEAN/REPORT.md | [pos 717] [pos 796] [pos 953] | M1 Theorem V/H (K35, K36); L-T12 |
| CJ313 | T12 round-kernel invariance; Prop 2 (b)(d)(e) in Lean | open problem | Invariance of the actual round kernel (composition and mixture of invariant kernels), instantiation gamma_t = gamma_0 exp(phi_t d), RB-PIP and pooled-evidence parts of Prop 2 | OPEN | L-LEAN/T12_PLAN.md (step 5) | [pos 796] | M1 Theorem V/H (K46, K35, K36); L-T12 |
| CJ314 | T21 routes (a)-(f); H03 asymptotics; not formalised | open problem | Routes (a)-(f) bounding P(U^c, S0 not scored) and the H03 limit E0 delta1 -> 0 are not in Lean (only the finite step LM232) | OPEN | L-LEAN/ASSUMPTIONS.md (A-T21-5); L-LEAN/REPORT.md | [pos 796] | M5 Theorem HPM (K72); S-OUT |
| CJ315 | T11(iii) regular conditional probability given calibration output | open problem | Conditional-on-C version of T11(iii) (pointwise reading only in Lean) | OPEN | L-LEAN/ASSUMPTIONS.md (A-T11-1); L-LEAN/REPORT.md | [pos 796] | none (campaign-only) |
| CJ316 | T37 A4 remaining clauses; not formalised | open problem | Necessity clause 'every greedy path from R_{a,d} decreases Phi at each step and ends at S0 implies TD'_P(R_{a,d})' and other A4 clauses beyond PD and A1 converse | OPEN | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean (header); L-LEAN/REPORT.md | [pos 796] | M5 Theorem HPM (K65) |
| CJ317 | T37 A5 relation to literal TD; not formalised | open problem | A5: literal TD(d,0) strict implies TD'_P(R_d); TD'_P implies TD'_inf, converse fails | OPEN | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean (header); L-LEAN/REPORT.md | [pos 796] | none (campaign-only) |
| CJ318 | T37 Theorem B (finite-n bound) and Theorem C (asymptotics); not formalised | open problem | Probabilistic parts of W1-T37R Theorems B and C; only the deterministic A3 lattice step (TH454) is in Lean | OPEN | L-LEAN/REPORT.md; L-LEAN/STATUS.md; W1-T37R/PROOF.md | [pos 796] | none (campaign-only) |
| CJ319 | SMC-BVS score formula and regression structure; not formalised | open problem | F and m are arbitrary reals in all Lean results; no Gaussian-regression posterior theorem is formalised | OPEN | L-LEAN/REPORT.md (section 3); L-LEAN/ASSUMPTIONS.md | [pos 796] | none |
| CJ320 | Lemma 0(b) and E_LS repair; not formalised | open problem | Lean covers Lemma 0 (a),(c) only; Lemma 0(b) (informal ERROR per A-REV2) and its three-way-partition repair are not in Lean | OPEN | L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean; T38-RECORD/REGISTRY_v2.md (Lemma0(b), C12) | n/a | M5 Theorem HPM (K65 area) |
| CJ321 | explicit first-hit clause for standalone A3 statements | open problem | Make the existential witness tau of theoremA3 / theoremA3_lattice_tau an explicit first-hit time | OPEN (optional; Astra r2 minor remark) | L-LEAN/fidelity/ASTRA_round2.md | n/a | M5 Theorem HPM (K65) |
| CJ322 | capped-scan certification interface; T38-(0) as finite Boolean lemma | open problem | To add: capped-scan certification interface (l >= tau(C), completed scan => certified return) and (0) as a finite Boolean lemma with the output event | OPEN (proposal of the theorem meeting) | MEET-THM/THEOREM_LIST_FINAL.md (M5 Lean core) | [pos 1353] [pos 1361] | M5 Theorem HPM (K65, K72) |
| CJ323 | production semantics of the greedy search; implementation verification | open problem | Engine v3_core.cpp local_search, lexicographic tie rule as a rank, local_limit flag and feasibility inside Rad are not formalised | OPEN | L-LEAN/ASSUMPTIONS.md (A-T37-2); L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | n/a | none (campaign-only) |
| CJ324 | standalone cardinality theorem /Lat(S)/ = 2^Phi(S) | open problem | No exported theorem states /Lat S/ = 2^(Phi S) | OPEN (optional; Astra r2 minor remark) | L-LEAN/fidelity/ASTRA_round2.md | n/a | M5 Theorem HPM (K65) |
| CJ325 | Lean certificates for the remaining paper-1 cards | open problem | No .lean file exists for V2, V3, V4, A1-A4, D1-D4, S1, S2, C1, R1, R5; Lean cores in THEOREM_LIST_FINAL are proposals | OPEN | MEET-THM/evidence/CHK_INHERITED/scripts/sources/registry.md (section 3.4); MEET-THM/THEOREM_LIST_FINAL.md; MEET-THM/REGISTRY_PAPER1.md (line 31) | [pos 1015] [pos 1018] [pos 1492] | all cards with a Lean core row |
| CJ326 | output-event, GUARD and SR conventions inside the Lean composition | open problem | Lean t21_C1 takes U arbitrary; the convention that U contains every stopped fit and abort (G1, G3) is not stated in Lean | OPEN (gap recorded; no source proposes a statement) | T38-RECORD/REGISTRY_v2.md (rows Thm4-C1, T38-(0)) | n/a | M5 Theorem HPM (K72); S-OUT |
| CJ327 | independent rebuild and full axiom audit of the 101 theorems | open problem | W8-SYNTH did not rebuild; #print axioms covers 56 of 101 theorems; no recorded rebuild by anyone other than the L-LEAN lead | OPEN (gap recorded; UNCERTAIN whether anyone intends it) | W8-SYNTH/REPORT.md; W8-SYNTH/SYNTHESIS.md (section 7); L-LEAN/REPORT.md | [pos 796] | none |

## Refuted or retired claims

| ID | native name(s) | kind | description | final status | authoritative file | positions | feeds |
|---|---|---|---|---|---|---|---|
| RF101 | literal T37; T37(i); TD(d,m) literal; truth dominance; Prop1-TD (retires literal T37); V1-TDfails; CEX1 | refuted claim | Literal T37(i): under TD(d, 0) with strict inequalities the production local search walks monotonically from any centre in R_d to S0 in exactly /S symmetric-difference S0/ moves; TD(d,m) itself is self-contradictory for d >= 1 | REFUTED: TH198 (Prop1-TD) PROVED, SF VERIFIED (W3-VT37R), XF VERIFIED (A-REV2); d = 0 counterexample RF101 (CEX1) VERIFIED (W3-VT37R, reproduced by A-REV2) | main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T37_truth_dominance_greedy_repair.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md; main@c4ef0dc/Docs/THEORY_PRIORITIES.md; T38-RECORD/REGISTRY_v2.md | [pos 150]; [pos 156]; [pos 178]; [pos 355]; [pos 370] | none (refuted / dropped claim) |
| RF102 | H24; H24 as written; uniform exit; (L+4) eta_n -> 0 | refuted claim | H24: uniform in R_d, K1(x,{S0}) >= a_n and one-round first-exit probability <= eta_n, with a_n >= c_n/2 and (L+4) eta_n -> 0; the vanishing-exit input is false in correlated designs | REFUTED as a general asymptotic input (CE144 (CE1) COUNTEREXAMPLE, SF VERIFIED* W2-VT24G, XF VERIFIED* A-REV1; broad asymptotic wording GAP, narrow explicit sequence VERIFIED A-REV5) | main@c4ef0dc/Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md; main@c4ef0dc/Docs/Theory/theorems/T24_T18p_terminal_repair.md; T38-RECORD/REGISTRY_v2.md | [pos 327]; [pos 342]; [pos 370]; [pos 557] | none (refuted / dropped claim) |
| RF103 | T02 sharp size cutoff; m_n = s0 + O(s0 log n/log p); T02(i) tail sharpening; geometric tail 2^-m replaced by exact BB(1,p) tail; Prop. D target | refuted claim | Replacing T02(i)'s geometric tail 2^-m by the exact BB(1,p) tail would cut the cutoff m_n from about 200 to s0 + O(s0 log n / log p) under G and R; false without SE (duplicated columns) | REFUTED under G and R alone: CE111 (PropD-T03) COUNTEREXAMPLE, SF VERIFIED (W2-VT03R row 11), XF VERIFIED (A-REV2); TH126 (E3-T03) barrier VERIFIED* | main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FROZEN_LIST.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md; main@c4ef0dc/Docs/THEORY.md; T38-RECORD/REGISTRY_v2.md | [pos 342]; [pos 355]; [pos 370] | none (refuted / dropped claim) |
| RF104 | tempering is needed; the sampler is needed; the bridge is needed; start-only methods fail; motivation for the SMC machinery | refuted claim | Claim that start-only discovery fails in the masked regime so the tempering bridge / sampler is needed; false on the paper's own masked family LH: one greedy search from the start mode suffices (Prop. GU) | REFUTED on LH by proof (TH388 (SEP-GU) Cor. GU-LH: COUNTEREXAMPLE to the task's claim (a); numerically 386/386 replicates); SF: none (A-REV7 pending then), XF: TH388 (SEP-GU) VERIFIED* (A-REV7), GAP in A-REV9 review | main@c4ef0dc/Docs/THEORY_PRIORITIES.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T38_two_regime_HPM_consistency.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md; E-SPINE/Docs/Theory/AMENDMENTS_20261102.md; W7-SEP/REPORT.md; T38-RECORD/REGISTRY_v2.md | [pos 717]; [pos 796]; [pos 800]; [pos 805]; [pos 807]; [pos 850] | none (refuted / dropped claim) |
| RF105 | beta-min about 100x; n=200 disclosure numbers; 55 vs 0.64 and 0.16 | refuted claim | Pre-campaign disclosure figure: the explicit BM-C constant fails by about 100x in squared signal at n = 200; corrected to at least 43x once T03-sharp replaced M* | CORRECTED (number retired; not a theorem). Treat as a disclosure fact: beta-min fails by at least 43x (E-SPINE 2.3) | main@c4ef0dc/Docs/THEORY_PRIORITIES.md; main@c4ef0dc/Docs/THEORY.md; E-SPINE/Docs/Theory/AMENDMENTS_20261102.md | [pos 370]; [pos 850] | none (refuted / dropped claim) |
| RF106 | T15(i') SE-only; DROPPED.md (LF) | refuted claim | SE alone does not make every best local-search move a true move: a signal-bearing proxy can win the first improvement and the search certifies a wrong local maximum | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF107 | T14-H one-move-addition iid-cheap clause for all polynomial p; DROPPED.md (LF) | refuted claim | iid discovery is cheap for all polynomial p: factor-n error | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF108 | T21(iv) 'MISS with eta_n -> 0 fails'; DROPPED.md (LF) | refuted claim | wrong object: it is D_n eta_n -> 0 that fails; the '~20 entries' number withdrawn | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF109 | T22(iv) existence claim for usable upper bounds; DROPPED.md (LF) | refuted claim | existence of usable upper bounds U >= Z is false as stated | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF110 | T11(ii) 'no ordering constant for a = 1'; DROPPED.md (LF) | refuted claim | claim that no ordering constant exists for a = 1 is false | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF111 | T5(iii) additive band as the main statement; DROPPED.md (LF) | refuted claim | an additive band for the orthogonal threshold is false for slowly growing p | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF112 | 'TWO' / valley-protected two-move set as the negative regime; DROPPED.md (LF) | refuted claim | the two-move valley set is neither necessary nor sufficient for the negative regime | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF113 | Universal memory ceiling p_max = Theta(sqrt M0) (T23-S); DROPPED.md (LF) | refuted claim | memory ceiling on p independent of the branch: false because the exact branch precedes Gram construction | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF114 | Discrepancy range bound (n+K) log(n+1), the '1e17' cutoff, and gap-only STIFF (T23-R); DROPPED.md (LF) | refuted claim | discrepancy range bound and gap-only STIFF obstruction: duplicated predictors across blocks accumulate gains | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF115 | Selected-model fixed-atom certificate exp(-Q_f pi0(S-hat)); fixed final E2; 'checks pass' from coupling alone; DROPPED.md (LF) | refuted claim | competitor certificates from selected models: selection and information restrictions missing | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF116 | Blanket working-set / full-space vacuity claims (T12, L-RC); DROPPED.md (LF) | refuted claim | d = 0 is a benign full-space case; a large union bound proves no impossibility | DROPPED (LF) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114]; [pos 178] | none (refuted / dropped claim) |
| RF117 | DROPPED.md judge UR/UA items; T18' slot constants 1/(s0! d!); EXIT_d as internal-change control; RET+OCC; phi*_n; NUM coverage | refuted claim | Group of routes dropped by the judge as unworkable (UR) or resting on unverifiable assumptions (UA); the first (slot constants and EXIT_d) is killed by the internal-non-Gibbs-moves example J4 (CE102) | DROPPED (UR / UA) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114] | none (refuted / dropped claim) |
| RF118 | DROPPED.md council and review group; T19 Tier A; Tier B' uniform coupling; over-tempered route | refuted claim | T19 Tier A (uniform coupling at the pair) is refuted on every dataset by the addition floor (zeta >= h_{s0}) and COVER-pair's eps_C >= n^(-1/2); Tier B' is vacuous; T17(iii)(a) over-tempered route needed concentration beyond 1 + delta | DROPPED (TR / UA / UR) | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114] | none (refuted / dropped claim) |
| RF119 | FAILED_ATTEMPTS.md; BFDR; expected-F1; GFM; block-MAP; Matryoshka; pMOM; BB(1,p)+HPM Phase 2 | refuted claim | Empirical record (not theorems) of selection rules that failed to beat the HPM under BB(1,p) in S1-S5 / Phase 2: do not retry as is | FAILED (empirical record; 'do not retry as is') | main@c4ef0dc/Docs/History/selection_campaign_2026-10-13/FAILED_ATTEMPTS.md; main@c4ef0dc/Docs/Theory/FAILED_ATTEMPTS.md | pre-campaign; [pos 114] | none (refuted / dropped claim) |
| RF120 | MASS; zeta-EXIT; AGG-stat; NL_eta0; VIS follows from G R SE BM; HIT; S-tilde0 scanned as a centre | refuted claim | Hypotheses/claims of the inventory retired by the review group; 'S-tilde0 scanned as a centre' is the pre-campaign form of what LS0 later made a method feature | DROPPED (UA / LF) | main@c4ef0dc/Docs/Theory/DROPPED.md; main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md | pre-campaign; [pos 114] | none (refuted / dropped claim) |
| RF121 | Brief/FROZEN_LIST target: the exact BB(1,p) tail cuts m_n to s0 + O(s0 log n / log p) so SE is meaningful at n=200 | refuted claim | FROZEN_LIST/FABLE_REVIEW/THEORY_PRIORITIES Thm 1 restatement: replacing 2^-m by the exact BB(1,p) tail cuts m_n from about 200 to s0+O(s0 log n/log p), making SE on sets of size <= m_n+s0 <= K meaningful at n=200. False: exact tail saves only 4 s0! e^(gamma_m) (about 36 sizes at s0=14); Prop E3 barrier; Prop D shows it false under G and R alone. | REFUTED (COUNTEREXAMPLE CE111 + PROVED LM101/TH126; SF VERIFIED W2-VT03R; XF VERIFIED A-REV2); scope: false for the SE-free size-tail route, outright under G and R alone (W2-VT03R R2) | W1-T03R/REPORT.md; W1-T03R/PROOF.md; W2-VT03R/REPORT.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FROZEN_LIST.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md | [pos 296]; [pos 342]; [pos 370] | replaced by TH125 (T02(i-sharp)) + TH126 (E3); cap K binds at n=200 (m# = K = 100); feeds S-T scope |
| RF122 | FROZEN_LIST/FABLE_REVIEW premise: BB(1,p) ratio is about k/2p, not 1/2 | refuted claim | The per-model ratio w(k+1)/w(k)=(k+1)/(2p-1-k) is about k/(2p) but the class (size-marginal) ratio is 1/2 because it is cancelled by the multiplicity C(p,k+1)/C(p,k); the premise that this shrinks the size tail is false. | REFUTED by LM101(a) (PROVED; SF VERIFIED W2-VT03R; XF VERIFIED A-REV2) | W1-T03R/REPORT.md; W1-T03R/PROOF.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md | [pos 296]; [pos 342] | replaced by LM101 (Lemma E1) |
| RF123 | W1-T03R disclosure: the proof deterministic thresholds start near n = 1.2e5; other thresholds bind earlier | refuted claim | W1-T03R REPORT headline 4/section 3/section 5: the proof's own deterministic thresholds start near n ~ 1.2*10^5 and other thresholds bind earlier. False: q_n <= 1/2 first holds at n about 2.1e6 (p=n^1.17) and 2.5e6 (p=n^1.30). | ERROR (SF: W2-VT03R verdict row 29); ERROR confirmed XF (A-REV2 section 3.5: q=5.5e22 and 7.9e28 at n=130,328); registry T03-1.2e5 [APPLIED] | W2-VT03R/REPORT.md; A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md; T38-RECORD/REGISTRY_v2.md | [pos 296]; [pos 370]; [pos 570] | replaced by the corrected disclosure (onset n >~ 2e6) in S-T (K93) |
| RF124 | Replacement onset gloss: the proof deterministic thresholds as written hold from n about 2e6 (W2-VT03R R1 / W6-FIXREV2 replacement sentence) | refuted claim | Replacement sentence: ...and the proof's own deterministic thresholds (as written) hold only from n about 2*10^6 (p=n^1.17) to 2.5*10^6 (p=n^1.30); the O_P constants are unspecified. Too broad: at n=2,116,048, q=0.4999999 but exp(2 eps_n)=4639.9 > 4. | ERROR (XF: A-REV5 section 3 "T03 replacement disclosure"); numerical correction VERIFIED; no replacement sentence written in the thread (final card: no universal onset n0) | A-REV5/REVIEW.md; W6-FIXREV2/STATEMENTS.md; W2-VT03R/REPORT.md | [pos 570]; [pos 807] | replaced by: geometric-series threshold crosses at 2,116,048 / 2,457,025, fixed-constant threshold at 25,571,897 / 29,755,302; neither a universal onset (C9 repairs: no universal n0) |
| RF125 | W2-BOOK Prop 1 data paragraph: every completed wrong HPM is a posterior miss (F(S0) <= F(HPM)); ERROR B5; Prop1-wrongHPM | refuted claim | "Every completed wrong HPM is a posterior miss (F(S0) <= F(HPM))." A finite scored set omitting S0 can return a lower-scoring wrong HPM although S0 is the unique global maximum; only a strict same-size posterior miss established by audit scores certifies the ceiling. | ERROR B5 (XF: A-REV4 BOOK_CHECK); A-REV6: original implication remains ERROR, replacement certificate (exactly scored strict competitor) verified; repair PENDING in registry (relabel as the empirical audit observation, ELS-4) | A-REV4/BOOK_CHECK.md; A-REV6/BOOK.md; W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; T38-RECORD/REGISTRY_v2.md | [pos 677]; [pos 807]; [pos 1238] | replaced by TH131 (iii-prime)/(iv) strict certificate; L-DEC flag Prop1-wrongHPM |
| RF126 | W5-LOCKBOOK Prop 1(iii) paraphrase: any same-size m(S) >= m(S0) is an unrepairable error | refuted claim | W5 paraphrase: a within-size ranking error (S != S0, /S/ = s0, m(S) >= m(S0)) is exactly the error that no re-tuning of the size prior can repair. Wrong at an equal likelihood where S0 wins the tie order. | ERROR in that paraphrase (XF: A-REV6 BOOK.md); tie-aware R3 repair (Astra candidate): strictly larger likelihood, or equal likelihood and a competitor preceding S0 in the tie order | A-REV6/BOOK.md; W5-LOCKBOOK/STATEMENTS.tex; W2-BOOK/REPORT.md | [pos 807] | replaced by the tie-aware criterion S*_{s0}=S0 (TH131 (i-prime)) |
| RF127 | T05 wording: the g-prior + BB(1,p) HPM loses a sqrt(log n) factor to the oracle | refuted claim | FROZEN_LIST/FABLE_REVIEW/T05 one-pager: the g-prior + BB(1,p) HPM loses a sqrt(log n) factor to the oracle under orthogonal design. False as a multiplicative statement at p=n^a, a>0; true additively on the amplitude scale. | COUNTEREXAMPLE (W7-SEC, author-only check; registry T05-wording); XF none (A-REV9 deferred) | W7-SEC/REPORT.md; W7-SEC/PROOF_T05.md; main@c4ef0dc/Docs/Theory/one_pagers/T05.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FROZEN_LIST.md | [pos 119]; [pos 717]; [pos 751] | replaced by TH135 (T05-G) additive-amplitude wording; feeds: none found |
| RF128 | W1-T03R wording: SE restricted to the comparison unions actually used (not all subsets); anchoring as the main relaxation | refuted claim | SE restricted to the comparison unions actually used (not all subsets). Imprecise: by Lemma A1 anchored SE is equivalent to the same bound on every column set T with at most j0 (resp. m#) columns outside S0; the real relaxations are the size cutoff m# and the unnormalised constant g0. | Imprecise wording, not a mathematical error (SF: W2-VT03R row 30); wording R2 applied in W6-FIXREV2 (anchoring is not a restriction to a hand-picked list) | W2-VT03R/REPORT.md; W6-FIXREV2/STATEMENTS.md; A-REV2/REVIEW.md | [pos 370]; [pos 570] | replaced by LM105 (Lemma A1) wording in TH128 |
| RF129 | THEORY_PRIORITIES n=200 disclosure: beta-min fails by about 100x in squared signal | refuted claim | beta-min fails by about 100x in squared signal (THEORY_PRIORITIES, brief of W1-T03R). Corrected: the proof sufficient constant requires theta*^2 >= 27.5/phi0^2 (p=500) and 30.6/phi0^2 (p=1000) against executed 0.64 (c=1) and 0.16 (c=0.5): shortfall at least 43x / 48x with phi0^2=1. | Superseded numerical claim (SYNTHESIS: about 100x predates T03-sharp); corrected numbers VERIFIED (W2-VT03R row 28) | W1-T03R/REPORT.md; W2-VT03R/REPORT.md; W8-SYNTH/SYNTHESIS.md; main@c4ef0dc/Docs/Theory/../THEORY_PRIORITIES.md | [pos 796] | replaced by 43x/48x in the n=200 disclosure |
| RF130 | Claim that T03-sharp(iii) P(S_dagger != S0) <= 2E0[1-pi(S0)] is a new contribution | refuted claim | LIT-STAT: this inequality is Rossell (2022, Bayesian Analysis) Proposition 1 verbatim (also for the MPM); T21 and Thm 5(0) inherit the term; it must be credited to Rossell. | Literature verdict KNOWN (LIT-STAT, single reader; Rossell read via arXiv:1806.04071); HQ acted on it [pos 1142] | LIT-STAT/REPORT.md | [pos 1009]; [pos 1142] | replaced by citation wording in S-T / M5 (T03-sharp via Rossell 2022, Prop 1) |
| RF131 | LIT-STAT first-draft line: every BB(1,p) ratio factor rho_i is <= 1/2 for i >= 0 | refuted claim | First draft of LIT-STAT section 12 said the BB(1,p)/BB(1,1) size factor ratio is <= 1/2 for every i >= 0; false at i=0 where rho_0 = p/(2p-1) = (1/2)(2p/(2p-1)). | Corrected in LIT-STAT section 12 (author only) | LIT-STAT/REPORT.md | [pos 1009] | replaced by LM108 |
| RF132 | LIT-STAT headline 4 before section 12: BB(1,p) penalises added variables differently from BB(1,1), so the BB(1,p) tail is a new mechanism | refuted claim | Per model, BB(1,p) and BB(1,1) penalise each added variable at the same order ((k+1)/(2p-1-k) vs (k+1)/(p-k)); BB(1,p) = BB(1,1) tilted by a Geometric(1/2) size law; the novelty of T02(i-sharp) is modest, not a new mechanism. | Self-correction by LIT-STAT (section 12 Correction after a later check); author only | LIT-STAT/REPORT.md | [pos 1009] | replaced by LM108; T03-sharp rated modest extension of Rossell 2022 |
| RF133 | LOCKED_PROOFS/THEORY_PRIORITIES wording of T06(i): two models tie exactly iff their projection matrices (X_S X_S-prime) agree | refuted claim | Register one-liner for T06 and THEORY_PRIORITIES say that models tie iff their projections agree. The locked condition is equality of the outer products X_S X_S^T; equal spans with different outer products give different score functions (T06(i)(b)). The paper must say outer products. | WORDING ERROR corrected: W2-BOOK PROOF section 3 Caution on wording; SF: W5-LOCKBOOK CORRECT (the register one-liner is the wording to fix); XF: not itemised (A-REV4 BOOK_CHECK verifies the sharp construction only) | W2-BOOK/PROOF.md; W2-BOOK/REPORT.md; W5-LOCKBOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; main@c4ef0dc/Docs/Theory/proofs/T06_T07_identifiability_size_prior/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md | [pos 358]; [pos 424]; [pos 550] | replaced by TH131 clause (v) (equal outer products, not merely equal spans) |
| RF134 | EXP-const; kappa_EXP -> 0.52/c_*; 4.16(M+2 sigma^2)/sigma^2; Lemma U limit constant | refuted claim | Displayed limit kappa_EXP -> 0.52/c_* = 4.16(M+2 sigma^2)/sigma^2; actual limit is 0.51/c_* = 4.08(M+2 sigma^2)/sigma^2 (0.52/c_*+o(1) valid only as a looser eventual bound); replaced by kappa_n decreasing to 0.51/c_E (W6-FIXREV1) | ERROR (A-REV1, A-REV2 5.1); SF W3-VEXP VERIFIED (missed it); repair PROVED (W6-FIXREV1/2, A-REV5 VERIFIED); registry conflict C6 | A-REV2/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md; W6-FIXREV2/REPORT.md; A-REV5/REVIEW.md | [pos 568] [pos 570] [pos 807] [pos 919] | feeds: none (no downstream effect; EXP′ TH136 feeds M3 K16) |
| RF135 | Thm4-iff; Thm 4 'iff' gloss; masking persists iff eta < 1/2.02; p^-c alone forces vanishing mass | refuted claim | 'masking persists iff eta < 1/2.02, a sufficient condition' (self-contradictory) and VEXP's 'p^-c alone forces pi_0(S0)->0 whatever eta'; only sufficiency holds | ERROR (A-REV2 5.3; W3-VEXP R4 partial); registry conflict C7 | W1-EXP/PROOF.md; W3-VEXP/REPAIRS.md; A-REV2/REVIEW.md | [pos 363] [pos 568] [pos 570] | feeds: none |
| RF136 | WeakSignal; weak-signal masking conjecture; W1-EXP escalation 3 | refuted claim | W1's guess that the n=200 start masking is weak-signal masking, CL(L) with bounded L on weak truths, with pi(S0) also small; replaced by dilution | ERROR (W3-VEXP row 27 'evidence against'; W3-PXN Prop W); retired in favour of dilution | W1-EXP/REPORT.md; W3-VEXP/REPAIRS.md; W3-PXN/REPORT.md | [pos 363] [pos 370] | feeds: none (retired) |
| RF137 | W1 headline 6; EXP′ applies at the study size via kappa_EXP | refuted claim | 'SE-blk holds at the study size ... so EXP′ (Thm 1) applies there' while kappa_EXP is ~100-1700 nats at study SNR (vacuous); replaced by R1 certificate | GAP -> repaired (W3-VEXP row 26, R1/R4) | W1-EXP/REPORT.md; W3-VEXP/REPAIRS.md | [pos 363] [pos 370] | feeds: none |
| RF138 | PXN-LemmaU-U1; nu log(1+a/RSS^y) <= 1; Lemma U (U1) arithmetic | refuted claim | nu log(1 + a_A/RSS^y_A) <= nu(1.02+1/(n phi0^2))/(c_* n) <= 1 is false (about 0.51/c_* >= 8; 20.4 for sigma^2=1, M=3) | ERROR (W5-VMASK R2; A-REV3); repaired R2 (VERIFIED A-REV6, A-REV8) | W5-VMASK/REPAIRS.md; A-REV3/REVIEW.md | [pos 742] [pos 796] [pos 919] | feeds: none |
| RF139 | W1 sec 1.5; kappa_17 >= 0.15 for all six study covariances | refuted claim | 'All six study covariances have kappa_17 >= 0.15'; false for S6 (rho=0.9 groups give 0.1) | ERROR (W3-VEXP R4; A-REV2 5.4); correct bound kappa_17 >= 0.1 | W1-EXP/PROOF.md; W3-VEXP/REPAIRS.md; A-REV2/REVIEW.md | [pos 363] [pos 568] | feeds: none |
| RF140 | PART-L3 literal; W7 Lemma 3 conditioning on both normalised vector collections | refuted claim | Conditionally on (U_h, U_h′) the cross correlations are (<u_j,v>)_j with v uniform: false since conditioning fixes the cross inner products; correct version conditions on within-group Gram matrices | ERROR (A-REV6); Theorem C GAP as written | W7-PART/PROOF.md; A-REV6/PARTITION.md; A-REV6/REVIEW.md | [pos 796] [pos 919] | feeds: none |
| RF141 | W7 CE2 header; 2 g_min <= B => blocks != groups surely (unequal sizes) | refuted claim | '2 g_min <= B, G >= 2 => next-fit puts >= 2 whole groups in every bin => blocks != groups surely' fails for unequal group sizes (2 and 5, B=5) | ERROR (A-REV6); equal-size study example survives (CE118) | W7-PART/PROOF.md; A-REV6/PARTITION.md | [pos 796] [pos 919] | feeds: S-BLOCKS cites PART-CE2 (XF ADVERSE on header only) |
| RF142 | W1 'under weak-signal masking pi(S0) is also small' | refuted claim | W1-EXP's claim that in the weak-signal mechanism pi(S0) is also small unlike LH | not supported (W3-PXN sec 8: 96-100% of start-masked truths have LO_1>0); W3-VEXP did not compute pi at p=500 | W1-EXP/REPORT.md; W3-PXN/REPORT.md; W3-VEXP/REPAIRS.md | [pos 363] [pos 423] | feeds: none |
| RF143 | PXN NB constant 1.925; T_e log 1.925 | refuted claim | NB threshold T_e log 1.925 does not guarantee ESS >= 0.9H (W3-VT38E); replace by r* = (11+2 sqrt(10))/9 | GAP (cosmetic, W5-VMASK R3); repaired (VERIFIED A-REV8) | W3-PXN/PROOF.md; W5-VMASK/REPAIRS.md | [pos 742] [pos 919] | feeds: none |
| RF144 | LH-LAT-sharp; W4-T38FULL LH-LAT 'm0 is sharp' | refuted claim | Prop LH-LAT states m0 is sharp; true only for homogeneous pairs (108/108), not 32/94 heterogeneous settings (down to x0.002) | GAP (overstatement, W5-VMASK R5); conflict C26; A-REV8: valid not sharp | W5-VMASK/REPAIRS.md; A-REV8/REVIEW.md | [pos 742] [pos 919] | feeds: none |
| RF145 | PXN-Lfail-numbers; quoted (L)-failure 4% and 1.2% unlabelled | refuted claim | Quoted '≈ 4% at (200,750) and ≈ 1.2% at (1600,10120)' are for s0=5 (config B), unlabelled; config A (s0=3) gives 2.7%, 1.8%, 1.2%, 0.8% | labelling error (W5-VMASK R4); formula VERIFIED by simulation | W3-PXN/PROOF.md; W5-VMASK/REPAIRS.md | [pos 742] | feeds: none |
| RF146 | PXN P7 Beta shape (n-3-s)/2 | refuted claim | Posterior-addition x_{S°,l} ~ Beta(1/2, (n-3-s)/2) by Lemma B(ii); correct shape (n-2-s)/2 | ERROR (A-REV3; A-REV8), not load-bearing | W3-PXN/PROOF.md; A-REV3/REVIEW.md; A-REV8/REVIEW.md | [pos 742] [pos 919] | feeds: none |
| RF147 | 9<=g<=16 range at n=200; SIZE range; W7 CE1 consequence | refuted claim | '9 <= g <= 16' as the admissible group size at the study's n=200 (B=14); valid only for n>=256; correct range g in [floor(B/2)+1, B] (8..14 at n=200) | COUNTEREXAMPLE (W7 CE1, deterministic) | W7-PART/PROOF.md; W7-PART/REPORT.md | [pos 717] [pos 796] | feeds: none |
| RF148 | not laminar => blocks != groups | refuted claim | Implicit step in W7 CE3: failure of laminarity forces blocks != groups; false in general since the cut can split a bad node of size > B back into whole groups | not proved / false in general (W7 Remark 2) | W7-PART/PROOF.md; W7-PART/REPORT.md | [pos 717] [pos 796] | feeds: none |
| RF149 | DM(i) size sign; Prop DM(i) -log A >= -log P_t(N<=K) | refuted claim | claim -log A_t(s0) >= -log P_t(N<=K) ~ 0 has the wrong sign | ERROR (A-REV9); replaced by -log A >= log P_t(N<=K) and by M3(d) 'no sign claim for -log A' | A-REV9/REVIEW.md; O-DILUTE/THEORY.md §7 | [pos 821] [pos 843] | replaced by TH171/TH172 as used in M3(d) |
| RF150 | Common plug-in sigma^2 is the right tool for the n = 200 dilution masking (O-MIX 1/10) | refuted claim | O-MIX recommendation of (C) for the dilution mechanism | rejected (E-SPINE 2.2, W8-SYNTH 4.5); refuted by O-DILUTE 5, F-SIGMA Thm S6, API-RESID Step 0 on 2400 real fits (0/2400 favourable) | O-DILUTE/REPORT.md §5; F-SIGMA/REPORT.md; API-RESID/REPORT.md §2; T38-RECORD/REGISTRY_v2.md (C23); E-SPINE/Docs/Theory/AMENDMENTS_20261102.md | [pos 763] [pos 807] [pos 850] [pos 937] [pos 1009] | replaced by: residualised tables (CJ162) if any start change |
| RF151 | W1-EXP weak-signal masking explains n = 200; WeakSignal; Needs escalation 3 | refuted claim | CL(L) with bounded L for a few weak truths, c = number of weak truths, pi0 concentrates on S0 minus them; pi(S0) also small | ERROR / retired (W3-VEXP row 27, W3-PXN Prop W: 'evidence against'); replaced by dilution masking; XF none | W1-EXP/REPORT.md; W3-VEXP/REPORT.md; W3-VEXP/REPAIRS.md §D; W3-PXN/REPORT.md; T38-RECORD/REGISTRY_v2.md | [pos 348] [pos 352] [pos 361] [pos 370] [pos 584] [pos 594] | replaced by PropD-dilution, PXN-W and TH171-TH178 |
| RF152 | N1 singleton bound controls multi-variable blocks | refuted claim | expected null inclusions bounded by t sum_l BF1(r_ly^2) for truth-free blocks | ERROR (A-REV9) on pointwise expectation bound; heavy-tail rate GAP | A-REV9/REVIEW.md; O-DILUTE/THEORY.md §3 | [pos 821] | replaced by: nothing (excluded) |
| RF153 | Lemma N parenthetical: zero truth correlation implies independence of (y,X_-l) | refuted claim | parenthetical in the premise of Lemma N | ERROR (A-REV9); replaced by explicit joint-independence premise | A-REV9/REVIEW.md; O-DILUTE/THEORY.md §3 | [pos 821] | replaced by LM131 as restated |
| RF154 | Prop S product denominator | refuted claim | pi0(S0)<=1/prod_i(1+[M_(i)-(i-1)]_+) | retired: GAP (A-REV9, not shown false); 'do not retain without a new proof'; weaker pi0(S0)<=1/(1+max_j M_j) | A-REV9/REVIEW.md; O-DILUTE/THEORY.md §5 | [pos 821] | replaced by weaker 1/(1+max_j M_j) |
| RF155 | (T_n+1)Delta_n < 1 in 0/56 runs at n <= 3,200 | refuted claim | W5-FAVIID REPORT headline 5 count | corrected to 1/56 (S3 p=500 n=3200, 0.997) by API-FAVIID; median 1.5 at 6400 and 1.6 at 12800 | API-FAVIID/REPORT.md; API-FAVIID/W5-FAVIID_REPORT_AMENDED.md | [pos 978] | amended report replaces original |
| RF156 | Truth context changes Q-bar by <= 4-5% (per design) | refuted claim | evidence for Conjecture B' | holds only at the cell median; single rows 0.31-5.1, 197/1200 outside [0.9,1.1] | API-FAVIID/REPORT.md §4 | [pos 978] | amended report replaces original |
| RF157 | q/xi_n 0.60-0.82 in every cell, factor 5 to spare | refuted claim | Theorem A moment check | holds only at the cell median; cell means 0.65-2.23, 20/1600 designs exceed 3.83 (max 30) | API-FAVIID/REPORT.md §4 | [pos 978] | amended report replaces original |
| RF158 | T22(i) vacuous at every n <= 3,200 in S3/S4/S6 | refuted claim | finite-n usefulness of locked T22(i) | holds only in the cell median; 5/80 S3 designs at n=3200 have bound <= 1 | API-FAVIID/REPORT.md §4 | [pos 978] | amended report replaces original |
| RF159 | (C-fix) iteration delivers S' in general | refuted claim | fixed point of the plug-in iteration near S0 (OMIX-Cfix) | refuted outside BO: runaway to /mode/=K (C-E4; exact numerics + PROOF SKETCH); 2113/2400 real fits at cap (API-RESID) | F-SIGMA/REPORT.md §7; API-RESID/REPORT.md §2 | [pos 763] [pos 1009] | replaced by: do not deploy; residualised tables |
| RF160 | Favourable from n ~ 800-1,600 (and other single thresholds); 590-730 / 800-1,600 / 1,050-3,200 | refuted claim | single 'favourable from n ~' figure for the start | withdrawn: sources disagree (O-DILUTE 590-730; W3-VEXP 800-1,600; W5-FAVIID 1,050-3,200); omit or attribute (W8-SYNTH 4.13; E-SPINE 2.3; T38_STATEMENT D6 open) | T38-RECORD/REGISTRY_v2.md; E-SPINE/Docs/Theory/AMENDMENTS_20261102.md; W8-SYNTH/SYNTHESIS.md; F-REFINE/CARDS.md | [pos 807] [pos 850] | replaced by: quote none or attribute W5-FAVIID empirical first n |
| RF161 | First Prop S numbers 10^-3..10^-6 | refuted claim | run-internal numeric claim for the ranking ceiling | corrected to computed 10^-0.8..10^-4.8 (10^-6.7..10^-10.6 in S5) | O-DILUTE/REPORT.md §7 | pos: n/a | replaced by computed values |
| RF162 | F-DRAFT d(S0) BO formula as finite-n predictor; Lemma W1 premise in-sample BO at n=200 | refuted claim | use of F-DRAFT W1 d(S0) formula and its premise for the study designs | fails at n=200: undefined in 132/480 fits, median error 57 nats elsewhere; premise false (BO only in population); FD-W1 itself XF VERIFIED under in-sample BO (A-REV4) | O-DILUTE/REPORT.md §4,§7; O-DILUTE/THEORY.md §4 | [pos 763] | replaced by TH171/TH172 per-block account |
| RF163 | delta-hat_1 ~ 0.99(1-pi0(S0)) at n >= 3200 | refuted claim | W5-FAVIID 4.5 pilot estimate | median 0.985, range 0.26-2.19, sets Delta_n in 24/74 runs (API-FAVIID); sensitivity with u1/(1+u1) | API-FAVIID/REPORT.md §4 | [pos 978] | amended report replaces original |
| RF164 | Headline gain capped at 6/2,400 as rationale against a start change | refuted claim | argument that no start change can improve study accuracy beyond 6 fits (API-RESID, R1_A) | rationale withdrawn (MEET-v31 MINUTES: a changed start does not nest scored sets); data statistic stands (565 posterior misses, 6 resource stops) | API-RESID/REPORT.md §0,§4; MEET-v31/MINUTES.md | [pos 1130] [pos 1251] | replaced by: backfit rejected as WORKHORSE with no theorem |
| RF165 | literal T37; TD(d,m); T37(i)-(iii) as filed; original T37; TD(d,0) w.p.->1; T37(iii); TD(d,0) for d>=1; (duplicate entry RF165 merged) | refuted claim | Literal truth dominance TD(d,m) with clauses (i) exact /S Delta S0/ moves, (ii) union bound, (iii) TD(d,0) w.p.->1 | REFUTED (Prop 1 for d>=1; CEX-1 for d=0); pre-campaign CONJECTURED (not proved) | main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T37_truth_dominance_greedy_repair.md; main@c4ef0dc/Docs/Theory/one_pagers/T37.md; W1-T37R/REPORT.md; W3-VT37R/REPORT.md | [pos 150] [pos 220] [pos 355] [pos 370] [pos 238] [pos 370] | replaced by Theorem A/B/C/W; K66/K67 DROP |
| RF166 | A5(a); literal TD(d,0) strict implies TD'_P; original A5 | refuted claim | Literal strict TD(d,0) implies TD'_P(R_d) (no positivity clause) | ERROR (SF W3-VT37R row 9; XF ERROR A-REV2); repaired by POS (R1-POS XF VERIFIED) | W3-VT37R/REPAIRS.md; A-REV2/REVIEW.md | [pos 370] [pos 570] | replaced by Theorem A (A5, repaired) |
| RF167 | Lemma0(b); Lemma 0(b); posterior miss inference; 0/541 forced remark | refuted claim | On every posterior miss F(S0)<=F(S-hat) no local search delivers S0; so 0/541 repairs is forced by monotonicity | ERROR (SF: inference ERROR, remark GAP; XF ERROR A-REV2); registry CONFLICT C1; true on study data (S-ELS) | W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md; A-REV2/REVIEW.md | [pos 355] [pos 370] [pos 570] [pos 1238] | replaced by Lemma 0(b') and Prop F (L-TA) |
| RF168 | R2-dichotomy; V37 R2; two-way failure dichotomy | refuted claim | Every failed fit is E_LS^c or E_LS with terminal score>=F(S0) | ERROR (XF A-REV2: omits inferior local maximum and capped searches); SF none (authored by verifier) | W3-VT37R/REPAIRS.md; A-REV2/REVIEW.md | [pos 570] [pos 1238] | replaced by Prop F |
| RF169 | TDP-iff-DS; TD'_P iff (L) and all D_S | refuted claim | TD'_P(R) iff (L) and strict one-state events D_S hold for all S | ERROR with exact ties (XF A-REV2); SF VERIFIED (W3-VT37R) in conflict; registry CONFLICT C2 | W1-T37R/PROOF.md; A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md | [pos 570] | replaced by Lemma T / Lemma NT |
| RF170 | Weakest-prose; TD'_P is the weakest; cap needs l>=a+d | refuted claim | TD'_P is necessary and sufficient among conditions keeping move count <= Phi; cap needs l>=a+d | ERROR (SF W3-VT37R row 11, 23/360 designs; XF A-REV2); l>=a+d suffices, exact need l>=tau(S_c) | W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md; A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md | [pos 370] [pos 570] | replaced by corrected prose in Theorem A |
| RF171 | Theorem C (C1) containment; LD exceptional nulls | refuted claim | NA_d events contained in {max_l Z^2>=c(1-o(1/log p))} under LD | ERROR/GAP (miscomputed, SF W3-VT37R R4; XF GAP A-REV2); repaired at sketch level with LD* | W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md | [pos 370] | replaced by Lemma S route |
| RF172 | Theorem C (C2) noise inequality | refuted claim | sd of noise term <= C sigma sqrt(n(/Delta'-Delta/+/Delta''-Delta/)) <= C sigma sqrt(n R+) | ERROR (SF W3-VT37R row 14; ratios 201 and 1,896) | W1-T37R/PROOF.md; W3-VT37R/REPAIRS.md | [pos 370] | replaced by union-model bound LM160 |
| RF173 | R4-excess; V37 R4 printed Gaussian tail | refuted claim | With t^2=2 log p+u^2, p P(/Z/>=u) vanishes | ERROR (XF A-REV2; A-REV5 fix VERIFIED): must use original threshold t | W3-VT37R/REPAIRS.md; A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md | [pos 570] | replaced by tail in t |
| RF174 | PGD-star-misleading; star off by factor 3-4 from C-LD | refuted claim | The constant in star is off by a factor ~3-4 from C-LD's 1/(2A) | misleading (W5-VPGD): C-LD not extremal; star certifies r<0.111, star' r<0.143, Prop G fails for r>1/3 | W3-PGD/PROOF.md; W5-VPGD/REPAIRS.md; W5-VPGD/STAR.md | [pos 550] [pos 742] | replaced by STAR.md summary |
| RF175 | cap-free lattice and exact count; Lat(S) without cap | refuted claim | Lat(S) subset R_{a,d} and the displayed missing-truth count, stated without the size cap K | ERROR (XF A-REV5); repair Lat intersect Omega or s0+d<=K | W6-FIXREV2/STATEMENTS.md; A-REV5/REVIEW.md | [pos 919] [pos 1238] | Theorem A feasible-lattice scope (L-TA) |
| RF176 | Theorem W region form covers masked regime; general sufficient condition for (M2) | refuted claim | Region-form Theorem W (a>=2) as general sufficient condition for masked LH | COUNTEREXAMPLE (W5-VPGD: eta=0, 20/20; D_S fails 200/200); registry CONFLICT C15 | W5-VPGD/REPAIRS.md; W5-VPGD/REPORT.md | [pos 550] [pos 742] | replaced by W_Lat and LH-PGD |
| RF177 | T37 explains n=200 masked successes | refuted claim | The T37 greedy repair explains the n=200 masked-regime successes | refuted by data (S-ELS: final local search made 0 moves in 2,394/2,394; W1 card P(true)=0.1) | W1-T37R/REPORT.md; S-ELS/REPORT.md; W8-SYNTH/SYNTHESIS.md | [pos 355] [pos 763] | data fact ELS-1 |
| RF178 | Theorem B headline 2^Phi(S_c) states no 2^s0 | refuted claim | Headline count 2^Phi(S_c) states for the production (data-dependent) centre | GAP (presentation; W3-VT37R R6): holds only for data-independent centre | W3-VT37R/REPAIRS.md; A-REV2/REVIEW.md | [pos 370] [pos 570] | wording corrected in Theorem B |
| RF179 | initial centre is the truth trivial success | refuted claim | If initial centre is already the truth the fit is a trivial success | ERROR as table shorthand (W6-FIXREV2; A-REV5 VERIFIED disagreement); registry CONFLICT C12 | A-REV2/REVIEW.md; W6-FIXREV2/REPORT.md; A-REV5/REV2_CHECK.md | [pos 570] | Lemma 0(b') |
| RF180 | C3-PGD; SE + BM-inf imply PGD | refuted claim | SE and beta-min imply progress-greedy dominance | COUNTEREXAMPLE (SF VERIFIED W3-VT37R; XF VERIFIED A-REV2) | W1-T37R/REPORT.md; W3-VT37R/REPORT.md; A-REV2/REVIEW.md | [pos 355] [pos 370] | K66 DROP |
| RF181 | exactly /S Delta S0/ moves | refuted claim | T37(i): search moves to S0 in exactly /S Delta S0/ moves | false in general (W1-T37R: tau=Phi-#swaps) | W1-T37R/REPORT.md | [pos 355] | replaced by Theorem A (A2) |
| RF182 | H24; H24 (asymptotic input); T21 route (e) hypothesis H24 | refuted claim | T24 terminal-repair inputs: K1(x,{S0})>=a_n and one-round exit<=eta_n uniformly on R_d with (L+4)eta_n->0 | Retired; CE1 COUNTEREXAMPLE (numerical, SF CONFIRMED); CE1-narrow COUNTEREXAMPLE PROVED (XF VERIFIED A-REV5); H24 as written trivially satisfiable (a_n=0, eta_n=1) per W2-VT24G; register keeps 'not proved' [UNCERTAIN wording] | main@c4ef0dc/Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md; main@c4ef0dc/Docs/Theory/proofs/LOCKED_PROOFS.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md; W6-FIXREV1/CONSOLIDATED.md; T38-RECORD/REGISTRY_v2.md | [pos 156] [pos 296] [pos 342] [pos 370] [pos 510] [pos 550] [pos 570] | feeds: none (campaign-only) |
| RF183 | c_n = 1/(s0+d+B+2)!; factorial constant; 1/31! | refuted claim | T24's entrance constant is 1/31! at s0=14 and useless | Retired as useless (FABLE_REVIEW; confirmed W1-T24G) | main@c4ef0dc/Docs/Theory/theorems/T24_T18p_terminal_repair.md; main@c4ef0dc/Docs/Theory/PAPER_SELECTION_20261028/FABLE_REVIEW.md; W1-T24G/REPORT.md | [pos 238] [pos 342] | feeds: none (campaign-only) |
| RF184 | brief's exponent (1-c')^floor(H/(s0+d)); CE2 target form | refuted claim | P(not scored) <= (1-c')^floor(H/(s0+d)) + ... does not follow from one-step-per-round progress | REFUTED (CE2 COUNTEREXAMPLE; SF CONFIRMED exact rationals); replaced by v(1-c)^floor(H/v) | W1-T24G/BRIEF.md; W1-T24G/PROOF.md; W2-VT24G/REPORT.md; T38-RECORD/REGISTRY_v2.md | [pos 238] [pos 296] [pos 370] | feeds: none (campaign-only) |
| RF185 | LK_d; EXIT_d; GAIN_d; LK_d/EXIT_d/GAIN_d | refuted claim | Uniform-over-R_d hypotheses of T24 (look-alike leakage, exit, gain) | Retired (W1-T24G escalation 2; T24 file withdrew EXIT_d as internal-change control); replaced by Theorem B constants and premises NL0,UDEL,TS,TL,BTP,IND | main@c4ef0dc/Docs/Theory/theorems/T24_T18p_terminal_repair.md; W1-T24G/REPORT.md | [pos 238] [pos 296] | feeds: none (campaign-only) |
| RF186 | Prop. U shortcuts; (U-a); (U-b); PropU shortcut claims | refuted claim | 'Independence acceptance bad iff it leaves F(x) or raises V' and 'extra-for-extra swap is neutral' | ERROR (A-REV1) vs SF VERIFIED as bookkeeping (W2-VT24G) [CONFLICT C3]; repaired by Prop. U' (A-REV5 VERIFIED); Theorem B unaffected | W1-T24G/PROOF.md; A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 296] [pos 370] [pos 470] [pos 570] | feeds: none (campaign-only) |
| RF187 | Lemma S attainment claim; 'attained by two-level weights' | refuted claim | ESS share bound is attained by two-level weights on its full domain | ERROR (A-REV1); inequality VERIFIED; repaired Lemma S' (A-REV5 VERIFIED) | W1-T38E/PROOF.md; A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 570] | feeds: none (campaign-only) |
| RF188 | E3(ii); E3(ii) without q<1; F-REFINE Card 3(i) | refuted claim | Start mass >= (1-q)^{s+1}/(1+e)^s used without the locked hypothesis q<1 | ERROR (A-REV1; SF VERIFIED incl. (ii) by W3-VT38E) [CONFLICT C5]; repaired E3' (A-REV5 VERIFIED); F-REFINE Card 3(i) repeated it (A-REV5 ERROR) | W1-T38E/PROOF.md; A-REV1/REVIEW.md; A-REV5/REV1_CHECK.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 570] [pos 919] | feeds: none (campaign-only) |
| RF189 | Lemma U limit 0.52/c_E; 4.16(M+2sigma^2)/sigma^2; EXP-const (Lemma U part) | refuted claim | kappa_n -> 0.52/c_E | ERROR (A-REV1, A-REV2); true limit 0.51/c_E = 4.08(M+2sigma^2)/sigma^2; finite bound unaffected; repaired W6-FIXREV1 (A-REV5 VERIFIED) | W2-PREM/PROOF.md; A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 570] [pos 742] | feeds: none (campaign-only) |
| RF190 | NL0-inflation; equicorrelated inflation 1.86; p >~ n^0.58 | refuted claim | Equicorrelated nulls give Z^2 inflation (1+r)/(1-r)=1.86 so NL0(1) fails for p>~n^0.58 | ERROR inside a PROOF SKETCH (W2-VT24G); true inflation 1+r=1.3, threshold p >> n^{5/3} at r=0.3 | W1-T24G/PROOF.md; W2-VT24G/PROOF.md | [pos 370] | feeds: none (campaign-only) |
| RF191 | sup-of-sum NL0; W1 section 6 premises imply H*eta->0; NL0 quantifier | refuted claim | NL0 stated as sup_W sum_l o_l but eta uses sum_l sup_W o_l | GAP (A-REV1); repaired NL0' (A-REV5 VERIFIED) | W1-T24G/PROOF.md; A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 742] | feeds: none (campaign-only) |
| RF192 | FamilyDefect; W1 repair family with A = neighbour graph | refuted claim | With A(x)= neighbours of missing truths, eta1 -> 0 (premise TL(Z,A)) | COUNTEREXAMPLE (W2-PREM; numerical, asymptotic PROOF SKETCH); fixed by Theorem B-sharp | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| RF193 | Lemma U C3 lower bound; C3-low | refuted claim | Matching lower bound on odds with zero leakage only | ERROR (A-REV2); repaired (mu in span X_T); A-REV5 VERIFIED | W2-PREM/PROOF.md; A-REV2/REVIEW.md; A-REV5/REV2_CHECK.md | [pos 570] | feeds: none (campaign-only) |
| RF194 | NL0(1)/UDEL(2) under G,R,SE,BM-inf alone | refuted claim | Hoped that NL0(1) and UDEL(2) hold without design conditions | COUNTEREXAMPLE EQ (asymptotic; PROVED modulo extreme-value facts); PROVED UNDER PG(a) | W2-PREM/PROOF.md | [pos 424] | feeds: none (campaign-only) |
| RF195 | TS from SE; truth stability under SE | refuted claim | Truth retention at incomplete states follows from G,R,SE,BM-inf | COUNTEREXAMPLE (cancellation pair; PROVED computation) | W2-PREM/PROOF.md; W1-T24G/PROOF.md | [pos 424] | feeds: none (campaign-only) |
| RF196 | W1 evidence non-production pi0; S5 masked mode {0,2,13,14} | refuted claim | Start-law numbers computed with non-production block packing | GAP (evidence), W2-VT24G; qualitative conclusions survive | W2-VT24G/REPORT.md | [pos 370] | feeds: none (campaign-only) |
| RF197 | brief's eligibility condition; F(S°) > sup_{R_d^c} F | refuted claim | The best-scored model before the final search lies in R_d because F(S°) > sup over states outside R_d (T02/T03-type) | REFUTED (Prop E1; fails w.p. -> 1 under omission masking); SF VERIFIED (deterministic part) | W1-T38E/PROOF.md; W1-T38E/BRIEF.md | [pos 238] [pos 370] | replaced by LS0 eligibility (E3) / bridge discovery; feeds none |
| RF198 | set analogue of T22(iv); inf_phi q_phi(A) >= min{pi0(A),pi(A)} | refuted claim | Bridge mass of a set is never below the smaller endpoint mass | REFUTED (C0); SF VERIFIED | W1-T38E/PROOF.md | [pos 370] | replaced by Lemma B (LM173); feeds none |
| RF199 | start mass + bridge mass + exit control imply delivery; Bridge mass => delivery | refuted claim | Start mass on R_d, uniform bridge mass and exit control imply a near-truth particle at the terminal rounds | REFUTED (C1, reproducible; SF VERIFIED* after kernel repair) | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | replaced by D4/D5 (TH248, TH249), closure F1, LH confinement (TH271); feeds none |
| RF200 | Kantorovich-1.925; ratio 1.925 gives ESS>=0.9H | refuted claim | M/m <= 1.925 implies ESS/H >= 0.9 (and NB with log 1.925) | ERROR (cosmetic), repaired: r* = (11+2 sqrt 10)/9 = 1.9249506 (W3-VT38E, A-REV1 agrees) | W3-VT38E/REPORT.md; W1-T38E/PROOF.md | [pos 370] | replaced by r* and NB'; feeds none |
| RF201 | LemmaS-attain; Lemma S tight on the full domain | refuted claim | Lemma S bound is attained by two-level weights (tight) for all f | ERROR on f <= 1-e (A-REV1); W3-VT38E had VERIFIED; repaired Lemma S' (W6-FIXREV1) | W1-T38E/PROOF.md; W6-FIXREV1/CONSOLIDATED.md | [pos 557] [pos 570] | replaced by Lemma S' (LM174); feeds none |
| RF202 | E3(ii); start-law lower bound without q<1 | refuted claim | T22(i) gives pi0(x°) >= (1-q_n)^{s+1}/(1+e_n)^s with no hypothesis on q | ERROR (A-REV1 Section 3.3); W3-VT38E had VERIFIED; E3' PROVED (W6-FIXREV1) | W1-T38E/PROOF.md; W6-FIXREV1/CONSOLIDATED.md | [pos 557] [pos 570] | replaced by E3'(ii) with 0<=q<1 (TH243); feeds none |
| RF203 | SHARE-M(b); Proposition M(b); Prop M (b) | refuted claim | Under G,R,SE,BM-inf every T in R_d missing a truth has an addition with odds >= 1 for all phi >= phi_n = lambda_n/(lambda_n+g_n) -> 0 (no posterior barrier near the truth) | PROOF SKETCH (W4-SHARE); SF argument correct, upgraded on LH (W5-B2ENV); XF ERROR (A-REV3, retained A-REV6): quadratic expansion remainder of order n; vanishing crossing temperature false under BM-C; GAP no deletion/traversal bound | A-REV3/REVIEW.md; W4-SHARE/PROOF.md; T38-RECORD/REGISTRY_v2.md | [pos 742] [pos 807] [pos 1361] | replaced on LH by Prop M-LH (TH270); dropped as K98 KNOWN-FALSE |
| RF204 | SHARE-B2W4-exitloss; exit-loss simplification | refuted claim | In B2-W4, -sum log(1-eta_t) may be replaced by sum eta_t with coefficient one (condition sum eta <= log(N/T) - omega(1)) | ERROR (A-REV3, two-state counterexample); repair pending (valid replacement 2 sum eta for eta<=1/2) | W4-SHARE/PROOF.md; A-REV3/REVIEW.md | [pos 742] [pos 807] | replaced by exact negative-log product; feeds none |
| RF205 | SHARE-SH-prose; FSH-rareoutsider; rare-outsider sharp transition | refuted claim | Universal zero-to-one extinction transition at kappa ≈ log(N pi0(a)/pi0(o)), including pi0(o) = 1/N (also in F-SHARE sharpness remark) | GAP (A-REV3); ERROR for F-SHARE's form (A-REV6) | W4-SHARE/PROOF.md; F-SHARE/REPORT.md; A-REV3/REVIEW.md | [pos 742] [pos 919] | replaced by exact formula with N pi0(a) -> infinity and N pi0(o) -> infinity regime; feeds none |
| RF206 | FSH-retention; retention inequality prod(1-eta_s) >= e^{-T eta} | refuted claim | prod_{s}(1-eta_s) >= e^{-T eta} (F-SHARE Section 5.2) | ERROR (A-REV6: at T=1, eta=1/2, 1-eta < e^{-eta}); no repair written | F-SHARE/PROOF.md; T38-RECORD/REGISTRY_v2.md | [pos 748] | feeds none |
| RF207 | FSH-DOMc1; DOM void for c = 1 | refuted claim | DOM is void when c = 1 (swap a1 -> b1 is the same-unit case of PK-s) | ERROR (A-REV7): fails when visible groups are present; the c=1 no-visible-group case unaffected | F-SHARE/PROOF.md; F-SHARE/REPORT.md; A-REV7/REVIEW.md | [pos 748] [pos 919] | feeds none |
| RF208 | OBG-LH-lock-general; general LH locking; LH-lock for general (rho,psi,g,c) | refuted claim | Strict gaps C1-C3 (LH locking) hold for all LH parameters with /psi/ < rho | ERROR (A-REV7): C2 fails e.g. g=4, rho=0.85, psi=0.5; reproduced by Claude (API-VSTAB) | O-BGIBBS/REPORT.md; A-REV7/REVIEW.md; API-VSTAB/REPORT.md | [pos 824] [pos 919] [pos 941] [pos 945] [pos 978] | replaced by conditional fixed-p LH-lock (TH261) and (CERT) corollary (TH276); feeds none |
| RF209 | Lemma 3.4 Schur increment; displayed ridge identity | refuted claim | Q_{x-j} - Q_x = n (ytilde_j' y)^2/(xtilde_j' x_j + 1/(n+1)) | ERROR (A-REV7): correct increment is [n/(n+1)] (x_j'Ay)^2/(x_j'Ax_j + 1/(n+1)); repairable with additive bound | F-SHARE/PROOF.md; A-REV7/REVIEW.md | [pos 919] | feeds none |
| RF210 | enlarged class W+; W+(S°) = W(S°) ∪ {x - j + b'} | refuted claim | The enlarged class W+ absorbs the DOM leak and is closed under the kernel | refuted by exact enumeration (F-SHARE, +175 nats at LH20 n=1600) | F-SHARE/PROOF.md; F-SHARE/REPORT.md | [pos 748] | replaced by reversible-leak theorem F1' (CJ200); feeds none |
| RF211 | SHARE and LT as route-(b2) hypotheses; grid-based conditions for SHARE | refuted claim | SHARE or LT (or an ESS-grid condition) is the right delivery hypothesis for route (b2) | superseded/refuted (W4-SHARE: Prop G, C1 with method grid, C1 w/o o, PB); LT not necessary | W4-SHARE/REPORT.md; T38-RECORD/REGISTRY_v2.md | [pos 444] [pos 742] | replaced by D4/D5 envelope and closure/confinement; feeds none |
| RF212 | Without LS0 no masked-regime consistency theorem; Not claimed (W4-T38FULL II.9, W6-FIXREV1) | refuted claim | Without LS0 the paper has no masked-regime consistency theorem | retired (A-REV7 VERIFIED B2-LH under STAB-LH and D2-LH; API-VSTAB VERIFIED the certificate); unrestricted LH still not claimed | T38-RECORD/T38_STATEMENT.md; T38-RECORD/REGISTRY_v2.md; A-REV7/REVIEW.md | [pos 919] [pos 978] | replaced by (b2-LH) (TH272, TH275); feeds M5 variant clause K70 |
| RF213 | limit form P(Shat = S0) -> 1 - limsup P(U) | refuted claim | P(Shat = S0) -> 1 - limsup P(U) (T38 brief) | not a well-formed limit (W1-T38E); VERIFIED (W3-VT38E) | W1-T38E/REPORT.md; W1-T38E/BRIEF.md | [pos 238] [pos 370] | replaced by liminf P(U^c, Shat+ = S0) >= 1 - limsup P(U) (TH241) |
| RF214 | D2 covers one-cancellation masking including p >> sqrt(n) (CF(1) instances) | refuted claim | D2 covers one-cancellation masking at every p <~ n^A including p >> sqrt n where iid discovery fails | GAP (overstated) (W3-VT38E): holds only conditionally; CF(1) instances not masked | W1-T38E/REPORT.md; W3-VT38E/REPORT.md | [pos 370] | replaced by conditional D2-inf (TH242) and LH instance TH269 |
| RF215 | GUARD literal; every reported output equals R-bar's; W2-BOOK GUARD literal full-output claim | refuted claim | W2-BOOK GUARD: 'on G^c, st = st-bar, and every reported output equals the corresponding component of R-bar' | ERROR (A-REV4 B1; A-REV8 E2): statistical-output transfer survives; replaced by the projected stop-only coupling on statistical outputs, scored sets, decisions and status | A-REV4/BOOK_CHECK.md; A-REV4/REVIEW.md; A-REV8/REVIEW.md E2; W5-LOCKBOOK/AUDIT.md s1 | [pos 696] [pos 742] [pos 919] [pos 1238] | S-OUT GUARD-W (statistical scope) |
| RF216 | LS-score move count; at most Phi(C0)-1 moves (literal) | refuted claim | Lemma LS-score: 'It needs at most Phi(C0) - 1 moves.' (negative at C0 = S0) | ERROR (A-REV8 E1); repaired to max{Phi(C0)-1, 0}; scoring conclusion unaffected | A-REV8/REVIEW.md E1; W4-T38FULL/T38_PROOF.md s3.1 | [pos 843] [pos 919] | M5 (a): LS0 scores S0 within max{Phi(S°)-1,0} moves |
| RF217 | T38-b1-LH-iidfail; (b1-LH) iid-failure clause for c>=2; Q_f pi0(S0) -> 0 for c>=2 and p -> infinity | refuted claim | (b1-LH) in v1/v2: 'Q_f pi0(S0) -> 0 when c >= 2 and p -> infinity, or c = 1 and p/(sqrt(n) log^2 n) -> infinity' | ERROR (A-REV5, counterexample p ~ log log n) / GAP (A-REV8 G1); recorded at the weaker verdict (ERROR); replaced by the growth condition n^{1-c/2} p^{-c} log^2 n -> 0 (c=2: p/log n -> infinity); LS0 consistency unaffected; FUTURE_WORK FW10 | A-REV5/REVIEW.md s2; A-REV5/REV1_CHECK.md s4; A-REV8/REVIEW.md G1; T38-RECORD/T38_STATEMENT.md V18, III.13 | [pos 807] [pos 843] [pos 919] | FUTURE_WORK FW10 (K71); excluded from M5 |
| RF218 | Without LS0 the paper has no masked-regime consistency theorem whose premises are all proved on an explicit family | refuted claim | W4-T38FULL II.9: 'So without LS0, the paper has no masked-regime consistency theorem whose premises are all proved on an explicit family.' (also v2 Not claimed, F-REFINE) | retired: no-LS0 candidates on LH now exist ((b1'-LH) A-REV7 VERIFIED qualitative; (b2-LH) A-REV7 VERIFIED conditional + Astra STAB certificate, API-VSTAB verified); replaced by 'candidates on LH, pending cross-family review' then by (b1'-LH), (b2-LH) in I.C | W4-T38FULL/T38_STATEMENT.md II.9; T38-RECORD/T38_STATEMENT.md V10, III.2; A-REV7/REVIEW.md s4; T38-RECORD/REGISTRY_v2.md D | [pos 364] [pos 763] [pos 919] [pos 978] | M5 (b2-LH) variant (K70) |
| RF219 | T32(i) is a CONJECTURE (stale status in W6-FIXREV1 k1 and W7-SEP I11) | refuted claim | W6-FIXREV1 dependency k1: 'T32(i) ceiling: CONJECTURE'; W7-SEP input I11 | retired as stale: T32(i) PROVED by W5-LOCKBOOK, re-counted by W7-SEC (SF); XF A-REV6 'supported by loop accounting', A-REV9 deferred (registry conflict C18) | W6-FIXREV1/T38_STATEMENT.md II.6; T38-RECORD/T38_STATEMENT.md III.1; T38-RECORD/REGISTRY_v2.md A2 C18 | [pos 463] [pos 742] [pos 919] | M8 Proposition D context |
| RF220 | LH-LAT margin m0 is sharp | refuted claim | W4-T38FULL Prop. LH-LAT: 'POP-LAT(S°, m0) holds on LH with an explicit m0 > 0, which is sharp' | GAP (overstatement) (W5-VMASK R5); sharp for homogeneous pairs (108/108), not sharp in 32/94 heterogeneous settings (down to 0.002); replaced by 'valid lower bound; exact margin m0-sharp' (V4); A-REV8 agrees | W4-T38FULL/T38_STATEMENT.md II.3 b1.8; W5-VMASK/REPAIRS.md R5; W5-VMASK/REPORT.md row 23'; A-REV8/REVIEW.md | [pos 463] [pos 843] | M5 (b1-LH) uses m0 > 0 only |
| RF221 | E[Zhat / completed] = Z; conditioning on completion; 'unbiased given output' | refuted claim | Identities in expectation (E[Zhat]=Z, E[Zhat PIPhat]=Z PIP) hold conditionally on output / completion | REFUTED (CEX-guard, exact stylised counterexample; W5-LOCKBOOK reproduced it and also under the engine-faithful cost rule; A-REV4 VERIFIED qualitatively); replaced by output-intersected statements P(O, .) via Lemma RO; also theme 8 (Prop 2) | W2-BOOK/PROOF.md s0.3; W2-BOOK/REPORT.md; W5-LOCKBOOK/REPORT.md; A-REV4/BOOK_CHECK.md | [pos 328] [pos 342] [pos 742] | S-OUT K77; M4 K78 (joint with output) |
| RF222 | T11(vii) citation in the composition proof | refuted claim | W1-T38E s7 step (1): 'the running-best rule over S+ returns S0 (T11(vii); no tie is possible since the maximum is strict)' | incorrect citation (A-REV1 s8; A-REV5 'T38 citation and cap'): T11(vii) does not exist; replaced by the direct set argument = locked T21(C1) (v2 S6); also K = min(p, floor(n/2)) not floor(n/2) | W6-FIXREV1/T38_STATEMENT.md S6; A-REV1/REVIEW.md; A-REV5/REVIEW.md | [pos 570] [pos 807] | M5 (0) (locked T21(C1) argument) |
| RF223 | P(S-hat = S0) -> 1 - limsup P(U) (brief's limit form) | refuted claim | T38 brief: 'P(S-hat = S0) -> 1 - limsup P(U)' | ill-posed as a limit (W1-T38E s7; W3-VT38E VERIFIED trivial); replaced by liminf P(U^c, S-hat+ = S0) >= 1 - limsup P(U), and P(U^c, S-hat+ = S0) -> 1-u if P(U)->u | W1-T38E/PROOF.md s7; W3-VT38E/REPORT.md; main@c4ef0dc/Docs/Theory/one_pagers/T38.md | [pos 201] [pos 370] | M5 (0) liminf form |
| RF224 | brief's cost O(N T (p+B+2) + l p) for T38(c) | refuted claim | T38 brief (c): 'expected score evaluations O(N_n T_n (p + B + 2) + l_n p)' | incorrect (W1-T38E s7): omits the scan's k(p-k) swaps and the number of local searches; replaced by T32(i) ceiling plus (l+1) max_k[p+k(p-k)] (+1 for the emitted centre, A-REV1/R7) | W1-T38E/PROOF.md s7; W5-VMASK/REPAIRS.md R7; main@c4ef0dc/Docs/Theory/one_pagers/T38.md | [pos 201] [pos 370] [pos 463] | M8 Proposition D (cost) |
| RF225 | T26-exact-branch-paren; "the exact branch fails for p>=18, n>=22"; T26 exact-branch aside | refuted claim | Claim in W2-T26 that at p>=18 and n>=22 the exact-enumeration branch is not taken (used to call (P1-ex) vacuous); false at p=18, n=2^18 | ERROR (XF A-REV4 section 7; confirmed A-REV5, A-REV6); repair [PENDING], none written; replacement: exact combinatorial branch criterion | W2-T26/PROOF.md; W2-T26/REPORT.md; A-REV4/REVIEW.md; A-REV5/REVIEW.md; A-REV6/BOOK.md | [pos 342] [pos 677] [pos 796] [pos 1233] [pos 1238] | none (supporting remark only; K76 eventual exact dispatch seat-proved) |
| RF226 | pooled Z-hat x pooled PIP unbiased; pooled x pooled PIP | refuted claim | Claim that the pooled evidence times the pooled primary PIP is unbiased for Z PIP_j; exact bias is -(3/4)Cov(PIP_1j,Z_1) | REFUTED (Prop 2(c)); SF reproduced to 1e-58; XF VERIFIED (A-REV4) | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | M1 K50 negative result; S-POOL |
| RF227 | E[Z-hat/completed]=Z; unbiasedness given completion | refuted claim | Claim that conditioning on the output-available event preserves E[Z-hat]=Z | COUNTEREXAMPLE (CEX-guard, exact enumeration); SF reproduced (also engine-faithful costs); XF VERIFIED* (A-REV4, stylised) | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | M1/S-OUT/S-POOL/L-RO negative result |
| RF228 | OPW2-cex; PW2 with a_t=chi2_t; perfect-mixing guess | refuted claim | Claim that PW2 holds with a_t=chi2_t (T13-only constant) and that prod(1+chi2_t/N)-1 bounds the actual variance | COUNTEREXAMPLE (numerical, exact enumeration p<=10); not otherwise reviewed | O-PW2/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | S-Z Proposition Z (ii) (exact-refresh product never substituted) |
| RF229 | F-MASKPIP M3 printed instance; P(W_r<c/C)=1 | refuted claim | Claim that for every kappa in (0,1), delta1 in (0,1/4) an abstract instance has P(W_r<c/C)=1 for some c<1 | ERROR (XF A-REV9: forces E[W/C]>=1.6 at kappa=1/2, delta=1/10) | F-MASKPIP/REPORT.md; A-REV9/REVIEW.md; A-REV9/MASKED_PW2_CHECK.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | K53 (FMP-M3 XF ERROR) |
| RF230 | all bounded h converge to the generating value; section 13.1 as drafted | refuted claim | Claim that SMC estimates of E[h] converge to h(theta*) for every bounded h | COUNTEREXAMPLE (equality indicator); Astra-on-Astra VERIFIED* (A-REV4) | A-DRAFT/REPORT.md; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 493] [pos 494] [pos 563] [pos 616] [pos 677] | replacement text for draft 13.1 (TH323) |
| RF231 | API-MASKZPIP first-draft LH evidence collapse; floor phi_1>=1/T_e | refuted claim | First-draft claim that on LH the method Z-hat underestimates by e^{-Theta(n)/T_e} via the floor phi_1>=1/T_e | retracted by its author (wrong for the method: floor belongs to the pilot, V contains top 20p scored models); survives for a blind grid only | API-MASKZPIP/REPORT.md | [pos 909] [pos 911] [pos 957] [pos 978] | none |
| RF232 | full-output expectation E[1_O Z-hat]<=Z P(A); LOCKBOOK-exactexp(A6) | refuted claim | Claim that E[1_O Z-hat_rep]<=Z P(A) holds jointly over random data and with SMC-only A on the exact branch | GAP (A-REV4 B3/B4); ERROR in the W5 form (A-REV6); replacement A-REV6 R2 candidate pending Claude verification | W2-BOOK/REPORT.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md; A-REV6/BOOK.md; A-REV6/REVIEW.md | [pos 677] [pos 806] | none (repair pending) |
| RF233 | Z-hat can only fail downward in the masked regime; THM-SYNTH A2 plain sentence; THM-SYNTH Theorem Z: "in the masked regime Zhat errs only downward"; (duplicate entry RF233 merged) | refuted claim | Plain-language claim that in the masked regime Z-hat errs only downward | PROVED false (PC1 claim 4, theorem-meeting phase); formal tail statement untouched; also owned by theme 12 (THM-SYNTH) | MEET-v31/evidence/2026-11-03_PC1_proof_check.md | pos: n/a (theorem-meeting phase) [pos 1177] [pos 1242] | S-Z Proposition Z (iii) exception-probability form |
| RF234 | resource_limit as sigma(C) launch event; T12(iv.d) coverage of resource_limit | refuted claim | Treating resource_limit as a sigma(C)-measurable launch event covered by T12(iv.d) | fails (W2-BOOK section 5); fixed by potential run R-bar and Lemma RO | W2-BOOK/REPORT.md; W2-BOOK/PROOF.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | L-RO / S-OUT |
| RF235 | frozen second premise (L_n+4)rho*_n->0; one-pager T26 restatement | refuted claim | Premise (L_n+4)rho*_n->0 of the FROZEN_LIST T26 restatement, needed to control departure over L+4 terminal rounds | retired as redundant (PROVED, W2-T26 Lemma 3; SF CORRECT; XF VERIFIED (A-REV4)); replaced, not refuted | W2-T26/PROOF.md; W2-T26/REPORT.md; W5-LOCKBOOK/STATEMENTS.tex; A-REV4/REVIEW.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] [pos 919] | none |
| RF236 | OPTIONAL_PW2 (A)-(C) one-step parent-uniform route; T25(iv) B_T with those constants | refuted claim | Route requiring sup_x K_{t-1}g_t(x)<=1+O(1/N) (false for any imperfect kernel) making T25(iv) B_T vacuous (about 1-223 vs truth <=0.1) | vacuous (numerical, exact enumeration); replaced by martingale route (TH316/TH317) | O-PW2/REPORT.md | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | none |
| RF237 | O-CERT C1(b) unscored-mass sentence; C6 G3; unscored and unreported mass | refuted claim | "The posterior mass of the unscored and unreported models is at least 1 - Z_T/(alpha Zhat)" is false for unscored mass (bound is for mass outside T) | REFUTED by O-VCERT (counterexample CE189), A-REV9 ERROR for the original wording; replaced by R1 (TH332) | O-VCERT/REPORT.md; A-REV9/REVIEW.md; O-CERT/REPORT.md | [pos 763]; [pos 917] [pos 919] | none |
| RF238 | O-CERT C1(a) self-inclusive gap inequality | refuted claim | "For every scored S in T, pi(S)/pi(S-hat) = e^(F(S)-F(S-hat)) <= e^-g" includes S = HPM | ERROR as literally quantified (A-REV9); repair: exclude HPM | A-REV9/REVIEW.md; O-CERT/REPORT.md | [pos 830]; [pos 917] [pos 919] | K42 status cell carries "XF ERROR as quantified" |
| RF239 | O-CERT C5 tie-insensitive prose | refuted claim | F(S0) <= F(S-hat) is certified as a posterior miss without tie order or /S0/ <= K | ERROR (A-REV9) on tie-insensitive prose; strict-score inclusion VERIFIED; SF VERIFIED* with tie caveat (O-VCERT S3) | A-REV9/REVIEW.md; O-VCERT/REPORT.md | [pos 763]; [pos 917] [pos 919] | none |
| RF240 | O-CERT C6 floating-point clause alpha e^eta + eps | refuted claim | FP bound claimed without SC(eta_F) inflation of the G items (Z_T^fp can exceed Z) | GAP (O-VCERT, A-REV9); replaced by R2 (TH333); P(A) factor difference is weaker-vs-sharper, not an error | O-VCERT/REPORT.md; A-REV9/REVIEW.md; O-CERT/REPORT.md | [pos 763]; [pos 917] [pos 919] | none |
| RF241 | O-CERT overstatement: cannot certify confidence without PW2 or enumeration | refuted claim | Prose overreach on C1(c): any certified upper bound on Z gives a sure lower bound on pi(S-hat) | Overstated (O-VCERT S2); A-REV9 agrees with corrected scope | O-VCERT/REPORT.md; O-CERT/REPORT.md | [pos 706]; [pos 763] | none |
| RF242 | O-SWAP Props 1-3 PROVED under PA; displayed Prop. 2 event identity | refuted claim | Displayed superset law with deterministic Omega_0 stated as an identity under PA alone | ERROR if asserted under PA alone; predicted rates GAP (A-REV9); no repair written | A-REV9/REVIEW.md; O-SWAP/REPORT.md | [pos 830]; [pos 917] [pos 919] | none |
| RF243 | O-SWAP "4 no-output fits are excluded" | refuted claim | Number of stopped fits stated as 4; true number is 6 (S-ELS); cells rescaled to 100 | Superseded by S-ELS count 6; logged by W8-SYNTH 4.13 | O-SWAP/REPORT.md; S-ELS/REPORT.md; W8-SYNTH/SYNTHESIS.md | [pos 578]; [pos 763] | none |
| RF244 | Engine error_bound() is a bound; R9 global_certified rigorous; T33-errbound | refuted claim | Engine heuristic eta_eng (v3_score.h:241-246) is exceeded by the true score error at large n | COUNTEREXAMPLE (W7-SEC author check); implementation fix recommended, not a method change; n=200 unaffected | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md | [pos 711]; [pos 742] | FUTURE_WORK FW16 (K107) |
| RF245 | W5-LOCKBOOK T32(i-lit) proof slip 1+4l >= 5l | refuted claim | Inequality 1+4l >= 5l used in the corollary proof is false for l >= 2 | Harmless slip; conclusion stands with 4l (W7-SEC, same family) | W7-SEC/REPORT.md | [pos 711]; [pos 742] | M8 Proposition D (T32(i) status cell) |
| RF246 | S-ELS move cap l=10 at both p | refuted claim | Move cap l stated as 10 at both p; l=11 at p=1000 | Minor inaccuracy corrected by O-LS0-WRAP; no effect on counts | S-ELS/REPORT.md; O-LS0/REPORT.md | [pos 715]; [pos 760] | none |
| RF247 | W8-SYNTH: O-LS0 check has not landed | refuted claim | SYNTHESIS section 1 states the O-LS0 data check has not landed | Stale: landed 20:24 UTC and passed (0/2,394); HQ corrected [pos 793] | W8-SYNTH/SYNTHESIS.md; campaign/LEDGER.md; O-LS0/REPORT.md | [pos 763]; [pos 793]; [pos 796] | none |
| RF248 | O-SWAP predictors T1 (independence) and T1-lo (cluster maximum) | refuted claim | T1 overshoots at c=0.5 (326/383 vs 230/259); T1-lo undershoots by half (118/141) | Retired predictors, replaced by T2 (TH342), itself an approximation | O-SWAP/REPORT.md | [pos 578]; [pos 742] | none |
| RF249 | Union bound over Hamming balls bounds Pi(X) | refuted claim | Distance-2 superset union bound ~0.07 at p=500, c=1, as large as the whole one-add rate | Failed route (API-N200); see CE195; CJ230 remains OPEN | API-N200/PROOF.md; API-N200/REPORT.md | [pos 978] | FUTURE_WORK FW14 (K94) |
| RF250 | A-priori epsilon of VAL-FP certifiable at study budgets | refuted claim | Union bound over 1e8-1e11 final-run decisions: epsilon from 2e-3 to >>1 | Vacuous (W7-SEC); measure by replay | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md | [pos 711]; [pos 742] | FUTURE_WORK FW16 (K107) |
| RF251 | HQ premise: size prior not monotone, marginal likelihood is | refuted claim | Brief to O-VCERT: "the size prior is NOT monotone in /S/; the marginal likelihood is" | Refuted by O-VCERT: w and size marginal non-increasing; m(S) not monotone | O-VCERT/REPORT.md | [pos 729]; [pos 763] | none |
| RF252 | F-DRAFT Theorem W(c) divergent side; FD-W(c) | refuted claim | log(1+chi2(pi//pi0))=[R2 log p-1/2 log n]_+ +O_P(log log p) is false when 2Ar>1 | REFUTED (COUNTEREXAMPLE, O-WSTAB Theorem W(e)); SF verified for A in (1/(2r),1), scope of F-DRAFT hypotheses not verified (F8); XF A-REV9 verified W(e) | O-WSTAB/REPORT.md; O-WSTAB/review/CHECK_SEP_W.md; F-DRAFT/NEW_TARGETS.md | [pos 748] | replaced by TH362(e),(g) |
| RF253 | F-DRAFT Theorem W(b) divergent side; FD-W(b) | refuted claim | 1+chi2<=1+p^{R2+eps}/sqrt n+o(1) is false when 2Ar>1 | REFUTED (O-WSTAB: log(1+chi2) grows faster than any multiple of log p) | O-WSTAB/REPORT.md; F-DRAFT/NEW_TARGETS.md | [pos 748] | replaced by TH362(d)(e) |
| RF254 | F-DRAFT Lemma W2 exact identity with partial R^2; FD-W2 | refuted claim | LR_l=nu[log(1-x_{T,l})-log(1-x_{S°,l})] with x the ordinary RSS partial R^2 is false for the v3 score | ERROR (A-REV4); [PENDING] repair h_{T,l}; replaced by LM212, TH378 | A-REV4/REVIEW.md; A-REV4/DRAFTS_CHECK.md; F-DRAFT/NEW_TARGETS.md | [pos 807] [pos 919] | replaced by LM212 and TH378 |
| RF255 | F-DRAFT W″ O(1) stages; STG-cexW2 | refuted claim | A masked-regime crossing costs a bounded number of stages (about 3pi) whatever the odds gap | COUNTEREXAMPLE (O-STAGES; registry STG-cexW2: F-DRAFT O(1) stage count is false); XF A-REV9 VERIFIED logarithmic order of Theorem M | O-STAGES/REPORT.md; F-DRAFT/NEW_TARGETS.md | [pos 733] [pos 748] [pos 1028] | replaced by TH368, TH369 |
| RF256 | Draft section 5.3 premise for v3 tables; weak cross-block dependence bounds weight variance | refuted claim | Divergence controlled by cross-block covariance so importance-weight variance stays bounded | REFUTED for v3 tables: d=d_sigma>=0 under exact BO; chi2 can diverge at zero cross-block correlation (WS6(d)); F-DRAFT: false for v3 tables | F-DRAFT/CROSSWALK.md; O-WSTAB/PROOF.md; O-WSTAB/REPORT.md | [pos 616] [pos 748] | replaced by TH350, TH356, TH362 |
| RF257 | O-WSTAB first W(d) hypothesis p^r/sqrt n->0 for the upper half | refuted claim | If p^r/sqrt n->0 then chi2<=p^{r+eps}/sqrt n (first version) | GAP found by same-family review (CHECK_SEP_W F1); statement restricted to p^r sqrt(log p)/sqrt n->0; XF A-REV9 VERIFIED with the stronger premise | O-WSTAB/review/CHECK_SEP_W.md; O-WSTAB/REPORT.md | [pos 748] | replaced by restricted TH362(d); residual CJ266 |
| RF258 | Path length determines the number of ESS-0.9 stages | refuted claim | Stage count is proportional to thermodynamic length L (the 3pi heuristic) | REFUTED at production c=log(10/9): two-state family has L<=pi while T*->inf (O-STAGES); true only as c->0 (TH365) | O-STAGES/REPORT.md | [pos 733] [pos 748] | replaced by TH365 (c->0), TH368 |
| RF259 | T_n<=C1+C2 log(1/Delta_n) follows from the rules alone | refuted claim | Realised stage count bounded by log(1/Delta_n) from the calibration rules (task R5 intended route) | NOT PROVABLE as stated (API-T26BUD REPORT section 5); controlling quantity is eta_n | API-T26BUD/REPORT.md; campaign/tasks/API-T26BUD.md | [pos 906] [pos 978] | replaced by TH370, TH371, TH373, CJ268 |
| RF260 | Expectation route to Theorem W; E e^{(1+r)Z^2/2}<inf | refuted claim | A moment bound on sum_l c_l exists | REFUTED (expectation infinite); replaced by truncation HT (LM215) | O-WSTAB/REPORT.md; F-DRAFT/CROSSWALK.md | [pos 748] | replaced by LM215 |
| RF261 | Uniform lower bound of T* by path length without regularity | refuted claim | A uniform constant bounds T* below by the path length | REFUTED (family F″(u+x)=x^-a, a up to 2: ratio unbounded); needs kappa-regularity (Theorem L(ii)) | O-STAGES/REPORT.md | [pos 733] | replaced by TH365 |
| RF262 | task clause (a); start-only plus local search fails unless basin contains S~0 | refuted claim | Claim in W7-SEP task: Q iid draws + production local search (and LS0 alone) score S0 w.p. -> 0 for every polynomial budget unless basin contains S~0 | COUNTEREXAMPLE (by proof, Cor GU-LH; 386/386 replicates; SF: none; XF: GU VERIFIED* A-REV7); replaced by TH384, TH388, TH389 | campaign/tasks/W7-SEP.md; W7-SEP/PROOF.md; W7-SEP/REPORT.md | [pos 711] [pos 717] [pos 763] [pos 796] | M6 scope boundary (SEP-taska remains COUNTEREXAMPLE) |
| RF263 | super-polynomial start-only budget; every polynomial budget fails | refuted claim | Claim that start-only discovery needs a super-polynomial budget while v3 is polynomial | False in R1: Q*=p^c n^{c/2} polynomial since c<=s0 fixed; super-polynomial needs c_n -> infinity; replaced by TH380, TH386 | campaign/tasks/W7-SEP.md; W7-SEP/PROOF.md; W7-SEP/REPORT.md | [pos 717] [pos 763] | none |
| RF264 | tempering is needed; the sampler is needed for discovery in the masked regime | refuted claim | Spine claim: the tempering bridge/sampler is needed in the masked regime (That is exactly why the sampler exists) | REFUTED on LH by W7-SEP Prop GU (candidate-based); replaced by 'moving off the start is needed' (E-SPINE PR #1; T38 v3 Remark 6; decision D4) | E-SPINE/Docs/Theory/AMENDMENTS_20261102.md; E-SPINE/E-SPINE_vs_mergebase.diff; T38-RECORD/T38_STATEMENT.md; W7-SEP/REPORT.md | [pos 763] [pos 796] [pos 798] [pos 807] [pos 850] | T38 Thm 5 statement of record Remark 6 / Why it matters; M6 notes (no universal necessity of tempering) |
| RF265 | FD-NM; F-DRAFT Prop NM; F-DRAFT NM | refuted claim | F-DRAFT Proposition NM (naive merge fails, rigorous): general proxy-split family with O_P(1) log BF remainder, start mode, naive union and O(1) ideal grid stages | ERROR (A-REV4; scope GAP); F-DRAFT status PROVED modulo T03/EXP'/Cor. P1; repairs: A-DRAFT Prop M (CE208), NM-R (TH393, pending Claude); not applied to F-DRAFT text | F-DRAFT/NEW_TARGETS.md; A-REV4/REVIEW.md; A-REV4/DRAFTS_CHECK.md; A-REV6/WEIGHTS.md | [pos 563] [pos 616] [pos 677] [pos 796] [pos 807] [pos 919] [pos 957] | none (paper-1 list: Prop 0 proposal at pos 957 not retained; K98 dropped) |
| RF266 | K98; naive merge of block fits recovers the posterior (Prop M(b)) | refuted claim | Proposal claim that naively merging local inclusion probabilities of correlated predictors recovers the posterior | KNOWN-FALSE (SHARE-M(b) XF ERROR A-REV3/A-REV6; FD-NM XF ERROR A-REV4; ADRAFT-PropM COUNTEREXAMPLE); DROP | MEET-THM/R0_DIFF.md; MEET-THM/MINUTES.md; MEET-THM/FUTURE_WORK.md; T38-RECORD/REGISTRY_v2.md | [pos 1361] [pos 1626] | dropped (K98) |
| RF267 | K97 draft clause cov(x_t,y)=0 on isolation; B.D9(b) | refuted claim | Draft clause that isolation makes the observed response exactly orthogonal to the hub (exact orthogonal null column, cov(x_t,y)=0) | COUNTEREXAMPLE (W1 PC1; conceded R2); replaced by population cancellation x_t^T mu = 0 | MEET-THM/R1_B.md; MEET-THM/evidence/W1_PC1/VERDICTS.md | [pos 1608] | FW21 (K97) |
| RF268 | methods with guarantees are sequential; no analogue speed-up for MCMC; first parallel exact BVS; thesis premise "guarantees => sequential" | refuted claim | The sentence "methods that come with guarantees are sequential, and parallel-friendly methods with guarantees break under correlated designs" (HQ framing of Felipe's belief) and the wordings "no analogue speed-up in the context of Markov chains" and "first parallel exact BVS" must not be printed: the first half is FALSE in the work/depth sense (informed chain of Zhou-Yang-Vats-Roberts-Rosenthal 2022 with parallel neighbour scoring), the second half survives only in the three-part S-GAP form | REFUTED as a general statement (LIT-PAR §1 item 2: "FALSE in the work/depth sense. Do not print it."); replaced by CJ282 S-GAP (three-part form); THM-SYNTH REPORT §3.3 "Do not print"; counterexample candidate CE212 | LIT-PAR/REPORT.md §1, §3.3 item 5, §4.1 S-COUNTER; THM-SYNTH/REPORT.md §3.3; campaign/LEDGER.md (13:03 UTC 2026-11-03) | [pos 1030] [pos 1038] [pos 1070] [pos 1107] | Thesis CD (K96, remark only); M8 Proposition D remark |
| RF269 | depth = T stages; the only sequential part is the stage count; depth = stage count without the per-round factor | refuted claim | HQ framing: "Sequential depth: the only sequential part is the stage count, and O-STAGES already bounds it" i.e. depth = T; in score evaluations a round is p+B+2 sequential elementary steps per particle, so depth is T L (p+B+2), worse in p than a parallelised ZYVR chain; the only fix is a kernel change (informed or tempered-Gibbs moves scoring all p neighbours at once), rejected by METH-AUDIT as WORKHORSE | REFUTED / withdrawn (LIT-PAR §1 item 4 "Self-critique"; METH-AUDIT §7 "Depth = T stages without the round factor fails"); replaced by Prop D depth (I+2)(T+L+4)(p+B+2) at island level (TH399, M8); factor costs about 2-3 ms per round at p = 500 (METH-AUDIT §6) | LIT-PAR/REPORT.md §1 item 4, §3.3; METH-AUDIT/REPORT.md §1 item 4, §7; METH-AUDIT/PROOFS.md (Prop D remark) | [pos 1038] [pos 1070] [pos 1072] [pos 1107] | M8 Proposition D ((e) ceilings: Theta(p) slots per round) |
| RF270 | METH-AUDIT REPORT s1.2: "bitwise on the smoke problem and on 3/3 study designs (s6)"; headline overclaim | refuted claim | METH-AUDIT REPORT §1 item 2 states that the bitwise reproduction holds "on the smoke problem and on 3/3 study designs (§6)" and C8 cites "measured in §6 (R = 32 x 312)"; the worker exited while waiting on runs: only smoke + p0500_S1_r001 had completed, §6 was an unfilled placeholder and results/ was not committed to the branch | RETRACTED as written (LEDGER 16:50 UTC: "its 3/3 headline is an overclaim"; THM-SYNTH task file: "treat METH-AUDIT's 3/3 as 1/1 + smoke"; MEET-v31 R1_B: "METH-AUDIT 3/3 is not supported by committed files"); empirically re-established by HQ re-runs: S4_r001 (pos 1175) and S5_r002 (pos 1241) bitwise PASS, so the executed check is smoke + 3/3 (concurrency log); UNCERTAIN residue: REGISTRY_INDEX §5.B B1 and REGISTRY_PAPER1 still list "1/1 vs 3/3" as a source CONFLICT | METH-AUDIT/REPORT.md §1, §4 C8, §6; campaign/LEDGER.md; campaign/tasks/THM-SYNTH.md; MEET-v31/R1_B.md; MEET-v31/evidence/2026-11-03_concurrency_runs.md; MEET-THM/REGISTRY_PAPER1.md | [pos 1085] [pos 1103] [pos 1107] [pos 1175] [pos 1241] | S-OUT (K83): executed check wording |
| RF271 | depth free of N, H and R for v3.1 (Prop D clause; D1(c); D3(b)) | refuted claim | Prop D / Theorem D(c) / Theorem CD(b): "D does not depend on N, H or R" for the critical path with one worker per particle per island; false for v3.1 as implemented, whose particle rounds are serial within an island (depth N (T+L+4)(p+B+2) per island at tier e); particle-level parallelism needs per-particle random streams (C6), a LAW-PRESERVING change not bitwise-reproducible | STRUCK for v3.1 (MEET-v31 decision 6: "Depth and cost are stated at the implemented (island) level. Free of N, H, R is removed. Calibration is counted."; METHOD_v3.1_FINAL: "Depth free of N, H, R is not claimed for v3.1"); Felipe decided (2026-11-03) that paper 1 claims island-level depth only; C6 is implemented and law-checked iff paper 1 claims particle-parallel depth or demonstrates any fit with p > 2,500 (neither fires); the as-recorded METH-AUDIT statement itself is conditional on width R N so not false as a particle-parallel statement | METH-AUDIT/REPORT.md §1 item 4, §2.2, §7; THM-SYNTH/THEOREM_LIST.md (D1, D3); MEET-v31/MINUTES.md (decision 6, item 10); MEET-v31/METHOD_v3.1_FINAL.md (#19); MEET-THM/THEOREM_LIST_FINAL.md (Card Prop D) | [pos 1107] [pos 1177] [pos 1276] | M8 Proposition D (island-level restatement) |
| RF272 | post-search HPM monotone in the island count R prime without the extra local search; stacking never worsens the reported HPM | refuted claim | Reading of Cor W-R: since the pre-local-search scored set and HPM are nested in R prime, the reported (post-local-search) HPM is monotone in R prime; the deterministic implication "pre-search sets nested => post-search HPM monotone" is false | FALSE (PC1 claim 6, Claude Opus 5.5 same-family proof check for the MEET-v31 chair; COUNTEREXAMPLE CE220); METH-AUDIT PROOFS.md already carried the caveat; replaced by Cor W-R with the extra local search from c4 (TH396); no listed theorem uses post-search monotonicity | METH-AUDIT/PROOFS.md (Cor W-R caveat); MEET-v31/evidence/2026-11-03_PC1_proof_check.md (Claim 6); MEET-v31/MINUTES.md (decision 5) | [pos 1107] [pos 1242] | S-OUT (K84) |
| RF273 | more islands always helps; splitting the particle budget into R >> 4 smaller islands (C8) | refuted claim | "More islands always helps": false for the equal-weight (primary) PIP under a split of a fixed total, because its limit is the single-island mean E[PIPhat_1j/C] whose bias is set by N per island (Prop P(i)); Zhat is neutral to first order (Cor V) but the equal-weight PIP gets worse; measured at R = 32 x 312 the differences are small on three designs (max dPIP eq 1e-4, 2.3e-3, 5e-4; Zhat-weighted 2e-4, 2.0e-3, 7e-4) but the theorem gives no protection | REJECTED (METH-AUDIT §4 C8 WORKHORSE in effect, §7 "More islands always helps fails"); replaced by stacking R prime = 4k at fixed N_e (TH396, MEET-v31 item 5) and the Zhat-weighted primary PIP (MEET-v31 item 8) | METH-AUDIT/REPORT.md §1 item 3, §4 C4/C8, §7; METH-AUDIT/PROOFS.md (Prop P(i)); MEET-v31/evidence/2026-11-03_concurrency_runs.md | [pos 1107] [pos 1175] [pos 1241] | M1 Theorem V/H; S-POOL (K49, K59) |
| RF274 | rapid-mixing theorems (YWJ, ZYVR, Chang-Zhou) apply to / certify the paper target on LH (ledger gloss of API-POS headline 2) | refuted claim | Ledger gloss of API-POS: "Rapid-mixing theorems (YWJ, ZYVR) apply to LH"; HQ correction at pos 1009: "API-POS said the rapid-mixing theorems apply to the linked-hub family. LIT-MCMC finds they don't, at least for our own posterior": the unimodal-ratio hypothesis R > M fails for the paper target at n = 200 and 1,600 on LH (c = 1, 2) and in 12 of 12 study-like data sets by a factor of at least p^0.87; R > M^2 fails at every n tested up to 102,400 | QUALIFIED, UNCERTAIN: API-POS headline 2 itself says the theorems apply "with their own priors" to LH-iid and headline 3 that "for the paper's own target, neither theorem applies as stated"; LIT-MCMC refutes only a sufficient condition (R > M), not fast mixing; THM-INV D1 and THM-SYNTH REPORT §4.1: say both; replaced by Prop OB (TH401) and the positioning paragraph (TH404) | campaign/LEDGER.md (API-POS entry; "Correction"); API-POS/REPORT.md §1; LIT-MCMC/REPORT.md §0, §4; THM-INV/REPORT.md §2 D1 | [pos 978] [pos 1009] [pos 1107] | positioning paragraph next to M5; FUTURE_WORK FW4 |
| RF275 | LIT-VENUE s1.3: poly-time recovery on LH also follows from Chang-Zhou R > M "since on LH S0 is the unique local mode" | refuted claim | LIT-VENUE headline item 3: polynomial-time recovery of S0 on LH "also follows from Chang-Zhou's unimodality condition R > M, since on LH S0 is the unique local mode"; unimodality gives R > 1, not R > M, and R > M fails on LH at n = 200 and 1,600 | CONTRADICTED by LIT-MCMC exact enumeration (CE216) and THM-INV D1; "LIT-MCMC's computation contradicts this: unimodality (R > 1) does not give R > M" | LIT-VENUE/REPORT.md §1 item 3, §8; LIT-MCMC/results/rz_lh.md; THM-INV/REPORT.md §2 D1 | [pos 1009] [pos 1107] | none |
| RF276 | LIT-PAR G4 analytic sketch: Song-Liang loses the masked variable whenever the split separates the linked pair; SaM "Thm 5" label | refuted claim | LIT-PAR G4: SaM recovers S0 in 5/318 splits that separate the linked pair "(probability ~ 1/2 for two halves, -> (K-1)/K for K groups)" and the analytic sketch via "Song-Liang Thm 5" read from slides; corrections: the failure needs the masked hub to be isolated from its partner AND its own group (group members carry the marginal signal -rho psi beta, so Stage 1 retains the hub otherwise); LIT-PAR's 5/318 used a singleton masked variable (g = 1), where isolation = separation; the theorem reference should read Thm 4 / Cor 2 + eq. (19) + Condition 5 of the JRSS-B text | CORRECTED by THM-SYNTH REPORT §1.6(a) / Theorem SL(e) (checked numerically, scripts/check_lemmas.py; CE214) and THM-INV D10; replaced by Theorem SL (TH417, PROOF SKETCH); final: K97 -> FUTURE_WORK FW21 (null-exclusion/FDR step NOT REPAIRED, W2PC1) | LIT-PAR/REPORT.md §3.1 G4, §5 item 1; LIT-PAR/notes/09_sam_lh_counterexample.md; THM-SYNTH/REPORT.md §1 item 6; THM-INV/REPORT.md §2 D10 | [pos 1070] [pos 1107] [pos 1177] | FUTURE_WORK FW21 (K97) |
| RF277 | LIT-PAR notes 04: ZYVR Condition 1(b) likely fails on masked LH because true variables are marginally weak | refuted claim | Inference in LIT-PAR notes 04 that ZYVR Condition 1(b) "likely fails" on masked LH; superseded by API-POS: by exact enumeration (p = 16, 20) and Prop U (PROOF SKETCH) on LH the masking is a property of the start pi0 not of pi, every underfitted model has a strongly beneficial addition, c1 grows linearly in n (x8 per x8 in n) | SUPERSEDED (LIT-PAR REPORT §2.4 "Discrepancy to flag"); for the study scenarios S1-S6 whether Condition 1 holds is OPEN | LIT-PAR/REPORT.md §2.4; API-POS/REPORT.md §6; API-POS/results/cond1_lh.md | [pos 978] [pos 1070] | none |
| RF278 | N9: "a fixed order is not self-adjoint" and "the exact condition ... it fails if"; RB consequence without a stationary start | refuted claim | N9 REPORT row 6: "A fixed order is not self-adjoint"; PROOF §2 "The exact condition, and what would break it ... It fails if the order or the step counts depend on the state, or if the order law is not reversal-invariant"; REPORT §3: the state before each Gibbs step is pi-distributed and E[o_j] = pi(j in S) | AMENDED by CHK_INHERITED (cross-family, gpt-6.1-sol): the conditions are sufficient, not necessary ("is not guaranteed", commuting kernels can stay reversible under a fixed order; "A fixed order need not be self-adjoint"; CE218); the RB consequence must say the round starts in q_phi, invariance alone does not make finite terminal particles exactly stationary or plain normalised RB estimates unbiased; N9K registry status unchanged (PROVED (candidate)) | N9-KERNEL/REPORT.md §2 row 6, §3; N9-KERNEL/PROOF.md §2; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 (Required amendments) | [pos 1593] [pos 1626] | S-KERNEL (K21, K20) |
| RF279 | F-REFINE: Theorem W (region form R_{a,d}) covers the masked families / is the general sufficient condition for (M2) | refuted claim | F-REFINE ARCHITECTURE/CARDS describe Theorem W (W3-PGD) as the general sufficient condition for (M2) / for TD-prime | FALSE on LH with c >= 2: exact tie, PGD(eta) fails for every eta > 0 (VPGD-PropT, W5-VPGD) [T38-RECORD registry D, C15]; replaced by Theorem W_Lat (lattice form, VPGD-WLat) and Prop LH-PGD; owner theme 4 (REPAIR-GREEDY) | T38-RECORD/REGISTRY_v2.md (A2 C15; D retired statements); F-REFINE/ARCHITECTURE.md; F-REFINE/CARDS.md (Card 4) | [pos 463] [pos 957] | none (campaign-only); see theme 4 for Theorem W_Lat |
| RF280 | F-REFINE: without LS0 the paper has no masked-regime consistency theorem | refuted claim | F-REFINE ARCHITECTURE §4: "So without LS0 the paper has no masked-regime consistency theorem whose premises are all proved on an explicit family" (also W4-T38FULL II.9, W6-FIXREV1 "Not claimed") | SUPERSEDED: no-LS0 candidates on LH now exist (W5-B2ENV, W5-VMASK R1, O-BGIBBS BG3, F-SHARE F1/F2, W7-SEP); registry: "candidates on LH, pending cross-family review (A-REV7)"; A-REV7 VERIFIED B2-LH under STAB-LH; F-REFINE amended in place by E-SPINE (2026-11-02) | F-REFINE/ARCHITECTURE.md §4 (amendment note); T38-RECORD/REGISTRY_v2.md (D retired statements) | [pos 463] [pos 850] [pos 957] | M5 Theorem HPM ((b2-LH) variant K70) |
| RF281 | LIT-STAT first draft: no published BB(1,p)/g = n tail bound, hence a new mechanism; "<= 1/2 for every i >= 0" | refuted claim | First-draft LIT-STAT headline 4 treated the exact BB(1,p) tail (T02(i sharp)) as the most distinctive statistical piece with BB(1,p) a different mechanism from BB(1,1); and a first-draft line "<= 1/2 for every i >= 0" for the factors of C(p,k)/C(2p-1,k) | NARROWED/CORRECTED in the same report (§12 addendum): per model BB(1,p) and BB(1,1) penalise each added variable at the same order (LM228), so the gap is narrow (Rossell's analysis does not reach a cap K ~ n); the i = 0 factor is p/(2p-1) = (1/2)(2p/(2p-1)) > 1/2; novelty verdict "modest" (CJ293) | LIT-STAT/REPORT.md §1 item 4, §12 | [pos 1009] | none |
| RF282 | THM-SYNTH A1(v) / THM-INV: R_n >~ 1/P(crossing) as a consequence of F-MASKPIP M3 | refuted claim | Use of F-MASKPIP Proposition M3 (no conditional evidence theorem from first moments) to justify that the island count R_n must exceed the reciprocal crossing probability | M3 recorded XF ERROR (A-REV9, probability-one counterexample); THM-SYNTH REPORT §1.6(b): the remark "must not cite it", replaced by Cauchy-Schwarz + M2: E[W^2/C] >= (E[W 1_cross/C])^2/P_C(cross) (PROOF SKETCH, A1(v)); owner of M3 is theme 8 | THM-SYNTH/REPORT.md §1 item 6(b); THM-SYNTH/THEOREM_LIST.md (A1(v)); T38-RECORD/REGISTRY_v2.md (FMP-M3) | [pos 1177] | M1 Theorem V/H (growth-rate clause) |
| RF283 | 87 declarations; W8-SYNTH Lean count | refuted claim | W8-SYNTH SYNTHESIS section 7 stated 87 declarations, 87 proved, 0 sorry for L-LEAN head d9c2f2c | superseded by 101 declarations (DECL_STATUS.md; REGISTRY_v2 section G); stale snapshot, attribution of the 14 added theorems UNCERTAIN | W8-SYNTH/SYNTHESIS.md; W8-SYNTH/BRIEF.md; THM-INV/digests/REG.md; L-LEAN/DECL_STATUS.md | [pos 763] [pos 796] | none |
| RF284 | Astra did not finish; cross-family Lean fidelity incomplete | refuted claim | W8-SYNTH section 7: ASTRA_raw.md empty, run did not finish, cross-family fidelity incomplete | superseded: Astra round 1 completed (RED on T37 coverage), round 2 OVERALL (T37) GREEN | W8-SYNTH/SYNTHESIS.md; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md; T38-RECORD/REGISTRY_v2.md (section G) | [pos 763] [pos 796] | none |
| RF285 | Lean theoremA2 / theoremA2_lattice as the full A2 | refuted claim | Packet-1 A2 statements lacked the exact move count tau + sigma = m + e and the lower bound max(m,e) <= tau | repaired by TH451 (Astra r1 objection 1 RESOLVED in r2) | L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | n/a | none |
| RF286 | move-count identity documented as not formalised | refuted claim | W8-SYNTH section 7 and ADVISER_DECISIONS Fable remark 4: tau = m + e - sigma listed as not formalised | superseded: formalised as TH451, LM244, LM245 | W8-SYNTH/SYNTHESIS.md; L-LEAN/ADVISER_DECISIONS.md; L-LEAN/SmcBvs/SmcBvs/T37Greedy.lean (header) | [pos 796] | none |
| RF287 | exists_bestImprovement docstring overclaim | refuted claim | Docstring said an injective tie rank was supplied; theorem takes no rank | docstring reworded (ADVISER_DECISIONS 2); statement unchanged | L-LEAN/fidelity/FABLE.md; L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/ADVISER_DECISIONS.md | n/a | none |
| RF288 | Lean theoremA3 as giving the reported HPM after certified repair | refuted claim | Packet-1 A3 statements omit the pre-search ledger and reported maximiser; abstract instance with a higher previously scored model | repaired by TH445 and TH447 (Astra r1 objection 2 RESOLVED in r2); see CE221 | L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md; L-LEAN/fidelity/FABLE.md (remark 1) | n/a | none |
| RF289 | Lean theoremA3 under full TDP as Lemma 0(c) | refuted claim | Lemma 0(c) needs only 'reaches S0 and stops certified'; packet-1 theoremA3 assumed full TDP, cap l >= Phi and TD'_P on all Rad | repaired by TH446, TH447, TH453, TH454 (Astra r1 objection 3 RESOLVED in r2) | L-LEAN/fidelity/ASTRA_round1.md; L-LEAN/fidelity/ASTRA_round2.md | n/a | none |

## Counterexamples

| ID | native name(s) | kind | description | final status | authoritative file | positions | feeds |
|---|---|---|---|---|---|---|---|
| CE101 | J3; T20(v) counterexample; correlation 0.65; proxy local maximum | counterexample | n = 128, correlations 0.65, S0 = {1,2}: a proxy wins the first improvement and the local search certifies a wrong local maximum | named counterexample 'J3' of the architecture-run judge; full construction (file judge/sol2/...) not in the archive. the construction itself is recorded only under the code name given (council/judge Sol-check files, e.g. judge/sol2/J4_REPAIR_BASIN.md, are NOT in the archive snapshots): UNCERTAIN beyond the one-line description. | main@c4ef0dc/Docs/Theory/DROPPED.md; main@c4ef0dc/Docs/Theory/theorems/T20_T15_local_search.md | pre-campaign; [pos 114] | none (counterexample) |
| CE102 | J4; Sol check J4; internal change probability 1.0 while xi = 0.29 | counterexample | Enumerated component (n = 8, p = 4, d = 1): internal non-Gibbs changes occur with probability 1.0 while the exit bound xi = 0.29 | provisional numerical evidence (Sol check J4). Files judge/sol2/J4_REPAIR_BASIN.md and J12_TWO_CANCELLATIONS.md (named in the theorem file) are not in the archive. | main@c4ef0dc/Docs/Theory/theorems/T24_T18p_terminal_repair.md; main@c4ef0dc/Docs/Theory/DROPPED.md | [pos 119] | none (counterexample) |
| CE103 | D18; D2; TD data audit; 0 of 95; 541 fits | counterexample | d = 0 audit on the p >> n fits (n = 200): TD held strictly in 0 of 95 sampled cases (partial sample of 196); S0 a strict local maximum in about half; in 541 fits the search centre was in R_2 but not S0 and never returned S0 | DATA (preliminary, unreviewed at 2026-11-02): later confirmed by S-ELS (0 moves in 2,394/2,394 completed fits; all 541 'unrepaired' centres forced by Lemma 0) - see REGISTRY_v2 D2 ELS-1..ELS-3 | main@c4ef0dc/Docs/THEORY_PRIORITIES.md | [pos 150]; [pos 178] | none (counterexample) |
| CE104 | J10; two-state system; RET+OCC | counterexample | J10 counterexample in an abstract two-state system showing RET+OCC cannot give the evidence-variance rate without particle-history control | named counterexample; construction not in the archive. the construction itself is recorded only under the code name given (council/judge Sol-check files, e.g. judge/sol2/J4_REPAIR_BASIN.md, are NOT in the archive snapshots): UNCERTAIN beyond the one-line description. | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114] | none (counterexample) |
| CE105 | J7; factor-n error | counterexample | J7: for all polynomial p the T14-H one-move-addition iid-cheap clause has a factor-n error; initial-base cancellation products lack normalisation / sequential conditioning | named counterexample / error 'J7'; construction not in the archive. the construction itself is recorded only under the code name given (council/judge Sol-check files, e.g. judge/sol2/J4_REPAIR_BASIN.md, are NOT in the archive snapshots): UNCERTAIN beyond the one-line description. | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114] | none (counterexample) |
| CE106 | J9; duplicated predictors across blocks; exact branch | counterexample | J9: duplicated predictors across blocks accumulate gains (so gap-only STIFF and the discrepancy range bound fail); and p_max cannot be universal because the exact branch precedes Gram construction | named counterexample 'J9'; construction not in the archive. the construction itself is recorded only under the code name given (council/judge Sol-check files, e.g. judge/sol2/J4_REPAIR_BASIN.md, are NOT in the archive snapshots): UNCERTAIN beyond the one-line description. | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114] | none (counterexample) |
| CE107 | P8; usable upper bounds | counterexample | P8: the T22(iv) existence claim for usable upper bounds is false as stated | named counterexample 'P8'; whether it is the legacy Example 2.3a is not stated in the sources. | main@c4ef0dc/Docs/Theory/DROPPED.md; main@c4ef0dc/Docs/Theory/legacy_pre_v3/elementary_III/PROOF.md | pre-campaign; [pos 114] | none (counterexample) |
| CE108 | T11(ii) a = 1 counterexample | counterexample | review-group counterexample showing the claim 'no ordering constant for a = 1' is false | named only as '(counterexample)'; construction not in the archive. the construction itself is recorded only under the code name given (council/judge Sol-check files, e.g. judge/sol2/J4_REPAIR_BASIN.md, are NOT in the archive snapshots): UNCERTAIN beyond the one-line description. | main@c4ef0dc/Docs/Theory/DROPPED.md | pre-campaign; [pos 114] | none (counterexample) |
| CE109 | T01 (T)(b1); same-rate bounds do not transfer; r1 < r2 witnesses | counterexample | p = 1 inputs with Pi_{r1}({S={1}}) -> 1 and Pi_{r2}({S={1}}) -> 0 for fixed rates r1 < r2 (s_y^2 -> 0, outside the scale event) | PROVED-LOCKED inside T01 (wave 3: statement checker approved R2; two Opus xhigh reviewers verified; external review queued) | main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/STATEMENT.md | [pos 119]; [pos 156]; [pos 178] | none (counterexample) |
| CE110 | T01 (T)(b2); witnesses in B_n; b-, b+ | counterexample | p = 2 inputs with s_y^2 = s^2 in (sigma*^2/2, 2(sigma*^2+M)+1) for every n >= 4 such that Pi_{b-}(E) -> 0 while Pi(E/y) -> 1 (E = {S={1}}), and Pi_{b+}(E') -> 0 while Pi(E'/y) -> 1 (E' = {S={1,2}}) | PROVED-LOCKED inside T01 (wave 3, as TH101) | main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/STATEMENT.md | [pos 119]; [pos 156]; [pos 178] | none (counterexample) |
| CE111 | Prop D; Proposition D; PropD-T03; duplicated columns counterexample | counterexample | n>=3, p>=2 (e.g. p=n), X^r=[x,...,x] with p identical columns, beta*=(beta1,0,...,0) fixed beta1 != 0: G and R hold (s0=1) but on E_n (P0(E_n)->1) Pi(/S/>m/y) >= 2^(-(m+4)) exp{-m(m-1)/(4(p-m))} for 0<=m<=K-1, so any cutoff needs m_n >= (1/2)log2 n - O(1). | COUNTEREXAMPLE (reproducible) (W1-T03R); SF VERIFIED (W2-VT03R row 11; constants re-derived, 0.25157 >= 1/4); XF VERIFIED (A-REV2: G and R only, violates even size-two SE) | W1-T03R/PROOF.md; W1-T03R/REPORT.md; W2-VT03R/REPORT.md; A-REV2/REVIEW.md | [pos 296]; [pos 342]; [pos 370]; [pos 570] | feeds S-LIM (limitations as theorems, K100 duplicates clause) as related PropD-T03; scope sentence in S-T |
| CE112 | A-REV4 B5 counterexample: scored set {S1} with F(S0)=1, F(S1)=0 | counterexample | Let F(S0)=1, F(S1)=0 and scored set {S1}: a completed search reports S1 although S0 is the global maximiser; completion does not imply a posterior miss. | COUNTEREXAMPLE (analytic; XF: A-REV4 BOOK_CHECK ERROR B5; A-REV6 retains) | A-REV4/BOOK_CHECK.md; A-REV4/REVIEW.md | [pos 807] | refutes RF125 |
| CE113 | T05 amplitude-versus-energy computation at p = n^a (T05-wording) | counterexample | At p=n^a: tau_n ~ (1+2a)log n and the oracle threshold 2a log n, so the amplitude gap is [sqrt(1+2a)-sqrt(2a)] sqrt(log n) (additive) and the energy ratio is the constant (1+2a)/(2a). Example a=1/2, lambda=0.7 tau_n: oracle success 0.61->0.74, HPM 0.080->0.020 as n goes 10^3 -> 10^9; amplitude gap 0.61 -> 1.05. | COUNTEREXAMPLE to the multiplicative wording (W7-SEC; own check; registry T05-wording); XF none | W7-SEC/REPORT.md; W7-SEC/PROOF_T05.md | [pos 751] | refutes RF127 |
| CE114 | Numerical refutation of the 1.2e5 onset: q_n at n=130,328 | counterexample | With s0=14, p=round(n^A), 1/g0->0 and exact m#: at n=130,328 the geometric-series quantity q_n is about 5.53e22 (A=log500/log200) and 7.86e28 (A=log1000/log200), not <= 1/2; first n with q_n <= 1/2 is 2,116,048 / 2,457,025. | NUMERICAL (SF: W2-VT03R proof_thresholds.py; W6-FIXREV2 t03_thresholds.py agrees to the integer; XF: A-REV2 stable-product recomputation and A-REV5 Owls point checks) | W2-VT03R/REPORT.md; W6-FIXREV2/STATEMENTS.md; A-REV2/REVIEW.md; A-REV5/REVIEW.md | [pos 370]; [pos 570] | refutes RF123 |
| CE115 | A-REV5 point check at n=2,116,048: exp(2 eps_n) = 4639.924697 > 4 | counterexample | At n=2,116,048 the independent calculation gives q=0.499999989 but exp(2 eps_n)=4639.924697 > 4; the fixed-constant condition exp(2 eps_n) <= 4 first holds at 25,571,897 (29,755,302 for p=n^1.30). | NUMERICAL (XF: A-REV5 Owls point checks; not a proof that no earlier nonmonotone crossing exists) | A-REV5/REVIEW.md | [pos 807] | refutes RF124 |
| CE116 | LH /psi/>rho; PART-CE3; psi=0.71, 0.75, 0.8; hub pair co-clusters; psi-rho cliff | counterexample | LH with /psi/ > rho: hub pair has /r_hat_ab/ -> /psi/ > max(f_a,f_b), (C*) fails at the leaf pair, partition != groups (failure 80-83% at psi=0.75, n=200; 23-26% at psi=rho) | COUNTEREXAMPLE (mechanism PROVED; blocks != groups by simulation) (W7-PART CE3; W3-VEXP row 17; W5-VMASK 5.5) | W3-VEXP/REPORT.md; W7-PART/PROOF.md; W5-VMASK/REPORT.md | [pos 363] [pos 742] [pos 796] | feeds: none |
| CE117 | PART-CE1; W7 CE1; g > B (g=15,16 at n=200, B=14) | counterexample | If some group has g_h > B the cut always splits it, so blocks != groups with probability 1; g=15,16 at n=200: 50/50 replicates per cell | COUNTEREXAMPLE (deterministic) (W7-PART) | W7-PART/PROOF.md; W7-PART/REPORT.md | [pos 717] [pos 796] | feeds: none |
| CE118 | PART-CE2; W7 CE2; 2g<=B study groups of 5 | counterexample | Equal groups with 2g <= B (g=5, B=14): next-fit packs >= 2 groups per bin so blocks != groups surely, though blocks are unions of whole groups (200/200) | COUNTEREXAMPLE (deterministic for equal sizes) (W7-PART); XF ERROR only on the unequal-size header | W7-PART/PROOF.md; W3-PXN/PROOF.md | [pos 717] [pos 796] [pos 919] | S-BLOCKS (K07) cites PART-CE2 |
| CE119 | A-REV6 counterexample to CE2 header; sizes 2 and 5 with B=5 | counterexample | Two groups of sizes 2 and 5 with B=5: 2 g_min = 4 <= B yet under separation the cut retains them individually and next-fit cannot combine them | referee counterexample (A-REV6) | A-REV6/PARTITION.md; A-REV6/REVIEW.md | [pos 796] [pos 919] | feeds: none |
| CE120 | A-REV2 counterexample to 'iff'; CL(sqrt(log n)) with eta=1 on exact-zero-leakage LH | counterexample | Any exact-zero-leakage masked LH sequence satisfies CL(sqrt(log n)) with eta=1 as well as CL(0), yet the fixed-CL theorem gives vanishing start mass, so a loose eta cannot determine a necessary threshold | referee counterexample (A-REV2 5.3) | A-REV2/REVIEW.md | [pos 568] [pos 570] | feeds: none |
| CE121 | n=200 dilution numbers vs CL(0) prediction; study-design numerical counterexample | counterexample | gen_dev_data.R in numpy: n=200, s0=14, groups of 5, beta (1.4,-1.0,1.8,-1.2,0.8,-1.6)×scale in {1,0.5}, S1/S3/S4/S6, p in {500,1000}: masked truths L^2 = 50-199, observed log10 pi_0 (S0)/pi_0 (tilde S0) -11..-17 vs CL(0) prediction -29..-46 | numerical (W3-PXN sec 5; W3-VEXP sec D); not a proof | W3-PXN/REPORT.md; W3-VEXP/REPAIRS.md | [pos 363] [pos 423] | feeds: none (Theme 3) |
| CE122 | heterogeneous LH pairs; m0 below true margin; margins_grid | counterexample | Random heterogeneous pairs (psi up to 0.95, beta in [0.3, 2.5]): m0 strictly below the Phi>=2 margin in 32/94 settings, down to a factor 0.002 (worst-case parameters not in snapshot) | brute force (W5-VMASK R5) | W5-VMASK/REPAIRS.md; W5-VMASK/REPORT.md | [pos 742] | feeds: none |
| CE123 | DM(i) size-sign counterexample | counterexample | p=2, K=s0=1, singleton table BFs=1, t=1: P_t(N<=K)=3/4, A=4/5, log(5/4)<log(4/3) | explicit construction (A-REV9) | A-REV9/REVIEW.md | [pos 821] | see RF149 |
| CE124 | IID500 cell, oracle sigma^2 common-sigma-hat^2 start; 10^-1303 | counterexample | (n,p,s0)=(200,500,14), c=1: v3 log10 pi0(S0)=-12.35 (mode size 5); oracle common sigma-hat^2 -1302.69 (mode at cap K=100); BO196: -7.47 to -0.52 | exact numerics (F-SIGMA, 2 replicates per cell); S6 PROVED mechanism | F-SIGMA/REPORT.md §1,§7,§8 | [pos 763] | see RF150 |
| CE125 | Two-variable block violating the N1 bound | counterexample | exact two-variable count (t r1+t r2+2t^2 r12)/(1+t r1+t r2+t^2 r12) near 2 while t(r1+r2) small; orthogonal columns with fit fraction x<1/2, r12/r1^2=[(1-x)^2/(1-2x)]^nu | explicit analytic construction (A-REV9) | A-REV9/REVIEW.md | [pos 821] | see RF152 |
| CE126 | Prop S non-injective replacement assignments | counterexample | two replaceable truths, three eligible null blocks: claimed (1+3)(1+2)=12 supports, only 1+6+3=10 distinct | explicit (A-REV9); counterexample to injectivity not to the final inequality | A-REV9/REVIEW.md | [pos 821] | see RF154 |
| CE127 | Two correlated Gaussian nulls against Lemma N parenthetical | counterexample | two correlated nulls independent of truths and response: conditional on the other null the first has nonzero conditional mean | explicit (A-REV9) | A-REV9/REVIEW.md | [pos 821] | see RF153 |
| CE128 | C-E1 screening plug-in underestimate | counterexample | pooled residual variance from top-20 marginal screening at p>>n gives a=2-3 > a*=1.43 even under BO; IID500 sigma-hat^2=0.114 vs sigma^2=0.038; BO196 a=1.15 | PROVED by S2(iv) (F-SIGMA) | F-SIGMA/REPORT.md §7 | [pos 763] | feeds: none (campaign-only) |
| CE129 | C-E3 non-BO leakage (S5 common-factor family) | counterexample | delta^2_{empty,l} ~ n for nulls in 98/100 blocks: common-sigma-hat^2 exponent exceeds v3's by v_T/sigma-hat^2 ~ 1/(1-R^2), start hits K | PROOF SKETCH (F-SIGMA) | F-SIGMA/REPORT.md §7 | [pos 763] | feeds: none (campaign-only) |
| CE130 | C-E4 runaway of the iterative plug-in (C-fix) | counterexample | second fixed point at /mode/=K; IID500 c=1: sigma-hat^2 0.50 -> 0.0207 (a=1.85) in 4 steps, /S_fix/=100; BO196 converges to S0 in 2 steps | COUNTEREXAMPLE (exact numerics) + PROOF SKETCH (F-SIGMA) | F-SIGMA/REPORT.md §7 | [pos 763] | see RF159 |
| CE131 | Data against weak-signal masking: L^2 ~ 50-199 and CL(0) overshoot | counterexample | masked truths have L^2=delta_pop^2/sigma^2 ~ 50 (c=0.5) to 199 (c=1); CL(0) prediction -29..-46 overshoots observed -11..-17 by 17-29 orders; V0 3.2-4.4 vs threshold 7.0-7.6; predicted masked 7.0-10.0 vs observed 6.3-9.0 | exact computations (W3-PXN, W3-VEXP) | W3-PXN/REPORT.md; W3-VEXP/REPORT.md; W3-VEXP/REPAIRS.md §D | [pos 361] [pos 370] | see RF151 |
| CE132 | Flooding of common-sigma^2 variants on the 2,400 real PROD-H fits (data) | counterexample | median log10 pi0(S0): v3 -15.65, C-fix -887.91 (2113/2400 at cap K), oracle -710.15, sigma_tilde_S0 -737.05, sigma_tilde_mode -18.59 (pi0(R2)=4.6e-6), s_y^2 -16.12; 0/2400 favourable for every feasible plug-in | data (API-RESID Step 0; reproduces study start law to 1.6e-12) | API-RESID/REPORT.md §2; API-RESID/results/tables.md; API-RESID/results/extra_tables.md | [pos 973] [pos 1009] | see RF150 |
| CE133 | CEX-1; CEX1; suppressor pair | counterexample | n=100, corr(x1,x2)=.95, mu=3x1-2.8x2, 10 orthogonal nulls: literal TD(0,0) strict holds yet best gain at empty -2.2977998984, search certifies empty | COUNTEREXAMPLE; SF VERIFIED (W3-VT37R); XF VERIFIED (A-REV2) | W3-VT37R/REPAIRS.md; W3-VT37R/REPORT.md; A-REV2/REVIEW.md | [pos 370] | K66 DROP |
| CE134 | Exp 3; C3-PGD; combination look-alike | counterexample | x3=0.85(x1+x2)/sqrt2+sqrt(1-.85^2)z: SE holds (lambda_min .15) but first greedy move is add x3 in 200/200 at n=3000; TD'_inf holds, TD'_P fails | COUNTEREXAMPLE; SF VERIFIED (W3-VT37R); XF VERIFIED (A-REV2) | W1-T37R/REPORT.md; W3-VT37R/REPORT.md; A-REV2/REVIEW.md | [pos 355] [pos 370] | K66 DROP |
| CE135 | CEX-2; CEX2 | counterexample | S_c=S0-x2+x3 with F(S_c)=F(S0)-2.29 climbs to S0+x3 (+7.21 above S0): posterior miss with E_LS true | COUNTEREXAMPLE; SF VERIFIED (W3-VT37R); XF VERIFIED (A-REV2) | W3-VT37R/REPAIRS.md; W3-VT37R/REPORT.md | [pos 370] [pos 570] | registry CEX2 XF-VERIFIED |
| CE136 | TIE; duplicate columns x1=x2 | counterexample | n=100,p=2,x1=x2,S0={1}: TD'_P(R0) holds but D_empty fails (exact tie), gains 7.6308489425 and -0.0018640607 | VERIFIED (A-REV2; reproduced by W6-FIXREV2) | A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md | [pos 570] [pos 742] | none |
| CE137 | PHI-REACH; neutral move paid back by two-unit swap | counterexample | S0={2,6,13}, centre {5,6,12}: path {5,6,12}->{2,5,12}->{2,5,13}->{2,6,13} in 3 moves<=Phi=4 with first move neutral; 23/360 designs | VERIFIED (XF A-REV2 retains V37 R3) | W3-VT37R/REPAIRS.md; W6-FIXREV2/STATEMENTS.md | [pos 370] [pos 570] | none |
| CE138 | C-LD; Prop C-LD; equicorrelated nulls | counterexample | s0=1, nulls sqrt r f+sqrt(1-r)g_i, r>1/2, p=n-2: all hypotheses and PGD(1) hold yet TD'_P(R_{0,2}) fails w.p.->1 | COUNTEREXAMPLE; SF VERIFIED* (W5-VPGD, A=1; p~n^A sentence sketch) | W3-PGD/PROOF.md; W5-VPGD/REFEREE.md | [pos 370] [pos 550] | none |
| CE139 | Prop G; VPGD-PropG; grouped equicorrelated nulls | counterexample | A=1, s0=1, N^{1-beta} groups of size N^beta with within correlation r>1/3: TD'_P(R_{0,2}) fails w.p.->1 although PGD(1), GERC hold | COUNTEREXAMPLE (d=2 proved; d>=3 PROOF SKETCH); SF authored by W5-VPGD | W5-VPGD/STAR.md; W5-VPGD/REPORT.md | [pos 550] [pos 742] | none |
| CE140 | cap witness n=8 p=7 K=4 | counterexample | Orthogonal G=7I, S0={1,2,3,4}, y=(x1+..+x4)/2, a=d=1: TD-P holds on 17 feasible states yet Lat({1,2,3,5}) contains infeasible {1,2,3,4,5} | VERIFIED (A-REV5, independent Owls enumeration) | A-REV5/REVIEW.md | [pos 919] | none |
| CE141 | LH exact tie; Prop T instance | counterexample | LH with c>=2 linked pairs: at S0 minus {a1,a2} swap b2->a1 ties add a1; PGD eta=0 in 20/20, D_S fails in 200/200 fits at n=200,2000,20000 | numerical (W5-VPGD scripts lh_pgd.py, lh_tie.py) | W5-VPGD/REPAIRS.md; W5-VPGD/REPORT.md | [pos 550] [pos 742] | none |
| CE142 | C2N; noise-bound counterexamples | counterexample | Orthogonal design theta=(1,1,0.1): //(P_S'-P_S'')mu//^2=2.01(n-1) vs 0.01 (ratio 201); theta=(3,0.2): ratio up to 1,896 in 400 designs | VERIFIED (SF W3-VT37R) | W3-VT37R/REPAIRS.md; W3-VT37R/REPORT.md | [pos 370] | none |
| CE143 | VAR; CEX-localmax(A2); hub variant | counterexample | p=20,B=4 two groups within corr .99 hub cross .95, signal 3x1-2.8x5: every table model below empty, start mode empty, search certifies empty while two-hub truth is higher (F gap 19.92) | COUNTEREXAMPLE (XF A-REV2; reproduced by W6-FIXREV2) | A-REV2/REVIEW.md; W6-FIXREV2/STATEMENTS.md | [pos 570] [pos 742] | K66 DROP |
| CE144 | CE1; CE-H24; H24 exit counterexample | counterexample | At boundary state (S0 minus j) union P a look-alike exits with prob >= (1-o(1))/(B+d+4); MC exit 0.62-0.98 in S2-S6 at n=200, exact lower bound >=0.39 | COUNTEREXAMPLE (numerical, reproducible; asymptotic PROOF SKETCH); SF CONFIRMED (W2-VT24G, wording GAP); XF VERIFIED* finite obstruction (A-REV1) | W1-T24G/PROOF.md; W1-T24G/REPORT.md; W2-VT24G/REPORT.md; A-REV1/REVIEW.md | [pos 296] [pos 370] | feeds: none (campaign-only) |
| CE145 | CE1-narrow; AREV1-CE1-seq; W6F1-CE1'; explicit sequence p=ceil(n^{1/3}) | counterexample | Exact-Gram sequence, one truth, one proxy at correlation r, p_n=ceil(n^{1/3}): (L+4)eta_n -> infinity for every fixed d | COUNTEREXAMPLE (PROVED from Lemma E and Lemma U(C5), W6-FIXREV1); referee-authored in A-REV1; XF VERIFIED as stated candidate (A-REV5); not universal | A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md; A-REV5/REVIEW.md | [pos 470] [pos 742] [pos 919] | feeds: none (campaign-only) |
| CE146 | CE2; chain on {2,1,0} | counterexample | Chain moving down by one w.p. c' per round: at H=2, P(not at 0)=1-c'^2 > 1-c'; form invalid in 395 of 1050 exact cases | COUNTEREXAMPLE; SF CONFIRMED (exact rationals) | W1-T24G/PROOF.md; W2-VT24G/REPORT.md | [pos 296] [pos 370] | feeds: none (campaign-only) |
| CE147 | Prop. U (U-a) counterexample | counterexample | S0={1,2}, x=empty, A=empty: independence jump {1}->{2} removes a truth with V unchanged (probability 0.826 on W6 config 1b) | reproduced (W6-FIXREV1); A-REV1 construction; VERIFIED by A-REV5 | A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 742] | feeds: none (campaign-only) |
| CE148 | Prop. U (U-b) counterexample | counterexample | S0={1}, x=empty, A={2}, junk 3: swap 2->3 keeps V but leaves the phase-1 family (probability 0.091) | reproduced (W6-FIXREV1); A-REV1 construction | A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 742] | feeds: none (campaign-only) |
| CE149 | Lemma S positivity counterexample | counterexample | e=0.9, f=1/20: the two-level low weight is -0.4529663145 (bound -0.0226483157); positive iff f>1-e | A-REV1; reproduced (W6-FIXREV1) | A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 742] | feeds: none (campaign-only) |
| CE150 | E3(ii) counterexample | counterexample | n=20, p=2, orthogonal columns, y=x2, reference {1}: formula (1-q)^2/(1+e) = 1.983334052945e23 vs pi0({1}) = 9.441607620478e-14; start mode {2} | A-REV1; reproduced to all printed digits (W6-FIXREV1) | A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 742] | feeds: none (campaign-only) |
| CE151 | EQ; equicorrelated nulls counterexample | counterexample | Equicorrelated nulls (r=0.8, p=n^0.9): Lambda_2(1) >= 1-o_P(1) and eps_del(2)->1 although G,R,SE,BM-inf hold | COUNTEREXAMPLE (asymptotic; PROVED modulo extreme-value facts; numerics) | W2-PREM/PROOF.md; W2-PREM/REPORT.md | [pos 424] | feeds: none (campaign-only) |
| CE152 | TS cancellation pair; TS counterexample | counterexample | Truths 1,2 with corr r, theta1=1, theta2=-1/r: gamma_1({1})=0 so G1 deletes truth 1 w.p. -> 1 | COUNTEREXAMPLE (PROVED computation; numerics 0.996 -> 0.99993) | W2-PREM/PROOF.md | [pos 424] | feeds: none (campaign-only) |
| CE153 | FamilyDefect on LH; family defect counterexample | counterexample | On LH under the symmetric-union neighbour graph useless group-mates are look-alikes; uniform-swap bad probability 0.088 at W*, U part of eta1 0.43 does not decay | COUNTEREXAMPLE (numerical, reproducible; asymptotic PROOF SKETCH) | W2-PREM/PROOF.md; W2-PREM/results/lh_table.md | [pos 424] | feeds: none (campaign-only) |
| CE154 | quantifier array counterexample; sup-of-sum vs sum-of-sups | counterexample | a_l(W_j)=1/p for l=j else 0: sup_W sum_l = 1/p but sum_l sup_W = 1 | abstract counterexample (A-REV1; not a BVS instance) | A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 742] | feeds: none (campaign-only) |
| CE155 | C3-low counterexample | counterexample | n=1e6, p=2, S0={1}, mu=x1, T=empty, l=2, Z^2=65: actual log BF + .5 log(n+1) = 16.2502645682 < claimed bound 19.5571554183 | A-REV2; reproduced (A-REV5) | A-REV2/REVIEW.md; A-REV5/REV2_CHECK.md | [pos 570] | feeds: none (campaign-only) |
| CE156 | conditioning on completion counterexample; fair bits conditioned equal | counterexample | Independent fair bits conditioned equal: P(00/equal)=1/2 vs product of conditional marginals 1/4 | illustration (A-REV1) | A-REV1/REVIEW.md; W6-FIXREV1/CONSOLIDATED.md | [pos 470] [pos 742] | feeds: none (campaign-only) |
| CE157 | C0; counterexample C0 | counterexample | Three states a1,a2,o, A={a1,a2}, log gamma0=(0,-30,-5), log gamma1=(-30,0,-5): q0(A)=q1(A)=0.9933 but q_{1/2}(A)=9.1e-5 | COUNTEREXAMPLE; SF VERIFIED (W3-VT38E, exact 9.08e-5) | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 370] | refutes RF198; feeds none |
| CE158 | C1; C1-T38E; counterexample C1 | counterexample | Four-state SMC: A={a1,m,a2}, log gamma0=(0,-120,-55.2,-10), log gamma1=(-2000,-2000,0,-1930), T=1000 uniform stages: no particle in A in 0.480/0.995 of islands at N=1e5/1e6 (W1 kernel), 0.56/1.00 (reversible kernel) | COUNTEREXAMPLE (reproducible); SF VERIFIED* after kernel repair (W3-VT38E); reproduced by W4-SHARE; no XF verdict row | W1-T38E/PROOF.md; W3-VT38E/REPORT.md; W4-SHARE/PROOF.md | [pos 238] [pos 370] [pos 742] | refutes RF199; feeds none |
| CE159 | TD(d,0) failure CF1/CF2; swap dominance | counterexample | CF1: TD(1,0) fails at 248/352 (n=400) and 728/1004 (n=1600) states of R_1; CF2: TD(2,0) fails at 26,019/29,936 states; swap proxy->j beats addition of j by ≈ 1/2 log n + log p | COUNTEREXAMPLE (reproducible); SF VERIFIED, strengthened to a universal statement (W3-VT38E) | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 238] [pos 370] | refutes RF165; feeds none |
| CE160 | GP(2) four-state failure; gp_fail_probe | counterexample | In CF2 GP(2) fails at 4 states (two proxies jointly replace x3, greedy deletes the true x3); all 4 reach S0 in 3 moves; 149 failures in an independent design at n=400 | COUNTEREXAMPLE (numerical); SF VERIFIED | W1-T38E/PROOF.md; W3-VT38E/REPORT.md | [pos 370] | shows GP(d) stronger than TD'; feeds none |
| CE161 | E3(ii) p=2 counterexample | counterexample | n=20, p=2, orthogonal columns, y=x2, B=1, x°={1}: claimed bound 1.983e23 vs pi0({1}) = 9.4416e-14, start mode {2} | reproduced (A-REV1; W6-FIXREV1 matches every digit) | W6-FIXREV1/CONSOLIDATED.md | [pos 557] [pos 570] | refutes RF202; feeds none |
| CE162 | Lemma S negative low weight; f=0.05, e=0.9 | counterexample | At e=0.9, f=0.05 the two-level low weight is -0.453 (A-REV1: -0.45297), positive iff f > 1-e | reproduced (A-REV1, W6-FIXREV1) | W6-FIXREV1/CONSOLIDATED.md | [pos 557] [pos 570] | refutes RF201; feeds none |
| CE163 | Kantorovich two-level weights {1, 1.925} | counterexample | Two-level weights {1,1.925} give ESS/H = 0.8999927 < 0.9; 4r/(1+r)^2 = 0.9 exactly at r* | exact (W3-VT38E; W6-FIXREV1) | W3-VT38E/REPORT.md; W6-FIXREV1/CONSOLIDATED.md | [pos 370] | refutes RF200; feeds none |
| CE164 | CEX-Mbquad(A3) | counterexample | Orthogonal p=n-1, one true coefficient theta=1, sigma^2=1, T empty: exact gain/n -> (log 2)/2 = 0.34657, quadratic term/n -> 1/4 (n=10000: 0.345653 vs 0.249564) | referee-authored COUNTEREXAMPLE (A-REV3) | A-REV3/REVIEW.md; T38-RECORD/REGISTRY_v2.md | [pos 742] | refutes RF203; feeds none |
| CE165 | CEX-MbBMC(A3) | counterexample | theta^2 = C log n/n (C >= BM-C constant, e.g. 1024), p=n-1: gain (C/2-3/2) log n, lambda_n = (3/2) log n, crossing-temperature ratio -> 3/C > 0 | referee-authored COUNTEREXAMPLE (A-REV3) | A-REV3/REVIEW.md; T38-RECORD/REGISTRY_v2.md | [pos 742] | refutes RF203 scope clause; feeds none |
| CE166 | CEX-exitloss(A3) | counterexample | Two-state kernel (good a, absorbing bad o), survival 1/2 per round, T = floor(1.6 log N): sum eta = 0.8 log N satisfies the printed condition but E n_T(a) = N 2^{-T} -> 0 | referee-authored COUNTEREXAMPLE (A-REV3), abstract | A-REV3/REVIEW.md; T38-RECORD/REGISTRY_v2.md | [pos 742] | refutes RF204; feeds none |
| CE167 | CEX-SHrare(A3) | counterexample | Rare outsider pi0(o) = 1/N: with probability (1-1/N)^N -> e^{-1} no outsider is present; extinction <= 1 - e^{-1} (0.63212) at kappa = 3 log N | referee-authored COUNTEREXAMPLE (A-REV3) | A-REV3/REVIEW.md; T38-RECORD/REGISTRY_v2.md | [pos 742] | refutes RF205; feeds none |
| CE168 | CEX-ESSneutral(A3) | counterexample | Two states, d=0, identity moves, multinomial resampling: ESS ratio one at every interval yet a class is lost by neutral drift at fixed N | referee-authored COUNTEREXAMPLE (A-REV3), abstract not BVS | A-REV3/REVIEW.md; T38-RECORD/REGISTRY_v2.md | [pos 742] | shows ESS alone is not a delivery theorem; feeds none |
| CE169 | SHARE-PB; posterior-barrier design PB | counterexample | BVS design with lambda_min(R_{S0}) = 0.004, pi(S0)=0.94-0.97, start mode {12} ⊂ S0 (pi0≈0.98): delivery to R_0 in 200/200 islands, LT fails (median log Zhat/Z = -67), S0 scored only through a rare gate in 82% (n=4000) and 51% (n=16000) of islands; Prop X bound 0.48 | COUNTEREXAMPLE (finite n, reproducible; W4-SHARE; no verifier assigned); defeats route (b2), LS0 and T39 alike | W4-SHARE/REPORT.md; W4-SHARE/PROOF.md | [pos 371] [pos 742] | cited as related for K99 qualitative barrier remark (S-LIM); FW15 quantitative |
| CE170 | LH swap counterexample to C2; g=4, rho=0.85, psi=0.5; STAB-LH failure A85 | counterexample | One pair, g=4, rho=.85, psi=.5, beta_a=1.4, beta_b=-.7, V={0,1,2,3}, W={1,2,3,4}: Delta(V)=.3675, Delta(W)=.3627106863596872, swap 0->4 improves the fit by .004789313640313 (also g=9) | referee-authored COUNTEREXAMPLE (A-REV7); reproduced exactly by Claude (API-VSTAB) | A-REV7/REVIEW.md; API-VSTAB/REPORT.md; W5-B2ENV/PROOF.md | [pos 919] [pos 978] | refutes RF208; feeds none |
| CE171 | DOM visible-hub swap counterexample | counterexample | One pair, g=4, rho=.4, psi=.2, beta_a=1, visible hub h=8 with beta_h=.01: swap h->b lowers the residual from .0384 to .0001 | referee-authored COUNTEREXAMPLE (A-REV7) | A-REV7/REVIEW.md | [pos 919] | refutes RF207; feeds none |
| CE172 | Schur-increment n=10 example | counterexample | n=10, U empty, x_j'x_j=9, x_j'y=1: actual increment .1; printed expression gives 1.1 | referee-authored (A-REV7) | A-REV7/REVIEW.md | [pos 919] | refutes RF209; feeds none |
| CE173 | non-closure of W+; f1b_swap_margins | counterexample | LH20 (p=20,c=2, rho=0.7, psi=0.5, g=B=4), n=1600: from x - j_h + b' the swap b' -> proxy(j_h) is posterior-favourable by +175 nats; landing state worse than x+b' by >= 107 nats | numerical (F-SHARE exact enumeration) | F-SHARE/REPORT.md; F-SHARE/PROOF.md | [pos 748] | refutes RF210; feeds none |
| CE174 | CF(1) instances not masked; iid miss 0.000 | counterexample | In every CF(1) instance used (n=400,1600, 4 designs) pi0(S0)=9.6e-5 to 2.2e-3 and the tier-0 iid miss is 0.000; 'iid miss >= 0.86' is tier-0 only (0.64-0.86 across designs, 0.001-0.09 at tier 1) | numerical (W3-VT38E) | W3-VT38E/REPORT.md | [pos 370] | supports RF214; feeds none |
| CE175 | CEX-guard; stylised guard counterexample; conditioning on completion counterexample | counterexample | T12(iv.b) component instance n=20, p=2, T=1, N=1, L'=L=5, M=4; stylised guard cost 1+k^3 per scored model of size k, checked after the stage-1 bridge stage; output iff accumulated cost <= h: h=33 stops 0.22% and E[Zhat/O]/Z = 0.9739; h=32 gives 0.7978; h<=30 gives 0.011 | COUNTEREXAMPLE (stylised cost model, exact 50-digit enumeration); SF VERIFIED (W5-LOCKBOOK reproduced; also under engine-faithful cost: 0.32% stops give 0.975 Z, 3.0% stops give 1.0014 Z); XF VERIFIED qualitatively (A-REV4; stylised, not an estimate of production bias) | W2-BOOK/PROOF.md s0.3; W2-BOOK/NOTES.md; W5-LOCKBOOK/REPORT.md s4.1; A-REV4/BOOK_CHECK.md | [pos 328] [pos 342] [pos 742] | S-OUT K77 (negative result); M1 clause |
| CE176 | GUARD counterexample (allocation and diagnostics fields); E2; B1 | counterexample | Two completed runs with the same data and seed but different sufficiently large allocations return different allocation, timings, peak_memory_kb, runtime_guard fields; RuntimeGuard::check also appends a GuardRecord on a non-stopping check, which the guard-free run does not | COUNTEREXAMPLE to the literal GUARD claim (A-REV4 B1; A-REV8 E2); API-AUDIT confirms the statistical outputs are bitwise equal on 10/10 fits | A-REV4/BOOK_CHECK.md; A-REV4/REVIEW.md; A-REV8/REVIEW.md E2; API-AUDIT/REPORT.md s2 | [pos 696] [pos 843] [pos 1009] | S-OUT GUARD-W (statistical scope) |
| CE177 | E1 (A-REV8); LS-score move-count counterexample; n=4 p=1 C0=S0 | counterexample | n=4, p=1, any centred nonconstant column and response, S0 = C0 = {1}, l = 0, centre emitted: hypotheses (i) vacuous, (ii) 0 >= -1, (iii) holds; truth is scored at zero moves, but 0 is not at most -1 | COUNTEREXAMPLE (A-REV8 E1; analytic); repair max{Phi(C0)-1,0} | A-REV8/REVIEW.md E1 | [pos 843] [pos 919] | M5 (a) |
| CE178 | A-REV5 slow-p counterexample; (b1-LH) c=2 with p ~ log log n | counterexample | c=2, p asymptotic log log n rounded to a multiple of the fixed group size 9, fixed admissible correlations and coefficients; exact Gram exists, eventually B=16 so g<=B<2g; pi0(S0)=n^{-1}p^{-2}exp(O_P(1)); hypothetical SMC budget Q_f >= 4n(L+6), so Q_f pi0(S0) >= const (log n)/p^2 exp(O_P(1)) diverges in probability | COUNTEREXAMPLE (A-REV5; analytic asymptotic, not numerical); the sequence eventually enumerates, so the hypothetical SMC budget is not the executed production budget (branch-qualification GAP); LS0 scoring implication unaffected | A-REV5/REVIEW.md s2; A-REV5/REV1_CHECK.md s4 | [pos 807] [pos 919] | FUTURE_WORK FW10 |
| CE179 | LH-LAT heterogeneous non-sharpness; W5-VMASK R5 table | counterexample | Brute-force grid of 202 LH settings: m0 equals the true Phi>=2 population margin in 108/108 homogeneous settings (common psi, common /beta/) but is strictly below it in 32/94 heterogeneous settings, down to a ratio 0.002; binding term R_{i*} - max_{i in I} kappa_i R_i with i* = argmax R_i | COUNTEREXAMPLE to 'm0 is sharp' (W5-VMASK row 23', R5; numerical, results/margins_grid.txt); A-REV8: valid lower bound, not universal sharp margin | W5-VMASK/REPAIRS.md R5; W5-VMASK/REPORT.md | [pos 463] [pos 843] | none |
| CE180 | exact branch at p=18, n=2^18 | counterexample | p=18, n=2^18=262144: K=p, 262144 feasible models <= exact threshold 23706288 so enumeration is taken | verified by hand in A-REV4 (threshold>=4*2^18*18) and A-REV5 (23706288) | A-REV4/REVIEW.md; A-REV5/REVIEW.md | [pos 677] [pos 806] | refutes RF225 |
| CE181 | CEX-guard; stylised guard counterexample | counterexample | n=20,p=2,T=1,N=1; cost 1+k^3 per scored model; guard after stage 1: 0.22% stops give E[Z-hat/output]/Z=0.974, 0.93% give 0.798, 3.9% give 0.011 | COUNTEREXAMPLE (exact, 50 digits); SF reproduced incl. engine-faithful cost (bias can be upward); XF VERIFIED* (A-REV4) | W2-BOOK/PROOF.md; W5-LOCKBOOK/REPORT.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | refutes RF227; M1/S-OUT/S-POOL |
| CE182 | T12(iv.b) component instance; pooled x pooled bias instance | counterexample | n=20,p=2,T=1,N=1,M=4,L'=L=5,j=1: E[P-bar_1]-PIP_1=-0.173974177850, pooled relative bias -0.131716, D=8.14676240634, PIP_1=0.990618012243 | reproduced by W2-BOOK (50 digits), W5-LOCKBOOK (60 digits), A-REV4 (Owls) | main@c4ef0dc/Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md; W2-BOOK/REPORT.md; W5-LOCKBOOK/REPORT.md; A-REV4/REVIEW.md | [pos 334] [pos 342] [pos 424] [pos 507] [pos 677] [pos 796] [pos 806] | refutes RF226 |
| CE183 | OPW2-cex instance; p=6 Gibbs-only, a_4*=0.90 vs chi2_4=0.111 | counterexample | n=60 AR(0.9) design, p=6, gibbs1 kernel, thr 0.9: T=5, min PW2 constant a*=0.896 vs chi2=0.111; other rows a*=4.13 (p=8,corr .95) and 0.416 (indep) | numerical, exact enumeration; MC N=20 agrees (0.1357 vs 0.1360) | O-PW2/REPORT.md; O-PW2/results/pw2_p6_rho0.9_gibbs1_thr0.9.json | [pos 673] [pos 706] [pos 748] [pos 830] [pos 915] | refutes RF228, RF236 |
| CE184 | M3 repaired instance (A-REV9) | counterexample | 0<a<min(c,(1-delta)/kappa); C split into masses kappa-kappa' and kappa' with W=a and W=[1-delta-a(kappa-kappa')]/kappa'; on C^c f=1, W=delta/(1-kappa); P(W<c/C)=1-kappa'/kappa->1 | referee-authored (A-REV9), abstract moment instance only | A-REV9/MASKED_PW2_CHECK.md; A-REV9/REVIEW.md | [pos 675] [pos 748] [pos 830] [pos 915] [pos 919] | repairs RF229 |
| CE185 | ADRAFT-CEXh; equality indicator h=1{theta_j=theta*_j} | counterexample | Posterior expectation 0 (continuous slab, atom at 0 for inactive) but value 1 at the generating parameter | PROVED; Astra-on-Astra VERIFIED* (A-REV4) | A-DRAFT/REPORT.md; A-REV4/DRAFTS_CHECK.md | [pos 493] [pos 494] [pos 563] [pos 616] [pos 677] | refutes RF230 |
| CE186 | expectation-convention counterexamples (A-REV4, A-REV6) | counterexample | A=O=whole space and exact evidence equally likely 1 or 2 gives expectation 1.5 > Z on the first data outcome; exact enumeration completing surely with A SMC-only gives left Z>0, right 0 | referee-authored analytic examples (A-REV4 section 2; A-REV6 BOOK R2) | A-REV4/REVIEW.md; A-REV6/BOOK.md | [pos 677] [pos 806] | refutes RF232 |
| CE187 | two-state instance, c24_twostate.py | counterexample | pi0(a)=0.01, pi(a)=0.99, one particle: W=99 w.p. 0.01 and W=0.0101 w.p. 0.99; E W=1, E(W-1)+=E(1-W)+=0.98 | PROVED (PC1 claim 4, line by line and script) | MEET-v31/evidence/2026-11-03_PC1_proof_check.md | pos: n/a (theorem-meeting phase) | refutes RF233 |
| CE188 | vanishing-signal sequence; theta_n=n^-1, support {1} | counterexample | Fixed-p sequence with theta_n=n^-1: SMC-restricted P1 can be vacuous while exact-posterior truth-PIPs fail (why P1-ex is needed) | referee-authored illustration (A-REV4 section 1 item 6), no numbers | A-REV4/REVIEW.md | [pos 677] | explains T26-shorthand GAP |
| CE189 | O-VCERT section 2.1 factor design n=40 p=10 | counterexample | Every model scored, Zhat=Z; T = top-m models: m=3, alpha=0.5 claimed unscored mass >= 0.590 vs true 0 (outside T 0.795); m=10: claimed 0.007 vs 0 (outside T 0.504) | O-VCERT computation (vcert_check.py section 4); A-REV9 restates analytically | O-VCERT/REPORT.md; A-REV9/REVIEW.md | [pos 729]; [pos 763] | none |
| CE190 | A-REV9 self-inclusive gap counterexample | counterexample | Any two scored models with strict gap g>0 and S=HPM: 1 <= exp(-g) fails | Analytic (A-REV9) | A-REV9/REVIEW.md | [pos 830]; [pos 917] [pos 919] | none |
| CE191 | A-REV9 duplicate-column tie counterexample for C5 | counterexample | Identical predictor columns 1 and 2 give F({1})=F({2}); truth {1}, alternative {2}, U={1,2}; lexicographic rule prefers {1} | Analytic (A-REV9) | A-REV9/REVIEW.md | [pos 830]; [pos 917] [pos 919] | none |
| CE192 | O-VCERT section 2.2 floating-point instance | counterexample | SC(eta_F) allows F^fp = F + eta_F on every S in T; if Z_T ~ Z then Z_T^fp ~ e^eta_F Z > Z so the deterministic bound can be false on every run | Logical gap, not an observed failure (O-VCERT) | O-VCERT/REPORT.md | [pos 729]; [pos 763] | none |
| CE193 | A-REV9 O-SWAP Prop. 2 construction | counterexample | Varying the Gaussian component in span(X_S0) changes the exact PA threshold while keeping orthogonal residual components fixed (W_S0 is noncentral chi-square) | Analytic (A-REV9) | A-REV9/REVIEW.md | [pos 830]; [pos 917] [pos 919] | none |
| CE194 | W7-SEC engine error_bound stress test | counterexample | y = x1 + noise, k in {1,2}: /Dlog m//eta_eng = 1.17 at n=1e5, 3.5 at n=1e6, 6.2 at n=4e6; held with ~24x room at n=200 | Author run (seed 20261104); A-REV9 deferred | W7-SEC/PROOF_T33.md; W7-SEC/REPORT.md | [pos 711]; [pos 742] | FUTURE_WORK FW16 (K107) |
| CE195 | API-N200 distance-2 union bound | counterexample | C(p-s0,2) ~ 1.2e5 pairs times e^(-2 kappa+(1+eta)) ~ 0.07 at p=500, c=1; true two-add-only probability ~6e-4 for orthogonal nulls | Author computation (API-N200) | API-N200/PROOF.md; API-N200/REPORT.md | [pos 978] | none |
| CE196 | O-VCERT non-monotonicity of m(S) and endpoint failure | counterexample | m rises on 185,095 additions and falls on 291,065; endpoint evaluation max(F(L),F(U)) underestimates the box maximum in 2,764 of 6,561 boxes | O-VCERT exhaustive tests (results/vcert_check.txt) | O-VCERT/REPORT.md | [pos 729]; [pos 763] | none |
| CE197 | Exact large-p numerics vs F-DRAFT W(c); n=1e16, p=n^0.95, r=0.9 | counterexample | Exact lower bound on l(2) 8.8e3 nats (REPORT; 7961 nats independent) against W(c) prediction 13.08; 35-row table, s0=2, r=0.9 | numerical, two independent implementations; rigorous contradiction asymptotic (W(e)); SF CHECK_SEP_W F8 | O-WSTAB/REPORT.md; O-WSTAB/review/CHECK_SEP_W.md | [pos 748] | refutes RF252/RF253; feeds TH362 |
| CE198 | A-REV4 counterexample to F-DRAFT W2; n=20, p=4 | counterexample | n=20,p=4,G=19I, blocks {1,3},{2,4}, S°={1}, l=2, //y//^2=19, z^2=(100,30,0,0): actual 0.310405538698 vs RSS-based 0.353784569589 (difference 0.043379030891) | referee-authored; reproduced on Owls (A-REV4 NUMERICS) | A-REV4/REVIEW.md; A-REV4/NUMERICS.md | [pos 677] [pos 919] | refutes RF254 |
| CE199 | Zero cross-block correlation, chi2 diverges; p=n-1, one coefficient 2, sigma^2=1 | counterexample | XtX=(n-1)I, p=n-1, one nonzero coefficient 2, sigma^2=1 (R2=0.8): chi2(pi//pi0)->inf while TV->0 | PROVED within WS6(d) (VERIFIED WITH AMENDMENT, CHK_INHERITED); numerical sanity n=65536, ten seeds | O-WSTAB/PROOF.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md | [pos 748] [pos 616] | refutes RF256; feeds M2 (c1) |
| CE200 | Proxy-split exact stage counts 14, 16, 18 vs log2 A0 + 7.7 | counterexample | p=12, two blocks of 6, exact enumeration: T*=14,14/16,16/18,18 at n=200/800/3200 against log2A0+7.7=14.1/16.1/18.0 | numerical (exact population grid); SF none; XF A-REV9 did not reproduce numerics | O-STAGES/REPORT.md | [pos 733] [pos 748] | refutes RF255; feeds TH368/TH369 |
| CE201 | Two-state family: L<=pi but T* -> infinity | counterexample | T*-log2 A0 in [6.0,8.1] for A0 0.5..1e6, A1 5..1e5; T*=9,13,17,20,23,27,30 for D=10..1e7 | numerical (two_state.txt); PROVED order in TH368 | O-STAGES/REPORT.md; F-DRAFT/NEW_TARGETS.md | [pos 733] [pos 748] | refutes RF255/RF258 |
| CE202 | Window p^r = sqrt(n)/log log n (CHECK_SEP_W F1) | counterexample | r in (1/2,1), p^r=sqrt n/log log n: rho_n(2)->0 but rho_n(2) sqrt(log p)->inf; step of the proof of W(d) upper half fails | counterexample to a proof step, not to the theorem; numerical table r=0.9 | O-WSTAB/review/CHECK_SEP_W.md | [pos 748] | refutes RF257 hypothesis; leaves CJ266 |
| CE203 | Abstract TV,KL->0 while chi2->inf | counterexample | pi=(1-1/k,1/k), pi0=(1-1/k^3,1/k^3): TV->0, KL~2log(k)/k->0, chi2~k; also pi0=(1-eps, eps e^{-1/sqrt eps}) normalised, pi=(1-eps,eps) | referee-authored (A-REV4); abstract, not the claimed BVS theorem | A-REV4/REVIEW.md; A-REV4/DRAFTS_CHECK.md | [pos 677] [pos 919] | supports TH356/TH362; refutes draft consequence small divergence implies stable weights |
| CE204 | E exp(Z^2/2) is infinite | counterexample | E[e^{Z^2/2} 1{Z^2<=tau}]=sqrt(2tau/pi)->inf | elementary (REPORT proof of HT) | O-WSTAB/REPORT.md | [pos 748] | refutes RF260 |
| CE205 | Family F″(u+x)=x^-a, a up to 2 (T* vs path length) | counterexample | Makes (int sqrt F″)^2/Phi unbounded | author statement (O-STAGES section 5); no numerics | O-STAGES/REPORT.md | [pos 733] | refutes RF261 |
| CE206 | Single extreme particle forces pilot step of order 1/n (informal) | counterexample | One pilot particle with d-d(S0) of order n makes trimmed range of order n, so Lemma P only gives step 1/n | informal argument (T26BUD REPORT section 5) | API-T26BUD/REPORT.md | [pos 978] | refutes RF259 (informally) |
| CE207 | SEP-taska; LH greedy-universality exact enumeration (386 replicates, 40-design stress test) | counterexample | LH families B2 (c=2,p=20), V2 (c=2,p=18), C3 (c=3,p=18), n 100 to 409600 and scaling runs p 108-864: LS0 scores S0 in 386/386; GU stress 40 designs p=14 all pass by n=50000 | COUNTEREXAMPLE (by proof Cor GU-LH and numerics); XF: numerics not reproduced (A-REV9) | W7-SEP/PROOF.md; W7-SEP/REPORT.md; T38-RECORD/REGISTRY_v2.md (row SEP-taska) | [pos 763] [pos 796] | M6 scope boundary (SEP-taska) |
| CE208 | Prop M; ADRAFT-PropM; Prop NM-A; A-DRAFT Proposition M; identifiable cross-block proxy p=2 | counterexample | p=2, X'X=(n-1)[[1,rho],[rho,1]], y=b x1+eps: local PIPs ->1, product/union put mass ->1 on {1,2}, full posterior ->1 on {1}, TV ->1; table rho=0.8 b=sigma*=1 | COUNTEREXAMPLE, complete proof (author A-DRAFT = Astra; used by A-REV4 as valid repair; no campaign verification) | A-DRAFT/REPORT.md; A-REV4/DRAFTS_CHECK.md | [pos 563] [pos 613] [pos 616] [pos 796] | none (naive merge dropped as K98) |
| CE209 | CEX-NMremainder(A4); fixed-p two columns b=sigma=1 r=1/2 | counterexample | O_P(1) remainder in log BF({l}) = nc/2 - (1/2)log n + O_P(1) false for fixed nonzero proxy correlation: sqrt(n) fluctuation about n log(8/7)/2 | referee-authored (A-REV4); numerical corroboration 256 replicates per n, 768 saved (A-REV4/NUMERICS.md) | A-REV4/REVIEW.md; A-REV4/DRAFTS_CHECK.md; A-REV4/NUMERICS.md | [pos 796] [pos 1238] | none |
| CE210 | LIT-PAR G4; Song-Liang-type splitting counterexample on LH-like masked pair p=16 n=200 | counterexample | Exact posterior recovers S0 in 20/20 datasets; split-and-merge recovers it in 5/318 splits separating the linked pair (median stage-I PIP of masked variable 0.010), 265/282 when pair together; 0/318 at beta=0.6 | COUNTEREXAMPLE (numerical, reproducible); analytic PIP -> 0 step not verified; cited in paper as labelled numerical evidence | LIT-PAR/REPORT.md; MEET-THM/MINUTES.md | [pos 1072] [pos 1626] | FUTURE_WORK FW21 (cited as labelled numerical evidence; Cor 2 wording) |
| CE211 | W1 PC1 E4 SL_sample_cov_cex; n=20 | counterexample | x_t^T mu = 0 but x_t^T y = x_t^T eps nondegenerate Gaussian (value .4358899 at n=20) | filed check by PC1 (gpt-6.1-sol); DESIGN-VERIFIED; conceded in R2 | MEET-THM/evidence/W1_PC1/VERDICTS.md; MEET-THM/R2_B.md | [pos 1608] | FW21 (K97) |
| CE212 | ZYVR informed chain with parallel neighbour scoring; Zhou-Yang-Vats-Roberts-Rosenthal JRSSB 84(5) 2022 Thm 1; counterexample candidate to "guarantees => sequential" | counterexample | One informed (locally informed, thresholded) chain with a p-free proved mixing bound T_mix <= 800 max(n kappa_1/c_1, 3 s_0) under n = O(p), s_0 log p = O(n), kappa = O(s_0) and Condition 1 (no underfitted model without a p^{c_1}-better addition; overfitted additions penalised by p^{-c_0}); each iteration scores O(p s_0) neighbours which "can be easily parallelized" (authors), so depth is O(n log p) score rounds; API-POS: Condition 1 holds on LH with ZYVR's priors (PROOF SKETCH), for the paper prior and cap it fails as stated | literature counterexample candidate (LIT-PAR §1 item 2, §3.2 TH1 severity high); does not refute the three-part S-GAP (no unbiased Zhat, no islands, unimodality condition excludes competing models at n = 200) | LIT-PAR/REPORT.md §1, §2.2, §3.2 TH1, §4.3; API-POS/REPORT.md §4.2 | [pos 1070] [pos 1107] | none (positioning) |
| CE213 | SaM on an LH-like masked design; sam_lh_demo.py; 5/318 splits; LIT-PAR G4 numerical counterexample | counterexample | LH-like design (LIT-PAR construction, not the exact W1-EXP family): p = 16; groups {0..3}, {5,6,7}, {8..11}, {12..15} equicorrelated rho = 0.7; x4 a singleton linked only to hub x0 with corr psi = 0.5; truth theta_0 = beta, theta_4 = -psi beta (suppressor), theta_8 = beta; S0 = {0,4,8}; n = 200, noise sd 1; cov(x4,y) = 0; Zellner g = n, sigma^2 integrated, BB(1,p), cap 6; SaM as in Liang's slides (2 halves, exact Stage-I posterior per half, keep PIP > 0.5, Stage II exact posterior on the merged set, HPM). beta = 1.0: full posterior HPM = S0 in 20/20; SaM recovers S0 in 5/318 splits separating (0,4) (median Stage-I PIP of x4 = 0.010) vs 265/282 when the pair stays together; clustered split {0..7},{8..15}: 15/20. beta = 0.6: 13/20; 0/318; 154/282; 3/20. Seed 20261103 | COUNTEREXAMPLE (numerical, reproducible) to "SaM recovers S0" on an LH-like masked design when the random split separates the linked pair [LIT-PAR §3.1 G4]; analytic part PROOF SKETCH, corrected by RF276/TH417; author-only; cited at MEET-THM as labelled numerical evidence | LIT-PAR/REPORT.md §3.1 G4; LIT-PAR/notes/09_sam_lh_counterexample.md | [pos 1070] [pos 1107] | FUTURE_WORK FW21 (K97); Coverage Cor 2 (numerical evidence) |
| CE214 | isolation probability of a masked hub under a uniform equipartition (THM-SYNTH check_lemmas.py); Theorem SL(a) numbers | counterexample | Exactly P(j_b isolated from g given columns) = C(P_n-1-g, s_n-1)/C(P_n-1, s_n-1); the union bound is vacuous at small K_n: at K_n = 2, P(isolated) = 0.53 for g = 1 (LIT-PAR design, P = 16) but 0.05 for g = 4, so at fixed K_n the failure probability is bounded away from 0 but can be small and "-> 1" needs K_n -> infinity | numerical check (THM-SYNTH scripts/check_lemmas.py, seed 20261103); part of Theorem SL (TH417, PROOF SKETCH); shows LIT-PAR's 5/318 used g = 1 | THM-SYNTH/THEOREM_LIST.md (C1(i)(a)); THM-SYNTH/REPORT.md §1 item 6 | [pos 1177] | FUTURE_WORK FW21 |
| CE215 | LIT-MCMC ob_check: R < M in 12 of 12 study-like data sets (S1/S4, n = 200, p in {500, 1000}) | counterexample | Study-like (not the study's own) generator: n = 200, p in {500, 1000}, s0 = 14, sigma = 1, designs S1 (iid) and S4 (blocks of 5, 0.85H + 0.15I), 3 replicates each, paper exact score; scoring only gamma_{e*} = S0 + {e*} and its add/delete/swap neighbours gives R_ub >= R and M_lb <= M; log_p R_ub in {0.23, 0.43, 0.36 / 0.36, 0.54, 0.49 / -0.21, 0.43, 0.53 / 0.30, 0.47, 0.37}, log_p M_lb = 1.44 (p = 500), 1.40 (p = 1000); R < M certified 12/12, margin at least p^0.87, so R > M^2 fails as well; one replicate (p = 1000, S1, rep 0) is a posterior miss with log pi(S0)/pi(gamma_e*) = -2.08 | COUNTEREXAMPLE to the applicability of Chang-Zhou Thm 1/4, Zhou-Smith Assumption 1 and ZYVR c0 = 2 to the paper target at the study scale [LIT-MCMC §4]; reproducible with scripts/ob_check.py; author-only; explained by Prop OB (PROOF SKETCH) | LIT-MCMC/results/ob_check.md; LIT-MCMC/REPORT.md §0 item 1, §4 | [pos 1009] | FUTURE_WORK FW4 |
| CE216 | LIT-MCMC rz_lh: exact enumeration of R and M on LH (p = 16, 20) | counterexample | Paper target on exact-Gram LH (c = 1: p = 16, rho = 0.7, psi = 0.5; c = 2: p = 20, rho = 0.85), R = min_{x != x*} max_{y in N(x)} pi(y)/pi(x), M = max /N(x)/, N = add/delete/swap: S0 is the unique mode (0 other local modes) at every n tested; R > M fails at n = 200 and 1,600 for both c (log_p R 0.95 vs log_p M 1.58 at n = 200, c = 1; 0.88 vs 1.60 at c = 2) and holds only at n >= 12,800 (c = 1) and n = 102,400 (c = 2); R > M^2 fails at every n up to 102,400; flattest state almost always overfitted (a superset of S0 or the full model) | COUNTEREXAMPLE to R > M (Chang-Zhou Thm 1) and R > M^2 (informed samplers) for the paper target on LH [LIT-MCMC §4]; p <= 20 only (OB predicts the failure is worse at p >= 500); author-only | LIT-MCMC/results/rz_lh.md; LIT-MCMC/REPORT.md §4; API-POS/results/cond1_lh.md | [pos 1009] | FUTURE_WORK FW4 |
| CE217 | N9 negative controls: mutated kernels that must fail detailed balance | counterexample | Three mutated controls on the production-extraction harness (designs n = 20, p = 6 and 8; n = 10, p = 8 with cap K = 5; phi in {0, 1/2, 1}): a neighbour swap without its Hastings factor fails detailed balance (DB rel 0.5-0.75; the factor is != 1 on 31-61% of proposals, 120 of 256 in the HQ note); an independence step with symmetric acceptance fails (rel 1.0); the canonical fixed-order product fails self-adjointness at phi > 0 (rel 0.68-0.999 / 0.92-0.999); the production kernels pass to <= 2.3e-12 relative | numerical controls showing the check has power [N9 REPORT §1]; author-only; not a counterexample to any claim of the campaign | N9-KERNEL/REPORT.md §1; N9-KERNEL/HQ_NOTE.md; N9-KERNEL/CHECK.md | [pos 1546] [pos 1550] [pos 1593] | S-KERNEL (K20, K21) |
| CE218 | fixed canonical order at phi = 0 is reversible (counterexample to "a fixed order is not self-adjoint") | counterexample | At phi = 0 the final independence step refreshes exactly from pi0, so the canonical fixed-order product is reversible; commuting kernels can also stay reversible under a fixed order | recorded in N9 CHECK.md and used by CHK_INHERITED (cross-family, gpt-6.1-sol) to amend REPORT row 6 ("A fixed order need not be self-adjoint") | N9-KERNEL/CHECK.md; MEET-THM/evidence/CHK_INHERITED/REPORT.md §5 | [pos 1626] | S-KERNEL (K21) |
| CE219 | two-state instance of upward Zhat excursions: W = 99 w.p. 0.01 | counterexample | pi0(a) = 0.01, pi(a) = 0.99, one particle (the masked start): W = 99 with probability 0.01 and W = 0.0101 with probability 0.99; E W = 1 and E(W-1)^+ = E(1-W)^+ = 0.98; Zhat overestimates by a factor of 99 with probability 0.01 | PC1 claim 4 explicit instance (c24_twostate.py), Claude same-family; shows that "Zhat errs only downward" is literally false | MEET-v31/evidence/2026-11-03_PC1_proof_check.md (Claim 4) | [pos 1242] | S-Z (K37-K41) |
| CE220 | post-search HPM nonmonotone in R prime: n = 29, p = 8 proxy design (c6_ls.py) | counterexample | Spec m(S), production local search (flips and swaps, centre frozen during each scan, best strict improvement, <= l moves then one more scan), seed 20261106; n = 29, p = 8, K = 8, l = 6, y = x0 + x1 + noise, x2 approx x0 + x1; two local maxima {2} (F = -34.843, the proxy) and {0,1} = S0 = S-dagger (F = -31.512); R = 4 run: pre-search HPM c4 = {0,1,2,3} (F = -35.789), path -> {0,1,3} -> {0,1}, post-search HPM = S0; R prime run: an extra island scores {2}, c prime = {2} (F = -34.843) is a local maximum, search stops, post-search HPM {2} != S0; with whole down-sets as scored sets 3,813 of 32,640 ordered pairs (c4 < c prime) give HPM(R prime) < HPM(4); adding the search from c4 restores {0,1} | COUNTEREXAMPLE (PC1 claim 6, Claude Opus 5.5 same-family; "I did not prove that the actual SMC realises these particular scored sets with positive probability ... CANNOT DECIDE here") | MEET-v31/evidence/2026-11-03_PC1_proof_check.md (Claim 6) | [pos 1242] | S-OUT (K84) |
| CE221 | Astra round-1 abstract instance for objection 2 | counterexample | Schematic instance of the hypotheses of theoremA3 with a previously scored model of score above F(S0) outside the search ledger; no numbers given | object of an Astra round-1 argument; closed by the pre-search ledger hypothesis in TH445/TH447 | L-LEAN/fidelity/ASTRA_round1.md (objection 2) | n/a | none |

## Alias index (normalised native label to ID)

| native label (normalised) | ID |
|---|---|
| "<=1/2foreveryi>=0" | RF281 |
| "theexactbranchfailsforp>=18,n>=22" | RF225 |
| 'attainedbytwo-levelweights' | RF187 |
| 'checkspass'fromcouplingalone | RF115 |
| 'two'/valley-protectedtwo-movesetasthenegativeregime | RF112 |
| 'unbiasedgivenoutput' | RF221 |
| (0) | TH281 |
| (0_h) | TH282 |
| (b-merge)onlh-iid(p>>n) | CJ159 |
| (b-merge)onlhexactgram | TH181 |
| (b1') | TH285 |
| (b1')undero_h | CJ216 |
| (b1'-lh) | TH269 |
| (b1) | LM104 |
| (b1-lh) | TH287 |
| (b1-lh)c=2withp~loglogn | CE178 |
| (b1-lh)iid-failureclauseforc>=2 | RF217 |
| (b1-lh-iid) | TH288 |
| (b2) | LM104 |
| (b2-lh) | TH272 |
| (b3) | LM104 |
| (c) | TH289 |
| (c-fix)deliverss' | CJ157 |
| (c-fix)iterationdeliverss'ingeneral | RF159 |
| (c1') | TH278 |
| (c1')/(c2') | TH261 |
| (c1)locked | TH277 |
| (cert) | TH274 |
| (d+) | TH279 |
| (duplicateentryrf224merged) | RF165 |
| (duplicateentryrf352merged) | RF233 |
| (duplicateentryth392merged) | TH269 |
| (duplicateentryth393merged) | TH272 |
| (duplicateentryth397merged) | TH241 |
| (d⁺) | TH279 |
| (e') | TH280 |
| (e')/(e-m) | TH239 |
| (e-m) | TH280 |
| (ht) | LM215 |
| (l+4)eta_n->0 | RF102 |
| (r5) | TH228 |
| (t_n+1)delta_n<1in0/56runsatn<=3,200 | RF155 |
| (track)+(osc)forbvs | CJ192 |
| (u-a) | RF186 |
| (u-b) | RF186 |
| (u1)-(u3) | LM118 |
| -3/4cov | TH298 |
| 0.05z-hatone-sided95%lowerbound | TH297 |
| 0/541forcedbymonotonicity | CJ176 |
| 0/541forcedremark | RF167 |
| 0of95 | CE103 |
| 1/31! | RF183 |
| 10^-1303 | CE124 |
| 233/234vs0/541discrepancy | CJ179 |
| 2^b-freefavourablerate,fixedpartition | TH190 |
| 2g<=bkillslhmasking | TH157 |
| 2g<=bstudygroupsof5 | CE118 |
| 2g_min<=b=>blocks!=groupssurely(unequalsizes) | RF141 |
| 4.16(m+2sigma^2)/sigma^2 | RF134 |
| 5/318splits | CE213 |
| 541fits | CE103 |
| 55vs0.64and0.16 | RF105 |
| 590-730/800-1,600/1,050-3,200 | RF160 |
| 8-targetarchitecture | CJ311 |
| 87declarations | RF283 |
| 95%evidencelowerbound | TH120 |
| 9<=g<=16rangeatn=200 | RF147 |
| [la] | LM172 |
| a-draftcorollarya1 | TH321 |
| a-draftcorollaryd1 | TH323 |
| a-draftpropositionm | CE208 |
| a-drafttheorema | TH320 |
| a-drafttheoremd | TH322 |
| a-prioriepsilonofval-fpcertifiableatstudybudgets | RF250 |
| a-priorival-fpepsilon | CJ235 |
| a-rev2counterexampleto'iff' | CE120 |
| a-rev4b5counterexample:scoredset{s1}withf(s0)=1,f(s1)=0 | CE112 |
| a-rev4counterexampletof-draftw2 | CE198 |
| a-rev4exactklbound | TH379 |
| a-rev5pointcheckatn=2,116,048:exp(2eps_n)=4639.924697>4 | CE115 |
| a-rev5slow-pcounterexample | CE178 |
| a-rev6counterexampletoce2header | CE119 |
| a-rev6four-statereplacementoff-draftnm | TH393 |
| a-rev6w2-r | TH378 |
| a-rev7minimalgap | CJ206 |
| a-rev9duplicate-columntiecounterexampleforc5 | CE191 |
| a-rev9o-swapprop.2construction | CE193 |
| a-rev9self-inclusivegapcounterexample | CE190 |
| a0 | TH101 |
| a1 | TH102 |
| a1(thm-synth) | TH412 |
| a1-a5 | TH199 |
| a1>=0.14atproductionb=14 | CJ188 |
| a1new | TH412 |
| a2 | TH103 |
| a2(thm-synth) | TH413 |
| a2lower-boundaccounting | LM252 |
| a3 | TH104 |
| a4 | CJ101 |
| a5 | TH105 |
| a5(a) | RF166 |
| a5(b) | TH199 |
| a6 | TH106 |
| a7 | CJ102 |
| a8 | CJ211 |
| a_t,nu_tslack | CJ122 |
| abl-confclaim1 | CJ164 |
| abl-confclaim2 | CJ165 |
| abl-startoutcome1depthclaim | CJ166 |
| abstracttv,kl->0whilechi2->inf | CE203 |
| accuracyclaim | CJ165 |
| accuracyofe_pi[h(s)]asngrowsinthemaskedregime | CJ298 |
| actualnoise-dependentpacking | TH191 |
| actualsmall-pv3onpropmfamily | TH391 |
| additionfloorr_k | TH108 |
| adraft-cexh | CE185 |
| adraft-cora1 | TH321 |
| adraft-cord1 | TH323 |
| adraft-maskedpip | CJ220 |
| adraft-novelty | CJ276 |
| adraft-propm | CE208 |
| adraft-smccomp | TH392 |
| adraft-thma | TH320 |
| adraft-thmd | TH322 |
| adraft-uncert | CJ275 |
| adraft-unipip | TH322 |
| adraft-v3exact | TH391 |
| agg-stat | RF120 |
| aggregatestartbounds | TH116 |
| allboundedhconvergetothegeneratingvalue | RF230 |
| analyticsplit-and-mergefailureonamaskedlhfamily | TH417 |
| analyticstabcertificate | TH274 |
| anchored=unanchored | LM105 |
| anchoringasthemainrelaxation | RF128 |
| aparallelwork/depththeorem | CJ299 |
| api-maskzpipfirst-draftlhevidencecollapse | RF231 |
| api-maskzpiplemmaj | LM203 |
| api-maskzpippropositione3 | TH310 |
| api-maskzpippropositionp3 | TH314 |
| api-maskzpippropositionsc1-c3 | TH315 |
| api-maskzpiptheoreme1 | TH308 |
| api-maskzpiptheoreme2 | TH309 |
| api-maskzpiptheoreme4 | TH311 |
| api-maskzpiptheoremp1 | TH312 |
| api-maskzpiptheoremp2 | TH313 |
| api-n20024-celltable | CJ243 |
| api-n200distance-2unionbound | CE195 |
| api-n200draftparagraphforthepapern=200section | CJ240 |
| api-n200exactenumerationatp=12 | CJ244 |
| api-posopenitems | CJ297 |
| api-pospropu | TH402 |
| api-posr3 | TH404 |
| api-posunimodalityonlh | TH403 |
| api-pxngaptheorem | TH161 |
| api-t03const | CJ134 |
| api-t26budconjecturep | CJ268 |
| api-t26budcorollary1 | TH372 |
| api-t26budfact1 | LM220 |
| api-t26budfact2 | LM221 |
| api-t26budlemmap | LM222 |
| api-t26budpropositiono | TH374 |
| api-t26budrulecap | TH373 |
| api-t26budtheorem1 | TH371 |
| api-t26budtheoremg | TH370 |
| arev1-ce1-seq | CE145 |
| arev4-klexact | TH379 |
| assemblyofpremises | TH236 |
| astrac37 | CJ119 |
| astracandidatebound | CJ208 |
| astracandidaterepairofpropm(b) | CJ207 |
| astradidnotfinish | RF284 |
| astraround-1abstractinstanceforobjection2 | CE221 |
| asympremises-t24 | TH238 |
| asymptoticpremisestable | TH238 |
| atmostphi(c0)-1moves(literal) | RF216 |
| b# | TH220 |
| b'-conj | CJ154 |
| b-,b+ | CE110 |
| b-rp | CJ105 |
| b.d9(b) | RF267 |
| b1 | CE176 |
| b1'-prem+pa | TH229 |
| b1'/b2'-vt24g | TH219 |
| b1-b3 | TH382 |
| b2-lh | TH272 |
| b2-lhwithoutstab-lh | CJ204 |
| b2-w4assembly | TH254 |
| b2e-b2lh | TH272 |
| b2e-conf | TH271 |
| b2e-d2lh | TH269 |
| b2e-l2.1 | LM178 |
| b2e-l2.2 | LM178 |
| b2e-latpot | TH273 |
| b2e-lemmaj | LM179 |
| b2e-lemmaof | LM177 |
| b2e-lemmar1 | LM181 |
| b2e-lemmat | LM180 |
| b2e-lhiid | CJ205 |
| b2e-mlh | TH270 |
| b2e-nblh | TH268 |
| b2e-open47 | CJ204 |
| b2env-finding | TH273 |
| b2lh-subfamily(a7) | TH275 |
| b_n->1 | TH150 |
| backfitstart | CJ162 |
| backfitsweepiterationconverges | CJ163 |
| backwardblock-sizesamplertelescopes | TH410 |
| barrieroftheexact-tailroute | TH126 |
| basin | CJ123 |
| basin(r,r0,a,eta,rho,delta) | CJ123 |
| basin-to-outputguarantee | TH117 |
| basinentranceexitdepartureoccupancy | CJ123 |
| bayesdecisions | TH106 |
| bb(1,p)+hpmphase2 | RF119 |
| bb(1,p)=bb(1,1)tiltedbyageometricsizefactor | LM228 |
| bb(1,p)isnotacomplexityprior | LM107 |
| bb(1,p)isnotacomplexitypriorinthesenseofcsvdv(2.2) | LM227 |
| bb(1,p)sizemarginal | LM101 |
| bb(1,p)versusbb(1,1) | LM108 |
| benchmarkgap | CJ101 |
| bestbelievedversionsoftheeightpapertargets | CJ311 |
| besttruthadditionresidualbound | LM151 |
| besttruthadditionunderse | LM147 |
| beta-minabout100x | RF105 |
| beta-removalconjecture | CJ171 |
| betatruncatedmomentsanyfixeddimension,polynomialfamilies | LM122 |
| bfdr | RF119 |
| bg1 | TH255 |
| bg1' | TH256 |
| bg3 | TH258 |
| binomialdomination | LM165 |
| biometrikaconditional | CJ296 |
| blanketworking-set/full-spacevacuityclaims(t12,l-rc) | RF116 |
| blindhalf | TH311 |
| block-map | RF119 |
| blockreduction | TH206 |
| blocksareunionsofwholegroupsw.p.->1 | LM143 |
| blockstartreducesdepth/stagesatequalaccuracy | CJ166 |
| bm-c | CJ130 |
| bm-inf | CJ130 |
| bm-infinity | CJ130 |
| bm-∞ | CJ130 |
| boexactstructureofd | TH350 |
| bookkeeping:c5screeningeventover2,400fits | CJ238 |
| bothfeasibleconfigurationsscored | CJ128 |
| boundarybandmaxrho0/rho+->1 | CJ175 |
| boundarycase2ar=1oftheoremwandwprime | CJ267 |
| bounded-leakagezjl | CJ186 |
| boxb&bcostheuristic2^(ambiguousvariables) | CJ248 |
| boxcertificate | TH329 |
| boxmonotonicity | TH329 |
| bracketsforpi(x) | TH335 |
| branch-specificarithmeticandstoragecounts | CJ112 |
| bridge-gibbsdiscovery | CJ193 |
| bridge-stagediscoveryforc>=3withoutbg3 | CJ203 |
| bridgeandpw2underiid | TH358 |
| bridgemass=>delivery | RF199 |
| brief'scosto(nt(p+b+2)+lp)fort38(c) | RF224 |
| brief'seligibilitycondition | RF197 |
| brief'sexponent(1-c')^floor(h/(s0+d)) | RF184 |
| brief/frozen_listtarget:theexactbb(1,p)tailcutsm_ntos0+o(s0logn/logp)soseismeaningfulatn=200 | RF121 |
| btpreplacement | TH229 |
| budgetexponents | TH386 |
| bw_w | CJ219 |
| c-e1screeningplug-inunderestimate | CE128 |
| c-e3non-boleakage(s5common-factorfamily) | CE129 |
| c-e4runawayoftheiterativeplug-in(c-fix) | CE130 |
| c-fixplug-inconjecture | CJ157 |
| c-ld | CE138 |
| c-ldforp~n^a | CJ172 |
| c0 | CE157 |
| c1 | TH115 |
| c1(thm-synth) | TH417 |
| c1-t38e | CE158 |
| c1-typeextinctioninbvsonlywhererepairfails | CJ194 |
| c14 | CJ274 |
| c1new | CJ274 |
| c2n | CE142 |
| c3-low | RF193 |
| c3-lowcounterexample | CE155 |
| c3-pgd | RF180 |
| c3-upper | LM168 |
| c4 | CJ170 |
| c6-prime | TH331 |
| c6g3 | RF237 |
| c_n=1/(s0+d+b+2)! | RF183 |
| cal | CJ130 |
| calibration | CJ302 |
| cancellationchainssurvivecommonsigma-hat^2 | TH187 |
| cancellationmaskinguntouchedby(c) | TH185 |
| cap-freelatticeandexactcount | RF175 |
| capneedsl>=a+d | RF170 |
| capped-scancertificationinterface | CJ322 |
| capped_mpm_min_riskh | TH430 |
| capwitnessn=8p=7k=4 | CE140 |
| card_le_of_mem_rad | TH455 |
| ce-h24 | CE144 |
| ce1 | CE144 |
| ce1-narrow | CE145 |
| ce101 | CE101 |
| ce102 | CE102 |
| ce103 | CE103 |
| ce104 | CE104 |
| ce105 | CE105 |
| ce106 | CE106 |
| ce107 | CE107 |
| ce108 | CE108 |
| ce109 | CE109 |
| ce110 | CE110 |
| ce121 | CE111 |
| ce122 | CE112 |
| ce123 | CE113 |
| ce124 | CE114 |
| ce125 | CE115 |
| ce141 | CE116 |
| ce142 | CE117 |
| ce143 | CE118 |
| ce144 | CE119 |
| ce145 | CE120 |
| ce146 | CE121 |
| ce147 | CE122 |
| ce161 | CE123 |
| ce162 | CE124 |
| ce163 | CE125 |
| ce164 | CE126 |
| ce165 | CE127 |
| ce166 | CE128 |
| ce167 | CE129 |
| ce168 | CE130 |
| ce169 | CE131 |
| ce170 | CE132 |
| ce181 | CE133 |
| ce182 | CE134 |
| ce183 | CE135 |
| ce184 | CE136 |
| ce185 | CE137 |
| ce186 | CE138 |
| ce187 | CE139 |
| ce188 | CE140 |
| ce189 | CE141 |
| ce190 | CE142 |
| ce191 | CE143 |
| ce1asymptoticsketch | CJ187 |
| ce2 | CE146 |
| ce201 | CE144 |
| ce202 | CE145 |
| ce203 | CE146 |
| ce204 | CE147 |
| ce205 | CE148 |
| ce206 | CE149 |
| ce207 | CE150 |
| ce208 | CE151 |
| ce209 | CE152 |
| ce210 | CE153 |
| ce211 | CE154 |
| ce212 | CE155 |
| ce213 | CE156 |
| ce221 | CE157 |
| ce222 | CE158 |
| ce223 | CE159 |
| ce224 | CE160 |
| ce225 | CE161 |
| ce226 | CE162 |
| ce227 | CE163 |
| ce228 | CE164 |
| ce229 | CE165 |
| ce230 | CE166 |
| ce231 | CE167 |
| ce232 | CE168 |
| ce233 | CE169 |
| ce234 | CE170 |
| ce235 | CE171 |
| ce236 | CE172 |
| ce237 | CE173 |
| ce238 | CE174 |
| ce241 | CE175 |
| ce242 | CE176 |
| ce243 | CE177 |
| ce244 | CE178 |
| ce245 | CE179 |
| ce261 | CE180 |
| ce262 | CE181 |
| ce263 | CE182 |
| ce264 | CE183 |
| ce265 | CE184 |
| ce266 | CE185 |
| ce267 | CE186 |
| ce268 | CE187 |
| ce269 | CE188 |
| ce281 | CE189 |
| ce282 | CE190 |
| ce283 | CE191 |
| ce284 | CE192 |
| ce285 | CE193 |
| ce286 | CE194 |
| ce287 | CE195 |
| ce288 | CE196 |
| ce2targetform | RF184 |
| ce301 | CE197 |
| ce302 | CE198 |
| ce303 | CE199 |
| ce304 | CE200 |
| ce305 | CE201 |
| ce306 | CE202 |
| ce307 | CE203 |
| ce308 | CE204 |
| ce309 | CE205 |
| ce310 | CE206 |
| ce321 | CE207 |
| ce322 | CE208 |
| ce323 | CE209 |
| ce324 | CE210 |
| ce325 | CE211 |
| ce341 | CE212 |
| ce342 | CE213 |
| ce343 | CE214 |
| ce344 | CE215 |
| ce345 | CE216 |
| ce346 | CE217 |
| ce347 | CE218 |
| ce348 | CE219 |
| ce349 | CE220 |
| ce361 | CE221 |
| ceiling | TH423 |
| ceiling_sharp | TH425 |
| certificationslow,scoringnot | TH170 |
| certifiedrepairgivess-hat=s0 | LM144 |
| cex-1 | CE133 |
| cex-2 | CE135 |
| cex-essneutral(a3) | CE168 |
| cex-exitloss(a3) | CE166 |
| cex-guard | CE175 |
| cex-localmax(a2) | CE143 |
| cex-mbbmc(a3) | CE165 |
| cex-mbquad(a3) | CE164 |
| cex-nmremainder(a4) | CE209 |
| cex-shrare(a3) | CE167 |
| cex1 | RF101 |
| cex2 | CE135 |
| cf(1)instancesnotmasked | CE174 |
| cf(c) | CJ195 |
| cf-compat | CJ195 |
| chainon{2,1,0} | CE146 |
| chainrule | LM159 |
| chatterjee-diaconisexp(kl)scale | LM230 |
| chebyshevcoolingschedule | CJ284 |
| cj101 | CJ101 |
| cj102 | CJ102 |
| cj103 | CJ103 |
| cj104 | CJ104 |
| cj105 | CJ105 |
| cj106 | CJ106 |
| cj107 | CJ107 |
| cj108 | CJ108 |
| cj109 | CJ109 |
| cj110 | CJ110 |
| cj111 | CJ111 |
| cj112 | CJ112 |
| cj113 | CJ113 |
| cj114 | CJ114 |
| cj115 | CJ115 |
| cj116 | CJ116 |
| cj117 | CJ117 |
| cj118 | CJ118 |
| cj119 | CJ119 |
| cj120 | CJ120 |
| cj121 | CJ121 |
| cj122 | CJ122 |
| cj123 | CJ123 |
| cj124 | CJ124 |
| cj125 | CJ125 |
| cj126 | CJ126 |
| cj127 | CJ127 |
| cj128 | CJ128 |
| cj129 | CJ129 |
| cj130 | CJ130 |
| cj131 | CJ131 |
| cj132 | CJ132 |
| cj133 | CJ133 |
| cj134 | CJ134 |
| cj135 | CJ135 |
| cj136 | CJ136 |
| cj137 | CJ137 |
| cj138 | CJ138 |
| cj161 | CJ139 |
| cj162 | CJ140 |
| cj163 | CJ141 |
| cj164 | CJ142 |
| cj165 | CJ143 |
| cj166 | CJ144 |
| cj167 | CJ145 |
| cj168 | CJ146 |
| cj169 | CJ147 |
| cj170 | CJ148 |
| cj171 | CJ149 |
| cj172 | CJ150 |
| cj173 | CJ151 |
| cj174 | CJ152 |
| cj191 | CJ153 |
| cj192 | CJ154 |
| cj193 | CJ155 |
| cj194 | CJ156 |
| cj195 | CJ157 |
| cj196 | CJ158 |
| cj197 | CJ159 |
| cj198 | CJ160 |
| cj199 | CJ161 |
| cj200 | CJ162 |
| cj201 | CJ163 |
| cj202 | CJ164 |
| cj203 | CJ165 |
| cj204 | CJ166 |
| cj205 | CJ167 |
| cj206 | CJ168 |
| cj207 | CJ169 |
| cj221 | CJ170 |
| cj222 | CJ171 |
| cj223 | CJ172 |
| cj224 | CJ173 |
| cj225 | CJ174 |
| cj226 | CJ175 |
| cj227 | CJ176 |
| cj228 | CJ177 |
| cj229 | CJ178 |
| cj230 | CJ179 |
| cj251 | CJ180 |
| cj252 | CJ181 |
| cj253 | CJ182 |
| cj254 | CJ183 |
| cj255 | CJ184 |
| cj256 | CJ185 |
| cj257 | CJ186 |
| cj258 | CJ187 |
| cj259 | CJ188 |
| cj281 | CJ189 |
| cj282 | CJ190 |
| cj283 | CJ191 |
| cj284 | CJ192 |
| cj285 | CJ193 |
| cj286 | CJ194 |
| cj287 | CJ195 |
| cj288 | CJ196 |
| cj289 | CJ197 |
| cj290 | CJ198 |
| cj291 | CJ199 |
| cj292 | CJ200 |
| cj293 | CJ201 |
| cj294 | CJ202 |
| cj295 | CJ203 |
| cj296 | CJ204 |
| cj297 | CJ205 |
| cj298 | CJ206 |
| cj299 | CJ207 |
| cj311 | CJ208 |
| cj312 | CJ209 |
| cj313 | CJ210 |
| cj314 | CJ211 |
| cj315 | CJ212 |
| cj316 | CJ213 |
| cj317 | CJ214 |
| cj318 | CJ215 |
| cj319 | CJ216 |
| cj341 | CJ217 |
| cj342 | CJ218 |
| cj343 | CJ219 |
| cj344 | CJ220 |
| cj345 | CJ221 |
| cj371 | CJ222 |
| cj372 | CJ223 |
| cj373 | CJ224 |
| cj374 | CJ225 |
| cj375 | CJ226 |
| cj376 | CJ227 |
| cj377 | CJ228 |
| cj378 | CJ229 |
| cj379 | CJ230 |
| cj380 | CJ231 |
| cj381 | CJ232 |
| cj382 | CJ233 |
| cj383 | CJ234 |
| cj384 | CJ235 |
| cj385 | CJ236 |
| cj386 | CJ237 |
| cj387 | CJ238 |
| cj388 | CJ239 |
| cj389 | CJ240 |
| cj390 | CJ241 |
| cj391 | CJ242 |
| cj392 | CJ243 |
| cj393 | CJ244 |
| cj394 | CJ245 |
| cj395 | CJ246 |
| cj396 | CJ247 |
| cj397 | CJ248 |
| cj401 | CJ249 |
| cj402 | CJ250 |
| cj403 | CJ251 |
| cj404 | CJ252 |
| cj405 | CJ253 |
| cj406 | CJ254 |
| cj407 | CJ255 |
| cj408 | CJ256 |
| cj409 | CJ257 |
| cj410 | CJ258 |
| cj411 | CJ259 |
| cj412 | CJ260 |
| cj413 | CJ261 |
| cj414 | CJ262 |
| cj415 | CJ263 |
| cj416 | CJ264 |
| cj417 | CJ265 |
| cj418 | CJ266 |
| cj419 | CJ267 |
| cj420 | CJ268 |
| cj421 | CJ269 |
| cj422 | CJ270 |
| cj423 | CJ271 |
| cj424 | CJ272 |
| cj425 | CJ273 |
| cj431 | CJ274 |
| cj432 | CJ275 |
| cj433 | CJ276 |
| cj434 | CJ277 |
| cj435 | CJ278 |
| cj436 | CJ279 |
| cj437 | CJ280 |
| cj438 | CJ281 |
| cj461 | CJ282 |
| cj462 | CJ283 |
| cj463 | CJ284 |
| cj464 | CJ285 |
| cj465 | CJ286 |
| cj466 | CJ287 |
| cj467 | CJ288 |
| cj468 | CJ289 |
| cj469 | CJ290 |
| cj470 | CJ291 |
| cj471 | CJ292 |
| cj472 | CJ293 |
| cj473 | CJ294 |
| cj474 | CJ295 |
| cj475 | CJ296 |
| cj476 | CJ297 |
| cj477 | CJ298 |
| cj478 | CJ299 |
| cj479 | CJ300 |
| cj480 | CJ301 |
| cj481 | CJ302 |
| cj482 | CJ303 |
| cj483 | CJ304 |
| cj484 | CJ305 |
| cj485 | CJ306 |
| cj486 | CJ307 |
| cj487 | CJ308 |
| cj488 | CJ309 |
| cj489 | CJ310 |
| cj490 | CJ311 |
| cj491 | CJ312 |
| cj492 | CJ313 |
| cj493 | CJ314 |
| cj494 | CJ315 |
| cj495 | CJ316 |
| cj496 | CJ317 |
| cj497 | CJ318 |
| cj498 | CJ319 |
| cj499 | CJ320 |
| cj500 | CJ321 |
| cj501 | CJ322 |
| cj502 | CJ323 |
| cj503 | CJ324 |
| cj504 | CJ325 |
| cj505 | CJ326 |
| cj506 | CJ327 |
| cl(l)=>t27(i) | TH142 |
| cl(l)ratiolaw | TH141 |
| cl(sqrt(logn))witheta=1onexact-zero-leakagelh | CE120 |
| claimthatt03-sharp(iii)p(s_dagger!=s0)<=2e0[1-pi(s0)]isanewcontribution | RF130 |
| classificationofthe2,400fits | CJ223 |
| closed-classdelivery | TH264 |
| clusterrepresentation | TH342 |
| co-blocking | TH157 |
| coh | CJ130 |
| combinationlook-alike | CE134 |
| commonplug-insigma^2inflateseverynull | LM132 |
| commonplug-insigma^2istherighttoolforthen=200dilutionmasking(o-mix1/10) | RF150 |
| comparisonlemma | LM171 |
| comparisonwithsong-liangs6 | TH414 |
| compositiontheoremforthereportedhpm | TH115 |
| conc | LM121 |
| concurrentislandsbitwise | TH394 |
| conditionalconcentration | TH116 |
| conditionalevidenceboundsthroughacrossing | TH118 |
| conditionalindependenceofterminaltrajectories | TH228 |
| conditionalrepair | TH114 |
| conditioningoncompletion | RF221 |
| conditioningoncompletioncounterexample | CE156 |
| confidencecards(writtenbeforea-rev1/a-rev2) | CJ311 |
| conj.dm-asy | CJ153 |
| conjecture4.3 | CJ199 |
| conjectureb'(w5-faviid) | CJ154 |
| conjecturedm-asy | CJ153 |
| conjecturef2-iid | CJ201 |
| conjecturem-s0=o(logn)underse_watallsizes<=k | CJ132 |
| conservativeterminalrepairwithafixedextra-variablebudget | CJ107 |
| conservativeworking-setboundswithexplicitrewardtargets | CJ106 |
| contingency | CJ119 |
| contractionwithoutbeta-min | TH104 |
| contrastreduction | TH101 |
| contrastreductionandmixed-ratetransfer | TH121 |
| cor.a(w2-prem) | TH236 |
| cor.b-m | TH223 |
| cor.b-unif | TH222 |
| cor.b1-lh | TH287 |
| cor.d2-lh | TH269 |
| cor.e1 | TH172 |
| cor.e2 | TH173 |
| cor.n1 | TH175 |
| cor.p1 | TH224 |
| cor.p1atproductionb | CJ188 |
| cor.ws-w' | TH363 |
| cora-prem | TH236 |
| corb-m | TH223 |
| corb-unif | TH222 |
| corc5 | TH330 |
| corgu-lh | TH389 |
| corollariese1ae1be1c | TH308 |
| corollary1 | LM127 |
| corollary2 | TH373 |
| corollary2.1(o-swap) | TH338 |
| corollarya | TH236 |
| corollaryb | TH163 |
| corollaryb-m | TH223 |
| corollaryb-unif | TH222 |
| corollaryb1-lh | TH287 |
| corollarybg1' | TH256 |
| corollarybg1-∞ | TH255 |
| corollaryc | TH164 |
| corollaryc1(w5-faviid) | TH195 |
| corollaryc2(w5-faviid) | TH196 |
| corollaryc3(w5-faviid) | TH197 |
| corollaryc5 | TH330 |
| corollaryconf-run | TH271 |
| corollaryd2-inf | TH242 |
| corollaryd2-lh | TH269 |
| corollaryd5 | TH249 |
| corollarye1 | TH172 |
| corollarye2 | TH173 |
| corollaryf3 | TH265 |
| corollaryfixed-pbg3/lh-lockon(cert) | TH276 |
| corollarygu-lh | TH389 |
| corollaryn1 | TH175 |
| corollarynt | LM149 |
| corollaryp1 | TH224 |
| corollaryp3-prime | TH314 |
| corollaryr' | TH304 |
| corollaryr1 | TH137 |
| corollaryt32(c) | TH294 |
| corollaryt32(c)corrected | CJ208 |
| corollaryt32(i-lit) | TH294 |
| corollaryt33-nf | TH344 |
| corollaryuprime | TH403 |
| corollaryv | TH398 |
| corollaryw-r | TH396 |
| corp1 | TH224 |
| corp2' | TH206 |
| corp6 | TH209 |
| corp6repairedcomposition | TH212 |
| correctedundoclassification | TH227 |
| correlation0.65 | CE101 |
| cort05-r1 | LM106 |
| cort05-shat | TH133 |
| cort05-u-infinity | TH132 |
| coru' | TH403 |
| corv | TH398 |
| corw' | TH210 |
| corw'(bofavourable) | TH367 |
| corw-r | TH396 |
| corw‴(correctedw″) | TH369 |
| cost-t38 | TH289 |
| costclaim | CJ164 |
| costcorollaryoftheorem5 | TH289 |
| counterexamplec0 | CE157 |
| counterexamplec1 | CE158 |
| counterexamplecandidateto"guarantees=>sequential" | CE212 |
| cover | CJ124 |
| cover(w,eps_c) | CJ124 |
| cross-blockcovarianceterm | CJ258 |
| cross-familyleanfidelityincomplete | RF284 |
| csvdv(2.2)violated(lit-statsection6) | LM107 |
| cumulantfunctionofd | LM210 |
| cumulativescoringhazard | TH257 |
| cutoffm#_n | LM102 |
| d1 | TH244 |
| d1(c) | RF271 |
| d1(thm-synth) | TH414 |
| d1(thm-synththeoremdprecursor) | TH399 |
| d18 | CE103 |
| d1api-posversuslit-mcmc | CJ301 |
| d2 | CE103 |
| d2(t38-recordpartiv) | CJ215 |
| d2(thm-synth) | TH415 |
| d2-dproof | TH159 |
| d2-infinity | TH242 |
| d2-instance | CJ196 |
| d2-lh | TH269 |
| d2-∞ | TH242 |
| d2atgibbsdistance>=2 | CJ148 |
| d2coversone-cancellationmaskingincludingp>>sqrt(n)(cf(1)instances) | RF214 |
| d2onlh-iidc=1 | TH154 |
| d2route | TH285 |
| d2statisticalinstance | CJ196 |
| d3 | TH245 |
| d3(b)) | RF271 |
| d3(thm-synth) | TH416 |
| d3klbound | LM230 |
| d4(thm-synth) | TH398 |
| d9 | CJ274 |
| d_n^{sl} | TH282 |
| d_n^{sl}->0for(b1')automatic | CJ216 |
| d_s(one-stateprogressevent) | LM246 |
| d_s^lex | LM148 |
| dataagainstweak-signalmasking:l^2~50-199andcl(0)overshoot | CE131 |
| decisionpoint2d1 | CJ121 |
| decisionrulesandthesize-priorceiling | TH131 |
| deliv | CJ191 |
| deliv(x_n) | CJ191 |
| deliv-pop | CJ217 |
| deliveryinclusion | LM145 |
| deliveryofaneligibleparticle | CJ191 |
| deliveryofoutput | CJ212 |
| deliveryofoutputp(u)->0 | CJ300 |
| delta-hat_1~0.99(1-pi0(s0))atn>=3200 | RF163 |
| deltaidentity | LM198 |
| den' | LM103 |
| den-prime | LM103 |
| denominatorlemmabeforethes0priorbound | LM103 |
| dep,nb',pi0(x°)>1/10onamaskedfamily | CJ196 |
| departurefromthetruth | LM199 |
| depth=stagecountwithouttheper-roundfactor | RF269 |
| depth=tstages | RF269 |
| depthfreeofn,handrforv3.1(propdclause | RF271 |
| depthwithparticle-parallelislands | TH399 |
| designconditions | TH210 |
| determinant-onlyse | CJ133 |
| determinantratio | LM110 |
| dichotomies | TH301 |
| dil-dm | TH178 |
| dil-dmasy | CJ153 |
| dil-dp | TH177 |
| dil-e | TH171 |
| dil-e1 | TH172 |
| dil-e1(sharedrow) | TH173 |
| dil-lw | LM132 |
| dil-n | LM131 |
| dil-n1 | TH175 |
| dil-r | TH174 |
| dil-s | TH176 |
| dilthreshold | TH147 |
| dilutionmasking | TH158 |
| dilutionremovedexactlyunderbo | TH183 |
| dimensioncontrol | TH102 |
| dimensioncontrolandstrictsupersets(lockedform) | TH122 |
| discoverygap | CJ288 |
| discoveryhalfforlogp=o(n) | CJ147 |
| discrepancyrangebound(n+k)log(n+1),the'1e17'cutoff,andgap-onlystiff(t23-r) | RF114 |
| displayedprop.2eventidentity | RF242 |
| displayedridgeidentity | RF209 |
| distance-onescoring | TH224 |
| dm(i)size-signcounterexample | CE123 |
| dm(i)sizesign | RF149 |
| doesthetrueposteriorneedm-s0~s0logpundergandr | CJ131 |
| dom | CJ198 |
| dominationcondition | CJ198 |
| domvisible-hubswapcounterexample | CE171 |
| domvoidforc=1 | RF207 |
| draftapproximationerror | CJ252 |
| draftconvergenceofe[h(theta)]estimates | CJ254 |
| draftnaiveunionmergedistortsuncertainty | CJ253 |
| draftpartitionasarandomvariable | CJ255 |
| draftprop1mhexactness | CJ249 |
| draftprop2smcconsistency | CJ250 |
| draftsection5.3premiseforv3tables | RF256 |
| draftweightstabilityunderweakcross-blockdependence | CJ251 |
| draw_pi0exactstartsampler | TH410 |
| driftform | TH221 |
| driftwithstate-averagedrates | CJ182 |
| drop_two_swap | LM244 |
| dropped.md(lf) | RF106 |
| dropped.mdcouncilandreviewgroup | RF118 |
| dropped.mdjudgeur/uaitems | RF117 |
| ds_move | LM246 |
| dup | CJ130 |
| duplicatecolumnsx1=x2 | CE136 |
| duplicatedcolumnscounterexample | CE111 |
| duplicatedpredictorsacrossblocks | CE106 |
| dx | CJ130 |
| e1 | LM101 |
| e1(a-rev8) | CE177 |
| e1-t38e | TH246 |
| e1two-phasesandwich | TH308 |
| e2 | LM102 |
| e2missbound | TH309 |
| e3 | TH310 |
| e3' | TH240 |
| e3(ii) | RF188 |
| e3(ii)counterexample | CE150 |
| e3(ii)p=2counterexample | CE161 |
| e3(ii)withoutq<1 | RF188 |
| e3(ls0eligibility) | TH240 |
| e3-core | TH243 |
| e3-t03 | TH126 |
| e4evidencedichotomy | TH311 |
| e4resolvedhalf | CJ218 |
| e4tie-dpinvariant | CJ209 |
| e[z-hat/completed]=z | RF227 |
| e[z_rpip_rj]=zpip_j | TH297 |
| e[zhat/completed]=z | RF221 |
| e_lsledgerdatafact | CJ222 |
| ee^{(1+r)z^2/2}<inf | RF260 |
| eexp(z^2/2)isinfinite | CE204 |
| effective-truthpotentialformaskeddesigns | CJ173 |
| eligibility | TH152 |
| ell-formoft13 | TH360 |
| els-1 | CJ222 |
| els-2 | CJ223 |
| els-3 | CJ224 |
| els-4 | CJ225 |
| emit_centre | CJ128 |
| engineerror_bound()isabound | RF244 |
| enlargedclassw+ | RF210 |
| envelopetheorem | TH248 |
| eq | CE151 |
| equalityindicatorh=1{theta_j=theta*_j} | CE185 |
| equicorrelatedinflation1.86 | RF190 |
| equicorrelatednulls | CE138 |
| equicorrelatednullscounterexample | CE151 |
| erccontrolsnullleakage | LM152 |
| errorb5 | RF125 |
| esssharelemma | LM170 |
| eta*(d) | TH206 |
| eta_freplay | CJ238 |
| everypolynomialbudgetfails | RF263 |
| everyreportedoutputequalsr-bar's | RF215 |
| evidence-weightedpipbound | TH300 |
| evidencecollapseonnon-crossingrealisations | TH305 |
| evidencelossundercalibrationavoidanceandevidencecoupling | CJ109 |
| evidencelowertail | CJ190 |
| evidenceo_p(sqrt(t/n))whenthegridresolvesthecrossing | CJ218 |
| ex-a | CJ130 |
| ex-s | CJ130 |
| exactbeta-binomialsizetail | TH125 |
| exactbetalawforanygroup-union | LM138 |
| exactbetalawsofstartstatistics | LM116 |
| exactblockfactorisationofthestart | TH171 |
| exactbranch | CE106 |
| exactbranchatp=18,n=2^18 | CE180 |
| exactdecompositionoftheexp'remainder | LM111 |
| exactdilutionform | LM212 |
| exactlarge-pnumericsvsf-draftw(c) | CE197 |
| exactlawof#truths/#nullsunderpi0 | TH174 |
| exactly/sdeltas0/moves | RF181 |
| exactpairrefresh | TH310 |
| exactrelativecertificatesonfullyscoredregions | TH328 |
| exactrepresentationunderorth | LM106 |
| exactstart | TH107 |
| exacttail | LM101 |
| exactties | TH105 |
| exactvarianceidentity | TH316 |
| excess_riskh_le | TH434 |
| exec | CJ130 |
| exists_bestimprovement | LM242 |
| exists_bestimprovementdocstringoverclaim | RF287 |
| exists_capped | LM240 |
| exists_isleastargmax | LM256 |
| exit-losssimplification | RF204 |
| exit_d | RF185 |
| exit_dasinternal-changecontrol | RF117 |
| exit_dresolution | TH227 |
| exitboundforthesupersetclass | LM182 |
| exp | CJ121 |
| exp' | CJ121 |
| exp'appliesatthestudysizeviakappa_exp | RF137 |
| exp'remaindercertificate | TH137 |
| exp-const | RF134 |
| exp-const(lemmaupart) | RF189 |
| exp-prime | CJ121 |
| exp-primetheorem | TH136 |
| exp3 | CE134 |
| expectation-conventioncounterexamples(a-rev4,a-rev6) | CE186 |
| expectationroutetotheoremw | RF260 |
| expected-f1 | RF119 |
| explicitc0(s0,a)andfirst-ntable | CJ134 |
| explicitfamilycf(c) | CJ195 |
| explicitfirst-hitclauseforstandalonea3statements | CJ321 |
| explicitgrowing-psubfamily | TH275 |
| explicitsequencep=ceil(n^{1/3}) | CE145 |
| explicitsplitfamily | TH307 |
| exponential-familyidentitiesforthebridge | TH348 |
| extrascountacrossresampling | CJ199 |
| f' | LM163 |
| f(s°)>sup_{r_d^c}f | RF197 |
| f-draftconjecturewprime | CJ257 |
| f-draftconjecturew″windowform | CJ260 |
| f-draftd(s0)boformulaasfinite-npredictor | RF162 |
| f-draftlemmaw1 | TH350 |
| f-draftlemmaw2exactidentitywithpartialr^2 | RF254 |
| f-draftlemmaw3 | CJ258 |
| f-draftmethodnoteplug-insigma^2tables | CJ273 |
| f-draftnm | RF265 |
| f-draftpropnm | RF265 |
| f-draftpropositionp | TH375 |
| f-draftpropositionw4 | CJ259 |
| f-draftremarkh | TH324 |
| f-drafttheoremw | CJ256 |
| f-drafttheoremw(b)divergentside | RF253 |
| f-drafttheoremw(c)divergentside | RF252 |
| f-draftw″o(1)stages | RF255 |
| f-draftw″two-statepart | TH377 |
| f-maskpipcorollarym2 | TH301 |
| f-maskpipcorollaryr-prime | TH304 |
| f-maskpipm3printedinstance | RF229 |
| f-maskpippropositionm1 | TH300 |
| f-maskpippropositionm3 | TH302 |
| f-maskpippropositionn(a) | TH305 |
| f-maskpippropositionn(b) | TH306 |
| f-maskpippropositionn(c) | TH307 |
| f-maskpiptheoremr | TH303 |
| f-refereem1(jrss-brefereesimulation,majorpoint) | CJ303 |
| f-refereem2(jrss-brefereesimulation,majorpoint) | CJ304 |
| f-refereem3(jrss-brefereesimulation,majorpoint) | CJ305 |
| f-refereem4(jrss-brefereesimulation,majorpoint) | CJ306 |
| f-refereem5(jrss-brefereesimulation,majorpoint) | CJ307 |
| f-refereem6(jrss-brefereesimulation,majorpoint) | CJ308 |
| f-refereem7(jrss-brefereesimulation,majorpoint) | CJ309 |
| f-refereem8(jrss-brefereesimulation,majorpoint) | CJ310 |
| f-refine:theoremw(regionformr_{a,d})coversthemaskedfamilies/isthegeneralsufficientconditionfor(m2) | RF279 |
| f-refine:withoutls0thepaperhasnomasked-regimeconsistencytheorem | RF280 |
| f-refinecard3(i) | RF188 |
| f-refinecards/architecture | CJ311 |
| f1b_swap_margins | CE173 |
| f2(lhclosedsupersetclass) | TH266 |
| f2-iid | CJ201 |
| f=0.05,e=0.9 | CE162 |
| factf | LM202 |
| factor-nerror | CE105 |
| factorialconstant | RF183 |
| failed_attempts.md | RF119 |
| failurepartitioni/ii/iii | TH200 |
| fairbitsconditionedequal | CE156 |
| familydefect | RF192 |
| familydefectcounterexample | CE153 |
| familydefectonlh | CE153 |
| familyf″(u+x)=x^-a,aupto2(t*vspathlength) | CE205 |
| fav-c1 | TH195 |
| fav-c2 | TH196 |
| fav-c3 | TH197 |
| fav-conjbp | CJ154 |
| fav-lemmabp | LM138 |
| fav-lemmag | LM142 |
| fav-lemmam | LM140 |
| fav-lemmap1p | LM143 |
| fav-lemmas | LM141 |
| fav-lemmatrp | LM139 |
| fav-lemmax | LM136 |
| fav-lemmaxminus | LM137 |
| fav-plugin | CJ156 |
| fav-propb1 | TH193 |
| fav-propf | TH194 |
| fav-propn | TH192 |
| fav-sharp | CJ155 |
| fav-thma | TH190 |
| fav-thmb | TH191 |
| favourablefromn~800-1,600(andothersinglethresholds) | RF160 |
| favourableregime | TH283 |
| favourableregimebo | TH138 |
| favourablesandwich | TH366 |
| favplug-inthresholds | CJ156 |
| favsharpfirstorder | CJ155 |
| fd-h | TH324 |
| fd-nm | RF265 |
| fd-p | TH375 |
| fd-w'idealgridstagecount | CJ257 |
| fd-w(a) | CJ256 |
| fd-w(b) | CJ256 |
| fd-w(c) | CJ256 |
| fd-w0 | TH359 |
| fd-w1 | TH350 |
| fd-w2 | RF254 |
| fd-w3 | CJ258 |
| fd-w4 | CJ259 |
| fd-w″-two | TH377 |
| fd-w″-window | CJ260 |
| feasibilityofrad | TH455 |
| feasible-additionhazards | TH108 |
| finallocalsearch0moves | CJ222 |
| finalsearchfroms_preinsider | CJ278 |
| finding(ls0/emit_centre) | LM196 |
| finite-hpilotvst*_omega | CJ272 |
| finite-n | CJ302 |
| finite-ncompositiontheorem | TH334 |
| finite-ndilutionformula | TH177 |
| finite-nfailureboundfortheglobalhpm | TH132 |
| finite-ngibbs-routediscoverybound | CJ237 |
| finite-nidentitiesformarkedrbrewards | TH321 |
| finite-ntruthdominanceanddeterministicgreedyrepair | CJ117 |
| finitestepofh03=>e0delta1->0 | LM232 |
| first-changeprogress | LM166 |
| first-failurebound | LM162 |
| first-momentevidenceconsistency | TH112 |
| first-orderbracket | TH340 |
| firstexit<=eta_n | CJ120 |
| firstparallelexactbvs | RF268 |
| firstpropsnumbers10^-3..10^-6 | RF161 |
| fit-fractionformofthescore | LM209 |
| fitnessoscillationcorollary | TH249 |
| fixed-dataparticleconsistency | TH320 |
| fixed-datavalidityforanyislandcount | TH411 |
| fixed-pcomponentcorollaryon(cert) | TH276 |
| fixed-pointrule | CJ163 |
| fixed-ptwocolumnsb=sigma=1r=1/2 | CE209 |
| fixed-s0dilutionfamily | CJ140 |
| fixedcanonicalorderatphi=0isreversible(counterexampleto"afixedorderisnotself-adjoint") | CE218 |
| fixedfinale2 | RF115 |
| flagpower | CJ302 |
| flipswap_sdiff_card | LM252 |
| floating-pointerrorboundforonescore(choleskyroute) | TH343 |
| floating-pointevidenceandval-fp | TH346 |
| floating-pointinflationofthegitems | TH333 |
| floatingpoint | CJ302 |
| floodingofcommon-sigma^2variantsonthe2,400realprod-hfits(data) | CE132 |
| floorphi_1>=1/t_e | RF231 |
| fmp-delivpop | CJ217 |
| fmp-m1 | TH300 |
| fmp-m2 | TH301 |
| fmp-m3 | TH302 |
| fmp-na | TH305 |
| fmp-nb | TH306 |
| fmp-nc | TH307 |
| fmp-thmr | TH303 |
| fmp-thmrprime | TH304 |
| forcedsmccomponentonpropmfamily | TH392 |
| forwardchain | TH245 |
| frobeniusmonotonicitylemma(ws4) | LM223 |
| frozen-particleandindependent-islandlimits | CJ103 |
| frozen-runevidence | TH110 |
| frozen_list/fable_reviewpremise:bb(1,p)ratioisaboutk/2p,not1/2 | RF122 |
| frozensecondpremise(l_n+4)rho*_n->0 | RF235 |
| fs | TH234 |
| fs/tl#/ulr | TH234 |
| fsh-c4.3 | CJ199 |
| fsh-domc1 | RF207 |
| fsh-f1 | TH264 |
| fsh-f1' | CJ200 |
| fsh-f2 | TH266 |
| fsh-f2iid | CJ201 |
| fsh-f3 | TH265 |
| fsh-l1.2 | LM182 |
| fsh-l3.1 | LM183 |
| fsh-l3.2 | LM184 |
| fsh-l3.3 | LM185 |
| fsh-l3.4 | LM186 |
| fsh-pk | CJ197 |
| fsh-rareoutsider | RF205 |
| fsh-retention | RF206 |
| fsh-s4 | TH267 |
| fsh-t38b2 | TH267 |
| full-outputexpectatione[1_oz-hat]<=zp(a) | RF232 |
| full-spacecoverage | CJ124 |
| full-spaceessgridcannotjumpacrossing | LM203 |
| fw13 | CJ212 |
| fw18 | CJ135 |
| fw19 | CJ135 |
| fw21 | CJ274 |
| g | CJ130 |
| g=4,rho=0.85,psi=0.5 | CE170 |
| g=9,c=2,rho=0.4,psi=0.2 | TH275 |
| g>b(g=15,16atn=200,b=14) | CE117 |
| gain_d | RF185 |
| gapclaim | CJ282 |
| gateobstruction | TH252 |
| gaussiancorrelationconcentration | LM121 |
| generalh(theta) | TH324 |
| generallhlocking | RF208 |
| generalsufficientconditionfor(m2) | RF176 |
| generating-valueconsistencyundercontinuity | TH323 |
| geometric-meaneigenvaluecondition | CJ133 |
| geometricsizetilt(lit-statsection12) | LM108 |
| geometrictail2^-mreplacedbyexactbb(1,p)tail | RF103 |
| gerc+trcimpliespgd | TH205 |
| gercremarks | TH205 |
| gfm | RF119 |
| gibbs-pathrepair | TH218 |
| gibbs-pathroute | TH286 |
| gibbs-routerestatement | CJ177 |
| gibbscoordinatestepreversible | TH405 |
| gl | CJ130 |
| gp(2)four-statefailure | CE160 |
| gp(d)=>td' | LM187 |
| gp(d)impliestd'(r_d,l) | LM187 |
| gp_fail_probe | CE160 |
| gram-perturbationstability | LM156 |
| greedyoptimality | TH364 |
| greedyuniversality | TH388 |
| grid-basedconditionsforshare | RF211 |
| gridstagecount | TH370 |
| groupedequicorrelatednulls | CE139 |
| growingc_n | CJ279 |
| gu-iid | TH390 |
| guard | CJ128 |
| guardcounterexample(allocationanddiagnosticsfields) | CE176 |
| guardliteral | RF215 |
| guonlh-iid | TH390 |
| guwithdata-chosennullsinthecentre | CJ277 |
| h-orth | TH362 |
| h-t02 | CJ126 |
| h-t02use | TH124 |
| h-t03 | CJ126 |
| h-t12 | CJ126 |
| h03 | CJ126 |
| h03(=t03(i)conclusion) | TH123 |
| h03asymptotics | CJ314 |
| h1 | CJ125 |
| h10 | CJ126 |
| h2 | CJ125 |
| h2/h3 | CJ125 |
| h24 | CJ120 |
| h24(asymptoticinput) | RF182 |
| h24aswritten | RF102 |
| h24exitcounterexample | CE144 |
| h24falseincorrelateddesigns(blanket) | CJ187 |
| h24inputs | CJ120 |
| h3 | CJ125 |
| h4 | CJ125 |
| halvingcount | LM218 |
| hastingsfactor | TH407 |
| headlinegaincappedat6/2,400asrationaleagainstastartchange | RF164 |
| headlineoverclaim | RF270 |
| headlinetheorem | CJ118 |
| heterogeneouslhpairs | CE122 |
| heterogeneouswithin-groupcorrelations | CJ144 |
| hit | RF120 |
| hitting/scoringtimeofs0fromconditions(1b)/(1c)aloneisnotpublished | CJ292 |
| hotelling-densitytail | LM128 |
| hpm_eq_truth | TH418 |
| hpm_min_risk01 | TH427 |
| hpmconventioncomposition | TH282 |
| hpmdecisionsandtiesonacommonscoredset | TH345 |
| hpmlossneedsscoringavoidance | CJ110 |
| hqpremise:sizepriornotmonotone,marginallikelihoodis | RF251 |
| htheavy-taillemma | LM215 |
| hub-movevariantof(b-merge) | CJ160 |
| hubgain | LM184 |
| hubgain(g) | LM180 |
| hubpairco-clusters | CE116 |
| hubvariant | CE143 |
| hypotheses-that-changelist | TH400 |
| hypothesesoft21usedasinputs | CJ126 |
| hypothesis(ll) | CJ269 |
| hypothesispair | CJ270 |
| ideal-gridsandwich | TH361 |
| identifiability | TH105 |
| identifiablecross-blockproxyp=2 | CE208 |
| iid-discoverybudget | TH119 |
| iid500cell,oraclesigma^2common-sigma-hat^2start | CE124 |
| iidmiss0.000 | CE174 |
| iidstartdiscovery | TH380 |
| iii.8 | CJ216 |
| im | TH235 |
| impl-emit | LM196 |
| impl-guard | CJ128 |
| impl-guard' | LM191 |
| impl-loop | LM197 |
| impl-ls | LM195 |
| impl-out | LM192 |
| impl-sr | LM193 |
| impl-stream | LM194 |
| impl-t | LM197 |
| implementationverification | CJ323 |
| in-samplefavourableregimeforiids1/s3/s4/s6 | CJ139 |
| in-samplefavourableregimeforiids1/s3/s4/s6designs | CJ211 |
| ind(f) | TH235 |
| ind-m | TH235 |
| ind-mforsupersetstarts | CJ185 |
| ind-t | TH228 |
| ind-tstreampremise | LM194 |
| independence-proposalbadacceptance | TH235 |
| independentgroupssharpbound | TH164 |
| independentrebuildandfullaxiomauditofthe101theorems | CJ327 |
| independentstart-to-terminalscoringtracks | CJ119 |
| inf_phiq_phi(a)>=min{pi0(a),pi(a)} | RF198 |
| initialcentreisthetruthtrivialsuccess | RF179 |
| insample-fav | CJ139 |
| integral_le_eps_add_prob | LM232 |
| integralform | LM214 |
| integratedls0 | CJ213 |
| integratedls0testfit | CJ178 |
| integratedls0testfitnotrun | CJ229 |
| interlacing | LM104 |
| internalchangeprobability1.0whilexi=0.29 | CE102 |
| invariance_step | LM248 |
| invariantkernels | TH107 |
| islandwiseevidencelowertail | CJ190 |
| islandwiseunbiasedness | TH297 |
| isleastargmax.unique | LM256 |
| isolationprobabilityofamaskedhubunderauniformequipartition(thm-synthcheck_lemmas.py) | CE214 |
| j10 | CE104 |
| j3 | CE101 |
| j4 | CE102 |
| j7 | CE105 |
| j9 | CE106 |
| jointinclusion | TH412 |
| jointinclusionprobabilities | CJ298 |
| jointlawoflambda_bacrossblocks | CJ168 |
| jointmasked-regimefamilylh | TH144 |
| jrss-bastretch | CJ296 |
| jrss-bprop1 | TH106 |
| jrss-bprop2 | TH110 |
| jrss-bthm1 | TH103 |
| jrss-bthm2 | TH116 |
| jrss-bthm3(newprimaryroute) | CJ117 |
| jrss-bthm4 | TH115 |
| jrss-bthm5 | CJ118 |
| jrss-bthm6(i)-(ii) | CJ108 |
| junkandproxyinclusionodds | LM179 |
| k1(x,{s0})>=a_n | CJ120 |
| k68(a-fav) | TH283 |
| k69 | TH287 |
| k70 | TH272 |
| k71 | TH288 |
| k72 | TH281 |
| k82 | CJ212 |
| k94 | CJ230 |
| k97 | CJ274 |
| k97draftclausecov(x_t,y)=0onisolation | RF267 |
| k98 | RF266 |
| kantorovich-1.925 | RF200 |
| kantorovichtwo-levelweights{1,1.925} | CE163 |
| kappa_17>=0.15forallsixstudycovariances | RF139 |
| kappa_2 | TH167 |
| kappa_exp->0.52/c_* | RF134 |
| kappag<=lr<=kappag/(1-y) | LM212 |
| keep(w,eta) | TH264 |
| known-cite | CJ287 |
| l+4vsl+5 | CJ177 |
| l-fm | TH112 |
| l-led | TH109 |
| l-occ | TH113 |
| l-rc | CJ104 |
| l2mixingcertification | CJ219 |
| lambda_2(a) | TH232 |
| laminarity | TH162 |
| lat(s)withoutcap | RF175 |
| lat_subset | LM250 |
| lattice-indicatorpotentialnegative | TH273 |
| latticeclosure | LM146 |
| latticeform | TH214 |
| layeredpotential(cancellation) | CJ181 |
| layeredversionoftheoremb | CJ181 |
| layerlawatgeneralw | CJ269 |
| ld-flat | LM155 |
| ld-flatstability | LM161 |
| ldexceptionalnulls | RF171 |
| leakage | CJ127 |
| leakageboundsdiscrepancy | LM113 |
| leakagedecomposition | LM211 |
| leakageformulas | TH352 |
| lean(c1) | TH422 |
| leancertificatesfortheremainingpaper-1cards | CJ325 |
| leant07ceiling | TH423 |
| leant21deterministiccore | TH418 |
| leantheorema2/theorema2_latticeasthefulla2 | RF285 |
| leantheorema3asgivingthereportedhpmaftercertifiedrepair | RF288 |
| leantheorema3underfulltdpaslemma0(c) | RF289 |
| lemma(designde-randomisation) | LM120 |
| lemma-stream | LM194 |
| lemma0(a) | TH440 |
| lemma0(a),(c) | LM144 |
| lemma0(a,c) | LM144 |
| lemma0(b') | LM145 |
| lemma0(b) | RF167 |
| lemma0(b)ande_lsrepair | CJ320 |
| lemma0(b-prime) | LM145 |
| lemma0(c)generalform | TH446 |
| lemma0(c)reported-hpmclause | TH447 |
| lemma0(o-swap) | LM208 |
| lemma0c | TH446 |
| lemma0c_hpm | TH447 |
| lemma0dataremark | CJ176 |
| lemma1(api-n200) | LM205 |
| lemma1.2 | LM182 |
| lemma2(a) | TH449 |
| lemma2(a)helpers | LM250 |
| lemma2(t37) | LM146 |
| lemma2-t37 | LM146 |
| lemma2.1 | LM178 |
| lemma2.2 | LM178 |
| lemma2a | TH449 |
| lemma3(t37) | LM147 |
| lemma3-t37 | LM147 |
| lemma3.1 | LM183 |
| lemma3.2 | LM184 |
| lemma3.3 | LM185 |
| lemma3.4 | LM186 |
| lemma3.4schurincrement | RF209 |
| lemmaa | LM172 |
| lemmaa' | LM153 |
| lemmaa-t38e | LM172 |
| lemmaa1 | LM105 |
| lemmab | LM104 |
| lemmab' | LM138 |
| lemmab-link | LM133 |
| lemmab-prime(w5-faviid) | LM138 |
| lemmab-t38e | LM173 |
| lemmabbeyond/psi/<rho | CJ142 |
| lemmac | LM165 |
| lemmac2 | LM121 |
| lemmac3 | LM121 |
| lemmacmp | LM171 |
| lemmaden' | LM103 |
| lemmae | LM167 |
| lemmae1 | LM101 |
| lemmae2 | LM102 |
| lemmaess | LM174 |
| lemmaf | LM162 |
| lemmaf' | LM163 |
| lemmaf-prime | LM163 |
| lemmag | LM142 |
| lemmagu-1 | LM224 |
| lemmagu-2 | LM225 |
| lemmai | LM104 |
| lemmai-b | LM104 |
| lemmaimpl-guard | LM191 |
| lemmaimpl-ls | LM195 |
| lemmaimpl-out | LM192 |
| lemmaimpl-sr | LM193 |
| lemmaimpl-stream | LM194 |
| lemmaimpl-t | LM197 |
| lemmaj | LM179 |
| lemmakl | LM230 |
| lemmal | LM132 |
| lemmalambda | LM210 |
| lemmald | LM155 |
| lemmals | LM189 |
| lemmals-score | LM189 |
| lemmam | LM190 |
| lemmam(w5-faviid) | LM140 |
| lemmamf | LM176 |
| lemmaml | LM140 |
| lemmamon(proposedrename) | LM204 |
| lemman | LM131 |
| lemmanparenthetical:zerotruthcorrelationimpliesindependenceof(y,x_-l) | RF153 |
| lemmant | LM149 |
| lemmao | LM164 |
| lemmaof | LM177 |
| lemmap | LM166 |
| lemmap1 | TH148 |
| lemmap1' | LM143 |
| lemmap2 | TH149 |
| lemmap5 | LM156 |
| lemmapd | LM175 |
| lemmapert | LM219 |
| lemmapsi(a) | LM237 |
| lemmapsi(a)uniqueness | LM238 |
| lemmapsi(b) | LM239 |
| lemmapsi(b)existence | LM240 |
| lemmaq | LM158 |
| lemmar | LM176 |
| lemmar1 | LM181 |
| lemmaro | LM188 |
| lemmars | LM216 |
| lemmas | LM154 |
| lemmas' | LM170 |
| lemmas(essshare) | LM170 |
| lemmas(shift) | LM169 |
| lemmas(shiftatastoppingtime) | LM169 |
| lemmas(w5-faviid) | LM141 |
| lemmas-attain | LM174 |
| lemmas-ineq | LM174 |
| lemmas0 | LM134 |
| lemmas1(f-sigma) | LM135 |
| lemmasattainmentclaim | RF187 |
| lemmasc | LM190 |
| lemmasep | LM213 |
| lemmasep' | LM214 |
| lemmasepprime | LM214 |
| lemmasnegativelowweight | CE162 |
| lemmaspositivitycounterexample | CE149 |
| lemmastightonthefulldomain | RF201 |
| lemmastream | LM194 |
| lemmat | LM148 |
| lemmat05-r | LM106 |
| lemmat33-m | LM206 |
| lemmat33-q | LM207 |
| lemmatr' | LM139 |
| lemmau | LM168 |
| lemmau(f) | LM168 |
| lemmau(u1)arithmetic | RF138 |
| lemmau-prem | LM168 |
| lemmauc3lowerbound | RF193 |
| lemmaulimit0.52/c_e | RF189 |
| lemmaulimitconstant | RF134 |
| lemmaw1 | TH350 |
| lemmaw1premisein-sampleboatn=200 | RF162 |
| lemmaw2(o-wstab) | LM212 |
| lemmaws0 | LM209 |
| lemmaws5.1 | LM211 |
| lemmax+ | LM136 |
| lemmax- | LM137 |
| lemmax-minus | LM137 |
| lemmax-plus | LM136 |
| lh-iidanalogueofnb'andb2-lh | CJ205 |
| lh-lat | TH293 |
| lh-lat-sharp | RF144 |
| lh-latalgebraneedsonly/psi/<1 | CJ143 |
| lh-latheterogeneousnon-sharpness | CE179 |
| lh-latmarginm0issharp | RF220 |
| lh-latsharpmargin | TH166 |
| lh-lock | TH261 |
| lh-lockforgeneral(rho,psi,g,c) | RF208 |
| lh-lockforp->infinity | CJ202 |
| lh-rate | TH260 |
| lhexactgram | TH144 |
| lhexacttie | CE141 |
| lhgreedy-universalityexactenumeration(386replicates,40-designstresstest) | CE207 |
| lhiidfixed-partitionsurrogate | TH145 |
| lhlock-completion(a7) | TH261 |
| lhmaskingc>=2chainofcrossingsstagecount | CJ271 |
| lhpopulationalgebra | LM114 |
| lhpremisetable | TH237 |
| lhswapcounterexampletoc2 | CE170 |
| lh/psi/>rho | CE116 |
| limitformp(shat=s0)->1-limsupp(u) | RF213 |
| limitlaw | TH143 |
| linkgraphrecoverslinkedpairs | LM133 |
| lit-mcmcg1 | CJ292 |
| lit-mcmcl1 | CJ289 |
| lit-mcmcl2 | CJ290 |
| lit-mcmcl3 | CJ291 |
| lit-mcmcob_check:r<min12of12study-likedatasets(s1/s4,n=200,pin{500,1000}) | CE215 |
| lit-mcmcpropob | TH401 |
| lit-mcmcrz_lh:exactenumerationofrandmonlh(p=16,20) | CE216 |
| lit-parg4 | CE210 |
| lit-parg4analyticsketch:song-lianglosesthemaskedvariablewheneverthesplitseparatesthelinkedpair | RF276 |
| lit-parg4numericalcounterexample | CE213 |
| lit-parnotes04:zyvrcondition1(b)likelyfailsonmaskedlhbecausetruevariablesaremarginallyweak | RF277 |
| lit-parth2 | CJ287 |
| lit-parth4 | CJ285 |
| lit-parth6 | CJ283 |
| lit-parverdicttruewithqualifications | CJ282 |
| lit-smcg1-g2 | CJ288 |
| lit-smct1 | CJ284 |
| lit-smct2 | CJ285 |
| lit-smct3 | CJ287 |
| lit-smct4 | CJ286 |
| lit-statbb(1,p)dimensionratio | LM227 |
| lit-statbb(1,p)versusbb(1,1) | LM228 |
| lit-state1andg1:nopublishedbb(1,p^u)dimension/tailbound | CJ138 |
| lit-statfirst-draftline:everybb(1,p)ratiofactorrho_iis<=1/2fori>=0 | RF131 |
| lit-statfirstdraft:nopublishedbb(1,p)/g=ntailbound,henceanewmechanism | RF281 |
| lit-stath1 | CJ294 |
| lit-stath2 | CJ293 |
| lit-statheadline4beforesection12:bb(1,p)penalisesaddedvariablesdifferentlyfrombb(1,1),sothebb(1,p)tailisanewmechanism | RF132 |
| lit-venuegapsg1-g5 | CJ295 |
| lit-venues1.3:poly-timerecoveryonlhalsofollowsfromchang-zhour>m"sinceonlhs0istheuniquelocalmode" | RF275 |
| lit-venuevenueverdict | CJ296 |
| literalt37 | CJ117 |
| literaltd(d,0)strictimpliestd'_p | RF166 |
| literaltdunsatisfiable | TH198 |
| lk_d | RF185 |
| lk_d/exit_d/gain_d | RF185 |
| lm131 | LM101 |
| lm132 | LM102 |
| lm133 | LM103 |
| lm134 | LM104 |
| lm135 | LM105 |
| lm136 | LM106 |
| lm137 | LM107 |
| lm138 | LM108 |
| lm161 | LM109 |
| lm162 | LM110 |
| lm163 | LM111 |
| lm164 | LM112 |
| lm165 | LM113 |
| lm166 | LM114 |
| lm167 | LM115 |
| lm168 | LM116 |
| lm169 | LM117 |
| lm170 | LM118 |
| lm171 | LM119 |
| lm172 | LM120 |
| lm173 | LM121 |
| lm174 | LM122 |
| lm175 | LM123 |
| lm176 | LM124 |
| lm177 | LM125 |
| lm178 | LM126 |
| lm179 | LM127 |
| lm180 | LM128 |
| lm181 | LM129 |
| lm182 | LM130 |
| lm191 | LM131 |
| lm192 | LM132 |
| lm193 | LM133 |
| lm194 | LM134 |
| lm195 | LM135 |
| lm196 | LM136 |
| lm197 | LM137 |
| lm198 | LM138 |
| lm199 | LM139 |
| lm200 | LM140 |
| lm201 | LM141 |
| lm202 | LM142 |
| lm203 | LM143 |
| lm221 | LM144 |
| lm222 | LM145 |
| lm223 | LM146 |
| lm224 | LM147 |
| lm225 | LM148 |
| lm226 | LM149 |
| lm227 | LM150 |
| lm228 | LM151 |
| lm229 | LM152 |
| lm230 | LM153 |
| lm231 | LM154 |
| lm232 | LM155 |
| lm233 | LM156 |
| lm234 | LM157 |
| lm235 | LM158 |
| lm236 | LM159 |
| lm237 | LM160 |
| lm238 | LM161 |
| lm251 | LM162 |
| lm252 | LM163 |
| lm253 | LM164 |
| lm254 | LM165 |
| lm255 | LM166 |
| lm256 | LM167 |
| lm257 | LM168 |
| lm258 | LM169 |
| lm259 | LM170 |
| lm260 | LM171 |
| lm281 | LM172 |
| lm282 | LM173 |
| lm283 | LM174 |
| lm284 | LM175 |
| lm285 | LM176 |
| lm286 | LM177 |
| lm287 | LM178 |
| lm288 | LM179 |
| lm289 | LM180 |
| lm290 | LM181 |
| lm291 | LM182 |
| lm292 | LM183 |
| lm293 | LM184 |
| lm294 | LM185 |
| lm295 | LM186 |
| lm296 | LM187 |
| lm311 | LM188 |
| lm312 | LM189 |
| lm313 | LM190 |
| lm314 | LM191 |
| lm315 | LM192 |
| lm316 | LM193 |
| lm317 | LM194 |
| lm318 | LM195 |
| lm319 | LM196 |
| lm320 | LM197 |
| lm341 | LM198 |
| lm342 | LM199 |
| lm343 | LM200 |
| lm344 | LM201 |
| lm345 | LM202 |
| lm346 | LM203 |
| lm371 | LM204 |
| lm372 | LM205 |
| lm373 | LM206 |
| lm374 | LM207 |
| lm375 | LM208 |
| lm401 | LM209 |
| lm402 | LM210 |
| lm403 | LM211 |
| lm404 | LM212 |
| lm405 | LM213 |
| lm406 | LM214 |
| lm407 | LM215 |
| lm408 | LM216 |
| lm409 | LM217 |
| lm410 | LM218 |
| lm411 | LM219 |
| lm412 | LM220 |
| lm413 | LM221 |
| lm414 | LM222 |
| lm415 | LM223 |
| lm431 | LM224 |
| lm432 | LM225 |
| lm461 | LM226 |
| lm462 | LM227 |
| lm463 | LM228 |
| lm464 | LM229 |
| lm465 | LM230 |
| lm491 | LM231 |
| lm492 | LM232 |
| lm493 | LM233 |
| lm494 | LM234 |
| lm495 | LM235 |
| lm496 | LM236 |
| lm497 | LM237 |
| lm498 | LM238 |
| lm499 | LM239 |
| lm500 | LM240 |
| lm501 | LM241 |
| lm502 | LM242 |
| lm503 | LM243 |
| lm504 | LM244 |
| lm505 | LM245 |
| lm506 | LM246 |
| lm507 | LM247 |
| lm508 | LM248 |
| lm509 | LM249 |
| lm510 | LM250 |
| lm511 | LM251 |
| lm512 | LM252 |
| lm513 | LM253 |
| lm514 | LM254 |
| lm515 | LM255 |
| lm516 | LM256 |
| local-searchsemantics | TH114 |
| local-to-globalablation | CJ166 |
| local/fardecomposition | LM155 |
| locationoftheexact-tailcutoff | LM102 |
| lockbook-exactexp(a6) | RF232 |
| locked_proofs/theory_prioritieswordingoft06(i):twomodelstieexactlyifftheirprojectionmatrices(x_sx_s-prime)agree | RF133 |
| lockedstartset+terminaldownhill | TH258 |
| lockedt03 | TH123 |
| ls-score | LM189 |
| ls-scoremove-countcounterexample | CE177 |
| ls-scoremovecount | RF216 |
| ls0-1 | CJ226 |
| ls0-2 | CJ227 |
| ls0-3 | CJ228 |
| ls0-4 | CJ178 |
| ls0-emit | CJ178 |
| ls0cost | CJ228 |
| ls0cost+1 | TH169 |
| ls0eligibility | TH243 |
| ls0headlineversusno-ls0headline | CJ215 |
| ls0intheproductioncore | CJ213 |
| ls0posthocoutcome-neutral | CJ226 |
| ls0route | TH284 |
| ls0scoresandcertifiess0 | TH153 |
| lt | CJ190 |
| lyapunovversion | CJ182 |
| m-star | CJ207 |
| m0# | TH166 |
| m0-sharp | TH166 |
| m0belowtruemargin | CE122 |
| m1 | TH300 |
| m2 | TH301 |
| m3 | TH302 |
| m3repairedinstance(a-rev9) | CE184 |
| m8 | CJ274 |
| m_n=s0+o(s0logn/logp) | RF103 |
| ma-corv | TH398 |
| ma-corwr | TH396 |
| ma-lemmas | LM226 |
| ma-propd | TH399 |
| ma-propp | TH397 |
| ma-propw | TH394 |
| ma-wcal | TH395 |
| margins_grid | CE122 |
| markov_half | TH421 |
| markovatlevel1/2 | TH421 |
| martin-mess-walker2017notread | CJ138 |
| masked-regimepip/evidenceguaranteesforunmodifiedv3 | CJ220 |
| maskedstart=lowpersistence(woodard-schmidler-huber2009) | CJ288 |
| maskedtwo-statecrossing | TH368 |
| maskedweights | TH357 |
| maskinglaw | TH119 |
| maskinglimitlaw(fixed-pform) | TH143 |
| maskinglimitlawonlh-iid | TH151 |
| maskingneedsorder-onecross-blockcancellation | TH354 |
| maskingpersistsiffeta<1/2.02 | RF135 |
| mass | RF120 |
| mass-qualifiedfixed-bisectionobstructionandthediscrepancyrange | CJ115 |
| matchinglowerbound | LM137 |
| mathews-schmidler2024template | CJ283 |
| matryoshka | RF119 |
| measurable_post | LM233 |
| meth-auditreports1.2:"bitwiseonthesmokeproblemandon3/3studydesigns(s6)" | RF270 |
| meth-audits3table | TH400 |
| meth-audittheoremrobustnessunderparallelexecution | TH400 |
| methodpartition=groupsonlhexactgram | LM115 |
| methodswithguaranteesaresequential | RF268 |
| mis_ext_le_of_mem_lat | LM250 |
| mis_ext_step | LM252 |
| mittag-lefflerlemma | LM140 |
| mix-pos | TH404 |
| mixed-ratetransfer | TH101 |
| mixing/spectralgapofthephi=1moveround(v10) | CJ301 |
| mixturestartexactlysamplable | TH179 |
| monotoneheightsandinterleaving | LM130 |
| monotonicity | LM144 |
| monotonicityin/r | LM127 |
| monotonicityofrho_vandpilotess | LM220 |
| monotonicityoftheesscriterion | LM217 |
| moreislandsalwayshelps | RF273 |
| motivationforthesmcmachinery | RF104 |
| move-classtable | LM243 |
| move-countidentitydocumentedasnotformalised | RF286 |
| move-limitbinding | CJ279 |
| movealgebra | LM150 |
| mpm_hat_eq_iff | TH435 |
| mpm_min_riskh | TH428 |
| mpm_unique_iff | TH429 |
| multi-flipd2conjecture | CJ193 |
| multi-fliproundlemma | LM176 |
| multi-step-per-roundprogressbound | CJ183 |
| multi-targetlemmap | LM166 |
| mz-c1 | TH315 |
| mz-e1e2 | TH308 |
| mz-p1p2 | TH312 |
| mz-p3 | TH314 |
| n(w-bar) | LM218 |
| n*_nulln*_deln*_swpn*_halfn*_hit | CJ156 |
| n-a | TH305 |
| n-b | TH306 |
| n-c | TH307 |
| n-indexedbudgets | TH322 |
| n-indexedformoftheoremr | TH304 |
| n1(t38-recordi.d) | TH269 |
| n11 | CJ135 |
| n12 | CJ135 |
| n16 | CJ221 |
| n1oft38v3 | TH269 |
| n1singletonboundcontrolsmulti-variableblocks | RF152 |
| n2(c) | CJ213 |
| n200 | TH334 |
| n200deterministicinclusions | LM205 |
| n3 | CJ209 |
| n3(t38-recordi.d) | TH272 |
| n3dpinvariant | CJ209 |
| n3oft38v3 | TH272 |
| n4(iii) | CJ218 |
| n4oft38v3 | TH263 |
| n5oft38v3 | TH267 |
| n9-g | TH405 |
| n9-i | TH408 |
| n9-n | TH407 |
| n9-r | LM229 |
| n9-s | TH410 |
| n9-u | TH406 |
| n9-z | TH409 |
| n9:"afixedorderisnotself-adjoint"and"theexactcondition...itfailsif" | RF278 |
| n9claimg | TH405 |
| n9claimi | TH408 |
| n9claimn | TH407 |
| n9claimr | LM229 |
| n9claims | TH410 |
| n9claimu | TH406 |
| n9claimz | TH409 |
| n9negativecontrols:mutatedkernelsthatmustfaildetailedbalance | CE217 |
| n=1e16,p=n^0.95,r=0.9 | CE197 |
| n=20 | CE211 |
| n=20,p=4 | CE198 |
| n=200dilutionnumbersvscl(0)prediction | CE121 |
| n=200disclosurenumbers | RF105 |
| n=200disclosureparagraph | CJ239 |
| n=4p=1c0=s0 | CE177 |
| naivemergeatgrowingp | CJ281 |
| naivemergeofblockfitsrecoverstheposterior(propm(b)) | RF266 |
| nb' | TH242 |
| nb'-lh | TH268 |
| nbconstantr* | TH168 |
| nbproof | TH159 |
| near-truthregionr_d | CJ129 |
| near-truthstartmassatp>>n | TH150 |
| needsescalation3 | RF151 |
| neutralmovepaidbackbytwo-unitswap | CE137 |
| new-synth | TH412 |
| new_targetsh | TH324 |
| nis | CJ130 |
| nl0' | TH232 |
| nl0(0) | TH231 |
| nl0(0)/udel(1) | TH231 |
| nl0(1)/udel(2)underg,r,se,bm-infalone | RF194 |
| nl0(a) | TH232 |
| nl0(a)/udel(a>=2) | TH232 |
| nl0,udel,ts,tl,btp,ind | TH238 |
| nl0-inflation | RF190 |
| nl0quantifier | RF191 |
| nl_avg | CJ127 |
| nl_avg(kappa) | CJ127 |
| nl_eta | CJ127 |
| nl_eta->nl_c | TH139 |
| nl_eta0 | RF120 |
| nl_η | CJ127 |
| nm-r | TH393 |
| nmnormalisation,label-timeoccupancy,o(1)ideal-gridstagecount | CJ281 |
| no-blow-upevent | TH242 |
| no-ls0maskedconsistencyonf_cert | TH275 |
| no-ls0t38(b)viagu | CJ278 |
| no-switchconsistencyattheactualbudgets | CJ108 |
| no-tweakroute | TH154 |
| no-tweakroute(b1')forc>=2 | CJ148 |
| no_size_prior_repairs | TH424 |
| noanaloguespeed-upformcmc | RF268 |
| noc1underkeep | TH265 |
| noconditionalevidencetheoremfromfirstmoments | TH302 |
| nodeterministiclimitpartitionfors3/s4 | TH192 |
| noise-boundcounterexamples | CE142 |
| noise-chasingobstruction | TH356 |
| non-closureofw+ | CE173 |
| non-vacuousfinite-nsingle-particlerepair | CJ182 |
| nopublishedbvsmcmc-slow/smc-fastseparation | CJ290 |
| normalisedreferencemass | CJ125 |
| nosize-onlypriorrepairsawithin-sizerankingerror | TH424 |
| notclaimed(w4-t38fullii.9,w6-fixrev1) | RF212 |
| notformalised | CJ314 |
| nothinginthesampleprovesansmc-bvsoutputtheorem | CJ295 |
| notint | TH332 |
| notlaminar=>blocks!=groups | RF148 |
| noveltyoflocal-to-globalsmcforbvs | CJ276 |
| null-inflationriskof(c) | CJ158 |
| nullinclusionso(1) | TH175 |
| nullscorelaw(beta(1/2,(n-2)/2)) | LM131 |
| nullties | LM149 |
| nulog(1+a/rss^y)<=1 | RF138 |
| numcoverage | RF117 |
| numerical_failureimpossibleatn=200 | TH344 |
| numericalmarginsonacommonscoredset | CJ113 |
| numericalrefutationofthe1.2e5onset:q_natn=130,328 | CE114 |
| o-certc1(a)self-inclusivegapinequality | RF238 |
| o-certc1(b)unscored-masssentence | RF237 |
| o-certc5tie-insensitiveprose | RF239 |
| o-certc6floating-pointclausealphae^eta+eps | RF240 |
| o-certlemmam(monotonicityofthescoreingredients) | LM204 |
| o-certoverstatement:cannotcertifyconfidencewithoutpw2orenumeration | RF241 |
| o-certsection4illustration | CJ245 |
| o-diluteresidvariant | CJ162 |
| o-mixthmb3remark3 | CJ160 |
| o-pw2corollaryb2 | TH318 |
| o-pw2lemma1 | LM201 |
| o-pw2lemma2 | LM202 |
| o-pw2non-vacuity | CJ219 |
| o-pw2theorema | TH316 |
| o-pw2theoremaversuscerou-delmoral-guyader2011thm1.4 | CJ286 |
| o-pw2theoremb | TH317 |
| o-pw2theoremc | TH319 |
| o-stagescorollarywprime | TH367 |
| o-stagescorollaryw‴ | TH369 |
| o-stagesitem4denselimitsqrt(c)t*->l=syedetal.globalbarrierlambda | CJ285 |
| o-stageslemma0 | LM216 |
| o-stageslemma1 | LM217 |
| o-stageslemmap | LM219 |
| o-stagestheoremf | TH366 |
| o-stagestheoremg | TH364 |
| o-stagestheoremg(i)+lemma1=stefankovic-vempala-vigoda2009 | CJ284 |
| o-stagestheoreml | TH365 |
| o-stagestheoremm | TH368 |
| o-swap"4no-outputfitsareexcluded" | RF243 |
| o-swappredictedratest2vsobserved | CJ242 |
| o-swappredictorst1(independence)andt1-lo(clustermaximum) | RF248 |
| o-swapprops1-3provedunderpa | RF242 |
| o-swaprealisedone-movecheckreproducesobservedmisses | CJ241 |
| o-vcertnon-monotonicityofm(s)andendpointfailure | CE196 |
| o-vcertr1 | TH332 |
| o-vcertr2 | TH333 |
| o-vcertsection2.1factordesignn=40p=10 | CE189 |
| o-vcertsection2.2floating-pointinstance | CE192 |
| o-wstabfirstw(d)hypothesisp^r/sqrtn->0fortheupperhalf | RF257 |
| o-wstablemma0 | LM209 |
| o-wstabtheoremw | TH362 |
| obg-bg1 | TH255 |
| obg-bg1' | TH256 |
| obg-bg2 | TH257 |
| obg-bg3 | TH258 |
| obg-corbg1inf | TH255 |
| obg-final-run | CJ203 |
| obg-lemmar | LM176 |
| obg-lh-ii-iv | TH259 |
| obg-lh-lock | TH261 |
| obg-lh-lock-general | RF208 |
| obg-lh-lockc1p | TH261 |
| obg-lh-p1 | TH259 |
| obg-lh-rate | TH260 |
| obg-lhiid | CJ202 |
| obg-pinf | CJ202 |
| obg-t38b-bg3 | TH263 |
| obg-t38b-nols0 | TH262 |
| occupancyfromanevidencelowertail | TH113 |
| ocert-c1 | TH326 |
| ocert-c2 | TH327 |
| ocert-c3 | TH328 |
| ocert-c4 | TH329 |
| ocert-c5 | TH330 |
| ocert-c6 | TH331 |
| ocert-lemmam | LM204 |
| oddstransferunderbo | LM135 |
| omitted-massidentity | TH111 |
| omix-b1 | TH179 |
| omix-b2 | TH180 |
| omix-b3 | TH181 |
| omix-biidlh | CJ159 |
| omix-blink | LM133 |
| omix-c-null | CJ158 |
| omix-c0 | TH182 |
| omix-c1 | TH183 |
| omix-c2 | TH184 |
| omix-c3 | TH185 |
| omix-cfix | CJ157 |
| one-changeceiling | TH194 |
| one-pagert26restatement | RF235 |
| one-roundconfinement | TH271 |
| one-roundrepairatphi=1 | LM181 |
| one-roundsweep | TH225 |
| one-shotimportancecorrection | TH382 |
| one-sidedchain-freetablebound | LM136 |
| one-sidedglobalcertificate | TH326 |
| one-stageregime | TH371 |
| one-stepsecond-momentbound | CJ122 |
| oneadditionatasuperset | LM225 |
| oneimportancestep | TH349 |
| op-ls0 | CJ213 |
| open | CJ290 |
| optimalityofpropg | CJ174 |
| optional_pw2(a)-(c)one-stepparent-uniformroute | RF236 |
| opw2-cex | RF228 |
| opw2-cexinstance | CE183 |
| opw2-thma | TH316 |
| opw2-thmb | TH317 |
| opw2-thmbcorollaryb2 | TH318 |
| opw2-thmc | TH319 |
| oraclegap | TH135 |
| oraclejointbernstein-vonmiseslimit | CJ102 |
| orderedpaths | TH108 |
| orderfacts | LM164 |
| orderindependenceoftheboundedstores | LM226 |
| originala5 | RF166 |
| originalt37 | RF165 |
| orth | CJ130 |
| orth-joint | CJ210 |
| orthcompatibility | TH325 |
| orthcomposition | CJ210 |
| orthgridinputs | TH374 |
| orthjointfamily | CJ210 |
| orthogonalfactorisationofthediscrepancy | LM177 |
| orthogonalthreshold | CJ101 |
| oswap-l0 | LM208 |
| oswap-p1 | TH336 |
| oswap-p2 | TH337 |
| oswap-p3 | TH339 |
| oswap-p5 | TH341 |
| oswap-t4 | TH340 |
| otherthresholdsbindearlier | RF123 |
| out | LM192 |
| output-event,guardandsrconventionsinsidetheleancomposition | CJ326 |
| outputconventiondecision | CJ214 |
| outside-storemass | TH332 |
| over-temperedroute | RF118 |
| overfitted-sidebottleneckforthepaperprior | TH401 |
| ows-ws1 | TH348 |
| ows-ws2 | TH349 |
| ows-ws3 | TH350 |
| ows-ws4 | TH351 |
| ows-ws52 | TH352 |
| ows-ws53f | TH353 |
| ows-ws53m | TH354 |
| ows-ws53n | TH353 |
| ows-ws6abc | TH355 |
| ows-ws6d | TH356 |
| ows-ws6e | CJ261 |
| ows-ws7 | TH357 |
| ows-ws8abc | TH358 |
| ows-ws8d | CJ262 |
| p(s-hat=s0)->1-limsupp(u)(brief'slimitform) | RF223 |
| p(u)->0 | CJ212 |
| p(w_r<c/c)=1 | RF229 |
| p1rbpipbiasbound | TH312 |
| p2l1errorafterdelivery | TH313 |
| p8 | CE107 |
| p=6gibbs-only,a_4*=0.90vschi2_4=0.111 | CE183 |
| p=n-1,onecoefficient2,sigma^2=1 | CE199 |
| p>~n^0.58 | RF190 |
| p^-caloneforcesvanishingmass | RF135 |
| paerrortoprobabilitybound | CJ236 |
| pair-lawrepresentation | LM127 |
| papertheorem5 | TH290 |
| part-ce1 | CE117 |
| part-ce2 | CE118 |
| part-ce3 | CE116 |
| part-corb | TH163 |
| part-corc | TH164 |
| part-kappa | TH165 |
| part-l1 | LM127 |
| part-l2 | LM128 |
| part-l3 | LM129 |
| part-l3literal | RF140 |
| part-pairing | CJ146 |
| part-thma | TH162 |
| part-thmb | TH163 |
| part-thmc | TH164 |
| partial-residualtables | CJ162 |
| partition-freegoodevents(g1)-(g5) | LM142 |
| partition-noisedecoupling | CJ139 |
| partition-recoverylemma | TH163 |
| partition=groupsdeterministic | TH162 |
| partition=groupsonlh-iid | TH148 |
| partitionasarandomvariable | TH375 |
| partitionlaw | CJ302 |
| path-freefpargument | CJ235 |
| path-wisefinite-n(d_s)boundatn=200 | CJ152 |
| path_f_strictmono | TH440 |
| path_mem_of_tdinf | LM254 |
| path_stays | LM253 |
| pathlength | TH365 |
| pathlength<=pi | TH377 |
| pathlengthdeterminesthenumberofess-0.9stages | RF258 |
| pcapmempty | CJ124 |
| pd_of_reach | TH448 |
| per-datasetmatching | CJ238 |
| per-fitcertificatecard | TH331 |
| per-fitconfidencecertificate | CJ234 |
| per-fitevidenceband | TH315 |
| per-stagesharehypothesis | CJ189 |
| perfect-mixingguess | RF228 |
| perturbation | LM219 |
| perturbationinstandardisedcross-blockgram | TH351 |
| pg(a) | TH232 |
| pgd-corw' | TH210 |
| pgd-l1.1 | LM150 |
| pgd-l1.2 | LM151 |
| pgd-l1.3 | LM152 |
| pgd-la' | LM153 |
| pgd-lg | LM158 |
| pgd-lld | LM155 |
| pgd-lq | LM158 |
| pgd-lr | LM157 |
| pgd-ls | LM154 |
| pgd-lu | LM159 |
| pgd-p1 | TH205 |
| pgd-p2 | TH206 |
| pgd-p3 | TH207 |
| pgd-p4 | TH208 |
| pgd-p5 | LM156 |
| pgd-p6 | TH209 |
| pgd-star-misleading | RF174 |
| pgdiffpop-latonalattice | TH216 |
| pgdsharpness | TH208 |
| phase-1andphase-2progress | TH226 |
| phi*_n | RF117 |
| phi-reach | CE137 |
| pi(x)finite-nenvelope | CJ230 |
| pilotdiscoveryundertheterminal-repairhypotheses | CJ111 |
| pilotfidelity | CJ272 |
| pilotone-flipdiscovery | TH242 |
| pilotstagecounto_p(1) | CJ268 |
| pilotstep | LM222 |
| piplossneedsrewardcontrol | CJ110 |
| pk(d*) | CJ197 |
| pk(g-1) | CJ197 |
| pmom | RF119 |
| pointwiseaddability | TH229 |
| poolavoidance | CJ124 |
| pooledxpooledbiasinstance | CE182 |
| pooledxpooledpip | RF226 |
| pooledxpooledpipbias | TH298 |
| pooledz-hatxpooledpipunbiased | RF226 |
| poolingasrgrowsatfixedn | TH397 |
| pop-latonlh | TH293 |
| population-gapcomparisons | LM158 |
| populationdelivery | CJ217 |
| populationdescent | LM224 |
| populationresidualsofthelhcomponents | LM119 |
| pos | TH199 |
| positioningagainstywj/zyvr | TH404 |
| post-searchhpmmonotoneintheislandcountrprimewithouttheextralocalsearch | RF272 |
| post-searchhpmnonmonotoneinrprime:n=29,p=8proxydesign(c6_ls.py) | CE220 |
| posterior-barrierdesignpb | CE169 |
| posterior-misscertificate | TH330 |
| posteriorbarrier | CJ279 |
| posteriorconcentrationonfav | TH195 |
| posteriorconcentrationonlh-iid | TH155 |
| posteriorkeepandswapmargins | LM186 |
| posteriormissinference | RF167 |
| postfactsofbasic.lean | LM234 |
| predicted558vsobserved571 | CJ243 |
| predictort2 | TH342 |
| preprocessingerror | CJ235 |
| primitiveconstants | TH319 |
| probabilityofresource_limit | CJ212 |
| production-bconjecturec2->1-h_a | CJ184 |
| productionlocalsearchonthelattice | LM125 |
| productionmaskedconsistencybeyondlh | CJ302 |
| productionsemanticsofthegreedysearch | CJ323 |
| progress_mem_lat | LM243 |
| projectionapproximationpa | LM208 |
| projectionontonearlyorthogonalsubspaces | LM141 |
| proof_v2 | TH123 |
| proofsection3remark3 | TH383 |
| prop.a | TH225 |
| prop.b1 | TH179 |
| prop.b1'(w2-prem) | TH229 |
| prop.b2 | TH180 |
| prop.c0 | TH182 |
| prop.c2 | TH184 |
| prop.c3 | TH185 |
| prop.d | TH221 |
| prop.d' | TH129 |
| prop.d'dilutionclauseassharptheorem | CJ168 |
| prop.d-prime | TH177 |
| prop.dm | TH178 |
| prop.dtarget | RF103 |
| prop.im | TH235 |
| prop.ind-m | TH235 |
| prop.lh-lat | TH293 |
| prop.nl0 | TH232 |
| prop.pa | TH229 |
| prop.s | TH176 |
| prop.sw | TH234 |
| prop.t2 | TH230 |
| prop.tl | TH234 |
| prop.ts | TH233 |
| prop.u | TH227 |
| prop.u' | TH227 |
| prop.u(u-a)counterexample | CE147 |
| prop.u(u-b)counterexample | CE148 |
| prop.udel | TH232 |
| prop.ulr | TH234 |
| prop.ushortcuts | RF186 |
| prop.w | TH130 |
| prop1 | TH131 |
| prop1(i-prime) | TH131 |
| prop1(iii-prime) | TH131 |
| prop1-t07 | TH131 |
| prop1-td | TH198 |
| prop1-td(retiresliteralt37) | RF101 |
| prop1-wronghpm | RF125 |
| prop2 | CJ250 |
| prop2(a,b,d,e) | TH297 |
| prop2(b)(d)(e)inlean | CJ313 |
| prop2(c) | TH298 |
| prop2(f) | TH299 |
| prop2.1-2.2 | TH139 |
| prop2/t12/t31(i)arestandard | CJ287 |
| prop2restatedt12+t31(i) | TH297 |
| propa-sweep | TH225 |
| propb1-b2 | TH226 |
| propbasin | TH387 |
| propc | TH325 |
| propc-ld | CE138 |
| propd | CE111 |
| propd'-t03 | TH129 |
| propd-dilution | TH146 |
| propd-drift | TH221 |
| propd-t03 | CE111 |
| propdm(i)-loga>=-logp_t(n<=k) | RF149 |
| propf | TH200 |
| propg | CE139 |
| propg-wording | TH250 |
| propgu | TH388 |
| propl | TH360 |
| proplh | TH259 |
| proplh-pgd | TH215 |
| propm | CE208 |
| propm(a) | TH253 |
| propm(b) | RF203 |
| propm(b)onlh | TH270 |
| propm-lh | TH270 |
| propnm-a | CE208 |
| propob | TH401 |
| proposals13.1 | CJ298 |
| proposition1 | TH131 |
| proposition1(o-swap) | TH336 |
| proposition2(a),(b),(d),(e) | TH297 |
| proposition2(api-n200) | TH335 |
| proposition2(c) | TH298 |
| proposition2(f) | TH299 |
| proposition2(o-swap) | TH337 |
| proposition3(o-swap) | TH339 |
| proposition5(o-swap) | TH341 |
| proposition6(o-swap) | TH342 |
| propositiona | TH225 |
| propositionb1(o-mix) | TH179 |
| propositionb1(w5-faviid) | TH193 |
| propositionb2 | TH180 |
| propositionbasin | TH387 |
| propositionc0 | TH182 |
| propositionc2 | TH184 |
| propositionc3 | TH185 |
| propositionconf | TH271 |
| propositiond | CE111 |
| propositiond' | TH129 |
| propositiond(deterministicstart-massceiling) | TH146 |
| propositiond3 | TH245 |
| propositiondm | TH178 |
| propositione1 | TH246 |
| propositione3 | TH126 |
| propositionf | TH200 |
| propositionf(w5-faviid) | TH194 |
| propositiong | TH250 |
| propositiongu | TH388 |
| propositionl | TH360 |
| propositionlh | TH259 |
| propositionlh-lat | TH293 |
| propositionlh-lock | TH261 |
| propositionlh-rate | TH260 |
| propositionm(a) | TH253 |
| propositionm(b) | RF203 |
| propositionm-lh | TH270 |
| propositionn(w5-faviid) | TH192 |
| propositionob | TH401 |
| propositionone-shot | TH356 |
| propositionp | TH397 |
| propositions | TH176 |
| propositionsh | TH251 |
| propositionsl | CJ274 |
| propositiont33-h | TH345 |
| propositiont33-z | TH346 |
| propositionu | TH227 |
| propositionu' | TH227 |
| propositionu(api-pos) | TH402 |
| propositionv1 | TH247 |
| propositionw | TH130 |
| propositionw-cal | TH395 |
| propositionw0 | TH359 |
| propositionws5.2 | TH352 |
| propositionws8(a)-(c) | TH358 |
| propositionx | TH252 |
| propp | TH397 |
| propp1 | TH205 |
| propp2 | TH206 |
| propp3 | TH207 |
| propp4 | TH208 |
| props' | TH213 |
| props.b1'/b2' | TH219 |
| props.b1,b2 | TH226 |
| propsl | CJ274 |
| propsnon-injectivereplacementassignments | CE126 |
| propsproductdenominator | RF154 |
| propt | TH217 |
| propt05-o | TH135 |
| propt2-prem | TH230 |
| proptinstance | CE141 |
| propu | TH227 |
| propushortcutclaims | RF186 |
| propw | TH394 |
| propw-cal | TH395 |
| propw-sig | TH130 |
| propw0 | TH359 |
| propx-moreover | TH252 |
| proxy-splitexactstagecounts14,16,18vslog2a0+7.7 | CE200 |
| proxykeep | CJ197 |
| proxylocalmaximum | CE101 |
| psi-rhocliff | CE116 |
| psi=0.71,0.75,0.8 | CE116 |
| psi>rhotransitiontothefavourableregime | CJ145 |
| psi_capped_le | LM239 |
| psi_jplus_le | LM237 |
| psi_jplus_unique_iff | LM238 |
| pw2 | CJ122 |
| pw2-freevariancebound | TH317 |
| pw2forthehybridparticlesystem | CJ262 |
| pw2holdswitha_t=(s_t-s_{t-1})_+ | TH318 |
| pw2varianceidentity | TH316 |
| pw2witha_t=chi2_t | RF228 |
| pxn(l)-failureformula | TH170 |
| pxn-cor | TH156 |
| pxn-lemmau-u1 | RF138 |
| pxn-lfail-numbers | RF145 |
| pxn-p1 | TH148 |
| pxn-p2 | TH149 |
| pxn-p3 | TH150 |
| pxn-p4 | TH151 |
| pxn-p5 | TH152 |
| pxn-p6 | TH153 |
| pxn-p7 | TH154 |
| pxn-p8 | TH155 |
| pxn-q | TH157 |
| pxn-w | TH158 |
| pxn-w' | CJ140 |
| pxncor(b1) | TH288 |
| pxndesignde-randomisationlemma | LM120 |
| pxngaplemmae | LM123 |
| pxngaplemmals | LM125 |
| pxngaplemmat | LM124 |
| pxngaplemmatr-j | LM122 |
| pxngapmaintheorem | TH161 |
| pxngapo2 | CJ147 |
| pxnjointls0route | TH160 |
| pxnlemmab | LM116 |
| pxnlemmac1 | LM121 |
| pxnlemmalambda | LM119 |
| pxnlemmatr | LM117 |
| pxnlemmau | LM118 |
| pxnnbconstant1.925 | RF143 |
| pxnp7betashape(n-3-s)/2 | RF146 |
| q/xi_n0.60-0.82ineverycell,factor5tospare | RF157 |
| q_fpi0(s0)->0forc>=2andp->infinity | RF217 |
| q_s>=y'y/(n+1) | LM207 |
| q_sversusrss | LM109 |
| q_{t-1}(q_tf)=q_t(f) | LM201 |
| quantifierarraycounterexample | CE154 |
| quoted(l)-failure4%and1.2%unlabelled | RF145 |
| r | CJ130 |
| r-t13 | CJ116 |
| r1 | CJ130 |
| r1-cert | TH137 |
| r1-pos | TH199 |
| r1<r2witnesses | CE109 |
| r2 | CJ130 |
| r2-dichotomy | RF168 |
| r3 | CJ130 |
| r3-lhiid(vexp) | TH145 |
| r4 | CJ130 |
| r4-excess | RF173 |
| r5(a-rev6book) | CJ208 |
| r9global_certifiedrigorous | RF244 |
| r>1/(2a) | CJ172 |
| random-designleakagecatastrophe | TH189 |
| random-orderroundself-adjointness | LM229 |
| random-partitionquantifier | LM124 |
| randomgaussiandesigns | TH209 |
| randompartitionsdonotundolhmasking | TH180 |
| rankingceilingforeverycommonsigma^2 | TH176 |
| rapid-mixinghypotheses | CJ289 |
| rapid-mixingtheorems(ywj,zyvr,chang-zhou)applyto/certifythepapertargetonlh(ledgerglossofapi-posheadline2) | RF274 |
| rare-outsidersharptransition | RF205 |
| ratio1.925givesess>=0.9h | RF200 |
| rbconsequencewithoutastationarystart | RF278 |
| realisedbudget | TH372 |
| recordedrbidentities | TH110 |
| recording-prefixcontrol | TH117 |
| refereetaskr9 | CJ134 |
| reference-stateidentity | LM216 |
| referencedecomposition | LM221 |
| referencetransfer | TH139 |
| refinedfinite-naggregationfort22(i)weightingubystartmass | CJ167 |
| refinedt37(i) | TH199 |
| refinedt37(ii) | TH201 |
| refinedt37(iii) | TH204 |
| reflectedcomparator | TH306 |
| reflectedsingle-flippairbenchmark | CJ105 |
| reflectionwithoutput-specificcoupling | CJ104 |
| regimeassumptions | CJ130 |
| registryocert-§4conflict | CJ245 |
| remaininggapinldthreshold | CJ174 |
| remarkc6'(deterministicregime) | TH331 |
| renyithresholdalpha*=1+1/(2aomega*) | CJ261 |
| repairedc2bound | LM160 |
| repairr1 | TH332 |
| repairr2 | TH333 |
| replacementonsetgloss:theproofdeterministicthresholdsaswrittenholdfromnabout2e6(w2-vt03rr1/w6-fixrev2replacementsentence) | RF124 |
| reported_eq_hpm_iff | TH431 |
| reported_min_risk01_iff | TH432 |
| reported_truth_needs_unscored | TH433 |
| reportedhpmversionoft05-u | TH133 |
| resample_move_step | LM249 |
| residsweeps | CJ162 |
| residualisedtables | CJ162 |
| resource_limitassigma(c)launchevent | RF234 |
| restatedt24 | TH218 |
| restrictedess | TH111 |
| ret+occ | RF117 |
| retentioninequalityprod(1-eta_s)>=e^{-teta} | RF206 |
| rev6-cands(a6) | CJ207 |
| reversal-invariantrandomorderofreversiblekernels | LM229 |
| reversibleleaks | CJ200 |
| reweightingcannotcreatethetruth | TH357 |
| rf101 | RF101 |
| rf102 | RF102 |
| rf103 | RF103 |
| rf104 | RF104 |
| rf105 | RF105 |
| rf106 | RF106 |
| rf107 | RF107 |
| rf108 | RF108 |
| rf109 | RF109 |
| rf110 | RF110 |
| rf111 | RF111 |
| rf112 | RF112 |
| rf113 | RF113 |
| rf114 | RF114 |
| rf115 | RF115 |
| rf116 | RF116 |
| rf117 | RF117 |
| rf118 | RF118 |
| rf119 | RF119 |
| rf120 | RF120 |
| rf121 | RF121 |
| rf122 | RF122 |
| rf123 | RF123 |
| rf124 | RF124 |
| rf125 | RF125 |
| rf126 | RF126 |
| rf127 | RF127 |
| rf128 | RF128 |
| rf129 | RF129 |
| rf130 | RF130 |
| rf131 | RF131 |
| rf132 | RF132 |
| rf133 | RF133 |
| rf141 | RF134 |
| rf142 | RF135 |
| rf143 | RF136 |
| rf144 | RF137 |
| rf145 | RF138 |
| rf146 | RF139 |
| rf147 | RF140 |
| rf148 | RF141 |
| rf149 | RF142 |
| rf150 | RF143 |
| rf151 | RF144 |
| rf152 | RF145 |
| rf153 | RF146 |
| rf154 | RF147 |
| rf155 | RF148 |
| rf161 | RF149 |
| rf162 | RF150 |
| rf163 | RF151 |
| rf164 | RF152 |
| rf165 | RF153 |
| rf166 | RF154 |
| rf167 | RF155 |
| rf168 | RF156 |
| rf169 | RF157 |
| rf170 | RF158 |
| rf171 | RF159 |
| rf172 | RF160 |
| rf173 | RF161 |
| rf174 | RF162 |
| rf175 | RF163 |
| rf176 | RF164 |
| rf181 | RF165 |
| rf182 | RF166 |
| rf183 | RF167 |
| rf184 | RF168 |
| rf185 | RF169 |
| rf186 | RF170 |
| rf187 | RF171 |
| rf188 | RF172 |
| rf189 | RF173 |
| rf190 | RF174 |
| rf191 | RF175 |
| rf192 | RF176 |
| rf193 | RF177 |
| rf194 | RF178 |
| rf195 | RF179 |
| rf196 | RF180 |
| rf197 | RF181 |
| rf201 | RF182 |
| rf202 | RF183 |
| rf203 | RF184 |
| rf204 | RF185 |
| rf205 | RF186 |
| rf206 | RF187 |
| rf207 | RF188 |
| rf208 | RF189 |
| rf209 | RF190 |
| rf210 | RF191 |
| rf211 | RF192 |
| rf212 | RF193 |
| rf213 | RF194 |
| rf214 | RF195 |
| rf215 | RF196 |
| rf221 | RF197 |
| rf222 | RF198 |
| rf223 | RF199 |
| rf224 | RF165 |
| rf225 | RF200 |
| rf226 | RF201 |
| rf227 | RF202 |
| rf228 | RF203 |
| rf229 | RF204 |
| rf230 | RF205 |
| rf231 | RF206 |
| rf232 | RF207 |
| rf233 | RF208 |
| rf234 | RF209 |
| rf235 | RF210 |
| rf236 | RF211 |
| rf237 | RF212 |
| rf238 | RF213 |
| rf239 | RF214 |
| rf241 | RF215 |
| rf242 | RF216 |
| rf243 | RF217 |
| rf244 | RF218 |
| rf245 | RF219 |
| rf246 | RF220 |
| rf247 | RF221 |
| rf248 | RF222 |
| rf249 | RF223 |
| rf250 | RF224 |
| rf261 | RF225 |
| rf262 | RF226 |
| rf263 | RF227 |
| rf264 | RF228 |
| rf265 | RF229 |
| rf266 | RF230 |
| rf267 | RF231 |
| rf268 | RF232 |
| rf269 | RF233 |
| rf270 | RF234 |
| rf271 | RF235 |
| rf272 | RF236 |
| rf281 | RF237 |
| rf282 | RF238 |
| rf283 | RF239 |
| rf284 | RF240 |
| rf285 | RF241 |
| rf286 | RF242 |
| rf287 | RF243 |
| rf288 | RF244 |
| rf289 | RF245 |
| rf290 | RF246 |
| rf291 | RF247 |
| rf292 | RF248 |
| rf293 | RF249 |
| rf294 | RF250 |
| rf295 | RF251 |
| rf301 | RF252 |
| rf302 | RF253 |
| rf303 | RF254 |
| rf304 | RF255 |
| rf305 | RF256 |
| rf306 | RF257 |
| rf307 | RF258 |
| rf308 | RF259 |
| rf309 | RF260 |
| rf310 | RF261 |
| rf321 | RF262 |
| rf322 | RF263 |
| rf323 | RF264 |
| rf324 | RF265 |
| rf325 | RF266 |
| rf326 | RF267 |
| rf341 | RF268 |
| rf342 | RF269 |
| rf343 | RF270 |
| rf344 | RF271 |
| rf345 | RF272 |
| rf346 | RF273 |
| rf347 | RF274 |
| rf348 | RF275 |
| rf349 | RF276 |
| rf350 | RF277 |
| rf351 | RF278 |
| rf352 | RF233 |
| rf353 | RF279 |
| rf354 | RF280 |
| rf355 | RF281 |
| rf356 | RF282 |
| rf361 | RF283 |
| rf362 | RF284 |
| rf363 | RF285 |
| rf364 | RF286 |
| rf365 | RF287 |
| rf366 | RF288 |
| rf367 | RF289 |
| rfixedinadvance | TH397 |
| rigorousbracketforpredictort2 | CJ232 |
| rigorousceiling | TH173 |
| rigorousn=200partitionboundforthelhlinkedpair | CJ150 |
| risk01_eq | LM235 |
| risk01_min_iff | TH426 |
| riskh_eq | LM236 |
| ro | LM188 |
| rotationinvariance | LM129 |
| round-startoccupancy | LM200 |
| route(e') | TH239 |
| route(e)viatheoremb | TH280 |
| route(e-m) | TH223 |
| routeconjectureofw1-t03rsection4 | CJ132 |
| routes(a)-(f) | TH115 |
| rssfloor | LM112 |
| run/outputsplit | LM188 |
| s-elsmovecapl=10atbothp | RF246 |
| s-gap | CJ282 |
| s-tilde0scannedasacentre | RF120 |
| s03 | TH128 |
| s03section2 | TH125 |
| s1context-freebound | TH193 |
| s5-typeglobalfactor | CJ149 |
| s5maskedmode{0,2,13,14} | RF196 |
| sam"thm5"label | RF276 |
| sam_lh_demo.py | CE213 |
| same-rateboundsdonottransfer | CE109 |
| sametotalparticles,rislands | TH398 |
| samonanlh-likemaskeddesign | CE213 |
| sampled-centrererun | CJ179 |
| scan-before-limit | LM195 |
| scanbeforelimit | LM195 |
| schur-incrementn=10example | CE172 |
| scopeofprop.d | TH129 |
| score-evaluationceilingofthesmcbranch | TH294 |
| scorerepresentation | LM157 |
| scoringbasin | TH387 |
| scoringruleofstep_gibbs | LM193 |
| se | CJ130 |
| se+bm-infimplypgd | RF180 |
| se-blkandexp'foriiddesignswithx-dependentpartition | CJ151 |
| section13.1 | CJ254 |
| section13.1asdrafted | RF230 |
| section13.3 | CJ255 |
| section3.2 | CJ253 |
| section5.3theorem1 | CJ251 |
| section5.4 | CJ252 |
| selected-modelfixed-atomcertificateexp(-q_fpi0(s-hat)) | RF115 |
| selection-proof | TH326 |
| selectionconsistency | TH103 |
| sep(a) | TH380 |
| sep(a)onlh-iid | TH381 |
| sep(b) | TH382 |
| sep(b)pipversion | TH383 |
| sep(c) | TH384 |
| sep(d) | TH385 |
| sep(e) | TH386 |
| sep-a | TH380 |
| sep-a-iid | TH381 |
| sep-b | TH382 |
| sep-basin | TH387 |
| sep-c | TH384 |
| sep-corgulh | TH389 |
| sep-e | TH386 |
| sep-gu | TH388 |
| sep-gu1 | LM224 |
| sep-gu2 | LM225 |
| sep-guiid | TH390 |
| sep-gunulls | CJ277 |
| sep-nols0 | CJ278 |
| sep-taska | CE207 |
| separabledominationunderorth | LM213 |
| separationforevidence/pipaccuracy | CJ280 |
| separationoutsidethefrozensetting | CJ279 |
| sequentialcancellation | TH119 |
| sequentialratiolaw | CJ125 |
| setanalogueoft22(iv) | RF198 |
| share | CJ189 |
| share(zeta) | CJ189 |
| share-b2w4 | TH254 |
| share-b2w4-exitloss | RF204 |
| share-bgd | CJ193 |
| share-c1bvs | CJ194 |
| share-d4 | TH248 |
| share-d5 | TH249 |
| share-g | TH250 |
| share-m(a) | TH253 |
| share-m(b) | RF203 |
| share-pb | CE169 |
| share-pd | LM175 |
| share-sh | TH251 |
| share-sh-prose | TH251 |
| share-track | CJ192 |
| share-x | TH252 |
| share/exit-end | TH245 |
| shareandltasroute-(b2)hypotheses | RF211 |
| sharpenedsizetail | TH125 |
| sharperthanstar | TH213 |
| sharpnessoflognthreshold | TH251 |
| shortestvalidgrid | TH364 |
| sidak/royenroute | CJ232 |
| sig(c) | TH130 |
| sig-s0 | LM134 |
| sig-s1 | LM135 |
| sig-s2 | TH186 |
| sig-s3 | TH187 |
| sig-s4 | TH188 |
| sig-s6 | TH189 |
| sigma^2-gridmixture | TH184 |
| singleextremeparticleforcespilotstepoforder1/n(informal) | CE206 |
| size-onlyrankingceiling | TH106 |
| size-priorceiling | TH131 |
| sizerange | RF147 |
| sizes2and5withb=5 | CE119 |
| smc-bvsscoreformulaandregressionstructure | CJ319 |
| smctheoryneedsglobalgapsormodemassalongthebridge | CJ291 |
| solcheckj4 | CE102 |
| song-liang-typesplittingcounterexampleonlh-likemaskedpairp=16n=200 | CE210 |
| song-lianganalyticseparation | CJ274 |
| sourceofh24 | CJ107 |
| space-timepotentialdeliverybound | TH248 |
| splitneutrality | TH398 |
| splittingtheparticlebudgetintor>>4smallerislands(c8) | RF273 |
| sr | CJ128 |
| stab-cert(a7) | TH274 |
| stab-lh | TH272 |
| stab-lhfailurea85 | CE170 |
| stackingneverworsensthereportedhpm | RF272 |
| stackingrprime>4 | TH396 |
| stagelawsofthev3grid | TH415 |
| standalonecardinalitytheorem/lat(s)/=2^phi(s) | CJ324 |
| star-prime-aalonesuffices | CJ171 |
| staroffbyfactor3-4fromc-ld | RF174 |
| start | CJ126 |
| start+onegreedysearch | TH384 |
| start-lawlowerboundwithoutq<1 | RF202 |
| start-modedptierule | CJ209 |
| start-onlymethodsfail | RF104 |
| start-onlypluslocalsearchfailsunlessbasincontainss~0 | RF262 |
| startaggregationandtailsonlh | LM178 |
| startconcentrationdichotomyundercommonsigma-hat^2 | TH186 |
| startconcentrationunderexactzeroleakage | TH140 |
| startkeepodds | LM185 |
| startmaskingbysigma^2-dilutionatfiniten | TH178 |
| startmass+bridgemass+exitcontrolimplydelivery | RF199 |
| startmassxfitness=posterior | LM175 |
| startmode=references° | TH152 |
| statementr3 | TH404 |
| statusesandallocation-dependentguarantees | CJ114 |
| stg-cexw2 | RF255 |
| stg-f | TH366 |
| stg-g | TH364 |
| stg-l | TH365 |
| stg-l0 | LM216 |
| stg-l1 | LM217 |
| stg-m | TH368 |
| stg-p | LM219 |
| stg-w3p | TH369 |
| stg-wp | TH367 |
| stochasticscheduling | CJ255 |
| stop-onlycoupling | CJ128 |
| stopping-timeshiftlemma | LM169 |
| strict_max_of_post_gt_half | LM234 |
| strictoversushpmconventiono_h | CJ214 |
| strictsame-sizemissesatc=0.5 | CJ225 |
| strictsupersets | TH102 |
| strongeruncertaintythancompletesong-liang | CJ275 |
| study-designnumericalcounterexample | CE121 |
| stylisedguardcounterexample | CE175 |
| subset:atruthdropped | TH339 |
| sufficientconditionsfortrc | TH207 |
| sup-of-sumnl0 | RF191 |
| sup-of-sumvssum-of-sups | CE154 |
| super-polynomialstart-onlybudget | RF263 |
| supersetbyonenull | TH337 |
| supersetratep-freeandrisesassignalfalls | TH338 |
| supersetreduction | LM146 |
| supersetsofs0 | LM159 |
| supersetstartconcentrations°⊋s0 | CJ185 |
| supersetstates | LM154 |
| suppressorpair | CE133 |
| susie/ssleffective-thresholdconjecture | CJ231 |
| swap_extra_truth_drop_two | LM245 |
| swapceilingisinformation-theoretic | TH341 |
| swapdominance | CE159 |
| swapidentitysw | TH198 |
| t*=log2a0+o(1) | TH368 |
| t-id | TH105 |
| t01 | TH101 |
| t01(i)-(iv) | TH121 |
| t01(t)(b1) | CE109 |
| t01(t)(b2) | CE110 |
| t02 | TH102 |
| t02(i#) | TH125 |
| t02(i) | TH102 |
| t02(i)tailsharpening | RF103 |
| t02(i-sharp) | TH125 |
| t02(ii#) | TH127 |
| t02(ii) | TH102 |
| t02(ii-sharp) | TH127 |
| t02(isharp)bb(1,p)tailnoveltynarrow | CJ293 |
| t02sharpsizecutoff | RF103 |
| t03 | TH103 |
| t03# | TH128 |
| t03-const | CJ134 |
| t03-sharp | TH128 |
| t03-sharpextensions:growings0,randomdesign,exponentialp | CJ135 |
| t03r | TH128 |
| t03sharp | TH128 |
| t03sharp(3)p(s-dagger!=s0)<=2e0[1-pi(s0)]isrossell2022proposition1 | CJ294 |
| t03sharpisamodestextensionofrossell2022andmoreno-giron-casella2015 | CJ293 |
| t04 | TH104 |
| t04andt03downstreamre-derivationwitht02(i-sharp)andse_winsteadofh-t02 | CJ137 |
| t05 | CJ101 |
| t05(i) | LM106 |
| t05(ii)failurehalf | TH132 |
| t05(ii)successhalf | TH134 |
| t05(iii) | TH135 |
| t05-g | TH135 |
| t05-l | TH134 |
| t05-shat | TH133 |
| t05-u | TH132 |
| t05amplitude-versus-energycomputationatp=n^a(t05-wording) | CE113 |
| t05explicitn0viadkw-typeuniformcontrolofnullorderstatistics | CJ136 |
| t05wording:theg-prior+bb(1,p)hpmlosesasqrt(logn)factortotheoracle | RF127 |
| t06 | TH105 |
| t06(i) | TH131 |
| t07 | TH106 |
| t07(i')sharpness | TH425 |
| t07(i)ceiling | TH423 |
| t07(ii)(a) | TH426 |
| t07(ii)(a)hpmminimises0-1risk | TH427 |
| t07(ii)(b) | TH428 |
| t07(ii)(b)uniqueness | TH429 |
| t07(ii)(c) | TH430 |
| t07(iii)(a) | TH431 |
| t07(iii)(b) | TH433 |
| t07(iii)(c) | TH434 |
| t07(iii)(c)lastclause | TH435 |
| t08 | CJ102 |
| t09 | TH107 |
| t1 | TH101 |
| t10 | TH108 |
| t10(oldlabel) | TH111 |
| t11 | TH109 |
| t11(ii)'noorderingconstantfora=1' | RF110 |
| t11(ii)a=1counterexample | CE108 |
| t11(iii) | TH109 |
| t11(iii)iidrealform | TH439 |
| t11(iii)product-spaceform | TH436 |
| t11(iii)random-variableform | TH438 |
| t11(iii)realform | TH437 |
| t11(iii)regularconditionalprobabilitygivencalibrationoutput | CJ315 |
| t11(oldlabel) | TH108 |
| t11(vii)citationinthecompositionproof | RF222 |
| t11_miss_iid | TH438 |
| t11_miss_iid_real | TH439 |
| t11_miss_pi | TH436 |
| t11_miss_pi_real | TH437 |
| t11_pow_le_exp | LM241 |
| t12 | TH110 |
| t12(i.a)probabilisticstep | CJ312 |
| t12(i.a)reduction | TH456 |
| t12(iv.b)componentinstance | CE182 |
| t12(iv.d)coverageofresource_limit | RF234 |
| t12(oldlabel) | CJ106 |
| t12_plan | CJ312 |
| t12hstep | CJ312 |
| t12invariancealgebra | LM248 |
| t12one-stepresample-moveidentity | LM249 |
| t12round-kernelinvariance | CJ313 |
| t13 | TH111 |
| t14 | TH112 |
| t14(i) | TH112 |
| t14-d | TH109 |
| t14-h | TH115 |
| t14-hone-move-additioniid-cheapclauseforallpolynomialp | RF107 |
| t15 | TH113 |
| t15(i')se-only | RF106 |
| t15(oldlabel) | TH114 |
| t15route | TH244 |
| t16 | CJ103 |
| t16(oldlabel) | TH116 |
| t17 | CJ104 |
| t17(oldlabel) | CJ108 |
| t18 | CJ105 |
| t18' | CJ107 |
| t18'slotconstants1/(s0!d!) | RF117 |
| t18(oldlabel) | TH117 |
| t19 | CJ106 |
| t19(oldlabel) | TH118 |
| t19tiera | RF118 |
| t2 | TH102 |
| t20 | TH114 |
| t20(i) | TH114 |
| t20(ii) | TH114 |
| t20(v)counterexample | CE101 |
| t20-c(oldlabel) | TH119 |
| t21 | TH115 |
| t21(c1) | TH422 |
| t21(iv)'misswitheta_n->0fails' | RF108 |
| t21(oldlabelt14-h) | TH277 |
| t21-e | CJ109 |
| t21-e' | TH239 |
| t21-h | CJ110 |
| t21-x | CJ111 |
| t21_c1 | TH422 |
| t21_decomposition | TH419 |
| t21_decomposition' | TH420 |
| t21_event_subset | LM231 |
| t21_t14h_hpm_composition | TH277 |
| t21c1 | TH422 |
| t21decomposition(l-leanbriefform) | TH420 |
| t21decomposition(sharpform) | TH419 |
| t21route(e') | TH239 |
| t21route(e)hypothesish24 | RF182 |
| t21routes(a)-(f) | TH277 |
| t22 | TH116 |
| t22(i)(ii)(iv) | TH116 |
| t22(i)vacuousateveryn<=3,200ins3/s4/s6 | RF158 |
| t22(iii) | TH116 |
| t22(iii)fors3/s4/s6 | CJ141 |
| t22(iii)unconditionalinbo | TH138 |
| t22(iii)° | TH139 |
| t22(iv)existenceclaimforusableupperbounds | RF109 |
| t22(oldlabel) | TH120 |
| t23 | TH117 |
| t23(ii) | TH117 |
| t23-c | CJ112 |
| t23-n | CJ113 |
| t23-r | CJ115 |
| t23-s | CJ114 |
| t24 | CJ107 |
| t24(i)inputs | CJ120 |
| t24(t18') | CJ180 |
| t24fromlat-neighbourhoodswithphi<=2scoredwithinoneortworounds | CJ177 |
| t24gtheoremb | TH218 |
| t25 | TH118 |
| t25(iv) | TH118 |
| t25(iv)b_twiththoseconstants | RF236 |
| t26 | CJ108 |
| t26(i)-(ii)premiseform | TH295 |
| t26-exact-branch-paren | RF225 |
| t26-lemma1 | LM198 |
| t26-lemmas2-3(lemma2) | LM199 |
| t26-lemmas2-3(lemma3) | LM200 |
| t26-propc | TH325 |
| t26-thma | TH295 |
| t26-thmb | TH296 |
| t26bud-g | TH370 |
| t26dischargedform | TH296 |
| t26exact-branchaside | RF225 |
| t27 | TH119 |
| t27(i) | TH119 |
| t27(i)fromchainleakage | TH142 |
| t28 | CJ109 |
| t29 | CJ110 |
| t3 | TH103 |
| t30 | CJ111 |
| t31 | TH120 |
| t31(i) | TH120 |
| t32 | CJ112 |
| t32(c) | TH294 |
| t32(c)log^3 | CJ208 |
| t32(i) | CJ112 |
| t32(i)fp-pilotaddendum | TH347 |
| t32(i)isaconjecture(stalestatusinw6-fixrev1k1andw7-sepi11) | RF219 |
| t32(i-lit) | TH294 |
| t32-fp | TH347 |
| t33 | CJ113 |
| t33(i)generalised | LM206 |
| t33-errbound | RF244 |
| t33-s | TH343 |
| t34 | CJ114 |
| t35 | CJ115 |
| t36 | CJ116 |
| t37 | CJ117 |
| t37(i) | RF101 |
| t37(i)-(iii)asfiled | RF165 |
| t37(iii) | RF165 |
| t37-a | TH199 |
| t37a4remainingclauses | CJ316 |
| t37a5relationtoliteraltd | CJ317 |
| t37explainsn=200maskedsuccesses | RF177 |
| t37theoremb(finite-nbound)andtheoremc(asymptotics) | CJ318 |
| t37wiring | TH279 |
| t38 | CJ118 |
| t38(0) | TH281 |
| t38(0_h) | TH282 |
| t38(a) | CJ118 |
| t38(a)andt32(i)asbvsinstancesofmathews-schmidlerthm1 | CJ283 |
| t38(b) | CJ118 |
| t38(b)-r | TH241 |
| t38(b)-rcomposition | TH241 |
| t38(b)atn=200 | CJ237 |
| t38(b)onlh-iid | TH156 |
| t38(b)withoutls0onlh,pfixed | TH263 |
| t38(b)withoutls0viabg1 | TH262 |
| t38(b1)premisesatn=200 | CJ227 |
| t38(b2)onlhexactgramnotweak | TH267 |
| t38(c) | CJ118 |
| t38-(0) | TH281 |
| t38-(0)asfinitebooleanlemma | CJ322 |
| t38-(a) | TH283 |
| t38-(b1') | TH285 |
| t38-(b1) | TH284 |
| t38-(b2) | TH286 |
| t38-(c) | TH289 |
| t38-b1' | TH285 |
| t38-b1-lh | TH287 |
| t38-b1-lh-iid | TH288 |
| t38-b1-lh-iid(lh-iidfamily) | TH160 |
| t38-b1-lh-iidfail | RF217 |
| t38-b2 | TH286 |
| t38-recordv3 | TH290 |
| t38-v3 | TH290 |
| t38_statementv3 | TH290 |
| t38b-r(b1') | TH241 |
| t38b-r(b1) | TH241 |
| t38b-r(b2) | TH241 |
| t38b-r(whole) | TH241 |
| t38correctedstatement(v2) | TH292 |
| t38paper-readystatement(v1) | TH291 |
| t38route(a)undercommonsigma-hat^2,nols0 | TH188 |
| t39 | CJ119 |
| t4 | TH104 |
| t5(iii)additivebandasthemainstatement | RF111 |
| t5-c | TH106 |
| t5-s | CJ101 |
| t6 | CJ102 |
| t7 | TH107 |
| t8 | TH110 |
| t9 | CJ103 |
| t_elog1.925 | RF143 |
| t_n<=c1+c2log(1/delta_n)followsfromtherulesalone | RF259 |
| t_n=o_p(1)inthefavourableregime | CJ161 |
| taskclause(a) | RF262 |
| tau_2 | TH230 |
| td | CJ129 |
| td'_p(r_{a,d})underpgd | TH203 |
| td'_piff(l)andalld_s | RF169 |
| td'_pistheweakest | RF170 |
| td'latticeconditionats° | TH153 |
| td(d,0) | CJ129 |
| td(d,0)failurecf1/cf2 | CE159 |
| td(d,0)ford>=1 | RF165 |
| td(d,0)w.p.->1 | RF165 |
| td(d,m) | CJ129 |
| td(d,m)failsuniversally | TH247 |
| td(d,m)literal | RF101 |
| td*route | TH279 |
| td-prime(later) | CJ129 |
| tddataaudit | CE103 |
| tdp-iff-ds | RF169 |
| tdp_of_tdp' | LM251 |
| temperingisneeded | RF104 |
| th101 | TH101 |
| th102 | TH102 |
| th103 | TH103 |
| th104 | TH104 |
| th105 | TH105 |
| th106 | TH106 |
| th107 | TH107 |
| th108 | TH108 |
| th109 | TH109 |
| th110 | TH110 |
| th111 | TH111 |
| th112 | TH112 |
| th113 | TH113 |
| th114 | TH114 |
| th115 | TH115 |
| th116 | TH116 |
| th117 | TH117 |
| th118 | TH118 |
| th119 | TH119 |
| th120 | TH120 |
| th141 | TH121 |
| th142 | TH122 |
| th143 | TH123 |
| th144 | TH124 |
| th145 | TH125 |
| th146 | TH126 |
| th147 | TH127 |
| th148 | TH128 |
| th149 | TH129 |
| th150 | TH130 |
| th151 | TH131 |
| th152 | TH132 |
| th153 | TH133 |
| th154 | TH134 |
| th155 | TH135 |
| th181 | TH136 |
| th182 | TH137 |
| th183 | TH138 |
| th184 | TH139 |
| th185 | TH140 |
| th186 | TH141 |
| th187 | TH142 |
| th188 | TH143 |
| th189 | TH144 |
| th190 | TH145 |
| th191 | TH146 |
| th192 | TH147 |
| th193 | TH148 |
| th194 | TH149 |
| th195 | TH150 |
| th196 | TH151 |
| th197 | TH152 |
| th198 | TH153 |
| th199 | TH154 |
| th200 | TH155 |
| th201 | TH156 |
| th202 | TH157 |
| th203 | TH158 |
| th204 | TH159 |
| th205 | TH160 |
| th206 | TH161 |
| th207 | TH162 |
| th208 | TH163 |
| th209 | TH164 |
| th210 | TH165 |
| th211 | TH166 |
| th212 | TH167 |
| th213 | TH168 |
| th214 | TH169 |
| th215 | TH170 |
| th221 | TH171 |
| th222 | TH172 |
| th223 | TH173 |
| th224 | TH174 |
| th225 | TH175 |
| th226 | TH176 |
| th227 | TH177 |
| th228 | TH178 |
| th229 | TH179 |
| th230 | TH180 |
| th231 | TH181 |
| th232 | TH182 |
| th233 | TH183 |
| th234 | TH184 |
| th235 | TH185 |
| th236 | TH186 |
| th237 | TH187 |
| th238 | TH188 |
| th239 | TH189 |
| th240 | TH190 |
| th241 | TH191 |
| th242 | TH192 |
| th243 | TH193 |
| th244 | TH194 |
| th245 | TH195 |
| th246 | TH196 |
| th247 | TH197 |
| th261 | TH198 |
| th262 | TH199 |
| th263 | TH200 |
| th264 | TH201 |
| th265 | TH202 |
| th266 | TH203 |
| th267 | TH204 |
| th268 | TH205 |
| th269 | TH206 |
| th270 | TH207 |
| th271 | TH208 |
| th272 | TH209 |
| th273 | TH210 |
| th274 | TH211 |
| th275 | TH212 |
| th276 | TH213 |
| th277 | TH214 |
| th278 | TH215 |
| th279 | TH216 |
| th280 | TH217 |
| th301 | TH218 |
| th302 | TH219 |
| th303 | TH220 |
| th304 | TH221 |
| th305 | TH222 |
| th306 | TH223 |
| th307 | TH224 |
| th308 | TH225 |
| th309 | TH226 |
| th310 | TH227 |
| th311 | TH228 |
| th312 | TH229 |
| th313 | TH230 |
| th314 | TH231 |
| th315 | TH232 |
| th316 | TH233 |
| th317 | TH234 |
| th318 | TH235 |
| th319 | TH236 |
| th320 | TH237 |
| th321 | TH238 |
| th322 | TH239 |
| th323 | TH240 |
| th341 | TH241 |
| th342 | TH242 |
| th343 | TH243 |
| th344 | TH244 |
| th345 | TH245 |
| th346 | TH246 |
| th347 | TH247 |
| th348 | TH248 |
| th349 | TH249 |
| th350 | TH250 |
| th351 | TH251 |
| th352 | TH252 |
| th353 | TH253 |
| th354 | TH254 |
| th355 | TH255 |
| th356 | TH256 |
| th357 | TH257 |
| th358 | TH258 |
| th359 | TH259 |
| th360 | TH260 |
| th361 | TH261 |
| th362 | TH262 |
| th363 | TH263 |
| th364 | TH264 |
| th365 | TH265 |
| th366 | TH266 |
| th367 | TH267 |
| th368 | TH268 |
| th369 | TH269 |
| th370 | TH270 |
| th371 | TH271 |
| th372 | TH272 |
| th373 | TH273 |
| th374 | TH274 |
| th375 | TH275 |
| th376 | TH276 |
| th381 | TH277 |
| th382 | TH278 |
| th383 | TH279 |
| th384 | TH280 |
| th385 | TH281 |
| th386 | TH282 |
| th387 | TH283 |
| th388 | TH284 |
| th389 | TH285 |
| th390 | TH286 |
| th391 | TH287 |
| th392 | TH269 |
| th393 | TH272 |
| th394 | TH288 |
| th395 | TH289 |
| th396 | TH290 |
| th397 | TH241 |
| th398 | TH291 |
| th399 | TH292 |
| th400 | TH293 |
| th401 | TH294 |
| th421 | TH295 |
| th422 | TH296 |
| th423 | TH297 |
| th424 | TH298 |
| th425 | TH299 |
| th426 | TH300 |
| th427 | TH301 |
| th428 | TH302 |
| th429 | TH303 |
| th430 | TH304 |
| th431 | TH305 |
| th432 | TH306 |
| th433 | TH307 |
| th434 | TH308 |
| th435 | TH309 |
| th436 | TH310 |
| th437 | TH311 |
| th438 | TH312 |
| th439 | TH313 |
| th440 | TH314 |
| th441 | TH315 |
| th442 | TH316 |
| th443 | TH317 |
| th444 | TH318 |
| th445 | TH319 |
| th446 | TH320 |
| th447 | TH321 |
| th448 | TH322 |
| th449 | TH323 |
| th450 | TH324 |
| th451 | TH325 |
| th461 | TH326 |
| th462 | TH327 |
| th463 | TH328 |
| th464 | TH329 |
| th465 | TH330 |
| th466 | TH331 |
| th467 | TH332 |
| th468 | TH333 |
| th469 | TH334 |
| th470 | TH335 |
| th471 | TH336 |
| th472 | TH337 |
| th473 | TH338 |
| th474 | TH339 |
| th475 | TH340 |
| th476 | TH341 |
| th477 | TH342 |
| th478 | TH343 |
| th479 | TH344 |
| th480 | TH345 |
| th481 | TH346 |
| th482 | TH347 |
| th501 | TH348 |
| th502 | TH349 |
| th503 | TH350 |
| th504 | TH351 |
| th505 | TH352 |
| th506 | TH353 |
| th507 | TH354 |
| th508 | TH355 |
| th509 | TH356 |
| th510 | TH357 |
| th511 | TH358 |
| th512 | TH359 |
| th513 | TH360 |
| th514 | TH361 |
| th515 | TH362 |
| th516 | TH363 |
| th517 | TH364 |
| th518 | TH365 |
| th519 | TH366 |
| th520 | TH367 |
| th521 | TH368 |
| th522 | TH369 |
| th523 | TH370 |
| th524 | TH371 |
| th525 | TH372 |
| th526 | TH373 |
| th527 | TH374 |
| th528 | TH375 |
| th529 | TH376 |
| th530 | TH377 |
| th531 | TH378 |
| th532 | TH379 |
| th541 | TH380 |
| th542 | TH381 |
| th543 | TH382 |
| th544 | TH383 |
| th545 | TH384 |
| th546 | TH385 |
| th547 | TH386 |
| th548 | TH387 |
| th549 | TH388 |
| th550 | TH389 |
| th551 | TH390 |
| th552 | TH391 |
| th553 | TH392 |
| th554 | TH393 |
| th581 | TH394 |
| th582 | TH395 |
| th583 | TH396 |
| th584 | TH397 |
| th585 | TH398 |
| th586 | TH399 |
| th587 | TH400 |
| th588 | TH401 |
| th589 | TH402 |
| th590 | TH403 |
| th591 | TH404 |
| th592 | TH405 |
| th593 | TH406 |
| th594 | TH407 |
| th595 | TH408 |
| th596 | TH409 |
| th597 | TH410 |
| th598 | TH411 |
| th599 | TH412 |
| th600 | TH413 |
| th601 | TH414 |
| th602 | TH415 |
| th603 | TH416 |
| th604 | TH417 |
| th621 | TH418 |
| th622 | TH419 |
| th623 | TH420 |
| th624 | TH421 |
| th625 | TH422 |
| th626 | TH423 |
| th627 | TH424 |
| th628 | TH425 |
| th629 | TH426 |
| th630 | TH427 |
| th631 | TH428 |
| th632 | TH429 |
| th633 | TH430 |
| th634 | TH431 |
| th635 | TH432 |
| th636 | TH433 |
| th637 | TH434 |
| th638 | TH435 |
| th639 | TH436 |
| th640 | TH437 |
| th641 | TH438 |
| th642 | TH439 |
| th643 | TH440 |
| th644 | TH441 |
| th645 | TH442 |
| th646 | TH443 |
| th647 | TH444 |
| th648 | TH445 |
| th649 | TH446 |
| th650 | TH447 |
| th651 | TH448 |
| th652 | TH449 |
| th653 | TH450 |
| th654 | TH451 |
| th655 | TH452 |
| th656 | TH453 |
| th657 | TH454 |
| th658 | TH455 |
| th659 | TH456 |
| the541unrepairedcentresforcedbylemma0 | CJ224 |
| thebridgeisneeded | RF104 |
| theevidence:whatzhatcanandcannotdo | TH413 |
| theonlysequentialpartisthestagecount | RF269 |
| theorem-canalogueforfactor-dependentgroups | CJ149 |
| theorem1 | TH128 |
| theorem1(exp') | TH136 |
| theorem4(lockedt21) | TH277 |
| theorem4(o-swap) | TH340 |
| theorem4(restatedt21) | TH278 |
| theorem4composition(w5-lockbookstatements.tex) | TH278 |
| theorem5(0) | TH281 |
| theorem5(a) | TH283 |
| theorem5(b)headlinedecision | CJ215 |
| theorem5(b1') | TH285 |
| theorem5(b1) | TH284 |
| theorem5(b1-lh) | TH287 |
| theorem5(b1-lh-iid) | TH288 |
| theorem5(b2) | TH286 |
| theorem5(c) | TH289 |
| theorem5(t38)statementofrecord | TH290 |
| theorem5v1 | TH291 |
| theorem5v2 | TH292 |
| theorem6a | TH295 |
| theorema | TH199 |
| theorema(a1forward) | TH441 |
| theorema(a1reverse) | TH442 |
| theorema(a2)movecount | TH451 |
| theorema(a2abstract) | TH443 |
| theorema(a2concretelatticeform) | TH450 |
| theorema(a3)hpmclause(ledgerbound) | TH445 |
| theorema(a3)lattice-conditionversion | TH454 |
| theorema(a3)sharpcapl>=tau | TH453 |
| theorema(a3abstract) | TH444 |
| theorema(a3concrete,capl>=phi) | TH452 |
| theorema(a4)pdpart | TH448 |
| theorema(t26) | TH295 |
| theorema(w5-faviid) | TH190 |
| theorema1 | TH441 |
| theorema1_converse | TH442 |
| theorema2 | TH443 |
| theorema2_lattice | TH450 |
| theorema2_lattice_count | TH451 |
| theorema3 | TH444 |
| theorema3_hpm | TH445 |
| theorema3_lattice | TH452 |
| theorema3_lattice_only | TH454 |
| theorema3_lattice_tau | TH453 |
| theoremaforprogress-closedregions | LM153 |
| theoremb | TH218 |
| theoremb#(monotonelook-alikemap) | TH220 |
| theoremb' | TH219 |
| theoremb'(bsharpened) | TH219 |
| theoremb'/b# | TH220 |
| theoremb(restatedt24) | TH218 |
| theoremb(t37) | TH201 |
| theoremb(w5-faviid) | TH191 |
| theoremb-sharp | TH220 |
| theoremb1 | TH284 |
| theoremb2-lh | TH272 |
| theoremb2-w4 | TH254 |
| theoremb3 | TH181 |
| theorembg1 | TH255 |
| theorembg2 | TH257 |
| theorembg3 | TH258 |
| theorembheadline2^phi(s_c)statesno2^s0 | RF178 |
| theoremc(c1) | TH202 |
| theoremc(c1)containment | RF171 |
| theoremc(c2) | TH203 |
| theoremc(c2)noiseinequality | RF172 |
| theoremc(c4) | CJ170 |
| theoremc1 | TH326 |
| theoremc1(o-mix) | TH183 |
| theoremc2 | TH327 |
| theoremc3 | TH328 |
| theoremc4 | TH329 |
| theoremc6 | TH331 |
| theoremcd | TH416 |
| theoremd | TH414 |
| theoremd1 | TH244 |
| theoremd2 | TH242 |
| theoremd4 | TH248 |
| theoreme | TH171 |
| theoreme3 | TH243 |
| theoreme3' | TH240 |
| theoreme3corrected | TH240 |
| theoremf1 | TH264 |
| theoremf1' | CJ200 |
| theoremf2 | TH266 |
| theoremh | TH412 |
| theoremind-t | TH228 |
| theoreml | TH237 |
| theoreml(gibbs-pathrepaironlh) | TH237 |
| theoremn200 | TH334 |
| theoremnb'-lh | TH268 |
| theorempgd-w | TH204 |
| theoremr | TH174 |
| theoremr(restarttheoremforthepips) | TH303 |
| theoremr/p3'/p6'/p8'composition | TH161 |
| theorems2 | TH186 |
| theorems3 | TH187 |
| theorems4 | TH188 |
| theorems6 | TH189 |
| theoremsep(a) | TH380 |
| theoremsep(b) | TH382 |
| theoremsl | CJ274 |
| theoremsl(a)numbers | CE214 |
| theoremstg | TH415 |
| theoremt02(i#) | TH125 |
| theoremt02(ii#) | TH127 |
| theoremt05-g | TH135 |
| theoremt05-l | TH134 |
| theoremt05-u | TH132 |
| theoremt32(i) | TH294 |
| theoremt33-s | TH343 |
| theoremt38(b)-r | TH241 |
| theoremv | TH411 |
| theoremw | TH204 |
| theoremw' | TH363 |
| theoremw(d)uppersidewindowp^r/sqrtn->0butp^rsqrt(logp)/sqrtnnot->0 | CJ266 |
| theoremw(orth) | TH362 |
| theoremw_lat | TH214 |
| theoremwforp~nunderorth | CJ264 |
| theoremwgeneralbowithcorrelatedblocks | CJ263 |
| theoremwprime | TH363 |
| theoremwregionformcoversmaskedregime | RF176 |
| theoremws | TH362 |
| theoremws1 | TH348 |
| theoremws2 | TH349 |
| theoremws3 | TH350 |
| theoremws4 | TH351 |
| theoremws5.3(f) | TH353 |
| theoremws5.3(m) | TH354 |
| theoremws6(a)-(c) | TH355 |
| theoremws6(d) | TH356 |
| theoremws7 | TH357 |
| theoremwuniformform | TH212 |
| theoremwweightstability | TH362 |
| theoremz | TH413 |
| theory.mdrowt01 | TH101 |
| theory.mdrowt02 | TH102 |
| theory.mdrowt03 | TH103 |
| theory.mdrowt04 | TH104 |
| theory.mdrowt05 | CJ101 |
| theory.mdrowt06 | TH105 |
| theory.mdrowt07 | TH106 |
| theory.mdrowt08 | CJ102 |
| theory.mdrowt09 | TH107 |
| theory.mdrowt10 | TH108 |
| theory.mdrowt11 | TH109 |
| theory.mdrowt12 | TH110 |
| theory.mdrowt13 | TH111 |
| theory.mdrowt14 | TH112 |
| theory.mdrowt15 | TH113 |
| theory.mdrowt16 | CJ103 |
| theory.mdrowt17 | CJ104 |
| theory.mdrowt18 | CJ105 |
| theory.mdrowt19 | CJ106 |
| theory.mdrowt20 | TH114 |
| theory.mdrowt21 | TH115 |
| theory.mdrowt22 | TH116 |
| theory.mdrowt23 | TH117 |
| theory.mdrowt24 | CJ107 |
| theory.mdrowt25 | TH118 |
| theory.mdrowt26 | CJ108 |
| theory.mdrowt27 | TH119 |
| theory.mdrowt28 | CJ109 |
| theory.mdrowt29 | CJ110 |
| theory.mdrowt30 | CJ111 |
| theory.mdrowt31 | TH120 |
| theory.mdrowt32 | CJ112 |
| theory.mdrowt33 | CJ113 |
| theory.mdrowt34 | CJ114 |
| theory.mdrowt35 | CJ115 |
| theory.mdrowt36 | CJ116 |
| theory_prioritiesn=200disclosure:beta-minfailsbyabout100xinsquaredsignal | RF129 |
| thepilotlimitasafinite-comparisonrule | CJ116 |
| thesamplerisneeded | RF104 |
| thesamplerisneededfordiscoveryinthemaskedregime | RF264 |
| thesis/positioning:nobvsmethodisparallel+correlation-robust+stronglyguaranteed | CJ282 |
| thesiscd | TH416 |
| thesispremise"guarantees=>sequential" | RF268 |
| theta_n=n^-1,support{1} | CE188 |
| thethesissentence"correlationcostsonlydepthandparticles,nevercorrectness"isnotatheoremyet | CJ299 |
| thethesissentenceasatheorem | TH416 |
| thm-b1 | TH284 |
| thm-invgap1 | CJ298 |
| thm-invgap3 | CJ299 |
| thm-invgap4 | CJ300 |
| thm-invgap7 | CJ301 |
| thm-invremaininggaps2,5,6,8-12 | CJ302 |
| thm-syntha1(v)/thm-inv:r_n>~1/p(crossing)asaconsequenceoff-maskpipm3 | RF282 |
| thm-syntha2plainsentence | RF233 |
| thm-synththeoremz:"inthemaskedregimezhaterrsonlydownward" | RF233 |
| thm1-exp | TH136 |
| thm2-bo | TH138 |
| thm3(theorema) | TH199 |
| thm3-exp | TH141 |
| thm4'iff'gloss | RF135 |
| thm4(w2-book) | TH278 |
| thm4-c1 | TH278 |
| thm4-exp | TH142 |
| thm4-growl | TH142 |
| thm4-iff | RF135 |
| thm4finite-nform(k72) | TH334 |
| thm4route(d+) | TH279 |
| thm4route(e') | TH280 |
| thm4route(e-m) | TH280 |
| thm5(a)ons3/s4/s6 | TH197 |
| thm5(b1')lh-iidc=1 | TH159 |
| thm5(b1)lh-iidcorollary | TH156 |
| thm5(b1)withls0onlh-iidp>>n | TH161 |
| thm5(b1-lh)premises | TH144 |
| thm5(b1-lh-iid)(w5-vmaskform) | TH160 |
| thm5-lh | TH144 |
| thm6(p1)ons3/s4/s6 | TH196 |
| thm6-exp | TH140 |
| thm6a | TH295 |
| thm6b | TH296 |
| thmb# | TH220 |
| thmb-t24 | TH218 |
| thmb-t37(events) | TH201 |
| thmb-t37(incl) | TH201 |
| thmb3 | TH181 |
| thmc-c1 | TH202 |
| thmc-c2 | TH203 |
| thmc1 | TH183 |
| thmc2 | TH327 |
| thmc3 | TH328 |
| thmc4 | TH329 |
| thmc6 | TH331 |
| thmcd | TH416 |
| thmd | TH414 |
| thme | TH171 |
| thmh | TH412 |
| thmr | TH174 |
| thms2 | TH186 |
| thms3 | TH187 |
| thms4 | TH188 |
| thms6 | TH189 |
| thmsl | TH417 |
| thmstg | TH415 |
| thmv | TH411 |
| thmw | TH204 |
| thmz | TH413 |
| threedeficits | TH172 |
| threefacesofpi/pi0 | TH359 |
| thresholdlimit | TH134 |
| tie | TH217 |
| tielemma | LM148 |
| tierb'uniformcoupling | RF118 |
| tl | CJ127 |
| tl-sharp | TH234 |
| tl-sharpinrandomdesigns | CJ186 |
| tl_avg | CJ127 |
| tl_dandna_dw.p.->1 | TH202 |
| top-cmerge | LM226 |
| top-storeevidenceandpips | TH314 |
| transferlemma | LM124 |
| transferrule(t) | TH121 |
| trueposteriorsizecutoff | CJ131 |
| truncatedmomentandtailofbetastatistics | LM117 |
| truncatedmomentandtruncationevent | LM139 |
| truncatedsize-profileconvolution | TH409 |
| truthcontextchangesq-barby<=4-5%(perdesign) | RF156 |
| truthdominance | CJ117 |
| truthremovalatsupersets | TH230 |
| truthretention | LM180 |
| truthstabilityunderse | RF195 |
| ts | TH233 |
| ts(w) | TH233 |
| tscancellationpair | CE152 |
| tscounterexample | CE152 |
| tsfromse | RF195 |
| two-regimeconsistencyofthereportedhpm | CJ118 |
| two-sidedbandconditionalonpw2 | TH327 |
| two-sidedchainratiolaw | TH141 |
| two-sidedmaskedzhat | CJ302 |
| two-sidednon-asymptoticbound | TH317 |
| two-statefamily:l<=pibutt*->infinity | CE201 |
| two-stateinstance,c24_twostate.py | CE187 |
| two-stateinstanceofupwardzhatexcursions:w=99w.p.0.01 | CE219 |
| two-statesystem | CE104 |
| two-variableblockformula(truth+4equicorrelatedproxies) | CJ169 |
| two-variableblockviolatingthen1bound | CE125 |
| two-wayfailuredichotomy | RF168 |
| twocorrelatedgaussiannullsagainstlemmanparenthetical | CE127 |
| twospeeds | TH170 |
| u1constant | TH167 |
| udel(1) | TH231 |
| udel(a>=2) | TH232 |
| ulr | TH234 |
| unbiased_of_step | TH456 |
| unbiasednessgivencompletion | RF227 |
| underfittedmodelsareneverlocalmodesofthepapertargetonlh-g | TH402 |
| unifiedscoringanddiscoveryledger | TH109 |
| uniformactual-blockexpansion | CJ121 |
| uniformexit | RF102 |
| uniformexithypothesis | CJ120 |
| uniformlog-bfexpansion | LM168 |
| uniformlowerboundoft*bypathlengthwithoutregularity | RF261 |
| uniformpipswithout(l+4)rho*->0 | TH322 |
| uniformscoreapproximationonsmallsets | LM118 |
| uniformscorecomparisonunderpopulationmargins | LM190 |
| uniformscoreexpansiononpolynomialfamilyofsmallsets | LM123 |
| unimodalitybeyondp<=20 | CJ297 |
| union-modelprojectionbound | LM160 |
| unionboundoverhammingballsboundspi(x) | RF249 |
| unitstructure | LM183 |
| universalmemoryceilingp_max=theta(sqrtm0)(t23-s) | RF113 |
| unrestrictedlhno-ls0theorem | CJ206 |
| unscoredandunreportedmass | RF237 |
| upperboundonpi(x) | CJ230 |
| upperboundonz | CJ234 |
| usableupperbounds | CE107 |
| v+c-logaidentity | TH172 |
| v0 | TH241 |
| v1(thm-synth) | TH411 |
| v1-tdfails | RF101 |
| v11 | CJ218 |
| v2(thm-synth) | TH394 |
| v3(thm-synth) | TH397 |
| v37r2 | RF168 |
| v37r4printedgaussiantail | RF173 |
| v37r5repairedbound | LM160 |
| v3succeeds(citation) | TH385 |
| v5exactness | CJ302 |
| v5gibbsflip | TH405 |
| v5independencemove | TH408 |
| v5neighbourswap | TH407 |
| v5uniformswap | TH406 |
| val-fp | TH299 |
| val-fp(eta,epsilon) | TH299 |
| val-fpmeasurement | CJ221 |
| validatedarithmetic | CJ221 |
| validityofcommon-sigma-hat^2tables | TH182 |
| validityofv3.1underparallelexecution | TH411 |
| vanishing-signalsequence | CE188 |
| vanishingmargin | TH211 |
| var | CE143 |
| variantinvarianceoflockedidentitiesundercommonsigma-hat^2 | LM134 |
| vis | CJ127 |
| visfollowsfromgrsebm | RF120 |
| visibility | CJ127 |
| visibilityfromblockgain | LM113 |
| vmask-beyond-cliff | CJ145 |
| vmask-hetero-rho | CJ144 |
| vmask-lemmab-psi | CJ142 |
| vmask-psi-lt-1 | CJ143 |
| vmask-r1-nb | TH159 |
| vmask-r2 | TH167 |
| vmask-r3 | TH168 |
| vmask-r5 | TH166 |
| vmask-r7 | TH169 |
| vmasklemmab(i') | LM126 |
| vpgd-equiv | TH216 |
| vpgd-lh-pgd | TH215 |
| vpgd-propg | CE139 |
| vpgd-props' | TH213 |
| vpgd-propt | TH217 |
| vpgd-r0 | TH211 |
| vpgd-r2 | TH212 |
| vpgd-r3 | LM161 |
| vpgd-r4 | CJ172 |
| vpgd-wlat | TH214 |
| vpgdlh-lat | TH293 |
| w'idealgrid | TH363 |
| w(a)-(g) | TH362 |
| w+(s°)=w(s°)∪{x-j+b'} | RF210 |
| w1'underweak-signalmaskingpi(s0)isalsosmall' | RF142 |
| w1-expescalation3 | RF136 |
| w1-explemma1.1 | LM109 |
| w1-explemma1.2 | LM110 |
| w1-explemma1.3 | LM111 |
| w1-explemma1.4 | LM112 |
| w1-explemma2.3 | LM113 |
| w1-explemma4.1 | LM114 |
| w1-explemma4.2 | LM115 |
| w1-explimitlawofmstat | TH143 |
| w1-expprop2.1 | TH139 |
| w1-expprop2.2 | TH139 |
| w1-expthm1 | TH136 |
| w1-expthm2 | TH138 |
| w1-expthm3 | TH141 |
| w1-expthm4 | TH142 |
| w1-expthm5 | TH144 |
| w1-expthm6 | TH140 |
| w1-expweak-signalmaskingexplainsn=200 | RF151 |
| w1-t03rdisclosure:theproofdeterministicthresholdsstartnearn=1.2e5 | RF123 |
| w1-t03rproofsection7remark3 | CJ133 |
| w1-t03rwording:serestrictedtothecomparisonunionsactuallyused(notallsubsets) | RF128 |
| w1-t38esection7 | TH241 |
| w1cardt22(iii)iiddesigns | CJ141 |
| w1evidencenon-productionpi0 | RF196 |
| w1headline6 | RF137 |
| w1pc1e4sl_sample_cov_cex | CE211 |
| w1repairfamilywitha=neighbourgraph | RF192 |
| w1sec1.5 | CJ151 |
| w1section6premises | TH238 |
| w1section6premisesimplyh*eta->0 | RF191 |
| w1t37r-prop1 | TH198 |
| w2-book(iii') | TH424 |
| w2-bookguardliteralfull-outputclaim | RF215 |
| w2-bookprop1(i') | TH425 |
| w2-bookprop1dataparagraph:everycompletedwronghpmisaposteriormiss(f(s0)<=f(hpm)) | RF125 |
| w2-r(a) | TH378 |
| w2-r(b) | TH378 |
| w2-t26lemma1 | LM198 |
| w2-t26lemma2 | LM199 |
| w2-t26lemma3 | LM200 |
| w2-t26propositionc | TH325 |
| w2-t26theorema | TH295 |
| w2-t26theoremb | TH296 |
| w3-pgdlemma1.1 | LM150 |
| w3-pgdlemma1.2 | LM151 |
| w3-pgdlemma1.3 | LM152 |
| w3-pgdlemmag | LM158 |
| w3-pgdlemmar | LM157 |
| w3-pgdlemmau | LM159 |
| w3-pxnconjecturew' | CJ140 |
| w3-pxncorollary | TH156 |
| w3-pxnlemmab | LM116 |
| w3-pxnp1 | TH148 |
| w3-pxnp2 | TH149 |
| w3-pxnp3 | TH150 |
| w3-pxnp4 | TH151 |
| w3-pxnp5 | TH152 |
| w3-pxnp6 | TH153 |
| w3-pxnp7 | TH154 |
| w3-pxnp8 | TH155 |
| w3-pxnpropq | TH157 |
| w3-pxnpropw | TH158 |
| w3-vexpdilutionthreshold | TH147 |
| w3-vexppropd | TH146 |
| w3-vexpr1 | TH137 |
| w3-vexpr3 | TH145 |
| w3-vt38esection3.5 | LM187 |
| w4-t38fulllh-lat'm0issharp' | RF144 |
| w4-t38fullt38_statement | TH291 |
| w5-faviidsection10 | CJ155 |
| w5-faviidsection5openitem | CJ161 |
| w5-lockbookprop1(iii)paraphrase:anysame-sizem(s)>=m(s0)isanunrepairableerror | RF126 |
| w5-lockbookt32(i-lit)proofslip1+4l>=5l | RF245 |
| w5-vmaskr1 | TH159 |
| w5-vmaskr2 | TH167 |
| w5-vmaskr3 | TH168 |
| w5-vmaskr5 | TH166 |
| w5-vmaskr5table | CE179 |
| w5-vmaskr6 | LM126 |
| w5-vmaskr7 | TH169 |
| w5prop.b1 | TH193 |
| w6-fixrev1t38_statement | TH292 |
| w6f1-ce1' | CE145 |
| w6f1-d2inf | TH242 |
| w6f1-e3' | TH240 |
| w6f1-lemmap | LM166 |
| w6f1-lemmas' | LM170 |
| w6f1-lemmau' | LM168 |
| w6f1-nl0' | TH232 |
| w6f1-propu' | TH227 |
| w6f1-t38 | TH292 |
| w6f1-t38(0) | TH281 |
| w6f1-thmb-conv(conventions,beta_h) | TH218 |
| w6f2-t03 | TH128 |
| w6f2-theorema | TH199 |
| w7-partkappa_c=2i* | TH165 |
| w7-parttheorema | TH162 |
| w7-parttheoremb | TH163 |
| w7-parttheoremc | TH164 |
| w7-secengineerror_boundstresstest | CE194 |
| w7-secmeasuredt33numericalmarginsatn=200 | CJ246 |
| w7-secrecountoft32(i) | TH347 |
| w7-sect33-m | LM206 |
| w7ce1 | CE117 |
| w7ce1consequence | RF147 |
| w7ce2 | CE118 |
| w7ce2header | RF141 |
| w7lemma1 | LM127 |
| w7lemma2 | LM128 |
| w7lemma3 | LM129 |
| w7lemma3conditioningonbothnormalisedvectorcollections | RF140 |
| w7lemmaa0 | LM130 |
| w8-synth4.13numericalinconsistencies | CJ247 |
| w8-synth:o-ls0checkhasnotlanded | RF247 |
| w8-synthleancount | RF283 |
| w8-synthsection1decision3 | CJ239 |
| weak-signalmaskingconjecture | RF136 |
| weakcross-blockdependenceboundsweightvariance | RF256 |
| weakest-prose | RF170 |
| weakleakageimpliesfavourablestart | TH353 |
| weaksignal | RF136 |
| weaksignals | CJ279 |
| weightedunbiasedness | LM202 |
| whatthereportedchecksandcertificatesestablish | TH120 |
| whichgroupsshareablockwhen2g<=b | CJ146 |
| whole-modelassouad/fanofloor | CJ233 |
| whole-roundminorisation | TH107 |
| windowp^r=sqrt(n)/loglogn(check_sep_wf1) | CE202 |
| within-sizeswap | TH336 |
| withoutls0nomasked-regimeconsistencytheorem | RF212 |
| withoutls0thepaperhasnomasked-regimeconsistencytheoremwhosepremisesareallprovedonanexplicitfamily | RF218 |
| witnessesinb_n | CE110 |
| work,depthandwidthofv3.1 | TH414 |
| work/depth/width | TH399 |
| workerequivalenceofthecalibrationdiagnosticislands | TH395 |
| workerequivalenceofthefinalrun | TH394 |
| wprimeforthemethodv-restrictedpilotgrid | CJ265 |
| ws1 | TH348 |
| ws2 | TH349 |
| ws3 | TH350 |
| ws4 | TH351 |
| ws5.2 | TH352 |
| ws5.3(f) | TH353 |
| ws5.3(m) | TH354 |
| ws5.3(n) | TH353 |
| ws6(e) | CJ261 |
| ws8(d) | CJ262 |
| y1extension | CJ297 |
| ywj-typespectralgapforthepaperprioronlh-gwithcapk | CJ297 |
| z-hatcanonlyfaildownwardinthemaskedregime | RF233 |
| zbar0exact | TH409 |
| zero-dependenceobstruction | TH356 |
| zerocross-blockcorrelation,chi2diverges | CE199 |
| zeta-exit | RF120 |
| zhat-weightedestimatesofboundedfunctionals | TH412 |
| zhat-weightedpip | TH397 |
| zhou-yang-vats-roberts-rosenthaljrssb84(5)2022thm1 | CE212 |
| zjl+cs | TH234 |
| zyvrinformedchainwithparallelneighbourscoring | CE212 |
| φ_eq | LM255 |
| φ_le_of_mem_rad | LM247 |
| ⟦lemma0(a,c)⟧(a) | TH440 |
| ⟦lemma0(a,c)⟧(c) | TH446 |
| ⟦lemma2-t37⟧(a) | TH449 |
| ⟦prop2(a,b,d,e)⟧(leanpart) | TH456 |
| ⟦theorema⟧(a1) | TH441 |
| ⟦thm4-c1⟧(lean) | TH422 |
| ⟦thm4-c1⟧core | TH418 |
