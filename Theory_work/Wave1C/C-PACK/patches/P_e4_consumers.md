# Patch P-e4 — premise replacement e4 → e4′ in the three consumers (item 1)

Proof and audit: `lemmas/I1_e4_replacement.md` v2 (Lemma UM; §1.1; §4 text of e4′). Wave1 / NBH / SoP files are not edited;
HQ applies these on adoption. Aliases as in that file.

## PXN (`W1/W1-PXN/`)
1. `STATEMENT.md:33` "(… deterministic tie rule)" — append: "; the centre is the coded `start_mode(st, cap).S` under e4′
   (C-PACK I1 §4); no tie rule property is used".
2. `FINAL_PROOF.md:51-53` and `lemmas/LS_P6_repair.md:38-42` — replace "(N3 bypassed, not proved)" / "This **bypasses**
   the N3 tie-DP invariant (OB03) on this event; it does not prove N3." by "On {π₀(S°) > ½} the coded routine returns S°
   by C-PACK Lemma UM (W1-N3 (c), or (a), with N = 1; cap ≥ 1, (H1), (H4)). N3 for tied instances is not needed."
3. `FINAL_PROOF.md:14-15` (Lemma T, group versions) — add after "all laws used are unconditional": "Lemma T(i) is used
   for the mathematical tables, π₀ and aggregation quantities only; the coded centre is identified with S° on
   𝒜_n ∩ {π̃₀(S°) > ½} by Lemma UM, so P(C₀ ≠ S°) ≤ P(𝒜_nᶜ) + P(π̃₀(S°) ≤ ½) (C-PACK I1 §1.1)." (The original
   `API-PXNGAP/PROOF.md:106-108` sentence "and the LS0 centre is S̃₀^~" is not used.)
4. Premise list (STATEMENT §1 OP-LS0 / EX-A): add e4′; keep EX-A unchanged.

## GEN (`W1/W1-GEN/`)
5. `STATEMENT.md:43-44` and `lemmas/00_MAIN.md:10` — replace "**e4** (emitted LS0 centre = the prescribed start-mode
   maximiser; DP invariant N3 OPEN, owned by W1-N3)" by "**e4′** (C-PACK I1 §4: LS0 centred at and emitting the coded
   start_mode output, a deterministic data function on every branch; H1, H4 of W1-N3; cap ≥ 1)".
6. `lemmas/L2_centre.md:58-59` — replace "under premise e4 the emitted LS0 centre is S*" by "by C-PACK Lemma UM (W1-N3 (c)
   with N = 1) and e4′ the emitted LS0 centre is S*".
7. `lemmas/L5_assembly.md:13` "(e4)" → "(e4′)"; `:41-45` Note (0) — replace by (R39 #3 text) "The mathematical centre-identification part of e4′ is
   used on `{π₀(S*) > ½}` (L2 step 9), where Lemma UM identifies the coded centre with S*. The all-data deterministic-centre,
   emitted-centre, OP-LS0, guard and complete-scan contracts remain in force for the closure argument, including outside
   that event. Their implementation remains an obligation for C-ENG."
8. `lemmas/L7_counterexample.md:63-75` ((C6)) — add: "Here maximality of S̃₀ is N3(a) under EX-A (any cap, truncated or
   not); (C6) is not covered by e4′'s binary64 alternative."
9. `lemmas/L6_instances.md:42` "premises (incl. N3)" → "premises (incl. e4′)".

## M5(b1-LH) (`NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md`; card `SoP/04_theory.tex:484-521`)
10. Card implementation premises (`:484`) "e4" → "e4′"; Risk/Fallback rows (`:507-509`, `:521`): "N3 OPEN (DP invariant)"
    → "N3 not needed for (b1-LH) (C-PACK Lemma UM); LS0 integration (e4′ (i)–(iii)) pending (C-ENG)"; the fallback label
    "conditional on N3" becomes unnecessary.
11. `T38_PROOF.md:254` step 1 — append: "The coded routine returns S° on this event by C-PACK Lemma UM."
12. `T38_PROOF.md:263-266` (data-dependent-centre alternative, PROOF SKETCH) — unchanged and **not covered** by e4′.

## Additions after mid-point R38 (finding 1; `reviews/R38_midpoint_sol.md`)
13. In `W1/W1-GEN/lemmas/00_MAIN.md:10`, replace `e4 [N3 OPEN]` by `e4′ (C-PACK I1 §4)`. (Item 5 above applies to
    `STATEMENT.md:43-44` only; 00_MAIN's text differs.)
14. In `W1/W1-GEN/STATEMENT.md:28`, replace `start mode S̃₀ = argmax_Ω γ₀ with the size-then-lex tie rule` by `coded start
    centre S̃₀ := start_mode(st, cap).S under e4′ (C-PACK I1 §4); on {π₀(S*) > 1/2}, Lemma UM identifies it with S*`.
15. In `W1/W1-PXN/STATEMENT.md:33`, replace `centred at the exact start mode S̃₀ = argmax π₀ (max-plus convolution of block
    tables, deterministic tie rule)` by `centred at S̃₀ := start_mode(st, cap).S under e4′ (C-PACK I1 §4); on
    {π₀(S°) > 1/2}, Lemma UM identifies it with S°` (this supersedes item 1 above).
16. In the unquoted explanatory prose of `SoP/04_theory.tex:505,515`, replace the requirement for the prescribed e4/N3
    centre by `the emitted coded centre under e4′ (C-PACK I1 §4), identified with S° on {π₀(S°) > 1/2} by Lemma UM; EX-A
    and LS0 integration remain premises`. Preserve the verbatim historical status rows, including N3 "OPEN", and identify
    this as a C-PACK addendum.
These instructions supplement, rather than remove, P-e4's retained EX-A, H1, H3–H4, OP-LS0 and complete-scan contracts.
Note: on tied (and possibly truncated) instances e4′ specifies the coded output and does not assert the prescribed lex choice.

## Additions after council C1 (opus non-blocking #1; `reviews/C1_council_opus.md`)
17. `W1/W1-GEN/REPORT.md:16,30,97` and `W1/W1-PXN/REPORT.md:47`: read e4 as e4′ (C-PACK I1 §4); keep the historical verdict
    text. (`W1/W1-PXN/lemmas/ERRATA.md:17` likewise: historical, append a pointer to Lemma UM and I1 §1.1.)
18. `SoP/04_theory.tex:84`: after the e4 definition add "C-PACK addendum: for the consistency cards, e4 may be replaced by
    e4′ (C-PACK I1 §4); N3 status unchanged."
19. `W1/W1-GEN/lemmas/L5_assembly.md:69`: the start-mode part of "the deterministic tie rules" is the coded centre of e4′ (ii),
    a deterministic measurable data function on every branch.
