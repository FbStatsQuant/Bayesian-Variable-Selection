# B — Corollary B: a sparsity obstruction on every design (W3-PSHARP, Claim B)

Status: **PROVED (by this seat, unchecked)**. Check record: see `../REPORT.md` §2.
Notation: `../STATEMENT.md` §0, §3. Uses only Lemma S(1), (2) (`S_one_step.md`).

## Statement
For every n ≥ 3, every standardised design with p ≥ 2, every data set and every S₀ ⊆ [p] with 0 ≤ s₀ ≤ K − 1:
  δ_n/(1 − δ_n) ≥ 𝒪^{lb}_n := Σ_{j=1}^{K−s₀} C(s₀+j, j) n^{−j/2} Π_{i=0}^{j−1} (p − s₀ − i)/(2p − 1 − s₀ − i) ≥ c(p, s₀)/√n,
c(p, s) = (s+1)(p−s)/(2p−1−s); equivalently π(S₀) ≤ 1/(1 + 𝒪^{lb}_n), and in particular π(S₀) ≤ √n/(√n + c(p, s₀)). Moreover c(p, s₀) ≥ (s₀+1)/3 if s₀ ≤ p/2;
c(p, s₀) ≥ 1 if s₀ ≥ 1; c(p, 0) > ½; c(p, s₀)/(s₀+1) → ½ if p → ∞ and s₀/p → 0.

## Proof
Fix 1 ≤ j ≤ K − s₀ and J ⊆ [p]∖S₀ with |J| = j; S_J := S₀ ∪ J ∈ Ω and (normalising constant cancelled)
  π(S_J)/π(S₀) = [w(s₀+j)/w(s₀)] · (D_{S₀}/D_{S_J})^{1/2} · ((2b₀ + Q_{S₀})/(2b₀ + Q_{S_J}))^{ν}.
Adding the columns of J one at a time, Lemma S(2) gives Q_{S_J} ≤ Q_{S₀}, so the last factor is ≥ 1, and Lemma S(1)
gives D_{S_J}/D_{S₀} ≤ n^{j}. (Lemma S is applied to intermediate sets of size ≤ s₀ + j − 1 ≤ K − 1.) Hence
π(S_J)/π(S₀) ≥ [w(s₀+j)/w(s₀)] n^{−j/2}. There are C(p − s₀, j) such J (j ≤ K − s₀ ≤ p − s₀); the models S_J are
distinct and different from S₀; so
  δ_n/(1 − δ_n) = Σ_{S≠S₀} π(S)/π(S₀) ≥ Σ_{j=1}^{K−s₀} C(p − s₀, j) [w(s₀+j)/w(s₀)] n^{−j/2}.
Prior: w(s₀+j)/w(s₀) = C(2p−1, s₀)/C(2p−1, s₀+j) = [(s₀+j)!/s₀!] / Π_{i=0}^{j−1}(2p−1−s₀−i), and
C(p−s₀, j) = Π_{i=0}^{j−1}(p−s₀−i)/j!. Their product is C(s₀+j, j) Π_{i=0}^{j−1}(p−s₀−i)/(2p−1−s₀−i): this is 𝒪^{lb}_n.
All terms are positive and the j = 1 term is (s₀+1)(p−s₀)/((2p−1−s₀)√n) = c(p, s₀)/√n. Since π(S₀) = 1/(1 + δ_n/(1−δ_n)),
π(S₀) ≤ 1/(1 + 𝒪^{lb}_n) ≤ 1/(1 + c/√n).

Constants. (i) s₀ ≤ p/2: (p−s₀)/(2p−1−s₀) ≥ 1/3 ⟺ 3p − 3s₀ ≥ 2p − 1 − s₀ ⟺ p + 1 ≥ 2s₀. (ii) s₀ ≥ 1:
c ≥ 1 ⟺ (s₀+1)(p−s₀) ≥ 2p−1−s₀ ⟺ (s₀−1)(p−s₀−1) ≥ 0, true since p ≥ s₀ + 1. (iii) c(p, 0) = p/(2p−1) > ½.
(iv) c/(s₀+1) = (1 − s₀/p)/(2 − (1+s₀)/p) → ½ when p → ∞ and s₀/p → 0. ∎

## Consequences (sequences with s₀ ≤ min(K − 1, p/2); any designs; any data)
Put a_n := (s₀+1)/(3√n), deterministic. By the above, **for every data set**, δ_n/(1−δ_n) ≥ a_n, i.e.
π(S₀) ≤ 1/(1 + a_n) and δ_n ≥ a_n/(1 + a_n).
- **B1.** If π(S₀) → 1 in probability along a subsequence, then 1/(1 + a_n) → 1 along it (a deterministic upper bound of
  a sequence converging to 1 in probability), so s₀ = o(√n) there. If s₀ ≥ λ√n: a_n ≥ λ/3 and π(S₀) ≤ 1/(1 + λ/3). If
  s₀/√n → ∞: π(S₀) ≤ 1/(1 + a_n) → 0, surely.
- **B1, critical scale.** Let s₀/√n → λ ∈ (0, ∞) and s₀/p → 0 (so s₀ → ∞, p → ∞, and K − s₀ → ∞ because
  s₀ = o(n) and p − s₀ → ∞). Fix j ≥ 1. For n large, j ≤ K − s₀, and the j-th term of 𝒪^{lb}_n is
  C(s₀+j, j) n^{−j/2} Π_{i<j}(p−s₀−i)/(2p−1−s₀−i) → (λ^j/j!)·2^{−j}: C(s₀+j, j) n^{−j/2} = Π_{l=1}^{j}((s₀+l)/√n)/j! → λ^j/j!, and each
  of the j factors (p−s₀−i)/(2p−1−s₀−i) = (1 − (s₀+i)/p)/(2 − (1+s₀+i)/p) → ½. All terms are ≥ 0, so for every J:
  liminf 𝒪^{lb}_n ≥ Σ_{j=1}^{J}(λ/2)^j/j!; letting J → ∞, liminf 𝒪^{lb}_n ≥ e^{λ/2} − 1, and
  limsup π(S₀) ≤ limsup 1/(1 + 𝒪^{lb}_n) ≤ e^{−λ/2}, for every sequence of designs and data sets.
- **B2.** Let ρ_n → 0 be deterministic and δ_n = O_P(ρ_n): there is C with P(δ_n ≤ Cρ_n) ≥ ½ for all large n. On that
  (nonempty) event a_n/(1 + a_n) ≤ δ_n ≤ Cρ_n; a_n is deterministic, so a_n/(1+a_n) ≤ Cρ_n for all large n, hence
  a_n ≤ 2Cρ_n eventually: s₀ + 1 = O(√n ρ_n). With ρ_n = r_n: s₀ = O(√(log n)). The claim "s₀ = O(1) on the witness
  sequences of Corollary A2 with log p ≍ log n" is proved in `A_log_factor.md` §6.
- **B3** is a reading of B1, B2 and Corollary A2 (no further mathematical content): on the witness sequences of
  Corollary A2 with log p ≍ log n the rate r_n cannot hold with s₀ → ∞; there any concentration theorem must allow the
  rate (s₀+1)√(log p/n), and π(S₀) → 1 needs s₀ = o(√(n/log p)); on every design, π(S₀) → 1 needs s₀ = o(√n).

## Remarks
1. **Relation to the parents (not used above).** The first display is `W3-POST2:A2` (δ_n ≥ 𝒪⁰_n/(1 + 𝒪⁰_n)) with
   D_{S_J}/D_{S₀} ≤ n^{|J|} inserted, i.e. 𝒪⁰_n ≥ 𝒪^{lb}_n. Its j = 1 term with c(p, s₀) ≥ 1 is [LB] with n in place of
   n + 1, on [LB]'s domain (1 ≤ s₀ < p, s₀ + 1 ≤ K), without s₀ ≤ p/2; s₀ = 0 is added (constant > ½).
2. **Equality.** If X is orthogonal and y ⟂ col X, every D ratio is n and every fit factor is 1, so the superset odds
   equal 𝒪^{lb}_n exactly (`../numerics/b_check_out.txt`, F2, "equality case": 1.000000000000).
3. **Size of the full sum.** Table T1 of `b_check_out.txt` agrees with the critical-scale limit of B1 (e.g. λ = 4,
   p = 10n: 1/(1 + 𝒪^{lb}_n) = 0.1353 at n = 10⁶, e^{−2} = 0.1353, against the j = 1 cap 0.3333).
4. **Falsification.** `../numerics/b_check.py` F2: 55,740 triples (design, data, S₀) — every S₀ with s₀ ≤ K − 1, not
   only a true support; iid, equicorrelated, duplicated, near-duplicated, orthogonal and binary designs; null, sparse,
   dense, near-exact and Cauchy responses; n from 6 to 5000 — minimum of odds/𝒪^{lb}_n = 1.033.
