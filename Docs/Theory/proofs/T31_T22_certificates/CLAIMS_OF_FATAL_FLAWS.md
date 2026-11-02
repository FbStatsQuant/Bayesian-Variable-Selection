# CLAIMS_OF_FATAL_FLAWS — T31 (T22) part (i)

## Fatal or gap findings

None. Three independent reviews of PROOF_v1 (Astra #1, Astra #2, Opus 5.5 xhigh) reported no fatal and no gap finding;
all three returned **verified**.

## Exposition findings and the lead's answers (for the record; Opus reviewer, Stage B round 1)

| # | Finding (short) | Answer | Change in v2 |
|---|---|---|---|
| 1 | Non-implication reading of (c)/(d) is the only true one: surely e^{−Δ}Z ≤ Ẑ ≤ e^{Δ}Z with Δ = max d − min d; statement should say so | Accepted (checked: ϖ·BF = γ₀e^{d}, stage factors in [e^{Δφ d_min}, e^{Δφ d_max}]) | STATEMENT §3 paragraph before (c) reworded; new final paragraph of the last Remark in the proof derives the bound |
| 2 | "Final flags" plural vs one witness flag | Accepted: existential reading | STATEMENT sentence after (d2); last Remark |
| 3 | Link P_c ↔ conditional law given 𝓒 not written out; CAL unused | Accepted | New Remark "P_c and conditioning on 𝓒" (substitution lemma; CAL used only there) |
| 4 | Fidelity to METHODOLOGY_v3 and T12 not checkable from the packet | Noted (scope of the packet). Lead checked: Ẑ_r formula = METHODOLOGY_v3 §6.12 verbatim; E2 = §6.9, "recomputed as flags only" after the final run; (H-T12) = T12(iii) first identity | None |
| 5 | Preamble could be read as asserting iid islands / islandwise unbiasedness of the actual run | Accepted | STATEMENT §3 preamble reworded; Remark on 𝓛(Z) extended |
| 6 | π₀ and "every move stays in Ω" not in the packet | Accepted | Lemma 1(iii) now cites STATEMENT §1 (states in Ω) only |
| 7 | Measurability via "outputs", N_e ≥ 1, T ≥ 1 | Accepted | Lemma 1(iii) reworded |
| 8 | Table entries with |A| > K | Accepted | Lemma 1(ii): only A = S ∩ C_b ∈ Ω enter |
| 9 | "On this event" ambiguous | Accepted | Theorem (d1) proof |
| 10 | e³ > 20 unjustified | Accepted | Theorem (d2) proof: e > 2.718 ⇒ e³ > 20.07 |
| 11 | "No upper limit on Z/Ẑ" informal | Accepted as informal remark; no change needed | None |

## Round 2 (PROOF_v2): rulings and new findings

Both Stage B reviewers returned **verified** on PROOF_v2, with no fatal or gap finding, and agreed with the answers to
rows 2–11. Row 1: both agree with the sure bound but disagree with the wording "the only true one" (accepted, see R2-1).
Full rulings: review/stageB_opus_r2.md, review/stageB_astra2_r2.log.

| # | Finding (short; source) | Answer | Change in v3 |
|---|---|---|---|
| R2-1 | "Only true reading" overclaims; only the per-data-set reading is refuted (Opus R2-1; Astra #2 finding 1) | Accepted | STATEMENT §3 and last Remark: "the intended one; the per-data-set reading would be false"; added "whether such laws are realised by the actual run for some data set is not addressed" |
| R2-2 | Small-Δ claims lack derivation and assume such data exist (Opus) | Accepted | Last Remark: SD ≤ Δ/2 (pop), ≤ Δ/√3 (sample) derived; stated conditionally ("if Δ ≤ √3", "if e^Δ ≤ 1/α"), no existence claim |
| R2-3 | Implicit steps in the sure bound; "method does not compute/report" unverifiable (Opus; Astra #2 finding 2) | Accepted | Steps written out (positive increments, averaging, γ₀-weighted average); "not among the reported quantities listed in STATEMENT.md" |
| R2-4 | Joint-measurability proviso missing in STATEMENT §1 (Opus) | Accepted | STATEMENT §1 P_c sentence now carries the proviso and says conclusions are stated for P_c |
| R2-5 | Proof cites "STATEMENT.md" while packet file is STATEMENT_v2.md (Opus) | No change: the project file is STATEMENT.md; packet copies are renamed only to keep versions apart | None |

## Round 3 (PROOF_v3): confirmation

Astra #2 and the Opus reviewer both returned **verified** on PROOF_v3, agreed with all Round 2 answers (R2-1..R2-5:
change works), and reported no fatal or gap finding. Opus added three exposition notes (R3-1: the (d) half of the
per-data remark is true for every data set by a one-line argument not on the page; R3-2: symbol A reused; R3-3:
wording of "reported quantities"). Lead's answer: all three accepted as correct and cosmetic; **not applied**, so that
the final text is exactly the reviewed PROOF_v3. They concern commentary only, not any conclusion.
