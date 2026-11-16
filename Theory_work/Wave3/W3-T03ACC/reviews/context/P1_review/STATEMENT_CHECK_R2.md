# Statement checker reply, round 2 (final text): APPROVED

# STATEMENT_CHECK_R2: T01 and T02 (wave 3)

**Verdict: approved.** The current STATEMENT.md can be used as is. I re-read it in full, and every round-1 change is in and correct. I found nothing false and no misstatement of the original conjectures or 00_COMMON. Four small wording fixes are listed at the end; none of them blocks.

Same constraints as before: I read only the listed files, ran nothing, and am replying inline.

## Ruling on each change

**C1: (T)(b) — approved.**
- **(b1) is true.** My earlier p = 1 construction is a valid witness:
  - Take ‖y_c‖² = t fixed, Δ = a log n/n and a = r₁ + r₂ + t.
  - The log Bayes factor is then ½ log n·(a/(2r + t) − 1) + o(1), which tends to +∞ at r₁ and −∞ at r₂.
  - The function g is ruled out in both directions:
    - If b < b′, use {S = ∅}: Π_b → 0 while Π_{b′} → 1.
    - If b > b′, use {S = {1}} in the same way.
  - The witness probabilities stay positive, so g(Π_b(E)) → 0 would contradict Π_{b′}(E) → 1.
- **(b2) is true**, by the p = 2 construction from my revised reply:
  - Orthogonal columns, with Q^c_{1} − Q^c_{12} = a log n/n.
  - a in (2b₋ + s², 2b₀s² + s²) gives the first witness; a in (2b₀s² + s², 2b₊ + s²) gives the second.
  - The strict-interior condition on s² is used, and n ≥ 4 is needed so that K = 2.
- **The closing "no constant C, independent of n and of the data" claim follows**, since the ratio Π(E | y)/Π_b(E) tends to ∞ on the witnesses. Dropping the "growing factor" phrase was right: as I showed, the factor (b₊/b₋)^ν always works.
- **The "worst case over inputs, not P₀" heading is right.**
- **Faithfulness:**
  - (a) is the positive content of the original sentence.
  - (b2) is the negative content on "the event of (iii)".
  - (b1) is an extra true statement and changes no hypothesis.

**C2: notation — approved.** All model events are now written as {S = ·}.

**C3: U — approved.**
- §1 now says U is fixed and non-random, so the exact law in (iii) holds.
- "May depend on n only" is stricter than necessary but harmless, because the deterministic claims don't depend on U.
- Reading 7 is correct.

**(ii) — approved.**
- With b₁, b₂ and κ₁₂ = (b₂/b₁)^{0.51}, all three inequalities hold pointwise for any numbers 0 < b₁ ≤ b ≤ b₂. The added note is accurate.
- Using (ii) at b = b₀s_y² is now plainly allowed.

**Discipline clause — approved.** It is the wording I suggested.

**Readings 8–10 — approved.** They record the earlier U1–U5 accurately, and 00_COMMON does list a `no_predictors` status, which covers p = 0.

## Optional wording fixes (non-blocking)

1. **Reading 2** still says "U is any orthonormal basis of 1^⊥". Change it to "any fixed orthonormal basis" so it matches §1 and reading 7.
2. **Reading 10** cites "checker's note E8". My round-1 replies were inline and numbered differently: in the revised reply that note is E7, and E8 is the T02 check. Cite it by content instead ("the checker's P₀ sketch").
3. **(b1)** could add one sentence: "its inputs have s_y² → 0, so they lie outside 𝓑_n for large n; (b2) is the version on 𝓑_n." This would stop a proof writer from using (b1) for claims about 𝓑_n.
4. **Reading 4** could name the (b1)/(b2) split. Its current wording, "counterexample to any data-free same-rate implication", is still accurate.

## Counterexample referee

None. Every part of the current precise statement is either checked by hand or has no counterexample I could find.

### Critical Files for Implementation
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\proofs\T01_T02_contrast_dimension\STATEMENT.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\T01_A0_contrast_reduction.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\T02_A1_dimension_supersets.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\00_COMMON.md