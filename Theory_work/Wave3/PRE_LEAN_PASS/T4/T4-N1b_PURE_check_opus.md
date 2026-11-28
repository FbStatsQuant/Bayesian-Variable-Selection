PURE check of `T4/T4-N1b_correction.patch` (the T4-N1 phrase fix applied at READER_VERSIONS.md:824 and :885; fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/n1b_*`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE
1. Mechanics: `git apply --check` passes for N1b, and for N1 on its own. I ran `patch -p1` on a scratch copy (.rc_tmp/n1b_2774892/). `diff` shows only lines 824c824 and 885c885, and in each only the beta-min phrase changes. The rest of each line, including the [RM2R-4] tag and the B7.2′ table cells, is untouched. The file stays at 1458 lines.
2. Combined: N1 and N1b applied to the same scratch copy give no conflict. Exactly lines 109, 121-122, 824 and 885 change, and the file stays at 1458 lines.
3. LaTeX: the new string `$\theta^*_{\min}\ge\sigma_*\sqrt{M_n\log n/n}/\varphi_0$ for a fixed sequence $M_n\to\infty$` is identical character for character to T4-N1's line 109.
4. (i) φ₀ is in scope. Theorem 7's (A2) (:825) sets λ_min(R̂_T) ≥ φ₀², and (A1) already lists φ₀ among the constants at :824. σ_* > 0 is fixed by (S1) (:28). Both are therefore fixed and positive at :824 and :885.
5. (ii) The rewrite is exact. W3-POST/STATEMENT.md:74 states BM-∞ as θ*²_min nφ₀²/(σ*² log n) → ∞. K_BC_check_sol.md:154 states it as a deterministic envelope, θ²_min ≥ M_nσ*² log n/(nφ₀²). The new form is that envelope with the square root taken.
6. The new form and the old limit are equivalent in both directions. Given the limit, take M_n := θ*²_min nφ₀²/(σ*² log n), which is deterministic on a fixed design and tends to ∞. Given some M_n → ∞, the inequality forces θ*_min√(n/log n) ≥ σ_*√M_n/φ₀ → ∞. So "fixed sequence" versus "any sequence tending to ∞" changes nothing.
7. (iii) The master's (BM-W⁺) paragraph (W3-RM2-R/STATEMENT.md:107-112) is unchanged in meaning. The patch replaces the qualifier at :885 with an equivalent condition, so B7.2′ is neither weakened nor strengthened.
8. Not caused by the patch, but the qualifier is the reader's own, not the master's. The master states (BM-W) ⇒ (BM-W⁺) with no beta-min condition (:109). Its last sentence (:111-112) says that if d_n² ≤ D log n, then λ_n ≥ max{c_TL, 8(1+√(D/2))²}·log n is enough for large n, "a BM(c) condition". The patch changes neither of these sentences.
9. (4) Other instances of the limit phrase in READER_VERSIONS.md are only :109 and :122, both covered by T4-N1.
10. :676 contains "ϖ_n√(n/log n) → 0", a different condition (no leak outside Q) that is correctly left alone.
11. CLAIMS_CARD.md has no instance. helpers/GATES_G2.md:133 is untouched, as ruled.
12. (5) Neither :824 nor :885 lies in a registry premises span. They are outside every W3-READER:R1 span, the nearest being 661-811 and 1283-1388, and outside R3's 32-60.
13. Hygiene: no tracked file changed, so `git status` still shows only the untracked N1b patch. Scratch work is only in .rc_tmp/n1b_2774892/. Nothing was committed.
