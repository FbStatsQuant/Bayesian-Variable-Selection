PURE check (v2: two edits, line 87 and the manager-added "and n ≥ 4" at line 164) of `T8/T8-3_correction.patch` (fresh Opus subagent, claudeAgent_personal, high). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. `git apply --check` passes from the repo root. On a scratch copy (`patch -p1`, removed afterwards) only lines 87 and 164 change, and the file stays at 183 lines. No tracked file was touched.
2. Line 87, character by character: "again √(2/π)z_n ≤ F-bound below" becomes "J_{z_n}(0, τ_U) ≤ √(2/π)z_n (since τ_U ≥ σ), within the bound below". This matches the T8-3 replacement text in `FABLE_CARD.md:13` column (c) exactly.
3. Line 164, character by character: the only change is " and n ≥ 4" inserted between "s₀ < K" and ", by (T0)". Nothing else moves.
4. The edit is true. (T0) in W3-START `STATEMENT.md:241` reads "For every valid data set (n ≥ 4, EX-A)", and `L1_AGG_FLOOR.md` L1.0 (line 8) says "Valid inputs, n ≥ 4, EX-A".
5. The second display does not use n ≥ 4 itself; it inherits it from the hypothesis. o₀ ≥ T₁ ≥ f_n(s₀) ≥ ½(n+1)^{−1/2} (L1 (iv)–(v)) needs only k < p. n ≥ 4 is used only in the ⅓ step of the first display (f ≤ ½·5^{−1/2}, line 133). Stating the qualifier is faithful either way.
6. The optimality remark still holds asymptotically. With s₀ fixed and p > s₀, K = min(p, ⌊n/2⌋) > s₀ once n ≥ 2s₀ + 2, and n ≥ 4 holds for all large n. This matches (T0)'s own "true for all large n when p > s₀".
7. The wording matches T8-2. Once T8-2 is applied, W3-START2-R `STATEMENT.md:237` reads "o₀ ≥ ½(n + 1)^{−1/2} on every data set with s₀ < K and n ≥ 4"; before it, the line reads "on every data set". The qualifier is word-for-word the same.
8. Registry: `grep R3_RATE.md Theory_work/INFRA/registry/claims.tsv` returns 0 matches, so the file lies in no claim span.
9. Manifest (report only): `R3_RATE.md` is an entry of `Theory_work/Wave3/W3-START2-R/reviews/MANIFEST_R2r.txt` line 20 (sha 43dadcf5…), so the START2-R re-freeze will need to update it.
