# W5-VMASK — REPAIRS (fixable gaps found while refereeing W3-PXN and W4-T38FULL)

Every item here is a **candidate**. The proofs were written and checked line by line in this run only. Notation follows
`00_COMMON.md`, W3-PXN `PROOF.md` (§ numbers "PXN §k") and W4-T38FULL `T38_PROOF.md`. To avoid a clash with Euler's
number, the T22 deletion quantity of the reference S° is written **e_T** here; PXN writes it e. **H** = H₀ is the
tier-0 pilot population size. **𝒩** is the set of neutral variables of PXN §0: l ∉ S₀ and l ∉ C_b for every masked
group C_b.

| # | Where | Kind | Status after repair |
|---|---|---|---|
| R1 | PXN P7 (D2-d, NB) on LH-iid, c = 1 | GAP (fixable): the step was a PROOF SKETCH | PROVED (candidate, this run) |
| R2 | PXN Lemma U (U1): "ν log(1 + a_A/RSS^y_A) ≤ 1" | ERROR (cosmetic): the number is wrong, the argument is not affected | repaired |
| R3 | PXN P7 statement: NB with the constant 1.925 | GAP (cosmetic, inherited from W1-T38E) | repaired (NB′ or r*) |
| R4 | PXN §9.3 remark and REPORT §6: "(L) fails ≈ 4% at n = 200, 1.2% at n = 1600" | ERROR (numerical, cosmetic) | corrected numbers |
| R5 | T38FULL Prop. LH-LAT: "m₀ … which is sharp" | GAP (overstatement) | restated |
| R6 | PXN Lemma B, extension used by R1 and PXN §10 (2) | GAP (cosmetic: the extension is stated only implicitly) | stated |
| R7 | LS0 cost (W1-T38E E3, quoted in T38 (c)) | GAP (cosmetic, +1) | corrected |

---

## R1. D2-d (no first-stage blow-up) on LH-iid with c = 1 — PROVED (candidate)

**Statement.** On LH-iid with c = 1 (PXN §0; any 1 ≤ a ≤ A, any fixed v ≥ 0, g with g ≤ B_n < 2g), let X₁, …, X_H
be the H = H₀ = ⌈512 N₀/2500⌉ initial iid π₀ draws of the tier-0 pilot, with N₀ = max(2500, n, p). Then

  P( max_i d(X_i) − min_i d(X_i) > T₀ log r* ) → 0,  r* = (11 + 2√10)/9 ≈ 1.92495,

so NB holds with W3-VT38E's constant r*. NB′ (the ESS form) holds a fortiori. Together with PXN P7 (D2-a, b, c),
Theorem D2 (W1-T38E, repaired by W3-VT38E) gives P(S₀ ∉ 𝒮_cal) → 0 for c = 1, with no method change.

**Proof.** Put k₀ := ⌈2A⌉, so k₀ + 1 > 2A, and 𝒢 := {S° ∪ P : P ⊆ 𝒩, |P| ≤ k₀}.
Work on the X-measurable event 𝒜_n of PXN §0, on which blocks = groups and P2(a) holds. P(𝒜_n) → 1 by P1 and P2.
Use unnormalised weights γ(S) := w(|S|)∏_b r_b(S ∩ C_b) for every S ⊆ [p], so π₀(S) = γ(S)/Z̄₀ for |S| ≤ K,
with Z̄₀ = Σ_{|S|≤K} γ(S). Recall that S° ∩ C_h is {j_h} for the a-group and the visible groups, and ∅ otherwise.

*Step 0 (two facts from the definitions).*
- (F-a) For P ∩ S° = ∅ with |P| = k and s + k ≤ p,
  Σ_{|P|=k} γ(S° ∪ P) ≤ γ(S°)·[w(s+k)/w(s)]·[z^k]∏_b(Σ_j a_bj z^j) ≤ γ(S°)·((s+k)/p)^k·((p−s)q)^k/k!
  ≤ γ(S°)·(e(1+s)q)^k, where e here is Euler's number.
  Proof. The first inequality is the block factorisation of γ. In the second, a_bj ≤ D_b^j/j! (definition of D_b), so
  each factor is dominated coefficientwise by exp(D_b z). The product is then dominated by exp(z(p−s)q), whose k-th
  coefficient is ((p−s)q)^k/k!. Also w(s+k)/w(s) = ∏_{i<k}(s+i+1)/(2p−1−s−i) ≤ ((s+k)/p)^k. The third inequality uses
  (s+k)^k/k! ≤ (e(s+k)/k)^k ≤ (e(1+s))^k. This is PXN §10 (iii), written out.
- (F-b) For S ⊆ [p] with W := S° ∖ S ≠ ∅ and T := S ∪ S°: γ(S) ≤ e_T^{|W|}·γ(T).
  Proof. Each block meeting W carries exactly one reference variable, so by the definition of e_T,
  r_b(S ∩ C_b)/r_b(T ∩ C_b) ≤ e_T/(2p). Also w(k)/w(k+1) = (2p−1−k)/(k+1) ≤ 2p.

*Step 1: the draws avoid 𝒢ᶜ.* Every S ∈ Ω ∖ 𝒢 lies in one of the following sets.
- E1 = {S ⊉ S°}.
- E3 = {S ⊇ S° : |S ∖ S°| > k₀}.
- E2 = {S ⊇ S° : |S ∖ S°| ≤ k₀, S ∩ C_b ≠ ∅}.

This covers everything because the only non-neutral variables outside S° lie in C_b. Each set is bounded as follows.
- **E1.** The map S ↦ (T, W) is injective, and |T| ≤ K + s. By (F-b), on {e_T ≤ 1},
  Σ_{S∈E1}γ(S) ≤ e_T·2^s·Σ_{T⊇S°, |T|≤K+s}γ(T). Split the last sum at |T| = K:
  - the part with |T| ≤ K is at most Z̄₀;
  - the part with |T| > K is at most γ(S°)Σ_{k>K−s}(e(1+s)q)^k by (F-a), since s + k ≤ p (p ≥ n ≥ 2K).

  On {e(1+s)q ≤ ½} this gives π₀(E1) ≤ 2^{s+1}e_T.
- **E3.** By (F-a), π₀(E3) ≤ Σ_{k>k₀}(e(1+s)q)^k ≤ 2(e(1+s)q)^{k₀+1} on {e(1+s)q ≤ ½}.
- **E2.** Write S = S° ∪ R ∪ V with V = S ∩ C_b ≠ ∅, R ⊆ 𝒩 and |R| + |V| ≤ k₀. Since C_b is a block with empty
  reference, γ(S) = γ(S° ∪ R)·[w(m+j)/w(m)]·r_b(V), with m = s + |R| and j = |V|. Also
  w(m+j)/w(m) ≤ ((s+k₀)/p)^j. Summing over V and then over R (Σ_R π₀(S° ∪ R) ≤ 1) gives
  π₀(E2) ≤ Σ_{j=1}^{g}((s+k₀)/p)^j a_bj, with a_bj = Σ_{|V|=j}r_b(V).

Multiply each bound by H. For p ≥ 2500, H ≤ 0.205p + 1.
- **E1.** H·π₀(E1) ≤ p·2^{s+1}e_T = O_P(p²√n e^{−c₆n}) → 0 (PXN P3).
- **E3.** H·π₀(E3) ≤ 2p(e(1+s)q)^{k₀+1} = O_P(n^A(log n/n)^{(k₀+1)/2}) → 0, since q = O_P(√(log n/n)) (P3) and
  k₀ + 1 > 2A.
- **E2.** H·π₀(E2) ≤ (s+k₀)^g Σ_j a_bj ≤ (s+k₀)^g(e^{D_b} − 1). PXN P3's moment bound applies to the b-group
  (U° = ∅): E[D̃_b 1_{𝒢_n}] ≤ 1.14C_e g²ξ_n = O(√(log n/n)). So this term is O_P(√(log n/n)) → 0.

Conditionally on the data, P(∃ i: X_i ∉ 𝒢) ≤ min{1, H·π₀(𝒢ᶜ)} → 0 in probability. By bounded convergence, the
unconditional probability → 0 as well.

*Step 2: d varies by O(log n) on 𝒢.* Take S = S° ∪ P ∈ 𝒢 and add the elements l₁, …, l_k of P (k ≤ k₀) one at a
time: T₀ = S°, T_i = T_{i−1} + l_i. With b = b(l_i) and U_i := T_{i−1} ∩ C_b ⊇ U_b*,

  d(T_i) − d(T_{i−1}) = [log BF(T_i) − log BF(T_{i−1})] − [log r_b(U_i + l_i) − log r_b(U_i)].

Expand both brackets.
- **Full-set bracket.** W1-EXP Lemmas 1.1–1.3 apply to the pair (T_{i−1}, T_i): their proofs use only
  λ_min(G) ≥ φ₀²(n−1) on these sets, and P2(a) gives that because |T_i| ≤ s + k₀ ≤ m_n + s₀. Lemma 1.4 applies with
  the union bound taken over all sets of size ≤ s + k₀ + 1, whose number is ≤ (p+1)^{s+k₀+1}, with L > 4A(s+k₀+2).
  Together they give −½log(n+1) − ν log(1 − x^full_i) + R^full_i, with |R^full_i| ≤ κ′ on a ε-event of probability → 1.
  Here x^full_i := 1 − RSS_{T_i}/RSS_{T_{i−1}}.
- **Block bracket.** EXP′ (W1-EXP Thm 1, on 𝒜_n) gives −½log(n+1) − ν log(1 − x^blk_i) + R^blk_i, with |R^blk_i| ≤ κ_EXP.

The −½log(n+1) terms cancel. The two Beta laws are:
- x^full_i ~ Beta(½, (n−2−|T_{i−1}|)/2), by Lemma B(ii) (T_{i−1} ⊇ S°, T_{i−1} ∖ S° ⊆ 𝒩, l_i ∈ 𝒩);
- x^blk_i ~ Beta(½, (n−2−|U_i|)/2), by Lemma B(i′) of R6.

The family of all (T_{i−1}, l_i) and (U_i, l_i) that occur has at most (p+1)^{k₀+1} + G2^g g ≤ n^{A(k₀+1)+1} members
for large n. Lemma Tr(c), with A replaced by A′ := A(k₀+1) (its proof only uses the size of the family), gives
max x ≤ τ′_n := t′_n/n w.p. → 1, with t′_n = 4(A′+3) log n. For x ≤ ½ we have |log(1−x)| ≤ 2x, so

  |d(S) − d(S°)| ≤ k₀·[ν·4τ′_n + κ′ + κ_EXP] ≤ k₀[2.1 t′_n + κ′ + κ_EXP] =: Λ_n/2 = O(log n),

uniformly over S ∈ 𝒢.

*Step 3: comparison with the threshold.* T₀ = max(1000, ℓ²) with ℓ = ⌈log₂(n+p+1)⌉ ≥ log₂ n, so
T₀ log r* ≥ 0.6549·max(1000, log₂²n). Since Λ_n = O(log n), we have Λ_n < T₀ log r* for all large n. On the
intersection of the events of Steps 1 and 2, every draw lies in 𝒢 and the d-range is ≤ Λ_n. ∎

*Remark.* The proof also covers c ≥ 2 verbatim (the masked groups are handled like C_b in E2). For c ≥ 2, however,
D2 itself does not apply: its reference must be at Gibbs distance 1 from S₀. So the no-tweak route stays OPEN for
c ≥ 2, as PXN says.

## R2. PXN Lemma U (U1): the constant of the Q-correction

PXN writes ν log(1 + a_A/RSS^y_A) ≤ ν(1.02 + 1/(nφ₀²))/(c_*n) ≤ 1. The last inequality is false.
c_* = σ²/(8(M + 2σ²)) ≤ 1/16, so the middle term is about 0.51/c_* ≥ 8. **Repair:** replace "≤ 1" by "≤ 0.52/c_* + o(1)"
and define κ₂ := ½ sup_n (s₀+2)(1+φ₀⁻²)/(φ₀²(n−1)) + 0.52/c_* + 1. Nothing downstream uses the value of κ₂: it enters
only as an O(1) term against Θ(n) or −½log n + O(log log n) margins.

## R3. The NB constant in PXN P7

PXN's D2-d is written with T_e log 1.925, but W3-VT38E showed that 1.925 does not guarantee ESS ≥ 0.9H.
**Repair:** use r* = (11+2√10)/9, or W3-VT38E's NB′ directly. R1 is written with r*. The change has no effect here,
because the d-range is O(log n) against a threshold of order log²n.

## R4. The (L)-failure numbers

PXN's formula is P((L) fails) ≈ (s₀+1)/√(2π(n+1)t_n), with t_n = 2log((2p−s₀−1)/(s₀+1)) + log(n+1). For config A
this formula gives 2.7% at (200, 750), 1.8% at (400, 1790), 1.2% at (800, 4260) and 0.8% at (1600, 10120).

PXN quotes ≈ 4% at n = 200 and 1.2% at n = 1600. Those figures come from a threshold computed differently in its
script (16.3 instead of 17.15 at n = 200; 23.6 instead of 24.4 at n = 1600). Exact simulation with this run's own
scorer (`scripts/L_failure.py`) gives:
- 2.47% (74/3000) at n = 200;
- 1.47% (22/1500) at n = 400;
- 0.8% (4/500) at n = 800.

These agree with the formula as written. **Repair:** quote 2.7% and 0.8% (the formula), or the simulated rates.
The qualitative statement (an n^{−1/2}(log n)^{−1/2} rate, certification slower than scoring) is unaffected.

## R5. LH-LAT: "sharp"

m₀ = min{(1−κ_max)R_min, min_iβ_i²(1−ψ_i²)², min_hθ_h²} is a valid lower bound on the Φ ≥ 2 population margin.
On the brute-force grid (`results/margins_grid.txt`), it equals that margin in all 108 homogeneous settings
(common ψ, common |β|). In the heterogeneous settings it is strictly below the margin in 32/94 cases, down to a factor
of 0.002. The reason: the binding proxy term is R_{i*} − max_{i∈I}κ_iR_i, with i* = argmax_{i∈I}R_i, and
(1−κ_max)R_min can be far below it.

**Repair:** say "valid, and sharp when the pairs are homogeneous". The exact Φ ≥ 2 margin is

  m₀^♯ = min over I ⊆ [c] with |I| ≥ 2 of min{ R_{i*(I)} − max_{i∈I}κ_iR_i ,
          min_{t, i ∈ I} [del_t(S_I + b_i) + R_{i*(I)} − R_i] },

where S_I := S° ∪ {b_k : k ∉ I}, del_t is the deletion increase of the truth t at that state, and t ranges over
the truths of S_I. The brute force computes exactly this minimum. Nothing in Theorem b1 depends on sharpness.

## R6. Lemma B(i′) (used in R1 and implicitly in PXN §10 (2))

**Statement.** Let h be a null, visible or a-group, let U ⊆ C_h with U ⊇ U_h°, and let l ∈ C_h ∖ U with l neutral.
Then x^blk_{U,l} := 1 − RSS_{U+l}/RSS_U ~ Beta(½, (n−2−|U|)/2), independent of (X_U, y).

**Proof.** This is PXN Lemma B's argument with W = {l} and conditioning set U. Its covariance identity is the
"a-group, U ∋ j_a" bullet of PXN §4, which already allows U to contain other members of C_a: weak union applied to
C_b ⊥ (C_a ∖ j_a) | x_{j_a}. The visible and null cases are immediate. The Grassmannian step is unchanged. ∎

Checked numerically as statistics B2 (U = {j_a}, three non-hubs), B5 and B6 in `results/ks_lemmaB.txt`.

## R7. LS0 cost

The local search evaluates its centre once when the centre is emitted, plus at most ℓ + 1 scans, each of
≤ p + k(p−k) neighbours. The LS0 term in T38 (c) and W1-T38E E3 should therefore read
1 + (ℓ+1)·max_{k≤K}[p + k(p−k)]. This is immaterial asymptotically.
