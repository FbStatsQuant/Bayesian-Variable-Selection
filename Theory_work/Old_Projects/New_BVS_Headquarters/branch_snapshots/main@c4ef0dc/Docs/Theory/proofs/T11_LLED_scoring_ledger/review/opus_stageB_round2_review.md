# Round 2: rulings on the author's answers and review of PROOF_v4.tex

**Reviewer:** B (Opus). **Inputs read:** STATEMENT.md (updated), CLAIMS_OF_FATAL_FLAWS.md, PROOF_v4.tex, PROOF_v4.pdf (4 pages) and REPORT_FORMAT.md. I checked the v4 PDF against the .tex and they match. I ran nothing and wrote nothing.

## Part 1: Rulings on the logged claims

**A1-F1 (sampler definitions not in the setting): agree; the fix works.**
- Setting item 1 now gives everything Lemma 3 uses: w(k) > 0, W_K, ϖ, the product form of γ₀, and r_b > 0.
- From these I re-derived two facts. First, M = W_K Z̄₀, because Z̄₀ = W_K^{−1} Σ_{k≤K} w(k) c^{(J)}_k. Second, the path probability: the e_b factors cancel and the c-ratios telescope, giving π₀(S).
- The main claim still uses only item 3.

**A1-F2 (Remark 4's list of interruptions cannot be checked): agree; the fix works for the main argument.**
- PROOF_v4 takes full execution from item 5.
- Item 5 now says it outright: "A launched final run executes all these rounds (no early stop …)".
- Remark 4 no longer carries any weight in the proof. My remaining note on it is N4 below (exposition).

**A1-F3 (scoring premises missing): agree, as refined in round 2.**
- The §6.5 quote ("Every proposal is scored, accepted or not") supports the proposals-only corollary.
- The §6.12 premise was later withdrawn (see A1-R2-F2).

**A1-R2-F2 (initial draws not shown to be scored): agree; the fix works.**
- I cannot check the definition of d(·) used in that reviewer's one-block counterexample, because METHODOLOGY is not in the packet.
- The fix does not depend on it. The corollary now uses only the Q_p proposals, which the quoted §6.5 text requires to be scored. The exponent Q_f appears only under an explicitly stated condition (initial draws also scored).
- The set inclusion {S* not scored in the final run} ⊆ {S* not among the proposals} is valid.

**Round-2 exposition items (matrix parenthetical; "in general not"): handled.**
- PROOF_v4 Remark 4 (lines 125–135) has no matrix claim.
- Remark 7 (line 218) reads "in general not of the calibration streams".

**OB-F8 (my finding: Corollary 9's citation of Proposition 5): agree with the answer; the fix works.**
- Proposition 5 is now stated for any *designated* class of sampler calls: membership is decided by the run's state when the call starts, and the number of designated calls is a constant Q given υ.
- I checked three points:
  - {τ_m = t} ∈ 𝓕_t, where τ_m is the number of values read before the m-th designated call starts. The state after t reads is a function of V_1..V_t, and it decides whether a call starts next, whether that call is designated, and how many designated calls came before.
  - D_1..D_{m−1} are 𝓕_{τ_m}-measurable.
  - Lemma 2 plus the freezing argument gives P(A ∩ {D_m = s}) = P(A) π₀(s) for every A ∈ 𝓕_{τ_m}.
- So the designated outputs are iid π₀ in chronological order, whatever the positions of other calls.
- Part (b) applies this to the independence proposals. A call's status as a proposal is part of the state when it starts, so that class is designated. Corollary 9 now cites (b). This closes the gap.

**Handling of my exposition findings F1–F7 and my item-6 concern:**
- **F1:** adequate. The replacement constant is ½ ∈ (0,1), so the coupled realisation stays inside the support.
- **F2:** adequate. 𝓕_τ now requires A ∈ σ(V_1, V_2, …), and V_{τ+j} := ½ on {τ = ∞}.
- **F3:** adequate. Finiteness of τ_m now follows from two facts: the designated call does occur (the hypothesis, via item 5), and operations run one at a time (item 2). In a sequential run, a call that occurs is preceded by finitely many completed operations, and an operation that read infinitely many values would never complete.
- **F4:** adequate. The designated-call formulation covers it.
- **F5:** adequate. The proof now allows a state-dependent map G_{Z_m}, and item 3 is worded to match. One small measurability point remains; see N3.
- **F6:** adequate. The text now says "exactly one path of positive probability".
- **F7:** adequate for the proof, since item 5 is now explicit. One wording point in the remark remains; see N4.
- **Item 6:** resolved. STATEMENT.md now quotes the source file's own preamble: "Fix S* ∈ Ω measurable w.r.t. data and 𝓒 (before final randomness)". Item 6 is a faithful transcription. For a variable with finitely many values, "measurable w.r.t. data and 𝓒" and "a measurable function of data and 𝓒" are equivalent (Doob–Dynkin). I can check the quote only as it appears in the packet; the source file itself is not provided.

## Part 2: Review of PROOF_v4.tex against the updated STATEMENT.md

### What changed from v3, and what I checked

Compared with v3, the edits are:
- Lemma 1: replacement constant ½.
- Lemma 2: 𝓕_τ definition and the convention on {τ = ∞}.
- Lemma 3: "of positive probability".
- Remark 4: wording.
- Proposition 5: rewritten.
- Corollary 9: now cites Proposition 5(b).

Lemma 1, Lemma 3, Theorem 6, and Remarks 7–8 are otherwise unchanged, and my round-1 checks of them still apply.

**Lemma 1 with ½.** The coupling argument is unchanged and remains correct.

**Lemma 2.** Correct. On {τ = ∞} the convention makes (V_{τ+j}) measurable, and that event is null, so the decomposition over {τ = t} is unaffected.

**Proposition 5, lines 142–185.**
- *Reading scheme.* Unchanged from v3 and correct: with υ fixed, the run reads not-yet-read values of Ξ, the next index is a measurable function of the values read so far, and padding with stream 10 makes the sequence infinite.
- *Stopping time τ_m.* Correct, as described under OB-F8.
- *The map G_{Z_m}.* Correct.
  - Item 2 says operations do not overlap, so the m-th designated call reads exactly V_{τ_m+1}, V_{τ_m+2}, … in order.
  - The state Z_m is 𝓕_{τ_m}-measurable: on {τ_m = t} it is a function of V_1..V_t.
  - Item 3 gives G_z(iid Unif) ~ π₀ for every state z.
- *Fubini step (line 175).* Correct, given joint measurability (see N3).
  - (1_A, Z_m) is 𝓕_{τ_m}-measurable, and W = (V_{τ_m+j})_{j≥1} is independent of 𝓕_{τ_m} by Lemma 2.
  - So E[1_A 1{G_{Z_m}(W) = s}] = E[1_A ψ(Z_m)], with ψ(z) = P(G_z(W) = s) = π₀(s).
- *Induction over m.* Correct.
- *Parts (a) and (b).* Correct. Both classes are designated, and item 5 gives exactly Q_f and Q_p calls respectively, both constants given υ.

**Theorem 6, lines 189–210.** Unchanged apart from citing Proposition 5(a). The steps hold:
- h is jointly measurable (item 2).
- Υ and Ξ are independent (EX-S).
- Freezing gives E[h | Υ] = g(Υ).
- g(Υ) = 1_Λ (1 − π₀(S*))^{Q_f} is σ(𝓒)-measurable (items 4–6).
- The tower property applies because σ(𝓒) ⊆ σ(Υ).
- The bound uses 0 ≤ 1 − x ≤ e^{−x} on (0,1].

**Corollary 9.** Correct under the quoted §6.5 premise, as discussed under OB-F8.

### Do the clarified setting items change the claim?

No. The text of Claim (iii) (STATEMENT.md lines 52–54) is identical to the round-1 version.

- **Item 3** now states the structure Proposition 5 uses: a measurable map, possibly depending on the state, with exact law π₀ on iid uniform input. Lemma 3 shows the §6.3 sampler meets it, with a map that does not depend on the state. So the item asks no more than the method's own sampler delivers, and it is not a new hypothesis.
- **Item 5** now states "no early stop" explicitly and puts aborts imposed by the computing environment outside the model. v3 used this implicitly, so the claim's content is unchanged. It is now an openly declared idealisation. It cannot be folded into Λ, because such an abort could depend on the final run's randomness. So the theorem does not cover runs aborted by the environment, and the statement now says so. The phrase "as everywhere in this theory" cannot be checked from the packet.
- **Item 6** is a transcription of the file's preamble and changes nothing.
- **The "Statement changes" paragraph** now names "the method's own specification" as the source of item 5. This is accurate and consistent with my round-1 observation that item 5 is a method specification rather than one of EX-A, EX-S or CAL.

### Findings on PROOF_v4

**N1**
- **Location:** Lemma 2 proof, line 76 ("Taking A = Ω").
- **Severity:** exposition.
- **Claim:** Ω is used here for the sample space, but throughout the paper (line 22) Ω is the model space {S ⊆ [p] : |S| ≤ K}.
- **Evidence:** This clash was already in v3; I missed it in round 1. The intended meaning is clear and it has no effect on correctness.

**N2**
- **Location:** Section 2, line 82.
- **Severity:** exposition.
- **Claim:** The paraphrase of Setting item 3 ("reading fresh values, returns an exact π₀ draw") uses the old wording, not the reworded item 3 (measurable, possibly state-dependent map with exact law π₀ on iid input).
- **Evidence:** Compare STATEMENT.md lines 31–34. It is harmless: Proposition 5 cites the new form correctly at lines 170–171.

**N3**
- **Location:** Proposition 5, lines 168–175 (G_z and the Fubini step). Also Setting item 3.
- **Severity:** exposition.
- **Claim:** The Fubini/freezing step needs two things the proof does not state: (z, w) ↦ 1{G_z(w) = s} must be jointly measurable, and the states must form a measurable space. Item 3 only says the map is measurable in the read values for each state.
- **Evidence:** This can be closed from the setting.
  - Take the state to be the history, z = (t, v_1, …, v_t) in the disjoint union ⊔_t [0,1]^t.
  - On {τ_m = t}, D_m is a Borel function of (V_1..V_t, W), because the whole run is a Borel function of the values read (item 2: "All maps are Borel measurable").
  - That gives the required joint measurability, and Z_m is 𝓕_{τ_m}-measurable.
  - So the step holds, but this justification should be written out.

**N4**
- **Location:** Remark 4, lines 131–132 ("m(S) is a finite positive number for every S …, so scoring does not fail").
- **Severity:** exposition. The remark carries no weight in the proof.
- **Claim:** That m(S) is mathematically well defined does not by itself show that the §6.13 computation (Cholesky, then refactor, then augmented QR) returns it.
- **Evidence:** The inference needs EX-A to be read as "every score computation returns log m(S) exactly". That is a reasonable reading of "Scores … are exact". Item 5 now asserts "no early stop" directly, so the proof does not depend on the remark.

There are no fatal or gap findings on PROOF_v4.

### Setting: faithfulness and sufficiency (v4)

- **Sufficiency.** Items 1–6 suffice for the proof. The one implicit point it uses is the joint measurability in N3, which follows from item 2.
- **Item 6.** It is now confirmed against the quoted source preamble, so my round-1 concern is resolved.
- **Item 5.** It is explicit and openly identified as the method's specification plus an idealisation that excludes environment aborts.
- **Item 3.** It is the exact form used and is met by the §6.3 sampler (Lemma 3).
- **What I could not check.** The underlying source files (the theorem file, 00_COMMON, METHODOLOGY) are not in the packet. I can only confirm that the items agree with the passages quoted in the packet.
- **Hidden assumptions.** None beyond those already disclosed.

## Conclusion

All logged claims are resolved and the fixes work. In particular, my OB-F8 is closed by the designated-call form of Proposition 5 together with part (b). Handling of F1–F7 and of the item-6 concern is adequate. PROOF_v4 establishes Claim (iii) of the updated STATEMENT.md under Setting items 1–6. The four new findings (N1–N4) are exposition only.

**VERDICT: verified**
