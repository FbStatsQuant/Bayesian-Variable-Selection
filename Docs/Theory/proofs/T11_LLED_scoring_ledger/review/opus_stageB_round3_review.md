# Round 3: final confirmation for PROOF_v5.tex

**Inputs read:** PROOF_v5.tex, PROOF_v5.pdf (4 pages, matches the .tex), the final section of CLAIMS_OF_FATAL_FLAWS.md, and STATEMENT.md Setting items 2–6 and the Claim. Those STATEMENT.md lines are unchanged since round 2. I compared v5 with v4 by reading the two .tex files side by side, not with a mechanical diff, because I was told to run nothing. I ran nothing and wrote nothing.

## (a) Does v5 differ from v4 only at N1–N4?

Yes. Apart from the title ("version 5", line 15), the only changes are these four:

| Item | v5 location | Change |
|---|---|---|
| N1 | Lemma 2 proof, line 76 | "Taking A = Ω" became "Taking A to be the whole sample space". This removes the clash with the model space Ω. |
| N2 | Section 2, lines 82–84 | The paraphrase of item 3 now matches the reworded item 3: a measurable map, possibly depending on the state, with exact law π₀ on iid uniform input. |
| N3 | Proposition 5 proof, lines 169–174 | New "Measurability:" paragraph. It replaces v4's parenthetical "(an 𝓕_{τ_m}-measurable variable)", which it supersedes. |
| N4 | Remark 4, lines 132–133 | Now says which reading of EX-A it uses: "every score computation returns log m(S) exactly". |

Everything else matches v4 word for word: Lemma 1, the rest of Lemma 2, Lemma 3, the paragraph defining Υ and Ξ, the statement of Proposition 5, the rest of its proof including parts (a) and (b), Theorem 6, Remarks 7–8, and Corollary 9. This agrees with the ledger's summary (lines 152–156).

## (b) Is the new measurability paragraph (N3) correct?

Yes. I checked each step.

1. **The state is the history.** Take z = (t, v_1, …, v_t) in the disjoint union ⊔_{t≥0} [0,1]^t, where t = 0 is the empty history. Item 2 makes the run a Borel function of the values it reads. So any other notion of "the run's state when the call starts", including whatever item 3 has in mind, is a Borel function of the history. The clause "any coarser state is a measurable function of it" is justified.
2. **Z_m = (τ_m, V_1, …, V_{τ_m}) is 𝓕_{τ_m}-measurable.** For a Borel set B with pieces B_t = B ∩ [0,1]^t, {Z_m ∈ B} ∩ {τ_m = t} = {(V_1..V_t) ∈ B_t} ∩ {τ_m = t}, which is in 𝓕_t. The set {Z_m ∈ B} is also in σ(V_1, V_2, …), as v4's definition of 𝓕_τ requires.
3. **Joint measurability on each piece.** Concatenation [0,1]^t × [0,1]^ℕ → [0,1]^ℕ is a homeomorphism. On the piece t, (v, w) ↦ G_{(t,v)}(w) is the output of the sampler call that starts after read t, computed from the concatenated read sequence (v, w). That is a Borel function by item 2.
4. **Joint measurability on the whole space.** The disjoint union is countable, so (⊔_t [0,1]^t) × [0,1]^ℕ, with the product σ-field, is the disjoint union of the pieces [0,1]^t × [0,1]^ℕ. A map that is measurable on every piece is therefore measurable on the whole space.
5. **Consistency with D_m.** On {τ_m = t}, G_{Z_m}(W) = G_{(t, V_1..V_t)}(V_{t+1}, V_{t+2}, …) = D_m.
6. **The freezing (Fubini) step.** It now has everything it needs:
   - (1_A, Z_m) is 𝓕_{τ_m}-measurable, and W is independent of 𝓕_{τ_m} (Lemma 2).
   - (a, z, w) ↦ a·1{G_z(w) = s} is jointly measurable.
   - So P(A ∩ {D_m = s}) = E[1_A ψ(Z_m)] with ψ(z) = P(G_z(W) = s) = π₀(s).

   This closes my round-2 N3.

## (c) Does anything new break the proof?

No. Proposition 5, Theorem 6 and Corollary 9 have the same logical structure as in v4, which I verified in round 2.
- **N1 and N2** change wording only.
- **N4** sits in Remark 4, which the proof does not rely on: it uses item 5 directly. The stated reading of EX-A ("every score computation returns log m(S) exactly") is a reasonable reading of item 3's "Scores … are exact". Grammatically, "m(S) is a finite positive number" belongs to item 1, not to EX-A, and the remark cites item 1 for it, so it reads correctly.
- **N3** adds justification only.

## Findings

**E1**
- **Location:** Proposition 5 proof, line 176 ("G_z applied to an iid Unif sequence has law π₀ for every z"). This interacts with the new paragraph at lines 170–174.
- **Severity:** exposition.
- **Claim:** The state space is now every history in ⊔_t [0,1]^t. But the run only defines G_z at histories where a sampler call starts right after read t. By item 2, the set H_t of such histories is a Borel subset of [0,1]^t. Elsewhere G_z is undefined, so "for every z" says slightly more than is meant.
- **Evidence:** This is harmless. The Fubini step evaluates ψ only at Z_m, and Z_m always lies in ⊔_t H_t, where item 3 applies. Alternatively, G_z could be extended off ⊔_t H_t by the §6.3 sampler (Lemma 3). That sampler does not depend on the state and is Borel, so the extension keeps both joint measurability and the law π₀. The proof's correctness is not affected and no change is required.

There are no fatal or gap findings. N1–N4 are applied correctly, and the only change outside those places is the version number in the title.

**VERDICT: verified**
