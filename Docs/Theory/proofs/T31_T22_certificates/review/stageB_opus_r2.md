# Stage B, Opus 5.5 (xhigh) reviewer, round 2 — reply saved verbatim (PROOF_v2, STATEMENT_v2, claims log)

# Review report, round 2: T31 (T22), part (i), PROOF_v2 against STATEMENT_v2

**Overall: verified.** PROOF_v2 proves (a), (b), (c), (d1) and (d2) under exactly the hypotheses of STATEMENT_v2, and STATEMENT_v2 changes no hypothesis, definition or conclusion. The one thing that needs action is that both files now say the non-implication reading is "the only true one". That is not established, and my own round-1 Finding 1 invited the wording. It is exposition only because no conclusion depends on it.

**Packet read (round 2):** STATEMENT_v2.md, PROOF_v2.tex, PROOF_v2.pdf and CLAIMS_OF_FATAL_FLAWS.md. I compared them against STATEMENT.md and PROOF_v1.tex, which are the round-1 versions in the same folder. I ran nothing. The PDF matches the .tex: Lemma 1 through Remark 13, including the new Remark 4 and the final paragraph of Remark 13 on page 5.

## A. Does STATEMENT_v2 change any hypothesis or conclusion of STATEMENT.md?

No. Line-by-line comparison:

**Identical word for word:**
- the source quote and the header;
- §1, all definitions, including P_c/E_c, the formula for Ẑ_r and the E2_final definition with both divisors;
- §2: EX-A, EX-S, CAL, (H-T12);
- §3: the opening "Fix any successful calibration value c. Under EX-A, EX-S, CAL and (H-T12)";
- (a), (b), (c), (d1), (d2);
- "Both hold for either SD divisor";
- the definition of 𝓛(Z): i.i.d., finitely many values in (0, ∞), E Ẑ_r = Z.

**Changed (explanatory text only):**
- **§3 preamble, lines 65–71.**
  - The old clause "has all properties of the final-run evidence … together with island independence, identical distribution and islandwise unbiasedness" is replaced by "has every property of Ẑ that the proof of (a)–(b) uses (positive, finitely many values, mean Z)". A sentence is added saying the extra requirements of 𝓛(Z) are not hypotheses about the actual run.
  - A new sentence asserts that the non-implication reading is "the intended one, and the only true one", together with the sure bound e^{−Δ}Z ≤ Ẑ ≤ e^{Δ}Z.
- **Lines 83–85:** a sentence saying "final flags" is read existentially.
- **"Approved changes" section:** now describes the exposition edits. It cites review/STATEMENT_as_reviewed_r1.md, which is not in my packet. I compared against STATEMENT.md, the version I reviewed in round 1.

The added text contains two new mathematical assertions:
1. The sure bound. It is correct and is proved in the final paragraph of Remark 13 (checked in §B).
2. "The only true one". This is not established; see Finding R2-1.

Neither is one of the lettered conclusions.

## B. Verification of what is new or changed in PROOF_v2

**Lemma 1(ii), lines 56–59.**
- The proof now uses (i) only for S ∈ Ω.
- The table entries that actually enter γ₀ and d are r_b(S ∩ C_b) with S ∈ Ω. Since |S ∩ C_b| ≤ |S| ≤ K, we have S ∩ C_b ∈ Ω, so BF(S ∩ C_b) ∈ (0, ∞) by (i).
- The rest is unchanged. Checked; this resolves round-1 Finding 8.

**Lemma 1(iii), lines 61–73.**
- T ≥ 1 follows from φ₀ = 0 < φ_T = 1. Correct.
- N_e ≥ 1 is taken as part of what "particle count" means. This is acceptable: the §1 formula is undefined otherwise.
- That every state lies in Ω is now taken from STATEMENT §1 alone, with π₀ and the "moves" remark removed.
- Finite-valuedness is argued pointwise (Ẑ_r(ω) ∈ g(Ω^{N_e T})), and measurability comes from EX-S applied to Ẑ_r as an output.
- If anyone doubts that island evidences count as "outputs", note that (a) and (b) only need the pooled Ẑ, which is certainly an output, and the E2 flag is computed from the Ẑ_r.
- Checked; this resolves round-1 Findings 6 and 7.

**Remark 4 (P_c and conditioning on 𝓒), lines 110–117.**
- The content is correct. If the final outputs are F(c, U), with U independent of 𝓒 and F jointly measurable, then the substitution (freezing) lemma gives P(· | 𝓒) = P_𝓒 almost surely on the success event.
- "CAL is used only here" is accurate: Theorem 3 lists CAL but its proof does not use it.
- One residual: joint measurability of F is stated as a proviso, not derived. See Finding R2-4.

**Remark 5 (extended), lines 119–126.**
- "Adding [the extra properties] to the class only makes the non-implications stronger" is correct. A witness law satisfying the larger set of properties P′ ⊇ P shows that P′ does not imply Q, and hence neither does P.
- It also correctly says these properties are not hypotheses about the actual run.
- Checked; this resolves round-1 Finding 5.

**Theorem 11 proof, line 200.** The ambiguous "On this event" is now "On the event {E2_final raised}". Checked.

**Theorem 12 proof, line 219.** e > 2.718 gives e³ > 2.718³ ≈ 20.0793 > 20.07, so e³ − 1 > 19. Checked.

**Remark 13, final paragraph, lines 247–257 (the sure bound).** I re-derived every step.
- **Stage factors.** The grid is strictly increasing, so φ_t − φ_{t−1} > 0. Each term exp{(φ_t − φ_{t−1})·d(S)} therefore lies in [e^{(φ_t−φ_{t−1})d_min}, e^{(φ_t−φ_{t−1})d_max}], and so does their average.
- **Product over t.** Since Σ_t(φ_t − φ_{t−1}) = φ_T − φ₀ = 1, the product lies in [e^{d_min}, e^{d_max}]. So Ẑ_r ∈ m(∅)Z̄₀·[e^{d_min}, e^{d_max}] surely, and the same holds for Ẑ as the average of the Ẑ_r. This averaging step is left implicit.
- **The identity.** By definition γ₀(S) = ϖ(S)·∏_b r_b(S ∩ C_b) and e^{d(S)} = BF(S)/∏_b r_b(S ∩ C_b), with all factors positive by Lemma 1(ii). So ϖ(S)·BF(S) = γ₀(S)·e^{d(S)}.
- **Z.** Z = m(∅)·Σ_S ϖ(S)BF(S) = m(∅)·Σ_S γ₀(S)e^{d(S)}. Dividing by m(∅)Z̄₀ leaves a γ₀-weighted average of e^{d(S)}, which lies in [e^{d_min}, e^{d_max}]. This step is also left implicit.
- **Conclusion.** Ẑ and Z lie in the same interval [L, L·e^{Δ}], so e^{−Δ}Z ≤ Ẑ ≤ e^{Δ}Z surely. Correct.
- **"Flag can never be raised" for small Δ.** True, but not derived in the proof. The four values log Ẑ_r lie in an interval of length Δ, so the sum of squared deviations is at most Δ². That gives population SD ≤ Δ/2 and sample SD ≤ Δ/√3. So Δ ≤ √3 rules the flag out for either divisor.
- **"Coverage can hold surely".** True when e^{Δ} ≤ 1/α, because then αẐ ≤ αe^{Δ}Z ≤ Z.
- **"A flag independent of Ẑ would preserve coverage".** True for a flag with positive probability: P(cov | F) = P(cov) ≥ 1 − α.
- See Findings R2-1, R2-2 and R2-3 for what this paragraph does not establish.

**Unchanged parts.** Lemma 1(i), Lemma 2, Theorem 3, Lemma 6, Corollary 7, Remark 8, Lemma 9, Corollary 10, the statement of Theorem 11 and the rest of both proofs are verbatim the same as v1. My round-1 checks still apply, and the cross-references after renumbering (Remark 5, Corollary 10) resolve correctly.

## C. Findings (round 2)

**Finding R2-1**
- Location: STATEMENT_v2.md §3 preamble, line 69 ("the intended one, and the only true one"); PROOF_v2.tex Remark 13, line 247 ("This reading is the only one under which (c) and (d) are true").
- Severity: exposition. No lettered conclusion depends on it. If the lead treats the §3 preamble as something to be proved, it becomes a gap, not a fatal flaw.
- Claim: The claim that this is the *only* true reading is not established. The sure bound refutes only one other reading: that, for a fixed data set, the actual estimator admits no relative-error bound at all.
- Evidence:
  - **(c), uniform-over-data reading not refuted.** Consider "the actual method has no data-independent relative-error guarantee": for every 0 < c₁ ≤ 1 ≤ c₂ and γ > 0, some data set and successful c give P_c(c₁Z ≤ Ẑ ≤ c₂Z) < γ. This is neither proved nor refuted. The sure bound uses a constant e^{Δ} that depends on the data, so it says nothing about this reading.
  - **(d), realisability reading not refuted.** Consider "for some data set and successful c, the actual P_c(Z ≥ αẐ | E2_final raised or not raised) < 1 − α". This is also neither proved nor refuted. The small-Δ argument only refutes the reading "for every data set".
  - **My share of this.** My round-1 Finding 1 said the non-implication was "the only reading under which the clause is true", and that wording appears to be the source of the overclaim. I withdraw it. What round 1 actually showed is narrower: the per-data-set reading about the actual estimator is false, so the non-implication reading is the right one to formalise.

**Finding R2-2**
- Location: PROOF_v2 Remark 13, lines 254–256 ("for data with small Δ the flag E2 can never be raised … conditioning on a flag can preserve coverage for some data").
- Severity: exposition.
- Claim: The proof gives no threshold and no derivation for "never raised" or "holds surely". It also assumes, without showing it, that data with small Δ exist.
- Evidence:
  - "Never raised" needs an *upper* bound on the SD in terms of the range; Lemma 9 only gives a lower bound. The bound and thresholds are in §B: the flag cannot be raised when Δ ≤ √3 (either divisor), and coverage holds surely when Δ ≤ log(1/α).
  - "Can preserve coverage for some data" assumes some admissible (X, y) has Δ ≤ √3. One example would be a single block, which makes d ≡ 0. Whether the method's block construction allows that cannot be checked from the packet. The refutation of the "for every data set" reading of (d) rests on this existence claim.

**Finding R2-3**
- Location: PROOF_v2 Remark 13, lines 248–253.
- Severity: exposition.
- Claim: The derivation of the sure bound leaves three one-line steps implicit:
  1. φ_t − φ_{t−1} > 0, from the strict grid, which is needed for the direction of the interval;
  2. passing from the Ẑ_r to Ẑ by averaging;
  3. writing Z/(m(∅)Z̄₀) as a γ₀-weighted average of e^{d}.

  Two remarks there are also claims about the method or the data that I cannot check from the packet: e^{Δ} "can be astronomically large", and "the method neither computes nor reports" it. The second also appears in STATEMENT_v2 line 70.
- Evidence: I verified steps 1–3 in §B. The two unverifiable remarks have no bearing on any conclusion.

**Finding R2-4**
- Location: PROOF_v2 Remark 4, lines 112–115; STATEMENT_v2 §1, lines 37–38.
- Severity: exposition.
- Claim: Remark 4 needs F(c, u) to be jointly measurable in (c, u) and states this as a parenthetical proviso. STATEMENT_v2 §1 still says, unconditionally, that P_c and E_c are the conditional law and expectation given 𝓒 = c "under CAL and EX-S".
- Evidence: EX-S gives measurability of outputs as functions of the streams, that is G(V, U) with V = streams 0–9. It does not give measurability of F in c. The step can be repaired with standard tools: apply Fubini to G, condition on σ(V), then project onto σ(𝓒), with universal measurability where needed. It is not one of the conclusions, since (a) and (b) are stated and proved for P_c.

**Finding R2-5**
- Location: PROOF_v2 line 21; Lemma 1(iii); Remarks 4 and 5.
- Severity: exposition.
- Claim: The proof still cites "STATEMENT.md", but the statement under review is now STATEMENT_v2.md.
- Evidence: Harmless, because §1–§3 definitions are word-for-word identical (see §A).

## D. Rulings on CLAIMS_OF_FATAL_FLAWS.md

**"Fatal or gap findings: None."** Agree for my own round-1 review: no fatal or gap findings, verdict verified. I cannot confirm the two Astra reviews, which are not in my packet. My round-2 review also finds no fatal or gap findings.

| # | Finding | Agree with the answer? | Does the change work? |
|---|---|---|---|
| 1 | Non-implication reading; sure bound | Agree with accepting it. The derivation in Remark 13 and the bound restated in STATEMENT_v2 are correct (§B). | Partly. The bound is right, but "the only true one" / "the only one under which (c) and (d) are true" goes beyond what is shown (R2-1), partly because of my own round-1 wording. The small-Δ sentence lacks its derivation and the existence of such data (R2-2). |
| 2 | "Final flags" plural vs one witness | Agree | Yes. STATEMENT_v2 lines 83–85 and Remark 13 state the existential reading correctly. "A flag independent of Ẑ would preserve it" is correct for flags of positive probability. |
| 3 | P_c ↔ conditional law given 𝓒; CAL unused | Agree | Mostly. Remark 4 is correct, and the a.s. qualifier and the success event are now explicit. Residual: joint measurability of F is assumed, not derived, and STATEMENT §1 still states the identification without that proviso (R2-4). |
| 4 | Fidelity to METHODOLOGY_v3 and T12 not checkable | Agree it is a scope note and needs no change | Not applicable. The lead's check (formula for Ẑ_r = §6.12 verbatim; E2 = §6.9; (H-T12) = T12(iii)) is outside my packet and I have not verified it. |
| 5 | Preamble could imply i.i.d. / islandwise unbiasedness of the actual run | Agree | Yes. The STATEMENT_v2 preamble and the extended Remark 5 are accurate, and the logic ("only makes the non-implications stronger") is correct. |
| 6 | π₀ and "moves stay in Ω" not in packet | Agree | Yes. Lemma 1(iii) now relies only on STATEMENT §1. |
| 7 | Measurability via "outputs"; N_e ≥ 1; T ≥ 1 | Agree | Yes. T ≥ 1 is derived. N_e ≥ 1 comes from the meaning of the formula, which is acceptable. Measurability now comes directly from EX-S on outputs, and finite-valuedness is pointwise. |
| 8 | Table entries with \|A\| > K | Agree | Yes (Lemma 1(ii), lines 56–58). |
| 9 | "On this event" ambiguous | Agree | Yes (line 200). |
| 10 | e³ > 20 unjustified | Agree | Yes (line 219; 2.718³ ≈ 20.079 > 20.07). |
| 11 | "No upper limit on Z/Ẑ" is informal | Agree; no change needed | Not applicable. As mathematics it is the identity {Z ≥ αẐ} = {Z/Ẑ ≥ α}, so it is true and needs no proof. |

## E. Conclusion

Under exactly the hypotheses of STATEMENT_v2 (EX-A, EX-S, CAL, (H-T12)), PROOF_v2 proves every conclusion: (a), (b), (c), (d1) and (d2), with (d) for both SD divisors. STATEMENT_v2 changes no hypothesis, definition or conclusion of STATEMENT.md and remains a faithful formalisation of source clause (i). All findings are exposition. The one with substance is R2-1, the "only true one" overclaim in both files; it is commentary and affects no conclusion. No fatal or gap findings.

**verified**
