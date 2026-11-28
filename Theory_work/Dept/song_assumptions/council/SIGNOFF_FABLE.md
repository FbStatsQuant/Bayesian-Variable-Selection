# FABLE senior sign-off — TH-SONG-ASSUMPTIONS, v1.4 at 3ee24ea9

Fable 5.2, Final Council, 2026-11-28. Single sign-off pass.

**Verdict: SIGN-OFF WITH FIXES.** Scores: completeness **8.5**, generality and naturalness **9.0**, owner Q&A readiness **8.0** (Stage 1: 7.5 / 6.0 / 6.5). No blocker. The twelve fixes in §5 are one-line edits; none changes an assumption.

**What I did.**
- Read: both Stage 1 reports, the Lead proposal, both advisor replies, V14_CHANGESPEC and the whole V14_DIFF.
- Checked by hand: U1/U2a/U2b, ā and its reading aid, special cases (i)–(iii), m̄_d and the k > m̄_d dispatch, C-i, C-ii, W1–W3, the per-base step 3, A-BS′, the A-MIS primitive form, the converse remainder, and the AR(1) and equicorrelation closed forms.
- Ran: `.rc_tmp/lead_v14/u2a_check.py` (reproduced) and one inline population computation, no files written.
- Not done: a line-by-line derivation of TS-b steps 2–3, which are still unwritten proof obligations.
- Disclosure: I wrote my list before opening `SIGNOFF_ASTRA.md`. Fixes 1, 4, 5, 6, 7 and 11 coincide with Astra's edits 1, 2, 8, 3, 6 and 7.

## 1. Resolution of my Stage 1 findings
- **C-1** (population form, Lemma W): RESOLVED, subject to fix 1.
- **C-2** (S1 numbers inside statements): RESOLVED, subject to fix 12.
- **C-3** (proof constants and level M): RESOLVED. The rival range m̄_d is explicit and C is out of the headline. J remains only as a sieve restriction, which narrows the rival set; see fix 2.
- **C-4** (three SL counterparts): RESOLVED, all three, with the right caveats.
- **C-5** (A-SPARSE-C): RESOLVED.
- **C-6** (worked cases): RESOLVED. I re-derived the AR(1) and equicorrelation formulas.
- **C-7** (converse under its minimal set): RESOLVED in the package files. The spec overstates it; see fix 6.
- **C-8** (a.s. versions): not addressed. No action: "all D_n on a common probability space" already admits any coupling.
- Table rows:
  - A-DIM′, A-NEC, A-BS, A-BS′, A-MARGIN-U: RESOLVED.
  - A-MARGIN-H: RESOLVED. The advisors' "every fixed k" is right and my "s + m̄" was too small.
  - A-SUBG: PARTLY. The window k_n is adopted; the standard sufficient models are still not listed first. No action required.
  - A-MIS(iii): PARTLY. The primitive form is added; full rank stays the headline sufficient version. Acceptable.
- My P-U had two errors, both corrected in v1.4: the inverted price ratio, and a generic-prior price that the proof does not support.

## 2. Correctness of the new statements
Everything below was checked and is correct, except where a fix is named.
- **(U1), (U2a), (U2b).** Sound. (U1) is the case N = ∅ of (U2a). T∖S = T∖B because N ⊆ Q_n^c.
- **ā.** √ϑ ≤ ā ≤ √(2ϑ) holds, in fact on all of [0, 1].
- **Special case (ii).** Correct with common root-scale slack: the loss is √(1−ϑ) and ā·√(2 log C) ≤ 2√(mϑ log p) → 0.
- **m̄_d.** For k > m̄_d, (k/2)·log(n/log p) − Pr_n(d) ≥ log n − O(log log n). The cutoff is safe; k = m̄_d is itself already dispatched.
- **C-i, C-ii.** Both hold: R_n(S)/σ*² ≥ nφ²dθ_min², Pr_n(d) ≤ d·log(2p√(n+1)) and log C(p−s, m) ≤ m·log p. The orthogonal gloss is only sufficient (fix 4).
- **W1, W2.** Exact identity; ϑ̂ ≤ ϑ + 2δ/(1+δ); ā(ϑ̂) ≤ ā(ϑ) + 2√δ, since the slope of a² is at most 2 below the cap.
- **W3: a gap.** The display bounds the width by the uncapped chord ‖v_S − v_B‖ = a(ϑ̂), which reaches √2. (U2b) charges ā ≤ 1. For leakage above 3/4 the stated lemma does not deliver the stated coefficient (fix 1).
- **Per-base step 3.** Accounting is right: for fixed D each added set gives one S, so the containing-model odds are summed once.
- **A-MARGIN-H, windows, A-NEC, A-DIM′, A-BS′, sieve, TM-a0-inc.** Correct. E ≤ M_μ/c_ψ follows from A-NEC on T.
- **A-MIS(iii) primitive form.** Equivalent to v1.3. The conditional characteristic function gives it directly, including τ² = 0.
- **Converse.** The O_P(1) remainder suffices for "the rival beats T with probability → Φ(−c)". That gives a liminf bound on P(π(T|y) ≤ ½), not a limit (fix 6).

## 3. Generality
- No headline statement contains an AR(1), S1 or S2 element, or a simulation constant.
- A-MARGIN-U is stated on (Σ, β*) and the coded price only. C-i and C-ii give the standard genre.
- One residue: the withdrawn "≈ 121" sits inside the refined-form statement paragraph (fix 12).
- AR(1) in the A-SPARSE-C defence and in the worked cases is evidence or example, which is allowed.

## 4. Faithfulness
- None of "C ≈ 121 implied", "every m ≤ J active" or "margin holds there" survives.
- **S1 (U2a) check: confirmed.** The minimum equals κ_n in all cells. Over D containing x_10 with the proxy x_11 in the base, the minimum ratio at SNR 2 is 2.862–3.177, above κ_n. By the AR(1) Markov property the nearest proxy is the only one that matters, so the check is exhaustive over proxy sets, not only at ≤ 2 proxies.
- Contradictions and leftovers found: fixes 2, 3, 5, 6, 8, 9, 10.

## 5. Fixes (each a one-line edit)
1. **Lemma W (W3)**, in the spec §1, ASSUMPTIONS §2 and DOSSIER item 2: add "on the same event also −⟨v_S, g⟩ ≤ √(2[log C(p−s, m) + l_n]) (direct union bound), so the coefficient is min{1, a(ϑ̂)} = ā(ϑ̂)". In ASSUMPTIONS §3.3 step 3, replace "a(ϑ̂) ≤ ā(ϑ) + 2√δ_n" by "ā(ϑ̂) ≤ ā(ϑ) + 2√δ_n".
2. **TS-b statement**, DEFINITIONS §4.2 and the A-MARGIN-U statement in ASSUMPTIONS §2: restore "Fix an admissible level M independently of n; J := ⌊s + C_s M⌋ (prop:dist(i))". Both use J in the sieve, and the TS-b rate uses n^{−c_H M}, without defining either.
3. **Pervasive factors**, ASSUMPTIONS §6 item 2: replace "fail (U2a) for small Q_n" by "admit no small Q_n with vanishing outside leakage, so special case (ii) is unavailable". They do not fail (U2a). In DOSSIER worked case 4, "no small Q_n exists" becomes "no small Q_n with vanishing outside leakage exists".
4. **C-ii orthogonal gloss**, all copies: "reads" becomes "is implied by". Exact (U1) is n·Σ_{j∈D} β*_j²Var(x_j) ≥ 2(1+η)σ*²·Pr_n(|D|) for every nonempty D.
5. **S1 special case (ii)**, spec evidence, ASSUMPTIONS Defence (b), DOSSIER item 4 and SIMULATION: "L_n → ∞" becomes "L_n → ∞ with ρ^{2L_n}·log p → 0, for example L_n = ⌈√log n⌉". Divergence alone does not give ϑ·log p → 0.
6. **Converse**, spec §2 only: "P(π(T|y) ≤ ½) → Φ(−c)" becomes "P(this rival beats T) → Φ(−c), hence liminf P(π(T|y) ≤ ½) ≥ Φ(−c)", as the package files already say.
7. **TS-a fixed-level remark**, DEFINITIONS §4.2, ASSUMPTIONS §2 and DOSSIER: add "j ∉ S" to the infimum. Without it the infimum includes S ⊇ T and is zero.
8. **Upward-rounded minima.** Exact κ_n at SNR 2 is 2.50455 at (1000, 500), 2.61261 at (500, 500) and 2.77075 at (500, 5000): quote the truncated 2.504, 2.612 and 2.770, not 2.505, 2.613 and 2.771, in every copy. DOSSIER item 4: 2.4889, not 2.489.
9. **SIMULATION Lead synthesis, item 2**: "(mixed classes: E9)" becomes "(mixed classes: the U2a check and leakage decay below; E9 covers the refined form only)".
10. **DEFINITIONS §4.3**: move "For discrete y, f₀ is defined by expected Gaussian log score" back from TM-a0-inc to TM-a0. TM-a0-inc does not use f₀.
11. **A-DIM′**, DOSSIER and DEFINITIONS §4.1: drop the "i.e." and "headline form" that equate the product budget ≤ c·n with (log p)² = o(n). They are not equivalent.
12. **Generality**, ASSUMPTIONS §2 refined-form paragraph: move "the v1.3 claim C ≍ (s0+1)² ≈ 121 is withdrawn" to Defence (b) with E9b.

Optional, no action required: say in the (U2a) evidence that one nearest proxy is exhaustive on S1 (§4 above).

## 6. Scores

| criterion | score | reason |
|---|---|---|
| Completeness | 8.5 | Every Stage 1 gap is closed. What remains is stated openly: TS-b is a target, there is no necessity result for (U2b), and TD′ is a conjecture |
| Generality and naturalness | 9.0 | The central margin is now a population condition with one slack, an explicit rival range and standard-genre corollaries. (U2b) is more elaborate than a referee expects, and C-i and C-ii are the answer to that |
| Owner Q&A readiness | 8.0 | The dossier now answers "why this width" and "how do I construct Q_n". Fixes 1, 2 and 7 are the ones the owner could trip on; with them applied I would put this at 8.5 |
