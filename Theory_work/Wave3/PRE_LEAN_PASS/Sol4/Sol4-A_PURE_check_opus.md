PURE check of `Sol4/Sol4-A_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch under `.rc_tmp/`, deleted). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. **Patch applies and touches only line 216.** `git apply --check` passes. I applied the patch to a scratch copy under `.rc_tmp/` (now deleted). Only line 216 changes, and TRACK_B.md stays at 444 lines.
2. **Text around the edit is untouched.** The prefix `**Holds / fails.** ` is kept. Line 217 (` (W2-APP family map, …`) is byte-identical. The old line equals the prefix plus the card's "Old" text, character for character.
3. **New text matches the card.** It equals the card's "New" paragraph for Replacement A in FABLE_CARD.md exactly; I compared programmatically.
4. **The Lemma VIS labels exist and mean what the sentence says** (V1_VIS/STATEMENT.md):
   - (VIS-a), line 32: the sign route with aligned signs.
   - (VIS-b), lines 36-40: "B is closed" and δ = inf dist(ϑ_n, B) > 0, which matches "a fixed distance from the closed bad set B".
   - (VIS-d)(ii), line 52: stationary designs, explicitly naming "banded/MA(q)". These have countable 𝒩, so "banded designs in generic position" is a (VIS-b) case, as the sentence says.
5. **Small nit, not a defect.** Lemma VIS does not list "one truth per block" as a numbered case. It follows from (VIS-0), via Cov = θ*_j·Var(W_j | W_U), as FAMC B.V1 (line 136) and (BLK-1) show. So "under the sufficient conditions of Lemma VIS" is a slightly loose attribution for that case, but the statement is true.
6. **(AR-sep) quote matches** W3-FAMC/STATEMENT.md:72-74 up to notation: the patch writes Σ_{k≠j} where the source has Σ_{k∈S₀∖{j}}. These are equivalent because θ*_k = 0 off S₀, and the rest of the bound is the same.
7. **The study-layout claim is sourced.** That the study's AR(0.5) layouts satisfy (AR-sep) is stated in FAMC §1b(iii) (lines 98-100, citing C-GROW (C5)(c)).
8. **Arithmetic checks out.**
   - 0.5^31 = 4.66×10⁻¹⁰ < 10⁻⁹.
   - Adjacent truths, ρ = 0.5, θ = (1, −2): 1 + 0.5·(−2) = 0.
   - Gap 31, ρ = 2^{−1/31}: ρ^31 = 1/2, so 1 + ½·(−2) = 0 exactly. Both vectors lie on B.
9. **The pointer stays valid.** W3-FAMC/STATEMENT.md:93 cites "[TB] B8 `:216`" for the adjacent ρ = ½, θ = (1, −2) cancellation example. That example is still on line 216.
10. **The patch touches only TRACK_B.md**, a single-hunk diff.
11. **No registry claim span is involved.** `Theory_work/INFRA/registry/claims.tsv` (551 lines) has zero rows whose file column names TRACK_B.md, so nothing in lines 209-233 is a claim span. The patch header and the card both say re-freezes are needed (track V CORRECTION-ONLY, FAMC CITATION-ONLY), and the recorder handles them.
12. **No tracked files were modified, and nothing was committed.**
