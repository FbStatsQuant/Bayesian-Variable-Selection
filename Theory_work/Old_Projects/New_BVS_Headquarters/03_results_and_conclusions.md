> **Archive note.** In this archive, "02a" means `02_theory.md` (final state), "02b" means `02b_theory_campaign_history.md` (campaign history), and "REG-A"/"REG-B" or "registry A/B" mean parts A and B of `ID_REGISTRY.md`. Paths like `branch_snapshots/...` and `transcript/...` are relative to this folder.

# 03 · Results and conclusions (final theoretical state, empirical results, conclusions and confidence)

Archive of the T3 thread "New BVS Headquarters" (threadId `5e38497d-7dfd-48f9-88e9-b21895922f58`), 2026-11-02 to 2026-11-04. Companion files: `02_theory.md` (02a, final state), `02b_theory_campaign_history.md` (02b, campaign), `ID_REGISTRY.md (part A)` (REG-A), `ID_REGISTRY.md (part B)` (REG-B), `05_open_questions_and_next_steps.md` (05).

Conventions. IDs are written `ID (native name)`. Positions are `[pos N]` in `transcript/part_*.md`. Snapshot files are `branch_snapshots/<B>/<path>` (relative to `archive/`). Status words are copied from the sources and never upgraded. "SF" = same-family check (Claude checking Claude), "XF" = cross-family check (Astra A-REV1–A-REV9; PC1 = gpt-6.1-sol on Seats A, B, D; PC2 = Opus 5.5 on Seat C; "CHK" = PC1 on inherited proofs). Text labelled "Summary:" is editor text; everything in quotation marks is verbatim from the cited source. **UNCERTAIN:** marks a conflict between sources or something the sources do not settle.

Contents: §1 Final theoretical results. §2 Empirical results (numbers and files). §3 Conclusions and confidence. Open items are in 05.

---

# §1 Final theoretical results

## 1.0 State of the package, who checked what, what "approved" means

- Summary: the theorem meeting `branch_snapshots/MEET-THM/` closed with "Open questions: none" ([pos 1626]; `MEET-THM/MINUTES.md`). The list is 8 main cards TH01–TH08 (M1–M8) plus 12 supplement cards TH09–TH20, one dissolved card TH21 (S-STGI) and a scoped remark TH22 (Thesis CD, K96). The meeting considered 108 candidates; all were dispositioned: on the list, 27 in FUTURE_WORK (CJ01–CJ27), 6 dropped (DR01–DR06), or cited published results (CL01–CL23) ([pos 1650]; 02a §A4.5).
- HQ reviewed and approved the package with one change (growth rate (ii), RL06 (HQ approval amendment, growth rate (ii)), [pos 1639]). **Felipe had not approved the theorem list when the archive ends**: "I will take a look at the theorems and give you feedback / questions later" ([pos 1673]); 02a §A0.2, §A7 U12.
- The final audit of the package, `MEET-THM/CLOSE_AUDIT.md` (Sol 6.1 as auditor), is "PASS WITH CORRECTIONS (#4–#10; chair applies without another audit)". Its corrections that change reading: M5 δ₁ is pointwise in the deterministic clause (02a §A7 U5); N14(c) is IND-T extension, extra-search nesting is K84/N14(a); S-STGI dissolution propagated.
- Two cross-family check waves (PC1 on Seats A, B, D; PC2 on Seat C) and an inherited-proof check (CHK): "OWS-WS3/4 VERIFIED; WS6(d), WS7 and N9 VERIFIED WITH AMENDMENT" ([pos 1626]). HQ's plain-language statement: "Two rounds of proof checks by a different model family found 20 counterexamples in draft statements, and all were repaired or removed" ([pos 1650]).
- Method-side reviews (not theorem cards): Sol 2 audit (13 findings, 4 decision-level) and Sol 1 proof check (60 findings: 7 FALSE, 6 GAP) of the MEET-v31 documents; HQ dispositions in `MEET-v31/AMENDMENT_HQ_01.md` (73 findings: 45 changed, 28 no change; "No method decision changed") ([pos 1480], [pos 1512], [pos 1584]; `campaign/LEDGER.md` 02:05 UTC entry).
- **No main card is Lean-certified as a whole** (02a §A0.2). Every main card has a "Lean core" to be written (quoted per card below). Existing sorry-free Lean covers T21 (C1), T07, T11(iii) and T37(i)/Theorem A (see §1.4); M5 cites parts of these.
- Every "PROVED" on a card is a candidate unless it says "PROVED-LOCKED"; "PROVED-LOCKED" items (pre-campaign, `main@c4ef0dc`) are same-family only with "external review queued" ("SAME-FAMILY-ONLY", TH09/TH10 rows of REG-A). "Not adopted (adoption is Felipe's decision)" appears in the REG-B rows of the locked set.

## 1.1 The eight main cards

Source of the exact statements: `branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md` (TLF), Part I, quoted in full in 02a §A2. Source of the statuses: the card "Status (verbatim)" rows as copied in REG-A. Source of Lean/risk lines: TLF cards' "Lean core" and "Risk" rows.

### TH01 (M1 · Theorem V/H, validity of v3.1 and accuracy of reported bounded functionals)
- Positions: [pos 1550], [pos 1593], [pos 1626], [pos 1639], [pos 1650]. Binding proposal goals §5.1, §5.2, §13.1 ([pos 1650]).
- Summary: validity of v3.1 (island identities, frozen-𝓒 contract, output event) and accuracy of reported bounded summaries. Clauses (REG-A rows): TH01.a validity [cited], TH01.b Lemma N1, TH01.c contract, TH01.d output event, TH01.e islandwise bound, TH01.f finite-R′ bound, TH01.g declared classes, TH01.h decision transfer, TH01.i asymptotics with R′_n.
- Status per clause (verbatim):
  - TH01.a: "T12, T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N9K: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT".
  - TH01.b (Lemma N1, OB01 (N1)): "PROOF SKETCH". Binding §13.1: "if it fails the goal is not met by withdrawal; HQ escalates to Felipe" (OB01).
  - TH01.c: "CEX-guard: COUNTEREXAMPLE; W1PC1:127 AMBIGUOUS → 'need not' (W2PC1:92 REPAIRED)" (adaptive R′ or conditioning on completion need not keep the bounds).
  - TH01.d: "N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT); LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)); GUARD-W audit open". Statement: P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05, never conditional on 𝒪.
  - TH01.e/f: "PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r] = π(h) is still a premise'" (that premise is N1); "FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9))".
  - TH01.g: interval claim narrowed (W1PC1:263); posterior-content error only, no quantile claim (RL02 (HQ ruling Q2)).
  - TH01.h, TH01.i: "(h), (i): PROVED (by this seat, unchecked)"; i uses "T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2))" (TH09 (S-T, Theorem 1 target consistency)).
  - Other ingredients: "A1new: PROOF SKETCH (NEW-SYNTH)"; "IND-T: PROVED (SF: none; XF: VERIFIED* (A-REV1))"; "MA-PropP: PROVED (elementary), author-only".
- Checked by: SF for T12/T31(i) locked set and Prop2; XF A-REV4/6/9, A-REV1 for IND-T; PC1 CHK for N9; N1 and the assembly unchecked.
- Lean: planned "Lean core": "T12Core `unbiased_of_step` with `hstep` discharged for multinomial resampling + an invariant kernel; detailed balance of the four kernels (finite matrices); (e) deterministic step; (f) finite inequality on abstract nonnegative weights; (h) finite; CEX-guard as a two-point example." Existing: `T12Core.lean` is "yes, partial" (the probabilistic recursion `hstep` is an explicit hypothesis) (`L-LEAN/STATUS.md`).
- Caveats (TLF "Risk"): "N1 fails (binding §13.1); GUARD-W or IND-T extension audit fails (then (c),(d) stay potential-run statements)." (i) uses the optional stacking configuration, not the default four islands. **UNCERTAIN:** growth-rate (ii) R′_n = 4⌈(n+p)⁶/4⌉ is "kept only as a sufficient rate inside the theorem" (RL06) but the printed M1 text has only the log rate in (i): 02a §A7 U1.

### TH02 (M2 · Theorem WS, the §5.3 package)
- Positions: [pos 1614], [pos 1624], [pos 1626], [pos 1650]. Binding goal §5.3 with HQ rulings RL01 (HQ ruling Q1 (§5.3)) and RL05 (HQ ruling Q5 (stage count continuous in ε)).
- Summary: (a) discrepancy between start and posterior controlled by cross-block terms plus σ²-coupling (TH02.a1–a3); (b) bridge-form stability including the stage-count sandwich and a step-function statement (TH02.b1–b8); (c) the one-shot reading is false (TH02.c1, TH02.c2; Proposition ONE-SHOT).
- Status per clause (verbatim from REG-A): a3 "OWS-WS3, OWS-WS4: PROVED (SF: none; XF: none) + CHK 'VERIFIED (PC1, cross-family, line by line)'"; "FD-W1: PROVED, XF VERIFIED (A-REV4)"; a1/b5 "Seat C's D_* decomposition and actual-grid moment: PROOF SKETCH (NEW-COMP); W1PC2/W2PC2 TRUE-AS-WRITTEN (statement sanity, not a proof)"; b2–b4, b6 "(b2)–(b4), (b6) assemblies: PROVED (by Seats A/B/D, unchecked), W2PC1 TRUE-AS-WRITTEN"; b6′ "C8 pilot extension: PROOF SKETCH, unchecked (W2PC2 PLAUSIBLE); T26BUD-G: PROVED, deterministic, AUTHOR-ONLY"; b7 "PROVED (by this seat, unchecked)"; c1 "OWS-WS6d: PROVED (SF: none; XF: none) + CHK 'VERIFIED WITH AMENDMENT'"; c2 "OWS-WS7: PROVED (SF: none; XF: none) + CHK 'VERIFIED WITH AMENDMENT'". Not used: "OWS-WS6e: CONJECTURE; OWS-WS8d: OPEN".
- TH02.b8 verbatim: "T(ε) is a step function of ε. It can jump at critical thresholds: PC1 exhibits an actual design (n = 40, p = 2, B = 1) with one-sided baseline counts {2, 4} and T = 3 at ε = 10⁻⁵."
- Lean: planned "Finite-space: WS1(a) cumulant identity; the four-normaliser bound given sup|d − d′| ≤ η; the product-of-averages pathwise bound; the scalar log inequalities defining b_X and the Lipschitz algebra of (b7). Not Lean: (c) and the probability-in-the-design clauses."
- Caveats: "D_* route is a PROOF SKETCH: if the general matrix route stalls, prove on W directly (C's fallback). The useful scale is perturbative (ε ≲ n^{−1/2}/p): disclosed. Pilot-extension envelope unchecked as a proof: the checked fallback count stands." HQ's plain-language caveat: "the example family gives useful constants only for very weak cross-block correlation, of order ε ≲ n^(−1/2)/p" ([pos 1650]). The sharp ε-scale necessity is CJ22 (FW22).

### TH03 (M3 · Theorem START)
- Positions: [pos 1626], [pos 1650].
- Summary: deterministic start mass (TH03.a, TH03.b), exact factorization (c), dilution (d: −log π₀(S₀) = V + C − log A(|S₀|)), σ²-coupling decomposition (e), masked law on LH (f). Supplementary: TH03.K16 (T22(iii)).
- Status (verbatim, REG-A): "Status: deterministic: T22(i)(ii)(iv): **PROVED-LOCKED**. DIL-E: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. DIL-E1: **PROVED; SF: none; XF: VERIFIED* (A-REV9)**. Status: statistical: T27(i): **PROVED-LOCKED, CONDITIONAL**. Thm3/4-EXP: **PROVED; SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)**. Thm5-LH: **PROVED; SF: VERIFIED (W3-VEXP); XF: none; SAME-FAMILY-ONLY**. Status: coupling/assembly: OWS-WS3: **PROVED; SF: none; XF: none; AUTHOR-ONLY** in the inherited ledger; CHK separately records **VERIFIED (PC1, cross-family, line by line)**. Final assembly: **PROOF SKETCH, unchecked**."
- Lean: planned "finite products, prior ratios, logarithmic dilution identity, endpoint Hölder inequality and scalar shared-variance bounds. Gaussian asymptotics remain cited prose."
- Caveats (Risk): "Losing normalized reference mass; treating the capped start as independent blocks; confusing sample and population cancellation; exporting exact-Gram results to adaptive random packing." LH-only for the masked law (LIM03 (inherent limitation 3)).

### TH04 (M4 · Theorem Z𝒯 and the certificate card, with the masked-regime statement)
- Positions: [pos 1614], [pos 1626], [pos 1650]. Binding §5.4 (RL02 (HQ ruling Q2), RL03 (HQ ruling Q3, not binding, obligation with fallback)).
- Summary: deterministic brackets from the reported store (TH04.a, b), retention at δ₁ < ½ (c; ½ sharp), analytic envelope (d), output-event certificate (e: P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05), masked-regime statement (f), definitional facts (g).
- Status (verbatim, REG-A): "MZ-P3: 'PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery'; 'candidate: not reviewed, not adopted'; AUTHOR-ONLY. N13: PROVED (PC1 claim 5). PC1c5: (a) PROVED, ½ sharp. N17: PROVED (PC1 claim 1; PC2 C1(c)). PC1c2: PROVED for the potential run; N6(a) output form CORRECT WITH AMENDMENT; N6(b) PROVED modulo premise (i) (GUARD-W not audited). LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)). CEX-guard: COUNTEREXAMPLE (XF VERIFIED*). OCERT-C1: XF ERROR as quantified (O-VCERT R1 wording used). T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)). Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none), SAME-FAMILY-ONLY. T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)). (f) assembly: PROOF SKETCH (seat-assembled; W2PC1/W2PC2 TRUE-AS-WRITTEN as an assembly)."
- Lean: "(a)–(d): finite inequalities on a finite Ω; (e): finite event algebra given Lemma RO; (f): the containment is finite; the limits are prose."
- Caveats: "GUARD-W audit (N2(e)); N16 floating point; N3 (e4 DP) hypothesis in (f); SAME-FAMILY-ONLY on LH; MZ-P3 AUTHOR-ONLY." Each card number carries the label "numerical implementation of an exact-arithmetic certificate" until validated arithmetic and VAL-FP exist (MD10 (MEET-v31 decision 10)). Reading of (f): "vanishing P(output and error), not conditional success".

### TH05 (M5 · Theorem HPM)
- Positions: [pos 1626], [pos 1650]. Objective 3 (selection).
- Summary: TH05.0 composition at every n, any X: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n; TH05.a Theorem A / LS-score; TH05.b1LH reported HPM with LS0 on LH; labelled variants TH05.afav (a-fav) and TH05.b2LH (b2-LH, no LS0).
- Status (verbatim, REG-A): "Thm4-C1 'PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none)'; T38-(0) 'PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))'; N200 'PROVED (elementary, every n); Π(X) upper bound OPEN' (author-only); TheoremA 'PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2))'; LS-score 'PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8))'; T38-b1-LH 'PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))' (registry ⚑ CONFLICT on the iid sub-claim, excluded); Thm-b1 'PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8))'; T38-(a) 'PROVED-UNDER (SF: VERIFIED* (inputs); XF: none)'; B2E-B2LH 'PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7))'; STAB-cert(A7) 'REFEREE (Astra-authored)'; PART-ThmA 'PROVED (XF: VERIFIED* (A-REV9))'; N3 'OPEN'; Thm5-LH (input via M3) 'PROVED (SF: VERIFIED (W3-VEXP); XF: none)' SAME-FAMILY-ONLY. Assembly: PROOF SKETCH (by this seat, unchecked)."
- Campaign-era IDs: TH115 (T21, composition theorem for the reported HPM): "PROVED-LOCKED (C1 and routes (a)-(f), wave 2) + CONDITIONAL on open hypotheses: H24 (route (e)) …"; TH334 (Theorem N200): "PROVED (elementary, every n); author-only (no SF, no XF); Pi(X) upper bound OPEN"; TH199 (Theorem A); LM189 (LS-score).
- Fidelity: v3.1 with LS0 (METHOD #8) for (0), (a), (b1-LH); any frozen grid; (b2-LH) is v3 without LS0, labelled; (a-fav) is an iid-draw variant, labelled.
- Lean: existing sorry-free `T37Greedy.lean`, `T37Lattice.lean`, `T21HPM.lean` (`t21_C1`); "To add: the capped-scan certification interface (ℓ ≥ τ(C), completed scan ⇒ certified return) and (0) as a finite Boolean lemma with the output event."
- Caveats: "N3 OPEN (DP invariant); integrated-LS0 replay (N2(c)) pending; Π(X) only measured (K94 FW); study generator N8 uncovered (the g = 5 study is not the LH exhibit)." Premises of M5 largely fail at n = 200 (see §2.2: π₀(S̃₀) > ½ in 18 of 2,400 fits).

### TH06 (M6 · Theorem SEP + Lemma KL)
- Positions: [pos 1626], [pos 1650]. Thesis theorem ("why the merge alone fails") ([pos 1650]).
- Summary: start-only discovery obstruction: Q*_n = p²n draws needed on LH (TH06.a, TH06.b), singleton second-moment bound 1 + χ²(π‖π₀) ≥ b²/a (TH06.c), Lemma KL: KL(π‖π₀) ≥ b log(1/a) − log 2 (TH06.KL).
- Status (verbatim): "SEP-A/SEP-B: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. KL: **PROOF SKETCH (NEW-SYNTH)**, **AUTHOR-ONLY** in IDX. Statement checks remain TRUE-AS-WRITTEN; they do not upgrade KL. Final assembly: **PROOF SKETCH, unchecked**."
- Lean: "iid miss probability, singleton second-moment inequality, binary coarsening/log-sum inequality and entropy bound. Probability tightness arguments remain prose." (Existing `T11Miss.lean` formalises the iid miss probability (1 − π₀{s})^Q ≤ exp(−Qπ₀{s}) for TH109 (T11(iii)); whether it is reused for TH06.a is not stated in the sources: **UNCERTAIN**.)
- Caveats: "Replacing a lower bound by an asymptotic equality; confusing evidence variance with self-normalized variance; claiming probability failure from variance alone; claiming universal necessity of tempering." The claim "tempering is needed" was refuted on LH (RF104 ('Tempering (the sampler) is needed for discovery in the masked regime')): only "moving off the start is needed".

### TH07 (M7 · Theorem STG, stage laws of the coded grid)
- Positions: [pos 1624], [pos 1626], [pos 1650]. Objective 2.
- Summary: monotonicity/termination and greedy optimality among refinements (a), coverage identity (b), interval inequality and count T ≤ P + ⌈D_V/c_ρ⌉ + 1 (c), pilot-count T ≤ 2⌈D_*/c_ρ⌉ + 2 (c′), ideal-grid crossing log₂A₀ + O(1) (d, labelled, not the coded grid), cited limit √c·T*(c) → Λ_len (e), as-coded masked T_n is Conjecture P, OPEN → FUTURE_WORK (f, CJ06).
- Status (verbatim): "STG-G, STG-L0, STG-L1: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic (AUTHOR-ONLY, W2PC2:155); STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)), explicit decimal constants GAP (W2PC2 C14); STG-L: PROVED (SF: none; XF: none); ConjP: OPEN; STG-cexW2: COUNTEREXAMPLE; OWS-WS7(d): PROVED (SF: none; XF: none) + CHK VERIFIED WITH AMENDMENT; (b), (c): D/E proposals, TRUE-AS-WRITTEN (W1PC1:192–193); (c′): PROOF SKETCH (Seat C, unchecked), W2PC2 TRUE-AS-WRITTEN; STG-F: PROVED (SF: none; XF: none), cited only (K29 FW)." (e) "KNOWN—CITE Syed et al. 2024 Thm 3, Gelman–Meng 1998". Greedy optimality is Štefankovič–Vempala–Vigoda 2009 (CL05).
- Lean: "Lemma RS identity; Theorem G optimality among refinements of fixed targets; (b) identity; (c) finite inequality with the Popoviciu step; (d) two-state recurrence bound."
- Caveats: "The resolution/snap premises; the (c′) pilot-progress lemma unchecked; no compiled replay of the coded rule." Numerics: O-STAGES T* = log₂A₀ + 7.7 ± 0.4 (TLF row "Numerical companion").

### TH08 (M8 · Proposition D, island-level work, depth and width; no speed claim)
- Positions: [pos 1304], [pos 1626], [pos 1650]. Objective 2; compared with Song–Liang §6.
- Summary: final run work = R′·N_e·(T + L + 4)·m slots with island depth N_e·(T + L + 4)·m in ⌈R′/w⌉ waves (TH08.a); calibration (b); searches (c); polynomial work and Brent W/w + D (d); ceilings Θ(p) slots per round and Θ(p²) Gram memory not removed (e).
- Status (verbatim): "MA-PropD 'PROVED (counting, given the code's structure)' AUTHOR-ONLY; T32(i) 'PROVED (SF: VERIFIED (W7-SEC); XF: none)', displayed rate GAP (A-REV5), registry ⚑ CONFLICT marker carried; Cost-T38 'PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))'; calibration share 'seat-derived, unchecked' (N15); assembly PROOF SKETCH (by this seat, unchecked)."
- Fidelity: "island level, v3.1 as shipped; 'depth free of N, H, R' struck (MEET-v31 decision 6 = MD06 (MEET-v31 decision 6)); K88's particle-parallel critical path is v3.2 and not claimed."
- Lean: "The counting identity (sum of products over the inventory), the scan bound p + k*(p − k*) ≤ p + p²/4, and Brent's inequality as finite lemmas; low value but certifiable."
- Caveats: "The DAG audit finds an uncounted serial component …; then (a)/(b) are restated, not dropped." Seat D's alternative: Prop D in the supplement (main = 7); HQ recommends main ([pos 1650]; pending, see 05).

## 1.2 The supplement cards and remark (TH09–TH22), statuses verbatim from REG-A

| ID (native name) | Status words (verbatim) | Positions |
|---|---|---|
| TH09 (S-T · Theorem 1, target consistency T03♯) | "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY". Asymptotic, proof thresholds n ≳ 2·10⁶; beta-min constant ≥ 43× above executed signals (LOCKABLE_v2 row `T03♯`). | [pos 1626] |
| TH10 (S-TARGET · propriety, invariance, envelopes, exact branch, odds certificate) | "N17: PROVED. T01: PROVED-LOCKED (wave 3; external review queued); SAME-FAMILY-ONLY. Remaining assembly: PROOF SKETCH, unchecked. N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected)" | [pos 1626] |
| TH11 (S-BLOCKS · separation ⇒ groups kept; SIZE ⇒ equality) | "PART-ThmA: PROVED; SF none; XF VERIFIED*. Counting/graph assembly: PROOF SKETCH, unchecked. PART-pairing remains OPEN, excluded. PART-CE2: COUNTEREXAMPLE" | [pos 1626] |
| TH12 (S-KERNEL · N9 kernel facts, start sampler, minorisation) | "N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); T09: PROVED-LOCKED (wave 1); N3: OPEN; K22, K23, K103: PROVED (by this seat, unchecked)… C10 (K09): PROOF SKETCH, unchecked" | [pos 1626] |
| TH13 (S-IDENT · restricted-ESS coverage identity, TI/KL/TV calculus, C15-CI) | "C15-TV, C15-KL, C15-CI: PROOF SKETCH, unchecked (assembly); Independence-sampler foundation: KNOWN—CITE; S9: PROVED (by this seat, unchecked); OWS-WS1: PROVED (SF: none; XF: none)" | [pos 1626], [pos 1614] |
| TH14 (S-CERT · local search, certificate semantics, B&B soundness, perturbation lemma) | "N7 L1: CORRECT WITH AMENDMENT; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*)" (LM204 (Lemma M, OCERT-LemmaM)) | [pos 1626] |
| TH15 (S-OUT · output-event validity, worker equivalence, stacking) | "LemmaRO: PROVED; SF VERIFIED; XF VERIFIED*. CEX-guard: COUNTEREXAMPLE; XF VERIFIED*. N6 potential-run: PROVED; output form: CORRECT WITH AMENDMENT. GUARD-W: not audited" | [pos 1626] |
| TH16 (S-Z · evidence variance, masked tails) | "OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)); PC1c4: PROVED; T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)); T26 overall CONJECTURE" | [pos 1626] |
| TH17 (S-POOL · pooling rules, recording-marginal equal-weight bias comparison P1, R_eff) | "MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH; ADRAFT-ThmA Astra-only, cite Del Moral; OBG-LH-lock-general: XF ERROR" | [pos 1626] |
| TH18 (S-LIM · limitations as theorems) | "CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB: COUNTEREXAMPLE (constructions); INP I5 PROVED" | [pos 1626] |
| TH19 (S-REP · run-card reporting corollary: Ĵ and ε̂_×) | "Reporting assembly: PROOF SKETCH, unchecked. N1: PROOF SKETCH. PC1c3: PROVED, with N1 as premise. W2P2 C16 and repaired W2P1 T4/T5 are statement/route checks, not a full proof upgrade" | [pos 1626], [pos 1614] |
| TH20 (S-LEAK · leakage clauses (F), (S)) | "OWS-WS6(b): PROVED (SF: none; XF: none), PC1 B.D6(S) TRUE; the m lower bound: PROVED (by this seat, unchecked); (b6) OWS-WS53F: PROVED-UNDER (SF: none; XF: none); PC1 B.D6(F) TRUE / DESIGN-VERIFIED (D_B)" | [pos 1626] |
| TH21 (S-STGI) | "DISSOLVED (MINUTES §2.2, corrected)": K30 is TH07.d (M7(d)); K29 → CJ23 (FW23). Dissent DS03 (Dissent K29 / S-STGI, Seat D). | [pos 1626] |
| TH22 (Thesis CD, K96) | "remark, not a theorem"; "there is no retained non-corollary thesis sentence". The thesis sentence adopted at [pos 1044]: "In split-and-merge, correlation breaks correctness. In local-to-global SMC, correlation costs only sequential depth and particles, never correctness." | [pos 1044], [pos 1626] |

Cited published results (not numbered claims of paper 1) are CL01–CL23 (TLF Part III), e.g. CL13 (Rossell 2022 Prop 1, the 2E₀δ₁ term), CL05 (Štefankovič–Vempala–Vigoda 2009), CL06 (Syed et al. 2024 Thm 3), CL03 (Del Moral; Whiteley–Lee–Heine 2016; Dai et al. 2022), CL23 (LIT-PAR G4, Song–Liang numerical comparison, "labelled numerical evidence").

### Headline campaign-era results behind the cards (REG-B IDs)
| ID (native name) | Status (exact words, abridged by the registry) |
|---|---|
| TH115 (T21; composition theorem for the reported HPM) | "PROVED-LOCKED (C1 and routes (a)-(f), wave 2) + CONDITIONAL on open hypotheses: H24 (route (e)) and the route-specific occurrence / exposure conditions; not adopted" |
| TH422 (t21_C1; Lean) | "Lean: sorry-free (lake build green, 0 sorry); Fable 5.1 GREEN; Astra r1 GREEN (statement fidelity only)" |
| TH334 (Theorem N200) | "PROVED (elementary, every n); author-only (no SF, no XF); Pi(X) upper bound OPEN" |
| TH106 (T07, Bayes decisions / size-only ceiling) | "PROVED-LOCKED (all parts, wave 3); not adopted" (Lean-checked, §1.4) |
| TH109 (T11, scoring and discovery ledger; T11(iii)) | "PARTLY PROVED: (iii) PROVED-LOCKED (wave 1); (i), (ii), (iv)-(vii) not locked (CONJECTURED)" |
| TH199 (Theorem A, refined T37(i)) | "PROVED (W6-FIXREV2 candidate); SF VERIFIED (W3-VT37R, 720 designs 0 violations); XF VERIFIED* (A-REV2 A1-A4 and POS-repaired A5; original A5(a) ERROR)" |
| LM189 (LS-score) | "PROVED; SF VERIFIED (W5-VMASK row 20); XF VERIFIED* (A-REV8 …; move count 'at most Phi(C0)-1' ERROR at C0=S0, repaired to max{Phi(C0)-1,0})" |
| LM204 (Lemma M, OCERT-LemmaM) | "PROVED; SF VERIFIED (O-VCERT: 0 violations in 476,160 exhaustive pairs); XF VERIFIED in exact arithmetic (A-REV9); LOCKABLE_v2" |
| TH394 (Proposition W, concurrent islands) | "PROVED (code reading; executed check …)"; author-only; executed on smoke + 3/3 designs (see §2.5) |
| TH395 (Proposition W-cal) | "PROVED (code reading only; not executed)"; still not executed at MEET-v31 close |

## 1.3 Verification infrastructure: LOCKABLE, registry, conflicts

- **LOCKABLE_v2** (`T38-RECORD/LOCKABLE_v2.md`): "**Counts:** 55 strict candidates · 3 repaired by W6 but not re-reviewed · 43 same-family-only · 43 cross-family-only · 6 counterexamples confirmed by both · 5 conditional implications verified by both." Rule (strict): "author status PROVED (not PROVED-UNDER) and same-family verdict VERIFIED (or VERIFIED after repair) and cross-family verdict VERIFIED (or VERIFIED with qualification)". HQ phrased it: "55 results are proved and checked by both families (the LOCKABLE list), and 431 claims are tracked in the registry" ([pos 929]). The file "lists candidates; it does not adopt, lock or upgrade anything". Locking is Felipe's decision.
- **REGISTRY_v2** (`T38-RECORD/REGISTRY_v2.md` §A1): "431 named results in the main table (§B) plus 49 flagged sub-claims". By author status: PROVED 256, PROVED-UNDER 51, PROOF SKETCH 42, COUNTEREXAMPLE 34, CONJECTURE 29, OPEN 9, REFEREE 10. By verification level: XF-VERIFIED 118, XF-ADVERSE 46, SF-VERIFIED only 53, SF-ADVERSE only 3, REFEREE-AUTHORED 19, UNVERIFIED 192.
- **Conflicts**: REGISTRY_v2 §A2 lists C1–C26 (26 conflicts; reproduced in 02b Part II P.1). **UNCERTAIN:** the registrar index `theory/MEET-THM-REG` (`campaign/LEDGER.md`, 2026-11-04 00:50 UTC entry) reports "24 draft entries, 166 cited IDs (51 author-only), 25 Lean files (library 101 results, 0 sorry), 37 conflicts"; 26 (REGISTRY_v2, campaign registry) and 37 (MEET-THM registrar index) refer to different registries and are not reconciled.
- **W8-SYNTH §4** lists 15 conflict groups (02b P.4). The F-REFEREE verdict ("major revision") and its 8 major points: "0 of its 8 major points are fully addressed, 6 are in progress and 2 are open" at [pos 796].
- **Standing caveat** (REGISTRY_v2 header): "F-REFINE's CARDS/ARCHITECTURE were written before A-REV1/A-REV2 existed, so their 'VERIFIED' is same-family only. None of this is adopted; locking is Felipe's decision."

## 1.4 The Lean library (`branch_snapshots/L-LEAN/`)

- `L-LEAN/STATUS.md`: "`lake build` is green: 0 errors, 0 warnings, 0 `sorry`. A per-declaration list (101 declarations) is in `DECL_STATUS.md`" (Lean `v4.35.0-rc2`, Mathlib rev `065356127b1d`). `L-LEAN/REPORT.md`: "`#print axioms` shows only `propext`, `Classical.choice` and `Quot.sound` for all 56 audited declarations, and no `sorryAx`". **UNCERTAIN (wording only):** the task statement and HQ at [pos 796] say "101 theorems/declarations", the registrar says "library 101 results"; the Lean sources say 101 declarations, of which 56 were audited for axioms.
- Sorry-free targets: **T21 (C1)** (`T21HPM.lean`: `hpm_eq_truth`, `t21_event_subset`, `t21_decomposition`, `markov_half`, `t21_C1` = P(U ∨ Ŝ≠S₀) ≤ P(U) + 2Eδ₁ + P(Uᶜ, S₀∉𝒮), the T21 inequality, REG-B TH422 (t21_C1; Lean)); **T07** (`T07Bayes.lean`: ceiling, `no_size_prior_repairs`, HPM minimises 0–1 loss, MPM minimises Hamming loss, reported-model clauses; REG-B TH106 (T07)); **T11(iii)** (`T11Miss.lean`: `t11_miss_pi`, `t11_miss_iid`, (1 − π₀{s})^Q ≤ exp(−Qπ₀{s}); REG-B TH109 (T11)); **T37(i) / Theorem A** (`T37Greedy.lean`, `T37Lattice.lean`: Lemma 0, A1–A4, concrete lattice forms; REG-B TH199 (Theorem A)).
- **T12(i.a)** (`T12Core.lean`): "yes, partial": invariance algebra, one-step resample–move identity and induction are sorry-free; "**The resample–move recursion `hstep` is an explicit hypothesis**: the probabilistic island model is not formalised. Plan: `T12_PLAN.md`."
- Fidelity: Fable 5.1 GREEN (`fidelity/FABLE.md`); Astra (xhigh) round 1 GREEN on T21, T07, T11, T12 and RED on T37 coverage only; new theorems added with no frozen statement changed; Astra round 2: "all three objections resolved: OVERALL (T37) GREEN" (`fidelity/ASTRA_round2.md`). Every frozen statement passes `stmtdiff.py` against `frozen/v1/` ("RESULT OK 0" for all 7 files).
- Meaning for the cards: the Lean files are abstract finite versions. They do not certify M1–M8; the cards' "Lean core" rows say what to add (quoted in §1.1).

---

# §2 Empirical results (numbers and the files that hold them)

Paths are relative to `branch_snapshots/` unless they begin `Results/` or `Docs/` (the repository `C:/Users/felip/Bayesian-Variable-Selection`).

## 2.1 The 2,400-fit production study (PROD-H; "v3 study", stands as v3.1 with 4 islands)

- Design (S-ELS, API-RESID): n = 200, p ∈ {500, 1000}, scenarios S1–S6, 100 replicates, c ∈ {1, 0.5} (signal scale), s₀ = 14, B = 14, K = 100; 6 × 100 × 2 × 2 = 2,400 fits (1,200 regenerated datasets × 2 scales). Files: `Results/SMC_BVS_v3_production/HEADLINE_TABLES.md`, `.../p0500/`, `.../p1000/`, `exact_recovery_long.csv`; ledger classification `S-ELS/REPORT.md`; run id `20261030T0934Z_prodH`.
- Classification (`S-ELS/REPORT.md` §3), 2,400 fits:

| p | c | exact recovery | posterior miss | search miss | stopped (no final ledger) |
|---|---|---|---|---|---|
| 500 | 0.5 | 370 | 230 | 0 | 0 |
| 500 | 1 | 559 | 40 | 0 | 1 |
| 1000 | 0.5 | 340 | 258 | 0 | 2 |
| 1000 | 1 | 560 | 37 | 0 | 3 |
| **all** | | **1,829** | **565** | **0** | **6** |

  The 6 stopped fits are `resource_limit`, all in S5. "In all 2,394 completed fits the final local search made 0 moves: E3 never fired, the HPM never changed, and every search ended `no_improvement`, `local_certified = TRUE`, `local_limit = FALSE`." "**S₀ was scored by the fit in all 2,394 completed fits**": it is in the 20,001-model top store (store F(S₀) equals the offline F(S₀) to 1e-12). "The event E_LS … is empty in the data (0 of 2,394)". For all 565 posterior misses F(S₀) < F(Ŝ) strictly (smallest margin 0.0049; 23 within 0.1; 0 ties). The 541 fits with S_c ∈ 𝓡₂∖{S₀} have median gap −1.33 (range −9.05 to −0.0049); 434 have S₀ one move away. Other ledger facts: E1 0 times, E2 83 times (10 among posterior misses), `local_limit` 0.
- Exact-recovery comparison (`Results/SMC_BVS_v3_production/HEADLINE_TABLES.md`; totals /600 for p = 500 and p = 1000):

| method | c = 1 (p500 / p1000) | c = 0.5 (p500 / p1000) |
|---|---|---|
| SMC-BVS v3 (HPM) | 559 / 560 | 370 / 340 |
| SMC-BVS v3 (PIP>0.5) | 559 / 561 | 338 / 321 |
| SuSiE | 585 / 582 | 220 / 205 |
| Spike-and-slab LASSO (SSL) | 569 / 582 | 303 / 255 |
| Horseshoe | 574 / 575 | 185 / 136 |
| SSL-RS (suppl.) | 593 / 592 | 32 / 32 |
| ABESS / L0 (EBIC) | 365 / 323 | 254 / 186 |

  HQ's reading ([pos 933]): "At c = 1, SMC-BVS is slightly behind on exact recovery … At c = 0.5 it is clearly the best … the paper should pitch exactly that, and not claim to beat everything." F-REFEREE §4: the c = 1 misses are "mostly supersets"; the comparison is "a comparison of *targets* as much as of *algorithms*". **UNCERTAIN:** HQ at [pos 933] quotes SSL at c = 1 as 569/582, which is the Spike-and-slab LASSO row; the supplementary SSL-RS row is higher (593/592). HQ also notes no head-to-head Ẑ/PIP comparison against other Bayesian methods exists.
- Per-cell MPM-vs-HPM counts for the 2,394 completed fits (`MEET-v31/evidence/2026-11-03_pip_rescore/REPORT.md` Part B): MPM_eq = S₀ in 1,779, HPM = S₀ in 1,829.
- "Limitation LIM07 (Inherent limitation 7: posterior misses at n = 200)": at least 565 target-mode misses; no start or search change can fix them (API-RESID: a start change can add at most the 6 stopped fits, 0.25%).

## 2.2 The LS0 check (O-LS0; `O-LS0/REPORT.md`; `campaign/LEDGER.md` 20:33 UTC)

- LS0 (one local search from the start mode S̃₀) run post hoc on all 2,400 fits (1,200 regenerated datasets × 2 scales, 0 errors; lattice subsample r = 1..20 per cell = 480 fits, D_S check on 297 fits with |Lat| ≤ 1024). Job B reproduced job A "0 of 11 fields differ across 480 fits".
- Result: "LS0 does not change a single study outcome … LS0's best-scored model never beats the production HPM: 0 / 2,394. The smallest margin is 0.002 nats". Exact recovery with = without: "1,119 / 1,200 at c = 1; 710 / 1,200 at c = 0.5; gain 0, harm 0". LS0 finds models better than S₀ in 55 fits at c = 1 and 358 at c = 0.5, every one already a production posterior miss. In the 1,829 production-exact fits LS0 never beats S₀ (0 / 1,829). "'S₀ is not a flip/swap local maximum' implies a production miss, with 0 exceptions in 559 fits."
- Cost: median 0.17 s (p = 500) and 0.37 s (p = 1000), about 5·10⁴ and 1.1·10⁵ score evaluations: "under 0.1% of a production fit" (400–2,200 s). REG-B CJ226 (LS0-1, LS0 post hoc outcome-neutral), CJ228 (LS0-3, LS0 cost). By itself LS0 is weaker than the sampler: best model = S₀ in 1,032 (c = 1) and 553 (c = 0.5) fits, against production's 1,119 and 710.
- T38(b1) premises mostly fail at n = 200: (M1) π₀(S̃₀) > ½ in 18 of 2,400 fits; (M2) D_S on all of Lat(S̃₀) in 17 of 168 (c = 1) and 1 of 129 (c = 0.5) checked fits; (M3) λ_min > 0 everywhere (min 0.056); cap ℓ ≥ Φ(S̃₀) − 1 in 1,968 of 2,400. LS-score's premise held in all 18 fits that met it. "LS0 succeeds far more often than its premises hold."
- Caveats: post hoc, not a redeploy; production core has no LS0 (API-AUDIT: "LS0 exists only in the O-LS0 test export"); REG-B CJ178 (LS0-4, LS0-EMIT, integrated LS0 test fit) is an "OPEN implementation check". Decision: LS0 adopted into the method ([pos 774]; MD03 (MEET-v31 decision 3)).

## 2.3 API-N200: predicted 558 vs 571 observed (`API-N200/REPORT.md`; REG-B TH334 (Theorem N200))

- Theorem N200 (PROVED, elementary, every n): P(U ∪ {Ŝ ≠ S₀}) = P(U) + P(𝒪, Ŝ ≻ S₀) + P(𝒪, S₀ ≻ Ŝ) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮), Π(X) := P₀(S† ≠ S₀ | X).
- n = 200 table (24 cells = 2 p × 2 c × 6 scenarios), pooled per (p, c):

| p | c | obs U | obs posterior misses | obs wrong | pred wrong = U + ΣP̂₀(L\|X) |
|---|---|---|---|---|---|
| 500 | 1 | 1 | 40 | 41 | 41.5 |
| 1000 | 1 | 3 | 37 | 40 | 40.3 |
| 500 | 0.5 | 0 | 230 | 230 | 228.3 |
| 1000 | 0.5 | 2 | 258 | 260 | 248.0 |
| all | | 6 | 565 | **571** | **558.1** |

  Check: 81.8 vs 81 at c = 1 and 476 vs 490 at c = 0.5. RMS z = 1.08 over the 24 cells; |z| ≤ 1.5 in 20 of 24; max |z| = 2.5 (p = 1000, S5, c = 0.5). The prediction is a lower bound plus a measured term. Discovery term: 0 search misses in 2,394, exact 95% Clopper–Pearson upper bound 0.125% per fit; a-priori route-(a) bound ≥ 1 − 10⁻⁶, vacuous. 2E₀δ₁ > 1 at n = 200 (π(S₀) ≤ 0.37 even on correct fits, O-CERT).
- Exact enumeration (n = 40, p = 12): Π − P₀(L) of 0.2–1 point at c = 1 and 2–8 points at c = 0.5 (`API-N200/results/small_p_exact.txt`).
- Not proved: "An upper bound on Π(X) at finite n is OPEN" (CJ14 (FW14)). Cost $6.06 ([pos 978]; `campaign/LEDGER.md` 23:25 UTC). Per-dataset matching and the C5 tabulation over the 2,400 fits remain bookkeeping (REG-B CJ238).

## 2.4 API-RESID, the common-σ² and residualised-start pilots (`API-RESID/REPORT.md`; `O-DILUTE/REPORT.md`; `F-SIGMA`)

- Post hoc recomputation of the start law on the 2,400 PROD-H fits, no SMC runs ("the v3 row below *is* the study's start law": rebuilt tables match to 3.1·10⁻¹³; log π₀(S₀) to 1.6·10⁻¹²).
- Common σ̂²: "None of the three feasible plug-ins gives one favourable fit (0/2,400 each)". C-fix floods to the cap K = 100 in 2,113/2,400 fits; oracle and s²(S₀) plug-ins flood in essentially all fits; σ̃²_{S̃₀} destroys π₀(R₂) (median 0.81 → 5·10⁻⁶); s_y² reproduces v3 within half a decade. "No SMC pilot for common σ̂²." Rejected (RF150 (common plug-in σ² is the right tool for the n = 200 dilution masking); `E-SPINE` §2.2).
- Residualised (backfit) tables, 3 sweeps: median log₁₀π₀(S₀) −15.65 (v3) → −1.07; "1,888/2,400 fits are favourable (O-DILUTE criterion π₀(S₀) ≥ 10⁻⁴), against O-DILUTE's 378/480 on regenerated data (78.7% vs 78.8%)"; start mode = S₀ in 1,245/2,400; no flooding; weak in S5 (1–44 favourable per 100) and S4 at c = 0.5 (74 and 47). Fixed-point version (≤ 10 sweeps): mode settles in 2,310/2,400; favourable in 2,203/2,400, mode = S₀ in 1,672; weak spot S5 at c = 0.5 (47 and 19 favourable).
- "Status, unchanged: residualised tables remain an **unproven candidate**." REG-B CJ162 (backfit start; residualised tables): "candidate, unproven … rejected for paper 1, recorded as future work (MEET-v31 MINUTES item 1)". Cost: API-RESID plus resume about $2.41 for the resume run ([pos 978], LEDGER).
- **UNCERTAIN:** favourable count of the unmodified v3 start: API-RESID table "v3 (method) … favourable (≥ 10⁻⁴) 0" of 2,400; O-DILUTE §1 "Favourable fits: 0 of 480; study: 1 of 2,394". Not reconciled.

## 2.5 Concurrency bitwise checks (`MEET-v31/evidence/2026-11-03_concurrency_runs.md`; REG-B TH394 (Proposition W))

Verbatim log (HQ re-run on Owls, 2026-11-03):

| design | serial final (s) | R = 4 concurrent wall (s) | bitwise logZ / pip / hpm | R = 32, N = 312 wall (s) | max ΔPIP eq / zw |
|---|---|---|---|---|---|
| p0500_S1_r001 c100 | 358.2 | 189.2 (sum island 377.7) | TRUE / TRUE / TRUE | 189.8 | 0.0001 / 0.0002 |
| p0500_S4_r001 c050 | 671.8 | 351.8 (sum island 699.1) | TRUE / TRUE / TRUE | 355.3 | 0.0023 / 0.0020 |
| p0500_S5_r002 c100 | 413.3 | 219.4 (sum island 433.5) | TRUE / TRUE / TRUE | 218.3 | 0.0005 / 0.0007 |

  So 3/3 designs bitwise (358 → 189 s, 672 → 352 s, 413 → 219 s; about 1.9× with 2 cores, FOR_FELIPE_FINAL_METHOD §1). Calibration times 161.6, 1184.5, 258.1 s. The author's own run covered the smoke problem and S1 only; its "3/3" headline was "an overclaim" until HQ re-ran S4 (pos 1175) and S5 (pos 1241) (`campaign/LEDGER.md` 16:50 UTC entry). **UNCERTAIN:** the task statement says "32 islands within 2e-4". The file shows R = 32 (N = 312) max ΔPIP ≤ 2e-4 only on S1; it is up to 2.3e-3 on S4 and 7e-4 on S5; the log Z of R = 32 differs from R = 4 by 0.027 (S1), 0.012 (S4) and 0.47 (S5) nats. The "2e-4" appears in the LEDGER as "R=32×312 split max ΔPIP 2e-4" for S1.
- Prop W-cal (concurrent calibration diagnostic islands) is not executed (REG-B TH395; METHOD_v3.1_FINAL §6 check 1).

## 2.6 PIP rescoring (`MEET-v31/evidence/2026-11-03_pip_rescore/REPORT.md`, chair helper, Opus 5.5)

- "Main finding: The equal-weight vs Ẑ-weighted MPM comparison cannot be computed for the 2,394 completed fits from this machine: their per-island `log_Z_r` and `pip_r` are not stored here." Production bundles are on the laptop and NOTS (`/scratch/fb31/smcbvs_v3_deploy_20261022/...`).
- Part A (3 designs, R = 4 `prod`, 11 variants): max|ΔPIP| = 3.94e-06 (S1), 1.75e-04 (S4 c0.5), **1.29e-03** (S5 r002, ESS_isl 1.88, W_max 0.707); R = 32 variants ≤ 8.38e-04; MPMs differ in 0 rows; MPM_eq right 2/3 and MPM_zw right 2/3; median max|ΔPIP| 1.75e-04. Caveat: the 3 designs were chosen by METH-AUDIT, not at random; "It says nothing about the rate of MPM disagreement in the study."
- Part B: counts of MPM_eq = S₀ and HPM = S₀ per cell (1,779 and 1,829). The Ẑ-weighted counterpart is **not computed** for the 2,394 fits (engineering TODO, 05 §4).

## 2.7 ABL-START (`ABL-START/REPORT.md` is a draft; the result is `MEET-v31/ITEM1_ABL_START.md`)

- 12 designs (p = 500, S1–S6 × {r001 c100, r002 c050}) × 1 seed; arms A block start (production, bitwise identical to production on S1 r001 c100), B singleton factors, C capped prior start (D backfit dropped as v2 evidence only). 33 of 36 A–C fits completed; three arm-B fits did not (S4 ×2 > 4 h CPU, S3 r001 stopped after 3 h 06 min); A took 10–28 min on the same designs.
- Rule outcome: 9 complete designs, 0 conclusive (arm C's log Ẑ differs by > 1 nat), "**Outcome 2. Keep the block start, reframed. The paper makes no depth or speed claim for the block start.**" REG-B CJ166 (ABL-START Outcome 1 depth claim): "not licensed". The rule was flawed (vacuous); v1 and HQ's corrected v2 script agree.
- Descriptive: arm C log Ẑ below arm A on 12/12 designs by 0.06 to 13.3 nats (> 2.5 on 11/12); island SD 1.5–76× larger (median about 8×); escalated to tier 1 on 9/12; wall time larger on 9/12. **Certified underestimation** (Ẑ below a model score the run itself found, a deterministic lower bound on Z): arm C on **10/12**, arm A on 0/12, arm B on 0/9. B agrees with A within 0.02–0.24 nats on 9 designs and costs more (A's wall time shorter on 8/9). All 33 completed fits return the best-known mode as HPM.

## 2.8 ABL-CONF, the confirmatory start test (`ABL-CONF/REPORT.md`, `ABL-CONF/results/final/*`; [pos 1669])

- 118 fits, all terminal: 107 completed, 11 capped at 75 min, 0 failed. 3 designs (S1, S4, S5 at p = 500, r001 c100) × 10 seeds × arms A/B/C, reference = K = 8 reserved arm-A seeds per design; rule pre-registered in 49b3496 (dry-run included) before any fit, applied by `scripts/finalize.sh` 2026-11-04 11:35 UTC; last fit 11:20 UTC. Branch `theory/ABL-CONF` @ 7e12cf5.
- Guard (reference not favouring arm A, S1): pass, |refA − refB| = 0.029 nat vs tolerance 0.287.
- **Claim 2 (accuracy): LICENSED** on all three designs: median log Ẑ error of the prior start −13.4 (S1), −10.8 (S4), −5.7 (S5) nats; every test fit below arm A (10/10, 9/9, 10/10); escalated to tier 1 in 7, 9, 8 of 10; cost 2–4× the block start's wall time. REG-B CJ165 (ABL-CONF Claim 2): "LICENSED (… median log Z error -13.4/-10.8/-5.7 nats); XF none". The report text says "by 6–13 nats in median".
- **Claim 1 (cost): INCONCLUSIVE** overall (rule: licensed iff it holds on every design). REG-B CJ164 (ABL-CONF Claim 1): "INCONCLUSIVE (pre-registered rule: S1 inconclusive, S4 holds_nondeliv, S5 holds); XF none".
  - S5 (correlated): block start cheaper in 10/10 pairs (sign test p = 0.001); median wall 1,116 s vs 1,639 s, evaluations 3.5e8 vs 4.5e8; accuracy equivalent (median Δ log Ẑ error 0.033 nat, 90% interval [−0.010, 0.056]; PIP difference within ±0.002).
  - S4 (masked): singleton factors did not deliver within 75 min in 10/10 fits; block start delivered 9/10 (median 1,915 s). "This is a delivery result, not an equal-accuracy result."
  - S1 (favourable): B cheaper in 8/10 pairs (p = 0.055, not significant); accuracy equivalent.
- Reference table: log Z_ref −65.671 (S4, se 0.036, best-known = S₀ FALSE, posterior miss), −105.402 (S5, se 0.024, TRUE), −69.546 (S1, se 0.007, TRUE).
- What the paper may say (report): the prior-start claim as licensed; the per-design cost results as pre-registered per-design results, not the overall cost claim. All delivered fits returned the best-known model as HPM (descriptive).
- Operational record: first launch killed 01:25 UTC (T3 stops the agent's systemd scope; `setsid` does not escape); relaunched 01:29 UTC as `systemd-run --user` units (`ABL-CONF/results/final/DEVIATIONS.md`).

## 2.9 Calibration cost formula (MEET-v31 SYNTH_R2 D4; TLF M8 "Numerical companion")

- Seat A's formula: calibration / final work ≈ 0.05 + 0.2·I, I = rebuilds ("Calibration-cost ratio 0.0512 + 0.2048·I (single tier; rounded 0.05 + 0.2·I): seat-derived, unchecked", METHOD_v3.1_FINAL "Points settled" 5). "Filed: calibration/final ratio predicted 0.46/0.67/1.69 vs observed 0.45/0.62/1.76 on 3 designs."
- Reconstruction from the concurrency log (editor check, not in a source): S1 r001 (I = 2): 0.0512 + 0.4096 = 0.46 predicted, observed 161.6/358.2 = 0.45; S5 r002 (I = 3): 0.67 predicted, observed 258.1/413.3 = 0.62; S4 r001 (I = 8): 1.69 predicted, observed 1184.5/671.8 = 1.76. Status: Prop D's calibration share is "seat-derived, unchecked" (TH08.b, OB15). The 20-fit tabulation of `timings$calibration/final` on saved fits is an engineering TODO (05 §4).

## 2.10 LIT-PAR: 20/20 vs 5/318 (`LIT-PAR/REPORT.md` §3.1 G4; REG-B CE213 (SaM on an LH-like masked design))

- "At β = 1: the exact full posterior recovers S₀ in 20/20 datasets. SaM recovers S₀ in **5/318** random splits that separate the linked pair"; at β = 0.6 the separated count is 0/318. LH-like design, p = 16 (not the exact W1-EXP family). Status: "COUNTEREXAMPLE (numerical, reproducible) … analytic part PROOF SKETCH, corrected by RF276/TH417; author-only; cited at MEET-THM as labelled numerical evidence" (CL23). The analytic separation is CJ21 (FW21, Song–Liang analytic separation).
- LIT-PAR verdict ([pos 1072]): "The gap is real": every parallel BVS method with a theorem (Song–Liang, DECO, Bayesian-bootstrap SSL, Gutierrez–Guhaniyogi, variational) needs a design condition that strongly correlated designs violate; none combines (exact model posterior with unbiased Ẑ) + (communication-free parallel computation) + (proved bound on sequential depth under correlation). Qualification: "Don't print 'methods with guarantees are sequential'" (Zhou–Yang–Vats–Roberts–Rosenthal's informed sampler has a p-free mixing bound and parallel neighbour scoring). Cost about $5.50.

## 2.11 Dilution numbers (`O-DILUTE/REPORT.md` §1; REG-B LM212 (Lemma W2), TH177 (Proposition D′), TH158 (dilution masking))

- "PROVED (exact, any data, any partition): −log π₀(S₀) = V + C − log A." "On 480 regenerated study fits, V carries 83% of −log π₀(S₀), C carries 11% and the size term 6%." (TH03.d is the final-card form.)
- Mechanism: σ²-dilution of the truths' table log-odds: keep-j gain scaled by log(1 − ρ_j²)/log(1 − x_j) = 0.05–0.20; "About 7 of the 14 truths are invisible at n = 200 for every c"; start favourable only at n ≈ 590–730. Verification: pooled median π₀(R₂) = 0.79 (study ≈ 0.8); median π₀(S₀) = 10^{−15.7}; per-cell medians 10^{−11.1} to 10^{−25.6}; the design-level formula predicts the per-cell median within 0.1–1.3 in S1/S2/S5 but underpredicts by 1.0–1.6 in S3/S4.
- Status: the formula Prop D′ (finite-n dilution formula) is "PROOF SKETCH (author); numerically checked; SF none; XF none"; the identity DIL-E/DIL-E1 is XF VERIFIED / VERIFIED* (A-REV9). RF105 ('Beta-min fails by about 100x in squared signal'): corrected to 43× ([pos 796]). **UNCERTAIN:** other single thresholds for "favourable from n" disagree: 590–730, 800–1,600, 1,050–3,200 (REGISTRY_v2 §D; 02b P.2).

## 2.12 The O-CERT exhaustive check (476,160) (`O-CERT/REPORT.md`, `O-VCERT/REPORT.md`; REG-B LM204 (Lemma M), TH330 (Corollary C5))

- Lemma M (Q_S decreases, D_S increases, w non-increasing): O-VCERT "0 violations in 476,160 exhaustive (S, S+j) pairs"; log D rises by ≥ 5.6·10⁻³ per addition in every test, duplicates included; Thm C4 (box certificate): "0 Φ-violations and 0 M-violations over all 285,712 boxes on 48 designs"; B&B agrees with brute force 80/80, mass lower bound valid 40/40. XF: A-REV9 "VERIFIED in exact arithmetic". Independent code `scripts/vcert_check.py` written from `00_COMMON.md` only.
- O-VCERT's gaps: Thm C1(b) last sentence ("unscored" mass) GAP with counterexample, repaired (R1); C6 floating-point clause GAP, repair R2; §4 illustration of O-CERT "MISSING" at 17e7f15 (later added; not reviewed: registry conflict C21). OCERT-C1 "XF ERROR as quantified" (TH04 row); Cor C5 "VERIFIED*, tie caveat" (XF ERROR on tie-insensitive prose, TH330). Certificate card in the final method: MD10 (MEET-v31 decision 10).
- O-CERT's result that π(Ŝ) ≤ 0.37 on correct fits is quoted in API-N200 §1.

## 2.13 Billing and cost record

| item | numbers (source) |
|---|---|
| Cloud-session credits (Claude Personal) | `campaign/LEDGER.md` header: "$245 cloud-session credits (Personal), expire 2026-11-05 07:59 UTC"; HQ text: "How the $250 was spent: about $229 over Waves 2–8, roughly 30 Opus sessions, all of which reported" ([pos 784]); readings $245 (16:00), $244 (17:19), $239 (~17:22); "Felipe's reading: $21 of $250 left" (20:35 UTC); at [pos 1673] Felipe: "remaining $19 of cloud". **UNCERTAIN:** $245 vs $250 initial; $21 (LEDGER 20:35 UTC) vs $19 ([pos 1673]); the difference is not explained in the sources. Cloud runs were Opus 5.5 only. |
| Billing rule | Routines (RemoteTrigger / triggers API) are EXCLUDED from the cloud credit and bill weekly plan usage; sessions created with `claude --cloud` DO bill the credit (a 7 s test moved it from $245 to $244) ([pos 301], [pos 342]; LEDGER). Wave 1 (5 routines) billed the plan, not the credits. |
| API credit ($200 promotional, "Felipe's Individual Org") | covers the Agent SDK, NOT the Claude Code CLI ("Credit balance is too low" on the CLI); a test run cost $0.002; expires 2026-11-17; no payment method on file; monthly spend limit $195 (LEDGER 21:25 UTC; [pos 867], [pos 894]). |
| API spend by run (LEDGER / transcript) | API wave (9 runs): "measured cost ≈ $31 for 7 runs with a cost line + 2 unmeasured": API-PXNGAP (Fable) $11.04; API-N200 (Fable) $6.06; API-MASKZPIP (Opus) $5.12; API-POS (Opus) $2.77; API-VSTAB (Opus) $2.23; API-T26BUD, API-FAVIID, API-RESID, API-AUDIT: no cost line in the wave summary. Caps: RESID $15, FAVIID $15, PXNGAP $25, N200 $25, MASKZPIP $15, AUDIT $12, T26BUD $12, POS $10, VSTAB $12. Resumes (cap $6 each): API-RESID resume $2.41, API-AUDIT resume $1.47. Literature phase: LIT-SMC $2.81, LIT-MCMC $3.56, LIT-STAT $4.01, LIT-VENUE $2.78 (≈ $17.0 with the resumes); LIT-PAR ≈ $5.50; METH-AUDIT $5.89; THM-INV $7.99; THM-SYNTH $8.4; ABL-START worker stopped at $2.45; MEET-v31 chair spend $0 (subscriptions); theorem meeting and ABL-CONF on subscriptions/Owls (no API). |
| API balance readings | about "$45 of the $200" spent at [pos 978]; "$160.34 left" before the literature phase ([pos 1009]; LEDGER 23:27 UTC); "roughly $143" after it; funding rule "~$144" ([pos 1048]); Felipe at [pos 1673]: "the remaining $121 of the other credit". **UNCERTAIN:** the run-by-run costs above sum to less than the implied $79 spent ($200 − $121); no sources reconcile the difference (HQ's "I haven't checked the Console", [pos 1009]). |
| New credit | "a new $200 is coming in on Nov 15th, we will burn it as well on theory" (Felipe, [pos 987]); HQ's plan: the first $200 expires Nov 17, about $60 kept in reserve to start the per-theorem HQs before then; the Nov 15 credit "continues them" ([pos 1059]). |
| Weekly plan | Ultra plan weekly use 84% when cloud credits ran out (LEDGER 20:35); CP window resets 21:00 UTC ([pos 763]); Claude Work (CW) and Claude Personal (CP) subscriptions used for the later work ("no API credit: subscriptions only", LEDGER 00:50 UTC 2026-11-04; reversed at [pos 1673]). |

---

# §3 Conclusions and confidence

Everything below is the thread's own position (quoted or cited) unless labelled "Summary:" (editor's compression).

## 3.1 What the thread concluded about the method

- Summary: **v3.1 = v3 unchanged as a statistical method** + a parallel execution layer over islands, scans and block tables (never variables), optional stacking, LS0, Ẑ-weighted PIP as primary, a general-h accumulator, a certificate card and explicit NA outputs (`MEET-v31/FOR_FELIPE_FINAL_METHOD.md`; MD01–MD13). Approved by HQ ([pos 1557], [pos 1584]); Felipe approved the four decisions ([pos 1302], recorded [pos 1304]). "No open method questions remain" (N9 kernel gate passed, [pos 1550], [pos 1593]).
- The block (local-to-global) start is kept (MD01 (MEET-v31 decision 1)); the data (ABL-CONF) license that the prior start underestimates Ẑ and show per-design cost advantages, but not a general cost claim (§2.8). HPM stays the only decision rule (MD02).
- Honest scope statements: nine inherent limitations (LIM01–LIM09); seventeen obligations (OB01–OB17) that are *not* limitations; island-level depth only (MD06). The method meeting recorded that nothing is tuned to the study (49 settings classed (a)–(d), none (e); DF25).
- At n = 200 "every error is statistical, never computational": 1,829 exact, 565 posterior misses, 0 search misses, 6 stopped ([pos 796]); the local search works as a pure certificate (§2.1).

## 3.2 Maturity of the theory (HQ's own assessments, with positions)

- [pos 929] (2026-11-02 22:14, before the meeting phases): "Overall: the theory is past the halfway point and its architecture is settled … about two-thirds to three-quarters of what a strong JRSS-B submission needs." Mature: the story (T21 composition), the statistical half (T03♯, T07 "proved and verified by both families" but "not where the novelty lies"), the computational half "from conjecture to theorem in one day". Not mature then: p ≫ n, nothing quantitative at n = 200, masked Ẑ and PIP only one-sided, narrower novelty.
- [pos 933]: "about 8–12 working days at 70% of today's pace … the story would be strong, though not airtight."
- [pos 937]: "airtight" would need premises checked on the study's own designs and a finite-n bound matching the observed counts; "items 2 and 3 in full are probably beyond current SMC theory for correlated designs with p = 1000 and n = 200".
- After the meetings ([pos 1626], [pos 1650]): the paper-1 list M1–M8 plus 12 supplement cards is complete as a list ("every one ended up on the list, in future work (27, each with a reason), as a cited published result, or dropped (6, with reasons)"). Proof maturity is lower than list completeness: many "PROVED" are "(by this seat, unchecked)", several assemblies are "PROOF SKETCH", N1 (binding §13.1) is a sketch, GUARD-W unaudited, N3 OPEN (§1.1). A hostile-referee simulation (F-REFEREE, Fable 5.1, JRSS-B standard) said "major revision": (1) asymptotic theorems (thresholds n ≈ 2·10⁶) against n = 200 simulations; (2) the masked regime proved only with a method change (LS0), routes for the evaluated method hypotheses-as-conclusions; (3) no positioning against the rapid-mixing literature (Yang–Wainwright–Jordan 2016; Zhou–Yang–Vats–Roberts 2022). Later items answered: LS0 adopted; no-LS0 candidates on LH (BG3, etc.) cross-verified both ways; N200 gives a quantitative n = 200 account; positioning done by LIT-*.
- Not-covered candidly: Song–Liang analytic separation (CJ21), p exponential (CJ18), finite-n Π(X) upper bound (CJ14), masked two-sided Ẑ/PIP accuracy (CJ24, CJ07), delivery P(U) → 0 (CJ13).

## 3.3 Novelty versus the literature (LIT-* reports; REG-B; [pos 616], [pos 1009], [pos 1072])

| Work | Position of the thread |
|---|---|
| Rossell 2022 (Bayesian Analysis) | Theorem 1 / T03♯ is "a modest extension"; "The bound P(S† ≠ S₀) ≤ 2E[1 − π(S₀)] is his Proposition 1 word for word, so Thm 4 and Thm 5 must credit him" (CL13 (Rossell 2022 Prop 1)); what remains ours is the cap K of order n under BB(1,p) (LIT-STAT). |
| Song–Liang 2015 (split-and-merge) | Model for "how much theory to get out of a method" ([pos 1150]); their results are about selection, not the posterior; Condition 5 / Cor 2 violation under cancelling correlated partners; the analytic separation was not proved (scouting recommended; CJ21 (FW21)); paper "compares, and does not claim to exceed, Thm 1, Thm 2 and Thm 4" (MINUTES §3 item 3); numerical counterexample 5/318 is labelled evidence (CL23). |
| Lindsten et al. 2017 (D&C-SMC, JCGS) | "closest conceptual antecedent"; "The general local-to-global idea already exists" ([pos 616]); Ẑ unbiased, consistency; depth-as-tree-height precedent; no R → ∞ pooling theorem (LIT-PAR). Pitch must be "when and why a scored-HPM SMC succeeds", not "local-to-global correction". |
| Štefankovič–Vempala–Vigoda 2009 (J. ACM) | O-STAGES Theorem G(i) (greedy ESS grid is the shortest valid grid) "is already in the literature"; cite and present as known (CL05 (greedy-schedule optimality)); G(ii) sandwich is a routine v3-specific extension. |
| Syed et al. 2024 | "global barrier": the dense-schedule limit √c·T* → Λ_len is a known analogue; cite (CL06 (Syed Thm 3; Gelman–Meng)). Our Theorem M (masked crossing T* = log₂A₀ + O(1)) and the favourable O(1) were "not found in anything I read", but "elementary given SVV" (LIT-SMC). |
| Dai–Heng–Jacob–Whiteley 2022; Whiteley–Lee–Heine 2016 | Frozen-run unbiasedness, Ẑ-weighted pooling of independent islands and the freeze-adaptive-run advice are standard and must be cited (CL03, CL11). The non-standard items in Prop 2 are the negatives (pooled × pooled is not an identity; E[Ẑ \| completed] ≠ Z). |
| Schäfer–Chopin 2013 | Ancestor of the method; parallel tempered SMC on binary spaces; BVS SMC machinery "covered" ([pos 616], [pos 1072]); no theorems (LIT-VENUE). |
| Papaspiliopoulos–Rossell 2017 | Exact enumeration of correlation-clustered blocks is their precedent (CL10); our contribution is the exactly samplable block start under a global size prior and cap. |
| Zhou–Yang–Vats–Roberts–Rosenthal 2022 (JRSS-B), Yang–Wainwright–Jordan 2016 | Rapid mixing under their priors covers LH-like designs; API-POS: on LH the masking is a property of the start, S₀ the unique local mode; LIT-MCMC corrects: their unimodality condition R > M fails for OUR target at study scale (12/12, factor ≥ p^0.87; Prop OB sketch); "No published BVS example has MCMC provably slow while tempering or SMC succeeds" (open). Hence the masked-start theorems "repair a problem created by the start. They don't show the method beats MCMC." Cited next to M5 (CL14). Also Hou–Wang–Atchadé arXiv:2407.20580 (never "first finite-n", CL15). |

- Genuinely ours (LIT-VENUE, LIT-SMC): (i) the exact, algorithm-agnostic finite-n split of the reported-model error into a posterior-miss term and a search-miss term that can be measured per run (Theorem N200 / T21 composition; only the informal idea exists: García-Donato–Martínez-Beneito 2013); (ii) the masked-start lower bound paired with a repair theorem; (iii) consistency of an SMC-BVS output at all ("No paper in the sample proves anything about the output of an SMC sampler for BVS"); (iv) run certificates (nothing of the same kind found); (v) Lean-checked finite cores. Polynomial-time recovery on LH already follows for YWJ/ZYVR priors: "T38(c), 'polynomial cost', is not a selling point on its own."

## 3.4 Venue

- [pos 933] (before the literature phase): "JRSS-B is realistic, probably after one major revision. Biometrika or JASA Theory & Methods are solid alternatives."
- LIT-VENUE (`LIT-VENUE/REPORT.md` §1.5, summarised at [pos 1009]): "The package **realistically supports Biometrika, the 5-result cut, only if** the referee's major point is met: Thm 5(b) for the algorithm as run, with the transition shown at growing n. It supports **JCGS, Bayesian Analysis, EJS or Statistics and Computing comfortably** if the numerics are strengthened. JRSS-B is a stretch. AoS is not realistic." Expectations not yet met: real-data analyses; head-to-head comparisons (PARNI, MAdaSub, TGS, SuSiE/SSL); simulations at growing n; a main theorem not tied to LH; external human review of proofs that are now AI-checked only.
- Felipe's decision ([pos 1015]): "Let's try to build something rigorous enough to make it to Biometrika. Down to Lean certificates. Then we will analyze what more challenging results can we go to." HQ: "Version 1 is the Biometrika paper … The key results get Lean certificates. Harder results wait." Paper 1 = Biometrika; paper 2 = trees (LEDGER 13:03 UTC 2026-11-03). Felipe's priorities: posterior accuracy primary, selection secondary ([pos 1020]); the goal is "to start retiring sequential MCMC for BVS" ([pos 1030]).
- **UNCERTAIN (position shift):** HQ's venue view moved from "JRSS-B realistic" ([pos 933]) to "JRSS-B a stretch, Biometrika conditional" ([pos 1009]) after LIT-VENUE; the final state carries the later one, with Biometrika as the target by Felipe's instruction.

## 3.5 Confidence statements and their basis

- High: the organising inequality (T21 composition / Theorem N200) is proved and its finite core is Lean-checked (TH422); the 2,400-fit decomposition is fully accounted (1,829 + 565 + 0 + 6); LS0 changes no outcome (0/2,394) and costs under 0.1%; kernel validity N9 holds with exact production checks and negative controls.
- Medium: the masked-regime theorems (LH, LS0) and Thm5-LH are SAME-FAMILY-ONLY or XF-VERIFIED* on a constructed family; p ≫ n handled only by API-PXNGAP "PROVED (candidate) — needs cross-family review" (campaign-era, outside the final list).
- Low or open: N1 (binding §13.1), GUARD-W, N3, floating point (OB16), masked two-sided Ẑ, finite-n Π(X) upper bound, delivery, exponential p (§1.1, 05).
- Reviewers' consensus on honesty: F-REFEREE praises the composition inequality as "exactly the right organising principle"; the theory is asymptotic with thresholds n ≈ 2·10⁶ and the paper "can explain the mechanism, not the n = 200 numbers" ([pos 550]); N200 supplies the quantitative n = 200 account at the level of Π(X) predictions (558 vs 571).
- External human review of the proofs has not happened; all checks are AI-based (two model families plus Lean for finite cores).
