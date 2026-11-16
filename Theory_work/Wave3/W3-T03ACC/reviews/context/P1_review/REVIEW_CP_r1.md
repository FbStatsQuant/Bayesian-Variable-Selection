# Review CP round 1 (Opus 5.5 xhigh, Claude Personal, Agent tool, Plan type) — findings and verdict, copied from the reviewer's reply

Scope stated by the reviewer: read only STATEMENT.md, REPORT_FORMAT.md, PROOF_v1.tex (all 477 lines), PROOF_v1.pdf (pp. 1–12); ran no commands. Record of hand checks covered §§1–2 preliminaries, T01(i)–(iv), (T)(a), (T)(b1), (T)(b2), T02(i), T02(ii), each marked "Verified".

## Findings

1. **Location:** §1, display (1) (tex line 45). **Severity:** exposition. **Claim:** A line break is typed as `\` instead of `\\`, so the gathered display renders on one line. **Evidence:** PDF p. 1, equation (1). The content is correct.

2. **Location:** §8 preamble (tex line 391): "|S_0∪J| ≤ m_n ≤ min(p, m_n+s_0)". **Severity:** exposition. **Claim:** The step `m_n ≤ p` is false in general. **Evidence:** With p fixed and n large, `m_n ≥ (log n)/(2 log 2) > p`. The conclusion still holds through the correct chain `|S_0∪J| ≤ min(p, m_n) ≤ min(p, m_n + s_0)`, because `S_0∪J ⊆ [p]`. The SE application is unaffected.

3. **Location:** Theorem 6.1 (statement and last line of the proof). **Severity:** exposition. **Claim:** The proof's theorem restricts `E_n` to deterministic events, which STATEMENT (T)(a) does not require. The O_P consequence is also left implicit. **Evidence:** The inequality `P(Π(E_n|y) > κ²x) ≤ P(𝓑_n^c) + P(I_{b₋}(E_n)/Z^c_{b₊} > x)` holds pointwise on the sample space for any measurable, possibly data-dependent `E_n`. Taking `x = ε_n`, resp. `x = Lε_n`, gives both consequences. No step of the argument changes.

4. **Location:** Lemma 7.2 (`γ_n`, `C_Ω`) with `s_0 = 0`. **Severity:** exposition. **Claim:** `C_Ω` and `γ_n` contain `φ_0`, which is void under R when `s_0 = 0`. **Evidence:** `R_n = 0` in that case, so any `φ_0 > 0`, or dropping the term, works. This matches the lemma's own parenthetical.

5. **Location:** Lemma 2.3(d) and the opening paragraph's list of elementary facts. **Severity:** exposition. **Claim:** The proof uses that matrix inversion is order-reversing (`0 ≺ B_1 ⪯ B_2 ⇒ B_2^{-1} ⪯ B_1^{-1}`), but this fact is not in its list. **Evidence:** checked by hand: `B_2^{-1/2} B_1 B_2^{-1/2} ⪯ I` implies `B_2^{1/2} B_1^{-1} B_2^{1/2} ⪰ I`, which implies `B_1^{-1} ⪰ B_2^{-1}`.

6. **Location:** Remark 7.4 ("fails for the data-dependent rate … no longer a density in y_c") and Remark 6.4 ("logarithmically slow"). **Severity:** exposition. **Claim:** These side assertions are not proved. **Evidence:** Neither is used by any theorem; marked unverified. Remark 8.5 ("nonincreasing in the IG rate") does follow from T01(iv) and L2.3(d).

7. **Location:** Lemma 8.2, the claim "n_0 depending only on s_0, A, φ_0, σ*², M". **Severity:** exposition. **Claim:** The condition `s_0 ≤ K` is attributed to R. **Evidence:** It holds automatically for `n ≥ 2s_0 + 1`, since `S_0 ⊆ [p]` gives `s_0 ≤ p`. `δ_n ≤ ½` is controlled through (5) by `(s_0, A)` alone, so the claim is correct.

8. **Location:** Throughout. **Severity:** exposition. **Claim:** Several symbols are overloaded (`M` smoother vs constant; `A` matrix vs exponent vs `A_n`; `β`, `B_n` next to `𝓑_n` in Theorem 6.3; `θ_n`, `ϵ_n` in L8.3; `Ω_n` vs `Ω`). None of these causes an error.

Observation (no finding): Theorem 7.3 proves the consequence of T02(i) for every deterministic `ω_n`, which is stronger than the statement and valid. The proof never treats `ε` or `ε_c` as Gaussian conditionally on `s_y` or on `𝓑_n`.

**Verdict: verified**
