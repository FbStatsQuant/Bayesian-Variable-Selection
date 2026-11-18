# W1-T03R — REPORT: exact BB(1,p) tail in T02(i), restated T03

Run W1-T03R, 2026-11-02, branch `theory/W1-T03R`. Every status below is a **candidate pending cross-family review**. Full proofs: `PROOF.md`. Scripts: `scripts/`. Raw outputs: `*_output.txt`.

## Headline

1. **The brief's premise about m_n is false. The exact BB(1,p) tail does not bring m_n down to s₀ + O(s₀ log n / log p).** The BB(1,p) size marginal is exactly geometric with ratio ρ_i = ½(1 − (i−1)/(2p−1−i)) (Lemma E1(a)). The per-model ratio w(k+1)/w(k) ≈ k/(2p), quoted in FABLE_REVIEW and FROZEN_LIST, is cancelled by the multiplicity C(p,k+1)/C(p,k) ≈ p/k. The exact tail improves the locked bound by the factor 4·s₀!·e^{γ_m}: about 36 bits at s₀ = 14, plus m²/(4p) nats. It cannot do more:
   - **PROVED (Prop. E3):** the two-sided bound E1 shows that any bound of the T02(i) form needs m − s₀ ≥ log₂C(p,s₀) + ((s₀+2)/2)log₂n − O(1).
   - **COUNTEREXAMPLE (Prop. D, reproducible):** under G and R alone, a design with duplicated columns has Π(|S|>m | y) ≥ 2^{−(m+4)}e^{−m²/(4(p−m))} with probability → 1. So *no* cutoff s₀ + O(1) gives an O_P(n^{−1/2}) tail; at least ½log₂n − O(1) is necessary.
2. **T02(i♯), PROVED (candidate):** Π(|S|>m | y) = R_m(n+1)^{s₀/2}√n·Θ♯_{n,m}. Here R_m = ϖ(|S|>m)/ϖ(S₀) is the exact, data-free prior ratio, and P₀(Θ♯ > L) has an explicit non-asymptotic bound uniform in m. The new cutoff m♯_n is the smallest m ≥ s₀ with R_m ≤ n^{−(s₀+2)/2}. It satisfies m♯_n ≤ min(K, m_n^{old}), and it saves 36–100 sizes relative to m_n^{old} (table below).
3. **T03♯, PROVED as a candidate** (changed steps written in full; unchanged steps cited by label). Same conclusions (i)–(v). The changes:
   - H-T02 is removed.
   - SE is replaced by two conditions **anchored at S₀ ∪ J**, the comparison unions actually used:
     - **SE_λ(j₀):** normalised λ_min(R_{S₀∪J}) ≥ φ₀² only for |J| ≤ j₀ = ⌈(2A+1)s₀⌉+1, a *fixed* size;
     - **SE_w(m♯_n; g₀):** only λ_min(G_{S₀∪J}) ≥ g₀ > 0 (unnormalised, i.e. normalised ≥ g₀/(n−1), meaning "no near-exact collinearity") for |J| ≤ m♯_n.
   - The beta-min condition is BM-∞, or BM(c) with any fixed c > c₀(s₀,A) (an unnamed constant; the proof's value is L*).
   - Both new SE conditions are implied by the locked SE.
4. **At n = 200 the rank obstruction disappears because of the cap K = ⌊n/2⌋, not because of the exact tail.** We have m♯ = K = 100 at both p, so SE_w concerns at most K + s₀ = 114 ≤ 199 columns. The exact uncapped cutoff, 146 (p = 500) / 168 (p = 1000), still exceeds K. Nothing becomes quantitatively informative at n = 200:
   - the size-tail inequality is ≥ 10^{15.8} for every m < K;
   - the beta-min constant still fails by 43× (p = 500) / 48× (p = 1000) in θ², even with φ₀² = 1;
   - the proof's own deterministic thresholds start near n ≈ 1.2·10⁵.

## 1. Refined statements (all hypotheses named)

Notation as in 00_COMMON. The quantities used below:
- K = min(p, ⌊n/2⌋);
- q_k = C(p,k)w(k);
- R_m = Σ_{m<k≤K} q_k / w(s₀);
- m♯_n(ω) = min{m ≥ s₀ : R_m ≤ n^{−(s₀+1)/2}e^{−ω}}, and m♯_n = m♯_n(½ log n);
- j₀ = ⌈(2A+1)s₀⌉+1.

**Lemma E1 (exact tail; PROVED).** Let p ≥ 2 and ρ_i = (p−i)/(2p−1−i).
- (a) ρ_i = ½(1 − (i−1)/(2p−1−i)), and q_k/w(s₀) = C(p,s₀)∏_{i=s₀}^{k−1}ρ_i.
- (b) For m ≥ s₀: R_m ≤ C(p,s₀)·2^{−(m−s₀)}·exp{−[m(m−1) − (s₀−1)(s₀−2)]/(4(p−1))}.
- (c) For s₀ ≥ 1 and s₀ ≤ m ≤ K−1: R_m ≥ C(p,s₀)·2^{−(m+1−s₀)}·exp{−[m(m−1) − (s₀−1)(s₀−2)]/(4(p−m))}.
- (d) The locked bound is R_m ≤ 4(2p)^{s₀}2^{−m}. Bound (b) improves it by at least 4·s₀!·e^{γ_m}.

**Lemma E2 / Prop. E3 (PROVED).**
- s₀ ≤ m♯_n(ω) ≤ min(K, m_n(ω)).
- Closed form: m♯_n(ω) ≤ min{K, s₀ + ⌈(log C(p,s₀) + ((s₀+1)/2)log n + ω)/log 2⌉}.
- In R1 with n^a ≤ p ≤ n^A, either m♯_n = K or m♯_n − s₀ ≥ [s₀ log(p/s₀) + ((s₀+2)/2)log n]/log 2 − 1 − o(1). This is of order s₀ log n, not s₀ log n / log p = O(1).

**Theorem T02(i♯) (PROVED; candidate).** Hypotheses: G and R. Fix n with s₀ ≤ K, and an integer m.
- Define Θ♯_{n,m} by Π(|S|>m | y) = R_m(n+1)^{s₀/2}√n·Θ♯_{n,m}, with Θ♯ := 0 when R_m = 0.
- For L > c♯², with c♯ = κ²/(c_IG σ*²):

  sup_m P₀(Θ♯_{n,m} > L) ≤ (8 + 24M/σ*²)/(n−1) + L^{−1/2} + C_Λ / log(√L/c♯).

  The constants κ, c_IG and C_Λ are those of [P1] `lem:den`.
- Hence Π(|S| > m♯_n(ω_n) | y) ≤ (1+1/n)^{s₀/2}e^{−ω_n}Θ♯ = O_P(e^{−ω_n}) for every deterministic ω_n.

**Prop. D (COUNTEREXAMPLE, reproducible).** Hypotheses: G and R, with s₀ = 1, p identical columns (e.g. p = n), and fixed β₁ ≠ 0.
- With probability → 1, for all 0 ≤ m ≤ K−1: Π(|S|>m | y) ≥ 2^{−(m+4)}e^{−m(m−1)/(4(p−m))}.
- Consequently, Π(|S|>m_n | y) = O_P(e^{−ω_n}) with m_n ≤ √p forces m_n ≥ ω_n/log 2 − O(1).
- So the target "m_n = s₀ + O(s₀ log n / log p)" is false under G and R.

**Hypotheses SE_λ(j₀), SE_w(m; g₀)** (PROOF.md §4). Both are anchored at S₀:
- SE_λ(j₀): λ_min(R_{S₀∪J}) ≥ φ₀² for all J ⊆ [p]∖S₀ with |J| ≤ j₀.
- SE_w(m; g₀): λ_min(G_{S₀∪J}) ≥ g₀ > 0 for all J ⊆ [p]∖S₀ with |J| ≤ m.

By interlacing, SE_λ(j₀) also covers every subset of these unions.

**Theorem T02(ii♯) (PROVED; candidate).** Hypotheses: R1, G, R, SE_w(m♯_n; g₀). Conclusion: Π(S ⊋ S₀ | y) = O_P(√(log n/n)).

**Theorem T03♯ (PROVED; candidate).** Hypotheses for (i)–(iii): R1 (triangular array, s₀ fixed, p_n ≤ n^A), G, R, SE_λ(j₀), SE_w(m♯_n; g₀), and BM-∞ or BM(c) with c > c₀(s₀, A). The constant c₀ is unnamed in the statement; the proof gives c₀ = L* = max{4C*, 32[s₀(A+1)+2]}.
- (i) 1 − π(S₀) = O_P(√(log n/n)).
- (ii) max_j |PIP_j − 1{j∈S₀}| ≤ 1 − π(S₀) for every data set, and P₀(MPM = S₀) → 1.
- (iii) P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] → 0, and S₀ is the strict global maximiser of F on {π(S₀) > ½}.
- (iv) **No beta-min needed.** For fixed c > c₀ and J_n(c) = {j ∈ S₀ : θ*_j² ≥ cσ*² log n/(nφ₀²)}: Π(S ⊉ J_n(c) | y) = O_P(r_n) and 1 − min_{J_n(c)} PIP_j = O_P(r_n). The same holds for J_n^∞ with any M_n → ∞. So large signals get PIP → 1.
- (v) Scale invariance.

The generator's rule s₀ = ⌊√n⌋ is **not** covered (s₀ is fixed).

## 2. Proofs: what changed in the locked proofs

The full new proofs of the changed steps are in PROOF.md §§1–6. [P1] = T01_T02 `PROOF_v3.tex`; [P3] = T03 `PROOF_v2.tex`.

| Locked step | Status | New version |
|---|---|---|
| [P1] `lem:prior`(c),(d) used separately in `thm:T02i` | replaced | Lemma E1, the exact ratio R_m |
| [P1] `lem:den` | body reused; last factor ϖ(S₀) ≥ ½(2p)^{−s₀} dropped | Lemma den′ |
| [P1] `thm:T02i` | changed (prior factor) | T02(i♯), §2 |
| [P1] `lem:one` (determinant step), `thm:T02ii` | changed (SE → SE_w; a_n, c₂ with 1+1/g₀; T₂ through T02(i♯)) | §5 |
| [P3] §1 (m_n), eq. `eq:mn` | changed definition, same inequality | (C1) |
| [P3] SE paragraph before 𝒢_n | replaced | Lemma B, (C2) |
| [P3] `lem:ongood`(c) | restricted to \|J′(S)\| ≤ j₀ | (C3) |
| [P3] `lem:onesup` | determinant from SE_w; numerator from the upper half of `cor:diff` (needs only λ_min(G_{S₀})) | (C4) |
| [P3] `prop:sup` | (1+1/(Nφ₀²)) → (1+1/g₀); c_q | (C5) |
| [P3] `lem:SvsSp` | split into a crude bound with no SE (used for \|J′\| > j₀) and the sharp bound (\|J′\| ≤ j₀) | (C6) |
| [P3] `lem:assemble` | \|J′\| > j₀ branch through the crude bound | (C8) |
| [P3] Step 0 | through T02(i♯) | (C9) |
| [P3] Step 1, (iv) | BM(c), c > L*, or BM-∞ | (C10) |
| [P3] `lem:red`, `lem:smoother`, `cor:diff`, `lem:det`, `lem:prior`, `lem:signal`, `lem:chi`, `lem:Gprob`, `lem:ongood`(a)(b)(d), `lem:signalgain`, (ii), (iii), (v); [P1] `lem:spec`, `lem:num`, `thm:T01iii`, `thm:Ta`, `lem:good`, `lem:onG` | **unchanged** | cited by label |

## 3. Evidence (task 5 and checks)

### Thresholds at ω = ½ log n, s₀ = 14

Source: `scripts/tail_bound.py`, output in `tail_bound_output.txt`.

| n | p | K | m_old (locked) | m♯ (exact, capped) | m♯ uncapped | old SE size m_old + s₀ | new SE_w size min(m♯,K) + s₀ |
|---|---|---|---|---|---|---|---|
| 200 | 500 | 100 | 201 | **100 (cap binds)** | 146 | 215 | 114 |
| 200 | 1000 | 100 | 215 | **100 (cap binds)** | 168 | 229 | 114 |
| 10³ | 500 | 500 | 220 | 161 | 161 | 234 | 175 |
| 10³ | 1000 | 500 | 234 | 184 | 184 | 248 | 198 |
| 10⁴ | 1000 | 1000 | 260 | 207 | 207 | 274 | 221 |
| 10⁶ | 1000 | 1000 | 313 | 251 | 251 | 327 | 265 |
| 10⁴ | n^{1.17} = 49,177 | 5000 | 339 | 302 | 302 | 353 | 316 |
| 10⁶ | n^{1.17} ≈ 1.1·10⁷ | 5·10⁵ | 501 | 465 | 465 | 515 | 479 |
| 10⁸ | n^{1.30} ≈ 2.7·10¹⁰ | 5·10⁷ | 712 | 676 | 676 | 726 | 690 |

- For p = n^A the saving is ≈ 36 sizes. This equals log₂(14!) = 36.3, as Lemma E1(d) predicts.
- For fixed p the saving grows with n (65–100), because of the Gaussian factor e^{−m²/4p}.
- m♯ − s₀ grows like s₀ log n everywhere, as Prop. E3 predicts.

### Prior ratio R_m (log₁₀) at n = 200, p = 500

| m | exact | E1(b) upper bound | E1(c) lower bound | locked bound 4(2p)^{s₀}2^{−m} |
|---|---|---|---|---|
| 14 | 26.75 | 26.76 | 26.46 | 38.39 |
| 40 | 18.60 | 18.63 | 18.31 | 30.56 |
| 80 | 5.40 | 5.56 | 5.00 | 18.52 |
| 99 | −1.44 | −0.90 | −1.71 | 12.80 |

- The locked bound overstates R_m by 10^{11.6}–10^{14.2}. Of this, 10^{11.6} = 4·14!, and the rest is the Gaussian factor.
- Bounds (b) and (c) bracket the exact value within 10^{0.6}.
- The full T02(i♯) prefactor, minimised over m < K, is 10^{15.8} (p = 500) and 10^{21.3} (p = 1000). It is vacuous at n = 200.
- The cutoff first falls below K at n = 342 (exact) versus n = 464 (locked), for p = n^{1.17}.

### Counterexample (Prop. D)

Source: `scripts/duplicate_counterexample.py`, output in `duplicate_counterexample_output.txt`.
- 2^m·Π(|S|>m | y) lies between 0.70 and 1.00 for m ≤ 16 and n from 200 to 2·10⁵.
- The cutoff needed for an n^{−1/2} tail is 4, 6, 8, 9 at n = 200, 2·10³, 2·10⁴, 2·10⁵. That is ≈ ½log₂n.
- 200 of 200 replicate data sets satisfy the bound 2^{−m}/8.

### Restricted SE at n = 200, p = 500

Source: `scripts/se_n200.py`, output in `se_n200_output.txt`. One design draw each. The greedy adversary gives an *upper* bound on the minimum over J.

| | S1 (iid) random J | S1 greedy | S4 (0.85 blocks) random J | S4 greedy |
|---|---|---|---|---|
| SE_λ: λ_min(R), \|S₀∪J\| = 62 | 0.16–0.21 | **≤ 0.033** | 0.046–0.060 | **≤ 0.0125** |
| SE_w: λ_min(G), \|S₀∪J\| = 114 | 11.3–13.1 | **≤ 0.40** | 2.9–3.7 | **≤ 0.22** |

Neither condition is rank-impossible any more. SE_w with some g₀ ≈ 0.1–0.2 is plausible for these designs, but this is not verified, because the true minimum over C(486,100) sets was not computed.

### Beta-min at n = 200

Source: `scripts/bm_constants.py`.
- c₀ = L* = 1037.5 (p = 500) and 1153.2 (p = 1000).
- The required θ² is ≥ 27.5/φ₀² and 30.6/φ₀² respectively. Under the locked M*, it was ≥ 55.0/φ₀² and 61.1/φ₀².
- Executed signals (THEORY_INVENTORY §C): θ² = 0.64 (c = 1) and 0.16 (c = 0.5); the largest is 3.24.
- The shortfall is 43×/48× with φ₀² = 1. With the adversarial S1 value φ₀² ≈ 0.033 it is ≈ 1,300×.
- For orientation (a heuristic, not a theorem): the orthogonal-design selection scale (log n + 2 log p)/n is 0.089 / 0.096. The executed signals are ≈ 7× above it. **The failure is in the proof constant, not in the signal.**

### Proof thresholds

Source: `scripts/proof_n0.py`. The deterministic steps of the T03 proof (binding condition δ_n ≤ ½) hold from:
- n ≈ 115,000 (new cutoff) versus 127,000 (old cutoff), for p = n^{1.17};
- n ≈ 130,000 versus 143,000, for p = n^{1.30}.

These are only the deterministic thresholds. The O_P constants are not specified.

## 4. What fails and why

- **The frozen-plan sentence "cuts m_n from about 200 to s₀ + O(s₀ log n / log p), so SE on sets of size ≤ m_n + s₀ ≤ K becomes meaningful at n = 200" is wrong on both counts.**
  - The exact tail saves ~36–55 sizes, not ~180. The reason is in Lemma E1(a): the size marginal is geometric(½), so the truth's prior cost log C(p,s₀) ≈ s₀ log p must be repaid at log 2 nats per extra size.
  - Prop. D shows that, without eigenvalue conditions, even the true posterior can need m_n ≳ ½log₂n.
  - What does make SE meaningful at n = 200 is the **cap**: m♯ ≤ K always.
- **Whether the true posterior needs m − s₀ ≍ s₀ log p under G and R is OPEN.** E3 is a barrier for the proof technique (Markov numerator over an S₀ denominator), not a lower bound for the posterior. Prop. D gives only ½log₂n.
- **A route that might give m − s₀ = O(log n) is a CONJECTURE, not attempted in full.** It would need SE_w at *all* sizes ≤ K, a per-eigendirection truncation of the Markov moment, and handling of non-supersets through a weak residual condition.
- **At n = 200 no finite-n guarantee follows from T01–T03.** The reasons are listed in §5 below.

## 5. n = 200 disclosure paragraph (for the paper)

> *Scope at the study's sample size.* Theorem 1 (T03♯) and its lemmas are asymptotic statements for a triangular array with s₀ fixed and p_n ≤ n^A; they are not numerical guarantees at n = 200, p ∈ {500, 1000}, s₀ = 14 (and the generator's rule s₀ = ⌊√n⌋ is outside their scope). In the original formulation the sparse-eigenvalue premise ranged over all subsets of up to 215 (p = 500) or 229 (p = 1000) columns, which is impossible at rank ≤ 199. In the restated version the premise is anchored at the true support and restricted to the comparison sets S₀ ∪ J that the proof uses: a normalised bound λ_min(R_{S₀∪J}) ≥ φ₀² for |J| ≤ j₀ (62 and 66 columns) and an unnormalised non-degeneracy bound λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for |J| ≤ min(m♯_n, K) = 100 (114 columns, because the model-size cap K = ⌊n/2⌋ = 100 binds at n = 200; the exact Beta-Binomial tail alone would give 146 and 168 extra variables). These conditions are no longer excluded by rank, but they are not verified for the realised designs, and in correlated designs the normalised constant can be as small as φ₀² ≈ 0.01–0.03. The beta-min condition remains far from the executed signals: the proof's sufficient constant requires θ*² ≥ 27.5/φ₀² (p = 500) and 30.6/φ₀² (p = 1000) on the standardised scale, against executed values 0.64 (c = 1) and 0.16 (c = 0.5), a shortfall of at least 43× (p = 500) and 48× (p = 1000) even with φ₀² = 1. This is a limitation of the proof constant, not evidence that the signals are weak: a heuristic orthogonal-design scale is ≈ 0.09. The rate √(log n/n) = 0.163 carries unspecified constants, and the proof's own deterministic thresholds hold only from n ≈ 10⁵. The empirical recovery rates at n = 200 are therefore evidence in their own right, not an instance of the theorem.

**Finite-n statements that survive at n = 200** (every n, every data set or exact law):
- **(F1) Deterministic (T03(ii)–(iii) deterministic parts):**
  - max_j |PIP_j − 1{j ∈ S₀}| ≤ 1 − π(S₀);
  - if π(S₀) > ½, then the global HPM and the MPM both equal S₀, and S₀ is the strict maximiser, so no tie-breaking occurs.

  More generally, for any model S* with π(S*) > ½: S* is the strict global HPM and the MPM equals S*.
- **(F2) Exact identities:**
  - T01(i): the posterior is exactly the contrast-model posterior at IG rate b₀s_y²;
  - the Markov identity E₀[Σ_{S∈𝒜} ϖ(S)m^c_b(S)/f₀(y_c)] = ϖ(𝒜) for every fixed rate b.
- **(F3) Explicit inequality (T02(i♯)):**

  P₀(Π(|S|>m | y) > L·R_m(n+1)^{s₀/2}√n) ≤ (8 + 24M/σ*²)/(n−1) + L^{−1/2} + C_Λ / log(√L/c♯).

  It holds at every n, but at n = 200 it is vacuous for every m < K: the prefactor is ≥ 10^{15.8}.
- **(F4) Prop. D at every n:** without eigenvalue conditions, posterior size tails of order 2^{−m} occur. Any finite-n size control must use design conditions.

## 6. Needs escalation (HQ decisions)

1. **Correct FROZEN_LIST "Restatement notes — T03 / T02", first bullet, and FABLE_REVIEW Thm 1.** The premise "ratio ≈ k/2p, not ½" is the per-model ratio. The class ratio is ½. Suggested replacement text: "Use the exact BB tail R_m (saves log₂ s₀! ≈ 36 sizes); the cap K binds at n = 200, so the anchored SE ranges over ≤ K + s₀ = 114 columns."
2. **Adopt the split SE_λ(j₀) + SE_w(m♯; g₀)?** It is weaker than SE and implied by it. It must go through cross-family review together with the changed steps (C2)–(C8).
3. **Downstream.** T04 cites H-T02 with the old m_n. Its SE branches could use m♯ and SE_w, but this was not checked; it is outside scope. T20, T21, T06 and T22(iv-c) use only the T03(i) conclusion, which is unchanged.
4. A finite-n result at n = 200 needs a different route, for example T37 (FABLE). It cannot come from sharpening these constants: even c₀ → 0 leaves the T02(i♯) prefactor vacuous.

## 7. Outside scope (not done)

- Growing s₀.
- Sharp beta-min constants.
- The true-posterior lower bound in the s₀ log p question (OPEN).
- Determinant-only SE (PROOF.md §7, remark 3; CONJECTURE).
- T04 and other downstream re-derivations.
- Verifying SE_w and SE_λ exactly on the realised designs.

## 8. Confidence card

| Statement | Status | P(true) | P(provable) | Crux |
|---|---|---|---|---|
| E1 (exact tail, two-sided bounds) | PROVED | 0.99 | 0.99 | the elementary factor bounds; checked numerically (table) |
| E2/E3 (location of m♯; barrier for the Markov route) | PROVED | 0.97 | 0.97 | E3 is about the technique, not the posterior |
| T02(i♯) with explicit constants | PROVED (candidate) | 0.97 | 0.96 | Lemma den′ is the body of locked `lem:den` before ϖ(S₀) is bounded |
| Prop. D (target false without SE) | COUNTEREXAMPLE | 0.96 | 0.95 | P₀(m(∅) ≤ m({1})) → 1; m_k depends on \|S\| only (exact formulas, numerically confirmed) |
| T02(ii♯) under SE_w only | PROVED (candidate) | 0.93 | 0.92 | `lem:one` needs only rank + determinant penalty; the S₀-eigenvalue in the ridge term comes from R |
| T03♯ under SE_λ(j₀) + SE_w(m♯; g₀) + BM | PROVED (candidate) | 0.90 | 0.88 | every SE use falls in (B1)/(B2)/(B3); the \|J′\| > j₀ branch needs no SE (crude bound (C6)(a)) |
| Brief's target m_n = s₀ + O(s₀ log n / log p) under G, R | COUNTEREXAMPLE | 0.02 | — | duplicate columns |
| True posterior needs m − s₀ ≍ s₀ log p under G, R | OPEN | 0.3 | 0.3 | constructing designs that make large non-supersets cheap |
| Under SE_w at all sizes ≤ K: m − s₀ = O(log n) suffices | CONJECTURE | 0.6 | 0.4 | non-superset large models without beta-min control |
