# W3-EDIT: triage of the 59 NOT-EDITORIAL API-audit MINORs (for the manager; nothing applied)

Classes: **(iii)** could affect a stated hypothesis or conclusion · **(ii)** real local slip in a proof step, claim unaffected (one-line fix + line check) · **(i)** wording that only looks statement-level (an E finding after all). ★ = the claim, or the theorem it is a clause or package of, is on `HEADLINE_CANDIDATES.md` (recorder/staging-1115 ac5754d) / the W3-READER card. Finding text: `reviews/H1_minors_extract.tsv` (row n = ledger I1-Mnn).

| class | ledger | ★ | claim | file:line | what the audit says | note |
|---|---|---|---|---|---|---|
| (iii) | I1-M05 |  | C-DLV:L1-R | `Wave1C/C-DLV/lemmas/L1_resources.md:78` | memory envelope: population term lacks factor w; constants called "absolute" (L1:70) but depend on w, k | O(·) unaffected; stated constant property wrong |
| (iii) | I1-M08 |  | C-DLV:Cor-R | `Wave1C/C-DLV/lemmas/L1_resources.md:127` | MACH stated for whole-run wall time, applied segment-wise | hypothesis reading must be stated; else P̄_t needs W̄ (still polynomial) |
| (iii) | I1-M10 |  | C-DLV:L3-3.3 | `Wave1C/C-DLV/lemmas/L3_grid.md:30-31` | "φ_k = 1" at every tier assumes the pilot completes; pilot exits truncate it | lemma conclusion false for truncated pilots; uses unaffected |
| (iii) | I1-M11 |  | C-DLV:Thm-D | `Wave1C/C-DLV/lemmas/L4_delivery.md:15` | Thm-D (ii) stated as a set identity; holds only up to the null set of (i) | conclusion form: identity a.s. |
| (iii) | I1-M13 |  | C-DLV:Thm-D | `Wave1C/C-DLV/lemmas/L1_resources.md:78-80` | same as M05 for Thm-D: C_M depends on w, not absolute | dup of M05 |
| (iii) | I1-M16 |  | W2-APP:Thm-APP | `Wave2/W2-APP/lemmas/L4_families.md:167-168` | Family-map cell "per FAC (pending)" stale vs body (FAC-A covers p ≤ n^{1/6−}) | inside registered span 152-171; fixing it strengthens the stated conclusion |
| (iii) | I1-M23 |  | W2-UNI:U-LOC | `Wave2/W2-UNI/STATEMENT.md:168-169` | U-LOC (d) omits the rate δ_n√(p log log n) → 0 that the transfer needs (proof states it) | missing hypothesis in statement |
| (iii) | I1-M27 | ★ (W2-UNI:F-UNI, card 3.1) | W2-UNI:F-UNI | `Wave2/W2-UNI/lemmas/L5_delivery.md:33-34` | (S) phrased for every n; instances supply |Q_n| ≤ K_n only eventually; "(s₀ ≤ K eventually)" redundant | hypothesis should read "eventually"; every-n conclusion does not use (S) |
| (iii) | I1-M30 | ★ (part: W3-SAMP package; LT# card 3.6) | W3-SAMP:Pkg | `Wave3/W3-SAMP/lemmas/LT_theorem.md:98-99` | "no output certifies W_r ≥ η" justified only by top store ⊊ Ω | strength of a label (hedged "in general"); no theorem uses it |
| (iii) | I1-M35 | ★ (W2-FAC-B:Thm-FAC-CS) | W2-FAC-B:Thm-FAC-CS | `Wave2/W2-FAC-B/STATEMENT.md:105-106` | (C1) "S̃₀ = S*" needs premise e4′, not listed in (C1) | missing hypothesis; (C3)/(C4) and L5.2 carry it |
| (iii) | I1-M37 |  | W2-FAC-PK:Thm-FAC-PK | `Wave2/W2-FAC-PK/lemmas/L4_assembly.md:32-33` | L4(ii) adds "liminf P(𝒪∩{Ŝ⁺=S₀}) = 1 − limsup P(U_n)", U_n undefined, unproved | outside the registered statement (STATEMENT:73-87); unproved assertion in the lemma |
| (iii) | I1-M48 |  | C-ENG:TDP_E | `Wave1C/C-ENG/lemmas/TDP_E.md:40` | specialisation E = 𝒜* cites N3-code (b) under (H3), never stated; needs cap ≥ N | registered statement :38-40; result unaffected under exact arithmetic |
| (iii) | I1-M50 |  | C-PACK:I1-audit | `Wave1C/C-PACK/lemmas/I1_e4_replacement.md:20-45` | catalogue lacks PXN potential-run and M5(0)/T38 structural rows | completeness of an audit claim |
| (iii) | I1-M55 |  | C-PACK:I1-e4prime | `Wave1C/C-PACK/lemmas/I1_e4_replacement.md:36` | e4′(i) allows any routine with MR1; GEN (C6) needs a global maximiser (N3(a), coded routine only) | not falsified ((C6) declared outside); fix = keep e4 for (C6) or strengthen MR1 |
| (iii) | I1-M57 | ★ (W2-APP:POST, card 1.2) | W2-APP:POST | `Wave2/W2-APP/lemmas/L1_POST.md:33` | J_n(c) inclusion sub-clause: one-sentence proof, unstated T03♯ variant; BM-∞ envelope does not apply there | text should say so; transfer itself fine |
| (iii) | I1-M58 | ★ (W2-APP:POST, card 1.2) | W2-APP:POST | `Wave2/W2-APP/lemmas/L1_POST.md:12-15` | raw-scale parenthetical: event is raw-design-measurable, not X-measurable as (a) states; needs T03♯ with n-dependent θ* in a compact | scope of the parenthetical; depends on input version |
| (iii) | I1-M59 |  | W2-APP:VN-routes | `Wave2/W2-APP/lemmas/L5_VN.md:29-33` | "hence" names only (H2) / (G1)+(G3); literally proved: the full hypothesis set cannot hold | conclusion wording narrower than written |
| (iii) | I1-M61 | ★ (clause of W1-GEN:Thm-GEN) | W1-GEN:Thm-GEN(C4) | `Wave1/W1-GEN/STATEMENT.md:119-120` | "the conclusions of (C3)" include D_n ≤ P(S̃₀≠S*)+O(1/log n); L5.4 proves only the limits | strength: rate does not transfer |
| (iii) | I1-M69 |  | W2-FAC-XA:L2 | `Wave2/W2-FAC-XA/lemmas/L2_robust_path_attempt.md:200` | conclusion presupposes search starts at S* and best-improving LS0; not in hypothesis list | missing hypotheses |
| (iii) | I1-M70 |  | W2-FAC-XA:L2 | `Wave2/W2-FAC-XA/lemmas/L2_robust_path_attempt.md:186-193` | o(1), o(H) terms must be uniform over prefixes/states; statement does not say so | hypothesis precision |
| (ii) | I1-M01 | ★ (W1-N1:Thm-N1, card 3.5) | W1-N1:Thm-N1 | `Wave1/W1-N1/lemmas/L1_bridge.md:119-123` | measurability partition omits `tier` (finite; add to cells) | one-line fix + line check |
| (ii) | I1-M02 | ★ (W1-N1:Thm-N1, card 3.5) | W1-N1:Thm-N1 | `Wave1/W1-N1/lemmas/L3_freezing.md:34-36` | bound "depends only on data" needs blocks/tables data-determined; else split h⁺/h⁻ | one-line fix + line check |
| (ii) | I1-M04 |  | C-DLV:L1-R | `Wave1C/C-DLV/lemmas/L1_resources.md:53` | enumeration cost covered via unstated E ≤ 9N₀p ≤ Σ̄ (true) | one-line fix + line check |
| (ii) | I1-M06 |  | C-DLV:L1-R | `Wave1C/C-DLV/lemmas/L1_resources.md:90-91` | archive count not ≤ K(ℓ+3)² for large ℓ; absorbed in C_M | one-line fix + line check |
| (ii) | I1-M07 |  | C-DLV:Cor-R | `Wave1C/C-DLV/lemmas/L1_resources.md:132-133` | exact-branch bytes not ≤ P₀ term by term; aggregate holds | one-line fix + line check |
| (ii) | I1-M09 |  | C-DLV:Cor-R | `Wave1C/C-DLV/lemmas/L1_resources.md:78` | inherits M05 constant | one-line fix + line check |
| (ii) | I1-M14 | ★ (C-GROW:Thm-GROW) | C-GROW:Thm-GROW | `Wave1C/C-GROW/lemmas/L2_NA_TL.md:32` | L1.4(b) cited for non-nested swap; direct log u ≥ 1−1/u | one-line fix + line check |
| (ii) | I1-M20 |  | W2-APP:Thm-APP | `Wave2/W2-APP/lemmas/L1_POST.md:33` | two side remarks only sketched ("same diagonal argument") | one-line fix + line check |
| (ii) | I1-M21 |  | W2-FAC-S5:L4 | `Wave2/W2-FAC-S5/lemmas/L4_path.md:16` | n₀ also depends on the sequence (p_n) under limsup form of (P_α) | one-line fix + line check |
| (ii) | I1-M22 |  | W2-FAC-S5:L4 | `Wave2/W2-FAC-S5/lemmas/L4_path.md:22-23` | cap clause rests on external prefix property (FINAL s7_impl.tex L3) | one-line fix + line check |
| (ii) | I1-M24 |  | W2-UNI:UNI-1 | `Wave2/W2-UNI/lemmas/L4_k1.md:39-41` | energy constant M := s₀θ_hi² should be s₀²θ_hi² (any fixed M serves) | one-line fix + line check |
| (ii) | I1-M28 |  | W3-RM:RM-R | `Wave3/W3-RM/lemmas/L4_formR.md:53-55` | p = 1 branch: H_A = n² vs normaliser n; −½ log n vs −½ log(n+1) | one-line fix + line check |
| (ii) | I1-M31 | ★ (part: W3-SAMP package) | W3-SAMP:Pkg | `Wave3/W3-SAMP/lemmas/CC_code_check.md:96-100` | T ≤ 4·max(1000, ℓ²) needs tier e ∈ {0,1}; affects only a remark | one-line fix + line check |
| (ii) | I1-M34 | ★ (W2-FAC-B:Thm-FAC-CS) | W2-FAC-B:Thm-FAC-CS | `Wave2/W2-FAC-B/lemmas/L5_assembly.md:23-24` | g₀ = 1−ρ fails by a hair if SE_w is n-normalised; any g₀ < 1−ρ works | one-line fix + line check |
| (ii) | I1-M39 | ★ (W2-FAC-X:Thm-FAC-CS-iid) | W2-FAC-X:Thm-FAC-CS-iid | `Wave2/W2-FAC-X/lemmas/X4_path.md:22-27` | E6/E7 undefined for bounded p; intersect E′_n only in regime (L) | one-line fix + line check |
| (ii) | I1-M40 | ★ (W2-FAC-X:Thm-FAC-CS-iid) | W2-FAC-X:Thm-FAC-CS-iid | `Wave2/W2-FAC-X/lemmas/X4_path.md:46` | pair-probability constant: t/√π, not p²c₁ϖ(2π)^{−1/2} | one-line fix + line check |
| (ii) | I1-M41 |  | W1-N1:B | `Wave1/W1-N1/lemmas/L1_bridge.md:63` | (B-0)/(B-d) silent on `tier`; add to partition, KERNEL per tier | one-line fix + line check |
| (ii) | I1-M46 |  | W1-PXN:CR | `Wave1/W1-PXN/lemmas/CR_corr_tails.md:44-48` | [CONC′] bounds {max>δ}, used for {≥δ*}; δ↑δ* limit | one-line fix + line check |
| (ii) | I1-M49 |  | C-ENG:TDP_E | `Wave1C/C-ENG/lemmas/TDP_E.md:57` | step (4) "every cap ≥ 1" but shipped tie_dp throws for cap < 2 (outside registered statement) | one-line fix + line check |
| (ii) | I1-M51 |  | C-PACK:I1-audit | `Wave1C/C-PACK/lemmas/I1_e4_replacement.md:68-69` | inclusion 𝒯_n ⊆ {S̃₀ = S°} asserted; holds on 𝒜_n ∩ {π̃₀(S°) > ½} | one-line fix + line check |
| (ii) | I1-M53 |  | C-PACK:I1-UM-FP | `Wave1C/C-PACK/lemmas/I1_e4_replacement.md:96-98` | η bound needs ρ*_b(∅) = 0 / met-blocks sum | one-line fix + line check |
| (ii) | I1-M54 |  | C-PACK:I1-PXNrepair | `Wave1C/C-PACK/lemmas/I1_e4_replacement.md:69` | same inclusion as M51; intersect 𝒯_n at o(1) cost | one-line fix + line check |
| (ii) | I1-M56 | ★ (W2-APP:POST, card 1.2) | W2-APP:POST | `Wave2/W2-APP/lemmas/L1_POST.md:43-48` | GROW L6.2 applied beyond its stated AR(1) hypotheses; true by polarisation + χ² + union | one-line fix + line check |
| (ii) | I1-M60 |  | W2-APP:Ex-STAR | `Wave2/W2-APP/lemmas/L5_VN.md:70-71` | STAR ∉ LOC argued for (LOC-Σ) only; (LOC-Θ) one line via CD(c) | one-line fix + line check |
| (ii) | I1-M62 |  | W2-FAC-A:Lemma-GAP | `Wave2/W2-FAC-A/lemmas/L8_frontier.md:38-39` | base case t = 1 misses the step computation for c_{T₁} | one-line fix + line check |
| (ii) | I1-M63 |  | W2-FAC-A:Lemma-GAP | `Wave2/W2-FAC-A/lemmas/L8_frontier.md:39-42` | adjacency of e to D_{t−1} unstated; degenerate z_e = c | one-line fix + line check |
| (ii) | I1-M65 |  | W2-FAC-PKA:L4 | `Wave2/W2-FAC-PKA/lemmas/L4_table_discovery.md:18` | two code facts asserted by source cite (v3_core.cpp:372,408); needs a code check / named premise | one-line fix + line check |
| (ii) | I1-M67 |  | W2-FAC-X:X9 | `Wave2/W2-FAC-X/lemmas/X9_iid_general.md:47-48` | event probabilities of s² range and X5-type events not stated (implied by D1–D4) | one-line fix + line check |
| (ii) | I1-M71 |  | W2-FAC-XA:L2 | `Wave2/W2-FAC-XA/lemmas/L2_robust_path_attempt.md:203-205` | Δ_k ≥ (½−o(1))log n used, not written; leans on FAC-B L1.3 | one-line fix + line check |
| (ii) | I1-M72 |  | W2-FAC-XA:L2 | `Wave2/W2-FAC-XA/lemmas/L2_robust_path_attempt.md:245-249` | small branch cites FAC-B L4.2; needs gain ≤ −t with t > ζ (outside registered span) | one-line fix + line check |
| (i) | I1-M12 |  | C-DLV:Thm-D | `Wave1C/C-DLV/lemmas/L4_delivery.md:16` | (α) written with counts of the aborted run; operative statement is L3 3.4(c) | wording |
| (i) | I1-M15 |  | C-GROW:L3 | `Wave1C/C-GROW/lemmas/L3_sandwich.md:6-8` | header restatement of (G1) omits "|Q| ≤ K"; (G1) is cited by name and includes it | wording |
| (i) | I1-M26 | ★ (W2-UNI:F-UNI, card 3.1) | W2-UNI:F-UNI | `Wave2/W2-UNI/lemmas/L5_delivery.md:16` | (V)(R) states λ_min(Σ_n) > 0, unused; the argument uses the unit diagonal of setting (R) | hypothesis listed is unused, not insufficient |
| (i) | I1-M29 |  | W3-RM:Examples | `Wave3/W3-RM/lemmas/L7_examples.md:88` | UNI-1 row "RM-0 with Q = [p]" needs p ≤ ⌊n/2⌋ | in a "related through (C0)" remark, not a verified instance |
| (i) | I1-M32 |  | W3-SCR:SCR-M | `Wave3/W3-SCR/STATEMENT.md:122-123` | "SCR-A … special case" loose: 4e^{-x} vs 3e^{-x} | relation wording; L7:34 gives the repair |
| (i) | I1-M42 |  | W1-N3:Thm-N3-code(e) | `Wave1/W1-N3/STATEMENT.md:101-104` | (H2-FP) should carry NEG_INF = −∞ explicitly (stated only in (H2)) | fact about the code constant (v3_util.h:22), true for the pinned code; no narrowing |
| (i) | I1-M44 |  | W1-N3:LFP | `Wave1/W1-N3/STATEMENT.md:102-104` | same as M42 for LFP | dup of M42 |
| (i) | I1-M64 |  | W2-FAC-PKA:L4 | `Wave2/W2-FAC-PKA/lemmas/L4_table_discovery.md:12` | π(S0|data) never defined; step needs the exact posterior ∝ exp(F) | definition by the natural reading; no narrowing |
| (i) | I1-M73 |  | W2-FAC-XA:L8-S | `Wave2/W2-FAC-XA/lemmas/L8_truth_start.md:40-42` | block marginal m(·) never defined; one reading consistent with the interface | definition |
