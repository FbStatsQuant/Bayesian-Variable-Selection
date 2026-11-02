# W2-VT03R — REPORT: adversarial verification of W1-T03R

Run W2-VT03R, 2026-11-02, branch `theory/W2-VT03R`. This run referees `theory_campaign/W1-T03R/` on branch `theory/W1-T03R`: its REPORT.md, PROOF.md and scripts. The locked proofs are cited as:
- **[P1]** `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`;
- **[P3]** `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex`.

W1 labels (E1, E2, E3, den′, B1–B3, C1–C10, Prop. D) are as in W1's PROOF.md. Verdict words per step: **VERIFIED**, **GAP**, **ERROR**. Status words for results: as in PROTOCOL. Every verdict is a single-referee verdict from one model family. It is not an adoption.

## Headline

1. **No GAP and no ERROR in the mathematics.** I checked each changed step of W1 line by line against [P1] and [P3]:
   - Lemma E1 (a)–(d), Lemma E2 (i)–(iii) and Prop. E3;
   - Lemma den′ and T02(i♯) with its explicit constants;
   - Lemma B, and T02(ii♯) under SE_w;
   - T03♯ under SE_λ(j₀) + SE_w(m♯; g₀) + BM: (C1)–(C10) and the assembly.

   Every step is **VERIFIED**. Exact-rational and brute-force numerics back E1/E2 (2,779 parameter triples) and the deterministic inequalities (on random, equicorrelated and near-collinear designs).
2. **Prop. D (COUNTEREXAMPLE) is reproduced** independently, analytically and numerically. Brute-force evidences agree with W1's closed form to 10⁻¹³. The bound holds on E_n in every case, P(E_n) = 1 in all replicates up to n = 2·10⁵, and the required cutoffs are 4/6/8/9 ≈ ½log₂n. Scope: it refutes the target under **G and R only**. That is how W1 states it in its body; its headline 1 reads more broadly.
3. **Hidden SE uses: none found.** Two facts settle the question:
   - (a) The only eigenvalue uses on sets *not* containing S₀ are on subsets S ⊆ S₀ ∪ J′(S). Interlacing covers them.
   - (b) The underfitting branch |J′(S)| > j₀ is replaced by a bound that needs no eigenvalue condition. I verified it.

   Clarification: by interlacing, the "anchored" SE_w(m) is *equivalent* to λ_min(G_T) ≥ g₀ for **every** T with |T∖S₀| ≤ m (Lemma A1 below). Anchoring therefore saves only s₀ columns. The real weakenings are the size (m♯ instead of m_n) and the normalisation (g₀ instead of (n−1)φ₀²) for the large sets.
4. **One ERROR, in a numerical claim in W1's REPORT and disclosure paragraph (not in a theorem).** W1 claims "the proof's own deterministic thresholds start near n ≈ 1.2·10⁵" and "other thresholds bind earlier". This is false:
   - the geometric-series condition q_n ≤ ½ of [P3] `prop:sup`(b) / W1 (C5)(b) first holds at n ≈ **2.1·10⁶** (p = n^{1.17}) and **2.5·10⁶** (p = n^{1.30});
   - W1's own stated condition e^{2ε_n} ≤ 4 in (C5)(b) first holds at n ≈ 2.6·10⁷ and 3.0·10⁷.

   The repair is below (§3, R1). The error makes the n = 200 disclosure *stronger*, not weaker.
5. **New, PROOF SKETCH (Prop. W):** SE_λ(j₀) is used essentially only in [P3] `lem:signal`. T03♯(i)–(iii) hold with SE_λ(j₀) + BM(c) replaced by SE_w + a direct signal-separation condition SIG(c).

## 1. Verdict table

| # | W1 item | Checked against | Verdict | Notes |
|---|---|---|---|---|
| 1 | E1(a): ρ_i identity; q_k/w(s₀) = C(p,s₀)∏ρ_i | [P1] `lem:prior`(b),(c) | VERIFIED | exact rational check, all k ≤ K, 2,779 (p,n,s₀) |
| 2 | E1(b) upper bound | — | VERIFIED | ρ₀ ≤ ½e^{1/(2p−2)} and ρ_i ≤ ½e^{−(i−1)/(2p−2)}; the index sum and the monotonicity of t(t−1) are re-derived; numerics: max R_m/ub = 0.998 |
| 3 | E1(c) lower bound (s₀ ≥ 1, m ≤ K−1) | — | VERIFIED | log(2ρ_i) = −log(1+(i−1)/(2(p−i))); tight (ratio → 1) at m = s₀ |
| 4 | E1(d) gain ≥ 4·s₀!·e^{γ_m} over the locked 4(2p)^{s₀}2^{−m} | [P1] `lem:prior`(c),(d), `thm:T02i` | VERIFIED | |
| 5 | m♯ well defined, ≤ K | — | VERIFIED | R_m is nonincreasing and R_K = 0 |
| 6 | E2(i) m♯ ≤ min(K, m_n) | 00_COMMON m_n(ω) | VERIFIED | needs s₀ ≥ 1, or s₀ = 0 with n ≥ 5, as stated |
| 7 | E2(ii), E2(iii) | — | VERIFIED | exact check on 129 cases |
| 8 | Prop. E3 | — | VERIFIED | as a statement about m♯. "Any bound of this form" is a correct reading for bounds of the type Markov numerator / S₀-denominator; it is not a lower bound for the posterior (W1 says so) |
| 9 | Lemma den′ | [P1] `lem:den` (body, l. 337–359) | VERIFIED | identical to the body before the factor ϖ(S₀) ≥ ½(2p)^{−s₀} is used |
| 10 | T02(i♯): the inequality with explicit constants; the O_P consequence | [P1] `thm:T02i`, `thm:Ta`, `lem:num`, `thm:T01iii` | VERIFIED | c♯ = κ²/(c_IG σ*²); E₀Θ⁽¹⁾ = 1 exactly; P₀(𝓑ₙᶜ) ≤ (8+24M/σ*²)/(n−1) re-derived. Pointwise chain checked numerically (§4.3) |
| 11 | Prop. D (COUNTEREXAMPLE) | — | VERIFIED | every constant re-derived: √(2/3)/(½+e^{1.01}) = 0.25157 ≥ ¼ (margin 0.0016); ((n+1)N+1)(N+0.02) ≤ 2nN² ⇔ n²−3.02n+2 ≥ 0. Numerics in §4.2 |
| 12 | SE_λ(j₀), SE_w(m♯; g₀) implied by the locked SE | 00_COMMON SE | VERIFIED | for n with j₀ ≤ m_n; SE_w with g₀ = φ₀² |
| 13 | Lemma I (interlacing); Lemma B (B1), (B2), (B3) | [P1] `lem:spec`(c),(e); [P3] `lem:smoother`(b),(c), `cor:diff` | VERIFIED | (B3) is the upper half of `cor:diff`; only λ_min(G_S) on the *smaller* set is needed. Checked on 9,000 random pairs |
| 14 | T02(ii♯) changes 1–5 | [P1] §`sec:T02ii`, `lem:onG`, `lem:one`, `thm:T02ii` | VERIFIED | `lem:onG`(c) already uses only R on S₀; the only SE use in [P1] §`sec:T02ii` is the determinant in `lem:one` and the exact χ² law, both supplied by (B1). c₂ = √(eC_A(1+1/g₀)) re-derived |
| 15 | (C1) m_n := m♯ | [P3] §1, eq. `eq:mn` | VERIFIED | δ_n, ε_n, q_n are monotone in m_n |
| 16 | (C2) ranks and laws; 𝒢ₙ unchanged | [P3] §`sec:good`, `lem:Gprob` | VERIFIED | Remark: (G4) needs *no* eigenvalue condition, because rank(P_{S′} − P_S) ≤ \|J(S)\| always and stochastic domination by χ²_{s₀} suffices. W1's attribution to (B2) is unnecessary but harmless |
| 17 | (C3) `lem:ongood`(c) restricted to \|J′(S)\| ≤ j₀ | [P3] `lem:ongood`(c) | VERIFIED | S ⊆ S₀ ∪ J′(S), interlacing |
| 18 | (C4) `lem:onesup` under SE_w | [P3] `lem:onesup`, `lem:det`, `cor:diff` | VERIFIED | determinant from (B1); numerator from (B3) with R on S₀ |
| 19 | (C5) `prop:sup` with (1+1/g₀), c_q | [P3] `prop:sup` | VERIFIED | q_n² = c_q²r_n²·(n/(n+1))·e^{2ε_n}/4 |
| 20 | (C6)(a) crude ℓ(S)/ℓ(S′) ≤ (2p)^{\|J\|}(n+1)^{\|J\|/2}, no eigenvalue condition | [P3] `lem:prior`(a), `lem:det` (first part), `lem:smoother`(d) | VERIFIED | holds for every rate b > 0. Checked on 15,240 (S, b) |
| 21 | (C6)(b) sharp `lem:SvsSp` for \|J′\| ≤ j₀ | [P3] `lem:SvsSp` | VERIFIED | |
| 22 | (C7) `lem:signal`, `lem:signalgain` | [P3] | VERIFIED | applied only with \|J′\| ≤ j₀ |
| 23 | (C8) `lem:assemble` | [P3] `lem:assemble` | VERIFIED | e^{ρ_n} instead of [P3]'s e^{2ρ_n} on the second term is correct, since (C6)(a) carries no e^{ρ_n}. (j₀+1)/2 ≥ s₀(A+½)+1 re-derived |
| 24 | (C9) Step 0 through T02(i♯) | [P3] eq. `eq:tail` | VERIFIED | |
| 25 | (C10) BM(c), c > L*, or BM-∞ | [P3] Step 1, (iv), Remark "on M*" | VERIFIED | n ≥ c/(c−L*) is the extra threshold |
| 26 | Assembly (i)–(v) | [P3] §`sec:main` | VERIFIED | the decomposition of Ω∖{S₀} is unchanged; every superset needed has \|J\| ≤ m♯ |
| 27 | Threshold table, R_m table, first n with m♯ < K (342 vs 464) | — | VERIFIED | reproduced exactly (`verify_E1_exact_output.txt`) |
| 28 | β-min numbers (L* = 1037.5 / 1153.2; θ² ≥ 27.5/φ₀², 30.6/φ₀²; executed 0.64 / 0.16 / 3.24) | 00_COMMON BM-C; THEORY_INVENTORY l. 207 | VERIFIED | |
| 29 | "Deterministic steps of the T03 proof hold from n ≈ 1.2·10⁵; other thresholds bind earlier" (REPORT headline 4, §3, §5) | [P3] `prop:sup`(b); W1 (C5)(b) | **ERROR** | the binding condition is q_n ≤ ½: n ≈ 2.1·10⁶ / 2.5·10⁶. See R1 |
| 30 | "SE restricted to the comparison unions actually used (not all subsets)" (REPORT §1, disclosure) | — | imprecise wording, not a mathematical error | by Lemma A1 this is equivalent to a condition on all T with \|T∖S₀\| ≤ m. See R2 |

## 2. Statements (refined or new in this run)

**Lemma A1 (anchored = unanchored up to s₀ columns; PROVED).** Let g > 0 and m ≥ 0. The following are equivalent:
- (a) λ_min(G_{S₀∪J}) ≥ g for every J ⊆ [p]∖S₀ with |J| ≤ m and S₀ ∪ J ≠ ∅;
- (b) λ_min(G_T) ≥ g for every nonempty T ⊆ [p] with |T∖S₀| ≤ m.

The same holds with R in place of G and φ₀² in place of g.

*Proof.* (b) ⇒ (a): T = S₀ ∪ J has T∖S₀ = J. (a) ⇒ (b): T ⊆ S₀ ∪ (T∖S₀) with J := T∖S₀, |J| ≤ m. By Cauchy interlacing (W1 Lemma I), λ_min(G_T) ≥ λ_min(G_{S₀∪J}) ≥ g. ∎

Consequences:
- SE_w(m; g₀) implies the unanchored non-degeneracy λ_min(G_T) ≥ g₀ for **all** T with |T| ≤ m.
- In particular, every m columns of X are linearly independent: spark(X) > m.
- At n = 200 with m♯ = K = 100, SE_w requires every 100 columns of X to be linearly independent with λ_min(XᵀX) ≥ g₀, and every 114-set that contains S₀ likewise.
- SE_λ(j₀) requires normalised conditioning φ₀² on **every** set of ≤ j₀ columns, null columns included. So SE_λ(j₀) fails for every fixed φ₀ > 0 once n > 1/φ₀² if a single pair of null columns has correlation 1 − 1/n. Such a pair constrains SE_w only to g₀ ≤ λ_min(G_{{a,b}}) = (n−1)(1−r) = (n−1)/n, so it is compatible with SE_w for any fixed g₀ < 1/2 (n ≥ 2).

**Proposition W (SE_λ is needed only for the signal; PROOF SKETCH).** Define, for c > 0:

> **SIG(c):** for all large n, every underfitting S with |S| ≤ m♯_n and |J′(S)| ≤ j₀ has Δ_S = ‖(I−P_S)μ_c‖² ≥ cσ*² log n.

Assume R1, G, R (including λ_min(R_{S₀}) ≥ φ₀²), SE_w(m♯_n; g₀) and SIG(c) with c ≥ L*. Then T03♯(i)–(iii) hold.

SE_λ(j₀) + BM(c) implies SIG((1−1/n)c), by [P3] `lem:signal`. So Prop. W contains T03♯(i)–(iii).

*Sketch.* SE_λ(j₀) enters W1's proof in exactly three places: (C3) = `lem:ongood`(c), the lower half of `cor:diff` inside (C6)(b), and `lem:signal` in (C10). Each is handled as follows.

1. **`lem:ongood`(c).** Take S ≠ ∅ underfitting with |J′(S)| ≤ j₀. SE_w and interlacing give λ_min(G_S) ≥ g₀. [P1] `lem:spec`(c) then gives I − M_S ⪯ (I−P_S) + (1+1/g₀)(n+1)^{−1}P_S. So 2b + Q^c_S ≤ E′_n + V_S, where:
   - E′_n := 2b + ‖e‖² + (1+1/g₀)(n+1)^{−1}‖y_c‖²;
   - on 𝒢_n, Nσ*²(1−δ_n) ≤ E′_n ≤ Nσ*²(1+δ‴_n);
   - δ‴_n := 3√(log n/N) + (12b₀ + 4(1+1/g₀))(M+σ*²)/(Nσ*²) → 0.

   (Checked numerically as [OGc′], §4.3.)
2. **Lower half of `cor:diff` with an eigenvalue bound g₀ on T = S′ only.** M_{S′} − M_S ⪰ (n/(n+1))[(P_{S′} − P_S) − η′P_{S′}], with η′ = 1/((n+1)g₀). (Checked as [CDl′].) In `lem:SvsSp` the subtracted term is

   ν(n/(n+1))η′‖y_c‖²/E′_n ≤ 8n²(M+σ*²)/((n²−1)g₀σ*²) ≤ ρ′ := 9(M+σ*²)/(g₀σ*²),

   a constant. The second inequality of `lem:SvsSp` holds once δ‴_n ≤ 1.
3. **`lem:signalgain`.** Use Δ_S ≥ L*σ*² log n directly from SIG, and (G4), which needs no eigenvalue condition. This gives κ_n(𝒰) ≤ e^{ρ′}n^{−2} on 𝒢_n. The constant e^{ρ′} does not affect any rate. The rest is T03♯ verbatim.

Status PROOF SKETCH: the verbatim parts were not re-typeset line by line, and (iv) needs a per-coordinate version of SIG that I did not write.

**Proposition D′ (scope of Prop. D; PROVED).** Under the hypotheses of T03♯, conclusion (i) gives Π(|S| > s₀ | y) ≤ 1 − π(S₀) = O_P(r_n). Hence the cutoff s₀ + 0 works under SE-type conditions *a posteriori*. Prop. D refutes "m_n = s₀ + O(s₀ log n/log p)" only as a size-tail statement under G and R alone. The large m_n is an artefact of the SE-free Markov route that T02(i)/(i♯) take.

*Proof.* {|S| > s₀} ⊆ Ω∖{S₀}. ∎

## 3. Repairs

There is **no GAP to repair**. The ERROR in row 29 and the wording in row 30 are fixed as follows.

**R1 (replaces W1 REPORT headline 4, last clause; §3 "Proof thresholds"; and the sentence in the §5 disclosure).** Source: `scripts/proof_thresholds.py`, output in `proof_thresholds_output.txt`. The conditions are evaluated with p = n^A, s₀ = 14, the most favourable g₀ = ∞, and exact m♯.

| Condition | Source | First n, p = n^{1.17} (m♯) | First n, p = n^{1.30} (m♯) |
|---|---|---|---|
| δ_n ≤ ½ (W1's "binding" condition) | [P3] `lem:ongood`(b) | 115,150 | 130,328 |
| n/5 ≥ (s₀(A+1)+2) log n | [P3] Step 1 | 1,142 | 1,217 |
| **q_n ≤ ½** (geometric series) | [P3] `prop:sup`(b), W1 (C5)(b) | **2,116,048** | **2,457,025** |
| e^{2ε_n} ≤ 4 (W1's condition for q_n ≤ c_q r_n) | W1 (C5)(b) | 25,571,897 | 29,755,302 |

With the locked m_n the same rows read 127,302 / 2,268,667 / 27,055,513 (A = 1.17).

The condition e^{2ε_n} ≤ 4 only fixes the constant c_q, so a larger constant would remove it. The q_n ≤ ½ condition is structural to the proof as written: the series Σ(j+1)^{s₀}q_n^j must converge with the stated constant K_{s₀,j₁}.

Replacement sentence for the disclosure paragraph:

> "…and the proof's own deterministic thresholds (as written) hold only from n ≈ 2×10⁶ (p = n^{1.17}) to 2.5×10⁶ (p = n^{1.30}); the O_P constants are unspecified."

**R2 (wording of the SE restatement; W1 REPORT §1 and the disclosure paragraph).** After "restricted to the comparison sets S₀ ∪ J that the proof uses", add:

> "By eigenvalue interlacing this is equivalent to requiring the same bounds for every column set T with at most j₀ (resp. 100) columns outside S₀; in particular every 100 columns of X must be linearly independent, with λ_min(XᵀX) ≥ g₀."

In W1 headline 1, replace "The brief's premise about m_n is false" with:

> "The brief's premise about m_n is false for the SE-free size-tail route (T02(i)); under G and R alone it is false outright (Prop. D)."

## 4. Evidence

All scripts are in `scripts/`. Outputs are next to this report. Seeds are fixed where randomness occurs.

### 4.1 W1 scripts rerun

`tail_bound.py`, `duplicate_counterexample.py`, `proof_n0.py` and `bm_constants.py` reproduce W1's stored outputs **byte for byte**.

### 4.2 Independent checks

| Script | Checks | Result |
|---|---|---|
| `verify_E1_exact.py` (exact rationals; the threshold test is R_m²n^{s₀+2} ≤ 1 in integers) | E1(a)–(d) on 2,779 (p,n,s₀) triples and all m; E2(i)–(iii) on 129 cases; W1's full threshold table; first n with m♯ < K | all PASS. Table identical to W1, e.g. (n,p) = (200,500): m_old 201, m♯ 100, uncapped 146; (10⁸, n^{1.30}): 712 / 676. First n below K: 342 (exact) vs 464 (locked) |
| `propD_independent.py` | **Part A:** brute-force log m(S) from the 00_COMMON formulas (slogdet/solve) for *every* S ∈ Ω, n = 8–16. **Part B:** closed form at n = 50 … 2·10⁵. **Part C:** the analytic constants | **A:** within-size-class spread and difference from W1's closed form ≤ 1.1·10⁻¹³; the bound holds on E_n in 108/108 cases (the 200 data sets include 50 adversarial, non-model y vectors); min tail/bound = 5.8. **B:** P(E_n) = 1.000 and bound 100% at every n; 2^m·Π(\|S\|>m\|y) ∈ [0.70, 1.00] for m ≤ 16 at n ≥ 200; cutoff for an n^{−1/2} tail = 3, 4, 4, 6, 8, 9 at n = 50, 200, 200, 2·10³, 2·10⁴, 2·10⁵ (= ⌈½log₂n⌉ in every row) |
| `check_deterministic.py` (60 designs: iid, equicorrelated 0.9, one near-collinear pair at corr ≈ 1−1/n; n = 12–40, p ≤ 8; exhaustive over models) | (B3); (C6)(a) for all rates b ∈ {10⁻⁴, 0.01, 1, 100}; (B1); the [P3] eq. `eq:score` identity; the Prop. W variants [OGc′], [CDl′]; Lemma den′; the T02(i♯) chain Π(\|S\|>m\|y) ≤ R_m(n+1)^{s₀/2}√n·c♯e^{Λ_n}Θ⁽¹⁾ on 𝓑_n | every inequality holds. Worst slacks: −4.8·10⁻¹⁰ (B3, tight), −0.096 (C6a), −8.6·10⁻⁶ (B1), identity error 2.4·10⁻¹⁴, −5·10⁻¹¹ (OGc′), −1·10⁻¹¹ (CDl′), −2.9 (den′, log scale), −4.7 (chain, log scale) |
| `proof_thresholds.py` | every explicit deterministic threshold of [P3] + W1 that depends only on (n, p, s₀, A, g₀) | R1 table. W1's claim "other thresholds bind earlier" is false |

### 4.3 What the stress tests do and do not show

They test the *deterministic* inequalities on which the changed steps rest, including designs with near-duplicate columns. They are not a test of the asymptotic theorem: no finite-n check can be.

## 5. What fails and why (routes tried)

- **Hunting a hidden SE use on unions without S₀.** I inventoried every occurrence of λ_min, φ₀, "SE", `cor:diff`, `lem:det` (second part), `lem:signal` and `lem:smoother`(c) in [P1] and [P3] (grep, then reading each):
  - [P3] l. 119 (interlacing in `cor:diff`);
  - [P3] l. 220 (`lem:ongood`(c), on S itself);
  - [P3] l. 282 (preamble of §6, "SE applies to S").

  These are the only uses on sets that do not contain S₀. Every one is on a subset S ⊆ S₀ ∪ J′(S), and the anchored condition covers it by interlacing (Lemma A1). The branch |J′(S)| > j₀ in `lem:assemble` used [P3] `lem:SvsSp`, which needs `lem:ongood`(c) on S. W1 replaced it by (C6)(a), which needs nothing, and I verified that bound.

  (G2) unions over all T with |T| ≤ m♯ + s₀ but needs only rank(X_{c,T}) ≤ |T|. (G4) needs no eigenvalue condition at all.

  **Result: no hidden use.** Given Lemma A1, a hidden use would have to be a *normalised* bound on a set with more than j₀ columns outside S₀, or any bound on a set with more than m♯ columns outside S₀. Neither occurs.
- **Trying to break T02(i♯) by a data-dependent rate or by m-dependence.** The rate b₋ in the numerator is data-free, so [P1] `lem:num` applies. The denominator constant c_IG is fixed because b₊ is fixed. The bound is uniform in m because R_m is factored out exactly. No break found.
- **Trying to break E3 as a claim about the posterior.** E3 is not such a claim, and W1 does not make it one. Under the T03♯ hypotheses the posterior concentrates on size s₀ (Prop. D′), so the Θ(s₀ log n) cutoff is a property of the SE-free route only.
- **Trying to break Prop. D at the boundary.** The constant ¼ has margin 0.0016, but it is exact and correct. P(E_n) → 1 needs β₁ ≠ 0 fixed; with β₁ = 0 the design has s₀ = 0, and the proposition makes no claim there.

## 6. Needs escalation

1. **HQ: correct the n = 200 disclosure** (R1, R2) before it enters the paper. The fix is a number and one sentence.
2. **Independent check of Lemma A1's consequence for the paper's framing.** The SE restatement is weaker than the locked SE mainly through size and normalisation, not through anchoring. A second family should confirm that the paper does not advertise anchoring as the main relaxation.
3. **Prop. W** (SE_λ needed only for the signal) is a PROOF SKETCH. If HQ wants the weakest T03 hypothesis set, a prover should write it out, including a per-coordinate SIG for (iv).
4. The **T03♯ chain as a whole** should still go to the cross-family review W1 already requests: one same-family referee is not adoption.

## 7. Outside scope (not pursued)

- W1's `se_n200.py` (greedy adversarial eigenvalues at n = 200) was not rerun. Its numbers are upper bounds on minima and are labelled so; the exact minima over C(486,100) sets remain unknown.
- Lemma A1 implies that SE_w(100) at n = 200 requires spark(X) > 100. For Gaussian designs this holds almost surely, but the size of g₀ is the open question. Not pursued.
- T04 and the downstream uses of H-T02 (W1 §6 item 3): not checked.

## 8. Confidence card

| Target | Refined statement | Status | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|---|
| Lemma E1 (a)–(d) | as W1 | PROVED (W1); VERIFIED here | 0.99 | 0.99 | elementary factor bounds; exact check | no |
| Lemma E2 / Prop. E3 | as W1 | PROVED (W1); VERIFIED here | 0.98 | 0.98 | E3 is about the technique, not the posterior | no |
| T02(i♯) with explicit constants | as W1 | PROVED (W1); VERIFIED here | 0.97 | 0.97 | Lemma den′ = body of [P1] `lem:den` | no |
| T02(ii♯) under SE_w(m♯; g₀) | as W1 | PROVED (W1); VERIFIED here | 0.95 | 0.95 | (B1): determinant and exact χ² need only rank + g₀ | no |
| T03♯ under SE_λ(j₀) + SE_w(m♯; g₀) + BM | as W1 | PROVED (W1); VERIFIED here | 0.93 | 0.92 | (C6)(a) handles \|J′\| > j₀ without eigenvalues; (C3)/(C6)(b) by interlacing | no |
| Prop. D (duplicate columns) | as W1; scope: G and R only (Prop. D′) | COUNTEREXAMPLE (W1); reproduced | 0.98 | — | P₀(m(∅) ≤ m({1})) → 1 | no |
| Anchored SE suffices everywhere | no hidden use; anchored ⇔ \|T∖S₀\| ≤ m (Lemma A1) | Lemma A1 PROVED; the no-hidden-use audit is a careful single reading | 0.95 | — | interlacing | no |
| Proof thresholds | q_n ≤ ½ binds at n ≈ 2.1–2.5·10⁶ | W1 claim: ERROR; corrected numbers computed | 0.97 | — | e^{2ε_n} with ε_n ≈ δ_nC_A log n/2 | no |
| Prop. W (SE_λ only in `lem:signal`) | T03♯(i)–(iii) under R, SE_w, SIG(c ≥ L*) | PROOF SKETCH | 0.85 | 0.85 | ρ_n becomes a constant ρ′ = 9(M+σ*²)/(g₀σ*²), harmless in `lem:signalgain` | no |
