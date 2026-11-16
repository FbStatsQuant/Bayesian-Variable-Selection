# W3-DIST — P2 same-family pre-check of `lemmas/X.md` v0.2 (Lemma X §0–§8, Lemma X′ §9)

Checker: Claude Opus 5.5 (Claude Third), effort high. Independent line check under `briefs/BRIEF_P2_X_precheck.md`.
This is a same-family filter before the cross-family line check. It is not a review layer.

**Files read:** `lemmas/X.md`, `STATEMENT.md` (§0, §3), `API_CARDS.md` (Common definitions, Cards X/S/V),
[P1] `PROOF_v3.tex` (all of §1–§7 up to the end of `lem:den`), `W3-POST2/lemmas/B_tail_approx.md`, `lemmas/X_route_a.md`,
`work/api_attempts/dist1/X-a-1.md`, `X-a-2.md` (head), `X-b-2.md`, `X-d-1.md`.
**Not read (per brief):** `reviews/`, `LOG.md`, `CHECKPOINT_*`, `DEPS.*`, and `X-b-1.md` (the source of §0–§8, not on
the list). §10 of X.md was not used as evidence.

## Summary

I recomputed every numbered inequality of §0–§7 and §9 with the stated constants. I found no CRITICAL or MAJOR defect.
The fractional-moment route is sound:
- λ = (4A+1)/(4A+2) gives A(1−λ) − λ/2 = −¼ exactly.
- Condition (c) gives λ₁ ≤ 1 − 1/(8A+4).
- The determinant bound uses only 0 ⪯ D′_J ≺ I and rank ≤ s₀ + j.
- Jensen is applied to the (ND) average in the right direction.
- The Markov step at power λ is correct with the indicator of 𝓔_t.

Every [P1] citation exists and is used within its hypotheses. Two definitional gaps need amendment: the definition of
n₀ (F1) and the undefined constants and threshold n₀′ in §9 (F2). The rest are NITs.

## Findings

### F1 — MINOR — §0 line 46 (and §7 line 169): definition of n₀
**Error.** "n₀ is the least n such that, at t = n^{1−κ₀}, (a)–(g) hold." This says the conditions hold *at n₀*. The proof
needs them at every n ≥ n₀. Monotonicity in t, which X.md verifies, gives uniformity in t at a fixed n. It gives nothing
in n. With t = n^{1−κ₀}, the left side of (c) contains (C_A′C_m+4)·n^{−κ₀}log n·n/N. That term *increases* in n for
n < e^{1/κ₀}. So "least n" does not imply "all larger n" without a further argument. Such an argument exists:
- At n ≥ e⁸ in the increasing regime, (C_A′C_m+4)n^{−κ₀}log n ≥ 40·log n/e > 1, so (c) cannot hold there.
- Hence the first n where (c) holds lies in the decreasing regime.
- (a), (b), (d), (e), (f), (g) are monotone in n.

X.md does not give this argument. §7's sentence "the single n₀ is uniform in t because conditions (a)–(g) are monotone in
t" is correct for t only.
**Repair.** "n₀ is the least integer such that for every n ≥ n₀, (a)–(g) hold at t = n^{1−κ₀} (hence for all smaller t)."
Such an n₀ exists because every condition holds for all large n. This is the form X-a-2 uses ("the least n ≥ 16 beyond
which all of the following hold").

### F2 — MINOR — §9 lines 190–205: n₀′, C_v′, C₁′ and C undefined; the "unchanged" v-step needs a new threshold
**Gap.**
- (i) C₁′, C_v′ and the final C of Lemma X′ are used but never defined.
- (ii) "The v-step is unchanged (level t)" gives |v/σ² − 1| ≤ 2(C_β′ + 6)√(t/n) =: C_v′√(t/n), with
  C_β′ := b̄/σ² + 5 + C_Q′. The mean bound uses v ≤ 2σ², which needs C_v′√(t/n) ≤ 1. Condition (f) is stated for
  C_v, not C_v′, and C_v′ > C_v in general. (The step |g| ≤ 6√(t/n) ≤ ½ still follows from (f), since C_v ≥ 12.)
- (iii) §9 says "use the event 𝓔_t of §2 … unchanged". §2's consequences are stated "on 𝓔_t, n ≥ n₀", and n₀ includes
  (d), which involves c_D. The closing claim that the constants depend only on (s₀^r, A, σ², M, M′, κ₀) therefore needs
  n₀′ to be defined without (d).
**Repair.**
- Constants: C_Q′ as written. C_v′ := 2(b̄/σ² + 11 + C_Q′). C₁′ := 4(2C_m + 4 + C_P′ + Λ′). C := max{C₁′, C_v′}.
- M₀′ := max{16, (A+1)s}. This suffices: §9 needs t ≥ 16, n^{(A+1)s₀} ≤ e^t and t ≥ (s₀+1)log 2, but not t ≥ log C₅.
- n₀′ := the least integer such that for all n ≥ n₀′, at t = n^{1−κ₀}:
  - n ≥ 16;
  - (b);
  - (e), first part;
  - (g);
  - Λ′t log n ≤ 8n;
  - √(t/n)·log n ≤ 1;
  - (f′) C_v′n^{−κ₀/2} ≤ 1.

  None of these involves c_D. (a), (c), (d) and (e)'s second part are not used in §9.

With these definitions every step of §9 checks (see the §9 verdict).

### F3 — NIT — §3 Step 4, line 118: interlacing order unstated
"λ_i(G_{S′}) ≤ λ_i(G_S)" holds for i ≤ |S| when eigenvalues are in **increasing** order. In decreasing order the inequality
reverses. With increasing order, D_{S′} = Π_{i≤|S|}f(λ_i(G_{S′}))·Π_{i>|S|}f(·) ≤ D_S(n+1)^{|S′|−|S|}, as claimed.
**Repair:** add "(increasing order, i ≤ |S|)", as in X-a-2 T4 and X-b-2 (F5).

### F4 — NIT — §4 line 132: citation of `lem:prior`(c)
The *statement* of `lem:prior`(c) is ϖ(|S|>m) ≤ 2^{1−m}. The inequality used, Σ_{k>m}q_k ≤ 2^{−m} for m ≥ 0, is a line in
its *proof*. It is correct, and B_tail_approx Remark 4 cites it the same way.
**Repair:** cite it as "proof of `lem:prior`(c)". Using the statement instead would cost a factor 2, which (g) can absorb.

### F5 — NIT — §8 R4, line 185: incomplete list of uses of p ≤ n^A
p ≤ n^A is also used in:
- (E3), through C_m (log(2p) ≤ log 2 + A log n);
- (E4) (x_{|S|} ≤ C_x t);
- §5's last line ((2p)^{s₀}(n+1)^{s₀/2} ≤ 2^{s₀}e^t).

This is a remark only. **Repair:** complete the list.

### F6 — NIT — §8 R1–R2: unproved remarks
R1 (Lemma V(b)'s determinant chain) and R2 (1 − λ ≍ 1/log n recovers q ≍ (log n/n)^{1/2}) are unproved. No step of
§0–§7 uses them. I did not check R1's determinant chain.
**Repair:** label §8 as non-load-bearing commentary.

## Line check by section (key recomputations)

**§0.**
- On the range: t ≥ M₀ log n ≥ M₀, log n ≤ t (M₀ ≥ 16), (A+1)s₀ log n ≤ t (M₀ ≥ (A+1)s), and t/N ≤ 1.5n^{−κ₀}
  (N ≥ 2n/3). ✓
- ε₁, ε₂, ε₃ are deterministic and nondecreasing in t. ε₃ > 0 since n > N. All three → 0 at t = n^{1−κ₀}, since
  t log n/N ≤ 1.5n^{−κ₀}log n. ✓
- Every condition (a)–(g) is monotone in t ✓ (but see F1 for n).
- "32/log n ≤ 3/log 2" ⇔ log n ≥ 7.39, which (a) gives. Then ⌈32t/log n⌉ ≤ ⌈(…+3t)/log 2⌉, so min(d_t, K) ≤ m_n(t). ✓
- WLOG c_D ≤ 1 is valid: the right side of (ND) increases as c_D decreases. ✓

**§1 V(a).**
- M^{(1)}_T = X_{c,T}(H_T/n)^{−1}X_{c,T}ᵀ = M_T ✓. Eigenvalues g/(g + c(g+1)/n) ∈ [0,1) ✓.
- (i), upper bound: φ = θ* + φ′ with penalty ≤ 2θ*ᵀAθ* + 2φ′ᵀAφ′ gives Q_{S₀}(y_c) ≤ Q^{(2)}_{S₀}(e) + 2ρ′.
  Penalty ≥ ½φ′ᵀAφ′ − θ*ᵀAθ* gives Q_S(y_c) ≥ Q^{(1/2)}_S(e) − ρ′. Zero-padding gives θ*ᵀ(G_S+I)θ* = nρ′. ✓
- (ii): Q^{(c)} is nondecreasing in c and nonincreasing in T, so D′_J ⪰ 0. D′_J ⪯ M^{(1/2)}_S ≺ I. The range lies in
  col X_{c,S}, so rank ≤ s₀ + |J|. ✓
- ρ′ = (‖μ‖² + ‖θ*‖²)/n ≤ B ✓. L_{S₀} = Q_{S₀}(μ_c) ≤ ρ′ ✓.

**§2 X1.**
- (N1): (F1) with ν = N/2. ✓
- (N2): 2k log 2 + 4k log p + 4k + 4t ≤ (4A+6)k log n + 4t, using 2 log 2 + 4 ≤ 6 log n for n ≥ 3. The union bound is
  Σ p^k e^{−k log p−k−t} = e^{−t}/(e−1). ✓
- (N3): ‖(I−M_S)μ_c‖² ≤ L_S ✓. Σ_k p^k·2e^{−x_k} = 2e^{−t}/(e−1) ✓. Total ≤ 5e^{−t} ✓.
- (E2): 2√(2(t+1)) ≤ 4√t for t ≥ 1 ✓. The AM-GM splits are correct ✓. (4/3)·1.5M = 2M ✓. Both bounds follow from (b)
  ✓. The result lies inside [P1]'s 𝓑_n = {σ²/2 ≤ s_y² ≤ 2(σ²+M)+1} ✓. 2b ≤ b̄ ✓.
- (E3): (I−P_S)y_c = (I−P_S)e and `lem:spec`(b) ✓. The bound m_n(t) + s₀ ≤ C_m t holds: numerator/t ≤ s₀(A + log 2 +
  0.631) + 4.27 ≤ s(A+2) + 5, using log(n+1) ≤ 1.262 log n for n ≥ 3. Then ν/Q_S ≤ (n+0.02)/(2Nσ²(1−ε₂)) ✓.
- (E4): |S| ≤ min(d_t, K) ≤ m_n(t) ✓. |S| log n ≤ (s₀+33)t ✓. x_{|S|} ≤ (A+1)C_d t + 2t ✓.

**§3 X4(b,c).**
- Step 1: (2b+Q₀)/(2b+Q_J) ≤ Q₀/Q_J ✓, then (1+ξ)^ν ≤ e^{νξ} with ν/Q_J ≤ (1+ε₃)/(2σ²) ✓.
- Step 2: (1 − 1/(8A+4))/λ = (8A+3)/(8A+2) ✓, so λ₁ ≤ 1 − 1/(8A+4) ⇔ ε₃ ≤ 1/(8A+2) ✓.
  det(I − λ₁D′)^{−1/2} = Π(1−λ₁d_i)^{−1/2} ≤ (1−λ₁)^{−(s₀+j)/2} ✓.
  e^{λ₁·3ρ′/(2σ²)} ≤ e^{3B/(2σ²)} since λ₁ ≤ 1 ✓. The indicator is handled correctly: the bound holds pointwise on 𝓔_t
  and is extended as a function of z ✓.
- Step 3:
  - Jensen: mean of x^λ ≤ (mean of x)^λ, with x = (D₀/D_J)^{1/2} ✓.
  - [2(j+1)^{s₀}2^{−j}]^λ ≤ 2(j+1)^{s₀} ✓, and C(p−s₀, j)^{1−λ} ≤ n^{Aj(1−λ)} ✓.
  - c_D^{−λj/2} ≤ c_D^{−j/2} ✓.
  - The exponent is A/(4A+2) − (4A+1)/(2(4A+2)) = −(2A+1)/(2(4A+2)) = −¼ ✓.
  - (d) gives e^{s₀}q ≤ n^{−1/8} ≤ e^{−1} ✓.
  - Geometric sum: with j = j₁+1+i, (j₁+2)^{s₀} ≤ e^{s₀(j₁+1)} and q^i ≤ 2^{−i}, so the sum is ≤ K_s(e^{s₀}q)^{j₁+1}.
    Since (j₁+1)/8·log n ≥ 4t, this is ≤ K_s e^{−4t} ✓.
- Step 4:
  - |J′| ≥ |S| − s₀ + 1 > j₁ ✓.
  - w(k)/w(k+1) = (2p−1−k)/(k+1) ≤ 2p for k ≤ p−1 ✓, and D_{S′}/D_S ≤ (n+1)^{s₀} ✓ (F3).
  - Multiplicity 2^{s₀} − 1 ✓.
  - A_n ≤ 4^{s₀}n^{As₀}(n+1)^{s₀/2} + 1 ≤ 2·4^{s₀}n^{(A+1)s₀} ✓.
  - S′ ∉ Ω is handled: ℓ is defined on all subsets, |J′| ≤ min(m_n(t), p−s₀), and (N2)/(E3) cover |S′| ≤ min(p, m_n(t)+s₀) ✓.
- Step 5: P(1_𝓔 A_nV > e^{−t}) ≤ e^{λt}A_n^λ E[1_𝓔 Σ BF_J^λ] ✓. The product is 4^{s₀+1}e^{3B/(2σ²)}(8A+4)^{s₀/2}K_s e^{−2t}
  ≤ C₅e^{−2t} ✓.
- (ND) is used only on j₁ < j ≤ min(m_n(t), p−s₀) ✓.

**§4 X4(a).**
- R_m = Σ_{m<k≤K}q_k/w(s₀) (W_K cancels) ≤ 2(2p)^{s₀}2^{−m} ✓.
- 2^{−m} ≤ 2^{−s₀}(2p)^{−s₀}(n+1)^{−(s₀+2)/2}e^{−3t}. Hence R_m√(D_{S₀})√n ≤ 2^{1−s₀}√n/(n+1)·e^{−3t} ≤ 2n^{−1/2}e^{−3t} ✓.
- `lem:num`: b₋ = b₀σ²/2 is data-free, and m = m_n(t) is design-measurable ✓.
- Denominator: Q_{S₀} ≤ ‖e‖² + ρ′ (`lem:slab` at θ*) ✓. In [P1] `lem:den`'s proof, the exponent step uses only
  Q ≤ σ²E′ + R with R ≥ 0 and u ≥ 1 (−R/(2σ²u) ≥ −R/(2σ²)). So R_n → ρ′ is legitimate, and no floor φ₀ is needed. This is
  identical to B_tail_approx Steps 2–3 with r = 0 ✓.
- `thm:Ta` on 𝓑_n with S₀ ∈ Ω ✓. c♯ = κ²/(c_IGσ²) ✓.
- Λ″ ≤ √t + t/√n + (1+ε₁)/2 + B/(2σ²), and √t ≤ t/4 (t ≥ 16), t/√n ≤ t/4 (n ≥ 16). The final bound
  2c♯e^{1+B/(2σ²)}n^{−1/2}e^{−1.5t} ≤ e^{−1.5t} follows by (g) ✓.

**§5 X3.**
- The Q_S expansion and M_S ⪯ P_S are correct ✓.
- 2√(2C_xλ_S) ≤ λ_S/2 ⇔ λ_S ≥ 32C_x ✓. Then λ_S(1 − ½ − ⅛ − ⅛) = λ_S/4 ✓.
- 2b + Q_{S₀} ≤ b̄ + B + Nσ²(1+ε₁) ≤ 2Nσ² by (e) ✓.
- log(1+u) ≥ (log 2)min(u,1) and ν ≥ n/2 give ≥ min{(n/2)log 2, (log 2)Λt·n/(16N)} ✓. The minimum is the second term,
  since Λt ≤ 8n. Then (log 2)Λ/16 ≥ 3 ✓.
- Final bound: 2(2p)^{s₀}(n+1)^{s₀/2}e^{−3t} ≤ 2^{s₀+1}e^{−2t} ≤ e^{−t} ✓.

**§6 X2.**
- ‖M_Se‖ ≤ ‖P_Se‖ ✓.
- |Q_S − ‖e‖²| ≤ σ²t(C_P + 2√(2C_xΛ) + Λ) ✓.
- |2b + Q_S − nσ²| ≤ b̄ + σ²C_Qt + σ²(2√(Nt)+2t) + σ² ✓. Then (b̄/σ²+1)/n ≤ (b̄/σ²+1)√(t/n) ✓, which gives C_β ✓.
- Gamma tail: 0.02 + 2√((n+0.02)t) + 2t ≤ 4.03√(nt) ≤ 6√(nt) ✓.
- |g| ≤ 6n^{−κ₀/2} ≤ 6/C_v ≤ ½ ✓. |(1+a)/(1+g) − 1| ≤ 2(|a|+|g|) ✓. v ≤ 2σ² by (f) ✓.
- θ-step: N(0, vM_S), and the MGF argument of `lem:chi`(a) applies to ξᵀM_Sξ directly ✓.
- 4σ²(2C_d + 4 + C_P + Λ)t ≤ Cσ²t ✓.
- ‖X_Sθ − μ‖ = ‖X_{c,S}θ − μ_c‖, since both vectors lie in range C ✓.

**§7.**
- The four classes partition Ω, since min(d_t, K) ≤ m_n(t) ✓.
- Posterior mass: e^{−1.5t} + 5e^{−t} ≤ e^{−t/2} for t ≥ 3.6 ✓.
- Probability: 7e^{−t} ≤ 2e^{−t/2} for t ≥ 2.5 ✓.
- The result matches STATEMENT §3 exactly:
  - the three-part bad set, with d_t = s₀ + ⌈32t/log n⌉;
  - threshold e^{−t/2};
  - probability 2e^{−t/2};
  - c = ½;
  - constants in (s₀^r, A, σ², M, M′, c_D, κ₀), with c_D only in n₀ (via (d)) and through min(c_D, 1).
- s₀ = 0 holds at every step:
  - ρ′ = 0, S₀ = ∅, D_∅ = 1, 1/w(0) = 2;
  - Step 4 has no non-supersets (A_n = 2 is harmless);
  - `lem:prior`(e) with s₀ = 0 holds;
  - `lem:den` holds with Q_∅ = ‖e‖².
- S₀ ∈ Ω is used in Step 4, §5 and §4 (`thm:Ta`), and is guaranteed by s₀ ≤ K ✓.

**§9 X′.**
- (E4′): x_k ≤ C_m t(A+1)log n + (C_m + 2)t ≤ (C_m(A+2)+2)t′ ✓.
- Far′: Δ ≥ σ²t′λ_S/4, with B/(σ²t′) ≤ B/σ² ✓. ν log(·) ≥ 3t′ ≥ 3t given Λ′t′ ≤ 8n and 2b + Q_{S₀} ≤ 2Nσ² ✓.
- Good′:
  - t′/n = √(t/n)·√(t/n)log n ≤ √(t/n) once √(t/n)log n ≤ n^{−κ₀/2}log n ≤ 1 ✓.
  - 2√(Nt) + 2t ≤ 4√(nt) ✓.
  - θ-step: 2|S|log 2 + 4t ≤ (2C_m + 4)t ≤ (2C_m + 4)t′ ✓.
  - t′ = t log n ≤ tℓ_n, since ℓ_n = log(p_raw ∨ n) ≥ log n. Only this is used, so the thresholds may use ℓ_n ✓.
- {|S| > m}: §4 is used unchanged; it uses no (ND) ✓.
- Assembly: e^{−1.5t} + 4e^{−t} ≤ e^{−t/2} and 6e^{−t} ≤ 2e^{−t/2} ✓.
- p ≤ n^A is still used ((N2), (N3), (E4′), Far′). This is consistent with STATEMENT's fixed-design setting for X′.
- Missing definitions: F2.

## Citations of [P1] (item 2)
All exist with the content used:
- `lem:slab`: min-representation and the conditional law N(nH⁻¹Aᵀy, nvH⁻¹).
- `lem:spec`:
  - (b) 0 ⪯ M ⪯ (n/(n+1))P and Q ≥ ‖(I−P)Y‖²;
  - (d) monotonicity in the column set;
  - (e) D = Πf(λ_i), 1 ≤ f < n+1, Cauchy interlacing.
- `lem:prior`:
  - (b) w(k+1)/w(k) = (k+1)/(2p−k−1) for k ≤ p−1;
  - (c) used in its proof-line form (F4);
  - (e) requires j ≥ 1 and s₀ + j ≤ p, both satisfied.
- `lem:chi`(a): r ≤ d.
- `lem:num`: needs data-free b; b₋ is data-free ✓. Only Gaussianity and f₀ > 0 are used, not R's floor.
- `thm:Ta`: needs 𝓑_n, given by (E2), and S₀ ∈ Ω.
- `thm:T01i`: posterior form and conditionals; b = b₀s_y², ν = 0.51 + N/2.
- Proof of `lem:den`: R_n → ρ′ legitimate, as above.

The constants b₋ = b₀σ²/2, b₊ = b₀(2(σ²+M)+1), κ = (b₊/b₋)^{0.51} and c_IG = min_{[σ²,2σ²]}IG(·; 0.51, b₊) match [P1] §1 and
`lem:den`.

## Comparison derivations (item 6)
- **𝓑_n upper bound.** X-b-2 §2.3 (N1) derives s_y² ≤ 2(σ²+M)+1 from ‖y_c‖² ≤ 2nM + 2‖e‖². That gives only
  s_y² ≲ 3M + 2σ², which exceeds 2(σ²+M)+1 when M > 1. So X-b-2's step is wrong as written. X.md (E2) is right: it uses
  (N3) at S = ∅ and the split ‖μ‖²/3 + 12σ²t, which gives 2M + 2σ². X-a-1 avoids the issue by enlarging b₊ to b₀(3M+4σ²)
  and using `thm:T01ii` directly. That is valid, but it is not [P1]'s 𝓑_n.
- **Λ″ bound.** X-b-2 Step A writes E′/(2n) ≤ ½. The correct bound is ≤ (1+ε₁)/2. X.md's "≤ 1" is right. The slip is
  harmless in X-b-2.
- **n₀ definition.** X-a-2's form ("least n beyond which all hold") is the correct one. X.md should adopt it (F1).
- **Far step.** Route a's log(1+x) ≥ min(x,1)/2 and X.md's (log 2)min(u,1) are both valid. X.md's is sharper.
- **Superset bound.** Route a's −log(1−x) ≤ x/(1−x) step and X.md's (Q₀/Q_J)^ν ≤ e^{νΔ/Q_J} give the same bound.
- **No other disagreements.** I found no other disagreement on a step both proofs need. In particular:
  - the size-tail instance (§4 vs X-a-1 §5, X-a-2 T6, X-b-2 Step A);
  - the union device for non-supersets (§3 Step 4 vs route a §3(a), X-a-1 (6a));
  - the Far/Good bounds.

  All agree up to constants.

## Not checked
- The external tail inequalities (BLM 2013 §2.4; Laurent–Massart 2000 Lemma 1). I checked their content: I re-derived the
  sub-gamma MGF bounds and the Chernoff consequences. I did not check them against the printed sources.
- §8 R1's determinant chain (F6).
- §10's [P1] line numbers.

## Verdicts
- §1 V(a): **VERIFIED**
- §2 X1: **VERIFIED**
- §3 X4(b,c): **VERIFIED** (NIT F3)
- §4 X4(a): **VERIFIED** (NIT F4)
- §5 X3: **VERIFIED**
- §6 X2: **VERIFIED**
- §7 assembly: **VERIFIED-WITH-AMENDMENTS** (F1: n₀ must be defined as valid for all n ≥ n₀)
- §9 X′: **VERIFIED-WITH-AMENDMENTS** (F2: define C₁′, C_v′, C, M₀′, and a c_D-free n₀′ including (f′))

**Overall verdict: VERIFIED-WITH-AMENDMENTS. No CRITICAL or MAJOR findings; the amendments are F1 and F2 (MINOR) plus
four NITs.**
