# Fable 5.1 (high) Stage C review: phase 1 (blind)

Thread <thread>, 2026-10-22, completed 17:39Z. The verdicts and findings below are copied verbatim from the reply. The reply's per-theorem "What I checked" paragraphs are kept in the thread and in the lead's session log.

Phase 1 is complete. I read, for each of the ten chapters, parts (a), (b) and (c) only, plus 00_COMMON.md and METHODOLOGY_v3.md. I did not read any part (d), the overview table, or any review file, and I ran no commands. Verdicts below were formed before seeing any review material.

## Findings by theorem (verbatim)

### T09
- (exposition) Part (v) family: three orthonormal vectors in 1^⊥ need n ≥ 4, while the setting allows n ≥ 3. Harmless, since the claim is for n ≥ n₀.
- (exposition) The constant 55 has very little slack (1.3926 against 1.3863). Correct as written.
Statement fidelity: the readings of (iii) "need not be reversible" (existence of a non-reversible order) and of (v) (an explicit family with ε₁ exponentially small, a switch, range linear in n, yet gap ≥ 1/40 and t_mix ≤ 55) are honest and stated beside the original wording. No hypothesis added.
Verdict: correct.

### T11(iii)
- (exposition) Setting item 5 assumes the launched final run executes all rounds; the Remark justifies this under EX-A (no numerical_failure) and declares environment aborts outside the model. Acceptable as an idealisation, and it is declared.
Statement fidelity: exact. The scope note correctly excludes the adaptive calibration draw count, with a correct counterexample in Remark 6.
Verdict: correct.

### T12
I could not run the interval-arithmetic script. I checked plausibility by hand from the printed values (b₁ ≈ 0.224, b₂ ≈ 0.474, b₁₂ ≈ 366, PIP₁ ≈ 0.9906; bias near −0.17; E[Ẑ₁PIP̂₁|F] ≈ 0.8Z₀ against Z·PIP₁ ≈ 96.4Z₀ matches the printed −95.6Z₀).
- (exposition) The code and log for (iv.b)/(iv.e) enter the proof by file inclusion (\lstinputlisting of build/helpers files) and are not reproduced in the collected text, unlike T13's inline script. A reader of the collected document cannot check them. The certificate is accepted here as reported.
- (exposition) The instance has p = 2 and N = 1; the statement scopes this correctly as a component example.
Statement fidelity: all seven informal clauses of the original (iv) are given precise forms; the T09(i) import (START) is labelled. No conclusion weakened.
Verdict: correct, with the (iv.b)/(iv.e) numerical certificate taken as reported.

### T13
Hand checks: t₁+t₂ ≈ 0.928, D ≈ 2.457; a_c(0) ≈ 0.979, a_c(1) ≈ 0.927, a_c(2) ≈ 0.573; ρ(0,½) ≈ 0.9708, ρ(½,1) ≈ 0.9138.
- (exposition) (ii)(b) rests on the reading that the construction's left point is always the last appended point; the proof states this reading and it is the only one consistent with the method text.
- (exposition) The witnesses' blocks are never computed; only size ≤ 6 and the partition property are used, which the proof justifies from the method text.
Statement fidelity: the ten listed changes are each justified. The weakening in (iv)(a) (explicit pool-avoidance or provenance condition instead of "calibration never scores 𝓜") is honest: the method does not say whether tables or carried leaders feed V's top lists.
Verdict: correct.

### T14(i)
Findings. None. Statement fidelity: exact; the (i-d) reading is declared to be an abstract instance, not an SMC-BVS data set. The hypothesis "one q_t-invariant round per stage" is what T09(iii) proves.
Verdict: correct.

### T15
Findings. None. Statement fidelity: exact; the pooled-tail sentence is made a non-implication with scope stated.
Verdict: correct.

### T20(i)–(ii)
- (exposition, unverifiable here) H03 is stated as "1 − π(S₀) = O_{P₀}(r_n) with S₀ ∈ Ω eventually". T03 is not in the collection, so I could not confirm this is exactly T03(i)'s conclusion. The method's §11 V2 target has rate √(log n/n) + e^{−ω_n}, which with ω_n = ½log n is O(r_n), so no conflict is visible.
Statement fidelity: the seven readings (returned model = running HPM, "within the cap", "iff" for the certificate, EXEC) are declared and consistent with METHODOLOGY §6.10.
Verdict: correct.

### T22(i)(ii)(iv)
Findings. None. Statement fidelity: the added hypothesis S₀ ∈ Ω for (ii) and (iv) is necessary (the n = 3, p = 2 instance shows (ii-a) fails without it) and is recorded as approved. The generalisation to all real X, y and all partitions is strictly stronger than the source.
Verdict: correct.

### T23(ii)
- (exposition) ρ is read as the whole-round departure probability from S₀ (reading 1). This is at least as large as any prefix-departure probability, so it is a slightly stronger hypothesis than "truth prefix-departure ≤ ρ" in the inventory; it is declared and matches what T23(iii) intends to bound.
Statement fidelity: exact on the inequalities and constants; readings declared.
Verdict: correct.

### T31(i)
Findings. None. Statement fidelity: (a),(b) are the original claims; "not a relative-error interval" and "conditioning on final flags" are formalised as non-implications over the class 𝓛(Z), with the per-data-set reading explicitly shown to be false. Honest and justified.
Verdict: correct.

## Cross-theorem checks (verbatim)
- T15's (H-T12) against T12: T15's set 𝒯 of positions (a), (b), (c) is exactly T12's list (i.a)–(i.c), transferred to conditioning on 𝓒 via the freezing lemma. Consistent.
- T31's (H-T12) is T12 (i.a) at t = T with h ≡ 1, averaged over four islands, as T12 (iii) states. Consistent.
- T12's START is T09(i). Consistent.
- T14's hypothesis "one q_{φ_t}-invariant round per stage" is T09(iii). Consistent. T14 re-derives the unbiasedness identity rather than citing T12, and the two agree.
- T23's initial-occupancy δ is defined at T15's position (a). Consistent.
- Final-run description across T11, T12, T14, T15, T23, T31: all chapters agree; T11's count T+L+4 rounds per particle matches.
- Hypotheses from conjectures not in this collection: T20's H03 (from T03) and T22's (iv-c) hypotheses (from T03 and T22(iii)) are explicit and used only as hypotheses. I could not check them against T03's text, which was not among my inputs.
- Statement deviations, all declared and justified: T13 (iv)(a) provenance condition (honest weakening); T22 C1 (S₀ ∈ Ω, necessary); T12 (iv.b)/(iv.e) component scope; T15 (iv) and T31 (c),(d) non-implication readings; T09 (iii),(v) existence readings; T20 and T23 readings of informal wording.

No fatal finding and no gap in any of the ten chapters. The only items I could not verify myself are the two interval-arithmetic certificates (T12's instance, which is referenced rather than printed; T13's, which is printed and which I spot-checked by hand to four or five digits) and the exact wording of T03.

## Summary of verdicts

| Theorem | Fatal | Gap | Exposition notes | Verdict |
|---|---|---|---|---|
| T09 | 0 | 0 | 2 (n ≥ 4 for the family; tight constant 55) | correct |
| T11(iii) | 0 | 0 | 1 (full execution is an idealisation, declared) | correct |
| T12 | 0 | 0 | 2 (numerical certificate only referenced; p = 2, N = 1 instance scoped) | correct |
| T13 | 0 | 0 | 2 (construction reading; blocks used only via size and partition) | correct |
| T14(i) | 0 | 0 | 0 | correct |
| T15 | 0 | 0 | 0 | correct |
| T20(i)–(ii) | 0 | 0 | 1 (H03 vs T03 not checkable here) | correct |
| T22(i)(ii)(iv) | 0 | 0 | 0 | correct |
| T23(ii) | 0 | 0 | 1 (ρ read as whole-round departure, declared) | correct |
| T31(i) | 0 | 0 | 0 | correct |
