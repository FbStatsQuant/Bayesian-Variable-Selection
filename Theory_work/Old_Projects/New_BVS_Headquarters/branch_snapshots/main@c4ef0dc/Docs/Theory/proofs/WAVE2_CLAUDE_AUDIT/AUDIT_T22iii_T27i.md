# Independent Claude audit: T22(iii) and T27(i)

Auditor: Claude Opus 5.5 (one agent, no sub-agents). Date: 2026-10-22. Local machine; files were only read, except one single-seed numerical sanity check (§4).

Files audited (SHA-256):
- `T22iii_T16_start_aggregation/STATEMENT.md` 30c4580b…7e; `proof/PROOF_v1.tex` 36d2f98a…19
- `T27i_T20C_cancellation_budget/STATEMENT.md` da6d6e8a…95; `proof/PROOF_v2.tex` 8069934f…9c

Also read: `theorems/T22_…md`, `theorems/T27_…md`, `theorems/00_COMMON.md`, the DP2 decisions snapshot (D1), METHODOLOGY_v3 §§4–6 (formulas only), the T22 chapter of `COLLECTED_PROOFS_v2.tex` (statement and proof of (i), (ii)). `FAILED_ATTEMPTS.md` lists no approach relevant to these audits. Both LaTeX logs show 0 errors and no undefined references (T22: 7 pp.; T27: 5 pp.); I did not recompile.

Order of work: Step 1 (blind) was finished before I opened either `CLAIMS_OF_FATAL_FLAWS.md` or `WAVE2_REVIEW/REVIEW.md`.

## Verdicts

| Theorem | Verdict | Required edits |
|---|---|---|
| T22(iii) | **Correct** (one optional exposition fix, E-T22-1) | none required |
| T27(i) | **Correct** (one optional exposition fix, E-T27-1) | none required |

No fatal finding and no gap in either proof. Both statements faithfully express the original parts, given the approved DP2 change.

---

## 1. T22(iii): what is proved, in plain words

Setting: the start law π₀ is built from block tables r_b. The theorem says that, under the assumptions, the start puts almost all its mass on the true model S₀: 1 − π₀(S₀) = O_P(2^B √(log n) n^{−κ}).

The proof has three parts:
1. **Noise variables are cheap to leave out** (u_n is small). For a variable l that is not in the truth, the table gain from adding l is about n^{−1/2} × exp{(signal leak + noise)²/(2v)}. On average over l, this is at most of order n^{−κ}√(log n). This uses a Gaussian integral and Markov's inequality, not independence.
2. **Leaving out a true variable is very expensive** (e_n is super-polynomially small). VIS says every missing true variable explains a lot of signal; the score then rewards adding it by a factor like n^{M_n} with M_n → ∞.
3. **Plug into wave-1 T22(i)**, which turns small u_n and e_n into 1 − π₀(S₀) ≤ 2(s₀+1)u_n + s₀e_n.

### 1.1 Statement fidelity

| Original part (iii) | STATEMENT.md | Check |
|---|---|---|
| Assumptions G, R, within-block SE, VIS, NL_avg(κ), EXP | G, R, within-block SE, VIS, NL_avg(κ), **EXP′**, plus **NL_η** | EXP→EXP′ and the added NL_η are exactly DP2 D1 ("T22(iii) under EXP′ (D1) and NL_η"). Not under review. |
| q_n ≤ u_n = O_P(2^B√(log n) n^{−κ}) with O_P(1) remainder; exponent form with o_P(log n) remainder | items 1 and the weaker variant | Same. |
| "EXP's visibility lower bound" + M_n^V→∞ + B ≤ 16 ⇒ e_n = o_P(n^{−m}) | item 2; the visibility lower bound is now *proved* from EXP′ + VIS | Same conclusion; one fewer assumption (the old EXP bundled a lower gain bound). |
| 1 − π₀(S₀) = O_P(a_n + e_n) | item 3, plus sharper O_P(a_n) | Same, slightly stronger. |
| Exact zero leakage ⇒ κ = ½; NL_η supplies κ | §2 rate parameter | Same; explicit formula κ ≤ ½ − η/2 − √(2η(A+ε₀)). |
| Definitions q_n, u_n, e_n (00_COMMON AGG with S° = S₀), w(k), m(S), B, blocks | §§1, 3 | Checked against 00_COMMON and METHODOLOGY_v3 lines 103–106, 164–168: identical. |

Fidelity: **faithful**. One scope note for Felipe (not a flaw): adding NL_η narrows the regime compared with the original, because the old EXP was an upper bound that needed no max-leakage control. Under EXP′ some control of the largest leakage is genuinely needed (the log form −ν log(1−x) is *larger* than the quadratic, so the quadratic cannot be used as an upper bound without x being small). This is a consequence of the approved decision.

### 1.2 Step-by-step check (my own algebra)

**Lemma 1 (residuals).** With r_T = (I−P_T)μ, Y = μ + Cε, and P_T C = P_T (columns centered):
(I−P_T)Y = r_T + (C−P_T)ε, ‖(C−P_T)ε‖² = ‖Cε‖² − ‖P_Tε‖², cross term 2r_Tᵀ(C−P_T)ε = 2r_Tᵀε (r_T is centered and orthogonal to span X_T). With ‖r_T‖² = (n−1)Δ_T:
RSS_T − (n−1)v_T = 2r_Tᵀε + {‖Cε‖² − (n−1)σ²} − ‖P_Tε‖². ✔ (matches eq. decompose)
- Var(2r_Tᵀε) ≤ 4σ²‖μ‖² ≤ 4σ²Mn; union over ≤ p2^B ≤ 2^16 n^A sets ⇒ O_P(√(n log n)). ✔
- E exp{χ²_d/4} = (1 − ½)^{−d/2} = 2^{d/2} ≤ 2^8 (d ≤ 16). Markov + union: 2^8·2^16·n^A·n^{−L/4} = 2^24 n^{A−L/4}. ✔
- Count: Σ_b 2^{|C_b|} ≤ Σ_b |C_b|2^B = p2^B. ✔
- ν/RSS_T − 1/(2v_T) = [(n−1)v_T − RSS_T + 1.02 v_T]/(2v_T RSS_T) = O_P(√(n log n))/Θ(n) = O_P(√(log n/n)). ✔

**Lemma 2 (quadratic form on the leakage family).** u_{T,l} is a deterministic unit vector in the centered space, so Z_{T,l} ~ N(0,1) exactly and u_{T,l}ᵀY = δ + σZ. ✔
P(max|Z| > h_n) ≤ 2·p2^B·n^{−(A+ε₀)} ≤ 2^17 n^{−ε₀}. ✔
On that event (δ+σZ)² ≤ σ²(√η + √(2(A+ε₀)))² log n, so x = O_P(log n/n). ✔
0 ≤ −log(1−x) − x = ∫₀ˣ t/(1−t)dt ≤ x²/(2(1−x)) ⇒ ν·error = O_P((log n)²/n). ✔
νx − (δ+σZ)²/(2v) = (δ+σZ)²(ν/RSS − 1/(2v)) = O(log n)·O_P(√(log n/n)) = o_P(1). ✔

**Lemma 3 (truncated Gaussian integral).** Exponent after including the density:
(δ+σz)²/(2v) − z²/2 = δ²/(2v) + δσz/v − (Δ/(2v))z² (using v − σ² = Δ). ✔
Completing the square: = δ²/(2Δ) − (Δ/(2v))(z − δσ/Δ)², since δ²/(2v) + δ²σ²/(2vΔ) = δ²(Δ+σ²)/(2vΔ) = δ²/(2Δ). ✔
Integrate a uniform bound over [−h, h] with the factor (2π)^{−1/2}: 2h/√(2π)·exp(min{…}). ✔ The case Δ = 0 ⇒ δ = 0 is correct (μ in span X_T ⇒ u ⊥ μ).

**Proposition 1 (u_n).** E V_n ≤ (2h_n/√(2π))·2^B·n^{½−κ} (≤ 2^{B−1} sets T per l; average-of-max condition). ✔ E W_n ≤ 2√(2(A+ε₀))/√(2π), so W_n = O_P(1). ✔
On {max|Z| ≤ h_n}: each ratio ≤ (n+1)^{−½} e^{ρ_n+d_n} exp{(δ+σZ)²/(2v)}, max ≤ sum, so u_n ≤ (n+1)^{−½}e^{ρ_n+d_n}V_n ≤ a_n e^{ρ_n+d_n}W_n. ✔ Note d_n is defined as a maximum of absolute deviations, so the inequality holds wherever x < 1; no extra event needed.
Weaker variant: ξ_n = (ρ_n + d_n + log max(1,W_n))/log n ≥ 0 and = o_P(1). ✔

**Proposition 2 (e_n).** P = P_V − P_U has rank a ≤ 16 (within-block SE gives full column rank of X_V). PY = Pμ + Pε. ✔ VIS: ‖Pμ‖² ≥ M_n^V v_U log n ≥ M_n^V σ² log n, while max‖Pε‖ = O_P(√log n), so ‖PY‖² ≥ ‖Pμ‖²/4 for all pairs simultaneously w.p.→1. ✔
Telescoping EXP′ along U = T₀ ⊂ … ⊂ T_a = V: Σ[−ν log(1 − x_i)] = ν log(RSS_U/RSS_V) exactly. ✔
−log t ≥ 1 − t with t = RSS_V/RSS_U: ν log(RSS_U/RSS_V) ≥ (n/2)(g/4)/(C_R n) = g/(8C_R) ≥ (σ²/(8C_R)) M_n^V log n. ✔
Hence {r_b(U)/r_b(V)}^{1/a} ≤ exp{½log(n+1) + ρ_n − (c/16)M_n^V log n} (using a ≤ 16). ✔
log(n^m e_n)/log n ≤ m + A + ½ − (c/16)M_n^V + o_P(1) → −∞. ✔ C_R = 2M + 2σ² + 1 works deterministically.

**Section 5 (κ from NL_η).** E ≤ δ²/(2v) + |δ|σh_n/v ≤ (η/2)log n + √(η)·√(2(A+ε₀))·log n. ✔
½ − η/2 − √(2Aη) > 0 ⇔ t² + 2√(2A)t < 1 (t = √η) ⇔ (t + √(2A))² < 2A+1 ⇔ t < √(2A+1) − √(2A). ✔

**Section 6 (finish).** On {u_n ≤ ½}: (s₀+1)u/(1−u) ≤ 2(s₀+1)u. Ratio to a_n + e_n ≤ 2(s₀+1)u_n/a_n + s₀ = O_P(1). e_n/a_n ≤ n^m e_n → 0 for m > κ (2^B√(log n) ≥ 1 for n ≥ 3). ✔ Weaker form: ζ_n = ξ_n + log(2(s₀+1))/log n. ✔

### 1.3 Wave-1 citation check

The proof uses T22(i-a) and (i-b) with reference S° = S₀. In `COLLECTED_PROOFS_v2.tex` (T22 chapter, statement lines ~3640–3662; proofs ~3778–3840): same a_bj, D_b, q, u, e (with the 2p factor), reference must be in Ω, tables positive, and the bound 1 − π₀(S°) ≤ (s+1)q/(1−q) + s·e with q replaced by u when u < 1. I re-read the wave-1 proofs of the completed-sum lemma, the charging lemma, (i-a) and (i-b); they are correct. **Citation matches.**

### 1.4 Findings (T22(iii))

- **E-T22-1.** Location: proof §6, paragraph introducing eq. (aggregation). Severity: **exposition**. Claim: the wave-1 statement is for partitions with |C_b| ≤ B ≤ K; the proof does not say why this holds here. Evidence: B = min(⌊√n⌋, ⌊√p⌋, 16) ≤ K = min(p, ⌊n/2⌋) because ⌊√n⌋ ≤ ⌊n/2⌋ for n ≥ 3 and ⌊√p⌋ ≤ p. (Parts (i-a,b) in fact use only a partition and positive tables, so nothing breaks.) Suggested wording, after "with the cap included;": *"the actual blocks satisfy |C_b| ≤ B ≤ K, since ⌊√n⌋ ≤ ⌊n/2⌋ for n ≥ 3 and ⌊√p⌋ ≤ p, so the wave-1 hypotheses hold verbatim."*
- **N-T22-2 (note, no edit).** Hypotheses that are listed but not used: λ_min(R_{S₀}) ≥ φ₀² from R (only within-block SE is used). Harmless.

No fatal finding, no gap.

---

## 2. T27(i): what is proved, in plain words

The theorem is an identity plus bookkeeping. Walk from a smaller model S^(0) to the truth S₀ by adding c variables one at a time. Each step multiplies the start mass by (prior ratio) × (table ratio). The prior ratio is about 1/p, and H2 *assumes* the table ratio is about n^{−½}. H3 *assumes* the start of the walk has mass at least c₀. Multiply: π₀(S₀) ≈ p^{−c} n^{−c/2}. All the statistical content lives in the two assumptions H2 and H3; the proof itself is short and elementary.

### 2.1 Statement fidelity

| Original part (i) | STATEMENT.md | Check |
|---|---|---|
| Completion chain of feasible successive additions, fixed c and starting size | H1 (c ≥ 1, fixed s, feasible states, data-measurable chain allowed) | Same; data-selected chains must satisfy H2 themselves (correct qualification). |
| Ratio r_{b_i}(S^(i+1)∩C_{b_i})/r_{b_i}(S^(i)∩C_{b_i}) = n^{−½}e^{O_P(1)} jointly | H2: max_i |log ratio + ½ log n| = O_P(1) | Same (note (S^(i)∪l_i)∩C_{b_i} = T_i ∪ l_i). |
| π₀(S^(0)) ≥ c₀ > 0 w.p.→1 | H3 | Same. |
| EX-A, EX-S, CAL, successful final execution; p ≍ n^a | H4 and Definitions | Same; correctly noted as unused by the algebra. |
| π₀(S₀) = p^{−c} n^{−c/2} e^{O_P(1)} | Exact conclusion | Same; unconditional P₀ is the natural reading since π₀ is a function of data only. |
| (not in original) | empty-chain extension, optional EXP′ discussion | Additions, harmless and correct. |

Fidelity: **faithful**.

### 2.2 Step-by-step check (my own algebra)

- **Positivity.** Eigenvalues of nX_U H_U^{−1} X_Uᵀ are nλ/((n+1)λ+1) < n/(n+1), so Q_U ≥ yᵀy/(n+1) = (n−1)/(n+1) > 0. ✔ (Matches METHODOLOGY line 114.)
- **Prior ratio.** w(k+1)/w(k) = C(2p−1,k)/C(2p−1,k+1) = (k+1)/(2p−1−k). ✔ And 2p − k − 1 = p(2 − (k+1)/p). ✔
- **Exact identity.** π₀(S₀) = π₀(S^(0)) · Π_{i<c}[(s+i+1)/(p(2 − (s+i+1)/p))] · Π_i r-ratio_i = π₀(S^(0)) p^{−c} n^{−c/2} A_{p,s,c} e^{ΣE_{n,i}}. ✔ Normalisers cancel because all states are in Ω.
- **A bounds.** s+i+1 ≤ s+c ≤ K ≤ p, so each denominator is in [1, 2); each factor is in ((s+i+1)/2, s+i+1]; product of (s+i+1) = (s+c)!/s!. Hence (s+c)!/(2^c s!) ≤ A ≤ (s+c)!/s!. ✔
- **Tightness.** For M > −log c₀: {|log π₀(S^(0))| > M} ⊆ {π₀(S^(0)) < c₀} (since log π₀ ≤ 0). ✔ |ΣE| ≤ c·max|E| = O_P(1). ✔ Sum of three tight terms is tight. ✔
- **Wave-1 citation.** T22(ii-a) (COLLECTED, statement ~3665; proof ~3860) is the same odds identity and needs both sets in Ω; satisfied. The proof also re-derives it, so the citation is not load-bearing. ✔ The proof's warning that T22(i) can discharge H3 only if its lower bound stays above a fixed constant is correct.
- **EXP′ discussion.** E_{n,i} = g_i + R_i − ½log(1+1/n). ✔ H2 ⇔ max g_i = O_P(1) ⇔ max nx_i = O_P(1): nx ≤ 2νx ≤ 2g (since −log(1−x) ≥ x, ν ≥ n/2); conversely −log(1−x) ≤ 2x for x ≤ ½. ✔ The example x = n^{−½} (nx² = 1, νx → ∞) is correct.

### 2.3 Findings (T27(i))

- **E-T27-1.** Location: proof §2, sentence "Multiplying (odds) along the chain and applying H2 yields the exact expression". Severity: **exposition**. Claim: eq. (exact) is an identity that uses only the definition of E_{n,i}; H2 is first used in the next paragraph. Saying "applying H2" suggests the identity depends on an assumption. Suggested wording: *"Multiplying (odds) along the chain and writing each table ratio as n^{−1/2}e^{E_{n,i}} (the definition of E_{n,i}) yields the exact identity"*.
- **N-T27-2 (note, no edit).** The theorem is thin by design: H2 and H3 carry all the statistics. It is a correct conditional statement, but it should not be read as showing that cancellation actually happens under G/R/SE.

No fatal finding, no gap.

---

## 3. Comparison with the OpenAI reviews (Step 2)

**T22(iii) flaw log.** Both Sol reviewers found nothing. I agree there is no fatal finding or gap. They missed only the cosmetic E-T22-1, which is optional.

**T27(i) flaw log.** Both Sol reviewers raised the same exposition point ("uniformly on that family" was ambiguous), and the lead fixed it in v2. I agree with the objection and the fix: the v2 text "uniformly over the selected chain comparisons i = 0,…,c−1" is correct and precise.

**WAVE2_REVIEW/REVIEW.md (Astra closing review), T22(iii) and T27(i) sections.** I agree with every mathematical claim in these sections. Specifically:
- T22(iii) summary bullets (residual control, leakage-only quadratic form, truncated integral + Markov, VIS + logarithmic telescoping, κ threshold, use of T22(i-a,b)): each matches my own check in §1.2.
- T27(i) summary (positivity, prior ratio, bounds on A, tightness, EXP′ equivalence): matches §2.2.
- Wave-1 citation table rows for T22(iii) and T27(i): correct.
- **B1** (leakage-family quadratic form cannot give cancellation along true-variable additions): agree.
- **B2** (T22 concentration and T27 cancellation are different regimes; π₀(S^(0)) ≤ 1 − π₀(S₀) for a proper-subset reference, so H3 and T22(iii)'s conclusion cannot hold together): agree; this is the most useful remark in the review for Felipe.
- **B3** (q < 1 does not give H3): agree.
- Circular-dependence check for these two proofs: agree, no cycle.

Where I differ: only in that I propose two optional wording edits (E-T22-1, E-T27-1); the closing review proposed none. Neither changes a claim.

## 4. An observation outside the audit scope (unverified sketch)

EXP′ is currently an **assumption** in T22(iii). From the closed-form score it looks **provable** from G, R (bounded signal energy) and within-block SE, which would remove one hypothesis. Sketch: write Q_S ≈ RSS_S + ESS_S/(n+1) (standardised units) plus a ridge correction of relative size O(n^{−2}); then −ν log[(0.02+Q_{T+l})/(0.02+Q_T)] = −ν log(1−x) + O(ESS/RSS), which is O(1) when RSS_T ≥ c·n (Lemma 1); and D_{T+l}/D_T = (n+1)(1 + O(1/n)) by Schur complements when ‖(I−P_T)x_l‖² ≥ φ₀²(n−1). Single-seed local check (p = 6, correlated pair, β scaled by 0.3/1/3, 20 replicates per n, all within-block-type additions from five T's): max |R| was 16.5, 15.7, 14.9 at n = 10², 10³, 10⁴, i.e. bounded but not small when the signal is strong. This is a sketch, not a checked proof; if wanted, it is a natural short theorem-proving task.

## 5. Final verdicts

- **T22(iii): correct.** Optional exposition fix E-T22-1 (wording in §1.4).
- **T27(i): correct.** Optional exposition fix E-T27-1 (wording in §2.3).

Both are conditional theorems: T22(iii) rests on EXP′, VIS, NL_η and NL_avg(κ); T27(i) rests on H2 and H3. Neither proof establishes those inputs.
