# Stage B, Opus 5.5 (xhigh) reviewer, round 3 — reply saved verbatim (PROOF_v3, STATEMENT_v3)

# Review report, round 3 (confirmation): T31 (T22), part (i), PROOF_v3 against STATEMENT_v3

**Overall: verified.** Every round-3 change is correct, and no hypothesis or conclusion changed. All five Round 2 answers in CLAIMS_OF_FATAL_FLAWS.md are acceptable. No fatal or gap findings remain; the three findings below are wording only.

**Packet read (round 3):** PROOF_v3.tex, pages 4–5 of PROOF_v3.pdf (the changed part), STATEMENT_v3.md and CLAIMS_OF_FATAL_FLAWS.md. I compared them against PROOF_v2.tex and STATEMENT_v2.md from the same folder. I ran nothing. PDF pages 4–5 match the .tex.

## A. What changed, and confirmation that no hypothesis or conclusion changed

### PROOF_v3 against PROOF_v2
- Only the author line (line 16) and the final paragraph of Remark 13 (lines 247–265) differ.
- Everything else is word for word the same: Lemma 1, Lemma 2, Theorem 3, Remarks 4, 5 and 8, Lemma 6, Corollary 7, Lemma 9, Corollary 10, Theorems 11–12, and the first paragraph of Remark 13.
- So my round-1 and round-2 checks of those parts still apply.

### STATEMENT_v3 against STATEMENT_v2
**Identical:**
- the source quote;
- all §1 definitions, including the definition of P_c and E_c themselves ("probability and expectation over the final streams 10–13, with the calibration fixed at c");
- §2 (EX-A, EX-S, CAL, (H-T12));
- the §3 opening "Under EX-A, EX-S, CAL and (H-T12)";
- the definition of 𝓛(Z);
- (a), (b), (c), (d1), (d2), and the sentence after (d2).

**Changed (explanatory only):**
- **§1, lines 37–40.** The sentence linking P_c to the conditional law given 𝓒 now carries a joint-measurability proviso and a version/success-event qualifier, and adds "All conclusions below are stated for P_c".
  - The proviso is not added to §2 and does not qualify any conclusion. It only qualifies the explanatory identification with the conditional law.
  - Faithfulness to the source is unaffected. The source writes P_𝓒 with a subscript, which reads naturally as the frozen-calibration law P_c evaluated at c = 𝓒, and that reading needs no proviso.
- **§3 preamble, lines 70–74.**
  - "Nor that they are not realised" is added.
  - "The only true one" is replaced by "the intended one; the per-data-set reading about the actual estimator would be false".
  - "The method does not report" is replaced by "not among the reported quantities listed above".
- **Changes log.** Updated. It cites review/STATEMENT_as_reviewed_r2.md, which is not in my packet. I compared against STATEMENT_v2.md in the packet.

**Conclusion:** no hypothesis, definition of a conclusion's terms, or conclusion changed.

### New final paragraph of Remark 13 (lines 247–265): step-by-step check
- **Stage factors.** The grid is strictly increasing, so φ_t − φ_{t−1} > 0. Each term exp{(φ_t − φ_{t−1})·d(S)}, and hence each stage average, lies in [e^{(φ_t−φ_{t−1})d_min}, e^{(φ_t−φ_{t−1})d_max}]. Correct.
- **Product.** Σ_t(φ_t − φ_{t−1}) = φ_T − φ₀ = 1, so each Ẑ_r, and their average Ẑ, lies in [A·e^{d_min}, A·e^{d_max}] with A = m(∅)Z̄₀ > 0 (Lemma 1). Correct.
- **Z.** ϖ(S)·BF(S) = γ₀(S)·e^{d(S)}, by the definitions and the positivity in Lemma 1(ii). So Z/A = Σ_S γ₀(S)e^{d(S)}/Z̄₀ is a γ₀-weighted average of the e^{d(S)} (positive weights summing to 1), and Z lies in the same interval. Correct.
- **Sure bound.** It follows that e^{−Δ}Z ≤ Ẑ ≤ e^{Δ}Z surely. Correct.
- **SD bounds.** The four values log Ẑ_r lie in an interval of length at most Δ. The mean minimises the sum of squared deviations, and each value is within Δ/2 of the interval's midpoint, so the sum of squared deviations is at most 4(Δ/2)² = Δ². Hence population SD ≤ Δ/2 and sample SD ≤ Δ/√3. Correct.
- **Δ ≤ √3.** Both SDs are then at most 1, so the flag, which requires SD strictly above 1, is never raised. Correct.
- **e^{Δ} ≤ 1/α.** Then αẐ ≤ αe^{Δ}Z ≤ Z, so coverage holds surely. Correct.
- **Existence claim.** These statements are now conditional ("if …", "for such data"). The paragraph claims no such data exist, and states that realisability of the (c)–(d) laws is not addressed. Correct.
- **Independent flag.** "A flag of positive probability independent of Ẑ would preserve coverage": P(cov | F) = P(cov) ≥ 1 − α. Correct.

## B. Rulings on the Round 2 rows of CLAIMS_OF_FATAL_FLAWS.md

**R2-1 ("only true one" overclaim): agree; the change works.**
- "The only true one" is gone, and the new last sentence correctly states that realisability is not addressed.
- The replacement claim, that the per-data-set reading is false, is true for both (c) and (d). As written, though, the paragraph proves it for (c) and argues (d) only conditionally (see R3-1 below).

**R2-2 (small-Δ claims): agree; the change works.**
- The SD upper bounds are now derived correctly (see §A), the thresholds are explicit, and the claim is stated conditionally without asserting such data exist.

**R2-3 (implicit steps; "method does not report"): agree; the change works.**
- Positive increments, the averaging step and the γ₀-weighted average are all written out and correct.
- "Not among the reported quantities" can now be checked against the packet. A small wording mismatch remains (R3-3).

**R2-4 (joint-measurability proviso in STATEMENT §1): agree; the change works.**
- The proviso, the "version" qualifier, the success-event qualifier and the line saying conclusions are stated for P_c together make §1 consistent with Remark 4.
- No §2 hypothesis was added.

**R2-5 (file name cited by the proof): agree with not changing it.**
- The packet copies are renamed only to keep versions apart, and the definitions the proof relies on are word for word the same in STATEMENT.md, STATEMENT_v2.md and STATEMENT_v3.md.

**Round 2 summary text.** It accurately describes my round-2 rulings: verified, no fatal or gap findings, agreement on rows 2–11 with partial caveats on rows 3 and 4, and acceptance of row 1 with the wording objection. I cannot confirm the Astra reviews, which are not in my packet.

## C. Findings (round 3)

**Finding R3-1**
- Location: PROOF_v3 Remark 13, line 247; STATEMENT_v3 §3, lines 71–72.
- Severity: exposition.
- Claim: "The per-data-set reading about the actual estimator is false" is justified in the text only for (c), through the sure bound, which holds for every data set. For (d) the text gives only a conditional argument (data with Δ ≤ √3 or e^{Δ} ≤ 1/α) and makes no existence claim.
- Evidence: The claim is still true for (d), for every data set and without any small-Δ assumption.
  - Under P_c, Ẑ takes finitely many values (Lemma 1). For α < Z/max Ẑ, coverage holds surely.
  - So per-data (d1) fails for that α: either P_c(raised) = 0, or P_c(cov | raised) = 1 ≠ 0.
  - Per-data (d2) fails for that α and any γ ≤ 1: either P_c(not raised) = 0, or P_c(cov | not raised) = 1 ≥ γ.
  - Nothing false is asserted; part of the reasoning is just not on the page.

**Finding R3-2**
- Location: PROOF_v3 Remark 13, line 249.
- Severity: exposition.
- Claim: The symbol A is reused for m(∅)Z̄₀. A already names the event of Lemma 6 (cited in Remark 8), and the similar script 𝒜 is the value set in Corollary 10.
- Evidence: Inside Remark 13 the meaning is clear, so this is cosmetic.

**Finding R3-3**
- Location: STATEMENT_v3 line 73 ("reported quantities listed above"); PROOF_v3 line 256 ("the Ẑ_r, Ẑ and 0.05Ẑ").
- Severity: exposition.
- Claim: STATEMENT §1 explicitly calls only 0.05·Ẑ "reported" (plus the E2 flag). The proof's list of reported quantities is its own.
- Evidence: Harmless. e^{Δ} is a deterministic data constant and is none of the listed random quantities under either list.

**No fatal or gap findings.**

## D. Conclusion

PROOF_v3 proves (a), (b), (c), (d1) and (d2), with (d) for both SD divisors, under exactly the hypotheses of STATEMENT_v3 (EX-A, EX-S, CAL, (H-T12)). STATEMENT_v3 changes no hypothesis or conclusion of STATEMENT.md or STATEMENT_v2.md and remains a faithful formalisation of source clause (i). The round-3 text is mathematically correct.

**verified**
