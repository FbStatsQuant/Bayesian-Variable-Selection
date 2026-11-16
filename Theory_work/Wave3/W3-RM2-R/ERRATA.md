# W3-RM2-R — ERRATA (editorial findings; never block; applied later in one editorial batch, PROTOCOL_v4 §5.3)

| # | source | file:line | finding | planned fix |
|---|---|---|---|---|
| E1 | LC-A finding 1 (E) | `lemmas/Q1_sandF_c.md:171` | Remark 3 (inherited) says the text differs from its sources only in Step 2(b)'s last line and the toolkit; Step 2(a) [R-3] now also differs | add "and in Step 2(a) [R-3] (constant-level visibility)" to Remark 3 |
| E2 | R1 Opus E1 | `STATEMENT.md:80-81` | "two upper-bound predicates, which are treated as true" reads as if the rejection predicates fire | "the two bounds are treated as satisfied (the rejection predicates `le > 1e6`, `cap_ll > INT_MAX` never fire)" |
| E3 | R1 Opus E2 | `lemmas/Q5_dlv0.md:3` | status line says "re-check pending"; RC1 VERIFIED | update to "RC1 (Sol) VERIFIED" |
| E4 | R1 Opus E4 | `STATEMENT.md` (C-D); `lemmas/Q5_dlv0.md` §1 | DLV-0 uses Lemma E4 (to exclude the tie-DP throw) but does not name "the hypotheses of Lemma E4" | add "and the hypotheses of Lemma E4" to (C-D) and Q5 §1 |
| E5 | R1 Opus E5 | `lemmas/Q4_core_plus.md` (a′) | the identity St_n(𝓛′) = {S₀ ⊆ S̃₀} ∩ {[S₀, S̃₀] ⊆ 𝓛′} (STATEMENT:66-67) is not written out | add: "⊆: S̃₀ ∈ 𝓛′ ⊆ 𝓛 gives S₀ ⊆ S̃₀, and down-closure gives [S₀, S̃₀] ⊆ 𝓛′; ⊇: S̃₀ ∈ [S₀, S̃₀]" |
| E6 | R1 Opus E7 | `STATEMENT.md:135-142` (c⁺) | "for n with s₀ ≤ K" not restated | add "(for n with s₀ ≤ K, as in (b⁺))" |
| E7 | R1 Opus E9 | `STATEMENT.md` (C1⁺) vs `lemmas/Q6_assembly.md` §1 | (FL_b) vs (G3a) for the same block-relative floor | use one name, "(FL_b) = (G3a) + (FL-Q)" (checked: RM `STATEMENT.md:120` defines (FL_b) = GROW (G3a) + (FL-Q); PARENT `STATEMENT.md:169-170` imports it; R2 Opus caution answered) |
